#!/usr/bin/env python3
"""Walk on the Wild Side: zehn Mail-Vorlagen an Gäste, als Idee zum Entwurf (Werkbank, Nachtbau 31.10.2026).
Bauart aus mails/_src/bau.py des Culinarium (elf Mails, Band mit «Ganze Mail»), Inhalt und Kleid der Bar.

Die Fälle kommen aus der neuen Website der Bar: Reservieren (besuch.html, «Die Bar bestätigt»), Feiern mit Anfrage, Angebot und Anzahlung
(tafel.html, Preise von dort gelesen, nie abgetippt), die DJ-Abende SESSION (LINEUP in website/bau.py), die Feste (programm.html),
die wechselnde Karte von Momo (drinks.html). Im Du wie die Bar. Absender «Walk on the Wild Side», Gruss der Bar ohne Namen («Dein Wild Side»); die Bar hat
keine belegte Mailadresse: Kontakt über Telefon und Instagram (HAUS in website/bau.py). Fotos aus dem Bildregister der Website, unter 100 KB,
mit Beschreibung; Tabellen und feste Stile, Titel in Prata (Georgia, wo ein Mailprogramm keine Schrift lädt), Lauf in Hanken Grotesk.
Namen, Daten und Nummern der Gäste sind Beispielwerte und so beschriftet; Preise, Zeiten, Adresse, DJ-Abend und Feste sind die der Bar.
Wortlaut von Tasty Studios, als Vorschlag. Gebaut, nie verschickt.

Aufruf:  python3 mails/_src/bau.py  → mails/NN-<fall>/index.html, mails/index.html, mails/img/;  danach WB_PORT=9288 node mails/_src/aufnahme.js"""
import ast, html, json, os, re, glob, shutil

HIER = os.path.dirname(os.path.abspath(__file__)); MAILS = os.path.dirname(HIER); ROOT = os.path.dirname(MAILS); WEB = os.path.dirname(ROOT)
from PIL import Image  # noqa: E402

# ---------- Hauswerte aus der Website (nur gelesen) ----------
_BAU = open(os.path.join(WEB, 'bau.py'), encoding='utf-8').read()
HAUS = ast.literal_eval(re.search(r'^HAUS = (\{.*?^\})', _BAU, re.S | re.M).group(1))
LINEUP = ast.literal_eval(re.search(r'^LINEUP = (\[.*?^\])', _BAU, re.S | re.M).group(1))
_BILDER = open(os.path.join(WEB, 'bilder.py'), encoding='utf-8').read()


def _text(datei):
    t = open(os.path.join(WEB, datei), encoding='utf-8').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>', '', t, flags=re.S)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)))


_TAFEL = _text('tafel.html')
PAUSCHALE = {int(k): int(p) for k, p in re.findall(r'Kategorie (\d) [^€]*? (\d+) € pro Person', _TAFEL)}
SERVICE = re.search(r'Service und Raum (\d+) €', _TAFEL).group(1)
BUDGET = re.search(r'Euer Budget für Drinks ab ([\d.]+) €', _TAFEL).group(1)
STUNDE = re.search(r'jede angefangene Stunde (\d+) Euro pro Person', _TAFEL).group(1)
ANZAHLUNG = int(re.search(r'(\d+) Prozent eine Woche vorher', _TAFEL).group(1))
SIGNATURE = re.search(r'Signature Drinks ([\d,]+) €', _TAFEL).group(1)
OHNE = re.search(r'Alkoholfreie Drinks ([\d,]+) €', _TAFEL).group(1)
assert sorted(PAUSCHALE) == [1, 2, 3], PAUSCHALE
_FESTE = _text('programm.html')
assert 'am 5. Dezember 2025 zwei' in _FESTE and 'Silvester ab mittags' in _FESTE

TEL, TEL2, IG = HAUS['telefon'], HAUS['telefon2'], HAUS['ig_name']
ADRESSE = f"Walk on the Wild Side · {HAUS['adresse']} · {HAUS['ort']}"
ZEITEN = ' · '.join(f'{t} {z}' for t, z, _ in HAUS['zeiten'][:3]).replace('Freitag 19 bis 2 Uhr · Samstag 19 bis 2 Uhr', 'Freitag und Samstag 19 bis 2 Uhr')
GRUSS = 'Dein Wild Side'   # Gruss der Bar, ohne Namen (Robert 1.11.2026)
STAND = '31.10.2026'

def e(t):
    """escape; Zahl und Euro, Zahl und Uhr bleiben zusammen"""
    return re.sub(r'(\d) (€|Uhr|%)', '\\1&nbsp;\\2', html.escape(t))


TIEF, NACHT, NACHT2, CREME, BLATT, TINTE, LEISE, GOLD, ROT = '#130E0D', '#1C1513', '#261E1A', '#F2E9DC', '#F7F1E7', '#1C1513', '#5E524A', '#D8B264', '#F0323F'
SERIF = "Prata,Georgia,'Times New Roman',serif"
SANS = "Hanken,'Hanken Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif"


