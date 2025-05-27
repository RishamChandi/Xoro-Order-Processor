# Step 2: Load item mapping and store mapping from Excel/CSV files
import pandas as pd

def load_mappings(item_file, store_file):
    """Return item_mapping_df and store_mapping_df as DataFrames"""
    item_mapping_df = pd.read_excel(item_file)
    store_mapping_df = pd.read_excel(store_file)
    return item_mapping_df, store_mapping_df

# Step 3: Match item number from Whole Foods to internal Xoro item #
def map_item_number(whole_foods_item_no, item_mapping_df):
    """Return Xoro item number for a given WF item number (string)"""
    # Assume item_mapping_df has columns: 'WF_ItemNo', 'Xoro_ItemNo'
    match = item_mapping_df[item_mapping_df['WF_ItemNo'].astype(str) == str(whole_foods_item_no)]
    if not match.empty:
        return match.iloc[0]['Xoro_ItemNo']
    return None

# Step 4: Match store number to Xoro customer info
def map_store_info(store_number, store_mapping_df):
    """Return customer_id, account_number, and ship_to_name for a given store number (string)"""
    # Assume store_mapping_df has columns: 'StoreNo', 'CustomerId', 'AccountNumber', 'CompanyName', 'ShipToCompanyName'
    match = store_mapping_df[store_mapping_df['StoreNo'].astype(str) == str(store_number)]
    if not match.empty:
        row = match.iloc[0]
        return row['CustomerId'], row['AccountNumber'], row['ShipToCompanyName']
    return None, None, None
