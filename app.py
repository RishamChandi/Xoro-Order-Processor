import streamlit as st
import pandas as pd
import tempfile
import os

from generator import build_xoro_row, save_to_csv
from mapper import load_mappings

# File paths (adjust if needed)
ITEM_MAPPING_FILE = "mappings/item_mapping.xlsx"
STORE_MAPPING_FILE = "mappings/store_mapping.xlsx"
TEMPLATE_FILE = "templates/base_xoro_template.csv"

from main import extract_order_data

st.title("Whole Foods to Xoro CSV Converter")

uploaded_file = st.file_uploader("Upload Whole Foods HTML Order File", type=["html"])

if uploaded_file is not None:
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Process the file
    order_data = extract_order_data(tmp_path)
    item_mapping_df, store_mapping_df = load_mappings(ITEM_MAPPING_FILE, STORE_MAPPING_FILE)
    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        template_columns = f.readline().strip().split(',')

    xoro_rows = []
    for line_item in order_data['line_items']:
        row = build_xoro_row(order_data, line_item, item_mapping_df, store_mapping_df, template_columns)
        xoro_rows.append(row)

    # Save to CSV in temp file
    csv_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    save_to_csv(xoro_rows, csv_temp.name)
    csv_temp.close()

    # Provide download link
    with open(csv_temp.name, "rb") as f:
        st.download_button(
            label="Download Xoro CSV",
            data=f,
            file_name="xoro_sales_order_import.csv",
            mime="text/csv"
        )

    # Clean up temp files
    os.remove(tmp_path)
    os.remove(csv_temp.name)