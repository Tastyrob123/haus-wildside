#!/usr/bin/env python3
"""Walk on the Wild Side: zwölf Untersetzer, neu (Werkbank Papier, 1.11.2026; Robert: «sehen kacke aus – Motive doof oder nicht richtig mittig»).
Ein System wie die Untersetzer des Culinarium: rund 94 mm, Goldlinie 3 mm innen, jedes Motiv als Gruppe genau in der Mitte des Kreises
(Höhe der Gruppe aus Versalhöhe und Grundlinie der Schriften berechnet, nicht geschätzt), kein schiefer Text, Zeile rundherum gleichmässig verteilt.
Weniger, stärkere Motive: die Wortmarke gross (Rot auf Creme, Creme auf Nacht), Fotos der Bar randlos im Kreis (NEGRONI über der Vitrine,
das Eckschild, das Gewölbe, Momo), die SESSION-Wellen mit Ultramarin-Schrift, «Du sagst, was du magst.» in Prata, Falstaff 91, die Zeiten.
Aufruf aus papier.py (untersetzer_alle)."""
import math
import os
from fontTools.ttLib import TTFont
from papier_kern import etikett, hwz, e
from kern import W
import papier_neu as N
from papier_neu import NACHT, CREME, CREME3, GOLD, GOLDT, ROT, ULTRA, PROT, TINTE

D = 94
R = D / 2
WM = 1600 / 1296       # Höhe : Breite der Wortmarke
_F = os.path.join(W, 'fonts')


def _cap(datei):
    f = TTFont(os.path.join(_F, datei))
    return f['OS/2'].sCapHeight / f['head'].unitsPerEm


CAP = {'s': _cap('Prata-Regular.ttf'), 'm': _cap('HankenGrotesk-Medium.ttf')}
FAM = {'s': 'Prata', 'm': 'Hanken Grotesk'}


def kreis(r=R):
    return f'M{R} {R - r}A{r} {r} 0 1 1 {R - .01} {R - r}Z'


def zeile(y_grund, text, gr, farbe, art='s', sperr=0, x=R, anker='middle', gewicht=None):
    w = f' font-weight="{gewicht}"' if gewicht else (' font-weight="500"' if art == 'm' else '')
    return (f'<text x="{x:.2f}" y="{y_grund:.2f}" text-anchor="{anker}" font-family="{FAM[art]}" font-size="{gr}" letter-spacing="{sperr}em" fill="{farbe}"{w}>'
            f'{e(text.upper() if art == "m" else text)}</text>')


def gruppe(teile, mitte=R):
    """teile: Liste von ('text', text, gr, farbe, art, sperr, abstand_danach) oder ('form', hoehe, zeichnen(y_oben), abstand_danach).
    Die ganze Gruppe (Versalhöhe bis Grundlinie, Formen ganz) steht senkrecht genau in der Mitte."""
    hoehe = sum((t[2] * CAP[t[4]] if t[0] == 'text' else t[1]) + t[-1] for t in teile) - teile[-1][-1]
    y = mitte - hoehe / 2
    aus = ''
    for t in teile:
        if t[0] == 'text':
            _, text, gr, farbe, art, sperr, ab = t
            h = gr * CAP[art]
            aus += zeile(y + h, text, gr, farbe, art, sperr)
            y += h + ab
        else:
            _, h, zeichnen, ab = t
            aus += zeichnen(y)
            y += h + ab
    return aus


def strich(b, farbe, d=.35):
    return lambda y: f'<rect x="{R - b / 2:.2f}" y="{y:.2f}" width="{b}" height="{d}" fill="{farbe}"/>'


def punkt(r, farbe=ROT):
    return lambda y: f'<circle cx="{R}" cy="{y + r:.2f}" r="{r}" fill="{farbe}"/>'


def wortmarke(b, farbe):
    return lambda y: hwz(R, y, b, farbe)


