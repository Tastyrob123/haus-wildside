"""Walk on the Wild Side Hannover: Inhalt der Werkbank («Alles auf einen Blick») und ihrer Beigaben.   Werkzeug: ~/Desktop/Website-Projekte/_Werkbank-Kit/

Werkbank-Chat Wild Side, Nachtbau 31.10.2026 (Auftrag Oberchef; Roberts Deal: «kopieren, umkleiden, Hauswerte eintragen, nichts neu erfinden»).
Vorlage: die Werkbank des Culinarium Hannover (28.–30.10.2026, dort über die Taverne zum Schäfli), Aufbau, Wege und Funktionen unverändert.
Kleid der Bar (CHARAKTER.md 4, _werkzeuge/AUFTRAG-GEMEINSAM.md «Kleid»): Nacht #130E0D, Platte #1C1513/#261E1A, Creme #F2E9DC der weissen Plakate,
Gold #D8B264 nur als Haarlinie, Etikett, Knauf; Rot #F0323F nur als Punkt; Prata für Titel (eine Stärke, nie fett, nie kursiv), Hanken Grotesk zum Lesen
und für gesperrte Etiketten; die echte Wortmarke (WALK / ON THE / WILD SIDE, nachgezogen) als einziges Zeichen. Fakten nur aus der Website
(website/bau.py HAUS und LINEUP, ihre Seiten), CHARAKTER.md und _quelle/, nichts abgetippt, nichts erfunden.

Eigenes Revier: website/_werkbank/ ist der Projektordner des Kits (ROOT), die Website liegt eine Ebene höher (WEB) und wird nur gelesen;
assets/ ist ein Verweis auf website/assets (nur gelesen). Serviert von website/_werkbank/serve.py auf Port 9088 (zuerst das Revier, sonst die Website).
Ton: die Bar duzt (Website, Instagram): der Brief sagt «Hallo Derya», sonst «ihr/euch» an Derya und Momo. Deutsche Schreibung mit ß.
Kein Preis für Roberts Arbeit in der Werkbank. Eine E-Mail-Adresse der Bar ist nicht belegt: keine erfunden, Kontakt über Telefon, Instagram, Formular."""
import json
import os
import re as _re
import shutil
import sys
import glob as _glob
import hilfen as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # = website/_werkbank (Projektordner des Kits)
WEB = os.path.dirname(ROOT)                                          # = website/ (nur gelesen)
PROJ = os.path.dirname(WEB)
KLEID = os.path.join(PROJ, '_werkzeuge', 'oberflaeche', 'kleid')


def bild(key, hoechstens=2400):
    """Grösste Fassung eines Fotos der Website bis «hoechstens» Pixel Breite (assets/bild/<key>-<breite>.webp) als voller Pfad für K.hausbild."""
    b = sorted(int(m.group(1)) for p in _glob.glob(os.path.join(WEB, 'assets', 'bild', key + '-*.webp')) if (m := _re.fullmatch(_re.escape(key) + r'-(\d+)\.webp', os.path.basename(p))) and int(m.group(1)) <= hoechstens)
    if not b:
        raise FileNotFoundError(f'Bild {key} fehlt in website/assets/bild')
    return os.path.join(WEB, 'assets', 'bild', f'{key}-{b[-1]}.webp')


NAME = 'Walk on the Wild Side'
KURZ = 'wildside'
LEISTE = ''          # die Wortmarke steht in der Leiste schon als Zeichen (keine doppelten Logos, Kriterium 14)
HAUSART = 'restaurant'
PORT = 9088
DOMAIN = 'Instagram'   # die Bar hat heute keine Website (wildside-hannover.de war nie eine, CHARAKTER.md 9); «heute» ist das Profil auf Instagram
HEUTE_URL = 'https://www.instagram.com/walkonthewildside_hannover/'
ANREDE = 'Hallo Derya, hallo Momo'
RECHTE = 'dem Walk on the Wild Side und den jeweiligen Fotografen.'
START_MS = 4200
WAHL = 'body > section, body > header'
ADRESSE = 'Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover'

# ---------- Farben: die der Website (website/assets/wild.css :root) ----------
# Nacht, Platte, Creme der weissen Plakate, Gold als Haarlinie und Etikett, Rot als Punkt. «gold» ist das Gold des Eckschilds, «punkt»/«rot» das Rot der Wortmarke.
FARBEN = dict(nacht='#130e0d', tief='#1c1513', navy='#261e1a', blau='#33281f', papier='#f2e9dc', creme='#e7dccb', weiss='#f7f1e7',
              gold='#d8b264', messing='#b08a43', taupe='#6e5d4e', tinte='#1b1512', punkt='#f0323f', rot='#f0323f')
_SCHRIFT = os.path.join(WEB, 'assets', 'schrift')
SCHRIFT = dict(titel=('Prata', 'prata.woff2'), titel_folge="Georgia,serif", ersatz="local('Georgia')", druckgewicht=400)
SCHRIFT_MEHR = []
DRUCKQUELLEN = []   # Prata und Hanken setzt _werkbank/druckschrift.py fest
DRUCKSCHRIFT = [('Prata', 400, 'Prata-Regular.ttf'), ('Prata', 500, 'Prata-Regular.ttf'), ('Prata', 700, 'Prata-Regular.ttf')]
# Die Webschriften der Website unter den Namen, die der Kit erwartet (er sucht sie in werkbank/fonts; die Website legt sie unter assets/schrift ab).
# Der Kit kennt nur die Familien «Instrument Sans» und «DM Mono»: beide zeigen hier auf Hanken Grotesk (kleid_wild.py benennt sie danach um).
_WF = os.path.join(ROOT, 'werkbank', 'fonts')
os.makedirs(_WF, exist_ok=True)
for _q, _z in (('prata-latin.woff2', 'prata.woff2'), ('hanken-latin.woff2', 'hanken.woff2'), ('hanken-latin.woff2', 'InstrumentSans-normal-400_600.woff2'), ('hanken-latin.woff2', 'DMMono-normal-400.woff2')):
    if os.path.exists(os.path.join(_SCHRIFT, _q)):
        shutil.copy2(os.path.join(_SCHRIFT, _q), os.path.join(_WF, _z))
# Muster: das Ornament der Website (assets/bild/haus-tapete.svg, Gold-Haarlinien), als eigene Kachel für dunkle und helle Flächen (werkbank/eigen/tapete-*.svg)
_EI = os.path.join(ROOT, 'werkbank', 'eigen')
os.makedirs(_EI, exist_ok=True)
_TP = open(os.path.join(WEB, 'assets', 'bild', 'haus-tapete.svg'), encoding='utf-8').read()
open(os.path.join(_EI, 'tapete-dunkel.svg'), 'w', encoding='utf-8').write(_TP.replace('opacity=".55"', 'opacity=".16"'))
open(os.path.join(_EI, 'tapete-hell.svg'), 'w', encoding='utf-8').write(_TP.replace('stroke="#D8B264"', 'stroke="#B08A43"').replace('opacity=".55"', 'opacity=".22"'))
MUSTER = 'url(/werkbank/eigen/tapete-dunkel.svg)'
MUSTER_B = '150px'
MUSTER_DRUCK = '12mm'
# Das Zeichen: die echte Wortmarke der Bar (drei Zeilen WALK / ON THE / WILD SIDE, nachgezogen) aus dem Kleid, unverändert übernommen, nie nachgezeichnet.
_ZC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen', 'zeichen-ws.svg')
os.makedirs(os.path.dirname(_ZC), exist_ok=True)
open(_ZC, 'w', encoding='utf-8').write(open(os.path.join(KLEID, 'wildside-zeichen.svg'), encoding='utf-8').read())
ZEICHEN = K.svg_innen(_ZC)
ZEICHEN = (ZEICHEN[0], ZEICHEN[1].replace(' fill="#000"', ''))   # Farbe über currentColor


