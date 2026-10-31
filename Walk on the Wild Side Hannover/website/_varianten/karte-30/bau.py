# Walk on the Wild Side · Drinks-Seite, Abschnitt «Die einzige Karte» (id karte): 30 neue Darstellungen (30.10.2026).
# Robert zu den 20 ersten: «Das ist alles scheiße. Bitte nochmal komplett neu und 30 Vorschläge.» und «du kannst da kein Valentinstags-Schriftzug
# hinmachen, wenn daneben ein Bild von Weihnachten ist.» Daraus: Jedes Bild steht nur neben seinem eigenen Fest.
#   Valentinstag 2026: Leopard und Glas von der Karte (Ausschnitt, nie das ganze Plakat), Foto Momo und Rudi vom Februar 2026, neutrale Drinkfotos.
#   Weihnachten 2023: nur das Foto der Karte am Tisch, immer unter eigener Überschrift «Weihnachten 2023».
# 01–18 nur Valentinstag, 19–30 beide Feste streng getrennt. Texte: Absatz, Karte und Teller vom Valentins-Plakat, Namen vom Foto 2023.
# Jede Fassung eigene Anordnung und ein eigener bewegter Moment, nur transform. Das Hochschweben der Seite läuft mit.
# 00 = heutiger Stand. Wechsel mit ← →. Aufruf: python3 _varianten/karte-30/bau.py → 00.html … 30.html
import os, sys, json, html
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(HIER)
sys.path.insert(0, HIER)
import bau as B
import bilder
import unter

E = html.escape
ORD = '_varianten/karte-30'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('v.css', 'v.js', 'nav.js'))))
bilder.BILDER.update({
    'k30-leopard': ('valentin/leopard-2x.jpg', 'Der Leopard mit Herzen im Fell und ein Glas mit Kirsche, gezeichnet für die Valentinskarte 2026'),
    'k30-coupe': ('valentin/coupe-2x.jpg', 'Ein rosa Drink im Glas mit Kirsche und Schleife, gezeichnet für die Valentinskarte 2026'),
    'k30-paar': ('valentin/momo-rudi-2026.jpg', 'Momo und Rudi am Abend in der Bar, Februar 2026'),
    'k30-weihnacht': ('ig/2023-12-07_walkonthewildside_hannover_C0j1thbsh_y-1.jpg', 'Momos Signature Drinks auf einer Karte am Tisch, daneben ein Windlicht, Weihnachten 2023'),
})

# ---- Texte (nur Belegtes)
KZ_V = B.kz('Valentinstag 2026', 'Eine Karte im Jahr', 0)
TITEL_V = B.h2(['Die einzige Karte.'])
S1 = 'Einmal im Jahr gibt es doch eine Karte: zum Valentinstag, zusammen mit Rudi von Culinarium.'
S2 = '2026 hiess sie «Drunk in Love», vier Drinks zu je zwölf Euro, dazu Teller zum Teilen.'
VTEXT = S1 + ' ' + S2
HINWEIS = 'Preise vom Plakat zum 14. Februar 2026. An allen anderen Abenden gibt es keine Karte.'
KARTE = [('Frensh 26', 'Gin · Bergamotte · Nori · Schaumwein'), ('Whey Bramble', 'Gin · Lemon Shrub · Vetiver · Whey Berry Soda'),
         ('Pink Lady', 'Kakaobutter-Fat-Washed Rum · Himbeerpüree · Agave · Limette'),
         ('Karamella', 'Havana 7 Jahre · Portwein · Johannisbeere · Karamell · schwarze Walnüsse · Limette')]
TELLER = [('Bergamotten Schaumwein', 'Auster · Granita', '15'), ('Sauerteigbrot', 'Butter · Maldon', '6'),
          ('Kichererbsen Hummus', 'geräucherte Paprika · Olivenöl', '8'), ('Stracciatella Creme', 'Dillöl · dunkle Trauben · Basilikum Pesto', '8'),
          ('Rosa gegarte Entenbrust', 'Teriyaki Jus · Pak Choi', '12'), ('Boeuf Bourguignon', 'Kartoffel Mousseline · eingelegte Paprika · Schmand', '12'),
          ('Geschmorter Hokkaido', 'Süsskartoffel Honig · Kartoffel Mousseline · Wirsing', '11'), ('Dunkle Schokolade', 'Olivenöl · Maldon', '8')]
