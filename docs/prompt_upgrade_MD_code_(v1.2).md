# prompt_upgrade_md_v1.2 — Factorisation de fichiers Markdown par variables de référence

## Objectif de ce prompt

Ce prompt sert de référence méthodologique pour appliquer, à n'importe quel fichier `.md` du projet (README principal, README de langue, documentation, etc.), la même technique de factorisation par variables déjà validée et testée sur le `README.md` racine de NMS_TC, puis affinée sur le cas `UiP_logo` (v1.2).

**Principe fondamental** : le rendu visuel final du fichier factorisé doit être **strictement identique** au rendu du fichier avant factorisation. La factorisation ne change jamais l'apparence — elle change uniquement la maintenabilité du code source.

**Méthode de travail obligatoire** : proposition → feu vert → exécution. Avant toute modification d'un fichier, lister précisément les changements envisagés, attendre une validation explicite ("tu as le feu vert" ou équivalent), et ne jamais enchaîner plusieurs modifications sans revalidation intermédiaire si elles sont distinctes.

---

## 0. Prérequis : identifier la syntaxe existante avant de factoriser *(ajouté en v1.2)*

La technique de ce prompt repose entièrement sur les références Markdown (`[texte][ref]`, `![alt][ref]`). Cette substitution est une fonctionnalité **du parseur Markdown** : elle ne fonctionne jamais à l'intérieur d'un attribut HTML brut (`href="..."`, `src="..."`).

**Avant toute proposition de factorisation**, identifier pour chaque lien/image sa syntaxe actuelle :
- **Markdown natif** (`[texte](url)`, `![alt](url)`) → factorisable directement.
- **HTML brut** (`<a href="...">`, `<img src="...">`) → doit d'abord être **converti** en syntaxe Markdown équivalente (`[![alt][badge_x]][ref]`, `![alt][ref]`) avant de pouvoir être factorisé.

Cette conversion de syntaxe fait partie intégrante du travail de factorisation, mais elle touche à la **structure** du code source (pas seulement aux valeurs) : elle doit donc être explicitement signalée dans la proposition, avant exécution, et non appliquée silencieusement.

---

## 1. Principe général : les liens de référence Markdown

Le Markdown standard (CommonMark) permet de remplacer une URL écrite en dur par une variable, définie une seule fois en bas du fichier :

```markdown
Voici [un lien][ma_variable] dans le texte.

[ma_variable]: https://exemple.com
```

Le même principe s'applique aux images :
```markdown
![Texte alternatif][ma_variable_image]

[ma_variable_image]: https://exemple.com/image.png
```

Et aux images cliquables (image + lien) :
```markdown
[![Texte alternatif][ma_variable_image]][ma_variable_lien]
```

**Avantage recherché** : si une URL change (nouvelle version de release, nouveau lien de mod, etc.), il suffit de modifier la variable une seule fois en bas du fichier, sans toucher au corps du document, même si cette URL est utilisée à plusieurs endroits.

---

## 2. Convention de nommage des variables

Une convention cohérente doit être respectée **dans tous les fichiers du projet**, pour que n'importe quel fichier factorisé se lise de la même manière.