def _wortmarke():
    """Die Wortmarke aus _werkzeuge/oberflaeche/kleid/wildside-marke.svg (Symbol «wm»), so wie Website und Werkzeuge sie zeigen."""
    s = open(os.path.join(KLEID, 'wildside-marke.svg'), encoding='utf-8').read()
    m = _re.search(r'<symbol id="wm" viewBox="([^"]+)">(.*?)</symbol>', s, _re.S)
    vb = ' '.join(str(float(x)).rstrip('0').rstrip('.') for x in m.group(1).split())
    return vb, _re.sub(r'\s+fill="currentColor"', '', _re.sub(r'\s*\n\s*', ' ', m.group(2))).strip()


WORT = _wortmarke()
ETIKETTEN = dict(ordner='untersetzer', name='Untersetzer', einzahl='Untersetzer')

SEITEN = [   # alle Seiten, die ein Gast als Seite wahrnimmt, dazu das Rechtliche (Sätze nur aus dem, was auf der Seite steht)
    ('index.html', 'Startseite', 8, 'Ein Abend an der Ecke von 19 bis 2 Uhr: das Eckschild, Momos Frage, das Gewölbe, seit 2018 in Linden, die DJ-Abende, die lange Tafel und wer im selben Haus wohnt.', ''),
    ('drinks.html', 'Drinks', 4, 'Was magst du? Das Gespräch an der Theke, Momos drei Techniken aus dem Labor und die Klassiker des Hauses.', ''),
    ('programm.html', 'Programm', 5, 'Die Plakatwand, die Woche mit drei Abenden, jeder DJ-Abend mit seinem Plakat, Gäste hinterm Tresen, die Feste und Stadtfeste.', ''),
    ('tafel.html', 'Feiern', 5, 'Vom Privaten Dinner über die lange Tafel bis zur ganzen Bar, mit Pauschalen, Budget, Preisen der Bar, Musik und Anfrage.', ''),
    ('haus.html', 'Das Haus', 4, 'Unter dieser Decke: vier Plätze im Raum, Derya und Momo, was bisher geschah, Falstaff und Google.', ''),
    ('besuch.html', 'Besuch', 4, 'Wann die Bar offen hat, die Ecke auf der Karte, einen Platz reservieren und was Gäste vorher fragen.', ''),
    ('impressum.html', 'Rechtliches', 1, 'Impressum und Datenschutz.', 'recht'),
]
LANG = {'Startseite': 'Startseite', 'Rechtliches': 'Impressum und Datenschutz'}   # «und Datenschutz» bleibt zusammen (Tor: Einzelwort)
KURZNAME = {}

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import namen_fall as _nf  # noqa: E402


def _werkzeugname(teil):
    """Name eines Werkzeugs aus der einen Stelle (_werkzeuge/oberflaeche/kleid/wildside.js › namen), nie fest geschrieben."""
    k = open(os.path.join(KLEID, 'wildside.js'), encoding='utf-8').read()
    return dict(_re.findall(r"(\w+): '([^']+)'", _re.search(r'namen:\s*\{([^}]*)\}', k).group(1)))[teil]


# ---------- Unterlagen: die Karten der Bar (gesetzt mit der Pairing-Karte, PDFs in unterlagen/pdf) ----------
SATZ_FUSS = 'Walk on the Wild Side · Haasemannstraße 13 · 30449 Hannover-Linden'
UNTERLAGEN = dict(
    pflege=('Karten selbst ändern', 'http://127.0.0.1:9083/_werkzeuge/carte/'),
    text='Die Karte wechselt immer wieder, die Drinks dafür entwirft Momo. Hier liegen die Karten der Bar neu gesetzt neben dem Blatt, wie es auf dem Tisch lag.',
    seite_text='Die Karten der Bar, neu gesetzt im Kleid der neuen Seite: Momos Drinks mit Zutaten und Preis. Links das Blatt, wie es auf dem Tisch lag, rechts die Idee. Jede neue Karte schreibt ihr ' + _nf.in_(_werkzeugname('karten')) + '.',
    knopf2=('Die Drinks auf der Website', '../drinks.html'))
FAECHER = [(_z, _n) for _z, _n in (('drunk-in-love', 'Sonderkarte'), ('preisliste', 'Preisliste'))
           if os.path.exists(os.path.join(ROOT, 'unterlagen', 'pdf', _z + '.pdf'))]   # zwei Karten im Fächer (PDFs von Werkbank Papier, sb_karten.py)

# ---------- Auftakt, Brief ----------
AUFTAKT = dict(
    titel=['Ein Abend', 'an der Ecke.'],
    text='Die neue Website des Walk on the Wild Side, so wie sie werden könnte. Dazu sieben Werkzeuge, mit denen ihr Karte, DJ-Abende, Anfragen und Plakate selbst führt, und Ideen für Papier und Instagram.',
    abzuege=[(bild('momo-giesst'), 'Momo gießt ein'), (bild('negroni'), 'NEGRONI über der Vitrine'), (bild('schild'), 'Das Eckschild bei Nacht')])
BRIEF = dict(
    art='kurz',
    bild=bild('decke-raum'), schnitt=2.0, lage=(.5, .42), bild_alt='Das Gewölbe über dem Raum des Walk on the Wild Side, die Theke darunter',
    schild=('Walk on the Wild Side', 'Haasemannstraße 13 · Linden'), ort='Tasty Studios',
    absaetze=[
        'Ein Abend bei euch fängt mit einer Frage an: Was magst du? Momo hört zu, greift zu den Flaschen und stellt einen Drink hin, den es so nur an diesem Abend gibt. Darüber das Gewölbe, samstags legt jemand auf. Die neue Seite soll das zeigen, bevor jemand zum ersten Mal an der Ecke steht.',
        'Heute gibt es das Wild Side auf Instagram und in Portalen wie Google und Falstaff. Zeiten, DJ-Abende und Feiern stehen in Beiträgen und Bildunterschriften, reserviert wird per Anruf oder Nachricht. Die neue Seite stellt alles an einen Ort: die Drinks, die DJ-Abende mit ihren Plakaten, Feiern auf der Empore, das Haus unter der Decke und den Weg an die Ecke.',
        'Um die Seite herum liegt, was ihr im Alltag braucht: die Karte, die Momo immer wieder neu schreibt, Ideen für Papier und Instagram und sieben Werkzeuge, in denen ihr Karte, DJ-Abende, Anfragen und Plakate selbst führt. Alles hier lässt sich anklicken und ausprobieren.'],
    schluss='<q>Good Drinks, Good Music, Good Energy.</q> <small>Walk on the Wild Side</small>',
    abzuege=[])
GABEN = dict(seite='{n} Seiten.', unterlagen='Eure Karten.', papier='{d} Drucksachen und {e} Untersetzer.', feed='{n} Beiträge.', gaeste='Für eure Gäste.', studio='')
GABEN_BILDER = dict(seite=(bild('decke-hoch'), (.5, .5)), unterlagen=(bild('karte-2023'), (.5, .5)), papier=(bild('p-0906'), (.5, .3)), material=(bild('flaschen'), (.5, .5)), gaeste=(bild('theke'), (.5, .5)))
LAUFWORTE = ['Walk on the Wild Side', '<b>Nachbarschafts-Mixology-Bar</b>', 'Du sagst, was du magst', 'Samstags SESSION', '<b>Linden</b>', 'Falstaff 91 Punkte']
REIHENFOLGE = ['brief', 'vergleich', 'ideen', 'gefuege', 'seiten', 'unterlagen', 'handschrift', 'papier', 'material', 'dazu', 'schluss']   # der Feed kommt als eigene Bühne (feed_buehne.py)

