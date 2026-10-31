# Walk on the Wild Side · Unterseite Besuch: 15 Fassungen für den Kopf «Bis 2 Uhr.» (31.10.2026).
# Robert: «gib mir 15 alternative visualisierungen für den Hero». 00 = heute.
# Wortlaut wie heute, Zeiten und Adresse aus HAUS (bau.py), nur echte Fotos der Bar. Titel gross, Satz gut lesbar.
# Jede Fassung eigene Darstellung und eigene Bewegung, nur transform/opacity. Wechsel mit ← →.
# Aufruf: python3 _varianten/besuch-hero-15/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, mache, zl, HAUS, V as BV

ORD = '_varianten/besuch-hero-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('hero.css', 'hero.js', 'varianten-nav.js', 'varianten-nav.css', 'bau.py'))))
basis = open('besuch.html').read()
a = basis.index('<header class="sk auf" id="auftakt">')
b = basis.index('</header>', a) + len('</header>')

SATZ = 'Haasemannstraße 13, Ecke Rampenstraße, Linden-Mitte. Donnerstag bis Samstag ab 19 Uhr.'
TAGE = [('Do', 'Donnerstag', '19 bis 1 Uhr'), ('Fr', 'Freitag', '19 bis 2 Uhr'), ('Sa', 'Samstag', '19 bis 2 Uhr')]
assert [(t[1], t[2]) for t in TAGE] == [(z[0], z[1]) for z in HAUS['zeiten'][:3]]


EXTRA_ALT = {'fb-fenster-nacht': 'Blick von der Strasse durchs Fenster in die Bar bei Nacht',
             'fb-fenster-aussen': 'Die Fenster der Bar von aussen am Abend'}


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
    return '<figure class="bh-f %s" style="--lq:url(%s);%s"><img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s%s></figure>' % (
        cls, d['lq'], stil, d['stufen'][-1][1], BV, ss, sizes, E(d['alt']), d['w'], d['h'], lade, st)


def titel(cls='', zeilen=('Bis 2 Uhr.',), i0=1):
    return '<h1 class="titel bh-t %s">%s</h1>' % (cls, zl(list(zeilen), i0=i0))


def satz(cls='', i=3):
    return '<p class="text sw bh-s %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def tage(cls='', i0=4):
    return '<div class="bh-tage %s">%s</div>' % (cls, ''.join(
        '<div class="sw" style="--i:%d"><span class="etikett">%s</span><b>%s</b></div>' % (i0 + j, E(lang), E(zeit)) for j, (_, lang, zeit) in enumerate(TAGE)))


def kopf(n, inner, cls=''):
    return '<header class="sk-v auf bh bh%02d %s" id="auftakt" data-v="%d">%s</header>' % (n, cls, n, inner)


V = []

# 01 Die Uhr
def h01(n):
    striche = ''.join('<i style="--r:%ddeg" class="%s"></i>' % (k * 30, 'gross' if k % 3 == 0 else '') for k in range(12))
    zahlen = ''.join('<span style="--r:%ddeg"><em>%d</em></span>' % (k * 30, k or 12) for k in range(12))
    return kopf(n, '<div class="innen bh01-in"><div>%s%s%s</div><div class="bh01-uhr sw" style="--i:2" aria-hidden="true"><div class="bh01-blatt">%s%s'
                   '<i class="bh01-std"></i><i class="bh01-min"></i><i class="bh01-nabe"></i></div></div></div>' % (titel(), satz(), tage(), striche, zahlen))
V.append(('Die Uhr', 'Links der Titel und die drei Abende, rechts ein grosses Zifferblatt; der Zeiger läuft beim Öffnen von 19 auf 2 Uhr.', h01))

# 02 Der Raum am Abend
V.append(('Der Raum am Abend', 'Der volle Raum über den ganzen Schirm, die Kamera fährt langsam zurück; Titel unten links, riesig.',
          lambda n: kopf(n, '<div class="bh02-zoom">%s</div><div class="innen bh-unten">%s%s</div>' % (bild('ft-raum-abend', 'bh-voll', '100vw', '50% 45%'), titel(), satz()))))

# 03 Die Ecke, halbiert
V.append(('Die Ecke, halbiert', 'Links die Hausecke mit dem Schild als hohe Hälfte, die von links hereinschiebt; rechts auf Nacht der Titel und die drei Abende.',
          lambda n: kopf(n, '<div class="bh03-bild">%s</div><div class="bh03-text"><div>%s%s%s</div></div>' % (
              bild('schild-ecke', '', '50vw', '30% 45%'), titel(), satz(), tage()))))

