/* Wild Side · Drinks, «Die einzige Karte», 30 Darstellungen: der eigene Moment jeder Fassung. Nur transform, ein Scroll-Takt.
   [data-m] Auftritt einmal (.da), Ausgangslage im CSS, sichtbar von Anfang an · [data-par] / [data-px] senkrecht / waagrecht versetzt
   [data-zoom] Bild zieht sich zurecht · [data-dreh="a,b"] Drehung von a nach b · [data-quer] Querband · [data-buehne] Bühnenwechsel
   [data-jahr] Jahreszahl wechselt · [data-skala] Leopard wächst, solange [data-pin] steht. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var k = $('#karte'); if (!k) return;
  if (!ruhig) document.documentElement.classList.add('vjs');

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  // Auftritt: einmal, sobald gut im Bild
  var m = $$('[data-m]', k);
  if (ruhig || !('IntersectionObserver' in window)) m.forEach(function (el) { el.classList.add('da'); });
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -16% 0px' });
    m.forEach(function (el) { io.observe(el); });
  }
  if (ruhig) return;

  // Lage zur Bildmitte: -1 (unten) … 1 (oben)
  var lage = function (el) { var r = el.getBoundingClientRect(); return ((r.top + r.height / 2) - H() / 2) / H(); };
  $$('[data-par]', k).forEach(function (el) {
    var f = +el.dataset.par;
    takt.push(function () { el.style.transform = schmal() ? '' : 'translate3d(0,' + (lage(el) * f * H()).toFixed(1) + 'px,0)'; });
  });
  $$('[data-px]', k).forEach(function (el) {
    var f = +el.dataset.px;
    takt.push(function () { el.style.transform = 'translate3d(' + (lage(el) * f * innerWidth).toFixed(1) + 'px,0,0)'; });
  });
  $$('[data-zoom]', k).forEach(function (el) {
    var img = $('img', el);
    takt.push(function () { var r = el.getBoundingClientRect(), t = kl((H() - r.top) / (H() * 0.8)); img.style.transform = 'scale(' + (1.16 - 0.16 * t).toFixed(4) + ')'; });
  });
  $$('[data-dreh]', k).forEach(function (el) {
    var w = el.dataset.dreh.split(',').map(Number);
    takt.push(function () { var r = el.getBoundingClientRect(), t = kl((H() * 0.95 - r.top) / (H() * 0.6)); el.style.transform = 'rotate(' + (w[0] + (w[1] - w[0]) * t).toFixed(2) + 'deg)'; });
  });
  // Steht ein Bereich (sticky), Fortschritt 0 … 1
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  $$('[data-skala]', k).forEach(function (el) {
    var p = el.closest('[data-pin]');
    takt.push(function () { el.style.transform = schmal() ? '' : 'scale(' + (1 + 0.1 * pin(p)).toFixed(4) + ')'; });
  });
  $$('[data-quer]', k).forEach(function (q) {
    var zug = $('.qb-zug', q);
    function mass() { if (schmal()) { q.style.height = ''; zug.style.transform = ''; return; } q.style.height = (zug.scrollWidth - innerWidth + H()) + 'px'; }
    mass(); addEventListener('resize', mass); addEventListener('load', mass);
    takt.push(function () { if (!schmal()) zug.style.transform = 'translate3d(' + (-pin(q) * (zug.scrollWidth - innerWidth)).toFixed(1) + 'px,0,0)'; });
  });
  $$('[data-buehne]', k).forEach(function (b) {
    var a = $('.bw-a', b), c = $('.bw-b', b);
    takt.push(function () {
      if (schmal()) { a.style.transform = c.style.transform = ''; return; }
      // erst geht Weihnachten ganz hinaus, dann kommt der Valentinstag herein: die beiden Feste stehen nie nebeneinander
      var t = kl((pin(b) - 0.15) / 0.7);
      a.style.transform = 'translate3d(' + (-100 * kl(t * 2)).toFixed(2) + '%,0,0)';
      c.style.transform = 'translate3d(' + (100 - 100 * kl(t * 2 - 1)).toFixed(2) + '%,0,0)';
    });
  });
  $$('[data-jahr]', k).forEach(function (j) {
    var teil = $$('.jb-teil', k)[1];
    takt.push(function () { j.classList.toggle('b', teil.getBoundingClientRect().top < H() * 0.6); });
  });
  lauf();
})();
