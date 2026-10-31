#!/usr/bin/env python3
"""Nach papier_seiten.py (Kit): Drucksachen- und Untersetzer-Seite in den Worten des Hauses (Werkbank Papier, 31.10.2026).
Gleich grosse Stücke «je 94 mm», Du statt Sie, ß; die Drucksachen-Seite sagt, woher die zwanzig fertigen Stücke kommen (Plakatwerkstatt),
Bilder laden sofort (kein lazy, WebKit-Prüfung), Vorschaubild je Seite unter <seite>/img/vorschau.webp für die Startseite der Werkbank.
Aufruf: python3 _werkbank/papier_nach.py (im Ordner website/_werkbank)."""
import json, os, re
from PIL import Image

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEHR = json.load(open(os.path.join(HIER, '_werkbank', 'papier_mehr.json'), encoding='utf-8'))['druck'] if os.path.exists(os.path.join(HIER, '_werkbank', 'papier_mehr.json')) else []
ZAHL = {20: 'zwanzig', 5: 'fünf', 12: 'zwölf'}


def nach(ordner, fn=None):
    p = os.path.join(HIER, ordner, 'index.html')
    if not os.path.exists(p):
        return
    t = open(p, encoding='utf-8').read()
    n = re.sub(r'(\d+) bis \1 mm', r'je \1 mm', t).replace('und Ihre Unterlagen im selben Stil', 'und eure Unterlagen im selben Stil').replace('Originalgrösse', 'Originalgröße')
    n = n.replace(' loading="lazy" decoding="async"', ' decoding="async"').replace(' loading="lazy"', '')
    if fn:
        n = fn(n)
    if n != t:
        open(p, 'w', encoding='utf-8').write(n)
        print('papier-nach:', ordner)


def drucksachen(t):
    k = len(MEHR)
    alt = 'Papier, das bei euch an der Theke, an der Tür oder im Umschlag landen könnte. Was nicht passt, lasst ihr einfach weg.'
    neu = (f'Fünf Ideen für Papier im Stil der Bar, dazu die {ZAHL.get(k, k)} Drucksachen, die die Plakatwerkstatt schon fertig gesetzt hat: '
           'Plakate, Karten, Aufsteller, Flyer und Gutschein, jede als PDF zum Herunterladen. Was nicht passt, lasst ihr einfach weg.')
    t = t.replace(alt, neu)
    # Abschnitte der Plakatwerkstatt: Knopf heisst «PDF herunterladen» und lädt die Datei
    for d in MEHR:
        a = t.find(f'id="{d["id"]}"')
        if a < 0:
            continue
        b = t.find('</section>', a)
        teil = t[a:b].replace('Als PDF ansehen', 'PDF herunterladen').replace(f'href="pdf/{d["pdf"]}"', f'href="pdf/{d["pdf"]}" download')
        t = t[:a] + teil + t[b:]
    return t


def vorschau(ordner, quelle, breite=1200):
    """ein Vorschaubild je Seite für das Kapitel Papier der Werkbank"""
    q = os.path.join(HIER, ordner, 'img', quelle)
    if os.path.exists(q):
        im = Image.open(q)
        if im.width > breite:
            im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
        im.save(os.path.join(HIER, ordner, 'img', 'vorschau.webp'), 'WEBP', quality=86)


if __name__ == '__main__':
    nach('untersetzer')
    nach('drucksachen', drucksachen)
    vorschau('untersetzer', 'u03.webp')
    vorschau('drucksachen', 'karte.webp')
