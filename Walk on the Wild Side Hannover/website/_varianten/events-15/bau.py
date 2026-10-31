# Walk on the Wild Side · Feiern-Seite, Abschnitt «Grosse Events · Grösser als die Bar.» (id="events"): 15 Darstellungen (30.10.2026).
# Robert: «gib mir 15 visuelle alternative darstellungsformen von dem abschnitt». 00 = heutiger Stand.
# Je Fassung eine eigene Anordnung und eine eigene Bewegung. Texte Wort für Wort aus unter.tafel() (unten geprüft).
# Bilder: das Foto der Loge plus echte Fotos der Bar, die sonst nicht auf der Feiern-Seite stehen.
# Bewegung nur über transform, alles deckend; Scroll-Getriebenes in einem Takt in e.js, nativer Scroll. Wechsel mit ← →.
# Aufruf: python3 _varianten/events-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
import bilder
from bilder import mache

E = html.escape
ORD = '_varianten/events-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('e.css', 'e.js', 'nav.js'))))

# Nur für diese Fassungen, bilder.py bleibt unberührt
bilder.BILDER.setdefault('ev-theke', ('angebote-pdf/img-001.jpg', 'Die Theke mit den Barhockern im gelben Licht'))

TEXT = 'Für grössere Veranstaltungen zieht die Bar um, in externe Locations wie die Loge. Derya und Momo übernehmen die Organisation und kümmern sich um das ganze Konzept, von der Bar bis zum Ablauf des Abends.'
KLEIN = 'Infos auf Anfrage.'
_q = open('unter.py').read()
for _s in (TEXT, KLEIN, "kz('Grosse Events', 'Ausser Haus', 0), h2(['Grösser als', 'die Bar.']), knopf('Event anfragen', '#anfragen')"):
    assert _s in _q, 'Text weicht ab: ' + _s[:40]

# Breite, ab der ein Bild nicht mehr grösser gezeigt wird (80 % seiner Auflösung)
LOGE = 'an-loge'        # 590 × 792
GLAS = 'an-glaeser'     # 656 × 820
BAR = 'decke-raum'      # 4284 × 5712
BARQ = 'decke-flach'    # 1200 × 900
THEKE = 'ev-theke'      # 832 × 1110


def img(k, sizes, cls='', stil=''):
    return '<figure class="fb %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, B.img_tag(k, sizes))


def kz(i=0):
    return B.kz('Grosse Events', 'Ausser Haus', i)


def titel(cls='t-kap', zeilen=None):
    return B.h2(zeilen or ['Grösser als', 'die Bar.'], cls)


def text(i=1, cls=''):
    return '<p class="text sw %s" style="--i:%d">%s</p>' % (cls, i, E(TEXT))


def klein(i=2):
    return '<p class="ev-klein sw" style="--i:%d">%s</p>' % (i, E(KLEIN))


def knopf(i=3, cls=''):
    return '<div class="knoepfe sw" style="--i:%d;margin-top:26px">%s</div>' % (i, B.knopf('Event anfragen', '#anfragen', cls))


def alles(tcls='t-kap'):
    return kz() + titel(tcls) + text() + klein() + knopf()


