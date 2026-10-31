# Walk on the Wild Side · Besuch-Kopf «Das Licht geht an»: Ersatz für zwei Bilder (31.10.2026).
# Robert: «5 aber die beiden bilder siehe screenshot tauschen» (Momo vor der NEGRONI-Schrift oben Mitte, Sängerin hinter Blumen unten Mitte).
# Jede Fassung ist die echte Besuch-Seite, nur diese zwei Plätze tragen ein anderes Paar. 00 = heute. Wechsel mit ← →.
# Aufruf: python3 _varianten/besuch-bildtausch/bau.py
import os, sys, re, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER); sys.path.insert(0, HIER)
from bau import E, mache, img_tag

ORD = '_varianten/besuch-bildtausch'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('varianten-nav.js', 'varianten-nav.css', 'bau.py'))))
basis = open('besuch.html').read()
POS = {'voll': '50% 50%', 'fe-theke': '50% 50%', 'decke-hoch': '50% 40%', 'fw-h18': '50% 40%', 'tuer-rot': '50% 55%', 'dg-coupes': '50% 50%',
       'fw-a31': '50% 50%', 'freundinnen': '50% 40%', 'fw-h7': '50% 35%', 'decke-raum': '50% 45%', 'dg-abseihen': '50% 40%', 'fw-highballs': '50% 50%',
       'feste-anstossen': '50% 45%', 'fw-h19': '50% 50%', 'fw-h31': '50% 30%', 'dg-flaschen': '50% 50%', 'fe-highball': '50% 50%'}
PAARE = [('voll', 'fe-theke'), ('decke-hoch', 'fw-h18'), ('tuer-rot', 'dg-coupes'), ('fw-a31', 'freundinnen'), ('fe-highball', 'fw-h7'), ('decke-raum', 'dg-abseihen'),
         ('fw-highballs', 'feste-anstossen'), ('fw-h19', 'fw-h31'), ('voll', 'dg-flaschen'), ('decke-hoch', 'tuer-rot'), ('fe-theke', 'fw-a31'), ('dg-coupes', 'fw-h18')]


def platz(html, alt_key, neu_key):
    m = re.search(r'<figure class="lw-f" style="--lq:url\([^)]*\);--d:([\d.]+)s"><img[^>]*assets/bild/%s-\d+\.webp[^>]*></figure>' % re.escape(alt_key), html)
    assert m, alt_key
    neu = '<figure class="lw-f" style="--lq:url(%s);--d:%ss">%s</figure>' % (mache(neu_key)['lq'], m.group(1), img_tag(neu_key, '(max-width:860px) 50vw, 34vw', True, ' style="object-position:%s"' % POS[neu_key]))
    return html[:m.start()] + neu + html[m.end():]


NAME = {'voll': 'Voller Raum', 'fe-theke': 'Theke', 'decke-hoch': 'Decke', 'fw-h18': 'Gast am Tisch', 'tuer-rot': 'Tür', 'dg-coupes': 'Coupes',
        'fw-a31': 'Rückbar', 'freundinnen': 'Freundinnen', 'fe-highball': 'Highball', 'fw-h7': 'Gast', 'decke-raum': 'Gewölbe', 'dg-abseihen': 'Abseihen',
        'fw-highballs': 'Drinks unter der Decke', 'feste-anstossen': 'Anstossen', 'fw-h19': 'Drinks', 'fw-h31': 'Gast mit Glas', 'dg-flaschen': 'Flaschen'}
LISTE = [[0, 'Heute']] + [[j + 1, '%s + %s' % (NAME[a], NAME[b])] for j, (a, b) in enumerate(PAARE)]


def seite(nr, html, name):
    h = html.replace('<head>', '<head><base href="../../">', 1).replace('</head>', '<link rel="stylesheet" href="%s/varianten-nav.css?v=%s">\n</head>' % (ORD, VER), 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>') % (nr, len(PAARE), E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', fuss, 1)


open(os.path.join(ORD, '00.html'), 'w').write(seite(0, basis, 'Heute'))
for j, (a, b) in enumerate(PAARE):
    h = platz(platz(basis, 'wf-raum', a), 'saengerin', b)
    open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, h, LISTE[j + 1][1]))
print('00 …', len(PAARE), 'in', ORD)
