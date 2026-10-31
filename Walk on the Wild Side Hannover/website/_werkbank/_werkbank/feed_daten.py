"""Instagram-Feed von Walk on the Wild Side als Idee (Werkbank, Nachtbau 31.10.2026). Bauart und Aufbau aus dem Feed des Culinarium
(Fassung 3 «Fortsetzung», 29.10.2026): der echte Feed bleibt, darüber die nächsten 60 Beiträge in der Reihenfolge des Postens.

Das Profil: @walkonthewildside_hannover, «Walk on the Wild Side | Nachbarschafts Mixology Bar», 82 Beiträge, 2.680 Follower, 331 gefolgt,
Bio «Drinks | Events | private Veranstaltungen | Tastings … Do 19:00-01:00 | Fr & Sa 19:00-02:00 … Schreib uns eine DM oder ruf an»
(_quelle/research_notes/…/programm_zeiten_kooperationen.md, Stand 26.10.2026). Neuester Beitrag: SESSION mit den Ghazouani Brothers (13.10.2026).
Heute im Profil der Werkbank: die 39 Beiträge mit Bild aus _quelle/ig/ (herkunft.json, beitraege.md), neuester zuerst (feed_leicht.py).

Die nächsten 60 (Robert zum Culinarium: «damit wir jetzt diese 60 Beiträge darauf aufbauen können»): ein Jahr der Bar in Folgen, von November
2026 an. Drinks von Momo und seine drei Techniken, die SESSION-Abende (samstags 21 bis 1 Uhr, ohne Eintritt; ohne erfundene Namen und Daten),
Konzerte am Donnerstag, die Decke, Falstaff Bar Guide 2027 mit 91 Punkten, die Feste (Geburtstag der Bar, Silvester ab mittags, Valentinstag
mit Rudi, Tanz in den Mai), Feiern auf der Empore und in der ganzen Bar, die Bar ausser Haus. Die SESSION-Plakate der Bar kommen «Aus dem Archiv»
wieder (einzige Ausnahme im Bestandsabgleich, BESTAND_AUSNAHMEN). Alles andere: Fotos aus dem Bildregister der Website (website/assets/bild),
die noch nicht auf dem Profil stehen (feed_bestand.py im Kit prüft jedes), keine Gästefotos Dritter, keine erzeugten Bilder.
Kleid: Nacht #130E0D, Creme #F2E9DC wie die weissen Plakate der Bar, Gold nur als Haarlinie und Etikett, Rot nur in der Wortmarke,
Ultramarin und Plakatrot nur bei SESSION. Titel Prata, Lauf Hanken Grotesk, Etiketten Hanken gesperrt. Texte zu den Beiträgen: Tasty Studios,
Zitat von Momo aus der Website (drinks.html). Arten für den Nachbar-Abgleich: text, session, plakat, cover, drink, mensch, raum, bar, leute, musik, feier."""
import glob, os, re
import feed_bogen

_HIER = os.path.dirname(os.path.abspath(__file__))
_WB = os.path.dirname(_HIER)
_WEB = os.path.dirname(_WB)
_HAUS = os.path.dirname(_WEB)


def quelle(key):
    """Größte Fassung des Fotos im Bildregister der Website (website/assets/bild/<key>-<breite>.webp)."""
    b = sorted(int(m.group(1)) for p in glob.glob(os.path.join(_WEB, 'assets', 'bild', key + '-*.webp')) if (m := re.fullmatch(re.escape(key) + r'-(\d+)\.webp', os.path.basename(p))))
    if not b:
        raise FileNotFoundError(key)
    return os.path.join(_WEB, 'assets', 'bild', f'{key}-{b[-1]}.webp')


# Die Wortmarke der Bar als Bild je Farbe (aus dem Kleid, unverändert; die Tafeln werden über file:// gesetzt, darum Dateien statt Maske)
_FEED = os.path.join(_WB, 'feed')
os.makedirs(_FEED, exist_ok=True)
_MARKE = open(os.path.join(_HAUS, '_werkzeuge', 'oberflaeche', 'kleid', 'wildside-marke.svg'), encoding='utf-8').read()
for _n, _f in (('rot', '#F0323F'), ('creme', '#F2E9DC'), ('nacht', '#130E0D')):
    _s = _MARKE.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1296 1600">', f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1296 1600" color="{_f}">', 1)
    _s = _s.replace('</svg>', '<use href="#wm" xlink:href="#wm" width="1296" height="1600"/></svg>') if '<use' not in _s else _s
    open(os.path.join(_FEED, f'marke-{_n}.svg'), 'w', encoding='utf-8').write(_s)

