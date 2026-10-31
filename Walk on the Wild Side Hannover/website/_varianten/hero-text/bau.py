#!/usr/bin/env python3
"""Walk on the Wild Side · 15 Textanordnungen auf dem heutigen Auftakt (29.10.2026).
Robert: Hintergrundbild und Logo bleiben, nur die Texte und Knöpfe werden anders dargestellt («dieses Linksbündige … holt nicht ab»).
Foto, Verlauf, Schleier, Bewegung des Bildes bleiben wie heute; nur der Inhalt von .innen wechselt. 00 = heute. Wechsel mit ← →.
Aufruf: python3 bau.py"""
import json, re, html, time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
INDEX = (WEB / "index.html").read_text()
KOPF = re.search(r'<header class="auftakt auf" id="auftakt">.*?</header>', INDEX, re.S)
H = KOPF.group(0)

BILD = H[:H.index('<div class="innen">')]          # Header-Anfang, Foto, Verlauf, Schleier: unverändert
LOGO = re.search(r'(<a class="at-logo sw".*?</a>)', H, re.S).group(1)
KNOEPFE = re.search(r'(<div class="knoepfe sw" style="--i:5">.*?</div>)</div>\n<p class="at-weiter', H, re.S).group(1)
RES, HEUTE = re.findall(r'(<a class="knopf[^"]*".*?</a>)', KNOEPFE, re.S)
PFEIL = re.search(r'(<svg viewBox="0 0 24 24".*?</svg>)', RES, re.S).group(1)
WEITER = re.search(r'(<p class="at-weiter sw".*?</p>)', H, re.S).group(1)
SATZ = "Eine Nachbarschafts-Mixology-Bar in Linden-Mitte. Es gibt keine Karte: Du sagst Momo, was du magst, und er mixt dir deinen Drink."
ZEILE = re.search(r'(<div class="at-zeile sw".*?</div>)', H, re.S).group(1)


def titel(zeilen, start=1, cls="titel at-titel"):
    z = "".join(f'<span class="z"><span style="--i:{start + i}">{t}</span></span>' for i, t in enumerate(zeilen))
    return f'<h1 class="{cls}"><span class="zl">{z}</span></h1>'


def satz(i=3, text=SATZ, cls="at-satz"):
    return f'<p class="{cls} sw" style="--i:{i}">{text}</p>'


def zeile(i=4):
    return ZEILE.replace('style="--i:4"', f'style="--i:{i}"')


def knoepfe(i=5, inhalt=None):
    return f'<div class="knoepfe sw" style="--i:{i}">{inhalt or (RES + HEUTE)}</div>'


def logo(i=0):
    return LOGO.replace('style="--i:0"', f'style="--i:{i}"')


T2 = ["Du sagst,", "was du magst."]
T1 = ["Du sagst, was du magst."]

