#!/usr/bin/env python3
"""Werkbank Wild Side, Kapitel I «Was wir gefunden haben» (Nachtbau 31.10.2026, Bauart wie sb_befund.py des Culinarium, dort aus dem Schäfli).

Das Wild Side hat keine Website. Die vier Funde kommen aus dem Charakterblatt (CHARAKTER.md 2, 9) und dem Kundenmaterial (_quelle/: Web-Archiv der alten
Adresse, Aufnahme des Instagram-Profils, Google Maps, NeoTaste, Falstaff, Angebotsmappe); die Aufnahmen liegen als Kopie in _werkbank/heute/
(befund_bilder.js, damit der Bau ohne _quelle läuft). Kein Vorwurf, keine Mutmassung. Eine Bühne, ein Befund im Blick: Pfeile, Ziffern, Wischen, Tasten.
Der Knopf führt zum ganzen Befund als eigene Seite unter befund/ (kopiere_analyse), ohne mailto."""
import html, json, os, re, shutil
from PIL import Image, ImageDraw

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
PROJ = os.path.dirname(os.path.dirname(ROOT))
SP = os.path.join(W, 'heute')
G = os.path.join(W, 'geraete')
LI = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5"/></svg>'
RE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>'
ALLE = 7   # vier Funde vorn, drei weitere unten
BEFUNDE = [  # nr, was, wo, für die Gäste, fürs Haus, was wir tun würden, Aufnahme am Handy, Ausschnitt (Datei, Kasten in Pixeln) oder None
    dict(nr='01', was='Es gibt keine eigene Website.',
         wo='wildside-hannover.de zeigte von 2017 bis 2025 nur «Wir arbeiten gerade an unserer Website» (Web-Archiv). Am 26. Oktober 2026 war die Adresse frei (DENIC).',
         gaeste='Wer die Bar sucht, findet keine Seite mit Zeiten, Drinks und Weg, nur Portale und ein Profil.',
         haus='Der Name, der auf jedem Plakat steht, führt im Netz nicht zu einer eigenen Seite. Die alte Adresse könnte jemand anderes nehmen.',
         tun='Die freie Adresse sichern und eine eigene Seite mit Drinks, DJ-Abenden, Feiern, Haus und Besuch darunter stellen.',
         ganz='archiv-handy.jpg', nah=None),
    dict(nr='02', was='Instagram ist die einzige Quelle.',
         wo='Profil @walkonthewildside_hannover am 25. Oktober 2026: Zeiten in der Bio, dazu «Schreib uns eine DM oder ruf an». Kein Link zu einer Seite.',
         gaeste='Ohne Anmeldung zeigt das Profil nur die ersten Beiträge. Wann der nächste DJ-Abend ist, steht in einer Bildunterschrift.',
         haus='Jede Frage nach Platz, Zeiten oder Feiern kommt als Nachricht, oft spät am Abend, und will beantwortet werden.',
         tun='Zeiten, DJ-Abende und Reservieren an einem Ort, den jeder ohne Anmeldung öffnen kann; Instagram verweist darauf.',
         ganz='ig-handy.jpg', nah=('ig-profil-rechner.jpg', (1110, 150, 2050, 580))),
    dict(nr='03', was='Die guten Noten stehen woanders.',
         wo='Google Maps am 25. Oktober 2026: 4,8 aus 75 Berichten, als Website «Website hinzufügen». NeoTaste 4,8 aus 40. Falstaff Bar Guide 2027: 91 Punkte.',
         gaeste='Wer euch empfohlen bekommt, liest die Noten in Portalen, die andere führen, mit Fotos, die andere ausgesucht haben.',
         haus='Die 91 von Falstaff und die 4,8 bei Google stehen nirgends bei euch selbst.',
         tun='Falstaff, Google und NeoTaste auf der eigenen Seite nennen, mit Quelle, und Google die eigene Adresse geben.',
         ganz='noten-handy.jpg', nah=None),   # Robert 1.11.2026: das Bild zeigt die Noten (Website-Stelle «Drei Zahlen», haus.html#stimmen)
    dict(nr='04', was='Feiern stehen in einer PDF.',
         wo='Die Angebotsmappe der Bar (PDF): Privates Dinner, lange Tafel, ganze Bar mit Preisen. Als Kontakt nennt sie die E-Mail-Adresse von Culinarium.',
         gaeste='Wer feiern will, muss erst nach der Mappe fragen und dann per Nachricht oder Anruf anfragen.',
         haus='Anfragen kommen ohne Format, Tag und Zahl der Gäste und landen dort, wo gerade jemand liest.',
         tun='Die Mappe als Seite «Feiern» mit Preisen und einer Anfrage, die mit Format, Tag und Zahl der Gäste im Werkzeug ankommt.',
         ganz=None, nah=('mappe-seite1.jpg', (0, 0, 2200, 1238))),
]


