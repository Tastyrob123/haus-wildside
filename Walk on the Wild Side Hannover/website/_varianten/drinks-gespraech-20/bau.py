# Walk on the Wild Side · Drinks-Seite, «Das Gespräch» und «Wie Momo arbeitet»: 20 neue Darstellungen (30.10.2026).
# Robert: «Ich finde die Idee cool, aber wir benutzen genau dasselbe schon auf der Landingpage … was Eigenes Neues …, was richtig geil passt zum Stil der Seite.»
# Also: kein Zickzack an der Goldlinie (Startseite), keine laufenden Bildreihen (Drinks-Kopf), kein Schachbrett, kein Mosaik, und nichts aus der Runde
# drinks-geschichte-15 wiederholen. Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte nur aus der heutigen Drinks-Seite.
# 00 = heutiger Stand. Wechsel mit ← →. Aufruf: python3 _varianten/drinks-gespraech-20/bau.py → 00.html … 20.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/drinks-gespraech-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))
K = '../../Culinarium Hannover/_quelle/vom-kunden/'
bilder.BILDER.update({
    'dg-siphon': (K + 'drive/63963.jpg', 'Schaum aus dem Siphon auf einen Drink'),
    'dg-coupes-hand': (K + 'drive/4828.jpg', 'Eine Hand stellt Coupes mit Goldrand bereit'),
    'dg-feige': (K + 'drive/4876.jpg', 'Ein Drink mit einer Feigenscheibe im Glas'),
    'dg-schaumglas': (K + 'drive/4893.jpg', 'Ein Drink mit Schaum in der Hand'),
})

KZ_A = B.kz('Das Gespräch', 'An der Theke', 0)
TITEL_A = B.h2(['Erst die Frage,', 'dann das Glas.'])
TEXT_A = 'So läuft es an der Theke: Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll. Daraus wird ein Drink.'
FR = [('dg-shaker', 'Der Geschmack', 'Lieber sauer, süss, bitter oder rauchig?'), ('dg-coupes', 'Das Glas', 'Klar, cremig oder spritzig?'),
      ('dg-flaschen', 'Was hinein soll', 'Gin, Rum, Mezcal, Whisky oder ganz ohne Alkohol?')]
