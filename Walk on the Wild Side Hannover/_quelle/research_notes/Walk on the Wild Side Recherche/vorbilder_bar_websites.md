# Vorbilder: Websites von Cocktail-/Mixology-Bars mit DJ-Abenden, Live-Musik und Private Dining (für «Walk on the Wild Side», Hannover-Linden)

Methode (für den Report-Schreiber): Am 26.10.2026 wurden alle Seiten live mit Playwright headless (Chromium für den Schnell-Check, WebKit für die Aufnahmen) aufgerufen. Erfasst wurden: Erreichbarkeit, Navigation, Schriften (computed font-family), Hintergrundfarbe, Video-/iframe-Einsatz, Laufband/Ticker, Cursor-Elemente, Buchungs- und Ticket-Anbieter, Unterseiten zu Events und Private Hire. Offizielle URLs der 50-Best-Bars wurden über den «Visit website»-Link der jeweiligen Seite bei The World's 50 Best Bars geholt, nicht geraten. «Eigene Sichtung» heisst: Text, Aufbau und Werte wurden auf der genannten URL selbst abgelesen. Firecrawl hatte kein Guthaben, deshalb gibt es keine Firecrawl-Daten. Cookie-Banner wurden, wo möglich, abgelehnt. Nirgends wurde eingeloggt.

Aufnahmen (nur intern) liegen in `_quelle/vorbilder/`, die Herkunft steht in `_quelle/vorbilder/herkunft.json`: 01 Bar Tausend, 02 krypt., 03 Brilliant Corners (+ 03b Dates-Seite), 04 Moebius Milano, 05 Double Chicken Please, 06 Superbueno, 07 Velvet, 08 Attaboy. Jeweils `-desktop.jpg` (1440 px) und `-handy.jpg` (390 px, DPR 2). Public Records war als Nr. 04 geplant. In WebKit lief der Screenshot zweimal in einen Timeout, deshalb wurde Moebius Milano als Ersatz aufgenommen.

## Kuratierte Liste: 22 Bar-Websites + Award-gelistete Seiten (was ist besonders, was lernen wir)

### Takeaway
Die besten Vorbilder für WOTWS sind nicht die berühmtesten Bars, sondern Seiten, die Musik und Nacht als Inhalt behandeln: Bar Tausend (DJ-Line-up als Startseite), Brilliant Corners (ein DJ pro Nacht, als schlichte Liste), krypt. Wien («Cocktailbar | Club», Separee mit Pauschalpreis), Moebius Milano (feste Musikformate plus Restaurant und Plattenladen), Superbueno (laute Farbe, freche Sprache, sauberes Event-Formular) und Attaboy (Bar ohne Karte, die auf der Website schlicht keine Drinks zeigt). Mehrere Top-50-Bars haben auffallend schwache oder minimalistische Seiten. Für die Gestaltung sind sie kaum Vorbilder, wohl aber für die Haltung.

### Cited Findings

**A. Top 8 (aufgenommen)**

