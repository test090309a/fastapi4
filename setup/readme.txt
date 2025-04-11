# FastAPI Bildergalerie Projekt

## Zusammenfassung
Dieses Projekt wurde entwickelt, um eine moderne und elegante Bildergalerie mit FastAPI, SQLAlchemy und einem responsiven Frontend zu realisieren. 

- **Backend:** 
  - FastAPI zur Erstellung der API-Endpunkte
  - SQLAlchemy als ORM für die SQLite-Datenbank (alternativ kann PostgreSQL verwendet werden)
  - JWT-basierte Authentifizierung für den Admin-Benutzer ("admin" / "sysop")
  - Endpunkte für CRUD-Operationen von Bildern, Artikeln und Kategorien
  - Dateiupload-Funktion für Bilder

- **Frontend:**
  - HTML, CSS (mit modernen Techniken wie CSS Grid und Flexbox) und JavaScript für eine ansprechende Benutzeroberfläche
  - Eine schmale Navigationsleiste mit Logo und Links zu Home, View und Edit
  - Eine Bildergalerie, die die volle Höhe des Browserfensters einnimmt, mit automatischem Bildwechsel und Navigationspfeilen
  - Eine Ansichtseite für Artikel in einem Rasterlayout
  - Eine Edit-Seite, die den Admin-Login und Formulare zum Hochladen von Bildern und Erstellen von Artikeln enthält

- **Weitere Features:**
  - Responsives Design, das auf verschiedenen Bildschirmgrößen funktioniert
  - Ein Footer mit Logo und Links zu Impressum und Kontakt
  - Moderne Animationen und Übergänge
  - Einsatz neuester Techniken für Performance und Benutzerfreundlichkeit

## Warum wurde das Projekt so erstellt?
Das Projekt wurde konzipiert, um eine umfassende Plattform zu bieten, die die Präsentation von Bildern und Artikeln in einem modernen Webdesign vereint. 
Es verbindet innovative Technologien und Best Practices in der Webentwicklung, um ein ansprechendes und funktionales Benutzererlebnis zu gewährleisten. 
Die Verwendung von FastAPI sorgt für eine schnelle und skalierbare Backend-Lösung, während moderne Frontend-Techniken und responsives Design die Benutzerfreundlichkeit maximieren.

## Installation und Setup
1. Führe die `setup.bat` Datei aus, um die Verzeichnisstruktur und leere Dateien zu erstellen.
2. Installiere die benötigten Python-Pakete (z.B. FastAPI, uvicorn, SQLAlchemy, jinja2, python-jose, passlib, pillow)