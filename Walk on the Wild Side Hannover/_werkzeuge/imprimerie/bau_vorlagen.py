#!/usr/bin/env python3
"""Die Plakatwerkstatt · Walk on the Wild Side Hannover: Katalog und Vorlagen der Bar.
   python3 bau_vorlagen.py → katalog.js, haeuser/wildside/vorlagen/*.json + index.json, Beispielinhalte in start.js (INHALT) und vorlagen.js (DS.BEISPIEL).
Jeder Satz, jede Zahl, jeder Preis und jeder Termin steht so in der Website der Bar (website/*.html, bau.py LINEUP/HAUS), in CHARAKTER.md oder auf den
echten Plakaten und Beiträgen der Bar (_quelle/ig/beitraege.md, Plakate p-*, wp-*). Nichts ist erfunden; was fehlt (nächster DJ, Uhrzeit Silvester 2026,
Datum des dritten Geburtstags), steht nicht da. Prüfung am Ende: jede Zahl muss in den Quellen vorkommen."""
import json, os, re

HIER = os.path.dirname(os.path.abspath(__file__))
Z = os.path.join(HIER, 'haeuser', 'wildside')
PROJ = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJ, 'website')

ADR = 'Haasemannstraße 13 · 30449 Hannover'
IG = '@walkonthewildside_hannover'
TEL = '+49 163 3909578'
ZEIT = 'Donnerstag 19 bis 1 Uhr · Freitag und Samstag 19 bis 2 Uhr'
ZEILE = 'Eure Nachbarschafts-Mixology-Bar'
PL_FUSS = 'HAASEMANNSTR. 13\n30449 HANNOVER'
S0 = {"ausr": "c", "rahmen": "einfach", "titel": 1, "zeichen": 1, "ecke": 2.4, "bild": 0.56}
S1 = {"ausr": "c", "rahmen": "ohne", "titel": 1.04, "zeichen": .95, "ecke": 2.4, "bild": 0.56}
S2 = {"ausr": "l", "rahmen": "ohne", "titel": 1.1, "zeichen": .85, "ecke": 2.4, "bild": 0.56}

# Die DJ-Abende (website/bau.py LINEUP; Uhrzeit wie auf dem Plakat bzw. im Beitrag, «01 PM» der Plakate als «1 AM» gelesen)
LINEUP = [
    ('17|10', '17.10.2026', 'GHAZOUANI\nBROTHERS', 'Ghazouani Brothers', '10 PM TO 1 AM', 'sw-an-dj', 'welle-1'),
    ('03|10', '03.10.2026', 'JOJO & REZA', 'Jojo & Reza', '9 PM TO 1 AM', 'sw-konzert-love', 'welle-2'),
    ('05|09', '05.09.2026', 'APO', 'Apo', '9 PM TO 1 AM', 'sw-wf-raum', 'welle-3'),
    ('16|05', '16.05.2026', 'JOJO & REZA', 'Jojo & Reza', '9 PM TO 1 AM', 'sw-freundinnen', 'welle-1'),
    ('21|03', '21.03.2026', 'MOURY', 'Moury', '9 PM TO 1 AM', 'sw-anstossen', 'welle-2'),
    ('24|01', '24.01.2026', 'LOVERENCE', 'Loverence', '9 PM TO 1 AM', 'sw-momo-lacht', 'welle-3'),
    ('06|12', '06.12.2025', 'KOLLEKTIV\nGERBER', 'Kollektiv Gerber', '10 PM TO 1 AM', 'sw-pl-theke', 'welle-1'),
    ('22|11', '22.11.2025', 'MOURY', 'Moury', '9 PM TO 1 AM', 'sw-momo-giesst', 'welle-2'),
    ('06|09', '06.09.2025', 'BJÖRN', 'Björn', '8 TO 11 PM', 'sw-an-dj', 'welle-3'),
]


def session(tag, name, zeit, bild, welle):
    return {"bild": bild, "grundbild": welle, "ueber": "SESSION", "unter": "SIP &\nSOUNDS", "name": name, "tag": tag, "zeit": zeit, "fuss": PL_FUSS}


def v(n, wo, fmt, vorlage, ton, inhalt, rueck=None, stil=S0):
    return {"n": n, "wo": wo, "format": fmt, "vorlage": vorlage, "ton": ton, "inhalt": inhalt, "rueck": rueck, "stil": stil}


# ---------------- Abteilungen ----------------
PLAKATE = [
    ('p-1710', 'SESSION · Ghazouani Brothers, 17.10.2026'), ('p-0310', 'SESSION · Jojo & Reza, 03.10.2026'), ('p-0509', 'SESSION · Apo, 05.09.2026'),
    ('p-1605', 'SESSION · Jojo & Reza, 16.05.2026'), ('p-2103', 'SESSION · Moury, 21.03.2026'), ('p-2401', 'SESSION · Loverence, 24.01.2026'),
    ('p-2211', 'SESSION · Moury, 22.11.2025'), ('p-0906', 'SESSION · Björn, 06.09.2025'),
    ('wp-relaunch', 'Relaunch Party, 01.12.2023'), ('wp-silvester24', 'Silvester Frühshoppen, 31.12.2024'), ('wp-mai25', 'Tanz in den Mai, 30.04.2025'),
    ('wp-silvester25', 'Silvester Frühshoppen, 31.12.2025'), ('ja-2025', 'Two Years, 05.12.2025'), ('valentin', 'Wild Side x Rudi in Love, Valentinstag 2026'),
    ('uw-pl-limmer25', 'Christi Limmerfahrt 2025'), ('uw-pl-limmer', 'Christi Limmerfahrt 2026'), ('uw-pl-okt', 'Oktoberfest des Event Klub 2026'),
]
abt_plakate = [v('Plakat · ' + t, 'Instagram, an der Tür, an der Bar', 'insta' if k.startswith('p-') else 'ig11' if not k.startswith(('valentin', 'uw-', 'ja-')) else 'insta', 'plakatganz', 'hell', {"bild": k}) for k, t in PLAKATE]

abt_session = []
for tag, datum, name, nn, zeit, bild, welle in LINEUP:
    abt_session.append(v('SESSION · %s, %s' % (nn, datum), 'Instagram', 'insta', 'plakat', 'session', session(tag, name, zeit, bild, welle), stil=S2))
