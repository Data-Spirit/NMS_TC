# Translation Prompt — NMS_TC README

> **Dernière mise à jour de ce prompt : 2026-09-09 (2)** — ajout de l'entrée d'historique correspondant à la traduction ES du 2026-09-09 (`README_FR.md` → `README_ES.md`, hash `e36972f2f6f0f926335caa49aba5396f`, `companion_html_guide` `NMS_txt_code_ES.html` utilisé après confirmation de fraîcheur). S'ajoute aux changements précédents du même jour (auto-versionnage, section « LES FICHIERS FOURNIS », règle de fraîcheur étendue, restriction de `companion_html_guide` à la fourniture explicite, protection des modifications de ce prompt, feu vert de traduction, vérifications techniques recommandées, colonne de traçabilité, correction des noms de fichiers obsolètes, réorganisation des sections). Cette ligne doit être mise à jour à chaque modification validée de ce prompt (voir section « PROTECTION DES MODIFICATIONS DE CE PROMPT ») — si elle semble absente ou visiblement ancienne par rapport au contenu, traiter ce prompt comme potentiellement obsolète et le signaler à la personne avant de l'utiliser.

Prompt réutilisable pour traduire le README du projet NMS_TC dans une nouvelle langue.
Pour une nouvelle traduction : copier ce fichier, changer uniquement le bloc `TARGET`, et donner ce fichier + le `README_FR.md` source à Claude.

Ce prompt est le pendant documentaire de `prompt_translation_HTML_GUIDE_LANG.md`. Les deux partagent la même exigence de qualité et la même terminologie (voir §7 Cohérence terminologique), mais celui-ci s'applique à un texte pur (Markdown), pas à un fichier fonctionnel : une erreur ici casse la lisibilité ou la cohérence documentaire, pas une fonctionnalité.

> **Note (README_FR mis à jour)** : le fichier `README_FR.md` a évolué depuis les premières traductions — notamment l'ajout d'encadrés `> **🔧 Détail technique :** ...` documentant le fix XSS, le déplacement du bloc `ICON_DATA` en fin de script, la formule de luminance `ITU-R BT.601`, et la décision de conserver 16 icônes de boutons manette en réserve. Si vous comparez avec d'anciennes traductions (EN/ES antérieures à cette mise à jour), ne soyez pas surpris d'y trouver du contenu absent des versions précédentes : ce n'est pas une divergence à corriger dans la source, c'est le README qui s'est enrichi. Toute retraduction doit repartir de cette version à jour, jamais porter/compléter une ancienne traduction existante.

---

## LES FICHIERS FOURNIS — RÔLE DE CHACUN (à lire avant tout le reste)

Une session de traduction avec ce prompt fournit typiquement deux fichiers, parfois trois. Chacun a un rôle précis et **un seul est le texte à traduire** :

| Fichier | Rôle | Faut-il le traduire ? |
|---|---|---|
| `README_<LANG_SOURCE>.md` (ex. `README_FR.md`) | **La source** : le README à traduire vers `target_language`. | **Oui — c'est l'unique cible de la traduction.** |
| `prompt_translation_README_LANG.md` (ce fichier) | Le mode d'emploi : quoi traduire, quoi ne jamais toucher, comment vérifier. | Non — c'est la consigne, pas un contenu à traduire. |
| `NMS_txt_code_<LANG_SOURCE>.html` (optionnel, ex. `NMS_txt_code_FR.html`, dans la même langue que le README source) | Un **document de contexte** éventuel, donné pour que la traduction du README soit fidèle au fonctionnement réel du guide HTML qu'il documente. | **Non, jamais dans cette session.** Ce guide HTML n'est pas la cible — il n'est là que pour informer la traduction du README. Le traduire relèverait d'une tout autre session, avec `prompt_translation_HTML_GUIDE_LANG.md`. |

**Repère utile (signal, pas règle absolue)** : si la personne fournit `prompt_translation_README_LANG.md`, l'intention est presque toujours de traduire le README, pas le guide HTML qui l'accompagne — et symétriquement, si elle fournit `prompt_translation_HTML_GUIDE_LANG.md`, l'intention est de traduire le HTML. Un guide HTML fourni à côté du prompt README (ou l'inverse) est là pour du **contexte**, pas comme cible implicite. En cas de doute réel sur l'intention, poser la question plutôt que présumer.

