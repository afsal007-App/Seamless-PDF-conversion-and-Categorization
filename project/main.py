import streamlit as st
import runpy
import os

st.set_page_config(page_title="Bank Tool Suite", layout="centered")
st.title("🏦 Bank PDF & Categorization Suite")

# Dynamically get the current directory (very important)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Sidebar option
choice = st.sidebar.radio("Choose App", ["PDF Converter", "Categorization"])

# PDF Converter App
if choice == "PDF Converter":
    with st.spinner("Launching PDF Converter..."):
        runpy.run_path(os.path.join(BASE_DIR, "pdf_app.py"))

    if "converted_data" in st.session_state:
        if st.button("➡️ Proceed to Categorization"):
            st.session_state["next_app"] = "Categorization"
            st.experimental_rerun()

# Categorization App
elif choice == "Categorization" or st.session_state.get("next_app") == "Categorization":
    with st.spinner("Launching Categorizer..."):
        runpy.run_path(os.path.join(BASE_DIR, "categorizer_app.py"))

    st.session_state["next_app"] = None
