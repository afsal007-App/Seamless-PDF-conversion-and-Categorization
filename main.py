import streamlit as st
import os

st.set_page_config(page_title="Financial Toolkit", layout="centered")

st.title("📊 Financial Toolkit")

option = st.selectbox("Choose a tool", ["🔄 PDF to CSV Converter", "🧠 Categorize Transactions"])

if option == "🔄 PDF to CSV Converter":
    st.markdown("Run `pdf_app/app.py` directly or deploy it as a Streamlit app.")
    st.code("streamlit run pdf_app/app.py")

elif option == "🧠 Categorize Transactions":
    st.markdown("Run `categorization_app/app.py` directly or deploy it as a Streamlit app.")
    st.code("streamlit run categorization_app/app.py")
