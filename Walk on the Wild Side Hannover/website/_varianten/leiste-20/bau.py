# Walk on the Wild Side · Kopfleiste: 20 Fassungen (31.10.2026).
# Robert: «Gib mir 20 alternative Visualisierungsmöglichkeiten für diese Leiste da oben.»
# Grundlage: Drinks-Seite wie gebaut, nur die Leiste wird getauscht. Wegfahren beim Scrollen (wild.js, id="leiste", .weg) bleibt.
# Texte nur aus bau.py (NAV, HAUS, Fusszeile). Aufruf: python3 _varianten/leiste-20/bau.py → 00 … 20.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter

E = html.escape
ORD = '_varianten/leiste-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'nav.js', 'v.js'))))
AKTIV = 'drinks.html'
UNTERZEILE = 'Nachbarschafts-Mixology-Bar · Hannover-Linden'   # steht so in der Fusszeile
assert UNTERZEILE in open('bau.py').read()


def links(cls=''):
    return ''.join('<a href="%s" class="%s%s">%s</a>' % (h, cls, ' aktiv' if h == AKTIV else '', E(t)) for h, t in B.NAV)


def logo(cls='logo'):
    return '<a class="%s" href="index.html" aria-label="Walk on the Wild Side">%s</a>' % (cls, B.LOGO)


def res(cls='klein'):
    return B.knopf('Reservieren', 'besuch.html#reservieren', cls)


def hülle(n, innen, extra=''):
    return '<div class="leiste lv lv%02d" id="leiste"%s>%s</div>' % (n, extra, innen)


def v01():  # Glühbirnen unter dem aktiven Wort, wie der NEGRONI-Schriftzug
    return hülle(1, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res()))

def v02():  # Die Theke: Holzton, gelbes Licht unter der Kante
    return hülle(2, '<div class="innen">%s<nav>%s</nav>%s</div><i class="lv-licht"></i>' % (logo(), links(), res()))

def v03():  # Logo in der Mitte, Seiten links und rechts
    l = B.NAV
    a = ''.join('<a href="%s"%s>%s</a>' % (h, ' class="aktiv"' if h == AKTIV else '', E(t)) for h, t in l[:2])
    b = ''.join('<a href="%s"%s>%s</a>' % (h, ' class="aktiv"' if h == AKTIV else '', E(t)) for h, t in l[2:])
    return hülle(3, '<div class="innen"><nav class="lv-l">%s</nav>%s<nav class="lv-r">%s</nav>%s</div>' % (a, logo(), b, res()))

def v04():  # Prata statt Grossbuchstaben
    return hülle(4, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res()))

def v05():  # Kapsel, frei unter dem Rand
    return hülle(5, '<div class="lv-kapsel">%s<nav>%s</nav>%s</div>' % (logo(), links(), res()))

def v06():  # Zwei Etagen: oben Adresse, Zeiten, Telefon
    h = B.HAUS
    oben = '<div class="lv-oben"><div class="innen"><span>%s, %s</span><span>%s</span><a href="tel:%s">%s</a></div></div>' % (
        E(h['adresse']), E(h['ort']), E(h['zeit_kurz']), h['tel_href'], E(h['telefon']))
    return hülle(6, oben + '<div class="lv-unten"><div class="innen">%s<nav>%s</nav>%s</div></div>' % (logo(), links(), res()))

def v07():  # Goldrahmen mit Rauten an den Ecken
    return hülle(7, '<div class="innen"><div class="lv-rahmen"><b></b><b></b><b></b><b></b>%s<nav>%s</nav>%s</div></div>' % (logo(), links(), res()))

def v08():  # Unten am Rand
    return hülle(8, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res()))

def v09():  # Creme
    return hülle(9, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res('klein hellk')))

def v10():  # Gewölbe: die Unterkante als Bögen
    return hülle(10, '<div class="innen">%s<nav>%s</nav>%s</div><i class="lv-boegen"></i>' % (logo(), links(), res()))

