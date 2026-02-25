
import cv2
import pickle
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from mtcnn import MTCNN
from keras_facenet import FaceNet
from sklearn.metrics.pairwise import cosine_distances
from csv_utils import mark_attendance

# Load models
detector = MTCNN()
embedder = FaceNet()

# Load known embeddings
with open("embeddings/face_embeddings.pkl", "rb") as f:
    known_faces = pickle.load(f)

THRESHOLD = 0.6
camera_url = 0  # CHANGE IP

cap = None
running = False

# GUI Window
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("900x700")

label = tk.Label(root)
label.pack()

status = tk.Label(root, text="Status: Idle", font=("Arial", 12))
status.pack(pady=10)

def process_frame(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(rgb)

    for face in faces:
        x, y, w, h = face['box']
        face_img = rgb[y:y+h, x:x+w]
        if face_img.size == 0: continue
        face_img = cv2.resize(face_img, (160, 160))

        embedding = embedder.embeddings([face_img])[0]
        distances = [(cosine_distances([embedding], [k[2]])[0][0], k[0], k[1]) for k in known_faces]
        
        if distances:
            dist, emp_id, emp_name = min(distances)
            if dist < THRESHOLD:
                mark_attendance(emp_id, emp_name)
                text = f"{emp_name} ({emp_id})"
            else:
                text = "Unknown"
        else:
            text = "Unknown"

        cv2.rectangle(rgb, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(rgb, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

    img = Image.fromarray(rgb)
    img = ImageTk.PhotoImage(img)
    label.config(image=img)
    label.image = img

def start_camera():
    global cap, running
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        status.config(text="Status: Camera Not Detected. Please Upload Image.")
        return
    running = True
    status.config(text="Status: Camera Running")
    update_frame()

def stop_camera():
    global running
    running = False
    if cap:
        cap.release()
    status.config(text="Status: Camera Stopped")

def update_frame():
    if not running:
        return
    ret, frame = cap.read()
    if ret:
        process_frame(frame)
        root.after(10, update_frame)
    else:
        status.config(text="Status: Camera Error. Try Uploading.")

def upload_image():
    stop_camera()
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        frame = cv2.imread(file_path)
        if frame is not None:
            process_frame(frame)
            status.config(text="Status: Image Processed")

# Buttons
tk.Button(root, text="Start Camera", width=20, command=start_camera).pack(pady=5)
tk.Button(root, text="Stop Camera", width=20, command=stop_camera).pack(pady=5)
tk.Button(root, text="Upload Image", width=20, command=upload_image).pack(pady=5)

root.mainloop()
