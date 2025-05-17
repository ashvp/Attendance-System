from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException
from ..database import get_connection
import io
import csv

router = APIRouter()

@router.get("/api/attendance/export")
def export_attendance():
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT users.name, users.email, attendance.date FROM attendance JOIN users ON attendance.user_id = users.id ORDER BY date DESC")
        rows = cur.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Name", "Email", "date"])  
        
        for row in rows:
            writer.writerow(row)

        output.seek(0)  

        return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=attendance.csv"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cur.close()
        conn.close()

@router.get("/api/attendance/user/{user_id}")
def get_attendance_by_user(user_id: int):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cur = conn.cursor()
        cur.execute("SELECT date FROM attendance WHERE user_id = %s ORDER BY date DESC", (user_id,))
        rows = cur.fetchall()
        return {"user_id": user_id, "records": [r[0] for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


@router.get("/api/attendance/filter")
def filter_attendance(start_date: str, end_date: str):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT users.name, users.email, attendance.date FROM attendance JOIN users ON attendance.user_id = users.id WHERE date BETWEEN %s AND %s ORDER BY date DESC",
            (start_date, end_date)
        )
        rows = cur.fetchall()
        return [{"name": r[0], "email": r[1], "date": r[2]} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

