#!/usr/bin/env python3
"""Walk on the Wild Side: fünf Beigaben als Druckvorlage (Werkbank Papier, 31.10.2026; Bauart wie beigaben.py des Culinarium).
Streichholzbriefchen, Drink-Fähnchen zu Momos drei Techniken, ein Kärtchen «Was magst du?» zum Ankreuzen (Momos drei Fragen von der Seite «Drinks»),
Cocktailservietten und eine Banderole fürs Windlicht auf dem Tisch. Kleid und Texte wie die Drucksachen (papier_neu.py), Seite beigaben/.
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/beigaben.py "<website/_werkbank>"          →  satz/beigabe-*.html, beigaben_plan.json
   node _werkbank/sticker_druck.js "<…>" beigaben, dann  python3 _werkbank/beigaben.py "<…>" --seite"""
import json, os, re, sys
import papier_kern as P
from papier_kern import t, lin, linv, rahmen, kasten, blatt, hw, e
import kern as K
from kern import H, ROOT, W, kn, titel, kap, zahl
import papier_neu as N
from papier_neu import NACHT, CREME, CREME3, GOLD, GOLDT, ROT, TINTE, LEISE, TAPETE


def etk(x, y, text, farbe, gr=1.8, b=None, mehr=''):
    return t(x, y, e(text.upper()), 'm' + (' c' if b else ''), f'font-size:{gr}mm;letter-spacing:.2em;font-weight:500;color:{farbe};{mehr}', b)


def falz(x, y, b, waag=True, farbe='rgba(216,178,100,.7)'):
    if waag:
        return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:0;border-top:.25mm dashed {farbe}"></i>'
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:0;height:{b}mm;border-left:.25mm dashed {farbe}"></i>'


def feld(x, y, b, h, farbe, r=1.4, d=.25):
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{b}mm;height:{h}mm;border:{d}mm solid {farbe};border-radius:{r}mm"></i>'


def kreis_feld(x, y, d=2.6, farbe=TINTE):
    return f'<i class="abs" style="left:{x}mm;top:{y}mm;width:{d}mm;height:{d}mm;border:.3mm solid {farbe};border-radius:50%"></i>'


# ------------------------------------------------------------------ die fünf
def streichholz():
    """flach 50 × 110: oben die Rückseite, Reibefläche, unten die Vorderseite mit der Wortmarke (gefalzt 50 × 40)"""
    inn = (kasten(0, 0, 50, 46, f'background:{CREME}')
           + t(0, 10, 'Bis 2\xa0Uhr.', 's c', f'font-size:5.6mm;color:{TINTE}', 50)
           + etk(0, 21, 'Do 19 – 1 · Fr und Sa 19 – 2', GOLDT, 1.35, 50, 'letter-spacing:.12em')
           + etk(0, 30, N.ADRESSE, LEISE, 1.35, 50, 'letter-spacing:.1em') + etk(0, 34, 'Linden', LEISE, 1.35, 50)
           + kasten(0, 46, 50, 10, 'background:#3a2a20;background-image:radial-gradient(rgba(0,0,0,.35) .25mm,transparent .3mm);background-size:.9mm .9mm')
           + kasten(0, 56, 50, 54, f'background:{NACHT} {TAPETE}') + feld(3, 59, 44, 48, GOLD, 1.6)
           + hw(25, 66, 18, ROT)
           + falz(0, 46, 50) + falz(0, 56, 50))
    return [blatt(50, 110, inn, '', f'background:{NACHT}')]


def faehnchen():
    """drei Fähnchen je 60 × 20 mm, in der Mitte am Stäbchen gefalzt: vorn und hinten gleich"""
    inn = ''
    for i, (name, _s) in enumerate(N.TECHNIK):
        y = 6 + i * 26
        inn += kasten(5, y, 60, 20, f'background:{NACHT};border-radius:.6mm')
        for x in (5, 35):
            inn += (etk(x, y + 4, 'Momo', GOLD, 1.3, 30) + t(x, y + 8.2, e(name), 's c', f'font-size:{4 if len(name) < 10 else 3.6}mm;color:{CREME}', 30))
        inn += falz(35, y, 20, False)
    return [blatt(70, 82, inn, '', 'background:transparent')]


def wahlkarte():
    """A6 quer: Momos drei Fragen zum Ankreuzen, für die Theke oder den Tisch"""
    spalten = [('Der Geschmack', ['sauer', 'süss', 'bitter', 'rauchig']), ('Das Glas', ['klar', 'cremig', 'spritzig']),
               ('Was hinein soll', ['Gin', 'Rum', 'Mezcal', 'Whisky', 'ohne Alkohol'])]
    for (n, w), (n2, s) in zip(spalten, N.WAHL):
        assert n == n2 and all(x.lower() in s.lower() for x in w), n
    inn = (hw(14, 11, 9, ROT, False)
           + etk(28, 13, 'An der Theke', GOLDT, 1.7)
           + t(28, 17.5, 'Was magst\xa0du?', 's', f'font-size:7.4mm;color:{TINTE}')
           + lin(14, 33, 120, GOLD, .25))
    for i, (n, worte) in enumerate(spalten):
        x = 14 + i * 42
        inn += etk(x, 39, n, GOLDT, 1.6)
        for k, w in enumerate(worte):
            inn += kreis_feld(x, 46 + k * 7.4) + t(x + 4.6, 45.4 + k * 7.4, e(w), '', f'font-size:3.1mm;color:{TINTE}')
    inn += (lin(14, 86, 120, GOLD, .25)
            + t(14, 90, e(N.MOMO), '', f'font-size:2.7mm;line-height:1.4;color:{TINTE}', 96)
            + etk(14, 96.5, 'Momo Ben Khelifa', LEISE, 1.4)
            + f'<i class="abs" style="left:131mm;top:92mm;width:2.4mm;height:2.4mm;border-radius:50%;background:{ROT}"></i>')
    return [blatt(148, 105, inn, '', f'background:{CREME}')]