abt_session += [
    v('SESSION · Aushang A3', 'an der Tür, an der Bar', 'a3h', 'plakat', 'session', session('17|10', 'GHAZOUANI\nBROTHERS', '10 PM TO 1 AM', 'sw-momo-giesst', 'welle-1'), stil=S2),
    v('SESSION · Story', 'Instagram-Story', 'story', 'plakat', 'session', session('17|10', 'GHAZOUANI\nBROTHERS', '10 PM TO 1 AM', 'sw-an-dj', 'welle-3'), stil=S2),
    v('Samstags legt jemand auf', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "an-dj", "ueber": "Samstags · 21 bis 1 Uhr", "titel": "Samstags legt jemand auf.",
      "text": "Rund einmal im Monat legt jemand auf, von 21 bis 1 Uhr. Auf den Plakaten heisst die Reihe SESSION, gemeint sind Drinks und Musik an einem Abend.", "aktion": IG}),
    v('Die DJ-Abende', 'zum Mitnehmen, an der Bar', 'a5h', 'programm', 'dunkel', {"ueber": "SESSION · Sip & Sounds", "titel": "Die DJ-Abende",
      "termine": [{"wann": d, "was": nn, "wo": z.replace(' TO ', ' bis ')} for _, d, _, nn, z, _, _ in LINEUP[:6]]}),
]

FESTE = [
    v('Silvester Frühshoppen', 'Instagram, an der Tür', 'insta', 'plakatrueck', 'hell', {"bild": "silvester", "ueber": ZEILE, "titel": "SILVESTER FRÜHSHOPPEN",
      "tag": "31 | 12 | 25", "zeit": "~ 12:00 - 20:00h", "text": "Drinks @ Momo · Food @ Tru Story · Musik @ Mahir Maulud", "fuss": PL_FUSS}),
    v('Tanz in den Mai', 'Instagram, an der Tür', 'insta', 'plakatrueck', 'hell', {"bild": "fw-a58", "ueber": ZEILE, "titel": "TANZ IN DEN MAI",
      "tag": "30 | 04 | 25", "zeit": "~ 20:00h mit Mahir Maulud", "text": "Mahir Maulud am Deck, Momo an der Bar, Eintritt frei.", "fuss": PL_FUSS}),
    v('Relaunch Party', 'Instagram, an der Tür', 'ig11', 'plakatrueck', 'hell', {"bild": "fw-a12", "ueber": ZEILE, "titel": "RELAUNCH PARTY",
      "tag": "01 | 12 | 23", "zeit": "ab 17 Uhr", "text": "Am 9. November 2023 machen Derya Ivkin und Momo Ben Khelifa die Bar wieder auf.", "fuss": PL_FUSS}),
    v('Der Geburtstag der Bar', 'Instagram, an der Tür', 'insta', 'plakatrueck', 'hell', {"bild": "feste-anstossen", "ueber": ZEILE, "titel": "TWO YEARS",
      "tag": "05 | 12 | 25", "zeit": "", "text": "Mit DJs, Mexikanern und einem Drink zur Begrüssung für die ersten Gäste.", "fuss": PL_FUSS}),
    v('Live am Donnerstag', 'an der Tür, an der Bar', 'a3h', 'plakatrueck', 'hell', {"bild": "konzert-scharf", "ueber": ZEILE, "titel": "LIVE AM DONNERSTAG",
      "tag": "Donnerstags", "zeit": "ab 20 Uhr", "text": "Kleine Konzerte mitten im Raum: Jazz, Soul, Pop. Duos und Trios, ohne Eintritt.", "fuss": PL_FUSS}),
    v('Konzert · Instagram', 'Instagram', 'insta', 'plakatrueck', 'dunkel', {"bild": "saengerin-kunde", "ueber": ZEILE, "titel": "LIVE AM DONNERSTAG",
      "tag": "Donnerstags", "zeit": "ab 20 Uhr", "text": "2024 und 2025 spielten Alone Together, Anissa Al Jay, Josseff and Friends und Sina and Friends.", "fuss": PL_FUSS}),
    v('Valentinstag', 'Instagram', 'insta', 'plakatrueck', 'hell', {"bild": "pf-momo-rudi", "ueber": ZEILE, "titel": "VALENTINSTAG",
      "tag": "14 | 02", "zeit": "", "text": "Mit Rudi von Culinarium: eine Karte mit vier Drinks und Tellern zum Teilen, die es nur an diesem Abend gibt.", "fuss": PL_FUSS}),
    v('Oktoberfest des Event Klub', 'Instagram', 'insta', 'plakatrueck', 'hell', {"bild": "uw-tische", "ueber": ZEILE, "titel": "OKTOBERFEST DES EVENT KLUB",
      "tag": "31 | 10 und 01 | 11 | 26", "zeit": "12 bis 21 Uhr", "text": "Am Stephansplatz. Die Drinks kommen vom Wild Side.", "fuss": PL_FUSS}),
]
GAST = [('02.03.2024', 'Musa', 'Rebe & Brot, Hannover. Mit Momo hinter der Bar.', 'gast-musa'),
        ('09.03.2024', 'Aus dem Havn', 'Eine Bartenderin aus dem Havn in Hannover, mit Momo.', 'gast-havn'),
        ('20.04.2024', 'Nils Lutterbach', 'Lovis, Berlin. Vier Signature Drinks mit Freimeister Kollektiv.', 'gast-nils'),
        ('25.05.2024', 'Cold Drinks and More', 'Ein alter Bekannter aus Berlin mit fünf eigenen Drinks.', 'gast-cold'),
        ('19.10.2024', 'Enlil Arevalo', 'Ein Name der Barszene in Hannover, fünf Signature Drinks.', 'gast-enlil')]
for d, n, t, b in GAST:
    FESTE.append(v('Gastschicht · ' + n, 'Instagram', 'insta', 'plakatrueck', 'hell', {"bild": b, "ueber": "Walk on the Wild Side · Gastschicht", "titel": n.upper(),
                   "tag": d.replace('.', ' | ').replace(' | 20', ' | '), "zeit": "", "text": t, "fuss": PL_FUSS}))