CUPID = 'Cupid’s Signature Drinks'
V_ETI = 'Valentinstag 2026 · mit Rudi von Culinarium'
V_H = 'Drunk in Love.'
V_P = 'Vier Drinks zu je zwölf Euro, dazu Teller zum Teilen. Gemacht zusammen mit Rudi von Culinarium.'
W_ETI = 'Weihnachten 2023'
W_H = 'Momos Signature Drinks.'
W_P = 'Zum Weihnachtsfest 2023 standen Momos erste Signature Drinks auf einem Blatt. Daneben am Tisch: Oma’s Glühwein für fünf Euro.'
SIG23 = ['Linden Mule', 'Sakura', 'Mary Bramble', 'Ambré', 'Clean Pornstar', 'Zauberwald']
KZ_Z = B.kz('Zum Fest', 'Sonst keine Karte', 0)
TITEL_Z = B.h2(['Wenn es doch', 'eine Karte gibt.'])
ZTEXT = 'An allen anderen Abenden gibt es keine Karte. Da sagst du Momo, was du magst.'
KNOPF = B.knopf('Platz reservieren', 'besuch.html#reservieren', 'rot')


# ---- Bausteine
def p(t, cls='text', i=1):
    return '<p class="%s sw" style="--i:%d">%s</p>' % (cls, i, E(t))


def eti(t, cls=''):
    return '<span class="etikett %s">%s</span>' % (cls, E(t))


def knoepfe(i=2):
    return '<div class="knoepfe sw" style="--i:%d">%s</div>' % (i, KNOPF)


def klein(t=HINWEIS):
    return '<small class="k-hinweis">%s</small>' % E(t)


def bild(k, sizes, cls, stil='', attr=''):
    """Eigenes Bild ohne die Hebe-Bewegung der Seite (die Fassung hat ihre eigene)."""
    d = bilder.mache(k)
    return '<figure class="%s" style="--lq:url(%s);%s"%s>%s</figure>' % (cls, d['lq'], stil, attr, B.img_tag(k, sizes))


def leo(cls='', attr='', sizes='(max-width:760px) 80vw, 420px'):
    return bild('k30-leopard', sizes, 'illu leo ' + cls, attr=attr)


def coupe(cls='', attr=''):
    return bild('k30-coupe', '(max-width:760px) 50vw, 240px', 'illu cp ' + cls, attr=attr)


def drinks(cls='dl', preis=True):
    return '<div class="%s">%s</div>' % (cls, ''.join('<div class="d" style="--n:%d"><b>%s</b>%s<p>%s</p></div>' % (
        n, E(t), '<span>12 €</span>' if preis else '', E(z)) for n, (t, z) in enumerate(KARTE)))


def teller(cls='tl'):
    return '<div class="%s">%s</div>' % (cls, ''.join('<div class="d"><b>%s</b><span>%s €</span><p>%s</p></div>' % (E(t), pr, E(z)) for t, z, pr in TELLER))


def sig(cls='sg'):
    return '<div class="%s">%s</div>' % (cls, ''.join('<b style="--n:%d">%s</b>' % (n, E(t)) for n, t in enumerate(SIG23)))


def kopf_v(text=True):
    return KZ_V + TITEL_V + (p(VTEXT) if text else '')


def kopf_z():
    return KZ_Z + TITEL_Z + p(ZTEXT)


def vblock(liste=True, cls='vb'):
    return '<div class="%s">%s<h3 class="titel">%s</h3>%s%s%s</div>' % (cls, eti(V_ETI), E(V_H), '<p class="text">%s</p>' % E(V_P),
                                                                      drinks() if liste else '', klein('Preise vom Plakat zum 14. Februar 2026.'))


def wblock(cls='wb'):
    return '<div class="%s">%s<h3 class="titel">%s</h3><p class="text">%s</p>%s</div>' % (cls, eti(W_ETI), E(W_H), E(W_P), sig())


def foto_w(cls='', attr=''):
    return bild('k30-weihnacht', '(max-width:760px) 100vw, 40vw', 'vfig fw ' + cls, attr=attr)


def foto_p(cls='', attr='', sizes='(max-width:760px) 100vw, 60vw'):
    return bild('k30-paar', sizes, 'vfig fp ' + cls, attr=attr)


