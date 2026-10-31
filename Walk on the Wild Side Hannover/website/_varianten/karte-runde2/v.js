/* Wild Side · Drinks, «Die einzige Karte», Runde 2: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() && r.top < 2 * H(); };
  var lage = function (el) { var r = el.getBoundingClientRect(); return kl((H() - r.top) / (H() + r.height)); };

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -14% 0px' }) : null;
  $$('.vauf').forEach(function (el) { io ? io.observe(el) : el.classList.add('da'); });

  var g = document.getElementById('karte'); if (!g) return;
  var n = +((g.className.match(/\bv(\d\d)\b/) || [])[1] || 0);
  if (ruhig) return;

  var F = {
    11: function () {
      var b = $('.pa-b', g), f = $('.pa-f2', g);
      takt.push(function () {
        if (!sicht(b)) return;
        f.style.transform = 'translate3d(0,' + (schmal() ? 0 : (lage(b) - .5) * -16).toFixed(2) + 'vh,0)';
      });
    },
    13: function () {
      var r = $('.rg', g), f = $('.rg-f img', g);
      takt.push(function () {
        if (!sicht(r)) return;
        var b = r.getBoundingClientRect(), p = kl(-b.top / Math.max(1, b.height - H() * .7));
        f.style.setProperty('--rg', (1.22 - .22 * p).toFixed(4));
      });
    },
    15: function () {
      var f = $('.mm-f', g), img = $('.mm-f img', g);
      takt.push(function () {
        if (schmal() || !sicht(f)) return;
        img.style.transform = 'translate3d(0,' + ((lage(f) - .5) * 12).toFixed(2) + '%,0)';
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