def v11():  # Ein goldener Schein wandert unter die Maus
    return hülle(11, '<div class="innen">%s<nav><i class="lv-schein"></i>%s</nav>%s</div>' % (logo(), links(), res()))

def v12():  # Das Logo hängt als Schild über die Kante
    return hülle(12, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo('logo lv-schild'), links(), res()))

def v13():  # Spalten mit Goldlinien, wie eine Barkarte
    return hülle(13, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res()))

def v14():  # Zweizeilig: Logo oben in der Mitte, Seiten darunter
    return hülle(14, '<div class="innen">%s<div class="lv-zeile"><nav>%s</nav>%s</div></div>' % (logo(), links(), res()))

def v15():  # Leuchtschrift
    return hülle(15, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res()))

def v16():  # Schmal: nur Schrift, Reservieren als Wort
    return hülle(16, '<div class="innen">%s<nav>%s</nav><a class="lv-wort" href="besuch.html#reservieren">Reservieren<i>%s</i></a></div>' % (logo(), links(), B.PFEIL))

def v17():  # Mit Unterzeile neben dem Logo
    return hülle(17, '<div class="innen"><div class="lv-marke">%s<span>%s</span></div><nav>%s</nav>%s</div>' % (logo(), E(UNTERZEILE).replace(' · ', '<br>'), links(), res()))

def v18():  # Goldleiste
    return hülle(18, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res('klein lv-dunkel')))

def v19():  # Gewölbeblau
    return hülle(19, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res()))

def v20():  # Ein roter Punkt markiert die Seite, Reservieren rot
    return hülle(20, '<div class="innen">%s<nav>%s</nav>%s</div>' % (logo(), links(), res('klein rot')))


V = [('Glühbirnen', v01), ('Die Theke', v02), ('Logo in der Mitte', v03), ('Prata statt Versalien', v04), ('Die Kapsel', v05),
     ('Zwei Etagen', v06), ('Goldrahmen', v07), ('Unten am Rand', v08), ('Creme', v09), ('Das Gewölbe', v10),
     ('Der wandernde Schein', v11), ('Das hängende Schild', v12), ('Spalten wie eine Karte', v13), ('Zweizeilig, mittig', v14), ('Leuchtschrift', v15),
     ('Ganz schmal', v16), ('Mit Unterzeile', v17), ('Goldleiste', v18), ('Gewölbeblau', v19), ('Der rote Punkt', v20)]
N = len(V)
assert N == 20


SEITEN = [('index.html', 'Start'), ('drinks.html', 'Drinks'), ('programm.html', 'Programm'), ('tafel.html', 'Feiern'), ('haus.html', 'Das Haus'), ('besuch.html', 'Besuch')]
import re
LINK = re.compile(r'href="(index|drinks|programm|tafel|haus|besuch)\.html(#[^"]*)?"')


def datei(n, name):
    return '%02d-%s' % (n, name)


def seite(n, name, roh):
    global AKTIV
    AKTIV = name if name != 'index.html' else ''
    h = roh
    alt = B.leiste(AKTIV)
    assert h.count(alt) == 1, name
    if n:
        h = h.replace(alt, V[n - 1][1](), 1)
    h = LINK.sub(lambda m: 'href="%s/%s%s"' % (ORD, datei(n, m.group(1) + '.html'), m.group(2) or ''), h)
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    if n:
        h = h.replace('<body class="', '<body class="mit-lv%02d ' % n, 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s · %s</span><i>← →</i></p>' % (n, N, E(liste[n][1]), E(dict(SEITEN)[name]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;window.VSEITE=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), json.dumps(name), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    roh = {'index.html': B.seite()}
    roh.update(unter.alle())
    for name, _ in SEITEN:
        for n in range(N + 1):
            open(os.path.join(ORD, datei(n, name)), 'w').write(seite(n, name, roh[name]))
    # alte Adressen NN.html zeigen weiter auf die Startseite
    for n in range(N + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=%s">' % datei(n, 'index.html'))
    print('20 Fassungen ×', len(SEITEN), 'Seiten')
