---
tags: [projekt, feed]
status: aktiv
---

# Feed-Bestand und Gegenprobe · Walk on the Wild Side (Werkbank, Nachtbau 31.10.2026)

Vorlage: `feed-bestand.md` des Culinarium (Fassung 3 «Fortsetzung», 29.10.2026). Bau: `_Werkbank-Kit/feed.py`, `feed_druck.js`, `feed_bestand.py` (unverändert), Daten `_werkbank/feed_daten.py`, danach `_werkbank/feed_leicht.py`.

## Dieses Haus: @walkonthewildside_hannover · die nächsten 60 Beiträge

- **Profil heute** (`_quelle/research_notes/…/programm_zeiten_kooperationen.md`, 26.10.2026): 82 Beiträge, 2.680 Follower, 331 gefolgt, Bio «Drinks | Events | private Veranstaltungen | Tastings … Do 19:00-01:00 | Fr & Sa 19:00-02:00 … Schreib uns eine DM oder ruf an». Neuester Beitrag 13.10.2026 (SESSION mit den Ghazouani Brothers). Profilbild: das echte der Bar (`_quelle/logo/wildside-profilbild-1080.jpg`).
- **Bestandsabgleich:** `feed_bestand.py` gegen alle 53 Bilder der 39 Beiträge mit Bild in `_quelle/ig/`. Ein Foto der Website war schon gepostet und ist raus (`dg-abseihen` = Beitrag DE1rV7YML5A vom 15.01.2025). Die SESSION-Plakate (`p-…`) sind die einzige Ausnahme (`BESTAND_AUSNAHMEN`) und kommen gezielt «Aus dem Archiv» wieder: p-0906, p-2401, p-2103, p-1605, p-0509, p-0310. Bericht: `feed/bestand.json`.
- **Die nächsten 60** in Reihenfolge des Postens (`JAHR` in `feed_daten.py`, im Raster umgekehrt): November 2026 (Was magst du?, Momo, die Decke, SESSION, Negroni, «Jeder Abend ein Plakat», Momos Satz, die Ecke, drei Techniken, Milk Washing, das Team), Dezember (Geburtstag der Bar, Falstaff 91 Punkte, Silvester ab mittags, Weihnachtsfeier in der ganzen Bar), Januar (Danke für 2026, erste SESSION 2027, Feiern auf der Empore), Februar (Valentinstag mit Rudi von Culinarium), Frühjahr (Gastschicht, Konzerte am Donnerstag, Tanz in den Mai, ohne Alkohol, die Bar ausser Haus), Sommer (Jeder Drink ein Unikat, «Euer Abend»). 34 Fotos, 6 Plakate, 13 Schrift-Beiträge, 3 SESSION-Beiträge in Ultramarin und Plakatrot, 4 Karussell-Deckblätter. Keine gleiche Art neben- oder untereinander (`nachbarn()` leer). Termine nur, wo sie feststehen (31.12., 14.02., 30.04.); SESSION und Geburtstag ohne Datum und ohne erfundene Namen.
- **Profil:** oben die 60 neuen (nummeriert, Nummern abschaltbar), Band «Die nächsten 60 · Euer Feed heute», darunter die 39 echten bisherigen Beiträge mit ihrem Text; Schalter «Heute» / «Mit den nächsten 60»; Zahl im Kopf 142 bzw. 82.
- **Kleid:** Tafeln in Prata und Hanken, Nacht und Creme mit Gold-Haarlinie, rote Wortmarke; Schriftnamen und Farbreste des Kits tauscht `feed_leicht.kleid()` (Liste aus `kleid_wild.py`).
- Sicherungen: `*.vor-wildside-2026-10-31`.
