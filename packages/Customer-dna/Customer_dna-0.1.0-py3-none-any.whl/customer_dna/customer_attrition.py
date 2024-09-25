from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from lifetimes import  BetaGeoFitter
from scipy.sparse import csr_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def predict_customer_attrition(cltv_df):
    """
    Predicts the probability of customer attrition using the BG/NBD model.
    Identifies at-risk customers and visualizes attrition probabilities.
    """
    # Re-fit the BG/NBD model if not already available
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'], cltv_df['recency'], cltv_df['tenure'])

    # Predict attrition probability (probability of being active)
    cltv_df['attrition_probability'] = 1 - bgf.conditional_probability_alive(
        cltv_df['frequency'], cltv_df['recency'], cltv_df['tenure']
    )

    # Display top at-risk customers
    top_risk_customers = cltv_df[['customerid', 'attrition_probability']].sort_values(by='attrition_probability', ascending=False).head(10)
    print("Top 10 At-Risk Customers (Most Likely to Stop Buying):")
    print(top_risk_customers)

    # Visualize attrition probability distribution
    sns.histplot(cltv_df['attrition_probability'], kde=True, color='orange')
    plt.title('Customer Attrition Probability Distribution')
    plt.xlabel('Attrition Probability')
    plt.ylabel('Frequency')
    plt.show()

    return cltv_df[['customerid', 'attrition_probability']]
# Default Recommendation Fallback: Top 5 Popular Products
def get_popular_products(df, top_n=5):
    popular_products = df['description'].value_counts().head(top_n).index.tolist()
    return popular_products

def next_best_product_recommendation(df, cltv_final, top_n=5):
    customer_product_matrix = df.pivot_table(index='customerid', columns='description', values='quantity', aggfunc='sum', fill_value=0)
    customer_product_matrix_sparse = csr_matrix(customer_product_matrix)

    scaler = MinMaxScaler()
    customer_product_matrix_scaled = scaler.fit_transform(customer_product_matrix)

    product_similarity = cosine_similarity(customer_product_matrix_scaled.T, dense_output=False)

    recommendations = {}
    popular_products = get_popular_products(df, top_n)

    for customer_id in customer_product_matrix.index:
        purchased_products = customer_product_matrix.loc[customer_id]
        purchased_products = purchased_products[purchased_products > 0].index.tolist()

        if not purchased_products:
            recommendations[customer_id] = popular_products
            continue

        product_scores = product_similarity.dot(customer_product_matrix.loc[customer_id].values)
        product_scores_series = pd.Series(product_scores, index=customer_product_matrix.columns)
        product_scores_series = product_scores_series[~product_scores_series.index.isin(purchased_products)]

        top_recommendations = product_scores_series.sort_values(ascending=False).head(top_n).index.tolist()
        if not top_recommendations:
            top_recommendations = popular_products

        recommendations[customer_id] = top_recommendations

    recommendations_df = pd.DataFrame.from_dict(recommendations, orient='index')
    recommendations_df.columns = [f"recommendation_{i+1}" for i in range(top_n)]

     # Merge with CLTV data, filling missing values if no match is found
    cltv_final['customerid'] = cltv_final['customerid'].astype(float)
    recommendations_df = recommendations_df.merge(
        cltv_final[['customerid', 'clv', 'segment', 'country']],
        left_index=True,
        right_on='customerid',
        how='left'
    ).fillna({'clv': 0, 'segment': 'D'})    
    
    recommendations_df = recommendations_df[recommendations_df['clv'] != 0]

    # Filter out rows with NaN or invalid customer IDs
    recommendations_df = recommendations_df[recommendations_df['customerid'].notna() & (recommendations_df['customerid'] != 0.0)]

    return recommendations_df