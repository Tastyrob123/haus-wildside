# Walk on the Wild Side · Haus-Seite, Abschnitt «Der Raum»: 15 neue Fassungen (31.10.2026).
# Robert: «finde die beiden steckbriefe wie bei 2 gut aber den oberen bereich bitte nochmal andere neue ideen 15 weitere».
# Steckbriefe sind seit 31.10.2026 in der Seite; hier wird nur #raum getauscht. 00 = heutiger Stand. Andere Ideen als _varianten/haus-15.
# Texte Wort für Wort aus unter.py, dieselben sechs Bilder. Nur transform und opacity, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/haus-15b/bau.py → 00 … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/haus-15b'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

RAUM = [('decke-bar', 'Die Decke: ein Gewölbe als Druck über dem ganzen Raum, blau und silbern angeleuchtet.'),
        ('negroni', 'NEGRONI in Glühbirnen über der Vitrine. Der Schriftzug sagt, was hier jeden Abend gerührt wird.'),
        ('theke', 'Die Theke mit dem gelben Licht unter der Kante. Hier wird gefragt, was du magst.'),
        ('rueckbar-breit', 'Die Rückbar: Flaschen, die man nicht in jedem Laden findet, und eine beleuchtete Vitrine.'),
        ('fenster', 'Von der Strasse aus sieht man die Rückbar durchs Fenster, oben spiegelt sich die Decke.'),
        ('tuer-rot', 'Durch die Tür: der rote Boden, links die Theke, hinten die Stufen hinauf zur Empore.')]
_q = open('unter.py').read()
for _, t in RAUM:
    assert t in _q, 'Text weicht von der Seite ab: ' + t


def foto(k, sizes='33vw', cls='', stil=''):
    return '<figure class="hv-f %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, B.img_tag(k, sizes))


def F(j, sizes='33vw', cls='', stil=''):
    return foto(RAUM[j][0], sizes, cls, stil)


def S(j):
    return E(RAUM[j][1])


def kopf(cls=''):
    return '<div class="hv-kopf %s">%s%s</div>' % (cls, B.kz('Der Raum', 'Fünf Blicke', 0), B.h2(['Klein, dunkel,', 'warm.']))


def sek(inner, cls='', voll=''):
    return '<section class="kap auf hv %s" id="raum"><div class="innen">%s</div>%s</section>' % (cls, inner, voll)


V = []

# 01 · Drei Worte: der Titel zerfällt in seine drei Worte, jedes riesig, mit zwei Bildern daneben. Klein: Tür und Theke. Dunkel: Decke und Fenster. Warm: NEGRONI und Rückbar.
# Je Wort eine eigene Bewegung: aus dem Schlitz und steigen, sich setzen, aus der Tiefe.
def v01():
    worte = [('Klein,', (5, 2)), ('dunkel,', (0, 4)), ('warm.', (1, 3))]
    bew = ['w1-steigt', 'w1-setzt', 'w1-tiefe']
    h = '<div class="hv-kopf">%s<h2 class="hv-weg-sr">Klein, dunkel, warm.</h2></div>' % B.kz('Der Raum', 'Fünf Blicke', 0)
    for n, (w, js) in enumerate(worte):
        h += '<div class="auf w1 %s %s"><p class="titel w1-wort" aria-hidden="true">%s</p><div class="w1-paar">%s</div></div>' % (
            'w1-r' if n % 2 else '', bew[n], B.zl([w]), ''.join('<figure class="w1-b" style="--n:%d">%s<figcaption class="text">%s</figcaption></figure>' % (m, F(j, '(max-width:760px) 50vw, 28vw'), S(j)) for m, j in enumerate(js)))
    return sek(h)
V.append(('Drei Worte', v01))

# 02 · Die Wandtafel: die sechs Sätze gross in zwei Spalten, jeder mit seinem Bild davor; die Haarlinien ziehen sich auf, Zeigen hebt das Bild.
def v02():
    z = ''.join('<div class="t2-z" style="--n:%d">%s<p class="titel">%s</p><i class="t2-linie"></i></div>' % (j, F(j, '160px'), S(j)) for j in range(6))
    return sek(kopf() + '<div class="auf t2">%s</div>' % z)
