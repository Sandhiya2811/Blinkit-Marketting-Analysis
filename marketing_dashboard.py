import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import timedelta
from sqlalchemy import create_engine

# -------------------------------------------------
# DATABASE ENGINE
# -------------------------------------------------
engine = create_engine(
    "mysql+mysqlconnector://root:Subash%4028@localhost:3306/blinkit"
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Business Analytics Dashboard", layout="wide")

st.title("📊 Business Analytics Dashboard")
st.caption("Marketing • Sales • Delivery • Customer Feedback – Unified Dashboard")

# -------------------------------------------------
# LOAD DATA (WITH SQLALCHEMY)
# -------------------------------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM blinkit_data;"
    df = pd.read_sql(query, engine)

    # Convert date columns to datetime
    df["order_day_only"] = pd.to_datetime(df["order_day_only"])
    df["promised_date"] = pd.to_datetime(df["promised_date"])
    
    return df

df = load_data()

# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
st.sidebar.header("🔍 Controls")

analysis_type = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Time-based Performance",
        "Marketing Analysis",
        "Sales Analysis",
        "Delivery / Operations Analysis",
        "Customer Feedback Analysis"
    ]
)

show_raw = st.sidebar.checkbox("Show Raw Data Table", value=True)

date_option = st.sidebar.radio(
    "Date Filter",
    ["Last 7 Days", "Last 30 Days", "Custom"]
)

max_date = df["order_day_only"].max()
min_date = df["order_day_only"].min()

if date_option == "Last 7 Days":
    start_date = max_date - timedelta(days=7)
    end_date = max_date
elif date_option == "Last 30 Days":
    start_date = max_date - timedelta(days=30)
    end_date = max_date
else:
    
    start_date = st.sidebar.date_input(
        "Select Start Date",
        value=min_date
    )
    end_date = st.sidebar.date_input(
        "Select End Date",
        value=max_date
    )


# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------
filtered_df = df[
    (df["order_day_only"] >= pd.to_datetime(start_date)) &
    (df["order_day_only"] <= pd.to_datetime(end_date))
]