# ---------- Website: Ideen (Aufnahmen _werkbank/sb_ideen.js → ansichten/Ideen), Vergleich (sb_heute.py → ansichten/Vorher) ----------
IDEEN = [   # (Aufnahme, Titel, Satz, Ausschnitt): jeder Satz nur aus dem, was auf der Aufnahme zu sehen ist
    ('Ideen/start', 'Du sagst, was du magst.', 'Das Eckschild bei Nacht über den ganzen Schirm, links die Wortmarke, der Satz der Bar, die Zeiten und der Weg zum Reservieren.', '50% 50%'),
    ('Ideen/bar', 'Eure Nachbarschafts-Mixology-Bar', 'Gleich nach dem Auftakt steht, wessen Bar das ist: wer sie führt, wo sie liegt und wann sie offen hat, in einem Schild mit Goldlinie.', '50% 50%'),
    ('Ideen/gespraech', 'Was magst du?', 'Momos Frage als Weg durch die Seite: Momo bei der Arbeit in fünf Fotos an einer Goldlinie, von der Frage bis zum fertigen Glas.', '50% 50%'),
    ('Ideen/gewoelbe', 'Ein Gewölbe über der Theke', 'Zwölf Stücke steigen aus verschiedenen Tiefen und schließen sich zum Bild der Decke.', '50% 50%'),
    ('Ideen/chronik', 'Seit 2018 in Linden', 'Fotos und Jahre im Wechsel wie ein Schachbrett, die 91 von Falstaff als dunkle Zelle.', '50% 50%'),
    ('Ideen/lauter', 'Samstags legt jemand auf', 'Das Plakat des nächsten DJ-Abends liegt wie ein Flyer auf dem Tresen, daneben die Woche der Bar.', '50% 50%'),
    ('Ideen/tafel', 'Die lange Tafel', 'Ein breites Bild der Empore über zwei kleinen, daneben der Weg zu Feiern mit zehn bis zwanzig Gästen.', '50% 50%'),
    ('Ideen/imhaus', 'Unter demselben Dach', 'Culinarium, Dirty Chicken und die Feste als Vitrine unter warmem Licht, die Links auf einer Linie.', '50% 50%'),
    ('Ideen/technik', 'Aus dem Labor an die Theke', 'Milk Washing, Fat Washing und Enzyme als drei Platten, jede Technik in zwei Sätzen erklärt.', '50% 50%'),
    ('Ideen/plakate', 'Jeder Abend ein Plakat', 'Das große Plakat auf Creme, alle DJ-Abende klein daneben; wer auf einen Abend zeigt, sieht sein Plakat.', '50% 50%'),
    ('Ideen/raum', 'Dein Platz für heute Abend', 'An der Theke, am Tisch, auf der Empore, draußen an der Ecke: vier Plätze im Raum, jeder mit Bild und Satz.', '50% 50%'),
    ('Ideen/licht', 'Das Licht geht an', 'Sechs Fotos Kante an Kante im Halbdunkel, das Licht geht eins nach dem anderen an, darüber «Bis 2 Uhr.».', '50% 50%'),
]
VORHER = [   # das Wild Side hat heute keine Website: «heute» ist das Profil auf Instagram (Aufnahme des Spähers, _quelle/aus-culinarium/spaeher), «neu» die neue Seite
    ('startseite', 'Startseite', 'Aus einem Profil wird eine Seite.',
     ['Heute ist das Wild Side ein Profil auf Instagram: der Name, vier Zeilen und die Beiträge. Neu steht eine Seite unter eigenem Namen, mit Zeiten und dem Weg zum Reservieren gleich oben.',
      'Was die Bar ausmacht, steht in einem Satz, bevor die Seite erzählt: Momo fragt, was du magst, und macht daraus einen Drink.',
      'Drinks, DJ-Abende, Feiern, das Haus und der Besuch haben je ihre eigene Seite.'], 'index.html'),
]
VERGLEICH_TEXT = 'Links, wie das Wild Side heute im Netz steht, rechts die neue Seite. Den Griff schiebt ihr hin und her, daneben steht, was neu ist.'


def gefuege(z):
    n = [
        ['fotos', 0, 0, 'Eure Fotos', 'von Abenden an der Bar', 'ein', 'Eure Fotos', 'Die Aufnahmen aus euren Beiträgen, von Google und vom Haus: Momo an der Theke, das Gewölbe, die Gläser, das Eckschild bei Nacht.', ['Bar', 'Decke', 'Gläser']],
        ['plakate', 0, 1, 'Eure Plakate', 'seit September 2025', 'ein', 'Eure Plakate', 'Jedes SESSION-Plakat der DJ-Abende, mit Datum und Gesicht des Abends, dazu die weißen Plakate mit roter Wortmarke.', ['SESSION', 'Feste']],
        ['karte', 0, 2, 'Eure Karten', 'Momos Drinks', 'ein', 'Eure Karten', 'Die Karte, die Momo immer wieder neu schreibt, die Klassiker und die Valentinskarte «Drunk in Love».', ['Drinks', 'Preise']],
        ['texte', 0, 3, 'Eure Worte', 'aus euren Beiträgen', 'ein', 'Eure Worte', 'Was ihr auf Instagram schreibt, «Eure Nachbarschafts-Mixology-Bar», «Good Drinks, Good Music, Good Energy», ist der Grund jeder Zeile.', ['Beiträge', 'Bio']],
        ['zeichen', 0, 4, 'Eure Wortmarke', 'drei Zeilen in Rot', 'ein', 'Eure Wortmarke', 'WALK / ON THE / WILD SIDE aus eurem Logo, nachgezogen, in jeder Größe scharf.', ['Wortmarke']],
        ['mappe', 0, 5, 'Eure Mappe', 'Angebote zum Feiern', 'ein', 'Eure Mappe', 'Die Angebotsmappe der Bar: Privates Dinner, lange Tafel, die ganze Bar, Pauschalen und Preise.', []],
        ['bildwelt', 1, 0, 'Bildwelt', 'jedes Foto mit festem Platz', '', 'Bildwelt', 'Jedes Foto liegt in mehreren Größen vor, für den Rechner und fürs Handy, und sitzt mit seinem Ausschnitt fest.', ['Ausschnitt', 'Größen']],
        ['abende', 1, 1, 'Die DJ-Abende', 'eine Stelle', '', 'Die DJ-Abende', 'Jeder DJ-Abend mit Datum, Namen und Plakat an einer Stelle. Daraus entstehen die Woche, die Plakatwand und der nächste Abend auf der Startseite.', ['Datum', 'Plakat']],
        ['zeiten', 1, 2, 'Zeiten und Adresse', 'eine Stelle', '', 'Zeiten und Adresse', 'Donnerstag bis Samstag ab 19 Uhr, die Ecke, Telefon und Instagram stehen einmal und erscheinen überall gleich.', []],
        ['muster', 1, 3, 'Nacht und Gold', 'wie das Eckschild', '', 'Farben und Form', 'Die Nacht der Bar, das Creme der weißen Plakate, Gold als Haarlinie wie am Eckschild, Rot nur als Punkt.', ['Farben', 'Eckschild']],
        ['uhr', 1, 4, 'Von 19 bis 2 Uhr', 'als Faden', '', 'Die Uhrzeiten', 'Jedes Kapitel der Startseite trägt eine Uhrzeit, vom Auftakt um 19 Uhr bis zum Fuß um 2 Uhr.', []],
        ['chronik', 1, 5, 'Chronik', '2018 bis 2027', '', 'Chronik', 'Momo seit 2018 in Linden, die Wiedereröffnung am 9. November 2023, die DJ-Abende seit 2025, Falstaff 2027.', []],
        ['start', 2, 0, 'Startseite', 'ein Abend an der Ecke', 'seite', 'Startseite', 'Vom Eckschild über Momos Frage und das Gewölbe zu den DJ-Abenden, zur langen Tafel und zu den Nachbarn im Haus.', ['Frage', 'Gewölbe', 'SESSION']],
        ['drinks', 2, 1, 'Drinks', 'Was magst du?', 'seite', 'Drinks', 'Das Gespräch an der Theke, drei Techniken aus dem Labor und die Klassiker.', ['Gespräch', 'Klassiker']],
        ['programm', 2, 2, 'Programm', 'Lauter', 'seite', 'Programm', 'Die Woche, die DJ-Abende mit ihren Plakaten, Gastschichten und Feste.', []],
        ['feiern', 2, 3, 'Feiern', 'Euer Abend', 'seite', 'Feiern', 'Privates Dinner, lange Tafel und die ganze Bar mit Preisen und Anfrage.', []],
        ['haus', 2, 4, 'Haus und Besuch', 'unter dieser Decke', 'seite', 'Das Haus und der Besuch', 'Der Raum, Derya und Momo, die Jahre, die Zeiten und der Weg an die Ecke.', []],
        ['reservieren', 3, 0, 'Reservieren', 'per Nachricht', 'sys', 'Reservieren', 'Im Entwurf gespielt: Plätze antippen, Abend und Uhrzeit wählen, die Bar bestätigt per Nachricht. Es wird nichts verschickt.', []],
        ['anfrage', 3, 1, 'Feiern anfragen', 'ins Werkzeug', 'sys', 'Feiern anfragen', 'Wer feiern will, schreibt Format, Tag und Zahl der Gäste. Die Anfrage kommt im Werkzeug für die Gäste an, nie als Mail.', []],
        ['pdf', 3, 2, 'Karte als PDF', 'zum Teilen', 'sys', 'Karte als PDF', 'Jede Karte liegt zusätzlich als PDF bereit.', []],
        ['studio', 3, 3, 'Sieben Werkzeuge', 'für euch', 'sys', 'Sieben Werkzeuge', 'Mit ihnen tragt ihr Karte, DJ-Abende, Plakate und Texte selbst ein; jede Änderung wartet als Entwurf.', ['Karte', 'DJ-Abende', 'Plakate']],
    ]
    k = [['fotos', 'bildwelt'], ['plakate', 'abende'], ['plakate', 'muster'], ['karte', 'pdf'], ['karte', 'drinks'], ['texte', 'start'], ['zeichen', 'muster'], ['mappe', 'feiern'],
         ['bildwelt', 'start'], ['bildwelt', 'haus'], ['abende', 'programm'], ['abende', 'start'], ['zeiten', 'haus'], ['uhr', 'start'], ['chronik', 'haus'],
         ['feiern', 'anfrage'], ['haus', 'reservieren'], ['studio', 'programm'], ['studio', 'drinks'], ['studio', 'start']]
    return {'sp': ['Von euch', 'Daraus gemacht', 'Die Seiten', 'Im Hintergrund'], 'fx': [0.118, 0.372, 0.628, 0.882], 'n': n, 'k': k,
            'tour': ['fotos', 'plakate', 'karte', 'reservieren', 'anfrage', 'studio'], 'fuss': 'Folgt einer Linie: Sie führt von dem, was von euch kommt, zur Seite',
            'start': ['Übersicht', 'Von euch zur Seite', 'Tippt eine Kachel an, dann leuchtet ihr Weg. Oder startet den Rundgang.']}


