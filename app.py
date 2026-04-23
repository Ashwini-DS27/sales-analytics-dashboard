import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("sales.csv")

# Fix date format
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
df = df.dropna(subset=["Date"])

# -------------------------
# UI TITLE
# -------------------------
st.set_page_config(layout="wide")
st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive dashboard for business insights")

# -------------------------
# SIDEBAR FILTERS
# -------------------------
st.sidebar.header("🔎 Filters")

start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

# Store filter
stores = df["Store"].unique()
selected_store = st.sidebar.selectbox("Select Store", ["All"] + list(stores))

# Apply filters
df_filtered = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

if selected_store != "All":
    df_filtered = df_filtered[df_filtered["Store"] == selected_store]

# -------------------------
# KPI SECTION
# -------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_sales = df_filtered["Weekly_Sales"].sum()
avg_sales = df_filtered["Weekly_Sales"].mean()
max_sales = df_filtered["Weekly_Sales"].max()

col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("📈 Avg Sales", f"₹ {avg_sales:,.0f}")
col3.metric("🔥 Max Sales", f"₹ {max_sales:,.0f}")

# -------------------------
# SALES TREND
# -------------------------
st.subheader("📈 Sales Trend Over Time")

trend = df_filtered.groupby("Date")["Weekly_Sales"].sum().reset_index()

fig, ax = plt.subplots()
ax.plot(trend["Date"], trend["Weekly_Sales"], linewidth=2)

# Smooth line (rolling avg)
trend["Smooth"] = trend["Weekly_Sales"].rolling(7).mean()
ax.plot(trend["Date"], trend["Smooth"], linestyle="--")

ax.set_xlabel("Date")
ax.set_ylabel("Sales")

st.pyplot(fig)

# -------------------------
# MONTHLY ANALYSIS
# -------------------------
st.subheader("📊 Monthly Sales")

df_filtered["Month"] = df_filtered["Date"].dt.to_period("M")
monthly = df_filtered.groupby("Month")["Weekly_Sales"].sum()

monthly.index = monthly.index.astype(str)

fig2, ax2 = plt.subplots()
ax2.plot(monthly.index, monthly.values, marker="o")

plt.xticks(rotation=45)
st.pyplot(fig2)

# -------------------------
# TOP STORES BAR CHART
# -------------------------
st.subheader("🏬 Top Stores by Sales")

store_sales = df.groupby("Store")["Weekly_Sales"].sum().sort_values(ascending=False)

fig3, ax3 = plt.subplots()
ax3.bar(store_sales.index, store_sales.values)

plt.xticks(rotation=45)
st.pyplot(fig3)