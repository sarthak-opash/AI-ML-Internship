import os
from transformers import pipeline

# os.environ["HF_TOKEN"] = "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"

sarcasm_classifier = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-irony",
    device=-1
)

THRESHOLD = 0.80

def detect_sarcasm(text):

    if len(text.split()) < 3:
        return False, 0

    result = sarcasm_classifier(text)[0]

    label = result["label"]
    score = result["score"]

    if label.lower() == "irony" and score > THRESHOLD:
        return True, score
    else:
        return False, score