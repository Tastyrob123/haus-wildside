#!/usr/bin/env python3
"""Beispiele für das Gästebuch von Walk on the Wild Side Hannover (31.10.2026, Muster _bau/culinarium_beispiele.py des Culinarium): schreibt gast_beispiele.json
(Anfragen im Eingang) und gast_beispiel_fragen.json («Das wurde gefragt»). Namen und Adressen sind erfunden (example.com), in der Oberfläche steht
«Beispiel» dabei (Master E10, R20). Jede Angabe in Antworten und Briefen steht so in gast/gast_wissen.txt oder gast/gast_umgebung.txt (Wortlaut der Website);
Preise, Zeiten, Formate sind nicht erfunden, kein Datum eines kommenden DJ-Abends wird genannt (kündigt die Bar auf Instagram an).
Zwei Fragen haben mit Absicht keine Antwort (Hund, Nussallergie beim Dinner): dazu sagt die Website nichts, Lücken zum Nachtragen. Nie erfinden, das Team
habe etwas nachgetragen (gast_beispiel_nachgetragen.json bleibt leer, die Oberfläche zeigt beschriftete Musterkarten).
Die Formular-Anfragen haben genau die Zeilen, die baustein/anfrage.js schickt. Prüfung am Ende: jede Zahl der Antworten steht im Wissen.
Aufruf: python3 _werkzeuge/reception/_bau/wildside_beispiele.py"""
import json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, C)
from reception import DANKE   # Dank an den Gast mit dem Namen des Werkzeugs aus kleid/wildside.js
KONTAKT = 'Telefon +49 163 3909578 · +49 174 9916296 · Instagram @walkonthewildside_hannover'
TEAM = '- Telefon der Bar: +49 163 3909578\n- Instagram: @walkonthewildside_hannover'
GRUSS = '\n\nBis bald an der Ecke\n\nDerya und Momo\nWalk on the Wild Side'


def web(seite, seite_name, zeilen):
    n = '\n'.join(zeilen)
    return {'web': True, 'an': KONTAKT, 'seite': seite, 'seite_name': seite_name, 'nachricht': n,
            'verlauf': [['user', f'Über ein Formular der Website (Seite {seite_name}): ' + n]]}


def chat(*z):
    return {'verlauf': [[('user' if i % 2 == 0 else 'assistant'), t] for i, t in enumerate(z)]}


