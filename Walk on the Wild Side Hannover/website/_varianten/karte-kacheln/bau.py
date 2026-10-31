# Walk on the Wild Side · Drinks, «Die einzige Karte»: Fassungen für die Drink-Kacheln im Schachbrett (30.10.2026).
# Robert: «können wir statt den weißen Schachbrett kacheln … was anderes besser zum konzept des ladens passenderes nehmen?»
# Nur die Kacheln ändern sich, Anordnung und Bewegung bleiben. Farben aus der echten Karte «Drunk in Love» (Rosa #FEE1E6, Rot #D30625 gemessen),
# vom Eckschild (Nacht, Goldrahmen) und von den Plakaten (Ultramarin, Plakatrot, Creme). 00 = heutiger Stand. Wechsel mit ← →.
import os, json, html, time
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ORD = '_varianten/karte-kacheln'
VER = str(int(time.time()))
V = ['Heutiger Stand', 'Die Valentinskarte', 'Rosa und Rot im Wechsel', 'Das Eckschild', 'Der Goldrahmen', 'Die Karte bei Nacht',
     'Das Rot der Wortmarke', 'Die Decke', 'Das Plakat', 'Gold', 'Valentin im Dunkeln']
h0 = open(os.path.join(HIER, 'drinks.html')).read()
for n, name in enumerate(V):
    h = h0.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    h = h.replace('<section class="kap auf" id="karte">', '<section class="kap auf kk%02d" id="karte">' % n, 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V) - 1, html.escape(name))
    liste = [[j, x] for j, x in enumerate(V)]
    h = h.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script></body>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER), 1)
    open(os.path.join(HIER, ORD, '%02d.html' % n), 'w').write(h)
print(len(V))