# ---------- Für eure Gäste (Gäste-Funktionen der Website, Aufnahmen sb_ideen.js → ansichten/Gaeste) ----------
GAESTE = [
    ('reservieren', 'Einen Platz reservieren', 'Hocker antippen, Abend und Uhrzeit wählen, Name und Telefon; die Bar bestätigt per Nachricht. Im Entwurf wird nichts verschickt.', '50% 0'),
    ('wann', 'Wann offen ist', 'Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr, der heutige Tag hervorgehoben.', '50% 50%'),
    ('feiern', 'Wie viele seid ihr?', 'Drei Formate vom Privaten Dinner bis zur ganzen Bar; wer sein Format wählt, kommt direkt zu Preisen und Anfrage.', '50% 50%'),
    ('woche', 'Die Woche', 'Donnerstag live, Freitag Momo an der Bar, Samstag die DJ-Abende: drei Abende auf einen Blick.', '50% 50%'),
    ('fragen', 'Was Gäste vorher fragen', 'Karte, Preise, Drinks ohne Alkohol, Eintritt, Essen, draußen sitzen, feiern: sieben Antworten zum Aufklappen.', '50% 50%'),
    ('wo', 'Die Ecke', 'Haasemannstraße 13, Ecke Rampenstraße, mit Stadtbahn und Karte von Linden-Mitte.', '50% 50%'),
]
GAESTE_TEL = []
GAESTE_KNOEPFE = [('Platz reservieren', '../besuch.html#reservieren'), ('Feiern anfragen', '../tafel.html#anfragen'), ('Der Weg', '../besuch.html#wo')]
GAESTE_LINK = '../besuch.html'
GABEN['gaeste'] = 'Reservieren, die Zeiten, Feiern, die Woche, die Fragen und der Weg.'

# ---------- Handschrift (marke_werkbank.py) ----------
HANDSCHRIFT = dict(
    text='Eure Bar hat schon alles, was eine Marke braucht: die Wortmarke in Rot, das Eckschild mit Goldrahmen und die Plakate in Creme. Die Seite nimmt das auf, dazu eine Antiqua mit Glanz für die großen Zeilen.',
    marke_etik='Wortmarke', marke_text='Eure Wortmarke kommt aus dem Logo der Bar und bleibt in jeder Größe scharf: Rot auf Creme, Creme auf der Nacht, nie neu gesetzt.',
    schriften=[], farben=[], farben_etik='aus Schild, Plakaten und Fotos',
    muster_etik='Das Ornament',
    muster_text='Auf ruhigen Flächen liegt ein feines Ornament in Gold-Haarlinien, Ton in Ton. Man findet es auf der Seite und auf den Drucksachen.',
    knopf_text='Diese Knöpfe darf man drücken.', knoepfe=('Ausprobieren', 'Noch einmal'))

# ---------- Feed, Papier, Dateien ----------
FEED = dict(art='bogen', bogen=[1, 2, 3, 4, 5, 6, 7, 8, 9], bogen_zeile='Die ersten drei Reihen',
            text1='', text2='Tippt auf den Bildschirm, dann scrollt ihr durch den Feed wie am Handy.', kacheln=[])
PAPIER = dict(
    etik_text='An der Theke stehen Momos Drinks auf Untersetzern: zwölf Ideen mit der Wortmarke, dem Eckschild und den Wellen der SESSION-Plakate.',
    druck_text='Von der Karte bis zum Plakat für die Tür, dazu <a href="../sticker/index.html" target="_blank" rel="noopener">Sticker</a> und <a href="../beigaben/index.html" target="_blank" rel="noopener">Beigaben</a>.',
    orte_e=[(3, 6, 28, -3), (36, 6, 28, 2), (69, 6, 28, -2), (3, 54, 28, 2), (36, 54, 28, -3), (69, 54, 28, 3)],
    orte_d=[('karte', 3, 16, 29, -3, 0), ('tuer', 35.5, 16, 29, 2, 0), ('session', 68, 16, 29, -2, 0)])
PAPIER_SEITE = dict(
    breit={'karte', 'karte-r', 'briefbogen', 'umschlag', 'gutschein', 'gutschein-r'},
    formen=set(),
    auslage=[('karte', 2, 2, 26, -6), ('gutschein', 32, 8, 58, 3), ('drink-1', 74, 44, 17, 7), ('drink-2', 56, 56, 17, -4), ('karte-r', 6, 50, 26, 4), ('umschlag', 28, 70, 42, -3)],
    karton={'karte': ('', [('karte', 44, 'Vorderseite'), ('karte-r', 44, 'Rückseite')]),
            'drinks': ('', [('drink-1', 30, 'Milk Washing'), ('drink-2', 30, 'Fat Washing'), ('drink-3', 30, 'Enzyme')]),
            'gutschein': ('', [('gutschein', 88, 'Vorderseite'), ('gutschein-r', 88, 'Rückseite')]),
            'briefpapier': ('', [('umschlag', 92, 'Umschlag'), ('briefbogen', 38, 'Briefbogen')])},
    titel={'karte': ['Die Karte', 'für die Theke.'], 'drinks': ['Ein Kärtchen', 'zu jeder Technik.'], 'gutschein': ['Ein Gutschein', 'für einen Abend.'], 'briefpapier': ['Briefbogen', 'und Umschlag.']},
    schatten={'karte', 'drinks', 'gutschein', 'briefpapier'},
    flaeche=['fl--papier', 'fl--nacht tapete-leicht', 'fl--papier', 'fl--creme'],
    etik_titel=('Untersetzer', 'für die Theke.'),
    etik_text='Zum Drink an der Theke gehört ein Untersetzer. Hier sind {n} als Idee: sechs auf Creme mit roter Wortmarke und den Wellen der Plakate, sechs auf der Nacht der Bar mit Goldlinie.',
    etik_kap='Die Untersetzer', etik_kopf=['Zwölf', 'Untersetzer.'],
    etik_kopftext='Die Wortmarke kommt aus eurem Logo, die Wellen von den SESSION-Plakaten, die Goldlinie vom Eckschild.',
    druck_text='Papier, das bei euch an der Theke, an der Tür oder im Umschlag landen könnte. Was nicht passt, lasst ihr einfach weg.',
    etik_auslage=[(2, 4, 30, -5), (35, 0, 30, 4), (68, 6, 30, -3), (4, 36, 30, 3), (37, 36, 30, -4), (70, 40, 28, 5), (12, 66, 28, 2), (46, 68, 28, -3), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)])
