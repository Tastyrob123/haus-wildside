#!/usr/bin/env python3
"""Feste Druckschnitte für Walk on the Wild Side (Werkbank Papier, 31.10.2026): Prata (eine Stärke) und Hanken Grotesk 400/500/600
aus den Webschriften der Website (website/assets/schrift/*.woff2). Variable Schriften schreibt Chromium als «Type 3» in die PDF,
mit festen TrueType-Schnitten bleibt die Schrift scharf.   python3 _werkbank/druckschrift.py → _werkbank/fonts/*.ttf
Der Kit kennt im Satz die Familien «Instrument Sans» und «DM Mono»; papier.py, sticker.py und postkarten.py stellen sie im Satz-CSS
auf diese Hanken-Schnitte um (_werkbank/druckschrift.py › umstellen)."""
import os
import re
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

W = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(os.path.dirname(os.path.dirname(W)), 'assets', 'schrift')
Z = os.path.join(W, 'fonts')
SCHNITTE = [('prata-latin.woff2', 'Prata-Regular', 'Prata Druck', 'Regular', 400),
            ('hanken-latin.woff2', 'HankenGrotesk-Regular', 'Hanken Druck', 'Regular', 400),
            ('hanken-latin.woff2', 'HankenGrotesk-Medium', 'Hanken Druck', 'Medium', 500),
            ('hanken-latin.woff2', 'HankenGrotesk-SemiBold', 'Hanken Druck', 'SemiBold', 600)]
# die Familien, die der Kit im Satz fest schreibt → Hanken-Schnitt (Gewicht → Datei)
HANKEN = {400: 'HankenGrotesk-Regular.ttf', 500: 'HankenGrotesk-Medium.ttf', 600: 'HankenGrotesk-SemiBold.ttf'}


def umstellen(css):
    """Satz-CSS des Kits: Instrument Sans → Hanken 400/500/600, DM Mono → Hanken 500 (Etiketten), Fraunces → Prata."""
    css = re.sub(r"InstrumentSans-Regular\.ttf", HANKEN[400], css)
    css = re.sub(r"InstrumentSans-Medium\.ttf", HANKEN[500], css)
    css = re.sub(r"InstrumentSans-SemiBold\.ttf", HANKEN[600], css)
    css = re.sub(r"DMMono-Regular\.ttf", HANKEN[500], css)
    css = re.sub(r"Fraunces-(Light|Regular)\.ttf", 'Prata-Regular.ttf', css)
    css = re.sub(r"Urbanist-(Medium|SemiBold)\.ttf", HANKEN[500], css)
    return css


def bau():
    os.makedirs(Z, exist_ok=True)
    for quelle, ziel, fam, stil, g in SCHNITTE:
        f = TTFont(os.path.join(Q, quelle))
        if 'fvar' in f:
            f = instancer.instantiateVariableFont(f, {'wght': g}, inplace=False)
        for rec in f['name'].names:
            if rec.nameID in (1, 16): rec.string = fam
            if rec.nameID in (2, 17): rec.string = stil
            if rec.nameID == 4: rec.string = f'{fam} {stil}'
            if rec.nameID == 6: rec.string = f'{fam.replace(" ", "")}-{stil}'
        f['OS/2'].usWeightClass = g
        f.flavor = None
        f.save(os.path.join(Z, ziel + '.ttf'))
        print(ziel + '.ttf', 'variabel' if 'fvar' in f else 'fest')


if __name__ == '__main__':
    bau()
