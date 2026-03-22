import re
import json
import easyocr
import numpy as np
import streamlit as st

@st.cache_resource
def get_reader():
    """Cached EasyOCR reader for Streamlit deploy (CPU only to avoid GPU issues)."""
    return easyocr.Reader(['en'], gpu=False)

def extract_aadhar_details(image):
    """Extract Aadhaar details with error handling for deploy."""
    image = np.array(image)
    
    try:
        # Run OCR with cached reader
        results = get_reader().readtext(image)
    except Exception as e:
        st.error(f"OCR failed: {str(e)}. Try smaller image or local run.")
        return json.dumps({
            "error": "OCR unavailable",
            "name": None,
            "date_of_birth": None,
            "gender": None,
            "aadhaar_number": None
        }, indent=4)

    text_list = []
    for (_, text, prob) in results:
        cleaned = text.strip()
        text_list.append(cleaned)

    full_text = " ".join(text_list)

    # Aadhaar Number Extraction
    aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    aadhar_match = re.search(aadhar_pattern, full_text)
    aadhar_number = aadhar_match.group() if aadhar_match else None

    # DOB Extraction
    dob_pattern = r'\d{2}/\d{2}/\d{4}'
    dob_match = re.search(dob_pattern, full_text)
    dob = dob_match.group() if dob_match else None

    # Gender Extraction
    gender = None
    full_text_lower = full_text.lower()
    if re.search(r'\b(female|femal|femaie|femle)\b', full_text_lower):
        gender = "Female"
    elif re.search(r'\b(male|maie|nale)\b', full_text_lower):
        gender = "Male"
    elif "female" in full_text_lower:
        gender = "Female"
    elif "male" in full_text_lower:
        gender = "Male"

    # Name Extraction Logic
    stop_words = [
        "government", "india", "aadhaar", "uidai", "dob", "birth", "year", "male", "female"
    ]

    def is_valid_name(text):
        text = text.strip()
        if len(text) < 4:
            return False
        if not text or not text[0].isupper():
            return False
        reject_garbage = {"yok", "YOK", "yol", "YOL", "bok", "BOK", "yoy", "voy"}
        if text.upper().strip() in reject_garbage:
            return False
        if re.search(r'\d', text):
            return False
        if any(word in text.lower() for word in stop_words):
            return False
        if not re.match(r'^[A-Za-z ]+$', text):
            return False
        words = [w for w in text.split() if w]
        if len(words) == 1 and len(text) < 6:
            return False
        return True

    name = None
    target_index = None

    # Find target index (NAME label, gender, DOB)
    for i, text in enumerate(text_list):
        lower = text.lower()
        if any(kw in lower for kw in ["male", "female", "name"]):
            target_index = i
            break
        if re.search(r'\d{2}/\d{2}/\d{4}', text):
            target_index = i
            break

    # Search above target (limited range)
    if target_index is not None:
        search_start = max(0, target_index - 5)
        for j in range(target_index - 1, search_start - 1, -1):
            candidate = text_list[j]
            if is_valid_name(candidate):
                name = candidate
                break

    # Scored fallback
    if not name:
        candidates = []
        for idx, text in enumerate(text_list):
            if is_valid_name(text):
                words_cnt = len([w for w in text.split() if w])
                score = (words_cnt * 15) + len(text) - (idx * 0.5)
                candidates.append((score, text))
        if candidates:
            candidates.sort(reverse=True)
            name = candidates[0][1]

    data = {
        "name": name,
        "date_of_birth": dob,
        "gender": gender,
        "aadhaar_number": aadhar_number
    }

    return json.dumps(data, indent=4)
