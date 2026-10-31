# Walk on the Wild Side · Drinks-Seite, Abschnitt «Die einzige Karte» (id karte): 20 Darstellungen (30.10.2026).
# Robert: «Gib mir 20 verschiedene Visualisierungsmöglichkeiten für einen Abschnitt.» (Bildschirmfoto des Abschnitts).
# Texte nur aus dem heutigen Abschnitt (Absatz, vier Drinks, Hinweis, Knopf), nichts dazu. Plakat nie als Hauptbild (CHARAKTER.md 3);
# das Foto der Karte 2023 ist ein Foto vom Tisch. Je Fassung eine eigene Anordnung und eine eigene Bewegung, nur transform und opacity.
# 00 = heutiger Stand. Wechsel mit ← →. Aufruf: python3 _varianten/karte-20/bau.py → 00.html … 20.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/karte-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))
bilder.BILDER.update({
    'karte-2023': ('ig/2023-12-07_walkonthewildside_hannover_C0j1thbsh_y-1.jpg', 'Momos Signature Drinks auf einer Karte am Tisch, daneben ein Windlicht, Dezember 2023'),
})

KZ = B.kz('Eine Karte im Jahr', 'Valentinstag', 0)
TITEL = B.h2(['Die einzige Karte.'])
S1 = 'Einmal im Jahr gibt es doch eine Karte: zum Valentinstag, zusammen mit Rudi von Culinarium.'
S2 = '2026 hiess sie «Drunk in Love», vier Drinks zu je zwölf Euro, dazu Teller zum Teilen.'
S3 = 'Zum Weihnachtsfest 2023 standen Momos erste Signature Drinks auf einem Blatt: Linden Mule, Sakura, Mary Bramble, Ambré, Clean Pornstar, Zauberwald.'
TEXT = ' '.join([S1, S2, S3])
ETI = 'Valentinstag 2026 · Wild Side x Rudi in Love'
NAME = 'Drunk in Love.'
HINWEIS = 'Preise vom Plakat zum 14. Februar 2026. An allen anderen Abenden gibt es keine Karte.'
KARTE = [('Frensh 26', ['Gin', 'Bergamotte', 'Nori', 'Schaumwein']), ('Whey Bramble', ['Gin', 'Lemon Shrub', 'Vetiver', 'Whey Berry Soda']),
         ('Pink Lady', ['Kakaobutter-Fat-Washed Rum', 'Himbeerpüree', 'Agave', 'Limette']),
         ('Karamella', ['Havana 7 Jahre', 'Portwein', 'Johannisbeere', 'Karamell', 'schwarze Walnüsse', 'Limette'])]
SIG23 = ['Linden Mule', 'Sakura', 'Mary Bramble', 'Ambré', 'Clean Pornstar', 'Zauberwald']
PREIS = '12 €'
KNOPF = B.knopf('Platz reservieren', 'besuch.html#reservieren', 'rot')


def z(xs):
    return ' · '.join(xs)


def p(t, cls='text', i=1):
    return '<p class="%s sw" style="--i:%d">%s</p>' % (cls, i, E(t))


def et(t=ETI, cls=''):
    return '<span class="etikett %s">%s</span>' % (cls, E(t))


def knoepfe(i=2):
    return '<div class="knoepfe sw" style="--i:%d">%s</div>' % (i, KNOPF)


def klein(i=3):
    return '<small class="k-hinweis sw" style="--i:%d">%s</small>' % (i, E(HINWEIS))


def kopf(text=True, i=1):
    return KZ + TITEL + (p(TEXT, i=i) if text else '')


def foto(k, sizes, cls='foto', stil=''):
    return B.bild(k, cls, sizes, stil=stil)


def posten(cls='posten'):
    """Die Liste wie heute: Name, Preis, Zutaten."""
    return '<div class="%s">%s</div>' % (cls, ''.join('<div style="--n:%d"><b>%s</b><span>%s</span><p>%s</p></div>' % (n, E(t), PREIS, E(z(zs))) for n, (t, zs) in enumerate(KARTE)))


def sek(n, inhalt, cls='', innen=True):
    return '<section class="kap auf kx v%02d %s" id="karte" data-k="%d">%s</section>' % (n, cls, n, '<div class="innen">%s</div>' % inhalt if innen else inhalt)


V = []


