<!-- ================================================================================================================================ -->

<!-- PROMPT GUIDE HTML -->
Je te joins le fichier source NMS_txt_code_FR.html (le guide interactif autonome du projet NMS_TC) ainsi que le prompt de traduction prompt_translation_HTML_GUIDE_LANG.md, qui contient toutes les règles à appliquer (périmètre de traduction, éléments intouchables, règle critique sur CATEGORY_DESCRIPTIONS, etc.).

Je veux traduire ce fichier en [LANGUE_CIBLE], pour produire NMS_txt_code_[CODE].html.

Avant de commencer, applique bien les règles de démarrage du prompt :
- Confirme le fichier source utilisé (nom, nombre de lignes, un élément distinctif du contenu).
- Reformule et fais-moi valider les paramètres TARGET : target_language ([LANGUE_CIBLE]), target_variant (à me proposer/demander si cette langue a des variantes régionales notables — ne présume pas), lang_code ([CODE]), tone, fidelity_style, html_lang_attribute ([code_iso_minuscule]).
- Pose-moi toutes les questions nécessaires pour parfaire ces paramètres.

Ne traduis rien avant que je te dise explicitement : "c'est bon tu as le feu vert".

Ne traduis rien avant que je te dise explicitement : "c'est bon tu as le feu vert".


<!-- PROMPT README_LANG -->
Je te joins le fichier source README_FR.md (version à jour, avec les encadrés 🔧 Détail technique) ainsi que le prompt de traduction prompt_translation_README_LANG.md, qui contient toutes les règles à appliquer (règle §0 de correspondance de suffixe, éléments intouchables, placeholders pédagogiques, encadrés techniques, etc.).

Je te joins aussi NMS_txt_code_[CODE].html, déjà traduit en [LANGUE_CIBLE] juste avant dans cette même conversation — utilise-le comme companion_html_guide pour la cohérence terminologique (§7 du prompt) : reprends à l'identique ses choix déjà faits (noms de catégories, libellés de badges, termes récurrents).
(Si aucun guide HTML n'a encore été traduit dans cette langue à ce stade, retire ce paragraphe — cette traduction du README deviendra alors elle-même la référence terminologique.)

Je veux traduire ce README en [LANGUE_CIBLE], pour produire README_[CODE].md.

Avant de commencer, applique bien les règles de démarrage du prompt :
- Confirme le fichier source utilisé (nom, nombre de lignes, un élément distinctif du contenu).
- Reformule et fais-moi valider les paramètres TARGET : target_language ([LANGUE_CIBLE]), target_variant, lang_code ([CODE]), tone, fidelity_style, companion_html_guide.
- Pose-moi toutes les questions nécessaires pour parfaire ces paramètres.

N'oublie pas la règle §0 : la ligne d'intro du README doit référencer NMS_txt_code_[CODE].html, pas NMS_txt_code_FR.html.

Ne traduis rien avant que je te dise explicitement : "c'est bon tu as le feu vert".

<!-- ================================================================================================================================ -->





