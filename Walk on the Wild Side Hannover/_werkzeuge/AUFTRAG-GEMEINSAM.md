---
tags: [projekt, website]
status: aktiv
---

# Walk on the Wild Side Hannover · Werkzeuge, Werkbank, Drucksachen, Prüfung — gemeinsamer Auftrag (Oberchef, Nachtbau 31.10./1.11.2026)

Robert, 31.10.2026 (`AUFTRAG-NACHT.md`, `CLAUDE.md` «Der Deal»): Ein Tag (eine Nacht) für das ganze Paket: Werkbank, die sieben Werkzeuge, Drucksachen, Prüfung, Übergabe. **Fertig um 09:00 Uhr Ortszeit Robert (01:00 UTC).** «Fertig» heisst: Robert öffnet den Link und könnte das Paket so an den Kunden schicken. **Nichts neu erfinden: kopieren, umkleiden, Hauswerte eintragen.**

Vorlage dieser Datei: `Culinarium Hannover/_werkzeuge/AUFTRAG-GEMEINSAM.md` (28.10.2026), Hauswerte getauscht. Stamm: die sieben Werkzeuge und die Werkbank des Culinarium (`https://github.com/Tastyrob123/haus-culinarium-hannover`, Kopie in `/tmp/culinarium/`) sind schon nach `_werkzeuge/` und `website/_werkbank/` kopiert (ohne Prüfordner und Sicherungen); das gemeinsame Kleid `_werkzeuge/oberflaeche/kleid/wildside.{js,css}` + `wildside-zeichen.svg` + `wildside-marke.svg` ist angelegt, alle Verweise zeigen darauf.

## Das Haus in drei Zeilen

Walk on the Wild Side ist eine **Nachbarschafts-Mixology-Bar** in Linden-Mitte (Haasemannstraße 13, Ecke Rampenstraße, 30449 Hannover). Derya Ivkin führt die Bar seit Herbst 2023, Mohamed «Momo» Ben Khelifa entwirft die Drinks; die Karte **wechselt** (nie «keine Karte» oder «einmal im Jahr eine Karte» schreiben, Kundin 30.10.2026), an der Bar sagst du, was du magst. Offen Do 19–1, Fr/Sa 19–2 Uhr; DJ-Abende «SESSION» samstags, Konzerte, Feiern und Private Dinner auf der Empore (Angebotsmappe: `website/tafel.html`). Falstaff Bar Guide 2027: 91 Punkte. Culinarium (Food-Pairing-Abende) und Dirty Chicken laufen im selben Haus, hier nur als Verweis. Alles Weitere: `CHARAKTER.md`.

Für die Werkzeuge heisst das (Aufbau und Funktionen aus dem Culinarium bleiben, Inhalt kommt aus diesem Haus): Karten = die wechselnde Karte von Momo, Klassiker, Sonderkarten (Valentinskarte «Drunk in Love» mit Preisen vom Plakat, `website/drinks.html`); Termine = DJ-Abende (`LINEUP` in `website/bau.py`), Konzerte, Feste (`website/programm.html`); Anfragen = Reservieren und Feiern (`website/besuch.html`, `website/tafel.html`); Drucksachen = SESSION-Plakate (Rot/Creme-Wellen, Ultramarin-Schrift), weisse Plakate mit roter Wortmarke, Karte, Untersetzer; Gäste-Chat = Fragen zu Zeiten, Plätzen, Feiern, DJ-Abenden.

## Wer was macht (je Agent genau ein Revier)

| Agent | Revier (nur hier schreiben) | Port | Schlüssel im Tor |
|---|---|---|---|
| wildside-maison (Der Tresen) | `_werkzeuge/maison/` **und** `_werkzeuge/oberflaeche/` (einziger Schreiber) | 9081 | `tresen` |
| wildside-bureau (Das Schaufenster) | `_werkzeuge/bureau/` | 9082 | `schaufenster`, `schaufenster-anleitung` |
| wildside-carte (Die Pairing-Karte) | `_werkzeuge/carte/` | 9083 | `pairing-karte`, `pairing-karte-anleitung` |
| wildside-reception (Das Gästebuch) | `_werkzeuge/reception/` | 9084 | `gaestebuch`, `gaestebuch-anleitung` |
| wildside-livre (Das Markenbuch) | `_werkzeuge/livre/` | 9085 | `plakatarchiv`, `plakatarchiv-buch`, `plakatarchiv-anleitung` |
| wildside-registre (Die Besucherliste) | `_werkzeuge/registre/` | 9086 | `besucherliste`, `besucherliste-anleitung` |
| wildside-imprimerie (Die Plakatwerkstatt + Drucksachen) | `_werkzeuge/imprimerie/` | 9087 | `plakatwerkstatt`, `plakatwerkstatt-mail` |
| wildside-werkbank | `website/_werkbank/` | 9088 | `werkbank*` |

