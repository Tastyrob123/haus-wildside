# Walk on the Wild Side · Unterseite Besuch: 15 Fassungen für den Kopf «Bis 2 Uhr.», Runde 2 (31.10.2026).
# Robert zur ersten Runde: «alle mist. die müssen außergewöhnlicher sein». 00 = heute.
# Wortlaut wie heute, Zeiten und Adresse aus HAUS (bau.py), nur echte Fotos der Bar und ihre Freisteller (hero-20/ebenen.py).
# Jede Fassung ein eigener Gegenstand mit eigener Bewegung, nur transform/opacity. Wechsel mit ← →.
# Aufruf: python3 _varianten/besuch-hero-15b/bau.py → 00.html … 15.html
import os, sys, json, math, re
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, mache, zl, HAUS, V as BV

ORD = '_varianten/besuch-hero-15b'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('hero.css', 'hero.js', 'varianten-nav.js', 'varianten-nav.css', 'bau.py'))))
basis = open('besuch.html').read()
a = basis.index('<header class="sk auf" id="auftakt">')
b = basis.index('</header>', a) + len('</header>')
LOGO = re.search(r'(<svg viewBox="0 0 1296 1600".*?</svg>)', basis, re.S).group(1)

SATZ = 'Haasemannstraße 13, Ecke Rampenstraße, Linden-Mitte. Donnerstag bis Samstag ab 19 Uhr.'
TAGE = [('Do', 'Donnerstag', '19 bis 1 Uhr'), ('Fr', 'Freitag', '19 bis 2 Uhr'), ('Sa', 'Samstag', '19 bis 2 Uhr')]
assert [(t[1], t[2]) for t in TAGE] == [(z[0], z[1]) for z in HAUS['zeiten'][:3]]
EXTRA_ALT = {'fb-fenster-aussen': 'Die Fenster der Bar von aussen am Abend'}


def daten(k):
    try:
        return mache(k)
    except KeyError:   # Fotos aus früheren Runden, schon fertig in assets/bild
        d = json.load(open('assets/bild/%s.json' % k))
        d['alt'] = EXTRA_ALT[k]
        return d


def bild(k, cls='', sizes='100vw', pos=None, sofort=True, stil=''):
    d = daten(k)
    ss = ', '.join('assets/bild/%s?v=%s %dw' % (f, BV, w) for w, f in d['stufen'])
    st = ' style="object-position:%s"' % pos if pos else ''
    lade = ' fetchpriority="high"' if sofort else ' loading="lazy"'
    return '<figure class="bx-f %s" style="--lq:url(%s);%s"><img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s%s></figure>' % (
        cls, d['lq'], stil, d['stufen'][-1][1], BV, ss, sizes, E(d['alt']), d['w'], d['h'], lade, st)


def url(k):
    return 'assets/bild/%s?v=%s' % (daten(k)['stufen'][-1][1], BV)


def eb(name, cls='', alt=''):
    return '<img class="%s" src="%s/%s.webp?v=%s" alt="%s" decoding="async">' % (cls, ORD, name, VER, E(alt))


def titel(cls='', zeilen=('Bis 2 Uhr.',), i0=1):
    return '<h1 class="titel bx-t %s">%s</h1>' % (cls, zl(list(zeilen), i0=i0))


def satz(cls='', i=3):
    return '<p class="text sw bx-s %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def kopf(n, inner, cls=''):
    return '<header class="sk-v auf bx bx%02d %s" id="auftakt" data-v="%d">%s</header>' % (n, cls, n, inner)


V = []

# 01 Die Fallblatt-Tafel
def h01(n):
    zeilen = ['DO  19 BIS 1 UHR', 'FR  19 BIS 2 UHR', 'SA  19 BIS 2 UHR', '']   # letzte Zeile: Stand jetzt, setzt hero.js
    tafel = ''.join('<div class="bx01-zeile%s">%s</div>' % (' jetzt' if j == 3 else '', ''.join(
        '<span class="bx01-z" data-z="%s"><b>&nbsp;</b></span>' % E(c) for c in z.ljust(20))) for j, z in enumerate(zeilen))
    return kopf(n, '<div class="innen bx01-in"><div class="bx01-kopf">%s%s</div><div class="bx01-tafel sw" style="--i:2" aria-label="Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr">%s</div></div>' % (
        titel(), satz(), tafel))
V.append(('Die Fallblatt-Tafel', 'Eine Abfahrtstafel wie am Bahnhof: die Blätter klappern durch und bleiben auf den drei Abenden stehen; die letzte Zeile sagt, ob gerade offen ist.', h01))

