def execute_trade(client, symbol:str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):
    payload = {
        "symbol":symbol,
        "side": side,
        "type": order_type,
        "quantity":quantity
    }
    if order_type == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = "GTC"

    elif order_type == "STOP_MARKET":
        payload["stopPrice"] = stop_price

    elif order_type == "STOP":
        payload["price"] = price
        payload["stopPrice"] = stop_price
        payload["timeInForce"] = "GTC"
    
    print(f"--> Sending {order_type} {side} order for {quantity} {symbol}...")
    try:
        response = client.send_signed_request("POST", "/fapi/v1/order", payload=payload)
        return response
    except Exception as e:
        # We will catch this properly in the CLI layer, but it's good to raise it here
        raise Exception(f"Failed to execute trade: {str(e)}")
