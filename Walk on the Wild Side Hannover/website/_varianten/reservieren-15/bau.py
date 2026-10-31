# Walk on the Wild Side · Besuch-Seite, Abschnitt «Reservieren» (id="reservieren"), 15 Fassungen (31.10.2026).
# Robert: «gib mir 15 alternative visualiserungen für den abschnitt» (Bildschirmfoto: Reservieren · Ein Platz an der Theke, Formular rechts).
# Inhalt bleibt wie heute (Titel, Satz, Felder, Hinweis); je Fassung eigener Aufbau und eigene Bewegung, nur transform/opacity, nie seitwärts.
# Wechsel mit ← → (varianten-nav.js). Aufruf: python3 _varianten/reservieren-15/bau.py
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, HAUS, mache, img_tag, LOGO, PFEIL

ORD = '_varianten/reservieren-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('rv.css', 'rv.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('besuch.html').read()
assert len(basis) > 10000, 'besuch.html leer (anderer Bau läuft?)'
a = basis.index('<section class="kap auf" id="reservieren">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]

SATZ = 'Für zwei bis sechs Leute. Ab zehn Gästen gibt es die lange Tafel, ab dreissig die ganze Bar: alles unter <a href="tafel.html">Feiern</a>. Die Bar bestätigt per Nachricht.'
SATZ_KURZ = 'Ab zehn Gästen gibt es die lange Tafel, ab dreissig die ganze Bar: alles unter <a href="tafel.html">Feiern</a>. Die Bar bestätigt per Nachricht.'
HINWEIS = 'Vorführung: In diesem Entwurf wird nichts verschickt.'
DANK = 'Danke. Die Bar bestätigt dir den Abend.'
ZEITEN = ['19 Uhr', '20 Uhr', '21 Uhr', '22 Uhr']


def bildf(key, cls='', sizes='40vw', pos=None):
    extra = ' style="object-position:%s"' % pos if pos else ''
    return '<figure class="rv-bild %s" style="--lq:url(%s)">%s</figure>' % (cls, mache(key)['lq'], img_tag(key, sizes, extra=extra))


def kz(cls=''):
    return '<div class="kz rv-kz %s"><span class="uhr">Reservieren</span><i></i><span class="was">Ein Platz an der Theke</span></div>' % cls


def titel(cls='rv-t'):
    return '<h2 class="titel %s"><span class="rv-z"><span>Ein Platz</span></span><span class="rv-z"><span>für euch.</span></span></h2>' % cls


def satz(cls='', kurz=False):
    return '<p class="text rv-satz %s">%s</p>' % (cls, SATZ_KURZ if kurz else SATZ)


# --- Felder (gleiche Namen wie heute)
def f_abend(lab='Abend'):
    return '<label class="rv-f"><span>%s</span><input type="date" name="datum"></label>' % lab


def f_zeit(lab='Uhrzeit'):
    return '<label class="rv-f"><span>%s</span><select name="zeit">%s</select></label>' % (lab, ''.join('<option>%s</option>' % z for z in ZEITEN))


def f_wie(lab='Wie viele'):
    return '<label class="rv-f"><span>%s</span><input type="number" name="gaeste" min="1" max="6" placeholder="z. B. 4"></label>' % lab


def f_name(lab='Name'):
    return '<label class="rv-f"><span>%s</span><input type="text" name="name"></label>' % lab


def f_kontakt(lab='Telefon oder E-Mail'):
    return '<label class="rv-f"><span>%s</span><input type="text" name="kontakt"></label>' % lab


def knopf(cls='rot', text='Platz reservieren'):
    return '<button class="knopf %s" type="submit"><span>%s</span><i>%s</i></button>' % (cls, text, PFEIL)


def fuss(cls='', kn='rot'):
    return '<div class="rv-fuss rv-weg %s">%s<span class="rv-hinweis">%s</span></div><p class="dank">%s</p>' % (cls, knopf(kn), HINWEIS, DANK)


def form(inner, cls=''):
    return '<form class="rv-form %s" data-vorfuehrung>%s</form>' % (cls, inner)


def sek(n, inner, cls=''):
    return '<section class="kap auf rv rv%02d %s" id="reservieren" data-v="%d">%s</section>' % (n, cls, n, inner)


V = []

# 01 Die Thekenkante: oben Bild der Rückbar und der Titel nebeneinander, darunter alle Felder in einer einzigen Reihe
#    wie die Kante der Theke; die Felder steigen nacheinander auf, das Bild setzt sich von leicht gross auf seine Grösse
def f01(n):
    reihe = ''.join('<div class="rv01-zelle" style="--n:%d">%s</div>' % (j, x) for j, x in enumerate([f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt()]))
    return sek(n, '<div class="innen"><div class="rv01-oben">%s<div>%s%s%s</div></div>%s</div>' % (
        bildf('rueckbar-breit', 'rv01-bild', '(max-width:800px) 92vw, 46vw'), kz(), titel('rv-t rv-gross'), satz(),
        form('<div class="rv01-reihe rv-weg">%s</div>%s' % (reihe, fuss('rv01-fuss')), 'rv01-form')))
V.append(('Die Thekenkante', f01))

# 02 Sechs Hocker: die Theke als Zeichnung mit sechs Hockern; wer «Wie viele» wählt, tippt die Hocker an, die so viele leuchten.
#    Die Hocker fallen beim Auftritt nacheinander an ihren Platz
def f02(n):
    hocker = ''.join('<label class="rv02-h" style="--n:%d"><input type="radio" name="gaeste" value="%d"%s><svg viewBox="0 0 60 120" aria-hidden="true">'
                     '<ellipse class="rv02-sitz" cx="30" cy="12" rx="22" ry="7"/><path class="rv02-bein" d="M16 18 L10 116 M44 18 L50 116 M14 78 H46"/></svg>'
                     '<b>%d</b></label>' % (j, j + 1, ' checked' if j == 3 else '', j + 1) for j in range(6))
    theke = '<div class="rv02-theke"><i class="rv02-licht"></i><div class="rv02-hocker">%s</div></div>' % hocker
    felder = '<div class="rv02-felder rv-weg">%s%s%s%s</div>' % (f_abend(), f_zeit(), f_name(), f_kontakt())
    return sek(n, '<div class="innen"><div class="rv02-kopf">%s%s%s</div>%s</div>' % (
        kz(), titel('rv-t rv-gross'), satz('', True),
        form('<div class="rv02-wahl rv-weg"><span class="etikett">Wie viele · tippt die Hocker an</span><span class="rv02-zahl"><b>4</b> Plätze</span></div>%s%s%s' % (theke, felder, fuss()), 'rv02-form')))
V.append(('Sechs Hocker', f02))

# 03 Ein Satz zum Ausfüllen: kein Formular-Kasten, sondern ein Satz in der Titelschrift, in dem die Lücken die Felder sind;
#    die Zeilen steigen nacheinander aus dem Schlitz
def f03(n):
    zeit = '<select name="zeit" class="rv03-l">%s</select>' % ''.join('<option>%s</option>' % z for z in ZEITEN)
    zeilen = [
        'Wir kommen am <input class="rv03-l rv03-d" type="date" name="datum" aria-label="Abend">',
        'um %s, <input class="rv03-l rv03-k" type="number" name="gaeste" min="1" max="6" placeholder="4" aria-label="Wie viele"> Leute.' % zeit,
        'Ich heisse <input class="rv03-l rv03-n" type="text" name="name" placeholder="Name" aria-label="Name">,',
        'ihr erreicht mich unter <input class="rv03-l rv03-n" type="text" name="kontakt" placeholder="Telefon oder E-Mail" aria-label="Telefon oder E-Mail">.']
    s = ''.join('<span class="rv03-z" style="--n:%d"><span>%s</span></span>' % (j, z) for j, z in enumerate(zeilen))
    return sek(n, '<div class="innen rv03-g"><div>%s%s%s</div>%s</div>' % (
        kz(), titel('rv-t rv-mittelgross'), satz(),
        form('<p class="titel rv03-satz rv-weg">%s</p>%s' % (s, fuss()), 'rv03-form')))
V.append(('Ein Satz zum Ausfüllen', f03))

# 04 Hell und dunkel: der Abschnitt teilt sich randlos; links cremefarben wie die Plakate der Bar mit grossem Titel,
#    rechts dunkel das Formular. Die helle Fläche wächst beim Auftritt von unten auf
def f04(n):
    felder = '<div class="rv-zwei">%s%s</div><div class="rv-zwei">%s%s</div>%s' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="rv04-g"><div class="rv04-hell hell"><div class="rv04-in">%s%s%s</div></div>'
               '<div class="rv04-dunkel">%s</div></div>' % (kz(), titel('rv-t rv-gross'), satz(),
                                                          form('<div class="rv-weg rv-stapel">%s</div>%s' % (felder, fuss()), 'rv04-form')), 'rv04-sek')
