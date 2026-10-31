# Walk on the Wild Side · Drinks-Seite, «Die einzige Karte»: 15 andere Darstellungen (30.10.2026).
# Robert: «Und jetzt gib mir 15 verschiedene Visualisierungsmöglichkeiten für den Abschnitt.» Je Fassung eigene Anordnung, eigene Bewegung.
# Texte nur aus der heutigen Drinks-Seite (unter.py), nichts dazu. Bilder: die echte Karte und Tellerkarte vom Valentinstag 2026 (Instagram der Bar),
# die Signature-Karte vom Weihnachtsfest 2023 (Instagram der Bar), Gläser aus den Google-Fotos. 00 = heutiger Stand. Wechsel mit ← →.
# Aufruf: python3 _varianten/karte-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/karte-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

KZ = B.kz('Eine Karte im Jahr', 'Valentinstag', 0)
TITEL = B.h2(['Die einzige Karte.'])
SATZ = ['Einmal im Jahr gibt es doch eine Karte: zum Valentinstag, zusammen mit Rudi von Culinarium.',
        '2026 hiess sie «Drunk in Love», vier Drinks zu je zwölf Euro, dazu Teller zum Teilen.',
        'Zum Weihnachtsfest 2023 standen Momos erste Signature Drinks auf einem Blatt: Linden Mule, Sakura, Mary Bramble, Ambré, Clean Pornstar, Zauberwald.']
TEXT = ' '.join(SATZ)
WEIH = ['Linden Mule', 'Sakura', 'Mary Bramble', 'Ambré', 'Clean Pornstar', 'Zauberwald']
ETIKETT = 'Valentinstag 2026 · Wild Side x Rudi in Love'
KTITEL = 'Drunk in Love.'
POSTEN = [('Frensh 26', 'Gin · Bergamotte · Nori · Schaumwein', '12'), ('Whey Bramble', 'Gin · Lemon Shrub · Vetiver · Whey Berry Soda', '12'),
          ('Pink Lady', 'Kakaobutter-Fat-Washed Rum · Himbeerpüree · Agave · Limette', '12'),
          ('Karamella', 'Havana 7 Jahre · Portwein · Johannisbeere · Karamell · schwarze Walnüsse · Limette', '12')]
KLEIN = 'Preise vom Plakat zum 14. Februar 2026. An allen anderen Abenden gibt es keine Karte.'
POS = {'fw-a55': '45% 55%', 'glas-coupe': '50% 50%', 'karte-love': '50% 30%', 'karte-dishes': '50% 30%'}


def img(k, sizes):
    return B.img_tag(k, sizes, extra=' style="object-position:%s"' % POS.get(k, '50% 50%'))


def fig(k, sizes, cls='', stil=''):
    return '<figure class="kf %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def text(i=1, cls='text'):
    return '<p class="%s sw" style="--i:%d">%s</p>' % (cls, i, E(TEXT))


def knopf(i=2):
    return '<div class="knoepfe sw" style="--i:%d">%s</div>' % (i, B.knopf('Platz reservieren', 'besuch.html#reservieren', 'rot'))


def kopf(cls='k-kopf'):
    return '<div class="%s">%s%s%s%s</div>' % (cls, KZ, TITEL, text(), knopf())


def posten(cls='posten', extra=''):
    return '<div class="%s">%s</div>' % (cls, ''.join('<div style="--n:%d">%s<b>%s</b><span>%s €</span><p>%s</p></div>' % (j, extra, E(t), p, E(z))
                                                    for j, (t, z, p) in enumerate(POSTEN)))


def blatt(cls='blatt', stil=''):
    return '<div class="%s" style="%s"><span class="etikett">%s</span><h3 class="titel">%s</h3>%s<small>%s</small></div>' % (
        cls, stil, E(ETIKETT), E(KTITEL), posten(), E(KLEIN))


def sek(n, inhalt, innen=True):
    return '<section class="kap auf kk v%02d" id="karte">%s</section>' % (n, '<div class="innen">%s</div>' % inhalt if innen else inhalt)


V = []


# 01 · Das Original: links Titel, Satz und Knopf, rechts die echte Karte vom Valentinstag, als Abzug hingelegt; sie schwebt hoch und legt sich aus der Schräge.
def v01(n):
    return sek(n, '<div class="or-gr">%s<div class="or-r vauf">%s<p class="or-u">%s</p></div></div>' % (
        kopf(), fig('karte-love', '(max-width:760px) 90vw, 40vw', 'or-k'), E(KLEIN)))
V.append(('Das Original', v01))


# 02 · Zwei Jahre: oben Titel und Satz quer, darunter zwei Spalten: die Weihnachtskarte 2023 im Foto mit ihren sechs Namen, daneben das Blatt vom Valentinstag.
def v02(n):
    links = '<div class="zj-l vauf">%s<span class="etikett">Weihnachtsfest 2023</span><ul class="zj-n">%s</ul></div>' % (
        fig('fw-a55', '(max-width:760px) 100vw, 40vw', 'zj-b'), ''.join('<li style="--n:%d">%s</li>' % (j, E(t)) for j, t in enumerate(WEIH)))
    return sek(n, '<div class="k-quer"><div>%s%s</div><div>%s%s</div></div><div class="zj-gr">%s<div class="zj-r vauf">%s</div></div>' % (
        KZ, TITEL, text(), knopf(), links, blatt()))
