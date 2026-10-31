#!/usr/bin/env python3
"""Die Plakatwerkstatt · Walk on the Wild Side Hannover: legt die Marke der Bar für die Werkstatt an (nichts abgetippt, alles aus dem Projekt gelesen).
   python3 bau.py   → haeuser/wildside/ (marke.json, schriften, tapete, bilder, mini, kopf, mail, motive.json, druck.json) + api/_daten/wildside.json
Quellen (nur gelesen):
  Farben      _werkzeuge/oberflaeche/kleid/wildside.css und CHARAKTER.md Abschnitt 4: Nacht, Platte, Creme, Gold als Linie, Rot nur als Punkt (Logo),
              Ultramarin #1A00AA und Plakatrot #D21C0A und Plakatcreme #EBE2D8 nur bei den SESSION-Plakaten (gemessen an den echten Plakaten).
  Schriften   Prata (Titel), Hanken Grotesk 400/500/600 (Lauf, Etiketten, Plakatzeilen der weissen Plakate), Rammetto One (SESSION-Plakate: breite,
              sehr fette Versalien wie auf den echten Plakaten), alle OFL aus dem google/fonts-Repository, feste TrueType-Schnitte (kein Type 3 im PDF).
  Zeichen     die echte Wortmarke (drei Zeilen WALK / ON THE / WILD SIDE), _werkzeuge/oberflaeche/kleid/wildside-marke.svg, Pfade unverändert.
  Fotos       website/assets/bild/<key>-<stufe>.webp mit Beschreibung aus BILDER in website/bilder.py (als Daten gelesen). Die weissen Plakate
              «Eure Nachbarschafts-Mixology-Bar» aus _quelle (verkleinert ins Revier kopiert, zur Laufzeit wird nichts aus _quelle geladen).
  Plakat-Grund  die rot-cremefarbenen Wellen der SESSION-Plakate, hier gerechnet (keine Kopie der Plakate), drei Fassungen.
  Schwarzweiss  Porträts der Bar in Schwarzweiss für das SESSION-Plakat (wie die Gesichter auf den echten Plakaten)."""
import ast, glob, json, math, os, re, shutil
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJ, 'website')
QU = os.path.join(PROJ, '_quelle')
Z = os.path.join(HIER, 'haeuser', 'wildside')
SCHRIFT_Q = os.environ.get('WS_SCHRIFT', os.path.join(HIER, 'haeuser', 'wildside', 'schriften'))

ROLLEN = ['Eigene Fotos', 'Plakate', 'Plakat-Grund', 'Schwarzweiss', 'Drinks & Bar', 'Die Leute', 'Raum & Decke', 'Musik & Feste', 'Die lange Tafel', 'Linden & die Ecke']

# Nicht in den Drucksachen der Bar: Teller und Abende von Culinarium und Dirty Chicken (eigene Häuser, nur Verweis)
RAUS = re.compile(r'^(culinarium-|dirty-|nb-|tf-|karte-dishes|fb-kerzen-koch|fb-koch|ft-koch|ft-gast-am-teller|ft-dessert)')


def gruppe(k):
    if re.match(r'^(p-|uw-pl-|wp-)', k) or k in ('ja-2025', 'karte-love', 'valentin'):
        return 'Plakate'
    if re.match(r'^(momo-|gast-)', k) or k in ('derya', 'fw-derya', 'an-team', 'pf-momo-rudi', 'wf-raum', 'pl-theke', 'freundinnen', 'fw-a46', 'ft-momo-mixt-gast', 'dg-shaker'):
        return 'Die Leute'
    if re.match(r'^(saengerin|konzert|an-party|uw-)', k) or k in ('ja-2024', 'an-dj', 'silvester', 'feste-anstossen', 'fw-a58', 'paloma', 'ft-runde-stoesst-an'):
        return 'Musik & Feste'
    if re.match(r'^(an-empore|tafel-)', k) or k in ('pl-empore', 'fw-tafel', 'an-dinner', 'an-loge', 'fw-a9', 'an-glaeser', 'fb-tafel-gedeckt', 'fb-tafel-im-raum', 'fb-platz-gedeckt', 'ft-glaeser-tafel'):
        return 'Die lange Tafel'
    if re.match(r'^(decke-|alt-|rueckbar|ja-20)', k) or k in ('negroni', 'theke', 'ev-theke', 'flaschen', 'pf-raum', 'voll', 'ft-raum-abend', 'fw-a12', 'fw-h7', 'fw-a1', 'fw-h3',
                                                           'an-campari', 'dg-flaschen', 'dg-behaelter', 'fw-a31', 'fw-h16', 'fb-2020-bar', 'fb-2023-negroni', 'haus-decke-weit'):
        return 'Raum & Decke'
    if re.match(r'^(schild|pf-schild|pl-ecke)', k) or k in ('fenster', 'terrasse', 'tuer-rot', 'fw-h31', 'fw-a49', 'fb-fenster-aussen', 'fb-fenster-nacht', 'fb-blick-durch-die-tuer'):
        return 'Linden & die Ecke'
    return 'Drinks & Bar'


