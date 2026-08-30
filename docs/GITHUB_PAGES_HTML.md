# Afficher une page HTML avec GitHub Pages

## Guide de publication et d'accès direct aux fichiers HTML

---

## 0. Introduction — Objectif du guide

Lorsqu'un fichier `.html` est placé dans un repository GitHub, GitHub affiche généralement son **code source** dans son interface.

Par exemple, un fichier :

```text
LANG_FR/
└── guide_FR.html
```

peut être consulté depuis l'interface GitHub avec une URL de type :

```text
https://github.com/UTILISATEUR/MON_REPO/blob/master/LANG_FR/guide_FR.html
```

Cette URL permet de consulter le fichier et son code, mais elle ne demande pas au navigateur de l'interpréter comme une page web.

**GitHub Pages** permet de publier les fichiers d'un repository comme un site web statique.

Le même fichier peut alors être accessible avec une URL de type :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

Dans ce cas, le navigateur reçoit le fichier HTML comme une page web et en affiche le **rendu**, et non le code source présenté par l'interface GitHub.

### Objectif principal

Le but premier de ce guide est donc très simple :

> **Permettre d'obtenir une URL GitHub Pages qui affiche directement le rendu d'un fichier HTML stocké dans un repository GitHub.**

Cette URL peut ensuite être utilisée dans un `README.md`, une documentation, un autre site ou tout autre emplacement permettant d'ajouter un lien.

---

# 1. Comprendre la différence entre GitHub et GitHub Pages

Avant de configurer GitHub Pages, il est important de distinguer deux façons différentes d'accéder au même fichier.

## 1.1. Consultation depuis GitHub

Une URL comme :

```text
https://github.com/UTILISATEUR/MON_REPO/blob/master/LANG_FR/guide_FR.html
```

correspond à l'interface GitHub.

GitHub présente alors le contenu du fichier dans son interface, ce qui permet notamment de consulter et modifier son code.

Pour un fichier HTML, on voit donc essentiellement :

```html
<!DOCTYPE html>
<html>
    ...
</html>
```

Le navigateur n'est pas utilisé ici pour afficher le fichier comme une page du site.

---

## 1.2. Consultation depuis GitHub Pages

Une URL comme :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

correspond au site publié par GitHub Pages.

Le fichier HTML est alors servi comme une ressource web.

Le navigateur interprète :

```html
<h1>Mon guide</h1>
<p>Bienvenue...</p>
```

comme du HTML et affiche le résultat visuel correspondant.

---

## 1.3. Une distinction à retenir

Les deux URLs peuvent pointer vers **le même fichier du repository**, mais elles n'ont pas le même rôle :

| URL | Résultat |
|---|---|
| `github.com/.../blob/...` | Affichage du code dans GitHub |
| `utilisateur.github.io/...` | Affichage du rendu HTML via GitHub Pages |

Il ne faut donc pas chercher à modifier l'URL GitHub `blob` pour obtenir le rendu.

Il faut utiliser **l'URL GitHub Pages**.

---

# 2. Les trois notions fondamentales

Pour comprendre GitHub Pages, trois notions doivent être séparées.

## 2.1. Le repository

Le repository est l'espace contenant les fichiers du projet.

Exemple :

```text
MON_REPO/
├── README.md
├── LANG_FR/
│   └── guide_FR.html
└── LANG_EN/
    └── guide_EN.html
```

GitHub stocke l'ensemble de cette arborescence.

---

## 2.2. GitHub Pages

GitHub Pages prend une partie déterminée du repository et la publie sous forme de site web.

La partie publiée est déterminée par la **source de publication** configurée dans les paramètres de GitHub Pages.

Cette source peut notamment être :

```text
master / (root)
```

ou :

```text
master / docs
```

selon l'organisation du repository et la configuration choisie.

---

## 2.3. `index.html`

`index.html` est traditionnellement le fichier utilisé comme **page d'entrée** d'un site web.

Il peut donc servir de page d'accueil lorsque l'on ouvre simplement :

```text
https://UTILISATEUR.github.io/MON_REPO/
```

Cependant, il est essentiel de comprendre que :

> **`index.html` n'est pas une liste des pages du site et n'est pas nécessaire pour rendre chaque fichier HTML secondaire accessible directement par son URL.**

Cette distinction est développée dans la section suivante.

---

# 3. `index.html` est-il nécessaire ?

## 3.1. Pour afficher directement un fichier HTML : non