# 01 · In Rosa: das Blatt in den Farben der Valentinskarte (Rosa, Rot), es legt sich beim Auftritt aus der Schräge flach auf den Tisch.
def v01(n):
    blatt = '<div class="r-blatt vauf">%s<h3 class="titel">%s</h3>%s<small>%s</small></div>' % (et(), E(NAME), posten(), E(HINWEIS))
    return sek(n, '<div class="k-zwei"><div>%s%s</div><div class="r-tisch">%s</div></div>' % (kopf(), knoepfe(), blatt))
V.append(('In Rosa', v01))


# 02 · Zwei Karten: links das Foto der Karte von 2023 am Tisch, rechts das Blatt von 2026; über beiden das Jahr. Sie kommen nacheinander von unten.
def v02(n):
    links = '<div class="zk-sp sw" style="--i:2"><span class="zk-jahr titel">2023</span>%s<p class="text">%s</p></div>' % (foto('karte-2023', '(max-width:760px) 92vw, 34vw', 'kachel'), E(S3))
    rechts = '<div class="zk-sp sw" style="--i:3"><span class="zk-jahr titel">2026</span><div class="blatt">%s<h3 class="titel">%s</h3>%s<small>%s</small></div></div>' % (et(), E(NAME), posten(), E(HINWEIS))
    return sek(n, '<div class="zk-kopf"><div>%s%s</div><div>%s%s</div></div><div class="zk-zwei">%s%s</div>' % (KZ, TITEL, p(S1 + ' ' + S2), knoepfe(), links, rechts))
V.append(('Zwei Karten', v02))


# 03 · Die Namen gross: jeder Drink steht über die ganze Breite in grosser Schrift, Zutaten und Preis rechts daneben; die Zeilen steigen nacheinander aus dem Schlitz.
def v03(n):
    zeilen = ''.join('<div class="ng-z" style="--n:%d"><span class="ng-name titel"><span>%s</span></span><span class="ng-zu">%s</span><span class="ng-p">%s</span></div>' % (
        j, E(t), E(z(zs)), PREIS) for j, (t, zs) in enumerate(KARTE))
    return sek(n, '<div class="ng-kopf"><div>%s%s</div><div>%s%s</div></div>%s<div class="ng-liste vauf">%s</div>%s' % (
        KZ, TITEL, p(TEXT), knoepfe(), et(ETI, 'sw ng-et'), zeilen, klein()))
V.append(('Die Namen gross', v03))


# 04 · Einer nach dem anderen: Der Abschnitt bleibt stehen, beim Scrollen kommt Drink für Drink in die Mitte; links steht der Text still.
def v04(n):
    drinks = ''.join('<div class="e-d%s"><span class="etikett">%s</span><p class="e-name titel">%s</p><p class="e-zu">%s</p></div>' % (
        ' an' if j == 0 else '', PREIS, E(t), E(z(zs))) for j, (t, zs) in enumerate(KARTE))
    striche = ''.join('<i%s></i>' % (' class="an"' if j == 0 else '') for j in range(len(KARTE)))
    return sek(n, '<div class="e-pin" data-pin><div class="e-buehne"><div class="innen e-raster"><div>%s%s%s</div><div class="e-blatt">%s<p class="titel e-titel">%s</p><div class="e-stage">%s</div><div class="e-striche">%s</div><small>%s</small></div></div></div></div>' % (
        kopf(), knoepfe(), '', et(), E(NAME), drinks, striche, E(HINWEIS)), innen=False)
V.append(('Einer nach dem anderen', v04))


# 05 · Die Karte dreht sich: vorn nur der Name der Karte, beim Scrollen wendet sie sich, hinten stehen die vier Drinks.
def v05(n):
    karte = '<div class="d-raum" data-dreh><div class="d-karte"><div class="d-vorn">%s<p class="titel">%s</p><span class="d-datum">14. Februar 2026</span></div><div class="d-hinten">%s%s<small>%s</small></div></div></div>' % (
        et(), E(NAME), '<h3 class="titel">%s</h3>' % E(NAME), posten(), E(HINWEIS))
    return sek(n, '<div class="k-zwei"><div>%s%s</div>%s</div>' % (kopf(), knoepfe(), karte))
V.append(('Die Karte dreht sich', v05))


