#!/usr/bin/env python3
"""Die Pairing-Karte · Walk on the Wild Side Hannover — setzt die Karten der Bar neu, im Kleid des Hauses (31.10.2026, Vorlage: satz_bau.py der
Pairing-Karte im Culinarium, dort aus der Tafel im Schäfli).

Grundlage ist die Machart der Bar (Fehlerbuch 10a: das Original ist die Grundlage, nie schwächer): die Valentinskarte «Drunk in Love» (Beitrag der
Bar vom 03.02.2026) hat oben den Titel, darunter eine Rubrik und Drink für Drink den Namen mit dem Preis rechts und die Zutaten klein in Versalien.
Verfeinert in den Farben und Schriften der Website (CHARAKTER.md Abschnitt 4, website/assets/wild.css): Creme wie die weissen Plakate der Bar, Nacht,
Gold nur als Haarlinie, Rot nur als Punkt (die Wortmarke); die Wortmarke als nachgezogener Vektor (oberflaeche/kleid/wildside-marke.svg #wm, unverändert);
Titel und Namen in Prata (eine Stärke, nie fett, nie kursiv), Zutaten und Etiketten in Hanken Grotesk, Preise mit Ziffern gleicher Breite.

Nichts ist abgetippt: jede Rubrik, jeder Name, jede Zutat, jeder Preis kommt aus _daten/quelle/<karte>.json (karten_lesen.py, gegen die Quelle
geprüft). Typografisch anders als das Original (der Wortlaut bleibt): Trennstrich «|» der Karten als « · » wie auf der Website (drinks.html).
Gesperrte Versalien höchstens .08em (pdftotext, Abschnitt 9).

Aus dem Satz liest einlesen.py die Karte als Baum; satz/satz.js setzt daraus Zeichen für Zeichen dasselbe HTML (Vorschau, PDF, Werkbank).
Die Karte «Die Karte» (wechselnd, Drinks von Momo) setzt satz.js selbst (Teil ABEND) mit denselben Klassen.

    python3 _werkzeuge/carte/satz_bau.py          setzt alle Karten nach satz/u-<karte>.html, die Zeichen nach satz/zeichen.json
"""
import html, json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
HAUS = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(HAUS, 'website')
QD = os.path.join(HIER, '_daten', 'quelle')
SATZ = os.path.join(HIER, 'satz')
KLEID = os.path.join(HIER, '..', 'oberflaeche', 'kleid')
e = lambda t: html.escape(t, quote=False)

# Hausangaben aus der Website (website/bau.py HAUS: Adresse, Ort); als Text gelesen, nie importiert
NAME = 'Walk on the Wild Side'
_bau = open(os.path.join(WEB, 'bau.py'), encoding='utf-8').read()
_adr = re.search(r"'adresse': '([^']+)'", _bau).group(1)
_ort = re.search(r"'ort': '([^']+)'", _bau).group(1)
FUSS = f'{NAME} · {_adr} · {_ort}'


def wortmarke():
    """Die Wortmarke WALK / ON THE / WILD SIDE als eigenes svg aus wildside-marke.svg #wm (unverändert, nur als Ganzes eingesetzt)."""
    s = open(os.path.join(KLEID, 'wildside-marke.svg'), encoding='utf-8').read()
    m = re.search(r'<symbol id="wm" viewBox="([^"]+)">(.*?)</symbol>', s, re.S)
    innen = re.sub(r'\s+', ' ', m.group(2).strip())
    return f'<svg class="ws-wm" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="{m.group(1)}" fill="currentColor">{innen}</svg>'


WM = wortmarke()


def q(kid):
    return json.load(open(os.path.join(QD, kid + '.json'), encoding='utf-8'))


def zeile(t):
    """Zutaten: Trennstrich der Karten « | » als « · » wie auf der Website; der Wortlaut bleibt."""
    return re.sub(r'\s*\|\s*', ' · ', t.strip())


# ---------------------------------------------------------------- Bausteine (dieselben Klassen setzt satz.js für «Die Karte»)
def eintrag(x):
    innen = f'<img class="sb-mb" src="bild/{x["bild"]}" alt="">' if x.get('bild') else ''
    innen += f'<p class="sb-n">{e(x["name"])}</p>'
    if x['preis']:
        innen += f'<p class="sb-mp">{e(x["preis"])}</p>'
    if x['zutaten']:
        innen += f'<p class="sb-dr">{e(zeile(x["zutaten"]))}</p>'
    return f'<div class="sb-m">{innen}</div>'


