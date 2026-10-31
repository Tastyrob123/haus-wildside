#!/usr/bin/env python3
"""Walk on the Wild Side · Startseite, Fenster «Ein Gewölbe über der Theke.» in 15 Darstellungen (29.10.2026).
Jede Fassung = die echte index.html, nur dieser Abschnitt getauscht. 00 = heute. Wechsel mit ← → (varianten-nav.js).
Je Fassung eine eigene Darstellung und eine eigene Bewegung; bewegt wird nur über transform, nichts blendet ein."""
import os, re, json, html

HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HIER, '..', '..'))
ORD = '_varianten/gewoelbe'
V = '29102'
E = html.escape


def daten(k):
    return json.load(open(os.path.join(WEB, 'assets', 'bild', k + '.json')))


def img(k, pos='50% 50%', sizes='100vw', cls='', alt=None):
    d = daten(k)
    srcset = ', '.join('assets/bild/%s?v=28103 %dw' % (f, b) for b, f in d['stufen'])
    a = alt if alt is not None else d.get('alt', '')
    return '<img%s data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" width="%d" height="%d" style="object-position:%s">' % (
        ' class="%s"' % cls if cls else '', srcset, sizes, E(a), d['w'], d['h'], pos)


def zl(zeilen, i0=0):
    return '<span class="zl">%s</span>' % ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i0 + n, z) for n, z in enumerate(zeilen))


def woerter(satz, i0=0):
    return '<span class="zl wz">%s</span>' % ' '.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i0 + n, w) for n, w in enumerate(satz.split()))


SATZ = ['Ein Gewölbe', 'über der Theke.']
DECKE_SATZ = 'Die Decke: ein Gewölbe als Druck über dem ganzen Raum, blau und silbern angeleuchtet. Seit 2017 hängt es dort.'


def sec(n, inhalt, extra=''):
    return '<section class="vg v%02d" id="gewoelbe"%s>%s</section>' % (n, extra, inhalt)


# ---------------------------------------------------------------- die 15 Fassungen
def f01():
    return sec(1, '<div class="v01-buehne"><div class="v01-bild">%s</div>'
               '<p class="vt v01-oben">%s</p><p class="vt v01-unten">%s</p></div>' % (
                   img('decke-hoch', '50% 50%'), zl(SATZ[:1]), zl(SATZ[1:])), ' data-schwenk')


def f02():
    return sec(2, '<div class="v02-a">%s<p class="vt">%s</p></div><div class="v02-b">%s<p class="vt">%s</p></div>' % (
        img('decke-raum', '50% 6%'), zl(SATZ[:1]), img('decke-hoch', '50% 88%'), zl(SATZ[1:], 1)), ' data-auf')


def f03():
    return sec(3, '<div class="innen"><p class="vt v03-z1">%s</p><div class="v03-streif" data-tiefe>%s</div><p class="vt v03-z2">%s</p></div>' % (
        zl(SATZ[:1]), img('decke-raum', '50% 14%', '92vw'), zl(SATZ[1:], 1)), ' data-auf')


def f04():
    tafeln = ''.join('<figure style="--n:%d">%s</figure>' % (n, img(k, p, '34vw')) for n, (k, p) in enumerate(
        [('decke-raum', '50% 20%'), ('decke-hoch', '50% 40%'), ('decke-bar', '50% 30%')]))
    return sec(4, '<div class="v04-wand">%s</div><p class="vt">%s</p>' % (tafeln, zl(SATZ, 2)), ' data-auf data-rand="-30%"')


def f05():
    return sec(5, '<div class="innen"><p class="vt">%s</p><div class="v05-paar">'
               '<figure class="v05-l">%s<figcaption>Das Bild zur Eröffnung · Oktober 2017</figcaption></figure>'
               '<figure class="v05-r">%s<figcaption>Haasemannstraße 13 · heute</figcaption></figure></div></div>' % (
                   woerter('Ein Gewölbe über der Theke.'), img('decke-2017', '50% 50%', '46vw'), img('decke-raum', '50% 24%', '46vw')),
               ' data-auf')


def f06():
    return sec(6, '<div class="v06-bild">%s</div><div class="v06-woerter"><p class="vt">Ein Gewölbe</p><p class="vt">über der Theke.</p></div>' % (
        img('decke-raum', '50% 30%')))


def f07():
    return sec(7, '<div class="v07-schild"><div class="v07-bild">%s</div>'
               '<p class="etikett v07-ort">Haasemannstraße 13 · Hannover-Linden</p><p class="vt">%s</p></div>' % (
                   img('decke-raum', '50% 24%', '90vw'), zl(['Ein Gewölbe über der Theke.'])), ' data-auf')


def f08():
    teile = []
    versatz = [22, 8, 30, 14, 12, 26, 6, 20, 28, 16, 24, 10]
    for r in range(3):
        for c in range(4):
            teile.append('<div class="v08-t" style="--c:%d;--r:%d;--v:%dvh">%s</div>' % (c, r, versatz[r * 4 + c], img('decke-raum', '50% 30%', '100vw')))
    return sec(8, '<div class="v08-mosaik">%s</div><p class="vt">%s</p>' % (''.join(teile), zl(SATZ, 3)), ' data-auf data-rand="-30%"')


