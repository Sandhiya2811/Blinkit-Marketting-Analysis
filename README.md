# 🛒 Blinkit Business Analysis Platform

## 📌 Project Overview
This project focuses on building a **Business Decision Platform** for Blinkit by integrating **6 different datasets**, merging them into a **single SQL table**, and performing **end-to-end business analysis**.

The analysis helps multiple teams such as **Marketing, Sales, Operations, and Customer Experience** to make **data-driven decisions** using real-world Blinkit data.

---

## 🎯 Project Motive
The main goals of this project are:

- To combine multiple Blinkit datasets into **one unified data source**
- To perform **business-oriented analytics** instead of just technical analysis
- To identify **revenue drivers, sales drops, customer behavior, and delivery issues**
- To support **strategic business decisions** using data insights and visualizations

---

## 📂 Datasets Used (6 Tables)

The project uses the following six Blinkit datasets:

1. `blinkit_customers.csv`  
   Customer details and demographics

2. `blinkit_marketing_performance.csv`  
   Marketing spend, channels, and campaign performance

3. `blinkit_orders.csv`  
   Order-level information such as date, time, revenue, and delivery status

4. `blinkit_order_items.csv`  
   Product-level details for each order

5. `blinkit_products.csv`  
   Product category, brand, pricing, and margin information

6. `blinkit_customer_feedback.csv`  
   Customer ratings, feedback text, and sentiment analysis

---

## 🗄️ Data Integration & SQL Strategy

### 🔄 Data Merging Process
- All 6 CSV files are loaded using **Pandas**
- Data cleaning and preprocessing are performed
- Tables are merged step-by-step using common keys such as:
  - `customer_id`
  - `order_id`
  - `product_id`
- After merging all six datasets, a **single consolidated dataset** is created

### 🗃️ Final SQL Table
The final merged dataset is stored in SQL as:

**`blinkit_data`**

All SQL queries, analysis, and dashboards are built using this single table.

---

## 🧰 Libraries & Tools Used
- **Python**
- **Pandas**
- **NumPy**
- **MySQL / SQL**
- **Matplotlib**
- **Seaborn**
- **Streamlit**
- **VS Code**
- **Git & GitHub**

---

## 📊 Business Decision Platform – Analysis Modules

### 1️⃣ Marketing Team Analysis
- Total Revenue & Total Orders
- Revenue vs Marketing Spend
- Marketing Channel Performance
- Target Audience Effectiveness

📈 Helps marketing teams optimize campaign strategies and budget allocation.

---

### 2️⃣ Sales Team Analysis
- Total Revenue and Orders per Day
- Total Revenue and Orders per Month
- Daily Revenue Trend
- Brand-wise Sales Performance
- Category-wise Sales Analysis
- Top-selling Categories  
  (High-performing category: **Dairy & Breakfast**)
- High Value Customers Identification
- Product Margin Analysis
- High Margin Products  
  (Top margin category: **Frozen Vegetables**)

💰 Helps sales teams focus on profitable products and customers.

---

### 3️⃣ Delivery / Operations Team Analysis
- Delivery Partner Load Analysis
- Peak Order Hours (Delay Risk Identification)
- Area-wise Demand Analysis

🚚 Helps improve delivery efficiency and operational planning.

---

### 4️⃣ Customer Feedback Analysis
- Rating vs Sales Relationship
- Impact of Customer Sentiment on Revenue

😊 Helps understand how customer satisfaction affects business performance.

---

### 5️⃣ Sales Drop Analysis (Root Cause Study)
- Sales Drop by Day
- Marketing Spend Comparison During Sales Drop
- Negative Feedback Spike Analysis

🔍 Helps identify **why sales are declining** and what business actions are required.

---

## 📈 Visualizations & Dashboards
- Business KPIs visualized using charts and graphs
- SQL queries connected directly to plots
- Interactive dashboards built using **Streamlit**

---

## 🏁 Final Outcome
This project demonstrates:
- Real-world **data integration using SQL**
- Team-wise **business analytics**
- Strong use of **Python, SQL, and visualization**
- End-to-end **Business Intelligence workflow**

---

## 🚀 Future Enhancements
- Real-time data ingestion
- Sales forecasting models
- Customer churn prediction
- Automated alerts for sales drop

---

## 👩‍💻 Author
**Sandhiya Subash**  
Data Analytics | Python | SQL | Streamlit | Business Intelligence

---

## 🤖 Machine Learning – Delivery Delay Prediction

### 🎯 ML Objective
The goal of the Machine Learning module is to **predict how much delay (in minutes)** an order may face compared to the promised delivery time.

This helps Blinkit to:
- Proactively identify delayed orders
- Improve delivery partner allocation
- Enhance customer satisfaction

---

## 📌 Target Variable
- **Delivery Delay (in minutes)**  
Calculated as the difference between:
- `actual_delivery_time` and `promised_delivery_time`

---

## 🧹 Data Preprocessing
Before training the model, the following preprocessing steps were performed:

- Handling missing values
- Date & time feature extraction  
  (hour, day, peak hours, etc.)
- Encoding categorical variables  
  (area, delivery partner, payment method, category)
- Feature selection based on business relevance
- Splitting data into **train and test sets**

---

## 🧠 Model Training
Multiple regression models were trained and evaluated, including:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor

Model evaluation was done using:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score

---

## 🏆 Best Model Selection
After comparing all models:

✅ **Random Forest Regressor** was selected as the **best-performing model**  
because it:
- Handled non-linear patterns effectively
- Provided better accuracy
- Reduced overfitting compared to other models

---

## 💾 Model Saving
The final trained Random Forest model was saved using **Pickle** for future use.

This allows:
- Reusing the model without retraining
- Easy integration with Streamlit dashboard
- Faster predictions in production

Saved file:
- `delivery_delay_model.pkl`

---

## 🔗 Model Usage
The saved Pickle model can be loaded and used to:
- Predict delivery delay for new orders
- Display delay risk in dashboards
- Support operational decision-making

---

## 📈 Business Impact
- Early detection of delay-prone orders
- Improved delivery planning
- Reduced customer complaints
- Better SLA management

---

## 🚀 Future ML Enhancements
- Real-time delay prediction
- Model retraining with live data
- Classification of high-risk delayed orders
- Explainable AI for delay reasons

