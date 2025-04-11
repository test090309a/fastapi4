# app/main.py

"""
Hauptdatei des FastAPI-Projekts.
Diese Version setzt den JWT-Token als Cookie, sodass der Admin über Seitenwechsel hinweg eingeloggt bleibt.
"""

from fastapi import FastAPI, Request, Depends, HTTPException, status, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timedelta
import shutil
import os
from .database import engine, SessionLocal, Base
from .models import User, Article, Category, Image
from .auth import get_password_hash, verify_password, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Body
from typing import List  # Für die Typisierung von Listen

# Erstellen aller Datenbanktabellen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mounten des statischen Verzeichnisses
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_admin(db: Session):
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(username="admin", hashed_password=get_password_hash("sysop"))
        db.add(admin)
        db.commit()

# Startup-Event: Admin initialisieren und vordefinierte Kategorien anlegen
@app.on_event("startup")
def startup():
    db = SessionLocal()
    init_admin(db)

    # Vordefinierte Kategorien: wissen, ki, privat, projekt
    predefined_categories = ["wissen", "ki", "privat", "projekt"]
    for cat_name in predefined_categories:
        existing_cat = db.query(Category).filter(Category.name == cat_name).first()
        if not existing_cat:
            new_cat = Category(name=cat_name)
            db.add(new_cat)
            db.commit()
    db.close()

# Startseite mit Bildergalerie (Hero-Carousel)
@app.get("/", response_class=HTMLResponse)
def read_gallery(request: Request, db: Session = Depends(get_db)):
    # Bilder nach der Reihenfolge sortieren
    images = db.query(Image).order_by(Image.order.asc()).all()
    
    # Token aus dem Cookie auslesen
    token = request.cookies.get("access_token")
    # Benutzernamen aus dem Token dekodieren (falls vorhanden)
    username = None
    if token:
        try:
            username = decode_access_token(token)
        except Exception as e:
            print(f"Fehler beim Dekodieren des Tokens: {e}")
    
    # Bilder aus der Datenbank abrufen und nach der Reihenfolge sortieren
    images = db.query(Image).order_by(Image.order.asc()).all()
    
    # Template mit den Daten rendern
    return templates.TemplateResponse("index.html", {
        "request": request,
        "username": username,  # Benutzername ans Template übergeben
        "images": images,      # Bilder für die Galerie (sortiert nach Reihenfolge)
        "token": token         # Token für Admin-Funktionen
    })

# Artikel-Ansichtsseite
@app.get("/view", response_class=HTMLResponse)
def view_articles(request: Request, db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    token = request.cookies.get("access_token")
    return templates.TemplateResponse("view.html", {"request": request, "articles": articles, "token": token})

# ARTIKEL BEARBEITEN
@app.get("/edit", response_class=HTMLResponse)
def edit_page(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if token and decode_access_token(token) == "admin":
        articles = db.query(Article).order_by(Article.created_at.desc()).all()
        # Bilder nach der Reihenfolge sortieren
        images = db.query(Image).order_by(Image.order.asc()).all()
        users = db.query(User).all()
        categories = db.query(Category).all()  # Kategorien abfragen
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "token": token,
            "categories": categories,  # Kategorien übergeben
            "articles": articles,
            "images": images,
            "users": users
        })
    else:
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "token": None,
            "message": "",
            "articles": [],
            "images": [],
            "users": [] # Leere Liste übergeben, wenn kein Admin
        })

# LOGIN
@app.post("/edit", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "token": None,
            "message": "Ungültige Anmeldedaten",
            "articles": [],
            "images": [],
            "users": []
        })

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
    users = db.query(User).all() # Alle Benutzer abrufen

    response = templates.TemplateResponse("edit.html", {
        "request": request,
        "token": token,
        "message": "Login erfolgreich",
        "articles": articles,
        "images": images,
        "users": users # Benutzer an das Template übergeben
    })
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

