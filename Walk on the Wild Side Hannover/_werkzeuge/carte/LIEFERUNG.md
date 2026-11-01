---
tags: [projekt, website]
status: aktiv
---

# Lieferung Die Pairing-Karte (La Carte, Karten) · Walk on the Wild Side Hannover (Nachtbau 31.10.2026)

Kopie der von Robert abgenommenen Pairing-Karte des Culinarium, umgekleidet und mit den Karten der Bar gefüllt («kopieren, umkleiden, Hauswerte eintragen»). Name im Werkzeug aus `_werkzeuge/oberflaeche/kleid/wildside.js` (**Die Pairing-Karte**; Ordner, Adressen und Schlüssel bleiben `carte`).

**Werkzeug:** http://127.0.0.1:9283/_werkzeuge/carte/ · **Anleitung:** http://127.0.0.1:9283/_werkzeuge/carte/anleitung.html · **Prüfung:** http://127.0.0.1:9283/_werkzeuge/carte/pruefung.html

## Was steht

- **Die Karte** (C08/C24 in der Form des Hauses, interne Kennung `abend`): die wechselnde Karte der Bar, deren Drinks Momo entwirft (Kundin 30.10.2026). Bis zu sechs Drinks mit Name und Zutaten, «Ab Donnerstag, …» mit Pfeilen (eine Woche), «Neue Karte anlegen», «Die Drinks stehen noch nicht fest», Name der Karte, Zeile, Preis je Drink, Hinweis, Fusszeile. Bis das Haus einträgt, steht beschriftet als **Beispiel** die jüngste überlieferte Drinkkarte (Valentinskarte «Drunk in Love», 14.02.2026, vier Drinks à 12).
- **Weitere Karten**, jede als Satz mit Rubriken, Name, Preis und Zutaten:
  - **Die Klassiker** (Negroni, Paloma, Mexikaner, Ohne Alkohol; aus `website/unter.py` drinks(), ohne Preise, die Website nennt keine).
  - **Drunk in Love** (Valentinstag 2026, «Cupid’s Signature Drinks», vier Drinks à 12, vom Plakat, `website/unter.py` drinks() karte).
  - **Dishes in Love** (zweite Seite derselben Karte, Rudis Teller zum Teilen mit Preisen 6–15; abgelesen vom Beitrag der Bar vom 03.02.2026, `_quelle/ig/2026-02-03_…DUT3HDnCMo1-3.jpg`, Wortlaut in `karten_lesen.py` DISHES; «Bouef» der Vorlage als «Bœuf»).
  - **Die Preise der Bar** (Angebotsmappe: sieben Getränkepreise, Pauschale Kategorie 1–3 mit 49/59/79, Service und Raum 500, Budget ab 1.000, Hinweise zu 2 Uhr und Anzahlung; `website/unter.py` PREISE, PAUSCHALE, tafel()).
- **Satz im Kleid der Bar** (`satz_bau.py`, `satz/satz.css`, A4 hoch): Creme wie die weissen Plakate, Gold-Haarlinie als Rahmen des Eckschilds, Wortmarke rot aus `oberflaeche/kleid/wildside-marke.svg`, Titel und Namen in Prata, Zutaten und Etiketten in Hanken Grotesk, Preise mit Ziffern gleicher Breite. Feste Schnitte für den PDF-Satz (`fonts_statisch.py`: Prata-Regular und HankenGrotesk[wght] aus dem google/fonts-Repository → `fonts/Prata-400.ttf`, `Hanken-400/500.ttf`).
- **Werkzeug** wie im Culinarium (gleiche Wege und Funktionen, Master 4.3): Einfach / Fortgeschritten, Entwurf, Quittung, Rückgängig, Vorher/nachher, Probe-PDF, Veröffentlichen mit Wort-für-Wort-Prüfung, frühere Fassungen, Prüfseite, Export, Rundgang, Zur Werkbank (9288), Ansicht Website (Drinks, Feiern, Programm; rollt zum Abschnitt der Karte). Fotos je Karte aus `website/assets/bild/` (Momo giesst, Negroni, die Zeichnungen der Valentinskarte, Flaschen), klein `bilder/z/`, gross `bilder/g/`.
- **Eine Quelle für Karte und Website (C27):** jedes Veröffentlichen schreibt `anschluss/karten.json` (je Karte Rubriken, Namen, Zutaten, Preise; dazu «Die Karte»).
- **Demo-Sperre:** Datei `DEMO` liegt. Die Pairing-Karte schreibt nie in `website/`.

## Starten und prüfen

- `python3 _werkzeuge/carte/serve.py 9283` → http://127.0.0.1:9283/_werkzeuge/carte/
- Karten neu: `python3 _werkzeuge/carte/karten_lesen.py` (prüft selbst gegen `website/unter.py`, `drinks.html`, `tafel.html`) → `python3 _werkzeuge/carte/satz_bau.py` → `python3 _werkzeuge/carte/einlesen.py` (ein Stand des Hauses wird nie überschrieben)
- `python3 _werkzeuge/carte/pruefe.py alles` (Rundlauf Satz → Baum → Satz, Wortlaut der Drucke gegen die Quellen, Karten = Quelle, Schriften der PDFs; Server muss laufen)

## Wie geprüft (31.10.2026)

- `pruefe.py alles`: Rundlauf 4/4 Zeichen für Zeichen gleich, Wortlaut jeder gedruckten Karte gegen ihre Quelle 5/5 gleich, Karten in der Form der Website = Quelle 4/4, Schriften aller PDFs nur feste Schnitte (Prata-Regular, HankenGrotesk-Regular), kein Type 3. GESAMT GRÜN.
- Schnelle Prüfung (`tor-schnell.js`, Chromium, max 40, Tiefe 2, 1440/1280/1000/390): `pairing-karte` 20 Zustände (Stichproben 20/20/29), `pairing-karte-anleitung` 14 Zustände (14/14/19): **0 Funde, nichts «nicht erreicht», keine Browserfehler**. Repariert unterwegs: Titel im Kopf (Prata über der Zeilenhöhe), Schrift in Knöpfen und Rubrik-Wahl optisch mittig, «Website ansehen» als Knauf 901–1240 px, linke Kante im aufgeklappten Rand, Einzelwörter in Fenster- und Seitentiteln, Prüfseite am Handy.
- Mit den Augen: Zustände 1440/1280/1000/390 (Start, jede Karte, Fortgeschritten, Fenster, Website-Ansicht, Rundgang, Handy) und jede Karte als PDF-Seite.

## Offen, mit Grund

- **Aktuelle Karte von Momo unbekannt:** keine Drinks der laufenden Karte belegt; darum das beschriftete Beispiel. Nichts erfunden.
- **Preise der Klassiker** nicht belegt (Website nennt keine); die Karte zeigt sie ohne Preis.
- **Website liest die Pairing-Karte noch nicht:** Einbau von `karten.json` in den Bau der Website (Revier `website/`, mit Auftrag und ohne DEMO).
- **Online** nicht gebaut und nicht hochgeladen (Auftrag).
