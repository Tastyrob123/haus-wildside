# Walk on the Wild Side · Startseite, Kopf von «20:00 An der Theke · Was magst du?»: zehn Fassungen (29.10.2026).
# Robert: «Kann man das auch noch irgendwie schöner darstellen?» Nur der Kopf (Titel, Satz, Momos Satz) wechselt, Wortlaut bleibt. 00 = heute.
# Wechsel mit ← →. Aufruf: python3 _varianten/theke-kopf/bau.py → 00.html … 10.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
from bau import E, kz, mache, img_tag

ORD = '_varianten/theke-kopf'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('kopf.css', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('index.html').read()
a = basis.index('<div class="th-kopf">')
b = basis.index('<div class="th-weg"', a)

KZ = kz('20:00', 'An der Theke', 0)
SATZ = 'Eine Getränkekarte gibt es im Wild Side nicht. Wer an die Theke kommt, wird gefragt, was er mag, und Momo macht daraus einen Drink. So sieht das aus.'
Z1, Z2 = 'Du sagst mir, was du magst,', 'ich mache dir einen Drink.'
WER = 'Momo, hinter der Theke'


def titel(cls='', text='Was magst du?', i=1):
    return '<h2 class="titel %s"><span class="zl"><span class="z"><span style="--i:%d">%s</span></span></span></h2>' % (cls, i, text)


def satz(cls='', i=2):
    return '<p class="text sw %s" style="--i:%d">%s</p>' % (cls, i, E(SATZ))


def zitat(cls='', i=3, zeilen=False, auf='«'):
    t = '%s<br>%s' % (E(Z1), E(Z2)) if zeilen else E(Z1 + ' ' + Z2)
    return '<blockquote class="tk-z sw %s" style="--i:%d"><p>%s%s»</p><cite>%s</cite></blockquote>' % (cls, i, auf, t, E(WER))


def portrait():
    return '<figure class="kachel tk-portrait" style="--lq:url(%s)">%s</figure>' % (mache('momo-lacht')['lq'], img_tag('momo-lacht', '120px', extra=' style="object-position:58% 30%"'))


V = [
    ('Momos Satz als Titel', lambda: '<div class="tk tk01">%s<p class="tk-frage sw" style="--i:1">Was magst du?</p><h2 class="titel tk-gross">%s</h2>%s<p class="tk-wer sw" style="--i:3">%s</p></div>' % (
        KZ, '<span class="zl"><span class="z"><span style="--i:2">«%s</span></span><span class="z"><span style="--i:3">%s»</span></span></span>' % (E(Z1), E(Z2)), satz('', 4), E(WER))),
    ('Goldenes Anführungszeichen', lambda: '<div class="tk tk02"><div>%s%s%s</div>%s</div>' % (KZ, titel(), satz(), zitat('', 3, True, ''))),
    ('Frage und Antwort versetzt', lambda: '<div class="tk tk03"><div class="tk03-frage">%s%s%s</div>%s</div>' % (KZ, titel('tk-riesig'), satz(), zitat('', 3, True))),
    ('Titel und Antwort übereinander', lambda: '<div class="tk tk04">%s%s<p class="tk04-antwort sw" style="--i:2">«%s %s»</p><p class="tk-wer sw" style="--i:3">%s</p>%s</div>' % (
        KZ, titel('tk-riesig'), E(Z1), E(Z2), E(WER), satz('', 4))),
    ('Titel über die ganze Breite', lambda: '<div class="tk tk05">%s%s<div class="tk05-zwei">%s%s</div></div>' % (KZ, titel('tk-riesig'), satz(), zitat('', 3))),
    ('Mit Momo im Kreis', lambda: '<div class="tk tk06"><div>%s%s%s</div><div class="tk06-z sw" style="--i:3">%s<blockquote class="tk-z"><p>«%s»</p><cite>%s</cite></blockquote></div></div>' % (
        KZ, titel(), satz(), portrait(), E(Z1 + ' ' + Z2), E(WER))),
    ('Alles in der Mitte', lambda: '<div class="tk tk07">%s%s%s<i class="tk07-strich"></i>%s</div>' % (KZ, titel('tk-riesig'), satz(), zitat('', 3, True))),
    ('Momos Satz auf einer Karte', lambda: '<div class="tk tk08"><div>%s%s%s</div><div class="tk08-karte sw" style="--i:3"><span class="etikett">An der Theke</span><p>«%s»</p><cite>%s</cite></div></div>' % (
        KZ, titel(), satz(), E(Z1 + ' ' + Z2), E(WER))),
    ('Zwei Stimmen', lambda: '<div class="tk tk09">%s<div class="tk09-zeilen"><p class="tk09-z tk09-gast sw" style="--i:1"><span class="etikett">Momo fragt</span><b>Was magst du?</b></p>'
                            '<p class="tk09-z tk09-momo sw" style="--i:2"><span class="etikett">%s</span><b>«%s %s»</b></p></div>%s</div>' % (KZ, E(WER), E(Z1), E(Z2), satz('', 3))),
    ('Satz in Gold darunter', lambda: '<div class="tk tk10"><div>%s%s</div><div class="tk10-r">%s<p class="tk10-gold sw" style="--i:3">«%s %s»</p><p class="tk-wer sw" style="--i:4">%s</p></div></div>' % (
        KZ, titel('tk-riesig'), satz(), E(Z1), E(Z2), E(WER))),
]
LISTE = [[0, 'Heute']] + [[j + 1, n] for j, (n, _) in enumerate(V)]
KOPF = '<link rel="stylesheet" href="%s/kopf.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, kopf, name):
    h = basis[:a] + kopf + '\n' + basis[b:] if nr else basis
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / %02d</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script>\n</body>') % (nr, len(V), E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, '', 'Heute'))
    for j, (name, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(), name))
    print('00.html … %02d.html in %s' % (len(V), ORD))
