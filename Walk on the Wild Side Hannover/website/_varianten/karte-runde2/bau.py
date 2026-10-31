# Walk on the Wild Side · Drinks-Seite, «Die einzige Karte»: Runde 2, 15 neue Darstellungen (30.10.2026).
# Robert zur ersten Runde (_varianten/karte-15): «Nee, die gefallen mir alle nicht. Bitte nochmal andere, weitere neue.»
# Diesmal tragen die Fotos der Bar den Abschnitt, nicht das Blatt. Je Fassung eigene Anordnung, eigene Bewegung.
# Texte nur aus der heutigen Drinks-Seite (unter.py), nichts dazu. 00 = heutiger Stand. Wechsel mit ← →.
# Aufruf: python3 _varianten/karte-runde2/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/karte-runde2'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

KZ = B.kz('Eine Karte im Jahr', 'Valentinstag', 0)
TITEL = B.h2(['Die einzige Karte.'])
TEXT = ('Einmal im Jahr gibt es doch eine Karte: zum Valentinstag, zusammen mit Rudi von Culinarium. 2026 hiess sie «Drunk in Love», vier Drinks zu je zwölf Euro, '
        'dazu Teller zum Teilen. Zum Weihnachtsfest 2023 standen Momos erste Signature Drinks auf einem Blatt: Linden Mule, Sakura, Mary Bramble, Ambré, Clean Pornstar, Zauberwald.')
ETIKETT = 'Valentinstag 2026 · Wild Side x Rudi in Love'
KTITEL = 'Drunk in Love.'
POSTEN = [('Frensh 26', 'Gin · Bergamotte · Nori · Schaumwein', '12'), ('Whey Bramble', 'Gin · Lemon Shrub · Vetiver · Whey Berry Soda', '12'),
          ('Pink Lady', 'Kakaobutter-Fat-Washed Rum · Himbeerpüree · Agave · Limette', '12'),
          ('Karamella', 'Havana 7 Jahre · Portwein · Johannisbeere · Karamell · schwarze Walnüsse · Limette', '12')]
KLEIN = 'Preise vom Plakat zum 14. Februar 2026. An allen anderen Abenden gibt es keine Karte.'
# Gläser aus den Fotos der Bar (Google-Eintrag) und aus Rudis Drive; welches Glas welcher Drink ist, ist nicht belegt, deshalb steht nie ein Name am Bild.
GL = ['fe-coupe', 'dg-coupes', 'glas-zwei', 'wf-pink']
POS = {'dg-coupes': '50% 55%', 'glas-zwei': '50% 62%', 'fe-coupe': '50% 45%', 'wf-pink': '35% 55%', 'dg-shaker': '45% 40%', 'momo-lacht': '50% 45%',
       'culinarium-tafel': '50% 55%', 'fw-tafel': '50% 50%', 'karte-love': '50% 50%'}


def img(k, sizes):
    return B.img_tag(k, sizes, extra=' style="object-position:%s"' % POS.get(k, '50% 50%'))


def fig(k, sizes, cls='', stil=''):
    return '<figure class="kf %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def text(i=1, cls='text'):
    return '<p class="%s sw" style="--i:%d">%s</p>' % (cls, i, E(TEXT))


def knopf(i=2):
    return '<div class="knoepfe sw" style="--i:%d">%s</div>' % (i, B.knopf('Platz reservieren', 'besuch.html#reservieren', 'rot'))


def drink(j, cls='dr', h='h3'):
    t, z, p = POSTEN[j]
    return '<div class="%s" style="--n:%d"><%s class="titel">%s</%s><p>%s</p><span class="dr-p">%s €</span></div>' % (cls, j, h, E(t), h, E(z), p)


def klein(cls='kl'):
    return '<small class="%s">%s</small>' % (cls, E(KLEIN))


def sek(n, inhalt, innen=True):
    return '<section class="kap auf kr v%02d" id="karte">%s</section>' % (n, '<div class="innen">%s</div>' % inhalt if innen else inhalt)


