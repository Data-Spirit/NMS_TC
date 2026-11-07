<!-- Version du fichier 
> Version : 1.0
> Dernière modification : 2026-11-07
-->

# Révision — NMS_TC

> **Journal des modifications** : voir la section « JOURNAL DES MODIFICATIONS » en fin de fichier (dernière entrée : version 1.0, 2026-11-07).

Comment réviser ce projet : les **outils** (`docs/scripts/`), le **code** (le guide `LANG/NMS_txt_code.html`), la **documentation** (README, prompts, guides, journaux, structure du dépôt), ou **les trois** à la suite. Cette page est la **procédure** ; le texte à donner à un agent est le [prompt maître](prompts/prompt_revision_NMS_TC.md). Les erreurs déjà rencontrées sont dans [pitfalls.md](pitfalls.md).

Pour comprendre le projet avant de le réviser : [README_FR.md](../LANG/FR/README_FR.md) (conception du guide), [trans_script_0_README.md](scripts/trans_script_0_README.md) (scripts de contrôle), [ROADMAP.md](../ROADMAP.md) et [CHANGELOG.md](../CHANGELOG.md).

---

## Quand réviser

Avant une release, après un lot important de fonctions ou de corrections, après l'ajout d'une langue, après une modification d'un script de contrôle, et dès qu'un doute apparaît (doc qui se contredit, outil jamais relancé, comportement inattendu signalé). Une révision ne remplace pas l'essai dans un vrai navigateur, ni la vérification **en jeu** de ce qui concerne No Man's Sky lui-même (une balise, une couleur, une icône).

## Choisir le mode

| Mode | Pour | Passes du [prompt maître](prompts/prompt_revision_NMS_TC.md) |
|---|---|---|
| **Outils** | fiabilité des scripts de contrôle : couverture, faux positifs, faux négatifs, bugs, hypothèses figées, documentation des scripts | 0, 1, 9 |
| **Code** | bugs, code mort et reliquats, optimisation, sécurité, accessibilité, mise en page, structure du guide | 0, 2 à 7, 9 |
| **Doc** | README (source et traductions), prompts, guides, journaux, liens et ancres, structure du dépôt, publication GitHub Pages | 0, 8, 9 |
| **Complète** | les trois, avant une release ou après un gros chantier | 0 à 9, dans l'ordre |

**Ordre de la révision complète : outils, puis code, puis doc.**
- **Les outils d'abord** : un script peu fiable rend les tests du code peu fiables, donc la révision du code elle-même.
- **Le code ensuite** : la doc décrit le code ; la réviser avant serait la réviser deux fois.
- **La doc en dernier**, mise à jour avec ce que les deux premières étapes ont changé, puis la vérification finale de l'ensemble.

En mode **Code** ou **Doc** seul, la passe 0 vérifie quand les outils ont été révisés pour la dernière fois (historique de ce fichier) ; si un script a changé depuis, le signaler avant de se fier à ses résultats.

---

## Les outils

Ce tableau est la **description de référence** de chaque contrôle : ce qu'il détecte et, surtout, ce qu'il ne voit pas.

