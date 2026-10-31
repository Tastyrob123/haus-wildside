#!/usr/bin/env python3
"""Ideen für Papier: Drucksachen und Untersetzer für Walk on the Wild Side (Werkbank Papier, 31.10.2026; Bauart wie papier.py des Culinarium, Inhalt und Kleid der Bar).
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/papier.py "<website/_werkbank>"

Fünf eigene Ideen im Stil der Bar: die Karte am Tresen (Klassiker vorne, Momos Frage hinten), ein Kärtchen zu jeder Technik, ein Tischaufsteller
mit dem NEGRONI-Schriftzug, die Visitenkarte und Briefbogen mit Umschlag. Dazu zwölf Untersetzer und die zwanzig fertigen Drucksachen der
Plakatwerkstatt (_werkzeuge/imprimerie/haeuser/wildside/drucksachen/liste.json, PDF und Vorschaubild, nur kopiert → papier_mehr.json).
Kleid: Nacht mit Goldrahmen wie das Eckschild, Creme der weissen Plakate, Rot nur als Wortmarke und Punkt, Ultramarin und Plakatrot nur bei SESSION.
Schrift: Titel Prata, Lauf Hanken Grotesk 400, Etiketten Hanken 500 gesperrt (druckschrift.py). Texte nur aus der Website (papier_neu.py)."""
import json, os, shutil
from PIL import Image
import papier_kern as P
import bogen_mitte  # noqa: F401  Druckbögen mittig (Tor 4, 30.10.2026)
from papier_kern import t, lin, rahmen, kasten, foto, blatt, hw, tx, hwz, bogen_text, etikett, e
from kern import H, ROOT
import druckschrift
import papier_neu as N
from papier_neu import NACHT, PLATTE, CREME, CREME2, CREME3, GOLD, GOLDT, ROT, ULTRA, PROT, TINTE, LEISE, TAPETE

WEB = os.path.dirname(ROOT)
HAUS = os.path.dirname(WEB)
PW = os.path.join(HAUS, '_werkzeuge', 'imprimerie', 'haeuser', 'wildside', 'drucksachen')
MEINS = ['Auswahl und Anordnung der Sätze auf Karte, Kärtchen, Aufsteller und Untersetzern', 'Die Zeile «Bis 2 Uhr.» auf dem Aufsteller (aus dem Fuss der Website)']


def vers(text):
    return e(text.upper())


def punkt(x, y, d=2.4, farbe=ROT):
    return f'<i class="abs" style="left:{x - d / 2}mm;top:{y - d / 2}mm;width:{d}mm;height:{d}mm;border-radius:50%;background:{farbe}"></i>'


def etk(x, y, text, farbe, groesse=1.9, b=None, mehr=''):
    """Etikett: Hanken 500, gesperrte Versalien"""
    return t(x, y, vers(text), 'm' + (' c' if b else ''), f'font-size:{groesse}mm;letter-spacing:.2em;font-weight:500;color:{farbe};{mehr}', b)


# ============================================================ Die Karte am Tresen (A5 hoch, zwei Seiten)
def karte():
    v = (kasten(0, 0, 148, 210, f'background:{NACHT} {TAPETE}') + rahmen(6, GOLD, 3, .3)
         + hw(74, 16, 26, ROT)
         + etk(0, 54, N.ZEILE, GOLD, 2, 148)
         + lin(66, 62, 16, GOLD, .3)
         + t(0, 68, 'Die Klassiker.', 's c', f'font-size:8mm;color:{CREME}', 148))
    for i, (n, s) in enumerate(N.KLASSIKER):
        y = 88 + i * 23
        v += (t(24, y, e(n), 's c', f'font-size:5mm;color:{CREME}', 100)
              + t(24, y + 7, e(N.erster(s)), 'c', f'font-size:2.75mm;line-height:1.45;color:{CREME3}', 100))
    v += (lin(66, 182, 16, GOLD, .3)
          + etk(0, 187, N.ZEIT_KURZ, CREME3, 1.6, 148, 'letter-spacing:.12em')
          + etk(0, 193, N.ADRESSE + ' · Linden', GOLD, 1.6, 148, 'letter-spacing:.12em'))
    r = (hw(74, 13, 12, ROT)
         + etk(0, 35, 'An der Theke', GOLDT, 2, 148)
         + t(0, 42, e(N.SATZ), 's c', f'font-size:8.2mm;color:{TINTE}', 148)
         + lin(66, 58, 16, GOLDT, .3))
    for i, (n, s) in enumerate(N.WAHL):
        y = 68 + i * 24
        r += etk(0, y, n, GOLDT, 1.8, 148) + t(14, y + 5.5, e(s).replace(' ohne Alkohol', ' ohne\xa0Alkohol'), 's c', f'font-size:5mm;line-height:1.2;color:{TINTE}', 120)
    r += (t(22, 145, e(N.MOMO), 'c', f'font-size:3.5mm;line-height:1.5;color:{TINTE}', 104)
          + etk(0, 160, 'Momo Ben Khelifa', LEISE, 1.6, 148)
          + punkt(74, 177)
          + etk(0, 190, N.IG, LEISE, 1.6, 148, 'letter-spacing:.12em'))
    return [blatt(148, 210, v, '', f'background:{NACHT}'), blatt(148, 210, r, '', f'background:{CREME}')]


