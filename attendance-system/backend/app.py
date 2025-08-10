import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env early
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

import firebase_auth

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.session import get_db
from db.table_manager import create_tables_if_not_exist
from contextlib import asynccontextmanager
# from .database import get_connection
from datetime import datetime
from psycopg2 import sql
from routes import mark_attendance, register, users, attendance, auth
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle FastAPI startup and shutdown events."""
    # Startup
    logger.info("🚀 Starting Attendance System API...")
    
    # Create tables if they don't exist
    db_success = await create_tables_if_not_exist()
    
    if not db_success:
        logger.error("❌ Failed to create database tables")
        # Don't exit, just log the error - app can still run if tables exist
    
    logger.info("✅ Application startup complete!")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down...")


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

