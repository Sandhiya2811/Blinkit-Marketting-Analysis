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
        "Marketing Team Analysis",
        "Sales Team Analysis",
        "Delivery / Operations Analysis",
        "Customer Feedback Analysis",
        "Why Sales Are Down"
    ]
)

show_raw = st.sidebar.checkbox("Show Raw Data Table", value=True)
show_overall_business_analysis =  st.sidebar.checkbox("show Overall Business Analysis Shortly", value=True)

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
    # Separate start and end date pickers
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
# KPI METRICS (SQL-based)
# -------------------------------------------------
st.markdown("### 🔢 Key Metrics")

query_kpis = f"""
SELECT
    SUM(revenue_generated) AS total_revenue,
    SUM(spend) AS total_spend,
    AVG(roas) AS avg_roas,
    AVG(delay_minutes) AS avg_delay
FROM blinkit_data
WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}';
"""

kpi_df = pd.read_sql(query_kpis, engine)

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Revenue", f"₹{kpi_df['total_revenue'].iloc[0]:,.0f}")
c2.metric("📢 Ad Spend", f"₹{kpi_df['total_spend'].iloc[0]:,.0f}")
c3.metric("📈 Avg ROAS", round(kpi_df['avg_roas'].iloc[0], 2))
c4.metric("⏱ Avg Delay", f"{round(kpi_df['avg_delay'].iloc[0], 1)} mins")

st.divider()


# =================================================
# ANALYSIS SECTIONS
# =================================================

# ---------------- TIME BASED PERFORMANCE ----------------  
if analysis_type == "Time-based Performance":
    st.subheader("📊 Time-based Performance (Revenue vs Ad Spend)")

    query_daily = f"""
    SELECT
        order_day_only,
        SUM(revenue_generated) AS revenue,
        SUM(spend) AS spend
    FROM blinkit_data
    WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY order_day_only
    ORDER BY order_day_only;
    """

    daily_perf = pd.read_sql(query_daily, engine)


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


# =================================================
# MARKETING TEAM ANALYSIS
# =================================================
elif analysis_type == "Marketing Team Analysis":

    option = st.sidebar.selectbox(
        "Marketing Analysis Type",
        [
            "Revenue & Orders",
            "Revenue vs Spend",
            "Channel Performance",
            "Target Audience Effectiveness"
        ]
    )

    if option == "Revenue & Orders":

        query = f"""
        SELECT COUNT(DISTINCT order_id) AS total_orders,
               SUM(order_total) AS total_revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}';
        """

        df1 = pd.read_sql(query, engine)
        st.dataframe(df1, use_container_width=True)
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
        - Blinkit received a total of 4991 orders, generating a total revenue of ₹ 98,939,180/-
        """)

    elif option == "Revenue vs Spend":

        query = f"""
        SELECT campaign_name, channel,
               SUM(spend) AS total_spend,
               SUM(order_total) AS total_revenue,
               ROUND(SUM(order_total)/NULLIF(SUM(spend),0),2) AS roi
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY campaign_name, channel
        ORDER BY roi DESC;
        """

        df2 = pd.read_sql(query, engine)
        fig = px.bar(df2, x="campaign_name", y=["total_revenue","total_spend"], barmode="group")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df2, use_container_width=True)
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
        - cus budget on high ROI campaigns.
        - Stop low-performing ads.
        """)

    elif option == "Channel Performance":

        query = f"""
        SELECT channel,
               COUNT(order_id) AS orders,
               SUM(order_total) AS revenue,
               SUM(spend) AS spend
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY channel;
        """

        df3 = pd.read_sql(query, engine)
        fig = px.bar(df3, x="channel", y="revenue")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df3, use_container_width=True)
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
        - The APP channel recorded 4646 total orders, generating ₹25561210.77 in revenue with a total spend of ₹35216669.86. 
        - This indicates the overall performance of the channel in driving sales through marketing campaigns.
        """)

    else:

        query = f"""
        SELECT target_audience,
               COUNT(order_id) AS orders,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY target_audience;
        """

        df4 = pd.read_sql(query, engine)
        fig = px.bar(df4, x="target_audience", y="revenue")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df4, use_container_width=True)
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
        - Focus ads on best audiences.
        - Give special offers and discounts for each audience group.
        - Keep enough stock for popular audiences.
        - Try new ads and offers for low-performing audiences.
        """)