V.append(('Zwei Jahre', v02))


# 03 · Der Vierzehnte: links das Datum in grossen Ziffern, Zeile für Zeile aus der Kante, rechts das Blatt.
def v03(n):
    datum = '<div class="vz-d vauf"><span class="vz-m"><i>14.</i></span><span class="vz-m"><i>Februar</i></span><span class="vz-m"><i>2026</i></span></div>'
    return sek(n, '<div class="vz-gr"><div>%s%s%s%s%s</div>%s</div>' % (datum, KZ, TITEL, text(), knopf(), blatt('blatt vz-bl sw')))
V.append(('Der Vierzehnte', v03))


# 04 · Die Breite: die Karte als breites Querblatt über die ganze Seite, vier Drinks in vier Spalten; die Goldlinien ziehen sich, dann steigen die Spalten.
def v04(n):
    br = '<div class="br vauf"><div class="br-kopf"><span class="etikett">%s</span><h3 class="titel">%s</h3></div>%s<small>%s</small></div>' % (
        E(ETIKETT), E(KTITEL), posten('br-p', '<i class="br-l"></i>'), E(KLEIN))
    return sek(n, '<div class="k-quer"><div>%s%s</div><div>%s%s</div></div>%s' % (KZ, TITEL, text(), knopf(), br))
V.append(('Die Breite', v04))


# 05 · Aufgeschlagen: eine Karte zum Aufklappen; links die Titelseite, die rechte Seite mit den Drinks klappt am Falz auf.
def v05(n):
    l = '<div class="au-s au-l"><span class="etikett">%s</span><h3 class="titel">%s</h3><small>%s</small></div>' % (E(ETIKETT), E(KTITEL), E(KLEIN))
    r = '<div class="au-s au-r">%s</div>' % posten()
    return sek(n, '<div class="au-gr"><div>%s</div><div class="au vauf">%s%s</div></div>' % (KZ + TITEL + text() + knopf(), l, r))
V.append(('Aufgeschlagen', v05))


# 06 · Ein Drink im Blick: die Bühne bleibt stehen, beim Scrollen kommt Drink für Drink in grosser Schrift, links bleibt der Titel.
def v06(n):
    d = ''.join('<div class="eb-d%s" style="--n:%d"><b class="titel">%s</b><p>%s</p><span>%s €</span></div>' % (' an' if j == 0 else '', j, E(t), E(z), p)
                for j, (t, z, p) in enumerate(POSTEN))
    st = ''.join('<i%s></i>' % (' class="an"' if j == 0 else '') for j in range(4))
    return sek(n, '<div class="eb" data-pin><div class="eb-st"><div class="innen eb-gr"><div>%s<span class="etikett eb-et">%s</span></div><div class="eb-r"><div class="eb-bl">%s</div><div class="eb-striche">%s</div><small>%s</small></div></div></div></div>' % (
        KZ + TITEL + text() + knopf(), E(ETIKETT), d, st, E(KLEIN)), innen=False)
V.append(('Ein Drink im Blick', v06))


# 07 · Die Zutaten: je Drink eine Zeile, die Zutaten gross, Wort für Wort, der Name klein davor, der Preis am Ende.
def v07(n):
    z = ''.join('<div class="zu-z vauf" style="--n:%d"><span class="zu-n titel">%s</span><p class="zu-w">%s</p><span class="zu-p">%s €</span></div>' % (
        j, E(t), ' '.join('<i style="--w:%d">%s</i>' % (w, E(x)) + ('<em>·</em>' if w < len(zz.split(' · ')) - 1 else '') for w, x in enumerate(zz.split(' · '))), p)
        for j, (t, zz, p) in enumerate(POSTEN))
    return sek(n, '<div class="k-quer"><div>%s%s</div><div>%s%s</div></div><span class="etikett zu-et">%s · %s</span><div class="zu">%s</div><small class="zu-k">%s</small>' % (
        KZ, TITEL, text(), knopf(), E(ETIKETT), E(KTITEL), z, E(KLEIN)))
V.append(('Die Zutaten', v07))


# 08 · Die Tasche: rechts eine dunkle Tasche mit Goldkante, beim Scrollen schiebt sich das Blatt aus ihr nach oben.
def v08(n):
    return sek(n, '<div class="ta-gr" data-ta><div>%s</div><div class="ta"><div class="ta-hinten"></div>%s<div class="ta-vorn"><span>Wild Side x Rudi in Love</span></div></div></div>' % (
        KZ + TITEL + text() + knopf(), blatt('blatt ta-bl')))
V.append(('Die Tasche', v08))


