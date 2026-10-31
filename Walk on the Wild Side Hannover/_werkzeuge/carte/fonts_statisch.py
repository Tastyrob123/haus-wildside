#!/usr/bin/env python3
"""Die Pairing-Karte · Walk on the Wild Side Hannover: feste Schnitte für den PDF-Satz (31.10.2026, Muster der Pairing-Karte im Culinarium).
Chromium bettet variable Schriften im PDF als «Type 3» ein; die Apple-Vorschau zeigt sie dann weich (Fehlerbuch 10a, 21.10.2026). Darum setzt der
Satz feste Schnitte (TrueType je Stärke, Lizenz SIL OFL wie das Original). Schriften der Website (CHARAKTER.md Abschnitt 4, website/assets/schrift/):
Titel Prata (eine Stärke), Lauf und Etiketten Hanken Grotesk 400 und 500. Quelle der TrueType-Dateien: das google/fonts-Repository
(ofl/prata/Prata-Regular.ttf, ofl/hankengrotesk/HankenGrotesk[wght].ttf), dieselben Schriften, aus denen die Website ihre Latin-WOFF2 hat.

    python3 _werkzeuge/carte/fonts_statisch.py <ordner mit Prata-Regular.ttf und HankenGrotesk.ttf>
        → fonts/Prata-400.ttf, fonts/Hanken-400.ttf, fonts/Hanken-500.ttf
"""
import os, shutil, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HIER = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HIER, 'fonts')
SCHNITTE = [('Hanken-400', {'wght': 400}), ('Hanken-500', {'wght': 500})]

if __name__ == '__main__':
    Q = sys.argv[1] if len(sys.argv) > 1 else F
    os.makedirs(F, exist_ok=True)
    if os.path.abspath(os.path.join(Q, 'Prata-Regular.ttf')) != os.path.abspath(os.path.join(F, 'Prata-400.ttf')):
        shutil.copyfile(os.path.join(Q, 'Prata-Regular.ttf'), os.path.join(F, 'Prata-400.ttf'))
    print('Prata-400')
    for name, achsen in SCHNITTE:
        t = TTFont(os.path.join(Q, 'HankenGrotesk.ttf'))
        s = instancer.instantiateVariableFont(t, achsen, updateFontNames=False)
        s.flavor = None
        s.save(os.path.join(F, name + '.ttf'))
        print(name)
