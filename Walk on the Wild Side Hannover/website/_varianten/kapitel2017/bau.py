#!/usr/bin/env python3
"""Walk on the Wild Side · Startseite, Kapitel «Seit 2017 in Linden» ganz neu, als Anschluss an das Mosaik darüber (29.10.2026).
Jede Fassung = die echte index.html, nur dieses Kapitel getauscht. 00 = heute. Wechsel mit ← →.
Texte unverändert aus bau.kap_theke (belegt). Das Eröffnungsbild steht schon im Mosaik, deshalb hier nie."""
import os, re, sys, json, html
HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HIER, '..', '..'))
sys.path.insert(0, WEB)
import bau
ORD = '_varianten/kapitel2017'
V = '29107'
E = html.escape

JAHRE = [('2017', 'Eröffnung', 'Ende Oktober 2017 öffnen Christoph Elbert und Verena Schindler vom Restaurant 11A gegenüber die Bar und hängen das Gewölbe an die Decke. Freitag und Samstag ab 19 Uhr, dazu private Dinner an der langen Tafel.'),
         ('2023', 'Neu an der Ecke', 'Am 9. November 2023 machen Derya Ivkin und Momo Ben Khelifa die Bar wieder auf: ohne Karte, drei Abende die Woche, mit DJs und Konzerten. Seitdem heisst es Nachbarschafts-Mixology-Bar.'),
         ('2027', 'Falstaff', 'Im Falstaff Bar Guide 2027 steht das Wild Side mit 91 Punkten unter den Cocktailbars: 47 von 50 für die Drinks. Bei Google geben 75 Gäste im Schnitt 4,8 von 5.')]


def KOPF(cls='kopf17', i=0):
    return '<div class="%s">%s<h2 class="titel t-gross">%s</h2></div>' % (cls, bau.kz('21:00', 'Unter der Decke', i), bau.zl(['Seit 2017 in Linden.'], i0=i + 1))


def UEBER(hell):
    return bau.ueber('Gegen 23 Uhr wird es lauter.', hell)


def jb(n, cls='', ohne_zahl=False, stil=''):
    j, e, t = JAHRE[n]
    return '<div class="jb %s" style="--n:%d;%s">%s<span class="etikett">%s</span><p>%s</p></div>' % (
        cls, n, stil, '' if ohne_zahl else '<span class="jz">%s</span>' % j, e, E(t))


def w91(cls=''):
    return '<div class="w91 %s"><span class="jz">91</span><div><span class="etikett">Falstaff Bar Guide 2027</span><p>Cocktailbars, 47 von 50 Punkten für die Drinks.</p></div></div>' % cls


def fo(k, pos='50% 50%', sizes='40vw', cls='foto', stil=''):
    return bau.bild(k, cls, sizes, stil=stil, extra=' style="object-position:%s"' % pos)


def sec(n, cls, inhalt):
    return '<section class="k17 s%02d %s auf" id="seit2017">%s</section>' % (n, cls, inhalt)


