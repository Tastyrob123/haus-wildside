/* Walk on the Wild Side · Laden, Auftritte, Leiste, «heute», das Gespräch, Flyer-Wechsel, Vorführ-Formulare. Nur transform und opacity, nativer Scroll. */
(function () {
  'use strict';
  var html = document.documentElement;
  var ruhig = html.classList.contains('ruhig');
  var IO = 'IntersectionObserver' in window;
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  /* ---------- Bilder: drei Bildschirme voraus, danach alles Übrige im Leerlauf */
  function laden(img) {
    if (!img.dataset.srcset) return;
    img.sizes = img.dataset.sizes || '100vw';
    img.srcset = img.dataset.srcset;
    img.removeAttribute('data-srcset');
  }
  var lader = IO ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { laden(e.target); lader.unobserve(e.target); } });
  }, { rootMargin: '300% 0px 300% 0px' }) : null;
  document.querySelectorAll('img[data-srcset]').forEach(function (img) { lader ? lader.observe(img) : laden(img); });
  addEventListener('load', function () {
    var rest = [].slice.call(document.querySelectorAll('img[data-srcset]'));
    var idle = window.requestIdleCallback || function (f) { return setTimeout(f, 200); };
    (function weiter() { if (!rest.length) return; idle(function () { for (var n = 0; n < 3 && rest.length; n++) laden(rest.shift()); weiter(); }); })();
  });

  /* ---------- Auftritte: sobald der Bereich den Rand berührt, einmal, man sieht sie noch hereinkommen */
  var auf = IO && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); auf.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -6% 0px' }) : null;
  document.querySelectorAll('.auf').forEach(function (el) { auf ? auf.observe(el) : el.classList.add('da'); });
  /* Der Auftakt geht von selbst auf, sobald sein Bild da ist (Rückfall: nach 900 ms) */
  var auftakt = document.getElementById('auftakt');
  if (auftakt) {
    var bild = auftakt.querySelector('img'), an = false;
    function los() { if (an) return; an = true; auftakt.classList.add('da'); }
    if (bild && bild.complete) setTimeout(los, 60); else if (bild) bild.addEventListener('load', function () { setTimeout(los, 60); });
    setTimeout(los, 900);
  }
  /* Fenster: der Satz rollt, sobald die Oberkante bei 38 % der Höhe steht */
  var fe = IO && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); fe.unobserve(e.target); } });
  }, { rootMargin: '-38% 0px 0px 0px', threshold: 0 }) : null;
  document.querySelectorAll('.fenster .zl').forEach(function (el) { fe ? fe.observe(el) : el.classList.add('da'); });
  /* Mosaik: setzt sich, sobald das Bild ein Stück hereingekommen ist (früh, damit nichts wartet) */
  var mo = IO && !ruhig ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); mo.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -15% 0px' }) : null;
  document.querySelectorAll('.gewoelbe').forEach(function (el) { mo ? mo.observe(el) : el.classList.add('da'); });

  /* ---------- Leiste: im Auftakt nie, danach beim Hinaufscrollen; auf Unterseiten oben sichtbar, weg beim Hinunterscrollen */
  var leiste = document.getElementById('leiste');
  if (leiste) {
    var y0 = scrollY, richt = 0, anker = y0, tick = false;
    var grenze = auftakt ? function () { return auftakt.offsetHeight - leiste.offsetHeight; } : function () { return 120; };
    function rechnen() {
      var y = scrollY;
      if ((y - y0) * richt < 0 || (!richt && y !== y0)) { richt = y > y0 ? 1 : -1; anker = y0; }
      var runter = richt > 0 && y - anker > 24, hoch = richt < 0 && anker - y > 24;
      if (auftakt) { if (y < grenze() || runter) leiste.classList.add('weg'); else if (hoch) leiste.classList.remove('weg'); }
      else { if (y < grenze() || hoch) leiste.classList.remove('weg'); else if (runter && y > 200) leiste.classList.add('weg'); }
      y0 = y; tick = false;
    }
    if (auftakt) leiste.classList.add('weg');
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechnen); } }, { passive: true });
  }

  /* ---------- Heute: welcher Abend ist heute, oder wann wieder offen (Do 19–1, Fr/Sa 19–2) */
  function heute() {
    var d = new Date(), t = d.getDay(), h = d.getHours();
    var offen = { 4: [19, 25], 5: [19, 26], 6: [19, 26] };
    var tagName = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
    var abend = t, satz;
    var gestern = (t + 6) % 7;
    if (offen[gestern] && h < offen[gestern][1] - 24) { abend = gestern; satz = 'Noch offen bis ' + (offen[gestern][1] - 24) + ' Uhr'; }
    else if (offen[t]) { satz = h < 19 ? 'Heute ab 19 Uhr' : (h < offen[t][1] - 24 || h >= 19 ? 'Jetzt offen, bis ' + (offen[t][1] - 24) + ' Uhr' : 'Heute ab 19 Uhr'); }
    else { var n = t, k = 0; while (!offen[n]) { n = (n + 1) % 7; k++; } abend = n; satz = (k === 1 ? 'Morgen' : 'Am ' + tagName[n]) + ' wieder ab 19 Uhr'; }
    document.querySelectorAll('[data-heute-satz]').forEach(function (el) { el.textContent = satz; });
    document.querySelectorAll('[data-tag]').forEach(function (el) {
      var tage = el.dataset.tag.split(',');
      var ist = tage.indexOf(String(abend)) >= 0 && offen[abend];
      el.classList.toggle('heute', !!ist);
      var j = el.querySelector('.jetzt'); if (j) j.textContent = ist ? 'heute' : '';
    });
  }
  heute();

  /* ---------- Das Gespräch: drei Wahlzeilen, ein Antwortsatz, das Glas tauscht an derselben Stelle */
  document.querySelectorAll('[data-gespraech]').forEach(function (g) {
    var wahl = {}, satz = g.querySelector('.ge-satz'), glas = g.querySelector('.ge-glas');
    var antworten = JSON.parse(g.dataset.gespraech);
    function finde() {
      for (var i = 0; i < antworten.length; i++) {
        var a = antworten[i], ok = true;
        for (var k in a.wenn) if (a.wenn[k] !== wahl[k]) ok = false;
        if (ok) return a;
      }
      return antworten[antworten.length - 1];
    }
    var zuletzt = null;
    function zeige() {
      var a = finde();
      if (zuletzt === a) return; zuletzt = a;
      satz.classList.add('wechsel');
      satz.innerHTML = a.satz.split('|').map(function (z) { return '<span class="z"><span>' + z + '</span></span>'; }).join('');
      void satz.offsetWidth; satz.classList.remove('wechsel');
      if (glas && a.bild) {
        var neu = glas.querySelector('[data-k="' + a.bild + '"]'), alt = glas.querySelector('.foto.an');
        if (neu && neu !== alt) {
          glas.querySelectorAll('.foto.war').forEach(function (f) { f.classList.remove('war'); });
          if (alt) { alt.classList.remove('an'); alt.classList.add('war'); }
          var img = neu.querySelector('img[data-srcset]'); if (img) laden(img);
          neu.classList.add('an');
          setTimeout(function () { glas.querySelectorAll('.foto.war').forEach(function (f) { if (f !== neu) f.classList.remove('war'); }); }, 1300);
        }
      }
    }
    g.querySelectorAll('.wahl').forEach(function (w) {
      var name = w.dataset.frage;
      w.querySelectorAll('button').forEach(function (b) {
        b.addEventListener('click', function () {
          w.querySelectorAll('button').forEach(function (x) { x.classList.remove('an'); });
          b.classList.add('an'); wahl[name] = b.dataset.w; zeige();
        });
      });
    });
    /* Anfangs die erste Wahl jeder Zeile, damit nie eine leere Antwort steht */
    g.querySelectorAll('.wahl').forEach(function (w) { var b = w.querySelector('button'); if (b) { b.classList.add('an'); wahl[w.dataset.frage] = b.dataset.w; } });
    zeige();
  });

  /* ---------- An der Theke: die Goldlinie läuft beim Scrollen mit, jeder erreichte Schritt bekommt seinen Punkt (nur solange der Weg im Bild ist).
     Sie endet im Knopf «Alle Drinks»: kommt sie dort an, wird der Abschnitt «frei» (Knopf leuchtet, der Satz darunter fliegt herein), wie beim Rivage. */
  document.querySelectorAll('[data-weg]').forEach(function (weg) {
    var linie = weg.querySelector('.th-linie i'), st = [].slice.call(weg.querySelectorAll('.th-st')), im = !IO, tick = false, sek = weg.closest('section');
    if (ruhig) { st.forEach(function (s) { s.classList.add('an'); }); if (sek) sek.classList.add('frei'); return; }
    /* Die Linie beginnt im ersten Punkt, nicht oben im Leeren (Robert 29.10.2026: «dass diese gelbe Linie so aus dem Nichts losgeht») */
    var bahn = linie.parentNode, erster = weg.querySelector('.th-punkt');
    function anfang() {
      if (!erster) return;
      var pr = erster.getBoundingClientRect();
      bahn.style.top = Math.round(pr.top + pr.height / 2 - weg.getBoundingClientRect().top) + 'px';
    }
    anfang(); addEventListener('load', anfang);
    function rechne() {
      tick = false;
      var h = innerHeight, r = weg.getBoundingClientRect(), b = bahn.getBoundingClientRect();
      if (sek && r.bottom < h * .62) sek.classList.add('frei');
      if (!im) return;
      var p = Math.max(0, Math.min(1, (h * .6 - b.top) / b.height));
      linie.style.transform = 'scaleY(' + p.toFixed(4) + ')';
      st.forEach(function (s) { s.classList.toggle('an', s.getBoundingClientRect().top + s.offsetHeight / 2 < h * .6); });
    }
    if (IO) new IntersectionObserver(function (es) { im = es[0].isIntersecting; if (im) rechne(); }).observe(weg);
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechne); } }, { passive: true });
    addEventListener('resize', function () { anfang(); rechne(); });
    rechne();
  });

  /* ---------- Drinks, «Das Gespräch» bis «Wie Momo arbeitet»: drei Goldlinien, die beim Scrollen mitlaufen und eine Station nach der anderen erreichen.
     Die mittlere führt in den Satz «Und so entsteht daraus ein Drink.» (Robert 29.10.2026, Fassung 01). */
  document.querySelectorAll('[data-w1]').forEach(function (w) {
    var linie = w.querySelector('.w1-linie i'), st = [].slice.call(w.querySelectorAll('.w1-st')), im = !IO, tick = false;
    if (ruhig) { linie.style.transform = 'none'; st.forEach(function (s) { s.classList.add('an'); }); return; }
    function rechne() {
      tick = false;
      if (!im) return;
      var h = innerHeight, r = w.getBoundingClientRect();
      linie.style.transform = 'scaleY(' + Math.max(0, Math.min(1, (h * .6 - r.top) / r.height)).toFixed(4) + ')';
      st.forEach(function (s) { var q = s.getBoundingClientRect(); s.classList.toggle('an', q.top + q.height / 2 < h * .6); });
    }
    if (IO) new IntersectionObserver(function (es) { im = es[0].isIntersecting; if (im) rechne(); }).observe(w);
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(rechne); } }, { passive: true });
    addEventListener('resize', rechne);
    rechne();
  });

  /* ---------- Kontaktbogen der DJ-Abende: Zeigen auf ein kleines Plakat, das grosse sinkt weg, das neue steigt auf */
  document.querySelectorAll('[data-kontaktbogen]').forEach(function (bogen) {
    var sek = bogen.closest('section'), gr = [].slice.call(sek.querySelectorAll('.kb-g')), kl = [].slice.call(bogen.querySelectorAll('.kb-k'));
    var nm = sek.querySelector('.kb-name'), dt = sek.querySelector('.kb-dat');
    kl.forEach(function (k) {
      function waehle() {
        if (k.classList.contains('an')) return;
        kl.forEach(function (x) { x.classList.toggle('an', x === k); });
        gr.forEach(function (b) {
          var an = b.dataset.k === k.dataset.k, img = b.querySelector('img[data-srcset]'); if (an && img) laden(img);
          if (b.classList.contains('an') && !an) { b.classList.add('raus'); setTimeout(function () { b.classList.remove('raus'); }, 800); }
          b.classList.toggle('an', an);
        });
        nm.textContent = k.dataset.name; dt.textContent = k.dataset.dat;
      }
      k.addEventListener('mouseenter', waehle); k.addEventListener('click', waehle);
    });
  });

  /* ---------- Vorführ-Formulare: verschicken nichts, danken nur */
  document.querySelectorAll('form[data-vorfuehrung]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); f.classList.add('fertig'); });
  });

  /* ---------- Aufklappen: immer nur eine Frage offen */
  document.querySelectorAll('.fragen').forEach(function (fr) {
    fr.querySelectorAll('details').forEach(function (d) {
      d.addEventListener('toggle', function () { if (d.open) fr.querySelectorAll('details[open]').forEach(function (x) { if (x !== d) x.open = false; }); });
    });
  });

  /* Fenster in fester Grösse: das Bild zeigt sich nur, wenn das Fenster nah ist; der Satz rollt, sobald die Oberkante bei 62 % der Höhe steht */
  document.querySelectorAll('.fk').forEach(function (f) {
    var z = f.querySelector('.zl');
    if (!IO) { f.classList.add('an'); z.classList.add('da'); return; }
    new IntersectionObserver(function (es) { es.forEach(function (e) { f.classList.toggle('an', e.isIntersecting); }); }, { rootMargin: '15% 0px 15% 0px' }).observe(f);
    if (ruhig) { z.classList.add('da'); return; }
    var o = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { z.classList.add('da'); o.disconnect(); } }); }, { rootMargin: '0px 0px -38% 0px' });
    o.observe(f);
  });
})();

