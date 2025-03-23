import streamlit as st
import importlib

st.set_page_config(page_title="Bank Tool Suite", layout="centered")
st.title("🏦 Bank PDF & Categorization Suite")

choice = st.sidebar.radio("Choose App", ["PDF Converter", "Categorization"])

if choice == "PDF Converter":
    with st.spinner("Launching PDF Converter..."):
        pdf_app = importlib.import_module("pdf_app")
        pdf_app.run_app()

    if "converted_data" in st.session_state:
        if st.button("➡️ Proceed to Categorization"):
            st.session_state["next_app"] = "Categorization"
            st.experimental_rerun()

elif choice == "Categorization" or st.session_state.get("next_app") == "Categorization":
    with st.spinner("Launching Categorizer..."):
        cat_app = importlib.import_module("categorizer_app")
        cat_app.run_app()

    st.session_state["next_app"] = None
