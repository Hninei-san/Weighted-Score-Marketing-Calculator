import pandas as pd

# Normalization function (Min-Max scaling)
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

def calculate_scores(df, total_sales_weights, clv_weights, demand_weights):
    # Check if required columns exist and handle missing ones
    required_columns = [
        'Product Code','product name', 'Add-to-Cart Rate', 'Total Sales',
    'Order Rate (Confirmed)', 'Repeat Purchase Rate',
    'Quantity Sold (Confirmed)', 'Average Time Before Repurchase',
    'Purchase Rate', 'Product Visitors', 'Number of Clicks from Search Results',
    'Buyer (Order confirmed)','Product views'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following required columns are missing: {', '.join(missing_columns)}")

    # Calculate Conversion Rate = Buyer (Order confirmed) / Product views
    df['Conversion Rate'] = df['Buyer (Order confirmed)'] / df['Product views']

    # Normalize the relevant columns
    df['Normalized Total Sales'] = normalize(df['Total Sales'])
    df['Normalized CLV'] = normalize(df['Quantity Sold (Confirmed)'])
    df['Normalized Demand Score'] = normalize(df['Product Visitors'])

    # Calculate the Total Sales Weighted Score
    df['Total Sales Weighted Score'] = (
        df['Conversion Rate'] * (total_sales_weights['Conversion Rate'] / 100) +
        df['Add-to-Cart Rate'] * (total_sales_weights['Add-to-Cart Rate'] / 100) +
        df['Normalized Total Sales'] * (total_sales_weights['Total Sales'] / 100) +
        df['Repeat Purchase Rate'] * (total_sales_weights['Repeat Purchase Rate'] / 100) +
        df['Order Rate (Confirmed)'] * (total_sales_weights['Order Rate (Confirmed)'] / 100)
    )




    # Calculate the CLV Weighted Score
    df['CLV Weighted Score'] = (
        df['Repeat Purchase Rate'] * (clv_weights['Repeat Purchase Rate'] / 100) +
        df['Quantity Sold (Confirmed)'] * (clv_weights['Quantity Sold (Confirmed)'] / 100) +
        df['Average Time Before Repurchase'] * (clv_weights['Average Time Before Repurchase'] / 100) +
        df['Order Rate (Confirmed)'] * (clv_weights['Order Rate (Confirmed)'] / 100) +
        df['Purchase Rate'] * (clv_weights['Purchase Rate'] / 100)
    )

    # Calculate the Demand Score
    df['Demand Score'] = (
        df['Quantity Sold (Confirmed)'] * (demand_weights['Quantity Sold (Confirmed)'] / 100) +
        df['Product Visitors'] * (demand_weights['Product Visitors'] / 100) +
        df['Number of Clicks from Search Results'] * (demand_weights['Number of Clicks from Search Results'] / 100) +
        df['Add-to-Cart Rate'] * (demand_weights['Add-to-Cart Rate'] / 100) +
        df['Order Rate (Confirmed)'] * (demand_weights['Order Rate (Confirmed)'] / 100)
    )

    # Normalize the weighted scores
    df['Normalized Total Sales Weighted Score'] = normalize(df['Total Sales Weighted Score'])
    df['Normalized CLV Weighted Score'] = normalize(df['CLV Weighted Score'])
    df['Normalized Demand Score'] = normalize(df['Demand Score'])

    # Calculate Q2 for each of the normalized scores
    q2_clv = df['Normalized CLV Weighted Score'].mean() + (2 * df['Normalized CLV Weighted Score'].std())
    q2_sales = df['Normalized Total Sales Weighted Score'].mean() + (2 * df['Normalized Total Sales Weighted Score'].std())
    q2_demand = df['Normalized Demand Score'].mean() + (2 * df['Normalized Demand Score'].std())

    # Filter the products where each normalized score is >= Q2
    filtered_df = df[
        (df['Normalized CLV Weighted Score'] >= q2_clv) &
        (df['Normalized Total Sales Weighted Score'] >= q2_sales) &
        (df['Normalized Demand Score'] >= q2_demand)
    ]

    # Return the final filtered DataFrame with products that meet the criteria
    return filtered_df[['Product Code','product name', 
                        'Normalized Total Sales Weighted Score', 'Normalized CLV Weighted Score', 'Normalized Demand Score']]