KARTE = [
    v('Drunk in Love · Valentinskarte', 'am Tisch, an der Bar', 'dlh', 'karte', 'creme', {"ueber": "Cupid’s Signature Drinks", "titel": "Drunk in Love", "text": "",
      "liste": [{"name": "Frensh 26", "detail": "Gin | Bergamotte | Nori | Schaumwein", "preis": "12"},
                {"name": "Whey Bramble", "detail": "Gin | Lemon Scrub | Vetiver | Whey Berry Soda", "preis": "12"},
                {"name": "Pink Lady", "detail": "Kakaobutter fat-washed Rum | Himbeerpüree | Agave | Limette", "preis": "12"},
                {"name": "Karamella", "detail": "Havana 7 Jahre | Portwein | Johannisbeere | Karamell | schwarze Walnüsse | Limette", "preis": "12"}],
      "fuss": "Valentinstag 2026 · Walk on the Wild Side"}),
    v('Die Preise der Bar', 'an der Bar', 'a5h', 'karte', 'dunkel', {"ueber": "Was ein Drink kostet", "titel": "Die Preise der Bar", "text": "Alle Preise brutto.",
      "liste": [{"name": "Signature Drinks", "detail": "", "preis": "12,00"}, {"name": "Alkoholfreie Drinks", "detail": "", "preis": "11,00"},
                {"name": "Longdrinks", "detail": "", "preis": "10,00"}, {"name": "Wein und Spritz", "detail": "", "preis": "8,00"},
                {"name": "Sekt auf Eis", "detail": "", "preis": "6,00"}, {"name": "Bier", "detail": "", "preis": "4,00"},
                {"name": "Alkoholfreie Getränke", "detail": "", "preis": "3,00"}], "fuss": ""}),
    v('Die Klassiker', 'am Tisch, an der Bar', 'dlh', 'karte', 'hell', {"ueber": "Auch ohne Frage", "titel": "Die Klassiker", "text": "",
      "liste": [{"name": "Negroni", "detail": "Gin, Wermut, Bitter, auf Eis gerührt.", "preis": ""},
                {"name": "Paloma", "detail": "Tequila, Grapefruit, Limette und Soda.", "preis": ""},
                {"name": "Mexikaner", "detail": "Der scharfe Shot des Hauses, Wild-Side-Tradition.", "preis": ""},
                {"name": "Ohne Alkohol", "detail": "Shrub, Soda, Kräuter, klarer Saft.", "preis": ""}], "fuss": ""}),
    v('Drei Techniken', 'am Tisch', 'a5h', 'karte', 'creme', {"ueber": "Wie Momo arbeitet", "titel": "Aus dem Labor an die Theke.", "text": "",
      "liste": [{"name": "Milk Washing", "detail": "Milch bindet die Trübstoffe und wird wieder abgefiltert. Was bleibt, ist klar wie Wasser und weich wie Sahne.", "preis": ""},
                {"name": "Fat Washing", "detail": "Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel.", "preis": ""},
                {"name": "Enzyme", "detail": "Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt.", "preis": ""}], "fuss": ""}),
    v('Du sagst, was du magst', 'Tischaufsteller', 'a6h', 'buehne', 'dunkel', {"bild": "momo-giesst", "ueber": "An der Theke", "titel": "Du sagst, was du magst.",
      "text": "Die Karte wechselt immer wieder, die Drinks dafür entwirft Momo. Und an der Bar sagst du, was du magst.", "aktion": ""}),
    v('Was magst du?', 'Tischaufsteller', 'a6h', 'karte', 'creme', {"ueber": "Erst die Frage, dann das Glas", "titel": "Was magst du?", "text": "",
      "liste": [{"name": "Der Geschmack", "detail": "Lieber sauer, süss, bitter oder rauchig?", "preis": ""},
                {"name": "Das Glas", "detail": "Klar, cremig oder spritzig?", "preis": ""},
                {"name": "Was hinein soll", "detail": "Gin, Rum, Mezcal, Whisky oder ganz ohne Alkohol?", "preis": ""}], "fuss": ""}),
    v('Der Negroni', 'Instagram', 'insta', 'geteilt', 'dunkel', {"bild": "negroni", "ueber": "Die Klassiker", "titel": "Den Negroni gibt es an jedem Abend.",
      "text": "Der Schriftzug über der Vitrine ist kein Zufall.", "aktion": IG}),
    v('Ohne Alkohol', 'Tischaufsteller', 'a6h', 'aushang', 'creme', {"ueber": "Drinks ohne Alkohol", "titel": "Mit derselben Sorgfalt.",
      "text": "Shrub, Soda, Kräuter, klarer Saft: Momo baut jeden Drink auch ohne Alkohol.", "aktion": ""}),
]

