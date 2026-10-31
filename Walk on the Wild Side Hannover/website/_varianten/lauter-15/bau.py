# Walk on the Wild Side · Startseite, Abschnitt «23:00 Lauter · Samstags legt jemand auf.» (id="lauter"): 15 Fassungen (29.10.2026).
# Robert: «gib mir 15 verschiedene Visualisierungsmöglichkeiten für den Abschnitt.» 00 = heutiger Stand.
# Jede Fassung eigene Darstellung und eigene Bewegung; Wortlaut bleibt, nur echte Plakate und Fotos der Bar, Abende aus LINEUP (bau.py).
# Nur transform, von Anfang an deckend. Wechsel mit ← →. Aufruf: python3 _varianten/lauter-15/bau.py → 00.html … 15.html
import os, sys, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau
from bau import E, kz, mache, img_tag, knopf, ueber, zl, LINEUP
from bilder import BILDER

ORD = '_varianten/lauter-15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('lauter.css', 'lauter.js', 'varianten-nav.js', 'varianten-nav.css'))))
basis = open('index.html').read()
a = basis.index('<section class="kap auf" id="lauter">')
b = basis.index('</section>', a) + len('</section>')

KZ = kz('23:00', 'Lauter', 0)
S = ['Samstags legen DJs an der Bar auf, rund einmal im Monat, von 21 bis 1 Uhr. Momo mixt dazu.',
     'Donnerstags spielt ab und zu jemand live, mitten im Raum, ohne Eintritt.',
     'Und an manchen Abenden steht neben Momo ein Gast aus einer anderen Bar mit eigenen Drinks.']
TEXT = ' '.join(S)
KNOPF = '<div class="knoepfe sw" style="--i:3">%s</div>' % knopf('Das Programm', 'programm.html')
UEBER = ueber('An manchen Abenden gehört die Empore euch.')
PLAKATE = []
for _, _, _, p in LINEUP:
    if p not in PLAKATE:
        PLAKATE.append(p)
POS = {'konzert-love': '50% 40%'}


def titel(cls='', zeilen=('Samstags legt', 'jemand auf.')):
    return '<h2 class="titel %s">%s</h2>' % (cls, zl(list(zeilen), i0=1))


def text(cls='', i=2, t=TEXT):
    return '<p class="text sw %s" style="--i:%d">%s</p>' % (cls, i, E(t))


def k(key, cls='', sizes='25vw', stil=''):
    pos = POS.get(key)
    return '<figure class="kachel %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(key)['lq'], stil, img_tag(key, sizes, extra=' style="object-position:%s"' % pos if pos else ''))


def flyer(cls='', alle=False, i=2):
    """Der Flyer der Seite (cremefarbene Karte mit dem echten Plakat); alle=True legt alle Plakate hinein, eines sichtbar."""
    d0, n0, r0, p0 = LINEUP[0]
    bilder = ''.join(img_tag(p, '36vw', extra=' data-k="%s" class="%s"' % (p, 'an' if p == p0 else '')) for p in (PLAKATE if alle else [p0]))
    daten = json.dumps([[d, n, r, p] for d, n, r, p in LINEUP], ensure_ascii=False).replace('"', '&quot;')
    return ('<div class="flyer lv-flyer sw %s" style="--i:%d" data-abende="%s"><figure class="foto" style="--lq:url(%s)">%s</figure>'
            '<div class="fl-unten"><span class="fl-reihe">Die DJ-Abende der Bar · samstags 21 bis 1 Uhr</span><p class="fl-name">%s</p><p class="fl-datum">%s%s</p></div></div>') % (
        cls, i, daten, mache(p0)['lq'], bilder, E(n0), E(d0), (' · ' + E(r0)) if r0 else '')


def kopf(cls=''):
    return '<div class="lv-kopf %s">%s%s%s%s</div>' % (cls, KZ, titel(), text(), KNOPF)


def kap(n, inner, voll=False):
    return '<section class="kap auf lv lv-s%02d" id="lauter" data-v="%d">%s</section>' % (n, n, inner if voll else '<div class="innen">%s</div>' % inner)


def datum_teile(d):
    t, m, j = d.split('.')
    return t, ['Jan', 'Feb', 'März', 'April', 'Mai', 'Juni', 'Juli', 'Aug', 'Sept', 'Okt', 'Nov', 'Dez'][int(m) - 1] + ' ' + j


V = []

# 01 Die Plakatwand
def v01():
    wand = k(PLAKATE[0], 'p-gross', '30vw') + ''.join(k(p, '', '15vw') for p in PLAKATE[1:]) + k('konzert-love', '', '15vw')
    return kap(1, '<div class="lv01">%s<div class="lv01-wand">%s</div></div>%s' % (kopf(), wand, UEBER))
