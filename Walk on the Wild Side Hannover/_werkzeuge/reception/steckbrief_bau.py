#!/usr/bin/env python3
"""Steckbrief für «Das weiss der Chat» von Walk on the Wild Side Hannover (31.10.2026, Kopie des Bauskripts des Culinarium).

Jede Zeile: Stichwort, Angabe, Beleg. Der Beleg ist eine Stelle, die wörtlich in `gast/gast_wissen.txt` (Wortlaut der Website) oder
`gast/gast_umgebung.txt` (Kontaktwege, Anzahlung, Lage) steht; dieses Skript bricht ab, wenn ein Beleg dort nicht vorkommt
oder eine Zahl der Angabe nicht im Umfeld des Belegs steht (nichts abgetippt oder verschönert).
Bewusst NICHT im Steckbrief, weil die Quellen es nicht sagen: Allergien (der Chat gibt die Frage an das Team, beim Dinner klärt es Rudi), Hunde, Kinder,
Barrierefreiheit, Parkplätze, eine E-Mail-Adresse der Bar, der Preis des Privaten Dinners, das Datum des nächsten DJ-Abends (kündigt die Bar auf Instagram an).
«Veranstaltungen» und «Fragen & Antworten» füllt das Team selbst.
Ergebnis: steckbrief.json daneben, gelesen von gedaechtnis.py. Nach jedem neuen Wissen (python3 _bau/wildside_wissen.py) erneut laufen lassen.
Aufruf: python3 _werkzeuge/reception/steckbrief_bau.py"""
import hashlib, json, os, re, sys

HIER = os.path.dirname(os.path.abspath(__file__))
WISSEN = os.path.join(HIER, 'gast')
DATEIEN = ('gast_wissen.txt', 'gast_umgebung.txt')

