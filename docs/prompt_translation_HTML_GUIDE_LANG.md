# Translation Prompt — NMS_TC HTML Guide

Prompt réutilisable pour traduire le fichier `NMS_txt_code_<LANG>.html` (le guide interactif autonome) dans une nouvelle langue.
Pour une nouvelle traduction : copier ce fichier, changer uniquement le bloc `TARGET`, et donner ce fichier + le `NMS_txt_code_FR.html` source à Claude.

Ce prompt est le pendant technique de `translation_prompt_README_LANG.md`. Les deux partagent la même exigence de qualité et la même terminologie (voir §6 Cohérence terminologique), mais celui-ci s'applique à un fichier **HTML/CSS/JS fonctionnel**, pas à un texte pur : une erreur ici peut casser une fonctionnalité, pas seulement une phrase.

> **Note (depuis l'audit de code du fichier source FR)** : le fichier `NMS_txt_code_FR.html` a été réorganisé structurellement — notamment le bloc `ICON_DATA` (données base64 des icônes), déplacé du milieu du script vers la toute fin, juste avant les appels d'initialisation. Ceci ne change rien aux règles de traduction ci-dessous, mais si vous comparez avec d'anciennes versions traduites (EN/ES antérieures à cet audit), ne vous étonnez pas de retrouver certains blocs à un autre endroit du fichier : c'est un réagencement volontaire, pas une anomalie.

---

## TARGET

```yaml
target_language: English            # ex: English, Deutsch, Español, 日本語
target_variant: neutral/standard    # ex: US, UK, neutral/standard, none
lang_code: EN                       # code à 2 lettres majuscules — DOIT être identique à celui utilisé pour le README correspondant
output_filename: NMS_txt_code_EN.html   # convention : NMS_txt_code_<lang_code>.html
source_file: NMS_txt_code_FR.html
html_lang_attribute: en             # code ISO 639-1 minuscule pour l'attribut <html lang="...">
tone: passionate/stylized           # ex: passionate/stylized, neutral/technical, compromise — ton éditorial à conserver ou adapter
fidelity_style: idiomatic           # ex: idiomatic (adaptation naturelle), literal (fidèle/littérale), case-by-case
companion_readme: README_EN.md      # README déjà traduit dans cette langue, s'il existe — pour cohérence terminologique (voir §3 et règle ci-dessous)
```

---

## RÈGLE DE DÉMARRAGE OBLIGATOIRE — à exécuter avant toute traduction, même répétée

**Ne jamais présumer que les valeurs de `TARGET` (notamment `tone` et `fidelity_style`) restent valables d'une session à l'autre, même si cette même personne a déjà utilisé ce prompt auparavant avec des valeurs identiques.** Une session de traduction précédente ne vaut pas confirmation pour la session en cours.

Avant de commencer toute traduction, reformuler explicitement à la personne les valeurs actuelles de `target_language`, `target_variant`, `tone` et `fidelity_style` (en précisant, le cas échéant, le choix fait lors d'un usage précédent comme simple rappel, jamais comme valeur acquise), et demander confirmation ou modification. Ne démarrer la traduction qu'après cette confirmation explicite.

## RÈGLE DE VÉRIFICATION DU FICHIER SOURCE — à exécuter avant toute traduction

Avant de commencer, confirmer explicitement à la personne :
1. Le nom exact du fichier source utilisé.
2. Son nombre de lignes (ou une autre métrique simple : taille en octets, hash).
3. Au moins un élément structurel distinctif permettant de confirmer qu'il s'agit bien de la dernière version en date (ex. présence de `FLAG_LABELS`, de `copyButtonHtml()`, position du bloc `ICON_DATA`) — en particulier dans une conversation longue où plusieurs versions du fichier ou du prompt ont pu circuler.

Ne jamais réutiliser silencieusement un fichier ou une traduction produite lors d'un tour précédent de la conversation sans revalider explicitement qu'il s'agit bien de la version la plus récente fournie.

---

## RÔLE

Tu es à la fois **traducteur technique** et **développeur front-end rigoureux**. Tu traduis un fichier HTML autonome (HTML + CSS + JavaScript vanilla dans un seul fichier) sans jamais casser son fonctionnement. Chaque modification de texte doit être vérifiée pour ses répercussions techniques avant d'être appliquée : dans ce fichier, du texte "de contenu" (noms de catégories, libellés) fait aussi office de donnée logique (clé de regroupement, valeur de filtre, clé de correspondance). Une traduction fidèle mais qui casse une correspondance de clé est un échec, pas une réussite partielle.

---

## PÉRIMÈTRE DE LA TRADUCTION — CE QUI SE TRADUIT

### A. Texte HTML visible
- Contenu du `<title>`.
- Tout le texte des 4 onglets (Infos/Couleurs/Icônes/À propos) : titres `h1`/`h2`/`h3`, paragraphes, listes, encadrés (`.protip`, `.important-box`, `.warn-box`, `.info-box`), libellés de la barre de simulateur, texte du footer.
- Libellés des boutons d'onglets (`Infos`, `Couleurs`, `Icônes`, `À propos`).
- Placeholders des champs de recherche (`placeholder="..."`).
- Attributs `aria-label` sur les champs de recherche (`#color-search`, `#icon-search`) et sur le filtre de catégorie (`#icon-cat-filter`) — destinés aux lecteurs d'écran.

  **Choix de style à valider avec la personne avant de traduire** (ce n'est pas qu'une question de langue, c'est un choix d'accessibilité) :
  - **Option A — miroir du placeholder** : reprendre le texte du placeholder correspondant, sans la partie exemples (ex. `Search a color tag`). Cohérence visuelle/sonore maximale entre les deux.
  - **Option B — libellé autonome pensé pour l'oral** : rédiger un texte indépendant, optimisé pour être compris hors contexte visuel par une voix de synthèse (ex. `Color tag search field`). Recommandé par les bonnes pratiques WCAG, car un lecteur d'écran n'a pas le contexte visuel du placeholder à côté.

  Ne pas choisir par défaut : demander la préférence à la personne avant de traduire ces 3 attributs, sauf si un choix a déjà été explicitement validé pour ce projet — auquel cas le rappeler comme au §RÈGLE DE DÉMARRAGE ci-dessus (rappel, pas présomption).
- Attribut `lang` de la balise `<html>` → utiliser `html_lang_attribute` défini dans `TARGET`.

### B. Texte généré dynamiquement en JavaScript (chaînes littérales dans le code)
Ces chaînes n'apparaissent pas comme texte HTML statique mais sont injectées au rendu — elles doivent être traduites avec la même rigueur que le texte visible :
- Libellés de badges de statut : `doublon`, `non fonctionnel`, `à vérifier`. *(Depuis l'audit de code : ces trois libellés sont désormais regroupés dans une seule constante `FLAG_LABELS` en début de section de rendu des icônes, au lieu d'un enchaînement de conditions dispersé dans le code — plus facile à repérer d'un coup d'œil.)*
- En-têtes de tableau générés en JS : `Aperçu`, `Balise`, `Chemin texture`.
- Option par défaut du filtre catégorie : `Toutes catégories`.
- Message d'absence de résultat : `Aucun résultat.`
- Compteurs dynamiques : le suffixe `' balises'` (dans `rows.length + ' / ' + COLORS.length + ' balises'` et son équivalent pour les icônes).
- Pastille de transparence : `transparence ${...}%`.
- Gabarit de texte copié pour les couleurs : `Texte` dans `` `<${tag}>Texte</>` `` (c'est un exemple de texte que l'utilisateur va coller puis remplacer en jeu — traduire ce mot-témoin, ex. `Text` en anglais).
- Préfixe des tooltips de copie : `Copier : ${...}` → traduire uniquement `Copier :`, jamais le contenu de `${...}` (qui est un fragment de code de balise). *(Depuis l'audit de code : ce préfixe est désormais centralisé dans une seule fonction `copyButtonHtml()` au lieu d'être dupliqué à deux endroits du fichier — une seule occurrence à vérifier, ce qui réduit le risque d'oubli.)*
- Attribut `title` généré pour l'aperçu d'icône teintée : `title="${iconTag} teinté ${colorTag}"` → traduire uniquement le mot `teinté`.

### C. Noms de catégories (le point le plus sensible du fichier)
Les catégories suivantes apparaissent comme **4ᵉ champ dans le tableau `COLORS`** et **3ᵉ champ dans le tableau `ICONS`**. Elles servent à la fois de texte affiché ET de valeur de regroupement/filtrage :

**Catégories de couleurs** : Joueurs, Génériques, Transmissions / Missions, Compagnons, Carte galactique, Ressources, États / valeurs, Marchandises / Tech, Titres, Missions.

**Catégories d'icônes** : Ressources, Interface, Frégates, Symboles de portail, Inventaire, Voix / Réseau, Butin, Plateformes / Contrôles, Classe (C→S), Modes de jeu, Édition de base, Non fonctionnel.

**Règle absolue** : construire d'abord un petit glossaire fixe *catégorie française → catégorie cible* (une seule fois), puis l'appliquer **à l'identique, caractère pour caractère, à chaque occurrence** de cette catégorie dans tout le fichier — y compris :
1. Chaque ligne du tableau `COLORS` où elle apparaît comme 4ᵉ élément.
2. Chaque ligne du tableau `ICONS` où elle apparaît comme 3ᵉ élément.
3. Le commentaire de section juste au-dessus du bloc correspondant dans `ICONS` (ex. `// Ressources`, `// Frégates`).
4. **La clé de l'objet `CATEGORY_DESCRIPTIONS`** — actuellement `"Classe (C→S)"`. Cette clé DOIT être remplacée par la traduction exacte utilisée pour cette catégorie dans le tableau `ICONS`, au caractère près (mêmes espaces, mêmes parenthèses, même flèche `→`). Si la clé ne correspond plus exactement à la valeur de catégorie utilisée dans les lignes `ICONS`, la description associée disparaît silencieusement du rendu — sans erreur, sans avertissement. **Vérifier ce point explicitement avant de livrer.**

### D. Commentaires de code (HTML / JavaScript / CSS)
Traduire l'intégralité des commentaires, sous toutes leurs formes, pour livrer un fichier source cohérent, entièrement en langue cible :
- Commentaires JS/CSS (`//` et `/* */`) — y compris les commentaires de section (`/* ==== DATA ==== */` reste tel quel s'il est déjà en anglais générique, mais les commentaires en français comme `// Ordre de référence défini manuellement...` doivent être traduits).
- **Commentaires HTML (`<!-- ... -->`)** — présents notamment comme marqueurs de section dans le `<body>` (ex. `<!-- ============ INFOS TAB ============ -->`). Ces marqueurs doivent rester cohérents avec le libellé d'onglet traduit correspondant : si l'onglet visible devient `Info` (singulier) en anglais, le commentaire doit devenir `<!-- ============ INFO TAB ============ -->` et non rester sur l'ancien libellé `INFOS TAB`.

---

## PÉRIMÈTRE DE LA TRADUCTION — CE QUI NE SE TRADUIT JAMAIS

- **Noms de balises NMS** : toute chaîne en MAJUSCULES_AVEC_UNDERSCORE dans les tableaux `COLORS` et `ICONS` (1ᵉʳ champ) — `VISOR`, `PET1`, `TECH1`, `PR_0`…`PR_15`, `BULLETPOINT_OFF`, etc. Ce sont des identifiants du jeu, jamais du texte.
- **Codes hexadécimaux** (`#FF776F`…) et valeurs d'opacité numériques.
- **Chemins de texture** internes au jeu (`TEXTURES/UI/FONTS/...DDS`), noms de fichiers PNG (`sclass.png`…). Seules les valeurs littérales `(chemin non listé)` et `— aucun chemin assigné` et `— symbole de portail` sont du texte à traduire (elles apparaissent comme 4ᵉ champ du tableau `ICONS`, à la place d'un vrai chemin) — attention à ne pas les confondre avec les vrais chemins `.DDS`.
- **Toutes les données `ICON_DATA`** : chaînes base64 des images, à ne jamais toucher, modifier, reformater ou même relire en profondeur (juste ne pas y toucher).
- **Noms de classes CSS, ID HTML, noms de variables et fonctions JavaScript** (`COLORS`, `ICONS`, `ICON_DATA`, `CATEGORY_DESCRIPTIONS`, `renderIcons`, `.copy-btn`, `#color-search`, etc.) — modifier un identifiant casse le fichier.
- **Les 10 exemples concrets de `CONTAINER_EXAMPLES`** (`Techs`, `Metals 1`, `Elmt/Comp`, `DATAs`, `Upgrade 1`, `Upgrade 2`, `MISC`, `Plants`, `Metals 2`, `Alloys`) : ce sont des noms réellement utilisés en jeu par l'auteur, déjà à consonance anglaise/abrégée. Les conserver **strictement identiques**, quelle que soit la langue cible — ne jamais les traduire ni les adapter.
- **Liens et attributions** : URL GitHub, nom "Spirit", noms de polices (Rajdhani, IBM Plex Sans, JetBrains Mono), "Hello Games", "No Man's Sky".
- **La syntaxe des balises elle-même** dans les exemples de code affichés (`<PET1><IMG>TECH1<></>` etc.) — ne jamais modifier ces chaînes, elles doivent rester exécutables telles quelles en jeu.

---

## PARAMÈTRES ÉDITORIAUX (cohérents avec le README)

### 1. Fidélité vs fluidité
Adaptation naturelle idiomatique, comme pour le README : reformuler pour un rendu naturel en langue cible, sans jamais perdre le sens technique exact. En cas de doute, privilégier la précision technique sur l'élégance stylistique — un README peut se permettre une image, une info-bulle d'interface ne peut pas se permettre une ambiguïté.

### 2. Ton et registre
Conserver le même ton que celui déjà établi pour le README de cette langue (passionné, direct, vulgarisé sans être familier). Les deux documents décrivent le même projet et doivent sonner comme écrits par la même personne.

### 3. Cohérence terminologique bidirectionnelle avec le README correspondant
Le README et ce guide HTML décrivent le même produit et doivent employer un vocabulaire strictement identique — cette règle fonctionne dans les deux sens selon lequel des deux documents a été traduit en premier, pas seulement du HTML vers le README.

- **Si `companion_readme` (défini dans `TARGET`) existe déjà et a déjà été traduit** : le relire avant de traduire ce fichier HTML, et réutiliser exactement les mêmes choix de traduction pour les termes récurrents du projet (ex. si « balise » a été traduit par « tag » dans le README, utiliser « tag » partout ici aussi ; idem pour « teinte/teinter » → « tint/tinting », « doublon » → « duplicate », etc.).
- **Si ce fichier HTML est traduit en premier, avant tout README dans cette langue** : les choix de terminologie faits ici (noms de catégories, libellés de badges, termes récurrents) font alors référence — le prompt `translation_prompt_README_LANG.md` s'appuiera dessus via son propre champ `companion_html_guide` lors de la traduction ultérieure du README. Pas d'action spécifique à faire ici dans ce cas, si ce n'est de traduire avec la même rigueur terminologique que si le README existait déjà, puisque ce fichier deviendra lui-même la référence.

### 4. Longueur des chaînes d'interface
Certaines chaînes traduites s'affichent dans des espaces contraints par du CSS (`.color-cat`, `.flag`, boutons, onglets). Privilégier, quand plusieurs formulations naturelles existent, celle qui reste raisonnablement courte et proche en longueur de l'original — sans sacrifier la clarté pour autant. Ne pas modifier le CSS pour compenser : signaler seulement si une chaîne semble poser un risque de débordement visuel.

---

## RÈGLES TECHNIQUES DE SÉCURITÉ (spécifiques au HTML/JS)

1. **Ne jamais modifier la structure du fichier** : mêmes balises HTML, même imbrication, mêmes attributs (hors valeurs de contenu et `lang`), même CSS, même logique JavaScript, mêmes noms de fonctions/variables/classes/ID.
2. **Ne jamais reformater ou "nettoyer" le code** : conserver l'indentation, les sauts de ligne et le style de code d'origine à l'identique. Cette traduction est un remplacement de chaînes de caractères, pas une réécriture.
3. **Respecter l'échappement existant** : toute chaîne traduite insérée dans un attribut HTML ou un template JavaScript doit respecter le même échappement de guillemets/apostrophes/accents que l'original (attention en particulier aux apostrophes françaises dans du code déjà entouré de guillemets simples en JS — vérifier qu'aucune apostrophe anglaise du type `don't` ne casse une chaîne délimitée par `'...'`).
4. **Vérifier la correspondance exacte des clés d'objet après traduction** (voir §C règle absolue ci-dessus) — c'est le point de rupture silencieuse le plus probable de tout ce fichier.
5. **Ne jamais toucher aux données `ICON_DATA`, aux valeurs hexadécimales, aux chemins `.DDS`, ni à la syntaxe des balises NMS dans les exemples de code.**
6. **Le fichier doit rester un fichier `.html` unique et autonome** : ne pas extraire le CSS ou le JS dans des fichiers séparés, ne pas ajouter de dépendance externe.

---

## VÉRIFICATION FINALE (auto-relecture obligatoire avant livraison)

- [ ] `<html lang="...">` correspond bien à `html_lang_attribute` défini dans `TARGET`.
- [ ] `<title>` traduit.
- [ ] Les 4 onglets, tous les encadrés, le footer et le simulateur sont intégralement traduits — aucune phrase française oubliée.
- [ ] Toutes les chaînes JS listées en §B (badges, en-têtes de tableau, compteurs, tooltips, placeholder de copie, "Toutes catégories", "Aucun résultat.") sont traduites.
- [ ] Les 3 `aria-label` (recherche couleurs, recherche icônes, filtre catégorie) sont traduits et cohérents avec le placeholder correspondant sur le même champ.
- [ ] Chaque nom de catégorie a été traduit **à l'identique partout** où il apparaît (tableaux `COLORS`/`ICONS`, commentaires de section, et surtout la clé de `CATEGORY_DESCRIPTIONS`) — vérifier caractère par caractère, en particulier les espaces autour de `/` et la flèche `→`.
- [ ] Aucun nom de balise NMS, chemin `.DDS`, code hex, nom de fichier PNG, ID HTML, classe CSS, nom de variable/fonction JS n'a été traduit ou modifié.
- [ ] Les 10 entrées de `CONTAINER_EXAMPLES` sont restées strictement identiques à la source.
- [ ] Tous les commentaires de code sont traduits, HTML compris (§D) — vérifier en particulier que les marqueurs `<!-- ... TAB ... -->` correspondent au libellé d'onglet traduit.
- [ ] La terminologie utilisée correspond à celle de `companion_readme` quand ce README existe déjà pour cette langue — sinon, la terminologie choisie ici est cohérente en interne et prête à servir de référence pour la traduction ultérieure du README.
- [ ] Aucune balise HTML, accolade JS ou guillemet n'a été cassé par une chaîne traduite mal échappée — relire spécifiquement les lignes où une traduction contient une apostrophe.
- [ ] Le fichier reste un unique `.html` autonome, structurellement identique à la source (aucune section ajoutée/supprimée/déplacée).

---

## LIVRABLE ATTENDU

Un unique fichier `.html` nommé selon `output_filename`, fonctionnellement identique au fichier source (même simulateur, mêmes tris, mêmes filtres, mêmes tableaux, mêmes 145 icônes intégrées), avec l'intégralité du texte visible et des chaînes de code traduites en langue cible, prêt à être ouvert directement dans un navigateur sans aucune retouche supplémentaire.

---

## HISTORIQUE D'UTILISATION

Table à compléter à chaque usage de ce prompt, pour tracer quelle version de quel fichier a été traduite, avec quels réglages — évite toute ambiguïté en cas de reprise de ce prompt dans une conversation ultérieure ou par une autre personne.

| Date | Fichier source (nom + repère de version) | Fichier produit | `target_language` | `target_variant` | `tone` | `fidelity_style` |
|---|---|---|---|---|---|---|
| 2026-09-08 | `NMS_txt_code_FR.html` (1298 lignes, avec `FLAG_LABELS`/`copyButtonHtml()`/`ICON_DATA` en fin de fichier) | `NMS_txt_code_EN.html` | English | neutral/standard | passionate/stylized | idiomatic |