PROFIL = {'name': 'walkonthewildside_hannover', 'titel': 'Walk on the Wild Side | Nachbarschafts Mixology\u00a0Bar', 'art': 'Bar',
          'bio': ['Drinks | Events | private Veranstaltungen | Tastings', 'Do 19 bis 1 Uhr · Fr und Sa 19 bis 2 Uhr', 'Haasemannstraße 13, Linden · Schreib uns eine DM oder ruf\u00a0an'],
          'link': '+49 163 3909578',
          'zahlen': {'beitraege': '82', 'follower': '2.680', 'gefolgt': '331'}, 'stand': '26.10.2026'}
HIGHLIGHTS = [('Zeiten', quelle('schild-ecke'), .5), ('SESSION', quelle('p-1710'), .5), ('Drinks', quelle('glas-coupe'), .5),
              ('Konzerte', quelle('saengerin-kunde'), .5), ('Feiern', quelle('an-empore'), .5)]
TON = (.98, 1.03, 1.0, .99)
REGEL = 'bogen'
SEITE = dict(
    titel=['Wie es', 'weitergeht.'],
    text1='Euer Feed bleibt, wie er ist. Darauf bauen die nächsten 60 Beiträge auf, so wie ihr sie nach und nach postet: Momos Drinks und seine Techniken, die SESSION-Abende, die Decke, Falstaff mit 91 Punkten, der Geburtstag der Bar, Silvester ab mittags, Valentinstag, Feiern auf der Empore.',
    text2='Kein Foto, das schon auf eurem Profil steht, kommt nochmal vor; nur eure SESSION-Plakate zeigen wir gezielt wieder, «Aus dem Archiv». Mit dem Schalter seht ihr euren Feed heute und mit den nächsten 60; die Nummern zeigen die Reihenfolge zum Posten.',
    aufbau='Die nächsten 60 Beiträge über eurem heutigen Feed, nummeriert in der Reihenfolge des Postens',
    texte='Ideen von mir, Zeilen von der Bar und von Momo',
    bilder='eure eigenen Fotos, die noch nie gepostet wurden, und eure SESSION-Plakate')

_WELLE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='360' height='240' viewBox='0 0 360 240'%3E"
          "%3Cpath d='M-360 60 C-300 10 -240 10 -180 60 S-60 110 0 60 S120 10 180 60 S300 110 360 60 S480 10 540 60 S660 110 720 60' fill='none' stroke='%23D21C0A' stroke-width='46'/%3E"
          "%3Cpath d='M-360 180 C-300 130 -240 130 -180 180 S-60 230 0 180 S120 130 180 180 S300 230 360 180 S480 130 540 180 S660 230 720 180' fill='none' stroke='%23D21C0A' stroke-width='46'/%3E%3C/svg%3E\") 0 0/360px 240px")   # Linie läuft über die Kachel hinaus: keine Kerben an der Kachelgrenze
