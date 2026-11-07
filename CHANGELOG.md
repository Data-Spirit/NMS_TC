# Changelog

All notable changes to **NMS // TEXT CODES** are listed here, newest first.
Versions are those of the guide, `NMS_txt_code.html`. Each entry is a short summary: the detailed release notes are linked under each version.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/): **Added**, **Changed**, **Fixed**, **Removed**, **Security**.

---

## [Unreleased]

### Changed
- README v3.13: repository tree now lists `CHANGELOG.md` and `ROADMAP.md`, follows the Windows Explorer order (folders first, then files, alphabetically), and uses shorter descriptions so that no line overflows on GitHub.

---

## [2.3] — 2026-11-07 · *Reviewed from top to bottom*

First full review of the project (tools, code and docs) with the new review procedure. Same content, data and translations as 2.2. ≈ 451 KB.
[Release notes](https://github.com/Data-Spirit/NMS_TC/blob/main/docs/RELEASE_NOTES_v2.3.md)

### Added
- `docs/scripts/trans_script_5_test_mutations.py`: checks the check scripts themselves, by injecting 13 known faults into copies of the guide.
- `docs/prompts/prompt_add_language_NMS_TC.md`: an end-to-end prompt to add a new language (guide block, `<noscript>`, README, rest of the repository, checks, report).
- `CHANGELOG.md` and `ROADMAP.md`.
- Review system: `docs/revision.md` (procedure: when to review, which mode, what each tool detects and misses), `docs/prompts/prompt_revision_NMS_TC.md` (master prompt: three review types, tools, code and docs, and four modes, including a full review in that order) and `docs/pitfalls.md` (known pitfalls and their solutions).
- `_config.yml`: no GitHub Pages home page generated from the README (the site root returns a 404 on purpose; the guide stays online).

### Changed
- Add language prompt v1.1, READMEs v2.6 and README translation prompt v5.5: point to the new review system (the README prompt no longer cites `prompt_fix_allcode.md`, a file from another repository).
- README translation prompt v5.4: static anchors rule, corrected rule for GitHub heading anchors.
- Check scripts v1.1, after the first full review: script 1 now detects a duplicated or malformed language block (both were silently ignored), script 2 tests the tabs (mouse and keyboard) and a refused copy, script 3 tests `?lang=` and hostile values from the address and the storage, script 4 refuses a language missing from the file (it silently compared the default language); a missing file gives a clear message everywhere.
- Guide v2.3 (accessibility): decorative icons are hidden from screen readers, and the tab panels can be reached with the keyboard.
- Docs: repository tree in the README (v3.12), review procedure v1.2 and master review prompt v1.1 (fault-injection script), pitfalls v1.1, size of a language block (~14 KB) in the READMEs v2.7, scripts table of the HTML translation prompt (v4.4).

### Fixed
- READMEs (FR, EN, ES v2.5): the "Icons" and "About" links of the table of contents led nowhere (the emojis of those headings put an invisible character in GitHub's anchors); the four tab headings now have static anchors (`#tab-infos`, `#tab-colors`, `#tab-icons`, `#tab-about`).

### Removed
- `prompt_translation_transfert.md`, written for the old one-file-per-language guide (archived in `docs/_legacy/`).
- `index.html`, an empty placeholder page at the repository root.
- `prompt_code_review_NMS_TC.md`, replaced by the review system (archived in `docs/_legacy/`).

---

## [2.2] — 2026-11-07 · *Polished under the hood*

Full code review. Same content, data and translations as 2.1. ≈ 447 KB → ≈ 451 KB.
[Release notes](https://github.com/Data-Spirit/NMS_TC/blob/main/docs/_legacy/RELEASE_NOTES_v2.2.md)

### Fixed
- Phones: the "Tag texture" column of the icon tables was squeezed to zero width (the table now scrolls sideways).
- Phones: empty extra line in every color row.
- Phones: the language selector overlapped the small title above the guide name.
- An invalid saved language (such as `constructor`) could be accepted.
- A non-functional icon tag typed in lowercase (`circle_w`) was reported as unknown instead of suggesting the uppercase fix.
- The copy button showed ✓ even when the copy had failed (now ✗).
- The bold weight of the main font was not loaded (synthetic bold).

### Added
- Accessible tabs (ARIA pattern) with keyboard navigation (arrows, Home, End).
- `aria-label` on every copy button of the tables.
- A short message when JavaScript is disabled (FR, EN, ES).
- Spell-check and autocomplete disabled in the simulator and search fields.
- Project code review prompt: `docs/prompts/prompt_code_review_NMS_TC.md`.

### Changed
- Lighter work for the browser (no invisible blur, targeted transitions, faster color sort); two unused font weights no longer downloaded.
- Cleaner code: dead CSS removed, shared helpers, explained error handling, all comments in French.

### Security
- Built-in Content Security Policy: the page can only load its fonts.

---

## [2.1] — 2026-11-07 · *Original game icons*

[Release notes](https://github.com/Data-Spirit/NMS_TC/blob/main/docs/_legacy/RELEASE_NOTES_v2.1.md)

### Added
- `docs/assets/BANK_ICONS/SOURCES.csv`: provenance and match level of every icon.
- Probable texture paths for 4 icons still marked "to verify" (`FRIGPIRATE`, `ICON_NIN`, `FLIPVERT`, `MIRROR`).
- Icon bank archive (32 × 32, 64 × 64 and full-resolution originals).

### Changed
- The 129 displayed icons now come from the game's `.pak` archives (NMSModTool v1.1.0.0), embedded at 64 × 64; 97 are pixel-identical to their game texture. ≈ 359 KB → ≈ 447 KB.
- Icon table column renamed "Tag texture".
- Untinted-icon list updated (`CREATURE`, `INTERACTABLE`, `SENTINEL` can now be tinted; `PLAYER0` added).
- About tab rewritten in French, English and Spanish.
- README download button now always points to the latest release.

---

## [2.0] — 2026-10-22 · *One file, every language*

[Release notes](https://github.com/Data-Spirit/NMS_TC/blob/main/docs/_legacy/RELEASE_NOTES_v2.0.md)

### Added
- Multilingual guide in a single file: language selector, `?lang=` links, browser language detection, remembered choice, fallback to French.
- One JSON block per language (`i18n-xx`) with a `_meta` header; adding a language adds one block, with no code change.
- Simulator *(from the untagged 1.2 and 1.3 versions)*: copy button, clear button, detection of unknown, misspelled or wrongly cased tags with the fix suggested.
- Copy button on each real-world example.
- Translation prompts (`docs/prompts/`) and automated check scripts (`docs/scripts/`).

### Changed
- `NMS_txt_code_FR.html`, `_EN.html` and `_ES.html` replaced by `NMS_txt_code.html` (≈ 938 KB → ≈ 359 KB in total); the old files are archived in `docs/_legacy/`.
- New online address: `…/LANG/NMS_txt_code.html`.
- Category names and status badges stored as neutral identifiers, translated at display time.

### Security
- Every translated text is cleaned through a tag and attribute whitelist; the `?lang=` value is never inserted into the page.

---

## [1.1] — 2026-09-07 · *Spanish edition and accessibility*

Separate file per language: French guide 1.1 on 2026-09-07, English 1.1 on 2026-09-08, Spanish 1.1 on 2026-09-09.
[Release notes](https://github.com/Data-Spirit/NMS_TC/blob/main/docs/_legacy/pre_v2.0/RELEASE_v1.1.md)

### Added
- Spanish guide (`NMS_txt_code_ES.html`) and README.

### Changed
- Accessibility: labelled simulator field, `aria-label` on the search fields and the category filter.
- Code clean-up (explicit button types, font preconnect, reorganized data and lookups).

---

## [1.0] — 2026-08-31 · *First release*

### Added
- Interactive guide to No Man's Sky text tags, in French and English (one HTML file per language): 59 color tags, 145 icon tags in 12 described categories, live simulator with icon tinting, sortable and searchable tables, real-world container name examples, About tab.

---

[Unreleased]: https://github.com/Data-Spirit/NMS_TC/compare/v2.3...HEAD
[2.3]: https://github.com/Data-Spirit/NMS_TC/compare/v2.2...v2.3
[2.2]: https://github.com/Data-Spirit/NMS_TC/compare/v2.1...v2.2
[2.1]: https://github.com/Data-Spirit/NMS_TC/compare/v2.0...v2.1
[2.0]: https://github.com/Data-Spirit/NMS_TC/compare/v1.1...v2.0
[1.1]: https://github.com/Data-Spirit/NMS_TC/compare/v1.0...v1.1
[1.0]: https://github.com/Data-Spirit/NMS_TC/releases/tag/v1.0
