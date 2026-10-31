# Walk on the Wild Side · Programm-Seite, Kopf «Lauter.»: 15 Fassungen passend zum neuen Stil darunter (Kinoschild, Gewölbe-Tapete, Deckel) (30.10.2026).
# Robert: «was wir mit dem Hero machen … Gib mal bitte 15 verschiedene Variationsmöglichkeiten … das, was jetzt gerade da ist, passt nicht zu dem Stil.»
# Titel und Satz Wort für Wort aus unter.py, nur echte Fotos der Bar. Titel gross (Desktop ab ~110 px), Satz ~20 px. Bewegung nur transform/opacity.
# Kein gerahmtes Schild auf einem Foto, kein Vorhang, kein Plakat als Hauptbild. 00 = heutiger Stand. Aufruf: python3 _varianten/programm-hero/bau.py
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER); sys.path.insert(0, HIER)
import bau as B
import unter
E = html.escape
ORD = '_varianten/programm-hero'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('h.css', 'h.js', 'nav.js'))))
TITEL = 'Lauter.'
SATZ = 'Donnerstags spielt ab und zu jemand live, samstags legen DJs auf, und manchmal steht ein Gast aus einer anderen Bar neben Momo. Das Programm der Woche.'
assert SATZ in open('unter.py').read() and "['Lauter.']" in open('unter.py').read()
ABENDE = [('Donnerstag', 'Live, ab und zu'), ('Freitag', 'Momo an der Bar'), ('Samstag', 'Die DJ-Abende')]


def bild(k, pos='50% 50%', sizes='100vw', cls='hb'):
    d = B.mache(k)
    return '<figure class="%s" style="--lq:url(%s)">%s</figure>' % (cls, d['lq'], B.img_tag(k, sizes, True, ' style="object-position:%s"' % pos))


def titel(cls=''):
    return '<h1 class="titel hx-t %s">%s</h1>' % (cls, ''.join('<span style="--b:%d">%s</span>' % (i, E(c)) for i, c in enumerate(TITEL)))


def satz(cls=''):
    return '<p class="hx-s %s">%s</p>' % (cls, E(SATZ))


def tafel(zeilen, cls=''):
    c, out = 0, ''
    for t, k in zeilen:
        z = ''
        for ch in t:
            z += '<span style="--b:%d">%s</span>' % (c, '&nbsp;' if ch == ' ' else E(ch)); c += 1
        out += '<p class="%s">%s</p>' % (k, z)
    return '<div class="ht %s" aria-hidden="true"><div class="ht-r">%s</div></div>' % (cls, out)


