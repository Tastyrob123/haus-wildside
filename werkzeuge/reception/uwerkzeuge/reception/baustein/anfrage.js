/* Anschluss der Formulare der Website an das Gästebuch · Walk on the Wild Side Hannover (31.10.2026, Master Werkzeug-Bau E12/E24/E33, Muster: Culinarium Hannover).
   Die Website hat zwei Formulare, die etwas an das Team geben sollen, beide bisher nur als Vorführung (form[data-vorfuehrung], wild.js zeigt den Dank, nichts geht weg):
     besuch.html  «Ein Platz für euch.» (form.rh-form: Abend, Uhrzeit, Plätze, Name, Telefon oder E-Mail, Platz an der Theke)   → Art «reservieren»
     tafel.html   «Euer Abend» (Format, Datum, wie viele, Anlass, Musik dazu, Name, E-Mail oder Telefon, Was habt ihr vor?)      → Art «dinner» (Privates Dinner) oder «feier»
   Mit diesem Baustein geht jede Anfrage in den Eingang des Gästebuchs; erst wenn das Gästebuch sie angenommen hat, zeigt die Website ihren Dank wie bisher
   («Danke. Die Bar bestätigt dir den Abend.» bzw. «Danke. Derya und Momo melden sich …»). Fehlt Name oder Kontakt oder geht etwas schief, steht unter dem Knopf
   eine Meldung mit den Telefonnummern der Bar und Instagram, die Eingaben bleiben. Nie mailto, nie ein Mailprogramm (die Bar hat keine belegte Mail-Adresse).
   Die Skripte der Website (wild.js) bleiben unverändert. Der Baustein fängt das Abschicken im Fang-Durchlauf am Dokument ab, bevor die Website den Dank zeigt,
   schickt an das Gästebuch und gibt das Abschicken danach an die Website weiter.
   Einbinden (Website-Chat über bau.py, nicht von Hand): <script src="assets/anfrage.js?v={V}" defer></script> nach wild.js.
   Ziel: /_werkzeuge/reception/api/formular (anders mit <script … data-api="http://127.0.0.1:9284/_werkzeuge/reception/api/formular"> oder window.WS_ANFRAGE_API). */
