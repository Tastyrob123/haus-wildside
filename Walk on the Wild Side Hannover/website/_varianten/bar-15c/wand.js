/* Wild Side · Abschnitt «bar», dritte Runde: was mehr als CSS braucht. Nur transform, ein Takt für alles am Scrollen. */
(function () {
  'use strict';
  var s = document.getElementById('bar'); if (!s || !s.classList.contains('b3')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');

  /* 13 · Das Bild bleibt stehen: jedes Schild rechts schwebt hoch, sobald es in den Blick kommt */
  if (v === 13) {
    var st = [].slice.call(s.querySelectorAll('.v13-s'));
    if (ruhig || !('IntersectionObserver' in window)) st.forEach(function (e) { e.classList.add('da'); });
    else { var o = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); o.unobserve(e.target); } }); }, { rootMargin: '0px 0px -12% 0px' }); st.forEach(function (e) { o.observe(e); }); }
  }

  /* 06 · Das Bild läuft mit / 07 · Panorama: in einem Takt am Scrollen, nur solange der Abschnitt im Blick ist */
  if ((v !== 6 && v !== 7) || ruhig) return;
  var el = s.querySelector(v === 6 ? '.v06-b' : '.v07-b'), img = el && el.querySelector('img'); if (!img) return;
  var imBild = true, an = false;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { imBild = es[0].isIntersecting; if (imBild) los(); }).observe(el);
  function takt() {
    an = false;
    var r = el.getBoundingClientRect(), h = innerHeight;
    var t = Math.max(0, Math.min(1, (h - r.top) / (h + r.height)));   // 0 = kommt unten herein, 1 = oben hinaus
    if (v === 6) img.style.setProperty('--p', ((t - .5) * -16).toFixed(2) + '%');
    else img.style.setProperty('--z', (1.16 - .16 * Math.min(1, t * 1.6)).toFixed(4));
  }
  function los() { if (!an && imBild) { an = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', los, { passive: true }); addEventListener('resize', los); takt();
})();