# 02 Die Tür geht auf
def h02(n):
    tuer = lambda s: '<div class="bx02-fluegel %s"><i class="bx02-rahmen"></i><i class="bx02-griff"></i></div>' % s
    return kopf(n, bild('ft-raum-abend', 'bx-voll bx02-raum', '100vw', '50% 45%') +
                '<div class="bx02-tor" aria-hidden="true">%s%s</div><div class="innen bx-unten bx02-text">%s%s</div>' % (tuer('l'), tuer('r'), titel(), satz()))
V.append(('Die Tür geht auf', 'Zwei dunkle Türflügel schwingen in 3D nach innen auf, dahinter der Raum am Abend; erst dann steigt der Titel hoch.', h02))

# 03 Durchs Fenster hinein
V.append(('Durchs Fenster hinein', 'Die Fenster der Bar von aussen; beim Scrollen fährt die Kamera durch die Scheibe, bis man drinnen am Tresen steht.',
          lambda n: kopf(n, '<div class="bx03-buehne"><div class="bx03-innen">%s</div><div class="bx03-aussen">%s</div><div class="innen bx-unten">%s%s</div></div>' % (
              bild('ft-raum-abend', 'bx-voll', '100vw', '50% 45%'), bild('fb-fenster-aussen', 'bx-voll', '100vw', '50% 50%'), titel(), satz()))))

