import streamlit as st
import pandas as pd

st.set_page_config(page_title="HealthyPulse Dashboard", layout="wide")
st.title("🩺 HealthyPulse - Real-Time Patient Vitals Dashboard")

# Load Data
try:
    df = pd.read_parquet("vitals_transformed.parquet")
except Exception as e:
    st.error(f"⚠️ Could not load data: {e}")
    st.stop()

# -----------------------------
# 💡 Header Metrics
# -----------------------------
st.markdown("## 🧾 Summary Overview")

col1, col2, col3 = st.columns(3)
col1.metric("📈 Total Records", len(df))
col2.metric("🧠 Unique Risk Levels", df['risk_level'].nunique() if 'risk_level' in df.columns else "N/A")
col3.metric("🚨 Total Anomalies", df['anomaly'].sum() if 'anomaly' in df.columns else "N/A")

st.markdown("---")

# -----------------------------
# 📊 Descriptive Statistics
# -----------------------------
st.subheader("📊 Basic Descriptive Statistics")
st.dataframe(df.describe().style.format("{:.2f}"), use_container_width=True)

# -----------------------------
# 🧠 Risk Level Distribution
# -----------------------------
if "risk_level" in df.columns:
    st.subheader("🧠 Risk Level Distribution")
    risk_counts = df["risk_level"].value_counts()
    st.bar_chart(risk_counts)

# -----------------------------
# 🚨 Anomaly Breakdown
# -----------------------------
if "anomaly" in df.columns:
    st.subheader("🚨 Anomaly Flag Breakdown")
    st.bar_chart(df["anomaly"].value_counts())

# -----------------------------
# 😷 Mask Type vs Risk Level
# -----------------------------
if "masktype_label" in df.columns and "risk_level" in df.columns:
    st.subheader("😷 Mask Type vs Risk Level")
    grouped = df.groupby(["masktype_label", "risk_level"]).size().reset_index(name="Count")
    st.dataframe(grouped.style.background_gradient(cmap="YlOrRd"), use_container_width=True)

# -----------------------------
# 🔍 Filter Section
# -----------------------------
st.markdown("---")
st.subheader("🔍 Filter Patients by Risk Level")

risk_levels = df["risk_level"].dropna().unique().tolist()
risk_filter = st.selectbox("Select a risk level:", options=["All"] + sorted(risk_levels))

if risk_filter != "All":
    filtered_df = df[df["risk_level"] == risk_filter]
else:
    filtered_df = df

st.write(f"🧾 Showing **{len(filtered_df)}** matching records")
st.dataframe(filtered_df.style.applymap(
    lambda x: "background-color: #ffcccc" if str(x).lower() in ["critical", "high"] else "",
    subset=["risk_level"]
), use_container_width=True)
