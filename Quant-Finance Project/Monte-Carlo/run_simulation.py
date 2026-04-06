import yfinance as yf
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# --- CONFIGURATION ---
SYMBOL = "NVDA"        # Change this to whatever stock you want (e.g., AAPL, TSLA)
VOLATILITY = 0.45      # Estimated Volatility (45% for high growth)
EXECUTABLE_NAME = "./engine"  # On Mac/Linux
# EXECUTABLE_NAME = "engine.exe" # Uncomment this line if on Windows

def main():
    # 1. FETCH LIVE DATA
    print(f"\n[PYTHON] Fetching live data for {SYMBOL}...")
    try:
        ticker = yf.Ticker(SYMBOL)
        # Get today's data
        data = ticker.history(period="1d")
        
        if data.empty:
            print("[PYTHON] Market closed or invalid symbol. Using default $100.")
            current_price = 100.0
        else:
            current_price = data['Close'].iloc[-1]
            print(f"[PYTHON] Latest Market Price: ${current_price:.2f}")

    except Exception as e:
        print(f"[PYTHON] Error fetching data: {e}")
        current_price = 100.0

    # 2. RUN C++ ENGINE
    print("\n[PYTHON] Launching C++ Engine...")
    
    if not os.path.exists(EXECUTABLE_NAME):
        print(f"[ERROR] Could not find '{EXECUTABLE_NAME}'.")
        print("Please compile first: g++ -O3 engine.cpp -o engine")
        sys.exit(1)

    # Command: ./engine NVDA 125.50 0.45
    cmd = [EXECUTABLE_NAME, SYMBOL, str(current_price), str(VOLATILITY)]
    
    try:
        # Halt Python until C++ finishes
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] C++ Engine crashed.")
        sys.exit(1)

    # 3. VISUALIZE RESULTS
    print("\n[PYTHON] Visualizing data...")
    csv_file = "simulation_data.csv"
    
    if not os.path.exists(csv_file):
        print(f"[ERROR] '{csv_file}' not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(csv_file)
        
        plt.figure(figsize=(12, 7))
        
        # Plot Histogram
        plt.hist(df['Price'], bins=100, color='#2ca02c', edgecolor='black', alpha=0.7, label='Projected Prices')
        
        # Plot Start Price Line
        plt.axvline(x=current_price, color='red', linestyle='dashed', linewidth=2, label=f'Current Price (${current_price:.2f})')
        
        # Styling
        plt.title(f'Monte Carlo Simulation: {SYMBOL} (1 Year Outlook)', fontsize=16, fontweight='bold')
        plt.xlabel('Projected Stock Price ($)', fontsize=12)
        plt.ylabel('Frequency (Likelihood)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Show Mean
        mean_price = df['Price'].mean()
        plt.text(0.02, 0.95, f'Mean Prediction: ${mean_price:.2f}', transform=plt.gca().transAxes, 
                 fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

        print("[PYTHON] Graph generated.")
        plt.show()

    except Exception as e:
        print(f"[ERROR] Plotting failed: {e}")

if __name__ == "__main__":
    main()