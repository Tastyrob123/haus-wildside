# Walk on the Wild Side · Feiern-Seite (tafel.html), Abschnitt «Anfragen», Team-Bild «Lasst uns euren Abend gemeinsam gestalten.»: 15 Darstellungen (30.10.2026).
# Robert: «gib mir 15 visuelle darstellungsmöglichkeiten von dem abschnitt». 00 = heutiger Stand.
# Nur der Team-Block wird getauscht, Formular darunter bleibt. Texte Wort für Wort aus unter.py, nur das Team-Foto des Hauses (an-team).
# Je Fassung eine eigene Darstellung und eine eigene Bewegung; nur transform und opacity, ein Scroll-Takt in v.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/team-15/bau.py → 00 … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/team-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

ET = 'Ansprechpartner · Momo und Derya'
Z = ['Lasst uns euren Abend', 'gemeinsam gestalten.']
_q = open('unter.py').read()
for t in [ET] + Z:
    assert t in _q, 'Text weicht von der Seite ab: ' + t
LQ = mache('an-team')['lq']


def bild(sizes='(max-width:900px) 100vw, 1240px', cls='t-bild', pos='50% 30%'):
    return '<figure class="%s" style="--lq:url(%s)">%s</figure>' % (cls, LQ, B.img_tag('an-team', sizes, extra=' style="object-position:%s"' % pos))


def et(cls=''):
    return '<span class="etikett %s">%s</span>' % (cls, E(ET))


def titel(cls='', zeilen=Z):
    return '<p class="titel t-titel %s">%s</p>' % (cls, B.zl(zeilen))


def blk(n, inner, cls='', p=False):
    return '<div class="t-blk auf t%02d %s"%s>%s</div>' % (n, cls, ' data-p' if p else '', inner)


V = []

# 01 · Der Satz über die ganze Breite: der Titel gross in einer Zeile oben, das Bild darunter in voller Breite; das Bild setzt sich aus leichter Vergrösserung.
V.append(('Der Satz über die ganze Breite', lambda n: blk(n, '%s%s%s' % (et(), titel('', [' '.join(Z)]), bild()))))

# 02 · Drei Nischen: das Bild in drei Felder geteilt, jeder Mensch in seinem eigenen; die Felder steigen nacheinander aus verschiedenen Tiefen.
def v02(n):
    teile = ''.join('<div class="t2-f" style="--n:%d"><div class="t2-in" style="--x:%d">%s</div></div>' % (j, j, bild(cls='t-bild')) for j in range(3))
    return blk(n, '<div class="t2-kopf">%s%s</div><div class="t2-reihe">%s</div>' % (et(), titel(), teile))
V.append(('Drei Nischen', v02))

# 03 · Der Abzug: das Foto mit hellem Rand wie ein Abzug, erst schräg, dann richtet es sich gerade; links der Satz.
V.append(('Der Abzug', lambda n: blk(n, '<div class="t3-text">%s%s</div><div class="t3-abzug">%s</div>' % (et(), titel(), bild('(max-width:900px) 100vw, 760px')))))

# 04 · Auf hellem Papier: eine Creme-Tafel, darauf der Satz in Dunkel, das Bild rechts kommt nach der Tafel hoch.
V.append(('Auf hellem Papier', lambda n: blk(n, '<div class="t4-tafel">%s%s</div>%s' % (et(), titel(), bild('(max-width:900px) 100vw, 820px')))))

# 05 · Das Bild zieht sich auf: beim Scrollen wächst das Bild aus der Mitte zur vollen Breite, der Satz steht darunter.
V.append(('Das Bild zieht sich auf', lambda n: blk(n, '<div class="t5-halt">%s</div><div class="t5-unter">%s%s</div>' % (bild(), et(), titel()), p=True)))

# 06 · Zeilen um das Bild: die erste Zeile über dem Bild links, die zweite darunter rechts; erst das Bild, dann die Zeilen.
V.append(('Zeilen um das Bild', lambda n: blk(n, '%s<p class="titel t-titel t6-o">%s</p>%s<p class="titel t-titel t6-u">%s</p>' % (
    et(), B.zl([Z[0]]), bild(), B.zl([Z[1]], i0=1)))))

