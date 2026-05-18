import cv2
import numpy as np
from PIL import Image
# The clean, universal import pattern
from paddleocr import PaddleOCR

# Initialize PaddleOCR engine
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Valid Windows raw string path to avoid Unicode escape errors
img_path = r'C:\Users\Admin\Downloads\894545939a29407e74ed40a2f9123e87.jpg'

# Run detection and recognition
result = ocr.ocr(img_path, cls=True)

# Parse output array safely
for idx in range(len(result)):
    res = result[idx]
    if res is None: 
        continue
    for line in res:
        print("Bounding Box:", line[0])
        print("Text & Score:", line[1])
        print("-" * 30)


