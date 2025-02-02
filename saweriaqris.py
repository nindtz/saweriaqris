import requests
from bs4 import BeautifulSoup
import json

# Created from Playwright to BS4
# nindtz 2024


BACKEND = 'https://backend.saweria.co'
FRONTEND = 'https://saweria.co'

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15'
        }


def insert_plus_in_email(email, insert_str):
    return email.replace("@", f"+{insert_str}@", 1)


def paid_status(transaction_id: str) -> bool:
    """
    Check status of a saweria transaction paid or not from transaction_id.

    Args:
        transaction_id (str): String from output of create_payment

    Returns:
        bool: Returns true if paid anything else is False
    """
    resp = requests.get(f"{BACKEND}/donations/qris/{transaction_id}", headers=headers)    
    if not resp.status_code // 100 == 2:
        raise ValueError("Transaction ID is not found!")
    else:
        data = resp.json()["data"]
        if data["qr_string"] != "":
            return False
        else:
            return True
    

def create_payment_string(saweria_username: str, amount: int, sender: str, email: str, pesan:str) -> dict:
    """
    Outputs a details transaction from variables.

    Args:
        saweria_username (str): The length of the rectangle.
        amount (int): The width of the rectangle.
        sender (str): Name of donor.
        email (str): Email of sender.
        pesan (str): Message to be sent to the creator.

    Returns:
        dict: Transaction details from input variables.
    """
    if not saweria_username or not amount or not sender or not email or not pesan:
        raise ValueError("Parameter is missing!")
    if amount < 10000:
        # 10000 is needed so you can have webhook post request
        raise ValueError("Minimum amount is 10000")
    
    print(f"Loading {FRONTEND}/{saweria_username}")
    
    response = requests.get(f"{FRONTEND}/{saweria_username}", headers=headers)
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
            "first_name": sender,
            "email": insert_plus_in_email(email, sender),
            "phone": ""
        }
    }
    ps = requests.post(f"{BACKEND}/donations/{user_id}", json=payload)
    pc = ps.json()["data"]
    return pc


def create_payment_qr(saweria_username: str, amount: int, sender: str, email: str, pesan: str) -> list[str]:
    """
    Generates a QRIS payment string and a transaction ID.

    Args:
        saweria_username (str): The recipient's Saweria username.
        amount (int): The donation amount in IDR.
        sender (str): The donor's name.
        email (str): The donor's email address.
        pesan (str): A message to be sent to the creator.

    Returns:
        list[str]: A list containing the QRIS payment string and the transaction ID.
    """
    payment_details = create_payment_string(saweria_username, amount, sender, email, pesan)  
    return [payment_details["qr_string"], payment_details["id"]]

# print(create_payment_string("nindtz", 10000, "Budi", "budi@saweria.co", "coba ya")) 
# print(create_payment_qr("nindtz", 10000, "Budi", "budi@saweria.co", "coba ya"))
# print(paid_status("00000000-0000-0000-0000-000000000000")) # output True if paid, False if not paid and Error if anything else