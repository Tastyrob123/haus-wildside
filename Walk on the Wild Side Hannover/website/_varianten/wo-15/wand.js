/* Wild Side · Besuch «Wo», 15 Fassungen: Bewegung am Scrollen (04, 05, 07, 12). Ein Takt, nur solange der Abschnitt im Blick ist, nur transform. */
(function () {
  'use strict';
  var s = document.getElementById('wo'); if (!s || !s.classList.contains('wo15')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion:reduce)').matches;
  if ([4, 5, 7, 12].indexOf(v) < 0) return;
  if (ruhig) { if (v === 12) s.style.setProperty('--s', 1); return; }
  var imBild = true, an = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { imBild = es[0].isIntersecting; if (imBild) los(); }).observe(s);
  function anteil(el) { var r = el.getBoundingClientRect(), h = innerHeight; return Math.max(0, Math.min(1, (h - r.top) / (h + r.height))); }
  function takt() {
    an = false;
    if (v === 4) { var b = s.querySelector('.v04-b img'), t = anteil(b.parentNode); b.style.setProperty('--z', (1.16 - .16 * Math.min(1, t * 1.7)).toFixed(4)); }
    if (v === 5) {
      var l = s.querySelector('.v05-l'), r = s.querySelector('.v05-r'), t5 = anteil(l) - .5;
      l.style.setProperty('--p', (t5 * -40).toFixed(1) + 'px'); r.style.setProperty('--p', (t5 * 40).toFixed(1) + 'px');
    }
    if (v === 7) { var i = s.querySelector('.v07-b img'); i.style.setProperty('--p', ((anteil(i.parentNode) - .5) * -12).toFixed(2) + '%'); }
    if (v === 12) {
      var w = s.querySelector('.v12-weg'), rr = w.getBoundingClientRect(), h = innerHeight;
      s.style.setProperty('--s', Math.max(0, Math.min(1, (h * .75 - rr.top) / rr.height)).toFixed(3));
    }
  }
  function los() { if (!an && imBild) { an = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', los, { passive: true }); addEventListener('resize', los); takt();
})();
