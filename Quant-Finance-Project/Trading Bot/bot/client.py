import time
import hmac
import hashlib
import urllib.parse
import requests

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binancefuture.com"

    def _generate_signature(self, query_string):
        # Hashes the query string for safety
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, http_method, endpoint, payload=None):
        if payload is None:
            payload = {}

        # 1. Add the mandatory timestamp and other detials comes from cli
        payload['timestamp'] = int(time.time() * 1000)

        # 2. Format the payload into a standard query string
        query_string = urllib.parse.urlencode(payload)

        # 3. Generate the signature and add it
        signature = self._generate_signature(query_string)
        signed_query_string = f"{query_string}&signature={signature}"

        full_url = f"{self.base_url}{endpoint}?{signed_query_string}"
        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        response = requests.request(http_method, full_url, headers=headers)
        response.raise_for_status() 

        return response.json()
    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        # Limit orders require a price and a Time-In-Force (GTC = Good Till Canceled)
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        # Let the dispatcher handle the heavy lifting!
        return self.send_signed_request("POST", "/fapi/v1/order", payload=params)