import cv2
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_distances
from utils.embedding_utils import get_face_embedding
from utils.csv_utils import mark_attendance

with open("embeddings/face_embeddings.pkl", "rb") as f:
    known_faces = pickle.load(f)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    embedding, box = get_face_embedding(frame)

    if embedding is not None:
        distances = []

        for emp_id, emp_name, known_embedding in known_faces:
            dist = cosine_distances([embedding], [known_embedding])[0][0]
            distances.append((dist, emp_id, emp_name))

        best_dist, emp_id, emp_name = min(distances)

        x, y, w, h = box

        if best_dist < 0.5:
            mark_attendance(emp_id, emp_name)
            label = f"{emp_name} ({emp_id})"
            color = (0, 255, 0)
        else:
            label = "Not Employee"
            color = (0, 0, 255)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Webcam Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()