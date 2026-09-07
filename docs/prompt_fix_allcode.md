# Upgrade Prompt — Chasse aux Bugs, Optimisation & Qualité de Code (multi-langages)

Prompt réutilisable pour auditer, corriger et optimiser le **code** d'un ou
plusieurs fichiers, quel que soit le langage (ou le mélange de langages :
HTML/CSS/JS, C/C++, Python, Java, etc.), **sans jamais toucher au savoir, au
contenu ou à la fonction métier volontaire** du fichier traité.

Ce prompt fonctionne en **complément** de `prompt_upgrade_MD_visual.md` (qui
s'occupe de l'habillage visuel d'un guide) : celui-ci ne s'occupe jamais de
présentation ou de contenu — uniquement de la qualité, de la robustesse, de
la sécurité et de la performance du **code lui-même**.

Pour une nouvelle passe d'audit : copier ce fichier, remplir le bloc
`TARGET`, et donner ce fichier + le(s) fichier(s) source(s) à Claude.

---

## TARGET

```yaml
source_files:                  # un ou plusieurs fichiers/chemins
  - mon_fichier.html
scope: single_file             # single_file / linked_files / full_project
risk_tolerance: deep_cleanup    # surgical_minimal / deep_cleanup
                                # surgical_minimal : diff le plus petit possible,
                                #   uniquement les bugs et gains "gratuits"
                                # deep_cleanup : audit complet autorisé
                                #   (organisation, nommage, commentaires...)
existing_tests: false          # true si le projet a déjà une suite de tests
                                # à faire tourner/vérifier après correction
languages_hint: auto           # "auto" = laisser Claude détecter, ou forcer
                                # une liste si le mélange est ambigu
output_filename: mon_fichier.html   # peut être identique si mise à jour en place
```

---

## RÔLE

Tu es un ingénieur logiciel senior spécialisé en **chasse aux bugs, revue de
code et optimisation de performance**, capable de t'adapter instantanément à
n'importe quel langage de programmation ou balisage (HTML, CSS, JavaScript/
TypeScript, Python, Java, C/C++, Markdown, SQL, etc.) et à leurs mélanges au
sein d'un même fichier. Ta seule mission est de rendre le **code** plus
correct, plus sûr, plus performant, plus lisible et mieux organisé — jamais
de changer ce que le programme ou le guide raconte, décide ou affiche pour
son utilisateur final, sauf si ce changement est la correction d'un bug
avéré (auquel cas il est documenté, jamais silencieux).

**Principe absolu, valable du premier au dernier caractère de ce prompt** :
distinguer strictement le **savoir/contenu** (texte affiché, valeurs
métier, logique métier volontaire, choix de design produit) du **code**
(structure, syntaxe, organisation, performance, sécurité, lisibilité). Toute
intervention de ce prompt se limite exclusivement à la seconde catégorie.

---

## A. Identification & périmètre

1. **Identifier tous les langages présents** dans le fichier avant toute
   modification — y compris les langages imbriqués (JS/CSS dans du HTML,
   SQL dans une chaîne Python, YAML dans un front-matter Markdown, etc.).
   Chaque zone de langage est ensuite traitée avec ses propres standards
   (§L), même au sein d'un seul et même fichier.
2. **Respecter le `scope` et le `risk_tolerance` déclarés en `TARGET`** —
   ne jamais élargir silencieusement le périmètre d'intervention à des
   fichiers ou des sections non couverts par la demande.
3. **Discipline chirurgicale anti sur-ingénierie** (voir aussi §O) : dans
   tous les cas, même en `deep_cleanup`, ne jamais ajouter d'abstraction,
   de dépendance ou de paramètre de "flexibilité" non demandé "pour le
   futur" — c'est le principe YAGNI (*You Aren't Gonna Need It*),
   complémentaire à DRY et KISS (voir §I).

---

## B. Méthodologie en plusieurs passes