V.append(('Hell und dunkel', f04))

# 05 Das Reserviert-Schild: über dem Formular steht ein gefaltetes Tischschild «Reserviert», das sich beim Auftritt
#    aus der Fläche aufstellt; Titel und Satz links
def f05(n):
    schild = ('<div class="rv05-tisch"><div class="rv05-schild"><span class="rv05-logo">%s</span><b>Reserviert</b><span class="etikett">für euch</span></div>'
              '<i class="rv05-kante"></i></div>') % LOGO
    felder = '<div class="rv-zwei">%s%s</div><div class="rv-zwei">%s%s</div>%s' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="innen rv05-g"><div>%s%s%s</div><div>%s%s</div></div>' % (
        kz(), titel('rv-t rv-gross'), satz(), schild, form('<div class="rv-weg rv-stapel">%s</div>%s' % (felder, fuss()), 'rv05-form platte')))
V.append(('Das Reserviert-Schild', f05))

# 06 Wann, wer, wie: das Formular in drei Spalten nebeneinander, darüber zieht sich eine goldene Linie auf,
#    an der die drei Spalten nacheinander hochkommen; Titel gross oben
def f06(n):
    sp = [('Wann', f_abend() + f_zeit()), ('Wer', f_wie() + f_name()), ('Wie', f_kontakt())]
    spalten = ''.join('<div class="rv06-sp" style="--n:%d"><i class="rv06-punkt"></i><span class="rv06-w titel">%s</span>%s</div>' % (j, w, x) for j, (w, x) in enumerate(sp))
    return sek(n, '<div class="innen"><div class="rv06-kopf"><div>%s%s</div>%s</div>%s</div>' % (
        kz(), titel('rv-t rv-gross'), satz('', True),
        form('<div class="rv06-linie"><i></i></div><div class="rv06-reihe rv-weg">%s</div>%s' % (spalten, fuss('rv06-fuss')), 'rv06-form')))
