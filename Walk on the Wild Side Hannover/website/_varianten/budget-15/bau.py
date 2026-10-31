# Walk on the Wild Side · Feiern-Seite, Abschnitt «Weg 2 · Budget · Ein Rahmen, den ihr setzt.» (id="budget"): 15 Darstellungen (30.10.2026).
# Robert: «gib 15 visuelle alternative darstellungsmöglchkeiten von dem abschnitt». 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte und Preise Wort für Wort aus unter.tafel() / unter.PREISE, nur echte Fotos.
# Bewegung nur über transform und opacity, Auftritt über die .auf/.da-Wache der Seite, Scroll-Getriebenes in einem Takt in b.js. Wechsel mit ← →.
# Aufruf: python3 _varianten/budget-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/budget-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('b.css', 'b.js', 'nav.js'))))

TEXT = 'Für Service und Raum gibt es einen festen Betrag, für die Drinks setzt ihr vorher einen Rahmen. Ist er erreicht, stockt ihr auf, oder eure Gäste übernehmen ihre weiteren Bestellungen selbst. So bleibt der Abend offen und die Rechnung klar.'
KLEIN = 'Geschlossene Gesellschaft ab 30 Personen, 19 bis 2 Uhr. Das Budget lässt sich nach oben frei anpassen.'
HINWEIS = 'Gilt für das Budget an der langen Tafel und in der ganzen Bar. Alle Preise brutto.'
PREISE = unter.PREISE
_q = open('unter.py').read()
for _t in (TEXT, KLEIN, HINWEIS, 'Service und Raum', 'Euer Budget für Drinks', '500 €', 'ab 1.000 €', 'Was ein Drink kostet', 'Die Preise der Bar.'):
    assert _t in _q, 'Text weicht ab: ' + _t


def kopf(cls='', i0=0):
    return '<div class="bk %s">%s%s<p class="text sw" style="--i:%d">%s</p></div>' % (
        cls, B.kz('Weg 2 · Budget', 'Flexibel mit festem Rahmen', i0), B.h2(['Ein Rahmen,', 'den ihr setzt.']), i0 + 1, E(TEXT))


def klein(cls=''):
    return '<p class="bklein %s">%s</p>' % (cls, E(KLEIN))


def hinweis(cls=''):
    return '<small class="bhin %s">%s</small>' % (cls, E(HINWEIS))


def listenkopf(cls=''):
    return '<span class="etikett %s">Was ein Drink kostet</span><h3 class="titel bltitel">Die Preise der Bar.</h3>' % cls


def posten(cls='bp', linie=True):
    return ''.join('<div class="%s" style="--n:%d"><span>%s</span>%s<b class="titel">%s €</b></div>' % (
        cls, n, E(t), '<i></i>' if linie else '', p) for n, (t, p) in enumerate(PREISE))


def fo(k, sizes, cls='', pos='50% 50%'):
    return '<figure class="bf %s" style="--lq:url(%s)">%s</figure>' % (cls, mache(k)['lq'], B.img_tag(k, sizes, extra=' style="object-position:%s"' % pos))


def sek(n, inner, hell=True):
    return '<section class="kap%s auf bv b%02d" id="budget" data-b="%d"><div class="innen">%s</div></section>' % (' hell' if hell else '', n, n, inner)


SERVICE = ('Service und Raum', '500 €')
BUDGET = ('Euer Budget für Drinks', 'ab 1.000 €')
V = []


# 01 · Die Waage: links der Text, rechts eine Waage aus zwei Schalen, Service und Raum gegen euer Budget.
# Der Balken kommt schief herein und pendelt sich gerade ein; darunter die Preise als schmale Leiste.
def v01(n):
    schale = lambda e, z, c: '<div class="w1-schale %s"><i class="w1-kette"></i><div class="w1-teller"><span class="etikett">%s</span><b class="titel">%s</b></div></div>' % (c, E(e), E(z))
    waage = '<div class="w1-waage auf"><i class="w1-saeule"></i><div class="w1-balken">%s%s</div></div>' % (schale(*SERVICE, 'l'), schale(*BUDGET, 'r'))
    leiste = '<div class="w1-leiste auf">%s<div class="w1-reihe">%s</div>%s</div>' % (listenkopf(), posten('w1-p', False), hinweis())
    return sek(n, '<div class="w1-raster">%s%s</div>%s%s' % (kopf(), waage, klein('w1-klein'), leiste))
