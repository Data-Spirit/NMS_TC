<!-- Version du fichier 
> Version : 1.1
> Dernière modification : 2026-11-07
-->

# Pièges connus — NMS_TC

Les erreurs **déjà rencontrées** dans le projet, souvent vicieuses ou indirectes, avec la solution retenue, pour ne pas les refaire. Ce fichier sert aux trois types de révision ([procédure](revision.md), [prompt maître](prompts/prompt_revision_NMS_TC.md)) et à toute modification du guide, de la documentation ou des outils.

Chaque piège suit la même forme : **le symptôme**, **la cause**, **la solution**. Un piège nouveau, trouvé pendant une révision ou un travail courant, s'ajoute ici (sur proposition, comme toute modification du dépôt). Un piège devenu impossible (code supprimé, outil remplacé) se retire, et le compte rendu de la révision qui l'a constaté le dit.

---

## Guide (`LANG/NMS_txt_code.html`)

- **Rangée vide dans une grille CSS.** Masquer le *contenu* d'une cellule (`display:none` sur l'élément intérieur) laisse la cellule vide occuper une rangée de la grille (+14 px par ligne de couleur sur mobile, v2.1). **Masquer le conteneur** de la cellule.
- **Colonne écrasée à 0 px.** Un tableau à colonnes fixes en `width:100%` dans un conteneur à défilement ne défile jamais : la colonne libre est réduite à zéro (colonne « Texture de la balise » invisible à 375 px, v2.1). Donner au tableau une **largeur plancher** (`min-width`) pour que le conteneur défile.
- **Clé « constructor » trouvée.** Un objet littéral (`{}`) utilisé comme table de correspondance « trouve » `constructor`, `toString` ou `__proto__` : une langue mémorisée `constructor` était acceptée (`<html lang="constructor">`, v2.1). Toute table interrogée avec une valeur venue de l'utilisateur, de l'adresse ou du stockage : `Object.create(null)`, `Map` ou `Object.hasOwn`.
- **Icônes « non fonctionnelles » vues comme inconnues.** Elles existent dans `ICON_MAP` avec la valeur `""` : tester leur **existence** (`name in ICON_MAP`), jamais leur valeur. Même famille : une balise en minuscules (`circle_w`) doit recevoir la correction de casse, pas « inconnue ».
- **Faux gras.** Une graisse utilisée (`<strong>` en IBM Plex 700) mais non chargée est **synthétisée** par le navigateur ; une graisse chargée mais inutilisée coûte du réseau. Relever les graisses **calculées** dans un vrai navigateur et aligner l'adresse Google Fonts dessus.
- **Succès affiché sur un échec.** Le ✓ de copie s'affichait même quand le presse-papiers refusait. Un retour visuel ne se déclenche **qu'après** la confirmation du succès (sinon ✗).
- **Effets coûteux et invisibles.** `backdrop-filter` sous un fond opaque à 97 % et `transition: all` coûtent sans rien montrer : animer seulement les propriétés qui changent ; retirer un effet qu'on ne voit pas.
- **Préfixes à garder.** Stylelint signale `-webkit-mask-*` : c'est voulu (Safari < 15.4, anciens Chromium). Ne pas « corriger ».
- **Textes en dur légitimes.** Le `<title>` statique (repli sans JS) et le `<noscript>` (une phrase par langue) sont les **deux seules** exceptions à « aucun texte en dur » ; le `<noscript>` se complète à chaque nouvelle langue ([prompt d'ajout de langue](prompts/prompt_add_language_NMS_TC.md)).
- **Paramètres `{x}` de `T()`.** Ils sont insérés comme du HTML **de confiance** : n'y passer que des valeurs déjà échappées (`escapeHtml`).

## Langues et traductions

- **Une regex qui isole les blocs de langue en trouve un de trop.** Un commentaire du script principal contient le texte `<script type="application/json" id="i18n-XX">`. Ancrer la regex en **début de ligne** (drapeau multiligne) et **compter** les blocs trouvés (autant que de langues).
- **Une clé manquante ne se voit pas.** Le repli sur le français masque l'oubli à l'écran : seul `trans_script_1_check_keys.py --strict` le révèle.
- **Un texte source modifié ne se voit pas.** Sans la version précédente du guide (`--since`), le contrôle ne voit que les clés manquantes, pas les textes français changés : demander la version précédente, sinon l'écrire dans le rapport.
- **Langues délicates.** Écriture de droite à gauche, alphabets non couverts par les polices, accords du pluriel : voir la vérification préalable de [prompt_translation_HTML_GUIDE_LANG.md](prompts/prompt_translation_HTML_GUIDE_LANG.md).
- **Liens dans les textes du guide.** Décision du mainteneur : aucun lien vers le dépôt dans les textes du guide (une adresse peut changer) ; citer le dossier (`BANK_ICONS/`) en texte simple.

## Documentation, GitHub et GitHub Pages

- **Ancre de titre cassée par un émoji.** GitHub **conserve** le sélecteur de variation invisible `U+FE0F` de certains émojis (🖼️, ℹ️, ⚙️…) et compte ℹ comme une lettre : l'ancre de « 🖼️ Onglet Icônes » est `#️-onglet-icônes`, avec un caractère invisible. Les liens du sommaire écrits sans lui menaient nulle part (3 README, jusqu'à la v2.4). Solution : une **ancre statique** avant le titre (`<a id="tab-icons"></a>`), identique dans toutes les langues, comme `sec-N` dans `docs/guides/`. Vérifier une ancre en lisant les `id` réels de la page GitHub, jamais en la devinant.
- **GitHub Pages fabrique une page d'accueil.** Sans `index.html`, Jekyll transforme `README.md` en page d'accueil. Désactivé par `_config.yml` (`readme_index: enabled: false`) : la racine du site répond 404, volontairement.
- **Pages publie tous les Markdown.** Jekyll convertit chaque `.md` en page (`README_FR.html`, `CHANGELOG.html`, les prompts…), sauf dans les dossiers dont le nom commence par `_`. `docs/_legacy/` reste ainsi **hors de Pages, volontairement** : ne jamais ajouter de `.nojekyll`, qui le publierait.
- **Modifier `README_FR.md` change son md5.** Les README EN et ES tracent le md5 de leur source (commentaire « Translation parameters »), l'historique du prompt README aussi : toute modification de la source impose une nouvelle version, la mise à jour ciblée des traductions et leurs lignes d'historique.
- **Chiffres voués à devenir faux.** Poids du guide (~451 Ko), nombre de langues, de clés, d'icônes ou de lignes : les chercher partout (`grep`) à chaque changement ; préférer une formulation sans nombre quand elle suffit (« dans toutes les langues »).
- **Traces historiques.** Le CHANGELOG et les notes de version décrivent un état passé : ne pas les « mettre à jour » quand un fichier qu'ils citent est renommé ou archivé.

## Outils et vérifications

- **Le script 4 s'arrête au premier écart.** Un changement de balisage voulu (`<noscript>`, attributs ARIA) masque tous les écarts suivants. Neutraliser les changements attendus dans une copie du candidat, relancer, et ne conclure que lorsque **seuls les écarts voulus** restent.
- **jsdom n'est pas un navigateur.** Mise en page, polices, CSP, presse-papiers réel, drapeaux émoji : à vérifier dans un vrai navigateur.
- **Aperçu du navigateur intégré à l'application.** La page y est servie en `data:` : `localStorage` bloqué, `location.search` vide. Tester ces cas en appelant les fonctions directement (`matchLanguage`, `applyLanguage`) ou dans un vrai navigateur. Volet masqué : le défilement vers une ancre ne se produit pas, ce qui ne prouve pas que le lien est cassé.
- **ESLint ne trouve pas sa configuration.** `@eslint/js` doit être résolu depuis le dossier où il est installé : copier la configuration et le fichier à analyser dans le dossier temporaire `nm/` et lancer ESLint depuis lui.
- **Analyser le script principal.** Remplacer les chaînes base64 de `ICON_DATA` par un court texte avant ESLint : sinon le fichier est énorme et les messages illisibles.
- **Mesurer les performances dans jsdom.** jsdom est plusieurs fois plus lent qu'un navigateur (16,8 ms contre 2,2 ms pour le tableau complet des icônes) : un budget se vérifie dans un vrai navigateur.
- **Un contrôle vert avec un outil aveugle ne prouve rien.** Tester un outil sur un défaut connu (clé retirée, balise hostile, bloc cassé) avant de croire son « TOUT OK ».

## Environnement (Windows, shell, git)

- **`python` et `python3` ouvrent le Microsoft Store.** Utiliser `py -3` ; ajouter `-X utf8` pour l'affichage console (`PYTHONIOENCODING` est ignoré avec `-I`).
- **Les barres obliques inverses se perdent** dans un texte passé par heredoc ou en ligne de commande (`python -c`, `node -e`) : une chaîne Python devient invalide, une heredoc n'est plus fermée, une regex devient un commentaire. Écrire le script dans un fichier avec l'outil d'écriture de l'agent (une heredoc passée à son outil shell échoue aussi sur certaines apostrophes), éviter ce caractère quand c'est possible (par exemple `posixpath` pour les chemins), relire et tester après tout patch scripté.
- **`$?` après un tube.** Dans `script | tail`, `$?` est le code de sortie de `tail`, pas celui du script : rediriger la sortie vers un fichier, relever `$?`, puis lire le fichier.
- **Fins de ligne.** Les fichiers du dépôt sont en LF ; git avertit qu'il les convertira en CRLF à la prochaine opération : avertissement sans conséquence. Un script d'écriture relève les fins de ligne avant d'écrire et les conserve.
- **Ne pas toucher à l'index du mainteneur.** `git add`, y compris `git add -N` (« intention d'ajout ») pour un contrôle, modifie ce qu'il commitera : lister les fichiers non suivis avec `git ls-files --others --exclude-standard` à la place.

## Agent (Claude Code)

- **Hook GateGuard.** Avant la création ou la première modification de chaque fichier, il bloque l'écriture et demande d'énoncer dans le message ce que le fichier remplace ou qui l'utilise, ce que la modification corrige, et la consigne du mainteneur citée mot pour mot ; puis réessayer. Pas d'écritures parallèles sur un même fichier.
- **Mémoire de l'agent.** Hors dépôt : la relire en fin de révision (fiches à jour, sans doublon ni information périmée).

---

## Voir aussi

[Procédure de révision](revision.md) · [Prompt maître de révision](prompts/prompt_revision_NMS_TC.md) · [Scripts de contrôle](scripts/trans_script_0_README.md) · [Ajout d'une langue](prompts/prompt_add_language_NMS_TC.md)
