#!/usr/bin/env node
/*
 * Version du script : 1.1 (2026-11-07)
 * trans_script_2_test_behavior.js : test de comportement de NMS_txt_code.html dans une langue donnée.
 *
 * Aucun texte ni nombre n'est écrit en dur : les textes attendus (placeholder, aria-label, messages d'erreur de
 * balise, mot-témoin du gabarit…) sont lus dans le dictionnaire de la langue testée, et les quantités (exemples,
 * couleurs, icônes) dans la page elle-même (COLORS, ICONS, CONTAINER_EXAMPLES).
 *
 * Usage (jsdom doit être installé : `npm i jsdom` dans un dossier temporaire, puis NODE_PATH pointe vers son
 * node_modules) :
 *   NODE_PATH=/chemin/node_modules node trans_script_2_test_behavior.js --file NMS_txt_code.html --lang en [--ref precedent.html]
 *
 *   --lang : code de la langue à tester (fr, en, es…) ; le test la sélectionne dans la page.
 *   --ref  : version précédente du fichier (multilingue) ; sert au test de non-régression du rendu : toutes les entrées
 *            valides doivent donner un HTML identique dans cette langue.
 *
 * Code de sortie : 0 si tout passe, 1 sinon.
 * Limite : jsdom valide la logique, PAS le rendu visuel (alignement, couleurs, hauteurs).
 */
const fs = require('fs');
const { JSDOM } = require('jsdom');

const args = process.argv.slice(2);
const opt = n => { const i = args.indexOf('--' + n); return i >= 0 ? args[i + 1] : null; };
const file = opt('file'), lang = opt('lang'), refFile = opt('ref');
if (!file || !lang) { console.error('usage: --file NMS_txt_code.html --lang xx [--ref precedent.html]'); process.exit(2); }
for (const f of [file, refFile].filter(Boolean)) if (!fs.existsSync(f)) { console.error('fichier introuvable : ' + f); process.exit(2); }
let UI = {};   // rempli après le chargement de la page : textes lus dans la langue testée
const fmt = (t, v) => t.replace('{name}', v.name || '').replace('{fix}', v.fix || '');

const load = f => new JSDOM(fs.readFileSync(f, 'utf8'), { runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/' }).window;
const tick = () => new Promise(r => setTimeout(r, 20));
let fails = 0, passes = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); c ? passes++ : fails++; };

