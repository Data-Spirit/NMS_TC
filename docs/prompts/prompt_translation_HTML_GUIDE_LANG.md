<!-- Version du fichier 
> Version : 4.0
> Dernière modification : 2026-10-20
-->

# Translation Prompt — NMS_TC HTML Guide (guide multilingue en un seul fichier)

> **Dernière mise à jour de ce prompt : 2026-10-20** — refonte complète pour le guide multilingue en un seul fichier `NMS_txt_code.html` : on ne traduit plus un fichier HTML par langue, mais **un bloc de langue** (dictionnaire de clés) à l'intérieur du fichier unique. Remplacés : le mode « mise à jour incrémentale » de fichiers séparés, les scripts `trans_script_1_substitutions_*`, `_2_update_translation`, `_4_verify_symmetry`, les règles de correspondance des suffixes de langue et des clés de catégorie (devenues des identifiants neutres). Ajoutés : lecture et écriture des paramètres de traduction dans `_meta.target`, liste de travail des clés à traduire (`--todo`, `--since`), nouveaux scripts `trans_script_1_check_keys` à `trans_script_4_test_render`, règles d'écriture d'un bloc JSON, traduction cohérente des pseudo-noms et du mot-témoin. Ajoutés aussi : emplacement et modèles d'un bloc, vérification préalable de la langue (écriture de droite à gauche, polices, pluriels), encodage, comparaison hors bloc, clés supprimées de la source, cas sans version précédente, prérequis des outils, contexte du projet et terminologie officielle du jeu, traduction toujours depuis le français. Conservés : protocole de modification de ce prompt, feu vert avant de traduire, règles de fraîcheur, de ton, de terminologie et de longueur, rapport de livraison standard et glossaire. Cette ligne doit être mise à jour à chaque modification validée de ce prompt (voir « PROTECTION DES MODIFICATIONS DE CE PROMPT ») — si elle semble absente ou visiblement ancienne par rapport au contenu, traiter ce prompt comme potentiellement obsolète et le signaler à la personne avant de l'utiliser.

Prompt réutilisable pour **ajouter une langue** ou **mettre à jour une langue** dans `NMS_txt_code.html` (le guide interactif autonome et multilingue).

Ce prompt est le pendant technique de `prompt_translation_README_LANG.md`. Les deux partagent la même exigence de qualité et la même terminologie, mais celui-ci s'applique à un fichier **HTML/CSS/JS fonctionnel** : une erreur dans un bloc de langue peut dégrader l'affichage de cette langue, pas seulement une phrase.

---

## COMMENT EST FAIT LE GUIDE (à lire avant tout le reste)

`NMS_txt_code.html` est un unique fichier autonome. Tout le texte visible vient de **blocs de langue** placés en fin de fichier :

```html
<!-- ===== LANGUE : FRANÇAIS (source / par défaut) ===== -->
<script type="application/json" id="i18n-fr"> { "_meta": { … }, "clé": "texte", … } </script>
<!-- ===== LANGUE : ENGLISH ===== -->
<script type="application/json" id="i18n-en"> { "_meta": { … }, "clé": "texte", … } </script>
```

- Le HTML ne contient **plus de texte traduisible** : chaque élément porte une clé (`data-i18n="infos.li.03"`, ou `data-i18n-attr="placeholder:clé"` pour les attributs). Le code JavaScript lit les clés (`T('clé')`, `TA('clé')`).
- **Le bloc français est la source** : toute nouvelle fonctionnalité s'écrit d'abord en français, puis se traduit dans les autres blocs. Ce prompt ne modifie **jamais** le bloc français ni le code : ce sont des tâches distinctes, avec leur propre validation.
- Chaque bloc commence par un champ **`_meta`** : `native_name` (nom de la langue dans sa propre langue), `flag` (drapeau emoji), `lang_code`, `translation_version`, `updated`, et `target` (les paramètres de traduction ci-dessous). Le sélecteur de langue du guide se construit à partir de `_meta`.
- Un texte peut contenir une **mise en forme limitée** : `strong`, `em`, `b`, `i`, `code`, `span class='…'`, `br`, `a`. Tout le reste est neutralisé à l'affichage.
- Une valeur peut être une chaîne **ou une liste de morceaux** recollés bout à bout, pour garder un long paragraphe lisible sur plusieurs lignes.
- **Repli** : une clé absente dans une langue s'affiche dans la langue source (jamais une erreur), mais le contrôle la signale.

## CONTEXTE DU PROJET (pour le ton et le vocabulaire)

