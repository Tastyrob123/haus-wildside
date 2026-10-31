#!/usr/bin/env python3
"""Werkbank Walk on the Wild Side, Seite «Unterlagen» (Werkbank Papier, 31.10.2026; Bauart wie sb_karten.py des Culinarium).
Die Karten der Bar, neu gesetzt mit der Pairing-Karte (_werkzeuge/carte, Druck über carte/drucke.js auf dem Werkzeug-Server 9083, feste Schnitte
Prata und Hanken, kein Type 3), jede neben dem Blatt, wie es heute aussieht (Beitrag der Bar vom 03.02.2026, Angebotsmappe der Bar).
Dazu das Angebot für Feiern: die zwei Angebotsblätter der Plakatwerkstatt neben den Seiten «Modell 3» und «Modell 1» der Angebotsmappe.
Das Heute-Material kommt aus _quelle/ (nur in dieser Sitzung vorhanden) und wird als PDF nach _werkbank/heute/ kopiert, damit die Seite auch ohne _quelle baut.
   python3 _werkbank/sb_karten.py            → unterlagen/pdf/<ziel>.pdf, _werkbank/heute/<ziel>.pdf, _werkbank/unterlagen.json
   PYTHONPATH=<Kit>:_werkbank python3 _werkbank/sb_karten.py --seite   → unterlagen/index.html (Kit unterlagen.py mit den Fächern aus unterlagen.json, Du-Form)"""
import json, os, re, shutil, subprocess, sys, tempfile
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
CARTE = os.path.join(PROJ, '_werkzeuge', 'carte')
PW = os.path.join(PROJ, '_werkzeuge', 'imprimerie', 'haeuser', 'wildside', 'drucksachen')
ANGEBOTE = os.path.join(PROJ, '_quelle', 'angebote-pdf', 'Wild Side Angebote.pdf')
IG = os.path.join(PROJ, '_quelle', 'ig', '2026-02-03_walkonthewildside_hannover_DUT3HDnCMo1-{}.jpg')
# Ziel, Name, Gruppe, Idee (carte-Karte oder PDFs der Plakatwerkstatt), Heute (Bilder oder Seiten der Angebotsmappe)
KARTEN = [
    ('drunk-in-love', 'Drunk in Love', 'Die Karten', ('carte', 'drunk-in-love'), ('bild', [IG.format(2)])),
    ('dishes-in-love', 'Dishes in Love', 'Die Karten', ('carte', 'dishes-in-love'), ('bild', [IG.format(3)])),
    ('preisliste', 'Die Preise der Bar', 'Die Karten', ('carte', 'preisliste'), ('seiten', [3])),
    ('angebot-feiern', 'Angebot für Feiern', 'Feiern', ('pw', ['feiern-lange-tafel.pdf', 'feiern-pauschale.pdf']), ('seiten', [4, 2])),
]


