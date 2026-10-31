# Walk on the Wild Side · Feiern-Seite (tafel.html), zwei Abschnitte mit je 15 Darstellungen (30.10.2026).
# Robert: «gib mir 15 visuelle Darstellungsmöglichkeiten für den Abschnitt» (Strahl «Wie viele seid ihr?», id="wieviele")
# und «das gleich mit machen» (Privates Dinner, id="dinner"). 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte Wort für Wort aus unter.py, nur Bilder des Hauses.
# Bewegung nur über transform und opacity, ein Scroll-Takt in s.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/feiern-15/bau.py → wieviele/00 … 15.html, dinner/00 … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/feiern-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('s.css', 's.js', 'nav.js'))))

# ---------- Texte (Wort für Wort aus unter.py, wird geprüft)
W_TEXT = 'Für jede Runde gibt es den passenden Rahmen. Wählt euer Format, die Seite führt euch hin.'
D_TEXT = 'Ein exklusiver Abend für zehn bis vierzehn Gäste an der langen Tafel, mit Rudi in der Küche und Momo an der Bar. Für Geburtstage, kleine Weihnachtsfeiern, Junggesellenabschiede oder einen Abend mit den Menschen, die zählen.'
GAENGE = [('Zum Anfang', 'Ein Gruss aus der Küche'), ('Drei Gänge', 'Ein vegetarisches Menü von Rudi'), ('Im Glas', 'Fünf Drinks von Momo, auf die Gänge abgestimmt')]
# Formate: Anker, Name, Gäste, Zeile (die Unterzeile des Abschnitts auf der Seite), Bild, von, bis
FORMATE = [('#dinner', 'Privates Dinner', '10 bis 14 Gäste', 'Mit Rudi und Momo', 'an-dinner', 10, 14, '10–14'),
           ('#tafel', 'Die lange Tafel', '10 bis 20 Gäste', 'Mit eigenem Budget', 'an-empore', 10, 20, '10–20'),
           ('#bar', 'Die ganze Bar', 'ab 30 Gästen', 'Geschlossene Gesellschaft', 'an-party', 30, 40, '30+')]
_q = open('unter.py').read()
for t in [W_TEXT, D_TEXT] + [b for a, b in GAENGE] + [f[1] for f in FORMATE] + [f[2] for f in FORMATE] + [f[3] for f in FORMATE]:
    assert t in _q, 'Text weicht von der Seite ab: ' + t


def img(k, sizes, cls='', stil=''):
    """Bild auf seiner Unschärfe-Vorschau, ohne .foto, damit die Auftritte der Seite nicht mitspielen."""
    return '<figure class="fb %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, B.img_tag(k, sizes))


def wkopf(cls=''):
    return '<div class="w-kopf %s">%s%s<p class="text sw" style="--i:1">%s</p></div>' % (
        cls, B.kz('Wie viele seid ihr?', 'Drei Formate', 0), B.h2(['Vom Dinner', 'bis zur ganzen Bar.']), E(W_TEXT))


def dkopf(cls='', text=True, knopf=False):
    t = '<p class="text sw" style="--i:1">%s</p>' % E(D_TEXT) if text else ''
    k = '<div class="knoepfe sw" style="--i:3">%s</div>' % B.knopf('Dinner anfragen', '#anfragen', 'rot') if knopf else ''
    return '<div class="d-kopf %s">%s%s%s%s</div>' % (cls, B.kz('Privates Dinner', 'Mit Rudi und Momo', 0), B.h2(['Zehn bis vierzehn', 'Gäste, ein Menü.']), t, k)


def gaenge(cls='d-gaenge'):
    return '<div class="%s">%s</div>' % (cls, ''.join('<div style="--n:%d"><span class="etikett">%s</span><p>%s</p></div>' % (n, E(a), E(b)) for n, (a, b) in enumerate(GAENGE)))


def dtext():
    return E(D_TEXT)


def dknopf(cls='rot'):
    return B.knopf('Dinner anfragen', '#anfragen', cls)


