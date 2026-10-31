# Walk on the Wild Side · Feiern, neues Fenster zwischen «Grösser als die Bar» und «So geht es» (30.10.2026): Bild zur Wahl.
# Robert: «Baue da ein Fenster ein zwischen den Abschnitten». 01 = eingebaut, 02–04 = andere Querbilder. Wechsel mit ← →.
# Aufruf: python3 _varianten/feiern-fenster/bau.py
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter

E = html.escape
ORD = '_varianten/feiern-fenster'
VER = str(int(os.path.getmtime(os.path.join(ORD, 'nav.js'))))
SATZ = ['Gute Drinks,', 'gute Energie.']
HEUTE = B.fenster_fest('ft-raum-abend', SATZ, '50% 50%')
V = [(1, 'Der Raum am Abend (eingebaut)', None),
     (2, 'Gäste an der Theke', 'ft-theke-gaeste'),
     (3, 'Eine Runde stösst an', 'ft-runde-stoesst-an'),
     (4, 'Momo mixt, ein Gast schaut zu', 'ft-momo-mixt-gast')]

def seite(n, k):
    h = unter.tafel()
    assert h.count(HEUTE) == 1
    if k:
        h = h.replace(HEUTE, B.fenster_fest(k, SATZ, '50% 50%'))
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<style>.vschild{position:fixed;z-index:200;left:16px;bottom:16px;max-width:calc(100vw - 32px);margin:0;display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:12px;padding:11px 16px;border-radius:12px;background:var(--nacht);color:var(--creme);font:500 10.5px/1.2 var(--lauf);letter-spacing:.12em;text-transform:uppercase;box-shadow:0 18px 40px -16px rgba(0,0,0,.7),inset 0 0 0 1px rgba(216,178,100,.42);pointer-events:none}.vschild b{font-weight:500;color:var(--gold)}.vschild i{font-style:normal;opacity:.6}</style></head>', 1)
    liste = [[nr, nm] for nr, nm, _ in V]
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, V[-1][0], E(dict((a, b) for a, b, _ in V)[n]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script>' % (json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)

if __name__ == '__main__':
    for n, _, k in V:
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n, k))
    print('01 …', V[-1][0])
