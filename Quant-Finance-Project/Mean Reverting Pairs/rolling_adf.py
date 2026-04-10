import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
def compute_rolling_adf(results: pd.DataFrame, window: int = 60) -> pd.DataFrame:
    """Compute rolling ADF p-value on the spread series and add as new column."""
    results['ADF_PValue'] = np.nan;
    for i in range(window, len(results)):
        slice = results['Spread'].iloc[i-window:i]
        ad_results = adfuller(slice)
        p_value = ad_results[0]
        results['ADF_PValue'].iloc[i]  = p_value
    return results

def add_cointegration_filter(results: pd.DataFrame, p_threshold: float = 0.05) -> pd.DataFrame:
    """Add boolean column Is_Cointegrated based on rolling ADF p-value threshold."""
    results["Is_Cointegrated"] = results['ADF_PValue']<p_threshold
    return results