V.append(('Die Waage', v01))


# 02 · Die Rechnungsmappe: eine dunkle Mappe wie am Tisch; der Deckel klappt auf, innen links die beiden Beträge,
# rechts die Preise der Bar. Text darüber, mittig.
def v02(n):
    links = '<div class="m2-seite m2-l">%s<i class="m2-plus">+</i>%s%s</div>' % (
        '<div class="m2-betrag"><span>%s</span><b class="titel">%s</b></div>' % SERVICE,
        '<div class="m2-betrag"><span>%s</span><b class="titel">%s</b></div>' % BUDGET, klein())
    rechts = '<div class="m2-seite m2-r">%s<div class="m2-posten">%s</div>%s</div>' % (listenkopf(), posten(), hinweis())
    mappe = '<div class="m2-mappe auf"><div class="m2-innen">%s%s</div><div class="m2-deckel"><span class="titel">Walk on the Wild Side</span><i></i></div></div>' % (links, rechts)
    return sek(n, kopf('m2-kopf') + mappe, hell=True)
V.append(('Die Rechnungsmappe', v02))


# 03 · Das Glas füllt sich: ein grosses gezeichnetes Glas, an der Kante eine Goldmarke «ab 1.000 €».
# Beim Scrollen steigt der Drink bis zur Marke; neben dem Glas die Preise als Füllstriche von oben nach unten.
def v03(n):
    glas = '''<div class="g3-glas" data-fuell><svg viewBox="0 0 200 300" aria-hidden="true"><defs><clipPath id="g3c"><path d="M30 20 L170 20 L150 280 L50 280 Z"/></clipPath></defs>
<g clip-path="url(#g3c)"><rect class="g3-drink" x="0" y="20" width="200" height="260"/></g><path class="g3-rand" d="M30 20 L170 20 L150 280 L50 280 Z"/><line class="g3-marke" x1="22" y1="78" x2="178" y2="78"/></svg>
<p class="g3-mtext"><span class="etikett">Euer Budget für Drinks</span><b class="titel">ab 1.000 €</b></p><p class="g3-boden"><span class="etikett">Service und Raum</span><b class="titel">500 €</b></p></div>'''
    liste = '<div class="g3-liste auf">%s<div class="g3-posten">%s</div>%s</div>' % (listenkopf(), posten(), hinweis())
    return sek(n, '<div class="g3-raster"><div>%s%s</div>%s%s</div>' % (kopf(), klein(), glas, liste), hell=False)
V.append(('Das Glas füllt sich', v03))


# 04 · Die Schiefertafel: über der Theke hängt an zwei Schnüren eine dunkle Tafel mit den Preisen;
# sie schwingt beim Auftritt aus und kommt zur Ruhe. Links der Text, die Beträge stehen als zwei Zeilen am Fuss der Tafel.
def v04(n):
    tafel = '<div class="t4-haenger auf"><i class="t4-s l"></i><i class="t4-s r"></i><div class="t4-tafel">%s<div class="t4-posten">%s</div><div class="t4-fuss"><div><span class="etikett">%s</span><b class="titel">%s</b></div><i>+</i><div><span class="etikett">%s</span><b class="titel">%s</b></div></div>%s</div></div>' % (
        listenkopf(), posten(), SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], hinweis())
    return sek(n, '<div class="t4-raster"><div>%s%s</div>%s</div>' % (kopf(), klein(), tafel))
V.append(('Die Schiefertafel', v04))


