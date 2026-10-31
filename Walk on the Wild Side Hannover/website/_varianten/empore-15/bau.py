# Walk on the Wild Side · Feiern-Seite, Abschnitt «Die lange Tafel · Die Empore gehört euch.» (id="tafel"): 15 Darstellungen (30.10.2026).
# Robert: «gib 15 visuelle alternative darstellungen für den abschnitt». 00 = heutiger Stand.
# Je Fassung eine eigene Anordnung und eine eigene Bewegung. Texte Wort für Wort aus unter.tafel() (geprüft unten), nur echte Fotos der Bar.
# Auftritte deckend, nur transform (kein Einblenden), ein Scroll-Takt in e.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/empore-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/empore-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('e.css', 'e.js', 'nav.js'))))

TEXT = 'Oben auf der kleinen Empore steht die lange Tafel. Vier Stunden gehört sie eurer Runde, unten läuft die Bar weiter. Ihr legt vorher ein Budget für die Drinks fest; ist es erreicht, stockt ihr auf, oder eure Gäste bestellen selbst weiter.'
S1 = 'Oben auf der kleinen Empore steht die lange Tafel.'
S2 = 'Vier Stunden gehört sie eurer Runde, unten läuft die Bar weiter.'
S2a, S2b = 'Vier Stunden gehört sie eurer Runde,', 'unten läuft die Bar weiter.'
S3 = 'Ihr legt vorher ein Budget für die Drinks fest; ist es erreicht, stockt ihr auf, oder eure Gäste bestellen selbst weiter.'
ZAHLEN = [('10–20', 'Gäste an der Tafel'), ('4', 'Stunden auf der Empore'), ('0 €', 'für Service und Raum')]
_q = open('unter.py').read()
assert TEXT in _q and TEXT == ' '.join([S1, S2, S3]) and S2 == S2a + ' ' + S2b, 'Text weicht ab'
assert "zahlen = %r" % ZAHLEN in _q, 'Zahlen weichen ab'
assert "kz('Die lange Tafel', 'Mit eigenem Budget', 0), h2(['Die Empore', 'gehört euch.'])" in _q and "knopf('Tafel anfragen', '#anfragen', 'rot')" in _q


def kz():
    return B.kz('Die lange Tafel', 'Mit eigenem Budget', 0)


def h2(cls='t-kap'):
    return B.h2(['Die Empore', 'gehört euch.'], cls)


def p(t=TEXT, cls='text sw', i=1):
    return '<p class="%s" style="--i:%d">%s</p>' % (cls, i, E(t))


def knopf():
    return '<div class="knoepfe sw" style="--i:3">%s</div>' % B.knopf('Tafel anfragen', '#anfragen', 'rot')


def zahl(j, cls='ez', innen=''):
    z, t = ZAHLEN[j]
    return '<div class="%s" style="--n:%d"><b class="titel">%s</b>%s<span class="etikett">%s</span></div>' % (cls, j, E(z), innen, E(t))


def zahlen(cls='ez-reihe', zcls='ez'):
    return '<div class="%s">%s</div>' % (cls, ''.join(zahl(j, zcls) for j in range(3)))


def fo(k, sizes, cls='', pos='50% 50%'):
    return '<figure class="ef %s" style="--lq:url(%s)">%s</figure>' % (cls, mache(k)['lq'], B.img_tag(k, sizes, extra=' style="object-position:%s"' % pos))


def sek(n, inner, innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf em e%02d" id="tafel" data-e="%d">%s</section>' % (n, n, i)


V = []


# 01 · Die helle Karte: das Bild links, Wand an Wand daneben eine cremefarbene Karte wie die weissen Plakate der Bar, mit Goldlinie innen.
# Die Karte wächst von unten an ihren Platz, das Bild steigt von unten mit.
def v01(n):
    return sek(n, '<div class="g">%s<div class="x-karte">%s%s%s%s%s</div></div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 46vw'), kz(), h2(), p(), zahlen(), knopf()))
V.append((1, 'Die helle Karte', v01))


# 02 · Über dem Bild der Titel: Kapitelzeile, Titel und Satz mittig oben, darunter das Bild in der Mitte,
# links zwei Zahlen, rechts die dritte und der Knopf. Das Bild steigt aus der Tiefe und wächst an seinen Platz.
def v02(n):
    return sek(n, '<div class="x-kopf">%s%s%s</div><div class="g"><div class="seite x-links">%s%s</div>%s<div class="seite rechts">%s%s</div></div>' % (
        kz(), h2('t-kap x-gross'), p(), zahl(0), zahl(1), fo('an-empore', '(max-width:900px) 80vw, 34vw', 'mitte'), zahl(2), knopf()))
