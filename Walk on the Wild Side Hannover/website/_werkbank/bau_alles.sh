#!/bin/bash
# Werkbank Walk on the Wild Side: das ganze Paket bauen (Nachtbau 31.10.2026, Vorlage bau_alles.sh des Culinarium).
#   bash website/_werkbank/bau_alles.sh [--ohne-aufnahmen]
# Revier: website/_werkbank/ ist der Projektordner des Kits; die Website liegt eine Ebene höher und wird nur gelesen (assets ist ein Verweis).
# Voraussetzung: Vorschau-Server läuft:  python3 website/_werkbank/serve.py 9288, Werkzeug-Server 9281–9287 (cloud/server.sh). Kit unverändert, headless, nichts geht online.
# Teile: Kern (Startseite, Befund, KI, Karte, Geprüft), Papier (Unterlagen, Drucksachen, Untersetzer, Sticker, Beigaben, Postkarten), Feed/Mails/Dateien.
set -e
K="${WERKBANK_KIT:-$(cd "$(dirname "$0")/../../.." && pwd)/_Werkbank-Kit}"
P="$(cd "$(dirname "$0")" && pwd)"; cd "$P"
export PYTHONPATH="$K:$P/_werkbank" WB_PORT=9288
python3 "$K/kern.py" "$P" | grep -v "Schrift fehlt" || true
python3 "$K/schriften.py" "$P" > /dev/null || true
timeout 300 python3 _werkbank/druckschrift.py > /dev/null           # Prata und Hanken als feste Druckschnitte (nach schriften.py, das die Kit-Namen anlegt)
if [ "$1" != "--ohne-aufnahmen" ]; then
  timeout 900 node _werkbank/ansicht_lang.js "$P"                    # jede Seite der Website am Rechner und am Handy
  timeout 900 node _werkbank/sb_ideen.js                             # Ideen und Gäste-Funktionen
  timeout 900 node _werkbank/sb_werkzeuge.js                         # Bildschirme der sieben Werkzeuge (Adressen aus _werkbank/werkzeuge.json)
  timeout 300 node _werkbank/heute/befund_bilder.js || true          # nur mit _quelle/: Aufnahmen für den Befund (liegen danach in _werkbank/heute/)
fi
python3 _werkbank/sb_heute.py                                        # heute (Instagram) und neu
# ---------- Papier (Werkbank Papier) ----------
timeout 300 python3 _werkbank/papier.py "$P"
timeout 900 node "$K/papier_druck.js" "$P" > /dev/null
timeout 300 python3 "$K/papier_seiten.py" "$P" | grep -v "Schrift fehlt" || true
timeout 600 python3 _werkbank/sb_karten.py
timeout 600 python3 _werkbank/sb_karten.py --seite | grep -v "Schrift fehlt" || true
timeout 120 python3 _werkbank/sticker.py "$P"
timeout 120 python3 _werkbank/beigaben.py "$P"
rm -rf _werkbank/roh/einzel-sticker
timeout 900 node _werkbank/sticker_druck.js "$P" > /dev/null
timeout 300 python3 _werkbank/sticker.py "$P" --seite
timeout 300 python3 _werkbank/beigaben.py "$P" --seite
timeout 120 python3 _werkbank/postkarten.py "$P"
timeout 900 node _werkbank/postkarten_druck.js "$P" > /dev/null
timeout 300 python3 _werkbank/postkarten.py "$P" --seite
timeout 120 python3 _werkbank/papier_nach.py
# ---------- Feed, Mails, Dateien ----------
python3 "$K/feed.py" "$P"; node "$K/feed_druck.js" "$P"; python3 "$K/feed.py" "$P"; node "$K/feed_druck.js" "$P" --handy
python3 _werkbank/feed_leicht.py "$P" 2>/dev/null || python3 _werkbank/feed_leicht.py
node _werkbank/geraete/schirme.js feed || true
python3 mails/_src/bau.py; node mails/_src/aufnahme.js
python3 "$K/material.py" "$P" | grep -v "Schrift fehlt" || true
python3 _werkbank/material_mehr.py "$P"
node "$K/ziele.js" "$P" || true
# ---------- Kern: Startseite, Befund, KI, Karte «Ein Vorschlag.», Geprüft ----------
node _werkbank/sb_strom.js || true                                   # Befund, Prüfbericht, Karte, Markenbuch für die Objekte
python3 _werkbank/objekte_bau.py "$P"
python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"                    # die Werkbank (ruft haus.nach_bau: Kapitel, Befund, KI-Seite, Ihr-Form, Kleid)
node _werkbank/sb_strom.js || true
python3 _werkbank/objekte_bau.py "$P"
python3 "$K/bau.py" "$P" | grep -v "Schrift fehlt"
python3 _werkbank/ruecksprung.py "$P"                                 # zuletzt: Rücksprung auf die alte Höhe in jeder Seite (auch nach den Bauten der Beigaben)
echo "fertig: http://127.0.0.1:9288/werkbank/"
