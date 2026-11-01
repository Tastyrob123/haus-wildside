"""Gastschichten von Walk on the Wild Side im Schaufenster (1.11.2026, gleiches Muster wie die DJ-Abende in termine.py).

Robert 1.11.2026: «wie würde ich hier neue Gastgeschichten hinzufügen?» Die Gastschichten (Gäste hinterm Tresen) stehen auf der Seite
«Programm» als verdeckte Karten, die sich umdrehen. Die Website baut sie aus einer Liste in website/unter.py › programm() › gaeste
(Foto, Datum, Name, Satz). Diese Liste ist der Ursprung: sie wird gelesen (ast, nie ausgeführt), nie abgetippt und nie verändert.
Entwurf, veröffentlichter Stand und Verlauf liegen hier (Master Werkzeug-Bau 2.2) mit Sicherung der letzten guten Fassung (.gut).
Ausgeliefert wird der Stand, indem der Server programm.html der Probe-Kopie an genau dieser Stelle füllt (fuelle()): die Karten in der
Reihe nach Datum, dazu der Satz «Fünf Gastschichten aus dem Jahr 2024.» mit Zahl und Jahren der Liste. Ohne Änderung bleibt die Seite
Byte für Byte, wie die Website sie gebaut hat. Fotos: jedes Foto der Website (website/assets/bild/<schlüssel>.json) oder ein eigenes,
im Schaufenster hochgeladenes (Datenordner des Stamms, website-fotos/u-….json; der Stamm legt es auch in die Probe-Kopie).

Jede Anfrage, die den Entwurf ersetzt, trägt dessen Fingerabdruck (erwartet); passt er nicht mehr: KONFLIKT (409, L13).
Meldungen in der Form STICHWORT · Text (Master 2.6), jedes Stichwort steht im Lexikon der Prüfseite (pruefung-haus.js)."""
import ast
import datetime
import hashlib
import html
import json
import os
import re
import threading
import time
from pathlib import Path

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent.parent
WEB = PROJEKT / 'website'
QUELLE = WEB / 'unter.py'
BILDER = WEB / 'bilder.py'
BILD = WEB / 'assets' / 'bild'
STAMM = Path(os.path.expanduser('~/Desktop/Website-Projekte/_Werkzeuge'))
DATEN = Path(os.environ['WERKZEUGE_DATEN']) / 'bureau-gaeste' if os.environ.get('WERKZEUGE_DATEN') else HIER / '_daten'
DATEI = DATEN / 'gaeste.json'
WER = 'Team Wild Side'
HOECHSTENS = 24
_SCHLOSS = threading.Lock()
E = html.escape
ZAHLWORT = ['Keine', 'Eine', 'Zwei', 'Drei', 'Vier', 'Fünf', 'Sechs', 'Sieben', 'Acht', 'Neun', 'Zehn', 'Elf', 'Zwölf']


class Fehler(Exception):
    def __init__(self, status, stichwort, text):
        super().__init__(text)
        self.status, self.stichwort, self.text = status, stichwort, text


_ZW = {}


def _quelle():
    """Die Liste gaeste aus website/unter.py › programm() und die Beschreibungen der Fotos aus website/bilder.py (zwischengespeichert)."""
    try:
        zeit = (QUELLE.stat().st_mtime, BILDER.stat().st_mtime)
    except OSError:
        raise Fehler(503, 'gaeste-quelle', 'GASTSCHICHTEN · website/unter.py ist nicht lesbar.')
    if _ZW.get('zeit') != zeit:
        liste, alt = None, {}
        try:
            for n in ast.walk(ast.parse(QUELLE.read_text(encoding='utf-8'))):
                if isinstance(n, ast.FunctionDef) and n.name == 'programm':
                    for m in ast.walk(n):
                        if isinstance(m, ast.Assign) and len(m.targets) == 1 and getattr(m.targets[0], 'id', None) == 'gaeste':
                            liste = ast.literal_eval(m.value)
            for n in ast.parse(BILDER.read_text(encoding='utf-8')).body:
                if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], 'id', None) == 'BILDER':
                    alt = {k: v[1] for k, v in ast.literal_eval(n.value).items()}
        except (OSError, SyntaxError, ValueError) as e:
            raise Fehler(503, 'gaeste-quelle', f'GASTSCHICHTEN · website/unter.py ist nicht lesbar ({e}).')
        if not isinstance(liste, list):
            raise Fehler(503, 'gaeste-quelle', 'GASTSCHICHTEN · In website/unter.py › programm() steht keine Liste «gaeste» mehr. Die Website wurde umgebaut; die Gastschichten lassen sich erst wieder pflegen, wenn die Liste da ist.')
        _ZW.update(zeit=zeit, liste=liste, alt=alt)
    return _ZW


