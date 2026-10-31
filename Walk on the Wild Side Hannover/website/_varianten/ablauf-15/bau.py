# Walk on the Wild Side · Feiern-Seite (tafel.html), Abschnitt «So geht es · Anfragen, Angebot, Abend.» (id="ablauf"): 15 Darstellungen (30.10.2026).
# Robert: «gib mir 15 visuelle alternative Darstellungsformen von dem Abschnitt». 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte Wort für Wort aus unter.py (wird geprüft), nur Bilder des Hauses.
# Bewegung nur über transform und opacity, ein Scroll-Takt in a.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/ablauf-15/bau.py → 00 … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/ablauf-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('a.css', 'a.js', 'nav.js'))))

# Schritt, Satz (Wort für Wort aus unter.py), Bild, Ausschnitt
SCHRITTE = [
    ('Anfragen', 'Ihr schreibt, was ihr vorhabt: Anlass, Datum, wie viele ihr seid.', 'fw-a55', '50% 55%'),
    ('Angebot', 'Derya und Momo melden sich mit einem Vorschlag, nur für euch.', 'an-team', '50% 35%'),
    ('Anzahlung', 'Bei jedem Abend 30 Prozent eine Woche vorher, der Rest am Abend vor Beginn.', 'fw-tafel', '50% 50%'),
    ('Abend', 'Ihr kommt um 19 Uhr, alles ist bereit, Momo hat die Gläser kalt gestellt.', 'tafel-glaeser', '50% 45%'),
]
_q = open('unter.py').read()
for t, s, k, p in SCHRITTE:
    assert "('%s', '%s')" % (t, s) in _q, 'Text weicht von der Seite ab: ' + t

KZ = B.kz('So geht es', 'Vier Schritte', 0)


def titel(cls='t-kap'):
    return B.h2(['Anfragen, Angebot,', 'Abend.'], cls)


def kopf(cls=''):
    return '<div class="ab-kopf %s">%s%s</div>' % (cls, KZ, titel())


def fig(k, sizes, cls='', stil='', pos=None):
    d = mache(k)
    p = pos or dict((x[2], x[3]) for x in SCHRITTE).get(k, '50% 50%')
    return '<figure class="ab-b %s" style="--lq:url(%s);%s">%s</figure>' % (cls, d['lq'], stil, B.img_tag(k, sizes, extra=' style="object-position:%s"' % p))


def text(t, s, cls='ab-x'):
    return '<div class="%s"><h3 class="titel ab-t">%s</h3><p class="ab-s">%s</p></div>' % (cls, E(t), E(s))


