from model.vader import vader_sentiment
from model.sarcasm import detect_sarcasm
from model.preprocessing import clean_text
from model.bert import transformer_sentiment
from model.textblob import textblob_sentiment

def adjust_for_sarcasm(label, sarcasm):

    if sarcasm:

        if label == "Positive":
            return "Negative"

        if label == "Negative":
            return "Positive"

    return label


def analyze_text(text):

    text = clean_text(text)

    sarcasm_detected, sarcasm_score = detect_sarcasm(text)

    tb_label, tb_score = textblob_sentiment(text)
    vd_label, vd_score = vader_sentiment(text)
    tr_label, tr_score = transformer_sentiment(text)

    tb_label = adjust_for_sarcasm(tb_label, sarcasm_detected)
    vd_label = adjust_for_sarcasm(vd_label, sarcasm_detected)
    tr_label = adjust_for_sarcasm(tr_label, sarcasm_detected)

    result = {
        "textblob": {"label": tb_label, "score": tb_score},
        "vader": {"label": vd_label, "score": vd_score},
        "transformer": {"label": tr_label, "score": tr_score},
        "sarcasm": {
            "detected": sarcasm_detected,
            "score": sarcasm_score
        }
    }

    return result