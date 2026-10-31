#!/usr/bin/env python3
"""Walk on the Wild Side · Fenster über «Seit 2017», zweite Runde mit 20 Motiven (29.10.2026).
Nur Fotos, die im Fenster scharf bleiben: breite Einzelbilder ab 1800 px Breite, sonst drei Hochformate ganz nebeneinander.
Jede Fassung = die echte index.html, nur das Fenster getauscht; Grösse und Satz bleiben. 00 = heute. Wechsel mit ← →."""
import os, sys, json, html
HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HIER, '..', '..'))
sys.path.insert(0, WEB)
import bau
ORD = '_varianten/fenster2017b'
V = '29108'
E = html.escape
SATZ = ['Zwei Eröffnungen,', 'eine Decke.']
MOTIVE = [
    ('Heute: die Decke über der Theke', ['decke-hoch'], '50% 55%'),
    ('Derya an der Bar', ['fw-derya'], '60% 45%'),
    ('Zwei Highballs im Raum', ['fw-highballs'], '50% 62%'),
    ('Zu zweit am Abend', ['fw-h46', 'fw-a28', 'fw-h21']),
    ('Am Tresen', ['fw-a57', 'fw-a45', 'fw-h19']),
    ('Kerzenlicht', ['fw-h33', 'fw-h30', 'fw-a55']),
    ('Gläser auf der Theke', ['fw-h11', 'fw-h41', 'fw-h1']),
    ('Die Rückbar', ['fw-a31', 'fw-h16', 'fw-h37']),
    ('Gäste am Tisch', ['fw-h18', 'fw-a14', 'fw-h42']),
    ('Der Raum am Abend', ['fw-a12', 'fw-h7', 'fw-a9']),
    ('Zu zweit', ['fw-a4', 'fw-h46', 'fw-a3']),
    ('Gin', ['fw-a47', 'fw-h21', 'fw-a36']),
    ('Sommer an der Ecke', ['fw-h31', 'fw-a58', 'fw-a49']),
    ('Hinter dem Tresen', ['fw-a46', 'fw-a57', 'fw-a45']),
    ('Ein Abend mit Freunden', ['fw-a8', 'fw-a28', 'fw-a7']),
    ('Gäste und Kerze', ['fw-h18', 'fw-a8', 'fw-h33']),
    ('Theke und Kerze', ['fw-h11', 'fw-h33', 'fw-h41']),
    ('Gäste an der Bar', ['fw-a17', 'fw-h42', 'fw-a4']),
    ('Rückbar und Glas', ['fw-a31', 'fw-a57', 'fw-h37']),
    ('Licht im Raum', ['fw-a1', 'fw-h30', 'fw-h18']),
    ('Drinks des Abends', ['fw-h1', 'fw-a36', 'fw-h21']),
]
NAMEN = json.dumps([[n, m[0]] for n, m in enumerate(MOTIVE)], ensure_ascii=False)


def drei(keys):
    reihe = ''.join(bau.img_tag(k, '34vw') for k in keys)
    return '<section class="fk fk3" aria-label="%s"><figure class="foto" style="--lq:url(%s)"><div class="fk3-reihe">%s</div><div class="fe-hof"></div><p class="fe-satz">%s</p></figure></section>' % (
        E(' '.join(SATZ)), bau.mache(keys[1])['lq'], reihe, bau.zl(SATZ))


def main():
    quelle = open(os.path.join(WEB, 'index.html')).read()
    alt = bau.fenster_fest('decke-hoch', SATZ, '50% 55%')
    assert quelle.count(alt) == 1, 'Fenster nicht gefunden'
    for n, m in enumerate(MOTIVE):
        name, keys = m[0], m[1]
        neu = bau.fenster_fest(keys[0], SATZ, m[2]) if len(keys) == 1 else drei(keys)
        s = quelle.replace(alt, neu)
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
        s = s.replace('</head>', '<link rel="stylesheet" href="%s/fw.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s"></head>' % (ORD, V, ORD, V), 1)
        schild = '<p class="vschild" aria-hidden="true"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(MOTIVE) - 1, E(name))
        s = s.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD="%s"</script><script src="%s/varianten-nav.js?v=%s"></script></body>' % (NAMEN, n, ORD, ORD, V), 1)
        open(os.path.join(HIER, '%02d.html' % n), 'w').write(s)
    print('%d Motive' % len(MOTIVE))


if __name__ == '__main__':
    main()