# 05 · Grosse Zahlen: die beiden Beträge laufen über die ganze Breite, gross wie ein Titel, die Ziffern rollen
# wie ein Zählwerk auf ihren Wert. Darunter die Preise in sieben Spalten nebeneinander.
def v05(n):
    def rolle(txt):
        out = ''
        for j, ch in enumerate(txt):
            if ch.isdigit():
                d = int(ch)
                out += '<span class="z5-r" style="--d:%d;--j:%d"><em>%d</em><span>%s</span></span>' % (d, j, d, ''.join('<i>%d</i>' % x for x in range(10)))
            else:
                out += '<span class="z5-c">%s</span>' % E(ch)
        return out
    zahlen = '<div class="z5-zahlen auf"><div><span class="etikett">%s</span><b class="titel">%s</b></div><i class="titel">+</i><div><span class="etikett">%s</span><b class="titel">%s</b></div></div>' % (
        SERVICE[0], rolle(SERVICE[1]), BUDGET[0], rolle(BUDGET[1]))
    spalten = '<div class="z5-spalten auf">%s</div>' % ''.join('<div style="--n:%d"><b class="titel">%s €</b><span>%s</span></div>' % (j, p, E(t)) for j, (t, p) in enumerate(PREISE))
    return sek(n, '<div class="z5-kopf">%s%s</div>%s%s<div class="z5-fuss">%s%s</div>' % (kopf(), klein(), zahlen, '<div class="z5-lk">%s</div>' % listenkopf(), spalten, hinweis()), hell=False)
V.append(('Grosse Zahlen', v05))


# 06 · Vor der Rückbar: links hochkant das Foto der Rückbar, das beim Scrollen in seinem Rahmen ruhig näher rückt;
# rechts der Text, die Beträge, und die Preise als offene Liste ohne Karte.
def v06(n):
    rechts = '<div>%s<div class="r6-betraege sw" style="--i:2"><div><span class="etikett">%s</span><b class="titel">%s</b></div><div><span class="etikett">%s</span><b class="titel">%s</b></div></div>%s<div class="r6-liste sw" style="--i:3">%s<div class="r6-posten">%s</div>%s</div></div>' % (
        kopf(), SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], klein(), listenkopf(), posten(), hinweis())
    return sek(n, '<div class="r6-raster"><div class="r6-bild" data-nah>%s</div>%s</div>' % (fo('flaschen', '(max-width:900px) 92vw, 40vw', 'r6-f', '50% 50%'), rechts), hell=False)
V.append(('Vor der Rückbar', v06))


# 07 · Die Anhänger: sieben schmale Kartonanhänger hängen an Fäden nebeneinander, je einer pro Drink,
# Name oben, Preis gross unten. Sie fallen nacheinander herab und federn nach.
def v07(n):
    tags = ''.join('<div class="a7-tag" style="--n:%d"><i class="a7-faden"></i><div class="a7-karte"><i class="a7-loch"></i><span>%s</span><b class="titel">%s €</b></div></div>' % (j, E(t), p) for j, (t, p) in enumerate(PREISE))
    oben = '<div class="a7-oben"><div>%s</div><div class="a7-rechnung sw" style="--i:2"><div><span class="etikett">%s</span><b class="titel">%s</b></div><i>+</i><div><span class="etikett">%s</span><b class="titel">%s</b></div>%s</div></div>' % (
        kopf(), SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], klein())
    return sek(n, oben + '<div class="a7-lk">%s</div><div class="a7-stange auf"><i class="a7-holz"></i><div class="a7-reihe">%s</div></div>%s' % (listenkopf(), tags, hinweis('a7-hin')))
V.append(('Die Anhänger', v07))


# 08 · Das Leporello: eine dreiteilige Karte, die sich beim Auftritt von links nach rechts auffaltet.
# Feld eins: Service und Raum. Feld zwei: euer Budget. Feld drei: die Preise der Bar.
def v08(n):
    f1 = '<div class="l8-feld l8-a"><p class="l8-was">%s</p><b class="titel">%s</b></div>' % SERVICE
    f2 = '<div class="l8-feld l8-b"><p class="l8-was">%s</p><b class="titel">%s</b>%s</div>' % (BUDGET[0], BUDGET[1], klein())
    f3 = '<div class="l8-feld l8-c">%s<div class="l8-posten">%s</div>%s</div>' % (listenkopf(), posten(), hinweis())
    return sek(n, kopf('l8-kopf') + '<div class="l8-karte auf">%s%s%s</div>' % (f1, f2, f3))
