# Binance Futures Testnet Trading Bot  
**Author:** Adarsh Agarwala  
**Position:** Python Developer Intern Applicant (Primetrade.ai)  
**Execution Environment:** Python 3.x  

---

## 📌 Project Objective

This project is a Python application designed to place **Market** and **Limit** orders on the **Binance Futures Testnet (USDT-M)**.

The implementation focuses on:
- Clean and reusable code structure  
- Direct REST API interaction (no heavy wrappers)  
- Secure HMAC SHA256 signing  
- Robust logging and error handling  

---

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python **3.8+**
- Binance Futures Testnet account with API credentials  

---

### 2. Environment Configuration

Clone the repository and create a `.env` file:

```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Base URL used:**
```
https://testnet.binancefuture.com
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Mode A: Standard CLI (Automated)

**Market Order (BUY):**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

**Limit Order (SELL):**
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3500
```

---

### Mode B: Interactive CLI

Run without arguments:

```bash
python cli.py
```

---

### Mode C: Web UI (Streamlit)

```bash
streamlit run app.py
```

---

## 📝 Assumptions & Logic

- **Time-In-Force:** Default is `GTC`  
- **Trigger Orders:** `STOP` requires `stopPrice`  
- **Rounding:** Must match Binance tick size  
- **Logging:** API calls are logged  

---

## 🏗️ Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
├── cli.py
├── app.py
├── README.md
├── requirements.txt
└── .env
```

---

## 📊 Evaluation Criteria Met

- Correct order execution  
- Clean modular code  
- Validation and error handling  
- Logging  
- Documentation  

---

## 📁 Submission Checklist

- Public GitHub repo  
- Source code  
- requirements.txt  
- Log files  
- Submission form  
