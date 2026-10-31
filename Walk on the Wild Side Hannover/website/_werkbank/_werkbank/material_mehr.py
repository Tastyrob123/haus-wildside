#!/usr/bin/env python3
"""Walk on the Wild Side: der Ordner «Material» vollständig und frisch (Vorlage material_mehr.py des Culinarium, Prüfchat Gestaltung 29.10.2026;
Nachtbau Wild Side 31.10.2026). Läuft nach material.py des Kits und ist allein vollständig:
  1. leert die Ordner material/NN …, damit keine Datei einer früheren Fassung (Culinarium) liegen bleibt,
  2. ruft material.py des Kits (unverändert) noch einmal: Unterlagen, Drucksachen, Untersetzer, Zeichen, Ansichten, Instagram,
     dabei sammelt es die neuesten Dateien aus unterlagen/, drucksachen/, untersetzer/, feed/, _werkbank/ansichten/ ein,
  3. legt Sticker, Beigaben und Postkarten dazu (sticker/, beigaben/, postkarten/) und setzt sie vor den Ausklang,
  4. fehlt eine Quelle noch (ein anderer Teil baut gerade), fällt ihr Eintrag weg statt ins Leere zu zeigen,
  5. bringt die Seite ins Du und ins Kleid der Bar (dieselben Bausteine wie die übrigen Werkbank-Seiten: du_gang, kleid_wild, zeile_ganz, text_mitte).
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/material_mehr.py "<website/_werkbank>"   (wiederholbar; ein neuer Lauf holt die neuesten Dateien)"""
import glob, json, os, re, shutil
import kern as K
from kern import H, ROOT, W, e, kap, kn, PF
import material as M

ZIEL = M.ZIEL
FEHLT = []
_lege_kit = M.lege


def lege(ordner, quelle, name=None):
    """wie material.lege, aber eine fehlende Quelle bricht nicht ab: der Eintrag wird danach aus der Seite genommen"""
    if not os.path.exists(quelle):
        FEHLT.append(os.path.relpath(quelle, ROOT))
        return ordner + '/' + (name or os.path.basename(quelle))
    return _lege_kit(ordner, quelle, name)


def leeren():
    for d in glob.glob(os.path.join(ZIEL, '[0-9][0-9] *')):
        shutil.rmtree(d) if os.path.isdir(d) else os.remove(d)


def mehr():
    N = H.NAME
    sp = json.load(open(os.path.join(W, 'sticker_plan.json')))
    bp = json.load(open(os.path.join(W, 'beigaben_plan.json')))
    st = [('Druckbogen A3', lege('07 Sticker', os.path.join(ROOT, 'sticker', 'pdf', f'{H.KURZ}-sticker-druckbogen-a3.pdf'), f'{N} Sticker Druckbogen A3.pdf')),
          ('Alle einzeln', lege('07 Sticker', os.path.join(ROOT, 'sticker', 'pdf', f'{H.KURZ}-sticker-einzeln.pdf'), f'{N} Sticker einzeln.pdf'))]
    for x in sp['etiketten']:
        lege('07 Sticker/Bilder', os.path.join(W, 'roh', 'sticker', x['id'] + '.png'), 'Sticker ' + x['id'][1:] + ' ' + re.sub(r'[/:’]', ' ', x['name']).strip() + '.png')
    bg = [(d['name'], lege('08 Beigaben', os.path.join(ROOT, 'beigaben', 'pdf', f"{H.KURZ}-{d['id']}.pdf"), f"{N} {re.sub(r'[/:?’]', '', d['name']).strip()}.pdf")) for d in bp['druck']]
    pk = [(t, lege('09 Postkarten', os.path.join(ROOT, 'postkarten', 'pdf', f'{H.KURZ}-postkarten-{d}.pdf'), f'{N} Postkarten {t}.pdf'))
          for d, t in (('druck', 'mit Beschnitt'), ('sammelbogen-a3', 'Sammelbogen A3'), ('sammelbogen-sra3', 'Sammelbogen SRA3'))
          if os.path.exists(os.path.join(ROOT, 'postkarten', 'pdf', f'{H.KURZ}-postkarten-{d}.pdf'))]
    n_pk = len(json.load(open(os.path.join(W, 'postkarten_plan.json')))['karten'])
    namen = [d['name'] for d in bp['druck']]
    teile = ''
    for i, (name, satz, dateien, ident) in enumerate([
            ('Sticker', f'{K.zahl(len(sp["etiketten"]))} Sticker: der Druckbogen mit Schnittlinien, jeder einzeln und alle als Bild.', st, 'o-sticker'),
            ('Beigaben', (', '.join(namen[:-1]) + ' und ' + namen[-1] if len(namen) > 1 else ''.join(namen)) + ', jede als PDF.', bg, 'o-beigaben'),
            ('Postkarten', f'{K.zahl(n_pk)} Postkarten: mit Beschnitt für die Druckerei und als Sammelbogen.', pk, 'o-postkarten')]):
        zeilen = ''.join(f'<li data-a="auf" style="--i:{min(k, 6)}"><a href="{e(h)}" target="_blank" rel="noopener"><span>{e(t)}</span><i>{PF}</i></a></li>' for k, (t, h) in enumerate(dateien))
        teile += f'''<section class="fl {['fl--papier', 'fl--creme', 'fl--papier'][i]} blatt ordnerz" id="{ident}">
  <div class="in">
    <div>{kap(7 + i, e(name))}<div class="lauf"><p data-a="worte">{e(satz)}</p></div></div>
    <ul class="dateien">{zeilen}</ul>
  </div>
</section>
'''
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<section class="fl [^"]*" id="o-(sticker|beigaben|postkarten)">.*?</section>\n', '', s, flags=re.S)
    s = s.replace('<section class="ausklang">', teile + '<section class="ausklang">', 1)
    open(p, 'w', encoding='utf-8').write(s)
    return len(sp['etiketten']), len(bp['druck'])


