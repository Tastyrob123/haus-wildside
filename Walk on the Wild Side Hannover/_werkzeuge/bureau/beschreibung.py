#!/usr/bin/env python3
"""Beschreibung von Walk on the Wild Side für den Schreibtisch des Stamms (Das Schaufenster · Website pflegen), Nachtbau 31.10.2026.
Vorlage: dieselbe Datei des Culinarium (28.10.2026), Hauswerte getauscht.
   python3 _werkzeuge/bureau/beschreibung.py          schreibt beide Dateien neu und legt die Probe-Kopie an, falls sie fehlt
   python3 _werkzeuge/bureau/beschreibung.py --pruef  zeigt nur, was geschrieben würde
Der Server des Schaufensters (serve.py) ruft anlegen() beim Start selbst auf; die beiden Dateien entstehen so auch auf einem frischen Rechner.

Schreibt (Muster Schäfli 21.10.2026, Master Werkzeug-Bau 4.2 L17/L18):
  ~/Desktop/Website-Projekte/_Werkzeuge/haeuser/wildside/haus.json                 Kennung, Name, Welt, Quelle
  ~/Desktop/Website-Projekte/_Werkzeuge/werkzeuge/website/haeuser/wildside.json    Seiten, Bereiche, Angaben, Gastschichten
Nichts wird abgetippt: Seiten aus der Leiste der gebauten Website, Telefon, Adresse und Instagram aus dem Fuss von index.html.
Die Website selbst (website/) wird nur gelesen."""
import json
import re
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
PROJEKT = HIER.parent.parent
WEB = PROJEKT / 'website'
STAMM = Path.home() / 'Desktop/Website-Projekte/_Werkzeuge'
HAUS = 'wildside'
FOTO_SEITE = {'impressum.html': 'negroni', 'datenschutz.html': 'rueckbar'}   # Seiten ohne eigenes Foto: Bild für Google-Texte und Listen (Fotos der Website)
# Zeiten und Preise: Muster des Stamms (api.py › ZAHL) mit «EUR» und «€», wie die Website Preise schreibt
ZAHL_EUR = (r'(CHF|Fr\.|€|\bEUR\b|\bUhr\b|\d+\s?(Minuten|Min\.|m²|m2|Personen|Pers\.|Gäste|Nächte?|Nacht|Plätze|Gänge|Drinks|km)'
            r'|\d{1,2}[.:]\d{2}\s?(?:[–-]|bis)\s?\d{1,2}[.:]\d{2}|\d{1,2}[.:]\d{2}\s?Uhr|\b\d{1,2} bis \d{1,2} Uhr)')


def lies(name):
    return (WEB / name).read_text(encoding='utf-8')


def seiten():
    """Jede Seite, die die Leiste der Website nennt, dazu Impressum und Datenschutz aus dem Fuss. Wahl- und Konzeptseiten
    (auftakt-wahl.html, konzept.html) stehen nicht in der Leiste und gehören nicht dazu."""
    start = lies('index.html')
    leiste = re.search(r'<div class="leiste" id="leiste">.*?</nav>', start, re.S).group(0)
    namen = ['index.html'] + [d for d in re.findall(r'href="([a-z-]+\.html)"', leiste) if d != 'index.html']
    namen += [d for d in re.findall(r'href="((?:impressum|datenschutz)\.html)"', start) if d not in namen]
    for d in namen:
        if not (WEB / d).is_file():
            sys.exit(f'{d} steht in der Leiste, liegt aber nicht in website/.')
    return list(dict.fromkeys(namen))


