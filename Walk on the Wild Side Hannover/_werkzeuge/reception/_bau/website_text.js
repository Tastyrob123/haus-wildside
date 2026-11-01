// Wortlaut der Website von Walk on the Wild Side, wie ein Gast ihn sieht (31.10.2026): innerText jeder Seite, headless, nur lesen.
// Quelle für _bau/wildside_wissen.py. Aufruf aus dem Hausordner: node _werkzeuge/reception/_bau/website_text.js [basis, Standard http://127.0.0.1:9284]
// (der Server des Gästebuchs liefert die Website unter / aus, nur lesend)
const path = require('path'), fs = require('fs');
const { chromium } = require('playwright');
const BASIS = process.argv[2] || 'http://127.0.0.1:9284';
const SEITEN = ['index', 'drinks', 'programm', 'tafel', 'haus', 'besuch', 'impressum', 'datenschutz'];
const ZIEL = path.join(__dirname, 'website-text');
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  for (const f of fs.readdirSync(ZIEL)) if (f.endsWith('.txt') && !SEITEN.includes(f.slice(0, -4))) fs.unlinkSync(path.join(ZIEL, f));
  const br = await chromium.launch({ headless: true });
  const c = await br.newContext({ viewport: { width: 1440, height: 900 }, reducedMotion: 'reduce' });
  await c.route(/^(mailto|tel|sms):/, r => r.abort());
  const p = await c.newPage();
  for (const s of SEITEN) {
    await p.goto(`${BASIS}/${s}.html`, { waitUntil: 'networkidle' });
    await p.waitForTimeout(400);
    const t = await p.evaluate(() => {
      // Wortlaut, nicht die Versalien der Schrift; alles, was beim Scrollen erst erscheint, sichtbar
      document.querySelectorAll('body *').forEach(e => e.style.setProperty('text-transform', 'none', 'important'));
      document.querySelectorAll('.jetzt,[data-heute-satz]').forEach(e => e.remove());   // «heute» rechnet die Seite aus dem Tag des Abrufs
      // die Vorführung des Formulars («In diesem Entwurf wird nichts verschickt», Danke-Zustand) ist keine Angabe des Hauses
      document.querySelectorAll('script,noscript,style,svg,[hidden],[aria-hidden="true"],.hinweis,.dank,select,input,textarea').forEach(e => e.remove());
      // Überschriften als «## …» (eine Zeile, wie gesprochen): daran teilt «Das weiss der Chat» die Seiten in Abschnitte
      document.querySelectorAll('main h1, main h2, section h1, section h2, header h1').forEach(h => { const t = (h.getAttribute('aria-label') || h.innerText).replace(/\s+/g, ' ').trim(); if (t) h.textContent = '## ' + t; });
      return document.body.innerText;
    });
    const zeilen = []; const da = new Set();
    for (let z of t.split('\n')) { z = z.replace(/\s+/g, ' ').trim(); if (!z || da.has(z)) continue; da.add(z); zeilen.push(z); }
    fs.writeFileSync(path.join(ZIEL, s + '.txt'), `Quelle: ${s}.html (Website Walk on the Wild Side)\nAbgerufen: ${new Date().toISOString().slice(0, 10)}\n\n` + zeilen.join('\n') + '\n');
    console.log(s, zeilen.length, 'Zeilen');
  }
  await br.close();
})();
