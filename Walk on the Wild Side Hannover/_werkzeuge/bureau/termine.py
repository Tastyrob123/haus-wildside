"""DJ-Abende von Walk on the Wild Side im Schaufenster (Nachtbau 31.10.2026, Vorlage: die Termine des Culinarium vom 28.10.2026).

Die Website zeichnet die DJ-Abende der Bar (auf den Plakaten «SESSION») aus einer Liste in website/bau.py (LINEUP: Datum, Name, Zeile,
Plakat, neuester Abend zuerst): die Plakatwand im Kopf der Seite «Programm», den Kontaktbogen «Jeder Abend ein Plakat.» und den Flyer
auf der Startseite. Diese Liste ist der Ursprung: sie wird gelesen (ast, nie ausgeführt), nie abgetippt und nie verändert.
Hier liegen dazu Entwurf, veröffentlichter Stand und Verlauf (Master Werkzeug-Bau 2.2), in einer Datei mit Sicherung der letzten
guten Fassung (.gut). Ausgeliefert wird der Stand, indem der Server des Schaufensters index.html und programm.html der Probe-Kopie
beim Ausliefern an genau diesen drei Stellen mit dem Stand füllt (fuelle()); ohne Änderung bleibt jede Datei Byte für Byte, wie die
Website sie gebaut hat. Die Bilder kommen aus website/assets/bild/<plakat>.json (Stufen, Vorschaubild), die Beschreibung aus
website/bilder.py › BILDER, beides nur gelesen; nichts aus _quelle/.

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
WEB = HIER.parent.parent / 'website'
QUELLE = WEB / 'bau.py'
BILDER = WEB / 'bilder.py'
BILD = WEB / 'assets' / 'bild'
DATEN = Path(os.environ['WERKZEUGE_DATEN']) / 'bureau-termine' if os.environ.get('WERKZEUGE_DATEN') else HIER / '_daten'
DATEI = DATEN / 'termine.json'
WER = 'Team Wild Side'
HOECHSTENS = 40
_SCHLOSS = threading.Lock()
E = html.escape


class Fehler(Exception):
    def __init__(self, status, stichwort, text):
        super().__init__(text)
        self.status, self.stichwort, self.text = status, stichwort, text


def _konstanten(p, namen):
    """Werte einfacher Zuweisungen aus einer Python-Datei der Website, gelesen mit ast (nie ausgeführt)."""
    aus = {}
    for n in ast.parse(p.read_text(encoding='utf-8')).body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and getattr(n.targets[0], 'id', None) in namen:
            aus[n.targets[0].id] = ast.literal_eval(n.value)
    return aus


_ZW = {}


def _bau():
    """LINEUP und Fassungsnummer V aus website/bau.py, Beschreibungen der Plakate aus website/bilder.py (zwischengespeichert nach Änderungszeit)."""
    try:
        zeit = (QUELLE.stat().st_mtime, BILDER.stat().st_mtime)
    except OSError:
        raise Fehler(503, 'termine-quelle', 'DJ-ABENDE · website/bau.py ist nicht lesbar.')
    if _ZW.get('zeit') != zeit:
        try:
            k = _konstanten(QUELLE, {'LINEUP', 'V'})
            b = _konstanten(BILDER, {'BILDER'}).get('BILDER') or {}
        except (OSError, SyntaxError, ValueError) as e:
            raise Fehler(503, 'termine-quelle', f'DJ-ABENDE · website/bau.py ist nicht lesbar ({e}).')
        if not isinstance(k.get('LINEUP'), list):
            raise Fehler(503, 'termine-quelle', 'DJ-ABENDE · In website/bau.py steht keine Liste «LINEUP» mehr. Die Website wurde umgebaut; die DJ-Abende lassen sich erst wieder pflegen, wenn die Liste da ist.')
        _ZW.update(zeit=zeit, lineup=k['LINEUP'], v=str(k.get('V') or ''), alt={s: a for s, (q, a) in b.items()})
    return _ZW


def plakate():
    """Die Plakate der Bar, die die Website kennt (Schlüssel p-…, mit Stufen in assets/bild), neuestes zuerst: [{key, alt, bild}]."""
    z = _bau()
    aus = []
    for s in z['alt']:
        if s.startswith('p-') and (BILD / f'{s}.json').is_file():
            m = re.search(r'\d\d\.\d\d\.\d{4}', z['alt'][s])
            n = next((l[1] for l in z['lineup'] if m and l[0] == m.group(0)), '')
            aus.append({'key': s, 'alt': z['alt'][s], 'titel': f'{m.group(0)} · {n}' if m and n else z['alt'][s], 'bild': f'/assets/bild/{s}-480.webp'})
    reihe = [l[3] for l in z['lineup']]
    return sorted(aus, key=lambda p: reihe.index(p['key']) if p['key'] in reihe else -1)


def _iso(d):
    t, m, j = d.split('.')
    return f'{j}-{m}-{t}'


def _punkt(iso):
    j, m, t = iso.split('-')
    return f'{t}.{m}.{j}'


def ursprung():
    """Die DJ-Abende, wie die Website sie gebaut hat (LINEUP in bau.py), mit fester Kennung aus dem Datum."""
    aus, ids = [], set()
    for i, l in enumerate(_bau()['lineup']):
        try:
            d, n, r, k = l
            iso = _iso(d)
        except (ValueError, TypeError):
            raise Fehler(503, 'termine-quelle', f'DJ-ABENDE · Eintrag {i + 1} in LINEUP (website/bau.py) ist nicht lesbar.')
        tid = 'd' + iso.replace('-', '')
        while tid in ids:
            tid += 'b'
        ids.add(tid)
        aus.append({'id': tid, 'datum': iso, 'name': n, 'zeile': r, 'plakat': k})
    try:
        return [pruefe_einen(t, i) for i, t in enumerate(aus)]
    except Fehler as e:
        raise Fehler(503, 'termine-quelle', f'DJ-ABENDE · Die Liste in website/bau.py ist nicht lesbar ({e.text}).')


def fingerabdruck(liste):
    return hashlib.sha1(json.dumps(liste, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()[:12]


def _text(wert, nr, feld, hoechstens, leer_ok):
    s = re.sub(r'\s+', ' ', str(wert if wert is not None else '')).strip()
    if not s and not leer_ok:
        raise Fehler(400, 'termin-name', 'NAME · ' + nr + 'Wer legt auf? Bitte den Namen eintragen.')
    if len(s) > hoechstens:
        raise Fehler(400, 'termin-lang', f'ZU LANG · {nr}{feld} hat höchstens {hoechstens} Zeichen.')
    if re.search(r'[<>{}]', s):
        raise Fehler(400, 'termin-zeichen', f'ZEICHEN · {nr}{feld}: spitze und geschweifte Klammern stehen nicht auf dem Plakat.')
    return s


def pruefe_einen(t, i=0):
    """Ein DJ-Abend: Datum, Name, Zeile (darf leer sein), Plakat. Alles andere wird abgelehnt (keine fremden Felder auf die Website)."""
    if not isinstance(t, dict):
        raise Fehler(400, 'termin-falsch', 'DJ-ABEND · Ein Eintrag ist kein DJ-Abend.')
    nr = f'Abend {i + 1}: '
    tid = str(t.get('id') or '')
    if not re.fullmatch(r'[a-z0-9-]{1,24}', tid):
        raise Fehler(400, 'termin-falsch', 'DJ-ABEND · ' + nr + 'Kennung fehlt.')
    d = str(t.get('datum') or '')
    try:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d):
            raise ValueError
        datetime.date.fromisoformat(d)
    except ValueError:
        raise Fehler(400, 'termin-datum', 'DATUM · ' + nr + 'Das Datum fehlt oder gibt es nicht.')
    name = _text(t.get('name'), nr, 'Der Name', 60, False)
    zeile = _text(t.get('zeile'), nr, 'Die Zeile', 80, True)
    k = str(t.get('plakat') or '')
    if not re.fullmatch(r'p-[\w-]{1,30}', k) or not (BILD / f'{k}.json').is_file():
        raise Fehler(400, 'termin-plakat', 'PLAKAT · ' + nr + 'Bitte eines der Plakate der Bar wählen.')
    return {'id': tid, 'datum': d, 'name': name, 'zeile': zeile, 'plakat': k}


def pruefe(liste):
    if not isinstance(liste, list):
        raise Fehler(400, 'termin-falsch', 'DJ-ABENDE · Die Anfrage enthält keine Liste von Abenden.')
    if not liste:
        raise Fehler(400, 'termin-leer', 'LEER · Mindestens ein DJ-Abend bleibt auf der Seite: Plakatwand, Kontaktbogen und Flyer zeigen immer den neuesten.')
    if len(liste) > HOECHSTENS:
        raise Fehler(400, 'termin-viele', f'DJ-ABENDE · Höchstens {HOECHSTENS} Abende stehen gleichzeitig auf der Website.')
    aus = [pruefe_einen(t, i) for i, t in enumerate(liste)]
    if len({t['id'] for t in aus}) != len(aus):
        raise Fehler(400, 'termin-falsch', 'DJ-ABEND · Zwei Abende tragen dieselbe Kennung.')
    if len({t['datum'] for t in aus}) != len(aus):
        raise Fehler(400, 'termin-doppelt', 'DOPPELT · An einem Tag steht schon ein DJ-Abend.')
    return sorted(aus, key=lambda t: t['datum'], reverse=True)


def _leer():
    return {'entwurf': None, 'stand': None, 'verlauf': [], 'protokoll': []}


def lade():
    """Datei lesen; ist sie beschädigt, die letzte gute Fassung, nie still leer (Master 5.1)."""
    for p in (DATEI, DATEI.with_suffix('.json.gut')):
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding='utf-8'))
                if isinstance(d, dict) and 'verlauf' in d:
                    return d
            except ValueError:
                continue
    if DATEI.is_file():
        raise Fehler(500, 'termine-speicher', 'SPEICHER · Die Datei der DJ-Abende und ihre Sicherung sind beide unlesbar. Prüfung öffnen.')
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
    """Was die Ansicht braucht: Ursprung, Stand (veröffentlicht), Entwurf (falls einer wartet), Verlauf, Fingerabdruck, Plakate der Bar."""
    d = d or lade()
    u = ursprung()
    stand = d['stand'] if d['stand'] is not None else u
    entwurf = d['entwurf']
    return {'ursprung': u, 'stand': stand, 'entwurf': entwurf, 'wartet': entwurf is not None and entwurf != stand,
            'kennung': fingerabdruck(entwurf if entwurf is not None else stand),
            'zuletzt': next((v for v in reversed(d['verlauf']) if v.get('art') == 'veroeffentlicht'), None),
            'verlauf': [{'nr': i, 'zeit': v['zeit'], 'art': v['art'], 'notiz': v.get('notiz', ''), 'zahl': len(v['termine'])} for i, v in enumerate(d['verlauf'])][::-1],
            'plakate': plakate(),
            'quelle': 'website/bau.py › LINEUP'}


def wartend(l):
    """Wie viele Abende sich zwischen Stand und Entwurf unterscheiden (neu, geändert, entfällt), wie die Ansicht sie zählt."""
    if not l['wartet']:
        return 0
    alt, neu = {t['id']: t for t in l['stand']}, {t['id']: t for t in l['entwurf']}
    return sum(1 for k, t in neu.items() if alt.get(k) != t) + sum(1 for k in alt if k not in neu)


def _bewache(d, erwartet):
    l = lage(d)
    if erwartet != l['kennung']:
        raise Fehler(409, 'konflikt', 'KONFLIKT · In einem anderen Fenster wurden die DJ-Abende inzwischen geändert. Die Liste lädt neu, deine Eingaben bleiben stehen.')
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
        _protokoll(d, 'DJ-Abende im Entwurf gespeichert')
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
        d['verlauf'] = (d['verlauf'] + [{'zeit': jetzt(), 'art': 'veroeffentlicht', 'notiz': str(notiz or '')[:200], 'termine': d['stand']}])[-60:]
        _protokoll(d, 'DJ-Abende veröffentlicht')
        schreib(d)
        return lage(d)


def verwerfen(erwartet):
    with _SCHLOSS:
        d = lade()
        _bewache(d, erwartet)
        vorher = d['entwurf']
        d['entwurf'] = None
        _protokoll(d, 'Entwurf der DJ-Abende verworfen')
        schreib(d)
        return {'vorher': vorher, **lage(d)}


def zurueckholen(nr, erwartet):
    """Eine frühere Fassung (nr im Verlauf) oder den Ursprung («ursprung») in den Entwurf holen, nie direkt auf die Website (R14)."""
    with _SCHLOSS:
        d = lade()
        l = _bewache(d, erwartet)
        if nr == 'ursprung':
            t = l['ursprung']
        else:
            try:
                t = d['verlauf'][int(nr)]['termine']
            except (ValueError, IndexError, TypeError):
                raise Fehler(404, 'fassung-unbekannt', 'FASSUNG · Diese frühere Fassung gibt es nicht.')
        d['entwurf'] = None if t == l['stand'] else t
        _protokoll(d, 'Frühere Fassung der DJ-Abende in den Entwurf geholt')
        schreib(d)
        return lage(d)


# ------------------------------------------------------------------ Ausliefern: die drei Stellen der Website aus der Liste zeichnen
# Genau wie website/bau.py › img_tag(), flyer() und website/unter.py › kopf_plakate(), programm() (Kontaktbogen) sie bauen.
def _bild(k):
    d = json.loads((BILD / f'{k}.json').read_text(encoding='utf-8'))
    d['alt'] = _bau()['alt'].get(k, '')
    return d


_V = {'v': ''}   # Fassungsnummer der Bilder, wie die gebaute Seite sie trägt (die Seite kann älter sein als V in bau.py)


def _img(k, sizes, sofort=False, extra=''):
    d, v = _bild(k), _V['v'] or _bau()['v']
    srcset = ', '.join('assets/bild/%s?v=%s %dw' % (f, v, b) for b, f in d['stufen'])
    if sofort:
        return '<img src="assets/bild/%s?v=%s" srcset="%s" sizes="%s" alt="%s" fetchpriority="high" decoding="async" width="%d" height="%d"%s>' % (
            d['stufen'][-1][1], v, srcset, sizes, E(d['alt']), d['w'], d['h'], extra)
    return '<img data-srcset="%s" data-sizes="%s" alt="%s" decoding="async" width="%d" height="%d"%s>' % (srcset, sizes, E(d['alt']), d['w'], d['h'], extra)


def _lineup(liste):
    return [(_punkt(t['datum']), t['name'], t['zeile'], t['plakat']) for t in sorted(liste, key=lambda t: t['datum'], reverse=True)]


def _programm(roh, lineup):
    keys = list(dict.fromkeys(l[3] for l in lineup))
    wand = ''.join('<figure class="pw-f" style="--d:%d;--lq:url(%s)">%s</figure>' % (j, _bild(k)['lq'], _img(k, '(max-width:900px) 50vw, 25vw', True)) for j, k in enumerate(keys[:8]))
    plak = []
    for d, n, r, k in lineup:
        for p in plak:
            if p[0] == k:
                p[1].append((d, n, r))
                break
        else:
            plak.append((k, [(d, n, r)]))

    def p_datum(ab):
        return ' und '.join(d[:6] for d, n, r in ab[::-1])[:-1] + ab[0][0][5:] if len(ab) > 1 else ab[0][0]

    def p_name(ab):
        return ', '.join(n for d, n, r in ab[::-1])

    def sp(k, sizes, cls='', extra=''):
        return '<figure class="sp %s" style="--lq:url(%s)"%s>%s</figure>' % (cls, _bild(k)['lq'], extra, _img(k, sizes))
    gross = ''.join(sp(k, '(max-width:760px) 92vw, 40vw', 'kb-g' + (' an' if j == 0 else ''), ' data-k="%s"' % k) for j, (k, ab) in enumerate(plak))
    klein = ''.join('<div class="kb-k%s" data-k="%s" data-dat="%s" data-name="%s" style="--n:%d">%s<p>%s</p></div>' % (
        ' an' if j == 0 else '', k, E(p_datum(ab)), E(p_name(ab)), j, sp(k, '(max-width:760px) 22vw, 9vw'), E(p_datum(ab))) for j, (k, ab) in enumerate(plak))
    stellen = [(r'(<div class="pw-wand">)(.*?)(</div>\s*<div class="pw-band">)', wand),
               (r'(<div class="kb-bild">)(.*?)(</div><div class="kb-unten">)', gross),
               (r'(<p class="kb-name titel">)(.*?)(</p>)', E(p_name(plak[0][1]))),
               (r'(<p class="kb-dat">)(.*?)(</p>)', E(p_datum(plak[0][1]))),
               (r'(<div class="kb-bogen" data-kontaktbogen>)(.*?)(</div></div></div>\s*<div class="knoepfe)', klein)]
    return _setze(roh, stellen)


def _index(roh, lineup):
    d0, n0, r0, k0 = lineup[0]
    stellen = [(r'(<div class="flyer lu-flyer sw" id="flyer" style="--i:2">)(<figure class="foto".*?</figure>)(\s*<div class="fl-unten">)',
                '<figure class="foto" style="--lq:url(%s)">%s</figure>' % (_bild(k0)['lq'], _img(k0, '36vw', extra=' data-k="%s" class="an"' % k0))),
               (r'(<p class="fl-name">)(.*?)(</p>)', E(n0)),
               (r'(<p class="fl-datum">)(.*?)(</p>)', E(d0) + ((' · ' + E(r0)) if r0 else ''))]
    return _setze(roh, stellen)


def _setze(roh, stellen):
    for muster, neu in stellen:
        roh, n = re.subn(muster, lambda m: m.group(1) + neu + m.group(3), roh, count=1, flags=re.S)
        if not n:
            raise Fehler(503, 'termine-stelle', 'DJ-ABENDE · Die Seite hat die Stelle für die DJ-Abende nicht mehr; sie zeigt ihre gebauten Abende.')
    return roh


def fuelle(roh, seite, liste, u):
    """index.html oder programm.html mit einer Liste füllen. Gleich wie der Ursprung: unverändert zurück."""
    if liste == u or seite not in ('index.html', 'programm.html'):
        return roh
    lineup = _lineup(liste)
    m = re.search(r'assets/bild/[\w-]+\.webp\?v=(\w+)', roh)
    _V['v'] = m.group(1) if m else ''
    return _index(roh, lineup) if seite == 'index.html' else _programm(roh, lineup)


def ausliefern(roh, seite, welche='stand'):
    l = lage()
    liste = l['entwurf'] if welche == 'entwurf' and l['entwurf'] is not None else l['stand']
    return fuelle(roh, seite, liste, l['ursprung'])


def pruefung():
    """Punkte für die Prüfseite: Quelle lesbar, Stellen der Seiten da, Speicher lesbar, Sicherung da, Stand gültig."""
    p = []
    try:
        u = ursprung()
        p.append({'gut': True, 'titel': 'DJ-Abende der Website', 'text': f'{len(u)} Abende in website/bau.py › LINEUP gelesen, {len(plakate())} Plakate der Bar.'})
    except Fehler as e:
        return [{'gut': False, 'titel': 'DJ-Abende der Website', 'text': e.text, 'stichwort': e.stichwort}]
    try:
        probe = list(reversed(u))   # andere Reihenfolge der Plakate: jede Stelle muss sich füllen lassen
        probe = [dict(t, id=t['id'] + 'x') for t in probe]
        for s in ('index.html', 'programm.html'):
            fuelle((WEB / s).read_text(encoding='utf-8'), s, probe, u)
        p.append({'gut': True, 'titel': 'Stellen auf den Seiten', 'text': 'Plakatwand, Kontaktbogen und Flyer der Startseite lassen sich aus der Liste füllen.'})
    except (Fehler, OSError) as e:
        p.append({'gut': False, 'titel': 'Stellen auf den Seiten', 'text': getattr(e, 'text', str(e)), 'stichwort': 'termine-stelle'})
    try:
        d = lade()
        for k in ('stand', 'entwurf'):
            if d[k] is not None:
                pruefe(d[k])
        p.append({'gut': True, 'titel': 'Speicher der DJ-Abende', 'text': 'lesbar' + (', Sicherung der letzten guten Fassung liegt daneben' if DATEI.with_suffix('.json.gut').is_file() else ', noch nichts gespeichert') + '.'})
    except Fehler as e:
        p.append({'gut': False, 'titel': 'Speicher der DJ-Abende', 'text': e.text, 'stichwort': e.stichwort})
    return p
