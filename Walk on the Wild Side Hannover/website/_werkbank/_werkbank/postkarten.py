#!/usr/bin/env python3
"""Walk on the Wild Side: zwölf Postkarten (Werkbank Papier, 31.10.2026; Bauart wie postkarten.py des Culinarium).
Acht Karten von den SESSION-Plakaten der DJ-Abende (website/bau.py › LINEUP, Plakate als Bilder der Website p-<datum>), dazu vier Karten mit den
stärksten Bildern der Bar (CHARAKTER.md 5): das Gewölbe, NEGRONI über der Vitrine, das Eckschild bei Nacht, Momo gießt ein.
Vorn A6 hoch: das Plakat ganz, nie angeschnitten, auf der Nacht der Bar, bzw. das Foto randlos im Goldrahmen mit der Wortmarke.
Hinten A6 quer auf Creme: links Abend oder Satz, rechts Platz zum Schreiben mit Adresslinien und ein Markenfeld mit der Wortmarke.
Druck-PDF mit 3 mm Beschnitt, Sammelbogen SRA3, Fächer und Kartenständer als Bild (postkarten_druck.js).
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/postkarten.py "<website/_werkbank>"            → satz/postkarten*.html, postkarten_plan.json
   node _werkbank/postkarten_druck.js "<…>"   dann   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/postkarten.py "<…>" --seite"""
import json, os, re, shutil, sys
from PIL import Image
import papier_kern as P
from papier_kern import blatt, e, t, hw
import kern as K
from kern import H, ROOT, W, kn, titel, kap, zahl
import papier_neu as N
from papier_neu import NACHT, CREME, CREME3, GOLD, GOLDT, ROT, PROT, TINTE, LEISE

B = 3   # Beschnitt
_BAU = open(os.path.join(N.WEB, 'bau.py'), encoding='utf-8').read()
LINEUP = re.findall(r"\('(\d\d\.\d\d\.\d{4})', '([^']+)', '([^']*)', '(p-\d+)'\)", _BAU)
FOTOS = [('decke-2017', 'Ein Gewölbe über der Theke.', 'Und irgendwann schaust du nach oben.', '50% 50%'),
         ('negroni', 'Und wer einen Negroni will.', 'Den Negroni gibt es an jedem Abend.', '50% 40%'),
         ('schild', 'An der Ecke.', 'Haasemannstraße 13, Ecke Rampenstraße.', '40% 40%'),
         ('momo-giesst', 'Du sagst, was du magst.', N.MOMO, '50% 35%')]


def karten():
    K_, gesehen = [], set()
    for datum, name, art, key in LINEUP:
        if key in gesehen:
            continue
        gesehen.add(key)
        d = json.load(open(os.path.join(N.BILD, key + '.json')))
        K_.append(dict(id=f'pk{len(K_) + 1:02d}', key=key, art='plakat', name=name, abend=f'SESSION · {datum}', satz=art, ia=d['w'] / d['h'], lage='50% 50%'))
    for key, name, satz, lage in FOTOS:
        K_.append(dict(id=f'pk{len(K_) + 1:02d}', key=key, art='foto', name=name, abend='Walk on the Wild Side', satz=satz, ia=1, lage=lage))
    return K_


def et(text, gr, farbe, sp=.18):
    return f'<span style="font-family:\'Hanken Grotesk\';font-weight:500;font-size:{gr}mm;letter-spacing:{sp}em;text-transform:uppercase;color:{farbe};line-height:1.4">{e(text)}</span>'


def vorn(k, rand=0):
    """A6 hoch, 105 × 148; rand = Beschnitt ringsum (Druck)."""
    b, h = 105 + 2 * rand, 148 + 2 * rand
    if k['art'] == 'plakat':
        pw = 105 - 2 * 10
        ph = pw / k['ia']
        if ph > 148 - 34: ph = 148 - 34; pw = ph * k['ia']
        x, y = rand + (105 - pw) / 2, rand + (148 - ph) / 2 - 6
        inn = (f'<i class="abs" style="inset:0;background:{NACHT}"></i>'
               f'<img class="abs" src="{e(N.bild_satz(k["key"]))}" style="left:{x}mm;top:{y}mm;width:{pw}mm;height:{ph}mm;object-fit:contain;box-shadow:0 .6mm 2.4mm rgba(0,0,0,.45)" alt="">'
               f'<div class="abs" style="left:{rand}mm;top:{y + ph + 6}mm;width:105mm;text-align:center">{et(k["name"] + " · " + k["abend"].split(" · ")[1], 1.8, CREME3, .14)}</div>')
        return blatt(b, h, inn, '', f'background:{NACHT}')
    inn = (f'<img class="abs" src="{e(N.bild_satz(k["key"]))}" style="inset:0;width:{b}mm;height:{h}mm;object-fit:cover;object-position:{k["lage"]}" alt="">'
           f'<i class="abs" style="left:{rand + 5}mm;top:{rand + 5}mm;width:95mm;height:138mm;border:.3mm solid {GOLD};border-radius:2mm"></i>'
           + hw(rand + 52.5, rand + 124, 11, ROT))
    return blatt(b, h, inn, '', f'background:{NACHT}')


