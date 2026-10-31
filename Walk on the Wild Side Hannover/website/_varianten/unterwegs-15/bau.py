# Walk on the Wild Side · Programm-Seite, Abschnitt «Unterwegs · Und manchmal draussen.» (id="unterwegs"): 15 Fassungen (30.10.2026).
# Robert: «jetzt gib mir 15 visualisierungsmöglichekiten für den abschnitt». 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung. Texte Wort für Wort aus unter.programm(), Termine aus der Liste dort.
# Bilder nur echte: Christi Limmerfahrt 2025 (twopointsview), Ankündigung 2026 und Oktoberfest-Plakat (event.klub), Plakat 2025 (trustory),
# der Stand des Wild Side (fw-a45, fw-a46), die Hausecke (schild-ecke), die Loge (an-loge). Fotos nie einem Termin zugeordnet, zu dem sie nicht gehören.
# Bewegung nur über transform, alles von Anfang an deckend. Aufruf: python3 _varianten/unterwegs-15/bau.py → 00.html … 15.html
import os, sys, json, html, re
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/unterwegs-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('u.css', 'nav.js', 'nav.css'))))
BASIS = unter.programm()
_a = BASIS.rfind('<section', 0, BASIS.find('id="unterwegs"'))
_b = BASIS.find('</section>', _a) + len('</section>')
HEUTE = BASIS[_a:_b]
TEXT = re.search(r'<p class="text sw" style="--i:1">(.*?)</p>', HEUTE, re.S).group(1)     # mit dem Link «Mehr unter Feiern», unverändert
_q = open('unter.py').read()
AUSSEN = [('31.10. und 01.11.2026', 'Oktoberfest des Event Klub am Stephansplatz, 12 bis 21 Uhr, die Drinks kommen vom Wild Side', True),
          ('09.08.2026', 'Smash n Mingle beim HTV, mit Musa und Tru Story', False), ('13. und 14.06.2026', 'Südstadtfest, Cocktailstand mit dem Mon Bonheur', False),
          ('14. und 15.05.2026', 'Christi Limmerfahrt am Küchengarten', False), ('31.07.2025', 'Maschseefest, Stand Aresto x Lindenblatt', False)]
for _d, _s, _x in AUSSEN:
    assert "('%s', '%s', %s)" % (_d, _s, _x) in _q, 'Termin weicht ab: ' + _s
# Kurzname je Termin, nur aus dem Wortlaut darüber
ORT = ['Oktoberfest', 'Smash n Mingle', 'Südstadtfest', 'Christi Limmerfahrt', 'Maschseefest']
WO = ['Stephansplatz', 'HTV', 'Südstadt', 'Küchengarten', 'Maschsee']
REST = ['des Event Klub am Stephansplatz, 12 bis 21 Uhr, die Drinks kommen vom Wild Side', 'beim HTV, mit Musa und Tru Story', 'Cocktailstand mit dem Mon Bonheur', 'am Küchengarten', 'Stand Aresto x Lindenblatt']
def kurz(d):
    if ' und ' in d:
        a, b = d.split(' und ')
        return a + '/' + b[:6]
    return d[:6]


BALD = '<span class="etikett u-bald">bald</span>'


def kz():
    return B.kz('Unterwegs', 'Die Bar ausser Haus', 0)


def titel(cls='t-kap'):
    return B.h2(['Und manchmal', 'draussen.'], cls)


def text(i=1):
    return '<p class="text sw" style="--i:%d">%s</p>' % (i, TEXT)


def kopf(cls=''):
    return '<div class="u-kopf %s">%s%s%s</div>' % (cls, kz(), titel(), text())


def zeilen(i=2):
    """Die Terminliste wie heute (Datum, Satz, «bald»)."""
    return '<div class="zeilen sw" style="--i:%d">%s</div>' % (i, ''.join(
        '<div><span class="etikett">%s</span><span>%s%s</span></div>' % (E(d), E(s), ' ' + BALD if b else '') for d, s, b in AUSSEN))


def fo(k, sizes, cls='', stil='', pos=''):
    return '<figure class="uf %s" style="--lq:url(%s);%s">%s</figure>' % (
        cls, mache(k)['lq'], stil, B.img_tag(k, sizes, extra=' style="object-position:%s"' % pos if pos else ''))


