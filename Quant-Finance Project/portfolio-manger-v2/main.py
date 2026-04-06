import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


tickerSymbols = ["AAPL", "MSFT", "GOOGL", "XOM", "JPM","RIVN", "COIN", "SPY"]
df = pd.DataFrame()


for tickerSymbol in tickerSymbols:
    df[f'{tickerSymbol}'] = yf.Ticker(tickerSymbol).history(period="10y", interval="1d", auto_adjust=True )["Close"]

print(df.head())

threshold = 0.30
missing_fractions = df.isna().mean()
valid_columns = missing_fractions[missing_fractions < threshold].index
df = df[valid_columns]

print(f"Columns kept: {list(df.columns)}")


df = df.ffill()


df = df.dropna()

print("\nShape after cleaning:", df.shape)
print("Remaining NaNs:\n", df.isna().sum())


for tickerSymbol in valid_columns:
    df[f'{tickerSymbol}_PCA'] = np.log2(df[tickerSymbol]/df[tickerSymbol].shift(1))
    pcaMean = df[f'{tickerSymbol}_PCA'].mean()
    pcaStd = df[f'{tickerSymbol}_PCA'].std()
    df[f'{tickerSymbol}_Nmzt'] = (np.log2(df[tickerSymbol]/df[tickerSymbol].shift(1)) - pcaMean)/pcaStd

df = df.dropna()
print(df)

X = pd.DataFrame()

for tickerSymbol in valid_columns:
    X[f'{tickerSymbol}_Nmzt'] = df[f'{tickerSymbol}_Nmzt']

number_Of_Rows = X.shape[0]
cov_mat = np.dot(np.transpose(X), X)
cov_mat = cov_mat/(number_Of_Rows -1)
print(cov_mat)


eigenvalues, eigenvectors = np.linalg.eigh(cov_mat)


sorted_indices = np.argsort(eigenvalues)[::-1]


sorted_eigenvalues = eigenvalues[sorted_indices]


sorted_eigenvectors = eigenvectors[:, sorted_indices]

print("Sorted Eigenvalues:\n", sorted_eigenvalues)


totalMarketVairance = np.sum(sorted_eigenvalues)
explainVarianceRatio = sorted_eigenvalues/totalMarketVairance
print(explainVarianceRatio)


pc1 = sorted_eigenvectors[:, 0]
pc2 = sorted_eigenvectors[:, 1]

# Initialize the plot
plt.figure(figsize=(10, 7))
plt.scatter(pc1, pc2, color='royalblue', edgecolors='black', s=100)


for i, ticker in enumerate(valid_columns):
    plt.annotate(
        ticker, 
        (pc1[i], pc2[i]), 
        xytext=(8, 8),          
        textcoords='offset points', 
        fontsize=12, 
        fontweight='bold'
    )


plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.axvline(0, color='gray', linestyle='--', linewidth=1)
plt.grid(True, alpha=0.3)
plt.title('Statistical Factor Model: PC1 vs PC2', fontsize=16, fontweight='bold')
plt.xlabel('PC1: Market Factor (62.4% Variance)', fontsize=14)
plt.ylabel('PC2: Sector/Divergence Factor', fontsize=14)

# Render the plot
plt.show()