import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt") # selecting a specific yolo model and n stand for small yolo model model not a whole model

image = cv2.imread("robert_01.jpg")
results = model(image)
annotated_image = results[0].plot()
cv2.imshow("Result", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows() 