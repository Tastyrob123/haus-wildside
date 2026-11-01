#!/usr/bin/env python3
"""Die Pairing-Karte · Walk on the Wild Side Hannover: liest die Karten der Bar aus Website und Kundenmaterial (31.10.2026, C26 in der Form des Hauses).
Vorlage: karten_lesen.py der Pairing-Karte im Culinarium (dort je Abend eine Menükarte).

Die Bar hat eine wechselnde Karte, deren Drinks Momo entwirft (Kundin 30.10.2026), dazu Klassiker, Sonderkarten zu Festen und die Preise für Feiern.
Nichts wird abgetippt, wo es schon als Text vorliegt: website/unter.py wird als Text gelesen (ast, nie importiert: der Import baut die Website) und
geschrieben nach _daten/quelle/<karte>.json:
  · drunk-in-love   Valentinskarte 14.02.2026 «Drunk in Love · Cupid’s Signature Drinks» (unter.py drinks() karte: Name, Zutaten, Preis vom Plakat)
  · dishes-in-love  die zweite Seite derselben Karte «Dishes in Love» mit Rudis Tellern zum Teilen. Steht nicht auf der Website; abgelesen vom
                    Beitrag der Bar vom 03.02.2026 (_quelle/ig/2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-3.jpg), Wortlaut unten in DISHES
  · klassiker       die Klassiker der Bar (unter.py drinks() klassiker: Name, erster Satz als Zutaten; ohne Preis, die Website nennt keinen)
  · preisliste      die Preise der Bar für Feiern aus der Angebotsmappe (unter.py PREISE, PAUSCHALE; Service und Raum, Budget aus tafel())
Zwei Prüfwege, bricht bei jeder Abweichung ab:
  1. Wort für Wort: jedes Wort der Daten steht in der Quelle (unter.py bzw. DISHES).
  2. Gegen die gebaute Website: Namen und Preise der Website-Karten stehen so in website/drinks.html bzw. website/tafel.html.

Dazu die Karte «Die Karte» (art abend, C08/C24 in der Form des Hauses: bis zu sechs Drinks mit Name und Zutaten, gültig ab, Preis je Drink):
solange das Haus die aktuelle Karte nicht eingetragen hat, steht dort beschriftet als Beispiel die jüngste überlieferte Drinkkarte (Drunk in Love,
Fehlerbuch 10a: Beispiele statt Leere, nie erfundene Echtdaten).

    python3 _werkzeuge/carte/karten_lesen.py         schreibt _daten/quelle/ und prüft
"""
import ast, html, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(os.path.dirname(os.path.dirname(HIER)), 'website')
QD = os.path.join(HIER, '_daten', 'quelle')
# Plätze der Karte «Die Karte» (satz.js ABEND.GAENGE): je Drink Name (dN) und Zutaten (dN_z)
GAENGE = [('d1', 'Drink 1'), ('d2', 'Drink 2'), ('d3', 'Drink 3'), ('d4', 'Drink 4'), ('d5', 'Drink 5'), ('d6', 'Drink 6')]

# Zweite Seite der Valentinskarte 2026, abgelesen vom Beitrag der Bar (Bild 3 von 3); auf der Karte in Versalien, hier in normaler Schreibung.
# Trennstrich «|» der Karte wird im Satz « · » wie auf der Website (drinks.html). «Bouef» der Karte als «Bœuf» (Schreibfehler der Vorlage).
DISHES_QUELLE = '_quelle/ig/2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-3.jpg (Beitrag der Bar vom 03.02.2026, Bild 3)'
DISHES = [
    ('Wild Side Temptation', [('Bergamotten Schaumwein', 'Auster | Granita', '15')]),
    ('Sharing Dishes for Love Birds & Friends', [
        ('Sauerteigbrot', 'Butter | Maldon', '6'),
        ('Kichererbsen Hummus', 'geräucherte Paprika | Oliven Öl', '8'),
        ('Stracciatella Creme', 'Dill Öl | dunkle Trauben | Basilikum Pesto', '8'),
        ('Rosa gegarte Entenbrust', 'Teriyaki Jus | Pak Choi', '12'),
        ('Bœuf Bourguignon', 'Kartoffel Mousseline | eingelegte Paprika | Schmand', '12'),
        ('Geschmorter Hokkaido', 'Süsskartoffel Honig | Kartoffel Mousseline | Wirsing', '11')]),
    ('The Sweet End', [('Dunkle Schokolade', 'Oliven Öl | Maldon', '8')]),
]


class Fehler(Exception):
    pass


def _zuweisung(baum, name, funktion=None):
    """Den Wert einer Zuweisung NAME = … als Baum holen (ohne die Datei auszuführen); mit funktion nur innerhalb dieser Funktion."""
    wo = baum
    if funktion:
        wo = next((k for k in baum.body if isinstance(k, ast.FunctionDef) and k.name == funktion), None)
        if wo is None:
            raise Fehler(f'Funktion {funktion}() steht nicht in website/unter.py')
    for k in ast.walk(wo):
        if isinstance(k, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in k.targets):
            return ast.literal_eval(k.value)
    raise Fehler(f'{name} steht nicht in website/unter.py' + (f' ({funktion})' if funktion else ''))


