# app/routers/categories.py
"""
Router für CRUD-Operationen an Kategorien.
"""
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Category
from ..auth import decode_access_token

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_categories(db: Session = Depends(get_db)):
    """
    Liefert alle Kategorien.
    """
    categories = db.query(Category).all()
    return [{"id": cat.id, "name": cat.name} for cat in categories]

@router.post("/")
def create_category(token: str = Form(...), name: str = Form(...), db: Session = Depends(get_db)):
    """
    Erstellt eine neue Kategorie, sofern der Token gültig ist.
    """
    username = decode_access_token(token)
    if username != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")
    category = db.query(Category).filter(Category.name == name).first()
    if category:
        raise HTTPException(status_code=400, detail="Kategorie existiert bereits")
    new_category = Category(name=name)
    db.add(new_category)
    db.commit()
    return {"info": f"Kategorie '{name}' wurde erstellt"}

@router.delete("/{category_id}")
def delete_category(category_id: int, token: str, db: Session = Depends(get_db)):
    """
    Löscht eine Kategorie anhand der ID, wenn der Token gültig ist.
    """
    username = decode_access_token(token)
    if username != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Kategorie nicht gefunden")
    db.delete(category)
    db.commit()
    return {"info": f"Kategorie mit ID {category_id} wurde gelöscht"}