def eur(n):
    return f'{n:,}'.replace(',', '.') + ' €'


GAESTE, KAT = 40, 2
SUMME = GAESTE * PAUSCHALE[KAT]
D0, N0, R0, P0 = LINEUP[0]   # der jüngste DJ-Abend der Bar
_T, _M, _J = D0.split('.')
_MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
D0_LANG = f'Samstag, {int(_T)}. {_MONATE[int(_M) - 1]} {_J}'
WEG = ('Den Weg ansehen', 'besuch.html')
MUSIK0 = {'p-1710': '22 bis 1 Uhr'}.get(P0, '21 bis 1 Uhr')   # Zeit vom Plakat des Abends («10 PM TO 1 AM»), sonst die Reihe laut programm.html

FAELLE = [
    dict(nr='01', wann='Gleich nach der Reservierung', ordner='01-reservierung', name='Dein Platz ist reserviert', satz='Kommt gleich nach der Reservierung: Abend, Uhrzeit, Plätze und der Weg zur Ecke Haasemannstraße.',
         betreff='Dein Platz im Wild Side ist reserviert', titel=('Dein Platz', 'ist reserviert.'), foto='theke', bsp=True,
         text=['Hallo Lena', 'Schön, dass ihr kommt. Euer Platz ist reserviert, die Angaben stehen unten.',
               'Die Karte wechselt immer wieder, die Drinks dafür entwirft Momo. An der Bar sagst du einfach, was du magst, sauer, süss, bitter oder rauchig, und daraus wird dein Drink.',
               f'Kommt ihr später oder seid ihr weniger, ruf kurz an: {TEL}.'],
         karte=('Deine Reservierung', [('Abend', 'Freitag, 20. November 2026'), ('Uhrzeit', '20 Uhr'), ('Plätze', '4'), ('Name', 'Lena Wolf')]),
         knopf=WEG, dazu=f"{HAUS['adresse']}, {HAUS['ecke']}. Mit der Stadtbahn bis Am Küchengarten, Linien 9 und 17."),
    dict(nr='02', wann='Gleich nach einer Anfrage für eine Feier', ordner='02-anfrage-feier', name='Eure Anfrage ist da', satz='Kommt gleich nach der Anfrage über «Feiern»: was angefragt ist, und dass Derya und Momo sich mit einem Angebot melden.',
         betreff='Eure Anfrage für eine Feier ist angekommen', titel=('Eure Anfrage', 'ist angekommen.'), foto='an-empore-tafel', bsp=True,
         text=['Hallo Mara', 'Danke für eure Anfrage. Ein Geburtstag an der langen Tafel auf der Empore: Das machen wir gern.',
               'Derya und Momo schauen sich euren Abend an und melden sich in den nächsten Tagen mit einem Angebot, nur für euch. Bis dahin ist nichts fest, ihr müsst nichts tun.',
               f'Fällt euch noch etwas ein, ruf an unter {TEL} oder {TEL2}, oder schreib uns auf Instagram.'],
         karte=('Eure Anfrage', [('Format', 'Die lange Tafel'), ('Datum', 'Samstag, 16. Januar 2027'), ('Wie viele', '16 Gäste'), ('Anlass', 'Geburtstag'), ('Musik dazu', 'DJ')]),
         knopf=('Feiern im Wild Side', 'tafel.html'), dazu='Die lange Tafel gehört eurer Runde vier Stunden lang, unten läuft die Bar weiter.'),
    dict(nr='03', wann='Wenn das Angebot für eine Feier steht', ordner='03-angebot-feier', name='Das Angebot für euren Abend', satz=f'Das Angebot für eine geschlossene Gesellschaft: Pauschale pro Gast mit den Preisen der Bar, Anzahlung, was nach 2 Uhr gilt.',
         betreff='Das Angebot für euren Abend im Wild Side', titel=('Euer Abend,', 'unser Angebot.'), foto='an-party', bsp=True,
         text=['Hallo Tim', f'Danke für das Gespräch. Für eure Weihnachtsfeier mit {GAESTE} Gästen gehört euch die ganze Bar, von 19 bis 2 Uhr: unter der Decke, an der Theke, auf der Empore.',
               f'Wir schlagen die Pauschale Kategorie {KAT} vor: Longdrinks, Bier, Wein, Spritzgetränke, Shots und alkoholfreie Getränke für {PAUSCHALE[KAT]} € pro Person. Mit Bier, Wein und Spritz sind es {PAUSCHALE[1]} €, mit fünf Signature Cocktails dazu {PAUSCHALE[3]} € pro Person.',
               f'Lieber mit Budget? Dann sind es {SERVICE} € für Service und Raum und ein Rahmen für die Drinks ab {BUDGET} €, den ihr selbst setzt.'],
         karte=('Euer Angebot', [('Format', 'Die ganze Bar, 19 bis 2 Uhr'), ('Datum', 'Freitag, 11. Dezember 2026'), ('Gäste', str(GAESTE)), ('Pauschale', f'Kategorie {KAT}, {PAUSCHALE[KAT]} € pro Person'),
                                 ('Zusammen', eur(SUMME)), ('Anzahlung', f'{ANZAHLUNG} %, {eur(SUMME * ANZAHLUNG // 100)}, eine Woche vorher'), ('Nach 2 Uhr', f'je angefangene Stunde {STUNDE} € pro Person')]),
         knopf=('Alle Formate und Preise', 'tafel.html'), dazu='Alle Preise brutto. Passt etwas nicht, sagt es uns, dann bauen wir den Abend um.'),
    dict(nr='04', wann='Am Tag vor der Reservierung', ordner='04-erinnerung', name='Morgen bei uns', satz='Kommt am Tag vor dem reservierten Abend: wann, wie viele, wie man hinfindet, und wen man anruft, wenn sich etwas ändert.',
         betreff='Morgen Abend bei uns im Wild Side', titel=('Morgen Abend', 'an der Ecke.'), foto='schild-ecke', bsp=True,
         text=['Hallo Lena', 'Morgen ist es so weit. Das Schild an der Ecke leuchtet, Momo stellt die Gläser kalt.',
               f'Kommt ihr später oder seid ihr weniger, ruf kurz an unter {TEL}, dann geben wir den Platz nicht weiter.'],
         karte=('Morgen', [('Abend', 'Freitag, 20. November 2026'), ('Uhrzeit', '20 Uhr'), ('Plätze', '4'), ('Name', 'Lena Wolf')]),
         knopf=WEG, dazu=f"{HAUS['adresse']}, {HAUS['ecke']}."),
    dict(nr='05', wann='Am Tag nach dem Abend', ordner='05-danke', name='Danke für den Abend', satz='Kommt am Tag danach: ein Dank, die Zeiten der Bar und der Weg zum Programm der nächsten Wochen.',
         betreff='Danke, dass ihr da wart', titel=('Danke', 'für den Abend.'), foto='anstossen', bsp=False,
         text=['Hallo Lena', 'Schön, dass ihr gestern da wart. Wir hoffen, euer Drink war genau der, den ihr wolltet.',
               'Beim nächsten Mal sag Momo einfach, was dir gestern geschmeckt hat. Er baut darauf weiter auf, die Karte wechselt sowieso.'],
         karte=('Wann wir offen haben', [(t, z) for t, z, _ in HAUS['zeiten']]),
         knopf=('Was als Nächstes läuft', 'programm.html'), dazu=f'Fotos von gestern? Markier uns auf Instagram: {IG}.'),
    dict(nr='06', wann='Vor einem DJ-Abend', ordner='06-session', name='SESSION am Samstag', satz=f'Kommt vor einem DJ-Abend: wer auflegt, wann, und dass es ohne Eintritt ist. Hier mit dem Abend vom {D0}.',
         betreff=f'SESSION am Samstag: {N0}', titel=('Samstag', 'legt jemand auf.'), foto=P0, plakat=True, bsp=False, dj=True,
         text=['Hallo Jonas', f'Am Samstag ist wieder SESSION, Drinks und Musik an einem Abend: Die {N0} legen an der Bar auf' + (f', {R0}.' if R0 else '.'),
               f'Von {MUSIK0}, ohne Eintritt. Momo mixt dazu. Wer zu mehreren kommt, reserviert besser, die Bar ist klein.'],
         karte=('Der Abend', [('Wann', D0_LANG), ('Musik', MUSIK0), ('Am Deck', N0), ('Eintritt', 'frei')]),
         knopf=('Platz reservieren', 'besuch.html#reservieren'), dazu='Den nächsten Abend kündigt die Bar auf Instagram an, mit eigenem Plakat.'),
    dict(nr='07', wann='Nach einem Fest der Bar', ordner='07-rueckblick', name='So war der Geburtstag', satz='Kommt ein paar Tage nach einem Fest: ein Rückblick auf den Geburtstag der Bar und der Weg zu den Fotos auf Instagram.',
         betreff='So war der zweite Geburtstag der Bar', titel=('So war', 'der Geburtstag.'), foto='voll', bsp=False,
         text=['Hallo Jonas', 'Am 5. Dezember 2025 ist die neue Wild Side zwei geworden. Danke, dass ihr mitgefeiert habt.',
               'Mit DJs, mit Mexikanern, dem scharfen Shot des Hauses, und einem Drink zur Begrüssung für die ersten Gäste. Ein paar Fotos stehen jetzt auf Instagram, vielleicht findest du dich wieder.'],
         karte=('Der Abend', [('Datum', '5. Dezember 2025'), ('Geburtstag', 'der zweite'), ('Musik', 'DJs'), ('Im Glas', 'Mexikaner, die ganze Nacht')]),
         knopf=('Fotos auf Instagram', HAUS['instagram']), dazu='Gefällt dir ein Foto besonders, schreib uns auf Instagram.'),
    dict(nr='08', wann='Wenn jemand einen Abend verschenkt', ordner='08-gutschein', name='Ein Abend als Geschenk', satz='Geht an die Beschenkte: wer ihr den Abend schenkt, was er wert ist, bis wann, und der Gutschein als PDF im Anhang.',
         betreff='Ein Abend im Wild Side, für dich', titel=('Ein Abend', 'im Wild Side.'), foto='glas-negroni', bsp=True,
         text=['Hallo Lena', 'Jonas schenkt dir einen Abend im Wild Side: vier Drinks von Momo, an der Theke oder am Tisch.',
               'Den Gutschein findest du im Anhang. Zeig ihn einfach an der Bar, Donnerstag bis Samstag ab 19 Uhr.'],
         karte=('Dein Gutschein', [('Von', 'Jonas Becker'), ('Wert', f'4 Signature Drinks zu je {SIGNATURE} €'), ('Gültig bis', '31. Dezember 2027'), ('Nr.', 'WS-0412')]),
         knopf=('Die Drinks ansehen', 'drinks.html'), dazu=f'Lieber ohne Alkohol? Momo baut jeden Drink auch ohne, zu {OHNE} €.'),
    dict(nr='09', wann='An Stammgäste, vor Silvester', ordner='09-stammgaeste', name='Für dich zuerst', satz='Kommt an Stammgäste vor einem Fest: Silvester ab mittags, und ein Platz an der Theke wird für sie freigehalten.',
         betreff='Silvester bei uns: Wir halten dir einen Platz frei', titel=('Silvester', 'hältst du dir frei.'), foto='silvester', bsp=True,
         text=['Hallo Jonas', 'Du bist oft bei uns, darum fragen wir dich zuerst: Silvester geht es wieder ab mittags los, abends geht es weiter.',
               'Den Mexikaner gibt es die ganze Nacht, Wild-Side-Tradition. Für dich halten wir einen Platz an der Theke frei, bis Sonntag vor Weihnachten.'],
         karte=('Für dich', [('Wann', 'Donnerstag, 31. Dezember 2026'), ('Los geht es', 'ab mittags'), ('Plätze', '2'), ('Frei bis', 'Sonntag, 20. Dezember')]),
         knopf=('Die Feste der Bar', 'programm.html#feste'), dazu=f'Passt es dir nicht, musst du nichts tun. Zusagen per Anruf unter {TEL} oder auf Instagram.'),
    dict(nr='10', wann='Wenn Momo eine neue Karte hat', ordner='10-neue-karte', name='Momos neue Karte', satz='Kommt, wenn die Karte wechselt: was neu ist, wie Momo arbeitet, was ein Drink kostet.',
         betreff='Momo hat eine neue Karte', titel=('Die Karte', 'hat gewechselt.'), foto='momo-giesst', bsp=False,
         text=['Hallo Jonas', 'Die Karte im Wild Side wechselt immer wieder, und jetzt ist es wieder so weit: Momo hat neue Drinks entworfen.',
               'Er arbeitet dafür mit Techniken aus dem Labor. Milk Washing macht einen Drink klar und weich, Fat Washing gibt dem Rum den Geschmack von Kakaobutter, Enzyme machen aus Apfel einen klaren Saft. Und wer lieber einen Negroni will, bekommt ihn.'],
         karte=('Die neue Karte', [('Signature Drinks', f'{SIGNATURE} €'), ('Ohne Alkohol', f'{OHNE} €'), ('Techniken', 'Milk Washing, Fat Washing, Enzyme'), ('Ab', 'Donnerstag, 19 Uhr')]),
         knopf=('Die Drinks ansehen', 'drinks.html'), dazu='Am besten sagst du an der Bar, was du magst. Daraus wird dein Drink.'),
]
FUSSBILD = 'negroni'   # die NEGRONI-Glühbirnen über der Vitrine, ohne Personen (Robert 1.11.2026: kein Teamfoto mit Rudi, er gehört zum Culinarium)


