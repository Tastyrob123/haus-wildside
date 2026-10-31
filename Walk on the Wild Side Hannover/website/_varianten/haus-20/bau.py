# Walk on the Wild Side · Haus-Seite, Abschnitt «Der Raum»: 20 neue Fassungen, dritte Runde (31.10.2026).
# Robert: «deine ganzen Frontend-Schläge alles scheiße … nochmal 20 weitere Visualisierungsmöglichkeiten».
# Anders als haus-15 und haus-15b: voll, gross, Wand an Wand, mehr echte Raumfotos (acht, die auf der Haus-Seite noch fehlen),
# Bewegung nur aus dem, was bei Wild Side abgenommen ist: Kamerafahrt, Steigen aus dem Schlitz, Zoom im Rahmen. Keine Requisiten,
# nichts seitwärts, kein Drehen, keine Überblendung. Titel seit 31.10.2026 «Mit Stil, ganz entspannt.». Bildzeilen Wort für Wort aus unter.py.
# Aufruf: python3 _varianten/haus-20/bau.py → 00 … 20.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
import bilder
from bilder import mache

# Ein Raumfoto, das bilder.py noch nicht kennt (nur für diese Fassungen, bilder.py bleibt unberührt)
bilder.BILDER.setdefault('rm-g07', ('google-maps/google-07.jpg', 'Der Raum am Abend: Gäste an der Theke im gelben Licht, rechts die Rückbar'))
bilder.BILDER.setdefault('rm-glaeser', ('google-maps/google-27.jpg', 'Glasbehälter mit Zapfhahn auf der Rückbar, warm angeleuchtet'))

E = html.escape
ORD = '_varianten/haus-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))
N = 20

RAUM = [('decke-bar', 'Die Decke: ein Gewölbe als Druck über dem ganzen Raum, blau und silbern angeleuchtet.'),
        ('negroni', 'NEGRONI in Glühbirnen über der Vitrine. Der Schriftzug sagt, was hier jeden Abend gerührt wird.'),
        ('theke', 'Die Theke mit dem gelben Licht unter der Kante. Hier wird gefragt, was du magst.'),
        ('rueckbar-breit', 'Die Rückbar: Flaschen, die man nicht in jedem Laden findet, und eine beleuchtete Vitrine.'),
        ('fenster', 'Von der Strasse aus sieht man die Rückbar durchs Fenster, oben spiegelt sich die Decke.'),
        ('tuer-rot', 'Durch die Tür: der rote Boden, links die Theke, hinten die Stufen hinauf zur Empore.')]
CAP = dict(RAUM)
_q = open('unter.py').read()
for _, t in RAUM:
    assert t in _q, 'Text weicht von der Seite ab: ' + t
assert "h2(['Mit Stil,', 'ganz entspannt.'])" in _q


def fig(k, sizes='33vw', cls='', stil='', cap=True, extra=''):
    c = '<figcaption class="ov">%s</figcaption>' % E(CAP[k]) if (cap and k in CAP) else ''
    return '<figure class="hv-f %s" style="--lq:url(%s);%s"%s>%s%s</figure>' % (cls, mache(k)['lq'], stil, extra, B.img_tag(k, sizes), c)


def kopf(cls=''):
    return '<div class="hv-kopf %s">%s%s</div>' % (cls, B.kz('Der Raum', 'Fünf Blicke', 0), B.h2(['Mit Stil,', 'ganz entspannt.']))


def sek(inner, cls='', voll='', vor=''):
    return '<section class="kap auf hv %s" id="raum">%s<div class="innen">%s</div>%s</section>' % (cls, vor, inner, voll)


def zeilen(ks, cls='hv-zeilen'):
    return '<div class="%s">%s</div>' % (cls, ''.join('<p class="text">%s</p>' % E(CAP[k]) for k in ks if k in CAP))


V = []


def v(name):
    def d(f):
        V.append((name, f))
        return f
    return d


