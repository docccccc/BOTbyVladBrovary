import config

url = 'https://apirone.com/api/v2/wallets/{}/addresses'.format(config.WALLET_ID)
post = {
    "callback": {
        "url": "http://example.com/callback",
        "data": {
            "invoice_id": "1234",
            "secret": "7j0ap91o99cxj8k9"
        }
    }
}