def birnen(oben=15, seite=5):
    pos = [('calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (i / (oben - 1)), 'var(--wb)') for i in range(oben)]
    pos += [('calc(100% - var(--wb))', 'calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (i / (seite + 1))) for i in range(1, seite + 1)]
    pos += [('calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (1 - i / (oben - 1)), 'calc(100% - var(--wb))') for i in range(oben)]
    pos += [('var(--wb)', 'calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (1 - i / (seite + 1))) for i in range(1, seite + 1)]
    return ''.join('<i class="hx-birne" style="left:%s;top:%s;--j:%d"></i>' % (x, y, j) for j, (x, y) in enumerate(pos))


def ring(k, text, sizes):
    d = B.mache(k)
    return '''<div class="hx-deckel"><figure class="hx-dbild" style="--lq:url(%s)">%s</figure><svg class="hx-ring" viewBox="0 0 300 300" aria-hidden="true"><defs><path id="hx-r" d="M150,150 m-128,0 a128,128 0 1,1 256,0 a128,128 0 1,1 -256,0"/></defs>
<circle cx="150" cy="150" r="146"/><circle cx="150" cy="150" r="112"/><text><textPath href="#hx-r" textLength="796" lengthAdjust="spacing">%s</textPath></text></svg></div>''' % (
        d['lq'], B.img_tag(k, sizes, True, ' style="object-position:50% 30%"'), E(text * 2))


def kopf(n, inner, cls=''):
    return '<header class="hx h%02d auf %s" id="auftakt">%s</header>' % (n, cls, inner)


TAPETE = '<div class="hx-tapete"></div>'
V = []

# 01 · Kinoschild auf der Tapete: das Gewölbe der Bar über den ganzen Kopf, mittendrin ein grosses Kinoschild mit LAUTER. in Steckbuchstaben.
V.append(('Kinoschild auf der Tapete', lambda n: kopf(n, TAPETE + '<div class="innen hx-mitte"><div class="hx-schild"><div class="hx-birnen">%s</div>%s</div><h1 class="mx-sr">%s</h1>%s</div>' % (
    birnen(), tafel([('LAUTER.', '')], 'h1-tafel'), TITEL, satz()))))

# 02 · Die Tafel ist der Kopf: über die ganze Fläche schwarze Rillen, LAUTER. fällt in riesigen Steckbuchstaben, der Satz darunter.
V.append(('Die Tafel ist der Kopf', lambda n: kopf(n, '<div class="h2-rillen"></div><div class="innen"><h1 class="mx-sr">%s</h1>%s%s</div>' % (TITEL, tafel([('LAUTER.', '')], 'h2-tafel'), satz()))))

# 03 · Tapete und Sängerin: links das Gewölbe mit Titel und Satz, rechts die Sängerin in voller Höhe, Wand an Wand.
V.append(('Tapete und Sängerin', lambda n: kopf(n, '<div class="h3-links">%s<div class="h3-text">%s%s</div></div><div class="h3-rechts">%s</div>' % (
    TAPETE, titel(), satz(), bild('saengerin-sw', '50% 30%', '(max-width:760px) 100vw, 46vw')))))

# 04 · Das Love-Bild: das Duo unter den Glühbirnen-Buchstaben über die ganze Fläche, das Bild zieht sich beim Öffnen zurück.
V.append(('Das Love-Bild', lambda n: kopf(n, bild('konzert-love', '50% 38%') + '<div class="hx-hof"></div><div class="innen hx-unten">%s%s</div>' % (titel(), satz()))))

# 05 · Der Blick nach oben: der Raum mit dem Gewölbe an der Decke, beim Scrollen hebt sich der Blick langsam zur Decke.
V.append(('Der Blick nach oben', lambda n: kopf(n, bild('decke-raum', '50% 48%') + '<div class="hx-hof"></div><div class="innen hx-unten">%s%s</div>' % (titel(), satz()))))

# 06 · Ein grosser Deckel: auf der Tapete rechts ein grosser Deckel mit der Sängerin, sein Ring dreht beim Scrollen; links Titel und Satz.
V.append(('Ein grosser Deckel', lambda n: kopf(n, TAPETE + '<div class="innen h6-raster"><div>%s%s</div>%s</div>' % (
    titel(), satz(), ring('saengerin', 'LAUTER · WALK ON THE WILD SIDE · ', '(max-width:760px) 80vw, 34vw')))))

# 07 · Birnen unter dem Titel: auf der Tapete steht der Titel gross in der Mitte, darunter eine Goldleiste mit Birnen, die einmal nacheinander angehen.
V.append(('Birnen unter dem Titel', lambda n: kopf(n, TAPETE + '<div class="innen hx-mitte">%s<div class="h7-leiste">%s</div>%s</div>' % (
    titel(), ''.join('<i style="--j:%d"></i>' % j for j in range(21)), satz()))))

# 08 · Drei Bilder Wand an Wand: das Duo, die Sängerin, das Quartett in voller Höhe; sie steigen nacheinander auf, unten Titel und Satz.
V.append(('Drei Bilder Wand an Wand', lambda n: kopf(n, '<div class="h8-wand">%s</div><div class="hx-hof"></div><div class="innen hx-unten h8-text">%s%s</div>' % (
    ''.join('<div style="--n:%d">%s</div>' % (j, bild(k, p, '(max-width:760px) 34vw, 34vw')) for j, (k, p) in enumerate([('konzert-love', '40% 40%'), ('saengerin-sw', '50% 30%'), ('konzert', '72% 50%')])), titel(), satz()))))

# 09 · Das Schild hängt am Gewölbe: oben ein Band der Decke, daran hängt an zwei Ketten das Kinoschild und pendelt sich ein.
V.append(('Das Schild hängt am Gewölbe', lambda n: kopf(n, '<div class="h9-decke"></div><div class="innen hx-mitte h9-mitte"><div class="h9-haenger"><i class="h9-kette"></i><i class="h9-kette"></i><div class="hx-schild"><div class="hx-birnen">%s</div>%s</div></div><h1 class="mx-sr">%s</h1>%s</div>' % (
    birnen(13, 4), tafel([('LAUTER.', '')], 'h1-tafel'), TITEL, satz()))))

# 10 · Lichtschrift: auf der Tapete gehen die Buchstaben von «Lauter.» einzeln an, wie die Glühbirnen-Buchstaben über dem Duo.
V.append(('Lichtschrift', lambda n: kopf(n, TAPETE + '<div class="innen hx-mitte">%s%s</div>' % (titel('h10-t'), satz()))))

# 11 · Der Kreis öffnet sich: die Sängerin erst in einem runden Ausschnitt mit Goldring, dann wächst der Kreis über den ganzen Kopf.
V.append(('Der Kreis öffnet sich', lambda n: kopf(n, '<div class="h11-kreis"><div class="h11-innen">%s</div></div><div class="hx-hof h11-hof"></div><div class="innen hx-unten">%s%s</div>' % (
    bild('saengerin', '50% 30%'), titel(), satz()))))

# 12 · Das Gewölbe dreht sich: der Deckendruck wie von unten gesehen, er dreht sich beim Scrollen ganz langsam; der Titel steht still in der Mitte.
V.append(('Das Gewölbe dreht sich', lambda n: kopf(n, '<div class="h12-dreh"></div><div class="h12-schleier"></div><div class="innen hx-mitte">%s%s</div>' % (titel(), satz()))))

# 13 · Die Tapete sinkt: das Gewölbe senkt sich beim Öffnen von oben in den Kopf und läuft nach unten in die Nacht aus; Titel links, Satz rechts.
V.append(('Die Tapete sinkt', lambda n: kopf(n, '<div class="hx-tapete h13-tapete"></div><div class="innen h13-unten">%s%s</div>' % (titel(), satz()))))

# 14 · Bild im Birnenrahmen: das Quartett steht in einem Holzrahmen mit Glühbirnen, wie das Schild darunter; Titel und Satz unter dem Rahmen.
V.append(('Bild im Birnenrahmen', lambda n: kopf(n, TAPETE + '<div class="innen h14-raster"><div class="h14-rahmen"><div class="hx-birnen">%s</div>%s</div><div class="h14-text">%s%s</div></div>' % (
    birnen(17, 6), bild('konzert', '60% 50%', '(max-width:760px) 100vw, 80vw'), titel(), satz()))))

# 15 · Laufschrift: die Sängerin über die ganze Fläche, unten läuft ein schmales Band mit Steckbuchstaben ruhig durch: die drei Abende der Woche.
V.append(('Laufschrift', lambda n: kopf(n, bild('saengerin-sw', '50% 30%') + '<div class="hx-hof"></div><div class="innen hx-unten h15-text">%s%s</div><div class="h15-band" aria-hidden="true"><div class="h15-zug">%s</div></div>' % (
    titel(), satz(), ('<span>' + ''.join('%s&nbsp;&nbsp;%s&nbsp;&nbsp;·&nbsp;&nbsp;' % (E(t.upper()), E(u.upper())) for t, u in ABENDE) + '</span>') * 2))))


def seite(n):
    h = unter.programm()
    if n:
        a = h.find('<header class="sk auf" id="auftakt">'); b = h.find('</header>', a) + len('</header>')
        assert a > 0
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/h.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    sk = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/h.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + sk + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
