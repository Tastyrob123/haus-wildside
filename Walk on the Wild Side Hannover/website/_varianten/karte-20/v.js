/* Wild Side · Drinks, «Die einzige Karte», 20 Darstellungen: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  // Auftritte einzelner Gruppen (.vauf): einmal, sobald sie gut im Bild sind
  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -14% 0px' }) : null;
  $$('.vauf').forEach(function (el) { io ? io.observe(el) : el.classList.add('da'); });

  var k = $('#karte'), n = k ? +k.dataset.k : 0;

  // 04 · Drink für Drink, während der Abschnitt steht
  if (n === 4) {
    var p = $('[data-pin]', k), d = $$('.e-d', k), s = $$('.e-striche i', k), j0 = 0;
    takt.push(function () {
      if (schmal()) return;
      var j = Math.min(d.length - 1, Math.floor(pin(p) * d.length * 0.999));
      if (j === j0) return;
      d.forEach(function (x, i) { x.classList.toggle('an', i === j); x.classList.toggle('weg', i < j); });
      s.forEach(function (x, i) { x.classList.toggle('an', i <= j); });
      j0 = j;
    });
  }

  // 05 · Die Karte wendet sich, während sie durchs Bild zieht
  if (n === 5) {
    var kt = $('.d-karte', k);
    takt.push(function () {
      var r = kt.getBoundingClientRect(), t = ruhig ? 1 : kl((H() * 0.78 - r.top) / (H() * 0.5));
      kt.style.transform = 'rotateY(' + (t * 180).toFixed(1) + 'deg)';
    });
  }

  // 10 · Der Abschnitt färbt sich rosa
  if (n === 10) {
    var g = $('[data-rosa]', k);
    takt.push(function () {
      var r = k.getBoundingClientRect(), t = ruhig ? 1 : kl((H() * 0.85 - r.top) / (H() * 0.45));
      g.style.opacity = t.toFixed(3);
      k.classList.toggle('rosa', t > 0.5);
    });
  }

  lauf();
})();