# =================================================
# SALES TEAM ANALYSIS
# =================================================
elif analysis_type == "Sales Team Analysis":

    option = st.sidebar.selectbox(
        "Sales Analysis Type",
        [
            "Orders & Revenue by Day",
            "Monthly Revenue",
            "Brand-wise Sales",
            "Category-wise Sales",
            "High Value Customers",
            "Product Margin Analysis"
        ]
    )

    queries = {
        "Orders & Revenue by Day": f"""
        SELECT order_day_name,
               COUNT(DISTINCT order_id) AS orders,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY order_day_name;
        """,

        "Monthly Revenue": f"""
        SELECT order_month_name,
               COUNT(DISTINCT order_id) AS orders,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY order_month_name;
        """,

        "Brand-wise Sales": f"""
        SELECT brand,
               COUNT(DISTINCT order_id) AS orders,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY brand;
        """,

        "Category-wise Sales": f"""
        SELECT category,
               SUM(item_total) AS revenue,
               SUM(quantity) AS total_quantity
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY category;
        """,

        "High Value Customers": f"""
        SELECT customer_segment,
               COUNT(DISTINCT customer_id) AS customers,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY customer_segment;
        """,

        "Product Margin Analysis": f"""
        SELECT product_name,
               SUM(item_total) AS sales,
               AVG(margin_percentage) AS avg_margin
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY product_name;
        """
    }

    df_sales = pd.read_sql(queries[option], engine)

    fig = px.bar(
        df_sales,
        x=df_sales.columns[0],
        y=df_sales.columns[-1],
        title=option
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_sales, use_container_width=True)

    if option == "Orders & Revenue by Day":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                   - Run discounts on low-revenue days.
                   - Stock and deliver enough on high-demand days.
                   - Look at weekly trends to predict orders and plan marketing.
                   """)

    elif option == "Monthly Revenue":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                - Run festival or seasonal promotions in low-sales months.
                - During May holidays, parents will be free, so giving good offers on fast food will make sales easier.
                - In July, August, and September, it’s the rainy season, so orders will be higher.
                   """)

    elif option == "Brand-wise Sales":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("- Focus marketing spend on top performing brands.")

    elif option == "Category-wise Sales":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                   - Stock more of popular categories.
                - Give offers for each category when demand is high.
                - Pair slow categories with top products.
                - Use trends to show products better on shelves and app.
                """)

    elif option == "High Value Customers":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                   - Reward your best customers.
                    - Give personalized offers.
                    - Bundle products to get more from small customers.
                    - Stock and deliver fast for premium customers.
                   """)

    elif option == "Product Margin Analysis":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                    - Highlight profitable products.
                    - Pair low-profit items with top sellers.
                    - Talk to suppliers to lower costs for cheap items.
                    - Give discounts without losing money.
                    """)


# =================================================
# DELIVERY / OPERATIONS
# =================================================
elif analysis_type == "Delivery / Operations Analysis":

    option = st.sidebar.selectbox(
        "Delivery Analysis Type",
        ["Delivery Partner Load", "Peak Order Hours", "Area-wise Demand"]
    )

    queries = {
        "Delivery Partner Load": f"""
        SELECT delivery_partner_id,
               COUNT(order_id) AS total_orders,
               SUM(order_total) AS revenue_handled
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY delivery_partner_id;
        """,

        "Peak Order Hours": f"""
        SELECT order_hour,
               COUNT(order_id) AS total_orders,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY order_hour;
        """,

        "Area-wise Demand": f"""
        SELECT area,
               COUNT(order_id) AS total_orders,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY area;
        """
    }

    df_ops = pd.read_sql(queries[option], engine)

    fig = px.bar(
        df_ops,
        x=df_ops.columns[0],
        y="total_orders",
        title=option
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_ops, use_container_width=True)

    if option == "Delivery Partner Load":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                - Distribute orders to reduce delays.
                - Reward good delivery partners.
                - Use free partners when it’s busy.
                - Adjust partners based on demand.
                   """)

    elif option == "Peak Order Hours" :
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
            - Increase delivery staff when orders are high.
            - Stock popular products before peak hours.
            - Use timed offers to reduce peak orders.
            - Check busy-hour data to forecast delays.
             """)

    elif option == "Area-wise Demand":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                - Stock and deliver more in high-demand areas.
                - Give discounts in low-demand areas.
                - Check area trends to prevent delays.
                - Expand marketing to nearby areas with potential orders.
                """)



# =================================================
# CUSTOMER FEEDBACK
# =================================================
elif analysis_type == "Customer Feedback Analysis":

    option = st.sidebar.selectbox(
        "Feedback Analysis Type",
        ["Rating vs Sales", "Sentiment Impact"]
    )

    queries = {
        "Rating vs Sales": f"""
        SELECT rating,
               COUNT(order_id) AS orders,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY rating;
        """,

        "Sentiment Impact": f"""
        SELECT sentiment,
               COUNT(order_id) AS orders,
               AVG(order_total) AS avg_order_value
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY sentiment;
        """
    }

    df_fb = pd.read_sql(queries[option], engine)

    fig = px.bar(
        df_fb,
        x=df_fb.columns[0],
        y=df_fb.columns[-1],
        title=option
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_fb, use_container_width=True)

    if option == "Rating vs Sales":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                - Give good service to get good ratings.
                - Fix complaints fast.
                - Use feedback to make things better.
                - Ask happy customers to buy again and refer friends.
                   """)

    elif option == "Sentiment Impact" :
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
            - Listen to unhappy customers and solve issues.
            - Reward happy customers to keep them loyal.
            - Make delivery and products better using feedback.
            - Show positive feedback in ads to build trust.
             """)