def _alt(key):
    m = re.search(r"'%s':\s*\('[^']*',\s*'([^']*)'\)" % re.escape(key), _BILDER)
    return m.group(1) if m else 'Walk on the Wild Side'


def _bild(key):
    b = sorted(int(m.group(1)) for p in glob.glob(os.path.join(WEB, 'assets', 'bild', key + '-*.webp')) if (m := re.fullmatch(re.escape(key) + r'-(\d+)\.webp', os.path.basename(p))))
    return os.path.join(WEB, 'assets', 'bild', f'{key}-{b[-1]}.webp')


def bilder():
    """Fotos 1000 px im Format 16:9 (Plakate ganz, 600 px breit), unter 100 KB. Alte Bilder im Ordner, die keine Mail mehr braucht, fallen weg."""
    ziel = os.path.join(MAILS, 'img'); os.makedirs(ziel, exist_ok=True)
    brauch = {'marke.png', 'marke-klein.png'}
    for f in FAELLE + [dict(foto=FUSSBILD)]:
        key = f['foto']; z = os.path.join(ziel, key + '.jpg'); brauch.add(key + '.jpg')
        im = Image.open(_bild(key)).convert('RGB'); w, h = im.size
        if f.get('plakat'):
            stufen = ((640, 82), (640, 74), (600, 70), (560, 66))
        else:
            nh = round(w * 9 / 16)
            if nh < h:
                y = round((h - nh) * {'schild-ecke': .55, 'theke': .45, FUSSBILD: .3, 'silvester': .4, 'momo-giesst': .35, 'an-party': .2}.get(key, .5)); im = im.crop((0, y, w, y + nh))
            stufen = ((1000, 80), (1000, 72), (1000, 64), (900, 66), (820, 64), (760, 62))
        for br, qu in stufen:
            k = im.resize((br, round(im.height * br / im.width)), Image.LANCZOS) if br < im.width else im
            k.save(z, quality=qu, optimize=True, progressive=True)
            if os.path.getsize(z) < 100_000:
                break
    for p in os.listdir(ziel):
        if p not in brauch:
            os.remove(os.path.join(ziel, p))