V.append(('Wann, wer, wie', f06))

# 07 Der Bogen: links das Bild durch die Tür auf den roten Boden in einem hohen Bogen, wie ein Eingang;
#    das Bild setzt sich beim Auftritt von gross auf seine Grösse, rechts Titel und Formular untereinander
def f07(n):
    felder = '<div class="rv-zwei">%s%s</div><div class="rv-zwei">%s%s</div>%s' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="innen rv07-g"><div class="rv07-bogen">%s</div><div>%s%s%s%s</div></div>' % (
        bildf('tuer-rot', 'rv07-bild', '(max-width:800px) 92vw, 38vw'), kz(), titel('rv-t rv-gross'), satz(),
        form('<div class="rv-weg rv-stapel">%s</div>%s' % (felder, fuss()), 'rv07-form')))
V.append(('Der Bogen', f07))

# 08 Nur Schrift: der Titel sehr gross über die ganze Breite, rechts unten daneben der Satz;
#    darunter das Formular als ruhige Fläche mit Linien statt Kästen; kein Foto
def f08(n):
    felder = '<div class="rv08-raster rv-weg">%s%s%s%s%s</div>' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="innen">%s<div class="rv08-kopf">%s%s</div>%s</div>' % (
        kz(), titel('rv-t rv08-t'), satz('rv08-satz'), form(felder + fuss('rv08-fuss'), 'rv08-form rv-linien')))
V.append(('Nur Schrift', f08))

# 09 Drei Bilder vom Abend: oben drei hohe Bilder (Theke, voller Abend, Momo am Glas), die versetzt hochkommen und
#    in verschiedener Höhe stehen bleiben; darunter Titel links, Formular rechts
def f09(n):
    bil = ''.join('<div class="rv09-b" style="--n:%d">%s</div>' % (j, bildf(k, '', '(max-width:800px) 46vw, 26vw')) for j, k in enumerate(['theke', 'voll', 'momo-giesst']))
    felder = '<div class="rv-zwei">%s%s</div><div class="rv-zwei">%s%s</div>%s' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="innen"><div class="rv09-reihe">%s</div><div class="rv09-g"><div>%s%s%s</div>%s</div></div>' % (
        bil, kz(), titel('rv-t rv-gross'), satz(), form('<div class="rv-weg rv-stapel">%s</div>%s' % (felder, fuss()), 'rv09-form platte')))
