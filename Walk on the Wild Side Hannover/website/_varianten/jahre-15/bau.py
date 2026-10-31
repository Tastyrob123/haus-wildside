# Walk on the Wild Side · Das Haus · Abschnitt «Was bisher geschah.» (id="seit2017"), 15 Fassungen (31.10.2026).
# Robert: «gib mir 15 alternative visualierungen für den abschnitt». Texte und Jahre bleiben wörtlich (aus unter.py),
# je Fassung eine eigene Darstellung und eine eigene Bewegung, nur transform, alles ab dem ersten Bild deckend.
# Wechsel mit ← → (varianten-nav.js). Aufruf: python3 _varianten/jahre-15/bau.py → 00.html … 15.html
import os, sys, json, re
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, LOGO, mache, img_tag

ORD = '_varianten/jahre-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('jahre.css', 'jahre.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('haus.html').read()
a = basis.index('<section class="kap hell auf" id="seit2017">')
b = basis.index('</section>', a) + len('</section>')
HEUTE = basis[a:b]
KOPF_HTML = HEUTE[HEUTE.index('<div class="innen">') + len('<div class="innen">'):HEUTE.index('<div class="platte hell"')]

# die Jahre wörtlich aus unter.py
src = open('unter.py').read()
blk = src[src.index('    jahre = ['):src.index('    stimmen = [')]
JAHRE = re.findall(r"\('(\d{4})', '([^']+)'\)", blk)
assert [j for j, _ in JAHRE] == ['2018', '2023', '2024', '2025', '2027'], JAHRE

# Fotos je Jahr, nur was belegt dazu passt (Beschreibungen in bilder.py)
FOTO = {'2018': ('momo-flaschen', '50% 35%'),   # Momo hinter den Flaschen
        '2023': ('fw-a12', '50% 50%'),          # Der Raum am 9. November 2023
        '2024': ('konzert-scharf', '50% 45%'),  # Konzert in der Bar
        '2025': ('p-0906', '50% 50%'),          # Plakat SESSION mit Björn, 06.09.2025
        '2027': ('voll', '50% 50%')}            # Ein voller Abend


def k(key, cls='', sizes='30vw', pos=None, stil=''):
    pos = pos or FOTO.get(key, (None, '50% 50%'))[1]
    return '<figure class="kachel ja-k %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(key)['lq'], stil, img_tag(key, sizes, extra=' style="object-position:%s"' % pos))


def fk(jahr, cls='', sizes='30vw', stil=''):
    key, pos = FOTO[jahr]
    return k(key, cls, sizes, pos, stil)


def kap(n, inner, voll=False, nacht=False):
    return '<section class="kap %s auf ja v%02d" id="seit2017" data-v="%d"><div class="innen">%s</div>%s</section>' % (
        'nacht-ja' if nacht else 'hell', n, n, KOPF_HTML, inner if voll else '<div class="innen">%s</div>' % inner)


def zif(j):
    """Jahreszahl, jede Ziffer einzeln (für Ziffern-Bewegungen)."""
    return ''.join('<i>%s</i>' % c for c in j)


V = []

