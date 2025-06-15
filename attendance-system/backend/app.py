import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env early
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import backend.firebase_auth

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .db.session import get_db
# from .database import get_connection
from datetime import datetime
from psycopg2 import sql
from .routes import mark_attendance, register, users, attendance, auth

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


app = FastAPI()

origins = [
    "*",  # Allows all origins
    "http://localhost:3000" # Allows localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(mark_attendance.router)
app.include_router(register.router)
app.include_router(users.router)
app.include_router(attendance.router)
app.include_router(auth.router)

@app.on_event("startup")
def startup_event():
    get_db()
    print("Database tables ready.")

@app.get("/")
def read_root():
    return {"Message": "FastAPI is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

