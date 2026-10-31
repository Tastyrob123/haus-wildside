#!/usr/bin/env python3
"""Walk on the Wild Side · 15 Fassungen des Auftakts (29.10.2026).
Jede Fassung ist die echte Startseite, nur der Auftakt ist getauscht. 00 = heutiger Stand.
Wechsel mit den Pfeiltasten ← → (varianten-nav.js), Schild unten links.
Aufruf: python3 bau.py  → schreibt 00.html … 15.html in diesen Ordner."""
import json, re, html
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
BILD = WEB / "assets" / "bild"
INDEX = (WEB / "index.html").read_text()

# ---------- Bausteine aus der echten Seite (Text, Logo, Knöpfe 1:1)
LOGO = re.search(r'(<svg viewBox="0 0 1296 1600".*?</svg>)', INDEX, re.S).group(1)
KNOEPFE = re.search(r'<div class="knoepfe sw" style="--i:5">(.*?)</div></div>\n<p class="at-weiter', INDEX, re.S).group(1)
SATZ = "Eine Nachbarschafts-Mixology-Bar in Linden-Mitte. Es gibt keine Karte: Du sagst Momo, was du magst, und er mixt dir deinen Drink."
ZEITEN = "Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr"
ORT = "Haasemannstraße 13 · Linden"

ALT = {
    "schild-ecke": "Die Hausecke bei Nacht mit dem beleuchteten Schild",
    "schild": "Das beleuchtete Schild an der Hausecke: Walk on the Wild Side",
    "decke-2017": "Die bedruckte Gewölbe-Decke über der Bar",
    "decke-hoch": "Die Gewölbe-Decke über der Rückbar",
    "decke-raum": "Der Raum unter der Decke, links die Rückbar",
    "momo-giesst": "Momo giesst einen Drink ab",
    "momo-lacht": "Momo hinter der Theke unter der NEGRONI-Schrift",
    "glas-coupe": "Ein Drink mit Schaum im Coupe-Glas",
    "freundinnen": "Zwei Gäste an der Theke",
    "negroni": "Die Glühbirnen-Schrift NEGRONI über der Vitrine",
    "glas-rot": "Ein roter Drink im Kerzenlicht",
    "fenster": "Blick durchs Fenster in die Bar",
    "tuer-rot": "Der Eingang bei Nacht im roten Licht",
    "glas-sour": "Ein Sour auf der Theke",
    "voll": "Ein voller Abend unter der Decke",
    "gast-havn": "Ein Gast an der Theke",
    "konzert-love": "Konzert vor der Glühbirnen-Schrift love",
    "schaum": "Schaum wird auf einen Drink gegeben",
    "glas-negroni": "Ein Negroni auf dem Tisch",
    "theke": "Die Theke unter der Decke",
    "glas-trinkt": "Ein Gast trinkt aus dem Glas",
    "anstossen": "Zwei Gläser stossen an",
    "glas-kerze": "Ein Drink im Kerzenlicht",
    "paloma": "Flaschen auf der Theke",
    "saengerin": "Die Sängerin am Mikrofon",
    "glas-zwei": "Zwei Drinks auf dem Tisch",
    "silvester": "Ein Glas Sekt an Silvester",
    "tafel-glaeser": "Momo seiht Drinks für eine Tafel ab",
    "rueckbar-breit": "Die Rückbar mit den Flaschen",
}


def info(name):
    return json.loads((BILD / f"{name}.json").read_text())


def img(name, sizes="100vw", pos="50% 50%", eager=True, cls=""):
    j = info(name)
    st = j["stufen"]
    srcset = ", ".join(f"assets/bild/{f}?v=28103 {w}w" for w, f in st)
    mitte = next((f for w, f in st if w >= 960), st[-1][1])
    lade = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/bild/{mitte}?v=28103" srcset="{srcset}" sizes="{sizes}" '
            f'alt="{html.escape(ALT.get(name, ""))}" {lade} width="{j["w"]}" height="{j["h"]}" style="object-position:{pos}">')


def bild(name, sizes="50vw", pos="50% 50%", cls="bild", stil=""):
    s = f' style="{stil}"' if stil else ""
    return f'<figure class="{cls}"{s}>{img(name, sizes, pos)}</figure>'


def titel(zeilen, cls="T", start=1):
    z = "".join(f'<span class="z"><span style="--i:{start + i}">{t}</span></span>' for i, t in enumerate(zeilen))
    return f'<h1 class="{cls}"><span class="zl">{z}</span></h1>'


def logo(i=0, cls="logo"):
    return f'<a class="{cls} sw" style="--i:{i}" href="index.html" aria-label="Walk on the Wild Side">{LOGO}</a>'


def satz(i=3):
    return f'<p class="satz sw" style="--i:{i}">{SATZ}</p>'