# 07 · Fenster mit Tiefe: der Rahmen steht, das Foto darin läuft beim Scrollen langsamer mit; der Satz in einer schmalen Spalte rechts.
V.append(('Fenster mit Tiefe', lambda n: blk(n, '<div class="t7-rahmen">%s</div><div class="t7-text">%s%s</div>' % (bild(), et(), titel()), p=True)))

# 08 · Die Karte: das Bild gross, unten rechts eine helle Karte mit dem Satz, die mit einem Federn nachkommt.
V.append(('Die Karte', lambda n: blk(n, '%s<div class="t8-karte">%s%s</div>' % (bild(), et(), titel()))))

# 09 · Aus dem Detail: das Bild beginnt nah am NEGRONI-Schriftzug und fährt beim Scrollen zurück, bis das Team dasteht.
V.append(('Aus dem Detail', lambda n: blk(n, '<div class="t9-rahmen">%s</div><div class="t9-unter">%s%s</div>' % (bild(), et(), titel()), p=True)))

# 10 · Breitwand: oben und unten schwarze Balken wie im Kino, sie ziehen sich zurück und geben das ganze Bild frei; der Satz mittig darunter.
V.append(('Breitwand', lambda n: blk(n, '<div class="t10-kino">%s<i class="t10-o"></i><i class="t10-u"></i></div><div class="t10-unter">%s%s</div>' % (bild(), et(), titel()))))

# 11 · Die Unterschrift: der Satz mittig und gross, darunter zieht sich eine Goldlinie auf, dann steigt das Bild.
V.append(('Die Unterschrift', lambda n: blk(n, '<div class="t11-kopf">%s%s<i class="t11-linie"></i></div>%s' % (et(), titel(), bild()))))

# 12 · Gedreht in den Raum: das Bild steht schräg im Raum und dreht sich beim Scrollen nach vorn; links der Satz.
V.append(('Gedreht in den Raum', lambda n: blk(n, '<div class="t12-text">%s%s</div><div class="t12-raum">%s</div>' % (et(), titel(), bild('(max-width:900px) 100vw, 820px')), p=True)))

# 13 · Die Tafel am Bildrand: eine dunkle Tafel mit dem Satz sitzt an der linken unteren Ecke des Bildes und läuft beim Scrollen schneller als das Bild.
V.append(('Die Tafel am Bildrand', lambda n: blk(n, '<div class="t13-b">%s</div><div class="t13-tafel">%s%s</div>' % (bild('(max-width:900px) 100vw, 1000px'), et(), titel()), p=True)))

# 14 · Treppe aus Zeilen: der Satz in vier Stufen, jede weiter eingerückt; das Bild steht am Fuss der Treppe.
def v14(n):
    stufen = ['Lasst uns', 'euren Abend', 'gemeinsam', 'gestalten.']
    st = ''.join('<span class="t14-s" style="--n:%d">%s</span>' % (j, E(s)) for j, s in enumerate(stufen))
    return blk(n, '<div class="t14-kopf">%s<p class="titel t-titel t14-treppe">%s</p></div>%s' % (et(), st, bild('(max-width:900px) 100vw, 900px')))
V.append(('Treppe aus Zeilen', v14))

# 15 · Das Bild stellt sich auf: es liegt erst flach wie auf dem Tresen und richtet sich auf; der Satz steht davor.
V.append(('Das Bild stellt sich auf', lambda n: blk(n, '<div class="t15-kopf">%s%s</div><div class="t15-raum">%s</div>' % (et(), titel(), bild()))))

assert len(V) == 15


def seite(n):
    h = unter.tafel()
    if n:
        a = h.find('<div class="fr-team')
        b = h.find('<div class="zwei" style="margin-top:clamp(40px,5vw,72px)', a)
        assert a > 0 and b > a
        h = h[:a] + V[n - 1][1](n) + h[b:]
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
