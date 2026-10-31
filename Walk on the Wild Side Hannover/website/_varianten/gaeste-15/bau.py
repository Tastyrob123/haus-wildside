# Walk on the Wild Side · Programm-Seite, Abschnitt «Gäste hinterm Tresen · Jemand anderes am Shaker.» (id="gaeste"): 15 Darstellungen (30.10.2026).
# Robert: «gib mir bitte für den Abschnitt auch 15 verschiedene Visualisierungsmöglichkeiten». 00 = heutiger Stand.
# Je Fassung eine eigene Darstellung und eine eigene Bewegung, keine aus session-15 wiederholt. Texte Wort für Wort aus unter.programm(), nur die echten Fotos.
# Bewegung nur über transform und opacity, ein Scroll-Takt in g.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/gaeste-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/gaeste-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('g.css', 'g.js', 'nav.js'))))

TEXT = 'An manchen Abenden steht neben Momo jemand aus einer anderen Bar, aus Hannover oder Berlin, und bringt eigene Drinks mit. Fünf Gastschichten aus dem Jahr 2024.'
GAESTE = [('gast-musa', '02.03.2024', 'Musa', 'Rebe & Brot, Hannover. Mit Momo hinter der Bar.'),
          ('gast-havn', '09.03.2024', 'Aus dem Havn', 'Eine Bartenderin aus dem Havn in Hannover, mit Momo.'),
          ('gast-nils', '20.04.2024', 'Nils Lutterbach', 'Lovis, Berlin. Vier Signature Drinks mit Freimeister Kollektiv.'),
          ('gast-cold', '25.05.2024', 'Cold Drinks and More', 'Ein alter Bekannter aus Berlin mit fünf eigenen Drinks.'),
          ('gast-enlil', '19.10.2024', 'Enlil Arevalo', 'Ein Name der Barszene in Hannover, fünf Signature Drinks.')]
STADT = {'gast-musa': 'Hannover', 'gast-havn': 'Hannover', 'gast-nils': 'Berlin', 'gast-cold': 'Berlin', 'gast-enlil': 'Hannover'}   # aus den Sätzen
_q = open('unter.py').read()
assert TEXT in _q, 'Text weicht ab'
for _k, _d, _t, _s in GAESTE:
    assert "('%s', '%s', '%s', '%s')" % (_k, _d, _t, _s) in _q, 'Gast weicht ab: ' + _t
MONATE = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']


def kopf(rechts='', cls=''):
    return '<div class="gq-kopf %s"><div class="gq-kopf-l">%s%s<p class="text sw" style="--i:1">%s</p></div>%s</div>' % (
        cls, B.kz('Gäste hinterm Tresen', 'Gastschichten', 0), B.h2(['Jemand anderes', 'am Shaker.']), E(TEXT), rechts)


def fo(k, sizes, cls='', stil='', extra=''):
    return '<figure class="gf %s" style="--lq:url(%s);%s"%s>%s</figure>' % (cls, mache(k)['lq'], stil, extra, B.img_tag(k, sizes))


def satz(d, t, s, cls='g-satz'):
    return '<div class="%s"><span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p></div>' % (cls, E(d), E(t), E(s))


