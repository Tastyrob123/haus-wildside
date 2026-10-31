"""Walk on the Wild Side · Neubau 28.10.2026. Baut die Startseite (ein Abend an der Ecke, 19 bis 2 Uhr) und über unter.py die Unterseiten.
Inhalte (Zeiten, Adresse, Line-up) stehen einmal in HAUS; jede Zahl mit Quelle in _quelle/ (CHARAKTER.md). Konzept: _kette/06-konzepter/KONZEPT-2026-10-28.md"""
import html, json, math, os, re
from bilder import mache

HIER = os.path.dirname(os.path.abspath(__file__))
V = '31113'
E = html.escape

HAUS = {
    'adresse': 'Haasemannstraße 13', 'ort': '30449 Hannover-Linden', 'ecke': 'Ecke Rampenstraße, zwei Minuten vom Küchengarten',
    'telefon': '+49 163 3909578', 'tel_href': '+491633909578',          # Google-Eintrag und Falstaff, 25.10.2026
    'telefon2': '+49 174 9916296', 'tel2_href': '+491749916296',        # Angebotsmappe der Bar, Seite «Noch Fragen?» (30.10.2026)
    'instagram': 'https://www.instagram.com/walkonthewildside_hannover/', 'ig_name': '@walkonthewildside_hannover',
    'zeiten': [('Donnerstag', '19 bis 1 Uhr', '4'), ('Freitag', '19 bis 2 Uhr', '5'), ('Samstag', '19 bis 2 Uhr', '6'),
               ('Sonntag bis Mittwoch', 'geschlossen', '0,1,2,3')],   # Instagram-Bio, Falstaff, NeoTaste
    'zeit_kurz': 'Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr',
    'culinarium': 'http://localhost:8765/', 'dirty': 'http://localhost:8765/dirty-chicken.html',
}
# Die DJ-Abende der Bar (auf den Plakaten «SESSION»): alle Abende aus den Beiträgen der Bar (ig/beitraege.md), neueste zuerst
LINEUP = [
    ('17.10.2026', 'Ghazouani Brothers', 'elektronisch, aus Tunis', 'p-1710'),
    ('03.10.2026', 'Jojo & Reza', 'Old-School-Hip-Hop', 'p-0310'),
    ('05.09.2026', 'Apo', '', 'p-0509'),
    ('16.05.2026', 'Jojo & Reza', 'Old School', 'p-1605'),
    ('21.03.2026', 'Moury', '', 'p-2103'),
    ('24.01.2026', 'Loverence', '', 'p-2401'),
    ('06.12.2025', 'Kollektiv Gerber', 'Marco Nocks, Mahir Maulud, Leole', 'p-2211'),
    ('22.11.2025', 'Moury', '', 'p-2211'),
    ('06.09.2025', 'Björn', 'This Is Social Club, der erste Abend', 'p-0906'),
]

PFEIL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def logo_svg():
    """Die nachgezogene Wortmarke (potrace) als Inline-SVG, Farbe über currentColor."""
    s = open(os.path.join(HIER, '..', '_quelle', 'logo', 'wildside-logo-nachgezogen.svg')).read()
    s = re.sub(r'<\?xml.*?\?>|<!DOCTYPE[^>]*>|<metadata>.*?</metadata>', '', s, flags=re.S)
    s = re.sub(r'<svg[^>]*>', '<svg viewBox="0 0 1296 1600" aria-hidden="true" focusable="false">', s, count=1)
    s = s.replace('fill="#111111"', 'fill="currentColor"')
    return re.sub(r'\s+', ' ', s).strip()


LOGO = logo_svg()


def img_tag(k, sizes='50vw', sofort=False, extra=''):
    d = mache(k)
    srcset = ', '.join('assets/bild/%s?v=%s %dw' % (f, V, b) for b, f in d['stufen'])
    if sofort:
        return '<img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" fetchpriority="high" decoding="async" width="%d" height="%d"%s>' % (
            d['stufen'][-1][1], V, srcset, sizes, E(d['alt']), d['w'], d['h'], extra)
    return '<img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s>' % (srcset, sizes, E(d['alt']), d['w'], d['h'], extra)


def bild(k, cls='foto', sizes='50vw', sofort=False, stil='', extra=''):
    return '<figure class="%s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img_tag(k, sizes, sofort, extra))


def kachel(k, cls='', sizes='50vw', stil='', n=None):
    return bild(k, 'kachel leise ' + cls, sizes, stil=stil + ('--n:%d;' % n if n is not None else ''))


def knopf(text, href, cls=''):
    return '<a class="knopf %s" href="%s"><span>%s</span><i>%s</i></a>' % (cls, href, E(text), PFEIL)


def weiter(text, href, span=False):
    t = 'span' if span else 'a'
    return '<%s class="weiter"%s>%s %s</%s>' % (t, '' if span else ' href="%s"' % href, E(text), PFEIL, t)