@v('Die Kamera fährt an die Theke')
def v01():
    # Gehaltene Strecke: das Bild füllt den Schirm, die Kamera fährt langsam an den Tresen heran (bremst auf drei Vierteln), der Titel steht unten links.
    # Danach die sechs Blicke als Wand, Bildzeile im Bild.
    film = ('<div class="k1" data-pin><div class="k1-buehne"><div class="k1-bild">%s</div>'
            '<div class="innen k1-text">%s</div></div></div>') % (fig('rm-g07', '100vw', cap=False), kopf())
    wand = '<div class="auf k1-wand">%s</div>' % ''.join(fig(k, '(max-width:760px) 50vw, 33vw', 'k1-z', '--n:%d' % n) for n, (k, _) in enumerate(RAUM))
    return '<section class="kap auf hv k1-sek" id="raum">%s<div class="innen">%s</div></section>' % (film, wand)


@v('Die Wand')
def v02():
    # Zwölf Felder, zehn Fotos Wand an Wand mit schmaler dunkler Fuge, gemischte Grössen. Die Wand steigt als Ganzes, jedes Foto setzt sich im Rahmen.
    ks = [('decke-flach', 'a'), ('decke-bar', 'b'), ('negroni', 'c'), ('theke', 'd'), ('rm-glaeser', 'e'), ('rueckbar-breit', 'f'),
          ('fw-a31', 'g'), ('fenster', 'h'), ('tuer-rot', 'i'), ('alt-raum', 'j')]
    w = ''.join(fig(k, '(max-width:760px) 50vw, 40vw', 'w2-z', 'grid-area:%s' % a) for k, a in ks)
    return sek(kopf() + '<div class="auf w2">%s</div>' % w)


@v('Das Mosaik')
def v03():
    # Links setzt sich das Foto vom Tresen aus zwölf Stücken zusammen, die von unten steigen und sich schliessen. Rechts die sechs Blicke, dicht.
    d = mache('alt-raum')
    url = 'assets/bild/%s?v=%s' % ([f for b, f in d['stufen'] if b >= 1200][0], B.V)
    st = ''.join('<i style="background-image:url(%s);--x:%d;--y:%d;--n:%d"></i>' % (url, x, y, (x * 3 + y * 5) % 12) for y in range(4) for x in range(3))
    mos = '<div class="m3-mos" role="img" aria-label="%s" style="--u:url(%s)">%s</div>' % (E(d['alt']), url, st)
    rechts = '<div class="m3-r">%s</div>' % ''.join(fig(k, '(max-width:760px) 50vw, 25vw', 'm3-z', '--n:%d' % n) for n, (k, _) in enumerate(RAUM))
    return sek(kopf() + '<div class="auf m3">%s%s</div>' % (mos, rechts))


@v('Breitbild und vier Säulen')
def v04():
    # Oben der ganze Raum im Breitbild, darunter vier hohe Bilder Kante an Kante. Erst kommt das Breitbild, die Säulen steigen mit.
    oben = fig('decke-flach', '(max-width:760px) 100vw, 1200px', 'b4-breit', cap=False)
    s = ''.join(fig(k, '(max-width:760px) 50vw, 25vw', 'b4-s', '--n:%d' % n) for n, k in enumerate(['negroni', 'theke', 'alt-raum', 'tuer-rot']))
    return sek(kopf() + '<div class="auf b4">%s<div class="b4-reihe">%s</div></div>' % (oben, s))


@v('Drei Akte')
def v05():
    # Drei Reihen, je ein breites und ein hohes Bild, die Seiten wechseln. Jede Reihe steigt für sich, die Bilder zoomen im Rahmen.
    reihen = [('decke-flach', 'decke-bar'), ('rueckbar-breit', 'negroni'), ('pf-raum', 'tuer-rot')]
    h = ''.join('<div class="auf a5-r %s">%s%s</div>' % ('a5-spiegel' if n == 1 else '', fig(b, '(max-width:760px) 100vw, 66vw', 'a5-b'), fig(t, '(max-width:760px) 100vw, 33vw', 'a5-t'))
                for n, (b, t) in enumerate(reihen))
    return sek(kopf() + h)


