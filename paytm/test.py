# More Details: https://developer.paytm.com/docs/checksum/#python

import requests
import json

from paytm.checksum import generateSignature,verifySignature
from django.conf import settings
# from paytmchecksum.PaytmChecksum import generateSignature

# Generate Checksum via Hash/Array
# initialize an Hash/Array
paytmParams = {}

paytmParams["MID"] = settings.PAYTM_MID
paytmParams["ORDERID"] = "dbfdbdrdf564f56b1fdb"

# Generate checksum by parameters we have
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
paytmChecksum = generateSignature(paytmParams, settings.PAYTM_MID_KEY)
verifyChecksum = verifySignature(paytmParams, settings.PAYTM_MID_KEY,paytmChecksum)

print("generateSignature Returns:" + str(paytmChecksum))
print("verifySignature Returns:" + str(verifyChecksum))

# Generate Checksum via String
# initialize JSON String
body = "{\"mid\":\"NneZUq91488614187284\",\"orderId\":\"dbfdbdrdf564f56b1fdb\"}"

# Generate checksum by parameters we have
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
paytmChecksum = generateSignature(body, settings.PAYTM_MID_KEY)
verifyChecksum = verifySignature(body, settings.PAYTM_MID_KEY, paytmChecksum)

print("generateSignature Returns:" + str(paytmChecksum))
print("verifySignature Returns:" + str(verifyChecksum))