V.append(('Die Wandtafel', v02))

# 03 · Der Stapel: die Bilder liegen als Stapel, beim Scrollen fliegt das oberste nach oben weg und gibt das nächste frei; der Satz daneben wechselt mit. Der Abschnitt hält dafür kurz an.
def v03():
    karten = ''.join('<div class="s3-k" style="--i:%d;--r:%ddeg;z-index:%d">%s</div>' % (j if j < 5 else 99, (-3, 2, -1, 3, -2, 1)[j], 10 - j, F(j, '(max-width:760px) 80vw, 40vw')) for j in range(6))
    saetze = ''.join('<p class="titel s3-s" data-z="%d">%s</p>' % (j, S(j)) for j in range(6))
    return sek(kopf(), 's3-sek', '<div class="s3" data-pin data-schritte="6" data-tausch><div class="s3-buehne"><div class="innen s3-innen"><div class="platte s3-text"><div class="s3-saetze">%s</div><div class="s3-zaehl"><i></i></div></div><div class="s3-stapel">%s</div></div></div></div>' % (saetze, karten))
V.append(('Der Stapel', v03))

# 04 · Die Birnen gehen an: über den Bildern eine Reihe Glühbirnen wie im NEGRONI-Schriftzug; beim Scrollen geht eine nach der anderen an, und mit ihnen werden die Bilder hell.
def v04():
    birnen = ''.join('<i style="--d:%d"></i>' % d for d in range(28))
    b = ''.join('<figure class="b4-k" style="--n:%d"><div class="b4-bild">%s<i class="b4-dunkel"></i></div><figcaption class="text">%s</figcaption></figure>' % (j, F(j, '(max-width:760px) 50vw, 33vw'), S(j)) for j in range(6))
    return sek(kopf() + '<div class="b4" data-p><div class="b4-birnen" aria-hidden="true">%s</div><div class="b4-raster">%s</div></div>' % (birnen, b))
V.append(('Die Birnen gehen an', v04))

# 05 · Die Mitte: links und rechts je drei Bilder als Säule, in der Mitte eine helle Platte mit dem Satz zum Bild, auf das man zeigt. Die Säulen kommen gegeneinander, von oben und von unten.
def v05():
    li = ''.join('<div class="m5-b" data-t="%d">%s</div>' % (j, F(j, '(max-width:760px) 50vw, 26vw')) for j in (2, 5, 4))
    re = ''.join('<div class="m5-b" data-t="%d">%s</div>' % (j, F(j, '(max-width:760px) 50vw, 26vw')) for j in (0, 1, 3))
    mitte = '<div class="m5-mitte hell"><span class="etikett">Der Raum</span><div class="m5-saetze">%s</div></div>' % ''.join('<p class="titel" data-z="%d">%s</p>' % (j, S(j)) for j in range(6))
    return sek(kopf() + '<div class="auf m5" data-tausch><div class="m5-sp m5-l">%s</div>%s<div class="m5-sp m5-r">%s</div></div>' % (li, mitte, re))
V.append(('Die Mitte', v05))

# 06 · Wie die Steckbriefe: drei Zeilen in der Sprache der Steckbriefe darunter, je ein grosses Bild und eine Platte über der Kante; in der Platte ein zweites Bild und beide Sätze. Die Platte senkt sich von oben auf das Bild.
def v06():
    paare = [(3, 1), (2, 5), (4, 0)]
    h = ''.join('<div class="auf p6 %s"><div class="p6-b">%s</div><div class="platte p6-p">%s<p class="text"><b>%s</b></p><p class="text">%s</p></div></div>' % (
        'p6-r' if n % 2 else '', F(g, '(max-width:760px) 100vw, 60vw'), F(k, '(max-width:760px) 80vw, 30vw', 'p6-klein'), S(g), S(k)) for n, (g, k) in enumerate(paare))
    return sek(kopf() + h)
V.append(('Wie die Steckbriefe', v06))

