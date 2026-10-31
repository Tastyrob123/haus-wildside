# Walk on the Wild Side · Seite «Das Haus», Fenster direkt unter dem Kopf: 15 Bilder zur Wahl (31.10.2026, Robert: «15 Bilder, die ich da einfügen kann»).
# Aus dem Fundus (Bilder, die auf keiner Seite stehen), ohne Menschen, als Querband geschnitten und per KI auf 4K nachgeschärft (Higgsfield, 2 Credits je Bild).
# 00 = heute (Kerzen). Satz bleibt. Wechsel mit ← →. Aufruf: python3 _varianten/haus-fenster-15/bau.py
import os, re, json, glob
from PIL import Image
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); os.chdir(HIER)
ORD = '_varianten/haus-fenster-15'
basis = open('haus.html').read()
m = re.search(r'<section class="fk" aria-label="Kerzenlicht unter dem Gewölbe\.?">.*?</section>', basis, re.S)
FENSTER = m.group(0)
img_alt = re.search(r'<img [^>]*>', FENSTER).group(0)
NAMEN = {'01': 'Rückbar mit NEGRONI', '02': 'Raum mit Kerze', '03': 'Die Vitrine', '04': 'Crème brûlée', '05': 'Glasbehälter mit Zapfhähnen',
         '06': 'Karte und Kerzenglas', '07': 'Der Sour', '08': 'Zitronen und Blüten', '09': 'Verstärker am Fenster', '10': 'Tresen mit Gläsern',
         '11': 'Die Hausecke', '12': 'Negroni im Glas', '13': 'Der leere Raum', '14': 'Drei Probiergläser', '15': 'Die gedeckte Wand'}
liste = [[0, 'Heute: Kerzen']]
seiten = {0: basis}
for nr in sorted(NAMEN):
    gross = glob.glob(os.path.join(ORD, 'bild', nr + '-*-gross.webp'))
    if not gross: continue
    g = gross[0]; k = g.replace('-gross.webp', '-halb.webp')
    w, h = Image.open(g).size; wk = Image.open(k).size[0]
    neu = '<img src="%s" srcset="%s %dw, %s %dw" sizes="100vw" alt="%s" width="%d" height="%d" decoding="async" style="object-position:50%% 50%%">' % (
        g, k, wk, g, w, NAMEN[nr], w, h)
    seiten[int(nr)] = basis.replace(FENSTER, FENSTER.replace(img_alt, neu).replace('--lq:url(', '--lq-alt:url('))
    liste.append([int(nr), NAMEN[nr]])
VER = str(int(os.path.getmtime(os.path.join(ORD, 'varianten-nav.js'))))
for nr, h in seiten.items():
    name = dict(liste)[nr]
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', '<link rel="stylesheet" href="%s/varianten-nav.css?v=%s">\n</head>' % (ORD, VER), 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, name), 1)
    h = h.replace('</body>', '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
                  '<script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>' % (nr, len(liste) - 1, name, json.dumps(liste, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER), 1)
    open(os.path.join(ORD, '%02d.html' % nr), 'w').write(h)
print(len(seiten) - 1, 'Bilder')
