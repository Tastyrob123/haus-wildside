# Walk on the Wild Side · Seite «Besuch», Abschnitt «Wo · Die Ecke» (id="wo"), 15 Fassungen (31.10.2026).
# Inhalt bleibt wörtlich wie heute (Titel, Satz, fünf Zeilen, Knopf). Je Fassung eigener Aufbau und eigene Bewegung, nur transform.
# Das Bild «schild-ecke» steht schon im Kopf der Seite und wird hier nicht wiederholt.
# Wechsel mit ← → (varianten-nav.js). Aufruf: python3 _varianten/wo-15/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, LOGO, HAUS, kz, mache, img_tag, knopf, zl

ORD = '_varianten/wo-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('wand.css', 'wand.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('besuch.html').read()
a = basis.index('<section class="kap hell auf" id="wo">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]

KZ = kz('Wo', 'Die Ecke', 0)
SATZ = ('In Linden-Mitte, ein paar Schritte vom Küchengarten, gegenüber vom Restaurant 11A. Mit der Stadtbahn bis Am Küchengarten, '
        'dann zwei Minuten zu Fuss. Das Schild an der Ecke leuchtet.')
TEL = '<a href="tel:%s">%s</a><br><a href="tel:%s">%s</a>' % (HAUS['tel_href'], E(HAUS['telefon']), HAUS['tel2_href'], E(HAUS['telefon2']))
IG = '<a href="%s" rel="noopener">%s</a>' % (HAUS['instagram'], E(HAUS['ig_name']))
ZEILEN = [('Adresse', E(HAUS['adresse']) + ', ' + E(HAUS['ort'])), ('Ecke', 'Haasemannstraße, Ecke Rampenstraße'),
          ('Bahn', 'Stadtbahn bis Am Küchengarten, Linien 9 und 17'), ('Telefon', TEL), ('Instagram', IG)]
KARTE = 'https://www.openstreetmap.org/?mlat=52.37025&mlon=9.71339#map=18/52.37025/9.71339'


def titel(zeilen=('Haasemannstraße', '13.'), cls=''):
    return '<h2 class="titel w-t %s">%s</h2>' % (cls, zl(list(zeilen)))


def satz(cls=''):
    return '<p class="text w-s %s">%s</p>' % (cls, E(SATZ))


def zeilen(cls='', nur=None):
    z = [x for x in ZEILEN if nur is None or x[0] in nur]
    return '<div class="zeilen w-z %s">%s</div>' % (cls, ''.join('<div style="--n:%d"><span class="etikett">%s</span><span>%s</span></div>' % (j, E(x), y) for j, (x, y) in enumerate(z)))


def karte(cls='hellk'):
    return '<div class="knoepfe w-k">%s</div>' % knopf('Auf der Karte', KARTE, cls)


def k(key, cls='', sizes='50vw', pos='50% 50%', stil=''):
    return '<figure class="kachel w-b %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(key)['lq'], stil, img_tag(key, sizes, extra=' style="object-position:%s"' % pos))


def kap(n, inner, cls='hell', voll=False):
    return '<section class="kap %s auf wo15 v%02d" id="wo" data-v="%d">%s</section>' % (
        cls, n, n, inner if voll else '<div class="innen">%s</div>' % inner)


def txt(inner, cls=''):
    return '<div class="w-txt %s">%s</div>' % (cls, inner)


M = '(max-width:900px) 92vw, '
V = []

# 01 Das Schild im Hochformat: links das beleuchtete Schild an der Hausecke, gleich hoch wie der Text; das Foto zieht sich im Rahmen langsam zusammen
V.append(('Das Schild im Hochformat', lambda n: kap(n, '<div class="v01-g">%s%s</div>' % (
    k('schild', 'v01-b', M + '40vw', '50% 40%'), txt(KZ + titel() + satz() + zeilen() + karte())))))

# 02 Die Dreizehn: die Hausnummer riesig aus dem Schlitz, darunter die Strasse; rechts die Terrasse und die Zeilen
V.append(('Die Dreizehn', lambda n: kap(n, '<div class="v02-g">%s%s</div>' % (
    txt(KZ + '<p class="titel v02-13">%s</p>' % zl(['13']) + titel(['Haasemannstraße.'], 'v02-t') + satz()),
    '<div class="v02-r">%s%s%s</div>' % (k('terrasse', 'v02-b', M + '44vw', '50% 55%'), zeilen(), karte())))))

# 03 Der Weg in drei Bildern: Am Küchengarten, zwei Minuten zu Fuss, das Schild; eine Goldlinie zieht sich durch, die Bilder federn nacheinander hoch
def v03(n):
    halte = [('uw-bank', '50% 45%', 'Am Küchengarten', 'Stadtbahn, Linien 9 und 17'),
             ('pf-schild', '42% 50%', 'Zwei Minuten', 'zu Fuss bis zur Ecke Rampenstraße'),
             ('schild', '50% 35%', 'Die Ecke', 'Das Schild leuchtet')]
    karten = ''.join('<div class="v03-h" style="--n:%d">%s<p class="v03-u"><b class="titel">%s</b><span>%s</span></p></div>' % (
        j, k(kk, 'v03-b', M + '30vw', p), E(o), E(u)) for j, (kk, p, o, u) in enumerate(halte))
    return kap(n, '<div class="v03-kopf">%s%s</div><div class="v03-weg"><i class="v03-linie"></i>%s</div><div class="v03-fuss">%s%s</div>' % (
        txt(KZ + titel(['Haasemannstraße 13.'])), satz(), karten,
        zeilen('v03-z', ['Adresse', 'Telefon', 'Instagram']), karte()))
V.append(('Der Weg in drei Bildern', v03))

# 04 Panorama: die beiden Schilder an der Hausecke als breites Band, das sich beim Scrollen heranzieht; darunter Titel und Zeilen nebeneinander
V.append(('Panorama', lambda n: kap(n, '%s<div class="v04-g">%s%s</div>' % (
    k('pf-schild', 'v04-b', M + '1120px', '50% 42%'), txt(KZ + titel() + satz()), txt(zeilen() + karte())))))

# 05 Tag und Nacht: links die Terrasse am Tag, rechts das Schild am Abend, gleich gross; beim Scrollen gleiten beide verschieden schnell
V.append(('Tag und Nacht', lambda n: kap(n, '%s<div class="v05-bilder">%s%s</div><div class="v05-g">%s%s</div>' % (
    KZ, '<figure class="v05-f">%s<figcaption>Draussen an der Ecke</figcaption></figure>' % k('terrasse', 'v05-b v05-l', M + '46vw', '50% 55%'),
    '<figure class="v05-f">%s<figcaption>Am Abend leuchtet das Schild</figcaption></figure>' % k('pf-schild', 'v05-b v05-r', M + '46vw', '45% 45%'),
    txt(titel(['Haasemannstraße 13.']) + satz()), txt(zeilen() + karte())))))

# 06 Die Visitenkarte: eine dunkle Karte über die Breite mit dem roten Logo, Titel gross, die Zeilen in zwei Spalten; sie richtet sich beim Auftritt auf
V.append(('Die Visitenkarte', lambda n: kap(n, KZ + '<div class="v06-karte"><div class="v06-o"><span class="logo v06-logo">%s</span>%s</div><div class="v06-u">%s%s</div></div>' % (
    LOGO, txt(titel() + satz()), zeilen('v06-z'), karte('')))))

# 07 Am Abend: der Abschnitt dunkel wie die Bar; rechts der Blick durch die Tür auf den roten Boden, das Foto gleitet beim Scrollen in seinem Rahmen
V.append(('Am Abend', lambda n: kap(n, '<div class="v07-g">%s%s</div>' % (
    txt(KZ + titel() + satz() + zeilen() + karte('')), k('tuer-rot', 'v07-b', M + '44vw', '50% 50%')), cls='')))

# 08 Die Tafel: links Titel, Satz und Knopf, rechts eine dunkle Tafel mit den Zeilen in grosser Schrift, die nacheinander hochschweben
V.append(('Die Tafel', lambda n: kap(n, '<div class="v08-g">%s<div class="v08-tafel">%s</div></div>' % (
    txt(KZ + titel() + satz() + k('terrasse', 'v08-b', M + '40vw', '50% 55%') + karte()), zeilen('v08-z')))))

# 09 Zwei Hochformate: das Schild und die offene Tür nebeneinander, Wand an Wand; das zweite Bild kommt aus der Tiefe nach
V.append(('Zwei Hochformate', lambda n: kap(n, '<div class="v09-g"><div class="v09-bilder">%s%s</div>%s</div>' % (
    k('schild', 'v09-b v09-1', M + '24vw', '50% 40%'), k('tuer-rot', 'v09-b v09-2', M + '24vw', '50% 50%'),
    txt(KZ + titel() + satz() + zeilen() + karte())))))

# 10 Titel in voller Breite: die Adresse in Hero-Grösse über die ganze Seite, darunter Bild, Satz und Zeilen in drei Spalten
V.append(('Titel in voller Breite', lambda n: kap(n, KZ + titel(['Haasemannstraße 13.'], 'v10-t') + '<div class="v10-g">%s%s%s</div>' % (
    k('terrasse', 'v10-b', M + '30vw', '50% 55%'), txt(satz('v10-s') + karte()), zeilen('v10-z')))))

# 11 Das Strassenschild: der Titel als emailliertes Strassenschild, darunter «Rampenstraße»; beide klappen von oben herunter und pendeln aus
V.append(('Das Strassenschild', lambda n: kap(n, '<div class="v11-g">%s%s</div>' % (
    txt(KZ + '<div class="v11-pfosten"><h2 class="v11-schild v11-a"><span>Haasemannstraße</span><b>13</b></h2>'
        '<p class="v11-schild v11-c"><span>Rampenstraße</span></p></div>' + satz() + zeilen(nur=['Adresse', 'Bahn', 'Telefon', 'Instagram']) + karte()),
    k('schild', 'v11-b', M + '40vw', '50% 40%')))))

# 12 Von der Bahn bis zur Tür: links bleibt der Blick durchs Fenster stehen, rechts der Weg von oben nach unten; die Goldlinie wächst mit dem Scrollen
def v12(n):
    halte = [('Am Küchengarten', 'Mit der Stadtbahn bis Am Küchengarten, Linien 9 und 17.'),
             ('Zwei Minuten', 'Dann zu Fuss, ein paar Schritte. Gegenüber vom Restaurant 11A.'),
             ('Die Ecke', 'Haasemannstraße, Ecke Rampenstraße. Das Schild an der Ecke leuchtet.')]
    weg = ''.join('<div class="v12-h" style="--n:%d"><b class="titel">%s</b><p>%s</p></div>' % (j, E(o), E(u)) for j, (o, u) in enumerate(halte))
    return kap(n, '<div class="v12-g"><div class="v12-l">%s</div>%s</div>' % (
        k('fenster', 'v12-b', M + '44vw', '50% 55%'),
        txt(KZ + titel() + '<div class="v12-weg"><i class="v12-linie"></i>%s</div>' % weg + zeilen(nur=['Adresse', 'Telefon', 'Instagram']) + karte())))
V.append(('Von der Bahn bis zur Tür', v12))

# 13 Die Zeilen quer: oben Bild und Titel, unten die fünf Angaben als eine Leiste über die ganze Breite, die Felder steigen nacheinander
V.append(('Die Zeilen quer', lambda n: kap(n, '<div class="v13-g">%s%s</div>%s' % (
    k('terrasse', 'v13-b', M + '46vw', '50% 55%'), txt(KZ + titel() + satz() + karte()),
    '<div class="v13-leiste">%s</div>' % ''.join('<div style="--n:%d"><span class="etikett">%s</span><span>%s</span></div>' % (j, E(x), y) for j, (x, y) in enumerate(ZEILEN))))))

# 14 Das Fenster in der Mitte: links der Titel, in der Mitte der Blick durchs Fenster als hohes Bild, rechts Satz und Zeilen; das Bild steigt langsamer
V.append(('Das Fenster in der Mitte', lambda n: kap(n, '<div class="v14-g">%s%s%s</div>' % (
    txt(KZ + titel(['Haasemann-', 'straße', '13.'], 'v14-t') + satz() + karte()), k('fenster', 'v14-b', M + '32vw', '50% 55%'),
    txt(zeilen('v14-z'))))))

# 15 Der Aushang: wie das gerahmte Plakat neben der Tür; die Angaben als Aushang in Creme mit Rahmen, er pendelt beim Auftritt aus; daneben die beiden Schilder an der Hausecke
V.append(('Der Aushang', lambda n: kap(n, '<div class="v15-g">%s<div class="v15-aushang"><div class="v15-innen"><span class="logo v15-logo">%s</span>%s%s%s%s</div></div></div>' % (
    k('pf-schild', 'v15-b', M + '46vw', '62% 50%'), LOGO, KZ, titel(), zeilen('v15-z'), karte('')), cls='')))

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
