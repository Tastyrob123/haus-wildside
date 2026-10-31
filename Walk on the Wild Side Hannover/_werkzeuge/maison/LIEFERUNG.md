---
tags: [projekt, website]
status: aktiv
---

# Der Tresen (Zentrale, Arbeitsname La Maison) · Walk on the Wild Side Hannover · Lieferung 31.10.2026

Status: siehe letzter Commit «Tresen: …». Agent `wildside-maison` im Nachtbau. Nichts online, nichts verschickt.

**Adressen** (nur lokal)
- Der Tresen: http://127.0.0.1:9081/_werkzeuge/maison/ (Prüfserver `python3 server.py 9081` im Ordner `_werkzeuge/maison`)
- Rundgang: http://127.0.0.1:9081/_werkzeuge/maison/?rundgang
- Gemeinsames Kleid, Musterseite: http://127.0.0.1:9081/assets/oberflaeche/muster.html?haus=wildside · Anleitung `_werkzeuge/oberflaeche/UMSTELLUNG.md`

## Was steht

1. **Kopie des abgenommenen Tresens** (Stamm 28.–30.10.2026): gleicher Aufbau, gleiche Wege, gleiche Funktionen (Leiste als Insel, Empfang mit fünf Fenstern, Zahlenzeile der Besucherliste, Laufband, je Werkzeug ein Saal mit echten Bildschirmen und der Tafel «So geht’s», Weg zum Tisch, Fuss mit allen Anleitungen, Rundgang, Startfehler-Tür, «Zur Werkbank», Online-Fassung).
2. **Kleid der Bar** (das Eckschild): Nacht, Platten mit Gold-Haarlinie, Creme der weissen Plakate, Rot nur als Punkt (Wortmarke, «Website ansehen»); Prata und Hanken Grotesk; Wortmarke der Bar aus `kleid/wildside-marke.svg`, im Ring oben links wie in allen Werkzeugen.
3. **Inhalt der Bar**: Fotos nur aus dem Bildregister der Website (`website/bilder.py`): Blick durchs Fenster, Momo giesst, NEGRONI-Glühbirnen, zwei Gäste an der Bar, das Eckschild; im Saal des Markenbuchs Decke, Theke, Rückbar, Coupe, ein voller Abend, Momo. Adresse aus `website/bau.py` (`HAUS`). Sätze je Werkzeug für die Bar (wechselnde Karte von Momo, DJ-Abende, Feiern, Reservieren). Stufen «Weg zum Tisch» wie die Besucherliste (`registre.js trichter()`).
4. **Stücke der Säle** aus den Werkzeugen: drei Karten der Pairing-Karte (gesetztes Blatt, `kartenblatt.js`), drei Drucksachen der Plakatwerkstatt (SESSION-Aushang A3, Tischaufsteller «Was magst du?», Beitrag «Der Negroni»), zwölf Hausfarben aus dem Markenbuch. Holen: `python3 stuecke.py`, Bildschirme: `node schirme.js`, dann `python3 bau.py`.
5. **Gemeinsames Kleid** `_werkzeuge/oberflaeche/` geprüft und nachgeschärft (Änderungen in `UMSTELLUNG.md`).

## Wie geprüft

Schnelle Prüfung lokal (`node _Werkzeuge/abnahme-tor/tor-schnell.js _Werkzeuge/abnahme-tor/ziele-wildside.json /tmp/aus-tresen --nur tresen --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390`), dazu Augenprüfung der Bilder in allen vier Breiten und der fünf Rundgang-Schritte. Ergebnis im letzten Commit.
