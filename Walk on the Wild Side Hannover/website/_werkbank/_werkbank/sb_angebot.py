#!/usr/bin/env python3
"""Werkbank Wild Side, Kapitel VIII «Die Übergabe» (Robert 1.11.2026, ersetzt das frühere Angebot): Alles gehört euch, es läuft so, keine Bindung;
laufende Betreuung optional, aber empfohlen. Dazu die Karte «Die Übergabe.» (werkbank/karte.html und PDF, gebaut von sb_ki.py). Keine Preise."""
import html, os

e = html.escape
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(W)

DATUM = 'Hamburg, 1. November 2026'   # Absender und Ort immer Hamburg
PDF_NAME = 'vorschlag-wildside.pdf'
PF = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
ORN = '<div class="sag-orn" aria-hidden="true"><i></i><b></b><i></i></div>'
DATEN = ['Die Seite setzt keine Cookies und verfolgt niemanden.', 'Der Chat kennt nur, was auf euren Seiten und Karten steht.', 'Karten- und Zahlungsdaten haben im Chat nichts verloren.',
         'Ab dem Start meldet sich jede Person mit eigenem Passwort an.', 'Bis zum Start findet keine Suchmaschine den Entwurf.']


def bilder(webp, haus):
    import haus as _H
    webp(haus(_H.bild('fenster')), 'sag-haus', 1400, 80, 1.18, (.3, .5))


def angebot(k):
    """Kapitel VIII «Die Übergabe» (Robert 1.11.2026): alles gehört euch, es läuft so, keine Bindung, kein Vertrag; Wartung nur auf Wunsch.
    Keine Preise, keine Wochen, keine Leistungstabelle."""
    bild, kopfk = k['bild'], k['kopfk']
    h = lambda n, t: f'<h3 class="sag-h"><span>{n}</span>{e(t)}</h3>'
    liste = lambda pp: '<ul class="sag-l">' + ''.join(f'<li>{e(p)}</li>' for p in pp) + '</ul>'
    return f'''
<section class="fl fl--nacht tapete-leicht blatt sag" id="k8">
  <div class="in">
    {kopfk('k8', ['Alles gehört', 'euch.'], 'Website, Werkzeuge, Drucksachen und Dateien: Ihr bekommt alles, so wie es hier liegt. Ohne Bindung, ohne Vertrag.')}
    <div class="sag-blatt sag-kurz" id="sag-kurz" data-a="heben">
      <figure class="sag-bild">{bild('sag-haus', 'Die Fenster des Walk on the Wild Side am Abend')}</figure>
      <div class="sag-text">{h('01', 'Die Übergabe')}{''.join(f'<p>{e(p)}</p>' for p in UEBERGABE)}</div>
    </div>
    <div class="sag-blatt sag-zwei" id="sag-aufbau" data-a="heben">
      <div>{h('02', 'Was ihr bekommt')}{liste(BEKOMMT)}</div>
      <div>{h('03', 'Eure Daten und die eurer Gäste')}{liste(DATEN)}</div>
    </div>
    <div class="sag-blatt sag-zwei" id="sag-betreuung" data-a="heben">
      <div>{h('04', 'Laufende Betreuung')}<p class="sag-opt">Optional, aber empfohlen. Keine Bindung, ihr entscheidet.</p></div>
      <div>{liste(WARTUNG[:4])}</div>
    </div>
    <div class="sag-buehne" id="sag-vorschlag">{karte_html()}</div>
  </div>
</section>'''


UEBERGABE = ['Alles, was hier liegt, ist für euch gemacht und gehört euch: die Website, die sieben Werkzeuge, die Drucksachen und alle Dateien.',
             'Es läuft so, wie ihr es hier seht. Wenn etwas nicht klappt, meldet ihr euch bei mir.',
             'Es gibt keine Bindung und keinen Vertrag. Empfohlen ist eine laufende Betreuung: Ich halte die Seite jeden Monat sicher und aktuell. Sie ist freiwillig, ihr entscheidet.']
