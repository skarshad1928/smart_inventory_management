def analyze_sentiment(text: str) -> str:
    """
    Analyze sentiment of given review text.
    Returns: 'positive', 'negative', or 'neutral'
    """

    if not text or not isinstance(text, str):
        return "neutral"

    text = text.lower()

    positive_keywords = [
        "good", "excellent", "great", "amazing", "awesome",
        "love", "fantastic", "perfect", "satisfied", "happy"
    ]

    negative_keywords = [
        "bad", "worst", "poor", "terrible", "awful",
        "hate", "defective", "broken", "damaged", "disappointed"
    ]

    positive_score = sum(word in text for word in positive_keywords)
    negative_score = sum(word in text for word in negative_keywords)

    if positive_score > negative_score:
        return "positive"
    elif negative_score > positive_score:
        return "negative"
    else:
        return "neutral"
