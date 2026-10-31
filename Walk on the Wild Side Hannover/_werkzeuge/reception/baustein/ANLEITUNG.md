---
tags: [projekt, website]
status: aktiv
---

# Baustein: Formulare der Website → Eingang des Gästebuchs · Walk on the Wild Side Hannover

Gebaut am 31.10.2026 im Nachtbau (Revier `_werkzeuge/reception/`), Kopie des Bausteins aus dem Culinarium, umgestellt auf die beiden Formulare der Bar. Auf der Website ist **nichts** eingebaut; das macht der Website-Chat (Revier `website/`), sobald der Oberchef es freigibt.

## Was er tut

- Die Website hat zwei Formulare für das Team, beide heute nur als Vorführung (`form[data-vorfuehrung]`, `wild.js` zeigt den Dank, nichts geht weg):
  - `besuch.html` «Ein Platz für euch.» (`form.rh-form`: Abend, Uhrzeit, Plätze, Name, Telefon oder E-Mail, Platz an der Theke) → Art «Reservieren», Abteilung «Reservieren».
  - `tafel.html` «Euer Abend» (Format, Datum, wie viele, Anlass, Musik dazu, Name, E-Mail oder Telefon, Was habt ihr vor?) → Art «Privates Dinner» (Format Privates Dinner) oder «Feier» (lange Tafel, ganze Bar, grosses Event).
- Mit dem Baustein geht jede Anfrage in den Eingang des Gästebuchs (Art, Abteilung, Angaben als Zeilen, Name, Kontakt, Seite). Erst wenn das Gästebuch sie angenommen hat, zeigt die Website ihren Dank wie bisher; der kleine Satz unter dem Knopf heisst dann «Deine Anfrage liegt beim Team.».
- Fehlt Name oder Kontakt, oder kommt die Anfrage nicht an: Meldung unter dem Knopf mit den Telefonnummern der Bar und Instagram, die Eingaben bleiben. Nie `mailto:`, nie ein Mailprogramm (die Bar hat keine belegte Mail-Adresse).
- `wild.js` der Website bleibt unverändert: der Baustein fängt das Abschicken im Fang-Durchlauf am Dokument ab und gibt es nach der Annahme an die Website weiter.

## Einbauen (Website-Chat, über `bau.py`)

1. `_werkzeuge/reception/baustein/anfrage.js` nach `website/assets/anfrage.js` kopieren.
2. In `bau.py` auf `besuch.html` und `tafel.html` **nach** `wild.js` einhängen: `<script src="assets/anfrage.js?v={VERSION}" defer></script>`.
3. Ziel der Anfragen: auf dem Server des Gästebuchs (:9084) gilt der Standard `/_werkzeuge/reception/api/formular`. Läuft die Website auf einem anderen Server, braucht es `data-api` mit voller Adresse **und** eine Weiterleitung, weil das Gästebuch nur Aufrufe von der eigenen Seite annimmt (Herkunft 403).
4. Datenschutz: `datenschutz.html` muss dann sagen, wo die Anfrage liegt (beim Team der Bar, zwölf Monate, Löschung auf Wunsch). Vom Haus zu prüfen.

## Geprüft

Auf dem Server :9084 (der die Website ausliefert) mit dem Baustein in die Seite gesetzt, nicht in die Website geschrieben: Reservieren auf `besuch.html` und eine Feier auf `tafel.html` liegen danach im Eingang; ohne Name erscheint die Meldung, nichts wird abgelegt.
