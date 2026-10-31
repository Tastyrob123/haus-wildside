#!/usr/bin/env python3
"""Walk on the Wild Side · «Im selben Haus» (Vitrine): Fassungen nur für die kleine Zeile über den Titeln (29.10.2026).
Robert: «diese kleine Überschriften darüber … da muss was sein, aber so wie es jetzt ist, ist es irgendwie nicht schön.»
Alles andere bleibt wie in der echten Seite. 00 = heute. Wechsel mit ← →. Aufruf: python3 bau.py"""
import json, re, html, time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
INDEX = (WEB / "index.html").read_text()
assert len(INDEX) > 10000, "index.html leer (läuft gerade ein Bau?)"
SEK = re.search(r'<section class="kap auf" id="imhaus">.*?</section>', INDEX, re.S)
S = SEK.group(0)
assert 'class="vitrine"' in S


def nach_kante(s, cls):
    """Zeile aus dem Text nehmen und als eigenes Schild in den Bildteil setzen (über der Goldkante)."""
    def f(m):
        a = m.group(0)
        et = re.search(r'<span class="etikett">(.*?)</span>', a).group(1)
        a = a.replace(f'<span class="etikett">{et}</span>', '', 1)
        return a.replace('<div class="vi-text">', f'<span class="{cls}">{et}</span></div><div class="vi-text">'.replace('</div><div class="vi-text">', '<div class="vi-text">'), 1) if False else \
            re.sub(r'(<div class="vi-spiegel".*?</div>)(</div>)', lambda n: n.group(1) + f'<span class="{cls}">{et}</span>' + n.group(2), a, count=1, flags=re.S)
    return re.sub(r'<a class="vi-stueck".*?</a>', f, s, flags=re.S)


def roemisch(s):
    z = iter(["I", "II", "III"])
    return re.sub(r'<span class="etikett">(.*?)</span>', lambda m: f'<span class="etikett vi-rz"><b>{next(z)}</b><i></i>{m.group(1)}</span>', s)


