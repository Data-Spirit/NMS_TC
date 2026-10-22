#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version du script : 1.1 (2026-10-17)
(1.1 : renommé trans_script_4_*, aucune modification de logique)
trans_script_4_verify_symmetry.py : vérification de symétrie entre le guide source (FR) et une traduction.

Ce script NE TRADUIT RIEN et NE MODIFIE AUCUN FICHIER. Il compare deux fichiers HTML et
signale tout écart de structure, de code ou de données. Les valeurs attendues sont toujours
CALCULÉES à partir des fichiers fournis (aucun nombre de fonctions, de couleurs ou d'icônes
n'est écrit en dur), donc le guide peut évoluer sans produire de fausse alerte.

Usage (stdlib Python 3 uniquement) :

  # Traduction complète : la traduction reflète-t-elle exactement la source ?
  python3 trans_script_4_verify_symmetry.py --source NMS_txt_code_FR.html --translation NMS_txt_code_EN.html --lang en

  # Mise à jour incrémentale : en plus, les modifications entre deux versions sont-elles
  # identiques (positions et tailles) dans les deux langues ?
  python3 trans_script_4_verify_symmetry.py --source FR_v1.3.html --translation EN_v1.3.html --lang en \
      --prev-source FR_v1.1.html --prev-translation EN_v1.1.html \
      --residual-pattern "[àâçéèêëîïôùûü]|\\b(le|la|les|une|des)\\b"

  # Ajouter --subs fichier.json pour contrôler aussi les chaînes d'interface validées
  # (et reprendre automatiquement le motif de langue résiduelle du fichier).
  # Ajouter --tools pour lancer aussi node --check et html-validate quand ils sont disponibles.

Code de sortie : 0 si aucun FAIL, 1 sinon. Les WARN demandent une relecture humaine.

Ce qu'il faut mettre à jour ici si le guide change de nature : voir trans_script_0_README.md
(tableau « Si ceci change, mettre à jour cela »). Les constantes concernées sont
DATA_SCHEMA, FROZEN_BLOCKS, FIELD_AWARE_BLOCKS et TRANSLATED_BLOCKS ci-dessous.
"""
import argparse
import difflib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

# --------------------------------------------------------------------------------------
# Configuration structurelle (à adapter uniquement si le format des données change)
# --------------------------------------------------------------------------------------
# Position du champ « catégorie » dans chaque ligne des tableaux de données.
DATA_SCHEMA = {"COLORS": {"cat": 3}, "ICONS": {"cat": 2}}
# Blocs qui ne doivent jamais différer d'un seul caractère entre source et traduction.
FROZEN_BLOCKS = ["ICON_DATA", "CONTAINER_EXAMPLES", "ICON_ALREADY_COLORED", "SPECTRUM_ORDER"]
# Blocs dont seuls les champs textuels (non techniques) peuvent différer.
FIELD_AWARE_BLOCKS = ["COLORS", "ICONS"]
# Blocs entièrement traduits : seul le nombre de chaînes est exigé ici ; leur cohérence
# (clés, catégories) est contrôlée par des vérifications dédiées plus bas.
TRANSLATED_BLOCKS = ["CATEGORY_DESCRIPTIONS", "FLAG_LABELS"]
# Une chaîne est « technique » (donc jamais traduite) si elle correspond à ce motif :
# tag NMS en MAJUSCULES, code hex, chemin .DDS/.png, clé de badge, ou chaîne vide.
TECH_RE = re.compile(r"^(?:[A-Z][A-Z0-9_]*|#[0-9A-Fa-f]{3,8}|[\w./\-]+\.(?:DDS|dds|png|PNG)|dup|warn|unk|)$")


# --------------------------------------------------------------------------------------
# Lecture et extraction
# --------------------------------------------------------------------------------------
def read(path):
    with io.open(path, encoding="utf-8", newline="") as f:
        return f.read()


def md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def split_lines(text):
    return text.split("\n")


def script_of(text):
    blocks = re.findall(r"<script[^>]*>(.*?)</script>", text, re.S)
    return max(blocks, key=len) if blocks else ""


def css_of(text):
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S))


def strip_css_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def js_normalized(text):
    """JS sans ICON_DATA, sans commentaires, avec toutes les chaînes remplacées par un jeton.
    Deux fichiers qui ne diffèrent que par leurs textes donnent le même résultat."""
    j = script_of(text)
    j = re.sub(r"const ICON_DATA = \{.*?\n\};", "", j, flags=re.S)
    j = re.sub(r"//[^\n]*", "", j)
    j = re.sub(r"/\*.*?\*/", "", j, flags=re.S)
    j = re.sub(r"'(?:[^'\\\n]|\\.)*'", "S", j)
    j = re.sub(r"`(?:[^`\\]|\\.)*`", "T", j)
    j = re.sub(r'"(?:[^"\\\n]|\\.)*"', "S", j)
    return re.sub(r"\s+", " ", j)


def function_names(text):
    return re.findall(r"^\s*(?:async )?function (\w+)", script_of(text), re.M)


def html_ids(text):
    return sorted(re.findall(r'\bid="([^"]+)"', text))


def js_referenced_ids(text):
    return set(re.findall(r"getElementById\('([^']+)'\)", script_of(text)))


def html_tag_counts(text):
    return Counter(re.findall(r"<(section|div|table|thead|tbody|tr|th|td|h1|h2|h3|ul|ol|li|p|button|input|select|label|span|nav|header|footer|main|code|strong|em|a)\b", text))


MARK_RE = re.compile(
    r"^\s*(?:function |async function |const [A-Z_]+ = |<section|<div class=\"tab-panel|<header|<nav|<footer|"
    r"<script|</script|<style|</style|[.#][\w-][^;{}]*\{)"
)


def structural_markers(text):
    return [i + 1 for i, l in enumerate(split_lines(text)) if MARK_RE.match(l)]


def extract_block(js, name):
    """Retourne le texte du bloc `const NAME = ...` (tableau, objet ou new Set([...]))."""
    m = re.search(r"^const %s = " % re.escape(name), js, re.M)
    if not m:
        return None
    i, depth, started, n = m.end(), 0, False, len(js)
    while i < n:
        c = js[i]
        if c in "\"'`":
            q = c
            i += 1
            while i < n and js[i] != q:
                if js[i] == "\\":
                    i += 1
                i += 1
        elif js.startswith("//", i):
            j = js.find("\n", i)
            i = n if j < 0 else j
            continue
        elif js.startswith("/*", i):
            j = js.find("*/", i)
            i = n if j < 0 else j + 1
        elif c in "[{(":
            depth += 1
            started = True
        elif c in "]})":
            depth -= 1
            if started and depth == 0:
                return js[m.start(): i + 1]
        i += 1
    return None


def block_names(js):
    return re.findall(r"^const ([A-Z][A-Z0-9_]*) = (?:\[|\{|new Set\()", js, re.M)


def strings_in(block):
    out, i, n = [], 0, len(block)
    while i < n:
        if block.startswith("//", i):
            j = block.find("\n", i)
            i = n if j < 0 else j
            continue
        if block.startswith("/*", i):
            j = block.find("*/", i)
            i = n if j < 0 else j + 2
            continue
        c = block[i]
        if c in "\"'":
            j, buf = i + 1, []
            while j < n and block[j] != c:
                if block[j] == "\\":
                    buf.append(block[j:j + 2])
                    j += 2
                    continue
                buf.append(block[j])
                j += 1
            out.append("".join(buf))
            i = j + 1
            continue
        i += 1
    return out


def parse_rows(block):
    rows = []
    for line in block.split("\n"):
        s = line.strip()
        if s.startswith("//"):
            continue
        m = re.match(r"^(\[.*\]),?$", s)
        if m:
            rows.append(json.loads(m.group(1)))
    return rows


# --------------------------------------------------------------------------------------
# Contrôles : chaque fonction renvoie une liste de (statut, libellé, détail)
# statuts : PASS, FAIL, WARN, INFO, SKIP
# --------------------------------------------------------------------------------------
def R(status, label, detail=""):
    return (status, label, detail)


def check_data_blocks(src, tr):
    res = []
    sj, tj = script_of(src), script_of(tr)
    names_s, names_t = block_names(sj), block_names(tj)
    if names_s != names_t:
        res.append(R("FAIL", "blocs de données : mêmes noms, même ordre", "source=%s | traduction=%s" % (names_s, names_t)))
        return res
    res.append(R("PASS", "blocs de données : mêmes noms et même ordre (%d blocs)" % len(names_s)))
    cat_map = {}
    cat_conflicts = []
    for name in names_s:
        bs, bt = extract_block(sj, name), extract_block(tj, name)
        if name in FROZEN_BLOCKS:
            ok = bs == bt
            res.append(R("PASS" if ok else "FAIL", "%s strictement identique (bloc gelé)" % name))
        elif name in FIELD_AWARE_BLOCKS:
            ss, st = strings_in(bs), strings_in(bt)
            if len(ss) != len(st):
                res.append(R("FAIL", "%s : même nombre de champs texte" % name, "%d / %d" % (len(ss), len(st))))
                continue
            bad = [(i, a, b) for i, (a, b) in enumerate(zip(ss, st)) if TECH_RE.match(a) and a != b]
            res.append(R("PASS" if not bad else "FAIL",
                         "%s : %d champs, tous les champs techniques (tag, hex, chemin, badge) intacts" % (name, len(ss)),
                         "" if not bad else "écarts : %s" % bad[:5]))
            if name in DATA_SCHEMA:
                ci = DATA_SCHEMA[name]["cat"]
                try:
                    rs, rt = parse_rows(bs), parse_rows(bt)
                except ValueError as e:
                    res.append(R("FAIL", "%s : lignes lisibles" % name, str(e)))
                    continue
                if len(rs) != len(rt):
                    res.append(R("FAIL", "%s : même nombre de lignes" % name, "%d / %d" % (len(rs), len(rt))))
                    continue
                for a, b in zip(rs, rt):
                    if len(a) != len(b) or any(x != y for k, (x, y) in enumerate(zip(a, b)) if TECH_RE.match(str(x)) and k != ci):
                        cat_conflicts.append("ligne %s" % a[0])
                    ca, cb = a[ci], b[ci]
                    if cat_map.setdefault(ca, cb) != cb:
                        cat_conflicts.append("catégorie « %s » traduite de deux façons : « %s » et « %s »" % (ca, cat_map[ca], cb))
        elif name in TRANSLATED_BLOCKS:
            ss, st = strings_in(bs), strings_in(bt)
            res.append(R("PASS" if len(ss) == len(st) else "FAIL",
                         "%s : bloc traduit, même nombre de chaînes (%d)" % (name, len(ss)) if len(ss) == len(st)
                         else "%s : même nombre de chaînes" % name,
                         "" if len(ss) == len(st) else "%d / %d" % (len(ss), len(st))))
        else:
            if bs == bt:
                res.append(R("PASS", "%s identique" % name))
            else:
                ss, st = strings_in(bs), strings_in(bt)
                if len(ss) == len(st):
                    res.append(R("WARN", "%s : bloc non configuré, textes différents (même nombre de chaînes)" % name,
                                 "à relire manuellement ; ajouter le bloc à FROZEN_BLOCKS ou FIELD_AWARE_BLOCKS si besoin"))
                else:
                    res.append(R("FAIL", "%s : même nombre de chaînes" % name, "%d / %d" % (len(ss), len(st))))
    res.append(R("PASS" if not cat_conflicts else "FAIL",
                 "catégories : traduction cohérente partout (%d catégories distinctes)" % len(cat_map),
                 "; ".join(cat_conflicts[:5])))
    # Clés de CATEGORY_DESCRIPTIONS = catégories réellement utilisées dans ICONS (règle §C du prompt)
    bd_t = extract_block(tj, "CATEGORY_DESCRIPTIONS")
    bd_s = extract_block(sj, "CATEGORY_DESCRIPTIONS")
    if bd_t is not None and bd_s is not None and "ICONS" in names_t:
        keys_t = re.findall(r'^\s*"([^"]+)"\s*:', bd_t, re.M)
        keys_s = re.findall(r'^\s*"([^"]+)"\s*:', bd_s, re.M)
        icon_cats_t = {r[DATA_SCHEMA["ICONS"]["cat"]] for r in parse_rows(extract_block(tj, "ICONS"))}
        icon_cats_s = {r[DATA_SCHEMA["ICONS"]["cat"]] for r in parse_rows(extract_block(sj, "ICONS"))}
        miss_t = [k for k in keys_t if k not in icon_cats_t]
        miss_s = [k for k in keys_s if k not in icon_cats_s]
        mapped = [cat_map.get(k) for k in keys_s]
        ok = not miss_t and mapped == keys_t
        res.append(R("PASS" if ok else "FAIL",
                     "CATEGORY_DESCRIPTIONS : clés = catégories réellement utilisées dans ICONS, traduites à l'identique",
                     "" if ok else "clés absentes d'ICONS (traduction)=%s ; correspondance attendue=%s ; trouvée=%s" % (miss_t, mapped, keys_t)))
        if miss_s:
            res.append(R("WARN", "CATEGORY_DESCRIPTIONS (source) : clés absentes d'ICONS", str(miss_s)))
    # Badges : mêmes clés
    fl_s, fl_t = extract_block(sj, "FLAG_LABELS"), extract_block(tj, "FLAG_LABELS")
    if fl_s and fl_t:
        ks, kt = re.findall(r"(\w+)\s*:", fl_s), re.findall(r"(\w+)\s*:", fl_t)
        res.append(R("PASS" if ks == kt else "FAIL", "FLAG_LABELS : mêmes clés (%s)" % ", ".join(ks)))
    return res


def check_alignment(src, tr):
    """Contrôles de symétrie structurelle entre une source et une traduction."""
    res = []
    ls, lt = split_lines(src), split_lines(tr)
    res.append(R("PASS" if len(ls) == len(lt) else "FAIL", "même nombre de lignes", "%d / %d" % (len(ls) - 1, len(lt) - 1)))
    ms, mt = structural_markers(src), structural_markers(tr)
    if ms == mt:
        res.append(R("PASS", "%d repères structurels aux mêmes numéros de ligne" % len(ms)))
    else:
        first = next((a for a, b in zip(ms, mt) if a != b), None)
        res.append(R("FAIL", "repères structurels aux mêmes numéros de ligne", "premier écart autour de la ligne %s ; %d / %d repères" % (first, len(ms), len(mt))))
    cs, ct = html_tag_counts(src), html_tag_counts(tr)
    res.append(R("PASS" if cs == ct else "FAIL", "balises HTML : mêmes comptes",
                 "" if cs == ct else str({k: (cs[k], ct[k]) for k in set(cs) | set(ct) if cs[k] != ct[k]})))
    res.append(R("PASS" if strip_css_comments(css_of(src)) == strip_css_comments(css_of(tr)) else "FAIL",
                 "CSS identique hors commentaires"))
    fs, ft = function_names(src), function_names(tr)
    res.append(R("PASS" if fs == ft else "FAIL", "fonctions JS : mêmes noms, même ordre (%d)" % len(fs),
                 "" if fs == ft else "différences : %s" % sorted(set(fs) ^ set(ft))))
    ids_s, ids_t = html_ids(src), html_ids(tr)
    res.append(R("PASS" if ids_s == ids_t else "FAIL", "id HTML identiques (%d)" % len(ids_s)))
    missing = js_referenced_ids(tr) - set(ids_t)
    res.append(R("PASS" if not missing else "FAIL", "chaque getElementById du JS correspond à un id du HTML", str(sorted(missing))))
    res.append(R("PASS" if js_normalized(src) == js_normalized(tr) else "FAIL",
                 "JS identique hors chaînes et commentaires"))
    res.extend(check_data_blocks(src, tr))
    return res


def check_hygiene(tr, lang, src=None):
    res = []
    m = re.search(r'<html lang="([^"]*)"', tr)
    if lang:
        res.append(R("PASS" if m and m.group(1).lower() == lang.lower() else "FAIL", "attribut <html lang> = « %s »" % lang,
                     "" if m and m.group(1).lower() == lang.lower() else "trouvé : %s" % (m.group(1) if m else "absent")))
    res.append(R("PASS" if "\t" not in tr else "FAIL", "aucune tabulation"))
    if src is not None:
        vs = re.search(r"Version\s*:?\s*(\d+(?:\.\d+)*)", src)
        vt = re.search(r"Version\s*:?\s*(\d+(?:\.\d+)*)", tr)
        if vs and vt:
            res.append(R("PASS" if vs.group(1) == vt.group(1) else "FAIL", "numéro de version de l'en-tête identique (source %s / traduction %s)" % (vs.group(1), vt.group(1))))
        else:
            res.append(R("WARN", "numéro de version de l'en-tête introuvable"))
    return res


def check_incremental(prev_src, src, prev_tr, tr, residual_pattern=None, keep_as_is=()):
    res = []
    def hunks(a, b):
        sm = difflib.SequenceMatcher(None, split_lines(a), split_lines(b), autojunk=False)
        return [o for o in sm.get_opcodes() if o[0] != "equal"]
    hs, ht = hunks(prev_src, src), hunks(prev_tr, tr)
    if hs == ht:
        res.append(R("PASS", "les %d modifications entre versions ont exactement les mêmes positions et tailles dans les deux langues" % len(hs)))
    else:
        res.append(R("FAIL", "modifications entre versions identiques dans les deux langues", "source : %d modifications, traduction : %d" % (len(hs), len(ht))))
    # Blocs de données : inchangés dans la source => inchangés dans la traduction
    ps, pt, cs, ct = script_of(prev_src), script_of(prev_tr), script_of(src), script_of(tr)
    bad = []
    for name in block_names(cs):
        if extract_block(ps, name) == extract_block(cs, name) and extract_block(pt, name) != extract_block(ct, name):
            bad.append(name)
    res.append(R("PASS" if not bad else "FAIL", "blocs de données non modifiés dans la source : intacts dans la traduction", str(bad)))
    # Lignes ajoutées : pas de langue source résiduelle
    old = set(split_lines(prev_tr))
    added = [l for l in split_lines(tr) if l not in old]
    res.append(R("INFO", "%d lignes nouvelles ou modifiées dans la traduction" % len(added)))
    trailing = [l for l in added if l != l.rstrip()]
    res.append(R("PASS" if not trailing else "FAIL", "aucun espace de fin de ligne ajouté", str(trailing[:3])))
    if residual_pattern:
        rx = re.compile(residual_pattern, re.I)
        hits = [l for l in added if rx.search(l) and l not in keep_as_is]
        res.append(R("PASS" if not hits else "FAIL", "aucune langue source résiduelle dans les lignes ajoutées", "; ".join(h.strip()[:100] for h in hits[:5])))
    else:
        res.append(R("WARN", "recherche de langue source résiduelle non effectuée (aucun --residual-pattern fourni)"))
    res.append(R("PASS" if tr[-15:] == prev_tr[-15:] else "FAIL", "fin de fichier identique à la traduction précédente"))
    return res


def ui_fragments(ui, extra=()):
    """Fragments fixes des chaînes d'interface attendues (les {placeholders} sont écartés).
    Les messages « msg_* » sont souvent assemblés en plusieurs morceaux dans le code : ils
    ne sont pas cherchés en entier, mais via la liste « message_fragments » du fichier de
    substitutions (fragments déclarés explicitement par la personne qui valide)."""
    frags = [("message_fragments", f) for f in extra]
    for k, v in ui.items():
        if k.startswith("_") or k.startswith("msg_") or not isinstance(v, str):
            continue
        for part in re.split(r"\{[^}]*\}", v):
            part = part.strip()
            if len(part) >= 3:
                frags.append((k, part))
    return frags


def check_ui_strings(tr, subs):
    """Chaque chaîne d'interface validée dans le fichier de substitutions doit figurer dans la traduction."""
    missing = [(k, f) for k, f in ui_fragments(subs.get("ui_strings", {}), subs.get("message_fragments", [])) if f not in tr]
    n = len(ui_fragments(subs.get("ui_strings", {}), subs.get("message_fragments", [])))
    return [R("PASS" if not missing else "FAIL", "chaînes d'interface validées présentes dans la traduction (%d fragments)" % n, str(missing[:6]) if missing else "")]


def check_tools(tr):
    res = []
    js = script_of(tr)
    node = shutil.which("node")
    with tempfile.TemporaryDirectory() as d:
        if node:
            p = os.path.join(d, "script.js")
            with io.open(p, "w", encoding="utf-8") as f:
                f.write(js)
            r = subprocess.run([node, "--check", p], capture_output=True, text=True)
            res.append(R("PASS" if r.returncode == 0 else "FAIL", "node --check sur le JS extrait", r.stderr.strip()[:300]))
        else:
            res.append(R("SKIP", "node --check", "node introuvable"))
        hv = shutil.which("html-validate")
        npx = shutil.which("npx")
        if hv or npx:
            p = os.path.join(d, "page.html")
            with io.open(p, "w", encoding="utf-8") as f:
                f.write(tr)
            with io.open(os.path.join(d, ".htmlvalidate.json"), "w") as f:
                f.write('{ "extends": ["html-validate:recommended"] }')
            cmd = [hv, p] if hv else [npx, "--no-install", "html-validate", p]
            # NMSTC_TOOLS_DIR : dossier contenant node_modules (où html-validate a été installé avec npm)
            cwd = os.environ.get("NMSTC_TOOLS_DIR") or d
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=180)
                err = ((r.stderr or "") + (r.stdout or "")).lower()
                if r.returncode == 0:
                    res.append(R("PASS", "html-validate (preset recommended)"))
                elif any(k in err for k in ("not found", "could not determine", "missing packages", "canceled", "enoent")):
                    res.append(R("SKIP", "html-validate", "non installé : npm i html-validate, puis définir NMSTC_TOOLS_DIR sur le dossier qui contient node_modules"))
                else:
                    res.append(R("FAIL", "html-validate (preset recommended)", (r.stdout + r.stderr).strip()[:400]))
            except Exception as e:  # pragma: no cover
                res.append(R("SKIP", "html-validate", str(e)))
        else:
            res.append(R("SKIP", "html-validate", "npx introuvable"))
    return res


