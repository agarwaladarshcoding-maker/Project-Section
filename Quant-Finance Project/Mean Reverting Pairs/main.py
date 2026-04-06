import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model as lm
from statsmodels.tsa.stattools import adfuller

print("------ Mean Reverting Pairs-----------")

# 1. Setup
ticker_x = "GOOGL"
ticker_y = "MSFT"

# 2. DATA ACQUISITION & TRANSFORMATION
# Use Log Prices to stabilize variance and make the relationship linear
df = yf.download([ticker_x, ticker_y], period="3y")['Close']
df = np.log(df).dropna()

# 3. ROLLING REGRESSION LOOP
window = 90
betas = []
dates = []
spreads = []
model = lm.LinearRegression()

for i in range(window, len(df)):
    # X = Google, y = Microsoft
    X_slice = df[ticker_x].iloc[i-window:i].values.reshape(-1, 1)
    y_slice = df[ticker_y].iloc[i-window:i].values
    
    model.fit(X_slice, y_slice)
    
    beta = model.coef_[0]
    alpha = model.intercept_
    
    # Calculate Spread: Error = Actual_y - Predicted_y
    # Spread = Log_MSFT - (Beta * Log_GOOGL + Alpha)
    current_x = df[ticker_x].iloc[i]
    current_y = df[ticker_y].iloc[i]
    current_spread = current_y - (beta * current_x + alpha)
    
    betas.append(beta)
    spreads.append(current_spread)
    dates.append(df.index[i])

# 4. RESULTS & STATISTICAL TESTING
results = pd.DataFrame({'Spread': spreads}, index=dates)
results['Beta'] = betas

# Run ADF Test on the final Spread series
adf_result = adfuller(results['Spread'])
p_value = adf_result[1]

print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {p_value:.4f}")

# 5. SIGNAL GENERATION (Z-SCORE)
# Normalizing the spread so we know when it's "abnormal"
results['Mean'] = results['Spread'].rolling(window=30).mean()
results['Std'] = results['Spread'].rolling(window=30).std()
results['Z-Score'] = (results['Spread'] - results['Mean']) / results['Std']

# 6. VISUALIZATION
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

ax1.plot(results['Spread'], color='purple', label='Log Spread')
ax1.axhline(0, color='black', linestyle='--')
ax1.set_title(f'Cointegration Spread ({ticker_y} vs {ticker_x})')
ax1.legend()

ax2.plot(results['Z-Score'], color='blue', label='Z-Score')
ax2.axhline(2, color='red', linestyle='--', label='Sell Spread (+2σ)')
ax2.axhline(-2, color='green', linestyle='--', label='Buy Spread (-2σ)')
ax2.set_title('Trading Signals (Z-Score)')
ax2.legend()

plt.tight_layout()
plt.show()