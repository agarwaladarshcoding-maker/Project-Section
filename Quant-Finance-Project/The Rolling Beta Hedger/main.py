import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model as lm
import yfinance as yf  # Using yfinance to get real data

# 1. SETUP: Download Data (NVDA = Stock, SPY = Market)
tickers = ['NVDA', 'SPY']
data = yf.download(tickers, start="2023-01-01", end="2026-02-14", auto_adjust=True)['Close']

# 2. FEATURE ENGINEERING: Calculate Log Returns
# We use Log Returns for time-series stationarity in Quant models
returns = np.log(data / data.shift(1)).dropna()

# 3. ROLLING WINDOW PARAMETERS
window = 60  # 60 trading days (~3 months)
# ... [Previous code for returns calculation] ...
model = lm.LinearRegression() 
betas = []
r_squared = [] # New list for R^2
dates = []

for i in range(window, len(returns)):
    X = returns['SPY'].iloc[i-window:i].values.reshape(-1, 1)
    y = returns['NVDA'].iloc[i-window:i].values
    
    model.fit(X, y)
    
    # Extract Beta and R-Squared
    betas.append(model.coef_[0])
    r_squared.append(model.score(X, y)) # model.score returns R^2
    dates.append(returns.index[i])

# Update DataFrame
results = pd.DataFrame({'Rolling_Beta': betas, 'R_Squared': r_squared}, index=dates)

# 6. ENHANCED VISUALIZATION
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14), sharex=True)

# Plot 1: NVDA Price
ax1.plot(results.index, data['NVDA'].reindex(results.index), color='green')
ax1.set_title('NVDA Price Action')

# Plot 2: Rolling Beta
ax2.plot(results.index, results['Rolling_Beta'], color='red', label='Beta')
ax2.axhline(1.0, color='black', linestyle='--')
ax2.set_title('Rolling Beta (Magnitude of Risk)')

# Plot 3: R-Squared (The "Confidence" Metric)
ax3.fill_between(results.index, results['R_Squared'], color='blue', alpha=0.3, label='R-Squared')
ax3.set_title('Model Confidence (R-Squared)')
ax3.set_ylim(0, 1) # R^2 is always between 0 and 1

plt.tight_layout()
plt.show()