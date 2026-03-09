import re
import json
import easyocr
import numpy as np

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

def extract_aadhar_details(image):

    image = np.array(image)

    # Run OCR
    results = reader.readtext(image)

    text_list = []

    for (_, text, prob) in results:
        cleaned = text.strip()
        text_list.append(cleaned)

    full_text = " ".join(text_list)

    # -------------------------
    # Aadhaar Number Extraction
    # -------------------------

    aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    aadhar_match = re.search(aadhar_pattern, full_text)

    aadhar_number = aadhar_match.group() if aadhar_match else None

    # -------------------------
    # DOB Extraction
    # -------------------------

    dob_pattern = r'\d{2}/\d{2}/\d{4}'
    dob_match = re.search(dob_pattern, full_text)

    dob = dob_match.group() if dob_match else None

    # -------------------------
    # Gender Extraction
    # -------------------------

    gender = None

    for text in text_list:

        lower = text.lower()

        if "male" in lower:
            gender = "Male"
            break

        if "female" in lower:
            gender = "Female"
            break

    stop_words = [
        "government",
        "india",
        "aadhaar",
        "uidai",
        "dob",
        "birth",
        "year",
        "male",
        "female"
    ]

    def is_valid_name(text):

        if len(text) < 3:
            return False

        if re.search(r'\d', text):
            return False

        if any(word in text.lower() for word in stop_words):
            return False

        if not re.match(r'^[A-Za-z ]+$', text):
            return False

        return True

    name = None
    target_index = None

    # Find index of DOB or Gender
    for i, text in enumerate(text_list):

        lower = text.lower()

        if "male" in lower or "female" in lower:
            target_index = i
            break

        if re.search(r'\d{2}/\d{2}/\d{4}', text):
            target_index = i
            break

    # Look above DOB/Gender
    if target_index is not None:

        for j in range(target_index - 1, -1, -1):

            candidate = text_list[j]

            if is_valid_name(candidate):
                name = candidate
                break

    # Fallback method
    if not name:

        for text in text_list:

            if is_valid_name(text):
                name = text
                break

    data = {
        "name": name,
        "date_of_birth": dob,
        "gender": gender,
        "aadhaar_number": aadhar_number
    }

    return json.dumps(data, indent=4)