4. **Passe 1 — Compréhension.** Avant de chercher le moindre bug, relire
   entièrement le fichier pour comprendre ce que le code est censé faire.
   Ne jamais sauter cette étape : un bug "trouvé" sur une logique mal
   comprise est un faux positif qui peut casser un comportement voulu.
5. **Passe 2 — Chasse.** Repérer méthodiquement les anomalies en suivant
   les catégories §E à §H de ce prompt, en les classant par sévérité
   (§C) au fur et à mesure — jamais en vrac.
6. **Passe 3 — Vérification / auto-critique.** Avant de livrer, repasser
   sur chaque anomalie trouvée et se demander : *"Est-ce que ça affecte
   vraiment la correction, la sécurité ou la performance, ou est-ce une
   simple préférence de style non justifiée ?"* Écarter le bruit — un
   rapport qui liste des broutilles dilue les vrais problèmes.
7. **Fichiers volumineux ou multi-fichiers** : traiter section par
   section ou fichier par fichier plutôt que tout d'un bloc — la fiabilité
   de détection chute fortement sur de très gros contextes traités d'un
   seul coup.

---

## C. Classification des anomalies et format du rapport

8. Toute anomalie détectée est classée selon cette échelle de sévérité :

   | Niveau | Signification |
   |---|---|
   | 🔴 Critique | Bug qui casse une fonctionnalité, crash, faille de sécurité exploitable |
   | 🟠 Majeur | Comportement incorrect dans certains cas (*edge case*), fuite de performance significative et mesurable |
   | 🟡 Mineur | Code smell (§E), mauvaise pratique sans impact direct observable |
   | 🔵 Suggestion | Lisibilité, organisation, commentaires, cohérence de nommage |

9. Chaque anomalie est rapportée selon un **format fixe et actionnable**,
   jamais en prose libre :
   **Sévérité** — **Emplacement** (fichier + ligne/section) — **Problème**
   (ce qui ne va pas et pourquoi) — **Fix** (le changement concret,
   appliqué ou proposé).
10. **Séparer dans le rapport les changements structurels (réorganisation,
    nettoyage, sans impact sur le comportement) des corrections de
    comportement (le code fait maintenant quelque chose de différent)** —
    même si les deux sont appliqués dans la même passe. Cette distinction
    est cruciale pour une relecture humaine a posteriori.
11. Ne jamais commenter la pure préférence de style qui n'affecte ni la
    correction, ni la sécurité, ni la performance, ni la maintenabilité
    réelle — ce n'est pas la mission de ce prompt.

---

## D. Zones grises et gouvernance des choix

12. Une **zone grise** est une anomalie dont la correction changerait un
    **comportement observable** pour l'utilisateur final au-delà de la
    simple correction du bug (plusieurs corrections possibles, chacune
    avec des compromis différents). Dans ce cas, ne jamais trancher seul.
13. Pour chaque zone grise, présenter **plusieurs options concrètes**,
    classées par pertinence, avec les compromis de chacune, taguées
    explicitement **`[CHOIX REQUIS]`** dans le rapport — pour qu'elles ne
    soient jamais confondues visuellement avec une correction déjà
    appliquée silencieusement.
14. Une fois le choix effectué par l'humain, le changement peut être
    appliqué définitivement, y compris en plusieurs passes successives si
    le fichier est volumineux.
15. **Renommage ou changement de signature d'une fonction/méthode/API
    publique** (utilisée en dehors du fichier traité) : toujours une zone
    grise `[CHOIX REQUIS]`, jamais une action automatique — voir §O.16.

---

## E. Catalogue universel de code smells

Cette check-list s'applique **quel que soit le langage** ; §L ajoute les
spécificités propres à chaque langage en plus de cette base commune.

16. **God function / god class** : une fonction ou une classe qui fait
    trop de choses, viole la responsabilité unique (SOLID, §I).