def sek(v, inner, cls='hell', innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf ax %s" id="ablauf" data-v="%d">%s</section>' % (cls, v, i)


V = []


# 01 · Aufgedeckt: vier hohe Bilder Wand an Wand, unter jedem sein Schritt. Jedes Bild deckt sich von unten auf, eins nach dem anderen.
def v01(v):
    sp = ''.join('<div class="a1-sp va" style="--n:%d">%s%s</div>' % (n, fig(k, '(max-width:760px) 92vw, 26vw', 'a1-b'), text(t, s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '%s<div class="a1-reihe">%s</div>' % (kopf(), sp))
V.append(('Aufgedeckt', v01))


# 02 · Das Bild bleibt stehen: links ziehen die Schritte vorbei, rechts steht das Bild und wechselt; das neue schiebt sich von unten herein.
def v02(v):
    st = ''.join(fig(k, '(max-width:760px) 92vw, 40vw', 'a2-f' + (' an' if n == 0 else '')) for n, (t, s, k, p) in enumerate(SCHRITTE))
    bl = ''.join('<div class="a2-bl%s" data-j="%d"><span class="ab-et">%s</span>%s</div>' % (' an' if n == 0 else '', n, ('Erst', 'Dann', 'Dann', 'Zum Schluss')[n], text(t, s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '<div class="a2-g"><div class="a2-l">%s%s</div><div class="a2-r"><div class="a2-halt"><div class="a2-st">%s</div></div></div></div>' % (kopf(), bl, st))
V.append(('Das Bild bleibt stehen', v02))


# 03 · Die Goldlinie: vier Bilder in einer Reihe, darunter eine Linie über die ganze Breite, die sich beim Scrollen zieht; jede Station leuchtet auf, wenn die Linie sie erreicht.
def v03(v):
    st = ''.join('<div class="a3-st" data-j="%d">%s<i class="a3-p"></i>%s</div>' % (n, fig(k, '(max-width:760px) 92vw, 26vw', 'a3-b'), text(t, s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '%s<div class="a3-weg"><div class="a3-linie"><i></i></div>%s</div>' % (kopf('mitte'), st))
V.append(('Die Goldlinie', v03))


# 04 · Die lange Tafel: ein grosses Querbild über die ganze Breite öffnet sich, darunter vier Spalten, über jeder zieht sich ihre Goldlinie.
def v04(v):
    sp = ''.join('<div class="a4-sp" style="--n:%d"><i class="a4-l"></i>%s</div>' % (n, text(t, s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '%s<div class="a4-bild va">%s</div><div class="a4-spalten va">%s</div>' % (kopf('mitte'), fig('fw-tafel', '(max-width:760px) 100vw, 1240px', 'a4-b', pos='50% 55%'), sp))
V.append(('Die lange Tafel', v04))


# 05 · Die Liste zum Zeigen: die vier Schritte als grosse Wörter; wer darüber fährt oder tippt, sieht rechts das Bild und den Satz dazu, das Bild wischt herein.
def v05(v):
    w = ''.join('<button type="button" class="a5-w%s" data-j="%d"><i></i><span class="titel">%s</span></button>' % (' an' if n == 0 else '', n, E(t)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    st = ''.join(fig(k, '(max-width:760px) 92vw, 36vw', 'a5-f' + (' an' if n == 0 else '')) for n, (t, s, k, p) in enumerate(SCHRITTE))
    sa = ''.join('<p class="a5-s%s" data-j="%d">%s</p>' % (' an' if n == 0 else '', n, E(s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '<div class="a5-g"><div class="a5-l">%s<div class="a5-woerter va">%s</div></div><div class="a5-r va"><div class="a5-st">%s</div><div class="a5-saetze">%s</div></div></div>' % (kopf(), w, st, sa))
V.append(('Die Liste zum Zeigen', v05))


# 06 · Schachbrett: Bild und Schritt im Wechsel, acht Felder Wand an Wand; die Felder klappen nacheinander auf wie Karten auf dem Tisch.
def v06(v):
    oben, unten = [], []
    for n, (t, s, k, p) in enumerate(SCHRITTE):
        b = '<div class="a6-f a6-bf va" style="--n:%d">%s</div>' % (n * 2 if n % 2 == 0 else n * 2 + 1, fig(k, '(max-width:760px) 46vw, 26vw', 'a6-b'))
        x = '<div class="a6-f a6-xf va" style="--n:%d">%s</div>' % (n * 2 + 1 if n % 2 == 0 else n * 2, text(t, s))
        (oben if n % 2 == 0 else unten).append(b)
        (unten if n % 2 == 0 else oben).append(x)
    felder = ''.join(o + u for o, u in zip(oben, unten))
    return sek(v, '%s<div class="a6-brett">%s</div>' % (kopf(), felder))
V.append(('Schachbrett', v06))


# 07 · Gegenlauf: in der Mitte die Schritte, links und rechts je zwei Bilder, die beim Scrollen verschieden schnell gegeneinander laufen.
def v07(v):
    li = fig('fw-a55', '(max-width:760px) 46vw, 24vw', 'a7-b') + fig('fw-tafel', '(max-width:760px) 46vw, 24vw', 'a7-b')
    re_ = fig('an-team', '(max-width:760px) 46vw, 24vw', 'a7-b') + fig('tafel-glaeser', '(max-width:760px) 46vw, 24vw', 'a7-b')
    mitte = ''.join(text(t, s, 'ab-x a7-x va') for t, s, k, p in SCHRITTE)
    return sek(v, '<div class="a7-g"><div class="a7-sp" data-t="-1">%s</div><div class="a7-m">%s<div class="a7-liste">%s</div></div><div class="a7-sp" data-t="1">%s</div></div>' % (li, kopf('mitte'), mitte, re_))
V.append(('Gegenlauf', v07))


# 08 · Ein Satz mit Bildern: die vier Schritte als eine grosse Zeile, zwischen den Wörtern wachsen kleine Bilder auf; darunter die Sätze in vier Spalten.
def v08(v):
    teile = []
    for n, (t, s, k, p) in enumerate(SCHRITTE):
        d = mache(k)
        teile.append('<span class="a8-nb" style="--n:%d"><span class="a8-w">%s</span><span class="a8-bild" style="--lq:url(%s)">%s</span>%s</span>' % (
            n, E(t), d['lq'], B.img_tag(k, '220px', extra=' style="object-position:%s"' % p), '.' if n == 3 else ','))
    sp = ''.join('<div class="a8-sp" style="--n:%d"><span class="ab-et">%s</span><p class="ab-s">%s</p></div>' % (n, E(t), E(s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '<div class="ab-kopf">%s</div><p class="titel a8-satz va">%s</p><div class="a8-spalten va">%s</div>' % (KZ, ' '.join(teile), sp))
V.append(('Ein Satz mit Bildern', v08))


# 09 · Die Treppe: vier dunkle Platten mit Bild stehen erst versetzt wie Stufen und legen sich beim Scrollen in eine gerade Reihe.
def v09(v):
    pl = ''.join('<div class="a9-pl" data-j="%d">%s%s</div>' % (n, fig(k, '(max-width:760px) 92vw, 26vw', 'a9-b'), text(t, s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '%s<div class="a9-reihe">%s</div>' % (kopf(), pl))
V.append(('Die Treppe', v09))


# 10 · Abzüge: links die Schritte, rechts vier Abzüge mit hellem Rand, schief hingelegt; sie richten sich nacheinander gerade.
def v10(v):
    ab = ''.join('<figure class="a10-ab va" style="--n:%d;--r:%s">%s<figcaption class="ab-et">%s</figcaption></figure>' % (
        n, ('-5deg', '4deg', '3deg', '-4deg')[n], fig(k, '(max-width:760px) 44vw, 22vw', 'a10-b'), E(t)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    li = ''.join(text(t, s, 'ab-x a10-x') for t, s, k, p in SCHRITTE)
    return sek(v, '<div class="a10-g"><div class="a10-l">%s<div class="a10-liste">%s</div></div><div class="a10-tisch">%s</div></div>' % (kopf(), li, ab))
V.append(('Abzüge', v10))


# 11 · Das Band zum Blättern, dunkel: vier grosse Karten in einer Reihe bis über den Rand; sie fliegen von rechts herein, wischen oder mit den Pfeilen.
def v11(v):
    pf = '<div class="a11-pf"><button type="button" data-d="-1" aria-label="zurück">%s</button><button type="button" data-d="1" aria-label="weiter">%s</button></div>' % (B.PFEIL, B.PFEIL)
    ka = ''.join('<div class="a11-k" style="--n:%d">%s%s</div>' % (n, fig(k, '(max-width:760px) 78vw, 30vw', 'a11-b'), text(t, s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '<div class="innen a11-kopf">%s%s</div><div class="a11-band va">%s</div>' % (kopf(), pf, ka), cls='', innen=False)
V.append(('Das Band, dunkel', v11))


# 12 · Nach der Uhr: ein grosses Bild läuft von selbst durch die vier Schritte, darunter die Striche als Uhr; rechts steht der Schritt gross.
def v12(v):
    st = ''.join(fig(k, '(max-width:760px) 92vw, 44vw', 'a12-f' + (' an' if n == 0 else '')) for n, (t, s, k, p) in enumerate(SCHRITTE))
    sr = ''.join('<button type="button" data-j="%d"><i><b></b></i><span class="ab-et">%s</span></button>' % (n, E(t)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    gr = ''.join('<div class="a12-x%s" data-j="%d"><h3 class="titel">%s</h3><p class="ab-s">%s</p></div>' % (' an' if n == 0 else '', n, E(t), E(s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '<div class="a12-g"><div class="a12-l va"><div class="a12-st">%s</div><div class="a12-striche">%s</div></div><div class="a12-r">%s<div class="a12-gross">%s</div></div></div>' % (st, sr, kopf(), gr))
V.append(('Nach der Uhr', v12))


# 13 · Ein Bild, vier Teile: die gedeckte Tafel in vier Streifen geschnitten; die Streifen kommen verschieden hoch an und setzen sich beim Scrollen zu einem Bild zusammen, unter jedem sein Schritt.
def v13(v):
    d = mache('fw-tafel')
    sp = ''.join('<div class="a13-sp" data-j="%d"><figure class="a13-b" style="--lq:url(%s);--j:%d">%s</figure>%s</div>' % (
        n, d['lq'], n, B.img_tag('fw-tafel', '(max-width:760px) 100vw, 1240px'), text(t, s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '%s<div class="a13-reihe">%s</div>' % (kopf('mitte'), sp))
V.append(('Ein Bild, vier Teile', v13))


# 14 · Die Einladung: rechts eine Karte wie ein Einladungsbrief, mittig gesetzt, ihr Goldrahmen zeichnet sich; die Schritte schreiben sich Zeile für Zeile hinein. Links das Bild.
def v14(v):
    z = ''.join('<div class="a14-z" style="--n:%d"><h3 class="titel">%s</h3><p class="ab-s">%s</p></div>' % (n, E(t), E(s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    rahmen = '<svg class="a14-rahmen" aria-hidden="true"><rect x="12" y="12" rx="6" pathLength="100"/></svg>'
    return sek(v, '<div class="a14-g">%s<div class="a14-karte va">%s<div class="a14-in">%s%s<div class="a14-zeilen">%s</div></div></div></div>' % (
        fig('fw-a55', '(max-width:760px) 92vw, 44vw', 'a14-b va'), rahmen, KZ, titel(), z))
V.append(('Die Einladung', v14))


# 15 · Gestapelt: jeder Schritt eine grosse dunkle Platte mit Bild; die Platten bleiben oben stehen und legen sich beim Scrollen übereinander, die untere tritt zurück.
def v15(v):
    pl = ''.join('<div class="a15-pl" data-j="%d" style="--n:%d"><div class="a15-in">%s<div class="a15-x"><span class="ab-et">%s</span><h3 class="titel">%s</h3><p class="ab-s">%s</p></div></div></div>' % (
        n, n, fig(k, '(max-width:760px) 92vw, 46vw', 'a15-b'), ('Erst', 'Dann', 'Dann', 'Zum Schluss')[n], E(t), E(s)) for n, (t, s, k, p) in enumerate(SCHRITTE))
    return sek(v, '%s<div class="a15-stapel">%s</div>' % (kopf(), pl))
V.append(('Gestapelt', v15))


def seite(n):
    h = unter.tafel()
    if n:
        a = h.rfind('<section', 0, h.find('id="ablauf"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/a.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>So geht es · %s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/a.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('fertig', len(V))
