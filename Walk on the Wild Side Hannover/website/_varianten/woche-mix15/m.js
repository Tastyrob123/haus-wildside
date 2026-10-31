/* Wild Side · Programm, «Die Woche», 15 Mischungen aus Tafel und Deckeln: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var weich = function (t) { return t * t * (3 - 2 * t); };
  var H = function () { return innerHeight; };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };
  var mitte = function (el) { var r = el.getBoundingClientRect(); return (r.top + r.height / 2 - H() / 2) / H(); };

  var g = document.getElementById('woche'), n = g ? +g.getAttribute('data-w') || 0 : 0;
  if (!n) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -18% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('da'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  var schalte = function (liste, a) { liste.forEach(function (e, j) { e.classList.toggle('an', j === a); }); };
  var drehe = function (ring, grad) { ring.style.setProperty('--r', grad.toFixed(1)); };

  var F = {
    // Die Zeile des Abends in der Bildmitte leuchtet, die Ringe drehen mit
    4: function () {
      var ab = $$('.m4-abend', g), z = $$('.m4-tafel p', g).slice(2), alt = -1;
      takt.push(function () {
        if (!sicht(g)) return; var best = 0, d = 9;
        ab.forEach(function (e, j) { var m = Math.abs(mitte(e)); if (m < d) { d = m; best = j; } if (!ruhig) drehe($('.md-ring', e), mitte(e) * -120); });
        if (best !== alt) { alt = best; schalte(z, best); }
      });
    },
    5: function () { if (ruhig) return; $$('[data-ring]', g).forEach(function (s, j) { var r = $('.md-ring', s); takt.push(function () { if (sicht(s)) drehe(r, mitte(s) * (j % 2 ? 110 : -110)); }); }); },
    6: function () {
      var p0 = $('[data-pin]', g), l = $$('.m6-lage', g), s = $$('.m6-satz', g), z = $$('.m6-tafel p', g).slice(2), ringe = $$('.m6-lage .md-ring', g), alt = -1;
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var p = pin(p0), a = Math.min(2, Math.floor(p * 3));
        if (!ruhig) ringe.forEach(function (r) { drehe(r, p * -300); });
        if (a !== alt) { alt = a; schalte(l, a); schalte(s, a); schalte(z, a); }
      });
    },
    11: function () {
      var p0 = $('[data-pin]', g), d = $$('.m11-roll .md', g), s = $$('.m11-satz', g);
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var p = ruhig ? 1 : pin(p0);
        d.forEach(function (e, j) {
          var q = weich(kl(p * 1.7 - j * .28)), w = innerWidth * (.35 + j * .3);   // rollt so weit, wie der Deckel von links her zurücklegt
          e.style.transform = 'translate3d(' + (-(1 - q) * w).toFixed(1) + 'px,0,0) rotate(' + (-(1 - q) * w / (e.offsetWidth * Math.PI) * 360).toFixed(1) + 'deg)';
          s[j].classList.toggle('an', q > .97);
        });
      });
    },
    15: function () {
      var p0 = $('[data-pin]', g), l = $$('.m15-lage', g), d = $$('.m15-d', g), s = $$('.m15-satz', g), alt = -1;
      $('.m15-tafel', g).classList.add('da');
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var a = Math.min(2, Math.floor(pin(p0) * 3));
        if (a !== alt) { alt = a; schalte(l, a); schalte(s, a); schalte(d, a); d.forEach(function (e, j) { e.classList.toggle('weg', j < a); }); }
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
