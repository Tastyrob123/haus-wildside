// Befund 03 «Die guten Noten stehen woanders.»: Aufnahme der Website-Stelle «Drei Zahlen» (haus.html#stimmen: Falstaff 91, Google 4,8 aus 75, NeoTaste 4,8 aus 40)
// am Handy 390 × 844, nur lokal (Server 9088).   node _werkbank/heute/noten_bild.js  → _werkbank/heute/noten-handy.jpg
const path = require('path');
let pw; try { pw = require('playwright'); } catch (e) { pw = require('/opt/node-tools/node_modules/playwright'); }
(async () => {
  const b = await pw.chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  await p.goto('http://127.0.0.1:9088/haus.html', { waitUntil: 'load', timeout: 60000 });
  await p.evaluate(() => document.fonts && document.fonts.ready);
  for (let y = 0; y < 30; y++) { await p.evaluate(() => scrollBy(0, innerHeight * .8)); await p.waitForTimeout(120); }
  await p.evaluate(() => { const s = document.getElementById('stimmen'); const h = s.querySelector('h2') || s; h.scrollIntoView({ block: 'start' }); scrollBy(0, 110); });
  await p.waitForTimeout(2500);
  await p.screenshot({ path: path.join(__dirname, 'noten-handy.jpg'), type: 'jpeg', quality: 88 });
  await b.close();
  console.log('noten-handy.jpg');
})();
