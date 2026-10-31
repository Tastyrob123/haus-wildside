/* Walk on the Wild Side · «Im selben Haus» edel: das Prisma (14) dreht sich zum nächsten Eintrag, Reiter wählen. */
(function () {
  'use strict';
  var s = document.getElementById('imhaus');
  if (!s || !s.classList.contains('e14')) return;
  var ruhig = document.documentElement.classList.contains('ruhig');
  var raum = s.querySelector('.eh-p-raum'), k = s.querySelector('.eh-p-koerper');
  var texte = [].slice.call(s.querySelectorAll('.eh-pt')), reiter = [].slice.call(s.querySelectorAll('.eh-p-reiter button'));
  var jetzt = 0, dreh = 0, gewaehlt = 0;
  function breite() { k.style.setProperty('--b', raum.offsetWidth + 'px'); }
  function zeig(i) {
    var schritt = ((i - jetzt) % 3 + 3) % 3; if (schritt === 2) schritt = -1;
    dreh -= schritt * 120; jetzt = i;
    k.style.setProperty('--a', dreh + 'deg');
    texte.forEach(function (t, j) { t.classList.toggle('an', j === i); });
    reiter.forEach(function (r, j) { r.classList.toggle('an', j === i); });
  }
  breite(); addEventListener('resize', breite);
  reiter.forEach(function (r, i) { r.addEventListener('click', function () { gewaehlt = Date.now(); zeig(i); }); });
  if (!ruhig) setInterval(function () {
    var b = s.getBoundingClientRect();
    if (b.bottom > 0 && b.top < innerHeight && Date.now() - gewaehlt > 9000) zeig((jetzt + 1) % 3);
  }, 4800);
})();
