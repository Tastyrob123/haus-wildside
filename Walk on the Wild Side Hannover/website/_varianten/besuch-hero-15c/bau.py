# Walk on the Wild Side · Unterseite Besuch: 15 Fassungen für den Kopf «Bis 2 Uhr.», Runde 3 (31.10.2026).
# Runde 1: «alle mist. die müssen außergewöhnlicher sein». Runde 2: «die animationen sind müll. Diese ausgeschnittenen einzel elemente
# sehen immer scheiße aus. Und die anderen sachen einfach zu leer und unspektakulär».
# Darum hier: jeder Kopf voll mit ganzen, echten Fotos der Bar, Kante an Kante (wie Plakatwand und Mosaik, beide abgenommen).
# Kein Freisteller, kein Requisit, keine Kreise, kein Drehen/Flackern. Die Bewegung ist eine Kamerafahrt, die auf drei Vierteln langsam wird;
# der Text steht auf einem breiten dunklen Band und kommt synchron. Nur transform/opacity. Wechsel mit ← →. 00 = heute.
# Aufruf: python3 _varianten/besuch-hero-15c/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, mache, zl, HAUS, V as BV

ORD = '_varianten/besuch-hero-15c'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('hero.css', 'hero.js', 'varianten-nav.js', 'varianten-nav.css', 'bau.py'))))
basis = open('besuch.html').read()
a = basis.index('<header class="sk auf" id="auftakt">')
b = basis.index('</header>', a) + len('</header>')

SATZ = 'Haasemannstraße 13, Ecke Rampenstraße, Linden-Mitte. Donnerstag bis Samstag ab 19 Uhr.'
assert HAUS['adresse'] == 'Haasemannstraße 13'
EXTRA_ALT = {'fb-fenster-aussen': 'Die Fenster der Bar von aussen am Abend'}


def daten(k):
    try:
        return mache(k)
    except KeyError:
        d = json.load(open('assets/bild/%s.json' % k))
        d['alt'] = EXTRA_ALT[k]
        return d


def bild(k, cls='', sizes='100vw', pos=None, sofort=True, stil='', deko=False):
    d = daten(k)
    ss = ', '.join('assets/bild/%s?v=%s %dw' % (f, BV, w) for w, f in d['stufen'])
    st = ' style="object-position:%s"' % pos if pos else ''
    lade = ' fetchpriority="high"' if sofort else ' loading="lazy"'
    alt = '' if deko else E(d['alt'])
    return '<figure class="by-f %s" style="--lq:url(%s);%s"><img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s%s></figure>' % (
        cls, d['lq'], stil, d['stufen'][-1][1], BV, ss, sizes, alt, d['w'], d['h'], lade, st)


def titel(cls='', zeilen=('Bis 2 Uhr.',), i0=1):
    return '<h1 class="titel by-t %s">%s</h1>' % (cls, zl(list(zeilen), i0=i0))


def satz(cls='', i=3):
    return '<p class="text sw by-s %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def band(cls=''):
    """Das breite dunkle Band über allen Bildern (wie «Lauter.» auf der Plakatwand)."""
    return '<div class="by-band %s"><div class="innen">%s%s</div></div>' % (cls, titel(), satz())


def kopf(n, inner, cls=''):
    return '<header class="sk-v auf by by%02d %s" id="auftakt" data-v="%d">%s</header>' % (n, cls, n, inner)


def wand(fotos, cls, sizes, extra=lambda j: ''):
    return '<div class="%s">%s</div>' % (cls, ''.join(bild(k, 'w%d' % j, sizes, p, j < 6, '--j:%d;%s' % (j, extra(j))) for j, (k, p) in enumerate(fotos)))


V = []

# 01 Die Wand steigt
TIEFE = [34, 58, 22, 48, 30]
V.append(('Die Wand steigt', 'Fünf hohe Fotos vom Abend Kante an Kante; beim Öffnen steigen sie aus verschiedenen Tiefen hoch und schliessen sich zur Wand, das Band mit dem Titel kommt mit.',
          lambda n: kopf(n, wand([('decke-hoch', '50% 40%'), ('freundinnen', '50% 40%'), ('fe-theke', '50% 50%'), ('saengerin-kunde', '50% 35%'), ('feste-anstossen', '50% 45%')],
                                 'by01-wand', '21vw', lambda j: '--y:%d%%' % TIEFE[j]) + band())))

