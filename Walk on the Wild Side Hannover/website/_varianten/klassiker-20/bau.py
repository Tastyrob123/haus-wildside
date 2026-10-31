# Walk on the Wild Side · Drinks-Seite, «Die Klassiker»: 20 andere Darstellungen (30.10.2026).
# Robert: «Gib mir 20 alternative Visualisierungsmöglichkeiten für den Abschnitt.» Je Fassung eine eigene Anordnung und eine eigene Bewegung.
# Texte nur aus der heutigen Drinks-Seite (unter.py), nichts dazu. 00 = heutiger Stand. Wechsel mit ← →.
# Aufruf: python3 _varianten/klassiker-20/bau.py → 00.html … 20.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import unter
from bilder import mache

E = html.escape
ORD = '_varianten/klassiker-20'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))

KZ = B.kz('Die Klassiker', 'Auch ohne Frage', 0)
TITEL = B.h2(['Und wer einen', 'Negroni will.'])
LEAD = 'Wer lieber etwas Bekanntes will, bekommt es. Ein paar Drinks gehören fest zum Haus.'
KL = [('Negroni', 'Gin, Wermut, Bitter, auf Eis gerührt. Der Schriftzug über der Vitrine ist kein Zufall: Den Negroni gibt es an jedem Abend.'),
      ('Paloma', 'Tequila, Grapefruit, Limette und Soda. Im Sommer 2025 gab es ihm zu Ehren eine ganze Nacht.'),
      ('Mexikaner', 'Der scharfe Shot des Hauses. An Geburtstagen der Bar und an Silvester gibt es ihn die ganze Nacht, Wild-Side-Tradition.'),
      ('Ohne Alkohol', 'Shrub, Soda, Kräuter, klarer Saft: Momo baut jeden Drink auch ohne Alkohol, mit derselben Sorgfalt.')]
# Dieselben Sätze, nur in Kern und Rest geteilt (Fassung 13), kein Wort dazu.
SATZ = [('Den Negroni gibt es an jedem Abend.', 'Gin, Wermut, Bitter, auf Eis gerührt. Der Schriftzug über der Vitrine ist kein Zufall.'),
        ('Im Sommer 2025 gab es ihm zu Ehren eine ganze Nacht.', 'Tequila, Grapefruit, Limette und Soda.'),
        ('Der scharfe Shot des Hauses.', 'An Geburtstagen der Bar und an Silvester gibt es ihn die ganze Nacht, Wild-Side-Tradition.'),
        ('Momo baut jeden Drink auch ohne Alkohol, mit derselben Sorgfalt.', 'Shrub, Soda, Kräuter, klarer Saft.')]
HAUPT = 'glas-negroni'
BILD = ['fe-negroni', 'fe-highball', 'glas-kerze', 'fe-minze']   # je Drink ein Glas aus den Google-Fotos des Hauses
POS = {'fe-negroni': '50% 62%', 'fe-highball': '45% 40%', 'glas-kerze': '45% 60%', 'fe-minze': '50% 35%', 'glas-negroni': '42% 60%'}


def img(k, sizes):
    return B.img_tag(k, sizes, extra=' style="object-position:%s"' % POS.get(k, '50% 50%'))


def kachel(k, sizes, cls='', stil=''):
    return '<figure class="kachel %s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def foto(k, sizes, cls='foto', stil=''):
    return '<figure class="%s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img(k, sizes))


def lead(i=1, cls='text'):
    return '<p class="%s sw" style="--i:%d">%s</p>' % (cls, i, E(LEAD))


def kopf(cls='k-kopf'):
    return '<div class="%s">%s%s%s</div>' % (cls, KZ, TITEL, lead())


def kopf_quer():
    """Titel links, Satz rechts, auf einer Grundlinie."""
    return '<div class="k-quer"><div>%s%s</div>%s</div>' % (KZ, TITEL, lead())


