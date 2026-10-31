# Walk on the Wild Side · Seite «Das Haus», Kopf «Unter dieser Decke.» in 15 Fassungen (31.10.2026, Wunsch Robert: «15 alternative Visualisierungen für den Hero»).
# Titel und Satz bleiben wörtlich. Je Fassung eigener Aufbau und eigene Bewegung, nur transform und opacity, Text immer auf deckendem Grund.
# Nur die hochaufgelösten Deckenfotos (decke-hoch, decke-raum 2400 px), das 1200er-Foto von heute nur dort, wo es klein steht.
# Wechsel mit ← → (varianten-nav.js). Aufruf: python3 _varianten/haus-hero-15/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, LOGO, mache, img_tag

ORD = '_varianten/haus-hero-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('hh.css', 'hh.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('haus.html').read()
a = basis.index('<header class="sk auf" id="auftakt">')
b = basis.index('</header>', a) + len('</header>')
HEUTE = basis[a:b]

T = ['Unter dieser', 'Decke.']
SATZ = 'Eine kleine Bar an der Ecke Haasemannstraße, mit einem Gewölbe über der Theke, Glühbirnen über der Vitrine und zwei Leuten, die sie seit 2023 führen.'
LINIE = '<svg class="hh-linie" aria-hidden="true"><rect x="10" y="10" rx="8" ry="8" pathLength="100"/></svg>'


def foto(k, cls='', sizes='100vw', pos='50% 50%', stil='', sofort=True):
    return '<figure class="foto hh-f %s" style="--lq:url(%s);%s">%s</figure>' % (
        cls, mache(k)['lq'], stil, img_tag(k, sizes, sofort, extra=' style="object-position:%s"' % pos))


def titel(cls='', i0=1, zeilen=None):
    return '<h1 class="titel hh-t %s">%s</h1>' % (cls, bau.zl(zeilen or T, i0=i0))


def satz(cls='', i=3):
    return '<p class="text sw hh-s %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def kopf(n, inner):
    return '<header class="hh auf v%02d" id="auftakt" data-v="%d">%s</header>' % (n, n, inner)


V = []

# 01 Der Blick geht hoch: das hohe Foto füllt den Schirm und wandert von der Theke hinauf ins Gewölbe, wie wenn man hereinkommt und hochschaut.
#    Titel und Satz stehen unten links auf einer deckenden Nachtfläche.
V.append(('Der Blick geht hoch', lambda n: kopf(n, foto('decke-hoch', 'v01-b', '100vw', '50% 0%') +
    '<div class="v01-tafel"><div class="v01-in">%s%s</div></div>' % (titel(), satz()))))

# 02 Hochkant daneben: links die Nacht mit Titel und Satz, rechts das Gewölbe hochkant über die volle Höhe; das Bild steigt aus dem Boden.
V.append(('Hochkant daneben', lambda n: kopf(n, '<div class="v02-g"><div class="v02-l">%s%s</div><div class="v02-r">%s</div></div>' % (
    titel(), satz(), foto('decke-hoch', 'v02-b', '(max-width:760px) 100vw, 54vw', '50% 18%')))))

# 03 Die Decke senkt sich: das Gewölbe als breites Band oben, es senkt sich von oben herab an seinen Platz; darunter der Titel mittig und gross.
V.append(('Die Decke senkt sich', lambda n: kopf(n, '<div class="v03-band">%s</div><div class="v03-u">%s%s</div>' % (
    foto('decke-hoch', 'v03-b', '100vw', '50% 14%'), titel(), satz()))))

# 04 Drei Felder: drei Blicke ins Gewölbe nebeneinander, sie steigen nacheinander auf; darunter quer über alle drei der Titel, daneben der Satz.
V.append(('Drei Felder', lambda n: kopf(n, '<div class="v04-r">%s%s%s</div><div class="v04-u innen">%s%s</div>' % (
    foto('decke-raum', 'v04-b', '(max-width:760px) 100vw, 34vw', '30% 10%', '--n:0'),
    foto('decke-hoch', 'v04-b', '(max-width:760px) 100vw, 34vw', '50% 12%', '--n:1'),
    foto('decke-bar', 'v04-b', '(max-width:760px) 100vw, 34vw', '50% 20%', '--n:2'),
    titel(), satz()))))

# 05 Von der Strasse: das Foto durchs Fenster der Bar, in dem sich die Decke spiegelt. Es kommt klein wie von der anderen Strassenseite und wächst heran.
V.append(('Von der Strasse', lambda n: kopf(n, '<div class="v05-g innen"><div class="v05-l">%s%s</div><div class="v05-r">%s</div></div>' % (
    titel(), satz(), foto('fenster', 'v05-b', '(max-width:760px) 100vw, 40vw', '50% 40%')))))

# 06 Der Titel über alles: «Unter dieser Decke.» in einer Zeile über die ganze Breite, darunter das Gewölbe als breites Band, das beim Scrollen langsam herankommt.
V.append(('Der Titel über alles', lambda n: kopf(n, '<div class="v06-o innen">%s%s</div><div class="v06-band">%s</div>' % (
    titel('v06-t', zeilen=['Unter dieser Decke.']), satz('v06-s'), foto('decke-hoch', 'v06-b', '100vw', '50% 16%')))))

