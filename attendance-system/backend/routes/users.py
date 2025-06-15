from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..db.models.user import User
from ..db.session import get_db

router = APIRouter()

@router.get("/api/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).order_by(User.id))
        users = result.scalars().all()

        user_list = [
            {
                "id": user.id,
                "name": user.name,
                "account_id": user.account_id,
                "role": user.role.value,
                "is_admin": user.is_admin,
            }
            for user in users
        ]

        return {"users": user_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/api/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(user)
        await db.commit()

        return {"message": f"User with ID {user.id} deleted successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = {
            "id": user.id,
            "name": user.name,
            "account_id": user.account_id,
            "role": user.role.value,
            "is_admin": user.is_admin,
        }

        return {"user": user_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
