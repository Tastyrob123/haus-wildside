# Auftrag Nachtbau · Walk on the Wild Side Hannover (1.11.2026)

Du bist Oberchef dieses Hauses. Lies zuerst `CLAUDE.md` (vor allem «Der Deal mit Robert» und «Was fertig heisst»), dann `_Werkzeuge/OBERCHEF-PAKET.md`, `_Werkzeuge/ROBERTS-KRITERIEN.md`, `Walk on the Wild Side Hannover/CHARAKTER.md` und `_kette/`.
Vorbild holen: `git clone --depth 1 https://github.com/Tastyrob123/haus-culinarium-hannover /tmp/culinarium` (öffentlich, ohne Schlüssel). Kundenmaterial: Zweig `quelle` (siehe CLAUDE.md).

**Fertig um 09:00 Uhr Ortszeit Robert (UTC+8, also 01:00 UTC).** Keine Ausrede, keine neue Zeitangabe, keine Begründung; hängt ein Teil, wird der Weg gewechselt, nicht die Zeit.

1. **Werkbank** aus `/tmp/culinarium/Culinarium Hannover/website/_werkbank/` und `_Werkbank-Kit/`: alle Seiten (Start, Karte, KI, Geprüft, Befund, Unterlagen, Drucksachen, Untersetzer/Sticker, Feed, Mails, Material) mit Inhalt dieses Hauses (Website, CHARAKTER.md, `quelle`), ohne Platzhalter.
2. **Die sieben Werkzeuge** aus `/tmp/culinarium/Culinarium Hannover/_werkzeuge/` nach `Walk on the Wild Side Hannover/_werkzeuge/` kopieren und umkleiden: Name, Zeichen, Farben, Schriften aus Markenbuch/Charakter von Wild Side; Hauswerte eintragen (Adresse, Zeiten, Karte, Anlässe, Fotos aus `quelle`); aus der Werkbank verlinkt; Server wie in `cloud/haus.json`. Je Werkzeug ein Unteragent (Agent-Werkzeug, `model: "opus"`, nie Fable), parallel, jeder mit klarem Revier. Nichts neu erfinden.
3. **Drucksachen** der Plakatwerkstatt für das Haus.
4. **Prüfen:** Ziellisten `_Werkzeuge/abnahme-tor/ziele-wildside.json` und `_Werkzeuge/messlauf/ziele-wildside.json` aus den Culinarium-Listen anlegen (gleiche Ports, Namen des Hauses, Stilblatt-Pfad des Hauses). Jedes Werkzeug gleich nach dem Bau mit `[schnell: <werkzeug>]` prüfen (Commit-Nachricht), Funde reparieren, noch einmal prüfen; am Ende `[schnell]` über alles. Fundbilder und je Werkzeug 15 Zustandsbilder mit dem Auge ansehen (Kriterien A). Tafel: Zweig `ergebnis`, `ergebnis/laeufe/<zweig>-schnell/tor/index.html`.
5. Commits auf `main` mit kurzer Nachricht, was fertig ist. Robert sieht nach, ohne zu fragen.

**Letzte Nachricht, genau eine:** «Fertig. <Link Werkbank> <Link Prüftafel>» – oder nur, wenn trotz Wegwechsel etwas fehlt: «Nicht fertig. <Links> – es fehlt: <Liste>». Keine Zwischenmeldungen, keine Begründungen, keine Technik, keine neue Uhrzeit. Deutsch, kurz, Alltagssprache.
Nichts verschicken, nichts veröffentlichen, nichts bezahlen, keine Schlüssel einchecken; die Live-Website des Hauses nicht ändern.