def befunde():
    aus = []
    for b in BEFUNDE:
        x = dict(b)
        x['ganz'] = os.path.join(SP, b['ganz']) if b['ganz'] and os.path.exists(os.path.join(SP, b['ganz'])) else None
        x['nah'] = (os.path.join(SP, b['nah'][0]), b['nah'][1]) if b['nah'] and os.path.exists(os.path.join(SP, b['nah'][0])) else None
        x['voll'] = ''
        aus.append(x)
    return aus


def _handy(schirm):
    L = json.load(open(os.path.join(G, 'handy.json')))
    g = Image.open(os.path.join(G, 'handy-geraet.png')).convert('RGBA')
    x, y, b, h = (round(v * (g.width if i % 2 == 0 else g.height)) for i, v in enumerate(L['schirm']))
    s = Image.open(schirm).convert('RGB')
    f = max(b / s.width, h / s.height)
    s = s.resize((max(b, round(s.width * f)), max(h, round(s.height * f))), Image.LANCZOS).crop((0, 0, b, h))
    m = Image.new('L', (b, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, b - 1, h - 1], radius=round(b * .1), fill=255)
    grund = Image.new('RGBA', g.size, (0, 0, 0, 0)); grund.paste(s, (x, y), m); grund.alpha_composite(g)
    gx, gy, gb, gh = L['gehaeuse']
    return grund.crop((round(gx * g.width) - 6, round(gy * g.height) - 6, round((gx + gb) * g.width) + 6, round((gy + gh) * g.height) + 6))


def bilder(webp):
    for b in befunde():
        if b['ganz']:
            webp(_handy(b['ganz']), f'bf-h-{b["nr"]}', 700, 84)
        if b['nah']:
            webp(Image.open(b['nah'][0]).convert('RGB').crop(b['nah'][1]), f'bf-n-{b["nr"]}', 1100, 84)


STARK = [  # was der heutige Auftritt gut macht (CHARAKTER.md 2–4, Portale)
    ('Die Bar hat eine Stimme.', '«Eure Nachbarschafts-Mixology-Bar», «Good Drinks, Good Music, Good Energy», «Du sagst, was du magst»: Sätze, die man der Bar sofort zuordnet.'),
    ('Die Noten stimmen.', 'Falstaff Bar Guide 2027 mit 91 Punkten, Google 4,8 aus 75, NeoTaste 4,8 aus 40.'),
    ('Jeder DJ-Abend hat sein Plakat.', 'Seit September 2025 die SESSION-Plakate mit roten Wellen und Ultramarin-Schrift, dazu die weißen Plakate mit roter Wortmarke.'),
    ('Der Raum erzählt.', 'Das Gewölbe an der Decke, NEGRONI in Glühbirnen, das Eckschild mit Goldrahmen: Bilder, die nur hier entstehen.'),
]
WEITERE = [  # die übrigen Punkte, die vorne nicht stehen
    ('Ein Kalender.', 'DJ-Abende, Konzerte und Feste stehen nur in Beiträgen; zwischen zwei Abenden steht nirgends, wann der nächste kommt.'),
    ('Die Köpfe.', 'Über Derya und Momo gibt es außerhalb von Instagram und zwei Zeitungsartikeln kaum eine Zeile.'),
    ('Impressum und Datenschutz.', 'Zum Profil gibt es keins. Auf der eigenen Seite stehen beide mit euren Angaben, sobald sie online geht.'),
]