Supposons que le repository contienne uniquement :

```text
MON_REPO/
└── LANG_FR/
    └── guide_FR.html
```

et que GitHub Pages publie la racine du repository :

```text
master / (root)
```

Le fichier peut être directement demandé avec :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

**La présence d'un `index.html` n'est pas nécessaire pour accéder à cette page par son URL.**

C'est un point fondamental.

---

## 3.2. Pourquoi ?

GitHub Pages publie les fichiers présents dans sa source de publication.

Le navigateur demande directement :

```text
LANG_FR/guide_FR.html
```

Il n'a donc pas besoin de passer par :

```text
index.html
```

Le chemin est simplement :

```text
URL GitHub Pages
        ↓
MON_REPO/
        ↓
LANG_FR/
        ↓
guide_FR.html
```

---

## 3.3. Quand `index.html` devient-il nécessaire ?

`index.html` devient important lorsque l'on souhaite disposer d'une **page d'entrée** à la racine du site.

Par exemple :

```text
https://UTILISATEUR.github.io/MON_REPO/
```

peut ouvrir :

```text
MON_REPO/index.html
```

Dans ce cas, `index.html` sert de page d'accueil.

Il peut ensuite contenir des liens vers différentes pages :

```text
Accueil
├── Guide français
├── Guide anglais
├── Guide allemand
└── Documentation
```

Mais ces liens sont une question de **navigation**, pas une condition de publication.

---

## 3.4. Exemple concret

Avec :

```text
MON_REPO/
├── index.html
│
├── LANG_FR/
│   └── guide_FR.html
│
└── LANG_EN/
    └── guide_EN.html
```

on peut avoir :

```text
https://UTILISATEUR.github.io/MON_REPO/
```

→ page d'accueil `index.html`

et :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

→ guide français

et :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_EN/guide_EN.html
```

→ guide anglais.

Les deux guides restent accessibles par leur propre URL, qu'ils soient ou non référencés dans `index.html`.

---

# 4. Comprendre la source de publication GitHub Pages

GitHub Pages doit savoir **quelle partie du repository doit être publiée**.

Cette configuration se trouve dans les paramètres du repository, dans :

```text
Settings
└── Pages
```

Avec la méthode de publication depuis une branche, on peut choisir une branche et un dossier source.

Exemple :

```text
Branch : master
Folder : / (root)
```

ou :

```text
Branch : master
Folder : /docs
```

Ces deux configurations sont différentes.

---

# 5. Utiliser la racine du repository comme source

## 5.1. Configuration

La configuration :

```text
Branch : master
Folder : / (root)
```

signifie que la **racine du repository** est utilisée comme racine du site publié.

Exemple :

```text
MON_REPO/
├── index.html
├── README.md
├── LANG_FR/
│   └── guide_FR.html
└── LANG_EN/
    └── guide_EN.html
```

La racine publiée est :

```text
MON_REPO/
```

---

## 5.2. Conséquence

Un fichier :

```text
MON_REPO/LANG_FR/guide_FR.html
```

est accessible avec :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

Le chemin après le nom du repository correspond à son emplacement sous la racine publiée.

---

# 6. Utiliser `docs` comme source

GitHub Pages peut également utiliser le dossier :

```text
/docs
```

comme source de publication.

Dans ce cas, le repository peut être organisé ainsi :

```text
MON_REPO/
├── README.md
├── autres_fichiers/
│
└── docs/
    ├── index.html
    ├── LANG_FR/
    │   └── guide_FR.html
    └── LANG_EN/
        └── guide_EN.html
```

La configuration est alors :

```text
Branch : master
Folder : /docs
```

---

# 7. Point essentiel : `docs` n'apparaît pas dans l'URL

C'est une des principales sources de confusion.

Avec :

```text
MON_REPO/
└── docs/
    └── LANG_FR/
        └── guide_FR.html
```

et :

```text
master / docs
```

l'URL publique est :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

et **pas** :

```text
https://UTILISATEUR.github.io/MON_REPO/docs/LANG_FR/guide_FR.html
```

Pourquoi ?

Parce que `docs` représente ici **la racine de publication**.

Il ne constitue pas un dossier supplémentaire du site.

On peut visualiser le fonctionnement ainsi :

```text
Repository
│
├── README.md
│
└── docs/                    ← source GitHub Pages
    │
    ├── index.html           ← racine du site
    │
    └── LANG_FR/
        └── guide_FR.html