FEIERN = [
    v('Privates Dinner', 'Angebot, zum Mitschicken', 'a5h', 'karte', 'creme', {"ueber": "Mit Rudi und Momo · 10 bis 14 Gäste", "titel": "Privates Dinner", "text": "Für Geburtstage, kleine Weihnachtsfeiern, Junggesellenabschiede oder einen Abend mit den Menschen, die zählen.",
      "liste": [{"name": "Zum Anfang", "detail": "Ein Gruss aus der Küche", "preis": ""}, {"name": "Drei Gänge", "detail": "Ein vegetarisches Menü von Rudi", "preis": ""},
                {"name": "Im Glas", "detail": "Fünf Drinks von Momo, auf die Gänge abgestimmt", "preis": ""}], "fuss": ""}),
    v('Die lange Tafel', 'Angebot, zum Mitschicken', 'a5h', 'buehne', 'dunkel', {"bild": "an-empore-tafel", "ueber": "Mit eigenem Budget · 10 bis 20 Gäste", "titel": "Die Empore gehört euch.",
      "text": "Vier Stunden gehört die lange Tafel eurer Runde, unten läuft die Bar weiter. 0 € für Service und Raum.", "aktion": TEL}),
    v('Die ganze Bar · Pauschale', 'Angebot, zum Mitschicken', 'a5h', 'karte', 'dunkel', {"ueber": "Geschlossene Gesellschaft ab 30 Gästen", "titel": "Eine Nacht, nur für euch.",
      "text": "Von 19 bis 2 Uhr. Ab 2 Uhr jede angefangene Stunde 10 Euro pro Person.",
      "liste": [{"name": "Kategorie 1", "detail": "Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke", "preis": "49 €"},
                {"name": "Kategorie 2", "detail": "Longdrinks · Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke", "preis": "59 €"},
                {"name": "Kategorie 3", "detail": "Fünf Signature Cocktails · Longdrinks · Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke", "preis": "79 €"}], "fuss": "Preis pro Person"}),
    v('Die ganze Bar · Budget', 'Angebot, zum Mitschicken', 'a5h', 'karte', 'creme', {"ueber": "Flexibel mit festem Rahmen", "titel": "Ein Rahmen, den ihr setzt.",
      "text": "Geschlossene Gesellschaft ab 30 Personen, 19 bis 2 Uhr. Das Budget lässt sich nach oben frei anpassen.",
      "liste": [{"name": "Service und Raum", "detail": "", "preis": "500 €"}, {"name": "Euer Budget für Drinks", "detail": "", "preis": "ab 1.000 €"}], "fuss": ""}),
    v('So geht es', 'Angebot, zum Mitschicken', 'a5h', 'programm', 'hell', {"ueber": "Feiern im Wild Side", "titel": "Ihr erzählt, wir bereiten vor.",
      "termine": [{"wann": "Anfragen", "was": "Anlass, Datum, wie viele ihr seid", "wo": ""}, {"wann": "Angebot", "was": "Derya und Momo melden sich mit einem Vorschlag", "wo": ""},
                  {"wann": "Anzahlung", "was": "30 Prozent eine Woche vorher, der Rest am Abend vor Beginn", "wo": ""}, {"wann": "Abend", "was": "Ihr kommt um 19 Uhr, alles ist bereit", "wo": ""}]}),
    v('Euer Abend', 'Instagram', 'insta', 'fenster', 'dunkel', {"bild": "an-party", "ueber": "Feiern im Wild Side", "titel": "Euer Abend.", "unter": TEL,
      "text": "Ein Dinner an der langen Tafel, die ganze Bar für eure Gesellschaft, Musik, die zum Abend passt."}),
    v('Gutschein · Ein Abend an der Bar', 'zum Verschenken', 'dlq', 'gutschein', 'dunkel', {"titel": "Ein Abend an der Bar", "unter": ZEILE, "wert": "",
      "text": "Momo fragt, was du magst, und mixt daraus deinen Drink."}, {"vorlage": "gutscheinrueck", "inhalt": {"text": "Einzulösen an einem Abend nach Wahl, Donnerstag bis Samstag ab 19 Uhr."}}),
]

HAUS = [
    v('Flyer der Bar', 'zum Mitnehmen', 'a6h', 'buehne', 'dunkel', {"bild": "schild", "ueber": "Walk on the Wild Side", "titel": ZEILE + '.',
      "text": "Eine kleine Bar an der Ecke, in der man sich kennt, mit Drinks, für die man sonst weit fahren müsste.", "aktion": ZEIT},
      {"vorlage": "rueckseite", "inhalt": {"text": ZEIT}}),
    v('Öffnungszeiten', 'an der Tür', 'a4h', 'aushang', 'dunkel', {"ueber": "Walk on the Wild Side", "titel": "Bis 2 Uhr.",
      "text": "Donnerstag 19 bis 1 Uhr. Freitag und Samstag 19 bis 2 Uhr. Sonntag bis Mittwoch geschlossen.", "aktion": IG}),
    v('Falstaff Bar Guide 2027', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "decke-raum", "ueber": "Falstaff Bar Guide 2027", "titel": "91 Punkte.",
      "text": "Unter den Cocktailbars: 47 von 50 für die Drinks, 18 von 20 für Stil und Service.", "aktion": IG}),
    v('Derya und Momo', 'Instagram', 'insta', 'fenster', 'creme', {"bild": "derya", "ueber": "Wer hinter der Bar steht", "titel": "Derya und Momo.", "unter": "Seit Herbst 2023",
      "text": "Derya Ivkin führt die Bar, Momo Ben Khelifa entwirft die Drinks."}),
    v('Pressemappe', 'für Medien', 'a4h', 'deckel', 'dunkel', {"ueber": "Pressemappe", "titel": "Walk on the Wild Side", "unter": "Nachbarschafts-Mixology-Bar · Linden-Mitte",
      "text": "Eine kleine Bar an der Ecke Haasemannstraße, mit einem Gewölbe über der Theke, Glühbirnen über der Vitrine und zwei Leuten, die sie seit 2023 führen."}),
    v('Der Weg zur Ecke', 'zum Mitnehmen', 'a6h', 'aushang', 'creme', {"ueber": "Haasemannstraße 13", "titel": "Das Schild an der Ecke leuchtet.",
      "text": "Mit der Stadtbahn bis Am Küchengarten, Linien 9 und 17, dann zwei Minuten zu Fuss. Ecke Rampenstraße.", "aktion": TEL}),
    v('Unter dieser Decke', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "decke-flach", "ueber": "Das Haus", "titel": "Ein Gewölbe über der Theke.", "unter": "Linden-Mitte",
      "text": "Kerzenlicht unter dem Gewölbe, Glühbirnen über der Vitrine."}),
]

ABTEILUNGEN = [
    {"k": "plakate", "t": "Plakate der Bar", "satz": "Jedes Plakat der Bar ganz, wie es war: SESSION, Silvester, Tanz in den Mai, Relaunch.", "foto": "p-1710", "vorlagen": abt_plakate},
    {"k": "session", "t": "SESSION-Plakate", "satz": "Jeder DJ-Abend sein Plakat: rot-cremefarbene Wellen, Ultramarin, das Gesicht des Abends in Schwarzweiss.", "foto": "an-dj", "vorlagen": abt_session},
    {"k": "feste", "t": "Festplakate", "satz": "Die weissen Plakate der Bar: Silvester, Tanz in den Mai, der Geburtstag, Konzerte und Gastschichten.", "foto": "konzert-love", "vorlagen": FESTE},
    {"k": "karte", "t": "Karte & Drinks", "satz": "Die Valentinskarte, die Klassiker, die Preise der Bar und wie Momo arbeitet.", "foto": "glas-coupe", "vorlagen": KARTE},
    {"k": "feiern", "t": "Feiern im Wild Side", "satz": "Privates Dinner, die lange Tafel, die ganze Bar: die Angebote der Bar mit Preisen.", "foto": "an-empore-tafel", "vorlagen": FEIERN},
    {"k": "haus", "t": "Das Haus", "satz": "Die Bar an der Ecke, die Zeiten, der Weg, Derya und Momo, Falstaff.", "foto": "schild", "vorlagen": HAUS},
]