V.append(('Das Leporello', v08))


# 09 · Der Goldrahmen: der Rahmen aus dem Titel wörtlich. Um den Budget-Betrag zieht sich ein Goldrahmen Seite für Seite;
# innen stehen beide Beträge, darunter die Preise wie eine Bildlegende in zwei Spalten.
def v09(n):
    rahmen = '<div class="r9-rahmen auf"><i class="r9-k o"></i><i class="r9-k r"></i><i class="r9-k u"></i><i class="r9-k l"></i><div class="r9-innen"><span class="etikett">%s</span><b class="titel r9-gross">%s</b><p class="r9-dazu"><span class="etikett">%s</span> <b class="titel">%s</b></p></div></div>' % (
        BUDGET[0], BUDGET[1], SERVICE[0], SERVICE[1])
    legende = '<div class="r9-legende auf">%s<div class="r9-posten">%s</div>%s</div>' % (listenkopf(), posten(), hinweis())
    return sek(n, '<div class="r9-raster"><div>%s%s</div>%s</div>%s' % (kopf(), klein(), rahmen, legende), hell=False)
V.append(('Der Goldrahmen', v09))


# 10 · Auf der Theke: eine lange Thekenkante mit gelbem Licht darunter zieht sich über die ganze Breite;
# auf ihr stehen die sieben Preise wie Gläser und steigen einer nach dem anderen hinter der Kante hervor.
def v10(n):
    glaeser = ''.join('<div class="k10-p" style="--n:%d"><b class="titel">%s €</b><span>%s</span></div>' % (j, p, E(t)) for j, (t, p) in enumerate(PREISE))
    oben = '<div class="k10-oben">%s<div class="k10-betraege sw" style="--i:2"><div><span class="etikett">%s</span><b class="titel">%s</b></div><div><span class="etikett">%s</span><b class="titel">%s</b></div>%s</div></div>' % (
        kopf(), SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], klein())
    return sek(n, oben + '<div class="k10-lk">%s</div><div class="k10-theke auf"><div class="k10-reihe">%s</div><i class="k10-kante"></i><i class="k10-licht"></i></div>%s' % (listenkopf(), glaeser, hinweis('k10-hin')), hell=False)
V.append(('Auf der Theke', v10))


# 11 · Der Bestellblock: ein cremefarbener Kellnerblock mit Perforation oben und Linien; die Zeilen erscheinen,
# als würden sie eingetragen, ein feiner Strich läuft jeder Zeile voraus. Unter dem Strich die Summe des Abends.
def v11(n):
    zeilen = ''.join('<div class="b11-z" style="--n:%d"><span>%s</span><b class="titel">%s €</b><i class="b11-stift"></i></div>' % (j, E(t), p) for j, (t, p) in enumerate(PREISE))
    block = '<div class="b11-block auf"><i class="b11-perf"></i><p class="b11-kopf"><span>Walk on the Wild Side</span><span>Was ein Drink kostet</span></p><h3 class="titel bltitel">Die Preise der Bar.</h3><div class="b11-zeilen">%s</div><div class="b11-summe"><div><span>%s</span><b class="titel">%s</b></div><div><span>%s</span><b class="titel">%s</b></div></div>%s</div>' % (
        zeilen, SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], hinweis())
    return sek(n, '<div class="b11-raster"><div>%s%s</div>%s</div>' % (kopf(), klein(), block))
V.append(('Der Bestellblock', v11))


# 12 · Zwei Karten im Fächer: die helle Rechnungskarte liegt vorn, die dunkle Preiskarte dahinter, beide leicht gedreht.
# Beim Scrollen schieben sie sich auseinander, bis beide ganz zu lesen sind.
def v12(n):
    hell = '<div class="f12-k f12-hell"><div class="f12-b"><span>%s</span><b class="titel">%s</b></div><i class="f12-plus titel">+</i><div class="f12-b"><span>%s</span><b class="titel">%s</b></div>%s</div>' % (
        SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], klein())
    dunkel = '<div class="f12-k f12-dunkel">%s<div class="f12-posten">%s</div>%s</div>' % (listenkopf(), posten(), hinweis())
    return sek(n, '<div class="f12-raster">%s<div class="f12-faecher" data-faecher>%s%s</div></div>' % (kopf(), dunkel, hell))