def mail(f, basis, img='../img/'):
    """basis: Adresse der Website, relativ aus dem Ordner der Mail (Vorschau) oder voll (Versand)."""
    zeilen = ''.join(f'<tr><td style="padding:11px 12px 11px 0;border-top:1px solid rgba(216,178,100,.32);font:500 11px/1.35 {SANS};letter-spacing:.14em;text-transform:uppercase;color:{GOLD};width:36%;vertical-align:top">{e(k)}</td>'
                     f'<td style="padding:11px 0;border-top:1px solid rgba(216,178,100,.32);font:400 16px/1.4 {SANS};color:{CREME}">{e(v)}</td></tr>' for k, v in f['karte'][1])
    absaetze = f'<p style="margin:0 0 14px;font:400 21px/1.3 {SERIF};color:{TINTE}">{e(f["text"][0])}</p>' + ''.join(
        f'<p style="margin:0 0 14px;font:400 16px/1.62 {SANS};color:#3B302B">{e(t)}</p>' for t in f['text'][1:])
    href = f['knopf'][1] if f['knopf'][1].startswith('http') else basis + f['knopf'][1]
    if f.get('plakat'):
        foto = f'<img src="{img}{f["foto"]}.jpg" width="300" alt="{e("Plakat des DJ-Abends: " + _alt(f["foto"]))}" style="display:block;border:0;width:300px;max-width:70%;height:auto;margin:0 auto;border-radius:14px;box-shadow:0 18px 30px -18px rgba(19,14,13,.55)">'
    else:
        foto = f'<img src="{img}{f["foto"]}.jpg" width="544" alt="{e(f.get("alt") or _alt(f["foto"]))}" style="display:block;border:0;width:100%;height:auto;border-radius:16px">'
    etikett = f['karte'][0] + (' · Beispielwerte' if f['bsp'] else '')
    knauf = f'<span style="display:inline-block;width:22px;height:22px;margin-left:14px;border-radius:50%;background:{CREME};vertical-align:middle;font:400 13px/22px {SANS};color:{ROT};text-align:center">↗</span>'
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>{e(f['betreff'])} · Walk on the Wild Side</title>
<style>@font-face{{font-family:'Prata';font-weight:400;font-display:swap;src:url('../../assets/schrift/prata-latin.woff2') format('woff2')}}@font-face{{font-family:'Hanken';font-weight:100 900;font-display:swap;src:url('../../assets/schrift/hanken-latin.woff2') format('woff2')}}</style></head>
<body style="margin:0;padding:0;background:{CREME}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{CREME}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:{BLATT};border-radius:18px;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(216,178,100,.45)">
  <tr><td align="center" style="background:{TIEF};padding:34px 30px 32px;border-bottom:1px solid rgba(216,178,100,.55)">
    <img src="{img}marke.png" width="104" alt="Walk on the Wild Side" style="display:block;border:0;width:104px;height:auto;margin:0 auto">
    <h1 style="margin:26px 0 0;font:400 clamp(28px,7.4vw,38px)/1.16 {SERIF};color:{CREME}">{e(f['titel'][0]).replace(' ', '&nbsp;')}<br><span style="color:#CBBBA6">{e(f['titel'][1]).replace(' ', '&nbsp;')}</span></h1>
  </td></tr>
  <tr><td style="padding:34px clamp(22px,6vw,40px) 8px">{absaetze}</td></tr>
  <tr><td style="padding:6px 28px 6px">{foto}</td></tr>
  <tr><td style="padding:12px 28px 6px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{'#1A00AA' if f.get('dj') else NACHT};border-radius:14px;box-shadow:inset 0 0 0 1px rgba(216,178,100,.55)">
    <tr><td style="padding:22px 24px 12px"><div style="font:500 10.5px/1.3 {SANS};letter-spacing:.2em;text-transform:uppercase;color:{GOLD};padding-bottom:12px">{e(etikett)}</div>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{zeilen}</table></td></tr></table></td></tr>
  <tr><td align="center" style="padding:26px 30px 8px"><a href="{href}" style="display:inline-block;padding:9px 9px 9px 24px;border-radius:14px;background:{ROT};font:500 12px/22px {SANS};letter-spacing:.16em;text-transform:uppercase;color:#FFF6EC;text-decoration:none">{e(f['knopf'][0])}{knauf}</a></td></tr>
  <tr><td style="padding:14px 36px 30px"><p style="margin:0;font:400 15px/1.6 {SANS};color:{LEISE};text-align:center">{e(f['dazu'])}</p>
    <img src="{img}{FUSSBILD}.jpg" width="520" alt="{e(_alt(FUSSBILD))}" style="display:block;border:0;width:100%;max-width:520px;height:auto;margin:26px auto 0;border-radius:16px">
    <p style="margin:18px 0 0;font:400 19px/1.4 {SERIF};color:{TINTE};text-align:center">Bis bald an der Bar.<br>{fest(GRUSS)}</p></td></tr>
  <tr><td align="center" style="background:{TIEF};padding:26px 30px;border-top:1px solid rgba(216,178,100,.55)"><div style="font:400 13px/1.7 {SANS};color:#CBBBA6">{e(ADRESSE)}<br>{e(ZEITEN)}<br>{e(TEL)} · {e(IG)}</div></td></tr>