# 06 · Am Tisch: das Foto der Karte von 2023 randlos über die halbe Breite, die Karte von 2026 als Schrift direkt auf der Nacht daneben.
def v06(n):
    return sek(n, '<div class="t-raster">%s<div class="t-rechts">%s%s<div class="t-liste staffel">%s</div>%s%s</div></div>' % (
        foto('karte-2023', '(max-width:760px) 100vw, 50vw', 'foto t-bild'), kopf(), et(ETI, 'sw t-et'),
        ''.join('<div style="--n:%d"><p class="titel">%s <span>%s</span></p><p>%s</p></div>' % (j, E(t), PREIS, E(z(zs))) for j, (t, zs) in enumerate(KARTE)),
        klein(), knoepfe(3)), innen=False)
V.append(('Am Tisch', v06))


# 07 · Wie eine Speisekarte: alles mittig, Punktlinie vom Namen zum Preis, Zutaten darunter; Zeile für Zeile.
def v07(n):
    zeilen = ''.join('<div style="--n:%d"><p class="sk-zeile"><b class="titel">%s</b><i></i><span>%s</span></p><p class="sk-zu">%s</p></div>' % (
        j, E(t), PREIS, E(z(zs))) for j, (t, zs) in enumerate(KARTE))
    return sek(n, '<div class="sk-mitte">%s%s%s<div class="sk-karte">%s<p class="titel sk-name sw" style="--i:2">%s</p><div class="sk-liste staffel">%s</div>%s</div>%s</div>' % (
        KZ, TITEL, p(TEXT), et(ETI, 'sw'), E(NAME), zeilen, klein(), knoepfe(4)))
V.append(('Wie eine Speisekarte', v07))


# 08 · Das Querblatt: ein breites cremefarbenes Blatt, zwei Drinks links, zwei rechts; es liegt erst schräg und richtet sich gerade.
def v08(n):
    blatt = '<div class="qb vauf"><div class="qb-kopf">%s<h3 class="titel">%s</h3></div>%s<small>%s</small></div>' % (et(), E(NAME), posten('posten qb-posten'), E(HINWEIS))
    return sek(n, '<div class="qb-oben"><div>%s%s</div><div>%s%s</div></div>%s' % (KZ, TITEL, p(TEXT), knoepfe(), blatt))
V.append(('Das Querblatt', v08))


# 09 · 2023 und 2026: zwei grosse Jahreszahlen in Gold, darunter je die Namen der Drinks; die Zahlen steigen, die Namen folgen.
def v09(n):
    sp = lambda jahr, satz, namen, i: '<div class="jz-sp"><span class="jz-jahr titel sw" style="--i:%d">%s</span>%s<div class="jz-namen staffel">%s</div></div>' % (
        i, jahr, '<p class="text sw" style="--i:%d">%s</p>' % (i + 1, E(satz)), namen)
    n23 = ''.join('<p class="titel" style="--n:%d">%s</p>' % (j, E(x)) for j, x in enumerate(SIG23))
    n26 = ''.join('<p class="titel" style="--n:%d">%s<span>%s · %s</span></p>' % (j, E(t), PREIS, E(z(zs))) for j, (t, zs) in enumerate(KARTE))
    return sek(n, '<div class="jz-kopf"><div>%s%s</div><div>%s%s</div></div><div class="jz-zwei">%s%s</div>%s' % (
        KZ, TITEL, p(S1), knoepfe(), sp('2026', S2, n26, 2), sp('2023', S3, n23, 3), klein(5)))
V.append(('2023 und 2026', v09))


# 10 · Es wird rosa: Beim Hereinscrollen färbt sich der ganze Abschnitt in das Rosa der Valentinskarte, Schrift dunkel und rot.
def v10(n):
    return sek(n, '<div class="rs-grund" data-rosa></div><div class="innen rs-innen"><div class="k-zwei"><div>%s%s</div><div class="rs-liste">%s<h3 class="titel">%s</h3>%s<small>%s</small></div></div></div>' % (
        kopf(), knoepfe(), et(), E(NAME), posten(), E(HINWEIS)), innen=False)
V.append(('Es wird rosa', v10))