V.append(('Drei Bilder vom Abend', f09))

# 10 Wie eine Karte: das Formular auf einer cremefarbenen Karte mit der Wortmarke oben und gepunkteten Linien wie eine Getränkekarte,
#    die Punkte laufen beim Auftritt zum Feld hin; daneben zwei Drinks auf dem Tisch
def f10(n):
    zeilen = [('Abend', '<input type="date" name="datum" aria-label="Abend">'),
              ('Uhrzeit', '<select name="zeit" aria-label="Uhrzeit">%s</select>' % ''.join('<option>%s</option>' % z for z in ZEITEN)),
              ('Wie viele', '<input type="number" name="gaeste" min="1" max="6" placeholder="z. B. 4" aria-label="Wie viele">'),
              ('Name', '<input type="text" name="name" aria-label="Name">'),
              ('Telefon oder E-Mail', '<input type="text" name="kontakt" aria-label="Telefon oder E-Mail">')]
    z = ''.join('<div class="rv10-z" style="--n:%d"><span>%s</span><i></i>%s</div>' % (j, E(l), x) for j, (l, x) in enumerate(zeilen))
    karte = form('<span class="rv10-logo">%s</span><span class="etikett rv10-et">Reservierung</span><div class="rv-weg">%s</div>%s' % (LOGO, z, fuss('', 'rot')), 'rv10-karte hell')
    return sek(n, '<div class="innen rv10-g"><div>%s%s%s%s</div>%s</div>' % (
        kz(), titel('rv-t rv-gross'), satz(), bildf('glas-zwei', 'rv10-bild', '(max-width:800px) 60vw, 22vw'), karte))
V.append(('Wie eine Karte', f10))

# 11 Momo hinter der Bar: das Bild läuft links bis an den Rand und über die ganze Höhe des Abschnitts,
#    rechts Titel und Formular; das Bild zoomt beim Auftritt langsam auf seine Grösse
def f11(n):
    felder = '<div class="rv-zwei">%s%s</div><div class="rv-zwei">%s%s</div>%s' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="rv11-g">%s<div class="rv11-r">%s%s%s%s</div></div>' % (
        bildf('momo-lacht', 'rv11-bild', '(max-width:800px) 100vw, 46vw', '50% 30%'), kz(), titel('rv-t rv-gross'), satz(),
        form('<div class="rv-weg rv-stapel">%s</div>%s' % (felder, fuss()), 'rv11-form')), 'rv11-sek')
V.append(('Momo hinter der Bar', f11))

# 12 Die nächsten Abende: statt Kalender stehen die nächsten drei offenen Abende als grosse Karten da (Donnerstag, Freitag, Samstag
#    mit Datum, aus dem heutigen Tag gerechnet), ein Tipp wählt; darunter die Uhrzeit als vier Felder. Die Karten klappen nacheinander hoch
def f12(n):
    abende = ''.join('<label class="rv12-a" style="--n:%d"><input type="radio" name="datum"%s><span class="rv12-tag etikett"></span><b class="rv12-dat"></b><span class="rv12-bis"></span></label>' % (
        j, ' checked' if j == 0 else '') for j in range(3))
    zeiten = ''.join('<label class="rv12-u"><input type="radio" name="zeit" value="%s"%s><span>%s</span></label>' % (z, ' checked' if j == 0 else '', z) for j, z in enumerate(ZEITEN))
    felder = '<div class="rv-zwei">%s%s</div>%s' % (f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="innen rv12-g"><div>%s%s%s%s</div>%s</div>' % (
        kz(), titel('rv-t rv-gross'), satz(), bildf('schild-ecke', 'rv12-bild', '(max-width:800px) 60vw, 24vw', '50% 40%'),
        form('<div class="rv-weg"><span class="etikett rv12-et">Welcher Abend</span><div class="rv12-abende" data-abende>%s</div>'
             '<span class="etikett rv12-et">Uhrzeit</span><div class="rv12-zeiten">%s</div><div class="rv-stapel">%s</div></div>%s' % (abende, zeiten, felder, fuss()), 'rv12-form platte')))
