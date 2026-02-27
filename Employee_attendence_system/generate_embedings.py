import os
import cv2
import pickle
from utils.embedding_utils import get_face_embedding

DATASET_DIR = "Employee_Data"
OUTPUT_FILE = "embeddings/face_embeddings.pkl"

os.makedirs("embeddings", exist_ok=True)

all_embeddings = []

for person in os.listdir(DATASET_DIR):
    person_path = os.path.join(DATASET_DIR, person)

    if not os.path.isdir(person_path):
        continue

    try:
        emp_id, emp_name = person.split("_", 1)
    except:
        print("Folder name must be EMPID_NAME")
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        image = cv2.imread(img_path)

        if image is None:
            continue

        embedding, _ = get_face_embedding(image)

        if embedding is not None:
            all_embeddings.append((emp_id, emp_name, embedding))

print(f"Total Embeddings: {len(all_embeddings)}")

with open(OUTPUT_FILE, "wb") as f:
    pickle.dump(all_embeddings, f)

print("Embeddings Saved Successfully")