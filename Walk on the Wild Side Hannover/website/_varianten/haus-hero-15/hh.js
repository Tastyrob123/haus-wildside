/* Wild Side · Kopf «Das Haus», 15 Fassungen: was am Scrollen hängt (06 Heranzoomen, 10 Hinunter zur Bar, 15 Schwenk). Ein Takt, nur transform, nur solange der Kopf im Blick ist. */
(function () {
  'use strict';
  var s = document.getElementById('auftakt'); if (!s || !s.classList.contains('hh')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  if (ruhig || (v !== 6 && v !== 10 && v !== 15)) return;
  var img = s.querySelector(v === 6 ? '.v06-b img' : v === 10 ? '.v10-b img' : '.v15-b'); if (!img) return;
  var rahmen = v === 10 ? s.querySelector('.v10-r') : null;
  var imBild = true, an = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { imBild = es[0].isIntersecting; if (imBild) los(); }).observe(s);
  function takt() {
    an = false;
    var r = s.getBoundingClientRect(), h = innerHeight;
    if (v === 10) {
      var t = Math.max(0, Math.min(1, -r.top / Math.max(1, r.height - h)));   // 0 = oben, 1 = Ende der Strecke
      img.style.setProperty('--y', (-t * Math.max(0, img.offsetHeight - rahmen.offsetHeight)).toFixed(1) + 'px');
    } else {
      var u = Math.max(0, Math.min(1, -r.top / Math.max(1, r.height)));        // 0 = ganz oben, 1 = Kopf ist weg
      if (v === 6) img.style.setProperty('--z', (1.02 + .16 * Math.min(1, u * 1.8)).toFixed(4));
      else img.style.setProperty('--x', (-23.1 * Math.min(1, u * 1.5)).toFixed(3) + '%');
    }
  }
  function los() { if (!an && imBild) { an = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', los, { passive: true }); addEventListener('resize', los); takt();
})();
