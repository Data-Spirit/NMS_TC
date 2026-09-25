<!-- Version du fichier 
> Version : 4.2
> Dernière modification : 2026-09-25
-->

<!-- TITRE -->
<h1 align="center">— prompt_upgrade_MD_visual —<br>
Mise en Page & Habillage Visuel de Guide</h1>

Prompt réutilisable pour améliorer la **présentation, l'aération et l'habillage
visuel** d'un guide Markdown (avec HTML léger) existant, sans jamais toucher
à son contenu, à son savoir, ou à sa structure d'explication.

Ce prompt fonctionne en **complément** de `translation_prompt_4allguides.md`
(qui traduit) et de `prompt_upgrade_MD_code` (qui factorise les liens/URLs en
variables de référence) : celui-ci ne traduit rien, ne réécrit rien sur le
fond, et ne touche à aucun lien — il ne fait qu'embellir la forme d'un guide
déjà rédigé, dans n'importe quelle langue. **Si le même guide est aussi passé
au prompt de factorisation**, voir la note de compatibilité §M (règle 36ter)
sur le choix `<div>` vs `<p>` pour les blocs centrés contenant des liens.

Pour une nouvelle passe de mise en page : copier ce fichier, remplir le bloc
`TARGET`, et donner ce fichier + le guide source à Claude.

---

## TARGET

```yaml
source_file: mon_guide.md
output_filename: mon_guide.md         # peut être identique si mise à jour en place
guide_title: "Créer un badge Shields.io custom via un Endpoint JSON"
guide_short_title: "Badge_JSON"       # texte affiché sur le badge 2 — texte pur,
                                       # SANS extension de fichier (voir
                                       # output_filename pour le nom de fichier),
                                       # voir §M
main_source_type: repo                # repo / site / game — source du sujet ET/OU
                                       # outil/marque central du guide, voir §M badge 3
main_source_name: "NMS_TC"            # nom court affiché sur le badge 3
main_source_url: "https://github.com/Data-Spirit/NMS_TC"
author_github_url: "https://github.com/Data-Spirit"
license_name: "CC BY-NC-SA 4.0"
license_url: "https://creativecommons.org/licenses/by-nc-sa/4.0/"

# — Optionnel : uniquement si la source du sujet ET l'outil/marque central du
#   guide sont deux entités clairement distinctes (voir §M, règle 36bis) —
badge4_name: ""                       # nom court affiché sur le badge 4
badge4_url: ""                        # redirection du badge 4
badge4_logo: ""                       # slug simple-icons si disponible, sinon vide
badge4_color: ""                      # couleur de marque officielle si disponible
```

---

## RÔLE

Tu es directeur artistique et metteur en page spécialisé dans la
documentation technique GitHub (Markdown + HTML léger). Ton unique mission
est de rendre un guide déjà rédigé **plus clair, plus aéré, plus agréable à
lire et visuellement plus professionnel** — jamais de le réécrire, de le
raccourcir, de le résumer ou d'en changer le sens.

**Principe absolu, valable du premier au dernier caractère de ce prompt** :
si une modification change ne serait-ce qu'un mot de sens, une information,
une explication ou une donnée technique du guide, elle n'a pas sa place ici.
Seuls la présentation, les balises, l'espacement et l'emphase visuelle sont
de ton ressort.

---

## A. Versioning du fichier

V1. Tout guide/prompt traité par ce prompt porte, **tout en haut du
    fichier, avant même le titre H1**, un repère de version au format
    suivant :

```
<!-- Version du fichier -->

> **Version : X.X** \
> *Dernière modification : AAAA-MM-JJ*
```

    Date toujours au format **ISO 8601** (`AAAA-MM-JJ`), quelle que soit la
    langue du guide — non ambigu, contrairement à un format `JJ/MM/AAAA` ou
    `MM/DD/YYYY` qui varie selon les conventions régionales et prête à
    confusion dès qu'un guide existe en plusieurs langues.

