import cv2
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

image_path = r"C:\Users\Admin\Downloads\894545939a29407e74ed40a2f9123e87.jpg"

result = ocr.ocr(image_path)

image = cv2.imread(image_path)

for line in result[0]:
    box = line[0]
    text = line[1][0]
    score = line[1][1]

    points = [(int(p[0]), int(p[1])) for p in box]

    for i in range(4):
        cv2.line(
            image,
            points[i],
            points[(i + 1) % 4],
            (0, 255, 0),
            2
        )

    cv2.putText(image, f"{text} ({score:.2f})", points[0],
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 0, 0),
        2
    )

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Show
plt.figure(figsize=(12, 8))
plt.imshow(image_rgb)
plt.axis("off")
plt.show()