V.append((2, 'Über dem Bild der Titel', v02))


# 03 · Das Eckschild: der Text steht in einem schwarzen Kasten mit Goldrahmen wie das Schild an der Hausecke, das Bild rechts.
# Erst zieht der Goldrahmen von den Ecken her auf, dann steigt der Text.
def v03(n):
    r = ''.join('<i class="r %s"></i>' % c for c in ('o', 'u', 'l', 're'))
    return sek(n, '<div class="g"><div class="x-schild">%s<div class="x-schild-in">%s%s%s%s%s</div></div>%s</div>' % (
        r, kz(), h2(), p(), zahlen(), knopf(), fo('an-empore', '(max-width:900px) 92vw, 40vw')))
V.append((3, 'Das Eckschild', v03))


# 04 · Die Mittelsäule: links der Text, rechts das Bild, dazwischen die drei Zahlen sehr gross übereinander, getrennt durch Goldlinien.
# Die Zahlen zoomen nacheinander aus der Tiefe nach vorn.
def v04(n):
    return sek(n, '<div class="g"><div class="t">%s%s%s%s</div>%s%s</div>' % (
        kz(), h2(), p(), knopf(), zahlen('saeule'), fo('an-empore', '(max-width:900px) 92vw, 30vw')))
V.append((4, 'Die Mittelsäule', v04))


# 05 · Vier Stunden: neben dem Bild der Text, darunter die 4 gross und ein Balken aus vier Feldern, je Stunde eins.
# Beim Scrollen füllt sich ein Feld nach dem anderen mit Gold.
def v05(n):
    felder = ''.join('<i style="--n:%d"><u></u></i>' % j for j in range(4))
    z4 = '<div class="stunden"><b class="titel">4</b><div><div class="balken" data-stunden>%s</div><span class="etikett">%s</span></div></div>' % (felder, E(ZAHLEN[1][1]))
    return sek(n, '<div class="g">%s<div class="t">%s%s%s%s<div class="ez-reihe x-zwei">%s%s</div>%s</div></div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 44vw'), kz(), h2(), p(), z4, zahl(0), zahl(2), knopf()))
V.append((5, 'Vier Stunden', v05))


# 06 · Oben und unten: zwei Ebenen wie im Haus. Oben die Empore mit der Tafel, eine Goldlinie als Boden,
# unten die Bar mit den Gläsern. Die obere Ebene senkt sich, die untere steigt, die Linie zieht von der Mitte aus.
def v06(n):
    oben = '<div class="ebene x-oben auf"><div class="t">%s%s%s%s</div>%s</div>' % (
        kz(), h2(), p(S1), p(S2a, 'text sw x-gross', 2), fo('an-empore', '(max-width:900px) 92vw, 44vw', pos='50% 48%'))
    boden = '<div class="boden auf"><i></i></div>'
    unten = '<div class="ebene unten auf">%s<div class="t">%s%s%s%s</div></div>' % (
        fo('decke-raum', '(max-width:900px) 92vw, 36vw', pos='50% 60%'), p(S2b, 'text sw x-gross', 1), p(S3, 'text sw', 2), zahlen(), knopf())
    return sek(n, oben + boden + unten)
V.append((6, 'Oben und unten', v06))


# 07 · Das Budget: Text neben dem Bild, der Satz zum Budget gross, links daneben eine schmale Goldsäule,
# die sich beim Scrollen von unten füllt, bis sie voll ist.
def v07(n):
    return sek(n, '<div class="g">%s<div class="t">%s%s%s<div class="budget"><div class="saeule" data-budget><u></u></div>%s</div>%s%s</div></div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 42vw'), kz(), h2(), p(S1 + ' ' + S2), p(S3, 'titel b-satz sw', 2), zahlen(), knopf()))
V.append((7, 'Das Budget', v07))


# 08 · Der Titel quer: die Überschrift in einer Zeile sehr gross über die ganze Breite, darunter drei Spalten:
# Bild, Text mit Knopf, die Zahlen untereinander. Die Spalten steigen nacheinander herauf.
def v08(n):
    return sek(n, '<div class="x-kopf">%s%s</div><div class="g auf"><div class="x-sp" style="--n:0">%s</div><div class="x-sp" style="--n:1">%s%s</div><div class="x-sp" style="--n:2">%s</div></div>' % (
        kz(), h2('t-kap quer'), fo('an-empore', '(max-width:900px) 92vw, 34vw'), p(), knopf(), zahlen('x-liste')))
V.append((8, 'Der Titel quer', v08))


