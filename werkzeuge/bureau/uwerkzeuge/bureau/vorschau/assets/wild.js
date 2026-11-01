/* Walk on the Wild Side · Laden, Auftritte, Leiste, «heute», das Gespräch, Flyer-Wechsel, Vorführ-Formulare. Nur transform und opacity, nativer Scroll. */
(function () {
  'use strict';
  var html = document.documentElement;
  var ruhig = html.classList.contains('ruhig');
  var IO = 'IntersectionObserver' in window;
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';

  /* ---------- Bilder: drei Bildschirme voraus, danach alles Übrige im Leerlauf */
  /* Kein Unscharf-Bild vorweg (Robert 31.10.2026): ein Bild erscheint erst, wenn es ganz geladen ist, dann blendet es weich auf */
  function zeigen(img) {
    if (img.complete && img.naturalWidth) { img.classList.add('geladen'); return; }
    img.classList.add('lad');
    function fertig() { img.classList.add('geladen', 'blende'); }
    img.addEventListener('load', fertig, { once: true }); img.addEventListener('error', fertig, { once: true });
  }
  function laden(img) {
    if (!img.dataset.srcset) return;
    img.sizes = img.dataset.sizes || '100vw';
    img.srcset = img.dataset.srcset;
    img.removeAttribute('data-srcset');
    zeigen(img);
  }
  document.querySelectorAll('img:not([data-srcset])').forEach(zeigen);
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
  /* Besuch (Robert 31.10.2026): Schild, Karte, Strassenschild und Tafel starten erst, wenn sie selbst gut im Bild stehen (Oberkante bei 72 % der Höhe) */
  var SPAET = document.getElementById('wann') ? [['#wann', '.w15-g', 'da'], ['#wo', '.wk-karte', 'da'], ['#wo', '.wk-schild', 'sd']] : [];
  var spaetZiel = [];
  window.wildSpaet = function (ziele, rand) {
    if (!IO || ruhig) { ziele.forEach(function (z) { z[0].classList.add(z[1]); }); return; }
    var offen = ziele.slice();
    var o = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (!e.isIntersecting) return; o.unobserve(e.target);
        offen = offen.filter(function (z) { if (z[2] !== e.target) return true; z[0].classList.add(z[1]); return false; }); });
    }, { rootMargin: rand || '0px 0px -28% 0px', threshold: 0 });
    ziele.forEach(function (z) { o.observe(z[2]); });
    /* Ganz unten kommt nichts mehr höher: dann alles Übrige zeigen */
    addEventListener('scroll', function () {
      if (offen.length && innerHeight + scrollY >= document.documentElement.scrollHeight - 4) { offen.forEach(function (z) { z[0].classList.add(z[1]); }); offen = []; }
    }, { passive: true });
  };
  SPAET.forEach(function (d) { var b = document.querySelector(d[0]), z = b && b.querySelector(d[1]); if (b && z) { spaetZiel.push([b, d[2], z]); if (d[2] === 'da') b.dataset.spaet = '1'; } });
  if (spaetZiel.length) window.wildSpaet(spaetZiel);
  /* Reservieren (Robert 01.11.2026): Überschrift und Text kommen, sobald die Überschrift selbst ins Bild tritt, nicht erst mit den Hockern */
  var rs = document.getElementById('wann') && document.getElementById('reservieren'), rk = rs && rs.querySelector('.rh-kopf');
  if (rk) { rs.dataset.spaet = '1'; window.wildSpaet([[rs, 'da', rk]], '0px 0px -12% 0px'); }
  document.querySelectorAll('.auf').forEach(function (el) {
    if (el.id === 'auftakt' || el.dataset.spaet) return;
    auf ? auf.observe(el) : el.classList.add('da');
  });
  /* Erster Blick komplett (Robert 31.10.2026, Standard für jede Seite): die Seite zeigt sich erst, wenn alle Bilder im ersten Bild geladen sind.
     Dann steht alles im selben Moment da: Bilder ohne Aufblenden, Kopf offen, Titel fährt hoch. Nie erst Schrift, dann Bilder. */
  var auftakt = document.getElementById('auftakt'), an = false;
  function los() {
    if (an) return; an = true;
    [].slice.call(document.querySelectorAll('img')).forEach(function (i) {
      if (i.complete && i.naturalWidth) { i.classList.add('geladen'); i.classList.remove('blende'); }
    });
    if (auftakt) auftakt.classList.add('bereit', 'da');
    [].slice.call(document.querySelectorAll('#auftakt .titel .zl')).forEach(function (z) {
      var sp = z.querySelector('.z>span'); if (sp) getComputedStyle(sp).transform;
      z.classList.add('sofort');
    });
    html.classList.add('offen');
    if (auftakt) document.dispatchEvent(new Event('auftakt-da'));
  }
  var erste = [].slice.call(document.querySelectorAll('img')).filter(function (b) {
    var r = b.getBoundingClientRect(); return r.width > 0 && r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth;
  });
  if (auftakt) [].slice.call(auftakt.querySelectorAll('img')).forEach(function (b) { if (erste.indexOf(b) < 0) erste.push(b); });   /* der ganze Kopf, auch Kacheln, die gleich hereinlaufen */
  erste.forEach(function (b) { b.decoding = 'sync'; });   /* im ersten Bild gemeinsam mit allem anderen gemalt, nicht ein Bild später */
  erste.forEach(laden);   /* auch nachgeladene Bilder im ersten Bild sofort holen */
  Promise.all(erste.map(function (b) {
    return new Promise(function (ok) {
      if (b.complete && b.naturalWidth) ok(); else { b.addEventListener('load', ok, { once: true }); b.addEventListener('error', ok, { once: true }); }
    });
  })).then(los);
  setTimeout(los, 2500);
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') setTimeout(los, 300); });
  addEventListener('pageshow', function (e) { if (e.persisted) los(); });
  /* Sicherung: kein fertig geladenes Bild bleibt je versteckt, auch wenn ein Ereignis ausbleibt */
  function nachsehen() {
    document.querySelectorAll('img.lad:not(.geladen)').forEach(function (i) { if (i.complete && i.naturalWidth) i.classList.add('geladen'); });
  }
  setInterval(nachsehen, 700);
  addEventListener('load', nachsehen);
  addEventListener('pageshow', nachsehen);
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
  var EIGEN = '.fr-kopf,.fr-strahl,.fr-menue,.fr-dbilder,.fr-zahlen,.fr-bbild,.fr-treppe,.fr-posten,.fr-huellen,.fr-team,.auftakt,.gewoelbe,.vitrine,.fk,.fenster,[data-gespraech],.ge-glas,.flyer,.dg-zug,.wb-band-zug,.th';   /* .th: Kopf «Das Haus» geht als Ganzes auf (31.10.2026) */
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
  /* Besuch (Robert 31.10.2026): jeder Block steigt erst, wenn er sichtbar im Bild steht, nicht schon unter dem Rand */
  var besuch = !!document.getElementById('wann');
  var io = new IntersectionObserver(function (es) {
    var k = 0;
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target; io.unobserve(el);
      el.style.setProperty('--e', Math.min(k++, 3));
      el.classList.add('ein'); if (el.classList.contains('bild')) el.classList.add('da');
    });
  }, { rootMargin: besuch ? '0px 0px -14% 0px' : '0px 0px 120px 0px', threshold: 0 });
  /* Was im Kopf steht, wartet, bis der Kopf mit seinen Bildern aufgeht */
  var at = document.getElementById('auftakt'), warten = [];
  alle.forEach(function (el) { if (at && at.contains(el) && !at.classList.contains('da')) warten.push(el); else io.observe(el); });
  if (warten.length) document.addEventListener('auftakt-da', function () { warten.forEach(function (el) { io.observe(el); }); }, { once: true });
  if (besuch) addEventListener('scroll', function () {
    if (innerHeight + scrollY < document.documentElement.scrollHeight - 4) return;
    alle.forEach(function (el) { if (!el.classList.contains('ein') && !(at && at.contains(el))) { io.unobserve(el); el.classList.add('ein'); if (el.classList.contains('bild')) el.classList.add('da'); } });
  }, { passive: true });

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