# Weitere Drucksachen: Karton, Titel und Breite je Stück aus papier_neu_seite.json (geschrieben von papier.py)
try:
    for _k, _v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'papier_neu_seite.json'), encoding='utf-8')).items():
        PAPIER_SEITE['karton'][_k] = (_v['karton'][0], [tuple(x) for x in _v['karton'][1]]); PAPIER_SEITE['titel'][_k] = _v['titel']
        PAPIER_SEITE['breit'].update(_v['breit']); PAPIER_SEITE['schatten'].add(_k)
except FileNotFoundError:
    pass
MATERIAL = dict(
    text='Was für den Entwurf neu entstanden ist, liegt sortiert in einem Ordner: die Karten als PDF, die Drucksachen, die Untersetzer, die Sticker, die Beigaben, die Postkarten, die Beiträge für Instagram und eure Wortmarke als Datei.',
    streu=[(bild('wf-coupes-oben'), 'Gläser mit Goldrand', -4, '-0.05'), (bild('rm-glaeser'), 'Hinter der Theke', 3, '0.04'), (bild('wf-pink'), 'Ein Drink mit Schaum', -2, '-0.07'),
           (bild('wf-giesst'), 'Momo gießt ein', 4, '0.05'), (bild('wf-erdbeer'), 'Highball mit Erdbeere', -3, '-0.04')],
    druck_satz='Von der Karte für die Theke bis zum Plakat für die Tür.',
    zeichen=[('Eure Wortmarke', '../../_werkzeuge/oberflaeche/kleid/wildside-marke.svg', 'Walk on the Wild Side Wortmarke.svg')],
    zeichen_satz='Die Wortmarke der Bar als Zeichnung, die in jeder Größe scharf bleibt.',
    auslage=[])
AUSBLICK = dict(text='Ein paar Dinge fehlen noch.', gross=('', '', ''), punkte=[], studio='')
SCHLUSS = dict(bild=bild('schild-ecke'))
KAPITEL = {
    'vergleich': dict(text=VERGLEICH_TEXT),
    'ideen': dict(text='Hinter jeder Stelle der Seite steht ein Gedanke. Zwölf davon sind hier aufgenommen, so wie die Seite heute aussieht.'),
    'gefuege': dict(text='Links, was von euch kommt, in der Mitte, was daraus geworden ist, rechts die Seiten und was im Hintergrund mitläuft.'),
    'seiten': dict(text='Eine Seite aussuchen, mit den Pfeilen weiterblättern. Rechts dieselbe Stelle am Handy, mit «Öffnen» seid ihr auf der echten Seite.'),
    'unterlagen': dict(text=UNTERLAGEN['text']),
    'gaeste': dict(text='Wer vorbeikommen will, will vorher wissen, wann offen ist, ob noch Platz ist und wie er hinfindet. Wer feiern will, sucht Format und Preis. Auf der neuen Seite steht das an einem Ort.'),
    'papier': dict(text='Für das Wild Side ist einiges entstanden: zwölf Untersetzer für Momos Drinks, Drucksachen von der Karte bis zum Plakat für die Tür, Mails für eure Gäste und eine Postkarte zu jedem DJ-Abend.'),
    'material': dict(text='Wer eine Datei braucht, findet sie hier: jede Karte als PDF, jede Drucksache, jeden Untersetzer und eure Wortmarke in voller Schärfe.'),
    'geprueft': dict(text='Bevor etwas davon zu euch kommt, wird es geöffnet, gelesen und gedrückt: am Handy wie am Rechner, jede Karte gegen eure Angaben, jedes Werkzeug in jedem Schritt. Das Blatt fasst es zusammen, der Bericht erzählt es ganz.'),
    'schluss': dict(text='Sagt mir offen, was euch am Entwurf gefällt und was nicht. Ändern lässt sich alles.'),
}
MEINS = ['Der Brief und alle Sätze der Werkbank', 'Titel und Sätze zu den Ideen, zum Gefüge, zu den Drucksachen und Untersetzern', 'Feldnamen und Zeilen auf Gutschein und Karte', 'Texte zu den Beiträgen des Feeds']

# ---------- Geprüft (nur Belegtes; Belege in website/_werkbank/pruefung/, Werkzeuge aus ihren Lieferungen) ----------
import datetime as _dt
GEPRUEFT = [
    ('Die Website', 'seite', ['Alle Seiten in der Technik von Safari und von Chrome, am Handy und am Rechner: nichts läuft seitlich über, kein Skriptfehler, kein kaputtes Bild.',
                              'In vier Breiten angesehen, vom Handy bis zum großen Bildschirm.',
                              'Jede Angabe kommt aus einer Stelle mit Quelle: Zeiten, Adresse, Telefon, DJ-Abende und Preise.']),
    ('Die Karten', 'karte', ['Jede Karte aus euren Angaben gelesen, nicht abgetippt.',
                             'Was ihr klären müsst, steht gesondert in der Liste der offenen Punkte.']),
    ('Die Werkzeuge', 'schloss', ['Jedes der sieben Werkzeuge in einem eigenen Durchgang gebaut und Knopf für Knopf bedient, nur mit erfundenen Daten.',
                                  'Kein Werkzeug verschickt etwas von selbst, keines öffnet ein Mailprogramm.']),
]
GEPRUEFT_PUNKTE = [
    ('Die Website', 'Jede Seite am Handy und am Rechner, in vier Breiten. Nichts rutscht zur Seite, kein Bild fehlt.'),
    ('Die Karten', 'Gelesen aus euren eigenen Angaben, nicht abgeschrieben. Jeder Drink und jeder Preis steht so, wie ihr ihn angekündigt habt.'),
    ('Die Werkzeuge', 'Jedes der sieben in seinem eigenen Durchgang bedient, mit erfundenen Gästen und Zahlen. Keines schickt von sich aus eine Nachricht.'),
    ('Eure Daten', 'Gäste bekommen keine Kekse in den Browser. Was sie reservieren oder anfragen, landet bei euch, und im Entwurf nie bei der echten Bar.'),
]
GEPRUEFT_TRIO = [(bild('wf-theke'), 1.6, (.5, .5), 'An der Theke'), (bild('rueckbar'), 1.6, (.5, .5), 'Die Rückbar'), (bild('pl-ecke'), 1.6, (.5, .5), 'An der Ecke')]
GEPRUEFT_OFFEN = 'Ein paar Fragen könnt nur ihr beantworten: wer ins Impressum kommt, wer an welchem Foto und Plakat die Rechte hat und wer welches Werkzeug bekommt.'
GEPRUEFT_EIN = 'Hier steht in einfachen Worten, was an Website, Karten und Werkzeugen angesehen und ausprobiert wurde, und was danach noch bei euch liegt.'
GEPRUEFT_NAV = ['Website', 'Karten', 'Werkzeuge', 'Daten', 'Offen']
PRUEF_WERKZEUGE = [   # aus den Commits «…: fertig – geprüft (…)» im git log vom 31.10.2026 (Zahl der geprüften Zustände, je 0 Funde)
    ('zentrale', '1 Zustand'), ('website', '59 Zustände'), ('karten', '34 Zustände'), ('gaeste', '51 Zustände'),
    ('marke', '26 Zustände'), ('besuche', '172 Zustände'), ('druck', '346 Zustände')]