def sek(v, inner, cls='', innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf vx %s %s" id="events" data-v="%s">%s</section>' % (v, cls, v, i)


F = []


# 01 · Von der Bar in die Loge: links klein die Bar, eine Goldlinie, rechts die Loge. Die Linie zieht sich beim Scrollen
# von der Bar zur Loge, der Satz steht darunter in zwei Spalten.
def f01(v):
    weg = '<div class="e1-weg vauf"><div class="e1-ort">%s<span class="etikett">Die Bar</span></div><div class="e1-linie"><i></i></div><div class="e1-ort e1-ziel">%s<span class="etikett">Die Loge</span></div></div>' % (
        img(BAR, '(max-width:860px) 40vw, 22vw', 'e1-bar', '--pos:50% 40%'), img(LOGE, '(max-width:860px) 50vw, 30vw', 'e1-loge'))
    return sek(v, '%s<div class="e1-unten"><div>%s%s</div><div>%s%s%s</div></div>' % (weg, kz(), titel(), text(), klein(), knopf()))
F.append(('Von der Bar in die Loge', f01))


# 02 · Der Titel wächst: eine Zeile über die ganze Breite, sie wird beim Hereinscrollen grösser.
# Darunter Bild und Satz nebeneinander.
def f02(v):
    return sek(v, '%s<div class="e2-titel">%s</div><div class="e2-unten">%s<div class="e2-text">%s%s%s</div></div>' % (
        kz(), titel('t-gross', ['Grösser als die Bar.']), img(LOGE, '(max-width:860px) 92vw, 30vw', 'e2-bild vauf'), text(), klein(), knopf()))
F.append(('Der Titel wächst', f02))


# 03 · Stehender Text: links bleibt die Tafel stehen, rechts ziehen Loge, Theke und Gläser vorbei,
# jedes Bild zoomt im Vorbeiziehen aus seinem Rahmen zurück.
def f03(v):
    bl = ''.join(img(k, '(max-width:860px) 92vw, 36vw', 'e3-b vauf') for k in (LOGE, THEKE, GLAS))
    return sek(v, '<div class="e3"><div class="e3-links"><div class="platte e3-platte">%s</div></div><div class="e3-rechts">%s</div></div>' % (alles(), bl))
F.append(('Stehender Text, ziehende Bilder', f03))


# 04 · Bühne in der Mitte: die Loge steht hoch in der Mitte, links Überschrift, rechts der Satz.
# Das Foto steigt herauf und zoomt danach langsam in seinen Rahmen zurück.
def f04(v):
    return sek(v, '<div class="e4"><div class="e4-l">%s%s</div>%s<div class="e4-r">%s%s%s</div></div>' % (
        kz(), titel(), img(LOGE, '(max-width:860px) 80vw, 28vw', 'e4-bild vauf'), text(), klein(), knopf()))
F.append(('Bühne in der Mitte', f04))


# 05 · Heller Raum: der Abschnitt wechselt in Creme, das Foto setzt sich aus einer leichten Drehung gerade.
def f05(v):
    return sek(v, '<div class="e5">%s<div>%s</div></div>' % (img(LOGE, '(max-width:860px) 80vw, 30vw', 'e5-bild vauf'), alles()), 'hell')
F.append(('Heller Raum', f05))


# 06 · Laufband: der Titel zieht als ruhiges Band über die ganze Breite, darunter Satz und Bild.
def f06(v):
    band = ' · '.join(['Grösser als die Bar.'] * 6)
    return sek(v, '<div class="e6-band" aria-hidden="true"><div class="e6-lauf"><span>%s · </span><span>%s · </span></div></div><div class="innen e6">%s<div>%s<h2 class="ev-vh">Grösser als die Bar.</h2>%s%s%s</div></div>' % (
        E(band), E(band), img(LOGE, '(max-width:860px) 80vw, 30vw', 'e6-bild vauf'), kz(), text(), klein(), knopf()), innen=False)
F.append(('Laufband', f06))


# 07 · Eine Reihe: Kopf oben in zwei Spalten, darunter drei Bilder gleich hoch nebeneinander,
# die Reihe wandert beim Scrollen ein Stück nach links.
def f07(v):
    reihe = ''.join(img(k, '(max-width:860px) 60vw, 30vw', 'e7-b', '--r:%s' % r) for k, r in ((BARQ, '1.333'), (LOGE, '.745'), (GLAS, '.8')))
    return sek(v, '<div class="e7-kopf"><div>%s%s</div><div>%s%s%s</div></div><div class="e7-reihe vauf"><div class="e7-zug">%s</div></div>' % (
        kz(), titel(), text(), klein(), knopf(), reihe))
F.append(('Eine Reihe', f07))


# 08 · Das Bild zieht langsamer: grosser Titel ohne Tafel links, das Foto rechts gleitet langsamer als die Seite.
def f08(v):
    return sek(v, '<div class="e8"><div>%s</div><div class="e8-rahmen">%s</div></div>' % (alles('t-gross'), img(LOGE, '(max-width:860px) 80vw, 30vw', 'e8-bild')))
F.append(('Das Bild zieht langsamer', f08))


# 09 · Mittelachse: Bild, Titel und Satz auf einer Achse; das Foto zoomt beim Scrollen aus der Nähe in den Raum.
def f09(v):
    return sek(v, '<div class="e9">%s<div class="e9-kz">%s</div>%s%s%s%s</div>' % (
        img(LOGE, '(max-width:860px) 80vw, 28vw', 'e9-bild vauf'), kz(), titel('t-gross'), text(), klein(), knopf()))
F.append(('Mittelachse', f09))


# 10 · Abzüge fächern auf: drei Abzüge liegen gestapelt und legen sich beim Scrollen nebeneinander.
def f10(v):
    a = ''.join(img(k, '(max-width:860px) 40vw, 18vw', 'e10-a', '--n:%d' % n) for n, k in enumerate((THEKE, LOGE, GLAS)))
    return sek(v, '<div class="e10"><div class="e10-tisch vauf">%s</div><div>%s</div></div>' % (a, alles()))
F.append(('Abzüge fächern auf', f10))


# 11 · Gesetzt wie gedruckt: Haarlinien oben und unten, der Satz mit grosser Initiale, das Bild daneben.
def f11(v):
    ini = '<p class="text e11-text sw" style="--i:1"><span class="e11-ini">%s</span>%s</p>' % (E(TEXT[0]), E(TEXT[1:]))
    return sek(v, '<div class="e11"><div class="e11-satz">%s%s%s%s%s</div>%s</div>' % (
        kz(), titel('t-gross'), ini, klein(), knopf(), img(LOGE, '(max-width:860px) 80vw, 30vw', 'e11-bild vauf')))
F.append(('Gesetzt wie gedruckt', f11))


# 12 · Rotes Feld: Titel und Satz auf einer Fläche in Plakatrot, daneben das Foto, das im Rahmen langsamer zieht.
def f12(v):
    return sek(v, '<div class="e12"><div class="e12-feld vauf">%s</div>%s</div>' % (alles(), img(LOGE, '(max-width:860px) 80vw, 30vw', 'e12-bild')))
F.append(('Rotes Feld', f12))


# 13 · Eine Tafel für beides: Foto und Text in einer gemeinsamen Tafel, das Foto randlos links, zoomt beim Auftritt zurück.
def f13(v):
    return sek(v, '<div class="platte e13 vauf">%s<div class="e13-text">%s</div></div>' % (img(LOGE, '(max-width:860px) 92vw, 30vw', 'e13-bild'), alles()))
F.append(('Eine Tafel für beides', f13))


# 14 · Der Weg hinaus: der Abschnitt bleibt stehen, beim Scrollen fährt die Reihe von der Bar über die Gläser zur Loge.
def f14(v):
    zug = '<div class="e14-text">%s</div>%s%s%s' % (alles(), img(BAR, '(max-width:860px) 70vw, 34vw', 'e14-b', '--r:.75'),
                                                    img(GLAS, '(max-width:860px) 70vw, 34vw', 'e14-b', '--r:.8'), img(LOGE, '(max-width:860px) 70vw, 34vw', 'e14-b', '--r:.745'))
    return sek(v, '<div class="e14-steh"><div class="e14-zug">%s</div></div>' % zug, innen=False)
F.append(('Der Weg hinaus', f14))


# 15 · Säule: die Loge als hohe Säule am rechten Rand über die ganze Höhe, das Foto gleitet in der Säule;
# links der Text an einer Goldlinie.
def f15(v):
    return sek(v, '<div class="e15"><div class="e15-text">%s</div><div class="e15-saeule vauf">%s</div></div>' % (alles('t-gross'), img(LOGE, '(max-width:860px) 80vw, 30vw', 'e15-bild')))
F.append(('Säule', f15))


# ---------- Seiten
def seite(n):
    h = unter.tafel()
    if n:
        a = h.rfind('<section', 0, h.find('id="events"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + F[n - 1][1]('e%02d' % n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(F)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/e.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>Grosse Events · %s</span><i>← →</i></p>' % (n, len(F), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;window.VSEK="events";</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/e.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(F) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('fertig', len(F))
