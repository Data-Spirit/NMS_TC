<!-- Versión del archivo 
> Versión : 2.2
> Última modificación : 2026-10-27
-->
<!-- Parámetros de traducción
> source_file: README_FR.md v2.2 (md5 cd377f8f5d862542265d60d9aac220ac)
> target_language: Español
> target_variant: neutral/standard
> lang_code: ES
> tone: compromise (sober, key imagery kept)
> fidelity_style: idiomatic
> companion_html_guide: NMS_txt_code.html v2.0, bloque i18n-es (md5 c26672e58a3d43832ea06d02149368e9)
> translated_on: 2026-10-27
-->

<h1 align="center">NMS // TEXT CODES — Documentación de diseño</h1>

<p align="center"><em>README en español: documentación de diseño de la guía interactiva</em></p>

<!-- BADGES CENTRADAS -->
<p align="center">

  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" alt="License: CC BY-NC-SA 4.0">
  </a>
  
  <a href="https://github.com/Data-Spirit">
    <img src="https://img.shields.io/badge/README%20%3A-README_ES.md-blue?style=flat&logo=mdbook&logoColor=white&logoSize=auto&label=README%20%3A&labelColor=black&color=darkcyan" alt="README : README_ES.md">
  </a>
  
  <a href="https://github.com/Data-Spirit/NMS_TC">
    <img src="https://img.shields.io/badge/URL%20%3A-NMS_TC-blue?style=flat&logo=shieldsdotio&logoColor=white&logoSize=auto&label=Repo%20%3A&labelColor=grey&color=mediumseagreen" alt="Site">
  </a>
  
</p>

**Una guía interactiva, autónoma y exhaustiva de los códigos de formato de texto de No Man's Sky** — colores e iconos, completamente documentados, probados y reunidos en un único archivo HTML. Está **disponible en varios idiomas**, gracias a un selector de idioma integrado en el archivo.

`NMS_txt_code.html` · ~359 KB · multilingüe · sin dependencias externas críticas · funciona sin conexión

> **¿Qué es qué?**
> - **La guía interactiva** (`NMS_txt_code.html`) es el producto: un archivo HTML autónomo, **multilingüe**, con un selector de idioma integrado.
> - **Este README** documenta su diseño. Está escrito **en español**. Existe una versión por idioma (`README_EN.md`, etc.). **Solo la guía interactiva es multilingüe, no los README.**

---

## Índice

