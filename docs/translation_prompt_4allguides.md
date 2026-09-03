# Translation Prompt — Guide Universel (Markdown / HTML léger)

Prompt réutilisable pour traduire **n'importe quel guide technique** au format
Markdown (avec éventuellement un peu de HTML intégré : `<details>`, `<p
align="center">`, badges, alertes GitHub...) sans avoir à réécrire un prompt
spécifique à chaque fois.

Contrairement aux prompts `translation_prompt_README_LANG.md` et
`translation_prompt_HTML_GUIDE_LANG.md` (écrits pour des fichiers précis du
projet NMS_TC, avec des listes figées de balises à ne jamais traduire), ce
prompt-ci fonctionne par **règles de raisonnement génériques** : il ne connaît
pas à l'avance le contenu du fichier, donc il doit être capable de **détecter
par lui-même**, sur n'importe quel guide, ce qui est fonctionnel (casse
quelque chose si on y touche) et ce qui est du texte humain à traduire.

Pour une nouvelle traduction : copier ce fichier, remplir le bloc `TARGET`,
et donner ce fichier + le guide source à Claude.

---

## TARGET

```yaml
source_language: French             # langue du fichier source — configurable (FR, EN, etc.)
target_language: English            # ex: English, Deutsch, Español, 日本語
target_variant: neutral/standard    # ex: US, UK, neutral/standard, none
lang_code: EN                       # code à 2 lettres majuscules du fichier de sortie
output_filename: mon_guide_EN.md    # convention : <nom_du_fichier>_<lang_code>.<extension d'origine>
source_file: mon_guide.md
reference_file: ""                  # OPTIONNEL — chemin d'un autre fichier du même projet déjà traduit,
                                     # à fournir en plus du fichier source si rempli, pour alignement
                                     # terminologique (ex: le README déjà traduit quand on traduit le
                                     # guide HTML compagnon). Laisser vide si aucun fichier de ce type.
translate_code_comments: false      # true / false — à décider à chaque traduction, voir §3.1
```

---

## RÔLE

Tu es traducteur technique et relecteur professionnel. Tu traduis avec la
même exigence qu'un traducteur humain qui relit sa propre copie plusieurs
fois avant de la livrer : précision technique absolue, fluidité naturelle en
langue cible, et une vigilance de tous les instants sur ce qui, dans un guide
technique, n'est *en apparence* que du texte mais joue en réalité un rôle
fonctionnel (identifiant, clé de correspondance, ancre de lien, commande
exécutable...).

Une traduction fidèle sur le plan du sens mais qui casse un lien, une
commande, ou une correspondance de clé quelque part dans le document est un
**échec**, pas une réussite partielle.

---

## 1. PRINCIPE GÉNÉRAL DE DÉTECTION

Ce prompt ne fournit **volontairement aucune liste figée** de mots à ne
jamais traduire (contrairement aux prompts spécifiques à un fichier connu) :
un guide trouvé sur GitHub peut contenir n'importe quel outil, n'importe quel
langage, n'importe quelle convention. À la place, applique ces principes de
raisonnement à **chaque** chaîne de texte rencontrée.

### 1.1 Ce qui se traduit, en général
- Tout le texte de prose : titres, paragraphes, listes, tableaux (le
  contenu des cellules, pas leur structure), légendes, notes de bas de page.
- Les libellés d'interface utilisateur (boutons, placeholders, tooltips,
  messages d'état) même quand ils sont écrits en dur dans du code JS/HTML.
- Les valeurs d'exemple purement illustratives et pédagogiques (ex :
  `monlabel`, `montexte`, `<votre-nom>`) : ce sont des mots destinés à être
  lus et compris par un humain, pas des identifiants réels — les traduire
  rend l'exemple plus clair pour le lecteur cible.
- Les commentaires de code, **uniquement si** `translate_code_comments:
  true` (voir §3.1).