V.append(('Die Plakatwand', 'Alle Plakate der DJ-Abende als dichte Wand, das neueste gross; jedes wird beim Auftritt einmal angedrückt wie frisch geklebt.', v01))

# 02 Der Plattenteller
def v02():
    d0, n0, r0, p0 = LINEUP[0]
    platte = ('<div class="lv02-teller sw" style="--i:2"><div class="lv02-platte"><figure class="lv02-label" style="--lq:url(%s)">%s</figure></div>'
              '<svg class="lv02-arm" viewBox="0 0 120 220" aria-hidden="true"><circle cx="96" cy="22" r="14"/><path d="M96 22 L80 170 L58 196"/><rect x="46" y="190" width="22" height="12" rx="2" transform="rotate(-30 57 196)"/></svg>'
              '<p class="lv02-titel"><span class="etikett">Zuletzt aufgelegt</span><b>%s</b><small>%s%s</small></p></div>') % (
        mache(p0)['lq'], img_tag(p0, '20vw'), E(n0), E(d0), (' · ' + E(r0)) if r0 else '')
    return kap(2, '<div class="lv02">%s%s<div class="lv02-bilder">%s%s</div></div>%s' % (kopf(), platte, k('konzert-love'), k('saengerin'), UEBER))
V.append(('Der Plattenteller', 'Das neueste Plakat liegt als Etikett auf einer Platte, die sich dreht, solange der Abschnitt im Bild ist.', v02))

# 03 Die Setliste
def v03():
    zeilen = ''.join('<button class="lv03-z%s" data-k="%s" data-name="%s" data-datum="%s"><span>%s</span><b>%s</b><small>%s</small></button>' % (
        ' an' if j == 0 else '', p, E(nm), E(d + (' · ' + r if r else '')), E(d), E(nm), E(r)) for j, (d, nm, r, p) in enumerate(LINEUP))
    return kap(3, '<div class="lv03">%s<div class="lv03-liste sw" style="--i:2"><span class="etikett">Die DJ-Abende der Bar</span>%s</div>%s</div>%s' % (kopf(), zeilen, flyer('', True, 3), UEBER))
V.append(('Die Setliste', 'Alle DJ-Abende als Liste wie eine Setliste; fährt man über einen Abend, schiebt sich sein Plakat in den Flyer.', v03))

# 04 Drei Arten von Abend
def v04():
    karten = [(PLAKATE[0], 'Samstags', S[0], '--d:40px'), ('saengerin', 'Donnerstags', S[1], '--d:110px'), ('gast-nils', 'An manchen Abenden', S[2], '--d:70px')]
    inn = ''.join('<div class="lv04-k" style="%s">%s<span class="etikett">%s</span><p>%s</p></div>' % (st, k(key, '', '33vw'), E(et), E(t)) for key, et, t, st in karten)
    return kap(4, '<div class="lv04-kopf">%s%s</div><div class="lv04-karten">%s</div><div class="lv04-fuss">%s</div>%s' % (KZ, titel('t-gross'), inn, KNOPF, UEBER))
V.append(('Drei Arten von Abend', 'Der Satz in drei Karten: samstags die DJs, donnerstags live, an manchen Abenden ein Gast; die Karten kommen aus verschiedenen Tiefen und stehen zugleich.', v04))

# 05 Der Pegel
def v05():
    balken = ''.join('<i style="--h:%d;--t:%.2fs;--v:%.2fs"></i>' % (h, t, v) for h, t, v in
                     [((j * 37) % 70 + 22, .6 + (j * 13) % 9 / 10, (j * 7) % 10 / 10) for j in range(56)])
    return kap(5, '<div class="lv05-kopf">%s%s%s%s</div><div class="lv05-pegel sw" style="--i:2" aria-hidden="true">%s</div><div class="lv05-reihe">%s%s%s</div>%s' % (
        KZ, titel('t-gross'), text('', 2), KNOPF, balken, flyer('', False, 3), k('konzert-love', '', '33vw'), k('saengerin', '', '33vw'), UEBER))
V.append(('Der Pegel', 'Unter dem Titel ein schmales Band aus goldenen Balken, die sich wie eine Lautstärkeanzeige heben und senken.', v05))

# 06 Der Flyer fällt auf den Tresen
def v06():
    return kap(6, '<div class="lv06-kopf">%s%s%s%s</div><div class="lv06-drei">%s%s%s</div>%s' % (
        KZ, titel('t-gross'), text(), KNOPF, k('konzert-love', 'lv06-f', '28vw'), flyer('lv06-flyer', False, 2), k('saengerin', 'lv06-f', '28vw'), UEBER))