@v('Fünf Säulen')
def v06():
    # Fünf hohe Bilder über die ganze Breite, Kante an Kante. Beim Scrollen wandert das Foto in seinem Rahmen leicht nach oben, jede Säule im eigenen Mass.
    ks = ['decke-bar', 'negroni', 'theke', 'fenster', 'tuer-rot']
    s = ''.join(fig(k, '(max-width:760px) 50vw, 20vw', 's6-s', '--n:%d' % n, cap=False) for n, k in enumerate(ks))
    zl = '<div class="s6-zl innen">%s</div>' % ''.join('<p class="text">%s</p>' % E(CAP[k]) for k in ks)
    return sek(kopf(), voll='<div class="auf s6" data-p>%s</div>%s' % (s, zl))


@v('Das Triptychon')
def v07():
    # Wie ein Altar unter dem Gewölbe: in der Mitte die Decke hoch und oben gerundet, links und rechts je zwei Bilder übereinander, alles Kante an Kante.
    l = fig('negroni', '25vw', 't7-f') + fig('theke', '25vw', 't7-f')
    r = fig('rueckbar-breit', '25vw', 't7-f') + fig('tuer-rot', '25vw', 't7-f')
    m = fig('decke-bar', '(max-width:760px) 100vw, 40vw', 't7-m')
    return sek(kopf('hv-mitte') + '<div class="auf t7"><div class="t7-fl">%s</div>%s<div class="t7-fl t7-fr">%s</div></div>' % (l, m, r))


@v('Gewölbefenster')
def v08():
    # Sechs hohe Fenster mit rundem Bogen oben, wie im Kirchenschiff, das die Decke zeigt. Die Mitte am höchsten, nach aussen niedriger. Steigen von links nach rechts.
    ks = ['tuer-rot', 'theke', 'decke-bar', 'negroni', 'rueckbar-breit', 'fenster']
    h = ''.join(fig(k, '(max-width:760px) 50vw, 17vw', 'g8-f', '--n:%d;--h:%s' % (n, ['74', '86', '100', '100', '86', '74'][n])) for n, k in enumerate(ks))
    return sek(kopf('hv-mitte') + '<div class="auf g8">%s</div>' % h)


@v('Die Lichtkante')
def v09():
    # Quer durch den Abschnitt läuft die gelbe Lichtkante der Theke und zieht sich von der Mitte nach aussen. Darüber steht, was oben ist, darunter, was unten ist.
    o = ''.join(fig(k, '(max-width:760px) 50vw, 33vw', 'l9-o', '--n:%d' % n) for n, k in enumerate(['decke-bar', 'negroni', 'rueckbar-breit']))
    u = ''.join(fig(k, '(max-width:760px) 50vw, 33vw', 'l9-u', '--n:%d' % n) for n, k in enumerate(['theke', 'fenster', 'tuer-rot']))
    return sek(kopf(), voll='<div class="auf l9"><div class="innen l9-reihe l9-oben">%s</div><div class="l9-kante" aria-hidden="true"></div><div class="innen l9-reihe l9-unten">%s</div></div>' % (o, u))


@v('Grosses Bild, Reihe darunter')
def v10():
    # Wie bei den Zimmern: ein grosses Bild, darunter alle zehn Ansichten Kante an Kante. Zeigen oder Tippen holt ein Bild nach oben, es steigt im Rahmen hoch.
    ks = ['decke-flach', 'decke-bar', 'negroni', 'theke', 'rueckbar-breit', 'rm-glaeser', 'fw-a31', 'fenster', 'tuer-rot', 'pf-raum']
    buehne = ''.join('<div class="z10-z" data-z="%d">%s</div>' % (n, fig(k, '(max-width:760px) 100vw, 1200px', cap=False)) for n, k in enumerate(ks))
    satz = ''.join('<p class="text z10-s" data-z="%d">%s</p>' % (n, E(CAP.get(k, mache(k)['alt'] + '.'))) for n, k in enumerate(ks))
    reihe = ''.join('<button class="z10-t" data-t="%d" aria-label="%s">%s</button>' % (n, E(mache(k)['alt']), fig(k, '(max-width:760px) 20vw, 10vw', cap=False)) for n, k in enumerate(ks))
    return sek(kopf() + '<div class="auf z10" data-tausch><div class="z10-b">%s</div><div class="z10-sz">%s</div><div class="z10-r">%s</div></div>' % (buehne, satz, reihe))


