#!/usr/bin/env node
/*
 * Version du script : 1.0 (2026-10-19)
 * trans_script_4_test_render.js : équivalence de rendu entre deux versions de NMS_txt_code.html (jsdom).
 *
 * Compare, dans une langue donnée, le rendu d'une version de RÉFÉRENCE (ex. la version publiée) à celui d'une version
 * CANDIDATE (ex. après une modification du code), à travers une série de scénarios d'interaction : simulateur,
 * recherches, tris, filtre, onglets, bascule de langue et retour. Utile pour prouver qu'un changement de code n'a
 * pas modifié l'affichage. Les attributs data-i18n et le sélecteur de langue sont ignorés ; les espaces sont normalisés.
 *
 * Usage (jsdom doit être installé ; NODE_PATH vers son node_modules) :
 *   NODE_PATH=/chemin/node_modules node trans_script_4_test_render.js reference.html candidat.html fr
 * Code de sortie : 0 si les rendus sont identiques, 1 sinon.
 * Limite : jsdom valide la structure produite, PAS l'aspect visuel (couleurs, alignements, hauteurs).
 */
const fs = require('fs');
const { JSDOM } = require('jsdom');
const [,, origFile, newFile, lang] = process.argv;
const load = f => new JSDOM(fs.readFileSync(f, 'utf8'), { runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/' }).window;
const tick = () => new Promise(r => setTimeout(r, 30));
const INLINE = new Set(['STRONG','EM','B','I','CODE','A','SPAN','BR']);

function canon(w){
  const d = w.document, toks = [];
  const pushText = s => { if(toks.length && typeof toks[toks.length-1] === 'string') toks[toks.length-1] += s; else toks.push(s); };
  (function walk(n){
    n.childNodes.forEach(c => {
      if(c.nodeType === 3) pushText(c.nodeValue);
      else if(c.nodeType === 1){
        if(c.classList.contains('lang-switch') || c.tagName === 'SCRIPT' || c.tagName === 'STYLE') return;
        const attrs = Array.from(c.attributes).filter(a => a.name !== 'data-i18n' && a.name !== 'data-i18n-attr' && !(c.tagName === 'OPTION' && a.name === 'value' && a.value !== 'ALL')).map(a => a.name + '=' + a.value).sort();
        if(c.tagName === 'SPAN' && c.hasAttribute('data-i18n') && attrs.length === 0){ walk(c); return; }
        toks.push({ open: c.tagName, attrs: attrs.join(' ') }); walk(c); toks.push({ close: c.tagName });
      }
    });
  })(d.body);
  // espaces : réduits ; retirés aux frontières des éléments de structure (sans effet visuel)
  const out = [];
  toks.forEach((t, i) => {
    if(typeof t !== 'string'){ out.push(t.open ? '<' + t.open + ' ' + t.attrs + '>' : '</' + t.close + '>'); return; }
    let s = t.replace(/\s+/g, ' ');
    const prev = toks[i-1], next = toks[i+1];
    if(prev === undefined || (typeof prev !== 'string' && prev.open && !INLINE.has(prev.open)) || (typeof prev !== 'string' && prev.close && !INLINE.has(prev.close))) s = s.replace(/^ /, '');
    if(next === undefined || (typeof next !== 'string' && next.close && !INLINE.has(next.close)) || (typeof next !== 'string' && next.open && !INLINE.has(next.open))) s = s.replace(/ $/, '');
    if(s !== '') out.push(s);
  });
  return { tokens: out, title: d.title, lang: d.documentElement.lang };
}
function diff(a, b){
  const n = Math.min(a.tokens.length, b.tokens.length);
  for(let i = 0; i < n; i++) if(a.tokens[i] !== b.tokens[i]) return `jeton ${i} : « ${String(a.tokens[i]).slice(0,160)} »  ≠  « ${String(b.tokens[i]).slice(0,160)} »`;
  if(a.tokens.length !== b.tokens.length) return `nombre de jetons ${a.tokens.length} ≠ ${b.tokens.length}`;
  if(a.title !== b.title) return `titre « ${a.title} » ≠ « ${b.title} »`;
  if(a.lang !== b.lang) return `lang « ${a.lang} » ≠ « ${b.lang} »`;
  return null;
}
let fails = 0;
const report = (name, d) => { console.log((d ? 'FAIL ' : 'PASS ') + name + (d ? '\n     ' + d : '')); if(d) fails++; };

(async () => {
  if(!origFile || !newFile || !lang){ console.error('usage: node trans_script_4_test_render.js reference.html candidat.html langue'); process.exit(2); }
  const A = load(origFile), B = load(newFile);
  const ready = w => new Promise(r => { if(w.document.readyState === 'complete') r(); else w.addEventListener('load', r); });
  await ready(A); await ready(B); await tick();
  // les deux versions sont multilingues : on choisit la même langue dans chacune (une référence monolingue est acceptée)
  if(typeof A.applyLanguage === 'function') A.eval(`applyLanguage('${lang}')`);
  B.eval(`applyLanguage('${lang}')`);
  await tick();
  const run = async (name, fn) => { fn(A); fn(B); await tick(); report(name, diff(canon(A), canon(B))); };
  const type = (w, id, v) => { const i = w.document.getElementById(id); i.value = v; i.dispatchEvent(new w.Event('input', { bubbles: true })); };
  const click = (w, sel, i = 0) => w.document.querySelectorAll(sel)[i].dispatchEvent(new w.MouseEvent('click', { bubbles: true }));

  report('état initial (' + lang + ')', diff(canon(A), canon(B)));
  await run('simulateur : erreurs de balise', w => type(w, 'sim-input', '<REDD>x</> <img>FUEL<> <red><IMG>FUELL<> t</>'));
  await run('simulateur : champ vidé', w => type(w, 'sim-input', ''));
  await run('simulateur : texte valide', w => type(w, 'sim-input', '<PET1><IMG>TECH1<> Techs</> <VISOR><IMG>DWAYPOINT<> Elmt/Comp</>'));
  await run('recherche couleurs', w => type(w, 'color-search', 'PET'));
  await run('recherche couleurs sans résultat', w => type(w, 'color-search', 'ZZZZ'));
  await run('recherche couleurs effacée', w => type(w, 'color-search', ''));
  await run('tri des couleurs (hex-alpha)', w => click(w, '.color-head .sort-btn', 2));
  await run('tri des couleurs (retour)', w => { click(w, '.color-head .sort-btn', 2); click(w, '.color-head .sort-btn', 0); });
  await run('recherche icônes', w => type(w, 'icon-search', 'FUEL'));
  await run('recherche icônes sans résultat', w => type(w, 'icon-search', 'ZZZZ'));
  await run('recherche icônes effacée', w => type(w, 'icon-search', ''));
  await run('filtre de catégorie (3e option)', w => { const s = w.document.getElementById('icon-cat-filter'); s.selectedIndex = 3; s.dispatchEvent(new w.Event('change', { bubbles: true })); });
  await run('changement d\'onglet', w => click(w, '.tab-btn', 2));

  // --- bascule de langue et retour : l'état (catégorie choisie, recherche) doit être conservé
  const other = B.eval("I18N.order.find(c => c !== '" + lang + "')");
  const selBefore = B.document.getElementById('icon-cat-filter').selectedIndex;
  const typedBefore = B.document.getElementById('icon-search').value;
  B.eval(`applyLanguage('${other}')`); await tick();
  const selMid = B.document.getElementById('icon-cat-filter').selectedIndex;
  report(`bascule ${lang} → ${other} : la catégorie choisie est conservée (index ${selBefore})`, selMid === selBefore ? null : `index ${selMid}`);
  report(`bascule vers ${other} : <html lang> et titre mis à jour`, (B.document.documentElement.lang === other && B.document.title.length > 3) ? null : 'lang=' + B.document.documentElement.lang);
  B.eval(`applyLanguage('${lang}')`); await tick();
  report(`retour ${other} → ${lang} : rendu identique à l'original après interactions`, diff(canon(A), canon(B)));
  const miss = B.eval('Array.from(I18N.missing)');
  report('aucune clé manquante signalée', miss.length ? JSON.stringify(miss.slice(0, 5)) : null);
  console.log(fails ? `\n${fails} ÉCHEC(S)` : '\nTOUT OK');
  process.exit(fails ? 1 : 0);
})();