/* Besuch · Reservieren «Sechs Hocker» (Robert 31.10.2026): sieben Hocker und «+» über die ganze Breite. Hocker antippen = so viele Plätze.
   «+» lässt einen Hocker von rechts einschweben, die anderen rücken nach links (8, 9); beim zehnten wird aus der Theke die lange Tafel
   (zehn bis zwanzig Stühle, + / −; − bei zehn führt zurück an die Theke). Das Feld «Plätze» unten ist mit allem verbunden. */
(function () {
  'use strict';
  var SVG = '<svg viewBox="0 0 60 120" aria-hidden="true"><ellipse class="rh-sitz" cx="30" cy="12" rx="22" ry="7"/><path class="rh-bein" d="M16 18 L10 116 M44 18 L50 116 M14 78 H46"/></svg>';
  var ruhig = document.documentElement.classList.contains('ruhig') || matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.rh-form').forEach(function (f) {
    var reihe = f.querySelector('[data-rh-hocker]'), zahl = f.querySelector('[data-rh-zahl]'), was = f.querySelector('[data-rh-was]');
    var feld = f.querySelector('[data-rh-feld]'), platz = f.querySelector('[name=platz]');
    var oben = f.querySelector('[data-rh-oben]'), unten = f.querySelector('[data-rh-unten]');
    var hocker = 0, wahl = 4, tafel = false, bar = false, letzt = '', plus;

    /* Alle sichtbaren Plätze rücken weich an ihre neue Stelle (vorher/nachher messen, Unterschied ausgleiten lassen) */
    function ruecken(els, aendern) {
      var vor = els.map(function (e) { return e.getBoundingClientRect().left; });
      aendern();
      if (ruhig) return;
      els.forEach(function (e, i) {
        var d = vor[i] - e.getBoundingClientRect().left; if (!d) return;
        e.animate([{ transform: 'translateX(' + d + 'px)' }, { transform: 'none' }], { duration: 700, easing: 'cubic-bezier(.22,.68,.26,1)' });
      });
    }
    function rein(el) {   /* von rechts einschweben */
      if (ruhig) return;
      var w = innerWidth - el.getBoundingClientRect().left;
      el.animate([{ transform: 'translateX(' + w + 'px)', opacity: 0 }, { opacity: 1, offset: .5 }, { transform: 'none', opacity: 1 }], { duration: 900, easing: 'cubic-bezier(.25,1.1,.4,1)' });
    }
    function neuerHocker(k) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'rh-h'; b.dataset.n = k;
      b.setAttribute('aria-label', k + (k === 1 ? ' Platz' : ' Plätze')); b.innerHTML = SVG + '<b>' + k + '</b>';
      b.addEventListener('click', function () { setze(k); });
      return b;
    }
    function hockerDazu(animiert) {
      hocker++;
      var h = neuerHocker(hocker), alte = [].slice.call(reihe.children);
      ruecken(animiert ? alte : [], function () { reihe.insertBefore(h, plus); });
      if (animiert) rein(h);
    }
    function stuhl(animiert) {
      var s = document.createElement('i'); s.className = 'rh-stuhl';
      var ziel = oben.children.length <= unten.children.length ? oben : unten;
      ruecken(animiert ? [].slice.call(ziel.children) : [], function () { ziel.appendChild(s); });
      if (animiert) rein(s);
    }
    function stuhlWeg() { var r = oben.children.length > unten.children.length ? oben : unten; if (r.lastElementChild) r.removeChild(r.lastElementChild); }

    /* Eine Zahl setzen, egal woher (Hocker, Plus, Tafel-Knöpfe, Feld) */
    function setze(n, vonFeld, runter) {
      n = Math.max(1, Math.min(200, Math.round(n) || 1));
      if (n > 20 && n < 30) n = runter ? 20 : 30;   /* nach der Tafel (bis 20) kommt gleich die ganze Bar (ab 30) */
      if (n >= 30) {
        if (!bar) { bar = true; tafel = false; }
      } else if (n >= 10) {
        bar = false;
        var warTafel = tafel; tafel = true;
        if (!warTafel) { oben.innerHTML = ''; unten.innerHTML = ''; for (var i = 0; i < n; i++) stuhl(false); einfliegenAlle(); }
        else { while (oben.children.length + unten.children.length < n) stuhl(true); while (oben.children.length + unten.children.length > n) stuhlWeg(); }
      } else {
        tafel = false; bar = false;
        while (hocker < Math.min(n, 9)) hockerDazu(!vonFeld || true);
      }
      wahl = n; zeige(vonFeld);
    }
    function einfliegenAlle() {
      if (ruhig) return;
      [].forEach.call(f.querySelectorAll('.rh-stuhl'), function (s, i) {
        s.animate([{ transform: 'translateY(-24px)', opacity: 0 }, { transform: 'none', opacity: 1 }], { duration: 700, delay: 250 + i * 45, easing: 'cubic-bezier(.3,1.4,.5,1)', fill: 'backwards' });
      });
    }
    function zeige(vonFeld) {
      var t = wahl + (wahl === 1 ? ' Platz' : ' Plätze');
      if (t !== letzt && zahl) { zahl.textContent = t; zahl.classList.remove('rh-tick'); void zahl.offsetWidth; zahl.classList.add('rh-tick'); letzt = t; }
      if (was) was.textContent = bar ? 'Die ganze Bar · ab dreissig Gästen' : tafel ? 'An der langen Tafel · zehn bis zwanzig' : 'Wie viele · tippt die Hocker an';
      if (!vonFeld && feld) feld.value = wahl;
      platz.value = bar ? 'Ganze Bar' : tafel ? 'Tafel' : 'Theke';
      f.classList.toggle('rh-an-bar', bar); barEl.setAttribute('aria-hidden', bar ? 'false' : 'true');
      [].forEach.call(reihe.querySelectorAll('.rh-h[data-n]'), function (h) { var an = +h.dataset.n <= wahl; h.classList.toggle('an', an); h.setAttribute('aria-pressed', an); });
      f.classList.toggle('rh-an-tafel', tafel);
      if (tafel) ausrichten();
      f.querySelector('.rh-tafel').setAttribute('aria-hidden', tafel ? 'false' : 'true');
    }

    /* Die ganze Bar (ab 30): gezeichnet in Gold, Strich für Strich von links nach rechts — Lampen, Rückbuffet mit Flaschen, Tresen, Hocker */
    function barZeichnung() {
      var p = [], d = function (x) { return Math.round(x * 0.9); };
      function linie(pfad, x, cls) { p.push('<path pathLength="1" class="' + (cls || 'rh-strich') + '" style="--d:' + d(x) + '" d="' + pfad + '"/>'); }
      [300, 600, 900].forEach(function (x) { linie('M' + x + ' 0 V22 M' + (x - 17) + ' 36 L' + (x - 7) + ' 22 H' + (x + 7) + ' L' + (x + 17) + ' 36 Z', x); });
      [62, 98].forEach(function (y, r) {
        linie('M150 ' + y + ' H1050', 150);
        for (var x = 172 + r * 14, i = 0; x < 1036; x += 30 + (i % 3) * 5, i++) {
          var h = 18 + ((i * 7 + r * 3) % 4) * 3, b = 4 + (i % 2) * 2;
          linie('M' + (x - b) + ' ' + y + ' V' + (y - h + 6) + ' Q' + (x - b) + ' ' + (y - h + 2) + ' ' + (x - 2) + ' ' + (y - h) + ' V' + (y - h - 5) + ' H' + (x + 2) + ' V' + (y - h) + ' Q' + (x + b) + ' ' + (y - h + 2) + ' ' + (x + b) + ' ' + (y - h + 6) + ' V' + y, x, 'rh-strich rh-flasche');
        }
      });
      linie('M110 120 H1090 L1140 142 H60 Z', 60, 'rh-strich rh-platte3');
      linie('M60 142 V202 H1140 V142', 60);
      for (var x = 150; x < 1140; x += 90) linie('M' + x + ' 148 V196', x, 'rh-strich rh-fein');
      linie('M60 142 H1140', 60, 'rh-strich rh-kante');
      for (var k = 0; k < 12; k++) {
        var sx = 120 + k * 87.3;
        linie('M' + (sx - 13) + ' 182 L' + (sx - 17) + ' 230 M' + (sx + 13) + ' 182 L' + (sx + 17) + ' 230 M' + (sx - 15) + ' 212 H' + (sx + 15), sx, 'rh-strich');
        linie('M' + (sx - 22) + ' 178 A22 6 0 1 0 ' + (sx + 22) + ' 178 A22 6 0 1 0 ' + (sx - 22) + ' 178 Z', sx, 'rh-strich rh-sitz3');
      }
      return '<svg viewBox="0 -2 1200 236" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' + p.join('') + '</svg>';
    }
    var barEl = document.createElement('div'); barEl.className = 'rh-bar'; barEl.setAttribute('aria-hidden', 'true');
    barEl.innerHTML = '<div class="rh-barbild">' + barZeichnung().replace('xMidYMid meet', innerWidth <= 640 ? 'xMidYMid slice' : 'xMidYMid meet') + '</div><div class="rh-tknopf"><button type="button" data-rh-barminus aria-label="Zurück an die lange Tafel"><span class="rh-plus rh-minus" aria-hidden="true"></span></button></div>';
    f.querySelector('[data-rh-buehne]').appendChild(barEl);
    barEl.querySelector('[data-rh-barminus]').addEventListener('click', function () { setze(20, false, true); });

    /* Aufbau: sieben Hocker und das «+» */
    plus = document.createElement('button'); plus.type = 'button'; plus.className = 'rh-h rh-mehr';
    plus.setAttribute('aria-label', 'Einen Platz mehr'); plus.innerHTML = '<span class="rh-plus" aria-hidden="true"></span><b>mehr</b>';
    plus.addEventListener('click', function () { setze(wahl + 1); });   /* eins weiter: 4, 5, 6 … 9, dann die Tafel */
    reihe.appendChild(plus);
    for (var k = 0; k < 7; k++) hockerDazu(false);
    [].forEach.call(reihe.children, function (h, i) { h.style.setProperty('--n', i); });

    /* Tafel: + und − */
    var kn = document.createElement('div'); kn.className = 'rh-tknopf';
    kn.innerHTML = '<button type="button" data-rh-plus aria-label="Ein Stuhl mehr"><span class="rh-plus" aria-hidden="true"></span></button>'
                 + '<button type="button" data-rh-minus aria-label="Ein Stuhl weniger"><span class="rh-plus rh-minus" aria-hidden="true"></span></button>';
    f.querySelector('.rh-tisch').appendChild(kn);
    kn.querySelector('[data-rh-plus]').addEventListener('click', function () { setze(wahl + 1); });

    /* Das Plus der Tafel liegt genau dort, wo an der Theke das «mehr» war: von 9 auf 10 bleibt die Maus auf dem Plus (Robert 31.10.2026) */
    function mitte(el) { var x = el.offsetWidth / 2, y = el.offsetHeight / 2; for (var e = el; e; e = e.offsetParent) { x += e.offsetLeft; y += e.offsetTop; } return { x: x, y: y }; }
    function ausrichten() {
      kn.style.transform = ''; kn.style.marginRight = '';
      if (innerWidth <= 640) return;
      var a = mitte(plus.querySelector('.rh-plus')), c = mitte(kn.querySelector('[data-rh-plus]'));
      if (c.x > a.x) kn.style.marginRight = Math.round(c.x - a.x) + 'px';   /* Tisch wird etwas kürzer, Knöpfe rücken nach links */
      c = mitte(kn.querySelector('[data-rh-plus]'));
      kn.style.transform = 'translate(' + Math.round(a.x - c.x) + 'px,' + Math.round(a.y - c.y) + 'px)';
    }
    addEventListener('resize', function () { if (tafel) ausrichten(); });
    kn.querySelector('[data-rh-minus]').addEventListener('click', function () { setze(wahl - 1, false, true); });

    /* Feld «Plätze» */
    if (feld) {
      feld.addEventListener('input', function () { var v = +feld.value; if (feld.value !== '' && v >= 1 && (v <= 20 || v >= 30)) setze(v, true); });
      feld.addEventListener('change', function () { setze(+feld.value || 1); });
    }
    zeige();
  });
})();

