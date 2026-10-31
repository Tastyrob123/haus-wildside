# Walk on the Wild Side · Startseite, Fenster «Ein Abend, der nur euch gehört.» (vor der langen Tafel): 15 Bilder zur Wahl (29.10.2026).
# Robert: «15 verschiedene Möglichkeiten an Bildern … in dieses Fenster … scharf, was passt, nicht hochkant». 00 = heutiger Stand (altes Fenster).
# Jede Fassung ist die echte Startseite mit dem Fenster im festen Mass (fenster_fest, min(67vh,624px), Handy 58svh).
# Bilder: 16:10-Ausschnitte aus echten Querformaten oder hoch aufgelösten Originalen (quelle/, Herkunft in quelle/herkunft.json).
# Wechsel mit ← →. Aufruf: python3 _varianten/fenster-tafel-15/bau.py → 00.html … 15.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder

E = html.escape
ORD = '_varianten/fenster-tafel-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'nav.js'))))
Q = '../website/' + ORD + '/quelle/'

# (Datei, Name auf dem Schild, Alt-Text, Bildmitte, auch bei Culinarium verwendet)
BILDER = [
    ('anstossen-kerzen', 'Anstossen bei Kerzenlicht', 'Gäste stossen an der Tafel an, davor Kerzen', '50% 50%', True),
    ('drink-kraeuter', 'Ein Drink mit grüner Garnitur', 'Ein Drink mit grüner Garnitur auf dem dunklen Tisch', '50% 50%', True),
    ('koch-kerzen', 'Der Koch am Tisch, Kerzen', 'Der Koch an der Tafel im Kerzenlicht', '50% 50%', False),
    ('koch-am-tisch', 'Der Koch erzählt am Tisch', 'Der Koch erzählt den Gästen am Tisch', '50% 50%', False),
    ('runde-stoesst-an', 'Eine Runde stösst an', 'Eine Runde stösst mit kleinen Gläsern an', '50% 50%', True),
    ('gast-am-teller', 'Ein Gast am Teller', 'Ein Gast am Teller an der langen Tafel', '50% 50%', False),
    ('dessert-tafel', 'Dessert auf der Tafel', 'Dessert auf der gedeckten Tafel', '50% 50%', False),
    ('glaeser-tafel', 'Gläser auf dem Holztisch', 'Gläser auf dem Holztisch', '50% 50%', False),
    ('raum-abend', 'Der Raum am Abend', 'Der Raum am Abend, Gäste an der Theke und hinten an den Tischen', '50% 50%', False),
    ('momo-mixt-gast', 'Momo mixt, ein Gast schaut zu', 'Momo schüttelt einen Drink, daneben ein Gast', '50% 50%', True),
    ('theke-gaeste', 'Gäste an der Theke', 'Gäste an der Theke, hinten wird gemixt', '50% 50%', False),
    ('drinks-tisch', 'Ein Longdrink auf dem Tisch', 'Ein roter Longdrink auf dem Tisch', '50% 50%', False),
    ('drink-nische', 'Ein Drink in der Nische', 'Ein Drink im Stielglas auf dem Tisch in der Nische', '50% 50%', True),
    ('cocktail-flasche', 'Cocktail mit Schaum', 'Ein Cocktail mit Schaum, daneben eine Flasche', '50% 50%', True),
    ('rose-glas', 'Ein Glas vor dunklem Grund', 'Ein Drink im Stielglas vor dunklem Grund', '50% 50%', False),
]
for k, _, alt, _, _ in BILDER:
    bilder.BILDER['ft-' + k] = (Q + k + '.jpg', alt)


def seite(n):
    alt = B.fenster
    if n:
        k, _, _, pos, _ = BILDER[n - 1]
        B.fenster = lambda bild, satz, p='50% 50%': B.fenster_fest('ft-' + k, satz, pos) if bild == 'tafel-glaeser' else alt(bild, satz, p)
    h = B.seite()
    B.fenster = alt
    # Ein fester Anker am Fenster, damit ← → genau dort bleibt
    h = h.replace('<section class="fk" aria-label="Ein Abend, der nur euch gehört."', '<section id="tafel-fenster" class="fk" aria-label="Ein Abend, der nur euch gehört."', 1)
    h = h.replace('<section class="fenster">', '<section id="tafel-fenster" class="fenster">', 1)
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name + (' · auch bei Culinarium' if cul else '')] for j, (_, name, _, _, cul) in enumerate(BILDER)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>' % (n, E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(16):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 … 15')
