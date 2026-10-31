/* Die Besucherliste (Le Registre) · Walk on the Wild Side Hannover: Zählung auf der Website (Tasty Studios, Nachtbau 31.10.2026). Quelle dieser Datei; auf der
   Website liegt sie als assets/messung.js, auf jeder Seite vor </body> als <script src="assets/messung.js?v=…" defer></script>, nach wild.js.
   Den Einbau in bau.py (Fuss) macht der Bau der Website (Revier website/, erst auf Roberts Wort); hier nur die Quelle. Vorbild: messung.js der Besucherliste
   des Culinarium Hannover (nur kopiert), Ereignisse von Walk on the Wild Side.

   Je Seite geht eine Zeile an /api/registre (lokal der Server der Besucherliste, online die Funktion api/registre.py, gleiche Adresse):
       r1 <seitenaufruf> <datei> <sprache> <geraet> <sekunden> <ereignisse|-> <herkunft|->
   einmal beim Öffnen (0 Sekunden), bei jedem gezählten Klick und beim Verlassen (Sekunden, in denen die Seite sichtbar war).
   Ohne Cookies und ohne Kennung im Gerät: «seitenaufruf» ist eine Zufallsfolge, die nur in dieser Variablen lebt und mit der Seite endet.
   Dass die Seiten eines Besuchs zusammenfinden, Land und Ort bestimmt der Server aus der Verbindung (registre.py); die Adresse speichert er nicht.
   «herkunft» ist nur der Name der Website, von der der Gast kam (zum Beispiel l.instagram.com), nie die ganze Adresse.
   «sprache» ist die Sprache des Browsers (die Website gibt es nur deutsch), sonst «xx».
   Nicht gezählt: automatische Browser (Prüfläufe), Seiten im Rahmen, die Werkzeuge und die Werkbank, Wahl- und Vorschauseiten (*-wahl*.html, konzept.html,
   _varianten/) und Geräte mit der Marke «wildside-nicht-zaehlen» im localStorage (das Einzige, was je im Gerät steht).
   Die Formulare der Website (wild.js, form[data-vorfuehrung]) bleiben unberührt: gezählt wird nur, dass etwas begonnen oder abgeschickt wurde,
   nie ein Inhalt (kein Name, keine Telefonnummer).

   Ereignisse (Schlüssel wie in allen Häusern, Bedeutung bei Walk on the Wild Side):
     fenster  Reservieren begonnen: erste Wahl oder Eingabe im Formular «Reservieren» auf «Besuch» (form.rh-form)
     buchung  Tisch reserviert: erst wenn das Formular sein «Danke» zeigt (Klasse «fertig», wild.js)
     booking  Feier angefragt: erst wenn das Formular auf «Feiern» (form.formular) sein «Danke» zeigt
     tisch    Feier-Anfrage begonnen: erste Wahl oder Eingabe im Formular auf «Feiern»
     anfrage  Knopf «Reservieren» angeklickt (Verweis auf besuch.html#reservieren in der Leiste oder im Auftakt einer Seite)
     anruf    Telefonnummer der Bar angeklickt (+49 163 3909578 oder +49 174 9916296)
     mail     Instagram der Bar geöffnet (@walkonthewildside_hannover); die Website zeigt keine Mail-Adresse
     chat     weiter zu Culinarium oder Dirty Chicken (im selben Haus: Vitrine der Startseite, Fuss jeder Seite);
              die Website hat keinen Gäste-Chat, der Schlüssel bleibt wie in den anderen Häusern
     route    Karte geöffnet (OpenStreetMap auf «Besuch», Google Maps oder Apple Karten) */