/* Das Haus · Steckbriefe (31.10.2026): --sb von 0 (Zeile unten am Rand) bis 1 (Mitte), nur sichtbare Zeilen rechnen. */
(function () {
  var z = [].slice.call(document.querySelectorAll('[data-sb]')); if (!z.length) return;
  var sicht = new Set(), an = false;
  function takt() { an = false; var vh = innerHeight; sicht.forEach(function (el) { var r = el.getBoundingClientRect(); var p = (vh - r.top) / (vh / 2 + r.height / 2); el.style.setProperty('--sb', Math.max(0, Math.min(1, p)).toFixed(3)); }); }
  function los() { if (!an) { an = true; requestAnimationFrame(takt); } }
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? sicht.add(e.target) : sicht.delete(e.target); }); los(); }, { rootMargin: '100px 0px' });
  z.forEach(function (e) { io.observe(e); }); addEventListener('scroll', los, { passive: true }); addEventListener('resize', los);
})();

/* Reservieren und Anfragen: vergangene Abende sind im Kalender nicht wählbar (31.10.2026) */
(function () { var d = new Date(), z = function (n) { return (n < 10 ? '0' : '') + n; }, h = d.getFullYear() + '-' + z(d.getMonth() + 1) + '-' + z(d.getDate());
  document.querySelectorAll('input[type=date]:not([min])').forEach(function (i) { i.min = h; }); })();