def sek(n, inhalt, cls='', innen=True):
    return '<section class="kap auf kx v%02d %s" id="karte" data-k="%d">%s</section>' % (n, cls, n, '<div class="innen">%s</div>' % inhalt if innen else inhalt)


V = []


def fassung(name):
    def reg(f):
        V.append((name, f))
        return f
    return reg


# ================= 01–18: nur Valentinstag

# 01 · Die ganze Fläche ist Rosa wie die Karte, der Titel gross in Rot; der Leopard kommt von rechts herein und sitzt auf der Unterkante.
@fassung('Rosa Wand')
def v01(n):
    return sek(n, '<div class="innen rw"><div class="rw-l">%s%s</div>%s</div>' % (kopf_v(), drinks('dl rw-dl'), leo('rw-leo', ' data-m')), 'rosa voll', False)


# 02 · Momo und Rudi gross im Querformat, das Bild zieht sich beim Scrollen zurecht; darunter die vier Drinks in einer Reihe.
@fassung('Die zwei Gastgeber')
def v02(n):
    return sek(n, '<div class="gg-o">%s<div>%s%s</div></div>%s%s' % (foto_p('gg-f', ' data-zoom'), kopf_v(), knoepfe(), drinks('dl gg-dl staffel'), klein()))


# 03 · Die Karte neu gesetzt wie das Original: Rosa, rote Schrift, unten der Leopard. Sie richtet sich beim Scrollen auf.
@fassung('Die Karte nachgesetzt')
def v03(n):
    blatt = '<div class="kn-blatt" data-dreh="7,-2"><p class="kn-eti">Wild Side x Rudi in Love</p><p class="kn-titel"><span>Drunk in</span><em>Love.</em></p><p class="kn-cupid">%s</p>%s%s</div>' % (
        E(CUPID), drinks('dl kn-dl'), leo('kn-leo'))
    return sek(n, '<div class="kn"><div>%s%s%s</div>%s</div>' % (kopf_v(), knoepfe(), klein(), blatt))


# 04 · Zwei Blätter, Drinks und Teller. Sie liegen erst übereinander und gehen dann auseinander.
@fassung('Drinks und Teller')
def v04(n):
    a = '<div class="dt-b dt-a" data-m><p class="kn-titel"><span>Drunk in</span><em>Love.</em></p><p class="kn-cupid">%s</p>%s%s</div>' % (E(CUPID), drinks('dl kn-dl'), leo('dt-leo'))
    b = '<div class="dt-b dt-t" data-m><p class="kn-titel"><span>Dishes in</span><em>Love.</em></p><p class="kn-cupid">Sharing Dishes for Love Birds &amp; Friends</p>%s</div>' % teller('tl kn-dl')
    return sek(n, '<div class="dt-o"><div>%s%s</div><div>%s%s%s</div></div><div class="dt">%s%s</div>' % (KZ_V, TITEL_V, p(VTEXT), knoepfe(), klein(), a, b))


# 05 · Auf Rosa vier grosse Namen untereinander, jeder schiebt sich von rechts herein; links bleibt das gezeichnete Glas stehen.
@fassung('Die Namen auf Rosa')
def v05(n):
    reihen = ''.join('<div class="nr-z" data-m style="--n:%d"><b>%s</b><p>%s</p><span>12 €</span></div>' % (j, E(t), E(z)) for j, (t, z) in enumerate(KARTE))
    return sek(n, '<div class="innen nr"><div class="nr-l"><div class="nr-kleb">%s%s%s%s</div></div><div class="nr-r">%s</div></div>' % (
        coupe('nr-cp'), kopf_v(), knoepfe(), '', reihen), 'rosa voll', False)


# 06 · Wand an Wand: links das rosa Feld mit dem Leoparden, rechts die Nacht mit Text und Karte. Der Leopard steigt von unten in sein Feld.
@fassung('Leopard links')
def v06(n):
    return sek(n, '<div class="ll"><div class="ll-r rosa" data-m>%s</div><div class="ll-t">%s%s%s%s</div></div>' % (
        leo('ll-leo'), kopf_v(), drinks('dl ll-dl'), knoepfe(), klein()), 'voll ohne-rand', False)


# 07 · Das Datum quer über die Seite, es gleitet beim Scrollen seitwärts; darunter Text und Karte nebeneinander.
@fassung('Der 14. Februar')
def v07(n):
    return sek(n, '<div class="dm-datum" data-px="0.18" aria-hidden="true">14.02.</div><div class="innen dm"><div>%s%s%s</div><div>%s%s</div></div>' % (
        kopf_v(), knoepfe(), '', drinks('dl dm-dl'), klein()), 'rosa voll', False)


