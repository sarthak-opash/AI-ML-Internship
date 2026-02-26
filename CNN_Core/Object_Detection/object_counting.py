import cv2
import numpy
from ultralytics import YOLO
    

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("traffic.mp4")

unique_id = set()

while True:
    ret, frame = cap.read()
    result = model.track(frame, classes = [2], persist=True, verbose=False)
    annot = result[0].plot()
    if result[0].boxes.id is not None:
        id = result[0].boxes.id.cpu().numpy()
        for oid in id:
            unique_id.add(oid)
        cv2.putText(annot, f"Count: {len(unique_id)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Object Counting", annot)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()