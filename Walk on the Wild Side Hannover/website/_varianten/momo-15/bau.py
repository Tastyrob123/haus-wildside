# Walk on the Wild Side · Startseite, Abschnitt 20:00 «An der Theke»: 15 Fassungen «Momo bei der Arbeit» (29.10.2026).
# Robert: das Auswählen bringt nichts («was soll das bringen da i was auszuwählen?»), gewählt: Momo bei der Arbeit, am Ende das Glas, der Knopf führt zu den Drinks.
# Der Abschnitt zeigt den Ablauf an der Theke in echten Fotos: fragen, zur Flasche greifen, mixen, Schaum, das Glas. Kein Auswählen, kein Spiel.
# Texte nur aus der Seite und den Quellen (CHARAKTER.md, _quelle/presse/np-2021-09-14 für das Studium). 00 = heutiger Stand. Wechsel mit ← →.
# Aufruf: python3 _varianten/momo-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder
from bilder import mache

# Drei weitere echte Fotos der Bar für die Strecke (Google-Eintrag)
bilder.BILDER.update({
    'momo-flaschen': ('google-maps/google-08.jpg', 'Hinter der Theke, vorn die Flaschen der Rückbar'),
    'gereicht':      ('google-maps/google-23.jpg', 'Ein Drink wird über den Tisch gereicht'),
})

E = html.escape
ORD = '_varianten/momo-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

# Die Strecke: Bild, Satz, Zusatz (leer = nur der Satz)
SCHRITTE = [
    ('momo-lacht', 'Erst fragt Momo.', 'Sauer oder süss, klar oder cremig, Gin oder lieber gar kein Alkohol.'),
    ('momo-flaschen', 'Dann greift er zur Flasche.', 'Deine Antwort entscheidet, was ins Glas kommt.'),
    ('momo-giesst', 'Dann mixt er, für dich allein.', 'Momo hat Biotechnologie studiert, bevor er hinter die Bar ging.'),
    ('schaum', 'Zum Schluss der Schaum.', 'Aus dem Siphon, direkt aufs Glas.'),
    ('glas-hand', 'Und dann ist es deiner.', 'Ein Drink, den es nur an diesem Abend gibt.'),
]
POS = {'momo-giesst': '62% 45%', 'momo-lacht': '58% 45%', 'momo-flaschen': '40% 50%'}
KZ = B.kz('20:00', 'An der Theke', 0)
TITEL = B.h2(['Was magst du?'])
TEXT = '<p class="text sw" style="--i:1">Eine Getränkekarte gibt es im Wild Side nicht. Wer an die Theke kommt, wird gefragt, was er mag, und Momo macht daraus einen Drink. So sieht das aus.</p>'
ZITAT = '<p class="ge-zitat sw" style="--i:2">«Du sagst mir, was du magst, ich mache dir einen Drink.»<small>Momo, hinter der Theke</small></p>'
KNOPF = '<div class="knoepfe sw" style="--i:3">%s</div>' % B.knopf('Alle Drinks', 'drinks.html')
UEBER = B.ueber('Und irgendwann schaust du nach oben.')


def img(k, sizes, extra=''):
    p = POS.get(k)
    return B.img_tag(k, sizes, extra=(' style="object-position:%s"' % p if p else '') + extra)


def kachel(k, sizes, cls='', stil=''):
    return '<figure class="kachel leise %s" data-k="%s" style="--lq:url(%s);%s">%s</figure>' % (cls, k, mache(k)['lq'], stil, img(k, sizes))


def foto(k, sizes, cls='foto'):
    return '<figure class="%s" data-k="%s" style="--lq:url(%s)">%s</figure>' % (cls, k, mache(k)['lq'], img(k, sizes))


def satz(t, z, cls='m-satz'):
    return '<div class="%s"><p class="titel">%s</p>%s</div>' % (cls, E(t), '<p class="m-zu">%s</p>' % E(z) if z else '')


