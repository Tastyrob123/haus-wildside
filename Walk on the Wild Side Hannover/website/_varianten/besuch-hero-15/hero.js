/* Wild Side · Besuch, 15 Fassungen für den Kopf: Band gleitet langsamer (09), Streifen läuft seitwärts (13). Nur transform, ein Takt. */
(function () {
  'use strict';
  var h = document.querySelector('.bh'); if (!h) return;
  var v = +h.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  if (ruhig) return;
  var beimScrollen = function (fn) {
    var tick = false;
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; fn(); }); } }, { passive: true });
    fn();
  };

  /* 09 · das Foto im Band bleibt beim Scrollen zurück */
  if (v === 9) {
    var zug = h.querySelector('.bh09-zug');
    beimScrollen(function () {
      var y = Math.min(scrollY, h.offsetHeight);
      zug.style.transform = 'translate3d(0,' + (y * .22).toFixed(1) + 'px,0)';
    });
  }

  /* 13 · der Streifen läuft beim Scrollen seitwärts, bis das letzte Bild drin ist */
  if (v === 13) {
    var z = h.querySelector('.bh13-zug');
    beimScrollen(function () {
      var max = Math.max(0, z.scrollWidth - innerWidth + 16);
      var x = Math.min(scrollY * .7, max);
      z.style.transform = 'translate3d(' + (-x).toFixed(1) + 'px,0,0)';
    });
  }
})();
