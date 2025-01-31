## Saweria QRIS code generator

[![PyPI - Version](https://img.shields.io/pypi/v/saweriaqris)](http://pypi.org/project/saweriaqris/)
[![Discord](https://img.shields.io/discord/878859506405228574)](https://discord.gg/GzjyMZnpb7)
[![GitHub License](https://img.shields.io/github/license/nindtz/saweriaqris)](https://mit-license.org/)

### DISCLAIMER

**use at your own risk**

### Installation

`$ pip install saweriaqris` Install this package <br>

## Usage:

use this within your code
example below:

```python
from saweriaqris import create_payment_qr

myqr = create_payment_qr("nindtz", 10000, "Budi", "budi@saweria.co", "Semangat!")
qrcode = myqr[0]
transaction_id = myqr[1]

# Just feed the qrcode to your favourite qr code generator
# transaction_id for matching purpose to your webhook calls
```

## Example use case:

Discord bot Donate QRIS<br>
<img width="401" alt="image" src="https://github.com/user-attachments/assets/f607cc45-5836-4c19-abe2-b2b1f8393d1b" />

#### Thank you
