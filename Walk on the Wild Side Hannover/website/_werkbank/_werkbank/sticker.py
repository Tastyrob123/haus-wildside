#!/usr/bin/env python3
"""Walk on the Wild Side: dreissig Sticker (Werkbank Papier, 31.10.2026; Bauart wie sticker.py des Culinarium).
Gebaut wie die Untersetzer (papier_kern.etikett, Druckbogen A3 mit Schnittlinie in Magenta), in einen eigenen Ordner sticker/.
Formen: rund, eckig, Kapsel und Schild mit Bogen (das Gewölbe). Inhalte nur von der Bar: die Wortmarke (echtes Logo), das Eckschild mit Goldrahmen,
die NEGRONI-Glühbirnen, die Decke, die SESSION-Wellen in Plakatrot, Creme und Ultramarin, Sätze der Website, Zeiten, Adresse, Instagram.
Kein Ticket, kein Siegel, kein «x».
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/sticker.py "<website/_werkbank>"   →  satz/sticker*.html, sticker_plan.json
   danach  node _werkbank/sticker_druck.js "<website/_werkbank>" sticker   und   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/sticker.py "<…>" --seite"""
import json, os, sys
import papier_kern as P
import bogen_mitte  # noqa: F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import etikett, tx, hwz, blatt, t, e
from kern import H, W
import papier_neu as N
from papier_neu import NACHT, CREME, CREME3, GOLD, GOLDT, ROT, ULTRA, PROT, TINTE

WM = 1600 / 1296   # Höhe : Breite der Wortmarke


# ---------------------------------------------------------------- Formen (SVG-Pfade in mm)
def kreis(d):
    r = d / 2
    return f'M{r} 0A{r} {r} 0 1 1 {r - .01} 0Z'


def eck(b, h, r=3):
    return f'M{r} 0H{b - r}A{r} {r} 0 0 1 {b} {r}V{h - r}A{r} {r} 0 0 1 {b - r} {h}H{r}A{r} {r} 0 0 1 0 {h - r}V{r}A{r} {r} 0 0 1 {r} 0Z'


def kapsel(b, h):
    return eck(b, h, h / 2)


def schild(b, h):
    r = b / 2
    return f'M0 {r}A{r} {r} 0 0 1 {b} {r}V{h - 3}A3 3 0 0 1 {b - 3} {h}H3A3 3 0 0 1 0 {h - 3}Z'


# ---------------------------------------------------------------- Bausteine
def grund(form, farbe):
    return f'<path d="{form}" fill="{farbe}"/>'


def ring_kreis(d, farbe, ab=2.4):
    return f'<circle cx="{d / 2}" cy="{d / 2}" r="{d / 2 - ab}" fill="none" stroke="{farbe}" stroke-width=".3"/>'


def ring_eck(b, h, farbe, ab=2.2, r=1.6, d=.3):
    return f'<rect x="{ab}" y="{ab}" width="{b - 2 * ab}" height="{h - 2 * ab}" rx="{r}" fill="none" stroke="{farbe}" stroke-width="{d}"/>'


def pr(x, y, text, gr, farbe):
    """Titelschrift Prata"""
    return tx(x, y, e(text), gr, farbe, 's', 0, 'middle')


def mo(x, y, text, gr, farbe, sp=.16, fett=False):
    """Etikett: Hanken 500 (600) in gesperrten Versalien"""
    return tx(x, y, e(text.upper()), gr, farbe, 'm', sp, 'middle', f'font-weight="{600 if fett else 500}"')


def wm(x, y, b, farbe):
    """die Wortmarke, x = Mitte, y = Oberkante"""
    return hwz(x, y, b, farbe)


def punkt(x, y, r=1.1, farbe=ROT):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{farbe}"/>'


