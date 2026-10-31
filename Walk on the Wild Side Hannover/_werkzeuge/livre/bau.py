#!/usr/bin/env python3
"""Das Markenbuch (Le Livre, Marke) · Walk on the Wild Side Hannover: baut die Marke der Bar zum Arbeiten aus der Website und dem Charakterblatt.
Kopie des Markenbuchs von Culinarium Hannover (28.10.2026, von Robert abgenommen), umgekleidet und mit den Hauswerten der Bar (Nachtbau 31.10.2026).
Die Website wird nie angefasst und nie importiert (Falle 9): gelesen werden BILDER in website/bilder.py (register.py, per ast), die Merkzettel
website/assets/bild/<schlüssel>.json, website/assets/wild.css, assets/schrift/, assets/bild/haus-tapete.svg und _quelle/logo/ (nur beim Bau, nie zur Laufzeit).
Geschrieben wird nur in diesen Ordner.

   python3 _werkzeuge/livre/bau.py   → livre.json, dateien/, original/, _quellen.json (nur lokal), listen/, beispiel/, index.html

Farben = die Werte der Website heute (wild.css); jede wird dort gesucht, der Bau bricht ab, wenn eine fehlt (ausser den Plakatfarben, die am Plakat
gemessen sind, CHARAKTER.md 3). Herkunft je Foto: haus (Kanäle der Bar: Instagram, Facebook, erste Website, Angebotsmappe, von der Bar geschickt),
fremd (Google-Eintrag, Gäste und Partner auf Instagram, Presse, Portale, Rudis Fotos der Culinarium-Abende in der Bar)."""
import base64, hashlib, html, io, json, os, re, shutil, struct, subprocess, sys, time, zipfile
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFile, ImageFont

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))              # …/Walk on the Wild Side Hannover
ROOT = os.path.join(PROJEKT, 'website')                        # die Website, nur gelesen; ausgeliefert unter / (server.py)
PROJEKTE = os.path.dirname(PROJEKT)
QUELLE = os.path.join(PROJEKT, '_quelle')
BILDER = os.path.join(ROOT, 'assets', 'bild')
CSS = os.path.join(ROOT, 'assets', 'wild.css')
FONTS = os.path.join(ROOT, 'assets', 'schrift')
LOGO = os.path.join(QUELLE, 'logo')
DAT = os.path.join(HIER, 'dateien')
ORIG = os.path.join(HIER, 'original')
e = html.escape
HAUS = 'Walk on the Wild Side Hannover'
STAND = time.strftime('%d.%m.%Y')
SCHLUESSEL = 'wildside-hannover'
KLEID = os.path.join(PROJEKT, '_werkzeuge', 'oberflaeche', 'kleid', 'wildside.js')
PLATZHALTER = {'zentrale': 'Der Tresen', 'website': 'Das Schaufenster', 'karten': 'Die Pairing-Karte', 'gaeste': 'Das Gästebuch', 'marke': 'Das Markenbuch', 'besuche': 'Die Besucherliste', 'druck': 'Die Plakatwerkstatt'}   # nur falls das Kleid fehlt
sys.path.insert(0, HIER)
import register  # noqa: E402


def namen_aus_kleid():
    """Sichtbare Namen der Werkzeuge: eine Stelle für alle, WO_HAUS.namen im gemeinsamen Kleid."""
    if not os.path.exists(KLEID):
        return dict(PLATZHALTER)
    m = re.search(r'namen:\s*\{([^}]*)\}', open(KLEID, encoding='utf-8').read())
    if not m:
        return dict(PLATZHALTER)
    return dict(PLATZHALTER, **dict(re.findall(r"(\w+):\s*['\"]([^'\"]+)['\"]", m.group(1))))


NAMEN = namen_aus_kleid()
NAME = NAMEN['marke']


def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- Farben: so wie wild.css sie trägt (CHARAKTER.md 4)
# (Schlüssel, Name, Wert, Rolle, Gruppe, Herkunft)
FARBEN = [
    ('nacht', 'Nacht', '#130E0D', 'Grund der dunklen Flächen: die Bar nach 19 Uhr', 'nacht', 'css'),
    ('platte', 'Platte', '#1C1513', 'Platten und Karten auf Nacht, wie das Eckschild', 'nacht', 'css'),
    ('platte-hell', 'Platte hell', '#261E1A', 'gehobene Platte, Kachel auf Platte', 'nacht', 'css'),
    ('holz', 'Holz', '#33281F', 'tiefste Kante, Fugen zwischen Fotos', 'nacht', 'css'),
    ('text', 'Schrift auf Nacht', '#EDE4D8', 'Lesetext auf dunklem Grund, nie reines Weiss', 'nacht', 'css'),
    ('creme', 'Creme', '#F2E9DC', 'die weissen Plakate der Bar: Grund der hellen Kapitel', 'creme', 'css'),
    ('creme-2', 'Creme 2', '#E7DCCB', 'Fläche auf Creme, Kachel im hellen Kapitel', 'creme', 'css'),
    ('creme-3', 'Creme 3', '#D9CBB6', 'Linie und Rand auf Creme', 'creme', 'css'),
    ('dunkel', 'Schrift auf Creme', '#1B1512', 'Lesetext und Titel auf Creme, nie reines Schwarz', 'creme', 'css'),
    ('gold', 'Gold', '#D8B264', 'der Rahmen des Eckschilds: nur Haarlinie, Etikett, Knauf', 'gold', 'css'),
    ('gold-tief', 'Gold tief', '#A07F3A', 'Etikett auf Creme, wo Gold zu hell steht', 'gold', 'css'),
    ('rot', 'Rot', '#F0323F', 'die Farbe der Wortmarke: nur als Punkt, Hauptknopf und Logo', 'gold', 'css'),
    ('ultramarin', 'Ultramarin', '#1A00AA', 'die Schrift der SESSION-Plakate, nur bei den DJ-Abenden', 'session', 'css'),
    ('plakatrot', 'Plakatrot', '#D21C0A', 'die Wellen der SESSION-Plakate, nur bei den DJ-Abenden', 'session', 'css'),
    ('plakatcreme', 'Plakatcreme', '#EBE2D8', 'der Grund der SESSION-Plakate', 'session', 'plakat'),
]
GRUPPEN = [('nacht', 'Nacht und Platte', 'Die dunklen Flächen, so wie die Bar nach 19 Uhr unter der Decke steht. Platten liegen wie das Eckschild auf der Nacht, geschrieben wird in einem warmen Hell.'),
           ('creme', 'Creme', 'Das Creme der weissen Plakate der Bar. Es trägt die hellen Kapitel; darauf wird in einem warmen Dunkel gelesen.'),
           ('gold', 'Gold und Rot', 'Gold ist der Rahmen des Eckschilds an der Hausecke: Haarlinie, Etikett, Knauf. Rot ist die Wortmarke, und nur als Punkt.'),
           ('session', 'Die DJ-Abende', 'Die Farben der SESSION-Plakate, gemessen an den Plakaten: rot-cremefarbene Wellen und Ultramarin für die Schrift. Sie gehören nur zu den DJ-Abenden.')]
