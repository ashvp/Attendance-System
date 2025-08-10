from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship

from db.base import Base
from db.enum import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, index=True, nullable=False)
    # email = Column(String, unique=True, index=True, nullable=False)
    embedding = Column(Vector(512), nullable=False)  # Assuming embedding is a vector type
    is_admin = Column(Boolean, default=False)

    role = Column(Enum(UserRole), nullable=False)  
    account = relationship("Account", back_populates="users")

    attendances = relationship("Attendance", back_populates="user")
    student_profile = relationship("StudentProfile", uselist=False, back_populates="user")