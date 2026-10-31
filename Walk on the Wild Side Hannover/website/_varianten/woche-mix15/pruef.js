/* Nur für die eigene Prüfung im verdeckten Fenster: Endzustand ohne Übergänge, misst Überlappungen und Breite. */
window.__ruhe = function () {
  var st = document.createElement('style'); st.textContent = '*{transition:none!important;animation:none!important}'; document.head.appendChild(st);
  var h = document.documentElement; h.classList.add('ruhig'); h.classList.remove('einzeln');
  document.querySelectorAll('.vauf,.auf').forEach(function (e) { e.classList.add('da'); });
  dispatchEvent(new Event('scroll'));
  var s = document.getElementById('woche'), R = function (e) { return e.getBoundingClientRect(); }, els = [];
  s.querySelectorAll('.titel,.text,.etikett,.wf').forEach(function (e) { if (e.offsetParent !== null) els.push(e); });
  var hits = [];
  for (var i = 0; i < els.length; i++) for (var j = i + 1; j < els.length; j++) {
    var a = els[i], b = els[j]; if (a.contains(b) || b.contains(a)) continue;
    if (a.closest('.s-platte,.k-blatt,.f-hinten') !== b.closest('.s-platte,.k-blatt,.f-hinten')) continue;
    var x = R(a), y = R(b), ox = Math.min(x.right, y.right) - Math.max(x.left, y.left), oy = Math.min(x.bottom, y.bottom) - Math.max(x.top, y.top);
    if (ox > 2 && oy > 2) hits.push([String(a.className).slice(0, 22), String(b.className).slice(0, 22), Math.round(ox), Math.round(oy)]);
  }
  return { h: s.offsetHeight, docW: h.scrollWidth, anz: hits.length, hits: hits.slice(0, 4) };
};
