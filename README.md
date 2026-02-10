# 🛒 Blinkit Business Analysis Platform

# file_name: blinkit_project.ipynb

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
- `blinkit_best__model.pkl`

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

---

# file_name: marketing_dashboard.py

## 🖥️ Streamlit Business Analytics Dashboard

This project includes an **interactive Streamlit dashboard** built on top of the unified SQL table (`blinkit_data`).  
The dashboard acts as a **central Business Analytics Platform** for multiple teams.

---

## ⚙️ Dashboard Tech Stack
- **Streamlit** – UI & interaction
- **Pandas** – data handling
- **SQLAlchemy** – database connection
- **MySQL** – backend database
- **Plotly (Express & Graph Objects)** – interactive visualizations

---

## 🔗 Database Connection
- The dashboard connects directly to a **MySQL database**
- Data is fetched from a single consolidated table:

**`blinkit_data`**

This ensures:
- Faster querying
- Consistent data across all analyses
- Centralized business logic

---

## 🎛️ Dashboard Controls
The sidebar provides dynamic controls for analysis:

- **Analysis Type Selection**
  - Time-based Performance
  - Marketing Analysis
  - Sales Analysis
  - Delivery / Operations Analysis
  - Customer Feedback Analysis

- **Date Filters**
  - Last 7 Days
  - Last 30 Days
  - Custom Date Range

- **Raw Data Toggle**
  - Option to view raw SQL data in tabular format

---

## 🔢 Key Performance Indicators (KPIs)
The dashboard displays real-time KPIs based on selected date range:

- 💰 Total Revenue
- 📢 Total Marketing Spend
- 📈 Average ROAS
- ⏱ Average Delivery Delay (minutes)

These KPIs give a quick business health snapshot.

---

## 📊 Analysis Modules

### 1️⃣ Time-based Performance
**Focus:** Revenue vs Ad Spend over time

- Daily revenue trend
- Daily marketing spend comparison
- Dual-axis visualization (line + bar)

**Business Insight:**
- Identifies days where high ad spend does not convert into revenue
- Helps optimize marketing budget allocation

---

### 2️⃣ Marketing Analysis
**Focus:** Campaign & Channel effectiveness

- ROI by campaign and marketing channel
- Spend vs revenue comparison
- Identification of high and low-performing campaigns

**Business Insight:**
- Increase budget for high ROI campaigns
- Stop or optimize low-performing campaigns

---

### 3️⃣ Sales Analysis
**Focus:** Revenue & order behavior

- Orders and revenue by day of the week
- Brand-wise revenue analysis
- Identification of high-performing brands

**Business Insight:**
- Helps plan discounts and inventory
- Identifies peak sales days and strong brands

---

### 4️⃣ Delivery / Operations Analysis
**Focus:** Delivery efficiency and demand patterns

- Hourly order load (peak hour detection)
- Area-wise demand analysis
- Revenue contribution by time and location

**Business Insight:**
- Optimize delivery partner allocation
- Reduce delivery delays during peak hours
- Improve area-wise stocking strategy

---

### 5️⃣ Customer Feedback Analysis
**Focus:** Customer satisfaction impact

- Rating vs orders & revenue
- Negative feedback trend over time
- Sentiment-based performance analysis

**Business Insight:**
- Detect service quality issues early
- Correlate customer sentiment with sales drop
- Improve customer retention strategies

---

## 📂 Raw Data Viewer
- Users can view filtered raw data directly from SQL
- Helps validate analysis and ensures transparency
- Useful for debugging and detailed investigation

---

## 📈 Dashboard Benefits
- Single platform for all business teams
- Interactive and real-time analysis
- Easy to understand business insights
- Scalable for future ML integration

---

## 🔮 Future Enhancements
- ML-based delivery delay prediction integration
- Real-time alert system for delays and sales drop
- Role-based dashboards for different teams
- Deployment on cloud (AWS / GCP)

---

## 🧠 Summary
This Streamlit dashboard transforms raw Blinkit data into **actionable business insights**, enabling smarter decisions across **Marketing, Sales, Operations, and Customer Experience** teams.

---

## Overall Insighta

### Products

- Prioritize high-selling and high-margin products.

- Bundle slow-moving products with popular ones to increase sales.

### Offers & Discounts

- Give festival or seasonal discounts to attract customers.

