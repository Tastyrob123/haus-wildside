/* Wild Side · Abschnitt «Lauter», 15 Fassungen: Setliste (03) und wechselnder Flyer (07). Nur transform. */
(function () {
  'use strict';
  var s = document.getElementById('lauter'); if (!s || !s.classList.contains('lv')) return;
  var v = +s.dataset.v, ruhig = document.documentElement.classList.contains('ruhig');
  var flyer = s.querySelector('.lv-flyer'); if (!flyer || (v !== 3 && v !== 7)) return;
  var abende = JSON.parse(flyer.dataset.abende), name = flyer.querySelector('.fl-name'), datum = flyer.querySelector('.fl-datum');
  var bilder = [].slice.call(flyer.querySelectorAll('img[data-k]'));
  function laden(img) { if (img.dataset.srcset) { img.sizes = img.dataset.sizes || '36vw'; img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); } }
  bilder.forEach(laden);
  var jetzt = bilder.filter(function (i) { return i.classList.contains('an'); })[0];
  function zeige(i) {
    var a = abende[i], img = flyer.querySelector('img[data-k="' + a[3] + '"]');
    name.textContent = a[1]; datum.textContent = a[0] + (a[2] ? ' · ' + a[2] : '');
    if (img === jetzt) return;
    var alt = jetzt; alt.classList.remove('an'); alt.classList.add('war'); img.classList.add('an'); jetzt = img;
    setTimeout(function () { alt.classList.remove('war'); }, 1050);
  }
  if (v === 3) {
    var zeilen = [].slice.call(s.querySelectorAll('.lv03-z'));
    zeilen.forEach(function (z, i) {
      var los = function () { zeilen.forEach(function (x) { x.classList.toggle('an', x === z); }); zeige(i); };
      z.addEventListener('mouseenter', los); z.addEventListener('focus', los); z.addEventListener('click', los);
    });
  }
  if (v === 7 && !ruhig) {
    var n = 0, im = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { im = es[0].isIntersecting; }).observe(s);
    setInterval(function () { if (!im || document.hidden) return; n = (n + 1) % abende.length; zeige(n); }, 3600);
  }
})();
