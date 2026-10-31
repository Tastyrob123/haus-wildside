#!/usr/bin/env python3
"""Walk on the Wild Side · 15 Darstellungen des Abschnitts «Im selben Haus» (29.10.2026).
Texte, Bilder und Ziele wie heute; nur die Darstellung wechselt. Kopf (Kapitelzeile, Titel) und Schlusssatz bleiben.
00 = heute. Wechsel mit ← →, man bleibt beim Abschnitt. Aufruf: python3 bau.py"""
import json, re, html, time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
BILD = WEB / "assets" / "bild"
INDEX = (WEB / "index.html").read_text()
SEK = re.search(r'<section class="kap auf" id="imhaus">.*?</section>', INDEX, re.S)
S = SEK.group(0)
KOPF = re.search(r'(<div class="kz sw".*?</h2>)', S, re.S).group(1)
SCHLUSS = re.search(r'(<p class="ueber sw".*?</p>)', S, re.S).group(1)
PFEIL = re.search(r'(<svg viewBox="0 0 24 24".*?</svg>)', S, re.S).group(1)

# Die drei Einträge im Wortlaut von heute
E = []
for a in re.findall(r'<a class="platte schild.*?</a>', S, re.S):
    E.append(dict(
        href=re.search(r'href="([^"]+)"', a).group(1),
        bild=re.search(r'assets/bild/([a-z-]+)-480\.webp', a).group(1),
        alt=re.search(r'alt="([^"]*)"', a).group(1),
        etikett=re.search(r'<span class="etikett">(.*?)</span>', a).group(1),
        titel=re.search(r'<h3 class="titel">(.*?)</h3>', a).group(1),
        text=re.search(r'<p class="text">(.*?)</p>', a).group(1),
        weiter=re.search(r'<span class="weiter">(.*?) <svg', a).group(1),
    ))
assert len(E) == 3


def img(e, sizes="40vw", pos="50% 50%"):
    j = json.loads((BILD / f"{e['bild']}.json").read_text())
    st = j["stufen"]
    srcset = ", ".join(f"assets/bild/{f}?v=29108 {w}w" for w, f in st)
    mitte = next((f for w, f in st if w >= 960), st[-1][1])
    return (f'<img src="assets/bild/{mitte}?v=29108" srcset="{srcset}" sizes="{sizes}" alt="{html.escape(e["alt"])}" '
            f'loading="eager" decoding="async" width="{j["w"]}" height="{j["h"]}" style="object-position:{pos}">')


def foto(e, cls="ih-f", sizes="40vw", pos="50% 50%", stil=""):
    s = f' style="{stil}"' if stil else ""
    return f'<figure class="{cls}"{s}>{img(e, sizes, pos)}</figure>'


def text(e, h="h3", cls="ih-t"):
    return (f'<div class="{cls}"><span class="etikett">{e["etikett"]}</span><{h} class="titel">{e["titel"]}</{h}>'
            f'<p class="text">{e["text"]}</p><span class="weiter">{e["weiter"]} {PFEIL}</span></div>')


def karte(e, i, cls="ih-k", sizes="34vw", pos="50% 50%"):
    return f'<a class="{cls}" href="{e["href"]}" style="--n:{i}">{foto(e, sizes=sizes, pos=pos)}{text(e)}</a>'


C, D, F = E
POS = {"culinarium-teller": "50% 55%", "dirty-chicken": "50% 50%", "silvester": "50% 40%"}
V = []

# 01 Drei hohe Bilder: Wand an Wand, Text darunter; die Bilder steigen nacheinander aus der Kante
V.append((1, "Drei hohe Bilder", f'<div class="ih-drei">{"".join(karte(e, i, pos=POS[e["bild"]]) for i, e in enumerate(E))}</div>'))

