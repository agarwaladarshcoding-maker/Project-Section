import pandas as pd;
import matplotlib.pyplot as plt;

#print("Everything is working fine");

#Read Files For Apple CSV file
# df = pd.read_csv("APPLE.csv");

#Set Date as index
# df = df.set_index("Date");

# fig, ax = plt.subplots()
# x = df.index;
# y = df["Close"];
# ax.plot(x, y, linewidth=1.0)
# print(df.iloc[-1]["Close"]);
# df["MA20"] = df["Close"].rolling(window=20).mean();# gives rolling average of the last 20 closing prices
# df["MA50"] = df["Close"].rolling(window=50).mean();#gives rolling average of the last 50 closing prices;
# df["Daily Returns"] = df['Close'].pct_change();#gives percetnage change in closing price comapred to the previous day
# df = df.dropna();# drops any row which has any column with Nan;
# df_year = pd.DataFrame();
# # df_year["Open"] = 
# df = pd.to_datetime(df.index, utc=True);
# print(df)
# print(df.year.value_counts());


# # print(df);
# # plt.show();

import yfinance as yf

data = yf.download("AAPL", start="2020-01-01", end="2025-12-31")
data.head()
print(data);
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 5))
plt.plot(data['Close'])
plt.title('AAPL Adjusted Close Price')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.grid(True)
# plt.show()

data["MA20"] = data["Close"].rolling(window=20).mean();# gives rolling average of the last 20 closing prices
data["MA50"] = data["Close"].rolling(window=50).mean();#gives rolling average of the last 50 closing prices;
plt.figure(figsize=(14, 6))
plt.plot(data['Close'], label='Close')
plt.plot(data['MA20'], label='20-Day MA')
plt.plot(data['MA50'], label='50-Day MA')
data["MA20>MA50"] =(data["MA20"]>data['MA50'])*100;
data["MA20<MA50"] =(data["MA20"]<data['MA50'])*100;
# plt.plot(data["MA20>MA50"], label = "MA20>MA50");
# # print(data["MA20>MA50"].value_counts())
# # print(data["MA20<MA50"].value_counts())
# # plt.scatter(2020,67.227615);
# plt.legend()
# plt.title('AAPL Price with Moving Averages')
# plt.grid(True)
# plt.show()


# print(data.loc[data['MA50']>=data['MA20']])

import seaborn as sns
data['Daily Return'] = data['Close'].pct_change()
plt.figure(figsize=(12, 5))
sns.histplot(data['Daily Return'].dropna(), bins=10, kde=True)
plt.title('Histogram of Daily Returns')
plt.show()

plt.figure(figsize=(6, 5))
sns.boxplot(y=data['Daily Return'].dropna())
plt.title('Boxplot of Daily Returns')
plt.show()
