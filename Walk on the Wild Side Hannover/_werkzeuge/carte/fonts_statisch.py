#!/usr/bin/env python3
"""Die Pairing-Karte · Walk on the Wild Side Hannover: feste Schnitte für den PDF-Satz (31.10.2026, Muster der Pairing-Karte im Culinarium).
Chromium bettet variable Schriften im PDF als «Type 3» ein; die Apple-Vorschau zeigt sie dann weich (Fehlerbuch 10a, 21.10.2026). Darum setzt der
Satz feste Schnitte (TrueType je Stärke, Lizenz SIL OFL wie das Original). Quelle der TrueType-Dateien: das google/fonts-Repository.
  · Kleid der Bar (CHARAKTER.md Abschnitt 4): Prata (ofl/prata), Hanken Grotesk 400 und 500 (ofl/hankengrotesk, variabel → fest)
  · Valentinsreihe «Drunk in Love» / «Dishes in Love» im Charakter des Originals (Robert 01.11.2026: «Finde deren mit Pink Panther und Schriftarten
    viel schöner!»): Titan One (ofl/titanone, runde fette Display-Schrift wie «DRUNK IN»), Caveat Brush (ofl/caveatbrush, Pinselschrift wie «LOVE»),
    Montserrat 500 und 600 (ofl/montserrat, variabel → fest, die Zeilen des Originals)

    python3 _werkzeuge/carte/fonts_statisch.py <ordner mit Prata-Regular.ttf, HankenGrotesk.ttf, TitanOne-Regular.ttf, CaveatBrush-Regular.ttf, Montserrat-var.ttf>
"""
import os, shutil, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HIER = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HIER, 'fonts')
FEST = [('Prata-Regular.ttf', 'Prata-400'), ('TitanOne-Regular.ttf', 'TitanOne-400'), ('CaveatBrush-Regular.ttf', 'CaveatBrush-400')]
VARIABEL = [('HankenGrotesk.ttf', 'Hanken-400', 400), ('HankenGrotesk.ttf', 'Hanken-500', 500),
            ('Montserrat-var.ttf', 'Montserrat-500', 500), ('Montserrat-var.ttf', 'Montserrat-600', 600)]

if __name__ == '__main__':
    Q = sys.argv[1] if len(sys.argv) > 1 else F
    os.makedirs(F, exist_ok=True)
    for quelle, name in FEST:
        shutil.copyfile(os.path.join(Q, quelle), os.path.join(F, name + '.ttf'))
        print(name)
    for quelle, name, w in VARIABEL:
        t = TTFont(os.path.join(Q, quelle))
        s = instancer.instantiateVariableFont(t, {'wght': w}, updateFontNames=False)
        s.flavor = None
        s.save(os.path.join(F, name + '.ttf'))
        print(name)
