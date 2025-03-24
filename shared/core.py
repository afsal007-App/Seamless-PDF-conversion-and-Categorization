import pandas as pd
import os
import re

# Master categorization sheet URL
MASTER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1I_Fz3slHP1mnfsKKgAFl54tKvqlo65Ug/export?format=xlsx"

# Output CSV path for converted statement
OUTPUT_FILE_PATH = "shared/outputs/converted_output.csv"

# -------------------------------------
# PDF Conversion Logic
# -------------------------------------

def save_converted_df(df, output_path=OUTPUT_FILE_PATH):
    """Save the DataFrame from PDF conversion to a fixed CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

def get_converted_file():
    """Return path to the converted CSV file if it exists."""
    return OUTPUT_FILE_PATH if os.path.exists(OUTPUT_FILE_PATH) else None

# -------------------------------------
# Categorization Logic
# -------------------------------------

def clean_text(text):
    """Standardize text for keyword matching."""
    return re.sub(r'\s+', ' ', str(text).lower().replace('–', '-').replace('—', '-')).strip()

def load_master_file():
    """Download and clean the master categorization sheet."""
    try:
        df = pd.read_excel(MASTER_SHEET_URL)
        df['Key Word'] = df['Key Word'].astype(str).apply(clean_text)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to load master file: {e}")

def find_description_column(columns):
    """Detect likely description column from a list of columns."""
    possible = ['description', 'details', 'narration', 'particulars', 'transaction details', 'remarks']
    return next((col for col in columns if any(name in col.lower() for name in possible)), None)

def categorize_description(description, master_df):
    """Return category for a given description using the master sheet."""
    cleaned = clean_text(description)
    for _, row in master_df.iterrows():
        if row['Key Word'] and row['Key Word'] in cleaned:
            return row['Category']
    return 'Uncategorized'

def categorize_statement(statement_df, master_df):
    """Categorize an entire statement DataFrame."""
    desc_col = find_description_column(statement_df.columns)
    if not desc_col:
        raise ValueError("No description column found in uploaded statement.")
    statement_df['Categorization'] = statement_df[desc_col].apply(lambda x: categorize_description(x, master_df))
    return statement_df

