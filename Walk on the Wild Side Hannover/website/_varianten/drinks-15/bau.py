# Walk on the Wild Side · Startseite, Abschnitt «Was magst du?» (20:00 An der Theke): 15 Fassungen (29.10.2026).
# Robert: «gib mir 15 visuelle alternative darstelungen für den abschnitt». 00 = heutiger Stand.
# Jede Fassung ist die echte Startseite, nur dieser Abschnitt getauscht. Inhalte (Text, Fragen, Antworten, Bilder) bleiben die der Seite.
# Wechsel mit ← → (nav.js), man bleibt am Abschnitt. Aufruf: python3 _varianten/drinks-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
from bilder import mache

E = html.escape
ORD = '_varianten/drinks-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

DATEN = E(json.dumps(B.GESPRAECH, ensure_ascii=False))
GLAESER = sorted(set(a['bild'] for a in B.GESPRAECH))
FR = {k: (e, opt) for k, e, opt in B.FRAGEN}
KZ = B.kz('20:00', 'An der Theke', 0)
TITEL = B.h2(['Was magst du?'])
TEXT = '<p class="text sw" style="--i:1">Eine Getränkekarte gibt es im Wild Side nicht. Wer an die Theke kommt, wird gefragt: sauer oder süss, klar oder cremig, Gin oder lieber gar kein Alkohol. Daraus wird ein Drink, den es nur an diesem Abend gibt. Probier es hier schon einmal aus.</p>'
ZITAT = '<p class="ge-zitat sw" style="--i:6">«Du sagst mir, was du magst, ich mache dir einen Drink.»<small>Momo, hinter der Theke</small></p>'
KNOPF = '<div class="knoepfe sw" style="--i:7">%s</div>' % B.knopf('Alle Drinks', 'drinks.html')
UEBER = B.ueber('Und irgendwann schaust du nach oben.')
SATZ = '<p class="ge-satz"></p>'
MOMO = '<span class="etikett">Momo würde sagen</span>'


def wahl(k, cls=''):
    return '<div class="wahl %s" data-frage="%s">%s</div>' % (cls, k, ''.join('<button type="button" data-w="%s">%s</button>' % (w, E(t)) for w, t in FR[k][1]))


def zeile(k, i=2):
    return '<div class="ge-frage sw" style="--i:%d"><span class="etikett">%s</span>%s</div>' % (i, E(FR[k][0]), wahl(k))


ZEILEN = ''.join(zeile(k, n + 2) for n, k in enumerate(('geschmack', 'art', 'basis')))


def foto(k, sizes, cls='foto', extra=''):
    d = mache(k)
    return '<figure class="%s" data-k="%s" style="--lq:url(%s)"%s>%s</figure>' % (cls, k, d['lq'], extra, B.img_tag(k, sizes))


def glas(sizes='160px', cls=''):
    """Der Glas-Stapel der Seite: wild.js schiebt das passende Glas von unten herein."""
    return '<div class="ge-glas %s">%s</div>' % (cls, ''.join(foto(k, sizes) for k in GLAESER))


def stapel(sizes, cls):
    """Ein eigener Glas-Stapel für Fassungen mit eigener Bewegung (v.js)."""
    return '<div class="%s">%s</div>' % (cls, ''.join(foto(k, sizes) for k in GLAESER))


def sektion(n, inner, cls=''):
    return '<section class="kap auf vx vs%02d %s" id="drinks"><div class="innen" data-gespraech=\'%s\' data-v="%d">%s</div>%s</section>' % (n, cls, DATEN, n, inner, UEBER)


V = []

# 01 · Das Gespräch: Momos Fragen als Zeilen eines Gesprächs, deine Wahl antwortet; Momo «tippt», dann kommt sein Satz.
def v01(n):
    log = ''.join('<p class="v1-m sw" style="--i:%d"><span class="etikett">Momo</span>%s</p><div class="v1-du sw" style="--i:%d">%s</div>' % (2 + 2 * j, q, 3 + 2 * j, wahl(k))
                  for j, (k, q) in enumerate((('geschmack', 'Lieber sauer, süss, bitter oder rauchig?'), ('art', 'Und im Glas: klar, cremig oder spritzig?'),
                                              ('basis', 'Und was darf rein?'))))
    return sektion(n, '''<div class="v1">
<div class="v1-text">%s%s%s
<div class="v1-log">%s
<div class="v1-antw sw" style="--i:8"><div><span class="etikett">Momo</span><span class="v1-tippt" aria-hidden="true"><i></i><i></i><i></i></span>%s</div>%s</div></div>
%s</div>
<div class="v1-bild kachel leise sw" style="--i:1;--lq:url(%s)">%s</div>
</div>''' % (KZ, TITEL, TEXT, log, SATZ, glas('180px', 'v1-glas'), KNOPF, mache('momo-giesst')['lq'], B.img_tag('momo-giesst', '(max-width:900px) 100vw, 40vw')))
V.append(('Das Gespräch', v01))

