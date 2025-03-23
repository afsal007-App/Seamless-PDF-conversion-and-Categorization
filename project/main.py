import streamlit as st
import os

st.set_page_config(page_title="Integrated Bank Tool", layout="centered")
st.title("💼 Bank Statement Utility Suite")

# Sidebar Navigation
choice = st.sidebar.radio("Select Module", ["PDF Converter", "Categorization"])

# Run the PDF Converter
if choice == "PDF Converter":
    st.markdown("### 🏦 Bank PDF Converter")
    with st.spinner("Loading PDF converter..."):
        exec(open("pdf_converter/App.py").read())

    # Provide a button to navigate to Categorization
    if "converted_data" in st.session_state:
        if st.button("➡️ Proceed to Categorization"):
            st.session_state["next_app"] = "Categorization"
            st.experimental_rerun()

# Run the Categorization App
elif choice == "Categorization" or st.session_state.get("next_app") == "Categorization":
    st.markdown("### 🧠 Categorization Tool")
    with st.spinner("Loading Categorization tool..."):
        exec(open("categorizer/App.py").read())

    # Clear redirect trigger
    st.session_state["next_app"] = None
