/* Walk on the Wild Side · Bewegung der Fassungen «Im selben Haus» (05, 07, 08, 13, 14). Nur transform und opacity, ein Takt. */
(function () {
  'use strict';
  var s = document.getElementById('imhaus');
  if (!s) return;
  var ruhig = document.documentElement.classList.contains('ruhig');
  var fein = matchMedia('(hover:hover) and (pointer:fine)').matches;
  var schmal = matchMedia('(max-width:760px)').matches;
  function hat(c) { return s.classList.contains(c); }
  function qa(q) { return [].slice.call(s.querySelectorAll(q)); }
  function sichtbar() { var r = s.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }
  function scrollTakt(f) {
    var tick = false;
    function los() { tick = false; f(s.getBoundingClientRect()); }
    addEventListener('scroll', function () { if (!tick && sichtbar()) { tick = true; requestAnimationFrame(los); } }, { passive: true });
    addEventListener('resize', los); los();
  }

  /* 05: Zeile zeigen tauscht das Bild; ohne Maus wechselt es von selbst */
  if (hat('v05')) {
    var zeilen = qa('.ih-l'), bilder = qa('.ih-gross .ih-f'), jetzt = 0, maus = 0;
    function zeig(i) { jetzt = i; zeilen.forEach(function (z, j) { z.classList.toggle('an', j === i); }); bilder.forEach(function (b, j) { b.classList.toggle('an', j === i); }); }
    zeilen.forEach(function (z, i) { z.addEventListener('mouseenter', function () { maus = Date.now(); zeig(i); }); z.addEventListener('focus', function () { zeig(i); }); });
    if (!ruhig) setInterval(function () { if (sichtbar() && Date.now() - maus > 5000) zeig((jetzt + 1) % zeilen.length); }, 3800);
  }

  /* 07: beim Scrollen seitlich vorbei */
  if (hat('v07') && !ruhig && !schmal) {
    var quer = s.querySelector('.ih-quer'), spur = s.querySelector('.ih-spur');
    var tick = false;
    function rechnen() {
      tick = false;
      var r = quer.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
      spur.style.setProperty('--x', (-p * Math.max(0, spur.scrollWidth - innerWidth)).toFixed(1) + 'px');
    }
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }, { passive: true });
    rechnen();
  }

  /* 08: die mittlere Spalte läuft gegen die äusseren */
  if (hat('v08') && !ruhig && !schmal) {
    var ks = qa('.ih-k');
    scrollTakt(function (r) {
      var p = (innerHeight - r.top) / (innerHeight + r.height) - .5;
      ks.forEach(function (k, i) { k.style.setProperty('--y', ((i === 1 ? 1 : -1) * p * 140).toFixed(1) + 'px'); });
    });
  }

  /* 13: drei Tiefen folgen der Maus */
  if (hat('v13') && fein && !ruhig) {
    var es = qa('.ih-e'), mx = 0, my = 0;
    s.addEventListener('mousemove', function (e) { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; });
    (function lauf() {
      if (sichtbar()) es.forEach(function (e) { var t = +e.dataset.t; e.style.setProperty('--px', (mx * t).toFixed(1) + 'px'); e.style.setProperty('--py', (my * t * .6).toFixed(1) + 'px'); });
      requestAnimationFrame(lauf);
    })();
  }

  /* 14: das Bild bleibt stehen und wechselt mit dem Eintrag, der gerade in der Mitte steht */
  if (hat('v14')) {
    var bl = qa('.ih-b'), hb = qa('.ih-halt .ih-f');
    function setze(i) { bl.forEach(function (b, j) { b.classList.toggle('an', j === i); }); hb.forEach(function (b, j) { b.classList.toggle('an', j === i); }); }
    setze(0);
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) setze(+e.target.dataset.n); }); }, { rootMargin: '-45% 0px -45% 0px' });
      bl.forEach(function (b) { io.observe(b); });
    }
  }
})();
