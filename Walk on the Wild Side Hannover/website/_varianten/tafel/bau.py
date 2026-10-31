#!/usr/bin/env python3
"""Walk on the Wild Side · Startseite, Kapitel «Die lange Tafel» in 15 Darstellungen (29.10.2026).
Jede Fassung = die echte index.html, nur dieses Kapitel getauscht. 00 = heute. Wechsel mit ← →.
Texte unverändert aus bau.kap_tafel. Nur scharfe Fotos (Quelle mindestens 1440 px, nie grösser als 80 % gezeigt), keins aus Fenster davor oder Kapitel danach."""
import os, re, sys, json, html
HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HIER, '..', '..'))
sys.path.insert(0, WEB)
import bau
ORD = '_varianten/tafel'
V = '29110'
E = html.escape

TEXT = 'An manchen Abenden gehört der obere Teil der Bar einer einzigen Runde. Dann steht dort eine lange Tafel, Momo mixt die Drinks passend zum Menü, und unten läuft der Abend weiter wie immer.'
ZEILEN = [('Wo', 'Oben auf der kleinen Empore, an einer langen Tafel.'), ('Für wen', 'Eure Runde: Geburtstag, Firma, der eine Abend im Jahr.'),
          ('Drinks', 'Momo stimmt sie auf euer Menü ab.'), ('Wie', 'Anfragen, Angebot bekommen, Abend feiern.')]


def KZ(i=0):
    return bau.kz('Ein anderer Abend', 'Auf der Empore', i)


def H2(cls='t-kap', i0=0):
    return bau.h2(['Die lange Tafel.'], cls, i0)


def TX(i=1, cls=''):
    return '<p class="text sw %s" style="--i:%d">%s</p>' % (cls, i, E(TEXT))


def ZL(i=2, cls=''):
    return '<div class="zeilen sw %s" style="--i:%d">%s</div>' % (cls, i, ''.join('<div><span class="etikett">%s</span><span>%s</span></div>' % (E(a), E(b)) for a, b in ZEILEN))


def KN(i=3):
    return '<div class="knoepfe sw" style="--i:%d">%s</div>' % (i, bau.knopf('Tafel anfragen', 'tafel.html'))


def UE():
    return bau.ueber('Und wer sonst noch hier zu Hause ist.')


def woerter(satz, i0=0):
    return '<span class="zl wz">%s</span>' % ' '.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i0 + n // 3, E(w)) for n, w in enumerate(satz.split()))


def fo(k, pos='50% 50%', sizes='40vw', cls='foto', stil=''):
    return bau.bild(k, cls, sizes, stil=stil, extra=' style="object-position:%s"' % pos)


def ka(k, pos='50% 50%', sizes='40vw', stil=''):
    return fo(k, pos, sizes, 'kachel leise', stil)


def sec(n, inhalt, cls=''):
    return '<section class="kap tv tvs%02d %s auf" id="tafel">%s</section>' % (n, cls, inhalt)


def kopf(cls='', i=0):
    return '<div class="kopf %s">%s%s%s%s%s</div>' % (cls, KZ(i), H2(i0=i + 1), TX(i + 1), ZL(i + 2), KN(i + 3))


# ---------------------------------------------------------------- Fassungen
def f01():  # Die Gäste setzen sich: Band über die ganze Breite, Platz für Platz
    band = ''.join(fo(k, p, '20vw', stil='--n:%d' % n) for n, (k, p) in enumerate(
        [('fw-a9', '50% 55%'), ('tf-oben', '50% 50%'), ('tf-l5', '50% 50%'), ('tf-h2', '50% 50%'), ('fw-h30', '50% 50%')]))
    zellen = ''.join('<div style="--n:%d"><span class="etikett">%s</span><p>%s</p></div>' % (n, E(a), E(b)) for n, (a, b) in enumerate(ZEILEN))
    return sec(1, '<div class="innen tv-mitte">%s%s%s</div><div class="tv01-band staffel">%s</div><div class="innen"><div class="tv01-zellen staffel">%s</div><div class="tv-knopf-mitte">%s</div>%s</div>' % (
        KZ(), H2(i0=1), TX(1), band, zellen, KN(0), UE()))


