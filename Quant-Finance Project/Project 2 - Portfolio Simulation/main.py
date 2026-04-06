import yfinance as yf;
import pandas as pd;
import matplotlib.pyplot as plt;
import seaborn as sb;
import numpy as np;

tickerSymbolApple = "AAPL"
tickerSymbolMicrosoft = "MSFT"
tickerSymbolNVIDIA= "NVDA"
timePeriod = "1y";

#Apple Data
tickerApple = yf.Ticker(tickerSymbolApple);
historicalDataApple = tickerApple.history(period=f'{timePeriod}');
df_Apple = pd.DataFrame();
df_Apple = historicalDataApple;
print(df_Apple);

#Microsoft Data
tickerMicrosoft = yf.Ticker(tickerSymbolMicrosoft);
historicalDataMicrosoft = tickerMicrosoft.history(period=f'{timePeriod}');
df_Microsoft = pd.DataFrame();
df_Microsoft = historicalDataMicrosoft;
print(df_Microsoft);

#NVIDIA
tickerNVIDIA = yf.Ticker(tickerSymbolNVIDIA);
historicalDataNVIDIA = tickerNVIDIA.history(period=f'{timePeriod}');
df_NVIDIA = pd.DataFrame();
df_NVIDIA = historicalDataNVIDIA;
print(df_NVIDIA);

plt.figure(figsize=(14, 6))
plt.plot(df_Apple['Close'], label='Apple Closing Prices')
plt.plot(df_Microsoft['Close'], label='Microsoft Closing Prices')
plt.plot(df_NVIDIA['Close'], label='NVIDIA Closing Prices')
plt.legend()
plt.title('Apple vs Microsoft vs NVIDIA')
plt.grid(True)
# plt.show()

df_AM = pd.DataFrame();
df_AM["Apple Closing Prices"] = df_Apple['Close'];
df_AM['Microsoft Closing Prices'] =df_Microsoft['Close']
df_AM["NVIDIA Closing Prices"] =df_NVIDIA['Close'];
print(df_AM.corr());
plt.figure(figsize=(14,6));
ax = sb.heatmap(df_AM.corr(),annot=True);
# plt.show()

df_Apple['Daily Return'] = df_Apple['Close'].pct_change();
df_Microsoft['Daily Return'] = df_Microsoft['Close'].pct_change();
df_NVIDIA['Daily Return'] = df_NVIDIA['Close'].pct_change();
df_Apple = df_Apple.dropna();
df_Microsoft = df_Microsoft.dropna()
df_NVIDIA = df_NVIDIA.dropna()
print(df_Apple)
print(df_Microsoft)
print(df_NVIDIA)


plt.figure(figsize=(15,8));
plt.plot(df_Apple['Daily Return'], label="Apple Daily Returns");
plt.plot(df_Microsoft['Daily Return'], label= "Microsfot Daily Returns");
plt.plot(df_NVIDIA['Daily Return'], label = "NVIDIA Daily Returns");
plt.legend()
plt.title("Apple vs Microsoft vs NVIDIA Daily Returns")
plt.xlabel("Daily Returns")
plt.ylabel("Year")
plt.show()