def quellen():
    p = os.path.join(PROJ, 'unter.py')
    text = open(p, encoding='utf-8').read()
    baum = ast.parse(text)
    return dict(text=text, karte=_zuweisung(baum, 'karte', 'drinks'), klassiker=_zuweisung(baum, 'klassiker', 'drinks'),
                preise=_zuweisung(baum, 'PREISE'), pauschale=_zuweisung(baum, 'PAUSCHALE'))


def erster_satz(t):
    """«Gin, Wermut, Bitter, auf Eis gerührt. Der Schriftzug …» → «Gin | Wermut | Bitter | auf Eis gerührt» (Trennung wie die Karten der Bar)."""
    s = re.split(r'[.:]\s', t.strip() + ' ', maxsplit=1)[0].strip().rstrip('.')
    return ' | '.join(x.strip() for x in re.split(r',\s*|\s+und\s+', s) if x.strip())


def karte(ziel, name, unter, gruppe, foto, titel, datum, mit, rubriken, quelle, hinweis='', ab='', kleid='', bilder=None):
    """kleid: '' (Creme der Bar), 'love' (Valentinsreihe im Charakter des Originals), 'feier' (Angebot für Feiern mit Fotos der Bar);
    bilder: Bilder aus satz/bild/ (bilder_satz.py): {'deko': …, 'held': …, 'rubrik': {Rubrik: [Bild je Eintrag]}}"""
    b = bilder or {}
    return dict(ziel=ziel, art='satz', key=ziel, name=name, unter=unter, gruppe=gruppe, ab=ab, plakat='', foto=foto, titel=titel, datum=datum, mit=mit,
                rubriken=[dict(titel=t, eintraege=[dict(name=n, zutaten=z, preis=p, bild=((b.get('rubrik') or {}).get(t) or [''] * len(e))[i])
                                                   for i, (n, z, p) in enumerate(e)]) for t, e in rubriken],
                hinweis=hinweis, quelle=quelle, kleid=kleid, deko=b.get('deko', ''), held=b.get('held', ''))


def lesen():
    q = quellen()
    aus = {}
    aus['drunk-in-love'] = karte('drunk-in-love', 'Drunk in Love', 'Valentinstag 2026', 'Weitere Karten', 'k30-coupe', 'Drunk in Love',
                                 'Valentinstag · 14. Februar 2026', 'Wild Side goes in love',
                                 [('Cupid’s Signature Drinks', [(n, z.replace(' · ', ' | '), p) for n, z, p in q['karte']])],
                                 'website/unter.py drinks() karte (vom Plakat der Valentinskarte, Beitrag der Bar vom 03.02.2026)', ab='2026-02-14',
                                 kleid='love', bilder={'deko': 'leopard.png'})
    aus['dishes-in-love'] = karte('dishes-in-love', 'Dishes in Love', 'Teller zum Teilen', 'Weitere Karten', 'k30-leopard', 'Dishes in Love',
                                  'Valentinstag · 14. Februar 2026', 'Kleine Dishes zum Teilen, mit Rudi', DISHES, DISHES_QUELLE, ab='2026-02-14',
                                  kleid='love', bilder={'deko': 'coupe.png'})
    aus['klassiker'] = karte('klassiker', 'Die Klassiker', 'An jedem Abend', 'Weitere Karten', 'negroni', 'Die Klassiker', 'Auch ohne Frage',
                             'Ein paar Drinks gehören fest zum Haus.', [('Die Klassiker', [(n, erster_satz(s), '') for n, s in q['klassiker']])],
                             'website/unter.py drinks() klassiker (Seite drinks.html «Die Klassiker»), ohne Preise: die Website nennt keine')
    pausch = [(k + ' · ' + t, z, p + ',00') for k, t, z, p in q['pauschale']]
    aus['preisliste'] = karte('preisliste', 'Die Preise der Bar', 'Für Feiern und Gesellschaften', 'Weitere Karten', 'flaschen', 'Die Preise der Bar',
                              'Für Feiern im Wild Side', 'Für die lange Tafel und die ganze Bar',
                              [('Pauschale pro Person', pausch),
                               ('Was ein Drink kostet', [(t, '', p) for t, p in q['preise']]),
                               ('Budget', [('Service und Raum', '', '500,00'), ('Euer Budget für Drinks', 'Lässt sich nach oben frei anpassen', 'ab 1.000,00')])],
                              'website/unter.py PREISE, PAUSCHALE und tafel() (Angebotsmappe der Bar, _quelle/angebote-pdf/Wild Side Angebote.pdf)',
                              hinweis='Pauschale und Budget: geschlossene Gesellschaft ab 30 Gästen, 19 bis 2 Uhr, ab 2 Uhr jede angefangene Stunde 10 Euro pro Person. '
                                      'Alle Preise in Euro, brutto. Anzahlung 30 % eine Woche vorher, Rest vor Beginn.',
                              kleid='feier', bilder={'held': 'an-campari.webp', 'rubrik': {'Pauschale pro Person': ['an-sours.webp', 'an-glaeser.webp', 'an-negroni.webp']}})
    pruefe(aus, q)
    return aus


