"""Handgezeichnete Karte der Ecke für besuch.html, Abschnitt «Wo» (Wahl Robert 31.10.2026: Fassung 6 mit Karte und Strassenschild).
Strassen aus OpenStreetMap (_quelle/osm/ecke-2026-10-31.osm), nicht ausgedacht. Die Linien werden leicht zittrig doppelt gezogen,
damit sie wie mit dem Stift gezeichnet wirken. Ergebnis: ein SVG-Text, den unter.py in die Seite setzt. Die Lage des Schilds gibt KARTE_ECKE."""
import os, random, math
import xml.etree.ElementTree as T

HIER = os.path.dirname(os.path.abspath(__file__))
OSM = os.path.join(HIER, '..', '_quelle', 'osm', 'ecke-2026-10-31.osm')
LO0, LO1, LA0, LA1 = 9.71000, 9.71600, 52.36930, 52.37190       # Ausschnitt
VW, VH = 600, 400
ECKE = (52.370426, 9.7134249)          # Rampenstraße trifft Haasemannstraße (OSM), Haus 13 liegt an dieser Ecke
HALT = (52.3714413, 9.7132174)         # Stadtbahn Am Küchengarten (OSM tram_stop)
ELFA = (52.370543, 9.7132596)          # Restaurant 11A (OSM)

HAUPT = {'Fössestraße'}
NAMEN = {'Haasemannstraße', 'Rampenstraße', 'Fössestraße', 'Limmerstraße', 'Küchengartenstraße', 'Blumenauer Straße', 'Elisenstraße',
         'Pavillonstraße', 'Selmastraße', 'Mathildenstraße', 'Gartenallee', 'Stephanusstraße', 'Spinnereistraße'}


def xy(p):
    return ((p[1] - LO0) / (LO1 - LO0) * VW, (LA1 - p[0]) / (LA1 - LA0) * VH)


def lesen():
    r = T.parse(OSM).getroot()
    N = {n.get('id'): (float(n.get('lat')), float(n.get('lon'))) for n in r.findall('node')}
    wege = []
    for w in r.findall('way'):
        t = {x.get('k'): x.get('v') for x in w.findall('tag')}
        pts = [N[n.get('ref')] for n in w.findall('nd')]
        if t.get('name') in NAMEN and 'highway' in t:
            wege.append((t['name'], pts))
        elif t.get('railway') == 'light_rail':
            wege.append(('bahn', pts))
    return wege


