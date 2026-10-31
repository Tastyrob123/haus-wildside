/* Das Markenbuch · Walk on the Wild Side Hannover · Bilder für die Listen «Schriften» und «Farben» (Robert 20.10.2026: «in allen Tools Bilder dazu»): je Schrift ein Ausschnitt
   der Website, so wie sie dort steht (nur lesen, unsichtbar, ein Browser, «weniger Bewegung», damit nichts mitten im Auftritt steht); dazu ein Ausschnitt
   eines cremefarbenen Abschnitts (Gruppe «Creme»). Die Website ist meist dunkel: die Schriften dürfen auf dunkler Fläche stehen.
   Aufruf aus bau.py: node listen_bilder.js <zielordner> <adresse der seite> …  → listen/<name>.png (danach in bau.py zu WebP) */
const path = require('path');
const { chromium } = require('playwright');
const [, , ZIEL, ...SEITEN] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2, reducedMotion: 'reduce' });
  // je Wunsch: erstes Element im Wähler, sichtbar, rein in dieser Schrift, 12 bis 120 Zeichen
  const WUNSCH = [['schrift-t', 'Prata', 'h2.titel, h2, h3.titel, h3'], ['schrift-e', 'Hanken', '.etikett'], ['schrift-s', 'Hanken', 'p.text, p'], ['schrift-z', 'Hanken', '.zeiten'], ['farbe-creme', '', 'section.hell, .hell']];
  const offen = async SEITE => {
    await p.goto(SEITE, { waitUntil: 'load' });
    await p.evaluate(async () => { document.documentElement.classList.add('ruhig'); document.querySelectorAll('img').forEach(i => { i.loading = 'eager'; }); await document.fonts.ready; });
    for (let y = 0; y < 40000; y += 700) { const h = await p.evaluate(y => { scrollTo(0, y); return document.body.scrollHeight; }, y); await p.waitForTimeout(30); if (y > h) break; }
  };
  for (const [name, schrift, wahl] of WUNSCH) {
    let box = null;
    for (const SEITE of SEITEN) {
      await offen(SEITE);
      const ziel = await p.evaluate(([schrift, wahl]) => {
        const el = [...document.querySelectorAll(wahl)].find(e => {
          const s = getComputedStyle(e), t = (e.textContent || '').trim().replace(/\s+/g, ' '), r = e.getBoundingClientRect();
          if (!schrift) return r.width > 900 && r.height > 300 && s.display !== 'none';
          const rein = wahl === '.zeiten' || [...e.querySelectorAll('*')].every(k => getComputedStyle(k).fontFamily === s.fontFamily);   // Zeiten: Tage in Hanken, Uhrzeiten in Prata, wie auf der Website
          return rein && (wahl.indexOf('p.text') < 0 || t.length >= 50) && s.fontFamily.includes(schrift) && t.length >= 10 && t.length <= (wahl === '.zeiten' ? 200 : 120) && r.width > 140 && r.height > 10 && r.height < 300
            && s.visibility !== 'hidden' && +s.opacity > .9 && !e.closest('nav,header,footer,.leiste,[aria-hidden="true"]');
        });
        if (!el) return null;
        el.setAttribute('data-livre-probe', '1'); return true;
      }, [schrift, wahl]);
      if (!ziel) continue;
      const loc = p.locator('[data-livre-probe]').first();
      await loc.evaluate(e => e.scrollIntoView({ block: 'center' })); await p.waitForTimeout(900);
      const r = await loc.boundingBox();
      box = schrift ? { x: Math.max(0, r.x - 28), y: Math.max(0, r.y - 14), width: Math.min(r.width + 56, 1440 - Math.max(0, r.x - 28)), height: Math.min(r.height + 28, 900) }
        : { x: 0, y: Math.max(0, r.y), width: 1440, height: Math.min(r.height, 640, 900 - Math.max(0, r.y)) };
      break;
    }
    if (!box) { console.log('nicht gefunden', name); continue; }
    await p.screenshot({ path: path.join(ZIEL, name + '.png'), clip: box });
    console.log('ok', name);
  }
  await b.close();
})();