def kopf(rechts=ZITAT, cls='m-kopf'):
    return '<div class="%s"><div>%s%s%s</div>%s</div>' % (cls, KZ, TITEL, TEXT, rechts)


def sektion(n, inner, cls=''):
    return '<section class="kap auf mx ms%02d %s" id="drinks"><div class="innen m%02d" data-m="%d">%s</div>%s</section>' % (n, cls, n, n, inner, UEBER)


V = []

# 01 · Filmstreifen: alle fünf Bilder Wand an Wand in einer Reihe, unter jedem sein Satz; sie schweben nacheinander herein.
def v01(n):
    reihe = ''.join('<div class="m1-sch" style="--n:%d">%s%s</div>' % (j, kachel(k, '(max-width:900px) 50vw, 20vw'), satz(t, z)) for j, (k, t, z) in enumerate(SCHRITTE))
    return sektion(n, '%s<div class="m1-reihe staffel">%s</div><div class="m-fuss">%s</div>' % (kopf(), reihe, KNOPF))
V.append(('Filmstreifen', v01))

# 02 · Das Bild bleibt stehen: links steht das Foto, rechts scrollen die Sätze vorbei; zu jedem Satz kommt das nächste Bild von unten.
def v02(n):
    stapel = ''.join(foto(k, '(max-width:900px) 100vw, 46vw', 'foto' + (' an' if j == 0 else '')) for j, (k, t, z) in enumerate(SCHRITTE))
    bl = ''.join('<div class="m2-block" data-j="%d">%s</div>' % (j, satz(t, z)) for j, (k, t, z) in enumerate(SCHRITTE))
    return sektion(n, '''<div class="m2-links"><div class="m2-halt"><div class="m2-stapel">%s</div></div></div>
<div class="m2-rechts"><div class="m2-kopf">%s%s%s</div>%s<div class="m2-ende">%s%s</div></div>''' % (stapel, KZ, TITEL, TEXT, bl, ZITAT, KNOPF))
V.append(('Das Bild bleibt stehen', v02))

# 03 · Das Band zum Blättern: grosse Bilder in einer Reihe bis über den Rand, seitwärts wischen oder mit den Pfeilen.
def v03(n):
    pf = '<div class="m3-pfeile sw" style="--i:2"><button type="button" class="m3-pf" data-d="-1" aria-label="zurück">%s</button><button type="button" class="m3-pf" data-d="1" aria-label="weiter">%s</button></div>' % (B.PFEIL, B.PFEIL)
    band = ''.join('<div class="m3-sch">%s%s</div>' % (kachel(k, '(max-width:900px) 72vw, 34vw'), satz(t, z)) for k, t, z in SCHRITTE)
    return sektion(n, '%s<div class="m3-band sw" style="--i:3">%s</div><div class="m-fuss m3-fuss">%s%s</div>' % (kopf(pf), band, ZITAT, KNOPF), 'm3-sek')
V.append(('Das Band zum Blättern', v03))

# 04 · Nach der Uhr: ein grosses Bild, das von selbst weiterläuft, oben die feinen Striche wie bei einer Geschichte; rechts rollt der Satz mit.
def v04(n):
    stapel = ''.join(foto(k, '(max-width:900px) 100vw, 52vw', 'foto' + (' an' if j == 0 else '')) for j, (k, t, z) in enumerate(SCHRITTE))
    striche = ''.join('<button type="button" data-j="%d" aria-label="%s"><i></i></button>' % (j, E(t)) for j, (k, t, z) in enumerate(SCHRITTE))
    saetze = ''.join('<div class="m4-s%s" data-j="%d">%s</div>' % (' an' if j == 0 else '', j, satz(t, z)) for j, (k, t, z) in enumerate(SCHRITTE))
    return sektion(n, '''<div class="m4-links sw" style="--i:1"><div class="m4-striche">%s</div><div class="m4-stapel">%s</div></div>
<div class="m4-rechts">%s%s%s<div class="m4-saetze">%s</div>%s%s</div>''' % (striche, stapel, KZ, TITEL, TEXT, saetze, ZITAT, KNOPF))
V.append(('Nach der Uhr', v04))

