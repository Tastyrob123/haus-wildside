/* Wild Side · Kopf «Das Haus», zweite Runde: 01 Leuchtschrift (Birnen aus der Schrift gerechnet), 09 Lichtkegel, 13 Prisma am Scrollen. Nur transform und opacity. */
(function () {
  'use strict';
  var s = document.getElementById('auftakt'); if (!s || !s.classList.contains('g')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');

  /* 01 · Leuchtschrift: die Schrift wird auf ein Raster gelegt, jeder getroffene Punkt wird eine Birne */
  if (v === 1) {
    var svg = s.querySelector('.w01-svg');
    var bau = function () {
      var zeilen = ['UNTER DIESER', 'DECKE.'], fs = 230, lh = 250, schritt = 15;
      var c = document.createElement('canvas'), x = c.getContext('2d');
      x.font = '700 ' + fs + 'px Hanken, Arial, sans-serif';
      var breite = Math.ceil(Math.max.apply(null, zeilen.map(function (z) { return x.measureText(z).width; }))) + 20;
      c.width = breite; c.height = lh * zeilen.length + 20;
      x.font = '700 ' + fs + 'px Hanken, Arial, sans-serif'; x.fillStyle = '#000'; x.textBaseline = 'alphabetic';
      zeilen.forEach(function (z, i) { x.fillText(z, 10, 10 + fs * .86 + i * lh); });
      var d = x.getImageData(0, 0, c.width, c.height).data, ns = 'http://www.w3.org/2000/svg', g = document.createDocumentFragment(), n = 0;
      for (var yy = schritt / 2; yy < c.height; yy += schritt) for (var xx = schritt / 2; xx < c.width; xx += schritt) {
        if (d[(Math.round(yy) * c.width + Math.round(xx)) * 4 + 3] < 140) continue;
        var dl = (xx / c.width * 1.6 + (yy > lh ? .5 : 0) + Math.random() * .12).toFixed(3) + 's';
        var fl = Math.random() < .025;
        [['aus', 4.6], ['hof', 9], ['an', 4.6]].forEach(function (k) {
          var e = document.createElementNS(ns, 'circle'); e.setAttribute('cx', xx); e.setAttribute('cy', yy); e.setAttribute('r', k[1]);
          e.setAttribute('class', k[0] + (fl && k[0] !== 'aus' ? ' fl' : '')); e.style.setProperty('--d', dl); g.appendChild(e);
        });
        n++;
      }
      svg.setAttribute('viewBox', '0 0 ' + c.width + ' ' + c.height); svg.appendChild(g);
      requestAnimationFrame(function () { requestAnimationFrame(function () { s.classList.add('birnen'); }); });
    };
    (document.fonts && document.fonts.load ? document.fonts.load('700 230px Hanken') : Promise.resolve()).then(bau, bau);
  }

  /* 09 · Lichtkegel: einmal von links nach rechts über das Gewölbe, danach folgt er der Maus, weich nachgezogen */
  if (v === 9) {
    var band = s.querySelector('.w09-band'), kegel = s.querySelector('.w09-kegel'), hell = s.querySelector('.w09-hell');
    var pos = { x: -300, y: 0 }, ziel = null, t0 = null, an = false;
    var mass = function () { hell.style.setProperty('--bw', band.offsetWidth + 'px'); hell.style.setProperty('--bh', band.offsetHeight + 'px'); };
    mass(); addEventListener('resize', mass);
    var setze = function () { kegel.style.setProperty('--x', pos.x.toFixed(1) + 'px'); kegel.style.setProperty('--y', pos.y.toFixed(1) + 'px'); };
    var fahrt = function (t) {
      if (t0 === null) t0 = t;
      var u = Math.min(1, (t - t0) / 3400), e = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2, w = band.offsetWidth, h = band.offsetHeight;
      if (!ziel) { pos.x = -200 + e * (w * .62 + 200); pos.y = h * (.62 - .3 * Math.sin(e * Math.PI)); setze(); }
      if (u < 1 && !ziel) requestAnimationFrame(fahrt);
    };
    if (ruhig) { pos.x = band.offsetWidth * .6; pos.y = band.offsetHeight * .45; setze(); }
    else setTimeout(function () { requestAnimationFrame(fahrt); }, 500);
    var folge = function () {
      an = false; if (!ziel) return;
      pos.x += (ziel.x - pos.x) * .14; pos.y += (ziel.y - pos.y) * .14; setze();
      if (Math.abs(ziel.x - pos.x) + Math.abs(ziel.y - pos.y) > .5) { an = true; requestAnimationFrame(folge); }
    };
    band.addEventListener('pointermove', function (ev) {
      var r = band.getBoundingClientRect(); ziel = { x: ev.clientX - r.left, y: ev.clientY - r.top };
      if (!an) { an = true; requestAnimationFrame(folge); }
    });
  }

  /* 13 · Prisma: dreht sich mit dem Scrollen um 240 Grad, im Satz leuchtet die Seite, die gerade vorn ist */
  if (v === 13 && !ruhig && innerWidth > 760) {
    var pr = s.querySelector('.w13-prisma'), teile = [].slice.call(s.querySelectorAll('.w13-s span[data-t]')), lauf = false, vorn = -1;
    var takt = function () {
      lauf = false;
      var r = s.getBoundingClientRect(), t = Math.max(0, Math.min(1, -r.top / Math.max(1, r.height - innerHeight)));
      var e = t * 2, k = Math.floor(e), f = e - k;                    // je Seite erst stehen, dann drehen
      var w = k + (f < .35 ? 0 : (f - .35) / .65);
      w = Math.min(2, w); pr.style.setProperty('--rot', (-w * 120).toFixed(2) + 'deg');
      var j = Math.round(w); if (j !== vorn) { vorn = j; teile.forEach(function (sp) { sp.classList.toggle('jetzt', +sp.dataset.t === j); }); }
    };
    addEventListener('scroll', function () { if (!lauf) { lauf = true; requestAnimationFrame(takt); } }, { passive: true });
    takt();
  } else if (v === 13) { var sp0 = s.querySelector('.w13-s span[data-t="0"]'); if (sp0) sp0.classList.add('jetzt'); }
})();
