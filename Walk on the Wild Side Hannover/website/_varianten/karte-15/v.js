/* Wild Side · Drinks, «Die einzige Karte»: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var aus = function (t) { return 1 - Math.pow(1 - t, 3); };
  var H = function () { return innerHeight; };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() && r.top < 2 * H(); };

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

  var F = {
    6: function () {
      var p = $('[data-pin]', g), d = $$('.eb-d', g), st = $$('.eb-striche i', g), j0 = 0;
      takt.push(function () {
        if (schmal() || !sicht(p)) return;
        var j = Math.min(3, Math.floor(pin(p) * 4 * 1.0001)); if (j === j0) return;
        d.forEach(function (x, i) { x.classList.toggle('an', i === j); x.classList.toggle('war', i < j); });
        st.forEach(function (x, i) { x.classList.toggle('an', i <= j); }); j0 = j;
      });
    },
    8: function () {
      var t = $('.ta', g), bl = $('.ta-bl', g);
      if (ruhig) { bl.style.setProperty('--ta', '0%'); return; }
      takt.push(function () {
        if (!sicht(t)) return;
        var r = t.getBoundingClientRect(), p = aus(kl((H() * .95 - r.top) / (H() * .75)));
        bl.style.setProperty('--ta', (70 * (1 - p)).toFixed(2) + '%');
      });
    },
    9: function () {
      var f = $('.hh-bild', g), img = $('.hh-bild img', g);
      if (ruhig) return;
      takt.push(function () {
        if (schmal() || !sicht(f)) return;
        var r = f.getBoundingClientRect(), p = kl((H() - r.top) / (H() + r.height));
        img.style.transform = 'translate3d(0,' + ((p - .5) * 12).toFixed(2) + '%,0)';
      });
    },
    10: function () {
      var w = $('[data-wg]', g), b = $('.wg-linie b', g), h = $$('.wg-h', g);
      if (ruhig) { b.style.setProperty('--wg', 1); h.forEach(function (x) { x.classList.add('an'); }); return; }
      takt.push(function () {
        if (!sicht(w)) return;
        var r = w.getBoundingClientRect(), p = kl((H() * .8 - r.top) / (H() * .6));
        b.style.setProperty('--wg', p.toFixed(3));
        h[0].classList.toggle('an', p > .02); h[1].classList.toggle('an', p > .55);
      });
    },
    11: function () {
      var f = $('[data-fa]', g), k = $$('.fa-k', g);
      if (ruhig) return;
      takt.push(function () {
        if (!sicht(f)) return;
        if (schmal()) { k.forEach(function (x) { x.style.transform = ''; }); return; }
        var r = f.getBoundingClientRect(), p = aus(kl((H() * .92 - r.top) / (H() * .62)));
        var w = k[0].getBoundingClientRect().width + parseFloat(getComputedStyle(f).columnGap || 0);
        k.forEach(function (x, i) {
          var dx = (1.5 - i) * w * (1 - p), rot = (i - 1.5) * 5 * (1 - p), dy = Math.abs(i - 1.5) * 18 * (1 - p);
          x.style.transform = 'translate3d(' + dx.toFixed(1) + 'px,' + dy.toFixed(1) + 'px,0) rotate(' + rot.toFixed(2) + 'deg)';
        });
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
