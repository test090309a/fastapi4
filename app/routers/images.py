# app/routers/images.py
"""
Router für CRUD-Operationen an Bildern.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import shutil
from ..database import get_db
from ..models import Image
from ..auth import decode_access_token

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_images(db: Session = Depends(get_db)):
    """
    Liefert alle Bilder, sortiert nach Upload-Zeit (neueste zuerst).
    """
    images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
    return [{"id": img.id, "title": img.title, "description": img.description, "file_path": img.file_path, "uploaded_at": img.uploaded_at} for img in images]

@router.post("/")
def create_image(token: str = Form(...), title: str = Form(...), description: str = Form(""), file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Erstellt ein neues Bild, sofern der Token gültig ist.
    """
    username = decode_access_token(token)
    if username != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")
    file_location = f"static/images/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    new_image = Image(title=title, description=description, file_path=file_location)
    db.add(new_image)
    db.commit()
    return {"info": f"Bild '{file.filename}' wurde erstellt"}

@router.delete("/{image_id}")
def delete_image(image_id: int, token: str, db: Session = Depends(get_db)):
    """
    Löscht ein Bild anhand der ID, wenn der Token gültig ist.
    """
    username = decode_access_token(token)
    if username != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Bild nicht gefunden")
    db.delete(image)
    db.commit()
    return {"info": f"Bild mit ID {image_id} wurde gelöscht"}
