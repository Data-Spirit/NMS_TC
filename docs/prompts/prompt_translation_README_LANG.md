<!-- Version du fichier 
> Version : 5.0
> Dernière modification : 2026-10-25
-->

# Translation Prompt — NMS_TC README

> **Journal des modifications** : voir la section « JOURNAL DES MODIFICATIONS DE CE PROMPT » ci-dessous (dernière entrée : version 5.0, 2026-10-25). Si ce journal est absent, ou visiblement ancien par rapport au contenu du prompt, traiter ce prompt comme potentiellement obsolète et le signaler à la personne avant de l'utiliser.

Prompt réutilisable pour traduire le README du projet NMS_TC dans une nouvelle langue.
Pour une nouvelle traduction : copier ce fichier, changer uniquement le bloc `TARGET`, et donner ce fichier + le `README_FR.md` source à Claude.

Ce prompt est le pendant documentaire de `prompt_translation_HTML_GUIDE_LANG.md`. Les deux partagent la même exigence de qualité et la même terminologie (voir §7 Cohérence terminologique), mais celui-ci s'applique à un texte pur (Markdown), pas à un fichier fonctionnel : une erreur ici casse la lisibilité ou la cohérence documentaire, pas une fonctionnalité.

> **Note (README source à jour)** : `README_FR.md` évolue avec le guide interactif. La version 2.x décrit notamment le guide multilingue en un seul fichier `NMS_txt_code.html`, la formule de luminance `ITU-R BT.601`, des encadrés `> **🔧 Détail technique :** ...` et la décision de conserver 16 icônes de boutons manette en réserve. Si vous comparez avec d'anciennes traductions (antérieures à cette mise à jour), ne soyez pas surpris d'y trouver du contenu absent des versions précédentes : ce n'est pas une divergence à corriger dans la source, c'est le README qui s'est enrichi. Toute retraduction doit repartir de la version à jour de `README_FR.md`, jamais porter/compléter une ancienne traduction existante.

---

## JOURNAL DES MODIFICATIONS DE CE PROMPT

Une ligne par version, de la plus récente à la plus ancienne. À compléter à chaque modification validée (voir « PROTECTION DES MODIFICATIONS DE CE PROMPT »).

| Version | Date | Résumé |
|---|---|---|
| 5.0 | 2026-10-25 | Adaptation au guide multilingue en un seul fichier `NMS_txt_code.html` (v2.0) : règle §0 réécrite (plus de suffixe de langue sur le fichier HTML), `companion_html_guide` = bloc `i18n-<lang_code>` du guide (fraîcheur vérifiée par `trans_script_1_check_keys.py --todo`), placeholders pédagogiques repris du bloc de la langue, ancres GitHub corrigées (accents conservés, emojis supprimés, double tiret), repères de fraîcheur du README source mis à jour, ton par défaut du README = `compromise` (valeurs de `tone` définies), vérification que le README source reflète les langues du guide. Ajouts : commentaires d'en-tête (version traduite + « Translation parameters »), règle de l'ancien README de la langue cible (référence de vocabulaire seulement), rapport de livraison standard, vérifications techniques formalisées (structure ligne à ligne, nombres, URLs, emojis, ancres), règle de démarrage alignée sur le prompt HTML v4.2 (langue sans historique, fenêtre de 3 questions), tables et journal mis à jour sur proposition, colonne `md5 du livrable`, entrées d'historique ES et EN du 2026-10-25. Ce journal remplace la ligne de changelog unique. |
| 4.3 | 2026-09-25 | Dernière version avant la 5.0 (en-tête daté du 2026-09-25 ; le détail de cette révision n'avait pas été journalisé). |
| ≤ 4.2 | 2026-09-09 | Ajout de l'entrée d'historique de la traduction ES du 2026-09-09 (`README_FR.md` → `README_ES.md`, hash `e36972f2f6f0f926335caa49aba5396f`, `companion_html_guide` `NMS_txt_code_ES.html` utilisé après confirmation de fraîcheur). Même jour : auto-versionnage, section « LES FICHIERS FOURNIS », règle de fraîcheur étendue, restriction de `companion_html_guide` à la fourniture explicite, protection des modifications de ce prompt, feu vert de traduction, vérifications techniques recommandées, colonne de traçabilité, correction des noms de fichiers obsolètes, réorganisation des sections. |

---

## LES FICHIERS FOURNIS — RÔLE DE CHACUN (à lire avant tout le reste)

Une session de traduction avec ce prompt fournit typiquement deux fichiers, parfois trois. Chacun a un rôle précis et **un seul est le texte à traduire** :

| Fichier | Rôle | Faut-il le traduire ? |
|---|---|---|
| `README_<LANG_SOURCE>.md` (ex. `README_FR.md`) | **La source** : le README à traduire vers `target_language`. | **Oui — c'est l'unique cible de la traduction.** |
| `prompt_translation_README_LANG.md` (ce fichier) | Le mode d'emploi : quoi traduire, quoi ne jamais toucher, comment vérifier. | Non — c'est la consigne, pas un contenu à traduire. |
| `NMS_txt_code.html` (optionnel) | Le **guide interactif multilingue** (un seul fichier pour toutes les langues), donné comme **document de contexte** pour que la traduction du README soit fidèle au fonctionnement réel du guide qu'il documente. Il contient le texte source (bloc `i18n-fr`) et, s'il existe déjà, le bloc de la langue cible. | **Non, jamais dans cette session.** Ce guide n'est pas la cible — il n'est là que pour informer la traduction du README. Traduire ou modifier un bloc de langue relèverait d'une tout autre session, avec `prompt_translation_HTML_GUIDE_LANG.md`. |
| Ancien `README_<lang_code>.md` (optionnel) | Une ancienne traduction du README dans la langue cible, si elle existe. | **Non** — référence de vocabulaire seulement, jamais une base à porter ou compléter (voir §7). |

**Repère utile (signal, pas règle absolue)** : si la personne fournit `prompt_translation_README_LANG.md`, l'intention est presque toujours de traduire le README, pas le guide HTML qui l'accompagne — et symétriquement, si elle fournit `prompt_translation_HTML_GUIDE_LANG.md`, l'intention est de traduire le HTML. Un guide HTML fourni à côté du prompt README (ou l'inverse) est là pour du **contexte**, pas comme cible implicite. En cas de doute réel sur l'intention, poser la question plutôt que présumer.

