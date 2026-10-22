#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version du script : 1.1 (2026-10-17)
(1.1 : renommé trans_script_2_*, ne crée plus jamais de dossier __pycache__)
trans_script_2_update_translation.py : répercute dans une traduction existante les modifications
apportées au guide source entre deux versions (mode « mise à jour incrémentale »).

CE SCRIPT NE TRADUIT RIEN. Les textes ajoutés viennent exclusivement du fichier de
substitutions que la personne a validé (fichiers trans_script_1_substitutions_*.json). Le script se
contente de :
  1. calculer les modifications entre l'ancienne et la nouvelle source ;
  2. vérifier que la traduction existante est alignée avec l'ancienne source ;
  3. appliquer chaque modification au MÊME endroit dans la traduction ;
  4. vérifier le résultat avec trans_script_4_verify_symmetry.py.

IL S'ARRÊTE (code de sortie 2) au moindre doute, sans rien écrire :
  - la traduction n'est pas alignée avec l'ancienne source (retraduction complète à prévoir) ;
  - une ligne à remplacer n'est pas identique dans les deux langues ;
  - une substitution ne s'applique à aucune ligne (fichier de substitutions périmé) ;
  - une ligne ajoutée contient encore de la langue source (substitution manquante) ;
  - une chaîne d'interface attendue est absente du résultat.

Usage :
  python3 trans_script_2_update_translation.py \
      --old-source NMS_txt_code_FR_v1.1.html --new-source NMS_txt_code_FR_v1.3.html \
      --translation NMS_txt_code_EN_v1.1.html \
      --subs trans_script_1_substitutions_FR-EN_v1.1-to-v1.3.json --out NMS_txt_code_EN_v1.3.html --lang en

  --dry-run : fait toutes les vérifications sans écrire le fichier de sortie.
  --force   : autorise l'écrasement d'un fichier de sortie existant.
