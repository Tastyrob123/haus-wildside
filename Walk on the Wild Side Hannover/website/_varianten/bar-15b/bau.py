# Walk on the Wild Side · Abschnitt «Eure Nachbarschafts-Mixology-Bar» (id="bar"), zweite Runde mit 15 Fassungen (29.10.2026).
# Robert: «ich finds wie es jetzt ist cool mit den Bildern und so, aber das muss trotzdem nochmal anders gedacht werden.»
# Also: Zutaten bleiben wie heute (cremefarbenes Plakat mit Logo, dichte Bildwand aus den echten Fotos, Kacheln mit Tiefe),
# je Fassung ein eigener Gedanke für den Aufbau und eine eigene Bewegung. Auftritte nur mit transform, alles von Anfang an deckend.
# Wechsel mit ← → (varianten-nav.js). Aufruf: python3 _varianten/bar-15b/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, LOGO, HAUS, kz, mache, img_tag

ORD = '_varianten/bar-15b'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('wand.css', 'wand.js', 'varianten-nav.js', 'varianten-nav.css'))))
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
POS = {'theke': '50% 70%', 'derya': '35% 50%'}


def k(key, cls='', sizes='25vw', stil=''):
    """Eine Kachel wie heute (Tiefe, Zoom des Fotos beim Auftritt), ohne das Anheben beim Darüberfahren, damit die Fassung die Kachel selbst bewegen kann."""
    pos = POS.get(key)
    extra = ' style="object-position:%s"' % pos if pos else ''
    return '<figure class="kachel %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(key)['lq'], stil, img_tag(key, sizes, extra=extra))


def titel(cls=''):
    return '<h2 class="titel %s">%s</h2>' % (cls, bau.zl(T, i0=1))


def text(cls=''):
    return '<p class="text sw %s" style="--i:3">%s</p>' % (cls, E(SATZ))


def fakten(cls=''):
    return '<div class="fakten sw %s" style="--i:4">%s</div>' % (cls, ''.join('<div><span class="etikett">%s</span>%s</div>' % (E(x), y) for x, y in FAKTEN))


def logo():
    return '<span class="logo">%s</span>' % LOGO


def plakat(cls='', innen=None, stil=''):
    return '<div class="plakat %s" style="%s">%s</div>' % (cls, stil, innen if innen is not None else logo() + titel() + text() + fakten())


def quer():
    """Inhalt für ein breites Plakat: Titel über die ganze Breite, darunter Satz und Fakten nebeneinander."""
    return logo() + titel('t-plakat') + '<div class="q-unten">%s%s</div>' % (text(), fakten())


def kap(n, inner, extra='', voll=False):
    wand = inner if voll else '<div class="innen">%s</div>' % inner
    return '<section class="kap auf b2 w%02d %s" id="bar" data-v="%d">%s</section>' % (n, extra, n, wand)


V = []

# 01 Das Plakat quer: das Plakat liegt breit über drei Felder, Titel gross; darunter hebt sich die Bildreihe als ein Block
def w01(n):
    inn = quer()
    return kap(n, KZ + '<div class="w01-wand">%s%s<div class="w01-reihe">%s</div></div>%s' % (
        plakat('w01-p', inn), k('fenster', 'w01-f'), ''.join(k(x) for x in ['anstossen', 'negroni', 'freundinnen', 'flaschen']), UEBER))
V.append(('Das Plakat quer', w01))

# 02 Die Ecke: oben eine Bildreihe, rechts eine Bildspalte, das Plakat sitzt in der Ecke dazwischen; die Reihe kommt von oben, die Spalte von unten
def w02(n):
    oben = ''.join(k(x, 'w02-o', stil='--n:%d' % j) for j, x in enumerate(['fenster', 'negroni', 'theke', 'flaschen']))
    return kap(n, KZ + '<div class="w02-wand">%s%s%s%s</div>%s' % (oben, plakat('w02-p', quer()), k('anstossen', 'w02-r w02-r1'), k('freundinnen', 'w02-r w02-r2'), UEBER))
V.append(('Die Ecke', w02))

# 03 Die Wand lebt: Aufbau genau wie heute, aber die Kacheln wechseln ruhig nacheinander ihr Foto, jedes schiebt sich von unten herein
POOL = ['schild-ecke', 'momo-lacht', 'glas-rot', 'rueckbar', 'tuer-rot', 'voll', 'glas-coupe', 'saengerin', 'glas-kerze', 'schaum', 'glas-hand', 'decke-bar']
def w03(n):
    h = HEUTE.replace('class="kap auf" id="bar"', 'class="kap auf b2 w03" id="bar" data-v="3"', 1).replace('kachel leise', 'kachel')
    pool = []
    for key in POOL:
        d = mache(key)
        pool.append({'s': ', '.join('assets/bild/%s?v=%s %dw' % (f, bau.V, w) for w, f in d['stufen']), 'a': d['alt'], 'w': d['w'], 'h': d['h']})
    return h.replace('<div class="mosaik flaeche">', '<div class="mosaik flaeche" data-pool="%s">' % E(json.dumps(pool, ensure_ascii=False)), 1)