</table>
</td></tr></table>
</body></html>
'''


def eingebettet(f):
    """Die Mail steht direkt in der Seite (Robert 18.10.2026: kein eingebettetes Fenster). Dieselbe Mail wie im Ordner, nur die Bildwege von hier aus."""
    t = mail(f, '../', img='img/')
    t = t[t.index('<body'):]; t = t[t.index('>') + 1:t.rindex('</body>')]
    return t


def fest(t):
    """die letzten zwei Wörter fest verbunden (kein Wort allein in der letzten Zeile)"""
    a, _, b = t.rpartition(' ')
    return e(a) + '&nbsp;' + e(b) if a else e(t)


ZAHLWORT = {10: 'Zehn', 11: 'Elf', 12: 'Zwölf'}


def uebersicht():
    # Robert 18.10.2026 (Website-Master Punkt 15): Mails nebeneinander im Band, obere Hälfte mit weichem Auslauf, «Ganze Mail» auf und zu,
    # Nummer, Titel, Absender und Wann darüber; Pfeile am Laptop, am Handy eine nach der anderen
    pf = lambda d: f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="{d}"/></svg>'
    n = ZAHLWORT.get(len(FAELLE), str(len(FAELLE)))
    karten = ''.join(f'''<article class="mb hr" style="--i:{min(i, 4)}">
  <header class="mb-ueber"><span class="mb-nr">{f['nr']}</span><span class="mb-ueber__t"><b>{fest(f['name'])}</b><small><span>Von</span> Walk on the Wild&nbsp;Side</small><small><span>Wann</span> {fest(f['wann'])}</small><small><span>Betreff</span> {fest(f['betreff'])}</small></span></header>
  <div class="mb-blatt"><div class="mb-in">{eingebettet(f)}</div></div>
  <p class="mb-ganz"><button type="button" class="mb-kn" aria-expanded="false"><span class="a">Ganze Mail</span><span class="z">Weniger zeigen</span><i>{pf('M4 6l4 4 4-4')}</i></button></p>
