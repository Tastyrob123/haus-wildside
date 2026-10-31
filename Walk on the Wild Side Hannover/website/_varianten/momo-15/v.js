/* Wild Side · 15 Fassungen «Momo bei der Arbeit»: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  function lade(f) { var img = f && f.querySelector('img[data-srcset]'); if (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); } }
  /* Ein Stapel echter Fotos: das neue kommt von unten, das alte bleibt darunter liegen */
  function zeige(stapel, j) {
    var f = $$('.foto', stapel), neu = f[j], alt = $('.foto.an', stapel);
    if (!neu || neu === alt) return;
    f.forEach(function (x) { x.classList.remove('war'); });
    if (alt) { alt.classList.remove('an'); alt.classList.add('war'); }
    lade(neu); neu.classList.add('an');
  }
  function markiere(liste, j) { liste.forEach(function (x, i) { x.classList.toggle('an', i === j); }); }

  /* Ein Takt für alles, was am Scrollen hängt, und nur solange der Abschnitt im Bild ist */
  var takt = [], sichtbar = false, tick = false;
  function lauf() { tick = false; if (!sichtbar) return; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  var sek = document.getElementById('drinks');
  if (sek && 'IntersectionObserver' in window) new IntersectionObserver(function (es) { sichtbar = es[0].isIntersecting; if (sichtbar) lauf(); }).observe(sek);
  function fortschritt(el, vorlauf) { /* 0 wenn die Oberkante unten am Rand steht, 1 wenn die Unterkante oben angekommen ist */
    var r = el.getBoundingClientRect(), h = innerHeight; return Math.max(0, Math.min(1, (h * (vorlauf || 1) - r.top) / (r.height + h * ((vorlauf || 1) - 1) || 1)));
  }

  var F = {
    2: function (g) {
      var stapel = $('.m2-stapel', g), bl = $$('.m2-block', g);
      if (!('IntersectionObserver' in window)) return;
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { zeige(stapel, +e.target.dataset.j); markiere(bl, +e.target.dataset.j); } }); }, { rootMargin: '-42% 0px -42% 0px' });
      bl.forEach(function (b) { io.observe(b); });
      markiere(bl, 0);
    },
    3: function (g) {
      var band = $('.m3-band', g);
      $$('.m3-pf', g).forEach(function (p) {
        p.addEventListener('click', function () { var s = $('.m3-sch', band); band.scrollBy({ left: +p.dataset.d * (s.offsetWidth + 14), behavior: ruhig ? 'auto' : 'smooth' }); });
      });
      function knoepfe() { var p = $$('.m3-pf', g); p[0].disabled = band.scrollLeft < 8; p[1].disabled = band.scrollLeft > band.scrollWidth - band.clientWidth - 8; }
      band.addEventListener('scroll', knoepfe, { passive: true }); knoepfe();
    },
    4: function (g) {
      var stapel = $('.m4-stapel', g), st = $$('.m4-striche button', g), sa = $$('.m4-s', g), j = 0, t = 0, halt = false, im = false;
      function geh(z) {
        j = (z + st.length) % st.length; zeige(stapel, j); markiere(sa, j);
        st.forEach(function (b, i) { b.classList.toggle('war', i < j); b.classList.remove('an'); });
        void st[j].offsetWidth; st[j].classList.add('an');
        clearTimeout(t); if (!halt && im && !ruhig) t = setTimeout(function () { geh(j + 1); }, 4800);
      }
      st.forEach(function (b, i) { b.addEventListener('click', function () { geh(i); }); });
      var bild = $('.m4-stapel', g);
      bild.addEventListener('mouseenter', function () { halt = true; clearTimeout(t); g.classList.add('halt'); });
      bild.addEventListener('mouseleave', function () { halt = false; g.classList.remove('halt'); geh(j); });
      if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { var war = im; im = es[0].isIntersecting; if (im && !war) geh(j); if (!im) clearTimeout(t); }, { threshold: .35 }).observe(g);
      else { im = true; geh(0); }
    },
    7: function (g) {
      var sp = $$('.m7-sp', g);
      if (ruhig || matchMedia('(max-width:900px)').matches) return;
      takt.push(function () {
        var m = innerHeight / 2;
        sp.forEach(function (s) { var r = g.getBoundingClientRect(); s.style.transform = 'translateY(' + ((r.top + r.height / 2 - m) * +s.dataset.tempo).toFixed(1) + 'px)'; });
      });
    },
    8: function (g) {
      var bue = $('.m8-buehne', g), bild = $('.m8-bild', g), unter = $('.m8-unter', g);
      lade($('.foto', bild));
      if (ruhig) { bild.style.transform = 'none'; unter.classList.add('da'); return; }
      takt.push(function () {
        var r = bue.getBoundingClientRect(), weg = r.height - innerHeight, p = Math.max(0, Math.min(1, -r.top / (weg || 1)));
        var s = .46 + .54 * Math.min(1, p / .75);
        bild.style.transform = 'scale(' + s.toFixed(4) + ')';
        unter.classList.toggle('da', p > .8);
      });
    },
    12: function (g) {
      var stapel = $('.m12-stapel', g), kl = $$('.m12-k', g), sa = $$('.m12-s', g);
      kl.forEach(function (b, i) { b.addEventListener('click', function () { zeige(stapel, i); markiere(kl, i); markiere(sa, i); }); });
    },
    13: function (g) {
      var weg = $('.m13-weg', g), linie = $('.m13-linie i', g), st = $$('.m13-st', g);
      if (ruhig) { linie.style.transform = 'none'; st.forEach(function (s) { s.classList.add('an'); }); return; }
      takt.push(function () {
        var r = weg.getBoundingClientRect(), p = Math.max(0, Math.min(1, (innerHeight * .6 - r.top) / r.height));
        linie.style.transform = 'scaleY(' + p.toFixed(4) + ')';
        st.forEach(function (s) { s.classList.toggle('an', s.getBoundingClientRect().top + 40 < innerHeight * .6); });
      });
    },
    15: function (g) {
      var stapel = $('.m15-stapel', g), z = $$('.m15-z', g);
      z.forEach(function (b, i) {
        function w() { zeige(stapel, i); markiere(z, i); }
        b.addEventListener('mouseenter', w); b.addEventListener('focus', w); b.addEventListener('click', w);
      });
    }
  };
  $$('[data-m]').forEach(function (g) { var f = F[g.dataset.m]; if (f) f(g); });
  lauf();
})();
