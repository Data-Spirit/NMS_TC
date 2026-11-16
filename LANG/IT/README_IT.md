<!-- Versione del file 
> Versione : 2.8
> Ultima modifica : 2026-11-16
-->
<!-- Parametri di traduzione
> source_file: README_FR.md v2.8 (md5 e9c02b9294b4abf1df4f3e195e6d3c4a)
> target_language: Italiano
> target_variant: neutral/standard
> lang_code: IT
> tone: compromise (sober, key imagery kept)
> fidelity_style: idiomatic
> companion_html_guide: NMS_txt_code.html v2.4, blocco i18n-it (md5 0a5dc9ce7f462177e080852f0db61db8)
> translated_on: 2026-11-16
-->

<h1 align="center">NMS // TEXT CODES — Documentazione di progettazione</h1>

<p align="center"><em>README in italiano: documentazione di progettazione della guida interattiva</em></p>

<!-- BADGE CENTRATI -->
<p align="center">

  <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
    <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg" alt="License: CC BY-NC-SA 4.0">
  </a>
  
  <a href="https://github.com/Data-Spirit">
    <img src="https://img.shields.io/badge/README%20%3A-README_IT.md-blue?style=flat&logo=mdbook&logoColor=white&logoSize=auto&label=README%20%3A&labelColor=black&color=darkcyan" alt="README : README_IT.md">
  </a>
  
  <a href="https://github.com/Data-Spirit/NMS_TC">
    <img src="https://img.shields.io/badge/URL%20%3A-NMS_TC-blue?style=flat&logo=shieldsdotio&logoColor=white&logoSize=auto&label=Repo%20%3A&labelColor=grey&color=mediumseagreen" alt="Site">
  </a>
  
</p>

**Una guida interattiva, autonoma e completa ai codici di formattazione del testo di No Man's Sky** — colori e icone, interamente documentati, testati e riuniti in un unico file HTML. È **disponibile in più lingue**, grazie a un selettore di lingua integrato nel file.

`NMS_txt_code.html` · ~466 KB · multilingue · nessuna dipendenza esterna critica · funziona offline

> **Chi è cosa?**
> - **La guida interattiva** (`NMS_txt_code.html`) è il prodotto: un file HTML autonomo, **multilingue**, con un selettore di lingua integrato.
> - **Questo README** ne documenta la progettazione. È scritto **in italiano**. Esiste una versione per lingua (`README_EN.md`, ecc.). **Solo la guida interattiva è multilingue, non i README.**

---

## Indice