def kopiere_analyse():
    """Der ganze Befund als eigene Seite neben der Werkbank (befund/index.html), für Derya und Momo geschrieben: was heute stark ist,
    die vier Funde von vorn mit Bild und die übrigen drei. Quelle: Befund des Spähers (Station 02), nichts dazuerfunden. Die interne Seite der Kette
    (Knöpfe «Passt, weiter», Rückfragen) wird nicht kopiert."""
    import kern as K
    z = os.path.join(ROOT, 'befund'); os.makedirs(os.path.join(z, 'img'), exist_ok=True)
    bilder_ = {}
    for b in befunde():
        for art, q in (('h', b['ganz']), ('n', b['nah'])):
            if not q:
                continue
            im = _handy(q) if art == 'h' else Image.open(q[0]).convert('RGB').crop(q[1])
            im.thumbnail((900, 900)); n = f'{art}-{b["nr"]}.webp'
            (im if im.mode == 'RGBA' else im.convert('RGB')).save(os.path.join(z, 'img', n), 'WEBP', quality=84); bilder_.setdefault(b['nr'], []).append((n, im.size, art))
    stark = ''.join(f'<li><b>{e(t)}</b><span>{e(s)}</span></li>' for t, s in STARK)
    funde = ''
    for b in befunde():
        bi = ''.join(f'<img src="img/{n}" width="{w}" height="{h}" alt="Aufnahme zum Fund {b["nr"]}" loading="lazy" decoding="async" class="bfs-{art}">' for n, (w, h), art in bilder_.get(b['nr'], []))
        funde += (f'<article class="bfs-f"><div class="bfs-b">{bi}</div><div><p class="bfs-nr">{b["nr"]}</p><h2>{e(b["was"])}</h2><p class="bfs-wo"><b>Wo</b>{e(b["wo"])}</p>'
                  f'<dl><dt>Für eure Gäste</dt><dd>{e(b["gaeste"])}</dd><dt>Für euch</dt><dd>{e(b["haus"])}</dd><dt>Was wir tun würden</dt><dd>{e(b["tun"])}</dd></dl></div></article>')
    weitere = ''.join(f'<li><b>{e(t)}</b><span>{e(s)}</span></li>' for t, s in WEITERE)
    haupt = f'''<section class="fl fl--nacht tapete-leicht bfs"><div class="in">
  <p class="kap kap--z">Der Befund</p>
  <h1 class="t1 zt"><span class="z"><span>Wie das Wild Side</span></span><span class="z"><span><em>heute im Netz steht.</em></span></span></h1>
  <p class="bfs-lauf">Heute gibt es das Wild Side auf Instagram, unter @walkonthewildside_hannover, und in Portalen. Angesehen im Oktober 2026, ohne Anmeldung.
  Hier steht zuerst, was schon stark ist, dann, was einem Gast auf dem Weg an eure Theke fehlt.</p>
</div></section>
<section class="fl fl--papier tapete-hell bfs"><div class="in"><h2 class="bfs-h">Was schon stark ist</h2><ul class="bfs-l">{stark}</ul></div></section>
<section class="fl fl--nacht tapete-leicht bfs"><div class="in"><h2 class="bfs-h">Vier Punkte von vorn</h2>{funde}</div></section>
<section class="fl fl--papier tapete-hell bfs"><div class="in"><h2 class="bfs-h">Was sonst noch fehlt</h2><ul class="bfs-l">{weitere}</ul></div></section>'''
    css = ('<style>.bfs .in{max-width:1180px}.bfs-lauf{max-width:62ch;margin:18px auto 0;text-align:center;font-size:clamp(1.05rem,1.3vw,1.25rem);line-height:1.6;color:rgba(250,244,244,.86)}'
           '.bfs-h{font-family:var(--serif);font-weight:400;font-size:clamp(1.8rem,3vw,2.8rem);margin:0 0 clamp(24px,3vw,44px)}'
           '.bfs-l{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:clamp(18px,2vw,30px)}'
           '.bfs-l li{display:flex;flex-direction:column;gap:8px;padding-top:16px;border-top:1px solid rgba(38,36,45,.16)}.bfs-l b{font-family:var(--serif);font-weight:400;font-size:1.3rem}.bfs-l span{line-height:1.6}'
           '.bfs-f{display:grid;gap:clamp(24px,4vw,64px);align-items:center;padding:clamp(28px,4vw,56px) 0;border-top:1px solid rgba(250,244,244,.14)}'
           '@media(min-width:900px){.bfs-f{grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}}'
           '.bfs-b{display:flex;gap:16px;align-items:center;justify-content:center}.bfs-b img{max-width:100%;height:auto}.bfs-h{max-width:none}.bfs-b .bfs-h{width:min(260px,46%)}.bfs-b .bfs-n{width:min(520px,100%);border-radius:12px}'
           '.bfs-b img.bfs-h{width:min(260px,46%);max-height:none}.bfs-b img.bfs-n{width:min(480px,100%)}'
           '.bfs-b img{min-width:0}.bfs-b:has(img+img) img.bfs-h{width:32%;flex:none}.bfs-b:has(img+img) img.bfs-n{width:auto;flex:1 1 0}'   # Gestaltung 28.10.2026: zwei Bilder teilen sich die Spalte, nichts ragt in den Text oder über den Rand
           '.bfs-nr{margin:0;font-family:var(--serif);font-size:clamp(3rem,6vw,5.6rem);line-height:.9;color:var(--gold)}.bfs-f h2{font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2.2vw,2.1rem);margin:12px 0 0}'
           '.bfs-wo{display:flex;gap:14px;margin:16px 0 0;line-height:1.55;color:rgba(250,244,244,.78)}.bfs-wo b{font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding-top:3px}'
           '.bfs-f dl{margin:18px 0 0}.bfs-f dt{margin-top:14px;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}.bfs-f dd{margin:6px 0 0;line-height:1.6;color:rgba(250,244,244,.9)}</style>')
    s = K.rahmen('Der Befund', 'Wie das Wild Side heute im Netz steht, angesehen im Oktober 2026.', 'Befund', haupt,
                 'Ein Befund von Robert Reff, Tasty Studios, nach dem Stand vom Oktober 2026. Aufnahmen von Instagram, Portalen und dem Web-Archiv nur zur Anschauung.')
    s = s.replace('</head>', css + '</head>', 1)
    open(os.path.join(z, 'index.html'), 'w', encoding='utf-8').write(s)