# Neuer Endpunkt zum Löschen von Bildern
@app.post("/edit/image/{image_id}/delete", response_class=HTMLResponse)
def delete_image_endpoint(image_id: int, request: Request, token: str = Form(...), db: Session = Depends(get_db)):
    if decode_access_token(token) != "admin":
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "token": None,
            "message": "Nicht autorisiert",
            "articles": [],
            "images": [],
            "users": []
        })

    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Bild nicht gefunden")
    # Datei aus dem Dateisystem löschen (falls vorhanden)
    if image.file_path and os.path.exists(image.file_path):
        os.remove(image.file_path)

    db.delete(image)
    db.commit()
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
    users = db.query(User).all() # Alle Benutzer abrufen
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "token": token,
        "message": f"Bild '{image.title}' wurde gelöscht",
        "articles": articles,
        "images": images,
        "users": users # Benutzer an das Template übergeben
    })
# Neuer Endpunkt zum Löschen mehrerer Bilder gleichzeitig
@app.post("/edit/images/delete", response_class=HTMLResponse)
def delete_multiple_images(
    request: Request,
    token: str = Form(...),
    image_ids: List[int] = Form(...),
    db: Session = Depends(get_db)
):
    if decode_access_token(token) != "admin":
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "token": None,
            "message": "Nicht autorisiert",
            "images": []
        })

    try:
        # Lösche die ausgewählten Bilder
        for img_id in image_ids:
            img = db.query(Image).filter(Image.id == img_id).first()
            if img:
                db.delete(img)
        db.commit()

        # Aktualisiere die Reihenfolge der verbleibenden Bilder
        images = db.query(Image).order_by(Image.order.asc()).all()
        for idx, img in enumerate(images):
            img.order = idx
        db.commit()

        return templates.TemplateResponse("edit.html", {
            "request": request,
            "token": token,
            "message": f"{len(image_ids)} Bilder wurden gelöscht",
            "images": images
        })
    except Exception as e:
        db.rollback()
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "token": token,
            "message": f"Fehler beim Löschen der Bilder: {str(e)}",
            "images": db.query(Image).order_by(Image.order.asc()).all()
        }) 

# Logout: Löscht das Token-Cookie
@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    # response = templates.TemplateResponse("edit.html", {"request": request, "token": None, "message": "Abgemeldet", "articles": [], "users": []})
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

