/* Wild Side · Besuch, Runde 2: Bewegung für Fallblatt (01), Fenster-Fahrt (03), Abend (09), Kerze (10), Rundumblick (13), Weg hinein (14), Karte (15), Ecke (07).
   Nur transform/opacity, alles in einem requestAnimationFrame-Takt. */
(function () {
  'use strict';
  var h = document.querySelector('.bx'); if (!h) return;
  var v = +h.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  var klemm = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var weich = function (a, b, x) { x = klemm((x - a) / (b - a)); return x * x * (3 - 2 * x); };
  var beimScrollen = function (fn) {
    var tick = false;
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(function () { tick = false; fn(); }); } }, { passive: true });
    addEventListener('resize', fn); fn();
  };
  var fortschritt = function () { var r = h.getBoundingClientRect(); return klemm(-r.top / Math.max(1, h.offsetHeight - innerHeight)); };
  var maus = matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* 01 · Fallblatt: Stand jetzt (Berliner Zeit) aus den Öffnungszeiten, dann klappern die Blätter */
  if (v === 1) {
    var teile = new Intl.DateTimeFormat('de-DE', { timeZone: 'Europe/Berlin', weekday: 'short', hour: 'numeric', hour12: false }).formatToParts(new Date());
    var wt = { Mo: 1, Di: 2, Mi: 3, Do: 4, Fr: 5, Sa: 6, So: 7 }[(teile.find(function (t) { return t.type === 'weekday'; }) || {}).value.slice(0, 2)];
    var std = +(teile.find(function (t) { return t.type === 'hour'; }) || {}).value % 24;
    var jetzt = (wt === 4 && std >= 19) || (wt === 5 && std < 1) ? 'GEÖFFNET BIS 1 UHR'
      : (wt === 5 && std >= 19) || (wt === 6 && std < 2) || (wt === 6 && std >= 19) || (wt === 7 && std < 2) ? 'GEÖFFNET BIS 2 UHR'
      : (wt >= 4 && wt <= 6 && std < 19) ? 'HEUTE AB 19 UHR' : 'DONNERSTAG AB 19 UHR';
    var zl = h.querySelector('.bx01-zeile.jetzt'), zz = zl.querySelectorAll('.bx01-z');
    for (var i = 0; i < zz.length; i++) zz[i].dataset.z = jetzt.charAt(i) || ' ';
    var zellen = [].slice.call(h.querySelectorAll('.bx01-z'));
    var ABC = 'ABCDEFGHIJKLMNOPRSTUVWZ0123456789';
    var setze = function (b, c) { b.textContent = c === ' ' ? ' ' : c; b.className = b.className === 'k1' ? 'k2' : 'k1'; };
    if (ruhig) { zellen.forEach(function (z) { z.firstChild.textContent = z.dataset.z === ' ' ? ' ' : z.dataset.z; }); }
    else {
      var start = function () {
        zellen.forEach(function (z, n) {
          var b = z.firstChild, ziel = z.dataset.z, schritte = (ziel === ' ' ? 2 : 6) + Math.floor(Math.random() * 8) + (n % 20) * .35, k = 0;
          var lauf = setInterval(function () {
            k++;
            if (k >= schritte) { clearInterval(lauf); setze(b, ziel); return; }
            setze(b, ABC.charAt(Math.floor(Math.random() * ABC.length)));
          }, 70);
        });
      };
      setTimeout(start, 700);
    }
  }

  /* 03 · Kamera fährt durch die Scheibe */
  if (v === 3 && !ruhig) {
    var aus = h.querySelector('.bx03-aussen'), inn = h.querySelector('.bx03-innen');
    beimScrollen(function () {
      var p = fortschritt();
      aus.style.transform = 'scale(' + (1 + 3.4 * p * p).toFixed(3) + ')';
      aus.style.opacity = (1 - weich(.5, .86, p)).toFixed(3);
      inn.style.transform = 'scale(' + (1.25 - .25 * weich(.35, 1, p)).toFixed(3) + ')';
      inn.style.opacity = weich(.4, .82, p).toFixed(3);
    });
  }

  /* 07 · die Ecke folgt der Maus */
  if (v === 7 && !ruhig && maus) {
    var ecke = h.querySelector('.bx07-ecke');
    setTimeout(function () {
      ecke.classList.add('folgt');
      h.addEventListener('mousemove', function (e) {
        var x = e.clientX / innerWidth - .5;
        ecke.style.setProperty('--al', (-32 + x * 26).toFixed(1) + 'deg');
        ecke.style.setProperty('--ar', (44 + x * 26).toFixed(1) + 'deg');
      });
    }, 2300);
  }

  /* 09 · die Uhr läuft von 19:00 bis 02:00, dahinter der Abend */
  if (v === 9) {
    var fotos = [].slice.call(h.querySelectorAll('.bx09-foto')), uhr = h.querySelectorAll('.bx09-uhr span'), balken = h.querySelector('.bx09-leiste i'), alt = -1;
    beimScrollen(function () {
      var p = fortschritt(), min = Math.round(p * 420 / 5) * 5, st = (19 + Math.floor(min / 60)) % 24, mi = min % 60;
      uhr[0].textContent = (st < 10 ? '0' : '') + st; uhr[1].textContent = (mi < 10 ? '0' : '') + mi;
      balken.style.transform = 'scaleX(' + p.toFixed(4) + ')';
      var j = Math.min(fotos.length - 1, Math.floor(p * fotos.length * .999));
      if (j !== alt) { fotos.forEach(function (f, k) { f.classList.toggle('an', k === j); }); alt = j; }
    });
  }

  /* 10 · ein Lichtkreis folgt der Maus, ohne Maus wandert er */
  if (v === 10 && !ruhig) {
    var d = h.querySelector('.bx10-dunkel'), zx = innerWidth * .6, zy = innerHeight * .45, x = zx, y = zy, zuletzt = 0, t0 = performance.now();
    h.addEventListener('mousemove', function (e) { var r = h.getBoundingClientRect(); zx = e.clientX - r.left; zy = e.clientY - r.top; zuletzt = performance.now(); });
    var bild = function (t) {
      if (t - zuletzt > 2500) { var s = (t - t0) / 1000; zx = h.offsetWidth * (.5 + .3 * Math.sin(s * .37)); zy = h.offsetHeight * (.45 + .2 * Math.sin(s * .53 + 1)); }
      x += (zx - x) * .08; y += (zy - y) * .08;
      d.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)';
      if (h.getBoundingClientRect().bottom > 0) requestAnimationFrame(bild); else setTimeout(function () { requestAnimationFrame(bild); }, 300);
    };
    requestAnimationFrame(bild);
  }

  /* 13 · Rundumblick: das Foto als Bogen um den Betrachter, der Blick schwenkt */
  if (v === 13) {
    var raum = h.querySelector('.bx13-raum'), zyl = h.querySelector('.bx13-zyl'), n = 20, bogen = 150, th = bogen / n, mx = 0, a = 0;
    var mass = function () {
      var H = raum.offsetHeight, w = H * 1.6 / n, r = w / (2 * Math.tan(th * Math.PI / 360)), p = r * 1.04;
      raum.style.setProperty('--p', p.toFixed(1) + 'px'); raum.style.setProperty('--w', w.toFixed(2) + 'px');
      raum.style.setProperty('--r', r.toFixed(1) + 'px'); raum.style.setProperty('--th', th + 'deg');
      zyl.style.setProperty('--p', p.toFixed(1) + 'px');
      var sicht = 2 * Math.atan(raum.offsetWidth / 2 / p) * 180 / Math.PI;
      raum.dataset.spiel = Math.max(0, (bogen - sicht) / 2 - 2).toFixed(1);
    };
    mass(); addEventListener('resize', mass);
    if (maus) h.addEventListener('mousemove', function (e) { mx = e.clientX / innerWidth * 2 - 1; });
    if (!ruhig) {
      var t1 = performance.now();
      var dreh = function (t) {
        var spiel = +raum.dataset.spiel, ziel = spiel * (maus && mx ? mx : Math.sin((t - t1) / 7000));
        a += (ziel - a) * .04;
        zyl.style.setProperty('--a', a.toFixed(2) + 'deg');
        requestAnimationFrame(dreh);
      };
      requestAnimationFrame(dreh);
    }
  }

  /* 14 · vier Bilder legen sich beim Scrollen übereinander */
  if (v === 14) {
    var karten = [].slice.call(h.querySelectorAll('.bx14-karte'));
    beimScrollen(function () {
      var p = fortschritt() * (karten.length - 1);
      karten.forEach(function (k, j) {
        var rein = j === 0 ? 1 : weich(0, 1, p - (j - 1)), drauf = j < karten.length - 1 ? weich(0, 1, p - j) : 0;
        k.style.transform = 'translate3d(0,' + ((1 - rein) * 112).toFixed(2) + '%,0) scale(' + (1 - .06 * drauf).toFixed(4) + ')';
      });
    });
  }

  /* 15 · die Karte dreht sich um und neigt sich mit der Maus; Klick dreht zurück */
  if (v === 15) {
    var karte = h.querySelector('[data-karte]'), um = false;
    var dreh15 = function () { um = !um; karte.style.setProperty('--flip', um ? '180deg' : '0deg'); };
    karte.addEventListener('click', dreh15);
    if (!ruhig) setTimeout(dreh15, 1900);
    if (maus && !ruhig) h.addEventListener('mousemove', function (e) {
      var x = e.clientX / innerWidth - .5, y = e.clientY / innerHeight - .5;
      karte.style.setProperty('--ry', (-16 + x * 22).toFixed(1) + 'deg'); karte.style.setProperty('--rx', (16 - y * 16).toFixed(1) + 'deg');
    });
  }
})();
