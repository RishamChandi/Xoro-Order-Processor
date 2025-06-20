import streamlit as st
import tempfile
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from generator import build_xoro_row, save_to_csv
from mapper import load_mappings
from app.order_sources import ORDER_SOURCES

# Step 1: Import necessary libraries
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# TEMPLATE_FILE = os.path.join(BASE_DIR, "templates/base_xoro_template.csv")
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_FILE = os.path.join(BASE_DIR, "templates/base_xoro_template.csv")

st.set_page_config(page_title="Xoro Sales Order Transformer", layout="centered")
st.title("Xoro Sales Order Transformer")
st.markdown("""
Transform sales order files from **Whole Foods**, **UNFI**, or **TK Maxx** into Xoro import CSVs.  
Select your order source, upload your file, and download the ready-to-import CSV.
""")

source = st.radio(
    "Select Order Source:",
    list(ORDER_SOURCES.keys()),
    horizontal=True
)
config = ORDER_SOURCES[source]
# ...existing code...
uploaded_files = st.file_uploader(
    f"Upload {source} Order File(s)", 
    type=config["file_types"], 
    accept_multiple_files=True
)

if uploaded_files:
    all_xoro_rows = []
    temp_paths = []
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{config['file_types'][0]}") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
            temp_paths.append(tmp_path)
        order_data = config["parser"](tmp_path)
        item_mapping_df, store_mapping_df = load_mappings(config["item_mapping"], config["store_mapping"])
        with open(TEMPLATE_FILE, encoding="utf-8") as f:
            template_columns = f.readline().strip().split(',')
        for line_item in order_data['line_items']:
            row = build_xoro_row(order_data, line_item, item_mapping_df, store_mapping_df, template_columns)
            all_xoro_rows.append(row)
    csv_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    save_to_csv(all_xoro_rows, csv_temp.name)
    csv_temp.close()
    with open(csv_temp.name, "rb") as f:
        st.download_button(
            label="Download Xoro CSV",
            data=f,
            file_name="xoro_sales_order_import.csv",
            mime="text/csv"
        )
    for tmp_path in temp_paths:
        os.remove(tmp_path)
    os.remove(csv_temp.name)
# ...existing code...
# uploaded_file = st.file_uploader(f"Upload {source} Order File", type=config["file_types"])

