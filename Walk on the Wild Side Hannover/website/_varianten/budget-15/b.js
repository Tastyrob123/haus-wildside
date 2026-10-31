/* Wild Side · Feiern, «Ein Rahmen, den ihr setzt.», 15 Darstellungen: was am Scrollen hängt. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .3 && r.top < H() * 1.3; };
  // 0 wenn das Element unten hereinkommt, 1 wenn seine Mitte etwas über der Bildschirmmitte steht
  var weg = function (el, bis) { var r = el.getBoundingClientRect(); return kl((H() - r.top) / (H() * (bis || .8))); };

  var g = document.getElementById('budget'), n = g ? +g.getAttribute('data-b') || 0 : 0;
  if (!n) return;

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var F = {
    // Das Glas füllt sich bis zur Marke
    3: function () {
      var gl = $('[data-fuell]', g), d = $('.g3-drink', g);
      if (ruhig) { d.style.transform = 'translateY(22%)'; gl.classList.add('voll'); return; }
      takt.push(function () { if (!sicht(gl)) return; var p = weg(gl, 1.1); d.style.transform = 'translateY(' + (100 - p * 78).toFixed(2) + '%)'; gl.classList.toggle('voll', p > .97); });
    },
    // Die Rückbar rückt in ihrem Rahmen näher
    6: function () {
      var b = $('[data-nah] img', g), f = $('[data-nah]', g);
      if (ruhig) return;
      takt.push(function () { if (!sicht(f)) return; b.style.transform = 'scale(' + (1.16 - weg(f, 1.4) * .16).toFixed(4) + ')'; });
    },
    // Zwei Karten fächern auseinander
    12: function () {
      var f = $('[data-faecher]', g), h = $('.f12-hell', g), d = $('.f12-dunkel', g);
      if (ruhig || matchMedia('(max-width:900px)').matches) { f.classList.add('offen'); return; }
      takt.push(function () {
        if (!sicht(f)) return; var p = weg(f, 1.2);
        h.style.transform = 'translate3d(' + (-p * 62).toFixed(1) + '%,' + (60 - p * 20).toFixed(1) + 'px,0) rotate(' + (-6 + p * 3).toFixed(2) + 'deg)';
        d.style.transform = 'translate3d(' + (p * 62).toFixed(1) + '%,0,0) rotate(' + (5 - p * 3).toFixed(2) + 'deg)';
      });
    },
    // Die Walze dreht von Drink zu Drink
    15: function () {
      var r = $('[data-walze]', g), w = $('.w15-walze', g), z = $$('.w15-z', g), alt = -1;
      var stell = function (a) {
        if (a === alt) return; alt = a;
        w.style.transform = 'translate3d(0,' + (-a * 100 / z.length).toFixed(4) + '%,0)';
        z.forEach(function (e, j) { e.classList.toggle('an', j === a); e.classList.toggle('nah', Math.abs(j - a) === 1); });
      };
      stell(0);
      if (ruhig) return;
      takt.push(function () {
        if (!sicht(r)) return; var q = r.getBoundingClientRect();
        var p = kl((H() * .55 - q.top) / Math.max(1, q.height - H() * .45));
        stell(Math.min(z.length - 1, Math.floor(p * z.length)));
      });
    }
  };
  if (F[n]) { F[n](); lauf(); }
})();
