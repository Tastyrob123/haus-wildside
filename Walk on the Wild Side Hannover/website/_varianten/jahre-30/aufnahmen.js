// Prüfaufnahmen der 30 Fassungen (WebKit wie Safari). Aufruf: node aufnahmen.js [breite] [von] [bis]
// Abschnitt nach dem Auftritt; bei stehenden Bühnen drei Bilder (Anfang, Mitte, Ende). Meldet Überbreite und Text, der aus seiner Fläche läuft.
const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const path = require('path'), fs = require('fs');
const W = +(process.argv[2] || 1440), H = W > 1100 ? 900 : 650, VON = +(process.argv[3] || 0), BIS = +(process.argv[4] || 30);
const OUT = path.join(__dirname, '_pruef', String(W)); fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await webkit.launch(); const c = await b.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  for (let n = VON; n <= BIS; n++) {
    const nr = String(n).padStart(2, '0'), p = await c.newPage(), f = [];
    p.on('pageerror', e => f.push(e.message));
    await p.goto('http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/website/_varianten/jahre-30/' + nr + '.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => { const v = document.querySelector('.vschild'); if (v) v.style.display = 'none'; });
    const pin = await p.evaluate(() => !!document.querySelector('#seit2017 .pin'));
    const y = await p.evaluate(() => document.getElementById('seit2017').getBoundingClientRect().top + scrollY);
    for (let d = -400; d < 2400; d += 300) { await p.evaluate(v => scrollTo(0, v), y + d); await p.waitForTimeout(120); }
    if (pin) {
      for (const [k, fr] of [['a', 0], ['b', .5], ['c', 1]]) {
        await p.evaluate(fr => { const q = document.querySelector('#seit2017 .pin'); const t = q.getBoundingClientRect().top + scrollY; scrollTo(0, t + fr * (q.offsetHeight - innerHeight)); }, fr);
        await p.waitForTimeout(1500);
        await p.screenshot({ path: path.join(OUT, nr + k + '.jpg'), type: 'jpeg', quality: 62 });
      }
      await p.evaluate(v => scrollTo(0, v), y - 40); await p.waitForTimeout(1500);
      await p.screenshot({ path: path.join(OUT, nr + '0.jpg'), type: 'jpeg', quality: 62 });
    } else {
      await p.evaluate(v => scrollTo(0, v), y - 80); await p.waitForTimeout(3600);
      await p.locator('#seit2017').screenshot({ path: path.join(OUT, nr + '.jpg'), type: 'jpeg', quality: 62 });
    }
    const m = await p.evaluate(() => {
      const s = document.getElementById('seit2017'), raus = [];
      s.querySelectorAll('.jt,.jx,.v05-t,.v21-t,.v26-f,.v22-u').forEach(e => { if (e.scrollHeight > e.clientHeight + 2 && getComputedStyle(e).overflow !== 'visible') raus.push(e.className); });
      return [document.documentElement.scrollWidth, Math.round(s.offsetHeight), raus.slice(0, 4)];
    });
    console.log(nr, 'breite', m[0], 'hoehe', m[1], 'raus', JSON.stringify(m[2]), f.length ? 'FEHLER ' + f.join(' | ') : '');
    await p.close();
  }
  await b.close();
})();