"""
import argparse
import difflib
import io
import json
import os
import re
import sys

# Python crée sinon un dossier __pycache__ à côté du module importé : inutile à versionner, donc désactivé.
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trans_script_4_verify_symmetry as V  # noqa: E402


class Stop(Exception):
    """Arrêt volontaire : quelque chose n'est pas sûr, on n'écrit rien."""


def load_subs(path):
    with io.open(path, encoding="utf-8") as f:
        data = json.load(f)
    for key in ("replacements",):
        if key not in data:
            raise Stop("fichier de substitutions : clé « %s » manquante" % key)
    return data


def build(old_src, new_src, tr, subs):
    ls_old, ls_new, lt = V.split_lines(old_src), V.split_lines(new_src), V.split_lines(tr)
    if len(ls_old) != len(lt):
        raise Stop("la traduction n'a pas le même nombre de lignes que l'ancienne source (%d / %d)" % (len(lt), len(ls_old)))
    expected_old = subs.get("expected_old_lines", {})
    keep = set(subs.get("keep_as_is", []))
    pairs = subs["replacements"]
    used = [0] * len(pairs)

    sm = difflib.SequenceMatcher(None, ls_old, ls_new, autojunk=False)
    hunks = [o for o in sm.get_opcodes() if o[0] != "equal"]
    out, pos, warnings, added_lines = [], 0, [], []
    for n, (tag, i1, i2, j1, j2) in enumerate(hunks, 1):
        out += lt[pos:i1]
        if tag in ("replace", "delete"):
            for k in range(i1, i2):
                if lt[k] == ls_old[k]:
                    continue
                if expected_old.get(ls_old[k]) == lt[k]:
                    continue
                raise Stop("modification %d : la ligne %d n'est pas identique dans les deux langues et n'est pas déclarée dans "
                           "« expected_old_lines ».\n  source    : %s\n  traduction: %s" % (n, k + 1, ls_old[k][:120], lt[k][:120]))
        if tag == "insert":
            for k in (i1 - 1, i1):
                if 0 <= k < len(lt) and ls_old[k] != lt[k]:
                    warnings.append("modification %d : ligne voisine %d différente entre les deux langues (commentaire traduit ?) : à relire" % (n, k + 1))
        for line in ls_new[j1:j2]:
            new = line
            for idx, p in enumerate(pairs):
                if p["src"] in new:
                    new = new.replace(p["src"], p["dst"])
                    used[idx] += 1
            added_lines.append((line, new))
            out.append(new)
        pos = i2
    out += lt[pos:]

    unused = [pairs[i]["src"] for i, c in enumerate(used) if c == 0]
    if unused:
        raise Stop("substitution(s) ne s'appliquant à aucune ligne ajoutée (fichier de substitutions périmé ?) :\n  - " + "\n  - ".join(u[:110] for u in unused))
    rx = subs.get("residual_pattern")
    if rx:
        crx = re.compile(rx, re.I)
        hits = [new for _, new in added_lines if crx.search(new) and new not in keep]
        if hits:
            raise Stop("langue source résiduelle dans des lignes ajoutées (substitution manquante) :\n  - " + "\n  - ".join(h.strip()[:120] for h in hits[:10]))
    else:
        warnings.append("aucun « residual_pattern » dans le fichier de substitutions : détection de la langue source non effectuée")
    result = "\n".join(out)
    missing = [(k, f) for k, f in V.ui_fragments(subs.get("ui_strings", {}), subs.get("message_fragments", [])) if f not in result]
    if missing:
        raise Stop("chaînes d'interface attendues absentes du résultat : %s" % missing[:6])
    return result, hunks, added_lines, warnings


def main():
    ap = argparse.ArgumentParser(description="Met à jour une traduction à partir d'une nouvelle version de la source.")
    ap.add_argument("--old-source", required=True)
    ap.add_argument("--new-source", required=True)
    ap.add_argument("--translation", required=True, help="traduction existante, alignée avec --old-source")
    ap.add_argument("--subs", required=True, help="fichier de substitutions validé (JSON)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", help="valeur attendue de <html lang>")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--tools", action="store_true", help="lance aussi node --check et html-validate")
    a = ap.parse_args()
    try:
        old_src, new_src, tr = V.read(a.old_source), V.read(a.new_source), V.read(a.translation)
        subs = load_subs(a.subs)
        print("ancienne source : %s (md5 %s)" % (os.path.basename(a.old_source), V.md5(old_src)))
        print("nouvelle source : %s (md5 %s)" % (os.path.basename(a.new_source), V.md5(new_src)))
        print("traduction      : %s (md5 %s)\n" % (os.path.basename(a.translation), V.md5(tr)))
        print("== 1. Condition préalable : la traduction existante est-elle alignée avec l'ancienne source ?")
        pre = V.check_alignment(old_src, tr)
        for s, l, d in pre:
            if s in ("FAIL", "WARN"):
                print("%s %s%s" % (s, l, (" : " + d) if d else ""))
        if any(s == "FAIL" for s, _, _ in pre):
            raise Stop("la traduction n'est pas alignée avec l'ancienne source : le mode incrémental est impossible. "
                       "Retraduction complète à prévoir (voir le prompt de traduction).")
        print("PASS alignement vérifié (%d contrôles)\n" % len(pre))
        print("== 2. Application des modifications")
        result, hunks, added, warnings = build(old_src, new_src, tr, subs)
        print("PASS %d modifications appliquées aux mêmes positions (%d lignes ajoutées ou remplacées)" % (len(hunks), len(added)))
        for w in warnings:
            print("WARN " + w)
        print("\n== 3. Vérification du résultat")
        res = (V.check_alignment(new_src, result) + V.check_hygiene(result, a.lang, new_src)
               + V.check_incremental(old_src, new_src, tr, result, subs.get("residual_pattern"), set(subs.get("keep_as_is", []))))
        if a.tools:
            res += V.check_tools(result)
        ok = V.report(res)
        if not ok:
            raise Stop("la vérification du résultat a échoué : rien n'est écrit")
        if a.dry_run:
            print("\n--dry-run : fichier non écrit. md5 du résultat : %s" % V.md5(result))
            return 0
        if os.path.exists(a.out) and not a.force:
            raise Stop("%s existe déjà (utiliser --force pour l'écraser)" % a.out)
        with io.open(a.out, "w", encoding="utf-8", newline="") as f:
            f.write(result)
        print("\nÉcrit : %s (%d lignes, md5 %s)" % (a.out, len(V.split_lines(result)) - 1, V.md5(result)))
        print("Rappel : rendu visuel, alignements et couleurs restent à valider à l'oeil ; "
              "lancer aussi trans_script_3_test_behavior.js pour le comportement.")
        return 0
    except Stop as e:
        print("\nARRÊT : %s" % e)
        print("Aucun fichier n'a été écrit.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
