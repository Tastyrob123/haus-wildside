"""Walk on the Wild Side · Bilder: aus _quelle/ in WebP-Stufen und ein kleines Vorschaubild (LQ) für den Hintergrund.
Jedes Bild hat einen Schlüssel; Quelle, Ausschnitt und Beschreibung stehen in BILDER. Zwischenablage: assets/bild/."""
import base64, io, json, os
from PIL import Image, ImageOps, ImageFilter

HIER = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(HIER, '..', '_quelle')
ZIEL = os.path.join(HIER, 'assets', 'bild')
STUFEN = (480, 960, 1600, 2400)

# Schlüssel: (Quelle in _quelle/, Alt-Text). Alles echte Fotos der Bar (Google-Eintrag, Instagram, Facebook der Bar).
BILDER = {
    'decke-raum':   ('google-maps/google-52.jpg', 'Der Raum unter der Decke, links die Rückbar, hinten die Stufen nach oben'),
    'decke-flach':  ('google-maps/google-54.jpg', 'Die Decke über der Bar, darunter Rückbar und Wandlampen'),
    'decke-bar':    ('google-maps/google-05.jpg', 'Blick unter der Decke auf die Rückbar mit dem NEGRONI-Schriftzug'),
    'decke-hoch':   ('google-maps/google-42.jpg', 'Die Decke, darunter die Theke mit gelbem Licht'),
    'fenster':      ('google-maps/google-46.jpg', 'Von der Strasse durchs Fenster: die Rückbar, oben spiegelt sich die Decke'),
    'schild':       ('google-maps/google-25.jpg', 'Das beleuchtete Schild an der Hausecke: Walk on the Wild Side'),
    'schild-ecke':  ('google-maps/google-09.jpg', 'Die Ecke Haasemannstrasse am Abend, Gäste vor der Tür'),
    'momo-giesst':  ('google-maps/google-31.jpg', 'Momo giesst einen Drink an der Bar'),
    'momo-lacht':   ('google-maps/google-12.jpg', 'Momo hinter der Bar, oben der NEGRONI-Schriftzug'),
    'schaum':       ('google-maps/google-50.jpg', 'Schaum aus dem Siphon auf einen Sour'),
    'rueckbar':     ('google-maps/google-37.jpg', 'Die Rückbar durchs Fenster, am Tresen wird gemixt'),
    'rueckbar-breit': ('google-maps/google-40.jpg', 'Die Rückbar mit Flaschen und der beleuchteten Vitrine'),
    'negroni':      ('google-maps/google-11.jpg', 'Der NEGRONI-Schriftzug aus Glühbirnen über der Vitrine mit Gläsern'),
    'voll':         ('google-maps/google-01.jpg', 'Ein voller Abend an den Tischen vor der Bar'),
    'theke':        ('google-maps/google-06.jpg', 'Die Theke mit dem gelben Licht unter der Kante'),
    'glas-kerze':   ('google-maps/google-47.jpg', 'Ein Drink auf dem dunklen Tisch, dahinter Kerzen'),
    'glas-rot':     ('google-maps/google-41.jpg', 'Ein roter Drink im Stielglas neben Kerzen'),
    'glas-sour':    ('google-maps/google-44.jpg', 'Ein Sour auf der Theke'),
    'glas-hand':    ('google-maps/google-48.jpg', 'Ein Gast hält einen hellen Drink'),
    'glas-trinkt':  ('google-maps/google-36.jpg', 'Ein Gast trinkt aus einem Stielglas'),
    'glas-negroni': ('google-maps/google-26.jpg', 'Ein Negroni-Glas auf dem Tisch'),
    'glas-zwei':    ('google-maps/google-33.jpg', 'Zwei Drinks auf dem Tisch'),
    'glas-coupe':   ('google-maps/google-04.jpg', 'Ein Drink mit Schaum im Coupe-Glas, dahinter Kerzen'),
    'anstossen':    ('google-maps/google-23.jpg', 'Zwei Gäste stossen über dem Tisch an'),
    'freundinnen':  ('google-maps/google-34.jpg', 'Zwei Gäste an der Bar'),
    'saengerin':    ('google-maps/google-32.jpg', 'Eine Sängerin am Mikrofon in der Bar'),
    'saengerin-sw': ('google-maps/google-39.jpg', 'Eine Sängerin am Mikrofon, schwarzweiss'),
    'tuer-rot':     ('google-maps/google-38.jpg', 'Durch die Tür auf den roten Boden'),
    'flaschen':     ('google-maps/google-43.jpg', 'Flaschen in der Rückbar'),
    'derya':        ('presse/bilder/2024-01-11_np_derya-ivkin-continental-sour.jpg', 'Derya Ivkin an der Bar mit einem Continental Sour (Foto: Ilona Hottmann, Neue Presse)'),
    'terrasse':     ('facebook/2021-06-11_fb_3029501057278702.jpg', 'Gäste auf der Terrasse vor der Bar'),
    'paloma':       ('ig/2025-06-16_walkonthewildside_hannover_DK-GT7TITWD-1.jpg', 'Tequila und Palomas für die Paloma-Nacht'),
    'karte-love':   ('ig/2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-2.jpg', 'Die Karte «Drunk in Love» zum Valentinstag 2026'),
    'karte-dishes': ('ig/2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-3.jpg', 'Die Teller zum Valentinstag 2026, «Dishes in Love»'),
    'valentin':     ('ig/2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-1.jpg', 'Wild Side x Rudi in Love, Valentinstag 2026'),
    'p-0906': ('ig/2025-08-31_walkonthewildside_hannover_DOCMXG-iC59-1.jpg', 'Plakat SESSION mit Björn, 06.09.2025'),
    'p-2211': ('ig/2025-11-17_walkonthewildside_hannover_DRK_iVDiChc-1.jpg', 'Plakat SESSION mit Moury, 22.11.2025'),
    'p-2401': ('ig/2026-01-14_walkonthewildside_hannover_DTf-jwUCObe-1.jpg', 'Plakat SESSION mit Loverence, 24.01.2026'),
    'p-2103': ('ig/2026-03-13_walkonthewildside_hannover_DV1fl7MCO3q-1.jpg', 'Plakat SESSION mit Moury, 21.03.2026'),
    'p-1605': ('ig/2026-05-11_walkonthewildside_hannover_DYNDzMgIR7M-1.jpg', 'Plakat SESSION mit Jojo und Reza, 16.05.2026'),
    'p-0509': ('ig/2026-09-02_walkonthewildside_hannover_DcxmPV3oZbA-1.jpg', 'Plakat SESSION, 05.09.2026'),
    'p-0310': ('ig/2026-09-29_walkonthewildside_hannover_Dd3Vx4lolo3-1.jpg', 'Plakat SESSION mit Jojo und Reza, 03.10.2026'),
    'p-1710': ('ig/2026-10-13_walkonthewildside_hannover_DecaAh8oxYw-1.jpg', 'Plakat SESSION mit den Ghazouani Brothers, 17.10.2026'),
    'konzert':      ('facebook/2024-03-04_fb_816535553821520.jpg', 'Konzert in der Bar: Gitarren und Kontrabass unter der Decke'),
    'konzert-love': ('facebook/2024-06-07_fb_876524861155922.jpg', 'Ein Duo spielt in der Bar, dahinter Glühbirnen-Buchstaben'),
    'decke-2017':   ('facebook/2017-10-24_fb_2044517982443686.jpg', 'Das Kirchengewölbe, das zur Eröffnung 2017 gezeigt wurde'),
    'tafel-glaeser': ('ig/2025-01-15_walkonthewildside_hannover_DE1rV7YML5A-3.jpg', 'Momo seiht Drinks für eine ganze Tafel ab'),
    'fw-tafel': ('aus-culinarium/fenster/tafel-gedeckt-16x10.jpg', 'Die lange Tafel am Fenster, gedeckt mit Brot, Gläsern und Menükarten'),   # Fenster, Wahl Robert 29.10.2026
    # Fenster Feiern vor «So geht es» (Robert 30.10.2026): 16:10-Ausschnitte aus _varianten/fenster-tafel-15/quelle
    'ft-raum-abend': ('../website/_varianten/fenster-tafel-15/quelle/raum-abend.jpg', 'Der Raum am Abend, Gäste an der Theke und hinten an den Tischen'),
    'ft-theke-gaeste': ('../website/_varianten/fenster-tafel-15/quelle/theke-gaeste.jpg', 'Gäste an der Theke, hinten wird gemixt'),
    'ft-runde-stoesst-an': ('../website/_varianten/fenster-tafel-15/quelle/runde-stoesst-an.jpg', 'Eine Runde stösst mit kleinen Gläsern an'),
    'ft-momo-mixt-gast': ('../website/_varianten/fenster-tafel-15/quelle/momo-mixt-gast.jpg', 'Momo schüttelt einen Drink, daneben ein Gast'),
    # Drinks-Seite, «Das Gespräch» und «Wie Momo arbeitet» als ein Weg (Robert 29.10.2026: Fassung 01). Kundenfotos der Culinarium-Abende im Wild Side.
    'dg-shaker': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4568.jpg', 'Momo schüttelt einen Drink, daneben ein Gast'),
    'dg-coupes': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4829.jpg', 'Coupes mit Goldrand in einer Reihe'),
    'dg-flaschen': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/3956.jpg', 'Flaschen auf der Rückbar'),
    'dg-abseihen': ('../../Culinarium Hannover/_quelle/vom-kunden/4313.jpg', 'Ein Drink wird durch ein Sieb in eine Reihe Gläser abgeseiht'),
    'dg-behaelter': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/3937.jpg', 'Glasbehälter mit Zapfhahn auf der Rückbar'),
    'dg-giessen': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/63740.jpg', 'Ein Drink wird durch ein Sieb in ein Coupe gegossen'),
    # Drinks-Seite, Faden «Frage und Antwort» (Wahl Robert 30.10.2026: Fassung 02 aus _varianten/drinks-faden)
    'dg-schaumglas': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4893.jpg', 'Ein Drink mit Schaum in der Hand'),
    'wf-sour': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4558.jpg', 'Ein Drink mit Schaum, dahinter eine Flasche'),
    'wf-pink': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4108.jpg', 'Ein heller Drink mit Schaum bei Kerzenlicht'),
    'wf-zwei': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4843.jpg', 'Zwei Drinks nebeneinander auf dem Tisch'),
    'wf-erdbeer': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4858.jpg', 'Ein Longdrink mit Eis und Erdbeere'),
    'wf-nick': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/5369.jpg', 'Ein klarer Drink in einem Stielglas'),
    'wf-highball': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4921.jpg', 'Ein heller Longdrink im hohen Glas'),
    'wf-tablett': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/63972.jpg', 'Eine Reihe heller Drinks auf dem Tablett'),
    'wf-coupe-tisch': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/63741.jpg', 'Ein Drink im Coupe auf dem Holztisch'),
    # Einstieg und weitere Bilder (Robert 30.10.2026: «ein drittes Bild», «deutlich ästhetischeren Bildern … so zwei dazu»)
    'wf-fe-tequila': ('ig/2025-06-16_walkonthewildside_hannover_DK-GT7TITWD-1.jpg', 'Tequila und Grapefruit-Limonade auf der Theke'),   # Fenster Drinks, Wahl Robert 30.10.2026: Nummer 12
    'wf-raum': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/3925.jpg', 'Momo hinter der Bar, über ihm der Schriftzug NEGRONI'),
    'dg-siphon': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/63963.jpg', 'Schaum aus dem Siphon auf einen Drink'),
    'wf-klar': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/5289.jpg', 'Ein klarer Drink mit Rosmarin, daneben ein kleines Schälchen'),
    'dg-feige': ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4876.jpg', 'Ein Drink mit einer Feigenscheibe im Glas'),
    'tafel-teller': ('ig/2025-01-15_walkonthewildside_hannover_DE1rV7YML5A-4.jpg', 'Ein Teller vom privaten Dinner, daneben Zitronen und Blumen'),
    'tafel-drink':  ('ig/2025-01-15_walkonthewildside_hannover_DE1rV7YML5A-5.jpg', 'Ein Drink zum Menü'),
    'culinarium-teller': ('google-maps/google-15.jpg', 'Ein Teller an der langen Tafel'),
    'dirty-chicken': ('aus-culinarium/dirty-chicken/2026-06-03_dirtychicken.hannover_DZId0KMoAtq-1.jpg', 'Ein Dirty-Chicken-Sandwich'),
    # Fuss (Fassung 3, Robert 29.10.2026): Fotos der Nachbarn aus dem Culinarium-Projekt (Rudis Drive, Dirty-Chicken-Fotos vom 27.10.2026)
    'nb-cu-bete':   ('../../Culinarium Hannover/_quelle/vom-kunden/drive/4890.jpg', 'Rote Bete mit Schaum, dahinter der Drink zum Gang'),
    'nb-dc-burger': ('../../Culinarium Hannover/_quelle/dirty-chicken/vom-kunden-2026-10-27/84673.jpg', 'Ein Chicken-Sandwich im Papier'),
    'silvester':    ('ig/2024-12-18_walkonthewildside_hannover_DDuvG1Rs7kq-1.jpg', 'Ein Glas Sekt über der vollen Bar unter der Decke'),
    # Bildsatz 3 für «Im selben Haus» (Robert 29.10.2026): Rudis eigene Fotos aus seinem Drive (über Culinarium/_quelle/vom-kunden)
    'culinarium-tafel': ('aus-culinarium/vom-kunden/3901.jpg', 'Gäste an der langen Tafel, gedeckt mit Kerzen und Karten'),
    'dirty-burger':     ('aus-culinarium/vom-kunden/bearbeitet/84673-warm.jpg', 'Ein Dirty-Chicken-Sandwich mit Pommes auf dem Tresen'),
    'feste-anstossen':  ('aus-culinarium/vom-kunden/4574.jpg', 'Gäste stossen am Tisch an'),
    'gast-musa':    ('ig/2024-02-26_walkonthewildside_hannover_C30ngEIrNQM-1.jpg', 'Musa und Momo an der Bar'),
    'gast-havn':    ('ig/2024-03-08_walkonthewildside_hannover_C4QsQhqM2s1-1.jpg', 'Gastschicht aus dem Havn an der Bar'),
    'gast-nils':    ('ig/2024-04-10_walkonthewildside_hannover_C5ljExNs6kE-1.jpg', 'Nils Lutterbach vom Lovis in Berlin'),
    'gast-cold':    ('ig/2024-05-16_walkonthewildside_hannover_C7Bco_FsO1O-1.jpg', 'Gastbartender von Cold Drinks and More'),
    'gast-enlil':   ('ig/2024-10-14_walkonthewildside_hannover_DBHXxmYM0vY-1.jpg', 'Enlil Arevalo mit einem Drink'),
    'alt-theke':    ('web-archiv/bilder/103_506957808_theke-hochformat_1200x1600.jpg', 'Die Theke unter der Decke, Foto der ersten Website der Bar'),
    'alt-raum':     ('web-archiv/bilder/103_506957810_bar-raum-hochformat_1200x1600.jpg', 'Der Raum mit Theke und Stufen, Foto der ersten Website der Bar'),
    'alt-rueckbar': ('web-archiv/bilder/103_506957807_backbar-regale_1200x900.jpg', 'Die Rückbar mit Regalen und Vitrine, Foto der ersten Website der Bar'),
    'alt-decke':    ('web-archiv/bilder/103_506957809_raum-decke-lampen_1200x900.jpg', 'Die Decke über dem Raum mit den Wandlampen, Foto der ersten Website der Bar'),
    'fb-2020-bar':  ('facebook/2020-06-17_fb_2743375292557948.jpg', 'Zwei Gäste an der Bar im rosa Licht, Juni 2020'),
    'fb-2023-negroni': ('facebook/2023-11-12_fb_748224287319314.jpg', 'Die Rückbar mit dem NEGRONI-Schriftzug, November 2023'),
    'momo-flaschen': ('google-maps/google-08.jpg', 'Momo hinter den Flaschen an der Bar'),
    'fe-theke':     ('google-maps/google-28.jpg', 'Gäste an der Theke, dahinter wird gemixt'),
    'fe-highball':  ('google-maps/google-29.jpg', 'Ein roter Highball auf dem Tisch'),
    'fe-zwei':      ('google-maps/google-45.jpg', 'Zwei Drinks auf dem Tisch, dahinter die Rückbar'),
    'fe-coupe':     ('google-maps/google-55.jpg', 'Ein Gast hält eine Coupe mit hellem Drink'),
    'fe-serviette': ('google-maps/google-56.jpg', 'Ein Drink im Stielglas auf der Serviette'),
    'fe-minze':     ('google-maps/google-10.jpg', 'Ein Drink mit Minze auf dem Tisch'),
    'fe-old':       ('google-maps/google-19.jpg', 'Ein Drink mit Orangenzeste in der Hand'),
    'pf-raum':      ('portale/stadtwohnungenlinden_wild.jpeg', 'Der leere Raum am frühen Abend: Theke mit Licht, Stufen, Tische an der Wand'),
    'pf-schild':    ('facebook/2025-06-16_fb_1150755357066203.jpg', 'Die beiden Schilder an der Hausecke, davor bunte Papierfahnen'),
    'pf-momo-rudi': ('valentin/momo-rudi-2026.jpg', 'Momo und Rudi von Culinarium am Valentinsabend 2026'),
    'konzert-scharf': ('ki/konzert-4k.png', 'Konzert in der Bar: Gitarren und Kontrabass unter der Decke'),   # Facebook 04.03.2024, per KI auf 4K nachgeschärft (Robert 30.10.2026)
    'uw-tische':    ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-10.jpg', 'Gäste an der Biertischgarnitur, Christi Limmerfahrt 2025'),
    'uw-tanz':      ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-18.jpg', 'Tanzen auf der Strasse, Christi Limmerfahrt 2025'),
    'uw-singen':    ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-5.jpg', 'Eine Sängerin unter den Sonnenschirmen, Christi Limmerfahrt 2025'),
    'uw-sonne':     ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-7.jpg', 'Gäste in der Abendsonne, Christi Limmerfahrt 2025'),
    'uw-lachen':    ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-6.jpg', 'Ein Gast lacht in der Menge, Christi Limmerfahrt 2025'),
    'uw-bank':      ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-13.jpg', 'Auf der Bank am Küchengarten, Christi Limmerfahrt 2025'),
    'uw-kiez':      ('ig-dritte/2026-04-28_event.klub_DXqr_efDUuB-10.jpg', 'Volle Strasse zwischen den Ständen, Christi Limmerfahrt am Küchengarten'),
    'uw-stuehle':   ('ig-dritte/2026-04-28_event.klub_DXqr_efDUuB-5.jpg', 'Liegestühle und Sonnenschirme am Küchengarten'),
    'uw-buehne':    ('ig-dritte/2026-04-28_event.klub_DXqr_efDUuB-4.jpg', 'Eine Sängerin auf der Bühne am Küchengarten'),
    'uw-glas':      ('ig-dritte/2026-04-28_event.klub_DXqr_efDUuB-9.jpg', 'Ein roter Drink im Becher, mit Minze'),
    'uw-fahnen':    ('ig-dritte/2026-04-28_event.klub_DXqr_efDUuB-6.jpg', 'Bunte Fahnen über den Biertischen am Küchengarten'),
    'uw-buden':     ('ig-dritte/2026-04-28_event.klub_DXqr_efDUuB-8.jpg', 'Stände und Gäste am Küchengarten'),
    'uw-pl-limmer': ('ig-dritte/2026-04-28_event.klub_DXqr_efDUuB-2.jpg', 'Plakat Christi Limmerfahrt, 14. und 15. Mai, am Küchengarten'),
    'uw-pl-okt':    ('ig-dritte/2026-10-22_event.klub_Dey3ATejQj2-2.jpg', 'Plakat Oktoberfest am Stephansplatz, 31.10. bis 01.11.'),
    'uw-pl-limmer25':('ig-dritte/2025-05-22_trustory.linden_DJ8lGS2s3WI-1.jpg', 'Plakat Christi Limmerfahrt, 29. und 30. Mai, am Küchengarten'),
    'uw-fahnen25':  ('ig-dritte/2025-05-22_trustory.linden_DJ8lGS2s3WI-10.jpg', 'Fahnen zwischen den Bäumen am Küchengarten'),
    'fe-probe':     ('google-maps/google-17.jpg', 'Drei Gläser zum Probieren auf dem Tisch'),
    'fe-negroni':   ('google-maps/google-35.jpg', 'Ein Drink in der Hand unter dem NEGRONI-Schriftzug'),
    'fw-derya': ('presse/bilder/2024-01-11_np_derya-ivkin-continental-sour.jpg', 'Derya Ivkin an der Bar mit einem Continental Sour (Foto: Ilona Hottmann, Neue Presse)'),
    'fw-highballs': ('google-maps/google-24.jpg', 'Zwei Highballs auf dem Tisch, dahinter die Theke'),
    'fw-sour': ('google-maps/google-44.jpg', 'Ein Sour an der Theke'),
    'fw-a57': ('facebook/2024-05-17_fb_862746769200398.jpg', 'Am Tresen wird eingeschenkt'),
    'fw-a45': ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-1.jpg', 'Hinter der Bar wird gegossen'),
    'fw-h19': ('google-maps/google-18.jpg', 'Drinks werden über den Tresen gereicht'),
    'fw-h33': ('google-maps/google-51.jpg', 'Ein Glas neben der Kerze'),
    'fw-h30': ('neu-2026-10/2024-07-24_voronov_irina_C9z2rj1MRb2-4.jpg', 'Ein Tisch im Kerzenlicht'),
    'fw-a55': ('ig/2023-12-07_walkonthewildside_hannover_C0j1thbsh_y-1.jpg', 'Die Karte des Abends neben der Kerze'),
    'fw-h11': ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-8.jpg', 'Zwei Gläser auf der Theke'),
    'fw-h41': ('ig-dritte/2024-12-20_xwithjess_DDz7J1ps4m--1.jpg', 'Ein roter Highball an der Bar'),
    'fw-h1': ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-6.jpg', 'Zwei Drinks mit Orange auf dem Tisch'),
    'fw-a31': ('google-maps/google-22.jpg', 'Flaschen in der Rückbar'),
    'fw-h16': ('google-maps/google-49.jpg', 'Das Flaschenregal'),
    'fw-h37': ('ig-dritte/2024-12-20_xwithjess_DDz7J1ps4m--2.jpg', 'Ein roter Drink neben der Flasche'),
    'fw-h18': ('google-maps/google-20.jpg', 'Gäste am Tisch'),
    'fw-a14': ('neu-2026-10/2023-11-28_lizzas.diaryy_C0MQYiKtBvW-2.jpg', 'Ein Gast mit Drink'),
    'fw-h42': ('neu-2026-10/2024-03-24_luisaverfuerth_C46WyDtsKbl-1.jpg', 'Ein Gast mit einem Sour'),
    'fw-a12': ('ig/2023-11-09_walkonthewildside_hannover_CzbxDQMMKQ3-1.jpg', 'Der Raum am 9. November 2023'),
    'fw-h7': ('google-maps/google-14.jpg', 'In der Bar'),
    'fw-a9': ('neu-2026-10/2024-07-24_voronov_irina_C9z2rj1MRb2-8.jpg', 'Die gedeckte Tafel'),
    'fw-a4': ('ig/2024-02-26_walkonthewildside_hannover_C30ngEIrNQM-1.jpg', 'Zwei an der Bar'),
    'fw-h46': ('neu-2026-10/2024-03-24_luisaverfuerth_C46WyDtsKbl-5.jpg', 'Zwei Gäste mit Drinks'),
    'fw-a3': ('ig-dritte/2024-08-06_xwithjess_C-VADi2sNFU-2.jpg', 'Zwei Drinks am Fenster'),
    'fw-a47': ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-4.jpg', 'Zwei Gläser mit Gin'),
    'fw-h21': ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-7.jpg', 'Zwei Gin Tonic an der Bar'),
    'fw-a36': ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-5.jpg', 'Ein Drink im Abendlicht'),
    'fw-h31': ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-8.jpg', 'Ein Sommerabend vor der Bar'),
    'fw-a58': ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-15.jpg', 'Tanzen auf der Strasse'),
    'fw-a49': ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-11.jpg', 'Sonne vor der Bar'),
    'fw-a46': ('ig-dritte/2025-06-01_twopointsview_DKW3aKaNbjt-3.jpg', 'Zwei Bartender hinter dem Tresen'),
    'fw-a17': ('neu-2026-10/2024-07-20_luisaverfuerth_C9pIhtHs57s-1.jpg', 'Ein Gast an der Bar'),
    'fw-h3': ('neu-2026-10/2024-07-20_luisaverfuerth_C9pIhtHs57s-4.jpg', 'Gäste im Raum'),
    'fw-a8': ('neu-2026-10/2024-04-30_luisaverfuerth_C6YS0yFs-kk-9.jpg', 'Ein Gast auf der Bank'),
    'fw-a28': ('neu-2026-10/2023-11-28_lizzas.diaryy_C0MQYiKtBvW-1.jpg', 'Ein Gast trinkt'),
    'fw-a7': ('neu-2026-10/2024-04-30_luisaverfuerth_C6YS0yFs-kk-1.jpg', 'Gäste am Abend'),
    'fw-a15': ('neu-2026-10/2024-07-24_voronov_irina_C9z2rj1MRb2-2.jpg', 'Ein Drink wird gereicht'),
    'fw-a52': ('neu-2026-10/2024-07-24_voronov_irina_C9z2rj1MRb2-7.jpg', 'Am Tisch'),
    'fw-a53': ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-3.jpg', 'Ein Glas auf dem Tisch'),
    'fw-a1': ('neu-2026-10/2024-04-30_luisaverfuerth_C6YS0yFs-kk-10.jpg', 'Im Raum'),
    'tf-oben':    ('neu-2026-10/2024-07-24_voronov_irina_C9z2rj1MRb2-6.jpg', 'Die gedeckte Tafel von oben'),
    'tf-dessert': ('neu-2026-10/2024-07-24_voronov_irina_C9z2rj1MRb2-1.jpg', 'Ein Dessert wird an die Tafel gestellt'),
    'tf-l3':      ('neu-2026-10/2024-07-20_luisaverfuerth_C9pIhtHs57s-3.jpg', 'Ein Gang an der Tafel'),
    'tf-l5':      ('neu-2026-10/2024-07-20_luisaverfuerth_C9pIhtHs57s-5.jpg', 'Ein Teller an der Tafel, dahinter die Runde'),
    'tf-l8':      ('neu-2026-10/2024-07-20_luisaverfuerth_C9pIhtHs57s-8.jpg', 'Ein Teller mit Sauce an der Tafel'),
    'tf-h1':      ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-1.jpg', 'Ein Gang mit Kräutern'),
    'tf-h2':      ('neu-2026-10/2023-10-15_hannoverfoodie_Cyah0yBsSyQ-2.jpg', 'Ein Teller mit Erbsen und Kresse'),
    # Feiern-Seite (Robert 30.10.2026): Fotos aus der Angebotsmappe der Bar «Wild Side Angebote.pdf» (_quelle/angebote-pdf/)
    'an-empore':  ('angebote-pdf/img-039.jpg', 'Die lange Tafel auf der Empore am Fenster'),
    'an-empore-tafel': ('neu-2026-10/2024-07-24_voronov_irina_C9z2rj1MRb2-8.jpg', 'Die gedeckte lange Tafel oben auf der Empore unter dem Kronleuchter'),
    'an-party':   ('angebote-pdf/img-045.jpg', 'Gäste feiern mit erhobenen Gläsern'),
    'an-party-sw': ('angebote-pdf/img-020.jpg', 'Ein Abend in der Bar, schwarzweiss'),
    'an-dj':      ('angebote-pdf/img-048.jpg', 'Das DJ-Pult im Licht'),
    'an-dinner':  ('angebote-pdf/img-042.jpg', 'Die gedeckte Tafel mit Brot, Zitronen und Menükarte'),
    'an-loge':    ('angebote-pdf/img-051.jpg', 'Ein Saal mit langen, weiss gedeckten Tafeln'),
    'ev-theke':   ('angebote-pdf/img-001.jpg', 'Die Theke mit den Barhockern im gelben Licht'),   # Abzüge Grosse Events, Fassung 10 (Robert 30.10.2026)
    'an-campari': ('angebote-pdf/img-008.jpg', 'Leuchtschrift NO NEGRONI WITHOUT CAMPARI'),
    'an-sours':   ('angebote-pdf/img-011.jpg', 'Eine Reihe Sours mit Schaum'),
    'an-glaeser': ('angebote-pdf/img-057.jpg', 'Gläser werden für eine Runde gefüllt'),
    'an-sour':    ('angebote-pdf/img-038.jpg', 'Ein Sour mit Schaum neben der Kerze'),
    'an-team':    ('angebote-pdf/img-060.jpg', 'Das Team vor der Rückbar mit dem NEGRONI-Schriftzug'),
    'an-negroni': ('angebote-pdf/img-023.jpg', 'Ein Negroni ganz nah'),
}


