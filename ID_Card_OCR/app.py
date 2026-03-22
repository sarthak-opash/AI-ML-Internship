"""
Streamlit entrypoint for ID Card OCR (Aadhaar extractor).
Libraries: streamlit, Pillow — OCR logic and deps are in ocr.py.
"""

import json

import streamlit as st
from PIL import Image

from ocr import extract_aadhar_details

st.set_page_config(page_title="Aadhaar OCR", layout="centered")

st.title("Aadhaar ID — text extractor")

st.markdown(
    """
### About this project
This app uploads an **Aadhaar card image** and extracts **Name**, **date of birth**,
**gender**, and the **12-digit Aadhaar number** using OCR, then shows the result as JSON.

**Libraries used**
- **Streamlit** — web UI and file upload  
- **Pillow (PIL)** — open and display images  
- **EasyOCR** — text detection and recognition  
- **NumPy** — image arrays;

"""
)

uploaded_file = st.file_uploader("Upload Aadhaar Card", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Aadhaar Card", use_container_width=True)

    if st.button("Extract Details"):
        result = extract_aadhar_details(image)
        data = json.loads(result)
        st.subheader("Extracted Details")
        st.json(data)
