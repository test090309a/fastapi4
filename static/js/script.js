/* static/js/script.js */
// JavaScript für die Galerie und weitere UI-Funktionen
// Enthält den Original-Code sowie die Erweiterungen:
// - Automatischer Bildwechsel (alle 5 Sekunden)
// - Pause-/Weiter-Funktion und Tastaturnavigation für die Galerie
// - Fortschrittsanzeige für die Galerie
// - Scroll-to-Top Button (stilisiert wie eine Maus)
// - Anzeige der messageBox
// - Footer-Links mit Modal (Kontakt, Impressum, etc.)

// ==================== GALERIE-SLIDES ====================

// Variablen für die Galerie
let currentSlide = 0;
let slides = [];
let slideInterval; // ID des setInterval
let isPaused = false; // Zustand der Galerie (pausiert/nicht pausiert)

// Funktion: Zeigt den aktuellen Slide an und aktualisiert die Fortschrittsanzeige
function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.classList.toggle("active", i === index);
    });
    updateProgressBar(index);
}

// Nächster Slide (wird im Interval genutzt)
function nextSlide() {
    if (slides.length === 0) return;
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

// Vorheriger Slide (kann per Tastatur oder Button genutzt werden)
function prevSlide() {
    if (slides.length === 0) return;
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
}

// Startet den automatischen Bildwechsel
function startSlideShow() {
    slideInterval = setInterval(nextSlide, 5000); // Wechselt alle 5 Sekunden
}

// Stoppt den automatischen Bildwechsel
function stopSlideShow() {
    clearInterval(slideInterval);
}

// Aktualisiert die Fortschrittsanzeige (kleine Balken)
function updateProgressBar(index) {
    const progressBar = document.getElementById("galleryProgressBar");
    if (!progressBar) return;
    const bars = progressBar.querySelectorAll("div");
    bars.forEach((bar, i) => {
        bar.classList.toggle("active", i === index);
    });
}

// Initialisiert die Fortschrittsanzeige, indem für jeden Slide ein Balken erstellt wird
function initProgressBar() {
    const progressBar = document.getElementById("galleryProgressBar");
    if (!progressBar) return;
    progressBar.innerHTML = "";
    slides.forEach(() => {
        const bar = document.createElement("div");
        progressBar.appendChild(bar);
    });
}

// Initialisierung der Galerie und der zusätzlichen Funktionen
document.addEventListener("DOMContentLoaded", function () {
    // Galerie-Slides laden und initialisieren
    slides = document.querySelectorAll(".gallery-item");
    if (slides.length > 0) {
        slides[0].classList.add("active");
        initProgressBar(); // Erstelle Fortschrittsbalken
        startSlideShow();
    }

    // Pause-/Weiter-Button für die Galerie (Button muss die ID "galleryPauseBtn" haben)
    const pauseButton = document.getElementById("galleryPauseBtn");
    if (pauseButton) {
        pauseButton.addEventListener("click", function() {
            if (isPaused) {
                // Slideshow wird fortgesetzt, also zeigen wir das Pause-Symbol an
                startSlideShow();
                pauseButton.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <rect x="6" y="4" width="4" height="16" fill="currentColor"/>
                    <rect x="14" y="4" width="4" height="16" fill="currentColor"/>
                </svg>`;
                isPaused = false;
            } else {
                // Slideshow wird pausiert, also zeigen wir das Play-Symbol an
                stopSlideShow();
                pauseButton.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <polygon points="8,5 19,12 8,19" fill="currentColor"/>
                </svg>`;
                isPaused = true;
            }
        });
    }
    

    // Tastaturnavigation für die Galerie:
    // - ArrowRight: nächster Slide
    // - ArrowLeft: vorheriger Slide
    // - Leertaste: Pause/Weiter, deaktiviert. Weil man sonst keine Leerzeichen beim Erstellen eines Artikels machen kann ;)
    document.addEventListener("keydown", function(event) {
        if (event.key === "ArrowRight") {
            stopSlideShow();
            nextSlide();
        } else if (event.key === "ArrowLeft") {
            stopSlideShow();
            prevSlide();
        } 
        /**
        else if (event.key === " ") { // Leertaste als Pause-/Weitersteuerung
            event.preventDefault();
            if (pauseButton) pauseButton.click();
        } **/
    });

    // Scroll-to-Top Button Funktionalität:
    // Der Button (mit ID "scrollToTopBtn") erscheint, wenn der Benutzer scrollt, und bringt den Nutzer bei Klick nach oben.
    const scrollBtn = document.getElementById("scrollToTopBtn");
    if (scrollBtn) {
        window.addEventListener("scroll", function() {
            if (window.scrollY > 100) {
                scrollBtn.classList.add("visible");
            } else {
                scrollBtn.classList.remove("visible");
            }
        });
        scrollBtn.addEventListener("click", function() {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    document.getElementById('file').addEventListener('change', function(e) {
        const preview = document.getElementById('uploadPreview');
        preview.innerHTML = '';
        
        Array.from(e.target.files).forEach(file => {
          const reader = new FileReader();
          reader.onload = (e) => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.height = '100px';
            img.style.margin = '5px';
            preview.appendChild(img);
          }
          reader.readAsDataURL(file);
        });
    });
});

// ==================== MESSAGEBOX ====================

// Zeige die messageBox an (Element mit der ID "messageBox")
const messageBox = document.getElementById('messageBox');
if (messageBox) {
    messageBox.style.display = 'block'; // Zeige die Box an
    // Verstecke die Box nach 5 Sekunden
    setTimeout(() => {
        messageBox.style.display = 'none';
    }, 5000); // 5000 Millisekunden = 5 Sekunden
}

// ==================== FOOTER LINKS & MODAL ====================

document.addEventListener('DOMContentLoaded', function() {
    // Hole das Modal-Element
    var modal = document.getElementById("myModal");

    // Selektiere die Footer-Links für Kontakt und Impressum
    var contactLink = document.querySelector(".footer-link[href='#kontakt']");
    var impressumLink = document.querySelector(".footer-link[href='#impressum']");
    var modalContent = document.getElementById("modal-content");
    var span = document.getElementsByClassName("close")[0];

    // Alle Footer-Links abrufen
    var footerLinks = document.querySelectorAll(".footer-link");

    // Paragraph, in dem die Nachricht angezeigt wird
    var modalMessage = document.getElementById("modal-message");

    // Eventlistener für den Kontakt-Link
    if (contactLink) {
        contactLink.addEventListener("click", function(event) {
            event.preventDefault();
            openContactForm();
        });
    }
    // Eventlistener für den Impressum-Link
    if (impressumLink) {
        impressumLink.addEventListener("click", function(event) {
            event.preventDefault();
            openModalWithMessage(impressumLink.getAttribute("data-message"));
        });
    }

    // Schließt das Modal, wenn auf das Schließ-Symbol geklickt wird
    span.onclick = function() {
        modal.style.display = "none";
    };

    // Funktion zum Laden des Kontaktformulars in das Modal
    async function openContactForm() {
        try {
            const response = await fetch('/get_contact_form');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();
            modalContent.innerHTML = html;
            modal.style.display = "block";
        } catch (error) {
            console.error("Fehler beim Laden des Kontaktformulars:", error);
            modalContent.textContent = "Fehler beim Laden des Formulars.";
            modal.style.display = "block";
        }
    }

    // Funktion zum Öffnen des Modals mit einer Nachricht
    function openModalWithMessage(message) {
        // Ersetze benutzerdefinierte Tags durch HTML
        message = message.replace(/<headline>/g, '<h1>').replace(/<\/headline>/g, '</h1>');
        message = message.replace(/<p>/g, '<p>').replace(/<\/p>/g, '</p>');
    
        modalMessage.innerHTML = message; // HTML in den Nachrichtentext einfügen
        modalContent.innerHTML = ""; // Kontaktformular leeren
        modal.style.display = "block";
    }

    // Füge allen Footer-Links einen Click-Eventlistener hinzu, um das Modal zu öffnen
    footerLinks.forEach(function(link) {
        link.addEventListener("click", function(event) {
            event.preventDefault(); // Verhindert das Navigieren
            var message = this.getAttribute("data-message");
            openModalWithMessage(message);
        });
    });

    // Schließt das Modal, wenn außerhalb des Modal geklickt wird
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});
