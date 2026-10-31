# Walk on the Wild Side · Feiern-Seite, Abschnitt «Grosse Events · Grösser als die Bar.» (id="events"): 15 weitere Darstellungen (30.10.2026).
# Robert: «gib nochmal 15 visuelle alternative darstellungen von dem abschnitt». 00 = heutiger Stand (Fassung 10 aus events-15, Abzüge fächern auf).
# Keine Darstellung aus events-15 wiederholt. Texte Wort für Wort aus unter.tafel(), nur die drei echten Fotos (Theke, Loge, Gläser).
# Bildgrenzen: an-loge 590 px, an-glaeser 656 px, ev-theke 832 px breit, nie grösser als ~80 % davon zeigen.
# Auftritte nur über transform, alles ab dem ersten Bild deckend. Ein Scroll-Takt in x.js.
# Aufruf: python3 _varianten/events-15b/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/events-15b'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('x.css', 'x.js', 'nav.js'))))

TEXT = 'Für grössere Veranstaltungen zieht die Bar um, in externe Locations wie die Loge. Derya und Momo übernehmen die Organisation und kümmern sich um das ganze Konzept, von der Bar bis zum Ablauf des Abends.'
assert TEXT in open('unter.py').read(), 'Text weicht ab'
TH, LO, GL = 'ev-theke', 'an-loge', 'an-glaeser'


def kz():
    return B.kz('Grosse Events', 'Ausser Haus', 0)


def h2():
    return B.h2(['Grösser als', 'die Bar.'])


def rest(i=1):
    return '<p class="text sw" style="--i:%d">%s</p><p class="fr-klein sw" style="--i:%d">Infos auf Anfrage.</p><div class="knoepfe sw" style="--i:%d;margin-top:26px">%s</div>' % (
        i, E(TEXT), i + 1, i + 2, B.knopf('Event anfragen', '#anfragen'))


def text(cls=''):
    return '<div class="xe-t %s">%s%s%s</div>' % (cls, kz(), h2(), rest())


def kopf2():
    return '<div class="xe-k2"><div>%s%s</div><div>%s</div></div>' % (kz(), h2(), rest())


def fo(k, sizes, cls='', stil='', pos='50% 50%'):
    return '<figure class="xf %s" style="--lq:url(%s);%s">%s</figure>' % (
        cls, mache(k)['lq'], stil, B.img_tag(k, sizes, extra=' style="object-position:%s"' % pos))


