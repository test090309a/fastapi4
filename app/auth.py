# app/auth.py
"""
Dieses Modul implementiert die Authentifizierungslogik mit JWT und Passwort-Hashing.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Geheimschlüssel und Einstellungen für JWT
SECRET_KEY = ":fastapi4@96240"  # geheimer_schluessel_fuer_jwt, Sollte sicher verwaltet werden!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Passwort-Hashing Kontext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Überprüft, ob das eingegebene Passwort mit dem gehashten Passwort übereinstimmt.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Erzeugt einen Hash für das gegebene Passwort.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Erstellt einen JWT Access Token mit den gegebenen Daten.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Dekodiert und validiert den JWT Access Token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