F = [
    (1, "Über die ganze Breite",
     f'<div class="t-oben">{logo(0)}{satz(1)}<div class="t-r">{zeile(2)}{knoepfe(3)}</div></div>{titel(T1, 4)}',
     WEITER),
    (2, "Treppe",
     f'{logo(0)}{titel(["Du", "sagst,", "was du", "magst."])}<div class="t-fuss">{satz(5)}{zeile(6)}{knoepfe(7)}</div>',
     WEITER),
    (3, "Wie ein Zeitungskopf",
     f'<div class="t-unten">{titel(T2)}<div class="t-r">{satz(3)}{knoepfe(4)}</div></div>',
     f'<div class="t-kopf sw" style="--i:0">{LOGO.replace(" sw", "").replace("at-logo", "at-logo t-mlogo")}<span class="etikett">Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr</span><span class="ort">Haasemannstraße 13 · Linden</span></div>'),
    (4, "Keine Karte",
     f'{logo(0)}<p class="etikett t-dach sw" style="--i:1">Eine Nachbarschafts-Mixology-Bar in Linden-Mitte</p>{titel(["Es gibt keine Karte."], 2)}'
     f'<p class="t-antwort sw" style="--i:3">Du sagst Momo, was du magst,<br>und er mixt dir deinen Drink.</p>{zeile(4)}{knoepfe(5)}',
     WEITER),
    (5, "Mit Zeiten-Spalte",
     f'<div class="t-zwei"><div>{logo(0)}{titel(T2)}{satz(3)}</div><div class="t-spalte sw" style="--i:4">'
     f'<div class="t-z"><span class="etikett">Donnerstag</span><b>19 bis 1 Uhr</b></div><div class="t-z"><span class="etikett">Freitag</span><b>19 bis 2 Uhr</b></div>'
     f'<div class="t-z"><span class="etikett">Samstag</span><b>19 bis 2 Uhr</b></div><div class="t-z"><span class="etikett">Wo</span><b>Haasemannstraße 13</b></div>'
     f'{knoepfe(5)}</div></div>',
     WEITER),
    (6, "Knöpfe als Zeilen",
     f'{logo(0)}{titel(T2)}{satz(3)}{zeile(4)}<nav class="t-wege sw" style="--i:5" aria-label="Weiter">'
     f'<a class="t-weg rot" href="besuch.html#reservieren"><span>Platz reservieren</span><i>{PFEIL}</i></a>'
     f'<a class="t-weg" href="programm.html"><span>Heute Abend</span><i>{PFEIL}</i></a></nav>',
     WEITER),
    (7, "Breit statt hoch",
     f'{logo(0)}<div class="t-zwei">{titel(T2)}{satz(3)}</div><div class="t-band sw" style="--i:4">{ZEILE.replace(" sw", "")}{KNOEPFE.replace(" sw", "")}</div>',
     WEITER),
    (8, "Zweifarbig, Knöpfe am Titel",
     f'{logo(0)}<div class="t-reihe">{titel(T2)}{knoepfe(3)}</div>{satz(4)}{zeile(5)}',
     WEITER),
    (9, "Mittig, Knöpfe links und rechts",
     f'{logo(0)}{titel(T2)}<div class="t-flanke">{RES.replace("class=\"knopf rot\"", "class=\"knopf rot sw\" style=\"--i:4\"")}{satz(3)}{HEUTE.replace("class=\"knopf \"", "class=\"knopf sw\" style=\"--i:5\"")}</div>{zeile(6)}',
     ""),
    (10, "Fliesstext",
     f'{logo(0)}<div class="t-fluss"><h1 class="titel t-gross"><span class="zl"><span class="z"><span style="--i:1">Du sagst,</span></span><span class="z"><span style="--i:2">was du magst.</span></span></span></h1>'
     + "".join(f'<span class="t-w" style="--w:{i}">{w}</span> ' for i, w in enumerate(SATZ.split()))
     + f'</div>{zeile(4)}{knoepfe(5)}',
     WEITER),
    (11, "Laufband unten",
     f'{logo(0)}{titel(T2)}{satz(3)}{knoepfe(4)}',
     '<div class="t-lauf" aria-label="Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr, Haasemannstraße 13, Linden"><div class="t-spur">'
     + "".join('<span>Donnerstag 19 bis 1 Uhr</span><i>·</i><span>Freitag und Samstag 19 bis 2 Uhr</span><i>·</i><span>Haasemannstraße 13 · Linden</span><i>·</i><span>Ein Abend an der Ecke, von 19 bis 2 Uhr</span><i>·</i>' for _ in range(4))
     + '</div></div>'),
    (12, "Gross und klein",
     f'{logo(0)}<h1 class="titel at-titel t-gk"><span class="zl"><span class="z t-g"><span style="--i:1">Du sagst,</span></span><span class="z t-k"><span style="--i:2">was du magst.</span></span></span></h1>'
     f'<div class="t-fuss">{satz(3)}{zeile(4)}{knoepfe(5)}</div>',
     WEITER),
    (13, "Rote Linie",
     f'{logo(0)}<h1 class="titel at-titel"><span class="zl"><span class="z"><span style="--i:1">Du sagst,</span></span><span class="z t-strich"><span style="--i:2">was du magst.'
     '<svg class="t-linie" viewBox="0 0 600 40" preserveAspectRatio="none" aria-hidden="true"><path d="M6 28 C 120 14, 260 34, 390 20 S 560 12, 594 22" pathLength="1"/></svg></span></span></span></h1>'
     f'{satz(3)}{zeile(4)}{knoepfe(5)}',
     WEITER),
    (14, "Zeiten senkrecht",
     f'<div class="t-senk sw" style="--i:0" aria-hidden="true"><span>Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr</span><i></i><span>Haasemannstraße 13 · Linden</span></div>'
     f'<div class="t-haupt">{logo(0)}{titel(T2)}{satz(3)}{knoepfe(4)}</div>',
     WEITER),
    (15, "Als Zitat",
     f'{logo(0)}<div class="t-zitat"><span class="t-qa sw" style="--i:1" aria-hidden="true">„</span>{titel(T2)}<span class="t-qe sw" style="--i:3" aria-hidden="true">“</span></div>'
     f'<p class="etikett t-wer sw" style="--i:3">— Momo</p>{satz(4)}{zeile(5)}{knoepfe(6)}',
     WEITER),
]
NAMEN = [(0, "Heute")] + [(n, name) for n, name, _, _ in F]
STAND = time.strftime("%d%H%M")


def seite(nr, name, kopf=None):
    s = INDEX
    if kopf:
        s = s[:KOPF.start()] + kopf + s[KOPF.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    s = s.replace('</head>', f'<link rel="stylesheet" href="_varianten/hero-text/text.css?v={STAND}">'
                             f'<link rel="stylesheet" href="_varianten/hero-15/varianten-nav.css?v={STAND}"></head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Auftakt · ", 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / 15</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};'
                             f'window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");</script>'
                             f'<script src="_varianten/hero-15/varianten-nav.js?v={STAND}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for nr, name, innen, aussen in F:
    kopf = BILD.replace('class="auftakt auf"', f'class="auftakt auf ht t{nr:02d}"', 1) + f'<div class="innen">{innen}</div>\n{aussen}\n</header>'
    seite(nr, name, kopf)
print("gebaut:", len(F) + 1, "Seiten")