Ce guide s'adresse aux joueurs de **No Man's Sky** qui renomment en jeu leurs bases, vaisseaux, coffres ou sauvegardes à l'aide de **balises de couleur et d'icône**. Ces balises sont des codes internes du jeu (`<PET1><IMG>TECH1<> Techs</>`) que le guide explique, illustre et permet d'essayer. Le lecteur est un joueur, pas un développeur : le texte doit être clair, précis et agréable, sans jargon inutile.

## FICHIERS FOURNIS — RÔLE DE CHACUN

| Fichier | Rôle | Faut-il le modifier ? |
|---|---|---|
| `NMS_txt_code.html` | Le guide, qui contient le bloc source et les blocs déjà traduits. | **Oui, uniquement le bloc de la langue cible** (le créer ou le mettre à jour). |
| Version précédente de `NMS_txt_code.html` (facultative) | Sert à détecter les clés modifiées dans la source depuis la dernière traduction (`--since`). | Non. |
| `prompt_translation_HTML_GUIDE_LANG.md` (ce fichier) | Le mode d'emploi. | Non. |
| `README_<LANG>.md` fourni pour contexte | Document de contexte dans la langue source, pour que la traduction soit fidèle à la conception du projet. | **Non, jamais dans cette session** : le traduire relève de `prompt_translation_README_LANG.md`. |
| `docs/scripts/trans_script_*` | Les scripts de contrôle (voir plus bas), à exécuter, pas à traduire. | Non. |

**`companion_readme`** (un `README_<lang_code>.md` déjà traduit dans la langue cible, pour réutiliser le même vocabulaire) n'est en jeu que si la personne le fournit ou le désigne **explicitement** pour la session. Ne jamais aller le chercher de soi-même dans l'historique de la conversation. Sans lui, les choix de terminologie faits ici font référence pour la traduction ultérieure du README.

**Note de portée** : ce prompt suppose que la langue source est le français. Si ce n'est plus le cas un jour, le signaler à la personne plutôt que de présumer.

---

## TARGET

```yaml
target_language: English            # ex : English, Deutsch, Español, 日本語
lang_code: en                       # code de langue en minuscules (BCP-47) : en, es, de, pt-BR, zh-Hans… DOIT être identique à l'id du bloc (i18n-en) et à _meta.lang_code
native_name: English                # nom de la langue dans sa propre langue (affiché dans le sélecteur)
flag: "🇬🇧"                         # drapeau emoji le plus correspondant à la langue (un repli image reste possible si l'affichage pose problème)
target_variant: neutral/standard (US)   # ex : US, UK, neutral/standard, none
tone: passionate/stylized           # ex : passionate/stylized, neutral/technical, compromise (sober, key imagery kept)
fidelity_style: idiomatic           # ex : idiomatic (adaptation naturelle), literal, case-by-case
aria_label_style: B                 # A (miroir du placeholder) ou B (libellé autonome pensé pour l'oral) : voir « CE QUI SE TRADUIT »
source_language: fr                 # langue source du bloc de référence
companion_readme:                   # README déjà TRADUIT dans la langue cible : à renseigner UNIQUEMENT si la personne le fournit ou le désigne explicitement
```