A = [
    dict(vor=[0, 9, 12], art='reservieren', status='neu', abteilung='Reservieren', name='Lena Hoffmann', kontakt='lena.hoffmann@example.com',
         datum='Freitag, 13. November 2026', uhrzeit='20 Uhr', personen=4, sprache='de', anliegen='Platz reservieren: Freitag, 13. November 2026, 20 Uhr, 4 Plätze', betreff='', text='', team='', formular='reservieren', platz='Theke',
         **web('/besuch.html#reservieren', 'Besuch', ['Abend: Freitag, 13. November 2026', 'Uhrzeit: 20 Uhr', 'Plätze: 4'])),
    dict(vor=[1, 20, 5], art='reservieren', status='gelesen', abteilung='Reservieren', name='Jonas Albers', kontakt='+49 170 5550123',
         datum='Samstag, 7. November 2026', uhrzeit='21 Uhr', personen=2, sprache='de', anliegen='Platz reservieren: Samstag, 7. November 2026, 21 Uhr, 2 Plätze', formular='reservieren', platz='Theke',
         betreff='Dein Platz an der Theke am Samstag',
         text=('Hallo Jonas,\n\ndanke für deine Reservierung. Für Samstag, den 7. November, ab 21 Uhr halten wir dir zwei Plätze frei [Platz prüfen]; wir bestätigen dir den Abend per Nachricht.\n\n'
               'Am besten sitzt ihr an der Theke: Da ist Momo am nächsten dran, fragt, was ihr mögt, und mixt daraus euren Drink.\n\n'
               'Bis bald an der Ecke\n\nDerya und Momo\nWalk on the Wild Side'),
         team=('Grundlage: Besuch («Ein Platz für euch.», «Die Bar bestätigt per Nachricht.»), Das Haus («An der Theke»).\n'
               'Offen: ob zwei Plätze an der Theke frei sind.'),
         **web('/besuch.html#reservieren', 'Besuch', ['Abend: Samstag, 7. November 2026', 'Uhrzeit: 21 Uhr', 'Plätze: 2'])),
    dict(vor=[1, 11, 30], art='dinner', status='gelesen', abteilung='Dinner', name='Mira Schulte', kontakt='mira.schulte@example.com', datum='Samstag, 5. Dezember 2026', personen=12, sprache='de',
         anliegen='Privates Dinner für 12 zum 30. Geburtstag; eine Person hat eine Nussallergie.',
         betreff='Euer Dinner auf der Empore',
         text=('Hallo Mira,\n\ndanke für deine Nachricht und schön, dass ihr den 30. Geburtstag bei uns feiern wollt. Mit zwölf Gästen passt das Private Dinner genau: ein exklusiver Abend an der langen Tafel, mit Rudi in der Küche und Momo an der Bar.\n\n'
               'Zum Anfang ein Gruss aus der Küche, dann drei Gänge und dazu fünf Drinks von Momo, auf die Gänge abgestimmt. Dass eine von euch keine Nüsse verträgt, geben wir an Rudi weiter [Rudi fragen].\n\n'
               'Derya und Momo melden sich mit einem Vorschlag, nur für euch [Preis klären]. Die Anzahlung: 30 Prozent eine Woche vorher, der Rest am Abend vor Beginn.'
               + GRUSS),
         team=('Grundlage: Feiern («Privates Dinner», «So geht es»). Allergien: dazu sagt die Website nichts.\n'
               'Offen: Preis des Dinners (steht nicht auf der Website), Nussallergie mit Rudi klären, ob der 5. Dezember frei ist.'),
         **chat('Hallo, wir möchten den 30. Geburtstag meiner Schwester mit einem Dinner feiern, wir wären 12. Eine hat eine Nussallergie.',
                'Für zehn bis vierzehn Gäste gibt es das Private Dinner an der langen Tafel, mit Rudi in der Küche und Momo an der Bar. Zur Nussallergie sagt die Website nichts, Rudi klärt das mit dir. Magst du mir deinen Namen und eine E-Mail-Adresse geben?',
                'Mira Schulte, mira.schulte@example.com, am liebsten Samstag, 5. Dezember',
                DANKE['de'])),
    dict(vor=[2, 18, 45], art='feier', status='neu', abteilung='Feiern', name='Kai Brandt', kontakt='+49 151 2345678', datum='Samstag, 13. März 2027', personen=40, sprache='de',
         anliegen='Die ganze Bar für den 40. Geburtstag, 40 Personen, mit DJ.', betreff='', text='', team='',
         **chat('Kann man bei euch die ganze Bar mieten? Ich werde 40, wir wären etwa 40 Leute, gern mit DJ.',
                'Ja, ab dreissig Gästen schliesst die Bar für euch, von 19 bis 2 Uhr. Einen DJ ergänzt die Bar auf Wunsch. Wenn du magst, gebe ich deine Anfrage weiter: Wie heisst du, und wie erreicht dich das Team?',
                'Kai Brandt, 0151 2345678, am liebsten Samstag, 13. März 2027',
                DANKE['de'])),
    dict(vor=[3, 14, 10], art='feier', status='gelesen', abteilung='Feiern', name='Tim Becker', kontakt='tim.becker@example.com', datum='Freitag, 4. Dezember 2026', personen=24, sprache='de',
         anliegen='Weihnachtsfeier der Firma, 24 Personen.', betreff='', text='', team='', formular='feiern',
         **web('/tafel.html#anfragen', 'Feiern', ['Format: Die lange Tafel', 'Datum: Freitag, 4. Dezember 2026', 'Wie viele: 24', 'Anlass: Weihnachtsfeier', 'Musik dazu: Ohne', 'Was habt ihr vor?: Weihnachtsfeier unseres Büros, gern mit Drinks für alle.'])),
    dict(vor=[4, 10, 20], art='nachricht', status='erledigt', abteilung='Nachrichten', name='Sophie Wagner', kontakt='sophie.wagner@example.com', datum='', personen=1, sprache='de',
         anliegen='Fragt, ob es an DJ-Abenden Eintritt kostet.',
         betreff='DJ-Abende ohne Eintritt',
         text=('Hallo Sophie,\n\nschön, dass du zu einem der DJ-Abende kommen willst. Konzerte und DJ-Abende sind bei uns ohne Eintritt.\n\n'
               'Samstags legt rund einmal im Monat jemand auf, von 21 bis 1 Uhr; den nächsten Abend kündigen wir auf Instagram an.'
               + GRUSS),
         team='Grundlage: Besuch «Gut zu wissen» (ohne Eintritt), Programm («Die DJ-Abende», samstags 21 bis 1 Uhr).\nOffen: nichts.',
         **chat('Kostet es an den DJ-Abenden Eintritt?',
                'Konzerte und DJ-Abende sind ohne Eintritt. Magst du dem Team noch etwas schreiben? Dann brauche ich deinen Namen und eine E-Mail-Adresse.',
                'Sophie Wagner, sophie.wagner@example.com. Ich wollte nur sichergehen.',
                DANKE['de'])),
    dict(vor=[5, 21, 15], art='reservieren', status='gelesen', abteilung='Reservieren', name='Emma Clarke', kontakt='emma.clarke@example.com', datum='Thursday', personen=2, sprache='en',
         anliegen='Visiting Hannover with her partner and would like two seats on Thursday.',
         betreff='Two seats on Thursday',
         text=('Hi Emma,\n\nthank you for your message. On Thursdays we are open from 7 pm to 1 am, and we will keep two seats for you [Platz prüfen]; we confirm by message.\n\n'
               'There is no fixed answer to what you will drink: the menu changes, and at the bar you tell Momo what you like.\n\n'
               'See you at the corner\n\nDerya und Momo\nWalk on the Wild Side'),
         team='Grundlage: Besuch («Wann», Donnerstag 19 bis 1 Uhr), Drinks («an der Bar sagst du, was du magst»).\nOffen: Uhrzeit, Platz.',
         deutsch={'betreff': 'Zwei Plätze am Donnerstag',
                  'text': ('Hallo Emma,\n\ndanke für deine Nachricht. Donnerstags haben wir von 19 bis 1 Uhr offen, und wir halten euch zwei Plätze frei [Platz prüfen]; wir bestätigen per Nachricht.\n\n'
                           'Was du trinkst, steht nicht fest: Die Karte wechselt, und an der Bar sagst du Momo, was du magst.\n\nBis bald an der Ecke\n\nDerya und Momo\nWalk on the Wild Side')},
         verlauf_de=['Hallo, wir sind nächste Woche in Hannover und würden gern am Donnerstag zu zweit vorbeikommen. Kann man reservieren?',
                     'Ja, mit «Platz reservieren» auf der Seite Besuch geht es am schnellsten. Magst du mir deinen Namen und eine E-Mail-Adresse geben, dann gebe ich es weiter?',
                     'Emma Clarke, emma.clarke@example.com',
                     DANKE['de']],
         **chat('Hi, we are in Hannover next week and would love to come by on Thursday, two of us. Can we book?',
                'Yes, the quickest way is «Platz reservieren» on the Besuch page. Could you give me your name and an email address, and I will pass it on?',
                'Emma Clarke, emma.clarke@example.com',
                'Thank you. This is a draft by Tasty Studios: your request does not go to the team, it is only kept for viewing in the host tool.')),
]

