# Walk on the Wild Side · Haus-Seite, Abschnitt «Der Raum»: 20 Fassungen (31.10.2026, Runde nach raum-seite).
# Robert: «Das kann doch nicht sein. Bitte gib mir 20 verschiedene Visualisierungen.» Vorher: keine Bildwand, keine Fotos von anderen Seiten,
# in der Sprache der übrigen Seite (dunkle Tafel mit Goldlinie, Prata, Bögen, Filmstreifen).
# Fotos: nur theke und rueckbar-breit (stehen ausschliesslich auf der Haus-Seite), dazu Ausschnitte daraus. Jede Fassung eigene Anordnung, eigene Bewegung.
# Titel und Bildzeilen Wort für Wort aus unter.py. Aufruf: python3 _varianten/raum-20/bau.py → 00 … 20.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/raum-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

RAUM = [('decke', 'Decke', 'Die Decke: ein Gewölbe als Druck über dem ganzen Raum, blau und silbern angeleuchtet.'),
        ('schrift', 'Schrift', 'NEGRONI in Glühbirnen über der Vitrine. Der Schriftzug sagt, was hier jeden Abend gerührt wird.'),
        ('theke', 'Theke', 'Die Theke mit dem gelben Licht unter der Kante. Hier wird gefragt, was du magst.'),
        ('rueckbar', 'Rückbar', 'Die Rückbar: Flaschen, die man nicht in jedem Laden findet, und eine beleuchtete Vitrine.'),
        ('fenster', 'Fenster', 'Von der Strasse aus sieht man die Rückbar durchs Fenster, oben spiegelt sich die Decke.'),
        ('tuer', 'Tür', 'Durch die Tür: der rote Boden, links die Theke, hinten die Stufen hinauf zur Empore.')]
WORT = {k: w for k, w, _ in RAUM}
CAP = {k: t for k, _, t in RAUM}
_q = open('unter.py').read()
for _, _, t in RAUM:
    assert t in _q, 'Text weicht von der Seite ab: ' + t
assert "h2(['Mit Stil,', 'ganz entspannt.'])" in _q

FOTO = ['theke', 'rueckbar-breit']
# Ausschnitte: (Foto, Mitte x, Mitte y, Vergrösserung). Gelesen am Rasterbild der beiden Fotos.
AUS = {'decke': (0, .45, .10, 1.9), 'schrift': (1, .66, .62, 2.3), 'theke': (0, .70, .78, 2.0),
       'rueckbar': (1, .35, .38, 1.6), 'fenster': (0, .14, .45, 2.2), 'tuer': (0, .40, .62, 1.25)}


def tf(fx, fy, z):
    lim = (z - 1) / 2 * 100
    tx = max(-lim, min(lim, -(fx - .5) * z * 100))
    ty = max(-lim, min(lim, -(fy - .5) * z * 100))
    return 'translate(%.2f%%,%.2f%%) scale(%.2f)' % (tx, ty, z)


def foto(i, sizes='(max-width:760px) 100vw, 50vw', cls='q-f', stil='', extra=''):
    k = FOTO[i]
    return '<figure class="%s" style="--lq:url(%s);%s"%s>%s</figure>' % (cls, mache(k)['lq'], stil, extra, B.img_tag(k, sizes))


def aus(k, sizes='(max-width:760px) 90vw, 30vw', cls='q-f q-aus', stil=''):
    b, fx, fy, z = AUS[k]
    return foto(b, sizes, cls, '--t:%s;%s' % (tf(fx, fy, z), stil))


def kz():
    return B.kz('Der Raum', 'Fünf Blicke', 0)


def h2():
    return B.h2(['Mit Stil,', 'ganz entspannt.'])


def kopf(cls=''):
    return '<div class="q-kopf %s">%s%s</div>' % (cls, kz(), h2())


def sek(inner, cls='', voll=''):
    return '<section class="kap auf q %s" id="raum"><div class="innen">%s</div>%s</section>' % (cls, inner, voll)


def zeile(k, cls='q-z', stil=''):
    return '<div class="%s" style="%s"><span class="q-w titel">%s</span><p>%s</p></div>' % (cls, stil, E(WORT[k]), E(CAP[k]))


ALLE = [k for k, _, _ in RAUM]
V = []


