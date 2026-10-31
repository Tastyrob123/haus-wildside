/* Wild Side · Abschnitt «bar», zweite Runde: was mehr als CSS braucht. Nur transform, ein Takt für alles am Scrollen. */
(function () {
  'use strict';
  var s = document.getElementById('bar'); if (!s || !s.classList.contains('b2')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  var $$ = function (q) { return [].slice.call(s.querySelectorAll(q)); };
  var imBild = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { imBild = es[0].isIntersecting; }).observe(s);

  /* schmal: bleibt in einer Wand eine Kachel allein in der Reihe, geht sie über die ganze Breite */
  function ganz() {
    var schmal = innerWidth <= 900;
    $$('[class*="-wand"],.w07-reihe,.w13-reihe,.w15-oben,.w01-reihe').forEach(function (w) {
      var ks = [].slice.call(w.children).filter(function (c) { return c.classList.contains('kachel'); });
      ks.forEach(function (c) { c.classList.remove('ganz'); });
      if (!schmal) return;
      var n = 0, letzte = null;
      [].slice.call(w.children).forEach(function (c) {
        if (c.classList.contains('plakat') || c.classList.contains('w01-reihe')) { if (n % 2 && letzte) letzte.classList.add('ganz'); n = 0; letzte = null; }
        else if (c.classList.contains('kachel') || c.classList.contains('w14-f')) { n++; letzte = c.classList.contains('kachel') ? c : null; }
      });
      if (n % 2 && letzte) letzte.classList.add('ganz');
    });
  }
  ganz(); addEventListener('resize', ganz);

  /* 03 · Die Wand lebt: alle 3,2 s tauscht eine Kachel ihr Foto, das neue schiebt sich von unten herein */
  if (v === 3 && !ruhig) {
    var mos = s.querySelector('.mosaik'), pool = JSON.parse(mos.dataset.pool || '[]'), ks = [].slice.call(mos.querySelectorAll('.kachel'));
    var reihe = [3, 0, 5, 1, 4, 2], schritt = 0, p = 0;
    setInterval(function () {
      if (!imBild || document.hidden || !pool.length) return;
      var kach = ks[reihe[schritt % reihe.length] % ks.length]; schritt++;
      var d = pool[p % pool.length]; p++;
      var img = new Image(); img.className = 'tausch'; img.alt = d.a; img.decoding = 'async';
      img.sizes = Math.round(kach.offsetWidth) + 'px'; img.srcset = d.s;
      var los = function () {
        kach.appendChild(img);
        requestAnimationFrame(function () { requestAnimationFrame(function () { img.classList.add('an'); }); });
        setTimeout(function () { [].slice.call(kach.querySelectorAll('img')).forEach(function (x) { if (x !== img) x.remove(); }); img.classList.remove('tausch', 'an'); img.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:cover'; }, 1400);
      };
      if (img.decode) img.decode().then(los, los); else img.onload = los;
    }, 3200);
  }

  /* 10 · Mit Tiefe: die Maus verschiebt Plakat und Fotos verschieden weit */
  if (v === 10 && !ruhig && matchMedia('(hover:hover)').matches) {
    var wand = s.querySelector('.w10-wand'), teile = $$('.w10-t');
    wand.addEventListener('mousemove', function (e) {
      var r = wand.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      teile.forEach(function (t) { t.style.setProperty('--mx', (-x * 18).toFixed(1)); t.style.setProperty('--my', (-y * 14).toFixed(1)); });
    });
    wand.addEventListener('mouseleave', function () { teile.forEach(function (t) { t.style.setProperty('--mx', 0); t.style.setProperty('--my', 0); }); });
  }

  /* 11 · Die Wand schliesst sich: steht die Wand mitten im Bild, ist sie geschlossen; davor und danach stehen die Kacheln versetzt */
  if (v === 11 && !ruhig) {
    var w11 = s.querySelector('.w11-wand'), tick = false;
    var rechnen = function () {
      tick = false;
      var r = w11.getBoundingClientRect(), p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      if (Math.abs(p) < .08) p = 0; else p = p > 0 ? p - .08 : p + .08;
      w11.style.setProperty('--p', Math.max(-1, Math.min(1, p * 1.6)).toFixed(3));
    };
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }, { passive: true });
    addEventListener('resize', rechnen); rechnen();
  }
})();