# 07 Die Kuppel: das Gewölbe rund ausgeschnitten wie der Blick in eine Kuppel, es dreht sich ganz langsam; links der Titel.
V.append(('Die Kuppel', lambda n: kopf(n, '<div class="v07-g innen"><div class="v07-l">%s%s</div><div class="v07-r"><div class="v07-rund">%s</div></div></div>' % (
    titel(), satz(), foto('decke-hoch', 'v07-b', '(max-width:760px) 120vw, 60vw', '50% 18%')))))

# 08 Der Bogen: das Gewölbe in einem hohen Rundbogen in der Mitte, er wächst aus dem Boden; der Titel teilt sich links und rechts davon.
V.append(('Der Bogen', lambda n: kopf(n, '<div class="v08-g innen"><div class="v08-l">%s</div><div class="v08-m">%s</div><div class="v08-rr">%s%s</div></div>' % (
    titel('', 1, ['Unter', 'dieser']), foto('decke-bar', 'v08-b', '(max-width:760px) 70vw, 30vw', '50% 26%'),
    titel('', 3, ['Decke.']), satz('', 4)))))

# 09 Zwischen Decke und Theke: oben das Gewölbe, unten die Theke im gelben Licht; beide fahren aufeinander zu, dazwischen auf Nacht der Titel.
V.append(('Zwischen Decke und Theke', lambda n: kopf(n, '<div class="v09-o">%s</div><div class="v09-m innen">%s%s</div><div class="v09-u">%s</div>' % (
    foto('decke-hoch', 'v09-b', '100vw', '50% 12%'), titel(), satz(), foto('decke-hoch', 'v09-b', '100vw', '50% 82%')))))

# 10 Hinunter zur Bar: der Kopf bleibt kurz stehen; beim Scrollen fährt das Bild rechts vom Gewölbe hinunter bis zur Theke, links stehen Titel und Satz.
V.append(('Hinunter zur Bar', lambda n: kopf(n, '<div class="v10-steh"><div class="v10-g"><div class="v10-l">%s%s<p class="v10-weiter sw" style="--i:4">Scrollen, hinunter zur Theke</p></div><div class="v10-r">%s</div></div></div>' % (
    titel(), satz(), foto('decke-hoch', 'v10-b', '(max-width:760px) 100vw, 56vw', '50% 0%')))))

# 11 Das Eckschild: das Gewölbe über den ganzen Schirm, davor das Schild der Bar, deckend in Nacht, die Goldlinie zieht sich einmal herum.
V.append(('Das Eckschild', lambda n: kopf(n, foto('decke-raum', 'v11-b', '100vw', '50% 12%') +
    '<div class="v11-schild">%s<span class="logo v11-logo">%s</span>%s%s</div>' % (LINIE, LOGO, titel(), satz()))))

# 12 Die Birnen gehen an: links schmal und hoch die Decke über dem NEGRONI-Schriftzug, rechts eine Reihe Glühbirnen, die eine nach der anderen angeht, dann der Titel.
V.append(('Die Birnen gehen an', lambda n: kopf(n, '<div class="v12-g"><div class="v12-l">%s</div><div class="v12-r"><div class="v12-birnen" aria-hidden="true">%s</div>%s%s</div></div>' % (
    foto('decke-bar', 'v12-b', '(max-width:760px) 100vw, 38vw', '50% 40%'),
    ''.join('<i style="--n:%d"></i>' % j for j in range(18)), titel(), satz()))))

# 13 Fliese für Fliese: das Gewölbe in achtzehn Fliesen, sie drehen sich in einer Welle von links oben nach rechts unten zum ganzen Bild; darunter Titel und Satz.
def v13(n):
    d = mache('decke-hoch')
    srcset = ', '.join('assets/bild/%s?v=%s %dw' % (f, bau.V, w) for w, f in d['stufen'])
    sp, ze = 6, 3
    fl = ''.join('<div class="v13-fl" style="--c:%d;--r:%d;--n:%d"><img src="assets/bild/%s?v=%s" srcset="%s" sizes="100vw" alt="" decoding="async"></div>' % (
        c, r, c + r, d['stufen'][-1][1], bau.V, srcset) for r in range(ze) for c in range(sp))
    return kopf(n, '<div class="v13-wand" role="img" aria-label="%s">%s</div><div class="v13-u innen">%s%s</div>' % (E(d['alt']), fl, titel(), satz()))
V.append(('Fliese für Fliese', v13))

# 14 In Creme: der helle Kopf wie das Papier der Bar, Titel dunkel, rechts das Gewölbe als grosser Abzug, der hochschwebt.
V.append(('In Creme', lambda n: kopf(n, '<div class="v14-g innen"><div class="v14-l"><span class="logo v14-logo">%s</span>%s%s</div><div class="v14-r">%s</div></div>' % (
    LOGO, titel(), satz(), foto('decke-hoch', 'v14-b', '(max-width:760px) 100vw, 50vw', '50% 22%')))))

# 15 Der Schwenk: oben auf Nacht Titel und Satz nebeneinander, darunter das Gewölbe als Panorama, das beim Scrollen von links nach rechts unter der Decke entlangfährt.
V.append(('Der Schwenk', lambda n: kopf(n, '<div class="v15-o innen">%s%s</div><div class="v15-band">%s</div>' % (
    titel(), satz(), foto('decke-raum', 'v15-b', '130vw', '0% 10%')))))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/hh.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/hh.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
