# Walk on the Wild Side · Haus-Seite, Abschnitt «Der Raum»: sechs Ideen ohne Bildwand (31.10.2026).
# Robert: «Ich mag das nicht, wenn das so zuplakatiert ist mit solchen riesigen Bildern … elegant und luxuriös».
# Keine neuen Raumfotos (es gibt keine unbenutzten mehr), höchstens kleine Ausschnitte der sechs Fotos, die heute schon im Abschnitt stehen.
# Titel und Bildzeilen Wort für Wort aus unter.py. Aufruf: python3 _varianten/raum-ideen/bau.py → 00 … 06.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/raum-ideen'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

RAUM = [('decke-bar', 'Decke', 'Die Decke: ein Gewölbe als Druck über dem ganzen Raum, blau und silbern angeleuchtet.'),
        ('negroni', 'Schrift', 'NEGRONI in Glühbirnen über der Vitrine. Der Schriftzug sagt, was hier jeden Abend gerührt wird.'),
        ('theke', 'Theke', 'Die Theke mit dem gelben Licht unter der Kante. Hier wird gefragt, was du magst.'),
        ('rueckbar-breit', 'Rückbar', 'Die Rückbar: Flaschen, die man nicht in jedem Laden findet, und eine beleuchtete Vitrine.'),
        ('fenster', 'Fenster', 'Von der Strasse aus sieht man die Rückbar durchs Fenster, oben spiegelt sich die Decke.'),
        ('tuer-rot', 'Tür', 'Durch die Tür: der rote Boden, links die Theke, hinten die Stufen hinauf zur Empore.')]
CAP = {k: t for k, _, t in RAUM}
WORT = {k: w for k, w, _ in RAUM}
_q = open('unter.py').read()
for _, _, t in RAUM:
    assert t in _q, 'Text weicht von der Seite ab: ' + t
assert "h2(['Mit Stil,', 'ganz entspannt.'])" in _q
assert 'Haasemannstraße 13' in _q


def kopf(cls=''):
    return '<div class="ri-kopf %s">%s%s</div>' % (cls, B.kz('Der Raum', 'Fünf Blicke', 0), B.h2(['Mit Stil,', 'ganz entspannt.']))


def sek(inner, cls=''):
    return '<section class="kap auf ri %s" id="raum"><div class="innen">%s</div></section>' % (cls, inner)


def bild(k, sizes, stil=''):
    return '<figure class="ri-f" style="--lq:url(%s);%s">%s</figure>' % (mache(k)['lq'], stil, B.img_tag(k, sizes))


V = []


def v(name):
    def d(f):
        V.append((name, f))
        return f
    return d


# ---------------------------------------------------------------- 1 Der Grundriss
def grundriss():
    # Skizze nach den Fotos und der Bildzeile «Durch die Tür: der rote Boden, links die Theke, hinten die Stufen hinauf zur Empore».
    # Kein vermessener Plan. Je Teil eine Gruppe, die beim passenden Satz aufleuchtet.
    t = lambda x, y, s, a='start': '<text x="%d" y="%d" text-anchor="%s">%s</text>' % (x, y, a, E(s))
    teile = [
        # 0 Decke: Gewölbe-Bögen über dem ganzen Raum
        '<path d="M70 300 Q310 150 550 300 M70 250 Q310 100 550 250 M70 200 Q310 50 550 200" class="gr-l gr-fein"/>' + t(310, 92, 'Gewölbe', 'middle'),
        # 1 Schrift: NEGRONI über der Vitrine an der linken Wand
        '<rect x="44" y="150" width="12" height="96" class="gr-l"/><path d="M62 160 V236" class="gr-l gr-punkte"/>' + t(70, 146, 'NEGRONI'),
        # 2 Theke: lange Theke links, die Lichtkante darunter
        '<rect x="110" y="140" width="40" height="190" rx="3" class="gr-l"/><path d="M156 146 V324" class="gr-l gr-licht"/>' + t(166, 240, 'Theke'),
        # 3 Rückbar: Regale an der linken Wand
        '<path d="M40 130 V340 M40 150 H56 M40 180 H56 M40 210 H56 M40 240 H56 M40 270 H56 M40 300 H56 M40 330 H56" class="gr-l"/>' + t(28, 360, 'Rückbar'),
        # 4 Fenster: zur Strasse, vorn links
        '<path d="M30 392 H180" class="gr-l gr-fenster"/>' + t(105, 414, 'Fenster', 'middle'),
        # 5 Tür: vorn rechts, roter Boden, Stufen hinten hinauf zur Empore
        '<path d="M380 392 H440" class="gr-l gr-tuer"/><path d="M380 392 A60 60 0 0 1 440 332" class="gr-l gr-fein"/>'
        '<rect x="300" y="290" width="200" height="100" class="gr-boden"/>'
        '<path d="M380 120 H560 M380 108 H560 M380 96 H560 M380 84 H560" class="gr-l"/><rect x="380" y="30" width="180" height="50" class="gr-l gr-fein"/>'
        + t(410, 414, 'Tür', 'middle') + t(470, 60, 'Empore', 'middle'),
    ]
    rahmen = '<path d="M30 30 H590 V392 H440 M380 392 H180 M30 392 V30" class="gr-wand"/>'
    gs = ''.join('<g class="gr-g" data-z="%d">%s</g>' % (i, s) for i, s in enumerate(teile))
    return '<svg class="gr-svg" viewBox="0 0 620 430" role="img" aria-label="Skizze des Raums: Tür, roter Boden, Theke, Rückbar, Fenster, Stufen zur Empore, darüber das Gewölbe">%s%s</svg>' % (rahmen, gs)


