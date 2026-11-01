#!/usr/bin/env python3
"""Ideen-Engine · Schriften (1.11.2026): die vier Display-Schriften der Plakat-Ideen holen und wie bau.py als TTF (PDF) und woff2 (Bildschirm,
Teilmenge Latein) nach haeuser/wildside/schriften/ legen. Alle frei lizenziert (OFL bzw. Apache 2.0), Lizenztext liegt daneben.
   Archivo Black  (OFL)        fette Grotesk der Fest-Plakate (Christi Limmerfahrt, Oktoberfest)
   Anton          (OFL)        schmale fette Grotesk für Stempel und Zeilen (aus dem Stamm der Werkstatt)
   Yellowtail     (Apache 2.0) Leuchtschrift im Käfig («Two Years»)
   Permanent Marker (Apache 2.0) Handschrift (Info-Tabelle, «LOVE»)
Aufruf im Ordner _werkzeuge/imprimerie:  python3 _bau/engine_schriften.py"""
import os, shutil, urllib.request
from fontTools.ttLib import TTFont
from fontTools import subset

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(HIER, 'haeuser', 'wildside', 'schriften')
GF = 'https://raw.githubusercontent.com/google/fonts/main/'
STAMM = os.environ.get('STAMM', '/tmp/culinarium/Culinarium Hannover/_werkzeuge/imprimerie/haeuser/culinarium/schriften')
SCHRIFTEN = [
    ('ArchivoBlack-400.ttf', GF + 'ofl/archivoblack/ArchivoBlack-Regular.ttf', GF + 'ofl/archivoblack/OFL.txt', 'ArchivoBlack-OFL.txt'),
    ('Anton-400.ttf', os.path.join(STAMM, 'Anton-400.ttf'), os.path.join(STAMM, 'Anton-OFL.txt'), 'Anton-OFL.txt'),
    ('Yellowtail-400.ttf', GF + 'apache/yellowtail/Yellowtail-Regular.ttf', GF + 'apache/yellowtail/LICENSE.txt', 'Yellowtail-LICENSE.txt'),
    ('PermanentMarker-400.ttf', GF + 'apache/permanentmarker/PermanentMarker-Regular.ttf', GF + 'apache/permanentmarker/LICENSE.txt', 'PermanentMarker-LICENSE.txt'),
]
# Latein mit Umlauten, Satzzeichen, Striche, Anführungen, Euro (wie bau.py)
U = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + [0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E, 0x2022, 0x2026, 0x2039, 0x203A, 0x20AC, 0x1E9E]


def hole(quelle, ziel):
    if quelle.startswith('http'):
        with urllib.request.urlopen(quelle, timeout=60) as r:
            open(ziel, 'wb').write(r.read())
    else:
        shutil.copyfile(quelle, ziel)


for datei, ttf, lizenz, lizenz_datei in SCHRIFTEN:
    f = os.path.join(ZIEL, datei)
    if not os.path.exists(f):
        hole(ttf, f)
    if not os.path.exists(os.path.join(ZIEL, lizenz_datei)):
        hole(lizenz, os.path.join(ZIEL, lizenz_datei))
    o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True; o.legacy_kern = True
    ft = TTFont(f); u = subset.Subsetter(o); u.populate(unicodes=U); u.subset(ft); ft.flavor = 'woff2'; ft.save(f[:-4] + '.woff2')
    print(datei, os.path.getsize(f), os.path.getsize(f[:-4] + '.woff2'))