def serviette():
    """Cocktailserviette 125 × 125 mm (gefaltet 62,5 mm): Creme mit roter Wortmarke, Nacht mit Goldrahmen"""
    a = (falz(0, 62.5, 125, True, 'rgba(27,21,18,.18)') + falz(62.5, 0, 125, False, 'rgba(27,21,18,.18)')
         + feld(66, 66, 55, 55, GOLDT) + hw(93.75, 75, 15, ROT) + etk(62.5, 113, 'Linden', GOLDT, 1.4, 62.5))
    b = (kasten(0, 0, 125, 125, f'background:{NACHT} {TAPETE}')
         + falz(0, 62.5, 125, True, 'rgba(216,178,100,.25)') + falz(62.5, 0, 125, False, 'rgba(216,178,100,.25)')
         + feld(66, 66, 55, 55, GOLD) + t(66, 82, 'Du sagst,<br>was du\xa0magst.', 's c', f'font-size:5mm;line-height:1.2;color:{CREME}', 55)
         + f'<i class="abs" style="left:92.75mm;top:101mm;width:2mm;height:2mm;border-radius:50%;background:{ROT}"></i>')
    return [blatt(125, 125, a, '', f'background:{CREME}'), blatt(125, 125, b, '', f'background:{NACHT}')]


def windlicht():
    """Banderole fürs Windlicht, 210 × 50 mm, um das Glas gelegt"""
    inn = (kasten(0, 0, 210, 50, f'background:{NACHT} {TAPETE}')
           + lin(0, 5, 210, GOLD, .3) + lin(0, 44.7, 210, GOLD, .3)
           + hw(22, 12.5, 18, ROT) + hw(188, 12.5, 18, ROT)
           + etk(0, 14, 'Donnerstag bis Samstag ab 19 Uhr', GOLD, 1.7, 210)
           + t(0, 20, 'Unter dieser Decke.', 's c', f'font-size:7.6mm;color:{CREME}', 210)
           + etk(0, 34, N.ADRESSE + ' · Linden', CREME3, 1.6, 210, 'letter-spacing:.14em'))
    return [blatt(210, 50, inn, '', f'background:{NACHT}')]


BEIGABEN = [
    ('streichholz', 'Streichholzbriefchen', 'Briefchen 50 × 110 mm (gefalzt 50 × 40)', streichholz, [('streichholz', 1)], [('streichholz', 30, '')],
     ['Streichhölzer', 'für die Kerzen.'], 'Für die Kerzen auf den Tischen und zum Mitnehmen nach dem letzten Drink. Außen die Wortmarke im Goldrahmen, innen die Zeiten und die Ecke.'),
    ('faehnchen', 'Drink-Fähnchen', 'Fähnchen 60 × 20 mm, in der Mitte am Stäbchen gefalzt', faehnchen, [('faehnchen', 1)], [('faehnchen', 66, '')],
     ['Ein Fähnchen', 'am Glas.'], 'Am Stäbchen im Glas: welche von Momos drei Techniken in diesem Drink steckt. Milk Washing, Fat Washing, Enzyme.'),
    ('wahlkarte', 'Was magst du?', 'A6 quer, 148 × 105 mm', wahlkarte, [('wahlkarte', 1)], [('wahlkarte', 84, '')],
     ['Was', 'magst du?'], 'Momos drei Fragen zum Ankreuzen: der Geschmack, das Glas, was hinein soll. Für volle Abende, wenn die Theke dicht ist, und für alle, die erst überlegen wollen.'),
    ('serviette', 'Cocktailservietten', 'Serviette 125 × 125 mm, gefaltet 62,5 mm', serviette, [('serviette', 1), ('serviette-n', 2)], [('serviette', 46, 'Creme'), ('serviette-n', 46, 'Nacht')],
     ['Eine Serviette', 'unter dem Glas.'], 'Zwei Fassungen: Creme mit der roten Wortmarke, die Nacht der Bar mit Goldrahmen und Momos Satz. Gefaltet liegt das Motiv oben.'),
    ('windlicht', 'Banderole fürs Windlicht', 'Banderole 210 × 50 mm', windlicht, [('windlicht', 1)], [('windlicht', 92, '')],
     ['Ein Band', 'ums Windlicht.'], 'Um das Glas mit der Kerze gelegt, auf jedem Tisch unter dem Gewölbe: die Wortmarke links und rechts, dazwischen der Titel der Seite «Das Haus».'),
]


