# Walk on the Wild Side · Programm-Seite, Abschnitt «Die Woche · Drei Abende, drei Tempi.» (id="woche"): 20 Darstellungen (30.10.2026).
# Robert: «Gib jetzt 20 verschiedene Visualisierungsmöglichkeiten für den Abschnitt.» 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte Wort für Wort aus unter.programm(), Zeiten aus HAUS, nur echte Fotos der Bar.
# Bewegung nur über transform und opacity, ein Scroll-Takt in v.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/woche-20/bau.py → 00.html … 20.html
import os, sys, json, html, math
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/woche-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

KZ = B.kz('Die Woche', 'Drei Abende', 0)
TITEL = B.h2(['Drei Abende,', 'drei Tempi.'])
# Wort für Wort wie in unter.programm(); bau.py prüft das unten nach.
TAGE = [
    ('konzert', 'Donnerstag', 'Live, ab und zu', 'Kleine Konzerte mitten im Raum: Jazz, Soul, Pop. Duos und Trios, ohne Eintritt, ab 20 Uhr. 2024 und 2025 spielten Alone Together, Anissa Al Jay, Josseff and Friends und Sina and Friends.'),
    ('momo-lacht', 'Freitag', 'Momo an der Bar', 'Der Abend, an dem die Theke gehört, wem sie gehört: Momo fragt, mixt, erzählt. Bis 2 Uhr.'),
    ('glas-trinkt', 'Samstag', 'Die DJ-Abende', 'Rund einmal im Monat legt jemand auf, von 21 bis 1 Uhr. Auf den Plakaten heisst die Reihe SESSION, gemeint sind Drinks und Musik an einem Abend.'),
]
_q = open('unter.py').read()
for _k, _t, _u, _s in TAGE:
    assert _s in _q and _u in _q, 'Text weicht von der Seite ab: ' + _t
KURZ = ['Do', 'Fr', 'Sa']
OFFEN = {t: z for t, z, _ in B.HAUS['zeiten']}          # Öffnungszeiten aus HAUS
POS = {'konzert': '58% 50%', 'momo-lacht': '50% 42%', 'glas-trinkt': '45% 40%'}


def img(k, sizes, extra=''):
    p = POS.get(k)
    return B.img_tag(k, sizes, extra=(' style="object-position:%s"' % p if p else '') + extra)


def fb(k, sizes, cls='', stil=''):
    """Eigenes Bild ohne .kachel/.foto, damit die Auftritte der Seite die eigene Bewegung nicht überlagern."""
    return '<figure class="wf %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def name(t, cls='w-name'):
    return '<h3 class="titel %s">%s</h3>' % (cls, E(t))


def et(u):
    return '<span class="etikett">%s</span>' % E(u)


def tx(s, cls='text'):
    return '<p class="%s">%s</p>' % (cls, E(s))


def kopf(rechts='', cls=''):
    return '<div class="w-kopf %s"><div>%s%s</div>%s</div>' % (cls, KZ, TITEL, rechts)


