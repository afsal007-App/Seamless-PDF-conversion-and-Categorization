# ✅ Updated App.py (PDF to CSV Converter with Smooth Auto Push to Categorizer Tab)

import streamlit as st
import pandas as pd
from shared.core import save_converted_df
from io import BytesIO

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
        "🏚️ ADIB Bank": adib_bank,
        "🏠 Mashreq Neo Bank": mashreq,
        "🏤 ADCB Bank": adcb
    }

    # UI Styling
    st.markdown("""
        <style>
        .title {
            font-size: 2rem;
            font-weight: 800;
            text-align: center;
            padding-top: 0.5rem;
            background: linear-gradient(90deg, #00dbde, #fc00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            
        }

        .subtext {
            text-align: center;
            font-size: 0.9rem;
            font-weight: 400;
            color: #bbbbbb;
            margin-top: -8px;
            margin-bottom: 25px;
        }

        .dropdown-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #e0d3f5;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }

        hr {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin: 30px 0;
        }

        /* Toast & button tweaks */
        .element-container button {
            font-size: 0.8rem !important;
        }

        .stAlert {
            font-size: 0.85rem;
        }

        .stDataFrame {
            font-size: 0.75rem;
        }

        
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>Bank Statement PDF Extractor</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtext'>Convert your bank PDFs into clean, usable data \U0001F4C4 ➡️ \U0001F4C8</div>", unsafe_allow_html=True)

    st.markdown('<div class="dropdown-label"> Select Your Bank</div>', unsafe_allow_html=True)
    selected_bank = st.selectbox("", list(bank_modules.keys()))
    st.markdown("<hr>", unsafe_allow_html=True)

    if selected_bank:
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
            st.warning("⚠️ No pdf found/Data found")