| Préfixe | Usage | Exemples |
|---|---|---|
| `url_` | Liens vers des services externes, hors GitHub (CreativeCommons, NexusMods, etc.) | `url_license`, `url_nexusmods` |
| `github_` | Tout ce qui touche à un espace GitHub : repo (le nôtre ou celui d'un autre projet), releases, profils utilisateurs, **et fichiers locaux du repo** (ex. LICENSE.md) | `github_repo`, `github_release`, `github_license`, `github_user`, `github_banner` |
| `badge_` | Exclusivement les images de badges shields.io (le visuel, pas la cible du clic) | `badge_license`, `badge_status`, `badge_nexusmods` |
| `readme_` | Liens vers les fichiers README d'autres langues/dossiers | `readme_en`, `readme_fr`, `readme_es` |
| `guide_` | Liens vers les guides en ligne (GitHub Pages) par langue | `guide_en`, `guide_fr`, `guide_es` |
| `download_` | Liens de téléchargement direct, généralement uniques par langue/fichier | `download_en`, `download_fr`, `download_es` |
| `icon_` | Icônes/images partagées et réutilisées à plusieurs endroits | `icon_download` |

**Règles strictes à respecter :**
- Toujours en **minuscules**, y compris les suffixes de langue (`_en`, `_fr`, `_es`) — ne jamais faire `_EN`, `_FR`, `_ES`. Cette erreur a été commise puis corrigée en cours de route ; elle casse la cohérence avec le reste des variables du fichier.
- Utiliser des **underscores** (`_`), jamais de tirets (`-`), pour séparer les mots dans un nom de variable.
- Une variable peut être créée **même si elle n'est pas encore utilisée** dans le corps du texte, en réserve pour un usage futur (ex. `github_user` prévu avant d'avoir un usage concret). Ce n'est pas un problème tant qu'elle est bien rangée et commentée avec les autres.
- Une variable qui **n'est plus utilisée activement** (parce qu'un test a montré qu'elle cassait le rendu à un endroit précis) doit être conservée en mémo, accompagnée d'un commentaire expliquant pourquoi elle est inactive et où elle pourrait resservir. Ne pas la supprimer arbitrairement si elle a un intérêt de documentation ou de réutilisation future.
- **Une variable représente une cible (URL), pas un élément visuel.** *(ajouté en v1.2)* Si plusieurs badges ou éléments visuels différents pointent vers la même cible (ex. deux badges distincts qui renvoient tous les deux vers la page du repo), ils partagent la même variable `github_x` / `url_x` — on ne crée pas une variable par badge, mais une variable par destination réelle du clic.
- **Fusion des variables sémantiquement identiques.** *(ajouté en v1.2)* Si plusieurs URLs distinctes servent la même intention fonctionnelle (ex. « toujours pointer vers la dernière release », que ce soit exprimé via `/releases` ou `/releases/latest`), les fusionner sous une **seule** variable nommée d'après l'intention plutôt que la forme littérale de l'URL, et choisir comme valeur la cible la plus précise/dynamique parmi les candidates (ici, `/releases/latest`).