# 04 Die zwei Strassenschilder
def h04(n):
    return kopf(n, '<div class="innen bh04-in"><div>%s%s</div><div class="bh04-ecke" aria-hidden="true">'
                   '<div class="bh04-schild a"><b>Haasemannstraße</b><small>13</small></div>'
                   '<div class="bh04-schild b"><b>Rampenstraße</b></div><i class="bh04-mast"></i></div></div>' % (titel(), satz()))
V.append(('Die zwei Strassenschilder', 'Rechts kreuzen sich die beiden Strassenschilder der Ecke an einem Mast und schwingen beim Öffnen kurz nach; links der Titel.', h04))

# 05 Der Abend als Strecke
def h05(n):
    marken = ''.join('<span style="--x:%.4f"><b>%s</b></span>' % (j / 7, u) for j, u in enumerate(['19', '20', '21', '22', '23', '24', '1', '2']))
    return kopf(n, '<div class="bh05-bild">%s</div><div class="innen bh05-in"><div class="bh05-text">%s%s</div>'
                   '<div class="bh05-strecke sw" style="--i:4" aria-hidden="true"><i class="bh05-linie"></i><i class="bh05-licht"></i>%s</div></div>' % (
        bild('fb-fenster-nacht', '', '55vw', '50% 50%'), titel(), satz(), marken))
V.append(('Der Abend als Strecke', 'Oben rechts das Fenster bei Nacht, quer über die ganze Breite eine Zeitleiste von 19 bis 2 Uhr, auf der ein goldenes Licht entlangläuft.', h05))

# 06 Drei Abende
def h06(n):
    sp = ''.join('<div class="bh06-sp" style="--j:%d">%s<div class="bh06-tag"><b class="titel">%s</b><span>%s</span></div></div>' % (
        j, bild(k, '', '34vw', p, j < 3), E(lang), E(zeit)) for j, ((_, lang, zeit), k, p) in enumerate(zip(TAGE, ['tuer-rot', 'wf-raum', 'glas-kerze'], ['50% 60%', '50% 40%', '50% 50%'])))
    return kopf(n, '<div class="bh06-drei">%s</div><div class="bh06-oben"><div class="innen">%s%s</div></div>' % (sp, titel(), satz()))
V.append(('Drei Abende', 'Donnerstag, Freitag, Samstag als drei hohe Bilder, die nacheinander von unten hochsteigen; oben quer der Titel.', h06))

# 07 Das Schild geht an
V.append(('Das Schild geht an', 'Links der Titel, rechts gross das Schild an der Hausecke: es ist erst dunkel und flackert dann an wie Leuchtreklame.',
          lambda n: kopf(n, '<div class="innen bh07-in"><div>%s%s%s</div><div class="bh07-schild sw" style="--i:1">%s<i class="bh07-aus"></i></div></div>' % (
              titel(), satz(), tage('bh-tage-zeile'), bild('pf-schild', '', '58vw', '50% 50%')))))

# 08 Der Weg hin
def h08(n):
    return kopf(n, '<div class="innen bh08-in"><div>%s%s<p class="bh08-weg sw" style="--i:4"><span class="etikett">Zu Fuss</span>Zwei Minuten vom Küchengarten</p></div>'
                   '<div class="bh08-karte sw" style="--i:2" aria-hidden="true"><div class="bh08-flaeche">'
                   '<i class="bh08-str h"></i><i class="bh08-str r"></i><i class="bh08-str n1"></i><i class="bh08-str n2"></i>'
                   '<span class="bh08-name h">Haasemannstraße</span><span class="bh08-name r">Rampenstraße</span>'
                   '<span class="bh08-kg"><i></i>Küchengarten</span>'
                   '<span class="bh08-punkt"><i></i><i></i><b>13</b></span></div></div></div>' % (titel(), satz()))
V.append(('Der Weg hin', 'Rechts ein gezeichneter Stadtplan der Ecke: die zwei Strassen, der Küchengarten, und an der Nummer 13 pulsiert ein goldener Punkt.', h08))

# 09 Das Band zwischen den Zeilen
V.append(('Das Band zwischen den Zeilen', '«Bis» über, «2 Uhr.» unter einem breiten Band mit dem Raum unter der Decke; das Band gleitet beim Scrollen langsamer mit.',
          lambda n: kopf(n, '<div class="innen bh09-oben">%s</div><div class="bh09-band"><div class="bh09-zug">%s</div></div><div class="innen bh09-unten">%s%s</div>' % (
              titel('bh09-t1', ('Bis',), 1), bild('decke-raum', '', '100vw', '50% 62%'), titel('bh09-t2', ('2 Uhr.',), 2), satz('', 4)))))