GEPRUEFT_MEHR = [
    ('Die Website', 'seite', 'Acht Seiten: sechs für eure Gäste von der Startseite bis zum Besuch, dazu Impressum und Datenschutz.', [
        'Jede Seite in Safari und in Chrome geöffnet, auf dem Handy und auf dem Rechner. Nichts verrutscht zur Seite, kein Bild fehlt, kein Skript bricht ab.',
        'In vier Breiten angesehen, von 390 bis 1440 Pixel. Beim Laden springt nichts.',
        'Zeiten, Adresse, Telefon, DJ-Abende und Preise stehen an genau einer Stelle, mit ihrer Quelle, und jede Seite liest von dort.']),
    ('Die Karten', 'karte', 'Die Karten der Bar: Momos Drinks mit Zutaten und Preis.', [
        'Gelesen aus euren Beiträgen und Unterlagen, nicht abgeschrieben.',
        'Neu gesetzt im Kleid der neuen Seite, die Schriften fest eingebettet.']),
    ('Die sieben Werkzeuge', 'schloss', 'Die Werkzeuge, mit denen ihr Karte, DJ-Abende, Plakate und Gäste selbst führt.', [
        'Jedes Werkzeug in seinem eigenen Durchgang gebaut und Schritt für Schritt bedient, mit erfundenen Gästen und Zahlen.',
        'Kein Werkzeug schickt etwas von sich aus und keines öffnet ein Mailprogramm. Antworten an Gäste bleiben als Entwurf im Werkzeug, bis jemand sie selbst verschickt.',
        'Jedes Werkzeug ging durch die Prüfung in vier Breiten (1440, 1280, 1000 und 390 Pixel), Start, jeder Reiter, jedes Fenster: '
        + ', '.join(f'{_werkzeugname(t)} {n}' for t, n in PRUEF_WERKZEUGE) + '. Gefunden wurde dabei nichts, das offen geblieben ist.']),
    ('Eure Daten und die eurer Gäste', 'schild', 'Was gespeichert wird und was nicht.', [
        'Gäste bekommen keine Cookies. Im Entwurf werden keine Besuche gezählt; ' + _nf.klein(_werkzeugname('besuche')) + ' zeigt erfundene Zahlen.',
        'Reservieren und Feiern anfragen laufen im Entwurf nur zur Probe; nichts davon erreicht die echte Bar.',
        'Suchmaschinen sehen den Entwurf nicht, bis ihr ihn freigebt.']),
    ('Was offen bleibt', 'auge', 'Das könnt nur ihr entscheiden.', [
        'Wer im Impressum steht und unter welcher E-Mail-Adresse die Bar erreichbar sein soll.',
        'Wer an welchem Foto und an den Plakaten die Rechte hat.',
        'Im Entwurf öffnen sich die Werkzeuge ohne Anmeldung. Zum Umzug bekommt jede Person ihren eigenen Zugang.'])]
PRUEFDATUM = _dt.date(2026, 10, 31)
STEMPEL_TEXT = f'GEPRÜFT · WILD SIDE · {PRUEFDATUM:%d.%m.%Y} ·'
GEPRUEFT_BILD = bild('wf-theke')

# ================================================================ Bausteine (Vorlage Schäfli, kopiert und umgeschrieben; Kit unverändert)
import sys as _sys
_sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
EIGENE, EIGENE_BILDER, FLAECHE = [], [], {}
CSS = ''
_WB = os.path.join(ROOT, 'werkbank')

import brief_blatt as _bb  # noqa: E402
brief_abschnitt = _bb.abschnitt(globals())
EIGENE_BILDER += _bb.bilder(BRIEF)
CSS += _bb.CSS
import kopf_mitte as _km  # noqa: E402
import auftakt_kacheln as _ak  # noqa: E402
CSS += _km.CSS + _ak.CSS
FLAECHE.update(brief='fl--papier tapete-hell', vergleich='fl--nacht tapete-leicht', ideen='fl--blau tapete-leicht', gefuege='fl--nacht tapete-leicht',
               seiten='fl--papier tapete-hell', gaeste='fl--navy tapete', unterlagen='fl--tief tapete-leicht', papier='fl--navy tapete', material='fl--papier tapete-hell',
               feed='fl--nacht tapete-leicht', geprueft='fl--navy tapete')
CSS += '''
/* ---------- Leichte Tapete: das feine Raster der Website auf jeder dunklen Fläche ---------- */
.tapete-leicht{background-image:linear-gradient(var(--tl),var(--tl)),var(--muster);background-size:auto,var(--musterb) auto;background-position:0 0,50% 0}
.fl--nacht.tapete-leicht{--tl:rgba(19,14,13,.35)}
.fl--blau.tapete-leicht{--tl:rgba(51,40,31,.3)}
.fl--tief.tapete-leicht{--tl:rgba(28,21,19,.35)}
.tapete-hell{background-image:url(/werkbank/eigen/tapete-hell.svg);background-size:150px auto;background-position:50% 0}
/* ---------- Titel wie auf der Website: Prata, eine Stärke, normale Schreibung, Betonung nur über die Farbe, nie fett, nie kursiv ---------- */
.zt,.t1,.t2,.t3,.wfen__t,.ins-t h3,.rgw .wfa__texte h3,.sbf-text h3,.hs2-ww+small{font-weight:400!important}
.zt{text-transform:none;letter-spacing:-.012em}
.zt em,em{font-style:normal}
.kap--k .kap__geist{display:none}.kap--z span,.kap--k>span{font-family:var(--mono)!important;font-weight:400!important;font-size:12px!important;letter-spacing:.2em;text-transform:uppercase}
.wfen__t{text-transform:none;letter-spacing:-.01em}
h2,h3,.wege__t,.gb-blatt header h3,.rgw .wfa__texte h3,.fbz__n{font-weight:400!important}
b,strong{font-weight:500}
.gb-blatt header h3{font-family:var(--serif);text-transform:uppercase;letter-spacing:.135em}
.wf .wege__t{font-family:var(--serif);text-transform:none;letter-spacing:-.01em;font-size:clamp(2rem,3.6vw,3.4rem)!important;line-height:1.1}
/* Schriften der Bar unter ihrem Namen, auch wenn ein Kit-Lauf werkbank.css neu schreibt (dort heissen sie «Instrument Sans» und «DM Mono») */
@font-face{font-family:'Hanken Grotesk';font-style:normal;font-weight:100 900;font-display:swap;src:url('fonts/hanken.woff2') format('woff2')}
@font-face{font-family:'Hanken Etikett';font-style:normal;font-weight:100 900;font-display:swap;src:url('fonts/hanken.woff2') format('woff2')}
:root{--sans:'Hanken Grotesk','Sans Ersatz',system-ui,-apple-system,'Segoe UI',sans-serif!important;--mono:'Hanken Etikett','Hanken Grotesk',ui-monospace,monospace!important}
/* Schrift mittig (Abnahme-Tor 31.10.: Prata-Ziffern im Register 2 px zu hoch, «01» im Befund 1 px zu weit links) */
.rgc-p{padding:9px 10px 5px!important}
/* Reiter der Werkzeuge und Ziffern der Befunde: symmetrisch, letzter Buchstabe ohne Sperrung (ins-mitte-js), Chromium setzt Hanken 0,7 px höher als WebKit */
.ins-m{padding:8px 16px!important}
.ins-m .tm-l,.sbf-z .tm-l{letter-spacing:0}
@supports (interpolate-size:allow-keywords){.ins-m>.tm{position:relative;top:.7px}.sbf-b .sbf-z>.tm{top:.7px!important}}   /* nur Chromium: WebKit unter Linux kennt -apple-system-body nicht (Oberchef 1.11.) */
.sbf-z{padding:7px 9px!important;letter-spacing:0!important}.sbf-z[data-i="0"]{padding-left:9.5px!important;padding-right:8.5px!important}   /* «01»: die Eins steht in Hanken weiter links (Chromium und WebKit gleich) */
@media(max-width:600px){.auftakt__fuss .runter i{display:none}.auftakt__fuss .runter{gap:0}}   /* am Handy alle Zeilen auf einer Kante */
/* Die Wortmarke als Zeichen steht in ihrem Rot (Rot nur als Punkt: Logo), nie in Gold */
svg:has(> use[href="#hz"]){color:#f0323f!important;fill:#f0323f}
/* Etiketten der Bar: Hanken 500, gesperrt, Versalien (wie .etikett der Website) */
.rz{font-family:var(--sans);font-weight:500;letter-spacing:.17em;text-transform:uppercase}
'''

