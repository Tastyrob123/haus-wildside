/* Wild Side · Feiern, «Die Empore gehört euch.», Fassungen 01–15: die scrollgetriebenen Bewegungen. Nur transform, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:900px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };
  // 0, wenn die Oberkante am unteren Rand steht; 1, wenn die Unterkante oben angekommen ist
  var durch = function (el) { var r = el.getBoundingClientRect(); return kl((H() - r.top) / (H() + r.height)); };

  var g = document.getElementById('tafel'), n = g ? +g.getAttribute('data-e') || 0 : 0;
  if (!n) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var F = {
    // Vier Stunden: die Felder füllen sich nacheinander, solange der Balken durchs untere Drittel zieht
    5: function () {
      var b = $('[data-stunden]', g), f = $$('i', b);
      takt.push(function () {
        if (!sicht(b)) return; var r = b.getBoundingClientRect(), q = ruhig ? 1 : kl((H() * .92 - r.top) / (H() * .5)) * 4;
        f.forEach(function (e, j) { e.style.setProperty('--f', kl(q - j).toFixed(3)); });
      });
    },
    // Das Budget: die Säule füllt sich von unten, voll, wenn der Satz in der Mitte steht
    7: function () {
      var s = $('[data-budget]', g);
      takt.push(function () { if (!sicht(s)) return; var r = s.getBoundingClientRect(), q = ruhig ? 1 : kl((H() * .95 - r.top) / (H() * .5)); s.style.setProperty('--f', q.toFixed(3)); });
    },
    // Drei Schritte: der Scrollweg der Bühne ist in drei Stücke geteilt, je Stück tritt ein Satz hervor; das Bild kommt dabei ganz zur Ruhe
    12: function () {
      var p = $('[data-pin]', g), s = $$('.schritt', g), f = $('.ef', g), alt = -1;
      takt.push(function () {
        if (schmal() || !sicht(p)) return; var r = p.getBoundingClientRect(), q = kl(-r.top / Math.max(1, r.height - H()));
        var i = Math.min(s.length - 1, Math.floor(q * s.length * .999 + (q > 0 ? 0 : 0)));
        if (i !== alt) { alt = i; s.forEach(function (e, j) { e.classList.toggle('jetzt', j === i); e.classList.toggle('vorbei', j < i); }); }
        f.style.setProperty('--s', ruhig ? 1 : (1.08 - .08 * q).toFixed(4));
      });
    },
    // In die Tiefe: das Foto wandert in seinem Rahmen von oben nach unten, solange der Rahmen durchs Bild zieht
    15: function () {
      var t = $('[data-tief]', g);
      takt.push(function () { if (ruhig || !sicht(t)) return; t.style.setProperty('--y', (-18 * (1 - durch(t))).toFixed(2) + '%'); });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
