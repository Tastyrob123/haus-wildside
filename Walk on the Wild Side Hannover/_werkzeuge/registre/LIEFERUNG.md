---
tags: [projekt, website]
status: aktiv
---

# Lieferung · Die Besucherliste (Le Registre, Besuche) · Walk on the Wild Side Hannover

Status: im Nachtbau 31.10.2026 umgestellt, lokal, nichts online, nichts verschickt (Agent «wildside-registre»).

**Werkzeug:** http://127.0.0.1:9286/_werkzeuge/registre/ (Server: `python3 _werkzeuge/registre/server.py 9286` im Hausordner; Bilder ohne Tagesgruss: `?gruss=tag`)
**Anleitung:** http://127.0.0.1:9286/_werkzeuge/registre/anleitung.html (zehn Kapitel, Bilder aus dem Werkzeug, neu aufgenommen)
**Stand-Weg für den Tresen:** http://127.0.0.1:9286/api/registre?tage=30&beispiel=1

## Was steht

- **Kopie der Besucherliste des Culinarium Hannover** (28.10.2026, von Robert abgenommen): Aufbau, Funktionen, Wege, Ansichten und Rechnung unverändert.
- **Kleid Walk on the Wild Side:** Rahmen aus `_werkzeuge/oberflaeche/` (Kleid `wildside`), eigene Teile in `registre.css` und `registre-haus.css` nur über die Töne des Kleids (Nacht, Platte, Creme, Gold als Haarlinie, Rot als Punkt); Prata für Titel, Hanken Grotesk für Lauf und Etiketten; Zeichen ist die Wortmarke WALK / ON THE / WILD SIDE. Rundgang-Karte und «Zur Werkbank» im Kleid wie im Tresen.
- **Bühnen** je Ansicht mit Fotos der Bar aus dem Bildregister der Website (`/assets/bild/<schlüssel>-480/-960.webp`): Übersicht das Eckschild bei Nacht, Besuche Momo giesst, Herkunft die rote Tür, Zeit die volle Bar, Seiten die NEGRONI-Glühbirnen, Verlauf die Decke über der Bar, Zum Tisch zwei Gläser, So wird gezählt die Flaschen der Bar.
- **Seiten der Website** (`python3 registre.py seiten`): Startseite, Drinks, Programm, Feiern, Das Haus, Besuch, Impressum, Datenschutz, Namen aus der Leiste der Website; je Seite ihr erstes Foto (Plakate ausgenommen).
- **Wege der Bar** (Master G14, Schlüssel wie in allen Häusern): `fenster` Reservieren begonnen · `buchung` Tisch reserviert (erst mit «Danke») · `tisch` Feier-Anfrage begonnen · `booking` Feier angefragt · `anfrage` Knopf «Reservieren» · `anruf` Telefon der Bar · `mail` Instagram der Bar · `chat` weiter zu Culinarium oder Dirty Chicken · `route` Karte auf «Besuch». «Zum Tisch» = reserviert oder angefragt.
- **Eigene Zählung des Hauses** (Master G09): eigener Schlüssel (in der Cloud-Sitzung erzeugt unter `/home/user/_Schluessel/wildside-hannover.txt`, nicht eingecheckt; nur seine Prüfsumme in `anschluss.py` und `online/registre.py`), eigenes Geheimnis, eigener Speicher. Vorführ-Betrieb an: der Kunde sieht nur Beispielwerte.
- **Beispielwerte der Bar**, überall als Beispiel beschriftet: Hannover und Region, dazu Hildesheim, Braunschweig, Hamburg, Berlin, wenige von weiter her; Herkunft vor allem Instagram und Google, dazu Falstaff und NeoTaste; mehr Besuche donnerstags bis samstags und am Abend.
- **Zählung für die Website liegt bereit, ist nicht eingebaut:** `vorschlag/messung.js` (Formulare `form.rh-form` und `form.formular`, Telefon, Instagram, Vitrine, Karte) und `vorschlag/datenschutz-text.md`. Einbau nur auf Roberts Wort.

## Wie geprüft

- Schnelle Prüfung (tor-schnell, Chromium, 1440/1280/1000/390, höchstens 40 Zustände, zwei Ebenen) für `besucherliste` und `besucherliste-anleitung`; Zustandsbilder mit dem Auge angesehen.
- Der alte Volllauf `abnahme.js` ist auf die Wege der Bar umgestellt, im Nachtbau aber nicht gelaufen (Robert: nur auf ausdrücklichen Wunsch); `FUNKTIONSLISTE.md` zeigt deshalb «Noch kein Lauf».
