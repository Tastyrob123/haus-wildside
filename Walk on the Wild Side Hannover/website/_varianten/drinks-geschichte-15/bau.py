# Walk on the Wild Side · Drinks-Seite, «Das Gespräch» und «Wie Momo arbeitet» als eine Geschichte: 15 Fassungen (29.10.2026).
# Robert: «für den Bereich Drinks … eine Geschichte erzählen, die aber anders visuell dargestellt ist und schöner … das hängt ja alles unmittelbar
# miteinander zusammen … so richtig schön edel luxuriös, die Landingpage ist jetzt unser Anker». Kein Auswählen mehr (Startseite, 29.10.).
# Texte nur aus der heutigen Drinks-Seite. Fotos: Kundenfotos der Culinarium-Abende im Wild Side, die auf der Startseite noch nicht stehen.
# 00 = heutiger Stand. Wechsel mit ← →. Aufruf: python3 _varianten/drinks-geschichte-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/drinks-geschichte-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))
K = '../../Culinarium Hannover/_quelle/vom-kunden/'
bilder.BILDER.update({
    'dg-shaker': (K + 'drive/4568.jpg', 'Momo schüttelt einen Drink, daneben ein Gast'),
    'dg-abseihen': (K + '4313.jpg', 'Ein Drink wird durch ein Sieb in eine Reihe Gläser abgeseiht'),
    'dg-behaelter': (K + 'drive/3937.jpg', 'Glasbehälter mit Zapfhahn auf der Rückbar'),
    'dg-siphon': (K + 'drive/63963.jpg', 'Schaum aus dem Siphon auf einen Drink'),
    'dg-giessen': (K + 'drive/63740.jpg', 'Ein Drink wird durch ein Sieb in ein Coupe gegossen'),
    'dg-coupes': (K + 'drive/4829.jpg', 'Coupes mit Goldrand in einer Reihe'),
    'dg-coupes-hand': (K + 'drive/4828.jpg', 'Eine Hand stellt Coupes mit Goldrand bereit'),
    'dg-flaschen': (K + 'drive/3956.jpg', 'Flaschen auf der Rückbar'),
    'dg-feige': (K + 'drive/4876.jpg', 'Ein Drink mit einer Feigenscheibe im Glas'),
    'dg-schaumglas': (K + 'drive/4893.jpg', 'Ein Drink mit Schaum in der Hand'),
    'dg-coupe-tisch': (K + 'drive/63741.jpg', 'Ein Drink im Coupe auf dem Holztisch'),
})

KZ_A = B.kz('Das Gespräch', 'An der Theke', 0)
TITEL_A = B.h2(['Erst die Frage,', 'dann das Glas.'])
TEXT_A = 'So läuft es an der Theke: Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll. Daraus wird ein Drink.'
FRAGEN = [('Der Geschmack', 'Lieber sauer, süss, bitter oder rauchig?'), ('Das Glas', 'Klar, cremig oder spritzig?'),
          ('Was hinein soll', 'Gin, Rum, Mezcal, Whisky oder ganz ohne Alkohol?')]
