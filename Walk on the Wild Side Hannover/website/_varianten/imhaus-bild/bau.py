#!/usr/bin/env python3
"""Walk on the Wild Side · «Im selben Haus»: acht Bildsätze zur Wahl (29.10.2026).
Robert: «Die Bilder passen alle nicht zusammen … das muss richtig luxuriös und elegant und edel sein.»
Erst wählt Robert die Bilder (Nummer), dann folgt die Anordnung. Je Seite ein Satz aus Rudis eigenen Fotos in derselben ruhigen Darstellung.
00 = heute. Wechsel mit ← →. Aufruf: python3 bau.py"""
import json, re, html, time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
INDEX = (WEB / "index.html").read_text()
SEK = re.search(r'<section class="kap auf" id="imhaus">.*?</section>', INDEX, re.S)
S = SEK.group(0)
KOPF = re.search(r'(<div class="kz sw".*?</h2>)', S, re.S).group(1)
SCHLUSS = re.search(r'(<p class="ueber sw".*?</p>)', S, re.S).group(1)
PFEIL = re.search(r'(<svg viewBox="0 0 24 24".*?</svg>)', S, re.S).group(1)
E = []
for a in re.findall(r'<a class="platte schild.*?</a>', S, re.S):
    E.append(dict(href=re.search(r'href="([^"]+)"', a).group(1), etikett=re.search(r'<span class="etikett">(.*?)</span>', a).group(1),
                  titel=re.search(r'<h3 class="titel">(.*?)</h3>', a).group(1), text=re.search(r'<p class="text">(.*?)</p>', a).group(1),
                  weiter=re.search(r'<span class="weiter">(.*?) <svg', a).group(1)))

ALT = {"c-tafel-kerzen": "Die lange Tafel im Kerzenlicht, gedeckt für den Abend", "c-tafel-voll": "Gäste an der langen Tafel",
       "c-tafel-gin": "Die gedeckte Tafel mit Kerze und Flasche", "c-teller-hell": "Ein Teller des Abends von oben",
       "c-teller-dunkel": "Ein Teller des Abends auf dunklem Tisch", "c-sauce": "Die Sauce wird am Tisch angegossen",
       "c-gaeste": "Gäste stossen an der Tafel an", "c-knoedel": "Ein Teller des Abends",
       "d-coupe": "Ein Drink und Dirty Chicken auf dem Tresen", "d-tresen": "Dirty Chicken und ein Drink auf dem Tresen",
       "d-burger": "Ein Dirty-Chicken-Sandwich mit Pommes", "f-shots": "Gäste stossen mit Mexikanern an",
       "f-momo": "Momo mixt für einen Gast", "f-glas": "Ein Drink wird über den Tisch gereicht"}
POS = {"c-tafel-kerzen": "40% 50%", "f-shots": "50% 35%", "f-momo": "45% 40%"}
SAETZE = [("c-tafel-kerzen", "d-coupe", "f-shots"), ("c-teller-hell", "d-tresen", "f-momo"), ("c-tafel-voll", "d-burger", "f-shots"),
          ("c-sauce", "d-coupe", "f-momo"), ("c-teller-dunkel", "d-tresen", "f-glas"), ("c-gaeste", "d-burger", "f-momo"),
          ("c-tafel-gin", "d-coupe", "f-shots"), ("c-knoedel", "d-tresen", "f-glas")]


def bild(n):
    return (f'<figure class="bs-f"><img src="_varianten/imhaus-bild/b/{n}-900.webp?v=1" srcset="_varianten/imhaus-bild/b/{n}-900.webp?v=1 900w, '
            f'_varianten/imhaus-bild/b/{n}-1600.webp?v=1 1600w" sizes="30vw" alt="{html.escape(ALT[n])}" decoding="async" style="object-position:{POS.get(n, "50% 50%")}"></figure>')


def rumpf(satz):
    return '<div class="bs-reihe">' + "".join(
        f'<a class="bs-k" href="{e["href"]}" style="--n:{i}">{bild(n)}<div class="bs-t"><span class="etikett">{e["etikett"]}</span>'
        f'<h3 class="titel">{e["titel"]}</h3><p class="text">{e["text"]}</p><span class="weiter">{e["weiter"]} {PFEIL}</span></div></a>'
        for i, (e, n) in enumerate(zip(E, satz))) + '</div>'


NAMEN = [(0, "Heute")] + [(i + 1, f"Bildsatz {i + 1}") for i in range(len(SAETZE))]
STAND = time.strftime("%d%H%M")
CSS = """
.bs .bs-reihe{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,2.4vw,40px);margin-top:40px}
.bs .bs-k{display:flex;flex-direction:column;color:var(--text)}
.bs .bs-f{position:relative;margin:0;aspect-ratio:4/5;overflow:hidden;border-radius:4px;background:var(--nacht3)}
.bs .bs-f::after{content:"";position:absolute;inset:0;border-radius:4px;box-shadow:inset 0 0 0 1px rgba(216,178,100,.28);pointer-events:none}
.bs .bs-f img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none;transform:scale(1.08);transition:transform 2.4s var(--k2)}
.bs.da .bs-f img{transform:none} .bs .bs-k:hover .bs-f img{transform:scale(1.03)}
.bs .bs-t{padding:26px 4px 0}
.bs .bs-t .etikett{display:block;margin-bottom:12px}
.bs .bs-t .titel{font-size:clamp(28px,2.7vw,40px);line-height:1.05}
.bs .bs-t .text{margin-top:14px;font-size:16px}
.bs .bs-t .weiter{margin-top:20px}
@media (max-width:760px){.bs .bs-reihe{grid-template-columns:minmax(0,1fr);gap:36px}}
"""
(HIER / "bs.css").write_text(CSS)


def seite(nr, name, satz=None):
    s = INDEX
    if satz:
        neu = f'<section class="kap auf bs" id="imhaus"><div class="innen">\n{KOPF}\n{rumpf(satz)}\n{SCHLUSS}</div></section>'
        s = s[:SEK.start()] + neu + s[SEK.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    s = s.replace('</head>', f'<link rel="stylesheet" href="_varianten/imhaus-bild/bs.css?v={STAND}"><link rel="stylesheet" href="_varianten/hero-15/varianten-nav.css?v={STAND}"></head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Im selben Haus · ", 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / {len(SAETZE):02d}</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");'
                             f'if(!sessionStorage.getItem("vnav-stelle"))sessionStorage.setItem("vnav-stelle",JSON.stringify({{id:"imhaus",off:-40}}));</script>'
                             f'<script src="_varianten/hero-15/varianten-nav.js?v={STAND}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for i, satz in enumerate(SAETZE):
    seite(i + 1, f"Bildsatz {i + 1}", satz)
print("gebaut:", len(SAETZE) + 1)