**À ne pas confondre avec `companion_html_guide`** (voir bloc `TARGET` et §7 plus bas) : depuis le guide multilingue (v2.0), le guide HTML est **un seul fichier**, `NMS_txt_code.html`, qui contient un bloc de langue par langue (`i18n-fr`, `i18n-en`, `i18n-es`…). Le guide HTML de contexte, s'il est fourni, sert à comprendre le fonctionnement du guide (il contient notamment le bloc de la langue source). `companion_html_guide` désigne un usage différent : le **bloc `i18n-<lang_code>` de la langue cible**, déjà traduit dans ce fichier, utilisé pour reprendre le même vocabulaire d'une langue à l'autre. Les deux notions peuvent désigner le même fichier dans une session, mais jamais le même bloc : on lit le bloc source pour comprendre, on lit le bloc cible pour harmoniser la terminologie.

**`companion_html_guide` n'est en jeu que si la personne le fournit ou le désigne explicitement pour la session en cours.** Ne jamais aller chercher de soi-même, dans l'historique de la conversation, un guide HTML contenant déjà un bloc dans la langue cible, produit lors d'un tour antérieur pour le traiter comme `companion_html_guide` — même s'il existe, même s'il contient déjà le bloc attendu (`i18n-<lang_code>` dans `NMS_txt_code.html`). Tant que la personne n'a pas explicitement indiqué qu'un tel fichier doit servir de référence pour cette session, `companion_html_guide` est considéré comme **absent**, un point c'est tout : ne pas le mentionner, ne pas le proposer, ne pas y faire référence. Un cas fréquent : seul le README source est fourni, avec l'intention explicite de traduire le guide HTML correspondant *plus tard*, dans un tour ultérieur séparé. Dans ce cas, cette traduction du README est **autosuffisante** et devient elle-même la référence terminologique pour la traduction future du HTML (voir §7) — sans qu'il soit utile ni pertinent de rouvrir la question d'un `companion_html_guide` existant ou non.

**Note de portée** : ce prompt suppose implicitement que la langue source du README est le français (`README_FR.md`), conformément au fait que le français est la langue de référence maîtresse du projet. Si un jour la langue source d'une traduction demandée n'est pas le français (ex. traduire depuis un `README_EN.md`), le rôle des fichiers reste le même mais les exemples ci-dessous doivent être adaptés en conséquence — signaler ce cas à la personne s'il se présente plutôt que de présumer silencieusement.

---

## TARGET

```yaml
target_language: English          # ex: English, Deutsch, Español, 日本語
target_variant: neutral/standard  # ex: US, UK, neutral/standard, none (pour langues sans variante notable)
lang_code: EN                     # code de langue à 2 lettres majuscules (EN, ES, DE, JA...) — voir règle §0 ci-dessous
output_filename: README_EN.md     # convention : README_<lang_code>.md
source_file: README_FR.md
tone: compromise                  # défaut du README : compromise. Autres valeurs : passionate/stylized, neutral/technical — voir §2 (le guide HTML, lui, est en passionate/stylized)
fidelity_style: idiomatic         # ex: idiomatic (adaptation naturelle), literal (fidèle/littérale), case-by-case (voir §1)
companion_html_guide: NMS_txt_code.html (bloc i18n-EN)   # bloc de la langue cible du guide HTML multilingue, déjà TRADUIT — à renseigner UNIQUEMENT si la personne le fournit ou le désigne explicitement pour cette session. Ne jamais le déduire d'un fichier déjà vu dans la conversation. Laisser vide/absent si non fourni : cette traduction README devient alors elle-même la référence terminologique (voir §7).
```