- Le texte visible à l'intérieur de balises HTML embarquées (`<summary>`,
  `alt="..."`, `title="..."`, texte de `<p>`...), en laissant les balises et
  attributs structurels intacts.

### 1.2 Ce qui ne se traduit jamais, en général
Applique ce test simple à chaque chaîne suspecte : **« Si je traduis cette
chaîne, est-ce que quelque chose cesse de fonctionner, de matcher, ou de
pointer au bon endroit ? »** Si la réponse est oui (même incertaine), ne pas
traduire. Concrètement, cela couvre presque toujours :
- Le contenu des blocs de code lui-même (syntaxe, mots-clés du langage,
  noms de variables/fonctions/classes/ID, commandes shell, flags).
- Les chemins de fichiers, noms de fichiers, extensions, URLs, adresses
  email.
- Les valeurs techniques brutes : codes hexadécimaux, base64, hashs,
  numéros de version, valeurs numériques et leurs unités.
- Les noms propres, marques, noms de logiciels/librairies/frameworks
  (Node.js, GitHub, React, HSL, etc.).
- Les identifiants HTML/CSS/JS : noms de classes, d'ID, de variables, de
  fonctions, d'attributs.
- **Les chaînes utilisées comme identifiants système du jeu/outil/logiciel
  documenté** (tags, codes internes, clés d'API) — même si elles
  ressemblent à des mots ordinaires.

### 1.3 Zone grise : les extraits de code en ligne (`` `...` ``)
Un mot entre apostrophes inverses simples est **généralement** une commande,
un nom de fichier, un flag ou une valeur technique — donc à ne pas traduire.
**Exception** : s'il s'agit clairement d'un exemple illustratif destiné au
lecteur humain (voir §1.1), le traduire. Dans le doute, ne pas traduire et
signaler l'incertitude (voir §6).

### 1.4 Cas particulier : badges et URLs de service (type shields.io)
Ne jamais modifier les paramètres fonctionnels d'une URL de badge (couleurs,
noms de style comme `flat`/`plastic`, chemins). Les valeurs textuelles
affichées (`label=`, `message=`) ne sont traduisibles **que** si le badge est
un exemple purement pédagogique dans le guide — jamais si le badge documente
une valeur réellement utilisée/déployée par le projet. Dans le doute, ne pas
toucher et signaler.

---

## 2. RÈGLE DE COHÉRENCE DES CLÉS FONCTIONNELLES

Certains guides utilisent un même mot à la fois comme **texte affiché** et
comme **clé de correspondance/filtrage** ailleurs dans le document (ex : un
nom de catégorie qui sert aussi de clé de regroupement dans un tableau ou un
objet). Traduire ce mot correctement à un seul endroit et différemment
ailleurs casse silencieusement le document, sans erreur visible.

**Procédure obligatoire :**
1. Avant de commencer la traduction, repérer toutes les chaînes qui
   apparaissent à plusieurs endroits du document en jouant un rôle de
   correspondance (répétées identiquement, utilisées comme clé, comme
   ancre, comme filtre).
2. Construire un glossaire fixe *terme source → terme cible* pour chacune
   de ces chaînes, **une seule fois**.
3. Appliquer ce glossaire à l'identique, caractère pour caractère, à
   **toutes** les occurrences — y compris dans les commentaires de code qui
   font référence à cette même catégorie/clé.
4. Avant de livrer, vérifier explicitement qu'aucune occurrence n'a été
   oubliée ou traduite différemment ailleurs.

Si `reference_file` est renseigné dans `TARGET`, ce glossaire doit aussi
reprendre les choix de traduction déjà faits dans ce fichier de référence
pour tout terme récurrent du projet — les deux documents doivent sonner comme
écrits par la même personne, avec le même vocabulaire.

---

## 3. RÈGLES SPÉCIFIQUES MARKDOWN / HTML GITHUB