def ring_text(ident, text, farbe, r=37.2, gr=2.3, sperr=.16):
    """Zeile rundherum, mit textLength genau auf den Umfang verteilt (kein Anfang, keine Lücke); Grundlinie auf dem Kreis r."""
    umfang = 2 * math.pi * r
    stueck = text.upper() + ' · '
    n = max(1, round(umfang / (len(stueck) * gr * (0.62 + sperr))))
    return (f'<path id="{ident}r" d="M{R - r} {R}A{r} {r} 0 1 1 {R + r} {R}A{r} {r} 0 1 1 {R - r} {R}" fill="none"/>'
            f'<text font-family="Hanken Grotesk" font-weight="500" font-size="{gr}" letter-spacing="{sperr}em" fill="{farbe}">'
            f'<textPath href="#{ident}r" textLength="{umfang - gr * sperr:.2f}" lengthAdjust="spacing">{e(stueck * n)}</textPath></text>')


def foto(ident, key, fx, fy, breite, hoehe_zu_breite):
    """Foto randlos im Kreis; der Punkt (fx, fy) des Bildes liegt genau in der Mitte."""
    h = breite * hoehe_zu_breite
    x, y = R - fx * breite, R - fy * h
    assert x <= 0 and y <= 0 and x + breite >= D and y + h >= D, (key, x, y)
    return (f'<clipPath id="{ident}c"><path d="{kreis()}"/></clipPath>'
            f'<image href="{e(N.bild_satz(key))}" x="{x:.2f}" y="{y:.2f}" width="{breite}" height="{h:.2f}" preserveAspectRatio="none" clip-path="url(#{ident}c)"/>')


def us(ident, grund, innen, name, satz, linie=GOLD, ring=None):
    z = f'<path d="{kreis()}" fill="{grund}"/>' + innen
    if ring:
        z += ring_text(ident, ring[0], ring[1])
    z += f'<circle cx="{R}" cy="{R}" r="{R - 3}" fill="none" stroke="{linie}" stroke-width=".35"/>'
    return etikett(ident, D, D, kreis(), z, name, satz)


def wellen(ident, a, b):
    return f'<clipPath id="{ident}w"><path d="{kreis()}"/></clipPath>' + N.welle(None, D, D, a, b, clip=ident + 'w', breite=10, hub=3, laenge=38)


ZEILE = 'Walk on the Wild Side · Haasemannstraße 13 · Linden'