**À ne pas confondre avec `companion_html_guide`** (voir bloc `TARGET` et §7 plus bas) : ce guide HTML de contexte, s'il est fourni, est dans la **langue source** (celle du README à traduire, souvent le français) — il ne peut donc pas servir de référence terminologique pour la langue cible. `companion_html_guide` désigne un cas différent : un `NMS_txt_code_<lang_code>.html` **déjà traduit dans la langue cible** (ex. `NMS_txt_code_ES.html` pour une traduction vers l'espagnol), utilisé pour réutiliser le même vocabulaire d'une langue à l'autre. Les deux notions peuvent coexister dans une même session mais ne sont jamais le même fichier.

**`companion_html_guide` n'est en jeu que si la personne le fournit ou le désigne explicitement pour la session en cours.** Ne jamais aller chercher de soi-même, dans l'historique de la conversation, un guide HTML déjà traduit dans la langue cible lors d'un tour antérieur pour le traiter comme `companion_html_guide` — même s'il existe, même s'il porte le nom attendu (`NMS_txt_code_<lang_code>.html`). Tant que la personne n'a pas explicitement indiqué qu'un tel fichier doit servir de référence pour cette session, `companion_html_guide` est considéré comme **absent**, un point c'est tout : ne pas le mentionner, ne pas le proposer, ne pas y faire référence. Un cas fréquent : seul le README source est fourni, avec l'intention explicite de traduire le guide HTML correspondant *plus tard*, dans un tour ultérieur séparé. Dans ce cas, cette traduction du README est **autosuffisante** et devient elle-même la référence terminologique pour la traduction future du HTML (voir §7) — sans qu'il soit utile ni pertinent de rouvrir la question d'un `companion_html_guide` existant ou non.

**Note de portée** : ce prompt suppose implicitement que la langue source du README est le français (`README_FR.md`), conformément au fait que le français est la langue de référence maîtresse du projet. Si un jour la langue source d'une traduction demandée n'est pas le français (ex. traduire depuis un `README_EN.md`), le rôle des fichiers reste le même mais les exemples ci-dessous doivent être adaptés en conséquence — signaler ce cas à la personne s'il se présente plutôt que de présumer silencieusement.

---

## TARGET

```yaml
target_language: English          # ex: English, Deutsch, Español, 日本語
target_variant: neutral/standard  # ex: US, UK, neutral/standard, none (pour langues sans variante notable)
lang_code: EN                     # code de langue à 2 lettres majuscules (EN, ES, DE, JA...) — voir règle §0 ci-dessous
output_filename: README_EN.md     # convention : README_<lang_code>.md
source_file: README_FR.md
tone: passionate/stylized         # ex: passionate/stylized, neutral/technical, compromise — ton éditorial à conserver ou adapter (voir §2)
fidelity_style: idiomatic         # ex: idiomatic (adaptation naturelle), literal (fidèle/littérale), case-by-case (voir §1)
companion_html_guide: NMS_txt_code_EN.html   # guide HTML déjà TRADUIT dans la langue cible — à renseigner UNIQUEMENT si la personne le fournit ou le désigne explicitement pour cette session. Ne jamais le déduire d'un fichier déjà vu dans la conversation. Laisser vide/absent si non fourni : cette traduction README devient alors elle-même la référence terminologique (voir §7).
```

---

## RÈGLE DE DÉMARRAGE OBLIGATOIRE — à exécuter avant toute traduction, même répétée

**Ne jamais présumer que les valeurs de `TARGET` (notamment `tone` et `fidelity_style`) restent valables d'une session à l'autre, même si cette même personne a déjà utilisé ce prompt auparavant avec des valeurs identiques.** Une session de traduction précédente ne vaut pas confirmation pour la session en cours.

