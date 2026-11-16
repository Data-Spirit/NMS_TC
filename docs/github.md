<!-- Version du fichier 
> Version : 1.0
> Dernière modification : 2026-11-16
-->

# Maintenir le dépôt sur GitHub — NMS_TC

Comment ce dépôt est tenu sur GitHub : qui fait quoi, la forme des commits, les versions et les tags, les releases, le CHANGELOG et la ROADMAP, GitHub Pages, et les choix volontaires du dépôt. Ce fichier fait foi pour tout ce qui touche à git et à GitHub ; les autres documents y renvoient au lieu de répéter ces règles.

Il s'adresse au mainteneur, à toute personne qui contribue, et à tout agent (Claude Code ou autre) qui travaille sur le dépôt. Une règle nouvelle ou modifiée s'ajoute ici, sur proposition, comme toute modification du dépôt.

---

## 1. Qui fait quoi

- **Le mainteneur fait toutes les opérations git et GitHub** : `git add`, commit, push, tag, release, réglages du dépôt. Personne d'autre, et aucun agent, ne commite, ne pousse, ne tague ni ne publie.
- **Un agent prépare et vérifie** : il modifie les fichiers après un feu vert explicite, contrôle le résultat, puis **donne pour chaque commit un titre et un message à copier**, en texte dans la conversation. Jamais de message passé par un fichier (`git commit -F …`) : le mainteneur doit pouvoir lire exactement ce qu'il commite.
- **Un commit par fichier**, ou par lot très cohérent (par exemple un fichier et son déplacement). L'ordre des commits est donné ; après chaque commit annoncé par le mainteneur, l'agent vérifie l'état du dépôt avant de donner le suivant.
- **L'index git appartient au mainteneur.** Un agent ne fait ni `git add` (même `git add -N` pour un contrôle), ni `git mv`, ni `git rm` : il déplace ou supprime avec les commandes ordinaires (`mv`, `rm`), et le mainteneur ajoute les deux chemins ensemble (git reconnaît alors un renommage). Pour lister les fichiers non suivis : `git ls-files --others --exclude-standard`.

## 2. Messages de commit

**Forme** : un titre `type : description`, en anglais, puis un corps facultatif en anglais, sous forme de liste.

```
update : README_FR v2.8 - Italian added (4 languages, ~466 KB)
```

- **Types en usage** :

  | Type | Pour |
  |---|---|
  | `release` | le commit du guide qui le fait passer à une nouvelle version, et lui seul ; c'est sur lui que se pose le tag `vX.Y` (`release : HTML guide v2.4 - Italian added (i18n-it block, noscript)`) |
  | `add` | un fichier, une langue ou une fonction nouvelle, hors guide (`add : README_IT v2.8 - Italian README`) |
  | `update` | une évolution d'un fichier existant, hors guide, documentation comprise (`update : ROADMAP - …`) |
  | `fix` | une correction de défaut dans un script ou la documentation (`fix : check scripts v1.1 - …`) |
  | `move` | un déplacement sans changement de contenu (`move : release txt v2.0 move to legacy folder`) |

  Le guide lui-même (`LANG/NMS_txt_code.html`) ne change jamais sans changer de version : chacun de ses commits est donc un commit `release`, et la nature du changement (langue ajoutée, corrections, accessibilité…) se dit après le tiret. Les autres fichiers d'une même sortie (notes de version, CHANGELOG, README) gardent `add` ou `update` : `release` désigne le commit du guide, pas la release GitHub.

  Les anciens types (`test`, `sup`, `chgt`, `upgrade`…) appartiennent aux premières versions et ne s'emploient plus. Les commits déjà publiés ne se réécrivent pas : avant la v2.5, les commits du guide portent `add` ou `fix`.
- **Description** : le fichier ou le sujet, sa nouvelle version s'il en a une, puis l'essentiel après un tiret (`README_EN v2.8 - Italian added (…)`).
- **Corps** : ce qui a changé et comment cela a été vérifié (scripts lancés, md5 du livrable) ; ne pas répéter le titre.
- **Corps en liste classique** : une puce `- ` par changement ou par vérification, une idée par puce, avec des sous-puces indentées si un point se détaille. Ne pas enchaîner plusieurs éléments dans une même phrase séparés par des `/` ou des points-virgules : une liste se lit d'un coup d'œil, une énumération en ligne non.

  ```
  update : README_FR v2.8 - Italian added (4 languages, ~466 KB)

  - Available languages: French, English, Spanish and Italian.
  - Key figures: 4 languages in the interactive guide.
  - File size: ~451 KB → ~466 KB (3 mentions).
  - No heading changed: table of contents anchors unchanged.
  ```
- **Aucune ligne d'attribution.** Jamais de `Co-Authored-By: …`, de « Generated with … » ni d'autre mention d'un outil ou d'une IA, ni dans les commits, ni dans le texte d'une release, ni dans aucun fichier du dépôt — même si un outil le propose automatiquement. Règle permanente du mainteneur.

## 3. Versions et tags