ZITAT = '«Du sagst mir, was du magst, ich mache dir einen Drink.»'
WER = 'Momo Ben Khelifa'
UEBERGANG = 'Und so entsteht daraus ein Drink.'
KZ_B = B.kz('Wie Momo arbeitet', 'Drei Techniken', 0)
TITEL_B = B.h2(['Klar, weich, sauber.'])
TEXT_B = 'Momo hat Biotechnologie studiert, bevor er hinter die Bar ging. Man schmeckt es: Drei Techniken aus dem Labor machen aus einer Idee einen klaren, weichen Drink.'
TE = [
    ('dg-abseihen', 'Milk Washing', 'Milch bindet die Trübstoffe und wird wieder abgefiltert. Was bleibt, ist klar wie Wasser und weich wie Sahne. Momo macht das seit seiner Berliner Zeit, den Milchpunsch gab es schon 2021.'),
    ('dg-behaelter', 'Fat Washing', 'Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel. Kalt gestellt, abgehoben, fertig: Der Rum schmeckt nach Butter, ohne fettig zu sein.'),
    ('dg-giessen', 'Enzyme', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt. So wird aus Apfel oder Birne ein klarer Saft, der sich in einen Drink giessen lässt wie Wasser.'),
]
# Dieselben Sätze in drei Schritten, nur umgestellt, nichts dazu (für das Laborblatt, Fassung 07).
SCHRITTE = [
    ('Milch bindet die Trübstoffe.', 'Dann wird sie wieder abgefiltert.', 'Klar wie Wasser, weich wie Sahne.', 'Seit Momos Berliner Zeit, den Milchpunsch gab es schon 2021.'),
    ('Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel.', 'Kalt gestellt, abgehoben, fertig.', 'Der Rum schmeckt nach Butter, ohne fettig zu sein.', ''),
    ('Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt.', 'Aus Apfel oder Birne wird ein klarer Saft.', 'Er lässt sich in einen Drink giessen wie Wasser.', ''),
]
POS = {'dg-shaker': '45% 35%', 'dg-abseihen': '50% 45%', 'dg-behaelter': '50% 50%', 'dg-giessen': '50% 45%', 'dg-siphon': '50% 40%'}


def img(k, sizes, extra=''):
    p = POS.get(k)
    return B.img_tag(k, sizes, extra=(' style="object-position:%s"' % p if p else '') + extra)


def kachel(k, sizes, cls='', stil=''):
    return '<figure class="kachel %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def foto(k, sizes, cls='foto', stil=''):
    return '<figure class="%s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def p(t, cls='text', i=1):
    return '<p class="%s sw" style="--i:%d">%s</p>' % (cls, i, E(t))


def zitat(i=3, cls=''):
    return '<p class="ge-zitat sw %s" style="--i:%d">%s<small>%s</small></p>' % (cls, i, E(ZITAT), E(WER))


def et(t):
    return '<span class="etikett">%s</span>' % E(t)


def kopf_a(rechts=''):
    return '<div class="g-kopf"><div>%s%s%s</div>%s</div>' % (KZ_A, TITEL_A, p(TEXT_A), rechts)


def kopf_b(rechts=''):
    return '<div class="g-kopf"><div>%s%s%s</div>%s</div>' % (KZ_B, TITEL_B, p(TEXT_B), rechts)


def sek(n, a, b, ueb=True, a_innen=True, b_innen=True):
    """Beide Abschnitte mit den Ids von heute; dazwischen der Satz, der hinüberführt. Gepinnte Bühnen liegen ausserhalb von .innen."""
    ia = '<div class="innen">%s</div>' % a if a_innen else a
    ib = '<div class="innen">%s</div>' % b if b_innen else b
    return ('<section class="kap auf gx v%02d" id="gespraech" data-g="%d">%s%s</section>'
            '<section class="kap auf gx v%02d" id="technik" data-g="%d">%s</section>') % (n, n, ia, B.ueber(UEBERGANG) if ueb else '', n, n, ib)


V = []


# 01 · Quer durch: Der Bereich bleibt stehen, die Fragen und danach die Techniken ziehen als grosse Tafeln von rechts nach links vorbei.
def v01(n):
    def tafel(k, e, t, s=''):
        return '<article class="q-tafel">%s<div class="q-satz">%s<p class="titel">%s</p>%s</div></article>' % (
            kachel(k, '(max-width:760px) 80vw, 34vw'), et(e), E(t), '<p class="text">%s</p>' % E(s) if s else '')
    pin = lambda inhalt: '<div class="q-pin" data-pin><div class="q-buehne"><div class="q-zug">%s</div></div></div>' % inhalt
    a = '<div class="innen">%s</div>%s' % (kopf_a(zitat(2)), pin(''.join(tafel(k, e, f) for k, e, f in FR) + '<article class="q-ende"><p class="titel">%s</p></article>' % E(UEBERGANG)))
    b = '<div class="innen">%s</div>%s' % (kopf_b(), pin(''.join(tafel(k, 'Technik', t, s) for k, t, s in TE)))
    return sek(n, a, b, ueb=False, a_innen=False, b_innen=False)
V.append(('Quer durch', v01))


# 02 · Die Schilder: Momos Fragen hängen wie das Eckschild an der Hausecke, drei schwarze Schilder mit Goldrahmen an Ketten untereinander;
# die Techniken hängen nebeneinander an einer Stange. Beim Auftritt schwingen sie aus.
def v02(n):
    schild = lambda inhalt, j: '<div class="s-schild" style="--n:%d"><div class="s-platte">%s</div></div>' % (j, inhalt)
    a = '<div class="s-a">%s<div>%s%s%s<div class="s-kette vauf">%s</div>%s</div></div>' % (
        kachel('dg-shaker', '(max-width:760px) 100vw, 40vw', 's-bild sw'), KZ_A, TITEL_A, p(TEXT_A),
        ''.join(schild(et(e) + '<p class="titel">%s</p>' % E(f), j) for j, (k, e, f) in enumerate(FR)), zitat(2))
    b = kopf_b() + '<div class="s-stange vauf">%s</div>' % ''.join(
        schild(kachel(k, '(max-width:760px) 90vw, 28vw') + et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s)), j) for j, (k, t, s) in enumerate(TE))
    return sek(n, a, b)
