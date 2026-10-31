# Walk on the Wild Side · Programm-Seite, Abschnitt «Die Woche» (id="woche"): 15 Mischungen aus Stecktafel und Untersetzern (30.10.2026).
# Robert zu woche-20, Fassung 15 (Stecktafel) und 14 (Untersetzer): «bastel mal 15 Variationen aus den Elementen hier.»
# Bausteine: schwarze Rillentafel mit weissen Steckbuchstaben im Holzrahmen, runde Deckel mit Goldring und Ringschrift, Prata-Name, Etikett, Satz.
# Texte Wort für Wort aus unter.programm() (geprüft in woche-20/bau.py), nur echte Fotos. Bewegung nur über transform und opacity.
# Aufruf: python3 _varianten/woche-mix15/bau.py → 00.html … 15.html
import os, sys, json, html, importlib.util
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_spec = importlib.util.spec_from_file_location('w20', os.path.join(HIER, '_varianten', 'woche-20', 'bau.py'))
W = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(W)   # Texte, Bilder, Kopf aus woche-20
B, unter = W.B, W.unter
os.chdir(HIER)

E = html.escape
ORD = '_varianten/woche-mix15'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('m.css', 'm.js', 'nav.js'))))
TAGE, KURZ, fb, name, et, tx, kopf = W.TAGE, W.KURZ, W.fb, W.name, W.et, W.tx, W.kopf
RING = ['%s · WALK ON THE WILD SIDE · ' % t.upper() for _, t, _, _ in TAGE]