- **La version du projet est celle du guide** : `> Version :` dans l'en-tête de `LANG/NMS_txt_code.html`. Elle change quand le guide change (contenu, code, nouvelle langue), jamais pour la seule documentation.
- **Le tag `vX.Y` se pose sur le commit `release` du guide**, celui qui fait passer `NMS_txt_code.html` à la version X.Y (exemple, avant l'adoption du type `release` : `v2.4` sur `add : Italian translation - guide v2.4 …`). Les commits de documentation qui suivent (README, CHANGELOG, notes de version) restent après le tag : c'est voulu, le tag marque le guide, pas la documentation. Un tag déjà publié ne se déplace pas.
- **Les autres fichiers ont leur propre version**, indépendante : chaque README (`README_<LANG>.md`), le README racine, les prompts, `revision.md`, `pitfalls.md`, ce fichier (en-tête `Version du fichier`). Les blocs de langue du guide portent la version des textes qu'ils reflètent (`_meta.translation_version`).
- **Numérotation du guide** : version mineure suivante pour une langue ajoutée ou un lot de corrections et d'améliorations (2.3 → 2.4) ; version majeure pour un changement de conception (2.0 : un seul fichier pour toutes les langues).

## 4. Releases

Une release par version du guide, publiée par le mainteneur après le push du commit du guide et des documents de la version :

- **Tag** : `vX.Y` (voir ci-dessus). **Titre** : `NMS_TC vX.Y`.
- **Texte** : identique, caractère pour caractère, à `docs/RELEASE_NOTES_vX.Y.md` (bannière, présentation commune, langues disponibles, puis les notes propres à la version).
- **Fichier joint** : `NMS_txt_code.html`, le guide tel qu'il est au commit tagué ; sa taille et son SHA-256 figurent à la fin des notes de version.
- **Notes précédentes** : à chaque nouvelle version, `docs/RELEASE_NOTES_v<précédente>.md` est déplacé dans `docs/_legacy/` (sans modification) ; un seul fichier de notes reste dans `docs/`.
- **Téléchargement** : le README racine pointe vers `releases/latest/download/NMS_txt_code.html`, qui suit toujours la dernière release sans retouche.

## 5. CHANGELOG et ROADMAP

- **[CHANGELOG.md](../CHANGELOG.md)** suit [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), en anglais, du plus récent au plus ancien : une section par version du guide (date, sous-titre, lien vers les notes de version), rubriques Added, Changed, Fixed, Removed, Security. Chaque modification du dépôt s'inscrit dans `[Unreleased]` ; à la sortie d'une version, `[Unreleased]` passe dans la nouvelle section. Liens de comparaison en bas du fichier.
- **[ROADMAP.md](../ROADMAP.md)** ne garde que ce qui reste à faire (En cours, Prévu, Idées) ; ce qui est fait passe dans le CHANGELOG.
- **Ni l'un ni l'autre n'est lié depuis le README** : ils servent au suivi du projet (et aux curieux) ; le README porte déjà l'information utile aux joueurs.

## 6. Choix volontaires du dépôt

À ne pas « corriger » sans décision du mainteneur :

- **Les issues GitHub sont désactivées.** Aucun document ne renvoie vers elles.
- **Le badge Nexus Mods du README pointe vers une adresse provisoire** (`https://URL_NEXUSMOD`) jusqu'à la publication du guide sur Nexus Mods.
- **GitHub Pages** publie le dépôt avec Jekyll :
  - `_config.yml` désactive la page d'accueil générée depuis le README : la racine du site renvoie une 404, volontairement ; le guide reste en ligne à `/LANG/NMS_txt_code.html` ;
  - les dossiers dont le nom commence par `_` ne sont pas publiés : **`docs/_legacy/` ne doit jamais l'être** (anciennes versions) ;
  - tout autre fichier Markdown est publié ; choisir plus finement ce qui l'est (`exclude:`) est prévu dans la ROADMAP.

## 7. Fichiers et encodage

- Fichiers texte en **UTF-8 sans BOM**, fins de ligne **LF**. Git avertit qu'il les convertira en CRLF à la prochaine opération : avertissement sans conséquence.
- Un script qui écrit un fichier du dépôt relève ses fins de ligne avant d'écrire et les conserve.

## 8. Vérifier après publication

Après le push, le tag et la release, une vérification rapide (le mainteneur, ou un agent à sa demande) :

1. **Dépôt** : `main` local identique à `origin/main` ; aucune ligne d'attribution dans les derniers commits (`git log --format=%B | grep -ci "co-authored"` → `0`).
2. **Tag** : `vX.Y` présent sur GitHub et posé sur le commit du guide, dont le titre commence par `release :` (`git log -1 --format=%s vX.Y`).
3. **Release** : la dernière (« Latest »), ni brouillon ni préversion ; texte identique à `docs/RELEASE_NOTES_vX.Y.md` ; fichier joint au bon SHA-256 ; le lien de téléchargement du README sert ce même fichier.
4. **GitHub Pages** : le guide en ligne identique au fichier du dépôt ; la racine en 404 ; rien de `docs/_legacy/` publié.
5. **Liens et rendu** : liens des notes de version et du README racine valides ; ancres des README (`#tab-infos`…) présentes sur GitHub.

---

## Voir aussi

[Procédure de révision](revision.md) · [Pièges connus](pitfalls.md) · [Prompt maître de révision](prompts/prompt_revision_NMS_TC.md) · [Ajout d'une langue](prompts/prompt_add_language_NMS_TC.md)
