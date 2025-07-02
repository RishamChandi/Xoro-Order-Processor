from bs4 import BeautifulSoup
import re
import pandas as pd

def transform_unfi_west_order(html_path, store_mapping_path, template_path):
    """
    Transforms UNFI West order HTML file into Xoro sales order template.
    Returns a DataFrame representing the transformed order.
    """
    # Load store mapping
    store_mapping = pd.read_excel(store_mapping_path)

    # Load Xoro template
    xoro_template = pd.read_csv(template_path)

    # Parse HTML file
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Extract metadata
    metadata = {}
    customer_name_tag = soup.find(string=re.compile(r"UNFI -"))
    if customer_name_tag:
        metadata["customer_name"] = customer_name_tag.strip()

    order_date_tag = soup.find(string=re.compile(r"\d{2}/\d{2}/\d{2}"))
    if order_date_tag:
        metadata["order_date"] = order_date_tag.strip()

    # Map customer name using store_mapping
    xoro_customer_name = store_mapping.loc[store_mapping["UNFI Customer Name"] == metadata["customer_name"], "Xoro Customer Name"].values
    metadata["xoro_customer_name"] = xoro_customer_name[0] if len(xoro_customer_name) > 0 else "Unknown Customer"

    # Extract line items
    line_items = []
    table = soup.find("table")
    if table:
        rows = table.find_all("tr")[1:]  # Skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 7:
                line_item = {
                    "line": cols[0].get_text(strip=True),
                    "item_no": cols[1].get_text(strip=True),
                    "qty": cols[2].get_text(strip=True),
                    "description": cols[3].get_text(strip=True),
                    "size": cols[4].get_text(strip=True),
                    "cost": cols[5].get_text(strip=True),
                    "upc": cols[6].get_text(strip=True),
                }
                line_items.append(line_item)

    # Populate Xoro template
    for idx, item in enumerate(line_items):
        xoro_template.loc[idx, "CustomerName"] = metadata["xoro_customer_name"]
        xoro_template.loc[idx, "OrderDate"] = metadata["order_date"]
        xoro_template.loc[idx, "ItemCode"] = item["item_no"]
        xoro_template.loc[idx, "Quantity"] = item["qty"]
        xoro_template.loc[idx, "Description"] = item["description"]

    return xoro_template