# 02 Schachbrett: Bild und Text wechseln sich ab, alle Kanten bündig
V.append((2, "Schachbrett", f'''<div class="ih-schach">
<a class="ih-z bz" href="{C["href"]}" style="--n:0">{foto(C, sizes="30vw", pos=POS[C["bild"]])}</a><a class="ih-z tz" href="{C["href"]}" style="--n:1">{text(C)}</a>
<a class="ih-z bz" href="{D["href"]}" style="--n:2">{foto(D, sizes="30vw")}</a>
<a class="ih-z tz" href="{F["href"]}" style="--n:3">{text(F)}</a><a class="ih-z bz" href="{F["href"]}" style="--n:4">{foto(F, sizes="30vw", pos=POS[F["bild"]])}</a><a class="ih-z tz" href="{D["href"]}" style="--n:5">{text(D)}</a>
</div>'''))

# 03 Im Zickzack: drei Reihen, das Bild wechselt die Seite
V.append((3, "Im Zickzack", '<div class="ih-zz">' + "".join(
    f'<a class="ih-r{" um" if i == 1 else ""}" href="{e["href"]}" style="--n:{i}">{foto(e, sizes="56vw", pos=POS[e["bild"]])}{text(e)}</a>' for i, e in enumerate(E)) + '</div>'))

# 04 Register: die drei Namen gross wie ein Verzeichnis, unter jedem ein Bildband
V.append((4, "Register", '<div class="ih-reg">' + "".join(
    f'<a class="ih-zeile" href="{e["href"]}" style="--n:{i}"><div class="ih-kopf"><span class="etikett">{e["etikett"]}</span><h3 class="titel">{e["titel"]}</h3>'
    f'<div class="ih-rechts"><p class="text">{e["text"]}</p><span class="weiter">{e["weiter"]} {PFEIL}</span></div></div>{foto(e, "ih-f ih-band", "92vw", POS[e["bild"]])}</a>'
    for i, e in enumerate(E)) + '</div>'))

# 05 Ein Bild, drei Zeilen: links die drei Einträge, rechts das grosse Bild, das mit der Zeile wechselt
V.append((5, "Ein Bild, drei Zeilen", f'''<div class="ih-liste"><div class="ih-zeilen">{"".join(
    f'<a class="ih-l{" an" if i == 0 else ""}" href="{e["href"]}" data-n="{i}">{text(e)}</a>' for i, e in enumerate(E))}</div>
<div class="ih-gross">{"".join(foto(e, "ih-f" + (" an" if i == 0 else ""), "44vw", POS[e["bild"]]) for i, e in enumerate(E))}</div></div>'''))

# 06 Fächer: drei Tafeln im Raum, die gezeigte kommt nach vorn
V.append((6, "Fächer", f'<div class="ih-faecher">{"".join(karte(e, i, "ih-k platte", "30vw", POS[e["bild"]]) for i, e in enumerate(E))}</div>'))

# 07 Quer: beim Scrollen fahren die drei seitlich vorbei
V.append((7, "Quer", f'<div class="ih-quer"><div class="ih-buehne"><div class="ih-spur">{"".join(karte(e, i, "ih-k", "46vw", POS[e["bild"]]) for i, e in enumerate(E))}</div></div></div>'))

# 08 Gegenlauf: die mittlere Spalte läuft beim Scrollen gegen die äusseren
V.append((8, "Gegenlauf", f'<div class="ih-gegen">{"".join(karte(e, i, "ih-k" + (" mitte" if i == 1 else ""), "30vw", POS[e["bild"]]) for i, e in enumerate(E))}</div>'))

# 09 Schräg geschnitten: drei Bilder als schräge Streifen, ein Band, der Text folgt der Schräge
V.append((9, "Schräg geschnitten", f'''<div class="ih-schraeg"><div class="ih-streifen">{"".join(
    f'<a class="ih-s" href="{e["href"]}" style="--n:{i}">{foto(e, sizes="40vw", pos=POS[e["bild"]])}</a>' for i, e in enumerate(E))}</div>
<div class="ih-texte">{"".join(f'<a href="{e["href"]}" style="--n:{i}">{text(e)}</a>' for i, e in enumerate(E))}</div></div>'''))

# 10 Hell wie die Plakate der Bar: Creme, rote Etiketten, Bilder Wand an Wand
V.append((10, "Hell wie die Plakate", f'<div class="ih-hell-reihe">{"".join(karte(e, i, "ih-k", "30vw", POS[e["bild"]]) for i, e in enumerate(E))}</div>'))

