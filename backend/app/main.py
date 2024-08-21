from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .utils.pdf_to_text import pdf_to_text
from .utils.text_to_audio import text_to_audio
from .utils.language_detection import detect_language
import os
from pathlib import Path

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # Update with your frontend origin
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define directories for uploads and audio files
UPLOAD_DIR = Path("temp/uploads")
AUDIO_DIR = Path("temp/audio")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/convert/", response_model=schemas.Conversion)
async def convert_pdf_to_audio(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the uploaded PDF file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Convert PDF to text
    text = pdf_to_text(str(file_path))
    
    # Detect language
    lang = detect_language(text)
    
    # Convert text to audio
    audio_file_path = AUDIO_DIR / (file.filename.replace(".pdf", ".wav"))
    audio_file = text_to_audio(text, lang)
    
    # Save the audio file
    with open(audio_file_path, "wb") as audio_buffer:
        audio_buffer.write(audio_file)
    
    # Save conversion to database
    conversion = crud.create_conversion(db, file.filename, lang, str(audio_file_path))
    
    return conversion

@app.get("/conversions/", response_model=list[schemas.Conversion])
def read_conversions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conversions = crud.get_conversions(db, skip=skip, limit=limit)
    return conversions

@app.get("/download/{file_name}")
def download_file(file_name: str):
    file_path = AUDIO_DIR / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_name)
