import cv2
from ultralytics import YOLO

# 1. Top-Notch Detection: Upgraded to "yolov8m.pt" (Medium) which is highly accurate
model = YOLO("yolov8m.pt") 

# 2. Open Video Source
video_path = "stock-footage-montenegro-flying-through-the-modern-supermarket.webm"
cap = cv2.VideoCapture(video_path)

# 3. Setup Video Writer to save the tracked video in the same directory
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
original_fps = int(cap.get(cv2.CAP_PROP_FPS))
fps = (original_fps if original_fps > 0 else 30) // 2  # Halved FPS because we skip every 2nd frame

out = cv2.VideoWriter("output_tracked.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

people_counted = set()
frame_count = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_count += 1
    
    # 4. Skip every other frame (process 1, skip 1) for better performance 
    if frame_count % 2 == 0:
        continue

    # 5. Tracking with tuned accuracy parameters (conf=0.35, iou=0.5)
    results = model.track(frame, persist=True, classes=[0], conf=0.35, iou=0.5, tracker="botsort.yaml", verbose=False)

    # 6. Process tracking results
    current_in_view = 0
    if results[0].boxes is not None and results[0].boxes.id is not None:
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        current_in_view = len(boxes)

        for box, obj_id in zip(boxes, ids):
            x1, y1, x2, y2 = box
            
            # Auto-count unique IDs
            people_counted.add(obj_id)

            # Draw bounding box with a solid background for the text ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1 - 25), (x1 + 80, y1), (0, 255, 0), -1)
            cv2.putText(frame, f"ID: {obj_id}", (x1 + 5, y1 - 6), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # 7. Display Total Count and Current In View
    # Added a black semi-transparent box behind the text so it's always readable
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (350, 100), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    cv2.putText(frame, f"Total Counted: {len(people_counted)}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    cv2.putText(frame, f"Currently in View: {current_in_view}", (20, 85), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Save the frame to the output video
    out.write(frame)

    # Display on screen
    cv2.imshow("Top-Notch Supermarket Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print("Tracking finished. Video saved as 'output_tracked.mp4'")
