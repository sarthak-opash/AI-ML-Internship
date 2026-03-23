import cv2
from ultralytics import YOLO

model = YOLO("yolov8m.pt") 

video_path = "stock-footage-montenegro-flying-through-the-modern-supermarket.webm"
cap = cv2.VideoCapture(video_path)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
original_fps = int(cap.get(cv2.CAP_PROP_FPS))
fps = (original_fps if original_fps > 0 else 30) * 0.5 

out = cv2.VideoWriter("output_tracked.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

people_counted = set()
frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_count += 1

    if frame_count % 2 == 0:
        continue

    results = model.track(frame, persist=True, classes=[0], conf=0.35, iou=0.5, tracker="botsort.yaml", verbose=False)

    current_in_view = 0
    if results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        current_in_view = len(boxes)

        for box, obj_id in zip(boxes, ids):
            x1, y1, x2, y2 = box

            people_counted.add(obj_id)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1 - 25), (x1 + 80, y1), (0, 255, 0), -1)
            cv2.putText(frame, f"ID: {obj_id}", (x1 + 5, y1 - 6), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (350, 100), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    cv2.putText(frame, f"Total Counted: {len(people_counted)}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, f"Currently in View: {current_in_view}", (20, 85), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    out.write(frame)

    cv2.imshow("Top-Notch Supermarket Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print("Tracking finished. Video saved as 'output_tracked.mp4'")