# 01 Fünf Spalten: die Jahre nebeneinander, Zahl oben, Text darunter, feine Goldlinien dazwischen; die Spalten steigen nacheinander herauf
V.append(('Fünf Spalten', lambda n: kap(n, '<div class="v01-g">%s</div>' % ''.join(
    '<div class="jx" style="--n:%d"><span class="j-z">%s</span><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 02 Goldene Linie quer: eine Linie über die ganze Breite, je Jahr ein Punkt darauf, Zahl darüber, Text darunter; die Linie zieht sich von links, die Punkte springen auf
V.append(('Goldene Linie quer', lambda n: kap(n, '<div class="v02-g"><span class="v02-l"></span>%s</div>' % ''.join(
    '<div class="jx" style="--n:%d"><span class="j-z">%s</span><b class="v02-p"></b><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 03 Mittelachse: senkrechte Goldlinie in der Mitte, die Jahre abwechselnd links und rechts; die Linie wächst beim Scrollen mit
V.append(('Mittelachse', lambda n: kap(n, '<div class="v03-g"><span class="v03-l"><i></i></span>%s</div>' % ''.join(
    '<div class="jx %s" style="--n:%d"><b class="v03-p"></b><span class="j-z">%s</span><p>%s</p></div>' % ('li' if i % 2 == 0 else 're', i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 04 Riesenzahlen: je Jahr eine Zeile, die Zahl riesig und hell links, der Text rechts auf ihrer Grundlinie; die Zahl steigt aus dem Schlitz
V.append(('Riesenzahlen', lambda n: kap(n, '<div class="v04-g">%s</div>' % ''.join(
    '<div class="jx" style="--n:%d"><span class="j-z"><span>%s</span></span><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 05 Fotos im Wechsel: je Jahr ein Hochbild, abwechselnd links und rechts, daneben Zahl und Text; das Foto zoomt in seinen Rahmen
V.append(('Fotos im Wechsel', lambda n: kap(n, '<div class="v05-g">%s</div>' % ''.join(
    '<div class="jx %s" style="--n:%d">%s<div class="v05-t"><span class="j-z">%s</span><p>%s</p></div></div>' % (
        're' if i % 2 else 'li', i, fk(j, 'v05-b', '(max-width:900px) 92vw, 34vw'), j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 06 Nachtkarten: fünf dunkle Karten wie Tickets der Bar, Zahl in Gold, Text in Creme; jede Karte liegt nach hinten gekippt und richtet sich auf
V.append(('Nachtkarten', lambda n: kap(n, '<div class="v06-g">%s</div>' % ''.join(
    '<div class="jx" style="--n:%d"><span class="v06-o">Walk on the Wild Side</span><span class="j-z">%s</span><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 07 Die Zahl bleibt stehen: links steht eine grosse Jahreszahl, rechts ziehen die Jahre vorbei; die Ziffern rollen zum jeweiligen Jahr
V.append(('Die Zahl bleibt stehen', lambda n: kap(n, '<div class="v07-g"><div class="v07-l"><div class="v07-uhr">%s</div><span class="v07-u">Wild Side, Linden</span></div><div class="v07-r">%s</div></div>' % (
    ''.join('<span class="v07-s"><span>%s</span></span>' % ''.join('<i>%s</i>' % c for c in '0123456789') for _ in range(4)),
    ''.join('<div class="jx" data-j="%s" style="--n:%d"><span class="j-z">%s</span><p>%s</p></div>' % (j, i, j, E(t)) for i, (j, t) in enumerate(JAHRE))))))

# 08 Band mit Bildern: die Jahre als Karten in einem Band, das man seitlich schiebt; Foto oben, Zahl und Text darunter; die Karten kommen gestaffelt herauf
V.append(('Band mit Bildern', lambda n: kap(n, '<div class="v08-band">%s</div><p class="v08-h">Seitlich schieben</p>' % ''.join(
    '<div class="jx" style="--n:%d">%s<span class="j-z">%s</span><p>%s</p></div>' % (i, fk(j, 'v08-b', '360px'), j, E(t)) for i, (j, t) in enumerate(JAHRE)), voll=False)))

# 09 Wie die Karte der Bar: mittig gesetzt, je Jahr ein Absatz, die Zahl zwischen zwei Goldlinien; die Linien ziehen sich von der Mitte auf
V.append(('Wie eine Karte', lambda n: kap(n, '<div class="v09-g"><span class="logo v09-logo">%s</span>%s</div>' % (LOGO, ''.join(
    '<div class="jx" style="--n:%d"><div class="v09-z"><i></i><span class="j-z">%s</span><i></i></div><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE))))))

# 10 Treppe: jedes Jahr eine Stufe weiter rechts und tiefer, wie die Stufen zur Empore; die Stufen gleiten beim Scrollen verschieden schnell
V.append(('Treppe', lambda n: kap(n, '<div class="v10-g">%s</div>' % ''.join(
    '<div class="jx" style="--n:%d"><span class="j-z">%s</span><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 11 Medaillons: je Jahr ein goldener Ring mit der Zahl, der Text darunter; der Ring zieht sich einmal herum
RING = '<svg class="v11-r" viewBox="0 0 200 200" aria-hidden="true"><circle cx="100" cy="100" r="96" pathLength="100"/></svg>'
V.append(('Medaillons', lambda n: kap(n, '<div class="v11-g">%s</div>' % ''.join(
    '<div class="jx" style="--n:%d"><div class="v11-m">%s<span class="j-z">%s</span></div><p>%s</p></div>' % (i, RING, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 12 Plakate: jedes Jahr ein Plakat in den Farben der Bar (Nacht, Rot, Blau), Zahl riesig, Text unten; die Plakate hängen schief und rücken sich gerade
V.append(('Plakate', lambda n: kap(n, '<div class="v12-g">%s</div>' % ''.join(
    '<div class="jx f%d" style="--n:%d"><span class="v12-o">Walk on the Wild Side · Hannover</span><span class="j-z">%s</span><p>%s</p></div>' % (i % 3, i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 13 Lineal: ein Lineal von 2018 bis 2027 mit einem Strich je Jahr, die fünf Jahre gross in Gold; die Texte stehen unter ihrem Strich, die Striche wachsen nacheinander
def v13(n):
    striche = ''.join('<span class="v13-s %s" style="--n:%d"><i></i><b>%s</b></span>' % ('an' if str(y) in dict(JAHRE) else '', y - 2018, y if str(y) in dict(JAHRE) else y) for y in range(2018, 2028))
    texte = ''.join('<div class="jx" style="--n:%d"><span class="j-z">%s</span><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE))
    return kap(n, '<div class="v13-g"><div class="v13-lin">%s</div><div class="v13-t">%s</div></div>' % (striche, texte))
V.append(('Lineal', v13))

# 14 Zeitung: die Jahre als Zeitungsseite in drei Spalten, jede Meldung beginnt mit der Zahl als grossem Anfang; die Zeilen steigen aus dem Schlitz
V.append(('Zeitung', lambda n: kap(n, '<div class="v14-g"><div class="v14-kopf"><span>Lindener Chronik</span><span>Haasemannstraße 13</span></div><div class="v14-sp">%s</div></div>' % ''.join(
    '<div class="jx" style="--n:%d"><span class="j-z">%s</span><p>%s</p></div>' % (i, j, E(t)) for i, (j, t) in enumerate(JAHRE)))))

# 15 Stapel: jedes Jahr eine Tafel, die beim Scrollen oben stehen bleibt; die nächste legt sich darüber, bis alle fünf aufeinander liegen
V.append(('Stapel', lambda n: kap(n, '<div class="v15-g">%s</div>' % ''.join(
    '<div class="jx" style="--n:%d"><span class="j-z">%s</span><p>%s</p>%s</div>' % (i, j, E(t), fk(j, 'v15-b', '(max-width:900px) 40vw, 22vw')) for i, (j, t) in enumerate(JAHRE)))))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
BASE = '<base href="../../">'
KOPF = '<link rel="stylesheet" href="%s/jahre.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head>' + BASE, 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/jahre.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, HEUTE, 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(j + 1), name))
    print('16 Seiten gebaut')
