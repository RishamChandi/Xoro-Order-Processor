# Step 8: Post CSV or order JSON to Xoro API endpoint
import requests

def upload_order_to_xoro(api_url, order_payload):
    """Send POST request to Xoro ERP"""
    response = requests.post(api_url, json=order_payload)
    return response.status_code, response.text
