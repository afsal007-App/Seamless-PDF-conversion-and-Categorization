import streamlit as st
import sys, os

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="Financial Toolkit", layout="wide")

# 🧠 Add paths to access other apps
sys.path.append(os.path.abspath("pdf_app"))
sys.path.append(os.path.abspath("categorization_app"))

import App as pdf_app
import app as categorizer_app  # same name is fine due to import order

# ✅ UI
st.markdown("""
    <style>
    .title {
        font-size: 1.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown("<h1 style='text-align: center;'>📊 Financial Toolkit</h1>", unsafe_allow_html=True)

# Initialize session state
if "converted_df" not in st.session_state:
    st.session_state.converted_df = None

# Tabs
tab1, tab2 = st.tabs(["📄 PDF to CSV Converter", "🧠 Categorizer"])

# === PDF Converter Tab ===
with tab1:
    st.markdown("### 🔄 Convert PDF to CSV")
    df = pdf_app.run()
    if isinstance(df, pd.DataFrame):
        if st.button("📤 Send to Categorizer"):
            st.session_state.converted_df = df
            st.success("✅ Sent to Categorizer tab!")

# === Categorizer Tab ===
with tab2:
    st.markdown("### 🧠 Categorize Transactions")
    categorizer_app.run(preloaded_df=st.session_state.converted_df)
