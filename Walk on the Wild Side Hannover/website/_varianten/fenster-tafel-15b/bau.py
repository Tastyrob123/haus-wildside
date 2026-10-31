# Walk on the Wild Side · Startseite, Fenster «Ein Abend, der nur euch gehört.»: zweite Runde, 15 Bilder (29.10.2026).
# Erste Runde abgelehnt («alle richtig schlecht … unscharf … abgeschnitten»). Jetzt: Abende an der langen Tafel aus den Kundenfotos (Culinarium, im Wild Side aufgenommen),
# durchgehend scharf, jeder Ausschnitt vorher im Fensterband bei 1000 × 650 angesehen.
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
ORD = '_varianten/fenster-tafel-15b'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'nav.js'))))
Q = '../website/' + ORD + '/quelle/'

# (Datei, Name auf dem Schild, Alt-Text, Bildmitte, auch bei Culinarium verwendet)
BILDER = [
    ('tafel-gedeckt', 'Die lange Tafel, gedeckt', 'Die lange Tafel am Fenster, gedeckt mit Brot, Gläsern und Menükarten', '50% 50%', False),
    ('runde-von-oben', 'Eine Runde an der Tafel', 'Eine Runde an der langen Tafel, Kerzen, hinten die Rückbar', '50% 50%', False),
    ('tafel-im-raum', 'Der Koch an der Tafel', 'Der Koch bringt den nächsten Gang an die Tafel, Kerzen auf dem Tisch', '50% 50%', False),
    ('blick-durch-die-tuer', 'Blick durch die Tür auf die Tafel', 'Blick durch die Tür auf die Tafel, der Koch serviert, Kerzen', '50% 50%', False),
    ('koch-kerzentisch', 'Der Koch serviert, Kerzenlicht', 'Der Koch serviert lachend an der Tafel', '50% 50%', False),
    ('applaus-kerzen', 'Applaus an der Tafel', 'Gäste klatschen an der Tafel bei Kerzenlicht', '50% 50%', False),
    ('rote-drinks', 'Anstossen mit roten Drinks', 'Zwei Gäste stossen mit roten Drinks an', '50% 50%', False),
    ('momo-am-tisch', 'Momo erzählt am Tisch', 'Momo erzählt am Tisch, hinten der NEGRONI-Schriftzug', '50% 50%', False),
    ('koch-erzaehlt-hell', 'Der Koch erzählt, die Runde hört zu', 'Der Koch erzählt, die Gäste an der Tafel hören zu', '50% 50%', False),
    ('gaeste-am-fenster', 'Gäste am Fenster', 'Gäste am Fenster mit Gläsern, eine Frau lacht in die Kamera', '50% 50%', False),
    ('kerzen-koch', 'Der Koch hinter den Kerzen', 'Der Koch steht am Raum, vorn eine Kerze', '50% 50%', False),
    ('platz-gedeckt', 'Ein gedeckter Platz', 'Ein gedeckter Platz mit Menükarte und Besteck', '50% 50%', False),
    ('durch-die-wand', 'Kerzen hinter der Wandöffnung', 'Durch die Wandöffnung: Kerzen, Blumen und eine Apothekerflasche', '50% 50%', False),
    ('fenster-nacht', 'Von draussen ins Fenster', 'Von draussen durchs Fenster: die Decke und die Rückbar am Abend', '50% 50%', False),
    ('fenster-aussen', 'Die Fenster am Abend', 'Die Fenster der Bar am Abend, drinnen Licht und die Decke', '50% 50%', False),
]
for k, _, alt, _, _ in BILDER:
    bilder.BILDER['fb-' + k] = (Q + k + '.jpg', alt)


def seite(n):
    alt = B.fenster
    if n:
        k, _, _, pos, _ = BILDER[n - 1]
        B.fenster = lambda bild, satz, p='50% 50%': B.fenster_fest('fb-' + k, satz, pos) if bild == 'tafel-glaeser' else alt(bild, satz, p)
    h = B.seite()
    B.fenster = alt
    # Ein fester Anker am Fenster, damit ← → genau dort bleibt
    h = h.replace('<section class="fk" aria-label="Ein Abend, der nur euch gehört."', '<section id="tafel-fenster" class="fk" aria-label="Ein Abend, der nur euch gehört."', 1)
    h = h.replace('<section class="fenster">', '<section id="tafel-fenster" class="fenster">', 1)
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name] for j, (_, name, _, _, cul) in enumerate(BILDER)]
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