def v(name):
    def d(f):
        V.append((name, f))
        return f
    return d


def blicke(ks):
    return E(json.dumps([[AUS[k][0], tf(*AUS[k][1:])] for k in ks]))


@v('Ein Foto, sechs Blicke')
def v01():
    # Gehaltene Strecke: ein Rahmen in normaler Grösse, die Kamera fährt im Foto von Stelle zu Stelle; rechts steigt der passende Satz aus dem Schlitz.
    rahmen = '<div class="b1-rahmen">%s%s</div>' % (foto(0, '(max-width:760px) 100vw, 50vw', 'q-f b1-f', extra=' data-bild="0"'),
                                                   foto(1, '(max-width:760px) 100vw, 50vw', 'q-f b1-f', extra=' data-bild="1"'))
    s = ''.join('<div class="b1-s" data-z="%d"><div><span class="etikett">%s</span><p class="titel">%s</p></div></div>' % (i, E(WORT[k]), E(CAP[k])) for i, k in enumerate(ALLE))
    return ('<section class="kap auf q b1-sek" id="raum"><div class="innen">%s</div><div class="b1" data-pin data-schritte="6" data-blicke="%s">'
            '<div class="b1-buehne"><div class="innen b1-g">%s<div class="b1-txt">%s</div></div></div></div></section>') % (kopf(), blicke(ALLE), rahmen, s)


@v('Zeigen und schauen')
def v02():
    # Links die sechs Teile in einer Tafel, rechts ein Foto. Zeigen oder Tippen auf eine Zeile fährt das Foto an diese Stelle.
    zl = ''.join('<button class="b2-z" data-t="%d"><span class="titel">%s</span><p>%s</p></button>' % (i, E(WORT[k]), E(CAP[k])) for i, k in enumerate(ALLE))
    return sek(kopf() + '<div class="b2 auf" data-tausch data-blicke="%s"><div class="platte b2-tafel">%s</div><div class="b2-rahmen">%s%s</div></div>' % (
        blicke(ALLE), zl, foto(0, extra=' data-bild="0"', cls='q-f b2-f'), foto(1, extra=' data-bild="1"', cls='q-f b2-f')))


@v('Das Medaillon')
def v03():
    # In der Mitte ein rundes Foto der Theke, links und rechts je drei Teile wie auf einer Karte.
    l = ''.join(zeile(k, 'q-z b3-z', '--n:%d' % i) for i, k in enumerate(ALLE[:3]))
    r = ''.join(zeile(k, 'q-z b3-z', '--n:%d' % (i + 3)) for i, k in enumerate(ALLE[3:]))
    return sek(kopf('q-mitte') + '<div class="b3 auf"><div class="b3-sp">%s</div><div class="b3-med">%s</div><div class="b3-sp">%s</div></div>' % (
        l, foto(0, '(max-width:760px) 80vw, 420px', 'q-f b3-f', '--t:%s' % tf(.5, .55, 1.15)), r))


@v('Die Barkarte')
def v04():
    # Eine dunkle Karte mit doppelter Goldlinie, oben ein ovales Foto der Vitrine, der Titel in der Karte, die Teile in zwei Spalten.
    zl = ''.join(zeile(k, 'q-z b4-z', '--n:%d' % i) for i, k in enumerate(ALLE))
    return sek('<div class="q-mitte">%s</div><div class="b4 auf"><div class="b4-in"><div class="b4-oval">%s</div>%s<i class="b4-strich"></i><div class="b4-zl">%s</div></div></div>' % (
        kz(), aus('schrift', '(max-width:760px) 70vw, 380px', 'q-f q-aus b4-f'), h2(), zl))


@v('Der Bogen')
def v05():
    # Links ein hoher Bogen wie das Gewölbe, darin steigt die Theke auf. Rechts Titel und die Teile untereinander.
    zl = ''.join(zeile(k, 'q-z b5-z', '--n:%d' % i) for i, k in enumerate(ALLE))
    return sek('<div class="b5 auf"><div class="b5-bogen"><div class="b5-in">%s</div></div><div>%s<div class="b5-zl">%s</div></div></div>' % (
        foto(0, '(max-width:760px) 90vw, 40vw', 'q-f b5-f', '--t:%s' % tf(.55, .55, 1.1)), kopf(), zl))


