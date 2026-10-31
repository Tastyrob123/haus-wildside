/* Wild Side · Feiern, «Grösser als die Bar.», Fassungen 01–15 (Runde 2): die eigene Bewegung jeder Fassung. Nur transform, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };
  var mitte = function (el) { var r = el.getBoundingClientRect(); return (r.top + r.height / 2 - H() / 2) / H(); };

  var g = document.getElementById('events'), n = g ? +g.getAttribute('data-x') || 0 : 0;
  if (!n) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -15% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var F = {
    // Zwei Säulen: gleiten gegeneinander
    6: function () {
      var r = $('[data-saeulen]', g), l = $('.d6-l .xf', g), q = $('.d6-r .xf', g);
      takt.push(function () { if (ruhig || !sicht(r)) return; var m = mitte(r) * (schmal() ? 40 : 110);
        l.style.transform = 'translate3d(0,' + m.toFixed(1) + 'px,0)'; q.style.transform = 'translate3d(0,' + (-m).toFixed(1) + 'px,0)'; });
    },
    // Filmstreifen: gleitet langsamer als die Seite
    11: function () {
      var s = $('[data-film]', g);
      takt.push(function () { if (ruhig || schmal() || !sicht(s)) return; s.style.transform = 'translate3d(0,' + (mitte(s) * -90).toFixed(1) + 'px,0)'; });
    },
    // Halb und halb: die Theke gleitet im Rahmen
    13: function () {
      var b = $('[data-halb]', g), i = $('img', b);
      takt.push(function () { if (ruhig || !sicht(b)) return; i.style.transform = 'translate3d(0,' + (mitte(b) * -60).toFixed(1) + 'px,0) scale(1.14)'; });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