(async () => {
  const w = load(file), d = w.document;
  // attendre la fin du chargement (les blocs de langue sont en fin de page), puis choisir la langue testée
  await new Promise(r => { if(w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  if(!w.eval('I18N.order').includes(lang)){ console.error('langue « ' + lang + ' » absente du fichier (langues : ' + w.eval('I18N.order.join(", ")') + ')'); process.exit(2); }
  w.eval("applyLanguage('" + lang + "')");
  await tick();
  const E = (k, p) => w.eval('TA(' + JSON.stringify(k) + ',' + JSON.stringify(p || {}) + ')');
  UI = { placeholder: E('hero.sim_input.placeholder'), copy_aria: E('hero.copy.aria'), copy_title: E('hero.copy.title'),
         clear_aria: E('hero.sim_clear.aria'), clear_title: E('hero.sim_clear.title'),
         copy_prefix: E('copy.title', { text: '' }), template_word: E('copy.template_word'),
         msg_unknown_color: E('sim.err.unknown_color'), msg_unknown_icon: E('sim.err.unknown_icon'),
         msg_case_fix: E('sim.err.case_fix'), msg_keyword: E('sim.err.keyword') };
  let clip = null;
  Object.defineProperty(w.navigator, 'clipboard', { value: { writeText: async t => { clip = t; } }, configurable: true });
  const click = el => el.dispatchEvent(new w.MouseEvent('click', { bubbles: true }));
  const $ = id => d.getElementById(id);
  const input = $('sim-input'), box = $('sim-error-msg'), prev = $('sim-preview'), clear = $('sim-clear');
  const copy = d.querySelector('[data-copy-source="sim-input"]');
  const type = v => { input.value = v; input.dispatchEvent(new w.Event('input', { bubbles: true })); };
  const items = () => [...box.querySelectorAll('.sim-error-item')].map(e => e.textContent);
  const colors = w.eval('COLORS.map(c => c[0])'), icons = w.eval('ICONS.map(i => i[0])');
  const funcIcons = w.eval('Object.keys(ICON_MAP).filter(k => ICON_MAP[k])');   // fonctionnelles : valeur non vide
  const examples = w.eval('CONTAINER_EXAMPLES');

  // --- Interface (chaînes traduites) ---
  ok(!!copy && !!clear && !!input, 'éléments du simulateur présents (champ, copie, croix)');
  ok(input.placeholder === UI.placeholder, 'texte indicatif : « ' + input.placeholder + ' »');
  ok(copy.getAttribute('aria-label') === UI.copy_aria && copy.title === UI.copy_title, 'bouton copier : aria-label et title');
  ok(clear.getAttribute('aria-label') === UI.clear_aria && clear.title === UI.clear_title, 'croix : aria-label et title');

  // --- Copie dynamique du simulateur ---
  click(copy); await tick();
  ok(clip === input.value && clip.length > 0, 'copie du contenu initial du champ');
  type(`<${colors[0]}>abc</> <IMG>${funcIcons[0]}<>`); click(copy); await tick();
  ok(clip === `<${colors[0]}>abc</> <IMG>${funcIcons[0]}<>`, 'copie dynamique après modification');
  ok(copy.textContent === '✓' && copy.classList.contains('copied'), 'retour visuel ✓');
  ok(!clip.includes('<span'), 'copie = texte brut, pas l\'aperçu HTML');
  clip = 'SENTINELLE'; type(''); click(copy); await tick();
  ok(clip === 'SENTINELLE', 'champ vide : presse-papiers intact');

  // --- Copie refusée par le navigateur : ✗, jamais un ✓ trompeur ---
  Object.defineProperty(w.navigator, 'clipboard', { value: { writeText: async () => { throw new Error('refus'); } }, configurable: true });
  const execCopy = d.execCommand;
  d.execCommand = () => false;   // le repli échoue aussi
  type(`<${colors[0]}>x</>`); click(copy); await tick();
  ok(copy.textContent === '✗' && copy.classList.contains('copy-failed') && !copy.classList.contains('copied'), 'copie refusée : ✗ affiché, jamais ✓');
  d.execCommand = execCopy;
  Object.defineProperty(w.navigator, 'clipboard', { value: { writeText: async t => { clip = t; } }, configurable: true });

  // --- Onglets : souris et clavier (motif ARIA « tabs ») ---
  const tabs = [...d.querySelectorAll('.tab-btn')], lastTab = tabs.length - 1;
  const tabState = () => tabs.map(t => t.getAttribute('aria-selected') + ':' + t.tabIndex + ':' + d.getElementById(t.getAttribute('aria-controls')).classList.contains('active')).join(' ');
  const tabOn = i => tabs.map((t, j) => (j === i) + ':' + (j === i ? 0 : -1) + ':' + (j === i)).join(' ');
  const press = (el, key) => el.dispatchEvent(new w.KeyboardEvent('keydown', { key, bubbles: true }));
  click(tabs[1]);
  ok(tabs.length > 1 && tabState() === tabOn(1), 'onglet choisi à la souris : annoncé (aria-selected), seul atteignable (tabindex), panneau affiché');
  const steps = [];
  press(tabs[1], 'ArrowRight'); steps.push(tabState() === tabOn(2 > lastTab ? 0 : 2) && d.activeElement === tabs[2 > lastTab ? 0 : 2]);
  click(tabs[lastTab]); press(tabs[lastTab], 'ArrowRight'); steps.push(tabState() === tabOn(0));
  press(tabs[0], 'ArrowLeft'); steps.push(tabState() === tabOn(lastTab));
  press(tabs[lastTab], 'Home'); steps.push(tabState() === tabOn(0) && d.activeElement === tabs[0]);
  press(tabs[0], 'End'); steps.push(tabState() === tabOn(lastTab));
  ok(steps.every(Boolean), 'onglets au clavier : flèches (avec bouclage), Début, Fin, focus suivi : ' + steps.join(','));
  click(tabs[0]);

  // --- Exemples concrets ---
  const rows = d.querySelectorAll('.example-row-wrap');
  ok(rows.length === examples.length && rows.length > 0, `${examples.length} lignes d'exemples, chacune avec son bouton`);
  let allOk = true;
  for (let i = 0; i < rows.length; i++) {
    const b = rows[i].querySelector('.copy-btn');
    if (!b || !b.title.startsWith(UI.copy_prefix)) { allOk = false; continue; }
    click(b); await tick();
    if (clip !== examples[i]) { allOk = false; console.log('  écart ligne', i, clip, examples[i]); }
  }
  ok(allOk, 'chaque bouton copie le code exact de sa ligne et garde le préfixe « ' + UI.copy_prefix + ' »');
  ok(rows[0] && rows[0].children[1] === rows[0].querySelector('.copy-btn'), 'bouton placé à droite de la ligne');

  // --- Onglets Couleurs et Icônes ---
  const cb = d.querySelectorAll('#color-table-wrap .copy-btn'), ib = d.querySelectorAll('#icon-table-wrap .copy-btn');
  ok(cb.length === colors.length, `${colors.length} boutons dans l'onglet Couleurs`);
  ok(ib.length === icons.length, `${icons.length} boutons dans l'onglet Icônes`);
  // Les tableaux sont triés : on contrôle le format du gabarit et l'appartenance du tag aux données
  click(cb[0]); await tick();
  const mc = clip.match(new RegExp('^<([A-Z0-9_]+)>' + UI.template_word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '</>$'));
  ok(mc && colors.includes(mc[1]), 'onglet Couleurs : gabarit ' + clip);
  click(ib[0]); await tick();
  const mi = clip.match(/^<IMG>([A-Z0-9_]+)<>$/);
  ok(mi && icons.includes(mi[1]), 'onglet Icônes : ' + clip);

  // --- Erreurs de balise ---
  ok(box.hidden === true && !prev.innerHTML.includes('sim-error'), 'état initial : ligne d\'erreur cachée, aucun soulignement');
  const lowColor = colors[0].toLowerCase(), lowIcon = funcIcons[0].toLowerCase();
  type('<ZZZNOCOLOR>Texte</>');
  ok(items().join('|') === fmt(UI.msg_unknown_color, { name: 'ZZZNOCOLOR' }), 'couleur inconnue : ' + items());
  ok(prev.querySelector('.sim-error') && box.querySelector('.sim-err-name').textContent === 'ZZZNOCOLOR' && !box.querySelector('.sim-err-fix'), 'couleur inconnue : texte souligné, nom en rouge, pas de correction');
  type(`<${lowColor}>Texte</>`);
  ok(items().join('|') === fmt(UI.msg_case_fix, { name: lowColor, fix: colors[0] }), 'casse (couleur) : ' + items());
  ok(box.querySelector('.sim-err-fix').textContent === colors[0], 'casse (couleur) : correction affichée');
  type(`<ZZZNOCOLOR><IMG>${funcIcons[0]}<> Txt</>`);
  ok(items().join('|') === fmt(UI.msg_unknown_color, { name: 'ZZZNOCOLOR' }) && prev.querySelector('.sim-error img'), 'couleur inconnue devant icône : icône et texte soulignés');
  type('<IMG>ZZZNOICON<>');
  ok(items().join('|') === fmt(UI.msg_unknown_icon, { name: 'ZZZNOICON' }) && prev.querySelector('.sim-error .icon-inline').textContent === '?', 'icône inconnue : ' + items());
  type(`<IMG>${lowIcon}<>`);
  ok(items().join('|') === fmt(UI.msg_case_fix, { name: lowIcon, fix: funcIcons[0] }), 'casse (icône) : ' + items());
  type(`<img>${funcIcons[0]}<>`);
  ok(items().join('|') === fmt(UI.msg_keyword, { name: 'img', fix: 'IMG' }), 'mot-clé en minuscules : ' + items());
  type(`<${colors[0]}><img>${funcIcons[0]}<> x</>`);
  ok(items().includes(fmt(UI.msg_keyword, { name: 'img', fix: 'IMG' })), 'mot-clé en minuscules dans une combinaison');
  type('<ZZZ1>a</> <ZZZ1>b</> <ZZZ2>c</> <IMG>ZZZNOICON<>');
  ok(items().length === 3, 'doublons fusionnés : ' + JSON.stringify(items()));
  const nonFunc = icons.filter(i => !funcIcons.includes(i));
  if (nonFunc.length) {
    type(`<IMG>${nonFunc[0]}<>`);
    ok(box.hidden === true && prev.textContent.includes('?'), `icône listée mais non fonctionnelle (${nonFunc[0]}) : « ? » seul, pas de message`);
  } else console.log('SKIP aucune icône non fonctionnelle dans ce fichier');

  // --- Sécurité ---
  type('<constructor>x</> <toString>y</> <__proto__>z</>');
  ok(box.hidden === false && items().length === 3 && !prev.innerHTML.includes('undefined') && !prev.innerHTML.includes('function'), 'noms hérités (constructor, toString, __proto__) traités comme inconnus');
  type('<img src=x onerror=alert(1)><ZZZ1>x</>');
  ok(!prev.querySelector('img') && !box.querySelector('img') && !box.querySelector('script'), 'HTML injecté reste inerte');

  // --- Ligne cachée, croix ---
  type(`<${colors[0]}>ok</> <IMG>${funcIcons[0]}<>`);
  ok(box.hidden === true && box.innerHTML === '' && !prev.innerHTML.includes('sim-error'), 'redevenu valide : ligne cachée et vidée');
  type('<ZZZ1>a</>'); click(clear);
  ok(input.value === '' && box.hidden === true && prev.innerHTML === '' && d.activeElement === input, 'croix : champ vidé, aperçu vidé, ligne cachée, focus rendu');
  ok(!prev.contains(box) && prev.nextElementSibling === box, 'la ligne d\'erreur est hors du cadre d\'aperçu (sa hauteur ne dépend pas d\'elle)');
  ok(/\.sim-error-msg\[hidden\]\s*\{\s*display\s*:\s*none/.test(fs.readFileSync(file, 'utf8')), 'règle [hidden]{display:none} présente');

  // --- Non-régression du rendu (si --ref fourni) ---
  if (refFile) {
    const A = load(refFile);
    await new Promise(r => { if(A.document.readyState === 'complete') r(); else A.addEventListener('load', r); });
    if(typeof A.applyLanguage === 'function') A.eval("applyLanguage('" + lang + "')");
    const cases = [...examples, ...colors.map(c => `<${c}>${UI.template_word}</>`), ...icons.map(i => `<IMG>${i}<>`), 'texte brut', '<RED>non fermé', '<IMG>X', 'a <> b </> c', ''];
    for (const c of colors.slice(0, 20)) for (const i of funcIcons.slice(0, 15)) cases.push(`<${c}><IMG>${i}<> Txt</>`);
    // Les entrées volontairement invalides (icônes non fonctionnelles) donnent le même « ? » mais soulignement en moins ; on exclut ce qui est signalé
    let diff = 0, n = 0;
    for (const c of cases) {
      const errs = []; const b = w.renderNMSMarkup(c, { errors: errs });
      if (errs.length) continue; n++;
      if (A.renderNMSMarkup(c) !== b) diff++;
    }
    ok(diff === 0, `non-régression : ${n} entrées valides, rendu identique à la version de référence (écarts : ${diff})`);
  } else console.log('SKIP non-régression du rendu (pas de --ref)');

  console.log(`\n${passes} PASS, ${fails} FAIL` + (fails ? '' : ' : TOUT OK'));
  console.log('Rappel : rendu visuel, alignements et couleurs restent à valider à l\'oeil.');
  process.exit(fails ? 1 : 0);
})();
