# Walk on the Wild Side · Haus-Seite, Abschnitt «Der Raum» neu erzählt als «Dein Platz» (Wahl Robert 31.10.2026).
# Der Raum aus Sicht des Gastes: an der Theke, am Tisch, auf der Empore, draussen an der Ecke. Zehn Fassungen in der echten Seite.
# Empore: Instagram-Bild voronov_irina C9z2rj1MRb2-3, weisser Rand abgeschnitten → quelle/empore.jpg.
# Fotos: je Platz eines, das auf keiner Seite der Website steht (geprüft nach Bildinhalt und Pfad, 31.10.2026).
# Belege der Sätze: unter.py (Theke, Momo fragt, Empore, Culinarium, Tische vor der Tür), _quelle/research_notes/…/menschen_geschichte_presse_raum.md
# (Barhocker, Holztische, Polsterbank, Messing-Wandleuchten, Kerzen). Aufruf: python3 _varianten/platz/bau.py → 00 … 10.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
import bilder
from bilder import mache

bilder.BILDER.setdefault('pl-theke', ('kunde-2026-10-30/wa-bar.jpg', 'Momo hinter der Theke, unter der Kante das gelbe Lichtband'))
bilder.BILDER.setdefault('pl-tisch', ('google-maps/google-18.jpg', 'Drinks am Holztisch, im Hintergrund die Polsterbank'))
bilder.BILDER.setdefault('pl-empore', ('../website/_varianten/platz/quelle/empore.jpg', 'Die lange Tafel auf der Empore, gedeckt mit Grün'))
bilder.BILDER.setdefault('pl-ecke', ('portale/enprimeurclub_hero1.jpg', 'Die Ecke Haasemannstraße und Rampenstraße mit dem Schild der Bar'))

E = html.escape
ORD = '_varianten/platz'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

# (Bild, Ort kurz, Überschrift, Satz, Bildausschnitt)
PL = [('pl-theke', 'Theke', 'An der Theke', 'Auf den Hockern an der Theke bist du am nächsten dran. Momo fragt, was du magst, und mixt daraus deinen Drink. Unter der Kante leuchtet das gelbe Lichtband.', '55% 45%'),
      ('pl-tisch', 'Tisch', 'Am Tisch', 'Holztische und eine Polsterbank an hellen Wänden, darüber Messingleuchten, auf dem Tisch Kerzenlicht. Hier sitzt ihr zu zweit oder in der Runde, unter dem Gewölbe.', '50% 60%'),
      ('pl-empore', 'Empore', 'Auf der Empore', 'Oben auf der kleinen Empore steht die lange Tafel. Zehn bis zwanzig Gäste feiern dort ihren Abend, unten läuft die Bar weiter. An einzelnen Wochenenden deckt Culinarium hier ein Menü für alle.', '50% 70%'),
      ('pl-ecke', 'Draussen', 'Draussen an der Ecke', 'Wenn es warm ist, stehen Tische vor der Tür, an der Ecke Haasemannstraße und Rampenstraße. Drinnen läuft die Bar, draussen der Abend in Linden.', '35% 60%')]
_q = open('unter.py').read()
for b in ('Er fragt, was du magst, und baut daraus einen Drink', 'Oben auf der kleinen Empore steht die lange Tafel', 'unten läuft die Bar weiter', 'Zehn bis zwanzig Gäste',
          'An einzelnen Wochenenden öffnet', 'Wenn es warm ist, stehen Tische vor der Tür an der Ecke', 'Haasemannstraße 13, Ecke Rampenstraße'):
    assert b in _q, b


def kz():
    return B.kz('Der Raum', 'Vier Plätze', 0)


def h2():
    return B.h2(['Dein Platz', 'für heute Abend.'])


def kopf(cls=''):
    return '<div class="p-kopf %s">%s%s</div>' % (cls, kz(), h2())


def sek(inner, cls=''):
    return '<section class="kap auf p %s" id="raum"><div class="innen">%s</div></section>' % (cls, inner)