V.append(('Die nächsten Abende', f12))

# 13 Ruhig in der Mitte: alles mittig untereinander, Titel gross, darunter eine schmale Spalte mit Feldern als feine Linien;
#    die Linien ziehen sich beim Auftritt von der Mitte aus auf
def f13(n):
    felder = '<div class="rv13-spalte rv-weg">%s<div class="rv-zwei">%s%s</div>%s%s</div>' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="innen rv13-g">%s%s%s%s</div>' % (kz('rv13-kz'), titel('rv-t rv-gross'), satz('rv13-satz'),
                                                               form(felder + fuss('rv13-fuss'), 'rv13-form rv-linien')))
V.append(('Ruhig in der Mitte', f13))

# 14 Zwei bis sechs: links drei grosse Zahlen, wie viele an welchem Platz sitzen (2 bis 6 an der Theke, ab 10 die lange Tafel,
#    ab 30 die ganze Bar), die Zahlen steigen nacheinander aus dem Schlitz; rechts das Formular
def f14(n):
    za = [('2–6', 'An der Theke', 'Hier reservieren'), ('ab 10', 'Die lange Tafel', '<a href="tafel.html">unter Feiern</a>'), ('ab 30', 'Die ganze Bar', '<a href="tafel.html">unter Feiern</a>')]
    zahlen = ''.join('<div class="rv14-z" style="--n:%d"><span class="rv14-sch"><b class="titel">%s</b></span><span><span class="etikett">%s</span><em>%s</em></span></div>' % (j, E(z), E(w), x) for j, (z, w, x) in enumerate(za))
    felder = '<div class="rv-zwei">%s%s</div><div class="rv-zwei">%s%s</div>%s' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    return sek(n, '<div class="innen">%s%s<div class="rv14-g"><div class="rv14-zahlen">%s<p class="text">Die Bar bestätigt per Nachricht.</p></div>%s</div></div>' % (
        kz(), titel('rv-t rv-gross'), zahlen, form('<div class="rv-weg rv-stapel">%s</div>%s' % (felder, fuss()), 'rv14-form platte')))
V.append(('Zwei bis sechs', f14))

# 15 Drei Wege: drei Karten nebeneinander, links das Formular, daneben Anrufen (beide Nummern) und Schreiben (Instagram),
#    wie die Bar es selbst sagt; die Karten kommen gestaffelt hoch und richten sich gerade
def f15(n):
    felder = '<div class="rv-zwei">%s%s</div><div class="rv-zwei">%s%s</div>%s' % (f_abend(), f_zeit(), f_wie(), f_name(), f_kontakt())
    k1 = '<div class="rv15-k rv15-form-k" style="--n:0;--r:-1.5deg"><span class="titel rv15-w">Eintragen</span>%s</div>' % form('<div class="rv-weg rv-stapel">%s</div>%s' % (felder, fuss()), 'rv15-form')
    k2 = ('<div class="rv15-k hell" style="--n:1;--r:1.5deg"><span class="titel rv15-w">Anrufen</span><p class="text">An einem offenen Abend, Donnerstag bis Samstag ab 19 Uhr.</p>'
          '<a class="rv15-gross" href="tel:%s">%s</a><a class="rv15-gross" href="tel:%s">%s</a></div>') % (HAUS['tel_href'], E(HAUS['telefon']), HAUS['tel2_href'], E(HAUS['telefon2']))
    k3 = ('<div class="rv15-k" style="--n:2;--r:-1deg"><span class="titel rv15-w">Schreiben</span><p class="text">Eine Nachricht auf Instagram, die Bar antwortet.</p>'
          '<a class="knopf klein" href="%s" rel="noopener"><span>%s</span><i>%s</i></a></div>') % (HAUS['instagram'], 'Auf Instagram', PFEIL)
    return sek(n, '<div class="innen"><div class="rv15-kopf"><div>%s%s</div>%s</div><div class="rv15-reihe">%s%s%s</div></div>' % (
        kz(), titel('rv-t rv-gross'), satz(), k1, k2, k3))
V.append(('Drei Wege', f15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/rv.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    schluss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
               '<script src="%s/rv.js?v=%s" defer></script><script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schluss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
