/* Wild Side · Programm, «Jemand anderes am Shaker.», Fassungen 16–30: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
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

  var g = document.getElementById('gaeste'), n = g ? +g.getAttribute('data-g') || 0 : 0;
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
  var schalte = function (liste, a) { liste.forEach(function (e, j) { e.classList.toggle('an', j === a); }); };

  var F = {
    // Kamerafahrt: je Gast ein Stück Scrollweg, die Kamera fährt heran und wieder zurück
    22: function () {
      var p0 = $('[data-pin]', g), fe = $('.k22-fenster', g), gr = $('.k22-gruppe', g), bi = $$('.k22-p', g), tx = $$('.k22-t', g), S = 2.1, alt = -1;
      takt.push(function () {
        if (!sicht(p0)) return; var t = pin(p0) * bi.length, i = Math.min(bi.length - 1, Math.floor(t)), f = t - i;
        var s = ruhig ? 1 : 1 + (S - 1) * Math.sin(Math.PI * kl(f * 1.15 - .075)), k = (s - 1) / (S - 1);
        var b = bi[i], W = fe.clientWidth, Hh = fe.clientHeight, x = b.offsetLeft + b.offsetWidth / 2, y = b.offsetTop + b.offsetHeight * .4;
        gr.style.transform = 'translate3d(' + ((W / 2 - s * x) * k).toFixed(1) + 'px,' + ((Hh / 2 - s * y) * k).toFixed(1) + 'px,0) scale(' + s.toFixed(3) + ')';
        if (i !== alt) { alt = i; schalte(tx, i); }
      });
    },
    // Übereinander: die untere Tafel tritt zurück, sobald die nächste über ihr liegt
    24: function () {
      var t = $$('.t24-t', g);
      takt.push(function () {
        if (ruhig) return;
        t.forEach(function (e, j) { var nx = t[j + 1]; if (!nx) return; var a = e.getBoundingClientRect().top, b = nx.getBoundingClientRect().top;
          var q = kl(1 - (b - a) / (H() * .7)); $('.t24-innen', e).style.setProperty('--z', (1 - q * .06).toFixed(3)); });
      });
    },
    // Laufbänder: oben nach links, unten nach rechts, vom Scrollen getrieben
    25: function () {
      var w = $('[data-baender]', g), o = $('.l25-oben', g), u = $('.l25-unten', g);
      takt.push(function () {
        if (ruhig || !sicht(w)) return; var m = mitte(w), wo = o.scrollWidth / 2, wu = u.scrollWidth / 2;
        o.style.transform = 'translate3d(' + (-wo * .25 + m * -260).toFixed(1) + 'px,0,0)';
        u.style.transform = 'translate3d(' + (-wu * .35 - m * -260).toFixed(1) + 'px,0,0)';
      });
    },
    // Tresen von oben: richtet sich auf, bis er gerade steht
    28: function () {
      var r = $('[data-tresen]', g), f = $('.o28-flaeche', g);
      takt.push(function () { if (!sicht(r)) return; var q = ruhig ? 0 : kl((mitte(r) + .05) / .6); f.style.setProperty('--t', (q * 58).toFixed(1)); });
    },
    // Erst Schwarzweiss: einer nach dem anderen bekommt von links seine Farbe
    29: function () {
      var r = $('[data-farbe]', g), p = $$('.s29-p', g);
      takt.push(function () {
        if (!sicht(r)) return; var q = ruhig ? 1 : kl((H() * .85 - r.getBoundingClientRect().top) / (H() * .75)), z = Math.round(q * p.length);
        p.forEach(function (e, j) { e.classList.toggle('farbe', j < z); });
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
