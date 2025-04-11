@echo off
REM Erstelle die Verzeichnisstruktur für das FastAPI Projekt

REM Root-Verzeichnis
mkdir app
mkdir app\routers
mkdir templates
mkdir static
mkdir static\css
mkdir static\js
mkdir static\images

REM Erstelle leere Dateien in den entsprechenden Verzeichnissen
type nul > app\__init__.py
type nul > app\main.py
type nul > app\database.py
type nul > app\models.py
type nul > app\auth.py
type nul > app\routers\__init__.py
type nul > app\routers\images.py
type nul > app\routers\articles.py
type nul > app\routers\categories.py
type nul > templates\base.html
type nul > templates\index.html
type nul > templates\view.html
type nul > templates\edit.html
type nul > static\css\style.css
type nul > static\js\script.js

echo Verzeichnisstruktur wurde erstellt.
pause
