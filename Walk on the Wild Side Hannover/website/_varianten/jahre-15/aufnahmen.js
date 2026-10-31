// Prüfaufnahmen der Fassungen: Abschnitt #seit2017 je Fassung, nach dem Auftritt. Aufruf: node aufnahmen.js [breite]
const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const path = require('path'), fs = require('fs');
const W = +(process.argv[2] || 1440), H = W > 1100 ? 900 : 650;
const OUT = path.join(__dirname, '_pruef', String(W)); fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await webkit.launch(); const c = await b.newContext({ viewport: { width: W, height: H } });
  for (let n = 0; n <= 15; n++) {
    const nr = String(n).padStart(2, '0'), p = await c.newPage();
    await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/_varianten/jahre-15/' + nr + '.html', { waitUntil: 'networkidle' });
    const y = await p.evaluate(() => { const s = document.getElementById('seit2017'); document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); return s.getBoundingClientRect().top + scrollY; });
    for (let d = -400; d < 4200; d += 300) { await p.evaluate(v => scrollTo(0, v), y + d); await p.waitForTimeout(200); }
    await p.evaluate(v => { scrollTo(0, v); const l = document.getElementById('leiste'); if (l) l.style.visibility = 'hidden'; const v2 = document.querySelector('.vschild'); if (v2) v2.style.display = 'none'; }, y - 80);
    await p.waitForTimeout(3200);
    const m = await p.evaluate(() => { const s = document.getElementById('seit2017'); return [document.documentElement.scrollWidth, Math.round(s.offsetHeight)]; });
    await p.locator('#seit2017').screenshot({ path: path.join(OUT, nr + '.jpg'), type: 'jpeg', quality: 70 });
    console.log(nr, 'breite', m[0], 'hoehe', m[1]); await p.close();
  }
  await b.close();
})();