def eintrag(j, cls='k-e', h='h3', extra=''):
    t, s = KL[j]
    return '<div class="%s" style="--n:%d">%s<%s class="titel">%s</%s><p class="text">%s</p></div>' % (cls, j, extra, h, E(t), h, E(s))


def sek(n, inhalt, hell=True, innen=True):
    return '<section class="kap %sauf kx v%02d" id="klassiker">%s</section>' % ('hell ' if hell else '', n, '<div class="innen">%s</div>' % inhalt if innen else inhalt)


V = []


# 01 · Der Wechsel: links steht ein Glas, rechts die Liste. Wer weiterliest, dem wechselt das Bild zum Drink, über den er gerade liest.
def v01(n):
    bilder = ''.join(kachel(k, '(max-width:760px) 100vw, 44vw', 'w-b' + (' an' if j == 0 else '')) for j, k in enumerate(BILD))
    return sek(n, '<div class="w-gr" data-w><div class="w-sp"><div class="w-bilder">%s</div></div><div class="w-txt">%s%s</div></div>' % (
        bilder, kopf(), ''.join(eintrag(j, 'w-e' + (' an' if j == 0 else '')) for j in range(4))))
V.append(('Der Wechsel', v01))


# 02 · Die Spalte: Titel und die vier Namen bleiben links stehen, rechts ziehen die Gläser vorbei; der Name des Glases im Blick leuchtet golden.
def v02(n):
    idx = ''.join('<li class="%s">%s</li>' % ('an' if j == 0 else '', E(t)) for j, (t, s) in enumerate(KL))
    rechts = ''.join('<article class="sp-g" style="--n:%d">%s%s</article>' % (j, kachel(BILD[j], '(max-width:760px) 100vw, 46vw', 'sp-b'), eintrag(j, 'sp-e'))
                     for j in range(4))
    return sek(n, '<div class="sp-gr" data-sp><div class="sp-l"><div class="sp-fix">%s<ol class="sp-idx">%s</ol></div></div><div class="sp-r">%s</div></div>' % (kopf(), idx, rechts))
V.append(('Die Spalte', v02))


# 03 · Das Band: vier Gläser Wand an Wand über die ganze Breite; jedes Bild steigt in seinem Rahmen auf, darunter je Glas Name und Satz.
def v03(n):
    band = ''.join('<figure class="bd-f" style="--n:%d;--lq:url(%s)"><div class="bd-i">%s</div></figure>' % (j, mache(k)['lq'], img(k, '(max-width:760px) 50vw, 25vw')) for j, k in enumerate(BILD))
    return sek(n, '<div class="innen">%s</div><div class="bd vauf">%s</div><div class="innen bd-sp staffel">%s</div>' % (
        kopf_quer(), band, ''.join(eintrag(j, 'bd-e') for j in range(4))), innen=False)
V.append(('Das Band', v03))


# 04 · Der Aufruf: die Namen stehen riesig untereinander, rechts davon der Satz. Die Zeile in der Bildmitte ist hell, die anderen treten zurück.
def v04(n):
    zeilen = ''.join('<div class="af-z"><h3 class="titel af-n">%s</h3><p class="text">%s</p></div>' % (E(t), E(s)) for t, s in KL)
    return sek(n, '<div class="af-kopf">%s%s</div><div class="af-liste" data-af>%s</div>' % (
        kopf(), kachel(HAUPT, '(max-width:760px) 100vw, 30vw', 'af-bild sw', '--i:2;'), zeilen))
V.append(('Der Aufruf', v04))


# 05 · Vier Platten: auf dunklem Grund vier cremefarbene Platten im Quadrat, jede mit ihrem Glas; sie setzen sich nacheinander.
def v05(n):
    pl = ''.join('<article class="pl-p" style="--n:%d">%s%s</article>' % (j, kachel(BILD[j], '(max-width:760px) 40vw, 20vw', 'pl-b'), eintrag(j, 'pl-e'))
                 for j in range(4))
    return sek(n, '%s<div class="pl-gr vauf">%s</div>' % (kopf_quer(), pl), hell=False)
