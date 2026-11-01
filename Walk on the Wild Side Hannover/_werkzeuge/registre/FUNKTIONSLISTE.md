---
tags: [projekt, website]
status: aktiv
---

# Funktionsliste Die Besucherliste (Le Registre) · Walk on the Wild Side Hannover

Vorlage: die Besucherliste des Culinarium Hannover (28.10.2026); Rahmen aus der Oberfläche der Häuser (Kleid wildside, «Die Bühne»). Jede Zeile ist zugleich eine Prüfung in `abnahme.js`. Noch kein Lauf.

`✓` = in allen Läufen grün, in denen die Zeile gilt. «Rechner»/«Handy»: die Zeile gilt nur dort.

## Laden

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| A01 | Auftakt: beim Öffnen bleibt die Seite ruhig (alles verborgen), bis Daten, Schriften und Fotos im ersten Bild da sind (höchstens 2,5 s), dann erscheint alles auf einmal | alle | – |
| A02 | Beim Erscheinen stehen Rand, Kopf, Bühne mit Titel und Leiste schon da (nichts halb weiss, nichts leer) | alle | – |
| A03 | Jede der acht Ansichten öffnet über die Adresse (#start … #zaehlung) und zeigt ihren Titel | alle | – |
| A04 | Eine unbekannte Adresse (#gibtsnicht) öffnet die Übersicht | alle | – |
| A05 | Der Tab-Titel nennt die Ansicht («Besuche · <Name aus dem Kleid> · Wild Side») | alle | – |
| A06 | Seiten stehen mit ihrem Namen da (Startseite, Drinks, Programm, Feiern, Das Haus, Besuch …, gelesen aus der Leiste der Website), nie als Dateiname | alle | – |
| A07 | ?gruss=tag hält den Gruss fest («Guten Tag.») für die Bildschirmfotos der Werkbank | alle | – |
| A08 | Ohne Schlüssel zeigt die Adresse immer Beispielwerte (auch mit ?beispiel=1 gleich), überall beschriftet | alle | – |
| A08b | Mit falschem Schlüssel antwortet auch der Dienst nur mit Beispielwerten (Beispiel-Band da, kein Knopf zu den echten) | Dienst | – |
| A09 | Fällt das Laden aus, steht «<Name> startet nicht» mit dem Grund und den Knöpfen «Neu laden» und dem Weg zur Zentrale, kein leeres Fenster | alle | – |
| A10 | Der gewählte Zeitraum wird im Browser gemerkt und beim nächsten Öffnen wieder gewählt | alle | – |
| A11 | Keine Konsolenfehler, keine toten Adressen beim Öffnen jeder Ansicht | alle | – |

## Kopf

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| B01 | Der Kopf nennt oben den Titel der Ansicht und darunter den Stand («Beispielwerte · keine echten Besuche») | Rechner | – |
| B02 | Anleitung: runder Knopf mit Hinweis, öffnet anleitung.html in neuem Tab | alle | – |
| B03 | Die Zentrale: runder Knopf mit Hinweis, führt zur Zentrale (lokal auf ihren eigenen Server http://127.0.0.1:9281/_werkzeuge/maison/, Fehlerbuch 10a; online ../../maison/ = /maison/; die Adresse antwortet) | alle | – |
| B04 | «Website ansehen» öffnet die Website in neuem Tab | alle | – |
| B05 | Die Marke «Das Besucherbuch» (Zeichen des Hauses, oben links) führt zurück zur Übersicht | alle | – |
| B06 | Am Handy (Oberfläche der Häuser): im Kopf Marke und «Bereiche», Kopf-Titel und runde Knöpfe weichen; Website, Anleitung und Die Stube stehen im aufgeklappten Rand | Handy | – |

## Rand

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| C01 | Der Rand führt in die acht Ansichten (Übersicht; Die Gäste: Besuche, Herkunft, Zeit; Die Website: Seiten, Verlauf, Zum Tisch; Gut zu wissen: So wird gezählt), die aktuelle ist markiert | alle | – |
| C02 | Die Zahl hinter «Besuche» ist die Zahl der Besuche von heute (ohne Besuch heute keine Zahl; geprüft jetzt und um 16 Uhr) | Rechner | – |
| C03 | Unten im Rand stehen die Wege: Die Stube, Kurzer Rundgang, Website ansehen, Anleitung (ohne Doppel zu «So wird gezählt», Messlauf 29.10.2026) | alle | – |
| C04 | «So wird gezählt» öffnet die Zählung | alle | – |
| C05 | Am Handy klappt «Bereiche» den Rand auf und zu, nach der Wahl einer Ansicht schliesst er | Handy | – |

## Zeitraum

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| D01 | Unter jedem Titel wählt man 7, 30 oder 90 Tage; die gewählte ist markiert (aria-pressed), in allen sieben Ansichten mit Zahlen | alle | – |
| D02 | Der Zeitraum gilt für alle Zahlen: 7 Tage haben weniger Besuche als 30, 30 weniger als 90; die Leiste und der Satz folgen | alle | – |
| D03 | Ein neuer Zeitraum setzt die Besuchsliste zurück (erste Karte gewählt, wieder 40 Zeilen) | alle | – |
| D04 | Die Besuchstage in der Übersicht tragen Beschriftung im richtigen Abstand (7 Tage: jeder, 30: alle fünf, 90: alle fünfzehn) | alle | – |

## Leiste

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| E01 | Die Leiste unten nennt «Du siehst Beispielwerte» und dazu den Satz «Erfunden, damit du siehst …» | alle | – |
| E03 | In der Vorführung gibt es keinen Knopf zu den echten Besuchen und kein «Neu laden» | alle | – |
| E04 | Am Handy ist die Leiste umgebrochen, nichts läuft aus dem Bild; «Als Tabelle sichern» steht dort unter der Besuchsliste (registre-haus.css blendet ihn in der Leiste aus, wie Carlton und Doldenhorn) und ist erreichbar | Handy | – |
| E05 | Schmale Handys (390 und 320 px): keine Ansicht verrutscht seitlich, kein Knopftext abgeschnitten, Rand-Klappe und Zeitraum erreichbar | Handy | – |

## Meldungen

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| F01 | Meldungen stehen als Karte mit Kreuz, höchstens drei, und verschwinden nach fünf Sekunden von selbst; das Kreuz schliesst sofort | alle | – |

## Bühne

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| G01 | Jede Ansicht beginnt mit dem Startbild der Oberfläche: Übersicht «voll» mit dem Aussenfoto des Hauses, jede andere Ansicht «Bühne» mit eigenem Bild; Foto geladen, Titel, Satz, mindestens 240 px hoch | alle | – |
| G02 | Die Übersicht zeigt im Startbild vier Kennzahlen (Besuche, Länder, heute, zum Tisch) wie Zahlen auf einem Plakat des Hauses | alle | – |
| G03 | In jeder Ansicht mit Zahlen steht über dem Inhalt das Band «Beispielwerte. Diese Zahlen sind erfunden …» | alle | – |
| G04 | Der Zeitraum sitzt im Startbild jeder Ansicht (Segment-Wahl der Oberfläche) | alle | – |

## Übersicht

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| H01 | Vier Zahlen: Besuche (mit Vergleich zum Zeitraum davor), angesehene Seiten (je Besuch), Minuten je Besuch, zum Tisch (Tisch reserviert oder Feier angefragt, Prozent der Besuche) | alle | – |
| H02 | Besuche je Tag als Säulen, eine je Tag, mit Tag und Zahl beim Darüberfahren und Datum darunter | Rechner | – |
| H03 | Zwei Spalten ohne Leere (29.10.2026): links «Woher die Gäste kommen» (fünf Orte), «Wie sie zu dir finden», «Handy oder Rechner»; rechts «Am meisten angesehen» (sechs Seiten mit Zeit im Schnitt), je mit Link zur ganzen Liste | alle | – |
| H04 | «Zuletzt zu Besuch»: die letzten fünf Besuche als Karten; ein Klick öffnet genau diesen Besuch unter «Besuche» | alle | – |
| H05 | «Alle Besuche» führt in die Besuchsliste | alle | – |

## Besuche

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| I01 | Über der Liste grenzt man ein: Alle, Zum Tisch, Formular begonnen, Anruf oder Instagram, Am Handy (je mit Zahl); die Wahl ist markiert und Zum Tisch zeigt nur Besuche mit goldenem Kreis | alle | – |
| I01b | Beim Wählen eines Filters oder bei «Weitere zeigen» bleibt die Seite ruhig: die Filterleiste und die Liste schweben nicht neu herein (und lassen sich sofort anklicken) | alle | – |
| I02 | Die Liste ist nach Tagen gegliedert («Heute», «Gestern», Wochentag, Datum; geprüft jetzt und um 16 Uhr deutscher Zeit) | alle | – |
| I03 | Einen Besuch wählen wechselt nur die Karte; die Liste bleibt, wo sie ist (Seite springt nicht nach oben), genau ein Besuch ist gewählt | alle | – |
| I04 | Die Karte nennt Ort (Land), Tag, Siegel («Tisch reserviert» / «Feier angefragt» / «Formular begonnen» / «Anruf oder Instagram» wo es zutrifft), sechs Angaben (Gekommen, Geblieben, Seiten, Gerät, Sprache, Gekommen über) und den Weg durch die Website mit Zeit je Seite | alle | – |
| I05 | Unter einer Seite im Weg stehen die Klicks dort («Reservieren begonnen», «Tisch reserviert», «Feier-Anfrage begonnen», «Feier angefragt», «Karte geöffnet» …) | alle | – |
| I06 | «Weitere zeigen» bringt jeweils 60 Besuche mehr; ganz unten steht, wie viele gezeigt werden («die neuesten 400») | alle | – |
| I07 | Ist eine Auswahl leer, steht «Kein Besuch in dieser Auswahl» statt einer leeren Liste | alle | – |
| I08 | Rechner (ab 1181 px): die Karte rechts reicht vom Kopf bis über die Leiste, der Hinweis sitzt unten; sie bleibt beim Scrollen unter dem Kopf stehen; ohne eigene Scrollfläche; ist sie mit einem langen Weg höher als der Platz, klebt sie mit dem Ende über der Leiste (G15) | Rechner | – |
| I09 | Schmal (bis 1180 px) steht die Karte über der Liste; wählt man weiter unten einen Besuch, rückt die Seite zur Karte | Handy | – |

## Herkunft

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| J01 | Länder (zehn), Gekommen über (acht, «Direkt aufgerufen» für Adresse eingetippt), Orte (mit Land), Sprache, Gerät; Anteile in Prozent, Länder auf Deutsch | alle | – |

## Zeit

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| J02 | Zeit: Besuche nach Uhrzeit (24 Säulen), nach Wochentag und Stunde (Raster 7 × 24) und nach Wochentag; oben die Spitzen (meiste Besuche, stärkster Tag, ab 18 Uhr, am Wochenende) | alle | – |

## Seiten

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| J03 | Seiten: jede Seite mit Aufrufen (absteigend sortiert), Balken, Zeit im Schnitt und wie oft sie auf dem Weg zum Tisch lag; Fusszeile «Nicht aufgeführte Seiten …» | alle | – |

## Verlauf

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| J04 | Verlauf: Besuche je Tag neben dem Zeitraum davor, Vergleichstabelle (Jetzt/Davor/Veränderung), Woche für Woche, die wichtigsten Länder im Verlauf | alle | – |

## Zum Tisch

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| J05 | Zum Tisch: neun Werte mit Prozent und gezählten Zahlen (von der Startseite und von «Drinks» zum Tisch; über «Feiern»; Reservieren ohne Abschicken; Feier-Anfrage begonnen; «Reservieren» angeklickt; Anruf oder Instagram; weiter zu Culinarium oder Dirty Chicken; Karte), «Welche Seiten vor dem Tisch lagen», der Weg zum Tisch | alle | – |

## Schweben

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| K01 | Blätter liegen beim Öffnen tief und klein (unter dem Bild), schweben beim Auftauchen nach der Uhr (2,7 s, Feder) auf ihren Platz; nicht am Scrollen geführt | Rechner | – |
| K02 | Die grossen Zahlen zoomen aus einer Vergrösserung herein (nur Zoom, keine Verschiebung seitlich: kein Überlauf) | alle | – |
| K03 | Balken und Säulen wachsen erst, wenn ihr Blatt gut zur Hälfte im Bild ist (nicht schon beim Laden, wenn es unten liegt) | Rechner | – |
| K04 | Besuchs-Kacheln (viele gleiche Zeilen) blenden nur sanft ein: kein Weg, keine Feder | alle | – |
| K05 | Am Seitenende steht alles still an seinem Platz und nichts überdeckt etwas (jede Ansicht ganz durchgescrollt) | alle | – |
| K06 | Bei «Bewegung reduzieren» steht sofort alles da, nichts schwebt | alle | – |

## Rundgang

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| L01 | Auf jeder Seite erscheint unten rechts (über der Leiste) ein Schild «Kurzer Rundgang», fünf Sekunden lang; die Maus darauf hält es; das Kreuz schliesst; automatische Prüfungen sehen es nicht | alle | – |
| L02 | «Zeigen» (oder ?rundgang) startet den Rundgang: Lichtkegel auf dem echten Bedienelement, Karte mit «1 von 5» und Titel, Text | alle | – |
| L03 | Der Rundgang geht Schritt für Schritt (Weiter, Enter, →), zurück (←), überspringt (Überspringen, Esc), endet mit «Los geht’s»; die Karte steht neben dem Ziel, nie darauf | alle | – |
| L04 | «Kurzer Rundgang» im Rand startet ihn jederzeit, auch nach einem Ansichtswechsel (der Weg bleibt im Rand) | alle | – |
| L05 | Am Handy steht die Karte unten über dem Bild; in eingebetteten Ansichten (Werkbank, Laptop) erscheint nichts | Handy | – |

## Zählung

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| M01 | «So wird gezählt» sagt, was gezählt wird, was nie gezählt wird (kein Name, keine Adresse, kein Cookie), Aufbewahrung, eigene Geräte, Grenzen, Zugang | alle | – |
| M02 | Der Dienst gibt in der Vorführung nie echte Werte heraus (ohne Schlüssel, mit falschem Schlüssel, mit ?beispiel): immer «beispiel: true» | Dienst | – |
| Z01 | Zählung auf der Website (messung.js aus vorschlag/, an den Seiten der Probe-Kopie): Öffnen zählt die Seite (Sprache des Browsers, Gerät, Sekunden); auf der Startseite Telefon der Bar, Instagram der Bar, der Knopf «Reservieren» und der Weg zu Culinarium; auf «Besuch» Reservieren begonnen und abgeschickt (erst mit «Danke») und die Karte; auf «Feiern» Anfrage begonnen und abgeschickt; die Besucherliste zeigt sie mit Schlüssel | Dienst | – |
| Z02 | Nicht gezählt: Geräte mit «nicht mitzählen», automatische Browser (webdriver), Seiten der Werkzeuge | Dienst | – |

## Server

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| N01 | Mit dem Schlüssel liefert der Dienst die echten Besuche (leer, solange nichts gezählt wurde: «leer») | Dienst | – |
| N02 | Eine gültige Zeile der Website wird angenommen (204), Beginn und Ende desselben Seitenaufrufs fassen zu einem Eintrag zusammen, Klicks und Sekunden zählen | Dienst | – |
| N03 | Ungültiges wird verworfen: falsche Sprache, fremde Ereignisse, zu lange Zeilen, Fremdzeichen, Automaten (Bots, Prüfskripte) | Dienst | – |
| N04 | Datenschutz: in der Tagesdatei steht keine Adresse der Verbindung und kein Browser-Text, nur ein Kürzel, Ort und Zeiten | Dienst | – |
| N05 | Echte Werte im Werkzeug (mit ?k=): Leiste «Ein Besuch heute», Kopf-Stand, Knopf «Neu laden» (Meldung «Neu geladen»), kein Beispiel-Band, Zahlen stimmen mit dem Dienst | Dienst | – |
| N06 | Fällt der Dienst aus (mit Schlüssel), steht «<Name> ist gerade nicht abrufbar» mit Grund und bleibt stehen | Dienst | – |
| N07 | Leerer Zeitraum: «Noch kein Besuch gezählt» mit «Beispiel ansehen» (wechselt zu Beispielwerten); wenige Besuche: «Noch wenig zu sehen? Beispiel ansehen» | Dienst | – |
| N08 | Der Test-Server antwortet nur dem eigenen Rechner und gibt keine Quelltexte (.py) und keine Tagesdateien heraus | Dienst | – |

## Anleitung

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| O01 | Die Anleitung öffnet (zweimal geladen), hat zehn Kapitel (wie im Culinarium: Zeit und Verlauf eigene Kapitel, ohne den Knopf «nicht mitzählen») in vier Themen mit Bildern aus dem Werkzeug, Bild gross mit Klick und Esc, keine toten Links | alle | – |

## Nachrechnen

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| P01 | Jede Zahl im Werkzeug (7, 30 und 90 Tage) ist genau die Rechnung aus den Rohdaten der Beispielwerte, heute zur jetzigen Uhrzeit | alle | – |
| P01b | Jede Zahl im Werkzeug (7, 30 und 90 Tage) ist genau die Rechnung aus den Rohdaten der Beispielwerte, drei Tage nach der Ablage, 9:15 Uhr (Wochentage, Wochen und Vergleichszeitraum rücken mit) | alle | – |
| P02 | Was auf dem Bildschirm steht, ist richtig aus den Zahlen gerechnet: Kennzahlen, Anteile der Ranglisten an allen Besuchen (nicht an den gezeigten Plätzen), Bänder, Sätze | alle | – |
| P03 | «Als Tabelle sichern»: lädt eine CSV mit genau den Besuchen des Zeitraums (Beispielwerte im Dateinamen und je Zeile gekennzeichnet); mit Schlüssel alle echten Besuche, nicht nur 400; ohne Schlüssel gibt der Dienst nichts heraus | Dienst | – |

## Rahmen

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| Q01 | Jeder Weg im Kopf und im Rand antwortet (Website, Anleitung, Die Stube), keine tote Adresse | alle | – |
| Q02 | «Zur Werkbank» erscheint nur, wenn aus der Werkbank geöffnet (?wb=de.k5), und führt zur Werkbank; ohne Herkunft und eingebettet nie | alle | – |
| Q03 | Fehlermelder: ein Skriptfehler landet im Browser («wildside-registre-fehler») und beim Dienst, Ladefehler nicht, höchstens 20 | Dienst | – |
| Q05 | Die Stube bekommt vom Dienst dieselben Beispielzahlen, die das Besucherbuch zur selben Zeit zeigt | Dienst | – |
| Q06 | Unter der Sicherheitsregel der Online-Fassung (CSP wie vercel.json, eingebettete Skripte gesperrt) läuft alles: Laden, Fehlermelder, Rundgang, Anleitung mit Bild gross, Tabelle sichern; keine Regelverletzung | alle | – |

## Sicherheit

| Nr. | Was die Besucherliste tut, bei Walk on the Wild Side bedient | gilt | Stand |
|---|---|---|---|
| Q04 | Dienst: fremde Herkunft 403, zu grosse Zeile 413, zu viele Anfragen 429, Quelltexte und Tagesdateien nie | Dienst | – |

