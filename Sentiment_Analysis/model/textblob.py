from textblob import TextBlob

def textblob_sentiment(text):

    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        label = "Positive"
    elif polarity < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return label, polarity