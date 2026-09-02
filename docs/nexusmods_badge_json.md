# Guide — Créer un badge Shields.io custom via un Endpoint JSON

---

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

<details>
<summary>🌐 Liens utiles : </summary>

- Shields.io : <https://shields.io>
- Simple Icons : <https://simpleicons.org/>

</details>

---

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

---

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

---

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
  "cacheSeconds": 300,
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

---

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
  "cacheSeconds": 300
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

---

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

---

## 7. Générer correctement la chaîne `logoSvg`

Le champ `logoSvg` doit contenir **tout le contenu du fichier `.svg` sur
une seule ligne**, avec les guillemets internes `"` échappés en `\"`. Le
faire à la main est risqué (un guillemet oublié, un retour à la ligne qui
traîne, et le JSON entier devient invalide). Voici trois méthodes au choix
selon ce que tu as sous la main — toutes donnent exactement le même
résultat, à copier-coller tel quel comme valeur de `logoSvg`.

<details>
<summary> Laquelle choisir ? </summary>

- **[7a] (PowerShell)** : Si tu es sous Windows et que tu ne veux rien installer, cette méthode est la plus directe (l'outil est déjà présent sur le système). 
- **[7b] (Node.js)** : est équivalent en simplicité si tu l'as déjà installé (souvent le cas pour du dev web).
- **[7c] (Python)**  : demande une étape de plus (créer le fichier script), mais devient réutilisable d'un simple `python3 svg_to_logosvg.py autre_logo.svg` par la suite.

</details>

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

---

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

---

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
  "logoSvg": "<svg width=\"100%\" height=\"100%\" viewBox=\"0 0 42 42\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\"><g transform=\"matrix(0.253936,0,0,0.253936,0.330195,0.430507)\"><path d=\"M44.4,162.5C43.8,162.5 43.1,162.5 42.5,162.4C41,162.2 39.6,161.9 38,161.4C35.2,160.5 32.8,159.2 31.1,158.2C27.3,156 23.4,153.3 19.3,149.9C17.5,148.4 15.7,146.8 14,145.2L12.6,143.8C11.6,142.9 10.7,141.9 10,140.8C8.7,138.8 7.6,136.2 7.5,132.8C7.4,131.7 7.3,130.6 7.3,129.4C7.3,127 7.4,124.4 7.8,121.9C8.5,116.7 10.2,112.1 11.5,108.6C11.6,108.3 11.7,108 11.8,107.7C11.4,106.8 11.1,105.8 10.7,104.8C8.9,99.6 7.7,93.8 7.1,88C6.5,81.9 6.7,75.7 7.6,69.6C7.8,68.3 8,67 8.3,65.8C5.9,62.3 2.9,57.3 1,51.5L1,51.4C0.6,50.2 -0.4,47.2 0.2,43.4C0.4,42 0.7,40.6 1.2,39.1C2.1,36.3 3.4,34 4.4,32.3C6.6,28.5 9.3,24.7 12.6,20.6C14.1,18.8 15.6,17 17.2,15.4L18.6,14C19.3,13.2 20.1,12.5 21,11.9C23,10.4 25.8,9.1 29.6,9C30.8,8.9 32.1,8.8 33.4,8.8L33.5,8.8C36,8.8 38.7,9 41.3,9.4C45.3,10 48.9,11.1 52.1,12.3C54.2,11.4 56.4,10.6 58.7,9.8C64.1,8 69.9,6.8 75.7,6.4C81.8,5.9 88,6.2 93.9,7.2C95.3,7.4 96.7,7.7 98.1,8C102.8,4.8 107.1,2.5 111.6,1.1L111.7,1.1C112.7,0.7 114.9,-0 117.8,-0C118.4,-0 119.1,-0 119.7,0.1C121.2,0.3 122.6,0.6 124.2,1.1C127,2 129.4,3.3 131.1,4.3C134.9,6.5 138.8,9.2 142.9,12.6C144.7,14.1 146.5,15.7 148.2,17.3L149.6,18.7C150.3,19.3 151,20 151.5,20.8C153.3,23.1 154.7,26.4 154.8,31C154.9,32.6 154.9,34.3 154.8,36C154.6,39.7 154.1,43.2 153.2,46.4C152.5,48.8 151.7,51.2 150.8,53.6C152.6,58.1 153.9,62.7 154.8,67.4C156.6,77.3 156.4,87.5 154.2,97.3C155.5,99.2 156.7,101 157.7,102.8C159.4,105.8 160.8,108.9 161.8,112.1C162.2,113.3 163.1,116.3 162.5,120.3C162.3,121.7 161.9,123 161.4,124.5C159.6,129.6 156.8,133.8 154.3,137.3C151.6,141.1 148.5,144.8 145.3,148.2L144.1,149.4C143.4,150.2 142.6,150.9 141.7,151.6C139.7,153.1 136.9,154.3 133.1,154.5C131.9,154.6 130.6,154.7 129.3,154.7L129.2,154.7C126.5,154.7 123.8,154.5 121,154C116.5,153.3 112.5,151.9 108.9,150.5C107,151.3 105,152 103.1,152.6C97.5,154.3 91.6,155.4 85.7,155.7C79.6,156.1 73.4,155.6 67.4,154.5C66.7,154.4 65.9,154.2 65.2,154.1C60,157.8 55.4,160.2 50.6,161.8L50.5,161.8C49.5,161.7 47.3,162.5 44.4,162.5ZM24.6,134.1L35.2,137.8C36.1,135.2 36.2,132.4 35.6,129.8C35.6,130 35.6,130.3 35.7,130.5C35.7,130.8 35.8,131.2 35.8,131.6C35.7,129.6 35,127 33.2,124.6C32.5,123.7 31.7,122.9 30.8,122.2L31.3,122.6L32.2,123.5C31.4,122.7 30.5,121.9 29.5,121.2L24.6,134.1ZM123.7,129.4C122.9,130.2 122.1,131 121.4,132.1L133.3,136.7L133.3,125.6C132.2,125.6 131.1,125.7 130.1,126L130.7,126C131,126 131.4,125.9 131.8,125.9C130,126 127.6,126.6 125.4,128C124.2,128.8 123.2,129.7 122.3,130.9L122.7,130.4L123.7,129.4ZM35.8,126.8C36.3,127.2 36.8,127.6 37.3,128.1C39.9,130.3 42.3,132 44.5,133.3C45.9,132.6 47.5,131.6 49.2,130.3C49.7,130 50.1,129.6 50.6,129.2C50.9,129 51.1,128.7 51.4,128.5C51.5,128.4 51.7,128.2 51.8,128.1L58,121.8L66.4,124.7C66.7,124.8 67,124.9 67.2,125C69,125.6 70.8,126 72.6,126.4C76.3,127.1 80.2,127.4 84,127.1C87.6,126.9 91.3,126.2 94.7,125.2C96.4,124.7 98.1,124.1 99.7,123.3C100.5,123 101.3,122.6 102,122.2C104,121.2 106.3,120.6 108.6,120.6C112.2,120.6 114.9,121.9 116.2,122.6C116.6,122.8 117,123 117.5,123.1C120,124.1 122.9,125.3 125.5,125.7C125.9,125.8 126.4,125.8 126.8,125.9C128.3,124.2 129.7,122.4 131,120.6C131.8,119.5 132.6,118.4 133.3,117.3C133.2,117.1 133.1,116.9 132.9,116.6C132.2,115.4 131.4,114.2 130.4,112.7C130.1,112.2 129.7,111.8 129.3,111.3C129.1,111.1 129,110.9 128.8,110.7C124.7,106.7 123.3,101 125.2,95.6C125.3,95.3 125.4,95 125.5,94.8C127.8,87.6 128.2,79.9 126.9,72.5C126.2,69 125.2,65.5 123.7,62.2C123.6,61.9 123.4,61.6 123.3,61.3C120,55.2 121.4,50 122.6,47.5C123.1,46.5 123.5,45.4 123.9,44.4C124.7,42.5 125.3,40.5 125.9,38.7C126.1,37.8 126.3,36.9 126.4,35.8C125.9,35.4 125.4,35 124.9,34.5C122.2,32.3 119.9,30.6 117.7,29.3C116.3,30.1 114.7,31.1 112.9,32.3C112.4,32.7 111.9,33.1 111.4,33.5C111.3,33.6 111.1,33.7 111,33.9C108.3,36.5 104.7,37.9 101,37.9C99.2,37.9 97.5,37.6 95.8,36.9C95.4,36.8 95,36.6 94.6,36.5C92.8,36 91,35.5 89.1,35.2C85.4,34.6 81.5,34.4 77.7,34.7C74.1,35 70.5,35.7 67.1,36.8C65.4,37.3 63.8,38 62.2,38.7C61.4,39 60.7,39.4 59.9,39.8L59.5,40C57.4,41.2 54.9,41.8 52.5,41.8C50.3,41.8 48.1,41.3 46,40.3C45.5,40.1 45.1,39.9 44.6,39.7C42.2,38.7 39.3,37.6 36.8,37.3C36.4,37.2 36,37.2 35.7,37.1C35.3,37.6 34.9,38.1 34.5,38.5C32.3,41.2 30.6,43.5 29.3,45.8C30,47.2 31,48.7 32.2,50.5C32.5,51 32.9,51.5 33.3,51.9C33.5,52.2 33.8,52.4 34,52.7L39.8,58.8L37.3,66.8C37.1,67.3 37,67.8 36.8,68.3C36.3,70.1 35.9,72 35.6,73.9C35,77.7 34.9,81.5 35.3,85.4C35.6,89 36.4,92.6 37.6,96C38.2,97.7 38.9,99.3 39.6,100.9C39.7,101.1 39.8,101.3 39.9,101.5C42,105.8 42,110.6 39.8,114.9C39.6,115.3 39.4,115.7 39.3,116.1C38.9,117.1 38.4,118.1 38,119.1C37.2,121.3 36.2,123.9 35.9,126.2C35.9,126.3 35.8,126.6 35.8,126.8ZM129.9,38.8C130.7,39.6 131.6,40.4 132.7,41.2L137.6,28.3L127,24.6C126.1,27.2 126,30 126.6,32.6L126.6,30.9C126.6,32.4 127.1,34.9 128.7,37.3C129.5,38.4 130.4,39.4 131.5,40.3L131,39.9L129.9,38.8ZM29.3,26.3L29.3,37.4C30.4,37.4 31.5,37.3 32.5,37L31.9,37C31.6,37 31.2,37.1 30.8,37.1C32.6,37 35,36.4 37.2,35C38.4,34.2 39.4,33.3 40.3,32.1L39.9,32.6L39,33.6C39.8,32.8 40.6,31.9 41.3,30.9L29.3,26.3Z\" style=\"fill-rule:nonzero;\"/><path d=\"M56.3,88.4L57,116.7L50,111C42.2,123.7 39.7,136 43.4,145.1L44.7,148.3L41.5,146.9C34.2,143.7 27.6,139.2 22.1,133.4L21.8,133.1L21.7,132.6C21.3,129.1 21.5,125.3 22.4,121.4L22.4,121.3C23.7,116.4 25.6,111.5 28,106.6C29.5,103.5 31.3,100.4 33.3,97.4L27.2,92.4L56.3,88.4Z\" style=\"fill:rgb(249,115,22);fill-rule:nonzero;\"/><path d=\"M105.9,74.1L105.2,45.8L112.2,51.5C120,38.8 122.5,26.5 118.8,17.4L117.5,14.2L120.7,15.6C128,18.8 134.6,23.3 140.1,29.1L140.4,29.4L140.5,29.9C140.9,33.4 140.7,37.2 139.8,41.1L139.8,41.2C138.5,46.1 136.6,51 134.2,55.9C132.7,59 130.9,62.1 128.9,65.1L135,70.1L105.9,74.1Z\" style=\"fill:rgb(249,115,22);fill-rule:nonzero;\"/><path d=\"M88.5,105.4L116.8,104.7L111.1,111.7C123.8,119.5 136.1,122 145.2,118.3L148.4,117L147,120.2C143.8,127.5 139.3,134.1 133.5,139.6L133.2,139.9L132.7,140C129.2,140.4 125.4,140.2 121.5,139.3L121.4,139.3C116.5,138 111.6,136.1 106.7,133.7C103.6,132.2 100.5,130.4 97.5,128.4L92.5,134.5L88.5,105.4Z\" style=\"fill:rgb(249,115,22);fill-rule:nonzero;\"/><path d=\"M74.1,57.6L45.8,58.3L51.5,51.3C38.8,43.5 26.5,41 17.4,44.7L14.3,46L15.7,42.8C18.9,35.5 23.4,28.9 29.2,23.4L29.5,23.1L30,23C33.5,22.6 37.3,22.8 41.2,23.7L41.3,23.7C46.2,25 51.1,26.9 56,29.3C59.1,30.8 62.2,32.6 65.2,34.6L70.2,28.5L74.1,57.6Z\" style=\"fill:rgb(249,115,22);fill-rule:nonzero;\"/><circle cx=\"81.4\" cy=\"80.8\" r=\"60.5\" style=\"fill:rgb(251,146,60);\"/><path d=\"M59.3,59.5C55.8,57.9 53.2,56.3 50.6,54.4C46.6,51.6 42.9,48.5 39.8,45.2C32.2,37.5 28.2,29.6 29.3,23.1L27,25.6C21.5,31.4 14.2,41.6 14.1,46L14.2,46.5C15.2,49.9 16.8,53.3 19.1,56.6L19.1,56.7C22.1,61.5 28,69.4 49,78.6L45.3,85.6L73.6,78L63.5,51.5L59.3,59.5Z\" style=\"fill:rgb(244,244,245);fill-rule:nonzero;\"/><path d=\"M103.3,103.5C106.8,105.1 109.4,106.7 112,108.6C116,111.4 119.7,114.5 122.8,117.8C130.4,125.5 134.4,133.4 133.3,139.9L135.6,137.5C141.1,131.7 148.4,121.5 148.5,117.1L148.4,116.6C147.4,113.2 145.8,109.8 143.5,106.5L143.5,106.4C140.5,101.6 134.6,93.7 113.6,84.5L117.3,77.5L89,85.1L99.2,111.3L103.3,103.5Z\" style=\"fill:rgb(244,244,245);fill-rule:nonzero;\"/><path d=\"M104,59.3C105.6,55.8 107.2,53.2 109.1,50.6C111.9,46.6 115,42.9 118.3,39.8C126,32.2 133.9,28.2 140.4,29.3L138,27C132.2,21.5 122,14.2 117.6,14.1L117.1,14.2C113.7,15.2 110.3,16.8 107,19.1L106.9,19.1C102.1,22.1 94.2,28 85,49L78,45.3L85.6,73.6L112,63.6L104,59.3Z\" style=\"fill:rgb(244,244,245);fill-rule:nonzero;\"/><path d=\"M58.2,103.2C56.6,106.7 55,109.3 53.1,111.9C50.3,115.9 47.2,119.6 43.9,122.7C36.2,130.3 28.3,134.3 21.8,133.2L24.2,135.5C30,141 40.2,148.3 44.6,148.4L45.1,148.3C48.5,147.3 51.9,145.7 55.2,143.4L55.3,143.4C60.1,140.4 68,134.5 77.2,113.5L84.2,117.2L76.6,88.9L50.3,98.9L58.2,103.2Z\" style=\"fill:rgb(244,244,245);fill-rule:nonzero;\"/></g></svg>"
}
```

* 🎨 `0f0f10` :  couleur à gauche (noir)
* 🎨 `c07131` :  couleur à droite (orange/doré)

⚠️ correspondent aux couleurs Nexus Mods retenues pour le badge.

### 9.1 **Adresse raw du JSON hébergé sur le repo NMS_TC :**

```
https://raw.githubusercontent.com/Data-Spirit/NMS_TC/main/assets/nexusmods_badge.json
```

### 9.2 **URL finale du badge** 
Une fois cette adresse URL-encodée et injectée dans `img.shields.io/endpoint`, avec quelques paramètres ajoutés/surchargés
directement en query string (`style`, `logoSize`, `label`, `labelColor`, `color`) :

```
https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131
```

⚠️ Un lien surchargé en query strings est utile car il permet a celui qui le souhaite de changer a la volée (directement dans le lien), les couleurs, le message etc, sans toucher au fichier `.json`.

### 9.3 **Intègration dans le `README.md`.**

Deux versions possibles :

   **Version simple, lien cliquable classique (Markdown) :**

   ```markdown
   [![Mon badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131)](https://URL_MOD_NEXUSMOD.com)
   ```

   **Version centrée, lien cliquable (HTML — compatible README GitHub) :**

   ```html
   <p align="center">
     <a href="https://URL_MOD_NEXUSMOD.com">
       <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131" alt="Mon badge">
     </a>
   </p>
   ```

---

## 10. Sources

<details>
<summary>🌐 Liens externes : </summary>

- Documentation Endpoint Badge : <https://shields.io/badges/endpoint-badge>
- Documentation Badge statique : <https://shields.io/badges/static-badge>
- Bibliothèque d'icônes simple-icons : <https://simpleicons.org/>
- Liste des slugs simple-icons : <https://github.com/simple-icons/simple-icons/blob/master/slugs.md>
- Répertoire d'endpoints compatibles Shields (exemples communautaires) : <https://github.com/badges/endpoint-badges-directory>

</details>