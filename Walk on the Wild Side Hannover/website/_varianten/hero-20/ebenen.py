#!/usr/bin/env python3
"""Bildebenen für die 20 Auftakt-Fassungen: Freisteller (Apple Vision, lokal), Schild nach seinen Ecken, Unschärfe, Dunkel, Schwarzweiss."""
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
from pathlib import Path
H = Path(__file__).resolve().parent
B = H.parent.parent / "assets" / "bild"
E = H / "ebene"; E.mkdir(exist_ok=True)

def spar(im, name, q=82):
    im.save(E / f"{name}.webp", "WEBP", quality=q, method=6)

def trim(im):
    return im.crop(im.getchannel("A").getbbox())

# Schild: Ecken im 960er Bild gemessen, auf 1536 hochgerechnet
foto = Image.open(B / "schild-1536.webp").convert("RGBA")
f = 1536 / 960
ecken = [(218*f, 183*f), (545*f, 196*f), (565*f, 570*f), (240*f, 550*f)]
m = Image.new("L", foto.size, 0); ImageDraw.Draw(m).polygon(ecken, fill=255)
m = m.filter(ImageFilter.GaussianBlur(1.2))
sch = foto.copy(); sch.putalpha(m)
spar(sch, "schild-ebene")                     # volle Bildgrösse, deckungsgleich mit dem Foto
# Schild gerade gezogen (Vorderseite des Kastens)
w, h = 900, 1010
def koeff(src, dst):
    import numpy as np
    A = []; b = []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u*x, -u*y], [0, 0, 0, x, y, 1, -v*x, -v*y]]; b += [u, v]
    return list(np.linalg.solve(np.array(A, float), np.array(b, float)))
gerade = foto.convert("RGB").transform((w, h), Image.PERSPECTIVE, koeff(ecken, [(0, 0), (w, 0), (w, h), (0, h)]), Image.BICUBIC)
spar(gerade, "schild-gerade", 88)
# dunkle Fassung des Schild-Fotos (Licht aus)
dunkel = ImageEnhance.Brightness(foto.convert("RGB")).enhance(.1)
spar(dunkel, "schild-dunkel", 70)

# Vision-Freisteller zuschneiden
for n in ["momo-giesst", "momo-lacht", "glas-negroni", "glas-coupe", "glas-sour"]:
    im = Image.open(H / "frei" / f"{n}.png").convert("RGBA")
    t = trim(im)
    t.thumbnail((1400, 1400))
    spar(t, f"{n}-frei", 86)
# deckungsgleiche volle Ebenen (Momo, Sour) für Fassungen mit Foto darunter
for n, w0 in [("momo-giesst", 1536), ("glas-sour", 1600)]:
    im = Image.open(H / "frei" / f"{n}.png").convert("RGBA")
    im = im.resize((w0, round(im.height * w0 / im.width)), Image.LANCZOS)
    spar(im, f"{n}-ebene", 86)
# Schwarzweiss-Momo wie auf den SESSION-Plakaten
g = Image.open(E / "momo-giesst-frei.webp").convert("RGBA")
a = g.getchannel("A"); sw = ImageOps.grayscale(g.convert("RGB")); sw = ImageEnhance.Contrast(sw).enhance(1.25).convert("RGBA"); sw.putalpha(a)
spar(sw, "momo-sw-frei", 86)
# Unschärfe für «Schärfe zieht auf»
s = Image.open(B / "glas-sour-1600.webp").convert("RGB")
spar(s.filter(ImageFilter.GaussianBlur(16)), "sour-weich", 72)
gl = Image.open(E / "glas-sour-ebene.webp").convert("RGBA")
spar(gl.filter(ImageFilter.GaussianBlur(10)), "sour-glas-weich", 80)
print("fertig:", sorted(p.name for p in E.iterdir()))

# Decke als Fläche über dem Kopf: hinten (unten im Bild) läuft sie ins Dunkel der Bar aus
d = Image.open(B / "decke-2017-2048.webp").convert("RGB")
nacht = Image.new("RGB", d.size, (19, 14, 13))
maske = Image.new("L", (1, 256))
for y in range(256):
    t = max(0, (y / 255 - .45) / .55)
    maske.putpixel((0, y), int(255 * min(1, t ** 1.4)))
maske = maske.resize(d.size)
spar(Image.composite(nacht, d, maske), "decke-tunnel", 80)
print("Decke fertig")