def f02():  # Oben und unten: oben die Tafel, unten läuft die Bar weiter
    return sec(2, '<div class="innen tv02"><div class="tv02-bilder"><figure class="tv02-o">%s<figcaption class="etikett">Oben · die lange Tafel</figcaption></figure>'
               '<i class="tv02-linie"></i><figure class="tv02-u">%s<figcaption class="etikett">Unten · der Abend wie immer</figcaption></figure></div>%s</div>%s' % (
                   ka('fw-a9', '50% 58%', '56vw'), ka('voll', '50% 60%', '56vw'), kopf(), UE()))


def f03():  # Die Speisenfolge: in der Mitte die Karte, links und rechts die Tafel
    gang = ''.join('<div class="tv03-gang" style="--n:%d"><span class="etikett">%s</span><p>%s</p></div>' % (n, E(a), E(b)) for n, (a, b) in enumerate(ZEILEN))
    karte = '<div class="platte tv03-karte sw">%s%s%s<div class="tv03-gaenge staffel">%s</div>%s</div>' % (KZ(), H2(i0=1), TX(1), gang, KN(2))
    return sec(3, '<div class="innen tv03">%s%s%s</div>%s' % (ka('tf-l5', '50% 50%', '30vw'), karte, ka('tf-oben', '50% 50%', '30vw'), UE()))


def f04():  # Stufen zur Empore: die Zeilen steigen wie die Treppe hinauf zur Tafel
    stufen = ''.join('<div class="tv04-stufe" style="--n:%d;--s:%d"><span class="etikett">%s</span><span>%s</span></div>' % (n, 3 - n, E(a), E(b)) for n, (a, b) in enumerate(ZEILEN))
    return sec(4, '<div class="innen tv04"><div class="tv04-links">%s<span class="etikett tv-unter">Die Stufen hinauf zur Empore</span></div>'
               '<div class="tv04-rechts">%s<div class="kopf">%s%s%s</div><div class="tv04-treppe staffel">%s</div>%s</div></div>%s' % (
                   ka('alt-raum', '50% 60%', '44vw'), ka('fw-a9', '50% 55%', '40vw', stil='--x:1'), KZ(), H2(i0=1), TX(1), stufen, KN(2), UE()))


def f05():  # Der Film vom Tisch: der Gang an der gedeckten Tafel entlang
    film = '<figure class="kachel tv05-film sw"><video data-film muted loop playsinline preload="none" poster="assets/film/tafel-tisch.webp"><source src="assets/film/tafel-tisch.mp4" type="video/mp4"></video></figure>'
    return sec(5, '<div class="innen tv05">%s<div class="tv05-rechts">%s<div class="tv05-paar flaeche">%s%s</div></div></div>%s' % (
        film, kopf(), fo('tf-h2', '50% 50%', '24vw'), fo('tf-dessert', '50% 50%', '24vw'), UE()))


def f06():  # Bild mit Schild: die Tafel gross, darüber das Schild mit allem
    return sec(6, '<div class="innen tv06">%s<div class="platte tv06-schild sw">%s</div></div>%s' % (ka('fw-a9', '50% 55%', '66vw'), kopf(), UE()))


def f07():  # Text und Bildwand
    wand = ''.join(fo(k, p, '28vw') for k, p in [('tf-l5', '50% 50%'), ('fw-h30', '50% 50%'), ('tf-h1', '50% 50%'), ('tf-dessert', '50% 50%')])
    return sec(7, '<div class="innen tv07">%s<div class="tv07-wand flaeche">%s</div></div>%s' % (kopf(), wand, UE()))