def f09():
    return sec(9, '<div class="v09-band" data-breitwand><div class="v09-in">%s</div></div>'
               '<div class="innen v09-text"><p class="vt">%s</p><p class="text">%s</p></div>' % (
                   img('decke-raum', '50% 18%'), zl(['Ein Gewölbe über der Theke.']), E(DECKE_SATZ)), ' data-auf data-rand="-20%"')


def f10():
    return sec(10, '<div class="v10-bild">%s</div><div class="v10-text"><div class="kz"><span class="uhr">Die Decke</span><i></i><span class="was">Seit 2017</span></div>'
               '<p class="vt">%s</p><p class="text">%s</p></div>' % (
                   img('decke-hoch', '50% 40%', '50vw'), zl(SATZ), E(DECKE_SATZ)), ' data-auf data-rand="-20%"')


def f11():
    return sec(11, '<div class="v11-bild"><div class="v11-maus" data-maus>%s</div></div><p class="vt">%s</p>' % (
        img('decke-hoch', '50% 35%'), zl(SATZ)), ' data-auf data-rand="-25%"')


def f12():
    reihe = ''.join('<figure>%s</figure>' % img(k, p, '40vw') for k, p in [
        ('decke-raum', '50% 30%'), ('decke-flach', '50% 40%'), ('decke-bar', '50% 30%'), ('decke-hoch', '50% 40%'), ('fenster', '50% 30%')])
    return sec(12, '<div class="innen"><p class="vt">%s</p></div><div class="v12-band" data-lauf><div class="v12-reihe">%s%s</div></div>' % (
        zl(['Ein Gewölbe über der Theke.']), reihe, reihe.replace('<img ', '<img aria-hidden="true" ')), ' data-auf')


def f13():
    return sec(13, '<div class="v13-oben">%s</div><div class="v13-spiegel">%s</div><i class="v13-licht"></i><p class="vt">%s</p>' % (
        img('decke-raum', '50% 30%'), img('decke-raum', '50% 30%', alt=''), zl(SATZ, 1)), ' data-auf data-rand="-30%"')


def f14():
    return sec(14, '<div class="v14-raum"><div class="v14-decke">%s</div></div><p class="vt">%s</p>' % (
        img('decke-raum', '50% 8%'), zl(SATZ, 3)), ' data-auf data-rand="-25%"')


def f15():
    return sec(15, '<div class="innen"><p class="vt">%s</p><div class="v15-bild">%s</div><p class="text v15-zeile">%s</p></div>' % (
        woerter('Ein Gewölbe über der Theke.'), img('decke-raum', '50% 22%', '92vw'), E(DECKE_SATZ)), ' data-auf')


FASSUNGEN = [
    (0, 'Heute', None),
    (1, 'Der Schwenk von oben', f01),
    (2, 'Oben und unten', f02),
    (3, 'Schrift mit Fenster', f03),
    (4, 'Drei Blicke, gestaffelt', f04),
    (5, '2017 und heute', f05),
    (6, 'Der Satz zieht über die Decke', f06),
    (7, 'Das Eckschild', f07),
    (8, 'Das Mosaik setzt sich', f08),
    (9, 'Breitwand öffnet sich', f09),
    (10, 'Halb Decke, halb Satz', f10),
    (11, 'Die Decke folgt der Maus', f11),
    (12, 'Die Decken ziehen vorbei', f12),
    (13, 'Gespiegelt im Tresen', f13),
    (14, 'Die Decke über dir', f14),
    (15, 'Hell wie die Plakate', f15),
]
NAMEN = json.dumps([[n, name] for n, name, _ in FASSUNGEN], ensure_ascii=False)


def main():
    quelle = open(os.path.join(WEB, 'index.html')).read()
    m = re.search(r'<section class="fenster">(?:(?!</section>).)*?Ein Gewölbe.*?</section>', quelle, re.S)
    assert m, 'Fenster nicht gefunden'
    for n, name, f in FASSUNGEN:
        neu = f() if f else m.group(0).replace('<section class="fenster">', '<section class="fenster" id="gewoelbe">')
        s = quelle[:m.start()] + neu + quelle[m.end():]
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
        s = s.replace('</head>', '<link rel="stylesheet" href="%s/vg.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s"></head>' % (ORD, V, ORD, V), 1)
        schild = '<p class="vschild" aria-hidden="true"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(FASSUNGEN) - 1, E(name))
        s = s.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD="%s"</script>'
                      '<script src="%s/varianten-nav.js?v=%s"></script><script src="%s/vg.js?v=%s" defer></script></body>' % (NAMEN, n, ORD, ORD, V, ORD, V), 1)
        open(os.path.join(HIER, '%02d.html' % n), 'w').write(s)
    print('%d Fassungen' % len(FASSUNGEN))


if __name__ == '__main__':
    main()
