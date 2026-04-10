import pandas as pd
import numpy as np
def win_rate(trades_df: pd.DataFrame) -> float:
    """Return fraction of trades with positive PnL."""
    rows_over_zero = trades_df[trades_df['pnl']>0].shape[0]
    number_of_rows = trades_df.shape[0]
    win_percentage = rows_over_zero/number_of_rows
    return win_percentage

def max_drawdown(trades_df: pd.DataFrame) -> float:
    """Return the maximum peak-to-trough drawdown of the cumulative PnL curve."""
    cumulative = trades_df['pnl'].cumsum()
    running_max =cumulative.cummax()
    drawdown = cumulative - running_max
    return drawdown.min()

def sharpe_ratio(trades_df: pd.DataFrame) -> float:
    """Return annualised Sharpe ratio of the strategy."""
    mean_pnl = trades_df['pnl'].mean()
    std_pnl = trades_df['pnl'].std()
    if std_pnl ==0:
        return 0.0
    days = (trades_df['entry_date'].max() - trades_df['entry_date'].min()).days
    years = days / 365.25
    trades_per_year = len(trades_df) / years
    return (mean_pnl/std_pnl)*np.sqrt(trades_per_year)