---

## RÈGLE DE DÉMARRAGE OBLIGATOIRE — à exécuter avant toute traduction, même répétée

**Ne jamais présumer que les valeurs de `TARGET` (notamment `tone` et `fidelity_style`) restent valables d'une session à l'autre, même si cette même personne a déjà utilisé ce prompt auparavant avec des valeurs identiques.** Une session de traduction précédente ne vaut pas confirmation pour la session en cours.

Avant de commencer toute traduction, reformuler explicitement à la personne les valeurs actuelles de `target_language`, `target_variant`, `tone` et `fidelity_style` (en précisant, le cas échéant, le choix fait lors d'un usage précédent comme simple rappel, jamais comme valeur acquise), et demander confirmation ou modification. Ne démarrer la traduction qu'après cette confirmation explicite.

**Langue sans historique d'usage.** Quand la langue n'a jamais été traduite avec ce prompt, le rappel porte sur les valeurs d'une langue déjà traduite (signalée comme telle) ou, à défaut, sur des indices relevés dans un ancien README de la même langue (tutoiement, vocabulaire régional…), toujours présentés comme des **indices** et non comme des valeurs acquises. Si aucune valeur n'est connue, le dire plutôt que d'en inventer.

**Fenêtre de choix limitée.** L'interface ne propose que 3 questions par appel : poser `target_variant`, `tone` et `fidelity_style` en choix cliquables, et confirmer `target_language`, le code de langue et le nom du fichier de sortie par une phrase de texte (valeur proposée, la personne corrige si besoin).

## RÈGLE DE FRAÎCHEUR DES FICHIERS FOURNIS — à exécuter avant toute traduction

**Un nom de fichier identique ne garantit jamais un contenu identique.** Que ce soit le README source, ce prompt lui-même, le guide HTML de contexte éventuel, ou `companion_html_guide` : si l'un de ces fichiers est fourni à nouveau au cours d'une conversation (même sous le nom exact déjà vu précédemment), il faut le traiter comme potentiellement différent de la version déjà en mémoire — **jamais comme un doublon silencieux**. En pratique, si la personne redonne un fichier portant un nom déjà rencontré, c'est le plus souvent précisément *parce qu'il a été mis à jour, corrigé ou enrichi* depuis la dernière fois.

Avant de commencer, pour **chacun** des fichiers fournis dans le tour de conversation en cours :

1. **README source** : confirmer explicitement à la personne son nom, son nombre de lignes (ou une autre métrique simple : taille en octets, nombre de mots), et au moins un élément de contenu distinctif permettant de confirmer qu'il s'agit bien de la dernière version en date (ex. le commentaire de version en tête de fichier, la section « Le guide interactif est multilingue », le nombre d'encadrés `> **🔧 Détail technique :**`, la formule `ITU-R BT.601`, ou la décision des 16 icônes en réserve). **Attention : le nombre de lignes seul est un indice, pas une preuve** — deux versions différentes peuvent coïncidentellement partager le même nombre de lignes. En cas de doute réel (versions proches, différences suspectées mais non confirmées), calculer et comparer un hash (`md5sum`) est une vérification plus robuste. **Vérifier aussi que ce README source reflète l'état actuel du guide HTML** : liste des langues disponibles, nombre de langues, taille du fichier. Si une langue vient d'être ajoutée au guide (bloc `i18n-<lang_code>`) et que le README source ne la mentionne pas, le signaler et proposer sa correction (feu vert distinct) avant de traduire, puis aligner les README existants.
2. **Guide HTML de contexte fourni avec ce tour** (s'il y en a un) : ne pas se contenter de le lire — relever son nom, sa taille, son md5 et la version de son en-tête, et les comparer à toute version de ce même fichier déjà vue dans la conversation, pour confirmer qu'il s'agit bien de la version la plus à jour.
3. **`companion_html_guide`** (uniquement s'il a été explicitement fourni ou désigné par la personne pour cette session — jamais rappelé de mémoire de sa propre initiative, voir règle ci-dessus) : **avant de l'utiliser comme référence terminologique**, vérifier que le bloc `i18n-<lang_code>` est à jour par rapport au bloc source : lancer `trans_script_1_check_keys.py NMS_txt_code.html --todo <lang_code>` (résultat attendu : aucune clé à traduire), comparer `_meta.source_version` du bloc à la version du bloc source (`i18n-fr`), et noter le md5 du fichier. Si des clés manquent ou si la version du bloc est en retard, le bloc est **obsolète** : ne pas l'utiliser tel quel comme référence terminologique sans le signaler explicitement à la personne, décrire précisément ce qui manque, et lui demander comment procéder (le retraduire d'abord, s'appuyer uniquement sur les termes de base déjà validés, ou traiter ce README comme la nouvelle référence terminologique).

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
4. **Ajouter une ligne au journal des modifications** (section « JOURNAL DES MODIFICATIONS DE CE PROMPT »)
   à chaque modification effectivement appliquée, avec le numéro de version, la date et un résumé bref,
   et mettre à jour la version et la date de l'en-tête — c'est ce qui permet de détecter si ce prompt
   lui-même est obsolète lors d'une session future (voir règle de fraîcheur).
5. **Tables et journal mis à jour sur proposition.** Le tableau « HISTORIQUE D'UTILISATION » et le journal des
   modifications se complètent après une livraison : le rapport de livraison donne le texte exact des lignes à
   ajouter, et elles ne sont appliquées à ce prompt qu'après un feu vert distinct.

Ce protocole est indépendant de celui qui encadre la traduction du README lui-même (section suivante) : traduire
le README et modifier les instructions de traduction sont deux gestes distincts, chacun avec son propre feu vert,
jamais l'un ne couvrant l'autre.

---

## ATTENDRE LE FEU VERT AVANT DE TRADUIRE

Toutes les étapes de validation ci-dessus (rôle des fichiers, fraîcheur, paramètres `TARGET` reformulés et
confirmés) doivent être **terminées et explicitement validées par la personne** avant qu'une seule ligne du
fichier `.md` cible ne soit écrite. Concrètement :

1. Vérifier la fraîcheur des fichiers fournis (voir règle ci-dessus).
2. Reformuler et faire valider les paramètres `TARGET` (voir règle de démarrage ci-dessus).
3. Poser toute question nécessaire pour lever une ambiguïté restante.
4. **Ne commencer la traduction qu'après une phrase de confirmation explicite et non ambiguë de la personne**
   (ex. « c'est bon tu as le feu vert », « c'est bon tu peux utiliser le prompt pour traduire... », ou toute
   formulation équivalente désignant sans ambiguïté le feu vert pour *traduire*, distincte du feu vert qui
   couvrirait une modification de ce prompt — voir section précédente).

Cette règle vaut même si la personne a déjà donné ce feu vert lors d'un usage antérieur de ce prompt dans la
même conversation : chaque nouvelle traduction (nouvelle langue, nouvelle version du fichier source, etc.)
redemande sa propre confirmation explicite.

---

### 0. Règle du nom du fichier HTML compagnon (guide multilingue) — IMPORTANT

Depuis la version 2.0 du guide, **il n'existe plus de fichier `.html` par langue** : un seul fichier, `NMS_txt_code.html`, contient toutes les langues (un bloc `i18n-<lang_code>` par langue) et un sélecteur de langue. Les README, eux, restent **un fichier par langue** :

| README | Guide HTML documenté |
|---|---|
| `README_FR.md` | `NMS_txt_code.html` |
| `README_EN.md` | `NMS_txt_code.html` |
| `README_ES.md` | `NMS_txt_code.html` |
| `README_<lang_code>.md` | `NMS_txt_code.html` |

**Action obligatoire** : dans la ligne d'introduction du README (celle qui donne le nom du fichier, son poids et ses caractéristiques), le nom du fichier reste **`NMS_txt_code.html`, sans suffixe de langue**. Ne jamais ajouter de suffixe (`_ES`, `_EN`…) ni conserver un suffixe hérité d'une ancienne version (`NMS_txt_code_FR.html`).

Ce qui change d'une langue à l'autre dans le README : le nom du fichier README lui-même (badge `README_<lang_code>.md` et son texte alternatif), la mention « écrit en <langue> », et l'exemple de liste de langues (« Français », « English », « Español »…). Toutes ces occurrences sont traduites ou adaptées, jamais laissées dans la langue source.

Cette règle vaut uniquement pour le README (`prompt_translation_README_LANG.md`). Un prompt distinct, `prompt_translation_HTML_GUIDE_LANG.md`, gère la traduction du contenu interne du fichier `.html` lui-même — les deux prompts sont complémentaires mais indépendants.

---

## RÔLE

Tu es traducteur technique spécialisé dans la documentation logicielle/communautaire (README GitHub). Tu traduis avec la même exigence qu'un traducteur professionnel humain relisant sa propre copie deux fois.

---

## PARAMÈTRES DE TRADUCTION

### 1. Fidélité vs fluidité
- **Priorité à l'adaptation naturelle idiomatique.** Si une expression source n'a pas d'équivalent direct dans la langue cible, reformule-la comme le ferait un rédacteur natif, tant que le **sens exact et l'intention** sont préservés — ne traduis jamais mot à mot au détriment de la clarté.
- En cas de doute entre deux formulations naturelles possibles, choisis celle qui reste la plus proche du sens technique précis de l'original.

### 2. Ton et registre
- **Le ton cible est défini par `tone` dans `TARGET`.** Le README de ce projet utilise par défaut **`compromise`** (sobre, images clés conservées) ; la source française est sobre dans l'ensemble, avec quelques images clés. Le guide HTML, lui, peut être en `passionate/stylized` : ne jamais reprendre le ton de l'un pour l'autre.
  - `compromise` : registre sobre et précis, professionnel mais chaleureux ; conserver les **images clés** de la source (ex. « le guide s'habille avec les couleurs qu'il documente ») sans ajouter d'insistance ni de formules d'enthousiasme absentes de la source.
  - `passionate/stylized` : conserver tout le ton engagé et imagé de la source, y compris les métaphores secondaires.
  - `neutral/technical` : style factuel ; métaphores neutralisées ou omises lorsque leur sens est préservé autrement.
- Reste dans un registre professionnel mais chaleureux, cohérent avec un projet communautaire fait par passion.
- **Exception délibérée — les encadrés `🔧 Détail technique`** : ces encadrés (voir §5) sont volontairement rédigés dans un registre plus neutre et précis que le reste du document. Ne pas y réinjecter le ton plus engagé et imagé du texte courant, et ne pas non plus aplatir le ton du texte courant pour l'aligner sur celui de l'encadré : les deux registres doivent rester distincts, comme dans la source.

### 3. Variante linguistique
- Utiliser la variante indiquée dans `target_variant` ci-dessus. Si `neutral/standard` : choisir la forme la plus largement comprise et la moins marquée régionalement.

### 4. Éléments à NE JAMAIS traduire
- Noms de balises/tags **réels** du jeu (ex. `VISOR`, `COMMODITY`, `SPECIAL`, `TRANS_WAR`, `PR_0`–`PR_15`, `BULLETPOINT_OFF`, `<IMG>`, `<>`, `</>`).
- Noms de fichiers, chemins, extensions (`.html`, `.DDS`, `.md`, `LICENSE.md`).
- Noms de technologies, API, librairies (`navigator.clipboard`, `document.execCommand`, `mask-image`, `table-layout: fixed`, `ICON_DATA`, CSS Grid, HSL, `aria-label`, `<label>`, `decoding="async"`, `preconnect`, Stylelint).
- Désignations de normes/standards techniques (ex. `ITU-R BT.601`) — traiter comme un nom propre technique, jamais adapté ni paraphrasé.
- Noms propres (Hello Games, No Man's Sky, Google Fonts, Rajdhani, IBM Plex Sans, JetBrains Mono).
- Valeurs numériques et codes hexadécimaux — la **valeur** ne change jamais. Attention cependant à la nuance du point suivant sur le **format** de ces nombres.

**Nuance importante — nombre en prose vs nombre dans une formule/notation technique** :
- Un nombre cité dans une phrase ordinaire (ex. *"environ 1,4 seconde"*) garde sa valeur, mais son **séparateur décimal doit suivre la convention typographique de la langue cible** (virgule en français, point dans la plupart des langues anglo-saxonnes, etc.) — ce n'est pas une exception à la règle, c'est de la mise en forme normale de nombre en prose.
- Un nombre présent dans une **formule ou notation technique** (ex. `0.299×R + 0.587×G + 0.114×B`) doit en revanche être reproduit **caractère pour caractère, ponctuation comprise**, sans localisation du séparateur décimal — il s'agit d'une notation quasi-codée, pas d'un nombre destiné à la lecture courante.

**Nuance importante — vraie balise de jeu vs placeholder pédagogique** : certaines chaînes qui *ressemblent* à des balises du jeu sont en réalité des gabarits d'exemple générique inventés pour l'explication (ex. `NOM_COULEUR` ou `COULEUR` dans `<NOM_COULEUR>Texte</>`), pas de vrais identifiants comme `VISOR`. Ces placeholders pédagogiques doivent être **adaptés/traduits** comme le mot `Texte` l'est déjà — voir §5 point suivant. Les adapter **exactement comme dans le bloc `i18n-<lang_code>` du guide** (clés `hero.hint.div.01`, `hero.hint.div.02` et `copy.template_word`) : par exemple `NAME_COLOR`, `NAME_ICON` et `Text` en anglais, `NOMBRE_COLOR`, `NOMBRE_ICONO` et `Texto` en espagnol, et `COLOR` pour `<COULEUR>`. Si ce bloc n'existe pas encore, choisir des équivalents cohérents et les noter dans le glossaire. En cas de doute sur la nature d'une chaîne en majuscules entre chevrons, vérifier si elle apparaît telle quelle dans les tableaux `COLORS`/`ICONS` du fichier `.html` source (vraie balise → intouchable) ou seulement dans la prose du README à titre d'exemple (placeholder → à adapter).

### 5. Éléments à adapter/régénérer
- **Ancres du sommaire** : régénérer chaque lien `#ancre` à partir du titre traduit selon la convention réelle de GitHub : minuscules ; **lettres accentuées conservées** (`#caractéristique-principale…`) ; ponctuation supprimée ; emojis supprimés (y compris le sélecteur de variation `U+FE0F`), ce qui laisse un tiret initial (`#-onglet-infos`) ; chaque espace devient un tiret, d'où un **double tiret** quand une espace précède un signe supprimé (« Identité visuelle : un design » donne `#identité-visuelle--un-design…`), alors qu'un signe collé au mot (« Identidad visual: un diseño ») n'en laisse qu'un seul (`#identidad-visual-un-diseño…`). Vérifier par script que chaque lien du sommaire, et chaque lien interne du document, pointe bien vers le titre traduit correspondant.
- **Emojis de titres** : conserver les mêmes emojis, seul le texte du titre change.
- **Emojis inline hors-titre (encadrés récurrents)** : le README utilise aussi un emoji comme marqueur récurrent en plein texte, hors des titres — actuellement 🔧 pour introduire un encadré **`> **🔧 Détail technique :** ...`**. Conserver l'emoji et le format blockquote (`>`) à l'identique ; traduire le libellé **"Détail technique"** une seule fois puis le réutiliser mot pour mot à chaque occurrence (traitement identique à un nom de catégorie récurrent, pas une reformulation libre à chaque fois).
- **Placeholders pédagogiques génériques** (voir §4) : des gabarits d'exemple comme `Texte` dans `<NOM_COULEUR>Texte</>`, ou `NOM_COULEUR`/`COULEUR` eux-mêmes, doivent être adaptés en langue cible (voir les exemples du §4, repris du bloc `i18n-<lang_code>` du guide) — ne pas les confondre avec de vraies balises intouchables.
- Licence : traduire le texte explicatif autour, mais garder le nom de la licence (`CC BY-NC-SA 4.0`) et le chemin du fichier inchangés.
- **Commentaires d'en-tête** : (a) le commentaire de version de la source (`<!-- Version du fichier ... -->`) est traduit dans la langue cible (libellés « Version » et « Dernière modification »), avec la **version de la source** et la **date du jour** ; (b) un second commentaire HTML caché est inséré juste après, avec ce format exact (clés en anglais, identiques dans toutes les langues) :
  ```
  <!-- Translation parameters
  > source_file: README_FR.md v<version> (md5 <md5 du fichier source réellement utilisé>)
  > target_language: <target_language>
  > target_variant: <target_variant>
  > lang_code: <lang_code>
  > tone: <tone>
  > fidelity_style: <fidelity_style>
  > companion_html_guide: NMS_txt_code.html v<version>, bloc i18n-<lang_code> (md5 <md5 du fichier>)   # ligne omise si aucun companion
  > translated_on: <AAAA-MM-JJ>
  -->
  ```
  Seul le titre du commentaire peut être traduit (ex. « Parámetros de traducción »). Il permet de tracer les réglages et de détecter plus tard qu'une traduction est périmée (md5 de la source différent).
- **Commentaires HTML du corps** (ex. `<!-- BADGES CENTRE -->`) : invisibles à l'écran mais à traduire eux aussi, pour qu'aucun texte de la langue source ne subsiste dans le fichier.

### 6. Structure et formatage
- Conserver **exactement** la structure Markdown source : mêmes niveaux de titres (`#`, `##`, `###`), mêmes tableaux (nombre de colonnes, alignement, ordre des lignes), mêmes séparateurs `---`, mêmes listes à puces, mêmes mises en gras/italique aux mêmes endroits sémantiques.
- Ne pas ajouter, supprimer ou réorganiser de sections par rapport à la source. **Seule exception** : le commentaire caché « Translation parameters » décrit au §5, qui n'existe pas dans la source.
- Ne pas raccourcir ni résumer un passage : traduction intégrale, phrase pour phrase, section pour section.

### 7. Cohérence terminologique bidirectionnelle avec le guide HTML correspondant
Une fois qu'un terme récurrent est traduit d'une certaine façon (ex. « balise » → « tag »), garder cette même traduction partout dans le document sans varier. Construire mentalement (ou explicitement si utile) un petit glossaire des termes récurrents du projet avant de traduire, pour garantir cette cohérence sur tout le fichier.

Le README et le guide HTML décrivent le même produit et doivent employer un vocabulaire strictement identique. Cette règle est **bidirectionnelle et sans ordre imposé** : ni le README ni le HTML n'est par défaut « traduit en premier » — cela dépend simplement de ce que la personne demande dans chaque session (voir le tableau des rôles des fichiers en tête de ce prompt).

- **Si `companion_html_guide` (défini dans `TARGET`) a été explicitement fourni ou désigné par la personne pour cette session** : appliquer d'abord la **règle de fraîcheur des fichiers fournis** (voir plus haut) — ne jamais l'utiliser comme référence sans avoir vérifié que son bloc est à jour par rapport au bloc source actuel du guide. S'il est confirmé à jour (voir la règle de fraîcheur : bloc `i18n-<lang_code>` sans clé manquante), le consulter et reprendre à l'identique ses choix de terminologie déjà établis — noms de catégories (ex. `Frigates`, `Portal Glyphs`, `Class (C→S)`), libellés de badges (`duplicate`, `non-functional`, `to verify`), et termes récurrents (`tag`, `tint/tinting`). S'il est obsolète, suivre la procédure décrite dans la règle de fraîcheur (signaler, décrire l'écart, demander comment procéder) plutôt que de l'utiliser tel quel ou de l'ignorer silencieusement.
- **Dans tout autre cas** (aucun `companion_html_guide` fourni pour cette session, y compris si un guide HTML dans la langue cible existe quelque part dans l'historique de la conversation sans avoir été désigné comme référence) : ne pas aller le chercher, ne pas le mentionner. Les choix de terminologie faits ici font alors référence pour la suite — le prompt `prompt_translation_HTML_GUIDE_LANG.md` s'appuiera dessus via son propre champ `companion_readme` lors d'une traduction ultérieure du guide HTML, dans une session séparée. Traduire avec la même rigueur terminologique que si le guide HTML à jour existait déjà, puisque ce README deviendra lui-même la référence.

**Ancien README de la langue cible** (cas d'une langue déjà traduite autrefois). Il sert de **référence de vocabulaire seulement** : ne jamais le porter ni le compléter (voir la note en tête de ce prompt). Traduire phrase par phrase depuis la version à jour de la source ; reprendre une tournure déjà validée de l'ancien README quand le sens source n'a pas changé, après l'avoir vérifiée contre la source ; et **lister dans le rapport chaque terme volontairement amélioré** (ancien terme → nouveau terme, raison).

### 8. Vérification finale (auto-relecture obligatoire avant livraison)
- Le nom du fichier `.html` en tête de document est-il bien `NMS_txt_code.html`, sans suffixe de langue, et le nom du README (badge et texte alternatif) correspond-il à `output_filename` ? (voir règle §0)
- Chaque lien du sommaire correspond-il à un titre réellement présent et correctement traduit ?
- Aucune balise de jeu, chemin de fichier ou nom technique n'a été traduit par erreur ?
- Le ton reste-t-il fidèle à l'original sur l'ensemble du document, pas seulement dans l'introduction ?
- La structure Markdown (tableaux compris) est-elle identique ligne pour ligne à la source ?
- Chaque encadré `🔧 Détail technique` conserve-t-il l'emoji, le format blockquote, et le libellé traduit à l'identique à chaque occurrence — avec un registre plus neutre que le texte courant qui l'entoure ?
- Aucune formule ou notation technique (ex. la formule de luminance, `ITU-R BT.601`) n'a été altérée ou dont le séparateur décimal aurait été localisé par erreur ?
- Les placeholders pédagogiques génériques (`Texte`, `NOM_COULEUR`/`COULEUR`) ont-ils bien été adaptés en langue cible, comme dans le bloc `i18n-<lang_code>` du guide, sans être confondus avec de vraies balises intouchables ?
- Les deux commentaires d'en-tête (version traduite et « Translation parameters ») sont-ils présents, avec le md5 de la source réellement utilisée, et les commentaires HTML du corps sont-ils traduits ?
- Le ton appliqué correspond-il à la valeur de `tone` confirmée (par défaut `compromise`), et non à celui du guide HTML ?
- Si `companion_html_guide` a été explicitement fourni/désigné pour cette session : la terminologie utilisée correspond à son bloc `i18n-<lang_code>`, **confirmé à jour** (fraîcheur vérifiée par `--todo` et par `_meta.source_version`). Sinon (cas le plus fréquent : aucun `companion_html_guide` fourni) : la terminologie choisie ici est cohérente en interne et prête à servir de référence pour une traduction ultérieure du guide HTML, sans qu'il y ait eu lieu de rechercher ou mentionner un guide cible existant ailleurs dans la conversation.

---

## VÉRIFICATIONS TECHNIQUES RECOMMANDÉES (avant la relecture finale)

Cohérent avec le principe déjà établi pour ce projet (outils nommés et vérifiables plutôt qu'inspection ad hoc — voir `prompt_fix_allcode.md` §L.45bis) : privilégier une vérification programmatique aux points de rupture silencieuse identifiés ci-dessus, plutôt qu'une simple relecture visuelle.

- **Structure ligne à ligne** : après avoir retiré le commentaire « Translation parameters », comparer le type de chaque ligne de la traduction à celui de la ligne source (vide, titre par niveau, ligne de tableau par nombre de colonnes, puce par indentation, citation, séparateur, balise HTML) : tout écart est à corriger.
- **Comptes par ligne** : nombre de passages en gras, en italique et en code identique ligne par ligne ; mêmes nombres (hors séparateur décimal en prose, voir §4), mêmes URLs et liens externes (hors badge du README), mêmes emojis.
- **Correspondance sommaire ↔ titres** : calculer l'ancre de chaque titre selon la convention GitHub décrite au §5 et la comparer aux liens du sommaire ; contrôler aussi tous les autres liens internes `](#...)` du document.
- **Détection de résidus de la langue source** : recherche systématique (regex) des mots de vocabulaire spécifique au projet dans leur forme source (ex. « balise », « teinte », « doublon », « onglet » pour une source française) sur l'ensemble du fichier traduit, commentaires HTML compris — pas seulement une relecture visuelle, qui rate facilement une occurrence isolée dans un paragraphe long. Rester vigilant aux faux positifs (mots de la langue cible partageant une sous-chaîne avec un mot source).
- **Vérification des formules/notations techniques intouchables** : rechercher chaque formule ou désignation technique (ex. `ITU-R BT.601`, la formule de luminance) dans le document traduit et confirmer qu'elle est strictement identique, caractère pour caractère, à la source — y compris l'absence de localisation du séparateur décimal.
- **Cohérence terminologique croisée avec `companion_html_guide`** (si utilisé) : extraire du bloc `i18n-<lang_code>` les valeurs des clés `cat.*`, `flag.*`, `nav.tab.*` et `copy.template_word`, et confirmer par recherche textuelle qu'elles apparaissent à l'identique dans le README (les catégories non citées dans le README sont sans objet).
- **Transparence** : toute vérification non exécutée doit être déclarée comme telle dans le rapport (jamais présentée comme passée). Ces vérifications se font en quelques lignes de script jetables (Python ou shell) ; il n'est pas prévu d'ajouter de script au dépôt.

Ces vérifications ne remplacent pas la relecture humaine finale ci-dessus, elles la précèdent et la sécurisent.

---

## LIVRABLE ATTENDU

Un unique fichier Markdown nommé selon `output_filename`, contenant la traduction complète, prêt à être commité dans le dépôt sans retouche supplémentaire.

**Rapport de livraison** (dans la conversation, pas dans le fichier), toujours dans cet ordre :
1. Fichiers utilisés (nom, lignes, taille, md5, version) et md5 et taille du fichier livré.
2. Paramètres `TARGET` appliqués et références utilisées (bloc `i18n-<lang_code>` et son md5, ancien README éventuel).
3. Écarts avec la source ou avec ce prompt (exceptions de session) et modifications proposées pour le README source (ex. nombre de langues).
4. Vérifications exécutées, avec leurs résultats, et vérifications **non exécutées**.
5. Choix de traduction notables : guillemets, séparateurs, termes volontairement améliorés par rapport à l'ancien README, nouvelle terminologie (glossaire).
6. Éléments non vérifiés (rendu GitHub) et termes de jeu douteux à vérifier en jeu.
7. Lignes proposées pour « HISTORIQUE D'UTILISATION » (et pour le journal si ce prompt a changé), à n'appliquer qu'après un feu vert distinct.

---

## HISTORIQUE D'UTILISATION

Table à compléter à chaque usage de ce prompt, pour tracer quelle version de quel fichier a été traduite, avec quels réglages — évite toute ambiguïté en cas de reprise de ce prompt dans une conversation ultérieure ou par une autre personne. Elle se met à jour **sur proposition** (voir « PROTECTION DES MODIFICATIONS DE CE PROMPT », point 5).

| Date | Fichier source (nom + repère de version) | Fichier produit | md5 du livrable | `target_language` | `target_variant` | `tone` | `fidelity_style` | `companion_html_guide` utilisé ? |
|---|---|---|---|---|---|---|---|---|
| 2026-09-08 | `README_FR.md` (248 lignes, 4 encadrés `🔧 Détail technique`, mention ITU-R BT.601/XSS/16 icônes réserve) | `README_EN.md` | non relevé | English | neutral/standard | compromise (sober, key imagery kept) | idiomatic | Non fourni pour cette session |
| 2026-09-09 | `README_FR.md` (248 lignes, hash `e36972f2f6f0f926335caa49aba5396f`) | `README_ES.md` | non relevé | Español | neutral/standard | passionate/stylized | idiomatic | `NMS_txt_code_ES.html` fourni explicitement, fraîcheur confirmée (identique à la traduction HTML produite le même jour) |
| 2026-10-25 | `README_FR.md` v2.1 (309 lignes, md5 `e3ce5e7638a7b06f3ce3868f098ee6ac`, corrigé le jour même : 3 langues, ~358 Ko) | `README_ES.md` v2.1 (retraduit depuis la source à jour ; ancien README_ES v1.1 consulté comme référence de vocabulaire seulement) | `5ce4cda27c85973d0a28ea0305ece105` | Español | neutral/standard | compromise (sober, key imagery kept) — livré d'abord en passionate/stylized (md5 `97d36d26…`), corrigé le jour même | idiomatic | bloc `i18n-es` de `NMS_txt_code.html` v2.0 (md5 `75a04cc4966d23e4b6ccf4eb63909f17`), désigné par la personne, fraîcheur confirmée |
| 2026-10-25 | `README_FR.md` v2.1 (309 lignes, md5 `e3ce5e7638a7b06f3ce3868f098ee6ac`) | `README_EN.md` v2.1 (ancien README_EN v1.3 consulté comme référence de vocabulaire seulement) | `10899991518412e1b06216470f34f8c8` | English | neutral/standard | compromise (sober, key imagery kept) | idiomatic | bloc `i18n-en` de `NMS_txt_code.html` v2.0 (md5 `75a04cc4966d23e4b6ccf4eb63909f17`), désigné par la personne, fraîcheur confirmée |