def sek(n, inner, innen=True, cls=''):
    return '<section class="kap auf uw u%02d %s" id="unterwegs">%s</section>' % (n, cls, '<div class="innen">%s</div>' % inner if innen else inner)


V = []


def v(nr, name):
    def deko(f):
        V.append((nr, name, f)); return f
    return deko


@v(1, 'Die Fahnenkette')
def _():
    farben = ['rot', 'creme', 'gold', 'blau']
    fahnen = ''.join('<i class="u01-f u01-%s" style="--n:%d;--y:%.1fpx"></i>' % (farben[j % 4], j, 34 * (1 - ((j - 9.5) / 9.5) ** 2)) for j in range(20))
    return sek(1, '<div class="u01-kette" aria-hidden="true"><svg viewBox="0 0 1000 60" preserveAspectRatio="none"><path d="M0,4 Q500,76 1000,4"/></svg>%s</div>'
               '<div class="innen u01-raster"><div>%s%s%s%s</div><div class="u01-bilder">%s%s</div></div>' % (
                   fahnen, kz(), titel(), text(), zeilen(), fo('uw-fahnen25', '(max-width:900px) 92vw, 30vw', 'u01-a', pos='50% 40%'), fo('uw-tanz', '(max-width:900px) 46vw, 16vw', 'u01-b')), False)


@v(2, 'Das Tourplakat')
def _():
    reihen = ''.join('<div class="u02-r" style="--n:%d"><b class="titel">%s</b><i></i><span>%s%s</span></div>' % (j, E(d), E(ORT[j]), ' ' + BALD if b else '') for j, (d, s, b) in enumerate(AUSSEN))
    streifen = ''.join(fo(k, '(max-width:900px) 30vw, 14vw', '', pos=p) for k, p in (('fw-a45', '50% 30%'), ('uw-singen', '50% 30%'), ('uw-tische', '50% 40%'), ('fw-a46', '50% 40%')))
    return sek(2, '<div class="u02-plakat auf"><div class="u02-streifen">%s</div><div class="u02-mitte">%s%s</div><div class="u02-liste">%s</div></div><div class="u02-unten">%s</div>' % (
        streifen, kz(), titel('t-gross'), reihen, text()))


@v(3, 'Die Linie')
def _():
    halte = ''.join('<div class="u03-h" style="--n:%d"><i></i><span class="etikett">%s</span><b class="titel">%s</b><p>%s%s</p></div>' % (
        j, E(d), E(ORT[j]), E(REST[j]), ' ' + BALD if b else '') for j, (d, s, b) in enumerate(AUSSEN))
    bilder = ''.join(fo(k, '(max-width:900px) 46vw, 24vw', '', pos=p) for k, p in (('uw-kiez', '50% 45%'), ('fw-a45', '50% 30%'), ('uw-stuehle', '50% 50%'), ('uw-sonne', '50% 40%')))
    return sek(3, '<div class="u03-kopf">%s%s%s</div><div class="u03-linie auf"><div class="u03-strich"></div>%s</div><div class="u03-bilder auf">%s</div>' % (
        kz(), titel(), text(), halte, bilder))


@v(4, 'Die Markise')
def _():
    return sek(4, '<div class="u04-markise auf" aria-hidden="true"><div class="u04-tuch"></div></div><div class="innen u04-stand">'
               '<div class="u04-bilder">%s%s</div><div>%s%s%s%s</div></div>' % (
                   fo('fw-a45', '(max-width:900px) 46vw, 22vw', 'u04-a', pos='50% 30%'), fo('fw-a46', '(max-width:900px) 46vw, 22vw', 'u04-b', pos='50% 40%'),
                   kz(), titel(), text(), zeilen()), False)


@v(5, 'Die Eintrittskarten')
def _():
    karten = ''.join('<div class="u05-k%s" style="--n:%d"><div class="u05-abriss"><span class="etikett">%s</span></div><div class="u05-haupt"><b class="titel">%s</b><p>%s</p></div></div>' % (
        ' u05-rot' if b else '', j, E(d), E(ORT[j]), E(REST[j])) for j, (d, s, b) in enumerate(AUSSEN))
    return sek(5, '<div class="u05-raster"><div>%s%s</div><div class="u05-stapel auf">%s</div></div>' % (kopf(), fo('uw-stuehle', '(max-width:900px) 92vw, 40vw', 'u05-bild', pos='50% 55%'), karten))