- [Por qué este proyecto](#por-qué-este-proyecto)
- [Característica principal: un archivo 100 % autónomo](#característica-principal-un-archivo-100--autónomo)
- [La guía interactiva es multilingüe](#la-guía-interactiva-es-multilingüe)
- [Cifras clave](#cifras-clave)
- [Estructura de la interfaz](#estructura-de-la-interfaz)
  - [Pestaña Info](#-pestaña-info)
  - [Pestaña Colores](#-pestaña-colores)
  - [Pestaña Iconos](#-pestaña-iconos)
  - [Pestaña Acerca de](#-pestaña-acerca-de)
- [El simulador en directo](#el-simulador-en-directo)
- [La técnica de teñido de icono](#la-técnica-de-teñido-de-icono)
- [Copiar y pegar con un clic](#copiar-y-pegar-con-un-clic)
- [Identidad visual: un diseño "meta"](#identidad-visual-un-diseño-meta)
- [Cómo se extrajeron e integraron los iconos](#cómo-se-extrajeron-e-integraron-los-iconos)
- [Añadir o actualizar un idioma de la guía interactiva](#añadir-o-actualizar-un-idioma-de-la-guía-interactiva)
- [Fiabilidad de la información y limitaciones conocidas](#fiabilidad-de-la-información-y-limitaciones-conocidas)
- [Compatibilidad y accesibilidad](#compatibilidad-y-accesibilidad)
- [Stack técnico](#stack-técnico)
- [Licencia](#licencia)

---

## Por qué este proyecto

No Man's Sky permite personalizar los nombres (bases, naves, fragatas, multiherramientas, cofres de almacenamiento, sistemas estelares…) mediante un sistema de etiquetas de texto —coloración e iconos— que **no está documentado oficialmente en ningún sitio** por Hello Games. La información existe, pero está dispersa: capturas de pantalla de tablas de configuración internas, pruebas empíricas de jugadores en los foros, guías comunitarias parciales y a veces obsoletas.

**NMS_TC** recopila, verifica, corrige y presenta esta información de forma única, estructurada y directamente utilizable — pensada tanto para consultarse como documentación de referencia como para usarse a modo de herramienta de trabajo mientras se juega.

---

## Característica principal: un archivo 100 % autónomo

La guía se entrega en forma de **un único archivo `.html`** (con todos los idiomas incluidos), sin necesidad de ninguna carpeta adicional para funcionar.

En concreto, esto significa:

- **Sin instalación.** Basta con abrir el archivo en cualquier navegador moderno, y ya está.
- **Se puede mover y renombrar libremente.** El archivo no depende de ninguna ruta relativa hacia otros archivos.
- **Funciona sin conexión.** Todos los datos (colores, iconos, lógica de ordenación, simulador, textos de todos los idiomas) están embebidos directamente en el archivo — consulta la sección [Cómo se extrajeron e integraron los iconos](#cómo-se-extrajeron-e-integraron-los-iconos) para el detalle técnico de la integración de las imágenes.
- **Una única dependencia externa no crítica**: las fuentes tipográficas (Google Fonts, vía CDN — *Rajdhani*, *IBM Plex Sans*, *JetBrains Mono*). Sin conexión a internet, el renderizado simplemente recurre a las fuentes del sistema por defecto del navegador; no se pierde ninguna funcionalidad.

Esta decisión de diseño (integrarlo todo en lugar de depender de una carpeta de recursos externa) tiene un coste —un archivo más pesado (~359 KB) que una versión con imágenes externas— pero garantiza que un único archivo siempre baste para que todo funcione, lo cual responde directamente al uso previsto: una herramienta que se comparte, se descarga o se mueve sin tener nunca que preocuparse por archivos que falten.

---

## La guía interactiva es multilingüe

La guía interactiva existe en **varios idiomas dentro de un mismo archivo**: no hay un archivo por idioma.

- **Selector de idioma**: arriba a la derecha de la pantalla, un menú muestra cada idioma con su propio nombre, precedido de una bandera (por ejemplo «Français», «English», «Español»). La elección se aplica de inmediato a toda la guía: textos, tablas, mensajes del simulador.
- **Idioma elegido automáticamente**: un idioma indicado en la dirección (`?lang=es`) tiene prioridad; si no, la guía adopta la elección guardada y, después, el idioma del navegador si está disponible y, si no, el francés. El idioma mostrado se guarda después en el navegador.
- **Enlace directo a un idioma**: cada vez que cambia el idioma, la dirección de la guía se actualiza (`…/NMS_txt_code.html?lang=es`); basta con copiarla para compartir la guía en el idioma mostrado. Un valor desconocido simplemente se ignora. Este enlace se aplica a la versión en línea.
- **Idiomas disponibles actualmente**: el **francés** (idioma de origen), el **inglés** y el **español**.
- **Texto que falta en un idioma**: se muestra entonces la versión francesa en su lugar, nunca un mensaje de error.

> **Distinción importante.** Solo la **guía interactiva** es multilingüe. Este README, en cambio, está escrito en un único idioma; existe una versión por idioma (`README_FR.md`, `README_EN.md`…), cada una traducida por separado.

> **🔧 Detalle técnico:** cada idioma es un bloque de datos JSON situado al final del archivo, y los textos de la guía se identifican mediante claves. El formato (negrita, cursiva, código, enlaces…) se conserva, pero se depura mediante una lista blanca de etiquetas: una traducción no puede, por tanto, introducir código activo. Un bloque de idioma ilegible se ignora sin afectar a los demás. Cada idioma añade unos 13 KB al archivo. El valor `?lang=` de la dirección solo se compara con los idiomas disponibles; nunca se inserta en la página.

---

## Cifras clave

| | |
|---|---|
| 🎨 Etiquetas de color documentadas | **59** |
| 🖼️ Etiquetas de iconos documentadas | **145** |
| 📂 Categorías de iconos | **12** |
| 🔁 Duplicados de textura detectados | **21** |
| ⛔ Etiquetas listadas pero no funcionales | **16** |
| ❔ Etiquetas con ruta de textura no confirmada | **12** |
| 🖼️ Iconos integrados en base64 en el archivo | **145 / 145** |
| 📝 Ejemplos concretos de uso real | **10** |
| 🌍 Idiomas de la guía interactiva | **3** |
| 🔤 Textos por traducir (claves de traducción) | **116** |

---

## Estructura de la interfaz

La guía se organiza en **4 pestañas**, pensadas como un recorrido de lectura lógico: primero se aprende la sintaxis y luego se consultan las tablas de referencia. Un **selector de idioma**, arriba a la derecha, cambia el idioma de toda la guía interactiva.

### 📘 Pestaña Info

El punto de entrada de la guía. Reúne todo lo necesario para usar las etiquetas, sin tener que buscar por otros lados:

- **Sintaxis completa**, con coloración de sintaxis dedicada (ver más abajo) que distingue claramente el nombre de la etiqueta, el texto libre del usuario y los símbolos estructurales (`<`, `>`, `<>`, `</>`, `IMG`).
- **Técnica avanzada: teñir un icono con una etiqueta de color** — explica que una etiqueta de color pegada justo antes de una etiqueta `<IMG>` aplica su color sobre el icono a modo de filtro, con un recuadro **Importante** dedicado a la única sutileza real (dónde colocar la etiqueta de cierre para teñir solo el icono o el icono *y* el texto que le sigue), y una comparación visual de ambos casos lado a lado.
- **Recuadro de advertencia** que recuerda honestamente que este comportamiento ha sido observado por la comunidad pero no está documentado oficialmente, con la lista de limitaciones conocidas (los iconos que ya tienen color propio pueden resistirse al tinte, comportamiento no garantizado al 100 %).
- **Recuadro de Consejo** sobre el límite de caracteres de los campos de texto en el juego, con la recomendación de priorizar etiquetas cortas.
- **Sección "Ejemplos concretos"**: diez títulos realmente usados para organizar contenedores de almacenamiento en el juego, cada uno mostrado con su renderizado visual en directo *y* su código en bruto coloreado, con un botón de copia a la derecha de cada línea — la mejor demostración práctica de todo lo anterior.

### 🎨 Pestaña Colores

Una tabla de referencia completa de las 59 etiquetas de color, con:

- **Una muestra de color a todo lo ancho** por fila (en lugar de un pequeño cuadrado), con un fondo a cuadros para visualizar correctamente la transparencia de los colores que la tienen.
- **Código hexadecimal exacto** y **porcentaje de transparencia** (mostrado solo cuando es inferior al 100 %, para no sobrecargar la visualización innecesariamente).
- **Categoría de pertenencia** de cada etiqueta (Transmisiones / Misiones, Recursos, Jugadores, Compañeros, Mapa galáctico, etc.), alineada en el extremo derecho de cada fila.
- **Una franja de encabezado dedicada**, visualmente distinta (fondo y borde propios, separadores verticales entre columnas) en lugar de un simple texto flotante encima de la tabla.
- **Cuatro modos de ordenación en los que se puede hacer clic**: por nombre (alfabético), por color (ver más abajo), por código hexadecimal (alfabético) y por luminosidad (de más oscuro a más claro). Hacer clic una segunda vez sobre el mismo criterio invierte el orden.
- **Una barra de búsqueda** que filtra la lista al instante por nombre de etiqueta.

**La ordenación "Color" merece una explicación aparte.** Tras varias iteraciones fallidas con algoritmos de ordenación por matiz (HSL clásico, luego matiz+luminosidad, y después agrupación por familias perceptuales con umbrales de proximidad de matiz), quedó claro que ninguna fórmula matemática sencilla reproducía fielmente la percepción humana de un degradado "bien ordenado" — dos colores con exactamente el mismo matiz pero con una saturación muy distinta (un azul vivo y un azul desvaído, por ejemplo) nunca se clasificaban de forma satisfactoria con un cálculo automático por sí solo. La solución adoptada fue **un orden de referencia clasificado manualmente**, color por color, a ojo — más fiable que un algoritmo para captar matices como la viveza de un color o los neutros ligeramente teñidos (marfil, blanco roto) que deben distinguirse de los grises perfectamente neutros.

> **🔧 Detalle técnico:** a diferencia de la ordenación "Color", la ordenación por **luminosidad** sí se basa en un cálculo automático — la fórmula de luminancia perceptual estándar ITU-R BT.601 (`0.299×R + 0.587×G + 0.114×B`), que pondera el verde más fuertemente que el rojo y el azul, conforme a la sensibilidad del ojo humano a cada componente de color.

### 🖼️ Pestaña Iconos

Una tabla de referencia completa de las 145 etiquetas de iconos, agrupadas en **12 categorías** (Recursos, Interfaz, Fragatas, Inventario, Voz / Red, Botín, Plataformas / Controles, Símbolos de portal, Clase (C→S), Modos de juego, Edición de base, No funcional), con para cada icono:

- Una **miniatura de vista previa real** del icono (ver la sección dedicada a la extracción más abajo — no son símbolos genéricos, sino los iconos reales del juego, recortados).
- El **nombre exacto de la etiqueta**.
- La **ruta del archivo de textura** original (referencia `.DDS` interna del juego), cuando se ha podido identificar.
- Una **insignia de estado** en su caso: `duplicado` (la etiqueta apunta exactamente a la misma textura que otra, bajo un nombre distinto), `no funcional` (etiqueta presente en los datos pero sin textura asignada — probablemente un marcador de posición reservado por los desarrolladores) o `por verificar` (ruta de textura no confirmada en las fuentes disponibles).

La categoría **"Clase (C→S)"** ilustra una corrección de nomenclatura deliberada: originalmente llamada "Clases de naves", fue renombrada con una descripción en subtexto que aclara que en realidad se trata de una notación de calidad genérica del juego (naves, multiherramientas, fragatas, armas, tecnologías) y no de un sistema propio de las naves.

Igual que en la pestaña Colores, una **barra de búsqueda** y un **filtro por categoría** permiten navegar rápidamente por la lista.

**Alineación de columnas**: cada tabla de categoría utiliza anchos de columna fijos e idénticos (`table-layout: fixed`), y la columna "Etiqueta" está dimensionada según el nombre de etiqueta más largo de toda la guía (`BULLETPOINT_OFF`, 15 caracteres) — lo que garantiza que ningún nombre se trunque nunca y que la alineación se mantenga rigurosamente idéntica de una categoría a otra, independientemente de la longitud del título de la categoría o del contenido de sus filas.

### ℹ️ Pestaña Acerca de

El contexto y la transparencia metodológica de la guía:

- Recordatorio de que el sistema de etiquetado no está documentado oficialmente.
- Detalle técnico del banco de iconos (cómo se integran los 145 iconos, y dónde encontrar los archivos PNG individuales si se necesitan en otro lugar).
- Lista explícita de los duplicados de textura detectados, con ejemplos.
- Precisión sobre los símbolos de portal (`PR_0` a `PR_15`) — confirmados como funcionales en el juego por la comunidad (usados para renombrar sistemas estelares con el símbolo de su dirección de portal).
- Lista de las etiquetas no funcionales presentes en los datos pero sin textura asignada.
- Fuentes utilizadas para compilar la guía.

---

## El simulador en directo

Situado en la parte superior de la página, visible desde cualquier pestaña, el simulador permite **escribir una combinación de etiquetas y ver su renderizado al instante**, sin tener que volver al juego para comprobarlo:

- **Un botón de copia** (⧉) a la derecha del campo copia con un clic el código escrito, listo para pegarse en el juego (ver [Copiar y pegar con un clic](#copiar-y-pegar-con-un-clic)).
- **Una cruz de borrado** (×), situada dentro del campo, lo vacía y devuelve el foco para empezar de cero. Desaparece sola cuando el campo está vacío.
  - El marco de vista previa situado justo debajo mantiene la misma altura, tanto si contiene una vista previa como si está vacío: permanece negro y no se encoge al borrar el campo (altura mínima equivalente a una línea de contenido).
- **Un texto indicativo** discreto, en cursiva, aparece en el campo vacío para guiar a los nuevos usuarios.
- Reconoce y muestra correctamente las etiquetas de color, las etiquetas de icono y su combinación (incluida la técnica de teñido, ver más abajo).
- **Los errores de etiqueta se señalan**: un color o un icono desconocido (por ejemplo `REDD` en lugar de `RED`) se subraya en rojo, con un trazo ondulado, directamente en la vista previa. Debajo de la vista previa, una pequeña caja por error indica cuál es, con el nombre erróneo en rojo y, cuando existe, el nombre correcto en verde. Esta línea solo aparece cuando hay un error: sin errores, no se muestra nada y la altura de la vista previa no cambia.
- **Se comprueban las mayúsculas y minúsculas, igual que en el juego**: `red`, `fuel` o `<img>` en minúsculas se señalan con la corrección que hay que aplicar (`RED`, `FUEL`, `IMG`), mientras que antes se mostraban sin ninguna alerta o como texto sin formato.
- Los iconos mostrados son los iconos reales extraídos del juego (no son aproximaciones).
- Útil para componer un nombre complejo (varias etiquetas combinadas) y comprobar su renderizado antes de copiarlo en el juego.
- **El texto introducido siempre se neutraliza antes de mostrarse**: pegar cualquier texto en el campo, incluso deliberadamente "roto" o copiado de una fuente poco fiable, nunca puede interferir con la página en sí.

> **🔧 Detalle técnico:** el texto escrito se escapa primero por completo (transformación de los caracteres especiales HTML), y solo entonces se realiza el reconocimiento de las etiquetas `<COLOR>` y `<IMG>...<>` sobre esa versión ya escapada, en lugar de sobre el texto en bruto. Todo lo que no se reconozca como una etiqueta NMS real permanece, por tanto, como texto inerte, nunca interpretado como HTML activo. La búsqueda de etiquetas ignora las mayúsculas y minúsculas únicamente para poder detectar los errores de mayúsculas; la validez, en cambio, sigue siendo estricta (solo existen los nombres en mayúsculas), y los nombres se buscan en las tablas de colores e iconos sin tocar nunca las propiedades internas de los objetos JavaScript.

---

## La técnica de teñido de icono

El simulador reproduce la técnica que consiste en colocar una etiqueta de color justo antes de una etiqueta `<IMG>` para teñir el icono:

- Realizada técnicamente mediante una **máscara CSS** (`mask-image`): el color de la etiqueta se aplica como fondo, y el canal alfa del PNG del icono actúa como plantilla — lo que reproduce fielmente el comportamiento observado en el juego (el color *reemplaza* los píxeles del icono en lugar de fundirse con ellos).
- **No todos los iconos se tiñen en el simulador.** Un análisis de saturación (complementado con una verificación visual manual) permitió identificar una veintena de iconos que ya poseen un color propio significativo (insignias de clase, icono de PlayStation, diamantes de jugadores en red, algunos iconos de recursos...). Por motivos de legibilidad, estos se muestran con su color original en lugar de aplanarse en silueta — con una nota explícita que aclara que en el juego, el tinte puede aun así aplicarse realmente y dar un resultado distinto al de la vista previa.

---

## Copiar y pegar con un clic

Un mismo botón dedicado (símbolo ⧉) está presente en cuatro lugares de la guía:

- **Colores**: un botón a la izquierda de cada fila de la tabla copia una plantilla lista para usar, `<NOMBRE_COLOR>Texto</>`.
- **Iconos**: un botón a la izquierda de cada fila de la tabla copia directamente la sintaxis completa, `<IMG>NOMBRE_ICONO<>`.
- **Ejemplos concretos** (pestaña Info): un botón a la derecha de cada una de las diez filas copia el código en bruto del ejemplo, siempre idéntico.
- **Simulador**: un botón algo más grande, a la derecha del campo de entrada y a su altura, copia el código tal como está escrito en ese instante (el texto en bruto, no la vista previa). Su contenido se lee en el momento del clic: por tanto, sigue siempre las modificaciones hechas en el campo, sin nada que sincronizar. Si el campo está vacío, el clic no hace nada, para no sobrescribir el portapapeles con un contenido vacío.
- **Retroalimentación visual inmediata**: el botón se transforma brevemente en una marca de verificación (✓) durante aproximadamente 1,4 segundos para confirmar la copia.
- Se apoya en la API `navigator.clipboard`, con un respaldo automático (`document.execCommand`) para navegadores más antiguos que no la soporten.

---

## Identidad visual: un diseño "meta"

Decisión de diseño deliberada: en lugar de definir una paleta de interfaz arbitraria, **los colores de acento de la propia interfaz se toman directamente de las etiquetas de color reales del juego** documentadas en la guía:

| Uso en la interfaz | Color | Etiqueta NMS de origen |
|---|---|---|
| Títulos de sección, pestaña activa | Cian | `VISOR` |
| Recuadro "Consejo", acentos generales | Naranja | `COMMODITY` |
| Resaltado, texto subrayado | Verde esmeralda | *(tono personalizado, coherente con la familia de verdes del juego)* |
| Recuadro "Importante" | Violeta | `SPECIAL` |
| Recuadro de advertencia | Rojo | `TRANS_WAR` |

Esta elección crea una coherencia temática directa entre el contenido documentado y el vocabulario visual utilizado para presentarlo — la guía literalmente "se viste" con los colores que documenta.

---

## Cómo se extrajeron e integraron los iconos

Los 145 iconos no son símbolos genéricos: son los **iconos reales del juego**, extraídos individualmente de varias capturas de pantalla (tablas de configuración internas y capturas de la interfaz en el juego), y luego limpiados e integrados:

1. **Localización de las coordenadas.** Cada icono se localizó con precisión (coordenadas en píxeles) en su imagen de origen, con recalibrado manual en los casos en que las cuadrículas de origen no eran perfectamente regulares.
2. **Recorte.** El fondo se eliminó mediante umbralización por distancia de color (transformación a canal alfa), con aislamiento por componente conexa para eliminar los fragmentos de iconos vecinos que se colaban en las capturas donde los iconos estaban muy juntos.
3. **Control de calidad manual.** Varias pasadas de verificación visual permitieron identificar y corregir iconos mal encuadrados, descentrados o contaminados con un residuo del icono adyacente — hasta lograr un resultado limpio en los 145 iconos.
4. **Codificación.** Cada PNG (fondo transparente) se codifica en **base64** y se almacena en un objeto JavaScript (`ICON_DATA`) que asocia cada nombre de archivo con una cadena `data:image/png;base64,...`, utilizada directamente como atributo `src` de las etiquetas `<img>` — exactamente como si la imagen estuviera alojada en línea, salvo que está físicamente presente en el archivo.

Este enfoque explica tanto el peso del archivo (~359 KB, frente a unas pocas decenas de KB de una versión solo de texto) como su portabilidad total: mover, renombrar o compartir el archivo nunca rompe la visualización de los iconos.

Este bloque de datos (`ICON_DATA`) está deliberadamente aislado al final del script, separado de toda la lógica JavaScript que lo precede (solo los bloques de idioma, simples datos JSON, vienen después) — una organización pensada para que la lectura del código nunca quede saturada por esos varios miles de líneas de texto binario, y para facilitar que la comunidad añada iconos en el futuro.

> **🔧 Detalle técnico:** en JavaScript, una constante solo necesita estar declarada antes de usarse en tiempo de ejecución — no necesariamente antes de las funciones que la referencian en su código. Por eso `ICON_DATA` puede colocarse al final del script sin romper nada, siempre que permanezca declarado antes de la inicialización de la página, que se ejecuta una vez terminada la carga.

Las 16 etiquetas listadas como no funcionales no son todas simples entradas vacías: una parte de ellas (iconos genéricos de botones de mando) tienen, pese a todo, su imagen ya presente en base64 dentro de `ICON_DATA`, sin estar vinculadas a ella en la tabla de iconos.

> **🔧 Detalle técnico:** estas imágenes se conservan en reserva en lugar de eliminarse, por si Hello Games les asignara algún día una textura oficial en el juego — vincularlas se convertiría entonces en una simple corrección de una línea, sin tener que volver a extraer ni recodificar nada.

---

## Añadir o actualizar un idioma de la guía interactiva

Traducir la guía interactiva **no requiere ningún archivo nuevo**: un idioma es un bloque de texto más dentro de `NMS_txt_code.html`.

**Dos trabajos distintos, que no deben confundirse:**

| Qué | Dónde | Cómo |
|---|---|---|
| **El bloque de idioma de la guía interactiva** | dentro de `NMS_txt_code.html` | prompt `prompt_translation_HTML_GUIDE_LANG.md`, controlado por los scripts de la carpeta `docs/scripts/` |
| **Este README en otro idioma** | un archivo aparte (`README_EN.md`…) | prompt `prompt_translation_README_LANG.md` |

El principio de trabajo:

1. **El francés es el idioma de origen.** Toda nueva funcionalidad se escribe primero en francés, con sus textos identificados mediante claves.
2. **Solo se traduce lo que falta o ha cambiado.** El script `trans_script_1_check_keys.py` lista las claves que hay que traducir para un idioma dado.
3. **Cada bloque de idioma empieza con un campo `_meta`** que conserva el nombre del idioma, su bandera y los parámetros de traducción elegidos (tono, variante, fidelidad).
4. **Unos controles automáticos** verifican las claves, las etiquetas, los ejemplos de código, el comportamiento y la robustez de la guía en cada idioma.

---

## Fiabilidad de la información y limitaciones conocidas

La guía se esfuerza por ser honesta sobre lo que está confirmado y lo que no:

- El sistema de etiquetado **no está documentado oficialmente en ningún sitio** por Hello Games — toda la información procede de tablas de configuración internas del juego, pruebas en el juego y fuentes comunitarias.
- Los códigos hexadecimales de los colores proceden directamente de una tabla de valores RGBA/HEX exactos — con una excepción (`TRANS_ANM`) cuyo color exacto no ha podido confirmarse en las fuentes más recientes.
- Las etiquetas marcadas como `no funcional` o `por verificar` se identifican claramente como tales en lugar de presentarse con la misma certeza que el resto.
- La técnica de teñido de icono se presenta como un comportamiento observado, no como una garantía universal.
- Los idiomas **escritos de derecha a izquierda** (árabe, hebreo…) todavía no son compatibles con la guía interactiva: la visualización sería incorrecta.
- Las **banderas** del selector son emojis: algunos sistemas pueden mostrar dos letras en lugar de la bandera.

---

## Compatibilidad y accesibilidad

- **Responsive**: diseño adaptado a pantallas estrechas (columnas secundarias ocultas en móvil en la tabla de colores, desplazamiento horizontal de seguridad en las tablas de iconos).
- **Navegadores modernos**: Chrome, Firefox, Edge, Safari — se apoya en CSS Grid, `mask-image` y la API Clipboard, disponibles en todas las versiones recientes.
- **Accesibilidad básica**: las dos barras de búsqueda y el filtro de categoría se anuncian correctamente a los lectores de pantalla (`aria-label`), el campo del simulador está asociado a un verdadero `<label>` en lugar de a un simple texto flotante, y el botón de copia y la cruz de borrado del simulador llevan también un `aria-label`. El **selector de idioma** es un menú nativo etiquetado para los lectores de pantalla, y el atributo `lang` de la página sigue el idioma elegido.
- **No se envía ningún dato a ningún sitio**: todo se ejecuta localmente en el navegador, sin necesidad de conexión de red tras la primera carga de las fuentes tipográficas. Solo la **elección de idioma** se guarda, localmente, en el navegador; nunca se envía.

---

## Stack técnico

- **HTML/CSS/JavaScript vanilla** — sin frameworks, sin dependencias de compilación, sin ningún paso de build.
- **Fuentes tipográficas**: Rajdhani (títulos), IBM Plex Sans (texto general), JetBrains Mono (código), vía Google Fonts CDN.
- **Ninguna biblioteca de terceros**: la ordenación, la búsqueda, el filtrado, el simulador y la coloración de sintaxis son todos JavaScript nativo escrito específicamente para esta guía.
- **Sistema de idiomas propio**: las traducciones son diccionarios JSON embebidos en el archivo, leídos mediante JavaScript nativo, sin biblioteca de internacionalización.
- **Carga de fuentes optimizada**: dos `<link rel="preconnect">` establecen la conexión con los dominios de Google Fonts incluso antes de cargar la hoja de estilos, reduciendo la latencia percibida en la primera visualización.
- **Imágenes no bloqueantes**: los 145 iconos integrados usan `decoding="async"`, para que su decodificación nunca retrase el renderizado del resto de la página.
- **Código validado con herramientas estándar**: el HTML pasa la validación `html-validate` (preajuste recomendado), salvo dos reglas que señalan títulos y botones «vacíos» en el archivo fuente, desactivadas por decisión propia puesto que su texto se inserta al cargar según el idioma, y el CSS ha sido auditado con Stylelint sin anomalías de fondo (solo preferencias de formato, dejadas tal cual por coherencia de estilo).

---

## Licencia

Esta guía se distribuye bajo licencia [**CC BY-NC-SA 4.0**](https://creativecommons.org/licenses/by-nc-sa/4.0/). Consulta el archivo [`LICENSE.md`](../../LICENSE.md) en la raíz del repositorio para conocer los términos completos.

No Man's Sky y todos los assets, marcas y propiedades intelectuales asociados pertenecen a Hello Games y/o sus respectivos titulares. Esta guía es un recurso comunitario no oficial, sin ninguna relación con Hello Games.