- Run targeted promotions on low-sales days to boost revenue.

### Delivery Staff / Operations

- Increase delivery staff during peak hours or high-demand days.

- Reward best-performing delivery partners with bonuses.

### Stock & Inventory

- Ensure sufficient stock for high-demand areas and products.

- Use inventory trends to avoid stockouts and lost sales.

### Marketing & Campaigns

- Focus budget on high-ROI campaigns.

- Reduce spend on low-performing campaigns to save cost.

### Customer Engagement / Loyalty

- Target loyal customers with personalized offers.

- Encourage repeat purchases through reward programs(like free delivery).

### Customer Satisfaction

- Quickly address complaints and negative feedback.

- Monitor ratings and sentiment to improve service quality.

### Peak Hour / Time Management

- Prepare extra delivery capacity during peak order hours.

- Use offers to shift demand to off-peak hours.

### Area / Regional Focus

- Allocate stock and delivery staff to high-demand areas.

- Run marketing campaigns in low-demand areas to increase sales.

### Technology / Platform Improvements

- Use dashboards to track performance across campaigns, products, and areas.

- Implement predictive models for demand, sales drop, and delivery delays.

---

# file_name: risk_calculator.py

## 🚨 Machine Learning – Delivery Delay Risk Prediction App

This project includes a **Machine Learning–powered Streamlit application** that predicts **delivery delay (in minutes)** and classifies the **risk level** for Blinkit orders.

The app is designed for **operations managers** to proactively handle delayed deliveries.

---

## 🎯 Objective
- Predict **how many minutes an order may be delayed**
- Categorize the delay into:
  - Low Risk
  - Medium Risk
  - High Risk
- Suggest **immediate operational actions** based on risk level

---

## 🧠 Model Used
- **Random Forest Regressor**
- Selected as the best model after comparing multiple algorithms
- Trained using preprocessed Blinkit data
- Saved as a Pickle file for reuse

**Model file:**
- `blinkit_best__model.pkl`

---

## ⚙️ ML Pipeline
The trained model is a complete pipeline that includes:
- Categorical encoding
- Numerical feature handling
- Random Forest regression model

This ensures **consistent preprocessing during both training and prediction**.

---

## 🖥️ Streamlit ML App Features

### 🔹 Manager Inputs (Minimal & Simple)
The manager only needs to provide:
- Area
- Pincode
- Delivery Hour (0–23)
- Day of the Week
- Month

All other features are **automatically filled using safe default values**  
(median or most frequent values from training data).

---

### 🔹 Internal Default Handling
To reduce manual input errors:
- Non-critical fields are auto-filled
- Defaults are calculated from historical Blinkit data
- Ensures realistic and stable predictions

---

## 🔮 Prediction Output
The app predicts:
- **Expected delivery delay (minutes)**
- **Delivery risk level**
- **Risk percentage**

### Risk Classification Logic
- **Low Risk** → Delay ≤ 15 minutes
- **Medium Risk** → Delay between 15–30 minutes
- **High Risk** → Delay > 30 minutes

Early delivery (negative delay) is treated as **zero delay**.

---

## 🚦 Operational Risk Actions

Based on the predicted risk level, the app suggests actions:

### 🔴 High Risk
- Allocate extra delivery riders
- Notify customers in advance
- Prepare contingency delivery plans

### 🟠 Medium Risk
- Monitor orders closely
- Keep backup riders ready

### 🟢 Low Risk
- Continue normal operations

---

## 📊 Business Impact
- Early identification of delayed orders
- Better delivery partner planning
- Reduced customer complaints
- Improved SLA compliance
- Data-driven operational decisions

---

## 🔗 Integration Capability
- Can be integrated into the main Streamlit Business Dashboard
- Can be extended for real-time prediction using live order data
- Supports future automation and alert systems

---

## 🚀 Future Enhancements
- Real-time delay prediction
- Auto-alerts to operations team
- Explainable AI for delay reasons
- Model retraining with live data

---

## 🧠 Summary
This ML-powered delivery risk calculator transforms historical Blinkit data into **actionable operational intelligence**, enabling proactive delivery management and improved customer experience.

---

# file_name: rag.ipynb

## 🤖 GenAI / RAG – Customer Feedback Root Cause Analysis