def a4(im):
    """Das heutige Blatt ganz auf eine A4-Seite hoch legen (die Seite zeigt Heute und Idee im selben Format; nichts wird angeschnitten).
    Grund in der Farbe der Bildecke, damit das Blatt wie gedruckt aussieht."""
    B, H_ = 1240, 1754
    grund = im.getpixel((2, 2))
    s = min(B / im.width, H_ / im.height)
    k = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c = Image.new('RGB', (B, H_), grund)
    c.paste(k, ((B - k.width) // 2, (H_ - k.height) // 2))
    return c


def heute_pdf(art, was, ziel):
    if art == 'bild':
        bilder = [a4(Image.open(b).convert('RGB')) for b in was]
    else:
        bilder = []
        with tempfile.TemporaryDirectory() as tmp:
            for s in was:
                subprocess.run(['pdftoppm', '-f', str(s), '-l', str(s), '-r', '110', '-png', '-singlefile', ANGEBOTE, os.path.join(tmp, str(s))], check=True)
                bilder.append(a4(Image.open(os.path.join(tmp, f'{s}.png')).convert('RGB')))
    bilder[0].save(ziel, 'PDF', resolution=150, save_all=True, append_images=bilder[1:])


def bau():
    os.makedirs(os.path.join(ROOT, 'unterlagen', 'pdf'), exist_ok=True); os.makedirs(os.path.join(W, 'heute'), exist_ok=True)
    plan = []
    for ziel, name, gruppe, (ia, iw), (ha, hw) in KARTEN:
        aus = os.path.join(ROOT, 'unterlagen', 'pdf', ziel + '.pdf')
        if ia == 'carte':
            r = subprocess.run(['node', os.path.join(CARTE, 'drucke.js'), iw, 'stand', aus], capture_output=True, text=True, timeout=240)
            if r.returncode:
                print('Pairing-Karte nicht erreichbar, bleibt:', ziel, r.stderr[-200:])
        else:
            subprocess.run(['pdfunite', *[os.path.join(PW, p) for p in iw], aus], check=True)
        h = os.path.join(W, 'heute', ziel + '.pdf')
        if os.path.exists(ANGEBOTE):
            heute_pdf(ha, hw, h)
        if not (os.path.exists(aus) and os.path.exists(h)):
            print('fehlt', ziel); continue
        plan.append(dict(ziel=ziel, quelle=os.path.relpath(h, ROOT), name=name, gruppe=gruppe, seiten=0, b=210, h=297, dazu='', fehlt=''))
    json.dump(plan, open(os.path.join(W, 'unterlagen.json'), 'w'), ensure_ascii=False, indent=1)
    print('Unterlagen:', ', '.join(p['ziel'] for p in plan))


DU = [('Ihre Unterlagen,', 'Eure Unterlagen,'),
      ('Wählen Sie eine Unterlage und blättern Sie mit den Pfeilen. Links steht Ihre heutige Fassung, rechts die Idee im Stil der neuen Seite.',
       'Wählt eine Unterlage und blättert mit den Pfeilen. Links steht das Blatt, wie es heute aussieht, rechts die Idee im Stil der neuen Seite.'),
      ('keine offiziellen Unterlagen des Hauses', 'keine offiziellen Unterlagen der Bar')]


def seite():
    import kern as K
    import unterlagen as U
    plan = json.load(open(os.path.join(W, 'unterlagen.json'), encoding='utf-8'))
    K.H.FAECHER = [(p['ziel'], p['name']) for p in plan][:4]
    U.baue()
    p = os.path.join(ROOT, 'unterlagen', 'index.html')
    t = open(p, encoding='utf-8').read()
    for a, b in DU:
        t = t.replace(a, b)
    t = t.replace(' loading="lazy"', '')
    open(p, 'w', encoding='utf-8').write(t)
    # Vorschaubild für das Kapitel Papier der Werkbank
    q = os.path.join(ROOT, 'unterlagen', 'img', f'n-{plan[0]["ziel"]}-01.webp')
    im = Image.open(q); im.thumbnail((1200, 1200)); im.save(os.path.join(ROOT, 'unterlagen', 'img', 'vorschau.webp'), 'WEBP', quality=86)
    # alte Seitenbilder, die zu keiner Unterlage mehr gehören
    ids = {x['ziel'] for x in plan}
    for f in os.listdir(os.path.join(ROOT, 'unterlagen', 'img')):
        m = re.match(r'[nh]-(.+)-\d\d\.webp$', f)
        if m and m.group(1) not in ids:
            os.remove(os.path.join(ROOT, 'unterlagen', 'img', f))
    for f in os.listdir(os.path.join(ROOT, 'unterlagen', 'pdf')):
        if f[:-4] not in ids:
            os.remove(os.path.join(ROOT, 'unterlagen', 'pdf', f))


if __name__ == '__main__':
    seite() if '--seite' in sys.argv else bau()