# 09 · Halb und halb: links ein Glas bei Kerzenlicht über die ganze Höhe, das Bild wandert langsam; rechts Titel, Satz und das Blatt.
def v09(n):
    return sek(n, '<div class="hh">%s<div class="hh-r">%s%s%s%s</div></div>' % (
        fig('glas-coupe', '(max-width:760px) 100vw, 50vw', 'hh-bild'), KZ, TITEL, text(), blatt('blatt hh-bl sw') + knopf(3)), innen=False)
V.append(('Halb und halb', v09))


# 10 · Der Weg: eine Goldlinie von Weihnachten 2023 zum Valentinstag 2026, sie zieht sich beim Scrollen; an jedem Halt die echte Karte.
def v10(n):
    h1 = '<div class="wg-h"><i class="wg-p"></i><span class="etikett">Weihnachtsfest 2023</span>%s<ul class="zj-n">%s</ul></div>' % (
        fig('fw-a55', '(max-width:760px) 100vw, 34vw', 'wg-b'), ''.join('<li>%s</li>' % E(t) for t in WEIH))
    h2 = '<div class="wg-h"><i class="wg-p"></i><span class="etikett">%s</span>%s%s</div>' % (E(ETIKETT), fig('karte-love', '(max-width:760px) 100vw, 34vw', 'wg-b'), posten('posten wg-po'))
    return sek(n, '<div class="k-quer"><div>%s%s</div><div>%s%s</div></div><div class="wg" data-wg><i class="wg-linie"><b></b></i>%s%s</div><small class="zu-k">%s</small>' % (
        KZ, TITEL, text(), knopf(), h1, h2, E(KLEIN)))
V.append(('Der Weg', v10))


# 11 · Der Fächer: vier Kärtchen, eins je Drink, liegen erst aufeinander und fächern sich beim Scrollen zu einer Reihe auf.
def v11(n):
    k = ''.join('<div class="fa-k" style="--n:%d"><span class="etikett">Drunk in Love</span><b class="titel">%s</b><p>%s</p><span class="fa-p">%s €</span></div>' % (j, E(t), E(z), p)
                for j, (t, z, p) in enumerate(POSTEN))
    return sek(n, '<div class="k-quer"><div>%s%s</div><div>%s%s</div></div><div class="fa" data-fa>%s</div><small class="zu-k">%s</small>' % (KZ, TITEL, text(), knopf(), k, E(KLEIN)))
V.append(('Der Fächer', v11))


# 12 · In Rosa: das Blatt in den Farben der echten Karte, Rosa und Rot; es steigt hoch, die Zeilen folgen.
def v12(n):
    return sek(n, '<div class="ro-gr"><div>%s</div>%s</div>' % (KZ + TITEL + text() + knopf(), blatt('blatt ro-bl vauf')))
V.append(('In Rosa', v12))


# 13 · Drei Sätze: der Text in seinen drei Sätzen, jeder gross für sich, nacheinander; rechts bleibt das Blatt stehen.
def v13(n):
    s = ''.join('<p class="ds-s vauf" style="--n:%d">%s</p>' % (j, E(x)) for j, x in enumerate(SATZ))
    return sek(n, '<div class="ds-gr"><div>%s%s%s%s</div><div class="ds-r">%s</div></div>' % (KZ, TITEL, s, knopf(), blatt('blatt ds-bl')))
V.append(('Drei Sätze', v13))


# 14 · Die Wand: die drei echten Karten Wand an Wand, Drinks und Teller vom Valentinstag, die Weihnachtskarte 2023; jede schwebt einzeln hoch.
def v14(n):
    w = ''.join('<div class="wa-f" style="--n:%d">%s<span class="etikett">%s</span></div>' % (j, fig(k, '(max-width:760px) 100vw, 33vw', 'wa-b'), E(u))
                for j, (k, u) in enumerate((('karte-love', 'Valentinstag 2026 · Drunk in Love'), ('karte-dishes', 'Valentinstag 2026 · Dishes in Love'), ('fw-a55', 'Weihnachtsfest 2023'))))
    return sek(n, '<div class="innen"><div class="k-quer"><div>%s%s</div><div>%s%s</div></div></div><div class="wa vauf">%s</div><div class="innen"><small class="zu-k">%s</small></div>' % (
        KZ, TITEL, text(), knopf(), w, E(KLEIN)), innen=False)
V.append(('Die Wand', v14))


# 15 · Mittig: alles auf einer Achse, das Blatt breit in der Mitte, die vier Drinks zu zweit; die Linien ziehen sich von der Mitte aus.
def v15(n):
    bl = '<div class="mi-bl vauf"><span class="etikett">%s</span><h3 class="titel">%s</h3>%s<small>%s</small></div>' % (
        E(ETIKETT), E(KTITEL), posten('mi-p', '<i class="mi-l"></i>'), E(KLEIN))
    return sek(n, '<div class="mi">%s%s%s%s%s</div>' % (KZ, TITEL, text(), bl, knopf(3)))
V.append(('Mittig', v15))


def seite(n):
    h = unter.drinks()
    if n:
        a = h.find('<section class="kap auf" id="karte">')
        b = h.find('</section>', a) + len('</section>')
        assert a > 0
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
