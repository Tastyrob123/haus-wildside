#!/usr/bin/env python3
"""Das Markenbuch · Walk on the Wild Side Hannover: liest das Bildregister der Website (BILDER in website/bilder.py), ohne die Datei auszuführen
(Falle 9: der Import baut Bilder). Je Schlüssel (Quelle in _quelle/, Alt-Text); Grössen und Stufen stehen in website/assets/bild/<schlüssel>.json."""
import ast, os

HIER = os.path.dirname(os.path.abspath(__file__))
PROJEKT = os.path.dirname(os.path.dirname(HIER))
WEB = os.path.join(PROJEKT, 'website')


def lesen():
    """{schlüssel: (quelle relativ zu _quelle/, alt)} wie BILDER in website/bilder.py."""
    baum = ast.parse(open(os.path.join(WEB, 'bilder.py'), encoding='utf-8').read())
    for n in baum.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'BILDER':
            return ast.literal_eval(n.value)
    raise SystemExit('BILDER fehlt in website/bilder.py, erst klären')


if __name__ == '__main__':
    print(len(lesen()), 'Einträge')
