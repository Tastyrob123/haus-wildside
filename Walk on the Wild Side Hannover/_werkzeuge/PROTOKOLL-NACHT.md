---
tags: [projekt, website]
status: aktiv
---

# Protokoll Nachtbau · Walk on the Wild Side Hannover (31.10./1.11.2026, Oberchef)

Auftrag: `AUFTRAG-NACHT.md`, `CLAUDE.md` («Der Deal»). Stamm: Werkzeuge und Werkbank des Culinarium Hannover, kopiert, umgekleidet, Hauswerte eingetragen.

## Ablauf

| Zeit (UTC) | Was |
|---|---|
| 17:10 | Auftrag gelesen, Vorbild Culinarium geholt, Kundenmaterial (Zweig `quelle`) verlinkt |
| 17:20 | Sieben Werkzeuge + Werkbank aus dem Culinarium kopiert (ohne Prüfordner/Sicherungen), gemeinsames Kleid `oberflaeche/kleid/wildside.{js,css}` + echte Wortmarke, Ziellisten `ziele-wildside.json` (Tor, Messlauf), `AUFTRAG-GEMEINSAM.md` |
| 17:25 | Acht Bau-Agenten parallel (je Werkzeug einer, dazu die Werkbank), alle Opus |
| 17:35 | Probelauf der Cloud-Prüfung (GitHub Actions) bestätigt: Ablauf läuft durch |
| 18:20–19:45 | Werkzeuge «fertig» (lokal Chromium 0 Funde), danach je Werkzeug Cloud-Prüfung in WebKit, Funde zurück an die Agenten, Nachprüfung bis 0 |
| 20:15 | Werkbank-Agent hing seit 17:32 an einem einzigen Shell-Befehl (Freigabe-Abfrage für ein eingebettetes Skript). Weg gewechselt: drei Werkbank-Agenten (Kern, Papier, Feed/Mails/Material), Regel «keine eingebetteten Skripte in der Shell» |
| 20:40 | Kern-Agent hing erneut an derselben Art Befehl → angehalten und mit der Regel fortgesetzt |
| 22:41 | Container-Neustart: Server und Verweise neu eingerichtet, Agenten fortgesetzt, nichts verloren (alles war committet) |
| 22:50 | Voller Probelauf über alles (`[schnell]`, main) |

| 23:20 | Abschlusslauf über alles (Zweig): 26 Teile ausgewertet, zwei Rechner der Besucherliste hingen 50 min beim Einrichten (GitHub, nicht unser Code) → Lauf nach Werkbank/KI abgebrochen, Auswertung geschrieben |
| 00:15 | Werkbank: Ziffern-Knöpfe in WebKit (Weiche `-apple-system-body` erkennt WebKit unter Linux nicht → Chromium-Weiche); Nachprüfung Werkbank + Besucherliste auf main (`main-teil`) |
| 00:20 | Tresen und Plakatwerkstatt letzte Funde; Nachprüfung Zweig (`…-teil`): Tresen 0, Plakatwerkstatt 0, Mail-Seite 20 → behoben |
| – | Ablauf `schnell.yml`: Teilprüfungen schreiben nach `<zweig>-teil`, die volle Tafel `<zweig>-schnell` bleibt stehen |

## Prüfregeln geschärft (mit Beleg, nie Funde wegerklärt)