/* ---------- Bewegung wie im Culinarium (Robert 29.10.2026: «so schwach, man merkt das irgendwie kaum»). Vorher ging ein ganzer Abschnitt auf einmal auf,
   meist bevor man hinsah. Jetzt tritt jedes Bild, jede Zeile, jeder Block einzeln auf, wenn er selbst ins Bild kommt. In Ruhe bleibt jeder Bildausschnitt
   wie vorher (das Gleiten mit Vorzoom ist raus, es schnitt die Bilder enger an). Stand davor *.vor-bewegung-2026-10-29 */
(function () {
  'use strict';
  var html = document.documentElement;
  if (html.classList.contains('ruhig') || !('IntersectionObserver' in window)) return;
  /* Bereiche mit eigener Bewegung bleiben, wie sie sind */
  var EIGEN = '.fr-kopf,.fr-strahl,.fr-menue,.fr-dbilder,.fr-zahlen,.fr-bbild,.fr-treppe,.fr-posten,.fr-huellen,.fr-team,.auftakt,.gewoelbe,.vitrine,.fk,.fenster,[data-gespraech],.ge-glas,.flyer,.dg-zug,.wb-band-zug';
  function frei(el) { return !el.closest(EIGEN); }
  var alle = [];
  [].slice.call(document.querySelectorAll('.auf .sw,.sw.auf,.auf .staffel>*,.auf .flaeche>*')).filter(frei).forEach(function (el) {
    if (el.classList.contains('einz')) return; el.classList.add('einz', 'blk'); alle.push(el);
  });
  [].slice.call(document.querySelectorAll('.auf .zl')).filter(frei).forEach(function (el) { el.classList.add('einz'); alle.push(el); });
  [].slice.call(document.querySelectorAll('.foto,.kachel')).filter(frei).forEach(function (el) {
    if (!el.querySelector('img')) return;
    el.classList.add('einz', 'bild'); alle.push(el);
    /* Steigt der Block drumherum schon, zoomt das Bild nur; sonst steigt der Rahmen selbst hoch (Wand: hat eigene Bewegung) */
    if (!el.closest('.blk') && !el.closest('.wand')) el.classList.add('heben');
  });
  if (!alle.length) return;
  html.classList.add('einzeln');
  var io = new IntersectionObserver(function (es) {
    var k = 0;
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target; io.unobserve(el);
      el.style.setProperty('--e', Math.min(k++, 3));
      el.classList.add('ein'); if (el.classList.contains('bild')) el.classList.add('da');
    });
  }, { rootMargin: '0px 0px 120px 0px', threshold: 0 });
  alle.forEach(function (el) { io.observe(el); });

})();

