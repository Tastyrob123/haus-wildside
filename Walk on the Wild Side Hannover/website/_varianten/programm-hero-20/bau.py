# Walk on the Wild Side · Unterseite Programm: 20 Fassungen für den Kopf «Lauter.» (30.10.2026).
# Robert: «Gib mir 20 verschiedene Visualisierungsmöglichkeiten für den Hero.» 00 = heute.
# Titel gross (am Desktop 120 px und mehr), Satz gut lesbar; Wortlaut wie heute, nur echte Fotos und Plakate der Bar, Abende aus LINEUP (bau.py),
# Wochentage aus der Seite selbst. Jede Fassung eigene Darstellung und eigene Bewegung, nur transform. Das Foto ist sofort da.
# Wechsel mit ← →. Aufruf: python3 _varianten/programm-hero-20/bau.py → 00.html … 20.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, mache, zl, LINEUP, V as BV

ORD = '_varianten/programm-hero-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('hero.css', 'hero.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('programm.html').read()
a = basis.index('<header class="sk auf" id="auftakt">')
b = basis.index('</header>', a) + len('</header>')

SATZ = 'Donnerstags spielt ab und zu jemand live, samstags legen DJs auf, und manchmal steht ein Gast aus einer anderen Bar neben Momo. Das Programm der Woche.'
PLAKATE = ['p-1710', 'p-0310', 'p-0509', 'p-1605', 'p-2103', 'p-2401', 'p-2211', 'p-0906']   # neuestes zuerst
WOCHE = [('Do', 'Donnerstag', 'Live, ab und zu', 'ab 20 Uhr'), ('Fr', 'Freitag', 'Momo an der Bar', 'bis 2 Uhr'), ('Sa', 'Samstag', 'Die DJ-Abende', '21 bis 1 Uhr')]


def bild(k, cls='', sizes='100vw', pos=None, sofort=True, stil=''):
    d = mache(k)
    ss = ', '.join('assets/bild/%s?v=%s %dw' % (f, BV, w) for w, f in d['stufen'])
    st = ' style="object-position:%s"' % pos if pos else ''
    lade = ' fetchpriority="high"' if sofort else ' loading="lazy"'
    return '<figure class="ph-f %s" style="--lq:url(%s);%s"><img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s%s></figure>' % (
        cls, d['lq'], stil, d['stufen'][-1][1], BV, ss, sizes, E(d['alt']), d['w'], d['h'], lade, st)


def url(k):
    return 'assets/bild/%s?v=%s' % (mache(k)['stufen'][-1][1], BV)


def titel(cls='', zeilen=('Lauter.',), i0=1):
    return '<h1 class="titel ph-t %s">%s</h1>' % (cls, zl(list(zeilen), i0=i0))


def satz(cls='', i=3):
    return '<p class="text sw ph-s %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def kopf(n, inner, cls=''):
    return '<header class="sk-v auf ph ph%02d %s" id="auftakt" data-v="%d">%s</header>' % (n, cls, n, inner)


V = []
# 01
V.append(('Es wird lauter', 'Die Sängerin über den ganzen Schirm; der Titel wächst beim Öffnen von klein auf riesig.',
          lambda n: kopf(n, bild('saengerin-sw', 'ph-voll', '100vw', '50% 30%') + '<div class="innen ph-unten"><div class="ph01-wachs">%s</div>%s</div>' % (titel(), satz()))))
# 02
def h02(n):
    balken = ''.join('<i style="--h:%.2f;--d:%.2fs"></i>' % (h, d) for h, d in
                     [(.35, 0), (.7, .3), (.5, .1), (.95, .45), (.6, .2), (.82, .55), (.4, .05), (.66, .35), (.9, .15), (.48, .5), (.74, .25), (.3, .4)])
    return kopf(n, '<div class="innen ph02-in"><div>%s%s</div><div class="ph02-rechts sw" style="--i:2">%s<div class="ph02-pegel" aria-hidden="true">%s</div></div></div>' % (
        titel(), satz(), bild('konzert-love', '', '45vw', '50% 40%'), balken))
V.append(('Der Pegel', 'Links der Titel, rechts das Duo vor den Glühbirnen-Buchstaben; am unteren Rand schlägt ein goldener Pegel im Takt.', h02))
# 03
def h03(n):
    wand = ''.join(bild(k, '', '20vw', None, j < 4, '--d:%d' % j) for j, k in enumerate(PLAKATE))
    return kopf(n, '<div class="ph03-wand">%s</div><div class="ph03-band"><div class="innen">%s%s</div></div>' % (wand, titel(), satz()))
V.append(('Die Plakatwand', 'Alle acht SESSION-Plakate Kante an Kante als Wand, sie richten sich nacheinander auf; quer darüber ein dunkles Band mit dem Titel.', h03))
# 04
def h04(n):
    spalten = ''.join('<div class="ph04-sp">%s<div class="ph04-tag"><b class="titel">%s</b><span>%s</span><small>%s</small></div></div>' % (
        bild(k, '', '34vw', p), E(kurz), E(was), E(zeit)) for (kurz, _, was, zeit), k, p in zip(WOCHE, ['konzert-love', 'momo-lacht', 'p-1710'], ['50% 40%', '58% 40%', '50% 40%']))
    return kopf(n, '<div class="ph04-drei">%s</div><div class="innen ph04-oben">%s%s</div>' % (spalten, titel(), satz()))