# 09 · Die Bildleiste: unter dem Bild hängt Wand an Wand eine dunkle Leiste mit den drei Zahlen, rechts der Text.
# Das Bild kommt von oben, die Leiste von unten, sie treffen sich an der Kante.
def v09(n):
    return sek(n, '<div class="g"><div class="bl">%s%s</div><div class="t">%s%s%s%s</div></div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 44vw'), zahlen('x-leiste'), kz(), h2(), p(), knopf()))
V.append((9, 'Die Bildleiste', v09))


# 10 · Die lange Linie: oben Text und Bild, darunter eine Goldlinie über die ganze Breite wie die Tafel,
# auf ihr stehen die drei Zahlen. Die Linie zieht von links auf, die Zahlen senken sich auf sie.
def v10(n):
    return sek(n, '<div class="g">%s<div class="t">%s%s%s%s</div></div><div class="linie auf"><i></i>%s</div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 36vw'), kz(), h2(), p(), knopf(), zahlen('auf-linie')))
V.append((10, 'Die lange Linie', v10))


# 11 · Wand an Wand: rechts zwei Bilder ohne Fuge nebeneinander, die Tafel gross, die Gläser schmal; links der Text.
# Die Bilder schweben nacheinander von unten an ihren Platz.
def v11(n):
    return sek(n, '<div class="g"><div class="t">%s%s%s%s%s</div><div class="x-wand">%s%s</div></div>' % (
        kz(), h2(), p(), zahlen(), knopf(), fo('an-empore', '(max-width:900px) 56vw, 30vw', 'w1'), fo('an-glaeser', '(max-width:900px) 36vw, 20vw', 'w2')))
V.append((11, 'Wand an Wand', v11))


# 12 · Drei Schritte: das Bild bleibt stehen, rechts drei Sätze mit je einer Zahl. Beim Scrollen tritt einer nach dem anderen hervor,
# drei Scroll-Bewegungen lang.
def v12(n):
    s = ''.join('<div class="schritt" style="--n:%d">%s<p>%s</p></div>' % (j, zahl(j), E(t)) for j, t in enumerate((S1, S2, S3)))
    return sek(n, '<div class="pin" data-pin><div class="buehne"><div class="innen g">%s<div class="t">%s%s<div class="schritte">%s</div>%s</div></div></div></div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 40vw'), kz(), h2(), s, knopf()), innen=False)
V.append((12, 'Drei Schritte', v12))


# 13 · Mit Leitlinie: die Zahlen als drei Zeilen, links die Bezeichnung, rechts die Zahl, dazwischen eine gepunktete Goldlinie.
# Die Linien laufen von links zur Zahl.
def v13(n):
    z = ''.join('<div class="zeile" style="--n:%d"><span class="etikett">%s</span><i></i><b class="titel">%s</b></div>' % (j, E(t), E(w)) for j, (w, t) in enumerate(ZAHLEN))
    return sek(n, '<div class="g">%s<div class="t">%s%s%s<div class="leit auf">%s</div>%s</div></div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 44vw'), kz(), h2(), p(), z, knopf()))
V.append((13, 'Mit Leitlinie', v13))


# 14 · Die Platte: Bild und Text liegen gemeinsam auf einer dunklen Platte mit Goldlinie, die Zahlen als Fuss der Platte.
# Die Platte steigt als Ganzes, das Bild darin zoomt langsam aus der Nähe zurück.
def v14(n):
    return sek(n, '<div class="x-platte"><div class="g">%s<div class="t">%s%s%s%s</div></div>%s</div>' % (
        fo('an-empore', '(max-width:900px) 92vw, 42vw'), kz(), h2(), p(), knopf(), zahlen('x-fuss')))
V.append((14, 'Die Platte', v14))


# 15 · In die Tiefe: hohes Bild rechts, das Foto wandert beim Scrollen langsam in seinem Rahmen, als blicke man die Empore hinauf.
# Links der Text, die Zahlen untereinander mit Goldlinien.
def v15(n):
    return sek(n, '<div class="g"><div class="t">%s%s%s%s%s</div>%s</div>' % (
        kz(), h2(), p(), zahlen('stapel'), knopf(), '<div class="tief" data-tief>%s</div>' % fo('an-empore', '(max-width:900px) 92vw, 40vw')))
V.append((15, 'In die Tiefe', v15))


def seite(n):
    h = unter.tafel()
    eintrag = dict((nr, (nm, f)) for nr, nm, f in V)
    if n:
        a = h.rfind('<section', 0, h.find('id="tafel"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + eintrag[n][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[nr, nm] for nr, nm, _ in V]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/e.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, V[-1][0], E(eintrag[n][0] if n else 'Heutiger Stand'))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/e.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in [0] + [nr for nr, _, _ in V]:
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', V[-1][0])
