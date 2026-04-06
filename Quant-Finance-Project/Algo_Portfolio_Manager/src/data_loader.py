import yfinance as yf
import pandas as pd
import logging
from typing import List

def fetch_portfolio_data(tickers: List[str], period: str = "1y") -> pd.DataFrame:
    data = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, period=period, progress=False)
            if not df.empty:
                # Use 'Close' price for simplicity; 'Adj Close' is better for dividends
                data[ticker] = df['Close'].iloc[:, 0] if isinstance(df['Close'], pd.DataFrame) else df['Close']
                logging.info(f"Successfully fetched {ticker}")
            else:
                logging.warning(f"No data for {ticker}")
        except Exception as e:
            logging.error(f"Failed to fetch {ticker}: {str(e)}")

    # Combine into a single DF and drop any days where a stock might have missing data
    final_df = pd.DataFrame(data).dropna()
    logging.info(f"Data ingestion complete. Matrix shape: {final_df.shape}")
    return final_df