def zl(zeilen, cls='titel', i0=0):
    """Zeilen aus dem Schlitz."""
    return '<span class="zl">%s</span>' % ''.join('<span class="z"><span style="--i:%d">%s</span></span>' % (i0 + n, z) for n, z in enumerate(zeilen))


def h2(zeilen, cls='t-kap', i0=0):
    return '<h2 class="titel %s">%s</h2>' % (cls, zl(zeilen, i0=i0))


def kz(uhr, was, i=0, stil=''):
    return '<div class="kz sw" style="--i:%d;%s"><span class="uhr">%s</span><i></i><span class="was">%s</span></div>' % (i, stil, E(uhr), E(was))


def fenster(k, satz, pos='50% 50%'):
    """Bild steht, die Seite zieht darüber, der Satz rollt (Rivage-Höhe)."""
    d = mache(k)
    return '<section class="fenster"><figure class="foto" style="--lq:url(%s)">%s<div class="fe-hof"></div><p class="fe-satz">%s</p></figure></section>' % (
        d['lq'], img_tag(k, '100vw', extra=' style="object-position:%s"' % pos), zl(satz))


def mosaik(k, satz, pos='50% 50%'):
    """Zwölf Stücke desselben Bildes steigen aus verschiedenen Tiefen und schliessen sich zum Bild (Wahl Robert 29.10.2026, Fassung 8)."""
    d = mache(k)
    versatz = [22, 8, 30, 14, 12, 26, 6, 20, 28, 16, 24, 10]
    # Seit 29.10.2026 abends schneller und ohne Warten (Robert: «alle ein bisschen schneller und smoother, weil die warten jetzt immer noch alle»):
    # eine kurze Welle von oben Mitte, das letzte Stück startet nach 0,14 s.
    def warte(c, r):
        return math.hypot(((c + .5) / 4 - .5) * 1.6, (r + .5) / 3) * .15
    teile = ''.join('<div class="gw-t" style="--c:%d;--r:%d;--v:%dvh;--d:%.2fs">%s</div>' % (
        c, r, versatz[r * 4 + c], warte(c, r), img_tag(k, '100vw', extra=' style="object-position:%s"%s' % (pos, '' if r + c == 0 else ' aria-hidden="true"')))
        for r in range(3) for c in range(4))
    return '<section class="gewoelbe" style="--lq:url(%s)"><div class="gw-feld">%s</div><p class="gw-satz">%s</p></section>' % (d['lq'], teile, zl(satz, i0=3))


# Das Laufband unter dem Gewölbe (Robert 29.10.2026: «schmal, so wie bei Dirty Chicken … nichts in Rot, eher Gold»). Nur Angaben, die auf der Seite belegt sind.
BAND = ['Nachbarschafts-Mixology-Bar', 'Momo seit 2018 in Linden', 'Donnerstag bis Samstag ab 19 Uhr', HAUS['adresse'] + ', Linden', 'Falstaff Bar Guide 2027 · 91 Punkte']


def band():
    reihe = '<p>%s</p>' % ''.join('<span>%s</span><i></i>' % E(t) for t in BAND)
    return '<div class="wb-band" aria-hidden="true"><div class="wb-band-zug">%s%s</div></div>' % (reihe, reihe)


def fenster_fest(k, satz, pos='50% 50%'):
    """Fenster in der festgelegten Grösse (Culinarium-Mass, höchstens 67 % der Bildschirmhöhe, Handy 58 %): Bild und Satz stehen, die Seite zieht darüber (Robert 29.10.2026)."""
    d = mache(k)
    return '<section class="fk" aria-label="%s"><figure class="foto" style="--lq:url(%s)">%s<div class="fe-hof"></div><p class="fe-satz">%s</p></figure></section>' % (
        E(' '.join(satz)), d['lq'], img_tag(k, '100vw', extra=' style="object-position:%s"' % pos), zl(satz))


def ueber(satz, hell=False):
    return '<p class="ueber sw%s" style="--i:0">%s</p>' % (' hellu' if hell else '', E(satz))


# ---------------------------------------------------------------- Kapitel der Startseite
def auftakt():
    return '''<header class="auftakt auf" id="auftakt">
%s<div class="at-hof"></div><div class="schleier"></div>
<div class="innen"><a class="at-logo sw" style="--i:0" href="index.html" aria-label="Walk on the Wild Side">%s</a>
<h1 class="titel at-titel">%s</h1>
<p class="at-satz sw" style="--i:3">Eine Nachbarschafts-Mixology-Bar in Linden-Mitte. Die Drinks entwirft Momo, die Karte wechselt immer wieder, und an der Bar sagst du, was du magst.</p>
<div class="at-zeile sw" style="--i:4"><span class="etikett">%s</span><span class="trenner"></span><span class="ort">%s · Linden</span></div>
<div class="knoepfe sw" style="--i:5">%s%s</div></div>
<p class="at-weiter sw" style="--i:6">Ein Abend an der Ecke, von 19 bis 2 Uhr</p>
</header>''' % (bild('schild', 'at-bild', '100vw', True), LOGO, zl(['Du sagst,', 'was du magst.'], i0=1), E(HAUS['zeit_kurz']), E(HAUS['adresse']),
                knopf('Platz reservieren', 'besuch.html#reservieren', 'rot'), knopf('Heute Abend', 'programm.html'))