ZITAT = '«Du sagst mir, was du magst, ich mache dir einen Drink.»'
WER = 'Momo Ben Khelifa'
UEBERGANG = 'Und so entsteht daraus ein Drink.'
KZ_B = B.kz('Wie Momo arbeitet', 'Drei Techniken', 0)
TITEL_B = B.h2(['Klar, weich, sauber.'])
TEXT_B = 'Momo hat Biotechnologie studiert, bevor er hinter die Bar ging. Man schmeckt es: Drei Techniken aus dem Labor machen aus einer Idee einen klaren, weichen Drink.'
TECH = [
    ('dg-abseihen', 'Milk Washing', 'Milch bindet die Trübstoffe und wird wieder abgefiltert. Was bleibt, ist klar wie Wasser und weich wie Sahne. Momo macht das seit seiner Berliner Zeit, den Milchpunsch gab es schon 2021.'),
    ('dg-behaelter', 'Fat Washing', 'Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel. Kalt gestellt, abgehoben, fertig: Der Rum schmeckt nach Butter, ohne fettig zu sein.'),
    ('dg-giessen', 'Enzyme', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt. So wird aus Apfel oder Birne ein klarer Saft, der sich in einen Drink giessen lässt wie Wasser.'),
]
POS = {'dg-shaker': '45% 35%', 'dg-abseihen': '50% 45%', 'dg-behaelter': '50% 50%', 'dg-giessen': '50% 45%', 'dg-siphon': '50% 40%'}


def img(k, sizes, extra=''):
    p = POS.get(k)
    return B.img_tag(k, sizes, extra=(' style="object-position:%s"' % p if p else '') + extra)


def kachel(k, sizes, cls='', stil=''):
    return '<figure class="kachel leise %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def foto(k, sizes, cls='foto'):
    return '<figure class="%s" data-k="%s" style="--lq:url(%s)">%s</figure>' % (cls, k, mache(k)['lq'], img(k, sizes))


def p(t, cls='text', i=1):
    return '<p class="%s sw" style="--i:%d">%s</p>' % (cls, i, E(t))


def zitat(i=3, cls=''):
    return '<p class="ge-zitat sw %s" style="--i:%d">%s<small>%s</small></p>' % (cls, i, E(ZITAT), E(WER))


def frage(j, cls='g-frage'):
    e, f = FRAGEN[j]
    return '<div class="%s"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (cls, E(e), E(f))


def tech(j, cls='g-tech', mit_bild=False, sizes='30vw'):
    k, t, s = TECH[j]
    return '<div class="%s">%s<span class="etikett">Technik</span><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (cls, kachel(k, sizes) if mit_bild else '', E(t), E(s))


def kopf_a(rechts=''):
    return '<div class="g-kopf"><div>%s%s%s</div>%s</div>' % (KZ_A, TITEL_A, p(TEXT_A), rechts)


def kopf_b(rechts=''):
    return '<div class="g-kopf"><div>%s%s%s</div>%s</div>' % (KZ_B, TITEL_B, p(TEXT_B), rechts)


def sek(n, a, b, cls='', ueb=True):
    """Beide Abschnitte, dazwischen der Satz, der hinüberführt. Ids wie heute (gespraech, technik)."""
    return ('<section class="kap auf gx gs%02d %s" id="gespraech"><div class="innen ga%02d" data-g="%d">%s</div>%s</section>'
            '<section class="kap auf gx gt%02d %s" id="technik"><div class="innen gb%02d" data-g="%d">%s</div></section>') % (
        n, cls, n, n, a, B.ueber(UEBERGANG) if ueb else '', n, cls, n, n, b)


V = []

# 01 · Ein Weg von der Frage ins Glas: die Goldlinie der Startseite trägt beide Kapitel, sechs Stationen im Zickzack.
def v01(n):
    st = lambda k, t, z, j: '<div class="w1-st w1-%s"><figure class="kachel leise" style="--lq:url(%s)">%s</figure><i class="w1-punkt"></i><div class="w1-satz"><span class="etikett">%s</span><p class="titel">%s</p>%s</div></div>' % (
        'l' if j % 2 == 0 else 'r', mache(k)['lq'], img(k, '(max-width:900px) 80vw, 38vw'), E(t), E(z[0]), '<p class="text">%s</p>' % E(z[1]) if z[1] else '')
    # Ohne Lücke: Die Linie von Weg 1 läuft bis in den Satz, darunter gleich «Wie Momo arbeitet» (Robert 29.10.: «dieser krasse Leerraum dazwischen … so random»).
    a = kopf_a(zitat(2)) + '<div class="w1-weg" data-w1><div class="w1-linie"><i></i></div>%s</div>' % ''.join(
        st(k, FRAGEN[j][0], (FRAGEN[j][1], ''), j) for j, k in enumerate(['dg-shaker', 'dg-coupes', 'dg-flaschen']))
    a += '<div class="w1-weg w1-bruecke" data-w1><div class="w1-linie"><i></i></div>%s</div>' % B.ueber(UEBERGANG)
    b = kopf_b() + '<div class="w1-weg" data-w1><div class="w1-linie"><i></i></div>%s</div>' % ''.join(
        st(k, 'Technik', (t, s), j + 1) for j, (k, t, s) in enumerate(TECH))
    return sek(n, a, b, 'w1-seite', ueb=False)
V.append(('Ein Weg von der Frage ins Glas', v01))

# 02 · Die Fragen als grosse Schrift: drei Zeilen in Prata neben Momo am Shaker; die Techniken als drei Bilder Kante an Kante bis an den Rand.
def v02(n):
    a = '<div class="g2">%s<div class="g2-text">%s%s<div class="g2-fragen">%s</div>%s</div></div>' % (
        kachel('dg-shaker', '(max-width:900px) 100vw, 42vw', 'g2-bild sw'), KZ_A, TITEL_A,
        ''.join('<p class="titel g2-z sw" style="--i:%d">%s</p>' % (j + 2, E(f)) for j, (e, f) in enumerate(FRAGEN)), zitat(5))
    b = kopf_b() + '</div><div class="g2-band staffel">%s</div><div class="innen"><div class="g2-unter">%s</div>' % (
        ''.join('<div style="--n:%d">%s</div>' % (j, foto(k, '(max-width:900px) 100vw, 34vw')) for j, (k, t, s) in enumerate(TECH)),
        ''.join(tech(j, 'g-tech g2-t') for j in range(3)))
    return sek(n, a, b)
V.append(('Grosse Fragen, Bilder bis an den Rand', v02))

# 03 · Das Bild bleibt stehen: links steht ein Foto, rechts laufen die drei Fragen und die drei Techniken vorbei, zu jedem kommt das Bild.
def v03(n):
    def teil(kopf, bloecke, ks):
        stapel = ''.join(foto(k, '(max-width:900px) 100vw, 46vw', 'foto' + (' an' if j == 0 else '')) for j, k in enumerate(ks))
        return '<div class="g3"><div class="g3-links"><div class="g3-halt"><div class="g3-stapel">%s</div></div></div><div class="g3-rechts">%s%s</div></div>' % (stapel, kopf, bloecke)
    fr = ''.join('<div class="g3-block" data-j="%d"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (j, E(e), E(f)) for j, (e, f) in enumerate(FRAGEN))
    tb = ''.join('<div class="g3-block" data-j="%d"><span class="etikett">Technik</span><p class="titel">%s</p><p class="text">%s</p></div>' % (j, E(t), E(s)) for j, (k, t, s) in enumerate(TECH))
    a = teil('<div class="g3-kopf">%s%s%s</div>' % (KZ_A, TITEL_A, p(TEXT_A)), fr + '<div class="g3-ende">%s</div>' % zitat(1), ['dg-shaker', 'dg-coupes-hand', 'dg-flaschen'])
    b = teil('<div class="g3-kopf">%s%s%s</div>' % (KZ_B, TITEL_B, p(TEXT_B)), tb, [k for k, t, s in TECH])
    return sek(n, a, b)
V.append(('Das Bild bleibt stehen', v03))

# 04 · Geschlossenes Raster: beide Kapitel als Platten und Fotos Kante an Kante, die Fragen auf Creme, die Techniken mit ihrem Bild.
def v04(n):
    a = '<div class="g4a staffel"><div class="platte g4-kopf" style="--n:0">%s%s%s</div>%s%s<div class="plakat g4-fragen" style="--n:3">%s</div><div class="platte g4-zitat" style="--n:4"><p class="titel">%s</p><span class="etikett">%s</span></div></div>' % (
        KZ_A, TITEL_A, '<p class="text">%s</p>' % E(TEXT_A), kachel('dg-shaker', '30vw', 'g4-b1', '--n:1'), kachel('dg-coupes', '30vw', 'g4-b2', '--n:2'),
        ''.join(frage(j) for j in range(3)), E(ZITAT), E(WER))
    b = '<div class="g4b staffel"><div class="platte g4-kopf" style="--n:0">%s%s%s</div>%s</div>' % (
        KZ_B, TITEL_B, '<p class="text">%s</p>' % E(TEXT_B),
        ''.join('%s<div class="platte g4-t" style="--n:%d"><span class="etikett">Technik</span><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (
            kachel(k, '25vw', 'g4-tb', '--n:%d' % (j + 1)), j + 1, E(t), E(s)) for j, (k, t, s) in enumerate(TECH)))
    return sek(n, a, b)
V.append(('Geschlossenes Raster', v04))

# 05 · Die Karte ist eine Frage: die drei Fragen stehen auf einem cremefarbenen Blatt, als wären sie die Karte; die Techniken als drei Fenster.
def v05(n):
    a = '<div class="g5">%s<div class="g5-blatt sw" style="--i:2"><span class="etikett">Die Karte im Wild Side</span>%s<p class="g5-wer">%s<small>%s</small></p></div></div>' % (
        '<div>%s%s%s</div>' % (KZ_A, TITEL_A, p(TEXT_A)), ''.join('<div class="g5-z"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (E(e), E(f)) for e, f in FRAGEN), E(ZITAT), E(WER))
    b = kopf_b() + '<div class="g5-fenster staffel">%s</div>' % ''.join(
        '<div class="g5-f" style="--n:%d">%s<div class="g5-ft"><span class="etikett">Technik</span><h3 class="titel">%s</h3><p class="text">%s</p></div></div>' % (
            j, foto(k, '(max-width:900px) 100vw, 60vw'), E(t), E(s)) for j, (k, t, s) in enumerate(TECH))
    return sek(n, a, b)
V.append(('Die Karte ist eine Frage', v05))

# 06 · Halb und halb: links ein Foto bis an den Rand, rechts die Fragen; darunter gespiegelt, rechts das Foto, links die Techniken.
def v06(n):
    a = '</div><div class="g6 g6-l"><div class="g6-bild sw">%s</div><div class="g6-text">%s%s%s<div class="g6-liste">%s</div>%s</div></div><div class="innen">' % (
        foto('dg-shaker', '(max-width:900px) 100vw, 50vw'), KZ_A, TITEL_A, p(TEXT_A), ''.join(frage(j, 'g-frage g6-z') for j in range(3)), zitat(4))
    b = '</div><div class="g6 g6-r"><div class="g6-text">%s%s%s<div class="g6-liste">%s</div></div><div class="g6-bild sw">%s</div></div><div class="innen">' % (
        KZ_B, TITEL_B, p(TEXT_B), ''.join(tech(j, 'g-tech g6-z') for j in range(3)), foto('dg-abseihen', '(max-width:900px) 100vw, 50vw'))
    return sek(n, a, b, 'g6-sek')
V.append(('Halb und halb, gespiegelt', v06))

# 07 · Abzüge auf dem Tresen: Fotos liegen wie Abzüge übereinander, Kante an Kante; daneben die Fragen, unten die Techniken unter ihren Abzügen.
def v07(n):
    abz = lambda ks, cls: '<div class="g7-tresen %s flaeche">%s</div>' % (cls, ''.join('<figure class="g7-abzug g7-%d" style="--lq:url(%s)">%s</figure>' % (j, mache(k)['lq'], img(k, '(max-width:900px) 50vw, 24vw')) for j, k in enumerate(ks)))
    a = '<div class="g7">%s<div>%s%s%s<div class="g7-fragen">%s</div>%s</div></div>' % (
        abz(['dg-shaker', 'dg-coupes', 'dg-flaschen'], ''), KZ_A, TITEL_A, p(TEXT_A), ''.join(frage(j) for j in range(3)), zitat(4))
    b = kopf_b() + '<div class="g7-drei staffel">%s</div>' % ''.join(
        '<div class="g7-t" style="--n:%d"><figure class="g7-abzug" style="--lq:url(%s)">%s</figure><span class="etikett">Technik</span><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (
            j, mache(k)['lq'], img(k, '(max-width:900px) 100vw, 30vw'), E(t), E(s)) for j, (k, t, s) in enumerate(TECH))
    return sek(n, a, b)
V.append(('Abzüge auf dem Tresen', v07))

# 08 · Die Liste zum Zeigen: Fragen und Techniken als grosse Zeilen; wer darüberfährt, sieht rechts das passende Bild.
def v08(n):
    def liste(zeilen, ks):
        z = ''.join('<button type="button" class="g8-z%s" data-j="%d"><span class="etikett">%s</span><span class="titel">%s</span>%s</button>' % (
            ' an' if j == 0 else '', j, E(e), E(t), '<span class="text">%s</span>' % E(s) if s else '') for j, (e, t, s) in enumerate(zeilen))
        st = ''.join(foto(k, '(max-width:900px) 100vw, 40vw', 'foto' + (' an' if j == 0 else '')) for j, k in enumerate(ks))
        return '<div class="g8"><div class="g8-liste">%s</div><div class="g8-rahmen"><div class="g8-stapel">%s</div></div></div>' % (z, st)
    a = kopf_a(zitat(2)) + liste([(e, f, '') for e, f in FRAGEN], ['dg-shaker', 'dg-coupes-hand', 'dg-flaschen'])
    b = kopf_b() + liste([('Technik', t, s) for k, t, s in TECH], [k for k, t, s in TECH])
    return sek(n, a, b)
V.append(('Die Liste zum Zeigen', v08))

# 09 · Auf hellem Papier: beide Kapitel auf Creme, die Fragen und Techniken als Tabelle mit Goldlinien, daneben je ein Bildpaar.
def v09(n):
    tab = lambda z: '<div class="g9-tab staffel">%s</div>' % ''.join('<div class="g9-z" style="--n:%d"><span class="etikett">%s</span><div><p class="titel">%s</p>%s</div></div>' % (
        j, E(e), E(t), '<p class="text">%s</p>' % E(s) if s else '') for j, (e, t, s) in enumerate(z))
    paar = lambda a1, a2: '<div class="g9-paar flaeche">%s%s</div>' % (kachel(a1, '(max-width:900px) 50vw, 24vw'), kachel(a2, '(max-width:900px) 50vw, 24vw'))
    a = '<div class="g9"><div>%s%s%s%s%s</div>%s</div>' % (KZ_A, TITEL_A, p(TEXT_A), tab([(e, f, '') for e, f in FRAGEN]), zitat(4), paar('dg-shaker', 'dg-coupes'))
    b = '<div class="g9 g9-r">%s<div>%s%s%s%s</div></div>' % (paar('dg-abseihen', 'dg-giessen'), KZ_B, TITEL_B, p(TEXT_B), tab([('Technik', t, s) for k, t, s in TECH]))
    return sek(n, a, b, 'hell')
V.append(('Auf hellem Papier', v09))

# 10 · Drei Fragen, drei Antworten: oben drei Spalten mit je einer Frage über einem Foto, unten dieselben drei Spalten mit den Techniken.
def v10(n):
    a = kopf_a(zitat(2)) + '<div class="g10 staffel">%s</div>' % ''.join(
        '<div class="g10-s" style="--n:%d">%s<span class="etikett">%s</span><p class="titel">%s</p></div>' % (j, kachel(k, '(max-width:900px) 100vw, 30vw'), E(FRAGEN[j][0]), E(FRAGEN[j][1]))
        for j, k in enumerate(['dg-shaker', 'dg-coupes', 'dg-flaschen']))
    b = kopf_b() + '<div class="g10 staffel">%s</div>' % ''.join(
        '<div class="g10-s" style="--n:%d">%s<span class="etikett">Technik</span><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (j, kachel(k, '(max-width:900px) 100vw, 30vw'), E(t), E(s))
        for j, (k, t, s) in enumerate(TECH))
    return sek(n, a, b)
V.append(('Drei Fragen, drei Antworten', v10))

# 11 · Momos Satz als Titel: sein Satz steht riesig über dem Kapitel, darunter die Fragen klein; die Techniken als drei grosse Wörter mit Bild.
def v11(n):
    a = '<div class="g11">%s<blockquote class="titel g11-zitat">%s</blockquote><p class="g11-wer">%s</p><div class="g11-unten">%s<div>%s%s<div class="g11-fragen">%s</div></div></div></div>' % (
        KZ_A, B.zl(['«Du sagst mir,', 'was du magst,', 'ich mache dir', 'einen Drink.»'], i0=1), E(WER), kachel('dg-shaker', '(max-width:900px) 100vw, 40vw', 'g11-bild'),
        '<h3 class="titel g11-h">Erst die Frage, dann das Glas.</h3>', p(TEXT_A), ''.join(frage(j) for j in range(3)))
    b = kopf_b() + '<div class="g11-worte">%s</div>' % ''.join(
        '<div class="g11-w">%s<div><p class="titel g11-gross">%s</p><p class="text">%s</p></div></div>' % (kachel(k, '(max-width:900px) 100vw, 34vw'), E(t), E(s)) for k, t, s in TECH)
    return sek(n, a, b)
V.append(('Momos Satz als Titel', v11))

# 12 · Das Band zum Blättern: die drei Techniken in einer Reihe grosser Bilder bis über den Rand zum Wischen; oben die Fragen neben dem Glas.
def v12(n):
    pf = '<div class="g12-pfeile"><button type="button" class="g12-pf" data-d="-1" aria-label="zurück">%s</button><button type="button" class="g12-pf" data-d="1" aria-label="weiter">%s</button></div>' % (B.PFEIL, B.PFEIL)
    a = '<div class="g12a"><div>%s%s%s<div class="g12-fragen">%s</div>%s</div>%s</div>' % (
        KZ_A, TITEL_A, p(TEXT_A), ''.join(frage(j) for j in range(3)), zitat(4), kachel('dg-coupes-hand', '(max-width:900px) 100vw, 44vw', 'g12-bild'))
    b = kopf_b(pf) + '<div class="g12-band">%s</div>' % ''.join(
        '<div class="g12-k">%s<span class="etikett">Technik</span><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (kachel(k, '(max-width:900px) 80vw, 40vw'), E(t), E(s))
        for k, t, s in TECH + [('dg-siphon', 'Und dann der Schaum', 'Aus dem Siphon, direkt aufs Glas.')])
    return sek(n, a, b, 'g12-sek')
V.append(('Das Band zum Blättern', v12))

# 13 · Nach der Uhr: ein grosses Bild läuft von selbst durch die Techniken, feine Striche oben; die Fragen als Satz mit Bildern dazwischen.
def v13(n):
    worte = ['Lieber sauer, süss, bitter oder rauchig', 'klar, cremig oder spritzig', 'Gin, Rum, Mezcal, Whisky oder ganz ohne Alkohol']
    teile = []
    for j, (w, k) in enumerate(zip(worte, ['dg-shaker', 'dg-coupes', 'dg-flaschen'])):
        vorn, _, letzt = w.rpartition(' ')
        teile.append('%s <span class="g13-nb">%s <span class="g13-bild" style="--lq:url(%s)">%s</span>%s</span>' % (E(vorn), E(letzt), mache(k)['lq'], img(k, '260px'), '?' if j == 2 else ','))
    a = '<div class="g13-kopf">%s%s%s</div><p class="titel g13-satz sw" style="--i:2">%s</p>%s' % (KZ_A, TITEL_A, p(TEXT_A), ' '.join(teile), zitat(3))
    striche = ''.join('<button type="button" data-j="%d" aria-label="%s"><i></i></button>' % (j, E(t)) for j, (k, t, s) in enumerate(TECH))
    stapel = ''.join(foto(k, '(max-width:900px) 100vw, 56vw', 'foto' + (' an' if j == 0 else '')) for j, (k, t, s) in enumerate(TECH))
    saetze = ''.join('<div class="g13-s%s" data-j="%d"><span class="etikett">Technik</span><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (' an' if j == 0 else '', j, E(t), E(s)) for j, (k, t, s) in enumerate(TECH))
    b = '<div class="g13"><div class="g13-links sw"><div class="g13-striche">%s</div><div class="g13-stapel">%s</div></div><div class="g13-rechts">%s%s%s<div class="g13-saetze">%s</div></div></div>' % (
        striche, stapel, KZ_B, TITEL_B, p(TEXT_B), saetze)
    return sek(n, a, b)
V.append(('Nach der Uhr', v13))

# 14 · Gegenlauf: zwei Bildspalten laufen beim Scrollen verschieden schnell, in der Mitte stehen Fragen und Techniken untereinander.
def v14(n):
    a = '<div class="g14"><div class="g14-sp" data-tempo="-0.07">%s</div><div class="g14-mitte">%s%s%s<div class="g14-fragen">%s</div>%s</div><div class="g14-sp g14-r" data-tempo="0.12">%s</div></div>' % (
        ''.join(kachel(k, '(max-width:900px) 50vw, 28vw') for k in ['dg-shaker', 'dg-flaschen']), KZ_A, TITEL_A, p(TEXT_A), ''.join(frage(j) for j in range(3)), zitat(4),
        ''.join(kachel(k, '(max-width:900px) 50vw, 28vw') for k in ['dg-coupes', 'dg-feige']))
    b = '<div class="g14"><div class="g14-sp" data-tempo="-0.07">%s</div><div class="g14-mitte">%s%s%s<div class="g14-fragen">%s</div></div><div class="g14-sp g14-r" data-tempo="0.12">%s</div></div>' % (
        ''.join(kachel(k, '(max-width:900px) 50vw, 28vw') for k in ['dg-abseihen', 'dg-giessen']), KZ_B, TITEL_B, p(TEXT_B), ''.join(tech(j) for j in range(3)),
        ''.join(kachel(k, '(max-width:900px) 50vw, 28vw') for k in ['dg-behaelter', 'dg-schaumglas']))
    return sek(n, a, b)
V.append(('Gegenlauf', v14))

# 15 · Ein Bild zieht sich auf: Momo am Shaker steht klein in der Mitte und wird beim Scrollen gross, darunter die Fragen; die Techniken im Zickzack ohne Linie.
def v15(n):
    a = '<div class="g15-kopf">%s%s%s</div><div class="g15-buehne"><div class="g15-halt"><div class="g15-bild">%s</div></div></div><div class="g15-fragen staffel">%s</div>%s' % (
        KZ_A, TITEL_A, p(TEXT_A), foto('dg-shaker', '(max-width:900px) 100vw, 88vw'), ''.join('<div style="--n:%d">%s</div>' % (j, frage(j)) for j in range(3)), zitat(2, 'g15-zitat'))
    b = kopf_b() + '<div class="g15-zz">%s</div>' % ''.join(
        '<div class="g15-st g15-%s">%s%s</div>' % ('l' if j % 2 == 0 else 'r', kachel(k, '(max-width:900px) 100vw, 50vw'), tech(j)) for j, (k, t, s) in enumerate(TECH))
    return sek(n, a, b)
V.append(('Ein Bild zieht sich auf', v15))


def seite(n):
    h = unter.drinks()
    if n:
        a = h.find('<section class="kap auf" id="gespraech"')
        b = h.find('</section>', h.find('id="technik"')) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
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