HINWEISE = [
    v('Geschlossene Gesellschaft', 'sofort aushängen', 'a4h', 'aushang', 'dunkel', {"ueber": "Heute Abend", "titel": "Geschlossene Gesellschaft",
      "text": "Heute gehört die Bar einer Runde. Ab Donnerstag sind wir wieder für alle da.", "aktion": ZEIT}),
    v('Die Empore ist reserviert', 'sofort aushängen', 'a4h', 'aushang', 'creme', {"ueber": "Heute Abend", "titel": "Die Empore ist reserviert",
      "text": "Oben feiert heute eine Runde an der langen Tafel, unten läuft der Abend weiter wie immer.", "aktion": ""}),
    v('Eintritt frei', 'sofort aushängen', 'a5h', 'aushang', 'hell', {"ueber": "Konzerte und DJ-Abende", "titel": "Ohne Eintritt.",
      "text": "Konzerte und DJ-Abende sind ohne Eintritt.", "aktion": IG}),
    v('Ab 19 Uhr', 'an der Tür', 'a6h', 'aushang', 'dunkel', {"ueber": "Donnerstag bis Samstag", "titel": "Ab 19 Uhr",
      "text": "Donnerstag bis 1 Uhr, Freitag und Samstag bis 2 Uhr.", "aktion": ""}),
    v('Reservieren', 'an der Bar', 'a6h', 'aushang', 'creme', {"ueber": "Die Bar ist klein", "titel": "Ein Platz für euch.",
      "text": "Wer zu mehreren kommt, reserviert besser. Die Bar bestätigt per Nachricht.", "aktion": TEL}),
    v('Draussen an der Ecke', 'an der Tür', 'a5h', 'aushang', 'hell', {"ueber": "Wenn es warm ist", "titel": "Draussen an der Ecke.",
      "text": "Wenn es warm ist, stehen Tische vor der Tür an der Ecke.", "aktion": ""}),
]

NEWSLETTER = [
    v('Der nächste DJ-Abend', 'an alle Gäste', 'mail', 'fenster', 'dunkel', {"bild": "an-dj", "ueber": "SESSION · Sip & Sounds", "titel": "Samstags legt jemand auf.", "unter": "21 bis 1 Uhr",
      "text": "Rund einmal im Monat legt jemand auf. Den nächsten Abend kündigt die Bar auf Instagram an."}),
    v('Feiern im Wild Side', 'an Anfragen', 'mail', 'aushang', 'creme', {"ueber": "Feiern im Wild Side", "titel": "Euer Abend.",
      "text": "Ein Dinner an der langen Tafel, die ganze Bar für eure Gesellschaft, Musik, die zum Abend passt.", "aktion": TEL}),
    v('Gute Drinks, gute Musik', 'an die Gäste', 'mail', 'deckel', 'creme', {"ueber": "Walk on the Wild Side", "titel": "Gute Drinks, gute Musik.",
      "unter": ZEIT, "text": "Donnerstags spielt ab und zu jemand live, samstags legen DJs auf, und manchmal steht ein Gast aus einer anderen Bar neben Momo."}),
    v('Kopfbild Bar', 'über jeder E-Mail', 'mailkopf', 'ansicht', 'dunkel', {"bild": "negroni", "titel": "Walk on the Wild Side", "unter": "Hannover-Linden"}),
    v('Kopfbild Decke', 'über jeder E-Mail', 'mailkopf', 'ansicht', 'dunkel', {"bild": "decke-flach", "titel": "Walk on the Wild Side", "unter": "Linden-Mitte"}),
    v('Story: Was magst du?', 'Instagram', 'story', 'fenster', 'dunkel', {"bild": "momo-giesst", "ueber": "An der Theke", "titel": "Was magst du?", "unter": "Momo Ben Khelifa",
      "text": "«Du sagst mir, was du magst, ich mache dir einen Drink.»"}),
]

