"""
For text analysis.

Available methods:
- `analyze_sentiment(text)`: Analyze the sentiment of the input text using NLTK's SentimentIntensityAnalyzer.
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text):
    """
    Analyze the sentiment of the input text using NLTK's SentimentIntensityAnalyzer.

    Sentiment analysis assesses the emotional tone of a text, providing a sentiment
    score ranging from -1 (negative) to 1 (positive).
    
    Parameters:
    - `text` (str): The input text to be analyzed.

    Returns:
    - `float`: The sentiment score ranging from -1 (negative) to 1 (positive).
    """
    try:
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(text)
        sentiment_score = sentiment_scores['compound']
        return sentiment_score
    except Exception as e:
        print(f"An error occurred during sentiment analysis: {str(e)}")
        return 0.0