@v('Im Kinoformat')
def v11():
    # Gehaltene Strecke im Breitformat wie im Kino: ein Filmstreifen aus sechs Bildern fährt im Rahmen nach oben, ohne Schnitt. Darunter läuft die Bildzeile mit.
    st = ''.join(fig(k, '(max-width:760px) 100vw, 1200px', 'c11-f', cap=False) for k, _ in RAUM)
    sz = ''.join('<p class="text c11-s" data-z="%d">%s</p>' % (n, E(t)) for n, (_, t) in enumerate(RAUM))
    return sek('', voll='<div class="c11" data-pin data-schritte="6"><div class="c11-buehne"><div class="innen">%s<div class="c11-rahmen"><div class="c11-streifen">%s</div></div><div class="c11-sz">%s</div></div></div></div>' % (kopf(), st, sz))


@v('Titel gross, Wand daneben')
def v12():
    # Links der Titel sehr gross, darunter der Satz zum Bild, auf das man zeigt. Rechts sechs Bilder Wand an Wand, so hoch wie der Schirm.
    links = '<div class="w12-l">%s<div class="w12-sz">%s</div></div>' % (
        '<div class="hv-kopf">%s<h2 class="titel w12-t">%s</h2></div>' % (B.kz('Der Raum', 'Fünf Blicke', 0), B.zl(['Mit Stil,', 'ganz entspannt.'])),
        ''.join('<p class="text w12-s" data-z="%d">%s</p>' % (n, E(t)) for n, (_, t) in enumerate(RAUM)))
    rechts = '<div class="w12-r">%s</div>' % ''.join('<div class="w12-z" data-t="%d" tabindex="0">%s</div>' % (n, fig(k, '(max-width:760px) 50vw, 30vw', cap=False)) for n, (k, _) in enumerate(RAUM))
    return sek('<div class="auf w12" data-tausch>%s%s</div>' % (links, rechts))


@v('Von oben nach unten')
def v13():
    # Der Raum als Schnitt von oben nach unten: zuoberst die Decke über die ganze Breite, dann die Rückbar, dann die Theke, zuletzt Tür und Stufen.
    e = [[('decke-flach', '100%')], [('negroni', '34%'), ('rueckbar-breit', '42%'), ('rm-glaeser', '24%')], [('theke', '50%'), ('fw-a31', '50%')], [('tuer-rot', '58%'), ('alt-raum', '42%')]]
    h = ''.join('<div class="auf o13-e o13-e%d">%s</div>' % (i, ''.join(fig(k, '(max-width:760px) 100vw, 50vw', 'o13-f', 'flex-basis:%s' % w) for k, w in r)) for i, r in enumerate(e))
    return sek(kopf() + '<div class="o13">%s</div>' % h)


@v('Die Doppelseite')
def v14():
    # Wie eine aufgeschlagene Magazinseite im Dunkeln: links ein Bild über die ganze Seite, rechts drei Bilder übereinander, dazwischen der Falz.
    # Der Titel läuft gross über beide Seiten.
    links = fig('fw-a12', '(max-width:760px) 100vw, 50vw', 'd14-l', cap=False)
    rechts = '<div class="d14-r">%s</div>' % ''.join(fig(k, '(max-width:760px) 100vw, 45vw', 'd14-f') for k in ['negroni', 'theke', 'tuer-rot'])
    return sek('<div class="hv-kopf d14-kopf">%s<h2 class="titel d14-t">%s</h2></div><div class="auf d14">%s<i class="d14-falz" aria-hidden="true"></i>%s</div>' % (
        B.kz('Der Raum', 'Fünf Blicke', 0), B.zl(['Mit Stil, ganz entspannt.']), links, rechts))


@v('Spalten im eigenen Takt')
def v15():
    # Drei Spalten mit zehn Bildern; beim Scrollen läuft die mittlere langsamer als die äusseren, wie die Filmstreifen beim Rivage, nur senkrecht.
    sp = [['decke-bar', 'theke', 'fenster'], ['decke-flach', 'negroni', 'rm-glaeser', 'pf-raum'], ['rueckbar-breit', 'fw-a31', 'tuer-rot']]
    h = ''.join('<div class="t15-s t15-s%d">%s</div>' % (i, ''.join(fig(k, '(max-width:760px) 50vw, 33vw', 't15-f') for k in s)) for i, s in enumerate(sp))
    return sek(kopf() + '<div class="auf t15" data-p>%s</div>' % h)


