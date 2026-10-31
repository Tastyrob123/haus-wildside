#!/usr/bin/env python3
"""Das Markenbuch · Walk on the Wild Side Hannover: die Hausregeln (buch.html, Stil in buch/buch.css, Druck in buch.js), gebaut aus livre.json und
CHARAKTER.md Abschnitt 2 bis 5 (Register, Gegenstände, Marke, Bildbestand). Aufbau wie die Hausregeln von Culinarium (Titel, Kapitel als Blätter, Fenster,
Leiste mit «Als PDF sichern»), Inhalt und Kleid der Bar. Fotos aus der Website (/assets/bild), Wortmarke aus dateien/ (bau.py), Schriften der Website.

   python3 _werkzeuge/livre/buch.py      (nach bau.py)"""
import hashlib, html, json, os, re

e = html.escape
HIER = os.path.dirname(os.path.abspath(__file__))
L = json.load(open(os.path.join(HIER, 'livre.json'), encoding='utf-8'))
FOTO = {f['k']: f for f in L['fotos']}
FARBE = {f['k']: f for f in L['farben']}
S = 'wildside-hannover'


def _v(n):
    p = os.path.join(HIER, n)
    return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:10] if os.path.exists(p) else '1'


def bild(k, alt=None, pos='50% 50%', gross=False, lazy=False):
    f = FOTO[k]
    st = [x for x in (f['fs'], f['fm']) if x]
    w = lambda p: int(re.search(r'-(\d+)\.webp$', p).group(1))
    srcset = ', '.join(f'{p} {w(p)}w' for p in st)
    return (f'<img src="{f["fm"]}" srcset="{srcset}" sizes="{"100vw" if gross else "(max-width:900px) 100vw, 34vw"}" alt="{e(alt or f["t"]["de"])}"'
            f' width="{f["w"]}" height="{f["h"]}"{" loading=\"lazy\"" if lazy else ""} style="object-position:{pos}">')


FARBE_WM = {'rot': '#F0323F', 'creme': '#F2E9DC', 'nacht': '#1B1512'}


def symbol():
    """Die Wortmarke einmal als Symbol (Pfade aus dateien/, gebaut von bau.py), jede Verwendung über <use>, Farbe über color."""
    s = open(os.path.join(HIER, 'dateien', f'{S}-wortmarke-rot.svg'), encoding='utf-8').read()
    innen = re.search(r'<title>[^<]*</title>(.*)</svg>', s, flags=re.S).group(1).replace('#F0323F', 'currentColor')
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><symbol id="ws" viewBox="0 0 1296 1600">{innen}</symbol></defs></svg>'


def marke(farbe, klasse='', label='Walk on the Wild Side'):
    return f'<svg class="wm {klasse}" viewBox="0 0 1296 1600" style="color:{FARBE_WM[farbe]}" role="img" aria-label="{e(label)}"><use href="#ws"/></svg>'


PFEIL = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9.5M8.5 4l4 4-4 4"/></svg>'
RUNTER = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v9M3.8 7 8 11.2 12.2 7M3 14h10"/></svg>'
ZURUECK = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M13 8H3.5M7.5 4l-4 4 4 4"/></svg>'

KAP = [('haltung', 'Haltung'), ('zeichen', 'Zeichen'), ('farben', 'Farben'), ('session', 'DJ-Abende'), ('schrift', 'Schrift'), ('form', 'Form'),
       ('bilder', 'Bilder'), ('dinge', 'Gegenstände'), ('ton', 'Ton'), ('nachbarn', 'Nachbarn')]


def kopf(nr, etikett, titel, lead):
    a, b = titel
    return (f'<header class="mk" data-r><p class="mk__kap"><span>{nr:02d}</span><b>{e(etikett)}</b><i></i></p>'
            f'<h2 class="mk__t">{e(a)} <em>{e(b)}</em></h2><p class="mk__lead">{lead}</p></header>')


