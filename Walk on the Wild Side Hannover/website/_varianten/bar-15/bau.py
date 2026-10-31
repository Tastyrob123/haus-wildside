# Walk on the Wild Side · Startseite, Abschnitt «Eure Nachbarschafts-Mixology-Bar» (id="bar"): 15 Fassungen (29.10.2026).
# Robert: «gib mir 15 alternative visualisierungen von dem abschnitt». 00 = heutiger Stand.
# Jede Fassung eine eigene Darstellung UND ein eigener Effekt; Inhalt bleibt Wort für Wort (Titel, Satz, Wer/Wo/Wann aus bau.py).
# Nur echte Fotos der Bar (bilder.py), nur transform und opacity, nativer Scroll.
# Wechsel mit ← → (varianten-nav.js), man bleibt am Abschnitt. Aufruf: python3 _varianten/bar-15/bau.py → 00.html … 15.html
import os, sys, re, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, LOGO, HAUS, kz, mache
from bilder import BILDER

ORD = '_varianten/bar-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('bar15.css', 'bar15.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('index.html').read()
a = basis.index('<section class="kap auf" id="bar">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]

T = ['Eure Nachbarschafts-', 'Mixology-Bar.']
SATZ = ('So nennt sich das Wild Side selbst, und so ist es gemeint: eine kleine Bar an der Ecke, in der man sich kennt, mit Drinks, für die man sonst weit fahren müsste. '
        'Seit 2017 unter dieser Decke, seit November 2023 mit Derya und Momo hinter der Theke. Im Falstaff Bar Guide 2027 mit 91 Punkten.')
FAKTEN = [('Wer', 'Derya Ivkin führt die Bar, Momo Ben Khelifa mixt'), ('Wo', HAUS['adresse'] + ', ' + HAUS['ecke']),
          ('Wann', HAUS['zeit_kurz'].replace(' · ', '<br>'))]
KZ = kz('19:30', 'An der Ecke', 0)
UEBER = '<p class="ueber sw" style="--i:0">Und dann fragt Momo.</p>'


def img(k, sizes='50vw', pos=None, sofort=False):
    d = mache(k)
    ss = ', '.join('assets/bild/%s?v=%s %dw' % (f, bau.V, w) for w, f in d['stufen'])
    st = ' style="object-position:%s"' % pos if pos else ''
    if sofort:
        return '<img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s>' % (d['stufen'][-1][1], bau.V, ss, sizes, E(d['alt']), d['w'], d['h'], st)
    return '<img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" loading="lazy" width="%d" height="%d"%s>' % (ss, sizes, E(d['alt']), d['w'], d['h'], st)


def fig(k, cls='', sizes='50vw', pos=None, attr='', sofort=False, stil=''):
    return '<figure class="vb %s" style="--lq:url(%s);%s"%s>%s</figure>' % (cls, mache(k)['lq'], stil, attr, img(k, sizes, pos, sofort))


def titel(cls='', zeilen=T, i0=1):
    return '<h2 class="titel vt %s">%s</h2>' % (cls, bau.zl(zeilen, i0=i0))


def satz(cls='', i=3):
    return '<p class="vtx sw %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def fakten(cls='', i=4):
    return '<div class="vf sw %s" style="--i:%d">%s</div>' % (cls, i, ''.join('<div><span class="etikett">%s</span><p>%s</p></div>' % (E(x), y) for x, y in FAKTEN))


def logo(cls=''):
    return '<span class="vlogo %s">%s</span>' % (cls, LOGO)


def kap(n, inner, extra=''):
    return '<section class="kap auf v%02d %s" id="bar" data-v="%d"><div class="innen">%s</div></section>' % (n, extra, n, inner)


V = []

# 01 Die Wand: Titel über die ganze Breite, darunter Satz und Fakten, dann vier Bilder Wand an Wand, die nacheinander hochsteigen
V.append(('Die Wand', lambda n: kap(n,
    KZ + titel('v-riesig') +
    '<div class="v01-zeile">%s%s</div>' % (satz(), fakten()) +
    '<div class="v01-wand">%s</div>' % ''.join(fig(k, '', '25vw', p, stil='--n:%d' % j) for j, (k, p) in enumerate(
        [('fenster', None), ('anstossen', None), ('negroni', None), ('freundinnen', None)])) + UEBER)))

# 02 Das Plakat bleibt stehen: links das Plakat, es hält beim Scrollen still, rechts ziehen sechs Bilder vorbei
def v02(n):
    bilder = [('fenster', 'a1'), ('anstossen', 'b1'), ('negroni', 'a2'), ('theke', 'b2'), ('freundinnen', 'a3'), ('flaschen', 'b3')]
    return kap(n, KZ + '<div class="v02-raster"><div class="v02-links"><div class="plakat v02-plakat">%s%s%s%s</div></div><div class="v02-bilder">%s</div></div>%s' % (
        logo(), titel(), satz(), fakten(), ''.join(fig(k, c, '25vw') for k, c in bilder), UEBER))
V.append(('Das Plakat bleibt stehen', v02))

# 03 Laufband: grosser Titel mittig, Satz, darunter ein endlos laufendes Band aus zehn Bildern über die ganze Breite, Fakten als Zeile
def v03(n):
    reihe = ['fenster', 'anstossen', 'negroni', 'theke', 'freundinnen', 'flaschen', 'schild-ecke', 'momo-lacht', 'glas-rot', 'rueckbar']
    band = ''.join(fig(k, '', '320px') for k in reihe)
    return kap(n, '<div class="v03-kopf">%s%s%s</div><div class="v03-band" aria-hidden="false"><div class="v03-spur">%s%s</div></div>%s%s' % (
        KZ, titel('v-riesig'), satz(), band, band.replace('<img ', '<img aria-hidden="true" '), fakten('v-zeile'), UEBER))
V.append(('Laufband', v03))

# 04 Wer, Wo, Wann zeigen das Bild: grosses Bild links; fährt man über eine Zeile (oder wartet), schiebt sich das passende Foto herein
def v04(n):
    bilder = [('fenster', 'Die Bar'), ('derya', 'Wer'), ('schild-ecke', 'Wo'), ('voll', 'Wann')]
    rahmen = ''.join(fig(k, 'v04-dia' + (' an' if j == 0 else ''), '58vw', '35% 50%' if k == 'derya' else None, ' data-i="%d"' % j) for j, (k, _) in enumerate(bilder))
    zeilen = ''.join('<button class="v04-z" data-i="%d"><span class="etikett">%s</span><span class="v04-w">%s</span><i></i></button>' % (j + 1, E(x), y) for j, (x, y) in enumerate(FAKTEN))
    return kap(n, '<div class="v04-raster"><div class="v04-bild">%s</div><div class="v04-text">%s%s%s<div class="v04-zeilen sw" style="--i:4">%s</div></div></div>%s' % (
        rahmen, KZ, titel(), satz(), zeilen, UEBER))
V.append(('Wer, Wo, Wann zeigen das Bild', v04))

# 05 Hell, mit Diashow: der ganze Abschnitt auf Creme wie die Plakate, rechts ein grosses Bild, das von selbst weiterblättert, mit Zähler und Goldlinie
def v05(n):
    reihe = ['theke', 'negroni', 'anstossen', 'flaschen', 'freundinnen', 'fenster']
    spur = ''.join(fig(k, '', '58vw') for k in reihe)
    alts = json.dumps([BILDER[k][1] for k in reihe], ensure_ascii=False).replace('"', '&quot;')
    return kap(n, '<div class="v05-raster"><div class="v05-text">%s%s%s%s%s</div><div class="v05-show sw" style="--i:2" data-alt="%s"><div class="v05-fenster"><div class="v05-spur">%s</div></div>'
                  '<div class="v05-unter"><span class="v05-nr">01 / 06</span><span class="v05-alt">%s</span><span class="v05-linie"><i></i></span></div></div></div>%s' % (
        KZ, logo(), titel(), satz(), fakten(), alts, spur, E(BILDER[reihe[0]][1]), UEBER.replace('class="ueber sw"', 'class="ueber hellu sw"')), 'hell')
V.append(('Hell, mit Diashow', v05))

# 06 Bilder in der Zeile: der Titel steht riesig über drei Zeilen, zwischen den Wörtern öffnen sich kleine Fotos
def v06(n):
    def pille(k, j, pos=None):
        return '<span class="v06-pille" style="--n:%d;--lq:url(%s)">%s</span>' % (j, mache(k)['lq'], img(k, '240px', pos))
    zeilen = ['Eure %s Nachbar&shy;schafts-' % pille('anstossen', 0), '%s Mixology-Bar. %s' % (pille('negroni', 1), pille('freundinnen', 2))]
    t = '<h2 class="titel vt v06-titel">%s</h2>' % ''.join('<span class="v06-z sw" style="--i:%d">%s</span>' % (j + 1, z) for j, z in enumerate(zeilen))
    return kap(n, '<div class="v06-kopf">%s</div>%s<div class="v06-unten">%s%s</div>%s' % (KZ, t, satz(), fakten(), UEBER))
V.append(('Bilder in der Zeile', v06))

# 07 Die Ecke: Titel, darunter drei gleich hohe Felder: der Plan der Kreuzung (die Linien zeichnen sich), das Foto der Ecke, Satz und Fakten
def v07(n):
    plan = ('<svg class="v07-svg" viewBox="0 0 400 400" aria-hidden="true">'
            '<path class="v07-l" d="M-10 250 H410"/><path class="v07-l v07-l2" d="M232 -10 V410"/>'
            '<path class="v07-d" d="M-10 274 H208 V410 M256 410 V274 H410 M-10 226 H208 V-10 M256 -10 V226 H410"/>'
            '<circle class="v07-ring" cx="232" cy="250" r="22"/><circle class="v07-punkt" cx="232" cy="250" r="9"/></svg>'
            '<span class="v07-s v07-s1">Haasemannstraße</span><span class="v07-s v07-s2">Rampenstraße</span>'
            '<span class="v07-hier"><b>13</b>Hier ist die Bar</span>')
    return kap(n, KZ + titel('v-riesig') + '<div class="v07-raster"><div class="v07-plan plakat sw" style="--i:2">%s</div>%s<div class="v07-text">%s%s</div></div>%s' % (
        plan, fig('schild-ecke', 'v07-foto sw', '33vw', stil='--i:3'), satz(), fakten(), UEBER))
V.append(('Die Ecke', v07))

# 08 Das Schild geht an: das rote Logo gross in der Mitte flackert an wie die Leuchtschrift über der Vitrine, darunter Titel, Satz, Fakten und drei Bilder
def v08(n):
    return kap(n, '<div class="v08-kopf">%s%s%s%s</div>%s<div class="v08-drei">%s</div>%s' % (
        logo('v08-logo'), KZ.replace('class="kz sw"', 'class="kz sw v08-kz"'), titel('v-riesig'), satz(), fakten('v-zeile'),
        ''.join(fig(k, 'sw', '33vw', p, stil='--i:%d' % (5 + j)) for j, (k, p) in enumerate([('negroni', None), ('momo-lacht', None), ('glas-rot', None)])), UEBER))
V.append(('Das Schild geht an', v08))

# 09 Drei Bilder, drei Tempi: Titel links, Satz und Fakten rechts; darunter drei hohe Bilder, deren Fotos beim Scrollen verschieden schnell ziehen
def v09(n):
    drei = ''.join('<figure class="vb v09-f" style="--lq:url(%s)"><div class="v09-in" data-tempo="%s">%s</div></figure>' % (mache(k)['lq'], t, img(k, '33vw')) for k, t in
                   [('fenster', '-1'), ('theke', '1'), ('flaschen', '-0.6')])
    return kap(n, '<div class="v09-kopf"><div>%s%s</div><div>%s%s</div></div><div class="v09-drei">%s</div>%s' % (KZ, titel('v-riesig'), satz(), fakten(), drei, UEBER))
V.append(('Drei Bilder, drei Tempi', v09))

# 10 Die Karten wenden sich: drei hohe Karten zeigen erst je ein Foto und drehen sich dann um zu Wer, Wo und Wann; mit der Maus drauf wieder zum Foto
def v10(n):
    karten = ''.join('<div class="v10-karte" style="--n:%d"><div class="v10-dreh"><div class="v10-vorn">%s</div><div class="v10-hinten">%s<span class="etikett">%s</span><p>%s</p></div></div></div>' % (
        j, fig(k, '', '33vw', p), logo(), E(x), y) for j, ((x, y), (k, p)) in enumerate(zip(FAKTEN, [('derya', '30% 50%'), ('schild-ecke', None), ('voll', None)])))
    return kap(n, '<div class="v10-kopf">%s%s%s</div><div class="v10-karten">%s</div>%s' % (KZ, titel('v-riesig'), satz(), karten, UEBER))
V.append(('Die Karten wenden sich', v10))

# 11 Kacheln mit Tiefe: geschlossenes Raster aus Plakat, Fotos und grossen Zahlen aus dem Satz; jede Kachel neigt sich zur Maus
def v11(n):
    def zahl(cls, z, w):
        return '<div class="v11-k v11-zahl %s"><b>%s</b><span>%s</span></div>' % (cls, z, w)
    return kap(n, KZ + '<div class="v11-raster">'
               '<div class="v11-k v11-plakat plakat">%s%s%s%s</div>' % (logo(), titel(), satz(), fakten()) +
               fig('fenster', 'v11-k v11-b1', '25vw') + zahl('v11-rot', '91', 'Punkte im Falstaff<br>Bar Guide 2027') +
               fig('negroni', 'v11-k v11-b2', '25vw') + zahl('v11-dunkel', '2017', 'unter dieser Decke') + fig('anstossen', 'v11-k v11-b3', '25vw') +
               '</div>' + UEBER)
V.append(('Kacheln mit Tiefe', v11))

# 12 Hinein unter die Decke: ein Bild über die ganze Breite, beim Scrollen geht man langsam hinein; darunter Titel, Satz und Fakten in drei Spalten
def v12(n):
    return kap(n, KZ + '</div><div class="v12-buehne">%s</div><div class="innen v12-unten">%s%s%s</div><div class="innen">%s' % (
        fig('decke-hoch', 'v12-bild', '130vw', '50% 62%'), titel(), satz(), fakten(), UEBER))
V.append(('Hinein unter die Decke', v12))

# 13 Die Doppelseite: wie ein aufgeschlagenes Heft mit Goldfalz; links Titel und Satz mit roter Initiale, rechts drei Fotos, die der Maus leicht folgen
def v13(n):
    s = SATZ
    t = '<p class="vtx sw v13-satz" style="--i:3"><span class="v13-ini">%s</span>%s</p>' % (s[0], E(s[1:]))
    rechts = '<div class="v13-rechts">%s%s%s</div>' % (fig('momo-lacht', 'v13-g', '36vw'), fig('glas-negroni', 'v13-k1', '18vw'), fig('freundinnen', 'v13-k2', '18vw'))
    return kap(n, '<div class="v13-heft"><div class="v13-links">%s%s%s%s</div><i class="v13-falz"></i>%s</div>%s' % (KZ, titel(), t, fakten(), rechts, UEBER))
V.append(('Die Doppelseite', v13))

# 14 Von der Strasse an die Theke: ein breites Bild und ein Regler darunter; zieht man ihn, geht man von der Ecke durch die Tür bis ans Glas
def v14(n):
    weg = [('schild-ecke', 'Die Ecke', '50% 60%'), ('tuer-rot', 'Die Tür', '50% 50%'), ('fenster', 'Das Fenster', '50% 55%'), ('theke', 'Die Theke', '50% 70%'),
           ('negroni', 'Die Rückbar', '50% 35%'), ('anstossen', 'Das Glas', '50% 40%')]
    spur = ''.join(fig(k, '', '92vw', p) for k, _, p in weg)
    stopps = ''.join('<button class="v14-stopp%s" data-i="%d"><span>%s</span></button>' % (' an' if j == 0 else '', j, E(w)) for j, (_, w, _) in enumerate(weg))
    return kap(n, KZ + '<div class="v14-buehne sw" style="--i:1"><div class="v14-spur">%s</div></div>'
                  '<div class="v14-regler sw" style="--i:2"><input type="range" min="0" max="%d" step="0.001" value="0" aria-label="Von der Strasse an die Theke"><div class="v14-stopps">%s</div></div>'
                  '<div class="v14-unten"><div>%s</div><div>%s%s</div></div>%s' % (spur, len(weg) - 1, stopps, titel(), satz(), fakten(), UEBER))
V.append(('Von der Strasse an die Theke', v14))

# 15 Der Satz wird hell: Titel und Satz riesig in der Titelschrift, Wort für Wort wird es beim Scrollen hell; darunter Fakten und ein Streifen aus fünf Bildern
def v15(n):
    woerter = ' '.join('<span class="v15-w">%s</span>' % E(w) for w in SATZ.split(' '))
    streifen = ''.join(fig(k, '', '20vw') for k in ['fenster', 'anstossen', 'negroni', 'freundinnen', 'flaschen'])
    return kap(n, KZ + titel('v15-titel') + '<p class="v15-satz" data-hell>%s</p>%s<div class="v15-streifen staffel">%s</div>%s' % (woerter, fakten('v-zeile'), streifen.replace('class="vb ', 'class="vb sw '), UEBER))
V.append(('Der Satz wird hell', v15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = ('<link rel="stylesheet" href="%s/bar15.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER))


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/bar15.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
