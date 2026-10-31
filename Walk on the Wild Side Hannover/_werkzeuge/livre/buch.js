/* Die Hausregeln · Walk on the Wild Side Hannover (Kopie aus dem Markenbuch von Culinarium): «Als PDF sichern» öffnet das Druckfenster des Browsers
   (je Kapitel eine A4-Seite quer, buch.css @media print); ein Klick auf eine Farbe kopiert ihren Wert; Blätter heben sich beim Hereinkommen leicht
   (nur transform, deckend ab dem ersten Bild, «weniger Bewegung» beachtet). Fotos laden zuerst nur im Blick (lazy); vor dem Druck werden alle geholt. */
'use strict';
(function () {
  const alle = () => Promise.all([...document.images].map(i => { i.loading = 'eager'; return i.complete ? 0 : new Promise(r => { i.addEventListener('load', r, { once: true }); i.addEventListener('error', r, { once: true }); }); }));
  const b = document.getElementById('bu-pdf');
  if (b) b.addEventListener('click', () => alle().then(() => window.print()));
  addEventListener('beforeprint', () => { [...document.images].forEach(i => { i.loading = 'eager'; }); });
  addEventListener('load', () => setTimeout(alle, 1200));
  /* Farbe kopieren */
  const melde = t => { const m = document.getElementById('meldung'); if (!m) return; m.textContent = t; m.classList.add('an'); clearTimeout(melde.u); melde.u = setTimeout(() => m.classList.remove('an'), 1800); };
  document.querySelectorAll('[data-hex]').forEach(k => k.addEventListener('click', () => {
    const w = k.dataset.hex, ok = () => { k.classList.add('kopiert'); setTimeout(() => k.classList.remove('kopiert'), 1400); melde('Kopiert · ' + w); };
    if (navigator.clipboard && isSecureContext) navigator.clipboard.writeText(w).then(ok, ok); else ok();
  }));
  document.querySelectorAll('[data-hex][role="button"]').forEach(k => k.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); k.click(); } }));
  /* Auftritt: was im ersten Bild steht, hebt sich der Reihe nach (höchstens vier Stufen), alles darunter beim Hereinkommen; nie unsichtbar */
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  document.documentElement.classList.add('bewegt');
  const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { x.target.classList.add('da'); io.unobserve(x.target); } }), { rootMargin: '0px 0px -6% 0px' });
  let n = 0;
  document.querySelectorAll('[data-r]').forEach(el => { const r = el.getBoundingClientRect(); if (r.top < innerHeight) el.style.setProperty('--i', Math.min(n++, 4)); io.observe(el); });
})();