V.append(('Zwei Karten im Fächer', v12))


# 13 · Hell und dunkel geteilt: der Abschnitt ist in zwei Flächen geteilt, links creme mit Text und Beträgen,
# rechts randlos dunkel mit den Preisen. Die dunkle Fläche schiebt sich von rechts herein.
def v13(n):
    links = '<div class="h13-l">%s<div class="h13-betraege sw" style="--i:2"><div><span class="etikett">%s</span><b class="titel">%s</b></div><i class="titel">+</i><div><span class="etikett">%s</span><b class="titel">%s</b></div></div>%s</div>' % (
        kopf(), SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], klein())
    rechts = '<div class="h13-r auf"><div class="h13-rin">%s<div class="h13-posten">%s</div>%s</div></div>' % (listenkopf(), posten(), hinweis())
    return '<section class="kap hell auf bv b13" id="budget" data-b="13"><div class="h13-teil">%s%s</div></section>' % (links, rechts)
V.append(('Hell und dunkel geteilt', v13))


# 14 · Die Uhr des Abends: ein Zifferblatt, auf dem sich ein Goldbogen von 19 bis 2 Uhr dreht;
# in der Mitte die beiden Beträge. Daneben die Preise.
def v14(n):
    striche = ''.join('<i class="u14-st" style="--w:%ddeg"></i>' % (h * 30) for h in range(12))
    bogen = ''.join('<i class="u14-seg" style="--w:%ddeg;--n:%d"></i>' % ((7 + k) * 30, k) for k in range(8))   # 19 Uhr = 7 auf dem Zifferblatt, Stunde für Stunde bis 2 Uhr
    uhr = '<div class="u14-uhr auf">%s%s<span class="u14-z u14-19">19</span><span class="u14-z u14-2">2</span><div class="u14-mitte"><span class="etikett">%s</span><b class="titel">%s</b><i></i><span class="etikett">%s</span><b class="titel">%s</b></div></div>' % (
        striche, bogen, SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1])
    liste = '<div class="u14-liste sw" style="--i:2"><div>%s%s</div><div class="u14-posten">%s</div></div>' % (listenkopf(), hinweis(), posten())
    return sek(n, '<div class="u14-raster"><div>%s%s</div>%s</div>%s' % (kopf(), klein(), uhr, liste), hell=False)
V.append(('Die Uhr des Abends', v14))


# 15 · Die Walze: rechts steht ein Drink nach dem anderen gross in der Mitte, der Preis riesig daneben;
# beim Scrollen dreht die Walze zum nächsten (sieben Stufen auf rund zwei Scrollbewegungen), oben und unten die Nachbarn leise.
def v15(n):
    z = ''.join('<div class="w15-z" style="--n:%d"><span>%s</span><b class="titel">%s €</b></div>' % (j, E(t), p) for j, (t, p) in enumerate(PREISE))
    links = '<div class="w15-l">%s<div class="w15-betraege sw" style="--i:2"><div><span class="etikett">%s</span><b class="titel">%s</b></div><div><span class="etikett">%s</span><b class="titel">%s</b></div></div>%s</div>' % (
        kopf(), SERVICE[0], SERVICE[1], BUDGET[0], BUDGET[1], klein())
    walze = '<div class="w15-rechts"><div class="w15-kleb">%s<div class="w15-fenster"><div class="w15-walze">%s</div></div>%s</div></div>' % (listenkopf(), z, hinweis())
    return '<section class="kap auf bv b15" id="budget" data-b="15"><div class="innen w15-raster" data-walze>%s%s</div></section>' % (links, walze)
V.append(('Die Walze', v15))


def seite(n):
    h = unter.tafel()
    if n:
        a = h.rfind('<section', 0, h.find('id="budget"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/b.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/b.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