def _fotos_ordner():
    return Path(os.environ.get('WERKZEUGE_DATEN') or STAMM / 'daten') / 'wildside' / 'website-fotos'


def _eigene():
    """Eigene, im Schaufenster hochgeladene Fotos (vom Stamm abgelegt): {schlüssel: {w, h, alt, breiten}}."""
    aus = {}
    o = _fotos_ordner()
    if o.is_dir():
        for m in sorted(o.glob('u-*.json')):
            try:
                aus[m.stem] = json.loads(m.read_text(encoding='utf-8'))
            except ValueError:
                continue
    return aus


def fotos():
    """Zur Wahl: eigene Fotos zuerst, dann jedes Foto der Website mit Stufen (ohne Plakate und Zeichen): [{key, alt, bild, eigen}]."""
    probe = Path(os.environ['WEBSITE_PROBE']).name if os.environ.get('WEBSITE_PROBE') else '_probe'
    aus = [{'key': k, 'alt': m.get('alt') or 'Eigenes Foto', 'bild': f'/werkzeuge/website/{probe}/wildside/grundlage/assets/bild/{k}-{m["breiten"][0]}.webp', 'eigen': True}
           for k, m in _eigene().items() if m.get('breiten')]
    for k, a in _quelle()['alt'].items():
        if not k.startswith('p-') and (BILD / f'{k}.json').is_file():
            aus.append({'key': k, 'alt': a, 'bild': f'/assets/bild/{k}-480.webp', 'eigen': False})
    reihe = [g[0] for g in _quelle()['liste']]
    return sorted(aus, key=lambda f: (not f['eigen'], f['key'] not in reihe, reihe.index(f['key']) if f['key'] in reihe else 0))


def _iso(d):
    t, m, j = d.split('.')
    return f'{j}-{m}-{t}'


def _punkt(iso):
    j, m, t = iso.split('-')
    return f'{t}.{m}.{j}'


def ursprung():
    aus, ids = [], set()
    for i, g in enumerate(_quelle()['liste']):
        try:
            k, d, n, s = g
            iso = _iso(d)
        except (ValueError, TypeError):
            raise Fehler(503, 'gaeste-quelle', f'GASTSCHICHTEN · Eintrag {i + 1} der Liste gaeste (website/unter.py) ist nicht lesbar.')
        gid = 'g' + iso.replace('-', '')
        while gid in ids:
            gid += 'b'
        ids.add(gid)
        aus.append({'id': gid, 'datum': iso, 'name': n, 'satz': s, 'foto': k})
    try:
        return [pruefe_einen(g, i) for i, g in enumerate(aus)]
    except Fehler as e:
        raise Fehler(503, 'gaeste-quelle', f'GASTSCHICHTEN · Die Liste in website/unter.py ist nicht lesbar ({e.text}).')