def hinten(k, rand=0):
    """A6 quer, 148 × 105: links Abend oder Satz, rechts Adresse und Markenfeld mit der Wortmarke."""
    b, h = 148 + 2 * rand, 105 + 2 * rand
    r = rand
    linie = PROT if k['art'] == 'plakat' else GOLD
    oben = 'Plakat · DJ-Abend' if k['art'] == 'plakat' else 'Walk on the Wild Side'
    unten = k['abend'] if k['art'] == 'plakat' else ''
    satz = (k['satz'][:1].upper() + k['satz'][1:]) if k['satz'] else ''
    links = (f'<div class="abs" style="left:{r + 10}mm;top:{r + 12}mm;width:54mm;bottom:{r + 12}mm;display:flex;flex-direction:column;justify-content:space-between">'
             f'<div>{et(oben, 1.8, GOLDT, .16)}<div style="height:3mm"></div>'
             f'<div style="font-family:Prata;font-size:6.2mm;line-height:1.14;color:{TINTE}">{e(k["name"])}</div><div style="height:2.6mm"></div>'
             f'<i style="display:block;width:8mm;height:.35mm;background:{linie}"></i><div style="height:2.6mm"></div>'
             + (f'<div style="font-family:\'Hanken Grotesk\';font-size:3mm;line-height:1.45;color:{TINTE}">{e(unten)}</div>' if unten else '')
             + (f'<div style="font-family:\'Hanken Grotesk\';font-size:2.8mm;line-height:1.45;color:{LEISE}">{e(satz)}</div>' if satz else '')
             + f'</div><div>{et(N.ADRESSE + " · Linden", 1.5, GOLDT, .08)}<div style="height:1mm"></div>{et(N.IG, 1.5, GOLDT, .06)}</div></div>')
    trenn = f'<i class="abs" style="left:{r + 72}mm;top:{r + 12}mm;width:.25mm;height:81mm;background:{GOLD}"></i>'
    marke = (f'<div class="abs" style="left:{r + 148 - 10 - 20}mm;top:{r + 10}mm;width:20mm;height:24mm;border:.3mm dashed rgba(27,21,18,.4);border-radius:.8mm"></div>'
             + hw(r + 148 - 20, r + 14.5, 10.5, ROT))
    linien = ''.join(f'<i class="abs" style="left:{r + 80}mm;top:{r + 50 + n * 11}mm;width:58mm;height:.25mm;background:rgba(27,21,18,.34)"></i>' for n in range(4))
    return blatt(b, h, f'<i class="abs" style="inset:0;background:{CREME}"></i>' + links + trenn + marke + linien, '', f'background:{CREME}')


def setzen():
    KK = karten()
    os.makedirs(os.path.join(P.SATZ, 'bild'), exist_ok=True)
    Image.open(N.bild('decke-raum')).convert('RGB').save(os.path.join(P.SATZ, 'bild', 'barnacht.webp'), 'WEBP', quality=80)   # Hintergrund für den Kartenständer
    vor = [vorn(k) for k in KK]; hin = [hinten(k) for k in KK]
    P.seite('postkarten', [x for p in zip(vor, hin) for x in p], 'Postkarten')
    P.seite('postkarten-druck', [x for k in KK for x in (vorn(k, B), hinten(k, B))], 'Postkarten, Druck mit Beschnitt')
    BW, BH, LUFT = 450, 320, 3
    boegen = []
    for s0 in range(0, len(KK), 8):
        teil = KK[s0:s0 + 8]; inn = ''
        x0, y0 = (BW - (4 * 105 + 3 * LUFT)) / 2, (BH - (2 * 148 + LUFT)) / 2
        for n, k in enumerate(teil):
            x, y = x0 + (n % 4) * (105 + LUFT), y0 + (n // 4) * (148 + LUFT)
            inn += f'<div class="abs" style="left:{x}mm;top:{y}mm;width:105mm;height:148mm;overflow:hidden">{vorn(k).replace('style="width:', 'style="margin:0;width:', 1)}</div>'
            inn += f'<i class="abs" style="left:{x}mm;top:{y}mm;width:105mm;height:148mm;outline:.15mm solid #e6007e"></i>'
        inn += t(14, 4, f'{e(H.NAME)} · Postkarten · Sammelbogen {s0 // 8 + 1} von {(len(KK) + 7) // 8} · SRA3 quer · Originalgröße · Schnittlinie in Magenta', 'm', 'font-size:2.1mm;color:#1b1512')
        boegen.append(blatt(BW, BH, inn, '', 'background:#fff'))
    P.seite('postkarten-bogen', boegen, 'Postkarten, Sammelbogen')
    json.dump({'karten': [{k2: k[k2] for k2 in ('id', 'key', 'name', 'abend', 'art')} for k in KK], 'boegen': len(boegen)},
              open(os.path.join(W, 'postkarten_plan.json'), 'w'), ensure_ascii=False, indent=1)
    print('Postkarten gesetzt:', len(KK), 'Karten,', len(boegen), 'Sammelbögen')


def seite():
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'postkarten_plan.json')))
    KK = plan['karten']
    roh, ziel = os.path.join(W, 'roh', 'postkarten'), os.path.join(ROOT, 'postkarten', 'img')
    if os.path.isdir(ziel):
        shutil.rmtree(ziel)
    os.makedirs(ziel)
    M = {}
    for f in os.listdir(roh):
        if not f.endswith('.png'): continue
        im = Image.open(os.path.join(roh, f)).convert('RGBA')
        if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(os.path.join(ziel, f[:-4] + '.webp'), 'WEBP', quality=88, method=5); M[f[:-4]] = im.size
    img = lambda n, alt='': f'<img src="img/{n}.webp" width="{M[n][0]}" height="{M[n][1]}" alt="{e(alt)}" decoding="async">'
    unter = lambda k: k['abend'] if k['art'] == 'plakat' else 'Foto der Bar'
    liste = ''.join(f'<li data-a="kipp" style="--i:{n % 4}"><span class="b pk-paar">{img(k["id"] + "-v", k["name"])}{img(k["id"] + "-h", "Rückseite")}</span><h3>{e(k["name"])}</h3><p>{e(unter(k))}</p><small>A6 · vorn hoch, hinten quer</small></li>' for n, k in enumerate(KK))
    np_ = sum(1 for k in KK if k['art'] == 'plakat')
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(KK)), 'Postkarten', 'für die Theke.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">{zahl(np_)} Karten von den SESSION-Plakaten eurer DJ-Abende, jedes Plakat ganz, dazu vier mit den Bildern der Bar: das Gewölbe, NEGRONI, das Schild an der Ecke und Momo. Hinten Platz zum Schreiben und die Wortmarke im Markenfeld. Zum Auslegen an der Bar und zum Mitnehmen.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Druck-PDF', f'pdf/{H.KURZ}-postkarten-druck.pdf', 'kn--linie', neu=True)}</div>
    </div>
    <div class="auslage" aria-hidden="true"><div data-a="schweb" style="left:0;top:0;width:100%;--r:0deg;--r0:0deg;--i:2">{img("faecher", "")}</div></div>
  </div>
