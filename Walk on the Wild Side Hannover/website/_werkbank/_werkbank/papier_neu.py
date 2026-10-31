#!/usr/bin/env python3
"""Walk on the Wild Side: gemeinsame Bausteine für Papier, Untersetzer, Sticker, Postkarten und Beigaben (Werkbank Papier, 31.10.2026).
Farben aus website/assets/wild.css, Texte nur aus der Website (index.html, drinks.html, bau.py › HAUS), Motive aus CHARAKTER.md 3:
die Wortmarke (echtes Logo), das Eckschild (Nacht mit Goldrahmen), die NEGRONI-Glühbirnen, die Decke, die SESSION-Wellen.
Kein Ticket, keine Platzkarte, kein «x»."""
import html as _h
import math
import os
import re
from kern import ROOT

WEB = os.path.dirname(ROOT)
BILD = os.path.join(WEB, 'assets', 'bild')

# Farben der Website (wild.css :root)
NACHT, PLATTE, PLATTE2 = '#130e0d', '#1c1513', '#261e1a'
CREME, CREME2, CREME3 = '#f2e9dc', '#e7dccb', '#d9cbb6'
GOLD, GOLDT = '#d8b264', '#9a7a3c'          # Gold als Haarlinie; dunkles Gold für Schrift auf Creme
ROT = '#f0323f'                             # das Rot der Wortmarke, nur als Punkt
ULTRA, PROT = '#1a00aa', '#d21c0a'          # nur SESSION/DJ-Abende: Ultramarin und Plakatrot
TINTE, LEISE = '#1b1512', '#6e5d4e'

_Z = os.path.relpath(os.path.join(ROOT, 'werkbank', 'eigen'), os.path.join(ROOT, '_werkbank', 'satz'))
TAPETE = f'url({_Z}/tapete-dunkel.svg) 50% 0/16mm auto'   # das Ornament der Website, leise, für dunkle Flächen

# ---------------------------------------------------------------- Hauswerte (website/bau.py › HAUS)
ADRESSE = 'Haasemannstraße 13'
ORT = '30449 Hannover-Linden'
ECKE = 'Ecke Rampenstraße, zwei Minuten vom Küchengarten'
TELEFON = '+49 163 3909578'
IG = '@walkonthewildside_hannover'
ZEITEN = [('Donnerstag', '19 bis 1 Uhr'), ('Freitag', '19 bis 2 Uhr'), ('Samstag', '19 bis 2 Uhr'), ('Sonntag bis Mittwoch', 'geschlossen')]
ZEIT_KURZ = 'Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr'
ZEILE = 'Nachbarschafts-Mixology-Bar'
SATZ = 'Du sagst, was du magst.'
MOMO = '«Du sagst mir, was du magst, ich mache dir einen Drink.»'


def _text(s):
    return _h.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()


_DR = open(os.path.join(WEB, 'drinks.html'), encoding='utf-8').read()


def _abschnitt(name, folge):
    """Satz nach einer Überschrift in drinks.html (Techniken, Klassiker), nur gelesen."""
    t = _text(_DR)
    m = re.search(re.escape(name) + r'\s+(.+?)\s+(?=' + folge + ')', t)
    return m.group(1) if m else ''


TECHNIK = [('Milk Washing', _abschnitt('Technik Milk Washing', 'Technik')),
           ('Fat Washing', _abschnitt('Technik Fat Washing', 'Technik')),
           ('Enzyme', _abschnitt('Technik Enzyme', 'Jeder Drink'))]
KLASSIKER = [('Negroni', _abschnitt('zum Haus. Negroni', 'Paloma')), ('Paloma', _abschnitt('Paloma', 'Mexikaner')),
             ('Mexikaner', _abschnitt('Mexikaner', 'Ohne Alkohol')), ('Ohne Alkohol', _abschnitt('Ohne Alkohol', 'Donnerstag'))]
WAHL = [('Der Geschmack', 'Lieber sauer, süss, bitter oder rauchig?'), ('Das Glas', 'Klar, cremig oder spritzig?'),
        ('Was hinein soll', 'Gin, Rum, Mezcal, Whisky oder ganz ohne Alkohol?')]
for _n, _s in WAHL:
    assert _s in _text(_DR), _s
for _n, _s in TECHNIK + KLASSIKER:
    assert _s, _n


def erster(s, n=1):
    """die ersten n Sätze"""
    teile = re.split(r'(?<=[.!?])\s+', s)
    return ' '.join(teile[:n])


def bild(key):
    """grösste Fassung eines Fotos der Website (assets/bild/<key>-<breite>.webp)"""
    best = max((f for f in os.listdir(BILD) if re.fullmatch(re.escape(key) + r'-\d+\.webp', f)), key=lambda f: int(f.rsplit('-', 1)[1][:-5]))
    return os.path.join(BILD, best)


def bild_satz(key):
    """Adresse eines Fotos aus Sicht der Satzdateien (_werkbank/satz/*.html; assets ist im Projekt ein Verweis auf die Website)"""
    return '../../assets/bild/' + os.path.basename(bild(key))