```

Pour GitHub Pages, le contenu de `docs` devient :

```text
Racine du site
│
├── index.html
│
└── LANG_FR/
    └── guide_FR.html
```

---

# 8. `/root` et `/docs` : comparaison

La différence peut être résumée ainsi.

## Avec `/ (root)`

Repository :

```text
MON_REPO/
├── index.html
└── LANG_FR/
    └── guide_FR.html
```

URL :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

## Avec `/docs`

Repository :

```text
MON_REPO/
└── docs/
    ├── index.html
    └── LANG_FR/
        └── guide_FR.html
```

URL :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

### Ce qui change

L'emplacement physique du fichier dans le repository.

### Ce qui ne change pas

Le chemin relatif du fichier **à partir de la racine publiée**.

---

# 9. Comprendre la construction d'une URL GitHub Pages

Pour une Project Page, l'URL suit généralement cette logique :

```text
https://UTILISATEUR.github.io/NOM_DU_REPOSITORY/CHEMIN_DU_FICHIER
```

Par exemple :

```text
https://data-spirit.github.io/NMS_TC/LANG_FR/NMS_txt_code_FR.html
```

correspond à :

```text
NMS_TC/
└── LANG_FR/
    └── NMS_txt_code_FR.html
```

lorsque la racine du repository est la source GitHub Pages.

---

# 10. Les sous-dossiers n'ont pas besoin d'être déclarés

GitHub Pages peut publier une arborescence comportant autant de sous-dossiers que nécessaire.

Par exemple :

```text
MON_REPO/
└── LANG/
    ├── _FR/
    │   └── guide_FR.html
    ├── _EN/
    │   └── guide_EN.html
    ├── _DE/
    │   └── guide_DE.html
    └── _ES/
        └── guide_ES.html
```

Chaque fichier possède alors sa propre URL :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_FR/guide_FR.html
```

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_EN/guide_EN.html
```

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_DE/guide_DE.html
```

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_ES/guide_ES.html
```

Il n'est pas nécessaire de modifier `index.html` à chaque ajout d'une nouvelle langue pour que ces fichiers soient publiés.

---

# 11. Ajouter des liens dans `index.html`

Si une page d'accueil existe, on peut évidemment créer des liens vers les différents guides.

Par exemple :

```html
<a href="LANG/_FR/guide_FR.html">Français</a>
<a href="LANG/_EN/guide_EN.html">English</a>
<a href="LANG/_DE/guide_DE.html">Deutsch</a>
```

Cela permet aux visiteurs de naviguer depuis la page d'accueil.

Mais il faut retenir :

> **Créer un lien vers une page et publier une page sont deux opérations différentes.**

Le lien ne rend pas la page publiable.

La page est publiée parce qu'elle se trouve dans la source GitHub Pages.

Le lien sert uniquement à permettre au visiteur d'y accéder plus facilement.

---

# 12. README.md et index.html

Ces deux fichiers peuvent coexister dans un même repository, mais ils n'ont pas le même rôle.

## `README.md`

Le README est principalement destiné à présenter et documenter le repository GitHub.

Il peut contenir :

- une présentation du projet ;
- des instructions ;
- des informations techniques ;
- la structure du repository ;
- des liens ;
- des références vers des guides externes ou GitHub Pages.

Par exemple :

```text
Documentation

Guide français :
https://UTILISATEUR.github.io/MON_REPO/LANG/_FR/guide_FR.html

Guide anglais :
https://UTILISATEUR.github.io/MON_REPO/LANG/_EN/guide_EN.html
```

---

## `index.html`

`index.html` est une véritable page web.

Il peut servir de page d'accueil pour le site GitHub Pages.

Par exemple :

```text
https://UTILISATEUR.github.io/MON_REPO/
```

peut afficher cette page.

Les deux fichiers peuvent donc avoir des fonctions complètement différentes :

```text
README.md
    ↓
Documentation du repository GitHub

index.html
    ↓
Page d'accueil du site GitHub Pages
```

---

# 13. Exemple d'organisation multilingue

Une organisation possible est :

```text
MON_REPO/
│
├── README.md
├── index.html
│
├── LANG/
│   ├── _FR/
│   │   └── guide_FR.html
│   │
│   ├── _EN/
│   │   └── guide_EN.html
│   │
│   ├── _DE/
│   │   └── guide_DE.html
│   │
│   └── _ES/
│       └── guide_ES.html
│
└── DOCS/
    └── documentation.md