# 07 · Kleine Steckbriefe: sechs Karten im Raster, an jeder Bildkante eine kleine Platte mit dem Satz, versetzt; erst setzt sich das Bild, dann steigt die Platte.
def v07():
    k = ''.join('<figure class="k7" style="--n:%d">%s<figcaption class="platte k7-p"><p class="text">%s</p></figcaption></figure>' % (j, F(j, '(max-width:760px) 100vw, 33vw'), S(j)) for j in range(6))
    return sek(kopf() + '<div class="auf k7-raster">%s</div>' % k)
V.append(('Kleine Steckbriefe', v07))

# 08 · Die Zeitungsseite: auf hellem Papier drei Spalten mit Linien wie in der Neuen Presse, links die Decke hoch, in der Mitte zwei, rechts drei Bilder, jeder Satz als Bildzeile; die Spalten legen sich nacheinander hin.
def v08():
    sp = [[0], [1, 2], [3, 4, 5]]
    h = ''.join('<div class="z8-sp" style="--n:%d">%s</div>' % (c, ''.join('<figure class="z8-e">%s<figcaption>%s</figcaption></figure>' % (F(j, '(max-width:760px) 100vw, 33vw'), S(j)) for j in js)) for c, js in enumerate(sp))
    return sek(kopf() + '<div class="auf z8"><i class="z8-linie"></i><div class="z8-spalten">%s</div></div>' % h, 'hell z8-sek')
V.append(('Die Zeitungsseite', v08))

# 09 · Der Rundgang: der Abschnitt hält an, und beim Scrollen geht man seitwärts durch die Bar: von der Strasse durch die Tür, an der Theke vorbei bis unter die Decke. Unter jedem Bild sein Satz, eine Goldlinie zeigt den Weg.
def v09():
    folge = [4, 5, 2, 3, 1, 0]
    b = ''.join('<figure class="r9-f">%s<figcaption class="text">%s</figcaption></figure>' % (F(j, '(max-width:760px) 70vw, 34vw'), S(j)) for j in folge)
    return sek(kopf(), 'r9-sek', '<div class="r9" data-pin><div class="r9-buehne"><div class="r9-zug">%s</div><div class="innen r9-weg"><i></i></div></div></div>' % b)
V.append(('Der Rundgang', v09))

# 10 · Der Guckkasten: die Bilder bauen den Raum nach. Hinten die Rückbar, oben die Decke, unten der rote Boden, links Theke und NEGRONI, rechts das Fenster. Beim Scrollen geht man hinein. Zeigen auf einen Satz hebt seine Wand.
def v10():
    w = lambda cls, js: '<div class="g10-w %s">%s</div>' % (cls, ''.join('<div class="g10-f" data-z="%d">%s</div>' % (j, F(j, '(max-width:760px) 60vw, 40vw')) for j in js))
    box = w('g10-hinten', (3,)) + w('g10-oben', (0,)) + w('g10-unten', (5,)) + w('g10-links', (2, 1)) + w('g10-rechts', (4,))
    saetze = ''.join('<p class="text g10-s" data-t="%d" style="--n:%d">%s</p>' % (j, j, S(j)) for j in (0, 3, 1, 2, 4, 5))
    return sek(kopf() + '<div class="auf g10" data-tausch data-frei><div class="g10-kasten" data-p><div class="g10-box">%s</div></div><div class="g10-saetze">%s</div></div>' % (box, saetze))
V.append(('Der Guckkasten', v10))

# 11 · Die Decke bleibt: links steht die Decke hoch und bleibt stehen, während rechts die anderen fünf Blicke vorbeiziehen; sie setzen sich einzeln.
def v11():
    rechts = ''.join('<figure class="d11-e" style="--n:%d">%s<figcaption class="text">%s</figcaption></figure>' % (n, F(j, '(max-width:760px) 50vw, 28vw'), S(j)) for n, j in enumerate((1, 2, 3, 4, 5)))
    return sek(kopf() + '<div class="d11"><div class="d11-halt"><figure class="auf d11-decke">%s<figcaption class="platte"><p class="titel">%s</p></figcaption></figure></div><div class="auf d11-rechts">%s</div></div>' % (
        F(0, '(max-width:760px) 100vw, 42vw'), S(0), rechts))
V.append(('Die Decke bleibt', v11))