def foto(key, b, h, ident, lage='xMidYMid slice'):
    return (f'<clipPath id="{ident}c"><path d="{eck(b - 5, h - 5, 2)}" transform="translate(2.5 2.5)"/></clipPath>'
            f'<image href="{e(N.bild_satz(key))}" x="2.5" y="2.5" width="{b - 5}" height="{h - 5}" preserveAspectRatio="{lage}" clip-path="url(#{ident}c)"/>')


def wellen(ident, b, h, form, a, c, **k):
    return f'<clipPath id="{ident}w"><path d="{form}"/></clipPath>' + N.welle(None, b, h, a, c, clip=ident + 'w', **k)


# ---------------------------------------------------------------- die dreissig (gemischt: Form, Grösse und Farbe wechseln)
def alle():
    S, n = [], [0]

    def s(b, h, form, innen, name, satz):
        n[0] += 1
        S.append(etikett(f's{n[0]:02d}', b, h, form, innen, name, satz))

    def nid():
        return f's{n[0] + 1:02d}'
    s(46, 46, kreis(46), grund(kreis(46), CREME) + wm(23, 23 - 12 * WM, 24, ROT), 'Die Wortmarke', 'Rund, 46 mm. Das Logo der Bar in Rot auf Creme.')
    s(44, 54, eck(44, 54, 2.4), grund(eck(44, 54, 2.4), '#000') + ring_eck(44, 54, GOLD, 2.6, 1.6, .8) + wm(22, 27 - 15 * WM, 30, CREME),
      'Das Eckschild', 'Eckig, 44 × 54 mm. Das schwarze Kastenschild mit Goldrahmen von der Hausecke.')
    s(100, 22, kapsel(100, 22), grund(kapsel(100, 22), NACHT) + pr(50, 13.4, N.SATZ, 5.4, CREME), N.SATZ, 'Kapsel, 100 mm. Der Satz der Bar.')
    s(56, 56, kreis(56), wellen(nid(), 56, 56, kreis(56), CREME, PROT, breite=8, hub=2.2, laenge=30) + f'<circle cx="28" cy="28" r="14" fill="{CREME}"/>'
      + mo(28, 30, 'Session', 4.6, ULTRA, .04, True), 'SESSION', 'Rund, 56 mm. Die Wellen der DJ-Abende, die Schrift in Ultramarin.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), CREME) + foto('fb-2023-negroni', 60, 60, nid(), 'xMidYMid slice'), 'Foto: NEGRONI', 'Eckig, 60 mm. Die Glühbirnen-Schrift über der Vitrine, mit schmalem Rand.')
    s(90, 26, kapsel(90, 26), grund(kapsel(90, 26), CREME) + mo(45, 12.4, N.ZEILE, 3, TINTE, .1) + mo(45, 18.4, 'Hannover-Linden', 2.2, GOLDT, .16), N.ZEILE, 'Kapsel, 90 mm. So nennt sich die Bar selbst.')
    s(44, 44, kreis(44), grund(kreis(44), NACHT) + ring_kreis(44, GOLD, 2) + N.birnen(22, 25.4, 'NEGRONI', 6.4), 'NEGRONI in Lichtpunkten', 'Rund, 44 mm. Der Schriftzug wie aus Glühbirnen.')
    s(44, 62, schild(44, 62), grund(schild(44, 62), NACHT) + pr(22, 26, 'Bis 2 Uhr.', 6, GOLD)
      + ''.join(mo(22, 37 + k * 6, z, 2.3, CREME, .14) for k, z in enumerate(['Do 19 – 1 Uhr', 'Fr 19 – 2 Uhr', 'Sa 19 – 2 Uhr'])), 'Bis 2 Uhr.', 'Schild mit Bogen wie das Gewölbe, 44 × 62 mm. Die Zeiten der Woche.')
    s(56, 56, kreis(56), grund(kreis(56), CREME) + ring_kreis(56, GOLDT) + pr(28, 28, 'Was', 7.6, TINTE) + pr(28, 36, 'magst du?', 7.6, TINTE) + punkt(28, 44),
      'Was magst du?', 'Rund, 56 mm. Momos Frage an der Theke.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), NACHT) + foto('decke-2017', 60, 60, nid()), 'Foto: das Gewölbe', 'Eckig, 60 mm. Die Decke über der Theke.')
    s(100, 26, kapsel(100, 26), grund(kapsel(100, 26), PROT) + mo(50, 12.2, 'Sip & Sounds', 4.2, CREME, .08, True) + mo(50, 18.6, 'Samstags 21 – 1 Uhr', 2.2, CREME, .18),
      'Sip & Sounds', 'Kapsel, 100 mm. Die Zeile der SESSION-Plakate in Plakatrot.')
    s(40, 40, kreis(40), grund(kreis(40), NACHT) + wm(20, 20 - 10 * WM, 20, ROT), 'Die Wortmarke auf der Nacht', 'Rund, 40 mm.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), NACHT) + foto('schild', 60, 60, nid(), 'xMidYMid slice'), 'Foto: das Eckschild', 'Eckig, 60 mm. Das Schild an der Ecke bei Nacht.')
    s(56, 56, kreis(56), grund(kreis(56), NACHT) + ring_kreis(56, GOLD) + pr(28, 28.5, 'Seit 2018', 6.6, CREME) + mo(28, 36, 'in Linden', 2.4, GOLD, .22),
      'Seit 2018 in Linden', 'Rund, 56 mm. Seit 2018 ist Momo in Linden zu Hause.')
    s(96, 22, kapsel(96, 22), grund(kapsel(96, 22), NACHT) + mo(48, 12.4, N.IG, 2.9, GOLD, .06), N.IG, 'Kapsel, 96 mm. Wo die Bar ihre Abende ankündigt.')
    s(50, 50, kreis(50), grund(kreis(50), CREME) + mo(25, 15.5, 'Cocktailbars', 1.9, GOLDT, .2) + pr(25, 31, '91', 15, TINTE) + mo(25, 38.5, 'Falstaff 2027', 2, GOLDT, .18),
      '91 Punkte', 'Rund, 50 mm. Falstaff Bar Guide 2027.')
    s(44, 62, schild(44, 62), grund(schild(44, 62), CREME) + ring_eck(44, 62, ULTRA, 2.2, 1.6) + pr(22, 34, 'Erst der Drink,', 4.2, ULTRA) + pr(22, 41, 'dann die Musik.', 4.2, ULTRA),
      'Erst der Drink, dann die Musik.', 'Schild mit Bogen, 44 × 62 mm. Der Satz der Programm-Seite.')
    s(70, 40, eck(70, 40, 2.4), wellen(nid(), 70, 40, eck(70, 40, 2.4), CREME, ULTRA, breite=8, hub=2, laenge=28) + f'<rect x="15" y="12" width="40" height="16" rx="1.4" fill="{CREME}"/>'
      + mo(35, 22.6, 'Session', 5, ULTRA, .04, True), 'SESSION in Ultramarin', 'Eckig, 70 × 40 mm. Die Wellen in Ultramarin.')
    for name, _satz in N.TECHNIK:
        s(44, 44, kreis(44), grund(kreis(44), NACHT) + ring_kreis(44, GOLD, 2) + mo(22, 16, 'Momo', 1.9, GOLD, .22) + pr(22, 25.5, name, 5 if len(name) < 10 else 4.4, CREME),
          name, 'Rund, 44 mm. Eine von Momos drei Techniken.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), CREME) + foto('momo-giesst', 60, 60, nid()), 'Foto: Momo gießt ein', 'Eckig, 60 mm. Momo hinter der Theke.')
    s(96, 22, kapsel(96, 22), grund(kapsel(96, 22), CREME) + mo(48, 12.6, 'Mexikaner · Wild-Side-Tradition', 2.9, PROT, .1), 'Mexikaner', 'Kapsel, 96 mm. Der scharfe Shot des Hauses.')
    s(56, 56, kreis(56), wellen(nid(), 56, 56, kreis(56), CREME, PROT, breite=8, hub=2.2, laenge=30) + f'<circle cx="28" cy="28" r="15" fill="{CREME}"/>' + wm(28, 28 - 10 * WM, 20, ROT),
      'Wortmarke in der Welle', 'Rund, 56 mm. Die Wortmarke mitten in den SESSION-Wellen.')
    s(50, 50, eck(50, 50, 2.4), grund(eck(50, 50, 2.4), NACHT) + ring_eck(50, 50, GOLD, 2.6) + pr(25, 23, 'Jeder Drink', 5.4, CREME) + pr(25, 30.5, 'ein Unikat.', 5.4, CREME) + punkt(25, 38),
      'Jeder Drink ein Unikat.', 'Eckig, 50 mm. Aus der Seite «Drinks».')
    s(52, 52, kreis(52), grund(kreis(52), CREME) + ring_kreis(52, GOLDT) + pr(26, 25.5, 'Haasemannstr. 13', 4.6, TINTE) + mo(26, 32, 'Ecke Rampenstraße', 2, GOLDT, .14),
      'Haasemannstraße 13', 'Rund, 52 mm. Die Ecke mit dem Schild.')
    s(100, 22, kapsel(100, 22), grund(kapsel(100, 22), PROT) + mo(50, 12.6, 'Good Drinks · Good Music · Good Energy', 2.7, CREME, .1), 'Good Drinks, Good Music, Good Energy',
      'Kapsel, 100 mm. Wie die Bar ihre Abende auf Instagram beschreibt.')
    s(60, 60, eck(60, 60, 2.4), grund(eck(60, 60, 2.4), NACHT) + foto('decke-raum', 60, 60, nid()), 'Foto: der Raum', 'Eckig, 60 mm. Die Theke unter dem Gewölbe.')
    s(52, 70, schild(52, 70), grund(schild(52, 70), NACHT) + ring_eck(52, 70, GOLD, 2.4, 1.6) + wm(26, 10, 14, ROT) + pr(26, 46, 'Unter dieser', 5.6, CREME) + pr(26, 53.5, 'Decke.', 5.6, CREME),
      'Unter dieser Decke.', 'Schild mit Bogen, 52 × 70 mm. Der Titel der Seite «Das Haus».')
    s(56, 56, kreis(56), grund(kreis(56), ULTRA) + mo(28, 22, 'Samstags', 2.4, CREME, .22) + pr(28, 32, 'Jemand', 6.2, CREME) + pr(28, 39.5, 'legt auf.', 6.2, CREME),
      'Samstags legt jemand auf.', 'Rund, 56 mm. Nur für die DJ-Abende: Ultramarin.')
    return S


def fertig(S):
    """Satzdateien und Druckbögen wie papier_kern.fertig, aber für den Ordner sticker/."""
    alle = ''
    for x in S:
        svg = f'<svg class="abs" style="inset:0;width:{x["b"]}mm;height:{x["h"]}mm" viewBox="0 0 {x["b"]} {x["h"]}">{x["innen"]}</svg>'
        alle += blatt(x['b'], x['h'], svg, 'etikett', 'background:transparent')
    P.seite('sticker', [alle], 'Sticker')
    boegen, akt, x0, y0, zh = [], [], 14, 16, 0
    for x in S:
        if x0 + x['b'] > 420 - 14:
            x0, y0, zh = 14, y0 + zh + 9, 0
        if y0 + x['h'] > 297 - 12:
            boegen.append(akt); akt, x0, y0, zh = [], 14, 16, 0
        akt.append((x, x0, y0)); x0 += x['b'] + 9; zh = max(zh, x['h'])
    boegen.append(akt)
    seiten = []
    for nr, akt in enumerate(boegen):
        inn = ''.join(f'<svg class="abs" style="left:{ox}mm;top:{oy}mm;width:{x["b"]}mm;height:{x["h"]}mm;overflow:visible" viewBox="0 0 {x["b"]} {x["h"]}">'
                      f'{x["innen"].replace("id=\"", "id=\"b" + x["id"]).replace("url(#", "url(#b" + x["id"]).replace("href=\"#", "href=\"#b" + x["id"]).replace("#b" + x["id"] + "hz", "#hz").replace("#b" + x["id"] + "hw", "#hw")}'
                      f'<path d="{x["form"]}" fill="none" stroke="#e6007e" stroke-width=".15"/></svg>' for x, ox, oy in akt)
        inn += t(14, 6.5, f'{e(H.NAME)} · Sticker · Druckbogen {nr + 1} von {len(boegen)} · A3 quer · Originalgröße · Schnittlinie in Magenta', 'm', 'font-size:2.1mm;color:#26242d')
        seiten.append(blatt(420, 297, inn, '', 'background:#fff'))
    P.seite('sticker-bogen', seiten, 'Sticker, Druckbogen')
    plan = {'etiketten': [{k: x[k] for k in ('id', 'b', 'h', 'name', 'satz', 'form')} for x in S], 'boegen': len(boegen),
            'masse': [min(min(x['b'], x['h']) for x in S), max(max(x['b'], x['h']) for x in S)]}
    json.dump(plan, open(os.path.join(W, 'sticker_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Sticker gesetzt:', len(S), 'Stück,', len(boegen), 'Druckbögen')


def seite():
    """sticker/index.html mit der Seite der Untersetzer (papier_seiten.etiketten), umgestellt auf den Ordner sticker/."""
    import papier_seiten as PS
    plan = json.load(open(os.path.join(W, 'sticker_plan.json')))
    PS.plan = dict(PS.plan, etiketten=plan['etiketten'], boegen=plan['boegen'], masse=plan['masse'])
    PS.ROH = os.path.join(W, 'roh', 'sticker')
    PS.ET = dict(ordner='sticker', name='Sticker', einzahl='Sticker')
    PS.S = dict(PS.S, etik_titel=('Sticker', 'für alles, was rausgeht.'),
                etik_text='Für die Tür, das Glas, den Laptop und die Plattenhülle der Gäste: {n} Ideen, rund, eckig und mit Bogen wie das Gewölbe.',
                etik_kap='Die Sticker', etik_kopf=['Dreißig', 'Sticker.'],
                etik_kopftext='Die Wortmarke, das Eckschild, die NEGRONI-Birnen, die Decke, die Wellen der SESSION-Plakate, Momos Frage, die Zeiten und die Ecke.',
                etik_auslage=[(2, 4, 24, -5), (30, 0, 22, 4), (56, 6, 34, -3), (4, 34, 26, 3), (34, 32, 26, -4), (64, 34, 26, 5), (8, 66, 22, 2), (36, 64, 22, -3), (62, 66, 26, 4)]
                + [(0, 0, 0, 0)] * 30, etik_haufen=None)
    PS.etiketten()
    p = os.path.join(os.path.dirname(W), 'sticker', 'index.html')
    t = open(p, encoding='utf-8').read()
    t = t.replace('und Ihre Unterlagen im selben Stil', 'und eure Unterlagen im selben Stil').replace('Originalgrösse', 'Originalgröße').replace(' loading="lazy"', '').replace('Dreissig', 'Dreißig').replace('dreissig', 'dreißig')
    open(p, 'w', encoding='utf-8').write(t)
    from PIL import Image
    im = Image.open(os.path.join(os.path.dirname(W), 'sticker', 'img', 's04.webp')); im.save(os.path.join(os.path.dirname(W), 'sticker', 'img', 'vorschau.webp'), 'WEBP', quality=86)
    print('Seite gebaut: sticker/ ·', len(plan['etiketten']), 'Sticker')


if __name__ == '__main__':
    if '--seite' in sys.argv:
        import kern as K
        K.gestaltung(); seite()
    else:
        fertig(alle())