V.append(('Die Schilder', v02))


# 03 · Mit Untertitel: ein hohes Bild in der Mitte, darunter steht die Frage wie ein Untertitel im Film. Beim Scrollen kommt Bild für Bild, Zeile für Zeile.
def v03(n):
    def buehne(ks, zeilen):
        bilder_ = ''.join(foto(k, '(max-width:760px) 90vw, 40vw', 'foto u-b' + (' an' if j == 0 else '')) for j, k in enumerate(ks))
        z = ''.join('<div class="u-z%s">%s</div>' % (' an' if j == 0 else '', x) for j, x in enumerate(zeilen))
        striche = ''.join('<i%s></i>' % (' class="an"' if j == 0 else '') for j in range(len(ks)))
        return '<div class="u-pin" data-pin><div class="u-buehne"><div class="u-rahmen">%s</div><div class="u-unter">%s</div><div class="u-striche">%s</div></div></div>' % (bilder_, z, striche)
    a = '<div class="innen">%s</div>%s' % (kopf_a(zitat(2)), buehne([k for k, e, f in FR], [et(e) + '<p class="titel">%s</p>' % E(f) for k, e, f in FR]))
    b = '<div class="innen">%s</div>%s' % (kopf_b(), buehne([k for k, t, s in TE], [et('Technik') + '<p class="titel">%s</p><p class="text">%s</p>' % (E(t), E(s)) for k, t, s in TE]))
    return sek(n, a, b, a_innen=False, b_innen=False)
V.append(('Mit Untertitel', v03))


# 04 · Der Fächer: drei Bilder liegen zuerst wie ein Fächer in der Hand übereinander und legen sich beim Scrollen nebeneinander, dann erscheinen die Sätze.
def v04(n):
    def faecher(teile):
        return '<div class="f-faecher" data-f>%s</div>' % ''.join(
            '<div class="f-karte" style="--j:%d">%s<div class="f-satz">%s</div></div>' % (j, kachel(k, '(max-width:760px) 90vw, 30vw'), satz) for j, (k, satz) in enumerate(teile))
    a = kopf_a(zitat(2)) + faecher([(k, et(e) + '<p class="titel">%s</p>' % E(f)) for k, e, f in FR])
    b = kopf_b() + faecher([(k, et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s))) for k, t, s in TE])
    return sek(n, a, b)
V.append(('Der Fächer', v04))


# 05 · Platten auf Platten: jede Frage und jede Technik ist eine grosse Platte, die oben stehen bleibt; die nächste schiebt sich darüber, die vorige tritt zurück.
def v05(n):
    def stapel(teile):
        return '<div class="k-stapel" data-k>%s</div>' % ''.join(
            '<article class="k-karte platte" style="--j:%d">%s<div class="k-satz">%s</div></article>' % (j, kachel(k, '(max-width:760px) 90vw, 40vw'), satz) for j, (k, satz) in enumerate(teile))
    a = kopf_a(zitat(2)) + stapel([(k, et(e) + '<p class="titel">%s</p>' % E(f)) for k, e, f in FR])
    b = kopf_b() + stapel([(k, et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s))) for k, t, s in TE])
    return sek(n, a, b)
V.append(('Platten auf Platten', v05))


