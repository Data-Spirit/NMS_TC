# Translation Prompt — NMS_TC HTML Guide

> **Dernière mise à jour de ce prompt : 2026-09-09 (4)** — correction de références internes obsolètes (`translation_prompt_README_LANG.md` → `prompt_translation_README_LANG.md`), ajout de la politique de retraduction depuis la version à jour (jamais porter/compléter une ancienne traduction), et ajout d'un §0 explicite de correspondance des suffixes de langue, en miroir du prompt README. S'ajoute aux changements précédents du même jour (protocole de fraîcheur, rôle des trois fichiers, protection des modifications de ce prompt, feu vert de traduction, règle des pseudo-noms NAME_COLOR/NAME_ICON, vérifications techniques recommandées, traçabilité `companion_readme` dans l'historique). Cette ligne doit être mise à jour à chaque modification validée de ce prompt (voir section « PROTECTION DES MODIFICATIONS DE CE PROMPT ») — si elle semble absente ou visiblement ancienne par rapport au contenu, traiter ce prompt comme potentiellement obsolète et le signaler à la personne avant de l'utiliser.

Prompt réutilisable pour traduire le fichier `NMS_txt_code_<LANG>.html` (le guide interactif autonome) dans une nouvelle langue.
Pour une nouvelle traduction : copier ce fichier, changer uniquement le bloc `TARGET`, et donner ce fichier + le `NMS_txt_code_FR.html` source à Claude.

Ce prompt est le pendant technique de `prompt_translation_README_LANG.md`. Les deux partagent la même exigence de qualité et la même terminologie (voir la section « PARAMÈTRES ÉDITORIAUX » plus bas, §3 Cohérence terminologique), mais celui-ci s'applique à un fichier **HTML/CSS/JS fonctionnel**, pas à un texte pur : une erreur ici peut casser une fonctionnalité, pas seulement une phrase.

> **Note (depuis l'audit de code du fichier source FR)** : le fichier `NMS_txt_code_FR.html` a été réorganisé structurellement — notamment le bloc `ICON_DATA` (données base64 des icônes), déplacé du milieu du script vers la toute fin, juste avant les appels d'initialisation. Ceci ne change rien aux règles de traduction ci-dessous, mais si vous comparez avec d'anciennes versions traduites (EN/ES antérieures à cet audit), ne vous étonnez pas de retrouver certains blocs à un autre endroit du fichier : c'est un réagencement volontaire, pas une anomalie. **Toute retraduction doit repartir de cette version à jour du fichier `.html` source, jamais porter/compléter une ancienne traduction existante** — une traduction antérieure (EN/ES ou autre) ne sert jamais de base de travail, même partiellement ; elle peut tout au plus être consultée comme référence terminologique via `companion_readme` (voir plus bas), après vérification de sa fraîcheur.

---

### 0. Règle de correspondance des suffixes de langue (IMPORTANT)

Ce guide HTML a un README compagnon (voir tableau ci-dessus), et **les deux fichiers doivent toujours partager le même suffixe de langue** :

| Guide HTML | README documentant ce guide |
|---|---|
| `NMS_txt_code_FR.html` | `README_FR.md` |
| `NMS_txt_code_EN.html` | `README_EN.md` |
| `NMS_txt_code_ES.html` | `README_ES.md` |
| `NMS_txt_code_<lang_code>.html` | `README_<lang_code>.md` |

Le nom du fichier produit (`output_filename` dans `TARGET`) doit toujours suivre la convention `NMS_txt_code_<lang_code>.html`, où `<lang_code>` est exactement celui défini dans `TARGET`. Cette règle vaut uniquement pour le guide HTML (`prompt_translation_HTML_GUIDE_LANG.md`) ; le prompt `prompt_translation_README_LANG.md` gère la règle miroir pour le README — les deux prompts sont complémentaires mais indépendants.

---

## LES TROIS FICHIERS FOURNIS — RÔLE DE CHACUN (à lire avant tout le reste)

Une session de traduction avec ce prompt fournit typiquement trois fichiers. Chacun a un rôle précis et **un seul des trois est le texte à traduire** :

| Fichier | Rôle | Faut-il le traduire ? |
|---|---|---|
| `NMS_txt_code_<LANG_SOURCE>.html` (ex. `NMS_txt_code_FR.html`) | **La source** : le guide HTML à traduire vers `target_language`. | **Oui — c'est l'unique cible de la traduction.** |
| `prompt_translation_HTML_GUIDE_LANG.md` (ce fichier) | Le mode d'emploi : quoi traduire, quoi ne jamais toucher, comment vérifier. | Non — c'est la consigne, pas un contenu à traduire. |
| `README_<LANG_SOURCE>.md` (ex. `README_FR.md`, fourni dans la même langue que le HTML source) | Un **document de contexte**, donné pour que la traduction du HTML soit fidèle à la conception réelle du projet (pourquoi telle section existe, comment telle fonctionnalité a été pensée, etc.). | **Non, jamais dans cette session.** Ce README n'est pas la cible — il n'est là que pour informer la traduction du HTML. Le traduire relèverait d'une tout autre session, avec `prompt_translation_README_LANG.md`. |

**Repère utile (signal, pas règle absolue)** : si la personne fournit `prompt_translation_HTML_GUIDE_LANG.md`, l'intention est presque toujours de traduire le HTML, pas le README qui l'accompagne — et symétriquement, si elle fournit `prompt_translation_README_LANG.md`, l'intention est de traduire le README. Un README fourni à côté du prompt HTML (ou l'inverse) est là pour du **contexte**, pas comme cible implicite. En cas de doute réel sur l'intention, poser la question plutôt que présumer.

**À ne pas confondre avec `companion_readme`** (voir bloc `TARGET` et §3 plus bas) : ce README de contexte est dans la **langue source** (celle du HTML à traduire, souvent le français) — il ne peut donc pas servir de référence terminologique pour la langue cible. `companion_readme` désigne un cas différent : un `README_<lang_code>.md` **déjà traduit dans la langue cible** (ex. `README_ES.md` pour une traduction vers l'espagnol), utilisé pour réutiliser le même vocabulaire d'une langue à l'autre. Les deux notions peuvent coexister dans une même session mais ne sont jamais le même fichier.

**`companion_readme` n'est en jeu que si la personne le fournit ou le désigne explicitement pour la session en cours.** Ne jamais aller chercher de soi-même, dans l'historique de la conversation, un README déjà traduit dans la langue cible lors d'un tour antérieur pour le traiter comme `companion_readme` — même s'il existe, même s'il porte le nom attendu (`README_<lang_code>.md`). Tant que la personne n'a pas explicitement indiqué qu'un tel fichier doit servir de référence pour cette session, `companion_readme` est considéré comme **absent**, un point c'est tout : ne pas le mentionner, ne pas le proposer, ne pas y faire référence. Un cas fréquent (comme dans ce projet) : seuls le HTML source et son README de contexte en langue source sont fournis, avec l'intention explicite de traduire le README correspondant *plus tard*, dans un tour ultérieur séparé. Dans ce cas, cette traduction du HTML est **autosuffisante** et devient elle-même la référence terminologique pour la traduction future du README (voir §3) — sans qu'il soit utile ni pertinent de rouvrir la question d'un `companion_readme` existant ou non.

**Note de portée** : ce prompt suppose implicitement que la langue source du HTML est le français (`NMS_txt_code_FR.html`, onglets `Infos/Couleurs/Icônes/À propos`), conformément au fait que le français est la langue de référence maîtresse du projet (voir `README_FR.md`). Si un jour la langue source d'une traduction demandée n'est pas le français (ex. traduire depuis un `NMS_txt_code_EN.html`), le rôle des fichiers reste le même mais les exemples de libellés ci-dessous doivent être adaptés en conséquence — signaler ce cas à la personne s'il se présente plutôt que de présumer silencieusement.

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
companion_readme: README_EN.md      # README déjà TRADUIT dans la langue cible — à renseigner UNIQUEMENT si la personne le fournit ou le désigne explicitement pour cette session. Ne jamais le déduire d'un fichier déjà vu dans la conversation. Laisser vide/absent si non fourni : cette traduction HTML devient alors elle-même la référence terminologique (voir §3).
```

---

## RÈGLE DE DÉMARRAGE OBLIGATOIRE — à exécuter avant toute traduction, même répétée

**Ne jamais présumer que les valeurs de `TARGET` (notamment `tone` et `fidelity_style`) restent valables d'une session à l'autre, même si cette même personne a déjà utilisé ce prompt auparavant avec des valeurs identiques.** Une session de traduction précédente ne vaut pas confirmation pour la session en cours.

Avant de commencer toute traduction, reformuler explicitement à la personne les valeurs actuelles de **`target_language`, `target_variant`, `tone`, `fidelity_style`, et le style des 3 attributs `aria-label` (Option A miroir du placeholder / Option B libellé autonome, voir §A plus bas)** — cette dernière n'étant pas un simple choix de langue mais un choix d'accessibilité à part entière, elle doit être reconfirmée avec la même rigueur que les autres paramètres, pas laissée à la seule mention isolée du §A. Préciser, le cas échéant, le choix fait lors d'un usage précédent comme simple rappel, jamais comme valeur acquise, et demander confirmation ou modification. Ne démarrer la traduction qu'après cette confirmation explicite.

## RÈGLE DE FRAÎCHEUR DES FICHIERS FOURNIS — à exécuter avant toute traduction

**Un nom de fichier identique ne garantit jamais un contenu identique.** Que ce soit le fichier HTML source, ce prompt lui-même, ou un README de contexte/`companion_readme` : si l'un de ces fichiers est fourni à nouveau au cours d'une conversation (même sous le nom exact déjà vu précédemment), il faut le traiter comme potentiellement différent de la version déjà en mémoire — **jamais comme un doublon silencieux**. En pratique, si la personne redonne un fichier portant un nom déjà rencontré, c'est le plus souvent précisément *parce qu'il a été mis à jour, corrigé ou enrichi* depuis la dernière fois.

Avant de commencer, pour **chacun** des fichiers fournis dans le tour de conversation en cours :

1. **Fichier source HTML** : confirmer explicitement à la personne son nom, son nombre de lignes (ou une autre métrique simple : taille en octets), et au moins un élément structurel distinctif permettant de vérifier qu'il s'agit bien de la dernière version en date (ex. présence de `FLAG_LABELS`, de `copyButtonHtml()`, position du bloc `ICON_DATA`). **Attention : le nombre de lignes seul est un indice, pas une preuve** — deux versions différentes peuvent coïncidentellement partager le même nombre de lignes. En cas de doute réel (versions proches, différences suspectées mais non confirmées), calculer et comparer un hash (`md5sum`) est une vérification plus robuste.
2. **README de contexte fourni avec ce tour** (s'il y en a un) : ne pas se contenter de le lire — comparer sa structure de titres/sections avec toute version de ce même README déjà vue dans la conversation, pour confirmer qu'il s'agit bien de la version la plus à jour.
3. **`companion_readme`** (uniquement s'il a été explicitement fourni ou désigné par la personne pour cette session — jamais rappelé de mémoire de sa propre initiative, voir règle ci-dessus) : **avant de l'utiliser comme référence terminologique**, comparer sa structure (titres, callouts, sections distinctives comme des blocs `🔧 Détail technique`) avec celle du README de contexte en langue source fourni dans le tour actuel. Si des éléments distinctifs présents côté source sont absents côté `companion_readme`, ce dernier est **obsolète** : ne pas l'utiliser tel quel comme référence terminologique sans le signaler explicitement à la personne, décrire précisément ce qui manque, et lui demander comment procéder (le retraduire d'abord, s'appuyer uniquement sur les termes de base déjà validés, ou traiter ce fichier HTML comme la nouvelle référence terminologique).

Ne jamais réutiliser silencieusement un fichier ou une traduction produite lors d'un tour précédent de la conversation sans revalider explicitement qu'il s'agit bien de la version la plus récente fournie.

---

## PROTECTION DES MODIFICATIONS DE CE PROMPT — distincte de la traduction elle-même

Ce prompt est un document de référence, pas un brouillon de travail. Toute modification de ce fichier
(correction, clarification, ajout de règle) suit un protocole en deux temps, symétrique au « feu vert »
qui déclenche une traduction :

1. **Proposer d'abord, modifier ensuite.** Présenter à la personne, en langage clair, les changements
   envisagés et pourquoi ils sont nécessaires — sans toucher au fichier à ce stade.
2. **Attendre une confirmation explicite et non ambiguë** avant d'appliquer quoi que ce soit
   (ex. « tu as le feu vert », ou toute formulation équivalente de la personne). Une demande de
   correction du type « corrige X dans le prompt » n'est PAS en soi une validation du texte précis
   proposé — elle déclenche une proposition, pas une écriture immédiate.
3. **Ne jamais enchaîner un second lot de modifications sur la lancée d'un premier lot validé**, même
   dans le même tour de conversation. Chaque lot distinct de changements est proposé puis validé
   séparément — la validation d'un lot ne vaut pas blanc-seing pour le suivant.
4. **Mettre à jour la ligne de changelog en tête de ce fichier** (« Dernière mise à jour de ce prompt »)
   à chaque modification effectivement appliquée, avec la date et un résumé bref — c'est ce qui permet
   de détecter si ce prompt lui-même est obsolète lors d'une session future (voir règle de fraîcheur).

Ce protocole est indépendant de celui qui encadre la traduction du HTML lui-même (section suivante) : traduire
le HTML et modifier les instructions de traduction sont deux gestes distincts, chacun avec son propre feu vert,
jamais l'un ne couvrant l'autre.

---

## ATTENDRE LE FEU VERT AVANT DE TRADUIRE

Toutes les étapes de validation ci-dessus (rôle des fichiers, fraîcheur, paramètres `TARGET` reformulés et
confirmés) doivent être **terminées et explicitement validées par la personne** avant qu'une seule ligne du
fichier `.html` cible ne soit écrite. Concrètement :

1. Vérifier la fraîcheur des fichiers fournis (voir règle ci-dessus).
2. Reformuler et faire valider les paramètres `TARGET` (voir règle de démarrage ci-dessus), y compris le choix
   `aria-label`.
3. Poser toute question nécessaire pour lever une ambiguïté restante.
4. **Ne commencer la traduction qu'après une phrase de confirmation explicite et non ambiguë de la personne**
   (ex. « c'est bon tu as le feu vert », « c'est bon tu peux utiliser le prompt pour traduire... », ou toute
   formulation équivalente désignant sans ambiguïté le feu vert pour *traduire*, distincte du feu vert qui
   couvrirait une modification de ce prompt — voir section précédente).

Cette règle vaut même si la personne a déjà donné ce feu vert lors d'un usage antérieur de ce prompt dans la
même conversation : chaque nouvelle traduction (nouvelle langue, nouvelle version du fichier source, etc.)
redemande sa propre confirmation explicite.

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

### A bis. Pseudo-noms de balises génériques (placeholders pédagogiques)
Le HTML statique utilise deux pseudo-noms de balises à visée purement pédagogique, `NAME_COLOR` et `NAME_ICON` — ils illustrent la forme générale de la syntaxe (dans le bandeau d'aide du simulateur en hero, et dans la section « Syntaxe » de l'onglet Infos) mais **ne sont pas de vraies balises du jeu** : ils n'apparaissent dans aucune ligne des tableaux `COLORS`/`ICONS`, contrairement aux vrais identifiants comme `VISOR` ou `PET1`.

**Règle (validée) : les traduire**, contrairement aux vraies balises NMS qui elles restent toujours intactes. Conserver la structure `MOT_MOT` en MAJUSCULES_AVEC_UNDERSCORE, en traduisant les deux mots dans la langue cible. Exemple validé pour l'espagnol : `NAME_COLOR` → `NOMBRE_COLOR`, `NAME_ICON` → `NOMBRE_ICONO`. Appliquer ce même principe de traduction du couple de mots pour toute autre langue cible. Traduire **toutes** les occurrences de ces deux pseudo-noms, qu'elles soient dans le bandeau d'aide du simulateur ou dans l'onglet Infos — ne pas en oublier une par inadvertance en ne traitant qu'un seul des deux emplacements.


### B. Texte généré dynamiquement en JavaScript (chaînes littérales dans le code)
Ces chaînes n'apparaissent pas comme texte HTML statique mais sont injectées au rendu — elles doivent être traduites avec la même rigueur que le texte visible :
- Libellés de badges de statut : `doublon`, `non fonctionnel`, `à vérifier`. *(Depuis l'audit de code : ces trois libellés sont désormais regroupés dans une seule constante `FLAG_LABELS` en début de section de rendu des icônes, au lieu d'un enchaînement de conditions dispersé dans le code — plus facile à repérer d'un coup d'œil.)*
- En-têtes de tableau générés en JS : `Aperçu`, `Balise`, `Chemin texture`.
- Option par défaut du filtre catégorie : `Toutes catégories`.
- Message d'absence de résultat : `Aucun résultat.`
- Compteurs dynamiques : le suffixe `' balises'` (dans `rows.length + ' / ' + COLORS.length + ' balises'` et son équivalent pour les icônes).
- Pastille de transparence : `transparence ${...}%`.
- Gabarit de texte copié pour les couleurs : `Texte` dans `` `<${tag}>Texte</>` `` (c'est un exemple de texte que l'utilisateur va coller puis remplacer en jeu — traduire ce mot-témoin, ex. `Text` en anglais). **Ce mot a un jumeau statique dans le HTML visible** : `<span class="syn-text">Text</span>`, affiché dans le bandeau d'aide du simulateur (hero) — les deux représentent exactement la même idée (le texte libre que l'utilisateur tapera) et **doivent impérativement utiliser le mot traduit identique**. Vérifier cette correspondance explicitement avant de livrer, comme pour les noms de catégories.
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
4. **La clé de l'objet `CATEGORY_DESCRIPTIONS`** — actuellement `"Classe (C→S)"`. Cette clé DOIT être remplacée par la traduction exacte utilisée pour cette catégorie dans le tableau `ICONS`, au caractère près (mêmes espaces, mêmes parenthèses, même flèche `→`). Si la clé ne correspond plus exactement à la valeur de catégorie utilisée dans les lignes `ICONS`, la description associée disparaît silencieusement du rendu — sans erreur, sans avertissement. **Vérifier ce point explicitement avant de livrer, avec une méthode programmatique plutôt qu'une simple relecture visuelle** : extraire par script (ex. regex Python) l'ensemble des valeurs de catégorie distinctes réellement utilisées dans `ICONS`, et confirmer que la clé de `CATEGORY_DESCRIPTIONS` y figure exactement. Une relecture à l'œil est insuffisante pour détecter un espace ou un caractère de flèche mal recopié.

### D. Commentaires de code (HTML / JavaScript / CSS)
Traduire l'intégralité des commentaires, sous toutes leurs formes, pour livrer un fichier source cohérent, entièrement en langue cible :
- Commentaires JS/CSS (`//` et `/* */`) — y compris les commentaires de section (`/* ==== DATA ==== */` reste tel quel s'il est déjà en anglais générique, mais les commentaires en français comme `// Ordre de référence défini manuellement...` doivent être traduits).
- **Commentaires HTML (`<!-- ... -->`)** — présents notamment comme marqueurs de section dans le `<body>` (ex. `<!-- ============ INFOS TAB ============ -->`). Ces marqueurs doivent rester cohérents avec le libellé d'onglet traduit correspondant : si l'onglet visible devient `Info` (singulier) en anglais, le commentaire doit devenir `<!-- ============ INFO TAB ============ -->` et non rester sur l'ancien libellé `INFOS TAB`. **Cette règle s'applique aux 4 marqueurs de section** (`INFOS TAB`, `COLORS TAB`, `ICONS TAB`, `NOTES/ABOUT TAB` ou équivalent selon la source) — vérifier les 4, pas seulement le premier rencontré.

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
Le README et ce guide HTML décrivent le même produit et doivent employer un vocabulaire strictement identique. Cette règle est **bidirectionnelle et sans ordre imposé** : ni le HTML ni le README n'est par défaut « traduit en premier » — cela dépend simplement de ce que la personne demande dans chaque session (voir le tableau des rôles des trois fichiers en tête de ce prompt). Ce qui compte n'est pas l'ordre, mais que les deux documents, une fois tous deux traduits dans une langue donnée, utilisent exactement les mêmes choix pour les mêmes notions.

- **Si `companion_readme` (défini dans `TARGET`) a été explicitement fourni ou désigné par la personne pour cette session** : appliquer d'abord la **règle de fraîcheur des fichiers fournis** (voir plus haut) — ne jamais l'utiliser comme référence sans avoir vérifié qu'il est à jour par rapport au README de contexte en langue source fourni dans ce tour. S'il est confirmé à jour, le relire et réutiliser exactement les mêmes choix de traduction pour les termes récurrents du projet (ex. si « balise » a été traduit par « tag » dans le README, utiliser « tag » partout ici aussi ; idem pour « teinte/teinter » → « tint/tinting », « doublon » → « duplicate », etc.). S'il est obsolète, suivre la procédure décrite dans la règle de fraîcheur (signaler, décrire l'écart, demander comment procéder) plutôt que de l'utiliser tel quel ou de l'ignorer silencieusement.
- **Dans tout autre cas** (aucun `companion_readme` fourni pour cette session, y compris si un README dans la langue cible existe quelque part dans l'historique de la conversation sans avoir été désigné comme référence) : ne pas aller le chercher, ne pas le mentionner. Les choix de terminologie faits ici (noms de catégories, libellés de badges, termes récurrents) font alors référence pour la suite — le prompt `prompt_translation_README_LANG.md` s'appuiera dessus via son propre champ `companion_html_guide` lors d'une traduction ultérieure du README, dans une session séparée. Traduire avec la même rigueur terminologique que si le README à jour existait déjà, puisque ce fichier HTML deviendra lui-même la référence.

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

## VÉRIFICATIONS TECHNIQUES RECOMMANDÉES (avant la relecture finale)

Cohérent avec le principe déjà établi pour ce projet (outils nommés et vérifiables plutôt qu'inspection ad hoc — voir `prompt_fix_allcode.md` §L.45bis) : privilégier une vérification programmatique aux points de rupture silencieuse identifiés ci-dessus, plutôt qu'une simple relecture visuelle.

- **Validité syntaxique du JavaScript** : extraire le contenu de la balise `<script>` dans un fichier `.js` temporaire et le valider avec `node --check`. Une erreur de syntaxe introduite par une chaîne mal échappée (apostrophe, guillemet) sera détectée immédiatement, alors qu'elle peut passer inaperçue à la lecture.
- **Comparaison champ par champ des tableaux `COLORS` et `ICONS`** : extraire par script (regex) chaque ligne des deux tableaux, source et traduction, et vérifier que tous les champs non-traduisibles (tag, hex, alpha pour `COLORS` ; tag, fichier, chemin, flag pour `ICONS`) restent strictement identiques d'une version à l'autre, et que seul le champ catégorie diffère. Une divergence sur un champ censé être intouchable est le signe d'une erreur de traduction, même isolée.
- **Vérification de la clé `CATEGORY_DESCRIPTIONS`** : voir méthode décrite au §C point 4 ci-dessus.
- **Comparaison structurelle globale** : comptage des balises HTML structurelles (`<section`, `<div`, `<table`, `<h1/h2/h3`, etc.) entre source et traduction — un écart signale une structure cassée ou une section ajoutée/supprimée par erreur.
- **Vérification des ID référencés en JS** : confirmer que chaque `getElementById('...')` du script traduit correspond bien à un `id="..."` toujours présent dans le HTML traduit.

Ces vérifications ne remplacent pas la relecture humaine finale ci-dessous, elles la précèdent et la sécurisent.

---

## VÉRIFICATION FINALE (auto-relecture obligatoire avant livraison)

- [ ] `<html lang="...">` correspond bien à `html_lang_attribute` défini dans `TARGET`.
- [ ] `<title>` traduit.
- [ ] Les 4 onglets, tous les encadrés, le footer et le simulateur sont intégralement traduits — aucune phrase française oubliée.
- [ ] Toutes les chaînes JS listées en §B (badges, en-têtes de tableau, compteurs, tooltips, placeholder de copie, "Toutes catégories", "Aucun résultat.") sont traduites.
- [ ] Les 3 `aria-label` (recherche couleurs, recherche icônes, filtre catégorie) sont traduits et cohérents avec le placeholder correspondant sur le même champ.
- [ ] `NAME_COLOR` et `NAME_ICON` (pseudo-noms pédagogiques, pas de vraies balises) sont traduits dans la langue cible, sur **toutes** leurs occurrences (bandeau d'aide du simulateur ET onglet Infos) — voir §A bis.
- [ ] Le mot-témoin `Texte`/`Text` (gabarit de copie en JS) et son jumeau statique `<span class="syn-text">` dans le HTML utilisent **le même mot traduit**.
- [ ] Chaque nom de catégorie a été traduit **à l'identique partout** où il apparaît (tableaux `COLORS`/`ICONS`, commentaires de section, et surtout la clé de `CATEGORY_DESCRIPTIONS`) — vérifier caractère par caractère, en particulier les espaces autour de `/` et la flèche `→`, avec une méthode programmatique (voir §C point 4 et section « VÉRIFICATIONS TECHNIQUES RECOMMANDÉES »).
- [ ] Aucun nom de balise NMS, chemin `.DDS`, code hex, nom de fichier PNG, ID HTML, classe CSS, nom de variable/fonction JS n'a été traduit ou modifié.
- [ ] Les 10 entrées de `CONTAINER_EXAMPLES` sont restées strictement identiques à la source.
- [ ] Tous les commentaires de code sont traduits, HTML compris (§D) — vérifier en particulier que les 4 marqueurs `<!-- ... TAB ... -->` (Infos/Couleurs/Icônes/À propos) correspondent chacun au libellé d'onglet traduit.
- [ ] Si `companion_readme` a été explicitement fourni/désigné pour cette session : la terminologie utilisée y correspond, **confirmé à jour** (fraîcheur vérifiée par comparaison avec le README de contexte en langue source). Sinon (cas le plus fréquent : aucun `companion_readme` fourni) : la terminologie choisie ici est cohérente en interne et prête à servir de référence pour une traduction ultérieure du README, sans qu'il y ait eu lieu de rechercher ou mentionner un README cible existant ailleurs dans la conversation.
- [ ] Aucune balise HTML, accolade JS ou guillemet n'a été cassé par une chaîne traduite mal échappée — relire spécifiquement les lignes où une traduction contient une apostrophe.
- [ ] Le fichier reste un unique `.html` autonome, structurellement identique à la source (aucune section ajoutée/supprimée/déplacée).

---

## LIVRABLE ATTENDU

Un unique fichier `.html` nommé selon `output_filename`, fonctionnellement identique au fichier source (même simulateur, mêmes tris, mêmes filtres, mêmes tableaux, mêmes 145 icônes intégrées), avec l'intégralité du texte visible et des chaînes de code traduites en langue cible, prêt à être ouvert directement dans un navigateur sans aucune retouche supplémentaire.

---

## HISTORIQUE D'UTILISATION

Table à compléter à chaque usage de ce prompt, pour tracer quelle version de quel fichier a été traduite, avec quels réglages — évite toute ambiguïté en cas de reprise de ce prompt dans une conversation ultérieure ou par une autre personne.

| Date | Fichier source (nom + repère de version) | Fichier produit | `target_language` | `target_variant` | `tone` | `fidelity_style` | `companion_readme` utilisé ? |
|---|---|---|---|---|---|---|---|
| 2026-09-08 | `NMS_txt_code_FR.html` (1298 lignes indiquées à l'époque — **à vérifier** : la version fournie le 2026-09-09 fait 1297 lignes ; l'écart n'a pas été élucidé, possible imprécision de saisie lors de cette entrée) | `NMS_txt_code_EN.html` | English | neutral/standard | passionate/stylized | idiomatic | Non fourni pour cette session |
| 2026-09-09 | `NMS_txt_code_FR.html` (1297 lignes, hash `fb4b9e77452586130fcf7bc6fdf81e14`) | `NMS_txt_code_ES.html` | Español | neutral/standard | passionate/stylized | idiomatic | Non fourni pour cette session |
