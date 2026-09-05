# Upgrade Prompt — Mise en Page & Habillage Visuel de Guide

Prompt réutilisable pour améliorer la **présentation, l'aération et l'habillage
visuel** d'un guide Markdown (avec HTML léger) existant, sans jamais toucher
à son contenu, à son savoir, ou à sa structure d'explication.

Ce prompt fonctionne en **complément** de `translation_prompt_4allguides.md`
(qui traduit) et des prompts spécifiques du projet (qui traduisent aussi) :
celui-ci ne traduit rien et ne réécrit rien sur le fond — il ne fait
qu'embellir la forme d'un guide déjà rédigé, dans n'importe quelle langue.

Pour une nouvelle passe de mise en page : copier ce fichier, remplir le bloc
`TARGET`, et donner ce fichier + le guide source à Claude.

---

## TARGET

```yaml
source_file: mon_guide.md
output_filename: mon_guide.md         # peut être identique si mise à jour en place
guide_title: "Créer un badge Shields.io custom via un Endpoint JSON"
guide_short_title: "Badge_JSON"       # titre ultra-court pour le badge 2, voir §L
main_source_type: repo                # repo / site / game — voir §L, badge 3
main_source_name: "NMS_TC"            # nom court affiché sur le badge 3
main_source_url: "https://github.com/Data-Spirit/NMS_TC"
author_github_url: "https://github.com/Data-Spirit"
license_name: "CC BY-NC-SA 4.0"
license_url: "https://creativecommons.org/licenses/by-nc-sa/4.0/"
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

## A. Structure & navigation

1. **Sommaire replié** dans un `<details><summary><b>📑 Sommaire</b></summary>`
   juste sous le titre, avec un lien par section.
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
   🔧 ... · Nom_projet</sub></p>`) — **optionnel**, à omettre si les 3
   badges (§L) suffisent déjà à identifier le guide ; ne pas l'ajouter
   systématiquement par automatisme si ça fait doublon.

---

## B. Alertes GitHub natives (callouts)

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
    règle d'aération générale (§E) qui viserait à les séparer.

11. **Aérer aussi l'intérieur d'une alerte** avec une ligne `>` vide pour
    créer un saut de paragraphe interne, si son contenu est long ou dense.
    La règle d'aération (voir §E) s'applique dans les encadrés, pas
    seulement dans le texte courant.

---

## C. Emoji & repères visuels

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
    vigueur (§F) : si ce fichier existe réellement sur un repo ou un site
    officiel fiable, son nom doit en plus être un lien hypertexte vers son
    emplacement de téléchargement.

---

## D. Variété typographique

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

## E. Aération du texte

20. Scinder les paragraphes denses en plusieurs paragraphes plus courts via
    un vrai saut de paragraphe (ligne vide), sans jamais reformuler le
    contenu.
21. **Pas de seuil rigide** : se poser la question de la scission dès 3 à 5
    lignes de paragraphe, mais trancher au cas par cas selon le sens — et
    surtout, **ne jamais couper une idée ou un concept important en plein
    milieu**, même si le paragraphe dépasse ce seuil indicatif.

---

## F. Traçabilité & liens

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

## G. Sections repliables

27. Méthodes alternatives / approfondissements optionnels regroupés chacun
    dans son propre `<details>` — évite le mur de texte, laisse le lecteur
    ne déplier que ce qui l'intéresse.
28. **Jamais** une information faisant partie du chemin de lecture
    obligatoire ne doit être placée dans un `<details>` replié — réservé
    exclusivement au contenu réellement optionnel ou alternatif. Un lecteur
    qui ne déplie rien doit pouvoir suivre tout le raisonnement principal du
    guide sans rien manquer d'essentiel.

---

## H. Nettoyage technique (invisible mais important)

29. Supprimer les tabulations parasites isolées (lignes ne contenant qu'une
    tabulation) qui traînent parfois après un copier-coller — cosmétique
    pour le rendu final, mais pollue le fichier source.
30. **Réflexe à chaque itération, pas un contrôle final unique** : après
    *chaque* passe d'édition (pas seulement à la toute fin), revérifier que
    le nombre de blocs de code est resté identique, que les ancres résolvent
    toujours vers les bons titres, et que les blocs JSON restent valides.
30bis. **Commentaires HTML invisibles comme repères de navigation dans le
    fichier source** (ex : `<!-- TITRE DU GUIDE -->`, `<!-- BADGES -->`,
    `<!-- SOMMAIRE -->`) placés avant les grands blocs structurels de
    l'en-tête — n'apparaissent jamais au rendu, mais aident quiconque édite
    le fichier brut par la suite à s'y retrouver rapidement.

---

## I. Principe transversal

