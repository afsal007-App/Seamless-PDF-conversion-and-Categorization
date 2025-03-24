import streamlit as st
import sys, os

# ✅ Set wide layout and page title
st.set_page_config(page_title="Financial Toolkit", layout="wide")

# ✅ Add app paths
sys.path.append(os.path.abspath("pdf_app"))
sys.path.append(os.path.abspath("categorization_app"))

# ✅ Import PDF and Categorization apps
import App as pdf_app
import app as categorizer_app

# ✅ Custom title UI
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

# ✅ Determine which tab should open by default
default_tab = "📄 PDF to CSV Converter"
if st.session_state.get("active_tab") == "Categorizer":
    default_tab = "🧠 Categorizer"
    st.session_state["active_tab"] = None  # Reset flag

# ✅ Define tabs
tab1, tab2 = st.tabs(["📄 PDF to CSV Converter", "🧠 Categorizer"])

# ✅ Show each app inside respective tab
with tab1:
    if default_tab == "📄 PDF to CSV Converter":
        pdf_app.run()
with tab2:
    if default_tab == "🧠 Categorizer":
        categorizer_app.run()
