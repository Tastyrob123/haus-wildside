# Walk on the Wild Side · Haus-Seite (haus.html), Abschnitte «Der Raum» und «Wer hinter der Bar steht»: 15 Fassungen (31.10.2026).
# Robert: «diese beiden abschnitte deutlich anders, besser zum rest der seite (landingpage, Drinks, Programm, feiern) entwerfen - gib mir 15 alternative visuelle alternativen».
# 00 = heutiger Stand. Je Fassung beide Abschnitte, jeder mit eigener Darstellung und eigener Bewegung. Texte Wort für Wort aus unter.py, Bilder dieselben.
# Nur transform und opacity, ein Scroll-Takt in v.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/haus-15/bau.py → 00 … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/haus-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

RAUM = [('decke-bar', 'Die Decke: ein Gewölbe als Druck über dem ganzen Raum, blau und silbern angeleuchtet.'),
        ('negroni', 'NEGRONI in Glühbirnen über der Vitrine. Der Schriftzug sagt, was hier jeden Abend gerührt wird.'),
        ('theke', 'Die Theke mit dem gelben Licht unter der Kante. Hier wird gefragt, was du magst.'),
        ('rueckbar-breit', 'Die Rückbar: Flaschen, die man nicht in jedem Laden findet, und eine beleuchtete Vitrine.'),
        ('fenster', 'Von der Strasse aus sieht man die Rückbar durchs Fenster, oben spiegelt sich die Decke.'),
        ('tuer-rot', 'Durch die Tür: der rote Boden, links die Theke, hinten die Stufen hinauf zur Empore.')]
DERYA = dict(k='derya', name='Derya Ivkin', rolle='führt die Bar',
             text='Seit Herbst 2023 gehört die Bar ihr und Momo. Sie entscheidet, wer auflegt, wer kocht und wann die Empore gedeckt wird.',
             weg=[('2023', 'Übernimmt die Bar im Herbst, Wiedereröffnung am 9. November.'), ('2024', 'Die Neue Presse besucht sie an der Theke, Continental Sour im Glas.'), ('heute', 'Führt die Bar und die Abende von Culinarium mit.')])
MOMO = dict(k='momo-giesst', name='Momo Ben Khelifa', rolle='mixt die Drinks',
            text='Er fragt, was du magst, und baut daraus einen Drink. Vorher Biotechnologie an der Uni, dann Bars in Berlin und Hannover.',
            weg=[('1988', 'Geboren in Tunis, seit 2008 in Hannover.'), ('2014', 'Nach dem Master in Biotechnologie in die Bars von Berlin.'), ('2018', 'Barchef im Lindenblatt, Mitgründer der ProBierBar in Linden.'), ('2023', 'Mit Derya im Wild Side, ohne Karte.')])
LEUTE = [DERYA, MOMO]
_q = open('unter.py').read()
for t in [s for _, s in RAUM] + [p[f] for p in LEUTE for f in ('name', 'rolle', 'text')] + [s for p in LEUTE for _, s in p['weg']]:
    assert t in _q, 'Text weicht von der Seite ab: ' + t

POS = {'derya': '50% 30%', 'momo-giesst': '50% 30%'}


def foto(k, sizes='33vw', cls='', stil=''):
    p = POS.get(k)
    return '<figure class="hv-f %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, B.img_tag(k, sizes, extra=' style="object-position:%s"' % p if p else ''))


def kopf_raum(cls=''):
    return '<div class="hv-kopf %s">%s%s</div>' % (cls, B.kz('Der Raum', 'Fünf Blicke', 0), B.h2(['Klein, dunkel,', 'warm.']))


def kopf_leute(cls=''):
    return '<div class="hv-kopf %s">%s%s</div>' % (cls, B.kz('Wer hinter der Bar steht', 'Zwei Leute', 0), B.h2(['Derya und Momo.']))


def sek(id_, cls, inner, voll=''):
    return '<section class="kap auf hv %s" id="%s"><div class="innen">%s</div>%s</section>' % (cls, id_, inner, voll)


