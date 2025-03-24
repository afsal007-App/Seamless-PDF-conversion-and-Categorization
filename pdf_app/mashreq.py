import PyPDF2
import re
import pandas as pd
import streamlit as st

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

    uploaded_files = st.file_uploader("Upload one or more Mashreq Bank PDF statements", type="pdf", accept_multiple_files=True)
    opening_balance_input = st.text_input("Enter Opening Balance (leave blank to auto-calculate)")

    # ✅ Instruction Box (placed below upload and input)
    st.markdown(
        """
        <style>
        .instructions-box {
            padding: 1.2rem;
            border-left: 6px solid #2c7be5;
            border-radius: 10px;
            margin-top: 1.5rem;
            background-color: rgba(0, 0, 0, 0.0);
            color: var(--text-color);
        }
        .instructions-title {
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .instructions-box ul {
            padding-left: 1.2rem;
        }
        </style>

        <div class="instructions-box">
        <div class="instructions-title">📄 Instructions for Uploading PDFs:</div>
            <ul>
                <li>Upload one or more <strong>Mashreq Bank PDF statements</strong>.</li>
                <li>Rename files in order (e.g., <code>Mashreq1.pdf</code>, <code>Mashreq2.pdf</code>) for proper sorting.</li>
                </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        opening_balance = float(opening_balance_input.replace(",", "")) if opening_balance_input else None
    except ValueError:
        st.warning("Invalid Opening Balance. It will default to auto-calculation.")
        opening_balance = None

    if not uploaded_files:
        st.info("📂 Please upload PDF files to begin.")
        return None

    def extract_number(filename):
        numbers = re.findall(r'\d+', filename)
        return int(numbers[0]) if numbers else float('inf')

    uploaded_files = sorted(uploaded_files, key=lambda x: extract_number(x.name))

    unwanted_phrases = [
        "Opening balance", "ﺍﻟﺘﺎﺭﻳﺦ", "ﺍﻟﻤﻌﺎﻣﻠﺔ", "ﺭﻗﻢ ﺍﻟﻤﺮﺟﻊ", "ﻗﻴﻮﺩ",
        "ﻗﻴﻮﺩ ﺩﺍﺋﻨﻪ", "ﺍﻟﺮﺻﻴﺪ", "page", "The items and balance shown",
        "of the statement date", "All charges, terms and conditions",
        "Please note that for foreign currency", "verified. Report any discrepancies",
        "accurate.", "indicative only",
        "ﺍﻟﺮﺟﺎﺀ ﺍﻟﺘﺄﻛﺪ ﻣﻦ ﺻﺤﺔ ﺍﻟﻤﻌﺎﻣﻼﺕ ﻭﺍﻟﻤﺒﺎﻟﻎ ﺍﻟﻤﺒﻴﻨﺔ ﻏﻰ ﻫﺬﺍ ﺍﻟﻜﺸﻒ",
        "Closing balance", "8 of 8"
    ]

    of_pattern = re.compile(r'\bof\s*\d+\b', re.IGNORECASE)
    date_pattern = re.compile(r'\b\d{4}-\d{2}-\d{2}(?=\D)', re.IGNORECASE)
    amount_pattern = re.compile(r'\b(?:\d{1,3}(?:,\d{3})*|\d+)\.\d{1,2}\b|\b0\b')
    header_pattern = re.compile(r'Date\s*Transaction\s*Reference\s*Number\s*Debit\s*Balance\s*Credit', re.IGNORECASE)

    def extract_transactions(file):
        transactions = []
        current_transaction = []
        current_date = ""
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines = text.splitlines()
                for line in lines:
                    line = line.strip()
                    line = header_pattern.sub('', line)

                    if any(phrase in line for phrase in unwanted_phrases) or of_pattern.search(line):
                        continue

                    date_match = date_pattern.search(line)
                    if date_match:
                        if current_transaction:
                            transactions.append((current_date, current_transaction))
                            current_transaction = []
                        current_date = date_match.group()
                        current_transaction.append(line)
                    else:
                        current_transaction.append(line)

        if current_transaction:
            transactions.append((current_date, current_transaction))

        return transactions

    def parse_structured_data(transactions):
        structured_data = []
        for date, lines in transactions:
            full_text = " ".join(lines).strip()
            all_amounts = amount_pattern.findall(full_text)
            balance = all_amounts[-1] if all_amounts else ""

            if balance:
                balance_index = full_text.rfind(balance)
                description = (full_text[:balance_index] + full_text[balance_index + len(balance):]).strip()
            else:
                description = full_text

            description = re.sub(r'\s+', ' ', description)

            structured_data.append({
                "Date": date,
                "Description": description,
                "Balance": balance
            })
        return structured_data

    all_data = []
    final_df = None

    for file in uploaded_files:
        st.info(f"📄 Processing: {file.name}")
        transactions = extract_transactions(file)
        structured_data = parse_structured_data(transactions)
        df = pd.DataFrame(structured_data)

        df = df[
            df['Date'].notna() &
            df['Balance'].notna() &
            (df['Date'].str.strip() != "") &
            (df['Balance'].str.strip() != "")
        ]

        df['Balance'] = df['Balance'].str.replace(",", "").astype(float)
        df['Amount'] = df['Balance'].diff()
        if opening_balance is not None and not df.empty:
            df.loc[df.index[0], 'Amount'] = df.loc[df.index[0], 'Balance'] - opening_balance

        df['Source_File'] = file.name
        all_data.append(df)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.reset_index(drop=True, inplace=True)

        st.success("✅ All PDFs processed successfully!")
        st.dataframe(final_df, use_container_width=True)

        csv = final_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "all_statements_combined.csv", "text/csv")
    else:
        st.warning("⚠️ No valid transactions extracted from the PDFs.")

    return final_df

if __name__ == "__main__":
    run()