# 08 · Drei Felder Wand an Wand: Momo und Rudi, der Leopard, ein Drink. Das mittlere steigt zuerst.
@fassung('Drei Felder')
def v08(n):
    band = '<div class="df">%s<div class="df-m rosa" data-m>%s</div>%s</div>' % (
        foto_p('df-f', ' data-m', '(max-width:760px) 100vw, 34vw'), leo('df-leo'), bild('glas-coupe', '(max-width:760px) 100vw, 34vw', 'vfig df-f df-3', attr=' data-m'))
    return sek(n, '<div class="df-o"><div>%s%s</div><div>%s%s</div></div>%s%s%s' % (KZ_V, TITEL_V, p(VTEXT), knoepfe(), band, drinks('dl df-dl staffel'), klein()))


# 09 · Auf Rot, Schrift in Creme. Das gezeichnete Glas schwingt einmal aus, wenn es ins Bild kommt.
@fassung('Auf Rot')
def v09(n):
    return sek(n, '<div class="innen ar"><div class="ar-l"><div class="ar-feld rosa">%s</div></div><div>%s%s%s%s</div></div>' % (
        coupe('ar-cp', ' data-m'), kopf_v(), drinks('dl ar-dl'), knoepfe(), klein()), 'rotgrund voll', False)


# 10 · Der Leopard bleibt links stehen und wächst ein wenig, rechts läuft der Abend vorbei: Text, Drinks, Teller.
@fassung('Der Leopard bleibt stehen')
def v10(n):
    return sek(n, '<div class="lb" data-pin><div class="lb-l"><div class="lb-kleb rosa">%s</div></div><div class="lb-r">%s%s<h3 class="titel lb-h">%s</h3>%s<h3 class="titel lb-h">Dishes in Love.</h3>%s%s</div></div>' % (
        leo('lb-leo', ' data-skala'), kopf_v(), knoepfe(), E(CUPID), drinks('dl lb-dl'), teller('tl lb-dl'), klein()))


# 11 · Eine Einladung: die Karte als rosa Blatt mit roter Doppellinie auf rotem Grund. Sie dreht sich gerade und wird gross.
@fassung('Die Einladung')
def v11(n):
    karte = '<div class="ei-k" data-m><p class="kn-eti">Wild Side x Rudi in Love</p>%s<h3 class="titel">%s</h3><p class="kn-cupid">%s</p>%s%s</div>' % (
        coupe('ei-cp'), E(V_H), E(CUPID), drinks('dl ei-dl', False), '<p class="ei-preis">Jeder Drink 12 €</p>')
    return sek(n, '<div class="innen ei"><div class="ei-l">%s%s%s</div>%s</div>' % (kopf_v(), knoepfe(), klein(), karte), 'rotgrund voll', False)


# 12 · Drei Spalten auf Nacht: Drinks, der Leopard, Teller. Die äusseren rücken beim Auftritt an die Mitte.
@fassung('Drei Spalten')
def v12(n):
    return sek(n, '<div class="ds-o">%s%s%s</div><div class="ds"><div class="ds-s" data-m>%s%s</div><div class="ds-m rosa">%s</div><div class="ds-s ds-re" data-m>%s%s</div></div>%s' % (
        KZ_V, TITEL_V, p(VTEXT), eti(CUPID), drinks('dl ds-dl'), leo('ds-leo'), eti('Sharing Dishes for Love Birds & Friends'), teller('tl ds-dl'),
        '<div class="ds-u">%s%s</div>' % (knoepfe(), klein())))


# 13 · Ein Querband: beim Scrollen fährt der Abend seitwärts vorbei, Feld für Feld in Rosa und Rot.
@fassung('Querband')
def v13(n):
    felder = ['<div class="qb-f qb-t">%s%s%s%s</div>' % (KZ_V, TITEL_V, p(VTEXT), knoepfe())]
    for j, (t, z) in enumerate(KARTE):
        felder.append('<div class="qb-f qb-d %s"><span class="etikett">%s</span><b>%s</b><p>%s</p><i>12 €</i></div>' % ('rosa' if j % 2 == 0 else 'rotgrund', E(CUPID), E(t), E(z)))
    felder.append('<div class="qb-f qb-l rosa">%s</div>' % leo('qb-leo'))
    felder.append('<div class="qb-f qb-p">%s</div>' % foto_p('qb-foto', '', '(max-width:760px) 100vw, 46vw'))
    return sek(n, '<div class="qb" data-quer><div class="qb-kleb"><div class="qb-zug">%s</div></div></div>' % ''.join(felder), 'voll ohne-rand', False)