IMPR = os.path.join(ROOT, '..', '..', '_werkzeuge', 'imprimerie', 'haeuser', 'wildside', 'drucksachen')


def plakatwerkstatt():
    """02 Drucksachen: dazu die fertigen Drucksachen der Plakatwerkstatt (SESSION-Plakate, Karten, Aushänge, Instagram-Bilder),
    jede als PDF, sofern sie nicht schon im Plan der Drucksachen steht. Quelle: _werkzeuge/imprimerie/haeuser/wildside/drucksachen/liste.json."""
    try:
        liste = json.load(open(os.path.join(IMPR, 'liste.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return 0
    schon = {x['id'] for x in json.load(open(os.path.join(W, 'papier_plan.json')))['druck']}
    zeilen = ''
    k0 = 0
    for x in liste:
        if x['k'] in schon or not x.get('pdf'):
            continue
        name = x['n'].replace('·', '–')
        h = lege('02 Drucksachen', os.path.join(IMPR, x['pdf']), f"{H.NAME} {re.sub(r'[/:?’]', ' ', name).strip()}.pdf")
        t = f"{x['n']} · {x['format']}".replace(' · ' + x['format'], ' · ' + x['format'].replace(' ', ' ')) if x.get('format') and x['format'] not in x['n'] else x['n']   # Format nie auseinander
        zeilen += f'<li data-a="auf" style="--i:{min(6, 5 + k0)}"><a href="{e(h)}" target="_blank" rel="noopener"><span>{e(t)}</span><i>{PF}</i></a></li>'
        k0 += 1
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    m = re.search(r'(<section class="fl [^"]*" id="o2">.*?<ul class="dateien[^"]*">)(.*?)(</ul>)', s, flags=re.S)
    if m and zeilen:
        s = s[:m.start(2)] + m.group(2) + zeilen + s[m.end(2):]
        s = s.replace(m.group(1), m.group(1).replace('<ul class="dateien">', '<ul class="dateien dateien--2">'), 1)
        open(p, 'w', encoding='utf-8').write(s)
    return k0


AUSLAGE = [   # (Quelle, Klasse, links %, oben %, Breite %, Drehung): ein Stapel aus dem, was in den Ordnern liegt
    (os.path.join(IMPR, 'session-aushang-a3.jpg'), 'blattbild', 2, 6, 34, -6),
    (os.path.join(IMPR, 'karte-preise-der-bar.jpg'), 'blattbild', 33, 0, 32, 3),
    (os.path.join(IMPR, 'instagram-falstaff.jpg'), 'blattbild', 63, 10, 33, -3),
    ('03 Untersetzer/Bilder/Untersetzer 91 Punkte.png', 'form', 20, 58, 25, 8),
    ('07 Sticker/Bilder/Sticker 01 Die Wortmarke.png', 'form', 58, 62, 20, -9),
]


def auslage():
    """Die leere Auslage neben dem Titel füllen (H.MATERIAL['auslage'] ist leer): Drucksachen, ein Untersetzer, ein Sticker, klein als WebP."""
    from PIL import Image
    z = os.path.join(ZIEL, '_auslage'); os.makedirs(z, exist_ok=True)
    teile = ''
    for i, (q, kl, x, y, b, r) in enumerate(AUSLAGE):
        q = q if os.path.isabs(q) else os.path.join(ZIEL, q)
        if not os.path.exists(q):
            continue
        im = Image.open(q); im = im.convert('RGBA' if kl == 'form' else 'RGB'); im.thumbnail((560, 900), Image.LANCZOS)
        n = f'a{i + 1}.webp'; im.save(os.path.join(z, n), 'WEBP', quality=82, method=6)
        teile += (f'<div class="{kl}" data-a="schweb" style="left:{x}%;top:{y}%;width:{b}%;--r:{r}deg;--r0:{r * 3}deg;--i:{i + 2}">'
                  f'<img src="_auslage/{n}" width="{im.width}" height="{im.height}" alt="" loading="eager" decoding="async"></div>')
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    s = re.sub(r'<div class="auslage" aria-hidden="true">.*?</div>(?=\s*</div>\s*</section>)', '<div class="auslage" aria-hidden="true">' + teile + '</div>', s, count=1, flags=re.S)
    open(p, 'w', encoding='utf-8').write(s)


def nur_neue_beitraege():
    """06 Instagram: nur die neuen Beiträge (die bisherigen der Bar stehen im Feed nur zum Vergleich)."""
    try:
        n = len(json.load(open(os.path.join(ROOT, 'feed', 'feed.json'), encoding='utf-8'))['posts'])
    except (OSError, KeyError, ValueError):
        return
    for f in glob.glob(os.path.join(ZIEL, '06 Instagram', 'Beiträge', 'Beitrag *.jpg')):
        m = re.search(r'Beitrag (\d+)\.jpg$', f)
        if m and int(m.group(1)) > n:
            os.remove(f)


def aufraeumen():
    """Einträge ohne Datei und leere Ordner-Abschnitte aus der Seite nehmen; Zahl der Ordner im Text nachziehen."""
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()

    def li(m):
        import html as _h
        return m.group(0) if os.path.exists(os.path.join(ZIEL, _h.unescape(m.group(1)))) else ''
    s = re.sub(r'<li data-a="auf"[^>]*><a href="([^"]+)" target="_blank" rel="noopener">.*?</li>', li, s, flags=re.S)
    s = re.sub(r'<section class="fl [^"]*blatt ordnerz" id="[^"]+">\s*<div class="in">.*?<ul class="dateien[^"]*"></ul>\s*</div>\s*</section>\n?', '', s, flags=re.S)
    n = len(re.findall(r'class="fl [^"]*blatt ordnerz"', s))
    s = re.sub(r'liegt hier sortiert in \w+ Ordnern', f'liegt hier sortiert in {K.zahl(n).lower()} Ordnern', s)
    open(p, 'w', encoding='utf-8').write(s)
    return n


def du_und_kleid():
    """Ins Du (wie die übrigen Seiten der Werkbank), Titel des Hauses, kein mailto, Schriften und Farben der Bar."""
    import du_gang as DG, kleid_wild as KW, zeile_ganz as ZG, text_mitte as TM
    p = os.path.join(ZIEL, 'index.html'); s = open(p, encoding='utf-8').read()
    for a, b in (('Alles liegt für', 'Alle Dateien'), ('Sie bereit.', 'an einem Ort.'), ('Ihre Unterlagen als Idee im Stil der neuen Seite, jede als PDF.', 'Eure Karten und die Mappe für Feiern im neuen Satz, jede als PDF.'),
                 ('Sie können jede Datei ansehen und herunterladen.', 'Ihr könnt jede Datei ansehen und herunterladen.'),
                 ('Von der Karte für die Theke bis zum Plakat für die Tür.', 'Von der Karte für die Theke bis zum SESSION-Plakat für die Tür, dazu alles aus der Plakatwerkstatt.'),
                 ('Fehlt Ihnen eine Datei oder ein Format, schreiben Sie mir gern.', 'Fehlt euch eine Datei oder ein Format, lege ich sie gern dazu.'), ('Dreissig', 'Dreißig'), ('dreissig', 'dreißig')):
        s = s.replace(a, b)
    s = DG.attribute(DG.text_teile(s, DG.umformen))
    s = re.sub(r'<a class="kn [^"]*" href="mailto:[^"]*"[^>]*>.*?</a>', '', s, flags=re.S)   # nichts verschicken: kein mailto auf der Seite
    for a, b in KW.TAUSCH:
        s = s.replace(a, b)
    s = KW._farben(s)
    open(p, 'w', encoding='utf-8').write(s)
    ZG.anwenden(ZIEL)
    TM.anwenden(ZIEL)


def baue():
    K.gestaltung()
    leeren()
    M.lege = lege
    M.baue()
    nur_neue_beitraege()
    npw = plakatwerkstatt()
    ns, nb = mehr()
    n = aufraeumen()
    auslage()
    du_und_kleid()
    dateien = sum(len([f for f in fs if not f.startswith('.')]) for dp, _, fs in os.walk(ZIEL) if '_vorschau' not in dp) - 1
    print('Material:', n, 'Ordner,', dateien, 'Dateien · Plakatwerkstatt', npw, '· Sticker', ns, '· Beigaben', nb, ('· fehlt noch: ' + ', '.join(sorted(set(FEHLT)))) if FEHLT else '')


if __name__ == '__main__':
    baue()
