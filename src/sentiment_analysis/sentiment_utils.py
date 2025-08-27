def analyze_sentiment(text):
    text = text.lower()
    if any(word in text for word in ["bad", "poor", "terrible"]):
        return "negative"
    elif any(word in text for word in ["good", "great", "excellent"]):
        return "positive"
    else:
        return "neutral"