@v('Drei Nischen')
def v06():
    # Drei schmale Nischen mit rundem Abschluss, versetzt gehängt, jede mit einem Ausschnitt: das Gewölbe, die Lichtkante, die Vitrine.
    h = ''.join('<div class="b6-n" style="--n:%d"><div class="b6-nische">%s</div><span class="etikett">%s</span><p class="text">%s</p></div>' % (
        i, aus(k, '(max-width:760px) 80vw, 30vw', 'q-f q-aus b6-f'), E(WORT[k]), E(CAP[k])) for i, k in enumerate(['decke', 'theke', 'schrift']))
    return sek(kopf() + '<div class="b6 auf">%s</div>' % h)


@v('Der kurze Film')
def v07():
    # Ein kurzer Filmstreifen wie bei den Jahren, sechs Felder mit Ausschnitten, darunter die sechs Sätze in drei Spalten.
    fr = ''.join('<div class="b7-k"><span>%s</span>%s</div>' % (E(WORT[k]), aus(k, '(max-width:760px) 45vw, 16vw', 'q-f q-aus b7-f')) for k in ALLE)
    zl = ''.join(zeile(k, 'q-z b7-z', '--n:%d' % i) for i, k in enumerate(ALLE))
    return sek(kopf() + '<div class="b7 auf"><div class="b7-streifen">%s</div></div><div class="b7-zl auf">%s</div>' % (fr, zl))


@v('Säule und Detail')
def v08():
    # Eine hohe Säule mit der Theke, darunter versetzt ein kleiner Ausschnitt der Vitrine. Rechts die Teile. Die Säule wandert langsamer als die Seite.
    zl = ''.join(zeile(k, 'q-z b8-z', '--n:%d' % i) for i, k in enumerate(ALLE))
    return sek('<div class="b8" data-p><div class="b8-bilder"><div class="b8-saeule">%s</div><div class="b8-detail">%s</div></div><div>%s<div class="b8-zl">%s</div></div></div>' % (
        foto(0, '(max-width:760px) 70vw, 34vw', 'q-f b8-f'), aus('schrift', '(max-width:760px) 50vw, 20vw', 'q-f q-aus b8-f'), kopf(), zl))


@v('Aus dem Schlitz')
def v09():
    # Ein schmales Band der Rückbar steigt aus einer goldenen Linie, darunter die Teile in drei Spalten.
    zl = ''.join(zeile(k, 'q-z b9-z', '--n:%d' % i) for i, k in enumerate(ALLE))
    return sek(kopf() + '<div class="b9 auf"><div class="b9-band">%s</div><i class="b9-linie"></i><div class="b9-zl">%s</div></div>' % (
        foto(1, '(max-width:760px) 100vw, 1240px', 'q-f b9-f', '--t:%s' % tf(.5, .45, 1.05)), zl))


@v('Das Register')
def v10():
    # Wie ein Register: links gross das Wort, daneben der Satz, rechts ein kleiner runder Ausschnitt. Jede Zeile steigt aus ihrem Schlitz.
    zl = ''.join('<div class="b10-z" style="--n:%d"><span class="titel">%s</span><p class="text">%s</p><div class="b10-rund">%s</div></div>' % (
        i, E(WORT[k]), E(CAP[k]), aus(k, '160px', 'q-f q-aus b10-f')) for i, k in enumerate(ALLE))
    return sek(kopf() + '<div class="b10 auf">%s</div>' % zl)


@v('Orgelpfeifen')
def v11():
    # Drei Spalten aus Tafeln, jede Spalte anders hoch begonnen; zwei Tafeln tragen einen Ausschnitt. Die Spalten wandern beim Scrollen unterschiedlich schnell.
    def t(k):
        return '<div class="platte b11-t"><span class="etikett">%s</span><p class="text">%s</p></div>' % (E(WORT[k]), E(CAP[k]))
    def b(k):
        return '<div class="b11-b">%s</div>' % aus(k, '(max-width:760px) 90vw, 28vw', 'q-f q-aus b11-f')
    sp = [t('decke') + b('theke') + t('fenster'), t('schrift') + t('rueckbar'), b('rueckbar') + t('theke') + t('tuer')]
    return sek(kopf() + '<div class="b11" data-p>%s</div>' % ''.join('<div class="b11-sp" style="--s:%s">%s</div>' % (s, h) for s, h in zip(('-40px', '60px', '-10px'), sp)))