# 11 Breitbild und Paar: Culinarium randlos breit, darunter die beiden Nachbarn nebeneinander
V.append((11, "Breitbild und Paar", f'''<a class="ih-breit" href="{C["href"]}">{foto(C, sizes="92vw", pos="50% 58%")}{text(C)}</a>
<div class="ih-paar">{karte(D, 1, "ih-k", "20vw")}{karte(F, 2, "ih-k", "20vw", POS[F["bild"]])}</div>'''))

# 12 Im Wechsel: drei Spalten, Bild und Text tauschen von Spalte zu Spalte die Lage
V.append((12, "Im Wechsel", '<div class="ih-wechsel">' + "".join(
    f'<a class="ih-k{" um" if i == 1 else ""}" href="{e["href"]}" style="--n:{i}">{foto(e, sizes="30vw", pos=POS[e["bild"]])}{text(e)}</a>' for i, e in enumerate(E)) + '</div>'))

# 13 Übereinander von Rand zu Rand: drei Bilder in drei Tiefen, sie folgen der Maus; die Texte darunter in einer Reihe
V.append((13, "In drei Tiefen", f'''<div class="ih-tiefe"><div class="ih-ebenen">
<a class="ih-e e1" href="{C["href"]}" data-t="10">{foto(C, sizes="46vw", pos=POS[C["bild"]])}</a>
<a class="ih-e e2" href="{D["href"]}" data-t="24">{foto(D, sizes="26vw")}</a>
<a class="ih-e e3" href="{F["href"]}" data-t="18">{foto(F, sizes="26vw", pos=POS[F["bild"]])}</a></div>
<div class="ih-texte">{"".join(f'<a href="{e["href"]}" style="--n:{i}">{text(e)}</a>' for i, e in enumerate(E))}</div></div>'''))

# 14 Das Bild bleibt stehen: links ein grosses Bild, rechts scrollen die drei Einträge vorbei, das Bild wechselt mit
V.append((14, "Das Bild bleibt stehen", f'''<div class="ih-steht"><div class="ih-links"><div class="ih-halt">{"".join(foto(e, "ih-f" + (" an" if i == 0 else ""), "44vw", POS[e["bild"]]) for i, e in enumerate(E))}</div></div>
<div class="ih-rechts">{"".join(f'<a class="ih-b" href="{e["href"]}" data-n="{i}">{text(e)}</a>' for i, e in enumerate(E))}</div></div>'''))

# 15 Gross, schmal, gross: Culinarium und die Feste breit, Dirty Chicken als schmaler Streifen dazwischen
V.append((15, "Gross, schmal, gross", f'<div class="ih-gsg">{"".join(karte(e, i, "ih-k", ["40vw", "18vw", "40vw"][i], POS[e["bild"]]) for i, e in enumerate(E))}</div>'))

NAMEN = [(0, "Heute")] + [(n, name) for n, name, _ in V]
STAND = time.strftime("%d%H%M")


def seite(nr, name, rumpf=None):
    s = INDEX
    if rumpf is not None:
        hell = " hell" if nr == 10 else ""
        neu = f'<section class="kap auf ihv v{nr:02d}{hell}" id="imhaus"><div class="innen">\n{KOPF}\n{rumpf}\n{SCHLUSS}</div></section>'
        s = s[:SEK.start()] + neu + s[SEK.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    s = s.replace('</head>', f'<link rel="stylesheet" href="_varianten/imhaus-15/imhaus.css?v={STAND}">'
                             f'<link rel="stylesheet" href="_varianten/hero-15/varianten-nav.css?v={STAND}"></head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Im selben Haus · ", 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / 15</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};'
                             f'window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");'
                             f'if(!sessionStorage.getItem("vnav-stelle")&&!location.hash)sessionStorage.setItem("vnav-stelle",JSON.stringify({{id:"imhaus",off:-40}}));</script>'
                             f'<script src="_varianten/hero-15/varianten-nav.js?v={STAND}"></script>'
                             f'<script src="_varianten/imhaus-15/imhaus.js?v={STAND}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for nr, name, rumpf in V:
    seite(nr, name, rumpf)
print("gebaut:", len(V) + 1, "Seiten")