# je Gruppe ein eigenes Foto (Fehlerbuch 10a, 20.10.2026: ein Foto je Gruppe, nie wiederholt; Farbfeld ganz). Wege von der Seite des Werkzeugs aus.
GRUPPE_BILD = {'nacht': ('schild', 'Das Eckschild an der Hausecke bei Nacht. Daraus kommen Nacht, Platte und der Goldrahmen.'),
               'creme': ('listen/farbe-creme.webp', 'So steht Creme mit dunkler Schrift auf der Website.'),
               'gold': ('negroni', 'Der NEGRONI-Schriftzug aus Glühbirnen über der Vitrine: das Licht, aus dem Gold und Rot kommen.'),
               'session': ('p-1710', 'Das SESSION-Plakat vom 17. Oktober 2026: Wellen in Plakatrot und Creme, Schrift in Ultramarin.')}


def css_text():
    return open(CSS, encoding='utf-8').read()


def farben_liste():
    s = css_text().upper(); aus = []
    for k, n, h, r, g, w in FARBEN:
        if w == 'css' and h.upper() not in s:
            raise SystemExit(f'Farbe {n} {h} steht nicht in wild.css, erst klären')
        woher = 'Wert der Website (wild.css)' if w == 'css' else 'gemessen an den SESSION-Plakaten der Bar'
        aus.append((k, n, h, r, g, woher))
    return aus


# ---------------------------------------------------------------- Bildarchiv
REG = register.lesen()
BEREICHE = ['raum', 'drinks', 'leute', 'musik', 'tafel', 'plakate', 'unterwegs', 'jahre', 'nachbarn']
MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']


def bereich(k, alt):
    if k.startswith(('p-', 'uw-pl-', 'karte-')) or k in ('ja-2025', 'valentin'):
        return 'plakate'
    if k.startswith('uw-'):
        return 'unterwegs'
    if k.startswith(('culinarium-', 'dirty-', 'nb-')) or k == 'pf-momo-rudi':
        return 'nachbarn'
    if k.startswith(('ja-', 'alt-')) or k in ('decke-2017', 'fb-2020-bar', 'fb-2023-negroni', 'fw-a12'):
        return 'jahre'
    if k.startswith(('an-empore', 'tf-', 'tafel-')) or k in ('an-dinner', 'an-loge', 'fw-tafel', 'fw-a9', 'pl-empore'):
        return 'tafel'
    if k.startswith(('saengerin', 'konzert')) or k in ('an-dj', 'an-party', 'an-party-sw', 'silvester', 'fw-a58'):
        return 'musik'
    if k.startswith(('momo-', 'gast-', 'ft-')) or k in ('derya', 'fw-derya', 'freundinnen', 'anstossen', 'an-team', 'voll', 'feste-anstossen', 'terrasse', 'pl-theke'):
        return 'leute'
    if k.startswith(('glas-', 'fe-', 'wf-', 'dg-')) or k in ('schaum', 'paloma', 'an-sour', 'an-sours', 'an-negroni', 'an-glaeser', 'fw-highballs', 'fw-sour'):
        return 'drinks'
    if k.startswith('fw-'):
        a = alt.lower()
        if re.search(r'gast|gäste|zwei an|bartender|sonne|sommerabend|im raum|in der bar|am tisch|am abend|tresen|bar wird', a):
            return 'leute'
        if re.search(r'flaschen|regal|rückbar', a):
            return 'raum'
        return 'drinks'
    return 'raum'


def datum(s):
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', s or '')
    return f'{int(m.group(3))}. {MONATE[int(m.group(2)) - 1]} {m.group(1)}' if m else ''