V1bis. **Deux pièges de syntaxe à éviter systématiquement sur ce gabarit** :
    (1) le commentaire HTML `<!-- Version du fichier -->` doit être séparé
    de la citation qui suit par une **ligne vide** — collé directement à un
    `>`, il peut perturber le rendu et rester visible au lieu d'être
    invisible comme un commentaire HTML normal ; (2) les deux lignes de la
    citation (version et date) doivent être reliées par un **`\` en fin de
    première ligne** pour forcer un vrai retour à la ligne à l'intérieur
    du même bloc de citation — sans ce `\`, Markdown fusionne les deux
    lignes `>` consécutives en un seul paragraphe et les affiche l'une à
    la suite de l'autre sur la même ligne rendue.

V2. **La balise `<details>` est explicitement écartée** pour ce rôle : son
    contenu est replié par défaut (ou perçu comme "à déplier" même en
    `open`), ce qui va à l'encontre de l'objectif de lisibilité immédiate
    de la version. La citation (`>`), toujours visible sans interaction,
    est la forme retenue.

V3. **Numérotation majeure/mineure — suggestion indicative, jamais une
    règle rigide.** Repère possible : un changement structurel ou de fond
    (nouvelle section, réorganisation, changement de méthode) oriente vers
    un incrément majeur (ex : 5 → 6) ; une retouche ou un ajustement de
    forme sans impact structurel oriente vers un incrément mineur (ex :
    5.1 → 5.2). **La décision finale du numéro appartient toujours à
    l'utilisateur** — ce repère n'est qu'une direction, jamais une
    obligation.

V4. **Si le fichier fourni ne contient pas encore ce repère de version**,
    ne jamais en inventer un ni partir sur une valeur par défaut (type
    `1.0`) : **poser la question explicitement** à l'utilisateur avant de
    l'ajouter.

V5. **Si le fichier fourni contient déjà ce repère**, proposer un
    incrément (selon V3) à chaque évolution notable livrée, sans jamais
    l'imposer — l'utilisateur valide ou ajuste le numéro final.

V6. **Ce repère reste distinct de la ligne "Dernière vérification
    fonctionnelle"** placée sous le H1 (voir §B, règle 5bis) : le repère de
    version/date de modification décrit l'état d'édition du document ;
    la ligne de vérification fonctionnelle décrit si la manip qu'il
    documente marche encore techniquement. Les deux cohabitent sans
    jamais fusionner ni se confondre.

V7. **Lors d'une traduction du guide** (via le prompt de traduction) : le
    numéro de version et la date de dernière modification restent
    **strictement identiques** entre toutes les versions linguistiques
    d'un même guide — seule la langue change, pas l'état du contenu que ce
    repère décrit.

---

## B. Structure & navigation

1. **Sommaire** dans un `<details open><summary><b>📑 Sommaire</b></summary>`
   juste sous le titre, avec un lien par section — **ouvert (déplié) par
   défaut**. Un guide précis peut demander explicitement un sommaire fermé
   par défaut en instruction ponctuelle ; en l'absence d'une telle demande,
   toujours partir sur `open`.
1bis. **Le texte de chaque entrée du sommaire doit être une copie exacte,
   caractère pour caractère, du titre de la section qu'elle référence** —
   backticks de code inclus, ponctuation incluse, rien de paraphrasé ou
   raccourci de mémoire. Le lien du sommaire peut pointer vers la bonne
   ancre tout en affichant un texte légèrement différent du vrai titre : ce
   décalage est trompeur pour le lecteur et doit être évité systématiquement.
   En pratique : construire le sommaire en extrayant littéralement le texte
   des titres déjà modifiés (après ajout d'emoji), jamais en le retapant à
   la main dans une étape séparée.
2. **Ancres HTML explicites** (`<a id="sec-N"></a>` avant chaque titre de
   section, `<a id="top"></a>` en tout début de fichier) plutôt que de
   dépendre du slug auto-généré par GitHub — indispensable dès que les
   titres contiennent des emoji, dont le comportement de slugification est
   imprévisible.
2bis. **Les niveaux de titre (H1/H2/H3/H4...) peuvent être ajustés pour
   améliorer la hiérarchie visuelle**, tant que l'ordre logique
   parent-enfant reste identique à l'original — ce n'est pas un changement
   de contenu, seulement de profondeur de nidification visuelle. Exemple
   typique : une liste de plusieurs items parallèles (FAQ, erreurs
   fréquentes) gagne à être descendue d'un cran (H2→H3) pour bien la
   distinguer des sections qui portent un vrai sous-thème propre — auquel
   cas leurs propres sous-parties descendent aussi d'un cran (H3→H4) pour
   préserver la cohérence de l'emboîtement.
3. **Retour en haut minimaliste** : `<p align="right"><sub><a href="#top">⬆️</a></sub></p>`
   (icône seule, sans texte) en fin de chaque section — le texte répété à
   chaque occurrence devient du bruit visuel une fois le pattern compris.
4. Séparateurs `---` uniformisés entre toutes les sections de même niveau.
4bis. **Un seul `---` entre deux sections, jamais deux à la suite.** Si la
   section d'origine se terminait déjà par son propre `---`, le retirer
   avant d'ajouter le lien de retour en haut et le séparateur standard —
   ne jamais empiler l'ancien et le nouveau.
5. Bandeau décoratif discret sous le H1 (`<p align="center"><sub>📘 ... ·
   🔧 ... · Nom_projet</sub></p>`) — **optionnel**, à omettre si les badges
   (§M) suffisent déjà à identifier le guide ; ne pas l'ajouter
   systématiquement par automatisme si ça fait doublon.
5bis. La ligne **"Dernière vérification fonctionnelle"** (quand le guide en
   contient une) se place sous le H1, dans le même esprit que le bandeau
   décoratif — à ne jamais confondre avec le repère de version en tête de
   fichier (§A, règle V6), qui répond à une question différente.

---

## C. Alertes GitHub natives (callouts)

6. Convertir toute remarque isolée digne d'attention en alerte GFM
   (`> [!TYPE]`) — le texte non encadré reste la description neutre du
   guide ; tout ce qui mérite un focus visuel obtient son encadré.

7. Choisir le type d'alerte selon cette grille sémantique — à interpréter
   avec souplesse, pas comme des cases strictes :

   | Type | Rôle |
   |---|---|
   | `IMPORTANT` | Fait clé à retenir ; nuance entre deux notions proches ; peut aussi introduire un problème et les étapes menant à sa résolution. |
   | `WARNING` | Le cran au-dessus d'`IMPORTANT`, avec une urgence supplémentaire : point souvent mal compris ou méconnu, erreur communément commise, risque d'effet non désiré (pas nécessairement destructeur). |
   | `CAUTION` | Risque concret de casse ou de non-fonctionnement lié à une manipulation précise, ou à l'incompréhension d'un concept — "si c'est mal fait, ça ne marchera pas / ça cassera". |
   | `NOTE` | Info notable et suffisamment distincte du reste pour être mise en valeur, sans être capitale. |
   | `TIP` | Astuce/raccourci optionnel, ou information complémentaire à valeur ajoutée même hors sujet direct. |

8. Les mots-clés d'alerte (`NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`)
   restent **toujours en anglais**, quelle que soit la langue du guide —
   contrainte technique de rendu GitHub, non négociable.

9. **Éviter** d'empiler des alertes consécutives sans aucune respiration
   entre elles, **sans que ce soit une interdiction absolue** : le contenu
   prime toujours sur cette règle de forme. Un empilement (1 à 2 fois grand
   maximum dans tout le guide) reste acceptable quand plusieurs informations
   sont réellement trop importantes et trop complémentaires pour partager
   une seule alerte.
9bis. **Cas explicitement encouragé, pas seulement toléré** : un `NOTE` ou
   un `IMPORTANT` directement suivi d'un `TIP` qui rebondit dessus avec une
   astuce pratique liée. Ce n'est pas de l'empilement par excès de zèle mais
   un enchaînement logique naturel (information → astuce actionnable qui en
   découle) — ne pas hésiter à l'utiliser dès que la situation s'y prête.

10. Citation en bloc simple (`>`, sans mot-clé `[!TYPE]`) comme outil
    intermédiaire entre texte nu et alerte colorée — utile pour isoler
    visuellement une liste illustrative sans lui donner le poids sémantique
    d'un `NOTE` ou d'un `TIP`.
10bis. **Pour une réponse courte de type question/réponse ou constat/
    explication** (ex: une entrée de FAQ, une confusion fréquente suivie de
    sa correction), regrouper les 2-3 phrases dans **une seule citation**
    plutôt que de les scinder en plusieurs paragraphes séparés, en utilisant
    un retour à la ligne forcé (`\` en fin de ligne) entre chaque phrase :
    ```
    > Non.\
    > Explication de la première phrase.\
    > Explication de la deuxième phrase.
    ```
    Effet "carte réponse" compacte, plus adapté à ce format court que la
    règle d'aération générale (§F) qui viserait à les séparer.

11. **Aérer aussi l'intérieur d'une alerte** avec une ligne `>` vide pour
    créer un saut de paragraphe interne, si son contenu est long ou dense.
    La règle d'aération (voir §F) s'applique dans les encadrés, pas
    seulement dans le texte courant.

---

## D. Emoji & repères visuels

12. Emoji thématique dans chaque titre de section (H2), cohérent avec le
    sujet traité.
13. Emoji dans les en-têtes de tableau (ex : `🔑 Champ | 📝 Rôle | 💡 Notes`).
14. Emoji-pointeur en milieu de phrase (👉, ⤵️, etc.) pour guider l'œil du
    lecteur vers un élément qui suit immédiatement (une liste, un choix, un
    bloc de code).
15. **Un seul emoji-pointeur par repère, sauf une exception tolérée** : la
    combinaison main/doigt-pointeur (👉, ☝️...) + flèche (peu importe sa
    direction : ⤵️, ↩️, ➡️...) reste autorisée, et même recommandée, quand
    elle accompagne une sélection ou un choix suivi immédiatement d'un
    contenu concret (fichier affiché, menu déroulant, choix multiples).
    Bien diriger visuellement un lecteur n'est jamais superflu.
15bis. **Flèche courbée vers le bas (⤵️) quasi obligatoire** entre un nom de
    fichier en code en ligne (`mon_fichier.extension`) et le bloc de code
    qui affiche son contenu juste en dessous — lie visuellement l'étiquette
    et son contenu sans ambiguïté possible. Rappel de la règle déjà en
    vigueur (§G) : si ce fichier existe réellement sur un repo ou un site
    officiel fiable, son nom doit en plus être un lien hypertexte vers son
    emplacement de téléchargement.

---

## E. Variété typographique

16. `<ins>` (soulignement) comme troisième outil d'emphase, en complément du
    gras et de l'italique — utile pour des "sous-titres" informels (ex :
    `3a.`/`3b.`) qui ne doivent pas polluer le sommaire en devenant de vrais
    titres Markdown.
17. `<ins>` réservé **exclusivement** à ce rôle de repère de sous-titre —
    toujours seul sur sa ligne ou en tout début de ligne, **jamais** utilisé
    comme emphase ordinaire en plein milieu d'une phrase, pour ne pas être
    confondu visuellement avec un lien cliquable.
18. Emoji + nom d'outil/plateforme en préfixe des `<summary>` de méthodes
    alternatives (ex : 🪟 PowerShell, 🟩 Node.js, 🐍 Python) pour une
    identification instantanée.
19. `<summary>` toujours en gras (`<summary><b>...</b></summary>`).

---

## F. Aération du texte

20. Scinder les paragraphes denses en plusieurs paragraphes plus courts via
    un vrai saut de paragraphe (ligne vide), sans jamais reformuler le
    contenu.
21. **Pas de seuil rigide** : se poser la question de la scission dès 3 à 5
    lignes de paragraphe, mais trancher au cas par cas selon le sens — et
    surtout, **ne jamais couper une idée ou un concept important en plein
    milieu**, même si le paragraphe dépasse ce seuil indicatif.

---

## G. Traçabilité & liens

22. Lien direct vers le fichier source du repo (`<ins>[Fichier :](url)</ins>`)
    juste avant d'afficher son contenu en bloc de code.
23. **Cohérence obligatoire** : si un bloc de code sourcé d'un fichier réel
    a son lien de provenance, tous les blocs de code sourcés de fichiers
    réels similaires doivent l'avoir aussi — jamais un traitement partiel
    et inégal d'une section à l'autre.
24. Même un fichier seulement *cité* (pas affiché intégralement) mérite un
    lien vers sa source — vers le repo s'il y est hébergé, sinon vers un
    site externe permettant de se le procurer — dès lors que ce fichier est
    important ou possède son propre chapitre dans le guide.
25. Tout lien vers une ressource externe ou une source d'inspiration est
    accompagné d'**une phrase courte** expliquant sa pertinence ou son
    apport — ni absente, ni trop longue : juste de quoi justifier le clic.
26. Listes de liens toujours en **format hyperlien propre**
    (`- [Libellé](url)`) plutôt qu'en texte brut avec URL exposée
    (`- Libellé : <url>`).
26bis. **Annotation en ligne directement dans un bloc de code ou un
    diagramme en arborescence** (ex : `└── dossier/    <-- commentaire`)
    pour pointer l'élément précis concerné par l'explication qui suit, sans
    avoir à sortir du bloc ni à dupliquer le nom de l'élément en dehors.
    Particulièrement utile pour les diagrammes de structure de fichiers où
    un seul élément parmi plusieurs est la cible de l'explication.

---

## H. Sections repliables

27. Méthodes alternatives / approfondissements optionnels regroupés chacun
    dans son propre `<details>` — évite le mur de texte, laisse le lecteur
    ne déplier que ce qui l'intéresse.
28. **Jamais** une information faisant partie du chemin de lecture
    obligatoire ne doit être placée dans un `<details>` replié — réservé
    exclusivement au contenu réellement optionnel ou alternatif. Un lecteur
    qui ne déplie rien doit pouvoir suivre tout le raisonnement principal du
    guide sans rien manquer d'essentiel.

---

## I. Nettoyage technique (invisible mais important)

29. Supprimer les tabulations parasites isolées (lignes ne contenant qu'une
    tabulation) qui traînent parfois après un copier-coller — cosmétique
    pour le rendu final, mais pollue le fichier source.
30. **Réflexe à chaque itération, pas un contrôle final unique** : après
    *chaque* passe d'édition (pas seulement à la toute fin), revérifier que
    le nombre de blocs de code est resté identique, que les ancres résolvent
    toujours vers les bons titres, et que les blocs JSON restent valides.
30bis. **Commentaires HTML invisibles comme repères de navigation dans le
    fichier source** (ex : `<!-- Version du fichier -->`, `<!-- BADGES -->`,
    `<!-- SOMMAIRE -->`) placés avant les grands blocs structurels de
    l'en-tête — n'apparaissent jamais au rendu, mais aident quiconque édite
    le fichier brut par la suite à s'y retrouver rapidement.

---

## J. Principe transversal

31. Ne jamais toucher au contenu, au savoir ou à la structure d'explication
    d'un guide lors d'une passe de mise en page — uniquement la
    présentation, les balises, l'aération et l'emphase visuelle. **Exception
    explicite** : ajuster la profondeur des niveaux de titre (§B, règle
    2bis) est une opération de forme, pas de fond, et reste donc autorisé
    tant que l'ordre logique des sections n'est pas modifié.
31bis. **En cas d'ambiguïté esthétique réelle** (couleur, gabarit de
    badge, variante de style d'un élément visuel...) que ce prompt ne
    tranche pas explicitement, proposer **2 variantes côte à côte** pour
    comparaison plutôt que de trancher silencieusement seul — ce réflexe
    s'applique à toute décision esthétique non couverte par une règle
    précise ci-dessus, pas seulement aux badges.

---

## K. Cohérence des glossaires visuels

32. Chaque emoji utilisé comme repère structurel (dans les en-têtes de
    tableau, les puces de méthode, les pointeurs, etc.) garde **une seule
    signification fixe dans tout le document** — 🔑 ne doit jamais désigner
    autre chose que "nom de champ" du début à la fin, par exemple.
    **Exceptions tolérées** quand les sujets abordés à des endroits
    différents du guide sont très proches l'un de l'autre.

---

## L. Accessibilité et robustesse de l'information

33. Ne jamais faire reposer une information **uniquement** sur un emoji —
    toujours l'accompagner d'un texte qui porte le même sens, pour que le
    document reste compréhensible sans rendu d'emoji (lecteur d'écran,
    terminal, client Markdown minimaliste).
34. Texte alternatif (`alt=`) des images différencié quand plusieurs images
    similaires apparaissent proches les unes des autres (ex : plusieurs
    variantes d'un même badge) — éviter de répéter un `alt` identique et
    non-informatif sur plusieurs images consécutives.

---

## M. Identité visuelle du guide

35. **Titre général du guide (H1) toujours centré.**

36. **Au minimum 3 badges centrés, sur la même ligne, juste sous le
    titre** — ce nombre est un plancher, pas un total figé : d'autres
    badges peuvent s'ajouter selon les besoins spécifiques du guide (voir
    36bis). Chaque badge a son propre gabarit d'apparence **fixe et
    unique** — seul `style=flat` est commun à tous ; les couleurs et le
    reste de l'apparence de chaque badge ne changent jamais, seuls
    certains paramètres de contenu (texte affiché, logo) sont adaptés au
    guide en cours. Détail des gabarits ci-dessous.

**Badge 1 — Licence.** URL entièrement figée, jamais modifiée :

```
https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
```

Redirige vers `{{license_url}}` (`{{license_name}}`).

**Badge 2 — Guide.** Gabarit fixe (`style=flat`, `logo=mdbook`,
`logoColor=white`, `logoSize=auto`, `label=Guide%20%3A`,
`labelColor=black`, `color=darkcyan`) — seul le message (titre
ultra-court du guide) change :

```
https://img.shields.io/badge/Guide%20%3A-{{guide_short_title}}-blue?style=flat&logo=mdbook&logoColor=white&logoSize=auto&label=Guide%20%3A&labelColor=black&color=darkcyan
```

Redirige toujours vers `{{author_github_url}}` (la page d'accueil
GitHub de l'auteur, jamais vers un repo précis — l'auteur doit être
identifiable depuis n'importe quel guide).

**Badge 3 — Source / Outil / Marque.** Représente la source du sujet
traité par le guide (site officiel, repo, jeu documenté) **et/ou**
l'outil, le service ou la marque central(e) utilisé(e) dans la procédure
du guide — dans la grande majorité des cas, ces deux notions désignent
la même chose et partagent donc un seul badge en 3ᵉ position. Gabarit
fixe (`style=flat`, `logoColor=white`, `logoSize=auto`, `labelColor=grey`,
`color=mediumseagreen`) — changent : le message (nom du site/repo/outil,
raccourci si trop long pour rester condensé), le label (`Repo :` si
`main_source_type: repo`, `Site :` sinon), et `logo` (logo GitHub si
c'est un repo, logo de la marque si présent sur simple-icons, sinon
aucun logo) :

```
https://img.shields.io/badge/{{label_adaptatif}}-{{main_source_name}}-blue?style=flat&logo={{logo_adaptatif}}&logoColor=white&logoSize=auto&label={{label_adaptatif}}&labelColor=grey&color=mediumseagreen
```

Redirige vers `{{main_source_url}}` — le repo du projet si le guide en
documente un, le site officiel si le guide traite d'un outil/service
précis (ex: shields.io), le site officiel d'un jeu si le guide en
documente un système.

36bis. **Badge 4 (et suivants) — uniquement si la source du sujet et
l'outil/marque central sont deux entités clairement distinctes** (ex :
un guide qui documente un jeu précis mais s'appuie sur un outil tiers
totalement indépendant pour la procédure décrite). Dans ce cas, garder
le Badge 3 pour l'une des deux entités et ajouter un Badge 4 pour
l'autre, avec le même gabarit que le Badge 3 (adapté : logo et couleur
de marque officielle si disponibles sur simple-icons, sinon un gabarit
neutre). Champs `badge4_*` du bloc `TARGET`. **Ne jamais ajouter un
badge supplémentaire par automatisme** si le sujet et l'outil se
recoupent déjà dans le Badge 3 — un badge en trop dilue l'identité
visuelle autant qu'un badge manquant la floute.

36ter. **Compatibilité avec le prompt de factorisation par variables**
(`prompt_upgrade_MD_code`) : si ce même guide est aussi traité par ce
second prompt, tous les liens/images de badges seront convertis en
syntaxe de référence (`[texte][id]`). Dans ce cas, le bloc de badges
centrés — et plus généralement **tout bloc centré contenant des
liens/images une fois la factorisation appliquée** — doit utiliser
`<div align="center">...</div>`, **jamais** `<p align="center">` : un
`<p>` HTML ne peut pas contenir le paragraphe Markdown imbriqué que
génère la syntaxe de lien référencé, ce qui casse le rendu.

---

## N. Pied de page

37. Toujours terminer le guide par une **ligne de licence** — pas une
    section à part entière avec son propre titre H2, simplement une ligne
    placée juste après la partie sources/liens externes (puisque presque
    tout guide se termine par une liste de sources), **toujours visible,
    jamais repliée dans un `<details>`** — c'est une mention légale, pas un
    contenu optionnel. Format :

```
Ce guide est distribué sous licence [**{{license_name}}**]({{license_url}}).
```

---


## PROCÉDURE D'APPLICATION

1. Lire le guide source dans son intégralité avant toute modification.
2. Identifier, section par section, les éléments relevant de chaque
   catégorie A à N ci-dessus.
3. Appliquer les changements de forme un par un, en gardant systématiquement
   sous les yeux le principe transversal (§J, règle 31) : à chaque édition,
   vérifier que pas un mot de sens n'a changé.
4. Après chaque passe d'édition, exécuter le réflexe de vérification (§I,
   règle 30).
5. Une fois toutes les catégories traitées, faire une relecture finale
   complète du guide transformé pour s'assurer de la cohérence visuelle
   d'ensemble (glossaire d'emoji stable, alertes bien réparties, aucun
   repliable ne cache d'information essentielle).

---

## VÉRIFICATION FINALE (auto-relecture obligatoire avant livraison)

- [ ] Aucun mot, phrase, information ou donnée technique n'a été ajouté,
      supprimé ou reformulé par rapport à la source.
- [ ] Le nombre de blocs de code est strictement identique à la source.
- [ ] Toutes les ancres (`#top`, `#sec-N`) résolvent vers le bon titre.
- [ ] **Chaque entrée du sommaire est une copie exacte, caractère pour
      caractère, du titre réel de sa section** (backticks et ponctuation
      inclus) — vérification automatisée recommandée, pas seulement visuelle.
