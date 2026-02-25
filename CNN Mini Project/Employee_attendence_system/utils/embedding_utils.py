import cv2
import numpy as np
from mtcnn import MTCNN
from keras_facenet import FaceNet

detector = MTCNN()
embedder = FaceNet()


def get_face_embedding(image):
    """
    Takes BGR image and returns embedding.
    Returns None if face not detected.
    """
    try:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb)

        if len(faces) == 0:
            return None, None

        x, y, w, h = faces[0]['box']
        x, y = max(0, x), max(0, y)

        face = rgb[y:y+h, x:x+w]
        if face.size == 0:
            return None, None

        face = cv2.resize(face, (28, 28))
        embedding = embedder.embeddings([face])[0]

        return embedding, (x, y, w, h)

    except Exception as e:
        print("Embedding Error:", e)
        return None, None