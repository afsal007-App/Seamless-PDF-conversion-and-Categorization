# Categorization Bot
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Categorization Bot", layout="centered")
st.title("🧠 Categorization Bot")

def clean_text(text):
    return str(text).lower().strip()

def find_description_column(columns):
    keywords = ['description', 'details', 'narration']
    for col in columns:
        if any(k in col.lower() for k in keywords):
            return col
    return None

def categorize_description(desc):
    desc = clean_text(desc)
    if 'amazon' in desc:
        return 'Shopping'
    elif 'atm' in desc:
        return 'Cash Withdrawal'
    return 'Uncategorized'

csv_path = "shared/converted.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    st.success("Auto-loaded CSV from PDF extractor.")
    st.dataframe(df)

    desc_col = find_description_column(df.columns)
    if desc_col:
        df["Category"] = df[desc_col].apply(categorize_description)
        st.dataframe(df)

        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button("📥 Download Categorized Excel", buffer, "categorized.xlsx")
    else:
        st.error("Description column not found.")
else:
    st.info("Upload or trigger a conversion from App 1.")
