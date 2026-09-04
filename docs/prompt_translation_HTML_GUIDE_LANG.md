# Translation Prompt — NMS_TC HTML Guide

Prompt réutilisable pour traduire le fichier `NMS_txt_code_<LANG>.html` (le guide interactif autonome) dans une nouvelle langue.
Pour une nouvelle traduction : copier ce fichier, changer uniquement le bloc `TARGET`, et donner ce fichier + le `NMS_txt_code_FR.html` source à Claude.

Ce prompt est le pendant technique de `translation_prompt_README_LANG.md`. Les deux partagent la même exigence de qualité et la même terminologie (voir §6 Cohérence terminologique), mais celui-ci s'applique à un fichier **HTML/CSS/JS fonctionnel**, pas à un texte pur : une erreur ici peut casser une fonctionnalité, pas seulement une phrase.

---

## TARGET

```yaml
target_language: English            # ex: English, Deutsch, Español, 日本語
target_variant: neutral/standard    # ex: US, UK, neutral/standard, none
lang_code: EN                       # code à 2 lettres majuscules — DOIT être identique à celui utilisé pour le README correspondant
output_filename: NMS_txt_code_EN.html   # convention : NMS_txt_code_<lang_code>.html
source_file: NMS_txt_code_FR.html
html_lang_attribute: en             # code ISO 639-1 minuscule pour l'attribut <html lang="...">
```

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
- Attribut `lang` de la balise `<html>` → utiliser `html_lang_attribute` défini dans `TARGET`.

### B. Texte généré dynamiquement en JavaScript (chaînes littérales dans le code)
Ces chaînes n'apparaissent pas comme texte HTML statique mais sont injectées au rendu — elles doivent être traduites avec la même rigueur que le texte visible :
- Libellés de badges de statut : `doublon`, `non fonctionnel`, `à vérifier`.
- En-têtes de tableau générés en JS : `Aperçu`, `Balise`, `Chemin texture`.
- Option par défaut du filtre catégorie : `Toutes catégories`.
- Message d'absence de résultat : `Aucun résultat.`
- Compteurs dynamiques : le suffixe `' balises'` (dans `rows.length + ' / ' + COLORS.length + ' balises'` et son équivalent pour les icônes).
- Pastille de transparence : `transparence ${...}%`.
- Gabarit de texte copié pour les couleurs : `Texte` dans `` `<${tag}>Texte</>` `` (c'est un exemple de texte que l'utilisateur va coller puis remplacer en jeu — traduire ce mot-témoin, ex. `Text` en anglais).
- Préfixe des tooltips de copie : `Copier : ${...}` → traduire uniquement `Copier :`, jamais le contenu de `${...}` (qui est un fragment de code de balise).
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

### D. Commentaires de code JavaScript/CSS
Traduire l'intégralité des commentaires (`//` et `/* */`) pour livrer un fichier source cohérent, entièrement en langue cible — y compris les commentaires de section (`/* ==== DATA ==== */` reste tel quel s'il est déjà en anglais générique, mais les commentaires en français comme `// Ordre de référence défini manuellement...` doivent être traduits).

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

### 3. Cohérence terminologique avec le README déjà traduit
**Avant de traduire, relire le `README_<lang_code>.md` déjà produit pour cette langue** et réutiliser exactement les mêmes choix de traduction pour les termes récurrents du projet (ex. si « balise » a été traduit par « tag » dans le README, utiliser « tag » partout ici aussi ; idem pour « teinte/teinter » → « tint/tinting », « doublon » → « duplicate », etc.). Les deux fichiers sont deux faces du même projet et doivent utiliser un vocabulaire identique.

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
- [ ] Chaque nom de catégorie a été traduit **à l'identique partout** où il apparaît (tableaux `COLORS`/`ICONS`, commentaires de section, et surtout la clé de `CATEGORY_DESCRIPTIONS`) — vérifier caractère par caractère, en particulier les espaces autour de `/` et la flèche `→`.
- [ ] Aucun nom de balise NMS, chemin `.DDS`, code hex, nom de fichier PNG, ID HTML, classe CSS, nom de variable/fonction JS n'a été traduit ou modifié.
- [ ] Les 10 entrées de `CONTAINER_EXAMPLES` sont restées strictement identiques à la source.
- [ ] Tous les commentaires de code sont traduits (§D).
- [ ] La terminologie utilisée correspond à celle du `README_<lang_code>.md` déjà livré pour cette langue.
- [ ] Aucune balise HTML, accolade JS ou guillemet n'a été cassé par une chaîne traduite mal échappée — relire spécifiquement les lignes où une traduction contient une apostrophe.
- [ ] Le fichier reste un unique `.html` autonome, structurellement identique à la source (aucune section ajoutée/supprimée/déplacée).

---

## LIVRABLE ATTENDU

Un unique fichier `.html` nommé selon `output_filename`, fonctionnellement identique au fichier source (même simulateur, mêmes tris, mêmes filtres, mêmes tableaux, mêmes 145 icônes intégrées), avec l'intégralité du texte visible et des chaînes de code traduites en langue cible, prêt à être ouvert directement dans un navigateur sans aucune retouche supplémentaire.
