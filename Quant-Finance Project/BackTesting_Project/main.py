import yfinance as yf
import pandas as pd
import numpy as np
print("------------The BackTesting Project---------")

#Picking Tesla as the stock for the project
ticker = "TLSA"

#Uisng Yfinance to download tesla stock data for the last 5 years
stockTicker = yf.Ticker(ticker)
dfStock = pd.DataFrame()
dfStock["Close"] = stockTicker.history(period="5y", auto_adjust= True)["Close"]


#Getting the Rolling Average For 50 And 20 Days
dfStock["SMA_50"] = dfStock["Close"].rolling(window=50).mean()
dfStock["SMA_20"] = dfStock["Close"].rolling(window=20).mean()

#Dropping the Nan Values
dfStock = dfStock.dropna()
filt = dfStock["SMA_50"]>dfStock["SMA_20"]
dfStock["Signal"] = np.where(dfStock["SMA_50"]>dfStock["SMA_20"],1,0)

print(dfStock["Signal"].value_counts())

