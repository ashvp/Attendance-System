from fastapi import FastAPI, HTTPException
from .models import create_table
from .database import get_connection
from datetime import datetime
from psycopg2 import sql

app = FastAPI()

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

@app.post("/mark_attendance")
def mark_attendance():
    # Placeholder for getting facial recognition data
    embedding = None
    # This should be replaced with actual facial recognition logic

    # Getting connection to the database
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cur = conn.cursor()
    
    # Checking if the facial recognition data is valid
        cur.execute("SELECT id, name FROM users")
        users = cur.fetchall()
        

        best_user_id = None
        best_user_name = None
        best_similarity = -1

        for user in users:
            user_id, user_name = user

            similarity = 1
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_user_id = user_id
                best_user_name = user_name
        if best_similarity < 0.8:
            raise HTTPException(status_code=404, detail="No matching user found")
        
        

    # Marking attendance   
        date = datetime.now().date()
        session = "Morning" if datetime.now().hour < 12 else "Evening"

        cur.execute("INSERT INTO attendance (user_id, date, session, status) VALUES (%s, %s, %s, %s)",
                    (best_user_id, date, session, "Present"))

        conn.commit()

        return {"message": f"Attendance marked for {best_user_name} marked successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cur.close()
        conn.close()