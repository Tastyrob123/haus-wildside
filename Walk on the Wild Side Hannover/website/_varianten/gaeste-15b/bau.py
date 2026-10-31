# Walk on the Wild Side · Programm-Seite, Abschnitt «Gäste hinterm Tresen · Jemand anderes am Shaker.» (id="gaeste"): 15 weitere Darstellungen, Nummern 16–30 (30.10.2026).
# Robert zu gaeste-15: «Nee, bitte 15 weitere Fassungen.» Keine Darstellung und keine Bewegung aus gaeste-15 oder session-15 wiederholt. 00 = heutiger Stand.
# Texte Wort für Wort aus unter.programm() (geprüft in gaeste-15/bau.py), nur die echten Fotos. Bewegung nur über transform und opacity, ein Scroll-Takt in h.js.
# Aufruf: python3 _varianten/gaeste-15b/bau.py → 00.html, 16.html … 30.html
import os, sys, json, html, importlib.util
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_spec = importlib.util.spec_from_file_location('g15', os.path.join(HIER, '_varianten', 'gaeste-15', 'bau.py'))
G = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(G)   # Texte, Prüfung, Kopf aus gaeste-15
B, unter, mache = G.B, G.unter, G.mache
os.chdir(HIER)

E = html.escape
ORD = '_varianten/gaeste-15b'
VER = str(int(max(os.path.getmtime(os.path.join(ORD, f)) for f in ('h.css', 'h.js', 'nav.js'))))
GAESTE, TEXT, STADT = G.GAESTE, G.TEXT, G.STADT
MONAT = {'03': 'März', '04': 'April', '05': 'Mai', '10': 'Oktober'}
ADRESSE = 'Haasemannstr. 13 · 30449 Hannover'        # vom Plakat der Bar


def kopf(cls=''):
    return '<div class="hq-kopf %s"><div class="hq-kopf-l">%s%s<p class="text sw" style="--i:1">%s</p></div></div>' % (
        cls, B.kz('Gäste hinterm Tresen', 'Gastschichten', 0), B.h2(['Jemand anderes', 'am Shaker.']), E(TEXT))


def fo(k, sizes, cls='', stil='', extra=''):
    return '<figure class="hf %s" style="--lq:url(%s);%s"%s>%s</figure>' % (cls, mache(k)['lq'], stil, extra, B.img_tag(k, sizes))


def satz(d, t, s, cls='h-satz'):
    return '<div class="%s"><span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p></div>' % (cls, E(d), E(t), E(s))


def src(k, b=960):
    return 'assets/bild/%s?v=%s' % ([f for w, f in mache(k)['stufen'] if w >= b][0], B.V)


def sek(n, inner, innen=True):
    i = '<div class="innen">%s</div>' % inner if innen else inner
    return '<section class="kap auf hq h%02d" id="gaeste" data-g="%d">%s</section>' % (n, n, i)


V = []


# 16 · Der Bon: rechts druckt die Kasse einen langen Bon, Kopf mit Name und Adresse der Bar, darunter je Gastschicht ein Posten
# mit kleinem Bild. Der Bon schiebt sich beim Auftritt langsam aus dem Schlitz nach unten.
def v16(n):
    p = ''.join('<div class="b16-z">%s<div><p class="b16-dat">%s</p><p class="b16-name">%s</p><p class="b16-s">%s</p></div></div>' % (
        fo(k, '(max-width:760px) 18vw, 6vw'), E(d), E(t.upper()), E(s)) for k, d, t, s in GAESTE)
    bon = '<div class="b16-kasse"><i class="b16-schlitz"></i><div class="b16-fenster"><div class="b16-bon"><p class="b16-kopf">WALK ON THE WILD SIDE<br><span>%s</span></p><p class="b16-strich">GASTSCHICHTEN 2024</p>%s<p class="b16-strich">5 POSTEN</p></div></div></div>' % (E(ADRESSE.upper()), p)
    return sek(n, '<div class="b16-raster">%s<div class="vauf b16-ort">%s</div></div>' % (kopf(), bon))
V.append((16, 'Der Bon', v16))