(function () {
  'use strict';
  var n = navigator, d = document, w = window;
  if (w.__registre || !n.sendBeacon || n.webdriver || w.self !== w.top) return;
  try { if (w.localStorage.getItem('wildside-nicht-zaehlen') === '1') return; } catch (e) { /* privat: zählt normal */ }
  var teile = location.pathname.split('/'), datei = teile.pop() || 'index.html';
  if (/^(_werkzeuge|werkzeuge|werkbank|_werkbank|_varianten|maison|marke|reception|registre|imprimerie|_qa|_sicherung|_alt|_zuschnitt)$/.test(teile[1] || '')) return;   /* Werkzeuge und Werkbank zählen nie */
  if (!/^[a-z0-9-]{1,60}\.html$/.test(datei) || /wahl|^konzept|varianten|^vorschau|^404/.test(datei)) return;
  w.__registre = 1;
  var SPRACHEN = ' de en fr it nl es pt zh ja ko ar ';
  var sp = String(n.language || 'de').slice(0, 2).toLowerCase();
  if (SPRACHEN.indexOf(' ' + sp + ' ') < 0) sp = 'xx';
  var breit = function (px) { return !!(w.matchMedia && w.matchMedia('(max-width:' + px + 'px)').matches); };
  var geraet = breit(700) ? 'handy' : breit(1060) ? 'tablet' : 'rechner';
  var her = '-';
  try { var r = d.referrer ? new URL(d.referrer).hostname.toLowerCase() : ''; if (r && r !== location.hostname && /^[a-z0-9.-]{3,60}$/.test(r)) her = r; } catch (e) {}
  var BAR_TEL = /^tel:\+?(491633909578|01633909578|491749916296|01749916296)$/;
  var IG_BAR = /^\/walkonthewildside_hannover\/?$/;
  var pv, war, liste, sichtbar, seit, gesendet;
  function neu() {
    pv = (Math.random().toString(36) + '000000').slice(2, 8);
    war = {}; liste = []; sichtbar = 0; gesendet = '';
    seit = d.visibilityState === 'hidden' ? 0 : Date.now();
    sende();
  }
  function sek() { return Math.min(1800, Math.round((sichtbar + (seit ? Date.now() - seit : 0)) / 1000)); }
  function sende() {
    var zeile = 'r1 ' + pv + ' ' + datei + ' ' + sp + ' ' + geraet + ' ' + sek() + ' ' + (liste.length ? liste.join(',') : '-') + ' ' + her;
    if (zeile === gesendet) return;
    gesendet = zeile;
    try { n.sendBeacon('/api/registre', zeile); } catch (e) {}   /* wartet auf keine Antwort */
  }
  function zaehle(was) {
    if (war[was]) return;
    war[was] = 1; liste.push(was);
    sende();
  }
  function weg() { if (seit) { sichtbar += Date.now() - seit; seit = 0; } sende(); }
  neu();
  d.addEventListener('visibilitychange', function () { if (d.visibilityState === 'hidden') weg(); else if (!seit) seit = Date.now(); });
  w.addEventListener('pagehide', weg);
  w.addEventListener('pageshow', function (e) { if (e.persisted) neu(); });   /* zurück aus dem Seitenspeicher des Browsers: neuer Aufruf */

  /* Gezählt ist erst, was die Website zeigt («Danke»); nachgesehen wird kurz, höchstens 20 Sekunden. Bleibt es aus (Pflichtfeld leer), zählt nichts. */
  function danach(pruef, was) {
    var bis = Date.now() + 20000;
    (function schau() { if (pruef()) { zaehle(was); return; } if (Date.now() < bis) setTimeout(schau, 250); })();
  }

  /* Die zwei Formulare der Bar: Reservieren (Besuch) und Anfrage (Feiern), begonnen mit der ersten Wahl oder Eingabe */
  function formular(fm, begonnen, fertig) {
    if (!fm) return;
    fm.addEventListener('click', function (e) { if (e.target && e.target.closest && e.target.closest('button:not([type=submit]),input,select,textarea,label')) zaehle(begonnen); }, true);
    fm.addEventListener('input', function () { zaehle(begonnen); }, true);
    fm.addEventListener('submit', function () { zaehle(begonnen); danach(function () { return fm.classList.contains('fertig'); }, fertig); }, true);
  }
  formular(d.querySelector('form.rh-form'), 'fenster', 'buchung');
  formular(d.querySelector('form.formular'), 'tisch', 'booking');

  d.addEventListener('click', function (e) {
    var t = e.target; if (!t || !t.closest) return;
    var a = t.closest('a[href]'); if (!a) return;
    var h = (a.getAttribute('href') || '').replace(/\s/g, ''), host = (a.hostname || '').toLowerCase(), pfad = a.pathname || '';
    if (/(^|\/)besuch\.html#reservieren$/.test(h)) zaehle('anfrage');
    else if (/^tel:/i.test(h)) { if (BAR_TEL.test(h)) zaehle('anruf'); }
    else if (/(^|\.)instagram\.com$/.test(host)) { if (IG_BAR.test(pfad)) zaehle('mail'); else if (/culinarium|dirtychicken/i.test(pfad)) zaehle('chat'); }
    else if (/culinarium|dirty-?chicken/i.test(h) || (a.closest('.vi-stueck,.f03-f') && host !== location.hostname)) zaehle('chat');
    else if (/(^|\.)openstreetmap\.org$|(^|\.)maps\.apple\.com$|(^|\.)goo\.gl$/.test(host) || /(^|\.)google\.[a-z.]+$/.test(host) && /^\/maps/.test(pfad)) zaehle('route');
    else if (/^mailto:/i.test(h)) zaehle('mail');
  }, true);
})();
