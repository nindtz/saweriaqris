## Saweria QRIS code generator

### DISCLAIMER

**use at your own risk**

### Requirements

`$ pip install bs4` Install BeautifulSoup <br>
`$ pip install requests` Install requests

## Usage:

use this within your code
example below:

```python
from saweriaqris import create_payment_qr

myqr = create_payment_qr("nindtz", 10000, "Budi", "budi@saweria.co", "Semangat!")
qrcode = myqr[0]

# just feed the qrcode to your favourite qr code generator
```

#### Thank you