def alle():
    U = []
    T = lambda *a: ('text',) + a
    # 1 und 2: die Wortmarke gross
    U.append(us('u01', CREME, gruppe([('form', 40 * WM, wortmarke(40, ROT), 0)]), 'Die Wortmarke in Rot',
                'Das Logo der Bar gross in Rot auf dem Creme der weissen Plakate.', GOLDT))
    U.append(us('u02', NACHT, gruppe([('form', 40 * WM, wortmarke(40, CREME), 0)]), 'Die Wortmarke auf der Nacht',
                'Das Logo in Creme auf der Nacht der Bar, mit Goldlinie wie das Eckschild.'))
    # 3: NEGRONI, das Foto
    U.append(us('u03', NACHT, foto("u03", "fb-2023-negroni", .55, .378, 158, 1200 / 960), 'NEGRONI',
                'Die Glühbirnen-Schrift über der Vitrine, als Foto mitten im Kreis.'))
    # 4: SESSION
    U.append(us('u04', CREME, wellen('u04', CREME, PROT) + f'<circle cx="{R}" cy="{R}" r="22" fill="{CREME}"/>'
                + gruppe([T('Session', 8.4, ULTRA, 'm', .04, 3.6), T('Samstags 21 – 1 Uhr', 2.4, ULTRA, 'm', .16, 0)]).replace('font-weight="500">SESSION', 'font-weight="600">SESSION'),
                'SESSION', 'Die Wellen der Plakate der DJ-Abende in Plakatrot und Creme, die Schrift in Ultramarin.', PROT))
    # 5: Du sagst, was du magst.
    U.append(us('u05', CREME, gruppe([T('Du sagst,', 8.2, TINTE, 's', 0, 3.4), T('was du magst.', 8.2, TINTE, 's', 0, 5), ('form', 2.4, punkt(1.2), 0)]),
                'Du sagst, was du magst.', 'Der Satz der Bar in Prata, darunter der rote Punkt.', GOLDT, (ZEILE, GOLDT)))
    # 6: das Eckschild, Foto
    U.append(us('u06', NACHT, foto('u06', 'schild', .405, .29, 131, 1280 / 960), 'Das Eckschild',
                'Das beleuchtete Schild an der Hausecke bei Nacht, genau in der Mitte.'))
    # 7: Falstaff 91
    U.append(us('u07', NACHT, gruppe([T('Falstaff Bar Guide', 2.5, GOLD, 'm', .2, 5), T('91', 24, CREME, 's', 0, 5), T('Punkte · 2027', 2.5, GOLD, 'm', .2, 0)]),
                '91 Punkte', '91 Punkte im Falstaff Bar Guide 2027, Kategorie Cocktailbars.', GOLD, (ZEILE, GOLD)))
    # 8: SESSION in Ultramarin, Wortmarke in der Mitte
    U.append(us('u08', CREME, wellen('u08', CREME, ULTRA) + f'<circle cx="{R}" cy="{R}" r="22" fill="{CREME}"/>' + gruppe([('form', 24 * WM, wortmarke(24, ROT), 0)]),
                'Wortmarke in der Welle', 'Die Wortmarke mitten in den Wellen, in Ultramarin wie die Schrift der SESSION-Plakate.', ULTRA))
    # 9: die Zeiten, Tage links, Zeiten rechts
    def zeiten(y):
        aus, b = '', 50
        for i, (tag, zeit) in enumerate([('Donnerstag', '19 – 1 Uhr'), ('Freitag', '19 – 2 Uhr'), ('Samstag', '19 – 2 Uhr')]):
            gl = y + i * 8.4 + 3.6 * CAP['s']
            aus += zeile(gl, tag, 2.3, GOLD, 'm', .16, R - b / 2, 'start') + zeile(gl, zeit, 3.6, CREME, 's', 0, R + b / 2, 'end')
            if i < 2:
                aus += f'<rect x="{R - b / 2}" y="{gl + 3:.2f}" width="{b}" height=".2" fill="rgba(216,178,100,.35)"/>'
        return aus
    U.append(us('u09', NACHT, gruppe([T('Bis 2 Uhr.', 7, CREME, 's', 0, 7), ('form', 2 * 8.4 + 3.6 * CAP['s'], zeiten, 0)]),
                'Die Zeiten', 'Donnerstag bis Samstag ab 19 Uhr: die Tage links, die Zeiten rechts.'))
    # 10: das Gewölbe, Foto
    U.append(us('u10', NACHT, foto('u10', 'decke-2017', .5, .5, 150, 690 / 960), 'Das Gewölbe',
                'Die Decke über der Theke, von unten gesehen.'))
    # 11: die Ecke
    U.append(us('u11', CREME, gruppe([T('Haasemannstraße 13', 5.6, TINTE, 's', 0, 4.6), ('form', .35, strich(14, GOLDT), 4.6), T('Ecke Rampenstraße · Linden', 2.3, GOLDT, 'm', .16, 0)]),
                'Die Ecke', 'Haasemannstraße 13, Ecke Rampenstraße: die Ecke mit dem Schild.', GOLDT, ('Nachbarschafts-Mixology-Bar', GOLDT)))
    # 12: Momo, Foto
    U.append(us('u12', NACHT, foto('u12', 'momo-giesst', .55, .5, 120, 1280 / 960), 'Momo gießt ein',
                'Momo hinter der Theke beim Eingießen.'))
    return U