V.append(('Die Wand lebt', w03))

# 04 Randlos: die Bildwand geht von Rand zu Rand über die ganze Breite, das Plakat sitzt breit in der Mitte; die ganze Wand setzt sich beim Auftritt
def w04(n):
    r1 = ['fenster', 'glas-rot', 'negroni', 'schild-ecke', 'glas-coupe', 'flaschen']
    r3 = ['rueckbar', 'glas-kerze', 'theke', 'momo-lacht', 'schaum', 'tuer-rot']
    inn = quer()
    wand = ''.join(k(x, '', '17vw') for x in r1) + k('anstossen', '', '17vw') + plakat('w04-p', inn) + k('freundinnen', '', '17vw') + ''.join(k(x, '', '17vw') for x in r3)
    return kap(n, '<div class="innen">%s</div><div class="w04-wand">%s</div><div class="innen">%s</div>' % (KZ, wand, UEBER), voll=True)
V.append(('Randlos', w04))

# 05 Aufgehängt: das Plakat hängt leicht schräg an der Bildwand wie ein Flyer an der Bar und dreht sich beim Auftritt an seinen Platz
def w05(n):
    return kap(n, KZ + '<div class="w05-wand">%s%s%s%s%s%s%s</div>%s' % (
        plakat('w05-p'), k('theke', 'w05-a'), k('fenster', 'w05-b'), k('negroni', 'w05-c'), k('anstossen', 'w05-d'), k('freundinnen', 'w05-e'), k('flaschen', 'w05-f'), UEBER))
V.append(('Aufgehängt', w05))

# 06 Aus dem Plakat heraus: das Plakat steht in der Mitte, die acht Bilder liegen zuerst dahinter und fahren von dort an ihren Platz
def w06(n):
    um = [('fenster', 'tl'), ('negroni', 'tm'), ('anstossen', 'tr'), ('theke', 'ml'), ('freundinnen', 'mr'), ('flaschen', 'bl'), ('glas-rot', 'bm'), ('schild-ecke', 'br')]
    return kap(n, KZ + '<div class="w06-wand">%s%s</div>%s' % (''.join(k(x, 'w06-k w06-' + p) for x, p in um), plakat('w06-p'), UEBER))
V.append(('Aus dem Plakat heraus', w06))

# 07 Das Regal: eine einzige hohe Reihe wie die Rückbar, das Plakat steht breit in der Mitte; jede Kachel kommt aus einer anderen Tiefe, alle kommen zugleich an
def w07(n):
    return kap(n, KZ + '<div class="w07-reihe">%s%s%s%s%s</div>%s' % (
        k('fenster', '', '18vw', '--d:150px'), k('negroni', '', '18vw', '--d:80px'), plakat('w07-p', stil='--d:30px'), k('anstossen', '', '18vw', '--d:80px'), k('flaschen', '', '18vw', '--d:150px'), UEBER))
V.append(('Das Regal', w07))

# 08 Plakat mit Foto: das Plakat trägt oben ein grosses Foto der Rückbar wie ein gedrucktes Plakat; links und rechts hohe Bilder
def w08(n):
    foto = '<figure class="kachel w08-foto" style="--lq:url(%s)">%s</figure>' % (mache('rueckbar-breit')['lq'], img_tag('rueckbar-breit', '40vw'))
    inn = foto + '<div class="w08-text">%s%s%s</div>' % (titel(), text(), fakten())
    return kap(n, KZ + '<div class="w08-wand">%s%s%s%s%s</div>%s' % (k('fenster', 'w08-a'), k('glas-rot', 'w08-b'), plakat('w08-p', inn), k('anstossen', 'w08-c'), k('negroni', 'w08-d'), UEBER))
V.append(('Plakat mit Foto', w08))

# 09 Die Kacheln stellen sich auf: ein grosses Bild links, das Plakat breit rechts oben, drei Bilder darunter; jede Kachel liegt erst zurück und richtet sich auf
def w09(n):
    return kap(n, KZ + '<div class="w09-wand">%s%s%s%s%s</div>%s' % (
        k('theke', 'w09-k w09-gross', '45vw'), plakat('w09-k w09-p', quer()),
        k('anstossen', 'w09-k'), k('negroni', 'w09-k'), k('freundinnen', 'w09-k'), UEBER))
V.append(('Die Kacheln stellen sich auf', w09))

