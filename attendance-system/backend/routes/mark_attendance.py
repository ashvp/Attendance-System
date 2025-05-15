from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File
from datetime import datetime
import numpy as np
import cv2
from ..database import get_connection
from ..embeddings.facenet_model import FaceEmbedder
from ..embeddings.detector import FaceDetector

router = APIRouter()
detector = FaceDetector()
embedder = FaceEmbedder()

@router.post("/mark_attendance")
def mark_attendance(image: UploadFile = File(...)):
    contents = np.frombuffer(image.file.read(), np.uint8)
    img = cv2.imdecode(contents, cv2.IMREAD_COLOR)
    face = detector.detect_and_crop(img)
    if face is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")
    
    embedding = embedder.get_embedding(face).tolist()

    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cur = conn.cursor()

        embedding_str = ",".join(str(x) for x in embedding)
        query = f"""
            SELECT id, name, embedding <#> '{embedding_str}'::vector AS similarity
            FROM users
            ORDER BY similarity
            LIMIT 1;
        """
        cur.execute(query)
        result = cur.fetchone()

        if not result or result[2] > 0.4:
            raise HTTPException(status_code=404, detail="No matching user found")

        user_id, user_name, _ = result

        date = datetime.now().date()
        session = "Morning" if datetime.now().hour < 12 else "Evening"

        cur.execute(
            "INSERT INTO attendance (user_id, date, session, status) VALUES (%s, %s, %s, %s)",
            (user_id, date, session, "Present")
        )
        conn.commit()

        return {"message": f"Attendance marked for {user_name} successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()
