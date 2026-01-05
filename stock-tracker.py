import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

st.set_page_config(page_title="Stock P/L Tracker", layout="centered")

st.title("Simple Stock Profit / Loss Tracker")
st.markdown("Enter a ticker, the buy date, shares and buy price. The app shows profit since that date and plots portfolio value over time.")

# Input area
col1, col2 = st.columns(2)
with col1:
    ticker = st.text_input("Ticker (e.g. AAPL)", value="AAPL").upper().strip()
    buy_date = st.date_input("Buy date", value=(date.today() - timedelta(days=365)))
with col2:
    shares = st.number_input("Shares (can be fractional)", min_value=0.0, value=1.0, step=0.1, format="%.6f")
    buy_price = st.number_input("Buy price per share (USD)", min_value=0.0, value=100.0, step=0.01, format="%.2f")

st.write("---")

@st.cache_data(ttl=60*30)
def fetch_history(symbol, start_dt, end_dt):
    try:
        tk = yf.Ticker(symbol)
        df = tk.history(start=start_dt, end=end_dt, auto_adjust=False)
        # try adjusted close if available
        if "Close" not in df.columns or df.empty:
            return None
        return df
    except Exception as e:
        return None

if ticker:
    end_dt = date.today() + timedelta(days=1)  # include today
    hist = fetch_history(ticker, buy_date, end_dt)

    if hist is None or hist.empty:
        st.error("Could not fetch historical data for that ticker/date. Check the ticker and date.")
    else:
        # Use Close prices (or Adjusted Close if you prefer)
        if "Close" in hist.columns:
            price_series = hist["Close"].copy()
        elif "Adj Close" in hist.columns:
            price_series = hist["Adj Close"].copy()
        else:
            st.error("No close prices available.")
            price_series = None

        if price_series is not None:
            purchase_value = shares * buy_price
            latest_price = price_series.dropna().iloc[-1]
            current_value = shares * latest_price
            profit = current_value - purchase_value
            profit_pct = (profit / purchase_value) * 100 if purchase_value != 0 else 0.0

            # Create value series and profit series
            value_series = price_series * shares
            profit_series = value_series - purchase_value

            # Summary cards
            colA, colB, colC = st.columns(3)
            colA.metric("Buy value (USD)", f"${purchase_value:,.2f}")
            colB.metric("Current value (USD)", f"${current_value:,.2f}", delta=f"${profit:,.2f}")
            profit_label = f"{profit_pct:.2f}%"
            colC.metric("Profit (%)", profit_label, delta=f"{profit:,.2f}")

            st.write("### Price & Portfolio value")
            fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True, gridspec_kw={'height_ratios': [1,1]})
            ax[0].plot(price_series.index, price_series.values, color="tab:blue")
            ax[0].set_ylabel("Price (USD)")
            ax[0].set_title(f"{ticker} price")

            ax[1].plot(value_series.index, value_series.values, color="tab:green", label="Portfolio value")
            ax[1].axhline(purchase_value, color="gray", linestyle="--", label="Buy value")
            ax[1].set_ylabel("Value (USD)")
            ax[1].set_title("Portfolio value since buy date")
            ax[1].legend()

            plt.tight_layout()
            st.pyplot(fig)

            # Show table of latest rows
            st.write("### Latest data")
            latest_row = pd.DataFrame({
                "Date": [price_series.index[-1].date()],
                "Price": [latest_price],
                "Portfolio value": [current_value],
                "Profit (USD)": [profit],
                "Profit (%)": [profit_pct]
            }).set_index("Date")
            st.table(latest_row.style.format({"Price": "${:,.2f}", "Portfolio value": "${:,.2f}", "Profit (USD)": "${:,.2f}", "Profit (%)": "{:.2f}%"}))

            # Allow download of CSV of the value and profit series
            df_out = pd.DataFrame({
                "price": price_series,
                "portfolio_value": value_series,
                "profit_vs_buy": profit_series
            })
            csv = df_out.to_csv().encode('utf-8')
            st.download_button("Download CSV (price, portfolio value, profit)", csv, f"{ticker}_portfolio.csv", "text/csv")
else:
    st.info("Enter a ticker to begin.")
