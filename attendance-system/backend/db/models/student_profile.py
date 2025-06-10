from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.db.base import Base
from backend.db.enum import UserRole, StudentCategory

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(Enum(StudentCategory), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    user = relationship("User", back_populates="student_profile")

    