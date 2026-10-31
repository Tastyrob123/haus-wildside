/* Wild Side · Programm, «Die Woche», 20 Darstellungen: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var weich = function (t) { return t * t * (3 - 2 * t); };
  var H = function () { return innerHeight; };
  // Fortschritt, während die Oberkante des Elements von a*Höhe nach b*Höhe wandert
  var weg = function (el, a, b) { var r = el.getBoundingClientRect(); return kl((a * H() - r.top) / ((a - b) * H())); };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };

  var g = document.getElementById('woche'), n = g ? +g.getAttribute('data-w') || 0 : 0;
  if (!n) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  // Einmalige Auftritte (.vauf): sobald gut im Bild
  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -18% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('da'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  var setz = function (el, p) { el.style.setProperty('--p', p.toFixed(4)); };

  var F = {
    1: function () { $$('[data-a]', g).forEach(function (r) { var t = $$('.a-teil,.a-spur em', r); takt.push(function () { if (!sicht(r)) return; var p = ruhig ? 1 : weich(weg(r, .92, .5)); t.forEach(function (e) { setz(e, p); }); }); }); },
    4: function () {
      var p0 = $('[data-pin]', g), pl = $$('.s-platte', g);
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var p = pin(p0) * 2.3;   // zwei Wechsel, am Ende kurz stehen
        pl.forEach(function (e, j) {
          var ein = j === 0 ? 1 : weich(kl(p - (j - 1))), drauf = j < 2 ? weich(kl(p - j)) : 0;
          e.style.transform = 'translate3d(0,' + ((1 - ein) * 108).toFixed(2) + '%,0) scale(' + (1 - drauf * .06).toFixed(4) + ')';
          e.style.opacity = (1 - drauf * .55).toFixed(3);
        });
      });
    },
    5: function () {
      var p0 = $('[data-pin]', g), l = $('.f-0', g), r = $('.f-2', g);
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var p = ruhig ? 1 : weich(kl(pin(p0) * 1.6 - .1));
        // wie ein echtes Faltblatt: der obere Flügel (links) geht zuerst auf, dann der darunter
        l.style.transform = 'translateZ(2px) rotateY(' + ((1 - weich(kl(p / .55))) * 178).toFixed(2) + 'deg)';
        r.style.transform = 'translateZ(1px) rotateY(' + ((1 - weich(kl((p - .4) / .6))) * -176).toFixed(2) + 'deg)';
      });
    },
    7: function () { $$('[data-o]', g).forEach(function (f) { var b = $('.o-bogen', f); takt.push(function () { if (!sicht(f)) return; setz(b, ruhig ? 1 : weich(weg(f, .85, .35))); }); }); },
    8: function () {
      var b = $$('.w8-b', g), t = $$('.w8-t', g);
      takt.push(function () { if (schmal()) return; for (var j = 1; j < b.length; j++) setz(b[j], ruhig ? (weg(t[j], .5, .5001) ) : weich(weg(t[j], .95, .45))); });
    },
    11: function () {
      var p0 = $('[data-pin]', g), bl = $$('.k-blatt', g);
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var p = pin(p0) * 2.4;
        bl.forEach(function (e, j) {
          if (j === bl.length - 1) return; var w = weich(kl(p - j - .15));
          e.style.transform = 'rotateX(' + (w * 105).toFixed(2) + 'deg)'; e.style.opacity = (1 - kl((w - .55) / .4)).toFixed(3);
        });
      });
    },
    13: function () { $$('[data-li]', g).forEach(function (z) { var e = $$('.li-tag,.wf', z); takt.push(function () { if (!sicht(z)) return; var p = ruhig ? 1 : weich(weg(z, .95, .45)); e.forEach(function (x) { setz(x, p); }); }); }); },
    16: function () { $$('[data-r]', g).forEach(function (s, j) { var l = $('.r-laden', s); takt.push(function () { if (!sicht(s)) return; setz(l, ruhig ? 1 : weich(kl(weg(s, .9, .25) * 1.25 - j * .12))); }); }); },
    17: function () {
      var fl = $('[data-fl]', g), l = $('.fl-0', g), r = $('.fl-2', g);
      takt.push(function () { if (schmal() || !sicht(fl)) return; var p = ruhig ? 1 : weich(weg(fl, .95, .3)); l.style.transform = 'rotateY(' + ((1 - p) * 82).toFixed(2) + 'deg)'; r.style.transform = 'rotateY(' + ((1 - p) * -82).toFixed(2) + 'deg)'; });
    },
    18: function () {
      $$('[data-d]', g).forEach(function (d) {
        var v = +d.getAttribute('data-d'), im = $('.wf img', d);
        takt.push(function () {
          if (schmal() || ruhig || !sicht(d)) return; var r = d.getBoundingClientRect(), m = (r.top + r.height / 2 - H() / 2) / H();
          d.style.transform = 'translate3d(0,' + (m * v * 120).toFixed(1) + 'px,0)'; im.style.transform = 'translate3d(0,' + (m * -8).toFixed(2) + '%,0)';
        });
      });
    },
    19: function () { $$('[data-sz]', g).forEach(function (s) { var b = $('.sz-bild img', s); takt.push(function () { if (!sicht(s)) return; setz(b, ruhig ? 1 : weich(weg(s, 1, .05))); }); }); },
    20: function () {
      var p0 = $('[data-pin]', g), ra = $('.g-rahmen', g), f = $$('.g-feld', g), s = $$('.g-satz', g), alt = -1;
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var p = pin(p0) * 2.6, x = 0;
        x = weich(kl(p - .2)) + weich(kl(p - 1.3));   // zwei Schritte mit Halt dazwischen
        ra.style.setProperty('--x', x.toFixed(4));
        var a = Math.round(x); if (a !== alt) { alt = a; f.forEach(function (e, j) { e.classList.toggle('an', j === a); }); s.forEach(function (e, j) { e.classList.toggle('an', j === a); }); }
      });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
