/* Wild Side · Feiern, «Die ganze Bar», 15 Darstellungen: Auftritt beim Erscheinen am Rand und die scrollgetriebenen Fassungen in einem Takt. Nur transform. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .3 && r.top < H() * 1.3; };

  var g = document.getElementById('bar'), n = g ? +g.getAttribute('data-g') || 0 : 0;
  if (!n) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -12% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var F = {
    // Der leere Raum: das Bild zieht sich beim Scrollen aus der Nähe in seinen Rahmen zurück
    6: function () {
      var r = $('[data-zoom]', g), img = $('img', r);
      takt.push(function () {
        if (!sicht(r)) return; var b = r.getBoundingClientRect(), q = ruhig ? 1 : kl((H() - b.top) / (H() * .9));
        img.style.setProperty('--s', (1.18 - .18 * q).toFixed(4));
      });
    },
    // Bild zum Text: zu jedem Schritt rechts schiebt sich das passende Foto von unten in den Rahmen
    9: function () {
      var s = $$('.w09-s', g), b = $$('.w09-b', g), alt = -1;
      takt.push(function () {
        var a = 0; s.forEach(function (e, j) { if (e.getBoundingClientRect().top < H() * .55) a = j; });
        if (a === alt) return; alt = a; b.forEach(function (e, j) { e.classList.toggle('an', j <= a); });
      });
    },
    // Die grosse Schrift: die vier Fotos steigen beim Scrollen verschieden schnell
    15: function () {
      var w = $('[data-streifen]', g), b = $$('.g15-b', g);
      takt.push(function () {
        if (ruhig || !sicht(w)) return; var r = w.getBoundingClientRect(), m = (r.top + r.height / 2 - H() / 2) / H();
        b.forEach(function (e) { e.style.setProperty('--y', (m * parseFloat(e.style.getPropertyValue('--t')) * 600).toFixed(1) + 'px'); });
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
