// Prüfaufnahmen: Kopf der Seite «Das Haus» je Fassung, so wie er nach dem Auftritt oben steht. Aufruf: node aufnahmen.js [breite]
const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const path = require('path'), fs = require('fs');
const W = +(process.argv[2] || 1440), H = W > 1100 ? 900 : (W > 600 ? 650 : 812);
const OUT = path.join(__dirname, '_pruef', String(W)); fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await webkit.launch(); const c = await b.newContext({ viewport: { width: W, height: H } });
  for (let n = 0; n <= 15; n++) {
    const nr = String(n).padStart(2, '0'), p = await c.newPage();
    await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/_varianten/haus-hero-15/' + nr + '.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => { const v = document.querySelector('.vschild'); if (v) v.style.display = 'none'; });
    await p.waitForTimeout(4200);
    const m = await p.evaluate(() => { const s = document.getElementById('auftakt'); return [document.documentElement.scrollWidth, Math.round(s.offsetHeight)]; });
    await p.screenshot({ path: path.join(OUT, nr + '.jpg'), type: 'jpeg', quality: 70 });
    console.log(nr, 'breite', m[0], 'hoehe', m[1]); await p.close();
  }
  await b.close();
})();