# 06 · Wort für Wort: jede Frage steht riesig über die Breite, die Wörter gehen beim Scrollen eins nach dem anderen an; daneben das Bild.
def v06(n):
    def worte(t):
        return ' '.join('<span class="w-w">%s</span>' % E(w) for w in t.split())
    a = kopf_a(zitat(2)) + ''.join('<div class="w-block" data-w><div>%s<p class="titel w-gross">%s</p></div>%s</div>' % (
        et(e), worte(f), kachel(k, '(max-width:760px) 60vw, 22vw', 'w-bild')) for k, e, f in FR)
    b = kopf_b() + ''.join('<div class="w-block w-tech" data-w><div>%s<h3 class="titel w-gross">%s</h3><p class="text">%s</p></div>%s</div>' % (
        et('Technik'), worte(t), E(s), kachel(k, '(max-width:760px) 60vw, 22vw', 'w-bild')) for k, t, s in TE)
    return sek(n, a, b)
V.append(('Wort für Wort', v06))


# 07 · Das Laborblatt: Momos Fragen stehen auf einem cremefarbenen Blatt; die Techniken als Protokoll in drei Schritten, Zuerst, Dann, Im Glas.
# Die Goldlinien ziehen sich Schritt für Schritt (Momo hat Biotechnologie studiert).
def v07(n):
    a = '<div class="l-a">%s<div>%s%s%s<div class="l-blatt plakat vauf">%s</div>%s</div></div>' % (
        kachel('dg-coupes', '(max-width:760px) 100vw, 36vw', 'l-bild sw'), KZ_A, TITEL_A, p(TEXT_A),
        ''.join('<div class="l-zeile" style="--n:%d"><i class="l-linie"></i>%s<p class="titel">%s</p></div>' % (j, et(e), E(f)) for j, (k, e, f) in enumerate(FR)), zitat(3))
    def protokoll(j):
        k, t, s = TE[j]
        a1, a2, a3, notiz = SCHRITTE[j]
        schritte = ''.join('<div class="l-schritt" style="--n:%d"><i class="l-linie"></i>%s<p>%s</p></div>' % (i, et(w), E(x)) for i, (w, x) in enumerate(zip(['Zuerst', 'Dann', 'Im Glas'], [a1, a2, a3])))
        return '<article class="l-prot platte vauf">%s<div class="l-rechts">%s<h3 class="titel">%s</h3><div class="l-schritte">%s</div>%s</div></article>' % (
            kachel(k, '(max-width:760px) 90vw, 24vw', 'l-pbild'), et('Technik'), E(t), schritte, '<p class="l-notiz">%s</p>' % E(notiz) if notiz else '')
    b = kopf_b() + ''.join(protokoll(j) for j in range(3))
    return sek(n, a, b)
V.append(('Das Laborblatt', v07))


# 08 · Die Rechnung: Geschmack plus Glas plus das, was hinein soll, ergibt einen Drink. Die Teile rücken beim Scrollen zusammen;
# unten ergeben Milk Washing, Fat Washing und Enzyme zusammen «Klar, weich, sauber.»
def v08(n):
    def rechnung(teile, ergebnis):
        h = ''
        for j, (k, satz) in enumerate(teile):
            if j:
                h += '<span class="m-op titel" data-o>+</span>'
            h += '<div class="m-teil" data-t>%s%s</div>' % (kachel(k, '(max-width:760px) 80vw, 20vw'), satz)
        return '<div class="m-rechnung" data-m>%s<span class="m-op titel" data-o>=</span><div class="m-ergebnis platte hell" data-t>%s</div></div>' % (h, ergebnis)
    a = kopf_a() + rechnung([(k, et(e) + '<p class="titel">%s</p>' % E(f)) for k, e, f in FR],
                            '<p class="titel m-gross">Daraus wird ein Drink.</p><p class="m-zitat">%s<small>%s</small></p>' % (E(ZITAT), E(WER)))
    b = '<div class="g-kopf"><div>%s%s</div></div>' % (KZ_B, p(TEXT_B)) + rechnung(
        [(k, et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s))) for k, t, s in TE], '<h2 class="titel m-gross">Klar, weich, sauber.</h2>')
    return sek(n, a, b, ueb=False)
V.append(('Die Rechnung', v08))


