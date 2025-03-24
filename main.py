import streamlit as st
import sys, os

# ✅ MUST BE FIRST!
st.set_page_config(page_title="Financial Toolkit", layout="wide")

st.title("📊 Financial Toolkit")

tab1, tab2 = st.tabs(["🔄 PDF to CSV Converter", "🧠 Categorizer"])

with tab1:
    sys.path.append(os.path.abspath("pdf_app"))
    import app as pdf_app
    pdf_app.run()

with tab2:
    sys.path.append(os.path.abspath("categorization_app"))
    import app as categorizer_app
    categorizer_app.run()
