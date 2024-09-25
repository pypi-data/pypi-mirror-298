import pandas as pd

from .visualisation import visualize_rules_graph 
from .association_rules import generate_association_rules,generate_fpgrowth_rules,generate_eclat_rules


def mba(df, sample_size=10000):
    
    market_basket_df = df
    unique_clusters = market_basket_df['Cluster'].unique().tolist()
    print(unique_clusters)


    # Loop through each cluster and perform operations
    for cluster in unique_clusters:
        print(f"Processing Cluster {cluster}...")
        
        # Filter DataFrame for the current cluster
        cluster_df = market_basket_df[market_basket_df['Cluster'] == cluster]
          # Perform operations on the filtered DataFrame
        print(cluster_df.head())
        transaction_filtered = cluster_df[['InvoiceNo', 'Description', 'Quantity']].copy()
        transaction_filtered.sort_values(by='Quantity', ascending=True, inplace=True)
        transaction_filtered = transaction_filtered[transaction_filtered.Quantity > 0]
        transaction_filtered.sort_values(by='Quantity', ascending=True, inplace=True)
        transaction_filtered['Quantity'] = [1] * len(transaction_filtered)
        
        invoice = list(transaction_filtered.InvoiceNo)
        index_no = [inv for inv in invoice if isinstance(inv, str) and not inv.isnumeric()]
        filtered_transactions = transaction_filtered[transaction_filtered['InvoiceNo'].isin(index_no)]
        transaction_filtered = transaction_filtered[~transaction_filtered['InvoiceNo'].isin(index_no)]
        invoice = list(transaction_filtered['InvoiceNo'])
        index_no = [i for i, val in enumerate(invoice) if isinstance(val, str) and not val.isnumeric()]
        
        transaction_filtered = transaction_filtered[~transaction_filtered['InvoiceNo'].isin([invoice[i] for i in index_no])]
        
        temp_df = transaction_filtered[transaction_filtered.Description != transaction_filtered.Description]
        for invoice in list(temp_df.InvoiceNo):
            if len(transaction_filtered[transaction_filtered.InvoiceNo == invoice]) > 1:
                print(str(invoice))
                temp = transaction_filtered[transaction_filtered.InvoiceNo == invoice].groupby(['InvoiceNo']).agg({'Description': lambda x: list(x)})
                if len(list(set(temp))) > 0:
                    print(temp)
        
        transaction_filtered.dropna(axis=0, inplace=True)
        
        def return_one(x):
            return 1
        
        table = pd.pivot_table(transaction_filtered, values='Quantity', index=['InvoiceNo'],
                               columns=['Description'], aggfunc=return_one, fill_value=0)
        
        # Generate rules using the Apriori algorithm
        apriori_rules = generate_association_rules(table, min_support=0.02, metric="lift", min_threshold=2)
        print("Apriori Rules:")
        print(apriori_rules)
        # Visualize the Apriori rules
        if not apriori_rules.empty:
            fig = visualize_rules_graph(apriori_rules)
            fig.show()
        
        # Generate rules using the FP-Growth algorithm
        #fpgrowth_rules = generate_fpgrowth_rules(table, min_support=0.02, metric="lift", min_threshold=2)
        #print("FP-Growth Rules:")
        #print(fpgrowth_rules)
        
        # Generate rules using the Eclat algorithm
        #eclat_rules = generate_eclat_rules(table, min_support=0.02, metric="lift", min_threshold=2)
        #print("Eclat Rules:")
        #print(eclat_rules)

if __name__ == "__main__":
    example_df = pd.read_csv("data.csv", encoding='ISO-8859-1')  # Load an example DataFrame from a CSV file
    mba(example_df)