# 14 · «Drunk» und «in Love.» riesig, die beiden Worte laufen beim Scrollen gegeneinander; dazwischen Momo und Rudi.
@fassung('Drunk / in Love')
def v14(n):
    return sek(n, '<p class="dl2-w dl2-a" data-px="-0.16" aria-hidden="true">Drunk</p><div class="innen dl2-m">%s<div>%s%s%s%s</div></div><p class="dl2-w dl2-b" data-px="0.16" aria-hidden="true">in Love.</p><div class="innen">%s%s</div>' % (
        foto_p('dl2-f'), KZ_V, TITEL_V, p(VTEXT), knoepfe(), drinks('dl dl2-dl staffel'), klein()), 'creme voll', False)


# 15 · An der Bar: Momo beim Eingiessen links bis an den Rand, rechts die rosa Spalte mit der Karte. Die Spalte steigt schneller als das Bild.
@fassung('An der Bar')
def v15(n):
    return sek(n, '<div class="ab">%s<div class="ab-r rosa"><div class="ab-in" data-par="0.1">%s%s%s%s</div></div></div>' % (
        bild('momo-giesst', '(max-width:760px) 100vw, 55vw', 'vfig ab-f'), kopf_v(), drinks('dl ab-dl'), knoepfe(), klein()), 'voll ohne-rand', False)


# 16 · Der Leopard in der Mitte, links und rechts je zwei Drinks. Sie rücken beim Auftritt an ihn heran.
@fassung('Leopard in der Mitte')
def v16(n):
    l = ''.join('<div class="d"><b>%s</b><span>12 €</span><p>%s</p></div>' % (E(t), E(z)) for t, z in KARTE[:2])
    r = ''.join('<div class="d"><b>%s</b><span>12 €</span><p>%s</p></div>' % (E(t), E(z)) for t, z in KARTE[2:])
    return sek(n, '<div class="innen lm"><div class="lm-o">%s%s%s</div><div class="lm-b"><div class="dl lm-s lm-l" data-m>%s</div>%s<div class="dl lm-s lm-r" data-m>%s</div></div><div class="lm-u">%s%s</div></div>' % (
        KZ_V, TITEL_V, p(VTEXT), l, leo('lm-leo'), r, knoepfe(), klein()), 'rosa voll', False)


# 17 · Ein rosa Streifen quer durch die Nacht, Titel und Leopard fahren von beiden Seiten in ihn hinein; darunter die Karte mit Goldlinien.
@fassung('Rosa Streifen')
def v17(n):
    return sek(n, '<div class="rs rosa" data-m><div class="innen rs-i"><div>%s<p class="rs-titel titel">Drunk in <em>Love.</em></p></div>%s</div></div><div class="innen rs-u"><div>%s%s%s</div>%s</div>' % (
        KZ_V, leo('rs-leo'), p(VTEXT), knoepfe(), klein(), drinks('dl rs-dl')), 'voll', False)


# 18 · Der Satz ist die Hauptsache: der Absatz in grosser Schrift, «Drunk in Love» in Rot; Zeile für Zeile steigt er auf.
@fassung('Der Satz')
def v18(n):
    zeilen = ['Einmal im Jahr gibt es', 'doch eine Karte: zum', 'Valentinstag, mit Rudi', 'von Culinarium. 2026', 'hiess sie <em>Drunk in Love.</em>']
    satz = '<p class="sz-satz titel">%s</p>' % ''.join('<span class="sz-z" data-m style="--n:%d"><span>%s</span></span>' % (j, z) for j, z in enumerate(zeilen))
    return sek(n, '<div class="sz">%s%s</div><div class="sz-u">%s<div>%s%s%s</div></div>' % (KZ_V, satz, coupe('sz-cp'), drinks('dl sz-dl'), knoepfe(), klein()))


# ================= 19–30: beide Feste, jedes mit eigenem Bild unter eigener Überschrift