# Kopf der Ansichten (buehne.js / oberflaeche.js): je Ansicht ein Raum der Bar
KOPF = ['schild', 'momo-giesst', 'negroni', 'decke-raum', 'konzert-love', 'an-empore-tafel', 'fenster', 'rueckbar', 'theke', 'glas-coupe', 'voll', 'saengerin-kunde',
        'flaschen', 'schild-ecke', 'tuer-rot', 'decke-bar', 'glas-kerze']
ERSATZ = 'schild'
# Schwarzweiss-Fassungen für das SESSION-Plakat (Gesicht des Abends in Schwarzweiss wie auf den echten Plakaten)
SW = ['momo-giesst', 'momo-lacht', 'derya', 'gast-musa', 'gast-nils', 'gast-enlil', 'gast-cold', 'gast-havn', 'saengerin', 'konzert-love', 'an-dj', 'pl-theke', 'wf-raum', 'freundinnen', 'anstossen']
# Die weissen Plakate der Bar (Kundenmaterial, verkleinert ins Revier)
WEISS = {
    'wp-relaunch': ('facebook/2023-11-22_fb_753889330086143.jpg', 'Plakat Relaunch Party, 01.12.2023, «Eure Nachbarschafts-Mixology-Bar»'),
    'wp-silvester24': ('ig/2024-11-21_walkonthewildside_hannover_DCpKG5ossk4-1.jpg', 'Plakat Silvester Frühshoppen, 31.12.2024'),
    'wp-silvester25': ('ig/2025-11-25_walkonthewildside_hannover_DRfZEXXiHLj-1.jpg', 'Plakat Silvester Frühshoppen, 31.12.2025'),
    'wp-mai25': ('ig/2025-04-13_walkonthewildside_hannover_DIZXgSVMXWs-1.jpg', 'Plakat Tanz in den Mai, 30.04.2025'),
}


def bilder_register():
    src = open(os.path.join(WEB, 'bilder.py'), encoding='utf-8').read()
    env = {}
    for n in ast.parse(src).body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'BILDER':
            exec(compile(ast.Module([n], []), 'bilder.py', 'exec'), {}, env)
    return env['BILDER']