Oberchef: Ziellisten `_Werkzeuge/abnahme-tor/ziele-wildside.json`, `_Werkzeuge/messlauf/ziele-wildside.json`, `cloud/`, Commits und Pushes, Paketprüfung. `website/` (die Website selbst) ändert **niemand** (nur lesen).

## Kleid: Wild Side, nicht Culinarium umgefärbt

Gleicher Aufbau, gleiche Wege, gleiche Funktionen wie im Culinarium. Das Kleid kommt aus der Website des Hauses (`CHARAKTER.md` Abschnitt 4, `website/assets/wild.css`):
- **Farben:** Nacht `#130E0D`, Platte `#1C1513` / `#261E1A`, Creme `#F2E9DC` (die weissen Plakate der Bar), Gold `#D8B264` nur als Haarlinie, Etikett, Knauf; Rot `#F0323F` nur als Punkt (Hauptknopf, Logo); Ultramarin `#1A00AA` und Plakatrot `#D21C0A` nur bei den DJ-Abenden/SESSION-Plakaten. Im Werkzeug nur die Variablen `--wo-*` aus `kleid/wildside.css`, keine eigenen Hexwerte für Flächen.
- **Schrift:** Titel **Prata** (eine Stärke, nie fett, nie kursiv), Lauf **Hanken Grotesk** 400, Etiketten Hanken 500 gesperrt, Zahlen Hanken mit `tabular-nums`. Dateien: `/assets/schrift/prata-latin.woff2`, `/assets/schrift/hanken-latin.woff2` (aus `website/assets/schrift/`). Fraunces, Urbanist, Instrument Sans, DM Mono gibt es hier **nicht**: jede Stelle umstellen (auch in Druck-/PDF-Satz, eingebetteten Schriften, Canvas).
- **Wortmarke:** nur das echte Logo (drei Zeilen WALK / ON THE / WILD SIDE, nachgezogen): `<svg viewBox="0 0 1296 1600"><use href="/assets/oberflaeche/kleid/wildside-marke.svg#wm"/></svg>`, Farbe über `color` (Rot `#F0323F` oder Creme). Nie als Schrift nachbauen. Das «C» des Culinarium, das «x» von «Momo x Rudi», Kerzenlicht-Orange (#EF7649, #F5A689, #B15736), Nacht-Violett (#16141B/#3A3845) dürfen nirgends mehr stehen.
- **Form:** das Eckschild: Platten 18 px Radius mit Gold-Haarlinie innen und weichem Schatten, Kacheln 14 px; Knöpfe als Schild mit rundem Knauf (Rot mit Creme-Knauf = Hauptweg, Nacht mit Goldlinie und Gold-Knauf = Nebenweg). Keine Einkerbungen, keine Punkt-Etiketten, keine Pillen-Reihen, keine Tickets/Platzkarten/Leuchtschrift/Sticker-Optik des Culinarium.
- **Fotos:** nur aus `website/assets/bild/` (Register `BILD`/`mache()` in `website/bau.py`, Schlüssel z. B. `schild-ecke`, `momo-giesst`, `decke-raum`, `negroni`, `fenster`, `theke`, `rueckbar`, `derya`, `konzert`, `an-empore-tafel`, `p-1710` … Plakate `p-*`). Ausgeliefert unter `/assets/bild/<schlüssel>-<breite>.webp` (Breiten je Bild in `ls website/assets/bild/<schlüssel>-*`). Kein Bild von Culinarium-Tellern als Hausbild.

## Hauswerte (nie abtippen, aus der Quelle lesen und gegen sie prüfen)

`website/bau.py` (`HAUS`: Adresse, Telefon, Instagram, Zeiten; `LINEUP`: DJ-Abende), `website/*.html` (Texte, Drinks, Programm, Tafel-Angebote mit Preisen, Fragen), `CHARAKTER.md`, `_kette/06-konzepter/KONZEPT-2026-10-28.md`, Kundenmaterial `_quelle/` (Verweis auf den Zweig `quelle`; liegt nur hier in der Sitzung, **nicht in GitHub Actions** — zur Laufzeit darf kein Werkzeug etwas aus `_quelle/` laden: was gebraucht wird, ins eigene Revier kopieren). Preise nie raten: fehlt eine Zahl, bleibt sie offen (in der Meldung an den Oberchef nennen). **E-Mail-Adresse der Bar ist nicht belegt** (die Mappe nennt die von Culinarium): keine erfinden, Kontakt über Telefon/Instagram/Formular.

## Namen der Werkzeuge

Wie im Culinarium (Robert 28./29.10.2026): Der Tresen · Das Schaufenster · Die Pairing-Karte · Das Gästebuch · Das Markenbuch · Die Besucherliste · Die Plakatwerkstatt. Nur über `WO.name('<teil>')` bzw. `WO_HAUS.namen` (eine Stelle: `kleid/wildside.js`), nie fest schreiben. Dateien, Ordner, Schlüssel, Ports bleiben.

## Feste Regeln für jeden Agenten

- Keine Fragen an Robert. Offenes in die Schlussmeldung an den Oberchef.
- Nur im eigenen Revier schreiben. `oberflaeche/` nur `wildside-maison`; wer dort etwas braucht, löst es im eigenen CSS und nennt es in der Meldung.
- Haus-Kennung überall `wildside` statt `culinarium` (Ordner `haeuser/culinarium` → `haeuser/wildside`, Speicher-Schlüssel, localStorage `ds-culinarium-*` → `ds-wildside-*`, Dateinamen wie `culinarium.css` → `wildside.css` mit allen Verweisen). Am Ende im eigenen Revier: `grep -rIn -i "culinarium\|rudi\|fraunces\|urbanist\|instrument\|dm mono\|EF7649\|F5A689\|B15736\|16141B\|3A3845\|Beau-Rivage\|Schäfli\|Schlössli" <revier>` — jeder Treffer muss gewollt sein (Verweis «Unsere Abende an der langen Tafel: Culinarium» ist gewollt; Rudi nur, wo er im Haus wirklich vorkommt, z. B. Private Dinner).
- Kein Platzhalter, kein «Lorem», kein «TODO», keine leere Kachel, keine erfundenen Namen/Preise/Termine.
- Headless (Chromium hier), eine Instanz, eigene Prozesse per PID beenden, **nie pkill/killall** auf chrome/python/node. mailto/tel nie ausführen. Nichts verschicken, nichts veröffentlichen, nichts online stellen. KI nur mit Probe-Antworten (kein `*_KI=1`, keine Schlüssel).
- Server laufen schon (`bash cloud/server.sh`, Logs `/tmp/server/<port>.log`). Startet dein Server nach einer Änderung an Python neu: nur deinen eigenen Prozess (PID über `ss -ltnp | grep :<port>`) beenden und mit dem Befehl aus `cloud/haus.json` im richtigen Ordner neu starten (`nohup … > /tmp/server/<port>.log 2>&1 &`).
- Git: nur das eigene Revier committen (`git add "<revier>" && git commit -m "<Werkzeug>: …"`), nie `git add -A`, nie pushen (pusht der Oberchef), kein Force. Schlägt der Commit wegen `index.lock` fehl: 5 s warten, wiederholen.

## Prüfen (jedes Werkzeug gleich nach dem Bau, dann reparieren, noch einmal)

Lokal mit derselben schnellen Prüfung wie in Actions (Chromium):
```
cd /home/user/haus-wildside && node _Werkzeuge/abnahme-tor/tor-schnell.js _Werkzeuge/abnahme-tor/ziele-wildside.json /tmp/aus-<k> --nur <k> --browser chromium --max 40 --tiefe 2 --breiten 1440,1280,1000,390
```
Ergebnis in `/tmp/aus-<k>/<k>/` (Inventar, Bilder, Funde). Dazu mindestens 15 Zustandsbilder je Werkzeug mit dem Read-Werkzeug ansehen (Kriterien A in `_Werkzeuge/ROBERTS-KRITERIEN.md`: Zustände, die ein Kunde öffnet, vier Breiten, Auge an den Bildern, nichts Culinarium-Haftes mehr sichtbar). Fertig = null offene Funde, nichts «nicht erreicht», alles im Kleid des Hauses mit Inhalt des Hauses.

## Reihenfolge

Tresen, Schaufenster, Pairing-Karte, Gästebuch, Markenbuch, Besucherliste, Plakatwerkstatt laufen parallel; die Werkbank baut Rahmen und Seiten sofort und holt die Bildschirme der Werkzeuge, sobald sie fertig sind. Am Ende `[schnell]` über alles (Oberchef).