# 09 · Die Drehbühne: ein dreiseitiger Körper steht still im Bild und dreht sich beim Scrollen weiter, jede Seite eine Frage, danach jede Seite eine Technik.
def v09(n):
    def prisma(teile):
        seiten = ''.join('<div class="p-seite platte" style="--j:%d">%s<div class="p-satz">%s</div></div>' % (j, kachel(k, '(max-width:760px) 90vw, 30vw'), satz) for j, (k, satz) in enumerate(teile))
        return '<div class="p-pin" data-pin><div class="p-buehne"><div class="p-prisma">%s</div></div></div>' % seiten
    a = '<div class="innen">%s</div>%s' % (kopf_a(zitat(2)), prisma([(k, et(e) + '<p class="titel">%s</p>' % E(f)) for k, e, f in FR]))
    b = '<div class="innen">%s</div>%s' % (kopf_b(), prisma([(k, et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s))) for k, t, s in TE]))
    return sek(n, a, b, a_innen=False, b_innen=False)
V.append(('Die Drehbühne', v09))


# 10 · Sie stehen auf: Die Platten liegen flach wie auf dem Tresen und richten sich beim Scrollen eine nach der anderen auf.
def v10(n):
    def reihe(teile):
        return '<div class="a-boden">%s</div>' % ''.join(
            '<article class="a-platte platte" data-a><div class="a-satz">%s</div>%s</article>' % (satz, kachel(k, '(max-width:760px) 90vw, 40vw')) for k, satz in teile)
    a = kopf_a(zitat(2)) + reihe([(k, et(e) + '<p class="titel">%s</p>' % E(f)) for k, e, f in FR])
    b = kopf_b() + reihe([(k, et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s))) for k, t, s in TE])
    return sek(n, a, b)
V.append(('Sie stehen auf', v10))


# 11 · Die Fallblatt-Tafel: Fragen und Techniken klappen wie die Blätter einer Anzeigetafel von oben herunter, Zeile für Zeile.
def v11(n):
    zeile = lambda links, rechts, j: '<div class="fb-zeile" style="--n:%d"><div class="fb-links">%s</div><div class="fb-blatt">%s</div></div>' % (j, links, rechts)
    a = '<div class="fb-a"><div>%s%s%s<div class="fb-tafel platte vauf">%s</div></div><div class="fb-rechts">%s%s</div></div>' % (
        KZ_A, TITEL_A, p(TEXT_A), ''.join(zeile(et(e), '<p class="titel">%s</p>' % E(f), j) for j, (k, e, f) in enumerate(FR)),
        kachel('dg-shaker', '(max-width:760px) 100vw, 34vw', 'fb-bild sw'), zitat(3))
    b = '<div class="fb-b">%s<div>%s<div class="fb-tafel platte vauf">%s</div></div></div>' % (
        kachel('dg-giessen', '(max-width:760px) 100vw, 34vw', 'fb-bild sw'), kopf_b(),
        ''.join(zeile('<h3 class="titel">%s</h3>' % E(t), '<p class="text">%s</p>' % E(s), j) for j, (k, t, s) in enumerate(TE)))
    return sek(n, a, b)
V.append(('Die Fallblatt-Tafel', v11))


# 12 · Die Doppelseite: wie ein Bericht im Magazin. Links Momo am Shaker über die ganze Höhe, rechts Initiale, die Fragen im Interview-Ton, der Satz gross zwischen Linien;
# die Techniken in drei Spalten mit Linie, die Bilder im Wechsel oben und unten.
def v12(n):
    a = '<div class="mz-seite"><figure class="mz-bildseite sw">%s<figcaption>Momo am Shaker.</figcaption></figure><div class="mz-text">%s%s<p class="mz-lead sw" style="--i:1">%s</p><div class="mz-fragen staffel">%s</div><blockquote class="mz-zitat sw" style="--i:3"><p class="titel">%s</p><small>%s</small></blockquote></div></div>' % (
        kachel('dg-shaker', '(max-width:760px) 100vw, 46vw'), KZ_A, TITEL_A, E(TEXT_A),
        ''.join('<div style="--n:%d">%s<p class="titel">%s</p></div>' % (j, et(e), E(f)) for j, (k, e, f) in enumerate(FR)), E(ZITAT), E(WER))
    spalte = lambda j: '<div class="mz-spalte%s" style="--n:%d"><i class="mz-regel"></i>%s%s<h3 class="titel">%s</h3><p class="text">%s</p>%s</div>' % (
        ' mz-unten' if j == 1 else '', j, kachel(TE[j][0], '(max-width:760px) 90vw, 28vw') if j != 1 else '', et('Technik'), E(TE[j][1]), E(TE[j][2]),
        kachel(TE[j][0], '(max-width:760px) 90vw, 28vw') if j == 1 else '')
    b = '<div class="mz-b-kopf">%s%s%s</div><div class="mz-spalten staffel">%s</div>' % (KZ_B, TITEL_B, p(TEXT_B, 'text mz-lead'), ''.join(spalte(j) for j in range(3)))
    return sek(n, a, b)