def potrace_pfade(svg):
    """potrace-SVG (transform translate/scale, Befehle m M c l z, relativ) → absolute Pfade (y nach unten)."""
    tr = re.search(r'translate\(([-\d.]+),([-\d.]+)\)\s*scale\(([-\d.]+),([-\d.]+)\)', svg)
    tx, ty, sx, sy = (float(x) for x in tr.groups()) if tr else (0, 0, 1, 1)
    alle = []
    for d in re.findall(r'\sd="([^"]+)"', svg):
        tok = re.findall(r'[MmCcLlZz]|-?\d*\.?\d+', d)
        i, cmd, x, y, sx0, sy0, teile = 0, None, 0.0, 0.0, 0.0, 0.0, []
        while i < len(tok):
            t = tok[i]
            if re.match(r'[A-Za-z]', t):
                cmd = t; i += 1
                if cmd in 'Zz':
                    teile.append(('Z',)); x, y = sx0, sy0
                continue
            n = {'M': 2, 'm': 2, 'L': 2, 'l': 2, 'C': 6, 'c': 6}[cmd]
            v = [float(q) for q in tok[i:i + n]]; i += n
            rel = cmd.islower()
            if cmd in 'Mm':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); sx0, sy0 = x, y
                teile.append(('M', x, y)); cmd = 'l' if rel else 'L'
            elif cmd in 'Ll':
                x, y = (x + v[0], y + v[1]) if rel else (v[0], v[1]); teile.append(('L', x, y))
            else:
                q = [(x + v[k], y + v[k + 1]) if rel else (v[k], v[k + 1]) for k in (0, 2, 4)]
                teile.append(('C', *q[0], *q[1], *q[2])); x, y = q[2]
        neu = []
        for t in teile:
            if t[0] == 'Z':
                neu.append(t); continue
            q = []
            for k in range(1, len(t), 2):
                q += [tx + sx * t[k], ty + sy * t[k + 1]]
            neu.append((t[0], *q))
        alle.append(neu)
    return alle


def zeichen_aus(teile_liste, hoehe=140):
    pts = [(t[k], t[k + 1]) for p in teile_liste for t in p if t[0] != 'Z' for k in range(1, len(t), 2)]
    x0, y0, x1, y1 = min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)
    k = hoehe / (y1 - y0)
    f = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')
    aus = []
    for p in teile_liste:
        s = []
        for t in p:
            if t[0] == 'Z':
                s.append('Z'); continue
            s.append(t[0] + ' '.join(f((t[j] - x0) * k) if j % 2 == 1 else f((t[j] - y0) * k) for j in range(1, len(t))))
        aus.append(''.join(s))
    return aus, [0, 0, round((x1 - x0) * k, 2), hoehe]