def _lq(im):
    k = im.copy()
    k.thumbnail((28, 28))
    k = k.filter(ImageFilter.GaussianBlur(0.6))
    b = io.BytesIO()
    k.save(b, 'JPEG', quality=55)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


def mache(schluessel):
    """Gibt {'w','h','stufen':[(breite,datei)],'lq','alt'} zurück und legt fehlende Stufen an."""
    os.makedirs(ZIEL, exist_ok=True)
    quelle, alt = BILDER[schluessel]
    pfad = os.path.join(Q, quelle)
    merk = os.path.join(ZIEL, schluessel + '.json')
    mtime = os.path.getmtime(pfad)
    if os.path.exists(merk):
        d = json.load(open(merk))
        if d.get('mtime') == mtime and all(os.path.exists(os.path.join(ZIEL, f)) for _, f in d['stufen']):
            d['alt'] = alt
            return d
    im = ImageOps.exif_transpose(Image.open(pfad)).convert('RGB')
    w, h = im.size
    stufen = []
    for s in STUFEN:
        b = min(s, w)
        if stufen and b <= stufen[-1][0]:
            break
        k = im.resize((b, round(h * b / w)), Image.LANCZOS)
        name = '%s-%d.webp' % (schluessel, b)
        k.save(os.path.join(ZIEL, name), 'WEBP', quality=80, method=5)
        stufen.append((b, name))
    d = {'w': w, 'h': h, 'stufen': stufen, 'lq': _lq(im), 'mtime': mtime, 'quelle': quelle}
    json.dump(d, open(merk, 'w'))
    d['alt'] = alt
    return d


if __name__ == '__main__':
    for k in BILDER:
        d = mache(k)
        print(k, d['w'], d['h'], len(d['stufen']))
