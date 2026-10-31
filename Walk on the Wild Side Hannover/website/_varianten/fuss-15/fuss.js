/* Walk on the Wild Side · 15 Fassungen für den Fuss: das Band läuft nur, solange es zu sehen ist (07); die Platten neigen sich leicht zur Maus (09). */
(function () {
  var ruhig = document.documentElement.classList.contains('ruhig');
  var f07 = document.querySelector('.f07');
  if (f07 && !ruhig && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) { es.forEach(function (e) { f07.classList.toggle('lauf', e.isIntersecting); }); }).observe(f07.querySelector('.f07-band'));
  }
  if (ruhig || !matchMedia('(hover:hover) and (pointer:fine)').matches) return;
  document.querySelectorAll('.f09 .f09-p').forEach(function (p) {
    var takt = 0;
    p.addEventListener('pointermove', function (ev) {
      if (takt) return;
      takt = requestAnimationFrame(function () {
        takt = 0;
        var r = p.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width - .5, y = (ev.clientY - r.top) / r.height - .5;
        p.classList.add('zieht');
        p.style.setProperty('--ry', (x * 5).toFixed(2) + 'deg');
        p.style.setProperty('--rx', (-y * 4).toFixed(2) + 'deg');
      });
    });
    p.addEventListener('pointerleave', function () { p.style.setProperty('--ry', '0deg'); p.style.setProperty('--rx', '0deg'); });
  });
})();