@v('Die Postkarte')
def v12():
    # Eine Postkarte der Bar. Vorne die Theke, hinten die sechs Teile und die Adresse. Tippen dreht sie um.
    zl = ''.join('<div><b>%s</b> %s</div>' % (E(WORT[k]), E(CAP[k])) for k in ALLE)
    return sek(kopf('q-mitte') + '<div class="b12 auf"><div class="b12-karte" data-wenden><div class="b12-vorn">%s<span class="b12-hin">Zum Umdrehen tippen</span></div>'
               '<div class="b12-hinten"><div class="b12-zl">%s</div><div class="b12-adr"><span class="titel">Walk on the Wild Side</span><p>Haasemannstraße 13<br>30449 Hannover-Linden</p></div></div></div></div>' % (
                   foto(0, '(max-width:760px) 90vw, 760px', 'q-f b12-f', '--t:%s' % tf(.5, .55, 1.0)), zl))


@v('Zwei Abzüge')
def v13():
    # Auf einer dunklen Tafel liegen zwei Abzüge mit hellem Rand, darunter steht, was drauf ist. Die übrigen Teile folgen als Zeilen.
    a = lambda i, k, n: '<div class="b13-a" style="--n:%d"><div class="b13-rand">%s</div><span class="etikett">%s</span><p class="text">%s</p></div>' % (
        n, foto(i, '(max-width:760px) 80vw, 34vw', 'q-f b13-f'), E(WORT[k]), E(CAP[k]))
    zl = ''.join(zeile(k, 'q-z b13-z', '--n:%d' % i) for i, k in enumerate(['decke', 'schrift', 'fenster', 'tuer']))
    return sek(kopf() + '<div class="b13 auf"><div class="platte b13-tafel">%s%s</div><div class="b13-zl">%s</div></div>' % (a(0, 'theke', 0), a(1, 'rueckbar', 1), zl))


@v('Zickzack')
def v14():
    # Sechs Teile im Wechsel links und rechts, jeder mit eigenem Abstand; drei davon mit einem Ausschnitt.
    h = ''
    for i, k in enumerate(ALLE):
        bild = aus(k, '(max-width:760px) 90vw, 36vw', 'q-f q-aus b14-f') if k in ('decke', 'theke', 'rueckbar') else ''
        h += '<div class="auf b14-e%s%s" style="--n:%d">%s<div class="b14-t"><span class="titel">%s</span><p class="text">%s</p></div></div>' % (
            ' b14-r' if i % 2 else '', ' b14-mit' if bild else '', i, ('<div class="b14-b">%s</div>' % bild) if bild else '', E(WORT[k]), E(CAP[k]))
    return sek(kopf() + '<div class="b14">%s</div>' % h)


@v('Die Lupe')
def v15():
    # Die Rückbar in normaler Grösse, eine runde Lupe wandert beim Scrollen über die Flaschen bis zur Vitrine. Darunter die Teile.
    zl = ''.join(zeile(k, 'q-z b15-z', '--n:%d' % i) for i, k in enumerate(ALLE))
    return sek(kopf() + '<div class="b15" data-p><div class="b15-foto">%s<div class="b15-lupe"><div class="b15-zoom">%s</div></div></div></div><div class="b15-zl auf">%s</div>' % (
        foto(1, '(max-width:760px) 100vw, 64vw', 'q-f b15-f'), foto(1, '(max-width:760px) 100vw, 1240px', 'q-f b15-zf'), zl))


@v('Unter dem Bogen')
def v16():
    # Der ganze Abschnitt steht in einem grossen Bogen mit doppelter Goldlinie, wie die Bewertungen: Titel, ein Bild im kleinen Bogen, die Teile in drei Spalten.
    zl = ''.join(zeile(k, 'q-z b16-z', '--n:%d' % i) for i, k in enumerate(ALLE))
    return sek('<div class="b16 auf"><div class="b16-in"><div class="q-mitte">%s%s</div><div class="b16-bild">%s</div><div class="b16-zl">%s</div></div></div>' % (
        kz(), h2(), foto(0, '(max-width:760px) 80vw, 560px', 'q-f b16-f', '--t:%s' % tf(.5, .5, 1.25)), zl))