# 12 · Die Theke entlang: sechs hohe Bilder Kante an Kante wie eine Theke, darunter die gelbe Lichtkante; das Bild, auf das man zeigt, hebt sich, sein Satz steht auf der Kante.
def v12():
    b = ''.join('<div class="e12-b" data-t="%d" style="--n:%d">%s</div>' % (j, j, F(j, '(max-width:760px) 33vw, 17vw')) for j in range(6))
    s = ''.join('<p class="titel" data-z="%d">%s</p>' % (j, S(j)) for j in range(6))
    return sek(kopf() + '<div class="auf e12" data-tausch><div class="e12-reihe">%s</div><i class="e12-kante"></i><div class="e12-satz">%s</div></div>' % (b, s))
V.append(('Die Theke entlang', v12))

# 13 · Die Ecke: zwei Wände treffen sich wie die Hausecke an der Haasemannstraße, links Tür, Theke und NEGRONI, rechts Rückbar, Decke und Fenster; beim Scrollen dreht sich die Ecke fast gerade.
def v13():
    wand = lambda cls, js: '<div class="c13-w %s">%s</div>' % (cls, ''.join('<figure class="c13-e">%s<figcaption class="text">%s</figcaption></figure>' % (F(j, '(max-width:760px) 33vw, 16vw'), S(j)) for j in js))
    return sek(kopf(), '', '<div class="auf c13" data-p>%s%s</div>' % (wand('c13-l', (5, 2, 1)), wand('c13-r', (3, 0, 4))))
V.append(('Die Ecke', v13))

# 14 · Das Regal: zwei Bretter wie in der Rückbar, auf jedem stehen drei Bilder; unter dem Brett hängt zu jedem ein helles Schildchen mit dem Satz. Die Bilder setzen sich aufs Brett, die Schildchen pendeln aus.
def v14():
    brett = lambda js, o: '<div class="r14-brett"><div class="r14-reihe">%s</div><i class="r14-holz"></i><div class="r14-schilder">%s</div></div>' % (
        ''.join('<div class="r14-b" style="--n:%d">%s</div>' % (o + m, F(j, '(max-width:760px) 33vw, 30vw')) for m, j in enumerate(js)),
        ''.join('<p class="r14-s hell" style="--n:%d;--r:%ddeg">%s</p>' % (o + m, (-2, 1.5, -1)[m], S(j)) for m, j in enumerate(js)))
    return sek(kopf() + '<div class="auf r14">%s%s</div>' % (brett((1, 3, 0), 0), brett((2, 4, 5), 3)))
V.append(('Das Regal', v14))

# 15 · Bilder im Satz: die sechs Sätze gross als ein Text, in jedem steht sein Bild als kleines Fenster zwischen den Worten; beim Scrollen werden die Worte nacheinander hell.
def v15():
    teile = [('Die Decke:', 0), ('NEGRONI', 1), ('Die Theke', 2), ('Die Rückbar:', 3), ('Von der Strasse', 4), ('Durch die Tür:', 5)]
    alle = []
    for a, j in teile:
        s = RAUM[j][1]
        assert s.startswith(a)
        alle.append((a, j, s[len(a):].strip()))
    n_w = sum(len((a + ' ' + r).split()) for a, _, r in alle)
    i = 0
    h = ''
    for a, j, r in alle:
        ws = []
        for w in a.split():
            ws.append('<span class="i15-w" style="--w:%.4f">%s</span>' % (i / n_w, E(w))); i += 1
        ws.append('<span class="i15" style="--w:%.4f">%s</span>' % (i / n_w, F(j, '220px').replace('<figure', '<span', 1).replace('</figure>', '</span>')))
        for w in r.split():
            ws.append('<span class="i15-w" style="--w:%.4f">%s</span>' % (i / n_w, E(w))); i += 1
        h += '<p class="titel i15-s">%s</p>' % ' '.join(ws)
    return sek(kopf() + '<div class="i15-text" data-p>%s</div>' % h)
V.append(('Bilder im Satz', v15))

assert len(V) == 15


def seite(n):
    h = unter.haus()
    if n:
        a = h.find('<section class="kap auf" id="raum">')
        b = h.find('</section>', a) + len('</section>')
        assert a > 0 and b > a + 100
        h = h[:a] + V[n - 1][1]() + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>' % (n, E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(16):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 … 15')
