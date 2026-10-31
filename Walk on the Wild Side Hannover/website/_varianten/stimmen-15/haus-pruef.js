const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
(async () => {
  const b = await webkit.launch();
  for (const W of [1440, 1000, 390]) {
    const p = await (await b.newContext({ viewport: { width: W, height: W > 1100 ? 900 : 650 } })).newPage();
    const fehler = []; p.on('console', m => { if (m.type() === 'error') fehler.push(m.text()); }); p.on('requestfailed', r => fehler.push('fehlt ' + r.url()));
    await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/haus.html', { waitUntil: 'networkidle' });
    const y = await p.evaluate(() => document.getElementById('stimmen').getBoundingClientRect().top + scrollY);
    for (let d = -600; d < 1600; d += 300) { await p.evaluate(v => scrollTo(0, v), y + d); await p.waitForTimeout(200); }
    await p.evaluate(v => { scrollTo(0, v); const l = document.getElementById('leiste'); if (l) l.style.visibility = 'hidden'; }, y - 60);
    await p.waitForTimeout(3500);
    const m = await p.evaluate(() => [document.documentElement.scrollWidth, [...document.querySelectorAll('.et9-logo')].map(i => i.naturalWidth)]);
    await p.locator('#stimmen').screenshot({ path: '_pruef/haus-' + W + '.jpg', type: 'jpeg', quality: 75 });
    console.log(W, 'breite', m[0], 'logos', m[1].join(','), fehler.join(' | '));
  }
  await b.close();
})();