# ---------------- Anlässe & Events (nur, was die Bar ankündigt oder was jedes Jahr kommt) ----------------
ANLAESSE = [
    {"k": "oktoberfest-2026", "t": "Oktoberfest des Event Klub", "z": "31. Oktober – 1. November", "von": "2026-10-31", "bis": "2026-11-01", "wo": "stadt",
     "ort": "Stephansplatz, 12 bis 21 Uhr", "satz": "Oktoberfest des Event Klub am Stephansplatz, 12 bis 21 Uhr, die Drinks kommen vom Wild Side.", "fotos": ["uw-tische", "uw-pl-okt", "uw-glas"]},
    {"k": "session", "t": "SESSION am Samstag", "z": "samstags", "von": "2025-09-06", "bis": "2027-12-31", "wo": "haus", "ort": "Walk on the Wild Side · 21 bis 1 Uhr",
     "satz": "Rund einmal im Monat legt jemand auf, von 21 bis 1 Uhr. Den nächsten Abend kündigt die Bar auf Instagram an.", "fotos": ["an-dj", "p-1710", "sw-an-dj"]},
    {"k": "geburtstag", "t": "Der Geburtstag der Bar", "z": "im Winter", "von": "2026-11-01", "bis": "2026-12-31", "wo": "haus", "ort": "Walk on the Wild Side · Termin auf Instagram",
     "satz": "Am 30. November 2024 wurde die neue Wild Side eins, am 5. Dezember 2025 zwei. Mit DJs, Mexikanern und einem Drink zur Begrüssung für die ersten Gäste.", "fotos": ["feste-anstossen", "ja-2025", "an-party"]},
    {"k": "silvester-2026", "t": "Silvester ab mittags", "z": "31. Dezember", "von": "2026-12-31", "bis": "2026-12-31", "wo": "haus", "ort": "Walk on the Wild Side",
     "satz": "2024 als Frühschoppen von 12 bis 19 Uhr mit Buffet, 2025 von 12 bis 20 Uhr mit dem Foodtruck von Tru Story vor der Tür. Abends geht es weiter.", "fotos": ["silvester", "wp-silvester25", "an-party"]},
    {"k": "valentin-2027", "t": "Valentinstag", "z": "14. Februar", "von": "2027-02-14", "bis": "2027-02-14", "wo": "haus", "ort": "Walk on the Wild Side",
     "satz": "Mit Rudi von Culinarium: eine Karte mit vier Drinks und Tellern zum Teilen, die es nur an diesem Abend gibt.", "fotos": ["pf-momo-rudi", "karte-love", "valentin"]},
    {"k": "mai-2027", "t": "Tanz in den Mai", "z": "30. April", "von": "2027-04-30", "bis": "2027-04-30", "wo": "haus", "ort": "Walk on the Wild Side",
     "satz": "Mahir Maulud am Deck, Momo an der Bar, Eintritt frei. Wenn es warm ist, stehen die Tische vor der Tür.", "fotos": ["fw-a58", "wp-mai25", "fw-h31"]},
]
MOTIVE = {
    "oktoberfest-2026": [
        FESTE[7],
        v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "uw-glas", "ueber": "31.10. und 01.11.2026", "titel": "Oktoberfest des Event Klub", "unter": "Stephansplatz · 12 bis 21 Uhr", "text": "Die Drinks kommen vom Wild Side."}),
        v('Aushang an der Bar', 'an der Bar', 'a4h', 'aushang', 'creme', {"ueber": "Die Bar ausser Haus", "titel": "Oktoberfest des Event Klub", "text": "31.10. und 01.11.2026 am Stephansplatz, 12 bis 21 Uhr. Die Drinks kommen vom Wild Side.", "aktion": IG}),
        v('Beitrag', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "uw-tische", "ueber": "Die Bar ausser Haus", "titel": "Und manchmal draussen.", "text": "Ein paar Mal im Jahr steht die Bar vor der Tür oder ganz woanders.", "aktion": IG}),
    ],
    "session": abt_session[:2] + [abt_session[9], abt_session[10], abt_session[11], abt_session[12]],
    "geburtstag": [
        FESTE[3],
        v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "feste-anstossen", "ueber": "Der Geburtstag der Bar", "titel": "Die Bar hat Geburtstag.", "unter": "Mit DJs und Mexikanern", "text": "Ein Drink zur Begrüssung für die ersten Gäste."}),
        v('Aushang an der Bar', 'an der Bar', 'a4h', 'aushang', 'dunkel', {"ueber": "Im Winter", "titel": "Der Geburtstag der Bar", "text": "Mit DJs, Mexikanern und einem Drink zur Begrüssung für die ersten Gäste.", "aktion": IG}),
        v('Beitrag', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "an-party", "ueber": "Der Geburtstag der Bar", "titel": "Mexikaner all night long.", "text": "An Geburtstagen der Bar gibt es den Mexikaner die ganze Nacht, Wild-Side-Tradition.", "aktion": IG}),
    ],
    "silvester-2026": [
        FESTE[0],
        v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "silvester", "ueber": "31. Dezember", "titel": "Silvester ab mittags.", "unter": "Walk on the Wild Side", "text": "Abends geht es weiter."}),
        v('Aushang an der Bar', 'an der Bar', 'a4h', 'aushang', 'creme', {"ueber": "31. Dezember", "titel": "Silvester ab mittags.", "text": "Mit Frühschoppen, Musik und dem Mexikaner, Wild-Side-Tradition. Abends geht es weiter.", "aktion": IG}),
        v('Beitrag', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "an-party", "ueber": "Last Day of 2025", "titel": "Let’s go wild.", "text": "Silvester entspannt, laut und lecker, genau so, wie ihr es liebt.", "aktion": IG}),
    ],
    "valentin-2027": [
        FESTE[6], KARTE[0],
        v('Story', 'Instagram-Story', 'story', 'fenster', 'creme', {"bild": "karte-love", "ueber": "14. Februar", "titel": "Drunk in Love.", "unter": "Wild Side x Rudi in Love", "text": "Vier Drinks und Teller zum Teilen, nur an diesem Abend."}),
        v('Beitrag', 'Instagram', 'insta', 'geteilt', 'dunkel', {"bild": "pf-momo-rudi", "ueber": "Valentinstag", "titel": "Momo und Rudi am Valentinsabend.", "text": "Eine Karte mit vier Drinks und Tellern zum Teilen.", "aktion": IG}),
    ],
    "mai-2027": [
        FESTE[1],
        v('Story', 'Instagram-Story', 'story', 'fenster', 'dunkel', {"bild": "fw-a58", "ueber": "30. April", "titel": "Tanz in den Mai.", "unter": "Eintritt frei", "text": "Mahir Maulud am Deck, Momo an der Bar."}),
        v('Aushang an der Bar', 'an der Bar', 'a4h', 'aushang', 'creme', {"ueber": "30. April", "titel": "Tanz in den Mai", "text": "Mahir Maulud am Deck, Momo an der Bar, Eintritt frei. Wenn es warm ist, stehen die Tische vor der Tür.", "aktion": IG}),
        v('Beitrag', 'Instagram', 'insta', 'buehne', 'dunkel', {"bild": "fw-h31", "ueber": "Tanz in den Mai", "titel": "Die Tische stehen vor der Tür.", "text": "Wenn es warm ist, läuft der Abend draussen an der Ecke weiter.", "aktion": IG}),
    ],
}

