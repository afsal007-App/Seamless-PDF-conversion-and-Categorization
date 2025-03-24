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

st.markdown("<div class='title'>Financial Toolkit</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📄 PDF to CSV Converter", "🧠 Categorizer"])

with tab1:
    pdf_app.run()

with tab2:
    categorizer_app.run()
