---
tags: [projekt, website]
status: aktiv
---

# Das Markenbuch (Le Livre, Marke) · Walk on the Wild Side Hannover · Lieferung (Nachtbau 31.10.2026)

Kopie des abgenommenen Markenbuchs von Culinarium Hannover, umgekleidet und mit den Hauswerten der Bar. Nichts online, nichts verschickt.

**Adresse:** http://127.0.0.1:9085/_werkzeuge/livre/ · Hausregeln: http://127.0.0.1:9085/_werkzeuge/livre/buch.html · Anleitung: http://127.0.0.1:9085/_werkzeuge/livre/anleitung.html · Stand-Weg für den Tresen: http://127.0.0.1:9085/marke/livre.json

Server: `python3 server.py 9085` im Ordner `_werkzeuge/livre` (Markenprüfung ohne Claude, Probe-Antwort). Neu bauen (nur in einer Sitzung mit `_quelle/`): `python3 bau.py && python3 buch.py`, Bilder der Anleitung `node anleitung_bilder.js && python3 anleitung_bau.py`.

## Was steht

- **Fotos:** 183 Fotos aus dem Bildregister der Website (`BILDER` in `website/bilder.py`, per ast gelesen, `register.py`; Grössen aus `website/assets/bild/<schlüssel>.json`), 11 doppelte zusammengeführt, in 9 Bereichen (Der Raum, Die Drinks, Die Leute, Musik und Feste, Die lange Tafel, Plakate und Karten, Unterwegs, Seit 2017, Im selben Haus). Herkunft je Foto in Worten: 51 von der Bar (Instagram, Facebook, erste Website, Angebotsmappe, von der Bar geschickt), 132 mit fremden Rechten (Google-Eintrag, Gäste und Partner auf Instagram, Presse, Portale, Rudis Fotos der Culinarium-Abende in der Bar). Je Foto vier Grössen; «Druck» in voller Grösse aus dem Original nur lokal mit `_quelle/`, sonst in Website-Grösse (die Oberfläche sagt es). Das Konzertfoto ist mit KI nachgeschärft und zeigt Vorher / Nachher / Schieber.
- **Logo & Dateien:** die Wortmarke (nachgezogen aus dem Logo der früheren Seite der Bar) in Rot, Creme und Nacht als SVG und PNG; die Vorlage von 2020 und das Instagram-Profilbild unverändert; die Tapete aus dem Sternmuster der Website (Gold auf Nacht, Gold tief auf Creme); 15 Farben (12 aus `wild.css`, 3 der SESSION-Plakate) als CSS, JSON, ASE; Prata und Hanken Grotesk Byte für Byte die der Website, ZIP mit TTF und OFL. Alles als ein ZIP. 19 Dateien.
- **Markenprüfung:** Farben ohne KI gemessen (ΔE 2000 gegen die Palette der Bar), Rest nur mit `LIVRE_KI=1`; ohne Schalter Probe-Antwort. Regeln für die Bar (`livre.py regeln()`). Beispiel: ein eigens gezeichneter Beitrag «Party-Nacht im Wild Side» mit Foto und Wortmarke, aber fetter Serifenschrift, Neon-Pink, reinem Schwarz und «Sie».
- **Hausregeln (buch.html):** zehn Blätter aus CHARAKTER.md 2–5: Haltung, Zeichen, Farben, DJ-Abende, Schrift, Form (Eckschild), Bilder, Gegenstände, Ton, Nachbarn; Leiste mit «Als PDF sichern» (A4 quer).
- **Rahmen:** gemeinsames Kleid `kleid/wildside.*`, Kennung `wildside` (Speicher `ws-livre-*`, Rundgang `rundgang-wildside-livre`, Werkbank `wildside-wb`), Rundgang in Nacht/Gold/Creme.