# 10 Die grosse Zwei
V.append(('Die grosse Zwei', 'Kein Foto: links eine Zwei über die ganze Höhe als goldene Kontur, die sich aufrichtet; rechts Titel, Satz und die drei Abende.',
          lambda n: kopf(n, '<div class="innen bh10-in"><p class="bh10-zwei titel" aria-hidden="true"><span>2</span></p><div>%s%s%s</div></div>' % (titel(), satz(), tage()))))

# 11 Die Tafel an der Tür
def h11(n):
    zeilen = ''.join('<div><span>%s</span><b>%s</b></div>' % (E(lang), E(zeit)) for _, lang, zeit in TAGE)
    zeilen += '<div class="zu"><span>Sonntag bis Mittwoch</span><b>geschlossen</b></div>'
    return kopf(n, '<div class="innen bh11-in"><div>%s%s</div>'
                   '<div class="bh11-haken sw" style="--i:2"><div class="bh11-pendel"><i class="bh11-nagel"></i><i class="bh11-schnur l"></i><i class="bh11-schnur r"></i><div class="bh11-tafel"><span class="etikett">Geöffnet</span>%s</div></div></div></div>' % (
        titel(), satz(), zeilen))
V.append(('Die Tafel an der Tür', 'Rechts hängt an einer Schnur die Tafel mit den Öffnungszeiten der ganzen Woche und pendelt beim Öffnen aus; links der Titel.', h11))

# 12 Grosses Bild, zwei kleine
V.append(('Grosses Bild, zwei kleine', 'Wand an Wand: links gross das Fenster von aussen, rechts übereinander Schild und Drink im Kerzenlicht; der Titel unten links.',
          lambda n: kopf(n, '<div class="bh12-raster">%s%s%s</div><div class="innen bh-unten bh12-text">%s%s</div>' % (
              bild('fb-fenster-aussen', 'bh12-gross', '64vw', '50% 50%'), bild('schild', 'bh12-a', '36vw', '50% 30%'), bild('glas-kerze', 'bh12-b', '36vw', '50% 55%'), titel(), satz()))))

# 13 Von 19 bis 2
def h13(n):
    st = [('19 Uhr', 'schild-ecke', '40% 40%'), ('21 Uhr', 'ft-theke-gaeste', None), ('23 Uhr', 'voll', '50% 50%'), ('1 Uhr', 'an-party-sw', '50% 40%'), ('2 Uhr', 'glas-kerze', '50% 55%')]
    zug = ''.join('<div class="bh13-st">%s<span class="etikett">%s</span></div>' % (bild(k, '', '34vw', p, j < 3), E(u)) for j, (u, k, p) in enumerate(st))
    return kopf(n, '<div class="innen bh13-oben">%s%s</div><div class="bh13-streifen"><div class="bh13-zug">%s</div></div>' % (titel(), satz(), zug))
V.append(('Von 19 bis 2', 'Unter dem Titel ein Streifen mit fünf Bildern vom Abend, 19 Uhr bis 2 Uhr; er läuft beim Scrollen seitwärts weiter.', h13))

# 14 Leuchtschrift
def h14(n):
    buch = ''.join('<span style="--b:%d">%s</span>' % (j, '&nbsp;' if c == ' ' else E(c)) for j, c in enumerate('Bis 2 Uhr.'))
    return kopf(n, bild('decke-raum', 'bh-voll bh14-raum', '100vw', '50% 55%') +
                '<div class="innen bh14-mitte"><h1 class="titel bh-t bh14-t" aria-label="Bis 2 Uhr.">%s</h1>%s</div>' % (buch, satz('', 3)))
V.append(('Leuchtschrift', 'Der Raum unter der Decke dunkel im Hintergrund; der Titel steht mittig und geht Buchstabe für Buchstabe an wie die Glühbirnen-Schrift.', h14))

# 15 Die Woche
def h15(n):
    woche = [('Mo', 0), ('Di', 0), ('Mi', 0), ('Do', 1), ('Fr', 1), ('Sa', 1), ('So', 0)]
    zeit = {'Do': '19–1', 'Fr': '19–2', 'Sa': '19–2'}
    tg = ''.join('<div class="%s" style="--j:%d"><b class="titel">%s</b><span>%s</span></div>' % ('an' if o else 'aus', j, t, zeit.get(t, 'zu')) for j, (t, o) in enumerate(woche))
    return kopf(n, '<div class="bh15-bild">%s</div><div class="innen bh15-in"><div>%s%s</div><div class="bh15-woche sw" style="--i:4">%s</div></div>' % (
        bild('fb-fenster-aussen', '', '50vw', '50% 50%'), titel(), satz(), tg))
V.append(('Die Woche', 'Unten die ganze Woche Montag bis Sonntag; Donnerstag, Freitag und Samstag gehen nacheinander golden an. Rechts oben das Fenster von aussen.', h15))

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
    print('00.html … 15.html in', ORD)