@v('Der Grundriss')
def v01():
    # Links bleibt die Skizze im Rahmen stehen, rechts laufen die sechs Sätze. Der Satz in der Mitte des Schirms lässt seinen Teil der Skizze aufleuchten.
    schritte = ''.join('<div class="gr-s" data-schritt="%d"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (i, E(w), E(t)) for i, (_, w, t) in enumerate(RAUM))
    return sek('<div class="gr" data-wandern><div class="gr-links"><div class="gr-tafel auf">%s<p class="gr-fuss">Haasemannstraße 13 · Skizze, nicht massstäblich</p></div></div>'
               '<div class="gr-rechts">%s%s</div></div>' % (grundriss(), kopf(), schritte), 'gr-sek')


# ---------------------------------------------------------------- 2 Das Etikett
@v('Das Etikett')
def v02():
    # Der Raum als Etikett, wie bei einer guten Flasche: cremefarbenes Papier, doppelte schwarze Linie wie beim Falstaff-Siegel, ein roter Strich.
    zeilen = ''.join('<div class="et-z" style="--n:%d"><span class="et-w titel">%s</span><p>%s</p></div>' % (i, E(w), E(t)) for i, (_, w, t) in enumerate(RAUM))
    et = ('<div class="et auf"><div class="et-innen">'
          '<p class="et-oben">Walk on the Wild Side · Hannover‑Linden</p>'
          '<p class="et-raum">Der Raum</p><h2 class="titel et-t">Mit Stil,<br>ganz entspannt.</h2><i class="et-strich"></i>'
          '<div class="et-zeilen">%s</div>'
          '<p class="et-unten">Haasemannstraße 13 · Seit 2018</p></div></div>') % zeilen
    return sek('<div class="ri-mitte">%s</div>%s' % (B.kz('Der Raum', 'Fünf Blicke', 0), et), 'et-sek')


# ---------------------------------------------------------------- 3 Die Leuchtschrift
MUSTER = {'N': ['10001', '11001', '11001', '10101', '10011', '10011', '10001'],
          'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
          'G': ['01110', '10001', '10000', '10111', '10001', '10001', '01110'],
          'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
          'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
          'I': ['111', '010', '010', '010', '010', '010', '111']}


def leuchtschrift(wort='NEGRONI'):
    x0, aus, an = 1.0, '', ''
    for n, ch in enumerate(wort):
        m = MUSTER[ch]
        punkte = [(x0 + c, 1.0 + r) for r, z in enumerate(m) for c, b in enumerate(z) if b == '1']
        aus += ''.join('<circle cx="%.1f" cy="%.1f" r=".34"/>' % p for p in punkte)
        an += '<g class="ls-b" style="--n:%d">%s</g>' % (n, ''.join('<circle cx="%.1f" cy="%.1f" r=".95" class="ls-h"/><circle cx="%.1f" cy="%.1f" r=".34" class="ls-k"/>' % (p + p) for p in punkte))
        x0 += len(m[0]) + 1.4
    w = x0 - 1.4 + 1.0
    return ('<svg class="ls-svg" viewBox="0 0 %.1f 9" role="img" aria-label="NEGRONI in Glühbirnen">'
            '<defs><radialGradient id="ls-g"><stop offset="0" stop-color="#FFE7A8" stop-opacity=".55"/><stop offset="1" stop-color="#FFB547" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="ls-k"><stop offset="0" stop-color="#FFF6DD"/><stop offset=".6" stop-color="#FFD683"/><stop offset="1" stop-color="#E9A43C"/></radialGradient></defs>'
            '<g class="ls-aus">%s</g>%s</svg>') % (w, aus, an)


@v('Die Leuchtschrift')
def v03():
    # Der Schriftzug aus der Bar als einziger Blickfang, Buchstabe für Buchstabe gehen die Birnen an. Darunter die Sätze zum Raum in zwei Spalten.
    zl = ''.join('<div class="ls-z" style="--n:%d"><span class="etikett">%s</span><p class="text">%s</p></div>' % (i, E(w), E(t)) for i, (_, w, t) in enumerate(RAUM))
    return sek('<div class="ri-mitte">%s</div><div class="ls-schild auf">%s</div><div class="ls-zeilen auf">%s</div>' % (kopf('ri-mitte'), leuchtschrift(), zl), 'ls-sek')


# ---------------------------------------------------------------- 4 Drei Details
@v('Drei Details')
def v04():
    # Statt ganzer Raumbilder drei enge Ausschnitte in kleinen Rahmen mit Passepartout, viel dunkle Fläche drumherum, wie Stücke in einer Vitrine.
    det = [('negroni', '40% 34%', 2.3), ('theke', '68% 80%', 2.1), ('tuer-rot', '58% 84%', 2.0)]
    h = ''.join('<div class="dt-s" style="--n:%d"><div class="dt-rahmen"><div class="dt-fenster">%s</div></div><span class="etikett">%s</span><p class="text">%s</p></div>' % (
        i, bild(k, '(max-width:760px) 90vw, 640px', '--o:%s;--z:%s' % (o, z)), E(WORT[k]), E(CAP[k])) for i, (k, o, z) in enumerate(det))
    return sek('%s<div class="dt auf">%s</div>' % (kopf('ri-mitte'), h), 'dt-sek')


# ---------------------------------------------------------------- 5 Die Lichtkante
@v('Die Lichtkante')
def v05():
    # Nur Schrift auf Dunkel. In der Mitte des Schirms liegt eine gelbe Lichtkante wie unter der Theke; der Satz, der darüber steht, leuchtet auf.
    s = ''.join('<div class="lk-s" data-schritt="%d"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (i, E(w), E(t)) for i, (_, w, t) in enumerate(RAUM))
    return sek('%s<div class="lk" data-wandern><div class="lk-kante"><i></i></div>%s</div>' % (kopf(), s), 'lk-sek')


# ---------------------------------------------------------------- 6 Ein Weg durch die Tür
@v('Ein Weg durch die Tür')
def v06():
    # Ein einziges kleines Bild im Format eines Abzugs bleibt stehen. Mit jedem Satz steigt das nächste Foto im Rahmen von unten auf: Tür, Theke, Schrift, Rückbar, Decke, Fenster.
    weg = ['tuer-rot', 'theke', 'negroni', 'rueckbar-breit', 'decke-bar', 'fenster']
    bilder_ = ''.join('<div class="wg-b" data-z="%d">%s</div>' % (i, bild(k, '(max-width:760px) 60vw, 420px')) for i, k in enumerate(weg))
    s = ''.join('<div class="wg-s" data-schritt="%d"><span class="etikett">%s</span><p class="titel">%s</p></div>' % (i, E(WORT[k]), E(CAP[k])) for i, k in enumerate(weg))
    return sek('<div class="wg" data-wandern><div class="wg-links"><div class="wg-abzug auf"><div class="wg-fenster">%s</div></div></div><div class="wg-rechts">%s%s</div></div>' % (bilder_, kopf(), s), 'wg-sek')


N = len(V)


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