BEKOMMT = ['Die neue Website mit allen Seiten, für das Handy und den Rechner', 'Sieben Werkzeuge für Karte, DJ-Abende, Gäste, Marke und Plakate',
           'Eure Karten neu gesetzt, auch als PDF', 'Drucksachen, Untersetzer, Sticker und Postkarten zum Drucken', 'Mails an eure Gäste und ein Feed für Instagram',
           'Alle Dateien sortiert in einem Ordner, dazu eure Wortmarke']
UEBERGABE_KARTE = ['Website, Werkzeuge, Karten, Drucksachen, Beiträge und Dateien gehören dem Walk on the Wild Side.', 'Domain, Server und Zugänge stehen auf euren Namen.',
                   'Die Rechte an Fotos und Plakaten bleiben bei euch und euren Fotografen.']
LAEUFT = ['Alles läuft so, wie ihr es hier seht.', 'Klappt etwas nicht, meldet ihr euch bei mir.', 'Keine Bindung, kein Vertrag.']
WARTUNG = ['Jeden Monat Sicherheitsupdates für Seite und Werkzeuge.', 'Anpassungen beim Datenschutz, wenn sich Regeln ändern.',
           'Server, Domain und Sicherungen im Blick.', 'Kleine Fehler behebe ich, sobald ihr sie meldet.',
           'Optional, aber empfohlen. Ihr sagt Bescheid, wenn ihr sie wollt, und genauso, wenn nicht mehr.']


def karte_html():
    zeilen = lambda pp: '<ul class="mn-l">' + ''.join(f'<li>{e(p)}</li>' for p in pp) + '</ul>'
    gang = lambda n, t: f'<p class="mn-gang"><span>{n}</span>{e(t)}</p>'
    return f'''<article class="mn" data-a="heben">
        <header class="mn-kopf">
          <img class="mn-zeichen" src="eigen/zeichen-kerze.svg" alt="" width="72" height="73">
          <p class="mn-haus">Walk on the Wild Side · Hannover-Linden</p>
          <h3 class="mn-titel">Die Übergabe.</h3>
          <p class="mn-unter">Alles gehört euch. Ohne Bindung, ohne Vertrag.</p>
        </header>
        {ORN}{gang('I', 'Was euch gehört')}{zeilen(UEBERGABE_KARTE)}
        {ORN}{gang('II', 'Wie es läuft')}{zeilen(LAEUFT)}
        {ORN}{gang('III', 'Laufende Betreuung – optional, aber empfohlen')}{zeilen(WARTUNG)}
        <p class="mn-ki"><a class="kn kn--klein" href="ki.html">Mehr zu KI und euren Daten<i>{PF}</i></a></p>
        <footer class="mn-ende"><i></i><span>{e(DATUM)}</span><i></i></footer>
        <p class="mn-pdf"><a class="kn kn--klein" href="{PDF_NAME}" download>Als PDF speichern<i>{PF}</i></a></p>
      </article>'''


