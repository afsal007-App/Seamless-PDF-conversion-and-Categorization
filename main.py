import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Financial Toolkit", layout="centered")

st.markdown("""
    <style>
    .title {
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .choice-box {
        text-align: center;
        margin-top: 30px;
    }
    .watermark {
        text-align: center;
        font-size: 11px;
        font-style: italic;
        color: rgba(150, 150, 150, 0.7);
        margin-top: 60px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📊 Financial Toolkit</div>', unsafe_allow_html=True)
st.markdown("Welcome! Choose a tool below to get started:")

# Tool selection
tool = st.selectbox(
    "Choose a tool",
    ["🔄 PDF to CSV Converter", "🧠 Categorize Transactions"]
)

# Display corresponding app
if tool == "🔄 PDF to CSV Converter":
    st.markdown("---")
    st.markdown("### Launching: PDF to CSV Converter")
    st.info("Please run the app using `pdf_app/app.py` or deploy that file directly on Streamlit Cloud.")

elif tool == "🧠 Categorize Transactions":
    st.markdown("---")
    st.markdown("### Launching: Categorization Bot")
    st.info("Please run the app using `categorization_app/app.py` or deploy that file directly on Streamlit Cloud.")

# Optional: Display watermark
st.markdown('<div class="watermark">© 2025 Afsal. All Rights Reserved.</div>', unsafe_allow_html=True)
