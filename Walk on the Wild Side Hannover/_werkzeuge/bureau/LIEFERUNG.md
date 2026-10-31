---
tags: [projekt, website]
status: aktiv
---

# Das Schaufenster (Website pflegen, Arbeitsname Le Bureau) · Walk on the Wild Side Hannover · Lieferung

**Stand: Nachtbau 31.10.2026, in der Cloud gebaut und geprüft. Nichts online, nichts verschickt.** Vorlage: das abgenommene Schaufenster des Culinarium Hannover (28.–30.10.2026), kopiert, umgekleidet, Hauswerte eingetragen.

## Wo

- **Werkzeug:** http://127.0.0.1:9082/_werkzeuge/bureau/ · Server `python3 _werkzeuge/bureau/serve.py 9082` im Hausordner (Prüfläufe mit `BUREAU_PRUEFLAUF=1`).
- **DJ-Abende:** http://127.0.0.1:9082/_werkzeuge/bureau/?ansicht=e:termine
- **Anleitung:** http://127.0.0.1:9082/_werkzeuge/bureau/anleitung.html (neun Schritte, Bilder neu aufgenommen am 31.10.2026 mit Wegwerf-Daten)
- **Prüfseite:** http://127.0.0.1:9082/werkzeuge/website/pruefung.html?haus=wildside
- **Rundgang:** http://127.0.0.1:9082/_werkzeuge/bureau/?rundgang
- **Stand-Weg für den Tresen:** `GET /_werkzeuge/bureau/api/ueberblick` → `{aenderungen, zuletzt, bereiche, seiten, termine:{wartet, zahl}}`
- **Website, wie «online» wäre (Probe-Kopie):** http://127.0.0.1:9082/werkzeuge/website/_probe/wildside/online/index.html

## Was gebaut ist

| Teil | Was |
|---|---|
| `beschreibung.py` | Beschreibung der Bar für den Schreibtisch des Stamms, **nie von Hand**: 8 Seiten aus der Leiste der gebauten Website (Startseite, Drinks, Programm, Feiern, Das Haus, Besuch, Impressum, Datenschutz), 7 Bereiche mit Foto der Website, Bereich des Hauses «Gastschichten» (5 Gäste aus `programm.html`), Angaben aus dem Fuss von `index.html` (Telefon mit Link zum Anrufen, Strasse, PLZ/Ort, Instagram der Bar), Zeiten & Preise mit EUR, Google-Texte, eigenes Foto hochladen. Der Server ruft `anlegen()` beim Start: `_Werkzeuge/haeuser/wildside/haus.json`, `_Werkzeuge/werkzeuge/website/haeuser/wildside.json` und die Probe-Kopie `_probe/wildside/` entstehen so auch auf einem frischen Rechner (GitHub Actions). |
| **DJ-Abende** (`termine.py`, `termine-ansicht.js`) | Vorbild: die Termine des Culinarium. Die DJ-Abende der Bar stehen auf der Website als Liste `LINEUP` in `website/bau.py` (Datum, Name, Zeile, Plakat); gelesen mit `ast`, nie abgetippt, nie geändert. Daraus zeichnet die Website die Plakatwand und den Kontaktbogen auf «Programm» und den Flyer auf der Startseite. Der Server füllt beim Ausliefern genau diese drei Stellen der Probe-Kopie mit dem Stand (Vorschau: Entwurf), ohne Änderung Byte für Byte wie gebaut (geprüft: neu gezeichnet aus dem Ursprung = gebaute Seite). Je Abend sein echtes Plakat, Datum als Auswahl im Hausstil, «Wer legt auf», «Zeile unter dem Namen», Plakat aus den Plakaten der Bar; «Neuer Abend» (Samstag vier Wochen nach dem neuesten), «Von der Seite nehmen», «Wie gespeichert», Vorher/nachher, Vorschau 1440/390, Frühere Fassungen mit «Ursprünglicher Stand», 409 KONFLIKT bei zwei Fenstern, Prüfung jedes Felds auf dem Server mit Stichwort (Lexikon auf der Prüfseite). |
| Rahmen (`index.html`, `bureau.css`, `fehlermelder.js`, `rundgang.js`, `zur-werkbank.js`, `schweben.*`, `anleitung.*`, `pruefung-haus.*`, `bau.py`) | Kennung `wildside`, Kleid nur aus `--wo-*` (kein eigener Hexwert für Flächen), Schriften Prata/Hanken, Rundgang fünf Schritte mit «Die DJ-Abende», «Zur Werkbank» mit Schlüssel `wildside-wb` (Kopie aus dem Tresen), Fehlermelder an den Server, Prüfseite im Kleid mit Teil «DJ-Abende», Anleitung neun Schritte. |
| `serve.py` | Rahmen um den Server des Stamms wie im Culinarium; dazu: Du der Bar auch in Meldungen und auf der Prüfseite (ohne die Dateien des Stamms zu ändern), Foto-Stufen 640/1000 des gemeinsamen Startbilds auf die vorhandenen Stufen der Website (480/960/1536) abgebildet. |
| Festigkeit (`termine-ansicht.js`, `serve.py`) | Kleine Nachbesserungen am Stamm-Werkzeug, ohne dessen Dateien zu ändern: Gastschichten mit «Ändern» als Zeichen unter dem Namen, Foto-Titel ganz und ohne Einzelwort, lange Werte (Bildbeschreibung, Google-Titel, Instagram-Link) als umbrechende Felder, Suchbeispiel unter «Zeiten & Preise» mit Wörtern der Bar, Satz der Angaben ohne E-Mail, scharfe Kachelfotos; `website.js` wird beim Ausliefern so gefestigt, dass ein Stand nur aus einer Antwort mit Stand übernommen wird. |

