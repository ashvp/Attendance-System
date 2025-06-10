from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from backend.db.base import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(String, nullable=False)
    session = Column(String, nullable=False)  
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="attendances")

   