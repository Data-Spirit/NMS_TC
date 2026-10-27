<!-- File version 
> Version: 2.2
> Last modified: 2026-10-27
-->
<!-- Translation parameters
> source_file: README_FR.md v2.2 (md5 cd377f8f5d862542265d60d9aac220ac)
> target_language: English
> target_variant: neutral/standard
> lang_code: EN
> tone: compromise (sober, key imagery kept)
> fidelity_style: idiomatic
> companion_html_guide: NMS_txt_code.html v2.0, i18n-en block (md5 c26672e58a3d43832ea06d02149368e9)
> translated_on: 2026-10-27
-->

<h1 align="center">NMS // TEXT CODES — Design Documentation</h1>

<p align="center"><em>README in English: design documentation for the interactive guide</em></p>

<!-- CENTERED BADGES -->
<p align="center">

  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" alt="License: CC BY-NC-SA 4.0">
  </a>
  
  <a href="https://github.com/Data-Spirit">
    <img src="https://img.shields.io/badge/README%20%3A-README_EN.md-blue?style=flat&logo=mdbook&logoColor=white&logoSize=auto&label=README%20%3A&labelColor=black&color=darkcyan" alt="README : README_EN.md">
  </a>
  
  <a href="https://github.com/Data-Spirit/NMS_TC">
    <img src="https://img.shields.io/badge/URL%20%3A-NMS_TC-blue?style=flat&logo=shieldsdotio&logoColor=white&logoSize=auto&label=Repo%20%3A&labelColor=grey&color=mediumseagreen" alt="Site">
  </a>
  
</p>

**An interactive, self-contained, exhaustive guide to No Man's Sky's text formatting codes** — colors and icons, fully documented, tested, and packed into a single HTML file. It is **available in several languages**, thanks to a language selector built into the file.

`NMS_txt_code.html` · ~359 KB · multilingual · no critical external dependencies · works offline

> **Who's who?**
> - **The interactive guide** (`NMS_txt_code.html`) is the product: a self-contained, **multilingual** HTML file with a built-in language selector.
> - **This README** documents its design. It is written **in English**. There is one version per language (`README_EN.md`, etc.). **Only the interactive guide is multilingual, not the READMEs.**

---

## Table of Contents