def naechster(aus):
    """Karte «Die Karte»: Beispiel aus der jüngsten überlieferten Drinkkarte (Drunk in Love), jedes Feld wörtlich von dort."""
    b = aus['drunk-in-love']
    e = b['rubriken'][0]['eintraege']
    tag = dict(zu=False, hinweis='')
    for i, (s, _) in enumerate(GAENGE):
        tag[s], tag[s + '_z'] = (e[i]['name'], e[i]['zutaten']) if i < len(e) else ('', '')
    preise = sorted(set(x['preis'] for x in e))
    return dict(ziel='abend', art='abend', name='Die Karte', unter='Drinks von Momo', gruppe='Die Karte',
                quelle='Beispiel aus drunk-in-love (%s)' % b['quelle'], beispiel_aus='drunk-in-love',
                abend=dict(ab=b['ab'], titel='Die Karte', motto=b['titel'], mit='Cupid’s Signature Drinks', preis=(preise[0] + ',00 EUR') if len(preise) == 1 else '',
                           zusatz='', hinweis='', fuss='', tage=[tag], beispiel=True))


WORT = re.compile(r'[0-9A-Za-zÄÖÜäöüßœéèêàâçÉÈÀ]+')


def pruefe(aus, q):
    """1. Wort für Wort gegen unter.py (Dishes gegen DISHES), 2. Namen und Preise gegen die gebaute Website."""
    quelle = set(w.lower() for w in WORT.findall(q['text']))
    dishes = set(w.lower() for t, e in DISHES for x in e for w in WORT.findall(' '.join((t,) + x)))
    try:
        drinks = html.unescape(open(os.path.join(PROJ, 'drinks.html'), encoding='utf-8').read())
        tafel = html.unescape(open(os.path.join(PROJ, 'tafel.html'), encoding='utf-8').read())
    except OSError:
        raise Fehler('website/drinks.html oder tafel.html fehlt (Website erst bauen)')
    fehl = []
    for z, d in aus.items():
        q_w = dishes if z == 'dishes-in-love' else quelle
        for r in d['rubriken']:
            for x in r['eintraege']:
                for t in (x['name'], x['zutaten'], x['preis']):
                    for w in WORT.findall(t):
                        if w.lower() not in q_w and not (z == 'preisliste' and w in ('000', '1')):
                            fehl.append(f'{z}: Wort «{w}» nicht in der Quelle')
        if z == 'klassiker':
            for x in d['rubriken'][0]['eintraege']:
                if x['name'] not in drinks:
                    fehl.append(f'{z}: «{x["name"]}» steht nicht in website/drinks.html')
        if z == 'preisliste':
            for x in d['rubriken'][1]['eintraege']:
                if f'{x["name"]}' not in tafel or f'{x["preis"]} €' not in tafel:
                    fehl.append(f'{z}: «{x["name"]} {x["preis"]}» steht nicht in website/tafel.html')
            for x in d['rubriken'][0]['eintraege']:
                if x['preis'].split(',')[0] + ' €' not in tafel:
                    fehl.append(f'{z}: Pauschale {x["preis"]} steht nicht in website/tafel.html')
            for b in ('500 €', 'ab 1.000 €'):
                if b not in tafel:
                    fehl.append(f'{z}: «{b}» steht nicht in website/tafel.html')
    if fehl:
        raise Fehler('Prüfung gegen die Quelle: ' + '; '.join(fehl[:12]))
    return True


def _schreib(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    t = p + '.neu'
    with open(t, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    json.load(open(t, encoding='utf-8'))
    os.replace(t, p)


if __name__ == '__main__':
    try:
        aus = lesen()
    except Fehler as e:
        sys.exit('ABBRUCH · ' + str(e))
    aus['abend'] = naechster(aus)
    for f in os.listdir(QD):
        if f.endswith('.json') and f[:-5] not in aus and f != 'pruefung.json':
            os.remove(os.path.join(QD, f))
    bericht = {}
    for z, d in aus.items():
        _schreib(os.path.join(QD, z + '.json'), d)
        n = sum(len(r['eintraege']) for r in d.get('rubriken', [])) if d['art'] == 'satz' else sum(1 for s, _ in GAENGE if d['abend']['tage'][0][s])
        bericht[z] = dict(name=d['name'], eintraege=n, preise=sum(1 for r in d.get('rubriken', []) for x in r['eintraege'] if x['preis']))
        print(f'{z}: {d["name"]} · {n} Einträge')
    _schreib(os.path.join(QD, 'pruefung.json'), dict(geprueft='Wort für Wort gegen website/unter.py (Dishes in Love gegen den Beitrag vom 03.02.2026), '
                                                  'Klassiker gegen website/drinks.html, Preise gegen website/tafel.html', karten=bericht))
    print('Prüfung: gleich')