def kap_plakat():
    """Die Bar: links das Eckschild (Nacht, Goldlinie, die sich einmal herumzieht), rechts zwei Querbilder übereinander, die nacheinander aus der Tiefe kommen.
    Wahl Robert 31.10.2026: Fassung 4 «Schild und zwei Bilder» aus _varianten/bar-15c/, dazu «Wer, Wo, Wann» neu als drei Felder mit Goldfugen.
    Anlass: Wunsch der Bar «layout etwas cleaner, zu viele Bilder». Stand davor bau.py.vor-bar-fassung4-2026-10-31"""
    fakten = [('Wer', 'Derya Ivkin führt die Bar, Momo Ben Khelifa mixt'), ('Wo', HAUS['adresse'] + ', ' + HAUS['ecke']),
              ('Wann', HAUS['zeit_kurz'].replace(' · ', '<br>').replace(' bis ', '&nbsp;bis&nbsp;').replace(' Uhr', '&nbsp;Uhr'))]   # Zeiten brechen nie mitten auseinander

    def bk(k, n, pos):
        return '<figure class="kachel bw4-b" style="--lq:url(%s);--n:%d">%s</figure>' % (mache(k)['lq'], n, img_tag(k, '(max-width:900px) 92vw, 38vw', extra=' style="object-position:%s"' % pos))
    schild = '''<div class="bw4-s"><svg class="es-linie" aria-hidden="true"><rect x="9" y="9" rx="9" ry="9" pathLength="100"/></svg>
<span class="bw4-logo">%s</span>
<h2 class="titel bw4-t">%s</h2>
<p class="text bw4-x">So nennt sich das Wild Side selbst, und so ist es gemeint: eine kleine Bar an der Ecke, in der man sich kennt, mit Drinks, für die man sonst weit fahren müsste. Seit November 2023 mit Derya und Momo hinter der Theke. Im Falstaff Bar Guide 2027 mit 91 Punkten.</p>
<div class="bw4-f">%s</div></div>''' % (LOGO, zl(['Eure Nachbarschafts-', 'Mixology-Bar.'], i0=1),
                                     ''.join('<div style="--n:%d"><b>%s</b><p>%s</p></div>' % (n, E(a), b) for n, (a, b) in enumerate(fakten)))
    return '''<section class="kap auf bar-wand bw4" id="bar"><div class="innen">%s
<div class="bw4-g">%s<div class="bw4-r">%s%s</div></div>
%s</div></section>''' % (kz('19:30', 'An der Ecke', 0), schild, bk('ft-momo-mixt-gast', 0, '45% 40%'), bk('ft-runde-stoesst-an', 1, '50% 40%'),
                           ueber('Und dann fragt Momo.'))


