/* Wild Side · Feiern, «Der Klang dazu.», Fassungen 01–15: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };
  var mitte = function (el) { var r = el.getBoundingClientRect(); return (r.top + r.height / 2 - H() / 2) / H(); };

  var g = document.getElementById('musik'), n = g ? +g.getAttribute('data-m') || 0 : 0;
  if (!n) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -18% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var F = {
    // Spot: einer nach dem anderen wird hell
    4: function () {
      var r = $('[data-spot]', g), p = $$('.s4-p', g);
      takt.push(function () {
        if (!sicht(r)) return; var q = ruhig ? 1 : kl((H() * .75 - r.getBoundingClientRect().top) / (H() * .7)), z = Math.round(q * (p.length + .4) - .2);
        p.forEach(function (e, j) { e.classList.toggle('an', j < z); });
      });
    },
    // Grosse Worte: jedes Wort wandert seitwärts durch seine Zeile
    7: function () {
      var w = $$('[data-wort]', g);
      takt.push(function () {
        if (ruhig) return;
        w.forEach(function (e, j) { if (!sicht(e)) return; var x = kl(mitte(e) + .45) * (schmal() ? 50 : 150) * (j % 2 ? -1 : 1);
          e.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)'; });
      });
    },
    // Bühnenfahrt: die Spur fährt seitwärts, solange der Abschnitt steht
    11: function () {
      var p0 = $('[data-pin]', g), sp = $('.b11-spur', g);
      takt.push(function () {
        if (schmal()) { sp.style.transform = ''; return; }
        if (!sicht(p0)) return; var q = pin(p0), weg = Math.max(0, sp.scrollWidth - innerWidth);
        sp.style.transform = 'translate3d(' + (-q * weg).toFixed(1) + 'px,0,0)';
      });
    },
    // Stapel: fächert sich in die Reihe
    12: function () {
      var r = $('[data-stapel]', g);
      takt.push(function () {
        if (!sicht(r)) return; var q = ruhig || schmal() ? 1 : kl((H() * .95 - r.getBoundingClientRect().top) / (H() * .6));
        r.style.setProperty('--q', q.toFixed(3)); r.classList.toggle('fertig', q > .97);
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
