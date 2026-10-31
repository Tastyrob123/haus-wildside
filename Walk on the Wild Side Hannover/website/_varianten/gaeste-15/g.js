/* Wild Side · Programm, «Jemand anderes am Shaker.», 15 Darstellungen: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
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
  $$('.vauf, .s15-p', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  var schalte = function (liste, a) { liste.forEach(function (e, j) { e.classList.toggle('an', j === a); }); };
  var naechster = function (liste) { var best = 0, d = 9; liste.forEach(function (e, j) { var m = Math.abs(mitte(e)); if (m < d) { d = m; best = j; } }); return best; };

  var F = {
    // Verstreut: jedes Bild zieht mit eigener Geschwindigkeit
    3: function () {
      var p = $$('.s3-p', g), f = $('.s3-feld', g);
      takt.push(function () { if (ruhig || schmal() || !sicht(f)) return; var m = mitte(f) * H(); p.forEach(function (e) { e.style.transform = 'translate3d(0,' + (m * +e.dataset.v).toFixed(1) + 'px,0)'; }); });
    },
    // Einer nach dem anderen: je Scrollschritt schiebt sich das nächste Bild darüber
    5: function () {
      var p0 = $('[data-pin]', g), b = $$('.s5-b', g), t = $$('.s5-t', g), z = $$('.s5-zaehl i', g), alt = -1;
      takt.push(function () {
        if (!sicht(p0)) return; var a = Math.min(b.length - 1, Math.floor(pin(p0) * b.length)); if (a === alt) return; alt = a;
        b.forEach(function (e, j) { e.classList.toggle('da', j <= a); }); schalte(t, a); z.forEach(function (e, j) { e.classList.toggle('an', j <= a); });
      });
    },
    // Blick wandert: wer der Bildmitte am nächsten ist, tritt vor
    7: function () {
      var p = $$('.s7-p', g), r = $('[data-blick]', g), alt = -1;
      takt.push(function () {
        if (!sicht(r)) return; var a;
        if (schmal()) a = naechster(p);
        else { var q = kl((H() * .75 - r.getBoundingClientRect().top) / (H() * .9)); a = Math.min(p.length - 1, Math.floor(q * p.length)); }
        if (a !== alt) { alt = a; schalte(p, a); }
      });
    },
    // Namen gross: Zeigen öffnet das Bild wie ein Rollo von unten
    10: function () {
      var nm = $$('.s10-n', g), b = $$('.s10-b', g), jetzt = 0;
      nm.forEach(function (x, j) {
        var w = function () {
          if (j === jetzt) return; schalte(nm, j);
          b.forEach(function (e) { e.classList.remove('war'); }); b[jetzt].classList.add('war'); b[jetzt].classList.remove('an');
          b[j].classList.add('an'); jetzt = j;
        };
        x.addEventListener('mouseenter', w); x.addEventListener('click', w);
      });
    },
    // Bild bleibt stehen: wer rechts in der Mitte steht, dessen Bild steht links
    11: function () {
      var t = $$('.s11-t', g), b = $$('.s11-b', g), r = $('[data-steh]', g), alt = 0; t[0].classList.add('an');
      takt.push(function () { if (!sicht(r)) return; var a = naechster(t); if (a !== alt) { alt = a; schalte(t, a); schalte(b, a); } });
    },
    // Wand im Versatz: die Spalten gleiten verschieden weit
    13: function () {
      var p = $$('.s13-p', g), w = $('[data-versatz]', g);
      takt.push(function () { if (ruhig || schmal() || !sicht(w)) return; var m = Math.max(-.6, Math.min(.6, mitte(w))); p.forEach(function (e) { e.style.transform = 'translate3d(0,' + (m * H() * +e.dataset.v).toFixed(1) + 'px,0)'; }); });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