(function () {
  'use strict';
  var D = document, skript = D.currentScript;
  var API = window.WS_ANFRAGE_API || (skript && skript.getAttribute('data-api')) || '/_werkzeuge/reception/api/formular';
  var WEGE = 'Telefon +49 163 3909578 oder +49 174 9916296, oder eine Nachricht an @walkonthewildside_hannover auf Instagram';
  var wert = function (f, n) { var e = f.querySelector('[name="' + n + '"]'); return e ? String(e.value || '').trim() : ''; };
  var seiteName = function () { var t = (D.title || '').split(/ · | \| | — /)[0].trim(); return /^Walk on the Wild Side/.test(t) ? 'Startseite' : t; };
  var datumLang = function (iso) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || ''); if (!m) return iso || ''; var d = new Date(+m[1], +m[2] - 1, +m[3]);
    return d.toLocaleDateString('de-DE', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).replace(/^(\w+) /, '$1, '); };

  /* Was jedes Formular mitschickt: dieselben Angaben, die der Gast im Formular sieht, in Zeilen für das Team */
  function reservieren(f) {
    var tag = datumLang(wert(f, 'datum')), zeit = wert(f, 'zeit'), n = wert(f, 'gaeste');
    return { art: 'reservieren', formular: 'reservieren', anker: '#reservieren', platz: wert(f, 'platz') || 'Theke',
      anliegen: 'Platz reservieren: ' + [tag, zeit, n ? n + (n === '1' ? ' Platz' : ' Plätze') : ''].filter(Boolean).join(', '),
      datum: tag, uhrzeit: zeit, personen: n, name: wert(f, 'name'), kontakt: wert(f, 'kontakt'),
      zeilen: ['Abend: ' + (tag || '-'), 'Uhrzeit: ' + (zeit || '-'), 'Plätze: ' + (n || '-')] };
  }
  function feiern(f) {
    var format = wert(f, 'format'), tag = datumLang(wert(f, 'datum')), n = wert(f, 'gaeste'), anlass = wert(f, 'anlass'), musik = wert(f, 'musik'), text = wert(f, 'text');
    return { art: format === 'Privates Dinner' ? 'dinner' : 'feier', formular: 'feiern', anker: '#anfragen',
      anliegen: [format, anlass, n ? n + ' Gäste' : ''].filter(Boolean).join(', '), datum: tag, uhrzeit: '', personen: n, name: wert(f, 'name'), kontakt: wert(f, 'kontakt'),
      zeilen: ['Format: ' + (format || '-'), 'Datum: ' + (tag || '-'), 'Wie viele: ' + (n || '-'), 'Anlass: ' + (anlass || '-'), 'Musik dazu: ' + (musik || '-')].concat(text ? ['Was habt ihr vor?: ' + text] : []) };
  }
  var welches = function (f) { return f.classList.contains('rh-form') ? reservieren : f.querySelector('[name=format]') ? feiern : null; };

  /* Feld, das Menschen nicht sehen: nur Maschinen füllen es aus (das Gästebuch nimmt solche Anfragen still an und legt nichts ab) */
  function falle(f) {
    if (f.querySelector('[name=website]')) return;
    var i = D.createElement('input'); i.type = 'text'; i.name = 'website'; i.tabIndex = -1; i.autocomplete = 'off'; i.setAttribute('aria-hidden', 'true');
    i.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;opacity:0';
    f.appendChild(i);
  }
  function meldung(f, text) {
    var p = f.querySelector('.hinweis');
    f.classList.remove('fertig');
    if (p) p.textContent = text;
  }
  function senden(f, d, knopf, fertig) {
    if (f.dataset.sendet) return;
    f.dataset.sendet = '1'; if (knopf) knopf.disabled = true;
    var koerper = { art: d.art, formular: d.formular, name: d.name, kontakt: d.kontakt, datum: d.datum || '', uhrzeit: d.uhrzeit || '', personen: d.personen || '', platz: d.platz || '',
      allergene: [], anliegen: d.anliegen, nachricht: d.zeilen.join('\n'), seite: location.pathname + location.search + d.anker,
      seite_name: seiteName(), sprache: (D.documentElement.lang || 'de').slice(0, 2), website: wert(f, 'website') };
    fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(koerper) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (x) {
        if (!x.ok) throw new Error(String((x.j && x.j.fehler) || '').replace(/^[A-ZÄÖÜ-]+ · /, '') || 'Deine Anfrage kam nicht an.');
        fertig();
      })
      .catch(function (e) { meldung(f, (e && e.message && !/fetch|network|load/i.test(e.message) ? e.message : 'Deine Anfrage kam nicht an.') + ' Versuch es gleich noch einmal, oder melde dich direkt: ' + WEGE + '.'); })
      .then(function () { delete f.dataset.sendet; if (knopf) knopf.disabled = false; });
  }

  D.addEventListener('submit', function (e) {
    var f = e.target, bau = f && f.matches && f.matches('form[data-vorfuehrung]') && welches(f);
    if (!bau) return;
    if (f.dataset.durch) { delete f.dataset.durch; return; }   // angenommen: jetzt zeigt die Website ihren Dank wie bisher
    e.preventDefault(); e.stopImmediatePropagation();
    var d = bau(f);
    if (!d.name || !d.kontakt) { meldung(f, 'Bitte Name und ' + (d.formular === 'feiern' ? 'E-Mail oder Telefon' : 'Telefon oder E-Mail') + ' angeben, damit die Bar antworten kann.'); return; }
    senden(f, d, f.querySelector('[type=submit]'), function () {
      f.dataset.durch = '1'; f.dispatchEvent(new Event('submit', { cancelable: true }));
      var s = f.querySelector('.hinweis'); if (s) s.textContent = 'Deine Anfrage liegt beim Team.';   // statt «Vorführung: In diesem Entwurf wird nichts verschickt.»
    });
  }, true);
  function bereit() { [].forEach.call(D.querySelectorAll('form[data-vorfuehrung]'), function (f) { if (welches(f)) falle(f); }); }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', bereit); else bereit();
})();