# ============================================================ Ein Kärtchen zu jeder Technik (A7 hoch, 74 × 105 mm)
def drinks():
    aus = []
    for n, s in N.TECHNIK:
        aus.append(blatt(74, 105, kasten(0, 0, 74, 105, f'background:{NACHT} {TAPETE}') + rahmen(4, GOLD, 2.4, .25)
                         + etk(0, 12, 'Wie Momo arbeitet', GOLD, 1.6, 74)
                         + t(4, 22, e(n), 's c', f'font-size:{6.8 if len(n) < 12 else 6.2}mm;line-height:1.1;color:{CREME}', 66)
                         + lin(29, 34, 16, GOLD, .3)
                         + t(9, 39, e(N.erster(s, 2)), 'c', f'font-size:2.55mm;line-height:1.5;color:{CREME2}', 56)
                         + hw(37, 80, 8.5, ROT), '', f'background:{NACHT}'))
    aus.append(blatt(74, 105, hw(37, 12, 9, ROT)
                     + etk(0, 30, 'Drei Techniken', GOLDT, 1.6, 74)
                     + t(7, 37, 'Aus dem Labor an\xa0die\xa0Theke.', 's c', f'font-size:5.4mm;line-height:1.2;color:{TINTE}', 60)
                     + lin(29, 54, 16, GOLDT, .3)
                     + t(9, 59, 'Momo hat Biotechnologie studiert, bevor er hinter die Bar ging. Man schmeckt es.', 'c', f'font-size:2.6mm;line-height:1.5;color:{TINTE}', 56)
                     + etk(0, 93, N.IG, LEISE, 1.25, 74, 'letter-spacing:.08em'), '', f'background:{CREME}'))
    return aus


# ============================================================ Tischaufsteller (A6 hoch, zwei Seiten)
def aufsteller():
    v = (kasten(0, 0, 105, 148, f'background:{NACHT}')
         + foto(N.bild('fb-2023-negroni'), 0, 0, 105, 90, '50% 32%')
         + lin(0, 90, 105, GOLD, .45)
         + etk(0, 98, 'An jedem Abend', GOLD, 1.7, 105)
         + t(8, 104, 'Und wer einen Negroni\xa0will.', 's c', f'font-size:6.2mm;line-height:1.16;color:{CREME}', 89)
         + t(10, 121, e(N.erster(N.KLASSIKER[0][1])), 'c', f'font-size:2.8mm;line-height:1.45;color:{CREME3}', 85)
         + hw(52.5, 131, 7.5, ROT))
    zeilen = ''
    for i, (tag, zeit) in enumerate(N.ZEITEN):
        y = 54 + i * 11
        zeilen += (etk(14, y + 1.2, tag, GOLDT, 1.7) + t(14, y, e(zeit), 's', f'font-size:4.2mm;color:{TINTE};text-align:right', 77)
                   + lin(14, y + 7.5, 77, 'rgba(27,21,18,.18)', .2))
    r = (hw(52.5, 12, 13, ROT)
         + t(0, 36, 'Bis 2\xa0Uhr.', 's c', f'font-size:8mm;color:{TINTE}', 105)
         + zeilen
         + t(12, 104, 'Samstags legen DJs an der Bar auf, rund einmal im Monat, von 21 bis 1\xa0Uhr.', 'c', f'font-size:2.8mm;line-height:1.5;color:{TINTE}', 81)
         + punkt(52.5, 121, 2.2)
         + etk(0, 128, N.ADRESSE + ' · Linden', LEISE, 1.5, 105, 'letter-spacing:.12em')
         + etk(0, 134, N.IG, LEISE, 1.5, 105, 'letter-spacing:.1em'))
    return [blatt(105, 148, v, '', f'background:{NACHT}'), blatt(105, 148, r, '', f'background:{CREME}')]