def sek(n, inner, innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf gq g%02d" id="gaeste" data-g="%d">%s</section>' % (n, n, i)


V = []


# 01 · Der Schichtplan: wie der Dienstplan hinter der Bar. Je Gast eine Zeile: Datum gross, Name, woher, rechts ein schmales Porträt.
# Die Zeilen werden nacheinander eingetragen: jede steigt auf, dann schiebt sich ihr Bild aus der Zeile nach oben.
def v01(n):
    z = ''.join('<div class="s1-z" style="--n:%d"><span class="s1-dat titel">%s</span><div><h3 class="titel">%s</h3><p>%s</p></div><div class="s1-fen">%s</div></div>' % (
        j, E(d), E(t), E(s), fo(k, '(max-width:760px) 30vw, 14vw')) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="s1-plan vauf"><p class="s1-kopf"><span>Datum</span><span>Am Shaker</span><span></span></p>%s</div>' % z)
V.append(('Der Schichtplan', v01))


# 02 · Die Tresenkante: alle fünf stehen nebeneinander wie hinter der Bar, vorn läuft eine durchgehende Kante aus Gold mit den Namen.
# Erst zieht sich die Kante von links nach rechts, dann treten die fünf dahinter hoch.
def v02(n):
    b = ''.join('<div class="s2-p" style="--n:%d">%s</div>' % (j, fo(k, '(max-width:760px) 40vw, 19vw')) for j, (k, d, t, s) in enumerate(GAESTE))
    nm = ''.join('<div class="s2-n" style="--n:%d"><span>%s</span><b class="titel">%s</b><p>%s</p></div>' % (j, E(d), E(t), E(s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="s2-bar vauf"><div class="s2-reihe">%s</div><div class="s2-kante"><i></i><div class="s2-namen">%s</div></div></div>' % (b, nm))
V.append(('Die Tresenkante', v02))


# 03 · Verstreut im Raum: die fünf Porträts in verschiedenen Grössen über die Fläche verteilt, jedes mit seinem Satz.
# Beim Scrollen ziehen sie verschieden schnell, die grossen langsamer, die kleinen schneller: Tiefe ohne Bühne.
def v03(n):
    lage = [(0, 0, 28, -.10), (35, 11, 22, .18), (66, 2, 26, -.05), (6, 54, 22, .22), (44, 58, 27, -.12)]
    p = ''.join('<article class="s3-p" style="left:%s%%;top:%s%%;width:%s%%" data-v="%s">%s%s</article>' % (
        x, y, w, v, fo(k, '(max-width:760px) 80vw, 30vw'), satz(d, t, s)) for (k, d, t, s), (x, y, w, v) in zip(GAESTE, lage))
    return sek(n, kopf() + '<div class="s3-feld">%s</div>' % p)
V.append(('Verstreut im Raum', v03))


# 04 · Die Visitenkarten: jeder Gast als cremefarbene Karte im Querformat, Porträt links, Name und Bar rechts.
# Die Karten werden leicht schief auf den Tresen gelegt: kommen von oben, drehen sich und liegen still. Zeigen hebt eine an.
def v04(n):
    c = ''.join('<article class="s4-k" style="--n:%d;--w:%s">%s<div><span>%s</span><h3 class="titel">%s</h3><p>%s</p></div></article>' % (
        j, w, fo(k, '(max-width:760px) 30vw, 11vw'), E(d), E(t), E(s)) for j, ((k, d, t, s), w) in enumerate(zip(GAESTE, (-4, 3, -2, 4, -3))))
    return sek(n, kopf() + '<div class="s4-tisch vauf">%s</div>' % c)
V.append(('Die Visitenkarten', v04))


# 05 · Einer nach dem anderen: die Bühne steht, je Gast ein Scrollschritt. Das Porträt des nächsten schiebt sich von unten
# über das vorige, links wechselt der Name in grosser Schrift. Unten zählt ein feiner Strich die fünf Schichten.
def v05(n):
    b = ''.join('<div class="s5-b" style="--n:%d">%s</div>' % (j, fo(k, '(max-width:760px) 80vw, 36vw')) for j, (k, d, t, s) in enumerate(GAESTE))
    t_ = ''.join('<div class="s5-t" style="--n:%d"><span class="etikett">%s</span><p class="s5-name titel">%s</p><p class="s5-s">%s</p></div>' % (j, E(d), E(t), E(s)) for j, (k, d, t, s) in enumerate(GAESTE))
    zaehl = ''.join('<i></i>' for _ in GAESTE)
    return sek(n, '<div class="innen">%s</div><div class="s5-pin" data-pin><div class="s5-buehne"><div class="innen s5-raster"><div class="s5-texte">%s<div class="s5-zaehl">%s</div></div><div class="s5-bilder">%s</div></div></div></div>' % (
        kopf(), t_, zaehl, b), innen=False)
V.append(('Einer nach dem anderen', v05))


# 06 · Das Gästebuch: eine aufgeschlagene Seite mit Linien, je Gast ein Eintrag mit Datum, Name und Satz,
# daneben das Foto mit einem Streifen Klebeband. Die Einträge erscheinen Zeile für Zeile, als würden sie geschrieben.
def v06(n):
    e = ''.join('<div class="s6-e" style="--n:%d">%s<div><span>%s</span><h3 class="titel">%s</h3><p>%s</p></div></div>' % (
        j, fo(k, '(max-width:760px) 24vw, 9vw', 's6-foto', '--w:%sdeg' % w), E(d), E(t), E(s)) for j, ((k, d, t, s), w) in enumerate(zip(GAESTE, (-3, 2, -2, 3, -1))))
    return sek(n, kopf() + '<div class="s6-buch vauf"><p class="s6-titel titel">Gäste hinterm Tresen, 2024</p>%s</div>' % e)
V.append(('Das Gästebuch', v06))


# 07 · Der Blick wandert: alle fünf in einer Reihe; wer gerade in der Bildmitte steht, tritt etwas vor und wird hell,
# die anderen treten zurück. Gesteuert vom Scrollen, kein Klick nötig.
def v07(n):
    p = ''.join('<article class="s7-p">%s%s</article>' % (fo(k, '(max-width:760px) 70vw, 22vw'), satz(d, t, s)) for k, d, t, s in GAESTE)
    return sek(n, kopf() + '<div class="s7-reihe" data-blick>%s</div>' % p)
V.append(('Der Blick wandert', v07))


# 08 · Hannover und Berlin: zwei Spalten, links die Gäste aus Hannover, rechts die aus Berlin, getrennt von einer Goldlinie,
# die beim Auftritt von oben nach unten wächst. Die Stadt steht gross über jeder Spalte.
def v08(n):
    def spalte(st):
        return '<div class="s8-sp"><p class="s8-stadt titel">%s</p>%s</div>' % (st, ''.join(
            '<article class="s8-p" style="--n:%d">%s%s</article>' % (j, fo(k, '(max-width:760px) 40vw, 14vw'), satz(d, t, s)) for j, (k, d, t, s) in enumerate(g for g in GAESTE if STADT[g[0]] == st)))
    return sek(n, kopf() + '<div class="s8-zwei vauf">%s<i class="s8-linie"></i>%s</div>' % (spalte('Hannover'), spalte('Berlin')))
V.append(('Hannover und Berlin', v08))


# 09 · Das Jahr 2024: eine Monatsleiste von Januar bis Dezember, die Gäste hängen an feinen Fäden unter ihrem Monat.
# Die Leiste läuft beim Auftritt durch, dann fallen die Bilder an ihren Fäden herunter und pendeln aus.
def v09(n):
    leiste = ''.join('<span class="%s">%s</span>' % ('voll' if any(int(d[3:5]) == m + 1 for k, d, t, s in GAESTE) else '', nm) for m, nm in enumerate(MONATE))
    pos = []
    for k, d, t, s in GAESTE:
        m = int(d[3:5]) - 1 + int(d[:2]) / 31
        pos.append(m)
    h = ''.join('<article class="s9-p" style="--x:%.2f%%;--f:%dpx;--n:%d"><i class="s9-faden"></i>%s%s</article>' % (
        (x / 12) * 100, (30, 380, 30, 380, 30)[j], j, fo(k, '(max-width:760px) 30vw, 11vw'), satz(d, t, s)) for j, ((k, d, t, s), x) in enumerate(zip(GAESTE, pos)))
    return sek(n, kopf() + '<div class="s9-jahr vauf"><div class="s9-leiste">%s</div><div class="s9-haenge">%s</div></div>' % (leiste, h))
V.append(('Das Jahr 2024', v09))


# 10 · Die Namen gross: links die fünf Namen in Titelschrift untereinander, rechts ein grosses Porträt.
# Zeigen auf einen Namen öffnet sein Bild wie ein Rollo von unten nach oben; der Satz steht unter dem Namen.
def v10(n):
    nm = ''.join('<div class="s10-n%s" data-i="%d"><span>%s</span><h3 class="titel">%s</h3><p>%s</p></div>' % (' an' if j == 0 else '', j, E(d), E(t), E(s)) for j, (k, d, t, s) in enumerate(GAESTE))
    b = ''.join('<div class="s10-b%s">%s</div>' % (' an' if j == 0 else '', fo(k, '(max-width:760px) 80vw, 34vw')) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="s10-raster vauf"><div class="s10-namen">%s</div><div class="s10-bild">%s</div></div>' % (nm, b))
V.append(('Die Namen gross', v10))


# 11 · Das Bild bleibt stehen: links steht das Porträt fest im Bild, rechts ziehen Datum, Name und Satz der fünf vorbei.
# Wer gerade in der Mitte ist, dessen Bild steht links; es wechselt mit einem kurzen Zoom von 1,06 auf 1.
def v11(n):
    b = ''.join('<div class="s11-b%s">%s</div>' % (' an' if j == 0 else '', fo(k, '(max-width:760px) 80vw, 38vw')) for j, (k, d, t, s) in enumerate(GAESTE))
    t_ = ''.join('<article class="s11-t"><span class="s11-dat titel">%s</span><h3 class="titel">%s</h3><p>%s</p></article>' % (E(d), E(t), E(s)) for k, d, t, s in GAESTE)
    return sek(n, kopf() + '<div class="s11-raster" data-steh><div class="s11-links"><div class="s11-bild">%s</div></div><div class="s11-rechts">%s</div></div>' % (b, t_))
V.append(('Das Bild bleibt stehen', v11))


# 12 · Das Namensschild: fünf hohe Porträts, unter jedem ein Schild aus Messing mit dem Namen wie an der Schürze.
# Die Schilder klappen beim Auftritt von oben herunter, eins nach dem anderen.
def v12(n):
    p = ''.join('<article class="s12-p" style="--n:%d">%s<div class="s12-schild"><b class="titel">%s</b><span>%s</span></div><p>%s</p></article>' % (
        j, fo(k, '(max-width:760px) 70vw, 20vw'), E(t), E(d), E(s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="s12-reihe vauf">%s</div>' % p)
V.append(('Das Namensschild', v12))


# 13 · Wand an Wand im Versatz: fünf Porträts über die ganze Breite ohne Abstand, darunter je ein Satz.
# Beim Scrollen gleiten die Spalten verschieden weit, die Reihe wird zur Treppe und wieder gerade.
def v13(n):
    p = ''.join('<article class="s13-p" data-v="%s">%s%s</article>' % (v, fo(k, '(max-width:760px) 50vw, 20vw'), satz(d, t, s)) for (k, d, t, s), v in zip(GAESTE, (.0, .12, .24, .12, .0)))
    return sek(n, '<div class="innen">%s</div><div class="s13-wand" data-versatz>%s</div>' % (kopf(), p), innen=False)
V.append(('Wand an Wand im Versatz', v13))


# 14 · Bild im Satz: die Namen in grosser Titelschrift über die ganze Breite, mitten in jeder Zeile ein kleines Porträt wie ein Wort.
# Die Zeilen steigen nacheinander auf, das Bild darin öffnet sich danach von der Mitte aus.
def v14(n):
    z = ''.join('<div class="s14-z" style="--n:%d"><span class="s14-dat">%s</span><p class="s14-name titel">%s %s</p><p class="s14-s">%s</p></div>' % (
        j, E(d), E(t), '<span class="gf s14-wort" style="--lq:url(%s)">%s</span>' % (mache(k)['lq'], B.img_tag(k, '12vw')), E(s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="s14-liste vauf">%s</div>' % z)
V.append(('Bild im Satz', v14))


# 15 · Die Treppe: die fünf Schichten steigen wie Stufen von links unten nach rechts oben, 2024 von März bis Oktober.
# Eine Goldlinie zeichnet die Stufen nach; jede Stufe tritt beim Scrollen einzeln auf, von unten.
def v15(n):
    p = ''.join('<article class="s15-p" style="--n:%d">%s%s<i class="s15-stufe"></i></article>' % (j, fo(k, '(max-width:760px) 60vw, 15vw'), satz(d, t, s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="s15-treppe">%s</div>' % p)
V.append(('Die Treppe', v15))


def seite(n):
    h = unter.programm()
    if n:
        a = h.rfind('<section', 0, h.find('id="gaeste"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/g.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/g.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
