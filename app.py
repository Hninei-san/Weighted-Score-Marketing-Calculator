import streamlit as st
import pandas as pd
from calculations import calculate_scores  # Import the calculation function

# File upload
required_columns = [
    'Product Code', 'product name', 'Add-to-Cart Rate', 'Total Sales',
    'Order Rate (Confirmed)', 'Repeat Purchase Rate',
    'Quantity Sold (Confirmed)', 'Average Time Before Repurchase',
    'Purchase Rate', 'Product Visitors', 'Number of Clicks from Search Results',
    'Buyer (Order confirmed)', 'Product views'
]

st.subheader('Weighted Score Marketing Calculator')
# Display required file description
st.markdown("**Required Columns for the Excel File**")
st.write("The uploaded Excel file must contain the following columns:")
st.markdown(f"<p style='color:blue;'>{', '.join(required_columns)}</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])



# Add a header for Total Sales Weights
st.sidebar.header('Total Sales Weights')

# Initialize session state for weights if they don't exist
if 'total_sales_weights' not in st.session_state:
    st.session_state.total_sales_weights = {
        'Conversion Rate': 25,
        'Add-to-Cart Rate': 20,
        'Total Sales': 35,
        'Repeat Purchase Rate': 15,
        'Order Rate (Confirmed)': 5
    }

# Function to increment or decrement the weight values
def adjust_weight(weight_name, delta):
    # Ensure the weight_name exists in session_state before adjusting
    if weight_name in st.session_state.total_sales_weights:
        st.session_state.total_sales_weights[weight_name] += delta
    else:
        st.error(f"Weight name '{weight_name}' not found in total_sales_weights.")

# Display and adjust Total Sales Weights using number input
for weight_name, current_value in st.session_state.total_sales_weights.items():
    st.session_state.total_sales_weights[weight_name] = st.sidebar.number_input(
        f"{weight_name} Weight", min_value=0, max_value=100, value=current_value, step=1
    )

# Add a header for CLV Weights
st.sidebar.header('CLV Weights')

# Initialize session state for CLV weights if they don't exist
if 'clv_weights' not in st.session_state:
    st.session_state.clv_weights = {
        'Repeat Purchase Rate': 40,
        'Quantity Sold (Confirmed)': 20,
        'Average Time Before Repurchase': 20,
        'Order Rate (Confirmed)': 10,
        'Purchase Rate': 10
    }

# Display and adjust CLV Weights using number input
for weight_name, current_value in st.session_state.clv_weights.items():
    st.session_state.clv_weights[weight_name] = st.sidebar.number_input(
        f"{weight_name} Weight", min_value=0, max_value=100, value=current_value, step=1
    )

# Add a header for Demand Score Weights
st.sidebar.header('Demand Score Weights')

# Initialize session state for Demand Score weights if they don't exist
if 'demand_weights' not in st.session_state:
    st.session_state.demand_weights = {
        'Quantity Sold (Confirmed)': 40,
        'Product Visitors': 20,
        'Number of Clicks from Search Results': 10,
        'Add-to-Cart Rate': 15,
        'Order Rate (Confirmed)': 15
    }

# Display and adjust Demand Score Weights using number input
for weight_name, current_value in st.session_state.demand_weights.items():
    st.session_state.demand_weights[weight_name] = st.sidebar.number_input(
        f"{weight_name} Weight", min_value=0, max_value=100, value=current_value, step=1
    )

# Detailed weight validation function
def validate_weights(weights_dict, category_name):
    total_weight = sum(weights_dict.values())
    if total_weight != 100:
        st.error(f"Total weight  must be 100%. The current sum of {category_name}  is {total_weight}%.  Please adjust the weights.")
        return False
    return True

if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Check for necessary columns
    required_columns = [
        'Product Code', 'product name', 'Add-to-Cart Rate', 'Total Sales',
        'Order Rate (Confirmed)', 'Repeat Purchase Rate',
        'Quantity Sold (Confirmed)', 'Average Time Before Repurchase',
        'Purchase Rate', 'Product Visitors', 'Number of Clicks from Search Results',
        'Buyer (Order confirmed)', 'Product views'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if len(missing_columns) > 0:
        st.error(f"The following required columns are missing: {', '.join(missing_columns)}")
    else:
        # Validate that the weights sum to 100% for each category
        if validate_weights(st.session_state.total_sales_weights, "Total Sales Weights") and \
           validate_weights(st.session_state.clv_weights, "CLV Weights") and \
           validate_weights(st.session_state.demand_weights, "Demand Score Weights"):
            # Call the calculate_scores function from the calculations file
            df_results = calculate_scores(df, st.session_state.total_sales_weights, st.session_state.clv_weights, st.session_state.demand_weights)

            # Display the resulting dataframe with weighted scores
            st.write(df_results)