def zittrig(pts, rnd, amp=1.1):
    """Punkte verdichten und leicht verschieben, dann als weiche Kurve."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0); n = max(1, int(d / 14))
        for i in range(n):
            t = i / n; out.append((x0 + (x1 - x0) * t + rnd.uniform(-amp, amp), y0 + (y1 - y0) * t + rnd.uniform(-amp, amp)))
    out.append((pts[-1][0] + rnd.uniform(-amp, amp), pts[-1][1] + rnd.uniform(-amp, amp)))
    d = 'M%.1f %.1f' % out[0]
    for a, b in zip(out[1:], out[2:]):
        d += ' Q%.1f %.1f %.1f %.1f' % (a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    d += ' L%.1f %.1f' % out[-1]
    return d


def beschriftung(text, p, winkel, cls, anker='middle'):
    x, y = xy(p)
    return '<text class="%s" x="%.1f" y="%.1f" text-anchor="%s" transform="rotate(%.1f %.1f %.1f)">%s</text>' % (cls, x, y, anker, winkel, x, y, text)


def entlang(name, wege, t, abstand, text, cls):
    """Name an der Stelle t (0..1) der Strasse, parallel zur Linie, um «abstand» px daneben."""
    pts = [xy(q) for n, w in wege if n == name for q in w]
    pts = sorted(set(pts), key=lambda p: p[0])
    i = max(0, min(len(pts) - 2, int(t * (len(pts) - 1))))
    (x0, y0), (x1, y1) = pts[i], pts[i + 1]
    w = math.degrees(math.atan2(y1 - y0, x1 - x0))
    if w > 90: w -= 180
    if w < -90: w += 180
    nx, ny = -math.sin(math.radians(w)), math.cos(math.radians(w))
    x, y = (x0 + x1) / 2 + nx * abstand, (y0 + y1) / 2 + ny * abstand
    return '<text class="%s" x="%.1f" y="%.1f" text-anchor="middle" transform="rotate(%.1f %.1f %.1f)">%s</text>' % (cls, x, y, w, x, y, text)


def svg():
    rnd = random.Random(13)
    teile = []
    wege = lesen()
    for name, pts in wege:
        p = [xy(q) for q in pts]
        if name == 'bahn':
            teile.append('<path class="kk-bahn" d="%s"/>' % zittrig(p, rnd, .6))
            continue
        cls = 'kk-haupt' if name in HAUPT else ('kk-wir' if name in ('Haasemannstraße', 'Rampenstraße') else 'kk-str')
        teile.append('<path class="%s" d="%s"/>' % (cls, zittrig(p, rnd)))
        teile.append('<path class="%s kk-zwei" d="%s"/>' % (cls, zittrig(p, rnd, 1.6)))
    hx, hy = xy(HALT); ex, ey = xy(ECKE); ax, ay = xy(ELFA)
    # Haltestelle: kleines Schild mit H, Beschriftung darunter
    teile.append('<g class="kk-halt"><circle cx="%.1f" cy="%.1f" r="9"/><text x="%.1f" y="%.1f" text-anchor="middle">H</text></g>' % (hx, hy, hx, hy + 4))
    teile.append('<text class="kk-ort" x="%.1f" y="%.1f" text-anchor="end">Am Küchengarten</text><text class="kk-klein" x="%.1f" y="%.1f" text-anchor="end">Stadtbahn 9 und 17</text>' % (hx - 14, hy + 22, hx - 14, hy + 38))
    # 11A gegenüber
    teile.append('<circle class="kk-punkt" cx="%.1f" cy="%.1f" r="3.4"/><text class="kk-klein kk-elf" x="%.1f" y="%.1f" text-anchor="end">11A</text>' % (ax, ay, ax - 9, ay - 2))
    # Strassennamen neben den Linien (Lage aus den OSM-Punkten im Ausschnitt abgelesen)
    def name(t, x, y, w, cls='kk-name'):
        return '<text class="%s" x="%.1f" y="%.1f" text-anchor="middle" transform="rotate(%.1f %.1f %.1f)">%s</text>' % (cls, x, y, w, x, y, t)
    teile.append(name('Rampenstraße', 150, 289, -12.4))
    teile.append(name('Haasemannstraße', 311, 333, -59.3))
    teile.append(name('Fössestraße', 222, 183, -12.4, 'kk-name kk-hell'))
    # Die Bar: roter Kringel, zweimal herum, nicht ganz geschlossen
    pkt = []
    for i in range(0, 46):
        a = -2.2 + i / 45 * (2 * math.pi + 1.0)
        rr = 25 + 1.8 * math.sin(i * .7) + i * .06
        pkt.append((ex + 13 + rr * math.cos(a) * 1.12, ey + 13 + rr * math.sin(a)))
    teile.append('<path class="kk-kringel" d="%s"/>' % zittrig(pkt, random.Random(7), .4))
    return ('<svg class="kk" viewBox="0 0 %d %d" role="img" aria-label="Handgezeichnete Karte: Die Bar an der Ecke Haasemannstraße und Rampenstraße, '
            'gegenüber vom Restaurant 11A, oben die Stadtbahn-Haltestelle Am Küchengarten">%s</svg>') % (VW, VH, ''.join(teile))


def ecke_prozent():
    x, y = xy(ECKE)
    return x / VW * 100, y / VH * 100


if __name__ == '__main__':
    open(os.path.join(HIER, '_varianten', 'wo-15', 'karte-test.svg'), 'w').write(svg())
    print(ecke_prozent())
