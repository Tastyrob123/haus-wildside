/* Wild Side · Das Haus, «Was andere sagen», Fassungen 01–15: Auftritte und die Bewegung einzelner Fassungen. Nur transform, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var H = function () { return innerHeight; };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };
  var mitte = function (el) { var r = el.getBoundingClientRect(); return (r.top + r.height / 2 - H() / 2) / H(); };

  var g = document.getElementById('stimmen'), n = g ? +g.getAttribute('data-x') || 0 : 0;
  if (!n) return;

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -15% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var F = {
    // Laufband: zieht mit dem Scrollen
    7: function () {
      var l = $('[data-lauf]', g);
      takt.push(function () { if (!sicht(l)) return; var x = ruhig ? 0 : (mitte(l) * (schmal() ? 260 : 520)) - 600; l.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)'; });
    },
    // Wechselzahl: die Quelle in der Mitte bestimmt die Zahl links
    12: function () {
      var w = $('[data-wechsel]', g), e = $$('.w12-e', g), a = -1;
      takt.push(function () {
        if (!sicht(w)) return; var best = 0, d = 1e9;
        e.forEach(function (x, i) { var m = Math.abs(mitte(x)); if (m < d) { d = m; best = i; } });
        if (best !== a) { a = best; w.setAttribute('data-a', a); e.forEach(function (x, i) { x.classList.toggle('an', i === a); }); }
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