/* ---------- Auswahl, Kalender und Uhrzeit im Stil des Hauses (Master Website-Bau 2.9 Punkt 11; Robert 31.10.2026: «alles an ausklappbaren Möglichkeiten ist immer im Stil des Hauses»).
   Baustein aus Grand Beau-Rivage über Salt & Silver (site/assets/js/auswahl.js) unverändert übernommen; Aussehen Wild Side unten in wild.css. */
/* ---------- Datumsfelder, die der Browser selbst zeichnet (12.10.2026) ----------
   Feiern: Datum und Anfrage, Anreise: Spa-Tag, die Buchung im Chat. Der Browser schreibt dort das Datum in seiner eigenen Schreibweise
   (meist amerikanisch «mm/dd/yyyy»), nicht in der der Seite. Darum liegt über jedem solchen Feld eine Zeile in der Schreibweise der Sprache
   (de/fr 12.10.2026, en britisch 12/10/2026, zh 2026/10/12, ko 2026. 10. 12., ar 12/10/2026); das echte Feld bleibt darunter, unsichtbar
   beschriftet, und öffnet beim Klick den Kalender des Browsers. Felder mit eigenem Kalender (lw-nativ, Block darüber) brauchen das nicht. */
(function () {
  var LANG = document.documentElement.lang || 'de-DE', SP = LANG.slice(0, 2);
  var ORT = { de: 'de-DE', en: 'en-GB', fr: 'fr-CH', zh: 'zh-CN', ko: 'ko-KR', ar: 'ar-u-nu-latn' }[SP] || LANG;
  var LEER = { de: 'Datum wählen', en: 'Choose a date', fr: 'Choisir une date', zh: '选择日期', ko: '날짜 선택', ar: 'اختيار التاريخ' }[SP] || 'Datum wählen';
  var fmt; try { fmt = new Intl.DateTimeFormat(ORT, { day: '2-digit', month: '2-digit', year: 'numeric' }); } catch (e) { return; }
  var lies = function (s) { var p = (s || '').split('-'); return p.length === 3 ? new Date(+p[0], p[1] - 1, +p[2]) : null; };
  var alle = [];
  function lege(i) {
    var b = i._dtAnz; if (!b) return;
    if (!i.offsetWidth) { b.hidden = true; return; } b.hidden = false;
    b.style.left = i.offsetLeft + 'px'; b.style.top = i.offsetTop + 'px'; b.style.width = i.offsetWidth + 'px'; b.style.height = i.offsetHeight + 'px';
  }
  function schreibe(i) { var d = lies(i.value), b = i._dtAnz; b.textContent = d ? fmt.format(d) : LEER; b.classList.toggle('dt-anz--leer', !d); lege(i); }
  function ruest(i) {
    if (i._dtAnz || i.type !== 'date' || i.classList.contains('lw-nativ')) return;
    var el = i.parentNode; if (!el) return;
    var cs = getComputedStyle(i), b = document.createElement('b'); b.className = 'dt-anz'; b.setAttribute('aria-hidden', 'true');
    b.style.font = cs.font; b.style.letterSpacing = cs.letterSpacing; b.style.color = cs.color; b.style.padding = cs.padding; b.style.direction = cs.direction;
    b.style.justifyContent = /right|end/.test(cs.textAlign) ? 'flex-end' : cs.textAlign === 'center' ? 'center' : 'flex-start';
    i._dtAnz = b; i.classList.add('dt-nativ'); el.classList.add('dt-feld'); el.insertBefore(b, i.nextSibling);
    ['input', 'change', 'blur'].forEach(function (ev) { i.addEventListener(ev, function () { schreibe(i); }); });
    i.addEventListener('click', function () { try { i.showPicker(); } catch (e) {} });
    alle.push(i); schreibe(i);
    if (window.ResizeObserver) new ResizeObserver(function () { lege(i); }).observe(i);   /* S&S: Felder im Tischfenster sind beim Laden unsichtbar; sobald das Fenster aufgeht, sitzt die Zeile sofort */
  }
  function suche() { [].slice.call(document.querySelectorAll('input[type=date]')).forEach(ruest); }
  /* die Leisten mit eigenem Kalender markieren ihre Felder beim Laden (lw-nativ), darum erst danach suchen */
  setTimeout(suche, 0);
  if ('MutationObserver' in window) new MutationObserver(function (ms) {
    var neu = ms.some(function (m) { return [].some.call(m.addedNodes, function (n) { return n.nodeType === 1 && (n.tagName === 'INPUT' || (n.querySelector && n.querySelector('input[type=date]'))); }); });
    if (neu) setTimeout(suche, 0);
  }).observe(document.body, { childList: true, subtree: true });
  var takt = 0; window.addEventListener('resize', function () { if (!takt) takt = requestAnimationFrame(function () { takt = 0; alle.forEach(lege); }); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { alle.forEach(lege); });
})();

/* Auswahllisten im Stil des Hauses (Robert 11.10.2026: «überall, wo es solche Auswahlmöglichkeiten gibt, im Stil des Hauses,
   und immer, wenn sowas gebaut wird, direkt mit»). Jedes <select> der Seite bekommt eine eigene Liste: Creme-Karte mit Goldkante,
   Namen in der Titelschrift, gewählter Eintrag nachtblau mit Goldraute. Das echte <select> bleibt (unsichtbar) im Formular und trägt
   den Wert, deshalb funktionieren Formulare, Rechner und Mail-Anfragen unverändert; jede Wahl löst «change» und «input» aus.
   Auch später eingefügte Listen (z. B. gast.js) werden übernommen. Ausgenommen: die Buchungsleiste (form[data-leiste]) mit ihrer
   eigenen Gäste-Liste und alles in [data-eigene-wahl]. Tastatur: Pfeile, Pos1/Ende, Anfangsbuchstabe, Enter, Escape, Tab.
   Die Liste hängt am <body> (oder im offenen <dialog>), damit kein überlaufender Abschnitt sie abschneidet; sie öffnet nach unten
   oder, wenn unten kein Platz ist, nach oben. Bewegung nur über transform und opacity. */
(function () {
  'use strict';
  var doc = document, offen = null, nr = 0;
  var PFEIL = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>';

  function ausgenommen(s) { return s.multiple || s.size > 1 || s.closest('form[data-leiste],form[data-leiste-kal],[data-eigene-wahl]') || s.classList.contains('lw-nativ'); }

  function baue(s) {
    if (s.dataset.hwahl || ausgenommen(s)) return;
    s.dataset.hwahl = '1';
    var id = 'hwahl' + (++nr);
    var hülle = doc.createElement('span'); hülle.className = 'hwahl';
    s.parentNode.insertBefore(hülle, s); hülle.appendChild(s);
    s.classList.add('hwahl-nativ'); s.tabIndex = -1; s.setAttribute('aria-hidden', 'true');
    var k = doc.createElement('button'); k.type = 'button'; k.className = 'hwahl-knopf'; k.style.webkitAppearance = 'none'; k.style.appearance = 'none';   // nie der System-Knopf
    k.setAttribute('aria-haspopup', 'listbox'); k.setAttribute('aria-expanded', 'false'); k.setAttribute('aria-controls', id);
    var lab = s.closest('label'); var titel = lab ? (lab.querySelector('span') || {}).textContent : s.getAttribute('aria-label');
    if (titel) k.setAttribute('aria-label', titel.trim());
    k.innerHTML = '<b class="hwahl-wert"></b>' + PFEIL;
    hülle.appendChild(k);
    // Schrift, Linie, Polster und Fläche des Feldes übernehmen, damit der Knopf in jede Leiste passt. Das geschieht mehrmals (sofort, wenn alle
    // Stylesheets da sind, wenn die Schriften da sind): Läuft das Skript, bevor der Stil der Seite geladen ist, hat das Feld noch das Aussehen des
    // Systems (weiss, mit Rand), und das blieb sonst am Knopf hängen (Robert 12.10.2026, Pass-Berater: «diese weissen Kästen»).
    function kleide() {
      var cs = getComputedStyle(s);
      k.style.fontFamily = cs.fontFamily; k.style.fontSize = cs.fontSize; k.style.fontWeight = cs.fontWeight; k.style.color = cs.color; k.style.letterSpacing = cs.letterSpacing;
      ['borderBottom', 'borderTop', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'backgroundColor', 'borderRadius', 'boxShadow', 'minHeight'].forEach(function (x) { k.style[x] = ''; if (cs[x] && cs[x] !== 'none' && cs[x] !== 'rgba(0, 0, 0, 0)') k.style[x] = cs[x]; });
    }
    kleide(); s._kleide = kleide;
    var l = doc.createElement('ul'); l.className = 'hwahl-liste'; l.id = id; l.setAttribute('role', 'listbox'); l.tabIndex = -1;
    if (titel) l.setAttribute('aria-label', titel.trim());
    var g = { s: s, k: k, l: l, j: 0 };
    s._gw = g;
    k.addEventListener('click', function () { offen === g ? zu(true) : auf(g); });
    k.addEventListener('keydown', function (e) { if (e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Enter' || e.key === ' ') { e.preventDefault(); auf(g); } });
    l.addEventListener('keydown', function (e) { taste(g, e); });
    l.addEventListener('click', function (e) { var o = e.target.closest('[role=option]'); if (o) waehle(g, +o.dataset.i); });
    l.addEventListener('mousemove', function (e) { var o = e.target.closest('[role=option]'); if (o) markiere(g, +o.dataset.i); });
    s.addEventListener('change', function () { zeige(g); });
    var f = s.form; if (f) f.addEventListener('reset', function () { setTimeout(function () { zeige(g); }, 0); });
    zeige(g);
  }

  function zeige(g) { var o = g.s.options[g.s.selectedIndex]; g.k.querySelector('.hwahl-wert').textContent = o ? o.textContent : ''; g.k.classList.toggle('hwahl-leer', !!(o && !o.value && o.disabled)); }

  function fuelle(g) {
    var h = '';
    [].forEach.call(g.s.options, function (o, i) {
      if (o.hidden) return;
      var ja = i === g.s.selectedIndex;
      h += '<li role="option" data-i="' + i + '" aria-selected="' + ja + '"' + (o.disabled ? ' aria-disabled="true"' : '') + ' style="--i:' + i + '"><i></i><span></span></li>';
    });
    g.l.innerHTML = h;
    [].forEach.call(g.l.children, function (li) { li.querySelector('span').textContent = g.s.options[+li.dataset.i].textContent; });
  }

  function lage(g) {
    var r = g.k.closest('.hwahl').getBoundingClientRect(), feld = g.k.closest('label,.feld,.anf__f') || g.k;
    var rf = feld.getBoundingClientRect(), b = Math.max(rf.width, 240), hl = g.l.offsetHeight, unten = innerHeight - rf.bottom, oben = rf.top;
    var nachOben = unten < hl + 16 && oben > unten;
    var x = Math.min(Math.max(8, rf.left), innerWidth - b - 8);
    g.l.style.left = x + 'px'; g.l.style.width = b + 'px';
    g.l.style.top = (nachOben ? rf.top - hl - 8 : rf.bottom + 8) + 'px';
    g.l.classList.toggle('hwahl-oben', nachOben);
  }

  function auf(g) {
    if (offen) zu(false);
    fuelle(g);
    (g.s.closest('dialog[open]') || doc.body).appendChild(g.l);
    lage(g);
    offen = g; g.k.setAttribute('aria-expanded', 'true'); g.k.closest('.hwahl').classList.add('hwahl--offen');
    markiere(g, Math.max(0, g.s.selectedIndex));
    requestAnimationFrame(function () { g.l.classList.add('hwahl-auf'); });
    g.l.focus({ preventScroll: true });
    addEventListener('scroll', mit, true); addEventListener('resize', mit);
  }
  var takt = 0;
  function mit() { if (!offen || takt) return; takt = requestAnimationFrame(function () { takt = 0; if (offen) lage(offen); }); }

  function zu(fokus) {
    var g = offen; if (!g) return;
    offen = null; g.k.setAttribute('aria-expanded', 'false'); g.k.closest('.hwahl').classList.remove('hwahl--offen');
    g.l.classList.remove('hwahl-auf');
    removeEventListener('scroll', mit, true); removeEventListener('resize', mit);
    setTimeout(function () { if (offen !== g && g.l.parentNode) g.l.parentNode.removeChild(g.l); }, 320);
    if (fokus) g.k.focus({ preventScroll: true });
  }

  function markiere(g, i) {
    var lis = [].slice.call(g.l.children); if (!lis.length) return;
    var li = g.l.querySelector('[data-i="' + i + '"]') || lis[0];
    lis.forEach(function (x) { x.classList.toggle('hwahl-hier', x === li); });
    g.j = +li.dataset.i; g.l.setAttribute('aria-activedescendant', '');
    var r = li.getBoundingClientRect(), rl = g.l.getBoundingClientRect();
    if (r.bottom > rl.bottom) g.l.scrollTop += r.bottom - rl.bottom; else if (r.top < rl.top) g.l.scrollTop -= rl.top - r.top;
  }

  function waehle(g, i) {
    var o = g.s.options[i]; if (!o || o.disabled) return;
    g.s.selectedIndex = i;
    g.s.dispatchEvent(new Event('input', { bubbles: true })); g.s.dispatchEvent(new Event('change', { bubbles: true }));
    zeige(g); zu(true);
  }

  var suche = '', suchUhr = 0;
  function taste(g, e) {
    var lis = [].slice.call(g.l.children).filter(function (x) { return !x.hasAttribute('aria-disabled'); });
    var pos = lis.findIndex(function (x) { return +x.dataset.i === g.j; });
    if (e.key === 'ArrowDown') { e.preventDefault(); markiere(g, +lis[Math.min(lis.length - 1, pos + 1)].dataset.i); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); markiere(g, +lis[Math.max(0, pos - 1)].dataset.i); }
    else if (e.key === 'Home') { e.preventDefault(); markiere(g, +lis[0].dataset.i); }
    else if (e.key === 'End') { e.preventDefault(); markiere(g, +lis[lis.length - 1].dataset.i); }
    else if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); waehle(g, g.j); }
    else if (e.key === 'Escape') { e.preventDefault(); zu(true); }
    else if (e.key === 'Tab') { zu(false); }
    else if (e.key.length === 1) {
      clearTimeout(suchUhr); suche += e.key.toLowerCase(); suchUhr = setTimeout(function () { suche = ''; }, 700);
      var t = lis.find(function (x) { return x.textContent.trim().toLowerCase().replace(/^[«"„]/, '').indexOf(suche) === 0; }); if (t) markiere(g, +t.dataset.i);
    }
  }

  doc.addEventListener('pointerdown', function (e) { if (offen && !offen.l.contains(e.target) && !offen.k.contains(e.target)) zu(false); }, true);

  function alle(wurzel) { [].forEach.call((wurzel || doc).querySelectorAll('select'), baue); }
  // Werte, die andere Skripte direkt setzen (s.value = …), beim nächsten Blick nachziehen
  setInterval(function () { [].forEach.call(doc.querySelectorAll('select[data-hwahl]'), function (s) { var g = s._gw; if (g && g.k.querySelector('.hwahl-wert').textContent !== (s.options[s.selectedIndex] || {}).textContent) zeige(g); }); }, 600);
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', function () { alle(); }); else alle();
  function neuKleiden() { [].forEach.call(doc.querySelectorAll('select[data-hwahl]'), function (s) { if (s._kleide) s._kleide(); }); }
  [].forEach.call(doc.querySelectorAll('link[rel=stylesheet]'), function (l) { l.addEventListener('load', neuKleiden); });
  window.addEventListener('load', neuKleiden);
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(neuKleiden);
  new MutationObserver(function (ms) { ms.forEach(function (m) { [].forEach.call(m.addedNodes, function (n) { if (n.nodeType !== 1) return; if (n.tagName === 'SELECT') baue(n); else if (n.querySelector) alle(n); }); }); }).observe(doc.documentElement, { childList: true, subtree: true });
  window.susAuswahl = { baue: baue, alle: alle };
})();

/* ---------- Datum und Uhrzeit im Stil des Hauses (Robert 12.10.2026: «die Auswahlmöglichkeiten auch immer im Stil des Hauses, feste Designregel») ----------
   Jedes Datumsfeld (input type=date) bekommt den Kalender des Hauses, jedes Zeitfeld (type=time) die Zeitwahl des Hauses, statt des
   Kalenders und der Räder des Browsers. Das echte Feld bleibt im Formular und trägt den Wert (jjjj-mm-tt bzw. hh:mm), darum laufen
   Rechner, Prüfungen und Mail-Anfragen unverändert; jede Wahl löst «input» und «change» aus. Über dem Feld liegt ein unsichtbarer Knopf,
   der die Auswahl öffnet, so kommt der Browser gar nicht erst zum Zug. min/max und step des Feldes gelten. Ausgenommen: die Leisten mit
   eigenem Zeitraum-Kalender (lw-nativ) und alles in [data-eigene-wahl]. Tastatur: Pfeile, Bild auf/ab, Enter, Escape.
   Die Auswahl hängt am <body> (oder im offenen <dialog>), steht fest auf der Seite und scrollt mit. Bewegung nur über transform und opacity. */
(function () {
  'use strict';
  var doc = document, LANG = doc.documentElement.lang || 'de-DE', SP = LANG.slice(0, 2);
  var ORT = { de: 'de-DE', en: 'en-GB', fr: 'fr-CH', zh: 'zh-CN', ko: 'ko-KR', ar: 'ar-u-nu-latn' }[SP] || LANG;
  var W = { de: ['Vorheriger Monat', 'Nächster Monat', 'Stunde', 'Minute'], en: ['Previous month', 'Next month', 'Hour', 'Minute'], fr: ['Mois précédent', 'Mois suivant', 'Heure', 'Minute'],
            zh: ['上个月', '下个月', '时', '分'], ko: ['이전 달', '다음 달', '시', '분'], ar: ['الشهر السابق', 'الشهر التالي', 'الساعة', 'الدقيقة'] }[SP] || ['Vorheriger Monat', 'Nächster Monat', 'Stunde', 'Minute'];
  var fMonat, fTag, fLang;
  try { fMonat = new Intl.DateTimeFormat(ORT, { month: 'long' }); fTag = new Intl.DateTimeFormat(ORT, { weekday: 'short' }); fLang = new Intl.DateTimeFormat(ORT, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }); } catch (e) { return; }
  var PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>';
  var zwei = function (n) { return (n < 10 ? '0' : '') + n; };
  var iso = function (d) { return d.getFullYear() + '-' + zwei(d.getMonth() + 1) + '-' + zwei(d.getDate()); };
  var lies = function (s) { var p = (s || '').split('-'); return p.length === 3 && +p[0] ? new Date(+p[0], p[1] - 1, +p[2]) : null; };
  var offen = null;

  function ausgenommen(i) { return i.classList.contains('lw-nativ') || i.closest('[data-eigene-wahl]') || i.disabled; }

  function ruest(i) {
    if (i._zw || ausgenommen(i) || (i.type !== 'date' && i.type !== 'time')) return;
    var el = i.parentNode; if (!el) return;
    var art = i.type, k = doc.createElement('button'); k.type = 'button'; k.className = 'zw-knopf'; k.setAttribute('aria-haspopup', 'dialog'); k.setAttribute('aria-expanded', 'false');
    var lab = i.closest('label'), titel = lab && lab.querySelector('span') ? lab.querySelector('span').textContent.trim() : (i.getAttribute('aria-label') || '');
    i._zw = { i: i, k: k, art: art, titel: titel };
    el.classList.add('dt-feld'); i.classList.add('zw-nativ'); i.tabIndex = -1;
    if (art === 'time' && !i._dtAnz) {   /* Zeitfelder bekommen dieselbe Zeile wie die Datumsfelder (dort legt main.js sie an) */
      var cs = getComputedStyle(i), b = doc.createElement('b'); b.className = 'dt-anz'; b.setAttribute('aria-hidden', 'true');
      b.style.font = cs.font; b.style.letterSpacing = cs.letterSpacing; b.style.color = cs.color; b.style.padding = cs.padding; b.style.direction = 'ltr';
      b.style.justifyContent = /right|end/.test(cs.textAlign) ? 'flex-end' : cs.textAlign === 'center' ? 'center' : 'flex-start';
      i._zwAnz = b; i.classList.add('dt-nativ'); el.insertBefore(b, i.nextSibling);
      ['input', 'change'].forEach(function (ev) { i.addEventListener(ev, function () { schreibe(i); }); });
    }
    el.appendChild(k);
    k.addEventListener('click', function (e) { e.preventDefault(); offen && offen.z === i._zw ? zu(true) : auf(i._zw); });
    if (lab) lab.addEventListener('click', function (e) { if (e.target !== k && !(offen && offen.f.contains(e.target))) e.preventDefault(); });   /* ein Klick auf die Beschriftung soll das echte Feld nicht öffnen */
    lege(i); schreibe(i);
    if (window.ResizeObserver) new ResizeObserver(function () { lege(i); }).observe(i);   /* S&S: wie oben, ohne auf den 700-ms-Takt zu warten */
  }
  function schreibe(i) { var b = i._zwAnz; if (b) { b.textContent = i.value || '–:–'; b.classList.toggle('dt-anz--leer', !i.value); } beschrifte(i); }
  function beschrifte(i) { var z = i._zw; if (!z) return; var d = z.art === 'date' ? lies(i.value) : null; z.k.setAttribute('aria-label', (z.titel ? z.titel + ': ' : '') + (d ? fLang.format(d) : (i.value || '…'))); }
  function lege(i) {
    var z = i._zw; if (!z) return;
    var s = z.k.style, b = i._zwAnz; s.left = i.offsetLeft + 'px'; s.top = i.offsetTop + 'px'; s.width = i.offsetWidth + 'px'; s.height = i.offsetHeight + 'px'; z.k.hidden = !i.offsetWidth;
    if (b) { b.hidden = !i.offsetWidth; b.style.left = s.left; b.style.top = s.top; b.style.width = s.width; b.style.height = s.height; }
  }

  function auf(z) {
    zu(false);
    var f = doc.createElement('div'); f.className = 'zw zw--' + z.art; f.setAttribute('role', 'dialog'); if (z.titel) f.setAttribute('aria-label', z.titel);
    var wirt = z.i.closest('dialog[open]') || doc.body; wirt.appendChild(f);
    offen = { z: z, f: f, fest: wirt !== doc.body };
    if (offen.fest) f.classList.add('zw--fest');
    z.k.setAttribute('aria-expanded', 'true');
    if (z.art === 'date') { var d = lies(z.i.value) || grenze(z.i, new Date()); offen.blick = new Date(d.getFullYear(), d.getMonth(), 1); offen.hier = d; kalender(); }
    else zeit();
    lageF(); requestAnimationFrame(function () { f.classList.add('zw--auf'); });
    f.addEventListener('keydown', taste);
  }
  function zu(fokus) {
    if (!offen) return;
    var o = offen; offen = null; o.z.k.setAttribute('aria-expanded', 'false'); o.f.classList.remove('zw--auf');
    setTimeout(function () { if (o.f.parentNode) o.f.parentNode.removeChild(o.f); }, 320);
    if (fokus) o.z.k.focus();
  }
  function lageF() {
    if (!offen) return;
    var f = offen.f, r = offen.z.k.getBoundingClientRect(), b = f.offsetWidth, h = f.offsetHeight, vw = doc.documentElement.clientWidth, vh = window.innerHeight;
    var x = Math.max(10, Math.min(r.left, vw - b - 10)), unten = r.bottom + 10 + h <= vh || r.top - 10 - h < 60, y = unten ? r.bottom + 10 : r.top - 10 - h;
    f.classList.toggle('zw--oben', !unten);
    if (offen.fest) { f.style.left = x + 'px'; f.style.top = Math.max(10, y) + 'px'; }
    else { f.style.left = (x + window.scrollX) + 'px'; f.style.top = (y + window.scrollY) + 'px'; }
  }
  function grenze(i, d) { var mn = lies(i.min), mx = lies(i.max); if (mn && d < mn) return mn; if (mx && d > mx) return mx; return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function setze(z, wert) { z.i.value = wert; z.i.dispatchEvent(new Event('input', { bubbles: true })); z.i.dispatchEvent(new Event('change', { bubbles: true })); schreibe(z.i); }

  /* ----- Kalender: ein Monat, Wochentage in der Sprache der Seite, Woche beginnt am Montag ----- */
  function kalender() {
    var o = offen, i = o.z.i, mn = lies(i.min), mx = lies(i.max), wahl = lies(i.value), heute = iso(new Date()), b = o.blick, j = b.getFullYear(), m = b.getMonth();
    var h = '<div class="zw__kopf"><button type="button" class="zw__pfeil zw__pfeil--zur" data-schritt="-1" aria-label="' + W[0] + '">' + PF + '</button><p class="zw__monat"><b>' + fMonat.format(b) + '</b> ' + j + '</p><button type="button" class="zw__pfeil" data-schritt="1" aria-label="' + W[1] + '">' + PF + '</button></div><div class="zw__tage" aria-hidden="true">';
    for (var t = 0; t < 7; t++) h += '<span>' + fTag.format(new Date(2024, 0, 1 + t)).replace('.', '') + '</span>';   /* 1.1.2024 war ein Montag */
    h += '</div><div class="zw__raster" role="grid">';
    var leer = (new Date(j, m, 1).getDay() + 6) % 7, n = new Date(j, m + 1, 0).getDate();
    for (t = 0; t < leer; t++) h += '<span></span>';
    for (t = 1; t <= n; t++) {
      var d = new Date(j, m, t), s = iso(d), aus = (mn && d < mn) || (mx && d > mx);
      h += '<button type="button" class="zw__tag' + (s === heute ? ' zw__tag--heute' : '') + '" data-tag="' + s + '"' + (wahl && iso(wahl) === s ? ' aria-pressed="true"' : '') + (aus ? ' disabled' : '') + ' aria-label="' + fLang.format(d) + '" tabindex="-1">' + t + '</button>';
    }
    o.f.innerHTML = h + '</div>';
    var ziel = o.f.querySelector('[data-tag="' + iso(o.hier) + '"]:not([disabled])') || o.f.querySelector('.zw__tag[aria-pressed]') || o.f.querySelector('.zw__tag:not([disabled])');
    if (ziel) { ziel.tabIndex = 0; setTimeout(function () { if (offen === o) ziel.focus({ preventScroll: true }); }, 30); }
  }
  /* ----- Zeit: Stunden und Minuten nebeneinander, Schritt aus dem Feld (step in Sekunden) ----- */
  function zeit() {
    var o = offen, i = o.z.i, wert = /^\d\d:\d\d/.test(i.value) ? i.value : '12:00', hh = +wert.slice(0, 2), mm = +wert.slice(3, 5);
    var schritt = Math.max(1, Math.min(30, Math.round((+i.step || 900) / 60))); if (60 % schritt) schritt = 5;
    mm = Math.round(mm / schritt) * schritt % 60;
    var h = '<div class="zw__zeit"><div class="zw__spalte" role="listbox" aria-label="' + W[2] + '" data-teil="h">';
    for (var t = 0; t < 24; t++) h += '<button type="button" role="option" class="zw__z" data-w="' + t + '" aria-selected="' + (t === hh) + '" tabindex="' + (t === hh ? 0 : -1) + '">' + zwei(t) + '</button>';
    h += '</div><i class="zw__punkt" aria-hidden="true">:</i><div class="zw__spalte" role="listbox" aria-label="' + W[3] + '" data-teil="m">';
    for (t = 0; t < 60; t += schritt) h += '<button type="button" role="option" class="zw__z" data-w="' + t + '" aria-selected="' + (t === mm) + '" tabindex="' + (t === mm ? 0 : -1) + '">' + zwei(t) + '</button>';
    o.f.innerHTML = h + '</div></div>';
    o.hh = hh; o.mm = mm;
    [].forEach.call(o.f.querySelectorAll('.zw__spalte'), function (sp) { var a = sp.querySelector('[aria-selected=true]'); if (a) sp.scrollTop = a.offsetTop - sp.clientHeight / 2 + a.offsetHeight / 2; });
    var e = o.f.querySelector('[data-teil=h] [aria-selected=true]'); if (e) setTimeout(function () { if (offen === o) e.focus({ preventScroll: true }); }, 30);
  }

  doc.addEventListener('click', function (e) {
    if (!offen || !offen.f.contains(e.target)) return;
    var o = offen, p = e.target.closest('[data-schritt]'), tg = e.target.closest('.zw__tag'), zz = e.target.closest('.zw__z');
    if (p) { o.blick = new Date(o.blick.getFullYear(), o.blick.getMonth() + (+p.getAttribute('data-schritt')), 1); o.hier = o.blick; kalender(); lageF(); }
    else if (tg && !tg.disabled) { setze(o.z, tg.getAttribute('data-tag')); zu(true); }
    else if (zz) {
      var teil = zz.parentNode.getAttribute('data-teil'); if (teil === 'h') o.hh = +zz.getAttribute('data-w'); else o.mm = +zz.getAttribute('data-w');
      [].forEach.call(zz.parentNode.children, function (x) { x.setAttribute('aria-selected', String(x === zz)); x.tabIndex = x === zz ? 0 : -1; });
      setze(o.z, zwei(o.hh) + ':' + zwei(o.mm));
      if (teil === 'm') zu(true); else { var m = o.f.querySelector('[data-teil=m] [aria-selected=true]'); if (m) m.focus({ preventScroll: true }); }
    }
  });
  function taste(e) {
    var o = offen; if (!o) return;
    if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); zu(true); return; }
    if (e.key === 'Tab') { zu(false); return; }
    if (o.z.art === 'date') {
      var a = doc.activeElement, d = a && a.getAttribute && lies(a.getAttribute('data-tag')); if (!d) return;
      var plus = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[e.key];
      if (SP === 'ar' && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) plus = -plus;
      if (e.key === 'PageUp' || e.key === 'PageDown') { e.preventDefault(); d = new Date(d.getFullYear(), d.getMonth() + (e.key === 'PageUp' ? -1 : 1), d.getDate()); }
      else if (plus) { e.preventDefault(); d = new Date(d.getFullYear(), d.getMonth(), d.getDate() + plus); }
      else return;
      d = grenze(o.z.i, d); o.hier = d; o.blick = new Date(d.getFullYear(), d.getMonth(), 1); kalender(); lageF();
    } else {
      var z = doc.activeElement; if (!z || !z.classList || !z.classList.contains('zw__z')) return;
      var n = e.key === 'ArrowDown' ? z.nextElementSibling : e.key === 'ArrowUp' ? z.previousElementSibling : null;
      if (n) { e.preventDefault(); n.focus(); }
      else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); var and = o.f.querySelector('[data-teil=' + (z.parentNode.getAttribute('data-teil') === 'h' ? 'm' : 'h') + '] [aria-selected=true]'); if (and) and.focus(); }
    }
  }
  doc.addEventListener('pointerdown', function (e) { if (offen && !offen.f.contains(e.target) && !offen.z.k.contains(e.target)) zu(false); }, true);
  window.addEventListener('resize', function () { [].forEach.call(doc.querySelectorAll('.zw-nativ'), lege); lageF(); });

  function alle() { [].forEach.call(doc.querySelectorAll('input[type=date],input[type=time]'), ruest); [].forEach.call(doc.querySelectorAll('.zw-nativ'), function (i) { lege(i); if (i._zwAnz && i._zwAnz.textContent !== (i.value || '–:–')) schreibe(i); }); }
  /* nach main.js (legt die Datumszeile an und markiert die Leisten mit eigenem Kalender), dann für alles, was später dazukommt oder sichtbar wird */
  var start = function () { setTimeout(alle, 60); };
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', start); else start();
  setInterval(alle, 700);
  if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(alle);
  window.susZeitwahl = { alle: alle };
})();

/* Besuch · «Gut zu wissen» an der Goldlinie (Robert 31.10.2026): die Linie wächst mit dem Scrollen bis in den Feiern-Knopf, Paare und Knopf erscheinen, wenn sie ins Bild kommen */
(function () {
  'use strict';
  document.querySelectorAll('[data-fg-weg]').forEach(function (w) {
    var l = w.querySelector('.fg-linie'), teile = [].slice.call(w.querySelectorAll('.fg-p,.fg-ende')), takt = 0, im = true;
    function rechne() { takt = 0; var r = w.getBoundingClientRect(), p = Math.max(0, Math.min(1, (innerHeight * .72 - r.top) / r.height)); l.style.transform = 'scaleY(' + p.toFixed(3) + ')'; }
    if (!('IntersectionObserver' in window)) { teile.forEach(function (x) { x.classList.add('da'); }); l.style.transform = 'none'; return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('da'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -10% 0px' });
    teile.forEach(function (x) { io.observe(x); });
    new IntersectionObserver(function (es) { im = es[0].isIntersecting; if (im) rechne(); }, { rootMargin: '20% 0px 20% 0px' }).observe(w);
    addEventListener('scroll', function () { if (im && !takt) takt = requestAnimationFrame(rechne); }, { passive: true });
    addEventListener('resize', rechne); rechne();
  });
})();

/* Startseite «Lauter» (Robert 01.11.2026): das Plakat steigt hoch, sobald es selbst ins Bild tritt */
(function () {
  var f = document.querySelector('#lauter .lu-flyer'); if (!f || !window.wildSpaet) return;
  window.wildSpaet([[f, 'hoch', f]], '0px 0px -8% 0px');
})();