import marke_werkbank as _mw  # noqa: E402
EIGENE.append(_mw.abschnitt(globals())); EIGENE_BILDER += _mw.BILDER; CSS += _mw.CSS
FLAECHE['handschrift'] = 'fl--navy tapete'
import mails_reihe as _mr  # noqa: E402
CSS += _mr.CSS
EIGENE_BILDER += _mr.BILDER   # die drei Mails als dritte Karte im Papier (wb_kapitel.papier_mails)
import feed_buehne as _fb  # noqa: E402
_FEED_DA = os.path.exists(os.path.join(ROOT, 'feed', 'feed.json'))
if _fb.BEREIT and _FEED_DA:
    EIGENE.append(_fb.abschnitt(globals())); EIGENE_BILDER += _fb.BILDER; CSS += _fb.CSS
import fenster_ausblick as _fa  # noqa: E402
CSS += _fa.CSS
import geprueft_blatt as _gb  # noqa: E402
geprueft_abschnitt = _gb.abschnitt(globals())
_AN = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ansichten')
for _i, _q in enumerate([os.path.join(_AN, 'Rechner', 'Startseite.jpg'), os.path.join(ROOT, 'unterlagen', 'img', 'n-abend-01.webp'),
                         os.path.join(_AN, 'Werkzeuge', 'bureau.jpg'), os.path.join(_AN, 'Gaeste', 'buchen.jpg')]):
    if os.path.exists(_q):
        EIGENE_BILDER.append((f'gp-{_i}', _q, 320, dict(q=80, schnitt=4 / 3, lage=(.5, 0))))
CSS += _gb.CSS

import fuss_faecher as _ff  # noqa: E402
if _ff.BEREIT:
    wege_abschnitt = _ff.abschnitt
    CSS += _ff.CSS
CSS += '''
/* Dateien: Fotos ohne Polaroid-Rand und ohne Bildzeile, ungleich groß, ohne Drehung */
#material .streu .abzug{padding:0!important;background:none!important;border-radius:clamp(10px,1vw,14px);overflow:hidden;--r:0deg!important;--r0:0deg!important;box-shadow:0 30px 40px -26px rgba(10,7,6,.6),0 10px 16px -10px rgba(10,7,6,.35)!important}
#material .streu .abzug span{display:none!important}
#material .streu .abzug img{display:block;width:100%;height:100%;object-fit:cover;border-radius:0!important}
@media(min-width:760px){#material .streu{align-items:center}#material .streu .abzug:nth-child(3){transform:scale(1.18);z-index:2}#material .streu .abzug:nth-child(2),#material .streu .abzug:nth-child(4){transform:scale(1.04);z-index:1}}
/* Flüssigkeit (Regel 55): Abschnitte außerhalb des Blicks werden nicht gezeichnet. Ausgenommen der Brief (überstehendes Blatt). */
@supports (content-visibility:auto){main>section.fl:not(#brief){content-visibility:auto;contain-intrinsic-size:auto 1400px}}
html.cv-alle main>section.fl:not(#brief){content-visibility:visible}
@media(min-width:760px){.vh-wahl>:first-child,#seiten .wahl>:first-child{margin-left:auto}.vh-wahl>:last-child,#seiten .wahl>:last-child{margin-right:auto}}
@media(max-width:480px){.kn{max-width:100%;height:auto;min-height:54px;padding-top:9px;padding-bottom:9px;white-space:normal;line-height:1.35;text-align:left}.kn i{flex:none}.kn-reihe{max-width:100%}}
.schluss .zt,.schluss .lauf p,.schluss .kap span{text-shadow:0 1px 2px rgba(10,7,6,.9),0 2px 16px rgba(10,7,6,.8),0 0 42px rgba(10,7,6,.55)}
'''


CV_JS = ("<script id=\"cv-hoehen\">(function(){var d=document.documentElement;function alle(){d.classList.add('cv-alle');requestAnimationFrame(function(){requestAnimationFrame(function(){d.classList.remove('cv-alle')})})}"
         "/* einmal alles zeichnen, damit jede Fläche ihre echte Höhe kennt: Sprungmarken landen genau (content-visibility) */"
         "if(document.readyState==='complete')setTimeout(alle,300);else addEventListener('load',function(){setTimeout(alle,300)});"
         "addEventListener('resize',function(){clearTimeout(alle.t);alle.t=setTimeout(alle,400)})})();</script>")
BRETT_HILFE = ("<script id=\"brett-hilfe\">(function(){var b=document.getElementById('brett'),k=document.getElementById('brett-noch');if(!b||!k||!('IntersectionObserver' in window))return;"
               "new IntersectionObserver(function(E,o){if(!E[0].isIntersecting)return;o.disconnect();setTimeout(function(){if(/\\bvor\\b/.test(b.className))k.click()},700)},{rootMargin:'0px 0px -35% 0px'}).observe(b)})();</script>")


