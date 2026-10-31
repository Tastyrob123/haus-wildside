#!/usr/bin/env python3
"""Baut anleitung.html (Anleitung Das Markenbuch · Walk on the Wild Side Hannover) aus den Texten unten und anleitung.vorlage.html (Aufbau wie die Anleitung
im Culinarium: Bild gross mit Klick und Esc, «Gut zu wissen» je Kapitel, neun Kapitel in fünf Themen), angepasst an die Bar: Wortmarke, Tapete aus dem Gewölbe,
Farben der DJ-Abende, Herkunft (von der Bar, fremde Rechte), Probe-Antwort der Prüfung, Hausregeln im Werkzeug.
Bilder: node anleitung_bilder.js (anleitung/k01.jpg …, aus dem echten Werkzeug).   python3 anleitung_bau.py"""
import html, os
HIER = os.path.dirname(os.path.abspath(__file__))
THEMEN = [
 ('Grundlagen', 'So geht {N_es}', [
  ('k01', 'Übersicht', 'So ist {N_es} aufgebaut.', '{N} ist die Marke von Walk on the Wild Side zum Arbeiten. Drei Teile für den Alltag, dazu die Hausregeln zum Nachschlagen.',
   ['Links die Teile: «Fotos», «Logo & Dateien» und «Markenprüfung». Darunter die Hausregeln.',
    'Oben rechts stehen «{zentrale}», die Anleitung und «Website ansehen». Unten steht immer der Hinweis zu den Bildrechten, daneben lädst du alle Dateien der Marke auf einmal.',
    'Auf dem Handy öffnet der Knopf «Bereiche» die Teile als Menü und schliesst sich nach der Wahl.'],
   '{N} speichert nichts. Was du lädst, landet auf deinem Rechner, was du prüfst, ist nach der Prüfung wieder weg.')]),
 ('Fotos', 'Finden, laden, Herkunft', [
  ('k02', 'Fotos', 'Ein Foto finden.', 'Alle Fotos der Website liegen unter «Fotos»: der Raum, die Drinks, die Leute, Musik und Feste, die lange Tafel, Plakate und Karten, unterwegs, die Jahre seit 2017 und die Nachbarn im selben Haus.',
   ['Oben ins Suchfeld schreiben, zum Beispiel «Decke», «Negroni» oder «Plakat».',
    'Darunter eingrenzen: Bereich, Hoch- oder Querformat und Herkunft (von der Bar oder mit fremden Rechten).',
    'Über der Liste steht, wie viele Fotos passen. «Filter zurücksetzen» zeigt wieder alle. Beim Scrollen kommen weitere Fotos nach.'],
   'Für einen Instagram-Beitrag eignen sich Hochformate am besten: «Hochformat» wählen, dann wird am wenigsten weggeschnitten.'),
  ('k03', 'Fotos', 'In der richtigen Grösse laden.', 'Ein Klick auf ein Foto öffnet es gross. Rechts stehen vier fertige Grössen.',
   ['«Instagram-Beitrag» (1080 auf 1350) oder «Story» (1080 auf 1920) mit der Maus berühren. Im Bild erscheint der Ausschnitt.',
    'Den Rahmen im Bild an die Stelle ziehen, die zu sehen sein soll. Der Knopf «Laden» nimmt genau diesen Ausschnitt.',
    '«Website» lädt das Foto mit 2000 Pixel an der längsten Seite, «Druck» in voller Auflösung. Zwei Wege öffnen das Foto direkt in {druck_in}, mit demselben Ausschnitt.',
    'Beim nachgeschärften Konzertfoto zeigen «Vorher», «Nachher» und «Schieber», wie das Foto geliefert wurde und wie es heute auf der Website steht.'],
   'Ist das Foto für eine Story etwas zu klein, steht im Dateinamen «hochgerechnet».'),
  ('k04', 'Fotos', 'Woher ein Foto kommt.', 'Ein Teil der Fotos stammt von der Bar selbst: Instagram, Facebook, die erste Website und die Angebotsmappe. Die anderen kommen von Gästen, aus dem Google-Eintrag, von Partnern oder der Presse; dort liegen die Rechte bei den Fotografen.',
   ['Unter «Quelle» steht, woher das Foto kommt, bei Instagram mit dem Weg zum Beitrag.',
    'Unter «Herkunft» lassen sich die Fotos der Bar und die mit fremden Rechten ein- oder ausblenden.',
    'Fotos mit fremden Rechten tragen «Rechte» und den Hinweis, sie für Werbung nur mit Erlaubnis zu nehmen.'],
   'Für Plakate und Anzeigen zuerst unter «Herkunft» «Von der Bar» wählen.')]),
 ('Logo & Dateien', 'Dateien und Farben', [
  ('k05', 'Logo & Dateien', 'Die Wortmarke für die Agentur.', 'Unter «Logo & Dateien» liegt alles, was eine Agentur, ein DJ oder eine Druckerei braucht.',
   ['Die Wortmarke in Rot als Hauptform, in Creme für dunkle und in Nacht für helle Flächen.',
    '«SVG» bleibt in jeder Grösse scharf. «PNG» hat einen durchsichtigen Grund, für Präsentationen und Office.',
    'Dazu die Tapete aus dem Gewölbe als Kachel, die Vorlage von 2020 und das Profilbild. «Alle Dateien (ZIP)» lädt alles auf einmal, mit den Schriften.'],
   'Was mit der Wortmarke nie geschieht (verzerren, drehen, umfärben, Schatten), steht in den Hausregeln unter «Zeichen».'),
  ('k06', 'Logo & Dateien', 'Farbwerte kopieren.', 'Die Farben stehen mit Namen und Rolle da: Nacht und Platte, Creme, Gold und Rot, und die Farben der DJ-Abende mit ihrem Plakat. Ein Klick genügt.',
   ['Auf eine Farbe klicken: der Wert (zum Beispiel #130E0D für Nacht) liegt in der Zwischenablage.',
    'Ein Klick auf die RGB-Zeile kopiert die RGB-Werte.',
    'Darunter lädst du die Farben als CSS, JSON oder ASE (für InDesign und Illustrator) und die Schriften als WOFF2 oder als Paket mit TTF.'],
   'Gold rahmt und Rot steht nur als Punkt. Ultramarin und Plakatrot gehören zu den SESSION-Plakaten der DJ-Abende.')]),
 ('Markenprüfung', 'Prüfen und lesen', [
  ('k07', 'Markenprüfung', 'Einen Entwurf prüfen.', 'Schickt eine Agentur oder ein DJ ein Plakat, einen Flyer oder einen Beitrag, prüfst du hier, ob er zur Bar passt.',
   ['Den Entwurf in das Feld ziehen oder «Datei wählen». Bild (JPG, PNG, WebP) oder PDF, bis 30 MB.',
    '«Prüfen» drücken. {N} misst zuerst die Farben, dann sieht Claude sich den Entwurf an.',
    'Nach etwa einer halben Minute steht die Rückmeldung da. Unter dem leeren Feld steht schon ein Beispiel.'],
   'Die Farben misst das Markenbuch direkt im Entwurf.'),
  ('k08', 'Markenprüfung', 'Die Rückmeldung lesen.', 'Oben ein Satz, wie nah der Entwurf an der Marke ist. Darunter Punkt für Punkt: Farben, Schrift, Zeichen, Abstand, Bild und Ton.',
   ['Jeder Punkt hat ein Urteil: «passt», «achten» oder «passt nicht». Was nicht passt, steht oben.',
    'Links die gemessenen Farben: wie viel der Fläche in den Farben der Bar liegt und welche Töne fremd sind. Diese Messung macht keine KI.',
    '«Als Text kopieren» gibt dir die Rückmeldung für die Mail an die Agentur. «Ergebnis sichern» legt sie als Datei auf deinen Rechner, nur wenn du es willst.'],
   'Das Beispiel ist eigens gezeichnet. Die Farben darin sind wirklich gemessen; die Urteile zu Schrift, Zeichen, Bild und Ton sind ein Beispiel, so wie die Prüfung antwortet.')]),
 ('Nachschlagen', 'Die Hausregeln', [
  ('k09', 'Hausregeln', 'In den Hausregeln lesen.', 'Die Hausregeln erklären Blatt für Blatt, wie die Bar aussieht: Haltung, Zeichen, Farben, die DJ-Abende, Schrift, das Eckschild als Form, Bilder, Gegenstände, Ton und die Nachbarn im Haus.',
   ['Links «Die Hausregeln» oder auf der Übersicht «Die Hausregeln» drücken.', 'Oben in den Hausregeln springst du zu jedem Blatt. «Als PDF sichern» legt sie als PDF ab.'],
   'Die Markenprüfung prüft nach denselben Regeln. Ändert sich etwas an der Marke, wird beides zusammen neu gebaut.')])]


