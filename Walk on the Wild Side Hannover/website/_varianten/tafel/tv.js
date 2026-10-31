/* Kapitel «Die lange Tafel»: Film läuft nur, solange man hinsieht; das lange Bild geht zur Seite auf; Bänder stehen, wenn man sie nicht sieht. Nur transform. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig');
  if (!('IntersectionObserver' in window)) return;
  document.querySelectorAll('video[data-film]').forEach(function (v) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); }); }, { threshold: .25 }).observe(v);
  });
  document.querySelectorAll('[data-lauf]').forEach(function (l) {
    l.classList.add('halt');
    new IntersectionObserver(function (es) { es.forEach(function (e) { l.classList.toggle('halt', !e.isIntersecting); }); }).observe(l);
  });
  document.querySelectorAll('[data-lang]').forEach(function (b) {
    var inn = b.firstElementChild, s0 = .18;
    function auf() {
      if (ruhig) { b.style.transform = inn.style.transform = 'none'; return; }
      var t0 = performance.now();
      (function schritt(t) { var x = Math.min(1, (t - t0) / 1500), e = 1 - Math.pow(1 - x, 4), s = s0 + (1 - s0) * e;
        b.style.transform = 'scaleX(' + s + ')'; inn.style.transform = 'scaleX(' + (1 / s) + ')'; if (x < 1) requestAnimationFrame(schritt); })(t0);
    }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { auf(); io.disconnect(); } }); }, { rootMargin: '0px 0px -25% 0px' });
    io.observe(b);
  });
})();