# ---------------- Beispielinhalte je Aufbau (DS.BEISPIEL) und je Art (INHALT) ----------------
BEISPIEL = {
    "deckel": {"ueber": "Walk on the Wild Side", "titel": ZEILE, "unter": ADR, "text": "Die Drinks entwirft Momo, die Karte wechselt immer wieder, und an der Bar sagst du, was du magst."},
    "buehne": {"bild": "momo-giesst", "ueber": "An der Theke", "titel": "Du sagst, was du magst.", "text": "Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll. Daraus wird ein Drink.", "aktion": ADR},
    "ansicht": {"bild": "schild", "titel": "Walk on the Wild Side", "unter": "Hannover-Linden"},
    "karte": KARTE[2]["inhalt"],
    "einladung": {"ueber": "Feiern im Wild Side", "titel": "Ein Abend, der nur euch gehört.", "wann": "Von 19 bis 2 Uhr", "wo": ADR, "text": "Ab dreissig Gästen schliesst die Bar für euch: unter der Decke, an der Theke, auf der Empore.", "aktion": TEL},
    "programm": abt_session[12]["inhalt"],
    "fenster": {"bild": "decke-raum", "ueber": "Das Haus", "titel": "Unter dieser Decke.", "unter": "Linden-Mitte", "text": "Eine kleine Bar an der Ecke, mit einem Gewölbe über der Theke und Glühbirnen über der Vitrine."},
    "geteilt": {"bild": "schaum", "ueber": "Wie Momo arbeitet", "titel": "Fat Washing", "text": "Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel.", "aktion": "Walk on the Wild Side"},
    "gutschein": {"titel": "Ein Abend an der Bar", "unter": ZEILE, "wert": "", "text": "Momo fragt, was du magst, und mixt daraus deinen Drink."},
    "aushang": HINWEISE[4]["inhalt"],
    "rueckseite": {"text": ZEIT},
    "kartengruss": {"titel": "Walk on the Wild Side", "text": "Du sagst, was du magst."},
    "plakat": session('17|10', 'GHAZOUANI\nBROTHERS', '10 PM TO 1 AM', 'sw-an-dj', 'welle-1'),
    "plakathoch": session('17|10', 'GHAZOUANI\nBROTHERS', '10 PM TO 1 AM', 'sw-an-dj', 'welle-2'),
    "plakatrueck": FESTE[0]["inhalt"],
    "plakatganz": {"bild": "p-1710"},
    "menue": {"titel": "Drunk in Love", "ueber": "Valentinstag 2026", "liste": [{"gang": "12", "name": l["name"], "detail": l["detail"]} for l in KARTE[0]["inhalt"]["liste"]], "fuss": "Walk on the Wild Side · " + ADR},
}
INHALT = {
    "abendplakat": {"plakat": BEISPIEL["plakat"]},
    "plakat": {"plakatrueck": FESTE[4]["inhalt"], "buehne": {"bild": "konzert-love", "ueber": "Donnerstags · ab 20 Uhr", "titel": "Live am Donnerstag.", "text": "Kleine Konzerte mitten im Raum: Jazz, Soul, Pop. Ohne Eintritt.", "aktion": IG}},
    "getraenke": {"karte": KARTE[0]["inhalt"], "menue": BEISPIEL["menue"], "deckel": {"ueber": "Die Karte", "titel": "Was magst du?", "unter": ZEILE, "text": "Die Karte wechselt immer wieder, die Drinks dafür entwirft Momo."}},
    "flyer": {"buehne": HAUS[0]["inhalt"]},
    "tisch": {"buehne": KARTE[4]["inhalt"], "karte": KARTE[5]["inhalt"]},
    "instagram": {"geteilt": KARTE[6]["inhalt"], "buehne": HAUS[2]["inhalt"]},
    "tischkarte": {"deckel": {"ueber": "Die Empore", "titel": "Reserviert", "unter": "Walk on the Wild Side", "text": ""}},
    "hinweiskarte": {"aushang": HINWEISE[5]["inhalt"]},
    "stoerung": {"aushang": HINWEISE[0]["inhalt"]},
    "pressemappe": {"deckel": HAUS[4]["inhalt"]},
    "story": {"fenster": NEWSLETTER[5]["inhalt"]},
    "aushang": {"aushang": HAUS[1]["inhalt"]},
    "einladung": {"einladung": BEISPIEL["einladung"]},
    "programm": {"programm": abt_session[12]["inhalt"]},
}

# ---------------- Bibliothek je Art (vorlagen/<art>.json) ----------------
ART_FORMAT = {"abendplakat": "insta", "plakat": "a3h", "getraenke": "dlh", "flyer": "a6h", "tisch": "a6h", "instagram": "insta", "tischkarte": "a7q", "hinweiskarte": "a6h",
              "stoerung": "a4h", "pressemappe": "a4h", "story": "story", "aushang": "a4h", "einladung": "q148", "programm": "a5h", "newsletter": "mail", "gutschein": "dlq"}
GRUPPE_NAME = {"abendplakat": "SESSION-Plakat", "plakat": "Plakat und Pressemappe", "pressemappe": "Plakat und Pressemappe", "getraenke": "Getränkekarte", "flyer": "Flyer und Programm",
               "programm": "Flyer und Programm", "tisch": "Tischaufsteller", "instagram": "Instagram und Newsletter", "newsletter": "Instagram und Newsletter", "tischkarte": "Tischkarte",
               "hinweiskarte": "Hinweiskarte", "stoerung": "Aushang und Hinweise", "aushang": "Aushang und Hinweise", "story": "Story", "einladung": "Einladung und Gutschein",
               "gutschein": "Einladung und Gutschein"}
BIB = {k: [] for k in ART_FORMAT}


def neu(art, titel, bereich, x, fmt=None):
    BIB[art].append({"id": "%s-%03d" % (art, len(BIB[art]) + 1), "titel": titel, "bereich": bereich, "vorlage": x["vorlage"], "ton": x["ton"], "stil": x["stil"],
                     "inhalt": x["inhalt"], "rueck": x["rueck"], **({"format": fmt} if fmt else {})})


for x in abt_session[:9]:
    neu('abendplakat', x["n"].replace('SESSION · ', 'SESSION mit '), 'SESSION', x)
for x in abt_session[9:11]:
    neu('abendplakat', x["n"], 'SESSION', x, x["format"])
for x in FESTE:
    neu('plakat', x["n"], 'Feste', x)
for x in KARTE[:4]:
    neu('getraenke', x["n"], 'Karte', x)
for x in FEIERN[:5]:
    neu('flyer' if x["vorlage"] != 'programm' else 'programm', x["n"], 'Feiern', x)
neu('flyer', HAUS[0]["n"], 'Haus', HAUS[0])
neu('programm', abt_session[12]["n"], 'SESSION', abt_session[12])
for x in [KARTE[4], KARTE[5], KARTE[7], HINWEISE[3], HINWEISE[4]]:
    neu('tisch', x["n"], 'Karte' if x in KARTE else 'Hinweise', x)
for x in [KARTE[6], HAUS[2], HAUS[3], FEIERN[5], abt_session[11]] + [m for k in ('oktoberfest-2026', 'geburtstag', 'silvester-2026', 'mai-2027') for m in MOTIVE[k] if m["n"] == 'Beitrag']:
    neu('instagram', x["n"], 'Instagram', x)
for t, u in [('Reserviert', 'Die Empore'), ('Reserviert', 'An der Theke'), ('Die lange Tafel', 'Feiern im Wild Side'), ('Willkommen', 'Walk on the Wild Side')]:
    neu('tischkarte', t + ' · ' + u, 'Feiern', v(t, '', 'a7q', 'deckel', 'dunkel' if len(BIB['tischkarte']) % 2 else 'creme', {"ueber": u, "titel": t, "unter": "", "text": ""}))
for x in [HINWEISE[1], HINWEISE[2], HINWEISE[5], HAUS[5]]:
    neu('hinweiskarte', x["n"], 'Hinweise', x)
