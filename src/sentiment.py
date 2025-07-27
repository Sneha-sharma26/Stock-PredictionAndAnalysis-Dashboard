import requests
from textblob import TextBlob

import os
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news_and_sentiment(ticker):
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker} stock&"
        f"sortBy=publishedAt&"
        f"language=en&"
        f"apiKey={API_KEY}"
    )

    response = requests.get(url)
    if response.status_code != 200:
        return []

    articles = response.json().get("articles", [])
    results = []

    for article in articles[:5]:  # Limit to 5 headlines
        title = article.get("title", "")
        description = article.get("description", "")
        content = f"{title}. {description}"
        polarity = TextBlob(content).sentiment.polarity
        results.append({
            "title": title,
            "sentiment": polarity
        })

    return results