# ============================================================ Visitenkarte (85 × 55 mm)
def visitenkarte():
    v = kasten(0, 0, 85, 55, f'background:{NACHT} {TAPETE}') + rahmen(3, GOLD, 2, .25) + hw(42.5, 9.5, 29.5, ROT)
    r = (etk(7, 8, N.ZEILE, GOLDT, 1.45)
         + t(7, 13.5, 'Walk on the Wild Side', 's', f'font-size:4.6mm;color:{TINTE}')
         + ''.join(t(7, 25 + i * 4.5, e(z), '', f'font-size:2.5mm;color:{TINTE}') for i, z in enumerate([N.ADRESSE, N.ORT, N.TELEFON, N.IG]))
         + etk(7, 46.5, 'Do 19–1 · Fr und Sa 19–2 Uhr', LEISE, 1.4, None, 'letter-spacing:.14em')
         + punkt(77, 9.2, 2.2))
    return [blatt(85, 55, v, '', f'background:{NACHT}'), blatt(85, 55, r, '', f'background:{CREME}')]


# ============================================================ Briefbogen A4 und Umschlag DIN lang
def briefpapier():
    bogen = (hw(22, 16, 14, ROT, False)
             + t(110, 18, 'Walk on the Wild Side<br>' + e(N.ADRESSE) + '<br>' + e(N.ORT), '', f'font-size:2.5mm;line-height:1.55;color:{TINTE};text-align:right', 78)
             + etk(110, 34, N.ZEILE, GOLDT, 1.6, None, 'width:78mm;text-align:right')
             + lin(22, 42, 166, GOLD, .25)
             + lin(4, 105, 5, 'rgba(27,21,18,.45)', .15) + lin(4, 210, 5, 'rgba(27,21,18,.45)', .15)
             + lin(22, 273, 166, GOLD, .25) + punkt(105, 278.5, 1.8)
             + etk(0, 283, f'{N.ADRESSE} · {N.ORT} · {N.TELEFON} · {N.IG}', LEISE, 1.55, 210, 'letter-spacing:.08em'))
    umschlag = (kasten(0, 0, 220, 110, f'background:{NACHT} {TAPETE}') + rahmen(5, GOLD, 3, .25)
                + hw(14, 13, 16, ROT, False)
                + etk(36, 18, N.ZEILE, GOLD, 1.8) + t(36, 24, e(N.ADRESSE + ' · ' + N.ORT), '', f'font-size:2.6mm;color:{CREME3}')
                + f'<i class="abs" style="left:118mm;top:52mm;width:90mm;height:44mm;background:{CREME};border-radius:1mm"></i>')
    return [blatt(210, 297, bogen, '', f'background:{CREME}'), blatt(220, 110, umschlag, '', f'background:{NACHT}')]


# ============================================================ Untersetzer für die Theke (rund, 94 mm)
D = 94
R_ = D / 2


def kreis(r=R_):
    return f'M{R_} {R_ - r}A{r} {r} 0 1 1 {R_ - .01} {R_ - r}Z'


def ring(ident, text, farbe, rr=37, g=2.5):
    return bogen_text(ident + 'r', f'M{R_ - rr} {R_}A{rr} {rr} 0 1 1 {R_ + rr} {R_}A{rr} {rr} 0 1 1 {R_ - rr} {R_}', (e(text.upper()) + ' · ') * 2, g, farbe, 'm', .18)


def us(ident, grund, innen, name, satz, linie=GOLD):
    zeichnung = (f'<path d="{kreis()}" fill="{grund}"/>' + innen
                 + f'<circle cx="{R_}" cy="{R_}" r="{R_ - 3}" fill="none" stroke="{linie}" stroke-width=".35"/>')
    return etikett(ident, D, D, kreis(), zeichnung, name, satz)


