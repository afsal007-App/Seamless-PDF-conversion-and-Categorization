import streamlit as st
import pdfplumber
import pandas as pd
import re
import os

def extract_transaction_table(pdf_path):
    all_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row and len(row) >= 5:
                        all_data.append(row[:5])

    column_headers = ["Date", "Description", "Debit", "Credit", "Balance"]
    df = pd.DataFrame(all_data, columns=column_headers)

    date_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")
    df = df[df["Date"].apply(lambda x: bool(date_pattern.match(str(x).strip())))]

    df["Balance"] = df["Balance"].apply(lambda x: str(x).strip().split()[-1] if pd.notnull(x) else x)

    ignore_keywords = ["closing balance"]
    final_df = df[~df["Description"].str.lower().str.contains('|'.join(ignore_keywords), na=False)]

    final_df = final_df.reset_index(drop=True)
    return final_df

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
    <div class="custom-title">RAK Bank PDF Processor</div>
    """,
    unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader("Upload RAK Bank PDF file(s)", type="pdf", accept_multiple_files=True)

    combined_df = pd.DataFrame()

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())

                df = extract_transaction_table(temp_path)
                df["Source File"] = uploaded_file.name
                combined_df = pd.concat([combined_df, df], ignore_index=True)

                os.remove(temp_path)
            except Exception as e:
                st.error(f"Failed to process {uploaded_file.name}: {e}")

        if not combined_df.empty:
            st.success("✅ PDF converted and saved as CSV successfully!")
            st.dataframe(combined_df)
            csv = combined_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "combined_transactions.csv", "text/csv")
        else:
            st.warning("⚠️ No valid transaction data extracted. Please check your files.")

    return combined_df