- **Versalien (Stil):** Wild Side setzt Etiketten in Hanken 500 gesperrt in Versalien (`website/assets/wild.css`, 22× `text-transform:uppercase`). Ziellisten-Fallback `stil.versalienNur = Hanken`; das Stilblatt `imprimerie/haeuser/wildside/stilblatt.json` führt die Rolle «etikett» mit Hanken und Versalien.
- **leer-bild** (`abnahme-tor/seite.js`): nur Flächen, deren Mitte im Fenster liegt und die obenauf sind. Beleg: Schaufenster Zustand 021 «Foto tauschen» – die runden Kopf-Knöpfe lagen unter dem offenen Fenster und galten als «leer»; Gästebuch/Schaufenster – Bilder unterhalb des Fensters malt WebKit erst beim Hinscrollen.
- **loch/mitte** (`abnahme-tor/tor-schnell.js`): Blätter, die über die Aufnahme hinausreichen (eigene Scroll-Fläche), werden nicht als Loch gemessen. Beleg: Plakatwerkstatt `034-d0.png` (Blatt 294 px, Aufnahme 122 px). Ein Zeilenfehler aus dieser Änderung (22:22–22:40) ist behoben.
- **Ziel Tresen** mit Einstieg `?rundgang` (wie die anderen Werkzeuge).

## Gemeinsame Lösungen (für alle Häuser lehrreich)

- **WebKit hängt nach dem letzten Buchstaben keinen Sperrabstand an, Chromium schon.** Ausgleich für gesperrte Versalien in Knöpfen nur in Chromium (`@supports (interpolate-size:allow-keywords)`), Grundfall symmetrisch; senkrecht `text-box: trim-both cap alphabetic` statt Polster-Versätzen. Im Kleid: `--wo-sperr`, `.wo-sperr-mitte`; in der Werkbank `knopf_mitte.css/js`.
- **WebKit malt lazy Bilder unterhalb des Fensters in Ganzseiten-Aufnahmen nicht** → Kachel- und Listenbilder `loading="eager" decoding="sync"`.
- **WebKit setzt Prata breiter** → Handy-Titel mit Luft (`min(36px, 8.6vw)`), Namen in Ecken nie mit «…».
- **Subagenten nachts:** keine Heredocs / `python3 -` in der Shell (wartet auf Freigabe), Skripte mit dem Schreibwerkzeug anlegen; Wache auf still stehende Agenten.

## Offen beim Kunden zu klären (kein Bau-Fehler, nichts erfunden)

- E-Mail-Adresse der Bar nicht belegt (die Angebotsmappe nennt die von Culinarium) → überall Telefon/Instagram/Formular.
- Preis des Privaten Dinners steht nicht auf der Website → im Brief des Gästebuchs als offenes Feld.
- Laufende Karte von Momo: keine Drinks belegt → Pairing-Karte zeigt beschriftet die Valentinskarte als Beispiel; Klassiker ohne Preise.
- Nächster DJ-Abend nicht angekündigt → SESSION-Vorlagen zeigen vergangene Abende.
- Website (nicht angefasst, gehört Roberts Website-Chat): Startseite sagt noch «Eine Getränkekarte gibt es im Wild Side nicht.» (widerspricht der Kundin 30.10.); Fuss verlinkt Culinarium/Dirty Chicken auf `localhost:8765`.
- Wortmarke: die nachgezogene Vorlage zeigt WILD SIDE in der roten Fläche ohne die kleine Zeile «WALK ON THE»; so verbaut wie auf der Website.

## Wo was liegt

- Werkzeuge: `Walk on the Wild Side Hannover/_werkzeuge/<maison|bureau|carte|reception|livre|registre|imprimerie>/` (je `LIEFERUNG.md`), Kleid `oberflaeche/` (`UMSTELLUNG.md`).
- Drucksachen: `_werkzeuge/imprimerie/haeuser/wildside/drucksachen/` (`LISTE.md`), in der Werkbank unter `drucksachen/`.
- Werkbank: `Walk on the Wild Side Hannover/website/_werkbank/` (Start, Karte, KI, Geprüft, Befund, Unterlagen, Drucksachen, Untersetzer, Sticker, Postkarten, Beigaben, Feed, Mails, Material). Lokal: `bash cloud/server.sh`, dann http://127.0.0.1:9088/werkbank/index.html.
- Prüftafel: Zweig `ergebnis`, `ergebnis/laeufe/main-schnell/tor/index.html`.