</article>''' for i, f in enumerate(FAELLE))
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>{n} Mails · Walk on the Wild Side</title>
<style>
@font-face{{font-family:'Prata';font-weight:400;font-display:swap;src:url('../assets/schrift/prata-latin.woff2') format('woff2')}}
@font-face{{font-family:'Hanken';font-weight:100 900;font-display:swap;src:url('../assets/schrift/hanken-latin.woff2') format('woff2')}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:{TIEF};color:{CREME};font:400 17px/1.6 'Hanken','Helvetica Neue',Arial,system-ui,sans-serif;--rand:clamp(20px,4.6vw,76px)}}
header.kopf{{padding:clamp(56px,8vw,120px) var(--rand) clamp(30px,4vw,60px);text-align:center}}
header.kopf .marke{{display:block;width:clamp(58px,5.4vw,84px);height:auto;margin:0 auto;color:{ROT}}}
h1{{margin:clamp(18px,2vw,28px) auto 0;max-width:22ch;font:400 clamp(2rem,4.6vw,4.2rem)/1.1 'Prata',Georgia,serif;text-wrap:balance}}h1 em{{font-style:normal;color:#CBBBA6}}
header.kopf p{{max-width:60ch;margin:clamp(18px,2.1vw,32px) auto 0;color:rgba(242,233,220,.86)}}
main{{padding:0 0 clamp(60px,8vw,120px)}}
.band{{display:flex;gap:clamp(20px,2.4vw,40px);align-items:flex-start;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-inline:var(--rand);padding:4px var(--rand) 34px;scrollbar-width:none;-webkit-overflow-scrolling:touch}}
.band::-webkit-scrollbar{{display:none}}
.band:focus-visible{{outline:2px solid {GOLD};outline-offset:-2px}}
.mb{{flex:0 0 clamp(300px,34vw,520px);scroll-snap-align:start}}
.mb:last-child{{margin-inline-end:var(--rand)}}
.mb-ueber{{display:flex;gap:16px;align-items:flex-start;margin:0 4px 18px}}
.mb-nr{{font:400 2.3rem/.95 'Prata',Georgia,serif;color:{CREME};font-variant-numeric:tabular-nums}}
.mb-ueber__t{{display:flex;flex-direction:column;gap:5px;min-width:0}}
.mb-ueber__t b{{font:400 1.3rem/1.2 'Prata',Georgia,serif}}
.mb-ueber__t small{{font-size:.86rem;line-height:1.4;color:rgba(242,233,220,.76)}}
.mb-ueber__t small span{{display:inline-block;min-width:6.2em;font:500 10px/1.4 'Hanken',Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:{GOLD}}}
.mb-blatt{{position:relative;height:640px;border-radius:18px;overflow:hidden;background:{CREME};box-shadow:0 0 0 1px rgba(216,178,100,.45),0 40px 50px -30px rgba(0,0,0,.9);-webkit-mask-image:linear-gradient(#000 68%,transparent);mask-image:linear-gradient(#000 68%,transparent)}}
.mb.auf .mb-blatt{{-webkit-mask-image:none;mask-image:none}}
.mb-in{{position:relative}}.mb-in table{{max-width:100%}}
.mb-ganz{{position:relative;margin:18px 0 0;text-align:center}}
.mb.auf .mb-ganz{{margin-top:22px}}
.mb-kn{{display:inline-flex;align-items:center;gap:14px;padding:7px 7px 7px 20px;border:0;border-radius:14px;cursor:pointer;font:500 11.5px/1 'Hanken',Arial,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:{CREME};
  background:linear-gradient(180deg,#2E2420 0%,{NACHT} 52%,{TIEF} 100%);box-shadow:inset 0 0 0 1px rgba(216,178,100,.6),inset 0 1px 0 rgba(255,240,220,.12),0 16px 30px -16px rgba(0,0,0,.75)}}
.mb-kn i{{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;color:{NACHT};background:linear-gradient(180deg,#F1D79A,{GOLD} 55%,#B38D45);box-shadow:inset 0 1px 0 rgba(255,255,255,.55)}}
.mb-kn svg{{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}
.mb-kn .z,.mb.auf .mb-kn .a{{display:none}}.mb.auf .mb-kn .z{{display:inline}}.mb.auf .mb-kn svg{{transform:rotate(180deg)}}
.mb-kn:focus-visible{{outline:2px solid {CREME};outline-offset:3px}}
.pfeile{{display:flex;justify-content:center;gap:14px;margin-top:4px}}
.pf{{width:52px;height:52px;border:0;border-radius:50%;cursor:pointer;display:grid;place-items:center;color:{NACHT};background:linear-gradient(180deg,#F1D79A,{GOLD} 55%,#B38D45);box-shadow:inset 0 1px 0 rgba(255,255,255,.6),0 12px 20px -10px rgba(0,0,0,.7)}}
.pf svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}}
.pf:disabled{{opacity:.35;cursor:default}}
footer{{padding:26px var(--rand) 40px;text-align:center;font-size:.92rem;color:rgba(242,233,220,.64);border-top:1px solid rgba(216,178,100,.25)}}
footer a{{color:{CREME}}}
/* Hereinkommen wie auf den anderen Werkbank-Seiten: heben, nur transform und opacity, bei reduced-motion sofort da */
html.js .hr{{opacity:0;transform:translate3d(0,34px,0) scale(.985)}}
html.js .hr.da{{opacity:1;transform:none;transition:opacity .9s cubic-bezier(.2,.7,.2,1) calc(var(--i,0) * 110ms),transform 1.2s cubic-bezier(.16,1,.3,1) calc(var(--i,0) * 110ms)}}
@media (prefers-reduced-motion:reduce){{html.js .hr{{opacity:1;transform:none;transition:none}}}}
@media (max-width:760px){{.mb{{flex-basis:calc(100vw - 2 * var(--rand))}}.pfeile{{display:none}}}}
@media (hover:none){{.pfeile{{display:none}}}}
/* Hanken sitzt im Knopf von selbst mittig (Tor werkbank-mails 31.10.2026); der Ausgleich aus text_mitte.py ist für DM Mono gemacht */
.mb-kn>span{{top:0!important;left:0!important;text-box:trim-both cap alphabetic}}.pf svg{{transform:none!important}}   /* Versalien mittig in Chromium und WebKit (wie knopf_mitte.css) */
</style></head>
<body>
<script>if (!matchMedia('(prefers-reduced-motion:reduce)').matches && 'IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<header class="kopf"><svg class="marke hr" style="--i:0" viewBox="0 0 1296 1600" role="img" aria-label="Walk on the Wild Side"><use href="/assets/oberflaeche/kleid/wildside-marke.svg#wm"/></svg><h1 class="hr" style="--i:1">{n} Mails,<br><em>im Ton der&nbsp;Bar.</em></h1>
<p class="hr" style="--i:2">Was ein Gast nach der Reservierung, nach einer Anfrage für eine Feier oder vor einem DJ-Abend von euch bekommt, kommt im Kleid der neuen Seite. {n} Fälle als Idee, von der Reservierung bis zur neuen Karte von Momo. Namen, Daten und Nummern der Gäste sind Beispielwerte; Preise, Zeiten, Adresse und Abende sind eure.</p></header>
<main><div class="band" id="mband" tabindex="0" aria-label="Die {n.lower()} Mails, zum Blättern">{karten}</div>
<div class="pfeile hr" style="--i:2"><button type="button" class="pf" data-r="-1" aria-label="Vorige Mail">{pf('M10.5 3 5.5 8l5 5')}</button><button type="button" class="pf" data-r="1" aria-label="Nächste Mail">{pf('m5.5 3 5 5-5 5')}</button></div></main>
<footer class="hr">Entwurf von Robert Reff, Tasty Studios. Stand {STAND}. <a href="../werkbank/index.html#papier">Zurück zu «Alles auf einen Blick»</a></footer>
<script>
(function () {{
  /* Hereinkommen: Kopf, Band und Fuss heben sich, sobald sie ins Bild kommen; die Mails im Band kommen zusammen mit dem Band */
  if (document.documentElement.classList.contains('js')) {{
    var io = new IntersectionObserver(function (es) {{ es.forEach(function (e) {{ if (!e.isIntersecting) return; io.unobserve(e.target);
      (e.target.id === 'mband' ? [].slice.call(e.target.querySelectorAll('.hr')) : [e.target]).forEach(function (x) {{ x.classList.add('da'); }}); }}); }}, {{ rootMargin: '0px 0px -8% 0px', threshold: 0 }});
    [].forEach.call(document.querySelectorAll('header.kopf .hr,.pfeile,footer'), function (x) {{ io.observe(x); }}); io.observe(document.getElementById('mband'));
  }}
}})();
(function () {{
  /* die Mail steht in der Seite; zu sieht man den oberen Teil, auf die ganze Mail, sofort */
  var ms = [].slice.call(document.querySelectorAll('.mb'));
  function lage(m) {{ var bl = m.querySelector('.mb-blatt'), i = bl.querySelector('.mb-in'); bl.style.height = (m.classList.contains('auf') ? i.scrollHeight : Math.min(640, i.scrollHeight)) + 'px'; }}
  ms.forEach(function (m) {{
    var k = m.querySelector('.mb-kn');
    [].forEach.call(m.querySelectorAll('img'), function (im) {{ if (!im.complete) im.addEventListener('load', function () {{ lage(m); }}, {{ once: true }}); }});
    lage(m);
    k.addEventListener('click', function () {{ var auf = m.classList.toggle('auf'); k.setAttribute('aria-expanded', auf); lage(m); if (!auf) m.scrollIntoView({{ block: 'nearest' }}); }});
  }});
  var rt = 0; addEventListener('resize', function () {{ clearTimeout(rt); rt = setTimeout(function () {{ ms.forEach(lage); kl(); }}, 120); }});
  /* Pfeile am Laptop blättern das Band um eine Mail */
  var b = document.getElementById('mband'), p = document.querySelectorAll('.pf');
  function schritt() {{ return ms[0].getBoundingClientRect().width + parseFloat(getComputedStyle(b).columnGap || 0); }}
  function kl() {{ p[0].disabled = b.scrollLeft < 4; p[1].disabled = b.scrollLeft > b.scrollWidth - b.clientWidth - 4; }}
  [].forEach.call(p, function (x) {{ x.addEventListener('click', function () {{ b.scrollBy({{ left: +x.dataset.r * schritt(), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }}); }}); }});
  b.addEventListener('scroll', kl, {{ passive: true }}); kl();
}})();
</script>
</body></html>
'''