- [Why this project](#why-this-project)
- [Key feature: a 100% self-contained file](#key-feature-a-100-self-contained-file)
- [The interactive guide is multilingual](#the-interactive-guide-is-multilingual)
- [Key numbers](#key-numbers)
- [Interface structure](#interface-structure)
  - [Info Tab](#-info-tab)
  - [Colors Tab](#-colors-tab)
  - [Icons Tab](#-icons-tab)
  - [About Tab](#-about-tab)
- [The live simulator](#the-live-simulator)
- [The icon tinting technique](#the-icon-tinting-technique)
- [One-click copy](#one-click-copy)
- [Visual identity: a "meta" design](#visual-identity-a-meta-design)
- [How the icons were extracted and embedded](#how-the-icons-were-extracted-and-embedded)
- [Adding or updating a language in the interactive guide](#adding-or-updating-a-language-in-the-interactive-guide)
- [Information reliability and known limitations](#information-reliability-and-known-limitations)
- [Compatibility and accessibility](#compatibility-and-accessibility)
- [Tech stack](#tech-stack)
- [License](#license)

---

## Why this project

No Man's Sky lets players customize names (bases, ships, frigates, multi-tools, storage containers, star systems…) through a text tag system — coloring and icons — that Hello Games has **never officially documented anywhere**. The information exists, but it's scattered: screenshots of internal configuration tables, players' trial-and-error experiments on forums, and partial, sometimes outdated community guides.

**NMS_TC** compiles, verifies, corrects, and presents this information in a single, structured, directly usable format — built to work as both reference documentation and a live tool you keep open while playing.

---

## Key feature: a 100% self-contained file

The guide ships as **a single `.html` file** (all languages included), with no companion folder required for it to work.

In practice, that means:

- **No installation.** Just open the file in any modern browser — that's it.
- **Freely movable and renamable.** The file has no relative-path dependency on any other file.
- **Works offline.** All the data (colors, icons, sorting logic, simulator, texts in every language) is embedded directly in the file — see [How the icons were extracted and embedded](#how-the-icons-were-extracted-and-embedded) for the technical details of how the images are packed in.
- **One non-critical external dependency**: fonts (Google Fonts, via CDN — *Rajdhani*, *IBM Plex Sans*, *JetBrains Mono*). Without an internet connection, rendering simply falls back to the browser's default system fonts — no functionality is lost.

This design choice (embedding everything rather than relying on an external assets folder) comes at a cost — a heavier file (~359 KB) than a version with external images — but it guarantees that a single file is always enough to make everything work, which matches the intended use case exactly: a tool you share, download, or move around without ever having to worry about missing files.

---

## The interactive guide is multilingual

The interactive guide exists in **several languages within a single file**: there is no separate file per language.

- **Language selector**: at the top right of the screen, a menu lists each language under its own name, preceded by a flag (for example "Français", "English", "Español"). The choice applies immediately to the whole guide: texts, tables, simulator messages.
- **Automatically chosen language**: a language requested in the address (`?lang=es`) takes priority; otherwise the guide uses the saved choice, then the browser's language if it is available, otherwise French. The displayed language is then remembered in the browser.
- **Direct link to a language**: each time the language changes, the guide's address is updated (`…/NMS_txt_code.html?lang=en`); just copy it to share the guide in the displayed language. An unknown value is simply ignored. This link applies to the online version.
- **Currently available languages**: **French** (the source language), **English**, and **Spanish**.
- **Missing text in a language**: the French version is shown in its place, never an error message.

> **Important distinction.** Only the **interactive guide** is multilingual. This README is written in a single language; there is one version per language (`README_FR.md`, `README_EN.md`…), each translated separately.

> **🔧 Technical detail:** each language is a JSON data block placed at the end of the file, and the guide's texts are identified by keys. Formatting (bold, italics, code, links…) is preserved, but sanitized through a whitelist of tags: a translation therefore can't introduce active code. An unreadable language block is ignored without affecting the others. Each language adds about 13 KB to the file. The `?lang=` value in the address is only compared with the available languages; it is never inserted into the page.

---

## Key numbers

| | |
|---|---|
| 🎨 Documented color tags | **59** |
| 🖼️ Documented icon tags | **145** |
| 📂 Icon categories | **12** |
| 🔁 Duplicate textures identified | **21** |
| ⛔ Tags listed but non-functional | **16** |
| ❔ Tags with unconfirmed texture path | **12** |
| 🖼️ Icons embedded as base64 in the file | **145 / 145** |
| 📝 Real-world usage examples | **10** |
| 🌍 Languages in the interactive guide | **3** |
| 🔤 Texts to translate (translation keys) | **116** |

---

## Interface structure

The guide is organized into **4 tabs**, designed as a logical reading path: you learn the syntax before diving into the reference tables. A **language selector**, at the top right, changes the language of the entire interactive guide.

### 📘 Info Tab

The guide's entry point. It brings together everything you need to know to use the tags, without having to dig around:

- **Complete syntax**, with dedicated syntax highlighting (more on that below) that clearly distinguishes the tag name, the user's free-form text, and the structural symbols (`<`, `>`, `<>`, `</>`, `IMG`).
- **Advanced technique: tinting an icon with a color tag** — explains how a color tag placed right before an `<IMG>` tag applies its color to the icon like a filter, with a dedicated **Important** callout covering the one real subtlety (where to place the closing tag to tint only the icon, or the icon *and* the text that follows it), plus a side-by-side visual comparison of both cases.
- **Warning callout** honestly noting that this behavior is community-observed but not officially documented, along with a list of known limitations (already-colored icons that can resist the tint, behavior not 100% guaranteed).
- **Tip callout** on the character limit of in-game text fields, recommending short tags where possible.
- **"Real-world examples" section**: ten headings actually used to organize in-game storage containers, each shown with its live visual render *and* its raw, syntax-highlighted code, with a copy button to the right of each row — the best practical demonstration of everything above.

### 🎨 Colors Tab

A complete reference table of the 59 color tags, featuring:

- **A full-width color swatch** per row (rather than a small square), with a checkerboard background to correctly visualize the transparency of colors that have one.
- **Exact hex code** and **transparency percentage** (shown only when below 100%, to avoid cluttering the display unnecessarily).
- **Category** for each tag (Transmissions / Missions, Resources, Players, Companions, Galactic Map, etc.), right-aligned at the end of each row.
- **A dedicated header band**, visually distinct (its own background and border, vertical separators between columns) rather than plain floating text above the table.
- **Four clickable sort modes**: by name (alphabetical), by color (see below), by hex code (alphabetical), and by brightness (darkest to lightest). Clicking the same criterion a second time reverses the order.
- **A search bar** that instantly filters the list by tag name.

**The "Color" sort deserves its own explanation.** After several unsuccessful iterations with hue-based sorting algorithms (classic HSL, then hue+lightness, then grouping into perceptual families with hue-proximity thresholds), it turned out that no simple mathematical formula faithfully reproduced human perception of a "well-ordered" gradient — two colors with the exact same hue but very different saturation (a vivid blue versus a washed-out blue, for instance) never sorted satisfactorily through automated calculation alone. The solution was **a manually curated reference order**, color by color, by eye — more reliable than an algorithm at capturing nuances like a color's vividness, or slightly-tinted neutrals (ivory, off-white) that need to read as distinct from perfectly neutral grays.

> **🔧 Technical detail:** unlike the "Color" sort, the **brightness** sort does rely on an automated calculation — the standard ITU-R BT.601 perceptual luminance formula (`0.299×R + 0.587×G + 0.114×B`), which weights green more heavily than red and blue, matching the human eye's sensitivity to each color component.

### 🖼️ Icons Tab

A complete reference table of the 145 icon tags, grouped into **12 categories** (Resources, Interface, Frigates, Inventory, Voice / Network, Loot, Platforms / Controls, Portal Glyphs, Class (C→S), Game Modes, Base Building, Non-functional), with the following for each icon:

- A **real thumbnail preview** of the icon (see the dedicated extraction section below — these aren't generic placeholder symbols, but the actual, cut-out game icons).
- The **exact tag name**.
- The original **texture file path** (an internal in-game `.DDS` reference), when it could be identified.
- A **status badge** where applicable: `duplicate` (the tag points to the exact same texture as another one, under a different name), `non-functional` (tag present in the data but with no assigned texture — likely a placeholder reserved on the developers' side), or `to verify` (texture path not confirmed in the available sources).

The **"Class (C→S)"** category illustrates a deliberate naming correction: originally called "Ship Classes," it was renamed with a subtext description clarifying that it's actually the game's generic quality rating notation (ships, multi-tools, frigates, weapons, technology) rather than a system specific to ships.

As with the Colors tab, a **search bar** and a **category filter** let you navigate the list quickly.

**Column alignment**: each category table uses fixed, identical column widths (`table-layout: fixed`), with the "Tag" column sized to the longest tag name in the entire guide (`BULLETPOINT_OFF`, 15 characters) — guaranteeing that no name is ever truncated and that alignment stays perfectly consistent from one category to the next, regardless of the category title's length or its rows' content.

### ℹ️ About Tab

The guide's context and methodological transparency:

- A reminder that the tagging system isn't officially documented.
- Technical detail on the icon bank (how the 145 icons are embedded, and where to find the individual PNG files if needed elsewhere).
- An explicit list of the duplicate textures identified, with examples.
- A note on portal glyphs (`PR_0` through `PR_15`) — confirmed functional in-game by the community (used to rename star systems with the glyph of their portal address).
- A list of non-functional tags listed in the data but with no assigned texture.
- Sources used to compile the guide.

---

## The live simulator

Located at the top of the page and visible from any tab, the simulator lets you **type a combination of tags and see the result instantly**, without having to go back into the game to check:

- **A copy button** (⧉) to the right of the field copies the typed code in one click, ready to paste into the game (see [One-click copy](#one-click-copy)).
- **A clear button** (×), placed inside the field, empties it and gives it back focus so you can start over. It disappears on its own when the field is empty.
  - The preview frame just below keeps the same height whether it contains a preview or is empty: it stays black and doesn't shrink when you clear the field (its minimum height is equivalent to one line of content).
- **A discreet placeholder text**, in italics, appears in the empty field to guide newcomers.
- Correctly recognizes and renders color tags, icon tags, and combinations of the two (including the tinting technique, see below).
- **Tag errors are flagged**: an unknown color or icon (for example `REDD` instead of `RED`) is underlined in red with a wavy line, directly in the preview. Below the preview, a small box per error says which one it is, with the faulty name in red and, when one exists, the correct name in green. This line only appears when there is an error: with no error, nothing is displayed and the preview's height doesn't change.
- **Case is checked, just like in the game**: `red`, `fuel` or `<img>` in lowercase are flagged with the fix to apply (`RED`, `FUEL`, `IMG`), whereas they previously displayed with no warning at all, or as plain text.
- The icons shown are the actual icons extracted from the game (not approximations).
- Useful for composing a complex name (several tags combined) and checking the result before copying it into the game.
- **Input text is always sanitized before display**: pasting any text into the field, even deliberately "broken" or copied from an untrusted source, can never interfere with the page itself.

> **🔧 Technical detail:** the typed text is first fully escaped (HTML special characters are converted), and `<COLOR>` and `<IMG>...<>` tag recognition runs on that escaped version rather than on the raw text. Anything not recognized as a genuine NMS tag is therefore displayed as inert text, never interpreted as active HTML. Tag lookup ignores case only so that capitalization mistakes can be spotted; validity itself stays strict (only uppercase names exist), and names are looked up in the color and icon tables without ever touching the internal properties of JavaScript objects.

---

## The icon tinting technique

The simulator reproduces the technique of placing a color tag right before an `<IMG>` tag to tint the icon:

- Technically implemented via a **CSS mask** (`mask-image`): the color tag's color is applied as the background, and the icon PNG's alpha channel acts as the stencil — faithfully reproducing the behavior observed in-game (the color *replaces* the icon's pixels rather than blending over them).
- **Not every icon is tinted in the simulator.** A saturation analysis (backed up by manual visual review) identified about twenty icons that already carry a meaningful color of their own (class badges, the PlayStation icon, online-player diamonds, certain resource icons…). For readability, these are shown in their original color rather than flattened into a silhouette — with an explicit note pointing out that in-game, the tint may still genuinely apply and produce a different result than the preview.

---

## One-click copy

The same dedicated button (⧉ symbol) appears in four places in the guide:

- **Colors**: a button to the left of each table row copies a ready-to-use template, `<NAME_COLOR>Text</>`.
- **Icons**: a button to the left of each table row copies the full syntax directly, `<IMG>NAME_ICON<>`.
- **Real-world examples** (Info tab): a button to the right of each of the ten rows copies the example's raw code, which is always the same.
- **Simulator**: a slightly larger button, to the right of the input field and the same height as it, copies the code exactly as currently typed (the raw text, not the preview). Its content is read at the moment of the click, so it always follows the changes made in the field, with nothing to synchronize. If the field is empty, the click does nothing, so the clipboard isn't overwritten with nothing.
- **Immediate visual feedback**: the button briefly turns into a checkmark (✓) for about 1.4 seconds to confirm the copy.
- Relies on the `navigator.clipboard` API, with an automatic fallback (`document.execCommand`) for older browsers that don't support it.

---

## Visual identity: a "meta" design

A deliberate design choice: rather than defining an arbitrary interface palette, **the interface's own accent colors are borrowed directly from the game's real color tags** documented in the guide:

| Interface use | Color | Original NMS tag |
|---|---|---|
| Section headers, active tab | Cyan | `VISOR` |
| "Tip" callout, general accents | Orange | `COMMODITY` |
| Highlights, underlined text | Emerald green | *(custom shade, consistent with the game's green family)* |
| "Important" callout | Purple | `SPECIAL` |
| Warning callout | Red | `TRANS_WAR` |

This choice creates a direct thematic through-line between the documented content and the visual vocabulary used to present it — the guide literally dresses itself in the colors it documents.

---

## How the icons were extracted and embedded

The 145 icons aren't generic placeholder symbols: they are the **actual icons from the game**, individually extracted from several screenshots (internal configuration tables and in-game interface captures), then cleaned up and embedded:

1. **Coordinate mapping.** Each icon was precisely located (pixel coordinates) within its source image, with manual recalibration where the source grids weren't perfectly regular.
2. **Background removal.** The background was stripped using color-distance thresholding (converted into an alpha channel), with connected-component isolation to eliminate fragments of neighboring icons bleeding in from screenshots where icons were tightly packed together.
3. **Manual quality control.** Several passes of visual inspection caught and fixed poorly cropped, off-center icons, or ones contaminated by residue from an adjacent icon — until all 145 icons rendered cleanly.
4. **Encoding.** Each PNG (transparent background) is encoded in **base64** and stored in a JavaScript object (`ICON_DATA`) mapping each filename to a `data:image/png;base64,...` string, used directly as the `src` attribute of `<img>` tags — exactly as if the image were hosted online, except it's physically present inside the file.

This approach accounts for both the file's size (~359 KB, versus a few dozen KB for a text-only version) and its total portability: moving, renaming, or sharing the file never breaks icon rendering.

This data block (`ICON_DATA`) is deliberately isolated at the very end of the script, separate from all the JavaScript logic that precedes it (only the language blocks, simple JSON data, come after) — an organization designed so that reading the code is never drowned out by these few thousand lines of binary text, and to make it easier for the community to add icons in the future.

> **🔧 Technical detail:** in JavaScript, a constant only needs to be declared before it's used at runtime — not necessarily before the functions that reference it in their code. `ICON_DATA` can therefore be placed at the very bottom of the script without breaking anything, as long as it stays declared before the page initialization, which runs once loading is complete.

The 16 tags listed as non-functional aren't all simply empty entries: some of them (generic gamepad-button icons) actually have their image already present as base64 in `ICON_DATA`, without being linked to it in the icon table.

> **🔧 Technical detail:** these images are kept in reserve rather than deleted, in case Hello Games ever assigns them an official in-game texture — linking them would then become a simple one-line fix, without having to re-extract or re-encode anything.

---

## Adding or updating a language in the interactive guide

Translating the interactive guide requires **no new file**: a language is simply one more block of text inside `NMS_txt_code.html`.

**Two distinct jobs, not to be confused:**

| What | Where | How |
|---|---|---|
| **The interactive guide's language block** | inside `NMS_txt_code.html` | prompt `prompt_translation_HTML_GUIDE_LANG.md`, checked by the scripts in the `docs/scripts/` folder |
| **This README in another language** | a separate file (`README_EN.md`…) | prompt `prompt_translation_README_LANG.md` |

The working principle:

1. **French is the source language.** Every new feature is first written in French, with its texts identified by keys.
2. **Only what's missing or changed gets translated.** The `trans_script_1_check_keys.py` script lists the keys to translate for a given language.
3. **Each language block starts with a `_meta` field** that stores the language's name, its flag, and the translation parameters chosen (tone, variant, fidelity).
4. **Automated checks** verify the keys, tags, code examples, behavior, and robustness of the guide in each language.

---

## Information reliability and known limitations

The guide aims to be upfront about what's confirmed and what isn't:

- The tagging system is **not officially documented anywhere** by Hello Games — all information comes from internal game configuration tables, in-game testing, and community sources.
- Color hex codes come directly from an exact table of RGBA/HEX values — with one exception (`TRANS_ANM`), whose exact color couldn't be confirmed in the most recent available sources.
- Tags marked `non-functional` or `to verify` are clearly flagged as such rather than presented with the same certainty as the rest.
- The icon tinting technique is presented as an observed behavior, not a universal guarantee.
- **Right-to-left** languages (Arabic, Hebrew…) are not yet supported by the interactive guide: the display would be incorrect.
- The selector's **flags** are emoji: some systems may display two letters instead of the flag.

---

## Compatibility and accessibility

- **Responsive**: layout adapted for narrow screens (secondary columns hidden on mobile in the color table, safety horizontal scroll on the icon tables).
- **Modern browsers**: Chrome, Firefox, Edge, Safari — relies on CSS Grid, `mask-image`, and the Clipboard API, all available in every recent version.
- **Basic accessibility**: both search bars and the category filter are properly announced to screen readers (`aria-label`), the simulator field is tied to a real `<label>` rather than plain floating text, and the simulator's copy button and clear button carry an `aria-label` too. The **language selector** is a native menu labeled for screen readers, and the page's `lang` attribute follows the chosen language.
- **No data sent anywhere**: everything runs locally in the browser; no network connection is required after the initial font load. Only the **language choice** is remembered, locally, in the browser; it is never sent.

---

## Tech stack

- **Vanilla HTML/CSS/JavaScript** — no framework, no build dependency, no compilation step.
- **Fonts**: Rajdhani (headings), IBM Plex Sans (body text), JetBrains Mono (code), via Google Fonts CDN.
- **No third-party libraries**: sorting, search, filtering, the simulator, and syntax highlighting are all native JavaScript written specifically for this guide.
- **In-house language system**: translations are JSON dictionaries embedded in the file, read by native JavaScript, with no internationalization library.
- **Optimized font loading**: two `<link rel="preconnect">` tags open the connection to Google Fonts' domains before the stylesheet even loads, reducing perceived latency on first render.
- **Non-blocking images**: the 145 embedded icons use `decoding="async"`, so their decoding never delays the rendering of the rest of the page.
- **Code validated with standard tools**: the HTML passes `html-validate` (recommended preset), apart from two rules that flag "empty" headings and buttons in the source file, disabled by design since their text is inserted at load time depending on the language, and the CSS has been audited with Stylelint with no substantive issues (only formatting preferences, deliberately left as-is for stylistic consistency).

---

## License

This guide is distributed under the [**CC BY-NC-SA 4.0**](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. See the [`LICENSE.md`](../../LICENSE.md) file at the root of the repository for the full terms.

No Man's Sky and all associated assets, trademarks, and intellectual property belong to Hello Games and/or their respective rights holders. This guide is an unofficial community resource, not affiliated with Hello Games.
