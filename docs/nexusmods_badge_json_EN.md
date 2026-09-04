<a id="top"></a>
# Guide — Create a Custom Shields.io Badge via an Endpoint JSON

<p align="center"><sub>📘 Technical Guide · 🔧 Shields.io · NMS_TC</sub></p>

<details>
<summary><b>📑 Table of Contents</b></summary>

1. [🏷️ What Is a Shields.io Badge?](#sec-1)
2. [🔍 Why Use an Endpoint JSON Instead of a Static Badge?](#sec-2)
3. [🖼️ Common Pitfall: an "SVG" Can Be a Disguised PNG](#sec-3)
4. [🖌️ Case A — Badge with a Custom SVG Logo (`logoSvg`)](#sec-4)
5. [🗂️ Case B — Badge with a simple-icons Library Logo (`namedLogo`)](#sec-5)
6. [⚖️ `namedLogo` vs `logoSvg`: Which One to Use?](#sec-6)
7. [🛠️ Correctly Generating the `logoSvg` String](#sec-7)
8. [🌐 Hosting the JSON and Building the Badge URL](#sec-8)
9. [🎯 Real-world Example — Nexus Mods Badge (NMS_TC)](#sec-9)
10. [🎭 Badge Style Variants](#sec-10)
11. [📚 Sources](#sec-11)

</details>

---

<a id="sec-1"></a>
## 1. 🏷️ What Is a Shields.io Badge?

A badge is that small colored rectangle you see at the top of GitHub READMEs
(`build: passing`, `license: MIT`, etc.).

[Shields.io](https://shields.io) is the service that generates these images
on the fly: you give it a URL, and it returns a ready-to-display `.svg`.

There are several ways to generate a Shields badge:

> - **Static badge** (`img.shields.io/badge/...`): everything is in the URL,
> handy for a simple, fixed badge.
> - **Dynamic badge** (`dynamic-json`, `dynamic-xml`...): Shields reads a
> value from an external data file (e.g., a package's download count).
> - **Endpoint badge** (`img.shields.io/endpoint?url=...`): *you* provide a
> small JSON file that fully describes the badge (text, colors, logo, style).
> Shields simply reads it and draws it. This is the method documented here.

<details>
<summary><b>🌐 Useful Links:</b></summary>

- [Shields.io](https://shields.io)
- [Simple Icons](https://simpleicons.org/)

</details>

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-2"></a>
## 2. 🔍 Why Use an Endpoint JSON Instead of a Static Badge?

> [!IMPORTANT]
> The main reason, in our case: **displaying a logo that doesn't exist in
> Shields' standard icon library**.

Shields can natively display hundreds of logos via the `logo=` parameter
(or `namedLogo` in the JSON), pulling from
[simple-icons](https://simpleicons.org/) — a community-maintained library
of brand/tool/service logos.

But if the service you want to represent (Nexus Mods, in our case) isn't
listed there, `namedLogo` isn't enough anymore.

The Endpoint badge solves this with the `logoSvg` field: we can provide
**our own SVG**, regardless of its origin, and Shields will display it as
the badge's logo.

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-3"></a>
## 3. 🖼️ Common Pitfall: an "SVG" Can Be a Disguised PNG

> [!WARNING]
> Watch out when grabbing a "ready-made" SVG logo from the internet (forums,
> gists, third-party repos): a lot of these files are **not** actually vector
> SVGs.

They actually contain an `<image>` tag with a base64-encoded PNG image
inside a plain `<svg>` container:

```xml
<svg width="51" height="51" viewBox="0 0 51 51" ...>
  <image width="51" height="51"
         xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." />
</svg>
```

It *works* visually, but you lose the whole point of using vectors: the
image gets blurry when zoomed in or enlarged, the file is heavier than it
needs to be, and you can no longer easily tweak the colors or shapes.

> [!IMPORTANT]
> That's why it's always better to use a real vector SVG (`<path>`,
> `<circle>` shapes, etc.) rather than a PNG disguised inside an SVG
> container.

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-4"></a>
## 4. 🖌️ Case A — Badge with a Custom SVG Logo (`logoSvg`)

### 4.1 JSON Template (copy-paste ready, all fields relevant to this case)

```json
{
  "schemaVersion": 1,
  "label": "mylabel",
  "message": "mytext",
  "labelColor": "1a1a1a",
  "color": "blue",
  "isError": false,
  "style": "flat",
  "cacheSeconds": 300,
  "logoSvg": "<svg width=\"100%\" height=\"100%\" viewBox=\"0 0 42 42\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"...\" fill=\"#000\"/></svg>"
}
```

### 4.2 Field-by-field Explanation

| 🔑 Field | 📝 Role | 💡 Notes |
|---|---|---|
| `schemaVersion` | Shields schema version. | **Required**, always `1`. |
| `label` | The text shown **on the left** side of the badge. | **Required**. `""` completely hides the left side. Overridable via `?label=` in the URL. |
| `message` | The text shown **on the right** side of the badge. | **Required**, can never be empty. |
| `labelColor` | Background color of the **left** side (the `label` side). | Accepts hex (`1a1a1a`), rgb/rgba, hsl/hsla, or CSS names. Default: `grey`. |
| `color` | Background color of the **right** side (the `message` side). | Same formats as `labelColor`. Default: `lightgrey`. |
| `isError` | If `true`, the badge is marked as an "error". | Prevents the user from overriding the color via the URL. Default: `false`. |
| `style` | The badge's visual template. | Possible values: `flat` (default), `flat-square`, `plastic`, `for-the-badge`, `social`. Overridable via `?style=`. |
| `cacheSeconds` | How long Shields keeps the badge cached before reading your JSON again. A low value = faster badge updates when something changes; a high value = less load on your hosting. | **Default and minimum: 300 seconds (5 min).** Any value below 300 is ignored (Shields falls back to 300). Overridable via `?cacheSeconds=` in the URL, but **only upward** (a visitor can request a longer cache, never a shorter one than what you've set). |
| `logoSvg` | The custom SVG, as an escaped character string. | See §7 for how to properly generate this string. Takes priority over `namedLogo`. |

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-5"></a>
## 5. 🗂️ Case B — Badge with a simple-icons Library Logo (`namedLogo`)

### 5.1 JSON Template (copy-paste ready, all fields relevant to this case)

```json
{
  "schemaVersion": 1,
  "label": "mylabel",
  "message": "mytext",
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

### 5.2 Explanation of Fields Specific to This Case (non-custom logo)

The `schemaVersion`, `label`, `message`, `labelColor`, `color`, `isError`,
`style`, and `cacheSeconds` fields work exactly as described in §4.2.

Only the following fields are specific to a library logo rather than a
custom `logoSvg`:

| 🔑 Field | 📝 Role | 💡 Notes |
|---|---|---|
| `namedLogo` | Slug of an icon from the [simple-icons](https://simpleicons.org/) library. | The **simpleicons.org** site directly provides the code (`slug`) for each logo — just search for the icon on the site and copy its name to use as-is as the `namedLogo` value. Alternative full list: <https://github.com/simple-icons/simple-icons/blob/master/slugs.md>. Use it **instead of** `logoSvg`, not alongside it. |
| `logoColor` | The logo's color. | Only works **with** `namedLogo`. Has no effect if `logoSvg` is used. |
| `logoSize` | `"auto"` = adaptive logo resizing. | Only works **with** `namedLogo`. Useful for wide logos (e.g., `amd`, `amg`). Has no effect if `logoSvg` is used. |

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-6"></a>
## 6. ⚖️ `namedLogo` vs `logoSvg`: Which One to Use?

- **`namedLogo`** (§5): fast, lightweight, no data to host yourself — but
  limited to icons already listed on simple-icons.
  
- **`logoSvg`** (§4): full control over the visuals (colors, shapes, a
  custom logo or one you can't find elsewhere) — in exchange, you have to
  provide and host the SVG yourself.

> [!NOTE]
> Both fields can technically coexist in the same JSON without breaking the
> badge, but in practice `logoSvg` takes precedence — you might as well only
> fill in the one you actually need, to keep the file readable.

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-7"></a>
## 7. 🛠️ Correctly Generating the `logoSvg` String

The `logoSvg` field must contain **the entire content of the `.svg` file on
a single line**, with internal `"` quotes escaped as `\"`.

> [!CAUTION]
> Doing this by hand is risky (a forgotten quote, a stray line break, and the
> entire JSON becomes invalid).

Here are three methods to choose from depending on what you have on hand —
they all give exactly the same result, ready to copy-paste as the value of
`logoSvg`.

👉 <ins>**Which One Should You Choose?**</ins>
> - **7a- [ PowerShell ]** : If you're on Windows and don't want to install anything, this method is the most direct one (the tool is already on the system).
> - **7b- [ Node.js ]** : just as simple if you already have it installed (often the case for web dev).
> - **7c- [ Python ]**  : requires one extra step (creating the script file), but becomes reusable afterward with a simple `python3 svg_to_logosvg.py another_logo.svg`.

<details>
<summary><b>🪟 7a. With PowerShell (Windows, the simplest — nothing to install)</b></summary>

1. Put your `.svg` file in a folder, for example the Desktop.
2. In that folder, open PowerShell (right-click in the folder →
   *Open in Terminal*, or `cd` into the folder manually).
3. Run this command (replace `my_logo.svg` with your file's actual name):

   ```powershell
   Get-Content -Raw -Encoding UTF8 "my_logo.svg" | ConvertTo-Json
   ```

4. The result shown in the terminal (surrounding quotes included) is
   directly your value for `logoSvg` — copy it as-is.

</details>

<details>
<summary><b>🟩 7b. With Node.js (Windows/Mac/Linux, a single command)</b></summary>

If Node.js is installed on your machine:

1. Open a terminal in the folder containing your `.svg`.
2. Run (replacing `my_logo.svg` with the actual name):

   ```bash
   node -e "console.log(JSON.stringify(require('fs').readFileSync('my_logo.svg', 'utf8')))"
   ```

3. Copy the displayed result.

</details>

<details>
<summary><b>🐍 7c. With Python (requires creating a small script, reusable afterward)</b></summary>

1. In the same folder as your `.svg`, create a text file named `svg_to_logosvg.py` with this content:

   ```python
   #!/usr/bin/env python3
   """
   Prints the contents of an SVG file as an escaped JSON string,
   ready to paste as the value of the "logoSvg" field.

   Usage:
       python3 svg_to_logosvg.py my_logo.svg
   """
   import json
   import sys

   if len(sys.argv) != 2:
       sys.exit("Usage: python3 svg_to_logosvg.py <file.svg>")

   with open(sys.argv[1], "r", encoding="utf-8") as f:
       svg = f.read().strip()

   print(json.dumps(svg))
   ```

2. Open a terminal in that folder.
3. Run (replacing `my_logo.svg` with the actual name):

   ```bash
   python3 svg_to_logosvg.py my_logo.svg
   ```

4. Copy the displayed result.

</details>

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-8"></a>
## 8. 🌐 Hosting the JSON and Building the Badge URL

1. Put your final `.json` file in your repo (e.g. `assets/my-badge.json`)
   and commit/push to GitHub.
2. Get its raw URL (`raw.githubusercontent.com/...`).
3. Build the badge URL, 2 methods:

> _Shield.io URL Type:_
   ```
   https://img.shields.io/endpoint?url=<ENCODED_JSON_URL>
   ```

> [!NOTE]
> There are two methods to build the badge URL: a manual method, and a method via the shield.io website.

   <ins>**3a. The Manual Method:**</ins>

> [!IMPORTANT]
> Your JSON file's URL must be **URL-encoded** before being placed
> in the `url=` parameter, because certain characters (`:`, `/`, `?`, `&`...)
> have special meaning in a URL and must be replaced with their
> `%XX` equivalent so they aren't misinterpreted.

> [!TIP]
> The most common replacements for a GitHub raw URL:
> - `:` becomes `%3A`
> - `/` becomes `%2F`
> - `?` becomes `%3F`
> - `&` becomes `%26`
> - (space) becomes `%20`

   Before/after example:
   ```
   Before: https://raw.githubusercontent.com/user/repo/main/assets/my-badge.json
   After: https%3A%2F%2Fraw.githubusercontent.com%2Fuser%2Frepo%2Fmain%2Fassets%2Fmy-badge.json
   ```
	
   Rather than doing these replacements by hand, use one of these
   one-line tools:
	
   ```javascript
   // Browser console, or Node.js
   encodeURIComponent("https://raw.githubusercontent.com/user/repo/main/assets/my-badge.json")
   ```
	
   ```python
   # Python
   from urllib.parse import quote
   print(quote("https://raw.githubusercontent.com/user/repo/main/assets/my-badge.json", safe=""))
   ```
	
   ```powershell
   # PowerShell
   [uri]::EscapeDataString("https://raw.githubusercontent.com/user/repo/main/assets/my-badge.json")
   ```

   <ins>**3b. The Method via the shield.io Website**</ins>

> [!NOTE]
> Go to [shield.io/endpoint](https://img.shields.io/badges/endpoint-badge) to create your custom badge URL.\
> To do this, you'll just need the `RAW` url of your `nexusmods_badge.json` file, and enter it in the site's `url — query` field.\

> [!TIP]
> Clicking on `show optional parameters` lets you customize the style, colors, etc.


4. Add the badge to your `README.md`. Two options are possible:

   **Simple version, classic clickable link (Markdown):**

   ```markdown
   [![My badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fuser%2Frepo%2Fmain%2Fassets%2Fmy-badge.json)](https://example.com)
   ```

   **Centered version, clickable link (HTML — GitHub README compatible):**

   ```html
   <p align="center">
     <a href="https://example.com">
       <img alt="My badge" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fuser%2Frepo%2Fmain%2Fassets%2Fmy-badge.json">
     </a>
   </p>
   ```

> [!WARNING]
> **Two caching layers to know about:**
> - `raw.githubusercontent.com` is cached for about 5 minutes on GitHub's side.
> - The JSON's `cacheSeconds` field (see §4.2) has a default and minimum of 300 seconds (5 min) on Shields' side — any lower value is ignored.
>
> Both fall in the same order of magnitude: after editing the JSON, expect up to ~5 minutes before the displayed badge updates, regardless of the `cacheSeconds` setting.

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-9"></a>
## 9. 🎯 Real-world Example — Nexus Mods Badge (NMS_TC)

A real case used in this project:\
The Nexus Mods logo doesn't exist in simple-icons, so its vector SVG was recreated by hand 
(rather than reusing a base64-encoded PNG found elsewhere) and embedded as `logoSvg`:

<ins>[File :](https://github.com/Data-Spirit/NMS_TC/blob/main/assets/nexusmods_logo.svg)</ins> `nexusmods_logo.svg` :⤵️

```svg
<svg width="100%" height="100%" viewBox="0 0 42 42" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <g transform="matrix(0.253936,0,0,0.253936,0.330195,0.430507)">
        <path d="M44.4,162.5C43.8,162.5 43.1,162.5 42.5,162.4C41,162.2 39.6,161.9 38,161.4C35.2,160.5 32.8,159.2 31.1,158.2C27.3,156 23.4,153.3 19.3,149.9C17.5,148.4 15.7,146.8 14,145.2L12.6,143.8C11.6,142.9 10.7,141.9 10,140.8C8.7,138.8 7.6,136.2 7.5,132.8C7.4,131.7 7.3,130.6 7.3,129.4C7.3,127 7.4,124.4 7.8,121.9C8.5,116.7 10.2,112.1 11.5,108.6C11.6,108.3 11.7,108 11.8,107.7C11.4,106.8 11.1,105.8 10.7,104.8C8.9,99.6 7.7,93.8 7.1,88C6.5,81.9 6.7,75.7 7.6,69.6C7.8,68.3 8,67 8.3,65.8C5.9,62.3 2.9,57.3 1,51.5L1,51.4C0.6,50.2 -0.4,47.2 0.2,43.4C0.4,42 0.7,40.6 1.2,39.1C2.1,36.3 3.4,34 4.4,32.3C6.6,28.5 9.3,24.7 12.6,20.6C14.1,18.8 15.6,17 17.2,15.4L18.6,14C19.3,13.2 20.1,12.5 21,11.9C23,10.4 25.8,9.1 29.6,9C30.8,8.9 32.1,8.8 33.4,8.8L33.5,8.8C36,8.8 38.7,9 41.3,9.4C45.3,10 48.9,11.1 52.1,12.3C54.2,11.4 56.4,10.6 58.7,9.8C64.1,8 69.9,6.8 75.7,6.4C81.8,5.9 88,6.2 93.9,7.2C95.3,7.4 96.7,7.7 98.1,8C102.8,4.8 107.1,2.5 111.6,1.1L111.7,1.1C112.7,0.7 114.9,-0 117.8,-0C118.4,-0 119.1,-0 119.7,0.1C121.2,0.3 122.6,0.6 124.2,1.1C127,2 129.4,3.3 131.1,4.3C134.9,6.5 138.8,9.2 142.9,12.6C144.7,14.1 146.5,15.7 148.2,17.3L149.6,18.7C150.3,19.3 151,20 151.5,20.8C153.3,23.1 154.7,26.4 154.8,31C154.9,32.6 154.9,34.3 154.8,36C154.6,39.7 154.1,43.2 153.2,46.4C152.5,48.8 151.7,51.2 150.8,53.6C152.6,58.1 153.9,62.7 154.8,67.4C156.6,77.3 156.4,87.5 154.2,97.3C155.5,99.2 156.7,101 157.7,102.8C159.4,105.8 160.8,108.9 161.8,112.1C162.2,113.3 163.1,116.3 162.5,120.3C162.3,121.7 161.9,123 161.4,124.5C159.6,129.6 156.8,133.8 154.3,137.3C151.6,141.1 148.5,144.8 145.3,148.2L144.1,149.4C143.4,150.2 142.6,150.9 141.7,151.6C139.7,153.1 136.9,154.3 133.1,154.5C131.9,154.6 130.6,154.7 129.3,154.7L129.2,154.7C126.5,154.7 123.8,154.5 121,154C116.5,153.3 112.5,151.9 108.9,150.5C107,151.3 105,152 103.1,152.6C97.5,154.3 91.6,155.4 85.7,155.7C79.6,156.1 73.4,155.6 67.4,154.5C66.7,154.4 65.9,154.2 65.2,154.1C60,157.8 55.4,160.2 50.6,161.8L50.5,161.8C49.5,161.7 47.3,162.5 44.4,162.5ZM24.6,134.1L35.2,137.8C36.1,135.2 36.2,132.4 35.6,129.8C35.6,130 35.6,130.3 35.7,130.5C35.7,130.8 35.8,131.2 35.8,131.6C35.7,129.6 35,127 33.2,124.6C32.5,123.7 31.7,122.9 30.8,122.2L31.3,122.6L32.2,123.5C31.4,122.7 30.5,121.9 29.5,121.2L24.6,134.1ZM123.7,129.4C122.9,130.2 122.1,131 121.4,132.1L133.3,136.7L133.3,125.6C132.2,125.6 131.1,125.7 130.1,126L130.7,126C131,126 131.4,125.9 131.8,125.9C130,126 127.6,126.6 125.4,128C124.2,128.8 123.2,129.7 122.3,130.9L122.7,130.4L123.7,129.4ZM35.8,126.8C36.3,127.2 36.8,127.6 37.3,128.1C39.9,130.3 42.3,132 44.5,133.3C45.9,132.6 47.5,131.6 49.2,130.3C49.7,130 50.1,129.6 50.6,129.2C50.9,129 51.1,128.7 51.4,128.5C51.5,128.4 51.7,128.2 51.8,128.1L58,121.8L66.4,124.7C66.7,124.8 67,124.9 67.2,125C69,125.6 70.8,126 72.6,126.4C76.3,127.1 80.2,127.4 84,127.1C87.6,126.9 91.3,126.2 94.7,125.2C96.4,124.7 98.1,124.1 99.7,123.3C100.5,123 101.3,122.6 102,122.2C104,121.2 106.3,120.6 108.6,120.6C112.2,120.6 114.9,121.9 116.2,122.6C116.6,122.8 117,123 117.5,123.1C120,124.1 122.9,125.3 125.5,125.7C125.9,125.8 126.4,125.8 126.8,125.9C128.3,124.2 129.7,122.4 131,120.6C131.8,119.5 132.6,118.4 133.3,117.3C133.2,117.1 133.1,116.9 132.9,116.6C132.2,115.4 131.4,114.2 130.4,112.7C130.1,112.2 129.7,111.8 129.3,111.3C129.1,111.1 129,110.9 128.8,110.7C124.7,106.7 123.3,101 125.2,95.6C125.3,95.3 125.4,95 125.5,94.8C127.8,87.6 128.2,79.9 126.9,72.5C126.2,69 125.2,65.5 123.7,62.2C123.6,61.9 123.4,61.6 123.3,61.3C120,55.2 121.4,50 122.6,47.5C123.1,46.5 123.5,45.4 123.9,44.4C124.7,42.5 125.3,40.5 125.9,38.7C126.1,37.8 126.3,36.9 126.4,35.8C125.9,35.4 125.4,35 124.9,34.5C122.2,32.3 119.9,30.6 117.7,29.3C116.3,30.1 114.7,31.1 112.9,32.3C112.4,32.7 111.9,33.1 111.4,33.5C111.3,33.6 111.1,33.7 111,33.9C108.3,36.5 104.7,37.9 101,37.9C99.2,37.9 97.5,37.6 95.8,36.9C95.4,36.8 95,36.6 94.6,36.5C92.8,36 91,35.5 89.1,35.2C85.4,34.6 81.5,34.4 77.7,34.7C74.1,35 70.5,35.7 67.1,36.8C65.4,37.3 63.8,38 62.2,38.7C61.4,39 60.7,39.4 59.9,39.8L59.5,40C57.4,41.2 54.9,41.8 52.5,41.8C50.3,41.8 48.1,41.3 46,40.3C45.5,40.1 45.1,39.9 44.6,39.7C42.2,38.7 39.3,37.6 36.8,37.3C36.4,37.2 36,37.2 35.7,37.1C35.3,37.6 34.9,38.1 34.5,38.5C32.3,41.2 30.6,43.5 29.3,45.8C30,47.2 31,48.7 32.2,50.5C32.5,51 32.9,51.5 33.3,51.9C33.5,52.2 33.8,52.4 34,52.7L39.8,58.8L37.3,66.8C37.1,67.3 37,67.8 36.8,68.3C36.3,70.1 35.9,72 35.6,73.9C35,77.7 34.9,81.5 35.3,85.4C35.6,89 36.4,92.6 37.6,96C38.2,97.7 38.9,99.3 39.6,100.9C39.7,101.1 39.8,101.3 39.9,101.5C42,105.8 42,110.6 39.8,114.9C39.6,115.3 39.4,115.7 39.3,116.1C38.9,117.1 38.4,118.1 38,119.1C37.2,121.3 36.2,123.9 35.9,126.2C35.9,126.3 35.8,126.6 35.8,126.8ZM129.9,38.8C130.7,39.6 131.6,40.4 132.7,41.2L137.6,28.3L127,24.6C126.1,27.2 126,30 126.6,32.6L126.6,30.9C126.6,32.4 127.1,34.9 128.7,37.3C129.5,38.4 130.4,39.4 131.5,40.3L131,39.9L129.9,38.8ZM29.3,26.3L29.3,37.4C30.4,37.4 31.5,37.3 32.5,37L31.9,37C31.6,37 31.2,37.1 30.8,37.1C32.6,37 35,36.4 37.2,35C38.4,34.2 39.4,33.3 40.3,32.1L39.9,32.6L39,33.6C39.8,32.8 40.6,31.9 41.3,30.9L29.3,26.3Z" style="fill-rule:nonzero;"/>
        <path d="M56.3,88.4L57,116.7L50,111C42.2,123.7 39.7,136 43.4,145.1L44.7,148.3L41.5,146.9C34.2,143.7 27.6,139.2 22.1,133.4L21.8,133.1L21.7,132.6C21.3,129.1 21.5,125.3 22.4,121.4L22.4,121.3C23.7,116.4 25.6,111.5 28,106.6C29.5,103.5 31.3,100.4 33.3,97.4L27.2,92.4L56.3,88.4Z" style="fill:rgb(249,115,22);fill-rule:nonzero;"/>
        <path d="M105.9,74.1L105.2,45.8L112.2,51.5C120,38.8 122.5,26.5 118.8,17.4L117.5,14.2L120.7,15.6C128,18.8 134.6,23.3 140.1,29.1L140.4,29.4L140.5,29.9C140.9,33.4 140.7,37.2 139.8,41.1L139.8,41.2C138.5,46.1 136.6,51 134.2,55.9C132.7,59 130.9,62.1 128.9,65.1L135,70.1L105.9,74.1Z" style="fill:rgb(249,115,22);fill-rule:nonzero;"/>
        <path d="M88.5,105.4L116.8,104.7L111.1,111.7C123.8,119.5 136.1,122 145.2,118.3L148.4,117L147,120.2C143.8,127.5 139.3,134.1 133.5,139.6L133.2,139.9L132.7,140C129.2,140.4 125.4,140.2 121.5,139.3L121.4,139.3C116.5,138 111.6,136.1 106.7,133.7C103.6,132.2 100.5,130.4 97.5,128.4L92.5,134.5L88.5,105.4Z" style="fill:rgb(249,115,22);fill-rule:nonzero;"/>
        <path d="M74.1,57.6L45.8,58.3L51.5,51.3C38.8,43.5 26.5,41 17.4,44.7L14.3,46L15.7,42.8C18.9,35.5 23.4,28.9 29.2,23.4L29.5,23.1L30,23C33.5,22.6 37.3,22.8 41.2,23.7L41.3,23.7C46.2,25 51.1,26.9 56,29.3C59.1,30.8 62.2,32.6 65.2,34.6L70.2,28.5L74.1,57.6Z" style="fill:rgb(249,115,22);fill-rule:nonzero;"/>
        <circle cx="81.4" cy="80.8" r="60.5" style="fill:rgb(251,146,60);"/>
        <path d="M59.3,59.5C55.8,57.9 53.2,56.3 50.6,54.4C46.6,51.6 42.9,48.5 39.8,45.2C32.2,37.5 28.2,29.6 29.3,23.1L27,25.6C21.5,31.4 14.2,41.6 14.1,46L14.2,46.5C15.2,49.9 16.8,53.3 19.1,56.6L19.1,56.7C22.1,61.5 28,69.4 49,78.6L45.3,85.6L73.6,78L63.5,51.5L59.3,59.5Z" style="fill:rgb(244,244,245);fill-rule:nonzero;"/>
        <path d="M103.3,103.5C106.8,105.1 109.4,106.7 112,108.6C116,111.4 119.7,114.5 122.8,117.8C130.4,125.5 134.4,133.4 133.3,139.9L135.6,137.5C141.1,131.7 148.4,121.5 148.5,117.1L148.4,116.6C147.4,113.2 145.8,109.8 143.5,106.5L143.5,106.4C140.5,101.6 134.6,93.7 113.6,84.5L117.3,77.5L89,85.1L99.2,111.3L103.3,103.5Z" style="fill:rgb(244,244,245);fill-rule:nonzero;"/>
        <path d="M104,59.3C105.6,55.8 107.2,53.2 109.1,50.6C111.9,46.6 115,42.9 118.3,39.8C126,32.2 133.9,28.2 140.4,29.3L138,27C132.2,21.5 122,14.2 117.6,14.1L117.1,14.2C113.7,15.2 110.3,16.8 107,19.1L106.9,19.1C102.1,22.1 94.2,28 85,49L78,45.3L85.6,73.6L112,63.6L104,59.3Z" style="fill:rgb(244,244,245);fill-rule:nonzero;"/>
        <path d="M58.2,103.2C56.6,106.7 55,109.3 53.1,111.9C50.3,115.9 47.2,119.6 43.9,122.7C36.2,130.3 28.3,134.3 21.8,133.2L24.2,135.5C30,141 40.2,148.3 44.6,148.4L45.1,148.3C48.5,147.3 51.9,145.7 55.2,143.4L55.3,143.4C60.1,140.4 68,134.5 77.2,113.5L84.2,117.2L76.6,88.9L50.3,98.9L58.2,103.2Z" style="fill:rgb(244,244,245);fill-rule:nonzero;"/>
    </g>
</svg>
```
<ins>[File :](https://github.com/Data-Spirit/NMS_TC/blob/main/assets/nexusmods_badge.json)</ins> `nexusmods_badge.json` :⤵️

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

> [!NOTE]
> - 🎨 `0f0f10`: left-side color (black)
> - 🎨 `c07131`: right-side color (orange/gold)
>
> These colors match the Nexus Mods colors chosen for the badge.

### 9.1 **Raw address of the JSON hosted on the NMS_TC repo:**

```
https://raw.githubusercontent.com/Data-Spirit/NMS_TC/main/assets/nexusmods_badge.json
```

### 9.2 **Final badge URL**

Now that we have a `RAW` address for our `.json` file, we need to encode it in order to inject it into a shield.io URL.\
This can be done manually or directly via the shield.io website (see chapters 8-3a and 8-3b of the guide).

> [!NOTE]
> Simplified Method via Shield.io
> Encoding the URL via the shield.io website is much simpler and faster.\
> Go to [shield.io/endpoint](https://img.shields.io/badges/endpoint-badge) to create your custom badge URL.\
> To do this, you'll just need the `RAW` url of your `nexusmods_badge.json` file, and enter it in the site's `url — query` field.\

> [!TIP]
> Clicking on `show optional parameters` lets you customize the style, colors, etc.


Once this address is URL-encoded and injected into `img.shields.io/endpoint`,
with a few parameters added/overridden directly in the query string
(`style`, `logoSize`, `label`, `labelColor`, `color`),\
you'll get an address like this:

```
https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131
```

> [!TIP]
> A link with overridden query strings is handy because it lets anyone who wants to change the colors, the message, etc. on the fly (directly in the link), without touching the `.json` file.


### 9.3 **Adding It to the `README.md`.**

Two options are possible:

   **Simple version, classic clickable link (Markdown):**

   ```markdown
   [![My badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131)](https://URL_MOD_NEXUSMOD.com)
   ```

   **Centered version, clickable link (HTML — GitHub README compatible):**

   ```html
   <p align="center">
     <a href="https://URL_MOD_NEXUSMOD.com">
       <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131" alt="My badge">
     </a>
   </p>
   ```

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-10"></a>
## 10. 🎭 Badge Style Variants

**Examples:**

- `&style=plastic`
  [![Nexus_Mods](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=plastic&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131)](https://URL_MOD_NEXUSMOD.com)

- `&style=flat`
  [![Nexus_Mods](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131)](https://URL_MOD_NEXUSMOD.com)

- `&style=flat-square`
  [![Nexus_Mods](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=flat-square&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131)](https://URL_MOD_NEXUSMOD.com)

- `&style=for-the-badge`
  [![Nexus_Mods](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FData-Spirit%2FNMS_TC%2Fmain%2Fassets%2Fnexusmods_badge.json&style=for-the-badge&logoSize=auto&label=nexus&labelColor=0f0f10&color=c07131)](https://URL_MOD_NEXUSMOD.com)

<p align="right"><sub><a href="#top">⬆️</a></sub></p>

---

<a id="sec-11"></a>
## 11. 📚 Sources

<details>
<summary><b>🌐 External Links:</b></summary>

- [Endpoint Badge documentation](https://shields.io/badges/endpoint-badge)
- [Static Badge documentation](https://shields.io/badges/static-badge)
- [simple-icons icon library](https://simpleicons.org/)
- [List of simple-icons slugs](https://github.com/simple-icons/simple-icons/blob/master/slugs.md)
- [Directory of Shields-compatible endpoints (community examples)](https://github.com/badges/endpoint-badges-directory)
- [Nexus Mods Shield Mini-Guide](https://gist.github.com/radj307/e9a80731ee236cc67fb00b698e75201e)

</details>

<p align="right"><sub><a href="#top">⬆️</a></sub></p>
