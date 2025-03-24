# ✅ Updated App.py (PDF to CSV Converter with Smooth Auto Push to Categorizer Tab)
import streamlit as st
import pandas as pd
from shared.core import save_converted_df
from io import BytesIO
import uuid
# Import bank modules
import Rak_Bank
import al_jazira_bank
import emirates_islamic_bank
import fab_bank
import Wio_bank
import adib_bank
import mashreq
import adcb

def run():
    bank_modules = {
        "🏦 RAK Bank": Rak_Bank,
        "🏢 Emirates Islamic Bank": emirates_islamic_bank,
        "🏬 FAB Bank": fab_bank,
        "🏛️ WIO Bank": Wio_bank,
        "🏤 ADIB Bank": adib_bank,
        "🏤 Mashreq Neo Bank": mashreq,
        "🏤 ADCB Bank": adcb
    }
    
    # Enhanced reset function to clear session state
    def reset_app():
        # First explicitly remove all session state variables
        for key in list(st.session_state.keys()):
            del st.session_state[key]
                
        # Reinitialize fresh uploader key if needed
        st.session_state["uploader_key"] = str(uuid.uuid4())
        
        # Clear any converted dataframe
        st.session_state["converted_df_for_categorization"] = None
        
        # Flag to indicate reset was performed
        st.session_state["just_reset"] = True
        
        # Force the app to rerun after clearing state
        st.rerun()
    
    # Check if we just performed a reset
    just_reset = st.session_state.get("just_reset", False)
    if just_reset:
        # Clear the reset flag
        st.session_state["just_reset"] = False
        # Create auto-dismissing message with HTML/JavaScript
        st.markdown("""
            <div id="success-message" style="
                padding: 1rem; 
                background-color: #d4edda; 
                color: #155724; 
                border-radius: 0.25rem; 
                margin-bottom: 1rem;
                animation: fadeOut 1s ease-in 3s forwards;">
                ✅ App has been reset successfully!
            </div>
            <style>
                @keyframes fadeOut {
                    from { opacity: 1; }
                    to { opacity: 0; display: none; }
                }
            </style>
            <script>
                setTimeout(function() {
                    document.getElementById('success-message').style.display = 'none';
                }, 4000); // 4 seconds total (3s delay + 1s fade)
            </script>
        """, unsafe_allow_html=True)
        
    # UI Styling
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
            from { text-shadow: 0 0 5px #886dc7, 0 0 10px #cdb4d4; }
            to { text-shadow: 0 0 12px #EBE3D5, 0 0 2px #B5CB99; }
        }
        div.stButton > button {
            background-color: #444 !important;
            color: white !important;
            padding: 10px 24px;
            border-radius: 8px;
            font-size: 16px;
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<div class='title'>Bank Statement PDF Extractor</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>Convert your bank PDFs into clean, usable data \U0001F4C4 ➡️ \U0001F4C8</div>", unsafe_allow_html=True)
    st.markdown('<div class="dropdown-label"> Select Your Bank</div>', unsafe_allow_html=True)
    selected_bank = st.selectbox("", list(bank_modules.keys()))
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Skip processing if we just reset
    if not just_reset and selected_bank:
        df = bank_modules[selected_bank].run()
        if isinstance(df, pd.DataFrame):
            save_converted_df(df)
            st.success("✅ PDF converted and saved as CSV successfully!")
            st.dataframe(df.head())
            # ✅ Auto-push to Categorizer Tab with smooth toast & JS redirect
            st.toast("✅ PDF processed! Redirecting to Categorizer...", icon="🚀")
            st.session_state["converted_df_for_categorization"] = df
            st.session_state["active_tab"] = "Categorizer"
            st.markdown("""
                <script>
                    setTimeout(function() {
                        window.location.reload();
                    }, 500);
                </script>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No data returned from the selected bank's parser.")
    
    # Reset button to clear the app
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Reset / Clear App", key="uploader_key"):
            reset_app()