</section>
<section class="fl fl--nacht tapete-leicht blatt stueck" id="staender">
  <div class="in">
    <div class="stueck__t">{kap(1, 'An der Bar')}{titel(['Im Ständer', 'an der Theke.'])}<div class="lauf"><p data-a="worte">So könnten die Karten an der Bar stehen: nach jedem DJ-Abend eine neue, zum Mitnehmen nach dem letzten Drink.</p></div></div>
    <div class="karton"><figure class="sch" data-a="schweb" style="width:96%">{img("staender", "Kartenständer an der Bar")}</figure></div>
  </div>
</section>
<section class="fl fl--papier blatt" id="karten">
  <div class="in">
    <div class="kopfzeile"><div>{kap(2, 'Die Karten')}{titel([zahl(len(KK)), 'Postkarten.'])}</div><div class="lauf"><p data-a="worte">Jedes Plakat ganz, nie angeschnitten, auf der Nacht der Bar. Die Fotos randlos im Goldrahmen des Eckschilds.</p></div></div>
    <ul class="etk">{liste}</ul>
  </div>
</section>
<section class="fl fl--creme blatt stueck" id="druck">
  <div class="in">
    <div class="stueck__t">{kap(3, 'Für die Druckerei')}{titel(['Der', 'Sammelbogen.'])}
      <div class="lauf"><p data-a="worte">Alle Karten mit 3 mm Beschnitt als ein PDF, dazu {zahl(plan["boegen"]).lower()} Sammelbögen SRA3 mit Schnittlinien.</p></div>
      <div class="kn-reihe" data-a="auf">{kn('Druck-PDF', f'pdf/{H.KURZ}-postkarten-druck.pdf', neu=True)}{kn('Sammelbogen SRA3', f'pdf/{H.KURZ}-postkarten-sammelbogen-a3.pdf', 'kn--linie', neu=True)}</div></div>
    <div class="bogenblick" data-a="gross">{img("bogen", "Sammelbogen SRA3")}</div>
  </div>
</section>
<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Sticker und Beigaben im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}{kn('Beigaben', '../beigaben/index.html', 'kn--linie')}</div></div></section>'''
    css = '<style>.etk .b.pk-paar{display:flex!important;flex-direction:row!important;gap:4%;align-items:center;justify-content:center;height:auto!important;aspect-ratio:auto!important}.etk .b.pk-paar img{position:static!important;width:40%!important;height:auto!important;max-height:none!important}.etk .b.pk-paar img+img{width:56%!important}</style>'
    K.schreib(os.path.join(ROOT, 'postkarten', 'index.html'), K.rahmen('Postkarten', f'{zahl(len(KK))} Postkarten des {H.NAME}.', 'Postkarten', css + haupt))
    Image.open(os.path.join(ziel, 'faecher.webp')).save(os.path.join(ziel, 'vorschau.webp'), 'WEBP', quality=86)
    print('Seite gebaut: postkarten/ ·', len(KK), 'Karten')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else setzen()
