/* Wild Side · Drinks, 20 neue Darstellungen: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var aus = function (t) { return 1 - Math.pow(1 - t, 3); };
  var weich = function (t) { return t * t * (3 - 2 * t); };
  var H = function () { return innerHeight; };
  // Fortschritt, während die Oberkante von a*Höhe nach b*Höhe wandert
  var weg = function (r, a, b) { return kl((a * H() - r.top) / ((a - b) * H())); };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() && r.top < 2 * H(); };

  var takt = [], neu = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', function () { neu.forEach(function (f) { f(); }); lauf(); });

  function lade(root) { $$('img[data-srcset]', root).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); }); }

  // Auftritte einzelner Gruppen (.vauf): einmal, sobald sie gut im Bild sind
  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -14% 0px' }) : null;
  $$('.vauf').forEach(function (el) { io ? io.observe(el) : el.classList.add('da'); });

  var F = {
    1: function (g) {
      $$('[data-pin]', g).forEach(function (p) {
        var zug = $('.q-zug', p), breite = 0;
        function mass() { if (schmal()) { p.style.height = ''; return; } breite = zug.scrollWidth - innerWidth; p.style.height = (breite + H() * 1.15) + 'px'; }
        neu.push(mass); mass();
        takt.push(function () { if (schmal() || !sicht(p)) return; zug.style.transform = 'translate3d(' + (-pin(p) * breite).toFixed(1) + 'px,0,0)'; });
      });
    },
    3: function (g) {
      $$('[data-pin]', g).forEach(function (p) {
        var b = $$('.u-b', p), z = $$('.u-z', p), s = $$('.u-striche i', p), j0 = 0;
        takt.push(function () {
          if (schmal() || !sicht(p)) return;
          var j = Math.min(b.length - 1, Math.floor(pin(p) * b.length * 1.0001));
          if (j === j0) return;
          b.forEach(function (x, i) { x.classList.toggle('an', i === j); x.classList.toggle('war', i < j); });
          z.forEach(function (x, i) { x.classList.toggle('an', i === j); });
          s.forEach(function (x, i) { x.classList.toggle('an', i <= j); });
          j0 = j;
        });
      });
    },
    4: function (g) {
      $$('[data-f]', g).forEach(function (f) {
        var k = $$('.f-karte', f);
        if (ruhig) { f.classList.add('offen'); return; }
        takt.push(function () {
          if (schmal()) { k.forEach(function (x) { x.style.transform = ''; }); f.classList.add('offen'); return; }
          if (!sicht(f)) return;
          var e = aus(weg(f.getBoundingClientRect(), 1, .45)), w = k[1].offsetWidth + parseFloat(getComputedStyle(f).columnGap || 0);
          k.forEach(function (x, j) {
            var o = j - 1;
            x.style.transform = 'translate3d(' + (-o * w * .86 * (1 - e)).toFixed(1) + 'px,' + (Math.abs(o) * 26 * (1 - e)).toFixed(1) + 'px,0) rotate(' + (o * 8 * (1 - e)).toFixed(2) + 'deg)';
          });
          f.classList.toggle('offen', e > .97);
        });
      });
    },
    5: function (g) {
      $$('[data-k]', g).forEach(function (st) {
        var k = $$('.k-karte', st);
        if (ruhig) return;
        takt.push(function () {
          if (schmal() || !sicht(st)) return;
          k.forEach(function (x, i) {
            var n = k[i + 1]; if (!n) return;
            var d = n.getBoundingClientRect().top - x.getBoundingClientRect().top, c = kl(1 - d / x.offsetHeight);
            x.style.transform = 'scale(' + (1 - .06 * c).toFixed(4) + ')';
          });
        });
      });
    },
    6: function (g) {
      $$('[data-w]', g).forEach(function (b) {
        var w = $$('.w-w', b);
        if (ruhig) { w.forEach(function (x) { x.classList.add('an'); }); return; }
        takt.push(function () {
          if (!sicht(b)) return;
          var n = Math.ceil(weg(b.getBoundingClientRect(), .86, .4) * w.length);
          w.forEach(function (x, i) { x.classList.toggle('an', i < n); });
        });
      });
    },
    8: function (g) {
      $$('[data-m]', g).forEach(function (m) {
        var teile = [].slice.call(m.children), ops = $$('[data-o]', m), c = (teile.length - 1) / 2;
        function mass() { var k = $('.kachel', m); if (k) m.style.setProperty('--opy', Math.max(0, k.offsetHeight / 2 - 26) + 'px'); }
        neu.push(mass); mass(); addEventListener('load', mass);
        if (ruhig) return;
        takt.push(function () {
          if (schmal()) { teile.forEach(function (x) { x.style.transform = ''; x.style.opacity = ''; }); return; }
          if (!sicht(m)) return;
          var e = aus(weg(m.getBoundingClientRect(), .92, .4));
          teile.forEach(function (x, i) { x.style.transform = 'translate3d(' + ((i - c) * 30 * (1 - e)).toFixed(1) + 'px,0,0)'; });
          ops.forEach(function (o) { o.style.opacity = (e * e).toFixed(3); });
        });
      });
    },
    9: function (g) {
      $$('[data-pin]', g).forEach(function (p) {
        var pr = $('.p-prisma', p);
        takt.push(function () {
          if (schmal()) { pr.style.transform = ''; return; }
          if (!sicht(p)) return;
          var pos = pin(p) * 2, i = Math.min(2, Math.floor(pos)), s = i >= 2 ? 0 : weich(kl((pos - i - .2) / .6));
          pr.style.transform = 'translateZ(' + (-pr.offsetWidth * .2887).toFixed(1) + 'px) rotateY(' + (-(i + s) * 120).toFixed(2) + 'deg)';
        });
      });
    },
    10: function (g) {
      $$('[data-a]', g).forEach(function (a) {
        var oben = 0;
        function mass() { var t = a.style.transform; a.style.transform = 'none'; oben = a.getBoundingClientRect().top + scrollY; a.style.transform = t; }
        neu.push(mass); mass(); addEventListener('load', mass);
        if (ruhig) return;
        takt.push(function () {
          if (schmal()) { a.style.transform = ''; a.style.opacity = ''; return; }
          var top = oben - scrollY; if (top > 2 * H() || top < -H()) return;
          var e = aus(kl((.98 * H() - top) / (.4 * H())));
          a.style.transform = 'rotateX(' + ((1 - e) * 74).toFixed(2) + 'deg)';
          a.style.opacity = (.2 + .8 * e).toFixed(3);
        });
      });
    },
    13: function (g) {
      $$('.r-wort', g).forEach(function (w) {
        var d = +w.dataset.r, sek = w.parentNode;
        if (ruhig) return;
        takt.push(function () {
          if (schmal() || !sicht(sek)) return;
          var r = sek.getBoundingClientRect(), q = kl((H() - r.top) / (H() + r.height)), rest = w.offsetWidth - innerWidth * .7;
          var x = d > 0 ? innerWidth * .12 - q * rest : -rest + q * rest + innerWidth * .12;
          w.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,0)';
        });
      });
    },
    15: function (g) {
      $$('[data-kw]', g).forEach(function (f) {
        var t = $('.kw-trueb', f);
        if (ruhig) { t.style.opacity = 0; return; }
        takt.push(function () { if (!sicht(f)) return; t.style.opacity = (1 - weich(weg(f.getBoundingClientRect(), .92, .35))).toFixed(3); });
      });
    },
    16: function (g) {
      $$('[data-e]', g).forEach(function (gl) {
        var fu = $('.e-fuell', gl), ge = $('.e-gegen', gl), j = +gl.style.getPropertyValue('--j') || 0;
        function setz(e) { fu.style.transform = 'translate3d(0,' + ((1 - e) * 100).toFixed(2) + '%,0)'; ge.style.transform = 'translate3d(0,' + (-(1 - e) * 100).toFixed(2) + '%,0)'; }
        if (ruhig) { setz(1); return; }
        takt.push(function () { if (!sicht(gl)) return; var r = gl.getBoundingClientRect(); setz(weich(kl((.96 * H() - r.top - j * .05 * H()) / (.5 * H())))); });
      });
    },
    19: function (g) {
      $$('[data-pin]', g).forEach(function (p) {
        var bl = $$('.h-blatt', p), n = bl.length;
        takt.push(function () {
          if (schmal()) { bl.forEach(function (b) { b.style.transform = ''; }); return; }
          if (!sicht(p)) return;
          var pos = pin(p) * n;
          bl.forEach(function (b, j) {
            var t = weich(kl((pos - j) * 1.25 - .12)), a = -180 * t;
            b.style.transform = 'rotateY(' + a.toFixed(2) + 'deg)';
            b.style.zIndex = a > -90 ? 20 - j : 20 + j;
          });
        });
      });
    },
    20: function (g) {
      var z = $$('[data-z]', g);
      if (ruhig || !('IntersectionObserver' in window)) { z.forEach(function (x) { x.classList.add('an'); }); return; }
      var o = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { setTimeout(function () { e.target.classList.add('an'); }, 180); o.unobserve(e.target); } }); }, { rootMargin: '0px 0px -22% 0px' });
      z.forEach(function (x) { o.observe(x); });
    }
  };

  $$('section[data-g]').forEach(function (g) { var f = F[+g.dataset.g]; if (f) f(g); });
  // Bilder der beiden Abschnitte gleich mitladen (gepinnte und gedrehte Bühnen liegen zum Teil ausserhalb des Blicks)
  addEventListener('load', function () { $$('section[data-g]').forEach(lade); neu.forEach(function (f) { f(); }); lauf(); });
  lauf();
})();
