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

def main():
    # ==== Page Config ====
    st.markdown("<h1 style='text-align:center;'>Bank Statement PDF Extractor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Convert your bank PDFs into clean, usable data 📄 ➡️ 📊</p>", unsafe_allow_html=True)

    # ==== Bank Selection ====
    selected_bank = st.selectbox("Select Your Bank", list(bank_modules.keys()))

    # ==== Process ====
    if selected_bank:
        df = bank_modules[selected_bank].run()
        if df is not None:
            st.session_state["converted_data"] = df

# Call it for direct runs
if __name__ == "__main__":
    main()