V.append(('Der Flyer fällt auf den Tresen', 'Text mittig, darunter Foto, Flyer, Foto; der Flyer fällt beim Auftritt von oben auf den Tresen und bleibt schräg liegen.', v06))

# 07 Der Flyer wechselt
def v07():
    return kap(7, '<div class="lauter lv07">%s%s<div class="lauter-bilder">%s%s</div></div>%s' % (
        kopf('kopf'), flyer('', True, 2), k('konzert-love'), k('saengerin'), UEBER))
V.append(('Der Flyer wechselt', 'Aufbau wie heute, aber der Flyer blättert von selbst durch alle Plakate der DJ-Abende, Name und Datum wechseln mit.', v07))

# 08 Die Bühne
def v08():
    d0, n0, r0, p0 = LINEUP[0]
    quer = ('<div class="flyer lv08-quer sw" style="--i:3"><figure class="foto" style="--lq:url(%s)">%s</figure><div class="fl-unten"><span class="fl-reihe">Die DJ-Abende der Bar · samstags 21 bis 1 Uhr</span>'
            '<p class="fl-name">%s</p><p class="fl-datum">%s%s</p></div></div>') % (mache(p0)['lq'], img_tag(p0, '14vw'), E(n0), E(d0), (' · ' + E(r0)) if r0 else '')
    return kap(8, '<div class="lv08">%s%s%s%s%s</div>%s' % (k('konzert', 'lv08-buehne', '60vw'), kopf(), quer, k('saengerin', 'lv08-a', '25vw'), k('konzert-love', 'lv08-b', '25vw'), UEBER))
V.append(('Die Bühne', 'Ein breites Konzertfoto als Bühne, das beim Auftritt langsam heranzoomt; darunter der Flyer quer und zwei Fotos.', v08))

# 09 Von 21 bis 1 Uhr
def v09():
    uhr = ''.join('<span style="--x:%d"><b>%s</b></span>' % (j, h) for j, h in enumerate(['21 Uhr', '22', '23', '0', '1 Uhr']))
    return kap(9, '<div class="lv09">%s<div class="lv09-r">%s%s%s<div class="lv09-zeit sw" style="--i:2"><span class="etikett">Samstags</span><div class="lv09-strahl"><i></i>%s</div></div>%s<div class="lv09-bilder">%s%s</div></div></div>%s' % (
        flyer('lv09-flyer', False, 1), KZ, titel(), text('', 2), uhr, KNOPF, k('konzert-love', '', '25vw'), k('saengerin', '', '25vw'), UEBER))
V.append(('Von 21 bis 1 Uhr', 'Links gross der Flyer, rechts der Text mit einer Zeitleiste von 21 bis 1 Uhr, deren Goldlinie sich beim Auftritt zieht.', v09))

# 10 Die Gäste hinter der Theke
def v10():
    gaeste = ['gast-musa', 'gast-havn', 'gast-nils', 'gast-enlil']
    kachel = ''.join('<figure class="lv10-g" style="--n:%d">%s<figcaption>%s</figcaption></figure>' % (j, k(g, '', '20vw'), E(BILDER[g][1])) for j, g in enumerate(gaeste))
    return kap(10, '<div class="lv10">%s<div class="lv10-wand">%s%s</div></div>%s' % (kopf(), flyer('lv10-flyer', False, 2), kachel, UEBER))
V.append(('Die Gäste hinter der Theke', 'Neben dem Flyer die Gastschichten aus anderen Bars mit Namen; die Kacheln richten sich beim Auftritt auf.', v10))

# 11 Der Kalender
def v11():
    blaetter = ''
    for j, (d, nm, r, p) in enumerate(LINEUP):
        t, m = datum_teile(d)
        blaetter += '<div class="lv11-b%s" style="--n:%d"><b>%s</b><span>%s</span><p>%s</p></div>' % (' erst' if j == 0 else '', j, t, m, E(nm))
    return kap(11, '<div class="lv11">%s<div class="lv11-kal">%s</div>%s</div>%s' % (kopf(), blaetter, flyer('lv11-flyer', False, 3), UEBER))
V.append(('Der Kalender', 'Jeder DJ-Abend als Kalenderblatt mit grossem Tag, das neueste in Creme; die Blätter setzen sich nacheinander.', v11))

