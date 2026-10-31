#!/usr/bin/env python3
"""Werkbank Wild Side, Blatt «Worum es geht» zwischen Brief und Inhalt (Aufbau und Kleid wie sb_worum.py des Culinarium, dort aus dem Schäfli).
Robert 29.10.2026 (Culinarium): «Die Rechnung» raus, keine Rechnung mit Annahmen. Hier stehen die zwei Ziele der Bar und, als Gegenstück zu den Eingabefeldern,
nur belegte Angaben der Website (website/tafel.html, website/programm.html, website/bau.py HAUS). Kein Agenturpreis, keine Zusage."""
import html, os, re

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)
_TAFEL = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', open(os.path.join(os.path.dirname(ROOT), 'tafel.html'), encoding='utf-8').read()))


def _beleg(muster):
    """Eine Angabe nur, wenn sie wörtlich auf der Seite Feiern steht (sonst leer und die Zeile entfällt)."""
    return bool(re.search(muster, _TAFEL))


BELEGT = [  # Zeile, Wert, Quelle; nur, was auf der Website steht
    ('Offen', 'Do 19–1, Fr/Sa 19–2 Uhr', 'Zeiten der Bar', True),
    ('Donnerstag', 'ab und zu live, ohne Eintritt', 'Seite Programm', True),
    ('Privates Dinner', '10 bis 14 Gäste', 'Seite Feiern', _beleg(r'Privates Dinner 10 bis 14 Gäste')),
    ('Die lange Tafel', '10 bis 20 Gäste, 4 Stunden', 'Seite Feiern', _beleg(r'10–20 Gäste an der Tafel')),
    ('Die ganze Bar', 'ab 30 Gästen, 49, 59 oder 79 € pro Person', 'Seite Feiern', _beleg(r'49 € pro Person') and _beleg(r'79 € pro Person')),
]


def blatt(k):
    gruende = [('Donnerstag voller machen', 'Der Donnerstag steht auf der Seite wie Freitag und Samstag: mit Konzert, wenn eins ist, und dem Weg zum Reservieren. Wer am Wochenende keinen Platz bekommt, sieht den Donnerstag.'),
               ('Feiern anfragen, ohne zu suchen', 'Privates Dinner, lange Tafel, ganze Bar: Format wählen, Tag und Zahl der Gäste nennen. Die Anfrage landet im Werkzeug, nicht irgendwo in den Nachrichten.'),
               ('Gefunden werden', 'Heute gibt es das Wild Side nur auf Instagram und in Portalen. Eine eigene Adresse mit Zeiten, Karte und Weg macht euch bei Google zur ersten Antwort.')]
    fotos = ['vt-g-1', 'vt-g-2', 'vt-g-3']
    gr = ''.join(f'<li>' + (f'<span class="vt-gb">{k["bild"](f, t)}</span>' if f in k['m'] else '') + f'<b>{e(t)}</b><span>{e(x)}</span></li>' for (t, x), f in zip(gruende, fotos))
    zeilen = ''.join(f'<div class="vt-feld"><div class="vt-feld__l"><span>{e(z)}</span><small>{e(q)}</small></div><div class="vt-feld__w vt-feld__w--text">{e(w)}</div></div>' for z, w, q, ok in BELEGT if ok)
    return f'''
<section class="fl fl--navy tapete blatt vt" id="worum">
  <div class="in">
    {k['kopf'](0, 'Worum es geht', ['Mehr Gäste am Donnerstag,', 'mehr Feiern auf der Empore.'], 'Die neue Seite soll zwei Dinge leichter machen: dass an den Donnerstagen mehr Gäste kommen, und dass Feiern und Private Dinner als Anfrage bei euch ankommen, statt in Nachrichten unterzugehen. Zahlen stehen hier nur, wo sie auf eurer Seite belegt sind.')}
    <div class="ag-blatt vt-r" data-a="hoch">
      <div class="vt-r__t">
        <p class="ag-r__n">Zwei Ziele</p>
        <h3>Ein voller Donnerstag, eine Anfrage mehr.</h3>
        <p class="vt-r__lead">Wie viele Gäste mehr kommen, kann niemand vorher sagen. Was die Seite tun kann: den Donnerstag zeigen, das Reservieren leicht machen und jede Feier mit Format, Tag und Zahl der Gäste zu euch bringen.</p>
        <p class="ag-r__n vt-gr__k">Drei Wege an die Bar</p>
        <ul class="vt-gr">{gr}</ul>
        <p class="vt-gegen__satz">Ob es so kommt, entscheidet nicht die Seite allein. Instagram, Empfehlungen und euer Ruf haben ihren Teil daran. Versprechen kann ich keine Zahl.</p>
      </div>
      <div class="vt-r__r">
        <p class="vt-r__k">Was auf eurer Seite steht</p>
        {zeilen}
      </div>
    </div>
  </div>
</section>'''


