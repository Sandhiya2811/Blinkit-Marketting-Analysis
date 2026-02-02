import streamlit as st
import pandas as pd
import pickle
import numpy as np

# -------------------------------
# Load trained pipeline
# -------------------------------
with open("blinkit_best__model.pkl", "rb") as f:
    rf_pipeline = pickle.load(f)

# -------------------------------
# Load blinkit data for dropdowns
# -------------------------------
ml_data = pd.read_csv("blinkit_data.csv")

st.title("🚨 Blinkit Delivery Risk Calculator")
st.subheader("Manager Input")

# -------------------------------
# Minimal Manager Inputs
# -------------------------------
area = st.selectbox("Select Area:", ml_data['area'].unique())
pincode = st.selectbox("Select Pincode:", ml_data[ml_data['area']==area]['pincode'].unique())
order_hour = st.selectbox("Select Delivery Hour (0-23):", list(range(24)), index=18)
order_day_name = st.selectbox("Select Day of Week:", ml_data['order_day_name'].unique())
order_month_name = st.selectbox("Select Month:", ml_data['order_month_name'].unique())

# -------------------------------
# Fill other columns internally with defaults (safe)
# -------------------------------
def fill_defaults(area, pincode, order_hour, order_day_name, order_month_name):
    # Most frequent / median values from training data
    defaults = {
        'category': ml_data['category'].mode()[0],
        'brand': ml_data['brand'].mode()[0],
        'channel': ml_data['channel'].mode()[0],
        'target_audience': ml_data['target_audience'].mode()[0],
        'payment_method': ml_data['payment_method'].mode()[0],
        'customer_segment': ml_data['customer_segment'].mode()[0],
        'sentiment': ml_data['sentiment'].mode()[0],
        'delivery_status': ml_data['delivery_status'].mode()[0],
        'quantity': int(ml_data['quantity'].median()),
        'rating': ml_data['rating'].median(),
        'total_orders': int(ml_data['total_orders'].median()),
        'order_minutes': int(ml_data['order_minutes'].median()),
        'order_total': ml_data['order_total'].median(),
        'avg_order_value': ml_data['avg_order_value'].median(),
        'price': ml_data['price'].median(),
        'item_total': ml_data['item_total'].median(),
        'spend': ml_data['spend'].median()
    }

    input_data = pd.DataFrame({
        'order_hour':[order_hour],
        'order_day_name':[order_day_name],
        'order_month_name':[order_month_name],
        'area':[area],
        'pincode':[pincode],
        'delivery_status':[defaults['delivery_status']],
        'order_total':[defaults['order_total']],
        'total_orders':[defaults['total_orders']],
        'avg_order_value':[defaults['avg_order_value']],
        'category':[defaults['category']],
        'brand':[defaults['brand']],
        'quantity':[defaults['quantity']],
        'price':[defaults['price']],
        'item_total':[defaults['item_total']],
        'channel':[defaults['channel']],
        'target_audience':[defaults['target_audience']],
        'spend':[defaults['spend']],
        'payment_method':[defaults['payment_method']],
        'customer_segment':[defaults['customer_segment']],
        'rating':[defaults['rating']],
        'sentiment':[defaults['sentiment']],
        'order_minutes':[defaults['order_minutes']]
    })
    return input_data

# -------------------------------
# Predict Delay
# -------------------------------
if st.button("Predict Delay"):
    # Prepare input
    input_data = fill_defaults(area, pincode, order_hour, order_day_name, order_month_name)
    
    # Predict
    predicted_minutes = rf_pipeline.predict(input_data)[0]

    # -------------------------------
    # Display text logic
    # -------------------------------
    if predicted_minutes < 0:
        display_text = f"Before {abs(round(predicted_minutes, 1))} minutes"
        display_minutes = 0   # early delivery = no delay
    else:
        display_text = f"{round(predicted_minutes, 1)} minutes"
        display_minutes = predicted_minutes

    # -------------------------------
    # Risk calculation (only delay matters)
    # -------------------------------
    if display_minutes > 30:
        risk_level = "High Risk"
    elif display_minutes > 15:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    risk_percentage = min(round((display_minutes / 60) * 100, 2), 100)

    # -------------------------------
    # Show Results
    # -------------------------------
    st.warning(f"{risk_level} of Delay ({risk_percentage}%)")
    st.subheader("Predicted Delivery Time:")
    st.write(display_text)

    st.subheader("Immediate Actions:")
    if risk_level == "High Risk":
        actions = ["Allocate extra riders", "Notify customers", "Prepare contingency plan"]
    elif risk_level == "Medium Risk":
        actions = ["Monitor orders closely", "Keep extra riders ready"]
    else:
        actions = ["Normal operations"]

    for a in actions:
        st.write("-", a)
