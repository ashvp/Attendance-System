from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from ..db.session import get_db
from ..db.models.user import User
from ..db.models.attendance import Attendance

import io
import csv
from datetime import datetime

router = APIRouter()

@router.get("/api/attendance/export")
async def export_attendance(db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Attendance).options(joinedload(Attendance.user)).order_by(Attendance.date.desc())
        result = await get_db().execute(stmt)
        rows = result.scalars().all()

        if not rows:
            raise HTTPException(status_code=404, detail="No attendance records found")
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Name", "Email", "Date", "Session"])

        for row in rows:
            writer.writerow([row.user.name, row.user.email, row.date, row.session])

        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=attendance.csv"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/attendance/user/{user_id}")
async def get_attendance_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Attendance).where(Attendance.user_id == user_id).order_by(Attendance.date.desc())
        result = await get_db().execute(stmt)
        records = result.scalars().all()
        if not records:
            raise HTTPException(status_code=404, detail="No attendance records found for this user")

        return [{"date": record.date, "session": record.session} for record in records]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/attendance/filter")
async def filter_attendance(start_date: str, end_date: str, db: AsyncSession = Depends(get_db)):
    try:
        stmt = select(Attendance).options(joinedload(Attendance.user)).where(
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ).order_by(Attendance.date.desc())

        result = await get_db().execute(stmt)
        records = result.scalars().all()

        if not records:
            raise HTTPException(status_code=404, detail="No attendance records found for the specified date range")
        
        return [
            {
                "name": record.user.name,
                "email": record.user.email,
                "date": record.date,
                "session": record.session
            } for record in records
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))