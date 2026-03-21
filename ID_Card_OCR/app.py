import json
from PIL import Image
import streamlit as st
from ocr import extract_aadhar_details

st.set_page_config(page_title="Aadhaar OCR", layout="centered")

st.title("Aadhar Text Extractor")

uploaded_file = st.file_uploader("Upload Aadhaar Card", type=["jpg","png","jpeg"])

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Aadhaar Card", use_column_width=True)

    if st.button("Extract Details"):

        result = extract_aadhar_details(image)

        data = json.loads(result)

        st.subheader("Extracted Details")
        st.json(data)