# Walk on the Wild Side · Startseite, Eckschild im Abschnitt «bar»: zehn Fassungen für Wer, Wo, Wann (29.10.2026).
# Robert: «ich mag auch nicht, dass wie da drin so diese drei Sachen rechts sind, das kriegen wir alles noch ein bisschen edler und schöner hin».
# Nur der untere Teil des Schilds (Satz und Wer, Wo, Wann) wechselt; Wortlaut bleibt, alles andere bleibt wie eingebaut. 00 = heute.
# Wechsel mit ← →. Aufruf: python3 _varianten/fakten/bau.py → 00.html … 10.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, HAUS

ORD = '_varianten/fakten'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('fakten.css', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('index.html').read()
a = basis.index('<div class="es-unten">')
b = basis.index('</div></div></div>', a) + len('</div></div></div>')

SATZ = ('So nennt sich das Wild Side selbst, und so ist es gemeint: eine kleine Bar an der Ecke, in der man sich kennt, mit Drinks, für die man sonst weit fahren müsste. '
        'Seit 2017 unter dieser Decke, seit November 2023 mit Derya und Momo hinter der Theke. Im Falstaff Bar Guide 2027 mit 91 Punkten.')
F = [('Wer', 'Derya Ivkin führt die Bar, Momo Ben Khelifa mixt'), ('Wo', HAUS['adresse'] + ', ' + HAUS['ecke']),
     ('Wann', HAUS['zeit_kurz'].replace(' · ', '<br>'))]
S = '<p class="text sw" style="--i:3">%s</p>' % E(SATZ)
ZEICHEN = {  # feine Linien in Gold: Person, Ort, Uhr
    'Wer': '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="11" r="5"/><path d="M6 27c1.5-5.5 5.5-8 10-8s8.5 2.5 10 8"/></svg>',
    'Wo': '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 28s-8-8.5-8-15a8 8 0 0 1 16 0c0 6.5-8 15-8 15z"/><circle cx="16" cy="13" r="3"/></svg>',
    'Wann': '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="11"/><path d="M16 9v7l5 3"/></svg>'}


def spalten(cls, inhalt=lambda x, y: '<span class="etikett">%s</span><p>%s</p>' % (E(x), y)):
    return '<div class="ef %s sw" style="--i:4">%s</div>' % (cls, ''.join('<div>%s</div>' % inhalt(x, y) for x, y in F))


V = [
    ('Drei Spalten unter dem Satz', 'Satz über die ganze Breite, darunter Wer, Wo, Wann nebeneinander, getrennt von feinen Goldlinien, der Inhalt in der Titelschrift.',
     lambda: S + spalten('f01')),
    ('Die Messingleiste', 'Unten im Schild eine eigene Leiste mit Goldkante wie das Schild an der Hausecke, darin Wer, Wo, Wann nebeneinander.',
     lambda: S + spalten('f02')),
    ('Goldene Wörter', 'Wer, Wo und Wann stehen gross in Gold in der Titelschrift, der Inhalt ruhig darunter.',
     lambda: S + spalten('f03', lambda x, y: '<b>%s</b><p>%s</p>' % (E(x), y))),
    ('Drei Plaketten', 'Jede Angabe auf einer eigenen kleinen Plakette mit Goldrand, alle drei gleich hoch nebeneinander.',
     lambda: S + spalten('f04')),
    ('Zeilen über die ganze Breite', 'Wer, Wo, Wann als drei lange Zeilen mit Goldlinie, der Inhalt in der Titelschrift, die Zeiten in einer Zeile.',
     lambda: S + '<div class="ef f05 sw" style="--i:4">%s</div>' % ''.join('<div><span class="etikett">%s</span><p>%s</p></div>' % (E(x), y.replace('<br>', ' · ')) for x, y in F)),
    ('Oben am Schild', 'Wer, Wo, Wann laufen oben am Schild entlang neben dem Logo wie die Zeile auf einem Ladenschild; unten steht nur noch der Satz.',
     lambda: S),
    ('Mit Zeichen', 'Vor jeder Angabe ein feines Zeichen in Gold (Person, Ort, Uhr), drei Spalten unter dem Satz.',
     lambda: S + spalten('f07', lambda x, y: '<i>%s</i><span class="etikett">%s</span><p>%s</p>' % (ZEICHEN[x], E(x), y))),
    ('Eine ruhige Fusszeile', 'Alle drei Angaben in einer ruhigen Zeile in Versalien am Fuss des Schilds, getrennt von kleinen Goldrauten.',
     lambda: S + '<p class="ef f08 sw" style="--i:4">%s</p>' % '<i>◆</i>'.join('<span>%s</span>' % y.replace('<br>', ', ') for _, y in F)),
    ('Cremefarbene Kärtchen', 'Wer, Wo, Wann auf drei kleinen Kärtchen in der Farbe des alten Plakats, im dunklen Schild nebeneinander.',
     lambda: S + spalten('f09')),
    ('Die Zeiten gross', 'Die Öffnungszeiten stehen gross in der Titelschrift, Wer und Wo kleiner daneben.',
     lambda: S + '<div class="ef f10 sw" style="--i:4"><div class="f10-zeit"><span class="etikett">Wann</span><p>%s</p></div><div class="f10-rest">%s</div></div>' % (
         F[2][1], ''.join('<div><span class="etikett">%s</span><p>%s</p></div>' % (E(x), y) for x, y in F[:2]))),
]
LISTE = [[0, 'Heute']] + [[j + 1, n] for j, (n, _, _) in enumerate(V)]
KOPF = '<link rel="stylesheet" href="%s/fakten.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, unten, name):
    h = basis[:a] + '<div class="es-unten eu-%02d">%s</div>' % (nr, unten) + basis[b:] if nr else basis
    if nr == 6:   # die Zeile oben am Schild, neben dem Logo
        kopf = '<div class="ef f06">%s</div>' % ''.join('<div><span class="etikett">%s</span><p>%s</p></div>' % (E(x), y) for x, y in F)
        h = h.replace('<span class="logo">', '<div class="f06-kopf"><span class="logo">', 1)
        i = h.index('<div class="f06-kopf">'); j = h.index('</span>', h.index('</svg>', i)) + len('</span>')
        h = h[:j] + kopf + '</div>' + h[j:]
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / %02d</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>') % (nr, len(V), E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, '', 'Heute'))
    for j, (name, _, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(), name))
    print('00.html … %02d.html in %s' % (len(V), ORD))