/* Drinks · Faden «Frage und Antwort» (Wahl Robert 30.10.2026): --p je Schritt von 0 (Oberkante bei 95 % der Höhe) bis 1 (bei 30 %), Momos Satz Wort für Wort. */
(function () {
  'use strict';
  var g = document.querySelector('section.gx[data-g]'); if (!g) return;
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:760px)').matches; };
  var kl = function (x) { return x < 0 ? 0 : x > 1 ? 1 : x; };
  var takt = [], tick = false;
  function lauf() { tick = false; takt.forEach(function (f) { f(); }); }
  [].slice.call(g.querySelectorAll('[data-p]')).forEach(function (s) {
    var w = [].slice.call(s.querySelectorAll('.ww')), alt = -1;
    takt.push(function () {
      var p = 1, H = innerHeight;
      if (!ruhig && !schmal()) { var r = s.getBoundingClientRect(); if (r.top > 1.4 * H || r.bottom < -.4 * H) return; p = kl((.95 * H - r.top) / (.65 * H)); }
      var q = Math.round(p * 1000) / 1000; if (q === alt) return; alt = q;
      s.style.setProperty('--p', q);
      if (w.length) { var n = Math.ceil(kl(p * 1.15) * w.length); w.forEach(function (x, i) { x.classList.toggle('an', i < n); }); }
    });
  });
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf);
  lauf();
})();