# 11 · Das Bild bleibt stehen: links randlos ein Drink über die volle Höhe, er bleibt stehen, rechts ziehen Text und die vier Drinks vorbei.
def v11(n):
    return sek(n, '<div class="bs-raster"><div class="bs-links"><div class="bs-steh">%s</div></div><div class="bs-rechts">%s%s<div class="bs-liste">%s<h3 class="titel">%s</h3>%s<small>%s</small></div></div></div>' % (
        foto('glas-coupe', '(max-width:760px) 100vw, 50vw', 'foto bs-bild'), kopf(), knoepfe(),
        et(), E(NAME), ''.join('<div class="bs-d vauf"><p class="titel">%s</p><span>%s</span><p>%s</p></div>' % (E(t), PREIS, E(z(zs))) for t, zs in KARTE), E(HINWEIS)), innen=False)
V.append(('Das Bild bleibt stehen', v11))


# 12 · Wie im Magazin: der Text in zwei Spalten mit grosser Initiale, die Karte als Kasten zwischen zwei Goldlinien daneben.
def v12(n):
    return sek(n, '%s%s<div class="mg-raster"><div class="mg-text sw" style="--i:1"><p class="text"><span class="mg-ini titel">E</span>%s</p></div><aside class="mg-kasten sw" style="--i:2">%s<h3 class="titel">%s</h3>%s<small>%s</small></aside></div>%s' % (
        KZ, TITEL, E(TEXT[1:]), et(), E(NAME), posten(), E(HINWEIS), knoepfe(3)))
V.append(('Wie im Magazin', v12))


# 13 · Der 14.: das Datum des Abends riesig in Gold, daneben die Karte; die Zahl steigt langsam, die Karte folgt.
def v13(n):
    return sek(n, '<div class="dt-oben">%s%s</div><div class="dt-raster"><div class="dt-datum vauf"><span class="titel">14.</span><span class="etikett">Februar 2026</span></div><div class="dt-rechts">%s<div class="dt-liste staffel">%s</div>%s%s</div></div>' % (
        KZ, TITEL, p(TEXT), ''.join('<div style="--n:%d"><p class="titel">%s</p><span>%s</span><p>%s</p></div>' % (j, E(t), PREIS, E(z(zs))) for j, (t, zs) in enumerate(KARTE)),
        klein(), knoepfe(4)))
V.append(('Der 14.', v13))


# 14 · In einem Fluss: die vier Drinks als ein durchgehender Absatz, Namen gross, Zutaten klein in Gold dazwischen; Wort für Wort setzt er sich.
def v14(n):
    fluss = ''.join('<span class="fl-d" style="--n:%d"><b class="titel">%s</b> <span class="fl-zu">%s · %s</span></span> ' % (j, E(t), E(z(zs)), PREIS) for j, (t, zs) in enumerate(KARTE))
    return sek(n, '<div class="fl-oben"><div>%s%s</div><div>%s%s</div></div>%s<p class="fl-fluss vauf">%s</p>%s' % (
        KZ, TITEL, p(TEXT), knoepfe(), et(ETI + ' · ' + NAME[:-1], 'sw'), fluss, klein()))
V.append(('In einem Fluss', v14))


# 15 · Vier Platten: jeder Drink auf einer eigenen dunklen Platte mit Goldlinie wie das Eckschild, zwei mal zwei; sie schweben nacheinander herein.
def v15(n):
    platten = ''.join('<div class="pl-p" style="--n:%d"><span class="pl-preis titel">%s</span><p class="titel">%s</p><p class="pl-zu">%s</p></div>' % (
        j, PREIS, E(t), '<br>'.join(E(x) for x in zs)) for j, (t, zs) in enumerate(KARTE))
    return sek(n, '<div class="k-zwei pl-raster"><div>%s%s%s%s</div><div class="pl-gitter staffel">%s</div></div>' % (
        kopf(), et(ETI, 'sw pl-et'), knoepfe(3), klein(4), platten))
V.append(('Vier Platten', v15))


# 16 · Drei Felder: Wand an Wand das Foto der Karte von 2023, in der Mitte die Karte von 2026 auf Creme, rechts ein Drink; gleich hoch.
def v16(n):
    mitte = '<div class="tr-mitte">%s<h3 class="titel">%s</h3>%s<small>%s</small></div>' % (et(), E(NAME), posten(), E(HINWEIS))
    return sek(n, '<div class="tr-oben"><div>%s%s</div><div>%s%s</div></div><div class="tr-wand vauf">%s%s%s</div>' % (
        KZ, TITEL, p(TEXT), knoepfe(), foto('karte-2023', '(max-width:760px) 100vw, 30vw', 'foto tr-b'), mitte, foto('glas-rot', '(max-width:760px) 100vw, 30vw', 'foto tr-b')))