V.append(('Vier Platten', v05))


# 06 · Einer vorn: der Negroni gross, so wie im Titel; Paloma, Mexikaner und Ohne Alkohol klein in einer Reihe darunter.
def v06(n):
    gross = '<article class="ev-g vauf">%s<div class="ev-gt">%s<h3 class="titel">%s</h3><p class="text">%s</p></div></article>' % (
        kachel(HAUPT, '(max-width:760px) 100vw, 56vw', 'ev-gb'), KZ, E(KL[0][0]), E(KL[0][1]))
    klein = ''.join('<article class="ev-k" style="--n:%d">%s%s</article>' % (j, kachel(BILD[j], '(max-width:760px) 100vw, 30vw', 'ev-kb'), eintrag(j, 'ev-e'))
                    for j in (1, 2, 3))
    return sek(n, '<div class="ev-kopf">%s%s</div>%s<div class="ev-reihe staffel">%s</div>' % (TITEL, lead(), gross, klein))
V.append(('Einer vorn', v06))


# 07 · Das Blatt: eine cremefarbene Karte mit doppeltem Goldrand auf dunklem Grund, mittig gesetzt; die Drinks erscheinen Zeile um Zeile, dazwischen ziehen sich feine Linien.
def v07(n):
    zeilen = ''.join('<div class="bl-z" style="--n:%d"><i class="bl-l"></i><h3 class="titel">%s</h3><p>%s</p></div>' % (j, E(t), E(s)) for j, (t, s) in enumerate(KL))
    return sek(n, '<div class="bl-gr">%s<div class="bl-karte vauf"><div class="bl-innen">%s%s<p class="bl-lead">%s</p>%s</div></div></div>' % (
        kachel(HAUPT, '(max-width:760px) 100vw, 34vw', 'bl-bild sw', '--i:1;'), KZ, TITEL, E(LEAD), zeilen), hell=False)
V.append(('Das Blatt', v07))


# 08 · Das Schild: wie das Eckschild an der Hausecke, eine schwarze Platte, deren Goldrahmen sich zieht; darin Glas und die vier Drinks.
def v08(n):
    rahmen = '<svg class="sc-rahmen" preserveAspectRatio="none" aria-hidden="true"><rect x="10" y="10" rx="10" pathLength="100"/></svg>'
    return sek(n, '%s<div class="sc vauf">%s<div class="sc-in">%s<div class="sc-liste">%s</div></div></div>' % (
        kopf_quer(), rahmen, kachel(HAUPT, '(max-width:760px) 100vw, 34vw', 'sc-bild'), ''.join(eintrag(j, 'sc-e') for j in range(4))))
V.append(('Das Schild', v08))


# 09 · Die Stufen: vier Gläser nebeneinander; beim Scrollen setzt sich jedes eine Stufe tiefer, wie die Stufen hinauf zur Empore.
def v09(n):
    sp = ''.join('<article class="st-s" style="--n:%d">%s%s</article>' % (j, kachel(BILD[j], '(max-width:760px) 100vw, 24vw', 'st-b'), eintrag(j, 'st-e')) for j in range(4))
    return sek(n, '%s<div class="st-gr" data-st>%s</div>' % (kopf_quer(), sp))
V.append(('Die Stufen', v09))


