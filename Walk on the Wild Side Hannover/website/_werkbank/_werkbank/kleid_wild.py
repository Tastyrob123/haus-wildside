"""Kleid Wild Side, zuletzt nach jedem Bau (haus.nach_bau): Schriftfamilien des Kits heißen nach dem, was sie sind (Prata, Hanken Grotesk),
Farbreste der Vorlage (Kerzen-Orange, Nacht-Violett) werden zu den Tönen der Bar. Wiederholbar, ändert nur Ausgaben in werkbank/ und befund/.
Werkbank-Chat Wild Side, Nachtbau 31.10.2026."""
import os
import re

TAUSCH = [
    ("'Instrument Sans'", "'Hanken Grotesk'"), ('"Instrument Sans"', '"Hanken Grotesk"'),
    ("'DM Mono'", "'Hanken Etikett'"), ('"DM Mono"', '"Hanken Etikett"'),
    ('font-family="DM Mono', 'font-family="Hanken Grotesk'), ('font-family="Fraunces', 'font-family="Prata'), ('font-family="Instrument Sans', 'font-family="Hanken Grotesk'),
    ("'Fraunces'", "'Prata'"), ('"Fraunces"', '"Prata"'), ("'Urbanist'", "'Hanken Grotesk'"),
    ('InstrumentSans-normal-400_600.woff2', 'hanken.woff2'), ('DMMono-normal-400.woff2', 'hanken.woff2'), ('DMMono-normal-500.woff2', 'hanken.woff2'),
]
FARBE = {'ef7649': 'd8b264', 'f5a689': 'e7cf98', 'b15736': 'b08a43', '16141b': '130e0d', '3a3845': '33281f', 'dcc68f': 'd8b264'}


def _farben(t):
    t = t.replace('rgba(201,133,67,', 'rgba(216,178,100,').replace('rgba(239,118,73,', 'rgba(216,178,100,').replace('rgba(22,21,26,', 'rgba(19,14,13,')
    return re.sub(r'#(' + '|'.join(FARBE) + r')\b', lambda m: '#' + FARBE[m.group(1).lower()], t, flags=re.I)


def anwenden(root):
    for ordner in ('werkbank', 'befund'):
        for dp, dn, fn in os.walk(os.path.join(root, ordner)):
            for f in fn:
                if not f.endswith(('.html', '.css', '.js', '.svg')):
                    continue
                p = os.path.join(dp, f)
                try:
                    t = open(p, encoding='utf-8').read()
                except UnicodeDecodeError:
                    continue
                n = t
                for a, b in TAUSCH:
                    n = n.replace(a, b)
                n = _farben(n)
                if f.endswith('.html') and not p.endswith(os.path.join('werkbank', 'index.html')):
                    n = n.replace(' loading="lazy"', '')   # kleine Seiten: Bilder sofort laden (WebKit-Prüfung in Actions)
                if n != t:
                    open(p, 'w', encoding='utf-8').write(n)
    # die Kit-Dateinamen in werkbank/fonts bleiben liegen (Inhalt Hanken): andere Kit-Läufe schreiben werkbank.css mit diesen Namen neu


if __name__ == '__main__':
    anwenden(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