CSS = '''
/* ---------- Kapitel VIII «Die Übergabe» (sb_angebot.py): helle Blätter auf der Nacht ---------- */
.sag-opt{margin:14px 0 0;font-family:var(--serif);font-size:clamp(1.15rem,1.5vw,1.4rem);line-height:1.35;color:var(--tinte)}
.sag .kopfzeile{margin-bottom:clamp(30px,3.4vw,54px)}
.sag-reg{display:flex;flex-wrap:wrap;gap:8px clamp(18px,2.6vw,44px);justify-content:center;margin:0 auto clamp(40px,4.6vw,72px);padding-bottom:18px;border-bottom:1px solid rgba(162,182,207,.28)}
.sag-reg a{display:inline-flex;align-items:baseline;gap:9px;font:400 12.5px/1.2 var(--serif);letter-spacing:.22em;text-transform:uppercase;color:var(--creme);text-decoration:none;opacity:.82;transition:opacity .4s}
.sag-reg a span{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--messing)}
.sag-reg a:hover{opacity:1}
.sag-blatt{position:relative;margin-top:clamp(36px,4vw,64px);padding:clamp(28px,3.8vw,64px);border-radius:clamp(22px,2.4vw,34px);background:var(--weiss);color:var(--tinte);
  box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(17,61,136,.22),0 70px 90px -56px rgba(0,0,0,.9),0 26px 40px -30px rgba(0,0,0,.6)}
.sag-blatt::before{content:"";position:absolute;pointer-events:none;inset:clamp(10px,1.1vw,16px);border:1px solid rgba(17,61,136,.2);border-radius:clamp(14px,1.6vw,24px)}
.sag-reg+.sag-blatt{margin-top:0}
.sag-h{display:flex;align-items:baseline;gap:16px;margin:0 0 clamp(18px,2vw,28px);font-family:var(--serif);font-weight:400;font-size:clamp(1.7rem,2.4vw,2.5rem);line-height:1.1;letter-spacing:.06em;text-transform:uppercase;color:var(--tinte)}
.sag-h span{font-family:var(--mono);font-size:clamp(.78rem,.9vw,.92rem);letter-spacing:.16em;color:var(--blau)}
.sag-kurz{display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(26px,3.6vw,64px);align-items:center}   /* eine Spalte am Handy, nie breiter als das Blatt (Tor 30.10.) */
@media(min-width:900px){.sag-kurz{grid-template-columns:minmax(0,.84fr) minmax(0,1.16fr)}}
.sag-bild{margin:0;border-radius:clamp(14px,1.5vw,22px);overflow:hidden;aspect-ratio:1.18;background:var(--creme)}
.sag-bild img{display:block;width:100%;height:100%;object-fit:cover}
.sag-text p{margin:0;font-size:clamp(1.08rem,1.24vw,1.28rem);line-height:1.6;color:rgba(4,16,35,.84)}
.sag-text p+p{margin-top:1em}
.sag-text h3+p{font-size:clamp(1.24rem,1.5vw,1.5rem);line-height:1.45;color:var(--tinte)}
.sag-spalten{display:grid}
.sag-sp{padding:clamp(18px,2vw,30px) 0}
.sag-sp+.sag-sp{border-top:1px solid rgba(17,61,136,.2)}
.sag-sp h4{margin:0 0 8px;font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,1.8vw,1.9rem);line-height:1.15;color:var(--tinte)}
.sag-sp ul,.sag-l{list-style:none;margin:0;padding:0}
.sag-sp li{padding:11px 0;border-top:1px solid rgba(17,61,136,.12);font-size:clamp(1.06rem,1.2vw,1.24rem);line-height:1.4;color:rgba(4,16,35,.88)}
.sag-sp li:first-child{border-top:0}
@media(min-width:760px){
  .sag-spalten{grid-template-columns:repeat(2,minmax(0,1fr))}
  .sag-sp--1,.sag-sp--2,.sag-sp--3{grid-column:1/-1}   /* drei volle Reihen, keine Spalte mit Loch (Tor 30.10.) */
  .sag-sp--1 ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:clamp(22px,2.6vw,44px)}
  .sag-sp--1 li:nth-child(-n+2){border-top:0}
  .sag-sp--3 ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:clamp(22px,2.6vw,44px)}
  .sag-sp--3 li{border-top:0;text-wrap:balance}
  .sag-sp--2 ul{display:flex;flex-wrap:wrap;gap:0 clamp(18px,2vw,34px)}
  .sag-sp--2 li{border-top:0;display:flex;align-items:center;gap:clamp(18px,2vw,34px)}
  .sag-sp--2 li+li::before{content:"";flex:none;width:.7em;height:.74em;background:var(--blau);-webkit-mask:url(eigen/zeichen-c.svg) center/contain no-repeat;mask:url(eigen/zeichen-c.svg) center/contain no-repeat}
}
.sag-zwei{display:grid;grid-template-columns:minmax(0,1fr);gap:clamp(36px,4vw,64px)}
@media(min-width:900px){.sag-zwei{grid-template-columns:repeat(2,minmax(0,1fr))}}
.sag-l li{position:relative;padding:14px 0 14px 30px;border-top:1px solid rgba(17,61,136,.12);font-size:clamp(1.08rem,1.24vw,1.3rem);line-height:1.45;color:rgba(4,16,35,.88)}
.sag-l li:first-child{border-top:0;padding-top:0}
.sag-l li::before{content:"";position:absolute;left:1px;top:.28em;width:.74em;height:.78em;background:var(--blau);-webkit-mask:url(eigen/zeichen-c.svg) center/contain no-repeat;mask:url(eigen/zeichen-c.svg) center/contain no-repeat}   /* das «C» des Hauses als einziges Ornament (29.10.2026, vorher das «x» aus der Schrift) */
.sag-l li:first-child::before{top:.5em}
.sag-teil{margin-top:clamp(56px,6vw,100px)}
.sag-k{margin:0 0 clamp(18px,2vw,28px);text-align:center;font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--messing)}
.sag-weg{list-style:none;margin:0 auto;padding:clamp(10px,1.4vw,18px) clamp(24px,3.4vw,52px);max-width:780px;border-radius:28px;background:var(--weiss);color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(17,61,136,.2),0 40px 50px -36px rgba(0,0,0,.9)}
.sag-s{display:grid;grid-template-columns:clamp(46px,4.4vw,64px) 1fr;gap:clamp(12px,1.6vw,22px);align-items:baseline;padding:clamp(18px,2vw,26px) 0;border-top:1px solid rgba(17,61,136,.16)}
.sag-s:first-child{border-top:0}
.sag-s__n{font-family:var(--serif);font-size:clamp(1.9rem,2.3vw,2.4rem);line-height:1;color:var(--blau)}
.sag-s h4{margin:0 0 6px;font-family:var(--serif);font-weight:400;font-size:clamp(1.25rem,1.5vw,1.55rem);line-height:1.2}
.sag-s p{margin:0;font-size:clamp(1rem,1.08vw,1.12rem);line-height:1.55;color:rgba(4,16,35,.86)}
.sag-w{display:flex;flex-direction:column;padding:clamp(22px,2.2vw,32px);border-radius:24px;background:var(--weiss);color:var(--tinte);box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(17,61,136,.2),0 40px 50px -36px rgba(0,0,0,.9)}
.sag-w__n{display:flex;align-items:baseline;gap:12px;margin:0 0 8px}
.sag-w__n b{font-family:var(--serif);font-weight:400;font-size:clamp(2.2rem,2.6vw,2.8rem);line-height:.9;color:var(--blau)}
.sag-w__n small{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(4,16,35,.5)}
.sag-w h4{margin:0 0 14px;font-family:var(--serif);font-weight:400;font-size:clamp(1.3rem,1.5vw,1.6rem);line-height:1.15}
.sag-w__r{padding:10px 0;border-top:1px solid rgba(17,61,136,.18)}
.sag-w__r span{display:block;margin-bottom:3px;font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--blau)}
.sag-w__r p{margin:0;font-size:clamp(1rem,1.06vw,1.1rem);line-height:1.5;color:rgba(4,16,35,.86)}
.sag-w__r--wer{margin-top:auto}
.sag-satz{margin:clamp(22px,2.4vw,34px) auto 0;max-width:62ch;text-align:center;font-size:clamp(1.06rem,1.24vw,1.28rem);line-height:1.55;color:rgba(255,255,255,.86)}
.sag-buehne{display:flex;justify-content:center;margin-top:clamp(56px,6vw,100px)}
.mn{position:relative;width:min(100%,880px);padding:clamp(34px,5vw,80px) clamp(22px,5.4vw,92px) clamp(30px,4vw,60px);text-align:center;color:var(--tinte);background:var(--weiss);border-radius:6px;
  box-shadow:inset 0 1px 0 #fff,0 0 0 1px rgba(17,61,136,.3),0 90px 110px -60px rgba(0,0,0,.95),0 30px 50px -30px rgba(0,0,0,.7)}
.mn::before,.mn::after{content:"";position:absolute;pointer-events:none;border:1px solid rgba(17,61,136,.34);inset:clamp(10px,1.2vw,18px)}
.mn::after{inset:clamp(14px,1.6vw,24px);border-color:rgba(17,61,136,.14)}
.mn-zeichen{display:block;width:clamp(56px,5.4vw,80px);height:auto;margin:0 auto clamp(14px,1.6vw,22px)}
.mn-haus{margin:0;font:400 clamp(11px,.9vw,13px)/1.3 var(--serif);letter-spacing:.3em;text-transform:uppercase;color:var(--blau)}
.mn-titel{margin:clamp(14px,1.4vw,20px) 0 0;font-family:var(--serif);font-weight:400;font-size:clamp(2.4rem,4.2vw,4.2rem);line-height:1;letter-spacing:.06em;text-transform:uppercase;color:var(--tinte)}
.mn-unter{margin:clamp(12px,1.2vw,16px) auto 0;max-width:46ch;font-size:clamp(1.04rem,1.16vw,1.2rem);line-height:1.5;color:rgba(4,16,35,.66)}
.sag-orn{display:flex;align-items:center;justify-content:center;gap:14px;margin:clamp(26px,3vw,44px) auto clamp(20px,2.2vw,32px);max-width:420px}
.sag-orn i{flex:1;height:1px;background:rgba(17,61,136,.35)}
.sag-orn b{width:auto;height:auto;border:0}.sag-orn b::before{content:"";display:inline-block;width:.8em;height:.84em;background:var(--blau);-webkit-mask:url(eigen/zeichen-c.svg) center/contain no-repeat;mask:url(eigen/zeichen-c.svg) center/contain no-repeat}
.mn-gang{margin:0 0 clamp(14px,1.6vw,22px);font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,2.1vw,2.1rem);line-height:1.1;color:var(--tinte)}
.mn-gang span{display:block;margin-bottom:8px;font:400 11px/1 var(--mono);letter-spacing:.3em;color:var(--blau)}
.mn-l{list-style:none;margin:0 auto;padding:0;max-width:62ch}
.mn-l li{padding:8px 0;font-size:clamp(1.04rem,1.16vw,1.2rem);line-height:1.55;color:rgba(4,16,35,.88)}
.mn-preise{max-width:620px;text-align:left}
.mn-p{padding:clamp(12px,1.2vw,16px) 0!important}
.mn-p+.mn-p{border-top:1px solid rgba(17,61,136,.16)}
.mn-p__z{display:flex;align-items:baseline;gap:10px;margin:0}
.mn-p__z b{flex:none;font-family:var(--serif);font-weight:500;font-size:clamp(1.1rem,1.26vw,1.3rem);color:var(--tinte)}
.mn-p__z i{flex:1;border-bottom:1px dotted rgba(17,61,136,.6);transform:translateY(-.3em)}
.mn-p__z span{flex:none;font-size:clamp(1.04rem,1.16vw,1.2rem);color:var(--blau);white-space:nowrap}
.mn-p__l{list-style:none;margin:6px 0 0;padding:0}.mn-p__l li{padding:2px 0 2px 1.1em!important;position:relative;font-size:clamp(.96rem,1.02vw,1.06rem)!important;line-height:1.5!important;color:rgba(4,16,35,.68)!important}.mn-p__l li::before{content:'–';position:absolute;left:0;color:var(--blau)}
.mn-p__s{margin:5px 0 0;font-size:clamp(.96rem,1.02vw,1.06rem);line-height:1.5;color:rgba(4,16,35,.68)}
.mn-fuss{margin:clamp(12px,1.3vw,18px) 0 0;font-size:.96rem;color:rgba(4,16,35,.58)}
.mn-ende{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:clamp(30px,3.4vw,52px)}
.mn-ende i{width:clamp(30px,4vw,60px);height:1px;background:rgba(17,61,136,.4)}
.mn-ende span{font:400 10.5px/1 var(--mono);letter-spacing:.26em;text-transform:uppercase;color:var(--blau)}
.mn-ki,.mn-pdf{margin:clamp(18px,2vw,28px) 0 0}
@media(max-width:600px){.mn-p__z{flex-wrap:wrap;justify-content:center;text-align:center}.mn-p__z i{display:none}.mn-p__z span{width:100%;white-space:normal}.mn-preise{text-align:center}}
.sag [data-a="heben"]{opacity:1;transform:translate3d(0,120px,0) scale(.975);transition:transform 2.1s cubic-bezier(.16,1,.3,1)}
.sag [data-a="heben"].da{transform:none}
@media(prefers-reduced-motion:reduce){.sag [data-a="heben"]{transform:none;transition:none}}
'''
