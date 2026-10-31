/* Wild Side · Abschnitt «bar», 15 Fassungen: die Bewegungen, die mehr als CSS brauchen. Ein Takt (requestAnimationFrame), nur transform und opacity. */
(function () {
  'use strict';
  var s = document.getElementById('bar'); if (!s) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  var $ = function (q, r) { return (r || s).querySelector(q); }, $$ = function (q, r) { return [].slice.call((r || s).querySelectorAll(q)); };
  function laden(img) { if (img && img.dataset.srcset) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); } }
  function sichtbar(cb) { if (!('IntersectionObserver' in window)) return cb(true); new IntersectionObserver(function (es) { cb(es[0].isIntersecting); }).observe(s); }
  var imBild = false; sichtbar(function (x) { imBild = x; });

  /* Ein gemeinsamer Takt für alles, was am Scrollen hängt */
  var proScroll = [];
  function takt() { proScroll.forEach(function (f) { f(); }); }
  var tick = false;
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; if (imBild) takt(); }); } }, { passive: true });
  addEventListener('resize', takt);

  /* 04 · Wer, Wo, Wann: Bild schiebt sich herein, von selbst alle fünf Sekunden, mit der Maus sofort */
  if (v === 4) {
    var dias = $$('.v04-dia'), zeilen = $$('.v04-z'), jetzt = 0, halt = false;
    dias.forEach(function (d) { laden(d.querySelector('img')); });
    function zeige(i) {
      if (i === jetzt) return;
      var alt = dias[jetzt]; alt.classList.remove('an'); alt.classList.add('war');
      dias[i].classList.add('an'); jetzt = i;
      zeilen.forEach(function (z) { z.classList.toggle('an', +z.dataset.i === i); });
      setTimeout(function () { alt.classList.remove('war'); }, 1100);
    }
    zeilen.forEach(function (z) {
      z.addEventListener('mouseenter', function () { halt = true; zeige(+z.dataset.i); });
      z.addEventListener('focus', function () { halt = true; zeige(+z.dataset.i); });
      z.addEventListener('click', function () { zeige(+z.dataset.i); });
    });
    $('.v04-zeilen').addEventListener('mouseleave', function () { halt = false; });
    if (!ruhig) setInterval(function () { if (!halt && imBild) zeige((jetzt + 1) % dias.length); }, 5000);
  }

  /* 05 · Diashow: blättert von selbst, Zähler, Goldlinie läuft */
  if (v === 5) {
    var spur = $('.v05-spur'), n5 = spur.children.length, i5 = 0, alts = JSON.parse($('.v05-show').dataset.alt), linie = $('.v05-linie i');
    $$('.v05-spur img').forEach(laden);
    function blatt() {
      spur.style.transform = 'translateX(' + (-i5 * 100) + '%)';
      $('.v05-nr').textContent = ('0' + (i5 + 1)).slice(-2) + ' / ' + ('0' + n5).slice(-2);
      $('.v05-alt').textContent = alts[i5];
      linie.classList.remove('lauf'); void linie.offsetWidth; linie.classList.add('lauf');
    }
    blatt();
    if (!ruhig) setInterval(function () { if (imBild) { i5 = (i5 + 1) % n5; blatt(); } }, 4600);
  }

  /* 09 · Drei Tempi: jedes Foto zieht in seinem Rahmen anders schnell */
  if (v === 9 && !ruhig) {
    var ins = $$('.v09-in');
    proScroll.push(function () {
      ins.forEach(function (el) {
        var r = el.parentNode.getBoundingClientRect(), p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
        el.style.transform = 'translate3d(0,' + (p * 10 * +el.dataset.tempo).toFixed(2) + '%,0)';
      });
    });
    takt();
  }

  /* 11 · Kacheln neigen sich zur Maus */
  if (v === 11 && !ruhig && matchMedia('(hover:hover)').matches) {
    $$('.v11-k').forEach(function (k) {
      k.addEventListener('mousemove', function (e) {
        var r = k.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        k.style.setProperty('--ry', (x * 7).toFixed(2) + 'deg'); k.style.setProperty('--rx', (-y * 7).toFixed(2) + 'deg');
      });
      k.addEventListener('mouseleave', function () { k.style.setProperty('--ry', '0deg'); k.style.setProperty('--rx', '0deg'); });
    });
  }

  /* 12 · Hinein unter die Decke: das Bild wird beim Durchscrollen langsam grösser (1 bis 1,3; Quelle 3024 px breit) */
  if (v === 12 && !ruhig) {
    var bue = $('.v12-buehne'), bi = $('.v12-bild img');
    proScroll.push(function () {
      var r = bue.getBoundingClientRect(), p = Math.min(1, Math.max(0, (innerHeight - r.top) / (innerHeight + r.height)));
      bi.style.setProperty('--z', (1 + p * .3).toFixed(4));
    });
    takt();
  }

  /* 13 · Doppelseite: die Fotos folgen der Maus ein wenig */
  if (v === 13 && !ruhig && matchMedia('(hover:hover)').matches) {
    var heft = $('.v13-heft'), fotos = $$('.v13-rechts .vb');
    heft.addEventListener('mousemove', function (e) {
      var r = heft.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      fotos.forEach(function (f, j) { var t = j ? 14 : 9; f.style.setProperty('--mx', (-x * t).toFixed(1) + 'px'); f.style.setProperty('--my', (-y * t).toFixed(1) + 'px'); });
    });
    heft.addEventListener('mouseleave', function () { fotos.forEach(function (f) { f.style.setProperty('--mx', '0px'); f.style.setProperty('--my', '0px'); }); });
  }

  /* 14 · Regler: zieht man, wandert das Bild mit; lässt man los, rastet es am nächsten Halt ein */
  if (v === 14) {
    var ein = $('.v14-regler input'), sp = $('.v14-spur'), stopps = $$('.v14-stopp'), max = +ein.max;
    $$('.v14-spur img').forEach(laden);
    function setz(p, gleiten) {
      sp.classList.toggle('gleiten', !!gleiten);
      sp.style.setProperty('--p', p); ein.value = p; ein.style.setProperty('--q', p / max);
      var n = Math.round(p); stopps.forEach(function (b, j) { b.classList.toggle('an', j === n); });
    }
    ein.addEventListener('input', function () { setz(+ein.value, false); });
    ein.addEventListener('change', function () { setz(Math.round(+ein.value), true); });
    stopps.forEach(function (b) { b.addEventListener('click', function () { setz(+b.dataset.i, true); }); });
    setz(0, false);
  }

  /* 15 · Der Satz wird hell, Wort für Wort, während er von unten zur Mitte zieht */
  if (v === 15 && !ruhig) {
    var satz = $('.v15-satz'), w = $$('.v15-w');
    proScroll.push(function () {
      var r = satz.getBoundingClientRect(), p = (innerHeight * .86 - r.top) / (r.height + innerHeight * .3);
      var n = Math.round(Math.min(1, Math.max(0, p)) * w.length);
      w.forEach(function (x, j) { x.classList.toggle('hell', j < n); });
    });
    takt();
  }
})();
