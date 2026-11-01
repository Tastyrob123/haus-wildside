/* gaeste-ansicht.js · Das Schaufenster (Walk on the Wild Side, 1.11.2026): Ansicht «Gastschichten» im Schreibtisch des Stamms (window.WS_EIGEN).
   Robert 1.11.2026: «wie würde ich hier neue Gastgeschichten hinzufügen?» Gleiches Muster wie die DJ-Abende (termine-ansicht.js) und die Termine
   des Culinarium: Hauptknopf «Neue Gastschicht» oben, leere Karte «+ Neue Gastschicht» am Ende der Reihe, Fenster mit Datum, Name, Satz und Foto
   (Fotos der Website oder eigenes hochladen wie bei «Foto tauschen»), «Ändern» und «Entfernen» (mit Rückfrage) je Gastschicht. Eingaben warten gelb
   und zählen in der Leiste; «Speichern» legt sie in den Entwurf, «Veröffentlichen» bringt sie mit allem anderen auf die Website (Probe-Kopie).
   Daten: gaeste.py (Ursprung website/unter.py › programm() › gaeste). Vor website.js laden. Kein fester Farbwert: alles aus dem Kleid (--wo-*). */
(function () {
  'use strict';
  var API = '/_werkzeuge/bureau/api/gaeste';
  var SEITE = '/_werkzeuge/bureau/vorschau/programm.html', ANKER = 'gaeste';
  var MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  var L = null, liste = [], H = null, vorschauBreite = 'rechner', vsKennung = '';

  function kopie(x) { return JSON.parse(JSON.stringify(x)); }
  function basis() { return L ? (L.entwurf || L.stand) : []; }
  function gleich(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
  function nach(id, l) { return (l || []).find(function (t) { return t.id === id; }); }
  function datum(d) { var p = d.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function wann(g) { if (!g.datum) return 'Datum fehlt'; var d = datum(g.datum); return d.getDate() + '. ' + MONATE[d.getMonth()] + ' ' + d.getFullYear(); }
  function punkt(g) { var p = (g.datum || '').split('-'); return p.length === 3 ? p[2] + '.' + p[1] + '.' + p[0] : ''; }
  function foto(k) { return ((L && L.fotos) || []).find(function (f) { return f.key === k; }) || { key: k, alt: '', bild: '/assets/bild/' + k + '-480.webp' }; }
  function sortiert(l) { return l.slice().sort(function (a, b) { return ((a.datum || '') + a.id).localeCompare((b.datum || '') + b.id); }); }
  function istHier() { return H && H.ansicht() === 'e:gaeste' && document.querySelector('#ws-mitte[data-ws-ansicht="e:gaeste"]'); }
  function mitte() { return document.getElementById('ws-mitte'); }

  async function ruf(methode, weg_, daten, adresse) {
    var r;
    try {
      r = await fetch(adresse || (API + (weg_ ? '/' + weg_ : '')), { method: methode, headers: daten ? { 'Content-Type': 'application/json' } : {}, body: daten ? JSON.stringify(daten) : undefined, cache: 'no-store' });
    } catch (e) { throw { fehler: 'NETZ · Der Server des Werkzeugs antwortet nicht. Deine Eingaben bleiben stehen.', stichwort: 'netz' }; }
    var j = {}; try { j = await r.json(); } catch (e) { /* leer */ }
    if (!r.ok) { j.status = r.status; throw j; }
    return j;
  }
  function uebernehmen(neu, eingabenBehalten) {
    if (!neu || !Array.isArray(neu.stand)) return;   /* eine Antwort ohne Stand (z. B. ein Prüfprogramm) ändert nichts */
    L = neu;
    if (!eingabenBehalten) liste = kopie(basis());
  }
  function unterschiede(alt, neu) {
    var aus = [];
    neu.forEach(function (g) { var a = nach(g.id, alt); if (!a) aus.push({ art: 'neu', t: g }); else if (!gleich(a, g)) aus.push({ art: 'geaendert', t: g, a: a }); });
    alt.forEach(function (a) { if (!nach(a.id, neu)) aus.push({ art: 'weg', t: a }); });
    return aus;
  }
  function kurzZeile(g) { return punkt(g) + ' · ' + (g.name || 'Name fehlt'); }
  function zeile(u) {
    if (u.art === 'neu') return 'neue Gastschicht ' + kurzZeile(u.t);
    if (u.art === 'weg') return 'von der Seite genommen: ' + kurzZeile(u.t);
    var d = [];
    if (u.a.datum !== u.t.datum) d.push('Datum «' + punkt(u.a) + '» wird «' + punkt(u.t) + '»');
    if (u.a.name !== u.t.name) d.push('«' + u.a.name + '» wird «' + u.t.name + '»');
    if (u.a.satz !== u.t.satz) d.push('neuer Satz');
    if (u.a.foto !== u.t.foto) d.push('anderes Foto');
    return kurzZeile(u.t) + ': ' + d.join(', ');
  }
  function offen() { return L ? unterschiede(basis(), sortiert(liste)).length : 0; }

  async function speichern() {
    try {
      var a = await ruf('POST', 'speichern', { gaeste: sortiert(liste), erwartet: L.kennung });
      uebernehmen(a, false);
      if (a.nichts) { H && H.melde(a.meldung); } else if (a.vorher) {
        var n = unterschiede(a.vorher, basis()), k = H.quit('Gespeichert', 'Gastschichten · ' + zeile(n[0] || { art: 'neu', t: basis()[0] || {} }) + (n.length > 1 ? ' und ' + H.mz(n.length - 1, 'weitere Änderung', 'weitere Änderungen') : ''), [
          H.taste('Vorher/nachher ansehen', function () { k.remove(); H.geh('e:gaeste').then(function () { var v = document.getElementById('gs-tv'); if (v) v.scrollIntoView({ block: 'start' }); }); }),
          H.taste('Rückgängig', function () { k.remove(); rueckgaengig(a.vorher); })], { 'data-ws-quittung': n.length, 'data-gs': 'gespeichert' });
        setTimeout(function () { if (k.isConnected) k.remove(); }, 9000);
      }
      if (istHier()) zeichne(mitte(), H);
      return true;
    } catch (e) {
      if (e.status === 409) return konflikt();
      H.fehler(e);
      return false;
    }
  }
  async function rueckgaengig(vorher) {
    try { uebernehmen(await ruf('POST', 'speichern', { gaeste: vorher, erwartet: L.kennung }), false); H.melde('Rückgängig gemacht', { mehr: 'Die Gastschichten sind wie vor diesem Speichern.' }); }
    catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
    H.neu(); if (istHier()) zeichne(mitte(), H);
  }
  async function neuLaden(behalten) { uebernehmen(await ruf('GET', ''), behalten); }
  function konflikt() {
    return neuLaden(true).then(function () {
      return new Promise(function (fertig) {
        H.fenster('Zwei haben', 'gleichzeitig geändert.', H.el('div', { class: 'ws-form' },
          H.el('p', {}, 'In einem anderen Fenster wurden die Gastschichten inzwischen gespeichert. Deine Eingaben sind nicht verloren und nichts wurde überschrieben.'),
          H.el('p', {}, 'Speicherst du, gilt deine Liste, so wie sie hier steht.')), [
          { text: 'Meine Eingaben verwerfen', tun: function (zu) { zu(); liste = kopie(basis()); H.neu(); if (istHier()) zeichne(mitte(), H); fertig(false); } },
          { text: 'Meine Eingaben speichern', haupt: true, tun: function (zu) { zu(); speichern().then(fertig); } }], { name: 'konflikt' });
      });
    });
  }

  /* ---------- Fenster: eine Gastschicht anlegen oder ändern */
  function hoehe(t) { t.style.height = 'auto'; t.style.height = t.scrollHeight + 'px'; }
  function textFeld(wert, name, label, max, zeilen) {
    var i = H.el('textarea', { class: 'gs-ein', name: name, rows: String(zeilen || 1), maxlength: String(max), autocomplete: 'off', spellcheck: 'true', 'aria-label': label });
    i.value = wert || '';
    i.addEventListener('keydown', function (e) { if (e.key === 'Enter') e.preventDefault(); });
    i.addEventListener('input', function () { if (/\n/.test(i.value)) i.value = i.value.replace(/\s*\n\s*/g, ' '); hoehe(i); });
    requestAnimationFrame(function () { hoehe(i); });
    return i;
  }
  function auswahlDatum(g, beiWahl) {
    var p = (g.datum || '').split('-'), j0 = new Date().getFullYear(), tage = [], mon = [], jahre = [];
    for (var i = 1; i <= 31; i++) tage.push({ wert: ('0' + i).slice(-2), text: i + '.' });
    MONATE.forEach(function (n, i) { mon.push({ wert: ('0' + (i + 1)).slice(-2), text: n }); });
    for (var j = j0 - 3; j <= j0 + 1; j++) jahre.push({ wert: String(j), text: String(j) });
    if (p[0] && !jahre.some(function (x) { return x.wert === p[0]; })) jahre.unshift({ wert: p[0], text: p[0] });
    var setze = function (k, w) { p[k] = w; beiWahl(p.join('-')); };
    return H.el('span', { class: 'cu-datum gs-datum' }, H.auswahl(tage, p[2], function (w) { setze(2, w); }, 'Tag'), H.auswahl(mon, p[1], function (w) { setze(1, w); }, 'Monat'), H.auswahl(jahre, p[0], function (w) { setze(0, w); }, 'Jahr'));
  }
  function pruefeEingabe(g) {
    if (!g.datum || isNaN(datum(g.datum).getTime()) || datum(g.datum).getMonth() + 1 !== +g.datum.split('-')[1]) return 'Diesen Tag gibt es nicht.';
    if (!String(g.name || '').trim()) return 'Wer stand hinterm Tresen? Trag den Namen des Gastes oder der Bar ein.';
    if (!String(g.satz || '').trim()) return 'Ein Satz zum Gast fehlt: woher er kommt, was er mitgebracht hat.';
    if (/[<>{}]/.test((g.name || '') + (g.satz || ''))) return 'Spitze und geschweifte Klammern stehen nicht auf der Karte.';
    if (!g.foto) return 'Bitte ein Foto wählen.';
    return '';
  }
  function hochladen(datei, fertig, meld) {
    if (!datei) return;
    if (!/^image\/(jpeg|png|webp)$/.test(datei.type)) { meld('Bitte ein Foto als JPG, PNG oder WebP wählen.'); return; }
    if (datei.size > 25 * 1024 * 1024) { meld('Das Foto ist grösser als 25 MB.'); return; }
    var r = new FileReader();
    r.onload = async function () {
      meld('Foto wird übernommen …');
      try {
        var a = await ruf('POST', '', { name: datei.name, daten: r.result, alt: '' }, '/api/x/website/hochladen/' + (H.haus || 'wildside'));
        await neuLaden(true);
        meld(a.meldung || 'Foto übernommen.');
        fertig(a.b);
      } catch (e) { meld((e && e.fehler) || 'Das Foto liess sich nicht übernehmen.'); }
    };
    r.readAsDataURL(datei);
  }
  function fenster(alt) {
    var neu = !alt, g = alt ? kopie(alt) : vorschlag();
    var gross = H.el('img', { src: g.foto ? foto(g.foto).bild : '', alt: '', class: 'gs-f__bild' });
    var info = H.el('p', { class: 'gs-f__info' }, g.foto ? foto(g.foto).alt : 'Noch kein Foto gewählt.');
    var meld = H.el('p', { class: 'cu-t__fehler gs-f__fehler', role: 'alert', hidden: true });
    var hochMeld = H.el('p', { class: 'gs-f__info', hidden: true });
    var fundus = H.el('div', { class: 'kuhle ws-fundus gs-fundus' });
    function waehle(k) {
      g.foto = k; gross.src = foto(k).bild; info.textContent = foto(k).alt || 'Eigenes Foto';
      [].forEach.call(fundus.children, function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-gs-foto') === k ? 'true' : 'false'); });
    }
    function fuelleFundus() {
      fundus.textContent = '';
      ((L && L.fotos) || []).forEach(function (f) {
        fundus.append(H.el('button', { class: 'ws-fwahl', type: 'button', 'aria-pressed': f.key === g.foto ? 'true' : 'false', title: f.alt, 'data-gs-foto': f.key, onclick: function () { waehle(f.key); } },
          H.el('span', { class: 'ws-fwahl__b' }, H.el('img', { src: f.bild, alt: '', loading: 'eager', decoding: 'sync' })),
          H.el('span', { class: 'ws-fwahl__t' }, (f.eigen ? 'Eigenes Foto · ' : '') + (f.alt || f.key))));
      });
    }
    fuelleFundus();
    var name = textFeld(g.name, 'name', 'Name des Gastes oder der Bar', 50, 1), satz = textFeld(g.satz, 'satz', 'Ein Satz zum Gast', 160, 2);
    var datei = H.el('input', { type: 'file', accept: 'image/jpeg,image/png,image/webp', hidden: true });
    datei.addEventListener('change', function () { hochladen(datei.files[0], function (k) { fuelleFundus(); if (k) waehle(k); }, function (t) { hochMeld.textContent = t; hochMeld.hidden = !t; }); datei.value = ''; });
    var inhalt = H.el('div', { class: 'ws-form gs-f' },
      H.el('p', { class: 'gs-f__satz' }, 'Wer stand neben Momo hinterm Tresen? Auf der Seite «Programm» liegt jede Gastschicht als verdeckte Karte, die sich umdreht, nach Datum in der Reihe.'),
      H.el('div', { class: 'gs-f__reihe' },
        H.el('label', { class: 'cu-f' }, H.el('span', { class: 'cu-f__l' }, 'Datum'), auswahlDatum(g, function (w) { g.datum = w; })),
        H.el('label', { class: 'cu-f' }, H.el('span', { class: 'cu-f__l' }, 'Gast oder Bar'), name)),
      H.el('label', { class: 'cu-f' }, H.el('span', { class: 'cu-f__l' }, 'Ein Satz zum Gast'), satz),
      H.el('div', { class: 'cu-f' }, H.el('span', { class: 'cu-f__l' }, 'Foto'),
        H.el('div', { class: 'gs-f__foto' }, H.el('figure', { class: 'gs-f__rahmen' }, gross), H.el('div', {}, info,
          H.el('button', { class: 'wo-kn wo-kn--klein gs-f__hoch', type: 'button', html: '<span>Eigenes Foto hochladen</span><i>' + (window.WO ? WO.ic('pfeil') : '') + '</i>', onclick: function () { datei.click(); } }),
          H.el('p', { class: 'gs-f__info' }, 'Mindestens 900 Pixel breit, höchstens 25 MB, JPG, PNG oder WebP.'), hochMeld, datei)),
        fundus),
      meld);
    H.fenster(neu ? 'Neue' : 'Gastschicht', neu ? 'Gastschicht.' : 'ändern.', inhalt, [
      { text: 'Abbrechen' },
      { text: neu ? 'Gastschicht anlegen' : 'Übernehmen', haupt: true, tun: function (zu) {
        g.name = name.value.replace(/\s+/g, ' ').trim(); g.satz = satz.value.replace(/\s+/g, ' ').trim();
        var f = pruefeEingabe(g); meld.textContent = f; meld.hidden = !f;
        if (f) return;
        if (neu) liste.push(g); else liste[liste.findIndex(function (x) { return x.id === g.id; })] = g;
        zu(); zeichne(mitte(), H); H.leiste(); H.neu();
        var k = document.querySelector('[data-gs-karte="' + g.id + '"]'); if (k) { k.scrollIntoView({ block: 'center' }); k.classList.add('cu-t--leuchtet'); }
        H.melde(neu ? 'Gastschicht angelegt' : 'Gastschicht geändert', { mehr: kurzZeile(g) + '. Erst mit «Speichern» im Entwurf; auf die Website kommt sie mit «Veröffentlichen».' });
      } }], { name: neu ? 'gast-neu' : 'gast-aendern' });
    setTimeout(function () { try { name.focus({ preventScroll: true }); } catch (e) { /* ohne Fokus */ } }, 60);
  }
  function vorschlag() {   // Heute, ohne Namen und Satz (nie erfunden), Foto: das erste eigene, sonst keins
    var d = new Date(), iso = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
    var eigen = ((L && L.fotos) || []).find(function (f) { return f.eigen; });
    return { id: 'n' + Date.now().toString(36).slice(-8), datum: iso, name: '', satz: '', foto: eigen ? eigen.key : '' };
  }
  function entfernen(g) {
    var neu = !nach(g.id, basis());
    H.fenster('Gastschicht', 'entfernen?', H.el('div', { class: 'ws-form' }, H.el('p', {}, kurzZeile(g) + ' verschwindet von der Seite «Programm», sobald du speicherst und veröffentlichst. Jeder veröffentlichte Stand lässt sich unter «Frühere Fassungen» zurückholen.')), [
      { text: 'Abbrechen' },
      { text: 'Ja, entfernen', haupt: true, tun: function (zu) {
        zu(); liste.splice(liste.indexOf(g), 1); zeichne(mitte(), H); H.leiste(); H.neu();
        if (!neu) H.melde('Gastschicht entfernt', { mehr: kurzZeile(g) + '. Erst mit «Speichern» im Entwurf.' });
      } }], { name: 'gast-entfernen' });
  }

  /* ---------- Zeichnen */
  function karte(g) {
    var b = nach(g.id, basis()), neu = !b, geaendert = b && !gleich(b, g), f = foto(g.foto);
    return H.el('article', { class: 'gs-k' + (neu || geaendert ? ' gs-k--offen' : ''), 'data-gs-karte': g.id },
      H.el('figure', { class: 'gs-k__b' }, H.el('img', { src: f.bild, alt: f.alt || '', loading: 'eager', decoding: 'sync' })),
      H.el('div', { class: 'gs-k__t' },
        H.el('span', { class: 'gs-k__d' }, punkt(g) + (neu ? ' · neu' : geaendert ? ' · geändert' : '')),
        H.el('h3', { class: 'gs-k__n' }, g.name),
        H.el('p', { class: 'gs-k__s' }, g.satz),
        H.el('div', { class: 'gs-k__kn' },
          H.link('Ändern', function () { fenster(g); }, { 'data-gs-aendern': g.id }),
          b && geaendert ? H.link('Wie gespeichert', function () { liste[liste.indexOf(g)] = kopie(b); zeichne(mitte(), H); H.leiste(); }) : null,
          H.link('Entfernen', function () { entfernen(g); }, { 'data-gs-weg': g.id }))));
  }
  function rasterBox() {
    var box = H.el('section', { class: 'gs-raster', 'aria-label': 'Gastschichten' });
    sortiert(liste).forEach(function (g) { box.append(karte(g)); });
    box.append(H.el('button', { class: 'gs-k gs-k--neu', type: 'button', 'data-gs-neu-karte': '1', onclick: function () { fenster(null); } },
      H.el('span', { class: 'gs-k__plus', 'aria-hidden': 'true', html: window.WO ? WO.ic('plus') : '+' }), H.el('b', {}, 'Neue Gastschicht'), H.el('span', {}, 'Datum, Name, Satz und Foto.')));
    return box;
  }
  function vergleich() {
    var u = L.wartet ? unterschiede(L.stand, L.entwurf) : [];
    var box = H.el('section', { class: 'cu-v', id: 'gs-tv' }, H.el('h2', { class: 'wo-zw' }, 'Vorher, ', H.el('em', {}, 'nachher')));
    if (!u.length) {
      box.append(H.el('p', { class: 'cu-leise' }, 'Im Entwurf wartet nichts. Was du speicherst, steht hier: durchgestrichen, was jetzt auf der Website steht, markiert, was nach dem Veröffentlichen gilt.'),
        H.el('div', { class: 'cu-v__z cu-v__z--beispiel' }, H.el('span', { class: 'cu-v__mk' }, 'Beispiel'), H.el('s', {}, '09.03.2024 · Aus dem Havn'), H.el('mark', {}, '09.03.2024 · Aus dem Havn, Hannover')));
      return box;
    }
    u.forEach(function (x) {
      box.append(H.el('div', { class: 'cu-v__z', 'data-gs-v': x.art }, H.el('span', { class: 'cu-v__mk' }, x.art === 'neu' ? 'Neu' : x.art === 'weg' ? 'Entfällt' : 'Geändert'),
        x.art !== 'neu' ? H.el('s', {}, kurzZeile(x.a || x.t) + ' · ' + (x.a || x.t).satz) : null,
        x.art !== 'weg' ? H.el('mark', {}, kurzZeile(x.t) + ' · ' + x.t.satz) : null));
    });
    box.append(H.el('div', { class: 'ws-reihe' }, H.link('Entwurf der Gastschichten verwerfen', function () {
      H.fenster('Entwurf der Gastschichten', 'verwerfen?', H.el('p', {}, H.mz(u.length, 'Änderung geht', 'Änderungen gehen') + ' verloren. Die Website bleibt, wie sie ist.'), [
        { text: 'Abbrechen' },
        { text: 'Ja, verwerfen', haupt: true, tun: async function (zu) {
          zu();
          try { var a = await ruf('POST', 'verwerfen', { erwartet: L.kennung }); var vorher = a.vorher; uebernehmen(a, false); H.neu(); zeichne(mitte(), H);
            var k = H.quit('Entwurf verworfen', 'Die Gastschichten stehen, wie sie veröffentlicht sind.', [H.taste('Rückgängig', function () { k.remove(); rueckgaengig(vorher); })]);
          } catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
        } }], { name: 'verwerfen' });
    }, { 'data-gs-verwerfen': '1' })));
    return box;
  }
  function verlauf() {
    var box = H.el('section', { class: 'cu-vl' }, H.el('h2', { class: 'wo-zw' }, 'Frühere ', H.el('em', {}, 'Fassungen')));
    var holen = function (nr, was) {
      return H.taste('In den Entwurf holen', async function () {
        try { uebernehmen(await ruf('POST', 'zurueckholen', { nr: nr, erwartet: L.kennung }), false); H.neu(); zeichne(mitte(), H);
          H.melde('In den Entwurf geholt', { mehr: was + '. Auf der Website erscheint es erst, wenn du veröffentlichst.' });
        } catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
      }, { 'data-gs-holen': String(nr) });
    };
    if (!L.verlauf.length) box.append(H.el('div', { class: 'cu-vl__z cu-vl__z--beispiel' }, H.el('span', { class: 'cu-v__mk' }, 'Beispiel'),
      H.el('b', {}, '01.11.2026, 18:30 Uhr'), H.el('span', {}, 'Veröffentlicht · 6 Gastschichten · Notiz «neuer Gast im November»')));
    L.verlauf.forEach(function (v) {
      box.append(H.el('div', { class: 'cu-vl__z' }, H.el('b', {}, H.zeit(v.zeit)), H.el('span', {}, 'Veröffentlicht · ' + H.mz(v.zahl, 'Gastschicht', 'Gastschichten') + (v.notiz ? ' · Notiz «' + v.notiz + '»' : '')), holen(v.nr, 'Die Fassung vom ' + H.zeit(v.zeit))));
    });
    box.append(H.el('div', { class: 'cu-vl__z cu-vl__z--ur' }, H.el('b', {}, 'Ursprünglicher Stand'), H.el('span', {}, 'Wie die Website gebaut ist · ' + H.mz(L.ursprung.length, 'Gastschicht', 'Gastschichten')), holen('ursprung', 'Der ursprüngliche Stand')));
    return box;
  }
  function vorschau() {
    var rahmen = H.el('iframe', { class: 'cu-vs__rahmen', src: SEITE, title: 'Vorschau der Seite «Programm» mit den Gastschichten des Entwurfs', loading: 'lazy' });
    rahmen.addEventListener('load', function () {
      try { var z = rahmen.contentDocument.getElementById(ANKER); if (z) rahmen.contentWindow.scrollTo(0, z.getBoundingClientRect().top + rahmen.contentWindow.scrollY); } catch (e) { /* ohne Rollen */ }
    });
    var huelle = H.el('div', { class: 'cu-vs__huelle', 'data-breite': vorschauBreite }, rahmen);
    var wahl = H.wahl2([{ wert: 'rechner', text: 'Rechner' }, { wert: 'handy', text: 'Handy' }], vorschauBreite, function (w) { vorschauBreite = w; huelle.setAttribute('data-breite', w); }, 'Breite der Vorschau', true);
    return H.el('section', { class: 'cu-vs' }, H.el('h2', { class: 'wo-zw' }, 'So sieht es ', H.el('em', {}, 'auf der Seite aus')),
      H.el('div', { class: 'cu-vs__kopf' }, H.el('p', { class: 'cu-leise' }, L.wartet ? 'Mit den Gastschichten des Entwurfs. Noch nicht gespeicherte Eingaben erscheinen nach «Speichern».' : 'Die Seite «Programm», wie sie gerade auf der Website steht.'), wahl,
        H.el('a', { class: 'ws-taste', href: SEITE + '#' + ANKER, target: '_blank', rel: 'noopener' }, 'Gross öffnen')), huelle);
  }
  function zeichne(ort, h) {
    H = h;
    var m = ort || mitte(), y = window.scrollY;
    if (m.querySelector(':scope > .cu-vs') && m.querySelector(':scope > .gs-raster') && vsKennung === L.kennung) {
      m.querySelector(':scope > .gs-raster').replaceWith(rasterBox());
      m.querySelector(':scope > .cu-v').replaceWith(vergleich());
      m.querySelector(':scope > .cu-vl').replaceWith(verlauf());
      m.setAttribute('data-gs', String(liste.length));
      return;
    }
    vsKennung = L.kennung;
    m.textContent = '';
    m.append(h.titel('Gäste hinterm Tresen', 'Gastschichten', 'pflegen.', 'Wer neben Momo hinterm Tresen stand: Datum, Gast oder Bar, ein Satz und ein Foto. Auf der Seite «Programm» liegt jede Gastschicht als verdeckte Karte, die sich umdreht, nach Datum in der Reihe.',
      [h.el('button', { class: 'wo-kn wo-kn--gold', type: 'button', 'data-gs-neu': '1', html: '<span>Neue Gastschicht</span><i>' + (window.WO ? WO.ic('plus') : '') + '</i>', onclick: function () { fenster(null); } }),
       h.el('a', { class: 'wo-kn', href: SEITE + '#' + ANKER, target: '_blank', rel: 'noopener', html: '<span>Auf der Seite ansehen</span><i>' + (window.WO ? WO.ic('auge') : '') + '</i>' })]));
    m.append(rasterBox(), vergleich(), vorschau(), verlauf(),
      h.el('p', { class: 'cu-quelle' }, 'Ursprung der Gastschichten: ' + L.quelle + '. Die Website wird hier nie verändert; veröffentlicht wird in die Probe-Kopie.'));
    if (h.opt && h.opt.halten) window.scrollTo(0, y);
    m.setAttribute('data-gs', String(liste.length));
  }

  window.WS_EIGEN = window.WS_EIGEN || {};
  window.WS_EIGEN.gaeste = {
    name: 'Gastschichten', gruppe: 'Das Haus', aufgabe: ['Neue Gastschicht', 'Wer neben Momo hinterm Tresen stand: Datum, Name, ein Satz und ein Foto.'],
    bereit: function () { return ruf('GET', '').then(function (a) { uebernehmen(a, false); }); },
    zeichne: async function (ort, h) { H = h; if (h.opt && h.opt.neuLaden) await neuLaden(true); zeichne(ort, h); },
    offen: offen,
    wartet: function () { return L && L.wartet ? unterschiede(L.stand, L.entwurf).length : 0; },
    speichern: function () { if (!H) return Promise.resolve(false); return speichern(); },
    zeilen: function () { return L && L.wartet ? unterschiede(L.stand, L.entwurf).map(zeile) : []; },
    veroeffentlichen: async function (notiz) {
      var n = this.wartet();
      uebernehmen(await ruf('POST', 'veroeffentlichen', { erwartet: L.kennung, notiz: notiz }), true);
      if (istHier()) zeichne(mitte(), H);
      return n;
    }
  };
})();