GESPRAECH = [
    # Antworten auf die drei Wahlzeilen: Geschmack, Art, Basis. Jede Antwort ein Satz und ein Glas der Bar.
    {'wenn': {'geschmack': 'sauer', 'basis': 'gin'}, 'satz': 'Dann vielleicht ein Sour|mit Gin, Bergamotte und Schaum.', 'bild': 'glas-sour'},
    {'wenn': {'geschmack': 'sauer', 'basis': 'whisky'}, 'satz': 'Dann ein Whisky Sour,|mit Honig statt Zucker.', 'bild': 'schaum'},
    {'wenn': {'geschmack': 'sauer'}, 'satz': 'Dann etwas Helles mit Limette,|hoch im Glas, viel Eis.', 'bild': 'glas-hand'},
    {'wenn': {'geschmack': 'bitter', 'basis': 'gin'}, 'satz': 'Dann ein Negroni.|Den rührt Momo auf Eis.', 'bild': 'glas-negroni'},
    {'wenn': {'geschmack': 'bitter'}, 'satz': 'Dann etwas Rotes mit Wermut,|kalt gerührt, ohne Schaum.', 'bild': 'glas-rot'},
    {'wenn': {'geschmack': 'suess', 'art': 'cremig'}, 'satz': 'Dann etwas Weiches mit Kakao|und Rum, der nach Butter schmeckt.', 'bild': 'glas-coupe'},
    {'wenn': {'geschmack': 'suess'}, 'satz': 'Dann etwas mit Beeren und Vanille,|kalt und klar.', 'bild': 'glas-kerze'},
    {'wenn': {'geschmack': 'rauchig', 'basis': 'mezcal'}, 'satz': 'Dann Mezcal, Agave und Limette,|ein bisschen Salz am Rand.', 'bild': 'glas-trinkt'},
    {'wenn': {'geschmack': 'rauchig'}, 'satz': 'Dann etwas Dunkles mit Rauch,|ein grosser Eiswürfel.', 'bild': 'glas-zwei'},
    {'wenn': {'basis': 'ohne'}, 'satz': 'Dann ohne Alkohol, aber nicht ohne Idee:|Shrub, Soda, ein paar Kräuter.', 'bild': 'glas-hand'},
    {'wenn': {}, 'satz': 'Dann fragt Momo noch einmal nach|und mixt dir, was zu dir passt.', 'bild': 'glas-sour'},
]
FRAGEN = [('geschmack', 'Lieber', [('sauer', 'sauer'), ('suess', 'süss'), ('bitter', 'bitter'), ('rauchig', 'rauchig')]),
          ('art', 'Im Glas', [('klar', 'klar'), ('cremig', 'cremig'), ('spritzig', 'spritzig')]),
          ('basis', 'Darin', [('gin', 'Gin'), ('rum', 'Rum'), ('mezcal', 'Mezcal'), ('whisky', 'Whisky'), ('ohne', 'ohne Alkohol')])]


def gespraech_html(lang=False):
    glaeser = sorted(set(a['bild'] for a in GESPRAECH))
    fragen = ''.join('<div class="ge-frage sw" style="--i:%d"><span class="etikett">%s</span><div class="wahl" data-frage="%s">%s</div></div>' % (
        n + 2, E(e), k, ''.join('<button type="button" data-w="%s">%s</button>' % (w, E(t)) for w, t in opt)) for n, (k, e, opt) in enumerate(FRAGEN))
    return '''<div class="ge-fragen">%s</div>
<div class="ge-antwort sw" style="--i:5"><div><span class="etikett">Momo würde sagen</span><p class="ge-satz"></p></div>
<div class="ge-glas">%s</div></div>''' % (fragen, ''.join(bild(k, 'foto', '160px', extra=' data-k="%s"' % k).replace('<figure class="foto"', '<figure class="foto" data-k="%s"' % k) for k in glaeser))


# An der Theke seit 29.10.2026 (Wahl Robert: Fassung 13 «Der Weg nach unten» aus _varianten/momo-15): Momo bei der Arbeit in fünf echten Fotos,
# im Zickzack an einer Goldlinie, die beim Scrollen mitläuft. Kein Auswählen mehr («was soll das bringen da i was auszuwählen?»).
THEKE = [
    ('momo-lacht', 'Erst fragt Momo.', 'Sauer oder süss, klar oder cremig, Gin oder lieber gar kein Alkohol.'),
    ('momo-flaschen', 'Dann wählt er die Zutaten.', 'Nach dem, was du ihm gesagt hast.'),
    ('momo-giesst', 'Dann mixt er deinen Drink.', 'Momo hat Biotechnologie studiert, bevor er hinter die Bar ging.'),   # Neue Presse 14.09.2021
    ('schaum', 'Zum Schluss der Schaum.', 'Aus dem Siphon, direkt aufs Glas.'),
    ('glas-hand', 'Und dann ist es deiner.', 'Ein Drink, den es nur an diesem Abend gibt.'),
]
THEKE_POS = {'momo-lacht': '58% 45%', 'momo-flaschen': '40% 50%', 'momo-giesst': '62% 40%'}


def kap_gespraech():
    schritte = ''.join('''<div class="th-st th-%s"><figure class="kachel leise" style="--lq:url(%s)">%s</figure><i class="th-punkt"></i>
<div class="th-satz"><p class="titel">%s</p><p class="th-zu">%s</p></div></div>''' % (
        'l' if n % 2 == 0 else 'r', mache(k)['lq'], img_tag(k, '(max-width:900px) 80vw, 38vw', extra=' style="object-position:%s"' % THEKE_POS.get(k, '50% 50%')), E(t), E(z))
        for n, (k, t, z) in enumerate(THEKE))
    return '''<section class="kap auf" id="drinks"><div class="innen">
<div class="th-kopf"><div>%s%s
<p class="text sw" style="--i:1">Eine Getränkekarte gibt es im Wild Side nicht. Wer an die Theke kommt, wird gefragt, was er mag, und Momo macht daraus einen Drink. So sieht das aus.</p></div>
<p class="ge-zitat sw" style="--i:2">«Du sagst mir, was du magst, ich mache dir einen Drink.»<small>Momo, hinter der Theke</small></p></div>
<div class="th-weg" data-weg><div class="th-linie"><i></i></div>%s
<div class="th-fuss"><div class="knoepfe">%s</div></div></div>
</div>%s</section>''' % (kz('20:00', 'An der Theke', 0), h2(['Was magst du?']), schritte, knopf('Alle Drinks', 'drinks.html'), ueber('Und irgendwann schaust du nach oben.'))


