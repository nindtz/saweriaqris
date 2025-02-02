## Saweria QRIS code generator

[![PyPI - Version](https://img.shields.io/pypi/v/saweriaqris)](http://pypi.org/project/saweriaqris/)
[![PyPI Downloads](https://static.pepy.tech/badge/saweriaqris)](https://pepy.tech/projects/saweriaqris)
[![Discord](https://img.shields.io/discord/878859506405228574)](https://discord.gg/GzjyMZnpb7)
[![GitHub License](https://img.shields.io/github/license/nindtz/saweriaqris)](https://mit-license.org/)

> [!CAUTION]
> Using any kind of automation programs on your account can result in your account getting permanently banned by Saweria. Use at your own risk.

### Installation

`$ pip install saweriaqris` Install this package <br>

## Usage:

use this within your code
example below

creating a code

```python
from saweriaqris import create_payment_qr, paid_status

myqr = create_payment_qr("nindtz", 10000, "Budi", "budi@saweria.co", "Semangat!")
qrcode = myqr[0]
transaction_id = myqr[1]

# Just feed the qrcode to your favourite qr code generator
# transaction_id for matching purpose to your webhook calls
```

checking transaction status

```python
from saweriaqris import create_payment_qr, paid_status

is_paid = paid_status(transaction_id)

# is_paid is bool value
```

<br>

> [!Tip]
> Best Practice: You are supposed to use Saweria's Webhook Integration to get realtime payment notification to your API.

1. Set your Saweria Integration to point to your API (found in Integrations -> Webhook)
2. You issue a payment code to your client.
3. After successful payment, Saweria will do POST request (Webhook) to your API.
   Below example POST from Saweria Webhook:

```json
{
	"version": "2022.01",
	"created_at": "2021-01-01T12:00:00+00:00",
	"id": "00000000-0000-0000-0000-000000000000",
	"type": "donation",
	"amount_raw": 69420,
	"cut": 3471,
	"donator_name": "Someguy",
	"donator_email": "someguy@example.com",
	"donator_is_user": false,
	"message": "THIS IS A FAKE MESSAGE! HAVE A GOOD ONE",
	"etc": {
		"amount_to_display": 69420
	}
}
```

4. Parse the JSON from the POST and challenge the id given from Saweria Webhook with the paid_status function.
5. Only after it returns True, then you can update accordingly.

## Example use case:

Discord bot Donate QRIS<br>
<img width="401" alt="image" src="https://github.com/user-attachments/assets/f607cc45-5836-4c19-abe2-b2b1f8393d1b" />

#### Thank you
