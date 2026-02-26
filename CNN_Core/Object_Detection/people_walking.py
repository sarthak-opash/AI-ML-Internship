from collections import defaultdict, deque

import cv2  
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("walking_master.mp4")

id_map = {}
next_id = 1

trail = defaultdict(lambda: deque(maxlen=30))
apper = defaultdict(int)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    result = model.track(frame, classes = [0], persist = True)
    annot = result[0].plot()
    
    if result[0].boxes.id is not None:
        boxes = result[0].boxes.xyxy.numpy()
        ids = result[0].boxes.id.cpu().numpy()
        
        for box, oid in zip(boxes, ids):
            x1, y1, x2, y2 = map(int, box)
            c1, c2 = (x1 + x2) // 2, (y1 + y2) // 2
            apper[oid] += 1
            
            if oid not in id_map:
                id_map[oid] = len(id_map) + 1
            
            sid = id_map[oid]
            trail[sid].append((c1, c2))
            cv2.rectangle(annot, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annot, f"ID: {sid}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 0), 2)
            cv2.circle(annot, (c1, c2), 5, (0, 255, 0), -1)
            for i in range(1, len(trail[sid])):
                cv2.line(annot, trail[sid][i-1], trail[sid][i], (0, 255, 0), 2)
    cv2.imshow("People Walking Detection", annot)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()