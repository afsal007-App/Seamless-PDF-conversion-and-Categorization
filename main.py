import streamlit as st
import sys, os

# Page config
st.set_page_config(page_title="Financial Toolkit", layout="wide")

# App paths
sys.path.append(os.path.abspath("pdf_app"))
sys.path.append(os.path.abspath("categorization_app"))

# Imports
import App as pdf_app
import app as categorizer_app

# UI Title
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

# Handle default tab
default_tab = "📄 PDF to CSV Converter"
if st.session_state.get("active_tab") == "Categorizer":
    default_tab = "🧠 Categorizer"
    st.session_state["active_tab"] = None  # reset after switching

tab1, tab2 = st.tabs(["📄 PDF to CSV Converter", "🧠 Categorizer"])

with tab1:
    if default_tab == "📄 PDF to CSV Converter":
        pdf_app.run()

with tab2:
    if default_tab == "🧠 Categorizer":
        categorizer_app.run()
