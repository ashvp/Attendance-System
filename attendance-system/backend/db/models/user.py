from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship

from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_id = Column(String, unique=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    embedding = Column(Vector(512), nullable=False)  # Assuming embedding is a vector type
    is_admin = Column(Boolean, default=False)

    attendances = relationship("Attendance", back_populates="user")