/* Reservieren · 15 Fassungen: Hocker zählen (02), die nächsten drei offenen Abende ausrechnen (12). */
(function () {
  'use strict';
  /* 02 Sechs Hocker: angetippter Hocker und alle davor leuchten, die Zahl darüber zählt mit */
  document.querySelectorAll('.rv02-form').forEach(function (f) {
    var hs = [].slice.call(f.querySelectorAll('.rv02-h')), zahl = f.querySelector('.rv02-zahl b');
    function stelle() {
      var n = 0; hs.forEach(function (h, j) { if (h.querySelector('input').checked) n = j + 1; });
      hs.forEach(function (h, j) { h.classList.toggle('an', j < n); });
      if (zahl) zahl.textContent = n;
      var w = f.querySelector('.rv02-zahl'); if (w) w.lastChild.textContent = n === 1 ? ' Platz' : ' Plätze';
    }
    hs.forEach(function (h) { h.querySelector('input').addEventListener('change', stelle); });
    stelle();
  });

  /* 12 Die nächsten Abende: Do 19 bis 1 Uhr, Fr und Sa 19 bis 2 Uhr (HAUS.zeiten) */
  var BIS = { 4: '19 bis 1 Uhr', 5: '19 bis 2 Uhr', 6: '19 bis 2 Uhr' };
  var TAG = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  var MON = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  document.querySelectorAll('[data-abende]').forEach(function (box) {
    var d = new Date(); d.setHours(12, 0, 0, 0);
    if (new Date().getHours() < 5) d.setDate(d.getDate() - 1); /* nach Mitternacht zählt der laufende Abend */
    var liste = [];
    while (liste.length < 3) { if (BIS[d.getDay()]) liste.push(new Date(d)); d.setDate(d.getDate() + 1); }
    box.querySelectorAll('.rv12-a').forEach(function (a, j) {
      var t = liste[j], iso = t.getFullYear() + '-' + String(t.getMonth() + 1).padStart(2, '0') + '-' + String(t.getDate()).padStart(2, '0');
      a.querySelector('input').value = iso;
      a.querySelector('.rv12-tag').textContent = TAG[t.getDay()];
      a.querySelector('.rv12-dat').textContent = t.getDate() + '. ' + MON[t.getMonth()];
      a.querySelector('.rv12-bis').textContent = BIS[t.getDay()];
    });
  });
})();