# 10 · Einer nach dem anderen: die Bühne bleibt stehen, beim Scrollen kommt Drink für Drink, Bild und Name gleiten nach oben aus und der nächste nach.
def v10(n):
    b = ''.join(kachel(k, '(max-width:760px) 100vw, 40vw', 'en-b' + (' an' if j == 0 else '')) for j, k in enumerate(BILD))
    z = ''.join('<div class="en-z%s"><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (' an' if j == 0 else '', E(t), E(s)) for j, (t, s) in enumerate(KL))
    striche = ''.join('<i class="%s"></i>' % ('an' if j == 0 else '') for j in range(4))
    return sek(n, '<div class="innen">%s</div><div class="en-pin" data-pin><div class="en-buehne"><div class="innen en-gr"><div class="en-bilder">%s</div><div class="en-txt"><div class="en-striche">%s</div><div class="en-zeilen">%s</div></div></div></div></div>' % (
        kopf_quer(), b, striche, z), innen=False)
V.append(('Einer nach dem anderen', v10))


# 11 · Im Licht: vier Gläser in einer Reihe auf Nacht; das Licht wandert beim Scrollen von links nach rechts, immer ein Glas steht hell.
def v11(n):
    sp = ''.join('<article class="li-s" style="--n:%d">%s%s</article>' % (j, kachel(BILD[j], '(max-width:760px) 100vw, 24vw', 'li-b'), eintrag(j, 'li-e')) for j in range(4))
    return sek(n, '%s<div class="li-gr" data-li>%s</div>' % (kopf_quer(), sp), hell=False)
V.append(('Im Licht', v11))


# 12 · Die Zeilen: vier lange Zeilen mit Goldlinie, links das Glas, in der Mitte der Name, rechts der Satz; Linie und Bild öffnen sich mit jeder Zeile.
def v12(n):
    z = ''.join('<div class="ze-z vauf" style="--n:%d"><i class="ze-l"></i>%s<h3 class="titel">%s</h3><p class="text">%s</p></div>' % (
        j, kachel(BILD[j], '(max-width:760px) 40vw, 16vw', 'ze-b'), E(t), E(s)) for j, (t, s) in enumerate(KL))
    return sek(n, '%s<div class="ze-liste">%s</div>' % (kopf_quer(), z))
V.append(('Die Zeilen', v12))


# 13 · Der Satz: je Drink steht der Satz, der ihn ausmacht, gross; darüber der Name als Etikett, darunter der Rest. Der Satz hebt sich aus einer Kante.
def v13(n):
    bl = ''.join('<div class="sa-b vauf" style="--n:%d"><span class="etikett">%s</span><p class="titel sa-gross"><span class="sa-m"><span>%s</span></span></p><p class="text">%s</p></div>' % (
        j, E(KL[j][0]), E(g), E(r)) for j, (g, r) in enumerate(SATZ))
    return sek(n, '<div class="sa-kopf">%s%s</div><div class="sa-gr">%s</div>' % (kopf(), kachel(HAUPT, '(max-width:760px) 100vw, 28vw', 'sa-bild sw', '--i:2;'), bl))
V.append(('Der Satz', v13))


# 14 · Vom Glas zur Liste: der Negroni füllt zuerst den ganzen Bildschirm und setzt sich beim Scrollen an seinen Platz neben die Liste.
def v14(n):
    return sek(n, '<div class="gl-pin" data-gl><div class="gl-buehne"><div class="innen gl-gr"><div class="gl-platz">%s</div><div class="gl-txt">%s<div class="gl-liste">%s</div></div></div></div></div>' % (
        kachel(HAUPT, '100vw', 'gl-bild'), kopf(), ''.join(eintrag(j, 'gl-e') for j in range(4))), innen=False)
V.append(('Vom Glas zur Liste', v14))


# 15 · Halb und halb: links reicht das Glas über die ganze Höhe bis an den Rand, rechts Creme mit Titel und Liste; das Bild läuft langsamer als die Seite.
def v15(n):
    return sek(n, '<div class="hh">%s<div class="hh-txt">%s<div class="hh-liste staffel">%s</div></div></div>' % (
        foto(HAUPT, '(max-width:760px) 100vw, 50vw', 'foto hh-bild'), kopf(), ''.join(eintrag(j, 'hh-e') for j in range(4))), innen=False)
V.append(('Halb und halb', v15))


# 16 · Die Etiketten: vier hohe Etiketten wie auf einer Flasche, mit feinem Doppelstrich, oben das Glas; sie legen sich aus einer leichten Schräge gerade.
def v16(n):
    et = ''.join('<article class="et-k" style="--n:%d;--r:%s"><div class="et-in">%s<i class="et-s"></i><h3 class="titel">%s</h3><i class="et-s"></i><p class="text">%s</p></div></article>' % (
        j, ['-2.5deg', '2deg', '-1.5deg', '2.5deg'][j], kachel(BILD[j], '(max-width:760px) 100vw, 22vw', 'et-b'), E(t), E(s)) for j, (t, s) in enumerate(KL))
    return sek(n, '%s<div class="et-gr vauf">%s</div>' % (kopf_quer(), et))
V.append(('Die Etiketten', v16))


# 17 · Die Vitrine: ein Schrank mit Goldrahmen und vier Fächern, wie die Vitrine unter dem Schriftzug; das Licht geht Fach für Fach an.
def v17(n):
    f = ''.join('<div class="vt-f" style="--n:%d"><div class="vt-bw">%s<i class="vt-dunkel"></i></div>%s</div>' % (
        j, kachel(BILD[j], '(max-width:760px) 50vw, 24vw', 'vt-b'), eintrag(j, 'vt-e')) for j in range(4))
    return sek(n, '%s<div class="vt vauf">%s</div>' % (kopf_quer(), f), hell=False)
V.append(('Die Vitrine', v17))


# 18 · Abgestellt: eine lange Goldlinie wie die Thekenkante; die vier Gläser werden darauf abgestellt, eins nach dem anderen, mit leichtem Federn.
def v18(n):
    g = ''.join('<article class="ab-g" style="--n:%d">%s</article>' % (j, kachel(BILD[j], '(max-width:760px) 45vw, 22vw', 'ab-b')) for j in range(4))
    return sek(n, '%s<div class="ab vauf"><div class="ab-reihe">%s</div><i class="ab-kante"></i><div class="ab-txt">%s</div></div>' % (
        kopf_quer(), g, ''.join(eintrag(j, 'ab-e') for j in range(4))))
V.append(('Abgestellt', v18))


# 19 · Die Initialen: N, P, M, O als grosse Goldlinien-Buchstaben, daneben Name und Satz; links Titel und Glas.
def v19(n):
    bl = ''.join('<div class="in-b" style="--n:%d"><span class="in-i" aria-hidden="true">%s</span>%s</div>' % (j, E(t[0]), eintrag(j, 'in-e')) for j, (t, s) in enumerate(KL))
    return sek(n, '<div class="in-gr"><div class="in-l">%s%s</div><div class="in-r vauf">%s</div></div>' % (
        kopf(), kachel(HAUPT, '(max-width:760px) 100vw, 34vw', 'in-bild sw', '--i:2;'), bl))
V.append(('Die Initialen', v19))


# 20 · Die Zeitung: Titel über die ganze Breite, darunter ein Doppelstrich, der sich von der Mitte aus zieht; vier Spalten mit feinen Linien, oben je ein Glas.
def v20(n):
    sp = ''.join('<article class="zt-s" style="--n:%d">%s%s</article>' % (j, kachel(BILD[j], '(max-width:760px) 100vw, 24vw', 'zt-b'), eintrag(j, 'zt-e')) for j in range(4))
    return sek(n, '<div class="zt vauf"><div class="zt-kopf">%s%s%s</div><i class="zt-strich"></i><div class="zt-gr">%s</div></div>' % (KZ, TITEL, lead(), sp))
V.append(('Die Zeitung', v20))


def seite(n):
    h = unter.drinks()
    if n:
        a = h.find('<section class="kap hell auf" id="klassiker">')
        b = h.find('</section>', a) + len('</section>')
        assert a > 0
        h = h[:a] + V[n - 1][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[j + 1, name] for j, (name, _) in enumerate(V)]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/v.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, len(V), E(liste[n][1]))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/v.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in range(len(V) + 1):
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00 …', len(V))
