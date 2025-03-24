import streamlit as st
import sys, os

st.set_page_config(page_title="Integrated Bot", layout="wide")

# Import the apps
sys.path.append(os.path.abspath("pdf_app"))
sys.path.append(os.path.abspath("categorization_app"))

import App as pdf_app
import categorizer as categorizer_app

# Custom Styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1f1c2c, #928DAB);
        color: #ffffff;
    }

    .main {
        background-color: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(6px);
        border-radius: 12px;
        padding: 2rem;
    }

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
            text-shadow: 0 0 12px #e0aaff, 0 0 4px #b5cb99;
        }
    }

    /* Tabs: same size, cleaner UI */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
        gap: 12px;
        background: transparent;
        border: none;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1;
        text-align: center;
        font-size: 1rem;
        font-weight: 600;
        padding: 0.75rem 1rem;
        background-color: rgba(255, 255, 255, 0.07);
        color: #bbbbbb;
        border: none;
        border-radius: 12px;
        transition: all 0.3s ease;
        max-width: 200px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.15);
        color: #ffffff;
    }

    .stTabs [aria-selected="true"] {
        background-color: #6a4c93;
        color: #ffffff;
        font-weight: 700;
    }

    section[data-testid="stTabs"] > div:first-child {
        border-bottom: none !important;
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
