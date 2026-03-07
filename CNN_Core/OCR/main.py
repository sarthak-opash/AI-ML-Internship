import cv2
import re 
import easyocr
from ultralytics import YOLO 
from collections import defaultdict, deque

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="'pin_memory' argument is set as true but no accelerator is found")

model = YOLO("best.pt")
# enable GPU for OCR when available (speeds up recognition if CUDA is present)
import torch
use_gpu = torch.cuda.is_available()
reader = easyocr.Reader(['en'], gpu=use_gpu)

plate_pattern = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z]{3}$")


# correction in extracted value for similar looking digits and alphabet
def correct_plate_platform(ocr_text):
    mapping_num_to_alpha = {"0":"O", "5":"S", "1":"I", "8":"B", "2":"Z"}
    mapping_alpha_to_num = {"0":"0", "S":"5", "I":"1", "B":"8", "Z":"2"}
    
    ocr_text = ocr_text.upper().replace(" ", "")
    if len(ocr_text) > 7:
        return ""  # too long, invalid plate
    
    corrected = []
    for i, ch in enumerate(ocr_text):
        if i < 2 or i >= 4:
            if ch.isdigit() and ch in mapping_num_to_alpha:
                corrected.append(mapping_num_to_alpha[ch])
            elif ch.isalpha():
                corrected.append(ch)
            else:
                return ""
        else:
            if ch.isalpha() and ch in mapping_alpha_to_num:
                corrected.append(mapping_alpha_to_num[ch])
            elif ch.isdigit():
                corrected.append(ch)
            else:
                return ""
    return "".join(corrected) if len(corrected) == 7 else ""

# Recognizing a number plate by upscaling the image 

def recognize_plate(plate_crop):
    if plate_crop.size == 0:
        return ""
    # preprocessing the ocr 
    gray = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    plate_resized = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    try:
        ocr_result = reader.readtext(
            plate_resized, detail=0, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
        if len(ocr_result) > 0:
            candidate = correct_plate_platform(ocr_result[0])
            if candidate and plate_pattern.match(candidate):
                return candidate
    except:
        pass
    return ""
    
# number stabilization buffer

plate_history = defaultdict(lambda: deque(maxlen = 10))
plate_final = {}
# last 10 prediction per box
def get_box_id(x1, y1, x2, y2):
    return f"{int(x1/10)}_{int(y1/10)}_{int(x2/10)}_{int(y2/10)}"
def get_stable_plate(box_id, new_text):
    if new_text:
        plate_history[box_id].append(new_text)
        # Majority vote
        most_common = max(set(plate_history[box_id]),
        key = plate_history[box_id].count)
        plate_final[box_id] = most_common
    return plate_final.get(box_id, "")

# input

input_video = "vehicle_video.mp4"
output_video = "output_with_licence.mp4"

cap = cv2.VideoCapture(input_video)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
fourcc = cv2.VideoWriter.fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, cap.get(cv2.CAP_PROP_FPS), (int(cap.get(3)), int(cap.get(4))))

CONF_THRESH = 0.3
FRAME_SKIP = 2  # perform OCR every N frames to save time
frame_count = 0

# Operating frame by frame

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    h, w = frame.shape[:2]
    target_size = 640
    scale = 1.0
    if max(h, w) > target_size:
        scale = target_size / max(h, w)
        small = cv2.resize(frame, (int(w * scale), int(h * scale)))
    else:
        small = frame

    results = model(small)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            conf = float(box.conf.cpu().numpy().item())
            if conf < CONF_THRESH:
                continue
            # xyxy format is [x1, y1, x2, y2]
            coords = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, coords / scale)
            plate_crop = frame[y1:y2, x1:x2]

            # ocr with correction (skip some frames to reduce load)
            text = ""
            if frame_count % FRAME_SKIP == 0:
                text = recognize_plate(plate_crop)
            box_id = get_box_id(x1, y1, x2, y2)
            stable_text = get_stable_plate(box_id, text)

            # draw bounding box on original frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            # overlay zoomed-in plate and text
            if plate_crop.size > 0:
                overlay_h, overlay_w = 150, 400
                plate_resized = cv2.resize(plate_crop, (overlay_w, overlay_h))

                oy1 = max(0, y1 - overlay_h - 40)
                ox1 = x1
                oy2, ox2 = oy1 + overlay_h, ox1 + overlay_w

                if oy2 <= frame.shape[0] and ox2 <= frame.shape[1]:
                    frame[oy1:oy2, ox1:ox2] = plate_resized
                if stable_text:
                    cv2.putText(frame, stable_text, (ox1, oy1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 0), 9)
                    cv2.putText(frame, stable_text, (ox1, oy1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

    out.write(frame)
    try:
        cv2.imshow("License Plate Recognition", frame)  
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except cv2.error:
        pass
    
cap.release()
out.release()

try:
    cv2.destroyAllWindows()
except cv2.error:
    pass

print("Processing completed. Output saved as", output_video)