def weg(p, cls='hv-weg'):
    return '<div class="%s">%s</div>' % (cls, ''.join('<div style="--n:%d"><span>%s</span><p>%s</p></div>' % (j, E(a), E(b)) for j, (a, b) in enumerate(p['weg'])))


def person_text(p, cls='', mit_weg=True):
    return '<div class="hv-pt %s"><h3 class="titel hv-name">%s</h3><span class="etikett">%s</span><p class="text">%s</p>%s</div>' % (
        cls, E(p['name']), E(p['rolle']), E(p['text']), weg(p) if mit_weg else '')


def caps(cls='hv-caps', klein=False):
    return '<div class="%s">%s</div>' % (cls, ''.join('<p class="%s" data-t="%d">%s</p>' % ('text' if klein else 'titel', j, E(s)) for j, (_, s) in enumerate(RAUM)))


V = []

# ---------------------------------------------------------------- 01 Wand an Wand
# Raum: sechs Bilder Kante an Kante als eine Wand, jedes steigt aus seiner eigenen Tiefe; darunter ein cremefarbenes Band mit dem Satz zum Bild, Zeigen tauscht ihn.
# Leute: beide Porträts Kante an Kante, darunter ein cremefarbenes Band in zwei Spalten; die Bilder setzen sich, das Band kommt nach.
def v01():
    lage = ['a', 'b', 'c', 'd', 'e', 'f']
    wand = ''.join('<div class="w1-z w1-%s" data-t="%d" style="--n:%d;--t:%d">%s</div>' % (lage[j], j, j, (70, 150, 100, 60, 130, 90)[j], foto(k, '(max-width:760px) 50vw, 33vw')) for j, (k, s) in enumerate(RAUM))
    band = '<div class="w1-band hell">%s</div>' % ''.join('<p class="titel w1-satz" data-z="%d">%s</p>' % (j, E(s)) for j, (_, s) in enumerate(RAUM))
    r = sek('raum', 'v01', kopf_raum() + '<div class="auf w1" data-tausch>%s%s</div>' % ('<div class="w1-wand">%s</div>' % wand, band))
    l = sek('leute', 'v01', kopf_leute() + '<div class="auf w1l"><div class="w1l-bilder">%s</div><div class="w1l-band hell">%s</div></div>' % (
        ''.join(foto(p['k'], '(max-width:760px) 100vw, 50vw') for p in LEUTE), ''.join(person_text(p) for p in LEUTE)))
    return r + l
V.append(('Wand an Wand', v01))

# ---------------------------------------------------------------- 02 Kontaktbogen
# Raum: ein grosses Bild links, alle sechs klein rechts, Zeigen tauscht das grosse und den Satz (wie die Plakate auf der Programm-Seite).
# Leute: je Person das Bild gross, eine Platte mit dem Text schiebt sich über die Bildkante und läuft beim Scrollen etwas schneller.
def v02():
    gross = ''.join('<div class="k2-g" data-z="%d">%s</div>' % (j, foto(k, '(max-width:760px) 100vw, 60vw')) for j, (k, _) in enumerate(RAUM))
    klein = ''.join('<button class="k2-k" data-t="%d" aria-label="Bild %d" style="--n:%d">%s</button>' % (j, j + 1, j, foto(k, '15vw')) for j, (k, _) in enumerate(RAUM))
    saetze = ''.join('<p class="titel k2-s" data-z="%d">%s</p>' % (j, E(s)) for j, (_, s) in enumerate(RAUM))
    r = sek('raum', 'v02', kopf_raum() + '<div class="auf k2" data-tausch><div class="k2-gross">%s</div><div class="k2-rechts"><div class="k2-reihe">%s</div><div class="k2-saetze platte">%s</div></div></div>' % (gross, klein, saetze))
    zeilen = ''.join('<div class="auf k2l %s" data-p><div class="k2l-b">%s</div><div class="platte k2l-p">%s</div></div>' % ('k2l-r' if j else '', foto(p['k'], '(max-width:760px) 100vw, 60vw'), person_text(p)) for j, p in enumerate(LEUTE))
    return r + sek('leute', 'v02', kopf_leute() + zeilen)
V.append(('Kontaktbogen', v02))