This project includes a **Retrieval Augmented Generation (RAG)** module to analyze **customer feedback stored in SQL** and automatically identify the **root causes of negative feedback** using a Large Language Model (LLM).

---

## 🎯 Objective
- Analyze customer feedback text at scale
- Identify **common reasons for negative feedback**
- Convert unstructured feedback into **actionable business insights**
- Support customer experience and operations teams

---

## 🗄️ Data Source
- Feedback data is fetched from the **SQL table `blinkit_data`**
- Key columns used:
  - `feedback_text`
  - `rating`
  - `sentiment`
  - `delivery_status`
  - `area`, `pincode`
  - `product`, `category`, `brand`
  - `campaign`, `channel`
  - `order_total`, `delay_minutes`

---

## 🧹 Text Preprocessing
Customer feedback text is cleaned before embedding:

- Convert text to lowercase
- Remove URLs
- Remove special characters and numbers
- Remove extra spaces
- Store cleaned text as `clean_feedback`

This improves embedding quality and retrieval accuracy.

---

## 📄 Document Creation
- Each row in the dataset is converted into a **single combined text document**
- All columns are merged into one string (`full_text`)
- This ensures **business context is preserved** during retrieval

---

## 🧠 Embedding Model
- **HuggingFace Sentence Transformer**
- Model used:

`sentence-transformers/all-MiniLM-L6-v2`

This converts feedback and related business data into dense vector embeddings.

---

## 📦 Vector Store
- **FAISS** is used as the vector database
- Enables fast semantic search on customer feedback
- Top **5 most relevant records** are retrieved per question

---

## 🔍 Retrieval Strategy
- User question is converted into an embedding
- FAISS retrieves the most relevant feedback records
- Retrieved records are passed as context to the LLM

---

## 🧾 Prompt Engineering
A custom prompt is designed to:
- Act as a **business analyst**
- Read customer complaints
- Identify **root causes**
- Provide **short, clear summaries**
- Suggest **actionable business improvements**

Response constraints:
- Maximum 5 lines
- Friendly and professional tone
- Business-focused insights

---

## 🧠 LLM Used
- **Groq LLM**
- Model: `llama-3.1-8b-instant`
- Temperature: `0` (deterministic, factual responses)

This ensures consistent and reliable summaries.

---

## ❓ Example Question

---

## 📤 Output
The system generates:
- A concise summary of **main complaint themes**
- Clear identification of root causes such as:
  - Delivery delays
  - Poor packaging
  - Product quality issues
  - Payment or app-related problems
- Actionable recommendations for improvement

---

## 📊 Business Impact
- Converts thousands of feedback records into insights
- Saves manual analysis time
- Helps teams fix root problems faster
- Improves customer satisfaction and retention

---

## 🔗 Integration Possibilities
- Can be integrated into Streamlit dashboard
- Supports conversational analytics (Ask your data)
- Extendable to sales, marketing, and delivery questions

---

## 🚀 Future Enhancements
- Real-time feedback ingestion
- Sentiment trend alerts
- Feedback category prediction
- Voice-of-customer dashboard

---

## 🧠 Summary
This RAG-based GenAI module enables **intelligent feedback analysis** by combining SQL data, vector search, and LLMs, turning raw customer complaints into **clear business actions**.

---

# file_name: chatbot.py

# 🛒 Blinkit Business Intelligence & AI Chatbot Project

## 📌 Project Overview
This project is an **end-to-end Business Decision Platform** built using **Blinkit data**.  
It integrates **SQL, Python, Data Analysis, Machine Learning, NLP, LLM, and Streamlit** to support **managerial and strategic decision-making**.

A key highlight of this project is an **AI-powered chatbot** designed to **answer manager-level business questions** such as:
- Why sales are going down?
- What is the main reason for negative customer feedback?
- Which area or time has high delivery delays?
- Which marketing channel performs best?

The chatbot reads data directly from Blinkit’s unified analytical table and responds like a **business manager**, providing **clear, short, and actionable insights** instead of raw technical output.

The project includes:
- Data integration from **6 tables**
- SQL-based data modeling
- Business analytics for multiple teams
- Machine Learning for delivery delay prediction
- **Manager-focused AI Chatbot using RAG architecture**

---

## 🎯 Project Objective (Motive)
- Centralize Blinkit data into a **single analytical table**
- Provide insights for **Marketing, Sales, Operations, and Customer Experience**
- Predict **delivery delay** using Machine Learning
- Build an **AI-powered chatbot** to answer business questions using natural language