```

Avec Pages configuré sur :

```text
master / (root)
```

les pages HTML peuvent être directement accessibles :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_FR/guide_FR.html
```

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_EN/guide_EN.html
```

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_DE/guide_DE.html
```

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_ES/guide_ES.html
```

La présence ou l'absence de `index.html` n'empêche pas ces URLs individuelles de fonctionner, à condition que le site GitHub Pages soit correctement publié.

---

# 14. Utiliser une page d'accueil avec `index.html`

Si l'on souhaite ensuite créer une véritable page d'accueil, on peut ajouter :

```text
MON_REPO/
├── index.html
├── README.md
│
└── LANG/
    ├── _FR/
    │   └── guide_FR.html
    └── _EN/
        └── guide_EN.html
```

L'adresse :

```text
https://UTILISATEUR.github.io/MON_REPO/
```

peut alors servir de page d'accueil.

Cette page peut proposer :

- une présentation du projet ;
- un lien vers le repository GitHub ;
- des liens vers les différents guides ;
- un sélecteur de langue ;
- d'autres ressources.

Ce fonctionnement est indépendant de l'accessibilité directe des guides.

---

# 15. Procédure pour publier un fichier HTML existant

L'objectif suivant est de rendre directement accessible un fichier HTML existant.

## Étape 1 — Placer le fichier dans le repository

Par exemple :

```text
MON_REPO/
└── LANG_FR/
    └── guide_FR.html
```

---

## Étape 2 — Choisir la source GitHub Pages

Dans le repository GitHub :

```text
Settings
    ↓
Pages
```

Dans la section consacrée à la publication, choisir :

```text
Deploy from a branch
```

Puis sélectionner la branche souhaitée, par exemple :

```text
master
```

et le dossier :

```text
/ (root)
```

si les fichiers HTML se trouvent à la racine du repository et dans ses sous-dossiers.

---

## Étape 3 — Enregistrer la configuration

Sauvegarder la configuration GitHub Pages.

GitHub va alors construire et publier le site.

Le déploiement peut prendre un certain temps.

---

## Étape 4 — Construire l'URL du fichier

Si le fichier se trouve ici :

```text
MON_REPO/LANG_FR/guide_FR.html
```

l'URL correspondante est :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

---

## Étape 5 — Tester

Ouvrir l'URL dans un navigateur.

Le résultat attendu est :

```text
PAGE HTML RENDUE
```

et non :

```text
CODE SOURCE HTML
```

---

# 16. Ajouter le lien dans un README

Une fois l'URL GitHub Pages fonctionnelle, elle peut être utilisée dans le `README.md`.

Exemple Markdown :

```markdown
## Guides

