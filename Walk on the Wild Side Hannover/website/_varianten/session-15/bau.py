# Walk on the Wild Side · Programm-Seite, Abschnitt «Samstags · Die DJ-Abende · Jeder Abend ein Plakat.» (id="session"): 15 Darstellungen (30.10.2026).
# Robert: «Visualisierungsmöglichkeiten für den Abschnitt? 15». 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte Wort für Wort aus unter.programm(), Abende aus bau.LINEUP, nur die echten Plakate.
# Bewegung nur über transform und opacity, ein Scroll-Takt in s.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/session-15/bau.py → 00.html … 15.html
import os, sys, json, html, math
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/session-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('s.css', 's.js', 'nav.js'))))

ZEIG = 'Zeig auf einen Abend, dann siehst du sein Plakat. '
TEXT = 'Seit September 2025 holt das Wild Side DJs an die Bar. Jeder Abend bekommt ein eigenes Plakat mit rot-cremefarbenen Wellen und dem Gesicht des Abends in Schwarzweiss. Zeig auf einen Abend, dann siehst du sein Plakat. Den nächsten kündigt die Bar auf Instagram an.'
REIHE = 'Die DJ-Abende der Bar · samstags 21 bis 1 Uhr'
_q = open('unter.py').read()
assert TEXT in _q and REIHE in _q, 'Text weicht von der Seite ab'

LINEUP = B.LINEUP                                    # (datum, name, richtung, plakat), neuester zuerst
PLAKATE = []                                         # je Plakat einmal: (schlüssel, [abende])
for d, n, r, k in LINEUP:
    for p in PLAKATE:
        if p[0] == k:
            p[1].append((d, n, r)); break
    else:
        PLAKATE.append((k, [(d, n, r)]))


def kurz(d):
    return d[:6]                                     # 17.10.2026 → 17.10.


def p_datum(ab):
    return ' und '.join(kurz(d) for d, n, r in ab[::-1])[:-1] + ab[0][0][5:] if len(ab) > 1 else ab[0][0]


def p_name(ab):
    return ', '.join(n for d, n, r in ab[::-1])


def kopf(zeig=False, rechts='', cls='', knopf=True):
    t = TEXT if zeig else TEXT.replace(ZEIG, '')
    k = '<div class="knoepfe sw" style="--i:3;margin-top:30px">%s</div>' % B.knopf('Instagram der Bar', B.HAUS['instagram']) if knopf else ''
    return '<div class="s-kopf %s"><div class="s-kopf-l">%s%s<p class="text sw" style="--i:1">%s</p>%s</div>%s</div>' % (
        cls, B.kz('Samstags', 'Die DJ-Abende', 0), B.h2(['Jeder Abend', 'ein Plakat.']), E(t), k, rechts)


def pl(k, sizes, cls='', stil='', extra=''):
    """Ein Plakat: Bild auf seiner Unschärfe-Vorschau, ohne .foto, damit die Auftritte der Seite nicht mitspielen."""
    return '<figure class="sp %s" style="--lq:url(%s);%s"%s>%s</figure>' % (cls, mache(k)['lq'], stil, extra, B.img_tag(k, sizes))


def zeile(d, n, r, cls=''):
    return '<p class="s-zeile %s"><span class="s-dat">%s</span><b>%s</b>%s</p>' % (cls, E(d), E(n), '<small>%s</small>' % E(r) if r else '')