1. **Bar Tausend, Berlin** – https://tausendberlin.com/ – Nachtleben/DJ-Bar am Bahnhof Friedrichstrasse.
   - Schwarzer Grund, Versalien in Oswald. Im Hero dreht sich ein rundes «TAUSEND»-Logo mit einem Ring aus Audio-Wellenform über einem s/w Clubfoto. Auf dem Handy steht darunter der rote CTA «CHECK LINEUP». Erfasst: 7 `<video>`-Elemente, ein Laufband (marquee) und ein eigenes Cursor-Element — [eigene Sichtung](https://tausendberlin.com/)
   - Navigation: Über uns / Musik / Bar / Cantina / Kunst / Event / Presse / Kontakt. Es ist ein langer One-Pager (ca. 16.700 px Desktop) mit Ankern. /musik/ und /event/ liefern eine 404 mit dem schönen Text «Diese Tür führt ins Leere. Hier geht's zurück in die Tausend.» — [eigene Sichtung](https://tausendberlin.com/)
   - Das Line-up steht direkt auf der Startseite, als Zeilen im Format «DO | 01.10. | 21 H / CEEE», «FR | 02.10. | 21 H / AGENT! & ROBERTA DEFLORIO», «SA | 03.10. | 21 H / SPENCER PARKER», mit Links zu Resident Advisor (ra.co). Am 26.10. waren noch Einträge vom Monatsanfang zu sehen; die Liste wird also nicht laufend gepflegt — [eigene Sichtung](https://tausendberlin.com/)
   - Tonfall: Mythos und Tür. «Hinter einer unscheinbaren Stahltür … Cocktailbar, Tanzbar und Treffpunkt für internationale DJ-Kultur» — [eigene Sichtung](https://tausendberlin.com/)
   - Lernen: Musik als Hauptinhalt, ein Datumsformat, das Tag, Datum und Uhrzeit in einer Zeile zeigt, ein CTA «Line-up». Vermeiden: grauer Fliesstext (#666 auf Schwarz, schwach lesbar), sehr lange Seite und WordPress/Divi-Ladegewicht.

2. **krypt., Wien** – https://www.krypt.bar/ – «Cocktailbar | Club» (Wix).
   - Der Hero ist ein s/w Foto von Barwand und Bar. Darauf liegt das «krypt.»-Logo in goldener Handschrift, darunter die Öffnungszeiten als grosse handgeschriebene Ziffern «19 – 1 / 19 – 2», am Desktop dazu magentafarbene Versalien «WED & THU / FRI & SAT». Die Kopfzeile heisst «All the important stuff» — [eigene Sichtung](https://www.krypt.bar/)
   - Separee mit transparentem Paket: «If your group is bigger than 15 people you can rent out our separate room or lounge area. 15–30 people Rent: 999€ includes: 3 Bottles of Cremant de Loire, 2 Bottles of Spirits Gin / Vodka, 12 side drinks» — [krypt. Separee](https://www.krypt.bar/blank)
   - Die Karte ist in Reiter gegliedert: Signatures & Drinks / Bar Food / Wine & Bubbles / Beer / Sodas / Classics, mit «No & Low ABV» und «No Alcohol» — [krypt. Menu](https://www.krypt.bar/menu)
   - Lernen: Uhrzeiten als grafisches Element, und Private Hire als ein Satz plus Preis und Inhalt, ganz ohne Formular-Bürokratie. Bei WOTWS entspräche das der langen Tafel auf der Empore.

3. **Brilliant Corners, London** (Dalston, Hi-Fi/Vinyl-Bar mit Restaurant) – https://brilliantcornerslondon.co.uk/
   - Schwarzer Bildschirm mit schwebenden kupfer- und mondfarbenen Kugeln (Plattenteller/Planeten-Anmutung). Schriften: Apercu Mono und Bauer Bodoni Bold Italic. Navigation klein geschrieben: food / drinks / dates / reservations / contact & opening times / gift cards / jobs. Dazu ein Knopf «play live stream» (Mixcloud-Einbettung) — [eigene Sichtung](https://brilliantcornerslondon.co.uk/)
   - Die «dates»-Seite ist eine reine Liste mit einem DJ pro Abend über fünf Wochen: «Mon 26 Oct 26 Pedro – Tue 27 Oct 26 Dellores & Jonathan – Wed 28 Oct 26 Gavin Kavanagh …», offene Abende stehen als «tbc» drin. Reservierung läuft über superbexperience.com — [Brilliant Corners dates](https://brilliantcornerslondon.co.uk/dates/)
   - Lernen: Radikal reduzierter Kalender (Datum + Name, sonst nichts), das wirkt souverän. Ein Live-Stream- oder Playlist-Knopf bringt Ton auf die Seite, ohne Autoplay.

4. **Moebius Milano** – https://moebiusmilano.it/eng/ – Cocktailbar + Tapa-Bistrot + Restaurant «Sperimentale» + Live-Musik + Plattenladen.
   - Hero: Vollbildfoto des vollen Raums, Logo «Œ», «BOOK A TABLE», 50-Best- und Michelin-2026-Plakette. Die Navigation trennt die Angebote: Tapa Bistrot / Sperimentale Restaurant / Cocktail Bar / Music / Press / About. Auf der Startseite sind die Kacheln mit «Moebius Live Music» und «Moebius Record Store» beschriftet — [eigene Sichtung](https://moebiusmilano.it/eng/)
   - Musikseite: zuerst die feste Regel, dann das Programm. «Ogni Lunedì e Domenica, dalle 20:00 alle 22:00 … Jazz, Blues, Swing e Bossa Nova. Ogni Giovedì, dalle 21:30 a 00:30, un Dj set in vinile accompagnerà cena e dopocena.» Danach folgen datierte Einträge mit Kurzbio (z. B. «Giovedì 8 Ottobre – Cherian …») und ein Link zur Spotify-Playlist — [Moebius Music](https://moebiusmilano.it/eng/music/)
   - Auf der 50-Best-Liste 2026 (Plätze 1–100) verlinkt — [The World's 50 Best Bars, Liste 51–100](https://www.theworlds50best.com/bars/list/51-100)
   - Lernen: Wiederkehrendes Format als Satz («jeden Donnerstag Vinyl-Set zum Dinner»), dann die konkreten Termine darunter. Passt genau zu «SESSION – Sip & Sound».

5. **Double Chicken Please, New York** – https://doublechickenplease.com/ (Shopify)
   - Schwarz, Abril Fatface + Barlow. Zwei Räume sind zwei Welten mit je eigenem Menü-Link: «FREE RANGE – Where chickens fly and dreams range free. No rules, all fun. Having fun with food and drink is highly encouraged.» und «The Coop – Drink iconic dishes as crafted cocktails …». Dazu ein Shop mit Objekten (Keramik-Hühnerschale, «Robert the Screaming Chicken») und ein eigenes «Design Studio» — [eigene Sichtung](https://doublechickenplease.com/)
   - Lernen: Ein Maskottchen (Huhn) zieht sich durch Sprache, Objekte und Shop, bei WOTWS wäre das der Leopard 🐆. Den Merch-Teil nicht kopieren, solange es keinen Merch gibt.

6. **Superbueno, New York** – https://www.superbuenonyc.com/ (Squarespace)
   - Laut: geometrische Farbflächen (Petrol/Rot/Gelb, Grund #A9E077), fette Versalien «MEXICAN AMERICAN COCKTAIL BAR», umrandeter Oval-Button «SEE OUR MENU», Laufband «SUPERBUENO GIFT CARDS ⋆». Schriften: Alfarn, Henderson Sans, Inconsolata — [eigene Sichtung](https://www.superbuenonyc.com/)
   - Private Events: Kopfzeile als Laufband «PRIVATE EVENTSPRIVATE EVENTS…», dann «BOOK YOUR NEXT EVENT AT SUPERBUENO! … ¡SALUD!». Formularfelder: Name, E-Mail, Telefon, Firma, Art des Anlasses, Datum, Start- und Endzeit, Personenzahl, Freitext, «How did you hear about us?». Technik: Tripleseat — [Superbueno Private Events](https://www.superbuenonyc.com/private-events)
   - Lernen: Lautstärke über Farbe und Ausrufezeichen, ohne dass die Seite billig wirkt. Kurzes, klares Anfrageformular.

7. **Velvet, Berlin-Neukölln** – https://velvet-bar-berlin.de/ (Framer)
   - Fast schwarz (#0A0B0A), Helvetica Neue. Hero: ein einzelner Drink mit Blüte bzw. Spargel vor Schwarz, Produktfoto-Ästhetik. Das Typosystem arbeitet mit Schrägstrichen: «/ FINE SEASONAL DRINKING», «GANGHOFERSTRASSE 1 // OPEN – DAILY FROM 19.00H /// CLOSED – TUESDAYS». Tischbuchung im Zenchef-iframe. Laut Banner nur essenzielle Cookies — [eigene Sichtung](https://velvet-bar-berlin.de/)
   - Ein FAQ erklärt das ungewöhnliche Konzept über Fragen: «How is the menu structured?», «Why don't you use citrus in your drinks?», «Can I order classic cocktails at Velvet?», «Can I book Velvet for events?». Die Antworten stecken in Akkordeons und liessen sich nicht auslesen. Gestaltung laut Impressum-Link: elelog studio — [Velvet Info/FAQ](https://velvet-bar-berlin.de/info)
   - Lernen: Ein FAQ ist die eleganteste Art, «keine Karte» zu erklären («Gibt es eine Karte? – Nein. Sag uns, worauf du Lust hast.»). Ein konsequentes Satzzeichen-System ersetzt Ornamente.

8. **Attaboy, New York/Nashville** – https://attaboy.us/ (Squarespace)
   - Hellgrau #F5F5F5, new-spirit-condensed. Auf der Startseite steht nur ein gerahmtes Foto (Hand reicht Drink vor Wellblech und Trockenblumen) mit dem Satz «just knock.». Nirgends steht ein Drink oder eine Karte; die Navigation hat nur Visit Us / Press / Book Your Event / Shop — [eigene Sichtung](https://attaboy.us/)
   - Attaboy arbeitet ohne Karte: Die Bartender fragen nach Vorlieben (Spirituose, süss/sauer/bitter) und mixen danach — [Suchergebnis-Zusammenfassung, u. a. OpenTable-Listing](https://www.opentable.co.uk/r/attaboy-new-york) (Sekundärquelle, nicht im Wortlaut geprüft)
   - Private Hire mit Humor: «PRIVATE EVENTS: Want Attaboy all to yourself? (Greedy, but we get it.) BOOK YOUR PRIVATE PARTY HERE.» Ausserdem monatliche Cocktailkurse über Tripleseat Tickets; Reservierung «limited … on OpenTable. All others are first-come, first-served» — [Attaboy Visit Us](https://attaboy.us/visit-us)
   - Lernen: Fast genau das WOTWS-Konzept. Die Site behauptet nichts über Drinks; die Einladung ist die Botschaft. Private Hire in einem frechen Satz.

**B. Weitere starke Beispiele (ohne Aufnahme)**

9. **Public Records, New York** (Sound Room, Café, Upstairs-Bar) – https://publicrecords.nyc/ – Hellgrau #EDEDED, Univers. Senkrechte Reiter am rechten Rand («EVENT CALENDAR», «FOOD + BEVERAGE»), kleine verstreute Fotos. Kalender mit Filtern «All, Club, Live, Etc. Durations». Jeder Eintrag nennt Tag, Kategorie, Uhrzeit und **Raum** («Tue 10.27 Club, Live, 7:00 pm, Sound Room … Get tickets»). Tickets über DICE, Tische über Resy (zwei Räume getrennt), Private Events separat, eigene Mailadressen je Zweck (hello@/press@/reservations@/parties@) — [eigene Sichtung](https://publicrecords.nyc/). Lernen: Raum-Angabe pro Termin (Bar unten vs. Empore oben).
10. **Nowadays, New York** (Club/Bar) – https://nowadays.nyc/ – Schwarz, Modena + Grotesk Neue. Navigation: «Programming & RSVP / Residents / Safer Space / Hours & Location / Private Events». Das Programm läuft über Resident Advisor. Die Residents-Seite zeigt Bios mit SoundCloud-Mixen. Private Events bestehen aus einem einzigen Satz plus E-Mail — [Residents](https://nowadays.nyc/resident-djs/), [Private Events](https://nowadays.nyc/private-events/). Lernen: Eine «Residents»-Seite für die SESSION-DJs, mit je einem Mix.
11. **Drink Kong, Rom** – https://www.drinkkong.com/ – Dunkel, ein Gesicht im Halbschatten, neonmagenta Outline-Schrift «DRINK KONG THINK KONG BE KONG!». Separate Nachtmarke «Nite Kong» (nitekong.com), Shop, Dresscode «Smart casual», Mindestalter 18 — [eigene Sichtung](https://www.drinkkong.com/). Lernen: Neon-Outline als Nachtsignal; ein eigener Name für das Nachtformat.
12. **Bar Leone, Hongkong** – https://www.barleonehk.com/ – Warmes Beige mit Orange. Das einzige grosse Element ist ein Laufband «COCKTAIL POPOLARI •», dazu «NO RESERVATIONS» und die Mail tuttobene@ — [eigene Sichtung](https://www.barleonehk.com/). Auf der 50-Best-Liste 2026 (1–100) verlinkt — [50 Best](https://www.theworlds50best.com/bars/list/1-50). Lernen: Ein Slogan als Laufband trägt die ganze Seite.
13. **Caretaker's Cottage, Melbourne** – https://www.caretakerscottage.bar/ – Eine einzige Seite in Terrakotta mit hellem Bogen: «A PUBLIC BAR … SMART DRINKS, TOP TUNES & FUN TIMES … No bookings, walk-ins only.» — [eigene Sichtung](https://www.caretakerscottage.bar/). 50 Best 2026 (1–100). Lernen: Ehrlicher One-Screener für eine Walk-in-Bar.
14. **Bar Snack, New York** – https://www.barsnacknyc.com/ – Creme #FFFEE7 mit Rostbraun, Laufband «dressed-up classics for dressed-down people». Die Events-Seite ist eine Hire-Anfrage für «Little Snack», einen halbprivaten Hinterraum für bis zu 25 Gäste, «not available for hire on Fridays or Saturdays», Antwort «within 36 hours» — [Bar Snack Events](https://www.barsnacknyc.com/events). Lernen: Klare Regeln für den Privatraum (Kapazität, gesperrte Tage, Antwortzeit).
15. **Line, Athen** – https://lineathens.gr/ – Handgezeichnetes Raster aus schwarzen Linien mit Collage-Bildern, Schrift BaksoSapiPro, Manifest «LINE BELIEVES IN THE METHOD OF ANARCHY …», Teaser «Tasting dinner for a good cause». Konzept und Design: Eleni Sakali — [eigene Sichtung](https://lineathens.gr/). 50 Best 2026 (1–100). Lernen: Die Startseite als Karte aus Kästchen.
16. **The Clumsies, Athen** – https://www.theclumsies.gr/ – Gezeichnete Hausfassade, das Menü sitzt im Dach. Der private Raum heisst «KNOCK THE ROOM». Das Konzept ist als Rezept geschrieben: «A fail-proof recipe. Ingredients and quantities: Many "whoops!"» — [eigene Sichtung](https://www.theclumsies.gr/). Lernen: Sprache mit Witz und ein Name für den Privatraum.
17. **Paradiso, Barcelona** – https://paradiso.cat/en/ – Schwarz, Vidaloka-Serif-Logo mit Planet, «A universe of temptations». Drinks stehen mit Zutaten und Geschmacksworten da (z. B. «Perception … Gastronomic, umami, tropical»). 4 Videos, Buchung über carbonaraapp — [eigene Sichtung](https://paradiso.cat/en/). 50 Best 2026 (1–100).
18. **Little Red Door, Paris** – https://www.lrdparis.com/ – Ein roter Block als Hero mit Oswald «Playfully Pushing Boundaries» und «Walk-ins Welcomed». Kaum weitere Navigation — [eigene Sichtung](https://www.lrdparis.com/). 2026 auf Platz 93 — [Sortiraparis](https://www.sortiraparis.com/en/where-to-eat-in-paris/bars-cafes/guides/302448-the-world-s-50-best-bars-2026-a-parisian-bar-makes-the-51-100-best-bars-in-the-world-list).
19. **Himkok, Oslo** – https://www.himkok.no/ – Schwarz, Futura + Palatino kursiv, «Pronounced: {Him-kook} Translation: Moonshine». Navigation inkl. EVENT und «HIRE A BARTENDER» — [eigene Sichtung](https://www.himkok.no/). 50 Best 2026 (1–100). Lernen: Die Aussprache des Namens als Hero-Witz.
20. **Tayēr + Elementary, London** – https://tayer-elementary.com/ – Dunkel (#15131B), Staat Bold, grosse gestapelte Wortmarken (tayer / elementary / tayer studios / tayer shop), 5 Videos. **Achtung:** Laut Site «TEMPORARILY CLOSED DUE FIRE IN OUR BUILDING», «Walk in only / no bookings» — [eigene Sichtung](https://tayer-elementary.com/). Nur noch bedingt Vorbild.
21. **Buck and Breck, Berlin** – https://www.buckandbreck.com/ – Bewusstes Anti-Design: eine schwarze Seite, Arial-Versalien, «OPEN FROM *19.00 TO 2.00*», Telefon, «FOR PRIVATE EVENTS INFO@…», Gin-Presseinfos — [eigene Sichtung](https://www.buckandbreck.com/). Bei den Mixology Bar Awards 2026 «Bar-Institution» — [tageskarte.io](https://www.tageskarte.io/gastronomie/detail/bar-des-jahres-2026-das-sind-die-gewinner-der-mixology-bar-awards.html).
22. **Becketts Kopf, Berlin** – https://becketts-kopf.de/ – Schwarz mit Cinzel, ein gerahmter Infokasten «Walk-ins Welcome!». Idee «Drinks zum Dinner»: Drinks werden in Berliner Partner-Restaurants zum Essen bestellt — [eigene Sichtung](https://becketts-kopf.de/). Gestalterisch schwach; die /drinks/-Unterseite ist eine 404.

**C. Geprüft und verworfen (schwach oder nicht passend)**
- Little Link Köln (https://www.littlelink.de/): Elementor-Slider und generische Teaserkacheln («Erfolgsgastronom des Jahres 2024»), eher ein Event- und Catering-Shop — [eigene Sichtung](https://www.littlelink.de/)
- Café La Trova Miami: Vollbild-Modal «FOR RESERVATIONS, CLICK HERE» über einem Partyplakat — [eigene Sichtung](https://www.cafelatrova.com/)
- Sweet Liberty Miami: Popup «Get $25 … Enter email to claim» — [eigene Sichtung](https://www.mysweetliberty.com/)
- Limantour Mexiko-Stadt (https://limantour.tv/): weisses Standard-WordPress, schöner Satz «The bar is open, so is my heart» — [eigene Sichtung](https://limantour.tv/)
- Sips Barcelona: Lade-Spinner, Cookie-Banner nur mit «I AGREE» (keine Ablehnen-Option), Design Corberó Studio — [eigene Sichtung](https://sips.barcelona/)
- Schmuck NYC: nur Wortmarke «schmuck.» und Video — [eigene Sichtung](https://www.schmucknyc.com/)
- Le Lion Hamburg: Shopify-Shop-Optik, «NO RESERVATIONS – just come by» — [eigene Sichtung](https://www.lelion.net/)
- Satan's Whiskers London: Site live («NOW OPEN! – PLEASE CALL … FOR RESERVATIONS», Flaschen-Shop), aber Analyse brach ab, deshalb nicht bewertet — [eigene Sichtung](https://www.satanswhiskers.com/)
- Nicht gefunden oder ohne eigene Site: Kwānt (50 Best verlinkt nur Instagram), A Bar with Shapes for a Name (nur Instagram), Handshake Speakeasy (Site ist im Kern ein Buchungsformular) — [50 Best Kwānt](https://www.theworlds50best.com/bars/the-list/kwant.html), [50 Best Shapes](https://theworlds50best.com/bars/the-list/a-bar-with-shapes-for-a-name.html)
- Falsche Domains (Achtung bei Verlinkung): coahk.com ist eine fremde Film-Seite (richtig: https://coa.com.hk/), kumiko.bar steht zum Verkauf, twoschmucks.com ist eine Parkseite — [eigene Sichtung]

**D. Award- oder Siteinspire-gelistete Bar- und Nightlife-Seiten**
- **Mùn Rooftop Cocktail Bar, Rom** – https://munrooftoprome.com/ – Awwwards Honorable Mention, 10.08.2025, Studio Idee Materia. Elemente: Hero-Animation, Cocktail-Galerie, GSAP, Palette #222944 / #92ABA0 — [Awwwards](https://www.awwwards.com/sites/mun-rooftop-cocktail-bar). Live: nummerierte Navigation «1. SIGNATURE 2. MENU 3. SPACES 4. DOUBLETREE 5. EVENTS». Die Karte ist als Stadtspiel aufgebaut: «TEN DISTRICTS, TEN STORIES, TEN COCKTAILS … CHOOSE YOUR DISTRICT». Private Hire läuft unter «SPACES – RENT THE MÙN, THE PRIVATE ROOFTOP» (Gala-Dinner, Firmen, Geburtstage), Tische über SevenRooms — [Mùn](https://munrooftoprome.com/), [Spaces](https://munrooftoprome.com/spaces/). Hotelbar (DoubleTree), aber das beste live geprüfte Award-Beispiel.
- **Spiritland, London** (Listening-Bar/Hi-Fi-Venue) – https://spiritland.com/ – laut Suchergebnis bei Siteinspire gelistet (Cafés/Bars, Events, Music, Black & White) — [Siteinspire-Suchergebnis](https://www.siteinspire.com/website/6980-spiritland) (Detailseite gab HTTP 500). Live: «SPIRITLAND – come home to music», «Spiritland at the Barbican opens this October», Venue-Übersicht «See what's on at our venues» — [eigene Sichtung](https://spiritland.com/)
- **OMNIA Nightclub, Las Vegas** – Awwwards Nominee (Dez. 2015) — [Awwwards](https://www.awwwards.com/sites/omnia-nightclub). Die Domain leitet heute auf eine Tao-Group-Venue-Seite um (Event Calendar / VIP / Buy Tickets), das ausgezeichnete Design ist also nicht mehr online — [eigene Sichtung](https://omnianightclub.com)
- **The Sayers Club, Hollywood** – Awwwards Honorable Mention (Juli 2018) — [Awwwards](https://www.awwwards.com/sites/the-sayers-club). Die Domain lädt noch, zeigte im Check aber fast keinen Inhalt — [eigene Sichtung](https://www.thesayersclub.com/)
- Offline/kaputt: «A Bar Called Gemma» (Stockholm, Awwwards HM 12.02.2024, SABR; Palette #1D1B1E/#FD2600, Seitennavigation, Scroll-Animationen) gibt heute eine 404 — [Awwwards](https://www.awwwards.com/sites/a-bar-called-gemma). «VÖLLEREI Restaurant & Bar» (Awwwards SOTD 2017): Domain voellerei.at löst nicht mehr auf — [Awwwards](https://www.awwwards.com/sites/vollerei-restaurant-bar). «Piranha Bar» (HM 19.05.2026) ist ein Kreativstudio, keine Bar — [Awwwards](https://www.awwwards.com/sites/piranha-bar).

### Inferences
- Für WOTWS sind die Anordnungen von Bar Tausend (Line-up vorn), Brilliant Corners (Kalender als Liste), krypt. (Separee mit Paketpreis), Moebius (Regel + Termine) und Attaboy (keine Karte, nur Einladung) die direktesten Vorlagen. Superbueno und Drink Kong liefern die «laute» Farb- und Neon-Sprache.
- Award-Seiten (Awwwards) für Bars sind selten, oft Hotelbars und veralten schnell: 3 von 5 geprüften Award-Bar-Sites sind tot oder umgebaut. Bei einer kleinen Bar zählt Pflegbarkeit mehr als Effekt.
- Die besten deutschen Barseiten (Velvet, Bar Tausend) sind deutlich besser als die Mehrheit. Buck and Breck und Becketts Kopf setzen auf Kargheit; das passt zu ihrer Speakeasy-Haltung, aber nicht zu «loud, night, spontaneous».

### Gaps
- Public Records konnte nicht aufgenommen werden (WebKit-Timeout); nur Text und Struktur sind belegt.
- Mixology-Preisträger 2026 (Green Door Berlin, Dunlin Innsbruck, Late Bloomers Zürich, Nick & Nora Hamburg, Bar Basta Berlin) wurden nicht gestalterisch bewertet. Green Door hat eine klassische Site (https://www.greendoor.de/de/); für die übrigen wurde in der Zeit keine verlässliche Domain gefunden.
- Mehrere angefragte Bars haben keine nennenswerte eigene Site (Kwānt, Shapes, Bar Benfiddich: 50 Best verlinkt einen Ameblo-Blog) oder wurden nicht geprüft (Herbarium, Zum Wohl Bar, Gekkos, Kumo, «Die Rote Bar»: keine sichere Zuordnung oder Domain in der verfügbaren Zeit).
- Awwwards-Listen liessen sich headless nicht laden (Timeout). Award-Funde stammen aus WebSearch und WebFetch der einzelnen Awwwards-Seiten; es kann weitere passende Einträge geben.

## Welche Muster vermitteln «Nacht, Musik, Spontanität» am besten?

### Takeaway
Dunkler Grund ist die Regel bei Nacht-/Musikbars (Tausend, Brilliant Corners, Nowadays, Drink Kong, krypt., Velvet), aber die stärksten Seiten setzen ein lautes Signal darauf: Neon-Outline (Drink Kong), Magenta plus Handschrift (krypt.), rotierende Wellenform (Tausend), schwebende Planeten (Brilliant Corners). Laufbänder mit einem Slogan sind verbreitet (Bar Leone, Bar Snack, Superbueno, Tausend). «Spontan» entsteht vor allem durch Sprache und Walk-in-Botschaften, kaum durch Technik.

### Cited Findings
- Dunkle Hintergründe (computed background) gemessen bei Tausend (#000), Brilliant Corners (#000), Nowadays (#000), Velvet (#0A0B0A), Double Chicken Please (#000), Paradiso (#0A0A0A), Himkok (#000), Becketts Kopf (#000), Buck and Breck (#000) — [eigene Sichtung, siehe URLs oben]
- Helle Gegenbeispiele mit Charakter: Public Records (#EDEDED, Univers), Attaboy (#F5F5F5), Bar Snack (#FFFEE7 + Rostbraun), Superbueno (#A9E077 + Farbflächen), Bar Leone (Beige/Orange) — [eigene Sichtung]
- Laufband/Ticker gemessen bei Bar Tausend, Superbueno, Bar Snack («dressed-up classics for dressed-down people»), Bar Leone («COCKTAIL POPOLARI •») — [Bar Snack](https://www.barsnacknyc.com/), [Bar Leone](https://www.barleonehk.com/)
- Video: Tausend (7 Video-Elemente), Tayēr (5), Paradiso (4), krypt. (1), Schmuck (Vollbildvideo). Die meisten guten Seiten kommen ohne Video-Hero aus (Attaboy, Velvet, Brilliant Corners, Superbueno) — [eigene Sichtung]
- Ton auf der Website ohne Autoplay: «play live stream» (Brilliant Corners, Mixcloud), Spotify-Playlist (Moebius), SoundCloud-Mixe der Residents (Nowadays) — [Brilliant Corners](https://brilliantcornerslondon.co.uk/), [Moebius Music](https://moebiusmilano.it/eng/music/), [Nowadays Residents](https://nowadays.nyc/resident-djs/)
- Spontaneität über Sprache: «just knock.» (Attaboy), «Walk-ins Welcomed» (Little Red Door), «No bookings, walk-ins only» (Caretaker's Cottage), «NO RESERVATIONS – just come by» (Le Lion), «Walk-ins Welcome!» (Becketts Kopf) — [Attaboy](https://attaboy.us/), [LRD](https://www.lrdparis.com/), [Caretaker's](https://www.caretakerscottage.bar/), [Le Lion](https://www.lelion.net/), [Becketts Kopf](https://becketts-kopf.de/)
- Öffnungszeiten als Gestaltungselement: krypt. (handgeschriebene «19 – 1 / 19 – 2»), Velvet (Schrägstrich-Zeile «OPEN – DAILY FROM 19.00H /// CLOSED – TUESDAYS») — [krypt.](https://www.krypt.bar/), [Velvet](https://velvet-bar-berlin.de/)
- Eigene Cursor-Elemente nur bei wenigen erfasst (Tausend, Becketts Kopf, Bar Leone, Panda & Sons, Café La Trova), bei keiner prägend — [eigene Sichtung]
- Award-Beispiel Mùn: GSAP-Hero-Animation und Mond-Thema mit gedeckter Nachtpalette (#222944/#92ABA0) — [Awwwards](https://www.awwwards.com/sites/mun-rooftop-cocktail-bar)

### Inferences
- Für WOTWS bietet sich an: dunkler Grund und ein einziges lautes Signal (Leoparden-Akzent/Neon), dazu eine Slogan-Zeile als Laufband («let's go wild 🐆 · sexy drinks · no menu ·») und Öffnungszeiten als grosse Typo. Ein Video-Hero ist nicht nötig; ein Sound-Knopf (SESSION-Mix) ist origineller.
- Cursor-Effekte bringen wenig (sie fehlen bei den stärksten Beispielen und tun auf dem Handy nichts).

### Gaps
- Die Bewegung (Scroll-Animationen, Übergänge) wurde nur über DOM-Merkmale und Standbilder erfasst; Timing und Qualität der Animationen sind nicht belegt.

## Wie zeigen Bars ohne feste Karte ihre Drinks?

### Takeaway
Die konsequenteste Lösung ist, gar keine Drinks zu zeigen und stattdessen die Einladung (Attaboy: «just knock.»). Daneben gibt es drei brauchbare Muster: FAQ-Fragen, die das Konzept erklären (Velvet), Geschmackswörter statt Rezepten (Paradiso) und ein spielerischer Einstieg über eine Wahl (Mùn: «Choose your district»). Für WOTWS passt eine Kombination: keine Karte, aber ein interaktives «Sag uns, was du magst».

### Cited Findings
- Attaboy (Bar ohne Karte) zeigt auf der Site keine Drinks; Startseite «just knock.», Navigation ohne Menü — [Attaboy](https://attaboy.us/); No-Menu-Prinzip laut [Suchergebnis/OpenTable](https://www.opentable.co.uk/r/attaboy-new-york)
- Velvet erklärt Besonderheiten über FAQ-Fragen («How is the menu structured?», «Why don't you use citrus in your drinks?», «Can I order classic cocktails at Velvet?») — [Velvet Info](https://velvet-bar-berlin.de/info)
- Paradiso beschreibt Drinks mit Zutaten und drei Geschmackswörtern (z. B. «Perception … Gastronomic, umami, tropical») — [Paradiso](https://paradiso.cat/en/)
- Mùn: «TEN DISTRICTS, TEN STORIES, TEN COCKTAILS … CHOOSE YOUR DISTRICT» — [Mùn](https://munrooftoprome.com/)
- Double Chicken Please gibt jedem Raum eine eigene Drink-Welt mit Zweizeiler und Menü-Link («Free Range» vs. «The Coop») — [DCP](https://doublechickenplease.com/)
- Bar Snack und Bar Leone verdichten das Angebot auf einen Slogan statt einer Liste («dressed-up classics for dressed-down people», «COCKTAIL POPOLARI») — [Bar Snack](https://www.barsnacknyc.com/), [Bar Leone](https://www.barleonehk.com/)

### Inferences
- WOTWS-Idee (eigene Ableitung, nicht kopiert): ein kleines «Wähl deine Richtung»-Spiel (z. B. fruchtig / bitter / rauchig / sexy) als Vorgeschmack auf das Gespräch an der Bar, ohne Preise und ohne Rezepte. Dazu Fotos echter Drinks im Velvet-Stil (ein Glas vor Schwarz) und ein FAQ «Gibt's eine Karte? Nein.»
- Falstaff 91 Punkte und die Gastbartender-Schichten gehören als Beweis daneben (Zitat-Zeile wie bei Superbueno mit dem NYT-Zitat).

### Gaps
- Die genauen FAQ-Antworten von Velvet (z. B. zur Karte) waren im DOM nicht lesbar.

## Wie werden Eventkalender, DJ-Line-ups und wiederkehrende Formate elegant gezeigt?

### Takeaway
Die besten Kalender sind Textlisten: eine Zeile pro Abend mit Datum und Namen (Brilliant Corners), oder Tag | Datum | Uhrzeit | Act (Bar Tausend). Wiederkehrende Formate werden zuerst als Regel in einem Satz formuliert und dann mit Terminen gefüllt (Moebius). Musik-Venues ergänzen Filter, Raumangabe und Ticketlink (Public Records) sowie eine Residents-Seite mit Mixen (Nowadays). Tickets und Line-ups werden meist an RA oder DICE ausgelagert.

### Cited Findings
- Brilliant Corners: Liste über ca. fünf Wochen, Format «Mon 26 Oct 26 Pedro», offene Abende «tbc» — [dates](https://brilliantcornerslondon.co.uk/dates/)
- Bar Tausend: «DO | 01.10. | 21 H / CEEE», Links zu ra.co. Am 26.10. standen noch Oktober-Anfangstermine oben (Pflegeproblem) — [Tausend](https://tausendberlin.com/)
- Moebius: Regel («ogni Giovedì 21:30–00:30 Dj set in vinile accompagnerà cena e dopocena»; Mo/So 20–22 Jazz/Blues/Swing/Bossa Nova), dann datierte Einträge mit Kurzbio, dazu Spotify-Playlist — [Moebius Music](https://moebiusmilano.it/eng/music/)
- Public Records: Filter «All, Club, Live, Etc. Durations». Eintrag mit Tag, Kategorie, Uhrzeit, Raum («Sound Room», «Upstairs») und «Get tickets» (DICE) — [Public Records](https://publicrecords.nyc/)
- Nowadays: «Programming & RSVP» verlinkt auf RA. «Residents» als eigene Seite mit Bios und SoundCloud-Mixen — [Nowadays](https://nowadays.nyc/), [Residents](https://nowadays.nyc/resident-djs/)
- Mùn: Events-Seite mit nächstem Datum («OCTOBER 30 – RESERVE NOW») plus Kontaktformular — [Mùn Events](https://munrooftoprome.com/events/)

### Inferences
- Für «SESSION – Sip & Sound», Konzerte und Gastbartender eignet sich eine einzige Liste mit Format-Kennzeichen (SESSION / LIVE / GUEST SHIFT / DINNER) und, wie bei Public Records, der Raum-Angabe (Bar vs. Empore). Die Regel steht oben («jeden Freitag SESSION ab 21 Uhr»), die nächsten 4–6 Termine darunter, vergangene Termine fallen automatisch raus.
- Pflegbarkeit ist entscheidend: Bar Tausend zeigt, wie schnell ein Line-up auf der Startseite veraltet. Die Liste sollte von der Bar selbst pflegbar sein oder aus einer Quelle gespeist werden (z. B. Instagram, RA oder eine einfache Tabelle).

### Gaps
- Wie Bar Tausend und Brilliant Corners intern pflegen (CMS-Workflow), ist nicht belegt.

## Wie wird Private Hire / eine einzelne lange Tafel angeboten?

### Takeaway
Gut gemacht ist Private Hire kurz, konkret und im Ton der Bar: ein Satz plus Kapazität, Preis oder Paket (krypt.: 15–30 Personen, 999 € inkl. 3 Crémant, 2 Flaschen Spirits, 12 Filler). Klare Regeln helfen (Bar Snack: bis 25 Gäste, nicht Fr/Sa, Antwort in 36 Stunden). Ein freches Mikro-Wording kommt gut an (Attaboy: «Greedy, but we get it.»). Ein strukturiertes Formular gibt es nur, wo es nötig ist (Superbueno/Tripleseat). Ein Raum mit eigenem Namen wird zur Marke («KNOCK THE ROOM», «Little Snack», «Separee», «Rent the Mùn»).

### Cited Findings
- krypt.: Separee/Lounge ab 15 Personen, «15–30 people Rent: 999€ includes: 3 Bottles of Cremant de Loire, 2 Bottles of Spirits Gin / Vodka, 12 side drinks», Firmenevents per Mail — [krypt. Separee](https://www.krypt.bar/blank)
- Bar Snack: «Little Snack is our semi-private back room, perfect for events of up to 25 guests … not available for hire on Fridays or Saturdays … we'll respond to you within 36 hours» — [Bar Snack Events](https://www.barsnacknyc.com/events)
- Attaboy: «Want Attaboy all to yourself? (Greedy, but we get it.) BOOK YOUR PRIVATE PARTY HERE.» Dazu private Cocktailkurse für bis zu 10 Personen — [Attaboy Visit Us](https://attaboy.us/visit-us)
- Superbueno: Formular mit Anlass, Datum, Start/Ende, Personenzahl, Freitext, «How did you hear about us?», abgeschlossen mit «¡SALUD!» (Tripleseat) — [Superbueno Private Events](https://www.superbuenonyc.com/private-events)
- The Clumsies: privater Raum als eigener Menüpunkt «KNOCK THE ROOM» — [The Clumsies](https://www.theclumsies.gr/)
- Mùn: «SPACES – RENT THE MÙN, THE PRIVATE ROOFTOP» für Gala-Dinner, Business-Events, Geburtstage und private Partys — [Mùn Spaces](https://munrooftoprome.com/spaces/)
- Nowadays und Buck and Breck: Private Events nur als ein Satz plus E-Mail — [Nowadays](https://nowadays.nyc/private-events/), [Buck and Breck](https://www.buckandbreck.com/)
- Moebius: Restaurant («Sperimentale», Do–Sa 19–22:30) und Bar sind getrennt navigierbar, eigene Mailadresse für Events (eventi@) — [Moebius](https://moebiusmilano.it/eng/)

### Inferences
- Für die lange Tafel auf der Empore heisst das: ein eigener Name (z. B. «Die Tafel» / «Empore»), ein grosses Foto des Tischs von oben, Kapazität, was inklusive ist (Bartender mixt für die Tafel, Plattenwahl), Anfrage über ein Mini-Formular mit Datum, Personen und Anlass. Ton frech wie Attaboy.

### Gaps
- Preise und Pakete für Dinner-Tafeln (nicht Separee) bei Vorbild-Bars wurden nicht gefunden; nur krypt. nennt einen Preis.

## Was vermeiden die besten (Klischees)?

### Takeaway
Die starken Seiten verzichten auf Popups, Rabatt-Overlays, generische Slider, Stockfoto-Cocktails und lange Texte. Gehäuft treten diese Klischees bei den schwächeren Seiten auf (Café La Trova, Sweet Liberty, Little Link). Speakeasy-Goldornamentik und Art-déco-Klischees fehlen bei den besten durchweg.

### Cited Findings
- Vollbild-Modal «FOR RESERVATIONS, CLICK HERE» über einem Partyplakat beim Laden — [Café La Trova](https://www.cafelatrova.com/)
- Rabatt-Popup «Get $25 … Enter email to claim» beim Laden — [Sweet Liberty](https://www.mysweetliberty.com/)
- Newsletter-Popup über der Schliessungs-Meldung — [Tayēr + Elementary](https://tayer-elementary.com/)
- Generischer Elementor-Slider mit Teaserkacheln — [Little Link](https://www.littlelink.de/)
- Cookie-Banner ohne Ablehnen-Option («I AGREE» only) — [Sips](https://sips.barcelona/). Gegenbeispiel: Velvet setzt nur essenzielle Cookies — [Velvet](https://velvet-bar-berlin.de/)
- Seiten ohne Inhalt außer Logo/Video bzw. Spinner (Schmuck, Sips) — [Schmuck](https://www.schmucknyc.com/), [Sips](https://sips.barcelona/)
- Veraltete Termine auf der Startseite — [Bar Tausend](https://tausendberlin.com/)
- Die besten nutzen genau einen Satz als Haltung statt Absätzen: «just knock.», «Playfully Pushing Boundaries», «Fine seasonal drinking», «Smart drinks, top tunes & fun times» — [Attaboy](https://attaboy.us/), [LRD](https://www.lrdparis.com/), [Velvet](https://velvet-bar-berlin.de/), [Caretaker's](https://www.caretakerscottage.bar/)

### Inferences
- Für WOTWS vermeiden: Popups, Stock-Cocktails, Gold-Speakeasy-Schnörkel, «Willkommen auf unserer Website»-Text, Slider, Kalender mit vergangenen Terminen, Cookie-Zwang. Leopardenmuster nur als Akzent einsetzen, nicht als Tapete, sonst wird es schnell zum Kostüm.

### Gaps
- Es gibt keine Nutzerdaten (Conversion, Buchungen) dazu, welche Muster tatsächlich mehr Gäste bringen; die Bewertung ist gestalterisch.