# Bereich → Gruppen → Zeilen (Stichwort, Angabe, Beleg)
S = [
 ('Die Bar', [
  ('Auf einen Blick', [
   ('Was es ist', 'eine Nachbarschafts-Mixology-Bar in Linden-Mitte', 'Eine Nachbarschafts-Mixology-Bar in Linden-Mitte.'),
   ('Die Karte', 'wechselt immer wieder, die Drinks dafür entwirft Momo; an der Bar sagst du, was du magst', 'Die Karte im Wild Side wechselt immer wieder, die Drinks dafür entwirft Momo. Und an der Bar sagst du, was du magst.'),
   ('Wer', 'Derya Ivkin führt die Bar, Momo Ben Khelifa mixt', 'Derya Ivkin führt die Bar, Momo Ben Khelifa mixt'),
   ('Falstaff', 'Bar Guide 2027: 91 Punkte unter den Cocktailbars, 47 von 50 für die Drinks', 'Im Falstaff Bar Guide 2027 steht das Wild Side mit 91 Punkten unter den Cocktailbars: 47 von 50 für die Drinks.'),
   ('Gäste', 'bei Google im Schnitt 4,8 von 5 aus 75 Bewertungen', 'Bei Google geben 75 Gäste im Schnitt 4,8 von 5.'),
  ]),
 ]),
 ('Zeiten & Reservieren', [
  ('Geöffnet', [
   ('Donnerstag', '19 bis 1 Uhr', 'Donnerstag 19 bis 1 Uhr'),
   ('Freitag und Samstag', '19 bis 2 Uhr', 'Freitag und Samstag 19 bis 2 Uhr'),
   ('Geschlossen', 'Sonntag bis Mittwoch', 'Sonntag bis Mittwoch'),
  ]),
  ('Reservieren', [
   ('Lohnt sich', 'die Bar ist klein: wer zu mehreren kommt, reserviert besser', 'Die Bar ist klein. Wer zu mehreren kommt, reserviert besser, direkt hier: Platz reservieren.'),
   ('So geht es', '«Platz reservieren» auf der Seite Besuch: Abend, Uhrzeit, Plätze, Name, Telefon oder E-Mail; die Bar bestätigt per Nachricht', 'Reservieren: mit «Platz reservieren» auf der Seite Besuch (Abend, Uhrzeit, Plätze, Name, Telefon oder E-Mail).', 'Die Bar bestätigt per Nachricht.'),
   ('Viele Gäste', 'ab zehn Gästen gibt es die lange Tafel, ab dreissig die ganze Bar', 'Ab zehn Gästen gibt es die lange Tafel, ab dreissig die ganze Bar: alles unter Feiern.'),
  ]),
 ]),
 ('Drinks & Preise', [
  ('Wie Momo arbeitet', [
   ('Das Gespräch', 'Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll; daraus wird ein Drink', 'So läuft es an der Theke: Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll. Daraus wird ein Drink.'),
   ('Milk Washing', 'Milch bindet die Trübstoffe und wird wieder abgefiltert: klar wie Wasser, weich wie Sahne', 'Milch bindet die Trübstoffe und wird wieder abgefiltert. Was bleibt, ist klar wie Wasser und weich wie Sahne.'),
   ('Fat Washing', 'ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel', 'Ein Fett gibt seinen Geschmack an die Spirituose ab, Kakaobutter an Rum zum Beispiel.'),
   ('Enzyme', 'lösen die Trübung aus Fruchtsaft, der Geschmack bleibt', 'Enzyme lösen die Trübung aus Fruchtsaft, der Geschmack bleibt.'),
  ]),
  ('Die Klassiker', [
   ('Negroni', 'Gin, Wermut, Bitter, auf Eis gerührt; an jedem Abend', 'Gin, Wermut, Bitter, auf Eis gerührt.', 'Den Negroni gibt es an jedem Abend.'),
   ('Paloma', 'Tequila, Grapefruit, Limette und Soda', 'Tequila, Grapefruit, Limette und Soda.'),
   ('Mexikaner', 'der scharfe Shot des Hauses, Wild-Side-Tradition', 'Der scharfe Shot des Hauses.'),
   ('Ohne Alkohol', 'Shrub, Soda, Kräuter, klarer Saft, mit derselben Sorgfalt', 'Ja, mit derselben Sorgfalt: Shrub, Soda, Kräuter, klarer Saft.'),
  ]),
  ('Preise', [
   ('Signature Drinks', '12 Euro', 'Signature Drinks 12 Euro, alkoholfreie Drinks 11, Longdrinks 10, Wein und Spritz 8, Sekt auf Eis 6, Bier 4, alkoholfreie Getränke 3 Euro.'),
   ('Alkoholfreie Drinks', '11 Euro', 'Signature Drinks 12 Euro, alkoholfreie Drinks 11, Longdrinks 10, Wein und Spritz 8, Sekt auf Eis 6, Bier 4, alkoholfreie Getränke 3 Euro.'),
   ('Longdrinks', '10 Euro', 'Signature Drinks 12 Euro, alkoholfreie Drinks 11, Longdrinks 10, Wein und Spritz 8, Sekt auf Eis 6, Bier 4, alkoholfreie Getränke 3 Euro.'),
   ('Wein, Spritz, Bier', 'Wein und Spritz 8, Sekt auf Eis 6, Bier 4, alkoholfreie Getränke 3 Euro', 'Signature Drinks 12 Euro, alkoholfreie Drinks 11, Longdrinks 10, Wein und Spritz 8, Sekt auf Eis 6, Bier 4, alkoholfreie Getränke 3 Euro.'),
   ('Essen', 'an normalen Abenden nicht; beim Privaten Dinner und bei Festen mit Buffet oder Foodtruck', 'An normalen Abenden nicht.'),
  ]),
 ]),
 ('Programm', [
  ('Die Woche', [
   ('Donnerstag', 'ab und zu live: kleine Konzerte mitten im Raum, Jazz, Soul, Pop, ohne Eintritt, ab 20 Uhr', 'Kleine Konzerte mitten im Raum: Jazz, Soul, Pop. Duos und Trios, ohne Eintritt, ab 20 Uhr.'),
   ('Freitag', 'Momo an der Bar: er fragt, mixt und erzählt, bis 2 Uhr', 'Momo fragt, mixt und erzählt. Bis 2 Uhr.'),
   ('Samstag', 'die DJ-Abende: rund einmal im Monat, von 21 bis 1 Uhr, auf den Plakaten SESSION', 'Rund einmal im Monat legt jemand auf, von 21 bis 1 Uhr. Auf den Plakaten heisst die Reihe SESSION, gemeint sind Drinks und Musik an einem Abend.'),
   ('Eintritt', 'Konzerte und DJ-Abende sind ohne Eintritt', 'Konzerte und DJ-Abende sind ohne Eintritt.'),
  ]),
  ('DJ-Abende', [
   ('Zuletzt', 'Ghazouani Brothers am 17.10.2026, elektronisch, aus Tunis', 'Ghazouani Brothers', '17.10.2026 · elektronisch, aus Tunis'),
   ('Der nächste', 'kündigt die Bar auf Instagram an', 'Den nächsten kündigt die Bar auf Instagram an.'),
   ('Gastschichten', 'an manchen Abenden steht neben Momo jemand aus einer anderen Bar, aus Hannover oder Berlin', 'An manchen Abenden steht neben Momo jemand aus einer anderen Bar, aus Hannover oder Berlin, und bringt eigene Drinks mit.'),
  ]),
  ('Die Feste', [
   ('Silvester', 'ab mittags, abends geht es weiter', 'Silvester ab mittags', 'Abends geht es weiter.'),
   ('Geburtstag der Bar', 'im Winter, mit DJs, Mexikanern und einem Drink zur Begrüssung', 'Mit DJs, Mexikanern und einem Drink zur Begrüssung für die ersten Gäste.'),
   ('Tanz in den Mai', '30. April, Eintritt frei', 'Tanz in den Mai', 'Mahir Maulud am Deck, Momo an der Bar, Eintritt frei.'),
   ('Valentinstag', 'mit Rudi von Culinarium: vier Drinks und Teller zum Teilen, nur an diesem Abend', 'Mit Rudi von Culinarium: eine Karte mit vier Drinks und Tellern zum Teilen, die es nur an diesem Abend gibt.'),
  ]),
 ]),
 ('Feiern', [
  ('Drei Formate', [
   ('Privates Dinner', '10 bis 14 Gäste, mit Rudi in der Küche und Momo an der Bar: Gruss aus der Küche, drei Gänge, fünf Drinks', 'Ein exklusiver Abend für zehn bis vierzehn Gäste an der langen Tafel, mit Rudi in der Küche und Momo an der Bar.', 'Fünf Drinks von Momo, auf die Gänge abgestimmt'),
   ('Die lange Tafel', '10 bis 20 Gäste auf der Empore, vier Stunden, mit eigenem Budget für die Drinks', 'Oben auf der kleinen Empore steht die lange Tafel. Vier Stunden gehört sie eurer Runde, unten läuft die Bar weiter.', 'Ihr legt vorher ein Budget für die Drinks fest'),
   ('Die ganze Bar', 'ab 30 Gästen, von 19 bis 2 Uhr als geschlossene Gesellschaft', 'Ab dreissig Gästen schliesst die Bar für euch. Von 19 bis 2 Uhr gehört euch der ganze Raum: unter der Decke, an der Theke, auf der Empore.'),
  ]),
  ('Die ganze Bar: Preise', [
   ('Kategorie 1', 'Bier, Wein, Spritz: 49 € pro Person', 'Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke', '49 €'),
   ('Kategorie 2', 'dazu Longdrinks: 59 € pro Person', 'Longdrinks · Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke', '59 €'),
   ('Kategorie 3', 'dazu fünf Signature Cocktails: 79 € pro Person', 'Fünf Signature Cocktails · Longdrinks · Bier · Wein · Spritzgetränke · Shots · alkoholfreie Getränke', '79 €'),
   ('Länger bleiben', 'ab 2 Uhr jede angefangene Stunde 10 Euro pro Person', 'Wer länger bleibt: ab 2 Uhr jede angefangene Stunde 10 Euro pro Person.'),
   ('Budget', 'Service und Raum 500 €, Budget für Drinks ab 1.000 €', 'Für Service und Raum gibt es einen festen Betrag, für die Drinks setzt ihr vorher einen Rahmen.', '500 €', 'ab 1.000 €'),
  ]),
  ('So geht es', [
   ('Anfragen', 'Anlass, Datum, wie viele ihr seid', 'Ihr schreibt, was ihr vorhabt: Anlass, Datum, wie viele ihr seid.'),
   ('Angebot', 'Derya und Momo melden sich mit einem Vorschlag', 'Derya und Momo melden sich mit einem Vorschlag, nur für euch.'),
   ('Anzahlung', '30 Prozent eine Woche vorher, der Rest am Abend vor Beginn', 'Bei jedem Abend 30 Prozent eine Woche vorher, der Rest am Abend vor Beginn.'),
   ('Musik dazu', 'DJ, Gesang oder Jazz, auch mit den Musikern, die sonst hier spielen', 'Ihr sucht noch einen DJ, Live-Musik, Gesang oder Jazz?'),
   ('Grosse Events', 'ausser Haus, in externen Locations wie der Loge; Infos auf Anfrage', 'Für grössere Veranstaltungen zieht die Bar um, in externe Locations wie die Loge.', 'Infos auf Anfrage.'),
  ]),
 ]),
 ('Das Haus & Team', [
  ('Der Raum', [
   ('An der Theke', 'auf den Hockern am nächsten dran: Momo fragt, was du magst', 'Auf den Hockern an der Theke bist du am nächsten dran.'),
   ('Am Tisch', 'Holztische und eine Polsterbank, Kerzenlicht, unter dem Gewölbe', 'Holztische und eine Polsterbank an hellen Wänden, darüber Messingleuchten, auf dem Tisch Kerzenlicht.'),
   ('Draussen', 'wenn es warm ist, Tische vor der Tür an der Ecke', 'Wenn es warm ist, stehen Tische vor der Tür an der Ecke.'),
  ]),
  ('Zwei Leute', [
   ('Derya Ivkin', 'führt die Bar seit Herbst 2023, Wiedereröffnung am 9. November 2023', 'Seit Herbst 2023 gehört die Bar ihr und Momo.', 'Übernimmt die Bar im Herbst, Wiedereröffnung am 9. November.'),
   ('Momo Ben Khelifa', 'entwirft die Drinks; vorher Biotechnologie an der Uni, dann Bars in Berlin und Hannover', 'Vorher Biotechnologie an der Uni, dann Bars in Berlin und Hannover.'),
  ]),
 ]),
 ('Der Weg', [
  ('Hinfinden', [
   ('Adresse', 'Haasemannstraße 13, 30449 Hannover-Linden', 'Haasemannstraße 13, 30449 Hannover-Linden'),
   ('Ecke', 'Haasemannstraße, Ecke Rampenstraße; das Schild an der Ecke leuchtet', 'Haasemannstraße, Ecke Rampenstraße', 'Das Schild an der Ecke leuchtet.'),
   ('Bahn', 'Stadtbahn bis Am Küchengarten, Linien 9 und 17, dann zwei Minuten zu Fuss', 'Stadtbahn bis Am Küchengarten, Linien 9 und 17'),
  ]),
 ]),
 ('Kontakt', [
  ('So erreichst du das Team', [
   ('Telefon', '+49 163 3909578 und +49 174 9916296', 'Telefon der Bar: +49 163 3909578 und +49 174 9916296.'),
   ('Instagram', '@walkonthewildside_hannover', 'Instagram: @walkonthewildside_hannover.'),
   ('E-Mail', 'keine Adresse der Bar in den Quellen; Telefon oder Instagram', 'Eine E-Mail-Adresse der Bar steht in keiner Quelle des Hauses; nenne keine.'),
  ]),
 ]),
 ('Im selben Haus', [
  ('Die Nachbarn', [
   ('Culinarium', 'Food-Pairing-Abende an einzelnen Wochenenden: Rudi kocht drei Gänge, Momo mixt fünf Drinks dazu, eigene Tickets', 'An einzelnen Wochenenden wird aus der Tafel ein Menü: Rudi kocht drei Gänge, Momo mixt fünf Drinks dazu, vierzehn Gäste sitzen an einem Tisch. Eigene Abende, eigene Tickets, eigene Seite.'),
   ('Dirty Chicken', 'Rudis Sandwiches, mal hier, mal im Tiedthof; Termine auf Instagram', 'Rudis Sandwiches aus der Familie der Bar, mal hier, mal im Tiedthof. Termine auf Instagram.'),
  ]),
 ]),
]


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def main():
    quelle = {n: open(os.path.join(WISSEN, n), encoding='utf-8').read() for n in DATEIEN}
    roh = {n: norm(t) for n, t in quelle.items()}
    fehler, aus = [], []
    for bereich, gruppen in S:
        gl = []
        for gruppe, zeilen in gruppen:
            zl = []
            for was, angabe, beleg, *mehr in zeilen:
                datei = next((n for n, t in roh.items() if norm(beleg) in t), None)
                if not datei or any(not any(norm(m) in t for t in roh.values()) for m in mehr):
                    fehler.append(f'Beleg fehlt: {bereich} / {was}: «{beleg}»')
                    continue
                # jede Zahl der Angabe steht im Umfeld eines Belegs (±1500 Zeichen), nicht nur irgendwo im Wissen
                fen = ''
                for bl in [beleg] + mehr:
                    for t in roh.values():
                        i = t.find(norm(bl))
                        if i >= 0:
                            fen += t[max(0, i - 1500):i + 1500].replace('’', '')
                for zahl in re.findall(r'\d+(?:[.,]\d+)?', (gruppe + ' ' + angabe).replace('’', '')):
                    if zahl not in fen:
                        fehler.append(f'Zahl {zahl} nicht beim Beleg: {bereich} / {was}')
                fid = hashlib.sha1(f'{bereich}|{gruppe}|{was}'.encode('utf-8')).hexdigest()[:10]
                zl.append({'fid': fid, 'was': was, 'angabe': angabe, 'beleg': norm(beleg), 'datei': datei, 'mehr': [norm(m) for m in mehr]})
            gl.append({'gruppe': gruppe, 'zeilen': zl})
        aus.append({'bereich': bereich, 'gruppen': gl})
    if fehler:
        print('\n'.join(fehler)); sys.exit(1)
    json.dump({'stand': max(os.path.getmtime(os.path.join(WISSEN, n)) for n in DATEIEN), 'bereiche': aus},
              open(os.path.join(HIER, 'steckbrief.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(sum(len(g['zeilen']) for b in aus for g in b['gruppen']), 'Zeilen, alle belegt')


if __name__ == '__main__':
    main()
