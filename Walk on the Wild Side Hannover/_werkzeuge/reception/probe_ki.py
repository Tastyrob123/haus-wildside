"""Probe-Antworten statt Claude (Robert 16.10.2026: «lokal bis zur Kostenrunde», keine bezahlten KI-Aufrufe in Prüfläufen).

Im Wild Side ist das der Standard: python3 _werkzeuge/reception/server.py 9084 (ohne RECEPTION_KI=1). Kopie aus dem Culinarium, dort aus dem Schäfli, Schlössli, Ruedihus, Carlton und Doldenhorn.
Dann ruft kein Teil des Gästebuchs und vom Chat die KI auf und kein Schlüssel wird gelesen. Jede Stelle, die sonst Claude fragt, bekommt
eine Antwort in genau der Form, die Claude liefern würde, sichtbar als Probe beschriftet:
  Chat (gast.frage)        Text «Probe-Antwort ohne KI …»; nennt der Gast eine E-Mail oder Telefonnummer, ruft die Probe das Werkzeug «anfrage» auf
                           (so entsteht wie echt eine Anfrage im Eingang); enthält die Frage «lücke», meldet sie «nicht belegt».
  Brief (gast.anfrage)     «Betreff: …», Brief mit Anrede, offenen Stellen [in Klammern] und Gruss, darunter «---» mit Punkten fürs Team.
  Übersetzen               JSON mit betreff, text und verlauf in gleicher Länge.
  Wissen einlesen          Werkzeug «eintraege» mit einem Eintrag je Material.
"""
import json, re, time

BEREICH = 'Die Bar'



_CHAT = None


def _beleg(frage):
    """Antwort ohne KI aus dem belegten Wissen, wie der Chat auf der Website (_online/api/frage.py + steckbrief.json); None, wenn nicht ladbar.
    30.10.2026 (Oberchef, Tor K23): «Chat ausprobieren» zeigt keine «Probe/Demo»-Sätze mehr, sondern dieselben Antworten wie die Website."""
    global _CHAT
    try:
        if _CHAT is None:
            import importlib.util, json as _j, os as _o
            hier = _o.path.dirname(_o.path.abspath(__file__))
            spec = importlib.util.spec_from_file_location('probe_frage', _o.path.join(hier, '..', '..', '_online', 'api', 'frage.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
            sb = _j.load(open(_o.path.join(hier, 'steckbrief.json'), encoding='utf-8'))
            m.WISSEN = [{'fid': z['fid'], 'bereich': b['bereich'], 'gruppe': g['gruppe'], 'was': z['was'], 'angabe': z['angabe']}
                        for b in sb['bereiche'] for g in b['gruppen'] for z in g['zeilen']]
            _CHAT = m
        return _CHAT.antworte(frage)
    except Exception:
        return _steckbrief(frage)


_SB = None
_STOPP = set('der die das und oder ein eine einen einem ist sind gibt es bei euch ihr ich du wir was wie wo wann wer kann man mit für von zum zur den dem des auf aus noch auch habt hat haben the and you your for are what how when where'.split())


def _steckbrief(frage):
    """Ohne die Online-Antwort der Website (_online/api/frage.py fehlt in diesem Haus): dieselbe Antwort aus dem belegten Steckbrief, die Zeilen mit den
    meisten gemeinsamen Wörtern als Punkte «Stichwort: Angabe». Nichts erfunden: nur Angaben aus steckbrief.json (jede mit Beleg auf der Website)."""
    global _SB
    try:
        if _SB is None:
            import json as _j, os as _o
            sb = _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), 'steckbrief.json'), encoding='utf-8'))
            _SB = [(b['bereich'], g['gruppe'], z['was'], z['angabe']) for b in sb['bereiche'] for g in b['gruppen'] for z in g['zeilen']]
        f = frage.lower()
        if re.search(r'allerg|unverträg|gluten|laktose|nuss|nüss|hund|dog|barriere|rollstuhl|wheelchair|park|kind|baby|parking|e-?mail', f):
            return None   # steht in keiner Quelle des Hauses: Lücke fürs Team
        thema = [(r'feier|geburtstag|hochzeit|firmen|gruppe|dinner|tafel|empore|ganze bar|pauschale|budget|jga|party|birthday|wedding|group|private', ('Feiern',)),
                 (r'\bdj|session|konzert|live|musik|programm|eintritt|auflegen|gastschicht|silvester|valentin|mai\b|music|concert', ('Programm',)),
                 (r'öffnung|geöffnet|offen|wann|uhr\b|heute|reservier|platz|plätze|tisch|donnerstag|freitag|samstag|sonntag|open|when|book|table', ('Zeiten & Reservieren',)),
                 (r'drink|cocktail|karte|negroni|paloma|mexikaner|preis|kost|euro|€|alkohol|milk|fat|enzym|bier|wein|essen|price|menu', ('Drinks & Preise',)),
                 (r'anfahrt|anreise|adresse|wo ist|wo seid|wo finde|komme ich|hinkommen|bahn|tram|haasemann|küchengarten|where|address', ('Der Weg',)),
                 (r'telefon|anrufen|instagram|kontakt|erreichen|phone|call', ('Kontakt',)),
                 (r'culinarium|dirty|chicken|sandwich', ('Im selben Haus',)),
                 (r'momo|derya|team|falstaff|decke|gewölbe|draussen|terrasse|raum|who', ('Das Haus & Team', 'Die Bar'))]
        ber = next((b for r, b in thema if re.search(r, f)), None)
        w = {x for x in re.findall(r'[a-zäöüß0-9]{3,}', f) if x not in _STOPP}
        kand = [z for z in _SB if ber and z[0] in ber]
        if not kand or not w:
            return None
        def punkte(z):
            t = ' '.join(z).lower()
            return sum(2 if x in z[2].lower() or x in z[1].lower() else 1 for x in w if x in t or (len(x) > 5 and x[:5] in t))
        best = sorted(((punkte(z), -i, z) for i, z in enumerate(kand)), reverse=True)
        if best[0][0] < 1:
            if not ber:
                return None
            best = [(1, 0, z) for z in kand if z[1] == kand[0][1]]   # Thema klar, Wörter nicht: die erste Gruppe des Bereichs
        oben = [z for p, _, z in best if p >= max(1, best[0][0] - 1)][:3]
        g = oben[0][1]
        return {'belegt': True, 'text': f'Dazu steht auf der Website, unter «{g}»:\n' + '\n'.join(f'- {z[2]}: {z[3]}' for z in oben)}
    except Exception:
        return None

