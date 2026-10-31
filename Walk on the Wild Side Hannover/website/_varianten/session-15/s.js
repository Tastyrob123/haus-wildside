/* Wild Side · Programm, «Jeder Abend ein Plakat.», 15 Darstellungen: die eigene Bewegung jeder Fassung. Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };
  var mitte = function (el) { var r = el.getBoundingClientRect(); return (r.top + r.height / 2 - H() / 2) / H(); };

  var g = document.getElementById('session'), n = g ? +g.getAttribute('data-s') || 0 : 0;
  if (!n) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -18% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  var schalte = function (liste, a) { liste.forEach(function (e, j) { e.classList.toggle('an', j === a); }); };

  var F = {
    // Stapel: je Abschnitt des Scrollwegs ein Plakat weg
    2: function () {
      var p0 = $('[data-pin]', g), pl = $$('.w2-p', g), tx = $$('.w2-t', g), z = $('.w2-zahl b', g), alt = -1;
      takt.push(function () {
        if (!sicht(p0)) return; var a = Math.min(pl.length - 1, Math.floor(pin(p0) * pl.length));
        if (a === alt) return; alt = a;
        pl.forEach(function (e, j) { e.classList.toggle('weg', j < a); }); schalte(tx, a); z.textContent = a + 1;
      });
    },
    // Band: zieht nach links, solange der Abschnitt durchs Bild läuft
    3: function () {
      var f = $('[data-band]', g), b = $('.w3-band', g);
      takt.push(function () {
        if (schmal() || ruhig || !sicht(f)) return; var r = f.getBoundingClientRect();
        var p = kl((H() - r.top) / (H() + r.height)), weit = Math.max(0, b.scrollWidth - innerWidth);
        b.style.transform = 'translate3d(' + (-p * weit).toFixed(1) + 'px,0,0)';
      });
    },
    // Zeitstrahl: die Linie wächst bis zur Bildmitte
    4: function () {
      var s = $('[data-strahl]', g), l = $('.w4-linie', g);
      takt.push(function () { if (!sicht(s)) return; var r = s.getBoundingClientRect(); l.style.setProperty('--l', ruhig ? 1 : kl((H() * .62 - r.top) / r.height).toFixed(3)); });
    },
    // Fächer: Zeigen wechselt Datum und Name darunter
    5: function () {
      var st = $('.w5-satz', g), d = $('.w5-dat', g), nm = $('.w5-name', g), pl = $$('.w5-p', g), t = 0;
      pl.forEach(function (p) {
        var w = function () {
          pl.forEach(function (x) { x.classList.toggle('an', x === p); }); st.classList.add('weg'); clearTimeout(t);
          t = setTimeout(function () { d.textContent = p.dataset.dat; nm.textContent = p.dataset.name; st.classList.remove('weg'); }, 180);
        };
        p.addEventListener('mouseenter', w); p.addEventListener('click', w);
      });
      pl[pl.length - 1].classList.add('an');
    },
    // Kontaktbogen: das grosse sinkt weg, das neue steigt auf
    7: function () {
      var gr = $$('.w7-g', g), nm = $('.w7-name', g), dt = $('.w7-dat', g), kl_ = $$('.w7-k', g);
      kl_.forEach(function (k) {
        var w = function () {
          if (k.classList.contains('an')) return; schalte(kl_, kl_.indexOf(k));
          gr.forEach(function (b) { var an = b.dataset.k === k.dataset.k; if (b.classList.contains('an') && !an) { b.classList.remove('an'); b.classList.add('raus'); setTimeout(function () { b.classList.remove('raus'); }, 800); } b.classList.toggle('an', an); });
          nm.textContent = k.dataset.name; dt.textContent = k.dataset.dat;
        };
        k.addEventListener('mouseenter', w); k.addEventListener('click', w);
      });
    },
    // Heft: die Karte dreht sich, das neue Plakat liegt auf der gerade abgewandten Seite
    8: function () {
      var karte = $('[data-karte]', g), seiten = [$('.w8-vorn .sp img', g), $('.w8-hinten .sp img', g)], fig = [$('.w8-vorn .sp', g), $('.w8-hinten .sp', g)];
      var q = {}, lq = {}; $$('[data-quellen] img', g).forEach(function (i) { q[i.dataset.k] = i.dataset.src; lq[i.dataset.k] = i.dataset.lq; });
      var unter = $('.w8-unter', g), b = $('b', unter), s = $('small', unter), zl = $$('.w8-liste>div', g), dreh = 0, jetzt = zl[0].dataset.k, t = 0;
      zl.forEach(function (z) {
        var w = function () {
          schalte(zl, zl.indexOf(z)); unter.classList.add('weg'); clearTimeout(t);
          t = setTimeout(function () { b.textContent = z.dataset.name; s.textContent = z.dataset.dat; unter.classList.remove('weg'); }, 220);
          if (z.dataset.k === jetzt) return; jetzt = z.dataset.k;
          var hinten = (dreh + 1) % 2; seiten[hinten].removeAttribute('srcset'); seiten[hinten].src = q[jetzt];
          fig[hinten].style.setProperty('--lq', 'url(' + lq[jetzt] + ')');
          dreh++; karte.style.setProperty('--dreh', dreh);
        };
        z.addEventListener('mouseenter', w); z.addEventListener('click', w);
      });
    },
    // Letzter Abend: Zeigen holt einen Abend nach vorn
    10: function () {
      var gr = $$('.w10-g', g), ks = $$('.w10-k', g), li = $('.w10-links', g), dat = $('.w10-dat', g), jahr = $('.w10-jahr', g), nm = $('.w10-name', g), r = $('.w10-r', g), t = 0;
      ks.forEach(function (k) {
        var w = function () {
          if (k.classList.contains('an')) return; schalte(ks, ks.indexOf(k));
          gr.forEach(function (b) { b.classList.toggle('an', b.dataset.k === k.dataset.k); });
          li.classList.add('weg'); clearTimeout(t);
          var d = k.dataset.dat; dat.innerHTML = d.split('').map(function (c, i) { return '<span style="--b:' + i + ';opacity:0;transform:translateY(-60px)">' + c + '</span>'; }).join('');
          requestAnimationFrame(function () { requestAnimationFrame(function () { $$('span', dat).forEach(function (s) { s.style.opacity = ''; s.style.transform = ''; }); }); });
          t = setTimeout(function () { var full = $('p', k).textContent; jahr.textContent = k.querySelector('p span').textContent.slice(6); nm.textContent = k.dataset.name; r.textContent = k.dataset.r; li.classList.remove('weg'); }, 200);
        };
        k.addEventListener('mouseenter', w); k.addEventListener('click', w);
      });
    },
    // Tiefe: die Plakate fahren auf den Betrachter zu und an ihm vorbei
    12: function () {
      var p0 = $('[data-pin]', g), pl = $$('.w12-p', g), m = pl.length;
      takt.push(function () {
        if (!sicht(p0)) return; var p = ruhig ? 1 : pin(p0), s = schmal() ? .45 : 1;
        pl.forEach(function (e, j) {
          var z = (p * (m - .2) - j) * 900, x = +e.style.getPropertyValue('--x') * innerWidth * .2 * s;
          var o = z > 600 ? kl(1 - (z - 600) / 250) : kl(1 + z / 3200);
          e.style.transform = 'translate3d(' + x.toFixed(1) + 'px,0,' + Math.min(z, 860).toFixed(1) + 'px)';
          e.style.opacity = o.toFixed(3); e.style.zIndex = Math.round(z + 4000);
        });
      });
    },
    // Litfasssäule: dreht mit dem Scrollen, vorn wechselt der Abend
    13: function () {
      var o = $('[data-saeule]', g), s = $('.w13-saeule', g), tx = $$('.w13-t', g), m = tx.length, alt = -1;
      takt.push(function () {
        if (!sicht(o)) return; var d = ruhig ? 0 : -(mitte(o) + .6) * 300;
        s.style.setProperty('--d', d.toFixed(1));
        var a = ((Math.round(-d / (360 / m)) % m) + m) % m; if (a !== alt) { alt = a; schalte(tx, a); }
      });
    },
    // Folgt der Hand: Plakat schwebt weich hinter dem Zeiger her
    14: function () {
      var f = $('.w14-folg', g), fs = $$('.w14-f', g), zl = $$('.w14-z', g), x = 0, y = 0, tx = 0, ty = 0, an = false, raf = 0;
      function zieh() { x += (tx - x) * .16; y += (ty - y) * .16; f.style.transform = 'translate3d(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px,0)'; raf = an || Math.abs(tx - x) > .5 ? requestAnimationFrame(zieh) : 0; }
      zl.forEach(function (z) {
        z.addEventListener('mouseenter', function (e) { fs.forEach(function (b) { b.classList.toggle('an', b.dataset.k === z.dataset.k); }); if (!an) { x = tx; y = ty; } an = true; f.classList.add('an'); if (!raf) raf = requestAnimationFrame(zieh); });
      });
      $('.w14-liste', g).addEventListener('mouseleave', function () { an = false; f.classList.remove('an'); });
      addEventListener('mousemove', function (e) { tx = e.clientX + 40; ty = e.clientY - f.offsetHeight * .5; }, { passive: true });
    },
    // Im Plakat: die Wellen ziehen langsamer als die Seite
    15: function () {
      var fl = $('[data-wellen]', g), w = $('.w15-wellen', g);
      takt.push(function () { if (ruhig || !sicht(fl)) return; w.style.transform = 'translate3d(0,' + (mitte(fl) * -120).toFixed(1) + 'px,0)'; });
    }
  };
  if (F[n]) F[n]();
  lauf();
})();