def us_welle(ident, a, b):
    return f'<clipPath id="{ident}c"><path d="{kreis()}"/></clipPath>' + N.welle(None, D, D, a, b, clip=ident + 'c', breite=10, hub=3, laenge=38)


def untersetzer_alle():
    U = []
    wm_h = 1600 / 1296
    # sechs auf Creme: Wortmarke in Rot, SESSION-Wellen in Rot, Creme und Ultramarin
    U.append(us('u01', CREME, hwz(R_, R_ - 16 * wm_h, 32, ROT) + ring('u01', N.ZEILE + ' · Linden', GOLDT),
                'Die Wortmarke', 'Das Logo der Bar in Rot auf dem Creme der weissen Plakate, ringsum «Nachbarschafts-Mixology-Bar».', GOLDT))
    U.append(us('u02', CREME, us_welle('u02', CREME, PROT) + f'<circle cx="{R_}" cy="{R_}" r="21" fill="{CREME}"/>'
                + tx(R_, R_ + 3.2, 'SESSION', 7.4, ULTRA, 'm', .06, mehr='font-weight="600"') + tx(R_, R_ + 10.5, 'SAMSTAGS 21–1 UHR', 2.3, ULTRA, 'm', .14),
                'SESSION', 'Die Wellen der Plakate der DJ-Abende in Plakatrot und Creme, die Schrift in Ultramarin.', PROT))
    U.append(us('u03', CREME, us_welle('u03', CREME, PROT) + f'<circle cx="{R_}" cy="{R_}" r="23" fill="{CREME}"/>' + hwz(R_, R_ - 13 * wm_h, 26, ROT),
                'Wortmarke in der Welle', 'Die Wortmarke mitten in den SESSION-Wellen.', PROT))
    U.append(us('u04', CREME, tx(R_, R_ - 4, 'Du sagst,', 7.2, TINTE, 's') + tx(R_, R_ + 6.4, 'was du magst.', 7.2, TINTE, 's')
                + f'<circle cx="{R_}" cy="{R_ + 17}" r="1.3" fill="{ROT}"/>',
                'Du sagst, was du magst.', 'Der Satz der Bar aus Momos Frage, mit dem roten Punkt.', GOLDT))
    U.append(us('u05', CREME, us_welle('u05', CREME, ULTRA) + f'<circle cx="{R_}" cy="{R_}" r="20" fill="{CREME}"/>'
                + tx(R_, R_ - 2, 'Erst der Drink,', 4.2, ULTRA, 's') + tx(R_, R_ + 4.6, 'dann die Musik.', 4.2, ULTRA, 's'),
                'Erst der Drink, dann die Musik.', 'Die Wellen in Ultramarin, dazu der Satz der Programm-Seite.', ULTRA))
    U.append(us('u06', CREME, tx(R_, R_ + 6, '91', 24, TINTE, 's') + tx(R_, R_ + 15, 'FALSTAFF BAR GUIDE 2027', 2.3, GOLDT, 'm', .16)
                + tx(R_, R_ - 15, 'COCKTAILBARS', 2.3, GOLDT, 'm', .2) + f'<circle cx="{R_}" cy="{R_ - 22}" r="1.2" fill="{ROT}"/>',
                '91 Punkte', '91 Punkte im Falstaff Bar Guide 2027, Kategorie Cocktailbars.', GOLDT))
    # sechs auf der Nacht der Bar, mit Goldlinie wie das Eckschild
    U.append(us('u07', NACHT, f'<rect x="{R_ - 21}" y="{R_ - 25}" width="42" height="50" rx="2" fill="#000" stroke="{GOLD}" stroke-width=".9"/>'
                + hwz(R_, R_ - 18 * wm_h + 0.0, 29, CREME),
                'Das Eckschild', 'Das schwarze Kastenschild mit Goldrahmen an der Hausecke, darin die Wortmarke.'))
    U.append(us('u08', NACHT, N.birnen(R_, R_ + 4.6, 'NEGRONI', 11) + tx(R_, R_ + 14, 'AN JEDEM ABEND', 2.4, CREME3, 'm', .2),
                'NEGRONI', 'Die Glühbirnen-Schrift über der Vitrine, als Lichtpunkte in Gold.'))
    zt = ''.join(tx(R_, R_ - 9 + i * 8, z, 3.3, CREME, 'm', .16) for i, z in enumerate(['DO 19 – 1 UHR', 'FR 19 – 2 UHR', 'SA 19 – 2 UHR']))
    U.append(us('u09', NACHT, tx(R_, R_ - 19, 'Bis 2 Uhr.', 6, GOLD, 's') + zt, 'Die Zeiten', 'Donnerstag bis Samstag ab 19 Uhr, so wie im Fuss der Website.'))
    U.append(us('u10', NACHT, tx(R_, R_ - 3, 'Haasemannstraße 13', 5.2, CREME, 's') + tx(R_, R_ + 6, 'ECKE RAMPENSTRASSE', 2.5, GOLD, 'm', .18)
                + tx(R_, R_ + 17, 'LINDEN', 2.3, CREME3, 'm', .24), 'Die Adresse', 'Haasemannstraße 13, Ecke Rampenstraße: die Ecke mit dem Schild.'))
    U.append(us('u11', NACHT, tx(R_, R_ - 6, 'Instagram', 6, CREME, 's') + tx(R_, R_ + 4, '@WALKONTHEWILDSIDE', 2.9, GOLD, 'm', .1) + tx(R_, R_ + 9.5, '_HANNOVER', 2.9, GOLD, 'm', .1)
                + f'<circle cx="{R_}" cy="{R_ + 19}" r="1.2" fill="{ROT}"/>', 'Instagram', 'Wo die Bar ihre Abende ankündigt: @walkonthewildside_hannover.'))
    U.append(us('u12', NACHT, tx(R_, R_ - 1, 'Seit 2018', 7.6, CREME, 's') + tx(R_, R_ + 8, 'IN LINDEN', 2.6, GOLD, 'm', .22) + hwz(R_, R_ - 27, 12, ROT),
                'Seit 2018 in Linden', 'Seit 2018 ist Momo in Linden zu Hause, so steht es auf der Startseite.'))
    return U