def nach_bau():
    """Nach jedem Bau des Kits: Eigenes nach werkbank/eigen, Nacharbeit der Bausteine, Kapitel, Ruhe, Farben, Ihr-Form."""
    import re as _re, shutil as _sh
    from PIL import Image as _I
    q, z = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eigen'), os.path.join(_WB, 'eigen')
    os.makedirs(z, exist_ok=True)
    sig = _I.open(os.path.join(q, 'unterschrift-robert.webp')).convert('RGBA')
    r, g, b = (int(FARBEN['tinte'][i:i + 2], 16) for i in (1, 3, 5))
    _I.merge('RGBA', (*_I.new('RGB', sig.size, (r, g, b)).split(), sig.getchannel('A'))).save(os.path.join(z, 'unterschrift.webp'), 'WEBP', quality=90)
    _fa.fenster_bilder()
    for f in os.listdir(q):
        if f.startswith('fen-'):
            _sh.copy2(os.path.join(q, f), os.path.join(z, f))
    if _fb.BEREIT and _FEED_DA:
        _fb.bilder()
    if _ff.BEREIT:
        _ff.bilder()
    seite = os.path.join(_WB, 'index.html')
    _ak.anwenden(seite)
    _mw.anwenden(seite)
    _fa.anwenden(seite)
    _km.anwenden(seite)
    import fluss_werkbank as _fw
    _fw.anwenden(seite)
    import wb_kapitel as _kp
    _kp.anwenden(seite)
    # Nichts läuft mit dem Scrollen mit (Regel 55)
    t = open(seite, encoding='utf-8').read()
    t = _re.sub(r'\sdata-(?:drift|zug)="[^"]*"', '', t)
    ruhe = ('<style id="sb-ruhe">.bf .bf-blatt[data-a="heben"],.bf .bf-blatt[data-a="heben"].da{animation:none!important}.kap__geist{animation:none!important}'
            '.kn:hover,.kn:active,.rund:hover,.rund:active,.wahl button:active,.vh-wahl button:active,.bn button:hover,.bn button:active,.glanz:active,.ins-r:hover,.ins-r:active,.wf__pf:hover,.wf__pf:active,.rgc-p:hover,.rgc-p:active,.sbf-z:hover{transform:none!important;translate:none!important;scale:none!important}'
            '.kn{overflow:hidden}.ins-reiter,.fb__reiter{padding-top:10px!important;padding-bottom:26px!important;margin-top:-10px!important;margin-bottom:-26px!important}'
            '.wahl,.vh-wahl{padding-top:8px!important;padding-bottom:26px!important;margin-top:-8px!important;margin-bottom:-12px!important}'
            '.wfen .wfen__t{font-size:clamp(24px,3.6vw,54px)!important;line-height:1.14!important}.wfen .wfen__k{font-size:clamp(15px,1.36vw,19px)!important}'
            '#papier img.frei{filter:none!important;box-shadow:none!important}</style>')
    if 'id="sb-ruhe"' not in t:
        t = t.replace('</head>', ruhe + '</head>', 1)
    if 'id="ins-mitte-js"' not in t:   # Reiter der Werkzeuge: Text in .tm, letzter Buchstabe in .tm-l ohne Sperrung (wie knopf_mitte.js)
        t = t.replace('</body>', "<script id=\"ins-mitte-js\">(function(){function m(){document.querySelectorAll('.ins-m').forEach(function(k){var t=k.firstChild;"
                      "if(!t||t.nodeType!==3||!t.textContent.trim())return;var x=t.textContent.replace(/\\s+$/,'');var s=document.createElement('span');s.className='tm';"
                      "s.textContent=x.slice(0,-1);var l=document.createElement('span');l.className='tm-l';l.textContent=x.slice(-1);s.appendChild(l);k.replaceChild(s,t)})}"
                      "m();addEventListener('load',m)})();</script></body>", 1)
    if 'id="brett-hilfe"' not in t:
        t = t.replace('</body>', BRETT_HILFE + '</body>', 1)
    if 'id="cv-hoehen"' not in t:
        t = t.replace('</body>', CV_JS + '</body>', 1)
    import sb_skripte as _sk
    for _id, _js in (('rh-vorladen', _sk.VORLADEN_JS), ('rh-frueh', _sk.FRUEH_JS), ('rh-zurueck', _sk.WB_JS), ('rh-karussell', _sk.KARUSSELL_JS)):
        if f'id="{_id}"' not in t:
            t = t.replace('</body>', _js + '\n</body>', 1)
    open(seite, 'w', encoding='utf-8').write(t)
    import feed_leicht as _fl
    if _fb.BEREIT and _FEED_DA:
        _fl.mach()
    import sb_farbe
    sb_farbe.anwenden()
    # Das Zeichen (Wortmarke) in Gold als Datei für die Karte «Ein Vorschlag.» (als <img> wäre currentColor schwarz)
    vb, innen = ZEICHEN
    open(os.path.join(_WB, 'eigen', 'zeichen-kerze.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="{FARBEN["rot"]}">{innen}</svg>')   # die Wortmarke in ihrem Rot
    open(os.path.join(_WB, 'eigen', 'zeichen-c.svg'), 'w', encoding='utf-8').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="#000">{innen}</svg>')   # Maske für Schmuck im CSS (Listen, Namenszug)
    _ft = os.path.join(ROOT, 'feed', '_tafeln.html')
    if os.path.exists(_ft):
        _s = open(_ft, encoding='utf-8').read()
        if 'noindex' not in _s:   # nach <head> bzw. nach dem Doctype, nie davor (sonst Quirks-Modus)
            if '<head>' in _s:
                _s = _s.replace('<head>', '<head><meta name="robots" content="noindex, nofollow">', 1)
            elif _s.lower().startswith('<!doctype html>'):
                _s = _s[:15] + '<meta name="robots" content="noindex, nofollow">' + _s[15:]
            open(_ft, 'w', encoding='utf-8').write(_s)
    import sb_ki   # Seite «KI und eure Daten», Karte «Ein Vorschlag.» allein und als PDF (Robert 20.10.2026)
    sb_ki.bau()
    import du_gang   # zuletzt: die Sätze aus Kit und Vorlage von der Sie- in die Ihr-Form, deutsche Schreibung
    du_gang.anwenden()
    import nur_bewegung   # bewegt nur transform/opacity, Glanzkante dreht statt neu zu malen, Karte kommt herein (Abnahme-Tor 30.10.2026)
    nur_bewegung.anwenden(ROOT)
    import zeile_ganz   # kein Einzelwort allein in der letzten Titelzeile, Aufschrift im Fensterstapel frei (Abnahme-Tor 30.10.2026)
    zeile_ganz.anwenden(ROOT)
    import text_mitte   # Schrift optisch mittig in den Knöpfen aller Werkbank-Seiten (Messlauf «text-mitte», 29.10.2026)
    text_mitte.anwenden(ROOT)
    import bild_mass   # Bilder in der gezeigten Grösse, damit der Tab in WebKit nicht am Speicher scheitert (Abnahme-Tor 4, 30.10.2026)
    bild_mass.anwenden(ROOT)
    try:   # Knopfschrift in Chromium und WebKit gleich mittig (Baustein von Werkbank Papier, papier_nach.knopf_mitte, nach text_mitte)
        import papier_nach as _pn
        for _s in ('werkbank/index.html', 'werkbank/ki.html', 'werkbank/karte.html', 'werkbank/impressum.html', 'werkbank/geprueft/index.html', 'befund/index.html'):
            if os.path.exists(os.path.join(ROOT, _s)):
                _pn.knopf_mitte(os.path.join(ROOT, _s))
    except Exception as _f:
        print('knopf_mitte nicht gesetzt:', _f)
    import kleid_wild   # zuletzt: Schriftfamilien des Kits auf Prata und Hanken, Reste der Vorlage im Kleid der Bar (Wild Side 31.10.2026)
    kleid_wild.anwenden(ROOT)


TITEL_NEU = {   # eigene Überschriften des Wild Side (Werkbank-Regel 14), keine gleich wie bei Culinarium, Schäfli oder Schlössli
    ('Schön, dass Sie', 'hereinschauen.'): ('Schön, dass', 'ihr da seid.'),
    ('Ihre Website,', 'Seite für Seite.'): ('Heute ein Profil,', 'morgen eine Seite.'),
    ('Die Ideen', 'hinter der Seite.'): ('Zwölf Stellen,', 'zwölf Gedanken.'),
    ('Wie alles', 'zusammenhängt.'): ('Was hinter', 'der Theke steht.'),
    ('Alle Seiten zum', 'Durchblättern.'): ('Von der Ecke', 'bis zur Empore.'),
    ('Vorschläge für', 'Ihre Gäste.'): ('Bevor der Gast', 'an der Ecke steht.'),
    ('Ihre Unterlagen,', 'im selben Stil.'): ('Eure Karten,', 'neu gesetzt.'),
    ('Ein paar Ideen', 'für Papier.'): ('Für Theke', 'und Tür.'),
    ('Ein Feed', 'für Instagram.'): ('Ein Feed,', 'der nach Nacht aussieht.'),
    ('Alles liegt für', 'Sie bereit.'): ('Alle Dateien', 'an einem Ort.'),
    ('Alles geprüft,', 'bevor Sie es sehen.'): ('Ausprobiert,', 'Stück für Stück.'),
}
TEXT_NEU = [   # Sätze des Kits, die fürs Haus nicht stimmen (wb_kapitel.eigene_titel ersetzt sie wörtlich)
    ('Links Ihre Seite, wie sie heute ist, rechts der Entwurf. Schieben Sie den Griff hin und her, daneben steht, was neu ist.', VERGLEICH_TEXT),
]
KAP_NAME_NEU = {'Guten Tag': 'Ein Brief', 'Register': 'Inhalt', 'Zum Schluss': 'Bis Montag'}


# Farben und Schnitte schon in H.CSS setzen: baut ein anderer Schritt mit dem Kit (K.gestaltung), stehen so trotzdem die Töne des Hauses
# und kein fetter Schnitt in werkbank.css, nicht erst nach dem Farbgang.
import sb_farbe as _sf  # noqa: E402
CSS = _sf.ohne_fett(_sf.faerbe(CSS))

# Gestaltung 28.10.2026 (Prüfchat Gestaltung): Unterlagen «Heute und als Idee»: das Foto der Karte vom Tisch hat das Format des Blatts daneben (A-Format),
# beide Seiten gleich hoch, nicht ein langes Foto neben einem kürzeren Blatt (Regel «Spalten gleich hoch»).
CSS_SEITEN = '''
.upaar{align-items:center}
.ublatt--alt .ublatt__b{aspect-ratio:1/1.414!important}
.ublatt--alt .ublatt__b img{width:100%;height:100%;object-fit:cover}
'''