@v(6, 'Die Postkarten')
def _():
    karten = ''.join('<div class="u06-p" style="--n:%d"><div class="u06-l"><b class="titel">%s</b><p>%s</p></div><div class="u06-r"><span class="u06-marke"><b>WILD<br>SIDE</b></span><span class="u06-adr">%s</span><span class="u06-adr">%s</span>%s</div></div>' % (
        j, E(ORT[j]), E(REST[j]), E(d), E(WO[j]), BALD if b else '') for j, (d, s, b) in enumerate(AUSSEN))
    return sek(6, '<div class="u06-raster"><div class="u06-links">%s%s</div><div class="u06-karten auf">%s</div></div>' % (
        kopf(), fo('uw-sonne', '(max-width:900px) 92vw, 36vw', 'u06-bild', pos='50% 45%'), karten))


@v(7, 'Die Plakatsäule')
def _():
    pl = ''.join('<figure class="u07-pl" style="--n:%d;--lq:url(%s)">%s</figure>' % (j, mache(k)['lq'], B.img_tag(k, '(max-width:900px) 40vw, 16vw')) for j, k in enumerate(('uw-pl-limmer25', 'uw-pl-okt', 'uw-pl-limmer')))
    return sek(7, '<div class="zwei u07-raster"><div>%s%s</div><div class="u07-saeule auf"><div class="u07-rund">%s</div></div></div>' % (kopf(), zeilen(), pl))


@v(8, 'Das Nächste zuerst')
def _():
    d, s, b = AUSSEN[0]
    rest = ''.join('<div><span class="etikett">%s</span><span>%s</span></div>' % (E(d2), E(s2)) for d2, s2, b2 in AUSSEN[1:])
    return sek(8, '<div class="u08-kopf">%s%s%s</div><div class="u08-gross auf"><div class="u08-datum"><span class="etikett">%s · bald</span><b class="titel"><span>31.10.</span><span>01.11.</span></b><p>%s</p></div>%s</div>'
               '<div class="zeilen u08-rest sw" style="--i:2">%s</div>' % (kz(), titel(), text(), E(ORT[0]), E(s), fo('uw-pl-okt', '(max-width:900px) 70vw, 30vw', 'u08-pl'), rest))


@v(9, 'Der Aufsteller')
def _():
    tafel = ''.join('<div><span>%s</span><b>%s</b></div>' % (E(d), E(ORT[j]) + (' · bald' if b else '')) for j, (d, s, b) in enumerate(AUSSEN))
    return sek(9, '<div class="u09-raster"><div class="u09-strasse">%s<div class="u09-aufsteller auf"><div class="u09-tafel"><p class="titel">Unterwegs</p>%s</div><i class="u09-fuss"></i></div></div><div>%s</div></div>' % (
        fo('schild-ecke', '(max-width:900px) 92vw, 50vw', 'u09-bild', pos='50% 50%'), tafel, kopf()))


@v(10, 'Die Fotowand')
def _():
    wand = [('uw-tanz', '50% 40%'), ('fw-a45', '50% 30%'), ('uw-kiez', '50% 50%'), ('uw-singen', '50% 30%'), ('uw-sonne', '50% 40%'), ('fw-a46', '50% 40%'), ('uw-buehne', '50% 35%')]
    w = ''.join('<figure class="u10-f" style="--n:%d;--lq:url(%s)">%s</figure>' % (j, mache(k)['lq'], B.img_tag(k, '(max-width:900px) 46vw, 22vw', extra=' style="object-position:%s"' % p)) for j, (k, p) in enumerate(wand))
    return sek(10, '<div class="u10-wand auf">%s</div><div class="innen zwei u10-unten"><div>%s%s%s</div>%s</div>' % (w, kz(), titel(), text(), zeilen()), False)


