#!/usr/bin/env python3
"""Walk on the Wild Side · 20 aussergewöhnliche Auftakte (29.10.2026, Robert: «so outstanding wie Culinarium, auf die eigene Art»).
Jede Fassung ist die echte Startseite, nur der Auftakt ist getauscht. 00 = heute. Wechsel mit ← →.
Freisteller und Ebenen: ebenen.py (Apple Vision, lokal). Aufruf: python3 bau.py"""
import json, re, html, math, time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
BILD = WEB / "assets" / "bild"
INDEX = (WEB / "index.html").read_text()
KOPF = re.search(r'<header class="auftakt auf" id="auftakt">.*?</header>', INDEX, re.S)

LOGO = re.search(r'(<svg viewBox="0 0 1296 1600".*?</svg>)', INDEX, re.S).group(1)
KNOEPFE = re.search(r'<div class="knoepfe sw" style="--i:5">(.*?)</div></div>\n<p class="at-weiter', INDEX, re.S).group(1)
SATZ = "Eine Nachbarschafts-Mixology-Bar in Linden-Mitte. Es gibt keine Karte: Du sagst Momo, was du magst, und er mixt dir deinen Drink."
ZEITEN = "Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr"
ORT = "Haasemannstraße 13 · Linden"
ALT = {
    "schild": "Das beleuchtete Schild an der Hausecke: Walk on the Wild Side", "schild-ecke": "Die Hausecke bei Nacht",
    "decke-2017": "Die Gewölbe-Decke", "decke-raum": "Der Raum unter der Decke", "momo-giesst": "Momo giesst einen Drink ab",
    "momo-lacht": "Momo hinter der Theke", "glas-coupe": "Ein Drink mit Schaum", "freundinnen": "Zwei Gäste an der Theke",
    "negroni": "Die Glühbirnen-Schrift NEGRONI", "fenster": "Blick durchs Fenster in die Bar", "tuer-rot": "Der Eingang im roten Licht",
    "glas-sour": "Ein Sour auf der Theke", "voll": "Ein voller Abend unter der Decke", "gast-havn": "Ein Gast an der Theke",
    "konzert-love": "Konzert vor der Schrift love", "schaum": "Schaum auf einem Drink", "glas-negroni": "Ein Negroni",
    "theke": "Die Theke", "glas-trinkt": "Ein Gast trinkt", "anstossen": "Zwei Gläser stossen an", "glas-kerze": "Ein Drink im Kerzenlicht",
    "saengerin": "Die Sängerin am Mikrofon", "glas-zwei": "Zwei Drinks", "silvester": "Ein Glas an Silvester",
    "tafel-glaeser": "Momo seiht Drinks ab", "rueckbar-breit": "Die Rückbar", "glas-rot": "Ein roter Drink", "glas-hand": "Ein Drink in der Hand",
    "gast-musa": "Gäste an der Theke", "decke-bar": "Die Bar unter der Decke",
}


def img(name, sizes="100vw", pos="50% 50%", cls="", lazy=False):
    j = json.loads((BILD / f"{name}.json").read_text())
    st = j["stufen"]
    srcset = ", ".join(f"assets/bild/{f}?v=28103 {w}w" for w, f in st)
    mitte = next((f for w, f in st if w >= 960), st[-1][1])
    c = f' class="{cls}"' if cls else ""
    lade = 'loading="lazy"' if lazy else 'fetchpriority="high"'
    return (f'<img{c} src="assets/bild/{mitte}?v=28103" srcset="{srcset}" sizes="{sizes}" alt="{html.escape(ALT.get(name, ""))}" '
            f'{lade} decoding="async" width="{j["w"]}" height="{j["h"]}" style="object-position:{pos}">')


def eb(name, cls="", alt=""):
    return f'<img class="{cls}" src="_varianten/hero-20/ebene/{name}.webp?v=1" alt="{html.escape(alt)}" decoding="async">'


def fig(name, sizes="50vw", pos="50% 50%", cls="xb", stil=""):
    s = f' style="{stil}"' if stil else ""
    return f'<figure class="{cls}"{s}>{img(name, sizes, pos)}</figure>'


def titel(zeilen=("Du sagst,", "was du magst."), start=1, cls="T"):
    z = "".join(f'<span class="z"><span style="--i:{start + i}">{t}</span></span>' for i, t in enumerate(zeilen))
    return f'<h1 class="{cls}"><span class="zl">{z}</span></h1>'


def logo(i=0, cls="xlogo"):
    return f'<a class="{cls} sw" style="--i:{i}" href="index.html" aria-label="Walk on the Wild Side">{LOGO}</a>'