# 02 Rückfahrt aus dem Gewölbe
V.append(('Rückfahrt aus dem Gewölbe', 'Man steht mitten unter der Decke; die Kamera fährt zurück, und ringsum erscheinen vier weitere Bilder vom Abend.',
          lambda n: kopf(n, '<div class="by02-wand">%s%s%s%s%s</div>%s' % (
              bild('fw-h18', 'a', '30vw', '50% 40%'), bild('voll', 'b', '30vw', '50% 50%'), bild('decke-raum', 'm', '100vw', '50% 45%'),
              bild('fw-a31', 'c', '30vw', '50% 50%'), bild('fw-h7', 'd', '30vw', '50% 35%'), band()))))

# 03 Kopf in den Nacken
V.append(('Kopf in den Nacken', 'Ein Foto über die ganze Breite; beim Scrollen schwenkt die Kamera vom Tresen hinauf in die bedruckte Gewölbe-Decke.',
          lambda n: kopf(n, '<div class="by-buehne"><div class="by03-hoch">%s</div>%s</div>' % (bild('decke-raum', '', '100vw', '50% 50%'), band()))))

# 04 Die Bühne
V.append(('Die Bühne', 'Ein Konzertabend über den ganzen Schirm; die Kamera fährt zurück und wird zum Ende hin langsam, der Titel steigt mit.',
          lambda n: kopf(n, '<div class="by04-fahrt">%s</div>%s' % (bild('konzert-scharf', 'by-voll', '100vw', '50% 45%'), band()))))

# 05 Das Licht geht an
V.append(('Das Licht geht an', 'Sechs Fotos als Wand im Halbdunkel; eins nach dem anderen geht das Licht an, wie das Schild an der Ecke um 19 Uhr.',
          lambda n: kopf(n, wand([('fenster', '50% 55%'), ('wf-raum', '50% 45%'), ('fw-h33', '50% 50%'), ('fe-negroni', '50% 40%'), ('saengerin', '50% 35%'), ('fw-h16', '50% 50%')],
                                 'by05-wand', '34vw', lambda j: '--d:%.2fs' % (.5 + [3, 0, 5, 1, 4, 2][j] * .38)) + band('mitte'))))

# 06 Der grosse Titel
V.append(('Der grosse Titel', 'Oben der Raum am Abend über die ganze Breite, darunter der Titel so gross, dass er die ganze Seite füllt.',
          lambda n: kopf(n, '<div class="by06-bild">%s</div><div class="by06-unten"><h1 class="titel by06-t">%s</h1>%s</div>' % (
              bild('ft-raum-abend', 'by-voll', '100vw', '50% 45%'), zl(['Bis 2 Uhr.'], i0=1), satz('', 3)))))

# 07 Die Lamellen
def h07(n):
    # Ein Bild, zehn Streifen: als Hintergrund (eine dekodierte Datei), nicht zehnmal <img> (das brachte die Safari-Engine zum Absturz)
    d = daten('ft-runde-stoesst-an')
    datei = next(f for w, f in d['stufen'] if w >= 2000)
    st = ''.join('<i class="by07-st" style="--k:%d;--y:%d%%"></i>' % (k, [62, 40, 78, 30, 55, 85, 36, 70, 46, 60][k]) for k in range(10))
    return kopf(n, '<div class="by07-bild" role="img" aria-label="%s" style="--bild:url(../../assets/bild/%s?v=%s)">%s</div>%s' % (E(d['alt']), datei, BV, st, band()))
V.append(('Die Lamellen', 'Ein Foto vom Anstossen, in zehn senkrechte Streifen geteilt; sie steigen in einer Welle hoch und schliessen sich zum ganzen Bild.', h07))

# 08 Draussen und drinnen
V.append(('Draussen und drinnen', 'Links die Tür von der Strasse, rechts der volle Raum, Kante an Kante; links kommt von oben, rechts von unten, sie treffen sich in der Mitte.',
          lambda n: kopf(n, '<div class="by08-zwei">%s%s</div>%s' % (bild('tuer-rot', 'l', '50vw', '50% 55%'), bild('voll', 'r', '50vw', '50% 50%'), band('mitte')))))

