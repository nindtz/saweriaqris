from bs4 import BeautifulSoup
import json
import httpx

# Created from Playwright to BS4
# nindtz 2024


BACKEND = 'https://backend.saweria.co'
FRONTEND = 'https://saweria.co'

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15'
        }


def insert_plus_in_email(email, insert_str):
    return email.replace("@", f"+{insert_str}@", 1)


import httpx

def paid_status(transaction_id: str) -> bool:
    """
    Check if a Saweria transaction is paid or not from transaction_id.

    Args:
        transaction_id (str): String from output of create_payment

    Returns:
        bool: True if paid, False if not paid.
    """
    with httpx.Client(http2=True, headers=headers, timeout=2) as client:
        resp = client.get(f"{BACKEND}/donations/qris/{transaction_id}")
        if resp.status_code // 100 != 2:
            raise ValueError("Transaction ID is not found!")

        data = resp.json().get("data", {})
        # If qr_string still exists, payment is pending/unpaid
        return data.get("qr_string", "") == ""


def create_payment_string(saweria_username, amount, sender, email, pesan):
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
    if not all([saweria_username, amount, sender, email, pesan]):
        raise ValueError("Parameter is missing!")
    if amount < 10000:
        raise ValueError("Minimum amount is 10000")

    print(f"Loading {FRONTEND}/{saweria_username}")

    # httpx session (faster & supports HTTP/2)
    with httpx.Client(http2=True, headers=headers, timeout=2) as client:
        resp = client.get(f"{FRONTEND}/{saweria_username}")
        soup = BeautifulSoup(resp.text, "html.parser")

        next_data_script = soup.find(id="__NEXT_DATA__")
        if not next_data_script:
            raise ValueError("Saweria account not found")

        next_data = json.loads(next_data_script.text)
        user_id = (
            next_data.get("props", {})
            .get("pageProps", {})
            .get("data", {})
            .get("id")
        )

        if not user_id:
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
                "email": email,
                "phone": ""
            }
        }

        ps = client.post(f"{BACKEND}/donations/{user_id}", json=payload)
        ps.raise_for_status()
        return ps.json()["data"]

def create_payment_qr(saweria_username: str, amount: int, sender: str, email: str, pesan: str) -> list:
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

# print(create_payment_qr("nindtz", 10000, "Budi", "budi@saweria.co", "coba ya"))
# print(paid_status("00000000-0000-0000-0000-000000000000")) # output True if paid, False if not paid and Error if anything else

