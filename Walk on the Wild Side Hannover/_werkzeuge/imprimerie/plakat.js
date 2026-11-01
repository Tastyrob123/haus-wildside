/* Plakatwerkstatt · Walk on the Wild Side Hannover (31.10.2026, Form der Plakatwerkstatt des Stammhauses): zwei Ansichten.
   1. «Plakat-Grund» (#msMotive): die rot-cremefarbenen Wellen der SESSION-Plakate und die Gesichter in Schwarzweiss, jedes gleich als SESSION-Plakat;
      «Als Plakat öffnen» öffnet es im Editor.
   2. «DJ-Abend anlegen» (#msAbend): Baukasten mit Live-Vorschau (1.11.2026): Angaben, eigenes Foto (wird schwarzweiss), Plakat-Grund, Schrift lesbar setzen;
      eins wählen, dann im Editor wie gewohnt: Foto tauschen (das Gesicht des Abends), Texte als Ebenen, Speichern, PDF A3 und PNG 4:5 / 9:16.
   Gesetzt wird mit dem Aufbau «plakat» (vorlagen.js). Nur Lesen: Marke (DS.M), motive.json. */
(function () {
  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  const ZWEI = n => (n < 10 ? '0' : '') + n;
  const PFEIL = '<svg viewBox="0 0 24 24"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>';
  let MOTIVE = [];
  const FUSS = 'HAASEMANNSTR. 13\n30449 HANNOVER';

  /* nächste Samstage ab heute: die DJ-Abende sind samstags (website/programm.html) */
  function samstage(n) {
    const d = new Date(); d.setHours(12, 0, 0, 0); d.setDate(d.getDate() + ((6 - d.getDay() + 7) % 7 || 7));
    return Array.from({ length: n }, (_, i) => { const f = new Date(d); f.setDate(d.getDate() + 7 * i); return f; });
  }
  const tag = d => `Sa ${d.getDate()}. ${MONATE[d.getMonth()]} ${d.getFullYear()}`;
  const pdat = d => `${ZWEI(d.getDate())}|${ZWEI(d.getMonth() + 1)}`;
  const wellen = () => MOTIVE.map(m => m.key);
  const gesichter = () => (DS.M.bilder || []).filter(b => b.gruppe === 'Schwarzweiss').map(b => b.key);

  /* Das SESSION-Plakat als Drucksache; Texte sind eigene Ebenen (SESSION, SIP & SOUNDS, Name, Datum, Uhrzeit, Adresse) */
  function plakatDoc(o) {
    const M = DS.M, d = o.samstag || samstage(1)[0];
    const inhalt = { bild: o.gesicht || gesichter()[0] || null, grundbild: o.welle || wellen()[0] || 'welle-1', ueber: 'SESSION', unter: 'SIP &\nSOUNDS',
      name: String(o.name || '').toUpperCase(), tag: o.tag || pdat(d), zeit: String(o.zeit || '9 PM TO 1 AM').toUpperCase(), fuss: FUSS };
    const name = 'SESSION' + (o.name ? ' · ' + o.name : '') + ' · ' + (o.titel || tag(d));
    return DS.dokument(M, { name, format: o.format || 'insta', seiten: [{ vorlage: 'plakat', ton: 'session', inhalt }] });
  }
  function fach(raster, n) {
    const w = raster.clientWidth || 900, breit = matchMedia('(min-width:700px)').matches;
    const sp = !breit ? 1 : n == 4 ? 2 : 3;
    return Math.round(Math.max(230, Math.min(400, (w - (sp - 1) * 26) / sp / 1.05)));
  }
  function karte(doc, titel, unter, knopf, groesse) {
    const k = document.createElement('div'); k.className = 'pk-karte pk-karte--eins';
    const box = groesse || 230, S = window.DSStudio;
    const b = document.createElement('div'); b.className = 'pk-blaetter pk-blaetter--eins';
    b.style.cssText = `height:${Math.round(box * 1.25 + 20)}px`;
    try { const v = S.miniBox(doc, 0, box * 1.25); v.classList.add('pk-vorn'); b.appendChild(v); } catch (e) { console.warn(e); }
    k.appendChild(b);
    k.insertAdjacentHTML('beforeend', `<div class="pk-text"><b>${esc(titel)}</b><small>${esc(unter)}</small></div>
      <button class="kn knopf--voll pk-los" type="button"><span>${esc(knopf)}</span><i>${PFEIL}</i></button>`);
    k.querySelector('.pk-los').addEventListener('click', () => { DSStudio.oeffne(doc); if (DSStart.offen()) DSStart.zu(); });
    return k;
  }

  /* ---------- 1 Plakat-Grund: Wellen und Gesichter ---------- */
  function zeichneMotive() {
    const box = $('#pkMotive'); if (!box) return;
    $('#pkFilter').innerHTML = '';
    const G = gesichter(), W = wellen(), alt = k => ((DS.M.bildIndex || {})[k] || {}).alt || k;
    box.innerHTML = '';
    $('#pkMotivZahl').textContent = `${W.length} Wellen und ${G.length} Gesichter in Schwarzweiss`;
    W.forEach((w, i) => box.appendChild(karte(plakatDoc({ welle: w, gesicht: G[i % G.length], titel: 'Wellen ' + (i + 1) }), MOTIVE[i].titel, 'Rot und Creme, gerechnet wie die Wellen der echten Plakate', 'Als Plakat öffnen')));
    G.forEach((g, i) => box.appendChild(karte(plakatDoc({ welle: W[i % W.length], gesicht: g, titel: alt(g) }), alt(g).replace(/, schwarzweiss$/, ''), 'Schwarzweiss, für das Gesicht des Abends', 'Als Plakat öffnen')));
  }

  /* ---------- 2 DJ-Abend anlegen: Baukasten mit Live-Vorschau (Robert 1.11.2026) ----------
     Eine feste Vorlage (das SESSION-Plakat), dazu frei: das Foto des Abends (hochladen, auch in Farbe, wird hier im Browser schwarzweiss;
     oder ein Gesicht der Bar), der Plakat-Grund (die Wellen), und für Kopf, Name, Datum und Zusatzzeile je Farbe, Hinterlegung, Grösse und Lage.
     Die Lesbarkeit wird mitgerechnet (Kontrast unter 4,5:1 → Hinweis mit Vorschlag). Ohne KI, ohne Server: Fotos liegen wie «Meine Medien» im Browser. */
  const SPEICHER = 'ds-wildside-djabend';
  const FARBEN = [['blau', 'Ultramarin'], ['rot', 'Plakatrot'], ['creme', 'Creme'], ['nacht', 'Nacht']];
  const TEILE = [['kopf', 'SESSION und SIP & SOUNDS'], ['name', 'Name'], ['datum', 'Datum und Uhrzeit'], ['zusatz', 'Zusatzzeile']];
  const LAGEN = { kopf: [['ol', 'Oben links']], name: [['mr', 'Mitte rechts'], ['or', 'Oben rechts'], ['ur', 'Unten rechts'], ['ul', 'Unten links']],
    datum: [['ur', 'Unten rechts'], ['ul', 'Unten links'], ['or', 'Oben rechts'], ['mr', 'Mitte rechts']], zusatz: [['or', 'Oben rechts'], ['mr', 'Mitte rechts'], ['ur', 'Unten rechts'], ['ul', 'Unten links']] };
  /* gleich gut lesbar: Name und Datum auf einem Creme-Feld, die Zusatzzeile hell auf Nacht; SESSION bleibt wie auf den Plakaten der Bar */
  const START = { kopf: { farbe: 'blau', feld: '', groesse: 'M', lage: 'ol' }, name: { farbe: 'blau', feld: 'creme', groesse: 'M', lage: 'mr' },
    datum: { farbe: 'blau', feld: 'creme', groesse: 'M', lage: 'ur' }, zusatz: { farbe: 'creme', feld: 'nacht', groesse: 'M', lage: 'or' } };
  let BK = null, zeichnen = 0;
  const lies = () => { try { return JSON.parse(localStorage.getItem(SPEICHER) || 'null'); } catch (e) { return null; } };
  const merke = () => { try { localStorage.setItem(SPEICHER, JSON.stringify(BK)); } catch (e) { } };
  function zustand() {
    if (BK) return BK;
    const alt = lies() || {};
    BK = { bild: alt.bild || null, welle: alt.welle || null, bildlage: alt.bildlage || { fx: .5, fy: .5, zoom: 1 }, format: alt.format || 'insta', swVon: alt.swVon || {},
      gestalt: JSON.parse(JSON.stringify(START)) };
    TEILE.forEach(([k]) => Object.assign(BK.gestalt[k], (alt.gestalt || {})[k] || {}));
    return BK;
  }
  /* Kontrast nach WCAG */
  const hex = f => (DS.M.farben || {})[f] || f;
  const lum = h => { const n = parseInt(String(hex(h)).slice(1), 16), c = [n >> 16 & 255, n >> 8 & 255, n & 255].map(v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }); return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]; };
  const kontrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  function lesbar(k) {   // schlechtester Kontrast gegen das, was hinter dem Text liegt: das Feld, sonst Rot und Creme der Wellen
    const s = zustand().gestalt[k], f = s.farbe || 'blau', hinter = s.feld ? [s.feld === 'nacht' ? 'nacht' : 'creme'] : ['rot', 'creme'];
    return Math.min(...hinter.map(h => kontrast(f, h)));
  }
  function werte() {
    const name = $('#pkThema').value.trim(), zeit = $('#pkGast').value.trim() || '9 PM TO 1 AM', zusatz = ($('#pkZusatz') || { value: '' }).value.trim();
    const sa = new Date(($('#pkFreitag').value || samstage(1)[0].toISOString().slice(0, 10)) + 'T12:00:00');
    return { name: name || 'Name des DJs', zeit, zusatz, samstag: sa };
  }
  function bauDoc(format, welle) {
    const s = zustand(), w = werte(), G = gesichter();
    const bild = s.bild && DS.M.bildIndex[s.bild] ? s.bild : G[0];
    const doc = plakatDoc({ name: w.name, zeit: w.zeit, samstag: w.samstag, welle: welle || s.welle || wellen()[0], gesicht: bild, format: format || s.format });
    const q = doc.seiten[0].quelle || {};
    const inh = Object.assign({}, q.inhalt || {}, { gestalt: JSON.parse(JSON.stringify(s.gestalt)), bildlage: Object.assign({}, s.bildlage), zusatz: w.zusatz ? w.zusatz.toUpperCase() : '' });
    return DS.dokument(DS.M, { name: doc.name, format: format || s.format, seiten: [{ vorlage: 'plakat', ton: 'session', inhalt: inh }] });
  }
  function vorschau() {
    clearTimeout(zeichnen);
    zeichnen = setTimeout(() => {
      const box = $('#bkBlatt'); if (!box || !window.DSStudio) return;
      const breit = matchMedia('(min-width:1100px)').matches, F = DS.FORMATE[zustand().format] || { b: 4, h: 5 };
      const bw = (box.clientWidth || 320) - 4, h = Math.min(breit ? Math.min(600, innerHeight - 200) : 520, Math.floor(bw * F.h / F.b));   // nie breiter als die Spalte
      try { const v = DSStudio.miniBox(bauDoc(), 0, Math.max(200, h)); box.replaceChildren(v); } catch (e) { console.warn(e); }
      const w = werte(); $('#bkUnter').textContent = `${w.name} · ${tag(w.samstag)} · ${(DS.FORMATE[zustand().format] || {}).name || ''}`;
      pruefeLesbar(); merke();
    }, 90);
  }
  function pruefeLesbar() {
    const p = $('#bkPruefung'); if (!p) return;
    const schlecht = TEILE.filter(([k]) => k !== 'kopf' && (k !== 'zusatz' || ($('#pkZusatz') || { value: '' }).value.trim()) && lesbar(k) < 4.5);
    const gk = zustand().gestalt.kopf, kopf = !(gk.farbe === 'blau' && !gk.feld) && lesbar('kopf') < 3;   // SESSION in Ultramarin auf den Wellen ist das Zeichen der Plakate der Bar; sonst gilt für die grosse Schrift 3:1
    if (!schlecht.length && !kopf) { p.className = 'bk-pruefung bk-pruefung--gut'; p.textContent = 'Gut lesbar: jeder Text hebt sich genug vom Grund ab.'; return; }
    const namen = schlecht.map(([, n]) => n).concat(kopf ? ['SESSION'] : []);
    p.className = 'bk-pruefung bk-pruefung--hinweis';
    p.innerHTML = `<span>Schwer zu lesen auf den Wellen: ${esc(namen.join(', '))}. Vorschlag: ein Creme-Feld dahinter, die Schrift in Ultramarin.</span> <button type="button" class="ms-lnk" id="bkVorschlag">Vorschlag übernehmen</button>`;
    $('#bkVorschlag').addEventListener('click', () => {
      schlecht.forEach(([k]) => Object.assign(zustand().gestalt[k], { feld: 'creme', farbe: 'blau' }));
      if (kopf) Object.assign(zustand().gestalt.kopf, { farbe: 'blau', feld: 'creme' });
      zeichneSchrift(); vorschau();
    });
  }
  /* Foto des Abends: hochladen → schwarzweiss (Graustufen, etwas mehr Kontrast) → eigenes Foto im Browser */
  async function schwarzweiss(datei) {
    let bild;
    try { bild = await createImageBitmap(datei, { imageOrientation: 'from-image' }); }
    catch (e) { bild = await new Promise((ok, nein) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => nein(new Error('Dieses Bildformat kann der Browser nicht lesen (HEIC öffnet Safari). Bitte als JPG oder PNG speichern.')); i.src = URL.createObjectURL(datei); }); }
    const k = Math.min(1, 3600 / Math.max(bild.width, bild.height)), cv = document.createElement('canvas'); cv.width = Math.round(bild.width * k); cv.height = Math.round(bild.height * k);
    const g = cv.getContext('2d'); g.imageSmoothingQuality = 'high'; g.drawImage(bild, 0, 0, cv.width, cv.height);
    const d = g.getImageData(0, 0, cv.width, cv.height), p = d.data;
    for (let j = 0; j < p.length; j += 4) { let l = .2126 * p[j] + .7152 * p[j + 1] + .0722 * p[j + 2]; l = (l - 128) * 1.18 + 128; l = l < 0 ? 0 : l > 255 ? 255 : l; p[j] = p[j + 1] = p[j + 2] = l; }
    g.putImageData(d, 0, 0);
    const blob = await new Promise(ok => cv.toBlob(ok, 'image/jpeg', .92));
    return new File([blob], (datei.name || 'foto').replace(/\.[^.]+$/, '') + ' schwarzweiss.jpg', { type: 'image/jpeg' });
  }
  async function alsEigenes(datei, m) {   // Datei → schwarzweiss → eigenes Foto im Browser, wird gleich das Foto des Abends
    m.textContent = 'Das Foto wird schwarzweiss …';
    const sw = await schwarzweiss(datei);
    const neu = await DS.eigene.hinzu(DS.M, [sw], t => { m.textContent = t; });
    if (!neu.length) throw new Error('Das Foto liess sich nicht lesen.');
    const s = zustand(); s.bild = neu[0]; s.bildlage = { fx: .5, fy: .5, zoom: 1 };
    m.textContent = neu.fluechtig ? 'Fertig, schwarzweiss. Dieser Browser behält es nur bis zum Schliessen.' : 'Fertig, schwarzweiss. Das Foto bleibt in diesem Browser.';
    return neu[0];
  }
  async function hochladen(ev) {
    const d = ev.target.files && ev.target.files[0]; ev.target.value = ''; if (!d) return;
    const m = $('#bkMeldung');
    try { await alsEigenes(d, m); quelle = 'grund'; zeichneFotos(); regler(); vorschau(); }
    catch (e) { m.textContent = e.message || 'Das Foto liess sich nicht lesen.'; }
  }
  /* Fotos des Hauses sind farbig: beim Wählen wird eine schwarzweisse Fassung angelegt (einmal je Foto, danach wiederverwendet) */
  const NICHT = ['Schwarzweiss', 'Plakate', 'Plakat-Grund', 'Plakat-Motive', DS.eigene ? DS.eigene.GRUPPE : 'Eigene Fotos'], VORN = ['Die Leute', 'Musik & Feste'];   // erst Menschen und Musik, Plakate sind keine Fotos
  const hausFotos = () => { const W = new Set(wellen()), rang = b => { const i = VORN.indexOf(b.gruppe); return i < 0 ? 9 : i; };
    return (DS.M.bilder || []).filter(b => !b.eigen && !b.ki && !NICHT.includes(b.gruppe) && !W.has(b.key)).map((b, i) => [b, i]).sort((x, y) => rang(x[0]) - rang(y[0]) || x[1] - y[1]).map(x => x[0].key); };
  let quelle = 'grund', hausAlle = false;
  async function hausFoto(k) {
    const s = zustand(), m = $('#bkMeldung'), b = DS.M.bildIndex[k] || {};
    s.swVon = s.swVon || {};
    if (s.swVon[k] && DS.M.bildIndex[s.swVon[k]]) { s.bild = s.swVon[k]; s.bildlage = { fx: .5, fy: .5, zoom: 1 }; m.textContent = 'Schwarzweiss gewählt.'; zeichneFotos(); regler(); vorschau(); return; }
    try {
      const blob = await (await fetch(DS.bildUrl(DS.M, k, false))).blob();
      const name = String(b.alt || k).replace(/[\\/:*?"<>|.]+/g, ' ').slice(0, 60) + '.jpg';
      s.swVon[k] = await alsEigenes(new File([blob], name, { type: blob.type || 'image/jpeg' }), m);
      zeichneFotos(); regler(); vorschau();
    } catch (e) { m.textContent = e.message || 'Das Foto liess sich nicht lesen.'; }
  }
  function zeichneFotos() {
    const box = $('#bkFotos'); if (!box) return;
    document.querySelectorAll('[data-bkquelle]').forEach(x => { const an = x.dataset.bkquelle === quelle; x.classList.toggle('an', an); x.setAttribute('aria-pressed', an); });
    const s = zustand(), G = gesichter(), akt = s.bild && DS.M.bildIndex[s.bild] ? s.bild : G[0];
    const knopf = (k, art) => { const b = DS.M.bildIndex[k] || {}, an = art === 'haus' ? (s.swVon || {})[k] === akt : k === akt;
      return `<button type="button" class="bk-foto${an ? ' an' : ''}" data-${art === 'haus' ? 'bkhaus' : 'bkbild'}="${esc(k)}" aria-pressed="${an}" aria-label="${esc(b.alt || k)}" title="${esc(b.alt || k)}"><img src="${esc(DS.bildUrl(DS.M, k, true))}" alt="" loading="lazy"></button>`; };
    if (quelle === 'haus') {
      const H = hausFotos(), zeig = hausAlle ? H : H.slice(0, 24);
      box.innerHTML = zeig.map(k => knopf(k, 'haus')).join('') + (H.length > zeig.length ? `<button type="button" class="ms-lnk bk-mehrfotos" id="bkMehrFotos"><span>Alle ${H.length} Fotos zeigen</span>${PFEIL}</button>` : '');
      box.querySelectorAll('[data-bkhaus]').forEach(b => b.addEventListener('click', () => hausFoto(b.dataset.bkhaus)));
      const mehr = $('#bkMehrFotos'); if (mehr) mehr.addEventListener('click', () => { hausAlle = true; zeichneFotos(); });
      return;
    }
    const eig = (DS.M.bilder || []).filter(b => b.eigen && / schwarzweiss$/.test(b.alt || '')).map(b => b.key);
    box.innerHTML = eig.concat(G).map(k => knopf(k, 'grund')).join('');
    box.querySelectorAll('[data-bkbild]').forEach(b => b.addEventListener('click', () => { s.bild = b.dataset.bkbild; s.bildlage = { fx: .5, fy: .5, zoom: 1 }; zeichneFotos(); regler(); vorschau(); }));
  }
  function regler() {
    const s = zustand(); [['bkZoom', 'zoom'], ['bkFx', 'fx'], ['bkFy', 'fy']].forEach(([id, k]) => { const r = $('#' + id); if (r) r.value = s.bildlage[k]; });
  }
  function zeichneGruende() {
    const box = $('#bkGruende'); if (!box) return;
    const s = zustand(), W = wellen(), akt = s.welle || W[0];
    box.innerHTML = W.map((w, i) => `<button type="button" class="bk-grund${w === akt ? ' an' : ''}" data-bkgrund="${esc(w)}" aria-pressed="${w === akt}" aria-label="${esc((MOTIVE[i] || {}).titel || 'Wellen ' + (i + 1))}"><img src="${esc(DS.bildUrl(DS.M, w, true))}" alt="" loading="lazy"></button>`).join('');
    box.querySelectorAll('[data-bkgrund]').forEach(b => b.addEventListener('click', () => { s.welle = b.dataset.bkgrund; zeichneGruende(); vorschau(); }));
  }
  function zeichneSchrift() {
    const box = $('#bkSchrift'); if (!box) return;
    const s = zustand();
    box.innerHTML = TEILE.map(([k, n]) => { const g = s.gestalt[k];
      return `<div class="bk-zeile" role="group" aria-label="${esc(n)}" data-bkteil="${k}"><p class="bk-zname">${esc(n)}</p>
        <span class="bk-farben" role="group" aria-label="Farbe">${FARBEN.map(([f, fn]) => `<button type="button" class="bk-farbe${g.farbe === f ? ' an' : ''}" data-f="${f}" style="--f:${esc(hex(f))}" aria-pressed="${g.farbe === f}"><i></i>${esc(fn)}</button>`).join('')}</span>
        <label><span>Hinterlegung</span><select data-k="feld"><option value=""${!g.feld ? ' selected' : ''}>Keine</option><option value="creme"${g.feld === 'creme' ? ' selected' : ''}>Creme-Feld</option><option value="nacht"${g.feld === 'nacht' ? ' selected' : ''}>Nacht-Feld</option></select></label>
        <label class="bk-gr"><span>Grösse</span><select data-k="groesse">${['S', 'M', 'L'].map(x => `<option${g.groesse === x ? ' selected' : ''}>${x}</option>`).join('')}</select></label>
        ${LAGEN[k].length > 1 ? `<label><span>Lage</span><select data-k="lage">${LAGEN[k].map(([v, t]) => `<option value="${v}"${g.lage === v ? ' selected' : ''}>${esc(t)}</option>`).join('')}</select></label>` : ''}
      </div>`; }).join('');
    box.querySelectorAll('[data-bkteil]').forEach(fs => {
      const k = fs.dataset.bkteil;
      fs.querySelectorAll('.bk-farbe').forEach(b => b.addEventListener('click', () => { s.gestalt[k].farbe = b.dataset.f; fs.querySelectorAll('.bk-farbe').forEach(x => { x.classList.toggle('an', x === b); x.setAttribute('aria-pressed', x === b); }); vorschau(); }));
      fs.querySelectorAll('select').forEach(sel => sel.addEventListener('change', () => { s.gestalt[k][sel.dataset.k] = sel.value; vorschau(); }));
    });
  }
  function formular() {
    const f = $('#pkFreitag'); if (!f) return;
    if (!f.options.length) samstage(16).forEach((d, i) => { const o = document.createElement('option'); o.value = d.toISOString().slice(0, 10); o.textContent = tag(d); if (!i) o.selected = true; f.appendChild(o); });
    zustand(); zeichneFotos(); zeichneGruende(); zeichneSchrift(); regler();
    document.querySelectorAll('[data-bkformat]').forEach(b => { const an = b.dataset.bkformat === zustand().format; b.classList.toggle('an', an); b.setAttribute('aria-pressed', an); });
    vorschau();
  }
  /* «Plakate anlegen»: das gebaute Plakat in den drei Formaten, dazu dasselbe in den anderen Wellen; «Diesen bearbeiten» öffnet den Editor */
  function vorschlagen(ev) {
    if (ev) ev.preventDefault();
    const box = $('#pkVorschlaege');
    if ($('#pkThema').value.trim().length < 2) {
      $('#pkThema').setAttribute('aria-invalid', 'true'); $('#pkThema').focus();
      box.innerHTML = '<p class="pk-leer">Wer legt auf? Den Namen eintragen, zum Beispiel «Moury».</p>'; return;
    }
    $('#pkThema').removeAttribute('aria-invalid');
    const s = zustand(), w = werte(), W = wellen(), akt = s.welle || W[0], FN = { insta: 'Instagram 4:5', story: 'Story 9:16', a3h: 'A3 zum Aushang' };
    const welleName = we => { const i = W.indexOf(we); return (MOTIVE[i] || {}).titel || 'Wellen ' + (i + 1); };
    const liste = ['insta', 'story', 'a3h'].map(f => ({ doc: bauDoc(f), t: FN[f], u: `${welleName(akt)} · dein Plakat` }))
      .concat(W.filter(we => we !== akt).map(we => ({ doc: bauDoc(null, we), t: welleName(we), u: `${FN[s.format] || ''} · gleiche Schrift und Foto` })));
    box.innerHTML = `<p class="pk-hinweis">${liste.length} Plakate für ${esc(w.name)} am ${esc(tag(w.samstag))}: dein Plakat in drei Formaten und in den anderen Wellen. «Diesen bearbeiten» öffnet es im Editor.</p>`;
    box.dataset.n = liste.length; const gr = fach(box, liste.length);
    liste.forEach(x => box.appendChild(karte(x.doc, x.t, x.u, 'Diesen bearbeiten', gr)));
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function verdrahten() {
    $('#pkForm') && $('#pkForm').addEventListener('submit', vorschlagen);
    ['pkThema', 'pkGast', 'pkZusatz', 'pkFreitag'].forEach(id => { const e = $('#' + id); if (e) e.addEventListener(e.tagName === 'SELECT' ? 'change' : 'input', () => { e.removeAttribute('aria-invalid'); vorschau(); }); });
    const d = $('#bkDatei'); if (d) d.addEventListener('change', hochladen);
    [['bkZoom', 'zoom'], ['bkFx', 'fx'], ['bkFy', 'fy']].forEach(([id, k]) => { const r = $('#' + id); if (r) r.addEventListener('input', () => { zustand().bildlage[k] = +r.value; vorschau(); }); });
    document.querySelectorAll('[data-bkformat]').forEach(b => b.addEventListener('click', () => { zustand().format = b.dataset.bkformat; document.querySelectorAll('[data-bkformat]').forEach(x => { x.classList.toggle('an', x === b); x.setAttribute('aria-pressed', x === b); }); vorschau(); }));
    document.querySelectorAll('[data-bkquelle]').forEach(b => b.addEventListener('click', () => { quelle = b.dataset.bkquelle; zeichneFotos(); }));
    addEventListener('resize', () => { if ($('#msAbend') && !$('#msAbend').hidden) vorschau(); });
  }

  function zeige(a) { if (a === 'motive') zeichneMotive(); if (a === 'abend') formular(); }
  async function los() {
    try { MOTIVE = await (await fetch(DS.M.basis + 'motive.json', { cache: 'no-cache' })).json(); } catch (e) { MOTIVE = []; }
    const z = $('#pkZahl'); if (z) z.textContent = MOTIVE.length + gesichter().length;
    verdrahten();
    if ($('#msAbend') && !$('#msAbend').hidden) formular();
  }
  window.DSPlakat = { zeige, plakatDoc, samstage, freitage: samstage, motive: () => MOTIVE };
  if (window.DS && DS.M && window.DSStudio) los(); else document.addEventListener('ds:bereit', los, { once: true });
})();