BOGEN_CSS = (
    "@font-face{font-family:'Prata';src:url('../assets/schrift/prata-latin.woff2') format('woff2');font-weight:400}"
    "@font-face{font-family:'Hanken';src:url('../assets/schrift/hanken-latin.woff2') format('woff2');font-weight:100 900}"
    '.st{--nacht:#130E0D;--platte:#1C1513;--creme:#F2E9DC;--gold:#D8B264;--rot:#F0323F;--ultra:#1A00AA;--plakat:#D21C0A}'
    '.n,.w,.s{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:170px 130px}'
    '.n{background:radial-gradient(120% 90% at 50% 0%,#261E1A 0%,#130E0D 62%);color:var(--creme)}'
    '.w{background:var(--creme);color:var(--nacht)}'
    '.s{background:var(--creme) ' + _WELLE + ';color:var(--ultra)}'
    # Eckschild: Gold-Haarlinie innen, das Raster zeigt 3:4, also Abstand zum Rand
    '.n::before,.w::before{content:"";position:absolute;inset:92px 104px;border:1.5px solid rgba(216,178,100,.7);border-radius:22px;pointer-events:none}'
    '.w::before{border-color:rgba(122,92,36,.55)}'
    '.wm{position:absolute;top:150px;left:50%;width:96px;height:auto;transform:translateX(-50%)}'
    '.ki2{font:500 24px/1.3 Hanken,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:40px}'
    '.w .ki2{color:#7A5C24}'
    '.ti{font:400 124px/1.04 Prata,Georgia,serif;text-wrap:balance}'
    '.zi{font:400 92px/1.12 Prata,Georgia,serif;text-wrap:balance}'
    '.zi::before{content:"«"}.zi::after{content:"»"}'
    '.sa{margin-top:52px;max-width:720px;font:400 38px/1.45 Hanken,sans-serif;text-wrap:balance;opacity:.88}'
    '.fu{position:absolute;bottom:150px;left:150px;right:150px;font:500 22px/1.3 Hanken,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--gold)}'
    '.w .fu{color:#7A5C24}'
    '.li{width:110px;height:2px;background:var(--gold);margin:56px auto 0}'
    # SESSION: die Wellen der Plakate in Plakatrot, Schrift in Ultramarin auf einem Schild in Creme
    '.s .sch{position:relative;padding:70px 80px 74px;background:var(--creme);border-radius:22px;box-shadow:0 0 0 1.5px rgba(26,0,170,.55),0 30px 60px -30px rgba(19,14,13,.5)}'
    '.s .ki2{color:var(--ultra)}.s .ti{font-size:116px}.s .sa{color:var(--ultra);opacity:1;margin-top:40px}'
    '.s .se{font:400 150px/1 Prata,Georgia,serif;letter-spacing:.04em;color:var(--ultra);margin-bottom:26px}'
    # Plakate ganz, nichts beschnitten, auf der Nacht
    '.pl{position:absolute;inset:0;display:grid;place-items:center;background:radial-gradient(120% 90% at 50% 0%,#261E1A 0%,#130E0D 62%)}'
    '.pl img{display:block;width:80%;height:auto;border-radius:6px;box-shadow:0 34px 50px -20px rgba(0,0,0,.7)}'
    '.pl .fu{bottom:70px}'
    # Karussell-Deckblatt und Reel-Titel: Foto randlos, Titel im unteren Drittel auf einem Verlauf
    '.fo{position:absolute;inset:0}.fo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}'
    '.fo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(19,14,13,0) 36%,rgba(19,14,13,.9) 100%)}'
    '.fo .tx{position:absolute;left:104px;right:104px;bottom:128px;z-index:2;color:var(--creme);text-align:left}'
    '.fo .ki{font:500 24px/1.3 Hanken,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:28px}'
    '.fo .ti{font-size:100px;line-height:1.04}'
    '.fo .wi{position:absolute;top:104px;right:104px;z-index:2;font:500 22px/1 Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--creme);padding:16px 22px;border:1.5px solid rgba(216,178,100,.8);border-radius:14px;background:rgba(19,14,13,.45)}'
)


def _marke(ton):
    return f'<img class="wm" src="marke-{"rot" if ton in ("n", "w") else "creme"}.svg" alt="">'


def tafel(titel, satz='', fuss='', ton='n', kicker=''):
    """Schrift-Beitrag auf Nacht (n) oder Creme (w), oben die rote Wortmarke."""
    return (f'<div class="{ton}">{_marke(ton)}' + (f'<p class="ki2">{kicker}</p>' if kicker else '') + f'<p class="ti">{titel}</p>'
            + (f'<p class="sa">{satz}</p>' if satz else '') + (f'<p class="fu">{fuss}</p>' if fuss else '') + '</div>')


def zitat(satz, wer, ton='w'):
    return f'<div class="{ton}">{_marke(ton)}<p class="zi">{satz}</p><p class="fu">{wer}</p></div>'


def session(titel, satz, kicker='Samstag · 21 bis 1 Uhr'):
    """SESSION wie auf den Plakaten der Bar: Wellen in Plakatrot, Schrift in Ultramarin."""
    return f'<div class="s"><div class="sch"><p class="se">SESSION</p><p class="ki2">{kicker}</p><p class="ti">{titel}</p><p class="sa">{satz}</p></div></div>'


def plakat(key, fuss='Aus dem Archiv'):
    return '<div class="pl"><img src="{bild:' + quelle(key) + '}" alt=""><p class="fu">' + fuss + '</p></div>'