# 02 · Ein Satz zum Antippen: die drei Wahlen stehen in einem grossen Satz, jedes Wort rollt beim Antippen zur nächsten Möglichkeit.
def v02(n):
    def wort(k):
        opt = FR[k][1]
        return '<button type="button" class="v2-wort" data-ziel="%s"><span class="v2-roll">%s</span></button>' % (k, ''.join('<span>%s</span>' % E(t) for w, t in opt))
    return sektion(n, '''<div class="v2">
<div class="v2-text">%s%s%s
<p class="v2-satz sw" style="--i:2"><span>Lieber</span>%s<span>im Glas</span>%s<span>darin</span>%s</p>
<p class="v2-tipp sw" style="--i:3">Tipp auf ein Wort, und Momo fragt weiter.</p>
<div class="v2-wahlen" hidden>%s%s%s</div>
<div class="v2-antw sw" style="--i:4">%s%s</div>%s</div>
<div class="v2-glas sw" style="--i:1">%s</div>
</div>''' % (KZ, TITEL, TEXT, wort('geschmack'), wort('art'), wort('basis'), wahl('geschmack'), wahl('art'), wahl('basis'), MOMO, SATZ, KNOPF,
             glas('(max-width:900px) 100vw, 40vw', 'v2-stapel')))
V.append(('Ein Satz zum Antippen', v02))

# 03 · Drei Spalten: Lieber, Im Glas, Darin als drei senkrechte Listen nebeneinander, ein Goldstrich gleitet zur Wahl.
def v03(n):
    spalten = ''.join('<div class="v3-sp sw" style="--i:%d"><span class="etikett">%s</span><div class="v3-liste">%s<i class="v3-strich"></i></div></div>' % (
        2 + j, E(FR[k][0]), wahl(k)) for j, k in enumerate(('geschmack', 'art', 'basis')))
    return sektion(n, '''<div class="v3">
<div class="v3-bild kachel leise sw" style="--i:1;--lq:url(%s)">%s</div>
<div class="v3-rechts">%s%s%s
<div class="v3-spalten">%s</div>
<div class="ge-antwort sw" style="--i:5"><div>%s%s</div>%s</div>%s</div>
</div>''' % (mache('momo-giesst')['lq'], B.img_tag('momo-giesst', '(max-width:900px) 100vw, 38vw'), KZ, TITEL, TEXT, spalten, MOMO, SATZ, glas('150px'), KNOPF))
V.append(('Drei Spalten, ein Goldstrich', v03))

# 04 · Das Bildpaar: oben Momo und das Glas Wand an Wand, das Glas dreht sich wie eine Karte um; darunter die Fragen in einer Reihe.
def v04(n):
    seite = lambda c: '<div class="v4-seite %s">%s</div>' % (c, ''.join(foto(k, '(max-width:900px) 50vw, 30vw') for k in GLAESER))
    reihe = ''.join('<div class="v4-fr sw" style="--i:%d"><span class="etikett">%s</span>%s</div>' % (3 + j, E(FR[k][0]), wahl(k)) for j, k in enumerate(('geschmack', 'art', 'basis')))
    return sektion(n, '''<div class="v4">
<div class="v4-kopf"><div>%s%s%s</div>%s</div>
<div class="v4-paar flaeche"><div class="kachel leise" style="--lq:url(%s)">%s</div>
<div class="v4-karte"><div class="v4-dreh">%s%s</div></div></div>
<div class="v4-fragen">%s</div>
<div class="v4-unten sw" style="--i:6"><div>%s%s</div>%s</div>
</div>''' % (KZ, TITEL, TEXT, ZITAT, mache('momo-giesst')['lq'], B.img_tag('momo-giesst', '(max-width:900px) 50vw, 30vw'), seite('vorn'), seite('hinten'),
             reihe, MOMO, SATZ, KNOPF))
V.append(('Momo und das Glas, die Karte dreht sich', v04))

