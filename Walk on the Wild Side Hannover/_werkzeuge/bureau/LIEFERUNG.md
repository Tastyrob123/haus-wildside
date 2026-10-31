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
