/* Wild Side · 15 Fassungen «Was magst du?»: die eigene Bewegung jeder Fassung. Die Wahl selbst bleibt bei wild.js (.wahl-Knöpfe, .ge-satz, .ge-glas);
   hier hört jede Fassung auf dieselben Knöpfe und zeigt die Antwort auf ihre Art. Nur transform und opacity. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var fein = matchMedia('(pointer:fine)').matches && !document.documentElement.classList.contains('ruhig');
  function lade(f) { var img = f && f.querySelector('img[data-srcset]'); if (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); } }
  function nochmal(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }
  /* Ein Stapel echter Fotos: das neue kommt von unten, das alte bleibt darunter liegen (wie das Glas der Seite) */
  function tausche(stapel, k) {
    var neu = $('[data-k="' + k + '"]', stapel), alt = $('.foto.an', stapel);
    if (!neu || neu === alt) return;
    $$('.foto.war', stapel).forEach(function (f) { f.classList.remove('war'); });
    if (alt) { alt.classList.remove('an'); alt.classList.add('war'); }
    lade(neu); neu.classList.add('an');
  }

  var F = {
    1: function (api) {
      var antw = $('.v1-antw', api.g), satz = $('.ge-satz', api.g), t = 0;
      api.on.push(function (a, b) {
        if (!b) return;
        antw.classList.add('tippt'); clearTimeout(t);
        t = setTimeout(function () { antw.classList.remove('tippt'); nochmal(satz, 'wechsel'); satz.classList.remove('wechsel'); }, 750);
      });
    },
    2: function (api) {
      var worte = $$('.v2-wort', api.g);
      worte.forEach(function (w) {
        w.addEventListener('click', function () {
          var knoepfe = $$('.wahl[data-frage="' + w.dataset.ziel + '"] button', api.g);
          var i = knoepfe.map(function (x) { return x.dataset.w; }).indexOf(api.wahl[w.dataset.ziel]);
          knoepfe[(i + 1) % knoepfe.length].click();
        });
      });
      api.on.push(function () {
        worte.forEach(function (w) {
          var knoepfe = $$('.wahl[data-frage="' + w.dataset.ziel + '"] button', api.g);
          var i = knoepfe.map(function (x) { return x.dataset.w; }).indexOf(api.wahl[w.dataset.ziel]);
          $('.v2-roll', w).style.transform = 'translateY(' + (-i * 1.18) + 'em)';
        });
      });
    },
    3: function (api) {
      function setze() {
        $$('.v3-liste', api.g).forEach(function (l) {
          var b = $('button.an', l), s = $('.v3-strich', l);
          if (b) s.style.transform = 'translateY(' + b.offsetTop + 'px) scaleY(' + (b.offsetHeight / 100) + ')';
        });
      }
      api.on.push(setze); addEventListener('resize', setze); addEventListener('load', setze);
    },
    4: function (api) {
      var dreh = $('.v4-dreh', api.g), vorn = $('.vorn', api.g), hinten = $('.hinten', api.g), seite = 0, jetzt = null;
      function zeige(f, k) { $$('.foto', f).forEach(function (x) { x.classList.toggle('an', x.dataset.k === k); if (x.dataset.k === k) lade(x); }); }
      api.on.push(function (a) {
        if (jetzt === null) { zeige(vorn, a.bild); jetzt = a.bild; return; }
        if (a.bild === jetzt) return;
        jetzt = a.bild; seite = 1 - seite;
        zeige(seite ? hinten : vorn, a.bild);
        dreh.classList.toggle('um', !!seite);
      });
    },
    6: function (api) {
      var reihe = $('.v6-reihe', api.g);
      api.on.push(function (a) { $$('.v6-g', reihe).forEach(function (f) { f.classList.toggle('an', f.dataset.k === a.bild); }); });
    },
    7: function (api) {
      var satz = $('.v7-satz', api.g);
      api.on.push(function (a) {
        var n = 0;
        satz.innerHTML = a.satz.split('|').map(function (z) {
          return '<span class="v7-z">' + z.split(' ').map(function (w) { return '<span class="v7-w" style="--w:' + (n++) + '">' + w + '</span>'; }).join(' ') + '</span>';
        }).join('');
        nochmal(satz, 'los');
      });
    },
    8: function (api) {
      $$('.v8-w', api.g).forEach(function (w) {
        var rolle = $('.v8-rolle', w);
        $$('.v8-pf', w).forEach(function (p) {
          p.addEventListener('click', function () {
            var k = $$('button', rolle), i = k.indexOf($('button.an', rolle)), z = Math.max(0, Math.min(k.length - 1, i + +p.dataset.d));
            if (z !== i) k[z].click();
          });
        });
      });
      api.on.push(function () {
        $$('.v8-rolle', api.g).forEach(function (r) {
          var k = $$('button', r), i = k.indexOf($('button.an', r));
          r.style.transform = 'translateY(calc(var(--zh) * ' + (1 - i) + '))';
          k.forEach(function (b, j) { b.classList.toggle('nah', Math.abs(j - i) === 1); });
          var w = r.closest('.v8-w'); $$('.v8-pf', w).forEach(function (p) { p.disabled = (+p.dataset.d < 0 && i === 0) || (+p.dataset.d > 0 && i === k.length - 1); });
        });
      });
    },
    9: function (api) {
      var band = $('.v9-band', api.g), punkte = $$('.v9-punkte i', api.g), folien = $$('.v9-folie', api.g), t = 0;
      function geh(s) {
        band.style.transform = 'translateY(' + (-s * 25) + '%)';
        punkte.forEach(function (p, j) { p.classList.toggle('an', j <= s); });
        folien.forEach(function (f, j) { f.setAttribute('aria-hidden', j === s ? 'false' : 'true'); f.inert = j !== s; });
        if (s === 3) lade($('.v9-glas .foto.an', api.g));
      }
      api.on.push(function (a, b) {
        if (!b) return;
        var s = folien.indexOf(b.closest('.v9-folie'));
        clearTimeout(t); t = setTimeout(function () { geh(s + 1); }, 420);
      });
      $('.v9-nochmal', api.g).addEventListener('click', function () { geh(0); });
      geh(0);
    },
    12: function (api) {
      var stapel = $('.v12-stapel', api.g), glasZeit = false, jetzt = 'momo-giesst';
      function zeige() { var k = glasZeit ? api.finde().bild : 'momo-giesst'; if (k !== jetzt) { tausche(stapel, k); jetzt = k; } }
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (es) {
          es.forEach(function (e) { if (e.isIntersecting) { glasZeit = +e.target.dataset.schritt >= 3; zeige(); } });
        }, { rootMargin: '-45% 0px -45% 0px' });
        $$('.v12-block', api.g).forEach(function (b) { io.observe(b); });
      }
      api.on.push(function () { zeige(); });
    },
    13: function (api) {
      var box = $('.v13-glasbox', api.g);
      api.on.push(function (a, b) { if (b) nochmal(box, 'neu'); });
    },
    14: function (api) {
      api.on.push(function (a, b) {
        if (!b) return;
        var st = b.closest('.v14-st'); if (st) nochmal(st, 'tippt');
        var ziel = $('.v14-ziel', api.g); nochmal(ziel, 'tippt');
      });
    },
    15: function (api) {
      var m = $('.v15-m', api.g), kipp = $('.v15-kipp', api.g), stapel = $('.v15-stapel', api.g), jetzt = null, rx = 0, ry = 0, tick = false;
      api.on.push(function (a) {
        if (a.bild === jetzt) return; jetzt = a.bild;
        var neu = $('[data-k="' + a.bild + '"]', stapel);
        $$('.foto', stapel).forEach(function (f) { f.classList.remove('an'); }); lade(neu); nochmal(neu, 'an');
      });
      if (!fein) return;
      m.addEventListener('pointermove', function (e) {
        var r = m.getBoundingClientRect();
        ry = ((e.clientX - r.left) / r.width - .5) * 14; rx = -((e.clientY - r.top) / r.height - .5) * 10;
        if (!tick) { tick = true; requestAnimationFrame(function () { kipp.style.transform = 'rotateX(' + rx.toFixed(2) + 'deg) rotateY(' + ry.toFixed(2) + 'deg)'; tick = false; }); }
      });
      m.addEventListener('pointerleave', function () { kipp.style.transform = ''; });
    }
  };

  $$('[data-gespraech][data-v]').forEach(function (g) {
    var A = JSON.parse(g.dataset.gespraech), wahl = {};
    $$('.wahl', g).forEach(function (w) { var b = $('button.an', w) || $('button', w); if (b) wahl[w.dataset.frage] = b.dataset.w; });
    function finde() {
      for (var i = 0; i < A.length; i++) { var a = A[i], ok = true; for (var k in a.wenn) if (a.wenn[k] !== wahl[k]) ok = false; if (ok) return a; }
      return A[A.length - 1];
    }
    var api = { g: g, wahl: wahl, finde: finde, on: [] };
    $$('.wahl button', g).forEach(function (b) {
      b.addEventListener('click', function () { wahl[b.closest('.wahl').dataset.frage] = b.dataset.w; var a = finde(); api.on.forEach(function (f) { f(a, b); }); });
    });
    var f = F[g.dataset.v]; if (f) f(api);
    var a0 = finde(); api.on.forEach(function (fn) { fn(a0, null); });
  });
})();