def f08():  # Die Tafel zieht vorbei: ein Band läuft von selbst unter dem Titel
    bilder = [('fw-a9', '50% 55%'), ('tf-oben', '50% 50%'), ('tf-l3', '50% 50%'), ('tf-l8', '50% 50%'), ('fw-a53', '50% 50%'), ('fw-h30', '50% 50%'), ('tf-h1', '50% 50%')]
    reihe = ''.join('<figure>%s</figure>' % bau.img_tag(k, '22vw', extra=' style="object-position:%s"' % p) for k, p in bilder)
    zellen = ''.join('<div><span class="etikett">%s</span><p>%s</p></div>' % (E(a), E(b)) for a, b in ZEILEN)
    return sec(8, '<div class="innen tv-mitte">%s%s%s</div><div class="tv08-band" data-lauf><div class="tv08-reihe">%s%s</div></div>'
               '<div class="innen"><div class="tv01-zellen staffel">%s</div><div class="tv-knopf-mitte">%s</div>%s</div>' % (
                   KZ(), H2(i0=1), TX(1), reihe, reihe.replace('<img ', '<img aria-hidden="true" '), zellen, KN(0), UE()))


def f09():  # Die lange Tafel als langes Bild: ein schmaler, breiter Ausschnitt öffnet sich zur Seite
    return sec(9, '<div class="innen"><div class="tv09-kopf">%s<h2 class="titel tv09-titel">%s</h2></div>'
               '<div class="tv09-lang" data-lang><div class="tv09-in">%s</div></div>'
               '<div class="tv09-unten">%s<div>%s%s</div></div>%s</div>' % (
                   KZ(), bau.zl(['Die lange Tafel.'], i0=1), bau.img_tag('fw-a9', '86vw', extra=' style="object-position:50% 62%"'), TX(1), ZL(2), KN(3), UE()))


def f10():  # Vier Zeilen, vier Bilder: links steht der Titel, rechts zieht der Abend Zeile für Zeile vorbei
    reihen = ''.join('<div class="tv10-z auf">%s<span class="etikett sw">%s</span><p class="sw" style="--i:1">%s</p></div>' % (ka(k, p, '40vw'), E(a), E(b))
                     for (a, b), (k, p) in zip(ZEILEN, [('fw-a9', '50% 55%'), ('tf-l5', '50% 50%'), ('fw-h21', '50% 50%'), ('fw-h30', '50% 50%')]))
    return sec(10, '<div class="innen tv10"><div class="tv10-links"><div class="tv10-steh">%s%s%s%s</div></div><div class="tv10-rechts">%s</div></div>%s' % (
        KZ(), H2(i0=1), TX(1), KN(2), reihen, UE()))


def f11():  # Halb Bild, halb Seite
    return sec(11, '<div class="tv11"><div class="tv11-bild">%s</div><div class="tv11-seite">%s<div class="tv11-paar flaeche">%s%s</div></div></div><div class="innen">%s</div>' % (
        fo('fw-a9', '50% 55%', '50vw'), kopf(), fo('tf-h2', '50% 50%', '20vw'), fo('tf-dessert', '50% 50%', '20vw'), UE()), 'tv-randlos')


def f12():  # Hell wie die Plakate
    bilder = ''.join(ka(k, p, '30vw', stil='--n:%d' % n) for n, (k, p) in enumerate([('tf-l5', '50% 50%'), ('tf-oben', '50% 50%'), ('fw-h30', '50% 50%')]))
    return sec(12, '<div class="innen"><div class="tv-mitte">%s%s</div><div class="tv12-drei staffel">%s</div><div class="tv12-unten">%s<div>%s%s</div></div>%s</div>' % (
        KZ(), H2(i0=1), bilder, TX(1), ZL(2), KN(3), bau.ueber('Und wer sonst noch hier zu Hause ist.', True)), 'hell')


