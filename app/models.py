# app/models.py
"""
Dieses Modul definiert die Datenbankmodelle für den FastAPI Anwendung.
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    """
    Modell für den Benutzer, hier wird der Admin-Benutzer definiert.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Category(Base):
    """
    Modell für Kategorien, in die Bilder/Artikel einsortiert werden können.
    """
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    articles = relationship("Article", back_populates="category")

class Article(Base):
    """
    Modell für Artikel, die in der Galerie angezeigt werden.
    """
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    author = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="articles")
    image_path = Column(String, nullable=True)  # Pfad zum Bild

class Image(Base):
    """
    Modell für Bilder, die in der Galerie verwendet werden.
    """
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    order = Column(Integer, default=0)  # Neue Spalte hinzufügen


class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)