def abschnitt(k, kopfk):
    M, bild = k['m'], k['bild']
    B = befunde()
    platten = ''
    for i, b in enumerate(B):
        handy = (f'<div class="sbf-handy">{bild("bf-h-" + b["nr"], "Aufnahme von Instagram zum Befund " + b["nr"], lazy=i > 1)}</div>' if 'bf-h-' + b['nr'] in M else '')
        nah = (f'<figure class="sbf-nah">{bild("bf-n-" + b["nr"], "Ausschnitt mit der Stelle", lazy=i > 1)}</figure>' if 'bf-n-' + b['nr'] in M else '')
        sinn = ''.join(f'<div class="sbf-sinn__z"><dt>{e(t)}</dt><dd>{e(x)}</dd></div>' for t, x in (('Für eure Gäste', b['gaeste']), ('Für euch', b['haus']), ('Was wir tun würden', b['tun'])) if x) \
            or f'<div class="sbf-sinn__z"><dd>{e(b["voll"])}</dd></div>'
        platten += (f'<article class="sbf-p{" an" if i == 0 else ""}" data-i="{i}" aria-label="Befund {b["nr"]}">'
                    f'<div class="sbf-bild">{handy}{nah}</div>'
                    f'<div class="sbf-text"><p class="sbf-nr">{b["nr"]}</p><h3>{e(b["was"])}</h3><p class="sbf-wo"><b>Wo</b>{e(b["wo"])}</p><dl class="sbf-sinn">{sinn}</dl></div></article>')
    ziffern = ''.join(f'<button type="button" class="sbf-z" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}">{b["nr"]}</button>' for i, b in enumerate(B))
    return f'''
<section class="fl fl--nacht tapete-leicht blatt sbf" id="k1">
  <div class="in">
    {kopfk('k1', ['Gut bewertet,', 'aber schwer zu finden.'], f'Heute gibt es das Wild Side auf Instagram und in Portalen. Von den {ALLE} Punkten, die fehlen, stehen hier die vier, die am meisten ausmachen, jeder mit einer Aufnahme als Beleg. Die übrigen stehen im ganzen Befund.')}
    <div class="sbf-b" tabindex="0" aria-roledescription="Karussell" aria-label="Die Befunde">
      <div class="sbf-platten">{platten}</div>
      <div class="sbf-fuss"><button type="button" class="wf__pf" data-f="-1" aria-label="Voriger Befund">{LI}</button><div class="sbf-ziffern">{ziffern}</div><button type="button" class="wf__pf" data-f="1" aria-label="Nächster Befund">{RE}</button></div>
    </div>
    <div class="kn-reihe" data-a="auf" style="justify-content:center;margin-top:clamp(28px,3vw,48px)">{k['kn']('Den ganzen Befund ansehen', '../befund/index.html')}</div>
  </div>
</section>
<script>(function(){{var s=document.querySelector('.sbf-b');if(!s)return;var P=[].slice.call(s.querySelectorAll('.sbf-p')),Z=[].slice.call(s.querySelectorAll('.sbf-z')),ist=0,n=P.length;
function zeig(k){{ist=(k%n+n)%n;P.forEach(function(p,i){{p.classList.toggle('an',i===ist);if(i===ist||i===(ist+1)%n)[].forEach.call(p.querySelectorAll('img[loading=lazy]'),function(x){{x.loading='eager'}})}});Z.forEach(function(z,i){{z.setAttribute('aria-pressed',i===ist?'true':'false')}})}}
[].forEach.call(s.querySelectorAll('[data-f]'),function(b){{b.addEventListener('click',function(){{zeig(ist+(+b.getAttribute('data-f')))}})}});
Z.forEach(function(z,i){{z.addEventListener('click',function(){{zeig(i)}})}});
s.addEventListener('keydown',function(ev){{if(ev.key==='ArrowRight')zeig(ist+1);else if(ev.key==='ArrowLeft')zeig(ist-1)}});
var x0=null;s.addEventListener('touchstart',function(ev){{x0=ev.touches[0].clientX}},{{passive:true}});s.addEventListener('touchend',function(ev){{if(x0===null)return;var d=ev.changedTouches[0].clientX-x0;x0=null;if(Math.abs(d)>50)zeig(ist+(d<0?1:-1))}},{{passive:true}})}})();</script>'''