# ============================================================ Die zwanzig Drucksachen der Plakatwerkstatt (nur kopiert)
PW_TEXT = {
    'session-ghazouani-brothers': (['Ghazouani Brothers,', '17.10.2026.'], 'Das SESSION-Plakat des letzten DJ-Abends für Instagram: Wellen in Plakatrot und Creme, Schrift in Ultramarin, das Foto in Schwarzweiss.'),
    'session-aushang-a3': (['SESSION', 'zum Aushang.'], 'Dasselbe Plakat in A3 für die Tür und das Fenster an der Ecke.'),
    'session-story': (['SESSION', 'als Story.'], 'Das Plakat im Hochformat 9:16 für die Story am Abend selbst.'),
    'session-programm': (['Die', 'DJ-Abende.'], 'Alle DJ-Abende auf einem Blatt A5, für den Tresen oder zum Mitnehmen.'),
    'konzert-live-am-donnerstag': (['Live am', 'Donnerstag.'], 'Das weisse Plakat der Bar für die Konzerte am Donnerstag, ohne Eintritt.'),
    'silvester-fruehshoppen': (['Silvester', 'ab mittags.'], 'Das weisse Plakat «Eure Nachbarschafts-Mixology-Bar» für den Silvester-Frühschoppen.'),
    'tanz-in-den-mai': (['Tanz', 'in den Mai.'], 'Das weisse Plakat für den Tanz in den Mai, im Format für Instagram.'),
    'gastschicht-musa': (['Gastschicht', 'mit Musa.'], 'Wenn neben Momo ein Gast aus einer anderen Bar mit eigenen Drinks steht.'),
    'karte-drunk-in-love': (['Drunk', 'in Love.'], 'Die Sonderkarte zum Valentinstag, mit den Preisen vom Plakat.'),
    'karte-preise-der-bar': (['Die Preise', 'der Bar.'], 'Die Preisliste der Bar auf einem Blatt A5, so wie sie auf der Seite «Feiern» steht.'),
    'karte-klassiker': (['Die', 'Klassiker.'], 'Negroni, Paloma, Mexikaner und ohne Alkohol, als schmale Karte für die Theke.'),
    'untersetzer-was-magst-du': (['Was', 'magst du?'], 'Ein Aufsteller A6 mit Momos drei Fragen: der Geschmack, das Glas, was hinein soll.'),
    'tischaufsteller-du-sagst': (['Du sagst,', 'was du magst.'], 'Ein Aufsteller A6 mit Momo hinter der Theke.'),
    'flyer-nachbarschafts-mixology-bar': (['Der Flyer', 'der Bar.'], 'Vorne ein Foto der Bar, hinten die Zeiten und die Adresse, A6.'),
    'aushang-oeffnungszeiten': (['Die', 'Öffnungszeiten.'], 'Der Aushang A4 für die Tür: Donnerstag bis Samstag ab 19 Uhr.'),
    'instagram-falstaff': (['Falstaff', 'Bar Guide 2027.'], 'Der Beitrag zu den 91 Punkten im Falstaff Bar Guide.'),
    'instagram-negroni': (['Der', 'Negroni.'], 'Ein Beitrag für Instagram zum Negroni, den es an jedem Abend gibt.'),
    'feiern-pauschale': (['Die ganze Bar,', 'als Pauschale.'], 'Das Angebotsblatt A5 mit den Pauschalen 49, 59 und 79 Euro.'),
    'feiern-lange-tafel': (['Die lange', 'Tafel.'], 'Das Angebotsblatt A5 für die Runde auf der Empore.'),
    'gutschein': (['Ein Gutschein', 'für einen Abend.'], 'Ein Gutschein für einen Abend an der Bar, vorne und hinten, DIN lang quer.'),
}


