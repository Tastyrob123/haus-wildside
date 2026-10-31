// Vorher/Nachher-Aufnahmen der Kundenwünsche (30.10.2026): je Stelle ein Bild vom alten und vom neuen Stand.
const { webkit } = require('/Users/robertreff/Desktop/Apps & Tools/Tasty Website Builder/node_modules/playwright');
const path = require('path');
const BASIS = 'http://localhost:8978/haus/Walk%20on%20the%20Wild%20Side%20Hannover/';
const STAND = { vorher: '_vorher-kundenwuensche-2026-10-30/website/', nachher: 'website/' };
const STELLEN = [['bildwand', 'index.html', '#bar'], ['jahre', 'index.html', '#seit2017'], ['live', 'index.html', '#lauter'],
                 ['tafel', 'index.html', '#tafel'], ['haus-jahre', 'haus.html', '#seit2017'], ['feiern-bar', 'tafel.html', '#bar']];
(async () => {
  const b = await webkit.launch();
  const c = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, locale: 'de-DE' });
  for (const [st, ordner] of Object.entries(STAND)) for (const [name, seite, sel] of STELLEN) {
    const p = await c.newPage();
    await p.goto(BASIS + ordner + seite, { waitUntil: 'networkidle' });
    await p.evaluate(async (sel) => {
      document.documentElement.classList.add('ruhig');
      document.querySelectorAll('img[data-srcset]').forEach(i => { i.srcset = i.dataset.srcset; });
      document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
      const el = document.querySelector(sel); el.scrollIntoView();
      document.querySelectorAll('.auf,.sw,.hoch').forEach(e => e.classList.add('da', 'ein'));
      const l = document.getElementById('leiste'); if (l) l.style.display = 'none';
      await new Promise(r => setTimeout(r, 2500));
    }, sel);
    await p.waitForTimeout(3500);
    await p.locator(sel).first().screenshot({ path: path.join(__dirname, 'bilder', `${name}-${st}.jpg`), quality: 82, type: 'jpeg' });
    console.log(st, name); await p.close();
  }
  await b.close();
})();
