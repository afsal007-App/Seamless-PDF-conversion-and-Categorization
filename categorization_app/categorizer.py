import streamlit as st
import pandas as pd
import re
from io import BytesIO
import zipfile
import uuid
import time

# Master categorization file URL
MASTER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1I_Fz3slHP1mnfsKKgAFl54tKvqlo65Ug/export?format=xlsx"

def run():
    # Custom CSS for styling the app
    st.markdown("""
        <style>
        [data-testid="stToolbar"] { visibility: hidden !important; }

        body {
            background: linear-gradient(135deg, #141e30, #243b55);
            color: #e0e0e0;
            font-size: 12px;
        }

        .center-title {
            font-size: 2rem;
            font-weight: 800;
            text-align: center;
            padding-top: 0.5rem;
            background: linear-gradient(90deg, #00dbde, #fc00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: glow 2s ease-in-out infinite alternate;
        }

        .watermark {
            position: fixed;
            bottom: 2px;
            left: 0; right: 0;
            text-align: center;
            font-size: 11px;
            font-style: italic;
            color: rgba(200, 200, 200, 0.6);
            pointer-events: none;
            animation: fadeIn 2s ease;
        }

        div.stButton > button {
            background-color: #3b3b3b !important;
            color: #ffffff !important;
            padding: 8px 20px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        h1, h2, h3, h4 {
            font-size: 4rem !important;
            font-weight: 600 !important;
            color: #f0f0f0 !important;
        }

        .stAlert {
            font-size: 0.85rem;
        }

        .uploadedFileName, .stFileUploader label {
            font-size: 0.85rem !important;
        }

        .stDownloadButton > button {
            font-size: 0.8rem !important;
            padding: 6px 16px !important;
            border-radius: 6px;
        }

        .stDataFrame {
            font-size: 0.75rem;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        @keyframes glow {
            from { text-shadow: 0 0 5px #886dc7, 0 0 10px #cdb4d4; }
            to   { text-shadow: 0 0 12px #EBE3D5, 0 0 2px #B5CB99; }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to   { opacity: 1; }
        }
        </style>

        <h1 class="center-title">Categorization Bot</h1>
        <div class="watermark">© 2025 Afsal. All Rights Reserved.</div>
    """, unsafe_allow_html=True)

    just_reset = st.session_state.get("just_reset", False)
    if just_reset:
        st.session_state["just_reset"] = False
        st.markdown("""
            <div id="success-message" style="
                padding: 1rem; 
                background-color: #d4edda; 
                color: #155724; 
                border-radius: 0.25rem; 
                margin-bottom: 1rem;
                animation: fadeOut 1s ease-in 1s forwards;">
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
                }, 4000);
            </script>
        """, unsafe_allow_html=True)

    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = str(uuid.uuid4())

    def reset_categorizer():
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["uploader_key"] = str(uuid.uuid4())
        st.session_state["converted_df_for_categorization"] = None
        st.session_state["just_reset"] = True
        st.rerun()

    def clean_text(text):
        return re.sub(r'\s+', ' ', str(text).lower().replace('–', '-').replace('—', '-')).strip()

    def load_master_file():
        try:
            df = pd.read_excel(MASTER_SHEET_URL)
            df['Key Word'] = df['Key Word'].astype(str).apply(clean_text)
            return df
        except Exception as e:
            st.error(f"⚠️ Error loading master file: {e}")
            return pd.DataFrame()

    def find_description_column(columns):
        possible = ['description', 'details', 'narration', 'particulars', 'transaction details', 'remarks']
        return next((col for col in columns if any(name in col.lower() for name in possible)), None)

    def categorize_description(description, master_df):
        cleaned = clean_text(description)
        for _, row in master_df.iterrows():
            if row['Key Word'] and row['Key Word'] in cleaned:
                return row['Category']
        return 'Uncategorized'

    def categorize_statement(statement_df, master_df, desc_col):
        statement_df['Categorization'] = statement_df[desc_col].apply(lambda x: categorize_description(x, master_df))
        return statement_df

    categorized_files = []

    if not just_reset:
        if "converted_df_for_categorization" in st.session_state and st.session_state["converted_df_for_categorization"] is not None:
            st.subheader("📥 Categorize Data from PDF Conversion")
            with st.spinner('🚀 Loading master file...'):
                master_df = load_master_file()

            if not master_df.empty:
                statement_df = st.session_state["converted_df_for_categorization"]
                st.dataframe(statement_df.head(), use_container_width=True)
                desc_col = find_description_column(statement_df.columns)

                if desc_col:
                    categorized = categorize_statement(statement_df, master_df, desc_col)
                    st.success("✅ Data categorized successfully!")
                    st.dataframe(categorized.head(), use_container_width=True)

                    buffer = BytesIO()
                    categorized.to_excel(buffer, index=False)
                    buffer.seek(0)
                    categorized_files.append(("Categorized_PDF_Output.xlsx", buffer))

                    st.download_button(
                        label="📥 Download Categorized Data",
                        data=buffer,
                        file_name="Categorized_PDF_Output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error("⚠️ No description column found for categorization.")
            else:
                st.error("⚠️ Master file could not be loaded.")

    st.markdown("---")
    uploaded_files = st.file_uploader(
        "📂 Upload Statement Files (Excel or CSV)",
        type=["xlsx", "csv"],
        accept_multiple_files=True,
        key=st.session_state["uploader_key"]
    )

    if not just_reset and uploaded_files:
        with st.spinner('🚀 Loading master file...'):
            master_df = load_master_file()

        if master_df.empty:
            st.error("⚠️ Could not load the master file.")
        else:
            st.markdown('## 📑 Uploaded Files Preview & Results')

            for file in uploaded_files:
                st.subheader(f"📄 {file.name}")
                try:
                    statement_df = pd.read_excel(file)
                except Exception:
                    statement_df = pd.read_csv(file)

                st.dataframe(statement_df.head(), use_container_width=True)
                desc_col = find_description_column(statement_df.columns)

                if desc_col:
                    categorized = categorize_statement(statement_df, master_df, desc_col)
                    st.success(f"✅ {file.name} categorized successfully!")
                    st.dataframe(categorized.head(), use_container_width=True)

                    buffer = BytesIO()
                    categorized.to_excel(buffer, index=False)
                    buffer.seek(0)
                    categorized_files.append((f"Categorized_{file.name}", buffer))

                    st.download_button(
                        label=f"📥 Download {file.name}",
                        data=buffer,
                        file_name=f"Categorized_{file.name}",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(f"⚠️ No description column found in {file.name}.")

    if categorized_files:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for fname, data in categorized_files:
                zipf.writestr(fname, data.getvalue())
        zip_buffer.seek(0)

        st.download_button(
            label="📦 Download All Categorized Files as ZIP",
            data=zip_buffer,
            file_name="Categorized_Files.zip",
            mime="application/zip"
        )
    elif not uploaded_files and not just_reset:
        st.info("👆 Upload files to begin.")

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Reset / Clear App"):
            reset_categorizer()

# Run the app
if __name__ == "__main__":
    run()