def angaben():
    h = lies('index.html')
    besuch = re.search(r'<div class="besuch">.*?</div>', h, re.S)
    b = besuch.group(0) if besuch else ''
    tel = re.search(r'href="tel:(\+\d+)">([^<]+)</a>', b)
    ort = re.search(r'<p>([^<]+)<br>([^<]+)<br>', b)
    ig = re.findall(r'href="(https://www\.instagram\.com/[^"/]+/)"', b)
    if not (tel and ort and ig):
        sys.exit('Telefon, Adresse oder Instagram stehen nicht mehr im Fuss von index.html: Beschreibung nicht geschrieben.')
    q = 'website/index.html (gebaut aus website/bau.py › HAUS, fuss())'
    aus = [{'key': 'telefon', 'label': 'Telefon der Bar', 'art': 'telefon', 'wert': tel.group(2).strip(), 'link': 'tel:' + tel.group(1), 'quelle': q},
           {'key': 'strasse', 'label': 'Strasse', 'art': 'text', 'wert': ort.group(1).strip(), 'quelle': q},
           {'key': 'ort', 'label': 'PLZ und Ort', 'art': 'text', 'wert': ort.group(2).strip(), 'quelle': q}]
    for u in dict.fromkeys(ig):
        k = u.rstrip('/').rsplit('/', 1)[1]
        aus.append({'key': 'ig-' + re.sub(r'[^a-z]', '', k)[:20], 'label': 'Instagram der Bar', 'art': 'link', 'wert': u, 'quelle': q})
    return aus


def beschreibung():
    s = seiten()
    rechts = [d for d in s if d in ('impressum.html', 'datenschutz.html')]
    website = [
        ('start', 'Startseite', 'Der erste Eindruck: die Ecke bei Nacht, wer die Bar führt, was Momo mixt, die Decke, die DJ-Abende, die lange Tafel und die Nachbarn im Haus.', ['index.html'], 'schild'),
        ('drinks', 'Drinks', 'Was magst du? Das Gespräch an der Bar, wie Momo arbeitet, die Klassiker und die Sonderkarte «Drunk in Love».', ['drinks.html'], 'momo-giesst'),
        ('programm', 'Programm', 'Die Woche, Gastschichten, die Feste und die Bar unterwegs. Die DJ-Abende hast du in einer eigenen Ansicht.', ['programm.html'], 'konzert'),
        ('feiern', 'Feiern', 'Private Dinner, die lange Tafel, die ganze Bar mit Pauschalen und Preisliste, Musik und grosse Events, mit Anfrage.', ['tafel.html'], 'an-empore-tafel'),
        ('haus', 'Das Haus', 'Der Raum unter der Decke, Derya und Momo, was bisher geschah und die Auszeichnungen.', ['haus.html'], 'decke-raum'),
        ('besuch', 'Besuch', 'Wann die Bar offen hat, wo sie steht, Reservieren und die Fragen der Gäste.', ['besuch.html'], 'fenster'),
        ('recht', 'Rechtliches', 'Impressum und Datenschutz im Wortlaut des Hauses.', rechts, 'negroni'),
    ]
    fehlt = set(s) - {d for w in website for d in w[3]}
    if fehlt:
        sys.exit('Seiten ohne Bereich: ' + ', '.join(sorted(fehlt)))
    return {
        '_lies_mich': 'Beschreibung des Hauses für das Werkzeug «website» (Das Schaufenster · Website pflegen). Walk on the Wild Side Hannover: '
                      'Nachbarschafts-Mixology-Bar in Linden-Mitte, nur Deutsch. Jeder Text, jede Zahl, jedes Foto wird aus den gebauten Seiten gelesen '
                      '(website/ des Projekts). Läuft im Rahmen des Hauses: http://127.0.0.1:9082/_werkzeuge/bureau/ (Walk on the Wild Side Hannover/_werkzeuge/bureau/). '
                      'Geschrieben von _werkzeuge/bureau/beschreibung.py, nie von Hand ändern.',
        'seiten': [dict({'datei': d}, **({'foto': FOTO_SEITE[d]} if d in FOTO_SEITE else {})) for d in s],
        'sprachen': [],
        'kopie': {'unter': 'website', 'ordner': ['assets']},
        'gesperrt': [],
        # DJ-Abende: eigene Ansicht (die Plakate der Plakatwand, der Kontaktbogen und der Flyer der Startseite entstehen aus der Liste der Abende)
        'auslassen': ['.pw-wand', '.kb-gross', '.kb-bogen', '#flyer', '.wo-tafel', '.vk-rueck', '.vi-spiegel'],
        'vorschau': {'ohne_skripte': [], 'zusatz_css': '.fenster{overflow:clip}@media (hover:none){[data-ws-e],img[data-ws-b]{cursor:pointer}}'},
        'bereiche': {
            **{k: {'an': False} for k in ('zimmer', 'preisstufen', 'packages', 'saele', 'unterlagen', 'stellen')},
            'gaeste': {
                'name': 'Gastschichten',
                'satz': 'Wer neben Momo hinterm Tresen stand, mit Datum, Name, Satz und Foto, so wie es auf der Seite «Programm» steht. Was nicht mehr gezeigt werden soll, blendest du aus.',
                'quellen': [{'seite': 'programm.html', 'jedes': '.vk-reihe article.vk-p', 'felder': [
                    {'key': 'name', 'label': 'Gast', 'art': 'text', 'wo': '.vk-satz h3', 'titel': True},
                    {'key': 'datum', 'label': 'Datum', 'art': 'text', 'wo': '.vk-satz .etikett'},
                    {'key': 'satz', 'label': 'Satz zum Gast', 'art': 'text', 'wo': '.vk-satz p'},
                    {'key': 'bild', 'label': 'Foto', 'art': 'bild', 'wo': '.vk-bild img', 'kann_fehlen': True}]}]},
        },
        'zahlen': {'muster': ZAHL_EUR},
        'kleid': {'foto': 'schild-ecke'},
        'website': [{'key': k, 'name': n, 'satz': t, 'seiten': sei, 'foto': f} for k, n, t, sei, f in website],
        'angaben': angaben(),
        'google': {'an': True},
        'hochladen': {'an': True, 'ordner': 'assets/bild'},
        'funktionen': ['leiste_klar', 'team_wer'],
        'anleitung': '/_werkzeuge/bureau/anleitung.html',
    }


