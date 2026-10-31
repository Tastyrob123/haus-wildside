/* Gut zu wissen · 15 Fassungen: eine Frage offen (alle Aufklapp-Fassungen), Bild wechselt mit (02), Deckel drehen (05),
   Stichworte (07), Blättern (11), Linie zieht mit (09). */
(function () {
  'use strict';
  document.querySelectorAll('[data-fq-eins]').forEach(function (box) {
    var sek = box.closest('.fq');
    box.querySelectorAll('details').forEach(function (d) {
      d.addEventListener('toggle', function () {
        if (!d.open) return;
        box.querySelectorAll('details[open]').forEach(function (x) { if (x !== d) x.open = false; });
        if (sek) sek.querySelectorAll('[data-fq-bild]').forEach(function (b) { b.classList.toggle('an', b.dataset.fqBild === d.dataset.j); });
      });
    });
  });
  document.querySelectorAll('[data-fq-dreh]').forEach(function (b) {
    b.addEventListener('click', function () { var an = b.classList.toggle('um'); b.setAttribute('aria-pressed', an); });
  });
  document.querySelectorAll('.fq07').forEach(function (s) {
    s.querySelectorAll('[data-fq-reiter]').forEach(function (w) {
      w.addEventListener('click', function () {
        var j = w.dataset.fqReiter;
        s.querySelectorAll('[data-fq-reiter]').forEach(function (x) { x.classList.toggle('an', x === w); });
        s.querySelectorAll('[data-fq-tafel]').forEach(function (t) { t.classList.toggle('an', t.dataset.fqTafel === j); });
      });
    });
  });
  document.querySelectorAll('[data-fq-blatt]').forEach(function (b) {
    var s = [].slice.call(b.querySelectorAll('[data-fq-schritt]')), p = [].slice.call(b.querySelectorAll('[data-fq-geh]')), i = 0;
    function geh(j) { i = (j + s.length) % s.length; s.forEach(function (x, k) { x.classList.toggle('an', k === i); }); p.forEach(function (x, k) { x.classList.toggle('an', k === i); }); }
    b.querySelectorAll('[data-fq-schub]').forEach(function (k) { k.addEventListener('click', function () { geh(i + +k.dataset.fqSchub); }); });
    p.forEach(function (x, k) { x.addEventListener('click', function () { geh(k); }); });
  });
  /* Goldlinie (09): wächst mit dem Scrollen, Paare erscheinen, wenn sie ins Bild kommen */
  document.querySelectorAll('.fq09-weg').forEach(function (w) {
    var l = w.querySelector('.fq09-linie'), takt = 0;
    function rechne() { takt = 0; var r = w.getBoundingClientRect(), p = Math.max(0, Math.min(1, (innerHeight * .7 - r.top) / r.height)); l.style.transform = 'scaleY(' + p.toFixed(3) + ')'; }
    addEventListener('scroll', function () { if (!takt) takt = requestAnimationFrame(rechne); }, { passive: true }); rechne();
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.fq04-paar,.fq09-p,.fq13-z,.fq03-p,.fq12-z').forEach(function (x) { io.observe(x); });
  } else document.querySelectorAll('.fq04-paar,.fq09-p,.fq13-z,.fq03-p,.fq12-z').forEach(function (x) { x.classList.add('da'); });
})();