F = [
    dict(vor=[0, 10, 20], sprache='de', belegt=True, frage='Wann habt ihr heute offen?', buchung=True,
         antwort='Donnerstag bis Samstag ab 19 Uhr.\n- Donnerstag: 19 bis 1 Uhr\n- Freitag und Samstag: 19 bis 2 Uhr\n- Sonntag bis Mittwoch: geschlossen'),
    dict(vor=[0, 8, 55], sprache='de', belegt=True, frage='Was kostet ein Drink bei euch?',
         antwort='Ein Signature Drink kostet 12 Euro.\n- Alkoholfreie Drinks: 11 Euro\n- Longdrinks: 10 Euro\n- Wein und Spritz: 8 Euro, Bier 4 Euro'),
    dict(vor=[1, 19, 5], sprache='de', belegt=True, frage='Was ist Milk Washing?',
         antwort='Milch bindet die Trübstoffe und wird wieder abgefiltert. Was bleibt, ist klar wie Wasser und weich wie Sahne.'),
    dict(vor=[1, 13, 40], sprache='de', belegt=False, thema='Hund', frage='Darf ich meinen Hund mitbringen?',
         antwort='Dazu steht nichts in meinen Unterlagen. Frag am besten direkt:\n' + TEAM),
    dict(vor=[2, 17, 25], sprache='de', belegt=True, frage='Wann ist der nächste DJ-Abend?',
         antwort='Samstags legt rund einmal im Monat jemand auf, von 21 bis 1 Uhr. Den nächsten Abend kündigt die Bar auf Instagram an.\n- Eintritt: keiner\n- Zuletzt: Ghazouani Brothers am 17.10.2026'),
    dict(vor=[2, 9, 10], sprache='de', belegt=True, frage='Wie komme ich zu euch?',
         antwort='Mit der Stadtbahn bis Am Küchengarten, dann zwei Minuten zu Fuss.\n- Adresse: Haasemannstraße 13, 30449 Hannover-Linden\n- Ecke: Haasemannstraße, Ecke Rampenstraße\n- Bahn: Linien 9 und 17'),
    dict(vor=[3, 12, 30], sprache='de', belegt=False, thema='Nussallergie beim Dinner', frage='Kocht Rudi beim Dinner auch ohne Nüsse?',
         antwort='Dazu steht nichts in meinen Unterlagen; beim Privaten Dinner klärt Rudi das mit dir. Frag am besten direkt:\n' + TEAM),
    dict(vor=[3, 15, 45], sprache='en', belegt=True, frage='Do you have non-alcoholic drinks?',
         antwort='Yes, made with the same care: shrub, soda, herbs, clear juice. Alcohol-free drinks are 11 euros.'),
    dict(vor=[4, 11, 0], sprache='de', belegt=True, frage='Was kostet die ganze Bar für eine Feier?',
         antwort='Ab dreissig Gästen gehört euch die ganze Bar von 19 bis 2 Uhr, mit einem Preis pro Gast.\n- Kategorie 1: Bier, Wein, Spritz, 49 €\n- Kategorie 2: dazu Longdrinks, 59 €\n- Kategorie 3: dazu fünf Signature Cocktails, 79 €'),
    dict(vor=[4, 18, 20], sprache='de', belegt=True, frage='Kann ich mit 15 Leuten Geburtstag feiern?',
         antwort='Ja, zehn bis zwanzig Gäste feiern an der langen Tafel auf der Empore.\n- Dauer: vier Stunden, unten läuft die Bar weiter\n- Drinks: ihr legt vorher ein Budget fest\n- Anfragen: auf der Seite Feiern'),
]
for f in F:
    f.setdefault('thema', ''); f.setdefault('buchung', False)


