"""Konzept-Board als Seite im Kleid der Website: liest _kette/06-konzepter/KONZEPT-2026-10-28.md und baut konzept.html (nur lokal, nie zum Kunden)."""
import html, os, re
from bau import rahmen, HIER, E

QUELLE = os.path.join(HIER, '..', '_kette', '06-konzepter', 'KONZEPT-2026-10-28.md')


def inline(t):
    t = E(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`(.+?)`', r'<code>\1</code>', t)
    return t


def md_html(src):
    out, tabelle, liste = [], [], False
    def tabelle_aus():
        if not tabelle: return
        kopf, *zeilen = tabelle
        out.append('<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (
            ''.join('<th>%s</th>' % inline(c) for c in kopf), ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in z) for z in zeilen)))
        tabelle.clear()
    for z in src.split('\n'):
        s = z.strip()
        if s.startswith('|'):
            zellen = [c.strip() for c in s.strip('|').split('|')]
            if set(''.join(zellen)) <= set('-: '): continue
            tabelle.append(zellen); continue
        tabelle_aus()
        if s.startswith('- '):
            if not liste: out.append('<ul>'); liste = True
            out.append('<li>%s</li>' % inline(s[2:])); continue
        if liste: out.append('</ul>'); liste = False
        if s.startswith('# '): continue
        if s.startswith('## '): out.append('<h2 class="titel">%s</h2>' % inline(s[3:])); continue
        if s: out.append('<p>%s</p>' % inline(s))
    tabelle_aus()
    if liste: out.append('</ul>')
    return '\n'.join(out)


def seite():
    src = open(QUELLE).read()
    stil = '''<style>.kb{max-width:1100px}.kb h2{font-size:clamp(26px,2.6vw,36px);margin:48px 0 14px}.kb p{color:var(--text2);margin-bottom:12px;max-width:80ch}.kb b{color:var(--text);font-weight:400}
.kb table{width:100%;border-collapse:collapse;font-size:14px;margin:14px 0 24px}.kb th,.kb td{text-align:left;vertical-align:top;padding:10px 12px 10px 0;border-top:1px solid var(--gold-ll);color:var(--text2)}.kb th{color:var(--gold);font:500 11px/1.4 var(--lauf);letter-spacing:.14em;text-transform:uppercase}
.kb ul{padding-left:18px;color:var(--text2)}.kb li{margin-bottom:8px}.kb code{font-size:13px;color:var(--gold)}@media (max-width:900px){.kb table{display:block;overflow-x:auto;white-space:nowrap}.kb td,.kb th{white-space:normal;min-width:160px}}</style>'''
    inhalt = '<section class="kap" style="padding-top:150px"><div class="innen kb"><div class="kz"><span class="uhr">Konzept-Board</span><i></i><span class="was">intern, 28.10.2026</span></div><h1 class="titel t-kap">Walk on the Wild Side · der Neubau.</h1>%s</div></section>' % md_html(src)
    return rahmen('Konzept · Walk on the Wild Side', 'Konzept-Board des Neubaus', stil + inhalt, '', 'konzept')


if __name__ == '__main__':
    open(os.path.join(HIER, 'konzept.html'), 'w').write(seite())
    print('konzept.html')
