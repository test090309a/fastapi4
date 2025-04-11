# app/routers/articles.py
"""
Router für CRUD-Operationen an Artikeln.
"""
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database import get_db
from ..models import Article, Category
from ..auth import decode_access_token

router = APIRouter()

@router.get("/", response_model=List[dict])
def get_articles(db: Session = Depends(get_db)):
    """
    Liefert alle Artikel, sortiert nach Erstellungszeit (neueste zuerst).
    """
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    return [{"id": art.id, "title": art.title, "description": art.description, "content": art.content, "author": art.author, "created_at": art.created_at, "category": art.category.name if art.category else None} for art in articles]

@router.post("/")
def create_article(token: str = Form(...), title: str = Form(...), description: str = Form(""), content: str = Form(""), author: str = Form(...), category: str = Form(""), db: Session = Depends(get_db)):
    """
    Erstellt einen neuen Artikel, sofern der Token gültig ist.
    """
    username = decode_access_token(token)
    if username != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")
    cat = db.query(Category).filter(Category.name == category).first()
    if not cat:
        cat = Category(name=category)
        db.add(cat)
        db.commit()
        db.refresh(cat)
    new_article = Article(title=title, description=description, content=content, author=author, category_id=cat.id, created_at=datetime.utcnow())
    db.add(new_article)
    db.commit()
    return {"info": f"Artikel '{title}' wurde erstellt"}

@router.delete("/{article_id}")
def delete_article(article_id: int, token: str, db: Session = Depends(get_db)):
    """
    Löscht einen Artikel anhand der ID, wenn der Token gültig ist.
    """
    username = decode_access_token(token)
    if username != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")
    db.delete(article)
    db.commit()
    return {"info": f"Artikel mit ID {article_id} wurde gelöscht"}
