# 📈 Stock Prediction & Analysis Dashboard

An interactive, ML-powered dashboard built with **Streamlit** for analyzing stock market trends, performing technical analysis, visualizing market sentiment, and forecasting prices using an LSTM model.

---

## 🚀 Live App

[🔗 Click here to launch the app]()

---

## 🧠 Features

### ✅ Stock Price Analysis
- Candlestick chart with 20-day Moving Average and Bollinger Bands
- Latest close price marked clearly
- Metrics for current and previous close

### ✅ Technical Indicators
- **RSI (Relative Strength Index)** with overbought/oversold thresholds
- **MACD & Signal Line** plots

### ✅ Daily Returns
- Visualize daily return %
- Displays average and most recent return

### ✅ News Sentiment Analysis
- Fetches latest stock-related headlines from NewsAPI
- Analyzes sentiment using **TextBlob**
- Summarizes overall sentiment (Positive / Negative / Neutral)

### ✅ LSTM-Based Forecasting
- Predicts next 30 days of closing prices
- Built using a 2-layer LSTM model with TensorFlow
- Historical vs Predicted line chart

---

## 📦 Installation

### 1. Clone the Repository
```
git clone https://github.com/Sneha-sharma26/Stock-PredictionAndAnalysis-Dashboard.git
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Add Your NewsAPI Key
Create a .streamlit/secrets.toml file:

```toml
NEWS_API_KEY = "your_news_api_key"
```

You can get your API key from: https://newsapi.org

### 4. Run the App
```
streamlit run src/app.py
```

---


## 🧰 Tech Stack

| Layer         | Tool / Library          |
| ------------- | ----------------------- |
| UI & Layout   | Streamlit               |
| Data Fetching | yfinance (Yahoo API)    |
| Plotting      | Plotly                  |
| ML Model      | LSTM (TensorFlow/Keras) |
| Sentiment     | NewsAPI + TextBlob      |
| ML Utils      | scikit-learn            |

---

## 🙋‍♀️ Author
Sneha Sharma

💻 GitHub: https://github.com/Sneha-sharma26

🔗 LinkedIn: https://www.linkedin.com/in/sneha-sharma-5191092b8/

---

## 📃 License

This project is open-source under the **MIT License**.  
Feel free to use, share, or extend it!