CSS = '''
/* ---------- Kapitel I «Was wir gefunden haben» (sb_befund.py, 19.10.2026): ein Befund im Blick, Handy mit der heutigen Seite, daneben der Ausschnitt ---------- */
.sbf-b{outline:0;margin-top:clamp(16px,2vw,32px)}
.sbf-platten{display:grid}
.sbf-p{grid-area:1/1;display:grid;gap:clamp(26px,4vw,72px);align-items:center;opacity:0;visibility:hidden;transition:opacity .25s linear,visibility 0s .25s}
.sbf-p.an{opacity:1;visibility:visible;transition:opacity .45s linear .1s,visibility 0s}
@media(min-width:960px){.sbf-p{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.sbf-bild{position:relative;display:flex;align-items:center;justify-content:center;min-height:clamp(320px,40vw,620px)}
.sbf-handy{width:clamp(200px,20vw,300px);transform:rotate(-4deg);filter:drop-shadow(0 34px 34px rgba(0,0,0,.55))}
.sbf-handy img{display:block;width:100%;height:auto}
.sbf-nah{position:absolute;right:0;bottom:4%;width:clamp(200px,24vw,360px);margin:0;border-radius:16px;overflow:hidden;transform:rotate(3deg);
  box-shadow:0 0 0 6px var(--weiss),0 0 0 7px rgba(162,182,207,.6),0 34px 44px -24px rgba(0,0,0,.85)}
.sbf-handy+.sbf-nah{right:2%}
.sbf-bild>.sbf-nah:only-child{position:static;width:min(100%,520px);transform:rotate(-2deg)}
.sbf-nah img{display:block;width:100%;height:auto}
.sbf-p.an .sbf-handy{animation:sbfHoch 1.1s cubic-bezier(.16,1,.3,1) both}.sbf-p.an .sbf-nah{animation:sbfHoch 1.3s cubic-bezier(.16,1,.3,1) .12s both}
@keyframes sbfHoch{from{translate:0 60px}to{translate:0 0}}
.sbf-nr{margin:0;font-family:var(--serif);font-size:clamp(3.6rem,7vw,7rem);line-height:.9;letter-spacing:.06em;color:var(--gold)}
.sbf-text h3{margin:clamp(12px,1.4vw,20px) 0 0;font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2.1vw,2.2rem);line-height:1.25;color:var(--weiss);text-wrap:balance}
.sbf-wo{display:flex;gap:14px;margin:clamp(14px,1.6vw,22px) 0 0;font-size:clamp(.96rem,1.04vw,1.06rem);line-height:1.55;color:rgba(243,246,249,.78)}
.sbf-wo b{flex:none;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding-top:3px}
.sbf-sinn{margin:clamp(18px,2vw,28px) 0 0;border-top:1px solid rgba(162,182,207,.3)}
.sbf-sinn__z{padding:12px 0;border-bottom:1px solid rgba(162,182,207,.22)}
.sbf-sinn dt{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}
.sbf-sinn dd{margin:6px 0 0;font-size:clamp(1rem,1.08vw,1.1rem);line-height:1.6;color:rgba(243,246,249,.9)}
.sbf-fuss{display:flex;align-items:center;justify-content:center;gap:clamp(12px,2vw,28px);margin-top:clamp(26px,3vw,44px)}
.sbf-ziffern{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;max-width:640px}
.sbf-z{min-width:40px;padding:7px 9px;border-radius:999px;font-family:var(--mono);font-size:.78rem;color:rgba(243,246,249,.62);box-shadow:inset 0 0 0 1px rgba(162,182,207,.3);transition:color .4s,background .4s}
.sbf-z[aria-pressed="true"]{color:var(--tinte);background:var(--gold)}
@media(max-width:700px){.sbf-bild{min-height:0;padding:10px 0 30px}.sbf-handy{width:56vw}.sbf-nah{width:58vw;bottom:0}.sbf-ziffern{display:none}}
@media(prefers-reduced-motion:reduce){.sbf-p,.sbf-p.an .sbf-handy,.sbf-p.an .sbf-nah{transition:none;animation:none}}
'''
