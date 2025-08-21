def classify_outcome(call_data):
    """
    Classify the outcome of a call based on whether an agreed_rate exists.
    Returns: 'won', 'lost', 'no_match', 'ineligible'
    """
    if not call_data:
        return "no_match"
    elif call_data.get("agreed_rate"):
        return "won"
    else:
        return "lost"

def classify_sentiment(call_data):
    """
    Simple sentiment classification based on notes or interaction.
    Returns: 'positive', 'neutral', 'negative'
    """
    notes = call_data.get("notes", "").lower()
    if any(word in notes for word in ["thanks", "happy", "good"]):
        return "positive"
    elif any(word in notes for word in ["frustrated", "angry", "late"]):
        return "negative"
    else:
        return "neutral"