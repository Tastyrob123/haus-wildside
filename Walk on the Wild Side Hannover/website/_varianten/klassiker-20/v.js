/* Wild Side · Drinks, «Die Klassiker»: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
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
  // welches Element steht der Bildmitte am nächsten
  var mitte = function (els) { var m = H() / 2, best = 0, d0 = 1e9; els.forEach(function (e, i) { var r = e.getBoundingClientRect(), d = Math.abs((r.top + r.bottom) / 2 - m); if (d < d0) { d0 = d; best = i; } }); return best; };

  var takt = [], neu = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', function () { neu.forEach(function (f) { f(); }); lauf(); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -16% 0px' }) : null;
  $$('.vauf').forEach(function (el) { io ? io.observe(el) : el.classList.add('da'); });

  var g = document.getElementById('klassiker'); if (!g) return;
  var n = +((g.className.match(/\bv(\d\d)\b/) || [])[1] || 0);

  var F = {
    1: function () {
      var e = $$('.w-e', g), b = $$('.w-b', g), j0 = 0;
      takt.push(function () {
        if (!sicht(g)) return; var j = mitte(e); if (j === j0) return;
        e.forEach(function (x, i) { x.classList.toggle('an', i === j); }); b.forEach(function (x, i) { x.classList.toggle('an', i === j); }); j0 = j;
      });
    },
    2: function () {
      var s = $$('.sp-g', g), li = $$('.sp-idx li', g), j0 = 0;
      takt.push(function () {
        if (!sicht(g)) return; var j = mitte(s); if (j === j0) return;
        li.forEach(function (x, i) { x.classList.toggle('an', i === j); }); j0 = j;
      });
    },
    4: function () {
      var z = $$('.af-z', g);
      if (ruhig) return;
      takt.push(function () {
        if (!sicht(g)) return;
        if (schmal()) { z.forEach(function (x) { x.style.opacity = ''; }); return; }
        var m = H() * .5;
        z.forEach(function (x) { var r = x.getBoundingClientRect(), d = Math.abs((r.top + r.bottom) / 2 - m) / (H() * .32); x.style.opacity = (1 - .74 * kl(d)).toFixed(3); });
      });
    },
    9: function () {
      var s = $$('.st-s', g), gr = $('.st-gr', g);
      if (ruhig) { s.forEach(function (x, i) { x.style.transform = 'translate3d(0,' + i * 9 + 'vh,0)'; }); return; }
      takt.push(function () {
        if (schmal()) { s.forEach(function (x) { x.style.transform = ''; }); return; }
        if (!sicht(gr)) return;
        var r = gr.getBoundingClientRect(), p = aus(kl((H() * .95 - r.top) / (H() * .7)));
        s.forEach(function (x, i) { x.style.transform = 'translate3d(0,' + (i * 9 * p).toFixed(2) + 'vh,0)'; });
      });
    },
    10: function () {
      var p = $('[data-pin]', g), b = $$('.en-b', g), z = $$('.en-z', g), st = $$('.en-striche i', g), j0 = 0;
      takt.push(function () {
        if (schmal() || !sicht(p)) return;
        var j = Math.min(3, Math.floor(pin(p) * 4 * 1.0001)); if (j === j0) return;
        [b, z].forEach(function (l) { l.forEach(function (x, i) { x.classList.toggle('an', i === j); x.classList.toggle('war', i < j); }); });
        st.forEach(function (x, i) { x.classList.toggle('an', i <= j); }); j0 = j;
      });
    },
    11: function () {
      var s = $$('.li-s', g), gr = $('.li-gr', g);
      if (ruhig) { s.forEach(function (x) { x.style.opacity = 1; }); return; }
      takt.push(function () {
        if (schmal() || !sicht(gr)) return;
        var r = gr.getBoundingClientRect(), p = kl((H() * .85 - r.top) / (H() * .85 + r.height * .2)) * 3.4 - .2;
        s.forEach(function (x, i) { x.style.opacity = (1 - .72 * kl(Math.abs(p - i) * .9)).toFixed(3); });
      });
    },
    14: function () {
      var p = $('[data-gl]', g), platz = $('.gl-platz', g), b = $('.gl-bild', g), t = $('.gl-txt', g);
      if (ruhig) return;
      takt.push(function () {
        if (schmal()) { b.style.transform = ''; return; }
        if (!sicht(p)) return;
        var e = aus(kl(pin(p) / .7)), r = platz.getBoundingClientRect(), w = r.width, h = r.height;
        var s = Math.max(innerWidth / w, H() / h), x0 = (innerWidth - w * s) / 2 - r.left, y0 = (H() - h * s) / 2 - r.top;
        var sc = s + (1 - s) * e;
        b.style.transform = 'translate3d(' + (x0 * (1 - e)).toFixed(1) + 'px,' + (y0 * (1 - e)).toFixed(1) + 'px,0) scale(' + sc.toFixed(4) + ')';
        var f = kl((e - .55) / .45);
        t.style.opacity = f.toFixed(3); t.style.transform = 'translate3d(0,' + (40 * (1 - f)).toFixed(1) + 'px,0)';
      });
    },
    15: function () {
      var f = $('.hh-bild', g), img = $('.hh-bild img', g);
      if (ruhig) return;
      takt.push(function () {
        if (schmal() || !sicht(f)) return;
        var r = f.getBoundingClientRect(), p = kl((H() - r.top) / (H() + r.height));
        img.style.transform = 'translate3d(0,' + ((p - .5) * 12).toFixed(2) + '%,0)';
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
