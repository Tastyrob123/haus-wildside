# Walk on the Wild Side · Drinks, «Die einzige Karte»: Fassungen für den Kopf über dem Schachbrett (30.10.2026).
# Robert zum Bildschirmfoto des Kopfs: «den bereich … bitte nochmal anders anordnen / schöner geiler besser lesbar».
# Nur der Kopf ändert sich, das Schachbrett darunter bleibt. Wortlaut unverändert, nur in Sätze geteilt. 00 = heutiger Stand. Wechsel mit ← →.
import os, json, html, time, re
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ORD = '_varianten/karte-kopf'
VER = str(int(time.time()))
h0 = open(os.path.join(HIER, 'drinks.html')).read()
A = h0.index('<div class="innen"><div class="ka-kopf">'); B = h0.index('<div class="ka-brett', A)
alt = h0[A:B]
KZ = re.search(r'<div class="kz sw".*?</div>', alt).group(0)
KN = re.search(r'<a class="knopf rot".*?</a>', alt, re.S).group(0)
S1 = 'Einmal im Jahr gibt es doch eine Karte: zum Valentinstag, zusammen mit Rudi von Culinarium.'
S2 = '2026 hiess sie «Drunk in Love», vier Drinks zu je zwölf Euro, dazu Teller zum Teilen.'
S3 = 'Zum Weihnachtsfest 2023 standen Momos erste Signature Drinks auf einem Blatt: Linden Mule, Sakura, Mary Bramble, Ambré, Clean Pornstar, Zauberwald.'
assert ' '.join((S1, S2, S3)) in alt
E = html.escape


def T(zeilen=('Die einzige Karte.',), cls='t-kap'):
    return '<h2 class="titel %s"><span class="zl">%s</span></h2>' % (cls, ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i, E(z)) for i, z in enumerate(zeilen)))


def p(s, cls='tx', i=1):
    return '<p class="%s km" style="--i:%d">%s</p>' % (cls, i, E(s))


def kn(i=3):
    return '<div class="knoepfe km" style="--i:%d">%s</div>' % (i, KN)


def kopf(n, inhalt):
    return '<div class="innen"><div class="kh kh%02d">%s</div></div>\n' % (n, inhalt)


V = [('Heutiger Stand', None)]
V.append(('Mittig', lambda n: kopf(n, '<div class="kh-m">%s%s%s%s%s</div>' % (KZ, T(cls='kh-riesig'), p(S1 + ' ' + S2, 'lead', 1), p(S3, 'tx', 2), kn()))))
V.append(('Zwei Jahre', lambda n: kopf(n, '<div class="kh-l">%s%s%s%s</div><div class="kh-j"><div class="km" style="--i:2"><b>2026</b><i></i>%s</div><div class="km" style="--i:3"><b>2023</b><i></i>%s</div></div>' % (
    KZ, T(), p(S1, 'lead', 1), kn(4), '<p class="tx">%s</p>' % E(S2), '<p class="tx">%s</p>' % E(S3)))))
V.append(('Auf Rosa', lambda n: kopf(n, '<div class="kh-platte"><div>%s%s</div><div>%s%s%s</div></div>' % (KZ, T(cls='kh-gross'), p(S1 + ' ' + S2, 'lead', 1), p(S3, 'tx', 2), kn()))))
V.append(('Drei Spalten', lambda n: kopf(n, '%s%s<i class="kh-linie"></i><div class="kh-drei">%s%s<div class="km" style="--i:3"><p class="tx">%s</p>%s</div></div>' % (
    KZ, T(cls='kh-riesig'), p(S1, 'tx', 1), p(S2, 'tx', 2), E(S3), '<div class="knoepfe">%s</div>' % KN))))
V.append(('Der grosse Satz', lambda n: kopf(n, '%s%s%s<div class="kh-zwei">%s<div>%s%s</div></div>' % (
    KZ, T(), p(S1, 'satz', 1), p(S2, 'tx', 2), p(S3, 'tx', 3), kn(4)))))
V.append(('Die Goldlinie', lambda n: kopf(n, '<div class="kh-g"><div>%s%s</div><i class="kh-senk"></i><div>%s%s%s</div></div>' % (KZ, T(cls='kh-gross'), p(S1 + ' ' + S2, 'lead', 1), p(S3, 'tx', 2), kn()))))
V.append(('Gespiegelt', lambda n: kopf(n, '<div class="kh-sp"><div>%s%s%s</div><div class="kh-r">%s%s</div></div>' % (
    p(S1 + ' ' + S2, 'lead', 1), p(S3, 'tx', 2), kn(), KZ, T(('Die einzige', 'Karte.'), 'kh-riesig')))))
V.append(('Zwei Zeilen', lambda n: kopf(n, '<div class="kh-zz"><div>%s%s</div><div>%s%s%s</div></div>' % (KZ, T(('Die einzige', 'Karte.'), 'kh-riesig'), p(S1 + ' ' + S2, 'lead', 1), p(S3, 'tx', 2), kn()))))
V.append(('Die Leiste', lambda n: kopf(n, '<div class="kh-le"><div>%s%s</div>%s</div><div class="kh-zwei kh-strich">%s%s</div>' % (
    KZ, T(cls='kh-gross'), kn(1), p(S1 + ' ' + S2, 'tx', 2), p(S3, 'tx', 3)))))
V.append(('Auf Rot', lambda n: kopf(n, '<div class="kh-platte kh-rot"><div>%s%s</div><div>%s%s%s</div></div>' % (KZ, T(cls='kh-gross'), p(S1 + ' ' + S2, 'lead', 1), p(S3, 'tx', 2), kn()))))

for n, (name, f) in enumerate(V):
    h = h0 if not f else h0[:A] + f(n) + h0[B:]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V) - 1, E(name))
    liste = [[j, x[0]] for j, x in enumerate(V)]
    h = h.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script></body>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER), 1)
    open(os.path.join(HIER, ORD, '%02d.html' % n), 'w').write(h)
print(len(V) - 1)
