import cv2 
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

vid = cv2.VideoCapture("traffic.mp4")

while True:
    ret, frame = vid.read()
    result = model(frame)
    annot = result[0].plot()
    cv2.imshow("Object Detection", annot)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vid.release()
cv2.destroyAllWindows()