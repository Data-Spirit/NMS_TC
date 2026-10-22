# Scripts de traduction (docs/scripts)

Ces fichiers, tous préfixés `trans_script_`, forment **un seul outil** dont l'unique fonction est la traduction :
**répercuter dans un guide déjà traduit les modifications apportées au guide source (FR) entre deux versions,
sans tout retraduire, et prouver que la traduction reste symétrique du source.**

Le numéro dans le nom donne l'ordre d'utilisation. Ils ne sont pas nécessaires pour lire ou utiliser le guide,
et ils ne sont pas obligatoires pour traduire : la méthode manuelle du prompt de traduction HTML reste toujours valable.

## En bref : à quoi sert chaque fichier

| N° | Fichier | Utilité en une ligne |
|---|---|---|
| 0 | `trans_script_0_README.md` | Ce document : à lire en premier. |
| 1 | `trans_script_1_substitutions_FR-EN_v1.1-to-v1.3.json` | **Les textes validés** à ajouter dans la traduction (étape 1, données d'entrée). Sert aussi de glossaire. |
| 2 | `trans_script_2_update_translation.py` | **Met à jour** la traduction : applique les modifications du source aux mêmes positions. |
| 3 | `trans_script_3_test_behavior.js` | **Teste le comportement** du guide produit (copie, croix, erreurs de balise, exemples, onglets). |
| 4 | `trans_script_4_verify_symmetry.py` | **Vérifie la symétrie** entre le source et la traduction (structure, code, données). Sert aussi de bibliothèque au n° 2. |

## Ce que les scripts ne font jamais

- **Ils ne traduisent rien.** Tout texte ajouté vient du fichier n° 1, relu et validé par la personne qui pilote la traduction.
- **Ils ne devinent rien.** Au moindre doute, ils s'arrêtent avec un message clair et n'écrivent aucun fichier.
- **Ils ne remplacent pas la validation humaine** : la qualité de la traduction, le rendu visuel, les alignements et
  les couleurs restent à vérifier à l'oeil.

## Ce qui change, et à quelle fréquence

Au quotidien, il suffit de gérer le fichier n° 1. Les autres sont des outils stables.

| Fichier | Change quand | Fréquence |
|---|---|---|
| n° 1 (substitutions) | Nouvelle mise à jour ou nouvelle langue : on ajoute un nouveau fichier, on ne réécrit pas l'ancien | À chaque mise à jour |
| n° 3 (test de comportement) | Le guide gagne une **fonctionnalité** : on ajoute ses tests | Quand le guide gagne une fonctionnalité |
| n° 4 (vérification) | Le guide gagne un **nouveau type de bloc de données** ou change le format d'une ligne de données | Très rarement |
| n° 2 (moteur) | La méthode elle-même change | Très rarement |
| n° 0 (README) | L'un des scripts change | Avec les scripts |

- **Mise à jour de texte seule :** seul le n° 1 est touché.
- **Nouvelle fonctionnalité du guide :** le n° 1 (nouvelles chaînes) et le n° 3 (tests de la fonctionnalité).
- **Changement de nature des données :** le n° 4, rarement le n° 3.
- **Nouvelle langue :** un nouveau n° 1 uniquement, avec son propre motif de langue résiduelle.

Dès qu'un script (n° 2, 3 ou 4) change, il passe à la version suivante, son md5 est mis à jour dans le tableau ci-dessous et
dans le prompt de traduction, et le test de référence est rejoué.

## Rangement : ne pas accumuler de fichiers

- **Un seul fichier n° 1 par paire de langues dans le dépôt**, le plus récent. Les précédents peuvent être supprimés
  après publication : Git garde leur historique, et leur glossaire est repris dans le nouveau fichier.
- Le dossier se stabilise donc à : ce README, 3 scripts, et **un fichier n° 1 par langue**. Il grandit avec le nombre de
  langues, jamais avec le nombre de versions.
- Aucun dossier `__pycache__` n'est créé : le moteur désactive l'écriture de ces fichiers techniques.

## Bon usage avec Claude

- **Joindre les fichiers sans coller leur contenu** dans la conversation. Les gros fichiers HTML n'ont pas besoin d'être lus
  en entier : les scripts travaillent directement sur le disque.
- **Demander d'exécuter les scripts plutôt que de les lire.** Le README et le md5 suffisent à les identifier. Leur code
  n'a pas à entrer dans la conversation.
- **Fournir les md5** des fichiers (ceux du tableau plus bas pour les scripts) pour que Claude vérifie qu'ils sont les bons.
- Au début d'une session, Claude demande explicitement les fichiers dont il a besoin : l'ancienne source, la nouvelle,
  la traduction existante et les scripts.

## Déroulement d'une mise à jour

Prérequis : Python 3 (bibliothèque standard uniquement). Pour le n° 3, `npm i jsdom` dans un dossier temporaire.
Pour l'option `--tools`, Node.js et `html-validate` (npm).

1. **Préparer et valider le n° 1.** Les textes ajoutés sont proposés puis validés, puis consignés dans
   `trans_script_1_substitutions_<SRC>-<LANGUE>_v<ancienne>-to-v<nouvelle>.json`.
2. **Essai à blanc** (rien n'est écrit) :

   ```
   python3 trans_script_2_update_translation.py --old-source FR_v1.1.html --new-source FR_v1.3.html \
       --translation EN_v1.1.html --subs trans_script_1_substitutions_FR-EN_v1.1-to-v1.3.json \
       --out EN_v1.3.html --lang en --tools --dry-run
   ```
3. **Application** : la même commande sans `--dry-run`. Le moteur n'écrit le fichier que si toutes les vérifications
   passent, et refuse d'écraser un fichier existant sans `--force`.
4. **Comportement** :

   ```
   NODE_PATH=/chemin/vers/node_modules node trans_script_3_test_behavior.js --file EN_v1.3.html \
       --ui trans_script_1_substitutions_FR-EN_v1.1-to-v1.3.json --ref EN_v1.1.html
   ```
5. **Vérification indépendante** du fichier produit (utile aussi pour contrôler un fichier fait à la main) :

   ```
   python3 trans_script_4_verify_symmetry.py --source FR_v1.3.html --translation EN_v1.3.html --lang en \
       --prev-source FR_v1.1.html --prev-translation EN_v1.1.html \
       --subs trans_script_1_substitutions_FR-EN_v1.1-to-v1.3.json --tools
   ```
6. **Validation visuelle** par la personne : alignement, couleurs, hauteur du cadre d'aperçu, rendu sur mobile.

Variable facultative : `NMSTC_TOOLS_DIR` indique le dossier qui contient `node_modules` (là où `html-validate` est installé)
pour l'option `--tools`.

## Ce que le moteur (n° 2) vérifie avant d'écrire

1. La traduction existante est **alignée** avec l'ancienne source : même nombre de lignes, repères structurels aux mêmes
   numéros de ligne, CSS identique hors commentaires, mêmes fonctions, mêmes `id`, JS identique hors chaînes et
   commentaires, données intactes, catégories traduites de façon cohérente.
2. Chaque ligne à remplacer est **identique dans les deux langues** (sauf celles déclarées dans `expected_old_lines`).
3. Chaque substitution **s'applique au moins une fois** (sinon le fichier n° 1 est périmé).
4. Aucune ligne ajoutée ne contient de **langue source résiduelle** (motif `residual_pattern`).
5. Les **chaînes d'interface validées** (`ui_strings`, `message_fragments`) figurent dans le résultat.
6. Le résultat passe **toutes les vérifications de symétrie** : mêmes positions et tailles de modifications dans les
   deux langues, blocs de données non modifiés dans le source intacts dans la traduction, pas d'espace de fin de ligne
   ajouté, fin de fichier identique.

## Si ceci change, mettre à jour cela

| Si le contenu à traduire change ainsi | À mettre à jour |
|---|---|
| Nouvelle chaîne visible, nouveau message ou nouveau commentaire | Uniquement le n° 1 (`replacements`, et `ui_strings` / `message_fragments` pour une chaîne d'interface) |
| Nouvel attribut traduisible (`aria-label`, `title`, `placeholder`) | Le n° 1 (`ui_strings`) et les contrôles correspondants du n° 3 |
| Nouveau bloc de données (comme `ICONS` ou `FLAG_LABELS`) | Le n° 4 : la constante qui le classe (`FROZEN_BLOCKS`, `FIELD_AWARE_BLOCKS` ou `TRANSLATED_BLOCKS`). Un bloc non classé produit un avertissement, jamais un faux succès |
| Changement de format d'une ligne de données (colonne de catégorie déplacée) | `DATA_SCHEMA` dans le n° 4 |
| Nouvel identifiant HTML ou nouvelle fonction | Rien : les attendus sont calculés en comparant les deux fichiers |
| Nouvelle langue | Un nouveau n° 1, avec son `residual_pattern` propre à la langue source, et une adaptation des messages si la langue ne distingue pas majuscules et minuscules |
| Code réorganisé entre deux versions (blocs déplacés) | Rien : le moteur refuse de s'appliquer (alignement perdu). Il faut retraduire complètement |
| Modifications du source qui touchent aussi du texte déjà traduit | Déclarer les anciennes lignes concernées dans `expected_old_lines`, ou retraduire complètement |

## Limites

- **Alignement ligne à ligne.** Le moteur suppose que la traduction suit la structure du source. Sinon, il s'arrête.
- **Détection de la langue source résiduelle.** Elle repose sur un motif (accents, mots fréquents) : c'est un filet de
  sécurité, pas une preuve. La preuve est la présence exacte des chaînes validées (`ui_strings`) et le test de
  comportement. Adapter le motif à chaque langue source.
- **Symétrie, pas qualité.** Ces scripts garantissent qu'aucune ligne n'a été oubliée, perdue ou déplacée. Ils ne jugent
  ni la justesse ni le naturel d'une traduction.
- **Pas de rendu visuel.** jsdom valide la logique, pas l'affichage.
- **Mises à jour par ajouts localisés seulement.** Pour une refonte complète du source, retraduire en entier.

## Versions et test de référence

| Fichier | Version | md5 |
|---|---|---|
| `trans_script_1_substitutions_FR-EN_v1.1-to-v1.3.json` | v1.1 vers v1.3 (FR-EN) | `2b48fad9dd7de5297b1f2a5d31b4941c` |
| `trans_script_2_update_translation.py` | 1.1 | `ba5e34644467a5e51b9925f8f8633648` |
| `trans_script_3_test_behavior.js` | 1.1 | `1fa7782759debb56c3e06ddd66d29062` |
| `trans_script_4_verify_symmetry.py` | 1.1 | `9a77df4d2967bdf8cb9c0b85973bfa17` |

Avec les fichiers de la mise à jour FR v1.1 vers v1.3 puis EN v1.1 vers v1.3, le moteur doit reproduire **exactement** le
fichier validé :

| Fichier | md5 |
|---|---|
| `NMS_txt_code_FR.html` v1.1 | `ef6d389f8989d1019a9ea8b9cc755a49` |
| `NMS_txt_code_FR.html` v1.3 | `47c06aa3fe32100b491cca502bc34fb9` |
| `NMS_txt_code_EN.html` v1.1 | `7bb97d3d2ce21bf3d2f8100c7aba69cf` |
| `NMS_txt_code_EN.html` v1.3 (résultat attendu) | `1602e1936d40510ba9eb085dbd6e09ee` |

Si le md5 du résultat diffère, ne pas utiliser les scripts avant d'en avoir compris la raison.

Historique : 1.0 (2026-10-17) première version ; 1.1 (2026-10-17) renommage `trans_script_N_*`, le moteur ne crée plus
de dossier `__pycache__`, suppression du fichier `ui_strings_FR.json`, README complété.
