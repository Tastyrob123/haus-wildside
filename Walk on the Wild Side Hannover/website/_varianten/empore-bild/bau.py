# Walk on the Wild Side · Feiern, «Die Empore gehört euch.» (Platte, Fassung 14): welches Bild zeigt die Empore wirklich (30.10.2026).
# Robert: «aber die empore ist glaube ich andere bild oder ?». Das heutige Bild (Angebots-PDF img-039) zeigt die Fensterbank vorn am Eingang, nicht die Empore.
# 00 = heute, 01–03 = Bilder, auf denen die Empore zu sehen ist. Eingesetzt wird erst Roberts Nummer. Wechsel mit ← →.
# Aufruf: python3 _varianten/empore-bild/bau.py
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter

E = html.escape
ORD = '_varianten/empore-bild'
VER = str(int(os.path.getmtime(os.path.join(ORD, 'nav.js'))))
SIZES = '(max-width:900px) 92vw, 42vw'
HEUTE = B.bild('an-empore', 'fr-plbild', SIZES, extra=' style="object-position:50% 50%"')
V = [(0, 'Heute: die Fensterbank vorn', None),
     (1, 'Die lange Tafel mit Gästen, oben auf der Empore', ('culinarium-tafel', '50% 62%')),
     (2, 'Die Stufen hinauf zur Empore', ('decke-raum', '50% 78%')),
     (3, 'Die gedeckte lange Tafel', ('fw-tafel', '38% 50%'))]

def seite(n, wahl):
    h = unter.tafel()
    assert h.count(HEUTE) == 1
    if wahl:
        h = h.replace(HEUTE, B.bild(wahl[0], 'fr-plbild', SIZES, extra=' style="object-position:%s"' % wahl[1]))
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<style>.vschild{position:fixed;z-index:200;left:16px;bottom:16px;max-width:calc(100vw - 32px);margin:0;display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:12px;padding:11px 16px;border-radius:12px;background:var(--nacht);color:var(--creme);font:500 10.5px/1.2 var(--lauf);letter-spacing:.12em;text-transform:uppercase;box-shadow:0 18px 40px -16px rgba(0,0,0,.7),inset 0 0 0 1px rgba(216,178,100,.42);pointer-events:none}.vschild b{font-weight:500;color:var(--gold)}.vschild i{font-style:normal;opacity:.6}</style></head>', 1)
    liste = [[nr, nm] for nr, nm, _ in V]
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, V[-1][0], E(dict((a, b) for a, b, _ in V)[n]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script>' % (json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)

if __name__ == '__main__':
    for n, _, wahl in V:
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n, wahl))
    print('00 …', V[-1][0])
