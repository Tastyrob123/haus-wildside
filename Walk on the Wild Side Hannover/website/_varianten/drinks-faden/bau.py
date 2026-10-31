# Walk on the Wild Side · Drinks-Seite, «Das Gespräch» und «Wie Momo arbeitet» als EIN durchgehender Faden (30.10.2026).
# Robert: «die Vorschläge sind alle absoluter Mist … das soll ein durchgehender Faden mit verschiedenen Animationen und Bildern sein …
# Du kannst doch nicht einfach zweimal dieselben Sachen auseinandersetzen.» Also: keine zwei Blöcke im gleichen Stil, sondern ein Weg von der
# ersten Frage bis zur letzten Technik; jeder Schritt mit eigenem Bild, eigener Anordnung und eigener Bewegung. Texte nur von der heutigen Seite.
# Fotos: die Aufnahmen des Fotografen aus Rudis Drive, die auf der Website noch nicht stehen.
# 00 = heutiger Stand. Wechsel mit ← →. 20 Fäden (Robert: «Kannst du mir bitte 20 Versionen geben und nicht 3?»). Aufruf: python3 _varianten/drinks-faden/bau.py
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/drinks-faden'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))
K = '../../Culinarium Hannover/_quelle/vom-kunden/'
bilder.BILDER.update({
    'dg-siphon': (K + 'drive/63963.jpg', 'Schaum aus dem Siphon auf einen Drink'),
    'dg-coupes-hand': (K + 'drive/4828.jpg', 'Eine Hand stellt Coupes mit Goldrand bereit'),
    'dg-feige': (K + 'drive/4876.jpg', 'Ein Drink mit einer Feigenscheibe im Glas'),
    'dg-schaumglas': (K + 'drive/4893.jpg', 'Ein Drink mit Schaum in der Hand'),
    'wf-raum': (K + 'drive/3925.jpg', 'Momo hinter der Bar, über ihm der Schriftzug NEGRONI'),
    'wf-giesst': (K + 'drive/3823.jpg', 'Momo giesst einen Drink ins Glas'),
    'wf-coupes-oben': (K + 'drive/4834.jpg', 'Coupes mit Goldrand von oben'),
    'wf-sour': (K + 'drive/4558.jpg', 'Ein Drink mit Schaum, dahinter eine Flasche'),
    'wf-pink': (K + 'drive/4108.jpg', 'Ein heller Drink mit Schaum bei Kerzenlicht'),
    'wf-zwei': (K + 'drive/4843.jpg', 'Zwei Drinks nebeneinander auf dem Tisch'),
    'wf-erdbeer': (K + 'drive/4858.jpg', 'Ein Longdrink mit Eis und Erdbeere'),
    'wf-nick': (K + 'drive/5369.jpg', 'Ein klarer Drink in einem Stielglas'),
    'wf-highball': (K + 'drive/4921.jpg', 'Ein heller Longdrink im hohen Glas'),
    'wf-tablett': (K + 'drive/63972.jpg', 'Eine Reihe heller Drinks auf dem Tablett'),
    'wf-coupe-tisch': (K + 'drive/63741.jpg', 'Ein Drink im Coupe auf dem Holztisch'),
    'wf-theke': (K + 'drive/4019.jpg', 'Momo an der Theke, neben ihm die Zapfhähne'),
    'wf-negroni': (K + 'drive/5062.jpg', 'Die Bar im Dunkeln, der Schriftzug NEGRONI leuchtet'),
    'wf-glas': (K + '4274.jpg', 'Ein Drink im Stielglas auf dunklem Grund'),
    'wf-fenster': (K + 'drive/3998.jpg', 'Blick durchs Fenster in die Bar bei Nacht'),
})

TITEL_A = ['Erst die Frage,', 'dann das Glas.']
TEXT_A = 'So läuft es an der Theke: Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll. Daraus wird ein Drink.'
FR = [('Der Geschmack', 'Lieber sauer, süss, bitter oder rauchig?'), ('Das Glas', 'Klar, cremig oder spritzig?'),
      ('Was hinein soll', 'Gin, Rum, Mezcal, Whisky oder ganz ohne Alkohol?')]
