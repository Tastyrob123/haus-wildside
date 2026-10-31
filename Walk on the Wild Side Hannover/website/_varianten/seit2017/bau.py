#!/usr/bin/env python3
"""Walk on the Wild Side · Startseite, Kapitel «Seit 2017 in Linden»: 15 Bilder statt des Eröffnungsbilds (29.10.2026).
Jede Fassung = die echte index.html, nur das Bild in der Kachel neben den Jahren getauscht. 00 = heute. Wechsel mit ← →."""
import os, sys, json, html
HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HIER, '..', '..'))
sys.path.insert(0, WEB)
import bau
ORD = '_varianten/seit2017'
V = '29103'
E = html.escape

KANDIDATEN = [
    ('decke-2017', 'Heute: das Bild zur Eröffnung', '50% 50%'),
    ('alt-theke', 'Die Theke, erste Website', '50% 50%'),
    ('alt-raum', 'Der Raum, erste Website', '50% 50%'),
    ('alt-rueckbar', 'Die Rückbar, erste Website', '50% 50%'),
    ('alt-decke', 'Decke und Wandlampen, erste Website', '50% 50%'),
    ('fb-2020-bar', 'Zwei Gäste an der Bar, 2020', '50% 50%'),
    ('fb-2023-negroni', 'NEGRONI, November 2023', '50% 40%'),
    ('derya', 'Derya an der Bar', '62% 50%'),
    ('momo-flaschen', 'Momo hinter den Flaschen', '50% 50%'),
    ('decke-raum', 'Der Raum unter der Decke', '50% 30%'),
    ('decke-hoch', 'Decke über der Theke', '50% 45%'),
    ('decke-bar', 'Decke über der Rückbar', '50% 40%'),
    ('rueckbar-breit', 'Rückbar mit Vitrine', '50% 50%'),
    ('tuer-rot', 'Durch die Tür, roter Boden', '50% 50%'),
    ('konzert', 'Konzert unter der Decke', '50% 50%'),
    ('momo-lacht', 'Momo unter dem NEGRONI', '50% 40%'),
]
NAMEN = json.dumps([[n, k[1]] for n, k in enumerate(KANDIDATEN)], ensure_ascii=False)


def kachel(k, pos):
    return '<div class="kachel leise sw" style="--i:2;--lq:url(%s)">%s</div>' % (
        bau.mache(k)['lq'], bau.img_tag(k, '40vw', extra=' style="object-position:%s"' % pos))


def main():
    quelle = open(os.path.join(WEB, 'index.html')).read()
    alt = '<div class="kachel leise sw" style="--i:2;--lq:url(%s)">%s</div>' % (bau.mache('decke-2017')['lq'], bau.img_tag('decke-2017', '40vw'))
    assert quelle.count(alt) == 1, 'Kachel im Kapitel Seit 2017 nicht eindeutig gefunden'
    for n, (k, name, pos) in enumerate(KANDIDATEN):
        s = quelle if n == 0 else quelle.replace(alt, kachel(k, pos))
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
        s = s.replace('</head>', '<link rel="stylesheet" href="%s/varianten-nav.css?v=%s"></head>' % (ORD, V), 1)
        schild = '<p class="vschild" aria-hidden="true"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(KANDIDATEN) - 1, E(name))
        s = s.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD="%s"</script><script src="%s/varianten-nav.js?v=%s"></script></body>' % (NAMEN, n, ORD, ORD, V), 1)
        open(os.path.join(HIER, '%02d.html' % n), 'w').write(s)
    print('%d Fassungen' % len(KANDIDATEN))


if __name__ == '__main__':
    main()
