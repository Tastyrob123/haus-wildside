/* Wild Side · «Was bisher geschah.», 30 Fassungen. Auftritt je Jahr, Scroll-Dinge in einem Takt, nur transform. */
(function () {
  'use strict';
  var s = document.getElementById('seit2017'); if (!s || !s.classList.contains('j3')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion:reduce)').matches;
  var $$ = function (q) { return [].slice.call(s.querySelectorAll(q)); };

  /* alle Bilder des Abschnitts gleich laden (auch die, die seitlich ausserhalb stehen) */
  $$('img[data-srcset]').forEach(function (i) { i.sizes = i.dataset.sizes || '30vw'; i.srcset = i.dataset.srcset; i.removeAttribute('data-srcset'); });

  /* Auftritt: jedes Jahr, sobald es am unteren Rand auftaucht; der Abschnitt selbst bekommt .da */
  var jx = $$('.jx');
  if (ruhig || !('IntersectionObserver' in window)) { jx.forEach(function (e) { e.classList.add('da'); }); s.classList.add('da', 'drin'); }
  else {
    var o = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); o.unobserve(e.target); } }); }, { rootMargin: '0px 0px 4% 0px' });
    jx.forEach(function (e) { o.observe(e); }); o.observe(s);
    $$('.v04-streifen,.v09,.v12,.v14-bilder,.v20-tisch,.v23-bilder,.v24-z,.v26,.v28-boden,.v24-b').forEach(function (e) { o.observe(e); });
  }

  /* Laufband (19) läuft nur, solange es im Blick ist */
  var band = s.querySelector('.v19-band');
  if (band && 'IntersectionObserver' in window) new IntersectionObserver(function (es) { band.classList.toggle('laeuft', es[0].isIntersecting && !ruhig); }).observe(band);

  var pin = s.querySelector('.pin');
  var braucht = pin || v === 29;
  if (!braucht) return;
  if (ruhig && pin) { s.classList.add('ruhig-pin'); return; }

  function klemm(x, a, b) { return Math.max(a, Math.min(b, x)); }
  /* hält jedes Jahr eine Weile still und schiebt dann weich zum nächsten */
  function stufen(c) { var f = Math.floor(c), r = c - f, t = klemm((r - .32) / .36, 0, 1); t = t * t * (3 - 2 * t); return Math.min(4, f + t); }

  var imBild = false, an = false;
  new IntersectionObserver(function (es) { imBild = es[0].isIntersecting; if (imBild) los(); }, { rootMargin: '20% 0px 20% 0px' }).observe(s);
  var spur = s.querySelector('.v03-band'), W = 0;
  function mass() { if (spur) W = Math.max(0, spur.scrollWidth - innerWidth); }
  mass();
  var bl = $$('.v08-bl'), k13 = $$('.v13-k'), t13 = $$('.v13-t'), k18 = $$('.v18-bl'), e30 = $$('.v30-e');

  function takt() {
    an = false; if (!imBild) return;
    var h = innerHeight;
    if (v === 29) {
      var r = s.getBoundingClientRect();
      s.style.setProperty('--r', ((r.top + r.height / 2 - h / 2) / h).toFixed(4));
      return;
    }
    var pr = pin.getBoundingClientRect(), p = klemm(-pr.top / Math.max(1, pr.height - h), 0, 1), c = stufen(p * 4.0001);
    s.style.setProperty('--c', c.toFixed(4));
    if (v === 3) spur.style.transform = 'translate3d(' + (-p * W).toFixed(1) + 'px,0,0)';
    if (v === 8) bl.forEach(function (e, i) {
      var q = klemm(c - i, 0, 1), w = -180 * q;
      e.style.transform = 'rotateY(' + w.toFixed(2) + 'deg)'; e.style.zIndex = w < -90 ? 20 + i : 10 - i;
      e.children[0].style.visibility = w < -90 ? 'hidden' : 'visible'; e.children[1].style.visibility = w < -90 ? 'visible' : 'hidden';
    });
    if (v === 13) {
      var bw = k13[0].offsetWidth;
      k13.forEach(function (e, i) {
        var d = i - c, ad = Math.abs(d), sg = d < 0 ? -1 : 1;
        var x = sg * (Math.min(ad, 1) * bw * 1.06 + Math.max(0, ad - 1) * bw * .62);
        e.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,' + (-Math.min(ad, 2.2) * 220).toFixed(1) + 'px) rotateY(' + (-sg * Math.min(ad, 1) * 42).toFixed(2) + 'deg)';
        e.style.zIndex = 20 - Math.round(ad * 4);
      });
      t13.forEach(function (e, i) { e.style.transform = 'translate3d(0,' + ((i - c) * 112).toFixed(2) + '%,0)'; });
    }
    if (v === 18) k18.forEach(function (e, i) {
      var q = i < 4 ? klemm(c - i, 0, 1) : 0;
      e.style.transform = 'translate3d(0,' + (-q * h * 1.15).toFixed(1) + 'px,0) rotate(' + (-q * 7).toFixed(2) + 'deg)';
    });
    if (v === 30) e30.forEach(function (e, i) {
      var d = i - c, t;
      if (d >= 0) t = 'translate3d(0,0,' + (-d * 900).toFixed(1) + 'px)';
      else t = 'translate3d(0,' + (d * 125).toFixed(2) + 'vh,' + (-d * 380).toFixed(1) + 'px)';
      e.style.transform = t; e.style.visibility = d > 1.05 || d < -1 ? 'hidden' : 'visible';
    });
  }
  function los() { if (!an) { an = true; requestAnimationFrame(takt); } }
  addEventListener('scroll', los, { passive: true });
  addEventListener('resize', function () { mass(); los(); });
  los();
})();
