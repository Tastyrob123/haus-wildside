# Walk on the Wild Side · Drinks-Seite, Fenster «Jeder Drink ein Unikat.» mit 12 Bildern zur Wahl (30.10.2026).
# Robert: «Das ist eigentlich ein Fenster … gib mir bitte 12 Bilder, die man da reinpacken kann ins Fenster. Die richtig geil passen.»
# Nur echte Querformate (Fenster-Regel 29.10.2026). 00 = heutiger Stand. Wechsel mit ← →. Aufruf: python3 _varianten/drinks-fenster-12/bau.py
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder
import unter

E = html.escape
ORD = '_varianten/drinks-fenster-12'
VER = str(int(os.path.getmtime(os.path.join(ORD, 'nav.js'))))
K = '../../Culinarium Hannover/_quelle/vom-kunden/'
BILDER = [
    ('wf-fe-rose-1', K + 'drive-arw-vorschau/5406.jpg', 'Ein rosé Drink im Stielglas auf dunklem Grund', '50% 50%', 'Das Glas im Dunkeln'),
    ('wf-fe-rose-2', K + 'drive-arw-vorschau/5408.jpg', 'Ein rosé Drink im geneigten Stielglas', '50% 50%', 'Das geneigte Glas'),
    ('wf-fe-rose-3', K + 'drive-arw-vorschau/5409.jpg', 'Ein rosé Drink im Stielglas von der Seite', '50% 50%', 'Das Glas von der Seite'),
    ('wf-fe-shots', 'google-maps/google-17.jpg', 'Gläser auf dem Holztisch im warmen Licht', '50% 50%', 'Gläser auf dem Tisch'),
    ('wf-fe-rueckbar', 'web-archiv/bilder/103_506957807_backbar-regale_1200x900.jpg', 'Die Rückbar mit Flaschen bis unter die Decke', '50% 50%', 'Die Rückbar'),
    ('wf-fe-regal', 'google-maps/google-40.jpg', 'Flaschenregal und Vitrine hinter der Theke', '50% 50%', 'Regal und Vitrine'),
    ('wf-fe-raum', 'portale/stadtwohnungenlinden_wild.jpeg', 'Die Bar am Abend, Theke und Tische im Kerzenlicht', '50% 50%', 'Die Bar am Abend'),
    ('wf-fe-decke', 'web-archiv/bilder/103_506957809_raum-decke-lampen_1200x900.jpg', 'Der Raum unter dem Gewölbe, darunter die Rückbar', '50% 60%', 'Unter dem Gewölbe'),
    ('wf-fe-decke-2', 'google-maps/google-54.jpg', 'Das bemalte Gewölbe über der Bar', '50% 55%', 'Das Gewölbe'),
    ('wf-fe-tresen', 'facebook/2020-06-17_fb_2743375292557948.jpg', 'Zwei Gäste am Tresen im roten Licht', '50% 50%', 'Am Tresen'),
    ('wf-fe-violett', 'portale/bilder/enprimeur_10141f70_hero2.jpg', 'Ein violetter Drink vor der Rückbar', '50% 40%', 'Der violette Drink'),
    ('wf-fe-tequila', 'ig/2025-06-16_walkonthewildside_hannover_DK-GT7TITWD-1.jpg', 'Tequila und Grapefruit-Limonade auf der Theke', '50% 50%', 'Tequila und Paloma'),
]
bilder.BILDER.update({k: (p, a) for k, p, a, _, _ in BILDER})
SATZ = ['Jeder Drink', 'ein Unikat.']


def seite(n):
    h = unter.drinks()
    if n:
        a = h.find('<section class="fk" aria-label="Jeder Drink ein Unikat.">')
        b = h.find('</section>', a) + len('</section>')
        k, _, _, pos, _ = BILDER[n - 1]
        h = h[:a] + B.fenster_fest(k, SATZ, pos) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, x[4]] for j, x in enumerate(BILDER)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    schild = ('<p class="vschild" style="position:fixed;z-index:200;left:16px;bottom:16px;margin:0;display:flex;gap:12px;padding:11px 16px;border-radius:12px;background:var(--nacht);color:var(--creme);'
              'font:500 10.5px/1.2 var(--lauf);letter-spacing:.12em;text-transform:uppercase;box-shadow:inset 0 0 0 1px var(--gold-l);pointer-events:none"><b style="font-weight:500;color:var(--gold)">%02d / %02d</b><span>%s</span><i style="font-style:normal;opacity:.6">← →</i></p>') % (n, len(BILDER), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(BILDER) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(BILDER))
