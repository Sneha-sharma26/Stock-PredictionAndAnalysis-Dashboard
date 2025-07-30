import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
from data_fetcher import fetch_stock_data
from preprocess import preprocess_data
from sentiment import fetch_news_and_sentiment
from lstm_model import predict_next_30_days

# ---- Streamlit Setup ----
st.set_page_config(layout="wide")
st.title("Stock Prediction and Analysis Dashboard")

# ---- Sidebar Controls ----
tickers = ["AAPL", "MSFT", "AMZN", "META", "JPM", "INFY"]
selected_tickers = st.sidebar.multiselect("Select Stock Symbols", tickers, default=["AAPL"])
today = datetime.date.today()
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1), max_value = today)
end_date = st.sidebar.date_input("End Date", value = today, max_value = today)

start_date_str = pd.to_datetime(start_date).strftime('%Y-%m-%d')
end_date_str = pd.to_datetime(end_date).strftime('%Y-%m-%d')

# ---- Load Data ----
@st.cache_data
def load_data(tickers, start_date, end_date):
    raw_data = fetch_stock_data(tickers, start_date=start_date, end_date=end_date)
    if not raw_data:
        return {}
    return {ticker: preprocess_data(df, ticker) for ticker, df in raw_data.items()}

data_dict = load_data(selected_tickers, start_date, end_date)

if not data_dict:
    st.error("❗ No data fetched. Check tickers or date range.")
    st.stop()

# ---- Tabs ----
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Price Analysis", "📊 Technical Indicators", "📉 Daily Returns", "📰 News Sentiment", "🧩 Predict for next 30 Days"])

# ---- Price Analysis ----
with tab1:
    for ticker in selected_tickers:
        df = data_dict.get(ticker)
        if ticker not in data_dict:
            st.warning(f"⚠ No data for {ticker}.")
            continue
        df = data_dict[ticker]

        # Edited header to reflect data 
        st.subheader(f"{ticker} Price Chart")
        st.caption("Chart Type: Candlestick | Indicators: Close Price, 20-Day Moving Average, Bollinger Bands")

        fig = go.Figure()

        if all(col in df.columns for col in ["Open", "High", "Low", "Close_AAPL"]):
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close_AAPL"],
                name="Candlestick"
            ))
        else:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[f"Close_{ticker}"],
                name="Close Price",
                line=dict(color='blue', width=2)
            ))

        # 20-day Moving Average
        if "20_MA" in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["20_MA"],
                name="20-Day MA",
                line=dict(color='orange', width=2)
            ))

        # Bollinger Bands
        if "Upper_BB" in df.columns and "Lower_BB" in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Upper_BB"],
                name="Upper BB",
                line=dict(color='red', dash='dash')))
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df["Lower_BB"],
                name="Lower BB",
                line=dict(color='green', dash='dash')))

        # Volume as bar chart on secondary y-axis
        if "Volume" in df.columns:
            fig.add_trace(go.Bar(
                x=df.index,
                y=df["Volume"],
                name="Volume",
                marker_color='rgba(0, 123, 255, 0.6)',
                yaxis="y2",
                opacity=0.9))
            fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Volume'))

        # Highlight latest close
        if len(df) > 0:
            latest_date = df.index[-1]
            latest_close = df[f"Close_{ticker}"].iloc[-1]
            fig.add_trace(go.Scatter(
                x=[latest_date],
                y=[latest_close],
                mode="markers+text",
                marker=dict(color="gold", size=12),
                text=[f"{latest_close:.2f}"],
                textposition="top center",
                name="Latest Close"))

        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            legend_title="Legend",
            title= f"{ticker} Price Chart (Close Price, Moving Average, Bollinger Bands)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Show current and previous close as metrics
        current_close = df[f"Close_{ticker}"].iloc[-1] if len(df) >= 1 else None
        previous_close = df[f"Close_{ticker}"].iloc[-2] if len(df) >= 2 else None
        if current_close is not None and previous_close is not None:
            st.metric(
                "Current Price",
                f"${current_close.item():.2f}",
                delta=f"{(current_close.item() - previous_close.item()):.2f}"
            )

# ---- Technical Indicators ----
with tab2:
    for ticker in selected_tickers:
        if ticker not in data_dict:
            continue
        df = data_dict[ticker]
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{ticker} Relative Strength Index (RSI)")
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI", line=dict(color='purple')))
            fig_rsi.add_hline(y=70, line_dash="dot", annotation_text="Overbought", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dot", annotation_text="Oversold", line_color="green")
            fig_rsi.update_layout(template="plotly_white")
            st.plotly_chart(fig_rsi, use_container_width=True)
        with col2:
            st.subheader("MACD")
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name="MACD", line=dict(color='blue')))
            fig_macd.add_trace(go.Scatter(x=df.index, y=df['Signal_Line'], name="Signal Line", line=dict(color='red')))
            fig_macd.update_layout(template="plotly_white")
            st.plotly_chart(fig_macd, use_container_width=True)

