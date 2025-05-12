from fastapi import FastAPI
from .models import create_table

app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_table()
    print("Database tables ready.")

@app.get("/")
def read_root():
    return {"Message": "FastAPI is running!"}