import streamlit as st
import pdfplumber
import pandas as pd
import re
from io import BytesIO

# ---------- Regex Patterns ----------
date_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}")
amount_pattern = re.compile(r"(-?\d{1,3}(?:,\d{3})*(?:\.\d{2})?)")
account_number_pattern = re.compile(r"^\d{10}$")
iban_pattern = re.compile(r"AE\d{2}\d+")
ref_number_pattern = re.compile(r"^[PA]\d{9}$")

# ---------- Extract IBAN-Currency Mapping ----------
def extract_iban_currency_map(pdf):
    supported_currencies = ["AED", "USD", "EUR"]
    iban_currency_map = {}

    for page in pdf.pages[:2]:
        text = page.extract_text()
        if not text:
            continue
        lines = text.splitlines()
        for line in lines:
            if "AE" in line and any(cur in line for cur in supported_currencies):
                iban_match = iban_pattern.search(line)
                if iban_match:
                    iban = iban_match.group()
                    for currency in supported_currencies:
                        if currency in line:
                            iban_currency_map[iban] = currency
                            break
    return iban_currency_map

# ---------- Main PDF Processing Function ----------
def process_uploaded_pdfs(uploaded_files):
    all_transactions = []

    for uploaded_file in uploaded_files:
        with pdfplumber.open(uploaded_file) as pdf:
            iban_currency_map = extract_iban_currency_map(pdf)

            lines = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines.extend(text.splitlines())

        current_account_number = None
        current_iban = None

        for i, line in enumerate(lines):
            clean_line = line.strip().lower()

            if "account holder name" in clean_line:
                current_account_number = None
                current_iban = None

                for j in range(i, i + 15):
                    if j >= len(lines):
                        break
                    l = lines[j].strip()
                    if account_number_pattern.match(l):
                        current_account_number = l
                    if iban_match := iban_pattern.search(l):
                        current_iban = iban_match.group()
                        if not current_account_number:
                            current_account_number = current_iban[-10:]

            if date_pattern.match(line.strip()):
                parts = line.split()
                if len(parts) < 2:
                    continue

                date = parts[0]
                ref_candidate = parts[1]
                if ref_number_pattern.match(ref_candidate):
                    ref_number = ref_candidate
                    desc_start = 2
                else:
                    ref_number = ""
                    desc_start = 1

                balance_match = amount_pattern.findall(line)
                if len(balance_match) >= 2:
                    amount = balance_match[-2].replace(',', '')
                    balance = balance_match[-1].replace(',', '')
                    description = ' '.join(parts[desc_start:-2])
                else:
                    amount = ""
                    balance = ""
                    description = ' '.join(parts[desc_start:])

                currency = iban_currency_map.get(current_iban, None)

                all_transactions.append({
                    "Date": date,
                    "Ref Number": ref_number,
                    "Description": description.strip(),
                    "Amount": amount,
                    "Balance": balance,
                    "Currency": currency,
                    "Account Number": current_account_number,
                    "IBAN": current_iban,
                    "Source File": uploaded_file.name
                })

    return pd.DataFrame(all_transactions)

# ---------- Streamlit App Entry Point ----------
def run():
    st.markdown(
        """<style>
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
    uploaded_files = st.file_uploader("Upload one or more Wio bank PDFs", type=["pdf"], accept_multiple_files=True)

    final_df = pd.DataFrame()

    if uploaded_files:
        if st.button("Process PDFs"):
            final_df = process_uploaded_pdfs(uploaded_files)

            if final_df.empty:
                st.warning("No transactions found.")
            else:
                st.success("Transactions extracted successfully!")
                st.dataframe(final_df)

                for iban, group_df in final_df.groupby("IBAN"):
                    clean_iban = iban.replace('/', '_') if iban else "unknown"
                    csv = group_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label=f"📥 Download CSV for IBAN {clean_iban}",
                        data=csv,
                        file_name=f"transactions_{clean_iban}.csv",
                        mime="text/csv"
                    )

    return final_df