def setzen():
    plan = []
    for ident, name, fmt, fn, vorschau, karton, tit, satz in BEIGABEN:
        bl = fn()
        P.seite('beigabe-' + ident, bl, name)
        plan.append(dict(id=ident, name=name, format=fmt, vorschau=vorschau, satz=satz, seiten=len(bl), karton=karton, titel=tit))
    json.dump({'druck': plan}, open(os.path.join(W, 'beigaben_plan.json'), 'w'), ensure_ascii=False, indent=1)
    ids = {'beigabe-' + b[0] + '.html' for b in BEIGABEN}
    for f in os.listdir(P.SATZ):
        if f.startswith('beigabe-') and f not in ids:
            os.remove(os.path.join(P.SATZ, f))
    print('Beigaben gesetzt:', len(plan))


def seite():
    from PIL import Image
    K.gestaltung()
    plan = json.load(open(os.path.join(W, 'beigaben_plan.json')))
    roh, ziel = os.path.join(W, 'roh', 'beigaben'), os.path.join(ROOT, 'beigaben', 'img')
    os.makedirs(ziel, exist_ok=True)
    for f in os.listdir(ziel):
        os.remove(os.path.join(ziel, f))
    M = {}
    for d in plan['druck']:
        for name, _ in d['vorschau']:
            im = Image.open(os.path.join(roh, name + '.png')).convert('RGBA')
            if im.width > 1000:
                im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
            im.save(os.path.join(ziel, name + '.webp'), 'WEBP', quality=88, method=5); M[name] = im.size
    FL = ['fl--papier', 'fl--nacht tapete-leicht', 'fl--creme', 'fl--papier', 'fl--creme']
    haupt = f'''<section class="sk">
  <div class="in">
    <div>
      {kap(K.nr('papier'), 'Ideen für Papier')}
      {titel([zahl(len(plan['druck'])) + ' Beigaben', 'für den Abend.'], 'h1', 't1')}
      <div class="lauf"><p data-a="worte" style="--vz:700ms">Kleine Dinge, die ein Gast an der Theke findet oder nach dem Abend mitnimmt. Alle im Stil der neuen Seite, jede als Druckvorlage. Was nicht passt, lasst ihr einfach weg.</p></div>
      <div class="kn-reihe" data-a="auf" style="--i:8">{kn('Zur Werkbank', '../werkbank/index.html#papier')}{kn('Drucksachen', '../drucksachen/index.html', 'kn--linie')}</div>
    </div>
  </div>
</section>
'''
    for i, d in enumerate(plan['druck']):
        figs = ''.join(f'<figure class="sch" data-a="schweb" style="width:{w}%;--i:{k % 4}"><img src="img/{nm}.webp" width="{M[nm][0]}" height="{M[nm][1]}" alt="{e(d["name"])}" decoding="async">'
                       f'{f"<figcaption>{e(u)}</figcaption>" if u else ""}</figure>' for k, (nm, w, u) in enumerate(d['karton']))
        haupt += f'''<section class="fl {FL[i % len(FL)]} blatt stueck{" stueck--r" if i % 2 else ""}" id="{d['id']}">
  <div class="in">
    <div class="stueck__t">
      {kap(i + 1, e(d['name']))}
      {titel(d['titel'])}
      <div class="lauf"><p data-a="worte">{e(d['satz'])}</p></div>
      <p class="stueck__f" data-a="auf">{e(d['format'])}</p>
      <div class="kn-reihe" data-a="auf">{kn('Als PDF ansehen', f"pdf/{H.KURZ}-{d['id']}.pdf", neu=True)}</div>
    </div>
    <div class="karton">{figs}</div>
  </div>
</section>
'''
    haupt += f'''<section class="ausklang"><div class="in"><p data-a="auf">Dazu gibt es Drucksachen, Untersetzer, Sticker und Postkarten im selben Stil.</p><div class="kn-reihe" data-a="auf">{kn('Drucksachen', '../drucksachen/index.html')}{kn('Sticker', '../sticker/index.html', 'kn--linie')}{kn('Postkarten', '../postkarten/index.html', 'kn--linie')}</div></div></section>'''
    K.schreib(os.path.join(ROOT, 'beigaben', 'index.html'), K.rahmen('Beigaben', f'{zahl(len(plan["druck"]))} Beigaben für die Abende des {H.NAME}.', 'Beigaben', haupt))
    Image.open(os.path.join(ziel, 'wahlkarte.webp')).save(os.path.join(ziel, 'vorschau.webp'), 'WEBP', quality=86)
    ids = {d['id'] for d in plan['druck']}
    pd = os.path.join(ROOT, 'beigaben', 'pdf')
    for f in os.listdir(pd):
        if not any(f == f'{H.KURZ}-{i}.pdf' for i in ids):
            os.remove(os.path.join(pd, f))
    print('Seite gebaut: beigaben/ ·', len(plan['druck']), 'Beigaben')


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else setzen()
