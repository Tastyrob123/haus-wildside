/* Wild Side · Drinks, 15 Fassungen «Gespräch und Techniken»: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = matchMedia('(max-width:900px)').matches;
  function lade(f) { var img = f && f.querySelector('img[data-srcset]'); if (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); } }
  function zeige(stapel, j) {
    var f = $$('.foto', stapel), neu = f[j], alt = $('.foto.an', stapel);
    if (!neu || neu === alt) return;
    f.forEach(function (x) { x.classList.remove('war'); });
    if (alt) { alt.classList.remove('an'); alt.classList.add('war'); }
    lade(neu); neu.classList.add('an');
  }
  function markiere(l, j) { l.forEach(function (x, i) { x.classList.toggle('an', i === j); }); }
  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var F = {
    1: function (g) {
      $$('[data-w1]', g).forEach(function (w) {
        var linie = $('.w1-linie i', w), st = $$('.w1-st', w);
        if (ruhig) { linie.style.transform = 'none'; st.forEach(function (s) { s.classList.add('an'); }); return; }
        takt.push(function () {
          var h = innerHeight, r = w.getBoundingClientRect(); if (r.bottom < -h || r.top > 2 * h) return;
          linie.style.transform = 'scaleY(' + Math.max(0, Math.min(1, (h * .6 - r.top) / r.height)).toFixed(4) + ')';
          st.forEach(function (s) { var q = s.getBoundingClientRect(); s.classList.toggle('an', q.top + q.height / 2 < h * .6); });
        });
      });
    },
    3: function (g) {
      $$('.g3', g).forEach(function (t) {
        var stapel = $('.g3-stapel', t), bl = $$('.g3-block', t);
        if (!('IntersectionObserver' in window)) return;
        var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { zeige(stapel, +e.target.dataset.j); markiere(bl, +e.target.dataset.j); } }); }, { rootMargin: '-42% 0px -42% 0px' });
        bl.forEach(function (b) { io.observe(b); }); markiere(bl, 0);
      });
    },
    8: function (g) {
      $$('.g8', g).forEach(function (t) {
        var stapel = $('.g8-stapel', t), z = $$('.g8-z', t);
        z.forEach(function (b, i) { function w() { zeige(stapel, i); markiere(z, i); } b.addEventListener('mouseenter', w); b.addEventListener('focus', w); b.addEventListener('click', w); });
      });
    },
    12: function (g) {
      var band = $('.g12-band', g); if (!band) return;
      $$('.g12-pf', g).forEach(function (p) {
        p.addEventListener('click', function () { var k = $('.g12-k', band); band.scrollBy({ left: +p.dataset.d * (k.offsetWidth + 14), behavior: ruhig ? 'auto' : 'smooth' }); });
      });
      function knoepfe() { var p = $$('.g12-pf', g); p[0].disabled = band.scrollLeft < 8; p[1].disabled = band.scrollLeft > band.scrollWidth - band.clientWidth - 8; }
      band.addEventListener('scroll', knoepfe, { passive: true }); knoepfe();
    },
    13: function (g) {
      var t = $('.g13', g); if (!t) return;
      var stapel = $('.g13-stapel', t), st = $$('.g13-striche button', t), sa = $$('.g13-s', t), j = 0, uhr = 0, halt = false, im = false;
      function geh(z) {
        j = (z + st.length) % st.length; zeige(stapel, j); markiere(sa, j);
        st.forEach(function (b, i) { b.classList.toggle('war', i < j); b.classList.remove('an'); });
        void st[j].offsetWidth; st[j].classList.add('an');
        clearTimeout(uhr); if (!halt && im && !ruhig) uhr = setTimeout(function () { geh(j + 1); }, 5200);
      }
      st.forEach(function (b, i) { b.addEventListener('click', function () { geh(i); }); });
      stapel.addEventListener('mouseenter', function () { halt = true; clearTimeout(uhr); t.classList.add('halt'); });
      stapel.addEventListener('mouseleave', function () { halt = false; t.classList.remove('halt'); geh(j); });
      if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { var war = im; im = es[0].isIntersecting; if (im && !war) geh(j); if (!im) clearTimeout(uhr); }, { threshold: .35 }).observe(t);
    },
    14: function (g) {
      if (ruhig || schmal) return;
      $$('.g14', g).forEach(function (t) {
        var sp = $$('.g14-sp', t);
        takt.push(function () {
          var r = t.getBoundingClientRect(); if (r.bottom < -innerHeight || r.top > 2 * innerHeight) return;
          var d = r.top + r.height / 2 - innerHeight / 2;
          sp.forEach(function (s) { s.style.transform = 'translateY(' + (d * +s.dataset.tempo).toFixed(1) + 'px)'; });
        });
      });
    },
    15: function (g) {
      var bue = $('.g15-buehne', g); if (!bue) return;
      var bild = $('.g15-bild', bue); lade($('.foto', bild));
      if (ruhig) { bild.style.transform = 'none'; return; }
      takt.push(function () {
        var r = bue.getBoundingClientRect(), weg = r.height - innerHeight; if (r.bottom < 0 || r.top > innerHeight) return;
        var q = Math.max(0, Math.min(1, -r.top / (weg || 1)));
        bild.style.transform = 'scale(' + (.46 + .54 * Math.min(1, q / .8)).toFixed(4) + ')';
      });
    }
  };
  var fertig = {};
  $$('[data-g]').forEach(function (g) { var n = g.dataset.g, f = F[n]; if (f) f(g); fertig[n] = 1; });
  lauf();
})();
