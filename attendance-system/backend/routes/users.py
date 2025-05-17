from fastapi import APIRouter, HTTPException
from ..database import get_connection
router = APIRouter()

@router.get("/api/users")
def get_users():
    try:
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users ORDER BY id")
        users = cur.fetchall()

        user_list = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]

        return {"users": user_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        if conn:
            conn.close()

@router.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    try:
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
        deleted_user = cur.fetchone()

        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        conn.commit()
        return {"message": f"User with ID {deleted_user} deleted successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        if conn:
            conn.close()

@router.get("/api/users/{user_id}")
def get_user(user_id: int):
    try:
        conn = get_connection()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = {"id": user[0], "name": user[1], "email": user[2]}
        return {"user": user_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        if conn:
            conn.close()