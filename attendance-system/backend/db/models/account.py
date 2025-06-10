from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.db.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    firebase_id = Column(String, unique=True, nullable=True)
    users = relationship("User", back_populates="account", cascade="all, delete")