# ---------------------------------------------------------------- 03 Schachbrett
# Raum: Bild und Satz im Wechsel wie das Schachbrett «Seit 2018» auf der Startseite; die Felder drehen sich nacheinander in den Blick.
# Leute: vier Felder, Bild und Text über Kreuz; die Felder klappen von unten auf.
def v03():
    zellen = []
    for j, (k, s) in enumerate(RAUM):
        b = '<div class="s3-z s3-b">%s</div>' % foto(k, '(max-width:760px) 50vw, 25vw')
        t = '<div class="s3-z s3-t %s"><p class="titel">%s</p></div>' % ('hell' if j % 2 == 0 else '', E(s))
        zellen += [t, b] if j in (2, 3) else [b, t]
    z = ''.join(c.replace('class="s3-z', 'style="--n:%d" class="s3-z' % (j % 4 + j // 4), 1) for j, c in enumerate(zellen))
    r = sek('raum', 'v03', kopf_raum() + '<div class="auf s3">%s</div>' % z)
    d, m = LEUTE
    l = '<div class="auf s3l"><div class="s3l-z" style="--n:0">%s</div><div class="s3l-z hell" style="--n:1">%s</div><div class="s3l-z s3l-d" style="--n:2">%s</div><div class="s3l-z" style="--n:3">%s</div></div>' % (
        foto(d['k'], '(max-width:760px) 100vw, 50vw'), person_text(d), person_text(m), foto(m['k'], '(max-width:760px) 100vw, 50vw'))
    return r + sek('leute', 'v03', kopf_leute() + l)
V.append(('Schachbrett', v03))

# ---------------------------------------------------------------- 04 Ein Faden durch den Raum
# Beide Abschnitte als ein Weg: eine Goldlinie in der Mitte, von der Strasse durch die Tür bis unter die Decke, und weiter zu den beiden hinter der Bar.
# Je Halt eine eigene Bewegung: steigen, sich setzen, aus der Tiefe.
def v04():
    folge = [4, 5, 2, 3, 1, 0]
    bew = ['f4-steigt', 'f4-setzt', 'f4-tiefe']
    h = ''.join('<div class="auf f4-halt %s %s"><div class="f4-bild">%s</div><i class="f4-punkt"></i><p class="titel f4-s">%s</p></div>' % (
        'f4-r' if n % 2 else '', bew[n % 3], foto(RAUM[j][0], '(max-width:760px) 100vw, 44vw'), E(RAUM[j][1])) for n, j in enumerate(folge))
    r = sek('raum', 'v04', kopf_raum('f4-kopf') + '<div class="f4" data-p><i class="f4-linie"></i>%s</div>' % h)
    l = ''.join('<div class="auf f4-halt f4-p %s %s"><div class="f4-bild">%s</div><i class="f4-punkt"></i>%s</div>' % ('f4-r' if j else '', bew[j], foto(p['k'], '(max-width:760px) 100vw, 44vw'), person_text(p)) for j, p in enumerate(LEUTE))
    return r + sek('leute', 'v04', kopf_leute('f4-kopf') + '<div class="f4" data-p><i class="f4-linie"></i>%s</div>' % l)
V.append(('Ein Faden durch den Raum', v04))

# ---------------------------------------------------------------- 05 Das Eckschild
# Raum: eine grosse Platte mit doppelter Goldlinie wie das Schild an der Ecke; links die Sätze mit Haarlinien, rechts die Bilder; Zeigen auf einen Satz hebt sein Bild.
# Leute: zwei Schilder mit Goldrahmen, die Bilder darin, darunter die Jahre in Spalten; die Schilder steigen nacheinander.
def v05():
    saetze = ''.join('<p class="text e5-s" data-t="%d" style="--n:%d">%s</p>' % (j, j, E(s)) for j, (_, s) in enumerate(RAUM))
    bilder = ''.join('<div class="e5-b" data-z="%d" style="--n:%d">%s</div>' % (j, j, foto(k, '(max-width:760px) 50vw, 20vw')) for j, (k, _) in enumerate(RAUM))
    r = sek('raum', 'v05', kopf_raum() + '<div class="auf platte e5" data-tausch data-frei><i class="e5-rahmen"></i><div class="e5-saetze">%s</div><div class="e5-bilder">%s</div></div>' % (saetze, bilder))
    l = ''.join('<div class="platte e5l" style="--n:%d"><i class="e5-rahmen"></i>%s<h3 class="titel hv-name">%s</h3><span class="etikett">%s</span><p class="text">%s</p>%s</div>' % (
        j, foto(p['k'], '(max-width:760px) 100vw, 45vw'), E(p['name']), E(p['rolle']), E(p['text']), weg(p, 'hv-weg e5-jahre')) for j, p in enumerate(LEUTE))
    return r + sek('leute', 'v05', kopf_leute() + '<div class="auf e5l-reihe">%s</div>' % l)
V.append(('Das Eckschild', v05))

# ---------------------------------------------------------------- 06 Spalten finden zusammen
# Raum: drei Spalten mit je zwei Bildern, die Spalten kommen beim Scrollen mit verschiedenem Tempo und stehen am Ende auf einer Linie.
# Leute: gespiegelt, Bild aussen, Text innen; die Bilder fahren beim Scrollen aus der Nähe zurück, bis die Person ganz dasteht.
def v06():
    sp = [[0, 2], [1, 3], [4, 5]]
    cols = ''.join('<div class="z6-sp" style="--v:%d">%s</div>' % ((160, 40, 240)[c], ''.join('<figure class="z6-b">%s<figcaption class="text">%s</figcaption></figure>' % (
        foto(RAUM[j][0], '(max-width:760px) 100vw, 33vw'), E(RAUM[j][1])) for j in js)) for c, js in enumerate(sp))
    r = sek('raum', 'v06', kopf_raum() + '<div class="auf z6" data-p>%s</div>' % cols)
    d, m = LEUTE
    l = '<div class="auf z6l" data-p><div class="z6l-b">%s</div>%s%s<div class="z6l-b">%s</div></div>' % (
        foto(d['k'], '(max-width:760px) 100vw, 34vw'), person_text(d, 'platte'), person_text(m, 'platte'), foto(m['k'], '(max-width:760px) 100vw, 34vw'))
    return r + sek('leute', 'v06', kopf_leute() + l)
V.append(('Spalten finden zusammen', v06))

# ---------------------------------------------------------------- 07 Das Plakat
# Raum: in der Mitte ein cremefarbenes Plakat mit allen Sätzen (wie die weissen Plakate der Bar), links und rechts die Bilder Kante an Kante.
# Leute: eine dunkle Platte mit Goldrahmen wie «Eure Nachbarschafts-Mixology-Bar» auf der Startseite, die Jahre als Spalten.
def v07():
    li = ''.join(foto(RAUM[j][0], '(max-width:760px) 50vw, 25vw', 'p7-b', '--n:%d' % n) for n, j in enumerate((0, 2)))
    re = ''.join(foto(RAUM[j][0], '(max-width:760px) 50vw, 25vw', 'p7-b', '--n:%d' % n) for n, j in enumerate((1, 4)))
    unten = ''.join(foto(RAUM[j][0], '(max-width:760px) 50vw, 50vw', 'p7-b', '--n:%d' % (n + 2)) for n, j in enumerate((3, 5)))
    plakat = '<div class="p7-plakat hell">%s<div class="p7-liste">%s</div></div>' % (B.LOGO.replace('<svg', '<svg class="p7-logo"', 1), ''.join('<p>%s</p>' % E(s) for _, s in RAUM))
    r = sek('raum', 'v07', kopf_raum() + '<div class="auf p7"><div class="p7-sp">%s</div>%s<div class="p7-sp">%s</div><div class="p7-unten">%s</div></div>' % (li, plakat, re, unten))
    l = '<div class="auf platte p7l">%s</div>' % ''.join('<div class="p7l-p">%s<h3 class="titel hv-name">%s</h3><span class="etikett">%s</span><p class="text">%s</p>%s</div>' % (
        foto(p['k'], '(max-width:760px) 100vw, 45vw'), E(p['name']), E(p['rolle']), E(p['text']), weg(p, 'hv-weg p7-jahre')) for p in LEUTE)
    return r + sek('leute', 'v07', kopf_leute() + l)
V.append(('Das Plakat', v07))

# ---------------------------------------------------------------- 08 Auf dem Tresen
# Raum: auf einer hellen Fläche liegen die Bilder leicht gedreht wie Abzüge auf dem Tresen, sie landen nacheinander; der Satz steht darunter.
# Leute: zwei grosse Bilder liegen erst flach und stellen sich auf, der Text steht daneben auf derselben hellen Fläche.
def v08():
    dreh = (-4, 3, -2, 4, -3, 2)
    karten = ''.join('<figure class="t8-k" style="--r:%ddeg;--n:%d">%s<figcaption class="text">%s</figcaption></figure>' % (dreh[j], j, foto(k, '(max-width:760px) 50vw, 30vw'), E(s)) for j, (k, s) in enumerate(RAUM))
    r = sek('raum', 'v08 hell', kopf_raum() + '<div class="auf t8">%s</div>' % karten)
    l = ''.join('<div class="auf t8l %s"><div class="t8l-raum"><div class="t8l-b" style="--r:%ddeg">%s</div></div>%s</div>' % ('t8l-r' if j else '', (-2, 2)[j], foto(p['k'], '(max-width:760px) 100vw, 50vw'), person_text(p)) for j, p in enumerate(LEUTE))
    return r + sek('leute', 'v08 hell', kopf_leute() + l)
V.append(('Auf dem Tresen', v08))

# ---------------------------------------------------------------- 09 Das Band
# Raum: die sechs Bilder als ein Band über die ganze Breite, es wandert beim Scrollen langsam nach links, der Satz läuft unter jedem Bild mit.
# Leute: über die ganze Breite zwei Bilder Kante an Kante, die Hälften steigen aus verschiedener Tiefe, Text darunter in denselben Spalten.
def v09():
    band = ''.join('<figure class="b9-f">%s<figcaption class="text">%s</figcaption></figure>' % (foto(k, '(max-width:760px) 70vw, 30vw'), E(s)) for k, s in RAUM)
    r = sek('raum', 'v09', kopf_raum(), '<div class="auf b9" data-p><div class="b9-zug">%s</div></div>' % band)
    d, m = LEUTE
    l = sek('leute', 'v09', kopf_leute(), '<div class="auf b9l"><div class="b9l-h" style="--n:0">%s</div><div class="b9l-h" style="--n:1">%s</div><div class="b9l-t">%s</div><div class="b9l-t">%s</div></div>' % (
        foto(d['k'], '(max-width:760px) 100vw, 60vw'), foto(m['k'], '(max-width:760px) 100vw, 40vw'), person_text(d), person_text(m)))
    return r + l
V.append(('Das Band', v09))

# ---------------------------------------------------------------- 10 Unter der Decke
# Beide Abschnitte liegen auf der Decke der Bar als Tapete; sie ist erst dunkel, das Licht geht an, wenn der Abschnitt kommt.
# Raum: sechs hohe Karten, Bild oben, Satz unten; Leute: zwei breite Platten, Bild links, Text rechts.
def v10():
    tap = '<div class="d10-tapete" aria-hidden="true">%s</div>' % foto('decke-flach', '100vw')
    karten = ''.join('<figure class="platte d10-k" style="--n:%d">%s<figcaption class="text">%s</figcaption></figure>' % (j, foto(k, '(max-width:760px) 50vw, 33vw'), E(s)) for j, (k, s) in enumerate(RAUM))
    r = '<div class="d10-wrap auf">%s%s%s</div>' % (tap, sek('raum', 'v10', kopf_raum() + '<div class="auf d10">%s</div>' % karten),
        sek('leute', 'v10', kopf_leute() + ''.join('<div class="auf platte d10l" style="--n:%d">%s%s</div>' % (j, foto(p['k'], '(max-width:760px) 100vw, 45vw'), person_text(p)) for j, p in enumerate(LEUTE))))
    return r
V.append(('Unter der Decke', v10))

# ---------------------------------------------------------------- 11 Der Blick wandert
# Raum: links steht ein grosses Bild, rechts laufen die Sätze vorbei; mit jedem Satz wechselt das Bild an derselben Stelle.
# Leute: zwei Bilder nebeneinander, darunter die Jahre; beim Scrollen leuchtet ein Goldpunkt nach dem anderen auf.
def v11():
    bilder = ''.join('<div class="w11-b" data-z="%d">%s</div>' % (j, foto(k, '(max-width:760px) 100vw, 50vw')) for j, (k, _) in enumerate(RAUM))
    saetze = ''.join('<div class="w11-s" data-schritt="%d"><p class="titel">%s</p></div>' % (j, E(s)) for j, (_, s) in enumerate(RAUM))
    r = sek('raum', 'v11', kopf_raum() + '<div class="w11" data-tausch data-wandern><div class="w11-halt"><div class="w11-rahmen">%s</div></div><div class="w11-saetze">%s</div></div>' % (bilder, saetze))
    l = '<div class="w11l">%s</div>' % ''.join('<div class="auf w11l-p">%s%s</div>' % (foto(p['k'], '(max-width:760px) 100vw, 50vw'), person_text(p, 'w11l-t')) for p in LEUTE)
    return r + sek('leute', 'v11', kopf_leute() + l)
V.append(('Der Blick wandert', v11))

# ---------------------------------------------------------------- 12 Die Fensterreihe
# Raum: sechs hohe Fenster nebeneinander, dunkler Rahmen mit Goldlinie; abwechselnd von oben und von unten, der Satz darunter.
# Leute: zwei breite Fenster, das Bild steigt im Rahmen nach oben, bis es sitzt.
def v12():
    f = ''.join('<figure class="f12" style="--n:%d;--y:%d"><div class="f12-r">%s</div><figcaption class="text">%s</figcaption></figure>' % (j, -1 if j % 2 else 1, foto(k, '(max-width:760px) 50vw, 17vw'), E(s)) for j, (k, s) in enumerate(RAUM))
    r = sek('raum', 'v12', kopf_raum() + '<div class="auf f12-reihe">%s</div>' % f)
    l = '<div class="auf f12l">%s</div>' % ''.join('<div class="f12l-p" style="--n:%d"><div class="f12-r f12l-r">%s</div>%s</div>' % (j, foto(p['k'], '(max-width:760px) 100vw, 50vw'), person_text(p)) for j, p in enumerate(LEUTE))
    return r + sek('leute', 'v12', kopf_leute() + l)
V.append(('Die Fensterreihe', v12))

# ---------------------------------------------------------------- 13 Eine Chronik für zwei
# Raum: die Decke gross und hoch links, rechts die anderen fünf Bilder dicht, jedes mit seinem Satz in einer schmalen Leiste darunter.
# Leute: beide Bilder oben, darunter eine gemeinsame Goldlinie mit allen Jahren der beiden, Derya links, Momo rechts; die Linie zieht sich auf.
def v13():
    def zelle(j, cls, sizes):
        k, s = RAUM[j]
        return '<figure class="c13-z %s" style="--n:%d">%s<figcaption class="text">%s</figcaption></figure>' % (cls, j, foto(k, sizes), E(s))
    r = sek('raum', 'v13', kopf_raum() + '<div class="auf c13">%s%s%s%s%s%s</div>' % (
        zelle(0, 'c13-gross', '(max-width:760px) 100vw, 40vw'), zelle(3, 'c13-breit', '(max-width:760px) 100vw, 58vw'), zelle(1, '', '29vw'), zelle(2, '', '29vw'), zelle(4, '', '29vw'), zelle(5, '', '29vw')))
    d, m = LEUTE
    jahre = {}
    for wer, p in (('d', d), ('m', m)):
        for a, b in p['weg']:
            jahre.setdefault(a, {})[wer] = b
    ordnung = sorted(jahre, key=lambda a: 9999 if a == 'heute' else int(a))
    zeilen = ''.join('<div class="c13-j" style="--n:%d"><p class="text c13-d">%s</p><span class="titel">%s</span><p class="text c13-m">%s</p></div>' % (
        n, E(jahre[a].get('d', '')), E(a), E(jahre[a].get('m', ''))) for n, a in enumerate(ordnung))
    kopf = ''.join('<div class="c13l-p">%s%s</div>' % (foto(p['k'], '(max-width:760px) 100vw, 50vw'), person_text(p, '', False)) for p in LEUTE)
    l = '<div class="auf c13l"><div class="c13l-kopf">%s</div><div class="c13-chronik" data-p><i class="c13-linie"></i>%s</div></div>' % (kopf, zeilen)
    return r + sek('leute', 'v13', kopf_leute() + l)
V.append(('Eine Chronik für zwei', v13))

# ---------------------------------------------------------------- 14 Die Hängung
# Raum: die Bilder dicht gehängt wie an einer Wand, jedes in einem dunklen Rahmen mit Goldlinie; sie schwingen leicht und kommen zur Ruhe. Zeigen bringt den Satz in die Zeile darunter.
# Leute: zwei gerahmte Porträts, unter jedem ein helles Schildchen mit Name und Weg, das hinter dem Rahmen hervorkommt.
def v14():
    lage = ['a', 'b', 'c', 'd', 'e', 'f']
    w = ''.join('<div class="h14-r h14-%s" data-t="%d" style="--n:%d;--s:%ddeg">%s</div>' % (lage[j], j, j, (2, -2, 1.5, -1.5, 2, -2)[j], foto(k, '(max-width:760px) 50vw, 33vw')) for j, (k, _) in enumerate(RAUM))
    zeile = '<div class="h14-zeile">%s</div>' % ''.join('<p class="titel" data-z="%d">%s</p>' % (j, E(s)) for j, (_, s) in enumerate(RAUM))
    r = sek('raum', 'v14', kopf_raum() + '<div class="auf h14" data-tausch><div class="h14-wand">%s</div>%s</div>' % (w, zeile))
    l = '<div class="auf h14l">%s</div>' % ''.join('<div class="h14l-p" style="--n:%d"><div class="h14-r h14l-r">%s</div><div class="h14l-schild hell">%s</div></div>' % (j, foto(p['k'], '(max-width:760px) 100vw, 50vw'), person_text(p)) for j, p in enumerate(LEUTE))
    return r + sek('leute', 'v14', kopf_leute() + l)
V.append(('Die Hängung', v14))

# ---------------------------------------------------------------- 15 Das helle Kapitel
# Beide Abschnitte auf Creme, wie die hellen Kapitel der anderen Seiten. Raum: drei grosse Bilder, darunter drei, jeder Satz unter seinem Bild; die Bilder setzen sich.
# Leute: die Namen gross, die Bilder Kante an Kante, die Jahre mit braunen Haarlinien; die Namen kommen aus dem Schlitz.
def v15():
    g = ''.join('<figure class="h15-k" style="--n:%d">%s<figcaption class="text">%s</figcaption></figure>' % (j, foto(k, '(max-width:760px) 50vw, 33vw'), E(s)) for j, (k, s) in enumerate(RAUM))
    r = sek('raum', 'v15 hell', kopf_raum() + '<div class="auf h15">%s</div>' % g)
    l = '<div class="auf h15l"><div class="h15l-bilder">%s</div>%s</div>' % (''.join(foto(p['k'], '(max-width:760px) 100vw, 50vw') for p in LEUTE),
        ''.join('<div class="h15l-p"><h3 class="titel h15l-name">%s</h3><span class="etikett">%s</span><p class="text">%s</p>%s</div>' % (
            B.zl([p['name']]), E(p['rolle']), E(p['text']), weg(p)) for p in LEUTE))
    return r + sek('leute', 'v15 hell', kopf_leute() + l)
V.append(('Das helle Kapitel', v15))

assert len(V) == 15


def seite(n):
    h = unter.haus()
    if n:
        a = h.find('<section class="kap auf" id="raum">')
        b = h.find('</section>', h.find('id="leute"', a)) + len('</section>')
        assert a > 0 and b > a + 100
        h = h[:a] + V[n - 1][1]() + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>' % (n, E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(16):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 … 15')
