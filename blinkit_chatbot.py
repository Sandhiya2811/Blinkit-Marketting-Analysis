import pandas as pd
import re
import streamlit as st

from sqlalchemy import create_engine

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DataFrameLoader
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Blinkit Chatbot",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Blinkit Chatbot")
st.caption("Ask business questions")

# ------------------ LOAD DATA (SAME AS YOUR CODE) ------------------
@st.cache_data
def load_data():
    df1 = pd.read_csv("Blinkit - blinkit_products.csv")
    df2 = pd.read_csv("Blinkit - blinkit_orders.csv")
    df3 = pd.read_csv("Blinkit - blinkit_order_items.csv")
    df4 = pd.read_csv("Blinkit - blinkit_marketing_performance.csv")
    df5 = pd.read_csv("Blinkit - blinkit_customers.csv")
    df6 = pd.read_csv("Blinkit - blinkit_customer_feedback.csv")

    engine = create_engine(
        "mysql+mysqlconnector://root:Subash%4028@localhost:3306/blinkit"
    )

    df1.to_sql("blinkit_products", engine, if_exists="replace", index=False)
    df2.to_sql("blinkit_orders", engine, if_exists="replace", index=False)
    df3.to_sql("blinkit_order_items", engine, if_exists="replace", index=False)
    df4.to_sql("blinkit_marketing_performance", engine, if_exists="replace", index=False)
    df5.to_sql("blinkit_customers", engine, if_exists="replace", index=False)
    df6.to_sql("blinkit_customer_feedback", engine, if_exists="replace", index=False)

    query = """
    SELECT
        o.delivery_status,
        o.order_total,
        o.payment_method,

        c.customer_name,
        c.area,
        c.pincode,
        c.customer_segment,
        c.total_orders,
        c.avg_order_value,

        p.product_name,
        p.category,
        p.brand,
        p.price,
        p.mrp,
        p.margin_percentage,
        p.shelf_life_days,

        oi.quantity,
        oi.unit_price,
        (oi.quantity * oi.unit_price) AS item_total,

        f.rating,
        f.feedback_category,
        f.sentiment,
        f.feedback_text,

        m.campaign_name,
        m.channel,
        m.target_audience,
        m.spend,
        m.revenue_generated,
        m.roas

    FROM blinkit_orders o
    LEFT JOIN blinkit_customers c ON o.customer_id = c.customer_id
    LEFT JOIN blinkit_order_items oi ON o.order_id = oi.order_id
    LEFT JOIN blinkit_products p ON oi.product_id = p.product_id
    LEFT JOIN blinkit_customer_feedback f 
        ON o.order_id = f.order_id AND o.customer_id = f.customer_id
    LEFT JOIN blinkit_marketing_performance m
        ON DATE(o.order_date) = m.date;
    """

    df = pd.read_sql(query, engine)
    return df

df = load_data()

# ------------------ TEXT CLEANING (SAME) ------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["clean_feedback"] = df["feedback_text"].apply(clean_text)

df["full_text"] = df.apply(
    lambda row: " | ".join([str(row[col]) for col in df.columns]),
    axis=1
)

# ------------------ VECTOR STORE (SAME) ------------------
@st.cache_resource
def create_vectorstore(dataframe):
    loader = DataFrameLoader(
        dataframe,
        page_content_column="full_text"
    )

    documents = loader.load()

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

vectorstore = create_vectorstore(df)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# ------------------ LLM (SAME) ------------------
llm = ChatGroq(
    groq_api_key="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",
    model_name="llama-3.1-8b-instant",
    temperature=0
)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are ChatGPT, a friendly and helpful business analyst.
You are analyzing Blinkit data.

Data:
{context}

Question:
{question}

Instructions:
Read the data and answer like a business manager.
Keep your answer clear, short, and actionable.
Maximum 5 lines.
"""
)

# ------------------ CHAT MEMORY ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ CHAT INPUT ------------------
user_input = st.chat_input("💬 Ask a question about Blinkit data...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Retrieve context
    docs = retriever.invoke(user_input)
    context = "\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.format(
        context=context,
        question=user_input
    )

    response = llm.invoke(final_prompt)

    # Show assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )
    with st.chat_message("assistant"):
        st.markdown(response.content)
