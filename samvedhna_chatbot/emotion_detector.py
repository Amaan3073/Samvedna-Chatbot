from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

def detect_emotion(text):
    lowered = text.lower().strip()
    greetings = ["hi", "hello", "hey", "how are you", "good morning", "good evening", "good afternoon","good night","namaste"]

    if lowered in greetings:
        return "greeting", 0.9

    score = sid.polarity_scores(text)['compound']

    # Keyword override
    if "confused" in lowered:
        return "confused", score
    if score > 0.5:
        return "happy", score
    elif 0 < score <= 0.5:
        return "confused", score
    elif score == 0:
        return "neutral", score
    elif -0.5 <= score < 0:
        return "sad", score
    else:
        return "angry", score