31. Ne jamais toucher au contenu, au savoir ou à la structure d'explication
    d'un guide lors d'une passe de mise en page — uniquement la
    présentation, les balises, l'aération et l'emphase visuelle. **Exception
    explicite** : ajuster la profondeur des niveaux de titre (§A, règle
    2bis) est une opération de forme, pas de fond, et reste donc autorisé
    tant que l'ordre logique des sections n'est pas modifié.

---

## J. Cohérence des glossaires visuels

32. Chaque emoji utilisé comme repère structurel (dans les en-têtes de
    tableau, les puces de méthode, les pointeurs, etc.) garde **une seule
    signification fixe dans tout le document** — 🔑 ne doit jamais désigner
    autre chose que "nom de champ" du début à la fin, par exemple.
    **Exceptions tolérées** quand les sujets abordés à des endroits
    différents du guide sont très proches l'un de l'autre.

---

## K. Accessibilité et robustesse de l'information

33. Ne jamais faire reposer une information **uniquement** sur un emoji —
    toujours l'accompagner d'un texte qui porte le même sens, pour que le
    document reste compréhensible sans rendu d'emoji (lecteur d'écran,
    terminal, client Markdown minimaliste).
34. Texte alternatif (`alt=`) des images différencié quand plusieurs images
    similaires apparaissent proches les unes des autres (ex : plusieurs
    variantes d'un même badge) — éviter de répéter un `alt` identique et
    non-informatif sur plusieurs images consécutives.

---

## L. Identité visuelle du guide

35. **Titre général du guide (H1) toujours centré.**

36. **Toujours 3 badges centrés, sur la même ligne, juste sous le titre**,
    chacun avec son propre gabarit d'apparence **fixe et unique** — seul
    `style=flat` est commun aux trois ; les couleurs et le reste de
    l'apparence de chaque badge ne changent jamais, seuls certains
    paramètres de contenu (texte affiché, logo) sont adaptés au guide en
    cours. Détail des 3 gabarits ci-dessous.

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

**Badge 3 — Source principale.** Gabarit fixe (`style=flat`,
`logoColor=white`, `logoSize=auto`, `labelColor=grey`,
`color=mediumseagreen`) — changent : le message (nom du site/repo,
raccourci si trop long pour rester condensé), le label (`Repo :` si
`main_source_type: repo`, `Site :` sinon), et `namedLogo` (logo GitHub
si c'est un repo, logo de la marque si présent sur simple-icons, sinon
aucun logo) :

```
https://img.shields.io/badge/URL%20%3A-{{main_source_name}}-blue?style=flat&logo={{logo_adaptatif}}&logoColor=white&logoSize=auto&label=Repo%20%3A&labelColor=grey&color=mediumseagreen
```

Redirige vers `{{main_source_url}}` — le repo du projet si le guide en
documente un, le site officiel si le guide traite d'un outil/service
précis (ex: shields.io), le site officiel d'un jeu si le guide en
documente un système.

---

## M. Pied de page

37. Toujours terminer le guide par une **ligne de licence** — pas une
    section à part entière avec son propre titre H2, simplement un bloc
    replié placé juste après la partie sources/liens externes (puisque
    presque tout guide se termine par une liste de sources). Format :

```html
<details><summary><b>Licence :</b></summary>

Ce guide est distribué sous licence [**{{license_name}}**]({{license_url}}).

</details>
```

---


## PROCÉDURE D'APPLICATION

1. Lire le guide source dans son intégralité avant toute modification.
2. Identifier, section par section, les éléments relevant de chaque
   catégorie A à M ci-dessus.
3. Appliquer les changements de forme un par un, en gardant systématiquement
   sous les yeux le principe transversal (§I, règle 31) : à chaque édition,
   vérifier que pas un mot de sens n'a changé.
4. Après chaque passe d'édition, exécuter le réflexe de vérification (§H,
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
- [ ] **Aucun `---` consécutif en doublon** entre deux sections.
- [ ] Tous les blocs JSON restent syntaxiquement valides.
- [ ] Les mots-clés d'alerte GitHub sont en anglais partout.
- [ ] Aucune alerte n'est restée vide ou mal typée par rapport à la grille
      sémantique du §B.
- [ ] Aucun `<details>` replié ne contient d'information appartenant au
      chemin de lecture obligatoire.
- [ ] Le glossaire visuel des emoji est resté cohérent sur tout le document
      (exceptions justifiées uniquement).
- [ ] Le H1 est centré, et les 3 badges (licence/guide/source) sont présents,
      centrés, sur une même ligne, avec les bons gabarits fixes.
- [ ] Le bloc de licence en pied de page est présent, replié, juste après la
      section sources.
- [ ] Aucune tabulation parasite isolée ne subsiste dans le fichier.

---

## LIVRABLE ATTENDU

Un unique fichier, au même format que la source, nommé selon
`output_filename`, visuellement enrichi selon les 37 règles (+ 8 précisions
« bis ») ci-dessus, strictement fidèle au contenu et au sens du guide
d'origine, prêt à être commité dans le dépôt sans retouche supplémentaire.
