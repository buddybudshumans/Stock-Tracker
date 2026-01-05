```markdown
# Multi-Stock Price & Gains Tracker (Streamlit)

What this is
- A simple Streamlit app that tracks price and gains (absolute and percent) over time for the stocks you choose.
- For each ticker you can enter a buy date and either shares, total amount invested, or an explicit buy price.
- The app fetches historical prices (yfinance), resolves buy price/shares if needed, and plots:
  - Price chart (Close)
  - Percent gain since the buy date for each ticker
  - Combined portfolio value and overall P/L

Requirements
- Python 3.8+
- Install dependencies:
  pip install -r requirements.txt

Run
- streamlit run multi_stock_tracker.py

Notes
- Transactions / buy settings are kept only for the current Streamlit session.
- Uses yfinance (no API key). Yahoo may rate-limit heavy use.
- If you want multiple buys per ticker, advanced indicators, or persistent storage, I can add those next.
```