F = [
    (1, "In der Titelschrift", None, ".vi-text .etikett{font:400 clamp(18px,1.5vw,22px)/1.2 var(--titel);letter-spacing:.01em;text-transform:none;color:var(--gold);margin-bottom:10px}"),
    (2, "Titelschrift mit Strichen", None, ".vi-text .etikett{display:inline-flex!important;align-items:center;gap:14px;font:400 clamp(17px,1.4vw,21px)/1.2 var(--titel);letter-spacing:.01em;text-transform:none;color:var(--gold)}"
     ".vi-text .etikett::before,.vi-text .etikett::after{content:'';width:clamp(24px,2.4vw,40px);height:1px;background:var(--gold);opacity:.7}"),
    (3, "Unter dem Titel", None, ".vi-text .etikett{order:2;margin:10px 0 0!important;font:400 clamp(18px,1.5vw,22px)/1.2 var(--titel);letter-spacing:.01em;text-transform:none;color:var(--gold)}"
     ".vi-text .titel{order:1} .vi-text .text{order:3} .vi-text .weiter{order:4}"),
    (4, "Auf der Goldkante", lambda s: nach_kante(s, "vi-schild"),
     ".vi-bild{position:relative} .vi-schild{position:absolute;z-index:2;left:50%;top:calc(100% - clamp(70px,7vw,110px));transform:translate(-50%,-50%);padding:0 18px;background:var(--nacht);"
     "font:500 11.5px/1 var(--lauf);letter-spacing:.2em;text-transform:uppercase;color:var(--gold);white-space:nowrap} .vi-text{padding-top:18px}"),
    (5, "Im Spiegel eingraviert", lambda s: nach_kante(s, "vi-gravur"),
     ".vi-bild{position:relative} .vi-gravur{position:absolute;z-index:2;left:0;right:0;top:calc(100% - clamp(70px,7vw,110px) / 2);transform:translateY(-50%);text-align:center;"
     "font:400 clamp(17px,1.5vw,22px)/1 var(--titel);letter-spacing:.04em;color:var(--gold);opacity:.85;text-shadow:0 1px 0 rgba(0,0,0,.6)} .vi-text{padding-top:10px}"),
    (6, "Mit römischer Zahl", roemisch,
     ".vi-text .etikett.vi-rz{display:inline-flex!important;align-items:center;gap:12px;font:400 clamp(17px,1.4vw,21px)/1.2 var(--titel);letter-spacing:.01em;text-transform:none;color:var(--gold)}"
     ".vi-rz b{font-weight:400} .vi-rz i{display:block;width:34px;height:1px;background:var(--gold);opacity:.7}"),
    (7, "Leise", None, ".vi-text .etikett{font:400 14px/1.3 var(--lauf);letter-spacing:.02em;text-transform:none;color:var(--text3);margin-bottom:8px}"),
    (8, "Linie mit Lücke", None, ".vi-text .etikett{align-self:stretch;display:flex!important;align-items:center;gap:16px;margin-bottom:18px!important}"
     ".vi-text .etikett::before,.vi-text .etikett::after{content:'';flex:1;height:1px;background:var(--gold-l)}"),
    (9, "Messingschild", lambda s: nach_kante(s, "vi-messing"),
     ".vi-bild{position:relative} .vi-messing{position:absolute;z-index:2;left:50%;top:calc(100% - clamp(70px,7vw,110px));transform:translate(-50%,-50%);padding:9px 18px 8px;border-radius:2px;"
     "background:linear-gradient(180deg,#E4C67E,#B38D45);box-shadow:inset 0 1px 0 rgba(255,255,255,.45),0 8px 18px -8px rgba(0,0,0,.8);"
     "font:500 10.5px/1 var(--lauf);letter-spacing:.2em;text-transform:uppercase;color:#2A1F12;white-space:nowrap} .vi-text{padding-top:20px}"),
    (10, "Kapitälchen", None, ".vi-text .etikett{font:400 clamp(16px,1.3vw,19px)/1.2 var(--titel);font-variant:small-caps;text-transform:lowercase;letter-spacing:.14em;color:var(--gold)}"),
    (11, "Kurze Linie darunter", None, ".vi-text .etikett{margin-bottom:0!important}"
     ".vi-text .etikett::after{content:'';display:block;width:28px;height:1px;background:var(--gold);margin:14px auto 16px}"),
    (12, "Creme statt Gold", None, ".vi-text .etikett{font:500 10.5px/1 var(--lauf);letter-spacing:.32em;color:rgba(237,228,216,.62);margin-bottom:16px}"),
]
NAMEN = [(0, "Heute")] + [(n, name) for n, name, _, _ in F]
STAND = time.strftime("%d%H%M")


def seite(nr, name, umbau=None, css=""):
    s = INDEX
    if nr:
        neu = umbau(S) if umbau else S
        neu = neu.replace('class="kap auf" id="imhaus"', f'class="kap auf et{nr:02d}" id="imhaus"', 1)
        s = s[:SEK.start()] + neu + s[SEK.end():]
        css = "#imhaus " + css.replace("} ", "} #imhaus ").replace("}.", "} #imhaus .").replace("}#", "} #")
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    s = s.replace('</head>', f'<style>{css}</style><link rel="stylesheet" href="_varianten/hero-15/varianten-nav.css?v={STAND}"></head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Im selben Haus · ", 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / {len(F):02d}</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");'
                             f'if(!sessionStorage.getItem("vnav-stelle"))sessionStorage.setItem("vnav-stelle",JSON.stringify({{id:"imhaus",off:-40}}));</script>'
                             f'<script src="_varianten/hero-15/varianten-nav.js?v={STAND}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for nr, name, umbau, css in F:
    seite(nr, name, umbau, css)
print("gebaut:", len(F) + 1)
