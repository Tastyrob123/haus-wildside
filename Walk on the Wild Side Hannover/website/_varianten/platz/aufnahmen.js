// Prüfaufnahmen: #raum und #leute je Fassung nach dem Auftritt. Aufruf: node aufnahmen.js [breite] [nr…]
const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const path = require('path'), fs = require('fs');
const W = +(process.argv[2] || 1440), H = W > 1100 ? 900 : (W > 700 ? 650 : 812);
const nrs = process.argv.slice(3).length ? process.argv.slice(3).map(Number) : [...Array(11).keys()];
const OUT = path.join(__dirname, '_pruef', String(W)); fs.mkdirSync(OUT, { recursive: true });
if (process.argv[2] !== 'pin') (async () => {
  const b = await webkit.launch(); const c = await b.newContext({ viewport: { width: W, height: H } });
  for (const n of nrs) {
    const nr = String(n).padStart(2, '0'), p = await c.newPage();
    await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/_varianten/platz/' + nr + '.html', { waitUntil: 'networkidle' });
    for (const id of ['raum']) {
      const y = await p.evaluate(i => document.getElementById(i).getBoundingClientRect().top + scrollY, id);
      const hh = await p.evaluate(i => document.getElementById(i).offsetHeight, id);
      for (let d = -300; d < hh + 300; d += 250) { await p.evaluate(v => scrollTo(0, v), y + d); await p.waitForTimeout(140); }
      await p.evaluate(v => { scrollTo(0, v); const l = document.getElementById('leiste'); if (l) l.style.visibility = 'hidden'; const s = document.querySelector('.vschild'); if (s) s.style.display = 'none'; }, y + Math.max(0, hh / 2 - H / 2));
      await p.waitForTimeout(2600);
      const m = await p.evaluate(i => [document.documentElement.scrollWidth, document.getElementById(i).offsetHeight], id);
      await p.locator('#' + id).screenshot({ path: path.join(OUT, nr + '-' + id + '.jpg'), type: 'jpeg', quality: 62 });
      console.log(nr, id, 'breite', m[0], 'hoehe', m[1]);
    }
    await p.close();
  }
  await b.close();
})();
// Gehaltene Fassungen (03, 09): zusätzlich Schirmbilder mitten in der Strecke.
if (process.argv[2] === 'pin') (async () => {
  const b = await webkit.launch(); const c = await b.newContext({ viewport: { width: 1440, height: 900 } });
  for (const nr of ['03', '09']) { const p = await c.newPage();
    await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/_varianten/platz/' + nr + '.html', { waitUntil: 'networkidle' });
    const el = await p.evaluate(() => { const s = document.querySelector('[data-pin]'); return [s.getBoundingClientRect().top + scrollY, s.offsetHeight]; });
    for (const f of [0.05, 0.5, 0.95]) { const y = el[0] + f * (el[1] - 900); for (let d = y - 1200; d <= y; d += 300) { await p.evaluate(v => scrollTo(0, v), d); await p.waitForTimeout(120); }
      await p.evaluate(v => { scrollTo(0, v); document.getElementById('leiste').style.visibility = 'hidden'; document.querySelector('.vschild').style.display = 'none'; }, y); await p.waitForTimeout(1500);
      await p.screenshot({ path: path.join(OUT, nr + '-pin-' + f + '.jpg'), type: 'jpeg', quality: 60 }); }
    await p.close(); }
  await b.close(); })();
