from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import numpy as np
import cv2
import psycopg2
from ..database import get_connection
from ..embeddings.facenet_model import FaceEmbedder
from ..embeddings.detector import FaceDetector

router = APIRouter()
detector = FaceDetector()
embedder = FaceEmbedder()

@router.post("/api/register")
def register_user(name: str = Form(...),
                  email: str = Form(...), 
                  file: UploadFile = File(...)
                  ):
    contents = np.frombuffer(file.file.read(), np.uint8)
    img = cv2.imdecode(contents, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image format")

    face = detector.detect_and_crop(img)
    if face is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")
    
    embedding = embedder.get_embedding(face)
    embedding_vector = embedding.tolist()

    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, embedding) VALUES (%s, %s, %s)", (name, email, embedding_vector))
        conn.commit()
        return {"message": f"User {name} registered successfully."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