def satz(i=3):
    return f'<p class="xsatz sw" style="--i:{i}">{SATZ}</p>'


def zeile(i=4):
    return (f'<div class="xzeile sw" style="--i:{i}"><span class="etikett">{ZEITEN}</span>'
            f'<span class="trenner"></span><span class="ort">{ORT}</span></div>')


def knoepfe(i=5):
    return f'<div class="knoepfe sw" style="--i:{i}">{KNOEPFE}</div>'


def block(i=3):
    return satz(i) + zeile(i + 1) + knoepfe(i + 2)


def spalte(extra_logo=True, zeilen=("Du sagst,", "was du magst.")):
    return f'<div class="xt">{logo(0) if extra_logo else ""}{titel(zeilen)}{block()}</div>'


def wellen():
    n, breite, hoehe, periode = 7, 600, 1600, 400
    pfade = []
    for k in range(n):
        mx = breite * (k + .5) / n; w = breite / n * .3; phi = k * .9
        l, r = [], []
        for y in range(0, hoehe + 1, 10):
            dx = 26 * math.sin(2 * math.pi * y / periode + phi)
            l.append(f"{mx - w + dx:.1f},{y}"); r.append(f"{mx + w + dx:.1f},{y}")
        pfade.append("M" + " L".join(l) + " L" + " L".join(reversed(r)) + "Z")
    return f'<svg viewBox="0 0 {breite} {hoehe}" preserveAspectRatio="none" aria-hidden="true">' + "".join(f'<path d="{p}"/>' for p in pfade) + "</svg>"


F = []

# 01 Das Licht geht an: das Schild flackert an wie eine alte Leuchte, dann erst die Strasse und der Satz
F.append((1, "Das Licht geht an", f'''
<figure class="xfoto">{eb("schild-dunkel", "x-dunkel")}{img("schild", "80vw", "60% 36%", "x-hell")}</figure><div class="xhof"></div>
{spalte()}'''))

# 02 Hinter dem Schild: der Satz kommt hinter dem Schild an der Ecke hervor
F.append((2, "Hinter dem Schild", f'''
<figure class="xfoto">{img("schild", "70vw", "50% 20%")}</figure><div class="xhof"></div>
<div class="x-spur">{titel()}</div>
<div class="xfoto x-vorn" aria-hidden="true">{eb("schild-ebene")}</div>
<div class="xt x-unten">{block()}</div>'''))

# 03 Unter dem Gewölbe: die Decke zieht über den Kopf, wie beim Hereinkommen
F.append((3, "Unter dem Gewölbe", f'''
<div class="x-raum" aria-hidden="true"><div class="x-decke">{eb("decke-tunnel")}</div></div>
<div class="x-mitte">{logo(0)}{titel()}<div class="x-reihe">{satz(3)}<div>{zeile(4)}{knoepfe(5)}</div></div></div>'''))

# 04 Das Eckschild: der Kasten von der Hausecke als Gegenstand, er dreht sich zur Maus
F.append((4, "Das Eckschild", f'''
{spalte()}
<div class="x-objekt" aria-hidden="true"><div class="x-schein"></div><div class="x-kasten">
<div class="f f-hinten"></div><div class="f f-l"></div><div class="f f-r"></div><div class="f f-o"></div><div class="f f-u"></div><div class="f f-vorn">{eb("schild-gerade")}</div>
</div></div>'''))

# 05 Die Ecke: zwei Hauswände treffen sich, an der Kante hängt das Zeichen
F.append((5, "Die Ecke", f'''
<div class="x-ecke" aria-hidden="true"><div class="x-haus">
<div class="x-wand x-wl">{img("fenster", "34vw", "50% 55%")}</div><div class="x-wand x-wr">{img("tuer-rot", "34vw", "50% 60%")}</div>
<div class="x-fahne">{LOGO}</div></div></div>
<div class="x-mitte">{titel(["Du sagst, was du magst."], start=0)}<div class="x-reihe">{satz(2)}<div>{zeile(3)}{knoepfe(4)}</div></div></div>'''))

# 06 Das Karussell: der Abend auf einem Ring, er dreht sich, die Maus gibt Schwung
RING = ["momo-giesst", "glas-coupe", "freundinnen", "negroni", "konzert-love", "glas-sour", "voll", "tuer-rot", "gast-havn", "glas-negroni"]
F.append((6, "Das Karussell", f'''
<div class="x-ring" aria-hidden="true"><div class="x-dreh">{"".join(f'<figure class="x-feld" style="--n:{i}">{img(n, "16vw", "50% 40%")}</figure>' for i, n in enumerate(RING))}</div></div>
<div class="x-mitte">{titel(["Du sagst, was du magst."], start=0)}<div class="x-reihe">{satz(2)}<div>{zeile(3)}{knoepfe(4)}</div></div></div>'''))