def zeile(i=4):
    return (f'<div class="zeile sw" style="--i:{i}"><span class="etikett">{ZEITEN}</span>'
            f'<span class="trenner"></span><span class="ort">{ORT}</span></div>')


def knoepfe(i=5):
    return f'<div class="knoepfe sw" style="--i:{i}">{KNOEPFE}</div>'


def block(i=3):
    return satz(i) + zeile(i + 1) + knoepfe(i + 2)


TITEL2 = ["Du sagst,", "was du magst."]

# ---------- Wellen der SESSION-Plakate (für 06), senkrecht kachelbar über 800 Einheiten
def wellen():
    import math
    n, breite, hoehe, periode = 7, 600, 1600, 400
    pfade = []
    for k in range(n):
        mx = breite * (k + .5) / n
        w = breite / n * .3
        phi = k * .9
        links, rechts = [], []
        for y in range(0, hoehe + 1, 10):
            dx = 26 * math.sin(2 * math.pi * y / periode + phi)
            links.append(f"{mx - w + dx:.1f},{y}")
            rechts.append(f"{mx + w + dx:.1f},{y}")
        pfade.append("M" + " L".join(links) + " L" + " L".join(reversed(rechts)) + "Z")
    return (f'<svg viewBox="0 0 {breite} {hoehe}" preserveAspectRatio="none" aria-hidden="true">'
            + "".join(f'<path d="{p}"/>' for p in pfade) + "</svg>")


def licht_titel():
    """04: jeder Buchstabe eine Glühbirne, die nacheinander angeht."""
    n = 0
    zeilen = []
    for t in TITEL2:
        teile = []
        for ch in t:
            if ch == " ":
                teile.append(" ")
                continue
            teile.append(f'<span class="b" data-c="{html.escape(ch)}" style="--d:{n}">{html.escape(ch)}</span>')
            n += 1
        zeilen.append(f'<span class="lz">{"".join(teile)}</span>')
    return f'<h1 class="T licht" aria-label="Du sagst, was du magst.">{"".join(zeilen)}</h1>'


# ---------- Die 15 Fassungen: (Nummer, Name, HTML im Auftakt)
F = []

F.append((1, "Das Eckschild", f'''
<div class="htafel"><div class="rahmen" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<div class="tinnen">{logo(0)}{titel(TITEL2)}{block()}</div></div>
{bild("schild-ecke", "38vw", "48% 40%")}'''))

F.append((2, "Das Gewölbe", f'''
<div class="gewoelbe" aria-hidden="true">{img("decke-2017", "110vw", "50% 50%")}</div>
<div class="mitte">{logo(0)}{titel(TITEL2)}{block()}</div>'''))

F.append((3, "Drei Bilder", f'''
<div class="hdrei">{bild("momo-giesst", "34vw", "55% 45%")}{bild("glas-coupe", "40vw", "50% 55%")}{bild("freundinnen", "34vw", "50% 40%")}</div>
<div class="unten">{titel(TITEL2)}<div class="rechts">{logo(1)}{block(2)}</div></div>'''))

F.append((4, "Das Licht geht an", f'''
{bild("negroni", "42vw", "40% 45%")}
<div class="htext">{logo(0)}{licht_titel()}{block()}</div>'''))

WORTE = ["bitter.", "sauer.", "rauchig.", "süss.", "was du magst."]
F.append((5, "Was magst du?", f'''
<div class="htext">{logo(0)}<p class="frage etikett sw" style="--i:1">Was magst du?</p>
<h1 class="T"><span class="zl"><span class="z"><span style="--i:1">Du sagst,</span></span></span>
<span class="wechsel" aria-label="was du magst.">{"".join(f'<span class="w{" ende" if i == len(WORTE) - 1 else ""}">{w}</span>' for i, w in enumerate(WORTE))}<span class="mass">was du magst.</span></span></h1>
{block()}</div>
{bild("momo-lacht", "42vw", "50% 30%")}'''))

F.append((6, "Die Welle", f'''
<div class="htext">{logo(0)}{titel(TITEL2)}{block()}</div>
<div class="welle">{wellen()}{bild("glas-rot", "30vw", "50% 50%")}</div>'''))

F.append((7, "Hineingehen", f'''
<div class="buehne"><div class="htext">{logo(0)}{titel(TITEL2)}{block()}</div>
{bild("fenster", "48vw", "50% 55%")}</div>'''))

F.append((8, "19 Uhr", f'''
{bild("tuer-rot", "42vw", "50% 50%")}
<div class="htext"><p class="ab etikett sw" style="--i:0">Donnerstag bis Samstag, ab</p>
<p class="uhr sw" style="--i:0" aria-label="19 Uhr"><span data-uhr>18:45</span></p>
{titel(TITEL2)}{block()}</div>'''))