# 19 · Zwei Hälften Wand an Wand: links Rosa mit dem Leoparden, rechts die Nacht mit der Weihnachtskarte. Sie kommen von ihren Seiten herein.
@fassung('Zwei Hälften')
def v19(n):
    return sek(n, '<div class="innen zh-o">%s%s%s</div><div class="zh"><div class="zh-v rosa" data-m>%s%s</div><div class="zh-w" data-m>%s%s</div></div>' % (
        KZ_Z, TITEL_Z, p(ZTEXT), vblock(), leo('zh-leo'), foto_w('zh-f'), wblock()), 'voll ohne-unten', False)


# 20 · Erst Dezember, dann Februar: zwei Reihen im Zickzack, jedes Bild neben seinem eigenen Text. Die Bilder gleiten gegeneinander.
@fassung('Winter, dann Februar')
def v20(n):
    return sek(n, '<div class="wf-o">%s%s%s</div><div class="wf-z">%s%s</div><div class="wf-z wf-z2">%s<div class="wf-r rosa" data-par="-0.08">%s</div></div>' % (
        KZ_Z, TITEL_Z, p(ZTEXT), foto_w('wf-f', ' data-par="0.08"'), wblock(), vblock(), leo('wf-leo')))


# 21 · Zwei Blätter auf dem Tisch: das Weihnachtsblatt in Creme mit dem Foto, das Valentinsblatt in Rosa mit dem Leoparden. Beide legen sich gerade.
@fassung('Zwei Blätter')
def v21(n):
    w = '<div class="zb-b zb-w" data-m>%s%s</div>' % (foto_w('zb-f'), wblock('wb zb-t'))
    v = '<div class="zb-b zb-v rosa" data-m>%s%s</div>' % (vblock(True, 'vb zb-t'), leo('zb-leo'))
    return sek(n, '<div class="zb-o"><div>%s%s</div><div>%s%s</div></div><div class="zb">%s%s</div>' % (KZ_Z, TITEL_Z, p(ZTEXT), knoepfe(), w, v))


# 22 · Eine Goldlinie mit zwei Haltepunkten, Dezember 2023 und Februar 2026. Die Linie zieht sich beim Auftritt von links nach rechts.
@fassung('Die Linie')
def v22(n):
    return sek(n, '<div class="li-o">%s%s%s</div><div class="li"><i class="li-strich" data-m></i><div class="li-p"><span class="li-dat titel">Dezember 2023</span>%s%s</div><div class="li-p"><span class="li-dat titel">Februar 2026</span><div class="li-rosa rosa">%s</div>%s</div></div>' % (
        KZ_Z, TITEL_Z, p(ZTEXT), foto_w('li-f'), wblock(), leo('li-leo'), vblock()))


# 23 · Das Jahr bleibt links stehen und wechselt beim Scrollen von 2023 auf 2026; rechts erst Weihnachten, dann Valentinstag.
@fassung('Das Jahr bleibt stehen')
def v23(n):
    jahr = '<div class="jb-l"><div class="jb-kleb">%s%s<div class="jb-fenster" data-jahr><div class="jb-zug"><b class="titel">2023</b><b class="titel">2026</b></div></div></div></div>' % (KZ_Z, TITEL_Z)
    return sek(n, '<div class="jb" data-pin>%s<div class="jb-r">%s<div class="jb-teil">%s%s</div><div class="jb-teil">%s%s</div>%s</div></div>' % (
        jahr, p(ZTEXT), foto_w('jb-f'), wblock(), '<div class="jb-rosa rosa">%s</div>' % leo('jb-leo'), vblock(), knoepfe()))


# 24 · Der Valentinstag gross als rosa Wand, Weihnachten 2023 darunter als eigenes dunkles Band, dessen Inhalt von unten nachrückt.
@fassung('Februar gross, Dezember danach')
def v24(n):
    return sek(n, '<div class="innen fg">%s<div class="fg-l">%s%s%s%s</div></div><div class="fg-w"><div class="innen fg-wi" data-m>%s%s</div></div>' % (
        leo('fg-leo'), kopf_v(), drinks('dl fg-dl'), knoepfe(), klein(), foto_w('fg-f'), wblock('wb fg-t')), 'rosa voll ohne-unten', False)