# 05 · Geschlossenes Mosaik: Momo gross, vier Bilder daneben, darunter eine Platte mit dem ganzen Ablauf in einem Absatz und eine mit Momos Satz.
def v05(n):
    ablauf = ' '.join('<b>%s</b> %s' % (E(t), E(z)) for k, t, z in SCHRITTE)
    return sektion(n, '''<div class="m5-kopf">%s%s</div>
<div class="m5 flaeche">%s%s%s%s%s
<div class="platte m5-text"><p class="m5-ablauf">%s</p></div>
<div class="plakat m5-zitat"><p class="titel">«Du sagst mir, was du magst, ich mache dir einen Drink.»</p><span class="etikett">Momo, hinter der Theke</span>%s</div></div>''' % (
        KZ, TITEL, kachel('momo-giesst', '(max-width:900px) 100vw, 50vw', 'm5-a'), kachel('momo-lacht', '25vw', 'm5-b'), kachel('momo-flaschen', '25vw', 'm5-c'),
        kachel('schaum', '25vw', 'm5-d'), kachel('glas-hand', '25vw', 'm5-e'), ablauf, B.knopf('Alle Drinks', 'drinks.html', 'hellk')))
V.append(('Geschlossenes Mosaik', v05))

# 06 · Satz und Bilder im Wechsel: Momos Satz in grossen Zeilen, zwischen den Zeilen die Bilder in Reihen.
def v06(n):
    zeilen = [('«Du sagst mir,', ['momo-lacht', 'momo-flaschen']), ('was du magst,', ['momo-giesst', 'schaum']), ('ich mache dir einen Drink.»', ['glas-hand', 'gereicht'])]
    teile = ''.join('<p class="titel m6-zeile sw">%s</p><div class="m6-reihe flaeche">%s</div>' % (E(z), ''.join(kachel(k, '(max-width:900px) 50vw, 46vw') for k in ks)) for z, ks in zeilen)
    unter = ''.join('<li><b>%s</b> %s</li>' % (E(t), E(z)) for k, t, z in SCHRITTE)
    return sektion(n, '''<div class="m6-kopf">%s%s%s</div>%s<p class="m6-wer">Momo, hinter der Theke</p>
<div class="m-fuss m6-fuss"><ul class="m6-ablauf">%s</ul>%s</div>''' % (KZ, TITEL, TEXT, teile, unter, KNOPF))
V.append(('Satz und Bilder im Wechsel', v06))

# 07 · Gegenlauf: zwei Bildspalten laufen beim Scrollen verschieden schnell, in der Mitte steht der Ablauf.
def v07(n):
    li = ''.join(kachel(k, '(max-width:900px) 50vw, 30vw') for k in ('momo-lacht', 'momo-giesst', 'glas-hand'))
    re_ = ''.join(kachel(k, '(max-width:900px) 50vw, 30vw') for k in ('momo-flaschen', 'schaum', 'gereicht'))
    mitte = ''.join(satz(t, z) for k, t, z in SCHRITTE)
    return sektion(n, '''<div class="m7-sp m7-l" data-tempo="-0.06">%s</div>
<div class="m7-mitte"><div class="m7-halt">%s%s%s<div class="m7-saetze">%s</div>%s</div></div>
<div class="m7-sp m7-r" data-tempo="0.12">%s</div>''' % (li, KZ, TITEL, TEXT, mitte, KNOPF, re_))
V.append(('Gegenlauf', v07))

