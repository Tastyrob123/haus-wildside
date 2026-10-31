# Walk on the Wild Side · Das Haus, Abschnitt «Was andere sagen · 91, 4,8 und 4,8.» (id="stimmen"): 15 Darstellungen (31.10.2026).
# Robert: «gib mir 15 alternative visualisierungen für den abschnitt». 00 = heutiger Stand (drei Platten).
# Texte Wort für Wort aus unter.haus(). Keine Fotos dazu: der Abschnitt lebt von Schrift (Regel «leere Fläche: Schrift»).
# Auftritte nur über transform (Opazität nur beim Einschalten der Leuchtschrift), ein Scroll-Takt in x.js.
# Aufruf: python3 _varianten/stimmen-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter

E = html.escape
ORD = '_varianten/stimmen-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('x.css', 'x.js', 'nav.js'))))

ST = [('91', 'Falstaff Bar Guide 2027', 'Cocktailbars: 47 von 50 für die Drinks, 18 von 20 für Stil und Service.'),
      ('4,8', 'Google, 75 Bewertungen', 'Gelobt werden die Beratung ohne Karte, Momo mit Namen und die kleine, gemütliche Bar.'),
      ('4,8', 'NeoTaste, 40 Bewertungen', 'Dieselbe Note von Gästen, die über die App gekommen sind.')]
PRESSE = 'In der Presse: Die Neue Presse schrieb 2021 über Momo und 2024 über Derya an der Theke; Falstaff beschreibt die Bar als Loft, «stylish, relaxed», in der Gäste sagen, was sie mögen.'
_q = open('unter.py').read()
for z, q, s in ST:
    assert q in _q and s in _q, 'Text weicht ab: ' + q
assert PRESSE in _q, 'Pressetext weicht ab'


def kz():
    return B.kz('Was andere sagen', 'Drei Zahlen', 0)


def h2():
    return B.h2(['Gelobt von Gästen und Falstaff.'])


def presse(i=2, cls=''):
    return '<p class="text sw xp %s" style="--i:%d">%s</p>' % (cls, i, E(PRESSE))


def kopf():
    return kz() + h2()


