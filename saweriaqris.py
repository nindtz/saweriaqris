import requests
from bs4 import BeautifulSoup
import json

# Created from Playwright to BS4
# nindtz 2024


BASE_URL = 'https://backend.saweria.co'
FRONT_URL = 'https://saweria.co'



def insert_plus_in_email(email, insert_str):
    return email.replace("@", f"+{insert_str}@", 1)


def create_payment_string(saweria_username, amount, author, email, pesan):
    if not saweria_username or not amount or not author or not email or not pesan:
        raise ValueError("Parameter is missing!")
    if amount < 10000:
        # 10000 is needed so you can have webhook post request
        raise ValueError("Minimum amount is 10000")
    
    print(f"Loading {FRONT_URL}/{saweria_username}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15'
    }
    response = requests.get(f"{FRONT_URL}/{saweria_username}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    next_data_script = soup.find(id='__NEXT_DATA__')
    if not next_data_script:
        print("Saweria account not found")
        raise ValueError("Saweria account not found")
    
    next_data = json.loads(next_data_script.text)
    user_id = next_data.get("props", {}).get("pageProps", {}).get("data", {}).get("id")
    if not user_id:
        print("Saweria account not found")
        raise ValueError("Saweria account not found")
    
    payload = {
        "agree": True,
        "notUnderage": True,
        "message": pesan,
        "amount": int(amount),
        "payment_type": "qris",
        "vote": "",
        "currency": "IDR",
        "customer_info": {
            "first_name": "",
            "email": insert_plus_in_email(email, author),
            "phone": ""
        }
    }
    ps = requests.post(f"{BASE_URL}/donations/{user_id}", json=payload)
    pc = ps.json()["data"]
    
    return {
        "author": author,
        "trx_id": pc["id"],
        "message": pesan,
        "amount": amount,
        "invoice_url": f"https://saweria.co/qris/{pc['id']}",
        "qr_string": pc["qr_string"],
        "created_at": pc["created_at"],
        "amount_raw": pc["amount_raw"],
        "saweria_username": saweria_username,
        "user_id": user_id
    }

def create_payment_qr(saweria_username, amount, author, email, pesan):
    payment_details = create_payment_string(saweria_username, amount, author, email, pesan)  
    return [payment_details["qr_string"], payment_details["trx_id"]]

# print(create_payment_string("nindtz", 10000, "Budi", "budi@saweria.co, "coba ya"))
# print(create_payment_qr("nindtz", 10000, "Budi", "budi@saweria.co", "coba ya"))