def report(results):
    sym = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN", "INFO": "INFO", "SKIP": "SKIP"}
    for status, label, detail in results:
        print("%s %s%s" % (sym[status], label, (" : " + detail) if detail else ""))
    counts = Counter(s for s, _, _ in results)
    print("\nRésumé : %d PASS, %d FAIL, %d WARN, %d SKIP" % (counts["PASS"], counts["FAIL"], counts["WARN"], counts["SKIP"]))
    return counts["FAIL"] == 0


def main():
    ap = argparse.ArgumentParser(description="Vérifie la symétrie entre le guide source et une traduction (lecture seule).")
    ap.add_argument("--source", required=True, help="guide source (ex. NMS_txt_code_FR.html)")
    ap.add_argument("--translation", required=True, help="traduction à vérifier")
    ap.add_argument("--lang", help="valeur attendue de <html lang> (ex. en)")
    ap.add_argument("--prev-source", help="version précédente de la source (mode incrémental)")
    ap.add_argument("--prev-translation", help="version précédente de la traduction (mode incrémental)")
    ap.add_argument("--residual-pattern", help="regex de la langue source à traquer dans les lignes ajoutées")
    ap.add_argument("--subs", help="fichier de substitutions validé : active le contrôle des chaînes d'interface et fournit le motif de langue résiduelle")
    ap.add_argument("--tools", action="store_true", help="lance aussi node --check et html-validate si disponibles")
    a = ap.parse_args()
    subs = json.load(io.open(a.subs, encoding="utf-8")) if a.subs else None
    if subs and not a.residual_pattern:
        a.residual_pattern = subs.get("residual_pattern")
    src, tr = read(a.source), read(a.translation)
    print("source      : %s (%d lignes, md5 %s)" % (os.path.basename(a.source), len(split_lines(src)) - 1, md5(src)))
    print("traduction  : %s (%d lignes, md5 %s)\n" % (os.path.basename(a.translation), len(split_lines(tr)) - 1, md5(tr)))
    results = check_alignment(src, tr) + check_hygiene(tr, a.lang, src)
    if a.prev_source and a.prev_translation:
        results += check_incremental(read(a.prev_source), src, read(a.prev_translation), tr, a.residual_pattern,
                                     set(subs.get("keep_as_is", [])) if subs else ())
    elif a.prev_source or a.prev_translation:
        results.append(R("FAIL", "mode incrémental", "fournir --prev-source ET --prev-translation"))
    if subs:
        results += check_ui_strings(tr, subs)
    if a.tools:
        results += check_tools(tr)
    ok = report(results)
    print("\nRappel : ces contrôles garantissent la symétrie, pas la qualité de la traduction ni le rendu visuel (à valider à l'oeil).")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
