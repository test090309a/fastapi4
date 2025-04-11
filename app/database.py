# app/database.py
"""
Diese Datei initialisiert die Datenbankverbindung und erstellt die SQLAlchemy Base.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Erstellen der SQLite-Datenbank, in Produktion kann auch PostgreSQL verwendet werden.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Erstellen einer SessionLocal-Klasse für Datenbank-Sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Deklarative Base für die Modelle
Base = declarative_base()

def get_db():
    """
    Erzeugt eine Datenbank-Session, die nach Gebrauch wieder geschlossen wird.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()