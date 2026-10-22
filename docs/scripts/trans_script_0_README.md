# Scripts de traduction (docs/scripts)

Ces fichiers, tous préfixés `trans_script_`, forment **un seul outil** dont l'unique fonction est la traduction de
`NMS_txt_code.html`, le guide **multilingue en un seul fichier**. Le numéro dans le nom donne l'ordre d'utilisation.

Ils ne sont pas nécessaires pour lire ou utiliser le guide, et ils ne remplacent jamais une relecture humaine.

## Principe

Le guide contient un bloc de langue par langue (`<script type="application/json" id="i18n-fr">`, `…-en`, etc.) en fin de
fichier. Traduire, c'est **remplir ou mettre à jour les clés d'un bloc**, jamais retraduire un fichier entier. Chaque bloc
commence par un `_meta` qui contient le nom de la langue, son drapeau et les **paramètres de traduction** (variante, ton,
fidélité, style des `aria-label`) à réutiliser à chaque mise à jour.

## En bref : à quoi sert chaque fichier

| N° | Fichier | Utilité en une ligne |
|---|---|---|
| 0 | `trans_script_0_README.md` | Ce document : à lire en premier. |
| 1 | `trans_script_1_check_keys.py` | **Contrôle les blocs de langue** et **liste les clés à traduire** (nouvelles, modifiées, manquantes). |
| 2 | `trans_script_2_test_behavior.js` | **Teste le comportement** du guide dans une langue : copie, croix d'effacement, erreurs de balise, exemples, onglets. |
| 3 | `trans_script_3_test_robustness.js` | **Teste la robustesse** : traduction malveillante, bloc illisible, langue partielle, détection du navigateur, stockage bloqué. |
| 4 | `trans_script_4_test_render.js` | **Compare le rendu** de deux versions du guide (utile après une modification du code). |

## Ce que les scripts ne font jamais

- **Ils ne traduisent rien.** La traduction est faite avec le prompt `prompt_translation_HTML_GUIDE_LANG.md`, puis validée.
- **Ils ne modifient aucun fichier** : tous sont en lecture seule (les tests travaillent sur des copies en mémoire).
- **Ils ne remplacent pas la validation humaine** : qualité de la traduction, rendu visuel, alignements et couleurs
  restent à vérifier dans un vrai navigateur.

## Déroulement

Prérequis : Python 3 (bibliothèque standard uniquement). Pour les n° 2, 3 et 4 : Node.js, et `npm i jsdom` dans un dossier
temporaire (puis `NODE_PATH` pointe vers son `node_modules`).

**Ajouter une fonctionnalité au guide** : écrire le HTML avec ses clés et les textes dans le bloc français, puis lister ce
qu'il reste à traduire :

```
python3 trans_script_1_check_keys.py NMS_txt_code.html --since NMS_txt_code_precedent.html
python3 trans_script_1_check_keys.py NMS_txt_code.html --since NMS_txt_code_precedent.html --todo en
```

La seconde commande affiche, pour la langue `en`, uniquement les clés manquantes ou modifiées dans le français avec leur
texte source : c'est la **liste de travail**, sans avoir à relire le fichier.

**Ajouter une langue** : `python3 trans_script_1_check_keys.py NMS_txt_code.html --todo es` liste toutes les clés à traduire.
Le nouveau bloc reprend la forme d'un bloc existant ; son `_meta` renseigne le nom, le drapeau et les paramètres de traduction.

**Contrôler après traduction** :

```
python3 trans_script_1_check_keys.py NMS_txt_code.html --strict
NODE_PATH=/chemin/node_modules node trans_script_2_test_behavior.js --file NMS_txt_code.html --lang es
NODE_PATH=/chemin/node_modules node trans_script_3_test_robustness.js NMS_txt_code.html
```

