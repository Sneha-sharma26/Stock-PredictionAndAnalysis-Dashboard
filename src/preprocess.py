import pandas as pd

def preprocess_data(df, ticker=None):
    """Clean and add features to stock data including Daily Return, Bollinger Bands, RSI, and MACD."""
    
    # 1. Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip('_') for col in df.columns.values]

    # 2. Ensure Date is datetime and set as index (if not already)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

    # Use the correct close column
    close_col = 'Close'
    if ticker and f'Close_{ticker}' in df.columns:
        close_col = f'Close_{ticker}'
    elif 'Close_AAPL' in df.columns:
        close_col = 'Close_AAPL'

    # 3. Add Daily Return
    df['Daily_Return'] = df[close_col].pct_change()

    # 4. Add Bollinger Bands
    df['20_MA'] = df[close_col].rolling(window=20).mean()
    df['20_STD'] = df[close_col].rolling(window=20).std()
    df['Upper_BB'] = df['20_MA'] + (df['20_STD'] * 2)
    df['Lower_BB'] = df['20_MA'] - (df['20_STD'] * 2)

    # 5. RSI
    delta = df[close_col].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # 6. MACD
    df['12_EMA'] = df[close_col].ewm(span=12, adjust=False).mean()
    df['26_EMA'] = df[close_col].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['12_EMA'] - df['26_EMA']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df