def faecher():
    out = []
    for g in L['gruppen']:
        fs = [f for f in L['farben'] if f['g'] == g['k']]
        knoepfe = ''.join(
            f'<div class="fa" role="button" tabindex="0" data-hex="{f["h"]}" style="--c:{f["h"]}" aria-label="{e(f["n"])} {f["h"]} kopieren">'
            f'<span class="fa__f"><span class="fa__ok">kopiert</span></span><span class="fa__n"><b>{e(f["n"])}</b><small>{e(f["r"])}</small><code>{f["h"]}</code></span></div>'
            for f in fs)
        out.append(f'<div class="fg" data-r><div class="fg__t"><h3>{e(g["n"])}</h3><p>{e(g["s"])}</p></div><div class="fg__f">{knoepfe}</div></div>')
    return ''.join(out)


def seite():
    h = FARBE
    titel = f'''<section class="titel" id="oben">
  <div class="titel__in">
    <div class="titel__wm" data-r>{marke("rot", "", "Walk on the Wild Side")}</div>
    <div class="titel__t">
      <p class="etikett" data-r>Die Hausregeln · Oktober 2026</p>
      <h1 data-r>Walk on the <em>Wild Side.</em></h1>
      <p class="titel__ort" data-r>Nachbarschafts-Mixology-Bar <i></i> Haasemannstraße 13 <i></i> Hannover-Linden</p>
      <p class="titel__lead" data-r>Alles, was die Bar erkennbar macht, an einem Ort: die Wortmarke, die Farben und ihre Rollen, die Farben der DJ-Abende, die Schriften, das Eckschild als Form, die Bilder, die Gegenstände des Raums und der Ton. Damit jedes neue Stück, ob Plakat, Beitrag oder Karte, aussieht wie aus einem Guss.</p>
      <p class="titel__kn" data-r><a class="kn kn--rot" href="#haltung"><span>Lesen</span><i>{RUNTER}</i></a></p>
    </div>
  </div>
  <nav class="index" aria-label="Inhalt">{"".join(f'<a href="#{k}"><span>{i + 1:02d}</span>{e(n)}</a>' for i, (k, n) in enumerate(KAP))}</nav>
</section>'''

    haltung = f'''<section class="blatt hell" id="haltung"><div class="in">
  {kopf(1, 'Haltung', ('Du sagst,', 'was du magst.'), 'Eine Nachbarschaftsbar in Linden-Mitte mit wechselnder Karte, deren Drinks Momo entwirft. An der Bar sagst du, was du magst, und unter der bedruckten Gewölbe-Decke wird es donnerstags bis samstags von 19 Uhr an lauter. Die Gestaltung ist nachts: laut, spontan, sexy, aber aufgeräumt.')}
  <div class="drei">
    <article class="k3" data-r><div class="k3__b">{bild('momo-giesst', 'Momo giesst einen Drink an der Bar', '62% 40%')}</div>
      <div class="k3__n"><small>An der Bar</small><b>Das Glas.</b><p>Momo entwirft die Drinks, Derya führt die Bar. Die Karte wechselt; wer nicht wählen mag, sagt, was er mag.</p></div></article>
    <article class="k3" data-r><div class="k3__b">{bild('decke-raum', 'Der Raum unter der bedruckten Gewölbe-Decke', '50% 30%')}</div>
      <div class="k3__n"><small>Über dem Raum</small><b>Die Decke.</b><p>Ein grosser Druck eines Kathedralen-Gewölbes, blau-silbern und golden angeleuchtet. Kalt oben, warm unten.</p></div></article>
    <article class="k3" data-r><div class="k3__b">{bild('schild-ecke', 'Die Ecke Haasemannstraße am Abend', '50% 45%')}</div>
      <div class="k3__n"><small>Ecke Rampenstraße</small><b>Die Ecke.</b><p>Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr. Samstags legen DJs auf, an anderen Abenden spielen Bands.</p></div></article>
  </div>
</div></section>'''

    fenster = lambda k, satz, unter, pos='50% 50%': f'''<section class="fenster" aria-label="{e(satz)}"><div class="fenster__f">
  <div class="fenster__b">{bild(k, None, pos, True, False)}</div>
  <div class="fenster__t"><p class="fenster__s">{e(satz)}</p><p class="fenster__u">{e(unter)}</p></div></div></section>'''

    nein = lambda klasse, text: f'<figure class="nein nein--{klasse}"><div>{marke("rot")}</div><figcaption>{e(text)}</figcaption></figure>'
    zeichen = f'''<section class="blatt dunkel" id="zeichen"><div class="in">
  {kopf(2, 'Zeichen', ('Ein Zeichen,', 'überall dasselbe.'), 'Die Wortmarke ist das Logo der Bar: WILD SIDE in einer schmalen, fetten Grotesk, ausgespart aus einer leicht schrägen Fläche. Sie ist Pfad für Pfad aus dem Logo der früheren Seite der Bar nachgezogen und wird immer als Datei eingesetzt, nie als Schrift nachgebaut.')}
  <div class="lockups">
    <figure class="lock lock--nacht" data-r><div>{marke("rot")}</div><figcaption><b>Rot auf Nacht</b><small>Hauptform · {h["rot"]["h"]}</small></figcaption></figure>
    <figure class="lock lock--nacht" data-r><div>{marke("creme")}</div><figcaption><b>Creme auf Nacht</b><small>wo Rot schon steht · {h["creme"]["h"]}</small></figcaption></figure>
    <figure class="lock lock--creme" data-r><div>{marke("nacht")}</div><figcaption><b>Nacht auf Creme</b><small>auf den hellen Plakaten · {h["dunkel"]["h"]}</small></figcaption></figure>
  </div>
  <div class="regeln">
    <div class="regel" data-r><div class="regel__f"><span class="schutz">{marke("creme")}</span></div><h3>Schutzraum</h3><p>Rund um die Wortmarke bleibt ein Viertel ihrer Breite frei. Kein Text, kein Bildrand, keine Linie ragt hinein.</p></div>
    <div class="regel" data-r><div class="regel__f klein"><span>{marke("creme")}<small>32 px</small></span><span>{marke("creme")}<small>48 px</small></span><span>{marke("creme")}<small>72 px</small></span></div><h3>Kleinste Grösse</h3><p>Ab 32 Pixel Höhe am Bildschirm, im Druck ab 12 Millimeter. Darunter steht der Name der Bar als Text.</p></div>
    <div class="regel regel--breit" data-r><div class="regel__f neine">{nein('zerr', 'Nicht verzerren')}{nein('dreh', 'Nicht drehen')}{nein('schatten', 'Kein Schatten, kein Leuchten')}{nein('farbe', 'Keine fremde Farbe')}</div><h3>Was die Wortmarke nicht darf</h3><p>Sie steht so schräg, wie sie gezeichnet ist, in Rot, Creme oder Nacht, ohne Schatten und ohne Rahmen darum. Auf einem unruhigen Foto steht sie nie.</p></div>
  </div>
</div></section>'''

    farben = f'''<section class="blatt hell" id="farben"><div class="in">
  {kopf(3, 'Farben', ('Nacht und Creme,', 'Gold und ein Punkt Rot.'), 'Die Farben kommen aus dem Raum: die Nacht unter der Decke, das Creme der weissen Plakate der Bar, das Gold vom Rahmen des Eckschilds, das Rot der Wortmarke. Jede steht genau so in der Gestaltung der Website. Ein Klick auf eine Farbe kopiert ihren Wert.')}
  {faecher()}
  <div class="satzreihe" data-r><p><b>Gold rahmt.</b> Nur als Haarlinie, Etikett und Knauf, nie als Fläche.</p><p><b>Rot ist ein Punkt.</b> Die Wortmarke und der eine Hauptknopf, nie zwei grosse Flächen in Rot nebeneinander.</p><p><b>Nie rein.</b> Kein reines Schwarz, kein reines Weiss: Nacht und Creme tragen alles.</p></div>
</div></section>'''

    plakate = ['p-1710', 'p-0310', 'p-0906', 'p-2401']
    session = f'''<section class="blatt creme2" id="session"><div class="in">
  {kopf(4, 'Die DJ-Abende', ('Samstags', 'die Welle.'), 'Für die DJ-Abende hat die Bar eine eigene Sprache: die SESSION-Plakate mit rot-cremefarbenen Wellen, der Schrift in Ultramarin und den DJs in Schwarzweiss. Diese Farben gehören nur zu den DJ-Abenden. Auf der Website liefern die Plakate Farbe und Material, sie sind nie das Hauptbild.')}
  <div class="plakate">{"".join(f'<figure class="plakat" data-r>{bild(k, None)}<figcaption>{e(re.sub(r"^Plakat SESSION(,| mit( den)?) ", "", FOTO[k]["t"]["de"]))}</figcaption></figure>' for k in plakate)}</div>
  <div class="session-f" data-r>{"".join(f'<span style="--c:{FARBE[k]["h"]}"><i></i><b>{e(FARBE[k]["n"])}</b><code>{FARBE[k]["h"]}</code></span>' for k in ('plakatrot', 'ultramarin', 'plakatcreme'))}</div>
</div></section>'''

    schrift = f'''<section class="blatt dunkel" id="schrift"><div class="in">
  {kopf(5, 'Schrift', ('Eine Antiqua mit Glanz,', 'eine ruhige Grotesk.'), 'Prata für die Titel: eine einzige Stärke, nie fett, nie kursiv. Hanken Grotesk für alles, was gelesen wird, und in Versalien gesperrt für Etiketten und Knöpfe. Zahlen stehen in Hanken mit gleich breiten Ziffern, Uhrzeiten im Fuss der Website in Prata.')}
  <div class="proben">
    <div class="probe probe--prata" data-r><small>Titel · Prata 400</small><p class="p1">Du sagst, was du magst.</p><p class="abc">Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz Ää Öö Üü ß 0123456789</p></div>
    <div class="probe" data-r><small>Lesetext · Hanken Grotesk 400 · 17 px · Zeilenabstand 1,6</small><p class="p2">An der Bar sagst du, was du magst, und Momo macht dir einen Drink daraus. Samstags legen DJs auf, die Karte wechselt, und unter der Decke wird es von 19 Uhr an lauter.</p></div>
    <div class="probe" data-r><small>Etiketten und Knöpfe · Hanken 500 · Versalien · 0,17 em</small><p class="p3">Donnerstag bis Samstag ab 19 Uhr</p><p class="p4"><span>Do</span><b>19 bis 1 Uhr</b><span>Fr und Sa</span><b>19 bis 2 Uhr</b></p></div>
  </div>
</div></section>'''

    form = f'''<section class="blatt hell" id="form"><div class="in">
  {kopf(6, 'Form', ('Das Eckschild', 'an der Hausecke.'), 'Schwarz, mit Goldrahmen, nachts beleuchtet: das Schild an der Ecke Haasemannstraße ist die Form der ganzen Gestaltung. Platten liegen wie das Schild auf der Nacht, Kacheln sitzen ohne Rahmen darin, Knöpfe tragen einen runden Knauf.')}
  <div class="formen">
    <figure class="form-b" data-r>{bild('pf-schild', 'Die beiden Schilder an der Hausecke', '50% 40%')}<figcaption>Die Schilder an der Hausecke, Juni 2025</figcaption></figure>
    <div class="form-d" data-r>
      <div class="platte"><small>Platte</small><b>18 px Radius, Goldlinie innen, weicher Schatten</b><div class="kacheln"><span>Kachel</span><span>14 px</span><span>ohne Rahmen</span></div></div>
      <div class="kn-reihe"><span class="kn kn--rot"><span>Platz anfragen</span><i>{PFEIL}</i></span><span class="kn kn--nacht"><span>Programm</span><i>{PFEIL}</i></span></div>
      <p class="form-s"><b>Rot mit Creme-Knauf</b> ist der Hauptweg, einmal je Fläche. <b>Nacht mit Goldlinie und Gold-Knauf</b> ist jeder Nebenweg.</p>
    </div>
  </div>
  <div class="nicht" data-r><h3>Nicht bei uns</h3><p>Tickets, Platzkarten, Leuchtschrift-Optik, Sticker, Polaroids, Kreise und Siegel, Pillen-Reihen, Einkerbungen. Das alles gehört zu anderen Häusern.</p></div>
</div></section>'''

    mosaik = [('voll', '50% 50%'), ('glas-rot', '50% 55%'), ('anstossen', '50% 40%'), ('saengerin', '50% 35%'), ('momo-lacht', '58% 45%')]
    bilder = f'''<section class="blatt dunkel" id="bilder"><div class="in">
  {kopf(7, 'Bilder', ('Die Menschen', 'und der Moment.'), 'Nach vorn gehören die Menschen und der Moment an der Bar: Momo mit dem Glas, Gäste, DJs und Bands, gerahmt vom Raum mit Decke, Glühbirnen und Schild. Die Fotos sind warm, oft orange; neben Creme und Ultramarin werden sie nicht beruhigt. Das ist der Kontrast der Bar: warmes Licht, kalte Decke.')}
  <div class="mosaik">{"".join(f'<figure data-r>{bild(k, None, p)}</figure>' for k, p in mosaik)}</div>
  <ul class="regel-liste" data-r><li><b>Warm bleibt warm.</b> Kein Filter, der das Licht der Bar kühlt.</li><li><b>Kein Teller als Hauptbild.</b> Teller und lange Tafel erzählen Culinarium.</li><li><b>Nie unscharf.</b> Lieber ein kleineres Bild als ein hineingezoomtes.</li><li><b>Fotos von Gästen und Presse</b> nur mit Erlaubnis der Fotografen.</li></ul>
</div></section>'''

    dinge = [('negroni', 'NEGRONI in Glühbirnen', 'Der Schriftzug über der Vitrine, bei Konzerten auch «love». Er darf als Licht einmal angehen, nie als Schrift nachgebaut werden.'),
             ('schild', 'Das Eckschild', 'Schwarzes Kastenschild mit Goldrahmen an der Hausecke, nachts beleuchtet. Daraus kommen Platten und Knöpfe.'),
             ('decke-hoch', 'Die Decke', 'Der Druck eines Kathedralen-Gewölbes über dem ganzen Raum. Aus seinen Rippen kommt die Tapete.'),
             ('ja-2025', 'Die weissen Plakate', 'Creme mit roter Schrift: «Eure Nachbarschafts-Mixology-Bar», Silvester, Jahrestage. Daher kommt das Creme.')]
    gegenstaende = f'''<section class="blatt hell" id="dinge"><div class="in">
  {kopf(8, 'Gegenstände', ('Was nur', 'diese Bar hat.'), 'Vier Dinge machen die Bar unverwechselbar. Sie liefern Farbe, Form und Licht für jede Gestaltung; keines wird als Zeichnung nachgemacht.')}
  <div class="vier">{"".join(f'<article class="k4" data-r><div class="k4__b">{bild(k, None)}</div><b>{e(t)}</b><p>{e(s)}</p></article>' for k, t, s in dinge)}</div>
</div></section>'''

    ton = f'''<section class="blatt dunkel" id="ton"><div class="in">
  {kopf(9, 'Ton', ('Du, knapp,', 'nachts ein bisschen laut.'), 'Die Bar duzt. Sie schreibt kurz, spontan und mit einem Augenzwinkern, nie in Werbesprache. Lieber eine echte Angabe (der Tag, die Uhrzeit, der Name des DJs) als ein Adjektiv. Die Karte wechselt, und genau so steht es da.')}
  <div class="zwei">
    <div class="ton ton--ja" data-r><h3>So klingt die Bar</h3><ul>{"".join(f'<li>«{e(w)}»</li>' for w in L['ton']['eigene_worte'])}</ul></div>
    <div class="ton ton--nein" data-r><h3>So nicht</h3><ul><li><s>Sichern Sie sich Ihren Tisch</s><span>Platz anfragen</span></li><li><s>Bei uns gibt es keine Karte</s><span>Die Karte wechselt</span></li><li><s>Die exklusivste Event-Location</s><span>Eure Nachbarschafts-Mixology-Bar</span></li><li><s>Unvergessliche Cocktail-Erlebnisse</s><span>Du sagst, was du magst</span></li></ul></div>
  </div>
</div></section>'''

    nachbarn = f'''<section class="blatt hell" id="nachbarn"><div class="in">
  {kopf(10, 'Nachbarn', ('Im selben Haus,', 'nicht im selben Kleid.'), 'Im Haus laufen auch Culinarium, die Food-Pairing-Abende an der langen Tafel, und Dirty Chicken, Rudis Pop-up. Beide haben ihr eigenes Gesicht. Auf den Seiten der Bar stehen sie nur als Verweis: «Unsere Abende an der langen Tafel: Culinarium».')}
  <div class="vergleich">
    <div class="vg vg--wild" data-r>{marke("rot")}<div><h3>Walk on the Wild Side</h3><p>Nacht, Creme, Gold und ein Punkt Rot. Prata und Hanken. Das Glas, die Ecke, die Musik. Uhrzeiten von 19 bis 2 Uhr als Faden.</p></div></div>
    <div class="vg vg--nb" data-r><figure>{bild('culinarium-tafel', None)}</figure><div><h3>Culinarium</h3><p>Kerzenlicht, Teller und die lange Tafel, eigene Schrift und eigene Farben. Gemeinsam ist nur das Haus und Momo an der Bar.</p></div></div>
  </div>
</div></section>'''

    fuss = f'''<footer class="fuss"><div class="in">
  <div class="fuss__wm">{marke("rot")}</div>
  <div class="fuss__t"><p class="etikett">Die Hausregeln · Stand Oktober 2026</p><p class="fuss__a">Haasemannstraße 13, Ecke Rampenstraße<br>30449 Hannover-Linden</p>
    <dl class="fuss__z"><div><dt>Donnerstag</dt><dd>19 bis 1 Uhr</dd></div><div><dt>Freitag</dt><dd>19 bis 2 Uhr</dd></div><div><dt>Samstag</dt><dd>19 bis 2 Uhr</dd></div></dl>
    <p class="fuss__l"><a href="./">Zurück zum Markenbuch</a></p></div>
</div></footer>'''

    leiste = f'''<nav class="leiste" aria-label="Die Hausregeln">
  <a class="leiste__m" href="./" title="Zurück zum Markenbuch">{marke("rot", "leiste__wm")}<span><b>Die Hausregeln</b><small>Zurück zum Markenbuch</small></span></a>
  <div class="leiste__k">{"".join(f'<a href="#{k}">{e(n)}</a>' for k, n in KAP)}</div>
  <button class="kn kn--rot kn--leiste" type="button" id="bu-pdf"><span>Als PDF sichern</span><i>{RUNTER}</i></button>
</nav>'''

    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Die Hausregeln · Walk on the Wild Side Hannover</title>
