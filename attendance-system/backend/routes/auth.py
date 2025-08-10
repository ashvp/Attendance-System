# backend/routes/auth.py
from fastapi import APIRouter, Request, Header, HTTPException
from firebase_auth import verify_firebase_token

router = APIRouter()

@router.get("/api/auth/me")
async def get_me(authorization: str = Header(...)):
    try:
        token = authorization.split("Bearer ")[-1]
        user_info = verify_firebase_token(token)
        return {"email": user_info["email"], "uid": user_info["uid"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

from pydantic import BaseModel

class TokenRequest(BaseModel):
    token: str

@router.post("/api/auth/firebase")
async def firebase_auth(request: TokenRequest):
    try:
        user_info = verify_firebase_token(request.token)
        return {"email": user_info["email"], "uid": user_info["uid"]}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")