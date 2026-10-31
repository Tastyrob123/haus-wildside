# Walk on the Wild Side · Feiern-Seite, Abschnitt «Musik · Der Klang dazu.» (id="musik"): 15 Darstellungen (30.10.2026).
# Robert: «gib mir 15 visuelle alternative darstellungen von dem abschnitt». 00 = heutiger Stand (Plattenhüllen).
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte Wort für Wort aus unter.tafel(), nur die drei echten Fotos.
# an-dj ist nur 590 px breit: nie breiter als ~470 px zeigen. Bewegung nur über transform und opacity, ein Scroll-Takt in m.js.
# Aufruf: python3 _varianten/musik-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/musik-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('m.css', 'm.js', 'nav.js'))))

TEXT = 'Ihr sucht noch einen DJ, Live-Musik, Gesang oder Jazz? Die Bar ergänzt euren Abend mit der passenden Begleitung und greift dabei auf ein grosses Repertoire zurück, auch auf die Musikerinnen und Musiker, die sonst donnerstags und samstags hier spielen.'
MUSIK = [('an-dj', '50% 50%', 'DJ', 'Von entspannten Sounds bis zu tanzbaren Beats.'),
         ('saengerin', '50% 35%', 'Gesang', 'Eine Stimme mitten im Raum.'),
         ('konzert-love', '50% 40%', 'Jazz', 'Ein Duo oder Trio für den ruhigeren Abend.')]
_q = open('unter.py').read()
assert TEXT in _q, 'Text weicht ab'
for _k, _p, _t, _s in MUSIK:
    assert "('%s', '%s', '%s', '%s')" % (_k, _p, _t, _s) in _q, 'Eintrag weicht ab: ' + _t


def kopf(cls=''):
    return '<div class="fr-mkopf2 m-kopf %s"><div>%s%s</div><p class="text sw" style="--i:1">%s</p></div>' % (
        cls, B.kz('Musik', 'Für euren Abend', 0), B.h2(['Der Klang', 'dazu.']), E(TEXT))


def kopf_hoch(cls=''):
    return '<div class="m-kopfh %s">%s%s<p class="text sw" style="--i:1">%s</p></div>' % (
        cls, B.kz('Musik', 'Für euren Abend', 0), B.h2(['Der Klang', 'dazu.']), E(TEXT))


def fo(k, pos, sizes, cls='', stil=''):
    return '<figure class="mf %s" style="--lq:url(%s);%s">%s</figure>' % (
        cls, mache(k)['lq'], stil, B.img_tag(k, sizes, extra=' style="object-position:%s"' % pos))


def satz(t, s, cls='m-satz'):
    return '<div class="%s"><span class="etikett">%s</span><h3 class="titel">%s</h3></div>' % (cls, E(t), E(s))