# 17 · Aus Streifen: jedes Porträt ist in sechs senkrechte Streifen geschnitten, die von oben und unten abwechselnd kommen
# und sich zum Bild zusammensetzen. Fünf Bilder in einer Reihe, eins nach dem anderen.
def v17(n):
    def bild(j, k):
        st = ''.join('<i style="--s:%d;background-image:url(%s);background-position:%.1f%% 50%%"></i>' % (i, src(k), i * 20) for i in range(6))
        return '<div class="s17-bild" style="--n:%d;--lq:url(%s)">%s</div>' % (j, mache(k)['lq'], st)
    p = ''.join('<article class="s17-p" style="--n:%d">%s%s</article>' % (j, bild(j, k), satz(d, t, s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="s17-reihe vauf">%s</div>' % p)
V.append((17, 'Aus Streifen', v17))


# 18 · Die Zeitungsseite: eine cremefarbene Seite wie das Feuilleton, Kopfzeile, ein Aufmacher mit grossem Bild (Musa)
# und vier schmale Spalten. Erst ziehen die Linien der Seite, dann füllen sich die Spalten von links.
def v18(n):
    k, d, t, s = GAESTE[0]
    auf = '<article class="z18-auf">%s<div><span class="z18-dat">%s</span><h3 class="titel">%s</h3><p>%s</p></div></article>' % (fo(k, '(max-width:760px) 90vw, 40vw'), E(d), E(t), E(s))
    sp = ''.join('<article class="z18-sp" style="--n:%d">%s<span class="z18-dat">%s</span><h3 class="titel">%s</h3><p>%s</p></article>' % (
        j, fo(k, '(max-width:760px) 44vw, 14vw'), E(d), E(t), E(s)) for j, (k, d, t, s) in enumerate(GAESTE[1:]))
    return sek(n, kopf() + '<div class="z18-seite vauf"><p class="z18-kopf"><span>Walk on the Wild Side</span><b class="titel">Gäste hinterm Tresen</b><span>2024</span></p><i class="z18-linie"></i>%s<i class="z18-linie"></i><div class="z18-spalten">%s</div></div>' % (auf, sp))
V.append((18, 'Die Zeitungsseite', v18))


# 19 · Im Wechsel: je Gast eine Zeile, grosses Bild einmal links, einmal rechts, gegenüber Datum in grosser Schrift, Name und Satz.
# Das Bild kommt aus der Nähe (1,15 auf 1) in seinem Rahmen zur Ruhe, der Text steigt nach.
def v19(n):
    z = ''.join('<article class="w19-z %s vauf"><div class="w19-bild">%s</div><div class="w19-t"><p class="w19-dat titel">%s</p><h3 class="titel">%s</h3><p>%s</p></div></article>' % (
        'rechts' if j % 2 else '', fo(k, '(max-width:760px) 90vw, 40vw'), E(d), E(t), E(s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + z)
V.append((19, 'Im Wechsel', v19))


# 20 · Fünf Fenster bei Nacht: eine dunkle Fassade mit fünf Fenstern, Sprossen in Gold. Hinter jedem steht ein Gast,
# beim Auftritt geht in einem Fenster nach dem anderen das Licht an.
def v20(n):
    f = ''.join('<article class="f20-f" style="--n:%d"><div class="f20-rahmen">%s<i class="f20-sprosse"></i></div>%s</article>' % (
        j, fo(k, '(max-width:760px) 44vw, 18vw'), satz(d, t, s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="f20-fassade vauf"><div class="f20-reihe">%s</div></div>' % f)
V.append((20, 'Fünf Fenster bei Nacht', v20))


# 21 · Das Mosaik: Bilder in verschiedenen Grössen dicht aneinander, Musa gross, die anderen hoch, quer und klein,
# dazu ein Feld nur mit Schrift. Die Felder setzen sich von der Mitte her nacheinander ins Raster.
def v21(n):
    fl = ['a', 'b', 'c', 'd', 'e']
    t = ''.join('<article class="m21-f m21-%s" style="--n:%d">%s<div class="m21-band"><span>%s</span><b class="titel">%s</b></div></article>' % (
        f, j, fo(k, '(max-width:760px) 90vw, 50vw'), E(d), E(t_)) for j, ((k, d, t_, s), f) in enumerate(zip(GAESTE, fl)))
    return sek(n, kopf() + '<div class="m21-raster vauf">%s<div class="m21-f m21-schrift" style="--n:5"><p class="titel">Fünf Gastschichten aus dem Jahr 2024.</p></div></div>' % t)
V.append((21, 'Das Mosaik', v21))


# 22 · Die Kamerafahrt: die Bühne steht, alle fünf stehen klein nebeneinander. Beim Scrollen fährt die Kamera an einen nach dem anderen
# heran und wieder zurück; darunter steht, wer gerade im Bild ist.
def v22(n):
    p = ''.join('<div class="k22-p">%s</div>' % fo(k, '(max-width:760px) 60vw, 40vw') for k, d, t, s in GAESTE)
    tx = ''.join('<div class="k22-t" style="--n:%d"><span class="etikett">%s</span><p class="k22-name titel">%s</p><p>%s</p></div>' % (j, E(d), E(t), E(s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, '<div class="innen">%s</div><div class="k22-pin" data-pin><div class="k22-buehne"><div class="k22-fenster"><div class="k22-gruppe">%s</div></div><div class="innen k22-texte">%s</div></div></div>' % (kopf(), p, tx), innen=False)
V.append((22, 'Die Kamerafahrt', v22))


# 23 · Verdeckte Karten: fünf Karten liegen verdeckt, Rückseite schwarz mit Goldlinie und dem Namen der Bar.
# Beim Auftritt dreht sich eine nach der anderen um, darunter erscheint, wer es ist.
def v23(n):
    c = ''.join('<article class="c23-p" style="--n:%d"><div class="c23-karte"><div class="c23-rueck"><span>WALK ON THE</span><b>WILD SIDE</b><span>GASTSCHICHT</span></div><div class="c23-vorn">%s</div></div>%s</article>' % (
        j, fo(k, '(max-width:760px) 44vw, 19vw'), satz(d, t, s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="c23-reihe vauf">%s</div>' % c)
V.append((23, 'Verdeckte Karten', v23))


# 24 · Übereinander: je Gast eine grosse Tafel mit Bild und Namen; beim Scrollen bleibt jede oben stehen und die nächste schiebt sich darüber.
# Die untere tritt dabei etwas zurück, so liegt am Ende ein Stapel von fünf Abenden.
def v24(n):
    t = ''.join('<article class="t24-t" style="--n:%d"><div class="t24-innen">%s<div class="t24-text"><p class="t24-dat titel">%s</p><h3 class="titel">%s</h3><p>%s</p></div></div></article>' % (
        j, fo(k, '(max-width:760px) 40vw, 26vw'), E(d), E(t_), E(s)) for j, (k, d, t_, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="t24-stapel">%s</div>' % t)
V.append((24, 'Übereinander', v24))


# 25 · Zwei Laufbänder: oben ziehen die Bilder, darunter die Namen in grosser Schrift, beide gegeneinander und vom Scrollen getrieben.
# Wer sich nicht bewegt, sieht einen ruhigen Streifen.
def v25(n):
    b = ''.join('<div class="l25-b">%s</div>' % fo(k, '(max-width:760px) 44vw, 17vw') for k, d, t, s in GAESTE)
    nm = ''.join('<p class="l25-n"><span>%s</span><b class="titel">%s</b></p>' % (E(d), E(t)) for k, d, t, s in GAESTE)
    sz = ''.join('<div class="l25-s">%s</div>' % satz(d, t, s) for k, d, t, s in GAESTE)
    return sek(n, '<div class="innen">%s</div><div class="l25-baender" data-baender><div class="l25-band l25-oben">%s%s</div><div class="l25-band l25-unten">%s%s</div></div><div class="innen l25-saetze">%s</div>' % (
        kopf(), b, b, nm, nm, sz), innen=False)
V.append((25, 'Zwei Laufbänder', v25))


# 26 · Kalenderblätter: je Gast ein Blatt vom Abreisskalender, oben die Bindung, gross der Tag, darunter Monat und Bild.
# Die Blätter fallen nacheinander von oben auf ihren Platz und federn kurz nach.
def v26(n):
    c = ''.join('<article class="k26-p" style="--n:%d;--w:%sdeg"><div class="k26-blatt"><div class="k26-bindung"><i></i><i></i></div><p class="k26-tag titel">%s</p><p class="k26-monat">%s %s</p>%s</div><h3 class="titel">%s</h3><p class="k26-s">%s</p></article>' % (
        j, w, d[:2], MONAT[d[3:5]], d[6:], fo(k, '(max-width:760px) 40vw, 15vw'), E(t), E(s)) for j, ((k, d, t, s), w) in enumerate(zip(GAESTE, (-2, 1.5, -1, 2, -1.5))))
    return sek(n, kopf() + '<div class="k26-reihe vauf">%s</div>' % c)
V.append((26, 'Kalenderblätter', v26))


# 27 · Gesicht und Hand: von jedem Foto zwei Ausschnitte übereinander, oben das Gesicht, unten der Moment am Glas oder am Tresen.
# Die beiden Ausschnitte kommen von oben und unten aufeinander zu und treffen sich.
def v27(n):
    p = ''.join('<article class="g27-p" style="--n:%d"><div class="g27-oben">%s</div><div class="g27-unten">%s</div>%s</article>' % (
        j, fo(k, '(max-width:760px) 44vw, 18vw'), fo(k, '(max-width:760px) 60vw, 26vw'), satz(d, t, s)) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="g27-reihe vauf">%s</div>' % p)
V.append((27, 'Gesicht und Hand', v27))


# 28 · Der Tresen von oben: die fünf liegen wie Fotos auf dem Tresen, man sieht schräg von oben darauf.
# Beim Scrollen richtet sich die Fläche auf, bis sie gerade vor einem steht.
def v28(n):
    p = ''.join('<article class="o28-p">%s%s</article>' % (fo(k, '(max-width:760px) 44vw, 18vw'), satz(d, t, s)) for k, d, t, s in GAESTE)
    return sek(n, kopf() + '<div class="o28-raum" data-tresen><div class="o28-flaeche">%s</div></div>' % p)
V.append((28, 'Der Tresen von oben', v28))


# 29 · Erst Schwarzweiss: die fünf stehen in Schwarzweiss nebeneinander wie auf den Plakaten der Bar.
# Beim Scrollen bekommt einer nach dem anderen von links seine Farbe.
def v29(n):
    def bild(k):
        return '<figure class="hf s29-f" style="--lq:url(%s)">%s%s</figure>' % (mache(k)['lq'], B.img_tag(k, '(max-width:760px) 44vw, 20vw'), B.img_tag(k, '(max-width:760px) 44vw, 20vw', extra=' class="s29-grau"'))
    p = ''.join('<article class="s29-p">%s%s</article>' % (bild(k), satz(d, t, s)) for k, d, t, s in GAESTE)
    return sek(n, kopf() + '<div class="s29-reihe" data-farbe>%s</div>' % p)
V.append((29, 'Erst Schwarzweiss', v29))


# 30 · Die Liste an der Tür: ein Klemmbrett wie beim Einlass, je Gast eine Zeile mit Kästchen, Datum, Name und Satz.
# Beim Auftritt wird einer nach dem anderen abgehakt, dann erscheint sein Bild am Ende der Zeile.
def v30(n):
    z = ''.join('<div class="t30-z" style="--n:%d"><span class="t30-box"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7"/></svg></span><span class="t30-dat">%s</span><div><h3 class="titel">%s</h3><p>%s</p></div>%s</div>' % (
        j, E(d), E(t), E(s), fo(k, '(max-width:760px) 20vw, 7vw')) for j, (k, d, t, s) in enumerate(GAESTE))
    return sek(n, kopf() + '<div class="t30-brett vauf"><i class="t30-klemme"></i><div class="t30-blatt"><p class="t30-kopf"><span>Gästeliste</span><span>Hinterm Tresen · 2024</span></p>%s</div></div>' % z)
V.append((30, 'Die Liste an der Tür', v30))


def seite(n):
    h = unter.programm()
    eintrag = dict((nr, (nm, f)) for nr, nm, f in V)
    if n:
        a = h.rfind('<section', 0, h.find('id="gaeste"'))
        b = h.find('</section>', a) + len('</section>')
        h = h[:a] + eintrag[n][1](n) + h[b:]
    liste = [[0, 'Heutiger Stand']] + [[nr, nm] for nr, nm, _ in V]
    h = h.replace('<head>', '<head><base href="../../">', 1)
    h = h.replace('</head>', '<link rel="stylesheet" href="%s/h.css?v=%s"></head>' % (ORD, VER), 1)
    schild = '<p class="vschild"><b>%02d / %d</b><span>%s</span><i>← →</i></p>' % (n, V[-1][0], E(eintrag[n][0] if n else 'Heutiger Stand'))
    skripte = '<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script><script src="%s/nav.js?v=%s" defer></script><script src="%s/h.js?v=%s" defer></script>' % (
        json.dumps(liste, ensure_ascii=False), n, json.dumps(ORD), ORD, VER, ORD, VER)
    return h.replace('</body>', schild + skripte + '</body>', 1)


if __name__ == '__main__':
    for n in [0] + [nr for nr, _, _ in V]:
        open(os.path.join(ORD, '%02d.html' % n), 'w').write(seite(n))
    print('00, 16 …', V[-1][0])