# ---------------------------------------------------------------- die 15 Fassungen
def f01():  # Das Raster läuft weiter
    bilder = ''.join(fo(k, p, '25vw') for k, p in [('alt-theke', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('momo-flaschen', '50% 30%'), ('decke-hoch', '50% 30%')])
    zellen = jb(0) + jb(1) + jb(2) + '<div class="jb s01-91" style="--n:3"><span class="jz">91</span><span class="etikett">Falstaff Bar Guide 2027</span><p>Cocktailbars, 47 von 50 Punkten für die Drinks.</p></div>'
    return sec(1, '', '<div class="s01-bilder flaeche">%s</div><div class="hell s01-hell"><div class="innen">%s<div class="s01-zellen staffel">%s</div>%s</div></div>' % (
        bilder, KOPF(), zellen, UEBER(True)))


def f02():  # Schachbrett aus dem Mosaik
    z = lambda n: '<div class="s02-z hell">%s</div>' % jb(n)
    zellen = [fo('alt-theke', '50% 50%', '25vw'), z(0), fo('fb-2023-negroni', '50% 40%', '25vw'), z(1),
              z(2), fo('momo-flaschen', '50% 30%', '25vw'), '<div class="s02-z s02-nz">%s</div>' % w91('s02-w'), fo('alt-rueckbar', '50% 50%', '25vw')]
    return sec(2, 'dunkel', '<div class="innen">%s</div><div class="s02-brett flaeche">%s</div><div class="innen">%s</div>' % (KOPF(), ''.join(zellen), UEBER(False)))


def f03():  # Drei Hochformate mit grossen Jahren
    spalten = ''
    for n, (k, p) in enumerate([('alt-raum', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('momo-flaschen', '50% 30%')]):
        spalten += '<div class="s03-sp" style="--n:%d"><div class="s03-bild">%s<span class="s03-jahr">%s</span></div>%s</div>' % (
            n, fo(k, p, '30vw', 'kachel leise'), JAHRE[n][0], jb(n, ohne_zahl=True))
    return sec(3, 'hell', '<div class="innen">%s<div class="s03-reihe staffel">%s</div><i class="s03-linie"></i>%s%s</div>' % (
        KOPF(), spalten, w91('s03-91 sw'), UEBER(True)))


def f04():  # Damals und heute
    return sec(4, 'hell', '<div class="innen">%s<div class="s04-paar staffel">'
               '<figure style="--n:0">%s<figcaption class="etikett">Erste Website der Bar</figcaption></figure>'
               '<figure style="--n:1">%s<figcaption class="etikett">Heute</figcaption></figure></div>'
               '<div class="s04-jahre staffel">%s%s%s%s</div>%s</div>' % (
                   KOPF(), fo('alt-raum', '50% 50%', '46vw', 'kachel leise'), fo('decke-raum', '50% 40%', '46vw', 'kachel leise'),
                   jb(0), jb(1), jb(2), w91('s04-91'), UEBER(True)))


def f05():  # Stufen hinauf
    stufen = ''.join('<div class="s05-stufe" style="--n:%d">%s%s%s</div>' % (n, fo(k, p, '30vw', 'kachel leise'), jb(n), w91('s05-91') if n == 2 else '')
                     for n, (k, p) in enumerate([('alt-theke', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('momo-flaschen', '50% 30%')]))
    return sec(5, 'hell', '<div class="innen s05-innen">%s<div class="s05-treppe staffel">%s</div>%s</div>' % (KOPF('kopf17 s05-kopf'), stufen, UEBER(True)))


def f06():  # Ein Bild, drei Zeiten
    bilder = ''.join('<div class="s06-b" data-n="%d">%s</div>' % (n, bau.img_tag(k, '46vw', extra=' style="object-position:%s"' % p))
                     for n, (k, p) in enumerate([('alt-theke', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('momo-flaschen', '50% 30%')]))
    texte = ''.join('<div class="s06-txt" data-n="%d">%s%s</div>' % (n, jb(n, 'sw'), w91('s06-91') if n == 2 else '') for n in range(3))
    return sec(6, 'hell', '<div class="innen"><div class="s06-grid"><div class="s06-links"><div class="s06-rahmen" data-an="0">%s</div></div>'
               '<div class="s06-rechts">%s%s</div></div>%s</div>' % (bilder, KOPF('s06-kopf'), texte, UEBER(True)))


def f07():  # Auf der Theke
    karten = ''.join('<div class="s07-k hell" style="--n:%d">%s%s</div>' % (n, fo(k, p, '24vw'), jb(n))
                     for n, (k, p) in enumerate([('alt-theke', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('momo-flaschen', '50% 30%')]))
    karten += '<div class="s07-k s07-nz" style="--n:3">%s<div class="jb"><span class="jz">91</span><span class="etikett">Falstaff Bar Guide 2027</span><p>Cocktailbars, 47 von 50 Punkten für die Drinks.</p></div></div>' % fo('decke-hoch', '50% 30%', '24vw')
    return sec(7, 'dunkel', '<div class="innen">%s<div class="s07-theke"><div class="s07-karten">%s</div><i class="s07-tresen"></i></div>%s</div>' % (KOPF(), karten, UEBER(False)))


def f08():  # 91 als Fenster
    reihe = ''.join(fo(k, p, '31vw') for k, p in [('alt-rueckbar', '50% 50%'), ('fb-2020-bar', '50% 45%'), ('derya', '62% 40%')])
    liste = ''.join('<div class="s08-j" style="--n:%d"><span class="jz">%s</span><div><span class="etikett">%s</span><p>%s</p></div></div>' % (n, j, e, E(t)) for n, (j, e, t) in enumerate(JAHRE))
    return sec(8, 'dunkel', '<div class="innen"><div class="s08-oben"><div class="s08-links sw"><span class="s08-zahl">91</span>'
               '<span class="etikett">Falstaff Bar Guide 2027 · Cocktailbars</span></div><div class="s08-rechts">%s<div class="staffel">%s</div></div></div>'
               '<div class="s08-reihe flaeche">%s</div>%s</div>' % (KOPF('s08-kopf'), liste, reihe, UEBER(False)))


def f09():  # Das Bildband der Jahre
    band = ''.join('<div class="s09-b" style="flex-grow:%.3f">%s</div>' % (a, fo(k, p, '20vw')) for k, p, a in [
        ('alt-decke', '50% 50%', 1.333), ('alt-theke', '50% 50%', .75), ('fb-2020-bar', '50% 45%', 1.375),
        ('fb-2023-negroni', '50% 40%', .8), ('derya', '62% 40%', 1.511), ('momo-flaschen', '50% 30%', .75)])
    jahre = ''.join('<div class="s09-marke" style="--n:%d"><i></i><span class="jz">%s</span></div>' % (n, j) for n, (j, _, _) in enumerate(JAHRE))
    texte = ''.join(jb(n) for n in range(3))
    return sec(9, 'hell', '<div class="innen">%s</div><div class="s09-zeit"><i class="s09-linie"></i><div class="innen s09-marken staffel">%s</div></div>'
               '<div class="s09-band flaeche">%s</div><div class="innen"><div class="s09-texte staffel">%s</div>%s</div>' % (KOPF(), jahre, band, texte, UEBER(True)))


def f10():  # Der Zeitstrahl
    zeilen = ''
    for n, (k, p) in enumerate([('alt-raum', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('momo-flaschen', '50% 30%')]):
        bild = '<div class="s10-bild sw">%s</div>' % fo(k, p, '40vw', 'kachel leise')
        text = '<div class="s10-text sw" style="--i:1">%s%s</div>' % (jb(n), w91('s10-91') if n == 2 else '')
        zeilen += '<div class="s10-z%s"><i class="s10-marke"></i>%s</div>' % (' s10-um' if n % 2 else '', bild + text if n % 2 == 0 else text + bild)
    return sec(10, 'hell', '<div class="innen">%s<div class="s10-strahl" data-strahl><i class="s10-linie"></i>%s</div>%s</div>' % (KOPF(), zeilen, UEBER(True)))


def f11():  # Die Vitrine
    faecher = ''
    for n, (k, p) in enumerate([('alt-rueckbar', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('momo-flaschen', '50% 30%')]):
        j, e, t = JAHRE[n]
        faecher += '<div class="s11-fach" style="--n:%d"><span class="jz">%s</span><div class="jb"><span class="etikett">%s</span><p>%s</p></div>%s</div><i class="s11-licht" style="--n:%d"></i>' % (
            n, j, e, E(t), fo(k, p, '40vw', 'kachel leise'), n)
    faecher += '<div class="s11-fach" style="--n:3"><span class="jz s11-gold">91</span><div class="jb"><span class="etikett">Falstaff Bar Guide 2027</span><p>Cocktailbars, 47 von 50 Punkten für die Drinks.</p></div>%s</div>' % fo('decke-hoch', '50% 30%', '40vw', 'kachel leise')
    return sec(11, 'dunkel', '<div class="innen">%s<div class="s11-vitrine staffel">%s</div>%s</div>' % (KOPF(), faecher, UEBER(False)))


def f12():  # Das Fotobuch
    liste = ''.join('<div class="jahr" style="--n:%d"><span class="zahl">%s</span><span class="etikett">%s</span><p>%s</p></div>' % (n, j, e, E(t)) for n, (j, e, t) in enumerate(JAHRE))
    return sec(12, '', '<div class="s12-buch"><div class="s12-bild">%s<span class="etikett s12-unter">Erste Website der Bar</span></div>'
               '<div class="s12-seite hell">%s<div class="jahre staffel">%s</div>%s%s</div></div>' % (
                   fo('alt-raum', '50% 50%', '50vw'), KOPF('s12-kopf'), liste, w91('s12-91 sw'), UEBER(True)))


def f13():  # Ein Raum, drei Karten
    karten = ''.join('<div class="s13-k hell" style="--n:%d">%s</div>' % (n, jb(n)) for n in range(3)) + '<div class="s13-k s13-nz" style="--n:3">%s</div>' % (
        '<div class="jb"><span class="jz">91</span><span class="etikett">Falstaff Bar Guide 2027</span><p>Cocktailbars, 47 von 50 Punkten für die Drinks.</p></div>')
    return sec(13, 'hell', '<div class="s13-band">%s<div class="innen s13-kopf">%s</div></div><div class="innen"><div class="s13-karten staffel">%s</div>%s</div>' % (
        fo('decke-raum', '50% 32%', '100vw'), KOPF('kopf17'), karten, UEBER(True)))


def f14():  # Bildwand und Schild
    wand = ''.join(fo(k, p, '29vw') for k, p in [('alt-theke', '50% 50%'), ('alt-rueckbar', '50% 50%'), ('fb-2023-negroni', '50% 40%'), ('derya', '62% 40%')])
    liste = ''.join('<div class="s14-j" style="--n:%d"><span class="jz">%s</span><div><span class="etikett">%s</span><p>%s</p></div></div>' % (n, j, e, E(t)) for n, (j, e, t) in enumerate(JAHRE))
    return sec(14, 'hell', '<div class="innen"><div class="s14-grid"><div class="s14-wand flaeche">%s</div><div class="platte s14-schild sw">%s<div class="staffel">%s</div>%s</div></div>%s</div>' % (
        wand, KOPF('s14-kopf'), liste, w91('s14-91'), UEBER(True)))


def f15(alt):  # Wie heute, nur dichter
    paar = '<div class="s15-paar kachel sw" style="--i:2">%s%s</div>' % (fo('alt-theke', '50% 50%', '40vw'), fo('fb-2023-negroni', '50% 40%', '40vw'))
    kachel = '<div class="kachel leise sw" style="--i:2;--lq:url(%s)">%s</div>' % (bau.mache('decke-2017')['lq'], bau.img_tag('decke-2017', '40vw'))
    assert kachel in alt
    return alt.replace(kachel, paar).replace('<section class="kap hell auf" id="seit2017">', '<section class="kap hell auf s15" id="seit2017">')


FASSUNGEN = [(0, 'Heute', None), (1, 'Das Raster läuft weiter', f01), (2, 'Schachbrett aus dem Mosaik', f02), (3, 'Drei Hochformate, grosse Jahre', f03),
             (4, 'Damals und heute', f04), (5, 'Stufen hinauf', f05), (6, 'Ein Bild, drei Zeiten', f06), (7, 'Auf der Theke', f07),
             (8, '91 als Fenster', f08), (9, 'Das Bildband der Jahre', f09), (10, 'Der Zeitstrahl', f10), (11, 'Die Vitrine', f11),
             (12, 'Das Fotobuch', f12), (13, 'Ein Raum, drei Karten', f13), (14, 'Bildwand und Schild', f14), (15, 'Wie heute, nur dichter', f15)]
NAMEN = json.dumps([[n, name] for n, name, _ in FASSUNGEN], ensure_ascii=False)


def main():
    quelle = open(os.path.join(WEB, 'index.html')).read()
    m = re.search(r'<section class="kap hell auf" id="seit2017">.*?</section>', quelle, re.S)
    assert m
    for n, name, f in FASSUNGEN:
        neu = m.group(0) if f is None else (f(m.group(0)) if n == 15 else f())
        s = quelle[:m.start()] + neu + quelle[m.end():]
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
        s = s.replace('</head>', '<link rel="stylesheet" href="%s/k17.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s"></head>' % (ORD, V, ORD, V), 1)
        schild = '<p class="vschild" aria-hidden="true"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(FASSUNGEN) - 1, E(name))
        s = s.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD="%s"</script>'
                      '<script src="%s/varianten-nav.js?v=%s"></script><script src="%s/k17.js?v=%s" defer></script></body>' % (NAMEN, n, ORD, ORD, V, ORD, V), 1)
        if n == 0:
            s = s.replace('<body class="start">', '<body class="start null">', 1)
        open(os.path.join(HIER, '%02d.html' % n), 'w').write(s)
    print('%d Fassungen' % len(FASSUNGEN))


if __name__ == '__main__':
    main()
