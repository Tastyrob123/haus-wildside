/* Wild Side · Drinks, 15 Fassungen für den Kopf: Wortwechsel (04), Tiefe beim Scrollen (07), Regler (12), Kippen (13). Nur transform, ein Takt. */
(function () {
  'use strict';
  var h = document.querySelector('.dh'); if (!h) return;
  var v = +h.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  var $$ = function (q) { return [].slice.call(h.querySelectorAll(q)); };

  /* 04 · alle 3 s ein anderes Wort, das Foto schiebt sich mit herein */
  if (v === 4 && !ruhig) {
    var worte = $$('.dh04-w span'), fotos = $$('.dh04-b'), i = 0;
    setInterval(function () {
      if (document.hidden) return;
      var alt = i; i = (i + 1) % worte.length;
      worte[alt].classList.remove('an'); worte[alt].classList.add('weg');
      worte[i].classList.remove('weg'); worte[i].classList.add('an');
      setTimeout(function () { worte[alt].classList.remove('weg'); }, 950);
      fotos[alt].classList.remove('an'); fotos[alt].classList.add('war'); fotos[i].classList.add('an');
      setTimeout(function () { fotos[alt].classList.remove('war'); }, 1050);
    }, 3000);
  }

  /* 07 · Foto bleibt beim Scrollen zurück, der Titel zieht schneller */
  if (v === 7 && !ruhig) {
    var tief = h.querySelector('.dh07-tief'), vorn = h.querySelector('.dh07-vorn'), tick = false;
    var rechne = function () {
      tick = false; var y = Math.min(scrollY, h.offsetHeight);
      tief.style.transform = 'translate3d(0,' + (y * .35).toFixed(1) + 'px,0)';
      vorn.style.transform = 'translate3d(0,' + (-y * .25).toFixed(1) + 'px,0)';
    };
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechne); } }, { passive: true });
  }

  /* 12 · Regler zwischen den zwei Fotos: ziehen mit Maus oder Finger; zu Beginn fährt er einmal von selbst */
  if (v === 12) {
    var box = h.querySelector('[data-vergleich]'), zieh = false;
    var setz = function (p) { box.style.setProperty('--p', Math.max(4, Math.min(96, p)).toFixed(2) + '%'); };
    var vonX = function (x) { var r = box.getBoundingClientRect(); setz((x - r.left) / r.width * 100); };
    box.addEventListener('pointerdown', function (e) { zieh = true; vonX(e.clientX); });
    addEventListener('pointermove', function (e) { if (zieh) vonX(e.clientX); });
    addEventListener('pointerup', function () { zieh = false; });
    box.addEventListener('mousemove', function (e) { if (!zieh && matchMedia('(hover:hover)').matches) vonX(e.clientX); });
    if (!ruhig) {
      var t0 = null;
      var fahrt = function (t) { if (t0 === null) t0 = t; var p = Math.min(1, (t - t0) / 2200); setz(50 + Math.sin(p * Math.PI * 2) * 26); if (p < 1 && !zieh) requestAnimationFrame(fahrt); };
      setTimeout(function () { requestAnimationFrame(fahrt); }, 700);
    }
  }

  /* 13 · die Karte neigt sich zur Maus */
  if (v === 13 && !ruhig && matchMedia('(hover:hover)').matches) {
    var karte = h.querySelector('[data-kipp]'), f = karte.querySelector('.dh-f');
    h.addEventListener('mousemove', function (e) {
      var r = karte.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      f.style.setProperty('--ry', (x * 10).toFixed(2) + 'deg'); f.style.setProperty('--rx', (-y * 8).toFixed(2) + 'deg');
    });
    h.addEventListener('mouseleave', function () { f.style.setProperty('--ry', '0deg'); f.style.setProperty('--rx', '0deg'); });
  }
})();