- [Guide français](https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html)
- [Guide anglais](https://UTILISATEUR.github.io/MON_REPO/LANG_EN/guide_EN.html)
```

Le visiteur peut alors partir directement du repository GitHub et accéder à la version web du guide.

Le repository reste l'endroit où le code source est stocké, tandis que GitHub Pages fournit une URL permettant de consulter le rendu.

---

# 17. Erreurs et confusions fréquentes

## ❌ « GitHub devrait afficher mon HTML comme une page »

Pas depuis l'interface classique du repository.

GitHub affiche le fichier comme un fichier source.

Pour obtenir le rendu HTML, il faut passer par GitHub Pages.

---

## ❌ « Je dois ajouter chaque fichier HTML dans `index.html` »

Non.

Un fichier HTML peut être directement accessible par son URL sans apparaître dans `index.html`.

Ajouter un lien dans `index.html` permet seulement de faciliter la navigation.

---

## ❌ « Je dois avoir `index.html` pour que tous mes guides fonctionnent »

Non.

Pour une URL directe comme :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

`index.html` n'est pas nécessaire simplement pour afficher `guide_FR.html`.

---

## ❌ « `index.html` sert à déclarer les fichiers du site »

Non.

Il s'agit simplement d'une page web, généralement utilisée comme page d'entrée.

---

## ❌ « Si j'utilise `/docs`, `docs` apparaîtra dans l'URL »

Non.

Avec :

```text
master / docs
```

le dossier `docs` devient la racine du site publié.

Il ne fait donc pas partie du chemin public.

---

## ❌ « Je peux laisser mes fichiers à la racine si Pages utilise `/docs` »

Non.

Si `/docs` est la source de publication, les fichiers à publier doivent se trouver dans `docs` ou dans ses sous-dossiers.

---

## ❌ « L'URL GitHub et l'URL GitHub Pages sont identiques »

Non.

Exemple GitHub :

```text
https://github.com/UTILISATEUR/MON_REPO/blob/master/LANG_FR/guide_FR.html
```

Exemple GitHub Pages :

```text
https://UTILISATEUR.github.io/MON_REPO/LANG_FR/guide_FR.html
```

La première permet de consulter le code dans l'interface GitHub.

La seconde permet d'afficher la page publiée.

---

# 18. Diagnostic rapide

Si une page HTML ne s'affiche pas correctement via GitHub Pages, vérifier les points suivants :

```text
☐ GitHub Pages est activé

☐ La bonne branche est sélectionnée

☐ La bonne source (/root ou /docs) est sélectionnée

☐ Le fichier HTML se trouve dans la source publiée

☐ Le chemin utilisé dans l'URL correspond exactement à l'arborescence publiée

☐ L'URL utilisée est une URL github.io

☐ L'URL ne correspond pas à une URL github.com/.../blob/...

☐ Le déploiement GitHub Pages est terminé

☐ Le fichier HTML lui-même est valide et fonctionne correctement
```

### Et concernant `index.html` :

```text
☐ Ai-je besoin d'une page d'accueil à la racine du site ?
```

Si la réponse est **non**, l'absence de `index.html` n'empêche pas, à elle seule, l'accès direct à une page HTML secondaire.

Si la réponse est **oui**, il faut créer une page d'entrée appropriée à la racine de la source publiée.

---

# 19. Exemple de référence complet

## Structure avec la racine du repository comme source

```text
MON_REPO/
│
├── README.md
│
├── index.html
│
├── LANG/
│   ├── _FR/
│   │   └── guide_FR.html
│   │
│   ├── _EN/
│   │   └── guide_EN.html
│   │
│   └── _DE/
│       └── guide_DE.html
│
└── DOCS/
    └── documentation.md
```

Configuration :

```text
Branch : master
Folder : / (root)
```

URLs :

```text
https://UTILISATEUR.github.io/MON_REPO/
```

→ `index.html`

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_FR/guide_FR.html
```

→ guide français

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_EN/guide_EN.html
```

→ guide anglais

```text
https://UTILISATEUR.github.io/MON_REPO/LANG/_DE/guide_DE.html
```

→ guide allemand

Les trois guides sont accessibles directement, indépendamment du fait qu'ils soient ou non référencés dans `index.html`.

---

# 20. À retenir

Les cinq règles essentielles sont :

### 1. GitHub affiche les fichiers HTML comme du code

Une URL `github.com/.../blob/...` correspond à l'interface du repository.

### 2. GitHub Pages permet d'afficher le rendu HTML

Une URL `github.io/...` permet au navigateur d'interpréter le fichier HTML comme une page web.

### 3. La source GitHub Pages détermine ce qui est publié

Elle peut notamment être :

```text
master / (root)
```

ou :

```text
master / docs
```

La source sélectionnée devient la **racine du site publié**.

### 4. `index.html` n'est pas nécessaire pour les pages HTML secondaires

Un fichier comme :

```text
LANG_FR/guide_FR.html
```

peut être directement accessible par son URL sans être déclaré dans `index.html`.

### 5. `index.html` sert de page d'entrée

Si l'on souhaite que :

```text
https://UTILISATEUR.github.io/MON_REPO/
```

affiche une page d'accueil, `index.html` peut servir de page d'entrée à la racine de la source publiée.

---

## Résumé visuel

```text
                         REPOSITORY GITHUB
                                │
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
             Interface GitHub         GitHub Pages
                    │                       │
                    ▼                       ▼
             Affiche le code          Sert les fichiers
                    │                       │
                    ▼                       ▼
       github.com/.../blob/...       utilisateur.github.io/...
                                            │
                                            ▼
                                  navigateur interprète
                                       le HTML
                                            │
                                            ▼
                                   PAGE WEB RENDUE
```

Et concernant `index.html` :

```text
index.html
    │
    └── sert de page d'entrée / accueil
```

mais :

```text
LANG_FR/guide_FR.html
LANG_EN/guide_EN.html
LANG_DE/guide_DE.html
```

peuvent être consultés directement par leur propre URL.

**La publication d'une page HTML et sa présence dans `index.html` sont donc deux choses indépendantes.**