def sek(n, inner, cls='', innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf sx s%02d %s" id="session" data-s="%d">%s</section>' % (n, cls, n, i)


def daten(ab):
    d, nm, r = ab[0]
    return ' data-dat="%s" data-name="%s" data-r="%s"' % (E(p_datum(ab)), E(p_name(ab)), E(' · '.join(x[2] for x in ab if x[2])))


V = []


# 01 · Die Plakatwand: alle Plakate an einer Wand, leicht schief und überlappend, wie in Linden an der Mauer.
# Sie werden nacheinander angeklebt: jedes kommt etwas zu gross und setzt sich flach auf die Wand. Zeigen hebt eins an.
def v01(n):
    lage = [(0, 2, -3), (24, 6, 2), (49, 0, -1.5), (74, 5, 3), (5, 54, 2.5), (30, 52, -2), (54, 56, 1.5), (78, 53, -3)]
    w = ''.join('<div class="w1-p" style="--x:%s%%;--y:%s%%;--w:%sdeg;--n:%d"%s>%s<p class="w1-tag"><span>%s</span>%s</p></div>' % (
        x, y, r, j, daten(ab), pl(k, '(max-width:760px) 46vw, 22vw'), E(p_datum(ab)), E(p_name(ab))) for j, ((k, ab), (x, y, r)) in enumerate(zip(PLAKATE, lage)))
    return sek(n, kopf() + '<div class="w1-wand vauf">%s</div>' % w)
V.append(('Die Plakatwand', v01))


# 02 · Der Stapel: die Bühne steht, rechts liegen alle Plakate aufeinander, das neueste oben.
# Beim Scrollen wird eins nach dem anderen weggeschoben, links wechseln Datum und Name in grosser Schrift.
def v02(n):
    st = ''.join('<div class="w2-p" style="--n:%d;--w:%sdeg">%s</div>' % (j, (-3, 2, -1, 3, -2, 1.5, -2.5, 2)[j], pl(k, '(max-width:760px) 80vw, 34vw')) for j, (k, ab) in enumerate(PLAKATE))
    tx = ''.join('<div class="w2-t" style="--n:%d"><p class="w2-dat titel">%s</p><p class="w2-name">%s</p><p class="w2-r">%s</p></div>' % (
        j, E(p_datum(ab)), E(p_name(ab)), E(' · '.join(x[2] for x in ab if x[2]))) for j, (k, ab) in enumerate(PLAKATE))
    return sek(n, '<div class="innen">%s</div><div class="w2-pin" data-pin><div class="w2-buehne"><div class="innen w2-raster"><div class="w2-texte"><p class="etikett">%s</p>%s<p class="w2-zahl"><b>1</b> / %d</p></div><div class="w2-stapel">%s</div></div></div></div>' % (
        kopf(), E(REIHE), tx, len(PLAKATE), st), innen=False)
V.append(('Der Stapel', v02))


# 03 · Das Band: alle Plakate in einer Reihe, älteste links, neueste rechts; unter ihnen läuft eine Zeitleiste von September 2025 bis Oktober 2026.
# Das Band zieht beim Scrollen langsam nach links, so wandert man durch das Jahr.
def v03(n):
    b = ''.join('<article class="w3-p">%s<p class="w3-strich"></p>%s</article>' % (pl(k, '(max-width:760px) 62vw, 22vw'), zeile(p_datum(ab), p_name(ab), '')) for k, ab in PLAKATE[::-1])
    return sek(n, '<div class="innen">%s</div><div class="w3-fahrt" data-band><div class="w3-band">%s</div></div>' % (kopf(), b), innen=False)
V.append(('Das Band', v03))


# 04 · Der Zeitstrahl: eine Goldlinie läuft mittig nach unten und wächst beim Scrollen mit; die Plakate stehen abwechselnd links und rechts,
# das Datum gegenüber an der Linie. Jedes Plakat steigt auf, wenn die Linie es erreicht.
def v04(n):
    e = ''.join('<article class="w4-e %s vauf" style="--n:%d">%s<div class="w4-t">%s</div><i class="w4-mark"></i></article>' % (
        'rechts' if j % 2 else 'links', j, pl(k, '(max-width:760px) 60vw, 19vw'), zeile(p_datum(ab), p_name(ab), ' · '.join(x[2] for x in ab if x[2]))) for j, (k, ab) in enumerate(PLAKATE))
    return sek(n, kopf() + '<div class="w4-strahl" data-strahl><i class="w4-linie"></i>%s</div>' % e)
V.append(('Der Zeitstrahl', v04))


# 05 · Der Fächer: die Plakate liegen erst als Stapel, dann fächern sie sich auf wie ein Blatt Karten.
# Zeigen zieht ein Plakat aus dem Fächer nach oben, darunter stehen Datum und Name.
def v05(n):
    m = len(PLAKATE)
    f = ''.join('<div class="w5-p" style="--g:%.1fdeg;--n:%d;z-index:%d"%s>%s</div>' % (
        -30 + 60 * j / (m - 1), j, j, daten(ab), pl(k, '(max-width:760px) 36vw, 18vw')) for j, (k, ab) in enumerate(PLAKATE[::-1]))
    k0, ab0 = PLAKATE[0]
    return sek(n, kopf(zeig=True) + '<div class="w5-buehne vauf"><div class="w5-faecher">%s</div><div class="w5-satz"><p class="w5-dat titel">%s</p><p class="w5-name">%s</p></div></div>' % (
        f, E(p_datum(ab0)), E(p_name(ab0))))
V.append(('Der Fächer', v05))


# 06 · Der Schaukasten: ein schwarzer Kasten mit Goldrahmen wie das Eckschild der Bar, darin hängen alle Plakate in zwei Reihen.
# Sie werden von oben eingehängt und pendeln kurz aus.
def v06(n):
    g = ''.join('<div class="w6-p" style="--n:%d;--w:%sdeg"><i class="w6-nadel"></i>%s<p class="w6-tag">%s<br><b>%s</b></p></div>' % (
        j, (-1.5, 1, -.5, 1.5, 1, -1.5, .5, -1)[j], pl(k, '(max-width:760px) 40vw, 17vw'), E(p_datum(ab)), E(p_name(ab))) for j, (k, ab) in enumerate(PLAKATE))
    return sek(n, kopf() + '<div class="w6-kasten vauf"><div class="w6-innen"><p class="w6-kopf"><span>SESSION</span><span>%s</span></p><div class="w6-raster">%s</div></div></div>' % (E(REIHE), g))
V.append(('Der Schaukasten', v06))


# 07 · Der Kontaktbogen: links ein grosses Plakat, rechts der Text und darunter alle Plakate klein wie auf einem Kontaktbogen.
# Zeigen auf ein kleines: das grosse sinkt weg, das neue steigt auf.
def v07(n):
    gross = ''.join(pl(k, '(max-width:760px) 92vw, 40vw', 'w7-g' + (' an' if j == 0 else ''), extra=' data-k="%s"' % k) for j, (k, ab) in enumerate(PLAKATE))
    klein = ''.join('<div class="w7-k%s" data-k="%s" style="--n:%d"%s>%s<p>%s</p></div>' % (
        ' an' if j == 0 else '', k, j, daten(ab), pl(k, '(max-width:760px) 22vw, 9vw'), E(p_datum(ab))) for j, (k, ab) in enumerate(PLAKATE))
    k0, ab0 = PLAKATE[0]
    return sek(n, '<div class="w7-raster"><div class="w7-gross vauf"><div class="w7-bild">%s</div><div class="w7-unten"><span class="etikett">%s</span><p class="w7-name titel">%s</p><p class="w7-dat">%s</p></div></div><div>%s<div class="w7-bogen vauf">%s</div></div></div>' % (
        gross, E(REIHE), E(p_name(ab0)), E(p_datum(ab0)), kopf(zeig=True, knopf=False), klein) +
        '<div class="knoepfe" style="margin-top:34px">%s</div>' % B.knopf('Instagram der Bar', B.HAUS['instagram']))
V.append(('Der Kontaktbogen', v07))


# 08 · Das Heft: das Plakat ist eine Karte mit Vorder- und Rückseite. Zeigen auf einen Abend in der Liste
# dreht die Karte um, auf der Rückseite liegt das Plakat des neuen Abends.
def v08(n):
    li = ''.join('<div class="w8-z%s" data-k="%s" data-name="%s" data-dat="%s" style="--n:%d"><span>%s</span><b>%s</b><small>%s</small></div>' % (
        ' an' if i == 0 else '', k, E(nm), E(d), i, E(d), E(nm), E(r)) for i, (d, nm, r, k) in enumerate(LINEUP))
    karte = '<div class="w8-karte" data-karte><div class="w8-seite w8-vorn">%s</div><div class="w8-seite w8-hinten">%s</div></div>' % (
        pl(LINEUP[0][3], '(max-width:760px) 80vw, 34vw'), pl(LINEUP[1][3], '(max-width:760px) 80vw, 34vw'))
    bilder = '<div hidden data-quellen>%s</div>' % ''.join('<img data-k="%s" data-lq="%s" data-src="%s">' % (k, mache(k)['lq'], 'assets/bild/%s?v=%s' % ([f for w, f in mache(k)['stufen'] if w >= 960][0], B.V)) for k, ab in PLAKATE)
    return sek(n, '<div class="w8-raster"><div>%s<div class="w8-liste">%s</div></div><div class="w8-tisch vauf">%s<p class="w8-unter"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></p></div></div>%s' % (
        kopf(zeig=True), li, karte, E(REIHE), E(LINEUP[0][1]), E(LINEUP[0][0]), bilder))
V.append(('Das Heft', v08))


# 09 · Die Plattenkiste: die Plakate stehen hintereinander wie Platten in einer Kiste, das neueste vorn, von jedem sieht man den oberen Rand mit Datum.
# Beim Auftritt klappen sie nacheinander hoch. Zeigen zieht ein Plakat aus der Kiste nach oben.
def v09(n):
    m = len(PLAKATE)
    p = ''.join('<div class="w9-p" style="--n:%d;--h:%d;z-index:%d">%s<p class="w9-reiter"><span>%s</span>%s</p></div>' % (
        j, m - 1 - j, j, pl(k, '(max-width:760px) 70vw, 30vw'), E(p_datum(ab)), E(p_name(ab))) for j, (k, ab) in enumerate(PLAKATE[::-1]))
    return sek(n, '<div class="w9-raster">%s<div class="w9-kiste vauf"><div class="w9-reihe">%s</div><div class="w9-front"><span>SESSION</span><span>WALK ON THE WILD SIDE</span></div></div></div>' % (kopf(), p))
V.append(('Die Plattenkiste', v09))


# 10 · Der letzte Abend vorn: das Datum des letzten Abends in Hero-Grösse, Ziffer für Ziffer gesetzt, daneben sein Plakat.
# Darunter alle Abende davor in einer Reihe; Zeigen holt einen nach vorn.
def v10(n):
    def ziffern(t):
        return ''.join('<span style="--b:%d">%s</span>' % (i, E(c)) for i, c in enumerate(t))
    gross = ''.join(pl(k, '(max-width:760px) 80vw, 30vw', 'w10-g' + (' an' if j == 0 else ''), extra=' data-k="%s"' % k) for j, (k, ab) in enumerate(PLAKATE))
    reihe = ''.join('<div class="w10-k%s" data-k="%s" style="--n:%d" data-dat="%s" data-name="%s" data-r="%s">%s<p><span>%s</span>%s</p></div>' % (
        ' an' if i == 0 else '', k, i, E(d[:6]), E(nm), E(r), pl(k, '(max-width:760px) 30vw, 11vw'), E(d), E(nm)) for i, (d, nm, r, k) in enumerate(LINEUP))
    d0, n0, r0, k0 = LINEUP[0]
    vorn = '<div class="w10-vorn vauf"><div class="w10-links"><span class="etikett">Der letzte Abend</span><p class="w10-dat titel">%s</p><p class="w10-jahr">%s</p><p class="w10-name titel">%s</p><p class="w10-r">%s</p></div><div class="w10-bild">%s</div></div>' % (
        ziffern(d0[:6]), E(d0[6:]), E(n0), E(r0), gross)
    return sek(n, kopf(zeig=True) + vorn + '<div class="w10-reihe vauf">%s</div>' % reihe)
V.append(('Der letzte Abend vorn', v10))


# 11 · Wand an Wand: alle Plakate über die ganze Breite, ohne Abstand, zwei Reihen. Sie drehen sich in einer Welle von links oben her ins Bild.
# Zeigen schiebt von unten ein cremefarbenes Band mit Datum und Name ins Plakat.
def v11(n):
    t = ''.join('<div class="w11-p" style="--n:%d">%s<p class="w11-band"><span>%s</span><b>%s</b></p></div>' % (
        (j % 4) + (j // 4), pl(k, '(max-width:760px) 50vw, 25vw'), E(p_datum(ab)), E(p_name(ab))) for j, (k, ab) in enumerate(PLAKATE))
    return sek(n, '<div class="innen">%s</div><div class="w11-wand vauf">%s</div>' % (kopf(), t), innen=False)
V.append(('Wand an Wand', v11))


# 12 · Aus der Tiefe: die Bühne steht, die Plakate hängen hintereinander im Raum, abwechselnd links und rechts.
# Beim Scrollen fährt man an ihnen vorbei, vom ersten Abend 2025 bis zum letzten.
def v12(n):
    p = ''.join('<div class="w12-p" style="--n:%d;--x:%s">%s<p class="w12-tag"><span>%s</span>%s</p></div>' % (
        j, ('-1', '1')[j % 2], pl(k, '(max-width:760px) 50vw, 22vw'), E(p_datum(ab)), E(p_name(ab))) for j, (k, ab) in enumerate(PLAKATE[::-1]))
    return sek(n, '<div class="innen">%s</div><div class="w12-pin" data-pin><div class="w12-buehne"><div class="w12-raum">%s</div><p class="w12-reihe etikett">%s</p></div></div>' % (
        kopf(), p, E(REIHE)), innen=False)
V.append(('Aus der Tiefe', v12))


# 13 · Die Litfasssäule: die Plakate rundherum auf einer Säule, oben die Kappe mit SESSION.
# Die Säule dreht sich mit dem Scrollen; daneben steht, welcher Abend gerade vorn ist.
def v13(n):
    m = len(PLAKATE)
    s = ''.join('<div class="w13-p" style="--a:%.2fdeg">%s</div>' % (360 * j / m, pl(k, '(max-width:760px) 34vw, 18vw')) for j, (k, ab) in enumerate(PLAKATE))
    tx = ''.join('<div class="w13-t%s" style="--n:%d"><p class="w13-dat titel">%s</p><p class="w13-name">%s</p></div>' % (
        ' an' if j == 0 else '', j, E(p_datum(ab)), E(p_name(ab))) for j, (k, ab) in enumerate(PLAKATE))
    return sek(n, '<div class="w13-raster"><div>%s<div class="w13-vorn"><span class="etikett">Gerade vorn</span>%s</div></div><div class="w13-ort vauf" data-saeule><div class="w13-kappe"><span>SESSION</span></div><div class="w13-saeule">%s</div><div class="w13-fuss"></div></div></div>' % (
        kopf(), tx, s))
V.append(('Die Litfasssäule', v13))


# 14 · Das Plakat folgt der Hand: die Liste der Abende über die ganze Breite, Datum gross. Wer über eine Zeile fährt,
# dem folgt das Plakat dieses Abends schräg neben dem Zeiger. Auf dem Handy steht ein kleines Plakat vorn in der Zeile.
def v14(n):
    li = ''.join('<div class="w14-z" data-k="%s" style="--n:%d"><span class="w14-dat titel">%s</span><b>%s</b><small>%s</small>%s</div>' % (
        k, i, E(d), E(nm), E(r), pl(k, '20vw', 'w14-mini')) for i, (d, nm, r, k) in enumerate(LINEUP))
    folg = '<div class="w14-folg" aria-hidden="true">%s</div>' % ''.join(pl(k, '26vw', 'w14-f', extra=' data-k="%s"' % k) for k, ab in PLAKATE)
    return sek(n, kopf(zeig=True) + '<div class="w14-liste vauf">%s</div>%s' % (li, folg))
V.append(('Das Plakat folgt der Hand', v14))


# 15 · Im Plakat: der Abschnitt wird selbst zum SESSION-Plakat. Creme, rote Wellen, Schrift in Ultramarin.
# Die Wellen ziehen beim Scrollen langsamer als die Seite; die Plakate stehen als kleine Abzüge im Feld und steigen auf.
def v15(n):
    wellen = ''
    for i in range(14):
        y0 = -60 + i * 64
        pts = ' '.join('%s%.1f,%.1f' % ('M' if x == 0 else 'L', x, y0 + 26 * math.sin(x / 130 + i * .5)) for x in range(0, 1610, 20))
        wellen += '<path d="%s"/>' % pts
    sv = '<svg class="w15-wellen" viewBox="0 0 1600 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">%s</svg>' % wellen
    g = ''.join('<div class="w15-p" style="--n:%d">%s<p><span>%s</span>%s</p></div>' % (
        j, pl(k, '(max-width:760px) 40vw, 14vw'), E(p_datum(ab)), E(p_name(ab))) for j, (k, ab) in enumerate(PLAKATE))
    return sek(n, '<div class="w15-flaeche" data-wellen>%s<div class="innen w15-innen"><div class="w15-schild">%s</div><div class="w15-raster vauf">%s</div><p class="w15-fuss"><span>WALK ON THE WILD SIDE</span><span>HAASEMANNSTR. 13 · 30449 HANNOVER</span></p></div></div>' % (
        sv, kopf(), g), innen=False)
V.append(('Im Plakat', v15))


def seite(n):
    h = unter.programm()
    if n:
        a = h.rfind('<section', 0, h.find('id="session"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/s.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/s.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
