# Walk on the Wild Side · Programm, «Die Woche»: was links und rechts vom Kinoschild steht (30.10.2026).
# Robert: «kann man da links und rechts noch irgendwas machen, damit das nicht so leer aussieht … Sticker … oder generell mit so einer Tapete».
# Sticker sind laut CHARAKTER.md dem Culinarium vorbehalten; Tapete und Wand kommen aus dem echten Raum: Deckendruck des Kirchengewölbes,
# Messing-Wandleuchten, Rückbar. 00 = heutiger Stand. Aufruf: python3 _varianten/woche-wand/bau.py
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER); sys.path.insert(0, HIER)
import bau as B
import unter
E = html.escape
ORD = '_varianten/woche-wand'
VER = str(int(os.path.getmtime(os.path.join(ORD, 'w.css'))))
TAPETE = 'assets/bild/decke-2017-1600.webp?v=%s' % B.V


def mini(zeilen):
    z = ''.join('<p class="%s">%s</p>' % (k, ''.join('<span style="--b:%d">%s</span>' % (i + 20, '&nbsp;' if c == ' ' else E(c)) for i, c in enumerate(t))) for t, k in zeilen)
    return '<div class="ww-mini" aria-hidden="true"><div class="wo-rillen">%s</div></div>' % z


def leuchte():
    # Zwei Arme mit Kerzen an einer Wandplatte, wie die Leuchten an der Betonwand
    return '''<div class="ww-leuchte" aria-hidden="true"><svg viewBox="0 0 120 200"><rect class="stab" x="54" y="70" width="12" height="40" rx="2"/>
<path class="stab" d="M60 110 V150 M60 128 C40 128 26 120 26 98 M60 128 C80 128 94 120 94 98"/><circle class="stab" cx="60" cy="152" r="4"/>
<path class="stab" d="M18 98 H34 M86 98 H102"/><rect class="kerze" x="23" y="80" width="6" height="18" rx="1"/><rect class="kerze" x="91" y="80" width="6" height="18" rx="1"/>
<path class="flamme" d="M26 70 C23 75 23 78 26 80 C29 78 29 75 26 70Z"/><path class="flamme" d="M94 70 C91 75 91 78 94 80 C97 78 97 75 94 70Z"/></svg></div>'''


def foto(k, pos):
    d = B.mache(k)
    return '<figure class="ww-foto" style="--lq:url(%s)">%s</figure>' % (d['lq'], B.img_tag(k, '(max-width:760px) 0px, 24vw', extra=' style="object-position:%s"' % pos))


V = [('Das Gewölbe als Tapete', 1, '', ''),
     ('Das Gewölbe als Band', 2, '<div class="ww-band"></div>', ''),
     ('Zwei Wandleuchten', 3, leuchte(), leuchte()),
     ('Kleine Tafeln daneben', 4, mini([('DO BIS SA', 'rot'), ('AB 19 UHR', '')]), mini([('HAASEMANN-', ''), ('STRASSE 13', '')])),
     ('Rückbar links und rechts', 5, foto('rueckbar-breit', '30% 50%'), foto('decke-bar', '60% 60%')),
     ('Das Gewölbe im Licht der Bar', 6, '', '')]


def seite(n):
    h = unter.programm()
    if n:
        name, nr, l, r = V[n - 1]
        a = h.find('<div class="wo-tafel"'); b = h.find('<div class="wo-reihe">', a)
        tafel = h[a:b]
        if nr == 2:
            zeile = '<div class="ww-zeile">%s%s</div>' % (l, tafel)
        else:
            zeile = '<div class="ww-zeile"><div class="ww-l">%s</div>%s<div class="ww-r">%s</div></div>' % (l, tafel, r)
        h = h[:a] + zeile + h[b:]
        h = h.replace('<section class="kap auf wo" id="woche">', '<section class="kap auf wo ww%d" id="woche" style="--tapete:url(%s)">' % (nr, TAPETE), 1)
    liste = [[0, 'Heutiger Stand']] + [[j + 1, v[0]] for j, v in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/w.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    sk = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script>' % (json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', schild + sk + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