def zusammen(t):
    """Tor 3 R (30.10.2026): die letzten zwei Wörter eines Kapiteltitels mit festem Leerzeichen, nie ein Wort allein in der letzten Zeile."""
    w = t.split(' ')
    # in einem nowrap-Teil: das Kleid (WO_ZEILEN) teilt Titel in Wort-Blöcke, zwischen denen auch ein festes Leerzeichen umbricht
    return t if len(w) < 3 else ' '.join(w[:-2]) + ' <span style="white-space:nowrap">' + '&nbsp;'.join(w[-2:]) + '</span>'


def e(s): return html.escape(s, quote=False)


import json
import hashlib as _hl


def _v(bild):   # Stempel aus dem Bildinhalt: neue Aufnahmen kommen sofort an (Tor 3, 30.10.2026)
    return _hl.sha1(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anleitung', bild + '.jpg'), 'rb').read()).hexdigest()[:10]
import re as _re
_kleid = open(os.path.join(os.path.dirname(HIER), 'oberflaeche', 'kleid', 'wildside.js'), encoding='utf-8').read()
NAMEN = dict(_re.findall(r"(\w+):\s*'([^']+)'", _re.search(r'namen:\s*\{([^}]*)\}', _kleid).group(1)))   # eine Stelle: WO_HAUS.namen im Kleid
def n(s):
    """{N} Name des Werkzeugs, {N_es} klein am Satzanfang nach «So geht», {<schlüssel>} und {<schlüssel>_in} (Dativ) der Nachbarn."""
    d = lambda x: x.replace('Das ', 'dem ', 1).replace('Die ', 'der ', 1).replace('Der ', 'dem ', 1)
    m = NAMEN['marke']
    s = s.replace('{N_es}', m if _re.match(r'^(Le|La|L’) ', m) else m[0].lower() + m[1:]).replace('{N}', m)
    for k, v in NAMEN.items():
        s = s.replace('{' + k + '_in}', d(v)).replace('{' + k + '}', v)
    return s
THEMEN = json.loads(n(json.dumps(THEMEN, ensure_ascii=False)))


n = 0
inhalt, kapitel = [], []
for kz, tz, ks in THEMEN:
    zeilen = []
    for (bild, bereich, titel, einl, schritte, wissen) in ks:
        n += 1; nr = '%02d' % n
        zeilen.append(f'<li><a href="#k{nr}"><b>{nr}</b><span>{e(titel)}</span><i>{e(bereich)}</i></a></li>')
        li = ''.join(f'<li><span>{i}</span><p>{e(s)}</p></li>' for i, s in enumerate(schritte, 1))
        kapitel.append(f'''<article class="kap" id="k{nr}">
  <div class="kap__t"><span class="mono">{nr} · {e(bereich)}</span><h2>{zusammen(e(titel))}</h2><p class="einl">{e(einl)}</p>
    <ol class="schritte">{li}</ol>
    <p class="wissen"><b>Gut zu wissen</b>{e(wissen)}</p></div>
  <figure class="kap__b"><button type="button" class="bild" aria-label="Bild gross ansehen: {e(titel)}"><img src="anleitung/{bild}.jpg?v={_v(bild)}" width="1200" height="714" alt="{e(NAMEN['marke'])}, {e(bereich)}: {e(titel)}"></button>
    <figcaption><span>{e(NAMEN['marke'].split(' ', 1)[1].lower())} / {e(bereich.lower())}</span><span>Grösser ansehen</span></figcaption></figure>
</article>''')
    inhalt.append(f'<section class="thema"><h3><small>{e(kz)}</small>{e(tz)}<em>{len(ks)} Kapitel</em></h3><ol>{"".join(zeilen)}</ol></section>')
seite = open(os.path.join(HIER, 'anleitung.vorlage.html'), encoding='utf-8').read()
seite = seite.replace('%%ANZAHL%%', str(n)).replace('%%NAME%%', NAMEN['marke']).replace('%%NAME_IN%%', 'wie ' + (NAMEN['marke'] if _re.match(r'^(Le|La|L’) ', NAMEN['marke']) else NAMEN['marke'][0].lower() + NAMEN['marke'][1:])).replace('%%INHALT%%', ''.join(inhalt)).replace('%%KAPITEL%%', '\n'.join(kapitel))
open(os.path.join(HIER, 'anleitung.html'), 'w', encoding='utf-8').write(seite)
print('anleitung.html:', n, 'Kapitel')
