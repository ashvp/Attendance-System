from fastapi import APIRouter, HTTPException, UploadFile, File, Form
import numpy as np
import cv2
import psycopg2
from ..database import get_connection
from ..embeddings.facenet_model import FaceEmbedder
from ..embeddings.detector import FaceDetector
import csv

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
    
    # Store embedding as a Python list
    embedding_vector = embedding.tolist()
    
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
        
    try:
        cur = conn.cursor()
        
        # PostgreSQL will handle the conversion from Python list to vector format
        cur.execute("INSERT INTO users (name, email, embedding) VALUES (%s, %s, %s)", 
                   (name, email, embedding_vector))
        
        conn.commit()
        return {"message": f"User {name} registered successfully."}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@router.put("/api/register/csv")
def register_users_from_csv(file: UploadFile = File(...)):
    if file.endswith(".csv") is False:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    content = file.file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(decoded.splitlines())

    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    success = []
    failed = []

    try:
        cur = conn.cursor()
        
        for row in reader:
            name = row.get("name")
            email = row.get("email")
            image_path = row.get("image_path")
            
            if not name or not email or not image_path:
                failed.append({"name": name, "email": email, "error": "Missing required fields"})
                continue
            
            img = cv2.imread(image_path)
            if img is None:
                failed.append({"name": name, "email": email, "error": "Invalid image path"})
                continue
            
            face = detector.detect_and_crop(img)
            if face is None:
                failed.append({"name": name, "email": email, "error": "No face detected in the image"})
                continue
            
            embedding = embedder.get_embedding(face)
            embedding_vector = embedding.tolist()
            
            try:
                cur.execute("INSERT INTO users (name, email, embedding) VALUES (%s, %s, %s)", 
                           (name, email, embedding_vector))
                success.append({"name": name, "email": email})
            except Exception as e:
                failed.append({"name": name, "email": email, "error": str(e)})
        
        conn.commit()
        return {"message":"CSV Upload Complete", "success": len(success), "failed": len(failed), "success_list": success, "failed_list": failed}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cur.close()
        conn.close()

