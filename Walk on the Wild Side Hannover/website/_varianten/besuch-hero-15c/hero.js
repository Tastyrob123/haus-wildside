/* Wild Side · Besuch, Runde 3: Kamerafahrten beim Scrollen (03, 09, 10, 14, 15). Nur transform/opacity, ein Takt. */
(function () {
  'use strict';
  var h = document.querySelector('.by'); if (!h) return;
  var v = +h.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  if (ruhig) return;
  var klemm = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var weich = function (a, b, x) { x = klemm((x - a) / (b - a)); return x * x * (3 - 2 * x); };
  var kino = function (x) { return 1 - Math.pow(1 - klemm(x), 3); };     // schnell los, auf drei Vierteln langsam
  var beimScrollen = function (fn) {
    var tick = false;
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; fn(); }); } }, { passive: true });
    addEventListener('resize', fn); fn();
  };
  var buehne = h.querySelector('.by-buehne');
  var fortschritt = function () { var r = h.getBoundingClientRect(); return klemm(-r.top / Math.max(1, h.offsetHeight - buehne.offsetHeight)); };

  /* 03 · vom Tresen hinauf in die Decke */
  if (v === 3) {
    var hoch = h.querySelector('.by03-hoch');
    beimScrollen(function () {
      var weg = hoch.offsetHeight - buehne.offsetHeight, p = kino(fortschritt() * 1.1);
      hoch.style.transform = 'translate3d(0,' + (-weg * (1 - p)).toFixed(1) + 'px,0)';
    });
  }

  /* 09 · der Abend: jedes Bild mit eigener langsamer Fahrt */
  if (v === 9) {
    var fotos = [].slice.call(h.querySelectorAll('.by09-f')), alt = -1;
    beimScrollen(function () {
      var p = fortschritt() * fotos.length * .999, j = Math.min(fotos.length - 1, Math.floor(p)), t = p - j;
      if (j !== alt) { fotos.forEach(function (f, k) { f.classList.toggle('an', k === j); }); alt = j; }
      fotos[j].style.transform = 'scale(' + (1.14 - .14 * kino(t)).toFixed(4) + ')';
    });
  }

  /* 10 · durch die Scheibe */
  if (v === 10) {
    var aus = h.querySelector('.by10-aussen'), inn = h.querySelector('.by10-innen');
    beimScrollen(function () {
      var p = fortschritt();
      aus.style.transform = 'scale(' + (1 + 3.2 * p * p).toFixed(3) + ')';
      aus.style.opacity = (1 - weich(.5, .86, p)).toFixed(3);
      inn.style.transform = 'scale(' + (1.25 - .25 * kino((p - .35) / .65)).toFixed(3) + ')';
      inn.style.opacity = weich(.42, .82, p).toFixed(3);
    });
  }

  /* 14 · die Säulen gleiten unterschiedlich schnell nach oben */
  if (v === 14) {
    var s = [].slice.call(h.querySelectorAll('.by14-s'));
    beimScrollen(function () {
      var y = Math.min(scrollY, h.offsetHeight);
      s.forEach(function (el) { var t = +el.dataset.t; el.style.transform = 'translate3d(0,' + (-(t * 260) - y * t).toFixed(1) + 'px,0)'; });
    });
  }

  /* 15 · hinein in das mittlere Bild */
  if (v === 15) {
    var w = h.querySelector('.by15-wand');
    beimScrollen(function () { w.style.transform = 'scale(' + (1 + 1.3 * kino(fortschritt() * 1.15)).toFixed(4) + ')'; });
  }
})();
