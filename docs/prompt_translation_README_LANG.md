# Translation Prompt — NMS_TC README

Prompt réutilisable pour traduire le README du projet NMS_TC dans une nouvelle langue.
Pour une nouvelle traduction : copier ce fichier, changer uniquement le bloc `TARGET`, et donner ce fichier + le `README_FR.md` source à Claude.

---

## TARGET

```yaml
target_language: English          # ex: English, Deutsch, Español, 日本語
target_variant: neutral/standard  # ex: US, UK, neutral/standard, none (pour langues sans variante notable)
lang_code: EN                     # code de langue à 2 lettres majuscules (EN, ES, DE, JA...) — voir règle §0 ci-dessous
output_filename: README_EN.md     # convention : README_<lang_code>.md
source_file: README_FR.md
```

### 0. Règle de correspondance des suffixes de langue (IMPORTANT)

Ce README documente un fichier `.html` compagnon (le guide interactif lui-même), et **les deux fichiers doivent toujours partager le même suffixe de langue** :

| README | Guide HTML documenté |
|---|---|
| `README_FR.md` | `NMS_txt_code_FR.html` |
| `README_EN.md` | `NMS_txt_code_EN.html` |
| `README_ES.md` | `NMS_txt_code_ES.html` |
| `README_<lang_code>.md` | `NMS_txt_code_<lang_code>.html` |

**Action obligatoire** : dans la ligne d'introduction du README (juste sous le titre H1, celle qui donne le nom du fichier, son poids et ses caractéristiques), remplacer le nom du fichier `.html` par `NMS_txt_code_<lang_code>.html`, où `<lang_code>` est exactement celui défini dans `TARGET` ci-dessus. Ne jamais laisser le suffixe de la langue source (ex. `_FR`) dans un README traduit.

Cette règle vaut uniquement pour le README (`translation_prompt_README_LANG.md`). Un prompt distinct, `translation_prompt_HTML_GUIDE_LANG.md`, gérera plus tard la traduction du contenu interne du fichier `.html` lui-même — les deux prompts sont complémentaires mais indépendants.

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

### 3. Variante linguistique
- Utiliser la variante indiquée dans `target_variant` ci-dessus. Si `neutral/standard` : choisir la forme la plus largement comprise et la moins marquée régionalement.

### 4. Éléments à NE JAMAIS traduire
- Noms de balises/tags du jeu (ex. `VISOR`, `COMMODITY`, `SPECIAL`, `TRANS_WAR`, `PR_0`–`PR_15`, `BULLETPOINT_OFF`, `<IMG>`, `<>`, `</>`).
- Noms de fichiers, chemins, extensions (`.html`, `.DDS`, `.md`, `LICENSE.md`).
- Noms de technologies, API, librairies (`navigator.clipboard`, `document.execCommand`, `mask-image`, `table-layout: fixed`, `ICON_DATA`, CSS Grid, HSL).
- Noms propres (Hello Games, No Man's Sky, Google Fonts, Rajdhani, IBM Plex Sans, JetBrains Mono).
- Valeurs numériques, pourcentages, codes hexadécimaux.

### 5. Éléments à adapter/régénérer
- **Ancres du sommaire** : régénérer chaque lien `#ancre` à partir du titre traduit selon la convention de la plateforme cible (GitHub : minuscules, espaces → tirets, accents/caractères spéciaux supprimés). Vérifier que chaque lien du sommaire pointe bien vers le bon titre traduit.
- **Emojis de titres** : conserver les mêmes emojis, seul le texte du titre change.
- Licence : traduire le texte explicatif autour, mais garder le nom de la licence (`CC BY-NC-SA 4.0`) et le chemin du fichier inchangés.

### 6. Structure et formatage
- Conserver **exactement** la structure Markdown source : mêmes niveaux de titres (`#`, `##`, `###`), mêmes tableaux (nombre de colonnes, alignement, ordre des lignes), mêmes séparateurs `---`, mêmes listes à puces, mêmes mises en gras/italique aux mêmes endroits sémantiques.
- Ne pas ajouter, supprimer ou réorganiser de sections par rapport à la source.
- Ne pas raccourcir ni résumer un passage : traduction intégrale, phrase pour phrase, section pour section.

### 7. Cohérence terminologique
- Une fois qu'un terme récurrent est traduit d'une certaine façon (ex. « balise » → « tag »), garder cette même traduction partout dans le document sans varier.
- Construire mentalement (ou explicitement si utile) un petit glossaire des termes récurrents du projet avant de traduire, pour garantir cette cohérence sur tout le fichier.

### 8. Vérification finale (auto-relecture obligatoire avant livraison)
- Le nom du fichier `.html` en tête de document porte-t-il bien le suffixe `<lang_code>` cible (et non celui de la langue source) ? (voir règle §0)
- Chaque lien du sommaire correspond-il à un titre réellement présent et correctement traduit ?
- Aucune balise de jeu, chemin de fichier ou nom technique n'a été traduit par erreur ?
- Le ton reste-t-il fidèle à l'original sur l'ensemble du document, pas seulement dans l'introduction ?
- La structure Markdown (tableaux compris) est-elle identique ligne pour ligne à la source ?

---

## LIVRABLE ATTENDU

Un unique fichier Markdown nommé selon `output_filename`, contenant la traduction complète, prêt à être commité dans le dépôt sans retouche supplémentaire.