# 07 Die Decke dreht sich zur Bar: Fliese für Fliese wird aus dem Gewölbe der Abend darunter
kacheln = []
for r in range(4):
    for c in range(5):
        lage = f'style="left:{-c * 100}%;top:{-r * 100}%"'
        kacheln.append(f'<div class="k" style="--c:{c};--r:{r}"><div class="s v"><img src="assets/bild/decke-2017-1600.webp?v=28103" alt="" {lage}></div>'
                       f'<div class="s h"><img src="assets/bild/voll-1536.webp?v=28103" alt="" {lage}></div></div>')
F.append((7, "Die Decke dreht sich", f'''
{spalte()}
<div class="x-fliesen" aria-hidden="true">{"".join(kacheln)}</div>'''))

# 08 Schärfe zieht auf: erst ist alles weich, dann wird das Glas scharf; oben hingeschaut wird die Bar scharf
F.append((8, "Schärfe zieht auf", f'''
{spalte()}
<figure class="x-sour">{eb("sour-weich", "e1")}{img("glas-sour", "60vw", "50% 50%", "e2")}{eb("sour-glas-weich", "e3")}{eb("glas-sour-ebene", "e4", ALT["glas-sour"])}</figure>'''))

# 09 Der Drink kommt über den Tresen: Momo schiebt ihn dir hin
F.append((9, "Über den Tresen", f'''
<figure class="x-regal">{img("rueckbar-breit", "100vw", "50% 40%")}</figure><div class="x-tresen"></div><div class="xhof"></div>
{spalte()}
<div class="x-weg" aria-hidden="true">{eb("glas-negroni-frei", "x-glas")}</div>'''))

# 10 Aus dem Rahmen: Momo lehnt sich aus dem Bild heraus
F.append((10, "Aus dem Rahmen", f'''
{spalte()}
<div class="x-box">{img("momo-giesst", "44vw", "50% 50%")}<div class="x-linie"></div>{eb("momo-giesst-ebene", "x-frei", "")}</div>'''))

# 11 SESSION: die Welt der DJ-Plakate, Momo in Schwarzweiss vor den Wellen
F.append((11, "SESSION", f'''
{spalte()}
<div class="x-welle" aria-hidden="true">{wellen()}{eb("momo-sw-frei", "x-momo")}</div>'''))

# 12 Zeilen laufen: der Satz riesig, die Zeilen laufen beim Scrollen gegeneinander, dazwischen der Abend
BAND = ["glas-sour", "voll", "momo-giesst", "konzert-love", "schaum", "freundinnen", "negroni", "glas-coupe", "tuer-rot", "gast-havn"]
F.append((12, "Zeilen laufen", f'''
<h1 class="T x-z1"><span class="zl"><span class="z"><span style="--i:0">Du sagst,</span></span></span></h1>
<div class="x-band" aria-hidden="true"><div class="x-spur">{"".join(fig(n, "20vw", "50% 45%") for n in BAND)}</div></div>
<p class="T x-z2" aria-hidden="true"><span class="zl"><span class="z"><span style="--i:1">was du magst.</span></span></span></p>
<div class="x-unten">{logo(2)}<div>{satz(3)}{zeile(4)}</div>{knoepfe(5)}</div>'''))

# 13 Quer durch die Bar: beim Scrollen fährt man die Theke entlang
QUER = ["momo-giesst", "negroni", "glas-coupe", "voll", "konzert-love", "freundinnen", "tuer-rot"]
F.append((13, "Quer durch die Bar", f'''
<div class="x-buehne"><div class="x-spur"><div class="xt">{logo(0)}{titel()}{block()}</div>{"".join(fig(n, "48vw", "50% 40%") for n in QUER)}</div></div>'''))

# 14 Spiegel der Theke: der Raum spiegelt sich im Tresen, ein Lichtstreif läuft darüber
F.append((14, "Spiegel der Theke", f'''
<figure class="x-oben">{img("voll", "100vw", "50% 58%")}</figure>
<figure class="x-spiegel" aria-hidden="true">{img("voll", "100vw", "50% 58%")}<i class="x-glanz"></i></figure>
<div class="x-mitte">{titel(["Du sagst, was du magst."], start=0)}<p class="T x-echo" aria-hidden="true">Du sagst, was du magst.</p></div>
<div class="x-reihe">{logo(1)}{satz(2)}<div>{zeile(3)}{knoepfe(4)}</div></div>'''))