**Après une modification du code** (pas d'une traduction) :
`node trans_script_4_test_render.js reference.html candidat.html fr` doit répondre « TOUT OK » dans chaque langue.

Tous les scripts sortent avec le code 0 si tout passe, 1 sinon (2 pour une erreur d'utilisation).

## Ce que le contrôle des clés (n° 1) vérifie

- chaque bloc est un JSON valide, avec un `_meta` complet ; une langue de traduction renseigne ses paramètres de traduction ;
- les clés utilisées par le HTML et le JavaScript existent dans la langue source ; chaque langue a exactement les clés de la
  source (manquantes : avertissement, ou échec avec `--strict` ; en trop : échec) ;
- mêmes `{paramètres}`, mêmes balises et mêmes extraits `<code>` que la source ; seuls les **pseudo-noms** (`NAME_COLOR`,
  `NAME_ICON`) et le **mot-témoin** (`syn-text`) peuvent être traduits, et ils doivent l'être de façon cohérente partout et
  conforme à la clé `copy.template_word` ;
- uniquement des balises autorisées (`a`, `b`, `br`, `code`, `em`, `i`, `span`, `strong`), aucun attribut dangereux ;
- le `<title>` statique est identique à la clé `page.title` de la source ;
- avec `--since` : les clés ajoutées, modifiées et supprimées dans la source, et les traductions qui n'ont pas été retouchées.

## Bon usage avec Claude

- **Joindre les fichiers sans coller leur contenu** dans la conversation : les scripts travaillent sur le disque, et le
  guide pèse plusieurs centaines de Ko dont l'essentiel est du base64 sans intérêt pour la traduction.
- **Demander d'exécuter les scripts plutôt que de les lire** : ce README et le md5 suffisent à les identifier.
- **Traduire à partir de la liste de travail** (`--todo`) : Claude n'a besoin de lire que les clés concernées.
- Fournir le fichier précédent (`--since`) pour que les clés modifiées soient détectées.

## Si ceci change, mettre à jour cela

| Si le guide change ainsi | À mettre à jour |
|---|---|
| Nouveau texte ou nouvelle fonctionnalité avec des textes | Uniquement les blocs de langue (le n° 1 liste ce qui manque) |
| Nouvelle fonctionnalité avec un comportement à tester | Le n° 2 (ajouter ses contrôles) |
| Nouveau pseudo-nom pédagogique ou nouvelle classe de mot traduisible dans un extrait de code | Constantes `PSEUDO_NAMES` et `FREE_CLASSES` du n° 1 |
| Nouvelle balise autorisée dans les textes traduits | `I18N_ALLOWED` dans le guide, et `ALLOWED` dans le n° 1 |
| Clés renommées ou nouvelle zone de l'interface | Rien : les attendus sont calculés ; le n° 2 lit des clés connues (`hero.copy.*`, `sim.err.*`, `copy.*`) à adapter si elles sont renommées |
| Nouvelle langue | Un nouveau bloc dans le guide, rien dans les scripts |
| Nouvelle version du moteur de langues du guide | Les n° 2, 3 et 4 (ils s'appuient sur `applyLanguage`, `I18N` et les identifiants du guide) |

## Limites

- **jsdom n'est pas un vrai navigateur** : il valide la logique et la structure produite, pas l'aspect visuel, les polices ni
  les drapeaux emoji.
- **Cohérence, pas qualité** : ces scripts garantissent qu'aucune clé n'a été oubliée ou abîmée, pas que la traduction est juste.
- **Texte modifié dans la source et traduction laissée identique** : le n° 1 le signale comme « non retouchée », ce qui peut
  être un faux avertissement si le mot est identique dans la langue cible (par exemple un nom propre).

## Versions et empreintes

| Fichier | Version | md5 |
|---|---|---|
| `trans_script_1_check_keys.py` | 1.0 | `e5641d0f0d2b94da540cb49a8c14c38f` |
| `trans_script_2_test_behavior.js` | 1.0 | `65372c0f1f9218c2cb6f82e47566b370` |
| `trans_script_3_test_robustness.js` | 1.0 | `67385a8b840f2bdb5a85194de803d9e9` |
| `trans_script_4_test_render.js` | 1.0 | `ccde55fc62a27a856c918f4ab88f2b7c` |

Historique : 1.0 (2026-10-19) première version de cette série, qui remplace celle des fichiers de langue séparés
(`trans_script_1_substitutions_*.json`, `trans_script_2_update_translation.py`, `trans_script_3_test_behavior.js`,
`trans_script_4_verify_symmetry.py`), devenue sans objet depuis le guide multilingue en un seul fichier.
