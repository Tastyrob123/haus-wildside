#!/usr/bin/env python3
"""Die Pairing-Karte · Walk on the Wild Side Hannover: Bilder der Karten nach satz/bild/ (01.11.2026). Zur Laufzeit lädt nichts aus _quelle/.
  · Valentinsreihe: die Zeichnungen der Bar aus der Valentinskarte 2026 (Leopard mit Herzen und Cocktailglas, Cocktailglas allein;
    _quelle/valentin/leopard-2x.jpg, coupe-2x.jpg, freigestellt vom Rosa des Originals, Linien und Farben unverändert)
  · Angebot für Feiern: Fotos der Bar aus website/assets/bild/ (Neon «No Negroni without Campari», Gläser, Sours, Negroni)

    python3 _werkzeuge/carte/bilder_satz.py
"""
import os
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
Q = os.path.join(HAUS, '_quelle', 'valentin')
WEB = os.path.join(HAUS, 'website', 'assets', 'bild')
AUS = os.path.join(HIER, 'satz', 'bild')
ROSA = (254, 225, 230)   # Grund der Valentinskarte (gemessen)


def freistellen(quelle, ziel, breite):
    im = Image.open(os.path.join(Q, quelle)).convert('RGB')
    w, h = im.size
    px = im.load()
    aus = Image.new('RGBA', (w, h))
    po = aus.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            d = ((r - ROSA[0]) ** 2 + (g - ROSA[1]) ** 2 + (b - ROSA[2]) ** 2) ** .5
            a = min(1.0, max(0.0, (d - 14) / 46))
            if a <= 0:
                po[x, y] = (0, 0, 0, 0)
                continue
            c = [min(255, max(0, round((v - (1 - a) * bg) / a))) for v, bg in zip((r, g, b), ROSA)]
            po[x, y] = (c[0], c[1], c[2], round(a * 255))
    if w > breite:
        aus = aus.resize((breite, round(h * breite / w)), Image.LANCZOS)
    aus.save(os.path.join(AUS, ziel), 'PNG', optimize=True)


def foto(schluessel, ziel, breite=900):
    b = sorted(int(f[len(schluessel) + 1:-5]) for f in os.listdir(WEB) if f.startswith(schluessel + '-') and f[len(schluessel) + 1:-5].isdigit())
    g = max([x for x in b if x <= 1000] or [b[0]])
    im = Image.open(os.path.join(WEB, '%s-%d.webp' % (schluessel, g))).convert('RGB')
    if im.width > breite:
        im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    im.save(os.path.join(AUS, ziel), 'WEBP', quality=84)


if __name__ == '__main__':
    os.makedirs(AUS, exist_ok=True)
    freistellen('leopard-2x.jpg', 'leopard.png', 700)
    freistellen('coupe-2x.jpg', 'coupe.png', 420)
    for k in ('an-campari', 'an-sours', 'an-glaeser', 'an-negroni'):
        foto(k, k + '.webp')
    print('\n'.join(sorted(os.listdir(AUS))))
