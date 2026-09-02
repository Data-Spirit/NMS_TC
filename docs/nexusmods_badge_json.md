# Guide — Créer un badge Shields.io custom via un Endpoint JSON

## 1. C'est quoi, un badge Shields.io ?

Un badge est ce petit rectangle coloré qu'on voit en haut des README GitHub
(`build: passing`, `license: MIT`, etc.). [Shields.io](https://shields.io)
est le service qui génère ces images à la volée : tu lui donnes une URL, il
te renvoie un `.svg` prêt à afficher.

Il existe plusieurs façons de générer un badge Shields :

- **Badge statique** (`img.shields.io/badge/...`) : tout est dans l'URL,
  pratique pour un badge simple et fixe.
- **Badge dynamique** (`dynamic-json`, `dynamic-xml`...) : Shields va lire
  une valeur dans un fichier de données externe (ex: le nombre de
  téléchargements d'un package).
- **Endpoint badge** (`img.shields.io/endpoint?url=...`) : *toi* tu fournis
  un petit fichier JSON qui décrit entièrement le badge (texte, couleurs,
  logo, style). Shields se contente de le lire et de le dessiner. C'est
  cette dernière méthode qu'on documente ici.

**Liens utiles :**
- Shields.io : <https://shields.io>
- Simple Icons : <https://simpleicons.org/>

## 2. Pourquoi passer par un Endpoint JSON plutôt qu'un badge statique ?

La raison principale, dans notre cas : **afficher un logo qui n'existe pas
dans la bibliothèque d'icônes standard de Shields**.

Shields sait afficher nativement des centaines de logos via le paramètre
`logo=` (ou `namedLogo` dans le JSON), en piochant dans
[simple-icons](https://simpleicons.org/) — une bibliothèque communautaire
de logos de marques/outils/services. Mais si le service que tu veux
représenter (dans notre cas Nexus Mods) n'y figure pas, `namedLogo` ne
suffit plus.

L'Endpoint badge résout ça grâce au champ `logoSvg` : on peut fournir
**notre propre SVG**, peu importe son origine, et Shields l'affichera comme
logo du badge.

## 3. Piège courant : un "SVG" peut être un PNG déguisé

Attention en récupérant un logo SVG "tout fait" sur internet (forums,
gists, dépôts tiers) : beaucoup de ces fichiers ne sont **pas** de vrais
SVG vectoriels. Ils contiennent en réalité une balise `<image>` avec une
image PNG encodée en base64 à l'intérieur d'un simple conteneur `<svg>` :

```xml
<svg width="51" height="51" viewBox="0 0 51 51" ...>
  <image width="51" height="51"
         xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." />
</svg>
```

Ça *fonctionne* visuellement, mais on perd tout l'intérêt du vectoriel :
l'image devient floue en zoomant/agrandissant, le fichier est plus lourd
que nécessaire, et on ne peut plus modifier les couleurs ou les formes
facilement.

⚠️ C'est pourquoi il est toujours préférable d'utiliser un vrai
SVG vectoriel (tracés `<path>`, `<circle>`, etc.) plutôt qu'un PNG
camouflé dans un conteneur SVG.

## 4. Cas A — Badge avec logo SVG custom (`logoSvg`)

### 4.1 Modèle JSON (copiable, tous les champs pertinents pour ce cas)

```json
{
  "schemaVersion": 1,
  "label": "monlabel",
  "message": "montexte",
  "labelColor": "1a1a1a",
  "color": "blue",
  "isError": false,
  "style": "flat",
  "cacheSeconds": 3600,
  "logoSvg": "<svg width=\"100%\" height=\"100%\" viewBox=\"0 0 42 42\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"...\" fill=\"#000\"/></svg>"
}
```

### 4.2 Explication ligne par ligne

| Champ | Rôle | Notes |
|---|---|---|
| `schemaVersion` | Version du schéma Shields. | **Obligatoire**, toujours `1`. |
| `label` | Le texte affiché **à gauche** du badge. | **Obligatoire**. `""` masque complètement le côté gauche. Surchargeable via `?label=` dans l'URL. |
| `message` | Le texte affiché **à droite** du badge. | **Obligatoire**, ne peut jamais être vide. |
| `labelColor` | Couleur de fond du côté **gauche** (celui du `label`). | Accepte hex (`1a1a1a`), rgb/rgba, hsl/hsla, ou noms CSS. Défaut : `grey`. |
| `color` | Couleur de fond du côté **droit** (celui du `message`). | Mêmes formats que `labelColor`. Défaut : `lightgrey`. |
| `isError` | Si `true`, badge marqué "erreur". | Empêche l'utilisateur de surcharger la couleur via l'URL. Défaut : `false`. |
| `style` | Le gabarit visuel du badge. | Valeurs possibles : `flat` (défaut), `flat-square`, `plastic`, `for-the-badge`, `social`. Surchargeable via `?style=`. |
| `cacheSeconds` | Durée pendant laquelle Shields garde le badge en cache avant de revenir lire ton JSON. Une valeur basse = mise à jour plus rapide du badge en cas de changement ; une valeur haute = moins de sollicitation de ton hébergement. | **Défaut et minimum : 300 secondes (5 min).** Toute valeur inférieure à 300 est ignorée (Shields retombe sur 300). Surchargeable via `?cacheSeconds=` dans l'URL, mais **uniquement vers le haut** (un visiteur peut demander plus long, jamais plus court que ce que tu as défini). |
| `logoSvg` | Le SVG custom, sous forme de chaîne de caractères échappée. | Voir §7 pour la génération correcte de cette chaîne. Prioritaire sur `namedLogo`. |

## 5. Cas B — Badge avec logo de la bibliothèque simple-icons (`namedLogo`)

### 5.1 Modèle JSON (copiable, tous les champs pertinents pour ce cas)

```json
{
  "schemaVersion": 1,
  "label": "monlabel",
  "message": "montexte",
  "labelColor": "1a1a1a",
  "color": "blue",
  "isError": false,
  "namedLogo": "github",
  "logoColor": "white",
  "logoSize": "auto",
  "style": "flat",
  "cacheSeconds": 3600
}
```

### 5.2 Explication des champs propres à ce cas (logo NON-custom)

Les champs `schemaVersion`, `label`, `message`, `labelColor`, `color`,
`isError`, `style` et `cacheSeconds` fonctionnent exactement comme décrit
au §4.2. Seuls les champs suivants sont spécifiques à un logo de
bibliothèque plutôt qu'à un `logoSvg` custom :

| Champ | Rôle | Notes |
|---|---|---|
| `namedLogo` | Slug d'une icône de la bibliothèque [simple-icons](https://simpleicons.org/). | Le site **simpleicons.org** fournit directement le code (`slug`) de chaque logo — il suffit de chercher l'icône sur le site et de copier son nom pour l'utiliser tel quel comme valeur de `namedLogo`. Liste complète alternative : <https://github.com/simple-icons/simple-icons/blob/master/slugs.md>. À utiliser **à la place de** `logoSvg`, pas en plus. |
| `logoColor` | Couleur du logo. | Fonctionne **uniquement** avec `namedLogo`. Sans effet si `logoSvg` est utilisé. |
| `logoSize` | `"auto"` = redimensionnement adaptatif du logo. | Fonctionne **uniquement** avec `namedLogo`. Utile pour des logos larges (ex: `amd`, `amg`). Sans effet si `logoSvg` est utilisé. |

## 6. `namedLogo` vs `logoSvg` : lequel utiliser ?

- **`namedLogo`** (§5) : rapide, léger, aucune donnée à héberger toi-même
  — mais limité aux icônes déjà répertoriées sur simple-icons.
- **`logoSvg`** (§4) : total contrôle sur le visuel (couleurs, formes, logo
  maison ou introuvable ailleurs) — en échange il faut fournir et héberger
  le SVG toi-même.

Les deux champs peuvent techniquement coexister dans le même JSON sans
faire planter le badge, mais dans les faits `logoSvg` prend le dessus :
autant ne renseigner que celui dont tu as besoin, pour garder le fichier
lisible.

## 7. Générer correctement la chaîne `logoSvg`

Le champ `logoSvg` doit contenir **tout le contenu du fichier `.svg` sur
une seule ligne**, avec les guillemets internes `"` échappés en `\"`. Le
faire à la main est risqué (un guillemet oublié, un retour à la ligne qui
traîne, et le JSON entier devient invalide). Voici trois méthodes au choix
selon ce que tu as sous la main — toutes donnent exactement le même
résultat, à copier-coller tel quel comme valeur de `logoSvg`.

### 7a. Avec PowerShell (Windows, la plus simple — rien à installer)

1. Place ton fichier `.svg` dans un dossier, par exemple le Bureau
   (`Desktop`).
2. Dans ce dossier, ouvre PowerShell (clic droit dans le dossier →
   *Ouvrir dans le terminal*, ou `cd` manuellement vers le dossier).
3. Exécute cette commande (remplace `mon_logo.svg` par le nom réel de ton
   fichier) :

   ```powershell
   Get-Content -Raw -Encoding UTF8 "mon_logo.svg" | ConvertTo-Json
   ```

4. Le résultat affiché dans le terminal (guillemets englobants inclus) est
   directement ta valeur pour `logoSvg` — copie-le tel quel.

### 7b. Avec Node.js (Windows/Mac/Linux, une seule commande)

Si Node.js est installé sur ta machine :

1. Ouvre un terminal dans le dossier contenant ton `.svg`.
2. Exécute (en remplaçant `mon_logo.svg` par le nom réel) :

   ```bash
   node -e "console.log(JSON.stringify(require('fs').readFileSync('mon_logo.svg', 'utf8')))"
   ```

3. Copie le résultat affiché.

### 7c. Avec Python (nécessite de créer un petit script, réutilisable ensuite)

1. Dans le même dossier que ton `.svg`, crée un fichier texte nommé
   `svg_to_logosvg.py` avec ce contenu :

   ```python
   #!/usr/bin/env python3
   """
   Affiche le contenu d'un fichier SVG sous forme de chaîne JSON échappée,
   prête à coller comme valeur du champ "logoSvg".

   Usage :
       python3 svg_to_logosvg.py mon_logo.svg
   """
   import json
   import sys

   if len(sys.argv) != 2:
       sys.exit("Usage : python3 svg_to_logosvg.py <fichier.svg>")

   with open(sys.argv[1], "r", encoding="utf-8") as f:
       svg = f.read().strip()

   print(json.dumps(svg))
   ```

2. Ouvre un terminal dans ce dossier.
3. Exécute (en remplaçant `mon_logo.svg` par le nom réel) :

   ```bash
   python3 svg_to_logosvg.py mon_logo.svg
   ```

4. Copie le résultat affiché.

**Laquelle choisir ?** Si tu es sous Windows et que tu ne veux rien
installer, **7a (PowerShell)** est la plus directe — l'outil est déjà
présent sur le système. Node.js (7b) est équivalent en simplicité si tu
l'as déjà installé (souvent le cas pour du dev web). Python (7c) demande
une étape de plus (créer le fichier script), mais devient réutilisable
d'un simple `python3 svg_to_logosvg.py autre_logo.svg` par la suite.

## 8. Héberger le JSON et construire l'URL du badge

1. Place ton fichier `.json` final dans ton repo (par ex.
   `assets/mon-badge.json`) et commit/push sur GitHub.
2. Récupère son URL brute (`raw.githubusercontent.com/...`).
3. Construis l'URL du badge :

   ```
   https://img.shields.io/endpoint?url=<URL_JSON_ENCODÉE>
   ```

   L'URL de ton fichier JSON doit être **URL-encodée** avant d'être placée
   dans le paramètre `url=`, car certains caractères (`:`, `/`, `?`, `&`...)
   ont un sens spécial dans une URL et doivent être remplacés par leur
   équivalent `%XX` pour ne pas être mal interprétés. Les remplacements les
   plus courants pour une URL GitHub raw :

   - `:` devient `%3A`
   - `/` devient `%2F`
   - `?` devient `%3F`
   - `&` devient `%26`
   - (espace) devient `%20`

   Exemple avant/après :

   ```
   Avant : https://raw.githubusercontent.com/user/repo/main/assets/mon-badge.json
   Après : https%3A%2F%2Fraw.githubusercontent.com%2Fuser%2Frepo%2Fmain%2Fassets%2Fmon-badge.json
   ```

   Plutôt que de faire ces remplacements à la main, utilise un de ces
   outils en une commande :

   ```javascript
   // Console du navigateur, ou Node.js
   encodeURIComponent("https://raw.githubusercontent.com/user/repo/main/assets/mon-badge.json")
   ```

   ```python
   # Python
   from urllib.parse import quote
   print(quote("https://raw.githubusercontent.com/user/repo/main/assets/mon-badge.json", safe=""))
   ```

   ```powershell
   # PowerShell
   [uri]::EscapeDataString("https://raw.githubusercontent.com/user/repo/main/assets/mon-badge.json")
   ```

4. Intègre le badge dans ton `README.md`. Deux versions possibles :

   **Version simple, lien cliquable classique (Markdown) :**

   ```markdown
   [![Mon badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fuser%2Frepo%2Fmain%2Fassets%2Fmon-badge.json)](https://exemple.com)
   ```

   **Version centrée, lien cliquable (HTML — compatible README GitHub) :**

   ```html
   <p align="center">
     <a href="https://exemple.com">
       <img alt="Mon badge" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fuser%2Frepo%2Fmain%2Fassets%2Fmon-badge.json">
     </a>
   </p>
   ```

⚠️ **Deux niveaux de cache à connaître** :
- `raw.githubusercontent.com` est mis en cache environ 5 minutes côté GitHub.
- Le champ `cacheSeconds` du JSON (voir §4.2) a un défaut et un minimum de
  300 secondes (5 min) côté Shields — une valeur plus basse est ignorée.

Les deux tombent dans le même ordre de grandeur : après une modification du
JSON, compte jusqu'à ~5 minutes avant que le badge affiché ne se
mette à jour, quel que soit le réglage de `cacheSeconds`.

## 9. Exemple concret — badge Nexus Mods (NMS_TC)

Cas réel utilisé dans ce projet : le logo Nexus Mods n'existe pas dans
simple-icons, on a donc recréé son SVG vectoriel à la main (plutôt que de
réutiliser un PNG encodé en base64 trouvé ailleurs) et on l'a intégré en
`logoSvg` :

```json
{
  "schemaVersion": 1,
  "label": "nexus",
  "message": "mods",
  "labelColor": "0f0f10",
  "color": "c07131",
  "style": "flat",
  "logoSvg": "<svg width=\"100%\" height=\"100%\" viewBox=\"0 0 42 42\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\"><g transform=\"matrix(0.253936,0,0,0.253936,0.330195,0.430507)\">... (tracés du logo) ...</g></svg>"
}
```

`0f0f10` / `c07131` correspondent aux couleurs retenues pour le badge
Nexus Mods du projet NMS_TC.

**Adresse raw du JSON hébergé sur le repo NMS_TC :**

```
https://raw.githubusercontent.com/Data-Spirit/NMS_TC/main/assets/nexusmods_badge.json
```

**URL finale du badge**, une fois cette adresse URL-encodée et injectée dans
`img.shields.io/endpoint`, avec quelques paramètres ajoutés/surchargés
directement en query string (`style`, `logoSize`, `label`, `labelColor`,
`color`) :

```
https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131
```

## 10. Sources

- Documentation Endpoint Badge : <https://shields.io/badges/endpoint-badge>
- Documentation Badge statique : <https://shields.io/badges/static-badge>
- Bibliothèque d'icônes simple-icons : <https://simpleicons.org/>
- Liste des slugs simple-icons : <https://github.com/simple-icons/simple-icons/blob/master/slugs.md>
- Répertoire d'endpoints compatibles Shields (exemples communautaires) : <https://github.com/badges/endpoint-badges-directory>