# 12 Das Plakat an der Wand
def v12():
    p0 = PLAKATE[0]
    plakat = '<div class="lv12-plakat"><i class="lv12-nagel"></i><i class="lv12-nagel"></i><figure class="foto" style="--lq:url(%s)">%s</figure></div>' % (mache(p0)['lq'], img_tag(p0, '40vw'))
    return kap(12, '<div class="lv12">%s<div class="lv12-r">%s%s%s%s<div class="lv12-bilder">%s%s</div></div></div>%s' % (
        plakat, KZ, titel('t-gross'), text(), KNOPF, k('konzert-love', '', '25vw'), k('saengerin', '', '25vw'), UEBER))
V.append(('Das Plakat an der Wand', 'Das Plakat hängt gross an zwei Nägeln an der Wand und pendelt sich beim Auftritt ein; daneben Text und zwei Fotos.', v12))

# 13 Das Line-up
def v13():
    namen, schon = [], set()
    for d, nm, r, p in LINEUP:
        if nm in schon:
            continue
        schon.add(nm)
        namen.append((nm, d))
    zeilen = ''.join('<span class="z"><span style="--i:%d">%s <small>%s</small></span></span>' % (j + 1, E(nm), E(d)) for j, (nm, d) in enumerate(namen))
    return kap(13, '<div class="lv13">%s<div class="lv13-namen"><span class="etikett sw" style="--i:0">Die DJ-Abende der Bar · samstags 21 bis 1 Uhr</span><p class="lv13-z zl">%s</p></div></div>'
                   '<div class="lv13-bilder">%s%s%s</div>%s' % (kopf(), zeilen, flyer('', False, 2), k('konzert-love', '', '33vw'), k('saengerin', '', '33vw'), UEBER))
V.append(('Das Line-up', 'Die Namen aller DJs gross untereinander wie auf einem Festivalplakat, Zeile für Zeile aus dem Schlitz.', v13))

# 14 Das Programmheft
def v14():
    liste = ''.join('<div><span>%s</span><b>%s</b></div>' % (E(d), E(nm)) for d, nm, r, p in LINEUP[:5])
    p0 = PLAKATE[0]
    return kap(14, '<div class="lv14-heft"><div class="lv14-l">%s%s%s%s</div><div class="lv14-r"><figure class="foto" style="--lq:url(%s)">%s</figure><span class="etikett">Die DJ-Abende der Bar</span><div class="lv14-liste">%s</div></div></div>%s' % (
        KZ, titel(), text(), KNOPF, mache(p0)['lq'], img_tag(p0, '24vw'), liste, UEBER))
V.append(('Das Programmheft', 'Ein aufgeschlagenes Heft in Creme: links der Text, rechts Plakat und die letzten Abende; die rechte Seite klappt beim Auftritt auf.', v14))

# 15 Der Filmstreifen
def v15():
    reihe = ['konzert', 'konzert-love', 'saengerin', PLAKATE[0], 'voll', 'saengerin-sw', 'silvester', PLAKATE[1]]
    band = ''.join(k(x, '', '22vw') for x in reihe)
    return kap(15, '<div class="innen"><div class="lv15-kopf">%s%s<div>%s%s</div></div></div><div class="lv15-film"><div class="lv15-spur">%s%s</div></div><div class="innen">%s</div>' % (
        KZ, titel('t-gross'), text(), KNOPF, band, band, UEBER), voll=True)
V.append(('Der Filmstreifen', 'Unter dem Text läuft ein Filmstreifen mit Fotos und Plakaten von selbst langsam durchs Bild, mit Lochrand oben und unten.', v15))

assert len(V) == 15
LISTE = [[0, 'Heute']] + [[j + 1, n] for j, (n, _, _) in enumerate(V)]
KOPF = '<link rel="stylesheet" href="%s/lauter.css?v=%s"><link rel="stylesheet" href="%s/varianten-nav.css?v=%s">' % (ORD, VER, ORD, VER)


def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:] if nr else basis
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', KOPF + '\n</head>', 1)
    h = h.replace('<title>', '<title>%02d · %s · ' % (nr, E(name)), 1)
    fuss = ('<p class="vschild"><b>%02d / 15</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>\n'
            '<script src="%s/varianten-nav.js?v=%s" defer></script><script src="%s/lauter.js?v=%s" defer></script>\n</body>') % (
        nr, E(name), json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', fuss, 1)


if __name__ == '__main__':
    open(os.path.join(ORD, '00.html'), 'w').write(seite(0, '', 'Heute'))
    for j, (name, _, f) in enumerate(V):
        open(os.path.join(ORD, '%02d.html' % (j + 1)), 'w').write(seite(j + 1, f(), name))
    print('00.html … 15.html in', ORD)
