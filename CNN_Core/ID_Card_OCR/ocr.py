import re
import json
import easyocr
import numpy as np


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

    # Aadhaar Number Extraction
    aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    aadhar_match = re.search(aadhar_pattern, full_text)

    aadhar_number = aadhar_match.group() if aadhar_match else None

    # DOB Extraction
    dob_pattern = r'\d{2}/\d{2}/\d{4}'
    dob_match = re.search(dob_pattern, full_text)

    dob = dob_match.group() if dob_match else None

    # Gender
    gender = None

    for text in text_list:

        lower = text.lower()

        if "male" in lower:
            gender = "Male"
            break

        elif "female" in lower:
            gender = "Female"
            break

    # Name Extraction
    
    name = None

    for text in text_list:

        # Skip unwanted keywords
        if any(keyword in text.lower() for keyword in [
            "government", "india", "aadhaar", "male", "female", "dob"
        ]):
            continue

        if re.match(r'^[A-Za-z ]{3,}$', text):
            name = text
            break

    data = {
        "name": name,
        "date_of_birth": dob,
        "gender": gender,
        "aadhaar_number": aadhar_number
    }

    return json.dumps(data, indent=4)