import pandas as pd
import numpy as np
import re
from pycaret.clustering import *
import matplotlib.pyplot as plt
import seaborn as sns

def display_unique_values(df):
    df.describe()
    df.isnull().sum()
    df[df['Description'].isnull()]
    df.dropna(subset=['CustomerID'], inplace=True)
    df[df['Description'].isnull()]
    df.isnull().sum()
    df.describe()
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    df.describe()
    print("We have", df.duplicated().sum(), "duplicates")
    # Display unique values for each column
    for column in df.columns:
        unique_values = df[column].unique()
        print(f"Unique values in column '{column}':")
        print(unique_values)
        print(f"Total unique values: {len(unique_values)}")
        print('-' * 50)

def find_columns_with_data(df, patterns):
    """
    Find columns in the dataframe that match the given regex patterns along with their corresponding data.
    
    Parameters:
    - df: DataFrame
    - patterns: List of regex patterns to search for

    Returns:
    - DataFrame with matched columns and corresponding data
    """
    selected_data = {}
    for col in df.columns:
        for pattern in patterns:
            if re.search(pattern, col, re.IGNORECASE):
                selected_data[col] = df[col].astype('int64', errors='ignore')
                break
    selected_df = pd.DataFrame(selected_data)
    return selected_df


def plot_clustering_results(data, best_model):
    """
    Plot the clustering results using various visualizations.
    
    Parameters:
    - data: DataFrame containing the clustered data
    - best_model: The best clustering model selected
    """
    

    # Elbow plot of the best model
    plot_model(best_model, plot='elbow')

    # Silhouette plot of the best model
    plot_model(best_model, plot='silhouette')

    # Distribution of clusters
    plot_model(best_model, plot='distribution')

def remove_outliers_iqr(df, features):
    """
    Remove outliers using the IQR method for the specified features.
    
    Parameters:
    - df: DataFrame to process.
    - features: List of features to check for outliers.
    
    Returns:
    - Cleaned DataFrame with outliers removed.
    """
    for feature in features:
        Q1 = df[feature].quantile(0.25)
        Q3 = df[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[feature] >= lower_bound) & (df[feature] <= upper_bound)]
    return df
def customer_segmentation(df, sample_size=None):
    # Define regex patterns for each required column
    column_patterns = {
        'InvoiceNo': [r'invoice\s*no', r'invoice\s*number', r'invoice'],
        'StockCode': [r'stock\s*code', r'stock\s*id', r'product\s*code'],
        'Description': [r'description', r'desc'],
        'Quantity': [r'quantity', r'qty'],
        'InvoiceDate': [r'invoice\s*date', r'date'],
        'UnitPrice': [r'unit\s*price', r'price\s*per\s*unit', r'price'],
        'CustomerID': [r'customer\s*id', r'customer'],
        'Country': [r'country', r'nation']
    }

    # Find columns matching the regex patterns
    selected_df = find_columns_with_data(df, column_patterns)
    if selected_df.empty:
        print("No matching columns found in the DataFrame.")
        return None
    
    # Drop duplicates and filter data
    selected_df.dropna(subset=['CustomerID'], inplace=True)
    selected_df = selected_df[(selected_df['Quantity'] > 0) & (selected_df['UnitPrice'] > 0)]
    selected_df['Amount'] = selected_df['Quantity'] * selected_df['UnitPrice']

    # Convert InvoiceDate to datetime if available
    if 'InvoiceDate' in selected_df.columns:
        selected_df['InvoiceDate'] = pd.to_datetime(selected_df['InvoiceDate'])

    # Optionally sample data
    if sample_size and len(selected_df) > sample_size:
        selected_df = selected_df.sample(n=sample_size, random_state=42)
    # Remove outliers before passing to PyCaret setup
    numerical_features = ['Quantity', 'UnitPrice', 'Amount']
    selected_df = remove_outliers_iqr(selected_df, numerical_features)

    # PyCaret setup for clustering with updated configuration
    clu = setup(
        data=selected_df,
        normalize=True,
        pca=True,
        verbose = False,
        remove_multicollinearity=True,
        multicollinearity_threshold = 0.3,
        low_variance_threshold = 0.1,
        session_id=123
    )
    # Dictionary of available clustering models
    clustering_models = {
        'kmeans': 'K-Means Clustering',
        'ap': 'Affinity Propagation',
        'meanshift': 'Mean Shift Clustering',
        'sc': 'Spectral Clustering',
        'hclust': 'Agglomerative Clustering',
        'dbscan': 'Density-Based Spatial Clustering',
        'birch': 'Birch Clustering'
    }

    best_model_name = None
    best_model = None
    best_silhouette = -1  # Initialize with the lowest possible score

    # Iterate over all clustering models and calculate Silhouette scores
    for model_key, model_name in clustering_models.items():
        try:
            # Create model
            model = create_model(model=model_key, num_clusters=5)
            # Pull the metrics DataFrame right after creating the model
            metrics = pull()

            # Extract the Silhouette score
            silhouette_score = metrics['Silhouette'][0] if 'Silhouette' in metrics.columns else None
            print(f"{model_name} Silhouette Score: {silhouette_score}")

            # Check if this is the best model
            if silhouette_score is not None and silhouette_score > best_silhouette:
                best_silhouette = silhouette_score
                best_model = model
                best_model_name = model_name
        except Exception as e:
            print(f"Failed to create {model_name}: {e}")

    # Display the best model
    print(f"\nBest Model: {best_model_name} with Silhouette Score: {best_silhouette}")

    # Assign clusters using the best model
    final_results = assign_model(best_model)

    # Visualize and display the clustered results
    print("Clustered Data Using Best Model:")
    print(final_results.head())

    # Plot results
    plot_clustering_results(final_results, best_model)

    return final_results
