/* Kopf, Fuss und Trenner der Mails als PNG (kein Mailprogramm zeigt SVG zuverlässig): die echte Wortmarke in Rot, Trenner als Goldlinie.
   NODE_PATH=$(npm root -g) node _bau/mail_marken.js */
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const Z = path.join(__dirname, '..', 'haeuser', 'wildside', 'mail');
const svg = fs.readFileSync(path.join(__dirname, '..', '..', 'oberflaeche', 'kleid', 'wildside-marke.svg'), 'utf8').replace(/<symbol id="wm" viewBox="[^"]*">/, '').replace('</symbol>', '').replace(/fill="currentColor"/g, 'fill="#F0323F"');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
  const shot = async (html, w, h, f) => { await p.setViewportSize({ width: w, height: h }); await p.setContent(`<style>html,body{margin:0;background:transparent}</style>${html}`); await p.screenshot({ path: path.join(Z, f), omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } }); };
  const logo = (h) => svg.replace('<svg ', `<svg style="height:${h}px;width:auto;display:block" `);
  await shot(`<div style="width:278px;height:64px;display:grid;place-items:center">${logo(64)}</div>`, 278, 64, '_kopf.png');
  await shot(`<div style="width:48px;height:59px">${logo(59)}</div>`, 48, 59, '_fuss.png');
  await shot(`<div style="width:190px;height:30px;position:relative"><i style="position:absolute;left:20px;right:20px;top:14.5px;height:1px;background:#D8B264"></i></div>`, 190, 30, '_trenner.png');
  await b.close();
})();
