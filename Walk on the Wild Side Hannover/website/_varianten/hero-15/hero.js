/* Walk on the Wild Side · Bewegung der Auftakt-Fassungen 05, 07, 08, 10, 13, 14. Nur transform und opacity, ein Takt (requestAnimationFrame). */
(function () {
  'use strict';
  var k = document.getElementById('auftakt');
  if (!k) return;
  var ruhig = document.documentElement.classList.contains('ruhig');
  var fein = matchMedia('(hover:hover) and (pointer:fine)').matches;
  function hat(c) { return k.classList.contains(c); }
  function bereit(f) { var t = setInterval(function () { if (hat('da')) { clearInterval(t); f(); } }, 60); }
  function sichtbar() { var r = k.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }

  /* 05: bitter, sauer, rauchig, süss … und dann «was du magst.» */
  if (hat('v05')) {
    var w = [].slice.call(k.querySelectorAll('.wechsel .w')), i = -1;
    if (ruhig) { w[w.length - 1].classList.add('an'); return; }
    function weiter() {
      if (i >= 0) { var alt = w[i]; alt.classList.remove('an'); alt.classList.add('raus'); setTimeout(function () { alt.classList.remove('raus'); }, 950); }
      i = (i + 1) % w.length; w[i].classList.add('an');
      setTimeout(weiter, i === w.length - 1 ? 5200 : 1500);
    }
    bereit(function () { setTimeout(weiter, 700); });
  }

  /* 08: die Uhr zählt bis 19:00 */
  if (hat('v08')) {
    var u = k.querySelector('[data-uhr]');
    if (ruhig) { u.textContent = '19:00'; }
    else bereit(function () {
      var m = 45, t = setInterval(function () { m++; if (m >= 60) { u.textContent = '19:00'; clearInterval(t); } else u.textContent = '18:' + m; }, 85);
    });
  }

  /* 07 und 14: an den Scroll gekoppelt, ein Takt */
  if ((hat('v07') || hat('v14')) && !ruhig) {
    var tick = false, sa = k.querySelector('.sa'), sb = k.querySelector('.sb');
    function rechnen() {
      tick = false;
      var r = k.getBoundingClientRect();
      if (hat('v07')) {
        var p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
        k.style.setProperty('--s', (1 + p * p * 1.6).toFixed(4));
      } else {
        var q = Math.min(1, Math.max(0, -r.top / r.height));
        sa.style.setProperty('--ya', (-6 - q * 30).toFixed(2) + '%');
        sb.style.setProperty('--yb', (-38 + q * 30).toFixed(2) + '%');
      }
    }
    addEventListener('scroll', function () { if (!tick && sichtbar()) { tick = true; requestAnimationFrame(rechnen); } }, { passive: true });
    rechnen();
  }

  /* 10: das Schild neigt sich zur Maus */
  if (hat('v10') && fein && !ruhig) {
    var karte = k.querySelector('.hkarte');
    bereit(function () {
      setTimeout(function () { karte.classList.add('folgt'); }, 1900);
      k.addEventListener('mousemove', function (e) {
        var r = karte.getBoundingClientRect();
        var x = (e.clientX - (r.left + r.width / 2)) / innerWidth, y = (e.clientY - (r.top + r.height / 2)) / innerHeight;
        karte.style.setProperty('--ry', (x * 16).toFixed(2) + 'deg');
        karte.style.setProperty('--rx', (-y * 12).toFixed(2) + 'deg');
      });
      k.addEventListener('mouseleave', function () { karte.style.setProperty('--ry', '0deg'); karte.style.setProperty('--rx', '0deg'); });
    });
  }

  /* 13: der Lichtkegel folgt der Maus, ohne Maus wandert er langsam über die Theke */
  if (hat('v13')) {
    var raum = k.querySelector('.lampe'), kegel = k.querySelector('.kegel');
    var zx = 0, zy = 0, x = 0, y = 0, maus = 0, t0 = performance.now();
    if (fein) raum.addEventListener('mousemove', function (e) {
      var r = raum.getBoundingClientRect(); zx = e.clientX - r.left - r.width / 2; zy = e.clientY - r.top - r.height / 2; maus = performance.now();
    });
    (function lauf(now) {
      if (sichtbar()) {
        if (!fein || now - maus > 2500) {
          var r = raum.getBoundingClientRect(), s = (now - t0) / 1000;
          zx = Math.sin(s * .35) * r.width * .28; zy = Math.sin(s * .23 + 1) * r.height * .22 - r.height * .05;
        }
        x += (zx - x) * .08; y += (zy - y) * .08;
        kegel.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)';
      }
      if (!ruhig) requestAnimationFrame(lauf);
    })(t0);
  }
})();
