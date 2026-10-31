# Walk on the Wild Side · Fuss der Startseite (id="besuch"), 15 Fassungen (29.10.2026).
# Robert: «15 verschiedene Visualisierungsmöglichkeiten für diesen Footer beim Wildside, wo das Wildside im Vordergrund steht,
# aber wo wir auch das Kulinarium und das Dirty Chicken screenen.»
# Je Fassung ein eigener Aufbau und eine eigene Bewegung; Wild Side mit Logo, «heute», Zeiten und Adresse vorn, Culinarium und
# Dirty Chicken mit ihren echten Logos (Originale von Rudi, 28.10.2026) und echten Fotos kleiner daneben. Auftritte nur mit transform, deckend.
# Wechsel mit ← → (varianten-nav.js, merkt sich die Stelle auch im Fuss). Aufruf: python3 _varianten/fuss-15/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau, bilder
from bau import E, LOGO, HAUS, mache, img_tag, PFEIL

ORD = '_varianten/fuss-15'
Z = ORD + '/zeichen/'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('fuss.css', 'fuss.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('index.html').read()
a = basis.index('<footer class="fuss auf" id="besuch">')
b = basis.index('</footer>', a) + len('</footer>')
HEUTE = basis[a:b]

# Fotos der beiden Nachbarn aus dem Culinarium-Projekt (Rudis Drive und seine Dirty-Chicken-Fotos vom 27.10.2026)
CU = '../../Culinarium Hannover/_quelle/'
bilder.BILDER.update({
    'nb-cu-bete':   (CU + 'vom-kunden/drive/4890.jpg', 'Rote Bete mit Schaum, dahinter der Drink zum Gang'),
    'nb-cu-knoedel': (CU + 'vom-kunden/drive/5098.jpg', 'Zwei Knödel mit Kräutern auf Porzellan'),
    'nb-cu-tafel':  (CU + 'vom-kunden/drive/3930.jpg', 'Gläser und die gedruckte Karte auf der Tafel'),
    'nb-dc-burger': (CU + 'dirty-chicken/vom-kunden-2026-10-27/84673.jpg', 'Ein Chicken-Sandwich im Papier'),
    'nb-dc-tisch':  (CU + 'dirty-chicken/vom-kunden-2026-10-27/84678.jpg', 'Ein Tisch voller Dirty Chicken von oben'),
    'nb-dc-sosse':  (CU + 'dirty-chicken/vom-kunden-2026-10-27/84676.jpg', 'Grüne Sauce kommt auf die Chicken Chunks'),
})

CU_ET, CU_SATZ = 'Food-Pairing-Abende', 'An einzelnen Wochenenden wird aus der langen Tafel ein Menü: Rudi kocht, Momo mixt die Drinks dazu.'
DC_ET, DC_SATZ = 'Pop-up', 'Rudis Sandwiches aus der Familie der Bar, mal hier, mal im Tiedthof.'
NAV = [('drinks.html', 'Drinks'), ('programm.html', 'Programm'), ('tafel.html', 'Die lange Tafel'), ('haus.html', 'Das Haus'), ('besuch.html', 'Besuch')]


def k(key, cls='', sizes='25vw', stil='', pos=None):
    extra = ' style="object-position:%s"' % pos if pos else ''
    return '<figure class="kachel %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(key)['lq'], stil, img_tag(key, sizes, extra=extra))


def logo(cls=''):
    return '<span class="logo %s">%s</span>' % (cls, LOGO)


def cu_logo(farbe='creme', cls=''):
    return '<img class="z-cu %s" src="%scu-%s.svg?v=%s" alt="Culinarium" width="365" height="67" loading="lazy">' % (cls, Z, farbe, VER)


def dc_logo(farbe='creme', cls=''):
    return '<img class="z-dc %s" src="%sdc-%s.webp?v=%s" alt="Dirty Chicken, Sandwiches &amp; More" width="900" height="693" loading="lazy">' % (cls, Z, farbe, VER)


def kz(uhr='Bis 2 Uhr', was='Besuch', cls=''):
    return '<div class="kz %s"><span class="uhr">%s</span><i></i><span class="was">%s</span></div>' % (cls, E(uhr), E(was))


def heute(cls='t-mittel', schlitz=False):
    if schlitz:
        return '<h2 class="titel %s schlitz"><span data-heute-satz>Donnerstag bis Samstag ab 19 Uhr</span></h2>' % cls
    return '<h2 class="titel %s" data-heute-satz>Donnerstag bis Samstag ab 19 Uhr</h2>' % cls


def zeiten(cls=''):
    return '<div class="zeiten %s">%s</div>' % (cls, ''.join(
        '<div data-tag="%s"><span>%s<span class="jetzt"></span></span><b>%s</b></div>' % (t, E(n), E(z)) for n, z, t in HAUS['zeiten']))


def besuch(cls='', etikett=True):
    return '<div class="besuch %s">%s<p>%s<br>%s<br>%s</p><p><a href="tel:%s">%s</a><br><a href="%s" rel="noopener">%s</a></p></div>' % (
        cls, '<span class="etikett">Besuch</span>' if etikett else '', E(HAUS['adresse']), E(HAUS['ort']), E(HAUS['ecke']),
        HAUS['tel_href'], E(HAUS['telefon']), HAUS['instagram'], E(HAUS['ig_name']))


def weiter(text, span=True):
    return '<span class="weiter">%s %s</span>' % (E(text), PFEIL)


def nachbar_text(wer, farbe='creme', logo_cls=''):
    if wer == 'cu':
        return '%s<span class="etikett n-et">%s</span><p class="n-satz">%s</p>%s' % (cu_logo(farbe, logo_cls), CU_ET, E(CU_SATZ), weiter('Zu Culinarium'))
    return '%s<span class="etikett n-et">%s</span><p class="n-satz">%s</p>%s' % (dc_logo(farbe, logo_cls), DC_ET, E(DC_SATZ), weiter('Zu Dirty Chicken'))


def href(wer):
    return HAUS['culinarium'] if wer == 'cu' else HAUS['dirty']


UNTEN = ('<nav class="f-nav">%s</nav>' % ''.join('<a href="%s">%s</a>' % (h, E(t)) for h, t in NAV) +
         '<div class="fuss-unten"><span>Walk on the Wild Side · Nachbarschafts-Mixology-Bar · Hannover-Linden</span><span><a href="impressum.html">Impressum</a> · '
         '<a href="datenschutz.html">Datenschutz</a> · Entwurf von Tasty Studios, nicht die offizielle Website</span></div>')


def fuss(n, inner, voll=''):
    return '<footer class="fuss auf f2 f%02d" id="besuch" data-v="%d">%s<div class="innen">%s%s</div></footer>' % (n, n, voll, inner, UNTEN)


V = []

# 01 Die Schrift trägt: kein Foto, «Heute ab 19 Uhr» läuft gross über die ganze Breite aus dem Schlitz; darunter drei Spalten,
#    rechts die beiden Nachbarn mit ihren Logos
def f01(n):
    nb = ''.join('<a class="f01-n hoch" style="--n:%d" href="%s">%s</a>' % (j + 3, href(w), nachbar_text(w)) for j, w in enumerate(['cu', 'dc']))
    return fuss(n, kz() + '<div class="f01-kopf">%s%s</div><div class="f01-spalten"><div class="hoch" style="--n:1">%s</div><div class="hoch" style="--n:2">%s</div></div>'
                '<span class="etikett f01-et">Unter demselben Dach</span><div class="f01-dach">%s</div>' % (
                    logo('f01-logo'), heute('f01-satz', True), zeiten(), besuch(), nb))
V.append(('Die Schrift trägt', f01))

# 02 Die Hausecke: Eckschild-Foto, daneben alles zur Bar; unter einer goldenen Stange hängen zwei kleinere Schilder
#    der Nachbarn und pendeln sich beim Auftritt ein
def f02(n):
    sch = ('<a class="f02-schild f02-cu" href="%s"><i class="f02-h"></i>%s</a>' % (href('cu'), nachbar_text('cu', 'dunkel')) +
           '<a class="f02-schild f02-dc" href="%s"><i class="f02-h"></i>%s</a>' % (href('dc'), nachbar_text('dc', 'creme')))
    return fuss(n, kz() + '<div class="f02-oben">%s<div class="f02-info hoch">%s%s%s%s</div></div><div class="f02-stange"></div><div class="f02-haengen">%s</div>' % (
        k('schild', 'f02-bild', '40vw'), logo('f02-logo'), heute(), zeiten(), besuch(), sch))
V.append(('Die Hausecke', f02))

# 03 Drei Fenster in einer Fassade: eine Reihe Fotos gleicher Höhe, Wild Side doppelt so breit; unter jedem Fenster sein Name;
#    die Fenster setzen sich nacheinander, darunter Zeiten und Weg
def f03(n):
    ws = '<div class="f03-f f03-ws hoch" style="--n:0">%s<div class="f03-u f03-wsu"><div>%s%s</div>%s</div></div>' % (k('fenster', '', '50vw'), logo('f03-logo'), heute('t-klein'), zeiten())
    cu = '<a class="f03-f hoch" style="--n:1" href="%s">%s<div class="f03-u">%s<p class="n-satz">%s</p>%s</div></a>' % (href('cu'), k('nb-cu-bete', '', '25vw'), cu_logo(), E(CU_SATZ), weiter('Zu Culinarium'))
    dc = '<a class="f03-f hoch" style="--n:2" href="%s">%s<div class="f03-u">%s<p class="n-satz">%s</p>%s</div></a>' % (href('dc'), k('nb-dc-burger', '', '25vw'), dc_logo(), E(DC_SATZ), weiter('Zu Dirty Chicken'))
    return fuss(n, kz() + '<div class="f03-reihe">%s%s%s</div><div class="f03-unten hoch" style="--n:3">%s</div>' % (ws, cu, dc, besuch()))
V.append(('Drei Fenster in einer Fassade', f03))

# 04 Das Plakat an der Tür: alles zur Bar auf einem cremefarbenen Plakat wie die Plakate der Bar, leicht schräg,
#    es dreht sich beim Auftritt an seinen Platz; rechts ein Foto der Ecke und die zwei Nachbarn als Zeilen
def f04(n):
    pl = '<div class="f04-plakat hell">%s<span class="etikett">Eure Nachbarschafts-Mixology-Bar</span>%s%s%s</div>' % (logo('f04-logo'), heute(), zeiten(), besuch())
    zeilen = ''.join('<a class="f04-z hoch" style="--n:%d" href="%s">%s<div>%s</div></a>' % (
        j + 1, href(w), k(f, '', '14vw'), nachbar_text(w)) for j, (w, f) in enumerate([('cu', 'nb-cu-knoedel'), ('dc', 'nb-dc-sosse')]))
    return fuss(n, kz() + '<div class="f04-wand">%s<div class="f04-rechts">%s<span class="etikett hoch" style="--n:1">Unter demselben Dach</span>%s</div></div>' % (
        pl, k('schild-ecke', 'f04-bild hoch', '45vw'), zeilen))
V.append(('Das Plakat an der Tür', f04))

# 05 Die Nacht in Stunden: die Öffnungszeiten als Leiste von 19 bis 2 Uhr, die Balken wachsen beim Auftritt von 19 Uhr aus;
#    darunter die zwei Nachbarn als Platten mit Foto
def f05(n):
    stunden = ['19', '20', '21', '22', '23', '0', '1', '2']
    kopf = '<div class="f05-z f05-kopf"><span></span><div class="f05-std">%s</div></div>' % ''.join('<i>%s</i>' % s for s in stunden)
    reihen = ''
    for j, (name, zeit, tag) in enumerate(HAUS['zeiten']):
        lang = {'19 bis 1 Uhr': 6, '19 bis 2 Uhr': 7}.get(zeit, 0)
        balken = '<b class="f05-b" style="--l:%d;--n:%d"><span>%s</span></b>' % (lang, j, E(zeit)) if lang else '<em>%s</em>' % E(zeit)
        reihen += '<div class="f05-z" data-tag="%s"><span>%s<span class="jetzt"></span></span><div class="f05-std">%s</div></div>' % (tag, E(name), balken)
    pl = ''.join('<a class="platte f05-n hoch" style="--n:%d" href="%s">%s<div>%s</div></a>' % (j + 2, href(w), k(f, '', '18vw'), nachbar_text(w))
                 for j, (w, f) in enumerate([('cu', 'nb-cu-tafel'), ('dc', 'nb-dc-tisch')]))
    return fuss(n, kz() + '<div class="f05-oben"><div>%s%s</div>%s</div><div class="platte f05-leiste">%s%s</div><div class="f05-nachbarn">%s</div>' % (
        logo('f05-logo'), heute('t-gross'), besuch('hoch'), kopf, reihen, pl))
V.append(('Die Nacht in Stunden', f05))

# 06 Das Klingelschild: links das Eckschild bei Nacht, rechts die Tafel an der Haustür, Haasemannstraße 13, mit drei Klingeln;
#    oben gross die Bar, darunter die Nachbarn; die Knöpfe geben beim Darüberfahren nach
def f06(n):
    kn = '<i class="f06-knopf">%s</i>' % PFEIL
    ws = '<a class="f06-k f06-ws hoch" style="--n:1" href="besuch.html#reservieren">%s<div><span class="etikett">Nachbarschafts-Mixology-Bar</span>%s</div>%s</a>' % (logo('f06-logo'), heute('t-klein'), kn)
    cu = '<a class="f06-k hoch" style="--n:2" href="%s">%s<div><span class="etikett">%s</span><p>Die Abende an der Tafel</p></div>%s</a>' % (href('cu'), cu_logo(), CU_ET, kn)
    dc = '<a class="f06-k hoch" style="--n:3" href="%s">%s<div><span class="etikett">%s</span><p>Sandwiches aus der Familie der Bar</p></div>%s</a>' % (href('dc'), dc_logo(), DC_ET, kn)
    tafel = '<div class="f06-tafel platte"><div class="f06-adr"><span class="titel">%s</span><span class="etikett">Hannover-Linden</span></div>%s%s%s</div>' % (E(HAUS['adresse']), ws, cu, dc)
    return fuss(n, kz() + '<div class="f06-wand">%s<div class="f06-rechts">%s<div class="f06-unten hoch" style="--n:4">%s%s</div></div></div>' % (
        k('tuer-rot', 'f06-bild', '40vw'), tafel, zeiten(), besuch()))
V.append(('Das Klingelschild', f06))

# 07 Das Band: oben alles zur Bar in zwei Spalten, darunter läuft ein randloses Band aus Fotos langsam weiter;
#    zwischen den Bildern der Bar liegen die Logos und Fotos der Nachbarn, jedes führt zu seiner Seite
def f07(n):
    def lt(w):
        return '<a class="f07-logo-k f07-%s" href="%s">%s<span class="etikett">%s</span></a>' % (w, href(w), cu_logo('dunkel') if w == 'cu' else dc_logo(), 'Die Abende an der Tafel' if w == 'cu' else 'Das Pop-up')
    folge = (k('negroni', '', '16vw') + k('anstossen', '', '16vw') + lt('cu') + '<a href="%s">%s</a>' % (href('cu'), k('nb-cu-bete', '', '16vw')) +
             k('momo-giesst', '', '16vw') + k('glas-rot', '', '16vw') + lt('dc') + '<a href="%s">%s</a>' % (href('dc'), k('nb-dc-burger', '', '16vw')) +
             k('freundinnen', '', '16vw') + '<a href="%s">%s</a>' % (href('cu'), k('nb-cu-knoedel', '', '16vw')) + k('schild', '', '16vw') + '<a href="%s">%s</a>' % (href('dc'), k('nb-dc-tisch', '', '16vw')))
    band = '<div class="f07-band"><div class="f07-spur">%s%s</div></div>' % (folge, folge.replace('loading="lazy"', 'loading="lazy" aria-hidden="true"'))
    oben = '<div class="innen">%s<div class="f07-oben"><div class="hoch">%s%s%s</div><div class="hoch" style="--n:1">%s<p class="f07-dach"><span class="etikett">Im Band</span>Culinarium und Dirty Chicken, die Nachbarn unter demselben Dach.</p></div></div></div>' % (
        kz(), logo('f07-logo'), heute('t-gross'), zeiten(), besuch())
    return fuss(n, '', oben + band)
V.append(('Das Band', f07))

# 08 Das Gewölbe zum Schluss: ein breites Foto der Decke randlos über die ganze Breite, es setzt sich beim Auftritt;
#    darunter die Bar gross und vier Spalten, die letzten zwei für die Nachbarn
def f08(n):
    bild = '<div class="f08-bild">%s</div>' % k('decke-flach', '', '100vw')
    sp = ''.join('<a class="f08-n hoch" style="--n:%d" href="%s">%s</a>' % (j + 2, href(w), nachbar_text(w)) for j, w in enumerate(['cu', 'dc']))
    return fuss(n, '<div class="f08-kopf">%s<div>%s%s</div>%s</div><div class="f08-spalten">%s%s</div>' % (
        logo('f08-logo'), kz(), heute('t-gross'), zeiten('hoch'), besuch('hoch'), sp), bild)
V.append(('Das Gewölbe zum Schluss', f08))

# 09 Drei Platten mit Tiefe: die Bar auf einer breiten Platte, die Nachbarn auf zwei schmalen; die Platten richten sich beim Auftritt auf
#    und neigen sich leicht zur Maus
def f09(n):
    ws = '<div class="platte f09-p f09-ws" style="--n:0">%s%s%s%s</div>' % (logo('f09-logo'), heute(), zeiten(), besuch())
    nb = ''.join('<a class="platte f09-p" style="--n:%d" href="%s">%s<div class="f09-t">%s</div></a>' % (j + 1, href(w), k(f, '', '22vw'), nachbar_text(w))
                 for j, (w, f) in enumerate([('cu', 'nb-cu-knoedel'), ('dc', 'nb-dc-burger')]))
    return fuss(n, kz() + '<div class="f09-reihe">%s%s</div>' % (ws, nb))
V.append(('Drei Platten mit Tiefe', f09))

# 10 Das Triptychon: die Bar in der Mitte, zentriert, mit den drei Abenden nebeneinander; links Culinarium, rechts Dirty Chicken
#    als hohe Fotos mit Logo; die Mitte kommt zuerst, die Flügel danach
def f10(n):
    abende = ''.join('<div data-tag="%s"><span class="etikett">%s<span class="jetzt"></span></span><b>%s</b></div>' % (t, E(nm), E(z)) for nm, z, t in HAUS['zeiten'][:3])
    mitte = ('<div class="f10-mitte hoch">%s%s<div class="f10-abende">%s</div><p class="f10-zu">Sonntag bis Mittwoch geschlossen</p>%s</div>' % (
        logo('f10-logo'), heute('t-gross'), abende, besuch('f10-b', False)))
    fl = lambda w, f, j: '<a class="f10-fluegel hoch" style="--n:%d" href="%s">%s%s</a>' % (j, href(w), k(f, '', '24vw'), nachbar_text(w))
    return fuss(n, '<div class="f10-kz">%s</div><div class="f10-reihe">%s%s%s</div>' % (kz(), fl('cu', 'nb-cu-bete', 2), mitte, fl('dc', 'nb-dc-sosse', 3)))
V.append(('Das Triptychon', f10))

# 11 Die Wand: Wand an Wand ein Raster aus Fotos der Bar, einer grossen Platte mit allem zur Bar und den Logos und Fotos der Nachbarn;
#    jede Kachel kommt aus einer anderen Tiefe, die Wand schliesst sich
def f11(n):
    info = '<div class="platte f11-info f11-z" style="--d:20px"><div class="f11-kopf">%s%s</div>%s%s</div>' % (logo('f11-logo'), heute(), zeiten(), besuch('', False))
    teile = [k('schild', 'f11-z f11-a', '18vw', '--d:90px'), k('negroni', 'f11-z f11-b', '30vw', '--d:50px'),
             '<a class="f11-z f11-c f11-l f11-cu" href="%s" style="--d:120px">%s<span class="etikett">Die Abende an der Tafel</span></a>' % (href('cu'), cu_logo('dunkel')),
             '<a class="f11-z f11-d" href="%s" style="--d:70px">%s</a>' % (href('cu'), k('nb-cu-tafel', '', '18vw')),
             k('momo-giesst', 'f11-z f11-e', '18vw', '--d:100px', '50% 30%'),
             '<a class="f11-z f11-f f11-l f11-dc" href="%s" style="--d:60px">%s<span class="etikett">Das Pop-up</span></a>' % (href('dc'), dc_logo()),
             '<a class="f11-z f11-g" href="%s" style="--d:110px">%s</a>' % (href('dc'), k('nb-dc-tisch', '', '18vw'))]
    return fuss(n, kz() + '<div class="f11-wand">%s%s</div>' % (info, ''.join(teile)))
V.append(('Die Wand', f11))

# 12 Zwei Ebenen: oben die Bar in der Nacht, darunter hebt sich eine cremefarbene Ebene wie die Plakate der Bar
#    mit den beiden Nachbarn nebeneinander
def f12(n):
    oben = '<div class="f12-oben">%s<div class="f12-info hoch">%s%s%s%s</div></div>' % (k('momo-giesst', 'f12-bild', '40vw', '', '50% 35%'), logo('f12-logo'), heute(), zeiten(), besuch())
    nb = ''.join('<a class="f12-n" href="%s">%s<div>%s</div></a>' % (href(w), k(f, '', '20vw'), nachbar_text(w, 'dunkel')) for w, f in [('cu', 'nb-cu-bete'), ('dc', 'nb-dc-burger')])
    ebene = '<div class="f12-ebene hell"><span class="etikett">Unter demselben Dach</span><div class="f12-zwei">%s</div></div>' % nb
    return fuss(n, kz() + oben + ebene)
V.append(('Zwei Ebenen', f12))

# 13 Die Wegweiser: an einem goldenen Pfosten drei Schilder, oben breit die Bar, darunter Culinarium und Dirty Chicken;
#    jedes Schild setzt sich mit einer kleinen Drehung an seinen Platz; rechts Zeiten und Weg
def f13(n):
    ws = '<a class="f13-s f13-ws" href="besuch.html#reservieren" style="--n:0;--r:-3deg">%s<div><span class="etikett">Hier · %s</span><p class="titel">Eure Nachbarschafts-Mixology-Bar</p></div></a>' % (logo('f13-logo'), E(HAUS['adresse']))
    cu = '<a class="f13-s f13-cu" href="%s" style="--n:1;--r:3deg">%s<span class="etikett">Die Abende an der Tafel</span></a>' % (href('cu'), cu_logo('dunkel'))
    dc = '<a class="f13-s f13-dc" href="%s" style="--n:2;--r:-2deg">%s<span class="etikett">Das Pop-up</span></a>' % (href('dc'), dc_logo())
    return fuss(n, kz() + '<div class="f13-wand"><div class="f13-pfosten">%s%s%s</div><div class="f13-rechts hoch" style="--n:1">%s%s%s</div></div>' % (
        ws, cu, dc, heute('t-gross'), zeiten(), besuch()))
V.append(('Die Wegweiser', f13))

# 14 Drei Etagen: die Bar als hohe Etage mit grossem Foto, darunter zwei flachere Etagen für die Nachbarn,
#    jede über die ganze Breite; die Etagen heben sich nacheinander
def f14(n):
    eg = '<div class="f14-e f14-ws hoch" style="--n:0">%s<div class="f14-info">%s%s<div class="f14-zwei">%s%s</div></div></div>' % (
        k('rueckbar-breit', '', '50vw'), logo('f14-logo'), heute('t-gross'), zeiten(), besuch())
    et = ''.join('<a class="platte f14-e f14-n hoch" style="--n:%d" href="%s">%s%s<span class="etikett">%s</span><p class="n-satz">%s</p>%s</a>' % (
        j + 1, href(w), k(f, '', '24vw'), cu_logo() if w == 'cu' else dc_logo(), CU_ET if w == 'cu' else DC_ET, E(CU_SATZ if w == 'cu' else DC_SATZ),
        weiter('Zu Culinarium' if w == 'cu' else 'Zu Dirty Chicken')) for j, (w, f) in enumerate([('cu', 'nb-cu-tafel'), ('dc', 'nb-dc-tisch')]))
    return fuss(n, kz() + eg + et)
V.append(('Drei Etagen', f14))

# 15 Die Visitenkarten: drei Karten übereinander, vorn gross die Karte der Bar, dahinter schauen Culinarium und Dirty Chicken hervor;
#    beim Auftritt fächern sie sich auf, die hinteren heben sich beim Darüberfahren
def f15(n):
    karten = ('<a class="f15-k f15-cu" href="%s">%s<span class="etikett">Die Abende an der Tafel</span></a>' % (href('cu'), cu_logo('dunkel')) +
              '<a class="f15-k f15-dc" href="%s">%s<span class="etikett">Das Pop-up</span></a>' % (href('dc'), dc_logo()) +
              '<div class="f15-k f15-ws">%s<span class="etikett">Nachbarschafts-Mixology-Bar</span>%s</div>' % (logo('f15-logo'), besuch('', False)))
    return fuss(n, kz() + '<div class="f15-wand"><div class="f15-stapel">%s</div><div class="f15-rechts hoch" style="--n:1">%s%s<p class="f15-dach">'
                'Dahinter die Nachbarn unter demselben Dach: <a href="%s">Culinarium</a> und <a href="%s">Dirty Chicken</a>.</p></div></div>' % (
                    karten, heute('t-gross'), zeiten(), href('cu'), href('dc')))
V.append(('Die Visitenkarten', f15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/fuss.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    schluss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
               '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/fuss.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schluss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
