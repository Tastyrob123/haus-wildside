# Walk on the Wild Side · Haus-Seite, Abschnitt «Der Raum»: fünf Fassungen in der Sprache der übrigen Haus-Seite (31.10.2026).
# Robert zu raum-seite: «Wir sind alle scheiße, bitte. Orientiere dich am Rest der Seite.» Also Steckbrief-Tafel wie Derya und Momo, Bögen wie bei den Bewertungen.
# Nur Fotos, die ausschliesslich auf der Haus-Seite stehen (theke, rueckbar-breit), in normaler Grösse.
# Titel und Bildzeilen Wort für Wort aus unter.py. Aufruf: python3 _varianten/raum-seite/bau.py → 00 … 06.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/raum-seite'
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


def zeilen(ks):
    return '<div class="sb-weg rs-weg">%s</div>' % ''.join('<div><span>%s</span><p>%s</p></div>' % (E(WORT[k]), E(CAP[k])) for k in ks)


ALLE = [k for k, _, _ in RAUM]


def steck(k, name, etikett, ks, rechts, pos='50% 50%'):
    return '<div class="auf sb-zeile%s" data-sb>%s<div class="platte sb-platte"><h3 class="titel sb-name">%s</h3><span class="etikett">%s</span>%s</div></div>' % (
        ' sb-r' if rechts else '', B.bild(k, 'sb-bild', '(max-width:760px) 100vw, 60vw', extra=' style="object-position:%s"' % pos), E(name), E(etikett), zeilen(ks))


def kopf_alt():
    return B.kz('Der Raum', 'Fünf Blicke', 0) + B.h2(['Mit Stil,', 'ganz entspannt.'])


def sek(inner, cls=''):
    return '<section class="kap auf %s" id="raum"><div class="innen">%s</div></section>' % (cls, inner)


@v('Steckbrief des Raums')
def v01():
    # Wie Derya und Momo: ein Bild, die Tafel schiebt sich über die Kante, darin die sechs Teile des Raums als Zeilen.
    return sek(kopf_alt() + '<div style="margin-top:34px">%s</div>' % steck('rueckbar-breit', 'Der Raum', 'Haasemannstraße 13', ALLE, False))


@v('Steckbrief, gespiegelt')
def v02():
    # Dieselbe Sprache, Tafel links, rechts die Theke mit dem gelben Licht.
    return sek(kopf_alt() + '<div style="margin-top:34px">%s</div>' % steck('theke', 'Der Raum', 'Haasemannstraße 13', ALLE, True, '50% 62%'))


@v('Zwei Steckbriefe')
def v03():
    # Zwei Tafeln wie bei Derya und Momo: die Bar (Theke, Schrift, Rückbar) und der Raum drumherum (Decke, Fenster, Tür).
    return sek(kopf_alt() + '<div style="margin-top:34px">%s%s</div>' % (
        steck('rueckbar-breit', 'Die Bar', 'Theke · Schrift · Rückbar', ['theke', 'negroni', 'rueckbar-breit'], False),
        steck('theke', 'Der Raum', 'Decke · Fenster · Tür', ['decke-bar', 'fenster', 'tuer-rot'], True, '50% 40%')))


def bogen(k, wort, ks, n, pos='50% 50%'):
    return ('<div class="rs-b" style="--n:%d"><div class="et9-et rs-et"><div class="et9-in rs-in">'
            '<div class="rs-foto">%s</div><span class="etikett">%s</span><i></i>%s</div></div></div>') % (
        n, B.bild(k, 'rs-bild', '(max-width:760px) 90vw, 45vw', extra=' style="object-position:%s"' % pos), E(wort), zeilen(ks))


@v('Zwei Bögen')
def v04():
    # Wie die Etiketten bei «Was andere sagen»: zwei Bögen mit doppelter Linie, oben das Foto im Bogen, darunter je drei Zeilen.
    return sek(kopf_alt() + '<div class="rs-reihe">%s%s</div>' % (
        bogen('rueckbar-breit', 'Die Bar', ['theke', 'negroni', 'rueckbar-breit'], 0),
        bogen('theke', 'Der Raum', ['decke-bar', 'fenster', 'tuer-rot'], 1, '50% 45%')), 'rs-sek')


@v('Bogen und Tafel')
def v05():
    # Links ein Bogen mit der Theke, rechts die Tafel mit allen sechs Zeilen, beide gleich hoch.
    b = '<div class="rs-b" style="--n:0"><div class="et9-et rs-et"><div class="et9-in rs-in rs-voll"><div class="rs-foto">%s</div></div></div></div>' % B.bild(
        'theke', 'rs-bild', '(max-width:760px) 90vw, 45vw', extra=' style="object-position:50% 60%"')
    t = '<div class="rs-b" style="--n:1"><div class="platte rs-tafel"><h3 class="titel sb-name">Der Raum</h3><span class="etikett">Haasemannstraße 13</span>%s</div></div>' % zeilen(ALLE)
    return sek(kopf_alt() + '<div class="rs-reihe rs-zwei">%s%s</div>' % (b, t), 'rs-sek')


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
