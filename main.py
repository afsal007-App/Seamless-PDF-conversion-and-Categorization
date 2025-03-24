import streamlit as st
import sys, os

st.set_page_config(page_title="Integrated Bot", layout="centered")

# Import the apps
sys.path.append(os.path.abspath("pdf_app"))
sys.path.append(os.path.abspath("categorization_app"))

import App as pdf_app
import app as categorizer_app

# Enhanced Styling
st.markdown("""
    <style>
    /* Main Title Styling */
    .title {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 5px #9d4edd, 0 0 10px #c77dff;
        }
        to {
            text-shadow: 0 0 15px #e0aaff, 0 0 5px #b5cb99;
        }
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 3px solid #e0aaff;
        background-color: #f8f7ff;
        padding: 0.5rem 1rem;
        border-radius: 8px 8px 0 0;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 1rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        color: #6c757d;
        border: 2px solid transparent;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #3f3d56;
        background-color: #e0aaff33;
    }

    .stTabs [aria-selected="true"] {
        color: #5e60ce;
        background-color: #edf2fb;
        border-bottom: 2px solid #5e60ce;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>Integrated Bot</div>", unsafe_allow_html=True)

# Tab switch logic
default_tab = "📄 PDF to CSV Converter"
if st.session_state.get("active_tab") == "Categorizer":
    default_tab = "🧠 Categorizer"
    st.session_state["active_tab"] = None

# Tabs
tab1, tab2 = st.tabs(["📄 PDF to CSV Converter", "🧠 Categorizer"])

with tab1:
    pdf_app.run()

with tab2:
    categorizer_app.run()
