import pandas as pd
def run_backtest( results: pd.DataFrame, entry_z: float = 2.0, exit_z: float = 0.5 ) -> list[dict]:
    """Simulate trades based on Z-score signals and return list of completed trades."""
    trades = []
    position = "FLAT"
    entry_date = None
    entry_spread = None
    entry_z_value = None
    for date, row in results.iterrows():
        today_z = row["Z_Score"]
        today_spread = row["Spread"]
        if pd.isna(today_z):
            continue
        else:
            if position =="FLAT":
                if 'Is_Cointegrated' in results.columns:
                    if not row['Is_Cointegrated']:
                        continue   
                if today_z<-entry_z:
                    position = "LONG"
                    entry_date = date
                    entry_spread = row["Spread"]
                    entry_z_value = today_z
                elif today_z>entry_z:
                   position ="SHORT" 
                   entry_date = date
                   entry_spread = row["Spread"]
                   entry_z_value= today_z
            elif position=="LONG":
                if today_z > -exit_z:
                    pnl = today_spread - entry_spread
                    trade = {
                        "entry_date":  entry_date,
                        "exit_date":   date,
                        "direction":   position,
                        "entry_spread": entry_spread,   # spread value when trade opened
                        "exit_spread":  today_spread,   # spread value when trade closed
                        "entry_z":      entry_z_value,   # Z-score when trade opened
                        "exit_z":       today_z,   # Z-score when trade closed
                        "pnl":          pnl    # profit/loss on this trade
                    }
                    trades.append(trade)
                    position = "FLAT"
                    entry_date = None
                    entry_spread = None
                    entry_z_value = None
            else:
                if today_z<exit_z:
                    pnl = entry_spread - today_spread
                    trade = {
                        "entry_date":  entry_date,
                        "exit_date":   date,
                        "direction":   position,
                        "entry_spread": entry_spread,   # spread value when trade opened
                        "exit_spread":  today_spread,   # spread value when trade closed
                        "entry_z":      entry_z_value,   # Z-score when trade opened
                        "exit_z":       today_z,   # Z-score when trade closed
                        "pnl":          pnl    # profit/loss on this trade
                    }
                    trades.append(trade)
                    position = "FLAT"
                    entry_date = None
                    entry_spread = None
                    entry_z_value = None

    return trades

def trades_to_dataframe(trades: list[dict]) -> pd.DataFrame:
    """Convert list of trade dicts to a DataFrame sorted by entry date."""
    return pd.DataFrame(trades)