def pruefen():
    """Jede Zahl in Antworten und Briefen steht im Wissen (Website, Umgebung); kein Datum des nächsten Abends."""
    w = ''.join(open(os.path.join(C, 'gast', n), encoding='utf-8').read() for n in ('gast_wissen.txt', 'gast_umgebung.txt'))
    erlaubt = {'40', '12', '24', '4', '2', '13', '2027', '2026', '1', '0151', '2345678', '7', '5', '30', '15', '20', '21', '11'}   # Angaben der erfundenen Gäste (Alter, Personen, Wunschtage, Nummer) und englische Uhrzeiten
    fehler = []
    for x in [a.get('text', '') + ' ' + a.get('betreff', '') for a in A] + [f['antwort'] for f in F]:
        for z in re.findall(r'\d+(?:[.,]\d+)?', x.replace('+49 163 3909578', '')):
            if z not in w and z not in erlaubt:
                fehler.append(z)
    if fehler:
        sys.exit('PRUEF · Zahlen ohne Beleg: ' + ', '.join(sorted(set(fehler))))


if __name__ == '__main__':
    pruefen()
    json.dump(A, open(os.path.join(C, 'gast_beispiele.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(F, open(os.path.join(C, 'gast_beispiel_fragen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump([], open(os.path.join(C, 'gast_beispiel_nachgetragen.json'), 'w', encoding='utf-8'))
    print(len(A), 'Anfragen,', len(F), 'Fragen (davon', sum(1 for f in F if not f['belegt']), 'ohne Antwort)')
