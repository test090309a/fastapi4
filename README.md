Das Programm ist eine Webanwendung, die mit dem Framework FastAPI entwickelt wurde. Es bietet mehrere Funktionen, darunter:
    Benutzerverwaltung: Erstellung und Authentifizierung von Benutzern (inklusive Admin-Funktionalität).
    Artikelverwaltung: Erstellung, Bearbeitung, Anzeige und Löschung von Artikeln.
    Bildverwaltung: Hochladen, Löschen und Sortieren von Bildern, die in einer Bildergalerie angezeigt werden.
    Kategorien: Verwaltung von Kategorien zur Organisation von Artikeln.
    Login und Logout: Authentifizierung über JWT-Tokens, die als Cookies gespeichert werden.

Verwendete Module:
Das Programm nutzt verschiedene Python-Bibliotheken und Module:
    FastAPI: Für die Entwicklung der API-Endpunkte und die Webanwendung.
    SQLAlchemy: Für die Interaktion mit der Datenbank (ORM).
    Jinja2: Für die Template-Engine zur Darstellung der HTML-Seiten.
    Datetime: Zur Berechnung von Zeitintervallen für Token-Ablaufzeiten.
    Shutil und OS: Für Dateiverwaltung (z. B. Löschen von Bilddateien).
    Pydantic: Für die Validierung der Datenmodelle.
    Typing: Zur Typisierung von Daten (z. B. Listen).

API-Schnittstellen:
Das Programm stellt mehrere API-Endpunkte bereit:
    GET /: Zeigt die Startseite mit einer Bildergalerie.
    GET /view: Listet alle Artikel auf einer Ansichtsseite auf.
    GET /edit: Zeigt die Bearbeitungsseite für Artikel, Bilder und Benutzer (nur für Admins).
    POST /edit: Authentifiziert Benutzer und setzt ein JWT-Cookie.
    POST /upload_image: Ermöglicht das Hochladen von Bildern (nur für Admins).
    POST /create_article: Erstellt neue Artikel und ordnet sie Kategorien zu (nur für Admins).
    POST /edit/article/{article_id}: Aktualisiert bestehende Artikel (nur für Admins).
    POST /edit/article/{article_id}/delete: Löscht einen Artikel (nur für Admins).
    POST /edit/image/{image_id}/delete: Löscht ein Bild aus der Galerie (nur für Admins).
    POST /edit/images/delete: Löscht mehrere Bilder gleichzeitig und aktualisiert deren Reihenfolge (nur für Admins).
    GET /logout: Loggt den Benutzer aus, indem das Token-Cookie gelöscht wird.

Datenbankmodelle:
Die Anwendung verwendet folgende Modelle:
    User: Für Benutzerinformationen wie Benutzernamen und Passwörter.
    Article: Für Artikel mit Titel, Beschreibung, Inhalt und zugehöriger Kategorie.
    Category: Für Kategorien zur Organisation von Artikeln.
    Image: Für Bilder mit Titel, Beschreibung und Dateipfad.
