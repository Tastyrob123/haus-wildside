/* Wild Side · Feiern, «Wie viele seid ihr?» und «Privates Dinner», je 15 Darstellungen: die eigene Bewegung jeder Fassung.
   Nur transform und opacity, ein Scroll-Takt. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:860px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  var pin = function (el) { var r = el.getBoundingClientRect(); return kl(-r.top / Math.max(1, r.height - H())); };
  var sicht = function (el) { var r = el.getBoundingClientRect(); return r.bottom > -H() * .5 && r.top < H() * 1.5; };
  var schalte = function (liste, a) { liste.forEach(function (e, j) { e.classList.toggle('an', j === a); }); };

  var g = document.getElementById(window.VSEK || 'wieviele');
  var v = g ? g.getAttribute('data-v') : '';

  /* Beim ersten Öffnen gleich zum Abschnitt (beim Blättern mit ← → hält nav.js die Stelle) */
  var nav = false; try { nav = !!sessionStorage.getItem('vnav-da'); sessionStorage.removeItem('vnav-da'); } catch (e) {}
  addEventListener('keydown', function (ev) { if (ev.key === 'ArrowRight' || ev.key === 'ArrowLeft') try { sessionStorage.setItem('vnav-da', '1'); } catch (e) {} }, true);
  if (g && !nav && !location.hash) setTimeout(function () { if (scrollY < 40) window.scrollTo({ top: g.getBoundingClientRect().top + scrollY - 40, behavior: 'instant' }); }, 120);

  if (!v) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -16% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });

  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  function zeigen(liste, f) { liste.forEach(function (el) { ['mouseenter', 'focus'].forEach(function (t) { el.addEventListener(t, function () { f(el); }); }); }); }

  var F = {
    // Zahl als Fenster: das Bild in der Zahl zieht langsamer als die Seite
    w01: function () {
      var z = $$('.w1-z', g);
      takt.push(function () {
        if (ruhig) return;
        z.forEach(function (el) { if (!sicht(el)) return; var r = el.getBoundingClientRect(), p = (r.top + r.height / 2 - H() / 2) / H(); $('.w1-bild', el).setAttribute('transform', 'translate(0 ' + (p * 160).toFixed(1) + ')'); });
      });
    },
    // Zähler: Zahl, Format und Bild folgen dem Scrollweg
    w04: function () {
      var p0 = $('[data-pin]', g), zahl = $('.w4-zahl span', g), fs = $$('.w4-f', g), bi = $$('.w4-bild', g), sk = $('.w4-skala', g), alt = -1;
      takt.push(function () {
        if (!sicht(p0)) return; var p = pin(p0), z = Math.round(10 + p * 22);
        var t = z >= 32 ? '30+' : String(Math.min(z, 30)), a = z < 15 ? 0 : z < 24 ? 1 : 2;
        if (zahl.textContent !== t) zahl.textContent = t;
        sk.style.setProperty('--p', p.toFixed(3));
        if (a !== alt) { alt = a; schalte(fs, a); schalte(bi, a); }
      });
    },
    // Lineal: die Linie wächst bis zur Bildmitte
    w06: function () {
      var s = $('[data-lineal]', g), l = $('.w6-linie', g);
      $$('.w6-r', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });
      takt.push(function () { if (!sicht(s)) return; var r = s.getBoundingClientRect(); l.style.setProperty('--l', ruhig ? 1 : kl((H() * .62 - r.top) / r.height).toFixed(3)); });
    },
    // Plätze: Zeigen auf ein Format lässt seine Plätze leuchten
    w07: function () {
      var plan = $('.w7-plan', g), fs = $$('.w7-f', g);
      setTimeout(function () { plan.classList.add('fertig'); }, 4000);
      zeigen(fs, function (el) { schalte(fs, fs.indexOf(el)); plan.setAttribute('data-f', el.dataset.f); plan.classList.add('fertig'); });
    },
    // Ringe: Zeigen hebt den Ring und tauscht das Bild in der Mitte
    w11: function () {
      var ringe = $$('.w11-ring', g), fs = $$('.w11-f', g), bi = $$('.w11-bild', g);
      zeigen(ringe.concat(fs), function (el) { var n = +el.dataset.n; schalte(ringe, n); schalte(fs, n); schalte(bi, n); });
    },
    // Band: zieht nach links, solange die Bühne steht
    w13: function () {
      var p0 = $('[data-pin]', g), b = $('.w13-band', g), pk = $$('.w13-punkte i', g), alt = -1;
      takt.push(function () {
        if (schmal() || !sicht(p0)) return; var p = pin(p0);
        b.style.transform = 'translate3d(' + (-p * 200).toFixed(2) + 'vw,0,0)';
        var a = Math.round(p * 2); if (a !== alt) { alt = a; schalte(pk, a); }
      });
    },
    // Tisch wächst: Länge folgt dem Scrollweg, Plätze und Marken gehen an
    w14: function () {
      var f = $('[data-tisch]', g), pl = $('.w14-platte', g), st = $$('.w14-s', g), mk = $$('.w14-mk', g);
      takt.push(function () {
        if (!sicht(f)) return; var r = f.getBoundingClientRect();
        var t = ruhig ? 1 : .3 + .7 * kl((H() * .85 - r.top) / (H() * .55));
        pl.style.setProperty('--t', t.toFixed(3));
        st.forEach(function (s) { s.classList.toggle('an', +s.style.getPropertyValue('--a') <= t + .01); });
        mk.forEach(function (m) { m.classList.toggle('an', +m.style.getPropertyValue('--a') <= t + .02); });
      });
    },
    // Tafel von oben: das Bild zieht langsamer als die Seite
    d02: function () {
      var b = $('[data-par]', g), f = $('.d2-fb', g);
      takt.push(function () { if (ruhig || !sicht(b)) return; var r = b.getBoundingClientRect(), p = (r.top + r.height / 2 - H() / 2) / H(); f.style.transform = 'translate3d(0,' + (p * -9).toFixed(2) + '%,0)'; });
    },
    // Weg: die Linie wächst mit
    d03: function () {
      var s = $('[data-dweg]', g), l = $('.d3-linie', g);
      takt.push(function () { if (!sicht(s)) return; var r = s.getBoundingClientRect(); l.style.setProperty('--l', ruhig ? 1 : kl((H() * .6 - r.top) / r.height).toFixed(3)); });
    },
    // Abend läuft: der Gang in der Mitte bestimmt das Bild links
    d08: function () {
      var gs = $$('.d8-g', g), bi = $$('.d8-bild', g), alt = 0;
      takt.push(function () {
        if (!sicht(g)) return; var a = 0;
        gs.forEach(function (el, j) { if (el.getBoundingClientRect().top < H() * .55) a = j; });
        if (a !== alt) { alt = a; schalte(gs, a); schalte(bi, a); }
      });
    },
    // Band der Teller: zieht nach links, solange es durchs Bild läuft
    d10: function () {
      var f = $('[data-band]', g), b = $('.d10-band', g);
      takt.push(function () {
        if (ruhig || !sicht(f)) return; var r = f.getBoundingClientRect();
        var p = kl((H() - r.top) / (H() + r.height)), weit = Math.max(0, b.scrollWidth - innerWidth);
        b.style.transform = 'translate3d(' + (-p * weit).toFixed(1) + 'px,0,0)';
      });
    },
    // Tafel quer: das Bild läuft im Streifen mit
    d13: function () {
      var f = $('[data-quer]', g), b = $('.d13-bild', g);
      takt.push(function () {
        if (ruhig || !sicht(f)) return; var r = f.getBoundingClientRect(), p = (r.top + r.height / 2 - H() / 2) / H();
        b.style.setProperty('--y', (p * -14).toFixed(2) + 'vw');
      });
    }
  };
  if (F[v.slice(0, 1) + v.slice(1)]) F[v]();
  lauf();
})();
