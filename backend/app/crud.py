from sqlalchemy.orm import Session
from . import models, schemas


def create_conversion(db: Session, filename: str, language: str, audio_file: str):
    db_conversion = models.Conversion(filename=filename, language=language, audio_file=audio_file)
    db.add(db_conversion)
    db.commit()
    db.refresh(db_conversion)
    return db_conversion

def get_conversions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Conversion).offset(skip).limit(limit).all()