def foto(k, sizes, cls='p-f', pos='50% 50%', extra=''):
    return '<figure class="%s" style="--lq:url(%s)"%s>%s</figure>' % (cls, mache(k)['lq'], extra, B.img_tag(k, sizes, extra=' style="object-position:%s"' % pos))


V = []


def v(name):
    def d(f):
        V.append((name, f))
        return f
    return d


@v('Vier Spalten')
def v01():
    # Vier Plätze nebeneinander, je ein Hochformat in normaler Grösse, darunter Überschrift und Satz. Die Spalten steigen nacheinander auf.
    h = ''.join('<div class="a1-s" style="--n:%d"><div class="a1-b">%s</div><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (
        i, foto(k, '(max-width:760px) 90vw, 24vw', pos=p), E(t), E(s)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + '<div class="a1 auf">%s</div>' % h)


@v('Im Wechsel')
def v02():
    # Die vier Plätze untereinander, das Bild abwechselnd links und rechts, halb so breit wie der Text-Block. Beim Auftritt setzt sich das Bild im Rahmen.
    h = ''.join('<div class="auf a2-e%s"><div class="a2-b">%s</div><div class="a2-t"><span class="etikett">%s</span><h3 class="titel">%s</h3><p class="text">%s</p></div></div>' % (
        ' a2-r' if i % 2 else '', foto(k, '(max-width:760px) 90vw, 40vw', pos=p), E(o), E(t), E(s)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + '<div class="a2">%s</div>' % h)


@v('Wähl deinen Platz')
def v03():
    # Oben die vier Orte als grosse Worte in einer Zeile. Antippen oder Zeigen: darunter steigt das Bild des Platzes im Rahmen auf, daneben sein Satz.
    w = ''.join('<button class="a3-w titel" data-t="%d">%s</button>' % (i, E(o)) for i, (k, o, t, s, p) in enumerate(PL))
    b = ''.join('<div class="a3-b" data-z="%d">%s</div>' % (i, foto(k, '(max-width:760px) 90vw, 50vw', pos=p)) for i, (k, o, t, s, p) in enumerate(PL))
    tx = ''.join('<div class="a3-t" data-z="%d"><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (i, E(t), E(s)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + '<div class="a3 auf" data-tausch><div class="a3-worte">%s</div><div class="a3-g"><div class="a3-rahmen">%s</div><div class="a3-txt">%s</div></div></div>' % (w, b, tx))


@v('Vier Bögen')
def v04():
    # Wie die Bögen bei «Was andere sagen», dunkel mit Goldlinie: oben das Bild im Bogen, darunter Ort und Satz.
    h = ''.join('<div class="a4-s" style="--n:%d"><div class="et9-et a4-et"><div class="et9-in a4-in"><div class="a4-foto">%s</div><span class="etikett">%s</span><i></i><p>%s</p></div></div></div>' % (
        i, foto(k, '(max-width:760px) 90vw, 24vw', pos=p), E(t), E(s)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + '<div class="a4">%s</div>' % h, 'a4-sek')


@v('Einer nach dem anderen')
def v05():
    # Gehaltene Strecke: ein Rahmen in normaler Grösse bleibt stehen, mit jedem Scrollschritt steigt der nächste Platz darin auf; rechts der Satz aus dem Schlitz.
    b = ''.join('<div class="a5-b" data-z="%d">%s</div>' % (i, foto(k, '(max-width:760px) 100vw, 50vw', pos=p)) for i, (k, o, t, s, p) in enumerate(PL))
    tx = ''.join('<div class="a5-t" data-z="%d"><div><span class="etikett">%s</span><h3 class="titel">%s</h3><p class="text">%s</p></div></div>' % (i, E(o), E(t), E(s)) for i, (k, o, t, s, p) in enumerate(PL))
    return ('<section class="kap auf p a5-sek" id="raum"><div class="innen">%s</div><div class="a5" data-pin data-schritte="4"><div class="a5-buehne"><div class="innen a5-g">'
            '<div class="a5-rahmen">%s</div><div class="a5-txt">%s</div></div></div></div></section>') % (kopf(), b, tx)


@v('Das Register')
def v06():
    # Vier breite Zeilen: links der Ort gross in der Titelschrift, in der Mitte der Satz, rechts ein kleines Querformat. Jede Zeile steigt aus ihrer Linie.
    h = ''.join('<div class="a6-z" style="--n:%d"><span class="titel">%s</span><p class="text">%s</p><div class="a6-b">%s</div></div>' % (
        i, E(t), E(s), foto(k, '(max-width:760px) 40vw, 260px', pos=p)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + '<div class="a6 auf">%s</div>' % h)


@v('Ein Platz, ein Bildschirm')
def v07():
    # Jeder Platz bekommt einen ruhigen Bildschirm: das Wort riesig links, das Bild mittelgross rechts, der Satz unter dem Wort.
    h = ''.join('<div class="auf a7-e"><div class="a7-t"><span class="titel a7-w">%s</span><p class="text">%s</p></div><div class="a7-b">%s</div></div>' % (
        E(o), E(s), foto(k, '(max-width:760px) 90vw, 36vw', pos=p)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + h)


@v('Tischkarten')
def v08():
    # Vier helle Tischkarten wie auf einem reservierten Tisch, oben ein kleines Bild, darunter der Ort in der Titelschrift und der Satz. Sie stellen sich nacheinander auf.
    h = ''.join('<div class="a8-k" style="--n:%d"><div class="a8-b">%s</div><span class="a8-o">%s</span><h3 class="titel">%s</h3><p>%s</p></div>' % (
        i, foto(k, '(max-width:760px) 80vw, 22vw', pos=p), E(o), E(t), E(s)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + '<div class="a8 auf">%s</div>' % h)


@v('Der Weg hinein')
def v09():
    # Eine goldene Linie in der Mitte führt von der Ecke draussen bis hinauf zur Empore. Die Plätze hängen abwechselnd links und rechts, ein Licht wandert beim Scrollen die Linie entlang.
    ordnung = [3, 1, 0, 2]
    h = ''.join('<div class="a9-e%s" data-schritt="%d"><div class="a9-b">%s</div><div class="a9-t"><span class="etikett">%s</span><h3 class="titel">%s</h3><p class="text">%s</p></div></div>' % (
        ' a9-r' if n % 2 else '', n, foto(PL[i][0], '(max-width:760px) 80vw, 30vw', pos=PL[i][4]), E(PL[i][1]), E(PL[i][2]), E(PL[i][3])) for n, i in enumerate(ordnung))
    return sek(kopf('p-mitte') + '<div class="a9" data-pin><i class="a9-linie"></i><i class="a9-weg"><b></b></i>%s</div>' % h)


@v('Tafel mit Wahl')
def v10():
    # Links eine Tafel wie bei Derya und Momo mit den vier Plätzen als Zeilen, rechts ein Bild in normaler Grösse. Zeigen oder Tippen auf eine Zeile tauscht das Bild, es steigt im Rahmen auf.
    zl = ''.join('<button class="a10-z" data-t="%d"><span class="titel">%s</span><p>%s</p></button>' % (i, E(t), E(s)) for i, (k, o, t, s, p) in enumerate(PL))
    b = ''.join('<div class="a10-b" data-z="%d">%s</div>' % (i, foto(k, '(max-width:760px) 90vw, 46vw', pos=p)) for i, (k, o, t, s, p) in enumerate(PL))
    return sek(kopf() + '<div class="a10 auf" data-tausch><div class="platte a10-tafel">%s</div><div class="a10-rahmen">%s</div></div>' % (zl, b))


N = len(V)


def seite(n):
    h = unter.haus()
    if n:
        a = h.find('<section class="kap auf" id="raum">')
        b = h.find('</section>', a) + len('</section>')
        assert a > 0 and b > a + 100
        h = h[:a] + V[n - 1][1]() + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, N, E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(N + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', N)