# 09 Der Abend vergeht
V.append(('Der Abend vergeht', 'Beim Scrollen geht der Abend weiter: vom leeren Raum über die Theke und Momo bis zum Anstossen, jedes Bild mit eigener Fahrt.',
          lambda n: kopf(n, '<div class="by-buehne">%s%s</div>' % (''.join(bild(k, 'by-voll by09-f' + (' an' if j == 0 else ''), '100vw', p, j < 2, '--j:%d' % j) for j, (k, p) in enumerate(
              [('ft-raum-abend', '50% 45%'), ('ft-theke-gaeste', '50% 45%'), ('ft-momo-mixt-gast', '50% 40%'), ('ft-runde-stoesst-an', '50% 45%')])), band()))))

# 10 Durchs Fenster hinein
V.append(('Durchs Fenster hinein', 'Die Fenster der Bar von aussen; beim Scrollen fährt die Kamera durch die Scheibe, bis man drinnen steht.',
          lambda n: kopf(n, '<div class="by-buehne"><div class="by10-innen">%s</div><div class="by10-aussen">%s</div>%s</div>' % (
              bild('ft-raum-abend', 'by-voll', '100vw', '50% 45%'), bild('fb-fenster-aussen', 'by-voll', '100vw', '50% 50%'), band()))))

# 11 Die Tafel über drei Bildern
V.append(('Die Tafel über drei Bildern', 'Momo, Derya und die Theke als drei Bilder Wand an Wand; quer über alle drei steigt eine breite Tafel mit dem Titel hoch.',
          lambda n: kopf(n, wand([('ft-momo-mixt-gast', '38% 40%'), ('derya', '45% 40%'), ('ft-theke-gaeste', '30% 45%')], 'by11-drei', '34vw') +
                         '<div class="by11-tafel"><div>%s%s</div></div>' % (titel(), satz()))))

# 12 Hochfahrt
V.append(('Hochfahrt', 'Ein hohes Foto von Momo am Tresen; beim Öffnen fährt die Kamera vom Shaker hinauf bis zu Momo und wird oben langsam.',
          lambda n: kopf(n, '<div class="by12-hoch">%s</div>%s' % (bild('dg-shaker', '', '100vw', '50% 50%'), band()))))

# 13 Das Mosaik der Nacht
V.append(('Das Mosaik der Nacht', 'Sieben Fotos in verschiedenen Grössen als dichte Wand; sie kommen aus der Tiefe, von der Mitte nach aussen, und schliessen sich.',
          lambda n: kopf(n, wand([('dg-coupes', '50% 50%'), ('fw-h19', '50% 50%'), ('dg-abseihen', '50% 40%'), ('fw-a31', '50% 50%'), ('ft-theke-gaeste', '45% 45%'), ('fe-highball', '50% 50%'), ('fw-highballs', '50% 50%')],
                                  'by13-wand', '30vw') + band())))

# 14 Säulen beim Scrollen
SP = [[('freundinnen', '50% 40%'), ('decke-hoch', '50% 40%'), ('fw-h18', '50% 40%')], [('voll', '50% 50%'), ('saengerin-kunde', '50% 35%'), ('dg-coupes', '50% 50%')],
      [('fe-theke', '50% 50%'), ('fw-h7', '50% 35%'), ('tuer-rot', '50% 55%')], [('feste-anstossen', '50% 45%'), ('wf-raum', '50% 45%'), ('fw-highballs', '50% 50%')]]
V.append(('Säulen beim Scrollen', 'Vier Säulen aus je drei Fotos, Kante an Kante; beim Scrollen gleiten sie unterschiedlich schnell nach oben, das Band bleibt stehen.',
          lambda n: kopf(n, '<div class="by14-saeulen">%s</div>%s' % (''.join('<div class="by14-s" data-t="%.2f">%s</div>' % (t, ''.join(bild(k, '', '25vw', p, i < 2) for i, (k, p) in enumerate(s)))
                                                                          for s, t in zip(SP, [.18, .42, .28, .55])), band('mitte')))))

# 15 Hineinfahrt in die Wand
V.append(('Hineinfahrt in die Wand', 'Eine Wand aus fünf Bildern; beim Scrollen fährt die Kamera in das mittlere hinein, bis es den ganzen Schirm füllt.',
          lambda n: kopf(n, '<div class="by-buehne"><div class="by02-wand by15-wand">%s%s%s%s%s</div>%s</div>' % (
              bild('dg-giessen', 'a', '30vw', '50% 50%'), bild('fw-h31', 'b', '30vw', '50% 30%'), bild('fw-highballs', 'm', '100vw', '50% 50%'),
              bild('dg-siphon', 'c', '30vw', '50% 50%'), bild('dg-flaschen', 'd', '30vw', '50% 50%'), band()))))

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