---

## 🗂️ Datasets Used (6 Tables)

| File Name |
|----------|
| Blinkit - blinkit_products.csv |
| Blinkit - blinkit_orders.csv |
| Blinkit - blinkit_order_items.csv |
| Blinkit - blinkit_marketing_performance.csv |
| Blinkit - blinkit_customers.csv |
| Blinkit - blinkit_customer_feedback.csv |

---

## 🛠️ Tech Stack & Libraries Used

### 🔹 Programming & Database
- Python
- SQL (MySQL)
- SQLAlchemy

### 🔹 Data & Visualization
- Pandas
- NumPy
- Matplotlib
- Seaborn

### 🔹 Machine Learning
- Scikit-learn
- Random Forest Regressor
- Pickle (Model Saving)

### 🔹 NLP & AI
- LangChain
- HuggingFace Embeddings
- FAISS Vector Database
- Groq LLM (LLaMA 3.1)

### 🔹 Frontend
- Streamlit

---

## 🧩 Data Architecture (6 Tables → Single Table)

All 6 datasets are:
1. Loaded using Pandas  
2. Stored in **MySQL database**
3. Joined using SQL (`LEFT JOIN`)
4. Converted into **one unified Blinkit analytical table**

### 🔗 SQL Join Logic
- Orders → Customers
- Orders → Order Items → Products
- Orders → Customer Feedback
- Orders → Marketing Performance (date based)

This single table is used for:
- Analytics
- Machine Learning
- AI Chatbot

---

## 📊 Business Decision Platform – Team Wise Analysis

---

## 📣 1. Marketing Team Analysis
- Revenue vs Marketing Spend
- Channel Performance (Email, Ads, Social)
- ROAS Analysis
- Target Audience Effectiveness
- Campaign wise Revenue Contribution

---

## 💰 2. Sales Team Analysis
- Total Revenue & Orders per Day
- Monthly Sales Trend
- Brand-wise Sales Performance
- Category-wise Sales Analysis
- Top-selling Category: **Dairy & Breakfast**
- High Value Customers
- Product Margin Analysis
- High Margin Products: **Frozen Vegetables**

---

## 🚚 3. Delivery / Operations Team Analysis
- Delivery Partner Load
- Peak Order Hours (Delay Risk)
- Area-wise Demand Analysis
- Delivery Status vs Orders

---

## ⭐ 4. Customer Feedback Analysis
- Rating vs Sales
- Sentiment Impact on Revenue
- Feedback Category Analysis
- Common Reasons for Negative Feedback

---

## 📉 5. Why Sales Are Down?
- Sales Drop by Day
- Marketing Spend Reduction Check
- Negative Feedback Spike Analysis
- Delay Impact on Ratings & Orders

---

## 🤖 Machine Learning – Delivery Delay Prediction

### 🎯 ML Objective
Predict **delivery delay duration** based on:
- Order details
- Area
- Time
- Delivery status
- Product & order features

### 🧪 Steps Followed
1. Data Cleaning & Preprocessing
2. Feature Encoding
3. Train-Test Split
4. Model Training
5. Model Comparison

### 🏆 Best Model
- **Random Forest Regressor**
- Highest accuracy & lowest error

### 💾 Model Deployment
- Trained model saved using **Pickle**
- Used for future delay prediction

---

## 🧠 AI Chatbot (RAG – Retrieval Augmented Generation)

### 📌 Purpose
Allow business users to **ask questions in natural language** like:
- “Why customers are unhappy?”
- “Which area has delivery issues?”
- “What is the common negative feedback?”

---

## 🔄 Chatbot Architecture

1. SQL → Unified Blinkit Table
2. Text Cleaning (Regex)
3. Full Row Text Conversion
4. Vector Embedding (HuggingFace)
5. FAISS Vector Store
6. Context Retrieval (Top-K)
7. LLM Answer Generation (Groq – LLaMA 3.1)

---

## 🧼 Text Preprocessing
- Lowercasing
- URL removal
- Special character removal
- Whitespace normalization

---

## 💬 Streamlit Chatbot Features
- Interactive chat UI
- Chat memory (session based)
- Business-friendly responses
- Actionable insights
- Fast LLM response using Groq