BAND = ["glas-sour", "voll", "gast-havn", "konzert-love", "schaum", "freundinnen", "decke-raum", "glas-negroni"]
spur = "".join(bild(n, "26vw", "50% 45%") for n in BAND)
F.append((9, "Das Band", f'''
<div class="oben">{titel(["Du sagst, was du magst."], start=0)}</div>
<div class="band" aria-hidden="true"><div class="spur">{spur}{spur}</div></div>
<div class="unten">{logo(2)}<div class="mitte">{satz(3)}{zeile(4)}</div>{knoepfe(5)}</div>'''))

F.append((10, "Das Schild in der Hand", f'''
<div class="htext">{logo(0)}{titel(TITEL2)}{block()}</div>
<div class="stube"><div class="hkarte">{bild("schild", "34vw", "50% 40%")}</div></div>'''))

F.append((11, "Das Raster", f'''
<div class="zelle htext">{logo(0)}{titel(TITEL2)}{block()}</div>
{bild("voll", "40vw", "50% 55%", "bild b1")}{bild("theke", "20vw", "50% 40%", "bild b2")}{bild("glas-trinkt", "20vw", "50% 45%", "bild b3")}'''))

F.append((12, "Bild in der Schrift", f'''
<div class="schrift"><h1 class="T"><span class="zl"><span class="z"><span style="--i:0" class="klein">Du sagst, was du</span></span>
<span class="z"><span style="--i:1" class="gross">magst.</span></span></span></h1></div>
<div class="unten">{logo(2)}<div class="mitte">{satz(3)}{zeile(4)}</div>{knoepfe(5)}</div>
<img class="vorlader" src="assets/bild/decke-2017-2048.webp?v=28103" alt="" aria-hidden="true">'''))

F.append((13, "Das Licht folgt dir", f'''
<div class="lampe"><figure class="bild">{img("decke-raum", "44vw", "50% 35%")}</figure><div class="kegel" aria-hidden="true"></div></div>
<div class="htext">{logo(0)}{titel(TITEL2)}{block()}</div>'''))

A = ["anstossen", "glas-kerze", "momo-giesst", "glas-coupe"]
B = ["saengerin", "glas-zwei", "negroni", "silvester"]
F.append((14, "Gegenlauf", f'''
<div class="htext">{logo(0)}{titel(TITEL2)}{block()}</div>
<div class="spalten" aria-hidden="true"><div class="sp sa">{"".join(bild(n, "23vw") for n in A)}</div><div class="sp sb">{"".join(bild(n, "23vw") for n in B)}</div></div>'''))

F.append((15, "Das weisse Plakat", f'''
<div class="oben">{logo(0, "logo stempel")}<div class="rechts">{titel(TITEL2)}{block()}</div></div>
<div class="hreihe">{bild("tafel-glaeser", "25vw", "50% 50%")}{bild("glas-negroni", "25vw", "50% 55%")}{bild("konzert-love", "25vw", "50% 40%")}{bild("freundinnen", "25vw", "50% 40%")}</div>'''))

NAMEN = [(0, "Heute")] + [(n, name) for n, name, _ in F]

# ---------- Zusammensetzen
KOPF_ALT = re.search(r'<header class="auftakt auf" id="auftakt">.*?</header>', INDEX, re.S)
assert KOPF_ALT, "Auftakt nicht gefunden"


def seite(nr, name, inhalt=None):
    s = INDEX
    if inhalt is not None:
        neu = f'<header class="auftakt auf h15 v{nr:02d}" id="auftakt">{inhalt}\n</header>'
        s = s[:KOPF_ALT.start()] + neu + s[KOPF_ALT.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    kopf = ('<link rel="stylesheet" href="_varianten/hero-15/hero.css?v=' + STAND + '">'
            '<link rel="stylesheet" href="_varianten/hero-15/varianten-nav.css?v=' + STAND + '">')
    s = s.replace('</head>', kopf + '</head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Auftakt · ", 1)
    fuss = (f'<p class="vschild"><b>{nr:02d} / 15</b><span>{html.escape(name)}</span><i>← →</i></p>'
            f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};'
            f'window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");</script>'
            f'<script src="_varianten/hero-15/varianten-nav.js?v={STAND}"></script>'
            f'<script src="_varianten/hero-15/hero.js?v={STAND}"></script>')
    s = s.replace("</body>", fuss + "</body>", 1)
    (HIER / f"{nr:02d}.html").write_text(s)


import time
STAND = time.strftime("%d%H%M")
seite(0, "Heute")
for nr, name, inhalt in F:
    seite(nr, name, inhalt)
print("gebaut:", len(F) + 1, "Seiten")
