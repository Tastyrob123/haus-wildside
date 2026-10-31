#!/usr/bin/env python3
"""Bilder für die Bildsätze «Im selben Haus»: Rudis Fotos aus seinem Drive (Culinarium/_quelle/vom-kunden/drive) und vom Dirty-Chicken-Abend.
Dirty Chicken ist bei Tageslicht fotografiert und wird leicht warm gestimmt, damit es neben den Abendbildern steht (Original bleibt unverändert)."""
from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
Q = Path("/Users/robertreff/Desktop/Website-Projekte/Culinarium Hannover/_quelle")
A = Path(__file__).resolve().parent / "b"
BILDER = {
    "c-tafel-kerzen": Q / "vom-kunden/drive/4972.jpg", "c-tafel-voll": Q / "vom-kunden/drive/3901.jpg",
    "c-tafel-gin": Q / "vom-kunden/drive/3842.jpg", "c-teller-hell": Q / "vom-kunden/drive/4238.jpg",
    "c-teller-dunkel": Q / "vom-kunden/drive/4298.jpg", "c-sauce": Q / "vom-kunden/drive/4866.jpg",
    "c-gaeste": Q / "vom-kunden/drive/5005.jpg", "c-knoedel": Q / "vom-kunden/drive/5098.jpg",
    "d-coupe": Q / "dirty-chicken/vom-kunden-2026-10-27/84612.jpg", "d-tresen": Q / "dirty-chicken/vom-kunden-2026-10-27/84611.jpg",
    "d-burger": Q / "dirty-chicken/vom-kunden-2026-10-27/84673.jpg",
    "f-shots": Q / "vom-kunden/drive/4574.jpg", "f-momo": Q / "vom-kunden/drive/4568.jpg", "f-glas": Q / "vom-kunden/drive/4026.jpg",
}
def warm(im):
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.07))); b = b.point(lambda v: int(v * .86)); g = g.point(lambda v: int(v * .98))
    im = Image.merge("RGB", (r, g, b))
    return ImageEnhance.Brightness(ImageEnhance.Contrast(im).enhance(1.06)).enhance(.9)
for n, f in BILDER.items():
    im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
    if n.startswith("d-"): im = warm(im)
    for w in (900, 1600):
        k = im.copy(); k.thumbnail((w, w * 2), Image.LANCZOS)
        k.save(A / f"{n}-{w}.webp", "WEBP", quality=82, method=6)
    print(n, im.size)