def deckblatt(key, kicker, titel, wink):
    return '<div class="fo"><img src="{bild:' + quelle(key) + '}" alt=""><span class="wi">' + wink + '</span><div class="tx"><p class="ki">' + kicker + '</p><p class="ti">' + titel + '</p></div></div>'


F = lambda key, art, fx=.5, fy=.5: dict(art='foto', bild=quelle(key), fx=fx, fy=fy, _art=art)
H = lambda html, art: dict(art='html', html=html, _art=art)

# Die nächsten 60, in der Reihenfolge des Postens (1 = zuerst). Daten nur, wo sie feststehen (Silvester, Valentinstag, Tanz in den Mai);
# SESSION und Geburtstag ohne Datum, die Bar kündigt sie wie bisher auf Instagram an.
JAHR = [
    # ---- November 2026
    (H(tafel('Was magst du?', satz='Die Karte wechselt immer wieder. An der Bar sagst du, was du magst.', fuss='Walk on the Wild Side · Linden'), 'text'),
     'Was magst du? Die Karte im Wild Side wechselt immer wieder, die Drinks dafür entwirft Momo. Und an der Bar sagst du einfach, was du magst. Donnerstag ab 19 Uhr, Freitag und Samstag bis 2.'),
    (F('momo-giesst', 'mensch', .6, .4), 'Momo giesst. Vorher hat er gefragt: lieber sauer, süss, bitter oder rauchig?'),
    (F('decke-raum', 'raum', .5, .3), 'Schau nach oben. Über dem ganzen Raum hängt der Druck eines Kathedralen-Gewölbes, angeleuchtet in Blau, Silber und Gold.'),
    (H(session('Sip &amp; Sound.', 'Drinks und Musik an einem Abend. Ohne Eintritt.'), 'session'),
     'Samstag ist wieder SESSION: Drinks und Musik an einem Abend, von 21 bis 1 Uhr, ohne Eintritt. Wer auflegt, steht auf dem Plakat in der Story.'),
    (F('glas-negroni', 'drink', .5, .5), 'Den Negroni gibt es an jedem Abend. Gin, Wermut, Bitter, auf Eis gerührt. Der Schriftzug über der Vitrine ist kein Zufall.'),
    (H(tafel('Jeder Abend ein Plakat.', satz='Rot-cremefarbene Wellen, das Gesicht des Abends in Schwarzweiss.', fuss='SESSION · seit September 2025', ton='w'), 'text'),
     'Seit September 2025 holt das Wild Side DJs an die Bar, und jeder Abend bekommt sein eigenes Plakat: rot-cremefarbene Wellen, das Gesicht des Abends in Schwarzweiss. In den nächsten Wochen zeigen wir sie euch noch einmal, «Aus dem Archiv».'),
    (F('voll', 'leute', .5, .5), 'Ein voller Abend an den Tischen vor der Bar. Wer zu mehreren kommt, reserviert besser.'),
    (H(zitat('Du sagst mir, was du magst, ich mache dir einen Drink.', 'Momo · an der Theke'), 'text'), 'So läuft es an Momos Theke: erst die Frage, dann das Glas.'),
    (F('schild-ecke', 'bar', .5, .5), 'Haasemannstraße 13, Ecke Rampenstraße. Das Schild an der Ecke leuchtet, zwei Minuten vom Küchengarten.'),
    (H(deckblatt('dg-siphon', 'Wie Momo arbeitet', 'Drei Techniken aus dem Labor', '1 / 4'), 'cover'),
     'Milk Washing, Fat Washing, Enzyme: Wisch dich durch. Momo hat Biotechnologie studiert, bevor er hinter die Bar ging, und man schmeckt es.'),
    (F('wf-klar', 'drink', .5, .55), 'Klar wie Wasser, weich wie Sahne: Milk Washing. Die Milch bindet die Trübstoffe und wird wieder abgefiltert.'),
    (F('an-team', 'mensch', .5, .5), 'Das Team vor der Rückbar, über allen der NEGRONI-Schriftzug.'),
    (F('momo-lacht', 'mensch', .55, .45), 'Momo hinter der Bar. Erst fragt er, dann mixt er, und manchmal lacht er dabei.'),
    # ---- Dezember 2026
    (H(tafel('Drei Jahre Wild Side.', satz='Mit DJs, Mexikanern und einem Drink zur Begrüssung für die ersten Gäste.', fuss='Der Geburtstag der Bar', ton='w', kicker='Im Winter'), 'text'),
     'Die neue Wild Side wird drei. Wir feiern mit DJs, Mexikanern und einem Drink zur Begrüssung für die ersten Gäste. Den Abend kündigen wir hier an.'),
    (F('feste-anstossen', 'leute', .5, .4), 'Anstossen draussen an der Ecke. So soll es zum Geburtstag wieder aussehen.'),
    (H(tafel('91 Punkte.', satz='Falstaff Bar Guide 2027, Kategorie Cocktailbars. Drinks: 47 von 50.', fuss='Danke an alle an der Bar', kicker='Falstaff Bar Guide 2027'), 'text'),
     'Falstaff Bar Guide 2027: 91 Punkte für das Wild Side, in der Kategorie Cocktailbars. Drinks 47 von 50, Style 18 von 20, Service 18 von 20. Danke an euch alle, die mit uns an der Bar stehen.'),
    (F('glas-coupe', 'drink', .5, .5), 'Im Coupe, mit Schaum, dahinter Kerzen. Für alle, die cremig sagen.'),
    (H(tafel('Silvester ab mittags.', satz='Frühschoppen an der Bar, und abends geht es weiter.', fuss='Den Mexikaner gibt es die ganze Nacht', kicker='31 · 12'), 'text'),
     'Silvester sind wir wieder ab mittags da, abends geht es weiter. Den Mexikaner gibt es die ganze Nacht, Wild-Side-Tradition. Reservieren per DM oder unter +49 163 3909578.'),
    (F('theke', 'bar', .5, .5), 'Die Theke mit dem gelben Licht unter der Kante. Hier wird gefragt, gemixt und erzählt.'),
    (F('an-party', 'feier', .5, .4), 'Eure Weihnachtsfeier bei uns: Ab dreissig Gästen gehört euch die ganze Bar, von 19 bis 2 Uhr. Alles dazu per DM.'),
    (H(plakat('p-0906'), 'plakat'), 'Aus dem Archiv: das Plakat zum ersten SESSION-Abend, 6. September 2025, mit Björn vom This Is Social Club.'),
    # ---- Januar 2027
    (F('glas-rot', 'drink', .5, .5), 'Rot, im Stielglas, neben Kerzen. Wer bitter sagt, landet oft hier.'),
    (H(tafel('Danke für 2026.', satz='Für jede Frage an der Theke, jeden Abend unter der Decke und jedes Lied am Samstag.', fuss='Derya · Momo', ton='w'), 'text'),
     'Danke für 2026. Für jede Frage an der Theke, jeden Abend unter der Decke und jedes Lied am Samstag. Wir sehen uns im neuen Jahr an der Bar.'),
    (F('freundinnen', 'leute', .5, .45), 'Zu zweit an der Bar. Mehr braucht ein Donnerstag nicht.'),
    (H(session('Das erste Mal 2027.', 'Wer auflegt, verraten wir in der Story.'), 'session'),
     'Die erste SESSION 2027: Samstag, 21 bis 1 Uhr, ohne Eintritt. Wer auflegt, verraten wir in der Story.'),
    (F('decke-hoch', 'raum', .5, .4), 'Von unten nach oben: die Theke mit dem gelben Licht, darüber das Gewölbe.'),
    (H(deckblatt('an-empore', 'Feiern im Wild Side', 'Eure lange Tafel', '1 / 5'), 'cover'),
     'Zehn bis zwanzig Gäste, vier Stunden auf der Empore, unten läuft die Bar weiter. Wisch dich durch die Formate, vom Dinner bis zur ganzen Bar.'),
    (F('dg-giessen', 'drink', .5, .5), 'Durchs Sieb, ins Coupe. Jeder Drink geht durch Momos Hände.'),
    # ---- Februar 2027
    (H(tafel('Valentinstag.', satz='Mit Rudi von Culinarium: vier Drinks und Teller zum Teilen, nur an diesem Abend.', fuss='Reservieren erwünscht', kicker='14 · 02'), 'text'),
     'Valentinstag kocht Rudi von Culinarium bei uns: eine Karte mit vier Drinks und Tellern zum Teilen, die es nur an diesem Abend gibt. Reservieren erwünscht, per DM oder Telefon.'),
    (F('glas-zwei', 'drink', .5, .5), 'Zwei Gläser, ein Tisch. Für den Abend zu zweit.'),
    (H(plakat('p-2401'), 'plakat'), 'Aus dem Archiv: SESSION mit Loverence, 24. Januar 2026.'),
    (F('rueckbar', 'bar', .5, .5), 'Die Rückbar durchs Fenster. Jede Flasche hat ihren Platz, und Momo weiss, wo.'),
    # ---- März 2027
    (H(tafel('Erst die Frage, dann das Glas.', satz='Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll.', fuss='So läuft es an der Theke', ton='w'), 'text'),
     'Erst die Frage, dann das Glas. Momo fragt nach dem Geschmack, nach dem Glas, nach dem, was drin sein soll. Daraus wird ein Drink.'),
    (F('konzert', 'musik', .5, .5), 'Donnerstags spielt ab und zu jemand live, mitten im Raum. Jazz, Soul, Pop, ohne Eintritt.'),
    (F('pl-tisch', 'drink', .5, .5), 'Drinks am Holztisch, hinten die Polsterbank. Ein Abend fängt meistens so an.'),
    (H(deckblatt('dg-coupes', 'Gastschicht', 'Jemand anderes am Shaker', 'Film'), 'cover'),
     'An manchen Abenden steht neben Momo jemand aus einer anderen Bar, aus Hannover oder Berlin, und bringt eigene Drinks mit. Wer als Nächstes kommt, steht hier.'),
    (F('fenster', 'bar', .5, .5), 'Von der Strasse durchs Fenster: drinnen die Rückbar, oben spiegelt sich die Decke.'),
    (H(session('Samstag legt jemand auf.', 'Momo mixt dazu. Ohne Eintritt.'), 'session'),
     'Samstag legt wieder jemand auf, von 21 bis 1 Uhr. Momo mixt dazu, Eintritt frei. Wer zu mehreren kommt, reserviert besser, die Bar ist klein.'),
    # ---- April 2027
    (F('saengerin', 'musik', .5, .4), 'Eine Stimme mitten im Raum. So klingt ein Donnerstag im Wild Side.'),
    (F('glas-sour', 'drink', .5, .5), 'Ein Sour auf der Theke. Wer sauer sagt, bekommt so etwas.'),
    (H(plakat('p-2103'), 'plakat'), 'Aus dem Archiv: SESSION mit Moury, 21. März 2026.'),
    (F('anstossen', 'leute', .5, .45), 'Prost, Linden. Zwei Gläser über dem Tisch.'),
    (H(tafel('Tanz in den Mai.', satz='Musik, Momo an der Bar, Eintritt frei.', fuss='Wenn es warm ist, stehen die Tische vor der Tür', ton='w', kicker='30 · 04'), 'text'),
     'Tanz in den Mai: Musik, Momo an der Bar, Eintritt frei. Wenn es warm ist, stehen die Tische vor der Tür an der Ecke.'),
    (F('negroni', 'bar', .5, .5), 'Die Glühbirnen-Schrift über der Vitrine. Man sieht sie schon von der Tür aus.'),
    # ---- Mai 2027
    (F('momo-flaschen', 'mensch', .45, .5), 'Momo zwischen seinen Flaschen.'),
    (H(deckblatt('an-loge', 'Die Bar ausser Haus', 'Grösser als die Bar', '1 / 4'), 'cover'),
     'Für grössere Veranstaltungen zieht die Bar um, in externe Locations wie die Loge. Derya und Momo kümmern sich um das ganze Konzept, von der Bar bis zum Ablauf des Abends.'),
    (F('glas-hand', 'drink', .5, .5), 'In der Hand, kurz vor dem ersten Schluck.'),
    (H(tafel('Mit derselben Sorgfalt.', satz='Shrub, Soda, Kräuter, klarer Saft.', fuss='Jeder Drink geht auch ohne', kicker='Ohne Alkohol'), 'text'),
     'Ohne Alkohol, mit derselben Sorgfalt: Shrub, Soda, Kräuter, klarer Saft. Momo baut jeden Drink auch ohne.'),
    (F('tuer-rot', 'bar', .5, .5), 'Durch die Tür auf den roten Boden. Dahinter wartet die Bar.'),
    (H(plakat('p-1605'), 'plakat'), 'Aus dem Archiv: SESSION mit Jojo & Reza, Old School, 16. Mai 2026.'),
    # ---- Sommer 2027
    (F('wf-tablett', 'drink', .5, .5), 'Eine Reihe heller Drinks auf dem Tablett, gleich gehen sie an den Tisch.'),
    (F('decke-bar', 'raum', .5, .45), 'Unter der Decke, vor der Rückbar mit dem NEGRONI-Schriftzug.'),
    (H(tafel('Jeder Drink ein Unikat.', satz='Milk Washing, Fat Washing, Enzyme. Und wer einen Negroni will, bekommt ihn.', fuss='Momos Karte wechselt', ton='w'), 'text'),
     'Jeder Drink ein Unikat. Momo arbeitet mit Milk Washing, Fat Washing und Enzymen. Und wer einen Negroni will, bekommt ihn.'),
    (F('ft-momo-mixt-gast', 'mensch', .45, .5), 'Momo schüttelt, daneben wartet der Gast, für den der Drink ist.'),
    (H(plakat('p-0509'), 'plakat'), 'Aus dem Archiv: SESSION mit Apo, 5. September 2026.'),
    (F('flaschen', 'bar', .5, .5), 'Flaschen in der Rückbar. Gin, Rum, Mezcal, Whisky, du sagst, was hinein soll.'),
    (F('glas-kerze', 'drink', .5, .5), 'Ein Drink auf dem dunklen Tisch, dahinter Kerzen.'),
    (H(tafel('Euer Abend.', satz='Ein Dinner an der langen Tafel, die ganze Bar für eure Gesellschaft, Musik, die zum Abend passt.', fuss='Anfragen per DM oder Telefon'), 'text'),
     'Euer Abend im Wild Side: ein Dinner an der langen Tafel, die ganze Bar für eure Gesellschaft, Musik, die zum Abend passt. Derya und Momo planen ihn mit euch, vom ersten Drink bis zum letzten Lied.'),
    (F('ft-raum-abend', 'leute', .5, .5), 'Der Raum am Abend: vorn an der Theke, hinten an den Tischen.'),
    (H(plakat('p-0310'), 'plakat'), 'Aus dem Archiv: SESSION mit Jojo & Reza, Old-School-Hip-Hop, 3. Oktober 2026.'),
]
assert len(JAHR) == 60, len(JAHR)

