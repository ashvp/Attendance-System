from fastapi import FastAPI, HTTPException, APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select, insert
from pgvector.sqlalchemy import cosine_distance
from datetime import datetime
import numpy as np
import cv2
from ..db.session import get_db
from ..db.models.user import User
from ..db.models.attendance import Attendance
from ..embeddings.facenet_model import FaceEmbedder
from ..embeddings.detector import FaceDetector

router = APIRouter()
detector = FaceDetector()
embedder = FaceEmbedder()

@router.post("/mark_attendance")
async def mark_attendance(image: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    contents = await image.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

    face = detector.detect_and_crop(img)
    if face is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")
    
    embedding = embedder.get_embedding(face)
    
    stmt = select(User, cosine_distance(User.embedding, embedding).label("similarity")).order_by("similarity").limit(1)

    result = await get_db().execute(stmt)
    match = result.first()

    if not match or match.similarity > 0.5:
        raise HTTPException(status_code=404, detail="No matching user found")
    
    user: User = match[0]

    now = datetime.now()
    session = "Morning" if now.hour < 12 else "Evening"

    stmt = insert(Attendance).values(
        user=user.id,
        date = now.date(),
        session=session,
        status="Present"
    )

    await get_db().execute(stmt)
    await get_db().commit()

    return {"message": f"Attendance marked for {user.name} ({user.email}) on {now.date()} during {session} session."}

