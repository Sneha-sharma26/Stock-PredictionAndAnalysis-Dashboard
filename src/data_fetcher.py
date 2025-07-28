import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_data(tickers=["AAPL", "MSFT", "AMZN", "META", "JPM", "INFY"], start_date="2020-01-01", end_date=None):
    """Fetch stock data from Yahoo Finance."""
    start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
    end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d') if end_date else datetime.today().strftime('%Y-%m-%d')

    all_data = {}
    for ticker in tickers:
        try:
            yf_ticker = yf.Ticker(ticker)
            df = yf_ticker.history(start=start_date, end=end_date, auto_adjust=True)
            if df.empty:
                raise ValueError(f"No data found for ticker '{ticker}'. It may be delisted or invalid.")
            else:
                all_data[ticker] = df
        
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return all_data

# Example usage:
if __name__ == "__main__":
    tickers=["AAPL", "MSFT", "AMZN", "META", "JPM", "INFY"]
    data_dict = fetch_stock_data(tickers)
    
    if data_dict:
        for ticker, df in data_dict.items():
            df.to_csv("data/stock_data.csv")
            print(f"{ticker} Data Sample:")
            print(df.head())
    else:
        print("❗ No data fetched for any ticker.")