---
tags: [projekt, website]
status: aktiv
---

# Der Tresen (La Maison) · Walk on the Wild Side Hannover · Funktionsliste (31.10.2026)

Master Werkzeug-Bau 3 (R01–R24) und 4.1 (M01–M27). Vorlage: der abgenommene Tresen des Stamms (28.–30.10.2026), kopiert, umgekleidet, Hauswerte eingetragen; Aufbau, Wege und Funktionen unverändert. Beleg je Zeile: schnelle Prüfung (`_Werkzeuge/abnahme-tor/tor-schnell.js … --nur tresen`, Chromium, 1440/1280/1000/390), Bau-Ausgabe von `bau.py`, Augenprüfung der Bilder.

## Rahmen (R) — der Tresen ändert nichts, R08–R14 betreffen ihn nicht

| Nr | Stand | Beleg |
|---|---|---|
| R01 Aufbau | Leiste, Empfang, Säle, Fuss, Startfehler-Tür, `aria-live` | `bau.py seite()` |
| R02 Auftakt | Fenster in der Motivfarbe sofort da, Fotos blenden nach dem Laden ein, kein Vorhang | Bilder |
| R03 Fehlermelder | `fehler.js` vor allem anderen, Schlüssel `wildside_werkzeuge_fehler`, max. 20, Netzfehler nie | Code |
| R04 Startfehler-Tür | «Der Tresen startet nicht.» mit Grund, «Prüfung öffnen» (Prüfseite des Schaufensters) und «Neu laden»; Wache 12 s | Code |
| R05 Kopfleiste | Insel mit Zeichen + «Der Tresen», Eck-Knöpfe «Anleitungen», «Website ansehen» (Hauptweg rot) | Bilder |
| R06 Rand | als Insel und Fuss (Wege, Anleitungen) | Fuss mit allen sechs Anleitungen |
| R07 Handy | unter 1180 nur Marke; 390 ohne seitliches Verrutschen, Fenster als Bänder | Prüfung 390 |
| R08–R14 | betrifft nicht (der Tresen speichert und veröffentlicht nichts) | — |
| R16 Bühne | Empfang mit fünf Fenstern, Säle mit Kopf, Zeichen, Titel | Bilder |
| R17 Bewegung | nur transform/opacity, «Weniger Bewegung» steht sofort | Code |
| R18 Rundgang | fünf Schritte, Schlüssel `rundgang-wildside-maison`, `?rundgang`, nicht für Prüfprogramme | Bilder der fünf Schritte |
| R19 Zur Werkbank | `zur-werkbank.js`, Schlüssel `wildside-wb`, nur mit Herkunft | Code |
| R20 / M27 Beispiele | Besucherliste und Gästebuch mit beschrifteten Beispielwerten | Stand-Zeilen |
| R21 Hell mit Bühne | Empfang Nacht, Säle im Wechsel Creme / Nacht | Bilder |
| R24 Deutsch | `lang="de"`, Datum `de-DE` | Code |

## Der Tresen (M)

| Nr | Stand | Beleg |
|---|---|---|
| M01 Leiste als Insel | Namen nur, wenn sie zwischen die Eck-Knöpfe passen; Saal im Blick markiert | Bilder |
| M02 Eck-Knöpfe | «Anleitungen», «Website ansehen» | Bilder |
| M03 Gruss nach Tageszeit, Datum | `?gruss=morgen|tag|abend` | Code |
| M04 Empfang | fünf hohe Fenster mit Fotos der Bar (Fenster zur Strasse, Momo giesst, NEGRONI-Glühbirnen, Gäste an der Bar, das Eckschild), darüber Wortmarke, «Der Tresen», Gruss, Datum, Kennzahlen | Bilder |
| M05 Stand je Werkzeug, live | aus den Stand-Wegen (`stand_wege.json`), ohne Antwort Satz ohne Zahl | Bilder |
| M06 Zahlenzeile | «Heute X Besuche · Y zum Tisch · Die Besucherliste öffnen», «Beispiel» leise in der Datumszeile | Bilder |
| M07 Laufband | Namen der Werkzeuge, der Bar, Adresse, Falstaff 91 | Code |
| M08 Säle mit echten Bildschirmen | zehn Bildschirme aus den Werkzeugen (`schirme.js`, nur GET) | Bilder |
| M09 Stücke | Karten aus der Pairing-Karte, Drucksachen aus der Plakatwerkstatt, sechs Fotos der Bar im Saal des Markenbuchs | Bilder |
| M10 Fuss | Wortmarke, Die Bar (Adresse aus `website/bau.py`), Anleitungen, Fragen | Bilder |
| M11 Rundgang | fünf Schritte, Texte für die Bar | Bilder |
| M12 Taste 1–6 | wie Vorlage | Code |
| M13 Zwei Fassungen | `online/` ohne localhost, ohne Platzhalter (Bau bricht sonst ab) | `bau.py baue()` |
| M20 Fassung aus dem Inhalt; Knopf-Namen geprüft | `?v=` = Prüfsumme; jede «Knopf»-Angabe der Tafeln gegen den Code des Werkzeugs (`knoepfe()`) | Bau-Ausgabe |
| M21 Kacheln sanft | nichts hüpft, Foto zoomt ruhig | Code |
| M24 Ecke oben links gleich | Wortmarke der Bar in Rot im Ring, aus dem gemeinsamen Kleid | alle Bildschirme |
| M25 Farben eine Reihe | zwölf Hausfarben aus `livre/livre.json` (ohne die SESSION-Farben) | Bild |