@v('Der Kontaktbogen')
def v17():
    # Sechs kleine Ausschnitte in einer Reihe wie ein Kontaktbogen; der gewählte Satz steht gross darüber und wechselt beim Zeigen oder Tippen.
    gr = ''.join('<p class="titel b17-g" data-z="%d"><span class="etikett">%s</span>%s</p>' % (i, E(WORT[k]), E(CAP[k])) for i, k in enumerate(ALLE))
    kl = ''.join('<button class="b17-k" data-t="%d" aria-label="%s">%s</button>' % (i, E(WORT[k]), aus(k, '(max-width:760px) 33vw, 200px', 'q-f q-aus b17-f')) for i, k in enumerate(ALLE))
    return sek(kopf() + '<div class="b17 auf" data-tausch><div class="b17-gross">%s</div><div class="b17-reihe">%s</div></div>' % (gr, kl))


@v('Entlang der Theke')
def v18():
    # Gehaltene Strecke: oben ein flaches Band der Theke, darunter die Lichtkante mit sechs Stationen. Ein Licht wandert die Kante entlang, der Satz der Station steigt darunter auf.
    st = ''.join('<span class="b18-st" style="left:%.1f%%" data-z="%d">%s</span>' % (8 + i * 16.8, i, E(WORT[k])) for i, k in enumerate(ALLE))
    s = ''.join('<p class="titel b18-s" data-z="%d">%s</p>' % (i, E(CAP[k])) for i, k in enumerate(ALLE))
    return ('<section class="kap auf q b18-sek" id="raum"><div class="innen">%s</div><div class="b18" data-pin data-schritte="6"><div class="b18-buehne"><div class="innen">'
            '<div class="b18-band">%s</div><div class="b18-kante"><i class="b18-licht"></i>%s</div><div class="b18-saetze">%s</div></div></div></div></section>') % (
        kopf(), foto(0, '(max-width:760px) 100vw, 1240px', 'q-f b18-f', '--t:%s' % tf(.6, .78, 1.0)), st, s)


@v('Säule in der Mitte')
def v19():
    # Eine schmale hohe Säule mit der Theke steht in der Mitte, das Bild wandert langsam darin. Links und rechts die Worte gross, versetzt, mit ihrem Satz.
    l = ''.join('<div class="b19-w" style="--n:%d"><span class="titel">%s</span><p class="text">%s</p></div>' % (i, E(WORT[k]), E(CAP[k])) for i, k in enumerate(ALLE[0::2]))
    r = ''.join('<div class="b19-w" style="--n:%d"><span class="titel">%s</span><p class="text">%s</p></div>' % (i, E(WORT[k]), E(CAP[k])) for i, k in enumerate(ALLE[1::2]))
    return sek(kopf('q-mitte') + '<div class="b19 auf" data-p><div class="b19-sp">%s</div><div class="b19-saeule">%s</div><div class="b19-sp b19-r">%s</div></div>' % (
        l, foto(0, '(max-width:760px) 60vw, 300px', 'q-f b19-f'), r))


@v('Die Vitrine')
def v20():
    # Wie die beleuchtete Vitrine: drei Böden mit goldener Kante, auf jedem zwei Stücke, je ein kleiner Ausschnitt mit einem hellen Schildchen davor.
    def stueck(k):
        return '<div class="b20-s"><div class="b20-b">%s</div><div class="b20-schild"><b>%s</b><p>%s</p></div></div>' % (
            aus(k, '(max-width:760px) 45vw, 22vw', 'q-f q-aus b20-f'), E(WORT[k]), E(CAP[k]))
    boeden = ''.join('<div class="b20-boden" style="--n:%d">%s%s</div>' % (i, stueck(a), stueck(b)) for i, (a, b) in enumerate([('decke', 'schrift'), ('theke', 'rueckbar'), ('fenster', 'tuer')]))
    return sek(kopf() + '<div class="b20 auf"><div class="b20-kasten">%s</div></div>' % boeden)


N = len(V)
assert N == 20


def seite(n):
    h = unter.haus()
    if n:
        a = h.find('<section class="kap auf" id="raum">')
        b = h.find('</section>', a) + len('</section>')
        assert a > 0 and b > a + 100
        h = h[:a] + V[n - 1][1]() + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, N, E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(N + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', N)