def rubrik(r, i=0):
    bild = ' sb-r--bild' if any(x.get('bild') for x in r['eintraege']) else ''
    return f'<section class="sb-r sb-r{i}{bild}"><p class="sb-h">{e(r["titel"])}</p>' + ''.join(eintrag(x) for x in r['eintraege']) + '</section>'


def band(d):
    """Titel der Karte. Valentinsreihe wie das Original: alles bis aufs letzte Wort als kräftige Display-Schrift («DRUNK IN»), das letzte Wort
    in Pinselschrift («LOVE»); der Wortlaut bleibt."""
    t = d['titel']
    if d.get('kleid') == 'love' and ' ' in t:
        vorn, letzt = t.rsplit(' ', 1)
        return f'<h2 class="sb-band"><span class="sb-b1">{e(vorn)}</span> <span class="sb-b2">{e(letzt)}</span></h2>'
    return f'<h2 class="sb-band">{e(t)}</h2>'


def oben(d):
    return (f'<div class="sb-oben"><span class="uz sb-zeichen">{WM}</span>'
            f'{band(d)}<p class="sb-datum">{e(d["datum"])}</p>'
            + (f'<p class="sb-mit">{e(d["mit"])}</p>' if d.get('mit') else '') + '</div>')


def unten(d):
    return f'<div class="sb-unten"><p class="sb-hinweis">{e(d["hinweis"])}</p></div>' if d.get('hinweis') else ''


def blatt(inhalt, mx='1.6', d=None):
    """Ein Blatt A4 hoch. kleid 'love': rosa Grund, die Zeichnung der Bar (deko) unten rechts; 'nacht': Nacht mit Foto der Bar oben (held);
    'feier': wie 'nacht', dazu Pauschalen als Spalten, Preise zweispaltig, Budget als Felder."""
    d = d or {}
    kl = {'love': ' ws-love', 'feier': ' ws-nacht ws-feier', 'nacht': ' ws-nacht'}.get(d.get('kleid', ''), '')
    held = f'<figure class="sb-held"><img src="bild/{d["held"]}" alt=""></figure>' if d.get('held') else ''
    deko = f'<img class="sb-deko" src="bild/{d["deko"]}" alt="">' if d.get('deko') else ''
    return (f'<section data-max="{mx}" class="blatt ws{kl}" data-b="210" data-h="297" style="width:210mm;height:297mm">'
            f'{held}<div class="inhalt">{inhalt}</div>{deko}<footer class="ufuss2">{e(FUSS)}</footer></section>')


def doc(titel, seiten):
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8"><title>{e(titel)} · {e(NAME)}</title>\n'
            f'<link rel="stylesheet" href="satz.css"><style>@page{{size:210mm 297mm;margin:0}}</style></head><body>' + ''.join(seiten) + '</body></html>')


def barkarte(kid):
    d = q(kid)
    menue = '<div class="sb-menue">' + ''.join(rubrik(r, i) for i, r in enumerate(d['rubriken'])) + '</div>'
    return doc(d['name'], [blatt(f'<div class="sb-quer">{oben(d)}{menue}{unten(d)}</div>', d=d)])


def zeichen():
    """Feste Teile für das Blatt «Die Karte» (satz.js ABEND): Wortmarke, Fusszeile."""
    return dict(ZEICHEN=WM, BLATT='<i></i>', FUSS=FUSS, HAUS=NAME, WORTMARKE=WM)


def _schreib(p, t):
    with open(p + '.neu', 'w', encoding='utf-8') as f:
        f.write(t)
    os.replace(p + '.neu', p)


if __name__ == '__main__':
    os.makedirs(SATZ, exist_ok=True)
    for f in os.listdir(SATZ):
        if f.startswith('u-') and f.endswith('.html'):
            os.remove(os.path.join(SATZ, f))
    for f in sorted(os.listdir(QD)):
        kid = f[:-5]
        if not f.endswith('.json') or kid in ('abend', 'pruefung'):
            continue
        _schreib(os.path.join(SATZ, f'u-{kid}.html'), barkarte(kid))
        print('gesetzt:', f'satz/u-{kid}.html')
    with open(os.path.join(SATZ, 'zeichen.json'), 'w', encoding='utf-8') as f:
        json.dump(zeichen(), f, ensure_ascii=False)
    print('Zeichen: satz/zeichen.json')
