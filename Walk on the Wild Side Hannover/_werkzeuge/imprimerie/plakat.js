/* Plakatwerkstatt · Walk on the Wild Side Hannover (31.10.2026, Form der Plakatwerkstatt des Culinarium übernommen): zwei Ansichten.
   1. «Plakat-Grund» (#msMotive): die rot-cremefarbenen Wellen der SESSION-Plakate und die Gesichter in Schwarzweiss, jedes gleich als SESSION-Plakat;
      «Als Plakat öffnen» öffnet es im Editor.
   2. «DJ-Abend anlegen» (#msAbend): Name, Stil, Samstag und Uhrzeit → drei bis fünf SESSION-Plakate in verschiedenen Wellen und Gesichtern, sofort und ohne KI;
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

  /* ---------- 2 DJ-Abend anlegen ---------- */
  function formular() {
    const f = $('#pkFreitag'); if (!f || f.options.length) return;
    samstage(16).forEach((d, i) => { const o = document.createElement('option'); o.value = d.toISOString().slice(0, 10); o.textContent = tag(d); if (!i) o.selected = true; f.appendChild(o); });
  }
  function vorschlagen(ev) {
    if (ev) ev.preventDefault();
    const name = $('#pkThema').value.trim(), zeit = $('#pkGast').value.trim() || '9 PM TO 1 AM', stil = $('#pkKonzept').value.trim();
    const zahl = +(document.querySelector('[data-pkzahl].an') || { dataset: { pkzahl: 4 } }).dataset.pkzahl;
    const sa = new Date($('#pkFreitag').value + 'T12:00:00');
    const box = $('#pkVorschlaege');
    if (name.length < 2) { $('#pkThema').focus(); box.innerHTML = '<p class="pk-leer">Wer legt auf? Den Namen eintragen, zum Beispiel «Moury».</p>'; return; }
    box.innerHTML = `<p class="pk-hinweis">${zahl} Plakate für ${esc(name)} am ${esc(tag(sa))}${stil ? ' · ' + esc(stil) : ''}. Im Editor das Foto tauschen: das Gesicht des Abends in Schwarzweiss.</p>`;
    box.dataset.n = zahl;
    const G = gesichter(), W = wellen(), gr = fach(box, zahl);
    for (let i = 0; i < zahl; i++) {
      const doc = plakatDoc({ name, zeit, samstag: sa, welle: W[i % W.length], gesicht: G[(i * 4) % G.length] });
      box.appendChild(karte(doc, `Vorschlag ${i + 1}`, `Wellen ${(i % W.length) + 1} · ${tag(sa)}`, 'Diesen bearbeiten', gr));
    }
  }

  function zeige(a) { if (a === 'motive') zeichneMotive(); if (a === 'abend') formular(); }
  async function los() {
    try { MOTIVE = await (await fetch(DS.M.basis + 'motive.json', { cache: 'no-cache' })).json(); } catch (e) { MOTIVE = []; }
    const z = $('#pkZahl'); if (z) z.textContent = MOTIVE.length + gesichter().length;
    $('#pkForm') && $('#pkForm').addEventListener('submit', vorschlagen);
    document.querySelectorAll('[data-pkzahl]').forEach(b => b.addEventListener('click', () => { document.querySelectorAll('[data-pkzahl]').forEach(x => x.classList.toggle('an', x === b)); }));
    formular();
  }
  window.DSPlakat = { zeige, plakatDoc, samstage, freitage: samstage, motive: () => MOTIVE };
  if (window.DS && DS.M && window.DSStudio) los(); else document.addEventListener('ds:bereit', los, { once: true });
})();
