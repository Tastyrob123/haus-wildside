# Walk on the Wild Side · Drinks, «Die einzige Karte»: der Kopf als Teil des Schachbretts (30.10.2026).
# Robert zur Kopf-Runde 1 (_varianten/karte-kopf): «dieser Abschnitt passt nicht zu dem Schachbrett-Konzept, das beisst sich viel zu sehr».
# Deshalb sitzt der Kopf hier in denselben Feldern: gleiches Raster, gleiche Fugen, Farben der echten Karte (Rosa, Rot) und Nacht.
# Wortlaut unverändert, nur in Sätze geteilt. 00 = heutiger Stand. Wechsel mit ← →.
import os, sys, json, html, time, re
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER); sys.path.insert(0, HIER)
import bau as BB
from bilder import mache
ORD = '_varianten/karte-kopf2'
VER = str(int(time.time()))
h0 = open('drinks.html').read()
A = h0.index('<div class="innen"><div class="ka-kopf">')
B0 = h0.index('<div class="ka-brett auf">', A)
B = B0 + len('<div class="ka-brett auf">')
alt = h0[A:B0]
KZ = re.search(r'<div class="kz sw".*?</div>', alt).group(0).replace('kz sw', 'kz')
KN = re.search(r'<a class="knopf rot".*?</a>', alt, re.S).group(0)
S1 = 'Einmal im Jahr gibt es doch eine Karte: zum Valentinstag, zusammen mit Rudi von Culinarium.'
S2 = '2026 hiess sie «Drunk in Love», vier Drinks zu je zwölf Euro, dazu Teller zum Teilen.'
S3 = 'Zum Weihnachtsfest 2023 standen Momos erste Signature Drinks auf einem Blatt: Linden Mule, Sakura, Mary Bramble, Ambré, Clean Pornstar, Zauberwald.'
assert ' '.join((S1, S2, S3)) in alt
E = html.escape
# Felder des Bretts (8 Stück) in der Reihenfolge der Seite
rest = h0[B:]
brett = rest[:rest.index('</div>\n<div class="innen"><small class="ka-klein">')]
F = ['<div class="ka-x"' + x for x in brett.split('<div class="ka-x"')[1:]]
assert len(F) == 8, len(F)
ENDE = B + len(brett)


def T(z=('Die einzige Karte.',), cls=''):
    return '<h2 class="titel %s"><span class="zl">%s</span></h2>' % (cls, ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i, E(x)) for i, x in enumerate(z)))


def feld(farbe, inhalt, d, span=1, cls=''):
    return '<div class="kb-k kb-%s kb-s%d %s" style="--d:%d">%s</div>' % (farbe, span, cls, d, inhalt)


def tx(s, cls='tx'):
    return '<p class="%s">%s</p>' % (cls, E(s))


def kn():
    return '<div class="knoepfe">%s</div>' % KN


KARTE = '<div class="kb-k kb-bild kb-s1" style="--d:0"><figure class="ka-f" style="--lq:url(%s)">%s</figure></div>' % (
    mache('karte-love')['lq'], BB.img_tag('karte-love', '(max-width:760px) 100vw, 25vw', extra=' style="object-position:50% 20%"'))
V = [('Heutiger Stand', None)]
V.append(('Die Kopfreihe', lambda: feld('nacht', KZ + T(cls='kb-g'), 0, 2) + feld('rosa', tx(S1 + ' ' + S2, 'lead') + tx(S3) + kn(), 1, 2) + ''.join(F)))
V.append(('Die echte Karte', lambda: KARTE + feld('nacht', KZ + T(cls='kb-g') + tx(S1 + ' ' + S2, 'tx kb-ab'), 1, 2) + feld('rosa', tx(S3) + kn(), 2) + ''.join(F)))
V.append(('Der Kopf in der Mitte', lambda: ''.join(F[:4]) + feld('nacht', '<div>%s%s</div><div>%s%s%s</div>' % (KZ, T(cls='kb-g'), tx(S1 + ' ' + S2, 'lead'), tx(S3), kn()), 2, 4, 'kb-band') + ''.join(F[4:])))
V.append(('Das rote Titelfeld', lambda: feld('rot', KZ + T(('Die einzige', 'Karte.'), 'kb-g'), 0, 2) + feld('nacht', tx(S1 + ' ' + S2, 'lead'), 1) + feld('rosa', tx(S3) + kn(), 2) + ''.join(F)))
V.append(('Vier Felder', lambda: feld('nacht', KZ + T(('Die einzige', 'Karte.'), 'kb-m'), 0) + feld('rosa', tx(S1 + ' ' + S2, 'lead kb-kl'), 1) + feld('nacht', tx(S3) + kn(), 2) + KARTE.replace('--d:0', '--d:3') + ''.join(F)))
V.append(('Das rosa Band', lambda: feld('rosa', '<div>%s%s</div><div>%s%s%s</div>' % (KZ, T(cls='kb-g'), tx(S1 + ' ' + S2, 'lead'), tx(S3), kn()), 0, 4, 'kb-band') + ''.join(F)))
V.append(('Drei und eins', lambda: feld('nacht', '<div>%s%s</div><div>%s%s%s</div>' % (KZ, T(cls='kb-g'), tx(S1 + ' ' + S2, 'lead'), tx(S3), kn()), 0, 3, 'kb-band') + KARTE.replace('--d:0', '--d:1') + ''.join(F)))
V.append(('Gespiegelt', lambda: feld('rosa', tx(S1 + ' ' + S2, 'lead') + tx(S3) + kn(), 0, 2) + feld('nacht', KZ + T(('Die einzige', 'Karte.'), 'kb-g'), 1, 2, 'kb-rechts') + ''.join(F)))

for n, (name, f) in enumerate(V):
    if f:
        h = h0[:A] + '<div class="ka-brett kb kb%02d auf">' % n + f() + h0[ENDE:]
    else:
        h = h0
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V) - 1, E(name))
    liste = [[j, x[0]] for j, x in enumerate(V)]
    h = h.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script></body>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER), 1)
    open(os.path.join(ORD, '%02d.html' % n), 'w').write(h)
print(len(V) - 1)
