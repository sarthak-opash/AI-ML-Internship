import cv2
import pickle
from tkinter import Tk, filedialog
from sklearn.metrics.pairwise import cosine_distances
from utils.embedding_utils import get_face_embedding
from utils.csv_utils import mark_attendance

with open("embeddings/face_embeddings.pkl", "rb") as f:
    known_faces = pickle.load(f)

root = Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

if file_path:
    image = cv2.imread(file_path)

    embedding, box = get_face_embedding(image)

    if embedding is None:
        print("No Face Detected")
        exit()

    distances = []

    for emp_id, emp_name, known_embedding in known_faces:
        dist = cosine_distances([embedding], [known_embedding])[0][0]
        distances.append((dist, emp_id, emp_name))

    best_dist, emp_id, emp_name = min(distances)

    if best_dist < 0.5:
        mark_attendance(emp_id, emp_name)
        print(f"Attendance Marked for {emp_name}")
    else:
        print("Not an Employee")