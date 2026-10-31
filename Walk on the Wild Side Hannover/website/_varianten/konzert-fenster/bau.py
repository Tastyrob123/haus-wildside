# Walk on the Wild Side · Programm: Bild für das Fenster «Gute Drinks, gute Musik.» (30.10.2026). Robert: Motiv cool, aber unscharf, Alternativen zeigen.
# 00 = heute (Konzert). Nur echte Querformate der Bar, Satz bleibt. Wechsel mit ← →, man bleibt beim Fenster.
# Aufruf: python3 _varianten/konzert-fenster/bau.py
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, fenster_fest

ORD = '_varianten/konzert-fenster'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('varianten-nav.js', 'varianten-nav.css'))))
SATZ = ['Gute Drinks,', 'gute Musik.']
basis = open('programm.html').read()
a = basis.index('<section class="fk" aria-label="Gute Drinks')
b = basis.index('</section>', a) + len('</section>')

V = [('Derya an der Bar', 'derya', '50% 40%'),
     ('Das Gewölbe von 2017', 'decke-2017', '50% 50%'),
     ('Zwei Gäste stossen an', 'fb-2020-bar', '50% 45%'),
     ('Momo und Rudi am Valentinsabend', 'pf-momo-rudi', '50% 40%'),
     ('Der leere Raum am Abend', 'pf-raum', '50% 55%'),
     ('Das Team vor der Rückbar', 'an-team', '50% 45%'),
     ('Die Decke über der Bar', 'decke-flach', '50% 60%'),
     ('Die Rückbar mit Vitrine', 'rueckbar-breit', '50% 50%')]
LISTE = [[0, 'Heute · Konzert']] + [[j + 1, nm] for j, (nm, _, _) in enumerate(V)]
KOPF = '<link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER)


def seite(nr, html, name):
    h = basis[:a] + html + basis[b:] if nr else basis
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / %02d</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>') % (
        nr, len(V), E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, '', LISTE[0][1]))
    for j, (name, k, pos) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, fenster_fest(k, SATZ, pos), name))
    print('00.html … %02d.html in' % len(V), ORD)
