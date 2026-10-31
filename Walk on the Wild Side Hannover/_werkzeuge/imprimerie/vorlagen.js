/* Drucksachen-Studio · Vorlagen: elf Grundaufbauten im Hausstil. Jede Vorlage bekommt Format, Ton und Inhalt
   und setzt daraus frei verschiebbare Elemente. Alle Grössen wachsen mit dem Format, damit dieselbe Drucksache
   als A6-Karte und als A3-Plakat stimmt. Elemente tragen ihren «slot», damit Textänderungen beim Umsetzen bleiben. */
(function () {
  const DS = window.DS;
  let zaehler = 0;
  const neueId = () => 'e' + (Date.now() % 1e7).toString(36) + (zaehler++).toString(36);
  DS.neueId = neueId;

  const STIL = {
    titel: { zeile: 1.06, sperr: 0 },
    mono: { zeile: 1.6, sperr: .08, gross: true },
    kapitale: { zeile: 1.3, sperr: .08, gross: true },
    text: { zeile: 1.5, sperr: 0 },
    kursiv: { zeile: 1.5, sperr: 0 },
  };
  DS.STIL = STIL;

  /* stil (Vorlagen-Bibliothek, Robert 12.10.2026): rahmen 'ohne'|'einfach'|'doppelt', ausr 'c'|'l', titel 0.8–1.25, zeichen 0.6–1.5, bild 0.38–0.66 (Bildanteil) */
  function ctx(M, fmt, ton, stil) {
    const w = fmt.b, h = fmt.h, s = Math.sqrt(w * h / (105 * 148)), s8 = Math.pow(s, .8);
    const T = M.toene[ton] || M.toene.dunkel;
    const m = Math.max(7, 8 * s8);
    return { M, w, h, s, s8, T, m, ton, el: [], quer: w > h * 1.15, stil: stil || {}, rahmenZahl: 0 };
  }

  function tx(c, rolle, text, w, gr, farbe, o = {}) {
    const el = Object.assign({ id: neueId(), typ: 'text', rolle, text: String(text), x: o.x ?? (c.w - w) / 2, y: 0, w, gr: +gr.toFixed(2), farbe, ausr: 'c', deck: 1 }, STIL[rolle], o);
    el.h = DS.mess(el).h;
    return el;
  }
  const linie = (c, L, o = {}) => Object.assign({ id: neueId(), typ: 'linie', x: (c.w - L) / 2, y: 0, w: L, h: 0, staerke: .3, farbe: c.T.linie, deck: 1 }, o);
  const zeichen = (c, zw, o = {}) => { zw *= Math.min(1.6, Math.max(.5, c.stil.zeichen || 1)); return Object.assign({ id: neueId(), typ: 'zeichen', x: (c.w - zw) / 2, y: 0, w: zw, farbe: c.T.zeichen, deck: 1 }, o); };
  const hoehe = (c, el) => el.typ === 'zeichen' ? el.w * DS.zz(c.M, el).verh : el.typ === 'linie' ? el.staerke : el.h;

  /* Stapel: [element | zahl(abstand)] von oben nach unten setzen */
  function stapelHoehe(c, items) {
    let y = 0;
    for (const it of items) y += typeof it === 'number' ? it : hoehe(c, it);
    return y;
  }
  function stapel(c, items, y) {
    let lastGap = 0;
    for (const it of items) {
      if (typeof it === 'number') { y += it; lastGap = it; continue; }
      it.y = +y.toFixed(2); y += hoehe(c, it); c.el.push(it);
    }
    return y;
  }
  function stapelMitte(c, items, y0, y1) {
    let H = stapelHoehe(c, items);
    // Zu wenig Platz: Schrift und Abstände gemeinsam verkleinern, bis der Stapel passt (höchstens auf 60 %)
    for (let n = 0; n < 6 && H > (y1 - y0) + .05; n++) {
      const f = Math.max(.82, (y1 - y0) / H);
      items = items.map(it => {
        if (typeof it === 'number') return it * f;
        if (it.typ === 'text' && it.gr * f >= (it._gr0 || it.gr) * .6) { it._gr0 = it._gr0 || it.gr; it.gr = +(it.gr * f).toFixed(2); it.h = DS.mess(it).h; }
        return it;
      });
      H = stapelHoehe(c, items);
    }
    items.forEach(it => { if (it && it._gr0) delete it._gr0; });
    return stapel(c, items, Math.max(y0, y0 + (y1 - y0 - H) / 2));
  }
  /* Leere Felder und ihre Abstände aus einem Stapel entfernen */
  function sauber(items) {
    const out = [];
    for (const it of items) {
      if (it == null || it === false || it === '') { if (typeof out[out.length - 1] === 'number') out.pop(); continue; }
      out.push(it);
    }
    while (typeof out[0] === 'number') out.shift();
    while (typeof out[out.length - 1] === 'number') out.pop();
    return out;
  }

  function grund(c, seite, farbe, tapete) {
    seite.grund = farbe || c.T.grund;
    seite.tapete = tapete === undefined ? c.T.tapete : tapete;
  }
  function rahmen(c, inset, staerke = .25, deck = .75) {
    const r = inset ?? Math.max(4.5, 5 * c.s8);
    c.rahmenZahl++;
    if (c.stil.rahmen === 'ohne') return r;
    const ecke = c.stil.ecke ?? 2.2;
    c.el.push({ id: neueId(), typ: 'rahmen', x: r, y: r, w: c.w - 2 * r, h: c.h - 2 * r, staerke, r: ecke * c.s8, farbe: c.T.linie, deck });
    if (c.stil.rahmen === 'doppelt' && c.rahmenZahl === 1) { const r2 = r + 1.3 * c.s8; c.el.push({ id: neueId(), typ: 'rahmen', x: r2, y: r2, w: c.w - 2 * r2, h: c.h - 2 * r2, staerke: .15, r: Math.max(0, ecke - 1) * c.s8, farbe: c.T.linie, deck: deck * .8 }); }
    return r;
  }
  function foto(c, key, x, y, w, h, o = {}) {
    const el = Object.assign({ id: neueId(), typ: 'bild', bild: key, x, y, w, h, fx: .5, fy: .5, zoom: 1, slot: 'bild' }, o);
    c.el.push(el); return el;
  }
  function fuss(c, i, farbe, y1) {
    const t = i.fuss === undefined || i.fuss === null ? `${c.M.adr} · ${c.M.tel}` : i.fuss;
    if (!t) return y1 ?? c.h;
    const el = tx(c, 'mono', t, c.w - 2 * c.m - 6, 1.5 * c.s8, farbe || c.T.mono, { slot: 'fuss', deck: .85, sperr: .08 });
    el.y = +((y1 ?? c.h - c.m - 1.5 * c.s8) - el.h).toFixed(2);
    c.el.push(el);
    return el.y;
  }
  const titelGr = (c, t, faktor = 1, breite) => {
    let g = Math.min(9.4 * c.s * faktor * (c.stil.titel || 1), (breite || c.w) / 9.2 * Math.min(1.08, c.stil.titel || 1));
    const L = Math.max(...String(t || '').split('\n').map(z => z.length));
    if (L > 18) g *= .86; if (L > 26) g *= .86;
    return g;
  };

  /* ---------- die Vorlagen ---------- */
  const V = {};

  V.deckel = {
    name: 'Titelblatt', wofuer: 'Deckblatt, Einladung zum Anlass, Karte mit einem starken Titel',
    slots: ['ueber', 'titel*', 'unter', 'text', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite); const r = rahmen(c);
      const bw = c.w - 2 * (r + 6 * c.s8);
      const zh = Math.min(c.w * .3, 30 * c.s, c.h * .2);
      const items = sauber([
        zeichen(c, zh), 8 * c.s8,
        i.ueber && tx(c, 'mono', i.ueber, bw, 1.9 * c.s8, c.T.mono, { slot: 'ueber' }), i.ueber && 3 * c.s8,
        tx(c, 'titel', i.titel, bw, titelGr(c, i.titel), c.T.titel, { slot: 'titel' }), 5.5 * c.s8,
        linie(c, 14 * c.s8), 5 * c.s8,
        i.unter && tx(c, 'mono', i.unter, bw, 2.05 * c.s8, c.T.mono, { slot: 'unter' }), 6 * c.s8,
        i.text && tx(c, 'text', i.text, Math.min(bw, 80 * c.s8), 2.8 * c.s8, c.T.text, { slot: 'text' }),
      ]);
      const yF = fuss(c, i, null, c.h - r - 6 * c.s8);
      stapelMitte(c, items, r + 8 * c.s8, yF - 6 * c.s8);
    },
  };

  V.buehne = {
    name: 'Bild oben', wofuer: 'Flyer und Aushang mit grossem Foto oben, Text darunter; das Zeichen sitzt auf der Naht',
    slots: ['bild*', 'ueber', 'titel*', 'text', 'aktion', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite);
      const ph = c.h * Math.min(.66, Math.max(.38, c.stil.bild || (c.quer ? .5 : .54))), B = DS.B;
      foto(c, i.bild, -B, -B, c.w + 2 * B, ph + B);
      const d = 15 * c.s8;
      c.el.push({ id: neueId(), typ: 'flaeche', x: (c.w - d) / 2, y: ph - d / 2, w: d, h: d, r: d / 2, farbe: seite.grund, tapete: seite.tapete, deck: 1 });
      const zw = d * .6, z = zeichen(c, zw); z.y = ph - zw * c.M.zeichen.verh / 2; c.el.push(z);
      const bw = c.w - 2 * c.m - 6;
      const items = sauber([
        i.ueber && tx(c, 'mono', i.ueber, bw, 1.9 * c.s8, c.T.mono, { slot: 'ueber' }), i.ueber && 2.6 * c.s8,
        tx(c, 'titel', i.titel, bw, titelGr(c, i.titel, .82), c.T.titel, { slot: 'titel' }), 4.5 * c.s8,
        linie(c, 12 * c.s8), 4.5 * c.s8,
        i.text && tx(c, 'text', i.text, Math.min(bw, 86 * c.s8), 2.75 * c.s8, c.T.text, { slot: 'text' }), i.text && 4.5 * c.s8,
        i.aktion && tx(c, 'mono', i.aktion, bw, 2 * c.s8, c.T.mono, { slot: 'aktion' }),
      ]);
      const yF = fuss(c, i);
      stapelMitte(c, items, ph + d / 2 + 4 * c.s8, yF - 5 * c.s8);
    },
  };

  V.ansicht = {
    name: 'Ansichtskarte', wofuer: 'Postkarte: Foto randlos, kleines Schild mit dem Ort. Nur Haus von aussen oder Landschaft',
    slots: ['bild*', 'titel*', 'unter'],
    bau(c, i, seite) {
      grund(c, seite, 'navy', null);
      const B = DS.B;
      foto(c, i.bild, -B, -B, c.w + 2 * B, c.h + 2 * B);
      const dunkel = c.ton !== 'hell';
      const schild = dunkel ? 'papier' : 'navy', tf = dunkel ? 'navy' : 'papier', mf = dunkel ? 'taupe' : 'gold';
      const pad = 4.6 * c.s8, max = c.w * .62;
      const t = tx(c, 'titel', i.titel, max, Math.min(6.4 * c.s8, c.w / 15), tf, { ausr: 'l', slot: 'titel', x: pad });
      const u = i.unter ? tx(c, 'mono', i.unter, max, 1.55 * c.s8, mf, { ausr: 'l', slot: 'unter', x: pad }) : null;
      const bw = Math.max(DS.mess(t).bw, u ? DS.mess(u).bw : 0);
      const sh = pad * 2 + t.h + (u ? u.h + 1.2 * c.s8 : 0), R = 3 * c.s8;
      c.el.push({ id: neueId(), typ: 'flaeche', x: -B - R, y: c.h - sh, w: bw + 2 * pad + B + R + 1, h: sh + B + R, r: R, farbe: schild, tapete: dunkel ? null : 'dunkel', deck: 1 });
      t.w = u ? Math.max(bw + 1, 10) : bw + 1; if (u) u.w = t.w;
      stapel(c, sauber([t, u && 1.2 * c.s8, u]), c.h - sh + pad);
    },
  };

  V.karte = {
    name: 'Karte mit Liste', wofuer: 'Speise-, Getränke-, Behandlungs- oder Preiskarte: Einträge mit Name, Beschreibung, Preis',
    slots: ['ueber', 'titel*', 'text', 'liste*', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite); const r = rahmen(c);
      const x0 = r + 6 * c.s8, cw = c.w - 2 * x0;
      const kopf = sauber([
        zeichen(c, 10 * c.s8), 5 * c.s8,
        i.ueber && tx(c, 'mono', i.ueber, cw, 1.85 * c.s8, c.T.mono, { slot: 'ueber' }), i.ueber && 2.4 * c.s8,
        tx(c, 'titel', i.titel, cw, titelGr(c, i.titel, .74), c.T.titel, { slot: 'titel' }), 3.6 * c.s8,
        i.text && tx(c, 'kursiv', i.text, Math.min(cw, 80 * c.s8), 2.5 * c.s8, c.T.text, { slot: 'text', deck: .85 }),
      ]);
      const yK = stapel(c, kopf, r + 7 * c.s8) + 5 * c.s8;
      const yF = fuss(c, i, null, c.h - r - 5 * c.s8);
      const liste = (i.liste || []).filter(e => e && (e.name || e.preis));
      const verf = yF - 5 * c.s8 - yK;
      const sp = c.w / c.h > 1.6 && liste.length >= 3 ? 2 : 1, sg = 8 * c.s8, sw = (cw - (sp - 1) * sg) / sp;
      const baueListe = (k, luft) => {
        const els = []; let H = 0;
        const pw = Math.max(0, ...liste.map(e => e.preis ? DS.mess({ typ: 'text', rolle: 'mono', text: e.preis, w: 200, gr: 1.95 * c.s8 * k, ...STIL.mono, sperr: .08 }).bw : 0));
        const proSpalte = Math.ceil(liste.length / sp);
        for (let s0 = 0; s0 < sp; s0++) {
          const xs = x0 + s0 * (sw + sg), teil = liste.slice(s0 * proSpalte, (s0 + 1) * proSpalte);
          let y = 0;
          teil.forEach((e, j) => {
            const n = s0 * proSpalte + j, row = [];
            const nw = sw - (pw ? pw + 4 * c.s8 : 0);
            const nm = tx(c, 'titel', e.name || '', nw, 4.05 * c.s8 * k, c.T.titel, { ausr: 'l', x: xs, slot: `liste.${n}.name`, zeile: 1.12 });
            nm.y = y; row.push(nm);
            if (e.preis) {
              const p = tx(c, 'mono', e.preis, pw + 1, 1.95 * c.s8 * k, c.T.mono, { ausr: 'r', x: xs + sw - pw - 1, slot: `liste.${n}.preis`, sperr: .08 });
              p.y = y + (nm.gr * 1.12 - p.gr * 1.6) / 2 + .15 * c.s8 * k; row.push(p);
            }
            let yy = y + nm.h;
            if (e.detail) {
              const dt = tx(c, 'text', e.detail, nw, 2.3 * c.s8 * k, c.T.text, { ausr: 'l', x: xs, slot: `liste.${n}.detail`, deck: .78, zeile: 1.42 });
              dt.y = yy + .7 * c.s8 * k; row.push(dt); yy = dt.y + dt.h;
            }
            yy += 2.4 * c.s8 * k * luft;
            if (j < teil.length - 1) { row.push(linie(c, sw, { x: xs, y: yy, staerke: .15, deck: .4 })); yy += 2.4 * c.s8 * k * luft; }
            els.push(...row); y = yy;
          });
          H = Math.max(H, y);
        }
        return { els, H };
      };
      let k = 1, L = baueListe(k, 1);
      for (let n = 0; n < 8 && L.H > verf; n++) { k *= Math.max(.6, Math.sqrt(verf / L.H)) * .99; L = baueListe(k, 1); }
      if (L.H < verf * .7) { k = Math.min(1.35, Math.sqrt(verf * .8 / L.H)); L = baueListe(k, 1); if (L.H > verf) { k *= Math.sqrt(verf / L.H) * .98; L = baueListe(k, 1); } }
      if (L.H < verf * .85 && liste.length > sp) { const luft = Math.min(2.2, 1 + (verf * .92 - L.H) / (Math.ceil(liste.length / sp) * 4.8 * c.s8 * k)); L = baueListe(k, luft); }
      const dy = yK + Math.max(0, (verf - L.H) / 2) * .6;
      L.els.forEach(e => { e.y = +(e.y + dy).toFixed(2); c.el.push(e); });
    },
  };

  V.einladung = {
    name: 'Einladung', wofuer: 'Einladung zu Fest, Dinner, Hochzeit, Anlass: wann, wo, Bitte um Antwort',
    slots: ['ueber', 'titel*', 'wann', 'wo', 'text', 'aktion'],
    bau(c, i, seite) {
      grund(c, seite);
      const r = rahmen(c, null, .35, .85); rahmen(c, r + 1.4 * c.s8, .15, .6);
      const bw = c.w - 2 * (r + 8 * c.s8);
      const items = sauber([
        i.ueber && tx(c, 'mono', i.ueber, bw, 1.9 * c.s8, c.T.mono, { slot: 'ueber' }), i.ueber && 5 * c.s8,
        tx(c, 'titel', i.titel, bw, titelGr(c, i.titel, .95), c.T.titel, { slot: 'titel' }), 6 * c.s8,
        linie(c, 14 * c.s8), 6 * c.s8,
        i.wann && tx(c, 'mono', i.wann, bw, 2.45 * c.s8, c.T.titel, { slot: 'wann', sperr: .08 }), i.wann && 2 * c.s8,
        i.wo && tx(c, 'kursiv', i.wo, bw, 2.6 * c.s8, c.T.text, { slot: 'wo' }), 6 * c.s8,
        i.text && tx(c, 'text', i.text, Math.min(bw, 78 * c.s8), 2.7 * c.s8, c.T.text, { slot: 'text' }), i.text && 6 * c.s8,
        i.aktion && tx(c, 'mono', i.aktion, bw, 1.75 * c.s8, c.T.mono, { slot: 'aktion' }),
      ]);
      const z = zeichen(c, 9 * c.s8); z.y = c.h - r - 7 * c.s8 - hoehe(c, z); c.el.push(z);
      stapelMitte(c, items, r + 9 * c.s8, z.y - 6 * c.s8);
    },
  };

  V.programm = {
    name: 'Programm', wofuer: 'Termine, Veranstaltungen, Tagesablauf, Jahresprogramm: Datum, Titel, Ort',
    slots: ['ueber', 'titel*', 'termine*', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite); const r = rahmen(c);
      const x0 = r + 7 * c.s8, cw = c.w - 2 * x0;
      const kopf = sauber([
        i.ueber && tx(c, 'mono', i.ueber, cw, 1.85 * c.s8, c.T.mono, { slot: 'ueber', ausr: 'l', x: x0 }), i.ueber && 2.6 * c.s8,
        tx(c, 'titel', i.titel, cw, titelGr(c, i.titel, .8), c.T.titel, { slot: 'titel', ausr: 'l', x: x0 }), 4.4 * c.s8,
        linie(c, 14 * c.s8, { x: x0 }),
      ]);
      const yK = stapel(c, kopf, r + 9 * c.s8) + 7 * c.s8;
      const z = zeichen(c, 8 * c.s8, { x: c.w - x0 - 8 * c.s8 });
      const yF = fuss(c, Object.assign({}, i, {}), null, c.h - r - 5 * c.s8);
      const verf = yF - 6 * c.s8 - yK;
      const ter = (i.termine || []).filter(t => t && (t.was || t.wann));
      const sp = c.w / c.h > 1.6 && ter.length >= 3 ? 2 : 1, sg = 8 * c.s8, sw = (cw - (sp - 1) * sg) / sp, proSpalte = Math.ceil(ter.length / sp);
      const baue = (k, luft) => {
        const els = []; let H = 0;
        for (let s0 = 0; s0 < sp; s0++) {
          const xs = x0 + s0 * (sw + sg); let y = 0;
          ter.slice(s0 * proSpalte, (s0 + 1) * proSpalte).forEach((t, j) => {
            const n = s0 * proSpalte + j;
            if (t.wann) { const a = tx(c, 'mono', t.wann, sw, 1.8 * c.s8 * k, c.T.mono, { ausr: 'l', x: xs, slot: `termine.${n}.wann` }); a.y = y; els.push(a); y += a.h + .6 * c.s8 * k; }
            if (t.was) { const b = tx(c, 'titel', t.was, sw, 4.3 * c.s8 * k, c.T.titel, { ausr: 'l', x: xs, slot: `termine.${n}.was`, zeile: 1.12 }); b.y = y; els.push(b); y += b.h; }
            if (t.wo) { const d = tx(c, 'text', t.wo, sw, 2.3 * c.s8 * k, c.T.text, { ausr: 'l', x: xs, slot: `termine.${n}.wo`, deck: .75 }); d.y = y + .5 * c.s8 * k; els.push(d); y = d.y + d.h; }
            y += 4.6 * c.s8 * k * luft;
          });
          H = Math.max(H, y - 4.6 * c.s8 * k * luft);
        }
        return { els, H };
      };
      let k = 1, L = baue(k, 1);
      for (let n = 0; n < 8 && L.H > verf; n++) { k *= Math.max(.6, Math.sqrt(verf / L.H)) * .99; L = baue(k, 1); }
      if (L.H < verf * .7) { k = Math.min(1.35, Math.sqrt(verf * .8 / L.H)); L = baue(k, 1); if (L.H > verf) { k *= Math.sqrt(verf / L.H) * .98; L = baue(k, 1); } }
      if (L.H < verf * .85 && ter.length > sp) L = baue(k, Math.min(2, 1 + (verf * .92 - L.H) / (proSpalte * 4.6 * c.s8 * k)));
      L.els.forEach(e => { e.y = +(e.y + yK).toFixed(2); c.el.push(e); });
      void z;
    },
  };

  V.fenster = {
    name: 'Bild im Rahmen', wofuer: 'Foto mit Passepartout auf der Fläche, darunter Titel und Text; ruhig und edel',
    slots: ['bild*', 'ueber', 'titel*', 'unter', 'text', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite);
      const m = c.m + 1;
      if (c.quer) {
        const pw = c.w * .5 - m, ph = c.h - 2 * m;
        foto(c, i.bild, m, m, pw, ph);
        c.el.push({ id: neueId(), typ: 'rahmen', x: m - 1.6 * c.s8, y: m - 1.6 * c.s8, w: pw + 3.2 * c.s8, h: ph + 3.2 * c.s8, staerke: .25, r: 0, farbe: c.T.linie, deck: .8 });
        const x0 = c.w * .5 + 6 * c.s8, bw = c.w - x0 - m;
        const items = sauber([
          i.ueber && tx(c, 'mono', i.ueber, bw, 1.85 * c.s8, c.T.mono, { slot: 'ueber', x: x0 }), i.ueber && 2.6 * c.s8,
          tx(c, 'titel', i.titel, bw, titelGr(c, i.titel, .75, bw * 2), c.T.titel, { slot: 'titel', x: x0 }), 4.4 * c.s8,
          linie(c, 12 * c.s8, { x: x0 + (bw - 12 * c.s8) / 2 }), 4.4 * c.s8,
          i.unter && tx(c, 'mono', i.unter, bw, 1.9 * c.s8, c.T.mono, { slot: 'unter', x: x0 }), i.unter && 4 * c.s8,
          i.text && tx(c, 'text', i.text, bw, 2.6 * c.s8, c.T.text, { slot: 'text', x: x0 }),
        ]);
        stapelMitte(c, items, m, c.h - m);
        return;
      }
      const ph = c.h * Math.min(.56, Math.max(.36, (c.stil.bild || .54) * .87));
      foto(c, i.bild, m, m, c.w - 2 * m, ph);
      c.el.push({ id: neueId(), typ: 'rahmen', x: m - 1.6 * c.s8, y: m - 1.6 * c.s8, w: c.w - 2 * m + 3.2 * c.s8, h: ph + 3.2 * c.s8, staerke: .25, r: 0, farbe: c.T.linie, deck: .8 });
      const bw = c.w - 2 * m - 6;
      const items = sauber([
        i.ueber && tx(c, 'mono', i.ueber, bw, 1.85 * c.s8, c.T.mono, { slot: 'ueber' }), i.ueber && 2.6 * c.s8,
        tx(c, 'titel', i.titel, bw, titelGr(c, i.titel, .85), c.T.titel, { slot: 'titel' }), 4.5 * c.s8,
        linie(c, 12 * c.s8), 4.5 * c.s8,
        i.unter && tx(c, 'mono', i.unter, bw, 1.95 * c.s8, c.T.mono, { slot: 'unter' }), i.unter && 4 * c.s8,
        i.text && tx(c, 'text', i.text, Math.min(bw, 84 * c.s8), 2.7 * c.s8, c.T.text, { slot: 'text' }),
      ]);
      const yF = fuss(c, i);
      stapelMitte(c, items, m + ph + 8 * c.s8, yF - 5 * c.s8);
    },
  };

  V.geteilt = {
    name: 'Bild und Text geteilt', wofuer: 'Halb Foto, halb Text; quer nebeneinander, hoch übereinander. Für Restaurant, Wellness, Angebot',
    slots: ['bild*', 'ueber', 'titel*', 'text', 'aktion', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite);
      const B = DS.B;
      if (c.quer) {
        foto(c, i.bild, -B, -B, c.w * .5 + B, c.h + 2 * B);
        const x0 = c.w * .5 + c.m, bw = c.w - x0 - c.m;
        const items = sauber([
          zeichen(c, 9 * c.s8, { x: x0 + (bw - 9 * c.s8) / 2 }), 5 * c.s8,
          i.ueber && tx(c, 'mono', i.ueber, bw, 1.8 * c.s8, c.T.mono, { slot: 'ueber', x: x0 }), i.ueber && 2.6 * c.s8,
          tx(c, 'titel', i.titel, bw, titelGr(c, i.titel, .72, bw * 2), c.T.titel, { slot: 'titel', x: x0 }), 4.2 * c.s8,
          linie(c, 12 * c.s8, { x: x0 + (bw - 12 * c.s8) / 2 }), 4.2 * c.s8,
          i.text && tx(c, 'text', i.text, bw, 2.55 * c.s8, c.T.text, { slot: 'text', x: x0 }), i.text && 4 * c.s8,
          i.aktion && tx(c, 'mono', i.aktion, bw, 1.8 * c.s8, c.T.mono, { slot: 'aktion', x: x0 }),
        ]);
        stapelMitte(c, items, c.m, c.h - c.m);
        return;
      }
      const ph = c.h * Math.min(.62, Math.max(.4, c.stil.bild || .5));
      foto(c, i.bild, -B, c.h - ph, c.w + 2 * B, ph + B);
      const x0 = c.m + 2, bw = c.w - 2 * x0;
      const items = sauber([
        i.ueber && tx(c, 'mono', i.ueber, bw, 1.85 * c.s8, c.T.mono, { slot: 'ueber', ausr: 'l', x: x0 }), i.ueber && 2.8 * c.s8,
        tx(c, 'titel', i.titel, bw, titelGr(c, i.titel, .9), c.T.titel, { slot: 'titel', ausr: 'l', x: x0 }), 4.6 * c.s8,
        linie(c, 14 * c.s8, { x: x0 }), 4.6 * c.s8,
        i.text && tx(c, 'text', i.text, Math.min(bw, 90 * c.s8), 2.75 * c.s8, c.T.text, { slot: 'text', ausr: 'l', x: x0 }), i.text && 4.4 * c.s8,
        i.aktion && tx(c, 'mono', i.aktion, bw, 1.95 * c.s8, c.T.mono, { slot: 'aktion', ausr: 'l', x: x0 }),
      ]);
      stapelMitte(c, items, c.m, c.h - ph - c.m);
    },
  };

  V.gutschein = {
    name: 'Gutschein', wofuer: 'Gutschein oder Geschenkkarte mit Wert und Feldern für Für, Von und Nummer',
    slots: ['titel', 'unter', 'wert', 'text', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite); const r = rahmen(c);
      const titel = i.titel || 'Gutschein';
      const feld = (x, y, w, name, n) => {
        const l = tx(c, 'mono', name, 30, 1.55 * c.s8, c.T.mono, { ausr: 'l', x, slot: null }); l.y = y; c.el.push(l);
        c.el.push(linie(c, w - 12 * c.s8, { x: x + 12 * c.s8, y: y + l.h * .78, staerke: .15, deck: .6 }));
        void n;
      };
      if (c.quer) {
        const zw = Math.min(c.h * .42, c.w * .2);
        const z = zeichen(c, zw, { x: c.w * .17 - zw / 2 }); z.y = (c.h - hoehe(c, z)) / 2; c.el.push(z);
        c.el.push(linie(c, 0, { x: c.w * .33, y: r + 8 * c.s8, w: 0, h: c.h - 2 * r - 16 * c.s8, staerke: .2, deck: .7 }));
        const x0 = c.w * .38, bw = c.w - x0 - r - 8 * c.s8;
        const felder = 3 * 5.4 * c.s8;
        const items = sauber([
          tx(c, 'titel', titel, bw, Math.min(12 * c.s8, c.h / 6.5), c.T.titel, { slot: 'titel', ausr: 'l', x: x0 }), 3.5 * c.s8,
          i.unter && tx(c, 'mono', i.unter, bw, 1.9 * c.s8, c.T.mono, { slot: 'unter', ausr: 'l', x: x0 }), i.unter && 4 * c.s8,
          i.wert && tx(c, 'titel', i.wert, bw, Math.min(7 * c.s8, c.h / 11), c.ton === 'dunkel' ? 'gold' : c.T.titel, { slot: 'wert', ausr: 'l', x: x0 }), i.wert && 3 * c.s8,
          i.text && tx(c, 'text', i.text, bw * .9, 2.3 * c.s8, c.T.text, { slot: 'text', ausr: 'l', x: x0, deck: .85 }),
        ]);
        const yEnd = stapelMitte(c, items, r + 7 * c.s8, c.h - r - 8 * c.s8 - felder - 4 * c.s8);
        let y = Math.max(yEnd + 5 * c.s8, c.h - r - 7 * c.s8 - felder);
        for (const f of ['Für', 'Von', 'Nr.']) { feld(x0, y, bw, f); y += 5.4 * c.s8; }
        return;
      }
      const bw = c.w - 2 * (r + 7 * c.s8), x0 = r + 7 * c.s8;
      const items = sauber([
        zeichen(c, Math.min(26 * c.s8, c.w * .26)), 7 * c.s8,
        tx(c, 'titel', titel, bw, titelGr(c, titel, 1.05), c.T.titel, { slot: 'titel' }), 4.5 * c.s8,
        linie(c, 14 * c.s8), 4.5 * c.s8,
        i.unter && tx(c, 'mono', i.unter, bw, 1.95 * c.s8, c.T.mono, { slot: 'unter' }), i.unter && 5 * c.s8,
        i.wert && tx(c, 'titel', i.wert, bw, 7 * c.s8, c.ton === 'dunkel' ? 'gold' : c.T.titel, { slot: 'wert' }), i.wert && 4 * c.s8,
        i.text && tx(c, 'text', i.text, Math.min(bw, 70 * c.s8), 2.5 * c.s8, c.T.text, { slot: 'text', deck: .85 }),
      ]);
      const felder = 3 * 6 * c.s8;
      stapelMitte(c, items, r + 8 * c.s8, c.h - r - 10 * c.s8 - felder);
      let y = c.h - r - 8 * c.s8 - felder;
      for (const f of ['Für', 'Von', 'Nr.']) { feld(x0, y, bw, f); y += 6 * c.s8; }
    },
  };

  V.aushang = {
    name: 'Aushang', wofuer: 'Hinweis, Schild, Tischaufsteller, Info für Gäste: Titel und gut lesbarer Text',
    slots: ['ueber', 'titel*', 'text*', 'aktion', 'fuss'],
    bau(c, i, seite) {
      grund(c, seite); const r = rahmen(c);
      const bw = c.w - 2 * (r + 7 * c.s8);
      const z = zeichen(c, Math.min(15 * c.s8, c.w * .16)); z.y = r + 8 * c.s8; c.el.push(z);
      const items = sauber([
        i.ueber && tx(c, 'mono', i.ueber, bw, 1.95 * c.s8, c.T.mono, { slot: 'ueber' }), i.ueber && 3 * c.s8,
        tx(c, 'titel', i.titel, bw, titelGr(c, i.titel, .9), c.T.titel, { slot: 'titel' }), 5 * c.s8,
        linie(c, 14 * c.s8), 5.5 * c.s8,
        i.text && tx(c, 'text', i.text, Math.min(bw, 96 * c.s8), 3.15 * c.s8, c.T.text, { slot: 'text', zeile: 1.55 }), i.text && 6 * c.s8,
        i.aktion && tx(c, 'mono', i.aktion, bw, 2.1 * c.s8, c.T.mono, { slot: 'aktion' }),
      ]);
      const yF = fuss(c, i, null, c.h - r - 5 * c.s8);
      stapelMitte(c, items, z.y + hoehe(c, z) + 7 * c.s8, yF - 7 * c.s8);
    },
  };

  V.rueckseite = {
    name: 'Rückseite mit Adresse', wofuer: 'Rückseite eines Flyers oder einer Karte: Zeichen, Name, Adresse, Kontakt',
    slots: ['text'],
    bau(c, i, seite) {
      grund(c, seite); const r = rahmen(c);
      const M = c.M, bw = c.w - 2 * (r + 7 * c.s8);
      const items = sauber([
        zeichen(c, Math.min(19 * c.s8, c.w * .2)), 6 * c.s8,
        tx(c, 'kapitale', M.name, bw, 3.1 * c.s8, c.T.titel, { sperr: .08 }), 2 * c.s8,
        tx(c, 'mono', M.zeile, bw, 1.6 * c.s8, c.T.mono), 5 * c.s8,
        linie(c, 12 * c.s8), 5 * c.s8,
        i.text && tx(c, 'kursiv', i.text, Math.min(bw, 74 * c.s8), 2.55 * c.s8, c.T.text, { slot: 'text', deck: .9 }), i.text && 5 * c.s8,
        tx(c, 'text', [M.adr.replace(' · ', '\n'), M.tel, M.mail, M.web].join('\n'), bw, 2.45 * c.s8, c.T.text, { zeile: 1.75, deck: .9 }),
      ]);
      stapelMitte(c, items, r + 8 * c.s8, c.h - r - 8 * c.s8);
    },
  };

  V.kartengruss = {
    name: 'Postkarten-Rückseite', wofuer: 'Rückseite einer Ansichtskarte: links Platz für den Gruss, rechts Markenfeld und Adresszeilen',
    slots: ['titel', 'text'],
    bau(c, i, seite) {
      grund(c, seite, c.ton === 'dunkel' ? 'papier' : c.T.grund, null);
      const T = c.M.toene.hell, m = Math.max(7, 7 * c.s8), mx = c.w / 2;
      c.el.push(linie(c, 0, { x: mx, y: m + 4, w: 0, h: c.h - 2 * m - 8, staerke: .2, farbe: T.linie, deck: .7 }));
      const lw = mx - m - 6 * c.s8;
      const z = zeichen(c, 9 * c.s8, { x: m, farbe: T.zeichen }); z.y = m; c.el.push(z);
      const kopf = sauber([
        tx(c, 'kapitale', c.M.name, lw, 2.1 * c.s8, T.titel, { ausr: 'l', x: m, sperr: .08 }), 1.2 * c.s8,
        tx(c, 'mono', i.titel || c.M.zeile, lw, 1.45 * c.s8, T.mono, { ausr: 'l', x: m, slot: 'titel' }),
        i.text && 4 * c.s8, i.text && tx(c, 'kursiv', i.text, lw, 2.25 * c.s8, T.text, { ausr: 'l', x: m, slot: 'text', deck: .85 }),
      ]);
      stapel(c, kopf, m + hoehe(c, z) + 4 * c.s8);
      const f = tx(c, 'mono', `${c.M.adr} · ${c.M.web}`, lw, 1.25 * c.s8, T.mono, { ausr: 'l', x: m, deck: .8, sperr: .08 }); f.y = c.h - m - f.h; c.el.push(f);
      const mb = 19 * c.s8, mh = 23 * c.s8;
      c.el.push({ id: neueId(), typ: 'rahmen', x: c.w - m - mb, y: m, w: mb, h: mh, staerke: .2, r: 0, farbe: T.linie, deck: .8 });
      const mz = zeichen(c, mb * .42, { x: c.w - m - mb / 2 - mb * .21, farbe: T.zeichen, deck: .35 }); mz.y = m + (mh - hoehe(c, mz)) / 2; c.el.push(mz);
      const ax = mx + 6 * c.s8, aw = c.w - m - ax, top = m + mh + 10 * c.s8, gap = Math.min(9 * c.s8, (c.h - m - 4 - top) / 4);
      for (let n = 0; n < 4; n++) c.el.push(linie(c, aw, { x: ax, y: top + gap * (n + 1) - 2, staerke: .15, farbe: T.linie, deck: .6 }));
    },
  };


  /* ---------- Walk on the Wild Side (31.10.2026): die Plakat-Sprache der Bar ----------
     Zwei Plakate, abgelesen an den echten Plakaten (website/assets/bild/p-*, _quelle/ig, _quelle/facebook):
     1. SESSION (DJ-Abende, seit September 2025): Plakatcreme-Rand rund 5 %, darin die rot-cremefarbenen Wellen, oben links «SESSION» in breiten, sehr fetten
        Versalien (Ultramarin #1A00AA), darunter «SIP & / SOUNDS», das Gesicht des Abends in Schwarzweiss, rechts der Name, unten rechts das Datum «17|10»
        mit der Uhrzeit, im Fuss links die Wortmarke in Rot, rechts «HAASEMANNSTR. 13 / 30449 HANNOVER». Schrift: Rammetto One (OFL), Rolle «plakat».
     2. Das weisse Plakat «Eure Nachbarschafts-Mixology-Bar» (Relaunch 01.12.2023, Silvester, Tanz in den Mai): Bild oben, darunter die rote Wortmarke,
        die Zeile, der Titel in Versalien, Datum «31 | 12 | 25» mit Uhrzeit und die Angaben, unten die Adresse; alles linksbündig auf einer Kante.
     Alle Masse in Anteilen der Breite, damit dasselbe Plakat als Instagram-Beitrag, A3-Aushang und Story stimmt. */
  STIL.plakat = { zeile: 1.02, sperr: .02, gross: true };   // Sperrung höchstens .08 em (Fehlerbuch 10a, PDF)
  STIL.plakatfett = { zeile: 1.02, sperr: .02, gross: true };
  STIL.kopf = { zeile: 1, sperr: .01, gross: true };
  const plMass = (c, el, breite, hoehe) => {   // Text so gross setzen, dass er die Breite füllt, aber nicht höher als «hoehe» wird
    const m = DS.mess(Object.assign({}, el, { gr: 10, w: 100000 })).bw || 1;
    el.gr = +Math.min(10 * breite / m, hoehe).toFixed(2); el.h = DS.mess(el).h; return el;
  };
  const WS_FUSS = 'HAASEMANNSTR. 13\n30449 HANNOVER';
  V.plakat = {
    name: 'SESSION-Plakat', wofuer: 'DJ-Abend wie die SESSION-Plakate der Bar: rot-cremefarbene Wellen, Ultramarin-Schrift, das Gesicht des Abends in Schwarzweiss, Datum und Uhrzeit, Wortmarke und Adresse',
    slots: ['bild', 'grundbild', 'ueber', 'unter', 'name', 'tag*', 'zeit', 'fuss'],
    bau(c, i, seite) {
      const u = c.w, H = c.h, quadrat = H < u * 1.12;
      grund(c, seite, 'creme', null);
      const rx = +Math.max(u * .052, DS.SICHER + 1).toFixed(2), fussH = +Math.max(u * .075, 7).toFixed(2);
      const fy0 = rx, fy1 = +(H - rx * .55 - fussH).toFixed(2), fw = u - 2 * rx, fh = fy1 - fy0;
      foto(c, i.grundbild || 'welle-1', rx, fy0, fw, fh, { slot: 'grundbild' });
      if (i.bild) {
        const b = (c.M.bildIndex || {})[i.bild] || { w: 3, h: 4 }, ia = b.w / b.h;
        const ph = +(fh * (quadrat ? .7 : H > u * 1.6 ? .56 : .66)).toFixed(2), pw = +Math.min(fw * (quadrat ? .5 : .66), ph * Math.max(.72, Math.min(1.1, ia))).toFixed(2);
        foto(c, i.bild, +(rx + fw * .06).toFixed(2), +(fy1 - ph).toFixed(2), pw, ph, { slot: 'bild' });
      }
      const blau = 'blau', x0 = rx + fw * .035, w0 = fw * .93;
      const t = tx(c, 'plakat', i.ueber || 'SESSION', w0, u * .14, blau, { slot: 'ueber', ausr: 'l', x: x0, zeile: 1 });
      plMass(c, t, w0 * .97, u * .2); t.y = +(fy0 + fh * .035).toFixed(2); c.el.push(t);
      let y = t.y + t.h * .92;
      if (i.unter) { const s = tx(c, 'plakat', i.unter, fw * .5, t.gr * .3, blau, { slot: 'unter', ausr: 'l', x: x0 + t.gr * .02, zeile: 1.15 }); s.y = +y.toFixed(2); c.el.push(s); }
      const xr = rx + fw * .965, wr = fw * .55;
      const zt = i.zeit ? tx(c, 'plakat', i.zeit, wr, t.gr * .3, blau, { slot: 'zeit', ausr: 'r', x: xr - wr, zeile: 1 }) : null;
      const dt = tx(c, 'plakat', i.tag || '', wr, t.gr * .78, blau, { slot: 'tag', ausr: 'r', x: xr - wr, zeile: 1 });
      if (zt) plMass(c, zt, wr * .92, t.gr * .3);
      plMass(c, dt, wr * .95, t.gr * .78);
      let yb = fy1 - fh * .045;
      if (zt) { zt.y = +(yb - zt.h).toFixed(2); c.el.push(zt); yb = zt.y + zt.h * .06; }
      dt.y = +(yb - dt.h).toFixed(2); c.el.push(dt);
      if (i.name) { const n = tx(c, 'plakat', i.name, fw * .4, t.gr * .2, blau, { slot: 'name', ausr: 'r', x: xr - fw * .4, zeile: 1.12 }); n.y = +(fy0 + fh * (quadrat ? .5 : .47)).toFixed(2); c.el.push(n); }
      const Z = c.M.zeichen2 || c.M.zeichen, zh = fussH * .92, zw = +(zh / Z.verh).toFixed(2);
      c.el.push({ id: neueId(), typ: 'zeichen', z: 2, x: rx, y: +(fy1 + (H - fy1 - zh) / 2).toFixed(2), w: zw, farbe: 'logo', deck: 1 });
      const f = tx(c, 'mono', i.fuss || WS_FUSS, fw * .5, Math.max(1.5, u * .016), blau, { slot: 'fuss', ausr: 'r', x: rx + fw * .5, zeile: 1.45, sperr: .08 });
      f.y = +(fy1 + (H - fy1 - f.h) / 2).toFixed(2); c.el.push(f);
    },
  };
  V.plakathoch = Object.assign({}, V.plakat, { name: 'SESSION-Plakat, hoch' });
  V.plakatrueck = {
    name: 'Weisses Plakat der Bar', wofuer: 'Fest oder Ankündigung wie die weissen Plakate der Bar (Relaunch, Silvester, Tanz in den Mai): Bild oben, rote Wortmarke, «Eure Nachbarschafts-Mixology-Bar», Titel in Versalien, Datum, Angaben, Adresse',
    slots: ['bild*', 'ueber', 'titel*', 'tag', 'zeit', 'text', 'fuss'],
    bau(c, i, seite) {
      const u = c.w, H = c.h, dunkel = c.ton === 'dunkel';
      grund(c, seite, dunkel ? 'navy' : 'weiss', null);
      const farbe = dunkel ? 'weiss' : 'tinte', rx = +Math.max(u * .07, DS.SICHER + 1.5).toFixed(2), bw = u - 2 * rx;
      const b = (c.M.bildIndex || {})[i.bild] || { w: 1, h: 1 }, ia = b.w / b.h;
      const quadrat = H < u * 1.12;
      const bh = +Math.min(H * (quadrat ? .5 : H > u * 1.6 ? .5 : .56), bw / Math.max(.75, Math.min(1.35, ia))).toFixed(2);
      const x0 = rx, items = [];
      const Z = c.M.zeichen2 || c.M.zeichen, zh = +(u * (quadrat ? .1 : .12)).toFixed(2), zw = +(zh / Z.verh).toFixed(2);
      const kopf = { id: neueId(), typ: 'zeichen', z: 2, x: x0, y: 0, w: zw, farbe: 'logo', deck: 1 };
      const zeile = tx(c, 'kapitale', i.ueber || c.M.zeile || '', bw, Math.max(1.6, u * .022), farbe, { slot: 'ueber', ausr: 'l', x: x0, zeile: 1.2, sperr: .02 });
      const titel = tx(c, 'kapitale', i.titel || '', bw, Math.max(3, u * .052), farbe, { slot: 'titel', ausr: 'l', x: x0, zeile: 1.08, sperr: .01 });
      plMass(c, titel, bw, u * .056);
      const datum = [i.tag, i.zeit].filter(Boolean).join('    ');
      const d = datum ? tx(c, 'kursiv', datum, bw, Math.max(1.8, u * .024), farbe, { slot: 'tag', ausr: 'l', x: x0, zeile: 1.3 }) : null;
      const t = i.text ? tx(c, 'text', i.text, bw * .92, Math.max(1.8, u * .023), farbe, { slot: 'text', ausr: 'l', x: x0, zeile: 1.42 }) : null;
      const f = tx(c, 'kursiv', i.fuss || WS_FUSS, bw * .6, Math.max(1.6, u * .02), farbe, { slot: 'fuss', ausr: 'l', x: x0, zeile: 1.35 });
      const s = c.s8, liste = sauber([kopf, u * .022, zeile, u * .04, titel, u * .032, d, d && u * .024, t]);
      const yF = H - rx - f.h; f.y = +yF.toFixed(2);
      const yTop = rx + bh + u * .045, frei = yF - u * .04 - yTop;
      foto(c, i.bild, rx, rx, bw, bh);
      stapelMitte(c, liste, yTop, yTop + frei);
      // die Gruppe beginnt oben unter dem Bild wie auf den echten Plakaten, nicht in der Mitte
      const grp = c.el.filter(e => liste.includes(e)); const dy = Math.min(...grp.map(e => e.y)) - yTop;
      if (dy > u * .02) grp.forEach(e => { e.y = +(e.y - dy * .55).toFixed(2); });
      c.el.push(f); void s;
    },
  };
  V.plakatganz = {
    name: 'Plakat aus dem Archiv, ganz', wofuer: 'Ein echtes Plakat der Bar als ganzes Bild, nichts angeschnitten, mit weissem Rand; die Schrift steht schon im Plakat',
    slots: ['bild*'],
    /* Auftrag Oberchef 28.10.: echte Plakate mit eingebauter Schrift nie als Motiv unter neuer Schrift und nie angeschnitten, nur ganz im Archiv */
    bau(c, i, seite) {
      grund(c, seite, 'weiss', null);
      const rand = Math.min(c.w, c.h) * .04, fw = c.w - 2 * rand, fh = c.h - 2 * rand;
      const b = (c.M.bildIndex || {})[i.bild], ia = b && b.w && b.h ? b.w / b.h : 1;
      const w = Math.min(fw, fh * ia), h = w / ia;
      foto(c, i.bild, (c.w - w) / 2, (c.h - h) / 2, w, h);
    },
  };
  V.menue = {
    name: 'Menükarte am Tisch', wofuer: 'Karte des Abends am Platz: Wortmarke, Datum, je Gang Teller und Drink, wie die Karten der Abende auf der Website',
    slots: ['ueber', 'titel', 'liste*', 'text', 'fuss'],
    bau(c, i, seite) {
      const dunkel = c.ton === 'dunkel';
      grund(c, seite); const r = rahmen(c);
      const x0 = r + 6 * c.s8, cw = c.w - 2 * x0, Z2 = c.M.zeichen2;
      const kopf = [];
      if (Z2) { const zw = Math.min(cw * .78, 62 * c.s8); kopf.push({ id: neueId(), typ: 'zeichen', z: 2, x: (c.w - zw) / 2, y: 0, w: zw, farbe: dunkel ? 'weiss' : Z2.farben.zeichen, deck: 1 }, 1.6 * c.s8); }
      kopf.push(tx(c, 'kapitale', c.M.zeile || '', cw * .9, 1.5 * c.s8, dunkel ? 'gold' : c.T.mono, { slot: null, zeile: 1 }), 4.5 * c.s8);
      if (i.titel) kopf.push(tx(c, 'titel', i.titel, cw, 7.5 * c.s8, c.T.titel, { slot: 'titel' }), 1.8 * c.s8);
      if (i.ueber) kopf.push(tx(c, 'mono', i.ueber, cw, 1.85 * c.s8, i.akzent || c.T.mono, { slot: 'ueber' }));
      const yK = stapel(c, sauber(kopf), r + 7 * c.s8) + 3.5 * c.s8;
      c.el.push(linie(c, 12 * c.s8, { y: yK - 1.5 * c.s8, farbe: i.akzent || c.T.linie, staerke: .35 }));
      const yF = fuss(c, i, null, c.h - r - 5 * c.s8);
      const liste = (i.liste || []).filter(e => e && (e.name || e.detail || e.gang));
      const verf = yF - 4 * c.s8 - yK - (i.text ? 8 * c.s8 : 0);
      const baue = k => {
        const els = []; let y = 0;
        liste.forEach((e, n) => {
          if (e.gang) { const g = tx(c, 'mono', e.gang, cw, 1.7 * c.s8 * k, c.T.mono, { slot: `liste.${n}.gang` }); g.y = y; els.push(g); y += g.h + .6 * c.s8 * k; }
          if (e.name) { const t = tx(c, 'titel', e.name, cw, 3.1 * c.s8 * k, c.T.titel, { slot: `liste.${n}.name`, zeile: 1.16 }); t.y = y; els.push(t); y += t.h + .5 * c.s8 * k; }
          if (e.detail) { const d = tx(c, 'text', e.detail, cw * .92, 2.05 * c.s8 * k, c.T.text, { slot: `liste.${n}.detail`, deck: .8, zeile: 1.4 }); d.y = y; els.push(d); y += d.h; }
          y += 3.6 * c.s8 * k;
        });
        return { els, H: y - 3.6 * c.s8 * k };
      };
      let k = 1, L = baue(k);
      for (let n = 0; n < 8 && L.H > verf; n++) { k *= Math.max(.6, Math.sqrt(verf / L.H)) * .99; L = baue(k); }
      if (L.H < verf * .7) { k = Math.min(1.3, Math.sqrt(verf * .82 / L.H)); L = baue(k); if (L.H > verf) { k *= Math.sqrt(verf / L.H) * .98; L = baue(k); } }
      const dy = yK + Math.max(0, (verf - L.H) / 2);
      L.els.forEach(e => { e.y = +(e.y + dy).toFixed(2); c.el.push(e); });
      if (i.text) { const t = tx(c, 'kursiv', i.text, cw, 1.9 * c.s8, c.T.text, { slot: 'text', deck: .8 }); t.y = +(yF - 4 * c.s8 - t.h).toFixed(2); c.el.push(t); }
    },
  };
  DS.VORLAGEN = V;

  /* Eine Seite aus Vorlage + Inhalt setzen */
  DS.setze = function (M, formatKey, vorlage, ton, inhalt, stil) {
    const fmt = DS.FORMATE[formatKey];
    const c = ctx(M, fmt, ton, stil);
    const seite = { grund: 'navy', tapete: null, el: [], quelle: { vorlage, ton, inhalt: JSON.parse(JSON.stringify(inhalt || {})) } };
    if (stil && Object.keys(stil).length) seite.quelle.stil = Object.assign({}, stil);
    (V[vorlage] || V.deckel).bau(c, inhalt || {}, seite);
    if (ton === 'dc' && M.zeichen3) c.el.forEach(e => { if (e.typ === 'zeichen' && !e.z) e.z = 3; });
    if (c.stil.ausr === 'l' && LINKS_MOEGLICH.includes(vorlage) && !(vorlage === 'gutschein' && c.quer)) linksbuendig(c);
    seite.el = c.el;
    return seite;
  };
  /* Linksbündige Fassung: alles, was mittig auf der Achse steht, an den linken Satzrand (Fotos, Flächen, Rahmen bleiben) */
  const LINKS_MOEGLICH = ['deckel', 'buehne', 'fenster', 'aushang', 'einladung', 'gutschein'];
  function linksbuendig(c) {
    const rand = c.el.some(e => e.typ === 'rahmen') ? Math.max(4.5, 5 * c.s8) : 0;
    const L = Math.max(c.m + 2, rand + 7 * c.s8);
    const scheibe = c.el.find(e => e.typ === 'flaeche' && e.r && Math.abs(e.w - e.h) < .5);   // Zeichen auf der Naht (Bild oben) bleibt mittig
    const mittig = e => Math.abs(e.x + e.w / 2 - c.w / 2) < .8;
    for (const e of c.el) {
      if (e.typ === 'text' && e.ausr === 'c' && mittig(e) && !(e.slot === 'fuss')) { e.ausr = 'l'; e.w = Math.min(e.w, c.w - L - rand - 4 * c.s8); e.x = L; e.h = DS.mess(e).h; }
      else if (e.typ === 'linie' && mittig(e) && e.w < c.w * .5) e.x = L;
      else if (e.typ === 'zeichen' && mittig(e) && !scheibe) e.x = L;
    }
  }

  /* Ein ganzes Dokument aus einem Entwurf (der KI oder einer Vorlage) */
  DS.dokument = function (M, entwurf) {
    const fk = DS.FORMATE[entwurf.format] ? entwurf.format : 'a5h';
    return {
      id: 'd' + Date.now().toString(36),
      name: entwurf.name || 'Neue Drucksache',
      formatKey: fk, format: { b: DS.FORMATE[fk].b, h: DS.FORMATE[fk].h },
      seiten: entwurf.seiten.map(s => DS.setze(M, fk, s.vorlage, s.ton || 'dunkel', s.inhalt || {}, s.stil)),
      hinweise: entwurf.hinweise || [], auftrag: entwurf.auftrag || '', geaendert: Date.now(),
    };
  };

  /* Beispielinhalte im Wortlaut des Wild Side (geprüft in bau_vorlagen.py, eingesetzt von bau.py) */
  DS.BEISPIEL = {"deckel": {"ueber": "A UNiQUE EXPERiENCE BY MOMO X RUDI", "titel": "Culinarium", "unter": "Walk on the Wild Side · Haasemannstraße 13", "text": "Food-Pairing-Abende im Walk on the Wild Side in Linden: ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste."}, "buehne": {"bild": "tafelleer", "ueber": "Culinarium", "titel": "An der langen Tafel", "text": "Die Abende an der langen Tafel des Walk on the Wild Side: drei Gänge, fünf Drinks, vierzehn Plätze. Und wer dir erklärt, was auf dem Teller und im Glas ist.", "aktion": "Walk on the Wild Side · Haasemannstraße 13"}, "ansicht": {"bild": "barnacht", "titel": "Walk on the Wild Side", "unter": "Hannover-Linden"}, "karte": {"ueber": "Culinarium", "titel": "Vom Pass", "text": "Das Menü wechselt mit jedem Abend. Ein paar Teller und Drinks aus den letzten Ausgaben.", "liste": [{"name": "LAUCH / BLUMENKOHL / CHIPOTLE", "detail": "", "preis": ""}, {"name": "BLUMENKOHL / ROQUEFORT / KAPERN / QUINOA", "detail": "", "preis": ""}, {"name": "HOKKAIDO / KÜRBISKERNÖL / HASELNUSS", "detail": "", "preis": ""}, {"name": "SPAGHETTI-EIS / KIWI / WEISSE SCHOKOLADE", "detail": "", "preis": ""}], "fuss": "Walk on the Wild Side · Haasemannstraße 13"}, "einladung": {"ueber": "Culinarium", "titel": "Ein Abend an der Tafel", "wann": "27.–28. November", "wo": "Walk on the Wild Side · Haasemannstraße 13", "text": "Vierzehn Gäste an einer Tafel, drei Gänge aus der Küche und dazu fünf Signature Drinks, passend zum Essen. Momo erklärt am Tisch, was im Glas ist.", "aktion": "@walkonthewildside_hannover"}, "programm": {"ueber": "Culinarium", "titel": "Die nächsten Abende", "termine": [{"wann": "27.–28. November", "was": "Culinarium", "wo": "Walk on the Wild Side · Haasemannstraße 13"}, {"wann": "18.–19. Dezember", "was": "Culinarium", "wo": "Walk on the Wild Side · Haasemannstraße 13"}]}, "fenster": {"bild": "trio2", "ueber": "Culinarium", "titel": "Immer dieselben Leute", "unter": "A UNiQUE EXPERiENCE BY MOMO X RUDI", "text": "Hinter den Plakaten stehen dieselben Leute, Abend für Abend."}, "geteilt": {"bild": "schaumglas", "ueber": "Am Tisch erklärt", "titel": "Fatwashing", "text": "Die Spirituose nimmt den Geschmack eines Fetts an; kalt gestellt, wird das Fett wieder abgehoben.", "aktion": "Culinarium"}, "gutschein": {"titel": "Dein Platz an der Tafel", "unter": "A UNiQUE EXPERiENCE BY MOMO X RUDI", "wert": "Culinarium", "text": "Die Abende an der langen Tafel des Walk on the Wild Side: drei Gänge, fünf Drinks, vierzehn Plätze."}, "aushang": {"ueber": "Culinarium", "titel": "Heute ausgebucht", "text": "Der Abend ist ausgebucht, bevor er beginnt.", "aktion": "@walkonthewildside_hannover"}, "rueckseite": {"text": "Food-Pairing-Abende im Walk on the Wild Side in Linden: ein Menü mit fünf passenden Drinks an einer langen Tafel für vierzehn Gäste."}, "kartengruss": {"titel": "Walk on the Wild Side", "text": "Und wer dir erklärt, was auf dem Teller und im Glas ist."}, "plakat": {"bild": "pl_CyT32RTMB4d", "ueber": "", "ueberfarbe": "weiss", "zeile": "A UNiQUE EXPERiENCE BY MOMO X RUDI", "akzent": "#13606a"}, "plakatrueck": {"grund": "#0d545d", "ueber": "WALK\nON THE\nWILD SIDE", "tag1": "27 / 11 / 26", "zeit1": "19:00 UHR", "text": "3 GÄNGE MENÜ\n5 SiGNATURE DRiNKS", "tag2": "28 / 11 / 26", "zeit2": "17:00 UHR"}, "menue": {"titel": "Menü", "ueber": "Fr 21. und Sa 22. Februar 2025", "liste": [{"gang": "Apéritif", "name": "Sauerteig | Tomate | Butter", "detail": "Cognac | Toasted Pumpkin Samen | Limette | Champagner"}, {"gang": "Vorspeise", "name": "Miso | Sellerie | Röstzwiebeln", "detail": "Vodka | Tom Yam | Guava | Cocos | Acids | Soda"}, {"gang": "Hauptgang", "name": "Spinat | braune Butter | Parmesan", "detail": "Tequila | lakto-fermentierte Tomate | Agave | Limette"}, {"gang": "Dessert", "name": "Kaffee | Molke | Amaretto", "detail": "Vodka | Cacao | Matcha | Mango"}, {"gang": "Absacker", "name": "", "detail": "Gin | Turmeric | Ingwer"}], "akzent": "#d8b264", "fuss": "Walk on the Wild Side · Haasemannstraße 13"}, "plakathoch": {"bild": "pl_DPwlqcfiKcA", "ueber": "WALK ON THE WILD SIDE", "ueberfarbe": "#d6262b", "kopfschatten": "leuchten", "zeile": "A UNiQUE EXPERiENCE BY MOMO X RUDI", "tag1": "27 / 11 / 26", "zeit1": "19:00 UHR", "tag2": "28 / 11 / 26", "zeit2": "17:00 UHR", "text": "3 GÄNGE MENÜ\n5 SiGNATURE DRiNKS"}};
})();