def hk(rel):
    """Eintrag aus der herkunft.json im Ordner der Quelle (oder darüber)."""
    p = os.path.join(PROJEKT, rel); d = os.path.dirname(p)
    while d.startswith(QUELLE):
        f = os.path.join(d, 'herkunft.json')
        if os.path.exists(f):
            try:
                j = json.load(open(f, encoding='utf-8'))
            except ValueError:
                j = {}
            for key in (os.path.relpath(p, d), os.path.basename(p)):
                if isinstance(j, dict) and isinstance(j.get(key), dict):
                    return j[key]
        d = os.path.dirname(d)
    return {}


def beitrag(rel):
    """(Datum, Konto, Adresse) eines Instagram-Bildes aus dem Dateinamen JJJJ-MM-TT_konto_KENNUNG-n.jpg."""
    b = os.path.basename(rel)
    m = re.match(r'(\d{4}-\d{2}-\d{2})_([A-Za-z0-9_.]+?)_([A-Za-z0-9_-]{9,12})-\d+(?:-[a-z-]+)?\.\w+$', b)
    return (datum(m.group(1)), m.group(2), f'https://www.instagram.com/p/{m.group(3)}/') if m else (datum(b[:10]), '', '')


PORTALE = {'stadtwohnungenlinden': 'Stadtwohnungen Linden', 'enprimeurclub': 'En Primeur Club'}


def herkunft(k, q):
    """(art, Quelle als Satz, Adresse) für die Quelle q (relativ zu _quelle/, wie in website/bilder.py)."""
    rel = os.path.normpath(os.path.join('_quelle', q))
    h = hk(rel)
    if q.startswith('ig/'):
        d, _, u = beitrag(q)
        return 'haus', f'Instagram der Bar (@walkonthewildside_hannover), Beitrag vom {d}', h.get('adresse') or u
    if q.startswith('facebook/'):
        return 'haus', f'Facebook der Bar, Beitrag vom {datum(os.path.basename(q))}', h.get('adresse', '') if str(h.get('adresse', '')).startswith('http') else ''
    if q.startswith('web-archiv/'):
        return 'haus', 'Foto der ersten Website der Bar (wildside-hannover.de, aus dem Webarchiv)', ''
    if q.startswith('angebote-pdf/'):
        return 'haus', 'Aus der Angebotsmappe der Bar «Wild Side Angebote» (Oktober 2026)', ''
    if q.startswith('kunde-2026-10-30/'):
        return 'haus', 'Von der Bar geschickt (30. Oktober 2026)', ''
    if q.startswith('ki/'):
        return 'haus', 'Facebook der Bar, Beitrag vom 4. März 2024', ''
    if q.startswith('google-maps/'):
        return 'fremd', 'Google-Eintrag der Bar, Foto eines Gastes oder des Hauses; die Rechte liegen beim Fotografen', ''
    if q.startswith(('ig-dritte/', 'neu-2026-10/')):
        d, konto, u = beitrag(q)
        return 'fremd', f'Instagram von @{konto}, Beitrag vom {d}; die Rechte liegen beim Fotografen', h.get('adresse') or u
    if q.startswith('presse/'):
        if '_np_' in q:
            return 'fremd', 'Neue Presse, 11. Januar 2024, Foto: Ilona Hottmann', ''
        if 'vimeo' in q:
            return 'fremd', 'Standbild aus einem Film von Niemand Gin über die Bar (Vimeo, September 2018)', ''
        return 'fremd', f'Presse, {datum(os.path.basename(q))}', ''
    if q.startswith('portale/'):
        n = next((v for x, v in PORTALE.items() if x in q), 'einem Portal')
        return 'fremd', f'Foto von {n}; die Rechte liegen dort', ''
    if 'dirty-chicken' in q:
        return 'fremd', 'Foto von Dirty Chicken, Rudis Pop-up im selben Haus', ''
    if q.startswith('valentin/'):
        return 'fremd', 'Momo und Rudi am Valentinsabend 2026, Foto von Culinarium', ''
    if 'Culinarium Hannover' in q or q.startswith(('aus-culinarium/', '../website/_varianten/')):
        return 'fremd', 'Foto von Rudi (Culinarium) von einem Abend in der Bar; die Rechte liegen bei Culinarium', ''
    return 'fremd', 'Foto aus den Unterlagen der Bar', ''


# Nachgeschärft (Vermerk in website/bilder.py, Robert 30.10.2026): Vorlage für «Vorher»
GESCHAERFT = {'konzert-scharf': 'facebook/2024-03-04_fb_816535553821520.jpg'}


def quelle_pfad(q):
    p = os.path.normpath(os.path.join(QUELLE, q))
    if os.path.exists(p):
        return p
    alt = os.path.normpath(os.path.join('/tmp/culinarium', q.replace('../../', ''))) if 'Culinarium Hannover' in q else ''
    return alt if alt and os.path.exists(alt) else None


def signatur(pfad):
    im = Image.open(pfad).convert('L').resize((17, 16), Image.LANCZOS)
    a = np.asarray(im, np.int16)
    return (a[:, 1:] > a[:, :-1]).flatten()


