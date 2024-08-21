from pydantic import BaseModel
from datetime import datetime


class ConversionBase(BaseModel):
    filename: str
    language: str
    audio_file: str

class Conversion(ConversionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True