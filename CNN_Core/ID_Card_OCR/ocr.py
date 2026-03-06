import re
import json
import easyocr
import numpy as np

reader = easyocr.Reader(['en'])

def extract_aadhar_details(image):

    image = np.array(image)

    results = reader.readtext(image)

    text_list = []
    for (_, text, prob) in results:
        cleaned = text.strip()
        text_list.append(cleaned)

    full_text = " ".join(text_list)

    aadhar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    aadhar_match = re.search(aadhar_pattern, full_text)

    aadhar_number = aadhar_match.group() if aadhar_match else None

    dob_pattern = r'\d{2}/\d{2}/\d{4}'
    dob_match = re.search(dob_pattern, full_text)

    dob = dob_match.group() if dob_match else None


    gender = None
    name = None

    for i, text in enumerate(text_list):

        if any(keyword in text.lower() for keyword in [
            "government", "india", "aadhaar", "male", "female", "dob"
        ]):
            continue

        if re.match(r'^[A-Za-z ]{3,}$', text):
            if dob and i < len(text_list):
                name = text
                
            if not dob and i > len(text_list):
                gender = text

            if not dob:
                name = text
                break

    data = {
        "name": name,
        "date_of_birth": dob,
        "aadhaar_number": aadhar_number,
        "gender": gender
    }
    
    return json.dumps(data, indent=4)