Avant de commencer toute traduction, reformuler explicitement à la personne les valeurs actuelles de `target_language`, `target_variant`, `tone` et `fidelity_style` (en précisant, le cas échéant, le choix fait lors d'un usage précédent comme simple rappel, jamais comme valeur acquise), et demander confirmation ou modification. Ne démarrer la traduction qu'après cette confirmation explicite.

## RÈGLE DE FRAÎCHEUR DES FICHIERS FOURNIS — à exécuter avant toute traduction

**Un nom de fichier identique ne garantit jamais un contenu identique.** Que ce soit le README source, ce prompt lui-même, le guide HTML de contexte éventuel, ou `companion_html_guide` : si l'un de ces fichiers est fourni à nouveau au cours d'une conversation (même sous le nom exact déjà vu précédemment), il faut le traiter comme potentiellement différent de la version déjà en mémoire — **jamais comme un doublon silencieux**. En pratique, si la personne redonne un fichier portant un nom déjà rencontré, c'est le plus souvent précisément *parce qu'il a été mis à jour, corrigé ou enrichi* depuis la dernière fois.

Avant de commencer, pour **chacun** des fichiers fournis dans le tour de conversation en cours :

1. **README source** : confirmer explicitement à la personne son nom, son nombre de lignes (ou une autre métrique simple : taille en octets, nombre de mots), et au moins un élément de contenu distinctif permettant de confirmer qu'il s'agit bien de la dernière version en date (ex. présence des encadrés `> **🔧 Détail technique :**`, mention du fix XSS, de la formule `ITU-R BT.601`, ou de la décision des 16 icônes en réserve). **Attention : le nombre de lignes seul est un indice, pas une preuve** — deux versions différentes peuvent coïncidentellement partager le même nombre de lignes. En cas de doute réel (versions proches, différences suspectées mais non confirmées), calculer et comparer un hash (`md5sum`) est une vérification plus robuste.
2. **Guide HTML de contexte fourni avec ce tour** (s'il y en a un) : ne pas se contenter de le lire — comparer sa structure avec toute version de ce même fichier déjà vue dans la conversation, pour confirmer qu'il s'agit bien de la version la plus à jour.
3. **`companion_html_guide`** (uniquement s'il a été explicitement fourni ou désigné par la personne pour cette session — jamais rappelé de mémoire de sa propre initiative, voir règle ci-dessus) : **avant de l'utiliser comme référence terminologique**, comparer sa structure (noms de catégories, libellés de badges, présence d'éléments distinctifs récents comme des `aria-label` traduits ou des placeholders pédagogiques adaptés) avec celle du guide HTML source actuel. Si des éléments distinctifs présents côté source sont absents côté `companion_html_guide`, ce dernier est **obsolète** : ne pas l'utiliser tel quel comme référence terminologique sans le signaler explicitement à la personne, décrire précisément ce qui manque, et lui demander comment procéder (le retraduire d'abord, s'appuyer uniquement sur les termes de base déjà validés, ou traiter ce README comme la nouvelle référence terminologique).

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

### 0. Règle de correspondance des suffixes de langue (IMPORTANT)

Ce README documente un fichier `.html` compagnon (le guide interactif lui-même), et **les deux fichiers doivent toujours partager le même suffixe de langue** :

| README | Guide HTML documenté |
|---|---|
| `README_FR.md` | `NMS_txt_code_FR.html` |
| `README_EN.md` | `NMS_txt_code_EN.html` |
| `README_ES.md` | `NMS_txt_code_ES.html` |
| `README_<lang_code>.md` | `NMS_txt_code_<lang_code>.html` |

**Action obligatoire** : dans la ligne d'introduction du README (juste sous le titre H1, celle qui donne le nom du fichier, son poids et ses caractéristiques), remplacer le nom du fichier `.html` par `NMS_txt_code_<lang_code>.html`, où `<lang_code>` est exactement celui défini dans `TARGET` ci-dessus. Ne jamais laisser le suffixe de la langue source (ex. `_FR`) dans un README traduit.

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
- **Conserver le ton d'origine tel quel** : ce README a un ton passionné, engagé, parfois stylé/imagé (ex. métaphores comme « le guide s'habille avec les couleurs qu'il documente »). Ne neutralise pas ce ton vers un style corporate ou plat.
- Reste dans un registre professionnel mais chaleureux, cohérent avec un projet communautaire fait par passion.
- **Exception délibérée — les encadrés `🔧 Détail technique`** : ces encadrés (voir §5) sont volontairement rédigés dans un registre plus neutre et précis que le reste du document. Ne pas y réinjecter le ton passionné du texte courant, et ne pas non plus aplatir le ton du texte courant pour l'aligner sur celui de l'encadré : les deux registres doivent rester distincts, comme dans la source.

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

**Nuance importante — vraie balise de jeu vs placeholder pédagogique** : certaines chaînes qui *ressemblent* à des balises du jeu sont en réalité des gabarits d'exemple générique inventés pour l'explication (ex. `NOM_COULEUR` ou `COULEUR` dans `<NOM_COULEUR>Texte</>`), pas de vrais identifiants comme `VISOR`. Ces placeholders pédagogiques doivent être **adaptés/traduits** comme le mot `Texte` l'est déjà (ex. `COLOR_NAME`/`COLOR` en anglais) — voir §5 point suivant. En cas de doute sur la nature d'une chaîne en majuscules entre chevrons, vérifier si elle apparaît telle quelle dans les tableaux `COLORS`/`ICONS` du fichier `.html` source (vraie balise → intouchable) ou seulement dans la prose du README à titre d'exemple (placeholder → à adapter).

### 5. Éléments à adapter/régénérer
- **Ancres du sommaire** : régénérer chaque lien `#ancre` à partir du titre traduit selon la convention de la plateforme cible (GitHub : minuscules, espaces → tirets, accents/caractères spéciaux supprimés). Vérifier que chaque lien du sommaire pointe bien vers le bon titre traduit.
- **Emojis de titres** : conserver les mêmes emojis, seul le texte du titre change.
- **Emojis inline hors-titre (encadrés récurrents)** : le README utilise aussi un emoji comme marqueur récurrent en plein texte, hors des titres — actuellement 🔧 pour introduire un encadré **`> **🔧 Détail technique :** ...`**. Conserver l'emoji et le format blockquote (`>`) à l'identique ; traduire le libellé **"Détail technique"** une seule fois puis le réutiliser mot pour mot à chaque occurrence (traitement identique à un nom de catégorie récurrent, pas une reformulation libre à chaque fois).
- **Placeholders pédagogiques génériques** (voir §4) : des gabarits d'exemple comme `Texte` dans `<NOM_COULEUR>Texte</>`, ou `NOM_COULEUR`/`COULEUR` eux-mêmes, doivent être adaptés en langue cible (ex. `Text` et `COLOR_NAME`/`COLOR` en anglais) — ne pas les confondre avec de vraies balises intouchables.
- Licence : traduire le texte explicatif autour, mais garder le nom de la licence (`CC BY-NC-SA 4.0`) et le chemin du fichier inchangés.

### 6. Structure et formatage
- Conserver **exactement** la structure Markdown source : mêmes niveaux de titres (`#`, `##`, `###`), mêmes tableaux (nombre de colonnes, alignement, ordre des lignes), mêmes séparateurs `---`, mêmes listes à puces, mêmes mises en gras/italique aux mêmes endroits sémantiques.
- Ne pas ajouter, supprimer ou réorganiser de sections par rapport à la source.
- Ne pas raccourcir ni résumer un passage : traduction intégrale, phrase pour phrase, section pour section.

### 7. Cohérence terminologique bidirectionnelle avec le guide HTML correspondant
Une fois qu'un terme récurrent est traduit d'une certaine façon (ex. « balise » → « tag »), garder cette même traduction partout dans le document sans varier. Construire mentalement (ou explicitement si utile) un petit glossaire des termes récurrents du projet avant de traduire, pour garantir cette cohérence sur tout le fichier.

Le README et le guide HTML décrivent le même produit et doivent employer un vocabulaire strictement identique. Cette règle est **bidirectionnelle et sans ordre imposé** : ni le README ni le HTML n'est par défaut « traduit en premier » — cela dépend simplement de ce que la personne demande dans chaque session (voir le tableau des rôles des fichiers en tête de ce prompt).

- **Si `companion_html_guide` (défini dans `TARGET`) a été explicitement fourni ou désigné par la personne pour cette session** : appliquer d'abord la **règle de fraîcheur des fichiers fournis** (voir plus haut) — ne jamais l'utiliser comme référence sans avoir vérifié qu'il est à jour par rapport au guide HTML source actuel. S'il est confirmé à jour, le consulter et reprendre à l'identique ses choix de terminologie déjà établis — noms de catégories (ex. `Frigates`, `Portal Glyphs`, `Class (C→S)`), libellés de badges (`duplicate`, `non-functional`, `to verify`), et termes récurrents (`tag`, `tint/tinting`). S'il est obsolète, suivre la procédure décrite dans la règle de fraîcheur (signaler, décrire l'écart, demander comment procéder) plutôt que de l'utiliser tel quel ou de l'ignorer silencieusement.
- **Dans tout autre cas** (aucun `companion_html_guide` fourni pour cette session, y compris si un guide HTML dans la langue cible existe quelque part dans l'historique de la conversation sans avoir été désigné comme référence) : ne pas aller le chercher, ne pas le mentionner. Les choix de terminologie faits ici font alors référence pour la suite — le prompt `prompt_translation_HTML_GUIDE_LANG.md` s'appuiera dessus via son propre champ `companion_readme` lors d'une traduction ultérieure du guide HTML, dans une session séparée. Traduire avec la même rigueur terminologique que si le guide HTML à jour existait déjà, puisque ce README deviendra lui-même la référence.

### 8. Vérification finale (auto-relecture obligatoire avant livraison)
- Le nom du fichier `.html` en tête de document porte-t-il bien le suffixe `<lang_code>` cible (et non celui de la langue source) ? (voir règle §0)
- Chaque lien du sommaire correspond-il à un titre réellement présent et correctement traduit ?
- Aucune balise de jeu, chemin de fichier ou nom technique n'a été traduit par erreur ?
- Le ton reste-t-il fidèle à l'original sur l'ensemble du document, pas seulement dans l'introduction ?
- La structure Markdown (tableaux compris) est-elle identique ligne pour ligne à la source ?
- Chaque encadré `🔧 Détail technique` conserve-t-il l'emoji, le format blockquote, et le libellé traduit à l'identique à chaque occurrence — avec un registre plus neutre que le texte courant qui l'entoure ?
- Aucune formule ou notation technique (ex. la formule de luminance, `ITU-R BT.601`) n'a été altérée ou dont le séparateur décimal aurait été localisé par erreur ?
- Les placeholders pédagogiques génériques (`Texte`, `NOM_COULEUR`/`COULEUR`) ont-ils bien été adaptés en langue cible, sans être confondus avec de vraies balises intouchables ?
- Si `companion_html_guide` a été explicitement fourni/désigné pour cette session : la terminologie utilisée y correspond, **confirmé à jour** (fraîcheur vérifiée par comparaison avec le guide HTML source actuel). Sinon (cas le plus fréquent : aucun `companion_html_guide` fourni) : la terminologie choisie ici est cohérente en interne et prête à servir de référence pour une traduction ultérieure du guide HTML, sans qu'il y ait eu lieu de rechercher ou mentionner un guide cible existant ailleurs dans la conversation.

---

## VÉRIFICATIONS TECHNIQUES RECOMMANDÉES (avant la relecture finale)

Cohérent avec le principe déjà établi pour ce projet (outils nommés et vérifiables plutôt qu'inspection ad hoc — voir `prompt_fix_allcode.md` §L.45bis) : privilégier une vérification programmatique aux points de rupture silencieuse identifiés ci-dessus, plutôt qu'une simple relecture visuelle.

- **Correspondance sommaire ↔ titres** : extraire par script (regex sur les lignes `#`/`##`/`###`) la liste des titres réels du document traduit, et comparer avec la liste des ancres `#...` du sommaire — une divergence indique un lien de sommaire cassé ou un titre mal régénéré.
- **Détection de résidus de la langue source** : recherche systématique (regex) des mots de vocabulaire spécifique au projet dans leur forme source (ex. « balise », « teinte », « doublon », « onglet » pour une source française) sur l'ensemble du fichier traduit — pas seulement une relecture visuelle, qui rate facilement une occurrence isolée dans un paragraphe long. Rester vigilant aux faux positifs (mots de la langue cible partageant une sous-chaîne avec un mot source).
- **Vérification des formules/notations techniques intouchables** : rechercher chaque formule ou désignation technique (ex. `ITU-R BT.601`, la formule de luminance) dans le document traduit et confirmer qu'elle est strictement identique, caractère pour caractère, à la source — y compris l'absence de localisation du séparateur décimal.
- **Cohérence terminologique croisée avec `companion_html_guide`** (si utilisé) : lister les termes récurrents du glossaire (§7) et confirmer par recherche textuelle qu'ils apparaissent avec la même traduction dans les deux documents.

Ces vérifications ne remplacent pas la relecture humaine finale ci-dessus, elles la précèdent et la sécurisent.

---

## LIVRABLE ATTENDU

Un unique fichier Markdown nommé selon `output_filename`, contenant la traduction complète, prêt à être commité dans le dépôt sans retouche supplémentaire.

---

## HISTORIQUE D'UTILISATION

Table à compléter à chaque usage de ce prompt, pour tracer quelle version de quel fichier a été traduite, avec quels réglages — évite toute ambiguïté en cas de reprise de ce prompt dans une conversation ultérieure ou par une autre personne.

| Date | Fichier source (nom + repère de version) | Fichier produit | `target_language` | `target_variant` | `tone` | `fidelity_style` | `companion_html_guide` utilisé ? |
|---|---|---|---|---|---|---|---|
| 2026-09-08 | `README_FR.md` (248 lignes, 4 encadrés `🔧 Détail technique`, mention ITU-R BT.601/XSS/16 icônes réserve) | `README_EN.md` | English | neutral/standard | compromise (sober, key imagery kept) | idiomatic | Non fourni pour cette session |
| 2026-09-09 | `README_FR.md` (248 lignes, hash `e36972f2f6f0f926335caa49aba5396f`) | `README_ES.md` | Español | neutral/standard | passionate/stylized | idiomatic | `NMS_txt_code_ES.html` fourni explicitement, fraîcheur confirmée (identique à la traduction HTML produite le même jour) |
