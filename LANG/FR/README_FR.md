# NMS // TEXT CODES — Guide Français

<!-- BADGES CENTRE -->
<p align="center">

  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" alt="License: CC BY-NC-SA 4.0">
  </a>
  
  <a href="https://github.com/Data-Spirit">
    <img src="https://img.shields.io/badge/Guide%20%3A-README_FR.md-blue?style=flat&logo=mdbook&logoColor=white&logoSize=auto&label=Guide%20%3A&labelColor=black&color=darkcyan" alt="Guide : USER">
  </a>
  
  <a href="https://github.com/Data-Spirit/NMS_TC">
    <img src="https://img.shields.io/badge/URL%20%3A-NMS_TC-blue?style=flat&logo=shieldsdotio&logoColor=white&logoSize=auto&label=Repo%20%3A&labelColor=grey&color=mediumseagreen" alt="Site">
  </a>
  
</p>

**Un guide interactif, autonome et exhaustif des codes de formatage de texte de No Man's Sky** — couleurs et icônes, entièrement documentés, testés, et rassemblés dans un unique fichier HTML.

`NMS_txt_code_FR.html` · ~312 Ko · aucune dépendance externe critique · fonctionne hors-ligne

---

## Sommaire

- [Pourquoi ce projet](#pourquoi-ce-projet)
- [Caractéristique principale : un fichier 100 % autonome](#caractéristique-principale--un-fichier-100--autonome)
- [Chiffres clés](#chiffres-clés)
- [Structure de l'interface](#structure-de-linterface)
  - [Onglet Infos](#-onglet-infos)
  - [Onglet Couleurs](#-onglet-couleurs)
  - [Onglet Icônes](#-onglet-icônes)
  - [Onglet À propos](#-onglet-à-propos)
- [Le simulateur en direct](#le-simulateur-en-direct)
- [La technique de teinte d'icône](#la-technique-de-teinte-dicône)
- [Copier-coller en un clic](#copier-coller-en-un-clic)
- [Identité visuelle : un design "méta"](#identité-visuelle--un-design-méta)
- [Comment les icônes ont été extraites et intégrées](#comment-les-icônes-ont-été-extraites-et-intégrées)
- [Fiabilité de l'information et limites connues](#fiabilité-de-linformation-et-limites-connues)
- [Compatibilité et accessibilité](#compatibilité-et-accessibilité)
- [Stack technique](#stack-technique)
- [Licence](#licence)

---

## Pourquoi ce projet

No Man's Sky permet de personnaliser les noms (bases, vaisseaux, frégates, multi-outils, coffres de stockage, systèmes stellaires…) grâce à un système de balises de texte — coloration et icônes — qui n'est **documenté nulle part officiellement** par Hello Games. L'information existe, mais elle est éparpillée : captures d'écran de tableaux de configuration internes, essais empiriques de joueurs sur les forums, guides communautaires partiels et parfois obsolètes.

**NMS_TC** compile, vérifie, corrige et présente cette information sous une forme unique, structurée et directement exploitable — pensé pour être consulté aussi bien comme documentation de référence que comme outil de travail pendant qu'on joue.

---

## Caractéristique principale : un fichier 100 % autonome

Le guide est livré sous la forme d'**un seul fichier `.html`**, sans dossier annexe requis pour fonctionner.

Concrètement, cela signifie :

- **Aucune installation.** On ouvre le fichier dans n'importe quel navigateur moderne, c'est tout.
- **Déplaçable et renommable librement.** Le fichier ne dépend d'aucun chemin relatif vers d'autres fichiers.
- **Fonctionne hors-ligne.** Toutes les données (couleurs, icônes, logique de tri, simulateur) sont embarquées directement dans le fichier — voir la section [Comment les icônes ont été extraites et intégrées](#comment-les-icônes-ont-été-extraites-et-intégrées) pour le détail technique de l'intégration des images.
- **Une seule dépendance externe non critique** : les polices (Google Fonts, via CDN — *Rajdhani*, *IBM Plex Sans*, *JetBrains Mono*). Sans connexion internet, le rendu bascule simplement sur les polices système par défaut du navigateur ; aucune fonctionnalité n'est perdue.

Ce choix de conception (tout embarquer plutôt que de dépendre d'un dossier d'assets externes) a un coût — un fichier plus lourd (~312 Ko) qu'une version avec images externes — mais il garantit qu'un seul fichier suffit toujours à tout faire fonctionner, ce qui correspond directement à l'usage visé : un outil qu'on partage, télécharge ou déplace sans jamais avoir à se soucier de fichiers manquants.

---

## Chiffres clés

| | |
|---|---|
| 🎨 Balises de couleur documentées | **59** |
| 🖼️ Balises d'icônes documentées | **145** |
| 📂 Catégories d'icônes | **12** |
| 🔁 Doublons de texture repérés | **21** |
| ⛔ Balises listées mais non fonctionnelles | **16** |
| ❔ Balises au chemin de texture non confirmé | **12** |
| 🖼️ Icônes intégrées en base64 dans le fichier | **145 / 145** |
| 📝 Exemples concrets d'utilisation réelle | **10** |

---

## Structure de l'interface

Le guide s'organise en **4 onglets**, pensés comme un parcours de lecture logique : on apprend la syntaxe avant de consulter les tables de référence.

### 📘 Onglet Infos

Le point d'entrée du guide. Il regroupe tout ce qu'il faut savoir pour utiliser les balises, sans avoir à fouiller :

- **Syntaxe complète**, avec coloration syntaxique dédiée (voir plus bas) distinguant clairement le nom de la balise, le texte libre de l'utilisateur, et les symboles structurels (`<`, `>`, `<>`, `</>`, `IMG`).
- **Technique avancée : teinter une icône avec une balise couleur** — explique qu'une balise couleur collée juste avant une balise `<IMG>` applique sa couleur sur l'icône comme un filtre, avec un encadré **Important** dédié à la seule vraie subtilité (où placer la balise de fermeture pour teindre l'icône seule ou l'icône *et* le texte qui suit), et un comparatif visuel des deux cas côte à côte.
- **Encadré d'avertissement** rappelant honnêtement que ce comportement est observé par la communauté mais non documenté officiellement, avec la liste des limites connues (icônes déjà colorées qui peuvent résister à la teinte, comportement non garanti à 100 %).
- **Encadré Astuce** sur la limite de caractères des champs de texte en jeu, avec recommandation de privilégier des balises courtes.
- **Section "Exemples concrets"** : dix intitulés réellement utilisés pour organiser des conteneurs de stockage en jeu, chacun affiché avec son rendu visuel en direct *et* son code brut coloré — la meilleure démonstration pratique de tout ce qui précède.

### 🎨 Onglet Couleurs

Une table de référence complète des 59 balises de couleur, avec :

- **Une pastille de couleur pleine largeur** par ligne (plutôt qu'un petit carré), avec un fond en damier pour visualiser correctement la transparence des couleurs qui en ont une.
- **Code hexadécimal exact** et **pourcentage de transparence** (affiché uniquement quand il est inférieur à 100 %, pour ne pas surcharger l'affichage inutilement).
- **Catégorie d'appartenance** de chaque balise (Transmissions/Missions, Ressources, Joueurs, Compagnons, Carte galactique, etc.), alignée à l'extrême droite de chaque ligne.
- **Un bandeau d'en-tête dédié**, visuellement distinct (fond et bordure propres, séparateurs verticaux entre colonnes) plutôt qu'un simple texte flottant au-dessus du tableau.
- **Quatre modes de tri cliquables** : par nom (alphabétique), par couleur (voir ci-dessous), par code hexadécimal (alphabétique), et par luminosité (du plus sombre au plus clair). Cliquer une seconde fois sur le même critère inverse l'ordre.
- **Une barre de recherche** qui filtre instantanément la liste par nom de balise.

**Le tri "Couleur" mérite une explication à part.** Après plusieurs itérations infructueuses avec des algorithmes de tri par teinte (HSL classique, puis teinte+luminosité, puis regroupement par familles perceptuelles avec seuils de proximité de teinte), il s'est avéré qu'aucune formule mathématique simple ne reproduisait fidèlement la perception humaine d'un dégradé "bien rangé" — deux couleurs à la même teinte exacte mais à saturation très différente (un bleu vif et un bleu délavé, par exemple) ne se classaient jamais de façon satisfaisante par un calcul automatique seul. La solution retenue a été **un ordre de référence classé manuellement**, couleur par couleur, à l'œil — plus fiable qu'un algorithme pour capturer des nuances comme la vivacité d'une couleur ou les neutres légèrement teintés (ivoire, blanc cassé) qui doivent se distinguer des gris parfaitement neutres.

### 🖼️ Onglet Icônes

Une table de référence complète des 145 balises d'icônes, groupées en **12 catégories** (Ressources, Interface, Frégates, Inventaire, Voix/Réseau, Butin, Plateformes/Contrôles, Symboles de portail, Classe (C→S), Modes de jeu, Édition de base, Non fonctionnel), avec pour chaque icône :

- Un **aperçu miniature réel** de l'icône (voir la section dédiée à l'extraction plus bas — ce ne sont pas des symboles génériques, mais les vraies icônes du jeu, détourées).
- Le **nom exact de la balise**.
- Le **chemin du fichier texture** d'origine (référence `.DDS` interne au jeu), quand il a pu être identifié.
- Un **badge d'état** le cas échéant : `doublon` (la balise pointe vers exactement la même texture qu'une autre, sous un nom différent), `non fonctionnel` (balise présente dans les données mais sans texture assignée — probablement un emplacement réservé côté développeurs) ou `à vérifier` (chemin de texture non confirmé dans les sources disponibles).

La catégorie **"Classe (C→S)"** illustre une correction de nommage volontaire : à l'origine appelée "Classes de vaisseaux", elle a été renommée avec une description en sous-texte précisant qu'il s'agit en réalité d'une notation de qualité générique du jeu (vaisseaux, multi-outils, frégates, armes, technologies) et non d'un système propre aux vaisseaux.

Comme pour l'onglet Couleurs, une **barre de recherche** et un **filtre par catégorie** permettent de naviguer rapidement dans la liste.

**Alignement des colonnes** : chaque tableau de catégorie utilise des largeurs de colonnes fixes et identiques (`table-layout: fixed`), la colonne "Balise" étant dimensionnée sur le nom de balise le plus long de tout le guide (`BULLETPOINT_OFF`, 15 caractères) — garantissant qu'aucun nom n'est jamais tronqué et que l'alignement reste rigoureusement identique d'une catégorie à l'autre, indépendamment de la longueur du titre de la catégorie ou du contenu de ses lignes.

### ℹ️ Onglet À propos

Le contexte et la transparence méthodologique du guide :

- Rappel que le système de balisage n'est pas documenté officiellement.
- Détail technique de la banque d'icônes (comment les 145 icônes sont intégrées, et où trouver les fichiers PNG individuels si besoin ailleurs).
- Liste explicite des doublons de texture repérés, avec exemples.
- Précision sur les symboles de portail (`PR_0` à `PR_15`) — confirmés fonctionnels en jeu par la communauté (utilisés pour renommer des systèmes stellaires avec le symbole de leur adresse de portail).
- Liste des balises non fonctionnelles listées dans les données mais sans texture assignée.
- Sources utilisées pour compiler le guide.

---

## Le simulateur en direct

Situé en haut de page, visible depuis n'importe quel onglet, le simulateur permet de **taper une combinaison de balises et d'en voir le rendu instantanément**, sans avoir à retourner en jeu pour vérifier :

- Reconnaît et affiche correctement les balises couleur, les balises icône, et leur combinaison (y compris la technique de teinte, voir ci-dessous).
- Les icônes affichées sont les vraies icônes extraites du jeu (pas des approximations).
- Utile pour composer un nom complexe (plusieurs balises combinées) et vérifier son rendu avant de le recopier en jeu.

---

## La technique de teinte d'icône

Le simulateur reproduit la technique consistant à placer une balise couleur juste avant une balise `<IMG>` pour teindre l'icône :

- Techniquement réalisée via un **masque CSS** (`mask-image`) : la couleur de la balise est appliquée comme fond, et le canal alpha du PNG de l'icône sert de pochoir — ce qui reproduit fidèlement le comportement observé en jeu (la couleur *remplace* les pixels de l'icône plutôt que de se fondre dessus).
- **Toutes les icônes ne sont pas teintées dans le simulateur.** Une analyse de saturation (complétée par une vérification visuelle manuelle) a permis d'identifier une vingtaine d'icônes qui possèdent déjà une couleur propre significative (badges de classe, icône PlayStation, diamants de joueurs en réseau, certaines icônes de ressources...). Par souci de lisibilité, celles-ci sont affichées avec leur couleur d'origine plutôt que d'être aplaties en silhouette — avec une note explicite précisant qu'en jeu, la teinte peut malgré tout s'y appliquer réellement et donner un résultat différent de l'aperçu.

---

## Copier-coller en un clic

Chaque ligne des tableaux Couleurs et Icônes dispose d'un petit bouton dédié (symbole ⧉), positionné à gauche de la ligne :

- **Couleurs** : copie un gabarit prêt à l'emploi, `<NOM_COULEUR>Texte</>`.
- **Icônes** : copie directement la syntaxe complète, `<IMG>NOM_ICONE<>`.
- **Retour visuel immédiat** : le bouton se transforme brièvement en coche (✓) pendant environ 1,4 seconde pour confirmer la copie.
- Repose sur l'API `navigator.clipboard`, avec un repli automatique (`document.execCommand`) pour les navigateurs plus anciens qui ne la supporteraient pas.

---

## Identité visuelle : un design "méta"

Choix de conception délibéré : plutôt que de définir une palette d'interface arbitraire, **les couleurs d'accent de l'interface elle-même sont directement empruntées aux vraies balises couleur du jeu** documentées dans le guide :

| Usage dans l'interface | Couleur | Balise NMS d'origine |
|---|---|---|
| Titres de section, onglet actif | Cyan | `VISOR` |
| Encart "Astuce", accents généraux | Orange | `COMMODITY` |
| Mise en valeur, texte souligné | Vert émeraude | *(teinte personnalisée, cohérente avec la famille verte du jeu)* |
| Encart "Important" | Violet | `SPECIAL` |
| Encart d'avertissement | Rouge | `TRANS_WAR` |

Ce choix crée une cohérence thématique directe entre le contenu documenté et le vocabulaire visuel utilisé pour le présenter — le guide "s'habille" littéralement avec les couleurs qu'il documente.

---

## Comment les icônes ont été extraites et intégrées

Les 145 icônes ne sont pas des symboles génériques : ce sont les **vraies icônes du jeu**, extraites individuellement de plusieurs captures d'écran (tableaux de configuration internes et captures d'interface en jeu), puis nettoyées et intégrées :

1. **Repérage des coordonnées.** Chaque icône a été localisée précisément (coordonnées en pixels) dans son image source, avec recalibrage manuel dans les cas où les grilles sources n'étaient pas parfaitement régulières.
2. **Détourage.** Le fond a été retiré par seuillage de distance de couleur (transformation en canal alpha), avec une isolation par composante connexe pour éliminer les fragments d'icônes voisines qui débordaient dans les captures où les icônes étaient très resserrées.
3. **Contrôle qualité manuel.** Plusieurs passes de vérification visuelle ont permis d'identifier et de corriger des icônes mal cadrées, décentrées, ou contaminées par un résidu de l'icône adjacente — jusqu'à obtenir un rendu propre sur l'ensemble des 145 icônes.
4. **Encodage.** Chaque PNG (fond transparent) est encodé en **base64** et stocké dans un objet JavaScript (`ICON_DATA`) associant chaque nom de fichier à une chaîne `data:image/png;base64,...`, utilisée directement comme attribut `src` des balises `<img>` — exactement comme si l'image était hébergée en ligne, sauf qu'elle est physiquement présente dans le fichier.

Cette approche explique à la fois le poids du fichier (~312 Ko, contre quelques dizaines de Ko pour une version texte seule) et sa portabilité totale : déplacer, renommer ou partager le fichier ne casse jamais l'affichage des icônes.

---

## Fiabilité de l'information et limites connues

Le guide s'efforce d'être honnête sur ce qui est confirmé et ce qui ne l'est pas :

- Le système de balisage **n'est documenté nulle part officiellement** par Hello Games — toutes les informations proviennent de tableaux de configuration internes du jeu, de tests en jeu et de sources communautaires.
- Les codes hexadécimaux des couleurs proviennent directement d'un tableau de valeurs RGBA/HEX exact — à une exception près (`TRANS_ANM`) dont la couleur exacte n'a pas pu être confirmée dans les sources les plus récentes.
- Les balises marquées `non fonctionnel` ou `à vérifier` sont clairement identifiées comme telles plutôt que d'être présentées avec la même certitude que le reste.
- La technique de teinte d'icône est présentée comme un comportement observé, pas une garantie universelle.

---

## Compatibilité et accessibilité

- **Responsive** : mise en page adaptée aux écrans étroits (colonnes secondaires masquées sur mobile dans le tableau des couleurs, défilement horizontal de sécurité sur les tableaux d'icônes).
- **Navigateurs modernes** : Chrome, Firefox, Edge, Safari — s'appuie sur CSS Grid, `mask-image` et l'API Clipboard, disponibles dans toutes les versions récentes.
- **Aucune donnée envoyée nulle part** : tout s'exécute localement dans le navigateur, aucune connexion réseau requise après le premier chargement des polices.

---

## Stack technique

- **HTML/CSS/JavaScript vanilla** — aucun framework, aucune dépendance de build, aucune étape de compilation.
- **Polices** : Rajdhani (titres), IBM Plex Sans (texte courant), JetBrains Mono (code), via Google Fonts CDN.
- **Aucune bibliothèque tierce** : le tri, la recherche, le filtrage, le simulateur et la coloration syntaxique sont tous du JavaScript natif écrit spécifiquement pour ce guide.

---

## Licence

Ce guide est distribué sous licence [**CC BY-NC-SA 4.0**](https://creativecommons.org/licenses/by-nc-sa/4.0/). Voir le fichier [`LICENSE.md`](../../LICENSE.md) à la racine du dépôt pour les termes complets.

No Man's Sky et tous les assets, marques et propriétés intellectuelles associés appartiennent à Hello Games et/ou leurs ayants droit respectifs. Ce guide est une ressource communautaire non officielle, sans lien avec Hello Games.
