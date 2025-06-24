import re

# Step 5: Build a row for Xoro Sales Order Import Template
def build_xoro_row(order_data, line_item, item_mapping_df, store_mapping_df, template_columns):
    print(f"DEBUG: order_data['metadata'] = {order_data['metadata']}")
    from mapper import map_item_number, map_store_info

    # Robustly extract store number from metadata or line_item
    store_number = order_data['metadata'].get('store_number')
    if not store_number:
        # Try to extract from any metadata value that looks like a 5-digit number
        for v in order_data['metadata'].values():
            if isinstance(v, str) and v.strip().isdigit() and len(v.strip()) == 5:
                store_number = v.strip()
                break
    if not store_number:
        # Try to parse from a string like 'Store No: 10370'
        for v in order_data['metadata'].values():
            if isinstance(v, str) and 'Store No' in v:
                parts = v.split(':')
                if len(parts) > 1 and parts[1].strip().isdigit():
                    store_number = parts[1].strip()
                    break
    if not store_number:
        # Try to match against strings like 'Store #10337' or 'WHOLE FOODS #10337 BLITHEDALE'
        for v in order_data['metadata'].values():
            if isinstance(v, str):
                regex_match = re.search(r"#(\\d{5})", v)
                if regex_match:
                    store_number = regex_match.group(1)
                    break
    if not store_number:
        # Fallback: try to parse from line_item if present
        store_number = line_item.get('store_no', '').strip()

    # Ensure store_number is a stripped string for robust matching
    if store_number:
        store_number = str(store_number).strip()
    store_mapping_df['StoreNo'] = store_mapping_df['StoreNo'].astype(str).str.strip()
    print(f"DEBUG: Final extracted store_number: '{store_number}' (type: {type(store_number)})")
    print(f"DEBUG: store_mapping_df['StoreNo'] values: {store_mapping_df['StoreNo'].tolist()}")

    # Map store info
    customer_id, account_number, ship_to_name = map_store_info(store_number, store_mapping_df)
    # Get company name for CustomerName
    company_name = None
    match = store_mapping_df[store_mapping_df['StoreNo'] == store_number]
    print(f"DEBUG: store_number={store_number}, match_found={not match.empty}")
    if not match.empty:
        company_name = match.iloc[0]['CompanyName']
        print(f"DEBUG: Final company_name={company_name}")

    print('DEBUG: store_mapping_df.head() =')
    print(store_mapping_df.head())
    print(f'DEBUG: store_number being looked up: {store_number}')

    # Map item number
    # xoro_item_no = map_item_number(line_item['item_no'], item_mapping_df)
    xoro_item_no = map_item_number(line_item['item_no'], item_mapping_df, default_xoro_item_no="Invalid Item")
    # Build row dict
    row = {col: '' for col in template_columns}
    # Robustly extract order date
    order_date = order_data['metadata'].get('order_date', '')
    if not order_date:
        # Try to find a date in any metadata value (format: YYYY-MM-DD or MM/DD/YYYY)
        for v in order_data['metadata'].values():
            if isinstance(v, str):
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', v)
                if date_match:
                    order_date = date_match.group(1)
                    break
                date_match = re.search(r'(\d{2}/\d{2}/\d{4})', v)
                if date_match:
                    order_date = date_match.group(1)
                    break
    row['**DateToBeShipped'] = order_data['metadata'].get('ship_date', '')
    row['**OrderDate'] = order_date
    row['**ItemNumber'] = xoro_item_no
    row['ItemNotes'] = line_item['item_no'] + " " + line_item.get('description', '')
    row['**UnitPrice'] = line_item.get('cost', '')
    qty_raw = line_item.get('qty', '')
    qty_match = re.match(r"(\d+)", qty_raw)
    row['**Qty'] = qty_match.group(1) if qty_match else qty_raw
    row['**CurrencyCode'] = 'USD'
    row['**ExchangeRate'] = 0
    row['**CustomerName'] = company_name if company_name else ''
    row['**SaleStoreName'] = 'IDI - Richmond'
    row['StoreName'] = 'IDI - Richmond'
    order_number = order_data['metadata'].get('order_number', '')
    # Set **ThirdPartyRefNo for every row
    row['ThirdPartyRefNo'] = order_number
    row['RefNo'] = order_number
    row['CustomerPO'] = order_number
    row['SalesRepId'] = 'Office'
    # row['Description'] = line_item.get('description', '')
    row['CustomFieldD1'] = line_item.get('cost', '')
    return row

# Step 7: Write final DataFrame to Xoro-compatible CSV
def save_to_csv(xoro_rows, output_path):
    """Save list of dicts to CSV with correct headers"""
    import pandas as pd
    df = pd.DataFrame(xoro_rows)
    df.to_csv(output_path, index=False)
