# Walk on the Wild Side · Unterseite Drinks: 15 Fassungen für den Kopf «Was magst du?» (29.10.2026).
# Robert: «gib mir bitte 15 verschiedene Variationen für einen richtig geilen Hero. Für den Drinks-Bereich.» 00 = heute.
# Titel gross (am Desktop 120 px und mehr), Satz gut lesbar; Wortlaut wie heute, nur echte Fotos der Bar, Namen der Klassiker von derselben Seite.
# Jede Fassung eigene Darstellung und eigene Bewegung, nur transform (Ausnahme 11: eine Schicht blendet über die andere). Kein Vorhang, das Foto ist sofort da.
# Wechsel mit ← →. Aufruf: python3 _varianten/drinks-hero/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, mache, img_tag, zl, V as BV

ORD = '_varianten/drinks-hero'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('hero.css', 'hero.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('drinks.html').read()
a = basis.index('<header class="sk auf" id="auftakt">')
b = basis.index('</header>', a) + len('</header>')

SATZ = 'Eine Getränkekarte gibt es im Wild Side nicht. Du sagst Momo, was du magst, und bekommst einen Drink, den es nur an diesem Abend gibt.'
KLASSIKER = ['Negroni', 'Paloma', 'Mexikaner', 'Ohne Alkohol']   # die vier Klassiker weiter unten auf der Seite


def bild(k, cls='', sizes='100vw', pos=None, sofort=True, stil=''):
    d = mache(k)
    ss = ', '.join('assets/bild/%s?v=%s %dw' % (f, BV, w) for w, f in d['stufen'])
    st = ' style="object-position:%s"' % pos if pos else ''
    lade = ' fetchpriority="high"' if sofort else ' loading="lazy"'
    return '<figure class="dh-f %s" style="--lq:url(%s);%s"><img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s%s></figure>' % (
        cls, d['lq'], stil, d['stufen'][-1][1], BV, ss, sizes, E(d['alt']), d['w'], d['h'], lade, st)


def titel(cls='', zeilen=('Was magst du?',), i0=1):
    return '<h1 class="titel dh-t %s">%s</h1>' % (cls, zl(list(zeilen), i0=i0))


def satz(cls='', i=3):
    return '<p class="text sw dh-s %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def kopf(n, inner, cls=''):
    return '<header class="sk-v auf dh dh%02d %s" id="auftakt" data-v="%d">%s</header>' % (n, cls, n, inner)


V = []
V.append(('Langsam heran', 'Ein Negroni füllt den ganzen Schirm, die Kamera fährt beim Öffnen langsam zurück; Titel gross unten links.',
          lambda n: kopf(n, bild('glas-negroni', 'dh-voll', '100vw', '50% 55%') + '<div class="innen dh-unten">%s%s</div>' % (titel(), satz()))))
V.append(('Drei Gläser', 'Drei hohe Fotos Kante an Kante über die ganze Breite, sie steigen nacheinander herein; der Titel liegt über allen dreien.',
          lambda n: kopf(n, '<div class="dh02-drei">%s%s%s</div><div class="innen dh-unten">%s%s</div>' % (
              bild('glas-coupe', '', '34vw'), bild('momo-giesst', '', '34vw', '62% 40%'), bild('glas-rot', '', '34vw'), titel(), satz()))))
V.append(('Die Frage steht', 'Links auf Nacht die Frage Wort für Wort untereinander, rechts Momo hinter der Theke bis an den Rand.',
          lambda n: kopf(n, '<div class="dh03-l"><div>%s%s</div></div>%s' % (titel('', ('Was', 'magst', 'du?')), satz('', 4), bild('momo-lacht', 'dh03-r', '50vw', '58% 40%')))))
def h04(n):
    worte = [('sauer', 'glas-sour'), ('süss', 'glas-coupe'), ('bitter', 'glas-negroni')]
    rad = ''.join('<span%s>%s</span>' % (' class="an"' if j == 0 else '', E(w)) for j, (w, _) in enumerate(worte))
    fotos = ''.join(bild(k, 'dh04-b' + (' an' if j == 0 else ''), '40vw') for j, (_, k) in enumerate(worte))
    return kopf(n, '<div class="innen dh04-in"><div>%s<p class="dh04-rad sw" style="--i:2"><span class="dh04-fix">Lieber</span><span class="dh04-w">%s</span><span class="dh04-fix">?</span></p>%s</div><div class="dh04-rahmen sw" style="--i:2">%s</div></div>' % (
        titel(), rad, satz('', 3), fotos))
V.append(('Sauer, süss oder bitter', 'Unter dem Titel wechselt ein goldenes Wort aus der Frage an der Theke, das Foto daneben wechselt mit.', h04))
V.append(('Das runde Fenster', 'Ein grosses rundes Foto in der Mitte öffnet sich beim Laden, der Titel liegt mittig über seinem unteren Rand.',
          lambda n: kopf(n, '<div class="dh05-kreis">%s</div><div class="innen dh05-text">%s%s</div>' % (bild('anstossen', '', '70vw', '50% 40%'), titel(), satz()))))
def h06(n):
    r1 = ''.join(bild(k, '', '22vw', None, False) for k in ['glas-coupe', 'glas-rot', 'schaum', 'glas-sour', 'glas-kerze', 'glas-hand'])
    r2 = ''.join(bild(k, '', '22vw', None, False) for k in ['momo-giesst', 'rueckbar', 'flaschen', 'negroni', 'glas-trinkt', 'anstossen'])
    return kopf(n, '<div class="dh06-reihen"><div class="dh06-r"><div class="dh06-zug">%s%s</div></div><div class="dh06-r dh06-r2"><div class="dh06-zug">%s%s</div></div></div>'
                   '<div class="dh06-schild"><svg class="dh06-linie" aria-hidden="true"><rect x="10" y="10" rx="8" ry="8" pathLength="100"/></svg>%s%s</div>' % (r1, r1, r2, r2, titel(), satz()))
V.append(('Die Gläser laufen', 'Hinten laufen zwei Reihen Fotos langsam gegeneinander, vorn steht der Titel auf einem dunklen Schild mit Goldlinie.', h06))
V.append(('Tiefe beim Scrollen', 'Die Rückbar über den ganzen Schirm; beim Scrollen bleibt das Foto zurück und der Titel zieht schneller nach oben.',
          lambda n: kopf(n, '<div class="dh07-tief">%s</div><div class="innen dh-unten dh07-vorn">%s%s</div>' % (bild('rueckbar', 'dh-voll', '100vw', '50% 45%'), titel(), satz()))))
V.append(('Das Glas in der Mitte', 'In der Mitte ein hohes Foto über die ganze Höhe, links und rechts davon die zwei Teile der Frage riesig.',
          lambda n: kopf(n, '<div class="dh08-l">%s%s</div>%s<div class="dh08-r">%s</div>' % (
              titel('', ('Was magst',)), satz('', 3), bild('glas-hand', 'dh08-m', '34vw'), titel('', ('du?',), 2)))))
V.append(('Die Karte ohne Karte', 'Titel und Satz oben, darunter fünf Gläser Wand an Wand wie eine Karte ohne Worte; jedes kommt aus einer anderen Tiefe.',
          lambda n: kopf(n, '<div class="innen dh09-oben">%s%s</div><div class="dh09-glaeser">%s</div>' % (
              titel(), satz(), ''.join(bild(k, '', '20vw', None, j < 2, '--d:%dpx' % d) for j, (k, d) in enumerate(
                  [('glas-sour', 120), ('glas-coupe', 60), ('glas-rot', 150), ('glas-kerze', 80), ('glas-negroni', 130)]))))))
V.append(('Nur Schrift', 'Kein Foto: die Frage riesig über die ganze Breite, eine Goldlinie zieht sich darunter, darunter der Satz und die vier Klassiker.',
          lambda n: kopf(n, '<div class="innen dh10-in">%s<i class="dh10-linie"></i>%s<p class="dh10-k sw" style="--i:4">%s</p></div>' % (
              titel(), satz(), '<i>·</i>'.join('<span>%s</span>' % E(x) for x in KLASSIKER)))))
def h11(n):
    d = mache('anstossen')
    return kopf(n, '<div class="innen dh11-in"><h1 class="titel dh-t dh11-t"><span class="dh11-hell">Was magst du?</span><span class="dh11-foto" aria-hidden="true" style="background-image:url(assets/bild/%s?v=%s)">Was magst du?</span></h1>%s</div>' % (
        d['stufen'][-1][1], BV, satz('', 2)))
V.append(('Das Foto in der Schrift', 'Die Frage riesig auf Nacht; in den Buchstaben erscheint das Foto der zwei Gläser, die gerade anstossen.', h11))
V.append(('An der Theke, im Glas', 'Zwei Fotos übereinander mit einem goldenen Regler: links Momo beim Giessen, rechts das fertige Glas; der Regler fährt einmal von selbst.',
          lambda n: kopf(n, '<div class="dh12-vergleich" data-vergleich>%s<div class="dh12-oben"><div class="dh12-innen">%s</div></div><span class="dh12-griff"><i></i></span>'
                            '<span class="dh12-l etikett">An der Theke</span><span class="dh12-r etikett">Im Glas</span></div><div class="innen dh-unten">%s%s</div>' % (
              bild('glas-coupe', 'dh-voll', '100vw', '50% 50%'), bild('momo-giesst', 'dh-voll', '100vw', '62% 40%'), titel(), satz()))))
V.append(('Das Foto kippt', 'Titel links riesig, rechts ein grosses Foto als Karte, die sich mit der Maus leicht neigt.',
          lambda n: kopf(n, '<div class="innen dh13-in"><div>%s%s</div><div class="dh13-karte" data-kipp>%s</div></div>' % (titel('', ('Was magst', 'du?')), satz('', 3), bild('glas-trinkt', '', '45vw')))))
V.append(('Vier Felder', 'Vier gleich grosse Felder über den Schirm: eines mit dem Titel, drei mit Fotos; alle richten sich beim Laden auf.',
          lambda n: kopf(n, '<div class="dh14-felder"><div class="dh14-t">%s%s</div>%s%s%s</div>' % (
              titel(), satz(), bild('schaum', '', '50vw'), bild('momo-giesst', '', '50vw', '62% 40%'), bild('glas-kerze', '', '50vw')))))
V.append(('Bilder ziehen unter dem Titel durch', 'Der Titel bleibt stehen, darunter ziehen beim Scrollen drei Fotos über die ganze Breite durch.',
          lambda n: kopf(n, '<div class="dh15-bilder">%s%s%s</div><div class="dh15-steht"><div class="innen">%s%s</div></div>' % (
              bild('anstossen', '', '100vw', '50% 40%'), bild('schaum', '', '100vw', None, False), bild('glas-zwei', '', '100vw', None, False), titel(), satz()))))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, nm] for j, (nm, _, _) in enumerate(V)]
KOPF = '<link rel="stylesheet" href="%s/hero.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, kopfhtml, name):
    h = basis[:a] + kopfhtml + basis[b:] if nr else basis
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/hero.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, '', 'Heute'))
    for j, (name, _, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
