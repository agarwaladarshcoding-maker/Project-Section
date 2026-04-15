import os
import streamlit as st
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

st.set_page_config(page_title="Binance Testnet Bot", layout="centered")
st.title("📈 Binance Futures Trading Bot")
st.markdown("A lightweight algorithmic execution interface connected to the Binance Testnet.")
st.divider()

#  UI Input Forms
col1, col2 = st.columns(2)

with col1:
    raw_symbol = st.text_input("Trading Pair (e.g., BTCUSDT)", value="BTCUSDT")
    raw_side = st.selectbox("Order Side", ["BUY", "SELL"])

with col2:
    raw_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP", "STOP_MARKET", "OCO"])
    raw_qty = st.text_input("Quantity", value="0.01")

# Optional Inputs 
clean_price = None
clean_stop_price = None

# If order type uses the Limit Order Book, ask for a price
if raw_type in ["LIMIT", "STOP", "OCO"]:
    raw_price = st.text_input("Limit Price (Required)")
else:
    raw_price = None

# If order type uses the Trigger Engine, ask for a stop price
if raw_type in ["STOP", "STOP_MARKET", "OCO"]:
    raw_stop_price = st.text_input("Stop/Trigger Price (Required)")
else:
    raw_stop_price = None

st.divider()

# execution Zone
if st.button(" Place Order", use_container_width=True):
    with st.spinner("Validating and routing to exchange..."):
        try:
            # Validate all inputs
            if not raw_symbol.strip():
                raise ValidationError("Symbol cannot be empty.")
                
            clean_symbol = raw_symbol.upper().strip()
            clean_side = validate_side(raw_side)
            clean_type = validate_order_type(raw_type)
            clean_quantity = validate_quantity(raw_qty)
            clean_price = validate_price(clean_type, raw_price)
            clean_stop_price = validate_stop_price(clean_type, raw_stop_price)

            # Step B: Load Credentials
            load_dotenv()
            api_key = os.getenv("BINANCE_API_KEY")
            api_secret = os.getenv("BINANCE_API_SECRET")

            if not api_key or not api_secret:
                st.error("Missing API Credentials. Check your `.env` file.")
                st.stop()

            # Initialize Client & Dispatch Trade
            client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
            
            response = execute_trade(
                client=client,
                symbol=clean_symbol,
                side=clean_side,
                order_type=clean_type,
                quantity=clean_quantity,
                price=clean_price,
                stop_price=clean_stop_price
            )

            # Check the Response
            if "orderId" in response:
                st.success(f"✅ Order Placed Successfully! (ID: {response.get('orderId')})")
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                metric_col1.metric("Status", response.get("status"))
                metric_col2.metric("Executed Qty", response.get("executedQty"))
                
                avg_price = response.get("avgPrice") or response.get("price", "N/A")
                metric_col3.metric("Avg Price", avg_price)
                
                # Show raw JSON in a collapsible box for debugging
                with st.expander("View Raw JSON Exchange Receipt"):
                    st.json(response)
            else:
                st.error("❌ Exchange rejected the order.")
                st.json(response)

        except ValidationError as e:
            st.warning(f"⚠️ Validation Error: {str(e)}")
        except Exception as e:
            st.error(f"🛑 Critical Execution Failure: {str(e)}")