def sek(n, inner, cls='', innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf wx mx m%02d %s" id="woche" data-w="%d">%s</section>' % (n, cls, n, i)


def deckel(n, j, inner, cls='', stil=''):
    """Runder Deckel: Bild (oder anderes) innen, Goldring mit umlaufender Schrift."""
    pid = 'r%d-%d-%s' % (n, j, cls.replace(' ', '') or 'x')
    return '''<div class="md %s" style="%s">%s<svg class="md-ring" viewBox="0 0 300 300" aria-hidden="true"><defs><path id="%s" d="M150,150 m-128,0 a128,128 0 1,1 256,0 a128,128 0 1,1 -256,0"/></defs>
<circle cx="150" cy="150" r="146"/><circle cx="150" cy="150" r="112"/><text><textPath href="#%s" textLength="796" lengthAdjust="spacing">%s</textPath></text></svg></div>''' % (
        cls, stil, inner, pid, pid, E(RING[j] * 2))


def bild_deckel(n, j, sizes, cls='', stil=''):
    return deckel(n, j, fb(TAGE[j][0], sizes), cls, stil)


def tafel(zeilen, cls='', rahmen=True, start=0):
    """Rillentafel: zeilen = [(text, klasse)], jeder Buchstabe fällt einzeln in die Rille."""
    c = [start]

    def z(t, k):
        out = ''
        for ch in t:
            out += '<span style="--b:%d">%s</span>' % (c[0], '&nbsp;' if ch == ' ' else E(ch))
            c[0] += 1
        return '<p class="%s">%s</p>' % (k, out or '&nbsp;')
    r = '<div class="mt-r">%s</div>' % ''.join(z(t, k) for t, k in zeilen)
    return '<div class="mt %s" aria-hidden="true">%s</div>' % (cls, r) if rahmen else '<div class="mt-r %s" aria-hidden="true">%s</div>' % (cls, ''.join(z(t, k) for t, k in zeilen))


def satz(j, cls='m-satz', mit_name=True):
    k, t, u, s = TAGE[j]
    return '<div class="%s">%s%s%s</div>' % (cls, name(t) if mit_name else '', et(u), tx(s))


def zeilen_woche():
    return [('DIE WOCHE', 'rot'), ('', '')] + [('%s  %s' % (KURZ[j].upper(), u.upper()), '') for j, (k, t, u, s) in enumerate(TAGE)]


V = []


# 01 · Tafel über den Deckeln: eine breite Tafel, je Abend eine Spalte Steckbuchstaben; darunter die drei Deckel mit Name und Satz.
# Erst fallen die Buchstaben, dann senken sich die Deckel von oben auf ihren Platz.
def v01(n):
    sp = ''.join('<div class="m1-sp">%s</div>' % tafel([(KURZ[j].upper(), 'gross'), (u.upper(), '')], rahmen=False, start=j * 20) for j, (k, t, u, s) in enumerate(TAGE))
    tf = '<div class="mt m1-tafel" aria-hidden="true"><div class="mt-r m1-r">%s</div></div>' % sp.replace('aria-hidden="true"', '')
    dk = ''.join('<article class="m1-spalte" style="--n:%d">%s%s</article>' % (j, bild_deckel(n, j, '(max-width:760px) 70vw, 22vw'), satz(j)) for j in range(3))
    return sek(n, kopf() + '<div class="vauf">%s<div class="m1-reihe">%s</div></div>' % (tf, dk))
V.append(('Tafel über den Deckeln', v01))


# 02 · Deckel auf der Tafel: die Deckel liegen leicht schief auf einer grossen Tafel, unter jedem steckt sein Abend in Buchstaben.
# Sie werden nacheinander hingelegt: kommen etwas grösser von oben und setzen auf.
def v02(n):
    fl = ''.join('<div class="m2-platz" style="--n:%d;--w:%s">%s%s</div>' % (j, w, bild_deckel(n, j, '(max-width:760px) 60vw, 20vw'),
        tafel([(KURZ[j].upper(), ''), (u.upper(), 'klein')], rahmen=False, start=j * 20)) for j, ((k, t, u, s), w) in enumerate(zip(TAGE, ('-5deg', '3deg', '-2deg'))))
    sp = ''.join('<div style="--n:%d">%s</div>' % (j, satz(j)) for j in range(3))
    return sek(n, kopf() + '<div class="mt m2-tafel vauf"><div class="mt-r m2-r"><p class="rot m2-titel">%s</p><div class="m2-reihe">%s</div></div></div><div class="m2-saetze">%s</div>' % (
        ''.join('<span style="--b:%d">%s</span>' % (i, '&nbsp;' if c == ' ' else c) for i, c in enumerate('DIE WOCHE')), fl, sp))
V.append(('Deckel auf der Tafel', v02))


# 03 · Kleine Tafel unterm Deckel: jede Spalte ein Deckel, darunter eine eigene kleine Tafel mit Tag und Abend, dann der Satz.
# Der Deckel dreht sich herein, danach fallen die Buchstaben seiner Tafel.
def v03(n):
    sp = ''.join('<article class="m3-spalte vauf" style="--n:%d">%s%s%s</article>' % (j, bild_deckel(n, j, '(max-width:760px) 70vw, 22vw'),
        tafel([(t.upper(), 'rot'), (u.upper(), '')], 'm3-tafel'), satz(j, mit_name=False) ) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="m3-reihe">%s</div>' % sp)
V.append(('Kleine Tafel unterm Deckel', v03))


# 04 · Die Tafel zeigt mit: links bleibt die Tafel stehen, rechts ziehen die drei Deckel gross vorbei.
# Die Zeile des Abends, der gerade in der Mitte ist, leuchtet; die anderen treten zurück. Der Ring dreht sich mit dem Scrollen.
def v04(n):
    tf = tafel(zeilen_woche(), 'm4-tafel vauf')
    re = ''.join('<article class="m4-abend" data-i="%d">%s%s</article>' % (j, bild_deckel(n, j, '(max-width:760px) 70vw, 24vw'), satz(j)) for j in range(3))
    return sek(n, kopf() + '<div class="m4-raster"><div class="m4-links">%s</div><div class="m4-rechts">%s</div></div>' % (tf, re))
V.append(('Die Tafel zeigt mit', v04))


# 05 · Titel auf der Tafel: der Abschnittstitel selbst steckt auf der Tafel, rot DIE WOCHE, weiss DREI ABENDE, DREI TEMPI.
# Darunter die drei Deckel; ihre Ringe drehen sich beim Scrollen langsam weiter.
def v05(n):
    tf = tafel([('DIE WOCHE', 'rot'), ('DREI ABENDE,', ''), ('DREI TEMPI.', '')], 'm5-tafel vauf')
    dk = ''.join('<article class="m5-spalte" data-ring>%s%s</article>' % (bild_deckel(n, j, '(max-width:760px) 70vw, 22vw'), satz(j)) for j in range(3))
    return sek(n, '<div class="m5-kopf">%s<h2 class="mx-sr">Drei Abende, drei Tempi.</h2>%s</div><div class="m5-reihe">%s</div>' % (W.KZ, tf, dk))
V.append(('Titel auf der Tafel', v05))


# 06 · Ein Deckel, drei Abende: die Bühne steht. Links die Tafel, in der Mitte ein grosser Deckel, rechts der Satz.
# Beim Scrollen dreht sich der Ring weiter, Bild, Ringschrift und Satz wechseln von Donnerstag zu Freitag zu Samstag; die Tafelzeile leuchtet mit.
def v06(n):
    tf = tafel(zeilen_woche(), 'm6-tafel vauf')
    dk = '<div class="m6-deckel">%s</div>' % ''.join('<div class="m6-lage" style="--n:%d">%s</div>' % (j, bild_deckel(n, j, '(max-width:760px) 80vw, 34vw')) for j in range(3))
    st = '<div class="m6-saetze">%s</div>' % ''.join('<div class="m6-satz" style="--n:%d">%s</div>' % (j, satz(j, 'm-satz')) for j in range(3))
    return sek(n, '<div class="innen">%s</div><div class="m6-pin" data-pin><div class="m6-buehne"><div class="innen m6-raster">%s%s%s</div></div></div>' % (kopf(), tf, dk, st), innen=False)
V.append(('Ein Deckel, drei Abende', v06))


# 07 · Hingeworfen: auf einem breiten Tafelband liegen die drei Deckel übereinander, wie nach einem Abend auf den Tresen geworfen.
# Sie fliegen nacheinander von oben herein und drehen sich dabei in ihre Lage. Darunter die drei Sätze.
def v07(n):
    dk = ''.join('<div class="m7-wurf" style="--n:%d">%s</div>' % (j, bild_deckel(n, j, '(max-width:760px) 50vw, 20vw')) for j in range(3))
    band = '<div class="mt m7-band vauf"><div class="mt-r m7-r">%s<div class="m7-deckel">%s</div></div></div>' % (
        tafel([('DIE WOCHE', 'rot'), ('DO', ''), ('FR', ''), ('SA', '')], 'm7-ecke', rahmen=False), dk)
    sp = ''.join(satz(j) for j in range(3))
    return sek(n, kopf() + band + '<div class="m7-saetze">%s</div>' % sp)
V.append(('Hingeworfen', v07))


# 08 · Vorder- und Rückseite: jeder Deckel zeigt zuerst seine Tafelseite (Tag und Abend in Steckbuchstaben),
# dann dreht er sich um und das Bild mit Goldring kommt nach vorn. Nacheinander, Donnerstag zuerst.
def v08(n):
    def karte(j):
        k, t, u, s = TAGE[j]
        vorn = '<div class="m8-vorn">%s</div>' % tafel([(KURZ[j].upper(), 'gross'), (u.upper().replace(', ', ', ').replace(' AN ', ' AN '), 'klein')], rahmen=False)
        return '<article class="m8-spalte" style="--n:%d"><div class="m8-karte">%s<div class="m8-hinten">%s</div></div>%s</article>' % (
            j, vorn, bild_deckel(n, j, '(max-width:760px) 70vw, 22vw'), satz(j))
    return sek(n, kopf() + '<div class="m8-reihe vauf">%s</div>' % ''.join(karte(j) for j in range(3)))
V.append(('Vorder- und Rückseite', v08))


# 09 · Unter der Tafel: oben ein breites Tafelband mit den drei Abenden, die Deckel hängen halb unter seiner Kante hervor.
# Sie schieben sich beim Auftritt unter der Tafel heraus nach unten.
def v09(n):
    sp = ''.join('<div class="m9-sp">%s</div>' % tafel([(KURZ[j].upper() + '  ' + u.upper(), '')], rahmen=False, start=j * 20) for j, (k, t, u, s) in enumerate(TAGE))
    tf = '<div class="mt m9-tafel"><div class="mt-r m9-r">%s</div></div>' % sp
    dk = ''.join('<article class="m9-spalte" style="--n:%d"><div class="m9-schacht">%s</div>%s</article>' % (j, bild_deckel(n, j, '(max-width:760px) 64vw, 20vw'), satz(j)) for j in range(3))
    return sek(n, kopf() + '<div class="vauf m9-gruppe">%s<div class="m9-reihe">%s</div></div>' % (tf, dk))
V.append(('Unter der Tafel', v09))


# 10 · Drei Leisten: jeder Abend eine lange Tafelleiste mit Tag und Abend, am rechten Ende rollt sein Deckel heran und legt sich über die Kante.
# Darunter Name und Satz. Leiste für Leiste, wenn sie ins Bild kommt.
def v10(n):
    z = ''.join('<article class="m10-zeile vauf"><div class="m10-oben">%s%s</div>%s</article>' % (
        tafel([('%s  %s' % (KURZ[j].upper(), u.upper()), '')], 'm10-leiste'), bild_deckel(n, j, '(max-width:760px) 40vw, 16vw'), satz(j, 'm-satz m10-satz')) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="m10-liste">%s</div>' % z)
V.append(('Drei Leisten', v10))


# 11 · Rollt über die Tafel: die Bühne steht, eine breite Tafel mit drei Spalten. Beim Scrollen rollen die Deckel von links
# über die Tafel und bleiben jeder über seinem Abend liegen; danach erscheinen Name und Satz.
def v11(n):
    sp = ''.join('<div class="m11-sp" style="--n:%d"><div class="m11-roll">%s</div>%s</div>' % (j, bild_deckel(n, j, '(max-width:760px) 60vw, 17vw'),
        tafel([(KURZ[j].upper(), 'gross'), (u.upper(), '')], rahmen=False, start=j * 20)) for j, (k, t, u, s) in enumerate(TAGE))
    tf = '<div class="mt m11-tafel vauf"><div class="mt-r m11-r">%s</div></div>' % sp
    st = '<div class="m11-saetze">%s</div>' % ''.join('<div class="m11-satz" style="--n:%d">%s</div>' % (j, satz(j)) for j in range(3))
    return sek(n, '<div class="innen">%s</div><div class="m11-pin" data-pin><div class="m11-buehne"><div class="innen">%s%s</div></div></div>' % (kopf(), tf, st), innen=False)
V.append(('Rollt über die Tafel', v11))


# 12 · Im Wechsel: drei Zeilen, der Deckel gross abwechselnd links und rechts; daneben eine Tafel mit dem Tag in Steckbuchstaben und der Satz.
# Der Deckel gleitet von seiner Seite herein, die Buchstaben fallen nach.
def v12(n):
    z = ''.join('<article class="m12-zeile vauf %s"><div class="m12-bild">%s</div><div class="m12-rechts">%s%s</div></article>' % (
        'rechts' if j == 1 else '', bild_deckel(n, j, '(max-width:760px) 80vw, 34vw'), tafel([(t.upper(), 'rot'), (u.upper(), '')], 'm12-tafel'), satz(j, mit_name=False)) for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="m12-liste">%s</div>' % z)
V.append(('Im Wechsel', v12))


# 13 · Schwarze Deckel: die Deckel selbst aus Tafelmaterial, schwarz mit Rillen, die Ringschrift in weissen Steckbuchstaben, nur der Rand in Gold.
# Sie wachsen beim Auftritt aus der Mitte, der Ring dreht sich dabei eine Vierteldrehung in seine Lage.
def v13(n):
    sp = ''.join('<article class="m13-spalte" style="--n:%d">%s%s</article>' % (j, bild_deckel(n, j, '(max-width:760px) 70vw, 24vw', 'schwarz'), satz(j)) for j in range(3))
    return sek(n, kopf() + '<div class="m13-reihe vauf">%s</div>' % sp)
V.append(('Schwarze Deckel', v13))


# 14 · Drei Tafeln: jeder Abend eine hohe Tafel im Holzrahmen. Oben liegt der Deckel, darunter stecken Tag und Abend, unten der Satz.
# Die Tafeln steigen nacheinander auf, dann fallen ihre Buchstaben.
def v14(n):
    sp = ''.join('<article class="mt m14-tafel" style="--n:%d"><div class="mt-r m14-r">%s%s%s</div></article>' % (
        j, bild_deckel(n, j, '(max-width:760px) 60vw, 18vw'), tafel([(t.upper(), 'rot'), (u.upper(), '')], rahmen=False, start=j * 25).replace('aria-hidden="true"', ''), satz(j, mit_name=False))
        for j, (k, t, u, s) in enumerate(TAGE))
    return sek(n, kopf() + '<div class="m14-reihe vauf">%s</div>' % sp)
V.append(('Drei Tafeln', v14))


# 15 · Die Tafel wechselt: die Bühne steht. Links eine grosse Tafel, rechts ein Deckel. Beim Scrollen wird auf der Tafel umgesteckt,
# Donnerstag, Freitag, Samstag, und der alte Deckel rollt hinaus, der neue herein. Darunter wechselt der Satz.
def v15(n):
    lagen = ''.join('<div class="m15-lage" style="--n:%d">%s</div>' % (j, tafel([(t.upper(), 'rot'), (u.upper(), '')], rahmen=False)) for j, (k, t, u, s) in enumerate(TAGE))
    tf = '<div class="mt m15-tafel"><div class="mt-r m15-r"><p class="m15-kopf">DIE WOCHE</p><div class="m15-lagen">%s</div></div></div>' % lagen
    dk = '<div class="m15-deckel">%s</div>' % ''.join('<div class="m15-d" style="--n:%d">%s</div>' % (j, bild_deckel(n, j, '(max-width:760px) 70vw, 28vw')) for j in range(3))
    st = '<div class="m15-saetze">%s</div>' % ''.join('<div class="m15-satz" style="--n:%d">%s</div>' % (j, satz(j)) for j in range(3))
    return sek(n, '<div class="innen">%s</div><div class="m15-pin" data-pin><div class="m15-buehne"><div class="innen"><div class="m15-raster"><div>%s%s</div>%s</div></div></div></div>' % (kopf(), tf, st, dk), innen=False)
V.append(('Die Tafel wechselt', v15))


def seite(n):
    h = unter.programm()
    if n:
        a = h.rfind('<section', 0, h.find('id="woche"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, nm] for j, (nm, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/m.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/m.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
