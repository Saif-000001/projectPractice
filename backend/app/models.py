from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Conversion(Base):
    __tablename__ = "conversions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    language = Column(String)
    audio_file = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())