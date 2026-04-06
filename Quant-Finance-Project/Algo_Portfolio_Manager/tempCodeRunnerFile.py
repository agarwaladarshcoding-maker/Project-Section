import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(234)






print("----Algorithmic Portfolio Manager -------");





# The Universe of 20 Stocks - Used Gemini to pick the stocks for this study
# You can change it as per your need
stock_tickers = [
    # Technology (The Growth Engines)
    "AAPL", "MSFT", "GOOGL", "NVDA", "AMD",
    
    # Finance ( The Economy Trackers)
    "JPM", "BAC", "V", "MA",
    
    # Healthcare (The Defensive Players)
    "JNJ", "PFE", "UNH", "MRK",
    
    # Consumer Goods (The Stable Earners)
    "PG", "KO", "WMT", "COST",
    
    # Energy & Industrial (The Cyclical Stocks)
    "XOM", "CVX", "CAT"
]
#Creating an Empty Data Frame
df = pd.DataFrame()


#Adding Prices of Each Stock For the Last Year to the dataframe
for stock in stock_tickers:
    stockTicker = yf.Ticker(stock)
    stockData = stockTicker.history(period="1y", auto_adjust=True)
    df[stock] = stockData['Close']

#Handling the NaN Data By Dropna for safety purposes
df =df.dropna()

#Creating a new dataFrame returnDf to store daily returns of the stock
returnDf = pd.DataFrame();
expectedMean = pd.DataFrame()
covMatrix = pd.DataFrame()

#Calulating the pxt change for th returndf
for column in df.columns:
    returnDf[column] = df[column].pct_change()


#Deleting the Fast Row As it contains Nan
returnDf =returnDf.dropna()
expectedMean = returnDf.mean()*252
covMatrix= returnDf.cov()*252
print(expectedMean)

#Using Monte Carlo Simulation
allWeights = []
returnArr = []
volatilityArr = []
sharpeArr = []


for i in range(1):
    random_floats = [np.random.uniform(0.0, 1.0) for _ in range(20)]
    totalWeight = np.sum(random_floats)
    randomWeight = (random_floats/totalWeight)
    expectedReturns = randomWeight*expectedMean
    totalReturn = np.sum(expectedReturns)
    volatility  = np.dot(randomWeight,covMatrix)
    sharpeArr = np.sqrt(expectedReturns/volatility)

    allWeights.append(randomWeight)
    returnArr.append(totalReturn)
    volatilityArr.append(volatility)
    sharpeArr.append(sharpeArr)

    # print(volatility)


    

