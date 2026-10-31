#!/usr/bin/env python3
"""Walk on the Wild Side · «Im selben Haus»: 15 edle Anordnungen mit Bildsatz 3 (Robert 29.10.2026).
Bilder: culinarium-tafel, dirty-burger, feste-anstossen (Rudis eigene Fotos). Texte, Ziele, Kopf und Schlusssatz wie heute.
Keine der am 29.10. abgelehnten Ordnungen (imhaus-15) wird wiederholt. 00 = heute. Wechsel mit ← →. Aufruf: python3 bau.py"""
import json, re, html, time
from pathlib import Path

HIER = Path(__file__).resolve().parent
WEB = HIER.parent.parent
BILD = WEB / "assets" / "bild"
INDEX = (WEB / "index.html").read_text()
assert len(INDEX) > 10000, "index.html leer (läuft gerade ein Bau?)"
SEK = re.search(r'<section class="kap auf" id="imhaus">.*?</section>', INDEX, re.S)
S = SEK.group(0)
KOPF = re.search(r'(<div class="kz sw".*?</h2>)', S, re.S).group(1)
SCHLUSS = re.search(r'(<p class="ueber sw".*?</p>)', S, re.S).group(1)
PFEIL = re.search(r'(<svg viewBox="0 0 24 24".*?</svg>)', S, re.S).group(1)
E = []
for a in re.findall(r'<a class="platte schild.*?</a>', S, re.S):
    E.append(dict(href=re.search(r'href="([^"]+)"', a).group(1), bild=re.search(r'assets/bild/([a-z-]+)-480\.webp', a).group(1),
                  alt=re.search(r'alt="([^"]*)"', a).group(1), etikett=re.search(r'<span class="etikett">(.*?)</span>', a).group(1),
                  titel=re.search(r'<h3 class="titel">(.*?)</h3>', a).group(1), text=re.search(r'<p class="text">(.*?)</p>', a).group(1),
                  weiter=re.search(r'<span class="weiter">(.*?) <svg', a).group(1)))
assert [e["bild"] for e in E] == ["culinarium-tafel", "dirty-burger", "feste-anstossen"], [e["bild"] for e in E]
C, D, F = E
POS = {"culinarium-tafel": "50% 50%", "dirty-burger": "50% 58%", "feste-anstossen": "50% 34%"}


def img(e, sizes="34vw", pos=None):
    j = json.loads((BILD / f"{e['bild']}.json").read_text())
    st = j["stufen"]
    srcset = ", ".join(f"assets/bild/{f} {w}w" for w, f in st)
    mitte = next((f for w, f in st if w >= 960), st[-1][1])
    return (f'<img src="assets/bild/{mitte}" srcset="{srcset}" sizes="{sizes}" alt="{html.escape(e["alt"])}" decoding="async" '
            f'width="{j["w"]}" height="{j["h"]}" style="object-position:{pos or POS[e["bild"]]}">')


def foto(e, cls="eh-f", sizes="34vw", pos=None):
    return f'<figure class="{cls}">{img(e, sizes, pos)}</figure>'


def teile(e, h="h3"):
    return (f'<span class="etikett">{e["etikett"]}</span><{h} class="titel">{e["titel"]}</{h}>'
            f'<p class="text">{e["text"]}</p><span class="weiter">{e["weiter"]} {PFEIL}</span>')


def text(e, cls="eh-t"):
    return f'<div class="{cls}">{teile(e)}</div>'


def a(e, inner, cls="", n=0):
    return f'<a class="{cls}" href="{e["href"]}" style="--n:{n}">{inner}</a>'


V = []
# 01 Galerie: drei gerahmte Abzüge hängen an der Wand, darunter je ein Schild wie im Museum
V.append((1, "Galerie an der Wand", '<div class="eh-galerie">' + "".join(
    a(e, f'<div class="eh-rahmen">{foto(e, sizes="28vw")}</div>{text(e)}', "eh-g", i) for i, e in enumerate(E)) + '</div>'))
# 02 Passepartout: ein heller Rahmen hält alle drei Bilder, darunter drei Texte auf der Mitte
V.append((2, "Passepartout", '<div class="eh-pp"><div class="eh-pp-matte">' + "".join(a(e, foto(e, sizes="30vw"), "eh-ppb", i) for i, e in enumerate(E))
          + '</div><div class="eh-pp-texte">' + "".join(a(e, text(e), "", i) for i, e in enumerate(E)) + '</div></div>'))
