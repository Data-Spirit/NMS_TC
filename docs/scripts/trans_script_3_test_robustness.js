#!/usr/bin/env node
/*
 * Version du script : 1.0 (2026-10-19)
 * trans_script_3_test_robustness.js : robustesse de NMS_txt_code.html à l'exécution (jsdom).
 *
 * Contrôle, sur des copies modifiées du fichier (le fichier lui-même n'est jamais touché) :
 *   A. sécurité : une traduction malveillante (img onerror, javascript:, onclick, iframe, svg) est neutralisée ;
 *   B. un bloc de langue illisible est ignoré sans gêner les autres langues ;
 *   C. une langue partielle se replie sur la langue source, et les clés manquantes sont signalées ;
 *   D. la langue du navigateur est détectée, la langue choisie est mémorisée ;
 *   E. la page fonctionne même si le navigateur bloque localStorage.
 *
 * Aucune valeur n'est écrite en dur : langues, clés et quantités sont lues dans le fichier testé.
 *
 * Usage (jsdom doit être installé : `npm i jsdom`, puis NODE_PATH vers son node_modules) :
 *   NODE_PATH=/chemin/node_modules node trans_script_3_test_robustness.js NMS_txt_code.html [--source fr] [--lang en]
 *   --source : langue source (défaut : fr) ; --lang : langue de traduction utilisée pour les tests (défaut : la première autre).
 * Code de sortie : 0 si tout passe, 1 sinon.
 */
const fs = require('fs'); const { JSDOM, VirtualConsole } = require('jsdom');
const args = process.argv.slice(2);
const opt = n => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : null; };
const FILE = args.find(a => !a.startsWith('--') && a !== opt('source') && a !== opt('lang'));
if (!FILE) { console.error('usage: node trans_script_3_test_robustness.js NMS_txt_code.html [--source fr] [--lang en]'); process.exit(2); }
const SRC = fs.readFileSync(FILE, 'utf8');
const SOURCE = opt('source') || 'fr';
const ids = [...SRC.matchAll(/<script type="application\/json" id="i18n-([\w-]+)">\s*\{/g)].map(m => m[1]);
const LANG = opt('lang') || ids.find(i => i !== SOURCE);
if (!LANG) { console.error('aucune langue de traduction dans le fichier'); process.exit(2); }

let fails = 0;
const ok = (c, m, d = '') => { console.log((c ? 'PASS ' : 'FAIL ') + m + (c || !d ? '' : ' : ' + d)); if (!c) fails++; };
const tick = (ms = 40) => new Promise(r => setTimeout(r, ms));
async function open(html, { languages, storage } = {}) {
  const errors = [], vc = new VirtualConsole(); vc.on('jsdomError', e => errors.push(String(e.message).slice(0, 80))); vc.on('error', (...a) => errors.push(a.join(' ').slice(0, 100)));
  const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/', virtualConsole: vc,
    beforeParse(w) {
      if (languages) Object.defineProperty(w.navigator, 'languages', { value: languages, configurable: true });
      if (storage === 'blocked') Object.defineProperty(w, 'localStorage', { get() { throw new Error('SecurityError'); }, configurable: true });
    } });
  await new Promise(r => { if (dom.window.document.readyState === 'complete') r(); else dom.window.addEventListener('load', r); }); await tick();
  dom.window.__errors = errors; return dom.window;
}
const inBlock = (html, id, fn) => { const i = html.indexOf('id="i18n-' + id + '"'); const j = html.indexOf('</script>', i); return html.slice(0, i) + fn(html.slice(i, j)) + html.slice(j); };
const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

