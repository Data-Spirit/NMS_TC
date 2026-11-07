#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version du script : 1.0 (2026-11-07)
trans_script_5_test_mutations.py : vérifie que les scripts de contrôle n° 1 à 4 détectent bien des défauts connus.

Un contrôle vert avec un outil aveugle ne prouve rien. Ce banc injecte des défauts connus dans des COPIES du guide
(dossier temporaire du système ; le dépôt n'est jamais modifié), lance sur chaque copie le script censé le détecter,
et vérifie qu'il échoue. Il vérifie d'abord que le guide sain passe tous les contrôles.

Défauts injectés (chacun avec le script attendu) :
  M1 clé retirée d'une traduction (n° 1)           M8  onglet actif jamais annoncé, aria-selected figé (n° 2)
  M2 clé en trop dans une traduction (n° 1)        M9  copie : ✓ affiché même en cas d'échec (n° 2)
  M3 {paramètre} renommé (n° 1)                    M10 ?lang= ignoré (n° 3)
  M4 balise dangereuse dans une traduction (n° 1)  M11 langue mémorisée acceptée sans validation (n° 3)
  M5 JSON d'un bloc cassé (n° 1)                   M12 rendu du simulateur modifié (n° 4)
  M6 bloc de langue en double (n° 1)               M13 langue absente demandée au n° 4 (code 2 attendu)
  M7 bloc de langue mal formé (n° 1)

Les défauts de code (M8 à M12) remplacent un extrait exact du guide. Si le guide change et qu'un extrait n'est plus
trouvé, le banc le signale (« motif introuvable ») : c'est le banc qu'il faut alors mettre à jour, avec le guide.

Aucune valeur n'est écrite en dur côté langues : la langue source est fr (option --source), les langues de traduction
et les clés utilisées sont lues dans le fichier.

USAGE (depuis la racine du dépôt ; jsdom installé dans un dossier temporaire, NODE_PATH vers son node_modules)
  NODE_PATH=/chemin/node_modules python3 docs/scripts/trans_script_5_test_mutations.py LANG/NMS_txt_code.html
  Sous Windows : py -3 -X utf8 au lieu de python3 (sinon les accents s'affichent mal dans la console).

Code de sortie : 0 si chaque défaut est détecté, 1 sinon, 2 pour une erreur d'utilisation.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

try:
    sys.stdout.reconfigure(errors='replace')
except AttributeError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
S1, S2, S3, S4 = (os.path.join(HERE, n) for n in (
    'trans_script_1_check_keys.py', 'trans_script_2_test_behavior.js',
    'trans_script_3_test_robustness.js', 'trans_script_4_test_render.js'))
TAG = '<script type="application/json" id="i18n-%s">'
BLOCK_ID_RE = re.compile(r'^<script type="application/json" id="i18n-([\w-]+)">', re.M)
SIMPLE_KEY_RE = re.compile(r'^  "([a-z0-9_.]+)": "([^"<\\]*)",\n', re.M)
PARAM_KEY_RE = re.compile(r'^  "[a-z0-9_.]+": "[^"\n]*\{(\w+)\}[^"\n]*",?\n', re.M)

# Défauts de code : extrait exact du guide -> extrait fautif
CODE_MUTATIONS = [
    ('M8', "onglet actif jamais annoncé (aria-selected figé)", "b.setAttribute('aria-selected', on);", "b.setAttribute('aria-selected', false);", 's2'),
    ('M9', "copie : ✓ affiché même en cas d'échec", "btn.textContent = ok ? '✓' : '✗';", "btn.textContent = '✓';", 's2'),
    ('M10', "?lang= ignoré", "get('lang')", "get('langue')", 's3'),
    ('M11', "langue mémorisée acceptée sans validation", "const remembered = matchLanguage(saved);", "const remembered = saved;", 's3'),
    ('M12', "rendu du simulateur modifié", '<span class="sim-error">${html}</span>', '<span class="sim-error x">${html}</span>', 's4'),
]


def block_span(t, lang):
    i = t.index(TAG % lang)
    return i, t.index('</script>', i) + len('</script>')


def in_block(t, lang, fn):
    i, j = block_span(t, lang)
    new = fn(t[i:j])
    return None if new is None else t[:i] + new + t[j:]


def sub_once(pattern_re, repl, s):
    m = pattern_re.search(s)
    return None if not m else s[:m.start()] + repl(m) + s[m.end():]


def main():
    ap = argparse.ArgumentParser(description='Banc de défauts connus pour les scripts de contrôle n° 1 à 4 (lecture seule).')
    ap.add_argument('file')
    ap.add_argument('--source', default='fr')
    ap.add_argument('--keep', action='store_true', help='conserver le dossier des copies modifiées')
    a = ap.parse_args()
    try:
        g = open(a.file, encoding='utf-8', newline='').read()
    except (OSError, UnicodeDecodeError) as e:
        print('fichier introuvable ou illisible : %s (%s)' % (a.file, e), file=sys.stderr); sys.exit(2)
    ids = BLOCK_ID_RE.findall(g)
    tr = [i for i in ids if i != a.source]
    if a.source not in ids or not tr:
        print('il faut la langue source et au moins une traduction (blocs trouvés : %s)' % ', '.join(ids), file=sys.stderr); sys.exit(2)
    t1, t2 = tr[0], tr[-1]
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    tmp = tempfile.mkdtemp(prefix='nmstc_mutations_')
    sane = os.path.join(tmp, 'sain.html')
    open(sane, 'w', encoding='utf-8', newline='').write(g)

    def run(script, f, lang=None):
        if script == 's1': cmd = [sys.executable, S1, f, '--strict']
        elif script == 's2': cmd = ['node', S2, '--file', f, '--lang', lang or t1]
        elif script == 's3': cmd = ['node', S3, f]
        else: cmd = ['node', S4, sane, f, lang or t1]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
        except OSError as e:
            print('impossible de lancer %s : %s' % (cmd[0], e), file=sys.stderr); sys.exit(2)
        out = p.stdout + p.stderr
        first = next((l for l in out.splitlines() if l.startswith('FAIL')), out.strip().splitlines()[-1] if out.strip() else '')
        return p.returncode, ('FAIL' in out or 'ÉCHEC' in out), first

    fails = 0
    print('(langue source : %s ; traductions utilisées : %s, %s ; copies dans %s)\n' % (a.source, t1, t2, tmp))
    print('--- Le guide sain passe tous les contrôles')
    for s in ('s1', 's2', 's3', 's4'):
        rc, _, first = run(s, sane)
        print('%s %s : code %d%s' % ('PASS' if rc == 0 else 'FAIL', s, rc, '' if rc == 0 else ' : ' + first[:120]))
        if rc != 0: fails += 1
    if fails:
        print('\nLe guide sain ne passe pas : corriger le guide ou les scripts avant de tester les défauts.')
        shutil.rmtree(tmp, ignore_errors=True); sys.exit(1)

    mutations = []
    def k_remove(b): return sub_once(SIMPLE_KEY_RE, lambda m: '', b)
    def k_extra(b): return sub_once(SIMPLE_KEY_RE, lambda m: '  "zz.cle_en_trop": "x",\n' + m.group(0), b)
    def k_param(b): return sub_once(PARAM_KEY_RE, lambda m: m.group(0).replace('{%s}' % m.group(1), '{%s_x}' % m.group(1), 1), b)
    def k_evil(b): return sub_once(SIMPLE_KEY_RE, lambda m: '  "%s": "%s<img src=x onerror=alert(1)>",\n' % (m.group(1), m.group(2)), b)
    def k_json(b): return b.replace('"_meta":', '"_meta" "x":', 1) if '"_meta":' in b else None
    mutations.append(('M1', 'clé retirée (%s)' % t1, in_block(g, t1, k_remove), 's1'))
    mutations.append(('M2', 'clé en trop (%s)' % t2, in_block(g, t2, k_extra), 's1'))
    mutations.append(('M3', '{paramètre} renommé (%s)' % t1, in_block(g, t1, k_param), 's1'))
    mutations.append(('M4', 'balise dangereuse dans une traduction (%s)' % t1, in_block(g, t1, k_evil), 's1'))
    mutations.append(('M5', 'JSON cassé (%s)' % t2, in_block(g, t2, k_json), 's1'))
    i, j = block_span(g, t1)
    mutations.append(('M6', 'bloc de langue en double (%s)' % t1, g.replace('</body>', g[i:j] + '\n</body>', 1) if '</body>' in g else None, 's1'))
    tag2 = TAG % t2 + '\n'
    mutations.append(('M7', 'bloc de langue mal formé (%s)' % t2, g.replace(tag2, tag2 + 'x', 1) if tag2 in g else None, 's1'))
    for name, label, old, new, script in CODE_MUTATIONS:
        mutations.append((name, label, g.replace(old, new) if g.count(old) == 1 else None, script))

    print('\n--- Chaque défaut connu est détecté par le script attendu')
    for name, label, text, script in mutations:
        if text is None or text == g:
            print('FAIL %s %s : motif introuvable dans le guide (banc à mettre à jour)' % (name, label)); fails += 1; continue
        f = os.path.join(tmp, name + '.html')
        open(f, 'w', encoding='utf-8', newline='').write(text)
        rc, has_fail, first = run(script, f)
        ok = rc == 1 and has_fail
        print('%s %s %s : %s (code %d)%s' % ('PASS' if ok else 'FAIL', name, label, ('détecté par ' + script) if ok else ('NON détecté par ' + script), rc,
                                             '' if ok else ' : ' + first[:120]))
        if not ok: fails += 1
    rc, _, first = run('s4', sane, 'zz-inexistante')
    ok = rc == 2
    print('%s M13 langue absente demandée au n° 4 : %s (code %d)' % ('PASS' if ok else 'FAIL', 'refusée' if ok else 'acceptée', rc))
    if not ok: fails += 1

    if a.keep: print('\nCopies conservées dans : ' + tmp)
    else: shutil.rmtree(tmp, ignore_errors=True)
    print('\n' + ('%d ÉCHEC(S)' % fails if fails else 'TOUT OK'))
    print('Rappel : ce banc vérifie que les scripts réagissent à des défauts connus, pas qu\'ils voient tous les défauts possibles.')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
