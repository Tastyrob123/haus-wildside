# Wild Side · Das Haus · «Was bisher geschah.»: Bildvorschläge aus dem Fundus, die auf keiner Seite stehen (Robert 31.10.2026).
# 00 = heute, 01–03 = je ein Satz neuer Bilder. Jedes Bild trägt ein Schild «2018 · A». Wechsel mit ← →.
import os, re, json
HIER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); os.chdir(HIER)
ORD = '_varianten/jahre-bilder'
SAETZE = [('A', ['presse/bilder/2018-09-11_vimeo_niemand-gin-walk-on-the-wildside.jpg', 'ig/2023-11-12_walkonthewildside_hannover_CzjTFZSsFa5-1.jpg',
                 'ig/2024-06-07_walkonthewildside_hannover_C76ERk_oJal-1.jpg', 'facebook/2025-10-02_fb_1238918918249846.jpg', 'google-maps/google-53.jpg']),
          ('B', ['facebook/2020-06-17_fb_2743375292557948.jpg', 'neu-2026-10/2023-11-28_lizzas.diaryy_C0MQYiKtBvW-1.jpg',
                 'facebook/2024-03-12_fb_821120210029721.jpg', 'facebook/2025-11-17_fb_1279618994179838.jpg', 'google-maps/google-34.jpg']),
          ('C', ['facebook/2020-08-26_fb_2803992436496233.jpg', 'ig-highlights/2023-12-02_highlight-momos-sexy-01.jpg',
                 'ig/2024-11-10_walkonthewildside_hannover_DCMDSnpIOHt-1.jpg', 'facebook/2025-04-13_fb_1101965055278567.jpg',
                 'google-maps/google-18.jpg'])]
JAHRE = ['2018', '2023', '2024', '2025', '2027']
basis = open('haus.html').read()
a = basis.index('<section class="kap hell auf" id="seit2017">'); b = basis.index('</section>', a) + 10
HEUTE = basis[a:b]
LISTE = [[0, 'Heute']] + [[i + 1, 'Satz ' + s] for i, (s, _) in enumerate(SAETZE)]
STIL = ('<style>#seit2017 .jf-b .vb{position:absolute;left:12px;top:12px;z-index:3;background:#1C1513;color:#D8B264;font:500 13px/1 "Hanken",Arial,sans-serif;'
        'letter-spacing:.12em;padding:9px 12px;border-radius:8px}</style>')

def satz(buchst, dateien):
    s, i = HEUTE, 0
    out = []
    for teil in re.split(r'(<figure class="kachel leise jf-b".*?</figure>)', s, flags=re.S):
        if teil.startswith('<figure class="kachel leise jf-b"'):
            teil = ('<figure class="kachel leise jf-b"><img src="../_quelle/%s" alt="" decoding="async" style="object-position:50%% 50%%">'
                    '<span class="vb">%s · %s</span></figure>') % (dateien[i], JAHRE[i], buchst)
            i += 1
        out.append(teil)
    assert i == 5
    return ''.join(out)

def seite(nr, abschnitt, name):
    h = basis[:a] + abschnitt + basis[b:]
    h = h.replace('<head>', '<head><base href="../../">', 1).replace('</head>', '<link rel="stylesheet" href="%s/varianten-nav.css">%s\n</head>' % (ORD, STIL), 1)
    fuss = ('<p class="vschild"><b>%02d / %02d</b><span>%s</span><i>← →</i></p>\n<script>window.VARIANTEN=%s;window.VNR=%d;window.VORD=%s;</script>'
            '<script src="%s/varianten-nav.js" defer></script>\n</body>') % (nr, len(SAETZE), name, json.dumps(LISTE, ensure_ascii=False), nr, json.dumps(ORD), ORD)
    return h.replace('</body>', fuss, 1)

open(ORD + '/00.html', 'w').write(seite(0, HEUTE, 'Heute'))
for i, (bu, d) in enumerate(SAETZE):
    open(ORD + '/%02d.html' % (i + 1), 'w').write(seite(i + 1, satz(bu, d), 'Satz ' + bu))
print('ok')
