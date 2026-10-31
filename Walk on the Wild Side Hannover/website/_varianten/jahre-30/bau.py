# Walk on the Wild Side · Das Haus · «Was bisher geschah.» (id="seit2017"), 30 Fassungen (31.10.2026).
# Robert: «Gib mir für den ganzen Abschnitt nochmal 30 Visualisierungsmöglichkeiten. Diese ganzen Bilder so untereinander, das gefällt mir doch nicht.»
# Texte und Jahre wörtlich aus unter.py, Fotos = Satz A (ja-2018 … ja-2027). Keine Fassung stapelt die Bilder untereinander.
# Je Fassung eigene Anordnung und eigene Bewegung, nur transform, alles deckend. Wechsel mit ← → (varianten-nav.js).
# Aufruf: python3 _varianten/jahre-30/bau.py → 00.html … 30.html
import os, sys, json, re
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, LOGO, mache, img_tag

ORD = '_varianten/jahre-30'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('j30.css', 'j30.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('haus.html').read()
a = basis.index('<section class="kap hell auf" id="seit2017">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]
KOPF = HEUTE[HEUTE.index('<div class="innen">') + len('<div class="innen">'):HEUTE.index('<div class="jf-g">')]

src = open('unter.py').read()
blk = src[src.index('    jahre = ['):src.index('    stimmen = [')]
JAHRE = re.findall(r"\('(\d{4})', '([^']+)'\)", blk)
assert [j for j, _ in JAHRE] == ['2018', '2023', '2024', '2025', '2027'], JAHRE
FOTO = {'2018': 'ja-2018', '2023': 'ja-2023', '2024': 'ja-2024', '2025': 'ja-2025', '2027': 'ja-2027'}
POS = {'2018': '50% 50%', '2023': '50% 50%', '2024': '50% 45%', '2025': '50% 30%', '2027': '50% 50%'}


def F(j, cls='', sizes='30vw', stil=''):
    k = FOTO[j]
    return '<figure class="j3-f %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img_tag(k, sizes, extra=' style="object-position:%s"' % POS[j]))


def URL(j):
    return 'assets/bild/%s' % mache(FOTO[j])['stufen'][-1][1]


Z = lambda j: '<span class="j-z">%s</span>' % j
P = lambda t: '<p>%s</p>' % E(t)


def kap(n, inner, dunkel=False, breit=False, roh=False):
    """roh: inner steht direkt in der Section (für Bühnen, die über die ganze Breite gehen)."""
    hülle = inner if roh else '<div class="%s">%s</div>' % ('j3-breit' if breit else 'innen', inner)
    return '<section class="kap %s auf j3 f%02d" id="seit2017" data-v="%d"><div class="innen">%s</div>%s</section>' % (
        '' if dunkel else 'hell', n, n, KOPF, hülle)


def jede(fn):
    return ''.join(fn(i, j, t) for i, (j, t) in enumerate(JAHRE))


V = []

# 01 Bildreihe: fünf Hochbilder nebeneinander, gleiche Höhe; darunter je Jahr Zahl und Satz. Die Bilder steigen nacheinander herauf, der Text folgt.
V.append(('Bildreihe', lambda n: kap(n, '<div class="v01">%s</div>' % jede(lambda i, j, t:
    '<div class="jx" style="--n:%d">%s<div class="jt">%s%s</div></div>' % (i, F(j, 'v01-b', '(max-width:900px) 46vw, 19vw'), Z(j), P(t))), breit=True)))

# 02 Bühne: links ein grosses Bild, das beim Scrollen vom nächsten Jahr überschoben wird; rechts zieht der Text im selben Takt mit.
V.append(('Bühne', lambda n: kap(n, '<div class="pin" style="--h:420vh"><div class="pin-s"><div class="innen v02">'
    '<div class="v02-rahmen">%s</div><div class="v02-fenster"><div class="v02-spur">%s</div></div></div></div></div>' % (
        jede(lambda i, j, t: F(j, 'v02-b', '(max-width:900px) 92vw, 40vw', '--n:%d' % i)),
        jede(lambda i, j, t: '<div class="v02-t">%s%s</div>' % (Z(j), P(t)))), roh=True)))

# 03 Querfahrt: der Abschnitt bleibt stehen, die fünf Jahre fahren als breite Tafeln (Bild links, Text rechts) von rechts nach links durch.
V.append(('Querfahrt', lambda n: kap(n, '<div class="pin" style="--h:380vh"><div class="pin-s"><div class="v03-band">%s</div></div></div>' %
    jede(lambda i, j, t: '<div class="v03-t">%s<div class="jt"><span class="etikett">%d von 5</span>%s%s</div></div>' % (F(j, 'v03-b', '(max-width:900px) 60vw, 26vw'), i + 1, Z(j), P(t))), roh=True)))

# 04 Filmstreifen: ein schwarzer Streifen mit Lochrand, je Jahr ein Bild; der Streifen zieht von rechts ein, darunter die Jahre in Spalten.
V.append(('Filmstreifen', lambda n: kap(n, '<div class="v04-streifen"><div class="v04-zug">%s</div></div><div class="v04-txt">%s</div>' % (
    jede(lambda i, j, t: '<div class="v04-k"><span class="v04-nr">WS %s · %d</span>%s</div>' % (j, i + 1, F(j, 'v04-b', '(max-width:900px) 40vw, 18vw'))),
    jede(lambda i, j, t: '<div class="jx" style="--n:%d">%s%s</div>' % (i, Z(j), P(t)))), dunkel=True, breit=True)))

# 05 Mosaik: Bilder und Texttafeln Wand an Wand in einem Raster, 2018 quer oben, darunter Bild, Text, Bild; die Tafeln schweben gestaffelt herauf.
def v05(n):
    (j0, t0), (j1, t1), (j2, t2), (j3, t3), (j4, t4) = JAHRE
    T = lambda j, t, c, i: '<div class="jx v05-t %s" style="--n:%d">%s%s</div>' % (c, i, Z(j), P(t))
    B = lambda j, c, i: '<div class="jx %s" style="--n:%d">%s</div>' % (c, i, F(j, 'v05-b', '(max-width:900px) 92vw, 34vw'))
    return kap(n, '<div class="v05">%s%s%s%s%s%s%s%s%s%s</div>' % (
        B(j0, 'a', 0), T(j0, t0, 't1 nacht', 1), B(j1, 'b', 2), T(j1, t1, 't2', 3), B(j2, 'c', 4), T(j2, t2, 't3 nacht', 5),
        B(j3, 'd', 6), T(j3, t3, 't4 rot', 7), T(j4, t4, 't5', 8), B(j4, 'e', 9)))
V.append(('Mosaik', v05))

# 06 Plakatwand: fünf Plakate Kante an Kante, oben das Foto, unten Papier mit Jahr und Satz; jedes wird schräg angeschlagen und zieht sich gerade.
V.append(('Plakatwand', lambda n: kap(n, '<div class="v06">%s</div>' % jede(lambda i, j, t:
    '<div class="jx" style="--n:%d;--w:%s">%s<div class="v06-p"><span class="v06-k">Walk on the Wild Side</span>%s%s</div></div>' % (
        i, ['-1.6deg', '1.2deg', '-.8deg', '1.8deg', '-1.2deg'][i], F(j, 'v06-b', '(max-width:900px) 46vw, 19vw'), Z(j), P(t))), breit=True)))

# 07 Kontaktbogen: ein dunkler Bogen mit den fünf Abzügen und Bildnummern; um jede Jahreszahl zieht sich ein roter Fettstiftkreis.
KREIS = '<svg class="v07-kr" viewBox="0 0 200 100" preserveAspectRatio="none" aria-hidden="true"><path d="M18 58 C 14 26, 70 8, 112 10 C 160 12, 192 30, 186 56 C 180 84, 120 94, 80 90 C 40 86, 10 74, 22 48" pathLength="100"/></svg>'
V.append(('Kontaktbogen', lambda n: kap(n, '<div class="v07"><div class="v07-kopf"><span>Kontaktbogen</span><span>Wild Side · Haasemannstraße 13</span></div><div class="v07-g">%s</div></div>' % jede(lambda i, j, t:
    '<div class="jx" style="--n:%d"><span class="v07-nr">%dA</span>%s<div class="v07-z">%s%s</div>%s</div>' % (i, 12 + i * 4, F(j, 'v07-b', '(max-width:900px) 46vw, 19vw'), Z(j), KREIS, P(t))), dunkel=True, breit=True)))

# 08 Das Buch: ein aufgeschlagenes Buch, links das Foto, rechts der Text; beim Scrollen wird Seite um Seite umgeblättert.
def v08(n):
    links = lambda j: '<div class="v08-s v08-l">%s</div>' % F(j, 'v08-b', '(max-width:900px) 46vw, 30vw')
    rechts = lambda i, j, t: '<div class="v08-s v08-r"><span class="etikett">Seit 2018 · %d</span>%s%s<span class="v08-sz">%d</span></div>' % (i + 1, Z(j), P(t), (i + 1) * 2)
    blaetter = ''.join('<div class="v08-bl" data-bl="%d" style="--n:%d"><div class="v08-vorn">%s</div><div class="v08-hinten">%s</div></div>' % (
        i, i, rechts(i - 1, *JAHRE[i - 1]), links(JAHRE[i][0])) for i in range(1, 5))
    return kap(n, '<div class="pin" style="--h:400vh"><div class="pin-s"><div class="v08"><div class="v08-buch">%s%s%s</div></div></div></div>' % (
        links(JAHRE[0][0]), rechts(4, *JAHRE[4]), blaetter), roh=True)
V.append(('Das Buch', v08))

# 09 Zickzack: eine goldene Linie quer, die Bilder abwechselnd darüber und darunter, der Text jeweils auf der anderen Seite; alles wächst von der Linie weg.
V.append(('Zickzack', lambda n: kap(n, '<div class="v09">%s</div>' % jede(lambda i, j, t:
    '<div class="jx %s" style="--n:%d"><div class="v09-o">%s</div><span class="v09-r"><b class="v09-p"></b></span><div class="v09-u">%s</div></div>' % (
        'gerade' if i % 2 == 0 else 'ungerade', i,
        F(j, 'v09-b', '(max-width:900px) 46vw, 18vw') if i % 2 == 0 else '<div class="jt">%s%s</div>' % (Z(j), P(t)),
        '<div class="jt">%s%s</div>' % (Z(j), P(t)) if i % 2 == 0 else F(j, 'v09-b', '(max-width:900px) 46vw, 18vw'))), breit=True)))

# 10 Bild in der Zahl: je Jahr eine riesige Jahreszahl, durch die man das Foto sieht, daneben der Satz; zum Schieben, Tafel für Tafel.
V.append(('Bild in der Zahl', lambda n: kap(n, '<div class="v10-band">%s</div><p class="v10-h">Seitlich schieben</p>' % jede(lambda i, j, t:
    '<div class="jx v10-t" style="--n:%d"><span class="v10-z" style="background-image:url(%s)">%s</span><div class="jt"><span class="etikett">%d von 5</span>%s</div></div>' % (
        i, URL(j), j, i + 1, P(t))), roh=True)))

# 11 Postkarten: fünf Karten, oben drei, unten zwei breitere; Foto links, rechts Jahr, Satz und Stempel; jede wird auf den Tisch gelegt.
STEMPEL = '<span class="v11-st"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="44"/><circle cx="50" cy="50" r="34"/></svg><b>Linden</b></span>'
V.append(('Postkarten', lambda n: kap(n, '<div class="v11">%s</div>' % jede(lambda i, j, t:
    '<div class="jx v11-k k%d" style="--n:%d;--w:%s">%s<div class="jt">%s%s%s</div></div>' % (
        i, i, ['-1.4deg', '.9deg', '-.6deg', '1.1deg', '-.9deg'][i], F(j, 'v11-b', '(max-width:900px) 40vw, 16vw'), STEMPEL, Z(j), P(t))), breit=True)))

# 12 Schaufenster: die fünf Bilder als Scheiben eines langen Fensters mit schwarzen Sprossen, der Name in Goldschrift über dem Glas; auf dem Sims die Jahre.
V.append(('Schaufenster', lambda n: kap(n, '<div class="v12"><div class="v12-fenster"><span class="v12-name">Walk on the Wild Side</span><div class="v12-glas">%s</div></div><div class="v12-sims">%s</div></div>' % (
    jede(lambda i, j, t: '<div class="v12-sch" style="--n:%d">%s</div>' % (i, F(j, 'v12-b', '(max-width:900px) 40vw, 19vw'))),
    jede(lambda i, j, t: '<div class="jx" style="--n:%d">%s%s</div>' % (i, Z(j), P(t)))), breit=True)))

# 13 Drehbühne: das Jahr in der Mitte steht gross, die anderen stehen schräg daneben; beim Scrollen dreht sich die Reihe weiter, der Text wechselt mit.
V.append(('Drehbühne', lambda n: kap(n, '<div class="pin" style="--h:400vh"><div class="pin-s"><div class="v13"><div class="v13-reihe">%s</div><div class="v13-txt">%s</div></div></div></div>' % (
    jede(lambda i, j, t: '<div class="v13-k" data-k="%d">%s</div>' % (i, F(j, 'v13-b', '(max-width:900px) 60vw, 26vw'))),
    jede(lambda i, j, t: '<div class="v13-t" data-k="%d">%s%s</div>' % (i, Z(j), P(t)))), dunkel=True, roh=True)))

# 14 Barkarte: eine dunkle Karte wie die Getränkekarte, oben eine Reihe Bilder, darunter die Jahre wie Einträge mit Goldpunkten zur Zahl.
V.append(('Barkarte', lambda n: kap(n, '<div class="v14"><div class="v14-kopf"><span class="logo v14-logo">%s</span><span class="etikett">Die Jahre · Haasemannstraße 13</span></div><div class="v14-bilder">%s</div><div class="v14-liste">%s</div></div>' % (
    LOGO, jede(lambda i, j, t: F(j, 'v14-b', '(max-width:900px) 40vw, 17vw', '--n:%d' % i)),
    jede(lambda i, j, t: '<div class="jx" style="--n:%d"><div class="v14-z"><span class="v14-w">Kapitel %d</span><i></i>%s</div>%s</div>' % (i, i + 1, Z(j), P(t)))))))

# 15 Zeitungsseite: Titelseite mit grossem Aufmacherfoto 2018, die anderen vier Jahre als Meldungen mit eigenem Bild in Spalten.
def v15(n):
    j0, t0 = JAHRE[0]
    return kap(n, '<div class="v15"><div class="v15-kopf"><span>Lindener Abendblatt</span><b class="titel">Die Bar an der Ecke</b><span>Haasemannstraße 13 · seit 2018</span></div>'
        '<div class="v15-auf jx" style="--n:0">%s<div class="jt">%s%s</div></div><div class="v15-sp">%s</div></div>' % (
            F(j0, 'v15-b0', '(max-width:900px) 92vw, 56vw'), Z(j0), P(t0),
            ''.join('<div class="jx" style="--n:%d">%s%s%s</div>' % (i + 1, F(j, 'v15-b', '(max-width:900px) 46vw, 20vw'), Z(j), P(t)) for i, (j, t) in enumerate(JAHRE[1:]))))
V.append(('Zeitungsseite', v15))

# 16 Galerie mit Kopf: 2018 als breites Bild über die ganze Breite mit dem Text daneben, darunter die vier anderen Jahre in einer Reihe.
def v16(n):
    j0, t0 = JAHRE[0]
    return kap(n, '<div class="v16"><div class="v16-kopf jx" style="--n:0">%s<div class="jt">%s%s</div></div><div class="v16-reihe">%s</div></div>' % (
        F(j0, 'v16-b0', '(max-width:900px) 92vw, 64vw'), Z(j0), P(t0),
        ''.join('<div class="jx" style="--n:%d">%s<div class="jt">%s%s</div></div>' % (i + 1, F(j, 'v16-b', '(max-width:900px) 46vw, 22vw'), Z(j), P(t)) for i, (j, t) in enumerate(JAHRE[1:]))), breit=True)
V.append(('Galerie mit Kopf', v16))

# 17 Treppe: die fünf Jahre steigen von links unten nach rechts oben wie die Stufen zur Empore, Bild auf der Stufe, Text darunter.
V.append(('Treppe', lambda n: kap(n, '<div class="v17">%s</div>' % jede(lambda i, j, t:
    '<div class="jx" style="--n:%d">%s<div class="jt">%s%s</div><i class="v17-st"></i></div>' % (i, F(j, 'v17-b', '(max-width:900px) 46vw, 18vw'), Z(j), P(t))), breit=True)))

# 18 Abreisskalender: ein Block mit fünf Blättern; beim Scrollen hebt sich Blatt um Blatt nach oben weg und gibt das nächste Jahr frei.
V.append(('Abreisskalender', lambda n: kap(n, '<div class="pin" style="--h:400vh"><div class="pin-s"><div class="innen v18"><div class="v18-block">%s</div></div></div></div>' %
    ''.join('<div class="v18-bl" data-k="%d" style="--n:%d;z-index:%d"><div class="v18-ring"><i></i><i></i><i></i></div>%s<div class="jt">%s%s</div></div>' % (
        i, i, 10 - i, F(j, 'v18-b', '(max-width:900px) 46vw, 28vw'), Z(j), P(t)) for i, (j, t) in enumerate(JAHRE)), roh=True)))

# 19 Laufband: oben läuft ein Band mit den fünf Bildern langsam durch, jedes mit seinem Jahr; darunter stehen die fünf Jahre ruhig in Spalten.
V.append(('Laufband', lambda n: kap(n, '<div class="v19-band"><div class="v19-zug">%s</div></div><div class="innen"><div class="v19-txt">%s</div></div>' % (
    ''.join('<div class="v19-k"%s>%s</div>' % (' aria-hidden="true"' if r else '', F(j, 'v19-b', '360px')) for r in range(2) for j, t in JAHRE),
    jede(lambda i, j, t: '<div class="jx" style="--n:%d">%s%s</div>' % (i, Z(j), P(t)))), roh=True)))

# 20 Leuchttisch: fünf Dias in weissen Rähmchen auf einem beleuchteten Tisch, das Jahr von Hand auf dem Rahmen; der Text darunter.
V.append(('Leuchttisch', lambda n: kap(n, '<div class="v20"><div class="v20-tisch">%s</div><div class="v20-txt">%s</div></div>' % (
    jede(lambda i, j, t: '<div class="v20-dia" style="--n:%d;--w:%s"><div class="v20-fe">%s</div><span class="v20-hand">%s</span></div>' % (
        i, ['-3deg', '2deg', '-1deg', '3deg', '-2deg'][i], F(j, 'v20-b', '(max-width:900px) 40vw, 16vw'), j)),
    jede(lambda i, j, t: '<div class="jx" style="--n:%d">%s</div>' % (i, P(t)))), breit=True)))

# 21 Schachbrett: zwei Reihen à fünf Felder, Bild und Text wechseln sich ab, Kante an Kante; die Felder klappen nacheinander auf.
V.append(('Schachbrett', lambda n: kap(n, '<div class="v21">%s%s</div>' % (
    ''.join('<div class="jx v21-f" style="--n:%d">%s</div>' % (i, F(j, 'v21-b', '(max-width:900px) 46vw, 20vw') if i % 2 == 0 else '<div class="v21-t">%s%s</div>' % (Z(j), P(t))) for i, (j, t) in enumerate(JAHRE)),
    ''.join('<div class="jx v21-f" style="--n:%d">%s</div>' % (i + 5, '<div class="v21-t">%s%s</div>' % (Z(j), P(t)) if i % 2 == 0 else F(j, 'v21-b', '(max-width:900px) 46vw, 20vw')) for i, (j, t) in enumerate(JAHRE))), breit=True)))

# 22 Eintrittskarten: je Jahr ein Ticket mit Bild-Abriss oben, Zahl und Satz unten, gestanzte Kerbe dazwischen; die Tickets kommen wie aus dem Drucker.
V.append(('Eintrittskarten', lambda n: kap(n, '<div class="v22">%s</div>' % jede(lambda i, j, t:
    '<div class="jx" style="--n:%d"><div class="v22-o">%s<span class="v22-nr">Nr. %s</span></div><div class="v22-u"><span class="etikett">Walk on the Wild Side · Einlass</span>%s%s</div></div>' % (
        i, F(j, 'v22-b', '(max-width:900px) 46vw, 19vw'), j, Z(j), P(t))), dunkel=True, breit=True)))

# 23 Fünfteiler randlos: die fünf Bilder über die ganze Breite ohne Fugen; darunter ein dunkles Band mit Jahr und Satz in denselben Spalten.
V.append(('Fünfteiler randlos', lambda n: kap(n, '<div class="v23"><div class="v23-bilder">%s</div><div class="v23-band">%s</div></div>' % (
    jede(lambda i, j, t: '<div class="v23-s" style="--n:%d">%s</div>' % (i, F(j, 'v23-b', '20vw'))),
    jede(lambda i, j, t: '<div class="jx" style="--n:%d">%s%s</div>' % (i, Z(j), P(t)))), roh=True)))

# 24 Typoband: die fünf Jahreszahlen riesig in einer Zeile über die Breite, darunter eine Bildreihe, darunter die Sätze; die Zahlen steigen aus dem Schlitz.
V.append(('Typoband', lambda n: kap(n, '<div class="v24"><div class="v24-z">%s</div><div class="v24-b">%s</div><div class="v24-t">%s</div></div>' % (
    jede(lambda i, j, t: '<span class="v24-zz" style="--n:%d"><span>%s</span></span>' % (i, j)),
    jede(lambda i, j, t: F(j, 'v24-bb', '(max-width:900px) 40vw, 19vw', '--n:%d' % i)),
    jede(lambda i, j, t: '<div class="jx" style="--n:%d">%s</div>' % (i, P(t)))), breit=True)))

# 25 Anfang und danach: links 2018 als grosses Bild mit Text («der Anfang»), rechts die vier Jahre danach als Raster zwei mal zwei.
def v25(n):
    j0, t0 = JAHRE[0]
    return kap(n, '<div class="v25"><div class="v25-l jx" style="--n:0">%s<div class="jt"><span class="etikett">Der Anfang</span>%s%s</div></div><div class="v25-r">%s</div></div>' % (
        F(j0, 'v25-b0', '(max-width:900px) 92vw, 44vw'), Z(j0), P(t0),
        ''.join('<div class="jx" style="--n:%d">%s<div class="jt">%s%s</div></div>' % (i + 1, F(j, 'v25-b', '(max-width:900px) 46vw, 14vw'), Z(j), P(t)) for i, (j, t) in enumerate(JAHRE[1:]))), breit=True)
V.append(('Anfang und danach', v25))

# 26 Leporello: ein gefaltetes Heft im Zickzack quer über die Breite, Bild- und Textfelder im Wechsel; beim Hereinkommen faltet es sich auf.
V.append(('Leporello', lambda n: kap(n, '<div class="v26">%s</div>' % ''.join(
    '<div class="v26-f %s" style="--n:%d">%s</div>' % ('bild' if k % 2 == 0 else 'txt', k,
        F(JAHRE[k // 2][0], 'v26-b', '(max-width:900px) 46vw, 11vw') if k % 2 == 0 else '<div class="jt">%s%s</div>' % (Z(JAHRE[k // 2][0]), P(JAHRE[k // 2][1])))
    for k in range(10)) + '<p class="v10-h">Seitlich schieben</p>', roh=True)))

# 27 Farbsäulen: fünf gleich hohe Säulen in den Farben der Bar (Nacht, Plakatrot, Ultramarin), oben das Foto, darunter Jahr und Satz; sie wachsen nacheinander herauf.
V.append(('Farbsäulen', lambda n: kap(n, '<div class="v27">%s</div>' % jede(lambda i, j, t:
    '<div class="jx c%d" style="--n:%d">%s<div class="jt">%s%s</div></div>' % (i, i, F(j, 'v27-b', '(max-width:900px) 46vw, 19vw'), Z(j), P(t))), breit=True)))

# 28 Rückbar-Regal: zwei beleuchtete Regalböden (oben zwei, unten drei) wie hinter der Theke, die Bilder stehen darauf, die Jahre als Schildchen an der Kante; das Licht geht Boden für Boden an.
def v28(n):
    reihe = lambda paar: ''.join('<div class="jx v28-p" style="--n:%d">%s<div class="v28-s">%s%s</div></div>' % (i, F(j, 'v28-b', '(max-width:900px) 40vw, 17vw'), Z(j), P(t)) for i, (j, t) in paar)
    e = list(enumerate(JAHRE))
    return kap(n, '<div class="v28"><div class="v28-boden">%s<i class="v28-licht"></i></div><div class="v28-boden">%s<i class="v28-licht"></i></div></div>' % (reihe(e[:2]), reihe(e[2:])), dunkel=True, breit=True)
V.append(('Rückbar-Regal', v28))

# 29 Welle: die fünf Bilder nebeneinander in versetzter Höhe wie eine Welle; beim Scrollen laufen sie verschieden schnell, der Text sitzt unter jedem Bild.
V.append(('Welle', lambda n: kap(n, '<div class="v29">%s</div>' % jede(lambda i, j, t:
    '<div class="jx" style="--n:%d;--a:%s">%s<div class="jt">%s%s</div></div>' % (i, ['0', '1', '-1', '1', '0'][i], F(j, 'v29-b', '(max-width:900px) 46vw, 19vw'), Z(j), P(t))), breit=True)))

# 30 Tiefenflug: der Abschnitt bleibt stehen, die Jahre kommen wie bei einer Kamerafahrt aus der Tiefe auf dich zu und ziehen vorbei, das nächste wartet dahinter.
V.append(('Tiefenflug', lambda n: kap(n, '<div class="pin" style="--h:420vh"><div class="pin-s"><div class="v30">%s</div></div></div>' %
    ''.join('<div class="v30-e" data-k="%d" style="z-index:%d">%s<div class="jt">%s%s</div></div>' % (i, 10 - i, F(j, 'v30-b', '(max-width:900px) 70vw, 34vw'), Z(j), P(t)) for i, (j, t) in enumerate(JAHRE)), dunkel=True, roh=True)))

assert len(V) == 30, len(V)
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPFZ = '<link rel="stylesheet" href="%s/j30.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPFZ + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 30</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/j30.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('31 Seiten gebaut')
