/* pruefung-haus.js · Prüfseite im Rahmen von Walk on the Wild Side (31.10.2026; Vorlage Culinarium, aus dem Vorbild Schäfli): Name des Werkzeugs aus der einen Stelle, «Zum Werkzeug» führt in dieses Werkzeug, nicht in den Stamm. */
(function () {
  var z = document.getElementById('wsp-zurueck'); if (z) z.href = '/_werkzeuge/bureau/';
  var n = window.WO_HAUS && WO_HAUS.namen && WO_HAUS.namen.website;
  if (n) { document.querySelectorAll('[data-werkzeug]').forEach(function (e) { e.textContent = n; }); document.title = 'Prüfung · ' + n + ' · ' + WO_HAUS.name; }
})();
/* DJ-Abende (Wild Side 31.10.2026, Vorlage: Termine des Culinarium): eigener Teil der Prüfung (Quelle website/bau.py › LINEUP, Stellen der Seiten, Speicher,
   Sicherung) und die Lexikon-Einträge der Stichworte aus termine.py und termine-ansicht.js. Das Lexikon des Stamms bleibt unverändert; diese Einträge
   stehen darunter mit eigener Kennung lex-<stichwort> und öffnen sich, wenn «Was tun?» dorthin führt. */
(function () {
  var LEX = [
    { id: 'termine-quelle', titel: 'Die DJ-Abende der Website sind nicht lesbar', sehen: 'Die Ansicht «DJ-Abende» startet nicht, oder hier steht «DJ-Abende der Website» rot.',
      grund: 'Die DJ-Abende stehen auf der Website als Liste «LINEUP» in website/bau.py. Die Website wurde umgebaut und die Liste fehlt oder hat eine neue Form.',
      tun: 'Nichts ist verloren: Entwurf und veröffentlichte DJ-Abende liegen im Speicher des Werkzeugs. Die Liste in website/bau.py wieder so bauen lassen (Datum, Name, Zeile, Plakat), dann diese Seite neu laden.' },
    { id: 'termine-stelle', titel: 'Eine Seite hat keinen Platz mehr für die DJ-Abende', sehen: 'Hier steht «Stellen auf den Seiten» rot, oder Plakatwand, Kontaktbogen oder Flyer zeigen nach dem Veröffentlichen die alten Abende.',
      grund: 'Die Seiten «Programm» oder die Startseite wurden umgebaut; die Stelle, an der die Plakate hängen, sieht anders aus.', tun: 'Die Website zeigt weiter ihre gebauten Abende. Die Seiten neu bauen lassen, dann diese Seite neu laden.' },
    { id: 'termine-speicher', titel: 'Der Speicher der DJ-Abende ist beschädigt', sehen: 'Meldung «SPEICHER · Die Datei der DJ-Abende und ihre Sicherung sind beide unlesbar».',
      grund: 'Die Datei _werkzeuge/bureau/_daten/termine.json und ihre Sicherung termine.json.gut sind beide kaputt (zum Beispiel von Hand geändert).',
      tun: 'Die Website zeigt weiter die DJ-Abende, wie sie gebaut ist. Die Datei aus einer Sicherung des Rechners zurückholen oder beide Dateien entfernen: dann gilt wieder der ursprüngliche Stand.' },
    { id: 'termin-datum', titel: 'Diesen Tag gibt es nicht', sehen: 'Meldung «DATUM · Das Datum fehlt oder gibt es nicht», die Karte zeigt «Diesen Tag gibt es nicht».',
      grund: 'Tag und Monat passen nicht zusammen, zum Beispiel der 31. November.', tun: 'Tag, Monat und Jahr neu wählen, dann speichern.' },
    { id: 'termin-name', titel: 'Der Name fehlt', sehen: 'Meldung «NAME · Wer legt auf?», die Karte zeigt «Wer legt auf?».',
      grund: 'Das Feld «Wer legt auf» ist leer. Ohne Namen kann die Seite den Abend nicht ankündigen.', tun: 'Den Namen eintragen, so wie er auf dem Plakat steht, dann speichern.' },
    { id: 'termin-lang', titel: 'Name oder Zeile sind zu lang', sehen: 'Meldung «ZU LANG · … hat höchstens 60 (80) Zeichen».',
      grund: 'Der Text passt nicht mehr unter das Plakat.', tun: 'Kürzer schreiben: der Name wie auf dem Plakat, die Zeile mit Stil oder Herkunft.' },
    { id: 'termin-zeichen', titel: 'Klammern im Namen', sehen: 'Meldung «ZEICHEN · spitze und geschweifte Klammern stehen nicht auf dem Plakat».',
      grund: 'Im Namen oder in der Zeile steht ein Zeichen wie < > { }.', tun: 'Das Zeichen herausnehmen, dann speichern.' },
    { id: 'termin-plakat', titel: 'Kein Plakat gewählt', sehen: 'Meldung «PLAKAT · Bitte eines der Plakate der Bar wählen».',
      grund: 'Das Plakat gibt es auf der Website nicht (mehr).', tun: 'Unter «Plakat» eines aus der Liste wählen.' },
    { id: 'termin-doppelt', titel: 'Zwei DJ-Abende am selben Tag', sehen: 'Meldung «DOPPELT · An einem Tag steht schon ein DJ-Abend».',
      grund: 'Ein Abend wurde zweimal angelegt oder auf den Tag eines anderen verschoben.', tun: 'Bei einem der beiden den Tag ändern, oder ihn mit «Wieder entfernen» herausnehmen.' },
    { id: 'termin-leer', titel: 'Kein DJ-Abend mehr in der Liste', sehen: 'Meldung «LEER · Mindestens ein DJ-Abend bleibt auf der Seite».',
      grund: 'Plakatwand, Kontaktbogen und Flyer zeigen immer den neuesten Abend; ohne Abend hätten sie nichts zu zeigen.', tun: '«Wie gespeichert» oder «Neuer Abend» füllt die Liste wieder, dann speichern.' },
    { id: 'termin-viele', titel: 'Zu viele DJ-Abende', sehen: 'Meldung «DJ-ABENDE · Höchstens 40 Abende stehen gleichzeitig auf der Website».',
      grund: 'Der Kontaktbogen zeigt jedes Plakat; mehr als 40 machen ihn unlesbar.', tun: 'Alte Abende «Von der Seite nehmen», dann speichern.' },
    { id: 'termin-falsch', titel: 'Ein DJ-Abend ist unvollständig', sehen: 'Meldung «DJ-ABEND · …» mit Kennung oder Liste.',
      grund: 'Die Anfrage kam nicht aus dem Werkzeug oder wurde unterwegs verändert.', tun: 'Die Seite neu laden und die Eingabe wiederholen. Bleibt es, den Wortlaut der Meldung deinem Ansprechpartner schicken.' },
    { id: 'fassung-unbekannt', titel: 'Diese frühere Fassung gibt es nicht mehr', sehen: 'Meldung «FASSUNG · Diese frühere Fassung gibt es nicht».',
      grund: 'Die Liste der früheren Fassungen hält die letzten 60; ältere fallen heraus.', tun: 'Die Seite neu laden und eine Fassung aus der Liste wählen, oder den ursprünglichen Stand.' },
    { id: 'netz', titel: 'Der Server antwortet nicht', sehen: 'Meldung «NETZ · Der Server des Werkzeugs antwortet nicht».',
      grund: 'Die Verbindung ist weg oder der Server des Werkzeugs läuft nicht.', tun: 'Deine Eingaben bleiben stehen. Verbindung prüfen, dann noch einmal «Speichern». Läuft der Server nicht: python3 _werkzeuge/bureau/serve.py 9082 im Projektordner.' }
  ];
  function el(tag, attrs, kinder) { var e = document.createElement(tag); Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); }); (kinder || []).forEach(function (k) { e.append(k); }); return e; }
  var lex = document.querySelector('[aria-labelledby="wsp-t4"]');
  if (!lex) return;
  var teil = el('section', { class: 'wsp-teil', 'aria-labelledby': 'wsp-t-termine', 'data-cu-pruefung': 'termine' }, [
    el('div', {}, [el('p', { class: 'kap' }, [el('span', {}, ['Viertens'])]), el('h2', { class: 't-zwischen', id: 'wsp-t-termine' }, ['DJ-Abende'])]),
    el('div', { class: 'platte wsp-punkte', id: 'cu-termine-punkte' }, [el('p', { class: 'wsp-wartet' }, ['Wird geprüft …'])])]);
  lex.parentNode.insertBefore(teil, lex);
  var ort = el('div', { class: 'wsp-lexikon', id: 'cu-lexikon' });
  lex.append(el('p', { class: 'kap', style: 'margin-top:28px' }, [el('span', {}, ['DJ-Abende'])]), ort);
  LEX.forEach(function (l) {
    ort.append(el('details', { class: 'platte wsp-lex', id: 'lex-' + l.id }, [el('summary', {}, [l.titel]),
      el('dl', {}, [el('dt', { class: 'angabe' }, ['Sehen']), el('dd', {}, [l.sehen]), el('dt', { class: 'angabe' }, ['Grund']), el('dd', {}, [l.grund]), el('dt', { class: 'angabe' }, ['Tun']), el('dd', {}, [l.tun])])]));
  });
  function oeffne() {
    var e = location.hash.indexOf('#lex-') === 0 && document.getElementById(location.hash.slice(1));
    if (e && ort.contains(e)) { e.open = true; setTimeout(function () { e.scrollIntoView({ block: 'start' }); }, 0); }
  }
  window.addEventListener('hashchange', oeffne); oeffne();
  fetch('/_werkzeuge/bureau/api/termine/pruefung', { cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (d) {
    var p = document.getElementById('cu-termine-punkte'); p.textContent = '';
    (d.punkte || []).forEach(function (x) {
      p.append(el('div', { class: 'wsp-punkt', 'data-gut': x.gut ? 'ja' : 'nein', 'data-punkt': 'termine' }, [
        el('span', { class: 'wsp-punkt__z' }, [x.gut ? '✓' : '–']), el('span', { class: 'wsp-punkt__t' }, [x.titel]),
        el('span', { class: 'wsp-punkt__x' }, [x.text + ' ', !x.gut && x.stichwort ? el('a', { href: '#lex-' + x.stichwort }, ['Was tun?']) : ''])]));
    });
  }).catch(function () { var p = document.getElementById('cu-termine-punkte'); p.textContent = 'Der Server des Werkzeugs antwortet nicht (Stichwort netz).'; });
})();