/* Programm · Die Woche (Wahl Robert 30.10.2026): die Ringe der drei Deckel drehen beim Scrollen weiter, abwechselnd links und rechts herum. */
(function () {
  'use strict';
  var s = [].slice.call(document.querySelectorAll('#woche [data-ring]')); if (!s.length) return;
  if (document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var tick = false;
  function lauf() {
    tick = false; var H = innerHeight;
    s.forEach(function (e, j) {
      var r = e.getBoundingClientRect(); if (r.bottom < -.5 * H || r.top > 1.5 * H) return;
      e.querySelector('.wo-ring').style.setProperty('--r', (((r.top + r.height / 2 - H / 2) / H) * (j % 2 ? 110 : -110)).toFixed(1));
    });
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', lauf); lauf();
})();


/* Feiern · «So geht es» als Goldlinie (Wahl Robert 30.10.2026): die Linie folgt dem Scrollen, 0 bei Oberkante auf 85 % der Höhe, 1 bei 25 %;
   jede Station leuchtet, sobald die Linie sie erreicht. Schmal und in Ruhe sind alle Stationen an. */
(function () {
  'use strict';
  var weg = document.querySelector('.gl-weg'); if (!weg) return;
  var li = weg.querySelector('.gl-linie'), st = [].slice.call(weg.querySelectorAll('.gl-st')), pk = weg.querySelector('.gl-p');
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  var schmal = function () { return matchMedia('(max-width:900px)').matches; };
  function lage() { li.style.setProperty('--lt', (pk.offsetTop + 6) + 'px'); }
  lage(); addEventListener('resize', lage);
  if (ruhig) { li.style.setProperty('--p', 1); st.forEach(function (s) { s.classList.add('an'); }); return; }
  var tick = false, alt = -1;
  function lauf() {
    tick = false;
    var r = weg.getBoundingClientRect(), H = innerHeight;
    if (r.top > 1.3 * H || r.bottom < -.3 * H) return;
    var q = Math.max(0, Math.min(1, (.85 * H - r.top) / (.6 * H))); q = Math.round(q * 1000) / 1000;
    if (q === alt) return; alt = q;
    li.style.setProperty('--p', q);
    st.forEach(function (s, i) { s.classList.toggle('an', q >= i / 4 + .02 || schmal()); });
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', function () { alt = -1; lauf(); });
  lauf();
})();

/* Feiern · Weg 2 Budget: die Rückbar rückt beim Scrollen in ihrem Rahmen ruhig näher (30.10.2026). Nur transform. */
(function () {
  'use strict';
  var f = document.querySelector('#budget [data-nah]'); if (!f) return;
  var b = f.querySelector('img');
  if (document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var tick = false, alt = -1;
  function lauf() {
    tick = false;
    var r = f.getBoundingClientRect(), H = innerHeight;
    if (r.bottom < -.3 * H || r.top > 1.3 * H) return;
    var q = Math.max(0, Math.min(1, (H - r.top) / (H * 1.4))); q = Math.round(q * 1000) / 1000;
    if (q === alt) return; alt = q;
    b.style.transform = 'scale(' + (1.16 - q * .16).toFixed(4) + ')';
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', function () { alt = -1; lauf(); });
  lauf();
})();

/* Grosse Events (Feiern): die drei Abzüge legen sich beim Hereinscrollen nebeneinander (Fassung 10, 30.10.2026). Nur transform. */
(function () {
  var t = document.querySelector('.fr-tisch');
  if (!t) return;
  if (document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches) { t.style.setProperty('--p', 1); return; }
  var tick = false, alt = -1;
  function lauf() {
    tick = false;
    var r = t.getBoundingClientRect(), H = innerHeight;
    if (r.bottom < -.3 * H || r.top > 1.3 * H) return;
    var q = Math.max(0, Math.min(1, (H - r.top) / (H * .8))); q = Math.round(q * 1000) / 1000;
    if (q === alt) return; alt = q;
    t.style.setProperty('--p', q);
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', function () { alt = -1; lauf(); });
  lauf();
})();

/* Feiern, Anfragen: die Tafel am Team-Bild läuft beim Scrollen schneller (--p 0…1 bis zur Mitte des Bildschirms) */
(function () {
  var t = document.querySelector('.fr-team[data-p]'); if (!t) return;
  var tick = false, alt = -1;
  function lauf() {
    tick = false;
    var r = t.getBoundingClientRect(), H = innerHeight;
    if (r.bottom < -.3 * H || r.top > 1.3 * H) return;
    var q = Math.max(0, Math.min(1, (H - r.top) / (H / 2 + r.height / 2))); q = Math.round(q * 1000) / 1000;
    if (q === alt) return; alt = q;
    t.style.setProperty('--p', q);
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(lauf); } }, { passive: true });
  addEventListener('resize', function () { alt = -1; lauf(); });
  lauf();
})();