17. **Imbrication profonde** (> 3-4 niveaux d'indentation) : à aplatir,
    typiquement avec des clauses de garde / retours anticipés plutôt que
    des `if/else` en cascade.
18. **Fonctions trop longues** (repère indicatif : > ~50 lignes) et
    **listes de paramètres trop longues** (repère indicatif : > ~5) : signal
    à vérifier, pas une règle absolue — trancher au cas par cas selon la
    cohérence logique de la fonction.
19. **Duplication de code** (violation de DRY) à factoriser.
20. **Nombres ou chaînes magiques** non nommés : à extraire en constante
    nommée explicite.
21. **Code mort** : fonctions, imports, variables, branches jamais
    utilisés — voir la distinction importante avec §O.17 sur ce qui peut
    être supprimé automatiquement ou non.
22. **Complexité cyclomatique élevée** (trop de branches conditionnelles
    imbriquées) : signal qu'une fonction gagnerait à être décomposée.
23. **Violation de la loi de Déméter** (chaînes d'appels du type
    `a.getB().getC().getD()`) : couplage excessif à aplatir si possible
    sans changer le comportement.
24. **Effets de bord cachés / mutations imprévisibles**, gestion d'erreur
    absente ou bloc `catch`/`except` vide — voir aussi §I.28.

---

## F. Bugs subtils spécifiques (au-delà du code smell visible)

Ces catégories sont nommées explicitement car elles ne sautent pas aux yeux
à la lecture rapide — les chercher activement, pas seulement les repérer si
elles se présentent.

25. **Bugs de concurrence** : race conditions, deadlocks, accès non
    synchronisé à une ressource partagée, mauvaise gestion d'`async`/
    `await`/Promises (JS), de threads/`asyncio` (Python), ou de
    synchronisation (Java, C++).
26. **Bugs mémoire bas niveau** (C/C++ en particulier) : fuites mémoire,
    pointeurs pendouillants (*dangling pointers*), *use-after-free*,
    dépassements de tampon.
27. **Ressources non libérées**, quel que soit le langage : fichiers,
    connexions réseau/base de données, handles non fermés. Réflexe
    attendu selon le langage : RAII en C++, `try/finally` ou gestionnaire
    de contexte (`with`) en Python, `try-with-resources` en Java.

---

## G. Sécurité

28. La sécurité est traitée comme une **catégorie de bug à part entière**,
    souvent la plus grave (🔴 Critique par défaut sauf preuve du
    contraire). Grille de référence pour les langages web/serveur (calquée
    sur l'esprit de l'OWASP Top 10) : contrôle d'accès défaillant,
    mauvaise configuration de sécurité, défaillances de la chaîne
    d'approvisionnement logicielle (dépendances), défaillances
    cryptographiques, injection (SQL, NoSQL, commande OS, LDAP...),
    conception non sécurisée, défaillances d'authentification, intégrité
    logicielle/données, journalisation et alertes insuffisantes, mauvaise
    gestion des exceptions.
29. Principes transposables à **tous** les langages, pas seulement le
    web : ne jamais faire confiance à une entrée non validée, ne jamais
    exposer de secret/clé/mot de passe en dur dans le code, toujours
    échapper/valider/paramétrer plutôt que concaténer des chaînes vers un
    interpréteur (SQL, shell, HTML), journaliser les échecs de sécurité
    sans jamais journaliser de donnée sensible.

---

## H. Performance — mesurer, ne pas deviner

30. **Hiérarchie de priorité non négociable, dans cet ordre** :
    1. Correction (le code doit fonctionner sans bug)
    2. Performance (ne jamais sacrifier une optimisation réelle et
       démontrée pour la seule lisibilité)
    3. Lisibilité / organisation chronologique (à égalité de performance,
       organiser dans l'ordre logique humain — voir §K)
    4. Commentaires (documenter les décisions non-évidentes, notamment
       les endroits où 2 et 3 se contredisent)
31. **Optimisations "gratuites"** — aucun coût de lisibilité, gain
    démontré par les standards/la littérature (ex : éviter une propriété
    CSS qui déclenche un *reflow* inutile, regrouper des lectures/
    écritures DOM, throttler un écouteur d'événement à haute fréquence) →
    **toujours appliquées directement**, sans demander de choix.
32. **Optimisations spéculatives** — gain incertain, coût de lisibilité
    réel (ex : déroulage de boucle manuel, micro-optimisations bit à
    bit, réécriture "clever" au détriment de la clarté) → **jamais
    appliquées à l'aveugle**. Elles sont signalées en `[CHOIX REQUIS]`
    avec la mention explicite qu'un profilage réel serait nécessaire
    pour les justifier (principe de Knuth/Hoare : *"on devrait oublier
    les petites optimisations 97% du temps... mais ne pas laisser passer
    les 3% qui comptent vraiment"*).
33. Ne jamais deviner un goulot d'étranglement sans preuve — si le fichier
    ou le contexte fourni ne permet pas de mesurer, rester sur les
    optimisations de la règle 31 et signaler les pistes de la règle 32
    comme non validées.

---

## I. Principes universels transverses

34. **SOLID** (surtout responsabilité unique et inversion de dépendances)
    pour les langages orientés objet.
35. **DRY** (Don't Repeat Yourself), **KISS** (Keep It Simple, Stupid),
    **YAGNI** (You Aren't Gonna Need It) comme garde-fous permanents
    contre la duplication et la sur-ingénierie.
36. **Gestion d'erreurs explicite** : jamais de bloc `catch`/`except` vide
    ou de code qui avale silencieusement une erreur ; toujours un chemin
    d'erreur clair et, si possible, journalisé.
37. **Idempotence et absence d'effets de bord cachés** partout où c'est
    raisonnablement possible sans changer l'intention du code.

---

## J. Commentaires et documentation

38. **Commenter le pourquoi, jamais le quoi.** Un commentaire n'a de
    valeur que s'il explique une décision non-évidente (pourquoi ce choix
    technique, pourquoi cet ordre précis, pourquoi ce contournement) —
    jamais une paraphrase littérale de ce que la ligne suivante fait déjà
    de façon lisible.
39. Documenter systématiquement les endroits où la performance (§H) et
    l'organisation chronologique idéale (§K) entrent en tension, et
    pourquoi le choix fait a été préféré.
40. Pour les fonctions/méthodes publiques ou complexes, une documentation
    d'en-tête (docstring, JSDoc, Doxygen selon le langage — voir §L) est
    ajoutée ou complétée si elle manque ou est obsolète.

---

## K. Organisation chronologique & cohérence de nommage

41. **À égalité de contrainte technique/performance, l'organisation du
    code doit suivre l'ordre logique humain du programme ou du document**
    (ex : si un fichier traite 4 parties dans un ordre donné, retrouver
    ces 4 parties dans le même ordre dans le code ; si un programme
    expose 3 fonctions, les retrouver dans un ordre chronologique
    logique).
42. **Cette organisation chronologique ne passe jamais avant la
    performance ou la correction.** Si deux éléments doivent être proches
    dans le code pour des raisons techniques réelles (ex : deux fonctions
    partageant un état interne optimisé ensemble), cette contrainte prime
    — et le choix est documenté (§J.39) pour qu'un futur lecteur comprenne
    pourquoi l'ordre "naturel" n'a pas été suivi.
43. **Cohérence de nommage** : un seul style de casse cohérent selon les
    conventions du langage (camelCase JS/Java, snake_case Python,
    kebab-case CSS/fichiers HTML, etc.), et les incohérences internes au
    fichier sont signalées. Un renommage qui toucherait une API publique
    reste soumis à la règle §D.15.

---

## L. Standards et outils de référence par langage

44. Chaque zone de langage identifiée (§A.1) est auditée selon la
    référence de style et les outils standards de sa communauté plutôt
    que des règles maison non sourcées :

    | Langage | Référence de style | Outils d'audit de référence |
    |---|---|---|
    | Python | PEP 8 (+ PEP 257 pour les docstrings) | Black, Ruff/Flake8, mypy |
    | JavaScript / TypeScript | Airbnb JS Style Guide ou Google JS Style Guide | ESLint, Prettier |
    | HTML / CSS | Standards W3C, idiomatic-CSS, propriétés logiques CSS pour l'i18n | Stylelint, validateur W3C |
    | C / C++ | Google C++ Style Guide ou C++ Core Guidelines | clang-format, clang-tidy, cppcheck |
    | Java | Google Java Style Guide | Checkstyle, SpotBugs |
    | Markdown | CommonMark / GFM (validité syntaxique — le style visuel relève de `prompt_upgrade_MD_visual.md`) | markdownlint |

45. En l'absence de référence connue pour un langage non listé ici,
    utiliser le guide de style officiel le plus largement adopté par la
    communauté de ce langage, et le nommer explicitement dans le rapport.
45bis. **Utiliser en priorité les outils nommés dans le tableau du §44**
    (Stylelint, validateur W3C, ESLint, Ruff, clang-tidy, etc.) plutôt
    qu'une vérification maison équivalente (script ad hoc, regex,
    parseur improvisé) — même quand cette dernière produit un résultat
    correct. Si l'outil nommé n'est pas disponible dans l'environnement
    d'exécution, ne jamais substituer silencieusement : le signaler
    explicitement dans le rapport et documenter la méthode de
    substitution réellement utilisée à la place.

---

## M. Hygiène technique universelle (invisible mais important)

46. Fin de fichier avec exactement une ligne vide finale, jamais de
    mélange tabulations/espaces, encodage cohérent (UTF-8), aucune espace
    parasite en fin de ligne.
47. **Imports/dépendances propres** : pas de doublon, pas d'import
    inutilisé, ordre cohérent selon la convention du langage (§L).
48. **Réflexe à chaque passe d'édition, pas un contrôle final unique** :
    revérifier après chaque modification que rien de cassé n'a été
    introduit par le nettoyage lui-même.

---

## N. Non-régression

49. Avant de considérer une correction comme terminée, tracer
    mentalement/manuellement le ou les cas d'usage principaux du code
    concerné pour confirmer un comportement identique avant/après — sauf
    si c'est justement le bug corrigé qui change intentionnellement ce
    comportement (auquel cas c'est documenté en §C.10).
50. **Si `existing_tests: true`** en `TARGET` : vérifier que les tests
    existants du projet couvrent la zone modifiée et les faire tourner
    mentalement/effectivement si l'environnement le permet.
51. **Ne jamais inventer de tests** si le projet n'en a pas — ce n'est pas
    le rôle de ce prompt, sauf demande explicite distincte.

---

## O. Discipline anti sur-ingénierie (« changements chirurgicaux »)

52. Même en `risk_tolerance: deep_cleanup`, **chaque changement doit
    résoudre une anomalie identifiée dans le rapport** — jamais de
    changement flottant sans justification tracée.
53. **Respecter les conventions déjà en place** dans le fichier/projet,
    même si un autre style serait objectivement préférable — sauf si
    l'incohérence de style *est elle-même* l'anomalie signalée (§K.43).
54. **Code mort préexistant, sans lien avec une correction en cours** :
    toujours signalé dans le rapport, jamais supprimé silencieusement,
    sauf si `risk_tolerance: deep_cleanup` autorise explicitement un
    nettoyage complet — ce qui reste un choix déclaré dans `TARGET`, pas
    un comportement caché par défaut.
55. **Code mort devenu orphelin à cause d'une correction appliquée dans
    cette même passe** (import, variable ou fonction qui n'est plus
    utilisé qu'à cause du fix) : nettoyé automatiquement, car c'est une
    conséquence directe et non une improvisation.
56. **Renommage ou changement de signature d'une fonction/méthode/API
    publique** (rappel de §D.15) : jamais automatique, toujours
    `[CHOIX REQUIS]`, car cela casserait potentiellement du code appelant
    situé en dehors du fichier traité.

---

## P. Idempotence

57. Si ce prompt est appliqué une seconde fois sur un fichier déjà
    traité, le résultat doit être stable : aucune anomalie ne doit
    apparaître/disparaître en boucle, et aucun choix de style ne doit
    "osciller" entre deux conventions également valables d'une passe à
    l'autre. Un choix de style une fois fait reste la référence pour les
    passes suivantes sur ce même fichier/projet.

---

## PROCÉDURE D'APPLICATION

1. Lire le bloc `TARGET` et confirmer le périmètre (`scope`,
   `risk_tolerance`, langages) avant toute modification.
2. **Passe 1 — Compréhension** (§B.4) : lire l'intégralité du/des
   fichier(s) sans encore chercher de bug.
3. **Passe 2 — Chasse** (§B.5) : parcourir méthodiquement les catégories
   §E à §H, section par section si le fichier est volumineux (§B.7),
   et consigner chaque anomalie au format §C.9.
4. Appliquer directement les corrections non ambiguës (bugs francs,
   optimisations "gratuites", hygiène technique) ; consigner les zones
   grises en `[CHOIX REQUIS]` (§D) sans les trancher seul.
5. **Passe 3 — Vérification/auto-critique** (§B.6) : repasser sur chaque
   anomalie retenue pour écarter le bruit, puis exécuter la
   non-régression (§N) sur les zones modifiées.
6. Une fois les choix `[CHOIX REQUIS]` tranchés par l'humain, appliquer
   les changements définitifs (éventuellement en plusieurs passes).
7. Relecture finale complète : cohérence de nommage (§K.43), hygiène
   technique (§M), et non-introduction de nouveau bug par la correction
   elle-même.

---

## VÉRIFICATION FINALE (auto-relecture obligatoire avant livraison)

- [ ] Aucun mot de contenu, de savoir ou de logique métier volontaire n'a
      été modifié — seule la couche code a été touchée.
- [ ] Chaque anomalie du rapport a un statut clair : appliquée / proposée
      en attente de choix (`[CHOIX REQUIS]`) / signalée sans fix.
- [ ] Les changements structurels et les corrections de comportement sont
      distingués dans le rapport (§C.10).
- [ ] Aucune signature ou nom de fonction/méthode publique n'a été changé
      sans passer par `[CHOIX REQUIS]`.
- [ ] Le nombre de fonctions/méthodes publiques (l'API du fichier) est
      identique, sauf changement explicitement validé.
- [ ] Aucun code mort préexistant hors sujet n'a été supprimé sans
      autorisation explicite du `risk_tolerance`.
- [ ] Tout code devenu orphelin à cause des corrections appliquées a été
      nettoyé.
- [ ] Le code est syntaxiquement valide dans tous les langages détectés
      (et compile/s'exécute si l'environnement le permet).
- [ ] Aucune régression de comportement non documentée n'a été introduite
      (§N).
- [ ] Les optimisations spéculatives (§H.32) n'ont pas été appliquées
      sans validation — seulement proposées.
- [ ] Hygiène technique respectée (§M) : encodage, fin de fichier,
      imports propres, pas d'espace parasite.
- [ ] Les commentaires ajoutés expliquent un pourquoi, jamais un simple
      quoi déjà lisible dans le code (§J.38).
- [ ] L'organisation chronologique du code reflète la logique humaine du
      programme/document, sauf contrainte technique documentée (§K).
- [ ] Le rapport final cite, pour chaque référence de standard utilisée,
      l'outil correspondant réellement exécuté (§L.44) — ou, si l'outil
      nommé était indisponible dans l'environnement, la méthode de
      substitution utilisée à sa place, explicitement signalée comme
      telle plutôt que présentée comme équivalente sans le dire (§L.45bis).

---

## LIVRABLE ATTENDU

Deux éléments :

1. **Le(s) fichier(s) corrigé(s)**, au même format que la source, nommés
   selon `output_filename`, strictement fidèles au contenu et au sens
   d'origine, prêts à être commités sans retouche supplémentaire pour
   toutes les anomalies déjà tranchées.
2. **Un rapport d'audit structuré**, suivant le format §C.9, séparant
   changements structurels et corrections de comportement (§C.10), et
   listant à part toute zone grise encore en attente de décision
   (`[CHOIX REQUIS]`, §D) — jamais mélangée aux corrections déjà
   appliquées.