def sek(n, inner, innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf xq x%02d" id="events" data-x="%d">%s</section>' % (n, n, i)


S3 = '(max-width:760px) 80vw, 28vw'
V = []


# 01 · Das Band: oben Titel und Satz in zwei Spalten, darunter drei Bilder in einer Reihe.
# Hinter den Bildern zieht sich ein cremefarbenes Band über die ganze Breite, dann steigen die drei darauf.
def v01(n):
    b = ''.join('<div class="b1-p" style="--n:%d">%s</div>' % (j, fo(k, S3)) for j, k in enumerate((TH, LO, GL)))
    return sek(n, kopf2() + '<div class="b1-feld vauf"><i class="b1-band"></i><div class="b1-reihe">%s</div></div>' % b)
V.append(('Das Band', v01))


# 02 · Das Tischkärtchen: links die Theke hoch, daneben Loge und Gläser übereinander, rechts der Text auf einer cremefarbenen Karte,
# die sich beim Auftritt aus dem Liegen aufstellt wie ein Platzkärtchen auf der Tafel.
def v02(n):
    return sek(n, '<div class="t2-raster vauf"><div class="t2-bilder">%s%s%s</div><div class="t2-stand"><div class="t2-karte hell">%s</div></div></div>' % (
        fo(TH, '(max-width:760px) 60vw, 22vw', 't2-a'), fo(LO, '(max-width:760px) 40vw, 14vw', 't2-b'), fo(GL, '(max-width:760px) 40vw, 14vw', 't2-c'), text()))
V.append(('Das Tischkärtchen', v02))


# 03 · Die Bogenfenster: drei hohe Fenster mit rundem Bogen oben, wie die Fenster eines Saals. Darüber Titel und Satz.
# Jedes Fenster steigt aus seiner Fensterbank nach oben, eins nach dem anderen.
def v03(n):
    f = ''.join('<div class="f3-fenster" style="--n:%d"><div class="f3-innen">%s</div></div>' % (j, fo(k, S3)) for j, k in enumerate((TH, LO, GL)))
    return sek(n, kopf2() + '<div class="f3-reihe vauf">%s</div>' % f)
V.append(('Die Bogenfenster', v03))


# 04 · Bilder in der Überschrift: der Titel steht riesig über die ganze Breite, zwischen den Worten sitzen die drei Fotos als kleine Felder.
# Die Worte steigen aus der Zeile, die Fotos wachsen aus der Mitte auf ihre Grösse.
def v04(n):
    def bi(k, j):
        return '<span class="i4-bild" style="--n:%d;--lq:url(%s)" aria-hidden="true">%s</span>' % (j, mache(k)['lq'], B.img_tag(k, '(max-width:760px) 30vw, 14vw'))
    def w(t, j):
        return '<span class="i4-w"><span style="--n:%d">%s</span></span>' % (j, t)
    t = '<h2 class="titel i4-titel" aria-label="Grösser als die Bar."><span class="i4-z">%s %s %s</span><span class="i4-z">%s %s %s %s</span></h2>' % (
        w('Grösser', 0), bi(TH, 0), w('als', 1), w('die', 2), bi(LO, 1), w('Bar.', 3), bi(GL, 2))
    unten = '<p class="text sw" style="--i:1">%s</p><div><p class="fr-klein sw" style="--i:2">Infos auf Anfrage.</p><div class="knoepfe sw" style="--i:3;margin-top:22px">%s</div></div>' % (E(TEXT), B.knopf('Event anfragen', '#anfragen'))
    return sek(n, '<div class="i4-ganz vauf">%s%s<div class="i4-unten">%s</div></div>' % (kz(), t, unten))
V.append(('Bilder in der Überschrift', v04))


# 05 · Wand an Wand: die drei Fotos stossen ohne Lücke aneinander wie ein einziges Bild über die ganze Breite, darunter Titel und Satz.
# Jedes Foto setzt sich aus der Nähe in seinen Rahmen, von links nach rechts.
def v05(n):
    b = ''.join('<div class="w5-p" style="--n:%d">%s</div>' % (j, fo(k, S3)) for j, k in enumerate((TH, LO, GL)))
    return sek(n, '<div class="w5-wand vauf">%s</div>' % b + kopf2())
V.append(('Wand an Wand', v05))


# 06 · Zwei Säulen: der Text steht in der Mitte, links die Theke, rechts die Loge, beide hoch wie Säulen eines Saals.
# Beim Scrollen gleiten die beiden gegeneinander, die Theke hinauf, die Loge hinab.
def v06(n):
    return sek(n, '<div class="d6-raster" data-saeulen><div class="d6-s d6-l">%s</div>%s<div class="d6-s d6-r">%s</div></div>' % (
        fo(TH, '(max-width:760px) 45vw, 24vw'), text('d6-mitte'), fo(LO, '(max-width:760px) 45vw, 24vw')))
V.append(('Zwei Säulen', v06))


# 07 · Das geschlossene Raster: die Theke hoch links, rechts oben der Text auf einer Platte, darunter Loge und Gläser.
# Alle Kanten bündig, keine leere Ecke. Die Felder setzen sich nacheinander aus der Tiefe an ihren Platz.
def v07(n):
    return sek(n, '<div class="r7-raster vauf">%s<div class="r7-platte platte">%s</div>%s%s</div>' % (
        fo(TH, '(max-width:760px) 90vw, 30vw', 'r7-a'), text(), fo(LO, '(max-width:760px) 45vw, 30vw', 'r7-b'), fo(GL, '(max-width:760px) 45vw, 30vw', 'r7-c')))
V.append(('Das geschlossene Raster', v07))


# 08 · Die Kofferanhänger: links der Text, rechts hängen drei Anhänger an einer goldenen Stange, je ein Foto darauf.
# Beim Auftritt schwingen sie herein und pendeln an ihrem Loch aus, wie Gepäck, das mitkommt.
def v08(n):
    a = ''.join('<div class="k8-anh" style="--n:%d;--w:%sdeg"><i class="k8-faden"></i><div class="k8-karte"><i class="k8-loch"></i>%s</div></div>' % (
        j, w, fo(k, '(max-width:760px) 40vw, 14vw')) for j, (k, w) in enumerate(zip((TH, LO, GL), (-3, 2, -1.5))))
    return sek(n, '<div class="k8-raster">%s<div class="k8-stange vauf"><i class="k8-rohr"></i><div class="k8-reihe">%s</div></div></div>' % (text(), a))
V.append(('Die Kofferanhänger', v08))


# 09 · Die Salonhängung: eine dunkle Wand, darauf drei gerahmte Fotos in verschiedenen Grössen, die Loge gross in der Mitte.
# Die Rahmen hängen zuerst schief und richten sich gerade. Text rechts neben der Wand.
def v09(n):
    r = ''.join('<div class="s9-r s9-%s" style="--n:%d;--w:%sdeg"><div class="s9-pass">%s</div></div>' % (c, j, w, fo(k, '(max-width:760px) 40vw, 16vw'))
                for j, (k, c, w) in enumerate(((TH, 'a', -4), (LO, 'b', 3), (GL, 'c', -2.5))))
    return sek(n, '<div class="s9-raster"><div class="s9-wand vauf">%s</div>%s</div>' % (r, text()))
V.append(('Die Salonhängung', v09))


# 10 · Der Stempel: der Text steht auf einem cremefarbenen Auftragszettel, oben rechts landet ein roter Stempel «Ausser Haus».
# Daneben drei hohe, schmale Fotos wie Lamellen, die von unten heraufkommen.
def v10(n):
    l = ''.join('<div class="z10-l" style="--n:%d">%s</div>' % (j, fo(k, '(max-width:760px) 30vw, 12vw')) for j, k in enumerate((TH, LO, GL)))
    return sek(n, '<div class="z10-raster vauf"><div class="z10-zettel hell"><span class="z10-stempel">Ausser Haus</span>%s</div><div class="z10-lamellen">%s</div></div>' % (text(), l))
V.append(('Der Stempel', v10))


# 11 · Der Filmstreifen: links bleibt der Text stehen, rechts läuft ein senkrechter Filmstreifen mit drei Bildern
# und Perforation an beiden Rändern. Beim Scrollen gleitet der Streifen langsamer als die Seite.
def v11(n):
    b = ''.join('<div class="m11-bild">%s</div>' % fo(k, '(max-width:760px) 70vw, 26vw') for k in (TH, GL, LO))
    return sek(n, '<div class="m11-raster"><div class="m11-links">%s</div><div class="m11-spur"><div class="m11-streifen" data-film>%s</div></div></div>' % (text(), b))
V.append(('Der Filmstreifen', v11))


# 12 · Das Rund: die Loge als grosser Kreis, daneben Theke und Gläser als zwei kleinere Kreise übereinander, rechts der Text.
# Die Kreise rollen von unten an ihren Platz.
def v12(n):
    return sek(n, '<div class="r12-raster"><div class="r12-kreise vauf">%s<div class="r12-zwei">%s%s</div></div>%s</div>' % (
        fo(LO, '(max-width:760px) 70vw, 28vw', 'r12-gross'), fo(TH, '(max-width:760px) 35vw, 14vw', 'r12-k', stil='--n:1'), fo(GL, '(max-width:760px) 35vw, 14vw', 'r12-k', stil='--n:2'), text()))
V.append(('Das Rund', v12))


# 13 · Halb und halb: links reicht die Theke bis an den Rand der Seite und über die ganze Höhe des Abschnitts, das Foto gleitet beim Scrollen im Rahmen.
# Rechts Titel und Satz, darunter Loge und Gläser nebeneinander.
def v13(n):
    return sek(n, '<div class="h13-raster"><div class="h13-bild" data-halb>%s</div><div class="h13-rechts">%s<div class="h13-zwei vauf">%s%s</div></div></div>' % (
        fo(TH, '(max-width:760px) 100vw, 64vw'), text(), fo(LO, '(max-width:760px) 45vw, 18vw', stil='--n:0'), fo(GL, '(max-width:760px) 45vw, 18vw', stil='--n:1')), innen=False)
V.append(('Halb und halb', v13))


# 14 · Das Barregal: oben Titel und Satz, darunter ein Regal wie hinter der Theke. Die drei Fotos stehen verschieden hoch
# auf dem Regalbrett, die Loge in der Mitte am höchsten, und werden nacheinander von oben daraufgestellt.
def v14(n):
    b = ''.join('<div class="g14-p g14-%s" style="--n:%d">%s</div>' % (c, j, fo(k, S3)) for j, (k, c) in enumerate(((TH, 'a'), (LO, 'b'), (GL, 'c'))))
    return sek(n, kopf2() + '<div class="g14-regal vauf"><div class="g14-fach">%s</div><i class="g14-brett"></i></div>' % b)
V.append(('Das Barregal', v14))


# 15 · Die Umrissschrift: der Titel steht riesig über die ganze Breite, zuerst nur als goldener Umriss.
# Beim Auftritt steigt die Schrift von unten in ihren Umriss. Darunter drei Fotos und der Satz.
def v15(n):
    def zeile(t, j):
        return '<span class="u15-z"><span class="u15-umriss" aria-hidden="true">%s</span><span class="u15-voll" style="--n:%d">%s</span></span>' % (t, j, t)
    t = '<h2 class="titel u15-titel">%s%s</h2>' % (zeile('Grösser als', 0), zeile('die Bar.', 1))
    b = ''.join('<div class="u15-p" style="--n:%d">%s</div>' % (j, fo(k, '(max-width:760px) 30vw, 18vw')) for j, k in enumerate((TH, LO, GL)))
    return sek(n, '<div class="u15-ganz vauf">%s%s<div class="u15-unten"><div class="u15-bilder">%s</div><div>%s</div></div></div>' % (kz(), t, b, rest()))
V.append(('Die Umrissschrift', v15))


def seite(n):
    h = unter.tafel()
    if n:
        a = h.rfind('<section', 0, h.find('id="events"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[i + 1, nm] for i, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/x.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(V[n - 1][0] if n else 'Heutiger Stand'))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/x.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