# =================================================
# WHY SALES ARE DOWN
# =================================================
else:

    option = st.sidebar.selectbox(
        "Sales Drop Analysis",
        ["Daily Revenue Trend", "Spend vs Revenue", "Negative Feedback Spike"]
    )

    queries = {
        "Daily Revenue Trend": f"""
        SELECT promised_date,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY promised_date
        ORDER BY promised_date;
        """,

        "Spend vs Revenue": f"""
        SELECT promised_date,
               SUM(spend) AS spend,
               SUM(order_total) AS revenue
        FROM blinkit_data
        WHERE order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY promised_date;
        """,

        "Negative Feedback Spike": f"""
        SELECT promised_date,
               COUNT(*) AS negative_feedbacks
        FROM blinkit_data
        WHERE sentiment = 'negative'
          AND order_day_only BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY promised_date;
        """
    }

    df_drop = pd.read_sql(queries[option], engine)

    fig = px.line(
        df_drop,
        x=df_drop.columns[0],
        y=df_drop.columns[-1],
        markers=True,
        title=option
    )

    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df_drop, use_container_width=True)

    if option =="Daily Revenue Trend":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                - Give discounts on low-sales days.
                - Stock and deliver well on busy days.
                - Find out why sales fell.
                - Use trends to plan demand and marketing.
                   """)

    elif option =="Spend vs Revenue" :
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                - Focus money on campaigns that work well.
                - Cut spending on campaigns that don’t work.
                - Watch results daily and change campaigns fast.
                - Spend more during busy days or hours to earn more.
             """)

    elif option == "Negative Feedback Spike":
        st.markdown("### 🧠 Visual Business Insight")
        st.warning("""
                - Check why complaints are high.
                - Make delivery, packaging, and products better.
                - Reach out to unhappy customers with solutions.
                - Train delivery staff using feedback to give better service.
                """)

# -------------------------------------------------
# RAW DATA
# -------------------------------------------------
if show_raw:
    with st.expander("📂 View Raw Data"):
        query_raw_data = f"""
        SELECT
            order_day_only,
            customer_name,
            area,
            pincode,
            customer_segment,
            campaign_name,
            channel,
            order_total,
            total_orders,
            revenue_generated,
            spend,
            roas,
            delivery_status,
            delay_minutes,
            rating,
            sentiment
        FROM blinkit_data
        ORDER BY order_day_only DESC;
        """

        raw_data = pd.read_sql(query_raw_data, engine)

        st.dataframe(raw_data, use_container_width=True, height=600)
        
        
if show_overall_business_analysis:
        st.subheader("🧩 Overall Recommendations & Insights")

        option = st.sidebar.selectbox(
        "Select Insight Category",
        [
            "Products",
            "Offers & Discounts",
            "Delivery Staff / Operations",
            "Stock & Inventory",
            "Marketing & Campaigns",
            "Customer Engagement / Loyalty",
            "Customer Satisfaction",
            "Peak Hour / Time Management",
            "Area / Regional Focus",
            "Technology / Platform Improvements"
        ]
    )

        insights = {
        "Products": [
            "Prioritize high-selling and high-margin products.",
            "Bundle slow-moving products with popular ones to increase sales."
        ],
        "Offers & Discounts": [
            "Give festival or seasonal discounts to attract customers.",
            "Run targeted promotions on low-sales days to boost revenue."
        ],
        "Delivery Staff / Operations": [
            "Increase delivery staff during peak hours or high-demand days.",
            "Reward best-performing delivery partners with bonuses."
        ],
        "Stock & Inventory": [
            "Ensure sufficient stock for high-demand areas and products.",
            "Use inventory trends to avoid stockouts and lost sales."
        ],
        "Marketing & Campaigns": [
            "Focus budget on high-ROI campaigns.",
            "Reduce spend on low-performing campaigns to save cost."
        ],
        "Customer Engagement / Loyalty": [
            "Target loyal customers with personalized offers.",
            "Encourage repeat purchases through reward programs (like free delivery)."
        ],
        "Customer Satisfaction": [
            "Quickly address complaints and negative feedback.",
            "Monitor ratings and sentiment to improve service quality."
        ],
        "Peak Hour / Time Management": [
            "Prepare extra delivery capacity during peak order hours.",
            "Use offers to shift demand to off-peak hours."
        ],
        "Area / Regional Focus": [
            "Allocate stock and delivery staff to high-demand areas.",
            "Run marketing campaigns in low-demand areas to increase sales."
        ],
        "Technology / Platform Improvements": [
            "Use dashboards to track performance across campaigns, products, and areas.",
            "Implement predictive models for demand, sales drop, and delivery delays."
        ]
    }

        st.markdown(f"### 🔹 {option}")
        for item in insights[option]:
            st.write(f"- {item}")