V.append(('Drei Felder', v16))


# 17 · Vier Säulen: jeder Drink eine schmale Spalte zwischen feinen Goldlinien, Zutaten untereinander, der Preis unten; die Spalten wachsen von unten.
def v17(n):
    sae = ''.join('<div class="sa-s" style="--n:%d"><p class="titel">%s</p><ul>%s</ul><span class="sa-p titel">%s</span></div>' % (
        j, E(t), ''.join('<li>%s</li>' % E(x) for x in zs), PREIS) for j, (t, zs) in enumerate(KARTE))
    return sek(n, '<div class="sa-oben"><div>%s%s</div><div>%s%s</div></div><div class="sa-kopf sw" style="--i:2">%s<p class="titel">%s</p></div><div class="sa-reihe vauf">%s</div>%s' % (
        KZ, TITEL, p(TEXT), knoepfe(), et(), E(NAME), sae, klein()))
V.append(('Vier Säulen', v17))


# 18 · Der Satz gross: der Absatz selbst wird zur Hauptsache, gross gesetzt über die Breite; die Karte als eine Zeile darunter.
def v18(n):
    zeile = ''.join('<div style="--n:%d"><b class="titel">%s</b><span>%s</span><p>%s</p></div>' % (j, E(t), PREIS, E(z(zs))) for j, (t, zs) in enumerate(KARTE))
    return sek(n, '%s%s<div class="sg-satz">%s%s%s</div><div class="sg-unten">%s<div class="sg-zeile staffel">%s</div>%s%s</div>' % (
        KZ, TITEL, p(S1, 'titel sg-t', 1), p(S2, 'titel sg-t', 2), p(S3, 'text sg-k', 3), et(ETI, 'sw'), zeile, klein(), knoepfe(4)))
V.append(('Der Satz gross', v18))


# 19 · Der Name bleibt stehen: links steht «Drunk in Love.» gross und bleibt beim Scrollen stehen, rechts ziehen Text und Drinks vorbei.
def v19(n):
    return sek(n, '<div class="ns-raster"><div class="ns-links"><div class="ns-steh">%s%s%s<p class="titel ns-name">%s</p></div></div><div class="ns-rechts">%s<div class="ns-liste">%s</div>%s%s</div></div>' % (
        KZ, TITEL, et(ETI), E(NAME), p(TEXT),
        ''.join('<div class="ns-d vauf"><span class="etikett">%s</span><p class="titel">%s</p><p>%s</p></div>' % (PREIS, E(t), E(z(zs))) for t, zs in KARTE), klein(), knoepfe(4)))
V.append(('Der Name bleibt stehen', v19))


# 20 · Bilder und Karte: oben ein Band aus drei Bildern Wand an Wand, das sich beim Auftritt aus der Nähe setzt; darunter die vier Drinks in einer Reihe.
def v20(n):
    reihe = ''.join('<div style="--n:%d"><p class="titel">%s</p><span>%s</span><p>%s</p></div>' % (j, E(t), PREIS, E(z(zs))) for j, (t, zs) in enumerate(KARTE))
    band = '<div class="bk-band">%s%s%s</div>' % (foto('glas-coupe', '(max-width:760px) 100vw, 34vw', 'foto bk-b'), foto('karte-2023', '(max-width:760px) 100vw, 34vw', 'foto bk-b'),
                                                  foto('glas-kerze', '(max-width:760px) 100vw, 34vw', 'foto bk-b'))
    return sek(n, '<div class="innen bk-oben"><div>%s%s</div><div>%s%s</div></div>%s<div class="innen">%s<p class="titel bk-name sw" style="--i:2">%s</p><div class="bk-reihe staffel">%s</div>%s</div>' % (
        KZ, TITEL, p(TEXT), knoepfe(), band, et(ETI, 'sw'), E(NAME), reihe, klein()), innen=False)
V.append(('Bilder und Karte', v20))


def seite(n):
    h = unter.drinks()
    if n:
        a = h.rfind('<section', 0, h.find('id="karte"'))
        b = h.find('</section>', a) + len('</section>')
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
