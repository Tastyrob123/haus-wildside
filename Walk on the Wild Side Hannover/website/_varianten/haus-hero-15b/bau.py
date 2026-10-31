# Walk on the Wild Side · Seite «Das Haus», Kopf «Unter dieser Decke.», zweite Runde mit 15 Fassungen (31.10.2026).
# Robert zur ersten Runde: «alle mist. Bilder unscharf, verpixelt und die Hero Ideen müssen außergewöhnlicher sein.»
# Daraus: (1) Kein Foto wird grösser gezeigt als halb so gross wie seine echte Auflösung, ausgeliefert in voller Auflösung (bilder.py).
#         (2) Die Wirkung kommt aus einem Gegenstand des Hauses (Leuchtschrift, Gewölbe, Vitrine, Theke, Ecke, Schild), nicht aus einem grossen Foto.
# Titel und Satz bleiben wörtlich. Nur transform und opacity. Wechsel mit ← →. Aufruf: python3 _varianten/haus-hero-15b/bau.py
import os, sys, json, math
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, LOGO

ORD = '_varianten/haus-hero-15b'
P = ORD + '/bild/'
B = json.load(open(os.path.join(ORD, 'bild', 'bilder.json')))
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('hh2.css', 'hh2.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('haus.html').read()
a = basis.index('<header class="sk auf" id="auftakt">')
b = basis.index('</header>', a) + len('</header>')
HEUTE = basis[a:b]

T = ['Unter dieser', 'Decke.']
SATZ = 'Eine kleine Bar an der Ecke Haasemannstraße, mit einem Gewölbe über der Theke, Glühbirnen über der Vitrine und zwei Leuten, die sie seit 2023 führen.'
LINIE = '<svg class="g-linie" aria-hidden="true"><rect x="10" y="10" rx="8" ry="8" pathLength="100"/></svg>'


def img(k, sizes, cls='', pos='50% 50%', hoch=True):
    d = B[k]
    srcset = ', '.join('%s%s %dw' % (P, f, w) for w, f in d['stufen'])
    return '<img class="%s" src="%s%s" srcset="%s" sizes="%s" alt="%s" width="%d" height="%d" decoding="async"%s style="object-position:%s">' % (
        cls, P, d['stufen'][-1][1], srcset, sizes, E(d['alt']), d['w'], d['h'], ' fetchpriority="high"' if hoch else '', pos)


def bg(k):
    """Hintergrund in halber echter Grösse: ein CSS-Pixel = zwei Bildpunkte, scharf auch am Retina-Schirm."""
    d = B[k]
    return 'background-image:url(%s%s);background-size:%dpx %dpx' % (P, d['stufen'][-1][1], d['w'] // 2, d['h'] // 2)


def bg4(k):
    """Hintergrund in einem Viertel der echten Grösse: am Retina-Schirm zwei Bildpunkte je Bildschirmpunkt, die Handy-Glättung verschwindet."""
    d = B[k]
    return 'background-image:url(%s%s);background-size:%dpx %dpx' % (P, d['stufen'][-1][1], d['w'] // 4, d['h'] // 4)


def titel(cls='', i0=1, zeilen=None, tag='h1'):
    return '<%s class="titel g-t %s">%s</%s>' % (tag, cls, bau.zl(zeilen or T, i0=i0), tag)


def satz(cls='', i=3, text=None):
    return '<p class="text sw g-s %s" style="--i:%d">%s</p>' % (cls, i, text or E(SATZ))


def kopf(n, inner, extra=''):
    return '<header class="g auf w%02d" id="auftakt" data-v="%d"%s>%s</header>' % (n, n, extra, inner)


V = []

# 01 Leuchtschrift: «UNTER DIESER DECKE.» als Schild aus Glühbirnen wie der NEGRONI-Schriftzug über der Vitrine. Die Birnen gehen nacheinander an,
#    zwei flackern nach. Darüber das Gewölbe als schmales Band, darunter der Satz. Die Schrift ist gezeichnet, also immer scharf.
V.append(('Leuchtschrift', lambda n: kopf(n,
    '<div class="w01-decke">%s</div><div class="w01-m innen"><h1 class="w01-h"><span class="nur-lesen">Unter dieser Decke.</span><svg class="w01-svg" aria-hidden="true"></svg></h1>%s</div>' % (
        img('decke-weit', '100vw', 'w01-b', '50% 30%'), satz('w01-s')))))

# 02 Die Rosette: aus dem Gewölbe wird ein Kaleidoskop in zwölf Teilen, wie das Rund eines Kirchenfensters. Die Teile wandern langsam,
#    das Muster verändert sich ständig, jeder Ausschnitt in halber Grösse. Links der Titel.
def w02(n):
    teile = ''.join('<div class="w02-k" style="--j:%d"><div class="w02-bild" style="%s"></div></div>' % (j, bg4('decke-tief')) for j in range(12))
    return kopf(n, '<div class="w02-g innen"><div class="w02-l">%s%s</div><div class="w02-r"><div class="w02-rose" role="img" aria-label="%s">%s</div></div></div>' % (
        titel(), satz(), E(B['decke-tief']['alt']), teile))
V.append(('Die Rosette', w02))

# 03 Kopf in den Nacken: zuerst siehst du nur die Decke, als lägst du auf dem Rücken. Dann kippt sie nach hinten über dich weg,
#    und darunter steht der Titel. Echte Tiefe, eine einzige Bewegung.
V.append(('Kopf in den Nacken', lambda n: kopf(n,
    '<div class="w03-raum"><div class="w03-decke">%s</div></div><div class="w03-u innen">%s%s</div>' % (
        img('decke-weit', '100vw', 'w03-b', '50% 40%'), titel(), satz()))))

# 04 Die Decke rollt aus: das Gewölbe kommt eingerollt von oben und rollt sich Streifen für Streifen herunter wie ein Stoff.
def w04(n):
    st = 16
    s = ''.join('<div class="w04-st" style="--j:%d;%s;background-position:center %.4f%%"></div>' % (j, bg('decke-weit'), j / (st - 1) * 100) for j in range(st))
    return kopf(n, '<div class="w04-rolle" role="img" aria-label="%s" style="--st:%d">%s</div><div class="w04-u innen">%s%s</div>' % (
        E(B['decke-weit']['alt']), st, s, titel(), satz()))
V.append(('Die Decke rollt aus', w04))

# 05 Das Licht der Theke: oben das Gewölbe, darunter der Titel auf einer gelben Lichtkante wie die der Theke; sie zieht sich von der Mitte
#    nach aussen, und unter ihr spiegelt sich der Titel im Tresen.
V.append(('Das Licht der Theke', lambda n: kopf(n,
    '<div class="w05-o innen">%s</div><div class="w05-m innen">%s<div class="w05-kante" aria-hidden="true"></div><div class="w05-spiegel" aria-hidden="true">%s</div>%s</div>' % (
        img('decke-weit', '(max-width:760px) 100vw, min(1240px, 92vw)', 'w05-b', '50% 40%'), titel(), titel('', 1, None, 'div'), satz('w05-s')))))

# 06 Die Vitrine: neun beleuchtete Fächer wie die Vitrine unter dem NEGRONI-Schriftzug. In jedem liegt ein Stück der Bar,
#    die Fächer gehen nacheinander an. Links der Titel.
def w06(n):
    stellen = [('decke-tief', .30, .45), ('raum', .55, .07), ('decke-tief', .78, .5), ('raum', .64, .30), ('vitrine', .5, .5), ('raum', .76, .44),
               ('raum', .30, .37), ('theke', .55, .55), ('raum', .58, .54)]
    f = ''
    for j, (k, fx, fy) in enumerate(stellen):
        d = B[k]
        f += '<div class="w06-fach" style="--j:%d"><div class="w06-in" style="%s;background-position:calc(50cqi - %dpx) calc(50cqi - %dpx)"></div><i></i></div>' % (
            j, bg4(k), round(fx * d['w'] / 4), round(fy * d['h'] / 4))
    return kopf(n, '<div class="w06-g innen"><div class="w06-l">%s%s</div><div class="w06-r"><div class="w06-kasten" role="img" aria-label="Neun Blicke in die Bar: Gewölbe, Rückbar, Vitrine, Theke">%s</div></div></div>' % (
        titel(), satz(), f))
V.append(('Die Vitrine', w06))

# 07 Durch die Buchstaben: «Decke.» riesig über die ganze Breite, und durch die Buchstaben sieht man ins Gewölbe, das langsam weiterzieht.
V.append(('Durch die Buchstaben', lambda n: kopf(n,
    '<div class="w07-o innen">%s</div><svg class="w07-svg" viewBox="0 0 1400 470" role="img" aria-label="Decke."><defs><clipPath id="w07-c"><text x="700" y="392" text-anchor="middle">Decke.</text></clipPath></defs>'
    '<g clip-path="url(#w07-c)"><rect width="1400" height="470" fill="#261E1A"/><image class="w07-bild" href="%s%s" x="-80" y="-60" width="1560" height="551" preserveAspectRatio="xMidYMid slice"/></g>'
    '<text class="w07-rand" x="700" y="392" text-anchor="middle">Decke.</text></svg><div class="w07-u innen">%s</div>' % (
        titel('w07-t', 1, ['Unter dieser']), P, B['decke-weit']['stufen'][-1][1], satz('w07-s')))))

# 08 Das Gewölbe faltet sich: das Bild ist in acht Dreiecke geteilt wie die Kappen eines Gewölbes; jedes klappt um seine Aussenkante herein,
#    bis das Gewölbe geschlossen ist.
def w08(n):
    pkt = [(0, 0), (50, 0), (100, 0), (100, 50), (100, 100), (50, 100), (0, 100), (0, 50)]
    t = ''
    for j in range(8):
        (x1, y1), (x2, y2) = pkt[j], pkt[(j + 1) % 8]
        dx, dy = x2 - x1, (y2 - y1) * .627   # Seitenverhältnis des Feldes, damit die Achse auf der Kante liegt
        l = math.hypot(dx, dy)
        t += '<div class="w08-d" style="--j:%d;clip-path:polygon(50%% 50%%,%d%% %d%%,%d%% %d%%);transform-origin:%g%% %g%%;--ax:%.4f;--ay:%.4f;%s"></div>' % (
            j, x1, y1, x2, y2, (x1 + x2) / 2, (y1 + y2) / 2, dx / l, dy / l, bg('decke-tief'))
    return kopf(n, '<div class="w08-g innen"><div class="w08-l">%s%s</div><div class="w08-r"><div class="w08-feld" role="img" aria-label="%s">%s</div></div></div>' % (
        titel(), satz(), E(B['decke-tief']['alt']), t))
V.append(('Das Gewölbe faltet sich', w08))

# 09 Der Lichtkegel: das Gewölbe liegt im Dunkeln. Ein Lichtkegel fährt einmal darüber, danach folgt er der Maus.
V.append(('Der Lichtkegel', lambda n: kopf(n,
    '<div class="w09-band"><img class="w09-dunkel" src="%s%s" alt="" width="%d" height="%d" decoding="async">'
    '<div class="w09-kegel"><div class="w09-hell">%s</div></div></div><div class="w09-u innen">%s%s</div>' % (
        P, B['decke-weit']['dunkel'], B["decke-weit"]["w"], B["decke-weit"]["h"], img("decke-weit", "100vw", "w09-b", '50% 50%'), titel(), satz()))))

# 10 Die Ecke: zwei Wände treffen sich wie die Hausecke Haasemannstraße, Rampenstraße. Links die Nacht mit dem Titel, rechts das Gewölbe;
#    die Fläche faltet sich zur Ecke, an der Kante läuft eine Goldlinie.
V.append(('Die Ecke', lambda n: kopf(n,
    '<div class="w10-szene"><div class="w10-ecke"><div class="w10-w w10-links">%s%s</div><div class="w10-w w10-rechts">%s</div></div></div>' % (
        titel(), satz(), img('decke-tief', '(max-width:760px) 100vw, 50vw', 'w10-b', '50% 40%')))))

# 11 Die Kuppel: das Gewölbe als Kuppel aus sechzig Feldern, du schaust von unten hinein; sie dreht sich ganz langsam. Jedes Feld in halber Grösse.
def w11(n):
    d = B['decke-tief']
    bw, bh = d['w'] // 4, d['h'] // 4
    R = 330
    ringe = [(12, 6), (31, 12), (50, 18), (69, 22), (84, 26)]
    f = ''
    for phi, anz in ringe:
        hgt = R * math.radians(19.5)
        breite = 2 * math.pi * R * math.sin(math.radians(phi)) / anz
        for j in range(anz):
            th = 360 / anz * j + (phi * 3)
            bx = (th % 360) / 360 * (bw - breite)
            by = phi / 90 * (bh - hgt)
            f += '<i style="width:%.1fpx;height:%.1fpx;margin:%.1fpx 0 0 %.1fpx;transform:rotateZ(%.2fdeg) rotateX(%.2fdeg) translateZ(-%dpx);%s;background-position:-%.0fpx -%.0fpx"></i>' % (
                breite - 2, hgt - 2, -(hgt - 2) / 2, -(breite - 2) / 2, th, phi, R, bg4('decke-tief'), bx, by)
    return kopf(n, '<div class="w11-g innen"><div class="w11-l">%s%s</div><div class="w11-r"><div class="w11-blick" role="img" aria-label="%s"><div class="w11-kuppel">%s</div></div></div></div>' % (
        titel(), satz(), E(d['alt']), f))
V.append(('Die Kuppel', w11))

# 12 Die Glühbirne: in der Mitte hängt eine einzelne Birne. Sie flackert an, und mit ihrem Licht wird das Gewölbe über ihr sichtbar.
V.append(('Die Glühbirne', lambda n: kopf(n,
    '<div class="w12-decke">%s</div><div class="w12-schein" aria-hidden="true"></div>'
    '<div class="w12-birne" aria-hidden="true"><span class="w12-kabel"></span><span class="w12-fassung"></span><span class="w12-glas"><b></b></span></div>'
    '<div class="w12-u innen">%s%s</div>' % (img('decke-weit', '100vw', 'w12-b', '50% 35%'), titel(), satz()))))

# 13 Das Prisma: ein dreiseitiges Prisma dreht sich beim Scrollen: das Gewölbe, die Vitrine, Derya hinter der Bar, genau die drei Dinge aus dem Satz.
#    Im Satz leuchtet in Gold, was gerade zu sehen ist.
def w13(n):
    teile = ('Eine kleine Bar an der Ecke Haasemannstraße, mit einem <span data-t="0">Gewölbe über der Theke</span>, '
             '<span data-t="1">Glühbirnen über der Vitrine</span> und <span data-t="2">zwei Leuten, die sie seit 2023 führen</span>.')
    faces = ''.join('<div class="w13-seite" style="--j:%d">%s</div>' % (j, img(k, '(max-width:760px) 90vw, 46vw', '', p, j == 0))
                    for j, (k, p) in enumerate((('decke-tief', '50% 40%'), ('vitrine', '50% 40%'), ('derya', '40% 35%'))))
    return kopf(n, '<div class="w13-steh"><div class="w13-g innen"><div class="w13-l">%s%s</div><div class="w13-r"><div class="w13-prisma">%s</div></div></div></div>' % (
        titel(), satz('w13-s', 3, teile), faces))
V.append(('Das Prisma', w13))

# 14 Das Klappschild: unter dem Gewölbe hängt an zwei Ketten das Schild der Bar. Es klappt von der Decke herunter, schwingt aus und kommt zur Ruhe.
V.append(('Das Klappschild', lambda n: kopf(n,
    '<div class="w14-decke">%s</div><div class="w14-haenger"><div class="w14-schild"><span class="w14-kette"></span><span class="w14-kette r"></span>%s'
    '<span class="logo w14-logo">%s</span>%s%s</div></div>' % (img('decke-weit', '100vw', 'w14-b', '50% 30%'), LINIE, LOGO, titel(), satz('w14-s')))))

# 15 Der Satz als Bogen: das Gewölbe in einem hohen Rundbogen, und der Satz läuft aussen am Bogen entlang hinauf und wieder hinunter.
def w15(n):
    pfad = 'M 60 640 L 60 330 A 290 290 0 0 1 640 330 L 640 640'
    innen = 'M 104 640 L 104 330 A 246 246 0 0 1 596 330 L 596 640 Z'
    return kopf(n, '<div class="w15-g innen"><div class="w15-l">%s<p class="nur-lesen">%s</p></div><div class="w15-r">'
        '<svg class="w15-svg" viewBox="0 0 700 660" role="img" aria-label="%s"><defs><clipPath id="w15-c"><path d="%s"/></clipPath><path id="w15-p" d="%s"/></defs>'
        '<g clip-path="url(#w15-c)"><rect width="700" height="660" fill="#261E1A"/><image class="w15-bild" href="%s%s" x="60" y="70" width="580" height="590" preserveAspectRatio="xMidYMid slice"/></g>'
        '<path class="w15-rand" d="%s"/><text class="w15-text"><textPath href="#w15-p" startOffset="50%%" text-anchor="middle">%s</textPath></text></svg></div></div>' % (
            titel(), E(SATZ), E(B['decke-tief']['alt']), innen, pfad, P, B['decke-tief']['stufen'][-1][1], innen, E(SATZ)))
V.append(('Der Satz als Bogen', w15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/hh2.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/hh2.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