V.append(('Die Doppelseite', v12))


# 13 · Das Wort dahinter: hinter den Platten zieht ein riesiger Schriftzug in feiner Goldlinie langsam durch, oben «Erst die Frage», unten «Klar, weich, sauber.».
def v13(n):
    reihe = lambda teile: '<div class="r-reihe staffel">%s</div>' % ''.join(
        '<article class="r-platte platte" style="--n:%d">%s<div class="r-satz">%s</div></article>' % (j, kachel(k, '(max-width:760px) 90vw, 28vw'), s) for j, (k, s) in enumerate(teile))
    a = '<p class="r-wort titel" aria-hidden="true" data-r="1">Erst die Frage, dann das Glas.</p><div class="innen">%s%s</div>' % (
        kopf_a(zitat(2)), reihe([(k, et(e) + '<p class="titel">%s</p>' % E(f)) for k, e, f in FR]))
    b = '<p class="r-wort titel" aria-hidden="true" data-r="-1">Klar, weich, sauber.</p><div class="innen">%s%s</div>' % (
        kopf_b(), reihe([(k, et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s))) for k, t, s in TE]))
    return sek(n, a, b, a_innen=False, b_innen=False)
V.append(('Das Wort dahinter', v13))


# 14 · Das Regal: wie die Rückbar. Die Bilder steigen hinter einem Regalbrett mit Goldkante herauf, die Fragen und Techniken stehen davor wie Etiketten.
def v14(n):
    def regal(teile):
        faecher = ''.join('<div class="rg-raum"><div class="rg-steig" style="--n:%d">%s</div></div>' % (j, kachel(k, '(max-width:760px) 30vw, 28vw')) for j, (k, s) in enumerate(teile))
        etiketten = ''.join('<div class="rg-etikett" style="--n:%d">%s</div>' % (j, s) for j, (k, s) in enumerate(teile))
        return '<div class="rg-regal vauf"><div class="rg-faecher">%s</div><div class="rg-brett"></div><div class="rg-etiketten">%s</div></div>' % (faecher, etiketten)
    a = kopf_a(zitat(2)) + regal([(k, et(e) + '<p class="titel">%s</p>' % E(f)) for k, e, f in FR])
    b = kopf_b() + regal([(k, et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s))) for k, t, s in TE])
    return sek(n, a, b)
V.append(('Das Regal', v14))


# 15 · Es wird klar: Die Bilder kommen trüb und gedeckt herein und werden beim Scrollen klar, wie ein Drink nach dem Milk Washing.
def v15(n):
    def klar(k, sizes, cls=''):
        trueb = img(k, sizes, ' class="kw-trueb" aria-hidden="true"').replace(' alt="%s"' % E(mache(k)['alt']), ' alt=""', 1)
        return '<figure class="kw-bild %s" data-kw style="--lq:url(%s)">%s%s</figure>' % (cls, mache(k)['lq'], img(k, sizes), trueb)
    a = '<div class="kw-a">%s<div>%s%s%s<div class="kw-liste staffel">%s</div>%s</div></div>' % (
        klar('dg-shaker', '(max-width:760px) 100vw, 44vw'), KZ_A, TITEL_A, p(TEXT_A),
        ''.join('<div style="--n:%d">%s<p class="titel">%s</p></div>' % (j, et(e), E(f)) for j, (k, e, f) in enumerate(FR)), zitat(3))
    b = kopf_b() + '<div class="kw-spalten">%s</div>' % ''.join(
        '<div class="kw-sp">%s%s<h3 class="titel">%s</h3><p class="text">%s</p></div>' % (klar(k, '(max-width:760px) 90vw, 30vw'), et('Technik'), E(t), E(s)) for k, t, s in TE)
    return sek(n, a, b)