def bilder(webp, haus):
    for n, key, lage in (('vt-g-1', 'konzert', (.5, .45)), ('vt-g-2', 'an-empore-tafel', (.5, .45)), ('vt-g-3', 'schild-ecke', (.5, .45))):
        webp(haus(key), n, 520, 80, 3 / 2, lage)


JS = '''<script id="vt-rechner">
(function(){var S=document.getElementById('worum');if(!S)return;
var nf=new Intl.NumberFormat('de-DE',{maximumFractionDigits:0});
function w(el){var t=String(el.value).replace(/[\\u2019'\\u202f\\u00a0 ]/g,'').replace(/,/g,'.');var v=parseFloat(t);return isFinite(v)&&v>=0?v:null}
function setze(k,t){[].forEach.call(S.querySelectorAll('[data-vt="'+k+'"]'),function(x){x.textContent=t})}
function rechne(){var v={};[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){var x=w(i);i.classList.toggle('falsch',x===null);v[i.getAttribute('data-k')]=x===null?0:x});
var fest=v.mehr*v.plaetze*v.preis,lunch=v.frei*(v.abende+v.mehr)*v.preis;
setze('feste',nf.format(v.mehr));setze('lunch',nf.format(v.frei));setze('fest',nf.format(fest));setze('lunchsumme',nf.format(lunch));setze('summe',nf.format(fest+lunch))}
[].forEach.call(S.querySelectorAll('input[data-k]'),function(i){i.addEventListener('input',rechne)});rechne()})();
</script>'''


CSS = '''
.vt-feld__w--text{font-family:var(--serif);font-size:1.18rem;line-height:1.3;text-align:right;max-width:58%}
/* Blatt des Rechenbeispiels (Bauart des Blatts aus rh_angebot.py des Ruedihus) */
.ag-blatt{position:relative;padding:clamp(28px,3.8vw,64px);border-radius:clamp(22px,2.4vw,34px);background:linear-gradient(rgba(251,252,254,.94),rgba(251,252,254,.94)),var(--weiss) url(../assets/zeichen/tapete-hell.svg) 50% 0/224px auto;color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 50px 70px -46px rgba(0,0,0,.95)}
.ag-blatt::before,.ag-blatt::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(15,54,120,.4);border-radius:clamp(14px,1.6vw,24px);inset:clamp(10px,1.1vw,16px)}
.ag-blatt::after{inset:clamp(15px,1.5vw,22px);border-color:rgba(15,54,120,.18);border-radius:clamp(11px,1.3vw,19px)}
.ag-r__n{margin:0 0 12px;font-family:var(--mono);font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--taupe)}
.vt-r{color:var(--tinte)}
.vt-gr li{display:grid;grid-template-columns:clamp(92px,9vw,128px) 1fr;column-gap:16px;align-items:start}
.vt-gr li>.vt-gb{grid-row:1/span 2;display:block;border-radius:12px;overflow:hidden;aspect-ratio:3/2}.vt-gr li>.vt-gb img{display:block;width:100%;height:100%;object-fit:cover}
.vt-gr li>b,.vt-gr li>span:not(.vt-gb){grid-column:2}
'''
