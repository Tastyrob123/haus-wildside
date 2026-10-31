"""Walk on the Wild Side · Unterseiten (Neubau 28.10.2026): Drinks, Programm, Die lange Tafel, Das Haus, Besuch, Impressum, Datenschutz.
Jede Seite ein eigenes Kapitel in derselben Machart: grosser Kopf (Stimmung), ein Fenster, dichte Abschnitte mit echtem Text."""
import json
import bau
import karte_ecke
from bau import (HAUS, LINEUP, LOGO, PFEIL, E, bild, img_tag, kachel, knopf, weiter, zl, h2, kz, fenster, ueber, rahmen, fuss, mache, fenster_fest,
                 GESPRAECH, gespraech_html)


def kopf(k, zeilen, satz, pos='50% 40%', i0=1):
    """Seitenkopf: ein Bild über den Schirm, Titel aus dem Schlitz, Satz. Das Licht geht an."""
    return '''<header class="sk auf" id="auftakt">%s<div class="sk-hof"></div><div class="schleier"></div>
<div class="innen"><h1 class="titel at-titel">%s</h1><p class="text sw" style="--i:%d">%s</p></div></header>''' % (
        bild(k, 'foto', '100vw', True, '--pos:%s' % pos), zl(zeilen, i0=i0), i0 + len(zeilen), E(satz))


def kopf_glaeser(zeilen, satz):
    """Kopf der Drinks-Seite: hinten laufen zwei Reihen Fotos langsam gegeneinander, vorn der Titel auf dunklem Schild mit Goldlinie
    (Wahl Robert 29.10.2026, Fassung 6 «Die Gläser laufen», _varianten/drinks-hero/)."""
    def reihe(keys):
        f = ''.join('<figure class="dg-f" style="--lq:url(%s)">%s</figure>' % (mache(k)['lq'], img_tag(k, '22vw', j < 4)) for j, k in enumerate(keys))
        return '<div class="dg-zug">%s%s</div>' % (f, f.replace('<img ', '<img aria-hidden="true" '))
    return '''<header class="sk-g auf" id="auftakt"><div class="dg-reihen"><div class="dg-r">%s</div><div class="dg-r dg-r2">%s</div></div>
<div class="dg-schild"><svg class="dg-linie" aria-hidden="true"><rect x="10" y="10" rx="8" ry="8" pathLength="100"/></svg><h1 class="titel">%s</h1><p class="text sw" style="--i:2">%s</p></div></header>''' % (
        reihe(['glas-coupe', 'glas-rot', 'schaum', 'glas-sour', 'glas-kerze', 'glas-hand']),
        reihe(['momo-giesst', 'rueckbar', 'flaschen', 'negroni', 'glas-trinkt', 'anstossen']), zl(zeilen, i0=1), E(satz))


def kopf_licht(zeilen, satz):
    """Kopf der Besuch-Seite (Wahl Robert 31.10.2026, _varianten/besuch-hero-15c Fassung 5 «Das Licht geht an»): sechs Fotos als Wand im
    Halbdunkel, eins nach dem anderen geht das Licht an, wie das Schild an der Ecke um 19 Uhr; quer darüber das dunkle Band mit dem Titel."""
    # Robert 31.10.2026: Momo (wf-raum) und Sängerin (saengerin) getauscht gegen Paar 3 aus _varianten/besuch-bildtausch: Tür und Coupes
    wand = [('fenster', '50% 55%'), ('tuer-rot', '50% 55%'), ('fw-h33', '50% 50%'), ('fe-negroni', '50% 40%'), ('dg-coupes', '50% 50%'), ('fw-h16', '50% 50%')]
    reihe = [3, 0, 5, 1, 4, 2]          # Reihenfolge, in der das Licht angeht
    f = ''.join('<figure class="lw-f" style="--lq:url(%s);--d:%.2fs">%s</figure>' % (
        mache(k)['lq'], .5 + reihe[j] * .38, img_tag(k, '(max-width:860px) 50vw, 34vw', True, ' style="object-position:%s"' % pos)) for j, (k, pos) in enumerate(wand))
    return '''<header class="lw auf" id="auftakt"><div class="lw-wand">%s</div>
<div class="lw-band"><div class="innen"><h1 class="titel lw-t">%s</h1><p class="text sw lw-s" style="--i:3">%s</p></div></div></header>''' % (f, zl(zeilen, i0=1), E(satz))


def kopf_plakate(satz):
    """Kopf der Programm-Seite (Wahl Robert 30.10.2026, _varianten/programm-hero-20 Fassung 3 «Die Plakatwand»): die acht neuesten
    SESSION-Plakate Kante an Kante als Wand, sie richten sich nacheinander auf; quer darüber ein dunkles Band mit dem Titel."""
    keys = []
    for d, n, r, k in LINEUP:
        if k not in keys:
            keys.append(k)
    wand = ''.join('<figure class="pw-f" style="--d:%d;--lq:url(%s)">%s</figure>' % (j, mache(k)['lq'], img_tag(k, '(max-width:900px) 50vw, 25vw', True)) for j, k in enumerate(keys[:8]))
    return '''<header class="pw auf" id="auftakt"><div class="pw-wand">%s</div>
<div class="pw-band"><div class="innen"><h1 class="titel pw-t">%s</h1><p class="text sw pw-s" style="--i:3">%s</p></div></div></header>''' % (wand, zl(['Lauter.'], i0=1), E(satz))


def kopf_theke(zeilen, satz):
    """Kopf der Seite «Das Haus» (Wahl Robert 31.10.2026: Fassung 5 «Das Licht der Theke» aus _varianten/haus-hero-15b, dazu eine Tapete):
    oben das Gewölbe (google-07 in voller Auflösung, höchstens zwei Drittel gross gezeigt), darunter der Titel auf der gelben Lichtkante der Theke,
    die sich von der Mitte nach aussen zieht; unter ihr spiegelt sich der Titel. Dahinter die Tapete aus dem Sonnenmedaillon des Gewölbes."""
    bildtag = ('<img class="th-b" src="assets/bild/haus-decke-weit-4284.webp?v=%s" srcset="assets/bild/haus-decke-weit-2142.webp?v=%s 2142w, '
               'assets/bild/haus-decke-weit-4284.webp?v=%s 4284w" sizes="100vw" alt="Das Gewölbe über der Bar, quer über den ganzen Raum" '
               'width="4284" height="1514" fetchpriority="high" decoding="async">') % (bau.V, bau.V, bau.V)
    return '''<header class="th auf" id="auftakt"><div class="th-o innen">%s</div>
<div class="th-m innen"><h1 class="titel th-t">%s</h1><div class="th-kante" aria-hidden="true"></div><div class="th-spiegel" aria-hidden="true"><div class="titel th-t">%s</div></div>
<p class="text sw th-s" style="--i:3">%s</p></div></header>''' % (bildtag, zl(zeilen, i0=1), zl(zeilen, i0=1), E(satz))


def fenster_kerzen():
    """Seit 31.10.2026 Bild 6 «Karte und Kerzenglas» aus _varianten/haus-fenster-15 (Fundus, per KI auf 4K nachgeschärft, Wahl Robert). Fenster direkt unter dem Kopf der Seite «Das Haus» (Robert 31.10.2026: «dann direkt Fenster einbauen nach hero»): die Wand mit Kerzennische
    und Wandlampen (google-52, unterer Teil, ohne Gäste, nicht die Decke). In voller Auflösung ausgeliefert, damit es auch am Retina-Schirm scharf bleibt."""
    from PIL import Image
    from bilder import _lq
    lq = _lq(Image.open('assets/bild/haus-fenster-karte-2048.webp').convert('RGB'))
    satz = ['Kerzenlicht', 'unter dem Gewölbe.']
    bildtag = ('<img src="assets/bild/haus-fenster-karte-4096.webp?v=%s" srcset="assets/bild/haus-fenster-karte-2048.webp?v=%s 2048w, assets/bild/haus-fenster-karte-4096.webp?v=%s 4096w" '
               'sizes="100vw" alt="Die Getränkekarte am Tisch, davor ein Kerzenglas" width="4096" height="2560" decoding="async" '
               'style="object-position:50%% 50%%">') % (bau.V, bau.V, bau.V)
    return '<section class="fk" aria-label="%s"><figure class="foto" style="--lq:url(%s)">%s<div class="fe-hof"></div><p class="fe-satz">%s</p></figure></section>' % (
        E(' '.join(satz)), lq, bildtag, zl(satz))


def platte_karte(k, etikett, titel, text, n=0, hell=False):
    return '<div class="platte karte leise%s" style="--n:%d">%s<span class="etikett">%s</span><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (
        ' hell' if hell else '', n, kachel(k, '', '30vw'), E(etikett), E(titel), E(text))


