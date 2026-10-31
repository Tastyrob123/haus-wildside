---
tags: [projekt, website]
status: aktiv
---

# Lieferung Das Gästebuch (Team hinter dem Gäste-Chat) · Walk on the Wild Side Hannover (31.10.2026, Nachtbau)

Kopie des abgenommenen Gästebuchs aus dem Culinarium Hannover, umgekleidet und mit den Werten der Bar. Gleicher Aufbau, gleiche Wege, gleiche Funktionen. Nichts online, nichts verschickt, keine KI aufgerufen (Probe-Antworten, `probe_ki.py`), kein Schlüssel gelesen.

**Adresse:** http://127.0.0.1:9084/_werkzeuge/reception/ · Anleitung `anleitung.html` · Prüfung `pruefung.html`
Start aus dem Hausordner: `python3 _werkzeuge/reception/server.py 9084` (liefert die Website unter `/`, das Kleid unter `/assets/oberflaeche/`, den Chat unter `/api/gast`).

## Was steht

- **Kleid:** Eckschild der Bar (`kleid/wildside.css` + `wildside-reception.css`): Nacht, Platte, Creme, Gold als Haarlinie, Rot als Punkt; Prata und Hanken Grotesk, nie fett, nie kursiv (`font-synthesis:none`). Farben der Kopie mit `_bau/wildside_kleid.py` umgerechnet. Zeichen und Briefkopf: die echte Wortmarke (WALK / ON THE / WILD SIDE) in Rot, `zeichen-haus.svg`, `marke-haus.svg`, `marke-haus-weiss.png` (für den Mail-Satz).
- **Eingang** mit vier Arten: Reservieren (Platz an der Theke), Privates Dinner, Feier (lange Tafel, ganze Bar, grosses Event), Nachricht. Hinweise je Anfrage aus den Angaben der Website, nie gespeichert: Bar geschlossen (Sonntag bis Mittwoch), ab zehn Gästen die lange Tafel, Format passt nicht zur Zahl (Dinner 10–14, Tafel 10–20, ganze Bar ab 30), Allergien (Rudi fragen beim Dinner; an normalen Abenden kein Essen), Anzahlung 30 Prozent eine Woche vorher.
- **Brief** im Du der Website, Kopf mit der Wortmarke, Fuss mit Adresse, beiden Telefonnummern und Instagram (keine Mail-Adresse: nicht belegt). Vorlagen nur aus dem Wortlaut der Website (`vorlagen/reservieren.txt`, `dinner.txt`, `feier.txt`, gebaut von `_bau/wildside_wissen.py`, jeder Satz wörtlich geprüft). PDF «Walk on the Wild Side – Name – Datum.pdf».
- **Wissen des Chats** aus dem Wortlaut der Website (`_bau/website_text.js` headless gegen :9084, ohne Vorführ-Hinweise), Steckbrief mit 61 belegten Zeilen in neun Bereichen (`steckbrief_bau.py`). Der Satz der Startseite «Eine Getränkekarte gibt es im Wild Side nicht.» ist bewusst draussen (Kundin 30.10.2026: die Karte wechselt).
- **Chat ausprobieren** im Kleid der Bar; ohne KI antwortet er aus dem Steckbrief (belegte Zeilen), Lücken (Hund, Parken, Allergien) gehen als «ohne Antwort» ans Team.
- **Beispiele:** sieben Anfragen, zehn Fragen (zwei mit Absicht ohne Antwort), erfundene Gäste mit example.com, beschriftet (`_bau/wildside_beispiele.py`, prüft jede Zahl gegen das Wissen).
- **Baustein** `baustein/anfrage.js` für «Ein Platz für euch.» (besuch.html) und «Euer Abend» (tafel.html), auf der Website nicht eingebaut (`baustein/ANLEITUNG.md`).
- Anleitung mit zwölf Kapiteln auf die Bar umgeschrieben, Bilder neu (`_bau/anleitung_bilder.js`).

## Offen, mit Grund

- Preis des Privaten Dinners steht nicht auf der Website: im Brief als offenes Feld [Preis klären].
- E-Mail-Adresse der Bar nicht belegt: Brief und Chat nennen Telefon und Instagram.
- Allergien: die Website sagt nichts; der Chat gibt die Frage ans Team.
- Baustein auf der Website nicht eingebaut (Revier Website).
