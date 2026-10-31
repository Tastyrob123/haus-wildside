/* Die Plakatwerkstatt · Walk on the Wild Side: die fertigen Drucksachen der Bar als PDF (3 mm Beschnitt, Schriften eingebettet) und Vorschaubild,
   gesetzt mit dem Werkzeug selbst (DS.dokument, DS.pdf, DS.png) aus dem Katalog der Bar (katalog.js). Dazu Druckprüfung und Stilprüfung je Stück.
   Aufruf (Server :9087 läuft):  NODE_PATH=$(npm root -g) node _bau/drucksachen.js   → haeuser/wildside/drucksachen/ + LISTE.md */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ZIEL = path.join(__dirname, '..', 'haeuser', 'wildside', 'drucksachen');
const STUECKE = [
  ['session-ghazouani-brothers', 'session', 'SESSION · Ghazouani Brothers, 17.10.2026', 'SESSION-Plakat, Instagram 4:5'],
  ['session-aushang-a3', 'session', 'SESSION · Aushang A3', 'SESSION-Plakat A3 zum Aushang'],
  ['session-story', 'session', 'SESSION · Story', 'SESSION-Plakat als Story 9:16'],
  ['session-programm', 'session', 'Die DJ-Abende', 'Programm der DJ-Abende, A5'],
  ['konzert-live-am-donnerstag', 'feste', 'Live am Donnerstag', 'Konzert-Plakat A3, weisses Plakat der Bar'],
  ['silvester-fruehshoppen', 'feste', 'Silvester Frühshoppen', 'Weisses Plakat «Eure Nachbarschafts-Mixology-Bar», Instagram 4:5'],
  ['tanz-in-den-mai', 'feste', 'Tanz in den Mai', 'Weisses Plakat, Instagram 4:5'],
  ['gastschicht-musa', 'feste', 'Gastschicht · Musa', 'Weisses Plakat zur Gastschicht, Instagram 4:5'],
  ['karte-drunk-in-love', 'karte', 'Drunk in Love · Valentinskarte', 'Getränkekarte DL hoch mit Preisen vom Plakat'],
  ['karte-preise-der-bar', 'karte', 'Die Preise der Bar', 'Preisliste der Bar A5'],
  ['karte-klassiker', 'karte', 'Die Klassiker', 'Karte DL hoch: Negroni, Paloma, Mexikaner, ohne Alkohol'],
  ['untersetzer-was-magst-du', 'karte', 'Was magst du?', 'Tischaufsteller A6: Geschmack, Glas, was hinein soll'],
  ['tischaufsteller-du-sagst', 'karte', 'Du sagst, was du magst', 'Tischaufsteller A6 mit Momo'],
  ['flyer-nachbarschafts-mixology-bar', 'haus', 'Flyer der Bar', 'Flyer A6, vorne Foto, hinten Zeiten'],
  ['aushang-oeffnungszeiten', 'haus', 'Öffnungszeiten', 'Aushang A4'],
  ['instagram-falstaff', 'haus', 'Falstaff Bar Guide 2027', 'Instagram-Beitrag 4:5'],
  ['instagram-negroni', 'karte', 'Der Negroni', 'Instagram-Beitrag 4:5'],
  ['feiern-pauschale', 'feiern', 'Die ganze Bar · Pauschale', 'Angebotsblatt A5 mit den Pauschalen 49/59/79 €'],
  ['feiern-lange-tafel', 'feiern', 'Die lange Tafel', 'Angebotsblatt A5'],
  ['gutschein', 'feiern', 'Gutschein · Ein Abend an der Bar', 'Gutschein DL quer, Vorder- und Rückseite'],
];
(async () => {
  fs.mkdirSync(ZIEL, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  const fehler = []; p.on('pageerror', e => fehler.push(e.message));
  await p.addInitScript(() => { try { localStorage.setItem('ds-wildside-willkommen', '1'); } catch (e) {} });
  await p.goto('http://127.0.0.1:9087/_werkzeuge/imprimerie/', { waitUntil: 'load' });
  await p.waitForFunction(() => window.DS && DS.M && window.DSStudio && DS.pdf, null, { timeout: 30000 });
  await p.waitForTimeout(1500);
  const zeilen = [];
  for (const [k, abt, n, was] of STUECKE) {
    const r = await p.evaluate(async ({ abt, n }) => {
      const x = window.DSKATALOG.ABTEILUNGEN.find(a => a.k === abt).vorlagen.find(v => v.n === n);
      if (!x) return { fehlt: true };
      const seiten = [{ vorlage: x.vorlage, ton: x.ton, inhalt: x.inhalt, stil: x.stil }];
      if (x.rueck) seiten.push({ vorlage: x.rueck.vorlage, ton: x.ton, inhalt: x.rueck.inhalt });
      const doc = DS.dokument(DS.M, { name: 'Walk on the Wild Side · ' + n, format: x.format, seiten });
      const pr = (DS.pruefe(DS.M, doc) || []).filter(h => h.stufe === 'rot').map(h => h.text);
      const { bytes } = await DS.pdf(DS.M, doc, { marken: false });
      const b64 = u => { let s = ''; for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); };
      const bilder = [];
      for (let i = 0; i < seiten.length; i++) { const bl = await DS.png(DS.M, doc, i, 1200), bm = await createImageBitmap(bl), cv = document.createElement('canvas'); cv.width = bm.width; cv.height = bm.height; const g = cv.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, cv.width, cv.height); g.drawImage(bm, 0, 0); const jp = await new Promise(ok => cv.toBlob(ok, 'image/jpeg', .86)); bilder.push(b64(new Uint8Array(await jp.arrayBuffer()))); }
      return { pdf: b64(bytes), bilder, rot: pr, format: DS.FORMATE[x.format].name, seiten: seiten.length };
    }, { abt, n });
    if (r.fehlt) { console.log('FEHLT', n); continue; }
    fs.writeFileSync(path.join(ZIEL, k + '.pdf'), Buffer.from(r.pdf, 'base64'));
    r.bilder.forEach((bi, i) => fs.writeFileSync(path.join(ZIEL, k + (i ? '-' + (i + 1) : '') + '.jpg'), Buffer.from(bi, 'base64')));
    zeilen.push({ k, n, was, format: r.format, seiten: r.seiten, rot: r.rot });
    console.log(k, r.format, r.seiten, 'Seite(n)', r.rot.length ? 'ROT: ' + r.rot.join(' | ') : 'ohne roten Befund');
  }
  zeilen.forEach(x => { x.pdf = x.k + '.pdf'; x.vorschau = Array.from({ length: x.seiten }, (_, i) => x.k + (i ? '-' + (i + 1) : '') + '.jpg'); });
  fs.writeFileSync(path.join(ZIEL, 'liste.json'), JSON.stringify(zeilen, null, 1));
  const md = ['# Drucksachen · Walk on the Wild Side Hannover', '', 'Gesetzt mit der Plakatwerkstatt (`_werkzeuge/imprimerie/`, Aufruf `node _bau/drucksachen.js`), Inhalte nur aus Website, Plakaten und Beiträgen der Bar (`bau_vorlagen.py`).',
    'PDF mit 3 mm Beschnitt und eingebetteten Schriften (Prata, Hanken Grotesk, Rammetto One), Vorschaubild 1200 px breit (JPG). Druckprüfung je Stück: ' + (zeilen.every(x => !x.rot.length) ? 'ohne roten Befund.' : 'siehe liste.json.'), '',
    '| Datei | Drucksache | Was | Format | Seiten | Vorschau |', '|---|---|---|---|---|---|',
    ...zeilen.map(x => `| \`${x.pdf}\` | ${x.n} | ${x.was} | ${x.format} | ${x.seiten} | ${x.vorschau.map(v => '`' + v + '`').join(', ')} |`), '',
    'Hinweis: Der nächste DJ-Abend steht noch nicht fest (kündigt die Bar auf Instagram an); die SESSION-Plakate tragen als Beispiel den Abend vom 17.10.2026, das Foto im Plakat ist ein Bild der Bar in Schwarzweiss und wird im Editor gegen das Gesicht des Abends getauscht.'];
  fs.writeFileSync(path.join(ZIEL, 'LISTE.md'), md.join('\n') + '\n');
  if (fehler.length) console.log('Seitenfehler:', fehler.join('\n'));
  await b.close();
})();
