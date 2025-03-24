import streamlit as st
import pandas as pd
import uuid
import zipfile
from io import BytesIO
from shared.core import get_converted_file, load_master_file, categorize_statement

st.set_page_config(page_title="Categorization Bot", layout="wide")

# UI Setup
st.markdown("""
    <style>
    body { background: linear-gradient(135deg, #141e30, #243b55); color: #e0e0e0; }
    .center-title {
        text-align: center;
        font-size: 28px;
        font-weight: 700;
        color: #f1c40f;
        margin-bottom: 10px;
    }
    .watermark {
        position: fixed;
        bottom: 5px;
        left: 0; right: 0;
        text-align: center;
        font-size: 11px;
        font-style: italic;
        color: rgba(200, 200, 200, 0.7);
        pointer-events: none;
    }
    </style>
    <div class="center-title">🤖 Categorization Bot</div>
    <div class="watermark">© 2025 Afsal. All Rights Reserved.</div>
""", unsafe_allow_html=True)

# Session state
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = str(uuid.uuid4())

def reset_app():
    st.session_state["uploader_key"] = str(uuid.uuid4())
    st.rerun()

# Reset button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Reset"):
        reset_app()

# Check for auto-loaded converted file
converted_file = get_converted_file()
uploaded_files = []

if converted_file:
    st.success("✅ Auto-loaded the converted PDF file.")
    uploaded_files = [converted_file]
else:
    uploaded_files = st.file_uploader(
        "📂 Upload Statement Files (CSV or Excel)",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
        key=st.session_state["uploader_key"]
    )

if uploaded_files:
    try:
        master_df = load_master_file()
    except Exception as e:
        st.error(f"⚠️ Error loading master file: {e}")
        st.stop()

    categorized_files = []

    for file in uploaded_files:
        st.subheader(f"📄 {file.name}")
        try:
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")
            continue

        st.dataframe(df.head())

        try:
            categorized_df = categorize_statement(df, master_df)
            st.success(f"✅ {file.name} categorized successfully!")
            st.dataframe(categorized_df.head())

            buffer = BytesIO()
            categorized_df.to_csv(buffer, index=False)
            buffer.seek(0)
            categorized_files.append((file.name, buffer))

            st.download_button(
                label=f"📥 Download {file.name}",
                data=buffer,
                file_name=f"Categorized_{file.name.replace('.xlsx', '.csv')}",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"❌ Categorization failed: {e}")

    if categorized_files:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for fname, data in categorized_files:
                zipf.writestr(f"Categorized_{fname.replace('.xlsx', '.csv')}", data.getvalue())
        zip_buffer.seek(0)

        st.download_button(
            label="📦 Download All Categorized Files as ZIP",
            data=zip_buffer,
            file_name="Categorized_Files.zip",
            mime="application/zip"
        )
else:
    st.info("👆 Upload a CSV or Excel file to begin.")
