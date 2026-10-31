// Aufnahmen für den Befund der Werkbank Wild Side (Nachtbau 31.10.2026). Nur lokale Dateien, nichts geht online (alle Anfragen nach aussen werden abgebrochen).
//   node _werkbank/heute/befund_bilder.js   → _werkbank/heute/archiv-handy.jpg (Startseite wildside-hannover.de im Web-Archiv, 390 × 844),
//   mappe-handy.jpg (erste Seite der Angebotsmappe), ig-handy.jpg (Profil auf Instagram, Ausschnitt der Aufnahme des Spähers)
// Quellen nur aus _quelle/ (liegt nur in dieser Sitzung); die Ergebnisse liegen danach im Revier, damit der Bau ohne _quelle läuft.
const path = require('path'), fs = require('fs');
let pw; try { pw = require('playwright'); } catch (e) { pw = require('/opt/node-tools/node_modules/playwright'); }
const HIER = __dirname, Q = path.join(HIER, '..', '..', '..', '..', '_quelle');
(async () => {
  const b = await pw.chromium.launch({ headless: true });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  await p.route('**/*', r => (r.request().url().startsWith('file:') ? r.continue() : r.abort()));
  await p.goto('file://' + path.join(Q, 'web-archiv/html/20250908023546_offline.html'));
  await p.waitForTimeout(800);
  await p.screenshot({ path: path.join(HIER, 'archiv-handy.jpg'), type: 'jpeg', quality: 86 });
  await b.close();
  console.log('befund_bilder fertig');
})();
