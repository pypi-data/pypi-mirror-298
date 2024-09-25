import pandas as pd
import numpy as np
import datetime as dt
from lifetimes import GammaGammaFitter, BetaGeoFitter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import csr_matrix

# Column synonyms dictionary
column_synonyms = {
    'invoiceno': ['InvoiceNo', 'Invoice', 'BillNo'],
    'invoicedate': ['InvoiceDate', 'Date', 'BillDate'],
    'description': ['Description', 'Product', 'Item', 'Goods'],
    'quantity': ['Quantity', 'Qty', 'Amount', 'Units'],
    'unitprice': ['UnitPrice', 'Price', 'Amount', 'Rate'],
    'customerid': ['CustomerID', 'CustID', 'ClientID'],
    'country': ['Country', 'Location', 'Region']
  
}

def detect_column(column_names, expected_column):
    """
    Automatically detect the correct column based on synonyms.
    """
    synonyms = column_synonyms.get(expected_column, [])
    
    # Try to match the column by checking common synonyms
    for synonym in synonyms:
        for col in column_names:
            if synonym.lower() in col.lower():
                return col
    
    # If no match is found, return None (requires user input)
    return None

def prompt_user_for_column(expected_column, column_names):
    """
    Prompt the user to manually map a column if auto-detection fails.
    """
    print(f"Unable to detect the column for {expected_column}. Please choose from the following columns:")
    print(column_names)
    user_input = input(f"Please type the column name for {expected_column}: ")
    
    if user_input in column_names:
        return user_input
    else:
        print(f"Invalid input. Using default mapping for {expected_column}.")
        return None


# Define the function to find the top N customers likely to attrition
def map_columns(df):
    column_mapping = {}
    for expected_column in column_synonyms.keys():
        detected_column = detect_column(df.columns, expected_column)
        if detected_column:
            print(f"Auto-detected '{detected_column}' as the column for {expected_column}")
            column_mapping[expected_column] = detected_column
        else:
            user_input = prompt_user_for_column(expected_column, df.columns)
            if user_input:
                column_mapping[expected_column] = user_input
    return column_mapping

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    iqr = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * iqr
    low_limit = quartile1 - 1.5 * iqr
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[dataframe[variable] < low_limit, variable] = round(low_limit, 0)
    dataframe.loc[dataframe[variable] > up_limit, variable] = round(up_limit, 0)
# Merge the attrition identification into the overall CLTV process
def process_and_visualize_clv(df):
    column_mapping = map_columns(df)
    df.rename(columns={
        column_mapping.get('invoiceno', 'invoiceno'): 'invoiceno',
        column_mapping.get('invoicedate', 'invoicedate'): 'invoicedate',
        column_mapping.get('description', 'description'): 'description',
        column_mapping.get('quantity', 'quantity'): 'quantity',
        column_mapping.get('unitprice', 'unitprice'): 'unitprice',
        column_mapping.get('customerid', 'customerid'): 'customerid',
        column_mapping.get('country', 'country'): 'country'

    }, inplace=True)

    df.dropna(inplace=True)
    df = df[~df['invoiceno'].str.contains('C', na=False)]
    df = df[(df['quantity'] > 0) & (df['unitprice'] > 0)]

    replace_with_thresholds(df, 'quantity')
    replace_with_thresholds(df, 'unitprice')

    df['total_price'] = df['quantity'] * df['unitprice']
    df['invoicedate'] = pd.to_datetime(df['invoicedate'])
    today_date = dt.datetime(2011, 12, 11)

    cltv_df = df.groupby(['customerid', 'country']).agg({
        'invoicedate': [lambda x: (x.max() - x.min()).days, lambda x: (today_date - x.min()).days],
        'invoiceno': 'nunique',
        'total_price': 'sum'
    })

    cltv_df.columns = ['recency', 'tenure', 'frequency', 'monetary']
    cltv_df['monetary'] = cltv_df['monetary'] / cltv_df['frequency']
    cltv_df['recency'] = cltv_df['recency'] / 7
    cltv_df['tenure'] = cltv_df['tenure'] / 7
    cltv_df = cltv_df[cltv_df['frequency'] > 1]

    if cltv_df.empty:
        print("CLTV DataFrame is empty. Ensure sufficient data is available for each customer.")
        return pd.DataFrame()

    # Fitting the BG/NBD model
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    try:
        bgf.fit(cltv_df['frequency'], cltv_df['recency'], cltv_df['tenure'])
    except ValueError as e:
        print(f"BG/NBD model fitting error: {e}")
        return pd.DataFrame()

    cltv_df['expected_purch_1_week'] = bgf.predict(1, cltv_df['frequency'], cltv_df['recency'], cltv_df['tenure'])
    cltv_df['expected_purch_1_month'] = bgf.predict(4, cltv_df['frequency'], cltv_df['recency'], cltv_df['tenure'])
    cltv_df['expected_purch_3_month'] = bgf.predict(12, cltv_df['frequency'], cltv_df['recency'], cltv_df['tenure'])

    # Fitting the Gamma-Gamma model
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    try:
        ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
        cltv_df['expected_average_profit'] = ggf.conditional_expected_average_profit(cltv_df['frequency'], cltv_df['monetary'])
    except ValueError as e:
        print(f"Gamma-Gamma model fitting error: {e}")
        return pd.DataFrame()

    # Calculating CLTV
    cltv = ggf.customer_lifetime_value(
        bgf,
        cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['tenure'],
        cltv_df['monetary'],
        time=3,
        freq='W',
        discount_rate=0.01
    )

    cltv = cltv.reset_index()
    cltv_final = cltv_df.merge(cltv, on='customerid', how='left')
    cltv_final['segment'] = pd.qcut(cltv_final['clv'].fillna(0), 4, labels=['D', 'C', 'B', 'A'])

    return cltv_final