def katalog():
    aus, quellen, zusammen, gesehen = [], {}, {}, {}
    for k, (q, alt) in REG.items():
        mj = os.path.join(BILDER, k + '.json')
        if not os.path.exists(mj):
            print('nicht auf der Website gebaut:', k); continue
        if q in gesehen:                                           # Fehlerbuch 10a 19.10.2026: doppelte Einträge zusammenführen
            zusammen[k] = gesehen[q]; continue
        gesehen[q] = k
        m = json.load(open(mj))
        st = [s for s in m['stufen'] if os.path.exists(os.path.join(BILDER, s[1]))]
        if not st:
            print('nicht im Archiv:', k); continue
        gr = max(st)[1]; kl = min(st)[1]; mi = max([s for s in st if s[0] <= 1600] or [min(st)])[1]
        art, satz, u = herkunft(k, q)
        vor = GESCHAERFT.get(k)
        if vor:
            satz += '. Licht und Schärfe mit KI nachgeschärft'
        w, h = m['w'], m['h']
        f = 'hoch' if h > w * 1.04 else 'quer' if w > h * 1.04 else 'quadrat'
        aus.append(dict(k=k, t={'de': alt}, b=bereich(k, alt), s='jahr', f=f, w=w, h=h, art=art, q=satz, u=u, ue=bool(vor), alt=False, vn=False,
                        fl=f'../../assets/bild/{gr}', fm=f'../../assets/bild/{mi}', fs=f'../../assets/bild/{kl}'))
        quellen[k] = dict(druck=quelle_pfad(q), ausschnitt=None, original=quelle_pfad(vor) if vor else None)
    # gleiche Fotos unter verschiedenen Quellen (Bildvergleich, Abstand der Signaturen unter 0,08): ein Eintrag; das nachgeschärfte bleibt
    sigs = {d['k']: signatur(os.path.join(ROOT, d['fs'][6:])) for d in aus}
    weg = set()
    for i, a in enumerate(aus):
        for b in aus[i + 1:]:
            if b['k'] in weg or a['k'] in weg:
                continue
            if a['k'].startswith('p-') and b['k'].startswith('p-'):   # Plakate verschiedener Abende sehen sich ähnlich, bleiben aber eigene Einträge
                continue
            if np.mean(sigs[a['k']] != sigs[b['k']]) < .08 and a['art'] == b['art'] and a['f'] == b['f']:
                bleibt, geht = (b, a) if b['ue'] and not a['ue'] else (a, b)
                weg.add(geht['k']); zusammen[geht['k']] = bleibt['k']
    aus = [d for d in aus if d['k'] not in weg]
    for x in weg:
        quellen.pop(x, None)
    for x, z in list(zusammen.items()):                            # Ketten auflösen
        while z in zusammen:
            z = zusammen[z]
        zusammen[x] = z
    return aus, quellen, zusammen


def originale(aus, quellen):
    """Das unveränderte Ausgangsbild der nachgeschärften Fotos, auf die Grösse der Website gerechnet (original/<k>.webp), gleicher Ausschnitt."""
    if os.path.isdir(ORIG):
        shutil.rmtree(ORIG)
    os.makedirs(ORIG)
    n = 0
    for d in aus:
        o = quellen[d['k']]['original']
        if not (d['ue'] and o and os.path.exists(o)):
            continue
        with Image.open(os.path.join(ROOT, d['fl'][6:])) as nach:
            groesse = nach.size
        im = ImageOps.exif_transpose(Image.open(o)).convert('RGB')
        w, h = im.size; z = groesse[0] / groesse[1]
        if abs(w / h - z) > .005:
            if w / h > z:
                nw = round(h * z); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = round(w / z); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize(groesse, Image.LANCZOS).save(os.path.join(ORIG, d['k'] + '.webp'), 'WEBP', quality=80, method=5)
        d['vn'] = True
        n += 1
    return n


# ---------------------------------------------------------------- Zeichnen mit Chromium (SVG → PNG, unsichtbar, ein Lauf, eigener Prozess)
def svg_png(paare):
    """paare: [(svg, png, breite)]; jedes SVG in der gewünschten Breite auf durchsichtigem Grund (SVG als data:-Adresse, Falle 9)."""
    js = os.path.join(HIER, '_svg_png.js')
    open(js, 'w').write('''const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1 });
  for (const [svg, png, w, h] of JSON.parse(process.argv[2])) {
    await p.setViewportSize({ width: w, height: h });
    const d = 'data:image/svg+xml;base64,' + require('fs').readFileSync(svg).toString('base64');
    await p.setContent(`<html><body style="margin:0;background:transparent"><img src="${d}" style="display:block;width:${w}px;height:${h}px"></body></html>`);
    await p.waitForFunction(() => document.images[0].complete && document.images[0].naturalWidth > 0);
    await p.screenshot({ path: png, omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } }); }
  await b.close(); })();''')
    liste = []
    for svg, png, breite in paare:
        s = open(svg, encoding='utf-8').read()
        vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
        liste.append([svg, png, breite, round(breite * vb[3] / vb[2])])
    subprocess.run(['node', js, json.dumps(liste)], check=True, timeout=240, cwd=HIER)
    os.remove(js)


def logo_inhalt():
    """Die nachgezogene Wortmarke (potrace, _quelle/logo/wildside-logo-nachgezogen.svg): der Inhalt ohne Kopf, Farbe einsetzbar."""
    s = open(os.path.join(LOGO, 'wildside-logo-nachgezogen.svg'), encoding='utf-8').read()
    s = re.sub(r'<\?xml.*?\?>|<!DOCTYPE[^>]*>|<metadata>.*?</metadata>', '', s, flags=re.S)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', s, flags=re.S).group(1)
    return re.sub(r'\s+', ' ', inner).strip()


def ase(farben):
    def block(name, r, g, b):
        n = (name + '\0').encode('utf-16-be')
        body = struct.pack('>H', len(name) + 1) + n + b'RGB ' + struct.pack('>fff', r / 255, g / 255, b / 255) + struct.pack('>H', 2)
        return struct.pack('>HI', 1, len(body)) + body
    bl = b''.join(block(n, *rgb(h)) for n, h in farben)
    return b'ASEF' + struct.pack('>HHI', 1, 0, len(farben)) + bl


