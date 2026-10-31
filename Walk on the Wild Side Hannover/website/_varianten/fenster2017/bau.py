#!/usr/bin/env python3
"""Walk on the Wild Side · Startseite, Fenster über «Seit 2017»: Motive ohne Decke zur Wahl (29.10.2026).
Jede Fassung = die echte index.html, nur das Bild im Fenster getauscht; Grösse und Satz bleiben. 00 = heute. Wechsel mit ← →."""
import os, sys, json, html
HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(HIER, '..', '..'))
sys.path.insert(0, WEB)
import bau
ORD = '_varianten/fenster2017'
V = '29107'
E = html.escape
SATZ = ['Zwei Eröffnungen,', 'eine Decke.']
MOTIVE = [('decke-hoch', 'Heute: die Decke über der Theke', '50% 55%'),
          ('fe-theke', 'Gäste an der Theke', '50% 62%'),
          ('fe-highball', 'Roter Highball', '50% 55%'),
          ('fe-zwei', 'Zwei Drinks vor der Rückbar', '50% 60%'),
          ('fe-coupe', 'Coupe in der Hand', '50% 50%'),
          ('fe-serviette', 'Stielglas auf der Serviette', '50% 62%'),
          ('fe-minze', 'Drink mit Minze', '50% 50%'),
          ('fe-old', 'Drink mit Orangenzeste', '50% 50%'),
          ('fe-probe', 'Drei Gläser zum Probieren', '50% 62%'),
          ('fe-negroni', 'Drink unter dem NEGRONI', '50% 45%')]
NAMEN = json.dumps([[n, m[1]] for n, m in enumerate(MOTIVE)], ensure_ascii=False)


def main():
    quelle = open(os.path.join(WEB, 'index.html')).read()
    alt = bau.fenster_fest('decke-hoch', SATZ, '50% 55%')
    assert quelle.count(alt) == 1, 'Fenster nicht gefunden'
    for n, (k, name, pos) in enumerate(MOTIVE):
        s = quelle.replace(alt, bau.fenster_fest(k, SATZ, pos))
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
        s = s.replace('</head>', '<link rel="stylesheet" href="%s/varianten-nav.css?v=%s"></head>' % (ORD, V), 1)
        schild = '<p class="vschild" aria-hidden="true"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(MOTIVE) - 1, E(name))
        s = s.replace('</body>', schild + '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD="%s"</script><script src="%s/varianten-nav.js?v=%s"></script></body>' % (NAMEN, n, ORD, ORD, V), 1)
        open(os.path.join(HIER, '%02d.html' % n), 'w').write(s)
    print('%d Motive' % len(MOTIVE))


if __name__ == '__main__':
    main()