V.append(('Drei Abende, drei Bilder', 'Donnerstag, Freitag, Samstag als drei hohe Bilder nebeneinander, jedes mit seinem Abend; der Titel oben über allen.', h04))
# 05
V.append(('Die Bühne', 'Das Duo mit den Glühbirnen-Buchstaben über den ganzen Schirm, die Kamera fährt langsam zurück; Titel mittig, riesig.',
          lambda n: kopf(n, bild('konzert-love', 'ph-voll', '100vw', '50% 35%') + '<div class="innen ph05-mitte">%s%s</div>' % (titel(), satz()))))
# 06
def h06(n):
    return kopf(n, '<div class="innen ph06-in"><div>%s%s<p class="ph06-jetzt sw" style="--i:4"><span class="etikett">Zuletzt aufgelegt</span>%s · %s</p></div>'
                   '<div class="ph06-platte sw" style="--i:2"><div class="ph06-dreh">%s<i class="ph06-loch"></i></div></div></div>' % (
        titel(), satz(), E(LINEUP[0][1]), E(LINEUP[0][0]), bild('p-1710', '', '40vw', '50% 45%')))
V.append(('Die Platte dreht sich', 'Rechts dreht sich das letzte Plakat als runde Schallplatte mit Rillen, links der Titel und wer zuletzt aufgelegt hat.', h06))
# 07
V.append(('Dreimal lauter', 'Kein Foto: das Wort dreimal untereinander, jede Zeile grösser als die davor, und jede schwingt kurz nach.',
          lambda n: kopf(n, '<div class="innen ph07-in"><p class="ph07-echo titel" aria-hidden="true"><span style="--i:0">Lauter.</span><span style="--i:1">Lauter.</span></p>%s%s</div>' % (titel('', ('Lauter.',), 2), satz('', 4)))))
# 08
V.append(('Zwei Abende', 'Links die Sängerin, rechts das Duo, Kante an Kante; der Titel liegt über der Naht und die zwei Hälften schieben sich zusammen.',
          lambda n: kopf(n, '<div class="ph08-zwei">%s%s</div><div class="innen ph08-mitte">%s%s</div>' % (
              bild('saengerin', 'ph08-l', '50vw', '50% 30%'), bild('konzert-love', 'ph08-r', '50vw', '50% 40%'), titel(), satz()))))
# 09
def h09(n):
    zeilen = ''.join('<div><span>%s</span><b>%s</b><small>%s</small></div>' % (E(d), E(nm), E(r)) for d, nm, r, _ in LINEUP)
    return kopf(n, '<div class="innen ph09-in"><div>%s%s</div><div class="ph09-liste sw" style="--i:2"><span class="etikett">Die Abende bisher</span><div class="ph09-fenster"><div class="ph09-zug">%s%s</div></div></div></div>' % (
        titel(), satz(), zeilen, zeilen))
V.append(('Die Setliste', 'Links der Titel, rechts laufen alle DJ-Abende seit 2025 langsam nach oben durch, Datum, Name und Musik.', h09))
# 10
def h10(n):
    namen = '<i>·</i>'.join('<span>%s</span>' % E(nm) for nm in dict.fromkeys(x[1] for x in LINEUP))
    return kopf(n, bild('voll', 'ph-voll', '100vw', '50% 55%') + '<div class="ph10-band" aria-hidden="true"><div class="ph10-zug titel">%s<i>·</i>%s<i>·</i></div></div><div class="innen ph-unten">%s%s</div>' % (
        namen, namen, titel(), satz()))
V.append(('Die Namen laufen', 'Über dem vollen Abend läuft quer ein Band mit allen Namen, die hier aufgelegt haben; darunter der Titel.', h10))
# 11
V.append(('Das Mikrofon schwebt', 'Titel links riesig, rechts die Sängerin in einer hohen runden Form, die leicht auf und ab schwebt.',
          lambda n: kopf(n, '<div class="innen ph11-in"><div>%s%s</div><div class="ph11-kapsel sw" style="--i:2">%s</div></div>' % (titel(), satz(), bild('saengerin', '', '36vw', '50% 25%')))))
# 12
V.append(('Das Plakat kippt', 'Titel links, rechts das letzte SESSION-Plakat gross als Karte, die sich mit der Maus leicht neigt.',
          lambda n: kopf(n, '<div class="innen ph12-in"><div>%s%s</div><div class="ph12-karte sw" style="--i:2" data-kipp>%s</div></div>' % (titel(), satz(), bild('p-1710', '', '42vw')))))
