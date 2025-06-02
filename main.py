# Step 1: Load Whole Foods HTML order file and extract order information
from bs4 import BeautifulSoup
import re

def extract_order_data(html_path):
    """
    Extracts order metadata and line items from a Whole Foods Market order HTML file.
    Returns a dict with metadata and a list of line items.
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # --- Extract order metadata (existing logic) ---
    metadata = {}
    # Find the order number, order date, etc.
    order_number_tag = soup.find(string=re.compile(r"Order #"))
    if order_number_tag:
        order_number = order_number_tag.split("Order #")[-1].strip()
        metadata["order_number"] = order_number
    order_date_tag = soup.find(string=re.compile(r"Order Date:"))
    if order_date_tag:
        order_date = order_date_tag.split("Order Date:")[-1].strip()
        metadata["order_date"] = order_date

    # --- Fix: Store Number (span over tags) ---
    store_number = None
    texts = list(soup.stripped_strings)
    for i in range(len(texts) - 1):
        combined = f"{texts[i]} {texts[i+1]}"
        match = re.search(r"Store No[:#]?\s*(\d{5})", combined)
        if match:
            store_number = match.group(1)
            break
    metadata["store_number"] = store_number
    print(f"DEBUG: Final extracted store_number in HTML parser: '{store_number}'")
                
    # --- Extract line items ---
    # ...add more metadata extraction as needed...

    # --- Extract line items ---
    line_items = []
    # Find the table with the line items
    # The table has headers: Line, Item No., Qty, Description, Size, Cost, UPC
    table = None
    for t in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in t.find_all("th")]
        if headers[:7] == ["Line", "Item No.", "Qty", "Description", "Size", "Cost", "UPC"]:
            table = t
            break
    if table:
        rows = table.find_all("tr")[1:]  # skip header row
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
    else:
        print("Line items table not found.")

    return {"metadata": metadata, "line_items": line_items}

if __name__ == "__main__":
    html_file = "uploads/WholeFoodsOrder.html"
    # TODO: Add mapping and template logic
    order_metadata, line_items = extract_order_data(html_file)
    print(order_metadata)
    print(line_items)
