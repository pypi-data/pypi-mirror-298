# Customer Segmentation, CLTV, and MBA Analysis

This package performs **Customer Segmentation**, **Market Basket Analysis (MBA)**, and **Customer Lifetime Value (CLTV)** calculation with features for predicting **Customer Attrition** and generating **Next Best Product Recommendations**.

## Features

- **Customer Segmentation**: Clusters customers based on purchasing behavior using clustering models.
- **Market Basket Analysis (MBA)**: Performs market basket analysis to understand product association patterns.
- **CLTV Calculation**: Estimates customer lifetime value using BG/NBD and Gamma-Gamma models.
- **Customer Attrition Prediction**: Identifies customers at risk of leaving the company.
- **Next Best Product Recommendation**: Recommends products based on customer purchase behavior.

## Installation

1. Clone the repository:

   ```bash
   pip install Customer_dna
   ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Usage:
This package provides a main() function that runs customer segmentation, market basket analysis, CLTV calculation, attrition prediction, and product recommendation.
```bash
import pandas as pd
from customer_dna.main import main

# Load your dataset
df = pd.read_csv("your_dataset.csv")

# Call the main function
recommendations = main(df, sample_size=10000, top_n=5)

# Output the recommendations
print(recommendations)
```
## Data Requirements

Your input data should have the following columns (or their synonyms as detected by the package):

*   `InvoiceNo`: Invoice number of the transaction.
*   `InvoiceDate`: Date of the transaction.
*   `Description`: Product description.
*   `Quantity`: Quantity purchased.
*   `UnitPrice`: Price of the product.
*   `CustomerID`: Unique customer identifier.
*   `Country`: Country of the customer.

## Key Functions

1. **Customer Segmentation** (`customer_segmentation()`): Segments customers based on purchasing behavior using PyCaret’s clustering models.

2. **Market Basket Analysis (MBA)** (`mba()`): Analyzes product associations in different customer segments using `mlxtend`.

3. **CLTV Calculation** (`process_and_visualize_clv()`): Computes customer lifetime value using the BG/NBD and Gamma-Gamma models.

4. **Customer Attrition Prediction** (`predict_customer_attrition()`): Predicts customers likely to churn based on the CLTV output.

5. **Product Recommendation** (`next_best_product_recommendation()`): Recommends the next best products for each customer based on previous purchasing patterns.

### Required Modules

```bash
pandas==1.3.3
numpy==1.21.2
matplotlib==3.4.3
seaborn==0.11.2
scikit-learn==0.24.2
scipy==1.7.1
pycaret==2.3.3
lifetimes==0.11.3
mlxtend==0.19.0
plotly==5.3.1
networkx==2.6.3
```