# Im Profil steht der zuletzt gepostete Beitrag oben links: die Reihenfolge des Postens umgekehrt, Reihe für Reihe zu drei.
_RASTER = list(reversed(JAHR))
FEED = [_RASTER[i:i + 3] for i in range(0, 60, 3)]


def nachbarn():
    """Gleiche Art nie nebeneinander oder untereinander."""
    art = [[st['_art'] for st, _ in r] for r in FEED]
    return [(r + 1, c + 1, art[r][c]) for r in range(len(art)) for c in range(3)
            if (c < 2 and art[r][c] == art[r][c + 1]) or (r + 1 < len(art) and art[r][c] == art[r + 1][c])]


BESTAND_AUSNAHMEN = ('p-',)   # die SESSION-Plakate der Bar dürfen wieder gepostet werden; alles andere nie doppelt
BESTAND_KANDIDATEN = []

BOGEN = []
for _r, _reihe in enumerate(FEED):
    for _c, (st, text) in enumerate(_reihe):
        st = {k: v for k, v in st.items() if k != '_art'}
        kurz = (os.path.basename(st['bild']).rsplit('-', 1)[0] if st['art'] == 'foto' else re.sub(r'\W+', '', re.sub(r'<[^>]+>', ' ', st['html']))[:14] or 'tafel')
        BOGEN.append(dict(id=f'{_r + 1:02d}{_c + 1}-{kurz}', r=_r, c=_c, texte=[text], **st))
P = feed_bogen.p_liste(BOGEN)
BISHER = 82   # Beiträge auf @walkonthewildside_hannover heute (Profil, 26.10.2026); im Profil der Werkbank stehen die mit Bild unter den 60 neuen
PROFIL['zahlen']['beitraege'] = str(len(P) + BISHER)   # Gesamtzahl nach dem Nachposten
# Instagram-Bestand der Bar für den Abgleich: alle Beiträge mit Bild aus _quelle/ig (eigenes Konto)
IG_BESTAND = ['../../_quelle/ig/2*.jpg']
