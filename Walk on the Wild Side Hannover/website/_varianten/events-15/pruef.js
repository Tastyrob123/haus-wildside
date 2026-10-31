/* Prüfung (nur für die Kontrolle, nicht in den Seiten): Überdeckungen, Bildgrössen, Breite. */
window.evPruef = function () {
  var g = document.getElementById('events'), out = [];
  document.documentElement.classList.add('ruhig');
  var R = function (e) { return e.getBoundingClientRect(); };
  var texte = [].slice.call(g.querySelectorAll('.kz,.titel,.text,.ev-klein,.knopf'));
  var bilder = [].slice.call(g.querySelectorAll('.fb'));
  texte.forEach(function (t) { var a = R(t); bilder.forEach(function (b) { var c = R(b);
    var x = Math.min(a.right, c.right) - Math.max(a.left, c.left), y = Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top);
    if (x > 4 && y > 4 && !b.closest('.e10-tisch')) out.push('Text auf Bild: ' + t.className.slice(0, 20)); }); });
  bilder.forEach(function (b) { var i = b.querySelector('img'), c = R(b); var nat = +i.getAttribute('width');
    var f = Math.max(c.width / nat, c.height / +i.getAttribute('height'));
    if (f > 0.85) out.push('Bild zu gross ' + i.currentSrc.split('/').pop() + ' ' + Math.round(c.width) + 'x' + Math.round(c.height) + ' f=' + f.toFixed(2)); });
  if (document.documentElement.scrollWidth > innerWidth + 1) out.push('quer ' + document.documentElement.scrollWidth);
  out.push('Höhe ' + Math.round(g.offsetHeight) + ' / ' + innerHeight);
  return out;
};