**Règle de priorité entre préfixes (en cas d'ambiguïté)**

Certaines URL pourraient sembler correspondre à plusieurs préfixes à la fois — par exemple, un lien de téléchargement direct pointe techniquement vers `github.com/.../releases/download/...`, donc il pourrait sembler relever de `github_`. Dans ce genre de cas :

**Une catégorie sémantique plus spécifique (`readme_`, `guide_`, `download_`, `icon_`) prime toujours sur une catégorie générique liée à l'hébergeur (`github_`, `url_`)**, même si l'URL technique pointe effectivement vers GitHub. Le préfixe `github_` est réservé aux liens qui n'ont pas de catégorie sémantique plus précise (repo, releases/latest génériques, profil, fichiers locaux comme LICENSE.md).

Exemple concret : `download_en` (et non `github_download_en`), même si son URL est bien hébergée sur GitHub.

**Convention du placeholder (variable en attente de vraie valeur)**

Si une variable doit exister dès maintenant mais que sa vraie valeur n'est pas encore connue (ex. un lien externe qui sera fourni plus tard), on la définit quand même avec une valeur placeholder explicite, en majuscules, facile à repérer par une recherche (`grep`) future :

```markdown
[url_nexusmods]: https://URL_NEXUSMOD
```

Ne jamais laisser un placeholder ambigu (ex. `#`, `TODO`, ou une chaîne vide) — le placeholder doit rester une URL syntaxiquement valide (pour ne pas casser le lien à l'affichage) tout en étant immédiatement identifiable comme non-définitif.

---

## 3. Emplacement et organisation des définitions

Toutes les définitions de variables sont regroupées **en bas du fichier**, jamais dispersées.

**Ordre fixe des blocs**, à respecter dans tous les fichiers factorisés du projet pour garantir une cohérence inter-fichiers :

1. Badges (images shields.io)
2. External URLs (services tiers, hors GitHub)
3. GitHub links & local repo files
4. Download links (uniques par langue/fichier)
5. Language README files
6. Language online guides (GitHub Pages)
7. Icônes/assets partagés (mémo ou actifs)

Structure attendue :

```markdown
<!-- ============================== -->
<!--    Link & Badge Definitions    -->
<!-- ============================== -->

<!-- Badges (shields.io images) -->
[badge_xxx]: ...
[badge_yyy]: ...

<!-- External URLs (services tiers, hors GitHub) -->
[url_xxx]: ...

<!-- GitHub links & local repo files -->
[github_xxx]: ...

<!-- Download links (unique per language) -->
[download_xxx]: ...

<!-- Language README files -->
[readme_xxx]: ...

<!-- Language online guides (GitHub Pages) -->
[guide_xxx]: ...

<!-- Mémo : ... (préciser pourquoi la variable n'est pas utilisée activement) -->
[icon_xxx]: ...
```

**Règles strictes à respecter :**

1. **Une définition de référence doit être seule sur sa ligne.** Impossible d'ajouter un commentaire à la suite sur la même ligne (`[var]: url <!-- commentaire -->`) — GitHub ne reconnaît alors plus la ligne comme une définition valide, et l'affiche telle quelle, en texte brut visible dans le rendu final. Ce piège a été rencontré concrètement : toujours mettre un éventuel commentaire d'accompagnement sur la **ligne suivante**, jamais sur la même ligne.

   ✅ Correct :
   ```markdown
   [icon_download]: ./assets/download-loop.svg
   <!-- url_lien_absolu: https://raw.githubusercontent.com/... -->
   ```

   ❌ Incorrect (casse le rendu) :
   ```markdown
   [icon_download]: ./assets/download-loop.svg <!-- url_lien_absolu: ... -->
   ```

2. **Lien de secours obligatoire en cas de chemin relatif.** *(reformulé en v1.2 — n'est plus optionnel)* Dès qu'une variable utilise un chemin relatif (recommandé par défaut pour la robustesse — voir section 5), un lien absolu de secours doit **systématiquement** être documenté juste en dessous, en commentaire sur sa propre ligne — pas seulement « quand cela semble utile ». Ce lien de secours doit impérativement être une **URL raw** (`raw.githubusercontent.com/...`), jamais une URL `/blob/...` (voir section 5 pour la raison).

   **Label standardisé obligatoire** : toujours utiliser exactement le préfixe `url_lien_absolu:` pour ce commentaire, dans tous les fichiers du projet. Cette cohérence permet de retrouver facilement tous les liens de secours d'un projet par une simple recherche (`grep "url_lien_absolu"`).

   ```markdown
   [icon_download]: ./assets/download-loop.svg
   <!-- url_lien_absolu: https://raw.githubusercontent.com/... -->
   ```

3. **Chaque catégorie de variables doit être précédée d'un commentaire de section** (`<!-- Badges -->`, `<!-- GitHub links -->`, etc.), pour que le fichier reste lisible et navigable même avec beaucoup de variables.

---

## 4. Chapitre spécial : comportement des références dans les tableaux Markdown

C'est le point le plus piégeux et le plus important à respecter. Le moteur de rendu des tableaux GitHub Flavored Markdown se comporte différemment du reste du document dès qu'une **image** est impliquée dans un lien.

### Tableau récapitulatif des tests effectués

| Combinaison testée | Contexte | Résultat |
|---|---|---|
| Lien texte seul en référence : `[texte][lien_ref]` | Cellule de tableau | ✅ Fonctionne |
| Lien texte seul direct : `[texte](url)` | Cellule de tableau | ✅ Fonctionne (évidemment) |
| Image + lien tous deux en référence : `[![alt][img_ref]][lien_ref]` | Cellule de tableau | ❌ Casse — affiche le texte brut `![alt][img_ref]` en hyperlien |
| Image en référence + lien direct : `[![alt][img_ref]](url)` | Cellule de tableau | ❌ Casse — même symptôme |
| **Image directe + lien en référence : `[![alt](url_image)][lien_ref]`** | Cellule de tableau | ✅ Fonctionne |
| Image + lien tous deux en référence : `[![alt][img_ref]][lien_ref]` | **Hors tableau** (ex. badges en haut de page) | ✅ Fonctionne parfaitement |

### Règle à retenir, formulée précisément

**Dans une cellule de tableau, dès qu'une image est impliquée dans un lien, le chemin de l'image doit systématiquement rester écrit en direct** (`(url_image)` ou `(./chemin/relatif)`), jamais en référence. Seule la partie destination du lien — la redirection au clic — peut être une variable.

La syntaxe qui fonctionne à coup sûr dans un tableau est donc :

```markdown
[![nom](url_image)][variable_redirection]
```

La variable de redirection est indispensable à cet endroit précis (c'est elle qui apporte tout l'intérêt de la maintenabilité — un seul endroit à modifier si le lien de destination change), mais l'image, elle, doit impérativement rester en clair.

**Ne pas essayer de factoriser l'image elle-même dans un tableau**, même si ça a fonctionné hors tableau (badges) — le contexte "cellule de tableau" a un parseur plus restrictif qui ne supporte pas cette combinaison, quelle que soit l'URL utilisée (testé avec chemins relatifs, absolus, et raw — le problème n'est pas l'URL, c'est la position dans le tableau).

---

## 5. Chemins relatifs, chemins absolus, et piège des URL `/blob/`

- Un **chemin relatif** (`./assets/fichier.svg`) se résout **depuis l'emplacement du fichier qui le contient**, pas depuis la racine du repo par défaut. Si le fichier Markdown testé n'est pas à la racine du repo (par exemple un fichier de test posé dans un sous-dossier), le chemin relatif doit être ajusté en conséquence (`../assets/fichier.svg`, etc.). Toujours vérifier l'emplacement réel du fichier avant de diagnostiquer un chemin relatif comme "cassé".

- Une URL de type `https://github.com/.../blob/main/....` **n'est pas un fichier brut** — c'est la page HTML de visualisation du fichier sur GitHub (avec coloration syntaxique, blame, etc.), pas l'image ou le contenu en lui-même. Elle n'est réécrite en contenu brut que par le moteur de rendu des **fichiers de dépôt** (README affiché normalement), mais pas par celui des **Discussions, Issues, ou commentaires de Pull Request**, qui utilisent un pipeline de rendu différent et plus restrictif.

- Pour une compatibilité universelle (fonctionne partout : README, Discussions, Issues, sites externes), toujours préférer une URL de type `https://raw.githubusercontent.com/...` plutôt qu'une URL `/blob/...` pour tout lien de secours absolu ou toute image destinée à s'afficher hors du contexte README classique.

**Règle pratique (systématique, pas seulement "par défaut") :** *(reformulée en v1.2)* pour toute image ou fichier local du repo, toujours factoriser en chemin relatif (robustesse au renommage/déplacement du repo), **avec obligatoirement** un lien absolu raw en secours documenté en commentaire juste en dessous (voir section 3, règle 2). Ce n'est pas un choix au cas par cas : c'est la combinaison par défaut à appliquer systématiquement dès qu'un fichier local du repo est factorisé.

---

## 6. Contexte de test : où prévisualiser fiablement

Le rendu Markdown peut différer significativement selon l'endroit où on le teste :

- **Fichier réel affiché normalement** (README.md sur `main`, ou "Files changed" d'une Pull Request) → moteur de rendu de fichier, le plus fiable pour valider un vrai résultat final.
- **Discussion, Issue, commentaire de PR** → moteur de rendu différent (celui des commentaires), qui ne bénéficie pas de certaines commodités du moteur de fichier (notamment la réécriture automatique des URL `/blob/` en contenu brut).

**Recommandation** : pour tester une factorisation Markdown de façon fiable, toujours privilégier un test sur le vrai fichier (branche de test dédiée, ou Pull Request en prévisualisation "Files changed") plutôt qu'une Discussion ou un commentaire, qui peuvent donner de faux négatifs.

---

## 7. Emojis décoratifs : les placer en dehors des crochets de lien

Quand un emoji précède un texte de lien à but purement décoratif (ex. `🌐` devant "Guide : EN"), il doit être placé **en dehors** des crochets du lien, pas à l'intérieur.

❌ À éviter :
```markdown
[🌐 Guide : EN ↗️][guide_en]
```
→ l'emoji hérite du style de lien (souligné), ce qui est visuellement disgracieux.

✅ Recommandé :
```markdown
🌐 [Guide : EN ↗️][guide_en]
```
→ l'emoji reste neutre, seul le texte du lien lui-même est souligné/coloré.

Cette règle s'applique à tous les emplacements du document où un emoji sert d'illustration devant un lien (tableaux, listes, titres de section, etc.).

---

## 8. Regroupement visuel de plusieurs éléments (ex. badges) sur plusieurs lignes

En Markdown standard, des lignes consécutives **sans ligne vide entre elles** sont fusionnées dans le même paragraphe — le retour à la ligne du code source est traité comme un simple espace, pas comme un saut visuel.

Cela permet d'écrire, par lisibilité du code source, un élément par ligne (par exemple un badge par ligne) sans casser leur alignement visuel en ligne dans le rendu final :

```markdown
[![Badge 1][badge_1]][lien_1]
[![Badge 2][badge_2]][lien_2]
[![Badge 3][badge_3]][lien_3]
```
→ s'affiche bien à la chaîne, sur la même ligne visuelle (avec retour à la ligne naturel uniquement si la largeur de l'écran devient insuffisante).

Si un regroupement visuel volontaire est souhaité (par exemple 3 badges sur une ligne, 3 sur une autre), insérer un `<br />` explicite à l'endroit de la coupure désirée.

---

## 9. Convention pour les balises d'alignement/centrage

Pour centrer un bloc contenant du Markdown (bannière, badges, etc.), toujours utiliser :

```html
<div align="center">

[contenu Markdown ici]

</div>
```

**Ne jamais utiliser `<p align="center">`** pour englober du contenu Markdown multi-lignes ou des liens/images. Explication technique : le moteur de rendu Markdown enveloppe automatiquement chaque paragraphe de contenu dans ses propres balises `<p>...</p>`. Or, en HTML, un `<p>` ne peut pas contenir un autre `<p>` — le navigateur referme alors automatiquement le `<p>` parent dès qu'il rencontre le `<p>` généré par le Markdown, cassant le centrage avant même que le vrai contenu n'apparaisse. `<div>` n'a pas cette restriction et peut contenir des `<p>` imbriqués sans problème.

**Cas limite : texte pur, sans lien ni image.** *(ajouté en v1.2)* Cette règle s'applique uniquement aux blocs centrés contenant un lien ou une image — donc potentiellement factorisables et donc à risque de conflit `<p>` imbriqué. Un bloc de texte pur sans lien/image (ex. un sous-titre en `<em>`/`<b>`) peut légitimement rester en `<p align="center">`, puisqu'aucun `<p>` imbriqué n'est généré dans ce cas. Ne pas convertir systématiquement tous les `<p align="center">` du fichier par réflexe : seuls ceux qui encadrent un lien ou une image sont concernés.

**Rappel de syntaxe** : une ligne vide doit suivre l'ouverture du `<div>` et précéder sa fermeture, pour que GitHub termine correctement le "bloc HTML brut" et reprenne l'interprétation du Markdown à l'intérieur.

---

## 10. Checklist avant de considérer une factorisation terminée

- [ ] La syntaxe existante (Markdown natif vs HTML brut) a été identifiée pour chaque lien/image, et toute conversion HTML → Markdown nécessaire a été signalée avant exécution
- [ ] Le rendu visuel final est strictement identique à l'avant-factorisation (vérifié sur le vrai fichier, pas en Discussion)
- [ ] Toutes les variables respectent la convention de nommage (préfixe cohérent, minuscules, underscores)
- [ ] Chaque variable représente une cible unique, pas un élément visuel — les badges/liens partageant la même destination partagent la même variable
- [ ] Les URLs sémantiquement identiques (même intention fonctionnelle) ont été fusionnées sous une seule variable, avec la valeur la plus précise/dynamique
- [ ] La règle de priorité de préfixe a été appliquée en cas d'ambiguïté (catégorie spécifique avant catégorie générique)
- [ ] Toutes les définitions sont regroupées en bas du fichier, dans l'ordre fixe des blocs, chacune commentée
- [ ] Aucune définition de référence ne partage sa ligne avec un commentaire
- [ ] Tout chemin relatif est systématiquement accompagné d'un lien de secours absolu raw, sous le label standardisé `url_lien_absolu:`
- [ ] Dans les tableaux, aucune image n'est en référence — seul le lien de destination peut l'être
- [ ] Les emojis décoratifs devant un lien sont placés en dehors des crochets
- [ ] Les blocs de centrage contenant un lien/image utilisent `<div>`, jamais `<p>` ; le texte pur sans lien/image peut rester en `<p>`
- [ ] Chaque modification a été proposée et validée avant exécution (pas de changement à l'aveugle)
