/* Rücksprung (Robert 1.11.2026): Zurück/Vor im Browser landet auf der alten Höhe der Seite, nie ganz oben.
   Merkt je Seite in sessionStorage (rs:<Pfad>) die Höhe und das Inhaltsstück am oberen Fensterrand (beim Scrollen, beim Klick auf einen Link, bei pagehide).
   Kommt man mit Zurück/Vor wieder (Navigation «back_forward»), richtet sich die Seite nach dem Aufbau an diesem Stück aus, nicht nur an der Pixelzahl:
   Abschnitte mit content-visibility:auto stehen nach dem Laden als 1400-px-Platzhalter da, dieselbe Pixelhöhe zeigt sonst anderen Inhalt.
   Für den Moment des Sprungs: alles einmal gezeichnet, keine Übergänge, keine Auftakt-Bewegung (rs-sofort); alles bis zum Fensterrand gilt als gezeigt (.da).
   Aus dem bfcache stellt der Browser die Höhe selbst her. Keine unload-Handler. Seiten mit eigenem Rückweg (#rh-zurueck, «wb-y») und Rahmen bleiben unberührt. */
(function () {
  if (document.getElementById('rh-zurueck')) return;
  try { if (window.top !== window) return; } catch (e) { return; }
  var K = 'rs:' + location.pathname, H = document.documentElement, sperre = false, t = 0;
  var SEL = 'h1,h2,h3,h4,h5,p,li,figure,img,picture,video,blockquote,table,tr,section,article,header,footer';
  function fest(e) { for (var n = 0; e && e !== document.body && n < 12; e = e.parentElement, n++) { var p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') return true; } return false; }
  function text(e) { return (e.textContent || e.getAttribute('src') || '').replace(/\s+/g, ' ').trim().slice(0, 40); }
  function anker() {   /* das Inhaltsstück auf einem Drittel der Fensterhöhe (nicht die schwebende Leiste) */
    if (!document.elementsFromPoint) return null;
    var l = null, xs = [.5, .25, .75];
    for (var k = 0; k < xs.length; k++) {
      var st = document.elementsFromPoint(innerWidth * xs[k], innerHeight * .3);
      for (var j = 0; j < st.length; j++) { var c = st[j].closest && st[j].closest(SEL); if (c && !fest(c)) { l = c; break; } }
      if (l) break;
    }
    if (!l) return null;
    var alle = document.querySelectorAll(SEL), i = [].indexOf.call(alle, l);
    return i < 0 ? null : { i: i, n: l.tagName, t: text(l), o: Math.round(l.getBoundingClientRect().top) };
  }
  function merk(mitAnker) {
    if (sperre) return;
    var w = { y: Math.round(window.scrollY || 0) };
    if (mitAnker) { try { var a = anker(); if (a) w.a = a; } catch (e) {} }
    else { try { var alt = JSON.parse(sessionStorage.getItem(K) || '{}'); if (alt.a && Math.abs(alt.y - w.y) < 2) w.a = alt.a; } catch (e) {} }
    try { sessionStorage.setItem(K, JSON.stringify(w)); } catch (e) {}
  }
  addEventListener('scroll', function () { if (!t) t = setTimeout(function () { t = 0; merk(false); }, 150); }, { passive: true });
  document.addEventListener('click', function (ev) { if (ev.target.closest && ev.target.closest('a[href]')) merk(true); }, true);
  addEventListener('pagehide', function () { merk(true); });

  var nav; try { nav = performance.getEntriesByType('navigation')[0]; } catch (e) {}
  if (!nav || nav.type !== 'back_forward') return;
  var w; try { w = JSON.parse(sessionStorage.getItem(K)); } catch (e) {}
  if (!w || typeof w.y !== 'number' || w.y < 2) return;
  sperre = true;
  try { history.scrollRestoration = 'manual'; } catch (e) {}
  var st = document.createElement('style');
  st.textContent = 'html.rs-sofort,html.rs-sofort *{transition:none!important;animation-duration:0s!important;animation-delay:0s!important;scroll-behavior:auto!important}'
    + 'html.rs-ganz *{content-visibility:visible!important}';
  (document.head || H).appendChild(st);
  H.classList.add('rs-sofort', 'rs-ganz');
  var weg = false;
  function fertig() { sperre = false; H.classList.remove('rs-ganz'); }
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (k) { addEventListener(k, function () { weg = true; fertig(); }, { once: true, passive: true }); });
  function stueck() {   /* das gemerkte Stück wiederfinden (gleiche Stelle, sonst in der Nähe mit gleichem Anfang) */
    var a = w.a; if (!a) return null;
    var alle = document.querySelectorAll(SEL), e = alle[a.i];
    if (e && e.tagName === a.n && text(e) === a.t) return e;
    for (var d = 1; d < 40; d++) for (var s = -1; s <= 1; s += 2) { e = alle[a.i + s * d]; if (e && e.tagName === a.n && text(e) === a.t) return e; }
    return null;
  }
  function ziel() { var e = stueck(); return e ? Math.max(0, Math.round(window.scrollY + e.getBoundingClientRect().top - w.a.o)) : w.y; }
  function zeig() {
    var g = window.scrollY + innerHeight;
    [].forEach.call(document.querySelectorAll('[data-a],.odo,.zt,.roll,img.ld'), function (e) {
      if (!e.classList.contains('da') && e.getBoundingClientRect().top + window.scrollY < g) e.classList.add('da');
    });
  }
  function geh() { if (weg) return; var y = ziel(); if (Math.abs(window.scrollY - y) > 2) window.scrollTo(0, y); zeig(); }
  function los() {
    geh();
    requestAnimationFrame(function () { geh(); requestAnimationFrame(function () { geh(); H.classList.remove('rs-sofort'); }); });
    var n = 0, iv = setInterval(function () {
      n++; geh();
      if (n >= 16 || weg) { clearInterval(iv); geh(); fertig(); requestAnimationFrame(function () { geh(); merk(true); }); }
    }, 150);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', los); else los();
  addEventListener('load', function () { if (sperre) geh(); });
})();