# 13
V.append(('Der Ton geht raus', 'Die Sängerin über den ganzen Schirm; vom Mikrofon laufen feine goldene Ringe nach aussen.',
          lambda n: kopf(n, bild('saengerin-sw', 'ph-voll', '100vw', '50% 30%') + '<div class="ph13-ringe" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="innen ph-unten">%s%s</div>' % (titel(), satz()))))
# 14
V.append(('Tiefe beim Scrollen', 'Der volle Abend über den ganzen Schirm; beim Scrollen bleibt das Foto zurück und der Titel zieht schneller nach oben.',
          lambda n: kopf(n, '<div class="ph14-tief">%s</div><div class="innen ph-unten ph14-vorn">%s%s</div>' % (bild('silvester', 'ph-voll', '100vw', '50% 45%'), titel(), satz()))))
# 15
def h15(n):
    stapel = ''.join(bild(k, 'ph15-b' + (' an' if j == 0 else ''), '40vw', None, j < 2) for j, k in enumerate(PLAKATE[:6]))
    return kopf(n, '<div class="innen ph15-in"><div>%s%s<p class="ph15-name sw" style="--i:4"><span class="etikett">SESSION</span><b data-namen=\'%s\'>%s</b></p></div><div class="ph15-stapel sw" style="--i:2">%s</div></div>' % (
        titel(), satz(), json.dumps([x[1] + ' · ' + x[0] for x in LINEUP[:6]], ensure_ascii=False).replace("'", '&#39;'), E(LINEUP[0][1] + ' · ' + LINEUP[0][0]), stapel))
V.append(('Die Plakate blättern', 'Rechts ein Stapel Plakate, alle drei Sekunden schiebt sich das nächste nach oben weg; darunter steht, wer aufgelegt hat.', h15))
# 16
V.append(('Der Streifen', 'Drei Fotos als breiter Streifen, der beim Scrollen seitwärts weiterläuft; der Titel steht darüber.',
          lambda n: kopf(n, '<div class="innen ph16-oben">%s%s</div><div class="ph16-streifen"><div class="ph16-zug">%s%s%s%s</div></div>' % (
              titel(), satz(), bild('konzert-love', '', '40vw'), bild('saengerin', '', '40vw', '50% 30%'), bild('voll', '', '40vw', None, False), bild('gast-musa', '', '40vw', None, False)))))
# 17
def h17(n):
    tage = ''.join('<div class="sw" style="--i:%d"><b class="titel">%s</b><span>%s</span><small>%s</small></div>' % (j + 3, E(lang), E(was), E(zeit)) for j, (_, lang, was, zeit) in enumerate(WOCHE))
    return kopf(n, bild('konzert', 'ph-voll', '100vw', '50% 45%') + '<div class="innen ph17-in"><div>%s%s</div><div class="ph17-tafel">%s</div></div>' % (titel(), satz(), tage))
V.append(('Die Wochentafel', 'Das Konzert dunkel im Hintergrund, links der Titel, rechts die drei Abende untereinander in grosser Schrift.', h17))
# 18
V.append(('Grosses Bild, zwei kleine', 'Links gross die Sängerin, rechts übereinander das Duo und ein Plakat, Wand an Wand; der Titel unten links über dem grossen Bild.',
          lambda n: kopf(n, '<div class="ph18-raster">%s%s%s</div><div class="innen ph-unten ph18-text">%s%s</div>' % (
              bild('saengerin-sw', 'ph18-gross', '62vw', '50% 30%'), bild('konzert-love', 'ph18-a', '38vw', '50% 40%'), bild('p-0310', 'ph18-b', '38vw', '50% 30%'), titel(), satz()))))
# 19
V.append(('Das Foto in der Schrift', 'Das Wort riesig über die ganze Breite auf Nacht; in den Buchstaben die Sängerin im Fensterlicht, das Bild wandert langsam mit.',
          lambda n: kopf(n, '<div class="innen ph19-in"><h1 class="titel ph-t ph19-t"><span class="ph19-foto" style="background-image:url(%s)">Lauter.</span></h1>%s</div>' % (url('saengerin'), satz('', 2)))))
# 20
def h20(n):
    gaeste = ['gast-musa', 'gast-havn', 'gast-nils', 'gast-cold', 'gast-enlil']
    return kopf(n, '<div class="ph20-reihe">%s</div><div class="innen ph20-text">%s%s</div>' % (
        ''.join(bild(k, '', '20vw', None, j < 3, '--j:%d' % j) for j, k in enumerate(gaeste)), titel(), satz()))
V.append(('Gäste hinter der Bar', 'Fünf Gäste aus anderen Bars als Reihe hoher Bilder, sie fallen nacheinander herein; der Titel liegt unten quer über allen.', h20))

assert len(V) == 20
LISTE = [[0, 'Heute']] + [[j + 1, nm] for j, (nm, _, _) in enumerate(V)]
KOPF = '<link rel="stylesheet" href="%s/hero.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, kopfhtml, name):
    h = basis[:a] + kopfhtml + basis[b:] if nr else basis
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 20</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/hero.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, '', 'Heute'))
    for j, (name, _, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 20.html in', ORD)