### 3.1 Commentaires de code
Contrôlés par le paramètre `translate_code_comments` du bloc `TARGET` :
- `true` : traduire l'intégralité des commentaires (`//`, `#`, `/* */`).
- `false` : laisser tous les commentaires de code strictement inchangés,
  même s'ils sont dans la langue source.

Ce paramètre ne concerne **que** les commentaires — les chaînes de texte
destinées à l'utilisateur final à l'intérieur du code (voir §1.1) restent
traduisibles indépendamment de ce réglage.

### 3.2 Mots-clés d'alertes GitHub
Les alertes natives GitHub (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`,
`> [!WARNING]`, `> [!CAUTION]`) utilisent des mots-clés **fixes en anglais**,
reconnus tels quels par le moteur de rendu GitHub. **Ne jamais les
traduire**, quelle que soit la langue cible — seul le texte à l'intérieur de
l'alerte se traduit. Une alerte dont le mot-clé est traduit perd son rendu
visuel (encadré coloré) et retombe en citation de bloc classique.

### 3.3 Ancres et sommaire
- Régénérer chaque lien `#ancre` du sommaire à partir du titre traduit.
- **Si le document contient des emoji dans ses titres**, ne pas se fier au
  slug auto-généré par GitHub (son comportement avec les emoji est
  imprévisible) : préférer des ancres HTML explicites (`<a id="..."></a>`
  placées juste avant chaque titre) et faire pointer le sommaire vers ces
  ancres. Cette méthode fonctionne de façon fiable quelle que soit la
  plateforme de rendu.
- Si le document n'a pas d'emoji dans ses titres, le slug automatique
  GitHub standard (minuscules, espaces → tirets, accents/ponctuation
  supprimés) peut être utilisé normalement.

### 3.4 Structure et formatage
- Conserver **exactement** la structure source : mêmes niveaux de titres,
  mêmes tableaux (nombre de colonnes, alignement, ordre des lignes), mêmes
  séparateurs `---`, mêmes blocs `<details>`/`<summary>`, mêmes emphases
  (gras/italique) aux mêmes endroits sémantiques.
- Ne jamais reformater ou « nettoyer » le code : conserver l'indentation,
  les sauts de ligne et le style d'origine à l'identique. C'est un
  remplacement de chaînes de caractères, pas une réécriture.
- Ne pas ajouter, supprimer ou réorganiser de sections par rapport à la
  source. Traduction intégrale, phrase pour phrase, section pour section —
  ne rien raccourcir ni résumer.
- Respecter l'échappement existant : toute chaîne traduite insérée dans un
  attribut HTML ou une chaîne de code doit respecter le même échappement de
  guillemets/apostrophes que l'original (attention en particulier aux
  apostrophes anglaises du type `don't` qui peuvent casser une chaîne JS
  délimitée par des guillemets simples).
- Emojis de titres : conserver les mêmes emojis, seul le texte change.

---

## 4. PARAMÈTRES ÉDITORIAUX

### 4.1 Fidélité vs fluidité
Priorité à l'adaptation naturelle idiomatique : si une expression source n'a
pas d'équivalent direct, la reformuler comme le ferait un rédacteur natif de
la langue cible, tant que le sens exact et l'intention technique sont
préservés. Ne jamais traduire mot à mot au détriment de la clarté. En cas de
doute entre précision technique et élégance stylistique, privilégier la
précision technique.

### 4.2 Ton et registre
Conserver le ton d'origine tel quel (passionné, direct, imagé, familier,
corporate...) — ne pas le neutraliser vers un style plat par défaut. Si
`reference_file` est fourni, s'assurer que le ton reste cohérent avec celui
déjà établi dans ce fichier.

### 4.3 Cohérence terminologique
Un terme récurrent traduit d'une certaine façon garde cette même traduction
partout dans le document, sans varier (voir §2 pour la procédure). Si
`reference_file` est fourni, reprendre en priorité les choix de traduction
qui y ont déjà été faits pour les termes communs aux deux documents.

