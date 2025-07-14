import streamlit as st
import pandas as pd

st.set_page_config(page_title="HealthyPulse Dashboard", layout="wide")

st.title("🩺 HealthyPulse - Patient Vitals Dashboard")

try:
    df = pd.read_parquet("vitals_transformed.parquet")
except Exception as e:
    st.error(f"⚠️ Could not load parquet file: {e}")
    st.stop()

# Show basic stats
st.subheader("📊 Basic Statistics")
st.write(df.describe())

# Risk level distribution
if "risk_level" in df.columns:
    st.subheader("🧠 Risk Level Distribution")
    st.bar_chart(df["risk_level"].value_counts())

# Anomaly breakdown
if "anomaly" in df.columns:
    st.subheader("🚨 Anomaly Flag Breakdown")
    st.bar_chart(df["anomaly"].value_counts())

# Mask type vs risk level
if "masktype_label" in df.columns and "risk_level" in df.columns:
    st.subheader("😷 Mask Type vs Risk Level")
    st.dataframe(df.groupby(["masktype_label", "risk_level"]).size().reset_index(name="count"))

# Filter by risk level
st.subheader("🔍 Filter Patients by Risk Level")
risk_filter = st.selectbox("Choose a risk level", options=["All"] + df["risk_level"].dropna().unique().tolist())

if risk_filter != "All":
    filtered_df = df[df["risk_level"] == risk_filter]
else:
    filtered_df = df

st.write(f"Showing {len(filtered_df)} records")
st.dataframe(filtered_df)