@v('Wo das Licht sitzt')
def v16():
    # Sechs Lichter des Raums, eine Wand aus sechs grossen Feldern. Jedes Foto setzt sich von seinem Licht aus: der Zoom geht vom Licht im Bild zurück aufs ganze Bild.
    ks = [('decke-bar', '50% 20%'), ('negroni', '50% 35%'), ('theke', '40% 75%'), ('fw-a12', '30% 85%'), ('an-campari', '50% 40%'), ('tuer-rot', '45% 70%')]
    h = ''.join(fig(k, '(max-width:760px) 50vw, 33vw', 'l16-f', '--n:%d;--o:%s' % (n, o)) for n, (k, o) in enumerate(ks))
    return sek(kopf() + '<div class="auf l16">%s</div>' % h)


@v('Die Bühne')
def v17():
    # Über die ganze Breite: in der Mitte gross ein Bild, links und rechts laufen die Flügel bis an den Rand. Zwei Reihen, die zweite gespiegelt.
    r1 = fig('negroni', '25vw', 'b17-f') + fig('decke-flach', '50vw', 'b17-m', cap=False) + fig('theke', '25vw', 'b17-f')
    r2 = fig('fenster', '25vw', 'b17-f') + fig('rueckbar-breit', '50vw', 'b17-m') + fig('tuer-rot', '25vw', 'b17-f')
    return sek(kopf('hv-mitte'), voll='<div class="auf b17"><div class="b17-r">%s</div><div class="b17-r b17-r2">%s</div></div>' % (r1, r2))


@v('Ein Bild, ganz gross')
def v18():
    # Der Raum mit der Kerze im Vordergrund über den ganzen Schirm, Titel und Bildzeilen darauf. Darunter die sechs Blicke als hohe Leiste von Rand zu Rand.
    gross = '<div class="g18" data-p>%s<div class="innen g18-text">%s%s</div></div>' % (fig('fw-a12', '100vw', 'g18-b', cap=False), kopf(), zeilen([k for k, _ in RAUM], 'g18-zl'))
    leiste = '<div class="auf g18-l">%s</div>' % ''.join(fig(k, '(max-width:760px) 50vw, 17vw', 'g18-f', '--n:%d' % n, cap=False) for n, (k, _) in enumerate(RAUM))
    return '<section class="kap auf hv g18-sek" id="raum">%s%s</section>' % (gross, leiste)


@v('Jedes Bild im eigenen Format')
def v19():
    # Zehn Fotos in drei Reihen, jedes in seinem eigenen Seitenverhältnis, jede Reihe genau über die ganze Breite. Nichts wird beschnitten.
    reihen = [['decke-flach', 'negroni', 'theke'], ['decke-bar', 'rueckbar-breit', 'fw-a31', 'pf-raum'], ['fenster', 'rm-glaeser', 'tuer-rot']]
    h = ''
    for i, r in enumerate(reihen):
        h += '<div class="auf j19-r" style="--n:%d">%s</div>' % (i, ''.join(
            fig(k, '(max-width:760px) 50vw, 33vw', 'j19-f', 'flex:%.4f 1 0;aspect-ratio:%d/%d' % (mache(k)['w'] / mache(k)['h'], mache(k)['w'], mache(k)['h'])) for k in r))
    return sek(kopf() + '<div class="j19">%s</div>' % h)


@v('Die Fuge in Gold')
def v20():
    # Erst zieht sich ein goldenes Gitter auf, dann steigen die acht Bilder in ihre Felder. Zwei grosse Felder, sechs kleinere.
    ks = [('decke-flach', 'a'), ('negroni', 'b'), ('theke', 'c'), ('decke-bar', 'd'), ('rueckbar-breit', 'e'), ('fenster', 'f'), ('tuer-rot', 'g'), ('fw-a31', 'h')]
    h = ''.join(fig(k, '(max-width:760px) 50vw, 33vw', 'f20-f', 'grid-area:%s;--n:%d' % (a, n)) for n, (k, a) in enumerate(ks))
    return sek(kopf() + '<div class="auf f20">%s<i class="f20-h"></i><i class="f20-v"></i></div>' % h)


assert len(V) == N


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
