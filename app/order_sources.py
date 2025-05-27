from main import extract_order_data as extract_order_data_wholefoods
import os

def extract_order_data_unfi(path):
    # TODO: Implement UNFI parser
    return {"metadata": {}, "line_items": []}

def extract_order_data_tkmaxx(path):
    # TODO: Implement TK Maxx parser
    return {"metadata": {}, "line_items": []}

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ORDER_SOURCES = {
    "Whole Foods": {
        "parser": extract_order_data_wholefoods,
        "item_mapping": os.path.join(BASE_DIR, "mappings/wholefoods/item_mapping.xlsx"),
        "store_mapping": os.path.join(BASE_DIR, "mappings/wholefoods/store_mapping.xlsx"),
        "file_types": ["html"]
    },
    "UNFI": {
        "parser": extract_order_data_unfi,
        "item_mapping": "mappings/unfi/item_mapping.xlsx",
        "store_mapping": "mappings/unfi/store_mapping.xlsx",
        "file_types": ["csv", "xlsx"]
    },
    "TK Maxx": {
        "parser": extract_order_data_tkmaxx,
        "item_mapping": "mappings/tkmaxx/item_mapping.xlsx",
        "store_mapping": "mappings/tkmaxx/store_mapping.xlsx",
        "file_types": ["csv", "xlsx"]
    },
}