V = []


# 01 · Der Name: «Drunk in Love.» über die ganze Breite, darunter zwei Gläser Wand an Wand, die nacheinander hochschweben; darunter die vier Drinks in einer Reihe.
def v01(n):
    return sek(n, '<div class="innen">%s<p class="nm-t titel vauf"><span><i>Drunk</i></span><span><i>in Love.</i></span></p></div>'
                  '<div class="nm-b vauf">%s%s</div><div class="innen"><div class="nm-u"><div><span class="etikett">%s</span>%s%s%s</div><div class="nm-d">%s</div></div>%s</div>' % (
        KZ, fig('dg-coupes', '(max-width:760px) 100vw, 50vw', 'nm-f'), fig('fe-coupe', '(max-width:760px) 100vw, 50vw', 'nm-f'),
        E(ETIKETT), TITEL, text(), knopf(), ''.join(drink(j) for j in range(4)), klein()), innen=False)
V.append(('Der Name', v01))


# 02 · Im Wechsel: je Drink eine Zeile mit einem grossen Glas, mal links, mal rechts; das Bild steigt, das Glas zoomt sanft heran, dann folgt der Text.
def v02(n):
    z = ''.join('<div class="zz-z vauf%s">%s<div class="zz-t">%s</div></div>' % (' re' if j % 2 else '', fig(GL[j], '(max-width:760px) 100vw, 46vw', 'zz-f'), drink(j, 'dr zz-d', 'h3'))
                for j in range(4))
    return sek(n, '<div class="k-quer"><div>%s%s<span class="etikett zz-et">%s</span></div><div>%s%s</div></div>%s%s' % (KZ, TITEL, E(ETIKETT), text(), knopf(), z, klein()))
V.append(('Im Wechsel', v02))


# 03 · Zwei Häuser: links Momo an der Bar, rechts Rudis lange Tafel, dazwischen ein goldenes ×; beide Bilder steigen gleichzeitig, das × dreht sich ein.
def v03(n):
    return sek(n, '<div class="zh vauf">%s<span class="zh-x" aria-hidden="true">×</span>%s</div><div class="zh-u"><div>%s<span class="etikett">%s</span>%s%s%s</div><div class="zh-d">%s</div></div>%s' % (
        fig('momo-lacht', '(max-width:760px) 50vw, 42vw', 'zh-f'), fig('culinarium-tafel', '(max-width:760px) 50vw, 42vw', 'zh-f'),
        KZ, E(ETIKETT), TITEL, text(), knopf(), ''.join(drink(j) for j in range(4)), klein()))
V.append(('Zwei Häuser', v03))