def sek(id_, v, inner, cls='', innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf vx %s %s" id="%s" data-v="%s">%s</section>' % (v, cls, id_, v, i)


W, D = [], []

# =====================================================================================================
# WIE VIELE SEID IHR?
# =====================================================================================================


# 01 · Die Zahl als Fenster: drei Zeilen über die ganze Breite, die Gästezahl riesig, in ihr das Bild des Formats.
# Das Bild in der Zahl zieht beim Scrollen langsamer als die Seite; die Zeilen steigen aus dem Schlitz.
def w01(v):
    z = ''
    for n, (h, t, g, u, k, a, b, zahl) in enumerate(FORMATE):
        d = mache(k)
        src = 'assets/bild/%s?v=%s' % (d['stufen'][-1][1], B.V)
        z += '''<a class="w1-z vauf" href="%s" style="--n:%d"><svg class="w1-svg" viewBox="0 0 1000 300" aria-hidden="true"><defs><clipPath id="w1c%d"><text x="0" y="250">%s</text></clipPath></defs>
<g clip-path="url(#w1c%d)"><rect width="1000" height="300" fill="#261E1A"/><image class="w1-bild" href="%s" x="0" y="-200" width="1000" height="700" preserveAspectRatio="xMidYMid slice"/></g><text class="w1-kontur" x="0" y="250">%s</text></svg>
<div class="w1-t"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></div></a>''' % (h, n, n, zahl, n, src, zahl, E(t), E(g), E(u))
    return sek('wieviele', v, wkopf() + '<div class="w1-liste">%s</div>' % z)
W.append(('Die Zahl als Fenster', w01))


# 02 · Die Bögen: drei Durchgänge mit rundem Bogen wie das Gewölbe der Bar, in jedem das Bild des Formats.
# Sie steigen aus verschiedenen Tiefen, das Bild darin zoomt zurück.
def w02(v):
    b = ''.join('<a class="w2-b" href="%s" style="--n:%d">%s<span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></a>' % (
        h, n, img(k, '(max-width:760px) 92vw, 30vw', 'w2-bild'), E(t), E(g), E(u)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf('mitte') + '<div class="w2-reihe vauf">%s</div>' % b)
W.append(('Die Bögen', w02))


# 03 · Die Gästeliste: reine Schrift, drei Zeilen zwischen Goldlinien, die Zahl gross links, der Name rechts.
# Die Linien ziehen sich von links auf, Zahl und Name kommen aus dem Schlitz.
def w03(v):
    z = ''.join('<a class="w3-z" href="%s" style="--n:%d"><i class="w3-l"></i><span class="w3-zahl titel"><span>%s</span></span><span class="w3-name"><span class="etikett">%s</span><b class="titel">%s</b></span><span class="w3-g">%s</span><span class="w3-pf">%s</span></a>' % (
        h, n, E(zz), E(u), E(t), E(g), B.PFEIL) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf() + '<div class="w3-liste vauf">%s<i class="w3-l w3-end"></i></div>' % z)
W.append(('Die Gästeliste', w03))


# 04 · Der Zähler: die Bühne steht drei Scrollbewegungen lang. Links zählt die Zahl von 10 bis 30 und mehr,
# rechts wechselt das Bild, sobald ein neues Format beginnt.
def w04(v):
    bi = ''.join(img(k, '(max-width:760px) 92vw, 46vw', 'w4-bild' + (' an' if n == 0 else '')) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    tx = ''.join('<a class="w4-f%s" href="%s"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></a>' % (
        ' an' if n == 0 else '', h, E(u), E(t), E(g)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, '<div class="innen">%s</div><div class="w4-pin" data-pin><div class="w4-buehne"><div class="innen w4-raster"><div class="w4-links"><p class="etikett">Gäste</p><p class="w4-zahl titel"><span>10</span></p><div class="w4-fs">%s</div><div class="w4-skala"><i></i></div></div><div class="w4-bilder">%s</div></div></div></div>' % (
        wkopf(), tx, bi), innen=False)
W.append(('Der Zähler', w04))


# 05 · Die Tischkarten: drei gefaltete Karten in Creme stehen auf dem dunklen Tisch, je Format eine.
# Sie liegen erst flach und klappen nacheinander hoch.
def w05(v):
    k = ''.join('<a class="w5-k" href="%s" style="--n:%d"><div class="w5-v"><span class="etikett">%s</span><b class="titel">%s</b><i></i><p class="w5-g titel">%s</p><span class="weiter">Zum Format %s</span></div></a>' % (
        h, n, E(u), E(t), E(g), B.PFEIL) for n, (h, t, g, u, kk, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf('mitte') + '<div class="w5-tisch vauf">%s</div>' % k)
W.append(('Die Tischkarten', w05))


# 06 · Das Lineal: eine senkrechte Goldlinie mit den Gästezahlen, daneben die Formate als breite Bildbänder,
# je höher die Zahl, desto höher das Band. Die Linie wächst beim Scrollen mit.
def w06(v):
    r = ''.join('<a class="w6-r" href="%s" style="--h:%s;--n:%d"><span class="w6-m titel">%s</span>%s<div class="w6-t"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></div></a>' % (
        h, bb - 4, n, E(zz), img(k, '(max-width:760px) 92vw, 50vw', 'w6-bild'), E(u), E(t), E(g)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf() + '<div class="w6-lineal" data-lineal><i class="w6-linie"><b></b></i>%s</div>' % r)
W.append(('Das Lineal', w06))


# 07 · Die Plätze: eine lange Tafel von oben, zwanzig Plätze an der Tafel, dreissig im Raum dahinter.
# Die Punkte setzen sich nacheinander; zeigt man auf ein Format, leuchten genau seine Plätze.
def w07(v):
    sitz = ''
    for i in range(20):
        x = 6 + (i % 10) * 9.8
        y = 22 if i < 10 else 58
        sitz += '<i class="w7-s t%s" style="left:%.1f%%;top:%s%%;--n:%d"></i>' % (' d' if (i % 10) < 7 else '', x + 1.5, y, i)
    raum = ''.join('<i class="w7-s r" style="left:%.1f%%;top:%s%%;--n:%d"></i>' % (4 + (i % 15) * 6.6, 84 + (i // 15) * 8, 20 + i) for i in range(30))
    f = ''.join('<a class="w7-f%s" href="%s" data-f="%s"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></a>' % (
        ' an' if n == 0 else '', h, ('dinner', 'tafel', 'bar')[n], E(u), E(t), E(g)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, '<div class="w7-raster">%s<div class="w7-fs">%s</div></div><div class="w7-plan vauf" data-f="dinner"><div class="w7-tisch"></div>%s%s<p class="w7-leg etikett"><span>Die lange Tafel</span><span>Der Raum</span></p></div>' % (
        wkopf(), f, sitz, raum))
W.append(('Die Plätze', w07))


# 08 · Die Bildbalken: drei Zeilen, in jeder ein Bildstreifen, so lang wie die Runde gross ist.
# Eine dunkle Platte gleitet vom Streifen und gibt das Bild frei.
def w08(v):
    r = ''.join('<a class="w8-r" href="%s" style="--w:%s;--n:%d"><div class="w8-streifen">%s<i class="w8-platte"></i></div><div class="w8-t"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></div></a>' % (
        h, (.42, .62, 1)[n], n, img(k, '(max-width:760px) 92vw, 70vw', 'w8-bild', 'object-position:50% 50%'), E(u), E(t), E(g)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf() + '<div class="w8-liste vauf">%s</div>' % r)
W.append(('Die Bildbalken', w08))


# 09 · Die Rahmen: «für jede Runde den passenden Rahmen», wörtlich. Drei Goldrahmen an der Wand,
# klein, mittel, gross, unten auf einer Linie. Sie werden eingehängt und pendeln kurz aus.
def w09(v):
    r = ''.join('<a class="w9-r" href="%s" style="--s:%s;--n:%d;--w:%sdeg"><i class="w9-nagel"></i><div class="w9-rahmen">%s</div><div class="w9-t"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></div></a>' % (
        h, (.62, .8, 1)[n], n, (-2, 1.6, -1.2)[n], img(k, '(max-width:760px) 80vw, 30vw', 'w9-bild'), E(u), E(t), E(g)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf('mitte') + '<div class="w9-wand vauf">%s</div>' % r)
W.append(('Die Rahmen', w09))


# 10 · Die Karte: wie die Preisliste der Bar, in Creme, mit Goldrahmen. Drei Zeilen,
# vom Namen zieht sich eine Punktlinie zur Gästezahl; daneben das Bild der Empore hoch.
def w10(v):
    z = ''.join('<a class="w10-z" href="%s" style="--n:%d"><span class="w10-n"><span class="etikett">%s</span><b class="titel">%s</b></span><i class="w10-p"></i><b class="w10-g titel">%s</b></a>' % (
        h, n, E(u), E(t), E(g)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, '<div class="w10-raster"><div class="w10-karte hell vauf"><svg class="fr-rahmen" aria-hidden="true"><rect x="8" y="8" rx="6" ry="6" pathLength="100"/></svg>%s<div class="w10-zeilen">%s</div></div>%s</div>' % (
        wkopf(), z, img('an-empore', '(max-width:900px) 92vw, 36vw', 'w10-bild vauf')))
W.append(('Die Karte', w10))


# 11 · Die Ringe: drei Goldringe um eine Mitte, jeder so gross wie seine Runde. In der Mitte das Bild des Formats,
# auf das man zeigt. Die Ringe wachsen nacheinander aus der Mitte.
def w11(v):
    ringe = ''.join('<a class="w11-ring r%d%s" href="%s" data-n="%d" style="--n:%d"><span class="w11-mk etikett">%s</span></a>' % (
        n, ' an' if n == 0 else '', h, n, n, E(zz)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    mitte = ''.join(img(k, '(max-width:760px) 40vw, 16vw', 'w11-bild' + (' an' if n == 0 else '')) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    f = ''.join('<a class="w11-f%s" href="%s" data-n="%d"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></a>' % (
        ' an' if n == 0 else '', h, n, E(u), E(t), E(g)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, '<div class="w11-raster"><div>%s<div class="w11-fs">%s</div></div><div class="w11-feld vauf">%s<div class="w11-mitte">%s</div></div></div>' % (wkopf(), f, ringe, mitte))
W.append(('Die Ringe', w11))


# 12 · Die Glühbirnen: wie der NEGRONI-Schriftzug über der Vitrine. Die drei Zahlen aus Birnen,
# die nacheinander angehen; darunter Name und Gäste.
ZIFF = {'1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'], '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
        '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'], '0': ['01110', '10001', '10011', '10101', '11001', '10001', '01110'],
        '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'], '+': ['00000', '00100', '00100', '11111', '00100', '00100', '00000']}


def birnen(s, n0):
    out, j = '', 0
    for c in s:
        z = ZIFF[c]
        out += '<span class="w12-ziff">' + ''.join('<i class="%s" style="--j:%d"></i>' % ('b' if z[r][c2] == '1' else '', (j := j + 1) + n0 * 40 if z[r][c2] == '1' else 0) for r in range(7) for c2 in range(5)) + '</span>'
    return out


def w12(v):
    zs = ['14', '20', '30+']
    k = ''.join('<a class="w12-k" href="%s" style="--n:%d"><div class="w12-schild">%s</div><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></a>' % (
        h, n, birnen(zs[n], n), E(u), E(t), E(g)) for n, (h, t, g, u, k_, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf('mitte') + '<div class="w12-reihe vauf">%s</div>' % k)
W.append(('Die Glühbirnen', w12))


# 13 · Das Band: drei Tafeln nebeneinander, je eine Bildschirmbreite gross, die Bühne steht,
# und das Band zieht beim Scrollen nach links: ein Format nach dem anderen.
def w13(v):
    t = ''.join('<a class="w13-t" href="%s">%s<div class="w13-text"><p class="w13-zahl titel">%s</p><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small><span class="weiter">Zum Format %s</span></div></a>' % (
        h, img(k, '(max-width:760px) 92vw, 44vw', 'w13-bild'), E(zz), E(u), E(t_), E(g), B.PFEIL) for n, (h, t_, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, '<div class="innen">%s</div><div class="w13-pin" data-pin><div class="w13-buehne"><div class="w13-band">%s</div><div class="innen w13-punkte"><i class="an"></i><i></i><i></i></div></div></div>' % (wkopf(), t), innen=False)
W.append(('Das Band', w13))


# 14 · Der Tisch wächst: eine lange Tafel von oben über die ganze Breite. Beim Scrollen wird sie länger,
# Platz um Platz; die Marke eines Formats leuchtet, sobald die Tafel es erreicht hat.
def w14(v):
    st = ''.join('<i class="w14-s" style="left:%.2f%%;--a:%.3f"></i><i class="w14-s u" style="left:%.2f%%;--a:%.3f"></i>' % (
        2 + i * 6.4, (i + 1) / 16, 2 + i * 6.4, (i + 1) / 16) for i in range(15))
    mk = ''.join('<a class="w14-mk" href="%s" style="--x:%s;--a:%s"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></a>' % (
        h, x, x, E(t), E(g), E(u)) for (h, t, g, u, k, a, bb, zz), x in zip(FORMATE, (.47, .67, .99)))
    return sek('wieviele', v, wkopf() + '<div class="w14-feld" data-tisch><div class="w14-marken">%s</div><div class="w14-tafel"><i class="w14-platte"></i>%s</div></div>' % (mk, st))
W.append(('Der Tisch wächst', w14))


# 15 · Die Wand: drei Bilder Wand an Wand, jedes so breit wie seine Runde (14 · 20 · 30).
# Sie senken sich nacheinander von oben in die Reihe; darunter steht jedes Format auf seiner Bildkante.
def w15(v):
    b = ''.join('<a class="w15-b" href="%s" style="--g:%s;--n:%d">%s<span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></a>' % (
        h, (14, 20, 30)[n], n, img(k, '(max-width:760px) 92vw, 40vw', 'w15-bild'), E(t), E(g), E(u)) for n, (h, t, g, u, k, a, bb, zz) in enumerate(FORMATE))
    return sek('wieviele', v, wkopf() + '<div class="w15-wand vauf">%s</div>' % b)
W.append(('Die Wand', w15))


# =====================================================================================================
# PRIVATES DINNER
# =====================================================================================================

# 01 · Die Menükarte über die ganze Breite: Creme, Goldrahmen, oben Titel und Satz, darunter die drei Gänge
# als Spalten, über jedem Gang sein Bild. Die Karte entfaltet sich von oben, die Spalten steigen nacheinander.
def d01(v):
    sp = ''.join('<div class="d1-sp" style="--n:%d">%s<span class="etikett">%s</span><p class="titel">%s</p></div>' % (
        n, img(k, '(max-width:760px) 92vw, 26vw', 'd1-bild'), E(a), E(b)) for n, ((a, b), k) in enumerate(zip(GAENGE, ('tf-l3', 'tf-h2', 'tafel-drink'))))
    return sek('dinner', v, '<div class="d1-karte hell vauf"><svg class="fr-rahmen" aria-hidden="true"><rect x="8" y="8" rx="6" ry="6" pathLength="100"/></svg><div class="d1-oben">%s<div><p class="text">%s</p><div class="knoepfe">%s</div></div></div><div class="d1-spalten">%s</div></div>' % (
        dkopf(text=False), dtext(), dknopf(), sp))
D.append(('Die Menükarte, breit', d01))


# 02 · Die Tafel von oben: das Bild der gedeckten Tafel randlos über die linke Hälfte, bis an den Rand.
# Rechts Titel, Satz und Gänge. Das Bild zieht beim Scrollen langsamer als die Seite.
def d02(v):
    return sek('dinner', v, '<div class="d2-raster"><div class="d2-bild" data-par>%s</div><div class="d2-text">%s%s<div class="knoepfe sw" style="--i:4">%s</div></div></div>' % (
        img('tf-oben', '(max-width:900px) 100vw, 50vw', 'd2-fb'), dkopf(), gaenge(), dknopf()), cls='d2', innen=False)
D.append(('Die Tafel von oben', d02))


# 03 · Die Speisenfolge als Weg: eine Goldlinie läuft mittig nach unten und wächst mit; an ihr die drei Gänge,
# abwechselnd links und rechts, je mit eigenem Bild.
def d03(v):
    st = ''.join('<div class="d3-st %s vauf" style="--n:%d">%s<div class="d3-t"><span class="etikett">%s</span><p class="titel">%s</p></div><i class="d3-mk"></i></div>' % (
        'rechts' if n % 2 else 'links', n, img(k, '(max-width:760px) 80vw, 34vw', 'd3-bild'), E(a), E(b)) for n, ((a, b), k) in enumerate(zip(GAENGE, ('tf-l5', 'tf-h1', 'tafel-glaeser'))))
    return sek('dinner', v, dkopf('mitte') + '<div class="d3-weg" data-dweg><i class="d3-linie"></i>%s</div><div class="knoepfe mitte-k">%s</div>' % (st, dknopf()))
D.append(('Die Speisenfolge als Weg', d03))


# 04 · Rudi und Momo: die beiden gross und quer über die ganze Breite, darunter zwei Spalten:
# links Titel und Satz, rechts die Gänge. Eine dunkle Platte senkt sich vom Bild und gibt es frei.
def d04(v):
    return sek('dinner', v, '<div class="d4-bild vauf">%s<i class="d4-platte"></i></div><div class="d4-unten">%s<div>%s<div class="knoepfe sw" style="--i:4">%s</div></div></div>' % (
        img('pf-momo-rudi', '(max-width:900px) 92vw, 1240px', 'd4-fb', 'object-position:50% 40%'), dkopf(), gaenge(), dknopf()))
D.append(('Rudi und Momo', d04))


# 05 · Drei Teller: die Gänge als drei runde Teller auf dem dunklen Tisch, von oben gesehen,
# je mit dem Gang darunter. Sie werden nacheinander hingestellt und drehen sich dabei ein wenig ein.
def d05(v):
    t = ''.join('<div class="d5-t" style="--n:%d;--w:%sdeg">%s<span class="etikett">%s</span><p class="titel">%s</p></div>' % (
        n, (-14, 10, -8)[n], img(k, '(max-width:760px) 70vw, 26vw', 'd5-bild'), E(a), E(b)) for n, ((a, b), k) in enumerate(zip(GAENGE, ('tf-l3', 'tf-l8', 'tafel-drink'))))
    return sek('dinner', v, '<div class="d5-kopf">%s<div><p class="text sw" style="--i:1">%s</p><div class="knoepfe sw" style="--i:2">%s</div></div></div><div class="d5-tisch vauf">%s</div>' % (
        dkopf(text=False), dtext(), dknopf(), t))
D.append(('Drei Teller', d05))


# 06 · Das gedruckte Menü: helle Fläche, die Karte gesetzt wie die echte Menükarte auf der Tafel, alles mittig,
# links und rechts je ein hohes Bild. Die Bilder steigen aus verschiedenen Tiefen, die Zeilen der Karte nacheinander.
def d06(v):
    z = ''.join('<div class="d6-g" style="--n:%d"><span class="etikett">%s</span><p class="titel">%s</p>%s</div>' % (
        n, E(a), E(b), '<i class="d6-orn"></i>' if n < 2 else '') for n, (a, b) in enumerate(GAENGE))
    return sek('dinner', v, '<div class="d6-raster">%s<div class="d6-karte vauf">%s<p class="text">%s</p><i class="d6-strich"></i>%s<div class="knoepfe">%s</div></div>%s</div>' % (
        img('an-dinner', '(max-width:900px) 46vw, 24vw', 'd6-bild l vauf'), dkopf('mitte', text=False), dtext(), z, dknopf(), img('tafel-teller', '(max-width:900px) 46vw, 24vw', 'd6-bild r vauf')), cls='hell')
D.append(('Das gedruckte Menü', d06))


# 07 · Die Bildwand: acht Bilder vom Dinner Wand an Wand in vier Spalten, mittendrin der Text als dunkle Fläche
# über zwei mal zwei Felder. Die Bilder steigen aus verschiedenen Tiefen.
def d07(v):
    ks = ['an-dinner', 'tf-h2', 'tf-oben', 'tf-l8', 'pf-momo-rudi', 'tf-dessert', 'tafel-glaeser', 'tf-l3']
    pos = ['1/1/3/2', '1/2/2/3', '1/3/2/4', '1/4/3/5', '3/1/4/2', '3/2/4/3', '3/3/4/4', '3/4/4/5']
    f = ''.join(img(k, '(max-width:760px) 46vw, 24vw', 'd7-f', 'grid-area:%s;--n:%d' % (p, n)) for n, (k, p) in enumerate(zip(ks, pos)))
    return sek('dinner', v, '<div class="d7-wand vauf">%s<div class="d7-text">%s%s<div class="knoepfe">%s</div></div></div>' % (
        f, B.kz('Privates Dinner', 'Mit Rudi und Momo', 0), B.h2(['Zehn bis vierzehn', 'Gäste, ein Menü.']), dknopf()) +
        '<div class="d7-unten"><p class="text">%s</p>%s</div>' % (dtext(), gaenge()))
D.append(('Die Bildwand', d07))


# 08 · Der Abend läuft: links steht ein grosses Bild, rechts laufen die drei Gänge durch.
# Sobald ein Gang in die Mitte kommt, wechselt links das Bild zu ihm.
def d08(v):
    ks = ['tf-l3', 'tf-h1', 'tafel-glaeser']
    bi = ''.join(img(k, '(max-width:900px) 92vw, 46vw', 'd8-bild' + (' an' if n == 0 else '')) for n, k in enumerate(ks))
    st = ''.join('<div class="d8-g%s" data-gang="%d"><span class="d8-nr titel">%s</span><span class="etikett">%s</span><p class="titel">%s</p></div>' % (
        ' an' if n == 0 else '', n, ('I', 'II', 'III')[n], E(a), E(b)) for n, (a, b) in enumerate(GAENGE))
    return sek('dinner', v, '<div class="d8-raster"><div class="d8-links"><div class="d8-bilder">%s</div></div><div class="d8-rechts">%s<div class="d8-gaenge">%s</div><div class="knoepfe">%s</div></div></div>' % (
        bi, dkopf(), st, dknopf()))
D.append(('Der Abend läuft', d08))


# 09 · Die Klappkarte: eine Menükarte in Creme, deren Deckel aufklappt. Innen links das Bild der Tafel,
# rechts der Satz und die Gänge. Der Deckel dreht sich um seine linke Kante.
def d09(v):
    return sek('dinner', v, '<div class="d9-kopf">%s</div><div class="d9-karte vauf"><div class="d9-innen hell"><div class="d9-l">%s</div><div class="d9-r"><p class="text">%s</p>%s<div class="knoepfe">%s</div></div></div><div class="d9-deckel"><div class="d9-vorn hell"><span class="etikett">Wild Side</span><b class="titel">Privates Dinner</b><i></i><span class="etikett">Mit Rudi und Momo</span></div><div class="d9-hinten">%s</div></div></div>' % (
        B.h2(['Zehn bis vierzehn', 'Gäste, ein Menü.']), img('an-dinner', '(max-width:900px) 92vw, 30vw', 'd9-bild'), dtext(), gaenge(), dknopf(), img('tf-oben', '(max-width:900px) 92vw, 30vw', 'd9-bild')))
D.append(('Die Klappkarte', d09))


# 10 · Das Band der Teller: oben Titel und Satz in zwei Spalten, darunter alle Teller des Abends in einer Reihe,
# die beim Scrollen langsam nach links zieht. Die Gänge stehen darüber auf einer Linie.
def d10(v):
    ks = ['tf-h2', 'tf-l3', 'tf-l5', 'tf-l8', 'tf-h1', 'tf-dessert', 'tafel-drink', 'tafel-glaeser']
    b = ''.join(img(k, '(max-width:760px) 60vw, 22vw', 'd10-f') for k in ks)
    return sek('dinner', v, '<div class="innen d10-oben">%s<div><p class="text sw" style="--i:1">%s</p>%s<div class="knoepfe sw" style="--i:3">%s</div></div></div><div class="d10-fahrt" data-band><div class="d10-band">%s</div></div>' % (
        dkopf(text=False), dtext(), gaenge(), dknopf(), b), innen=False)
D.append(('Das Band der Teller', d10))


# 11 · Die drei Karten: jeder Gang eine eigene hohe Karte mit Bild oben und Gang darunter,
# sie drehen sich nacheinander von der Kante her auf. Darüber Titel und Satz.
def d11(v):
    k = ''.join('<div class="d11-k" style="--n:%d">%s<div class="d11-t"><span class="etikett">%s</span><p class="titel">%s</p></div></div>' % (
        n, img(kk, '(max-width:760px) 92vw, 30vw', 'd11-bild'), E(a), E(b)) for n, ((a, b), kk) in enumerate(zip(GAENGE, ('tf-l8', 'tf-h1', 'momo-giesst'))))
    return sek('dinner', v, '<div class="d11-kopf">%s<div><p class="text sw" style="--i:1">%s</p><div class="knoepfe sw" style="--i:2">%s</div></div></div><div class="d11-reihe vauf">%s</div>' % (
        dkopf(text=False), dtext(), dknopf(), k))
D.append(('Die drei Karten', d11))


# 12 · Text steht, Bilder laufen: links stehen Titel, Satz und Gänge fest, rechts laufen vier grosse Bilder
# des Abends untereinander durch. Jedes steigt beim Hereinkommen ein Stück auf.
def d12(v):
    ks = [('an-dinner', 'Die gedeckte Tafel'), ('tf-l8', 'Ein Gang von Rudi'), ('tafel-glaeser', 'Momo an der Bar'), ('pf-momo-rudi', 'Rudi und Momo')]
    b = ''.join('<div class="d12-b vauf">%s</div>' % img(k, '(max-width:900px) 92vw, 50vw', 'd12-bild') for k, t in ks)
    return sek('dinner', v, '<div class="d12-raster"><div class="d12-links"><div class="d12-fest">%s%s<div class="knoepfe sw" style="--i:4">%s</div></div></div><div class="d12-rechts">%s</div></div>' % (
        dkopf(), gaenge(), dknopf(), b))
D.append(('Text steht, Bilder laufen', d12))


# 13 · Die Tafel quer: die gedeckte Tafel von oben, um eine Vierteldrehung gelegt, läuft als langer Streifen
# über die ganze Breite. Über dem Streifen die Gänge in der Reihenfolge des Abends. Der Streifen zieht beim Scrollen mit.
def d13(v):
    return sek('dinner', v, '<div class="innen d13-oben">%s<div><p class="text sw" style="--i:1">%s</p><div class="knoepfe sw" style="--i:2">%s</div></div></div><div class="innen">%s</div><div class="d13-streifen" data-quer><div class="d13-dreh">%s</div></div>' % (
        dkopf(text=False), dtext(), dknopf(), gaenge('d-gaenge d13-g'), img('tf-oben', '100vw', 'd13-bild')), innen=False)
D.append(('Die Tafel quer', d13))


# 14 · Küche und Bar: zwei Spalten, links Rudi in der Küche mit Gruss und Menü, rechts Momo an der Bar mit den Drinks.
# Darüber Titel und Satz, die Spalten steigen aus verschiedenen Tiefen.
def d14(v):
    k = '<div class="d14-sp" style="--n:0">%s<span class="d14-wer titel">Rudi</span><span class="etikett">In der Küche</span>%s</div>' % (
        img('tf-h2', '(max-width:760px) 92vw, 44vw', 'd14-bild'), ''.join('<div class="d14-z"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (E(a), E(b)) for a, b in GAENGE[:2]))
    m = '<div class="d14-sp" style="--n:1">%s<span class="d14-wer titel">Momo</span><span class="etikett">An der Bar</span>%s</div>' % (
        img('momo-giesst', '(max-width:760px) 92vw, 44vw', 'd14-bild'), ''.join('<div class="d14-z"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (E(a), E(b)) for a, b in GAENGE[2:]))
    return sek('dinner', v, '<div class="d14-kopf">%s<div><p class="text sw" style="--i:1">%s</p><div class="knoepfe sw" style="--i:2">%s</div></div></div><div class="d14-raster vauf">%s%s</div>' % (
        dkopf(text=False), dtext(), dknopf(), k, m))
D.append(('Küche und Bar', d14))


# 15 · Der grosse Satz: der Titel über die ganze Breite, sehr gross. Darunter drei Bilder Wand an Wand, je ein Gang,
# die sich von der Mitte her öffnen; rechts daneben Satz und Knopf.
def d15(v):
    b = ''.join('<div class="d15-b" style="--n:%d"><div class="d15-ab">%s<i class="d15-o"></i><i class="d15-u"></i></div><span class="etikett">%s</span><p class="titel">%s</p></div>' % (
        n, img(k, '(max-width:760px) 92vw, 22vw', 'd15-bild'), E(a), E(b)) for n, ((a, b), k) in enumerate(zip(GAENGE, ('tf-l5', 'tf-h1', 'tafel-drink'))))
    return sek('dinner', v, '<div class="d15-kopf">%s%s</div><div class="d15-raster"><div class="d15-reihe vauf">%s</div><div class="d15-text"><p class="text sw" style="--i:1">%s</p><div class="knoepfe sw" style="--i:2">%s</div></div></div>' % (
        B.kz('Privates Dinner', 'Mit Rudi und Momo', 0), B.h2(['Zehn bis vierzehn Gäste,', 'ein Menü.'], 'd15-h'), b, dtext(), dknopf()))
D.append(('Der grosse Satz', d15))


# ---------- Seiten
def seite(teil, n):
    liste_v = W if teil == 'wieviele' else D
    sid = 'wieviele' if teil == 'wieviele' else 'dinner'
    h = unter.tafel()
    if n:
        a = h.rfind('<section', 0, h.find('id="%s"' % sid))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + liste_v[n - 1][1]('%s%02d' % (teil[0], n)) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(liste_v)]
    o = '%s/%s' % (ORD, teil)
    h = h.replace('<head>', '<head><base href="../../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/s.css?v=%s"></head>' % (ORD, VER), 1)
    titel = 'Wie viele seid ihr' if teil == 'wieviele' else 'Privates Dinner'
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s · %s</span><i>← →</i></p>' % (n, len(liste_v), titel, E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;window.VSEK=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/s.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(o), json.dumps(sid), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for teil, liste_v in (('wieviele', W), ('dinner', D)):
        for n in range(len(liste_v) + 1):
            open(os.path.join(ORD, teil, '%02d.html' % n), 'w').write(seite(teil, n))
    print('fertig', len(W), len(D))
