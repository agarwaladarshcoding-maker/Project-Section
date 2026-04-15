import sys
import os
import argparse
from dotenv import load_dotenv

# Import your custom modules
from bot.client import BinanceFuturesClient
from bot.validators import (
    validate_side, 
    validate_order_type, 
    validate_quantity, 
    validate_price, 
    validate_stop_price,
    ValidationError
)
from bot.orders import execute_trade
from bot.logging_config import setup_logger

def setup_parser():
    """Configures the command line argument parser for standard execution."""
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, help="Order side: BUY or SELL")
    parser.add_argument("--type", type=str, required=True, help="Order type: MARKET, LIMIT, STOP, etc.")
    parser.add_argument("--quantity", type=str, required=True, help="Amount to trade")
    
    parser.add_argument("--price", type=str, help="Limit price (Required for LIMIT and STOP orders)")
    parser.add_argument("--stop-price", type=str, dest="stop_price", help="Trigger price (Required for STOP orders)")
    
    return parser

def interactive_mode():
    """Interactive questionnaire that loops until valid inputs are provided."""
    print("\n--- Interactive Trading Mode ---")
    
    while True:
        try:
            raw_symbol = input("Enter trading pair symbol (e.g., BTCUSDT): ")
            clean_symbol = raw_symbol.upper().strip()
            if not clean_symbol: 
                raise ValidationError("Symbol cannot be empty.")
            break
        except ValidationError as e: 
            print(f"Error: {e}\n")

    while True:
        try:
            raw_side = input("Enter Order Side (BUY/SELL): ")
            clean_side = validate_side(raw_side)
            break
        except ValidationError as e: 
            print(f"Error: {e}\n")

    while True:
        try:
            raw_type = input("Enter Order Type (MARKET/LIMIT/STOP/OCO): ")
            clean_type = validate_order_type(raw_type)
            break
        except ValidationError as e: 
            print(f"Error: {e}\n")

    while True:
        try:
            raw_qty = input("Enter Quantity: ")
            clean_quantity = validate_quantity(raw_qty)
            break
        except ValidationError as e: 
            print(f"Error: {e}\n")

    clean_price = None
    if clean_type in ["LIMIT", "STOP", "OCO"]:
        while True:
            try:
                raw_price = input("Enter Limit Price: ")
                clean_price = validate_price(clean_type, raw_price)
                break
            except ValidationError as e: 
                print(f"Error: {e}\n")

    clean_stop_price = None
    if clean_type in ["STOP", "STOP_MARKET", "OCO"]:
        while True:
            try:
                raw_stop = input("Enter Stop/Trigger Price: ")
                clean_stop_price = validate_stop_price(clean_type, raw_stop)
                break
            except ValidationError as e: 
                print(f"Error: {e}\n")

    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "type": clean_type,
        "quantity": clean_quantity,
        "price": clean_price,
        "stop_price": clean_stop_price
    }

def main():
    # 1. Initialize Logger
    logger = setup_logger()

    if len(sys.argv) > 1:
        parser = setup_parser()
        args = parser.parse_args()
        try:
            clean_type = validate_order_type(args.type)
            params = {
                "symbol": args.symbol.upper(),
                "side": validate_side(args.side),
                "type": clean_type,
                "quantity": validate_quantity(args.quantity),
                "price": validate_price(clean_type, args.price),
                "stop_price": validate_stop_price(clean_type, args.stop_price)
            }
        except ValidationError as e:
            logger.error(f"Input Validation Failed: {str(e)}")
            return
    else:
        # User ran `python cli.py` with no flags, trigger interactive UI
        params = interactive_mode()

    #Loading Credentials
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Missing API Credentials. Please ensure your .env file is set up correctly.")
        return

    # Initialize Client & Execute Trade
    try:
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
        
        logger.info("Connecting to Binance Futures Testnet...")
        response = execute_trade(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["type"],
            quantity=params["quantity"],
            price=params["price"],
            stop_price=params["stop_price"]
        )

        # 5. Parse and log the response
        logger.info("=== Order Request Summary ===")
        logger.info(f"Symbol: {params['symbol']} | Side: {params['side']} | Type: {params['type']} | Qty: {params['quantity']}")
        
        if "orderId" in response:
            logger.info("=== Order Response Details ===")
            logger.info(f"Order ID: {response.get('orderId')}")
            logger.info(f"Status: {response.get('status')}")
            logger.info(f"Executed Qty: {response.get('executedQty')}")
            
            avg_price = response.get('avgPrice') or response.get('price', 'N/A')
            logger.info(f"Avg Price: {avg_price}")
            
            logger.info(" SUCCESS: Order placed successfully on Testnet.")
            logger.info('===============================================')
        else:
            logger.error(" FAILURE: Exchange rejected the order.")
            logger.error(f"Exchange Response: {response}")
            logger.info('===============================================')


    except Exception as e:
        logger.error(f" CRITICAL FAILURE: {str(e)}")
        logger.info('===============================================')

if __name__ == "__main__":
    main()