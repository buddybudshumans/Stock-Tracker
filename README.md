```markdown
# Simple Stock P/L Tracker (Streamlit)

What this does
- Lets you enter a ticker, buy date, number of shares, and buy price.
- Fetches historical prices (Yahoo via yfinance).
- Shows current profit/loss (absolute and percent) since the buy date.
- Plots portfolio value over time (from buy date to today).

Requirements
- Python 3.8+
- Install dependencies:
  pip install streamlit yfinance pandas matplotlib

Run
- In the folder with `stock_tracker.py`:
  streamlit run stock_tracker.py

Notes
- Uses yfinance (no API key). Yahoo may rate-limit heavy use.
- Supports fractional shares.
- If you want to track multiple entries or auto-refresh, we can extend it.
```
