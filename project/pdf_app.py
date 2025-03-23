
import streamlit as st

# ==== Bank Modules ====
import Rak_Bank
import al_jazira_bank
import emirates_islamic_bank
import fab_bank
import Wio_bank

# ==== Bank Mapping ====
bank_modules = {
    "🏦 RAK Bank": Rak_Bank,
    "🏢 Al Jazira Bank": al_jazira_bank,
    "🕌 Emirates Islamic Bank": emirates_islamic_bank,
    "💳 FAB Bank": fab_bank,
    "🧾 WIO Bank": Wio_bank
}

# ==== CSS Styling ====
st.markdown("""
    <style>
    .title {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        padding-top: 1rem;
        background: linear-gradient(90deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s ease-in-out infinite alternate;
    }
    .subtext {
        text-align: center;
        font-size: 1.05rem;
        color: #aaa;
        margin-top: -10px;
        margin-bottom: 30px;
    }
    
    .dropdown-label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #cdb4d4;
        margin-bottom: 12px;
    }
    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 40px 0;
    }
    @keyframes glow {
        from {
            text-shadow: 0 0 05px ##886dc7, 0 0 10px ##cdb4d4;
        }
        to {
            text-shadow: 0 0 12px #EBE3D5, 0 0 2px #B5CB99;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ==== Header ====
st.markdown("<div class='title'>Bank Statement PDF Extractor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Convert your bank PDFs into clean, usable data 📄 ➡️ 📊</div>", unsafe_allow_html=True)

# ==== Glass Dropdown Section ====
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="dropdown-label"> Select Your Bank</div>', unsafe_allow_html=True)
selected_bank = st.selectbox("", list(bank_modules.keys()))
st.markdown('</div>', unsafe_allow_html=True)

# ==== Divider ====
st.markdown("<hr>", unsafe_allow_html=True)

# ==== Launch Selected Bank Processor ====
if selected_bank:
    bank_modules[selected_bank].run()



def run_app():
    # Paste your entire existing code here inside this function
    # Wrap it within proper indentation
    import streamlit as st

    # --- Your existing code starts here ---
    ...
    ...
    if selected_bank:
        df = bank_modules[selected_bank].run()
        if df is not None:
            st.session_state["converted_data"] = df
# --- End of function ---

if __name__ == "__main__":
    run_app()