SCHRIFTEN = [
    ('t', 'Prata', 'prata-latin.woff2', 'Titel', '400, eine Stärke; nie fett, nie kursiv', 'Du sagst, was du magst.', 400),
    ('s', 'Hanken Grotesk', 'hanken-latin.woff2', 'Lesetext', '400, 17 px, Zeilenabstand 1,6', 'An der Bar sagst du, was du magst, und Momo macht dir einen Drink daraus.', 400),
    ('e', 'Hanken Grotesk', 'hanken-latin.woff2', 'Etiketten und Knöpfe', '500, 11,5 px, Versalien, 0,17 em gesperrt', 'DONNERSTAG BIS SAMSTAG AB 19 UHR', 500),
    ('z', 'Hanken Grotesk', 'hanken-latin.woff2', 'Zeiten, Daten, Preise', 'Tage in Hanken, Uhrzeiten in Prata wie im Fuss der Website; Preise und Listen mit gleich breiten Ziffern', 'Donnerstag 19 bis 1 Uhr', 400),
]


def dateien(fa):
    if os.path.isdir(DAT):
        shutil.rmtree(DAT)
    os.makedirs(DAT)
    F = {k: h for k, n, h, r, g, w in fa}
    liste, render = [], []
    inhalt = logo_inhalt()
    # Die Wortmarke: WILD SIDE ausgespart aus der schrägen Fläche, nachgezogen aus dem Logo der Bar; Rot als Hauptform, Creme auf Nacht, Nacht auf Creme
    var = []
    for k, farbe, grund in (('rot', F['rot'], 'dunkel'), ('creme', F['creme'], 'dunkel'), ('nacht', F['dunkel'], 'hell')):
        s = f'{SCHLUESSEL}-wortmarke-{k}.svg'; p = s[:-4] + '.png'
        open(os.path.join(DAT, s), 'w', encoding='utf-8').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1296 1600"><title>Walk on the Wild Side</title>'
            + inhalt.replace('fill="#111111"', f'fill="{farbe}"').replace('fill="#000000"', f'fill="{farbe}"') + '</svg>\n')
        render.append((os.path.join(DAT, s), os.path.join(DAT, p), 1600))
        var.append(dict(k=k, grund=grund, dateien=[s, p]))
    liste.append(dict(k='logo', var=var))
    # Die Vorlage: das Logo der früheren Seite wildside-hannover.de (2020), unverändert, und das Profilbild auf Instagram
    n = f'{SCHLUESSEL}-logo-vorlage-2020.png'
    shutil.copyfile(os.path.join(LOGO, 'wildside-logo-webarchiv-2020.png'), os.path.join(DAT, n))
    m = f'{SCHLUESSEL}-instagram-profilbild.jpg'
    shutil.copyfile(os.path.join(LOGO, 'wildside-profilbild-1080.jpg'), os.path.join(DAT, m))
    liste.append(dict(k='website', var=[dict(k='vorlage', grund='hell', dateien=[n], px=list(Image.open(os.path.join(DAT, n)).size)),
                                        dict(k='heute', grund='hell', dateien=[m], px=list(Image.open(os.path.join(DAT, m)).size))]))
    # Tapete: das Sternmuster der Website (assets/bild/haus-tapete.svg, die Rippen des Gewölbes), Gold auf Nacht und Gold tief auf Creme
    t_ = open(os.path.join(BILDER, 'haus-tapete.svg'), encoding='utf-8').read()
    kachel = re.search(r'<svg[^>]*>(.*)</svg>', t_, flags=re.S).group(1)
    var = []
    for k, grund, flaeche, linie in (('dunkel', 'dunkel', F['nacht'], F['gold']), ('hell', 'hell', F['creme'], F['gold-tief'])):
        s = f'{SCHLUESSEL}-tapete-{k}.svg'; p = s[:-4] + '.png'; w = s[:-4] + '.webp'
        k4 = ''.join(f'<g transform="translate({x * 150} {y * 150})">{kachel.replace("#D8B264", linie)}</g>' for x in range(4) for y in range(4))
        open(os.path.join(DAT, s), 'w', encoding='utf-8').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600"><title>Tapete Walk on the Wild Side</title><rect width="600" height="600" fill="{flaeche}"/>{k4}</svg>\n')
        render.append((os.path.join(DAT, s), os.path.join(DAT, p), 1200))
        var.append(dict(k=k, grund=grund, dateien=[p, s, w], farbe=flaeche))
    liste.append(dict(k='tapete', var=var))
    svg_png(render)
    for g in liste:
        for v in g['var']:
            png = next((x for x in v['dateien'] if x.endswith('.png')), None)
            if png and 'px' not in v:
                v['px'] = list(Image.open(os.path.join(DAT, png)).size)
    for v in next(g for g in liste if g['k'] == 'tapete')['var']:
        Image.open(os.path.join(DAT, v['dateien'][0])).convert('RGB').save(os.path.join(DAT, v['dateien'][2]), 'WEBP', quality=90)
    # Farben als Datei: CSS, JSON und ASE
    css = ':root{\n' + ''.join(f'  --{k}:{h}; /* {n}: {r} */\n' for k, n, h, r, g, w in fa) + '}\n'
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.css'), 'w', encoding='utf-8').write(f'/* {HAUS} · Farben der Marke ({STAND}), Werte der Website und der Plakate */\n' + css)
    json.dump([dict(name=n, hex=h, rgb=list(rgb(h)), rolle=r, gruppe=g, woher=w) for k, n, h, r, g, w in fa], open(os.path.join(DAT, f'{SCHLUESSEL}-farben.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(DAT, f'{SCHLUESSEL}-farben.ase'), 'wb').write(ase([(n, h) for k, n, h, r, g, w in fa]))
    liste.append(dict(k='farben', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-farben.css', f'{SCHLUESSEL}-farben.json', f'{SCHLUESSEL}-farben.ase'])]))
    # Schriften: die Dateien der Website, dazu als ZIP mit TTF und Lizenz (SIL Open Font License 1.1, Urheber aus der Schrift selbst)
    from fontTools.ttLib import TTFont
    ofl = open(os.path.join(HIER, '_ofl-vorlage.txt'), encoding='utf-8').read()
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-schriften.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for datei in sorted({s_[2] for s_ in SCHRIFTEN}):
            z.write(os.path.join(FONTS, datei), 'web/' + datei)
            f = TTFont(os.path.join(FONTS, datei)); recht = f['name'].getDebugName(0); fam = f['name'].getDebugName(1)
            f.flavor = None
            b = io.BytesIO(); f.save(b); z.writestr('programme/' + datei.replace('.woff2', '.ttf'), b.getvalue())
            z.writestr('lizenz/OFL-' + fam.lower().replace(' ', '-') + '.txt', recht + '\n' + ofl)
        z.writestr('LIESMICH.txt', f'''{HAUS} · Schriften der Marke ({STAND})

Prata 400: Titel. Eine Stärke, nie fett, nie kursiv.
Hanken Grotesk 400: Lesetext, 17 px, Zeilenabstand 1,6.
Hanken Grotesk 500: Etiketten und Knöpfe in Versalien, 0,17 em gesperrt.
Zeiten, Daten und Preise in Hanken Grotesk mit gleich breiten Ziffern (tabular-nums).

Beide stehen unter der SIL Open Font License 1.1 (frei für Druck, Website und Programme, auch gewerblich; nicht als Schrift allein verkaufen).
web/        die Dateien der Website
programme/  dieselben Schriften als TTF zum Installieren
lizenz/     Lizenztexte
''')
    liste.append(dict(k='schriften', var=[dict(k='alle', grund='hell', dateien=[f'{SCHLUESSEL}-schriften.zip'])]))
    alle = sorted(n_ for n_ in os.listdir(DAT) if not n_.endswith('-marke.zip'))   # erst die Liste, dann das ZIP (sonst packt es sich selbst ein)
    with zipfile.ZipFile(os.path.join(DAT, f'{SCHLUESSEL}-marke.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for n_ in alle:
            z.write(os.path.join(DAT, n_), n_)
    return liste


# ---------------------------------------------------------------- Beispiel für die Markenprüfung
def _schrift(namen, gr):
    for n in namen:
        for d in ('/usr/share/fonts/truetype/dejavu', '/usr/share/fonts/truetype/liberation', '/usr/share/fonts/truetype', '/usr/share/fonts'):
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, gr)
    r = subprocess.run(['fc-match', '-f', '%{file}', namen[0].split('.')[0]], capture_output=True, text=True)
    return ImageFont.truetype(r.stdout, gr) if r.stdout and os.path.exists(r.stdout) else ImageFont.load_default(gr)


def beispiel(F):
    """Ein eigens gezeichneter Entwurf, wie ihn eine Agentur schicken könnte: ein Beitrag für einen DJ-Abend mit einem Foto der Bar und der Wortmarke,
    aber in einer fremden Schrift (eine Serifenschrift fett), mit Neon-Pink und reinem Schwarz statt Nacht, Creme und Gold, und dem Wort «Sie».
    Geprüft mit der Prüfung selbst ohne Claude (LIVRE_KI=0); die Farben bleiben gemessen, Schrift, Zeichen, Bild und Ton bekommen Beispiel-Urteile, beschriftet."""
    os.environ['LIVRE_KI'] = '0'
    import livre as LV
    LV._livre.cache_clear()
    zb = os.path.join(HIER, 'beispiel')
    if os.path.isdir(zb):
        shutil.rmtree(zb)
    os.makedirs(zb)
    W, H = 1080, 1350
    PINK, SCHWARZ = (0xFF, 0x2E, 0xB8), (0, 0, 0)
    im = Image.new('RGB', (W, H), SCHWARZ)
    m = json.load(open(os.path.join(BILDER, 'voll.json')))
    foto = Image.open(os.path.join(BILDER, max(m['stufen'])[1])).convert('RGB')
    sk = max(W / foto.width, 860 / foto.height); foto = foto.resize((round(foto.width * sk), round(foto.height * sk)), Image.LANCZOS)
    y0 = round((foto.height - 860) * .45)
    im.paste(foto.crop(((foto.width - W) // 2, y0, (foto.width - W) // 2 + W, y0 + 860)), (0, 0))
    dr = ImageDraw.Draw(im)
    titel = _schrift(['DejaVuSerif-Bold.ttf', 'LiberationSerif-Bold.ttf'], 74)
    lese = _schrift(['DejaVuSerif.ttf', 'LiberationSerif-Regular.ttf'], 32)
    knopf = _schrift(['DejaVuSans-Bold.ttf', 'LiberationSans-Bold.ttf'], 26)
    dr.text((72, 910), 'Party-Nacht im Wild Side', font=titel, fill=(255, 255, 255))
    dr.text((72, 1020), 'Samstag ab 21 Uhr: DJ, Drinks und gute Laune.', font=lese, fill=(225, 225, 225))
    dr.text((72, 1066), 'Haasemannstraße 13 · Hannover-Linden', font=lese, fill=(225, 225, 225))
    dr.rectangle((72, 1170, 520, 1242), fill=PINK)
    dr.text((100, 1192), 'SICHERN SIE IHREN TISCH', font=knopf, fill=SCHWARZ)
    logo = Image.open(os.path.join(DAT, f'{SCHLUESSEL}-wortmarke-rot.png')).convert('RGBA'); logo.thumbnail((200, 250), Image.LANCZOS)
    dunkel = Image.new('RGBA', (W, 340), (0, 0, 0, 0)); dd = ImageDraw.Draw(dunkel)
    for i in range(340):
        dd.line((0, i, W, i), fill=(0, 0, 0, int(150 * (1 - i / 340))))
    im.paste(dunkel, (0, 0), dunkel); im.paste(logo, (64, 52), logo)
    im.save(os.path.join(zb, 'entwurf.png'), optimize=True)
    b = io.BytesIO(); im.save(b, 'PNG')
    j = LV.pruefen(dict(name='Beispiel-Entwurf «Party-Nacht im Wild Side», Instagram-Beitrag', typ='image/png', daten='data:image/png;base64,' + base64.b64encode(b.getvalue()).decode(), sprache='de'))
    j['beispiel'] = True
    kk = j.setdefault('ki', {})
    farb = [x for x in kk.get('punkte', []) if x.get('bereich') == 'farben']
    for x in farb:
        x['text'] = x['text'].replace('Gemessen ohne KI: ', 'Gemessen: ')
    kk['punkte'] = farb + [
        dict(bereich='farben', urteil='passt_nicht', titel='Neon-Pink und reines Schwarz', text=f'Der Knopf trägt ein Neon-Pink, die Fläche reines Schwarz. Bei Walk on the Wild Side tragen Nacht {F["nacht"]} und Platte {F["platte"]} die dunklen Flächen; Gold {F["gold"]} rahmt, Rot {F["rot"]} steht nur als Punkt.'),
        dict(bereich='schrift', urteil='passt_nicht', titel='Titel in einer fetten Serifenschrift', text='Der Titel steht fett in einer fremden Serifenschrift. Die Bar setzt Titel in Prata, eine Stärke, nie fett; Etiketten und Knöpfe in Hanken Grotesk, Versalien, gesperrt.'),
        dict(bereich='zeichen', urteil='passt', titel='Die Wortmarke steht richtig', text='Das Logo mit WILD SIDE in der schrägen roten Fläche steht auf dunklem Grund, unverzerrt und mit Luft rundherum.'),
        dict(bereich='bild', urteil='passt', titel='Das Foto zeigt einen vollen Abend', text='Gäste an den Tischen vor der Bar, warmes Licht: ein Foto aus dem Bildarchiv, genau der Moment an der Bar, der nach vorn gehört.'),
        dict(bereich='ton', urteil='achten', titel='Du statt Sie', text='Die Bar duzt ihre Gäste, knapp und ein bisschen laut. «Sichern Sie Ihren Tisch» klingt nach Verkauf; die Bar sagt «Platz anfragen» oder einfach, wann es losgeht.'),
    ]
    kk['gesamt'] = ('Ein guter Anfang: Foto und Wortmarke passen zu einem Abend im Wild Side. Schrift, Pink und Schwarz kommen nicht aus der Marke; '
                    'mit Prata, Nacht, Creme und einer Goldlinie wird daraus ein Beitrag, der aussieht wie die Website.')
    kk['ton'] = [dict(stelle='SICHERN SIE IHREN TISCH', vorschlag='Platz anfragen')]
    j['probe'] = False
    json.dump(j, open(os.path.join(zb, 'pruefung.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    return j


def listen_bilder():
    z = os.path.join(HIER, 'listen')
    if os.path.isdir(z):
        shutil.rmtree(z)
    os.makedirs(z)
    port = 9085
    seiten = [f'http://127.0.0.1:{port}/{n}' for n in ('index.html', 'drinks.html', 'haus.html', 'besuch.html')]
    r = subprocess.run(['node', os.path.join(HIER, 'listen_bilder.js'), z] + seiten, timeout=420, capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode:
        raise SystemExit('listen_bilder.js: ' + r.stderr[-600:])
    for n in os.listdir(z):
        im = Image.open(os.path.join(z, n)).convert('RGB'); im.thumbnail((1200, 800), Image.LANCZOS)
        im.save(os.path.join(z, n[:-4] + '.webp'), 'WEBP', quality=84, method=5); os.remove(os.path.join(z, n))


TON = dict(eigene_worte=['Nachbarschafts-Mixology-Bar', 'Du sagst, was du magst', 'Good Drinks, Good Music, Good Energy', 'Let’s go wild', 'Momos sexy Drinks', 'Wild Side Tradition'],
           nicht=['Sie', 'keine Karte', 'einmal im Jahr eine Karte', 'Cocktail-Lounge', 'exklusiv', 'Event-Location', 'Superlative'])


def main():
    t0 = time.time()
    fa = farben_liste()
    F = {k: h for k, n, h, r, g, w in fa}
    aus, quellen, zusammen = katalog()
    n_orig = originale(aus, quellen)
    liste = dateien(fa)
    groessen = {f: os.path.getsize(os.path.join(DAT, f)) for f in sorted(os.listdir(DAT))}
    daten = dict(haus=HAUS, ort='Hannover-Linden', fotos=aus, dateien=liste,
                 farben=[dict(k=k, n=n, h=h.upper(), rgb=list(rgb(h)), r=r, g=g, woher=w) for k, n, h, r, g, w in fa],
                 gruppen=[dict(k=k, n=n, s=s) for k, n, s in GRUPPEN], glanz=[], groessen=groessen,
                 bereiche=[b for b in BEREICHE if any(f['b'] == b for f in aus)],
                 schriften=[dict(k=k, n=fam, d=d, r=r, e=ein, p=p, w=w) for k, fam, d, r, ein, p, w in SCHRIFTEN],
                 namen=NAMEN, zusammen=zusammen, ton=TON,
                 stand=dict(fotos=len(aus), haus=sum(1 for x in aus if x['art'] == 'haus'), frei=sum(1 for x in aus if x['art'] == 'frei'),
                            ki=sum(1 for x in aus if x['art'] == 'ki'), fremd=sum(1 for x in aus if x['art'] == 'fremd'), partner=0,
                            ue=sum(1 for x in aus if x['ue']), vn=n_orig, original=sum(1 for v in quellen.values() if v['druck'] and os.path.exists(v['druck'])),
                            dateien=len(groessen), datum=STAND))
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump({k: dict(druck=v['druck'] and os.path.relpath(v['druck'], PROJEKTE), ausschnitt=v['ausschnitt'],
                       original=v['original'] and os.path.relpath(v['original'], PROJEKTE)) for k, v in quellen.items()},
              open(os.path.join(HIER, '_quellen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    beispiel(F)
    if '--ohne-listen' not in sys.argv:
        listen_bilder()
    fotos = {f['k']: f for f in aus}
    for g in daten['gruppen']:
        b, satz = GRUPPE_BILD[g['k']]
        g['bild'] = b if '/' in b else fotos[b]['fm']
        g['bild_t'] = satz
    for s_ in daten['schriften']:
        s_['bild'] = f'listen/schrift-{s_["k"]}.webp'
    for g in daten['gruppen']:
        p = os.path.join(ROOT, g['bild'][6:]) if g['bild'].startswith('../../') else os.path.join(HIER, g['bild'])
        if not os.path.exists(p):
            raise SystemExit('Bild fehlt: ' + g['bild'])
    for s_ in daten['schriften']:
        if not os.path.exists(os.path.join(HIER, s_['bild'])):
            print('Hinweis: Schriftbild fehlt', s_['bild']); s_.pop('bild')
    json.dump(daten, open(os.path.join(HIER, 'livre.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    seite(F)
    st = daten['stand']
    print(f'livre.json: {len(aus)} Fotos ({st["haus"]} von der Bar, {st["fremd"]} fremde Rechte, {st["ue"]} nachgeschärft, '
          f'{n_orig} mit Vorher, {st["original"]} mit Original) · {len(zusammen)} doppelte zusammengeführt · {len(groessen)} Dateien · {time.time() - t0:.0f} s')


def v_von(*namen):
    h = hashlib.sha1()
    for n in namen:
        p = os.path.join(HIER, n)
        h.update(open(p, 'rb').read() if os.path.exists(p) else b'-')
    return h.hexdigest()[:10]


def seite(F):
    v = v_von('livre.json'); vc = v_von('livre.css'); vj = v_von('livre.js')
    open(os.path.join(HIER, 'index.html'), 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{NAME} · Walk on the Wild Side Hannover</title>
<meta name="description" content="{NAME}, die Marke von Walk on the Wild Side zum Arbeiten: Bildarchiv mit fertigen Grössen, die Wortmarke, Tapete und Farben als Dateien, Markenprüfung für Entwürfe, Hausregeln.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{F['nacht']}">
<link rel="icon" href="/assets/oberflaeche/kleid/wildside-zeichen.svg" type="image/svg+xml">
<script src="/assets/oberflaeche/kleid/wildside.js?v={v_von('../oberflaeche/kleid/wildside.js')}"></script>
<link rel="preload" href="../../assets/schrift/prata-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="../../assets/schrift/hanken-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="livre.json?v={v}" as="fetch" crossorigin>
<link rel="stylesheet" href="/assets/oberflaeche/grund.css?v={v_von('../oberflaeche/grund.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/rahmen-buehne.css?v={v_von('../oberflaeche/rahmen-buehne.css')}">
<link rel="stylesheet" href="/assets/oberflaeche/kleid/wildside.css?v={v_von('../oberflaeche/kleid/wildside.css')}">
<link rel="stylesheet" href="livre.css?v={vc}">
</head>
<body class="li wo-app">
<header class="wo-kopf" id="kopf"></header>
<aside class="wo-rand" id="rand" aria-label="{NAME}"></aside>
<main class="wo-raum" id="haupt"><div id="ansicht"></div></main>
<footer class="wo-leiste" id="leiste" aria-live="polite"></footer>
<div class="fenster" id="fenster" hidden></div>
<div class="meldung" id="meldung" aria-live="polite"></div>
<noscript><p class="li-noscript">{NAME} braucht JavaScript.</p></noscript>
<script src="start.js?v={v_von('start.js')}" data-v="{vj}"></script>
<script src="/assets/oberflaeche/oberflaeche.js?v={v_von('../oberflaeche/oberflaeche.js')}"></script>
<script src="livre.js?v={vj}"></script>
</body>
</html>
''')


if __name__ == '__main__':
    if sys.argv[1:] == ['seite']:
        seite({k: h for k, n, h, r, g, w in farben_liste()})
    else:
        main()
