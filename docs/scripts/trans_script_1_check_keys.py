#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version du script : 1.0 (2026-10-19)
trans_script_1_check_keys.py : contrôle des blocs de langue de NMS_txt_code.html et liste des clés à traduire.

Lecture seule : ce script ne modifie aucun fichier. Aucune valeur n'est écrite en dur : tout est calculé à partir
du fichier fourni.

CONTRÔLES (par défaut)
  - chaque bloc <script type="application/json" id="i18n-XX"> est un JSON valide, avec un "_meta" complet
    (native_name, flag, lang_code) ; une langue de traduction renseigne aussi ses paramètres de traduction
    (_meta.target : variant, tone, fidelity_style, aria_label_style) ;
  - toutes les clés utilisées par le HTML (data-i18n, data-i18n-attr) et par le JS (T('…'), TA('…'), clés dynamiques
    cat.<id>, flag.<x>, path.<x>) existent dans la langue source ;
  - chaque langue a exactement les clés de la source (manquantes : avertissement, ou échec avec --strict ; en trop : échec) ;
  - mêmes {paramètres}, mêmes balises et mêmes extraits <code> que la source pour chaque clé ;
  - uniquement des balises autorisées, aucun attribut dangereux (on…=, javascript:), aucun </script ;
  - le <title> statique est identique à la clé page.title de la source (valeur de secours sans JavaScript).

