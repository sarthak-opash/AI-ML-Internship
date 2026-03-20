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

    # -------------------------
    # Name Extraction Logic
    # -------------------------

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

        text = text.strip()
        if len(text) < 4:
            return False
        if not text or not text[0].isupper():
            return False
        reject_garbage = {"yok", "YOK", "yol", "YOL", "bok", "BOK", "yoy", "voy"}
        if text.upper() in reject_garbage:
            return False

        if re.search(r'\d', text):
            return False

        if any(word in text.lower() for word in stop_words):
            return False

        if not re.match(r'^[A-Za-z ]+$', text):
            return False

        # Prefer reasonable names: multi-word or sufficiently long
        words = [w for w in text.split() if w]
        if len(words) == 1 and len(text) < 6:
            return False

        return True

    name = None
    target_index = None

    # Find index of DOB, Gender or NAME label (search above label)
    for i, text in enumerate(text_list):

        lower = text.lower()

        if any(kw in lower for kw in ["male", "female", "name"]):
            target_index = i
            break

        if re.search(r'\d{2}/\d{2}/\d{4}', text):
            target_index = i
            break

    # Look above DOB/Gender/NAME (limited to recent 5 texts to avoid wrong matches)
    if target_index is not None:

        search_start = max(0, target_index - 5)
        for j in range(target_index - 1, search_start - 1, -1):

            candidate = text_list[j]

            if is_valid_name(candidate):
                name = candidate
                break

    # Improved fallback: pick highest scoring valid name
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