# 10 Mit Tiefe: Plakat in der Mitte, Bilder links und rechts; fährt man mit der Maus darüber, liegen Plakat und Fotos auf verschiedenen Ebenen
def w10(n):
    return kap(n, KZ + '<div class="w10-wand">%s%s%s%s%s%s%s</div>%s' % (
        k('fenster', 'w10-t w10-a', '30vw', '--t:1'), plakat('w10-t w10-p', stil='--t:-.6'), k('anstossen', 'w10-t w10-b', '30vw', '--t:1.4'), k('negroni', 'w10-t w10-c', '30vw', '--t:.8'),
        k('theke', 'w10-t w10-d', '45vw', '--t:1.2'), k('freundinnen', 'w10-t w10-e', '30vw', '--t:.7'), k('flaschen', 'w10-t w10-f', '30vw', '--t:1.5'), UEBER))
V.append(('Mit Tiefe', w10))

# 11 Die Wand schliesst sich: beim Hinscrollen stehen die Kacheln versetzt, in der Mitte des Bildschirms schliessen sie sich zu einer Wand
def w11(n):
    teile = [('fenster', 'w11-1', '-90'), ('negroni', 'w11-2', '60'), ('anstossen', 'w11-3', '-40'), ('flaschen', 'w11-4', '110'),
             ('theke', 'w11-5', '80'), ('freundinnen', 'w11-6', '-70')]
    return kap(n, KZ + '<div class="w11-wand">%s%s</div>%s' % (''.join(k(x, 'w11-k ' + c, stil='--v:%s' % v) for x, c, v in teile), plakat('w11-k w11-p', stil='--v:-30'), UEBER))
V.append(('Die Wand schliesst sich', w11))

# 12 Das Eckschild: das Plakat in Nacht mit Goldlinie wie das Schild an der Hausecke, die Linie zieht sich beim Auftritt einmal um das Plakat
def w12(n):
    rahmen = '<svg class="w12-linie" aria-hidden="true"><rect x="9" y="9" rx="9" ry="9" pathLength="100"/></svg>'
    return kap(n, KZ + '<div class="w12-wand">%s%s%s%s%s%s%s</div>%s' % (
        plakat('w12-p', rahmen + logo() + titel() + text() + fakten()), k('schild-ecke', 'w12-a'), k('negroni', 'w12-b'), k('anstossen', 'w12-c'),
        k('fenster', 'w12-d'), k('freundinnen', 'w12-e'), k('theke', 'w12-f', '50vw'), UEBER))
V.append(('Das Eckschild', w12))

# 13 Unter der Decke: oben hängt eine Reihe Bilder wie Lampen und pendelt sich ein, darunter liegt das Plakat über die ganze Breite
def w13(n):
    inn = quer()
    return kap(n, KZ + '<div class="w13-reihe">%s</div>%s%s' % (''.join(k(x, 'w13-k', '20vw', '--n:%d' % j) for j, x in enumerate(['fenster', 'negroni', 'anstossen', 'freundinnen', 'flaschen'])),
                                                            plakat('w13-p', inn), UEBER))
V.append(('Unter der Decke', w13))

# 14 Das Plakat in Stücken: Titel, Satz und Wer, Wo, Wann sind eigene Kacheln zwischen den Fotos; alle Kacheln setzen sich zugleich
def w14(n):
    ft = ''.join('<div class="plakat w14-f w14-z"><span class="etikett">%s</span><p>%s</p></div>' % (E(x), y) for x, y in FAKTEN)
    return kap(n, KZ + '<div class="w14-wand">%s%s%s%s%s%s</div>%s' % (
        plakat('w14-t w14-z', logo() + titel()), k('theke', 'w14-a w14-z', '25vw'), k('negroni', 'w14-b w14-z'),
        plakat('w14-s w14-z', '<p class="text">%s</p>' % E(SATZ)), k('anstossen', 'w14-c w14-z'), ft + k('freundinnen', 'w14-d w14-z'), UEBER))
V.append(('Das Plakat in Stücken', w14))

# 15 Grosses Bild und Band: links ein grosses Foto, rechts das Plakat gleich gross, darunter ein Streifen kleiner Bilder, der von selbst langsam weiterläuft
def w15(n):
    band = ''.join(k(x, '', '14vw') for x in ['anstossen', 'negroni', 'freundinnen', 'flaschen', 'glas-rot', 'schild-ecke', 'glas-coupe', 'momo-lacht', 'glas-kerze', 'tuer-rot'])
    return kap(n, KZ + '<div class="w15-oben">%s%s</div><div class="w15-band"><div class="w15-spur">%s%s</div></div>%s' % (
        k('fenster', 'w15-gross', '50vw'), plakat('w15-p'), band, band, UEBER))
V.append(('Grosses Bild und Band', w15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/wand.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/wand.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
