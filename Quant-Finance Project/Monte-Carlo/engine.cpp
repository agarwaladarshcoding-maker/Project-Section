#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <random>
#include <algorithm>
#include <fstream>
#include <chrono>

// --- 1. DATA STRUCTURES ---
class Stock {
public:
    std::string symbol;
    double price;
    double volatility;
};

// --- 2. MONTE CARLO ENGINE ---
// We pass 'results' by reference (&) to avoid copying memory. Fast.
double MonteCarloSimulator(const Stock &stock, double strikePrice, double timeInYears, double riskFreeRate, int N, std::vector<double>& results)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> dist(0.0, 1.0);

    // Pre-calculate drift and diffusion to save CPU cycles inside the loop
    double driftInDay = (riskFreeRate - 0.5 * stock.volatility * stock.volatility) * (timeInYears / 252);
    double diffusionInDay = stock.volatility * std::sqrt(timeInYears / 252);

    double totalPayoff = 0.0;

    // The "Hot Loop" (100,000 simulations)
    for (int i = 0; i < N; ++i)
    {
        double currentStockPrice = stock.price;
        double barrierPrice = stock.price * 0.8; // 20% drop kills the option
        bool isKnockedOut = false;

        // Simulate 252 Trading Days
        for (int day = 0; day < 252; ++day)
        {
            double Z = dist(gen);
            currentStockPrice *= std::exp(driftInDay + diffusionInDay * Z);

            // Barrier Check
            if (currentStockPrice <= barrierPrice)
            {
                isKnockedOut = true;
                break;
            }
        }

        // Store the final price (The Distribution)
        results.push_back(currentStockPrice);

        // Calculate Payoff (The Option Value)
        double payoff = 0.0;
        if (!isKnockedOut)
        {
            payoff = std::max(currentStockPrice - strikePrice, 0.0);
        }
        totalPayoff += payoff;
    }

    double averagePayoff = totalPayoff / N;
    return averagePayoff * std::exp(-riskFreeRate * timeInYears);
}

// --- 3. MAIN ENTRY POINT ---
int main(int argc, char* argv[]) 
{
    // Defaults (If you run without Python)
    std::string symbol = "TEST";
    double price = 100.0;
    double volatility = 0.2;

    // PARSE INPUTS FROM PYTHON
    // argv[0] is program name, argv[1] is Symbol, argv[2] is Price, argv[3] is Vol
    if (argc >= 4) {
        symbol = argv[1];
        try {
            price = std::stod(argv[2]);        // String to Double
            volatility = std::stod(argv[3]);   // String to Double
        } catch (...) {
            std::cerr << "Error parsing arguments. Using defaults." << std::endl;
        }
    }

    Stock myStock;
    myStock.symbol = symbol;
    myStock.price = price;
    myStock.volatility = volatility;

    double strikePrice = price; // At-the-money option
    double r = 0.05;            // 5% Risk Free Rate
    double T = 1.0;             // 1 Year
    int N = 100000;             // 100k Simulations

    // Memory Buffer (Reserve size to prevent reallocation)
    std::vector<double> results;
    results.reserve(N);

    std::cout << "--- C++ ENGINE STARTED ---" << std::endl;
    std::cout << "Simulating: " << symbol << " @ $" << price << " (Vol: " << volatility << ")" << std::endl;

    // Start Timer (Math Only)
    auto start = std::chrono::high_resolution_clock::now();

    double optionPrice = MonteCarloSimulator(myStock, strikePrice, T, r, N, results);

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << "Theoretical Option Price: " << optionPrice << std::endl;
    std::cout << "Math Time: " << elapsed.count() << "s" << std::endl;

    // WRITE TO CSV (Disk I/O happens AFTER timer)
    std::ofstream file("simulation_data.csv");
    file << "Simulation,Price\n";
    for (int i = 0; i < results.size(); ++i) {
        file << i << "," << results[i] << "\n";
    }
    file.close();

    std::cout << "Data exported to 'simulation_data.csv'" << std::endl;
    std::cout << "--- C++ ENGINE FINISHED ---" << std::endl;

    return 0;
}