def plakatwerkstatt():
    """liste.json der Plakatwerkstatt → drucksachen/img/*.webp, drucksachen/pdf/*.pdf, _werkbank/papier_mehr.json (vom Kit als «Weitere» gezeigt)."""
    liste = json.load(open(os.path.join(PW, 'liste.json'), encoding='utf-8'))
    img = os.path.join(ROOT, 'drucksachen', 'img'); pdf = os.path.join(ROOT, 'drucksachen', 'pdf')
    os.makedirs(img, exist_ok=True); os.makedirs(pdf, exist_ok=True)
    mehr = []
    for d in liste:
        k = d['k']
        namen = []
        for j, v in enumerate(d['vorschau']):
            nm = (k if k == 'gutschein' else 'pw-' + k) + ('' if j == 0 else '-r')
            im = Image.open(os.path.join(PW, v)).convert('RGB')
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            im.save(os.path.join(img, nm + '.webp'), 'WEBP', quality=86, method=5)
            namen.append((nm, im.size))
        ziel = f'{H.KURZ}-{k}.pdf'
        shutil.copy2(os.path.join(PW, d['pdf']), os.path.join(pdf, ziel))
        hoch = namen[0][1][1] > namen[0][1][0]
        if len(namen) == 2:
            w = 44 if hoch else 84
            karton = [(namen[0][0], w, 'Vorderseite'), (namen[1][0], w, 'Rückseite')]
        else:
            r = namen[0][1][1] / namen[0][1][0]
            w = 40 if r > 1.6 else (54 if r > 1.3 else (64 if r > 1.05 else 86))
            karton = [(namen[0][0], w, '')]
        titel, satz = PW_TEXT.get(k, ([d['n'], ''], d['was']))
        mehr.append(dict(id='pw-' + k, name=d['n'], format=d['format'] + (' · ' + str(d['seiten']) + ' Seiten' if d['seiten'] > 1 else '') + ' · aus der Plakatwerkstatt',
                         satz=satz, titel=titel, pdf=ziel, karton=karton, masse={n: list(s) for n, s in namen}, schatten=True, haengt=False, seiten=d['seiten']))
    json.dump({'druck': mehr}, open(os.path.join(ROOT, '_werkbank', 'papier_mehr.json'), 'w'), ensure_ascii=False, indent=1)
    return mehr


SEITE_NEU = {   # Karton, Titel und Breite der eigenen Stücke, die haus.py › PAPIER_SEITE noch nicht kennt (haus.py liest papier_neu_seite.json)
    'aufsteller': dict(karton=['', [['aufsteller', 40, 'Vorderseite'], ['aufsteller-r', 40, 'Rückseite']]], titel=['Ein Aufsteller', 'für den Tisch.'], breit=[]),
    'visitenkarte': dict(karton=['', [['visitenkarte', 60, 'Vorderseite'], ['visitenkarte-r', 60, 'Rückseite']]], titel=['Die', 'Visitenkarte.'], breit=['visitenkarte', 'visitenkarte-r']),
}


