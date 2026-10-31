/* Wild Side · Programm, Kopf: was am Scrollen hängt (05 Blick nach oben, 06 Ring, 12 Gewölbe dreht). Ein Takt, nur transform. */
(function () {
  'use strict';
  var h = document.getElementById('auftakt'); if (!h) return;
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (ruhig) return;
  var ziel = h.querySelector('.h05 .hb img') || h.querySelector('.hx-ring') || h.querySelector('.h12-dreh');
  if (!h.classList.contains('h05')) ziel = h.querySelector('.hx-ring') || h.querySelector('.h12-dreh');
  else ziel = h.querySelector('.hb img');
  if (!ziel) return;
  var tick = false;
  function lauf() {
    tick = false; var r = h.getBoundingClientRect(); if (r.bottom < 0) return;
    var p = Math.max(0, Math.min(1, -r.top / r.height));
    if (ziel.classList.contains('hx-ring')) ziel.style.setProperty('--r', (p * -160).toFixed(1));
    else ziel.style.setProperty('--p', p.toFixed(4));
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  lauf();
})();