# ---------------------------------------------------------------- Drinks
def drinks():
    techniken = [('tafel-glaeser', 'Milk Washing', 'Milch bindet die Trübstoffe und wird wieder abgefiltert. Was bleibt, ist klar wie Wasser und weich wie Sahne. Momo macht das seit seiner Berliner Zeit, den Milchpunsch gab es schon 2021.'),
                 ('rueckbar', 'Fat Washing', 'Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel. Kalt gestellt, abgehoben, fertig: Der Rum schmeckt nach Butter, ohne fettig zu sein.'),
                 ('schaum', 'Enzyme', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt. So wird aus Apfel oder Birne ein klarer Saft, der sich in einen Drink giessen lässt wie Wasser.')]
    klassiker = [('Negroni', 'Gin, Wermut, Bitter, auf Eis gerührt. Der Schriftzug über der Vitrine ist kein Zufall: Den Negroni gibt es an jedem Abend.'),
                 ('Paloma', 'Tequila, Grapefruit, Limette und Soda. Im Sommer 2025 gab es ihm zu Ehren eine ganze Nacht.'),
                 ('Mexikaner', 'Der scharfe Shot des Hauses. An Geburtstagen der Bar und an Silvester gibt es ihn die ganze Nacht, Wild-Side-Tradition.'),
                 ('Ohne Alkohol', 'Shrub, Soda, Kräuter, klarer Saft: Momo baut jeden Drink auch ohne Alkohol, mit derselben Sorgfalt.')]
    karte = [('Frensh 26', 'Gin · Bergamotte · Nori · Schaumwein', '12'), ('Whey Bramble', 'Gin · Lemon Shrub · Vetiver · Whey Berry Soda', '12'),
             ('Pink Lady', 'Kakaobutter-Fat-Washed Rum · Himbeerpüree · Agave · Limette', '12'), ('Karamella', 'Havana 7 Jahre · Portwein · Johannisbeere · Karamell · schwarze Walnüsse · Limette', '12')]
    inhalt = kopf_glaeser(['Was magst du?'], 'Die Karte im Wild Side wechselt immer wieder, die Drinks dafür entwirft Momo. Und an der Bar sagst du, was du magst.')
    # «Das Gespräch» und «Wie Momo arbeitet» als EIN Faden, «Frage und Antwort» (Wahl Robert 30.10.2026: Fassung 02 aus _varianten/drinks-faden).
    # Der Faden ist Momos Stimme: jede Frage gross mit einer Goldlinie davor, und jedes Mal antworten Bilder, je Schritt mit eigener Bewegung (--p in wild.js).
    pos = {'dg-abseihen': '50% 45%', 'dg-giessen': '50% 45%'}

    def foto(k, sizes, cls='foto', stil=''):
        p = pos.get(k)
        return '<figure class="%s" style="--lq:url(%s);%s">%s</figure>' % (cls, mache(k)['lq'], stil, img_tag(k, sizes, extra=' style="object-position:%s"' % p if p else ''))

    def worte(t):
        return ' '.join('<span class="ww">%s</span>' % E(w) for w in t.split())

    def zeile(e, t):
        return '<div class="t2-zeile"><span class="etikett">%s</span><p class="titel t2-stimme">%s</p></div>' % (E(e), E(t))

    fragen = [('Der Geschmack', 'Lieber sauer, süss, bitter oder rauchig?'), ('Das Glas', 'Klar, cremig oder spritzig?'),
              ('Was hinein soll', 'Gin, Rum, Mezcal, Whisky oder ganz ohne Alkohol?')]
    h = '<section class="kap auf gx f02" id="gespraech" data-g="2"><div class="innen t2">'
    h += '<div class="t2-einstieg" data-p><div class="t2-spalte">%s<h2 class="titel t-gross">%s</h2><p class="text sw" style="--i:2">%s</p><div class="t2-s0" data-w><p class="titel t2-momo">%s</p><small>Momo Ben Khelifa</small></div></div><div class="t2-bild">%s</div></div>' % (
        kz('Das Gespräch', 'An der Theke', 0), zl(['Erst die Frage,', 'dann das Glas.'], i0=1),
        E('So läuft es an der Theke: Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll. Daraus wird ein Drink.'),
        worte('«Du sagst mir, was du magst, ich mache dir einen Drink.»'), foto('wf-raum', '(max-width:760px) 100vw, 42vw'))
    h += '<div class="t2-s1" data-p>%s<div class="t2-vier">%s</div></div>' % (zeile(*fragen[0]), ''.join(
        foto(k, '(max-width:760px) 50vw, 24vw', 'foto t2-karte', '--r:%ddeg;--j:%d' % (r, j)) for j, (k, r) in enumerate((('wf-sour', -7), ('wf-pink', 5), ('wf-zwei', -4), ('wf-erdbeer', 8)))))
    h += '<div class="t2-s2" data-p>%s<div class="t2-drei">%s</div></div>' % (zeile(*fragen[1]), ''.join(
        '<div class="t2-glas" style="--j:%d"><div class="t2-maske">%s</div><p class="titel">%s</p></div>' % (j, foto(k, '(max-width:760px) 33vw, 30vw'), w)
        for j, (k, w) in enumerate((('wf-nick', 'klar'), ('dg-schaumglas', 'cremig'), ('wf-highball', 'spritzig')))))
    h += '<div class="t2-s3" data-p>%s<div class="t2-fahrt">%s</div></div>' % (zeile(*fragen[2]), foto('dg-flaschen', '(max-width:760px) 100vw, 48vw'))
    h += '<section class="t2-t" id="technik"><div class="t2-s4" data-p><div class="t2-mitte"><i></i><p class="titel">Und so entsteht daraus ein Drink.</p><i></i></div><div class="t2-bkopf"><div>%s<h2 class="titel t-gross">%s</h2></div><p class="text sw" style="--i:2">%s</p></div></div>' % (
        kz('Wie Momo arbeitet', 'Drei Techniken', 0), zl(['Aus dem Labor', 'an die Theke.'], i0=1),
        E('Momo hat Biotechnologie studiert, bevor er hinter die Bar ging. Man schmeckt es: Drei Techniken aus dem Labor machen aus einer Idee einen klaren, weichen Drink.'))
    h += '<div class="t2-s5" data-p><div class="t2-kz">%s<p class="text">%s</p></div><div class="t2-paar">%s%s%s</div></div>' % (
        zeile('Technik', techniken[0][1]), E(techniken[0][2]), foto('dg-abseihen', '(max-width:760px) 100vw, 56vw', 'foto t2-p1'),
        foto('wf-tablett', '(max-width:760px) 50vw, 36vw', 'foto t2-p2', '--j:0'), foto('dg-siphon', '(max-width:760px) 50vw, 36vw', 'foto t2-p2', '--j:1'))
    h += '<div class="t2-s6" data-p><div class="t2-hoch">%s</div><div>%s<p class="text">%s</p></div></div>' % (
        foto('dg-behaelter', '(max-width:760px) 100vw, 40vw'), zeile('Technik', techniken[1][1]), E(techniken[1][2]))
    h += '<div class="t2-s7" data-p><div class="t2-kz">%s<p class="text">%s</p></div><div class="t2-vierer">%s</div></div>' % (
        zeile('Technik', techniken[2][1]), E(techniken[2][2]), ''.join(foto(k, '(max-width:760px) 50vw, %s' % w, 'foto t2-e', '--j:%d' % j)
            for j, (k, w) in enumerate((('dg-giessen', '56vw'), ('wf-klar', '40vw'), ('dg-feige', '40vw'), ('wf-coupe-tisch', '56vw')))))
    h += '</section></div></section>'
    inhalt += h
    inhalt += fenster_fest('wf-fe-tequila', ['Jeder Drink', 'ein Unikat.'], '50% 50%')   # Fenster in fester Grösse, Bild Nummer 12 (Robert 30.10.2026)
    # Klassiker: Fassung 3 «Das Band» (Robert 30.10.2026), jedes Glas schwebt einzeln hoch. Stand davor unter.py.vor-klassiker-band-2026-10-30
    kl_bild = [('fe-negroni', '50% 62%'), ('fe-highball', '45% 40%'), ('glas-kerze', '45% 60%'), ('fe-minze', '50% 35%')]
    inhalt += '''<section class="kap hell auf" id="klassiker"><div class="innen"><div class="kl-kopf"><div>%s%s</div>
<p class="text sw" style="--i:1">Wer lieber etwas Bekanntes will, bekommt es. Ein paar Drinks gehören fest zum Haus.</p></div></div>
<div class="kl-band auf">%s</div>
<div class="innen kl-liste staffel">%s</div></section>''' % (
        kz('Die Klassiker', 'Auch ohne Frage', 0), h2(['Und wer einen', 'Negroni will.']),
        ''.join('<figure class="kl-f" style="--n:%d;--lq:url(%s)">%s</figure>' % (n, mache(k)['lq'], img_tag(k, '(max-width:760px) 50vw, 25vw', extra=' style="object-position:%s"' % pos))
                for n, (k, pos) in enumerate(kl_bild)),
        ''.join('<div style="--n:%d"><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (n, E(t), E(s)) for n, (t, s) in enumerate(klassiker)))
    # Karte (Drunk in Love) raus: Kundin 30.10.2026, Robert 31.10.2026. Stand davor unter.py.vor-karte-raus-2026-10-31
    inhalt += fuss('tuer-rot')
    return rahmen('Drinks · Walk on the Wild Side Hannover', 'Die Karte wechselt, die Drinks entwirft Momo. Milk Washing, Fat Washing, Enzyme, Negroni, Paloma, alles auch ohne Alkohol.', inhalt, 'drinks.html')


# ---------------------------------------------------------------- Programm
def banderole():
    """Schmale Banderole über dem Beginn der Markise, wie bei Dirty Chicken: die Feste der Bar ausser Haus laufen langsam durch,
    dazwischen ein Glas in Gold (Robert 30.10.2026). Namen aus der Liste «aussen» der Programm-Seite."""
    glas = '<svg class="uw-glas" viewBox="0 0 24 30" aria-hidden="true"><path d="M3 3 H21 L12 14 Z M12 14 V26 M6 27 H18"/></svg>'
    namen = ['Oktoberfest des Event Klub', 'Christi Limmerfahrt', 'Südstadtfest', 'Smash n Mingle', 'Maschseefest', 'Die Bar ausser Haus']
    satz = '<p>%s</p>' % ''.join('<span>%s</span>%s' % (E(n), glas) for n in namen)
    return '<div class="uw-band"><div class="uw-band-zug">%s%s</div></div>' % (satz, satz)


def programm():
    woche = [('konzert', 'Donnerstag', 'Live, ab und zu', 'Kleine Konzerte mitten im Raum: Jazz, Soul, Pop. Duos und Trios, ohne Eintritt, ab 20 Uhr. 2024 und 2025 spielten Alone Together, Anissa Al Jay, Josseff and Friends und Sina and Friends.'),
             ('momo-lacht', 'Freitag', 'Momo an der Bar', 'Momo fragt, mixt und erzählt. Bis 2 Uhr.'),
             ('glas-trinkt', 'Samstag', 'Die DJ-Abende', 'Rund einmal im Monat legt jemand auf, von 21 bis 1 Uhr. Auf den Plakaten heisst die Reihe SESSION, gemeint sind Drinks und Musik an einem Abend.')]
    gaeste = [('gast-musa', '02.03.2024', 'Musa', 'Rebe & Brot, Hannover. Mit Momo hinter der Bar.'),
              ('gast-havn', '09.03.2024', 'Aus dem Havn', 'Eine Bartenderin aus dem Havn in Hannover, mit Momo.'),
              ('gast-nils', '20.04.2024', 'Nils Lutterbach', 'Lovis, Berlin. Vier Signature Drinks mit Freimeister Kollektiv.'),
              ('gast-cold', '25.05.2024', 'Cold Drinks and More', 'Ein alter Bekannter aus Berlin mit fünf eigenen Drinks.'),
              ('gast-enlil', '19.10.2024', 'Enlil Arevalo', 'Ein Name der Barszene in Hannover, fünf Signature Drinks.')]
    feste = [('silvester', '31. Dezember', 'Silvester ab mittags', '2024 als Frühschoppen von 12 bis 19 Uhr mit Buffet, 2025 von 12 bis 20 Uhr mit dem Foodtruck von Tru Story vor der Tür. Abends geht es weiter.'),
             ('voll', 'Im Winter', 'Der Geburtstag der Bar', 'Am 30. November 2024 wurde die neue Wild Side eins, am 5. Dezember 2025 zwei. Mit DJs, Mexikanern und einem Drink zur Begrüssung für die ersten Gäste.'),
             ('terrasse', '30. April', 'Tanz in den Mai', 'Mahir Maulud am Deck, Momo an der Bar, Eintritt frei. Wenn es warm ist, stehen die Tische vor der Tür.'),
             ('valentin', '14. Februar', 'Valentinstag', 'Mit Rudi von Culinarium: eine Karte mit vier Drinks und Tellern zum Teilen, die es nur an diesem Abend gibt.')]
    aussen = [('31.10. und 01.11.2026', 'Oktoberfest des Event Klub am Stephansplatz, 12 bis 21 Uhr, die Drinks kommen vom Wild Side', True),
              ('09.08.2026', 'Smash n Mingle beim HTV, mit Musa und Tru Story', False), ('13. und 14.06.2026', 'Südstadtfest, Cocktailstand mit dem Mon Bonheur', False),
              ('14. und 15.05.2026', 'Christi Limmerfahrt am Küchengarten', False), ('31.07.2025', 'Maschseefest, Stand Aresto x Lindenblatt', False)]
    inhalt = kopf_plakate('Donnerstags spielt ab und zu jemand live, samstags legen DJs auf, und manchmal steht ein Gast aus einer anderen Bar neben Momo. Das Programm der Woche.')
    # Fenster zwischen Plakatwand und Woche, damit es nach dem lauten Kopf ruhig wird (Robert 30.10.2026)
    inhalt += fenster_fest('pf-schild', ['Erst der Drink,', 'dann die Musik.'], '50% 40%')   # Bild Nummer 3 aus _varianten/programm-fenster
    # Die Woche (Wahl Robert 30.10.2026, _varianten/woche-mix15 Fassung 5, ohne «Tempi» und ohne Marke links): der Titel steckt auf einer
    # Stecktafel, die Buchstaben fallen einzeln in die Rillen; darunter drei runde Deckel mit Goldring, deren Ringe beim Scrollen weiterdrehen (wild.js).
    def tafel(zeilen):
        c, out = 0, ''
        for t, k in zeilen:
            z = ''
            for ch in t:
                z += '<span style="--b:%d">%s</span>' % (c, '&nbsp;' if ch == ' ' else E(ch)); c += 1
            out += '<p class="%s">%s</p>' % (k, z)
        # Glühbirnen rundherum wie an einem Kinoschild, im Uhrzeigersinn nummeriert, damit das Lauflicht umläuft
        oben, seite = 15, 5
        pos = [('calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (i / (oben - 1)), 'var(--wb)') for i in range(oben)]
        pos += [('calc(100% - var(--wb))', 'calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (i / (seite + 1))) for i in range(1, seite + 1)]
        pos += [('calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (1 - i / (oben - 1)), 'calc(100% - var(--wb))') for i in range(oben)]
        pos += [('var(--wb)', 'calc(var(--wb) + (100%% - 2 * var(--wb)) * %f)' % (1 - i / (seite + 1))) for i in range(1, seite + 1)]
        birnen = ''.join('<i class="wo-birne" style="left:%s;top:%s;--k:%d;--j:%d"></i>' % (x, y, j % 3, j) for j, (x, y) in enumerate(pos))
        return '<div class="wo-tafel" aria-hidden="true">%s<div class="wo-rillen">%s</div></div>' % (birnen, out)

    def deckel(j, k, t):
        pid = 'wo-r%d' % j
        return '''<div class="wo-deckel"><figure class="wo-bild" style="--lq:url(%s)">%s</figure><svg class="wo-ring" viewBox="0 0 300 300" aria-hidden="true"><defs><path id="%s" d="M150,150 m-128,0 a128,128 0 1,1 256,0 a128,128 0 1,1 -256,0"/></defs>
<circle cx="150" cy="150" r="146"/><circle cx="150" cy="150" r="112"/><text><textPath href="#%s" textLength="796" lengthAdjust="spacing">%s</textPath></text></svg></div>''' % (
            mache(k)['lq'], img_tag(k, '(max-width:760px) 70vw, 22vw', extra=' style="object-position:%s"' % {'konzert': '58% 50%', 'momo-lacht': '50% 42%', 'glas-trinkt': '45% 40%'}.get(k, '50% 50%')), pid, pid, E(('%s · WALK ON THE WILD SIDE · ' % t.upper()) * 2))
    inhalt += '''<section class="kap auf wo wo-tapete" id="woche"><div class="innen"><h2 class="wo-sr">Die Woche. Drei Abende.</h2>%s
<div class="wo-reihe">%s</div></div></section>''' % (
        tafel([('DIE WOCHE', 'rot'), ('DREI ABENDE.', '')]),
        ''.join('<article class="wo-spalte" data-ring="%d">%s<h3 class="titel wo-name">%s</h3><span class="etikett">%s</span><p class="text">%s</p></article>' % (
            j, deckel(j, k, t), E(t), E(u), E(s)) for j, (k, t, u, s) in enumerate(woche)))
    # Die DJ-Abende (Wahl Robert 30.10.2026, _varianten/session-15 Fassung 7 «Der Kontaktbogen»): links ein grosses Plakat auf Creme,
    # rechts Text und alle Plakate klein wie auf einem Kontaktbogen. Zeigen auf ein kleines: das grosse sinkt weg, das neue steigt auf (wild.js).
    plakate = []                                     # je Plakat einmal, neuester Abend zuerst
    for d, n, r, k in LINEUP:
        for p in plakate:
            if p[0] == k:
                p[1].append((d, n, r)); break
        else:
            plakate.append((k, [(d, n, r)]))

    def p_datum(ab):
        return ' und '.join(d[:6] for d, n, r in ab[::-1])[:-1] + ab[0][0][5:] if len(ab) > 1 else ab[0][0]

    def p_name(ab):
        return ', '.join(n for d, n, r in ab[::-1])

    def sp(k, sizes, cls='', extra=''):
        return '<figure class="sp %s" style="--lq:url(%s)"%s>%s</figure>' % (cls, mache(k)['lq'], extra, img_tag(k, sizes))
    gross = ''.join(sp(k, '(max-width:760px) 92vw, 40vw', 'kb-g' + (' an' if j == 0 else ''), ' data-k="%s"' % k) for j, (k, ab) in enumerate(plakate))
    klein = ''.join('<div class="kb-k%s" data-k="%s" data-dat="%s" data-name="%s" style="--n:%d">%s<p>%s</p></div>' % (
        ' an' if j == 0 else '', k, E(p_datum(ab)), E(p_name(ab)), j, sp(k, '(max-width:760px) 22vw, 9vw'), E(p_datum(ab))) for j, (k, ab) in enumerate(plakate))
    inhalt += '''<section class="kap auf" id="session"><div class="innen"><div class="kb-raster">
<div class="kb-gross"><div class="kb-bild">%s</div><div class="kb-unten"><span class="etikett">Die DJ-Abende der Bar · samstags 21 bis 1 Uhr</span><p class="kb-name titel">%s</p><p class="kb-dat">%s</p></div></div>
<div>%s%s<p class="text sw" style="--i:1">Seit September 2025 holt das Wild Side DJs an die Bar. Jeder Abend bekommt ein eigenes Plakat mit rot-cremefarbenen Wellen und dem Gesicht des Abends in Schwarzweiss. Zeig auf einen Abend, dann siehst du sein Plakat. Den nächsten kündigt die Bar auf Instagram an.</p>
<div class="kb-bogen" data-kontaktbogen>%s</div></div></div>
<div class="knoepfe sw" style="--i:3;margin-top:34px">%s</div></div></section>''' % (
        gross, E(p_name(plakate[0][1])), E(p_datum(plakate[0][1])), kz('Samstags', 'Die DJ-Abende', 0), h2(['Jeder Abend', 'ein Plakat.']), klein, knopf('Instagram der Bar', HAUS['instagram']))
    # Gastschichten (Wahl Robert 30.10.2026, _varianten/gaeste-15b Fassung 23 «Verdeckte Karten»): fünf Karten liegen verdeckt,
    # Rückseite schwarz mit Goldlinie und dem Namen der Bar; kommt die Reihe ins Bild, dreht sich eine nach der anderen um (nur CSS).
    inhalt += '''<section class="kap auf" id="gaeste"><div class="innen"><div class="vk-kopf">%s%s
<p class="text sw" style="--i:1">An manchen Abenden steht neben Momo jemand aus einer anderen Bar, aus Hannover oder Berlin, und bringt eigene Drinks mit. Fünf Gastschichten aus dem Jahr 2024.</p></div>
<div class="vk-reihe auf">%s</div></div></section>''' % (
        kz('Gäste hinterm Tresen', 'Gastschichten', 0), h2(['Jemand anderes', 'am Shaker.']),
        ''.join('<article class="vk-p" style="--n:%d"><div class="vk-karte"><div class="vk-rueck" aria-hidden="true"><span>WALK ON THE</span><b>WILD SIDE</b><span>GASTSCHICHT</span></div><div class="vk-vorn"><figure class="vk-bild" style="--lq:url(%s)">%s</figure></div></div><div class="vk-satz"><span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p></div></article>' % (
            n, mache(k)['lq'], img_tag(k, '(max-width:760px) 44vw, 19vw'), E(d), E(t), E(s)) for n, (k, d, t, s) in enumerate(gaeste)))
    inhalt += fenster_fest('konzert-scharf', ['Gute Drinks,', 'gute Musik.'], '50% 50%')   # seit 30.10.2026 Fenster in fester Grösse (Robert)
    inhalt += '''<section class="kap hell auf" id="feste"><div class="innen">%s%s
<div class="vier staffel" style="margin-top:34px">%s</div></div></section>''' % (
        kz('Die Feste', 'Vier im Jahr', 0), h2(['Vier Abende, die', 'jedes Jahr kommen.']),
        ''.join(platte_karte(k, d, t, s, n, True) for n, (k, d, t, s) in enumerate(feste)))
    # Unterwegs (Wahl Robert 30.10.2026, _varianten/unterwegs-15 Fassung 4 «Die Markise»): oben rollt die rot-cremefarbene Markise eines Standes aus,
    # links fünf Fotos von der Christi Limmerfahrt Wand an Wand (der Stand der Bar), rechts der Text gross und hell.
    wand = [('fw-a45', 'uw-a', '50% 30%'), ('fw-a46', 'uw-b', '50% 40%'), ('uw-singen', 'uw-c', '50% 30%'), ('uw-tanz', 'uw-d', '50% 45%'), ('uw-sonne', 'uw-e', '50% 40%')]
    inhalt += '''<section class="kap auf uw-m" id="unterwegs"><div class="uw-markise" aria-hidden="true"><div class="uw-tuch"></div>%s</div><div class="innen uw-stand">
<div class="uw-wand">%s</div>
<div class="uw-text">%s%s<p class="text sw" style="--i:1">Ein paar Mal im Jahr steht die Bar vor der Tür oder ganz woanders: beim Kiezfest am Küchengarten, am Maschsee, im Oktober auf dem Oktoberfest des Event Klub. Und wer selbst etwas Grösseres plant: Die Bar kommt mit, in externe Locations wie die Loge, mit dem ganzen Konzept. <a href="tafel.html#events" style="color:var(--gold)">Mehr unter Feiern</a>.</p>
<div class="zeilen sw" style="--i:2">%s</div></div></div></section>''' % (
        banderole(),
        ''.join('<figure class="uw-f %s" style="--n:%d;--lq:url(%s)">%s</figure>' % (c, n, mache(k)['lq'], img_tag(k, '(max-width:900px) 46vw, 24vw', extra=' style="object-position:%s"' % pos)) for n, (k, c, pos) in enumerate(wand)),
        kz('Unterwegs', 'Die Bar ausser Haus', 0), h2(['Und manchmal', 'draussen.']),
        ''.join('<div><span class="etikett">%s</span><span>%s%s</span></div>' % (E(d), E(s), '') for d, s, b in aussen))
    inhalt += fuss('schild')
    return rahmen('Programm · Walk on the Wild Side Hannover', 'DJ-Abende, Konzerte am Donnerstag, Gastschichten und die Feste der Bar: Silvester, Geburtstag, Tanz in den Mai, Valentinstag.', inhalt, 'programm.html')


# ---------------------------------------------------------------- Feiern (bis 30.10.2026 «Die lange Tafel»)
# Inhalte aus der Angebotsmappe der Bar (_quelle/angebote-pdf/Wild Side Angebote.pdf, Robert 30.10.2026). Preise brutto, wörtlich übernommen.
PREISE = [('Signature Drinks', '12,00'), ('Alkoholfreie Drinks', '11,00'), ('Longdrinks', '10,00'), ('Wein und Spritz', '8,00'),
          ('Sekt auf Eis', '6,00'), ('Bier', '4,00'), ('Alkoholfreie Getränke', '3,00')]
PAUSCHALE = [('Kategorie 1', 'Bier, Wein, Spritz', 'Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke', '49'),
             ('Kategorie 2', 'Dazu Longdrinks', 'Longdrinks · Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke', '59'),
             ('Kategorie 3', 'Dazu fünf Signature Cocktails', 'Fünf Signature Cocktails · Longdrinks · Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke', '79')]


def kopf_feiern():
    """Kopf der Feiern-Seite: drei hohe Bilder Wand an Wand (Tafel, Feier, Musik) steigen aus verschiedenen Tiefen, darüber der Titel breit."""
    tafeln = [('an-empore', '50% 55%'), ('an-party', '50% 30%'), ('an-dj', '50% 50%')]
    t = ''.join('<figure class="fr-t" style="--n:%d;--lq:url(%s)">%s</figure>' % (n, mache(k)['lq'], img_tag(k, '(max-width:760px) 100vw, 34vw', True, ' style="object-position:%s"' % pos))
                for n, (k, pos) in enumerate(tafeln))
    return '''<header class="fr-kopf auf" id="auftakt"><div class="fr-trip">%s</div><div class="fr-hof"></div>
<div class="innen"><span class="etikett fr-et">Feiern im Wild Side</span><h1 class="titel">%s</h1><p class="text">%s</p></div></header>''' % (
        t, zl(['Euer Abend.'], i0=1), 'Ein Dinner an der langen Tafel, die ganze Bar für eure Gesellschaft, Musik, die zum Abend passt. Derya und Momo planen ihn mit euch, vom ersten Drink bis zum letzten Lied.')


def strahl():
    """Wie viele seid ihr: die Karte der Formate wie die Preisliste der Bar, vom Namen zieht sich eine Punktlinie zur Gästezahl;
    daneben das Bild der Empore (Robert 30.10.2026, Fassung 10 aus _varianten/feiern-15/wieviele)."""
    formate = [('#dinner', 'Mit Rudi und Momo', 'Privates Dinner', '10 bis 14 Gäste'), ('#tafel', 'Mit eigenem Budget', 'Die lange Tafel', '10 bis 20 Gäste'),
               ('#bar', 'Geschlossene Gesellschaft', 'Die ganze Bar', 'ab 30 Gästen')]
    z = ''.join('<a class="fr-wz" href="%s" style="--n:%d"><span class="fr-wn"><span class="etikett">%s</span><b class="titel">%s</b></span><i class="fr-wp"></i><b class="fr-wg titel">%s</b></a>' % (h, n, E(u), E(t), E(g))
                for n, (h, u, t, g) in enumerate(formate))
    return '''<section class="kap auf" id="wieviele"><div class="innen fr-wraster">
<div class="fr-wkarte hell auf"><svg class="fr-rahmen" aria-hidden="true"><rect x="8" y="8" rx="6" ry="6" pathLength="100"/></svg>
<div class="fr-wkopf">%s%s<p class="text sw" style="--i:1">Für jede Runde gibt es den passenden Rahmen. Wählt euer Format, die Seite führt euch hin.</p></div>
<div class="fr-wzeilen">%s</div></div>%s</div></section>''' % (
        kz('Wie viele seid ihr?', 'Drei Formate', 0), h2(['Vom Dinner', 'bis zur ganzen Bar.']), z,
        bild('an-empore', 'foto fr-wbild auf', '(max-width:900px) 92vw, 36vw'))


def tafel():
    inhalt = kopf_feiern()
    inhalt += strahl()
    # Privates Dinner: acht Bilder vom Abend Wand an Wand, mittendrin Titel und Knopf als dunkle Fläche; darunter Satz und Gänge
    # (Robert 30.10.2026, Fassung 7 aus _varianten/feiern-15/dinner)
    gaenge = [('Zum Anfang', 'Ein Gruss aus der Küche'), ('Drei Gänge', 'Ein vegetarisches Menü von Rudi'), ('Im Glas', 'Fünf Drinks von Momo, auf die Gänge abgestimmt')]
    wand = ['an-dinner', 'tf-h2', 'tf-oben', 'tf-l8', 'pf-momo-rudi', 'tf-dessert', 'tafel-glaeser', 'tf-l3']
    feld = ['1/1/3/2', '1/2/2/3', '1/3/2/4', '1/4/3/5', '3/1/4/2', '3/2/4/3', '3/3/4/4', '3/4/4/5']
    inhalt += '''<section class="kap auf" id="dinner"><div class="innen">
<div class="fr-dwand auf">%s<div class="fr-dwtext">%s%s<div class="knoepfe">%s</div></div></div>
<div class="fr-dwunten"><p class="text sw" style="--i:1">Ein exklusiver Abend für zehn bis vierzehn Gäste an der langen Tafel, mit Rudi in der Küche und Momo an der Bar. Für Geburtstage, kleine Weihnachtsfeiern, Junggesellenabschiede oder einen Abend mit den Menschen, die zählen.</p>
<div class="fr-dwg">%s</div></div></div></section>''' % (
        ''.join(bild(k, 'foto fr-dwf', '(max-width:760px) 46vw, 24vw', stil='grid-area:%s;--n:%d' % (f, n)) for n, (k, f) in enumerate(zip(wand, feld))),
        kz('Privates Dinner', 'Mit Rudi und Momo', 0), h2(['Zehn bis vierzehn', 'Gäste, ein Menü.']), knopf('Dinner anfragen', '#anfragen', 'rot'),
        ''.join('<div style="--n:%d"><span class="etikett">%s</span><p>%s</p></div>' % (n, E(a), E(b)) for n, (a, b) in enumerate(gaenge)))
    # Die lange Tafel als Platte (Robert 30.10.2026, Fassung 14 aus _varianten/empore-15): Bild und Text auf einer dunklen Platte, die Zahlen als ihr Fuss
    zahlen = [('10–20', 'Gäste an der Tafel'), ('4', 'Stunden auf der Empore'), ('0 €', 'für Service und Raum')]
    inhalt += '''<section class="kap auf fr-pl" id="tafel"><div class="innen"><div class="fr-plplatte"><div class="fr-plg">
%s
<div class="fr-plt">%s%s<p class="text sw" style="--i:1">Oben auf der kleinen Empore steht die lange Tafel. Vier Stunden gehört sie eurer Runde, unten läuft die Bar weiter. Ihr legt vorher ein Budget für die Drinks fest; ist es erreicht, stockt ihr auf, oder eure Gäste bestellen selbst weiter.</p>
<div class="knoepfe sw" style="--i:3">%s</div></div></div>
<div class="fr-plfuss">%s</div></div></div></section>''' % (
        bild('an-empore-tafel', 'fr-plbild', '(max-width:900px) 92vw, 42vw', extra=' style="object-position:50% 50%"'),
        kz('Die lange Tafel', 'Mit eigenem Budget', 0), h2(['Die Empore', 'gehört euch.']),
        knopf('Tafel anfragen', '#anfragen', 'rot'),
        ''.join('<div class="fr-plz" style="--n:%d"><b class="titel">%s</b><span class="etikett">%s</span></div>' % (n, E(z), E(t)) for n, (z, t) in enumerate(zahlen)))
    inhalt += fenster_fest('tafel-glaeser', ['Momo mixt', 'für den ganzen Tisch.'], '50% 50%')   # seit 30.10.2026 Fenster in fester Grösse mit Schatten hinter dem Satz (Robert)
    # Die ganze Bar, seit 30.10.2026 «Das Schild an der Tür» (Wahl Robert: Fassung 3 aus _varianten/feiern-bar-15): links Feier und Pauschale,
    # rechts schwingt an zwei Schnüren das Schild «Geschlossene Gesellschaft» ein; darunter je Kategorie ein Foto mit Name, Liste und Preis
    glas = ['an-glaeser', 'wf-highball', 'an-negroni']
    karten = ''.join('<div class="fr-sk" style="--n:%d">%s<span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p><div class="fr-spreis"><b class="titel">%s €</b><small>pro Person</small></div></div>' % (
        n, bild(g, 'fr-sf', '(max-width:900px) 92vw, 30vw'), E(k), E(t), E(z), p) for n, (g, (k, t, z, p)) in enumerate(zip(glas, PAUSCHALE)))
    inhalt += '''<section class="kap auf" id="bar"><div class="innen">
<div class="fr-soben"><div><div class="fr-bkopf">%s%s<p class="text sw" style="--i:1">Ab dreissig Gästen schliesst die Bar für euch. Von 19 bis 2 Uhr gehört euch der ganze Raum: unter der Decke, an der Theke, auf der Empore. Für Hochzeit mit Party, Geburtstag, Firmenfeier, Weihnachtsfeier oder ein Gastro-Event, jeder Abend individuell gestaltet. Zwei Wege, den Abend zu planen.</p></div>
<div class="fr-mkopf sw" style="--i:2"><span class="etikett">Weg 1 · Pauschale</span><h3 class="titel t-mittel">Ein Preis pro Gast.</h3><p class="text">Von 19 bis 2 Uhr steht offen, was eure Kategorie umfasst. Wer länger bleibt: ab 2 Uhr jede angefangene Stunde 10 Euro pro Person.</p></div></div>
<div class="fr-haken auf"><i class="fr-schnur fr-sl"></i><i class="fr-schnur fr-sr"></i><div class="fr-schild"><span class="etikett">Die ganze Bar</span><p class="titel">Geschlossene Gesellschaft</p><small>Von 19 bis 2 Uhr</small></div></div></div>
<div class="fr-sreihe auf">%s</div></div></section>''' % (
        kz('Die ganze Bar', 'Geschlossene Gesellschaft', 0), h2(['Eine Nacht,', 'nur für euch.']), karten)
    # Weg 2 Budget, seit 30.10.2026 «Vor der Rückbar» (Wahl Robert: Fassung 6 aus _varianten/budget-15): links hochkant die Rückbar,
    # die beim Scrollen in ihrem Rahmen ruhig näher rückt; rechts Text, die zwei Beträge und die Preise als offene Liste. Namen brechen nie um.
    preise = ''.join('<div class="rb-p" style="--n:%d"><span>%s</span><i></i><b class="titel">%s €</b></div>' % (n, E(t), p) for n, (t, p) in enumerate(PREISE))
    inhalt += '''<section class="kap auf" id="budget"><div class="innen rb-raster">
<div class="rb-bild" data-nah>%s</div>
<div>%s%s<p class="text sw" style="--i:1">Für Service und Raum gibt es einen festen Betrag, für die Drinks setzt ihr vorher einen Rahmen. Ist er erreicht, stockt ihr auf, oder eure Gäste übernehmen ihre weiteren Bestellungen selbst. So bleibt der Abend offen und die Rechnung klar.</p>
<div class="rb-betraege sw" style="--i:2"><div><span class="etikett">Service und Raum</span><b class="titel">500 €</b></div><div><span class="etikett">Euer Budget für Drinks</span><b class="titel">ab 1.000 €</b></div></div>
<p class="rb-klein">Geschlossene Gesellschaft ab 30 Personen, 19 bis 2 Uhr. Das Budget lässt sich nach oben frei anpassen.</p>
<div class="rb-liste sw" style="--i:3"><span class="etikett">Was ein Drink kostet</span><h3 class="titel">Die Preise der Bar.</h3><div class="rb-posten">%s</div><small>Gilt für das Budget an der langen Tafel und in der ganzen Bar. Alle Preise brutto.</small></div></div>
</div></section>''' % (bild('flaschen', 'rb-f', '(max-width:900px) 92vw, 40vw', extra=' style="object-position:50% 50%"'),
                        kz('Weg 2 · Budget', 'Flexibel mit festem Rahmen', 0), h2(['Ein Rahmen,', 'den ihr setzt.']), preise)
    # Musik: eine goldene Schallwelle läuft durch den Abschnitt, die drei Bilder sitzen auf verschiedenen Höhen darauf (Wahl Robert 30.10.2026, Fassung 8).
    # Erst zeichnet sich die Welle von links nach rechts, dann steigen die drei nacheinander auf.
    musik = [('an-dj', '50% 50%', 'DJ', 'Erst leise im Hintergrund, später zum Tanzen.'), ('saengerin', '50% 35%', 'Gesang', 'Eine Stimme mitten im Raum.'), ('konzert-love', '50% 40%', 'Jazz', 'Ein Duo oder Trio für den ruhigeren Abend.')]
    wellen = ''.join('<article class="fr-mwp" style="--n:%d"><figure class="fr-mwb" style="--lq:url(%s)">%s</figure><span class="etikett">%s</span><h3 class="titel">%s</h3></article>' % (
        n, mache(k)['lq'], img_tag(k, '(max-width:760px) 80vw, 24vw', extra=' style="object-position:%s"' % pos), E(t), E(s)) for n, (k, pos, t, s) in enumerate(musik))
    welle = '<svg class="fr-mwsvg" viewBox="0 0 1200 200" preserveAspectRatio="none" aria-hidden="true"><path d="M0 100 C 100 20, 200 20, 300 100 S 500 180, 600 100 S 800 20, 900 100 S 1100 180, 1200 100"/></svg>'
    inhalt += '''<section class="kap auf" id="musik"><div class="innen">
<div class="fr-mkopf2"><div>%s%s</div><p class="text sw" style="--i:1">Ihr sucht noch einen DJ, Live-Musik, Gesang oder Jazz? Die Bar ergänzt euren Abend mit der passenden Begleitung und greift dabei auf ein grosses Repertoire zurück, auch auf die Musikerinnen und Musiker, die sonst donnerstags und samstags hier spielen.</p></div>
<div class="fr-mwelle auf"><div class="fr-mwspur">%s<i class="fr-mwdeck"></i></div>%s</div></div></section>''' % (kz('Musik', 'Für euren Abend', 0), h2(['Der Klang', 'dazu.']), welle, wellen)
    # Grosse Events ausser Haus: geschlossenes Raster (Wahl Robert 30.10.2026, Fassung 7 aus _varianten/events-15b). Die Theke hoch links, rechts oben der Text
    # auf einer Platte, darunter Loge und Gläser; alle Kanten bündig. Die Felder setzen sich nacheinander aus der Tiefe an ihren Platz. Stand davor *.vor-events-raster-2026-10-30
    def er_bild(k, cls, sizes):
        return '<figure class="fr-erf %s" style="--lq:url(%s)">%s</figure>' % (cls, mache(k)['lq'], img_tag(k, sizes))
    inhalt += '''<section class="kap auf" id="events"><div class="innen">
<div class="fr-erraster auf">%s<div class="fr-erplatte platte"><div class="fr-etext">%s%s<p class="text sw" style="--i:1">Für grössere Veranstaltungen zieht die Bar um, in externe Locations wie die Loge. Derya und Momo übernehmen die Organisation und kümmern sich um das ganze Konzept, von der Bar bis zum Ablauf des Abends.</p><p class="fr-klein sw" style="--i:2">Infos auf Anfrage.</p><div class="knoepfe sw" style="--i:3;margin-top:26px">%s</div></div></div>%s%s</div>
</div></section>''' % (er_bild('ev-theke', 'fr-er-a', '(max-width:760px) 90vw, 30vw'), kz('Grosse Events', 'Ausser Haus', 0), h2(['Grösser als', 'die Bar.']), knopf('Event anfragen', '#anfragen'),
                       er_bild('an-loge', 'fr-er-b', '(max-width:760px) 45vw, 30vw'), er_bild('an-glaeser', 'fr-er-c', '(max-width:760px) 45vw, 30vw'))
    ablauf = [('Anfragen', 'Ihr schreibt, was ihr vorhabt: Anlass, Datum, wie viele ihr seid.'),
              ('Angebot', 'Derya und Momo melden sich mit einem Vorschlag, nur für euch.'),
              ('Anzahlung', 'Bei jedem Abend 30 Prozent eine Woche vorher, der Rest am Abend vor Beginn.'),
              ('Abend', 'Ihr kommt um 19 Uhr, alles ist bereit, Momo hat die Gläser kalt gestellt.')]
    # Die Goldlinie (Wahl Robert 30.10.2026, Fassung 3 aus _varianten/ablauf-15): vier Bilder in einer Reihe, darunter eine Linie über die ganze Breite,
    # die sich beim Scrollen zieht; jede Station leuchtet auf, wenn die Linie sie erreicht. Stand davor *.vor-ablauf-goldlinie-2026-10-30
    ab_bild = [('fw-a55', '50% 55%'), ('an-team', '50% 35%'), ('fw-tafel', '50% 50%'), ('tafel-glaeser', '50% 45%')]
    stationen = ''.join('<div class="gl-st" data-j="%d"><figure class="gl-b" style="--lq:url(%s)">%s</figure><i class="gl-p"></i><h3 class="titel">%s</h3><p>%s</p></div>' % (
        n, mache(k)['lq'], img_tag(k, '(max-width:760px) 92vw, 26vw', extra=' style="object-position:%s"' % pos), E(t), E(s)) for n, ((t, s), (k, pos)) in enumerate(zip(ablauf, ab_bild)))
    inhalt += fenster_fest('ft-raum-abend', ['Eure Leute,', 'Momos Drinks.'], '50% 50%')   # Fenster zwischen Events und Ablauf, Bild 1 (Robert 30.10.2026)
    inhalt += '''<section class="kap hell auf" id="ablauf"><div class="innen">
<div class="gl-kopf">%s%s</div>
<div class="gl-weg"><div class="gl-linie"><i></i></div>%s</div></div></section>''' % (
        kz('So geht es', 'Vier Schritte', 0), h2(['Ihr erzählt,', 'wir bereiten vor.']), stationen)
    inhalt += '''<section class="kap auf" id="anfragen"><div class="innen">
<div class="fr-team auf" data-p><div class="fr-tb"><figure class="fr-tbild" style="--lq:url(%s)">%s</figure></div><div class="fr-ttafel"><span class="etikett">Ansprechpartner · Momo und Derya</span><p class="titel">%s</p></div></div>
<div class="zwei" style="margin-top:clamp(40px,5vw,72px);align-items:start">
<div class="fr-alinks">%s<p class="text sw" style="--i:1">Schreibt, was ihr vorhabt. Derya und Momo melden sich mit einem Angebot. Noch schneller geht es telefonisch:</p>
<div class="zeilen sw" style="--i:2">%s</div>
<p class="text sw" style="--i:3;margin-top:22px">Ohne eigene Runde: An einzelnen Wochenenden öffnet <a href="%s" style="color:var(--gold)">Culinarium</a> die lange Tafel für alle, mit Menü und Tickets.</p></div>
<form class="platte formular sw" style="--i:2" data-vorfuehrung>
<div class="feld reihe"><label><span>Format</span><select name="format"><option>Privates Dinner</option><option>Die lange Tafel</option><option>Die ganze Bar</option><option>Grosses Event ausser Haus</option></select></label><label><span>Datum</span><input type="date" name="datum"></label></div>
<div class="feld reihe"><label><span>Wie viele</span><input type="number" name="gaeste" min="10" placeholder="z. B. 16"></label><label><span>Anlass</span><select name="anlass"><option>Geburtstag</option><option>Firmenfeier</option><option>Weihnachtsfeier</option><option>Junggesellenabschied</option><option>Ein besonderer Abend</option></select></label></div>
<div class="feld reihe"><label><span>Musik dazu</span><select name="musik"><option>Ohne</option><option>DJ</option><option>Gesang</option><option>Jazz</option></select></label><label><span>Name</span><input type="text" name="name"></label></div>
<label class="feld"><span>E-Mail oder Telefon</span><input type="text" name="kontakt"></label>
<label class="feld"><span>Was habt ihr vor?</span><textarea name="text"></textarea></label>
<div class="fuss-f"><button class="knopf rot" type="submit"><span>Anfrage senden</span><i>%s</i></button><span class="hinweis">Vorführung: In diesem Entwurf wird nichts verschickt.</span></div>
<p class="dank">Danke. Derya und Momo melden sich mit einem Angebot für euren Abend.</p>
</form></div></div></section>''' % (
        mache('an-team')['lq'], img_tag('an-team', '(max-width:900px) 100vw, 1000px', extra=' style="object-position:50% 30%"'), zl(['Lasst uns euren Abend', 'gemeinsam gestalten.']),
        kz('Anfragen', 'Euer Abend', 0),
        ''.join('<div><span class="etikett">%s</span><span>%s</span></div>' % (E(a), b) for a, b in [
            ('Telefon', '<a href="tel:%s">%s</a>' % (HAUS['tel_href'], E(HAUS['telefon']))),
            ('Telefon', '<a href="tel:%s">%s</a>' % (HAUS['tel2_href'], E(HAUS['telefon2']))),
            ('Instagram', '<a href="%s" rel="noopener">%s</a>' % (HAUS['instagram'], E(HAUS['ig_name'])))]),
        HAUS['culinarium'],
        PFEIL)
    inhalt += fuss('rueckbar')
    return rahmen('Feiern · Walk on the Wild Side Hannover', 'Privates Dinner für 10 bis 14 Gäste, die lange Tafel für 10 bis 20, die ganze Bar ab 30 Gästen von 19 bis 2 Uhr, Musik dazu und grosse Events ausser Haus. Preise und Anfrage.', inhalt, 'tafel.html', 'feiern')


# ---------------------------------------------------------------- Das Haus
def haus():
    # «Dein Platz» (Wahl Robert 31.10.2026, _varianten/platz Fassung 1 «Vier Spalten»): der Raum aus Sicht des Gastes, vier Plätze nebeneinander.
    # Belege: Theke/Momo fragt (Steckbrief Momo), Barhocker, Holztische, Polsterbank, Messingleuchten, Kerzen (_quelle/research_notes/…/menschen_geschichte_presse_raum.md),
    # Empore und Culinarium (Feiern), Tische vor der Tür (Besuch).
    plaetze = [('pl-theke', 'An der Theke', 'Auf den Hockern an der Theke bist du am nächsten dran. Momo fragt, was du magst, und mixt daraus deinen Drink. Unter der Kante leuchtet das gelbe Lichtband.', '55% 45%'),
               ('pl-tisch', 'Am Tisch', 'Holztische und eine Polsterbank an hellen Wänden, darüber Messingleuchten, auf dem Tisch Kerzenlicht. Hier sitzt ihr zu zweit oder in der Runde, unter dem Gewölbe.', '50% 60%'),
               ('pl-empore', 'Auf der Empore', 'Oben auf der kleinen Empore steht die lange Tafel. Zehn bis zwanzig Gäste feiern dort ihren Abend, unten läuft die Bar weiter. An einzelnen Wochenenden deckt Culinarium hier ein Menü für alle.', '50% 70%'),
               ('pl-ecke', 'Draussen an der Ecke', 'Wenn es warm ist, stehen Tische vor der Tür, an der Ecke Haasemannstraße und Rampenstraße. Drinnen läuft die Bar, draussen der Abend in Linden.', '35% 60%')]
    derya = [('2023', 'Übernimmt die Bar im Herbst, Wiedereröffnung am 9. November.'), ('2024', 'Die Neue Presse besucht sie an der Theke, Continental Sour im Glas.'), ('heute', 'Führt die Bar und die Abende von Culinarium mit.')]
    momo = [('1988', 'Geboren in Tunis, seit 2008 in Hannover.'), ('2014', 'Nach dem Master in Biotechnologie in die Bars von Berlin.'), ('2018', 'Barchef im Lindenblatt, Mitgründer der ProBierBar in Linden.'), ('2023', 'Mit Derya im Wild Side, er entwirft die Drinks.')]
    jahre = [('2018', 'Momo ist in Linden zu Hause, zuerst mit der Probierbar an der Limmerstraße. Danach kommt das gemeinsame Baby von Derya und Momo: das Wild Side.'),   # Wunsch der Bar 30.10.2026
             ('2023', 'Am 9. November machen Derya Ivkin und Momo Ben Khelifa die Bar wieder auf. Relaunch-Party am 1. Dezember, seitdem Nachbarschafts-Mixology-Bar. Dazu Stadtfeste wie die Christi Limmerfahrt und das Südstadtfest, mit Partnern aus der Gastronomie.'),
             ('2024', 'Gastschichten aus Hannover und Berlin, Konzerte am Donnerstag, am 30. November der erste Geburtstag.'),
             ('2025', 'Im September beginnen die DJ-Abende. Am 5. Dezember wird die neue Wild Side zwei.'),
             ('2027', 'Der Falstaff Bar Guide 2027 führt das Wild Side mit 91 Punkten unter den Cocktailbars.')]
    stimmen = [('91', 'Falstaff Bar Guide 2027', 'Cocktailbars: 47 von 50 für die Drinks, 18 von 20 für Stil und Service.'),
               ('4,8', 'Google, 75 Bewertungen', 'Gelobt werden die Beratung ohne Karte, Momo mit Namen und die kleine, gemütliche Bar.'),
               ('4,8', 'NeoTaste, 40 Bewertungen', 'Dieselbe Note von Gästen, die über die App gekommen sind.')]
    inhalt = kopf_theke(['Unter dieser', 'Decke.'], 'Eine kleine Bar an der Ecke Haasemannstraße, mit einem Gewölbe über der Theke, Glühbirnen über der Vitrine und zwei Leuten, die sie seit 2023 führen.')
    inhalt += fenster_kerzen()
    inhalt += '''<section class="kap auf" id="raum"><div class="innen">%s%s
<div class="pz auf">%s</div></div></section>''' % (
        kz('Der Raum', 'Vier Plätze', 0), h2(['Dein Platz', 'für heute Abend.']),
        ''.join('<div class="pz-s" style="--n:%d"><div class="pz-b">%s</div><h3 class="titel">%s</h3><p class="text">%s</p></div>' % (
            n, bild(k, 'pz-f', '(max-width:560px) 90vw, (max-width:900px) 45vw, 24vw', extra=' style="object-position:%s"' % p), E(t), E(s_)) for n, (k, t, s_, p) in enumerate(plaetze)))
    # «Wer hinter der Bar steht» als zwei Steckbriefe (Wahl Robert 31.10.2026, _varianten/haus-15 Fassung 2): je Person das Bild gross,
    # eine Platte mit dem Text schiebt sich über die Bildkante und läuft beim Scrollen etwas schneller; Momo gespiegelt.
    def steckbrief(k, name, rolle, text, weg, rechts):
        jahre = ''.join('<div><span>%s</span><p>%s</p></div>' % (E(j), E(t)) for j, t in weg)
        return '<div class="auf sb-zeile%s" data-sb>%s<div class="platte sb-platte"><h3 class="titel sb-name">%s</h3><span class="etikett">%s</span><p class="text">%s</p><div class="sb-weg">%s</div></div></div>' % (
            ' sb-r' if rechts else '', bild(k, 'sb-bild', '(max-width:760px) 100vw, 60vw', extra=' style="object-position:50% 30%"'), E(name), E(rolle), E(text), jahre)
    inhalt += '''<section class="kap auf" id="leute"><div class="innen">%s%s
<div style="margin-top:34px">%s%s</div></div></section>''' % (
        kz('Wer hinter der Bar steht', 'Zwei Leute', 0), h2(['Derya und Momo.']),
        steckbrief('derya', 'Derya Ivkin', 'führt die Bar', 'Seit Herbst 2023 gehört die Bar ihr und Momo. Sie entscheidet, wer auflegt, wer kocht und wann die Empore gedeckt wird.', derya, False),
        steckbrief('momo-giesst', 'Momo Ben Khelifa', 'mixt die Drinks', 'Er fragt, was du magst, und baut daraus einen Drink. Vorher Biotechnologie an der Uni, dann Bars in Berlin und Hannover.', momo, True))
    inhalt += fenster_fest('decke-hoch', ['Ein Loft', 'mitten in Linden.'], '50% 30%')   # seit 31.10.2026 Fenster in fester Grösse (Robert)
    # Fassung 4 «Filmstreifen» (Robert 31.10.2026, Runde _varianten/jahre-30): dunkler Streifen mit Lochrand, je Jahr ein Bild,
    # der Streifen zieht von rechts ein; darunter die Jahre in fünf Spalten. Ersetzt «Fotos im Wechsel» (Robert: «Bilder so untereinander gefällt mir nicht»).
    jahr_foto = {'2018': ('ja-2018', '50% 50%'), '2023': ('ja-2023', '50% 50%'), '2024': ('ja-2024', '50% 45%'),
                 '2025': ('ja-2025', '50% 30%'), '2027': ('ja-2027', '50% 50%')}   # Satz A, Robert 31.10.2026
    inhalt += '''<section class="kap auf" id="seit2017"><div class="innen">%s%s</div>
<div class="film-breit"><div class="film-streifen auf"><div class="film-zug">%s</div></div><div class="film-txt">%s</div></div></section>''' % (
        kz('Seit 2018', 'Die Jahre', 0), h2(['Was bisher geschah.']),
        ''.join('<div class="film-k"><span class="film-nr">WS %s · %d</span>%s</div>' % (
            j, n + 1, bild(jahr_foto[j][0], 'film-b', '(max-width:900px) 46vw, 19vw', extra=' style="object-position:%s"' % jahr_foto[j][1]))
            for n, (j, t) in enumerate(jahre)),
        ''.join('<div class="film-j auf" style="--n:%d"><span class="film-z">%s</span><p>%s</p></div>' % (n, j, E(t)) for n, (j, t) in enumerate(jahre)))
    # Was andere sagen: Fassung 9 «Flaschenetiketten» aus _varianten/stimmen-15 (Robert 31.10.2026: «9 aber ich will noch mehr die Logos und CIs sehen»),
    # je Etikett Logo und Farben der Quelle. Logos: assets/zeichen/quellen/ (Herkunft: _quelle/logo/quellen-logos/HERKUNFT.md).
    marke = [('falstaff', 'falstaff.svg', 'Falstaff', 'Bar Guide 2027', '<span class="et9-sterne et9-leer" aria-hidden="true">★★★★★</span>'),
             ('google', 'google.svg', 'Google', '75 Bewertungen', '<span class="et9-sterne" aria-hidden="true">★★★★★</span>'),
             ('neo', 'neotaste-hell.svg', 'NeoTaste', '40 Bewertungen', '<span class="et9-sterne et9-leer" aria-hidden="true">★★★★★</span>')]
    inhalt += '''<section class="kap auf" id="stimmen"><div class="innen">%s%s
<div class="et9"><div class="et9-reihe">%s</div></div>
<blockquote class="et9-presse sw" style="--i:2"><p>In der Presse: Die Neue Presse schrieb 2021 über Momo und 2024 über Derya an der Theke; Falstaff beschreibt die Bar als Loft, «stylish, relaxed», in der Gäste sagen, was sie mögen.</p></blockquote></div></section>''' % (
        kz('Was andere sagen', 'Drei Zahlen', 0), h2(['Gelobt von Gästen und Falstaff.']),
        ''.join('<div class="et9-s" style="--n:%d"><div class="et9-et et9-%s"><div class="et9-in"><span class="et9-logo"><img src="assets/zeichen/quellen/%s" alt="%s" width="200" height="60"></span><span class="etikett">%s</span><i></i><span class="et9-z titel">%s</span>%s<i></i><p>%s</p></div></div></div>' % (
            n, c, logo, E(name), E(was), z, extra, E(t)) for n, ((z, q, t), (c, logo, name, was, extra)) in enumerate(zip(stimmen, marke))))
    inhalt += fuss('decke-raum')
    return rahmen('Das Haus · Walk on the Wild Side Hannover', 'Der Raum unter dem Gewölbe, Derya Ivkin und Momo Ben Khelifa, die Jahre seit 2018, Falstaff 91 Punkte.', inhalt, 'haus.html')


# ---------------------------------------------------------------- Besuch
def besuch():
    fragen = [('Gibt es eine Karte?', 'Ja, die Karte wechselt immer wieder, die Drinks dafür entwirft Momo. Und an der Bar sagst du, was du magst. Wer einen Klassiker will, bekommt ihn.'),
              ('Was kostet ein Drink?', 'Signature Drinks 12 Euro, alkoholfreie Drinks 11, Longdrinks 10, Wein und Spritz 8, Sekt auf Eis 6, Bier 4, alkoholfreie Getränke 3 Euro.'),
              ('Gibt es Drinks ohne Alkohol?', 'Ja, mit derselben Sorgfalt: Shrub, Soda, Kräuter, klarer Saft.'),
              ('Kostet der Eintritt etwas?', 'Konzerte und DJ-Abende sind ohne Eintritt.'),
              ('Gibt es etwas zu essen?', 'An normalen Abenden nicht. Essen gibt es an den Abenden von Culinarium an der langen Tafel und bei Festen mit Buffet oder Foodtruck.'),
              ('Kann man draussen sitzen?', 'Wenn es warm ist, stehen Tische vor der Tür an der Ecke.'),
              ('Kann ich bei euch feiern?', 'Ja. Zehn bis zwanzig Gäste feiern an der langen Tafel auf der Empore, ab dreissig gehört euch die ganze Bar von 19 bis 2 Uhr. Alles dazu, mit Preisen, steht unter «Feiern».')]
    zeiten = ''.join('<div data-tag="%s"><span>%s<span class="jetzt"></span></span><b>%s</b></div>' % (t, E(n), E(z)) for n, z, t in HAUS['zeiten'])
    inhalt = kopf_licht(['Bis 2 Uhr.'], 'Haasemannstraße 13, Ecke Rampenstraße, Linden-Mitte. Donnerstag bis Samstag ab 19 Uhr.')
    # «Wann» als Leuchtschild (Fassung 15 aus _varianten/wann-15, Wahl Robert 31.10.2026)
    inhalt += '''<section class="kap auf wann" id="wann"><div class="innen w15-g">
<div>%s<div class="w15-schild w-hoch" style="--n:1"><i class="w15-licht"></i><span class="w15-wild">Wild Side</span><h2 class="titel w15-t" data-heute-satz>Donnerstag bis Samstag ab 19 Uhr</h2>
<div class="zeiten w15-zt">%s</div></div>
<p class="text w-satz">Die Bar ist klein. Wer zu mehreren kommt, reserviert besser, direkt hier: <a href="#reservieren" style="color:var(--gold)">Platz reservieren</a>.</p></div>
<figure class="kachel w15-bild w-hoch" style="--lq:url(%s)">%s</figure></div></section>''' % (
        kz('Wann', 'Drei Abende', 0), zeiten, mache('schild-ecke')['lq'], img_tag('schild-ecke', '(max-width:800px) 92vw, 36vw'))
    # «Wo» als dunkle Visitenkarte mit handgezeichneter Karte und Strassenschild (Wahl Robert 31.10.2026: Fassung 6 aus _varianten/wo-15, dazu Karte und Schild wie Fassung 11)
    ex, ey = karte_ecke.ecke_prozent()
    inhalt += '''<section class="kap hell auf wo-karte" id="wo"><div class="innen">%s
<div class="wk-karte"><div class="wk-o"><span class="logo wk-logo">%s</span><div class="wk-txt">%s<p class="text wk-satz">In Linden-Mitte, ein paar Schritte vom Küchengarten, gegenüber vom Restaurant 11A. Mit der Stadtbahn bis Am Küchengarten, dann zwei Minuten zu Fuss. Das Schild an der Ecke leuchtet.</p></div></div>
<div class="wk-u"><div class="wk-l"><div class="zeilen wk-z">%s</div><div class="knoepfe">%s</div></div>
<figure class="wk-plan">%s<div class="wk-schild" style="--ex:%.2f%%;--ey:%.2f%%"><i class="wk-pfosten"></i><p class="wk-s wk-a"><span>Haasemannstraße</span><b>13</b></p><p class="wk-s wk-c"><span>Rampenstraße</span></p></div>
<figcaption>Kartengrundlage © OpenStreetMap-Mitwirkende</figcaption></figure></div></div></div></section>''' % (
        kz('Wo', 'Die Ecke', 0), LOGO, h2(['Haasemannstraße', '<span class="wk-nr">13.</span>'], 'wk-t'),
        ''.join('<div><span class="etikett">%s</span><span>%s</span></div>' % (E(a), b) for a, b in [
            ('Adresse', E(HAUS['adresse']) + ', <span class="wk-nb">' + E(HAUS['ort']) + '</span>'), ('Ecke', 'Haasemannstraße, Ecke Rampenstraße'), ('Bahn', 'Stadtbahn bis Am Küchengarten, <span class="wk-nb">Linien 9 und 17</span>'),
            ('Telefon', '<a href="tel:%s">%s</a><br><a href="tel:%s">%s</a>' % (HAUS['tel_href'], E(HAUS['telefon']), HAUS['tel2_href'], E(HAUS['telefon2']))), ('Instagram', '<a href="%s" rel="noopener">%s</a>' % (HAUS['instagram'], E(HAUS['ig_name'])))]),
        knopf('Auf der Karte', 'https://www.openstreetmap.org/?mlat=52.37025&mlon=9.71339#map=18/52.37025/9.71339'),
        karte_ecke.svg(), ex, ey)
    # Reservieren · Sechs Hocker (Wahl Robert 31.10.2026, Fassung 2 aus _varianten/reservieren-15). Hocker antippen = so viele Plätze;
    # Sieben Hocker und «+» über die ganze Breite; «+» lässt einen Hocker von rechts einschweben, die anderen rücken nach links (8, 9);
    # beim zehnten wird aus der Theke die lange Tafel (zehn bis zwanzig, wie unter Feiern). Unten das Feld «Plätze», mit den Hockern verbunden. Robert 31.10.2026.
    inhalt += '''<section class="kap auf rh" id="reservieren"><form class="innen rh-form" data-vorfuehrung>
<div class="rh-kopf"><div>%s%s<p class="text sw" style="--i:2">Ab zehn Gästen gibt es die lange Tafel, ab dreissig die ganze Bar: alles unter <a href="tafel.html">Feiern</a>. Die Bar bestätigt per Nachricht.</p></div>
<div class="rh-zahl sw rh-weg" style="--i:2"><span class="etikett" data-rh-was>Wie viele · tippt die Hocker an</span><b class="titel" data-rh-zahl>4 Plätze</b></div></div>
<input type="hidden" name="platz" value="Theke">
<div class="rh-buehne rh-weg" data-rh-buehne>
<div class="rh-theke"><i class="rh-licht"></i><div class="rh-hocker" data-rh-hocker></div></div>
<div class="rh-tafel" aria-hidden="true"><div class="rh-tisch"><div class="rh-reihe oben" data-rh-oben></div><div class="rh-platte"></div><div class="rh-reihe unten" data-rh-unten></div></div></div>
</div>
<div class="rh-felder rh-weg"><label><span>Abend</span><input type="date" name="datum"></label><label><span>Uhrzeit</span><select name="zeit"><option>19 Uhr</option><option>20 Uhr</option><option>21 Uhr</option><option>22 Uhr</option></select></label><label><span>Plätze</span><input type="number" name="gaeste" min="1" max="200" value="4" inputmode="numeric" data-rh-feld></label><label><span>Name</span><input type="text" name="name"></label><label><span>Telefon oder E-Mail</span><input type="text" name="kontakt"></label></div>
<div class="rh-fuss rh-weg"><button class="knopf rot" type="submit"><span>Platz reservieren</span><i>%s</i></button><span class="hinweis">Vorführung: In diesem Entwurf wird nichts verschickt.</span></div>
<p class="dank">Danke. Die Bar bestätigt dir den Abend.</p>
</form></section>''' % (kz('Reservieren', 'Ein Platz an der Theke', 0), h2(['Ein Platz', 'für euch.'], 'rh-t', 1), PFEIL)
    # «Gut zu wissen» an der Goldlinie (Fassung 9 aus _varianten/fragen-15, Wahl Robert 31.10.2026): die Linie wächst mit dem Scrollen,
    # die Fragen stehen abwechselnd links und rechts daran und die Linie endet im Knopf zur Feiern-Seite.
    paare = ''.join('<div class="fg-p %s"><i class="fg-punkt"></i><div><h3 class="titel">%s</h3><p>%s</p></div></div>' % ('l' if n % 2 == 0 else 'r', E(f), E(a)) for n, (f, a) in enumerate(fragen))
    inhalt += '''<section class="kap auf fg" id="fragen"><div class="innen">
<div class="fg-kopf">%s%s</div>
<div class="fg-weg" data-fg-weg><i class="fg-linie"></i>%s
<div class="fg-ende">%s</div></div></div></section>''' % (
        kz('Gut zu wissen', 'Sieben Fragen', 0, 'justify-content:center'), h2(['Was Gäste', 'vorher fragen.'], 'fg-t'), paare, knopf('Feiern im Wild Side', 'tafel.html', 'rot'))
    inhalt += fuss('momo-lacht')
    return rahmen('Besuch · Walk on the Wild Side Hannover', 'Öffnungszeiten, Adresse, Reservieren und die Fragen, die Gäste vor dem ersten Abend stellen.', inhalt, 'besuch.html')


# ---------------------------------------------------------------- Rechtstexte
def recht(titel, absaetze, name):
    inhalt = '<section class="kap auf" style="padding-top:150px"><div class="innen recht">%s<h1 class="titel t-kap">%s</h1>%s</div></section>' % (
        kz('Rechtliches', titel, 0), zl([titel]), ''.join('<h2 class="titel">%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % E(p) for p in ps)) for h, ps in absaetze))
    return rahmen('%s · Walk on the Wild Side Hannover' % titel, titel, inhalt + fuss(), name)


def impressum():
    return recht('Impressum', [
        ('Betreiber der Bar', ['Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover. Inhaber: Derya Ivkin und Momo Ben Khelifa. Rechtsform, Registereintrag und Umsatzsteuer-Nummer werden vor dem Online-Gehen von der Bar ergänzt.']),
        ('Kontakt', ['Telefon %s und %s · Instagram %s' % (HAUS['telefon'], HAUS['telefon2'], HAUS['ig_name'])]),
        ('Dieser Entwurf', ['Diese Seite ist eine Designstudie von Tasty Studios, Robert Reff, Hamburg, und nicht die offizielle Website der Bar. Fotos und Plakate stammen von der Bar, aus ihren öffentlichen Kanälen und aus der Presse; vor einer Veröffentlichung unter eigener Adresse werden die Rechte geklärt.'])], 'impressum.html')


def datenschutz():
    return recht('Datenschutz', [
        ('Keine Daten', ['Diese Seite setzt keine Cookies, lädt keine Schriften und Skripte von fremden Servern und misst keine Besuche. Die Formulare sind Vorführungen und verschicken nichts.']),
        ('Links', ['Links führen zu Instagram, OpenStreetMap und zur Seite von Culinarium. Dort gelten die Datenschutzregeln der jeweiligen Anbieter.']),
        ('Vor dem Online-Gehen', ['Sobald Formulare echte Anfragen verschicken, wird hier ergänzt, wer die Daten empfängt, wie lange sie gespeichert werden und welche Rechte Gäste haben.'])], 'datenschutz.html')


def alle():
    return {'drinks.html': drinks(), 'programm.html': programm(), 'tafel.html': tafel(), 'haus.html': haus(), 'besuch.html': besuch(),
            'impressum.html': impressum(), 'datenschutz.html': datenschutz()}