- [Perché questo progetto](#perché-questo-progetto)
- [Caratteristica principale: un file autonomo al 100%](#caratteristica-principale-un-file-autonomo-al-100)
- [La guida interattiva è multilingue](#la-guida-interattiva-è-multilingue)
- [Numeri chiave](#numeri-chiave)
- [Struttura dell'interfaccia](#struttura-dellinterfaccia)
  - [Scheda Info](#tab-infos)
  - [Scheda Colori](#tab-colors)
  - [Scheda Icone](#tab-icons)
  - [Scheda Note](#tab-about)
- [Il simulatore in tempo reale](#il-simulatore-in-tempo-reale)
- [La tecnica per tingere le icone](#la-tecnica-per-tingere-le-icone)
- [Copia e incolla con un clic](#copia-e-incolla-con-un-clic)
- [Identità visiva: un design "meta"](#identità-visiva-un-design-meta)
- [Come sono state estratte e integrate le icone](#come-sono-state-estratte-e-integrate-le-icone)
- [Aggiungere o aggiornare una lingua della guida interattiva](#aggiungere-o-aggiornare-una-lingua-della-guida-interattiva)
- [Affidabilità delle informazioni e limiti noti](#affidabilità-delle-informazioni-e-limiti-noti)
- [Compatibilità e accessibilità](#compatibilità-e-accessibilità)
- [Stack tecnico](#stack-tecnico)
- [Licenza](#licenza)

---

## Perché questo progetto

No Man's Sky permette di personalizzare i nomi (basi, astronavi, fregate, multiutensili, contenitori di stoccaggio, sistemi stellari…) grazie a un sistema di tag di testo — colori e icone — che **non è documentato ufficialmente da nessuna parte** da Hello Games. Le informazioni esistono, ma sono sparse: screenshot di tabelle di configurazione interne, prove empiriche dei giocatori sui forum, guide della community parziali e a volte obsolete.

**NMS_TC** raccoglie, verifica, corregge e presenta queste informazioni in un'unica forma, strutturata e subito utilizzabile — pensata per essere consultata sia come documentazione di riferimento sia come strumento di lavoro mentre si gioca.

---

## Caratteristica principale: un file autonomo al 100%

La guida è distribuita sotto forma di **un solo file `.html`** (tutte le lingue comprese), senza bisogno di cartelle aggiuntive per funzionare.

In pratica, questo significa:

- **Nessuna installazione.** Si apre il file in un qualsiasi browser moderno, e basta.
- **Si può spostare e rinominare liberamente.** Il file non dipende da alcun percorso relativo verso altri file.
- **Funziona offline.** Tutti i dati (colori, icone, logica di ordinamento, simulatore, testi di tutte le lingue) sono incorporati direttamente nel file — vedi la sezione [Come sono state estratte e integrate le icone](#come-sono-state-estratte-e-integrate-le-icone) per il dettaglio tecnico dell'integrazione delle immagini.
- **Una sola dipendenza esterna non critica**: i font (Google Fonts, tramite CDN — *Rajdhani*, *IBM Plex Sans*, *JetBrains Mono*). Senza connessione internet, la visualizzazione passa semplicemente ai font di sistema predefiniti del browser; nessuna funzionalità va persa.

Questa scelta di progettazione (incorporare tutto invece di dipendere da una cartella di asset esterni) ha un costo — un file più pesante (~466 KB) rispetto a una versione con immagini esterne — ma garantisce che un solo file basti sempre a far funzionare tutto, il che corrisponde direttamente all'uso previsto: uno strumento che si condivide, si scarica o si sposta senza doversi mai preoccupare di file mancanti.

---

## La guida interattiva è multilingue

La guida interattiva esiste in **più lingue in un unico file**: non c'è un file per lingua.

- **Selettore di lingua**: in alto a destra dello schermo, un menu mostra ogni lingua con il suo nome, preceduto da una bandiera (ad esempio «Français», «English», «Español»). La scelta si applica subito a tutta la guida: testi, tabelle, messaggi del simulatore.
- **Lingua scelta automaticamente**: una lingua richiesta nell'indirizzo (`?lang=es`) ha la priorità; altrimenti la guida riprende la scelta memorizzata, poi la lingua del browser se è disponibile, altrimenti il francese. La lingua visualizzata viene poi memorizzata nel browser.
- **Link diretto a una lingua**: a ogni cambio di lingua, l'indirizzo della guida si aggiorna (`…/NMS_txt_code.html?lang=fr`); basta copiarlo per condividere la guida nella lingua visualizzata. Un valore sconosciuto viene semplicemente ignorato. Questo link riguarda la versione online.
- **Lingue attualmente disponibili**: il **francese** (lingua sorgente), l'**inglese**, lo **spagnolo** e l'**italiano**.
- **Testo mancante in una lingua**: al suo posto viene mostrata la versione francese, mai un messaggio di errore.

> **Distinzione importante.** Solo la **guida interattiva** è multilingue. Questo README, invece, è scritto in una sola lingua; esiste una versione per lingua (`README_FR.md`, `README_EN.md`…), ciascuna tradotta separatamente.

> **🔧 Dettaglio tecnico:** ogni lingua è un blocco di dati JSON posto alla fine del file, e i testi della guida sono identificati da chiavi. La formattazione (grassetto, corsivo, codice, link…) viene mantenuta, ma ripulita tramite una lista bianca di tag HTML: una traduzione non può quindi introdurre codice attivo. Un blocco di lingua illeggibile viene ignorato senza disturbare gli altri. Ogni lingua aggiunge circa 14 KB al file. Il valore `?lang=` dell'indirizzo viene solo confrontato con le lingue disponibili: non viene mai inserito nella pagina.

---

## Numeri chiave

| | |
|---|---|
| 🎨 Tag di colore documentati | **59** |
| 🖼️ Tag icona documentati | **145** |
| 📂 Categorie di icone | **12** |
| 🔁 Duplicati di texture individuati | **21** |
| ⛔ Tag elencati ma non funzionanti | **16** |
| ❔ Tag con percorso di texture non confermato | **12** |
| 🖼️ Icone integrate in base64 nel file | **145 / 145** |
| 🎯 Icone identiche al pixel alle texture del gioco | **97 / 129** |
| 📝 Esempi concreti di uso reale | **10** |
| 🌍 Lingue della guida interattiva | **4** |
| 🔤 Testi da tradurre (chiavi di traduzione) | **116** |

---

## Struttura dell'interfaccia

La guida è organizzata in **4 schede**, pensate come un percorso di lettura logico: si impara la sintassi prima di consultare le tabelle di riferimento. Un **selettore di lingua**, in alto a destra, cambia la lingua dell'intera guida interattiva.

<a id="tab-infos"></a>
### 📘 Scheda Info

Il punto di ingresso della guida. Riunisce tutto ciò che serve sapere per usare i tag, senza doverlo cercare:

- **Sintassi completa**, con un'evidenziazione della sintassi dedicata (vedi più avanti) che distingue chiaramente il nome del tag, il testo libero dell'utente e i simboli strutturali (`<`, `>`, `<>`, `</>`, `IMG`).
- **Tecnica avanzata: tingere un'icona con un tag di colore** — spiega che un tag di colore attaccato subito prima di un tag `<IMG>` applica il suo colore all'icona come un filtro, con un riquadro **Importante** dedicato all'unica vera sottigliezza (dove mettere il tag di chiusura per tingere solo l'icona oppure l'icona *e* il testo che segue), e un confronto visivo dei due casi affiancati.
- **Riquadro di avvertenza** che ricorda onestamente che questo comportamento è osservato dalla community ma non documentato ufficialmente, con l'elenco dei limiti noti (icone già colorate che possono resistere alla tinta, comportamento non garantito al 100%).
- **Riquadro Consiglio** sul limite di caratteri dei campi di testo in gioco, con la raccomandazione di preferire i tag corti.
- **Sezione "Esempi concreti"**: dieci nomi realmente usati per organizzare i contenitori di stoccaggio in gioco, ciascuno mostrato con la sua resa visiva in tempo reale *e* il suo codice grezzo colorato, con un pulsante di copia a destra di ogni riga — la migliore dimostrazione pratica di tutto ciò che precede.

<a id="tab-colors"></a>
### 🎨 Scheda Colori

Una tabella di riferimento completa dei 59 tag di colore, con:

- **Un campione di colore a tutta larghezza** per riga (invece di un piccolo quadrato), con uno sfondo a scacchiera per visualizzare correttamente la trasparenza dei colori che ne hanno una.
- **Codice esadecimale esatto** e **percentuale di trasparenza** (mostrata solo quando è inferiore al 100%, per non appesantire inutilmente la visualizzazione).
- **Categoria di appartenenza** di ogni tag (Trasmissioni/Missioni, Risorse, Giocatori, Compagni, Mappa galattica, ecc.), allineata all'estrema destra di ogni riga.
- **Una barra d'intestazione dedicata**, visivamente distinta (sfondo e bordo propri, separatori verticali tra le colonne) invece di un semplice testo fluttuante sopra la tabella.
- **Quattro modalità di ordinamento cliccabili**: per nome (alfabetico), per colore (vedi sotto), per codice esadecimale (alfabetico) e per luminosità (dal più scuro al più chiaro). Cliccare una seconda volta sullo stesso criterio inverte l'ordine.
- **Una barra di ricerca** che filtra all'istante l'elenco per nome del tag.

**L'ordinamento "Colore" merita una spiegazione a parte.** Dopo diversi tentativi infruttuosi con algoritmi di ordinamento per tonalità (HSL classico, poi tonalità+luminosità, poi raggruppamento per famiglie percettive con soglie di vicinanza di tonalità), è risultato che nessuna formula matematica semplice riproduceva fedelmente la percezione umana di una sfumatura "ben ordinata" — due colori con la stessa identica tonalità ma con saturazione molto diversa (un blu vivo e un blu sbiadito, per esempio) non si classificavano mai in modo soddisfacente con il solo calcolo automatico. La soluzione adottata è stata **un ordine di riferimento classificato a mano**, colore per colore, a occhio — più affidabile di un algoritmo per cogliere sfumature come la vivacità di un colore o i neutri leggermente tinti (avorio, bianco sporco) che devono distinguersi dai grigi perfettamente neutri.

> **🔧 Dettaglio tecnico:** a differenza dell'ordinamento "Colore", l'ordinamento per **luminosità** si basa davvero su un calcolo automatico — la formula di luminanza percettiva standard ITU-R BT.601 (`0.299×R + 0.587×G + 0.114×B`), che pesa il verde più del rosso e del blu, in accordo con la sensibilità dell'occhio umano a ciascuna componente di colore.

<a id="tab-icons"></a>
### 🖼️ Scheda Icone

Una tabella di riferimento completa dei 145 tag icona, raggruppati in **12 categorie** (Risorse, Interfaccia, Fregate, Inventario, Voce/Rete, Bottino, Piattaforme/Controlli, Simboli del portale, Classe (C→S), Modalità di gioco, Costruzione base, Non funzionante), con per ogni icona:

- Un'**anteprima reale in miniatura** dell'icona (vedi la sezione dedicata all'estrazione più avanti — non sono simboli generici, ma le texture originali, estratte dai file del gioco).
- Il **nome esatto del tag**.
- La **texture del tag**: il file `.DDS` a cui punta il tag, quando è stato possibile identificarlo (da non confondere con la fonte dell'immagine, vedi `SOURCES.csv`).
- Un **badge di stato**, se necessario: `duplicato` (il tag punta esattamente alla stessa texture di un altro, con un nome diverso), `non funzionante` (tag presente nei dati ma senza texture assegnata — probabilmente un segnaposto riservato dagli sviluppatori) oppure `da verificare` (percorso di texture non confermato nelle fonti disponibili; 4 di questi tag mostrano un percorso probabile, trovato durante l'estrazione, in attesa di una conferma in gioco).

La categoria **"Classe (C→S)"** illustra una correzione di nome voluta: chiamata in origine "Classi di astronavi", è stata rinominata con una descrizione in sottotitolo che precisa che si tratta in realtà di una valutazione di qualità generica del gioco (astronavi, multiutensili, fregate, armi, tecnologie) e non di un sistema proprio delle astronavi.

Come per la scheda Colori, una **barra di ricerca** e un **filtro per categoria** permettono di muoversi rapidamente nell'elenco.

**Allineamento delle colonne**: ogni tabella di categoria usa larghezze di colonna fisse e identiche (`table-layout: fixed`), con la colonna "Tag" dimensionata sul nome di tag più lungo di tutta la guida (`BULLETPOINT_OFF`, 15 caratteri) — così nessun nome viene mai troncato e l'allineamento resta rigorosamente identico da una categoria all'altra, indipendentemente dalla lunghezza del titolo della categoria o dal contenuto delle sue righe.

<a id="tab-about"></a>
### ℹ️ Scheda Note

Il contesto e la trasparenza metodologica della guida:

- Promemoria che il sistema di tag non è documentato ufficialmente.
- Dettaglio tecnico della banca delle icone (da dove vengono le icone e come sono integrate, e dove trovare i singoli file PNG se servono altrove).
- Elenco esplicito dei duplicati di texture individuati, con esempi.
- Precisazione sui simboli del portale (da `PR_0` a `PR_15`) — confermati funzionanti in gioco dalla community (usati per rinominare sistemi stellari con il simbolo del loro indirizzo di portale).
- Elenco dei tag non funzionanti, presenti nei dati ma senza texture assegnata.
- Fonti usate per compilare la guida.

---

## Il simulatore in tempo reale

Posto in cima alla pagina, visibile da qualsiasi scheda, il simulatore permette di **scrivere una combinazione di tag e vederne subito la resa**, senza dover tornare in gioco per verificare:

- **Un pulsante di copia** (⧉) a destra del campo copia con un clic il codice scritto, pronto da incollare nel gioco (vedi [Copia e incolla con un clic](#copia-e-incolla-con-un-clic)).
- **Una crocetta di cancellazione** (×), posta nel campo, lo svuota e rimette il focus per ripartire da zero. Scompare da sola quando il campo è vuoto.
  - Il riquadro di anteprima subito sotto mantiene la stessa altezza, che contenga un'anteprima o che sia vuoto: resta nero e non si restringe quando si svuota il campo (altezza minima pari a una riga di contenuto).
- **Un testo indicativo** discreto, in corsivo, compare nel campo vuoto per guidare i nuovi utenti.
- Riconosce e mostra correttamente i tag di colore, i tag icona e la loro combinazione (compresa la tecnica della tinta, vedi sotto).
- **Gli errori nei tag vengono segnalati**: un colore o un'icona sconosciuti (per esempio `REDD` invece di `RED`) sono sottolineati in rosso, con una linea ondulata, direttamente nell'anteprima. Sotto l'anteprima, un piccolo riquadro per ogni errore indica quale sia, con il nome errato in rosso e, quando esiste, il nome corretto in verde. Questa riga compare solo quando c'è un errore: senza errori non viene mostrato nulla e l'altezza dell'anteprima non cambia.
- **Le maiuscole vengono controllate, come nel gioco**: `red`, `fuel` o `<img>` in minuscolo vengono segnalati con la correzione da apportare (`RED`, `FUEL`, `IMG`), mentre prima venivano mostrati senza alcun avviso o come testo grezzo.
- Le icone mostrate sono le vere icone estratte dal gioco (non approssimazioni).
- Utile per comporre un nome complesso (più tag combinati) e verificarne la resa prima di ricopiarlo in gioco.
- **Testo inserito sempre neutralizzato prima della visualizzazione**: incollare qualsiasi testo nel campo, anche volutamente "rotto" o copiato da una fonte poco affidabile, non può mai interferire con la pagina stessa.

> **🔧 Dettaglio tecnico:** il testo scritto viene prima interamente sottoposto a escape (trasformazione dei caratteri speciali HTML), poi il riconoscimento dei tag `<COLORE>` e `<IMG>...<>` avviene su questa versione con escape invece che sul testo grezzo. Tutto ciò che non è riconosciuto come un vero tag NMS resta quindi mostrato come testo inerte, mai interpretato come HTML attivo. La ricerca dei tag ignora le maiuscole solo per poter individuare gli errori di maiuscole; la validità, invece, resta rigorosa (esistono solo i nomi in maiuscolo), e i nomi vengono cercati nelle tabelle dei colori e delle icone senza mai toccare le proprietà interne degli oggetti JavaScript.

---

## La tecnica per tingere le icone

Il simulatore riproduce la tecnica che consiste nel mettere un tag di colore subito prima di un tag `<IMG>` per tingere l'icona:

- Realizzata tecnicamente tramite una **maschera CSS** (`mask-image`): il colore del tag viene applicato come sfondo, e il canale alfa del PNG dell'icona fa da stencil — il che riproduce fedelmente il comportamento osservato in gioco (il colore *sostituisce* i pixel dell'icona invece di fondersi con essi).
- **Non tutte le icone vengono tinte nel simulatore.** Un'analisi della saturazione (completata da un controllo visivo manuale) ha permesso di individuare una ventina di icone che hanno già un proprio colore significativo (badge di classe, icona PlayStation, diamanti dei giocatori in rete, alcune icone delle risorse...). Per maggiore leggibilità, queste vengono mostrate con il loro colore originale invece di essere appiattite in una silhouette — con una nota esplicita che precisa che in gioco la tinta può comunque applicarsi davvero e dare un risultato diverso dall'anteprima.

---

## Copia e incolla con un clic

Lo stesso pulsante dedicato (simbolo ⧉) è presente in quattro punti della guida:

- **Colori**: un pulsante a sinistra di ogni riga della tabella copia un modello pronto all'uso, `<NOME_COLORE>Testo</>`.
- **Icone**: un pulsante a sinistra di ogni riga della tabella copia direttamente la sintassi completa, `<IMG>NOME_ICONA<>`.
- **Esempi concreti** (scheda Info): un pulsante a destra di ciascuna delle dieci righe copia il codice grezzo dell'esempio, sempre identico.
- **Simulatore**: un pulsante un po' più grande, a destra del campo di inserimento e alla sua altezza, copia il codice così com'è scritto in quel momento (il testo grezzo, non l'anteprima). Il suo contenuto viene letto al momento del clic: segue quindi sempre le modifiche fatte nel campo, senza nulla da sincronizzare. Se il campo è vuoto, il clic non fa nulla, per non sovrascrivere gli appunti con il vuoto.
- **Riscontro visivo immediato**: il pulsante si trasforma brevemente in un segno di spunta (✓) per circa 1,4 secondi per confermare la copia; se il browser rifiuta la copia, al suo posto compare una croce rossa (✗), per non confermare mai a torto.
- Si basa sull'API `navigator.clipboard`, con un ripiego automatico (`document.execCommand`) per i browser più vecchi che non la supportassero.

---

## Identità visiva: un design "meta"

Scelta di progettazione deliberata: invece di definire una palette d'interfaccia arbitraria, **i colori d'accento dell'interfaccia stessa sono presi direttamente dai veri tag di colore del gioco** documentati nella guida:

| Uso nell'interfaccia | Colore | Tag NMS d'origine |
|---|---|---|
| Titoli di sezione, scheda attiva | Ciano | `VISOR` |
| Riquadro "Consiglio", accenti generali | Arancione | `COMMODITY` |
| Messa in evidenza, testo sottolineato | Verde smeraldo | *(tonalità personalizzata, coerente con la famiglia dei verdi del gioco)* |
| Riquadro "Importante" | Viola | `SPECIAL` |
| Riquadro di avvertenza | Rosso | `TRANS_WAR` |

Questa scelta crea una coerenza tematica diretta tra il contenuto documentato e il vocabolario visivo usato per presentarlo — la guida si "veste" letteralmente dei colori che documenta.

---

## Come sono state estratte e integrate le icone

Dalla versione 2.1, le icone non vengono più ritagliate da screenshot: sono le **texture originali del gioco**, estratte direttamente dai suoi file, poi convertite e integrate nella guida:

1. **Estrazione.** Gli archivi `.pak` di No Man's Sky sono stati estratti con **NMSModTool v1.1.0.0**, per accedere alle texture dell'interfaccia in formato `.DDS`.
2. **Scelta della fonte migliore.** Una stessa icona esiste spesso in più copie nei file del gioco, a risoluzioni diverse. Per ogni tag è stata scelta la versione visivamente identica con la **risoluzione più alta**: 54 icone a 256 × 256, 26 a 128 × 128, 17 a 64 × 64 e 32 a 32 × 32 (di cui 3 tasti larghi a 64 × 32). Queste ultime non esistono in nessuna versione più grande nei file del gioco.
3. **Conversione e ottimizzazione.** Ogni texture è stata convertita in PNG con sfondo trasparente, poi alleggerita senza perdita di qualità: rimozione dei profili ICC e dei metadati.
4. **Controllo e ritocchi.** Ogni immagine è stata confrontata con la sua texture sorgente: **97 icone su 129 sono identiche al pixel** al loro `.DDS` d'origine. Le altre 32 sono state ritoccate, ingrandite o ricomposte quando il gioco ne offriva solo una versione troppo piccola o inadatta — per esempio i badge di classe, ricreati a partire dalla base opaca dei badge di spedizione, o `ARROWLEFT`, ottenuta per simmetria da `ARROWRIGHT`.
5. **Ridimensionamento.** Tutte le icone sono state poi ridimensionate in blocco in due set, 32 × 32 e 64 × 64 pixel. La guida integra la versione **64 × 64**, nitida anche sugli schermi ad alta densità.
6. **Codifica.** Ogni PNG (sfondo trasparente) è codificato in **base64** e memorizzato in un oggetto JavaScript (`ICON_DATA`) che associa ogni nome di file a una stringa `data:image/png;base64,...`, usata direttamente come attributo `src` dei tag `<img>` — esattamente come se l'immagine fosse ospitata online, solo che è fisicamente presente nel file.

> **🔧 Dettaglio tecnico:** la colonna «Texture del tag» della guida indica il file `.DDS` a cui punta il tag nelle tabelle di configurazione del gioco. Non è sempre il file da cui proviene l'immagine della banca, che può essere una versione più grande dello stesso disegno, archiviata altrove. Per ogni icona, il file `SOURCES.csv` della cartella `BANK_ICONS/` fornisce la corrispondenza completa: texture del tag, fonte dell'immagine, risoluzione d'origine e livello di corrispondenza.

Questo approccio spiega sia il peso del file (~466 KB, contro poche decine di KB per una versione solo testo) sia la sua totale portabilità: spostare, rinominare o condividere il file non compromette mai la visualizzazione delle icone.

Questo blocco di dati (`ICON_DATA`) è volutamente isolato alla fine dello script, separato da tutta la logica JavaScript che lo precede (vengono dopo solo i blocchi di lingua, semplici dati JSON) — un'organizzazione pensata perché la lettura del codice non sia mai sommersa da queste 145 lunghissime righe di testo codificato, e per facilitare l'aggiunta futura di icone da parte della community.

> **🔧 Dettaglio tecnico:** in JavaScript, una costante deve solo essere dichiarata prima di essere usata durante l'esecuzione — non necessariamente prima delle funzioni che la citano nel loro codice. `ICON_DATA` può quindi essere posto in fondo allo script senza rompere nulla, purché resti dichiarato prima dell'inizializzazione della pagina, che viene eseguita a caricamento completato.

I 16 tag elencati come non funzionanti non sono tutti semplici voci vuote: una parte di essi (icone generiche di pulsanti del controller) ha comunque la propria immagine già presente in base64 in `ICON_DATA`, senza esservi collegata nella tabella delle icone. Sono le uniche immagini ancora provenienti dalla vecchia banca, ritagliata da screenshot.

> **🔧 Dettaglio tecnico:** queste immagini sono tenute in riserva invece di essere eliminate, nel caso in cui Hello Games assegni loro un giorno una texture ufficiale in gioco — collegarle diventerebbe allora una semplice correzione di una riga, senza dover estrarre o codificare di nuovo nulla.

---

## Aggiungere o aggiornare una lingua della guida interattiva

Tradurre la guida interattiva non richiede **nessun nuovo file**: una lingua è un blocco di testo in più dentro `NMS_txt_code.html`.

**Due lavori distinti, da non confondere:**

| Cosa | Dove | Come |
|---|---|---|
| **Il blocco di lingua della guida interattiva** | all'interno di `NMS_txt_code.html` | prompt `prompt_translation_HTML_GUIDE_LANG.md`, controllato dagli script della cartella `docs/scripts/` |
| **Questo README in un'altra lingua** | un file separato (`README_EN.md`…) | prompt `prompt_translation_README_LANG.md` |

Il principio di lavoro:

1. **Il francese è la lingua sorgente.** Ogni nuova funzionalità si scrive prima in francese, con i suoi testi identificati da chiavi.
2. **Si traduce solo ciò che manca o è cambiato.** Lo script `trans_script_1_check_keys.py` elenca le chiavi da tradurre per una determinata lingua.
3. **Ogni blocco di lingua inizia con un campo `_meta`** che conserva il nome della lingua, la sua bandiera e i parametri di traduzione scelti (tono, variante, fedeltà).
4. **Controlli automatici** verificano le chiavi, i tag, gli esempi di codice, il comportamento e la robustezza della guida in ogni lingua.

---

## Affidabilità delle informazioni e limiti noti

La guida cerca di essere onesta su ciò che è confermato e ciò che non lo è:

- Il sistema di tag **non è documentato ufficialmente da nessuna parte** da Hello Games — tutte le informazioni provengono da tabelle di configurazione interne del gioco, da test in gioco e da fonti della community.
- I codici esadecimali dei colori provengono direttamente da una tabella di valori RGBA/HEX esatta — con un'unica eccezione (`TRANS_ANM`), il cui colore esatto non è stato possibile confermare nelle fonti più recenti.
- I tag contrassegnati come `non funzionante` o `da verificare` sono chiaramente indicati come tali invece di essere presentati con la stessa certezza del resto.
- La tecnica per tingere le icone è presentata come un comportamento osservato, non come una garanzia universale.
- Le lingue **scritte da destra a sinistra** (arabo, ebraico…) non sono ancora supportate dalla guida interattiva: la visualizzazione sarebbe errata.
- Le **bandiere** del selettore sono emoji: alcuni sistemi possono mostrare due lettere al posto della bandiera.

---

## Compatibilità e accessibilità

- **Responsive**: impaginazione adattata agli schermi stretti (colonne secondarie nascoste su mobile nella tabella dei colori, scorrimento orizzontale sulle tabelle delle icone, che mantengono una larghezza minima perché nessuna colonna venga schiacciata).
- **Browser moderni**: Chrome, Firefox, Edge, Safari — si basa su CSS Grid, `mask-image` e l'API Clipboard, disponibili in tutte le versioni recenti.
- **Accessibilità di base**: le due barre di ricerca e il filtro per categoria vengono annunciati correttamente ai lettori di schermo (`aria-label`), il campo del simulatore è associato a un vero `<label>` invece che a un semplice testo fluttuante, e anche il pulsante di copia e la crocetta di cancellazione del simulatore hanno un `aria-label`. Il **selettore di lingua** è un menu nativo etichettato per i lettori di schermo, e l'attributo `lang` della pagina segue la lingua scelta. Le **schede** seguono il modello di accessibilità standard (ARIA *tabs*): la scheda attiva viene annunciata, e si passa dall'una all'altra da tastiera con le frecce, Inizio e Fine. Anche ogni pulsante di copia delle tabelle ha un `aria-label`, e i campi in cui si scrivono i tag disattivano il correttore ortografico.
- **Nessun dato inviato da nessuna parte**: tutto viene eseguito localmente nel browser, senza alcuna connessione di rete necessaria dopo il primo caricamento dei font. Solo la **scelta della lingua** viene memorizzata, localmente, nel browser; non viene mai inviata. Una **politica di sicurezza dei contenuti** (CSP), integrata nel file, lo impone al browser: la pagina può caricare solo i font e non può contattare nessun altro server.
- **Senza JavaScript**: un breve messaggio, in francese, inglese, spagnolo e italiano, indica che la guida ne ha bisogno, invece di una pagina vuota.

---

## Stack tecnico

- **HTML/CSS/JavaScript vanilla** — nessun framework, nessuna dipendenza di build, nessuna fase di compilazione.
- **Font**: Rajdhani (titoli), IBM Plex Sans (testo corrente), JetBrains Mono (codice), tramite Google Fonts CDN.
- **Nessuna libreria di terze parti**: ordinamento, ricerca, filtri, simulatore ed evidenziazione della sintassi sono tutti JavaScript nativo scritto appositamente per questa guida.
- **Sistema di lingue fatto in casa**: le traduzioni sono dizionari JSON incorporati nel file, letti da JavaScript nativo, senza librerie di internazionalizzazione.
- **Caricamento dei font ottimizzato**: due `<link rel="preconnect">` stabiliscono la connessione verso i domini di Google Fonts ancora prima del caricamento del foglio di stile, riducendo la latenza percepita alla prima visualizzazione.
- **Immagini non bloccanti**: le 145 icone integrate usano `decoding="async"`, così che la loro decodifica non ritardi mai la resa del resto della pagina.
- **Codice convalidato con strumenti standard**: l'HTML supera la convalida `html-validate` (preset consigliato), a eccezione di due regole che segnalano titoli e pulsanti «vuoti» nel file sorgente, disattivate per scelta poiché il loro testo viene inserito al caricamento in base alla lingua; il CSS è stato controllato con Stylelint senza anomalie di fondo (solo preferenze di formattazione, lasciate così per una scelta di stile coerente); e il JavaScript è stato verificato con ESLint (regole consigliate), senza alcuna segnalazione. La procedura di revisione propria del progetto (strumenti, codice e documentazione) è descritta in `docs/revision.md`, con il suo prompt `docs/prompts/prompt_revision_NMS_TC.md`.

---

## Licenza

Questa guida è distribuita con licenza [**CC BY-NC-SA 4.0**](https://creativecommons.org/licenses/by-nc-sa/4.0/). Vedi il file [`LICENSE.md`](../../LICENSE.md) nella radice del repository per i termini completi.

No Man's Sky e tutti gli asset, i marchi e le proprietà intellettuali associati appartengono a Hello Games e/o ai rispettivi aventi diritto. Questa guida è una risorsa non ufficiale della community, senza alcun legame con Hello Games.
