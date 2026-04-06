import numpy as np
import pandas as pd
from typing import Dict, Tuple

class PortfolioEngine:
    def __init__(self, price_data: pd.DataFrame, risk_free_rate: float = 0.04):
        self.returns_df = price_data.pct_change().dropna()
        self.mean_returns = self.returns_df.mean() * 252
        self.cov_matrix = self.returns_df.cov() * 252
        self.rf = risk_free_rate
        self.num_assets = len(price_data.columns)

    def run_monte_carlo(self, n_sims: int = 10000) -> Dict[str, np.ndarray]:
        """
        Vectorized Monte Carlo Simulation. 
        Calculates returns, volatility, and Sharpe ratios for thousands of portfolios at once.
        """
        # Generate random weights matrix (n_sims x num_assets)
        weights = np.random.random((n_sims, self.num_assets))
        weights /= np.sum(weights, axis=1)[:, np.newaxis]

        # Vectorized Portfolio Returns: R = W * Mean_Returns^T
        port_returns = np.dot(weights, self.mean_returns)

        # Vectorized Portfolio Volatility: Sigma = sqrt(W * Cov * W^T)
        # Using Einstein Summation for ultra-fast matrix diagonal calculation
        port_volatility = np.sqrt(np.einsum('ij,jk,ik->i', weights, self.cov_matrix, weights))

        # Sharpe Ratio Calculation
        sharpe_ratios = (port_returns - self.rf) / port_volatility

        return {
            "weights": weights,
            "returns": port_returns,
            "volatility": port_volatility,
            "sharpe": sharpe_ratios
        }

    def calculate_var(self, weights: np.ndarray, portfolio_value: float = 100000, conf: float = 0.95) -> float:
       
        from scipy.stats import norm
        port_return = np.dot(weights, self.mean_returns) / 252
        port_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix / 252, weights)))
        
        z_score = norm.ppf(1 - conf)
        var = portfolio_value * (port_return + z_score * port_vol)
        return var