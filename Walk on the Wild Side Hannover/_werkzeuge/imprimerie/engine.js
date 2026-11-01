/* Plakatwerkstatt · Ideen-Engine «Event beschreiben» (Walk on the Wild Side, 1.11.2026, Robert: «eine weitere Engine, die wie beim Culinarium durch Eingabe
   des Events und Rahmenbedingungen zusätzliche individuelle Plakat-Ideen erstellt»).
   Eingabe: Name, Art, Datum, Uhrzeit, Ort, Partner, Stichworte, Format. Ergebnis: sechs gesetzte Plakat-Ideen im Stil der echten Event-Plakate der Bar,
     Schallplatte  (Christi Limmerfahrt: verlaufende tanzende Figuren im Plattenbogen, fette Grotesk, Partnerleiste)
     Linien        (Oktoberfest des Event Klub: Linien-Figuren in einer Farbe, rote Typo, Info-Tabelle Wann/Wo/Drinks)
     Leuchtschrift («Two Years»: Neon auf Schwarz, Creme-Papier, roter Datums-Stempel)
     Rosa          (Valentin: Display-Schrift, Handschrift darüber, Herzen)
     Siebdruck     (zwei Farben, Rasterpunkte, schmale Versalien)
   Ohne KI und ohne Server: die Illustration rechnet sich als SVG aus einem Seed (Eingabe + Wurf), Texte, Linien und Rahmen sind Ebenen der Drucksache.
   «Diese bearbeiten» rastert die Illustration als Foto in «Eigene Fotos» (bleibt im Browser) und öffnet die Drucksache im Editor (Texte, PDF, PNG).
   Eigene Dateien: engine.js, engine.css. Navigation: index.html (Knopf, #msEngine), start.js (Ansicht «engine»). */
