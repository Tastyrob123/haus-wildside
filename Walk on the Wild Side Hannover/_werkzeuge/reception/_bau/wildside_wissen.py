#!/usr/bin/env python3
"""Wissen des Chats für das Gästebuch von Walk on the Wild Side Hannover (31.10.2026). Muster: _bau/culinarium_wissen.py des Culinarium.
Liest nur, aus dem Hausordner:
  _werkzeuge/reception/_bau/website-text/*.txt   Wortlaut der Website, wie ein Gast ihn sieht (node _bau/website_text.js, ohne Vorführ-Hinweise)
  website/besuch.html, website/tafel.html          die Bestätigungssätze der beiden Formulare (stehen erst nach dem Absenden auf der Seite)
  website/bau.py                                   HAUS (Adresse, Telefon, Instagram, Zeiten)
Schreibt: gast/gast_wissen.txt, gast/gast_umgebung.txt, gast/gast_haus.json und vorlagen/*.txt.
Nichts wird abgetippt oder umformuliert; jeder Satz, den dieses Skript für Vorlagen und Umgebung übernimmt, muss wörtlich in der Quelle stehen,
sonst bricht es ab. Ein Satz der Startseite («Eine Getränkekarte gibt es im Wild Side nicht.») bleibt draussen: Die Karte wechselt (Kundin 30.10.2026,
CHARAKTER.md Abschnitt 1); die Seite Drinks und «Gut zu wissen» sagen es richtig. Eine E-Mail-Adresse der Bar ist nicht belegt (die Angebotsmappe nennt
die von Culinarium) und kommt nirgends vor. Fehlt etwas, fehlt es auch im Chat und der Chat verweist an das Team.
Aufruf aus dem Hausordner: python3 _werkzeuge/reception/_bau/wildside_wissen.py   (nach neuen Quellen erneut, danach steckbrief_bau.py)"""
import json, os, re, sys

C = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))     # _werkzeuge/reception
PROJ = os.path.dirname(os.path.dirname(C))
WT = os.path.join(C, '_bau', 'website-text')
ZIEL = os.path.join(C, 'gast')
SEITEN = [('index', 'Startseite'), ('drinks', 'Drinks: Was magst du?'), ('programm', 'Programm: Lauter (DJ-Abende, Konzerte, Feste)'),
          ('tafel', 'Feiern: Euer Abend (Privates Dinner, lange Tafel, ganze Bar, Preise)'), ('haus', 'Das Haus: Unter dieser Decke'), ('besuch', 'Besuch: Zeiten, Weg, Reservieren, Fragen')]
NAV = {'Drinks', 'Programm', 'Feiern', 'Das Haus', 'Besuch', 'Reservieren'}
FUSS_ANFANG = 'An einzelnen Wochenenden wird aus der langen Tafel ein Menü: Rudi kocht, Momo mixt die Drinks dazu.'
ZEITZEILEN = {'Donnerstag', 'Freitag', 'Samstag', '19 bis 1 Uhr', '19 bis 2 Uhr', 'Sonntag bis Mittwoch', 'geschlossen'}
# Beschriftungen der Formulare und der gezeichneten Karte sind keine Angaben des Hauses
FORM = {'Wie viele · tippt die Hocker an', '4 Plätze', 'mehr', 'Abend', 'Uhrzeit', '19 Uhr', 'Plätze', 'Name', 'Telefon oder E-Mail', 'Platz reservieren',
        'Format', 'Datum', 'Wie viele', 'Anlass', 'Geburtstag', 'Musik dazu', 'Ohne', 'E-Mail oder Telefon', 'Was habt ihr vor?', 'Anfrage senden',
        'Auf der Karte', 'Haasemannstraße', '13', 'Rampenstraße', 'Kartengrundlage © OpenStreetMap-Mitwirkende'}
RAUS = {'Eine Getränkekarte gibt es im Wild Side nicht. Wer an die Theke kommt, wird gefragt, was er mag, und Momo macht daraus einen Drink. So sieht das aus.'}


def seite(n):
    roh = open(os.path.join(WT, n + '.txt'), encoding='utf-8').read()
    kopf, _, rumpf = roh.partition('\n\n')
    abgerufen = (re.search(r'^Abgerufen: (.+)$', kopf, re.M) or [None, ''])[1]
    zeilen = rumpf.splitlines()
    while zeilen and zeilen[0] in NAV:      # Leiste oben
        zeilen.pop(0)
    if FUSS_ANFANG in zeilen:               # Fuss: steht auf jeder Seite gleich, einmal als eigener Teil
        i = zeilen.index(FUSS_ANFANG)
        while i and zeilen[i - 1] in ZEITZEILEN:
            i -= 1
        zeilen, fuss = zeilen[:i], zeilen[i:]
    else:
        fuss = []
    text = '\n'.join(z for z in zeilen if z not in FORM and z not in RAUS)
    return text, fuss, abgerufen