def f13():  # Die Säulen laufen: zwei Bildsäulen laufen gegeneinander neben dem Text
    a = [('tf-oben', '50% 50%'), ('tf-l3', '50% 50%'), ('fw-h30', '50% 50%'), ('tf-h1', '50% 50%')]
    b = [('fw-a9', '50% 55%'), ('tf-l8', '50% 50%'), ('tf-dessert', '50% 50%'), ('tf-h2', '50% 50%')]
    s = lambda L: ''.join('<figure>%s</figure>' % bau.img_tag(k, '22vw', extra=' style="object-position:%s"' % p) for k, p in L)
    return sec(13, '<div class="innen tv13">%s<div class="tv13-saeulen" data-lauf><div class="tv13-s"><div class="tv13-lauf">%s%s</div></div><div class="tv13-s tv13-ab"><div class="tv13-lauf">%s%s</div></div></div></div>%s' % (
        kopf(), s(a), s(a), s(b), s(b), UE()))


def f14():  # Der Satz gross: der Text selbst trägt, darunter drei Bilder Wand an Wand und die Zeilen
    zellen = ''.join('<div><span class="etikett">%s</span><p>%s</p></div>' % (E(a), E(b)) for a, b in ZEILEN)
    drei = ''.join(fo(k, p, '31vw') for k, p in [('fw-a9', '50% 55%'), ('tf-l5', '50% 50%'), ('fw-h30', '50% 50%')])
    return sec(14, '<div class="innen">%s%s<p class="titel tv14-satz">%s</p><div class="tv14-drei flaeche">%s</div><div class="tv01-zellen staffel">%s</div><div class="tv-knopf-mitte">%s</div>%s</div>' % (
        KZ(), H2(i0=1), woerter(TEXT, 2), drei, zellen, KN(0), UE()))


def f15(alt):  # Wie heute, nur das unscharfe Glas getauscht
    k = bau.kachel('tafel-drink', '', '28vw')
    assert k in alt
    return alt.replace(k, bau.kachel('fw-h30', '', '28vw'))


FASSUNGEN = [(0, 'Heute', None), (1, 'Die Gäste setzen sich', f01), (2, 'Oben und unten', f02), (3, 'Die Speisenfolge', f03),
             (4, 'Stufen zur Empore', f04), (5, 'Der Film vom Tisch', f05), (6, 'Bild mit Schild', f06), (7, 'Text und Bildwand', f07),
             (8, 'Die Tafel zieht vorbei', f08), (9, 'Die lange Tafel als langes Bild', f09), (10, 'Vier Zeilen, vier Bilder', f10),
             (11, 'Halb Bild, halb Seite', f11), (12, 'Hell wie die Plakate', f12), (13, 'Die Säulen laufen', f13), (14, 'Der Satz gross', f14),
             (15, 'Wie heute, scharf', f15)]
NAMEN = json.dumps([[n, name] for n, name, _ in FASSUNGEN], ensure_ascii=False)


def main():
    quelle = open(os.path.join(WEB, 'index.html')).read()
    m = re.search(r'<section class="kap auf" id="tafel">.*?</section>', quelle, re.S)
    assert m
    for n, name, f in FASSUNGEN:
        neu = m.group(0) if f is None else (f(m.group(0)) if n == 15 else f())
        s = quelle[:m.start()] + neu + quelle[m.end():]
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
        s = s.replace('</head>', '<link rel="stylesheet" href="%s/tv.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s"></head>' % (ORD, V, ORD, V), 1)
        schild = '<p class="vschild" aria-hidden="true"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(FASSUNGEN) - 1, E(name))
        s = s.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD="%s"</script>'
                      '<script src="%s/varianten-nav.js?v=%s"></script><script src="%s/tv.js?v=%s" defer></script></body>' % (NAMEN, n, ORD, ORD, V, ORD, V), 1)
        open(os.path.join(HIER, '%02d.html' % n), 'w').write(s)
    print('%d Fassungen' % len(FASSUNGEN))


if __name__ == '__main__':
    main()
