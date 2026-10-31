/* Nur für die eigene Prüfung: misst Überlappungen in den beiden Abschnitten (ohne Auftritts-Versatz). */
window.__pruef = function () {
  var st = document.createElement('style'); st.textContent = '*{transition:none!important;animation:none!important}'; document.head.appendChild(st);
  document.documentElement.classList.add('ruhig'); document.documentElement.classList.remove('einzeln');
  var secs = [document.getElementById('gespraech'), document.getElementById('technik')], R = function (e) { return e.getBoundingClientRect(); };
  var out = { n: location.pathname.slice(-7, -5), h: secs.map(function (s) { return s.offsetHeight; }) }, els = [];
  secs.forEach(function (s) { s.querySelectorAll('.titel,.text,.etikett,.ge-zitat,.kachel,figure,.platte,.plakat').forEach(function (e) { if (e.offsetParent !== null && !e.closest('.g3-stapel,.g8-stapel,.g13-stapel,.g13-saetze,.g7-tresen')) els.push(e); }); });
  var hits = [];
  for (var i = 0; i < els.length; i++) for (var j = i + 1; j < els.length; j++) {
    var a = els[i], b = els[j]; if (a.contains(b) || b.contains(a)) continue;
    var x = R(a), y = R(b), ox = Math.min(x.right, y.right) - Math.max(x.left, y.left), oy = Math.min(x.bottom, y.bottom) - Math.max(x.top, y.top);
    if (ox > 2 && oy > 2) hits.push([String(a.className || a.tagName).slice(0, 26), String(b.className || b.tagName).slice(0, 26), Math.round(ox), Math.round(oy)]);
  }
  out.anz = hits.length; out.hits = hits.slice(0, 4); out.docW = document.documentElement.scrollWidth; return out;
};