for x in [HINWEISE[0]]:
    neu('stoerung', x["n"], 'Hinweise', x)
for x in [HAUS[1], HINWEISE[2], MOTIVE['oktoberfest-2026'][2], MOTIVE['geburtstag'][2], MOTIVE['silvester-2026'][2], MOTIVE['mai-2027'][2]]:
    neu('aushang', x["n"], 'Hinweise', x)
neu('pressemappe', HAUS[4]["n"], 'Haus', HAUS[4])
neu('pressemappe', 'Pressemappe · Falstaff', 'Haus', v('Pressemappe', '', 'a4h', 'deckel', 'creme', {"ueber": "Falstaff Bar Guide 2027", "titel": "91 Punkte", "unter": "Cocktailbars", "text": "47 von 50 für die Drinks, 18 von 20 für Stil und Service."}))
for x in [NEWSLETTER[5], HAUS[6], abt_session[10]] + [m for k in MOTIVE for m in MOTIVE[k] if m["n"] == 'Story']:
    neu('story', x["n"], 'Story', x, x["format"] if x["vorlage"] == 'plakat' else None)
for x in NEWSLETTER:
    neu('newsletter', x["n"], 'Newsletter', x, x["format"])
neu('einladung', 'Einladung · Die ganze Bar', 'Feiern', v('Einladung', '', 'q148', 'einladung', 'dunkel', BEISPIEL["einladung"]))
neu('einladung', 'Einladung · Privates Dinner', 'Feiern', v('Einladung', '', 'q148', 'einladung', 'creme', {"ueber": "Mit Rudi und Momo", "titel": "Privates Dinner", "wann": "10 bis 14 Gäste", "wo": ADR, "text": "Ein exklusiver Abend an der langen Tafel, mit Rudi in der Küche und Momo an der Bar.", "aktion": TEL}))
neu('gutschein', FEIERN[6]["n"], 'Feiern', FEIERN[6])
neu('gutschein', 'Gutschein · hell', 'Feiern', v('Gutschein', '', 'dlq', 'gutschein', 'hell', FEIERN[6]["inhalt"], FEIERN[6]["rueck"]))


def schreiben():
    vd = os.path.join(Z, 'vorlagen'); os.makedirs(vd, exist_ok=True)
    for f in os.listdir(vd):
        if f.endswith('.json'):
            os.remove(os.path.join(vd, f))
    index = []
    for art, l in BIB.items():
        if not l:
            continue
        json.dump({"art": art, "format": ART_FORMAT[art], "vorlagen": l}, open(os.path.join(vd, art + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        index.append({"art": art, "format": ART_FORMAT[art], "zahl": len(l), "gruppe": GRUPPE_NAME[art]})
    json.dump(index, open(os.path.join(vd, 'index.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
    kat = ("/* Die Plakatwerkstatt · Walk on the Wild Side Hannover · Katalog der Bar. GESCHRIEBEN VON bau_vorlagen.py, nicht von Hand ändern.\n"
           "   Fertig gesetzte Vorlagen nur aus dem, was die Bar selbst sagt (Website, Plakate, Beiträge); jede öffnet ohne KI und ohne Kosten. */\n(function () {\n"
           f"  const ABTEILUNGEN = {J(ABTEILUNGEN)};\n  const HINWEISE = {J(HINWEISE)};\n  const NEWSLETTER = {J(NEWSLETTER)};\n  const ANLAESSE = {J(ANLAESSE)};\n"
           f"  const MOTIVE = {J(MOTIVE)};\n  const motive = a => MOTIVE[a.k] || [];\n  window.DSKATALOG = {{ ABTEILUNGEN, HINWEISE, ANLAESSE, motive, NEWSLETTER }};\n}})();\n")
    open(os.path.join(HIER, 'katalog.js'), 'w', encoding='utf-8').write(kat)
    s = open(os.path.join(HIER, 'start.js'), encoding='utf-8').read()
    s = re.sub(r'  const INHALT = \{.*?\};\n', lambda m: '  const INHALT = ' + json.dumps(INHALT, ensure_ascii=False) + ';\n', s, count=1, flags=re.S)
    open(os.path.join(HIER, 'start.js'), 'w', encoding='utf-8').write(s)
    s = open(os.path.join(HIER, 'vorlagen.js'), encoding='utf-8').read()
    s = re.sub(r'  DS\.BEISPIEL = \{.*?\};\n', lambda m: '  DS.BEISPIEL = ' + json.dumps(BEISPIEL, ensure_ascii=False) + ';\n', s, count=1, flags=re.S)
    open(os.path.join(HIER, 'vorlagen.js'), 'w', encoding='utf-8').write(s)
    n = sum(len(l) for l in BIB.values())
    print('Vorlagen:', n, 'in', len(index), 'Arten ·', sum(len(a["vorlagen"]) for a in ABTEILUNGEN), 'in Abteilungen ·', len(ANLAESSE), 'Anlässe')


def pruefen():
    """Jede Zahl der Texte muss in den Quellen stehen (Website, Beiträge, Plakat-Listen hier im Skript)."""
    q = ''
    for f in ('index.html', 'drinks.html', 'programm.html', 'tafel.html', 'besuch.html', 'haus.html', 'bau.py'):
        p = os.path.join(WEB, f)
        if os.path.exists(p):
            q += open(p, encoding='utf-8').read()
    for p in (os.path.join(PROJ, '_quelle', 'ig', 'beitraege.md'), os.path.join(PROJ, 'CHARAKTER.md')):
        if os.path.exists(p):
            q += open(p, encoding='utf-8').read()
    q = q.replace('&nbsp;', ' ')
    texte = json.dumps([ABTEILUNGEN, HINWEISE, NEWSLETTER, ANLAESSE, MOTIVE], ensure_ascii=False)
    erlaubt = {'26', '25', '24', '23', '27', '2026', '2025', '2024', '2023', '2027', '13', '30449', '12', '9', '17', '01', '02', '03', '04', '05', '06', '10', '11', '14', '16', '20', '21', '22', '31', '7', '1', '2', '3', '4', '8', '0', '163', '3909578', '49', '15'}
    fehl = sorted({z for z in re.findall(r'\d+', texte) if z not in erlaubt and z not in q})
    if fehl:
        print('NICHT BELEGT:', fehl)


if __name__ == '__main__':
    pruefen()
    schreiben()
