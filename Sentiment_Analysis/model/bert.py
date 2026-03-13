from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def transformer_sentiment(text):

    result = classifier(text)[0]

    label = result["label"]
    score = result["score"]

    if label == "POSITIVE":
        label = "Positive"
    else:
        label = "Negative"

    return label, score