# Walk on the Wild Side · Besuch-Seite, Abschnitt «Gut zu wissen» (id="fragen"), 15 Fassungen (31.10.2026).
# Robert: «Jetzt überleg dir bitte für den Bereich noch was Schönes.» Fragen und Antworten wörtlich aus der heutigen Seite;
# je Fassung eigener Aufbau und eigene Bewegung, nur transform/opacity. Wechsel mit ← → (varianten-nav.js).
# Aufruf: python3 _varianten/fragen-15/bau.py
import os, sys, json, re, html as H
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, mache, img_tag, LOGO, PFEIL

ORD = '_varianten/fragen-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('fq.css', 'fq.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('besuch.html').read()
assert len(basis) > 10000, 'besuch.html leer (anderer Bau läuft?)'
a = basis.index('<section class="kap auf" id="fragen">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]
# Fragen und Antworten aus der heutigen Seite lesen (eine Quelle)
F = [(H.unescape(q), H.unescape(x)) for q, x in re.findall(r'<summary><span>(.*?)</span><i></i></summary><p>(.*?)</p>', HEUTE)]
assert len(F) == 7, len(F)
KURZ = ['Karte', 'Preise', 'Ohne Alkohol', 'Eintritt', 'Essen', 'Draussen', 'Feiern']
BILD = ['momo-giesst', 'glas-negroni', 'glas-zwei', 'konzert', 'tafel-teller', 'terrasse', 'an-empore']
ANZ = 'Sieben Fragen'


def bildf(key, cls='', sizes='40vw', pos=None, extra_attr=''):
    extra = ' style="object-position:%s"' % pos if pos else ''
    return '<figure class="fq-bild %s" style="--lq:url(%s)"%s>%s</figure>' % (cls, mache(key)['lq'], extra_attr, img_tag(key, sizes, extra=extra))


def kz(cls=''):
    return '<div class="kz fq-kz %s"><span class="uhr">Gut zu wissen</span><i></i><span class="was">%s</span></div>' % (cls, ANZ)


def titel(cls='fq-t'):
    return '<h2 class="titel %s"><span class="fq-z"><span>Was Gäste</span></span><span class="fq-z"><span>vorher fragen.</span></span></h2>' % cls


def akk(cls='', offen=0, extra=None):
    """Aufklappen, immer nur eine offen (fq.js). extra(j) liefert zusätzlichen Inhalt in der Antwort."""
    return '<div class="fq-akk %s" data-fq-eins>%s</div>' % (cls, ''.join(
        '<details%s style="--n:%d" data-j="%d"><summary><span>%s</span><i class="fq-pm"></i></summary><div class="fq-a"><p>%s</p>%s</div></details>' % (
            ' open' if j == offen else '', j, j, E(q), E(x), extra(j) if extra else '') for j, (q, x) in enumerate(F)))


def sek(n, inner, cls=''):
    return '<section class="kap auf fq fq%02d %s" id="fragen" data-v="%d">%s</section>' % (n, cls, n, inner)


V = []

# 01 Mit Bild: links unter dem Titel ein hohes Bild der Theke, damit die linke Seite nicht leer steht; rechts die Fragen wie heute,
#    sie steigen einzeln auf, das Bild setzt sich von gross auf seine Grösse
def f01(n):
    return sek(n, '<div class="innen fq-zwei"><div>%s%s%s</div>%s</div>' % (
        kz(), titel(), bildf('theke', 'fq01-bild', '(max-width:800px) 92vw, 34vw'), akk('fq-liste')))
V.append(('Mit Bild', f01))

# 02 Das Bild antwortet mit: links ein Bild, das zur offenen Frage wechselt (Momo am Glas, Negroni, zwei Drinks, Konzert, Teller, Terrasse, Empore);
#    rechts die Fragen
def f02(n):
    bil = ''.join(bildf(k, 'fq02-b%s' % (' an' if j == 0 else ''), '(max-width:800px) 92vw, 36vw', extra_attr=' data-fq-bild="%d"' % j) for j, k in enumerate(BILD))
    return sek(n, '<div class="innen fq-zwei"><div>%s%s<div class="fq02-rahmen">%s</div></div>%s</div>' % (kz(), titel(), bil, akk('fq-liste', extra=None)), 'fq-mitbild')
V.append(('Das Bild antwortet mit', f02))

# 03 Alles offen: Fragen und Antworten stehen offen in zwei Spalten, nichts zum Aufklappen; jedes Paar steigt einzeln auf
def f03(n):
    paare = ''.join('<div class="fq03-p" style="--n:%d"><h3 class="titel">%s</h3><p>%s</p></div>' % (j, E(q), E(x)) for j, (q, x) in enumerate(F))
    return sek(n, '<div class="innen">%s%s<div class="fq03-raster">%s</div></div>' % (kz(), titel('fq-t fq-gross'), paare))
V.append(('Alles offen', f03))

# 04 Ein Gespräch: die Frage rechts in Gold wie vom Gast, die Antwort links in Creme wie von der Bar; Zeile für Zeile beim Scrollen
def f04(n):
    z = ''.join('<div class="fq04-paar"><p class="fq04-q titel">%s</p><p class="fq04-x">%s</p></div>' % (E(q), E(x)) for q, x in F)
    return sek(n, '<div class="innen fq04-in"><div class="fq04-kopf">%s%s</div>%s</div>' % (kz(), titel('fq-t fq-gross'), z))
V.append(('Ein Gespräch', f04))

# 05 Sieben Bierdeckel: runde Deckel in Creme mit der Frage; ein Tipp dreht den Deckel um, hinten steht die Antwort
def f05(n):
    d = ''.join('<button type="button" class="fq05-d" style="--n:%d;--r:%ddeg" data-fq-dreh aria-pressed="false"><span class="fq05-in"><span class="fq05-v"><b class="titel">%s</b><i>umdrehen</i></span>'
                '<span class="fq05-h"><span>%s</span></span></span></button>' % (j, r, E(q), E(x)) for j, ((q, x), r) in enumerate(zip(F, (-6, 4, -3, 7, -5, 3, -2))))
    return sek(n, '<div class="innen"><div class="fq05-kopf">%s%s<p class="text">Tippt einen Deckel an, auf der Rückseite steht die Antwort.</p></div><div class="fq05-tisch">%s</div></div>' % (kz(), titel('fq-t fq-gross'), d))
V.append(('Sieben Bierdeckel', f05))

# 06 Wie eine Getränkekarte: eine cremefarbene Karte mit der Wortmarke, die Fragen stehen wie Drinks mit gepunkteter Linie,
#    die Antwort klappt darunter in kleiner Schrift auf
def f06(n):
    return sek(n, '<div class="innen fq06-g"><div>%s%s</div><div class="fq06-karte hell"><span class="fq06-logo">%s</span><span class="etikett">Gut zu wissen</span>%s</div></div>' % (
        kz(), titel('fq-t'), LOGO, akk('fq06-akk')))
V.append(('Wie eine Getränkekarte', f06))

# 07 Sieben Stichworte: oben die Stichworte in einer Reihe (Karte, Preise, Ohne Alkohol …), darunter gross die Frage und ihre Antwort,
#    rechts das passende Bild; beim Wechsel steigt die Antwort neu auf
def f07(n):
    w = ''.join('<button type="button" class="fq07-w%s" data-fq-reiter="%d">%s</button>' % (' an' if j == 0 else '', j, E(k)) for j, k in enumerate(KURZ))
    tafeln = ''.join('<div class="fq07-tafel%s" data-fq-tafel="%d"><div><h3 class="titel"><span>%s</span></h3><p>%s</p></div>%s</div>' % (
        ' an' if j == 0 else '', j, E(q), E(x), bildf(BILD[j], 'fq07-bild', '(max-width:800px) 92vw, 30vw')) for j, (q, x) in enumerate(F))
    return sek(n, '<div class="innen">%s%s<div class="fq07-reihe" role="tablist">%s</div><div class="fq07-buehne">%s</div></div>' % (kz(), titel('fq-t fq-gross'), w, tafeln))
V.append(('Sieben Stichworte', f07))

# 08 Ein Band zum Blättern: hohe Karten nebeneinander, oben das Bild, darunter Frage und Antwort; seitlich wischen oder scrollen
def f08(n):
    k = ''.join('<article class="fq08-k" style="--n:%d">%s<h3 class="titel">%s</h3><p>%s</p></article>' % (j, bildf(BILD[j], '', '(max-width:800px) 78vw, 340px'), E(q), E(x)) for j, (q, x) in enumerate(F))
    return sek(n, '<div class="innen fq08-kopf"><div>%s%s</div><p class="text">Zur Seite wischen.</p></div><div class="fq08-band"><div class="fq08-spur">%s</div></div>' % (kz(), titel('fq-t fq-gross'), k))
V.append(('Ein Band zum Blättern', f08))

# 09 An der Goldlinie: eine Goldlinie läuft senkrecht durch die Mitte, die Fragen stehen abwechselnd links und rechts daran,
#    an jedem Paar ein Goldpunkt; die Linie zieht sich beim Scrollen mit auf
def f09(n):
    z = ''.join('<div class="fq09-p %s" style="--n:%d"><i class="fq09-punkt"></i><div><h3 class="titel">%s</h3><p>%s</p></div></div>' % ('l' if j % 2 == 0 else 'r', j, E(q), E(x)) for j, (q, x) in enumerate(F))
    return sek(n, '<div class="innen"><div class="fq09-kopf">%s%s</div><div class="fq09-weg"><i class="fq09-linie"></i>%s</div></div>' % (kz('fq09-kz'), titel('fq-t fq-gross'), z))
V.append(('An der Goldlinie', f09))

# 10 Hell wie ein Plakat: der Abschnitt wird cremefarben wie die Plakate der Bar, dunkle Schrift, das Plus wird rot;
#    Titel gross links, die Fragen rechts
def f10(n):
    return sek(n, '<div class="innen fq-zwei"><div>%s%s</div>%s</div>' % (kz(), titel('fq-t fq-gross'), akk('fq-liste fq10-akk')), 'hell fq10-sek')
V.append(('Hell wie ein Plakat', f10))

# 11 Eine Frage nach der anderen: in der Mitte steht gross eine Frage mit ihrer Antwort, Pfeile links und rechts blättern weiter,
#    darunter sieben Punkte; die neue Frage steigt aus dem Schlitz
def f11(n):
    s = ''.join('<div class="fq11-s%s" data-fq-schritt="%d"><h3 class="titel"><span>%s</span></h3><p>%s</p></div>' % (' an' if j == 0 else '', j, E(q), E(x)) for j, (q, x) in enumerate(F))
    punkte = ''.join('<button type="button" class="fq11-pt%s" data-fq-geh="%d" aria-label="%s"></button>' % (' an' if j == 0 else '', j, E(q)) for j, (q, x) in enumerate(F))
    pf = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return sek(n, '<div class="innen fq11-in" data-fq-blatt>%s%s<div class="fq11-buehne"><button type="button" class="fq11-pf zur" data-fq-schub="-1" aria-label="Vorige Frage">%s</button>'
               '<div class="fq11-s-wrap">%s</div><button type="button" class="fq11-pf" data-fq-schub="1" aria-label="Nächste Frage">%s</button></div><div class="fq11-punkte">%s</div></div>' % (
                   kz('fq11-kz'), titel('fq-t fq-mittel'), pf, s, pf, punkte))
V.append(('Eine Frage nach der anderen', f11))

# 12 Zettel an der Theke: sieben cremefarbene Zettel, leicht schief, mit einem Goldpunkt angeheftet; Frage und Antwort stehen offen darauf.
#    Die Zettel fallen nacheinander an ihren Platz und richten sich aus
def f12(n):
    z = ''.join('<div class="fq12-z hell" style="--n:%d;--r:%sdeg"><i class="fq12-nadel"></i><h3 class="titel">%s</h3><p>%s</p></div>' % (j, r, E(q), E(x)) for j, ((q, x), r) in enumerate(zip(F, ('-2', '1.5', '-1', '2', '-1.5', '1', '-2.5'))))
    return sek(n, '<div class="innen"><div class="fq12-kopf">%s%s</div><div class="fq12-wand">%s</div></div>' % (kz(), titel('fq-t fq-gross'), z))
V.append(('Zettel an der Theke', f12))

# 13 Frage links, Antwort rechts: über die ganze Breite je eine Zeile, links die Frage in der Titelschrift, rechts die Antwort,
#    dazwischen feine Goldlinien, die sich von links aufziehen
def f13(n):
    z = ''.join('<div class="fq13-z" style="--n:%d"><i class="fq13-l"></i><h3 class="titel">%s</h3><p>%s</p></div>' % (j, E(q), E(x)) for j, (q, x) in enumerate(F))
    return sek(n, '<div class="innen"><div class="fq13-kopf">%s%s</div><div class="fq13-tab">%s</div></div>' % (kz(), titel('fq-t fq-gross'), z))
V.append(('Frage links, Antwort rechts', f13))

# 14 Antwort mit Bild: die Fragen gehen über die ganze Breite; wer eine öffnet, sieht links die Antwort und rechts das passende Bild
def f14(n):
    return sek(n, '<div class="innen"><div class="fq14-kopf">%s%s</div>%s</div>' % (
        kz(), titel('fq-t fq-gross'), akk('fq-liste fq14-akk', extra=lambda j: bildf(BILD[j], 'fq14-bild', '(max-width:800px) 92vw, 30vw'))))
V.append(('Antwort mit Bild', f14))

# 15 In der Mitte: alles mittig, die Fragen gross untereinander; die offene Frage leuchtet in Gold, die Antwort steht mittig darunter
def f15(n):
    return sek(n, '<div class="innen fq15-in">%s%s%s</div>' % (kz('fq15-kz'), titel('fq-t fq-gross'), akk('fq15-akk')))
V.append(('In der Mitte', f15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/fq.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    schluss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
               '<script src="%s/fq.js?v=%s" defer></script><script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schluss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('00.html … 15.html in', ORD)