def haus():
    try:
        welt = json.loads((PROJEKT / '_kette/05-markenbauer/marke.json').read_text(encoding='utf-8')).get('welt') or 'grand'
    except (OSError, ValueError):
        welt = 'grand'
    return {'kennung': HAUS, 'name': 'Wild Side', 'welt': welt, 'quelle': '~/Desktop/Website-Projekte/Walk on the Wild Side Hannover',
            'hinweis': 'Walk on the Wild Side, Nachbarschafts-Mixology-Bar in Hannover-Linden. Nur Deutsch. '
                       'Angelegt 31.10.2026 vom Bau-Agenten Schaufenster mit _werkzeuge/bureau/beschreibung.py. Die Quelle wird nur gelesen, nie beschrieben.'}


def schreib(p, d):
    neu = json.dumps(d, ensure_ascii=False, indent=1) + '\n'
    if p.is_file() and p.read_text(encoding='utf-8') == neu:
        return f'{p.name}: unverändert'
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix('.tmp')
    tmp.write_text(neu, encoding='utf-8')
    tmp.replace(p)
    return f'{p.name}: geschrieben'


def anlegen():
    """Beide Dateien schreiben (nur wenn anders) und die Probe-Kopie anlegen, falls sie fehlt."""
    b, h = beschreibung(), haus()
    aus = [schreib(STAMM / 'haeuser' / HAUS / 'haus.json', h), schreib(STAMM / 'werkzeuge/website/haeuser' / f'{HAUS}.json', b)]
    aus.append(subprocess.run([sys.executable, str(STAMM / 'werkzeuge/website/probe.py'), HAUS], capture_output=True, text=True).stdout.strip())
    return aus


if __name__ == '__main__':
    if '--pruef' in sys.argv:
        print(json.dumps({'haus': haus(), 'beschreibung': beschreibung()}, ensure_ascii=False, indent=1))
        sys.exit()
    print('\n'.join(anlegen()))
