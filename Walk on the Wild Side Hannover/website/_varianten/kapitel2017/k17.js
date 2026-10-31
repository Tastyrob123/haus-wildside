/* Kapitel «Seit 2017»: Bildwechsel im Rahmen (06), Zeitstrahl am Scroll (10). Nur transform. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  var IO = 'IntersectionObserver' in window;
  document.querySelectorAll('.s06-rahmen').forEach(function (r) {
    var sec = r.closest('section');
    if (!IO) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) r.dataset.an = e.target.dataset.n; });
    }, { rootMargin: '-45% 0px -45% 0px' });
    sec.querySelectorAll('.s06-txt').forEach(function (t) { io.observe(t); });
  });
  var strahl = document.querySelectorAll('[data-strahl]'), tick = false;
  function rechnen() {
    tick = false;
    strahl.forEach(function (s) {
      var r = s.getBoundingClientRect(), ih = innerHeight; if (r.bottom < -ih || r.top > ih * 2) return;
      var p = ruhig ? 1 : Math.max(0, Math.min(1, (ih * 0.62 - r.top) / r.height));
      s.querySelector('.s10-linie').style.transform = 'scaleY(' + p.toFixed(4) + ')';
    });
  }
  if (strahl.length) { addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }, { passive: true }); rechnen(); }
})();
