#!/usr/bin/env python3
"""Werkbank Wild Side: letzter Farbgang (31.10.2026, Vorlage sb_farbe.py des Culinarium, dort Schäfli). Jede fremde Farbe der Bausteine, die noch in den
gebauten Seiten steht, wird auf die Töne der Bar umgerechnet (website/assets/wild.css): dunkel wird Nacht und Platte, die Mitte Gold des Eckschilds,
hell Creme der weissen Plakate. Helligkeit bleibt. Fotos werden nicht angefasst, nur Text in CSS und HTML. Mehrfach anwendbar."""
import colorsys, glob, os, re

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
# Wild Side (31.10.2026): Töne der Bar aus website/assets/wild.css und dem Markenbuch: Nacht #130E0D, Platte #1C1513/#261E1A, Holz #33281F, Creme #F2E9DC,
# Gold #D8B264 (tief #A07F3A, Messing #B08A43), Rot #F0323F nur als Punkt. Dunkel wird Nacht, die Mitte Gold, hell Creme.
FEST = {'#fd9964': '#d8b264', '#e8875a': '#d8b264', '#fec7aa': '#e7cf98', '#c42e13': '#a07f3a', '#a8260f': '#a07f3a', '#e0a96a': '#d8b264', '#7d433a': '#33281f', '#e6007e': '#e6007e',
        '#ef7649': '#d8b264', '#f5a689': '#e7cf98', '#b15736': '#b08a43', '#16151a': '#130e0d', '#16141b': '#130e0d', '#3a3845': '#33281f', '#faf4f4': '#f2e9dc', '#8953a9': '#d8b264'}
HAUS = {(0x13, 0x0e, 0x0d), (0x1c, 0x15, 0x13), (0x26, 0x1e, 0x1a), (0x33, 0x28, 0x1f), (0xf2, 0xe9, 0xdc), (0xe7, 0xdc, 0xcb), (0xd9, 0xcb, 0xb6), (0xf7, 0xf1, 0xe7),
        (0xd8, 0xb2, 0x64), (0xa0, 0x7f, 0x3a), (0xb0, 0x8a, 0x43), (0xf0, 0x32, 0x3f), (0x1b, 0x15, 0x12), (0xed, 0xe4, 0xd8), (0x6e, 0x5d, 0x4e), (0x1a, 0x00, 0xaa), (0xd2, 0x1c, 0x0a)}


def _ton(r, g, b):
    if (r, g, b) in HAUS:
        return r, g, b
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    grad = h * 360
    if s < .1 or l > .985 or l < .02 or not (grad <= 70 or 195 <= grad <= 248 or grad >= 350):
        return r, g, b
    if l < .45:          # Nacht und Platte der Bar
        nh, ns = 14 / 360, .19
    elif l < .86:        # Gold des Eckschilds
        nh, ns = 40 / 360, .6
    else:                # Creme der weissen Plakate
        nh, ns = 36 / 360, .5
    nr, ng, nb = colorsys.hls_to_rgb(nh, l, ns)
    return round(nr * 255), round(ng * 255), round(nb * 255)


_blau = _ton


def faerbe(t):
    def hexf(m):
        x = m.group(1)
        if len(x) == 3:
            x = ''.join(c * 2 for c in x)
        if len(x) != 6:
            return m.group(0)
        k = '#' + x.lower()
        if k in FEST:
            return FEST[k]
        return '#%02x%02x%02x' % _blau(*(int(x[i:i + 2], 16) for i in (0, 2, 4)))
    t = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![0-9a-fA-F-])', hexf, t)
    t = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', lambda m: '%s(%d,%d,%d' % ((m.group(1),) + _blau(int(m.group(2)), int(m.group(3)), int(m.group(4)))), t)
    return t


def nur_style(t):
    """In HTML nur <style>-Blöcke und style=""-Werte umrechnen, nie Text, Adressen oder eingebettete Bilder."""
    t = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t, flags=re.S)
    t = re.sub(r'(style=")([^"]*)(")', lambda m: m.group(1) + faerbe(m.group(2)) + m.group(3), t)
    t = re.sub(r'(<meta name="theme-color" content=")(#[0-9a-fA-F]{6})', lambda m: m.group(1) + faerbe(m.group(2)), t)
    t = re.sub(r'(<svg\b.*?</svg>)', lambda m: faerbe(m.group(1)) if 'data:image' not in m.group(1) else m.group(1), t, flags=re.S)
    return t


def ohne_fett(t):
    """Nie fett (Tasty-Sprache Stufe 2 Nr. 8): kräftige Schnitte werden Medium, Titel bleiben Regular."""
    t = re.sub(r'font-weight:\s*(?:600|700|800|900|bold)\b', 'font-weight:500', t)
    return re.sub(r'(font:\s*)(?:600|700|800|900|bold)\b', r'\g<1>500', t)


def anwenden():
    n = 0
    for p in glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.css'), recursive=True):
        a = open(p, encoding='utf-8').read(); b = ohne_fett(faerbe(a))
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    seiten = (glob.glob(os.path.join(ROOT, 'werkbank', '**', '*.html'), recursive=True)
              + [os.path.join(ROOT, d, 'index.html') for d in ('befund',)])   # Wild Side: nur das eigene Revier (die übrigen Seiten bauen andere Agenten)
    for p in seiten:
        if not os.path.exists(p):
            continue
        a = open(p, encoding='utf-8').read(); b = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + ohne_fett(m.group(2)) + m.group(3), nur_style(a), flags=re.S)
        if a != b:
            open(p, 'w', encoding='utf-8').write(b); n += 1
    return n


if __name__ == '__main__':
    print('umgefärbt:', anwenden(), 'Dateien')