def kap_theke():
    jahre = [('2018', 'In Linden', 'Seit 2018 ist Momo in Linden zu Hause, zuerst mit der Probierbar an der Limmerstraße. Danach kommt das gemeinsame Baby von Derya und Momo: das Wild Side.'),
             ('2023', 'Neu an der Ecke', 'Am 9. November 2023 machen Derya Ivkin und Momo Ben Khelifa die Bar wieder auf: drei Abende die Woche, mit DJs und Konzerten. Seitdem heisst es Nachbarschafts-Mixology-Bar. Dazu Stadtfeste wie die Christi Limmerfahrt und das Südstadtfest, mit Partnern aus der Gastronomie.'),
             ('2027', 'Falstaff', 'Im Falstaff Bar Guide 2027 steht das Wild Side mit 91 Punkten unter den Cocktailbars: 47 von 50 für die Drinks. Bei Google geben 75 Gäste im Schnitt 4,8 von 5.')]
    return '''<section class="kap hell auf" id="seit2017"><div class="innen">
%s%s
<div class="theke" style="margin-top:34px">
<div class="jahres platte hell" style="padding:clamp(24px,3vw,40px)"><div class="jahres jahre staffel">%s</div></div>
<div class="theke-bild"><div class="kachel leise sw" style="--i:2;--lq:url(%s)">%s</div>
<div class="wert sw" style="--i:3"><span class="zahl">91</span><div><span class="etikett">Falstaff Bar Guide 2027</span><p>Cocktailbars, 47 von 50 Punkten für die Drinks.</p></div></div></div>
</div>%s</div></section>''' % (kz('21:00', 'Unter der Decke', 0), h2(['Seit 2018 in Linden.']),
                                ''.join('<div class="jahr" style="--n:%d"><span class="zahl">%s</span><span class="etikett">%s</span><p>%s</p></div>' % (n, j, e, E(t)) for n, (j, e, t) in enumerate(jahre)),
                                mache('decke-2017')['lq'], img_tag('decke-2017', '40vw'), ueber('Gegen 23 Uhr wird es lauter.', True))


def kap_chronik():
    """Seit 2017 als Schachbrett: Fotos und Jahre wechseln sich in einem geschlossenen Raster ab, mit den Fugen des Mosaiks (Wahl Robert 29.10.2026, Fassung 2)."""
    jahre = [('2018', 'In Linden', 'Seit 2018 ist Momo in Linden zu Hause, zuerst mit der Probierbar an der Limmerstraße. Danach kommt das gemeinsame Baby von Derya und Momo: das Wild Side.'),
             ('2023', 'Neu an der Ecke', 'Am 9. November 2023 machen Derya Ivkin und Momo Ben Khelifa die Bar wieder auf: drei Abende die Woche, mit DJs und Konzerten. Seitdem heisst es Nachbarschafts-Mixology-Bar. Dazu Stadtfeste wie die Christi Limmerfahrt und das Südstadtfest, mit Partnern aus der Gastronomie.'),
             ('2027', 'Falstaff', 'Im Falstaff Bar Guide 2027 steht das Wild Side mit 91 Punkten unter den Cocktailbars: 47 von 50 für die Drinks. Bei Google geben 75 Gäste im Schnitt 4,8 von 5.')]
    z = lambda n: '<div class="ch-z hell"><span class="ch-jz">%s</span><span class="etikett">%s</span><p>%s</p></div>' % (jahre[n][0], jahre[n][1], E(jahre[n][2]))
    f = lambda k, p: bild(k, 'foto', '25vw', extra=' style="object-position:%s"' % p)
    zellen = [f('alt-theke', '50% 50%'), z(0), f('fb-2023-negroni', '50% 40%'), z(1), z(2), f('momo-flaschen', '50% 30%'),
              '<div class="ch-z ch-nz"><span class="ch-jz">91</span><span class="etikett">Falstaff Bar Guide 2027</span><p>Cocktailbars, 47 von 50 Punkten für die Drinks.</p></div>',
              f('alt-rueckbar', '50% 50%')]
    return '<section class="chronik auf" id="seit2017"><div class="innen ch-kopf">%s<h2 class="titel t-gross">%s</h2></div><div class="ch-brett flaeche">%s</div><div class="innen">%s</div></section>' % (
        kz('21:00', 'Unter der Decke', 0), zl(['Seit 2018 in Linden.'], i0=1), ''.join(zellen), ueber('Gegen 23 Uhr wird es lauter.'))


