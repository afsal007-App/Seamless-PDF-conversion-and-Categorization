import streamlit as st

st.title("Financial Tools Suite")

option = st.selectbox("Choose a tool:", ["PDF to Excel", "Transaction Categorizer"])

if option == "PDF to Excel":
    st.switch_page("pdf_app/App.py")
elif option == "Transaction Categorizer":
    st.switch_page("categorization_app/app.py")
