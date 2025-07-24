import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="centered")
st.title("📊 Sales Dashboard (Python + Pandas + NumPy + Streamlit)")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload Sales Data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Date"])

    # Preprocess
    df["Revenue"] = df["Units"] * df["Price"]
    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    # Summary Stats
    total_sales = int(df["Units"].sum())
    total_revenue = round(df["Revenue"].sum(), 2)
    average_price = round(np.mean(df["Price"]), 2)

    # Top Product
    top_product = df.groupby("Product")["Revenue"].sum().idxmax()

    # Monthly Sales
    monthly = df.groupby("Month").agg({
        "Units": "sum",
        "Revenue": "sum"
    }).reset_index()

    # Show table
    st.subheader("📋 Sales Data")
    st.dataframe(df)

    # KPI Cards
    st.subheader("📈 Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🛒 Total Units", total_sales)
    col2.metric("💰 Total Revenue", f"${total_revenue}")
    col3.metric("🔢 Avg. Price", f"${average_price}")
    col4.metric("🏆 Top Product", top_product)

    # Monthly Trend Chart
    st.subheader("📊 Monthly Revenue Trend")
    st.line_chart(monthly.set_index("Month")["Revenue"])

    st.subheader("📦 Revenue by Product")
    product_revenue = df.groupby("Product")["Revenue"].sum()
    st.bar_chart(product_revenue)

else:
    st.info("Please upload a CSV file to begin analysis.")