def muss(satz, quelle_text, wo):
    if satz not in quelle_text:
        sys.exit(f'FEHLT · «{satz[:80]}» steht nicht in {wo}. Nichts geschrieben.')
    return satz


def bau():
    os.makedirs(ZIEL, exist_ok=True)
    os.makedirs(os.path.join(C, 'vorlagen'), exist_ok=True)
    teile, fuss, alles = [], [], ''
    for n, titel in SEITEN:
        t, f, ab = seite(n)
        fuss = fuss or f
        alles += '\n' + t
        teile.append(f'=== Seite: {titel} · Walk on the Wild Side (Website: {n}.html; Wortlaut wie auf der Seite, abgerufen {ab}) ===\n{t}')
    fuss = [z for z in fuss if z not in ('Zu Culinarium', 'Zu Dirty Chicken')]
    teile.append('=== Fuss jeder Seite (Zeiten, die Nachbarn im Haus, Adresse) ===\n' + '\n'.join(fuss))
    alles += '\n' + '\n'.join(fuss)
    if re.search(r'gibt es im Wild Side nicht|keine Karte', '\n'.join(teile)):
        sys.exit('PRUEF · «keine Karte» im Wissen: die Karte wechselt (Kundin 30.10.2026).')
    if re.search(r'[\w.+-]+@[\w-]+\.[a-z]{2,}', '\n'.join(teile)):
        sys.exit('PRUEF · eine E-Mail-Adresse im Wissen: die Bar hat keine belegte.')
    wissen = '\n\n'.join(teile) + '\n'

    besuch_html = open(os.path.join(PROJ, 'website', 'besuch.html'), encoding='utf-8').read()
    tafel_html = open(os.path.join(PROJ, 'website', 'tafel.html'), encoding='utf-8').read()
    bau_py = open(os.path.join(PROJ, 'website', 'bau.py'), encoding='utf-8').read()
    tel = muss('+49 163 3909578', bau_py, 'website/bau.py (HAUS)')
    tel2 = muss('+49 174 9916296', bau_py, 'website/bau.py (HAUS, Angebotsmappe)')
    ig = muss('@walkonthewildside_hannover', bau_py, 'website/bau.py (HAUS)')
    bahn = muss('Stadtbahn bis Am Küchengarten, Linien 9 und 17', alles, 'besuch.html')
    zahlung = muss('Bei jedem Abend 30 Prozent eine Woche vorher, der Rest am Abend vor Beginn.', alles, 'tafel.html')
    umgebung = f"""=== Kontakt (Website: besuch.html und tafel.html, website/bau.py HAUS) ===
Telefon der Bar: {tel} und {tel2}. Instagram: {ig}.
Reservieren: mit «Platz reservieren» auf der Seite Besuch (Abend, Uhrzeit, Plätze, Name, Telefon oder E-Mail). {muss('Die Bar bestätigt per Nachricht.', alles, 'besuch.html')}
Feiern: mit der Anfrage «Euer Abend» auf der Seite Feiern (Format, Datum, wie viele, Anlass, Musik dazu, Name, E-Mail oder Telefon). {muss('Noch schneller geht es telefonisch:', alles, 'tafel.html')} {tel} oder {tel2}.
Eine E-Mail-Adresse der Bar steht in keiner Quelle des Hauses; nenne keine.

=== Anzahlung bei Feiern (Website: tafel.html, «So geht es») ===
{zahlung}

=== Lage (Website: besuch.html) ===
Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover-Linden, Ecke Rampenstraße. {bahn}, dann zwei Minuten zu Fuss.
Parkplätze, Barrierefreiheit, Hunde und Kinder stehen in keiner Quelle des Hauses.
"""
    kontakt = f'der Bar am Telefon unter {tel} oder {tel2} oder mit einer Nachricht an {ig} auf Instagram'
    haus = {
        'name': 'Walk on the Wild Side', 'ort': 'Hannover-Linden', 'tel': tel, 'mail': '', 'kontakt': kontakt,
        'adresse': 'Walk on the Wild Side, Haasemannstraße 13, 30449 Hannover',
        'zeiten': 'Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr; Sonntag bis Mittwoch geschlossen',
        'art': 'Nachbarschafts-Mixology-Bar in Linden-Mitte: die Karte wechselt, die Drinks entwirft Momo, an der Bar sagst du, was du magst',
        'ruhetage': 'Die Bar hat Sonntag bis Mittwoch geschlossen',
        'fahrplan': '', 'kategorien': [], 'orte': [],
        'reservation': '/besuch.html#reservieren', 'reservation_name': 'Platz reservieren',
        'muster': ('Frage: Wann habt ihr offen?\nAntwort: Donnerstag bis Samstag ab 19 Uhr.\n'
                   '- Donnerstag: 19 bis 1 Uhr\n- Freitag und Samstag: 19 bis 2 Uhr\n- Sonntag bis Mittwoch: geschlossen\n\n'
                   'Frage: Darf mein Hund mit?\nAntwort: Dazu steht nichts in meinen Unterlagen. Frag am besten direkt:\n'
                   f'- Telefon der Bar: {tel}\n- Instagram: {ig}'),
    }
    besuch_t = seite('besuch')[0]; tafel_t = seite('tafel')[0]
    vorlagen = {
        'reservieren': [muss('Ab zehn Gästen gibt es die lange Tafel, ab dreissig die ganze Bar: alles unter Feiern. Die Bar bestätigt per Nachricht.', besuch_t, 'besuch.html (Reservieren)'),
                        muss('Die Bar ist klein. Wer zu mehreren kommt, reserviert besser, direkt hier: Platz reservieren.', besuch_t, 'besuch.html (Wann)'),
                        'Bestätigung des Formulars auf der Website: «' + muss('Danke. Die Bar bestätigt dir den Abend.', besuch_html, 'besuch.html (Formular)') + '»',
                        muss('Konzerte und DJ-Abende sind ohne Eintritt.', besuch_t, 'besuch.html (Gut zu wissen)')],
        'dinner': [muss('Ein exklusiver Abend für zehn bis vierzehn Gäste an der langen Tafel, mit Rudi in der Küche und Momo an der Bar. Für Geburtstage, kleine Weihnachtsfeiern, Junggesellenabschiede oder einen Abend mit den Menschen, die zählen.', tafel_t, 'tafel.html (Privates Dinner)'),
                   'Ablauf: Ein Gruss aus der Küche · Drei Gänge: ' + muss('Ein vegetarisches Menü von Rudi', tafel_t, 'tafel.html') + ' · Im Glas: ' + muss('Fünf Drinks von Momo, auf die Gänge abgestimmt', tafel_t, 'tafel.html'),
                   muss('Derya und Momo melden sich mit einem Vorschlag, nur für euch.', tafel_t, 'tafel.html (So geht es)'),
                   'Anzahlung: ' + zahlung,
                   'Bestätigung des Formulars auf der Website: «' + muss('Danke. Derya und Momo melden sich mit einem Angebot für euren Abend.', tafel_html, 'tafel.html (Formular)') + '»'],
        'feier': [muss('Oben auf der kleinen Empore steht die lange Tafel. Vier Stunden gehört sie eurer Runde, unten läuft die Bar weiter. Ihr legt vorher ein Budget für die Drinks fest; ist es erreicht, stockt ihr auf, oder eure Gäste bestellen selbst weiter.', tafel_t, 'tafel.html (Die lange Tafel, 10 bis 20 Gäste)'),
                  muss('Ab dreissig Gästen schliesst die Bar für euch. Von 19 bis 2 Uhr gehört euch der ganze Raum: unter der Decke, an der Theke, auf der Empore.', tafel_t, 'tafel.html (Die ganze Bar)'),
                  'Pauschale pro Person, 19 bis 2 Uhr: Kategorie 1 Bier, Wein, Spritz 49 € · Kategorie 2 dazu Longdrinks 59 € · Kategorie 3 dazu fünf Signature Cocktails 79 €. '
                  + muss('Wer länger bleibt: ab 2 Uhr jede angefangene Stunde 10 Euro pro Person.', tafel_t, 'tafel.html (Weg 1)'),
                  'Budget: Service und Raum 500 €, euer Budget für Drinks ab 1.000 €. ' + muss('Das Budget lässt sich nach oben frei anpassen.', tafel_t, 'tafel.html (Weg 2)'),
                  muss('Schreibt, was ihr vorhabt. Derya und Momo melden sich mit einem Angebot.', tafel_t, 'tafel.html (Euer Abend)'),
                  'Anzahlung: ' + zahlung],
    }
    for k in ('49 €', '59 €', '79 €', '500 €', 'ab 1.000 €'):
        muss(k, tafel_t, 'tafel.html (Preise)')
    open(os.path.join(ZIEL, 'gast_wissen.txt'), 'w', encoding='utf-8').write(wissen)
    open(os.path.join(ZIEL, 'gast_umgebung.txt'), 'w', encoding='utf-8').write(umgebung)
    json.dump(haus, open(os.path.join(ZIEL, 'gast_haus.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for alt in os.listdir(os.path.join(C, 'vorlagen')):
        if alt.endswith('.txt') and alt[:-4] not in vorlagen:
            os.remove(os.path.join(C, 'vorlagen', alt))
    for k, z in vorlagen.items():
        open(os.path.join(C, 'vorlagen', k + '.txt'), 'w', encoding='utf-8').write('\n\n'.join(x for x in z if x) + '\n')
    print(f'gast_wissen.txt {len(wissen) // 1024} kB · gast_umgebung.txt {len(umgebung)} Zeichen · gast_haus.json · vorlagen: {", ".join(vorlagen)}')


if __name__ == '__main__':
    bau()
