/* termine-ansicht.js · Das Schaufenster (Walk on the Wild Side, Nachtbau 31.10.2026; Vorlage: die Ansicht «Termine» des Culinarium, 28.10.2026):
   Ansicht «DJ-Abende» im Schreibtisch des Stamms (window.WS_EIGEN, website.js). Die DJ-Abende der Bar (auf den Plakaten «SESSION») sind auf der
   Website Daten (website/bau.py › LINEUP), kein Text: der Server liest sie (termine.py), hier werden sie gepflegt. Aus ihnen entstehen die Plakatwand
   der Seite «Programm», der Kontaktbogen «Jeder Abend ein Plakat.» und der Flyer auf der Startseite. Eingaben warten gelb und zählen in der Leiste mit;
   «Speichern» der Leiste legt sie in den Entwurf, «Veröffentlichen» bringt sie (mit den Änderungen an Texten und Fotos) auf die Website (Probe-Kopie).
   Frühere Fassungen und der ursprüngliche Stand lassen sich zurückholen. Vor website.js laden. Kein fester Farbwert: alles aus dem Kleid (--wo-*). */
(function () {
  'use strict';
  var API = '/_werkzeuge/bureau/api/termine';
  var SEITE = '/_werkzeuge/bureau/vorschau/programm.html', ANKER = 'session';
  var TAGE = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
  var MONATE = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'];
  var L = null, liste = [], H = null, vorschauBreite = 'rechner';

  function kopie(x) { return JSON.parse(JSON.stringify(x)); }
  function basis() { return L ? (L.entwurf || L.stand) : []; }
  function gleich(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
  function nach(id, l) { return (l || []).find(function (t) { return t.id === id; }); }
  function datum(d) { var p = d.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function wann(t) { if (!t.datum) return 'Datum fehlt'; var d = datum(t.datum); return TAGE[d.getDay()] + ', ' + d.getDate() + '. ' + MONATE[d.getMonth()] + ' ' + d.getFullYear(); }
  function wer(t) { return (t.name || 'Name fehlt') + (t.zeile ? ' · ' + t.zeile : ''); }
  function plakatInfo(k) { return ((L && L.plakate) || []).find(function (p) { return p.key === k; }) || { key: k, alt: 'Plakat', bild: '/assets/bild/' + k + '-480.webp' }; }

  async function ruf(methode, weg_, daten) {
    var r;
    try {
      var vorab = methode === 'GET' && !daten && !weg_ && window.__vorab && window.__vorab[API]; if (vorab) delete window.__vorab[API];   // beim Laden der Seite schon geholt (index.html)
      r = await (vorab || fetch(API + (weg_ ? '/' + weg_ : ''), { method: methode, headers: daten ? { 'Content-Type': 'application/json' } : {}, body: daten ? JSON.stringify(daten) : undefined, cache: 'no-store' }));
    } catch (e) { throw { fehler: 'NETZ · Der Server des Werkzeugs antwortet nicht. Deine Eingaben bleiben stehen.', stichwort: 'netz' }; }
    var j = {}; try { j = await r.json(); } catch (e) { /* leer */ }
    if (!r.ok) { j.status = r.status; throw j; }
    return j;
  }
  function uebernehmen(neu, eingabenBehalten) {
    L = neu;
    if (!eingabenBehalten) liste = kopie(basis());
  }
  /* Was geändert ist: zwischen zwei Listen, je Abend, mit den Feldern, die sich unterscheiden */
  function unterschiede(alt, neu) {
    var aus = [];
    neu.forEach(function (t) {
      var a = nach(t.id, alt);
      if (!a) aus.push({ art: 'neu', t: t });
      else if (!gleich(a, t)) aus.push({ art: 'geaendert', t: t, a: a });
    });
    alt.forEach(function (a) { if (!nach(a.id, neu)) aus.push({ art: 'weg', t: a }); });
    return aus;
  }
  function zeile(u) {
    if (u.art === 'neu') return 'neuer DJ-Abend ' + wann(u.t) + ', ' + wer(u.t);
    if (u.art === 'weg') return 'von der Seite genommen: ' + wann(u.t) + ', ' + (u.t.name || '');
    var d = [];
    if (u.a.datum !== u.t.datum) d.push('«' + wann(u.a) + '» wird «' + wann(u.t) + '»');
    if (u.a.name !== u.t.name) d.push('«' + u.a.name + '» wird «' + u.t.name + '»');
    if (u.a.zeile !== u.t.zeile) d.push('Zeile «' + (u.a.zeile || 'leer') + '» wird «' + (u.t.zeile || 'leer') + '»');
    if (u.a.plakat !== u.t.plakat) d.push('anderes Plakat');
    return wann(u.t) + ': ' + d.join(', ');
  }
  function offen() { return L ? unterschiede(basis(), sortiert(liste)).length : 0; }
  function sortiert(l) { return l.slice().sort(function (a, b) { return (b.datum || '').localeCompare(a.datum || ''); }); }   // neuester Abend zuerst, wie auf der Website
  function istHier() { return H && H.ansicht() === 'e:termine' && document.querySelector('#ws-mitte[data-ws-ansicht="e:termine"]'); }

  async function speichern() {
    try {
      var a = await ruf('POST', 'speichern', { termine: sortiert(liste), erwartet: L.kennung });
      uebernehmen(a, false);
      if (a.nichts) { H && H.melde(a.meldung); } else {
        var n = unterschiede(a.vorher, basis()), k = H.quit('Gespeichert', 'DJ-Abende · ' + zeile(n[0] || { art: 'neu', t: basis()[0] || {} }) + (n.length > 1 ? ' und ' + H.mz(n.length - 1, 'weitere Änderung', 'weitere Änderungen') : ''), [
          H.taste('Vorher/nachher ansehen', function () { k.remove(); H.geh('e:termine').then(function () { var v = document.getElementById('cu-tv'); if (v) v.scrollIntoView({ block: 'start' }); }); }),
          H.taste('Rückgängig', function () { k.remove(); rueckgaengig(a.vorher); })], { 'data-ws-quittung': n.length, 'data-cu-termine': 'gespeichert' });
        setTimeout(function () { if (k.isConnected) k.remove(); }, 9000);
      }
      if (istHier()) zeichne(document.getElementById('ws-mitte'), H);
      return true;
    } catch (e) {
      if (e.status === 409) { return konflikt(); }
      H.fehler(e);
      return false;
    }
  }
  async function rueckgaengig(vorher) {
    try { uebernehmen(await ruf('POST', 'speichern', { termine: vorher, erwartet: L.kennung }), false); H.melde('Rückgängig gemacht', { mehr: 'Die DJ-Abende sind wie vor diesem Speichern.' }); }
    catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
    H.neu(); if (istHier()) zeichne(document.getElementById('ws-mitte'), H);
  }
  async function neuLaden(behalten) { uebernehmen(await ruf('GET', ''), behalten); }
  function konflikt() {
    return neuLaden(true).then(function () {
      return new Promise(function (fertig) {
        H.fenster('Zwei haben', 'gleichzeitig geändert.', H.el('div', { class: 'ws-form' },
          H.el('p', {}, 'In einem anderen Fenster wurden die DJ-Abende inzwischen gespeichert. Deine Eingaben sind nicht verloren und nichts wurde überschrieben.'),
          H.el('p', {}, 'Speicherst du, gilt deine Liste, so wie sie hier steht.')), [
          { text: 'Meine Eingaben verwerfen', tun: function (zu) { zu(); liste = kopie(basis()); H.neu(); if (istHier()) zeichne(document.getElementById('ws-mitte'), H); fertig(false); } },
          { text: 'Meine Eingaben speichern', haupt: true, tun: function (zu) { zu(); speichern().then(fertig); } }], { name: 'konflikt' });
      });
    });
  }

  /* ---------- Zeichnen */
  function plakat(t) {   // das Bild eines Abends: sein echtes Plakat, wie Plakatwand und Kontaktbogen es zeigen
    var p = plakatInfo(t.plakat);
    return '<figure class="cu-pl"><img src="' + p.bild + '" alt="' + esc(p.alt) + '" width="480" height="640" loading="lazy" decoding="async"></figure>';
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function feld(label, inhalt, art) { return H.el('label', { class: 'cu-f' + (art ? ' cu-f--' + art : '') }, H.el('span', { class: 'cu-f__l' }, label), inhalt); }
  function auswahlDatum(t, beiWahl) {   // Datum im Stil des Hauses (R21): Tag, Monat, Jahr als Auswahl, nie die des Betriebssystems
    var p = (t.datum || '').split('-'), j0 = new Date().getFullYear(), tage = [], mon = [], jahre = [];
    for (var i = 1; i <= 31; i++) tage.push({ wert: ('0' + i).slice(-2), text: i + '.' });
    MONATE.forEach(function (n, i) { mon.push({ wert: ('0' + (i + 1)).slice(-2), text: n }); });
    for (var j = j0 - 1; j <= j0 + 1; j++) jahre.push({ wert: String(j), text: String(j) });
    if (p[0] && !jahre.some(function (x) { return x.wert === p[0]; })) jahre.unshift({ wert: p[0], text: p[0] });
    var setze = function (k, w) { p[k] = w; beiWahl(p.join('-')); };
    return H.el('span', { class: 'cu-datum' }, H.auswahl(tage, p[2], function (w) { setze(2, w); }, 'Tag'), H.auswahl(mon, p[1], function (w) { setze(1, w); }, 'Monat'), H.auswahl(jahre, p[0], function (w) { setze(0, w); }, 'Jahr'));
  }
  function auswahlPlakat(t, beiWahl) {
    var o = ((L && L.plakate) || []).map(function (p) { return { wert: p.key, text: p.titel || p.alt }; });
    return H.auswahl(o, t.plakat, beiWahl, 'Plakat');
  }
  function textFeld(wert, name, label, beiTippen) {
    var i = H.el('input', { type: 'text', class: 'cu-zahl cu-ein', name: name, value: wert || '', maxlength: name === 'name' ? '60' : '80', autocomplete: 'off', spellcheck: 'false', 'aria-label': label });
    i.addEventListener('input', function () { beiTippen(i.value); });
    return i;
  }
  function pruefeEingabe(t) {
    if (!t.datum || isNaN(datum(t.datum).getTime()) || datum(t.datum).getMonth() + 1 !== +t.datum.split('-')[1]) return 'Diesen Tag gibt es nicht.';
    if (!String(t.name || '').trim()) return 'Wer legt auf? Trag den Namen ein, so wie er auf dem Plakat steht.';
    if (/[<>{}]/.test((t.name || '') + (t.zeile || ''))) return 'Spitze und geschweifte Klammern stehen nicht auf dem Plakat.';
    if (liste.some(function (x) { return x !== t && x.datum === t.datum; })) return 'An diesem Tag steht schon ein DJ-Abend.';
    return '';
  }
  function karte(t) {
    var b = nach(t.id, basis()), neu = !b, geaendert = b && !gleich(b, t);
    var fehler = pruefeEingabe(t);
    var meld = H.el('p', { class: 'cu-t__fehler', role: 'alert', hidden: !fehler }, fehler);
    var kopfZeile = H.el('p', { class: 'cu-t__wann' }, wann(t));
    var bild = H.el('div', { class: 'cu-t__bild', html: plakat(t) });
    function neuZeichnen(bildNeu) {
      var f = pruefeEingabe(t); meld.textContent = f; meld.hidden = !f;
      kopfZeile.textContent = wann(t); if (bildNeu) bild.innerHTML = plakat(t);
      var bb = nach(t.id, basis());
      k.classList.toggle('cu-t--offen', !bb || !gleich(bb, t));
      H.leiste();
    }
    var k = H.el('article', { class: 'cu-t' + (neu || geaendert ? ' cu-t--offen' : ''), 'data-cu-termin': t.id },
      bild,
      H.el('div', { class: 'cu-t__felder' },
        H.el('div', { class: 'cu-t__kopf' }, kopfZeile, neu ? H.el('span', { class: 'cu-t__marke' }, 'Neu') : null),
        H.el('div', { class: 'cu-t__reihe' },
          feld('Datum', auswahlDatum(t, function (w) { t.datum = w; neuZeichnen(); }), 'datum'),
          feld('Plakat', auswahlPlakat(t, function (w) { t.plakat = w; neuZeichnen(true); }), 'plakat')),
        H.el('div', { class: 'cu-t__reihe' },
          feld('Wer legt auf', textFeld(t.name, 'name', 'Wer legt auf', function (v) { t.name = v; neuZeichnen(); }), 'name'),
          feld('Zeile unter dem Namen', textFeld(t.zeile, 'zeile', 'Zeile unter dem Namen', function (v) { t.zeile = v; neuZeichnen(); }), 'zeile')),
        H.el('p', { class: 'cu-t__frei' }, 'Samstags 21 bis 1 Uhr. Die Zeile nennt Stil oder Herkunft und darf leer bleiben.'),
        meld,
        H.el('div', { class: 'cu-t__kn' },
          b && geaendert ? H.link('Wie gespeichert', function () { liste[liste.indexOf(t)] = kopie(b); zeichne(document.getElementById('ws-mitte'), H); H.leiste(); }) : null,
          H.link(neu ? 'Wieder entfernen' : 'Von der Seite nehmen', function () {
            var nr = liste.indexOf(t); liste.splice(nr, 1); zeichne(document.getElementById('ws-mitte'), H); H.leiste(); H.neu();
            if (!neu) H.melde('Von der Seite genommen', { mehr: wann(t) + '. Erst mit «Speichern» im Entwurf; jeder veröffentlichte Stand lässt sich zurückholen.' });
          }, { 'data-cu-weg': t.id }))));
    return k;
  }
  function neuerAbend() {   // Vorschlag aus den Abenden, die schon stehen: der Samstag vier Wochen nach dem neuesten (die Bar legt rund einmal im Monat auf)
    var l = sortiert(liste.length ? liste : basis().length ? basis() : (L ? L.ursprung : [])), letzter = l[0];
    var d = letzter ? datum(letzter.datum) : new Date(); d.setDate(d.getDate() + 28);
    while (d.getDay() !== 6) d.setDate(d.getDate() + 1);
    while (liste.some(function (x) { return x.datum === iso(d); })) d.setDate(d.getDate() + 7);
    var t = { id: 'n' + Date.now().toString(36).slice(-8), datum: iso(d), name: '', zeile: '', plakat: (L && L.plakate && L.plakate[0] ? L.plakate[0].key : '') };
    liste.push(t);
    zeichne(document.getElementById('ws-mitte'), H); H.neu();
    var k = document.querySelector('[data-cu-termin="' + t.id + '"]'); if (k) { k.scrollIntoView({ block: 'center' }); k.classList.add('cu-t--leuchtet'); var i = k.querySelector('input[name="name"]'); if (i) try { i.focus({ preventScroll: true }); } catch (e) { /* ohne Fokus */ } }
  }

  function vergleich() {   // «Vorher, nachher»: veröffentlicht (durchgestrichen) gegen Entwurf (markiert)
    var u = L.wartet ? unterschiede(L.stand, L.entwurf) : [];
    var box = H.el('section', { class: 'cu-v', id: 'cu-tv' }, H.el('h2', { class: 'wo-zw' }, 'Vorher, ', H.el('em', {}, 'nachher')));
    if (!u.length) {
      box.append(H.el('p', { class: 'cu-leise' }, 'Im Entwurf wartet nichts. Was du speicherst, steht hier: oben, was jetzt auf der Website steht, darunter, was nach dem Veröffentlichen gilt.'),
        H.el('div', { class: 'cu-v__z cu-v__z--beispiel' }, H.el('span', { class: 'cu-v__mk' }, 'Beispiel'), H.el('s', {}, 'Samstag, 17. Oktober 2026 · Ghazouani Brothers · elektronisch'), H.el('mark', {}, 'Samstag, 17. Oktober 2026 · Ghazouani Brothers · elektronisch, aus Tunis')));
      return box;
    }
    u.forEach(function (x) {
      box.append(H.el('div', { class: 'cu-v__z', 'data-cu-v': x.art },
        H.el('span', { class: 'cu-v__mk' }, x.art === 'neu' ? 'Neu' : x.art === 'weg' ? 'Entfällt' : 'Geändert'),
        x.art !== 'neu' ? H.el('s', {}, wann(x.a || x.t) + ' · ' + wer(x.a || x.t)) : null,
        x.art !== 'weg' ? H.el('mark', {}, wann(x.t) + ' · ' + wer(x.t)) : null));
    });
    box.append(H.el('div', { class: 'ws-reihe' }, H.link('Entwurf der DJ-Abende verwerfen', function () {
      H.fenster('Entwurf der DJ-Abende', 'verwerfen?', H.el('p', {}, H.mz(u.length, 'Änderung geht', 'Änderungen gehen') + ' verloren. Die Website bleibt, wie sie ist.'), [
        { text: 'Abbrechen' },
        { text: 'Ja, verwerfen', haupt: true, tun: async function (zu) {
          zu();
          try { var a = await ruf('POST', 'verwerfen', { erwartet: L.kennung }); var vorher = a.vorher; uebernehmen(a, false); H.neu(); zeichne(document.getElementById('ws-mitte'), H);
            var k = H.quit('Entwurf verworfen', 'Die DJ-Abende stehen, wie sie veröffentlicht sind.', [H.taste('Rückgängig', function () { k.remove(); rueckgaengig(vorher); })]);
          } catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
        } }], { name: 'verwerfen' });
    }, { 'data-cu-verwerfen': '1' })));
    return box;
  }
  function verlauf() {   // Frühere Fassungen (R14): Datum, Zahl, Notiz, «In den Entwurf holen», unten immer der ursprüngliche Stand
    var box = H.el('section', { class: 'cu-vl' }, H.el('h2', { class: 'wo-zw' }, 'Frühere ', H.el('em', {}, 'Fassungen')));
    var holen = function (nr, was) {
      return H.taste('In den Entwurf holen', async function () {
        try { uebernehmen(await ruf('POST', 'zurueckholen', { nr: nr, erwartet: L.kennung }), false); H.neu(); zeichne(document.getElementById('ws-mitte'), H);
          H.melde('In den Entwurf geholt', { mehr: was + '. Auf der Website erscheint es erst, wenn du veröffentlichst.' });
        } catch (e) { if (e.status === 409) { await neuLaden(true); H.melde('Inzwischen hat jemand anderes gespeichert.', { stichwort: 'konflikt' }); } else H.fehler(e); }
      }, { 'data-cu-holen': String(nr) });
    };
    if (!L.verlauf.length) box.append(H.el('div', { class: 'cu-vl__z cu-vl__z--beispiel' }, H.el('span', { class: 'cu-v__mk' }, 'Beispiel'),
      H.el('b', {}, '31.10.2026, 18:30 Uhr'), H.el('span', {}, 'Veröffentlicht · 10 Abende · Notiz «November dazu»')));
    L.verlauf.forEach(function (v) {
      box.append(H.el('div', { class: 'cu-vl__z' }, H.el('b', {}, H.zeit(v.zeit)), H.el('span', {}, 'Veröffentlicht · ' + H.mz(v.zahl, 'Abend', 'Abende') + (v.notiz ? ' · Notiz «' + v.notiz + '»' : '')), holen(v.nr, 'Die Fassung vom ' + H.zeit(v.zeit))));
    });
    box.append(H.el('div', { class: 'cu-vl__z cu-vl__z--ur' }, H.el('b', {}, 'Ursprünglicher Stand'), H.el('span', {}, 'Wie die Website gebaut ist · ' + H.mz(L.ursprung.length, 'Abend', 'Abende')), holen('ursprung', 'Der ursprüngliche Stand')));
    return box;
  }
  function vorschau() {
    /* ohne Anker laden: ein Anker im Rahmen rollt auch die Seite des Werkzeugs dorthin (Fund 28.10.2026); gerollt wird nur innen */
    var rahmen = H.el('iframe', { class: 'cu-vs__rahmen', src: SEITE, title: 'Vorschau der Seite «Programm» mit den DJ-Abenden des Entwurfs', loading: 'lazy' });
    rahmen.addEventListener('load', function () {
      try { var z = rahmen.contentDocument.getElementById(ANKER); if (z) rahmen.contentWindow.scrollTo(0, z.getBoundingClientRect().top + rahmen.contentWindow.scrollY); } catch (e) { /* ohne Rollen */ }
    });
    var huelle = H.el('div', { class: 'cu-vs__huelle', 'data-breite': vorschauBreite }, rahmen);
    var wahl = H.wahl2([{ wert: 'rechner', text: 'Rechner' }, { wert: 'handy', text: 'Handy' }], vorschauBreite, function (w) { vorschauBreite = w; huelle.setAttribute('data-breite', w); }, 'Breite der Vorschau', true);
    return H.el('section', { class: 'cu-vs' }, H.el('h2', { class: 'wo-zw' }, 'So sieht es ', H.el('em', {}, 'auf der Seite aus')),
      H.el('div', { class: 'cu-vs__kopf' }, H.el('p', { class: 'cu-leise' }, L.wartet ? 'Mit den DJ-Abenden des Entwurfs. Noch nicht gespeicherte Eingaben erscheinen nach «Speichern».' : 'Die Seite «Programm», wie sie gerade auf der Website steht.'), wahl,
        H.el('a', { class: 'ws-taste', href: SEITE + '#' + ANKER, target: '_blank', rel: 'noopener' }, 'Gross öffnen')), huelle);
  }

  var vsKennung = '';
  function zeichne(ort, h) {
    H = h;
    var m = ort || document.getElementById('ws-mitte');
    var y = window.scrollY;
    /* Neu zeichnen nach einer Eingabe (Neuer Abend, Entfernen): nur Liste, Vergleich und Verlauf; die eingebettete Vorschau bleibt stehen, solange
       der Entwurf derselbe ist (ein iframe lädt bei jedem Einsetzen neu, Messung 28.10.2026) */
    if (m.querySelector(':scope > .cu-vs') && m.querySelector(':scope > .cu-liste') && vsKennung === L.kennung) {
      m.querySelector(':scope > .cu-liste').replaceWith(listeBox(h));
      m.querySelector(':scope > .cu-v').replaceWith(vergleich());
      m.querySelector(':scope > .cu-vl').replaceWith(verlauf());
      m.setAttribute('data-cu-termine', String(liste.length));
      return;
    }
    vsKennung = L.kennung;
    m.textContent = '';
    m.append(h.titel('Samstags an der Bar', 'DJ-Abende', 'pflegen.', 'Jeder Abend, an dem jemand an der Bar auflegt: Tag, Name, eine Zeile dazu und sein Plakat. Auf der Seite «Programm» hängen sie als Plakatwand und Kontaktbogen, der neueste liegt als Flyer auf der Startseite.',
      [h.el('button', { class: 'wo-kn wo-kn--gold', type: 'button', 'data-cu-neu': '1', html: '<span>Neuer Abend</span><i>' + (window.WO ? WO.ic('plus') : '') + '</i>', onclick: neuerAbend }),
       h.el('a', { class: 'wo-kn', href: SEITE + '#' + ANKER, target: '_blank', rel: 'noopener', html: '<span>Auf der Seite ansehen</span><i>' + (window.WO ? WO.ic('auge') : '') + '</i>' })]));
    var s = sortiert(liste);
    m.append(listeBox(h), vergleich(), vorschau(), verlauf(),
      h.el('p', { class: 'cu-quelle' }, 'Ursprung der DJ-Abende: ' + L.quelle + '. Die Website wird hier nie verändert; veröffentlicht wird in die Probe-Kopie.'));
    if (h.opt && h.opt.halten) window.scrollTo(0, y);
    m.setAttribute('data-cu-termine', String(s.length));
  }
  function listeBox(h) {
    var s = sortiert(liste);
    var box = h.el('section', { class: 'cu-liste', 'aria-label': 'DJ-Abende' });
    if (!s.length) {
      box.append(h.el('div', { class: 'cu-leer' }, h.el('p', {}, 'Gerade steht kein DJ-Abend in der Liste. Mindestens einer bleibt auf der Seite: Plakatwand, Kontaktbogen und Flyer zeigen immer den neuesten. «Wie gespeichert» oder «Neuer Abend» füllt die Liste wieder.'),
        h.el('div', { class: 'cu-t cu-t--beispiel' }, h.el('div', { class: 'cu-t__bild', html: plakat({ plakat: L && L.plakate && L.plakate[0] ? L.plakate[0].key : 'p-1710' }) }),
          h.el('div', { class: 'cu-t__felder' }, h.el('p', { class: 'cu-t__wann' }, 'Beispiel: Samstag, 17. Oktober 2026'), h.el('p', { class: 'cu-t__frei' }, 'Ghazouani Brothers · elektronisch, aus Tunis. Mit «Neuer Abend» legst du einen an.')))));
    }
    s.forEach(function (t) { box.append(karte(t)); });
    return box;
  }

  window.WS_EIGEN = window.WS_EIGEN || {};
  window.WS_EIGEN.termine = {
    name: 'DJ-Abende', gruppe: 'Das Haus', aufgabe: ['Neuer DJ-Abend', 'Wer samstags auflegt: Tag, Name und Plakat eintragen, ändern oder von der Seite nehmen.'],
    bereit: function () { return ruf('GET', '').then(function (a) { uebernehmen(a, false); }); },
    zeichne: async function (ort, h) { H = h; if (h.opt && h.opt.neuLaden) await neuLaden(true); zeichne(ort, h); },
    offen: offen,
    wartet: function () { return L && L.wartet ? unterschiede(L.stand, L.entwurf).length : 0; },
    speichern: function () { if (!H) return Promise.resolve(false); return speichern(); },
    zeilen: function () { return L && L.wartet ? unterschiede(L.stand, L.entwurf).map(zeile) : []; },
    veroeffentlichen: async function (notiz) {
      var n = this.wartet();
      uebernehmen(await ruf('POST', 'veroeffentlichen', { erwartet: L.kennung, notiz: notiz }), true);
      if (istHier()) zeichne(document.getElementById('ws-mitte'), H);
      return n;
    }
  };
})();

/* Abnahme-Tor 2, 30.10.2026 (S2, K7): Kacheltitel und -unterschriften der Übersicht («Einen Text ändern», «Preis oder Öffnungszeit») ohne einzelnes Wort in der
   letzten Zeile: die letzten zwei Wörter bleiben zusammen (Safari kennt den Umbruch «pretty» noch nicht) */
(function () {
  function fest() {
    document.querySelectorAll(':is(.wo-ag__t, .wo-bk__t) > :is(b, span):not([data-fest]):not(:has(*))').forEach(function (b) {
      b.setAttribute('data-fest', '');
      var t = b.textContent.trim(), i = t.lastIndexOf(' '), j = i > 0 ? t.lastIndexOf(' ', i - 1) : -1;
      if (j < 0) return;
      b.textContent = t.slice(0, j + 1) + t.slice(j + 1).replace(' ', '\u00a0');
    });
  }
  /* Fenster «Foto tauschen»: der Bildtitel steht ganz (das gemeinsame Werkzeug kürzt ihn auf 48 Zeichen mit «…»; der volle steht im title) */
  function ganz() {
    document.querySelectorAll('.ws-fwahl:not([data-ganz])').forEach(function (k) {
      k.setAttribute('data-ganz', '');
      var t = k.querySelector('.ws-fwahl__t'), voll = k.getAttribute('title');
      if (!t || !voll || !/…$/.test(t.textContent)) return;
      t.textContent = (/^Eigenes Foto · /.test(t.textContent) ? 'Eigenes Foto · ' : '') + voll;
    });
  }
  /* Kein «×» als Zählzeichen (K24, Tor 2, 30.10.2026): «Link · 4× auf der Seite» heisst «Link · an 4 Stellen der Seite», «Steht 9× …» heisst «Steht an 9 Stellen …» */
  function ohneX() {
    document.querySelectorAll('.ws-st small, .ws-ang__lage, .ws-hoch, .ws-hoch *').forEach(function (e) {
      if (e.children.length) return;
      var t = e.textContent; if (t.indexOf('×') < 0) return;
      e.textContent = t.replace(/(\d+)× auf der Seite/g, '$1-mal auf der Seite').replace(/Steht (\d+)×/g, 'Steht an $1 Stellen').replace(/(\d+)\s*×\s*(\d+)/g, '$1 auf $2').replace(/(\d+)×/g, '$1-mal');   /* Masse wie in der Werkstatt: «1600 auf 1067» */
    });
  }
  /* Knopf «Website ansehen» im Kopf: zwischen 901 und 1240 px nur der runde Knauf (bureau.css); sein Name bleibt für Vorlesegeräte als aria-label */
  function knaufName() {
    document.querySelectorAll('#ws-kopf a.wo-kn--gold:not([aria-label])').forEach(function (a) { var t = a.textContent.trim(); if (t) a.setAttribute('aria-label', t); });
  }
  var plan = 0;
  function alles() { plan = 0; fest(); ganz(); ohneX(); knaufName(); }
  if (window.MutationObserver) new MutationObserver(function () { if (!plan) plan = requestAnimationFrame(alles); }).observe(document.documentElement, { childList: true, subtree: true, characterData: true });
})();
