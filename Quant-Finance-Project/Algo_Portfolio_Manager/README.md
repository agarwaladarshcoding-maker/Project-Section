Algorithmic Portfolio Manager 📈

A quantitative finance tool that constructs an optimal portfolio of stocks using **Modern Portfolio Theory (MPT)** and **Monte Carlo Simulations**. This project analyzes historical data to identify the best risk-adjusted returns (Sharpe Ratio) and the safest possible portfolio allocation (Minimum Volatility).

---

## 🚀 Key Features

* **Automated Data Pipeline:** Fetches real-time adjusted stock data for 20+ tickers using `yfinance` (handling splits & dividends).
* **Financial Mathematics:** Calculates Annualized Returns, Volatility (Standard Deviation), and Correlation Matrices.
* **Monte Carlo Simulation:** Simulates **5,000+ unique portfolios** to visualize the risk-return landscape.
* **Optimization Algorithms:**
    * **Max Sharpe Ratio:** Identifies the portfolio with the highest risk-adjusted return (The "Red Star").
    * **Min Volatility:** Identifies the portfolio with the lowest possible risk (The "Blue Dot").
* **Risk Analysis:** Calculates **Value at Risk (VaR)** at a 95% confidence interval.
* **Visualization:** Plots the **Efficient Frontier** and a **Correlation Heatmap** to visually prove diversification benefits.

---

## 📊 Visuals

### 1. The Efficient Frontier
The graph below displays 5,000 simulated portfolios.
* ⭐️ **Red Star:** Optimal Portfolio (Max Sharpe Ratio)
* 🔵 **Blue Dot:** Safest Portfolio (Min Volatility)

![Efficient Frontier](fronteir.png)

### 2. Correlation Heatmap
Visualizing how assets move in relation to one another. Dark blue areas indicate low correlation, offering the best diversification benefits.

![Correlation Heatmap](correlation.png)

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Libraries:**
    * `pandas` & `numpy` (Data Manipulation & Linear Algebra)
    * `yfinance` (Market Data API)
    * `matplotlib` & `seaborn` (Data Visualization)

---

## 🧠 Quantitative Concepts Applied

1.  **Log vs. Simple Returns:** Used percentage change to normalize price differences across diverse stocks (e.g., comparing Apple at $200 vs. Google at $150).
2.  **Sharpe Ratio:** Calculated as $(R_p - R_f) / \sigma_p$ to measure "Reward per unit of Risk."
3.  **Covariance Matrix:** Used to assess how asset prices move together, which is critical for mathematical diversification.
4.  **Value at Risk (VaR):** A statistical technique used to measure the level of financial risk within a firm or portfolio over a specific time frame.

---

## 📥 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/Algo_Portfolio_Manager.git](https://github.com/yourusername/Algo_Portfolio_Manager.git)
    ```

2.  **Install dependencies:**
    ```bash
    pip install pandas numpy yfinance matplotlib seaborn
    ```

3.  **Run the main script:**
    ```bash
    python main.py
    ```

---

## 🔮 Future Improvements

* [ ] Implement **Backtesting** to see how the optimized portfolio would have performed in previous years.
* [ ] Add **Machine Learning (K-Means Clustering)** to automatically group stocks by behavior rather than sector labels.
* [ ] Deploy as a web app using **Streamlit**.
