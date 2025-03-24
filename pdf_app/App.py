# ✅ Updated App.py (PDF to CSV Converter + Inline Categorizer Preview)

import streamlit as st
import pandas as pd
from shared.core import save_converted_df
from io import BytesIO

# Import bank modules
import Rak_Bank
import al_jazira_bank
import emirates_islamic_bank
import fab_bank
import Wio_bank
import adib_bank
import mashreq
import adcb

# 🔁 Categorizer utility functions (moved from categorization app)
def clean_text(text):
    import re
    return re.sub(r'\s+', ' ', str(text).lower().replace('–', '-').replace('—', '-')).strip()

def load_master_file():
    url = "https://docs.google.com/spreadsheets/d/1I_Fz3slHP1mnfsKKgAFl54tKvqlo65Ug/export?format=xlsx"
    try:
        df = pd.read_excel(url)
        df['Key Word'] = df['Key Word'].astype(str).apply(clean_text)
        return df
    except Exception as e:
        st.error(f"⚠️ Error loading master file: {e}")
        return pd.DataFrame()

def find_description_column(columns):
    possible = ['description', 'details', 'narration', 'particulars', 'transaction details', 'remarks']
    return next((col for col in columns if any(name in col.lower() for name in possible)), None)

def categorize_description(description, master_df):
    cleaned = clean_text(description)
    for _, row in master_df.iterrows():
        if row['Key Word'] and row['Key Word'] in cleaned:
            return row['Category']
    return 'Uncategorized'

def categorize_statement(statement_df, master_df, desc_col):
    statement_df['Categorization'] = statement_df[desc_col].apply(lambda x: categorize_description(x, master_df))
    return statement_df

def run():
    bank_modules = {
        "🏦 RAK Bank": Rak_Bank,
        "🏢 Emirates Islamic Bank": emirates_islamic_bank,
        "🏬 FAB Bank": fab_bank,
        "🏛️ WIO Bank": Wio_bank,
        "🏤 ADIB Bank": adib_bank,
        "🏤 Mashreq Neo Bank": mashreq,
        "🏤 ADCB Bank": adcb
    }

    # UI Styling
    st.markdown("""
        <style>
        .title {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        padding-top: 1rem;
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
        }
        .subtext {
            text-align: center;
            font-size: 1.05rem;
            color: #aaa;
            margin-top: -10px;
            margin-bottom: 30px;
        }
        .dropdown-label {
            font-size: 1.2rem;
            font-weight: 600;
            color: #cdb4d4;
            margin-bottom: 12px;
        }
        hr {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin: 40px 0;
        }
        @keyframes glow {
            from { text-shadow: 0 0 5px #886dc7, 0 0 10px #cdb4d4; }
            to { text-shadow: 0 0 12px #EBE3D5, 0 0 2px #B5CB99; }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>Bank Statement PDF Extractor</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>Convert your bank PDFs into clean, usable data \U0001F4C4 ➡️ \U0001F4C8</div>", unsafe_allow_html=True)

    st.markdown('<div class="dropdown-label"> Select Your Bank</div>', unsafe_allow_html=True)
    selected_bank = st.selectbox("", list(bank_modules.keys()))
    st.markdown("<hr>", unsafe_allow_html=True)

    if selected_bank:
        df = bank_modules[selected_bank].run()
        if isinstance(df, pd.DataFrame):
            save_converted_df(df)
            st.success("✅ PDF converted and saved as CSV successfully!")
            st.dataframe(df.head())

            # 🔁 Inline categorization
            st.subheader("🧠 Categorization Preview")

            with st.spinner("Loading master file..."):
                master_df = load_master_file()

            if not master_df.empty:
                desc_col = find_description_column(df.columns)
                if desc_col:
                    categorized_df = categorize_statement(df.copy(), master_df, desc_col)
                    st.success("✅ Categorized successfully!")
                    st.dataframe(categorized_df.head(), use_container_width=True)

                    buffer = BytesIO()
                    categorized_df.to_excel(buffer, index=False)
                    buffer.seek(0)
                    st.download_button(
                        label="📥 Download Categorized Output",
                        data=buffer,
                        file_name="Categorized_Output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("⚠️ Could not find a valid description column.")
            else:
                st.error("⚠️ Master categorization file failed to load.")
        else:
            st.warning("⚠️ No data returned from the selected bank's parser.")