def sek(n, inner, cls='', innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf wx v%02d %s" id="woche" data-w="%d">%s</section>' % (n, cls, n, i)


def bildsrc(k, b=960):
    return 'assets/bild/%s?v=%s' % ([f for w, f in mache(k)['stufen'] if w >= b][0], B.V)


V = []


# 01 · Die Abendleiste: über allen drei Abenden läuft dieselbe Uhr von 19 bis 2 Uhr. Die Öffnungszeit liegt als feine Linie,
# darauf wächst beim Scrollen der Teil des Abends, um den es geht: Konzert ab 20, Momo bis 2, DJs von 21 bis 1.
def v01(n):
    stunden = ['19', '20', '21', '22', '23', '24', '1', '2']
    pos = lambda h: (h - 19) / 7 * 100
    spur = {'Donnerstag': (20, 20.18, 'ab 20 Uhr', True), 'Freitag': (19, 26, 'bis 2 Uhr', False), 'Samstag': (21, 25, '21 bis 1 Uhr', False)}
    ende = {'Donnerstag': 25, 'Freitag': 26, 'Samstag': 26}
    achse = '<div class="a-achse"><span></span><div>%s</div></div>' % ''.join('<b style="left:%.2f%%">%s</b>' % (pos(19 + j), s) for j, s in enumerate(stunden))
    reihen = ''
    for j, (k, t, u, s) in enumerate(TAGE):
        a, b, lab, offen_ende = spur[t]
        reihen += '''<div class="a-reihe" data-a>%s<div class="a-rechts"><div class="a-oben">%s%s</div>
<div class="a-spur"><i class="a-offen" style="left:0;width:%.2f%%"></i><i class="a-teil%s" style="left:%.2f%%;width:%.2f%%"></i><em style="left:%.2f%%">%s</em></div>
<small class="a-zeit">Geöffnet %s</small>%s</div></div>''' % (
            fb(k, '(max-width:760px) 92vw, 300px'), name(t), et(u), pos(ende[t]), ' a-auf' if offen_ende else '', pos(a), pos(b) - pos(a),
            pos(a), E(lab), E(OFFEN[t]), tx(s))
    return sek(n, kopf('<div class="a-kopfachse">%s</div>' % achse) + '<div class="a-reihen">%s</div>' % reihen)
V.append(('Die Abendleiste', v01))


# 02 · Die Plakate: jeder Abend ein cremefarbenes Plakat wie die SESSION-Plakate, Foto oben, der Tag gross darunter.
# Sie werden nacheinander angeschlagen: kommen schräg von oben und legen sich leicht schief an die Wand.
def v02(n):
    pl = ''.join('<article class="p-plakat" style="--n:%d">%s<div class="p-unten">%s%s%s</div></article>' % (
        j, fb(k, '(max-width:760px) 88vw, 30vw'), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="p-wand vauf">%s</div>' % pl)
V.append(('Die Plakate', v02))


# 03 · Die Lichtschrift: der Tag steht in Glühbirnen-Gold wie der NEGRONI-Schriftzug über der Vitrine; die Buchstaben gehen einzeln an,
# sobald die Zeile ins Bild kommt. Daneben Bild und Satz.
def v03(n):
    def licht(t):
        return '<p class="l-schrift titel" aria-label="%s">%s</p>' % (E(t), ''.join('<span style="--b:%d">%s</span>' % (j, E(c)) for j, c in enumerate(t)))
    reihen = ''.join('<div class="l-reihe vauf">%s<div class="l-rechts">%s<div>%s%s</div></div></div>' % (
        licht(t), fb(k, '(max-width:760px) 92vw, 30vw'), et(u), tx(s)) for k, t, u, s in TAGE)
    return sek(n, kopf() + '<div class="l-reihen">%s</div>' % reihen)
V.append(('Die Lichtschrift', v03))


# 04 · Der nächste Abend schiebt sich vor: die Bühne bleibt stehen, jeder Abend ist eine grosse Platte über die ganze Breite;
# beim Scrollen schiebt sich der Freitag über den Donnerstag, dann der Samstag über den Freitag.
def v04(n):
    pl = ''.join('<article class="s-platte" style="--n:%d">%s<div class="s-satz"><span class="s-nr titel">%s</span>%s%s%s</div></article>' % (
        j, fb(k, '(max-width:760px) 92vw, 56vw'), KURZ[j], name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, '<div class="innen">%s</div><div class="s-pin" data-pin><div class="s-buehne"><div class="innen s-stapel">%s</div></div></div>' % (kopf(), pl), innen=False)
V.append(('Schiebt sich vor', v04))


# 05 · Das Faltblatt: ein cremefarbenes Programmheft in drei Feldern. Zuerst liegt es gefaltet da, beim Scrollen klappen
# die Seitenflügel auf, und die Woche liegt offen.
def v05(n):
    feld = lambda j, k, t, u, s: '<div class="f-feld f-%d"><div class="f-vorn">%s%s%s%s</div>%s</div>' % (
        j, fb(k, '(max-width:760px) 88vw, 26vw'), name(t), et(u), tx(s),
        '<div class="f-hinten">%s<p class="titel">Drei Abende,<br>drei Tempi.</p></div>' % B.LOGO if j != 1 else '')
    return sek(n, kopf() + '<div class="f-pin" data-pin><div class="f-buehne"><div class="f-heft">%s</div></div></div>' % ''.join(
        feld(j, *x) for j, x in enumerate(TAGE)))
V.append(('Das Faltblatt', v05))


# 06 · Bild in den Buchstaben: Do, Fr, Sa stehen riesig, das Foto des Abends liegt in den Buchstaben. Sie steigen aus dem Schlitz.
def v06(n):
    sp = ''.join('<article class="b-spalte vauf" style="--n:%d"><div class="b-schlitz"><p class="b-gross titel" style="background-image:url(%s)" aria-hidden="true">%s</p></div>%s%s%s%s</article>' % (
        j, bildsrc(k), KURZ[j], fb(k, '(max-width:760px) 92vw, 28vw', 'b-klein'), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="b-reihe">%s</div>' % sp)
V.append(('Bild in den Buchstaben', v06))


# 07 · Die Fenster gehen an: drei hohe Bogenfenster mit Goldrahmen, erst dunkel; beim Scrollen geht hinter jedem das Licht an,
# Donnerstag zuerst. Darunter je ein Schild mit dem Abend.
def v07(n):
    fe = ''.join('<article class="o-fenster" data-o style="--n:%d"><div class="o-bogen">%s<i class="o-nacht"></i></div><div class="o-schild">%s%s%s</div></article>' % (
        j, fb(k, '(max-width:760px) 92vw, 30vw'), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="o-fassade">%s</div>' % fe)
V.append(('Die Fenster gehen an', v07))


# 08 · Das Bild wechselt mit dem Tag: links bleibt ein hohes Bild stehen, rechts zieht die Woche vorbei.
# Kommt der nächste Abend in die Mitte, schiebt sich sein Bild von unten in den Rahmen.
def v08(n):
    bilder = ''.join('<div class="w8-b" style="--n:%d">%s</div>' % (j, fb(k, '(max-width:760px) 92vw, 44vw')) for j, (k, t, u, s) in enumerate(TAGE))
    texte = ''.join('<div class="w8-t" data-t="%d"><span class="w8-nr titel">%s</span>%s%s%s</div>' % (j, '0%d' % (j + 1), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, '<div class="w8-raster"><div class="w8-links"><div class="w8-rahmen">%s</div></div><div class="w8-rechts">%s%s</div></div>' % (bilder, kopf(), texte))
V.append(('Das Bild wechselt', v08))


# 09 · Drei Tempi als Linie: neben jedem Abend zieht sich eine goldene Welle, ruhig am Donnerstag, dichter am Freitag,
# schnell am Samstag. Sie zeichnet sich, sobald der Abend ins Bild kommt.
def v09(n):
    def welle(z):
        w, h, pts = 600, 80, []
        for x in range(0, w + 1, 4):
            pts.append('%d,%.1f' % (x, h / 2 + math.sin(x / w * z * 2 * math.pi) * h * .36))
        return '<svg class="t-welle" viewBox="0 0 600 80" preserveAspectRatio="none" aria-hidden="true"><polyline points="%s" pathLength="100"/></svg>' % ' '.join(pts)
    reihen = ''.join('<div class="t-reihe vauf"><div class="t-satz">%s%s%s</div><div class="t-mitte">%s</div>%s</div>' % (
        name(t), et(u), tx(s), welle(z), fb(k, '(max-width:760px) 92vw, 24vw')) for (k, t, u, s), z in zip(TAGE, (2, 4, 9)))
    return sek(n, kopf() + '<div class="t-reihen">%s</div>' % reihen)
V.append(('Drei Tempi als Linie', v09))


# 10 · Die Treppe: die Woche steigt an. Donnerstag unten, Freitag eine Stufe höher, Samstag oben; jede Stufe mit Goldkante.
# Der Titel steht im Raum über den unteren Stufen. Die Stufen steigen nacheinander auf.
def v10(n):
    st = ''.join('<article class="tr-stufe" style="--n:%d">%s%s%s%s</article>' % (j, fb(k, '(max-width:760px) 92vw, 28vw'), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, '<div class="tr-treppe vauf">%s%s</div>' % (kopf('', 'tr-kopf'), st))
V.append(('Die Treppe', v10))


# 11 · Der Abreisskalender: rechts ein Kalenderblock mit roter Kopfleiste; beim Scrollen klappt das oberste Blatt nach oben weg,
# der Donnerstag gibt den Freitag frei, der Freitag den Samstag. Links bleibt der Titel stehen.
def v11(n):
    bl = ''.join('<div class="k-blatt" style="--n:%d;z-index:%d">%s<div class="k-satz"><span class="k-tag titel">%s</span>%s%s%s</div></div>' % (
        j, 3 - j, fb(k, '(max-width:760px) 92vw, 26vw'), KURZ[j], name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, '<div class="k-pin" data-pin><div class="k-buehne"><div class="innen k-raster">%s<div class="k-block"><div class="k-kopf"><i></i><i></i><span>Die Woche</span><i></i><i></i></div><div class="k-blaetter">%s</div></div></div></div></div>' % (
        kopf(), bl), innen=False)
V.append(('Der Abreisskalender', v11))


# 12 · Die Zeitungsseite: auf Creme gesetzt wie eine Wochenzeitung. Kopfzeile, drei Spalten mit grosser Initiale,
# die Spaltenlinien ziehen sich beim Auftritt von oben nach unten.
def v12(n):
    sp = ''.join('<article class="z-spalte" style="--n:%d">%s%s<p class="z-text"><span class="z-init titel">%s</span>%s</p></article>' % (
        j, fb(k, '(max-width:760px) 92vw, 28vw'), '<div class="z-kopf">%s%s</div>' % (name(t), et(u)), E(s[0]), E(s[1:])) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, '<div class="z-blatt vauf"><div class="z-leiste"><span class="etikett">Die Woche</span><span class="etikett">Walk on the Wild Side · Haasemannstraße 13</span><span class="etikett">Drei Abende</span></div>'
                  '<h2 class="titel z-titel">Drei Abende, drei Tempi.</h2><div class="z-spalten">%s</div></div>' % sp, 'hell')
V.append(('Die Zeitungsseite', v12))


# 13 · Die Liste: drei breite Zeilen zwischen Goldlinien. Der Tag steht riesig links; das Bild rechts wächst,
# während die Zeile zur Mitte kommt, der Name gleitet ihm entgegen.
def v13(n):
    rz = ''.join('<div class="li-zeile" data-li><p class="li-tag titel">%s</p><div class="li-satz">%s%s</div>%s</div>' % (
        E(t), et(u), tx(s), fb(k, '(max-width:760px) 92vw, 26vw')) for k, t, u, s in TAGE)
    return sek(n, kopf() + '<div class="li-liste">%s</div>' % rz)
V.append(('Die Liste', v13))


# 14 · Die Untersetzer: drei runde Bilder wie Bierdeckel mit Goldring, der Tag läuft als Schrift um den Rand.
# Sie rollen beim Auftritt nacheinander von links herein.
def v14(n):
    def deckel(j, k, t):
        return '''<div class="u-deckel">%s<svg viewBox="0 0 300 300" aria-hidden="true"><defs><path id="u-r%d" d="M150,150 m-128,0 a128,128 0 1,1 256,0 a128,128 0 1,1 -256,0"/></defs>
<circle cx="150" cy="150" r="146"/><circle cx="150" cy="150" r="112"/><text><textPath href="#u-r%d" startOffset="0" textLength="796" lengthAdjust="spacing">%s</textPath></text></svg></div>''' % (
            fb(k, '(max-width:760px) 70vw, 22vw'), j, j, E(('%s · WALK ON THE WILD SIDE · ' % t.upper()) * 2))
    sp = ''.join('<article class="u-spalte" style="--n:%d">%s%s%s%s</article>' % (j, deckel(j, k, t), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="u-reihe vauf">%s</div>' % sp)
V.append(('Die Untersetzer', v14))


# 15 · Die Stecktafel: eine schwarze Rillentafel mit weissen Steckbuchstaben, wie vor einem Kino oder einer Bar;
# die Buchstaben fallen einzeln in die Rillen. Daneben die drei Abende mit Bild.
def v15(n):
    zeilen = ['DIE WOCHE', ''] + ['%s  %s' % (KURZ[j].upper(), u.upper()) for j, (k, t, u, s) in enumerate(TAGE)]
    c = [0]

    def zeile(z):
        out = ''
        for ch in z:
            out += '<span style="--b:%d">%s</span>' % (c[0], '&nbsp;' if ch == ' ' else E(ch))
            c[0] += 1
        return '<p>%s</p>' % (out or '&nbsp;')
    tafel = '<div class="st-tafel vauf" aria-hidden="true"><div class="st-rillen">%s</div></div>' % ''.join(zeile(z) for z in zeilen)
    abende = ''.join('<div class="st-abend sw" style="--i:%d">%s<div>%s%s%s</div></div>' % (j + 1, fb(k, '(max-width:760px) 30vw, 14vw'), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="st-raster">%s<div class="st-abende">%s</div></div>' % (tafel, abende))
V.append(('Die Stecktafel', v15))


# 16 · Die Rollläden: drei hohe Bilder, vor jedem ein geschlossener Rollladen. Beim Scrollen fährt er hoch, die Bar macht auf;
# Donnerstag zuerst, dann Freitag, dann Samstag.
def v16(n):
    sp = ''.join('<article class="r-spalte" data-r style="--n:%d"><div class="r-kasten"></div><div class="r-oeffnung">%s<i class="r-laden"></i></div>%s%s%s</article>' % (
        j, fb(k, '(max-width:760px) 92vw, 30vw'), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="r-reihe">%s</div>' % sp)
V.append(('Die Rollläden', v16))


# 17 · Das Flügelbild: wie ein Altarbild in drei Tafeln, eine Erinnerung an das Gewölbe der Bar. Der Freitag in der Mitte unter dem Bogen,
# Donnerstag und Samstag als Flügel, die sich beim Scrollen öffnen.
def v17(n):
    tf = ''.join('<article class="fl-tafel fl-%d">%s<div class="fl-satz">%s%s%s</div></article>' % (
        j, fb(k, '(max-width:760px) 92vw, %s' % ('34vw' if j == 1 else '26vw')), name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="fl-bild" data-fl>%s</div>' % tf)
V.append(('Das Flügelbild', v17))


# 18 · In der Tiefe: drei hohe Platten, die verschieden schnell durchs Bild ziehen; in jeder Platte wandert das Foto
# gegen die Bewegung, als läge es weiter hinten.
def v18(n):
    sp = ''.join('<article class="d-platte" data-d="%s">%s<div class="d-satz">%s%s%s</div></article>' % (
        sp_, fb(k, '(max-width:760px) 92vw, 30vw'), name(t), et(u), tx(s)) for (k, t, u, s), sp_ in zip(TAGE, ('.6', '0', '-.6')))
    return sek(n, kopf() + '<div class="d-reihe">%s</div>' % sp)
V.append(('In der Tiefe', v18))


# 19 · Drei Szenen: jeder Abend bekommt ein Bild über die ganze Breite, das beim Scrollen langsam zur Ruhe kommt;
# darunter ein dunkles Band mit dem Tag in Hero-Grösse und dem Satz.
def v19(n):
    sz = ''.join('<article class="sz-szene" data-sz><div class="sz-bild">%s</div><div class="innen sz-band"><p class="sz-tag titel">%s</p><div>%s%s</div></div></article>' % (
        fb(k, '100vw'), E(t), et(u), tx(s)) for k, t, u, s in TAGE)
    return sek(n, '<div class="innen">%s</div>%s' % (kopf(), sz), innen=False)
V.append(('Drei Szenen', v19))


# 20 · Der Rahmen wandert: drei Bilder nebeneinander, ein Goldrahmen steht still im Bild und wandert beim Scrollen
# von Abend zu Abend; der Abend im Rahmen ist hell, die anderen treten zurück.
def v20(n):
    bilder = ''.join('<div class="g-feld" style="--n:%d">%s</div>' % (j, fb(k, '(max-width:760px) 92vw, 30vw')) for j, (k, t, u, s) in enumerate(TAGE))
    texte = ''.join('<div class="g-satz" style="--n:%d">%s%s%s</div>' % (j, name(t), et(u), tx(s)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, '<div class="innen">%s</div><div class="g-pin" data-pin><div class="g-buehne"><div class="innen"><div class="g-bilder">%s<i class="g-rahmen"></i></div><div class="g-saetze">%s</div></div></div></div>' % (
        kopf(), bilder, texte), innen=False)
V.append(('Der Rahmen wandert', v20))


def seite(n):
    h = unter.programm()
    if n:
        a = h.rfind('<section', 0, h.find('id="woche"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
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
