/* Wild Side · Drinks, ein Faden: setzt --p je Schritt (0 → 1, während er ins Bild kommt), Wörter, Licht und die stehende Wand. Ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);

  var g = $('section[data-g]'); if (!g) return;
  var nr = +g.dataset.g;

  // Jeder Schritt: --p läuft von 0 (Oberkante bei 95 % der Höhe) bis 1 (Oberkante bei 30 %).
  $$('[data-p]', g).forEach(function (s) {
    var w = $$('.ww', s), alt = -1;
    takt.push(function () {
      var p = 1;
      if (!ruhig && !schmal()) { var r = s.getBoundingClientRect(); if (r.top > 1.4 * H() || r.bottom < -.4 * H()) return; p = kl((.95 * H() - r.top) / (.65 * H())); }
      var q = Math.round(p * 1000) / 1000; if (q === alt) return; alt = q;
      s.style.setProperty('--p', q);
      if (w.length) { var n = Math.ceil(kl(p * 1.15) * w.length); w.forEach(function (x, i) { x.classList.toggle('an', i < n); }); }
    });
  });

  // 01: das Licht, Nacht → Bernstein → Creme
  if (nr === 1) {
    var a = $('.t1-a', g), c = $('.t1-c', g), sa = $('[data-bga]', g), sc = $('[data-bgc]', g);
    takt.push(function () {
      var ra = sa.getBoundingClientRect(), rc = sc.getBoundingClientRect();
      var pa = kl((.9 * H() - ra.top) / (.55 * H())), pc = kl((1.05 * H() - rc.top) / (.5 * H()));
      a.style.opacity = (pa * (1 - pc)).toFixed(3); c.style.opacity = pc.toFixed(3);
    });
  }

  // 03: die Wand füllt sich, ein Schritt je Abschnitt der Bühne
  if (nr === 3) {
    var pin = $('[data-pin]', g), tx = $$('.t3-text', g), ka = $$('.t3-kachel', g), st = $$('.t3-striche i', g), alt3 = 0;
    takt.push(function () {
      if (schmal()) return;
      var r = pin.getBoundingClientRect(), p = kl(-r.top / Math.max(1, r.height - H()));
      var j = Math.min(tx.length - 1, Math.floor(p * tx.length * .999 + (ruhig ? 0 : 0)));
      if (j === alt3) return; alt3 = j;
      tx.forEach(function (t, i) { t.classList.toggle('an', i === j); t.classList.toggle('war', i < j); });
      ka.forEach(function (k, i) { k.classList.toggle('da', i <= j); });
      st.forEach(function (s, i) { s.classList.toggle('an', i <= j); });
    });
  }


  // Stehende Bühnen (09 bis 15, 17): jedes [data-s] bekommt --d (Abstand zum aktuellen Schritt), --a (Betrag) und an / war
  $$('[data-pin]', g).forEach(function (pin) {
    var el = $$('[data-s]', pin); if (!el.length) return;
    var n = parseFloat(pin.style.getPropertyValue('--n')) || el.length, js = el.map(function (e) { return +e.style.getPropertyValue('--j') || 0; });
    var zug = $('.qb-zug', pin), breite = 0, lagen = $$('.bb-lage', pin), blickAlt = -1;
    function mass() { if (!zug) return; if (schmal()) { pin.style.height = ''; return; } breite = zug.scrollWidth - innerWidth; pin.style.height = (breite + H() * 1.1) + 'px'; }
    if (zug) { addEventListener('resize', mass); addEventListener('load', mass); mass(); }
    takt.push(function () {
      if (schmal()) return;
      var r = pin.getBoundingClientRect(); if (r.bottom < -H() || r.top > 2 * H()) return;
      var pp = kl(-r.top / Math.max(1, r.height - H())), pos = pp * (n - 1);
      if (zug) zug.style.transform = 'translate3d(' + (-pp * breite).toFixed(1) + 'px,0,0)';
      el.forEach(function (e, i) {
        var d = Math.max(-3, Math.min(3, pos - js[i]));
        e.style.setProperty('--d', d.toFixed(4)); e.style.setProperty('--a', Math.min(1, Math.abs(d)).toFixed(4));
        e.classList.toggle('an', Math.abs(d) < .5); e.classList.toggle('war', d >= .5);
      });
      if (lagen.length) {
        var k = Math.round(pos); if (k !== blickAlt) {
          blickAlt = k; var t = el.filter(function (e, i) { return js[i] === k && e.dataset.blick; })[0];
          if (t) { var b = t.dataset.blick.split(','); lagen.forEach(function (l, i) { var an = i === +b[0]; l.classList.toggle('an', an); if (an) { l.style.setProperty('--sc', b[1]); l.style.setProperty('--ox', b[2] + '%'); l.style.setProperty('--oy', b[3] + '%'); } }); }
        }
      }
    });
  });

  // 05 Pegel und 18 Kopfzeile: wo man gerade ist
  var schritte = $$('.b-weg > .b, .b-teil > .b', g), namen = ['Das Gespräch', 'Der Geschmack', 'Das Glas', 'Was hinein soll', 'Wie Momo arbeitet', 'Milk Washing', 'Fat Washing', 'Enzyme'];
  var pegel = $('.b-pegel', g), roehre = pegel && $('[data-pegel]', pegel), weg = $('.b-weg', g), kopfz = $('[data-kopf]', g), tech = $('#technik', g), merk = '';
  if (pegel || kopfz) takt.push(function () {
    if (pegel) {
      var r = weg.getBoundingClientRect(); pegel.style.setProperty('--pg', kl((H() * .5 - r.top) / r.height).toFixed(4));
      var k = 0; schritte.forEach(function (s, i) { if (s.getBoundingClientRect().top < H() * .5) k = i; });
      if (roehre.textContent !== namen[k]) roehre.textContent = namen[k];
    }
    if (kopfz) { var t = tech.getBoundingClientRect().top < H() * .4 ? 'Wie Momo arbeitet · Drei Techniken' : 'Das Gespräch · An der Theke'; if (t !== merk) { merk = t; kopfz.textContent = t; } }
  });

  addEventListener('load', function () { $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); }); lauf(); });
  lauf();
})();