# 04 · Das Schachbrett: Bild und Drink im Wechsel, Wand an Wand, zwei Reihen; die Felder steigen schräg von links oben nach rechts unten.
def v04(n):
    felder = []
    for j in range(4):
        b = fig(GL[j], '(max-width:760px) 50vw, 25vw', 'sb-f')
        d = '<div class="sb-d">%s</div>' % drink(j)
        felder += [b, d] if j < 2 else [d, b]
    fe = ''.join('<div class="sb-x" style="--d:%d">%s</div>' % ((i % 4) + (i // 4), f) for i, f in enumerate(felder))
    return sek(n, '<div class="innen"><div class="k-quer"><div>%s%s</div><div>%s%s</div></div></div><div class="sb vauf">%s</div><div class="innen">%s</div>' % (
        KZ, TITEL, text(), knopf(), fe, klein()), innen=False)
V.append(('Das Schachbrett', v04))


# 05 · Das Glas in der Mitte: ein hohes Glas bei Kerzenlicht mittig, links und rechts je zwei Drinks; erst das Glas, dann links, dann rechts.
def v05(n):
    return sek(n, '<div class="mt-k">%s%s%s</div><div class="mt vauf"><div class="mt-s">%s</div>%s<div class="mt-s">%s</div></div><div class="mt-fuss">%s%s</div>' % (
        KZ, TITEL, text(), drink(0) + drink(1), fig('wf-pink', '(max-width:760px) 100vw, 32vw', 'mt-f'), drink(2) + drink(3), knopf(), klein()))
V.append(('Das Glas in der Mitte', v05))


# 06 · Das Triptychon: Glas, Blatt, Glas, gleich hoch, Wand an Wand über die ganze Breite; die Mitte steigt zuerst, die Seiten folgen.
def v06(n):
    bl = '<div class="tp-bl"><span class="etikett">%s</span><h3 class="titel">%s</h3><div class="tp-p">%s</div>%s</div>' % (
        E(ETIKETT), E(KTITEL), ''.join(drink(j, 'dr tp-d') for j in range(4)), klein())
    return sek(n, '<div class="innen"><div class="k-quer"><div>%s%s</div><div>%s%s</div></div></div><div class="tp vauf">%s%s%s</div>' % (
        KZ, TITEL, text(), knopf(), fig('glas-zwei', '(max-width:760px) 100vw, 33vw', 'tp-f'), bl, fig('dg-coupes', '(max-width:760px) 100vw, 33vw', 'tp-f')), innen=False)
V.append(('Das Triptychon', v06))


# 07 · Die rosa Hälfte: links eine Fläche im Rosa der echten Karte, darauf die Karte selbst, randlos; rechts dunkel Titel, Satz und Knopf.
def v07(n):
    return sek(n, '<div class="rh"><div class="rh-l vauf">%s</div><div class="rh-r">%s%s%s%s%s</div></div>' % (
        fig('karte-love', '(max-width:760px) 100vw, 46vw', 'rh-k'), KZ, TITEL, text(), knopf(), klein()), innen=False)
V.append(('Die rosa Hälfte', v07))


# 08 · Die Tafel: Rudis lange Tafel am Fenster als breites Bild, darunter die vier Drinks Spalte an Spalte.
def v08(n):
    return sek(n, '<div class="innen"><div class="k-quer"><div>%s%s</div><div>%s%s</div></div><div class="tf vauf">%s</div><span class="etikett tf-et">%s</span><div class="tf-d">%s</div>%s</div>' % (
        KZ, TITEL, text(), knopf(), fig('fw-tafel', '(max-width:760px) 100vw, 86vw', 'tf-f'), E(ETIKETT), ''.join(drink(j) for j in range(4)), klein()), innen=False)
V.append(('Die Tafel', v08))


# 09 · Name und Glas: je Drink eine Zeile, der Name sehr gross, daneben ein kleines Glas; das Glas zoomt heran, wenn die Zeile kommt.
def v09(n):
    z = ''.join('<div class="ng-z vauf" style="--n:%d"><h3 class="titel ng-n">%s</h3>%s<p class="ng-w">%s</p><span class="ng-p">%s €</span></div>' % (
        j, E(t), fig(GL[j], '(max-width:760px) 30vw, 14vw', 'ng-f'), E(zz), p) for j, (t, zz, p) in enumerate(POSTEN))
    return sek(n, '<div class="k-quer"><div>%s%s</div><div>%s%s</div></div><span class="etikett">%s</span><div class="ng">%s</div>%s' % (KZ, TITEL, text(), knopf(), E(ETIKETT), z, klein()))
V.append(('Name und Glas', v09))


# 10 · Vier Kärtchen mit Glas: oben das Glas, unten Name, Zutaten und Preis; sie kommen nacheinander und federn ein wenig nach.
def v10(n):
    k = ''.join('<div class="vk-k" style="--n:%d">%s%s</div>' % (j, fig(GL[j], '(max-width:760px) 50vw, 24vw', 'vk-f'), drink(j, 'dr vk-d')) for j in range(4))
    return sek(n, '<div class="k-quer"><div>%s%s</div><div>%s%s</div></div><div class="vk vauf">%s</div>%s' % (KZ, TITEL, text(), knopf(), k, klein()))
V.append(('Vier Kärtchen mit Glas', v10))


# 11 · Das Paar: zwei hohe Gläser Wand an Wand links, das rechte läuft beim Scrollen langsamer; rechts Titel, Satz und die Drinks.
def v11(n):
    return sek(n, '<div class="pa"><div class="pa-b">%s%s</div><div class="pa-r">%s%s%s<span class="etikett pa-et">%s</span><div class="pa-d">%s</div>%s%s</div></div>' % (
        fig('dg-coupes', '(max-width:760px) 50vw, 28vw', 'pa-f'), fig('fe-coupe', '(max-width:760px) 50vw, 28vw', 'pa-f pa-f2'),
        KZ, TITEL, text(), E(ETIKETT), ''.join(drink(j) for j in range(4)), knopf(3), klein()))
V.append(('Das Paar', v11))


# 12 · Das Laufband: die vier Namen laufen gross und langsam durch die ganze Breite, darunter Titel, Satz und ein Glas, daneben die Drinks.
def v12(n):
    band = ''.join('<span>%s</span><i>·</i>' % E(t) for t, z, p in POSTEN) * 2
    return sek(n, '<div class="lb" aria-hidden="true"><div class="lb-zug">%s</div><div class="lb-zug">%s</div></div><div class="innen"><div class="lb-gr"><div>%s%s%s%s</div>%s<div class="lb-d"><span class="etikett">%s</span>%s%s</div></div></div>' % (
        band, band, KZ, TITEL, text(), knopf(), fig('glas-zwei', '(max-width:760px) 100vw, 26vw', 'lb-f sw'), E(ETIKETT), ''.join(drink(j) for j in range(4)), klein()), innen=False)
V.append(('Das Laufband', v12))


# 13 · Das ruhige Glas: links bleibt ein grosses Glas stehen und zieht sich beim Lesen langsam zurück; rechts Titel, Satz und die Drinks gross untereinander.
def v13(n):
    return sek(n, '<div class="rg"><div class="rg-l"><div class="rg-st">%s</div></div><div class="rg-r">%s%s%s%s<span class="etikett rg-et">%s</span>%s%s</div></div>' % (
        fig('fe-coupe', '(max-width:760px) 100vw, 44vw', 'rg-f'), KZ, TITEL, text(), knopf(), E(ETIKETT), ''.join(drink(j, 'dr rg-d vauf') for j in range(4)), klein()))
V.append(('Das ruhige Glas', v13))


# 14 · Die Reihe: die Coupes mit Goldrand als breites Band, es steigt hoch, die Gläser rücken heran; darunter die Drinks auf einer Goldlinie.
def v14(n):
    return sek(n, '<div class="innen">%s%s<div class="re-b vauf">%s</div><div class="re-u"><div>%s%s</div><div><span class="etikett">%s</span><div class="re-d">%s</div>%s</div></div></div>' % (
        KZ, TITEL, fig('dg-coupes', '(max-width:760px) 100vw, 86vw', 're-f'), text(), knopf(), E(ETIKETT), ''.join(drink(j) for j in range(4)), klein()), innen=False)
V.append(('Die Reihe', v14))


# 15 · Momo mixt: links Momo am Shaker im hohen Bild, das Foto wandert langsam; rechts Titel und Satz, darunter die Drinks zu zweit mit Goldlinien.
def v15(n):
    return sek(n, '<div class="mm">%s<div class="mm-r">%s%s%s<span class="etikett mm-et">%s</span><div class="mm-d vauf">%s</div>%s%s</div></div>' % (
        fig('dg-shaker', '(max-width:760px) 100vw, 42vw', 'mm-f'), KZ, TITEL, text(), E(ETIKETT), ''.join(drink(j, 'dr mm-x') for j in range(4)), knopf(3), klein()))
V.append(('Momo mixt', v15))


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