V.append(('Es wird klar', v15))


# 16 · Eingeschenkt: drei hohe Gläser mit feinem Goldrand; das Bild steigt beim Scrollen darin auf wie ein Drink, eine Goldlinie zeigt den Pegel.
def v16(n):
    def glaeser(teile, oben):
        return '<div class="e-reihe">%s</div>' % ''.join(
            '<div class="e-sp">%s<div class="e-glas" data-e style="--j:%d"><div class="e-fuell"><div class="e-gegen">%s</div></div></div>%s</div>' % (
                s if oben else '', j, kachel(k, '(max-width:760px) 90vw, 30vw'), '' if oben else s) for j, (k, s) in enumerate(teile))
    a = kopf_a(zitat(2)) + glaeser([(k, '<div class="e-satz">%s<p class="titel">%s</p></div>' % (et(e), E(f))) for k, e, f in FR], True)
    b = kopf_b() + glaeser([(k, '<div class="e-satz">%s<h3 class="titel">%s</h3><p class="text">%s</p></div>' % (et('Technik'), E(t), E(s))) for k, t, s in TE], False)
    return sek(n, a, b)
V.append(('Eingeschenkt', v16))


# 17 · Rund um das Bild: ein grosses Bild steht in der Mitte, die Sätze stehen links und rechts daneben; feine Goldlinien ziehen sich vom Bild zu jedem Satz.
def v17(n):
    def satz(inhalt, seite, j):
        return '<div class="u2-satz u2-%s" style="--n:%d"><i class="u2-linie"></i>%s</div>' % (seite, j, inhalt)
    a = '<div class="u2 vauf"><div class="u2-sp u2-l">%s%s</div>%s<div class="u2-sp u2-r">%s</div></div>' % (
        '<div>%s%s%s</div>' % (KZ_A, TITEL_A, p(TEXT_A)), satz('<p class="ge-zitat">%s<small>%s</small></p>' % (E(ZITAT), E(WER)), 'l', 3),
        kachel('dg-shaker', '(max-width:760px) 100vw, 34vw', 'u2-bild'),
        ''.join(satz(et(e) + '<p class="titel">%s</p>' % E(f), 'r', j) for j, (k, e, f) in enumerate(FR)))
    t = lambda j, seite: satz(et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(TE[j][1]), E(TE[j][2])), seite, j)
    b = '<div class="u2 u2-b vauf"><div class="u2-sp u2-l">%s%s</div>%s<div class="u2-sp u2-r">%s%s</div></div>' % (
        '<div>%s%s%s</div>' % (KZ_B, TITEL_B, p(TEXT_B)), t(0, 'l'), kachel('dg-giessen', '(max-width:760px) 100vw, 34vw', 'u2-bild'), t(1, 'r'), t(2, 'r'))
    return sek(n, a, b)
V.append(('Rund um das Bild', v17))


