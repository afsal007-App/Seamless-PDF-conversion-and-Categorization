import streamlit as st
import pdfplumber
import pandas as pd
import re
import os
from io import BytesIO

def extract_transaction_table(file):
    all_data = []

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    if row and len(row) >= 5:
                        all_data.append(row[:5])  # First 5 columns only

    column_headers = ["Date", "Description", "Debit", "Credit", "Balance"]
    df = pd.DataFrame(all_data, columns=column_headers)

    date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")
    df = df[df["Date"].apply(lambda x: bool(date_pattern.match(str(x).strip())))]

    df["Balance"] = df["Balance"].apply(lambda x: str(x).strip().split()[-1] if pd.notnull(x) else x)

    ignore_keywords = ["closing balance"]
    final_df = df[~df["Description"].str.lower().str.contains('|'.join(ignore_keywords), na=False)]

    final_df = final_df.reset_index(drop=True)
    return final_df

# ------------------------- STREAMLIT APP -------------------------- #
def run():
    st.markdown(
        """
        <style>
        .custom-title {
            font-size: 18px !important;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        </style>
        <div class="custom-title">Bank Statement PDF Parser</div>
        """,
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader("Upload one or more bank PDFs", type=["pdf"], accept_multiple_files=True)

    final_df = None

    if uploaded_files:
        combined_df = pd.DataFrame()

        for file in uploaded_files:
            st.info(f"Processing: {file.name}")
            df = extract_transaction_table(file)
            df["Source File"] = file.name
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        if not combined_df.empty:
            st.success("✅ Transactions Extracted")
            st.dataframe(combined_df, use_container_width=True)

            csv = combined_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "transactions.csv", "text/csv")

            final_df = combined_df

    return final_df
