from fastapi import FastAPI, HTTPException
from .models import create_table
from .database import get_connection
from datetime import datetime
from psycopg2 import sql
from .routes import mark_attendance, register, users, attendance

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


app = FastAPI()

app.include_router(mark_attendance.router)
app.include_router(register.router)
app.include_router(users.router)
app.include_router(attendance.router)

@app.on_event("startup")
def startup_event():
    create_table()
    print("Database tables ready.")

@app.get("/")
def read_root():
    return {"Message": "FastAPI is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

