import pandas as pd
from mlxtend.frequent_patterns import fpgrowth,apriori, association_rules



# Step 1: Implement the Eclat algorithm to generate frequent itemsets
def eclat(df, min_support=0.04):
    rows_count = len(df)
    frequent_itemsets = {}

    # Initial pass: get frequent 1-itemsets
    for column in df.columns:
        support = df[column].sum() / rows_count
        if support >= min_support:
            frequent_itemsets[frozenset([column])] = support
    # Iteratively generate k-itemsets
    k = 2
    current_itemsets = list(frequent_itemsets.keys())

    while current_itemsets:
        next_itemsets = []
        for i in range(len(current_itemsets)):
            for j in range(i + 1, len(current_itemsets)):
                combined_itemset = current_itemsets[i] | current_itemsets[j]
                if len(combined_itemset) == k:
                    support = (df[list(combined_itemset)].all(axis=1).sum()) / rows_count
                    if support >= min_support:
                        frequent_itemsets[combined_itemset] = support
                        next_itemsets.append(combined_itemset)
        k += 1
        current_itemsets = next_itemsets

    # Convert to DataFrame
    frequent_itemsets_df = pd.DataFrame(list(frequent_itemsets.items()), columns=['itemsets', 'support'])
    return frequent_itemsets_df

def generate_association_rules(table: pd.DataFrame, min_support: float = 0.02, metric: str = "lift", min_threshold: float = 2, target_rule_count: int = 30):
    current_support = min_support
    rules = pd.DataFrame()  
    # Loop to adjust min_support until more than target_rule_count rules are found
    while len(rules) < target_rule_count and current_support > 0:
        frequent_itemsets = apriori(table, min_support=current_support, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
        
        # Check if the number of rules is sufficient
        if len(rules) >= target_rule_count:
            print(f"Found {len(rules)} rules with min_support={current_support}.")
            break
        
        # Decrease min_support for the next iteration
        current_support -= 0.001
        
        print(f"Reducing min_support to {current_support}...")

    # If no sufficient rules are found, return the last attempt
    if len(rules) < target_rule_count:
        print(f"Only {len(rules)} rules found after reducing min_support to {current_support}.")

    return rules

def generate_fpgrowth_rules(table: pd.DataFrame, min_support: float = 0.02, metric: str = "lift", min_threshold: float = 2):
    frequent_itemsets = fpgrowth(table, min_support=min_support, use_colnames=True)
    fpgrowth_rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    return fpgrowth_rules

def generate_eclat_rules(table: pd.DataFrame, min_support: float = 0.02, metric: str = "lift", min_threshold: float = 2):
    frequent_itemsets = eclat(table, min_support=min_support)
    print(frequent_itemsets)
    eclat_rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    return eclat_rules