# 18 · Die Bilderwand: Bilder in Rahmen mit Passepartout, eng gehängt wie in einem Salon, dazwischen die Fragen und Techniken auf kleinen cremefarbenen Karten.
def v18(n):
    rahmen = lambda k, area, j: '<div class="sa-rahmen" style="grid-area:%s;--n:%d">%s</div>' % (area, j, foto(k, '(max-width:760px) 90vw, 30vw'))
    karte = lambda inhalt, area, j: '<div class="sa-karte" style="grid-area:%s;--n:%d">%s</div>' % (area, j, inhalt)
    a = kopf_a(zitat(2)) + '<div class="sa-wand sa-wa vauf">%s%s%s%s%s%s%s</div>' % (
        rahmen('dg-shaker', 'f1', 0), karte(et(FR[0][1]) + '<p class="titel">%s</p>' % E(FR[0][2]), 'q1', 1), rahmen('dg-coupes', 'f2', 2),
        rahmen('dg-flaschen', 'f3', 3), karte(et(FR[1][1]) + '<p class="titel">%s</p>' % E(FR[1][2]), 'q2', 4), rahmen('dg-coupes-hand', 'f4', 5),
        karte(et(FR[2][1]) + '<p class="titel">%s</p>' % E(FR[2][2]), 'q3', 6))
    tk = lambda j, area, n_: karte(et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(TE[j][1]), E(TE[j][2])), area, n_)
    b = kopf_b() + '<div class="sa-wand sa-wb vauf">%s%s%s%s%s%s</div>' % (
        rahmen(TE[0][0], 'f1', 0), tk(0, 't1', 1), rahmen(TE[1][0], 'f2', 2), tk(2, 't3', 3), rahmen(TE[2][0], 'f3', 4), tk(1, 't2', 5))
    return sek(n, a, b)
V.append(('Die Bilderwand', v18))


# 19 · Zum Umblättern: ein aufgeschlagenes Heft auf Creme. Beim Scrollen wenden sich die Seiten, vorn steht die Frage, auf der Rückseite das Bild.
def v19(n):
    def heft(links, blaetter, letzte):
        b_ = ''.join('<div class="h-blatt" style="--j:%d"><div class="h-vorn">%s</div><div class="h-hinten">%s</div></div>' % (
            j, vorn, foto(k, '(max-width:760px) 90vw, 36vw')) for j, (vorn, k) in enumerate(blaetter))
        return '<div class="h-pin" data-pin><div class="h-buehne"><div class="h-heft"><div class="h-links">%s</div><div class="h-rechts">%s</div>%s</div></div></div>' % (links, letzte, b_)
    a = heft('%s%s<p class="text">%s</p>' % (KZ_A, TITEL_A, E(TEXT_A)), [(et(e) + '<p class="titel h-frage">%s</p>' % E(f), k) for k, e, f in FR],
             '<p class="titel h-frage">%s</p><small class="h-wer">%s</small>' % (E(ZITAT), E(WER)))
    b = heft('%s%s<p class="text">%s</p>' % (KZ_B, TITEL_B, E(TEXT_B)), [(et('Technik') + '<h3 class="titel">%s</h3><p class="text">%s</p>' % (E(t), E(s)), k) for k, t, s in TE],
             '<p class="titel h-frage">Klar, weich, sauber.</p>')
    return sek(n, a, b, a_innen=False, b_innen=False)
V.append(('Zum Umblättern', v19))


# 20 · Bilder in der Zeile: die Fragen und die Namen der Techniken stehen riesig, mitten in der Zeile öffnet sich ein kleines Bild.
def v20(n):
    def mit_bild(t, k, nach):
        w = t.split()
        return ' '.join(w[:nach]) + ' <span class="z-bild" data-z style="--lq:url(%s)">%s</span> ' % (mache(k)['lq'], img(k, '220px')) + ' '.join(w[nach:])
    a = kopf_a(zitat(2)) + ''.join('<div class="z-zeile">%s<p class="titel z-gross">%s</p></div>' % (et(e), mit_bild(f, k, nach))
                                   for (k, e, f), nach in zip(FR, [1, 1, 2]))
    b = kopf_b() + ''.join('<div class="z-zeile z-tech"><div>%s<h3 class="titel z-gross">%s</h3></div><p class="text">%s</p></div>' % (et('Technik'), mit_bild(t, k, 1), E(s))
                           for k, t, s in TE)
    return sek(n, a, b)
V.append(('Bilder in der Zeile', v20))


def seite(n):
    h = unter.drinks()
    if n:
        a = h.rfind('<section', 0, h.find('id="gespraech"'))
        b = h.find('</section>', h.find('id="technik"')) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