def welle(ident, b, h, farbe_a, farbe_b, winkel=-32, breite=9.0, hub=2.6, laenge=34.0, clip=None):
    """SESSION-Wellen: schräge, gewellte Bänder in zwei Farben (wie die Plakate der DJ-Abende), als Pfade in mm."""
    d = math.hypot(b, h)
    cx, cy = b / 2, h / 2
    pf = ''
    k = -int(d / breite) - 2
    while k * breite < d + breite:
        y0 = k * breite
        oben, unten = [], []
        x = -d
        while x <= d:
            s = hub * math.sin(2 * math.pi * x / laenge)
            oben.append(f'{x + cx:.2f},{y0 + s + cy:.2f}')
            unten.append(f'{x + cx:.2f},{y0 + breite / 2 + s + cy:.2f}')
            x += 1.5
        pf += 'M' + 'L'.join(oben) + 'L' + 'L'.join(reversed(unten)) + 'Z'
        k += 1
    cp = f' clip-path="url(#{clip})"' if clip else ''
    return (f'<g{cp}><rect x="0" y="0" width="{b}" height="{h}" fill="{farbe_a}"/>'
            f'<path d="{pf}" fill="{farbe_b}" transform="rotate({winkel} {cx} {cy})"/></g>')


def welle_html(b, h, farbe_a, farbe_b, x=0, y=0, **k):
    """Wellen als eigenes SVG an mm-Koordinaten (für Drucksachen in HTML)."""
    return f'<svg class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm" viewBox="0 0 {b} {h}">{welle(None, b, h, farbe_a, farbe_b, **k)}</svg>'


def birnen(x, y, text, groesse, farbe=GOLD, anker='middle', sperr=.12):
    """NEGRONI wie die Glühbirnen-Schrift über der Vitrine: Buchstaben aus Lichtpunkten. Die Punkte sitzen auf den Konturen von Hanken SemiBold
    (fontTools), als Kreise gezeichnet, damit im PDF keine Schrift als «Type 3» landet (gestrichelte Schrift würde Chromium so schreiben)."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.basePen import BasePen
    f = TTFont(os.path.join(ROOT, '_werkbank', 'fonts', 'HankenGrotesk-SemiBold.ttf'))
    gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm
    s = groesse / upm

    class Pen(BasePen):
        def __init__(self):
            super().__init__(gs); self.wege, self.akt = [], []
        def _moveTo(self, p):
            self.akt = [p]; self.wege.append(self.akt)
        def _lineTo(self, p):
            self.akt.append(p)
        def _curveToOne(self, a, b, c):
            p0 = self.akt[-1]
            for i in range(1, 9):
                t_ = i / 8
                self.akt.append(tuple((1 - t_) ** 3 * p0[k] + 3 * (1 - t_) ** 2 * t_ * a[k] + 3 * (1 - t_) * t_ ** 2 * b[k] + t_ ** 3 * c[k] for k in (0, 1)))
        def _qCurveToOne(self, a, b):
            p0 = self.akt[-1]
            for i in range(1, 9):
                t_ = i / 8
                self.akt.append(tuple((1 - t_) ** 2 * p0[k] + 2 * (1 - t_) * t_ * a[k] + t_ ** 2 * b[k] for k in (0, 1)))
        def _closePath(self):
            if self.akt: self.akt.append(self.akt[0])

    namen = [cmap[ord(c)] for c in text]
    breite = sum(gs[n].width for n in namen) * s + sperr * groesse * (len(text) - 1)
    x0 = x - (breite / 2 if anker == 'middle' else 0)
    abstand, r = groesse * .13, groesse * .042
    punkte = ''
    for n in namen:
        pen = Pen(); gs[n].draw(pen)
        for weg in pen.wege:
            rest = 0
            for (ax, ay), (bx, by) in zip(weg, weg[1:]):
                l = math.hypot(bx - ax, by - ay) * s
                d = rest
                while d <= l:
                    q = d / l if l else 0
                    px, py = x0 + (ax + (bx - ax) * q) * s, y - (ay + (by - ay) * q) * s
                    punkte += f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{r:.2f}"/>'
                    d += abstand
                rest = d - l
        x0 += gs[n].width * s + sperr * groesse
    return f'<g fill="{farbe}">{punkte}</g>'


def satz_namen(*namen):
    """Satzdateien: die Familiennamen, die der Kit fest schreibt (DM Mono, Instrument Sans), heissen wie die Schrift, die gesetzt wird."""
    from kern import W
    for n in namen:
        p = os.path.join(W, 'satz', n)
        t = open(p, encoding='utf-8').read()
        u = t.replace('"DM Mono"', '"Hanken Grotesk"').replace("'DM Mono'", "'Hanken Grotesk'").replace("'Instrument Sans'", "'Hanken Grotesk'").replace('"Instrument Sans"', '"Hanken Grotesk"')
        if u != t:
            open(p, 'w', encoding='utf-8').write(u)


def stuecke(*_):
    """Früher zwanzig weitere Culinarium-Stücke; Wild Side zeigt stattdessen die zwanzig Drucksachen der Plakatwerkstatt (papier.py › plakatwerkstatt)."""
    return [], {}
