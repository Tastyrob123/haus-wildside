# Walk on the Wild Side · Feiern-Seite, Abschnitt «Die ganze Bar · Eine Nacht, nur für euch.» (id="bar"): 15 Darstellungen (30.10.2026).
# Robert: «gib 15 visuelle alternative darstellungen von dem abschnitt». 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte Wort für Wort aus unter.tafel() (unten geprüft), nur echte Fotos der Bar.
# Bewegung nur über transform, alles von Anfang an deckend; Scroll-Getriebenes in einem Takt in f.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/feiern-bar-15/bau.py → 00.html … 15.html
import os, sys, json, html, math
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/feiern-bar-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('f.css', 'f.js', 'nav.js'))))

TEXT = 'Ab dreissig Gästen schliesst die Bar für euch. Von 19 bis 2 Uhr gehört euch der ganze Raum: unter der Decke, an der Theke, auf der Empore. Für Geburtstag, Firmenfeier, Weihnachtsfeier oder ein Gastro-Event, mit eurer eigenen Atmosphäre. Zwei Wege, den Abend zu planen.'
WEG_E, WEG_T = 'Weg 1 · Pauschale', 'Ein Preis pro Gast.'
WEG_S = 'Von 19 bis 2 Uhr steht offen, was eure Kategorie umfasst. Wer länger bleibt: ab 2 Uhr jede angefangene Stunde 10 Euro pro Person.'
KAT = unter.PAUSCHALE
_q = open('unter.py').read()
for _s in (TEXT, WEG_E, WEG_T, WEG_S, "kz('Die ganze Bar', 'Geschlossene Gesellschaft', 0), h2(['Eine Nacht,', 'nur für euch.'])"):
    assert _s in _q, 'Text weicht ab: ' + _s[:40]
ORTE = [('decke-raum', 'Unter der Decke'), ('theke', 'An der Theke'), ('an-empore', 'Auf der Empore')]   # die drei Orte aus dem Satz
GLAS = ['an-glaeser', 'wf-highball', 'an-negroni']                                                       # je Kategorie ein Bild
DINGE = KAT[-1][2].split(' · ')                                                                      # alle Posten, aus der vollsten Kategorie
for _k in KAT:
    DINGE += [d for d in _k[2].split(' · ') if d not in DINGE]


def kopf(cls='', groesse='t-kap'):
    return '<div class="fq-kopf %s">%s%s<p class="text sw" style="--i:1">%s</p></div>' % (
        cls, B.kz('Die ganze Bar', 'Geschlossene Gesellschaft', 0), B.h2(['Eine Nacht,', 'nur für euch.'], groesse), E(TEXT))


def weg(cls=''):
    return '<div class="fq-weg sw %s" style="--i:2"><span class="etikett">%s</span><h3 class="titel t-mittel">%s</h3><p class="text">%s</p></div>' % (cls, E(WEG_E), E(WEG_T), E(WEG_S))


def preis(p, cls='fq-preis'):
    return '<div class="%s"><b class="titel">%s €</b><small>pro Person</small></div>' % (cls, p)


def kat(j, cls='fq-kat', mit_preis=True, vorne=''):
    k, t, z, p = KAT[j]
    return '<div class="%s" style="--n:%d">%s<span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p>%s</div>' % (
        cls, j, vorne, E(k), E(t), E(z), preis(p) if mit_preis else '')


def fo(k, sizes, cls='', stil='', pos='50% 50%'):
    return '<figure class="ff %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, B.img_tag(k, sizes, extra=' style="object-position:%s"' % pos))


def sek(n, inner, cls=''):
    return '<section class="kap auf fb b%02d %s" id="bar" data-g="%d"><div class="innen">%s</div></section>' % (n, cls, n, inner)


V = []


