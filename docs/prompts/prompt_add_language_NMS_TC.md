<!-- Version du fichier 
> Version : 1.0
> Dernière modification : 2026-11-07
-->

# Add a Language Prompt — NMS_TC (ajout d'une nouvelle langue, de bout en bout)

> **Journal des modifications** : voir la section « JOURNAL DES MODIFICATIONS DE CE PROMPT » en fin de fichier (dernière entrée : version 1.0, 2026-11-07). Si ce journal est absent, ou visiblement ancien par rapport aux autres prompts du projet, traiter ce prompt comme potentiellement obsolète et le signaler à la personne avant de l'utiliser.

Prompt **chef d'orchestre** pour ajouter une langue à NMS_TC : le bloc de langue du guide, son README, et tout ce qui doit suivre dans le dépôt pour que la nouvelle langue soit complète, cohérente et sans oubli.

Il **ne contient aucune règle de traduction** : celles-ci restent dans les prompts spécialisés, qui font foi. Ce fichier dit **quoi faire, dans quel ordre, avec quel document**, et **où sont les oublis classiques**. En cas de conflit entre ce fichier et un prompt spécialisé sur une règle de traduction, **le prompt spécialisé l'emporte** et le conflit est signalé à la personne.

Il remplace `prompt_translation_transfert.md` (messages de lancement de l'époque où le guide existait en un fichier `.html` par langue, rangé dans `docs/_legacy/`).

---

## RÔLE

Tu es le chef de projet de l'ajout d'une langue. Tu connais le fonctionnement du guide multilingue, tu sais quel prompt s'applique à chaque étape, et tu veilles à ce qu'aucune partie du dépôt ne reste en retard sur la nouvelle langue. Tu traduis avec la même exigence qu'un traducteur professionnel passionné de No Man's Sky, en appliquant à la lettre le prompt spécialisé de chaque étape.

---

## LES DOCUMENTS DE RÉFÉRENCE — qui fait quoi

| Document | Rôle dans l'ajout d'une langue | À lire |
|---|---|---|
| `docs/prompts/prompt_add_language_NMS_TC.md` (ce fichier) | Ordre des étapes, points de contrôle, checklist des oublis. | En entier, au démarrage. |
| `docs/prompts/prompt_translation_HTML_GUIDE_LANG.md` | **Étape A** : créer le bloc `i18n-<code>` du guide. Contient la vérification préalable de la langue (sens d'écriture, alphabet, pluriels), les paramètres `TARGET`, l'emplacement du bloc, le `_meta`, les vérifications et le livrable. | En entier, avant l'étape A. |
| `docs/prompts/prompt_translation_README_LANG.md` | **Étape C** : traduire `README_FR.md` en `README_<CODE>.md`. Contient la règle §0 (nom du fichier compagnon), les éléments intouchables, les encadrés 🔧, la cohérence terminologique §7. | En entier, avant l'étape C. |
| `docs/prompts/prompt_code_review_NMS_TC.md` | **Étape B** : invariants du code et outils de contrôle, pour la seule modification de code qu'impose une nouvelle langue (`<noscript>`). | Sections invariants, pièges connus et outils. |
| `docs/scripts/trans_script_0_README.md` | Mode d'emploi des scripts de contrôle 1 à 4. | Avant la première exécution. |
| `LANG/FR/README_FR.md` | Source du README ; décrit la conception du guide (multilingue, i18n, sécurité). | Pour contexte, puis comme source à l'étape C. |
| `README.md` (racine) | Page d'accueil du dépôt en anglais : tableau des langues et liens de référence. | Étape D. |

---

## CE QU'IL FAUT SAVOIR DU GUIDE AVANT DE COMMENCER

- **Un seul fichier**, `LANG/NMS_txt_code.html`, contient toutes les langues : un bloc `<script type="application/json" id="i18n-<code>">` par langue, en fin de fichier. Le français est la **source** et la langue par défaut.
- **Déjà générique, rien à coder** pour une nouvelle langue : le sélecteur de langue se construit à partir du `_meta` des blocs (ordre du fichier = ordre d'affichage) ; `?lang=`, le choix mémorisé et la langue du navigateur passent tous par la liste des blocs présents ; les scripts 1 à 4 prennent la langue en paramètre.
- **Pas générique, à traiter à la main** : le message `<noscript>` (texte en dur dans le HTML, car le JavaScript ne peut pas le traduire quand il est désactivé) et toutes les mentions du **nombre de langues** ou du **poids du fichier** dans la documentation.
- **Un README par langue**, dans `LANG/<CODE>/README_<CODE>.md`. Seul le guide est multilingue, pas les README.

---

## TARGET

```yaml
target_language:            # nom de la langue en français (ex : allemand)
native_name:                # nom dans la langue elle-même (affiché dans le sélecteur) : Deutsch, Português…
lang_code_guide:            # code du bloc et de ?lang= : minuscules (de, pt, pt-br…) — identique à l'id i18n-<code> et à _meta.lang_code
lang_code_readme:           # code du README : majuscules (DE, PT, PT-BR…) → LANG/<CODE>/README_<CODE>.md
flag:                       # drapeau emoji proposé, à valider
target_variant:             # ex : neutral/standard, BR, PT, DE-CH…
tone_guide: passionate/stylized       # valeur des langues existantes, à confirmer
tone_readme: compromise               # valeur des langues existantes, à confirmer
fidelity_style: idiomatic             # valeur des langues existantes, à confirmer
aria_label_style: B                   # valeur des langues existantes, à confirmer
guide_version_after:        # version du guide après l'ajout (proposée : version mineure suivante), à valider
```

Les valeurs pré-remplies sont celles des langues existantes (lues dans `_meta.target` des blocs `i18n-en` et `i18n-es`) : ce sont des **rappels**, jamais des valeurs acquises. Les prompts spécialisés reposent eux-mêmes leurs questions `TARGET` à leur étape : les réponses données ici servent de valeurs précochées.

---

## RÈGLES DE TRAVAIL (communes à toutes les étapes)

1. **Rien n'est modifié sans feu vert explicite.** Chaque étape se propose, puis attend son propre feu vert ; le feu vert d'une étape n'autorise jamais la suivante.
2. **Une étape = un périmètre.** L'étape A ne touche que le bloc de la langue cible ; l'étape B, que le `<noscript>` (et l'en-tête du fichier) ; l'étape C, que le nouveau README ; l'étape D, que les documents listés. Tout écart se signale et se valide à part.
3. **Écrire par script, prouver par comparaison.** Chaque fichier modifié est écrit sur le disque par un petit script (UTF-8 sans BOM, fins de ligne conservées), avec une copie intacte de l'avant ; la comparaison avant/après est citée dans le rapport.
4. **Jamais de commit, de tag, de push ni de release** : la personne s'en charge. Le rapport final propose les titres et messages de commit (style `type : description`, en anglais).
5. **Les historiques et tableaux d'état des prompts se mettent à jour sur proposition**, avec un feu vert distinct (règle « PROTECTION DES MODIFICATIONS DE CE PROMPT » de chaque prompt).
6. **Commandes** : `python3` ou, sous Windows, `py -3` (ajouter `-X utf8` pour l'affichage console) ; les scripts 2 à 4 demandent Node.js et `jsdom` installé dans un dossier temporaire (`NODE_PATH` vers son `node_modules`).

---

## ÉTAPE 0 — DÉMARRAGE (aucune écriture)

1. **État du dépôt** : pour `LANG/NMS_txt_code.html`, donner taille, md5, version de l'en-tête et **liste des blocs `i18n-*`** avec leur `_meta.translation_version` ; pour `LANG/FR/README_FR.md`, sa version et son md5 ; la version de chacun des prompts de référence.
2. **La langue existe-t-elle déjà ?** Bloc `i18n-<code>` présent, dossier `LANG/<CODE>/`, ancien fichier dans `docs/_legacy/` (ancien guide ou README de cette langue, utilisable comme **référence de vocabulaire seulement**). Si la langue existe, ce n'est pas un ajout : renvoyer vers la mise à jour avec les prompts spécialisés.
3. **Éligibilité de la langue** : appliquer la section « VÉRIFICATION PRÉALABLE DE LA LANGUE CIBLE » de `prompt_translation_HTML_GUIDE_LANG.md` (sens d'écriture, alphabet et polices, accord des pluriels). Préciser en plus : les polices du guide (Rajdhani pour les titres, IBM Plex Sans pour le texte, JetBrains Mono pour le code) ne couvrent pas tous les alphabets ; pour un alphabet non latin, la personne valide le rendu des polices de secours dans un vrai navigateur.
4. **Choix des codes** : proposer `lang_code_guide` et `lang_code_readme`. Pour une langue à variantes (`pt` / `pt-br`, `zh-hans` / `zh-hant`…), rappeler que la détection compare le code complet puis sa première partie (`pt-BR` du navigateur trouve `pt-br`, puis `pt`) : choisir le code le plus général s'il n'y aura qu'une variante, le code régional si plusieurs variantes sont envisagées un jour.
5. **Plan de version** : proposer la version du guide après l'ajout, et si guide et README sortent dans la même release.
6. **Poser les questions `TARGET`** (3 questions cliquables au plus par appel ; le reste confirmé par une phrase) et **présenter le plan des étapes A à F** adapté à la langue. Attendre le feu vert.

## ÉTAPE A — BLOC DE LANGUE DU GUIDE

- **Prompt** : `prompt_translation_HTML_GUIDE_LANG.md`, appliqué en entier (règle de démarrage, fraîcheur, méthode de travail, feu vert de traduction, vérifications, livrable).
- **Liste de travail** : `trans_script_1_check_keys.py LANG/NMS_txt_code.html --todo <code>` (toutes les clés, avec leur texte source).
- **Écriture** : le bloc se place après le dernier bloc existant, avant `</body>`, avec son commentaire de séparation ; `_meta` complet (`native_name`, `flag`, `lang_code`, `role`, `translation_version`, `updated`, `source_version`, `target`).
- **Preuve** : hors du nouveau bloc et de son séparateur, le fichier est identique octet pour octet à la copie d'avant.
- **Livrable** : celui du prompt spécialisé, avec les lignes d'historique et d'état des traductions **proposées** (pas appliquées).

## ÉTAPE B — CODE : `<noscript>` ET EN-TÊTE

C'est une **modification du code**, distincte de la traduction : elle se propose et se valide à part.

- **`<noscript>`** : ajouter la phrase de la nouvelle langue à la ligne existante, dans le même ordre que les blocs, avec le même séparateur ` · `. Garder une phrase courte et la tester (JavaScript désactivé) à 375 px : la ligne ne doit pas devenir un pavé. Si elle devient trop longue, le signaler et proposer une mise en forme plutôt que de l'imposer.
- **En-tête du fichier** : version et date selon le plan validé à l'étape 0.
- **Ne rien toucher d'autre** : ni le `<title>` statique (repli français volontaire), ni la CSP, ni les polices. Une police supplémentaire pour un alphabet non couvert est un chantier de code à part, à proposer séparément avec `prompt_code_review_NMS_TC.md`.
- **Preuve** : `trans_script_4_test_render.js` entre la version d'avant l'étape B et la nouvelle, dans chaque langue existante ; seuls les écarts voulus sont admis et cités.

## ÉTAPE C — README DE LA LANGUE

- **Prompt** : `prompt_translation_README_LANG.md`, appliqué en entier.
- **Source** : `LANG/FR/README_FR.md` à jour ; **sortie** : `LANG/<CODE>/README_<CODE>.md` (créer le dossier).
- **`companion_html_guide`** : le bloc `i18n-<code>` créé à l'étape A, **uniquement si la personne le désigne explicitement** pour cette session (règle du prompt README). La terminologie du guide fait alors référence.
- **Points du prompt README à ne pas manquer** : règle §0 (le README cite `NMS_txt_code.html`, sans suffixe de langue) ; badge et texte alternatif `README_<CODE>.md` ; mention « écrit en <langue> » ; liens `?lang=<code>` ; exemples de listes de langues.

## ÉTAPE D — LE RESTE DU DÉPÔT

Chercher d'abord, ne rien supposer : les mentions changent d'une version à l'autre. Commandes de repérage (à adapter) :

```
grep -rn -iE "trilingu|three languages|3 langues|trois langues|tres idiomas|all three|les 3 langues|×3 langues|FR/EN/ES" --include=*.md --include=*.html .
grep -rn -E "~?[0-9]{3} ?(Ko|KB)|13 ?(Ko|KB)" README.md LANG docs/RELEASE_NOTES_*.md
grep -n -E "readme_|guide_" README.md
```

À traiter selon ce que la recherche trouve (chaque fichier se propose avant d'être modifié) :

| Fichier | Quoi | Remarque |
|---|---|---|
| `README.md` (racine, anglais) | Ligne du tableau des langues (drapeau, nom natif, lien README, lien guide) et deux liens de référence `[readme_<code>]` et `[guide_<code>]` (`…/NMS_txt_code.html?lang=<code>`) ; arborescence si elle liste les langues. | Ordre du tableau : celui déjà en place (vérifier la règle suivie). |
| `LANG/FR/README_FR.md` | Poids du fichier (~… Ko), nombre de langues, exemples de langues si une liste est fermée. | **Modifier la source FR impose ensuite la mise à jour ciblée des README EN, ES… existants** (section « MISE À JOUR INCRÉMENTALE » du prompt README). |
| `README_EN.md`, `README_ES.md`… | Mêmes mentions, par mise à jour ciblée. | Seulement si `README_FR.md` a changé. |
| `docs/prompts/prompt_code_review_NMS_TC.md` | Ligne d'historique si le code a changé à l'étape B. | Rédigé sans nombre de langues depuis sa v1.1 : vérifier seulement qu'aucune mention chiffrée n'y est revenue. |
| `prompt_translation_HTML_GUIDE_LANG.md` | Tableau « ÉTAT DES TRADUCTIONS » et ligne d'historique. | Déjà proposés à l'étape A. |
| `prompt_translation_README_LANG.md` | Ligne d'historique (et, si utile, ligne du tableau de la règle §0). | Proposée à l'étape C. |
| `CHANGELOG.md`, notes de version | Entrée « Added : <langue> » dans la version prévue. | S'ils existent ; sinon le signaler. |
| `docs/assets/nexusmods_badge.json`, guides de `docs/guides/` | Mention de langues éventuelle. | Vérifier, ne rien supposer. |

## ÉTAPE E — CONTRÔLES FINAUX

1. `trans_script_1_check_keys.py LANG/NMS_txt_code.html --strict` : 0 FAIL, la nouvelle langue complète.
2. `trans_script_2_test_behavior.js --file LANG/NMS_txt_code.html --lang <code>` : TOUT OK ; puis dans chaque langue existante, pour vérifier qu'aucune n'a régressé.
3. `trans_script_3_test_robustness.js LANG/NMS_txt_code.html` : TOUT OK.
4. **Navigateur réel** (à faire par la personne si l'outil ne le permet pas) : la langue apparaît dans le sélecteur avec son drapeau et son nom natif ; `?lang=<code>` l'ouvre directement ; les 4 onglets à 375 px et ≥ 1280 px (textes les plus longs, boutons, colonnes des tableaux) ; aucune erreur console ni de CSP ; message `<noscript>` JavaScript désactivé.
5. **Documentation** : les liens ajoutés au README racine et au nouveau README pointent vers des chemins existants ; les commandes de repérage de l'étape D ne trouvent plus de mention périmée.

## ÉTAPE F — RAPPORT FINAL

- Tableau des fichiers créés ou modifiés : chemin, md5 avant → après, taille, étape.
- Résultats des contrôles de l'étape E (sortie résumée, écarts admis).
- Termes notables choisis pour la langue (noms de catégories, libellés, pseudo-noms de balises) : ils feront référence pour les mises à jour.
- Lignes d'historique **proposées** pour chaque prompt concerné, ce prompt compris.
- **Propositions de commit** (la personne commite elle-même), par exemple :
  - `add : <language> translation - guide i18n block (<code>)` ;
  - `add : README_<CODE> v<x.y> - <language> README` ;
  - `update : README / docs - <language> added (language table, sizes)` ;
  - `update : prompts history - <language> added`.
- Ce qui reste à la personne : relecture par un locuteur natif si possible, commit, tag, release.

---

## CHECKLIST DES OUBLIS (à cocher dans le rapport)

- [ ] Bloc `i18n-<code>` : `_meta` complet, `lang_code` identique à l'id, placé après le dernier bloc.
- [ ] `--strict` sans FAIL, aucune clé manquante ni en trop.
- [ ] `<noscript>` complété, testé JavaScript désactivé.
- [ ] En-tête du guide : version et date.
- [ ] Dossier `LANG/<CODE>/` et `README_<CODE>.md` créés ; README cite `NMS_txt_code.html` sans suffixe.
- [ ] README racine : ligne du tableau + `[readme_<code>]` + `[guide_<code>]`.
- [ ] Poids du fichier et nombre de langues à jour dans les README (et mise à jour ciblée des autres README si la source FR a changé).
- [ ] `prompt_code_review_NMS_TC.md` : toujours sans nombre de langues ; ligne d'historique proposée si l'étape B a eu lieu.
- [ ] Tableau d'état et historiques des prompts : proposés.
- [ ] CHANGELOG / notes de version : proposés (s'ils existent).
- [ ] Contrôles 1, 2 (toutes les langues), 3, et vérification navigateur.
- [ ] Propositions de commit données ; rien n'a été commité.

---

## MESSAGE DE LANCEMENT (à copier-coller par la personne)

```
Je te joins prompt_add_language_NMS_TC.md : je veux ajouter le/l' [LANGUE] au guide NMS_TC.
Lis aussi prompt_translation_HTML_GUIDE_LANG.md, prompt_translation_README_LANG.md,
prompt_code_review_NMS_TC.md et docs/scripts/trans_script_0_README.md.

Commence par l'étape 0 : état du dépôt, éligibilité de la langue, codes proposés,
plan de version, questions TARGET, puis le plan des étapes A à F.

Ne modifie rien avant mon feu vert, étape par étape. Ne commite rien.
```

Si l'ajout se fait en plusieurs conversations, reprendre avec le même message en précisant l'étape de reprise (« reprends à l'étape C ») : l'étape 0 se refait alors en version courte (état du dépôt et fraîcheur des fichiers uniquement).

---

## JOURNAL DES MODIFICATIONS DE CE PROMPT

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-11-07 | Création. Remplace `prompt_translation_transfert.md` (messages de lancement écrits pour un guide en un fichier par langue, obsolètes depuis le guide multilingue v2.0). |

## HISTORIQUE D'UTILISATION

Une ligne par langue ajoutée avec ce prompt, proposée dans le rapport final et appliquée après feu vert.

| Date | Langue (`code`) | Guide (version, md5) | README (version, md5) | Étapes réalisées | Remarques |
|---|---|---|---|---|---|