# 08 · Das Bild zieht sich auf: Momo beim Giessen steht erst klein in der Mitte und wird beim Scrollen gross; danach die übrigen Schritte.
def v08(n):
    rest = ''.join('<div class="m8-sch">%s%s</div>' % (kachel(k, '(max-width:900px) 50vw, 24vw'), satz(t, z)) for k, t, z in [SCHRITTE[0], SCHRITTE[1], SCHRITTE[3], SCHRITTE[4]])
    return sektion(n, '''<div class="m8-kopf">%s%s%s</div>
<div class="m8-buehne"><div class="m8-halt"><div class="m8-bild">%s</div><div class="m8-unter">%s</div></div></div>
<div class="m8-rest staffel">%s</div><div class="m-fuss">%s%s</div>''' % (KZ, TITEL, TEXT, foto('momo-giesst', '(max-width:900px) 100vw, 88vw'), satz(SCHRITTE[2][1], SCHRITTE[2][2]), rest, ZITAT, KNOPF))
V.append(('Das Bild zieht sich auf', v08))

# 09 · Abzüge auf dem Tresen: die Fotos liegen wie Abzüge übereinander, Kante an Kante, leicht verdreht; links der Ablauf.
def v09(n):
    abz = ''.join('<figure class="m9-abzug m9-%d" data-k="%s" style="--lq:url(%s)">%s</figure>' % (j, k, mache(k)['lq'], img(k, '(max-width:900px) 50vw, 24vw')) for j, (k, t, z) in enumerate(SCHRITTE))
    liste = ''.join(satz(t, z, 'm-satz m9-s') for k, t, z in SCHRITTE)
    return sektion(n, '''<div class="m9-links">%s%s%s<div class="m9-liste">%s</div>%s</div>
<div class="m9-tresen flaeche">%s</div>''' % (KZ, TITEL, TEXT, liste, KNOPF, abz))
V.append(('Abzüge auf dem Tresen', v09))

# 10 · Ein Satz mit Bildern: der ganze Ablauf als ein grosser Satz, die Bilder stehen zwischen den Wörtern.
def v10(n):
    worte = ['Erst fragt Momo', 'dann greift er zur Flasche', 'dann mixt er, für dich allein', 'zum Schluss der Schaum', 'und dann ist es deiner']
    teile = []
    for j, ((k, t, z), w) in enumerate(zip(SCHRITTE, worte)):
        vorn, _, letztes = w.rpartition(' ')
        teile.append('%s <span class="m10-nb">%s <span class="m10-bild" style="--lq:url(%s)">%s</span>%s</span>' % (E(vorn), E(letztes), mache(k)['lq'], img(k, '260px'), '.' if j == 4 else ','))
    return sektion(n, '''<div class="m10-kopf">%s%s%s</div>
<p class="titel m10-satz sw" style="--i:2">%s</p>
<div class="m-fuss m10-fuss">%s%s</div>''' % (KZ, TITEL, TEXT, ' '.join(teile), ZITAT, KNOPF))
V.append(('Ein Satz mit Bildern', v10))

# 11 · Auf hellem Papier: der Abschnitt auf Creme, links der Ablauf als Liste mit Goldlinien, rechts sechs Bilder Wand an Wand.
def v11(n):
    liste = ''.join('<div class="m11-z" style="--n:%d">%s</div>' % (j, satz(t, z)) for j, (k, t, z) in enumerate(SCHRITTE))
    wand = ''.join(kachel(k, '(max-width:900px) 33vw, 18vw') for k in ('momo-lacht', 'momo-flaschen', 'momo-giesst', 'schaum', 'glas-hand', 'gereicht'))
    return sektion(n, '''<div class="m11-links">%s%s%s<div class="m11-liste staffel">%s</div>%s</div>
<div class="m11-wand flaeche">%s</div>''' % (KZ, TITEL, TEXT, liste, KNOPF.replace('class="knopf ', 'class="knopf hellk '), wand), 'hell')
V.append(('Auf hellem Papier', v11))

