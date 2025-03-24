import streamlit as st
import sys, os

st.set_page_config(page_title="Financial Toolkit", layout="wide")

sys.path.append(os.path.abspath("pdf_app"))
sys.path.append(os.path.abspath("categorization_app"))

import App as pdf_app
import app as categorizer_app

st.markdown("""
    <style>
    .title {
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📊 Financial Toolkit</div>", unsafe_allow_html=True)

default_tab = 0
if st.session_state.get("active_tab") == "Categorizer":
    default_tab = 1
    st.session_state["active_tab"] = None

tab1, tab2 = st.tabs(["📄 PDF to CSV Converter", "🧠 Categorizer"])
tabs = [tab1, tab2]

with tabs[default_tab]:
    if default_tab == 0:
        pdf_app.run()
    else:
        categorizer_app.run()
