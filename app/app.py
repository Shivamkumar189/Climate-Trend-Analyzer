import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Climate Analyzer", layout="wide")

# -----------------------------
# CUSTOM STYLE (UI MAGIC )
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: white;
}
.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🌍 Climate Trend Analyzer Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("../data/climate_data.csv")
df['date'] = pd.to_datetime(df['date'])

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("⚙️ Controls")

year = st.sidebar.slider(
    "Select Year Range",
    int(df['date'].dt.year.min()),
    int(df['date'].dt.year.max()),
    (2015, 2022)
)

df = df[(df['date'].dt.year >= year[0]) & (df['date'].dt.year <= year[1])]

# -----------------------------
# METRICS
# -----------------------------
mean_temp = df['temperature'].mean()
std_temp = df['temperature'].std()

df['anomaly'] = abs(df['temperature'] - mean_temp) > 2 * std_temp
total_anomalies = df['anomaly'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("🌡 Avg Temp", f"{mean_temp:.2f} °C")
col2.metric("📉 Std Dev", f"{std_temp:.2f}")
col3.metric("⚠️ Anomalies", int(total_anomalies))

# -----------------------------
# TEMPERATURE GRAPH
# -----------------------------
st.subheader("🌡 Temperature Trend")

fig1 = px.line(df, x='date', y='temperature',
               title="Temperature Over Time",
               template="plotly_dark")

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# RAINFALL GRAPH
# -----------------------------
st.subheader("🌧 Rainfall Trend")

fig2 = px.line(df, x='date', y='rainfall',
               title="Rainfall Over Time",
               template="plotly_dark",
               color_discrete_sequence=['cyan'])

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# ANOMALY GRAPH
# -----------------------------
st.subheader("⚠️ Temperature Anomalies")

fig3 = px.scatter(df,
                  x='date',
                  y='temperature',
                  color=df['anomaly'].map({True: "Anomaly", False: "Normal"}),
                  title="Anomaly Detection",
                  template="plotly_dark")

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# ANOMALY TABLE
# -----------------------------
st.subheader("📊 Detected Anomalies (Top 20)")

st.dataframe(df[df['anomaly'] == True].head(20))

# -----------------------------
# INSIGHTS SECTION
# -----------------------------
st.subheader("🧠 Insights")

if total_anomalies > 50:
    st.warning("⚠️ High number of anomalies detected. Climate variability is significant.")
else:
    st.success("✅ Climate patterns are relatively stable.")

st.write(f"""
- Average Temperature: {mean_temp:.2f} °C  
- Variation Level: {std_temp:.2f}  
- Total Anomalies: {total_anomalies}
""")