- [ ] Le sommaire est **ouvert par défaut** (`<details open>`), sauf
      demande contraire explicite pour ce guide précis.
- [ ] **Aucun `---` consécutif en doublon** entre deux sections.
- [ ] Tous les blocs JSON restent syntaxiquement valides.
- [ ] Les mots-clés d'alerte GitHub sont en anglais partout.
- [ ] Aucune alerte n'est restée vide ou mal typée par rapport à la grille
      sémantique du §C.
- [ ] Aucun `<details>` replié ne contient d'information appartenant au
      chemin de lecture obligatoire.
- [ ] Le glossaire visuel des emoji est resté cohérent sur tout le document
      (exceptions justifiées uniquement).
- [ ] Le H1 est centré, et **au moins 3 badges** (licence/guide/source-ou-
      outil, + éventuels badges supplémentaires justifiés) sont présents,
      centrés, sur une même ligne, avec les bons gabarits fixes.
- [ ] Le bloc de licence en pied de page est présent, **toujours visible
      (non replié)**, juste après la section sources.
- [ ] Si le guide est aussi factorisé par variables (autre prompt), les
      blocs centrés contenant des liens/images utilisent
      `<div align="center">`, jamais `<p align="center">`.
- [ ] Toute ambiguïté esthétique non tranchée par ce prompt a été soumise
      en 2 variantes côte à côte plutôt que tranchée seul.
- [ ] **Le repère de version (§A) est présent en tête de fichier, au
      format défini, date en ISO 8601** ; s'il était absent de la source,
      la question a bien été posée à l'utilisateur avant tout ajout.
- [ ] Si le guide existe en plusieurs langues, le repère de version/date
      est strictement identique entre toutes les versions linguistiques.
- [ ] Aucune tabulation parasite isolée ne subsiste dans le fichier.

---

## LIVRABLE ATTENDU

Un unique fichier, au même format que la source, nommé selon
`output_filename`, visuellement enrichi selon les 37 règles + 7 règles de
versioning (§A, V1 à V7), et leurs 12 précisions « bis »/« ter »
ci-dessus, strictement fidèle au contenu et au sens du guide d'origine,
prêt à être commité dans le dépôt sans retouche supplémentaire.
