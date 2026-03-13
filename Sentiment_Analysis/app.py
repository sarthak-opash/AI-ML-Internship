import pandas as pd
import streamlit as st
import plotly.express as px
from main import analyze_text

st.set_page_config(page_title="Sentiment Analysis Dashboard", layout="centered")

st.title("Sentiment Analysis")

text = st.text_area("Enter Text")

if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter text")
    else:

        result = analyze_text(text)

        st.subheader("Model Predictions")

        df = pd.DataFrame([
            ["TextBlob", result["textblob"]["label"], result["textblob"]["score"]],
            ["VADER", result["vader"]["label"], result["vader"]["score"]],
            ["Transformer", result["transformer"]["label"], result["transformer"]["score"]],
        ], columns=["Model", "Sentiment", "Confidence"])

        st.dataframe(df, use_container_width=True)

        st.subheader("Sarcasm Detection")

        sarcasm_detected = result["sarcasm"]["detected"]
        sarcasm_score = result["sarcasm"]["score"]

        if sarcasm_detected:
            st.error(f"Sarcasm Detected (Confidence: {sarcasm_score:.2f})")
        else:
            st.success(f"No Sarcasm Detected (Confidence: {sarcasm_score:.2f})")

        st.subheader("Model Confidence Comparison")

        fig = px.bar(
            df,
            x="Model",
            y="Confidence",
            color="Sentiment",
            title="Sentiment Model Comparison"
        )

        st.plotly_chart(fig, use_container_width=True)