<meta name="description" content="Die Hausregeln von Walk on the Wild Side: Wortmarke, Farben und ihre Rollen, die DJ-Abende, Schriften, das Eckschild als Form, Bilder, Gegenstände und Ton.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#130E0D">
<link rel="icon" href="/assets/oberflaeche/kleid/wildside-zeichen.svg" type="image/svg+xml">
<link rel="preload" href="../../assets/schrift/prata-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/schrift/hanken-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="buch/buch.css?v={_v('buch/buch.css')}">
</head>
<body>
{symbol()}
{leiste}
<main>
{titel}
{haltung}
{fenster('theke', 'Good Drinks, Good Music, Good Energy.', 'So steht es unter den Beiträgen der Bar.', '50% 55%')}
{zeichen}
{farben}
{session}
{schrift}
{form}
{bilder}
{gegenstaende}
{fenster('konzert-scharf', 'Erst der Drink, dann die Musik.', 'Ein Konzert unter der Decke, März 2024.', '50% 45%')}
{ton}
{nachbarn}
</main>
{fuss}
<div class="meldung" id="meldung" aria-live="polite"></div>
<script src="buch.js?v={_v('buch.js')}"></script>
</body>
</html>
'''


if __name__ == '__main__':
    open(os.path.join(HIER, 'buch.html'), 'w', encoding='utf-8').write(seite())
    print('buch.html geschrieben')