# 01 · Die Uhr: links Kopf und Pauschale, rechts ein Zifferblatt, auf dem der Bogen von 19 bis 2 Uhr in Gold liegt.
# Beim Auftritt fährt der Zeiger einmal von 19 bis 2 Uhr. Darunter die drei Kategorien als Spalten mit grossem Preis.
def v01(n):
    def pt(a, r):
        a = math.radians(a)
        return 200 + r * math.sin(a), 200 - r * math.cos(a)
    striche = ''.join('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (pt(h * 30, 172) + pt(h * 30, 158 if h % 3 else 150)) for h in range(12))
    (x0, y0), (x1, y1) = pt(210, 186), pt(60, 186)
    bogen = '<path class="u01-bogen" d="M%.1f %.1f A186 186 0 1 1 %.1f %.1f"/>' % (x0, y0, x1, y1)
    (lx0, ly0), (lx1, ly1) = pt(196, 120), pt(80, 120)
    uhr = ('<div class="u01-uhr vauf"><svg viewBox="0 0 400 400" aria-hidden="true"><circle cx="200" cy="200" r="196" class="u01-scheibe"/>%s<g class="u01-striche">%s</g>'
           '<text x="%.1f" y="%.1f">19 Uhr</text><text x="%.1f" y="%.1f">2 Uhr</text></svg><i class="u01-zeiger"></i><i class="u01-nabe"></i></div>') % (bogen, striche, lx0, ly0, lx1, ly1)
    sp = ''.join(kat(j, 'fq-kat u01-k') for j in range(3))
    return sek(n, '<div class="u01-oben"><div>%s%s</div>%s</div><div class="u01-spalten">%s</div>' % (kopf(), weg(), uhr, sp))
V.append((1, 'Die Uhr', v01))


# 02 · Drei Gläser: drei hohe Säulen, in jeder steigt eine Füllung, je Kategorie höher; oben Name und Liste, in der Füllung der Preis.
def v02(n):
    s = ''.join('<div class="g02-s" style="--n:%d;--h:%s">%s<i class="g02-fuell"></i>%s</div>' % (
        j, h, '<div class="g02-t"><span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p></div>' % (E(k), E(t), E(z)), preis(p, 'fq-preis g02-p'))
        for j, ((k, t, z, p), h) in enumerate(zip(KAT, ('30%', '44%', '58%'))))
    bilder = '<div class="g02-bilder">%s%s</div>' % (fo('an-party-sw', '(max-width:760px) 60vw, 26vw', 'g02-b1', pos='50% 40%'), fo('an-negroni', '(max-width:760px) 40vw, 14vw', 'g02-b2'))
    return sek(n, '<div class="g02-oben"><div>%s%s</div>%s</div><div class="g02-reihe vauf">%s</div>' % (kopf(), weg(), bilder, s))
V.append((2, 'Drei Gläser', v02))


# 03 · Das Schild an der Tür: rechts hängt an zwei Schnüren ein cremefarbenes Schild «Geschlossene Gesellschaft», es schwingt beim Auftritt ein.
# Darunter je Kategorie ein Foto Wand an Wand mit Text und Preis darunter.
def v03(n):
    schild = '<div class="s03-haken vauf"><i class="s03-schnur s03-l"></i><i class="s03-schnur s03-r"></i><div class="s03-schild"><span class="etikett">Die ganze Bar</span><p class="titel">Geschlossene Gesellschaft</p><small>Von 19 bis 2 Uhr</small></div></div>'
    sp = ''.join('<div class="s03-k">%s%s</div>' % (fo(GLAS[j], '(max-width:760px) 92vw, 30vw', 's03-f'), kat(j)) for j in range(3))
    return sek(n, '<div class="s03-oben"><div>%s%s</div>%s</div><div class="s03-reihe">%s</div>' % (kopf(), weg(), schild, sp))
V.append((3, 'Das Schild an der Tür', v03))


# 04 · Das Zahlwerk: die drei Preise riesig nebeneinander, jede Ziffer rollt wie im Zählwerk aus dem Schlitz auf ihren Wert.
# Darunter Name und Liste; ganz unten vier Fotos des Abends Wand an Wand.
def v04(n):
    def rolle(ziffer, j):
        z = ''.join('<span>%d</span>' % i for i in range(10))
        return '<span class="z04-rolle"><span class="z04-band" style="--z:%s;--d:%d">%s</span></span>' % (ziffer, j, z)
    sp = ''.join('<div class="z04-k" style="--n:%d"><div class="z04-zahl titel">%s<small>€</small></div><small class="z04-pp">pro Person</small><span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p></div>' % (
        j, ''.join(rolle(c, j * 2 + i) for i, c in enumerate(p)), E(k), E(t), E(z)) for j, (k, t, z, p) in enumerate(KAT))
    wand = ''.join(fo(k, '(max-width:760px) 46vw, 24vw', pos=pos) for k, pos in (('an-party-sw', '50% 40%'), ('an-party', '50% 30%'), ('feste-anstossen', '50% 40%'), ('voll', '50% 50%')))
    return sek(n, '<div class="z04-oben">%s%s</div><div class="z04-reihe vauf">%s</div><div class="z04-wand">%s</div>' % (kopf(), weg(), sp, wand))
V.append((4, 'Das Zahlwerk', v04))


# 05 · Der Paravent: Decke, Theke, Empore als drei hohe Bilder Wand an Wand, die sich beim Auftritt wie ein Paravent aufklappen.
# Darunter eine helle Tafel mit den drei Kategorien, durch Goldlinien getrennt.
def v05(n):
    p = ''.join('<figure class="p05-f p05-%d" style="--lq:url(%s)">%s<figcaption class="etikett">%s</figcaption></figure>' % (
        j, mache(k)['lq'], B.img_tag(k, '(max-width:760px) 92vw, 32vw'), E(t)) for j, (k, t) in enumerate(ORTE))
    tafel = ''.join(kat(j, 'fq-kat p05-k') for j in range(3))
    return sek(n, '<div class="p05-oben">%s%s</div><div class="p05-wand vauf">%s</div><div class="p05-tafel">%s</div>' % (kopf(), weg(), p, tafel))
V.append((5, 'Der Paravent', v05))


# 06 · Der leere Raum: links das Bild des leeren Raums am frühen Abend, beim Scrollen zieht es sich aus der Nähe in seinen Rahmen zurück.
# Rechts Kopf und Pauschale, darunter die Kategorien als drei offene Spalten zwischen Goldlinien.
def v06(n):
    raum = '<div class="r06-rahmen" data-zoom>%s</div>' % fo('pf-raum', '(max-width:760px) 92vw, 50vw', 'r06-f')
    sp = ''.join(kat(j, 'fq-kat r06-k') for j in range(3))
    return sek(n, '<div class="r06-oben">%s<div>%s%s</div></div><div class="r06-spalten">%s</div>' % (raum, kopf(), weg(), sp))
V.append((6, 'Der leere Raum', v06))


# 07 · Plakate an der Wand: die Kategorien als drei cremefarbene Plakate wie die der Bar, rote Schrift, leicht schief.
# Beim Auftritt wird eines nach dem anderen an die Wand geschlagen.
def v07(n):
    pl = ''.join('<div class="k07-p" style="--n:%d;--w:%sdeg"><div class="k07-blatt"><span class="k07-et">%s</span><h3 class="titel">%s</h3><p>%s</p><p class="k07-preis titel">%s €</p><small>pro Person</small></div></div>' % (
        j, w, E(k), E(t), E(z), p) for j, ((k, t, z, p), w) in enumerate(zip(KAT, (-2.2, 1.4, -1.2))))
    return sek(n, '<div class="k07-oben"><div>%s%s</div>%s</div><div class="k07-wand vauf">%s</div>' % (
        kopf(), weg(), fo('an-party-sw', '(max-width:760px) 92vw, 40vw', 'k07-f', pos='50% 40%'), pl))
V.append((7, 'Plakate an der Wand', v07))


# 08 · Die Bierdeckel: je Kategorie ein runder Deckel mit rotem Ring und dem Preis in der Mitte.
# Die Deckel fallen beim Auftritt gedreht auf den Tisch und kommen gerade zur Ruhe.
def v08(n):
    d = ''.join('<div class="d08-p" style="--n:%d"><div class="d08-deckel"><span class="d08-et">%s</span><b class="titel">%s €</b><small>pro Person</small></div><h3 class="titel">%s</h3><p>%s</p></div>' % (
        j, E(k), p, E(t), E(z)) for j, (k, t, z, p) in enumerate(KAT))
    bilder = '<div class="d08-bilder">%s%s</div>' % (fo('an-party', '(max-width:760px) 46vw, 20vw', pos='50% 30%'), fo('an-sours', '(max-width:760px) 46vw, 20vw'))
    return sek(n, '<div class="d08-oben"><div>%s%s</div>%s</div><div class="d08-tisch vauf">%s</div>' % (kopf(), weg(), bilder, d))
V.append((8, 'Die Bierdeckel', v08))


# 09 · Bild zum Text: links steht ein Bilderrahmen still, rechts laufen Kopf, Pauschale und die drei Kategorien vorbei.
# Zu jedem Schritt schiebt sich von unten das passende Foto in den Rahmen.
def v09(n):
    bilder = [('an-party-sw', '50% 40%'), ('feste-anstossen', '50% 40%'), (GLAS[0], '50% 50%'), (GLAS[1], '50% 50%'), (GLAS[2], '50% 50%')]
    rahmen = ''.join('<div class="w09-b" style="--n:%d">%s</div>' % (j, fo(k, '(max-width:760px) 92vw, 44vw', pos=pos)) for j, (k, pos) in enumerate(bilder))
    schritte = '<div class="w09-s">%s</div><div class="w09-s">%s</div>%s' % (kopf(), weg(), ''.join('<div class="w09-s">%s</div>' % kat(j, 'fq-kat w09-k') for j in range(3)))
    return sek(n, '<div class="w09-raster" data-wechsel><div class="w09-links"><div class="w09-rahmen">%s</div></div><div class="w09-rechts">%s</div></div>' % (rahmen, schritte))
V.append((9, 'Bild zum Text', v09))


# 10 · Die Übersicht: eine Tafel, oben die drei Kategorien mit Preis, links jede Getränkeart, in den Feldern ein Goldpunkt, wo sie enthalten ist.
# Beim Auftritt füllen sich die Punkte Spalte für Spalte.
def v10(n):
    kopfz = '<div class="t10-z t10-kz"><span></span>%s</div>' % ''.join('<div class="t10-h"><span class="etikett">%s</span><p class="titel">%s</p>%s</div>' % (E(k), E(t), preis(p)) for k, t, z, p in KAT)
    zeilen = ''
    for d in DINGE:
        zellen = ''.join('<span class="t10-c">%s</span>' % ('<i class="t10-punkt" style="--n:%d"></i>' % j if d in KAT[j][2].split(' · ') else '<i class="t10-leer"></i>') for j in range(3))
        zeilen += '<div class="t10-z"><span class="t10-d">%s</span>%s</div>' % (E(d[0].upper() + d[1:]), zellen)
    return sek(n, '<div class="t10-oben"><div>%s%s</div>%s</div><div class="t10-tafel vauf">%s%s</div>' % (
        kopf(), weg(), fo('an-party-sw', '(max-width:760px) 92vw, 36vw', 't10-f', pos='50% 40%'), kopfz, zeilen))
V.append((10, 'Die Übersicht', v10))


# 11 · Drei Ebenen: die Kategorien als drei breite Bänder untereinander, jedes länger als das davor, rechts ein hohes Foto.
# Beim Auftritt fahren die Bänder aus der Wand bis auf ihre Länge aus.
def v11(n):
    b = ''.join('<div class="e11-b" style="--n:%d;--w:%s"><i class="e11-platte"></i><div class="e11-in"><div><span class="etikett">%s</span><h3 class="titel">%s</h3></div><p>%s</p>%s</div></div>' % (
        j, w, E(k), E(t), E(z), preis(p)) for j, ((k, t, z, p), w) in enumerate(zip(KAT, ('78%', '89%', '100%'))))
    return sek(n, '<div class="e11-oben">%s%s</div><div class="e11-raster"><div class="e11-baender vauf">%s</div>%s</div>' % (
        kopf(), weg(), b, fo('an-party', '(max-width:760px) 92vw, 30vw', 'e11-f', pos='50% 30%')))
V.append((11, 'Drei Ebenen', v11))


# 12 · Die Einladung: eine helle Klappkarte, vorn «Die ganze Bar». Beim Auftritt klappt der Deckel nach links auf,
# innen links der Satz und die Pauschale, rechts die drei Kategorien. Darunter drei Fotos des Abends.
def v12(n):
    innen_r = ''.join(kat(j, 'fq-kat c12-k') for j in range(3))
    deckel = '<div class="c12-deckel"><div class="c12-vorn"><span class="etikett">Geschlossene Gesellschaft</span><p class="titel">Die ganze Bar</p><small>Von 19 bis 2 Uhr</small></div><div class="c12-hinten">%s%s</div></div>' % (kopf(), weg())
    fotos = ''.join(fo(k, '(max-width:760px) 92vw, 30vw', pos=pos) for k, pos in (('an-party-sw', '50% 40%'), ('feste-anstossen', '50% 40%'), ('an-party', '50% 30%')))
    return sek(n, '<div class="c12-karte vauf"><div class="c12-rechts">%s</div>%s</div><div class="c12-fotos">%s</div>' % (innen_r, deckel, fotos))
V.append((12, 'Die Einladung', v12))


# 13 · Die Bildwand: Fotos des Abends und die drei Kategorien als Felder in einem dichten Raster, ohne Lücke.
# Beim Auftritt setzen sich die Felder von der Mitte nach aussen in die Wand.
def v13(n):
    felder = [('f', 'an-party-sw', 'w13-a', '50% 40%'), ('k', 0, 'w13-k1', ''), ('f', 'feste-anstossen', 'w13-b', '50% 40%'),
              ('f', 'an-party', 'w13-c', '50% 30%'), ('k', 1, 'w13-k2', ''), ('k', 2, 'w13-k3', ''), ('f', 'silvester', 'w13-d', '50% 40%'), ('f', 'voll', 'w13-e', '50% 50%')]
    ab = {'w13-a': 2, 'w13-k1': 0, 'w13-b': 1, 'w13-c': 1, 'w13-k2': 0, 'w13-k3': 0, 'w13-d': 2, 'w13-e': 2}
    h = ''
    for art, x, cls, pos in felder:
        if art == 'f':
            h += '<div class="w13-feld %s" style="--n:%d">%s</div>' % (cls, ab[cls], fo(x, '(max-width:760px) 92vw, 30vw', pos=pos))
        else:
            h += '<div class="w13-feld %s" style="--n:%d">%s</div>' % (cls, ab[cls], kat(x, 'fq-kat w13-kat'))
    return sek(n, '<div class="w13-oben">%s%s</div><div class="w13-wand vauf">%s</div>' % (kopf(), weg(), h))
V.append((13, 'Die Bildwand', v13))


# 14 · Die Einlasskarten: je Kategorie eine helle Karte mit Abriss, links der Preis, rechts Name und Liste.
# Sie liegen erst als Stapel übereinander und legen sich beim Auftritt untereinander aus.
def v14(n):
    t = ''.join('<div class="e14-t" style="--n:%d;--w:%sdeg"><div class="e14-abriss"><span class="e14-et">%s</span><b class="titel">%s €</b><small>pro Person</small></div><div class="e14-haupt"><h3 class="titel">%s</h3><p>%s</p></div></div>' % (
        j, w, E(k), p, E(t_), E(z)) for j, ((k, t_, z, p), w) in enumerate(zip(KAT, (-2.5, 1.8, -1))))
    bilder = '<div class="e14-bilder">%s%s</div>' % (fo('an-party-sw', '(max-width:760px) 60vw, 26vw', pos='50% 40%'), fo('an-glaeser', '(max-width:760px) 40vw, 16vw'))
    return sek(n, '<div class="e14-oben">%s%s</div><div class="e14-unten">%s<div class="e14-stapel vauf">%s</div></div>' % (kopf(), bilder, weg(), t))
V.append((14, 'Die Einlasskarten', v14))


# 15 · Die grosse Schrift: der Titel über die ganze Breite, darunter Satz und Pauschale nebeneinander,
# ein Streifen aus vier Fotos, die beim Scrollen verschieden schnell steigen, und die Kategorien als Zeilen zwischen Goldlinien.
def v15(n):
    fotos = ''.join('<div class="g15-b" style="--t:%s">%s</div>' % (t, fo(k, '(max-width:760px) 46vw, 24vw', pos=pos)) for (k, pos), t in zip(
        (('an-party-sw', '50% 40%'), ('an-party', '50% 30%'), ('feste-anstossen', '50% 40%'), ('voll', '50% 50%')), ('.10', '-.06', '.14', '-.04')))
    zeilen = ''.join('<div class="g15-z"><span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p>%s</div>' % (E(k), E(t), E(z), preis(p)) for k, t, z, p in KAT)
    kp = '<div class="fq-kopf g15-kopf">%s%s</div>' % (B.kz('Die ganze Bar', 'Geschlossene Gesellschaft', 0), B.h2(['Eine Nacht,', 'nur für euch.'], 'g15-titel'))
    return sek(n, '%s<div class="g15-zwei"><p class="text sw" style="--i:1">%s</p>%s</div><div class="g15-streifen" data-streifen>%s</div><div class="g15-liste">%s</div>' % (
        kp, E(TEXT), weg(), fotos, zeilen))
V.append((15, 'Die grosse Schrift', v15))


def seite(n):
    h = unter.tafel()
    eintrag = dict((nr, (nm, f)) for nr, nm, f in V)
    if n:
        a = h.rfind('<section', 0, h.find('id="bar"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + eintrag[n][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[nr, nm] for nr, nm, _ in V]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/f.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, V[-1][0], E(eintrag[n][0] if n else 'Heutiger Stand'))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/f.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in [0] + [nr for nr, _, _ in V]:
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', V[-1][0])