# Mehrere Bilder-Uploads (für Admin)
@app.post("/upload_image")
def upload_image(
    token: str = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    category: str = Form(""),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    if decode_access_token(token) != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")

    uploaded_files = []
    for file in files:
        file_location = f"static/images/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_image = Image(title=title, description=description, file_path=file_location)
        db.add(new_image)
        uploaded_files.append(file.filename)

    db.commit()
    # return {"info": f"Bilder {', '.join(uploaded_files)} wurden hochgeladen"}
    return RedirectResponse(url="/", status_code=303)

# Endpunkt für Artikelerstellung (nur authentifizierte Admins)
@app.post("/create_article")
def create_article(token: str = Form(...), title: str = Form(...), description: str = Form(""), content: str = Form(""), author: str = Form(...), category: str = Form(""), image_title: str = Form(""), db: Session = Depends(get_db)):
    """
    Erstellt einen neuen Artikel und ordnet diesen einer Kategorie zu.
    """
    username = decode_access_token(token)
    if username != "admin":
        raise HTTPException(status_code=401, detail="Nicht autorisiert")
    # Kategorie suchen oder erstellen
    cat = db.query(Category).filter(Category.name == category).first()
    if not cat:
        cat = Category(name=category)
        db.add(cat)
        db.commit()
        db.refresh(cat)
    # Neuen Artikel erstellen
    new_article = Article(title=title, description=description, content=content, author=author, category_id=cat.id)
    db.add(new_article)
    db.commit()
    # return {"info": f"Artikel '{title}' wurde erstellt"}
    return RedirectResponse(url="/view", status_code=303)

# Artikel bearbeiten: Formular anzeigen
@app.get("/edit/article/{article_id}", response_class=HTMLResponse)
def edit_article_form(
    article_id: int, 
    request: Request, 
    token: str = None, 
    db: Session = Depends(get_db)
):
    # Token aus dem Cookie auslesen, falls nicht übergeben
    if not token:
        token = request.cookies.get("access_token")
    
    # Überprüfen, ob der Benutzer ein Admin ist
    if not token or decode_access_token(token) != "admin":
        return RedirectResponse("/edit", status_code=302)

    # Artikel aus der Datenbank abrufen
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")
    
    # Kategorien aus der Datenbank abrufen
    categories = db.query(Category).all()
    
    # Template mit den Daten rendern
    return templates.TemplateResponse("edit_article.html", {
        "request": request, 
        "article": article, 
        "categories": categories,  # Kategorien an das Template übergeben
        "token": token,           # Token an das Template übergeben
        "message": "",            # Leere Nachricht (kann später gefüllt werden)
        "message_type": ""        # Leerer Nachrichtentyp (kann später gefüllt werden)
    })

# Artikel aktualisieren
@app.post("/edit/article/{article_id}", response_class=HTMLResponse)
def update_article(
    article_id: int,
    request: Request,
    token: str = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    content: str = Form(""),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    if decode_access_token(token) != "admin":
        return templates.TemplateResponse("edit.html", {"request": request, "token": None, "message": "Nicht autorisiert", "articles": []})

    if category not in ["wissen", "ki", "privat", "projekt"]:
        return templates.TemplateResponse("edit_article.html", {"request": request, "article": {"id": article_id}, "token": token, "message": "Ungültige Kategorie"})

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")

    article.title = title
    article.description = description
    article.content = content
    cat = db.query(Category).filter(Category.name == category).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Kategorie existiert nicht")
    article.category_id = cat.id

    db.commit()
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    return templates.TemplateResponse("edit.html", {
        "request": request, 
        "token": token, 
        "message": f"Artikel '{title}' wurde aktualisiert", 
        "articles": articles
        })

# Artikel löschen
@app.post("/edit/article/{article_id}/delete", response_class=HTMLResponse)
def delete_article(article_id: int, request: Request, token: str = Form(...), db: Session = Depends(get_db)):
    if decode_access_token(token) != "admin":
        return templates.TemplateResponse("edit.html", {"request": request, "token": None, "message": "Nicht autorisiert", "articles": []})

    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")

    db.delete(article)
    db.commit()
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    return templates.TemplateResponse("edit.html", {"request": request, "token": token, "message": f"Artikel '{article.title}' wurde gelöscht", "articles": articles})

#######################################################################
# HIER WILL ICH BENUTZER ANLEGEN UND LÖSCHEN KÖNNEN.                  #
#######################################################################

# Benutzer erstellen
@app.post("/edit/user/create", response_class=HTMLResponse)
def create_user(request: Request, username: str = Form(...), password: str = Form(...), token: str = Form(...), db: Session = Depends(get_db)):
    if decode_access_token(token) != "admin":
        return templates.TemplateResponse("edit.html", {"request": request, "token": None, "message": "Nicht autorisiert", "articles": [], "images":[], "users":[]})

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        articles = db.query(Article).order_by(Article.created_at.desc()).all()
        images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
        users = db.query(User).all()
        return templates.TemplateResponse("edit.html", {"request": request, "token": token, "message": f"Benutzername '{username}' bereits vorhanden.", "articles": articles, "images": images,  "users": users})

    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
    users = db.query(User).all()
    return templates.TemplateResponse("edit.html", {"request": request, "token": token, "message": f"Benutzer '{username}' erstellt.", "articles": articles, "images": images, "users": users})

# Benutzer löschen
@app.post("/edit/user/{user_id}/delete", response_class=HTMLResponse)
def delete_user(user_id: int, request: Request, token: str = Form(...), db: Session = Depends(get_db)):
    if decode_access_token(token) != "admin":
        return templates.TemplateResponse("edit.html", {"request": request, "token": None, "message": "Nicht autorisiert", "articles": [], "images":[], "users":[]})

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        articles = db.query(Article).order_by(Article.created_at.desc()).all()
        images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
        users = db.query(User).all()
        return templates.TemplateResponse("edit.html", {"request": request, "token": token, "message": "Benutzer nicht gefunden.", "articles": articles, "images": images, "users": users})

    # Verhindern, dass der Admin-Benutzer gelöscht wird
    if user.username == "admin":
        articles = db.query(Article).order_by(Article.created_at.desc()).all()
        images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
        users = db.query(User).all()
        return templates.TemplateResponse("edit.html", {"request": request, "token": token, "message": "Der Admin-Benutzer darf nicht gelöscht werden.", "articles": articles, "images": images, "users": users})

    db.delete(user)
    db.commit()

    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    images = db.query(Image).order_by(Image.uploaded_at.desc()).all()
    users = db.query(User).all()
    return templates.TemplateResponse("edit.html", {"request": request, "token": token, "message": f"Benutzer '{user.username}' gelöscht.", "articles": articles, "images": images, "users": users})


#######################################KONTAKT#######################
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import FastAPI, Request, Depends, Form, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from .database import engine, SessionLocal, Base  # Importiere Datenbank-Konfigurationen
from .models import User, Article, Category, Image # Importiere deine Modelle, einschließlich ContactRequest

# Definiere ContactRequest innerhalb von models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base


router = APIRouter()

Base = declarative_base()

class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)

@app.post("/submit_contact_form", response_class=RedirectResponse)
async def submit_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    ip_address = request.client.host  # Die IP-Adresse des Clients ermitteln

    # ContactRequest-Objekt erstellen und mit Formulardaten füllen
    contact_request = ContactRequest(
        name=name,
        email=email,
        message=message,
        ip_address=ip_address,
        created_at=datetime.utcnow()  # Aktuelles Datum und Uhrzeit
    )

    try:
        # Objekt zur Datenbank hinzufügen und Änderungen speichern
        db.add(contact_request)
        db.commit()

        # Weiterleitung zur Startseite mit Erfolgsmeldung
        return RedirectResponse(url="/?contact_success=True", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"Fehler beim Speichern der Daten: {e}")
        db.rollback()  # Datenbank-Rollback bei Fehler

        # Weiterleitung zur Startseite mit Fehlermeldung
        return RedirectResponse(url="/?contact_error=True", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/get_contact_form", response_class=HTMLResponse)
async def get_contact_form(request: Request):
    return templates.TemplateResponse("contact_form.html", {"request": request})

app.include_router(router)

# Neue Route für Kontaktformular-Submit
@app.post("/submit_contact", response_class=RedirectResponse)
async def submit_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    # Hier könntest du:
    # 1. E-Mail senden
    # 2. In Datenbank speichern
    # 3. Logging durchführen
    
    # Beispiel: In Datenbank speichern
    new_contact = ContactRequest(
        name=name,
        email=email,
        message=message,
        ip_address=request.client.host
    )
    
    try:
        db.add(new_contact)
        db.commit()
        return RedirectResponse(url="/?contact_success=true", status_code=303)
    except Exception as e:
        db.rollback()
        return RedirectResponse(url="/?contact_error=true", status_code=303)

##################################KONTAKT ENDE#####################

########### BILDER SORTIEREN #####################################
@app.post("/update_image_order")
def update_image_order(
    order: List[int] = Body(...),  # Liste von Bild-IDs in der neuen Reihenfolge
    token: str = Body(...),        # Token zur Authentifizierung
    db: Session = Depends(get_db)
):
    # Überprüfen, ob der Benutzer ein Admin ist
    if decode_access_token(token) != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nicht autorisiert"
        )

    try:
        # Reihenfolge der Bilder aktualisieren
        for idx, img_id in enumerate(order):
            img = db.query(Image).filter(Image.id == img_id).first()
            if img:
                img.order = idx  # Setze die neue Reihenfolge
        db.commit()  # Änderungen in der Datenbank speichern
        return {"status": "success"}
    except Exception as e:
        db.rollback()  # Bei Fehlern: Änderungen rückgängig machen
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Aktualisieren der Reihenfolge: {str(e)}"
        )
#################################################################


# Einbinden der API-Router
from .routers import images, articles, categories
app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