| Outil | Commande | Détecte | Limites connues |
|---|---|---|---|
| Clés et sécurité i18n (n° 1) | `py -3 docs/scripts/trans_script_1_check_keys.py LANG/NMS_txt_code.html --strict` (options `--since ANCIEN.html`, `--todo <code>`) | JSON des blocs, `_meta`, clés utilisées absentes de la source, clés manquantes ou en trop par langue, `{paramètres}`, balises et extraits `<code>` identiques à la source, balises et attributs hors liste blanche, `<title>` statique ; avec `--since` : clés ajoutées, modifiées, supprimées, traductions non retouchées | ne juge pas la **qualité** d'une traduction ; sans `--since`, un texte source modifié est invisible ; faux avertissement possible quand un mot est identique dans la langue cible (nom propre) |
| Comportement (n° 2) | `NODE_PATH=nm/node_modules node docs/scripts/trans_script_2_test_behavior.js --file LANG/NMS_txt_code.html --lang <code> [--ref ANCIEN.html]` | copie, croix d'effacement, messages d'erreur de balise, exemples, onglets, rendu des entrées valides ; avec `--ref` : non-régression du rendu dans cette langue | jsdom : ni mise en page, ni polices, ni presse-papiers réel ; ne connaît que les fonctions qu'il teste (une fonction nouvelle n'est pas couverte tant qu'on ne l'y ajoute pas) |
| Robustesse (n° 3) | `NODE_PATH=nm/node_modules node docs/scripts/trans_script_3_test_robustness.js LANG/NMS_txt_code.html` | traduction malveillante neutralisée, bloc illisible ignoré, langue partielle repliée sur la source, langue du navigateur, mémorisation, stockage bloqué | jsdom ; ne teste ni `?lang=` ni les valeurs hostiles du stockage (couvertes à la main lors de la revue v2.2) |
| Rendu (n° 4) | `NODE_PATH=nm/node_modules node docs/scripts/trans_script_4_test_render.js REFERENCE.html CANDIDAT.html <code>` | toute différence de rendu entre deux versions, sur une série d'interactions | **s'arrête au premier écart** ([pitfalls.md](pitfalls.md#outils-et-vérifications)) ; jsdom ; ignore les attributs `data-i18n` et le sélecteur de langue |
| HTML | `html-validate --preset recommended LANG/NMS_txt_code.html` | structure HTML, attributs, accessibilité de base | écarts acceptés : `empty-heading`, `text-content` (titres et boutons remplis au chargement) |
| CSS | extraire le `<style>`, puis `stylelint --config stylelint-config-standard` | propriétés invalides, doublons, spécificité | écarts acceptés : `property-no-vendor-prefix` sur `-webkit-mask-*`, `no-descending-specificity` (faux positifs), règles de pur formatage |
| JS | extraire le `<script>` principal (chaînes base64 remplacées par `"data:x"`), puis `eslint` avec la configuration ci-dessous | variables inutilisées, affectations dans les conditions, `const` possibles, ombrage, égalités lâches | ne voit ni le HTML ni les appels par chaîne ; rien sur la logique métier |
| Navigateur réel | ouvrir le guide : onglets, simulateur, copie, recherches, tris, filtre, langues, `?lang=` ; à 375, ~768 et ≥ 1280 px ; console ouverte | tout ce que jsdom ne voit pas : mise en page, polices, CSP, presse-papiers, émojis | manuel ; le navigateur intégré à l'application a ses propres limites ([pitfalls.md](pitfalls.md#outils-et-vérifications)) |
| GitHub et Pages | ouvrir les fichiers modifiés sur GitHub et le guide sur Pages après publication | ancres réelles, rendu Markdown, publication | seulement après le push du mainteneur |

**Installation** (dossier temporaire, hors du dépôt) :

```bash
mkdir nm && cd nm && npm init -y && npm i jsdom html-validate stylelint stylelint-config-standard eslint @eslint/js globals
```

**Configuration ESLint** (`eslint.config.mjs`, dans le dossier `nm/`, d'où ESLint se lance) :

```js
import js from "@eslint/js";
import globals from "globals";
export default [js.configs.recommended, { languageOptions: { ecmaVersion: 2022, sourceType: "script", globals: globals.browser },
  rules: { "no-unused-vars": "warn", "eqeqeq": "warn", "no-shadow": "warn", "prefer-const": "warn", "no-var": "warn", "no-cond-assign": ["error", "except-parens"] } }];
```

**Budgets de performance** (mesurés le 2026-11-07, guide v2.1) : rendu complet du tableau des icônes (`renderIcons('')`) ≤ 5 ms ; rendu filtré ≤ 1 ms ; changement de langue complet ≤ 15 ms ; simulateur ≤ 1 ms par frappe. Un dépassement **mesuré** justifie une optimisation ; en deçà, ne pas réécrire.

### Questionner les outils

Un contrôle vert avec un outil aveugle ne prouve rien. À chaque révision, pour chaque outil utilisé :
1. **À jour ?** Couvre-t-il les fonctions, clés, langues et fichiers ajoutés depuis la dernière fois ? (Comparer l'inventaire des fonctions du guide à ce que les scripts testent.)
2. **Juste ?** Faux positifs (alertes à tort) et faux négatifs (défaut non vu) : le tester sur un **défaut connu**, par exemple retirer une clé d'un bloc, ajouter une clé en trop, injecter `<img onerror>` dans une traduction, casser le JSON d'un bloc, modifier un caractère du rendu ; vérifier qu'il réagit, et qu'il se tait sur le fichier sain.
3. **Sans bug lui-même ?** Le relire comme du code (Python et JavaScript) ; vérifier ses codes de sortie (0, 1, 2) et ses hypothèses figées (nombre de langues, chemins, encodage, système d'exploitation).
4. **Le meilleur pour la tâche ?** Un besoin qui revient sans outil, ou qui prend trop de temps à la main, est un outil à créer : dans `docs/scripts/`, en Python standard ou en Node simple, en lecture seule, documenté dans [trans_script_0_README.md](scripts/trans_script_0_README.md) et dans ce tableau (création sur proposition, comme toute modification du dépôt).

### Lacunes connues (à combler)

- **Liens et ancres de la documentation** : aucun script dans le dépôt ; vérification par un script temporaire et sur GitHub.
- **Code mort** : aucun outil ; recherche à la main (ESLint ne voit que les variables locales inutilisées).
- **`ICON_DATA` ↔ `docs/assets/BANK_ICONS/`** : comparaison faite au cas par cas, sans script dédié.
- **Les scripts de contrôle n'ont pas de tests** : leur justesse se vérifie par les défauts connus de « Questionner les outils ».
- **`?lang=` et valeurs hostiles du stockage** : hors des scripts 2 et 3 ; contrôles ciblés à refaire à la main.

---

## Mode « Outils »

1. **État de départ** : version et md5 de chaque script ([trans_script_0_README.md](scripts/trans_script_0_README.md#versions-et-empreintes)), `git status`, résultats actuels sur le guide.
2. **Lecture intégrale** de chaque script et de son README.
3. **Questionner chaque outil** (les quatre questions ci-dessus), avec les défauts connus.
4. **Couverture** : l'inventaire des fonctions du guide face à ce que les scripts testent ; les lacunes vont dans la liste ci-dessus.
5. **Robustesse** : Windows (`py -3`, encodage, fins de ligne), chemins avec espaces, fichier absent ou illisible, codes de sortie.
6. **Documentation des scripts** : README des scripts, tableau de cette page, versions et md5.
7. **Vérification** : chaque script relancé sur le guide sain (tout passe) et sur les défauts connus (tout échoue), compte rendu.

## Mode « Code »

1. **État de départ** : taille, md5 et version du guide ; copie de la version de référence hors du dépôt ; résultats des outils.
2. **Cartographie et inventaire des fonctions** (référence de non-régression) : [README_FR.md](../LANG/FR/README_FR.md) et le code lui-même.
3. **Bugs**, en tenant compte de [pitfalls.md](pitfalls.md).
4. **Code mort et reliquats**, prouvés avant toute suppression.
5. **Optimisation** : budgets mesurés, poids du fichier, polices.
6. **Sécurité et confidentialité** : CSP, liste blanche des traductions, valeurs externes.
7. **Structure** : fichier unique, ordre des sections, interfaces utilisées par les scripts.
8. **Vérification** : tous les outils dans toutes les langues, navigateur aux trois largeurs, compte rendu.

## Mode « Doc »

1. **Confidentialité** : aucune donnée personnelle (adresse e-mail, chemin d'utilisateur, nom autre que le pseudo public du projet) dans les fichiers suivis ; `git ls-files --others --exclude-standard` pour les fichiers non suivis.
2. **Doc, fichier par fichier** : à jour ? **un sujet = un seul fichier** ? exemples et chiffres exacts ? renvois « Voir aussi » ? fichier long : le signaler et proposer (pas de limite stricte ; les prompts et les fichiers de révision en sont exemptés).
3. **Chaîne des traductions** : `README_FR.md` est la source ; chaque README traduit cite le md5 de la source qu'il reflète ; les historiques des prompts de traduction sont remplis. Une traduction en retard se signale et se met à jour **avec le prompt de traduction** concerné, jamais au fil de la révision.
4. **Liens et ancres** : tous les fichiers suivis (hors `docs/_legacy/`, archives figées) ; ancres réelles de GitHub ([pitfalls.md](pitfalls.md#documentation-github-et-github-pages)).
5. **Navigation** : le README racine mène aux README de langue, aux guides et au téléchargement ; **test du nouvel arrivant** : un agent trouve une information donnée en deux lectures sans ouvrir de gros fichiers.
6. **Dépôt** : licence, [CHANGELOG.md](../CHANGELOG.md) (section `[Unreleased]` à jour), [ROADMAP.md](../ROADMAP.md) (rien de fait n'y reste), journaux et historiques des prompts, versions cohérentes (en-têtes des fichiers, `_meta` des blocs, notes de version), `_config.yml` et ce que GitHub Pages publie.
7. **Mémoire de l'agent** (hors dépôt) : fiches regroupées, sans doublon ni information périmée.

## Mode « Complète »

Outils, puis Code, puis Doc. Entre le code et la doc, noter tout ce que le code a changé et que la doc doit refléter. Terminer par la vérification finale de l'ensemble et un compte rendu unique.

---

## Règles pendant une révision

- **Rapport d'abord, écriture ensuite.** L'agent explore, mesure, crée et lance ses outils **seul et hors du dépôt** ; il **n'écrit rien dans le dépôt** avant le feu vert explicite du mainteneur. Chaque lot validé s'applique séparément ; un feu vert ne vaut pas pour le lot suivant.
- **Dans le doute, ne pas modifier** ; le point va dans le compte rendu avec son niveau de certitude.
- **Ne jamais commiter, taguer, pousser ni publier** : le mainteneur le fait lui-même. Proposer à la fin les titres et messages de commit (`type : description`, en anglais). Ne pas envoyer de contenu à un service extérieur sans demande explicite.
- **Ne pas traduire pendant une révision** : une traduction se fait avec [prompt_translation_HTML_GUIDE_LANG.md](prompts/prompt_translation_HTML_GUIDE_LANG.md) ou [prompt_translation_README_LANG.md](prompts/prompt_translation_README_LANG.md), qui ont leurs propres règles et leur propre feu vert.
- **Dire ce qui n'est vérifié que dans jsdom ou par analyse**, et ce qui reste à voir dans un vrai navigateur, sur GitHub après le push, ou en jeu.

## Compte rendu

Format imposé par le [prompt maître](prompts/prompt_revision_NMS_TC.md#compte-rendu-final) : synthèse, modifications proposées ou appliquées par catégorie avec `fichier:ligne`, points non modifiés avec leur certitude, propositions en attente, ce qui est vérifié et comment, vérifications manuelles à faire, outils, suggestions pour la procédure.

## Faire évoluer cette procédure

Ce fichier et le prompt maître se perfectionnent. À la fin de chaque révision :
- **Ce qu'on a trouvé sans que la procédure le demande** devient une ligne dans le prompt, un piège dans [pitfalls.md](pitfalls.md) ou un outil.
- **Les formulations d'origine se complètent** : le prompt maître du projet Tizen_free qui a servi de modèle, la demande du mainteneur pour la revue de la v2.2 (« couvrir tous les cas, débusquer les bugs vicieux, variables mortes, sécurité, code optimisé ») et l'ancien `prompt_code_review_NMS_TC.md` (archivé dans `docs/_legacy/`). Une nuance retirée pour « simplifier » est une nuance de moins dans la détection. Conserver les nuances, ne les fusionner que sur preuve.
- **Mettre à jour** le tableau des outils, les lacunes et les budgets ; consigner tout changement de méthode dans le journal ci-dessous.
- **Cette page et le prompt maître sont exemptés de toute limite de longueur** : chaque élément y compte. Ne pas les raccourcir ni les scinder pour tenir une limite, sauf décision du mainteneur.

---

## JOURNAL DES MODIFICATIONS

Une ligne par version, de la plus récente à la plus ancienne. Toute modification suit le protocole habituel : proposition, feu vert explicite, puis ligne de journal et mise à jour de l'en-tête.

| Version | Date | Résumé |
|---|---|---|
| 1.0 | 2026-11-07 | Création, sur le modèle de la procédure de révision du projet Tizen_free, adaptée à NMS_TC : trois types de révision (outils, code, doc) et quatre modes, dont la révision complète dans l'ordre outils, code, doc ; reprend les outils, la configuration ESLint, les écarts acceptés et les budgets de `prompt_code_review_NMS_TC.md` (archivé). |

## HISTORIQUE DES RÉVISIONS

Une ligne par révision effectuée, proposée dans le compte rendu et ajoutée après feu vert.

| Date | Mode | Fichiers révisés (version, md5) | Livré (version, md5) | Résumé |
|---|---|---|---|---|
| 2026-11-07 | Code (avec l'ancien prompt) | `NMS_txt_code.html` v2.1 (`ab8a214b…`, 457 704 octets) | v2.2, `18555c10…` (462 234 octets) | 12 bugs ou défauts corrigés (dont 3 d'affichage mobile, 1 de robustesse de la langue mémorisée, 1 de polices), CSP, `<noscript>`, motif ARIA des onglets, nettoyage et commentaires harmonisés en français. |

---

## Voir aussi

[Prompt maître](prompts/prompt_revision_NMS_TC.md) · [Pièges](pitfalls.md) · [Scripts de contrôle](scripts/trans_script_0_README.md) · [Ajout d'une langue](prompts/prompt_add_language_NMS_TC.md) · [Feuille de route](../ROADMAP.md)
