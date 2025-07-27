import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler


def predict_next_30_days(df):
    look_back = min(60, len(df)-1)
    
    if len(df) <= look_back:
        raise ValueError(f"Not enough data to predict. Need more than {look_back} rows, got {len(df)}.")

    data = df[['Close']].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X = []
    y = []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i - look_back:i, 0])
        y.append(scaled_data[i, 0])
    X = np.array(X)
    y = np.array(y)
    
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X, y, epochs=10, batch_size=32, verbose=0)

    last_lookback = scaled_data[-look_back:]
    prediction_list = []

    for _ in range(30):
        pred_input = last_lookback[-look_back:].reshape(1, look_back, 1)
        pred_price = model.predict(pred_input, verbose=0)[0][0]
        prediction_list.append(pred_price)
        last_lookback = np.append(last_lookback, [[pred_price]], axis=0)

    predicted_prices = scaler.inverse_transform(np.array(prediction_list).reshape(-1, 1))
    return predicted_prices.flatten()