# 05 · Bis an den Rand: das Glas der Antwort füllt die linke Hälfte bis an den Bildschirmrand und wechselt von unten; rechts das Gespräch.
def v05(n):
    return sektion(n, '''<div class="v5">
<div class="v5-buehne sw" style="--i:1">%s<p class="v5-unter">%s%s</p></div>
<div class="v5-text">%s%s%s<div class="ge-fragen">%s</div>%s%s</div>
</div>''' % (glas('(max-width:900px) 100vw, 52vw', 'v5-glas'), MOMO, SATZ, KZ, TITEL, TEXT, ZEILEN, ZITAT, KNOPF), 'v5-sek')
V.append(('Das Glas bis an den Rand', v05))

# 06 · Alle Gläser in einer Reihe: neun echte Gläser der Bar Wand an Wand; das passende hebt sich, die anderen treten zurück.
def v06(n):
    reihe = ''.join(foto(k, '(max-width:900px) 34vw, 14vw', 'foto v6-g') for k in GLAESER)
    return sektion(n, '''<div class="v6">
<div class="v6-oben"><div>%s%s%s</div><div class="ge-fragen v6-fragen">%s</div></div>
<div class="v6-reihe sw" style="--i:5">%s</div>
<div class="v6-antw sw" style="--i:6">%s%s</div>
<div class="v6-fuss">%s%s</div>
</div>''' % (KZ, TITEL, TEXT, ZEILEN, reihe, MOMO, SATZ, ZITAT, KNOPF))
V.append(('Alle Gläser in einer Reihe', v06))

# 07 · Momos Satz: sein Satz steht gross wie ein Titel; die Antwort erscheint Wort für Wort.
def v07(n):
    return sektion(n, '''<div class="v7">
<div class="v7-text">%s
<blockquote class="v7-zitat titel">%s</blockquote>
<p class="v7-wer sw" style="--i:3">Momo, hinter der Theke</p>
<div class="v7-mitte"><h2 class="titel t-mittel sw" style="--i:4">Was magst du?</h2>%s</div>
<div class="ge-fragen">%s</div>
<div class="v7-antw sw" style="--i:6"><div>%s<p class="ge-satz v7-satz"></p></div>%s</div>%s</div>
<div class="v7-bild kachel leise sw" style="--i:1;--lq:url(%s)">%s</div>
</div>''' % (KZ, B.zl(['«Du sagst mir,', 'was du magst,', 'ich mache dir', 'einen Drink.»'], i0=1), TEXT.replace('--i:1', '--i:5'), ZEILEN,
             MOMO, glas('150px'), KNOPF, mache('momo-lacht')['lq'], B.img_tag('momo-lacht', '(max-width:900px) 100vw, 36vw')))
V.append(('Momos Satz als Titel', v07))

# 08 · Die Walzen: jede Frage eine Walze wie an einem Zahlenschloss; drehen mit den Pfeilen oder durch Antippen der Nachbarwörter.
def v08(n):
    def walze(k, j):
        return '<div class="v8-w sw" style="--i:%d"><span class="etikett">%s</span><button type="button" class="v8-pf" data-d="-1" aria-label="hoch">%s</button><div class="v8-fenster">%s</div><button type="button" class="v8-pf" data-d="1" aria-label="runter">%s</button></div>' % (
            2 + j, E(FR[k][0]), B.PFEIL, wahl(k, 'v8-rolle'), B.PFEIL)
    return sektion(n, '''<div class="v8">
<div class="v8-bild kachel leise sw" style="--i:1;--lq:url(%s)">%s</div>
<div class="v8-rechts">%s%s%s
<div class="v8-walzen">%s%s%s</div>
<div class="ge-antwort sw" style="--i:6"><div>%s%s</div>%s</div>%s</div>
</div>''' % (mache('momo-giesst')['lq'], B.img_tag('momo-giesst', '(max-width:900px) 100vw, 38vw'), KZ, TITEL, TEXT,
             walze('geschmack', 0), walze('art', 1), walze('basis', 2), MOMO, SATZ, glas('150px'), KNOPF))
V.append(('Die Walzen', v08))