(async () => {
  // --- référence : états de la page non modifiée
  const base = await open(SRC, { languages: [SOURCE] });
  const ORDER = base.eval('I18N.order.slice()');
  const NCOL = base.eval('COLORS.length'), NICON = base.eval('ICONS.length');
  const keyEls = base.eval('Array.from(document.querySelectorAll("[data-i18n]")).map(e => e.dataset.i18n)');
  // clés d'éléments dont la valeur est une simple chaîne sans balise, dans la langue de traduction
  const blockText = (() => { const i = SRC.indexOf('id="i18n-' + LANG + '"'); return SRC.slice(i, SRC.indexOf('</script>', i)); })();
  const simple = keyEls.filter(k => new RegExp('"' + reEsc(k) + '": "[^"<\\\\]{3,}"').test(blockText));
  if (simple.length < 2) { console.error('pas assez de clés simples pour les tests'); process.exit(2); }
  const [K1, K2] = simple;
  base.eval("applyLanguage('" + SOURCE + "')"); await tick();
  const srcText2 = base.document.querySelector('[data-i18n="' + K2 + '"]').textContent;
  console.log('(langue source : ' + SOURCE + ' ; langue de test : ' + LANG + ' ; langues du fichier : ' + ORDER.join(', ') + ')\n');

  console.log('--- A. sécurité : une traduction malveillante est neutralisée');
  const orig = blockText.match(new RegExp('"' + reEsc(K1) + '": "([^"]*)"'))[1];
  const payload = orig + '<img src=x onerror=\\"window.__pwn=1\\"><a href=\\"javascript:alert(1)\\" onclick=\\"window.__pwn2=1\\" class=\\"ok\\">x</a><iframe src=\\"//evil\\"></iframe><svg onload=\\"window.__pwn3=1\\"></svg><b onmouseover=\\"window.__pwn4=1\\">b</b>';
  const evil = inBlock(SRC, LANG, b => b.replace('"' + K1 + '": "' + orig + '"', '"' + K1 + '": "' + payload + '"'));
  let w = await open(evil, { languages: [LANG] });
  const el = w.document.querySelector('[data-i18n="' + K1 + '"]');
  ok(el.querySelector('img,iframe,svg,script') === null, 'aucune balise dangereuse (img, iframe, svg, script)', el.innerHTML);
  ok(el.querySelector('a') && !el.querySelector('a').hasAttribute('href') && !el.querySelector('a').hasAttribute('onclick'), 'lien : href javascript: et onclick supprimés', el.innerHTML);
  ok(el.querySelector('a').className === 'ok', 'attribut class autorisé conservé');
  ok(!el.querySelector('b').hasAttribute('onmouseover'), 'gestionnaire onmouseover supprimé');
  ok(!w.__pwn && !w.__pwn2 && !w.__pwn3 && !w.__pwn4, 'aucun code de la traduction ne s\'est exécuté');
  ok(el.textContent.startsWith(orig), 'le texte légitime est conservé');

  console.log('\n--- B. un bloc de langue illisible n\'affecte pas les autres');
  const broken = inBlock(SRC, LANG, b => b.replace('"_meta":', '"_meta" "oops":'));
  w = await open(broken, { languages: [LANG] });
  const expected = ORDER.filter(c => c !== LANG);
  ok(w.eval('I18N.order.join(",")') === expected.join(','), 'langues chargées : ' + expected.join(', '), w.eval('I18N.order.join(",")'));
  ok(w.document.getElementById('lang-select').options.length === expected.length, 'le sélecteur ne propose que les langues lisibles');
  ok(w.document.documentElement.lang === SOURCE, 'la page fonctionne dans la langue source malgré l\'erreur');
  ok(w.document.querySelectorAll('#color-table-wrap .color-row-wrap').length === NCOL && w.document.querySelectorAll('#icon-table-wrap tbody tr').length === NICON,
     'tableaux rendus (' + NCOL + ' couleurs, ' + NICON + ' icônes)');

  console.log('\n--- C. langue partielle : repli sur la langue source, signalé');
  const partial = SRC.replace('</body>', '<script type="application/json" id="i18n-xx">{"_meta":{"native_name":"Testish","flag":"🏳️","lang_code":"xx"},"' + K1 + '":"INFO-XX"}</script>\n</body>');
  w = await open(partial, { languages: [LANG] });
  w.eval("applyLanguage('xx')"); await tick();
  ok(w.document.querySelector('[data-i18n="' + K1 + '"]').textContent.trim() === 'INFO-XX', 'clé présente : traduite');
  ok(w.document.querySelector('[data-i18n="' + K2 + '"]').textContent === srcText2, 'clé absente : repli sur la langue source');
  ok(w.eval('Array.from(I18N.missing).filter(k => k.startsWith("xx:")).length') > 10, 'clés manquantes listées dans I18N.missing', String(w.eval('I18N.missing.size')));
  ok(w.eval('I18N.order.join(",")') === ORDER.concat('xx').join(',') && w.document.getElementById('lang-select').options.length === ORDER.length + 1, 'le sélecteur propose automatiquement la nouvelle langue');
  ok(w.document.querySelector('#lang-select option[value="xx"]').textContent.includes('Testish'), 'libellé du sélecteur lu dans _meta');

  console.log('\n--- D. détection de la langue du navigateur');
  const cases = [[[LANG + '-GB', SOURCE], LANG, LANG + '-GB (variante régionale) → ' + LANG], [['zz', SOURCE + '-CA'], SOURCE, 'zz puis ' + SOURCE + '-CA → ' + SOURCE],
                 [['zz'], SOURCE, 'langue inconnue → langue par défaut (' + SOURCE + ')'], [[SOURCE], SOURCE, SOURCE + ' → ' + SOURCE]];
  for (const [langs, expect, label] of cases) {
    w = await open(SRC, { languages: langs });
    ok(w.document.documentElement.lang === expect && w.document.getElementById('lang-select').value === expect && w.__errors.length === 0, label, w.document.documentElement.lang + ' ' + w.__errors.join(' | '));
  }
  w = await open(SRC, { languages: [LANG] });
  w.document.getElementById('lang-select').value = SOURCE; w.document.getElementById('lang-select').dispatchEvent(new w.Event('change')); await tick();
  ok(w.document.documentElement.lang === SOURCE && w.localStorage.getItem('nmstc-lang') === SOURCE, 'le changement via le sélecteur est appliqué et mémorisé');

  console.log('\n--- E. stockage bloqué par le navigateur');
  w = await open(SRC, { languages: [LANG], storage: 'blocked' });
  ok(w.document.documentElement.lang === LANG && w.document.querySelectorAll('#color-table-wrap .color-row-wrap').length === NCOL, 'la page fonctionne sans localStorage');
  ok(w.__errors.length === 0, 'aucune erreur JavaScript levée au chargement', w.__errors.join(' | '));
  w.document.getElementById('lang-select').value = SOURCE; w.document.getElementById('lang-select').dispatchEvent(new w.Event('change')); await tick();
  ok(w.document.documentElement.lang === SOURCE, 'le changement de langue fonctionne aussi sans localStorage');
  ok(w.__errors.length === 0, 'aucune erreur JavaScript levée au changement de langue', w.__errors.join(' | '));
  console.log(fails ? `\n${fails} ÉCHEC(S)` : '\nTOUT OK');
  console.log('Rappel : ces tests valident la logique dans jsdom, pas le comportement des vrais navigateurs.');
  process.exit(fails ? 1 : 0);
})();
