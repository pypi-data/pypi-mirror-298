import pandas as pd
from .customer_segmentation import customer_segmentation  
from .mba import mba  
from .cltv import process_and_visualize_clv  
from .customer_attrition import predict_customer_attrition, next_best_product_recommendation 

def main(df, sample_size=None, top_n=5):
    """
    Main function to handle customer segmentation, MBA, CLTV, attrition prediction, and product recommendation.
    
    Parameters:
    - df: DataFrame input provided by the user
    - sample_size: Optional sample size for customer segmentation
    - top_n: Number of top product recommendations to generate per customer
    
    Returns:
    - The final recommendations DataFrame after processing CLTV and product recommendation.
    """

    # Step 1: Perform customer segmentation
    print("Starting customer segmentation...")
    segmented_df = customer_segmentation(df, sample_size=sample_size)
    
    if segmented_df is None:
        print("Segmentation failed or no valid data found for clustering.")
        return None
    print('------------------------------------------------------------------------------------------')
    print("Customer segmentation completed. Proceeding to market basket analysis (MBA)...")
    print('------------------------------------------------------------------------------------------')

    # Step 2: Run Market Basket Analysis (MBA) on the segmented data
    mba(segmented_df, sample_size=sample_size)
    
    print('------------------------------------------------------------------------------------------')
    print("Market basket analysis (MBA) completed. Proceeding to CLTV calculation...")
    print('------------------------------------------------------------------------------------------')

    # Step 3: Calculate CLTV using the segmented data
    cltv_final = process_and_visualize_clv(segmented_df)
    
    if cltv_final.empty:
        print("CLTV processing failed or no valid data for CLTV calculation.")
        return None
    print('------------------------------------------------------------------------------------------')
    print("Customer Lifetime Value Prediction(CLTV) completed. Proceeding to Customer Attrition...")
    print('------------------------------------------------------------------------------------------')

    # Step 4: Predict customer attrition if CLTV is not empty
    attrition_df = predict_customer_attrition(cltv_final)
    if not attrition_df.empty:
        print("Customer Attrition Predictions:")
        print(attrition_df)
        print('--------------------------------------------------------------------')

    # Step 5: Generate next best product recommendations
    recommendations_df = next_best_product_recommendation(df, cltv_final, top_n=top_n)
    print("Next Best Product Recommendations:")
    print(recommendations_df)

    # Return the final recommendations DataFrame
    return recommendations_df