# 15 Das Zeichen als Fenster: die rote Tafel des Logos wird zum Fenster in die Bar
F.append((15, "Das Zeichen als Fenster", f'''
{spalte()}
<div class="x-platte"><div class="x-innen">{img("decke-raum", "44vw", "50% 40%")}</div></div>'''))

# 16 Von 19 bis 2: die Maus fährt durch die Nacht, jede Stunde ein Bild
NACHT = [("19", "schild"), ("20", "momo-giesst"), ("21", "glas-sour"), ("22", "freundinnen"), ("23", "konzert-love"), ("00", "voll"), ("01", "decke-raum"), ("02", "tuer-rot")]
F.append((16, "Von 19 bis 2", f'''
<figure class="xfoto x-nacht">{"".join(img(n, "74vw", "55% 40%", "x-st" + (" an" if i == 0 else ""), lazy=i > 0) for i, (_, n) in enumerate(NACHT))}</figure><div class="xhof"></div>
{spalte()}
<div class="x-uhr" aria-hidden="true">{"".join(f'<span data-n="{i}">{h}</span>' for i, (h, _) in enumerate(NACHT))}<i class="x-marke"></i></div>'''))

# 17 Ins Glas: beim Scrollen geht es hinein in den Negroni, bis alles rot ist
F.append((17, "Ins Glas", f'''
<div class="x-buehne">{eb("glas-negroni-frei", "x-glas", ALT["glas-negroni"])}<div class="x-rot"></div>{spalte()}</div>'''))

# 18 Getippt: der Satz wird geschrieben, als würdest du ihn gerade sagen
buch = []
k = 0
for zl in ["Du sagst,", "was du magst."]:
    teile = []
    for ch in zl:
        teile.append(f'<span class="b" style="--k:{k}">{html.escape(ch) if ch != " " else "&nbsp;"}</span>')
        k += 1
    buch.append(f'<span class="x-zl">{"".join(teile)}</span>')
F.append((18, "Getippt", f'''
<div class="xt">{logo(0)}<h1 class="T x-tipp" aria-label="Du sagst, was du magst.">{"".join(buch)}<i class="x-cursor"></i></h1>{block()}</div>
{fig("momo-lacht", "40vw", "50% 30%")}'''))

# 19 Filmstreifen: der Abend als Film, schräg durchs Bild
FILM = ["schild", "momo-giesst", "glas-coupe", "freundinnen", "konzert-love", "negroni", "voll", "glas-sour", "tuer-rot"]
F.append((19, "Filmstreifen", f'''
<div class="x-oben">{logo(0)}{titel()}</div>
<div class="x-film" aria-hidden="true"><div class="x-spur">{"".join(fig(n, "22vw", "50% 40%") for n in FILM * 2)}</div></div>
<div class="x-unten">{satz(3)}<div>{zeile(4)}{knoepfe(5)}</div></div>'''))

# 20 Stillleben: Momo und seine Drinks freigestellt im Raum, jedes Stück auf eigener Tiefe
F.append((20, "Stillleben", f'''
{spalte()}
<div class="x-still" aria-hidden="true"><i class="x-kante"></i>
<div class="x-e x-momo" data-t="10">{eb("momo-giesst-frei")}</div>
<div class="x-e x-g1" data-t="24">{eb("glas-coupe-frei")}</div>
<div class="x-e x-g2" data-t="34">{eb("glas-negroni-frei")}</div>
<div class="x-e x-g3" data-t="18">{eb("glas-sour-frei")}</div></div>'''))

NAMEN = [(0, "Heute")] + [(n, name) for n, name, _ in F]
STAND = time.strftime("%d%H%M")


def seite(nr, name, inhalt=None):
    s = INDEX
    if inhalt is not None:
        s = s[:KOPF.start()] + f'<header class="auftakt auf h20 x{nr:02d}" id="auftakt">{inhalt}\n</header>' + s[KOPF.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    s = s.replace('</head>', f'<link rel="stylesheet" href="_varianten/hero-20/hero20.css?v={STAND}">'
                             f'<link rel="stylesheet" href="_varianten/hero-15/varianten-nav.css?v={STAND}"></head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Auftakt · ", 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / 20</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};'
                             f'window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");</script>'
                             f'<script src="_varianten/hero-15/varianten-nav.js?v={STAND}"></script>'
                             f'<script src="_varianten/hero-20/hero20.js?v={STAND}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for nr, name, inhalt in F:
    seite(nr, name, inhalt)
print("gebaut:", len(F) + 1, "Seiten")
