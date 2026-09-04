# NMS // TEXT CODES — English Guide

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

**An interactive, self-contained, exhaustive guide to No Man's Sky's text formatting codes** — colors and icons, fully documented, tested, and packed into a single HTML file.

`NMS_txt_code_EN.html` · ~312 KB · no critical external dependencies · works offline

---

## Table of Contents

- [Why this project](#why-this-project)
- [Key feature: a 100% self-contained file](#key-feature-a-100-self-contained-file)
- [Key numbers](#key-numbers)
- [Interface structure](#interface-structure)
  - [Info tab](#-info-tab)
  - [Colors tab](#-colors-tab)
  - [Icons tab](#-icons-tab)
  - [About tab](#-about-tab)
- [The live simulator](#the-live-simulator)
- [The icon tinting technique](#the-icon-tinting-technique)
- [One-click copy](#one-click-copy)
- [Visual identity: a "meta" design](#visual-identity-a-meta-design)
- [How the icons were extracted and embedded](#how-the-icons-were-extracted-and-embedded)
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

The guide ships as **a single `.html` file**, with no companion folder required for it to work.

In practice, that means:

- **No installation.** Just open the file in any modern browser — that's it.
- **Freely movable and renamable.** The file has no relative-path dependency on any other file.
- **Works offline.** All the data (colors, icons, sorting logic, simulator) is embedded directly in the file — see [How the icons were extracted and embedded](#how-the-icons-were-extracted-and-embedded) for the technical details of how the images are packed in.
- **One non-critical external dependency**: fonts (Google Fonts, via CDN — *Rajdhani*, *IBM Plex Sans*, *JetBrains Mono*). Without an internet connection, rendering simply falls back to the browser's default system fonts — no functionality is lost.

This design choice (embedding everything rather than relying on an external assets folder) comes at a cost — a heavier file (~312 KB) than a version with external images — but it guarantees that a single file is always enough to make everything work, which matches the intended use case exactly: a tool you share, download, or move around without ever having to worry about missing files.

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

---

## Interface structure

The guide is organized into **4 tabs**, designed as a logical reading path: you learn the syntax before diving into the reference tables.

### 📘 Info tab

The guide's entry point. It brings together everything you need to know to use the tags, without having to dig around:

- **Complete syntax**, with dedicated syntax highlighting (more on that below) that clearly distinguishes the tag name, the user's free-form text, and the structural symbols (`<`, `>`, `<>`, `</>`, `IMG`).
- **Advanced technique: tinting an icon with a color tag** — explains how a color tag placed right before an `<IMG>` tag applies its color to the icon like a filter, with a dedicated **Important** callout covering the one real subtlety (where to place the closing tag to tint only the icon, or the icon *and* the text that follows it), plus a side-by-side visual comparison of both cases.
- **Warning callout** honestly noting that this behavior is community-observed but not officially documented, along with a list of known limitations (already-colored icons that can resist the tint, behavior not 100% guaranteed).
- **Tip callout** on the character limit of in-game text fields, recommending short tags where possible.
- **"Real-world examples" section**: ten headings actually used to organize in-game storage containers, each shown with its live visual render *and* its raw, syntax-highlighted code — the best practical demonstration of everything above.

### 🎨 Colors tab

A complete reference table of the 59 color tags, featuring:

- **A full-width color swatch** per row (rather than a small square), with a checkerboard background to correctly visualize the transparency of colors that have one.
- **Exact hex code** and **transparency percentage** (shown only when below 100%, to avoid cluttering the display unnecessarily).
- **Category** for each tag (Transmissions/Missions, Resources, Players, Companions, Galactic Map, etc.), right-aligned at the end of each row.
- **A dedicated header band**, visually distinct (its own background and border, vertical separators between columns) rather than plain floating text above the table.
- **Four clickable sort modes**: by name (alphabetical), by color (see below), by hex code (alphabetical), and by brightness (darkest to lightest). Clicking the same criterion a second time reverses the order.
- **A search bar** that instantly filters the list by tag name.

**The "Color" sort deserves its own explanation.** After several unsuccessful iterations with hue-based sorting algorithms (classic HSL, then hue+lightness, then grouping into perceptual families with hue-proximity thresholds), it turned out that no simple mathematical formula faithfully reproduced human perception of a "well-ordered" gradient — two colors with the exact same hue but very different saturation (a vivid blue versus a washed-out blue, for instance) never sorted satisfactorily through automated calculation alone. The solution was **a manually curated reference order**, color by color, by eye — more reliable than an algorithm at capturing nuances like a color's vividness, or slightly-tinted neutrals (ivory, off-white) that need to read as distinct from perfectly neutral grays.

### 🖼️ Icons tab

A complete reference table of the 145 icon tags, grouped into **12 categories** (Resources, Interface, Frigates, Inventory, Voice/Network, Loot, Platforms/Controls, Portal Glyphs, Class (C→S), Game Modes, Base Building, Non-functional), with the following for each icon:

- A **real thumbnail preview** of the icon (see the dedicated extraction section below — these aren't generic placeholder symbols, but the actual, cut-out game icons).
- The **exact tag name**.
- The original **texture file path** (an internal in-game `.DDS` reference), when it could be identified.
- A **status badge** where applicable: `duplicate` (the tag points to the exact same texture as another one, under a different name), `non-functional` (tag present in the data but with no assigned texture — likely a placeholder reserved on the developers' side), or `to verify` (texture path not confirmed in the available sources).

The **"Class (C→S)"** category illustrates a deliberate naming correction: originally called "Ship Classes," it was renamed with a subtext description clarifying that it's actually the game's generic quality rating notation (ships, multi-tools, frigates, weapons, technology) rather than a system specific to ships.

As with the Colors tab, a **search bar** and a **category filter** let you navigate the list quickly.

**Column alignment**: each category table uses fixed, identical column widths (`table-layout: fixed`), with the "Tag" column sized to the longest tag name in the entire guide (`BULLETPOINT_OFF`, 15 characters) — guaranteeing that no name is ever truncated and that alignment stays perfectly consistent from one category to the next, regardless of the category title's length or its rows' content.

### ℹ️ About tab

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

- Correctly recognizes and renders color tags, icon tags, and combinations of the two (including the tinting technique, see below).
- The icons shown are the actual icons extracted from the game (not approximations).
- Useful for composing a complex name (several tags combined) and checking the result before copying it into the game.

---

## The icon tinting technique

The simulator reproduces the technique of placing a color tag right before an `<IMG>` tag to tint the icon:

- Technically implemented via a **CSS mask** (`mask-image`): the color tag's color is applied as the background, and the icon PNG's alpha channel acts as the stencil — faithfully reproducing the behavior observed in-game (the color *replaces* the icon's pixels rather than blending over them).
- **Not every icon is tinted in the simulator.** A saturation analysis (backed up by manual visual review) identified about twenty icons that already carry a meaningful color of their own (class badges, the PlayStation icon, online-player diamonds, certain resource icons…). For readability, these are shown in their original color rather than flattened into a silhouette — with an explicit note pointing out that in-game, the tint may still genuinely apply and produce a different result than the preview.

---

## One-click copy

Every row in the Colors and Icons tables has a small dedicated button (⧉ symbol), positioned on the left of the row:

- **Colors**: copies a ready-to-use template, `<COLOR_NAME>Text</>`.
- **Icons**: copies the full syntax directly, `<IMG>ICON_NAME<>`.
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

This approach accounts for both the file's size (~312 KB, versus a few dozen KB for a text-only version) and its total portability: moving, renaming, or sharing the file never breaks icon rendering.

---

## Information reliability and known limitations

The guide aims to be upfront about what's confirmed and what isn't:

- The tagging system is **not officially documented anywhere** by Hello Games — all information comes from internal game configuration tables, in-game testing, and community sources.
- Color hex codes come directly from an exact table of RGBA/HEX values — with one exception (`TRANS_ANM`), whose exact color couldn't be confirmed in the most recent available sources.
- Tags marked `non-functional` or `to verify` are clearly flagged as such rather than presented with the same certainty as the rest.
- The icon tinting technique is presented as an observed behavior, not a universal guarantee.

---

## Compatibility and accessibility

- **Responsive**: layout adapted for narrow screens (secondary columns hidden on mobile in the color table, safety horizontal scroll on the icon tables).
- **Modern browsers**: Chrome, Firefox, Edge, Safari — relies on CSS Grid, `mask-image`, and the Clipboard API, all available in every recent version.
- **No data sent anywhere**: everything runs locally in the browser; no network connection is required after the initial font load.

---

## Tech stack

- **Vanilla HTML/CSS/JavaScript** — no framework, no build dependency, no compilation step.
- **Fonts**: Rajdhani (headings), IBM Plex Sans (body text), JetBrains Mono (code), via Google Fonts CDN.
- **No third-party libraries**: sorting, search, filtering, the simulator, and syntax highlighting are all native JavaScript written specifically for this guide.

---

## License

This guide is distributed under the [**CC BY-NC-SA 4.0**](https://creativecommons.org/licenses/by-nc-sa/4.0/) license. See the [`LICENSE.md`](../../LICENSE.md) file at the root of the repository for the full terms.

No Man's Sky and all associated assets, trademarks, and intellectual property belong to Hello Games and/or their respective rights holders. This guide is an unofficial community resource, not affiliated with Hello Games.