def main():
    bilder()
    neu = {f['ordner'] for f in FAELLE}
    for p in glob.glob(os.path.join(MAILS, '[0-9][0-9]-*')):   # alte Ordner (Culinarium: 01-ticket … 11-gutschein) fallen weg
        if os.path.basename(p) not in neu and os.path.isdir(p):
            shutil.rmtree(p)
    for f in FAELLE:
        z = os.path.join(MAILS, f['ordner']); os.makedirs(z, exist_ok=True)
        open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(mail(f, '../../'))
    open(os.path.join(MAILS, 'index.html'), 'w', encoding='utf-8').write(uebersicht())
    import sys
    sys.path.insert(0, os.path.join(ROOT, '_werkbank'))
    import papier_nach   # Knopfschrift mittig in Chromium und WebKit (knopf_mitte.css/.js des Papier-Teils, 31.10.2026)
    papier_nach.knopf_mitte(os.path.join(MAILS, 'index.html'))
    json.dump([[f['nr'], f['ordner'], f['name'], f['satz']] for f in FAELLE], open(os.path.join(HIER, 'werkbank.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(FAELLE), 'Mails gebaut:', ', '.join(f['ordner'] for f in FAELLE), '| Angebot', eur(SUMME), '| DJ-Abend', D0, N0)


if __name__ == '__main__':
    main()