LISTE DES CLÉS À TRADUIRE (évite de relire tout le fichier)
  --todo LANG          affiche les clés à traduire pour LANG (toutes si le bloc n'existe pas encore), avec le texte source
  --since ANCIEN.html  compare la langue source à une version précédente du fichier : clés ajoutées, modifiées, supprimées ;
                       avec --todo, les clés modifiées dans la source et non retouchées dans LANG s'y ajoutent

USAGE
  python3 trans_script_1_check_keys.py NMS_txt_code.html --strict
  python3 trans_script_1_check_keys.py NMS_txt_code.html --since NMS_txt_code_precedent.html
  python3 trans_script_1_check_keys.py NMS_txt_code.html --todo es [--since NMS_txt_code_precedent.html]

Code de sortie : 0 si aucun FAIL, 1 sinon.
"""
import argparse, html as htmllib, io, json, re, signal, sys
from collections import Counter

try:   # sortie coupée par « head » ou « less » : pas de message d'erreur (inexistant sous Windows)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    pass

ALLOWED = {'a', 'b', 'br', 'code', 'em', 'i', 'span', 'strong'}
# Éléments d'un extrait <code> qu'une traduction a le droit de modifier (tout le reste doit rester identique) :
#  - les pseudo-noms pédagogiques de balise (ex. NAME_COLOR -> NOMBRE_COLOR en espagnol), à traduire de façon cohérente ;
#  - le mot-témoin du texte libre (classe syn-text), qui doit correspondre à la clé copy.template_word.
# À mettre à jour ici si le guide ajoute un nouveau pseudo-nom ou une nouvelle classe de ce type.
PSEUDO_NAMES = {'NAME_COLOR', 'NAME_ICON'}
FREE_CLASSES = {'syn-text'}
TEMPLATE_WORD_KEY = 'copy.template_word'
SPAN_RE = re.compile(r"<span class='([\w-]+)'>(.*?)</span>", re.S)
# Un bloc de langue commence toujours par « { » : cela écarte les simples mentions dans des commentaires de code.
BLOCK_RE = re.compile(r'<script type="application/json" id="i18n-([\w-]+)">(\s*\{.*?)</script>', re.S)
META_REQUIRED = ('native_name', 'flag', 'lang_code')
TARGET_REQUIRED = ('variant', 'tone', 'fidelity_style', 'aria_label_style')


def read(p):
    with io.open(p, encoding='utf-8', newline='') as f:
        return f.read()


def val(v):
    return ''.join(v) if isinstance(v, list) else v


def flat(block):
    return {k: val(v) for k, v in block.items() if k != '_meta'}


def tags_of(h):
    return re.findall(r'<[^>]+>', h)


def code_compatible(src_h, tr_h):
    """Les extraits <code> de la traduction sont identiques à ceux de la source, aux pseudo-noms et au mot-témoin près."""
    sb, tb = re.findall(r'<code>(.*?)</code>', src_h, re.S), re.findall(r'<code>(.*?)</code>', tr_h, re.S)
    if len(sb) != len(tb): return False
    for s, t in zip(sb, tb):
        ss, ts = SPAN_RE.findall(s), SPAN_RE.findall(t)
        if len(ss) != len(ts) or SPAN_RE.sub('§', s) != SPAN_RE.sub('§', t): return False
        for (sc, st), (tc, tt) in zip(ss, ts):
            if sc != tc: return False
            if sc in FREE_CLASSES: continue
            if st in PSEUDO_NAMES:
                if not re.fullmatch(r'[A-Z0-9_]+', tt): return False
                continue
            if st != tt: return False
    return True


def free_words(src, tr):
    """Traductions réellement employées pour les pseudo-noms et pour le mot-témoin : {mot source: {mots traduits}}."""
    out = {}
    for k in src:
        if k not in tr: continue
        for s, t in zip(re.findall(r'<code>(.*?)</code>', src[k], re.S), re.findall(r'<code>(.*?)</code>', tr[k], re.S)):
            for (sc, st), (tc, tt) in zip(SPAN_RE.findall(s), SPAN_RE.findall(t)):
                if sc in FREE_CLASSES: out.setdefault('<%s>' % sc, set()).add(tt)
                elif st in PSEUDO_NAMES: out.setdefault(st, set()).add(tt)
    return out


def load_blocks(html, report=None):
    langs = {}
    for lid, txt in BLOCK_RE.findall(html):
        try:
            langs[lid] = json.loads(txt)
        except ValueError as e:
            if report: report('FAIL', '%s : JSON invalide' % lid, str(e)[:120])
    return langs


def used_keys(html, source_keys):
    keys = set(re.findall(r'data-i18n="([^"]+)"', html))
    for pair in re.findall(r'data-i18n-attr="([^"]+)"', html):
        keys |= {p.split(':', 1)[1] for p in pair.split(';') if ':' in p}
    script = max(re.findall(r'<script>(.*?)</script>', html, re.S), key=len)
    keys |= {k for k in re.findall(r"\b(?:T|TA|i18nHas)\('([^']+)'", script) if not k.endswith('.')}   # « cat. » = préfixe dynamique
    keys |= {k for k in source_keys if "'%s'" % k in script}       # clé référencée via une variable
    cats = set(re.findall(r'^\s*\["[^"]+","[^"]*",(?:\d+(?:\.\d+)?,)?"([a-z0-9_]+)"', script, re.M))
    cats |= set(re.findall(r'^\s*\["[A-Z0-9_]+","[^"]*","([a-z0-9_]+)","', script, re.M))
    keys |= {'cat.' + c for c in cats}
    keys |= {'flag.' + f for f in set(re.findall(r'","(dup|warn|unk)"\],?\s*$', script, re.M))}
    keys |= {'path.' + p for p in set(re.findall(r'"@([a-z_]+)"', script))}
    if "'cat.' + cat + '.desc'" in script:
        keys |= {k for k in source_keys if re.fullmatch(r'cat\.[a-z0-9_]+\.desc', k)}
    return keys


def diff_since(src, psrc):
    return ([k for k in src if k not in psrc], [k for k in psrc if k not in src],
            [k for k in src if k in psrc and src[k] != psrc[k]])


def main():
    ap = argparse.ArgumentParser(description='Contrôle des blocs de langue et liste des clés à traduire (lecture seule).')
    ap.add_argument('file')
    ap.add_argument('--source', default='fr', help='code de la langue source (défaut : fr)')
    ap.add_argument('--strict', action='store_true', help='les clés manquantes deviennent des échecs')
    ap.add_argument('--since', help='version précédente du fichier : compare la langue source')
    ap.add_argument('--todo', metavar='LANG', help='liste les clés à traduire pour LANG avec le texte source')
    a = ap.parse_args()
    html = read(a.file)
    res = []
    def R(status, msg, detail=''): res.append((status, msg, detail))

    langs = load_blocks(html, R)
    ids = list(langs)
    if a.source not in langs:
        R('FAIL', 'langue source « %s » absente ou illisible' % a.source)
        return finish(res)
    src = flat(langs[a.source])

    prev_langs = load_blocks(read(a.since)) if a.since else None
    ch_added = ch_removed = ch_changed = []
    if prev_langs is not None:
        if a.source not in prev_langs:
            R('FAIL', 'langue source absente de la version précédente')
        else:
            ch_added, ch_removed, ch_changed = diff_since(src, flat(prev_langs[a.source]))
            R('INFO', 'langue source %s depuis la version précédente : %d clé(s) ajoutée(s), %d modifiée(s), %d supprimée(s)'
              % (a.source, len(ch_added), len(ch_changed), len(ch_removed)),
              ('ajoutées : %s' % ', '.join(ch_added[:8])) if ch_added else '')

    if a.todo:
        return todo(a, langs, src, prev_langs, ch_added, ch_changed)

    R('PASS' if len(ids) == len(set(ids)) and ids else 'FAIL', 'blocs de langue : %s' % (', '.join(ids) or 'aucun'))
    for lid, d in langs.items():
        meta = d.get('_meta', {})
        miss = [f for f in META_REQUIRED if f not in meta]
        bad = miss or meta.get('lang_code') != lid
        R('FAIL' if bad else 'PASS', '%s : _meta complet (nom, drapeau, code)' % lid,
          ('champs manquants : %s' % miss) if miss else ('lang_code « %s » ≠ id' % meta.get('lang_code') if bad else ''))
        if lid != a.source:
            tmiss = [f for f in TARGET_REQUIRED if f not in meta.get('target', {})]
            R('PASS' if not tmiss else 'WARN', '%s : paramètres de traduction renseignés (_meta.target)' % lid, ', '.join(tmiss))
    mt = re.search(r'<title>(.*?)</title>', html, re.S)
    R('PASS' if mt and htmllib.unescape(mt.group(1)).strip() == src.get('page.title', '').strip() else 'FAIL',
      '<title> statique identique à la clé page.title de la source (valeur de secours sans JavaScript)',
      '' if mt else '<title> absent')
    used = used_keys(html, src)
    absent = sorted(k for k in used if k not in src)
    R('PASS' if not absent else 'FAIL', 'clés utilisées par le HTML et le JS présentes dans la source (%d clés)' % len(used), ', '.join(absent[:6]))
    unused = sorted(k for k in src if k not in used)
    R('PASS' if not unused else 'WARN', 'clés de la source jamais utilisées', ', '.join(unused[:6]))
    for lid, d in langs.items():
        tr = flat(d)
        miss = sorted(set(src) - set(tr)); extra = sorted(set(tr) - set(src))
        if lid != a.source:
            R('PASS' if not miss else ('FAIL' if a.strict else 'WARN'),
              '%s : clés manquantes (repli sur %s à l\'affichage) : %d / %d' % (lid, a.source, len(miss), len(src)), ', '.join(miss[:6]))
            R('PASS' if not extra else 'FAIL', '%s : clés en trop (absentes de la source)' % lid, ', '.join(extra[:6]))
            if prev_langs is not None and ch_changed:
                ptr = flat(prev_langs.get(lid, {}))
                stale = [k for k in ch_changed if k in tr and k in ptr and tr[k] == ptr[k]]
                R('PASS' if not stale else ('FAIL' if a.strict else 'WARN'),
                  '%s : clés modifiées dans la source mais pas retouchées dans la traduction : %d / %d' % (lid, len(stale), len(ch_changed)),
                  ', '.join(stale[:6]))
        bad_ph = [k for k in tr if k in src and Counter(re.findall(r'\{(\w+)\}', tr[k])) != Counter(re.findall(r'\{(\w+)\}', src[k]))]
        R('PASS' if not bad_ph else 'FAIL', '%s : mêmes {paramètres} que la source' % lid, ', '.join(bad_ph[:6]))
        bad_sk = [k for k in tr if k in src and (tags_of(tr[k]) != tags_of(src[k]) or not code_compatible(src[k], tr[k]))]
        R('PASS' if not bad_sk else 'FAIL', '%s : mêmes balises et mêmes extraits <code> que la source (pseudo-noms et mot-témoin exceptés)' % lid, ', '.join(bad_sk[:6]))
        if lid != a.source:
            fw = free_words(src, tr)
            incoh = ['%s -> %s' % (k, sorted(v)) for k, v in fw.items() if len(v) > 1]
            R('PASS' if not incoh else 'FAIL', '%s : pseudo-noms et mot-témoin traduits de façon cohérente partout' % lid, '; '.join(incoh))
            tw = fw.get('<syn-text>')
            if tw and TEMPLATE_WORD_KEY in tr:
                R('PASS' if tw == {tr[TEMPLATE_WORD_KEY]} else 'FAIL',
                  '%s : le mot-témoin de l\'aide de syntaxe est identique à la clé %s' % (lid, TEMPLATE_WORD_KEY),
                  'aide de syntaxe : %s ; clé : %s' % (sorted(tw), tr[TEMPLATE_WORD_KEY]) if tw != {tr[TEMPLATE_WORD_KEY]} else '')
        forbidden, dangerous = [], []
        for k, v in tr.items():
            for t in re.findall(r'<\s*/?\s*([a-zA-Z][\w-]*)', v):
                if t.lower() not in ALLOWED: forbidden.append('%s:<%s>' % (k, t))
            if re.search(r'\son\w+\s*=|javascript:', v, re.I): dangerous.append(k)
        R('PASS' if not forbidden else 'FAIL', '%s : uniquement des balises autorisées' % lid, ', '.join(forbidden[:6]))
        R('PASS' if not dangerous else 'FAIL', '%s : aucun attribut dangereux (on…=, javascript:)' % lid, ', '.join(dangerous[:6]))
    for lid, txt in BLOCK_RE.findall(html):
        if '</script' in txt.lower():
            R('FAIL', '%s : séquence </script interdite dans un bloc' % lid)
    return finish(res)


def todo(a, langs, src, prev_langs, ch_added, ch_changed):
    tr = flat(langs[a.todo]) if a.todo in langs else {}
    missing = [k for k in src if k not in tr]
    stale = []
    if prev_langs is not None and a.todo in langs:
        ptr = flat(prev_langs.get(a.todo, {}))
        stale = [k for k in ch_changed if k in tr and k in ptr and tr[k] == ptr[k]]
    keys = [k for k in src if k in set(missing) | set(stale)]
    print('# Clés à traduire pour « %s » : %d sur %d (%d manquantes, %d modifiées dans la source et non retouchées)%s'
          % (a.todo, len(keys), len(src), len(missing), len(stale), '' if a.todo in langs else ' ; bloc inexistant : tout est à traduire'))
    for k in keys:
        print('%s\t%s%s' % (k, src[k], '\t[MODIFIÉE]' if k in stale else ''))
    sys.exit(0)


def finish(res):
    for s, m, d in res: print('%s %s%s' % (s, m, (' : ' + d) if d else ''))
    c = Counter(s for s, _, _ in res)
    print('\nRésumé : %d PASS, %d FAIL, %d WARN' % (c['PASS'], c['FAIL'], c['WARN']))
    print('Rappel : ces contrôles garantissent la cohérence des clés, pas la qualité des traductions ni le rendu visuel.')
    sys.exit(0 if c['FAIL'] == 0 else 1)


if __name__ == '__main__':
    main()