# 12 · Grosses Bild, kleine Bilder: ein grosses Foto, darunter die fünf als kleine Bilder zum Antippen; daneben der Satz zum Bild.
def v12(n):
    stapel = ''.join(foto(k, '(max-width:900px) 100vw, 60vw', 'foto' + (' an' if j == 0 else '')) for j, (k, t, z) in enumerate(SCHRITTE))
    klein = ''.join('<button type="button" class="m12-k%s" data-j="%d" style="--lq:url(%s)" aria-label="%s">%s</button>' % (' an' if j == 0 else '', j, mache(k)['lq'], E(t), img(k, '140px')) for j, (k, t, z) in enumerate(SCHRITTE))
    saetze = ''.join('<div class="m12-s%s" data-j="%d">%s</div>' % (' an' if j == 0 else '', j, satz(t, z)) for j, (k, t, z) in enumerate(SCHRITTE))
    return sektion(n, '''<div class="m12-g">
<div class="m12-gross sw" style="--i:2"><div class="m12-stapel">%s</div><div class="m12-klein">%s</div></div>
<div class="m12-rechts">%s%s%s<div class="m12-saetze">%s</div>%s%s</div></div>''' % (stapel, klein, KZ, TITEL, TEXT, saetze, ZITAT, KNOPF))
V.append(('Grosses Bild, kleine Bilder', v12))

# 13 · Der Weg nach unten: eine Goldlinie in der Mitte zieht sich beim Scrollen mit, die Bilder stehen abwechselnd links und rechts.
def v13(n):
    st = ''.join('<div class="m13-st m13-%s">%s<i class="m13-punkt"></i>%s</div>' % ('l' if j % 2 == 0 else 'r', kachel(k, '(max-width:900px) 60vw, 30vw'), satz(t, z))
                 for j, (k, t, z) in enumerate(SCHRITTE))
    return sektion(n, '''%s<div class="m13-weg"><div class="m13-linie"><i></i></div>%s</div><div class="m-fuss m13-fuss">%s</div>''' % (kopf(), st, KNOPF))
V.append(('Der Weg nach unten', v13))

# 14 · Drei Bilder bis an den Rand: drei grosse Fotos ohne Lücke über die ganze Breite, darunter die Sätze in denselben Dritteln.
def v14(n):
    drei = [SCHRITTE[0], SCHRITTE[2], SCHRITTE[4]]
    bilder3 = ''.join('<div class="m14-b" style="--n:%d">%s</div>' % (j, foto(k, '(max-width:900px) 100vw, 34vw')) for j, (k, t, z) in enumerate(drei))
    saetze = ''.join(satz(t, z) for k, t, z in drei)
    return sektion(n, '''%s</div><div class="m14-band staffel">%s</div><div class="innen"><div class="m14-saetze sw" style="--i:1">%s</div><div class="m-fuss">%s</div>''' % (
        kopf(), bilder3, saetze, KNOPF))
V.append(('Drei Bilder bis an den Rand', v14))

# 15 · Die Liste zum Zeigen: die fünf Sätze als grosse Zeilen; wer über eine Zeile fährt oder sie antippt, sieht rechts ihr Bild.
def v15(n):
    zeilen = ''.join('<button type="button" class="m15-z%s" data-j="%d"><span class="titel">%s</span><span class="m-zu">%s</span></button>' % (' an' if j == 0 else '', j, E(t), E(z)) for j, (k, t, z) in enumerate(SCHRITTE))
    stapel = ''.join(foto(k, '(max-width:900px) 100vw, 40vw', 'foto' + (' an' if j == 0 else '')) for j, (k, t, z) in enumerate(SCHRITTE))
    return sektion(n, '''<div class="m15-links">%s%s%s<div class="m15-liste sw" style="--i:2">%s</div>%s</div>
<div class="m15-rahmen sw" style="--i:1"><div class="m15-stapel">%s</div></div>''' % (KZ, TITEL, TEXT, zeilen, KNOPF, stapel))
V.append(('Die Liste zum Zeigen', v15))


def seite(n, abschnitt):
    alt = B.kap_gespraech
    if abschnitt:
        B.kap_gespraech = abschnitt
    h = B.seite()
    B.kap_gespraech = alt
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>' % (n, E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, None))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, lambda f=f, n=j + 1: f(n)))
    print('00 … %02d' % len(V))