def css_umstellen():
    """Satz-CSS: die Familien des Kits (Instrument Sans, DM Mono, Titel) zeigen auf die festen Schnitte von Hanken Grotesk und Prata."""
    p = os.path.join(ROOT, '_werkbank', 'satz', 'papier.css')
    css = druckschrift.umstellen(open(p, encoding='utf-8').read())
    marke = '/* Wild Side: feste Schnitte */'
    if marke not in css:
        ff = ''
        for fam in ('Hanken Grotesk', 'Instrument Sans', 'DM Mono'):
            for g, d in druckschrift.HANKEN.items():
                ff += f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{g};src:url('../fonts/{d}') format('truetype')}}\n"
        ff += "@font-face{font-family:'Prata';font-style:normal;font-weight:100 900;src:url('../fonts/Prata-Regular.ttf') format('truetype')}\n"
        css += '\n' + marke + '\n' + ff + '.t.m{font-weight:500}\n.blatt{color:' + TINTE + '}\n'
    open(p, 'w', encoding='utf-8').write(css)


def baue():
    Dr = []

    def d(ident, name, format_, blaetter, vorschau, satz, quelle):
        Dr.append(dict(id=ident, name=name, format=format_, blaetter=blaetter, vorschau=vorschau, satz=satz, quelle=quelle))
    d('karte', 'Die Karte am Tresen', 'A5 hoch, zwei Seiten', karte(), [('karte', 1), ('karte-r', 2)],
      'Vorne die Klassiker des Hauses mit ihren Sätzen von der Website, hinten Momos Frage: der Geschmack, das Glas, was hinein soll. Für alle, die erst lesen und dann bestellen.',
      'Seite «Drinks» eurer Website: «Die Klassiker» und «Das Gespräch»')
    d('drinks', 'Ein Kärtchen zu jeder Technik', 'A7 hoch, drei Motive, eine Rückseite', drinks(), [('drink-1', 1), ('drink-2', 2), ('drink-3', 3), ('drink-r', 4)],
      'Milk Washing, Fat Washing und Enzyme, jede Technik mit ihrem Satz. Momo legt das Kärtchen zum Drink, der Gast nimmt es mit nach Hause.',
      'Abschnitt «Wie Momo arbeitet» der Seite «Drinks»')
    d('aufsteller', 'Tischaufsteller', 'A6 hoch, zwei Seiten', aufsteller(), [('aufsteller', 1), ('aufsteller-r', 2)],
      'Vorne der NEGRONI-Schriftzug über der Vitrine, hinten die Zeiten der Woche und die DJ-Abende am Samstag. Steht auf dem Tisch und auf der Fensterbank.',
      'Foto NEGRONI (November 2023), Fuss und Programm eurer Website')
    d('visitenkarte', 'Visitenkarte', '85 × 55 mm, zwei Seiten', visitenkarte(), [('visitenkarte', 1), ('visitenkarte-r', 2)],
      'Vorne die Wortmarke im Goldrahmen wie das Schild an der Ecke, hinten Adresse, Telefon, Instagram und die Zeiten.',
      'Fuss eurer Website')
    d('briefpapier', 'Briefbogen und Umschlag', 'Briefbogen A4, Umschlag DIN lang', briefpapier(), [('briefbogen', 1), ('umschlag', 2)],
      'Für Angebote an Firmen und Hochzeitspaare: der Briefbogen auf Creme mit roter Wortmarke, der Umschlag in der Nacht der Bar mit Goldrahmen.', 'Wortmarke und Fuss eurer Website')
    json.dump(SEITE_NEU, open(os.path.join(ROOT, '_werkbank', 'papier_neu_seite.json'), 'w'), ensure_ascii=False, indent=1)
    P.fertig(Dr, untersetzer_alle(), MEINS)
    css_umstellen()
    print('Plakatwerkstatt:', len(plakatwerkstatt()), 'Drucksachen kopiert')


if __name__ == '__main__':
    baue()