## Wie geprüft

- **Schnelle Prüfung** (`tor-schnell.js`, Chromium, 40 Zustände, Tiefe 2, 1440/1280/1000/390) je Schlüssel `schaufenster` und `schaufenster-anleitung`; Funde gelesen, repariert, wiederholt (Ergebnis siehe Schlussmeldung an den Oberchef).
- **Bedient** auf einem Wegwerf-Server (eigene Daten, eigene Probe-Kopie `_probe-schaufenster`): DJ-Abend anlegen, Name tippen (Leiste gelb), Cmd+S, Quittung, Veröffentlichen mit Fenster (nennt den DJ-Abend), Probe-Kopie zeigt den neuen Abend in Kontaktbogen und Flyer, Ursprung zurückgeholt; Text ändern, speichern, veröffentlichen, Frühere Fassungen; Google-Titel im umbrechenden Feld getippt (Leiste zählt, Vorschau schreibt mit). Keine Konsolenfehler.
- **Gleich wie gebaut:** Plakatwand, Kontaktbogen und Flyer aus dem Ursprung neu gezeichnet = die gebauten Seiten Byte für Byte.
- **Auge:** Übersicht, DJ-Abende, Bereich, Foto tauschen, Angaben, Google-Texte, Zeiten & Preise, Gastschichten, Hinweis, Entwurf, Frühere Fassungen, Rundgang, Prüfseite, Anleitung bei 1440/1280/1000/390 angesehen.

## Offen (mit Grund)

- **Dateien des Stamms:** `_Werkzeuge/haeuser/wildside/haus.json` und `_Werkzeuge/werkzeuge/website/haeuser/wildside.json` liegen ausserhalb des Reviers; der Server legt sie beim Start selbst an (`beschreibung.anlegen()`), einchecken kann sie der Oberchef.
- **Plakat eines neuen DJ-Abends:** wählbar sind die Plakate, die die Website schon hat (acht SESSION-Plakate). Ein neues Plakat kommt mit dem nächsten Seitenbau dazu (Bildregister `website/bilder.py`, Stufen in `website/assets/bild/`); bis dahin nimmt der neue Abend eines der vorhandenen.
- **Startbild des gemeinsamen Rahmens** fragt Fotostufen 640/1000 (Culinarium); die Website der Bar hat 480/960/1536. Der Server des Schaufensters bildet das ab; im Rahmen selbst (`oberflaeche/oberflaeche.js`, Revier Tresen) wäre es an einer Stelle zu lösen.
- **Online:** nur lokal; Veröffentlichen schreibt in die Probe-Kopie, nie in `website/`.
