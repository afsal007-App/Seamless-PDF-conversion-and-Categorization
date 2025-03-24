# ✅ Updated Emirates_Islamic_Bank.py – Returns DataFrame to App.py

import pdfplumber
import pandas as pd
import streamlit as st

# -------------------- PDF Parsing Logic --------------------

header_keywords = ["Transaction Date", "Narration", "Debit", "Credit", "Running Balance"]

def process(pdf_files):
    all_transactions = []

    for pdf_file in pdf_files:
        structured_data = []

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                table = page.extract_table()

                if table:
                    for row in table:
                        if len(row) < 6:
                            continue

                        if any(header in row[0] for header in header_keywords) and "Running Balance" in row:
                            continue

                        transaction_date = row[0].replace("\n", " ").strip()
                        narration = row[2].replace("\n", " ").strip()

                        debit = 0.0
                        credit = 0.0

                        try:
                            if row[3] and row[3] != "0.00":
                                debit = float(row[3].replace(',', '').strip())
                        except ValueError:
                            debit = 0.0

                        try:
                            if row[4] and row[4] != "0.00":
                                credit = float(row[4].replace(',', '').strip())
                        except ValueError:
                            credit = 0.0

                        running_balance = row[5].replace("\n", " ").strip() if len(row) > 5 else None

                        structured_data.append([transaction_date, narration, debit, credit, running_balance])

        all_transactions.extend(structured_data)

    # ✅ Return empty DataFrame if no transactions found
    if not all_transactions:
        return pd.DataFrame(columns=["Transaction Date", "Narration", "Debit", "Credit", "Account Balance"])

    df_combined = pd.DataFrame(all_transactions, columns=["Transaction Date", "Narration", "Debit", "Credit", "Account Balance"])
    df_combined = df_combined[df_combined["Transaction Date"] != "Transaction Date"]
    df_combined["Account Balance"] = df_combined["Account Balance"].astype(str)
    df_combined["Transaction Date"] = pd.to_datetime(df_combined["Transaction Date"], format="%d-%m-%Y", errors='coerce')
    df_combined = df_combined.dropna(subset=["Transaction Date"])

    merged_data = []
    prev_row = None

    for _, row in df_combined.iterrows():
        if prev_row is not None and row["Account Balance"] == prev_row["Account Balance"]:
            prev_row["Narration"] += " " + row["Narration"]
            prev_row["Debit"] = max(prev_row["Debit"], row["Debit"])
            prev_row["Credit"] = max(prev_row["Credit"], row["Credit"])
        else:
            if prev_row is not None:
                merged_data.append(prev_row)
            prev_row = row.copy()

    if prev_row is not None:
        merged_data.append(prev_row)

    df_final = pd.DataFrame(merged_data)
    df_final = df_final.sort_values(by="Transaction Date", ascending=True)
    df_final = df_final.drop_duplicates(subset=["Account Balance"], keep="first")

    return df_final

# -------------------- Streamlit UI --------------------

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
    <div class="custom-title">Bank PDF Processor</div>
    """,
    unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader("Upload one or more Emirates Islamic Bank PDF statements", type="pdf", accept_multiple_files=True)

    final_df = None

    if uploaded_files:
        st.info("Processing uploaded files...")
        df = process(uploaded_files)

        if df.empty:
            st.warning("⚠️ No transactions found.")
        else:
            st.success("✅ Transactions extracted successfully!")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download CSV", csv, "emirates_islamic_transactions.csv", "text/csv")

            # ✅ Return to App.py
            final_df = df

    return final_df