# ---- Daily Returns ----
with tab3:
    for ticker in selected_tickers:
        if ticker not in data_dict:
            continue
        df = data_dict[ticker]
        st.subheader(f"{ticker} Daily Returns")
        st.line_chart(df['Daily_Return'])
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Latest Daily Return", f"{df['Daily_Return'].iloc[-1]:.2%}")
        with col2:
            st.metric("Average Daily Return", f"{df['Daily_Return'].mean():.2%}")

# ---- News Sentiment ----
with tab4:
    for ticker in selected_tickers:
        st.subheader(f"{ticker} News Sentiment")
        sentiment_list = fetch_news_and_sentiment(ticker)
        if sentiment_list:
            sentiment_values = [s['sentiment'] for s in sentiment_list if 'sentiment' in s]
            if sentiment_values:
                avg_sentiment = sum(sentiment_values) / len(sentiment_values)
                if avg_sentiment > 0.1:
                    st.success(f"Average Sentiment: Positive  ({avg_sentiment:.2f})")
                elif avg_sentiment < -0.1:
                    st.error(f"Average Sentiment: Negative  ({avg_sentiment:.2f})")
                else:
                    st.info(f"Average Sentiment: Neutral ({avg_sentiment:.2f})")
            
                st.markdown("---")
                st.markdown("### Latest Headlines")
                for news in sentiment_list:
                    title = news.get('title', 'No Title')
                    sentiment = news.get('sentiment', 0)
                    if sentiment > 0.1:
                        st.success(f"📰 {title} — (+{sentiment:.2f})")
                    elif sentiment < -0.1:
                        st.error(f"📰 {title} — ({sentiment:.2f})")
                    else:
                        st.info(f"📰 {title} — ({sentiment:.2f})")
            
            else:
                st.warning("No valid sentiment scores found.")
        else:
            st.warning("No sentiment data available.")


# Prediction Tab
if "show_prediction" not in st.session_state:
    st.session_state["show_prediction"] = False
    
# ---- Sidebar Buttons ----
if st.sidebar.button("Predict Next 30 Days"):
    st.session_state["show_prediction"] = True
    st.session_state["prediction_started"] = True

# reset flag when prediction is done or reset
if st.sidebar.button("Reset Prediction"):
    st.session_state["show_prediction"] = False
    st.session_state["prediction_started"] = False
    
with tab5:
    if st.session_state.get("prediction_started", False):
        st.info("Your prediction has started.")
        st.session_state["prediction_started"] = False 
    
    if st.session_state.get("show_prediction", False):
        st.markdown("## 🧩 Prediction Results")
        for ticker in selected_tickers:
            st.subheader(f"{ticker} — 30-Day Price Forecast")
            df = data_dict.get(ticker)
            if df is None or len(df) < 61:
                st.warning(f"❗ Not enough historical data for {ticker} to generate a 30-day prediction. "
                "At least 61 days of price history are required. "
                "Try selecting an earlier start date in the sidebar.")
                continue
            with st.spinner(f"Training LSTM for {ticker}..."):
                try:
                    df_for_pred = df.rename(columns={f"Close_{ticker}": "Close"})
                    # predicted_prices,rmse, mae = predict_next_30_days(df_for_pred)
                    predicted_prices = predict_next_30_days(df_for_pred)
                except Exception as e:
                    st.error(f"Error predicting for {ticker}: {str(e)}")
                    continue

            # # prediction accuracy
            # st.success(f"📊 Prediction Model Evaluation for {ticker}:")
            # st.markdown(f"- **RMSE** (Root Mean Squared Error): `{rmse:.2f}`")
            # st.markdown(f"- **MAE** (Mean Absolute Error): `{mae:.2f}`")

            future_dates = pd.date_range(df.index[-1] + pd.Timedelta(days=1), periods=30)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df[f'Close_{ticker}'], name="Historical Close", line=dict(width=2)))
            fig.add_trace(go.Scatter(x=future_dates, y=predicted_prices, name="Predicted Close (30 Days)",line=dict(dash='dash', width=2)))
            fig.update_layout(template="plotly_white", title=f"{ticker} — Forecast vs Historical",xaxis_title="Date", yaxis_title="Price (USD)", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

st.caption(f"Data from Yahoo Finance | Last Updated: {pd.to_datetime('today').strftime('%Y-%m-%d')}")