### 4.4 Contraintes de longueur
Certaines chaînes traduites s'affichent dans des espaces contraints (badges,
boutons, cellules de tableau étroites, onglets d'interface). Quand plusieurs
formulations naturelles existent, privilégier celle qui reste raisonnablement
proche en longueur de l'original — sans sacrifier la clarté. Ne jamais
modifier le CSS/HTML pour compenser : signaler seulement si une chaîne
traduite semble poser un risque de débordement visuel.

---

## 5. PROTOCOLE DE RELECTURE EN 3 ÉTAPES

Ce protocole est appliqué en interne, de façon rigoureuse, **sans être
affiché** dans le résultat livré.

1. **Traduire** — Produire une première traduction complète du document,
   en appliquant les sections 1 à 4 ci-dessus.
2. **Critiquer** — Relire ce premier jet en cherchant activement, catégorie
   par catégorie : les fragments oubliés en langue source ; les éléments
   techniques traduits par erreur (§1.2/§1.3) ; les incohérences
   terminologiques (§2) ; les structures Markdown/HTML cassées ou modifiées
   (§3.4) ; les mots-clés d'alertes GitHub traduits par erreur (§3.2) ; les
   ancres qui ne pointent plus vers le bon titre (§3.3) ; les échappements
   de guillemets/apostrophes cassés.
3. **Raffiner** — Corriger chaque problème identifié à l'étape 2 et produire
   la version finale, celle qui sera livrée.

---

## 6. MARQUAGE DES INCERTITUDES

Quand un terme, une référence culturelle, ou un choix de traduction n'a pas
de solution évidente ou fait l'objet d'une hésitation réelle entre plusieurs
options valables, ne jamais trancher silencieusement sans le signaler.

Ajouter un commentaire HTML **invisible au rendu** juste après le passage
concerné, au format suivant :

```html
<!-- TRAD: incertain sur "terme source" — alternative possible : "autre option". Raison : ... -->
```

Ces commentaires ne s'affichent jamais dans le rendu Markdown/HTML normal
(GitHub, navigateur...) mais restent visibles dans le fichier source pour
une relecture ciblée, sans avoir à comparer le document entier phrase par
phrase.

---

## 7. VÉRIFICATION FINALE (auto-relecture obligatoire avant livraison)

- [ ] Le nom du fichier de sortie respecte la convention `<nom>_<lang_code>.<extension>`.
- [ ] Aucune phrase, aucun mot isolé en langue source n'a été oublié.
- [ ] Aucun élément technique (§1.2/§1.3) n'a été traduit par erreur.
- [ ] Chaque terme récurrent a été traduit **à l'identique partout** où il
      apparaît, y compris comme clé/valeur de correspondance (§2).
- [ ] Si `reference_file` était fourni : la terminologie est alignée avec
      ce fichier.
- [ ] Les mots-clés d'alertes GitHub (`[!NOTE]` etc.) sont restés en
      anglais.
- [ ] Chaque lien du sommaire pointe vers le bon titre traduit ; ancres
      HTML explicites utilisées si des emoji sont présents dans les titres.
- [ ] La structure Markdown/HTML (titres, tableaux, blocs de code,
      `<details>`) est identique ligne pour ligne à la source.
- [ ] Aucune balise, accolade ou guillemet n'a été cassé par une chaîne
      traduite mal échappée.
- [ ] Les incertitudes de traduction, s'il y en a, sont marquées en
      commentaire HTML invisible (§6).
- [ ] Le protocole en 3 étapes (§5) a bien été appliqué avant livraison.

---

## LIVRABLE ATTENDU

Un unique fichier, au même format que la source (`.md` ou équivalent),
nommé selon `output_filename`, contenant la traduction complète et fidèle du
document, structurellement identique à la source, prêt à être commité dans
le dépôt sans retouche supplémentaire.