def flyer(k0, mit_allen=False):
    """Der Flyer auf dem Tresen: das echte Plakatmaterial als cremefarbene Karte."""
    d0, n0, r0, _ = LINEUP[0]
    bilder = ''.join(img_tag(k, '36vw', extra=' data-k="%s" class="%s"' % (k, 'an' if k == k0 else '')) for k in (sorted(set(l[3] for l in LINEUP)) if mit_allen else [k0]))
    return '''<div class="flyer sw" id="flyer" style="--i:2"><figure class="foto" style="--lq:url(%s)">%s</figure>
<div class="fl-unten"><span class="fl-reihe">Die DJ-Abende der Bar · samstags 21 bis 1 Uhr</span><p class="fl-name">%s</p><p class="fl-datum">%s%s</p></div></div>''' % (
        mache(k0)['lq'], bilder, E(n0), E(d0), (' · ' + E(r0)) if r0 else '')


def kap_lauter():
    """Links gross der Flyer, rechts der Text mit der Zeitleiste von 21 bis 1 Uhr, deren Goldlinie sich beim Auftritt zieht
    (Wahl Robert 29.10.2026, Fassung 9 «Von 21 bis 1 Uhr», _varianten/lauter-15/)."""
    def lk(k, pos=None):
        extra = ' style="object-position:%s"' % pos if pos else ''
        return '<figure class="kachel" style="--lq:url(%s)">%s</figure>' % (mache(k)['lq'], img_tag(k, '25vw', extra=extra))
    uhr = ''.join('<span style="--x:%d"><b>%s</b></span>' % (j, h) for j, h in enumerate(['21 Uhr', '22', '23', '0', '1 Uhr']))
    return '''<section class="kap auf lauter-uhr" id="lauter"><div class="innen">
<div class="lu">%s
<div class="lu-r">%s<h2 class="titel">%s</h2>
<p class="text sw" style="--i:2">Samstags legen DJs an der Bar auf, rund einmal im Monat, von 21 bis 1 Uhr. Momo mixt dazu. Donnerstags spielt ab und zu jemand live, mitten im Raum, ohne Eintritt. Und an manchen Abenden steht neben Momo ein Gast aus einer anderen Bar mit eigenen Drinks.</p>
<div class="lu-zeit sw" style="--i:2"><span class="etikett">Samstags</span><div class="lu-strahl"><i></i>%s</div></div>
<div class="knoepfe sw" style="--i:3">%s</div>
<div class="lu-bilder">%s%s</div></div>
</div>%s</div></section>''' % (flyer(LINEUP[0][3]).replace('class="flyer sw"', 'class="flyer lu-flyer sw"', 1), kz('23:00', 'Lauter', 0), zl(['Samstags legt', 'jemand auf.'], i0=1),
                                uhr, knopf('Das Programm', 'programm.html'), lk('konzert-love', '50% 40%'), lk('saengerin-kunde', '50% 40%'),   # Bild der Bar (Web Side.pdf, 30.10.2026)
                               
                                ueber('An manchen Abenden gehört die Empore euch.'))


def kap_tafel():
    """Die Speisenfolge (Wahl Robert 29.10.2026, Fassung 3 mit Änderungen): links drei Bilder als Kacheln untereinander,
    in der Mitte die Karte wie ein gedrucktes Menü im Rahmen des Eckschilds, rechts die Tafel von oben als ein Bild, weiter gefasst."""
    zeilen = [('Wo', 'Oben auf der kleinen Empore, an einer langen Tafel.'), ('Für wen', 'Zehn bis zwanzig Gäste an der Tafel.'), ('Ab 30 Personen', 'Die ganze Bar für geschlossene Veranstaltungen, jeder Abend individuell gestaltet.'), ('Hochzeiten', 'Wir richten auch eure Hochzeit aus, mit Party.'),
              ('Drinks', 'Momo stimmt sie auf euer Menü ab.'), ('Wie', 'Anfragen, Angebot bekommen, Abend feiern.')]
    links = ''.join(bild(k, 'kachel leise', '26vw', extra=' style="object-position:%s"' % p) for k, p in [('fw-a9', '50% 58%'), ('tf-l5', '50% 50%'), ('fw-h30', '50% 55%')])
    gaenge = ''.join('<div class="tk-gang" style="--n:%d"><span class="etikett">%s</span><p>%s</p></div>' % (n, E(a), E(b)) for n, (a, b) in enumerate(zeilen))
    karte = '<div class="tk-karte sw"><div class="tk-rahmen">%s%s<i class="tk-zier"></i><p class="text">An manchen Abenden gehört der obere Teil der Bar einer einzigen Runde. Dann steht dort eine lange Tafel, Momo mixt die Drinks passend zum Menü, und unten läuft der Abend weiter wie immer.</p><div class="tk-gaenge staffel">%s</div><div class="knoepfe">%s</div></div></div>' % (
        kz('Ein anderer Abend', 'Auf der Empore', 0), h2(['Die lange Tafel.'], i0=1), gaenge, knopf('Feiern im Wild Side', 'tafel.html'))
    return '<section class="kap auf" id="tafel"><div class="innen tk"><div class="tk-links flaeche">%s</div>%s%s</div>%s</section>' % (
        links, karte, bild('tf-oben', 'kachel leise tk-rechts', '36vw', extra=' style="object-position:50% 50%"'), ueber('Und wer sonst noch hier zu Hause ist.'))


