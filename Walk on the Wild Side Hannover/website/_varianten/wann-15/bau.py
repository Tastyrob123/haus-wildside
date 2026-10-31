# Walk on the Wild Side · Besuch-Seite, Abschnitt «Wann» (id="wann"), 15 Fassungen (31.10.2026).
# Robert: «gib mir 15 alternative visualsierungen für den abschnitt» (Bildschirmfoto: Wann · Drei Abende, Zeiten, Glas mit Kerzen).
# Inhalt bleibt belegt (Zeiten aus HAUS, Satz zum Reservieren wie heute); je Fassung eigener Aufbau und eigene Bewegung,
# Auftritte deckend über transform, nie seitwärts. Wechsel mit ← → (varianten-nav.js). Aufruf: python3 _varianten/wann-15/bau.py
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, HAUS, mache, img_tag, LOGO

ORD = '_varianten/wann-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('wann.css', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('besuch.html').read()
assert len(basis) > 10000, 'besuch.html leer (anderer Bau läuft?)'
a = basis.index('<section class="kap auf" id="wann">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]

SATZ = 'Die Bar ist klein. Wer zu mehreren kommt, reserviert besser, per Nachricht auf Instagram oder telefonisch an einem offenen Abend.'
Z = HAUS['zeiten']   # [(Tag, Zeit, data-tag)]
OFFEN = Z[:3]
ZU = Z[3]
KURZ = {'Donnerstag': 'Do', 'Freitag': 'Fr', 'Samstag': 'Sa'}


def k(key, cls='', sizes='40vw', pos=None, stil=''):
    extra = ' style="object-position:%s"' % pos if pos else ''
    return '<figure class="kachel %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(key)['lq'], stil, img_tag(key, sizes, extra=extra))


def kz(cls=''):
    return '<div class="kz %s"><span class="uhr">Wann</span><i></i><span class="was">Drei Abende</span></div>' % cls


def heute(cls='t-mittel'):
    return '<h2 class="titel %s" data-heute-satz>Donnerstag bis Samstag ab 19 Uhr</h2>' % cls


def zeiten(cls=''):
    return '<div class="zeiten %s">%s</div>' % (cls, ''.join(
        '<div data-tag="%s"><span>%s<span class="jetzt"></span></span><b>%s</b></div>' % (t, E(n), E(z)) for n, z, t in Z))


def satz(cls=''):
    return '<p class="text w-satz %s">%s</p>' % (cls, E(SATZ))


def sek(n, inner, cls=''):
    return '<section class="kap auf wann wn%02d %s" id="wann" data-v="%d">%s</section>' % (n, cls, n, inner)


def jetzt():
    return '<span class="jetzt"></span>'


V = []

# 01 Die Theke als Leiste: Titel mittig, darunter das breite Bild der Rückbar; die drei Abende stehen wie auf der Thekenkante,
#    unter ihnen zieht sich eine goldene Lichtlinie auf (wie das gelbe Licht unter der Kante)
def f01(n):
    abende = ''.join('<div class="w01-a w-hoch" data-tag="%s" style="--n:%d"><span class="etikett">%s%s</span><b>%s</b></div>' % (t, j + 2, E(d), jetzt(), E(z))
                     for j, (d, z, t) in enumerate(OFFEN))
    return sek(n, '<div class="innen">%s%s<div class="w-hoch" style="--n:1">%s</div><div class="w01-kante">%s<i class="w01-licht"></i></div>'
               '<div class="w01-unten w-hoch" style="--n:5"><p data-tag="%s"><span>%s%s</span> · %s</p>%s</div></div>' % (
                   kz(), heute('w01-t'), k('rueckbar-breit', 'w01-bild', '(max-width:800px) 92vw, 900px'), abende,
                   ZU[2], E(ZU[0]), jetzt(), E(ZU[1]), satz()))
V.append(('Die Theke als Leiste', f01))

# 02 Die Nacht in Stunden: die Zeiten als Leiste von 19 bis 2 Uhr, die Balken wachsen von 19 Uhr aus; rechts das Glas
def f02(n):
    std = ['19', '20', '21', '22', '23', '0', '1', '2']
    kopf = '<div class="w02-z w02-kopf"><span></span><div class="w02-std">%s</div></div>' % ''.join('<i>%s</i>' % s for s in std)
    reihen = ''
    for j, (d, z, t) in enumerate(Z):
        lang = {'19 bis 1 Uhr': 6, '19 bis 2 Uhr': 7}.get(z, 0)
        bal = '<b class="w02-b" style="--l:%d;--n:%d"><span>%s</span></b>' % (lang, j, E(z)) if lang else '<em>%s</em>' % E(z)
        reihen += '<div class="w02-z" data-tag="%s"><span>%s%s</span><div class="w02-std">%s</div></div>' % (t, E(d), jetzt(), bal)
    return sek(n, '<div class="innen w02-g"><div>%s%s<div class="platte w02-leiste w-hoch" style="--n:1">%s%s</div>%s</div>%s</div>' % (
        kz(), heute(), kopf, reihen, satz(), k('glas-kerze', 'w02-bild w-hoch', '(max-width:800px) 92vw, 30vw')))
V.append(('Die Nacht in Stunden', f02))

# 03 Das Schild: links das leuchtende Eckschild, rechts hängt eine cremefarbene Tafel mit den Zeiten an zwei Schnüren
#    und pendelt sich beim Auftritt ein
def f03(n):
    tafel = '<div class="w03-tafel"><i class="w03-h"></i><i class="w03-h r"></i><span class="etikett">Geöffnet</span>%s%s</div>' % (heute('t-mittel'), zeiten())
    return sek(n, '<div class="innen w03-g">%s<div>%s%s%s</div></div>' % (k('schild', 'w03-bild w-hoch', '(max-width:800px) 92vw, 42vw', '50% 30%'), kz(), tafel, satz()))
V.append(('Das Schild', f03))

# 04 Drei Abende, drei Bilder: drei hohe Karten nebeneinander, Bild oben, Tag und Uhrzeit darunter; die Karte von heute bekommt den Goldrand
def f04(n):
    bil = ['theke', 'voll', 'momo-giesst']
    karten = ''.join('<div class="w04-k w-hoch" data-tag="%s" style="--n:%d">%s<div class="w04-u"><span class="etikett">%s%s</span><b>%s</b></div></div>' % (
        t, j + 1, k(bil[j], '', '(max-width:800px) 92vw, 30vw'), E(d), jetzt(), E(z)) for j, (d, z, t) in enumerate(OFFEN))
    return sek(n, '<div class="innen"><div class="w04-kopf">%s%s</div><div class="w04-reihe">%s</div><div class="w04-unten w-hoch" style="--n:4">'
               '<p data-tag="%s"><span>%s%s</span><b>%s</b></p>%s</div></div>' % (kz(), heute('t-mittel'), karten, ZU[2], E(ZU[0]), jetzt(), E(ZU[1]), satz()))
V.append(('Drei Abende, drei Bilder', f04))

# 05 Nur Schrift: der Satz von heute sehr gross über die ganze Breite, darunter die vier Zeiten in einer Reihe; kein Foto
def f05(n):
    reihe = ''.join('<div class="w05-z" data-tag="%s"><span class="etikett">%s%s</span><b>%s</b></div>' % (t, E(d), jetzt(), E(z)) for d, z, t in Z)
    return sek(n, '<div class="innen">%s<div class="w05-schlitz"><h2 class="titel w05-t" data-heute-satz>Donnerstag bis Samstag ab 19 Uhr</h2></div>'
               '<div class="w05-reihe w-hoch" style="--n:2">%s</div>%s</div>' % (kz(), reihe, satz('w-hoch')))
V.append(('Nur Schrift', f05))

# 06 Das Zifferblatt: eine Uhr, auf der die offenen Stunden in Gold liegen, aussen Freitag und Samstag bis 2, innen Donnerstag bis 1;
#    die Bögen ziehen sich beim Auftritt auf, rechts die Zeiten
def f06(n):
    def bogen(r, std):  # Bogen ab 19 Uhr (= 7 auf dem Blatt) über std Stunden, im Uhrzeigersinn
        u = 2 * 3.14159265 * r
        return '<circle class="w06-bg" cx="150" cy="150" r="%d" style="--u:%.1f;--l:%.1f" transform="rotate(120 150 150)"/>' % (r, u, u * std / 12)
    striche = ''.join('<line x1="150" y1="16" x2="150" y2="%d" transform="rotate(%d 150 150)"/>' % (27 if h % 3 == 0 else 22, h * 30) for h in range(12))
    zahlen = ''.join('<text x="%.1f" y="%.1f">%s</text>' % (150 + 82 * __import__('math').sin(h * 0.5235988), 155 - 82 * __import__('math').cos(h * 0.5235988), s)
                     for h, s in [(7, '19'), (10, '22'), (0, '24'), (1, '1'), (2, '2'), (4, '4')])
    uhr = ('<svg class="w06-uhr" viewBox="0 0 300 300" aria-hidden="true"><circle class="w06-rand" cx="150" cy="150" r="138"/><g class="w06-str">%s</g>'
           '<circle class="w06-spur" cx="150" cy="150" r="114"/><circle class="w06-spur" cx="150" cy="150" r="100"/>%s%s<g class="w06-z">%s</g>'
           '<text class="w06-l" x="150" y="146">Fr · Sa bis 2</text><text class="w06-l" x="150" y="166">Do bis 1</text></svg>') % (striche, bogen(114, 7), bogen(100, 6), zahlen)
    return sek(n, '<div class="innen w06-g"><div class="w06-links w-hoch" style="--n:1">%s</div><div>%s%s%s%s</div></div>' % (uhr, kz(), heute(), zeiten(), satz()))
V.append(('Das Zifferblatt', f06))

# 07 Die Tür: links öffnet sich das Bild durch die Tür auf den roten Boden wie eine Tür, die aufgeht (dreht sich in die Fläche);
#    rechts die Zeiten in zwei Spalten
def f07(n):
    tage = ''.join('<div class="w07-z w-hoch" data-tag="%s" style="--n:%d"><span class="etikett">%s%s</span><b>%s</b></div>' % (t, j + 2, E(d), jetzt(), E(z)) for j, (d, z, t) in enumerate(Z))
    return sek(n, '<div class="innen w07-g"><div class="w07-rahmen">%s</div><div>%s%s<div class="w07-raster">%s</div>%s</div></div>' % (
        k('tuer-rot', 'w07-bild', '(max-width:800px) 92vw, 40vw'), kz(), heute('t-gross'), tage, satz()))
V.append(('Die Tür', f07))

# 08 Drei Kalenderblätter: Donnerstag, Freitag, Samstag als Abreissblätter mit roter Kopfleiste und grosser 19;
#    sie fallen nacheinander gefächert an ihren Platz, das Blatt von heute liegt vorn
def f08(n):
    bl = ''.join('<div class="w08-b" data-tag="%s" style="--n:%d"><span class="w08-kopf">%s</span><b>19</b><span class="w08-bis">%s</span><span class="jetzt"></span></div>' % (
        t, j, E(d), E(z.replace('19 ', '', 1))) for j, (d, z, t) in enumerate(OFFEN))
    return sek(n, '<div class="innen w08-g"><div>%s%s<p class="w08-zu" data-tag="%s">%s%s · <b>%s</b></p>%s</div><div class="w08-stapel">%s</div></div>' % (
        kz(), heute('t-gross'), ZU[2], E(ZU[0]), jetzt(), E(ZU[1]), satz(), bl))
V.append(('Drei Kalenderblätter', f08))

# 09 Ein Satz: die Zeiten als ein grosser Satz in der Titelschrift, der heutige Abend in Gold; daneben klein das Glas in der Hand
def f09(n):
    t = dict((d, tg) for d, z, tg in Z)
    s = ('<span class="w09-tg" data-tag="%s">Donnerstag</span> von 19 bis 1 Uhr, <span class="w09-tg" data-tag="%s">Freitag</span> und '
         '<span class="w09-tg" data-tag="%s">Samstag</span> von 19 bis 2 Uhr. <span class="w09-zu" data-tag="%s">Sonntag bis Mittwoch ist zu.</span>') % (
        t['Donnerstag'], t['Freitag'], t['Samstag'], ZU[2])
    return sek(n, '<div class="innen w09-g"><div>%s<p class="titel w09-s w-hoch" style="--n:1">%s</p><div class="w09-unten w-hoch" style="--n:2">'
               '<span class="etikett" data-heute-satz>Donnerstag bis Samstag ab 19 Uhr</span>%s</div></div>%s</div>' % (
                   kz(), s, satz(), k('glas-hand', 'w09-bild w-hoch', '(max-width:800px) 60vw, 24vw')))
V.append(('Ein Satz', f09))

# 10 Hell und dunkel: der Abschnitt teilt sich randlos, links cremefarben mit dunkler Schrift wie die Plakate der Bar,
#    rechts das Bild der Theke bis an den Rand; das Bild setzt sich beim Auftritt von leicht vergrössert auf seine Grösse
def f10(n):
    return sek(n, '<div class="w10-g"><div class="w10-hell"><div class="w10-in w-hoch" style="--n:0">%s%s%s%s</div></div>%s</div>' % (
        kz(), heute('t-gross'), zeiten(), satz(), k('theke', 'w10-bild', '(max-width:800px) 100vw, 50vw')), 'w10-sek')
V.append(('Hell und dunkel', f10))

# 11 Sieben Glühbirnen: die Woche als Reihe Glühbirnen wie über der Vitrine, Donnerstag bis Samstag gehen nacheinander an,
#    unter jeder der Tag, unter den drei hellen die Uhrzeit
def f11(n):
    tage = [('Mo', '1', ''), ('Di', '2', ''), ('Mi', '3', ''), ('Do', '4', '19 bis 1'), ('Fr', '5', '19 bis 2'), ('Sa', '6', '19 bis 2'), ('So', '0', '')]
    birnen = ''.join('<div class="w11-t%s" data-tag="%s" style="--n:%d"><i class="w11-draht"></i><i class="w11-birne"><i class="w11-glanz"></i></i><span class="w11-tag">%s</span><b>%s</b></div>' % (
        ' an' if z else '', t, j, d, E(z + ' Uhr') if z else 'zu') for j, (d, t, z) in enumerate(tage))
    return sek(n, '<div class="innen"><div class="w11-kopf">%s%s</div><div class="w11-leine"><i class="w11-kabel"></i>%s</div>%s</div>' % (
        kz(), heute('t-gross'), birnen, satz('w11-satz')))
V.append(('Sieben Glühbirnen', f11))

# 12 Drei Bierdeckel: Donnerstag, Freitag, Samstag als runde Deckel in Creme, die nacheinander auf den Tisch fallen
#    und sich leicht gedreht einpendeln; links Titel und Satz
def f12(n):
    dk = ''.join('<div class="w12-d" data-tag="%s" style="--n:%d;--r:%ddeg"><span class="etikett">%s</span><b>%s</b><span class="w12-l">%s</span><span class="jetzt"></span></div>' % (
        t, j, r, E(d), E(z.replace(' Uhr', '')), 'Uhr') for j, ((d, z, t), r) in enumerate(zip(OFFEN, (-7, 4, -3))))
    return sek(n, '<div class="innen w12-g"><div>%s%s<p class="w12-zu" data-tag="%s">%s%s · <b>%s</b></p>%s</div><div class="w12-tisch">%s</div></div>' % (
        kz(), heute('t-gross'), ZU[2], E(ZU[0]), jetzt(), E(ZU[1]), satz(), dk))
V.append(('Drei Bierdeckel', f12))

# 13 Wie eine Karte: die Zeiten auf einer cremefarbenen Karte mit gepunkteten Linien wie eine Getränkekarte,
#    die Punkte laufen beim Auftritt zur Uhrzeit hin; daneben das Negroni-Glas
def f13(n):
    zeilen = ''.join('<div class="w13-z" data-tag="%s" style="--n:%d"><span>%s%s</span><i></i><b>%s</b></div>' % (t, j, E(d), jetzt(), E(z)) for j, (d, z, t) in enumerate(Z))
    karte = '<div class="w13-karte w-hoch" style="--n:1"><span class="logo w13-logo">%s</span><span class="etikett">Öffnungszeiten</span>%s<p class="w13-fuss" data-heute-satz>Donnerstag bis Samstag ab 19 Uhr</p></div>' % (LOGO, zeilen)
    return sek(n, '<div class="innen w13-g"><div>%s%s%s</div>%s</div>' % (kz(), karte, satz(), k('glas-negroni', 'w13-bild w-hoch', '(max-width:800px) 92vw, 32vw')))
V.append(('Wie eine Karte', f13))

# 14 Do, Fr, Sa: die drei Tage als sehr grosse Buchstaben untereinander, jede Zeile steigt einzeln auf, die Uhrzeit rechts daneben;
#    rechts das Fenster von der Strasse
def f14(n):
    zl = ''.join('<div class="w14-z" data-tag="%s"><span class="w14-sch"><b style="--n:%d">%s</b></span><span class="w14-r"><span class="etikett">%s%s</span><em>%s</em></span></div>' % (
        t, j, KURZ[d], E(d), jetzt(), E(z)) for j, (d, z, t) in enumerate(OFFEN))
    return sek(n, '<div class="innen w14-g"><div>%s%s<p class="w14-zu" data-tag="%s">%s%s · %s</p>%s</div>%s</div>' % (
        kz(), zl, ZU[2], E(ZU[0]), jetzt(), E(ZU[1]), satz(), k('fenster', 'w14-bild w-hoch', '(max-width:800px) 92vw, 36vw')))
V.append(('Do, Fr, Sa', f14))

# 15 Das Leuchtschild: die Zeiten stehen in einem schwarzen Kasten mit goldenem Rahmen wie das Schild an der Ecke;
#    beim Auftritt geht das Licht im Rahmen an; daneben die Ecke am Abend
def f15(n):
    sch = '<div class="w15-schild w-hoch" style="--n:1"><i class="w15-licht"></i><span class="w15-wild">Wild Side</span>%s%s</div>' % (heute('w15-t'), zeiten('w15-zt'))
    return sek(n, '<div class="innen w15-g"><div>%s%s%s</div>%s</div>' % (kz(), sch, satz(), k('schild-ecke', 'w15-bild w-hoch', '(max-width:800px) 92vw, 36vw')))
V.append(('Das Leuchtschild', f15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/wann.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    schluss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
               '<script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', schluss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