def sek(n, inner, innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf mq m%02d" id="musik" data-m="%d">%s</section>' % (n, n, i)


S3 = '(max-width:760px) 80vw, 26vw'
V = []


# 01 · Aus der Hülle: jedes Foto ist eine quadratische Plattenhülle, dahinter steckt die Platte.
# Beim Auftritt schiebt sich die schwarze Platte mit goldenem Etikett oben aus der Hülle, eine nach der anderen.
def v01(n):
    p = ''.join('<article class="a1-p" style="--n:%d"><div class="a1-ding"><div class="a1-platte"><i></i><i></i><i></i><b></b></div>%s</div>%s</article>' % (
        j, fo(k, pos, S3, 'a1-huelle'), satz(t, s)) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, kopf() + '<div class="a1-reihe vauf">%s</div>' % p)
V.append(('Aus der Hülle', v01))


# 02 · Das Mischpult: ein dunkles Pult mit drei Kanälen. Je Kanal oben das Bild, darunter ein Regler in seiner Schiene.
# Beim Auftritt fahren die drei Regler nacheinander hoch, jeder auf seine eigene Höhe.
def v02(n):
    k_ = ''.join('<article class="p2-k" style="--n:%d;--h:%d"><div class="p2-bild">%s</div><div class="p2-unten"><div class="p2-schiene"><i class="p2-skala"></i><b class="p2-knopf"></b></div>%s</div></article>' % (
        j, h, fo(k, pos, S3), satz(t, s)) for j, ((k, pos, t, s), h) in enumerate(zip(MUSIK, (83, 54, 105))))
    return sek(n, kopf() + '<div class="p2-pult vauf">%s</div>' % k_)
V.append(('Das Mischpult', v02))


# 03 · Die Plakatwand: drei Konzertplakate in Creme an der Wand, je Plakat das Foto, das Wort in Plakatrot und der Satz.
# Die Plakate werden von oben nach unten angeschlagen, eins nach dem anderen.
def v03(n):
    p = ''.join('<article class="w3-p" style="--n:%d;--w:%sdeg"><div class="w3-papier">%s<p class="w3-wort titel">%s</p><p class="w3-satz">%s</p></div></article>' % (
        j, w, fo(k, pos, S3), E(t), E(s)) for j, ((k, pos, t, s), w) in enumerate(zip(MUSIK, (-1.4, .8, -.6))))
    return sek(n, kopf() + '<div class="w3-wand vauf">%s</div>' % p)
V.append(('Die Plakatwand', v03))


# 04 · Der Spot: drei Bilder stehen im Dunkeln. Beim Scrollen geht über einem nach dem anderen das Licht an,
# und erst dann steigt sein Satz darunter auf.
def v04(n):
    p = ''.join('<article class="s4-p">%s<i class="s4-dunkel"></i>%s</article>' % (fo(k, pos, S3), satz(t, s)) for k, pos, t, s in MUSIK)
    return sek(n, kopf() + '<div class="s4-reihe" data-spot>%s</div>' % p)
V.append(('Der Spot', v04))


# 05 · Die Setlist: links der Kopf, rechts ein cremefarbenes Blatt, wie es auf der Bühne am Boden klebt.
# Je Zeile Bild, Wort und Satz; die Trennlinien ziehen sich, dann rückt jede Zeile ein.
def v05(n):
    z = ''.join('<div class="l5-z" style="--n:%d">%s<div><span class="etikett">%s</span><h3 class="titel">%s</h3></div></div>' % (
        j, fo(k, pos, '(max-width:760px) 30vw, 12vw'), E(t), E(s)) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, '<div class="l5-raster">%s<div class="l5-blatt vauf"><i class="l5-band"></i>%s</div></div>' % (kopf_hoch(), z))
V.append(('Die Setlist', v05))


# 06 · Die Stimme in der Mitte: Gesang gross in der Mitte, DJ und Jazz schmal daneben, alle drei gleich hoch.
# Die beiden äusseren liegen zuerst hinter der Mitte und gleiten dann zur Seite heraus.
def v06(n):
    (k0, p0, t0, s0), (k1, p1, t1, s1), (k2, p2, t2, s2) = MUSIK
    return sek(n, kopf() + '<div class="m6-reihe vauf"><article class="m6-p m6-l">%s%s</article><article class="m6-p m6-m">%s%s</article><article class="m6-p m6-r">%s%s</article></div>' % (
        fo(k0, p0, '(max-width:760px) 80vw, 22vw'), satz(t0, s0), fo(k1, p1, '(max-width:760px) 80vw, 36vw'), satz(t1, s1), fo(k2, p2, '(max-width:760px) 80vw, 22vw'), satz(t2, s2)))
V.append(('Die Stimme in der Mitte', v06))


# 07 · Die grossen Worte: je Art eine Zeile, das Wort riesig quer über die Breite, daneben Bild und Satz, im Wechsel links und rechts.
# Beim Scrollen wandert jedes Wort langsam seitwärts durch seine Zeile.
def v07(n):
    z = ''.join('<article class="g7-z %s">%s<div class="g7-t"><p class="g7-wort titel" data-wort aria-hidden="true" style="--g:%s">%s</p>%s</div></article>' % (
        'rechts' if j % 2 else '', fo(k, pos, '(max-width:760px) 70vw, 24vw'), {'DJ': 1.6, 'Gesang': 1, 'Jazz': 1.35}[t], E(t), satz(t, s)) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, kopf() + '<div class="g7-zeilen">%s</div>' % z)
V.append(('Die grossen Worte', v07))


# 08 · Die Schallwelle: eine goldene Welle läuft durch den ganzen Abschnitt, die drei Bilder sitzen auf verschiedenen Höhen darauf.
# Erst zeichnet sich die Welle von links nach rechts, dann steigen die drei nacheinander auf.
def v08(n):
    p = ''.join('<article class="s8-p" style="--n:%d">%s%s</article>' % (j, fo(k, pos, '(max-width:760px) 80vw, 24vw'), satz(t, s)) for j, (k, pos, t, s) in enumerate(MUSIK))
    welle = '<svg class="s8-welle" viewBox="0 0 1200 200" preserveAspectRatio="none" aria-hidden="true"><path d="M0 100 C 100 20, 200 20, 300 100 S 500 180, 600 100 S 800 20, 900 100 S 1100 180, 1200 100"/></svg>'
    return sek(n, kopf() + '<div class="s8-feld vauf"><div class="s8-spur">%s<i class="s8-deck"></i></div>%s</div>' % (welle, p))
V.append(('Die Schallwelle', v08))


# 09 · Das Notenblatt: fünf goldene Notenlinien quer über die Breite, die drei Bilder sitzen rund wie Noten auf verschiedenen Linien.
# Erst ziehen sich die Linien, dann fallen die Noten auf ihren Platz und federn nach.
def v09(n):
    linien = ''.join('<i style="--n:%d"></i>' % j for j in range(5))
    p = ''.join('<article class="n9-p" style="--n:%d">%s%s</article>' % (j, fo(k, pos, '(max-width:760px) 60vw, 20vw', 'n9-note'), satz(t, s)) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, kopf() + '<div class="n9-blatt vauf"><div class="n9-linien">%s</div><div class="n9-reihe">%s</div></div>' % (linien, p))
V.append(('Das Notenblatt', v09))


# 10 · Die Klapphülle: je Art eine geschlossene schwarze Hülle mit dem Wort in Gold. Beim Auftritt klappt sie nach links auf wie ein Doppelalbum,
# innen links das Foto, rechts auf Creme der Satz. Die drei Hüllen stehen versetzt untereinander.
def v10(n):
    h = ''.join('<article class="k10-h vauf %s"><div class="k10-innen"><div class="k10-rechts"><span class="etikett">%s</span><h3 class="titel">%s</h3></div>'
                '<div class="k10-deckel"><div class="k10-vorn"><b class="titel">%s</b></div><div class="k10-rueck">%s</div></div></div></article>' % (
        'rechts' if j % 2 else '', E(t), E(s), E(t), fo(k, pos, '(max-width:760px) 46vw, 22vw')) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, kopf() + '<div class="k10-stapel">%s</div>' % h)
V.append(('Die Klapphülle', v10))


# 11 · Die Bühnenfahrt: der Abschnitt bleibt stehen, beim Scrollen fährt die Bühne seitwärts von einer Besetzung zur nächsten,
# erst der Kopf, dann DJ, Gesang und Jazz, jede mit grossem Bild.
def v11(n):
    p = ''.join('<article class="b11-p">%s%s</article>' % (fo(k, pos, '(max-width:760px) 60vw, 26vw'), satz(t, s)) for k, pos, t, s in MUSIK)
    return sek(n, '<div class="b11-pin" data-pin><div class="b11-buehne"><div class="b11-spur"><div class="b11-kopf">%s</div>%s</div></div></div>' % (kopf_hoch(), p), innen=False)
V.append(('Die Bühnenfahrt', v11))


# 12 · Vom Stapel in die Reihe: die drei Bilder liegen zuerst als Stapel in der Mitte, leicht verdreht.
# Beim Scrollen fächern sie sich auseinander, bis sie gerade nebeneinander stehen; dann kommen die Sätze.
def v12(n):
    p = ''.join('<article class="f12-p" style="--n:%d;--r:%sdeg;--d:%s">%s<div class="f12-maske">%s</div></article>' % (
        j, r, d, fo(k, pos, S3), satz(t, s)) for j, ((k, pos, t, s), r, d) in enumerate(zip(MUSIK, (-5, 3, 6), (1, 0, -1))))
    return sek(n, kopf() + '<div class="f12-reihe" data-stapel>%s</div>' % p)
V.append(('Vom Stapel in die Reihe', v12))


# 13 · Die Glühbirnen-Schrift: über jedem Bild steht das Wort in Gold wie die Leuchtbuchstaben an der Bühnenwand.
# Beim Auftritt geht ein Buchstabe nach dem anderen an, erst dann steigt das Bild auf.
def v13(n):
    def wort(t):
        return '<p class="g13-wort titel" aria-label="%s">%s</p>' % (E(t), ''.join('<span style="--b:%d" aria-hidden="true">%s</span>' % (i, E(c)) for i, c in enumerate(t.upper())))
    p = ''.join('<article class="g13-p" style="--n:%d">%s%s<h3 class="titel g13-satz">%s</h3></article>' % (j, wort(t), fo(k, pos, S3), E(s)) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, kopf() + '<div class="g13-reihe vauf">%s</div>' % p)
V.append(('Die Glühbirnen-Schrift', v13))


# 14 · Die Eintrittskarten: drei hohe Karten in Creme, oben das Foto, eine gestrichelte Abrisskante, unten Wort und Satz.
# Die Karten steigen nacheinander auf, dann reisst bei jeder der untere Teil ein Stück ab.
def v14(n):
    p = ''.join('<article class="t14-p" style="--n:%d"><div class="t14-karte"><div class="t14-oben">%s</div><div class="t14-abriss">%s</div></div></article>' % (
        j, fo(k, pos, S3), satz(t, s, 'm-satz t14-satz')) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, kopf() + '<div class="t14-reihe vauf">%s</div>' % p)
V.append(('Die Eintrittskarten', v14))


# 15 · Das Pegelband: drei Bilder dicht nebeneinander, darunter läuft über die ganze Breite ein Band aus schmalen goldenen Balken.
# Beim Auftritt schlägt der Pegel von links nach rechts aus, Balken für Balken; darunter stehen die Sätze.
def v15(n):
    hoehen = [30, 63, 72, 90, 87, 85, 72, 56, 45, 39, 50, 38, 42, 38, 54, 49, 50, 37, 54, 71, 82, 95, 88, 88, 61, 52, 43, 71, 77, 86, 81, 71, 60, 43, 41, 35, 43, 36, 55, 53, 62, 54, 45, 48, 64, 84, 89, 100, 84, 81, 52, 42, 55, 74, 77, 76, 70, 55, 50, 34, 42, 32, 51, 52, 67, 65, 65, 53, 38, 61, 73, 95]
    balken = ''.join('<i style="--n:%d;--h:%d"></i>' % (j, h) for j, h in enumerate(hoehen))
    b = ''.join('<div class="e15-b">%s</div>' % fo(k, pos, S3) for k, pos, t, s in MUSIK)
    st = ''.join('<div class="e15-s" style="--n:%d">%s</div>' % (j, satz(t, s)) for j, (k, pos, t, s) in enumerate(MUSIK))
    return sek(n, kopf() + '<div class="e15-ganz vauf"><div class="e15-bilder">%s</div><div class="e15-pegel">%s</div><div class="e15-saetze">%s</div></div>' % (b, balken, st))
V.append(('Das Pegelband', v15))


def seite(n):
    h = unter.tafel()
    if n:
        a = h.rfind('<section', 0, h.find('id="musik"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[i + 1, nm] for i, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/m.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(V[n - 1][0] if n else 'Heutiger Stand'))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/m.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