def kap_haus():
    # Vitrine (Robert 29.10.2026: Fassung 7 aus _varianten/imhaus-edel, «da unten alles bündig» mit den Links). Stand davor *.vor-vitrine-2026-10-29
    eintraege = [(HAUS['culinarium'], 'culinarium-tafel', '50% 50%', 'Food-Pairing-Abende', 'Culinarium.', 'An einzelnen Wochenenden wird aus der Tafel ein Menü: Rudi kocht drei Gänge, Momo mixt fünf Drinks dazu, vierzehn Gäste sitzen an einem Tisch. Eigene Abende, eigene Tickets, eigene Seite.', 'Zu Culinarium'),
                 (HAUS['dirty'], 'dirty-burger', '50% 58%', 'Pop-up', 'Dirty Chicken.', 'Rudis Sandwiches aus der Familie der Bar, mal hier, mal im Tiedthof. Termine auf Instagram.', 'Zu Dirty Chicken'),
                 ('programm.html#feste', 'feste-anstossen', '50% 34%', 'Die Feste', 'Silvester ab mittags.', 'Silvester mit Frühschoppen, der Geburtstag der Bar im Winter, Tanz in den Mai. Und der Mexikaner, Wild-Side-Tradition.', 'Alle Feste')]
    stuecke = ''
    for i, (h, k, pos, et, ti, tx, w) in enumerate(eintraege):
        lage = ' style="object-position:' + pos + '"'
        stuecke += ('<a class="vi-stueck" href="' + h + '" style="--n:' + str(i) + '"><div class="vi-bild"><i class="vi-licht"></i>'
                    + bild(k, 'vi-f', '30vw', extra=lage) + '<div class="vi-spiegel" aria-hidden="true">' + img_tag(k, '30vw', extra=lage) + '</div></div>'
                    + '<div class="vi-text"><span class="etikett">' + et + '</span><h3 class="titel">' + ti + '</h3><p class="text">' + tx + '</p>'
                    + weiter(w, '', True) + '</div></a>\n')
    return ('<section class="kap auf" id="imhaus"><div class="innen">\n' + kz('Im selben Haus', 'Zwei Nachbarn und die Feste', 0) + h2(['Unter demselben Dach.'])
            + '\n<div class="vitrine auf">\n' + stuecke + '</div>' + ueber('Bis 2 Uhr. Dann nach Hause.') + '</div></section>')


NAV = [('drinks.html', 'Drinks'), ('programm.html', 'Programm'), ('tafel.html', 'Feiern'), ('haus.html', 'Das Haus'), ('besuch.html', 'Besuch')]