def welle(ziel, w, h, periode, phase, schraeg, rot='#D21C0A', creme='#EBE2D8', seed=1):
    """Rot-cremefarbene Wellen wie auf den SESSION-Plakaten: senkrechte Bänder, die in weichen Schleifen laufen, leicht unruhig wie gemalt."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = x / w, y / h
    f = (u * w / periode
         + 1.25 * np.sin(2 * np.pi * (v * .62 + phase) + u * 1.7)
         + .32 * np.sin(2 * np.pi * (v * 1.4 - phase * .7) + u * 3.1 + 1.3)
         + schraeg * v)
    rau = Image.fromarray((rng.random((h // 60 + 2, w // 60 + 2)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    f = f + (np.asarray(rau, np.float32) / 255 - .5) * .035
    band = (f - np.floor(f)) < .54
    r1, c1 = np.array([int(rot[i:i + 2], 16) for i in (1, 3, 5)]), np.array([int(creme[i:i + 2], 16) for i in (1, 3, 5)])
    img = np.where(band[..., None], r1, c1).astype(np.float32)
    korn = rng.normal(0, 5, (h, w, 1)).astype(np.float32)
    img = np.clip(img + korn, 0, 255).astype(np.uint8)
    im = Image.fromarray(img).filter(ImageFilter.GaussianBlur(.8))
    im.save(ziel, 'WEBP', quality=86, method=5)
    return im


def schriften(S):
    from fontTools.ttLib import TTFont
    from fontTools import subset
    os.makedirs(S, exist_ok=True)
    # Rammetto One trägt sehr hohe Zeilenmasse (1,69 em Inhaltsfläche): Zeilen der SESSION-Plakate stehen eng wie auf den echten Plakaten,
    # die Inhaltsfläche überlappte dabei die nächste Zeile (Tor 31.10.2026). Ober- und Unterlänge auf die Glyphen gesetzt (Versalien 1642, Unterlänge −555 von 2048).
    r = os.path.join(S, 'RammettoOne-400.ttf')
    if os.path.exists(r):
        f = TTFont(r)
        if f['hhea'].ascent != 1760:
            f['hhea'].ascent, f['hhea'].descent, f['hhea'].lineGap = 1760, -560, 0
            o = f['OS/2']; o.sTypoAscender, o.sTypoDescender, o.sTypoLineGap, o.usWinAscent, o.usWinDescent = 1760, -560, 0, 1760, 560
            f.save(r)
    U = list(range(0x20, 0x7f)) + list(range(0xa0, 0x250)) + list(range(0x2000, 0x2070)) + [0x20ac, 0x2122, 0x2190, 0x2192, 0x2212, 0xfb01, 0xfb02]
    for f in sorted(glob.glob(os.path.join(S, '*.ttf'))):
        o = subset.Options(); o.flavor = 'woff2'; o.layout_features = ['*']; o.name_IDs = ['*']; o.notdef_outline = True; o.legacy_kern = True
        ft = TTFont(f); u = subset.Subsetter(o); u.populate(unicodes=U); u.subset(ft); ft.flavor = 'woff2'; ft.save(f[:-4] + '.woff2')


def tapete(ziel, farbe, deck, groesse=448):
    """Feines Raster als Tapete (Haarlinie in Gold oder Tinte), Rapport 24 mm, WebP mit Alpha."""
    im = Image.new('RGBA', (groesse, groesse), (0, 0, 0, 0))
    px = im.load(); r, g, b = (int(farbe[i:i + 2], 16) for i in (1, 3, 5)); a = int(255 * deck)
    for i in range(groesse):
        for j in (0, groesse // 2):
            px[i, j] = (r, g, b, a); px[j, i] = (r, g, b, a)
    im.save(ziel, 'WEBP', lossless=True)


DRUCK = ['konzert-scharf', 'momo-giesst', 'decke-raum', 'an-empore-tafel', 'silvester']   # Druckfassungen bis 2400 px für A3 (druck.json)


def druckfassungen():
    """Grössere Fassungen nur für PDF und Druckprüfung (satz.js liest druck.json): die Wellen in 2400 × 3200, einige Fotos in der grössten Stufe der Website,
    Schwarzweiss-Porträts aus der grössten Stufe."""
    D = os.path.join(Z, 'druck'); os.makedirs(D, exist_ok=True)
    for f in os.listdir(D):
        os.remove(os.path.join(D, f))
    aus = {}
    for n, (per, ph, sch, seed) in enumerate(WELLEN, 1):
        p = os.path.join(D, 'welle-%d.jpg' % n)
        im = welle(p + '.webp', 2400, 3200, per * 1.6, ph, sch, seed=seed); os.remove(p + '.webp')
        im.save(p, 'JPEG', quality=88); aus['welle-%d' % n] = list(im.size)
    gross = lambda k: sorted(glob.glob(os.path.join(WEB, 'assets', 'bild', k + '-*.webp')), key=lambda q: int(re.search(r'-(\d+)\.webp$', q).group(1)))
    for k in DRUCK + ['sw-' + x for x in SW]:
        q = gross(k[3:] if k.startswith('sw-') else k)
        if not q:
            continue
        im = ImageOps.exif_transpose(Image.open(q[-1]))
        if max(im.size) <= 1600:
            continue
        if k.startswith('sw-'):
            g = ImageEnhance.Contrast(ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)).enhance(1.18); im = g
        im = im.convert('RGB'); im.save(os.path.join(D, k + '.jpg'), 'JPEG', quality=88); aus[k] = list(im.size)
    json.dump(aus, open(os.path.join(Z, 'druck.json'), 'w'))
    return aus


WELLEN = [(250, .1, .5, 3), (220, .55, -.4, 7), (280, .3, 1.0, 11)]


def main():
    for u in ('schriften', 'bilder', 'mini', 'kopf', 'mail'):
        os.makedirs(os.path.join(Z, u), exist_ok=True)
    F = dict(navy='#1c1513', nacht='#130e0d', blau='#1a00aa', tinte='#1c1513', papier='#f2e9dc', creme='#ebe2d8', weiss='#fffbf5', gold='#d8b264',
             taupe='#7a5c24', messing='#d8b264', tanne='#1c1513', kander='#f0323f', laden='#261e1a', rot='#d21c0a', logo='#f0323f', leise='#5e524a')
    N = dict(navy='Nacht', nacht='Nacht tief', blau='Ultramarin', tinte='Tinte', papier='Creme', creme='Plakatcreme', weiss='Weiss', gold='Gold',
             taupe='Gold tief', messing='Gold', tanne='Tinte', kander='Rot', laden='Platte', rot='Plakatrot', logo='Rot der Wortmarke', leise='Tinte leise')

    svg = open(os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid', 'wildside-marke.svg'), encoding='utf-8').read()
    pfade, vb = zeichen_aus(potrace_pfade(svg))

    S = os.path.join(Z, 'schriften')
    schriften(S)
    SCHRIFTEN = {
        'titel': ('Prata', 'Prata-400.ttf', 'Titel, Prata wie die Website: eine Stärke, nie fett, nie kursiv'),
        'kapitale': ('Hanken Grotesk 600', 'Hanken-600.ttf', 'Zeilen der weissen Plakate in Versalien («SILVESTER FRÜHSHOPPEN», «EURE NACHBARSCHAFTS-MIXOLOGY-BAR»)'),
        'text': ('Hanken Grotesk', 'Hanken-400.ttf', 'Lesetext wie die Website'),
        'kursiv': ('Hanken Grotesk 500', 'Hanken-500.ttf', 'Betont (die Bar setzt nie kursiv, Betonung über Stärke)'),
        'mono': ('Hanken Grotesk 500', 'Hanken-500.ttf', 'Etiketten, Zahlen, Daten und Zeiten: Hanken 500 gesperrt, Ziffern gleich breit'),
        'plakat': ('Rammetto One', 'RammettoOne-400.ttf', 'SESSION-Plakate: «SESSION», «SIP & SOUNDS», Datum «17|10», breite fette Versalien wie auf den echten Plakaten (OFL)'),
        'plakatfett': ('Rammetto One', 'RammettoOne-400.ttf', 'Grosse Zahlen und Namen auf den SESSION-Plakaten'),
        'kopf': ('Rammetto One', 'RammettoOne-400.ttf', 'Kopfzeile der SESSION-Plakate'),
    }

    tapete(os.path.join(Z, 'tapete-dunkel.webp'), F['gold'], .10)
    tapete(os.path.join(Z, 'tapete-hell.webp'), F['tinte'], .06)
    tapete(os.path.join(Z, 'tapete-ui-dunkel.webp'), F['gold'], .06)
    tapete(os.path.join(Z, 'tapete-ui-hell.webp'), F['tinte'], .04)
    t = Image.open(os.path.join(Z, 'tapete-dunkel.webp')).convert('RGBA'); g = Image.new('RGBA', t.size, F['navy']); g.alpha_composite(t)
    g.convert('RGB').save(os.path.join(Z, 'mail', '_tapete.jpg'), 'JPEG', quality=86)

    B = bilder_register()
    bilder = []

    def ablegen(key, im, alt, gr, quelle=None):
        im = ImageOps.exif_transpose(im).convert('RGB')
        if max(im.size) > 1600:
            im.thumbnail((1600, 1600), Image.LANCZOS)
        w, h = im.size
        im.save(os.path.join(Z, 'bilder', key + '.webp'), 'WEBP', quality=86, method=5)
        k = im.copy(); k.thumbnail((520, 520), Image.LANCZOS); k.save(os.path.join(Z, 'mini', key + '.webp'), 'WEBP', quality=74, method=5)
        k = im.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'mail', key + '.jpg'), 'JPEG', quality=76, optimize=True, progressive=True)
        if key in KOPF:
            k = im.copy(); k.thumbnail((1200, 1200), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '.webp'), 'WEBP', quality=78, method=5)
            k = im.copy(); k.thumbnail((800, 800), Image.LANCZOS); k.save(os.path.join(Z, 'kopf', key + '-800.webp'), 'WEBP', quality=76, method=5)
        b = dict(key=key, alt=alt, w=w, h=h, gruppe=gr)
        if quelle:
            b['quelle'] = quelle
        bilder.append(b)
        return im

    def website_bild(key):
        st = sorted(glob.glob(os.path.join(WEB, 'assets', 'bild', key + '-*.webp')), key=lambda p: int(re.search(r'-(\d+)\.webp$', p).group(1)))
        if not st:
            return None
        gut = [p for p in st if int(re.search(r'-(\d+)\.webp$', p).group(1)) <= 1600]
        return Image.open((gut or st)[-1])

    for key, (q, alt) in B.items():
        if RAUS.match(key):
            continue
        im = website_bild(key)
        if im is None:
            continue
        ablegen(key, im, alt, gruppe(key), 'website/assets/bild')
    for key, (q, alt) in WEISS.items():
        p = os.path.join(QU, q)
        if os.path.exists(p):
            ablegen(key, Image.open(p), alt, 'Plakate', '_quelle/' + q.split('/')[0])
        elif os.path.exists(os.path.join(Z, 'bilder', key + '.webp')):   # ohne _quelle (Actions): die Kopie im Revier bleibt
            im = Image.open(os.path.join(Z, 'bilder', key + '.webp')); bilder.append(dict(key=key, alt=alt, w=im.width, h=im.height, gruppe='Plakate'))

    # Plakat-Grund: drei Wellen (hochkant gerechnet, alle Formate schneiden daraus)
    motive = []
    for n, (per, ph, sch, seed) in enumerate(WELLEN, 1):
        k = 'welle-%d' % n
        p = os.path.join(Z, 'bilder', k + '.webp')
        im = welle(p, 1500, 2000, per, ph, sch, seed=seed)
        ablegen(k, im, 'Rot-cremefarbene Wellen der SESSION-Plakate, Fassung %d' % n, 'Plakat-Grund', 'gerechnet (bau.py welle)')
        motive.append(dict(key=k, titel='Wellen %d' % n, quelle='welle', schrift=False, schlagworte=dict(thema='SESSION', farbe='Rot und Creme'),
                           akzent=F['blau'], kopf_frei=True, kopf_farbe='#1a00aa', rueck_farbe=F['blau'], ganz=None, kopf_box=None, ganz_kopf_box=None))
    for k in SW:
        im = website_bild(k)
        if im is None:
            continue
        g = ImageOps.grayscale(ImageOps.exif_transpose(im))
        g = ImageOps.autocontrast(g, cutoff=1)
        g = ImageEnhance.Contrast(g).enhance(1.18)
        ablegen('sw-' + k, g.convert('RGB'), B[k][1].rstrip('.') + ', schwarzweiss', 'Schwarzweiss', 'website/assets/bild, schwarzweiss')

    da = {b['key'] for b in bilder}
    for u in ('bilder', 'mini'):
        for f in os.listdir(os.path.join(Z, u)):
            if f.endswith('.webp') and f[:-5] not in da:
                os.remove(os.path.join(Z, u, f))
    for f in os.listdir(os.path.join(Z, 'mail')):
        if f.endswith('.jpg') and not f.startswith('_') and f[:-4] not in da:
            os.remove(os.path.join(Z, 'mail', f))
    bilder.sort(key=lambda b: (ROLLEN.index(b['gruppe']), b['key']))
    json.dump(motive, open(os.path.join(Z, 'motive.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    druckfassungen()

    marke = dict(
        key='wildside', name='Wild Side', voll='Walk on the Wild Side Hannover', ort='Hannover-Linden', artikel='das',
        zeile='Eure Nachbarschafts-Mixology-Bar',
        satz='Eine Nachbarschafts-Mixology-Bar in Linden-Mitte. Die Drinks entwirft Momo, die Karte wechselt immer wieder, und an der Bar sagst du, was du magst.',
        adr='Haasemannstraße 13 · 30449 Hannover-Linden', tel='+49 163 3909578', mail='', web='@walkonthewildside_hannover',
        farben=F, farbnamen=N,
        toene=dict(
            dunkel=dict(grund='navy', tapete='dunkel', titel='weiss', text='papier', mono='gold', linie='gold', zeichen='logo', schild='papier', schild_text='navy'),
            hell=dict(grund='weiss', tapete=None, titel='tanne', text='tinte', mono='taupe', linie='gold', zeichen='logo', schild='navy', schild_text='weiss'),
            creme=dict(grund='papier', tapete='hell', titel='tanne', text='tinte', mono='taupe', linie='gold', zeichen='logo', schild='navy', schild_text='weiss'),
            session=dict(grund='creme', tapete=None, titel='blau', text='blau', mono='blau', linie='rot', zeichen='logo', schild='blau', schild_text='creme'),
        ),
        schriften={k: dict(familie=f, datei=d, wofuer=w) for k, (f, d, w) in SCHRIFTEN.items()},
        tapete=dict(dunkel='tapete-dunkel.webp', hell='tapete-hell.webp', rapport_mm=24),
        zeichen=dict(vb=vb, pfade=pfade, verh=vb[3] / vb[2], name='Die Wortmarke WALK / ON THE / WILD SIDE (das echte Logo, nachgezogen)'),
        zeichen2=dict(vb=vb, pfade=pfade, verh=vb[3] / vb[2], name='Die Wortmarke WALK / ON THE / WILD SIDE (das echte Logo, nachgezogen)',
                      farben=dict(grund=F['weiss'], zeichen=F['logo'], text=F['tinte'], hell=F['logo'])),
        abende=[],
        betriebe=[('Walk on the Wild Side', 'Nachbarschafts-Mixology-Bar in Linden-Mitte, Do 19–1, Fr/Sa 19–2 Uhr'),
                  ('Culinarium', 'Food-Pairing-Abende an der langen Tafel im selben Haus, nur als Verweis'),
                  ('Dirty Chicken', 'Rudis Pop-up aus der Familie der Bar, nur als Verweis')],
        regeln=['Anrede «du» (an Gruppen «ihr»), herzlich, knapp, ein bisschen Nacht, wie die Bar schreibt. Nie Werbesprache, nie Ausrufezeichen im Titel.',
                'Die Karte wechselt, die Drinks entwirft Momo, an der Bar sagst du, was du magst. Nie «keine Karte» oder «einmal im Jahr eine Karte» schreiben.',
                'DJ-Abende heissen auf den Plakaten SESSION · SIP & SOUNDS: rot-cremefarbene Wellen, Ultramarin-Schrift, das Gesicht des Abends in Schwarzweiss, '
                'Datum in der Form «17|10», Uhrzeit wie «9 TO 1 AM», unten die Wortmarke in Rot und «HAASEMANNSTR. 13 · 30449 HANNOVER».',
                'Feste und Ankündigungen stehen auf den weissen Plakaten: Bild oben, darunter die rote Wortmarke, «EURE NACHBARSCHAFTS-MIXOLOGY-BAR», Titel in Versalien, '
                'Datum in der Form «31 | 12 | 25».',
                'Titel in Prata, nie fett, nie kursiv. Lauf in Hanken Grotesk. Gold nur als Linie, Rot nur für die Wortmarke, Ultramarin nur bei SESSION.',
                'Preise nur, wo die Bar sie nennt (Preisliste der Bar, Pauschalen, Valentinskarte); sonst keine.',
                'Culinarium und Dirty Chicken sind eigene Häuser unter demselben Dach und kommen nur als Verweis vor. Keine E-Mail-Adresse erfinden: Kontakt über Telefon und Instagram.'],
        bilder=bilder, raus=[], ersatz=ERSATZ, doppelt={},
    )
    json.dump(marke, open(os.path.join(Z, 'marke.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    api = dict(marke)
    api['bilder'] = ['%s | %s | %s' % (b['key'], 'quer' if b['w'] > b['h'] * 1.1 else 'hoch' if b['h'] > b['w'] * 1.1 else 'quadrat', b['alt']) for b in bilder]
    for k in ('zeichen', 'zeichen2'):
        api.pop(k, None)
    os.makedirs(os.path.join(HIER, 'api', '_daten'), exist_ok=True)
    json.dump(api, open(os.path.join(HIER, 'api', '_daten', 'wildside.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Marke:', len(bilder), 'Fotos,', len(motive), 'Wellen,', len([b for b in bilder if b['gruppe'] == 'Schwarzweiss']), 'Schwarzweiss')


if __name__ == '__main__':
    main()