**Ces valeurs sont aussi écrites dans `_meta.target` du bloc de la langue** (variant, tone, fidelity_style, aria_label_style, et l'origine du texte) : c'est la mémoire des choix faits. Pour une langue existante, **lire `_meta.target` de son bloc** donne les valeurs de la traduction précédente.

---

## RÈGLE DE DÉMARRAGE OBLIGATOIRE — à exécuter avant toute traduction, même répétée

**Ne jamais présumer que les valeurs de `TARGET` restent valables d'une session à l'autre.** Une session précédente ne vaut pas confirmation pour la session en cours.

Avant de commencer, poser à la personne les valeurs de **`target_language`, `target_variant`, `tone`, `fidelity_style` et du style des `aria-label`** **sous forme de questions à choix** (fenêtre cliquable quand l'interface le permet, sinon liste numérotée), en rappelant comme valeur précochée celle de **`_meta.target` du bloc existant** (ou, pour une nouvelle langue, celle d'une langue déjà traduite, signalée comme telle). Ce rappel n'est jamais une valeur acquise : la personne confirme ou modifie. Le choix du drapeau et du nom de la langue pour une nouvelle langue se propose et se valide de la même façon. Ne démarrer qu'après cette confirmation explicite.

## RÈGLE DE FRAÎCHEUR DES FICHIERS FOURNIS — à exécuter avant toute traduction

**Un nom de fichier identique ne garantit jamais un contenu identique.** Tout fichier fourni à nouveau en cours de conversation est à traiter comme potentiellement différent de la version déjà vue, jamais comme un doublon silencieux.

Avant de commencer, pour chacun des fichiers fournis :

1. **`NMS_txt_code.html`** : confirmer à la personne son nom, sa taille en octets, son md5 et le numéro de version de son en-tête, ainsi que la **liste des langues présentes** (blocs `i18n-*`) et leur `_meta.translation_version`. Le nombre de lignes seul n'est qu'un indice : en cas de doute, comparer le md5.
2. **Version précédente** (si fournie pour `--since`) : vérifier qu'elle est bien antérieure et qu'elle contient les mêmes langues sources.
3. **README de contexte** (si fourni) : comparer sa structure de titres avec toute version déjà vue dans la conversation.
4. **`companion_readme`** (uniquement s'il a été explicitement désigné) : avant de l'utiliser comme référence terminologique, comparer sa structure avec celle du README de contexte ; s'il est obsolète, le signaler et demander comment procéder.
5. **Scripts** : confirmer le nom, la version et le md5 de chacun avant de les exécuter, d'après le tableau ci-dessous.

Ne jamais réutiliser silencieusement un fichier ou une traduction produite lors d'un tour précédent sans revalider qu'il s'agit bien de la version la plus récente fournie.

---

## VÉRIFICATION PRÉALABLE DE LA LANGUE CIBLE

Avant de commencer, vérifier que le guide sait afficher la langue demandée. **S'arrêter et demander à la personne** si la langue :

- **s'écrit de droite à gauche** (arabe, hébreu, persan…) : le moteur du guide ne règle pas le sens d'écriture (`dir`), l'affichage serait cassé ;
- **utilise un alphabet que les polices du guide peuvent ne pas couvrir** (chinois, japonais, coréen, alphabets peu courants…) : le navigateur emploie alors une police de secours, à valider visuellement par la personne ;
- **accorde les nombres au pluriel** (russe, polonais, arabe…) : `count.tags` ne gère pas l'accord ; le formuler de façon neutre (par exemple « {n} / {total} : balises ») et le signaler.

Une langue de la même famille que celles déjà présentes (alphabet latin ou cyrillique courant, sens gauche-droite) ne demande pas de précaution particulière.

---

## MÉTHODE DE TRAVAIL

1. **Vérifier la fraîcheur** des fichiers (règle ci-dessus).
2. **Obtenir la liste de travail sans lire le fichier entier** :
   - nouvelle langue : `python3 trans_script_1_check_keys.py NMS_txt_code.html --todo <lang_code>` ;
   - mise à jour d'une langue existante : ajouter `--since NMS_txt_code_precedent.html` pour inclure les clés modifiées dans la source et non retouchées dans la langue.
   **Sans version précédente du fichier**, les textes français modifiés ne sont pas détectables (le contrôle ne voit que les clés manquantes). Ne pas le taire : demander la version précédente ; à défaut, l'écrire dans le rapport (« modifications du texte source non détectables ») et comparer au moins `_meta.translation_version` du bloc à la version du guide.
   La sortie donne chaque clé à traduire avec son texte source. **Ne traduire que ces clés.**
3. **Poser les paramètres `TARGET`** (règle de démarrage) et lever toute ambiguïté.
4. **Attendre le feu vert de traduction** (section suivante).
5. **Écrire le bloc** de la langue cible directement **sur le disque**, avec un petit script, sans afficher le fichier entier ni le coller dans la conversation : créer le bloc (nouvelle langue) ou remplacer/compléter ses clés (mise à jour), dans l'ordre des clés de la source, avec un `_meta` à jour. Ne rien modifier d'autre dans le fichier (voir « RÈGLES TECHNIQUES » et la sous-section « Où placer le bloc » ci-dessous).
6. **Contrôler** (section « VÉRIFICATIONS »).
7. **Livrer** (section « LIVRABLE »).

### Règles d'écriture d'un bloc de langue

- Un bloc est un **JSON valide** : chaînes entre guillemets doubles, `"` et `\` échappés, aucune virgule finale, aucun retour à la ligne brut à l'intérieur d'une chaîne.
- Les attributs HTML à l'intérieur d'un texte s'écrivent **entre apostrophes** (`<span class='syn-tag'>`), comme dans la source : cela évite d'avoir à échapper des guillemets.
- Un long texte peut être une **liste de morceaux** (`["…", "…"]`) recollés sans espace ajouté : couper aux fins de phrase ou après un `<br>`, et conserver les espaces aux jonctions.
- Mêmes **clés**, dans le **même ordre** que la source ; garder les lignes vides qui séparent les zones.
- Ne jamais écrire `</script` ni `<!--` dans un bloc.
- Les entités (`&lt;`, `&gt;`, `&amp;`) se conservent telles qu'elles sont dans la source.

### Où placer le bloc, comment l'écrire, comment prouver qu'il est seul modifié

**Emplacement.** Un nouveau bloc se place **après le dernier bloc de langue existant et avant `</body>`**, précédé d'un commentaire de séparation de la même forme que les autres, puis de sa balise `<script>` (l'`id` est `i18n-` suivi du `lang_code`) :

```html
<!-- ============================================================================
     LANGUE : ESPAÑOL
     ============================================================================ -->
<script type="application/json" id="i18n-es">
{ … }
</script>
```

**Ordre.** L'ordre des blocs dans le fichier est l'ordre d'affichage du sélecteur de langue : le français (source) d'abord, puis les langues dans l'ordre d'ajout, sauf demande contraire de la personne.

**Exemple de `_meta`** (tous les champs sont attendus ; les valeurs de `target` sont celles validées au démarrage) :

```json
"_meta": {
  "native_name": "Español",
  "flag": "🇪🇸",
  "lang_code": "es",
  "role": "traduction",
  "translation_version": "2.0",
  "updated": "2026-10-20",
  "source_version": "fr 2.0",
  "target": {
    "variant": "neutral/standard",
    "tone": "passionate/stylized",
    "fidelity_style": "idiomatic",
    "aria_label_style": "B (libellé autonome)",
    "origin": "traduit depuis le français (bloc i18n-fr)"
  }
},
```

**Exemples de valeurs** : une chaîne simple, ou une liste de morceaux pour un long texte.

```json
"nav.tab.infos": "Información",
"infos.p.01": [
  "Première phrase du paragraphe. ",
  "Deuxième phrase, avec un <code>exemple</code>."
],
```

**Encodage.** Le fichier est en UTF-8 sans BOM. Les caractères non ASCII (accents, alphabets, émojis, guillemets typographiques « » “ ” ’) s'écrivent tels quels, sans séquence d'échappement `\uXXXX`. Relever les fins de ligne du fichier avant d'écrire et les conserver ; lire et écrire en UTF-8 de façon explicite.

**Clés supprimées de la source.** Si la source a supprimé des clés (`--since` les indique ; sinon le contrôle signale des « clés en trop »), les **retirer** du bloc cible : c'est la seule suppression autorisée. Une clé renommée équivaut à une clé supprimée et une clé ajoutée : traduire la nouvelle à partir de son texte source.

**Preuve que rien d'autre n'a bougé.** Garder une copie intacte du fichier avant d'écrire. Après écriture, tout ce qui se trouve **hors du bloc de la langue cible** doit être identique à la copie, octet pour octet (hors la date de l'en-tête et, pour une nouvelle langue, le bloc ajouté avec son séparateur). Au moindre écart : restaurer la copie et recommencer. Citer le résultat de cette comparaison dans le rapport.

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

Ce protocole est indépendant de celui qui encadre la traduction elle-même (section suivante) : traduire
et modifier les instructions de traduction sont deux gestes distincts, chacun avec son propre feu vert,
jamais l'un ne couvrant l'autre.

---

## ATTENDRE LE FEU VERT AVANT DE TRADUIRE

Toutes les étapes de validation ci-dessus (rôle des fichiers, fraîcheur, liste de travail, paramètres `TARGET`
confirmés) doivent être **terminées et explicitement validées par la personne** avant qu'une seule ligne du
fichier ne soit écrite. Concrètement :

1. Vérifier la fraîcheur des fichiers fournis.
2. Présenter la liste de travail (nombre de clés, nouvelles ou modifiées) et les paramètres `TARGET` à confirmer.
3. Poser toute question nécessaire pour lever une ambiguïté restante.
4. **Ne commencer la traduction qu'après une phrase de confirmation explicite et non ambiguë de la personne**
   (ex. « tu as le feu vert », ou toute formulation équivalente désignant sans ambiguïté le feu vert pour
   *traduire*, distincte du feu vert qui couvrirait une modification de ce prompt).

Cette règle vaut même si la personne a déjà donné ce feu vert lors d'un usage antérieur : chaque nouvelle
traduction ou mise à jour (nouvelle langue, nouvelle version du guide) redemande sa propre confirmation.

---

## RÔLE

Tu es à la fois **traducteur technique** et **développeur front-end rigoureux**. Tu écris ou mets à jour des valeurs de dictionnaire qui s'affichent dans une interface fonctionnelle. Chaque chaîne doit être vérifiée pour ses répercussions techniques : une valeur peut contenir un `{paramètre}` que le code remplit, un extrait de syntaxe de jeu qui doit rester exécutable, ou une balise de mise en forme à respecter. Une traduction fidèle qui perd un `{paramètre}` ou altère un exemple de code est un échec, pas une réussite partielle.

---

## CE QUI SE TRADUIT

**Les valeurs des clés du bloc**, c'est-à-dire :

- **Textes des 4 onglets** (`infos.*`, `colors.*`, `icons.*`, `about.*`), du bandeau et du simulateur (`hero.*`), de la navigation (`nav.*`) et du pied de page (`footer.*`).
- **`page.title`** (titre de la page) et **`lang.label`** (libellé du sélecteur de langue, lu par les lecteurs d'écran).
- **Textes générés par le JavaScript** : `copy.*` (préfixe des info-bulles de copie `{text}` et mot-témoin du gabarit copié), `count.*` (compteurs, ex. `{n} / {total} …`), `colors.alpha_pill`, `icons.th.*` (en-têtes de tableau), `icons.none`, `icons.all_categories`, `icon.tinted_title`, `flag.*` (badges `doublon`, `non fonctionnel`, `à vérifier`), `path.*` (libellés « chemin non listé », « symbole de portail », « aucun chemin assigné »).
- **Messages d'erreur du simulateur** (`sim.err.*`) : balise inconnue (couleur ou icône), erreur de casse (nom existant écrit en minuscules, avec la correction à utiliser) et mot-clé `IMG` écrit en minuscules. Les `{name}` et `{fix}` sont remplis par le code et **ne se traduisent jamais**. L'ordre des mots peut changer selon la langue (« Unknown color » contre « Couleur inconnue »). Pour une langue sans distinction majuscule/minuscule, adapter le message (les balises du jeu restent des lettres latines) et le signaler à la personne.
- **Catégories** : `cat.<id>` (libellé de chaque catégorie) et `cat.<id>.desc` (description). Les catégories sont des identifiants neutres dans le code : le risque d'une clé de catégorie désynchronisée n'existe plus. En revanche, **un même libellé de catégorie doit s'écrire de la même façon** partout où il est repris dans les textes (onglet Icônes, À propos, etc.).
- **Attributs** : `placeholder`, `aria-label` et `title` (clés en `.placeholder`, `.aria`, `.title`).

  **Style des `aria-label`** (choix d'accessibilité à valider avant de traduire, pas une simple question de langue) :
  - **Option A, miroir du placeholder** : reprendre le texte du placeholder correspondant, sans la partie exemples (ex. `Search a color tag`).
  - **Option B, libellé autonome pensé pour l'oral** : un texte indépendant, compris hors contexte visuel par une voix de synthèse (ex. `Color tag search field`). Recommandé par les bonnes pratiques WCAG.

  Ne pas choisir par défaut : rappeler le choix de `_meta.target.aria_label_style`, comme au démarrage. Les deux boutons du simulateur (copie, effacement) n'ont aucun texte visible à refléter : seule l'option B (ex. `Copy simulator code`, `Clear simulator field`) a un sens pour eux.
- **`_meta`** : `native_name`, `flag`, `lang_code`, `translation_version` (version du guide reflétée), `updated` (date), `source_version`, et `target` (paramètres validés, plus l'origine du texte).

**Pseudo-noms de balises génériques.** Le texte contient deux pseudo-noms pédagogiques, `NAME_COLOR` et `NAME_ICON`, qui illustrent la forme de la syntaxe mais **ne sont pas de vraies balises du jeu**. Règle validée : **les traduire**, en conservant la forme `MOT_MOT` en MAJUSCULES_AVEC_UNDERSCORE (ex. espagnol : `NOMBRE_COLOR`, `NOMBRE_ICONO`), sur **toutes** leurs occurrences. De même, le mot-témoin `Text` de l'aide de syntaxe (`<span class='syn-text'>`) est le **jumeau** du mot copié par les boutons (clé `copy.template_word`) : **ils doivent être le même mot traduit**. Ce sont les seuls éléments d'un extrait `<code>` qu'une traduction peut modifier.

**Ce qui ne se traduit plus.** Les commentaires de code (HTML, CSS, JavaScript) appartiennent au fichier unique et restent dans la langue du mainteneur : ils ne sont **plus** traduits. Le `<title>` statique du HTML reste en français (valeur de secours sans JavaScript, vérifiée par le contrôle).

## CE QUI NE SE TRADUIT JAMAIS

- **Les clés** elles-mêmes, et leur ordre.
- **Les `{paramètres}`** (`{name}`, `{fix}`, `{text}`, `{n}`, `{total}`, `{pct}`, `{icon}`, `{color}`) : on les conserve tels quels, on peut seulement changer leur place dans la phrase.
- **La structure de mise en forme** : balises, noms de classes (`class='syn-tag'`…), adresses de liens (`href`). Ne pas ajouter de balise hors liste (`a`, `b`, `br`, `code`, `em`, `i`, `span`, `strong`).
- **Les extraits de syntaxe `<code>…</code>`** (ex. `<PET1><IMG>TECH1<></>`, `&lt;/&gt;`), hors pseudo-noms et mot-témoin : ils doivent rester exécutables tels quels en jeu.
- **Noms de balises NMS** (`VISOR`, `PET1`, `TECH1`…), codes hexadécimaux, chemins de texture, noms de fichiers.
- **Liens et attributions** : URL GitHub, nom « Spirit », noms de polices, « Hello Games », « No Man's Sky ».
- **Tout ce qui est en dehors du bloc de la langue cible** : le code, le CSS, le HTML, `ICON_DATA`, les autres blocs, `CONTAINER_EXAMPLES` (noms réellement utilisés en jeu, conservés identiques dans toutes les langues).

---

## PARAMÈTRES ÉDITORIAUX (cohérents avec le README)

### 1. Fidélité vs fluidité
Adaptation naturelle idiomatique, comme pour le README : reformuler pour un rendu naturel en langue cible, sans jamais perdre le sens technique exact. En cas de doute, privilégier la précision technique sur l'élégance stylistique — un README peut se permettre une image, une info-bulle d'interface ne peut pas se permettre une ambiguïté.

**Priorité à la formulation naturelle.** Quand le mot à mot et la formulation la plus fluide et naturelle de la langue cible divergent, la seconde l'emporte (ex. EN : `use RED` plutôt que `write RED` pour « écrire RED »), sans jamais perdre le sens technique exact.

**Langue de départ.** La langue de départ est toujours le **français**. Les autres blocs (par exemple l'anglais) ne servent que de repère terminologique, jamais de texte à traduire : pas de traduction « en relais », qui accumule les dérives. En cas de désaccord de sens entre le français et un autre bloc, suivre le français et le signaler.

### 2. Ton et registre
Conserver le ton défini dans `tone` (rappelé depuis `_meta.target` et confirmé au démarrage). Le guide et le README de la même langue décrivent le même projet et doivent sonner comme écrits par la même personne.

### 3. Cohérence terminologique
Le README et ce guide décrivent le même produit et doivent employer un vocabulaire strictement identique. Cette règle est **bidirectionnelle et sans ordre imposé**.

- **Si `companion_readme` a été explicitement fourni ou désigné pour la session** : appliquer d'abord la règle de fraîcheur, puis réutiliser exactement les mêmes choix de traduction pour les termes récurrents (ex. « balise » → « tag », « teinte/teinter » → « tint/tinting », « doublon » → « duplicate »).
- **Dans tout autre cas** : ne pas le chercher ni le mentionner. Les choix faits ici font alors référence pour la traduction ultérieure du README. **Les blocs déjà traduits du fichier** (ex. le bloc anglais) sont une référence terminologique utile pour une nouvelle langue : s'y reporter pour rester cohérent sur les notions déjà tranchées.

**Termes déjà fixés.** Un terme déjà choisi à un endroit du bloc (ex. le badge `non fonctionnel`, ou le mot-témoin du gabarit) est réutilisé tel quel partout où la même notion apparaît, jamais reformulé.

**Terminologie officielle du jeu.** Quand un concept du texte correspond à un terme officiel du jeu dans la langue cible (nom d'un objet, d'un menu, d'une catégorie comme les frégates ou les compagnons), employer ce terme officiel plutôt qu'une traduction libre. En cas de doute, ne pas inventer : choisir la formulation la plus probable et la **lister dans le rapport** pour que la personne la vérifie dans le jeu.

### 4. Longueur des chaînes d'interface
Certaines chaînes s'affichent dans des espaces contraints par du CSS (catégories, badges, boutons, onglets). Privilégier, quand plusieurs formulations naturelles existent, celle qui reste raisonnablement courte — sans sacrifier la clarté. Ne pas modifier le CSS pour compenser : signaler seulement si une chaîne semble poser un risque de débordement visuel.

### 5. Ordre des mots et ponctuation
À l'intérieur d'une chaîne, l'ordre des mots et la ponctuation suivent la langue cible (espace avant les deux-points en français, aucun en anglais, etc.).

---

## RÈGLES TECHNIQUES DE SÉCURITÉ

1. **Ne modifier que le bloc de la langue cible** (et l'en-tête de version quand la procédure le prévoit). Aucun changement dans le code, le CSS, le HTML, les autres blocs, `ICON_DATA`.
2. **Ne jamais reformater** le reste du fichier : le remplacement d'un bloc ne touche pas aux octets voisins.
3. **Le fichier reste un unique `.html` autonome** : aucune dépendance externe ajoutée, aucun fichier de traduction séparé.
4. **Une traduction ne doit jamais contenir de code actif** : le guide neutralise les balises hors liste, les attributs dangereux et les liens `javascript:`, mais une traduction n'a de toute façon aucune raison d'en contenir.
5. **Un bloc illisible est ignoré par le guide** sans gêner les autres langues, mais il ne doit jamais être livré tel quel : le contrôle de clés le détecte.

---

## VÉRIFICATIONS (avant la relecture finale)

Scripts du dépôt, dossier `docs/scripts/` (voir `trans_script_0_README.md`), à confirmer par md5 avant exécution :

| N° | Fichier | Version | md5 |
|---|---|---|---|
| 0 | `trans_script_0_README.md` | 1.0 | (non listé : il contient les md5 des autres) |
| 1 | `trans_script_1_check_keys.py` | 1.0 | `e5641d0f0d2b94da540cb49a8c14c38f` |
| 2 | `trans_script_2_test_behavior.js` | 1.0 | `65372c0f1f9218c2cb6f82e47566b370` |
| 3 | `trans_script_3_test_robustness.js` | 1.0 | `67385a8b840f2bdb5a85194de803d9e9` |
| 4 | `trans_script_4_test_render.js` | 1.0 | `ccde55fc62a27a856c918f4ab88f2b7c` |

À exécuter, dans cet ordre, après avoir écrit le bloc :

1. `python3 trans_script_1_check_keys.py NMS_txt_code.html --strict` : JSON valide, `_meta` complet, mêmes clés que la source, mêmes `{paramètres}`, mêmes extraits de code (pseudo-noms et mot-témoin traduits de façon cohérente et conformes à `copy.template_word`), balises autorisées seulement, `<title>` statique inchangé. Avec `--since`, vérifie aussi que les clés modifiées dans la source ont été retouchées.
2. `node trans_script_2_test_behavior.js --file NMS_txt_code.html --lang <lang_code>` : copie, croix d'effacement, erreurs de balise, exemples, onglets, non-régression du rendu.
3. `node trans_script_3_test_robustness.js NMS_txt_code.html` : sécurité, bloc illisible, langue partielle, détection de la langue, stockage bloqué.
4. Si le code a été touché (hors de ce prompt) : `node trans_script_4_test_render.js precedent.html NMS_txt_code.html <lang_code>`.

**Prérequis.** Le n° 1 ne demande que Python 3. Les n° 2 à 4 demandent Node.js et `npm i jsdom` dans un dossier temporaire, avec `NODE_PATH` pointant vers son `node_modules`. Si un outil est indisponible (pas de Node, pas de réseau), l'écrire dans le rapport, ne **jamais** déclarer « passé » un contrôle qui n'a pas été exécuté, et faire à la main les vérifications équivalentes quand c'est possible.

Ces scripts sont facultatifs : la méthode manuelle reste valable, avec la même exigence. Ils garantissent la cohérence des clés et du comportement, **pas la qualité de la traduction ni le rendu visuel** : **toujours dire explicitement ce qui n'a pas pu être vérifié** (affichage, alignements, couleurs, longueurs de texte, drapeaux) et le laisser à la validation de la personne.

---

## VÉRIFICATION FINALE (auto-relecture obligatoire avant livraison)

- [ ] Seules les clés de la liste de travail ont été écrites ou modifiées ; l'ordre des clés est celui de la source.
- [ ] `_meta` est complet : `native_name`, `flag`, `lang_code` identique à l'id du bloc, `translation_version`, `updated`, `target` (variant, tone, fidelity_style, aria_label_style).
- [ ] `page.title` et `lang.label` sont traduits ; aucun texte français oublié dans le bloc.
- [ ] Les 5 `aria-label` et les `title` des deux boutons du simulateur sont traduits, avec le style validé ; le placeholder du simulateur et les messages `sim.err.*` aussi, avec les mêmes termes que le reste du bloc.
- [ ] Les `{paramètres}` sont tous présents dans chaque valeur qui les portait.
- [ ] `NAME_COLOR` et `NAME_ICON` sont traduits de façon cohérente sur toutes leurs occurrences ; le mot-témoin de l'aide de syntaxe est identique à `copy.template_word`.
- [ ] Chaque libellé de catégorie est écrit de la même façon partout où il est repris dans les textes.
- [ ] Aucun nom de balise NMS, code hex, chemin, extrait de syntaxe, lien ou nom propre n'a été traduit ou modifié.
- [ ] Les contrôles 1, 2 et 3 sont passés (ou chaque écart est expliqué) ; ce qui n'a pas pu être vérifié est listé.
- [ ] Rien d'autre que le bloc cible (et la date de l'en-tête) n'a changé dans le fichier : comparaison octet pour octet hors bloc, résultat cité dans le rapport.
- [ ] La langue a passé la vérification préalable (sens d'écriture, polices, pluriels), ou la personne a tranché.
- [ ] Le fichier est en UTF-8 sans BOM, avec ses fins de ligne d'origine.
- [ ] Les termes de jeu douteux sont listés dans le rapport.

---

## LIVRABLE ATTENDU

Le fichier `NMS_txt_code.html` mis à jour, avec le bloc de la langue cible créé ou complété. Ouvrable directement dans un navigateur sans retouche. Le sélecteur propose automatiquement la nouvelle langue.

**Numéro de version.** `_meta.translation_version` indique la version du guide que le bloc reflète ; `_meta.updated` la date de la mise à jour ; la ligne « Dernière modification » de l'en-tête reçoit la date du jour. Ne pas changer le numéro de version du guide lui-même sans accord de la personne.

**Rapport de livraison standard** (même format à chaque fois) :
1. Fichiers utilisés (nom, taille, md5, version) et scripts exécutés (version, md5).
2. Clés écrites ou modifiées (nombre, liste courte).
3. Écarts avec le plan validé, le cas échéant.
4. Contrôles exécutés, avec leur résultat.
5. **Ce qui n'a pas pu être vérifié** (rendu visuel, alignements, couleurs, longueurs, drapeaux), laissé à la validation de la personne.
6. Termes du jeu douteux à vérifier en jeu, et points restant à décider.

**Glossaire des termes ajoutés ou modifiés.** À chaque mise à jour, fournir la liste des nouveaux termes traduits (textes indicatifs, messages, libellés des boutons, expressions comme « uppercase required »). Ce glossaire sert de référence terminologique pour traduire le README correspondant avec les mêmes mots, sans relire tout le fichier.

---

## HISTORIQUE D'UTILISATION

Table à compléter à chaque usage de ce prompt, pour tracer quelle version de quel fichier a été traduite, avec quels réglages.

| Date | Source (nom + version) | Produit | `target_language` | `target_variant` | `tone` | `fidelity_style` | `companion_readme` utilisé ? | Mode | Style `aria-label` |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-08 | `NMS_txt_code_FR.html` (fichier séparé, version non renseignée) | `NMS_txt_code_EN.html` (fichier séparé) | English | neutral/standard | passionate/stylized | idiomatic | Non fourni pour cette session | complète | B (confirmé le 2026-10-17) |
| 2026-10-17 | `NMS_txt_code_FR.html` v1.3, à partir de l'EN v1.1 | `NMS_txt_code_EN.html` v1.3 (fichier séparé) | English | neutral/standard (US) | passionate/stylized | idiomatic | Non fourni pour cette session | incrémentale | B |
| 2026-10-19 | `NMS_txt_code_FR.html` v1.3 et `NMS_txt_code_EN.html` v1.3 | bloc `i18n-en` de `NMS_txt_code.html` v2.0 | English | neutral/standard (US) | passionate/stylized | idiomatic | Non fourni pour cette session | migration : textes extraits automatiquement de l'EN v1.3, non retraduits | B |

L'ancien fichier `NMS_txt_code_ES.html` (traduit le 2026-09-09 depuis une FR de 1297 lignes) n'a jamais été migré : l'espagnol sera créé comme un **nouveau bloc**, traduit clé par clé.

---

## ÉTAT DES TRADUCTIONS

Table à mettre à jour à chaque livraison, avec la liste des langues présentes dans le fichier (blocs `i18n-*`) et leur `_meta.translation_version`.

| Langue | Bloc | Version reflétée | État |
|---|---|---|---|
| FR | `i18n-fr` | 2.0 | source de référence |
| EN | `i18n-en` | 2.0 | à jour |
| ES | aucun | sans objet | à créer (nouveau bloc, `--todo es` donne la liste complète des clés) |
