from sklearn.linear_model import LinearRegression
import numpy as np

def train_linear_regression(X, y):
    """Train a simple linear regression model."""
    model = LinearRegression()
    model.fit(X, y)
    return model

def prepare_features(df):
    """Create features (past prices) and target (next day close)."""
    X = df[['Open', 'High', 'Low', 'Volume']][:-1]
    y = df['Close'].shift(-1).dropna()
    return X, y