(function () {
  const $ = s => document.querySelector(s);
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const PFEIL = '<svg viewBox="0 0 24 24"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>';
  const WUERFEL = '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="3.5"/><path d="M9 9h.01M15 15h.01M15 9h.01M9 15h.01M12 12h.01"/></svg>';
  const SPEICHER = 'ws-engine-event';
  const STANDORT = 'Haasemannstraße 13';
  /* Schriften der Event-Plakate (_bau/engine_schriften.py), als eigene Rollen neben denen der Marke: Bildschirm woff2, PDF die TTF */
  const SCHRIFTEN = {
    egrotesk: ['Archivo Black', 'ArchivoBlack-400', 'Event-Plakate: fette Grotesk wie «Christi Limmerfahrt» und «oktoberfest.» (OFL)'],
    eschmal: ['Anton', 'Anton-400', 'Event-Plakate: schmale fette Versalien für Stempel und Zeilen (OFL)'],
    eneon: ['Yellowtail', 'Yellowtail-400', 'Event-Plakate: Leuchtschrift wie «Two Years» (Apache 2.0)'],
    ehand: ['Permanent Marker', 'PermanentMarker-400', 'Event-Plakate: Handschrift der Info-Tabelle und «LOVE» (Apache 2.0)'],
  };
  const ARTEN = [['fest', 'Fest unter freiem Himmel'], ['party', 'Party und DJ'], ['jubilaeum', 'Jubiläum und Geburtstag'], ['konzert', 'Konzert und Live-Musik'],
    ['saison', 'Feiertag und Saison'], ['liebe', 'Valentin und Liebe'], ['tasting', 'Tasting und Kooperation']];
  const FORMATE = [['insta', 'Instagram 4:5'], ['story', 'Story'], ['a3h', 'A3']];
  const BEISPIEL = { name: 'Christi Limmerfahrt 2026', art: 'fest', datum: '14./15. Mai', zeit: '12–21 Uhr', ort: 'Am Küchengarten', partner: 'Tru Story, Rebe, Food Truck Klub, Probierbude', stimmung: 'Sonne, tanzen, Streetfood, Musik' };
  const STIL_NAMEN = { platte: 'Schallplatte', linien: 'Linien-Figuren', neon: 'Leuchtschrift', rosa: 'Rosa mit Handschrift', sieb: 'Siebdruck' };
  const STIL_IDEE = {
    platte: 'Verlaufende Figuren tanzen im Schallplatten-Bogen, fette Grotesk, Partnerleiste wie bei der Limmerfahrt.',
    linien: 'Linien-Figuren in einer Farbe, grosse rote Typo und die Info-Tabelle Wann, Wo, Drinks wie beim Oktoberfest.',
    neon: 'Leuchtschrift auf Schwarz im Rahmen aus Creme-Papier, dazu der rote Datums-Stempel wie zu «Two Years».',
    rosa: 'Rosa Grund, Display-Schrift mit Handschrift darüber, Herzen und Funken wie zum Valentinstag.',
    sieb: 'Siebdruck in zwei Farben: Rasterpunkte, schmale Versalien, leicht versetzt gedruckt.',
  };
  const REIHE = { fest: ['platte', 'linien', 'sieb', 'rosa', 'neon'], party: ['neon', 'sieb', 'platte', 'rosa', 'linien'], jubilaeum: ['neon', 'rosa', 'sieb', 'platte', 'linien'],
    konzert: ['platte', 'neon', 'sieb', 'linien', 'rosa'], saison: ['linien', 'platte', 'sieb', 'rosa', 'neon'], liebe: ['rosa', 'neon', 'sieb', 'platte', 'linien'],
    tasting: ['linien', 'sieb', 'neon', 'rosa', 'platte'] };

  let bereit = null, wurf = 0, IDEEN = [], gezeichnet = false, offen = false;

  /* ---------- Zufall aus der Eingabe ---------- */
  function hash(s) { let h = 1779033703 ^ s.length; for (let i = 0; i < s.length; i++) { h = Math.imul(h ^ s.charCodeAt(i), 3432918353); h = h << 13 | h >>> 19; } return h >>> 0; }
  function zufall(seed) {
    let a = seed >>> 0;
    const r = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
    r.zw = (x, y) => x + (y - x) * r(); r.wahl = l => l[Math.floor(r() * l.length) % l.length]; r.ganz = (x, y) => Math.floor(r.zw(x, y + 1)); r.ja = p => r() < (p == null ? .5 : p);
    return r;
  }
  const f2 = n => +(+n).toFixed(2);

  /* ---------- Schriften ---------- */
  let fontDaten = {};
  function schriften() {
    if (bereit) return bereit;
    const M = DS.M; let css = '';
    for (const [r, [fam, dat, wofuer]] of Object.entries(SCHRIFTEN)) {
      if (!M.schriften[r]) M.schriften[r] = { familie: fam, datei: dat + '.ttf', wofuer };
      css += `@font-face{font-family:'DS-${r}';src:url('${M.basis}schriften/${dat}.woff2') format('woff2'),url('${M.basis}schriften/${dat}.ttf') format('truetype');font-display:block}\n`;
    }
    const st = document.createElement('style'); st.id = 'engineSchriften'; st.textContent = css; document.head.appendChild(st);
    bereit = Promise.all(Object.keys(SCHRIFTEN).map(r => document.fonts.load(`20px 'DS-${r}'`, 'AaÄä0123').catch(() => null)));
    return bereit;
  }
  /* für die Illustration (SVG als Bild kennt die Schriften der Seite nicht): Leuchtschrift und Stempel als data-URL eingebettet */
  function fontUrl(r) {
    if (!fontDaten[r]) fontDaten[r] = fetch(DS.M.basis + 'schriften/' + SCHRIFTEN[r][1] + '.woff2').then(x => x.blob()).then(b => new Promise(ok => { const f = new FileReader(); f.onload = () => ok(f.result); f.readAsDataURL(b); })).catch(() => '');
    return fontDaten[r];
  }

  /* ---------- Ebenen der Drucksache ---------- */
  let nid = 0;
  const neueId = () => 'en' + Date.now().toString(36) + (nid++).toString(36);
  function txt(rolle, text, x, y, w, gr, farbe, o) {
    const el = Object.assign({ id: neueId(), typ: 'text', rolle, text: String(text), x: f2(x), y: f2(y), w: f2(w), gr: f2(gr), farbe, ausr: 'c', zeile: 1.08, sperr: 0, deck: 1 }, o || {});
    el.h = DS.mess(el).h; return el;
  }
  const breite = el => DS.mess(Object.assign({}, el, { w: 100000, ausr: 'l' })).bw || 0;
  function passe(el, maxW, maxH) {   // so klein, bis die breiteste Zeile in maxW passt (und der Block in maxH)
    const bw = breite(el); if (bw > maxW * .97) el.gr = f2(el.gr * maxW * .97 / bw);
    el.h = DS.mess(el).h;
    if (maxH && el.h > maxH) { el.gr = f2(el.gr * maxH / el.h); el.h = DS.mess(el).h; }
    return el;
  }
  const linie = (x, y, w, staerke, farbe) => ({ id: neueId(), typ: 'linie', x: f2(x), y: f2(y), w: f2(w), h: 0, staerke: f2(staerke), farbe, deck: 1 });
  const senkrecht = (x, y, h, staerke, farbe) => ({ id: neueId(), typ: 'linie', x: f2(x), y: f2(y), w: 0, h: f2(h), staerke: f2(staerke), farbe, deck: 1 });
  const rahmen = (x, y, w, h, staerke, farbe) => ({ id: neueId(), typ: 'rahmen', x: f2(x), y: f2(y), w: f2(w), h: f2(h), staerke: f2(staerke), r: 0, farbe, deck: 1 });
  /* Text in n ausgewogene Zeilen */
  function teile(text, n) {
    const w = String(text).split(/\s+/).filter(Boolean); if (n <= 1 || w.length <= 1) return w.join(' ');
    let best = null;
    const probe = (cuts) => { const z = []; let a = 0; for (const c of cuts.concat(w.length)) { z.push(w.slice(a, c).join(' ')); a = c; } const m = Math.max(...z.map(x => x.length)); if (!best || m < best.m) best = { m, z }; };
    if (n === 2 || w.length === 2) for (let i = 1; i < w.length; i++) probe([i]);
    else for (let i = 1; i < w.length - 1; i++) for (let j = i + 1; j < w.length; j++) probe([i, j]);
    return best.z.join('\n');
  }
  /* Partnerleiste wie die Logoreihe der Fest-Plakate: jeder Name ein eigenes Zeichen in einer anderen Schrift */
  function leiste(E, x, unten, w, gr, farbe) {
    const namen = ['walk on the wild side'].concat(E.partner).slice(0, 7);
    if (namen.length === 1) namen.push('@walkonthewildside_hannover');
    const rollen = ['egrotesk', 'ehand', 'eschmal', 'pinsel', 'titel', 'liebe', 'kapitale'];
    const sw = w / namen.length, els = namen.map((t, i) => passe(txt(rollen[i % rollen.length], t, x + i * sw + sw * .05, 0, sw * .9, gr * (i ? 1.15 : 1), farbe, { zeile: 1 }), sw * .86, gr * 2.4));
    const hoch = Math.max(...els.map(e => e.h));
    els.forEach(e => { e.y = f2(unten - hoch + (hoch - e.h) / 2); });
    return { els, oben: unten - hoch };
  }

  /* ---------- SVG-Bausteine ---------- */
  const SYM = {
    glas: 'M-.42 -.42 L.42 -.42 L0 .08 Z M-.03 .08 H.03 V.4 H-.03Z M-.24 .4 H.24 V.47 H-.24Z',
    burger: 'M-.5 -.06 Q-.5 -.44 0 -.44 Q.5 -.44 .5 -.06 Z M-.54 0 H.54 V.09 H-.54Z M-.5 .15 H.5 V.25 Q.5 .34 .41 .34 H-.41 Q-.5 .34 -.5 .25Z',
    flasche: 'M-.09 -.5 H.09 V-.24 Q.21 -.14 .21 .02 V.5 H-.21 V.02 Q-.21 -.14 -.09 -.24Z',
    note: 'M-.08 .32 m-.18 0 a.18 .13 -20 1 0 .36 0 a.18 .13 -20 1 0 -.36 0 M.07 .3 V-.46 H.14 Q.18 -.22 .4 -.12 Q.2 -.16 .14 -.26 V.3Z',
    herz: 'M0 .42 C-.62 .02 -.52 -.46 -.2 -.46 C-.06 -.46 0 -.34 0 -.26 C0 -.34 .06 -.46 .2 -.46 C.52 -.46 .62 .02 0 .42Z',
    stern: 'M0 -.5 Q.07 -.07 .5 0 Q.07 .07 0 .5 Q-.07 .07 -.5 0 Q-.07 -.07 0 -.5Z',
    torte: 'M-.42 -.02 H.42 V.42 H-.42Z M-.42 .14 Q-.28 .24 -.14 .14 Q0 .24 .14 .14 Q.28 .24 .42 .14 M-.03 -.02 V-.3 H.03 V-.02Z M0 -.34 Q-.08 -.42 0 -.52 Q.08 -.42 0 -.34Z',
    sonne: 'M0 -.22 a.22 .22 0 1 0 .001 0Z M0 -.5 V-.32 M0 .32 V.5 M-.5 0 H-.32 M.32 0 H.5 M-.35 -.35 L-.23 -.23 M.23 .23 L.35 .35 M-.35 .35 L-.23 .23 M.23 -.23 L.35 -.35',
  };
  const SYMBOLE = { fest: ['glas', 'burger', 'flasche', 'sonne'], party: ['glas', 'note', 'stern', 'flasche'], jubilaeum: ['torte', 'glas', 'stern', 'flasche'],
    konzert: ['note', 'glas', 'stern', 'note'], saison: ['glas', 'flasche', 'stern', 'burger'], liebe: ['herz', 'glas', 'herz', 'stern'], tasting: ['glas', 'flasche', 'glas', 'stern'] };
  function svgDoc(W, H, defs, inhalt, schriftCss) {
    const B = DS.B;
    return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${f2((W + 2 * B) * 10)}" height="${f2((H + 2 * B) * 10)}" viewBox="${-B} ${-B} ${W + 2 * B} ${H + 2 * B}">`
      + (schriftCss ? `<style>${schriftCss}</style>` : '') + `<defs>${defs}</defs>${inhalt}</svg>`;
  }
  const korn = (W, H, k, o) => `<filter id="korn" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="${f2(1.6 / k)}" numOctaves="2" seed="3" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 .1  0 0 0 0 .07  0 0 0 0 .05  -.9 0 0 0 ${o || .5}"/></filter>`;
  const kornFlaeche = (W, H) => `<rect x="-3" y="-3" width="${W + 6}" height="${H + 6}" filter="url(#korn)" opacity=".55"/>`;

  /* Tanzende Figur (Schallplatte): Strichmännchen mit runden Enden, Höhe ~1, Ursprung an der Hüfte */
  function taenzer(r) {
    const lean = r.zw(-.22, .22), dir = (t, s) => [s * Math.sin(t), Math.cos(t)];
    const hals = [lean * .3, -.42], kopf = [lean * .42, -.58], sch = [lean * .26, -.36];
    const P = (p, d, l) => [p[0] + d[0] * l, p[1] + d[1] * l];
    const glied = (a, t1, t2, s, l1, l2) => { const b = P(a, dir(t1, s), l1), c = P(b, dir(t2, s), l2); return `M${f2(a[0])} ${f2(a[1])} L${f2(b[0])} ${f2(b[1])} L${f2(c[0])} ${f2(c[1])}`; };
    const arme = [-1, 1].map(s => { const t1 = r.zw(1.1, 2.9); return glied(sch, t1, t1 + r.zw(-1, .9), s, .2, .19); }).join(' ');
    const beine = [-1, 1].map(s => { const t1 = r.zw(.08, .75); return glied([0, 0], t1, t1 + r.zw(-.8, .25), s, .25, .25); }).join(' ');
    return { d: `M${f2(hals[0])} ${f2(hals[1])} Q${f2(lean * .2)} -.2 0 0 ${arme} ${beine}`, kopf };
  }
  /* Linien-Figur (Oktoberfest): stehende Person, Füsse bei y=0, Kopf oben bei -1; Strichfarbe currentColor, Fläche Papier */
  function person(r, art, papier) {
    const rock = r.ja(.45), kind = false, hebt = r.wahl(['rechts', 'links', 'beide', 'rechts']);
    const hx = r.zw(-.02, .02), kopfR = .085, kopfY = -.86;
    const fuss = [-1, 1].map(s => `M${f2(s * .05)} -.44 L${f2(s * r.zw(.06, .12))} -.04 M${f2(s * r.zw(.06, .12) - .05)} -.02 h.1`).join(' ');
    let koerper, extra = '';
    if (rock) {
      koerper = `M-.1 -.74 L.1 -.74 L.11 -.6 L.21 -.36 Q0 -.31 -.21 -.36 L-.11 -.6Z`;
      extra = `<path d="M-.07 -.58 L.07 -.58 L.1 -.39 Q0 -.36 -.1 -.39Z" fill="${papier}"/><path d="M-.1 -.6 H.1" fill="none"/>`;
    } else {
      koerper = `M-.12 -.74 L.12 -.74 L.12 -.5 L-.12 -.5Z`;
      extra = `<path d="M-.11 -.5 L-.12 -.3 L-.02 -.3 L0 -.42 L.02 -.3 L.12 -.3 L.11 -.5Z" fill="currentColor"/><path d="M-.07 -.74 L-.07 -.5 M.07 -.74 L.07 -.5 M-.07 -.62 H.07" fill="none"/>`;
    }
    const muster = r.ja(.4) && !rock ? 'url(#karo)' : papier;
    const arm = (s, hoch) => hoch ? `M${f2(s * .11)} -.72 L${f2(s * .22)} -.6 L${f2(s * .2)} -.84` : `M${f2(s * .11)} -.72 L${f2(s * .17)} -.56 L${f2(s * .15)} -.42`;
    const hochR = hebt !== 'links', hochL = hebt !== 'rechts';
    const glas = (s) => art === 'saison' || art === 'fest' && r.ja(.5)
      ? `<path d="M${f2(s * .2 - .045)} -.95 h.09 v.11 h-.09Z M${f2(s * .2 + .045)} -.93 q.04 0 .04 .035 q0 .035 -.04 .035" fill="${papier}"/><path d="M${f2(s * .2 - .045)} -.93 h.09" fill="none"/>`
      : `<path d="M${f2(s * .2 - .05)} -.97 h.1 l-.05 .07Z M${f2(s * .2)} -.9 v.06 M${f2(s * .2 - .025)} -.84 h.05" fill="${papier}"/>`;
    const haar = r.wahl(['kurz', 'zopf', 'locken', 'hut', 'kurz']);
    let kopfTeil = `<circle cx="${hx}" cy="${kopfY}" r="${kopfR}" fill="${papier}"/><path d="M${f2(hx - .03)} -.86 h.001 M${f2(hx + .03)} -.86 h.001" stroke-width=".022" stroke-linecap="round"/><path d="M${f2(hx - .03)} -.83 q.03 .025 .06 0" fill="none"/>`;
    if (haar === 'kurz') kopfTeil += `<path d="M${f2(hx - kopfR)} ${kopfY} Q${f2(hx - kopfR)} ${f2(kopfY - kopfR * 1.25)} ${hx} ${f2(kopfY - kopfR)} Q${f2(hx + kopfR)} ${f2(kopfY - kopfR * 1.25)} ${f2(hx + kopfR)} ${kopfY} Q${hx} ${f2(kopfY - kopfR * .5)} ${f2(hx - kopfR)} ${kopfY}Z" fill="currentColor"/>`;
    if (haar === 'zopf') kopfTeil += `<circle cx="${hx}" cy="${f2(kopfY - kopfR * 1.25)}" r=".04" fill="currentColor"/><path d="M${f2(hx - kopfR)} ${kopfY} Q${hx} ${f2(kopfY - kopfR * 1.6)} ${f2(hx + kopfR)} ${kopfY} Q${hx} ${f2(kopfY - kopfR * .6)} ${f2(hx - kopfR)} ${kopfY}Z" fill="currentColor"/>`;
    if (haar === 'locken') kopfTeil = Array.from({ length: 9 }, (_, i) => { const a = Math.PI * (1.05 + i * .11); return `<circle cx="${f2(hx + Math.cos(a) * kopfR * 1.15)}" cy="${f2(kopfY + Math.sin(a) * kopfR * 1.15)}" r=".04" fill="currentColor"/>`; }).join('') + kopfTeil;
    if (haar === 'hut') kopfTeil += `<path d="M${f2(hx - .13)} ${f2(kopfY - .06)} H${f2(hx + .13)} M${f2(hx - .07)} ${f2(kopfY - .06)} L${f2(hx - .055)} ${f2(kopfY - .15)} H${f2(hx + .055)} L${f2(hx + .07)} ${f2(kopfY - .06)}Z" fill="currentColor"/>`;
    return `<path d="${fuss}" fill="none"/><path d="${arm(-1, hochL)} ${arm(1, hochR)}" fill="none"/>${hochR ? glas(1) : ''}${hochL && hebt === 'beide' ? glas(-1) : ''}`
      + `<path d="${koerper}" fill="${rock ? papier : muster}"/>${extra}<path d="M-.03 -.74 L0 -.77 L.03 -.74" fill="none"/>${kopfTeil}`;
  }

  /* ---------- Die fünf Stile ---------- */
  const STILE = {};

  /* 1 Schallplatte (Christi Limmerfahrt) */
  STILE.platte = function (E, r, F) {
    const W = F.b, H = F.h, k = W / 108, m = 7 * k, tinte = '#141010', papier = r.wahl(['#efe8dc', '#f1ebe1', '#ece4d6']);
    const pal = r.wahl([['#ff7ab6', '#ffb36b', '#5b6cff', 'Pink, Orange, Blau'], ['#ff6f61', '#ffd36b', '#7a5cff', 'Koralle, Gelb, Violett'], ['#3fd6a6', '#f6e35a', '#7b61ff', 'Mint, Gelb, Violett'], ['#ff8fd1', '#ff5a3c', '#4fb3ff', 'Rosa, Rot, Himmelblau']]);
    const el = [];
    const titel = passe(txt('egrotesk', teile(E.titel.toUpperCase(), E.titel.length > 11 ? 2 : 1), m + 10 * k, m, W - 2 * m - 20 * k, 11 * k, tinte, { zeile: .92 }), W - 2 * m - 20 * k, H * .2);
    const L = leiste(E, m, H - m * .8, W - 2 * m, 2.5 * k, tinte);
    const ort = passe(txt('egrotesk', E.ort.toUpperCase(), m, 0, W - 2 * m, 5.6 * k, tinte, { ausr: 'l', zeile: 1 }), W - 2 * m);
    ort.y = f2(L.oben - 5 * k - ort.h);
    const hb = (W - 2 * m) / 2 - 6 * k;
    const dat = passe(txt('egrotesk', (E.datum + (E.jahr && !/\d{4}/.test(E.datum) ? ' ' + E.jahr : '')).toUpperCase(), m, 0, hb, 5.6 * k, tinte, { ausr: 'l', zeile: 1 }), hb);
    const zeit = passe(txt('egrotesk', E.zeit.toUpperCase(), W - m - hb, 0, hb, 5.6 * k, tinte, { ausr: 'r', zeile: 1 }), hb);
    const g = Math.min(dat.gr, zeit.gr, ort.gr); [dat, zeit, ort].forEach(e => { e.gr = g; e.h = DS.mess(e).h; }); ort.y = f2(L.oben - 5 * k - ort.h);
    const zeileY = ort.y - 3.6 * k - dat.h; dat.y = zeit.y = f2(zeileY);
    const l1 = zeileY - 2 * k, l2 = zeileY + dat.h + 1.4 * k;
    el.push(linie(m, l1, W - 2 * m, .5 * k, tinte), linie(m, l2, W - 2 * m, .5 * k, tinte), dat, zeit, ort, titel, ...L.els);
    /* Bogen */
    const yA = titel.y + titel.h + 5 * k, yB = l1 - 3 * k, R = Math.min((W - 2 * m) * .34, (yB - yA) * .44), cx = W / 2, cy = yA + R, ri = R * .6;
    const bogen = (rr) => `M${f2(cx - rr)} ${f2(yB)} L${f2(cx - rr)} ${f2(cy)} A${f2(rr)} ${f2(rr)} 0 0 1 ${f2(cx + rr)} ${f2(cy)} L${f2(cx + rr)} ${f2(yB)}`;
    let rillen = ''; for (let rr = ri + .9 * k; rr < R - .5 * k; rr += r.zw(.6, 1.1) * k) rillen += `<path d="${bogen(rr)}" fill="none" stroke="#3b3535" stroke-width="${f2(.18 * k)}" opacity="${f2(r.zw(.4, .8))}"/>`;
    const defs = korn(W, H, k) + `<linearGradient id="g1" gradientUnits="userSpaceOnUse" x1="-.5" y1="-.7" x2=".5" y2=".6"><stop offset="0" stop-color="${pal[0]}"/><stop offset=".55" stop-color="${pal[1]}"/><stop offset="1" stop-color="${pal[0]}"/></linearGradient>`
      + `<linearGradient id="g2" gradientUnits="userSpaceOnUse" x1=".5" y1="-.7" x2="-.5" y2=".6"><stop offset="0" stop-color="${pal[1]}"/><stop offset="1" stop-color="${pal[0]}"/></linearGradient>`
      + `<filter id="hof" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation=".06"/></filter><filter id="kern" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation=".045"/></filter>`
      + `<filter id="weich" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation=".03"/></filter>`;
    let fig = '';
    const n = Math.max(4, Math.min(7, Math.round((yB - cy) / R * 2.6 + 2))), s = R * r.zw(.95, 1.12);
    for (let i = 0; i < n; i++) {
      const t = n === 1 ? .5 : i / (n - 1), seite = i % 2 ? 1 : -1;
      let x = cx + seite * R * r.zw(.12, .72) * (n % 2 && i === n - 1 ? 0 : 1), y = cy - R * .15 + (yB - cy) * t * .78 + r.zw(-.06, .06) * R;
      x = Math.max(m + s * .32, Math.min(W - m - s * .32, x));
      const f = taenzer(r), gr = r.ja() ? 'g1' : 'g2';
      fig += `<g transform="translate(${f2(x)} ${f2(y)}) scale(${f2(s)})" stroke-linecap="round" stroke-linejoin="round" fill="none">`
        + `<g filter="url(#hof)" stroke="url(#${gr})" fill="url(#${gr})"><path d="${f.d}" stroke-width=".25"/><circle cx="${f2(f.kopf[0])}" cy="${f2(f.kopf[1])}" r=".14" stroke="none"/></g>`
        + `<g filter="url(#kern)" stroke="${pal[2]}" fill="${pal[2]}" opacity=".7"><path d="${f.d}" stroke-width=".1"/><circle cx="${f2(f.kopf[0])}" cy="${f2(f.kopf[1])}" r=".07" stroke="none"/></g></g>`;
    }
    const sy = SYMBOLE[E.art] || SYMBOLE.fest;
    for (let i = 0; i < 4; i++) {
      const seite = i % 2 ? 1 : -1, gr = r.zw(7, 9.5) * k;
      const x = Math.max(m + gr / 2, Math.min(W - m - gr / 2, cx + seite * r.zw(R * .8, R * 1.15))), y = r.zw(cy - R * .55, yB - gr * .4);
      fig += `<g transform="translate(${f2(x)} ${f2(y)}) scale(${f2(gr)}) rotate(${f2(r.zw(-18, 18))})" filter="url(#weich)"><path d="${SYM[sy[i]]}" fill="url(#g1)" stroke="url(#g1)" stroke-width=".05" stroke-linejoin="round"/></g>`;
    }
    const sterne = [m + 4.5 * k, W - m - 4.5 * k].map(x => `<path transform="translate(${f2(x)} ${f2(titel.y + Math.min(titel.h, titel.gr) * .5)}) scale(${f2(4.2 * k)})" d="${SYM.stern}" fill="${tinte}"/>`).join('');
    const svg = svgDoc(W, H, defs, `<rect x="-3" y="-3" width="${W + 6}" height="${H + 6}" fill="${papier}"/>${kornFlaeche(W, H)}<path d="${bogen(R)} Z M${f2(cx - ri)} ${f2(yB)} L${f2(cx - ri)} ${f2(cy)} A${f2(ri)} ${f2(ri)} 0 0 1 ${f2(cx + ri)} ${f2(cy)} L${f2(cx + ri)} ${f2(yB)}Z" fill="${tinte}" fill-rule="evenodd"/>${rillen}${fig}${sterne}`);
    return { el, svg, grund: papier, farben: pal[3] };
  };

  /* 2 Linien-Figuren (Oktoberfest des Event Klub) */
  STILE.linien = function (E, r, F) {
    const W = F.b, H = F.h, k = W / 108, m = 7 * k, papier = r.wahl(['#efe9dd', '#f2ece2']);
    const pal = r.wahl([['#d8261c', '#1f3aa6', 'Rot und Blau'], ['#d8261c', '#1f3aa6', 'Rot und Blau'], ['#1f3aa6', '#d8261c', 'Blau und Rot'], ['#c2410c', '#14532d', 'Rost und Tanne']]);
    const [rot, blau] = pal, el = [];
    const wort = E.titel.toLowerCase().replace(/\.$/, '');
    let zeilen = teile(wort, wort.length > 16 ? 3 : 2);
    if (!/\s/.test(wort)) { const m2 = /^(.{3,}?)(fest|nacht|party|abend|markt|fahrt|sommer|zauber|klub|club|bar|feier)$/.exec(wort); if (m2) zeilen = m2[1] + '\n' + m2[2]; }
    const tb = W * .66 - m;
    const titel = passe(txt('egrotesk', zeilen + '.', m - .6 * k, m - 1.5 * k, tb, 24 * k, rot, { ausr: 'l', zeile: .84, sperr: -.02 }), tb, H * .3);
    const unter = passe(txt('egrotesk', E.partner[0] ? 'MIT ' + E.partner[0].toUpperCase() : 'WALK ON THE WILD SIDE', m, titel.y + titel.h + 1.2 * k, tb, 2.2 * k, rot, { ausr: 'l', sperr: .05, zeile: 1 }), tb);
    const L = leiste(E, m, H - m * .8, W - 2 * m, 2.5 * k, blau);
    /* Tabelle */
    const rh = 7.6 * k, ty = L.oben - 4.5 * k - 3 * rh, tw = W - 2 * m, lw = 16 * k, st = .42 * k;
    el.push(rahmen(m, ty, tw, 3 * rh, st, rot), linie(m, ty + rh, tw, st, rot), linie(m, ty + 2 * rh, tw, st, rot));
    const zelle = (label, wert, x, y, w) => {
      const l = txt('egrotesk', label, x + 1.6 * k, 0, lw - 2.4 * k, 2.5 * k, rot, { ausr: 'l', zeile: 1 }); passe(l, lw - 2.4 * k); l.y = f2(y + (rh - l.h) / 2);
      const v = txt('ehand', wert, x + lw + 1.6 * k, 0, w - lw - 3 * k, 3.1 * k, blau, { ausr: 'l', zeile: 1 }); passe(v, w - lw - 3 * k); v.y = f2(y + (rh - v.h) / 2);
      el.push(l, v, senkrecht(x + lw, y, rh, st, rot));
    };
    zelle('WANN', [E.datum, E.zeit].filter(Boolean).join(' · '), m, ty, tw);
    zelle('WO', E.ort + (/hannover/i.test(E.ort) ? '' : ', Hannover'), m, ty + rh, tw);
    zelle('DRINKS', 'Cocktails von Momo', m, ty + 2 * rh, tw / 2);
    zelle(E.partner.length ? 'MIT' : 'DAZU', E.partner.length ? E.partner.slice(0, 3).join(', ') : (E.worte.slice(0, 2).join(', ') || 'Musik und gute Leute'), m + tw / 2, ty + 2 * rh, tw / 2);
    el.push(senkrecht(m + tw / 2, ty + 2 * rh, rh, st, rot));
    const slogan = passe(txt('egrotesk', (E.worte.length >= 2 ? E.worte.slice(0, 4).map(w => w.toUpperCase()) : ['GOOD DRINKS', 'GOOD FOOD', 'GOOD TUNES', 'GOOD PEOPLE']).join('  -  '), m, 0, tw, 2.6 * k, rot, { zeile: 1 }), tw);
    slogan.y = f2(ty - 3.4 * k - slogan.h);
    const dat = passe(txt('egrotesk', E.datum.toUpperCase().replace(/\.$/, ''), m, 0, tw, 18 * k, rot, { zeile: .95, sperr: -.02 }), tw, 22 * k);
    dat.y = f2(slogan.y - 2.6 * k - dat.h);
    el.push(titel, unter, slogan, dat, ...L.els);
    /* Figuren */
    const oben = unter.y + unter.h + 4 * k, basis = dat.y - 1.5 * k, fh = Math.min(basis - oben, 46 * k * (H / W > 1.5 ? 1.35 : 1));
    const n = r.ganz(5, 7), defs = korn(W, H, k, .35) + `<pattern id="karo" patternUnits="userSpaceOnUse" width=".05" height=".05"><rect width=".05" height=".05" fill="${papier}"/><path d="M0 .025 H.05 M.025 0 V.05" stroke="${blau}" stroke-width=".008"/></pattern>`;
    let fig = '';
    const plaetze = Array.from({ length: n }, (_, i) => ({ x: m + fh * .2 + (W - 2 * m - fh * .4) * (n === 1 ? .5 : i / (n - 1)) + r.zw(-2, 2) * k, s: fh * r.zw(.78, 1), y: basis - r.zw(0, fh * .08) }));
    plaetze.sort((a, b) => a.y - b.y).forEach(p => {
      fig += `<g transform="translate(${f2(p.x)} ${f2(p.y)}) scale(${f2(p.s)})" color="${blau}" stroke="${blau}" stroke-width="${f2(.42 * k / p.s)}" stroke-linecap="round" stroke-linejoin="round">${person(r, E.art, papier)}</g>`;
    });
    /* Wimpelkette rechts oben neben dem Titel */
    const wx0 = W * .66 + 2 * k, wx1 = W - m + 2 * k, wy = m + 2 * k; let wim = `<path d="M${f2(wx0)} ${f2(wy)} Q${f2((wx0 + wx1) / 2)} ${f2(wy + 9 * k)} ${f2(wx1)} ${f2(wy)}" fill="none" stroke="${blau}" stroke-width="${f2(.35 * k)}"/>`;
    for (let i = 1; i < 7; i++) {
      const t = i / 7, x = wx0 + (wx1 - wx0) * t, y = wy + 2 * t * (1 - t) * 9 * k;
      wim += `<path d="M${f2(x - 1.6 * k)} ${f2(y)} L${f2(x + 1.6 * k)} ${f2(y)} L${f2(x)} ${f2(y + 4 * k)}Z" fill="${i % 2 ? rot : papier}" stroke="${blau}" stroke-width="${f2(.3 * k)}" stroke-linejoin="round"/>`;
    }
    const sy = SYMBOLE[E.art] || SYMBOLE.fest;
    const deko = `<g transform="translate(${f2(W * .66 + (W * .34 - m) / 2)} ${f2(Math.min(oben - 6 * k, wy + 17 * k))}) scale(${f2(9 * k)})" fill="${papier}" stroke="${blau}" stroke-width="${f2(.05)}" stroke-linejoin="round"><path d="${SYM[sy[0]]}"/></g>`;
    const svg = svgDoc(W, H, defs, `<rect x="-3" y="-3" width="${W + 6}" height="${H + 6}" fill="${papier}"/>${kornFlaeche(W, H)}${wim}${oben - 6 * k > wy + 22 * k ? deko : ''}${fig}`);
    return { el, svg, grund: papier, farben: pal[2] };
  };

  /* 3 Leuchtschrift («Two Years») */
  STILE.neon = async function (E, r, F) {
    const W = F.b, H = F.h, k = W / 108, p = 5 * k, m = p + 6 * k, papier = '#efe6d6', schwarz = '#0f0c0c', creme = '#f3eadb', rot = '#d8261c';
    const pal = r.wahl([['#ff3b8d', 'Pink'], ['#ff2e3b', 'Rot'], ['#37e2ff', 'Eisblau'], ['#c8ff3a', 'Grün'], ['#ff9a1f', 'Orange']]);
    const neon = pal[0], kern = '#fff4f6', el = [];
    const oben = passe(txt('eschmal', 'WALK ON THE WILD SIDE', m, p + 6 * k, W - 2 * m - 24 * k, 3.2 * k, creme, { ausr: 'l', sperr: .22, zeile: 1 }), W - 2 * m - 24 * k);
    const L = leiste(E, m, H - p - 5 * k, W - 2 * m, 2.4 * k, creme);
    const ort = passe(txt('eschmal', E.ort.toUpperCase(), m, 0, W - 2 * m, 4.2 * k, creme, { sperr: .08, zeile: 1 }), W - 2 * m);
    ort.y = f2(L.oben - 5 * k - ort.h);
    const zeit = passe(txt('eschmal', [E.datum, E.zeit].filter(Boolean).join('  ·  ').toUpperCase(), m, 0, W - 2 * m, 6 * k, neon, { sperr: .04, zeile: 1 }), W - 2 * m);
    zeit.y = f2(ort.y - 2 * k - zeit.h);
    el.push(oben, zeit, ort, ...L.els);
    /* Leuchtschrift, gemessen mit derselben Schrift */
    const zeilen = teile(E.titel, E.titel.length > 26 ? 3 : E.titel.length > 12 ? 2 : 1).split('\n');
    let gr = 22 * k; const maxW = W - 2 * m - 4 * k;
    const bw = Math.max(...zeilen.map(z => breite({ typ: 'text', rolle: 'eneon', text: z, gr: 10, zeile: 1, sperr: 0 })));
    gr = Math.min(gr, maxW / (bw / 10));
    const oben2 = oben.y + oben.h + 18 * k, unten2 = zeit.y - 6 * k, hoehe = zeilen.length * gr * 1.02;
    if (hoehe > unten2 - oben2) gr *= (unten2 - oben2) / hoehe;
    const ty = oben2 + Math.max(0, (unten2 - oben2 - zeilen.length * gr * 1.02) / 2);
    const tx = zeilen.map((z, i) => `<text x="${f2(W / 2)}" y="${f2(ty + gr * (.78 + i * 1.02))}" text-anchor="middle">${esc(z)}</text>`).join('');
    const sy = SYMBOLE[E.art] || SYMBOLE.party, ic = SYM[sy[0] === 'burger' ? 'stern' : sy[0]], is = 12 * k, iy = ty - is * .75;
    const fonts = await Promise.all([fontUrl('eneon'), fontUrl('eschmal')]);
    const css = (fonts[0] ? `@font-face{font-family:N;src:url(${fonts[0]}) format('woff2')}` : '') + (fonts[1] ? `@font-face{font-family:A;src:url(${fonts[1]}) format('woff2')}` : '');
    /* Stempel rechts oben über der Kante */
    const sr = 13 * k, sx = W - p - 10 * k, sYy = p + 11 * k, dz = E.datum.replace(/\s*[–-]\s*/, '–\n').split('\n');
    const dgr = Math.min(7.5 * k, (sr - 4.4 * k) * 2 / (dz.length * 1.05), ...dz.map(z => (sr - 4.2 * k) * 1.75 / ((breite({ typ: 'text', rolle: 'eschmal', text: z, gr: 10, zeile: 1 }) || 30) / 10)));
    const stempel = `<g transform="translate(${f2(sx)} ${f2(sYy)}) rotate(${f2(r.zw(8, 16))})" filter="url(#rau)" fill="${rot}" font-family="A,Anton,Impact,sans-serif">`
      + `<circle r="${f2(sr)}" fill="none" stroke="${rot}" stroke-width="${f2(.9 * k)}"/><circle r="${f2(sr - 3.6 * k)}" fill="none" stroke="${rot}" stroke-width="${f2(.35 * k)}"/>`
      + `<path id="kreis" d="M${f2(-(sr - 2.6 * k))} 0 a${f2(sr - 2.6 * k)} ${f2(sr - 2.6 * k)} 0 1 1 ${f2(2 * (sr - 2.6 * k))} 0 a${f2(sr - 2.6 * k)} ${f2(sr - 2.6 * k)} 0 1 1 ${f2(-2 * (sr - 2.6 * k))} 0" fill="none"/>`
      + `<text font-size="${f2(1.9 * k)}" letter-spacing="${f2(.35 * k)}"><textPath xlink:href="#kreis" href="#kreis">WALK ON THE WILD SIDE ✶ LINDEN ✶</textPath></text>`
      + dz.map((z, i) => `<text y="${f2((i - (dz.length - 1) / 2) * dgr * 1.02 + dgr * .36)}" text-anchor="middle" font-size="${f2(dgr)}">${esc(z)}</text>`).join('') + `</g>`;
    const defs = korn(W, H, k, .45)
      + `<filter id="weit" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="${f2(2.4 * k)}"/></filter><filter id="nah" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="${f2(.7 * k)}"/></filter>`
      + `<filter id="rau" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="${f2(.7 / k)}" numOctaves="2" seed="${r.ganz(1, 90)}" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -3.2 0 0 0 2.3" result="m"/><feComposite in="SourceGraphic" in2="m" operator="in"/></filter>`
      + `<radialGradient id="wand" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="${neon}" stop-opacity=".22"/><stop offset="1" stop-color="${neon}" stop-opacity="0"/></radialGradient>`;
    const rohr = (inhalt, breite_) => `<g fill="none" stroke="${neon}" stroke-linecap="round" stroke-linejoin="round"><g filter="url(#weit)" stroke-width="${f2(breite_ * 3)}" opacity=".9">${inhalt}</g><g filter="url(#nah)" stroke-width="${f2(breite_ * 1.6)}">${inhalt}</g></g><g fill="none" stroke="${kern}" stroke-width="${f2(breite_ * .55)}" stroke-linecap="round" stroke-linejoin="round">${inhalt}</g>`;
    const fr = p + 3 * k, rahmenD = `<rect x="${f2(fr)}" y="${f2(fr)}" width="${f2(W - 2 * fr)}" height="${f2(H - 2 * fr)}" rx="${f2(3 * k)}" stroke-dasharray="${f2((W - 2 * fr) * .62)} ${f2(4 * k)}" stroke-dashoffset="${f2(r.zw(0, 60) * k)}"/>`;
    const icon = `<path transform="translate(${f2(W / 2)} ${f2(iy)}) scale(${f2(is)})" d="${ic}" vector-effect="non-scaling-stroke"/>`;
    const schrift = `<g font-family="N,Yellowtail,cursive" font-size="${f2(gr)}"><g filter="url(#weit)" fill="${neon}" opacity=".95">${tx}</g><g filter="url(#nah)" fill="${neon}">${tx}</g><g fill="${kern}" stroke="${neon}" stroke-width="${f2(.18 * k)}">${tx}</g></g>`;
    const svg = svgDoc(W, H, defs, `<rect x="-3" y="-3" width="${W + 6}" height="${H + 6}" fill="${papier}"/>${kornFlaeche(W, H)}`
      + `<rect x="${f2(p)}" y="${f2(p)}" width="${f2(W - 2 * p)}" height="${f2(H - 2 * p)}" rx="${f2(1.6 * k)}" fill="${schwarz}"/>`
      + `<ellipse cx="${f2(W / 2)}" cy="${f2(ty + zeilen.length * gr * .5)}" rx="${f2(W * .5)}" ry="${f2(zeilen.length * gr * 1.1 + 16 * k)}" fill="url(#wand)"/>`
      + rohr(rahmenD, .5 * k) + rohr(icon, .55 * k) + schrift + stempel, css);
    return { el, svg, grund: schwarz, farben: pal[1] + ' auf Schwarz' };
  };

  /* 4 Rosa mit Handschrift (Valentin) */
  STILE.rosa = function (E, r, F) {
    const W = F.b, H = F.h, k = W / 108, m = 8 * k;
    const pal = r.wahl([['#ffdbe2', '#e0141e', '#ff6f91', 'Rosa und Rot'], ['#ffe2cc', '#e5370f', '#ff9a3c', 'Pfirsich und Orange'], ['#ebdfff', '#5b2bd6', '#ff5fa8', 'Flieder und Violett'], ['#ffd6e0', '#c8102e', '#f08a24', 'Rosa und Kirsche']]);
    const [grund, rot, akz] = pal, el = [];
    const kopf = passe(txt('egrotesk', 'WALK ON THE WILD SIDE' + (E.partner[0] ? ' × ' + E.partner[0].toUpperCase() : ''), m, m + 1 * k, W - 2 * m, 2.6 * k, rot, { sperr: .06, zeile: 1 }), W - 2 * m);
    const n = E.titel.length > 28 ? 3 : E.titel.length > 13 ? 2 : 1;
    const titel = passe(txt('liebe', teile(E.titel.toUpperCase(), n), m, 0, W - 2 * m, 13 * k, rot, { zeile: .98 }), W - 2 * m, H * .3);
    titel.y = f2(H * .42 - titel.h / 2);
    const wort = (E.worte[0] && E.worte[0].length <= 12 ? E.worte[0] : { liebe: 'love', party: 'tonight', fest: 'sunshine', jubilaeum: 'cheers', konzert: 'live', saison: 'yeah', tasting: 'cheers' }[E.art] || 'yeah').toUpperCase();
    const tbw = Math.min(W - 2 * m, breite(titel)), rechts = W / 2 + tbw / 2;
    const hand = passe(txt('ehand', wort, m, 0, rechts - m, Math.max(titel.gr * 1.05, 9 * k), akz, { ausr: 'r', zeile: 1 }), Math.min(W * .6, rechts - m));
    hand.w = f2(rechts - m + 2 * k); hand.y = f2(titel.y + titel.h - titel.gr * .22);
    const L = leiste(E, m, H - m * .8, W - 2 * m, 2.5 * k, rot);
    const ort = passe(txt('ehand', E.ort, m, 0, W - 2 * m, 4.6 * k, akz, { zeile: 1 }), W - 2 * m); ort.y = f2(L.oben - 5 * k - ort.h);
    const dat = passe(txt('egrotesk', [E.datum, E.zeit].filter(Boolean).join('  ·  ').toUpperCase(), m, 0, W - 2 * m, 5.4 * k, rot, { zeile: 1 }), W - 2 * m); dat.y = f2(ort.y - 2.2 * k - dat.h);
    el.push(kopf, titel, hand, dat, ort, ...L.els);
    /* Herzen, Funken, Kringel – nie über der Schrift */
    const frei = [[kopf.y - 2 * k, kopf.y + kopf.h + 2 * k], [titel.y - 4 * k, hand.y + hand.h + 3 * k], [dat.y - 3 * k, H]];
    let deko = ''; const zahl = Math.round(22 * (H / W) / 1.25);
    for (let i = 0, versuch = 0; i < zahl && versuch < 400; versuch++) {
      const s = r.zw(3, 7.5) * k, x = r.zw(m * .6 + s / 2, W - m * .6 - s / 2), y = r.zw(m * .6 + s / 2, H - m - s / 2);
      if (frei.some(([a, b]) => y + s / 2 > a && y - s / 2 < b)) continue;
      i++;
      const art = r.wahl(['herz', 'herz', 'stern', 'kringel', 'punkt']), farbe = r.ja(.55) ? rot : akz, dreh = r.zw(-25, 25);
      if (art === 'kringel') deko += `<path transform="translate(${f2(x)} ${f2(y)}) rotate(${f2(dreh)}) scale(${f2(s)})" d="M-.5 0 q.125 -.3 .25 0 t.25 0 t.25 0 t.25 0" fill="none" stroke="${farbe}" stroke-width=".09" stroke-linecap="round"/>`;
      else if (art === 'punkt') deko += `<circle cx="${f2(x)}" cy="${f2(y)}" r="${f2(s * .12)}" fill="${farbe}"/>`;
      else deko += `<path transform="translate(${f2(x)} ${f2(y)}) rotate(${f2(dreh)}) scale(${f2(s)})" d="${SYM[art]}" ${r.ja(.6) ? `fill="${farbe}"` : `fill="none" stroke="${farbe}" stroke-width=".08" stroke-linejoin="round"`}/>`;
    }
    const svg = svgDoc(W, H, korn(W, H, k, .3), `<rect x="-3" y="-3" width="${W + 6}" height="${H + 6}" fill="${grund}"/>${kornFlaeche(W, H)}${deko}`);
    return { el, svg, grund, farben: pal[3] };
  };

  /* 5 Siebdruck */
  STILE.sieb = function (E, r, F) {
    const W = F.b, H = F.h, k = W / 108, m = 7 * k, papier = '#f1eadc';
    const pal = r.wahl([['#e8341c', '#1a00aa', 'Rot und Ultramarin'], ['#ff6a1a', '#0f5a44', 'Orange und Tanne'], ['#ff4f9a', '#1f3aa6', 'Pink und Blau'], ['#f2b705', '#141010', 'Gelb und Schwarz']]);
    const [c1, c2] = pal, el = [];
    const L = leiste(E, m, H - m * .8, W - 2 * m, 2.5 * k, c2);
    const ort = passe(txt('egrotesk', E.ort.toUpperCase(), m, 0, W * .62, 3.4 * k, c2, { ausr: 'l', zeile: 1.05 }), W * .62); ort.y = f2(L.oben - 5 * k - ort.h);
    const zeit = passe(txt('egrotesk', E.zeit.toUpperCase(), m, 0, W * .62, 3.4 * k, c2, { ausr: 'l', zeile: 1.05 }), W * .62); zeit.y = f2(ort.y - 1 * k - zeit.h);
    const dat = passe(txt('eschmal', E.datum.toUpperCase(), m, 0, W - 2 * m, 12 * k, c2, { ausr: 'l', zeile: 1, sperr: .01 }), W - 2 * m); dat.y = f2(zeit.y - 1.6 * k - dat.h);
    const worte = E.titel.toUpperCase().split(/\s+/).filter(Boolean);
    const zeilen = worte.length > 4 ? teile(worte.join(' '), 4) : worte.join('\n');
    const titel = passe(txt('eschmal', zeilen, m - .5 * k, m - 2 * k, W - 2 * m, 40 * k, c2, { ausr: 'l', zeile: .9, sperr: .005 }), W - 2 * m, dat.y - m - 8 * k);
    el.push(titel, dat, zeit, ort, ...L.els);
    /* Rasterkreis und versetzte Formen */
    const cx = r.zw(W * .55, W * .7), cy = r.zw(H * .4, H * .58), R = Math.min(W, H) * r.zw(.34, .42), step = 2.3 * k;
    let punkte = '';
    for (let y = cy - R; y <= cy + R; y += step) for (let x = cx - R; x <= cx + R; x += step) {
      const d = Math.hypot(x - cx, y - cy) / R; if (d > 1) continue;
      const rr = step * .5 * Math.min(1, (1 - d * .85)); if (rr < .12 * k) continue;
      punkte += `<circle cx="${f2(x)}" cy="${f2(y)}" r="${f2(rr)}"/>`;
    }
    const form = r.wahl(['halb', 'streifen', 'kreis']);
    const dx = r.zw(1.2, 2.4) * k, dy = r.zw(-1.6, 1.6) * k;
    let zweit = '';
    if (form === 'halb') zweit = `<path d="M${f2(cx - R * .8 + dx)} ${f2(cy + dy)} A${f2(R * .8)} ${f2(R * .8)} 0 0 1 ${f2(cx + R * .8 + dx)} ${f2(cy + dy)}Z" fill="${c1}" opacity=".55"/>`;
    if (form === 'kreis') zweit = `<circle cx="${f2(cx + dx - R * .35)}" cy="${f2(cy + dy - R * .35)}" r="${f2(R * .42)}" fill="${c1}" opacity=".5"/>`;
    if (form === 'streifen') for (let i = 0; i < 6; i++) zweit += `<rect x="${f2(cx - R + dx)}" y="${f2(cy - R * .9 + i * R * .32 + dy)}" width="${f2(2 * R)}" height="${f2(R * .12)}" fill="${c1}" opacity=".55" transform="rotate(-12 ${f2(cx)} ${f2(cy)})"/>`;
    const svg = svgDoc(W, H, korn(W, H, k, .45), `<rect x="-3" y="-3" width="${W + 6}" height="${H + 6}" fill="${papier}"/><g fill="${c1}" opacity=".92">${punkte}</g>${zweit}${kornFlaeche(W, H)}`);
    return { el, svg, grund: papier, farben: pal[2] };
  };

  /* ---------- Eingabe ---------- */
  function liste(s) { return String(s || '').split(/\s*(?:[,;·\n]|\s&\s|\sund\s)\s*/).map(x => x.trim()).filter(Boolean); }
  function werte() {
    const v = id => (($('#' + id) || {}).value || '').trim();
    const beispiel = !v('enName');
    const roh = beispiel ? BEISPIEL : { name: v('enName'), art: v('enArt') || 'fest', datum: v('enDatum'), zeit: v('enZeit'), ort: v('enOrt') || STANDORT, partner: v('enPartner'), stimmung: v('enStimmung') };
    const jahr = (/\b(20\d\d)\b/.exec(roh.name) || [])[1] || '';
    const titel = (roh.name.replace(/\s*\b20\d\d\b\s*/, ' ').trim() || roh.name).slice(0, 60);
    return { beispiel, name: roh.name, titel, jahr, art: roh.art, datum: roh.datum || 'Datum folgt', zeit: roh.zeit || '', ort: roh.ort || STANDORT,
      partner: liste(roh.partner).slice(0, 6), worte: liste(roh.stimmung).slice(0, 6), format: formatWahl() };
  }
  const formatWahl = () => ((document.querySelector('[data-enformat].an') || {}).dataset || {}).enformat || 'insta';
  function reihe(E) {
    const r = (REIHE[E.art] || REIHE.fest).slice(), t = (E.name + ' ' + E.worte.join(' ')).toLowerCase();
    const vor = s => { const i = r.indexOf(s); if (i > 0) { r.splice(i, 1); r.unshift(s); } };
    if (/okto|bier|wiesn|tracht|markt/.test(t)) vor('linien');
    if (/neon|nacht|club|jahre|years|geburtstag|jubil/.test(t)) vor('neon');
    if (/liebe|love|valentin|rosa|pink|herz/.test(t)) vor('rosa');
    if (/tanz|dance|vinyl|platte|limmer|open air|sonne/.test(t)) vor('platte');
    return r;
  }
  async function entwerfen() {
    await schriften();
    const E = werte(), F = DS.FORMATE[E.format];
    merke();
    const basis = hash([E.name, E.art, E.datum, E.zeit, E.ort, E.partner.join(','), E.worte.join(','), E.format].join('|'));
    const stile = reihe(E); stile.push(stile[0]);   // sechs Karten: die fünf Stile, der passendste zweimal (zwei Fassungen)
    const alt = IDEEN; IDEEN = [];
    for (let i = 0; i < stile.length; i++) {
      const s = stile[i], r = zufall(basis + wurf * 7919 + i * 104729);
      try {
        const e = await STILE[s](E, r, F);
        const key = bildEintragen(e.svg, F, `${STIL_NAMEN[s]} · ${E.name}`);
        const bild = { id: neueId(), typ: 'bild', bild: key, x: -DS.B, y: -DS.B, w: F.b + 2 * DS.B, h: F.h + 2 * DS.B, fx: .5, fy: .5, zoom: 1, slot: 'bild' };
        const doc = { id: 'd' + Date.now().toString(36) + i, name: `${E.name} · ${STIL_NAMEN[s]}`, formatKey: E.format, format: { b: F.b, h: F.h },
          seiten: [{ grund: e.grund, tapete: null, el: [bild].concat(e.el), frei: true }], hinweise: [], auftrag: 'Ideen-Engine: ' + E.name, geaendert: Date.now() };
        IDEEN.push({ stil: s, doc, svg: e.svg, farben: e.farben, zweite: i === stile.length - 1, E });
      } catch (err) { console.warn('Idee', s, err); }
    }
    alt.forEach(a => { const b = DS.M.bildIndex[a.doc.seiten[0].el[0].bild]; if (b && b.idee && !b.behalten) { try { URL.revokeObjectURL(b.url); } catch (e) { } delete DS.M.bildIndex[a.doc.seiten[0].el[0].bild]; } });
    zeichneIdeen(E);
  }
  function bildEintragen(svg, F, alt) {
    const key = 'idee-' + neueId(), url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
    DS.M.bildIndex[key] = { key, alt, w: Math.round((F.b + 2 * DS.B) * 10), h: Math.round((F.h + 2 * DS.B) * 10), datei: true, url, miniUrl: url, gruppe: 'Plakat-Ideen', idee: true };
    return key;
  }

  /* ---------- Ansicht ---------- */
  function formular() {
    const box = $('#msEngine'); if (!box || box.dataset.fertig) return;
    box.dataset.fertig = '1';
    const alt = lies();
    box.innerHTML = `<div class="ms-titel"><h1>Event beschreiben</h1><span class="ms-leise">Name, Datum, Ort und ein paar Stichworte: Die Plakatwerkstatt setzt sechs eigene Plakat-Ideen im Stil der Event-Plakate der Bar, mit gerechneten Illustrationen, sofort und ohne KI. Eine wählen und im Editor fertig machen.</span></div>
      <form class="en-form" id="enForm" autocomplete="off" novalidate>
        <div class="en-felder">
          <label class="en-breit"><span>Event</span><input id="enName" maxlength="60" placeholder="Zum Beispiel: ${esc(BEISPIEL.name)}"></label>
          <label><span>Art</span><select id="enArt">${ARTEN.map(([k, n]) => `<option value="${k}">${esc(n)}</option>`).join('')}</select></label>
          <label><span>Datum</span><input id="enDatum" maxlength="30" placeholder="Zum Beispiel: ${esc(BEISPIEL.datum)}"></label>
          <label><span>Uhrzeit</span><input id="enZeit" maxlength="30" placeholder="Zum Beispiel: ${esc(BEISPIEL.zeit)}"></label>
          <label><span>Ort</span><input id="enOrt" maxlength="60" value="${esc(STANDORT)}"></label>
          <label class="en-breit"><span>Partner, wenn es welche gibt</span><input id="enPartner" maxlength="140" placeholder="Zum Beispiel: ${esc(BEISPIEL.partner)}"></label>
          <label class="en-breit"><span>Stichworte und Stimmung</span><textarea id="enStimmung" maxlength="160" rows="2" placeholder="Zum Beispiel: ${esc(BEISPIEL.stimmung)}"></textarea></label>
        </div>
        <div class="en-unten">
          <span class="en-formate" role="group" aria-label="Format">${FORMATE.map(([k, n]) => `<button type="button" data-enformat="${k}" aria-pressed="false">${esc(n)}</button>`).join('')}</span>
          <span class="en-knoepfe"><button type="button" class="kn kn--ohne en-wurf" id="enWurf"><span>Neu würfeln</span><i>${WUERFEL}</i></button>
          <button class="kn knopf--voll glanz-kn" id="enLos" type="submit"><span>Ideen entwerfen</span><i>${PFEIL}</i></button></span>
        </div>
      </form>
      <p class="en-hinweis" id="enHinweis" role="status" aria-live="polite"></p>
      <div class="en-ideen" id="enIdeen"></div>`;
    if (alt) Object.entries({ enName: alt.name, enArt: alt.art, enDatum: alt.datum, enZeit: alt.zeit, enOrt: alt.ort, enPartner: alt.partner, enStimmung: alt.stimmung })
      .forEach(([id, v]) => { if (v != null && $('#' + id)) $('#' + id).value = v; });
    waehleFormat(alt && alt.format || 'insta');
    $('#enForm').addEventListener('submit', ev => { ev.preventDefault(); wurf = 0; los(); });
    $('#enWurf').addEventListener('click', () => { wurf++; los(); });
    box.querySelectorAll('[data-enformat]').forEach(b => b.addEventListener('click', () => { waehleFormat(b.dataset.enformat); los(); }));
  }
  function waehleFormat(f) { document.querySelectorAll('[data-enformat]').forEach(b => { const an = b.dataset.enformat === f; b.classList.toggle('an', an); b.setAttribute('aria-pressed', String(an)); }); }
  const lies = () => { try { return JSON.parse(localStorage.getItem(SPEICHER) || 'null'); } catch (e) { return null; } };
  function merke() {
    const v = id => (($('#' + id) || {}).value || '');
    try { localStorage.setItem(SPEICHER, JSON.stringify({ name: v('enName'), art: v('enArt'), datum: v('enDatum'), zeit: v('enZeit'), ort: v('enOrt'), partner: v('enPartner'), stimmung: v('enStimmung'), format: formatWahl() })); } catch (e) { }
  }
  let laeuft = null;
  async function los() {
    const k = $('#enLos'), w = $('#enWurf'); if (k) k.disabled = true; if (w) w.disabled = true;
    try { laeuft = entwerfen(); await laeuft; } catch (e) { console.warn(e); $('#enHinweis').textContent = 'Das hat nicht geklappt. Die Eingaben bleiben stehen, bitte noch einmal.'; }
    finally { if (k) k.disabled = false; if (w) w.disabled = false; }
  }
  function zeichneIdeen(E) {
    const box = $('#enIdeen'); if (!box) return;
    gezeichnet = true;
    $('#enHinweis').textContent = E.beispiel ? `Beispiel mit «${E.name}». Trag oben dein Event ein, dann entstehen die Ideen dafür.` : `Sechs Ideen für «${E.name}», ${DS.FORMATE[E.format].name}. «Neu würfeln» rechnet neue Figuren und Farben.`;
    box.innerHTML = '';
    IDEEN.forEach((idee, i) => {
      const k = document.createElement('div'); k.className = 'en-karte';
      const b = document.createElement('div'); b.className = 'en-blatt';
      k.appendChild(b);
      k.insertAdjacentHTML('beforeend', `<div class="en-text"><b>${esc(STIL_NAMEN[idee.stil])}${idee.zweite ? ', zweite Fassung' : ''}</b><p>${esc(STIL_IDEE[idee.stil])}</p><small>${esc(idee.farben)}</small></div>
        <button class="kn knopf--voll en-los" type="button"><span>Diese bearbeiten</span><i>${PFEIL}</i></button>`);
      k.querySelector('.en-los').addEventListener('click', ev => bearbeiten(idee, ev.currentTarget));
      box.appendChild(k);
    });
    neuGross();
  }
  function neuGross() { document.querySelectorAll('#enIdeen .en-blatt').forEach((b, i) => IDEEN[i] && blatt(b, IDEEN[i].doc, b.clientWidth || 300)); }
  function blatt(b, doc, bw) {
    const f = doc.format, B = DS.B, hmax = Math.min(560, Math.round(innerHeight * .78));
    let box = (bw - 2) * (f.h + 2 * B) / f.b; box = Math.min(box, hmax * (f.h + 2 * B) / f.h);
    try { b.replaceChildren(DSStudio.miniBox(doc, 0, Math.floor(box))); } catch (e) { console.warn(e); }
  }
  let groesse = 0;
  addEventListener('resize', () => { clearTimeout(groesse); groesse = setTimeout(() => { if (!offen || !IDEEN.length) return; neuGross(); }, 150); });

  /* «Diese bearbeiten»: Illustration als Foto ablegen (im Browser, wie eigene Fotos), dann die Drucksache im Editor öffnen */
  async function rastern(svg, F) {
    const pxmm = F.b > 200 ? 8 : 10, w = Math.round((F.b + 2 * DS.B) * pxmm), h = Math.round((F.h + 2 * DS.B) * pxmm);
    const url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
    try {
      const img = new Image(); img.decoding = 'sync'; img.src = url; await img.decode();
      const cv = document.createElement('canvas'); cv.width = w; cv.height = h;
      cv.getContext('2d').drawImage(img, 0, 0, w, h);
      return await new Promise((ok, nein) => cv.toBlob(b => b ? ok(b) : nein(new Error('Bild nicht entstanden')), 'image/png'));
    } finally { URL.revokeObjectURL(url); }
  }
  async function bearbeiten(idee, knopf) {
    const t = knopf.querySelector('span'), vorher = t.textContent; knopf.disabled = true; t.textContent = 'Wird vorbereitet …';
    const doc = JSON.parse(JSON.stringify(idee.doc)); doc.id = 'd' + Date.now().toString(36); doc.geaendert = Date.now();
    const bildEl = doc.seiten[0].el[0];
    try {
      const png = await rastern(idee.svg, doc.format);
      const datei = new File([png], `Plakat-Idee ${STIL_NAMEN[idee.stil]} ${idee.E.name}.png`, { type: 'image/png' });
      const neu = await DS.eigene.hinzu(DS.M, [datei]);
      if (neu && neu[0]) bildEl.bild = neu[0];
    } catch (e) {   // ohne Ablage bleibt die Illustration für diese Sitzung erhalten
      console.warn('Illustration nicht abgelegt', e); const b = DS.M.bildIndex[bildEl.bild]; if (b) b.behalten = true;
    }
    knopf.disabled = false; t.textContent = vorher;
    DSStudio.oeffne(doc); if (window.DSStart && DSStart.offen()) DSStart.zu();
  }

  function zeige() {
    offen = true; formular();
    if (!gezeichnet) los();
    else if (IDEEN.length) neuGross();
  }
  /* die Ansicht schliesst sich über die Navigation (start.js blendet #msEngine aus) */
  function start() { schriften(); const b = $('#msEngine'); if (b) new MutationObserver(() => { offen = !b.hidden; }).observe(b, { attributes: true, attributeFilter: ['hidden'] }); }
  window.DSEngine = { zeige, entwerfen: () => los(), ideen: () => IDEEN, STILE };
  if (window.DS && DS.M && window.DSStudio) start(); else document.addEventListener('ds:bereit', start, { once: true });
})();
