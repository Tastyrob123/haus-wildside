/* Wild Side · «Was bisher geschah.», 15 Fassungen: Auftritt je Jahr nach der Uhr, Scroll-Dinge in einem Takt, nur transform. */
(function () {
  'use strict';
  var s = document.getElementById('seit2017'); if (!s || !s.classList.contains('ja')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion:reduce)').matches;
  var jx = [].slice.call(s.querySelectorAll('.jx'));

  /* jedes Jahr schwebt herein, sobald es am unteren Rand auftaucht */
  if (ruhig || !('IntersectionObserver' in window)) { jx.forEach(function (e) { e.classList.add('da'); }); s.classList.add('da'); }
  else {
    var o = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); o.unobserve(e.target); } }); }, { rootMargin: '0px 0px 8% 0px' });
    jx.forEach(function (e) { o.observe(e); });
  }

  /* 07 · die Ziffern rollen zum Jahr, das gerade in der Mitte steht */
  if (v === 7) {
    var sp = [].slice.call(s.querySelectorAll('.v07-s>span'));
    var setze = function (j) { for (var i = 0; i < 4; i++) sp[i].style.setProperty('--d', j.charAt(i)); };
    setze('2018');
    if ('IntersectionObserver' in window) {
      var m = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) setze(e.target.dataset.j); }); }, { rootMargin: '-45% 0px -45% 0px' });
      jx.forEach(function (e) { m.observe(e); });
    }
  }

  /* 03 Mittelachse, 10 Treppe: in einem Takt am Scrollen, nur solange der Abschnitt im Blick ist */
  if ((v !== 3 && v !== 10) || ruhig) return;
  var imBild = false, an = false;
  new IntersectionObserver(function (es) { imBild = es[0].isIntersecting; if (imBild) los(); }).observe(s);
  var linie = s.querySelector('.v03-l');
  function takt() {
    an = false; if (!imBild) return;
    var h = innerHeight;
    if (v === 3) {
      var r = linie.getBoundingClientRect();
      linie.style.setProperty('--p', Math.max(0, Math.min(1, (h * .6 - r.top) / r.height)).toFixed(4));
    } else {
      jx.forEach(function (e, i) {
        var r = e.getBoundingClientRect(), t = (r.top + r.height / 2 - h / 2) / h;   // -0.5 … 0.5 um die Mitte
        e.style.setProperty('--y', (t * (i + 1) * 26).toFixed(1) + 'px');
      });
    }
  }
  function los() { if (!an) { an = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', los, { passive: true }); addEventListener('resize', los);
  los();
})();