# 03 Kinoband: drei Breitbilder übereinander, darunter je eine Zeile im schwarzen Balken
V.append((3, "Kinoband", '<div class="eh-kino">' + "".join(
    a(e, foto(e, sizes="100vw") + f'<div class="eh-balken"><span class="etikett">{e["etikett"]}</span><h3 class="titel">{e["titel"]}</h3><p class="text">{e["text"]}</p><span class="weiter">{e["weiter"]} {PFEIL}</span></div>', "eh-band", i)
    for i, e in enumerate(E)) + '</div>'))
# 04 Doppelseite: wie ein aufgeschlagenes Magazin mit Falz in der Mitte
V.append((4, "Doppelseite", f'''<div class="eh-dop">
<div class="eh-seite links">{a(C, text(C, "eh-t gross"), "", 0)}</div><div class="eh-falz"></div><div class="eh-seite rechts">{a(C, foto(C, sizes="44vw"), "eh-voll", 0)}</div></div>
<div class="eh-dop zwei"><div class="eh-seite links">{a(D, foto(D, sizes="44vw") + text(D), "eh-halb", 1)}</div><div class="eh-falz"></div><div class="eh-seite rechts">{a(F, foto(F, sizes="44vw") + text(F), "eh-halb", 2)}</div></div>'''))
# 05 Mittelachse: alles steht auf der Mitte, Culinarium gross, die Nachbarn links und rechts darunter
V.append((5, "Auf der Mittelachse", f'''<div class="eh-achse">{a(C, foto(C, sizes="62vw", pos="50% 46%") + text(C, "eh-t mitte"), "eh-haupt", 0)}
<div class="eh-neben">{a(D, foto(D, sizes="30vw") + text(D, "eh-t mitte"), "", 1)}<i class="eh-strich"></i>{a(F, foto(F, sizes="30vw") + text(F, "eh-t mitte"), "", 2)}</div></div>'''))
# 06 Säulen: drei Spalten zwischen Goldlinien, oben Name, in der Mitte das Bild, unten der Text
V.append((6, "Säulen mit Goldlinien", '<div class="eh-saeulen">' + "".join(
    a(e, f'<span class="etikett">{e["etikett"]}</span><h3 class="titel">{e["titel"]}</h3>{foto(e, sizes="28vw")}<p class="text">{e["text"]}</p><span class="weiter">{e["weiter"]} {PFEIL}</span>', "eh-s", i)
    for i, e in enumerate(E)) + '</div>'))
# 07 Vitrine: warmes Licht von oben, die Bilder stehen auf einer polierten Kante und spiegeln sich
V.append((7, "Vitrine", '<div class="eh-vitrine"><div class="eh-stuecke">' + "".join(
    a(e, f'<i class="eh-licht"></i>{foto(e, sizes="26vw")}<div class="eh-spiegel" aria-hidden="true">{img(e, "26vw")}</div>', "eh-stueck", i) for i, e in enumerate(E))
    + '</div><div class="eh-vt">' + "".join(a(e, text(e, "eh-t mitte"), "", i) for i, e in enumerate(E)) + '</div></div>'))
# 08 Grosse Anfangsbuchstaben: jede Zeile beginnt mit einer grossen goldenen Initiale wie in einem Buch
V.append((8, "Grosse Initialen", '<div class="eh-init">' + "".join(
    a(e, f'<span class="eh-buch" aria-hidden="true">{e["titel"][0]}</span>{text(e)}{foto(e, sizes="40vw")}', "eh-iz", i)
    for i, e in enumerate(E)) + '</div>'))
# 09 Hauptbild mit zwei Begleitern: links Culinarium hoch, rechts die beiden Nachbarn übereinander, alles auf einer Platte
V.append((9, "Hauptbild mit Begleitern", f'''<div class="eh-haupt-platte platte">{a(C, foto(C, sizes="40vw") + text(C, "eh-t gross"), "eh-hp", 0)}
<div class="eh-begleiter">{a(D, foto(D, sizes="16vw") + text(D), "eh-b", 1)}<i class="eh-linie"></i>{a(F, foto(F, sizes="16vw") + text(F), "eh-b", 2)}</div></div>'''))
# 10 Sprossenfenster: ein Fenster wie das Eckschild, schwarz mit Goldrahmen, drei Scheiben mit den Bildern
V.append((10, "Sprossenfenster", '<div class="eh-fenster"><div class="eh-scheiben">' + "".join(a(e, foto(e, sizes="30vw"), "eh-scheibe", i) for i, e in enumerate(E))
          + '</div></div><div class="eh-ft">' + "".join(a(e, text(e), "", i) for i, e in enumerate(E)) + '</div>'))
