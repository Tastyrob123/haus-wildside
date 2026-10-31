/* Nur für die eigene Prüfung: alles sofort zeigen, Bilder laden, zum Abschnitt springen. */
window.__zeig = function (dy) {
  var st = document.createElement('style'); st.textContent = '*{transition:none!important;animation:none!important}'; document.head.appendChild(st);
  document.querySelectorAll('.auf,.vauf').forEach(function (e) { e.classList.add('da'); });
  document.querySelectorAll('.einz').forEach(function (e) { e.classList.add('ein'); });
  document.querySelectorAll('img[data-srcset]').forEach(function (i) { i.sizes = i.dataset.sizes || '100vw'; i.srcset = i.dataset.srcset; i.removeAttribute('data-srcset'); });
  var k = document.getElementById('karte'); scrollTo(0, k.getBoundingClientRect().top + scrollY + (dy || 0));
  var R = function (e) { return e.getBoundingClientRect(); }, els = [].slice.call(k.querySelectorAll('.titel,.text,.etikett,figure,.knopf,small,p'));
  var hits = 0; for (var i = 0; i < els.length; i++) for (var j = i + 1; j < els.length; j++) { var a = els[i], b = els[j]; if (a.contains(b) || b.contains(a) || a.offsetParent === null || b.offsetParent === null) continue;
    var x = R(a), y = R(b); if (Math.min(x.right, y.right) - Math.max(x.left, y.left) > 2 && Math.min(x.bottom, y.bottom) - Math.max(x.top, y.top) > 2) hits++; }
  return { h: k.offsetHeight, ueberlapp: hits, breit: document.documentElement.scrollWidth };
};
