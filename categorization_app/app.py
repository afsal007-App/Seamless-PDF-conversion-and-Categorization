import streamlit as st
import pandas as pd
import re
from io import BytesIO
import zipfile
import uuid

# ✅ Master categorization file URL
MASTER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1I_Fz3slHP1mnfsKKgAFl54tKvqlo65Ug/export?format=xlsx"

# 🎨 Updated CSS for improved design and hiding the GitHub icon
st.markdown("""
    <style>
    [data-testid="stToolbar"] {
        visibility: hidden !important;
    }

    body {
        background: linear-gradient(135deg, #141e30, #243b55);
        color: #e0e0e0;
        font-size: 12px;
    }

    .center-title {
        text-align: center;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 15px;
        color: #f1c40f;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.4);
        animation: fadeIn 1s ease-in-out;
    }

    h2, h3, .stSubheader {
        font-size: 16px !important;
        font-weight: 600;
        margin-bottom: 10px;
        color: #f39c12;
        animation: slideIn 0.7s ease forwards;
    }

    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 0.5s ease;
    }

    .stButton button, .stDownloadButton button {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: white;
        font-weight: bold;
        border-radius: 25px;
        padding: 6px 16px;
        font-size: 11px;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton button:hover, .stDownloadButton button:hover {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        transform: scale(1.05);
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.7);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .watermark {
        position: fixed;
        bottom: 5px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 11px;
        font-style: italic;
        color: rgba(200, 200, 200, 0.7);
        pointer-events: none;
        animation: fadeIn 2s ease;
    }
    </style>

    <div class="watermark">© 2025 Afsal. All Rights Reserved.</div>
""", unsafe_allow_html=True)

# ✅ Initialize session state variables
if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = str(uuid.uuid4())  # Unique key for file uploader

# 🔄 Reset Function
def reset_app():
    """Resets the session state and clears uploaded files."""
    st.session_state["uploader_key"] = str(uuid.uuid4())  # Generate new key to reset uploader
    st.rerun()

def load_master_file():
    """Load and clean the master categorization file."""
    try:
        df = pd.read_excel(MASTER_SHEET_URL)
        df['Key Word'] = df['Key Word'].astype(str).apply(clean_text)
        return df
    except Exception as e:
        st.error(f"⚠️ Error loading master file: {e}")
        return pd.DataFrame()

def clean_text(text):
    """Standardize text for matching."""
    return re.sub(r'\s+', ' ', str(text).lower().replace('–', '-').replace('—', '-')).strip()

def find_description_column(columns):
    """Identify the description column."""
    possible = ['description', 'details', 'narration', 'particulars', 'transaction details', 'remarks']
    return next((col for col in columns if any(name in col.lower() for name in possible)), None)

def categorize_description(description, master_df):
    """Assign categories based on keywords."""
    cleaned = clean_text(description)
    for _, row in master_df.iterrows():
        if row['Key Word'] and row['Key Word'] in cleaned:
            return row['Category']
    return 'Uncategorized'

def categorize_statement(statement_df, master_df, desc_col):
    """Categorize the entire statement."""
    statement_df['Categorization'] = statement_df[desc_col].apply(lambda x: categorize_description(x, master_df))
    return statement_df

# 🌐 Main Interface
st.markdown('<h1 class="center-title">🤖 Categorization Bot</h1>', unsafe_allow_html=True)

# 🔄 Reset Button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Reset"):
        reset_app()

# 📂 File Upload with dynamic key to reset uploader
uploaded_files = st.file_uploader(
    "📂 Upload Statement Files (Excel or CSV)",
    type=["xlsx", "csv"],
    accept_multiple_files=True,
    key=st.session_state["uploader_key"]
)

if uploaded_files:
    with st.spinner('🚀 Loading master file...'):
        master_df = load_master_file()

    if master_df.empty:
        st.error("⚠️ Could not load the master file.")
    else:
        categorized_files = []
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
                categorized_files.append((file.name, buffer))

                st.download_button(
                    label=f"📥 Download {file.name}",
                    data=buffer,
                    file_name=f"Categorized_{file.name}",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error(f"⚠️ No description column found in {file.name}.")

        # 📦 Download All as ZIP
        if categorized_files:
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for fname, data in categorized_files:
                    zipf.writestr(f"Categorized_{fname}", data.getvalue())
            zip_buffer.seek(0)

            st.download_button(
                label="📦 Download All Categorized Files as ZIP",
                data=zip_buffer,
                file_name="Categorized_Files.zip",
                mime="application/zip"
            )
else:
    st.info("👆 Upload files to begin.")

