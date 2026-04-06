import json
import logging
import matplotlib.pyplot as plt
from src.data_loader import fetch_portfolio_data
from src.engine import PortfolioEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # 1. Load Config
    with open('config/settings.json', 'r') as f:
        config = json.load(f)

    # 2. Fetch Data
    df = fetch_portfolio_data(config['tickers'], config['simulation_settings']['time_period'])

    # 3. Initialize Engine & Run Simulation
    engine = PortfolioEngine(df, config['simulation_settings']['risk_free_rate'])
    results = engine.run_monte_carlo(config['simulation_settings']['num_portfolios'])

    # 4. Find Optimal Portfolios
    idx_max_sharpe = np.argmax(results['sharpe'])
    best_w = results['weights'][idx_max_sharpe]
    
    # 5. Risk Assessment (VaR)
    var_95 = engine.calculate_var(best_w)
    
    logging.info(f"MAX SHARPE RATIO: {results['sharpe'][idx_max_sharpe]:.2f}")
    logging.info(f"95% Daily VaR: ₹{abs(var_95):,.2f}")

    # 6. Quick Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(results['volatility'], results['returns'], c=results['sharpe'], cmap='viridis', alpha=0.5)
    plt.colorbar(label='Sharpe Ratio')
    plt.scatter(results['volatility'][idx_max_sharpe], results['returns'][idx_max_sharpe], color='red', marker='*', s=200)
    plt.title(f"Efficient Frontier - {config['portfolio_name']}")
    plt.xlabel("Annualized Volatility")
    plt.ylabel("Annualized Returns")
    plt.show()

if __name__ == "__main__":
    import numpy as np # Ensure numpy is available for main.py argmax
    main()