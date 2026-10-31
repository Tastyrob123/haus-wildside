# Nach dem KI-Nachschärfen: Farben je Kanal an das Original angleichen (Mittelwert und Streuung), bei der Hausecke die Schrift der Schilder
# aus dem Original zurücksetzen (die KI hatte die kleine Zeile über «WILD SIDE» verändert). Schreibt bild/NR-name-gross.webp und -halb.webp.
import sys, os
import numpy as np
from PIL import Image, ImageFilter
FQ = '/private/tmp/claude-501/-Users-robertreff--claude-spares-spare-Wxdrje/0e567ef6-60f6-4ea3-941c-7f385d155a06/scratchpad/fq/'
NAMEN = {'01':'negroni-rueckbar','02':'raum-kerze','03':'vitrine','04':'creme-brulee','05':'zapfhaehne','06':'karte-kerze','07':'sour','08':'zitronen-blueten',
         '09':'verstaerker','10':'tresen-glaeser','11':'hausecke','12':'negroni-glas','13':'raum-leer','14':'lange-tafel','15':'gedeckte-wand'}
for nr in (sys.argv[1:] or sorted(NAMEN)):
    n = NAMEN[nr]; ki = os.path.join('ki', nr + '.png')
    if not os.path.exists(ki): continue
    k = Image.open(ki).convert('RGB'); o = Image.open(FQ + '%s-%s.jpg' % (nr, n)).convert('RGB').resize(k.size, Image.LANCZOS)
    a = np.asarray(k).astype(np.float32); b = np.asarray(o).astype(np.float32)
    for c in range(3):
        a[..., c] = (a[..., c] - a[..., c].mean()) / (a[..., c].std() + 1e-6) * b[..., c].std() + b[..., c].mean()
    k = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    if nr == '11':
        w, h = k.size; box = (round(.30 * w), round(.32 * h), round(.48 * w), round(.53 * h))
        m = Image.new('L', k.size, 0); m.paste(255, box); m = m.filter(ImageFilter.GaussianBlur(12))
        k = Image.composite(o, k, m)
    w, h = k.size
    for f in os.listdir('bild'):
        if f.startswith(nr + '-'): os.remove(os.path.join('bild', f))
    k.save('bild/%s-%s-gross.webp' % (nr, n), 'WEBP', quality=86, method=5)
    k.resize((w // 2, h // 2), Image.LANCZOS).save('bild/%s-%s-halb.webp' % (nr, n), 'WEBP', quality=84, method=5)
    print(nr, n, w, h)
