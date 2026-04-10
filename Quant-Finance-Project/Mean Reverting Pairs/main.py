import pandas as pd
import yfinance as yf
from rolling_adf import compute_rolling_adf, add_cointegration_filter
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model as lm
from statsmodels.tsa.stattools import adfuller
from backtest import run_backtest, trades_to_dataframe
from metrics import win_rate, max_drawdown, sharpe_ratio


def fetch_data(ticker_x: str, ticker_y: str, period: str = "3y") -> pd.DataFrame:
    """Download closing prices for two tickers and return log-transformed DataFrame."""
    df = yf.download([ticker_x, ticker_y], period=period)['Close']
    df = np.log(df).dropna()
    return df

def compute_rolling_spread(df: pd.DataFrame, ticker_x: str, ticker_y: str, window: int = 90) -> pd.DataFrame:
    betas = []
    dates = []
    spreads = []
    model = lm.LinearRegression()
    for i in range(window, len(df)):
        x_slice = df[ticker_x].iloc[i-window:i].values.reshape(-1,1)
        y_slice = df[ticker_y].iloc[i-window:i].values
        model.fit(x_slice, y_slice)
        beta = model.coef_[0]
        alpha = model.intercept_
        # Calculate Spread: Error = Actual_y - Predicted_y
        # Spread = Log_MSFT - (Beta * Log_GOOGL + Alpha)
        current_x = df[ticker_x].iloc[i]
        current_y = df[ticker_y].iloc[i]
        current_spread = current_y -(beta* current_x + alpha)
        betas.append(beta)
        spreads.append(current_spread)
        dates.append(df.index[i])
    
    results = pd.DataFrame({"Spread":spreads,"Beta": betas}, index= dates)
    return results



def run_adf_test(spreads: pd.Series) -> dict:
    adf_result = adfuller(spreads)
    p_value = adf_result[1]
    print(f"ADF Statistic: {adf_result[0]:.4f}")
    print(f"p-value: {p_value:.4f}")
    return {"statistic": adf_result[0], "p_value": p_value}

def generate_signals(results: pd.DataFrame, z_window: int = 30) -> pd.DataFrame:
    results['Mean'] = results['Spread'].rolling(window=z_window).mean()
    results['Std'] = results['Spread'].rolling(z_window).std()
    results['Z_Score'] = (results['Spread'] - results['Mean']) / results['Std']
    return results

def plot_results(results: pd.DataFrame, ticker_x: str, ticker_y: str) -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    ax1.plot(results['Spread'], color='purple', label='Log Spread')
    ax1.axhline(0, color='black', linestyle='--')
    ax1.set_title(f'Cointegration Spread ({ticker_y} vs {ticker_x})')
    ax1.legend()

    ax2.plot(results['Z_Score'], color='blue', label='Z-Score')
    ax2.axhline(2, color='red', linestyle='--', label='Sell Spread (+2σ)')
    ax2.axhline(-2, color='green', linestyle='--', label='Buy Spread (-2σ)')
    ax2.set_title('Trading Signals (Z-Score)')
    ax2.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # constants
    TICKER_X = "GOOGL"
    TICKER_Y = "MSFT"

    # pipeline
    df        = fetch_data(TICKER_X, TICKER_Y)
    results   = compute_rolling_spread(df, TICKER_X, TICKER_Y)
    adf       = run_adf_test(results["Spread"])
    results   = generate_signals(results)
    plot_results(results, TICKER_X, TICKER_Y)
    trades      = run_backtest(results)
    trades_df   = trades_to_dataframe(trades)
    print(trades_df)
    print(np.sum(trades_df['pnl']))
    print(f"\n--- Strategy Performance ---")
    print(f"Total Trades   : {len(trades_df)}")
    print(f"Total PnL      : {trades_df['pnl'].sum():.4f}")
    print(f"Win Rate       : {win_rate(trades_df):.1%}")
    print(f"Max Drawdown   : {max_drawdown(trades_df):.4f}")
    print(f"Sharpe Ratio   : {sharpe_ratio(trades_df):.2f}")
    # after generate_signals, before run_backtest:
    results = compute_rolling_adf(results)
    results = add_cointegration_filter(results)

    # print how many days were tradeable:
    pct = results['Is_Cointegrated'].mean()
    print(f"Days cointegrated: {pct:.1%}")
    trades      = run_backtest(results)
    trades_df   = trades_to_dataframe(trades)
    print(f"\n--- Strategy Performance ---")
    print(f"Total Trades   : {len(trades_df)}")
    print(f"Total PnL      : {trades_df['pnl'].sum():.4f}")
    print(f"Win Rate       : {win_rate(trades_df):.1%}")
    print(f"Max Drawdown   : {max_drawdown(trades_df):.4f}")
    print(f"Sharpe Ratio   : {sharpe_ratio(trades_df):.2f}")