def fingerabdruck(liste):
    return hashlib.sha1(json.dumps(liste, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()[:12]


def _text(wert, nr, feld, hoechstens, stichwort, leer):
    s = re.sub(r'\s+', ' ', str(wert if wert is not None else '')).strip()
    if not s:
        raise Fehler(400, stichwort, leer)
    if len(s) > hoechstens:
        raise Fehler(400, 'gast-lang', f'ZU LANG · {nr}{feld} hat höchstens {hoechstens} Zeichen.')
    if re.search(r'[<>{}]', s):
        raise Fehler(400, 'gast-zeichen', f'ZEICHEN · {nr}{feld}: spitze und geschweifte Klammern stehen nicht auf der Karte.')
    return s


def pruefe_einen(g, i=0):
    """Eine Gastschicht: Datum, Name des Gastes oder der Bar, ein Satz, Foto. Alles andere wird abgelehnt."""
    if not isinstance(g, dict):
        raise Fehler(400, 'gast-falsch', 'GASTSCHICHT · Ein Eintrag ist keine Gastschicht.')
    nr = f'Gastschicht {i + 1}: '
    gid = str(g.get('id') or '')
    if not re.fullmatch(r'[a-z0-9-]{1,24}', gid):
        raise Fehler(400, 'gast-falsch', 'GASTSCHICHT · ' + nr + 'Kennung fehlt.')
    d = str(g.get('datum') or '')
    try:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d):
            raise ValueError
        datetime.date.fromisoformat(d)
    except ValueError:
        raise Fehler(400, 'gast-datum', 'DATUM · ' + nr + 'Das Datum fehlt oder gibt es nicht.')
    name = _text(g.get('name'), nr, 'Der Name', 50, 'gast-name', 'NAME · ' + nr + 'Wer stand hinterm Tresen? Bitte den Namen des Gastes oder der Bar eintragen.')
    satz = _text(g.get('satz'), nr, 'Der Satz', 160, 'gast-satz', 'SATZ · ' + nr + 'Ein Satz zum Gast fehlt: woher er kommt, was er mitgebracht hat.')
    k = str(g.get('foto') or '')
    if not (re.fullmatch(r'[a-z0-9][\w-]{0,60}', k) and ((BILD / f'{k}.json').is_file() or (k.startswith('u-') and k in _eigene()))) or k.startswith('p-'):
        raise Fehler(400, 'gast-foto', 'FOTO · ' + nr + 'Bitte ein Foto der Website oder ein eigenes Foto wählen.')
    return {'id': gid, 'datum': d, 'name': name, 'satz': satz, 'foto': k}


def pruefe(liste):
    if not isinstance(liste, list):
        raise Fehler(400, 'gast-falsch', 'GASTSCHICHTEN · Die Anfrage enthält keine Liste von Gastschichten.')
    if not liste:
        raise Fehler(400, 'gast-leer', 'LEER · Mindestens eine Gastschicht bleibt auf der Seite; sonst stünde dort eine leere Reihe.')
    if len(liste) > HOECHSTENS:
        raise Fehler(400, 'gast-viele', f'GASTSCHICHTEN · Höchstens {HOECHSTENS} Gastschichten stehen gleichzeitig auf der Website.')
    aus = [pruefe_einen(g, i) for i, g in enumerate(liste)]
    if len({g['id'] for g in aus}) != len(aus):
        raise Fehler(400, 'gast-falsch', 'GASTSCHICHT · Zwei Gastschichten tragen dieselbe Kennung.')
    return sorted(aus, key=lambda g: (g['datum'], g['id']))


def _leer():
    return {'entwurf': None, 'stand': None, 'verlauf': [], 'protokoll': []}


def lade():
    for p in (DATEI, DATEI.with_suffix('.json.gut')):
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding='utf-8'))
                if isinstance(d, dict) and 'verlauf' in d:
                    return d
            except ValueError:
                continue
    if DATEI.is_file():
        raise Fehler(500, 'gaeste-speicher', 'SPEICHER · Die Datei der Gastschichten und ihre Sicherung sind beide unlesbar. Prüfung öffnen.')
    return _leer()


def schreib(d):
    DATEN.mkdir(parents=True, exist_ok=True)
    if DATEI.is_file():
        try:
            json.loads(DATEI.read_text(encoding='utf-8'))
            DATEI.replace(DATEI.with_suffix('.json.gut'))
        except ValueError:
            pass
    tmp = DATEI.with_suffix('.tmp')
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp.replace(DATEI)