# 25 · Zwei grosse Abzüge nebeneinander, das Weihnachtsfoto und die rosa Zeichnung, beide kippen beim Auftritt gerade; darunter je die Karte.
@fassung('Zwei Abzüge')
def v25(n):
    return sek(n, '<div class="az-o">%s%s%s</div><div class="az"><div class="az-s"><div class="az-bild" data-m>%s</div>%s</div><div class="az-s"><div class="az-bild az-r rosa" data-m>%s</div>%s</div></div>' % (
        KZ_Z, TITEL_Z, p(ZTEXT), foto_w('az-f'), wblock(), leo('az-leo'), vblock()))


# 26 · Vier Felder Wand an Wand über Kreuz: Leopard und Valentinskarte oben, Weihnachtskarte und Foto unten. Sie setzen nacheinander auf.
@fassung('Vier Felder')
def v26(n):
    return sek(n, '<div class="innen vf-o">%s%s%s</div><div class="vf"><div class="vf-f rosa" data-m style="--n:0">%s</div><div class="vf-f rotgrund" data-m style="--n:1">%s</div><div class="vf-f vf-n" data-m style="--n:2">%s</div><div class="vf-f vf-b" data-m style="--n:3">%s</div></div>' % (
        KZ_Z, TITEL_Z, p(ZTEXT), leo('vf-leo'), vblock(), wblock(), foto_w('vf-foto')), 'voll ohne-unten', False)


# 27 · Zwei Spalten versetzt: oben je ein Bild im Hochformat (Weihnachtskarte; ein rosa Drink im Kerzenlicht), darunter die Karte. Die Spalten steigen verschieden schnell.
@fassung('Zwei Spalten')
def v27(n):
    return sek(n, '<div class="zs-o"><div>%s%s</div><div>%s%s</div></div><div class="zs"><div class="zs-s" data-par="0.05">%s%s</div><div class="zs-s" data-par="-0.05">%s%s</div></div>' % (
        KZ_Z, TITEL_Z, p(ZTEXT), knoepfe(), foto_w('zs-f'), wblock(), bild('wf-pink', '(max-width:760px) 100vw, 46vw', 'vfig zs-f'), vblock()))


# 28 · Eine Bühne, die wechselt: erst Weihnachten im Kerzenlicht, beim Scrollen geht es nach links hinaus, danach kommt der rosa Valentinstag von rechts herein.
@fassung('Die Bühne wechselt')
def v28(n):
    a = '<div class="bw-s bw-a"><div class="innen bw-i">%s<div>%s%s%s</div></div></div>' % (foto_w('bw-f'), KZ_Z, TITEL_Z, wblock())
    b = '<div class="bw-s bw-b rosa"><div class="innen bw-i">%s%s</div></div>' % (vblock(), leo('bw-leo'))
    return sek(n, '<div class="bw" data-buehne><div class="bw-kleb">%s%s</div></div>' % (a, b), 'voll ohne-rand', False)


# 29 · Zwei Bänder randlos übereinander, Nacht und Rosa, jedes mit Bild und Karte nebeneinander. Sie fahren von entgegengesetzten Seiten ein.
@fassung('Zwei Bänder')
def v29(n):
    return sek(n, '<div class="innen zb2-o"><div>%s%s</div><div>%s%s</div></div><div class="zb2 zb2-w" data-m><div class="innen zb2-i">%s%s</div></div><div class="zb2 zb2-v rosa" data-m><div class="innen zb2-i">%s%s</div></div>' % (
        KZ_Z, TITEL_Z, p(ZTEXT), knoepfe(), foto_w('zb2-f'), wblock(), vblock(), leo('zb2-leo')), 'voll ohne-unten', False)


# 30 · Der Valentinstag mit Momo und Rudi, Drinks und Tellern; darunter, durch eine Goldlinie getrennt, der Rückblick auf Weihnachten 2023.
@fassung('Mit Rückblick')
def v30(n):
    return sek(n, '<div class="rb">%s<div>%s%s%s</div></div><div class="rb-k"><div>%s%s</div><div>%s%s</div></div><div class="rb-w">%s%s</div>' % (
        foto_p('rb-f', ' data-zoom'), kopf_v(), knoepfe(), klein(), eti(CUPID), drinks('dl rb-dl'), eti('Sharing Dishes for Love Birds & Friends'), teller('tl rb-dl'),
        foto_w('rb-wf'), wblock()))


def seite(n):
    h = unter.drinks()
    if n:
        a = h.rfind('<section', 0, h.find('id="karte"'))
        b = h.find('</section>', a) + len('</section>')
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
