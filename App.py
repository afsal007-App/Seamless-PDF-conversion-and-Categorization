# Bank PDF Extractor
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bank PDF Extractor", layout="centered")
st.title("🏦 Bank PDF Extractor")

# Dummy DataFrame to simulate parsed PDF
df = pd.DataFrame({
    "Date": ["2025-01-01", "2025-01-02"],
    "Description": ["Amazon Purchase", "ATM Withdrawal"],
    "Amount": [-50.75, -100.00]
})

st.dataframe(df)

if st.button("✅ Save for Categorization"):
    os.makedirs("shared", exist_ok=True)
    df.to_csv("shared/converted.csv", index=False)
    st.success("CSV saved for categorization.")
    st.markdown("[👉 Open Categorization Bot](http://localhost:8502)", unsafe_allow_html=True)
    st.markdown("""
        <script>
        window.open("http://localhost:8502", "_blank");
        </script>
    """, unsafe_allow_html=True)