# 11 Verzeichnis und Bildwand: links die drei Namen gross untereinander, rechts eine geschlossene Wand aus den drei Bildern
V.append((11, "Verzeichnis und Bildwand", '<div class="eh-vz"><div class="eh-vz-l">' + "".join(a(e, text(e), "eh-vz-e", i) for i, e in enumerate(E))
          + '</div><div class="eh-vz-w">' + "".join(a(e, foto(e, sizes="24vw"), f"eh-w{i}", i) for i, e in enumerate(E)) + '</div></div>'))
# 12 Hell und dunkel: die Bilder stehen auf der Kante zwischen der dunklen Bar und einer hellen Fläche, die Texte stehen im Hellen
V.append((12, "Auf der Kante hell und dunkel", '<div class="eh-kante2">' + "".join(a(e, foto(e, sizes="30vw") + text(e), "eh-kz", i) for i, e in enumerate(E)) + '</div>'))
# 13 Halbdunkel: die Bilder kommen aus dem Dunkel, nur die Mitte ist im Licht
V.append((13, "Halbdunkel", '<div class="eh-dunkel">' + "".join(
    a(e, f'<figure class="eh-f">{img(e, "30vw")}<i class="eh-vign"></i></figure>{text(e, "eh-t mitte")}', "eh-dk", i) for i, e in enumerate(E)) + '</div>'))
# 14 Das Prisma: drei Bilder auf einem Prisma, es dreht sich zum nächsten; daneben wechselt der Text
V.append((14, "Das Prisma", f'''<div class="eh-prisma"><div class="eh-p-raum"><div class="eh-p-koerper">{"".join(foto(e, "eh-f eh-p-seite", "40vw") for e in E)}</div></div>
<div class="eh-p-texte">{"".join(a(e, text(e, "eh-t gross"), "eh-pt" + (" an" if i == 0 else ""), i) for i, e in enumerate(E))}
<div class="eh-p-reiter">{"".join(f'<button type="button" data-n="{i}"{" class=an" if i == 0 else ""}>{e["etikett"]}</button>' for i, e in enumerate(E))}</div></div></div>'''))
# 15 Unten bündig: drei Bilder verschiedener Höhe stehen auf einer Linie, die Texte füllen den Raum darüber
V.append((15, "Unten bündig", '<div class="eh-buendig">' + "".join(a(e, text(e) + foto(e, sizes="30vw"), f"eh-bd h{i}", i) for i, e in enumerate(E)) + '</div><div class="eh-boden"></div>'))

NAMEN = [(0, "Heute")] + [(n, name) for n, name, _ in V]
STAND = time.strftime("%d%H%M")


def seite(nr, name, rumpf=None):
    s = INDEX
    if rumpf is not None:
        neu = f'<section class="kap auf eh e{nr:02d}" id="imhaus"><div class="innen">\n{KOPF}\n{rumpf}\n{SCHLUSS}</div></section>'
        s = s[:SEK.start()] + neu + s[SEK.end():]
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8"><base href="../../">', 1)
    s = s.replace('</head>', f'<link rel="stylesheet" href="_varianten/imhaus-edel/edel.css?v={STAND}"><link rel="stylesheet" href="_varianten/hero-15/varianten-nav.css?v={STAND}"></head>', 1)
    s = s.replace("<title>", f"<title>{nr:02d} {name} · Im selben Haus · ", 1)
    s = s.replace("</body>", f'<p class="vschild"><b>{nr:02d} / 15</b><span>{html.escape(name)}</span><i>← →</i></p>'
                             f'<script>window.VARIANTEN={json.dumps(NAMEN, ensure_ascii=False)};window.VNR={nr};window.VORD=location.pathname.replace(/\\/[^\\/]*$/,"");'
                             f'if(!sessionStorage.getItem("vnav-stelle"))sessionStorage.setItem("vnav-stelle",JSON.stringify({{id:"imhaus",off:-40}}));</script>'
                             f'<script src="_varianten/hero-15/varianten-nav.js?v={STAND}"></script><script src="_varianten/imhaus-edel/edel.js?v={STAND}"></script></body>', 1)
    (HIER / f"{nr:02d}.html").write_text(s)


seite(0, "Heute")
for nr, name, rumpf in V:
    seite(nr, name, rumpf)
print("gebaut:", len(V) + 1)
