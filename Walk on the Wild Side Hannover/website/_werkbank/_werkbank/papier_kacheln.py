#!/usr/bin/env python3
"""Werkbank Papier (1.11.2026): Bilder der Papier-Kacheln auf der Startseite der Werkbank sofort nachziehen, ohne den ganzen Bau des Kits.
Macht, was Kit bau.py für H.PAPIER['orte_d'] und ['orte_e'] tut (b-<drucksache>.webp 377 px, k-<untersetzer>.webp 340 px aus _werkbank/roh/papier),
und stellt in werkbank/index.html die Nachbauten der Plakate (b-pw-…) auf die eigenen Formate um. Der nächste Gesamtbau macht dasselbe aus haus.py.
   python3 _werkbank/papier_kacheln.py"""
import json, os, re
from PIL import Image

W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PR = os.path.join(W, 'roh', 'papier')
IMG = os.path.join(ROOT, 'werkbank', 'img')
TAUSCH = {'pw-session-aushang-a3': 'aufsteller', 'pw-tanz-in-den-mai': 'visitenkarte'}


def webp(quelle, name, breite, q=84):
    im = Image.open(quelle).convert('RGBA')
    im = im.resize((breite, round(im.height * breite / im.width)), Image.LANCZOS)
    im.save(os.path.join(IMG, name + '.webp'), 'WEBP', quality=q, method=5)
    return im.size


def main():
    masse = {}
    for n in ('karte', 'aufsteller', 'visitenkarte'):
        masse['b-' + n] = webp(os.path.join(PR, n + '.png'), 'b-' + n, 377)
    for x in json.load(open(os.path.join(W, 'papier_plan.json')))['etiketten'][:6]:
        masse['k-' + x['id']] = webp(os.path.join(PR, x['id'] + '.png'), 'k-' + x['id'], 340)
    # Kapitel Karten: die zwei Blätter im Fächer (Kit bau.py › H.FAECHER, img/pdf-<i>.webp) aus den neuen PDFs der Pairing-Karte
    import subprocess, tempfile
    for i, ziel in enumerate(('drunk-in-love', 'preisliste')):
        q = os.path.join(ROOT, 'unterlagen', 'pdf', ziel + '.pdf')
        alt = os.path.join(IMG, f'pdf-{i}.webp')
        if os.path.exists(q) and os.path.exists(alt):
            breite = Image.open(alt).width
            with tempfile.TemporaryDirectory() as tmp:
                subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', '110', '-png', '-singlefile', q, os.path.join(tmp, 'p')], check=True)
                masse[f'pdf-{i}'] = webp(os.path.join(tmp, 'p.png'), f'pdf-{i}', breite, 86)
    p = os.path.join(ROOT, 'werkbank', 'index.html')
    t = open(p, encoding='utf-8').read()
    for alt, neu in TAUSCH.items():
        t = t.replace(f'img/b-{alt}.webp', f'img/b-{neu}.webp')
        f = os.path.join(IMG, f'b-{alt}.webp')
        if os.path.exists(f):
            os.remove(f)
    for name, (b, h) in masse.items():
        t = re.sub(rf'(<img src="img/{name}\.webp" width=")\d+(" height=")\d+', rf'\g<1>{b}\g<2>{h}', t)
    open(p, 'w', encoding='utf-8').write(t)
    print('Kacheln:', ', '.join(masse))


if __name__ == '__main__':
    main()
