#!/usr/bin/env python3
"""Walk on the Wild Side · 15 Variationen des heutigen Auftakts (29.10.2026, Robert: «finde so wie es heute ist am besten»).
Grundgestalt bleibt: Nachtfoto über den Schirm, Logo, «Du sagst, was du magst.», Satz, Zeiten, zwei Knöpfe, Schleier hebt sich.
Je Fassung ändert sich eine Sache (Bild, Seite, Grösse, Ordnung). 00 = heute. Wechsel mit ← →.
Aufruf: python3 bau.py"""
import json, re, html, time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
BILD = WEB / "assets" / "bild"
INDEX = (WEB / "index.html").read_text()
KOPF = re.search(r'<header class="auftakt auf" id="auftakt">.*?</header>', INDEX, re.S)
H = KOPF.group(0)

# ---------- Teile des heutigen Auftakts, 1:1
LOGO = re.search(r'(<a class="at-logo sw".*?</a>)', H, re.S).group(1)
TITEL = re.search(r'(<h1 class="titel at-titel">.*?</h1>)', H, re.S).group(1)
SATZ = re.search(r'(<p class="at-satz sw".*?</p>)', H, re.S).group(1)
ZEILE = re.search(r'(<div class="at-zeile sw".*?</div>)', H, re.S).group(1)
KNOEPFE = re.search(r'(<div class="knoepfe sw" style="--i:5">.*?</div>)</div>\n<p class="at-weiter', H, re.S).group(1)
WEITER = re.search(r'(<p class="at-weiter sw".*?</p>)', H, re.S).group(1)

ALT = {
    "schild": "Das beleuchtete Schild an der Hausecke: Walk on the Wild Side",
    "schild-ecke": "Die Hausecke bei Nacht mit dem beleuchteten Schild",
    "momo-giesst": "Momo giesst einen Drink ab",
    "voll": "Ein voller Abend unter der Decke",
    "tuer-rot": "Der Eingang bei Nacht im roten Licht",
    "negroni": "Die Glühbirnen-Schrift NEGRONI über der Vitrine",
}


def foto(name):
    j = json.loads((BILD / f"{name}.json").read_text())
    st = j["stufen"]
    srcset = ", ".join(f"assets/bild/{f}?v=28103 {w}w" for w, f in st)
    gross = st[-1][1] if st[-1][0] <= 1600 else next(f for w, f in st if w >= 1600)
    return (f'<figure class="at-bild" style="--lq:url({j["lq"]});"><img src="assets/bild/{gross}?v=28103" srcset="{srcset}" sizes="100vw" '
            f'alt="{html.escape(ALT[name])}" fetchpriority="high" decoding="async" width="{j["w"]}" height="{j["h"]}"></figure>'
            f'<div class="at-hof"></div><div class="schleier"></div>')


def auftakt(nr, bild="schild", innen=None, aussen=WEITER):
    innen = innen if innen is not None else LOGO + TITEL + SATZ + ZEILE + KNOEPFE
    return (f'<header class="auftakt auf hh w{nr:02d}" id="auftakt">\n{foto(bild)}\n'
            f'<div class="innen">{innen}</div>\n{aussen}\n</header>')


TITEL3 = ('<h1 class="titel at-titel"><span class="zl"><span class="z"><span style="--i:1">Du sagst,</span></span>'
          '<span class="z"><span style="--i:2">was du</span></span><span class="z"><span style="--i:3">magst.</span></span></span></h1>')
ZEITEN_GROSS = ('<div class="at-zeile gross sw" style="--i:4"><span class="zg">Donnerstag 19 bis 1 Uhr</span>'
                '<span class="zg">Freitag und Samstag 19 bis 2 Uhr</span><span class="ort">Haasemannstraße 13 · Linden</span></div>')

F = [
    (1, "Grösser", auftakt(1)),
    (2, "Gespiegelt", auftakt(2)),
    (3, "Die Ecke von weiter weg", auftakt(3, "schild-ecke")),
    (4, "Momo an der Theke", auftakt(4, "momo-giesst")),
    (5, "Der volle Raum", auftakt(5, "voll")),
    (6, "Der Eingang", auftakt(6, "tuer-rot")),
    (7, "Die Glühbirnen", auftakt(7, "negroni")),
    (8, "Drei Zeilen", auftakt(8, innen=LOGO + TITEL3 + SATZ + ZEILE + KNOEPFE)),
    (9, "Zeichen neben dem Titel", auftakt(9, innen=f'<div class="kopfreihe">{LOGO}{TITEL}</div>' + SATZ + ZEILE + KNOEPFE)),
    (10, "Mittig", auftakt(10, "schild-ecke", aussen="")),
    (11, "Oben", auftakt(11)),
    (12, "Harte Kante", auftakt(12)),
    (13, "Gerahmt wie das Schild", auftakt(13)),
    (14, "Zeiten gross", auftakt(14, innen=LOGO + TITEL + SATZ + ZEITEN_GROSS + KNOEPFE)),
    (15, "Leiste unten", auftakt(15, innen=LOGO + TITEL + SATZ,
                                 aussen=f'<div class="at-band sw" style="--i:4"><div class="innen">{ZEILE}{KNOEPFE}</div></div>')),
]
NAMEN = [(0, "Heute")] + [(n, name) for n, name, _ in F]
STAND = time.strftime("%d%H%M")


def seite(nr, name, kopf=None):
    s = INDEX
    if kopf:
        s = s[:KOPF.start()] + kopf + s[KOPF.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    s = s.replace('</head>', f'<link rel="stylesheet" href="_varianten/hero-heute/heute.css?v={STAND}">'
                             f'<link rel="stylesheet" href="_varianten/hero-heute/varianten-nav.css?v={STAND}"></head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Auftakt · ", 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / 15</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};'
                             f'window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");</script>'
                             f'<script src="_varianten/hero-heute/varianten-nav.js?v={STAND}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for nr, name, kopf in F:
    seite(nr, name, kopf)
print("gebaut:", len(F) + 1, "Seiten")