# 09 · Eine Frage nach der anderen: die Bühne zeigt nur eine Frage, gross; nach jeder Wahl fährt die nächste herein, am Ende das Glas.
def v09(n):
    folien = ''.join('<div class="v9-folie"><p class="v9-nr">%d von 3</p><p class="v9-frage titel">%s</p>%s</div>' % (j + 1, q, wahl(k, 'v9-wahl'))
                     for j, (k, q) in enumerate((('geschmack', 'Lieber …'), ('art', 'Im Glas …'), ('basis', 'Darin …'))))
    folien += '<div class="v9-folie v9-ende"><div class="v9-ende-text">%s%s<button type="button" class="weiter v9-nochmal">Noch einmal fragen %s</button></div>%s</div>' % (
        MOMO, SATZ, B.PFEIL, glas('(max-width:900px) 40vw, 18vw', 'v9-glas'))
    return sektion(n, '''<div class="v9">
<div class="v9-bild kachel leise sw" style="--i:1;--lq:url(%s)">%s</div>
<div class="v9-rechts">%s%s%s
<div class="v9-buehne platte sw" style="--i:2"><div class="v9-band">%s</div><div class="v9-punkte"><i class="an"></i><i></i><i></i><i></i></div></div>%s</div>
</div>''' % (mache('momo-giesst')['lq'], B.img_tag('momo-giesst', '(max-width:900px) 100vw, 38vw'), KZ, TITEL, TEXT, folien, KNOPF))
V.append(('Eine Frage nach der anderen', v09))

# 10 · Auf hellem Papier: der Abschnitt auf Creme; die Fragen als Tabelle mit Goldlinien, die sich ziehen; rechts Momo und das Glas als Paar.
def v10(n):
    tab = ''.join('<div class="v10-z" style="--n:%d"><span class="etikett">%s</span>%s</div>' % (j, E(FR[k][0]), wahl(k)) for j, k in enumerate(('geschmack', 'art', 'basis')))
    return sektion(n, '''<div class="v10">
<div class="v10-text">%s%s%s
<div class="v10-tab staffel">%s</div>
<div class="v10-antw sw" style="--i:5">%s%s</div>%s</div>
<div class="v10-paar flaeche"><div class="kachel leise" style="--lq:url(%s)">%s</div>%s</div>
</div>''' % (KZ, TITEL, TEXT, tab, MOMO, SATZ, KNOPF.replace('class="knopf ', 'class="knopf hellk '), mache('momo-giesst')['lq'],
             B.img_tag('momo-giesst', '(max-width:900px) 50vw, 24vw'), glas('(max-width:900px) 50vw, 24vw', 'v10-glas')), 'hell')
V.append(('Auf hellem Papier', v10))

# 11 · Die Wortwand: alle Möglichkeiten als eine grosse Schriftwand; die Wahl leuchtet auf, der Rest tritt zurück.
def v11(n):
    wand = ''.join('<span class="v11-gr"><sup>%s</sup>%s</span>' % (E(FR[k][0]), wahl(k, 'v11-wahl')) for k in ('geschmack', 'art', 'basis'))
    return sektion(n, '''<div class="v11">
<div class="v11-oben"><div>%s%s%s</div><div class="v11-bild kachel leise sw" style="--i:1;--lq:url(%s)">%s</div></div>
<div class="v11-wand sw" style="--i:2">%s</div>
<div class="v11-antw sw" style="--i:3"><div>%s%s</div>%s<div>%s%s</div></div>
</div>''' % (KZ, TITEL, TEXT, mache('rueckbar-breit')['lq'], B.img_tag('rueckbar-breit', '(max-width:900px) 100vw, 46vw'), wand, MOMO, SATZ, glas('150px'), ZITAT, KNOPF))
V.append(('Die Wortwand', v11))

# 12 · Das Bild bleibt stehen: links steht Momo, rechts scrollen die drei Fragen vorbei; bei der letzten wird aus Momo das Glas.
def v12(n):
    bl = ''.join('<div class="v12-block" data-schritt="%d"><p class="v12-nr">%s</p><p class="titel v12-frage">%s</p>%s</div>' % (j + 1, '%d von 3' % (j + 1), E(FR[k][0]) + ' …', wahl(k, 'v12-wahl'))
                 for j, k in enumerate(('geschmack', 'art', 'basis')))
    return sektion(n, '''<div class="v12">
<div class="v12-links"><div class="v12-halt"><div class="v12-stapel">%s%s</div></div></div>
<div class="v12-rechts"><div class="v12-block v12-start" data-schritt="0">%s%s%s</div>%s
<div class="v12-block v12-schluss" data-schritt="4">%s%s%s%s</div></div>
</div>''' % (foto('momo-giesst', '(max-width:900px) 100vw, 46vw', 'foto v12-momo an'), ''.join(foto(k, '(max-width:900px) 100vw, 46vw') for k in GLAESER),
             KZ, TITEL, TEXT, bl, MOMO, SATZ, ZITAT, KNOPF))
V.append(('Das Bild bleibt stehen', v12))

