#!/usr/bin/env python3
"""Nach papier_seiten.py (Kit): Drucksachen- und Untersetzer-Seite in den Worten des Hauses (Werkbank Papier, 31.10.2026).
Gleich grosse Stücke «je 94 mm», Du statt Sie, ß; die Drucksachen-Seite sagt, woher die zwanzig fertigen Stücke kommen (Plakatwerkstatt),
Bilder laden sofort (kein lazy, WebKit-Prüfung), Vorschaubild je Seite unter <seite>/img/vorschau.webp für die Startseite der Werkbank.
Aufruf: python3 _werkbank/papier_nach.py (im Ordner website/_werkbank)."""
import json, os, re
from PIL import Image

HIER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEHR = json.load(open(os.path.join(HIER, '_werkbank', 'papier_mehr.json'), encoding='utf-8'))['druck'] if os.path.exists(os.path.join(HIER, '_werkbank', 'papier_mehr.json')) else []
ZAHL = {20: 'zwanzig', 5: 'fünf', 12: 'zwölf', 13: 'dreizehn', 14: 'vierzehn'}
# Untersetzer neu (1.11.2026): Texte aus haus.py › PAPIER_SEITE passend zu den neuen Motiven
UNTERSETZER_TEXT = [
    ('sechs auf Creme mit roter Wortmarke und den Wellen der Plakate, sechs auf der Nacht der Bar mit Goldlinie.',
     'die Wortmarke gross, vier Fotos der Bar, die Wellen der SESSION-Plakate, Momos Satz, Falstaff und die Zeiten, jedes Motiv genau in der Mitte.'),
    ('Die Wortmarke kommt aus eurem Logo, die Wellen von den SESSION-Plakaten, die Goldlinie vom Eckschild.',
     'Die Wortmarke kommt aus eurem Logo, die Fotos aus der Bar, die Wellen von den SESSION-Plakaten, die Goldlinie vom Eckschild.')]


def untersetzer(t):
    for a, b in UNTERSETZER_TEXT:
        t = t.replace(a, b)
    return t


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
    neu = (f'Fünf Ideen für Papier im Stil der Bar, dazu {ZAHL.get(k, k)} weitere Drucksachen aus der Plakatwerkstatt: '
           'Karten, Aufsteller, Angebote, Flyer und Gutschein, jede als PDF zum Herunterladen. Eure Plakate gestaltet ihr selbst, die stehen hier nicht. Was nicht passt, lasst ihr einfach weg.')
    t = t.replace(alt, neu)
    # Abschnitte der Plakatwerkstatt: Knopf heisst «PDF herunterladen» und lädt die Datei
    for d in MEHR:
        a = t.find(f'id="{d["id"]}"')
        if a < 0:
            continue
        b = t.find('</section>', a)
        teil = t[a:b].replace('Als PDF ansehen', 'PDF herunterladen').replace(f'href="pdf/{d["pdf"]}" download', f'href="pdf/{d["pdf"]}"').replace(' download download', '')
        teil = teil.replace(f'href="pdf/{d["pdf"]}"', f'href="pdf/{d["pdf"]}" download')
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


SEITEN = ('unterlagen', 'drucksachen', 'untersetzer', 'sticker', 'postkarten', 'beigaben')


def nachbau():
    """die Nachbauten der Werkbank (zeile_ganz: kein Wort allein unten, text_mitte: Schrift mittig in Knöpfen) nur über die Papier-Seiten;
    haus.nach_bau macht dasselbe später über alle Seiten, beides ist wiederholbar"""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import zeile_ganz, text_mitte
    for o in SEITEN:
        if os.path.exists(os.path.join(HIER, o, 'index.html')):
            nach(o)
            zeile_ganz.anwenden(os.path.join(HIER, o)); text_mitte.anwenden(os.path.join(HIER, o))
            knopf_mitte(os.path.join(HIER, o, 'index.html'))


def knopf_mitte(pfad):
    """Block aus knopf_mitte.css und knopf_mitte.js nach dem Block von text_mitte.py einfügen (wiederholbar). Für werkbank/ übernehmbar:
    dieselbe Funktion auf jede Seite anwenden, nachdem text_mitte.anwenden gelaufen ist."""
    w = os.path.dirname(os.path.abspath(__file__))
    css = open(os.path.join(w, 'knopf_mitte.css'), encoding='utf-8').read()
    js = open(os.path.join(w, 'knopf_mitte.js'), encoding='utf-8').read().strip()
    # Handy: Seitentitel (Prata 40 px) etwas kleiner, «Eure Unterlagen,» lief in WebKit bei 390 bis 394 px (Tor in Actions, 31.10.2026)
    # 31.10. 21:49: in WebKit ist Prata breiter, bei 9,4vw noch 394 px → 8,6vw (bei 390: 33,5 px)
    css += '\n@media(max-width:480px){h1.t1{font-size:min(36px,8.6vw)!important}}'
    block = f'<style id="knopf-mitte">{css}</style><script id="knopf-mitte-js">{js}</script>'
    t = open(pfad, encoding='utf-8').read()
    t = re.sub(r'<style id="knopf-mitte">.*?</style><script id="knopf-mitte-js">.*?</script>', '', t, flags=re.S)
    i = t.rfind('</body>')
    t = t[:i] + block + t[i:]
    open(pfad, 'w', encoding='utf-8').write(t)


if __name__ == '__main__':
    nach('untersetzer', untersetzer)
    nach('drucksachen', drucksachen)
    vorschau('untersetzer', 'u04.webp')
    vorschau('drucksachen', 'karte.webp')
    nachbau()