ZITAT = '«Du sagst mir, was du magst, ich mache dir einen Drink.»'
WER = 'Momo Ben Khelifa'
UEBERGANG = 'Und so entsteht daraus ein Drink.'
TITEL_B = ['Klar, weich, sauber.']
TEXT_B = 'Momo hat Biotechnologie studiert, bevor er hinter die Bar ging. Man schmeckt es: Drei Techniken aus dem Labor machen aus einer Idee einen klaren, weichen Drink.'
TE = [('Milk Washing', 'Milch bindet die Trübstoffe und wird wieder abgefiltert. Was bleibt, ist klar wie Wasser und weich wie Sahne. Momo macht das seit seiner Berliner Zeit, den Milchpunsch gab es schon 2021.'),
      ('Fat Washing', 'Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel. Kalt gestellt, abgehoben, fertig: Der Rum schmeckt nach Butter, ohne fettig zu sein.'),
      ('Enzyme', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt. So wird aus Apfel oder Birne ein klarer Saft, der sich in einen Drink giessen lässt wie Wasser.')]
POS = {'dg-shaker': '45% 35%', 'dg-abseihen': '50% 45%', 'dg-giessen': '50% 45%', 'wf-raum': '50% 40%', 'wf-giesst': '55% 40%'}


def img(k, sizes, extra=''):
    p = POS.get(k)
    return B.img_tag(k, sizes, extra=(' style="object-position:%s"' % p if p else '') + extra)


def foto(k, sizes, cls='foto', stil=''):
    return '<figure class="%s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def trueb(k, sizes, cls=''):
    """Dasselbe Bild zweimal: oben eine gedeckte Kopie, die beim Scrollen verschwindet."""
    t = img(k, sizes, ' class="trueb" aria-hidden="true"').replace(' alt="%s"' % E(mache(k)['alt']), ' alt=""', 1)
    return '<figure class="foto %s" style="--lq:url(%s)">%s%s</figure>' % (cls, mache(k)['lq'], img(k, sizes), t)


def et(t):
    return '<span class="etikett">%s</span>' % E(t)


def worte(t):
    return ' '.join('<span class="ww">%s</span>' % E(w) for w in t.split())


def kz_a(i=0):
    return B.kz('Das Gespräch', 'An der Theke', i)


def kz_b(i=0):
    return B.kz('Wie Momo arbeitet', 'Drei Techniken', i)


def sw(t, cls='text', i=1, tag='p'):
    return '<%s class="%s sw" style="--i:%d">%s</%s>' % (tag, cls, i, E(t), tag)


def faden(n, cls, inhalt):
    return '<section class="kap auf gx f%02d %s" id="gespraech" data-g="%d">%s</section>' % (n, cls, n, inhalt)


V = []


# 01 · Vom Dunkel ins Klare. Der Faden ist das Licht: Der Abschnitt beginnt in der Nacht der Bar, wird beim Übergang warm wie Bernstein
# und endet bei den Techniken auf Creme, klar wie der Drink. Jeder Schritt hat ein eigenes Bild und eine eigene Bewegung:
# der Shaker öffnet sich aus einem Schlitz, drei Coupes steigen verschieden schnell, die Wörter gehen an, das Bild wird klar, kippt ins Lot, giesst nach.
def v01(n):
    h = '<div class="t1-grund" aria-hidden="true"><i class="t1-a"></i><i class="t1-c"></i></div><div class="innen t1">'
    h += '<div class="t1-kopf">%s<h2 class="titel t-gross">%s</h2>%s<p class="ge-zitat sw" style="--i:3">%s<small>%s</small></p></div>' % (
        kz_a(), B.zl(TITEL_A, i0=1), sw(TEXT_A, 'text', 2), E(ZITAT), E(WER))
    h += '<div class="t1-s1" data-p><div class="t1-schlitz"><div class="t1-gegen">%s</div></div><div class="t1-satz">%s<p class="titel t1-frage">%s</p></div></div>' % (
        foto('dg-shaker', '(max-width:760px) 100vw, 50vw'), et(FR[0][0]), E(FR[0][1]))
    h += '<div class="t1-s2" data-p>%s<p class="titel t1-frage">%s</p><div class="t1-drei">%s</div></div>' % (
        et(FR[1][0]), E(FR[1][1]), ''.join(foto(k, '(max-width:760px) 33vw, 30vw', 'foto t1-d', '--v:%dpx' % v) for k, v in (('dg-coupes-hand', 90), ('dg-coupes', 200), ('wf-coupes-oben', 310))))
    h += '<div class="t1-s3" data-p data-w><div class="t1-satz">%s<p class="titel t1-frage">%s</p></div><div class="t1-zoom">%s</div></div>' % (
        et(FR[2][0]), worte(FR[2][1]), foto('dg-flaschen', '(max-width:760px) 100vw, 46vw'))
    h += '<section class="t1-t" id="technik"><div class="t1-s4" data-p data-bga><p class="titel t1-ueber">%s</p>%s<h2 class="titel t-gross">%s</h2>%s</div>' % (
        E(UEBERGANG), kz_b(), B.zl(TITEL_B, i0=1), sw(TEXT_B, 'text', 2))
    h += '<div class="t1-s5" data-p data-bgc>%s<div class="t1-satz">%s<h3 class="titel">%s</h3><p class="text">%s</p></div></div>' % (
        trueb('dg-abseihen', '(max-width:760px) 100vw, 50vw', 't1-klar'), et('Technik'), E(TE[0][0]), E(TE[0][1]))
    h += '<div class="t1-s6" data-p><div class="t1-satz">%s<h3 class="titel">%s</h3><p class="text">%s</p></div><div class="t1-lot">%s</div></div>' % (
        et('Technik'), E(TE[1][0]), E(TE[1][1]), foto('dg-behaelter', '(max-width:760px) 100vw, 46vw'))
    h += '<div class="t1-s7" data-p>%s<div class="t1-rechts">%s<div class="t1-satz">%s<h3 class="titel">%s</h3><p class="text">%s</p></div></div></div>' % (
        foto('dg-giessen', '(max-width:760px) 100vw, 56vw', 'foto t1-gross'), foto('wf-highball', '(max-width:760px) 100vw, 34vw', 'foto t1-klein'),
        et('Technik'), E(TE[2][0]), E(TE[2][1]))
    h += '</section></div>'
    return faden(n, '', h)
V.append(('Vom Dunkel ins Klare', v01))


# 02 · Frage und Antwort. Der Faden ist Momos Stimme: Jede Frage steht gross mit einer kurzen Goldlinie davor, und jedes Mal antworten Bilder.
# Auf den Geschmack vier Drinks, die sich auf den Tisch legen; auf das Glas drei Gläser mit klar, cremig, spritzig darunter;
# auf die Flaschen ein Bild, über das man fährt; dann antworten die Techniken mit dem, was Momo tut.
def v02(n):
    zeile = lambda e, t, wort=False: '<div class="t2-zeile">%s<p class="titel t2-stimme">%s</p></div>' % (et(e), worte(t) if wort else E(t))
    h = '<div class="innen t2">'
    h += '<div class="t2-kopf"><div>%s<h2 class="titel t-gross">%s</h2></div>%s</div>' % (kz_a(), B.zl(TITEL_A, i0=1), sw(TEXT_A, 'text', 2))
    h += '<div class="t2-s0" data-p data-w><p class="titel t2-momo">%s</p><small>%s</small></div>' % (worte(ZITAT), E(WER))
    h += '<div class="t2-s1" data-p>%s<div class="t2-vier">%s</div></div>' % (zeile(*FR[0]), ''.join(
        foto(k, '(max-width:760px) 50vw, 24vw', 'foto t2-karte', '--r:%ddeg;--j:%d' % (r, j)) for j, (k, r) in enumerate((('wf-sour', -7), ('wf-pink', 5), ('wf-zwei', -4), ('wf-erdbeer', 8)))))
    h += '<div class="t2-s2" data-p>%s<div class="t2-drei">%s</div></div>' % (zeile(*FR[1]), ''.join(
        '<div class="t2-glas" style="--j:%d"><div class="t2-maske">%s</div><p class="titel">%s</p></div>' % (j, foto(k, '(max-width:760px) 33vw, 30vw'), w)
        for j, (k, w) in enumerate((('wf-nick', 'klar'), ('dg-schaumglas', 'cremig'), ('wf-highball', 'spritzig')))))
    h += '<div class="t2-s3" data-p>%s<div class="t2-fahrt">%s</div></div>' % (zeile(*FR[2]), foto('dg-flaschen', '(max-width:760px) 100vw, 48vw'))
    h += '<section class="t2-t" id="technik"><div class="t2-s4" data-p><div class="t2-mitte"><i></i><p class="titel">%s</p><i></i></div><div class="t2-bkopf"><div>%s<h2 class="titel t-gross">%s</h2></div>%s</div></div>' % (
        E(UEBERGANG), kz_b(), B.zl(TITEL_B, i0=1), sw(TEXT_B, 'text', 2))
    h += '<div class="t2-s5" data-p><div class="t2-kz">%s<p class="text">%s</p></div><div class="t2-paar">%s%s</div></div>' % (
        zeile('Technik', TE[0][0]), E(TE[0][1]), foto('dg-abseihen', '(max-width:760px) 50vw, 30vw', 'foto t2-p1'), foto('wf-tablett', '(max-width:760px) 50vw, 30vw', 'foto t2-p2'))
    h += '<div class="t2-s6" data-p><div class="t2-klapp">%s</div><div>%s<p class="text">%s</p></div></div>' % (
        foto('dg-behaelter', '(max-width:760px) 100vw, 40vw'), zeile('Technik', TE[1][0]), E(TE[1][1]))
    h += '<div class="t2-s7" data-p>%s<div class="t2-folge">%s<i class="t2-pfeil"></i>%s</div><p class="text t2-unter">%s</p></div>' % (
        zeile('Technik', TE[2][0]), foto('dg-giessen', '(max-width:760px) 50vw, 36vw', 'foto t2-f1'), foto('wf-coupe-tisch', '(max-width:760px) 50vw, 36vw', 'foto t2-f2'), E(TE[2][1]))
    h += '</section></div>'
    return faden(n, '', h)
V.append(('Frage und Antwort', v02))


# 03 · Die Wand füllt sich. Der Faden ist eine Bilderwand: Der Bereich bleibt stehen, links wechselt der Text Schritt für Schritt
# von der ersten Frage bis zur letzten Technik, rechts kommt zu jedem Schritt ein Bild an seinen Platz, bis die Wand geschlossen ist.
def v03(n):
    schritte = [
        ('wf-giesst', '%s<h2 class="titel t3-gross">%s</h2><p class="text">%s</p><p class="ge-zitat">%s<small>%s</small></p>' % (kz_a(), '<br>'.join(TITEL_A), E(TEXT_A), E(ZITAT), E(WER))),
        ('dg-shaker', et(FR[0][0]) + '<p class="titel t3-frage">%s</p>' % E(FR[0][1])),
        ('dg-coupes', et(FR[1][0]) + '<p class="titel t3-frage">%s</p>' % E(FR[1][1])),
        ('dg-flaschen', et(FR[2][0]) + '<p class="titel t3-frage">%s</p>' % E(FR[2][1])),
        ('wf-sour', '<p class="titel t3-frage t3-leise">%s</p>%s<h2 class="titel t3-gross">%s</h2><p class="text">%s</p>' % (E(UEBERGANG), kz_b(), TITEL_B[0], E(TEXT_B))),
        ('dg-abseihen', et('Technik') + '<h3 class="titel t3-frage">%s</h3><p class="text">%s</p>' % (E(TE[0][0]), E(TE[0][1]))),
        ('dg-behaelter', et('Technik') + '<h3 class="titel t3-frage">%s</h3><p class="text">%s</p>' % (E(TE[1][0]), E(TE[1][1]))),
        ('dg-giessen', et('Technik') + '<h3 class="titel t3-frage">%s</h3><p class="text">%s</p>' % (E(TE[2][0]), E(TE[2][1]))),
    ]
    flaechen = 'abcdefgh'
    texte = ''.join('<div class="t3-text%s" data-j="%d">%s</div>' % (' an' if j == 0 else '', j, s) for j, (k, s) in enumerate(schritte))
    wand = ''.join('<div class="t3-kachel%s" style="grid-area:%s;--j:%d">%s</div>' % (' da' if j == 0 else '', flaechen[j], j, foto(k, '(max-width:760px) 50vw, 26vw')) for j, (k, s) in enumerate(schritte))
    striche = ''.join('<i%s></i>' % (' class="an"' if j == 0 else '') for j in range(len(schritte)))
    h = ('<div class="t3-pin" data-pin><section class="t3-anker" id="technik" aria-hidden="true"></section><div class="t3-buehne"><div class="innen t3">'
         '<div class="t3-links"><div class="t3-texte">%s</div><div class="t3-striche">%s</div></div><div class="t3-wand">%s</div></div></div></div>') % (texte, striche, wand)
    return faden(n, 't3-sek', h)
V.append(('Die Wand füllt sich', v03))


# ---------------------------------------------------------------- Bausteine für die Fäden 04 bis 20
# Jeder Schritt ist ein Baustein mit eigener Anordnung und eigener Bewegung (über --p). Innerhalb eines Fadens kommt kein Baustein zweimal vor.
ALT = lambda k: mache(k)['alt']


def txt(j, wort=False):
    """Text eines Schritts: 1 bis 3 die Fragen, 5 bis 7 die Techniken."""
    if j in (1, 2, 3):
        e, f = FR[j - 1]
        return et(e) + '<p class="titel b-frage">%s</p>' % (worte(f) if wort else E(f))
    t, z = TE[j - 5]
    return et('Technik') + '<h3 class="titel b-tech">%s</h3><p class="text">%s</p>' % (worte(t) if wort else E(t), E(z))


def bild(k, sizes='(max-width:760px) 100vw, 46vw', cls=''):
    return foto(k, sizes, 'foto ' + cls)


def b(art, j, inhalt, cls=''):
    return '<div class="b bs-%s %s" data-p style="--k:%d">%s</div>' % (art, cls, j, inhalt)


# Anfang (Schritt 0) und Wende (Schritt 4)
def kopf(art, k=None):
    t = '%s<h2 class="titel t-gross">%s</h2>' % (kz_a(), '<br>'.join(TITEL_A))
    z = '<p class="ge-zitat">%s<small>%s</small></p>' % (E(ZITAT), E(WER))
    if art == 'mitte':
        return b('kopf-mitte', 0, '%s<p class="text">%s</p>%s' % (t, E(TEXT_A), z))
    if art == 'links':
        return b('kopf-links', 0, '<div>%s<p class="text">%s</p></div>%s' % (t, E(TEXT_A), z))
    return b('kopf-bild', 0, '<div>%s<p class="text">%s</p>%s</div><div class="b-rahmen">%s</div>' % (t, E(TEXT_A), z, bild(k, '(max-width:760px) 100vw, 40vw')))


def wende(art, k=None):
    t = '%s<h2 class="titel t-gross">%s</h2><p class="text">%s</p>' % (kz_b(), TITEL_B[0], E(TEXT_B))
    u = '<p class="titel b-ueber">%s</p>' % E(UEBERGANG)
    if art == 'mitte':
        return b('wende-mitte', 4, u + t)
    if art == 'linien':
        return b('wende-linien', 4, '<div class="b-linien"><i></i>%s<i></i></div><div class="b-wkopf"><div>%s<h2 class="titel t-gross">%s</h2></div><p class="text">%s</p></div>' % (
            u, kz_b(), TITEL_B[0], E(TEXT_B)))
    return b('wende-bild', 4, '<div class="b-rahmen">%s</div><div>%s%s</div>' % (bild(k, '(max-width:760px) 100vw, 40vw'), u, t))


# Bausteine mit Bildern; seite = 'l' (Bild links) oder 'r'
def schlitz(j, k, seite='l'):
    return b('schlitz', j, '<div class="b-schlitz"><div class="b-gegen">%s</div></div><div class="b-satz">%s</div>' % (bild(k), txt(j)), 's-' + seite)

def zoom(j, k, seite='r'):
    return b('zoom', j, '<div class="b-satz">%s</div><div class="b-fenster">%s</div>' % (txt(j), bild(k)), 's-' + seite)

def steigen3(j, ks):
    return b('steigen3', j, '<div class="b-satz b-mittig">%s</div><div class="b-drei">%s</div>' % (txt(j), ''.join(bild(k, '(max-width:760px) 33vw, 30vw', 'b-st') for k in ks)))

def karten4(j, ks):
    return b('karten4', j, '<div class="b-satz">%s</div><div class="b-vier">%s</div>' % (txt(j), ''.join(
        '<div class="b-karte" style="--r:%ddeg;--i:%d">%s</div>' % (r, i, bild(k, '(max-width:760px) 50vw, 24vw')) for i, (k, r) in enumerate(zip(ks, (-7, 5, -4, 8))))))

def masken3(j, ks, worte_=('klar', 'cremig', 'spritzig')):
    return b('masken3', j, '<div class="b-satz">%s</div><div class="b-drei">%s</div>' % (txt(j), ''.join(
        '<div class="b-mk" style="--i:%d"><div class="b-maske">%s</div><p class="titel">%s</p></div>' % (i, bild(k, '(max-width:760px) 33vw, 30vw'), w) for i, (k, w) in enumerate(zip(ks, worte_)))))

def fahrt(j, k, seite='r'):
    return b('fahrt', j, '<div class="b-satz">%s</div><div class="b-fenster">%s</div>' % (txt(j), bild(k)), 's-' + seite)

def trueb_(j, k, seite='l'):
    return b('trueb', j, '%s<div class="b-satz">%s</div>' % (trueb(k, '(max-width:760px) 100vw, 50vw', 'b-tr'), txt(j)), 's-' + seite)

def lot(j, k, seite='r'):
    return b('lot', j, '<div class="b-satz">%s</div><div class="b-lot">%s</div>' % (txt(j), bild(k)), 's-' + seite)

def klapp(j, k, seite='l'):
    return b('klapp', j, '<div class="b-klapp">%s</div><div class="b-satz">%s</div>' % (bild(k), txt(j)), 's-' + seite)

def paar(j, k1, k2):
    return b('paar', j, '<div class="b-kz">%s</div><div class="b-paar">%s%s</div>' % (txt(j), bild(k1, '(max-width:760px) 60vw, 52vw', 'b-p1'), bild(k2, '(max-width:760px) 40vw, 36vw', 'b-p2')))

def folge(j, k1, k2):
    return b('folge', j, '<div class="b-satz b-mittig">%s</div><div class="b-folge">%s<i class="b-strich"></i>%s</div>' % (txt(j), bild(k1, '(max-width:760px) 50vw, 36vw', 'b-f1'), bild(k2, '(max-width:760px) 50vw, 36vw', 'b-f2')))

def nachkommen(j, k1, k2):
    return b('nachkommen', j, '%s<div class="b-rechts">%s<div class="b-satz">%s</div></div>' % (bild(k1, '(max-width:760px) 100vw, 56vw', 'b-gross'), bild(k2, '(max-width:760px) 100vw, 34vw', 'b-klein'), txt(j)))

def aufzug(j, k, seite='l'):
    return b('aufzug', j, '<div class="b-aufzug"><div class="b-auf">%s</div></div><div class="b-satz">%s</div>' % (bild(k), txt(j)), 's-' + seite)

def wachsen(j, k):
    return b('wachsen', j, '<div class="b-satz b-mittig">%s</div><div class="b-wachs">%s</div>' % (txt(j), bild(k, '(max-width:760px) 100vw, 44vw')))

def kippen(j, k, seite='r'):
    return b('kippen', j, '<div class="b-satz">%s</div><div class="b-kipp">%s</div>' % (txt(j), bild(k)), 's-' + seite)

def stufen(j, ks):
    return b('stufen', j, '<div class="b-satz">%s</div><div class="b-stufen">%s</div>' % (txt(j), ''.join(bild(k, '(max-width:760px) 33vw, 22vw', 'b-su') for k in ks)))

def band4(j, ks):
    return b('band4', j, '<div class="b-satz b-mittig">%s</div><div class="b-band"><div class="b-bandzug">%s</div></div>' % (txt(j), ''.join(bild(k, '(max-width:760px) 50vw, 30vw') for k in ks)))

def wortweise(j, k, seite='r'):
    return b('wortweise', j, '<div class="b-satz">%s</div><div class="b-fenster">%s</div>' % (txt(j, True), bild(k)), 's-' + seite)


def faden_b(n, cls, schritte, vor=None, dekor=''):
    """Acht Schritte als ein Weg; ab Schritt 4 liegt der Anker «technik». vor = {Index: Zwischenstück}."""
    vor = vor or {}
    teile = []
    for i, x in enumerate(schritte):
        if i == 4:
            teile.append('<section class="b-teil" id="technik">')
        teile.append(vor.get(i, '') + x)
    teile.append('</section>')
    return faden(n, 'bf ' + cls, '%s<div class="innen b-weg">%s</div>' % (dekor, ''.join(teile)))


# 04 · Momos Satz trägt durch. Zwischen den Schritten steht sein Satz in vier Stücken, riesig über die ganze Breite.
def v04(n):
    stueck = lambda t: '<div class="b-stueck" data-p><p class="titel">%s</p></div>' % ''.join('<span style="--w:%d">%s </span>' % (i, E(w)) for i, w in enumerate(t.split()))
    return faden_b(n, 'f-satz', [kopf('links'), aufzug(1, 'dg-shaker', 'r'), masken3(2, ['wf-nick', 'dg-schaumglas', 'wf-highball']), zoom(3, 'dg-flaschen', 'l'),
                                 wende('mitte'), paar(5, 'dg-abseihen', 'wf-tablett'), kippen(6, 'dg-behaelter', 'l'), folge(7, 'dg-giessen', 'wf-coupe-tisch')],
                   {1: stueck('«Du sagst mir,'), 2: stueck('was du magst,'), 4: stueck('ich mache dir'), 5: stueck('einen Drink.»')})
V.append(('Momos Satz trägt durch', v04))


# 05 · Der Pegel. Links läuft eine goldene Leiste mit, die sich füllt wie ein Glas; daneben steht immer, wo man gerade ist.
def v05(n):
    pegel = '<div class="b-pegel" aria-hidden="true"><div class="b-pegel-in"><span class="etikett" data-pegel>Das Gespräch</span><div class="b-roehre"><i></i></div></div></div>'
    return faden_b(n, 'f-pegel', [kopf('bild', 'wf-raum'), schlitz(1, 'dg-shaker', 'l'), steigen3(2, ['dg-coupes-hand', 'dg-coupes', 'wf-coupes-oben']), fahrt(3, 'dg-flaschen', 'r'),
                                  wende('linien'), trueb_(5, 'dg-abseihen', 'l'), klapp(6, 'dg-behaelter', 'r'), nachkommen(7, 'dg-giessen', 'wf-highball')], dekor=pegel)
V.append(('Der Pegel', v05))


# 06 · Immer näher. Mit jedem Schritt wird das Bild grösser, als ginge man an die Theke heran, vom Raum bis zum einzelnen Glas.
def v06(n):
    return faden_b(n, 'f-naeher', [kopf('bild', 'wf-fenster'), kippen(1, 'wf-theke', 'r'), wortweise(2, 'dg-coupes', 'l'), lot(3, 'dg-flaschen', 'r'),
                                   wende('mitte'), aufzug(5, 'dg-abseihen', 'l'), zoom(6, 'dg-behaelter', 'r'), wachsen(7, 'wf-nick')])
V.append(('Immer näher', v06))


# 07 · Hell und dunkel. Jeder Schritt ist ein Band über die ganze Breite, abwechselnd Nacht und Creme, wie die Plakate der Bar.
def v07(n):
    s = [kopf('mitte'), zoom(1, 'dg-shaker', 'r'), karten4(2, ['dg-coupes', 'wf-nick', 'dg-schaumglas', 'wf-highball']), schlitz(3, 'dg-flaschen', 'l'),
         wende('bild', 'wf-sour'), stufen(5, ['dg-abseihen', 'wf-tablett', 'dg-siphon']), lot(6, 'dg-behaelter', 'l'), aufzug(7, 'dg-giessen', 'r')]
    return faden_b(n, 'f-baender', [x.replace('class="b ', 'class="b hellband ', 1) if i % 2 else x for i, x in enumerate(s)])
V.append(('Hell und dunkel', v07))


# 08 · Die Treppe. Die Schritte rücken einer nach dem anderen nach rechts wie Stufen hinunter, bei den Techniken wieder zurück.
def v08(n):
    s = [kopf('links'), fahrt(1, 'dg-shaker', 'r'), schlitz(2, 'dg-coupes-hand', 'l'), kippen(3, 'dg-flaschen', 'r'),
         wende('linien'), klapp(5, 'dg-abseihen', 'l'), trueb_(6, 'dg-behaelter', 'r'), zoom(7, 'dg-giessen', 'l')]
    tl = [0, 4, 8, 12, 0, 12, 8, 4]
    return faden_b(n, 'f-treppe', [x.replace('style="--k:%d"' % i, 'style="--k:%d;--tl:%d%%;width:%d%%"' % (i, tl[i], 100 - tl[i]), 1) for i, x in enumerate(s)])
V.append(('Die Treppe', v08))


# 16 · Die Schlagworte. Hinter jedem Schritt zieht ein riesiges Wort in feiner Goldlinie vorbei: Frage, Geschmack, Glas, Mezcal, Labor, Milch, Fett, Enzyme.
def v16(n):
    w = ['Frage', 'Geschmack', 'Glas', 'Mezcal', 'Labor', 'Milch', 'Fett', 'Enzyme']
    vor = {i: '<p class="titel b-wort" aria-hidden="true" data-p>%s</p>' % x for i, x in enumerate(w)}
    return faden_b(n, 'f-worte', [kopf('mitte'), wachsen(1, 'dg-shaker'), band4(2, ['dg-coupes', 'wf-coupes-oben', 'dg-coupes-hand', 'wf-erdbeer']), aufzug(3, 'dg-flaschen', 'l'),
                                  wende('mitte'), lot(5, 'dg-abseihen', 'r'), schlitz(6, 'dg-behaelter', 'l'), kippen(7, 'dg-giessen', 'r')], vor)


# 18 · Das Magazin. Oben läuft eine Kopfzeile mit wie im Heft, jedes Bild trägt eine kleine Bildunterschrift, die Schritte wechseln ihre Spalten.
def v18(n):
    kopfzeile = '<div class="b-kopfzeile" aria-hidden="true"><span data-kopf>Das Gespräch · An der Theke</span></div>'
    return faden_b(n, 'f-magazin', [kopf('bild', 'wf-giesst'), stufen(1, ['dg-shaker', 'wf-sour', 'wf-pink']), zoom(2, 'dg-coupes', 'l'), wortweise(3, 'dg-flaschen', 'r'),
                                    wende('linien'), folge(5, 'dg-abseihen', 'wf-tablett'), aufzug(6, 'dg-behaelter', 'r'), trueb_(7, 'dg-giessen', 'l')], dekor=kopfzeile)


# 19 · Wand an Wand. Jeder Schritt läuft als Band von Rand zu Rand, die Bilder stossen aneinander, zwischen den Bändern nur eine feine Goldlinie.
def v19(n):
    return faden_b(n, 'f-wand', [kopf('links'), band4(1, ['dg-shaker', 'wf-sour', 'wf-zwei', 'wf-pink']), steigen3(2, ['wf-nick', 'dg-schaumglas', 'wf-highball']), nachkommen(3, 'dg-flaschen', 'wf-negroni'),
                                 wende('mitte'), paar(5, 'wf-tablett', 'dg-abseihen'), karten4(6, ['dg-behaelter', 'dg-siphon', 'wf-glas', 'dg-feige']), wachsen(7, 'dg-giessen')])


# 20 · Die Zoom-Kette. Jedes Bild kommt nah heran und zieht sich beim Scrollen auf, Schritt für Schritt, wie eine Kamera, die zurückfährt.
def v20(n):
    return faden_b(n, 'f-zoomkette', [kopf('bild', 'wf-giesst'), lot(1, 'dg-shaker', 'r'), stufen(2, ['wf-coupes-oben', 'dg-coupes', 'dg-coupes-hand']), klapp(3, 'dg-flaschen', 'l'),
                                      wende('bild', 'wf-glas'), schlitz(5, 'dg-abseihen', 'r'), wachsen(6, 'dg-behaelter'), paar(7, 'dg-giessen', 'wf-coupe-tisch')])


# ---------------------------------------------------------------- Stehende Bühnen (09 bis 15, 17)
# Der Bereich bleibt stehen; jedes Element [data-s] bekommt --d (Abstand zum aktuellen Schritt) und die Klassen an / war / ueber.
def txt_pin(j):
    if j == 0:
        return '%s<h2 class="titel p-gross">%s</h2><p class="text">%s</p><p class="ge-zitat">%s<small>%s</small></p>' % (kz_a(), '<br>'.join(TITEL_A), E(TEXT_A), E(ZITAT), E(WER))
    if j == 4:
        return '<p class="titel p-leise">%s</p>%s<h2 class="titel p-gross">%s</h2><p class="text">%s</p>' % (E(UEBERGANG), kz_b(), TITEL_B[0], E(TEXT_B))
    return txt(j)


def buehne(n, cls, links, rechts, anzahl=8):
    texte = ''.join('<div class="p-text" data-s style="--j:%d">%s</div>' % (j, txt_pin(j)) for j in range(anzahl)) if links is None else links
    return faden(n, 'pf ' + cls, ('<div class="p-pin" data-pin style="--n:%d"><section class="t3-anker" id="technik" aria-hidden="true"></section><div class="p-buehne"><div class="innen p-raster">'
                                  '<div class="p-links">%s</div><div class="p-rechts">%s</div></div></div></div>') % (anzahl, texte, rechts))


# 09 · Der Satz in der Mitte. Der Text steht still in der Mitte, links und rechts ziehen die Bilder des Schritts verschieden schnell vorbei.
def v09(n):
    paare = [('wf-raum', 'wf-negroni'), ('dg-shaker', 'wf-sour'), ('dg-coupes', 'dg-schaumglas'), ('dg-flaschen', 'wf-theke'),
             ('wf-glas', 'wf-pink'), ('dg-abseihen', 'wf-tablett'), ('dg-behaelter', 'dg-siphon'), ('dg-giessen', 'wf-coupe-tisch')]
    bilder_ = ''.join('<div class="m-paar" data-s style="--j:%d">%s%s</div>' % (j, bild(a, '(max-width:760px) 50vw, 24vw', 'm-l'), bild(c, '(max-width:760px) 50vw, 20vw', 'm-r')) for j, (a, c) in enumerate(paare))
    return buehne(n, 'f-mitte', None, bilder_)
V.append(('Der Satz in der Mitte', v09))


# 10 · Die Wendekarte. Eine einzige Karte steht rechts und wendet sich bei jedem Schritt, mal um die senkrechte, mal um die waagrechte Achse.
def v10(n):
    ks = ['wf-giesst', 'dg-shaker', 'dg-coupes-hand', 'dg-flaschen', 'wf-sour', 'dg-abseihen', 'dg-behaelter', 'dg-giessen']
    return buehne(n, 'f-karte', None, '<div class="w-karte">%s</div>' % ''.join('<div class="w-seite" data-s style="--j:%d">%s</div>' % (j, bild(k, '(max-width:760px) 90vw, 40vw')) for j, k in enumerate(ks)))
V.append(('Die Wendekarte', v10))


# 11 · Der Stapel. Die Bilder liegen als Stapel Abzüge da; mit jedem Schritt fliegt das oberste in eine andere Richtung davon.
def v11(n):
    ks = ['wf-theke', 'dg-shaker', 'dg-coupes', 'dg-flaschen', 'wf-nick', 'dg-abseihen', 'dg-behaelter', 'dg-giessen']
    wurf = [(-38, -14), (30, 12), (-20, -18), (44, 16), (-46, -10), (24, 20), (-30, -16), (0, 0)]
    return buehne(n, 'f-stapel', None, '<div class="s-stapel">%s</div>' % ''.join(
        '<div class="s-abzug" data-s style="--j:%d;--r:%ddeg;--x:%dvw;--w:%ddeg">%s</div>' % (j, (j % 3 - 1) * 3, x, w, bild(k, '(max-width:760px) 90vw, 36vw')) for j, (k, (x, w)) in enumerate(zip(ks, wurf))))
V.append(('Der Stapel', v11))


# 12 · Die Reihe. Alle Bilder des Abschnitts stehen in einer Reihe; die Reihe gleitet weiter, das Bild des Schritts tritt gross nach vorn, darunter der Text.
def v12(n):
    ks = ['wf-raum', 'dg-shaker', 'dg-coupes-hand', 'dg-flaschen', 'wf-glas', 'dg-abseihen', 'dg-behaelter', 'dg-giessen']
    reihe = '<div class="r2-reihe">%s</div>' % ''.join('<div class="r2-bild" data-s style="--j:%d">%s</div>' % (j, bild(k, '(max-width:760px) 60vw, 30vw')) for j, k in enumerate(ks))
    texte = ''.join('<div class="p-text" data-s style="--j:%d">%s</div>' % (j, txt_pin(j)) for j in range(8))
    return faden(n, 'pf f-reihe', ('<div class="p-pin" data-pin style="--n:8"><section class="t3-anker" id="technik" aria-hidden="true"></section><div class="p-buehne r2-buehne">%s'
                                   '<div class="innen r2-texte">%s</div></div></div>') % (reihe, texte))
V.append(('Die Reihe', v12))


# 13 · Der Paternoster. Rechts zwei Bildspalten, die eine fährt hinauf, die andere hinunter; links wechselt der Text Schritt für Schritt.
def v13(n):
    a = ['wf-giesst', 'dg-shaker', 'dg-coupes', 'dg-flaschen', 'wf-sour', 'dg-abseihen', 'dg-behaelter', 'dg-giessen']
    c = ['wf-negroni', 'wf-pink', 'dg-schaumglas', 'wf-theke', 'wf-glas', 'wf-tablett', 'dg-siphon', 'wf-coupe-tisch']
    spalte = lambda ks, cls: '<div class="pa-spalte %s">%s</div>' % (cls, ''.join('<div class="pa-bild" data-s style="--j:%d">%s</div>' % (j, bild(k, '(max-width:760px) 45vw, 20vw')) for j, k in enumerate(ks)))
    return buehne(n, 'f-pater', None, '<div class="pa-schacht">%s%s</div>' % (spalte(a, 'pa-hoch'), spalte(c, 'pa-runter')))
V.append(('Der Paternoster', v13))


# 14 · Quer durch die Bar. Der Bereich steht, die Schritte ziehen als ein Band von rechts nach links vorbei, jeder Schritt anders gebaut.
def v14(n):
    ks = [('wf-raum',), ('dg-shaker', 'wf-sour'), ('wf-nick', 'dg-schaumglas', 'wf-highball'), ('dg-flaschen',), ('wf-glas',), ('dg-abseihen', 'wf-tablett'), ('dg-behaelter',), ('dg-giessen', 'wf-coupe-tisch')]
    tafeln = ''.join('<article class="qb qb%d" data-s style="--j:%d"><div class="qb-bilder">%s</div><div class="qb-text">%s</div></article>' % (
        j, j, ''.join(bild(k, '(max-width:760px) 70vw, 30vw') for k in kk), txt_pin(j)) for j, kk in enumerate(ks))
    return faden(n, 'pf f-quer', '<div class="p-pin qb-pin" data-pin style="--n:8"><section class="t3-anker" id="technik" aria-hidden="true"></section><div class="p-buehne qb-buehne"><div class="qb-zug">%s</div></div></div>' % tafeln)
V.append(('Quer durch die Bar', v14))


# 15 · Das Heft. Ein aufgeschlagenes Heft auf Creme; jede Seite, die sich wendet, zeigt vorn den nächsten Schritt und hinten sein Bild.
def v15(n):
    ks = ['dg-shaker', 'dg-coupes', 'dg-flaschen', 'wf-sour', 'dg-abseihen', 'dg-behaelter', 'dg-giessen']
    blaetter = ''.join('<div class="hb-blatt" data-s style="--j:%d"><div class="hb-vorn">%s</div><div class="hb-hinten">%s</div></div>' % (
        j, txt_pin(j + 1), bild(k, '(max-width:760px) 90vw, 36vw')) for j, k in enumerate(ks))
    return faden(n, 'pf f-heft', ('<div class="p-pin" data-pin style="--n:8"><section class="t3-anker" id="technik" aria-hidden="true"></section><div class="p-buehne hb-buehne"><div class="hb-heft">'
                                  '<div class="hb-links">%s</div><div class="hb-rechts">%s</div>%s</div></div></div>') % (txt_pin(0), bild('wf-coupe-tisch', '(max-width:760px) 90vw, 36vw'), blaetter))
V.append(('Das Heft', v15))


V.append(('Die Schlagworte', v16))


# 17 · Ein Bild, viele Blicke. Ein grosses Bild steht; bei jedem Schritt fährt der Blick an eine andere Stelle oder auf das nächste Bild.
def v17(n):
    fotos = ['dg-shaker', 'wf-nick', 'wf-sour', 'dg-giessen']
    blicke = [(0, 1, 50, 50), (0, 1.9, 36, 42), (1, 1, 50, 50), (2, 1.7, 76, 30), (2, 1, 50, 50), (3, 1.8, 46, 62), (3, 1.6, 40, 22), (3, 1, 50, 50)]
    lagen = ''.join('<div class="bb-lage" data-f="%d">%s</div>' % (i, bild(k, '(max-width:760px) 100vw, 60vw')) for i, k in enumerate(fotos))
    texte = ''.join('<div class="p-text" data-s data-blick="%d,%s,%d,%d" style="--j:%d">%s</div>' % (f, s, x, y, j, txt_pin(j)) for j, (f, s, x, y) in enumerate(blicke))
    return buehne(n, 'f-blick', texte, '<div class="bb-rahmen">%s</div>' % lagen)
V.append(('Ein Bild, viele Blicke', v17))
V.append(('Das Magazin', v18))
V.append(('Wand an Wand', v19))
V.append(('Die Zoom-Kette', v20))


def seite(n):
    h = unter.drinks()
    if n:
        a = h.rfind('<section', 0, h.find('id="gespraech"'))
        b = h.find('</section>', h.find('id="technik"')) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %02d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