def jetzt():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def lage(d=None):
    d = d or lade()
    u = ursprung()
    stand = d['stand'] if d['stand'] is not None else u
    entwurf = d['entwurf']
    return {'ursprung': u, 'stand': stand, 'entwurf': entwurf, 'wartet': entwurf is not None and entwurf != stand,
            'kennung': fingerabdruck(entwurf if entwurf is not None else stand),
            'zuletzt': next((v for v in reversed(d['verlauf']) if v.get('art') == 'veroeffentlicht'), None),
            'verlauf': [{'nr': i, 'zeit': v['zeit'], 'art': v['art'], 'notiz': v.get('notiz', ''), 'zahl': len(v['gaeste'])} for i, v in enumerate(d['verlauf'])][::-1],
            'fotos': fotos(),
            'quelle': 'website/unter.py › programm() › gaeste'}


def wartend(l):
    if not l['wartet']:
        return 0
    alt, neu = {g['id']: g for g in l['stand']}, {g['id']: g for g in l['entwurf']}
    return sum(1 for k, g in neu.items() if alt.get(k) != g) + sum(1 for k in alt if k not in neu)


def _bewache(d, erwartet):
    l = lage(d)
    if erwartet != l['kennung']:
        raise Fehler(409, 'konflikt', 'KONFLIKT · In einem anderen Fenster wurden die Gastschichten inzwischen geändert. Die Liste lädt neu, deine Eingaben bleiben stehen.')
    return l


def _protokoll(d, was):
    d['protokoll'] = (d['protokoll'] + [{'zeit': jetzt(), 'wer': WER, 'was': was}])[-400:]


def speichern(liste, erwartet):
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        neu = pruefe(liste)
        alt = l['entwurf'] if l['entwurf'] is not None else l['stand']
        if neu == alt:
            return {'nichts': True, 'meldung': 'Nichts geändert, nichts gespeichert.', **lage(d)}
        d['entwurf'] = None if neu == l['stand'] else neu
        _protokoll(d, 'Gastschichten im Entwurf gespeichert')
        schreib(d)
        return {'vorher': alt, **lage(d)}


def veroeffentlichen(erwartet, notiz=''):
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        if not l['wartet']:
            return {'nichts': True, 'meldung': 'Nichts geändert, nichts veröffentlicht.', **l}
        d['stand'] = l['entwurf']
        d['entwurf'] = None
        d['verlauf'] = (d['verlauf'] + [{'zeit': jetzt(), 'art': 'veroeffentlicht', 'notiz': str(notiz or '')[:200], 'gaeste': d['stand']}])[-60:]
        _protokoll(d, 'Gastschichten veröffentlicht')
        schreib(d)
        return lage(d)


def verwerfen(erwartet):
    with _SCHLOSS:
        d = lade()
        _bewache(d, erwartet)
        vorher = d['entwurf']
        d['entwurf'] = None
        _protokoll(d, 'Entwurf der Gastschichten verworfen')
        schreib(d)
        return {'vorher': vorher, **lage(d)}


def zurueckholen(nr, erwartet):
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        if nr == 'ursprung':
            g = l['ursprung']
        else:
            try:
                g = d['verlauf'][int(nr)]['gaeste']
            except (ValueError, IndexError, TypeError):
                raise Fehler(404, 'fassung-unbekannt', 'FASSUNG · Diese frühere Fassung gibt es nicht.')
        d['entwurf'] = None if g == l['stand'] else g
        _protokoll(d, 'Frühere Fassung der Gastschichten in den Entwurf geholt')
        schreib(d)
        return lage(d)


# ------------------------------------------------------------------ Ausliefern: die Reihe der verdeckten Karten auf «Programm»
# Genau wie website/unter.py › programm() sie baut (bau.py › img_tag), eigene Fotos wie der Stamm sie in die Kopie legt.
def _img(k, v):
    sizes = '(max-width:760px) 44vw, 19vw'
    if k.startswith('u-'):
        m = _eigene()[k]
        srcset = ', '.join(f'assets/bild/{k}-{w}.webp {w}w' for w in m['breiten'])
        return '', '<img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" width="%d" height="%d">' % (srcset, sizes, E(m.get('alt') or ''), m['w'], m['h'])
    d = json.loads((BILD / f'{k}.json').read_text(encoding='utf-8'))
    srcset = ', '.join('assets/bild/%s?v=%s %dw' % (f, v, b) for b, f in d['stufen'])
    return d['lq'], '<img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" width="%d" height="%d">' % (srcset, sizes, E(_quelle()['alt'].get(k, '')), d['w'], d['h'])


