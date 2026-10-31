/* Wild Side · Feiern, «So geht es»: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt, nur solange der Abschnitt im Bild ist. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var sek = $('section.ax'); if (!sek) return;
  var v = +sek.dataset.v;
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var IO = 'IntersectionObserver' in window;
  var clamp = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  function lade(f) { var img = f && f.querySelector('img[data-srcset]'); if (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); } }
  /* 0, wenn die Oberkante bei a × Höhe steht, 1 bei b × Höhe */
  function p(el, a, b) { var r = el.getBoundingClientRect(), h = innerHeight; return clamp((a * h - r.top) / ((a - b) * h)); }

  /* Auftritt: .va bekommt .ok, sobald es im Bild ist */
  var va = $$('.va', sek);
  if (ruhig || !IO) va.forEach(function (el) { el.classList.add('ok'); });
  else {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -14% 0px' });
    va.forEach(function (el) { io.observe(el); });
  }

  /* Ein Takt für alles, was am Scrollen hängt */
  var takt = [], sicht = false, tick = false;
  function lauf() { tick = false; if (!sicht) return; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', function () { sicht = true; lauf(); });
  if (IO) new IntersectionObserver(function (es) { sicht = es[0].isIntersecting; if (sicht) lauf(); }, { rootMargin: '10% 0px 10% 0px' }).observe(sek);
  else sicht = true;

  function stapel(bilder, j) { bilder.forEach(function (f, i) { if (i === j) { lade(f); f.classList.add('an'); } else f.classList.remove('an'); }); }

  var F = {
    /* 02: der Block in der Mitte des Fensters bestimmt das Bild; frühere bleiben liegen, spätere warten unten */
    2: function () {
      var bl = $$('.a2-bl', sek), f = $$('.a2-f', sek);
      function geh(j) {
        bl.forEach(function (b, i) { b.classList.toggle('an', i === j); });
        f.forEach(function (x, i) { x.classList.toggle('an', i === j); x.classList.toggle('war', i < j); if (i <= j) lade(x); });
      }
      if (!IO) return geh(0);
      var o = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) geh(+e.target.dataset.j); }); }, { rootMargin: '-45% 0px -45% 0px' });
      bl.forEach(function (b) { o.observe(b); });
    },
    /* 03: die Linie folgt dem Scrollen, jede Station leuchtet, sobald die Linie sie erreicht */
    3: function () {
      var weg = $('.a3-weg', sek), li = $('.a3-linie', sek), st = $$('.a3-st', sek), pk = $('.a3-p', sek);
      function lage() { li.style.setProperty('--lt', (pk.offsetTop + 6) + 'px'); }
      lage(); addEventListener('resize', lage);
      if (ruhig) { li.style.setProperty('--p', 1); st.forEach(function (s) { s.classList.add('an'); }); return; }
      takt.push(function () {
        var q = p(weg, .85, .25);
        li.style.setProperty('--p', q.toFixed(4));
        st.forEach(function (s, i) { s.classList.toggle('an', q >= i / 4 + .02 || schmal()); });
      });
    },
    /* 05: Wort antippen oder darüberfahren zeigt Bild und Satz */
    5: function () {
      var w = $$('.a5-w', sek), f = $$('.a5-f', sek), s = $$('.a5-s', sek);
      function geh(j) { w.forEach(function (x, i) { x.classList.toggle('an', i === j); }); s.forEach(function (x, i) { x.classList.toggle('an', i === j); }); stapel(f, j); }
      w.forEach(function (x, i) { ['mouseenter', 'focus', 'click'].forEach(function (ev) { x.addEventListener(ev, function () { geh(i); }); }); });
      f.forEach(lade);
    },
    /* 07: die Bildspalten laufen gegeneinander */
    7: function () {
      var sp = $$('.a7-sp', sek), g = $('.a7-g', sek);
      if (ruhig) return;
      takt.push(function () {
        var q = p(g, 1, -.2) - .5, m = schmal() ? 0 : 1;
        sp.forEach(function (x) { x.style.transform = 'translate3d(0,' + (q * -170 * +x.dataset.t * m).toFixed(1) + 'px,0)'; });
      });
    },
    /* 09: Stufen legen sich zu einer Reihe */
    9: function () {
      var pl = $$('.a9-pl', sek), r = $('.a9-reihe', sek);
      if (ruhig) return;
      takt.push(function () {
        var q = p(r, .95, .35), m = schmal() ? 0 : 1;
        pl.forEach(function (x, i) { x.style.setProperty('--y', ((1 - q) * i * 70 * m).toFixed(1) + 'px'); });
      });
    },
    /* 10: die Abzüge richten sich gerade, wenn der Tisch zur Hälfte oben ist */
    10: function () {
      var ab = $$('.a10-ab', sek), t = $('.a10-tisch', sek);
      if (ruhig) return ab.forEach(function (a) { a.classList.add('gerade'); });
      takt.push(function () { var q = p(t, .7, .3); ab.forEach(function (a, i) { a.classList.toggle('gerade', q > .25 + i * .2); }); });
    },
    /* 11: Pfeile blättern das Band */
    11: function () {
      var band = $('.a11-band', sek), pf = $$('.a11-pf button', sek);
      pf.forEach(function (b) { b.addEventListener('click', function () { var k = $('.a11-k', band); band.scrollBy({ left: +b.dataset.d * (k.offsetWidth + 18), behavior: ruhig ? 'auto' : 'smooth' }); }); });
      function knoepfe() { pf[0].disabled = band.scrollLeft < 8; pf[1].disabled = band.scrollLeft > band.scrollWidth - band.clientWidth - 8; }
      band.addEventListener('scroll', knoepfe, { passive: true }); knoepfe();
    },
    /* 12: läuft von selbst alle 5 Sekunden weiter, solange der Abschnitt im Bild ist; Maus aufs Bild hält an */
    12: function () {
      var g = $('.a12-g', sek), f = $$('.a12-f', sek), st = $$('.a12-striche button', sek), x = $$('.a12-x', sek), j = 0, t = 0, halt = false, im = false;
      function geh(z) {
        j = (z + st.length) % st.length; stapel(f, j); lade(f[(j + 1) % f.length]);
        x.forEach(function (e, i) { e.classList.toggle('an', i === j); });
        st.forEach(function (b, i) { b.classList.toggle('war', i < j); b.classList.remove('an'); });
        void st[j].offsetWidth; st[j].classList.add('an');
        clearTimeout(t); if (!halt && im && !ruhig) t = setTimeout(function () { geh(j + 1); }, 5000);
      }
      st.forEach(function (b, i) { b.addEventListener('click', function () { geh(i); }); });
      var bild = $('.a12-st', sek);
      bild.addEventListener('mouseenter', function () { halt = true; clearTimeout(t); g.classList.add('halt'); });
      bild.addEventListener('mouseleave', function () { halt = false; g.classList.remove('halt'); geh(j); });
      if (IO) new IntersectionObserver(function (es) { var war = im; im = es[0].isIntersecting; if (im && !war) geh(j); if (!im) clearTimeout(t); }, { threshold: .35 }).observe(g);
      else { im = true; geh(0); }
    },
    /* 13: die vier Streifen kommen verschieden hoch an und setzen sich zusammen */
    13: function () {
      var sp = $$('.a13-sp', sek), r = $('.a13-reihe', sek), H = [150, 60, 210, 110];
      if (ruhig) return;
      takt.push(function () {
        var q = p(r, 1, .3), m = schmal() ? 0 : 1, e = 1 - Math.pow(1 - q, 3);
        sp.forEach(function (x, i) { x.querySelector('.a13-b').style.setProperty('--y', ((1 - e) * H[i] * m).toFixed(1) + 'px'); x.style.setProperty('--o', m ? clamp(e * 1.6 - .3).toFixed(3) : 1); });
      });
    },
    /* 15: die untere Platte tritt zurück, sobald die nächste über ihr ankommt */
    15: function () {
      var pl = $$('.a15-pl', sek);
      if (ruhig) return;
      takt.push(function () {
        pl.forEach(function (x, i) {
          var in_ = x.querySelector('.a15-in'), n = pl[i + 1];
          if (!n || schmal()) { in_.style.setProperty('--sk', 1); in_.style.setProperty('--o', 1); return; }
          var rn = n.getBoundingClientRect(), rx = x.getBoundingClientRect(), q = clamp(1 - (rn.top - rx.top) / rx.height);
          in_.style.setProperty('--sk', (1 - q * .06).toFixed(4)); in_.style.setProperty('--o', (1 - q * .45).toFixed(3));
        });
      });
    }
  };
  if (F[v]) F[v]();
  lauf();
})();
