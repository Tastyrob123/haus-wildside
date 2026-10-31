#!/usr/bin/env python3
"""Kleid des Gästebuchs für Walk on the Wild Side Hannover (31.10.2026): rechnet die Farben der Kopie aus dem Culinarium (Farbwelt «Plakat»,
Nacht-Violett und Kerzenlicht) in das Eckschild der Bar um (Werte wie _werkzeuge/oberflaeche/kleid/wildside.css, aus website/assets/wild.css):
  Nacht-Violett (Farbton 220–280°)                         → Nacht der Bar (Farbton 10°, #130E0D · #1C1513 · #261E1A), Helligkeit bleibt
  Kerze tief (Farbton 0–30°, Sättigung ab 0,3, bis 0,47)   → Gold tief (Farbton 40°, #7A5C24), Betonung auf Hell
  Kerze (0,47 bis 0,72)                                    → Gold (Farbton 40°, #D8B264), Haarlinie, Etikett, Knauf
  Kerze hell (über 0,72)                                   → Gold hell (#E4C88A), Linien und Zeichen auf Dunkel
  Warmweiss (Farbton 0–30°, Sättigung unter 0,3, hell)     → Creme der weissen Plakate (Farbton 36°, #F2E9DC)
Rot der Warnungen (Farbton unter 12°, Sättigung über 0,7), Grau und Grün bleiben. Schriften: Fraunces → Prata (eine Stärke), Instrument Sans und
DM Mono → Hanken Grotesk (Zahlen mit gleich breiten Ziffern), Dateien wie in website/assets/schrift/. Achsen von Fraunces (SOFT, WONK) entfallen.
Einmal angewendet am 31.10.2026 auf die frische Kopie aus dem Culinarium; erneut nur auf frische Kopien (sonst wird doppelt umgerechnet)."""
import colorsys, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATEIEN = ['studio/studio.css', 'studio/hell.css', 'studio/schweben.css', 'reception.css', 'wildside-reception.css', 'gastgeber.css', 'brief-pdf.css',
           'brief-pdf.js', 'reception.js', 'studio/rundgang.js', 'studio/zur-werkbank.js', 'studio/auswahl.js', 'pruefung.html', 'anleitung.html',
           'index.html', 'brief-pdf.html', 'studio/anleitung.js', 'pruefung.js']


def neu_rgb(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hg = h * 360
    if s < 0.03:
        return None
    if 220 <= hg <= 285:                                     # Nacht-Violett → Nacht der Bar
        h2, s2 = 10 / 360, min(max(s * 1.5, 0.08), 0.22)
    elif hg <= 30 or hg >= 345:
        if hg < 12 and s > 0.7 and l < 0.5:                  # Rot der Warnungen bleibt
            return None
        if s >= 0.3:
            if l <= 0.47:
                h2, s2 = 40 / 360, 0.54                      # Gold tief
            elif l <= 0.72:
                h2, s2 = 40 / 360, 0.58                      # Gold
            else:
                h2, s2 = 41 / 360, 0.62                      # Gold hell
        elif l > 0.7:
            h2, s2 = 36 / 360, min(max(s * 2, 0.25), 0.55)   # Warmweiss → Creme
        elif l < 0.3:
            h2, s2 = 10 / 360, min(s, 0.22)                  # dunkle warme Töne zur Nacht
        else:
            return None
    else:
        return None
    r2, g2, b2 = colorsys.hls_to_rgb(h2, l, s2)
    return round(r2 * 255), round(g2 * 255), round(b2 * 255)


def hexe(m):
    t = m.group(1)
    if len(t) == 3:
        t = ''.join(c * 2 for c in t)
    x = neu_rgb(int(t[0:2], 16), int(t[2:4], 16), int(t[4:6], 16))
    return m.group(0) if x is None else '#%02x%02x%02x' % x


def rgba(m):
    x = neu_rgb(int(m.group(2)), int(m.group(3)), int(m.group(4)))
    return m.group(0) if x is None else f'{m.group(1)}({x[0]},{x[1]},{x[2]}{m.group(5)}'


def um(s):
    s = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})(?![0-9a-fA-F\w])', hexe, s)
    s = re.sub(r'(rgba?)\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(\s*[,)])', rgba, s)
    s = re.sub(r'%23([0-9a-fA-F]{6})', lambda m: '%23' + hexe(re.match(r'#(\w+)', '#' + m.group(1)))[1:], s)   # Farben in eingebetteten SVG
    # Schriften: Prata (eine Stärke) statt Fraunces, Hanken statt Instrument Sans und DM Mono; nie fett, nie kursiv
    s = re.sub(r"@font-face\{font-family:'Fraunces';font-style:italic;[^}]*\}\n?", '', s)
    s = re.sub(r"@font-face\{font-family:'Fraunces';([^}]*?)font-weight:100 900;", r"@font-face{font-family:'Prata';\1font-weight:400;", s)
    s = re.sub(r"@font-face\{font-family:'(?:Instrument Sans|DM Mono)';([^}]*?)font-weight:(?:400 600|400);", r"@font-face{font-family:'Hanken';\1font-weight:300 700;", s)
    s = s.replace('assets/schrift/fraunces-soft.woff2', 'assets/schrift/prata-latin.woff2').replace('assets/schrift/instrument.woff2', 'assets/schrift/hanken-latin.woff2')
    s = s.replace('assets/schrift/dmmono.woff2', 'assets/schrift/hanken-latin.woff2')
    for alt, neu in (('Fraunces', 'Prata'), ('Instrument Sans', 'Hanken'), ('DM Mono', 'Hanken'), ('ZW Mono', 'ZW Hanken')):
        s = s.replace(f"'{alt}'", f"'{neu}'").replace(f'"{alt}"', f'"{neu}"').replace(f'font-family:{alt},', f'font-family:{neu},')
    s = s.replace('local("Hanken"),', '')
    s = re.sub(r'font-variation-settings:"SOFT"[^;}]*;?', '', s)
    return s


if __name__ == '__main__':
    for d in sys.argv[1:] or DATEIEN:
        p = os.path.join(C, d)
        alt = open(p, encoding='utf-8').read()
        neu = um(alt)
        open(p, 'w', encoding='utf-8').write(neu)
        print(d, 'geändert' if neu != alt else 'gleich')