# 13 · Geschlossenes Raster: Momo, Text, drei Fragen, Antwort, Glas und Zitat als Platten Kante an Kante, keine leere Ecke.
def v13(n):
    pl = lambda k, j: '<div class="platte v13-f v13-%s" style="--n:%d"><span class="etikett">%s</span>%s</div>' % (k, j, E(FR[k][0]), wahl(k, 'v13-wahl'))
    return sektion(n, '''<div class="v13 staffel">
<div class="kachel leise v13-momo" style="--n:0;--lq:url(%s)">%s</div>
<div class="platte v13-kopf" style="--n:1">%s%s%s</div>
%s%s%s
<div class="kachel v13-glasbox" style="--n:5">%s</div>
<div class="platte v13-antw" style="--n:6">%s%s%s</div>
<div class="plakat v13-zitat" style="--n:7"><p class="titel">«Du sagst mir, was du magst, ich mache dir einen Drink.»</p><span class="etikett">Momo, hinter der Theke</span></div>
</div>''' % (mache('momo-giesst')['lq'], B.img_tag('momo-giesst', '(max-width:900px) 100vw, 26vw'), KZ, TITEL.replace('t-kap', 't-mittel'), TEXT,
             pl('geschmack', 2), pl('art', 3), pl('basis', 4), glas('(max-width:900px) 50vw, 26vw', 'v13-glas'), MOMO, SATZ, KNOPF))
V.append(('Geschlossenes Raster', v13))

# 14 · Drei Bilder, dann der Weg: Momo, der Schaum, das Glas der Antwort Wand an Wand; darunter die drei Fragen als Weg mit Goldlinie.
def v14(n):
    st = ''.join('<div class="v14-st" data-st="%d"><i class="v14-punkt"></i><span class="etikett">%s</span>%s</div>' % (j, E(FR[k][0]), wahl(k)) for j, k in enumerate(('geschmack', 'art', 'basis')))
    return sektion(n, '''<div class="v14">
<div class="v14-kopf"><div>%s%s%s</div>%s</div>
<div class="v14-bilder flaeche"><div class="kachel leise" style="--lq:url(%s)">%s</div><div class="kachel leise" style="--lq:url(%s)">%s</div><div class="kachel">%s</div></div>
<div class="v14-weg sw" style="--i:3"><div class="v14-linie"><i></i></div>%s</div>
<div class="v14-fuss sw" style="--i:4"><div class="v14-ziel">%s%s</div>%s</div>
</div>''' % (KZ, TITEL, TEXT, ZITAT, mache('momo-giesst')['lq'], B.img_tag('momo-giesst', '(max-width:900px) 34vw, 30vw'), mache('schaum')['lq'], B.img_tag('schaum', '(max-width:900px) 34vw, 30vw'),
             glas('(max-width:900px) 34vw, 30vw', 'v14-glas'), st, MOMO, SATZ, KNOPF))
V.append(('Drei Bilder, dann der Weg', v14))

# 15 · Das Glas in der Hand: das Glas steht in der Mitte und neigt sich mit der Maus; bei jeder Wahl dreht es sich herein.
def v15(n):
    return sektion(n, '''<div class="v15">
<div class="v15-kopf">%s%s</div>
<div class="v15-drei">
<div class="v15-l"><div class="ge-fragen v15-fragen">%s</div><div class="v15-momo kachel leise sw" style="--i:5;--lq:url(%s)">%s</div></div>
<div class="v15-m sw" style="--i:2"><div class="v15-kipp">%s</div></div>
<div class="v15-r">%s<div class="v15-antw sw" style="--i:5">%s%s</div>%s%s</div>
</div></div>''' % (KZ, TITEL, ZEILEN, mache('momo-lacht')['lq'], B.img_tag('momo-lacht', '(max-width:900px) 100vw, 28vw', extra=' style="object-position:50% 30%"'),
                   stapel('(max-width:900px) 70vw, 34vw', 'v15-stapel'), TEXT, MOMO, SATZ, ZITAT, KNOPF))
V.append(('Das Glas in der Hand', v15))


def seite(n, abschnitt):
    alt = B.kap_gespraech
    if abschnitt:
        B.kap_gespraech = abschnitt
    h = B.seite()
    B.kap_gespraech = alt
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
    name = liste[n][1]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>' % (n, E(name))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, None))
    for j, (name, f) in enumerate(V):
        n = j + 1
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n, lambda f=f, n=n: f(n)))
    print('00 … %02d' % len(V))
