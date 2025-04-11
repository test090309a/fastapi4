# fastapi4
Bildgalerie mit Administration.

Ein Python Programm, das mit Uvicorn/FastApi eine Website zeigt.
Es lauft in einem Hero-Carousel eine Bildgalerie, 
welche als Admin bearbeitet werden kann.

CRUD
Artikel erstellen. @work
Bilder laden und sortieren.


---jn 11.04.2025
Commit NFO
    Why have I made these changes?
    What effect have my changes made?
    Why was the change needed?
    What are the changes in reference to?

JWT-Token als Cookie
Jinja2Templates

Api Schnittstellen:
    / -> index.html
    /view -> edit.html
    /edit -> edit.html
    /edit/image/image_id/delete -> Bilder löschen
    /edit/images/delete -> Mehrere Bilder löschen
    /logout -> /
    /upload_image ->
    /create_article -> /view
    /edit/article -> /edit
    /edit/article/article_id ->edit.html
    /edit/article/article_id/delete -> edit.html
    /edit/user/create -> edit.html
    /edit/user/user_id/delete -> edit.html
    /submit_contact_form -> contact_form.html
    /submit_contact -> ?contact_success=true/contact_error=true
    /update_image_order -> Bilder sortieren