def _karte(n, g, v):
    lq, img = _img(g['foto'], v)
    stil = '--lq:url(%s)' % lq if lq else ''
    return ('<article class="vk-p" style="--n:%d"><div class="vk-karte"><div class="vk-rueck" aria-hidden="true"><span>WALK ON THE</span><b>WILD SIDE</b><span>GASTSCHICHT</span></div>'
            '<div class="vk-vorn"><figure class="vk-bild" style="%s">%s</figure></div></div><div class="vk-satz"><span class="etikett">%s</span><h3 class="titel">%s</h3><p>%s</p></div></article>') % (
        n, stil, img, E(_punkt(g['datum'])), E(g['name']), E(g['satz']))


def zahlsatz(liste):
    n = len(liste)
    jahre = sorted({g['datum'][:4] for g in liste})
    wann = f'aus dem Jahr {jahre[0]}' if len(jahre) == 1 else f'aus den Jahren {jahre[0]} und {jahre[1]}' if len(jahre) == 2 else f'aus den Jahren {jahre[0]} bis {jahre[-1]}'
    return f'{ZAHLWORT[n] if n < len(ZAHLWORT) else n} Gastschicht{"" if n == 1 else "en"} {wann}.'


def fuelle(roh, liste, u):
    """programm.html mit einer Liste füllen. Gleich wie der Ursprung: unverändert zurück."""
    if liste == u:
        return roh
    m = re.search(r'assets/bild/[\w-]+\.webp\?v=(\w+)', roh)
    v = m.group(1) if m else ''
    liste = sorted(liste, key=lambda g: (g['datum'], g['id']))
    reihe = ''.join(_karte(n, g, v) for n, g in enumerate(liste))
    roh, n = re.subn(r'(<div class="vk-reihe auf">)(.*?)(</div></div></section>)', lambda x: x.group(1) + reihe + x.group(3), roh, count=1, flags=re.S)
    if not n:
        raise Fehler(503, 'gaeste-stelle', 'GASTSCHICHTEN · Die Seite «Programm» hat die Stelle für die Gastschichten nicht mehr; sie zeigt ihre gebauten Gastschichten.')
    alt = zahlsatz(u)
    if alt in roh:
        roh = roh.replace(alt, zahlsatz(liste), 1)
    return roh


def ausliefern(roh, welche='stand'):
    l = lage()
    liste = l['entwurf'] if welche == 'entwurf' and l['entwurf'] is not None else l['stand']
    return fuelle(roh, liste, l['ursprung'])


def pruefung():
    p = []
    try:
        u = ursprung()
        p.append({'gut': True, 'titel': 'Gastschichten der Website', 'text': f'{len(u)} Gastschichten in website/unter.py gelesen, {len(fotos())} Fotos zur Wahl.'})
    except Fehler as e:
        return [{'gut': False, 'titel': 'Gastschichten der Website', 'text': e.text, 'stichwort': e.stichwort}]
    try:
        fuelle((WEB / 'programm.html').read_text(encoding='utf-8'), [dict(g, id=g['id'] + 'x') for g in u], u)
        p.append({'gut': True, 'titel': 'Stelle auf der Seite «Programm»', 'text': 'Die Reihe der verdeckten Karten lässt sich aus der Liste füllen.'})
    except (Fehler, OSError) as e:
        p.append({'gut': False, 'titel': 'Stelle auf der Seite «Programm»', 'text': getattr(e, 'text', str(e)), 'stichwort': 'gaeste-stelle'})
    try:
        d = lade()
        for k in ('stand', 'entwurf'):
            if d[k] is not None:
                pruefe(d[k])
        p.append({'gut': True, 'titel': 'Speicher der Gastschichten', 'text': 'lesbar' + (', Sicherung der letzten guten Fassung liegt daneben' if DATEI.with_suffix('.json.gut').is_file() else ', noch nichts gespeichert') + '.'})
    except Fehler as e:
        p.append({'gut': False, 'titel': 'Speicher der Gastschichten', 'text': e.text, 'stichwort': e.stichwort})
    return p
