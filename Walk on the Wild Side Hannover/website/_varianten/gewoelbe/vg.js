/* Fenster-Fassungen: Auftritt beim Auftauchen, Schwenk und Tiefe am Scroll (ein Takt), Breitwand, Maus, Laufband nur wenn sichtbar. */
(function () {
  'use strict';
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var IO = 'IntersectionObserver' in window;
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };

  function breitwand(el) {
    var band = el.querySelector('[data-breitwand]'); if (!band) return;
    var inn = band.firstElementChild, s0 = 0.36, t0 = performance.now(), dauer = 1500;
    if (ruhig) { band.style.transform = 'none'; inn.style.transform = 'none'; return; }
    (function schritt(t) {
      var x = Math.min(1, (t - t0) / dauer), e = 1 - Math.pow(1 - x, 4), s = s0 + (1 - s0) * e;
      band.style.transform = 'scaleY(' + s + ')'; inn.style.transform = 'scaleY(' + (1 / s) + ')';
      if (x < 1) requestAnimationFrame(schritt);
    })(t0);
  }
  function an(el) { if (el.classList.contains('da')) return; el.classList.add('da'); breitwand(el); }

  $$('[data-auf]').forEach(function (el) {
    if (!IO || ruhig) return an(el);
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { an(el); io.disconnect(); } }); },
      { rootMargin: '0px 0px ' + (el.dataset.rand || '-8%') + ' 0px' });
    io.observe(el);
  });

  /* Schwenk (01) und Tiefe (03): ein Takt für beide */
  var schwenk = $$('[data-schwenk]'), tiefe = $$('[data-tiefe]'), tick = false;
  function rechnen() {
    tick = false; var ih = innerHeight;
    schwenk.forEach(function (s) {
      var r = s.getBoundingClientRect(); if (r.bottom < -ih || r.top > ih * 2) return;
      var p = Math.max(0, Math.min(1, -r.top / (r.height - ih)));
      var bild = s.querySelector('.v01-bild'); bild.style.transform = 'translate3d(0,' + (-p * 0.9 * ih).toFixed(1) + 'px,0)';
      if (r.top < ih * 0.45) s.querySelector('.v01-oben .zl').classList.add('da');
      if (p > 0.6) s.querySelector('.v01-unten .zl').classList.add('da');
    });
    tiefe.forEach(function (t) {
      var r = t.getBoundingClientRect(); if (r.bottom < -100 || r.top > ih + 100) return;
      var y = ((r.top + r.height / 2) - ih / 2) * -0.22;
      t.firstElementChild.style.transform = 'translate3d(0,' + y.toFixed(1) + 'px,0)';
    });
  }
  if (schwenk.length || tiefe.length) {
    if (ruhig) schwenk.forEach(function (s) { $$('.zl', s).forEach(function (z) { z.classList.add('da'); }); });
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }, { passive: true });
    addEventListener('resize', rechnen); rechnen();
  }

  /* Maus (11): leise, höchstens 2,5 % der Fläche */
  $$('[data-maus]').forEach(function (b) {
    if (ruhig || !matchMedia('(hover: hover)').matches) return;
    var sec = b.closest('section'), m = b, wartet = false, x = 0, y = 0;
    sec.addEventListener('mousemove', function (ev) {
      var r = sec.getBoundingClientRect(); x = (ev.clientX - r.left) / r.width - 0.5; y = (ev.clientY - r.top) / r.height - 0.5;
      if (wartet) return; wartet = true;
      requestAnimationFrame(function () { wartet = false; m.style.transform = 'translate3d(' + (-x * r.width * 0.05).toFixed(1) + 'px,' + (-y * r.height * 0.05).toFixed(1) + 'px,0)'; });
    });
    sec.addEventListener('mouseleave', function () { m.style.transform = 'none'; });
  });

  /* Laufband (12): steht, wenn man es nicht sieht */
  $$('[data-lauf]').forEach(function (l) {
    if (!IO) return; l.classList.add('halt');
    new IntersectionObserver(function (es) { es.forEach(function (e) { l.classList.toggle('halt', !e.isIntersecting); }); }).observe(l);
  });
})();
