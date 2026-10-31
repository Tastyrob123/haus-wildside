# Ausschnitte für die Hero-Runde 2 (31.10.2026). Aus den Originalen in voller Auflösung geschnitten, als WebP q90 in voller Breite
# und halber Breite (leicht nachgeschärft). Regel dieser Runde: kein Foto wird grösser gezeigt als halb so gross wie seine echte Auflösung.
import os, json
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
HIER = os.path.dirname(os.path.abspath(__file__))
Q = os.path.join(HIER, '..', '..', '..', '_quelle')
G7, G42, G52 = 'google-maps/google-07.jpg', 'google-maps/google-42.jpg', 'google-maps/google-52.jpg'
SCHNITTE = {   # name: (quelle, (links, oben, rechts, unten) als Bruchteil, alt)
    'decke-weit':  (G7,  (0, 0, 1, .265), 'Das Gewölbe über der Bar, quer über den ganzen Raum'),
    'decke-tief':  (G42, (0, 0, 1, .47), 'Das Gewölbe über der Theke'),
    'decke-ecke':  (G52, (0, 0, 1, .42), 'Das Gewölbe an der Ecke des Raums, darunter der Balken'),
    'vitrine':     (G42, (.25, .47, .75, .80), 'Die beleuchtete Vitrine unter dem NEGRONI-Schriftzug'),
    'theke':       (G7,  (.42, .66, 1, .86), 'Die Theke mit dem gelben Licht unter der Kante'),
    'raum':        (G7,  (0, 0, 1, 1), 'Der Raum unter dem Gewölbe: Rückbar, Theke im gelben Licht, Gäste am Tresen'),
    'derya':       ('presse/bilder/2024-01-11_np_derya-ivkin-continental-sour.jpg', (0, 0, 1, 1), 'Derya Ivkin an der Bar mit einem Continental Sour (Foto: Ilona Hottmann, Neue Presse)'),
}
out = {}
for name, (q, (l, o, r, u), alt) in SCHNITTE.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(Q, q))).convert('RGB')
    w, h = im.size
    c = im.crop((round(l * w), round(o * h), round(r * w), round(u * h)))
    cw, ch = c.size
    c.save(os.path.join(HIER, 'bild', '%s-%d.webp' % (name, cw)), 'WEBP', quality=90, method=5)
    hb = c.resize((cw // 2, ch // 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.1, percent=55, threshold=2))
    hb.save(os.path.join(HIER, 'bild', '%s-%d.webp' % (name, cw // 2)), 'WEBP', quality=88, method=5)
    out[name] = {'w': cw, 'h': ch, 'alt': alt, 'stufen': [[cw // 2, '%s-%d.webp' % (name, cw // 2)], [cw, '%s-%d.webp' % (name, cw)]]}
    if name == 'decke-weit':   # dunkle Fassung für den Lichtkegel, Abdunklung ins Bild gerechnet
        dk = ImageEnhance.Brightness(c).enhance(.22)
        dk.save(os.path.join(HIER, 'bild', 'decke-weit-dunkel-%d.webp' % cw), 'WEBP', quality=86)
        out['decke-weit']['dunkel'] = 'decke-weit-dunkel-%d.webp' % cw
json.dump(out, open(os.path.join(HIER, 'bild', 'bilder.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in out.items(): print(k, v['w'], v['h'])