def _text(koerper):
    """Alles, was der Aufruf an Text mitschickt (System und Nachrichten), für die Erkennung der Stelle."""
    s = koerper.get('system')
    sys_t = s if isinstance(s, str) else ' '.join(b.get('text', '') for b in (s or []) if isinstance(b, dict))
    msg = []
    for m in koerper.get('messages') or []:
        c = m.get('content')
        if isinstance(c, str):
            msg.append(c)
        else:
            msg += [b.get('text', '') for b in c or [] if isinstance(b, dict) and b.get('type') == 'text']
    return sys_t, msg


def _antwort(text='', werkzeug=None):
    inhalt = [{'type': 'text', 'text': text}] if text else []
    if werkzeug:
        inhalt.append({'type': 'tool_use', 'id': 'toolu_probe', 'name': werkzeug[0], 'input': werkzeug[1]})
    return {'content': inhalt, 'stop_reason': 'tool_use' if werkzeug else 'end_turn', 'usage': {'input_tokens': 0, 'output_tokens': 0}}


def api(koerper):
    sys_t, msg = _text(koerper)
    werkzeuge = [w.get('name') for w in koerper.get('tools') or []]
    letzte = msg[-1] if msg else ''
    if 'eintraege' in werkzeuge:                                    # Wissen einlesen (gedaechtnis._auszug)
        m = re.search(r'BEREICH DES TEAMS: (.+)', letzte)
        bereich = (m.group(1).strip() if m else '') or BEREICH
        roh = ' '.join(msg)
        stueck = re.sub(r'\s+', ' ', roh.split('TEXT DES TEAMS:', 1)[-1] if 'TEXT DES TEAMS:' in roh else roh)[-220:].strip()
        return _antwort(werkzeug=('eintraege', {'grund': 'Aus dem Dokument übernommen', 'eintraege': [
            {'bereich': bereich, 'titel': (' '.join(stueck.split()[:6]) or 'Neuer Eintrag'), 'text': stueck, 'gueltig_bis': None}]}))
    if sys_t.startswith('Du übersetzt'):                             # reception.uebersetzen
        try:
            d = json.loads(letzte)
        except ValueError:
            d = {}
        return _antwort(json.dumps({'betreff': str(d.get('betreff', '')), 'text': str(d.get('text', '')),   # ohne KI: der Wortlaut des Gastes unverändert, ohne Probe-Beschriftung (Tor K23, 30.10.2026)
                                    'verlauf': [str(v) for v in d.get('verlauf') or []]}, ensure_ascii=False))
    if 'ANFRAGE:' in letzte:                                         # gast.anfrage (Brief)
        name = (re.search(r'Name:\s*(.+)', letzte) or re.search(r'"name":\s*"([^"]+)"', letzte))
        wer = name.group(1).strip() if name else 'Gast'
        allerg = (re.search(r'Allergien \(Formular\):\s*(.+)', letzte) or [None, ''])[1].strip()
        art = (re.search(r'Art:\s*(.+)', letzte) or [None, ''])[1].strip()
        satz_al = f'Deine Angaben zu Allergien ({allerg}) gibt das Team an Rudi weiter [Rudi fragen].\n\n' if allerg and allerg != 'keine angegeben' else ''
        if art in ('Privates Dinner', 'Feier'):
            return _antwort(f'Betreff: Euer Abend im Wild Side\n\nHallo {wer},\n\n'
                            'danke für deine Nachricht und schön, dass ihr bei uns feiern wollt.\n\n'
                            'Derya und Momo melden sich mit einem Vorschlag, nur für euch [Angebot von Derya und Momo]. Bei jedem Abend gilt: 30 Prozent eine Woche vorher, der Rest am Abend vor Beginn.\n\n'
                            f'{satz_al}Damit wir euren Abend vorbereiten können:\n- Datum\n- wie viele ihr seid\n- der Anlass\n\n'
                            'Bis bald an der Ecke\n\n[Name]\nWalk on the Wild Side'
                            '\n---\nGrundlage: Feiern (Website)\nOffen: Angebot, Datum, Anzahl')
        return _antwort(f'Betreff: Dein Platz im Wild Side\n\nHallo {wer},\n\n'
                        'danke für deine Nachricht und schön, dass du zu uns an die Ecke kommen willst.\n\n'
                        'Wir schauen, ob dein Platz frei ist [Platz prüfen], und bestätigen dir den Abend per Nachricht.\n\n'
                        f'{satz_al}Damit wir deinen Platz in Ruhe vorbereiten können:\n- welcher Abend\n- welche Uhrzeit\n- wie viele Plätze\n\n'
                        'Bis bald an der Ecke\n\n[Name]\nWalk on the Wild Side'
                        '\n---\nGrundlage: Besuch (Website)\nOffen: Platz, Abend, Uhrzeit')
    # Chat (gast.frage, auch der zweite Schritt nach der Buchungsmaske)
    if any(isinstance(m.get('content'), list) and any(b.get('type') == 'tool_result' for b in m['content']) for m in koerper.get('messages') or []):
        return _antwort('OK')
    frage = letzte.strip()
    kontakt = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+|(?:\+|00)\d[\d\s]{7,}\d', frage)
    if kontakt and 'anfrage' in werkzeuge:
        name = re.search(r'(?:ich bin|mein name ist|name:|my name is|je suis)\s+([A-ZÄÖÜ][\w-]+(?:\s+[A-ZÄÖÜ][\w-]+)?)', frage, re.I)
        pers = re.search(r'(\d{1,3})\s*(?:personen|gäste|persons|people|personnes)', frage, re.I)
        art = 'dinner' if re.search(r'dinner|menü|essen', frage, re.I) else 'feier' if re.search(r'feier|geburtstag|hochzeit|party|birthday|wedding|firmen|gruppe|ganze bar|tafel', frage, re.I) else ('reservieren' if re.search(r'reservier|platz|plätze|tisch|theke|book|table', frage, re.I) else 'nachricht')
        return _antwort('Danke, deine Nachricht liegt jetzt beim Team. Es meldet sich persönlich bei dir.',
                        ('anfrage', {'art': art, 'name': name.group(1) if name else 'Gast', 'kontakt': kontakt.group(0), 'datum': None,
                                     'personen': int(pers.group(1)) if pers else None, 'anliegen': frage[:300]}))
    if 'lücke' in frage.lower() or 'luecke' in frage.lower():
        return _antwort('Dazu steht nichts in meinen Unterlagen. Ich gebe deine Frage gern ans Team weiter.', ('nicht_belegt', {'thema': frage[:80]}))
    if 'reservieren' in werkzeuge and re.search(r'reservier|platz (frei|buchen|für)|tisch für|book|table for', frage, re.I):   # wie echt: der Weg zu «Platz reservieren» unter der Antwort
        return _antwort('Mit «Platz reservieren» auf der Seite Besuch geht es am schnellsten, die Bar bestätigt per Nachricht.\n- Geöffnet: Donnerstag 19 bis 1 Uhr, Freitag und Samstag 19 bis 2 Uhr\n- Viele Gäste: ab zehn gibt es die lange Tafel, ab dreissig die ganze Bar',
                        ('reservieren', {'datum': None, 'uhrzeit': None, 'personen': None}))
    b = _beleg(frage)
    if b and b.get('belegt'):
        return _antwort(b['text'])
    return _antwort('Dazu steht nichts in meinen Unterlagen. Ich gebe deine Frage gern ans Team weiter.', ('nicht_belegt', {'thema': frage[:80]}))   # Uhrzeit: Prüfläufe erkennen daran, dass eine Antwort kam
