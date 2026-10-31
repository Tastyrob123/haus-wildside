/* Wild Side · Feiern, «Grosse Events · Grösser als die Bar.»: die eigene Bewegung jeder Fassung.
   Nur transform, ein Scroll-Takt, nativer Scroll. */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return [].slice.call((c || document).querySelectorAll(s)); };
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:860px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var H = function () { return innerHeight; };
  // 0, wenn die Oberkante unten am Rand auftaucht, 1, wenn die Unterkante oben verschwindet
  var durch = function (el) { var r = el.getBoundingClientRect(); return kl((H() - r.top) / (H() + r.height)); };
  // 0, wenn die Oberkante unten auftaucht, 1, wenn sie die Mitte erreicht
  var herein = function (el, bis) { var r = el.getBoundingClientRect(); return kl((H() - r.top) / (H() * (bis || .5))); };

  var g = document.getElementById('events');
  var v = g ? g.getAttribute('data-v') : '';

  /* Beim ersten Öffnen gleich zum Abschnitt (beim Blättern mit ← → hält nav.js die Stelle) */
  var nav = false; try { nav = !!sessionStorage.getItem('vnav-da'); sessionStorage.removeItem('vnav-da'); } catch (e) {}
  addEventListener('keydown', function (ev) { if (ev.key === 'ArrowRight' || ev.key === 'ArrowLeft') try { sessionStorage.setItem('vnav-da', '1'); } catch (e) {} }, true);
  if (g && !nav && !location.hash) setTimeout(function () { if (scrollY < 40) window.scrollTo({ top: g.getBoundingClientRect().top + scrollY - 40, behavior: 'instant' }); }, 120);

  if (!v) return;
  $$('img[data-srcset]', g).forEach(function (img) { img.sizes = img.dataset.sizes || '100vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); });

  var io = 'IntersectionObserver' in window && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('ok'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px 8% 0px' }) : null;
  $$('.vauf', g).forEach(function (el) { io ? io.observe(el) : el.classList.add('ok'); });
  if (ruhig) return;

  var takt = [];
  var F = {
    // Die Goldlinie zieht sich von der Bar zur Loge
    e01: function () { var w = $('.e1-weg', g), l = $('.e1-linie', g); return function () { l.style.setProperty('--p', herein(w, .7).toFixed(3)); }; },
    // Der Titel wächst beim Hereinscrollen auf volle Grösse
    e02: function () { var t = $('.e2-titel .titel', g); return function () { t.style.setProperty('--s', (.86 + .14 * herein(t, .55)).toFixed(4)); }; },
    // Jedes Bild zoomt im Vorbeiziehen aus seinem Rahmen zurück
    e03: function () { var b = $$('.e3-b', g); return function () { b.forEach(function (f) { f.style.setProperty('--z', (1.12 - .12 * herein(f, .7)).toFixed(4)); }); }; },
    // Die Reihe wandert ein Stück nach links
    e07: function () { var r = $('.e7-reihe', g), z = $('.e7-zug', g); return function () { z.style.setProperty('--x', (schmal() ? 0 : (4 - 12 * durch(r))).toFixed(2) + '%'); }; },
    // Das Bild gleitet langsamer als die Seite
    e08: function () { var b = $('.e8-bild', g); return function () { b.style.setProperty('--y', ((schmal() ? 0 : 90 - 180 * durch(b.parentNode))).toFixed(1) + 'px'); }; },
    // Aus der Nähe in den Raum
    e09: function () { var b = $('.e9-bild', g); return function () { b.style.setProperty('--z', (1.22 - .22 * herein(b, .75)).toFixed(4)); }; },
    // Die Abzüge legen sich nebeneinander
    e10: function () { var t = $('.e10-tisch', g); return function () { t.style.setProperty('--p', herein(t, .8).toFixed(3)); }; },
    // Das Foto zieht im Rahmen langsamer
    e12: function () { var b = $('.e12-bild', g), i = $('.e12-bild img', g); return function () { i.style.setProperty('--y', (6 - 12 * durch(b)).toFixed(2) + '%'); }; },
    // Die Reihe fährt von der Bar zur Loge, solange der Abschnitt steht
    e14: function () {
      var z = $('.e14-zug', g);
      return function () {
        if (schmal()) return;
        var r = g.getBoundingClientRect(), p = kl(-r.top / Math.max(1, r.height - H()));
        var l = z.lastElementChild, ende = l.offsetLeft + l.offsetWidth + parseFloat(getComputedStyle(z).paddingLeft);
        z.style.setProperty('--x', (-p * Math.max(0, ende - innerWidth)).toFixed(1) + 'px');
      };
    },
    // Das Foto gleitet in der Säule
    e15: function () { var s = $('.e15-saeule', g), b = $('.e15-bild', g); return function () { b.style.setProperty('--y', (-10.7 * durch(s)).toFixed(2) + '%'); }; }
  };
  if (F[v]) takt.push(F[v]());
  if (!takt.length) return;
  var tick = false;
  function lauf() { tick = false; if (g.getBoundingClientRect().bottom < -H() || g.getBoundingClientRect().top > 2 * H()) return; takt.forEach(function (f) { f(); }); }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  lauf();
})();