# 04 Glühbirnen-Schrift
def gluehbirnen(text='Bis 2 Uhr.', spalten=86):
    from PIL import Image, ImageDraw, ImageFont
    f = ImageFont.truetype(os.path.join(ORD, 'prata.ttf'), 420)   # aus assets/schrift/prata-latin.woff2
    l, t, r, u = f.getbbox(text)
    im = Image.new('L', (r - l + 40, u - t + 40), 0)
    ImageDraw.Draw(im).text((20 - l, 20 - t), text, font=f, fill=255)
    zelle = im.width / spalten
    zeilen = int(math.ceil(im.height / zelle))
    punkte = []
    for y in range(zeilen):
        for x in range(spalten):
            box = (int(x * zelle), int(y * zelle), int((x + 1) * zelle), int((y + 1) * zelle))
            st = im.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0)) / 255
            if st > .28:
                punkte.append((x, y))
    aus = ''.join('<circle cx="%.1f" cy="%.1f" r=".34"/>' % (x + .5, y + .5) for x, y in punkte)
    flacker = {len(punkte) // 3, (len(punkte) * 4) // 5}
    an = ''.join('<g class="an%s" style="--d:%.2fs"><circle class="h" cx="%.1f" cy="%.1f" r=".62"/><circle class="k" cx="%.1f" cy="%.1f" r=".34"/></g>' % (
        ' fl' if j in flacker else '', .5 + x * .03 + (y % 3) * .05, x + .5, y + .5, x + .5, y + .5) for j, (x, y) in enumerate(punkte))
    return '<svg class="bx04-svg" viewBox="0 0 %d %d" aria-hidden="true"><g class="aus">%s</g>%s</svg>' % (spalten, zeilen, aus, an), len(punkte)


def h04(n):
    svg, anzahl = gluehbirnen()
    return kopf(n, '<div class="innen bx04-in"><h1 class="titel bx04-t"><span class="vh">Bis 2 Uhr.</span>%s</h1>%s</div>' % (svg, satz('', 3)))
V.append(('Glühbirnen-Schrift', 'Der Titel aus Glühbirnen wie die NEGRONI-Schrift über der Vitrine; die Birnen gehen von links nach rechts an, zwei flackern weiter.', h04))

# 05 Das Plakat
def wellen():
    nn, breite, hoehe, periode = 7, 600, 1600, 400
    pfade = []
    for k in range(nn):
        mx = breite * (k + .5) / nn
        w = breite / nn * .3
        phi = k * .9
        links, rechts = [], []
        for y in range(0, hoehe + 1, 10):
            dx = 26 * math.sin(2 * math.pi * y / periode + phi)
            links.append('%.1f,%d' % (mx - w + dx, y))
            rechts.append('%.1f,%d' % (mx + w + dx, y))
        pfade.append('M' + ' L'.join(links) + ' L' + ' L'.join(reversed(rechts)) + 'Z')
    return '<svg viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true">%s</svg>' % (breite, hoehe, ''.join('<path d="%s"/>' % p for p in pfade))


def h05(n):
    return kopf(n, '<div class="bx05-papier"><div class="bx05-wellen"><div class="bx05-zug">%s%s</div></div>%s'
                   '<div class="innen bx05-in"><h1 class="bx05-t">%s</h1><p class="bx05-zeile sw" style="--i:3">Donnerstag bis Samstag<br>ab 19 Uhr</p>'
                   '<div class="bx05-fuss sw" style="--i:4"><b>Walk on the Wild Side</b><span>Haasemannstr. 13<br>30449 Hannover</span></div></div></div>' % (
        wellen(), wellen(), eb('momo-sw-frei', 'bx05-momo', 'Momo, schwarz-weiss freigestellt'), zl(['Bis 2', 'Uhr.'], i0=1)))
V.append(('Das Plakat', 'Der Kopf als SESSION-Plakat der Bar: Papier, rote Wellen, die langsam fliessen, Momo schwarz-weiss davor, die Schrift blau und riesig.', h05))

# 06 Kopf in den Nacken
V.append(('Kopf in den Nacken', 'Rechts eine grosse runde Öffnung, durch die man nach oben auf die bedruckte Gewölbe-Decke schaut; die Decke dreht sich ganz langsam.',
          lambda n: kopf(n, '<div class="bx06-auge sw" style="--i:1" aria-hidden="true"><div class="bx06-dreh">%s</div></div><div class="innen bx06-in"><div>%s%s</div></div>' % (
              bild('decke-2017', '', '110vh', '50% 50%'), titel(), satz()))))

# 07 Um die Ecke
def h07(n):
    u = url('pf-schild')
    return kopf(n, '<div class="innen bx07-in"><div class="bx07-text">%s%s</div><div class="bx07-ecke sw" style="--i:1" role="img" aria-label="Das Schild an der Hausecke, beide Seiten">'
                   '<div class="bx07-l" style="background-image:url(%s)"></div><div class="bx07-r" style="background-image:url(%s)"></div></div></div>' % (titel(), satz(), u, u))
V.append(('Um die Ecke', 'Das Foto der Hausecke ist an der Mauerkante in 3D gefaltet; die Ecke kommt einem entgegen und dreht sich mit der Maus.', h07))

# 08 Der Leuchtkasten
def h08(n):
    # Schildfläche als Hintergrund, nicht als <img>: Safari blendet sonst die Rückseite nicht aus
    s = '<div class="bx08-seite %s"%s></div>'
    flaeche = ' style="background-image:url(%s/schild-gerade.webp?v=%s)"' % (ORD, VER)
    return kopf(n, '<div class="innen bx08-in"><div>%s%s</div><div class="bx08-halter sw" style="--i:2" role="img" aria-label="Das Schild der Bar: Walk on the Wild Side"><i class="bx08-arm"></i><div class="bx08-kasten">%s%s%s%s</div></div></div>' % (
        titel(), satz(), s % ('v', flaeche), s % ('h', flaeche), s % ('re', ''), s % ('li', '')))
V.append(('Der Leuchtkasten', 'Das Schild der Hausecke als echter Leuchtkasten in 3D, an einem Arm aufgehängt; er dreht sich langsam und zeigt beide Seiten.', h08))

# 09 Der Abend vergeht
def h09(n):
    st = [('schild-ecke', '40% 40%'), ('ft-theke-gaeste', '50% 50%'), ('voll', '50% 50%'), ('glas-kerze', '50% 55%')]
    fotos = ''.join(bild(k, 'bx-voll bx09-foto' + (' an' if j == 0 else ''), '100vw', p, j < 2, '--j:%d' % j) for j, (k, p) in enumerate(st))
    return kopf(n, '<div class="bx09-buehne">%s<div class="innen bx09-in"><div>%s%s</div><p class="bx09-uhr" aria-hidden="true"><span>19</span><i>:</i><span>00</span></p></div>'
                   '<div class="bx09-leiste" aria-hidden="true"><i></i></div></div>' % (fotos, titel(), satz()))
V.append(('Der Abend vergeht', 'Beim Scrollen läuft eine grosse Uhr von 19:00 bis 02:00, dahinter wechselt der Abend: Ecke, Theke, voller Raum, letztes Glas.', h09))

# 10 Mit der Kerze
V.append(('Mit der Kerze', 'Der Raum liegt im Dunkeln; ein warmer Lichtkreis folgt der Maus und zeigt, was drin ist. Ohne Maus wandert das Licht von selbst.',
          lambda n: kopf(n, bild('ft-raum-abend', 'bx-voll bx10-raum', '100vw', '50% 45%') + '<div class="bx10-dunkel" aria-hidden="true"></div><div class="innen bx-unten">%s%s</div>' % (titel(), satz()))))

# 11 Breitwand
V.append(('Breitwand', 'Wie im Kino: oben ein schmaler Vorspann, in der Mitte der Raum im Breitwandformat mit langsamer Kamerafahrt, unten der Titel wie ein Filmtitel.',
          lambda n: kopf(n, '<div class="bx11-vor sw" style="--i:0"><span>Walk on the Wild Side</span><span>Linden-Mitte</span></div><div class="bx11-band"><div class="bx11-fahrt">%s</div></div>'
                         '<div class="innen bx11-unten">%s%s</div>' % (bild('ft-raum-abend', 'bx-voll', '130vw', '50% 45%'), titel(), satz()))))

# 12 Der Untersetzer
def h12(n):
    ring = 'HAASEMANNSTRASSE 13 · ECKE RAMPENSTRASSE · LINDEN-MITTE · DONNERSTAG BIS SAMSTAG AB 19 UHR · '
    return kopf(n, '<div class="innen bx12-in"><div>%s%s</div><div class="bx12-tisch sw" style="--i:2" aria-hidden="true"><div class="bx12-deckel">'
                   '<svg viewBox="0 0 400 400"><defs><path id="bx12-k" d="M200,200 m-168,0 a168,168 0 1,1 336,0 a168,168 0 1,1 -336,0"/></defs>'
                   '<circle cx="200" cy="200" r="196"/><circle class="l" cx="200" cy="200" r="186"/><circle class="l" cx="200" cy="200" r="148"/>'
                   '<g class="bx12-dreh"><text><textPath href="#bx12-k" textLength="1052" lengthAdjust="spacing">%s</textPath></text></g></svg></div>%s</div></div>' % (
        titel(), satz(), E(ring), eb('glas-negroni-frei', 'bx12-glas')))
V.append(('Der Untersetzer', 'Ein Negroni steht auf einem grossen Untersetzer, der flach im Raum liegt; um den Rand läuft die Adresse im Kreis.', h12))

# 13 Rundumblick
def h13(n):
    nn = 20
    stuecke = ''.join('<i style="--k:%d"></i>' % k for k in range(nn))
    return kopf(n, '<div class="bx13-raum" style="--n:%d;--bild:url(../../%s)"><div class="bx13-zyl">%s</div></div><div class="innen bx-unten">%s%s</div>' % (
        nn, url('ft-raum-abend'), stuecke, titel(), satz()))
V.append(('Rundumblick', 'Man steht mitten im Raum: das Foto ist um einen herum gebogen, der Blick schwenkt langsam von links nach rechts und folgt der Maus.', h13))

# 14 Der Weg hinein
def h14(n):
    st = [('schild-ecke', 'Die Ecke', '40% 40%'), ('tuer-rot', 'Die Tür', '50% 55%'), ('ft-theke-gaeste', 'Die Theke', '50% 50%'), ('glas-kerze', 'Dein Platz', '50% 55%')]
    karten = ''.join('<div class="bx14-karte" style="--j:%d">%s<span class="etikett">%s</span></div>' % (j, bild(k, '', '90vw', p, j < 2), E(w)) for j, (k, w, p) in enumerate(st))
    return kopf(n, '<div class="bx14-buehne"><div class="innen bx14-kopf">%s%s</div><div class="bx14-stapel">%s</div></div>' % (titel(), satz(), karten))
V.append(('Der Weg hinein', 'Beim Scrollen legen sich vier Bilder übereinander, von der Strasse bis an den Platz: Ecke, Tür, Theke, dein Glas.', h14))

# 15 Die Visitenkarte
def h15(n):
    zeilen = ''.join('<div><span>%s</span><b>%s</b></div>' % (E(lang), E(zeit)) for _, lang, zeit in TAGE)
    return kopf(n, '<div class="innen bx15-in"><div>%s%s</div><div class="bx15-tisch sw" style="--i:2"><div class="bx15-karte" data-karte>'
                   '<div class="bx15-vorn">%s<span class="etikett">Nachbarschafts-Mixology-Bar</span></div>'
                   '<div class="bx15-hinten"><b class="bx15-adr">Haasemannstraße 13</b><span>Ecke Rampenstraße · Linden-Mitte</span>%s</div></div></div></div>' % (
        titel(), satz(), LOGO, zeilen))
V.append(('Die Visitenkarte', 'Eine grosse Karte der Bar liegt schräg im Raum, dreht sich um und zeigt hinten Adresse und Zeiten; sie neigt sich mit der Maus.', h15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, nm] for j, (nm, _, _) in enumerate(V)]
KOPF = '<link rel="stylesheet" href="%s/hero.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, kopfhtml, name):
    h = basis[:a] + kopfhtml + basis[b:] if nr else basis
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/hero.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, '', 'Heute'))
    for j, (name, _, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD, '· Birnen:', gluehbirnen()[1])