# -------------------------------------------------
# KPI METRICS
# -------------------------------------------------
st.markdown("### 🔢 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

total_revenue = filtered_df["revenue_generated"].sum()
total_spend = filtered_df["spend"].sum()
avg_roas = round(filtered_df["roas"].mean(), 2)
avg_delay = round(filtered_df["delay_minutes"].mean(), 1)

c1.metric("💰 Revenue", f"₹{total_revenue:,.0f}")
c2.metric("📢 Ad Spend", f"₹{total_spend:,.0f}")
c3.metric("📈 Avg ROAS", avg_roas)
c4.metric("⏱ Avg Delay", f"{avg_delay} mins")

st.divider()

# =================================================
# ANALYSIS SECTIONS
# =================================================

# ---------------- TIME BASED PERFORMANCE ----------------  
if analysis_type == "Time-based Performance":
    st.subheader("📊 Time-based Performance (Revenue vs Ad Spend)")

    daily_perf = filtered_df.groupby("order_day_only").agg(
        revenue=("revenue_generated", "sum"),
        spend=("spend", "sum")
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_perf["order_day_only"],
        y=daily_perf["revenue"],
        mode="lines+markers",
        name="Revenue",
        line=dict(color="green", width=3)
    ))
    fig.add_trace(go.Bar(
        x=daily_perf["order_day_only"],
        y=daily_perf["spend"],
        name="Ad Spend",
        marker_color="red",
        opacity=0.6,
        yaxis="y2"
    ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Revenue"),
        yaxis2=dict(title="Ad Spend", overlaying="y", side="right"),
        height=520
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📍 Daily Revenue & Ad Spend Table")
    st.dataframe(daily_perf, use_container_width=True)

    st.markdown("### 🧠 Visual Business Insight")
    st.warning("""
    🔴 Ad Spend is high on some days  
    🟢 But Revenue is not increasing at the same level  

    👉 What this shows clearly:
    Even after spending more on ads, sales are not growing consistently.

    📌 Business meaning:
    - Some ad spends are not giving returns
    - Marketing budget is being wasted on certain days
    - We should spend more only on days where revenue increases
    """)


# ---------------- MARKETING ----------------
elif analysis_type == "Marketing Analysis":
    st.subheader("📢 Marketing Performance")

    campaign_perf = filtered_df.groupby(
        ["campaign_name", "channel"]
    ).agg(
        total_spend=("spend", "sum"),
        total_revenue=("order_total", "sum")
    ).reset_index()

    campaign_perf["roi"] = (
        campaign_perf["total_revenue"] / campaign_perf["total_spend"].replace(0, None)
    ).round(2)

    fig = px.bar(
        campaign_perf,
        x="campaign_name",
        y="roi",
        color="channel",
        title="ROI by Campaign & Channel"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📋 Campaign Performance Table")
    st.dataframe(campaign_perf, use_container_width=True)
    
    st.markdown("### 🧠 Business Insight")
    st.warning("""
    - We should increase spending only on days where revenue increases
    - Spend more on campaigns and days that give high profit
    - Spend less on days with low revenue
    - Stop campaigns with very poor ROI
    """)

# ---------------- SALES ----------------
elif analysis_type == "Sales Analysis":
    st.subheader("🛒 Sales Analysis")

    day_sales = filtered_df.groupby("order_day_name").agg(
        total_orders=("order_id", "count"),
        total_revenue=("order_total", "sum")
    ).reset_index()

    fig = px.bar(
        day_sales,
        x="order_day_name",
        y="total_orders",
        title="Orders by Day"
    )
    fig.add_scatter(
        x=day_sales["order_day_name"],
        y=day_sales["total_revenue"],
        mode="lines+markers",
        name="Revenue"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📋 Day-wise Sales Table")
    st.dataframe(day_sales, use_container_width=True)

    brand_sales = filtered_df.groupby("brand").agg(
        revenue=("order_total", "sum")
    ).reset_index().sort_values("revenue", ascending=False)

    st.markdown("#### 🏷 High Revenue Brands")
    st.dataframe(brand_sales, use_container_width=True)

    st.markdown("### 🧠 Business Insight")
    st.warning("""
    - Run discounts on low-revenue days.
    - Stock and deliver enough on high-demand days.
    - Look at weekly trends to predict orders and plan marketing.
    """)

# ---------------- DELIVERY ----------------
elif analysis_type == "Delivery / Operations Analysis":
    st.subheader("🚚 Delivery & Operations")

    hourly_load = filtered_df.groupby("order_hour").agg(
        orders=("order_id", "count"),
        revenue=("order_total", "sum")
    ).reset_index()

    fig = px.line(
        hourly_load,
        x="order_hour",
        y="orders",
        markers=True,
        title="Orders by Hour (Peak Load)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📋 Hourly Load Table")
    st.dataframe(hourly_load, use_container_width=True)

    area_demand = filtered_df.groupby("area").agg(
        orders=("order_id", "count"),
        revenue=("order_total", "sum")
    ).reset_index().sort_values("orders", ascending=False)

    st.markdown("#### 📍 Area-wise Demand")
    st.dataframe(area_demand, use_container_width=True)

    st.markdown("### 🧠 Business Insight")
    st.warning("""
    - Increase delivery staff when orders are high
    - Stock popular products before peak hours.
    - Use timed offers to reduce peak orders.
    - Check busy-hour data to forecast delays.
    """)


# ---------------- FEEDBACK ----------------
else:
    st.subheader("💬 Customer Feedback Analysis")

    rating_sales = filtered_df.groupby("rating").agg(
        orders=("order_id", "count"),
        revenue=("order_total", "sum")
    ).reset_index()

    fig = px.bar(
        rating_sales,
        x="rating",
        y="orders",
        title="Orders by Rating"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 📋 Rating vs Sales")
    st.dataframe(rating_sales, use_container_width=True)

    # ---------------- Negative Feedback Trend (Pandas, date-option dependent) ----------------
    negative_feedback_spike = (
        filtered_df[filtered_df["sentiment"].str.lower() == "negative"]  # case-insensitive
        .groupby("promised_date")
        .agg(negative_feedbacks=("order_id", "count"))  # feedback_id illa na order_id use panna
        .reset_index()
        .sort_values("promised_date", ascending=False)
    )

    # Plot bar/line chart exactly like rating_sales example
    fig = px.line(
        negative_feedback_spike,
        x="promised_date",
        y="negative_feedbacks",
        title="📉 Negative Feedbacks Over Time",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧠 Business Insight")
    st.warning("""
    - Give good service to get good ratings.
    - Fix complaints fast.
    - Use feedback to make things better.
    - Ask happy customers to buy again and refer friends.
    """)

# -------------------------------------------------
# RAW DATA
# -------------------------------------------------
if show_raw:
    with st.expander("📂 View Raw Data"):
        raw_columns = [
            "order_day_only", "customer_name", "area", "pincode",
            "customer_segment", "campaign_name", "channel",
            "order_total", "total_orders", "revenue_generated",
            "spend", "roas", "delivery_status", "delay_minutes",
            "rating", "sentiment"
        ]
        filtered_df_display = filtered_df[raw_columns]
        st.dataframe(filtered_df_display, use_container_width=True, height=600)

