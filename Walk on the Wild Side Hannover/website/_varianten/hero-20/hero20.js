/* Walk on the Wild Side · Bewegung der 20 Auftakte. Nur transform und opacity, ein Takt (requestAnimationFrame), ruhig gestellt = Endzustand. */
(function () {
  'use strict';
  var k = document.getElementById('auftakt');
  if (!k) return;
  var ruhig = document.documentElement.classList.contains('ruhig');
  var fein = matchMedia('(hover:hover) and (pointer:fine)').matches;
  function hat(c) { return k.classList.contains(c); }
  function bereit(f) { var t = setInterval(function () { if (hat('da')) { clearInterval(t); f(); } }, 60); }
  function sichtbar() { var r = k.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }
  function q(s) { return k.querySelector(s); }
  function qa(s) { return [].slice.call(k.querySelectorAll(s)); }
  var mx = 0, my = 0, maus = 0;
  if (fein) k.addEventListener('mousemove', function (e) { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; maus = performance.now(); });
  function scrollTakt(f) {
    var tick = false;
    function los() { tick = false; f(k.getBoundingClientRect()); }
    addEventListener('scroll', function () { if (!tick && sichtbar()) { tick = true; requestAnimationFrame(los); } }, { passive: true });
    addEventListener('resize', los); los();
  }

  /* 04 und 05: zur Maus neigen, ohne Maus sanft pendeln */
  if ((hat('x04') || hat('x05')) && !ruhig) {
    var ziel = q(hat('x04') ? '.x-kasten' : '.x-haus');
    bereit(function () {
      setTimeout(function () {
        ziel.classList.add('folgt');
        (function lauf(now) {
          if (sichtbar()) {
            var x = mx, y = my;
            if (!fein || now - maus > 2500) { x = Math.sin(now / 2600) * .35; y = Math.sin(now / 3400) * .2; }
            if (hat('x04')) { ziel.style.setProperty('--ry', (-16 + x * 44).toFixed(2) + 'deg'); ziel.style.setProperty('--rx', (4 - y * 18).toFixed(2) + 'deg'); }
            else ziel.style.setProperty('--ry', (x * 34).toFixed(2) + 'deg');
          }
          requestAnimationFrame(lauf);
        })(performance.now());
      }, 2100);
    });
  }

  /* 06: der Ring dreht sich, die Maus gibt Schwung */
  if (hat('x06')) {
    var dreh = q('.x-dreh'), w = 0, v = .07;
    (function lauf() {
      if (sichtbar() && !ruhig) { var soll = .07 + (fein ? mx * .9 : 0); v += (soll - v) * .04; w += v; dreh.style.setProperty('--rot', w.toFixed(2) + 'deg'); }
      if (!ruhig) requestAnimationFrame(lauf);
    })();
  }

  /* 08: erst wird das Glas scharf; schaut man nach oben, wird die Bar scharf */
  if (hat('x08')) {
    var sour = q('.x-sour');
    function fokus(bar) { sour.style.setProperty('--bg', bar ? 1 : 0); sour.style.setProperty('--gl', bar ? 0 : 1); }
    if (ruhig) fokus(false);
    else bereit(function () {
      setTimeout(function () { fokus(false); }, 900);
      if (fein) sour.addEventListener('mousemove', function (e) { var r = sour.getBoundingClientRect(); fokus((e.clientY - r.top) / r.height < .42); });
      if (fein) sour.addEventListener('mouseleave', function () { fokus(false); });
    });
  }

  /* 12: die beiden Zeilen laufen beim Scrollen gegeneinander, das Band in eigener Geschwindigkeit */
  if (hat('x12') && !ruhig) {
    var z1 = q('.x-z1'), z2 = q('.x-z2'), sp = q('.x-band .x-spur');
    scrollTakt(function (r) {
      var p = Math.min(1, Math.max(0, -r.top / r.height));
      z1.style.setProperty('--a', (-p * 18).toFixed(2) + 'vw');
      z2.style.setProperty('--b', (p * 18).toFixed(2) + 'vw');
      sp.style.setProperty('--c', (-6 - p * 34).toFixed(2) + 'vw');
    });
  }

  /* 13: beim Scrollen die Theke entlang */
  if (hat('x13') && !ruhig) {
    var spur = q('.x-spur');
    scrollTakt(function (r) {
      var p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
      spur.style.setProperty('--x', (-p * Math.max(0, spur.scrollWidth - innerWidth)).toFixed(1) + 'px');
    });
  }

  /* 16: die Maus fährt durch die Nacht von 19 bis 2 Uhr; ohne Maus läuft die Nacht von selbst */
  if (hat('x16')) {
    var bilder = qa('.x-st'), zeiten = qa('.x-uhr span'), marke = q('.x-marke'), uhr = q('.x-uhr'), jetzt = -1;
    function stunde(i) {
      if (i === jetzt) return; jetzt = i;
      bilder.forEach(function (b, j) { if (j === i && b.loading === 'lazy') b.loading = 'eager'; b.classList.toggle('an', j === i); });
      zeiten.forEach(function (z, j) { z.classList.toggle('an', j === i); });
      var z = zeiten[i], ru = uhr.getBoundingClientRect(), rz = z.getBoundingClientRect();
      marke.style.setProperty('--mw', rz.width.toFixed(0) + 'px');
      marke.style.setProperty('--mx', (rz.left - ru.left).toFixed(0) + 'px');
    }
    stunde(0);
    bilder.forEach(function (b) { b.loading = 'eager'; });
    if (!ruhig) {
      if (fein) k.addEventListener('mousemove', function (e) {
        var r = k.getBoundingClientRect(), x = (e.clientX - r.width * .26) / (r.width * .74);
        if (x >= 0) stunde(Math.min(bilder.length - 1, Math.floor(x * bilder.length)));
      });
      setInterval(function () { if (sichtbar() && (!fein || performance.now() - maus > 3000)) stunde((jetzt + 1) % bilder.length); }, 2400);
    }
  }

  /* 03: beim Scrollen senkt sich die Decke über den Kopf */
  if (hat('x03') && !ruhig) {
    var decke = q('.x-decke');
    scrollTakt(function (r) {
      var p = Math.min(1, Math.max(0, -r.top / r.height));
      decke.style.transform = 'rotateX(' + (-48 + p * 18).toFixed(2) + 'deg)';
    });
  }

  /* 17: ins Glas hinein, bis alles rot ist */
  if (hat('x17') && !ruhig) {
    scrollTakt(function (r) {
      var p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
      k.style.setProperty('--s', (1 + Math.pow(p, 2.2) * 17).toFixed(3));
      k.style.setProperty('--r', Math.min(1, Math.max(0, (p - .55) / .3)).toFixed(3));
    });
  }

  /* 18: der Satz wird getippt */
  if (hat('x18')) {
    var bs = qa('.x-tipp .b'), cur = q('.x-cursor');
    if (ruhig) { bs.forEach(function (b) { b.classList.add('an'); }); cur.classList.add('aus'); }
    else {
      bs[0].parentNode.insertBefore(cur, bs[0]);
      bereit(function () {
        var i = 0;
        (function tipp() {
          if (i >= bs.length) { setTimeout(function () { cur.classList.add('aus'); }, 2600); return; }
          bs[i].classList.add('an'); bs[i].parentNode.insertBefore(cur, bs[i].nextSibling); i++;
          setTimeout(tipp, bs[i - 1].textContent === ',' ? 360 : 55 + Math.random() * 70);
        })();
      });
    }
  }

  /* 20: jedes Stück auf eigener Tiefe, folgt der Maus */
  if (hat('x20') && fein && !ruhig) {
    var es = qa('.x-e');
    (function lauf() {
      if (sichtbar()) es.forEach(function (e) {
        var t = +e.dataset.t;
        e.style.setProperty('--px', (mx * t).toFixed(1) + 'px'); e.style.setProperty('--py', (my * t * .5).toFixed(1) + 'px');
      });
      requestAnimationFrame(lauf);
    })();
  }
})();
