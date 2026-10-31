/* Wild Side · Programm, 20 Fassungen für den Kopf: Kippen (12), Tiefe beim Scrollen (14), Plakate blättern (15), Streifen (16). Nur transform, ein Takt. */
(function () {
  'use strict';
  var h = document.querySelector('.ph'); if (!h) return;
  var v = +h.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  var $$ = function (q) { return [].slice.call(h.querySelectorAll(q)); };
  var beimScrollen = function (fn) {
    var tick = false;
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; fn(); }); } }, { passive: true });
    fn();
  };

  /* 12 · das Plakat neigt sich zur Maus */
  if (v === 12 && !ruhig && matchMedia('(hover:hover)').matches) {
    var karte = h.querySelector('[data-kipp]'), f = karte.querySelector('.ph-f');
    h.addEventListener('mousemove', function (e) {
      var r = karte.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      f.style.setProperty('--ry', (x * 12).toFixed(2) + 'deg'); f.style.setProperty('--rx', (-y * 9).toFixed(2) + 'deg');
    });
    h.addEventListener('mouseleave', function () { f.style.setProperty('--ry', '0deg'); f.style.setProperty('--rx', '0deg'); });
  }

  /* 14 · Foto bleibt beim Scrollen zurück, der Titel zieht schneller */
  if (v === 14 && !ruhig) {
    var tief = h.querySelector('.ph14-tief'), vorn = h.querySelector('.ph14-vorn');
    beimScrollen(function () {
      var y = Math.min(scrollY, h.offsetHeight);
      tief.style.transform = 'translate3d(0,' + (y * .35).toFixed(1) + 'px,0)';
      vorn.style.transform = 'translate3d(0,' + (-y * .25).toFixed(1) + 'px,0)';
    });
  }

  /* 15 · alle 3 s das nächste Plakat, der Name darunter wechselt mit */
  if (v === 15 && !ruhig) {
    var bl = $$('.ph15-b'), name = h.querySelector('[data-namen]'), namen = JSON.parse(name.dataset.namen), i = 0;
    setInterval(function () {
      if (document.hidden) return;
      var alt = i; i = (i + 1) % bl.length;
      bl.forEach(function (b) { b.classList.remove('war'); });
      bl[alt].classList.remove('an'); bl[alt].classList.add('war'); bl[i].classList.add('an');
      name.textContent = namen[i];
    }, 3000);
  }

  /* 16 · der Streifen läuft beim Scrollen seitwärts */
  if (v === 16 && !ruhig) {
    var zug = h.querySelector('.ph16-zug');
    beimScrollen(function () {
      var y = Math.min(scrollY, h.offsetHeight * 1.2);
      zug.style.transform = 'translate3d(' + (-y * .6).toFixed(1) + 'px,0,0)';
    });
  }
})();
