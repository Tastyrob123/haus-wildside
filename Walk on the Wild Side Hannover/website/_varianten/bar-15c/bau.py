# Walk on the Wild Side · Abschnitt «Eure Nachbarschafts-Mixology-Bar» (id="bar"), dritte Runde mit 15 Fassungen (31.10.2026).
# Wunsch der Bar (Web Side.pdf, Seite 5): «layout eventuell etwas cleaner, zu viele Bilder». Die schnelle Lösung mit zwei schmalen
# Bildstreifen links und rechts lehnte Robert ab («das sieht kacke aus»). Also: wenige, grosse Bilder, das Schild mit Goldlinie,
# Titel, Satz und «Wer, Wo, Wann» in Gold bleiben; je Fassung ein eigener Aufbau und eine eigene Bewegung, nur transform.
# Wechsel mit ← → (varianten-nav.js). Aufruf: python3 _varianten/bar-15c/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, LOGO, HAUS, kz, mache, img_tag

ORD = '_varianten/bar-15c'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('wand.css', 'wand.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('index.html').read()
a = basis.index('<section class="kap auf bar-wand" id="bar">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]

T = ['Eure Nachbarschafts-', 'Mixology-Bar.']
SATZ = ('So nennt sich das Wild Side selbst, und so ist es gemeint: eine kleine Bar an der Ecke, in der man sich kennt, mit Drinks, für die man sonst weit fahren müsste. '
        'Seit November 2023 mit Derya und Momo hinter der Theke. Im Falstaff Bar Guide 2027 mit 91 Punkten.')
FAKTEN = [('Wer', 'Derya Ivkin führt die Bar, Momo Ben Khelifa mixt'), ('Wo', HAUS['adresse'] + ', ' + HAUS['ecke']),
          ('Wann', HAUS['zeit_kurz'].replace(' · ', '<br>'))]
KZ = kz('19:30', 'An der Ecke', 0)
UEBER = '<p class="ueber sw" style="--i:0">Und dann fragt Momo.</p>'
LINIE = '<svg class="es-linie" aria-hidden="true"><rect x="9" y="9" rx="9" ry="9" pathLength="100"/></svg>'


def k(key, cls='', sizes='50vw', pos='50% 50%', stil=''):
    return '<figure class="kachel b3-k %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(key)['lq'], stil, img_tag(key, sizes, extra=' style="object-position:%s"' % pos))


def titel(cls=''):
    return '<h2 class="titel b3-t %s">%s</h2>' % (cls, bau.zl(T, i0=1))


def satz(cls=''):
    return '<p class="text b3-s %s">%s</p>' % (cls, E(SATZ))


def fakten(cls=''):
    return '<div class="es-fakten b3-f %s">%s</div>' % (cls, ''.join('<div><b>%s</b><p>%s</p></div>' % (E(x), y) for x, y in FAKTEN))


def logo():
    return '<span class="logo b3-logo">%s</span>' % LOGO


def schild(cls='', innen=None, stil=''):
    """Das Eckschild wie heute: Nacht, Goldlinie, die sich beim Auftritt einmal herumzieht."""
    return '<div class="b3-schild %s" style="%s">%s%s</div>' % (cls, stil, LINIE, innen if innen is not None else logo() + titel() + satz() + fakten())


def kap(n, inner, voll=False):
    return '<section class="kap auf b3 v%02d" id="bar" data-v="%d">%s</section>' % (
        n, n, inner if voll else '<div class="innen">%s</div>' % inner)


V = []

# 01 Halb und halb: links ein grosses Querbild (Momo mixt, daneben ein Gast), rechts das Schild gleich hoch; das Foto zieht sich im Rahmen zusammen
V.append(('Halb und halb', lambda n: kap(n, KZ + '<div class="v01-g">%s%s</div>%s' % (
    k('ft-momo-mixt-gast', 'v01-b', '(max-width:900px) 92vw, 50vw', '45% 40%'), schild('v01-s'), UEBER))))

# 02 Fenster über dem Schild: ein breites Bild vom Raum am Abend über die ganze Breite, darunter das Schild quer; das Bild senkt sich von oben an seinen Platz
V.append(('Fenster über dem Schild', lambda n: kap(n, KZ + '<div class="v02-g">%s%s</div>%s' % (
    k('ft-raum-abend', 'v02-b', '92vw', '50% 55%'),
    schild('v02-s', logo() + '<div class="v02-q">%s<div>%s%s</div></div>' % (titel(), satz(), fakten())), UEBER))))

# 03 Nur Schrift: kein Foto, das Schild trägt die ganze Breite, Titel gross, «Wer, Wo, Wann» als grosse goldene Wörter; die Goldlinie zieht sich langsam
V.append(('Nur Schrift', lambda n: kap(n, KZ + schild('v03-s', logo() + titel('v03-t') + satz('v03-x') + fakten('v03-f')) + UEBER)))

# 04 Schild und zwei Bilder: links das Schild breit, rechts zwei Querbilder übereinander, zusammen genau so hoch; die Bilder kommen nacheinander aus der Tiefe
V.append(('Schild und zwei Bilder', lambda n: kap(n, KZ + '<div class="v04-g">%s<div class="v04-r">%s%s</div></div>%s' % (
    schild('v04-s'), k('ft-momo-mixt-gast', 'v04-b', '(max-width:900px) 92vw, 38vw', '45% 40%', '--n:0'),
    k('ft-runde-stoesst-an', 'v04-b', '(max-width:900px) 92vw, 38vw', '50% 40%', '--n:1'), UEBER))))

# 05 Drei Tafeln: Bild, Schild, Bild in drei gleich breiten Feldern; die beiden Bilder klappen von der Seite her auf wie Flügel eines Altars
V.append(('Drei Tafeln', lambda n: kap(n, KZ + '<div class="v05-g">%s%s%s</div>%s' % (
    k('anstossen', 'v05-b v05-l', '(max-width:900px) 92vw, 32vw'), schild('v05-s'), k('freundinnen', 'v05-b v05-r', '(max-width:900px) 92vw, 32vw'), UEBER))))

# 06 Das Bild läuft mit: rechts ein hohes Foto von Momo unter dem NEGRONI-Schriftzug, links das Schild; beim Scrollen gleitet das Foto ruhig in seinem Rahmen
V.append(('Das Bild läuft mit', lambda n: kap(n, KZ + '<div class="v06-g">%s%s</div>%s' % (
    schild('v06-s'), k('wf-raum', 'v06-b', '(max-width:900px) 92vw, 42vw', '50% 50%'), UEBER))))

# 07 Panorama: der leere Raum am frühen Abend als breites Band von Rand zu Rand, das sich beim Scrollen langsam heranzieht; darunter das Schild quer
V.append(('Panorama', lambda n: kap(n, '<div class="innen">%s</div>%s<div class="innen">%s%s</div>' % (
    KZ, k('pf-raum', 'v07-b', '100vw', '50% 60%'),
    schild('v07-s', logo() + '<div class="v07-q">%s<div>%s%s</div></div>' % (titel(), satz(), fakten())), UEBER), voll=True)))

# 08 Das Bild steht auf: das Schild links breit, rechts ein hohes Bild vom vollen Abend; das Bild liegt erst nach hinten gekippt und richtet sich auf
V.append(('Das Bild steht auf', lambda n: kap(n, KZ + '<div class="v08-g">%s%s</div>%s' % (
    schild('v08-s'), k('voll', 'v08-b', '(max-width:900px) 92vw, 36vw', '50% 55%'), UEBER))))

# 09 Schild und Reihe: das Schild quer oben, darunter drei gleich grosse Querbilder vom Abend, die nacheinander hochschweben
V.append(('Schild und Reihe', lambda n: kap(n, KZ + schild('v09-s', logo() + '<div class="v09-q">%s<div>%s%s</div></div>' % (titel(), satz(), fakten())) +
    '<div class="v09-r">%s%s%s</div>%s' % (k('ft-raum-abend', 'v09-b', '(max-width:900px) 92vw, 30vw', '50% 50%', '--n:0'),
                                          k('ft-momo-mixt-gast', 'v09-b', '(max-width:900px) 92vw, 30vw', '45% 40%', '--n:1'),
                                          k('ft-runde-stoesst-an', 'v09-b', '(max-width:900px) 92vw, 30vw', '50% 40%', '--n:2'), UEBER))))

# 10 Grosser Titel: der Titel über die ganze Breite in Hero-Grösse, darunter links ein Querbild, rechts Satz und «Wer, Wo, Wann» auf dem Schild
V.append(('Grosser Titel', lambda n: kap(n, KZ + '<div class="v10-kopf">%s%s</div><div class="v10-g">%s%s</div>%s' % (
    logo(), titel('v10-t'), k('ft-raum-abend', 'v10-b', '(max-width:900px) 92vw, 50vw', '50% 50%'), schild('v10-s', satz() + fakten('v10-f')), UEBER))))

# 11 Wer, Wo, Wann in Bildern: oben das Schild mit Titel und Satz, darunter drei Karten, jede mit ihrem Foto (Momo, die Ecke, der Raum); sie federn nacheinander ein
def v11(n):
    bilder = [('wf-raum', '50% 35%'), ('pf-schild', '50% 50%'), ('pf-raum', '50% 60%')]
    karten = ''.join('<div class="v11-karte" style="--n:%d">%s<div class="v11-u"><b>%s</b><p>%s</p></div></div>' % (
        j, k(kk, 'v11-b', '(max-width:900px) 92vw, 30vw', p), E(x), y) for j, ((kk, p), (x, y)) in enumerate(zip(bilder, FAKTEN)))
    return kap(n, KZ + schild('v11-s', logo() + '<div class="v11-q">%s%s</div>' % (titel(), satz())) + '<div class="v11-r">%s</div>%s' % (karten, UEBER))
V.append(('Wer, Wo, Wann in Bildern', v11))

# 12 Die Ecke und das Schild: links das beleuchtete Schild an der Hausecke als hohes Foto, rechts das Schild der Seite; das Foto dreht sich wie ein Abzug gerade
V.append(('Die Ecke und das Schild', lambda n: kap(n, KZ + '<div class="v12-g">%s%s</div>%s' % (
    k('schild', 'v12-b', '(max-width:900px) 92vw, 40vw', '50% 45%'), schild('v12-s'), UEBER))))

# 13 Das Bild bleibt stehen: links ein hohes Foto, das stehen bleibt, während rechts Titel, Satz und «Wer, Wo, Wann» nacheinander vorbeiziehen
V.append(('Das Bild bleibt stehen', lambda n: kap(n, KZ + '<div class="v13-g"><div class="v13-l">%s</div><div class="v13-r">%s%s%s</div></div>%s' % (
    k('decke-raum', 'v13-b', '(max-width:900px) 92vw, 44vw', '50% 40%'),
    schild('v13-s v13-s1', logo() + titel()), schild('v13-s v13-s2', satz()), schild('v13-s v13-s3', fakten()), UEBER))))

# 14 In Creme: das Schild hell wie das Papier der Bar, rechts daneben ein grosses Querbild; das Schild hebt sich beim Auftritt aus der Fläche
V.append(('In Creme', lambda n: kap(n, KZ + '<div class="v14-g">%s%s</div>%s' % (
    schild('v14-s'), k('ft-momo-mixt-gast', 'v14-b', '(max-width:900px) 92vw, 46vw', '45% 40%'), UEBER))))

# 15 Das Logo vorne: das rote Logo gross links wie das Schild an der Hauswand, rechts Titel, Satz und Fakten; darunter ein breites Bild, das sich heranzoomt
V.append(('Das Logo vorne', lambda n: kap(n, KZ + schild('v15-s', '<div class="v15-g"><span class="logo v15-logo">%s</span><div>%s%s%s</div></div>' % (LOGO, titel(), satz(), fakten())) +
    k('ft-runde-stoesst-an', 'v15-b', '92vw', '50% 40%') + UEBER)))

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
