import streamlit as st
import cv2
import pickle
import numpy as np
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_distances
from utils.embedding_utils import get_face_embedding
from utils.csv_utils import mark_attendance

st.set_page_config(page_title="Employee Attendance System", layout="wide")

st.title("Employee Attendance System")


@st.cache_resource
def load_embeddings():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    embeddings_path = os.path.join(BASE_DIR, "embeddings", "face_embeddings.pkl")

    if not os.path.exists(embeddings_path):
        st.error("Embeddings file not found! Please generate embeddings first.")
        return {}

    with open(embeddings_path, "rb") as f:
        return pickle.load(f)

known_faces = load_embeddings()

menu = st.sidebar.selectbox(
    "Navigation",
    ["Take Attendance", "View Attendance Records"]
)


if menu == "Take Attendance":

    option = st.radio(
        "Choose Attendance Method:",
        ("Upload Image", "Use Webcam")
    )

    if option == "Upload Image":
        uploaded_file = st.file_uploader(
            "Upload Employee Image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)

            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                     caption="Uploaded Image",
                     width='stretch')

            embedding, box = get_face_embedding(image)

            if embedding is None:
                st.error("No Face Detected")
            else:
                distances = []
                for emp_id, emp_name, known_embedding in known_faces:
                    dist = cosine_distances([embedding], [known_embedding])[0][0]
                    distances.append((dist, emp_id, emp_name))

                best_dist, emp_id, emp_name = min(distances)

                if best_dist < 0.5:
                    mark_attendance(emp_id, emp_name)
                    st.success(f"Attendance Marked for {emp_name} ({emp_id})")
                else:
                    st.warning("This Person is not an Employee")

    elif option == "Use Webcam":

        run = st.checkbox("Start Webcam")
        FRAME_WINDOW = st.image([])

        camera = cv2.VideoCapture(0)

        while run:
            ret, frame = camera.read()
            if not ret:
                st.error("Failed to access webcam")
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
                    st.success(f"Attendance Marked for {emp_name} ({emp_id})")
                    color = (0, 255, 0)
                else:
                    label = "Not Employee"
                    color = (0, 0, 255)

                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, label, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        camera.release()
 
elif menu == "View Attendance Records":
    st.subheader("Attendance Records")
    if os.path.exists('Attendence/attendance.csv'):
        df = pd.read_csv('Attendence/attendance.csv', engine='python', on_bad_lines='skip')
        st.dataframe(df, use_container_width=True)
        
        with open('Attendence/attendance.csv', "rb") as file:
            st.download_button(
                label="⬇ Download Attendance CSV",
                data=file,
                file_name="attendance.csv",
                mime="text/csv"
            )
            
        st.markdown("### Attendance Summary")
        total_entries = len(df)
        unique_employees = df["Emp_ID"].nunique() if "Emp_ID" in df.columns else 0

        col1, col2 = st.columns(2)
        col1.metric("Total Entries", total_entries)
        col2.metric("Unique Employees", unique_employees)

    else:
        st.info("No attendance records found yet.")
