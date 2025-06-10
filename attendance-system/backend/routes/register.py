from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
import numpy as np
import cv2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db.session import get_db
from ..db.models.user import User
from ..embeddings.facenet_model import FaceEmbedder
from ..embeddings.detector import FaceDetector
import csv

router = APIRouter()
detector = FaceDetector()
embedder = FaceEmbedder()

@router.post("/api/register")
async def register_user(name: str = Form(...),
                  email: str = Form(...),
                  file: UploadFile = File(...),
                  db: AsyncSession = Depends(get_db)
                  ):
    
    contents = await file.read()
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    face = detector.detect_and_crop(img)
    if face is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")
    
    embedding = embedder.get_embedding(face)
    embedding_vector = embedding.tolist()
    try:
        async with db() as session:
            result = await session.execute(select(User).where(User.email == email))
            existing_user = result.scalars().first()
            if existing_user:
                raise HTTPException(status_code=400, detail="User with this email already exists")
            
            new_user = User(
                name=name,
                email=email,
                embedding=embedding_vector
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return {"message": "User registered successfully", "user_id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/api/register/csv")
async def register_users_from_csv(file: UploadFile = File(...)):
    if file.endswith(".csv") is False:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    content = file.file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(decoded.splitlines())

    try:
        for row in reader:
            name = row.get("name")
            email = row.get("email")
            image_path = row.get("image_path")

            if not name or not email or not image_path:
                raise HTTPException(status_code=400, detail="CSV must contain 'name', 'email', and 'image_path' columns")

            # Read the image file
            with open(image_path, "rb") as img_file:
                contents = img_file.read()
                img_array = np.frombuffer(contents, np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is None:
                    raise HTTPException(status_code=400, detail=f"Invalid image file for {name}")

                face = detector.detect_and_crop(img)
                if face is None:
                    raise HTTPException(status_code=400, detail=f"No face detected in the image for {name}")

                embedding = embedder.get_embedding(face)
                embedding_vector = embedding.tolist()

                async with get_db() as session:
                    result = await session.execute(select(User).where(User.email == email))
                    existing_user = result.scalars().first()
                    if existing_user:
                        raise HTTPException(status_code=400, detail=f"User with email {email} already exists")

                    new_user = User(
                        name=name,
                        email=email,
                        embedding=embedding_vector
                    )
                    session.add(new_user)
                    await session.commit()
                    await session.refresh(new_user)
                    print(f"User {name} registered successfully with ID {new_user.id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