@v(11, 'Die Stempel')
def _():
    formen = ['rund', 'eck', 'oval', 'rund', 'eck']
    st = ''.join('<div class="u11-s u11-%s" style="--n:%d;--r:%ddeg"><span class="etikett">%s</span><b class="titel">%s</b><small>%s</small></div>' % (
        formen[j], j, (-7, 5, -3, 8, -5)[j], E(WO[j]), E(ORT[j]), E(d)) for j, (d, s, b) in enumerate(AUSSEN))
    return sek(11, '<div class="u11-raster"><div>%s%s</div><div class="u11-blatt hell auf">%s</div></div>' % (kopf(), zeilen(), st))


@v(12, 'Der Faden')
def _():
    bild = {0: ('uw-pl-okt', '50% 50%'), 3: ('uw-buehne', '50% 35%')}
    s = ''
    for j, (d, x, b) in enumerate(AUSSEN):
        rechts = fo(bild[j][0], '(max-width:900px) 70vw, 26vw', 'u12-bild', pos=bild[j][1]) if j in bild else '<b class="titel u12-zahl">%s</b>' % E(kurz(d))
        s += '<div class="u12-schritt auf" style="--n:%d"><i class="u12-punkt"></i><div class="u12-t"><span class="etikett">%s</span><h3 class="titel t-mittel">%s</h3><p class="text">%s%s</p></div>%s</div>' % (
            j, E(d), E(ORT[j]), E(REST[j]), ' ' + BALD if b else '', rechts)
    return sek(12, '<div class="u12-kopf">%s%s%s</div><div class="u12-faden">%s</div>' % (kz(), titel(), text(), s))


@v(13, 'Der Abreisskalender')
def _():
    bl = ''.join('<div class="u13-b" style="--n:%d"><span class="etikett">%s</span><b class="titel">%s</b><p>%s%s</p></div>' % (
        j, E(d), E(ORT[j]), E(REST[j]), ' ' + BALD if b else '') for j, (d, s, b) in enumerate(AUSSEN))
    return sek(13, '<div class="u13-raster"><div>%s%s</div><div class="u13-block auf"><div class="u13-spirale" aria-hidden="true"></div>%s</div></div>' % (
        kopf(), fo('uw-tische', '(max-width:900px) 92vw, 40vw', 'u13-bild', pos='50% 45%'), bl))


@v(14, 'Die Bändchen')
def _():
    farben = ['rot', 'gold', 'blau', 'creme', 'rot2']
    bd = ''.join('<div class="u14-band u14-%s" style="--n:%d;--r:%.1fdeg"><span>%s</span><b>%s</b><em>%s</em><i class="u14-clip"></i></div>' % (
        farben[j], j, (-3, 2, -1.5, 3, -2)[j], E(d), E(ORT[j]).upper(), 'BALD' if b else E(WO[j]).upper()) for j, (d, s, b) in enumerate(AUSSEN))
    return sek(14, '<div class="u14-raster">%s<div>%s<div class="u14-baender auf">%s</div></div></div>' % (
        fo('uw-tanz', '(max-width:900px) 92vw, 38vw', 'u14-bild', pos='50% 40%'), kopf(), bd))


@v(15, 'Der Wegweiser')
def _():
    pf = ''.join('<div class="u15-pfeil u15-%s" style="--n:%d"><span class="etikett">%s</span><b class="titel">%s</b></div>' % (
        'l' if j % 2 else 'r', j, E(d) + (' · bald' if b else ''), E(ORT[j])) for j, (d, s, b) in enumerate(AUSSEN))
    return sek(15, '<div class="u15-raster"><div>%s%s</div><div class="u15-pfahl-w auf"><div class="u15-pfahl"></div>%s</div>%s</div>' % (
        kopf(), zeilen(), pf, fo('an-loge', '(max-width:900px) 92vw, 30vw', 'u15-bild', pos='50% 50%')))


def seite(n):
    eintrag = dict((nr, (nm, f)) for nr, nm, f in V)
    h = BASIS[:_a] + eintrag[n][1]() + BASIS[_b:] if n else BASIS
    liste = [[0, 'Heutiger Stand']] + [[nr, nm] for nr, nm, _ in V]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/u.css?v=%s"><link rel="stylesheet" href="%s/nav.css?v=%s"></head>' % (ORD, VER, ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>' % (n, E(eintrag[n][0] if n else 'Heutiger Stand'))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    assert len(V) == 15
    for n in range(16):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00.html … 15.html in', ORD)