def fuss(k='fenster'):
    """Fuss «Drei Fenster in einer Fassade» (Wahl Robert 29.10.2026, Fassung 3 aus _varianten/fuss-15): drei Fotos gleicher Höhe,
    die Bar doppelt so breit mit Logo, «heute» und Zeiten, daneben Culinarium und Dirty Chicken mit ihren Logos; unten alles bündig."""
    zeiten = ''.join('<div data-tag="%s"><span>%s<span class="jetzt"></span></span><b>%s</b></div>' % (t, E(n), E(z)) for n, z, t in HAUS['zeiten'])
    def fen(cls, key, sizes):
        return '<figure class="kachel" style="--lq:url(%s)">%s</figure>' % (mache(key)['lq'], img_tag(key, sizes))
    # Robert 29.10.2026: beide Logos auf eigener Kachel gleicher Höhe, Culinarium in Schiefer, Dirty Chicken in Lila (Farben der Culinarium-Seite)
    cu = '<span class="f03-marke f03-mcu"><img class="z-cu" src="assets/zeichen/cu-creme.svg?v=%s" alt="Culinarium" width="365" height="67" loading="lazy"></span>' % V
    dc = '<span class="f03-marke f03-mdc"><img class="z-dc" src="assets/zeichen/dc-creme.webp?v=%s" alt="Dirty Chicken, Sandwiches &amp; More" width="900" height="693" loading="lazy"></span>' % V
    return '''<footer class="fuss auf f2 f03" id="besuch"><div class="innen">
<div class="f03-reihe">
<div class="f03-f f03-ws hoch" style="--n:0">%s<div class="f03-u f03-wsu"><div><span class="logo f03-logo">%s</span></div><div class="zeiten">%s</div></div></div>
<a class="f03-f hoch" style="--n:1" href="%s">%s<div class="f03-u">%s<p class="n-satz">An einzelnen Wochenenden wird aus der langen Tafel ein Menü: Rudi kocht, Momo mixt die Drinks dazu.</p>%s</div></a>
<a class="f03-f hoch" style="--n:2" href="%s">%s<div class="f03-u">%s<p class="n-satz">Rudis Sandwiches aus der Familie der Bar, mal hier, mal im Tiedthof.</p>%s</div></a>
</div>
<div class="f03-unten hoch" style="--n:3"><div class="besuch"><span class="etikett">Besuch</span><p>%s<br>%s<br>%s</p><p><a href="tel:%s">%s</a><br><a href="%s" rel="noopener">%s</a></p></div></div>
<nav class="f-nav">%s</nav>
<div class="fuss-unten"><span>Walk on the Wild Side · Nachbarschafts-Mixology-Bar · Hannover-Linden</span><span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a> · Entwurf von Tasty Studios, nicht die offizielle Website</span></div>
</div></footer>''' % (fen('', k, '50vw'), LOGO, zeiten,
                       HAUS['culinarium'], fen('', 'nb-cu-bete', '25vw'), cu, weiter('Zu Culinarium', '', True),
                       HAUS['dirty'], fen('', 'nb-dc-burger', '25vw'), dc, weiter('Zu Dirty Chicken', '', True),
                       E(HAUS['adresse']), E(HAUS['ort']), E(HAUS['ecke']), HAUS['tel_href'], E(HAUS['telefon']), HAUS['instagram'], E(HAUS['ig_name']),
                       ''.join('<a href="%s">%s</a>' % (h, E(t)) for h, t in NAV))

def leiste(aktiv=''):
    return '<div class="leiste" id="leiste"><div class="innen"><a class="logo" href="index.html" aria-label="Walk on the Wild Side">%s</a><nav>%s</nav>%s</div></div>' % (
        LOGO, ''.join('<a href="%s"%s>%s</a>' % (h, ' class="aktiv"' if h == aktiv else '', E(t)) for h, t in NAV), knopf('Reservieren', 'besuch.html#reservieren', 'klein'))


def rahmen(titel, beschreibung, inhalt, aktiv='', body=''):
    return '''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%s</title><meta name="description" content="%s">
<meta name="theme-color" content="#130E0D"><link rel="preload" href="assets/schrift/prata-latin.woff2?v=%s" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/wild.css?v=%s"><script>document.documentElement.classList.add('js');try{if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('ruhig')}catch(e){}</script>
</head><body class="%s">
%s
%s
<script src="assets/wild.js?v=%s" defer></script>
</body></html>''' % (E(titel), E(beschreibung), V, V, body, leiste(aktiv), inhalt, V)


def seite():
    inhalt = ''.join([
        auftakt(),
        kap_plakat(),
        kap_gespraech(),
        mosaik('decke-2017', ['Ein Gewölbe', 'über der Theke.'], '50% 50%'),
        fenster_fest('fw-derya', ['Zwei Eröffnungen,', 'eine Decke.'], '60% 45%'),
        kap_chronik(),
        kap_lauter(),
        fenster_fest('fw-tafel', ['Ein Abend,', 'der nur euch gehört.'], '50% 50%'),   # Wahl Robert 29.10.2026: Fassung 1 aus _varianten/fenster-tafel-15b
        kap_tafel(),
        kap_haus(),
        band(),   # Robert 29.10.2026: das Laufband sitzt am Fuss, nicht mehr bei den Kacheln des Gewölbes
        fuss(),
    ])
    return rahmen('Walk on the Wild Side · Nachbarschafts-Mixology-Bar in Hannover-Linden',
                  'Walk on the Wild Side, Haasemannstraße 13, Hannover-Linden: Mixology mit wechselnder Karte, DJ-Abende, Konzerte und eine lange Tafel für private Abende. Donnerstag bis Samstag ab 19 Uhr.',
                  inhalt, 'index.html', 'start')


def schreiben(name, inhalt):
    """Erst fertig schreiben, dann austauschen: wer in dem Moment neu lädt, bekommt nie eine leere Seite (29.10.2026)."""
    ziel = os.path.join(HIER, name)
    with open(ziel + '.neu', 'w') as f:
        f.write(inhalt)
    os.replace(ziel + '.neu', ziel)


if __name__ == '__main__':
    schreiben('index.html', seite())
    print('index.html')
    import unter
    for name, h in unter.alle().items():
        schreiben(name, h)
        print(name)