def sek(n, inner, innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf xq x%02d" id="stimmen" data-x="%d">%s</section>' % (n, n, i)


V = []


# 01 · Die Zeile: drei Zahlen ohne Kästen, riesig nebeneinander, getrennt von goldenen Haarlinien.
# Jede Zahl steigt aus ihrer Zeile wie aus einem Schlitz, danach Quelle und Satz.
def v01(n):
    s = ''.join('<div class="z1-s" style="--n:%d"><div class="z1-m"><span class="z1-z titel">%s</span></div><span class="etikett">%s</span><p>%s</p></div>' % (j, z, E(q), E(t)) for j, (z, q, t) in enumerate(ST))
    return sek(n, kopf() + '<div class="z1 vauf">%s</div>' % s + presse())
V.append(('Die Zeile', v01))


# 02 · Die grosse 91: links die Falstaff-Zahl über die halbe Seite, rechts die beiden 4,8 übereinander, kleiner.
# Die 91 wächst von unten links auf ihre Grösse, die beiden Noten steigen danach.
def v02(n):
    z, q, t = ST[0]
    r = ''.join('<div class="g2-r" style="--n:%d"><span class="g2-k titel">%s</span><div><span class="etikett">%s</span><p>%s</p></div></div>' % (j, a, E(b), E(c)) for j, (a, b, c) in enumerate(ST[1:]))
    return sek(n, kopf() + '<div class="g2 vauf"><div class="g2-l"><span class="g2-z titel">%s</span><span class="etikett">%s</span><p>%s</p></div><div class="g2-rs">%s</div></div>' % (z, E(q), E(t), r) + presse())
V.append(('Die grosse 91', v02))


# 03 · Das Gästebuch: links Titel und Presse, rechts ein cremefarbenes Blatt mit Linien, darauf die drei Stimmen als Einträge.
# Das Blatt wird schräg hingelegt und dreht sich gerade.
def v03(n):
    e = ''.join('<div class="b3-e"><span class="b3-z titel">%s</span><div><span class="etikett">%s</span><p>%s</p></div></div>' % (z, E(q), E(t)) for z, q, t in ST)
    return sek(n, '<div class="b3"><div class="b3-l">%s%s</div><div class="b3-blatt vauf"><div class="b3-papier hell">%s</div></div></div>' % (kopf(), presse(), e))
V.append(('Das Gästebuch', v03))


# 04 · Die Bierdeckel: drei runde Deckel, cremefarben mit rotem Rand, die Zahl in der Mitte. Darunter Satz.
# Die Deckel fallen gedreht von oben auf den Tresen und bleiben leicht schief liegen.
def v04(n):
    d = ''.join('<div class="d4-s" style="--n:%d;--w:%sdeg"><div class="d4-deckel"><div class="d4-in"><span class="d4-z titel">%s</span><span class="etikett">%s</span></div></div><p>%s</p></div>' % (j, w, z, E(q), E(t)) for j, ((z, q, t), w) in enumerate(zip(ST, (-6, 4, -2))))
    return sek(n, kopf() + '<div class="d4 vauf">%s</div>' % d + presse())
V.append(('Die Bierdeckel', v04))


# 05 · Die Skala: jede Note auf ihrer Messlatte, 91 von 100, 4,8 von 5. Goldene Linien füllen sich bis zur Note.
def v05(n):
    r = ''.join('<div class="s5-r" style="--n:%d;--f:%s"><div class="s5-k"><span class="s5-z titel">%s</span><span class="etikett">%s</span></div><div class="s5-b"><div class="s5-spur"><i class="s5-voll"></i><b class="s5-ende">%s</b></div><p>%s</p></div></div>' % (
        j, f, z, E(q), m, E(t)) for j, ((z, q, t), f, m) in enumerate(zip(ST, (.91, .96, .96), ('100', '5', '5'))))
    return sek(n, kopf() + '<div class="s5 vauf">%s</div>' % r + presse())
V.append(('Die Skala', v05))


# 06 · Die Plakette: Falstaff als Messingschild in der Mitte, doppelt gerahmt in Gold. Links und rechts die beiden 4,8 frei.
# Das Schild kippt aus der Wand nach vorn und hängt gerade, die Seiten steigen danach.
def v06(n):
    z, q, t = ST[0]
    def frei(j, a, b, c):
        return '<div class="p6-f" style="--n:%d"><span class="p6-k titel">%s</span><span class="etikett">%s</span><p>%s</p></div>' % (j, a, E(b), E(c))
    return sek(n, kopf() + '<div class="p6 vauf">%s<div class="p6-schild"><div class="p6-in"><span class="etikett">%s</span><span class="p6-z titel">%s</span><p>%s</p></div></div>%s</div>' % (
        frei(1, *ST[1]), E(q), z, E(t), frei(2, *ST[2])) + presse())
V.append(('Die Plakette', v06))


# 07 · Das Laufband: ein cremefarbenes Band über die ganze Breite, darin die drei Zahlen mit Quelle in grosser Schrift.
# Das Band zieht beim Scrollen langsam mit. Darunter die drei Sätze.
def v07(n):
    eins = ''.join('<span class="l7-e"><b class="titel">%s</b><span class="etikett">%s</span><i></i></span>' % (z, E(q)) for z, q, t in ST)
    s = ''.join('<div class="l7-s" style="--n:%d"><span class="etikett">%s</span><p>%s</p></div>' % (j, E(q), E(t)) for j, (z, q, t) in enumerate(ST))
    return sek(n, '<div class="innen">%s</div><div class="l7-band hell" aria-hidden="true"><div class="l7-lauf" data-lauf>%s</div></div><div class="innen"><div class="l7-drei vauf">%s</div>%s</div>' % (
        kopf(), eins * 4, s, presse()), innen=False)
V.append(('Das Laufband', v07))


# 08 · Die Zeitungsseite: ein cremefarbenes Blatt mit Kopfzeile zwischen doppelten Linien, drei Spalten mit Spaltenlinien,
# unten die Presse über die ganze Breite. Das Blatt legt sich aus einer leichten Schräge flach.
def v08(n):
    sp = ''.join('<div class="n8-sp" style="--n:%d"><span class="n8-z titel">%s</span><span class="etikett">%s</span><p>%s</p></div>' % (j, z, E(q), E(t)) for j, (z, q, t) in enumerate(ST))
    return sek(n, '<div class="n8 vauf"><div class="n8-blatt hell"><div class="n8-kopf">%s</div><div class="n8-spalten">%s</div><p class="n8-presse">%s</p></div></div>' % (
        kz() + h2(), sp, E(PRESSE)))
V.append(('Die Zeitungsseite', v08))


# 09 · Die Flaschenetiketten: drei hohe Etiketten mit gewölbtem Kopf und feinem Innenrahmen, wie auf den Flaschen hinter der Theke.
# Sie kommen nacheinander hinter einer goldenen Kante hoch.
def v09(n):
    e = ''.join('<div class="e9-s" style="--n:%d"><div class="e9-et hell"><div class="e9-in"><span class="etikett">%s</span><i></i><span class="e9-z titel">%s</span><i></i><p>%s</p></div></div></div>' % (j, E(q), z, E(t)) for j, (z, q, t) in enumerate(ST))
    return sek(n, kopf() + '<div class="e9 vauf"><div class="e9-reihe">%s</div><i class="e9-kante"></i></div>' % e + presse())
V.append(('Die Flaschenetiketten', v09))


# 10 · Der Fächer: die drei Platten liegen zuerst übereinander gefächert wie Karten in der Hand
# und legen sich dann nebeneinander, jede leicht schräg.
def v10(n):
    k = ''.join('<div class="f10-k platte" style="--n:%d"><span class="f10-z titel">%s</span><span class="etikett">%s</span><p>%s</p></div>' % (j, z, E(q), E(t)) for j, (z, q, t) in enumerate(ST))
    return sek(n, kopf() + '<div class="f10 vauf">%s</div>' % k + presse())
V.append(('Der Fächer', v10))


# 11 · Die Anmerkungen: der Titel selbst wird riesig, unter jeder Zahl hängt ihre Quelle mit Satz wie eine Randnotiz an einer goldenen Linie.
def v11(n):
    def zahl(j, z, q, t, komma):
        return '<span class="a11-g" style="--n:%d"><span class="a11-m"><span class="a11-z titel">%s<span class="a11-k">%s</span></span></span><span class="a11-notiz"><i></i><span class="etikett">%s</span><span class="a11-p">%s</span></span></span>' % (j, z, komma, E(q), E(t))
    t = '<h2 class="titel a11-titel" aria-label="91, 4,8 und 4,8.">%s%s<span class="a11-und"><span class="a11-m"><span class="titel">und</span></span></span>%s</h2>' % (
        zahl(0, *ST[0], ','), zahl(1, *ST[1], ''), zahl(2, *ST[2], '.'))
    return sek(n, kz() + '<div class="a11 vauf">%s</div>' % t + presse())
V.append(('Die Anmerkungen', v11))


# 12 · Die Wechselzahl: links steht eine grosse Zahl fest, rechts laufen die drei Quellen vorbei.
# Je nachdem, welche Quelle in der Mitte steht, wechselt links die Zahl.
def v12(n):
    zs = ''.join('<span class="w12-z titel" data-w="%d">%s</span>' % (j, z) for j, (z, q, t) in enumerate(ST))
    r = ''.join('<div class="w12-e" data-w="%d"><span class="w12-iz titel">%s</span><span class="etikett">%s</span><p class="w12-p">%s</p></div>' % (j, z, E(q), E(t)) for j, (z, q, t) in enumerate(ST))
    return sek(n, '<div class="w12" data-wechsel><div class="w12-l"><div class="w12-steh">%s<div class="w12-zahlen">%s</div></div></div><div class="w12-r">%s%s</div></div>' % (kopf(), zs, r, presse(1)))
V.append(('Die Wechselzahl', v12))


# 13 · Der Bon: links Titel und Presse, rechts ein schmaler Kassenbon mit gezackter Kante.
# Jede Quelle mit Punktlinie bis zur Zahl, darunter der Satz. Der Bon läuft aus dem Schlitz der Kasse.
def v13(n):
    z = ''.join('<div class="k13-zeile"><div class="k13-oben"><span>%s</span><i></i><b class="titel">%s</b></div><p>%s</p></div>' % (E(q), z, E(t)) for z, q, t in ST)
    return sek(n, '<div class="k13"><div class="k13-l">%s%s</div><div class="k13-kasse vauf"><i class="k13-schlitz"></i><div class="k13-fenster"><div class="k13-bon hell"><span class="etikett k13-kopf">Was andere sagen</span>%s</div></div></div></div>' % (kopf(), presse(), z))
V.append(('Der Bon', v13))


# 14 · Die Weinkarte: drei Zeilen über die ganze Breite wie auf einer Karte, Quelle links, Satz in der Mitte, Zahl rechts gross.
# Goldene Haarlinien ziehen sich zwischen den Zeilen, die Zeilen steigen nacheinander.
def v14(n):
    r = ''.join('<div class="w14-r" style="--n:%d"><i class="w14-linie"></i><span class="etikett">%s</span><p>%s</p><span class="w14-z titel">%s</span></div>' % (j, E(q), E(t), z) for j, (z, q, t) in enumerate(ST))
    return sek(n, kopf() + '<div class="w14 vauf">%s<i class="w14-linie w14-end"></i></div>' % r + presse())
V.append(('Die Weinkarte', v14))


# 15 · Die Leuchtschrift: die drei Zahlen als rote Leuchtröhren in schmalen Rahmen, wie Schilder über einer Bar.
# Beim Auftritt flackern sie nacheinander an.
def v15(n):
    s = ''.join('<div class="n15-s" style="--n:%d"><div class="n15-rohr"><span class="n15-z titel">%s</span></div><span class="etikett">%s</span><p>%s</p></div>' % (j, z, E(q), E(t)) for j, (z, q, t) in enumerate(ST))
    return sek(n, kopf() + '<div class="n15 vauf">%s</div>' % s + presse())
V.append(('Die Leuchtschrift', v15))


def seite(n):
    h = unter.haus()
    if n:
        a = h.rfind('<section', 0, h.find('id="stimmen"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[i + 1, nm] for i, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/x.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(V[n - 1][0] if n else 'Heutiger Stand'))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/x.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
