# Nota del bibliotecario · Iteración 3a · 20 de octubre de 2026

**Agente:** bibliotecario (`.claude/agents/bibliotecario.md`). **Rama:** `iteracion-3a`, sin
commit ni push. **Encargo:** sección 7 de `asesoria/2026-10-20_plan-iteracion-3.md`, apartado
«Bibliotecario» (prioridades 1, 2 y 3), más dos pedidos del coordinador durante la sesión:
consolidar los `\pendiente` del redactor LaTeX y registrar las cuatro marcas `[VERIFICAR]` nuevas
del desarrollador.

**Archivos modificados:** `tesis/referencias.bib`, `tesis/registro_verificacion.md`,
`papers/baldi_hornik_1989.qmd`, `papers/fisher_1958.qmd` y 31 fichas nuevas en `papers/`. No se
tocó `tesis_latex/`, `R/`, `notebooks/`, `src/` ni `data/`.

## 0. Condiciones de acceso

- Desde la terminal, el proxy rechaza todas las conexiones a sitios bibliográficos (doi.org,
  Crossref, JSTOR, editoriales, BCRP, FMI, BIS…), con un 403 de política. No se intentó
  sortearlo; la verificación se hizo con las herramientas web designadas.
- Con esas herramientas **no fueron accesibles**: doi.org, Taylor & Francis, Wiley,
  ScienceDirect, Project Euclid, Semantic Scholar, Persée (robots.txt), SAGE (una de dos
  páginas), gob.pe (D. S. 044-2020-PCM) y **bcrp.gob.pe** (control antibots Incapsula en todas
  las publicaciones). Las URL construidas a mano (Crossref API, T&F, documento de Cowles) fueron
  rechazadas por falta de procedencia. Hubo además una pausa por el límite de uso de la sesión.
- Consecuencia: cuando la página de la editorial no se pudo abrir, el dato se marcó `VERIFICAR`
  aunque coincida en varias fuentes secundarias. Cuando solo se vio el título de la página de la
  editorial en el buscador (que incluye volumen y número) y el DOI en su dirección, se aceptaron
  volumen, número y DOI, y se dejaron las páginas en `VERIFICAR`.

## 1. Conteo de marcas abiertas

| Medida | Antes (inicio de la sesión) | Después |
|---|---|---|
| Registro, tabla de obras: filas abiertas | 33 (de 34) | 45 sin cerrar + 2 cerradas solo en metadatos (de 50) |
| Registro, episodios: filas abiertas | 6 | 6 (las 6 con fuentes fichadas o localizadas; falta la convención) |
| Registro, marcas `\pendiente` no bibliográficas | — | 4 (tabla nueva) |
| `.bib`: entradas | 17 | 47 |
| `.bib`: entradas con `VERIFICAR` | 15 | 30 |

El número de filas abiertas **sube** porque el registro ahora cubre más cosas, no porque haya más
problemas en las obras que ya estaban:

- se separaron filas combinadas (Horn / vara quebrada / Rencher; Eckart y Young / Jolliffe;
  Bartlett / KMO / Kaiser; ADF / KPSS);
- se agregaron 7 marcas que no existían al inicio: las 4 nuevas del desarrollador, 3 `\pendiente`
  nuevos del redactor (cos², anti-imagen y Bruynooghe) y la fuente de KPSS ante quiebres;
- se agregaron 3 filas de pendientes de metadatos de las fuentes de episodios.

**Avance sobre las 33 filas abiertas del inicio:**

- **Cerradas:** Horn (1965), en metadatos, y la congruencia de Tucker, con
  `lorenzo_seva_ten_berge_2006`.
- **Cerradas solo en metadatos:** Eckart y Young (1936); Kaiser (1970) y Kaiser y Rice (1974).
- **Reducidas a un dato:** Baldi y Hornik (1989), que ya solo debe el DOI; Fisher (1958), que
  debe las páginas y la lectura.
- **Fichadas de forma preliminar, con un dato pendiente:** Caliński y Harabasz, Benzécri,
  Granger y Newbold, Phillips, Dickey y Fuller, KPSS (sin entrada en el `.bib`), Bartlett (1950,
  1951), Kaiser (1960) y Hubert y Arabie.
- **Sin cambios:** las demás, entre ellas Atoche Murrieta (2022), que no se pudo fichar
  (sección 7).

## 2. Prioridad 1 · fichas y entradas

«Verificado» significa visto en la fuente oficial que se indica. Las fichas declaran el estado de
lectura.

| Clave | Estado de lectura | Fuente de verificación | Pendiente |
|---|---|---|---|
| `eckart_young_1936` | Texto parcial (pp. 211–217, copia OCR) | Cambridge Core: vol. 1, n.º 3, sep. 1936, pp. 211–218, DOI | Condición de unicidad (p. 216, cortada) |
| `horn_1965` | Resumen | Cambridge Core y SpringerLink: 30(2), jun. 1965, pp. 179–185, DOI | — |
| `calinski_harabasz_1974` | Solo localizada | Título de la página de T&F en el buscador (vol. 3, n.º 1) y DOI en la URL | Páginas 1–27 (Utah bib, secundaria). Grafía: **Harabasz** sin tilde |
| `bartlett_1950` | Solo localizada | Título de la página de Wiley en el buscador y DOI en la URL; índice de 3(2) | Páginas 77–85 |
| `bartlett_1951` | Solo localizada | Oxford Academic: 38(3–4), 337–344, 1-12-1951, DOI | Contenido (fórmula) |
| `kaiser_1970` | Solo localizada | Cambridge Core: 35(4), dic. 1970, 401–415, DOI | Contenido (MSA) |
| `kaiser_rice_1974` | Resumen (ERIC) | SAGE: 34(1), abr. 1974, 111–117, DOI | Contenido (MSA) |
| `kaiser_1960` | Solo localizada | Título de la página de SAGE en el buscador y DOI en la URL | Volumen, número y páginas |
| `granger_newbold_1974` | **Texto completo** (copia del artículo publicado) | Cabecera del artículo: *J. Econometrics* 2 (1974) 111–120, North-Holland | Número del fascículo y DOI |
| `phillips_1986` | Resumen (RePEc) | RePEc/IDEAS (secundaria): 33(3), dic. 1986, 311–340 | Contrastar con Elsevier; DOI |
| `benzecri_1973` | Solo localizada | Open Library (OCLC 34619039): t. 2, Dunod, 1973, vi + 619 p., ISBN | Autoría, editorial, tomo 1 y **pasaje del principio** |
| `baldi_hornik_1989` (completada) | **Texto completo** (PDF del artículo en la página de P. Baldi, UCI) | Catálogo de la Koninklijke Bibliotheek: 2(1), 53–58 | DOI |
| `fisher_1958` (actualizada) | Solo localizada | Título de la página de T&F en el buscador: vol. 53, n.º 284, y DOI en la URL | Páginas; texto (caso multivariado) |

**Atoche Murrieta (2022): no fichada.** El buscador muestra en el repositorio de tesis de la PUCP
una entrada de autor «Atoche Murrieta, Lilian Katherine», pero la página se carga con JavaScript
y no devolvió contenido. No se localizó el título ni el año, así que no hay ficha ni entrada.
**Pedido a Roberto:** el PDF o el enlace del repositorio. Según la ficha de Camiz et al. (2026),
ya la revisó.

**Para el redactor LaTeX:**

- Las nuevas claves citables son `eckart_young_1936`, `horn_1965`, `calinski_harabasz_1974`,
  `bartlett_1950`, `bartlett_1951`, `kaiser_1960`, `kaiser_1970`, `kaiser_rice_1974`,
  `granger_newbold_1974`, `phillips_1986` y `benzecri_1973`.
- Las que llevan `VERIFICAR` en el `.bib` deben ir con `\verificar{}`.
- Tres precisiones de contenido:
  - En Eckart y Young no hay que detallar la condición de unicidad.
  - En Horn, el percentil 95 es una elección de la tesis, no una regla de Horn.
  - **No conviene presentar *laisser parler les données* como cita textual de Benzécri (1973)**:
    no se localizó el pasaje (sección 7).

## 3. Prioridad 2 · fuentes de los episodios: tabla de opciones

**La convención (anuncio o evento externo frente a impacto en el Perú) la decide Roberto
(decisión I).** La tabla solo dice qué fecha respalda cada fuente leída. Todas están fichadas y
tienen entrada en el `.bib`.

| Episodio | Fuente (clave) | Fecha que respalda | Tipo | Coincide con |
|---|---|---|---|---|
| Crisis financiera global | Lehman Brothers Holdings Inc., comunicado, anexo 99.1 del 8-K en EDGAR/SEC (`lehman_brothers_2008`) | 15-09-2008 | Anuncio / evento externo | Inicio 2008-09 (Rmd, `modelos_dl.py`) |
| | NBER, Business Cycle Dating Committee, 20-09-2010 (`nber_2010`) | Valle de la recesión de EE. UU. en 06-2009; pico en 12-2007 | Evento externo (ciclo de EE. UU.) | Fin 2009-06 (todos los archivos) |
| | BCRP, Memoria 2008 / Reporte de Inflación de marzo de 2009 / notas informativas de 2008 | — | Impacto en el Perú | **Localizadas, no accesibles** |
| *Taper tantrum* | Bernanke, testimonio ante el JEC, página del BIS (`bernanke_2013`) | 22-05-2013 | Anuncio | Inicio 2013-05 (Rmd); **no** 2013-04 (`06a`/`06b`) |
| | Reserva Federal, comunicado del FOMC (`reserva_federal_2013`) | 18-12-2013 (reducción de compras desde enero de 2014) | Anuncio de la decisión | Fin 2013-12 (todos) |
| | BCRP, Reporte de Inflación de junio de 2013 | — | Impacto en el Perú | **Localizado, no accesible** |
| COVID-19 | OMS, declaración del Comité de Emergencia (`oms_2020a`) | 30-01-2020 (ESPII) | Evento externo | Inicio 2020-01 (`06a`/`06b`) |
| | OMS, discurso del director general (`oms_2020b`) | 11-03-2020 (pandemia) | Evento externo | Inicio 2020-03 (Rmd) |
| | D. S. 044-2020-PCM (estado de emergencia nacional) | 15-03-2020 según el título del PDF en gob.pe (*El Peruano*) | Impacto en el Perú | **Localizado, no leído**; no fichado |
| | — | Fin del episodio | — | **Sin fuente** para 2020-09 ni para 2020-12 |
| Colapso de materias primas | Stocker, Baffes, Kose y Ohnsorge, Banco Mundial PRN/15/01 (`stocker_et_al_2015`) | Caída del petróleo desde 06-2014 | Evento externo (petróleo) | Inicio 2014-06 (`06b`) |
| | FMI, recuadro especial del WEO de abril de 2015 (`fmi_2015`) | Caída medida desde 09-2014; metales: pico en 2011 | Evento externo | Alternativa; para metales, pico anterior |
| | — | Fin del episodio | — | **Sin fuente** para 2016-03 |
| Kuczynski / Odebrecht | Congreso, temas tratados del Pleno (`congreso_2016`) | 28-07-2016 (juramentación) | Evento interno | Inicio 2016-07 (`06b`) |
| | Departamento de Justicia de EE. UU. (`doj_2016`) | 21-12-2016 (declaración de culpabilidad de Odebrecht; no menciona al Perú en lo leído) | Evento externo | Inicio alternativo |
| | Congreso, R. L. 008-2017-2018-CR (`congreso_2018`) | 23-03-2018 (aceptación de la renuncia) | Evento interno | Fin 2018-03 (`06b`) y fecha de la «renuncia» del cap. 2 |
| Guerra comercial EE. UU.–China | USTR, comunicado (`ustr_2018`) | 15-06-2018 (anuncio); 06-07-2018 (inicio del cobro) | Anuncio / aplicación | Inicio 2018-06 o 2018-07 |
| | Firma de la «fase uno» | 15-01-2020 | Evento externo | **Solo fuentes secundarias**; no fichada |

**Observaciones para la decisión I:**

- **Inicios sin fuente:** ninguna fuente respalda los de `06a`/`06b` para la crisis global
  (2008-07) y el *taper tantrum* (2013-04).
- **Fines con fuente:** solo la crisis global (06-2009), el *taper tantrum* (12-2013) y
  Kuczynski (03-2018) tienen una fecha de fin respaldada.
- **Impacto en el Perú:** con la convención de impacto, todas las fuentes necesarias son del BCRP
  (o el D. S. 044-2020-PCM), y ninguna se pudo leer. Habría que descargarlas a mano y entregarlas
  al bibliotecario.
- **Materias primas:** las fuentes halladas tratan el petróleo; el Perú exporta metales, cuyo
  pico el FMI ubica en 2011.

## 4. Prioridad 3 · propuestas del asesor y marcas nuevas del desarrollador

| Propuesta | Resultado | Clave | Marca en el código o en el texto |
|---|---|---|---|
| Bootstrap por bloques móviles (Künsch, 1989) | **Localizada, sin verificar el contenido.** Project Euclid bloquea el acceso; volumen, número y DOI tomados de su URL y páginas de fuentes secundarias. No se verificó que defina los bloques móviles solapados | `kunsch_1989` | Rmd l. 492; `src/remuestreo.py:19` |
| $n$ efectivo para correlaciones autocorrelacionadas | **Sin verificar.** Candidata: Pyper y Peterman (1998). Una fuente secundaria (arXiv:2401.02387, ec. 3) atribuye la misma estructura, sin truncar en $n/5$, a Quenouille (1947). No se comprobó el truncamiento $J = \lfloor n/5\rfloor$; si no está en la fuente, es una elección propia y debe declararse | `pyper_peterman_1998` | Rmd l. 556 y 1754; notebook 05, celda 5; `02_marco_teorico.tex:485` |
| $n$ efectivo de Kish | **Obra verificada (catálogo de Penn), fórmula no.** Falta la página de $1/\sum\omega^2$ | `kish_1965` | Plan, apunte 5 |
| ADF (Dickey y Fuller) | Localizada; páginas pendientes. La versión **aumentada** se atribuye a Said y Dickey (1984): no verificada ni fichada | `dickey_fuller_1979` | Rmd l. 1332, 1963 |
| KPSS (Kwiatkowski et al.) | Resumen del documento de trabajo de Cowles (3 autores). **La lista de autores de la versión publicada no se vio en ninguna fuente oficial: sin entrada en el `.bib`** | `kwiatkowski_et_al_1992` (solo ficha) | Rmd l. 1334, 1963 |
| Raíz unitaria con quiebre (Perron, 1989) | **Verificada (resumen de la Econometric Society)** para ADF. **No sirve para KPSS**, que es de 1992. Hace falta otra fuente; además, el efecto de un quiebre sobre KPSS suele describirse como rechazo excesivo de la estacionariedad, no como pérdida de potencia (por verificar). Se informa al desarrollador; no se corrige su texto | `perron_1989` | Rmd l. 1964 |
| Congruencia de Tucker y umbrales 0,85 y 0,95 | **Verificada.** El resumen oficial (Hogrefe) dice: «.85-.94 corresponds to a fair similarity, while a value higher than .95 implies that [they] can be considered equal». Precisión: 0,85 es similitud aceptable, no equivalencia | `lorenzo_seva_ten_berge_2006` | Rmd l. 1324; `02_marco_teorico.tex:976` |
| Criterio de Rencher (OE6) | **No verificado.** Falta saber qué criterio y qué obra o edición se usa | — | `01_introduccion.tex:100`; `02_marco_teorico.tex:412` |
| Índice de Rand ajustado | Localizado (Hubert y Arabie, 1985) en RePEc; falta contrastar con Springer | `hubert_arabie_1985` | Rmd, A.4 |

## 5. Compatibilidad del `.bib` con biblatex-apa (biber) y citeproc

Se probó con un documento mínimo en el scratchpad (`\nocite{*}`, biblatex `style=apa`, biber), sin
tocar `tesis_latex/`. biber no emite advertencias. Cambios:

1. **Marcas `VERIFICAR`:** biblatex-apa imprime `note` (y también `annotation`) en la bibliografía
   del PDF; citeproc no. Las marcas pasaron a un campo propio, `verificar = {VERIFICAR: ...}`,
   que ignoran biber y citeproc, de modo que ninguna aparece en la bibliografía. La cabecera del
   `.bib` lo documenta. **El auditor debe buscar `verificar =`, no `note =`.**
2. `drehmann_borio_tsatsaronis_2012`: `number = {No. 380}` → `{380}`, porque biblatex-apa
   producía «N.o No. 380». Con citeproc ahora sale «(BIS Working Paper 380)», antes «No. 380».
3. `vincent_et_al_2008`: `@incollection` → `@inproceedings`.
4. Instituciones con «and» en `organization` (SEC, BIS): entre llaves dobles, porque biblatex
   las traducía como «y».
5. Fechas completas como `date = {AAAA-MM-DD}` en las entradas `@online`, que ambos motores leen.
   Se mantienen `journal` y `year` (biber los asigna a `journaltitle` y `date`).
6. `tuhin_et_al_2025`: con `eid`, citeproc pierde el número de artículo. Se mantuvo
   `pages = {Artículo 100}`, que ambos imprimen bien.

`quarto render tesis/06_referencias.qmd` termina sin advertencias, con 47 referencias y ninguna
marca VERIFICAR en la bibliografía. Las 33 fichas nuevas o modificadas renderizan una a una sin
advertencias.

**Observación de formato, fuera del alcance del bibliotecario:** citeproc, con `apa.csl` en
español, escribe las fechas completas como «2013, mayo 22»; APA 7 en español usa «2013, 22 de
mayo», que es lo que produce biblatex-apa. Corregirlo es tarea del editor del informe (CSL).

## 6. Consolidación del registro

- **`\pendiente` del redactor:** su nota (`auditorias/notas/2026-10-20_redactor-latex.md`)
  todavía no los lista, porque está en construcción. Se tomaron de los archivos `.tex` (lectura,
  sin modificarlos). Nuevos en el registro: cos² (`02:344`), anti-imagen (`02:442`) y Bruynooghe
  (`02:609`). Los demás remiten a filas existentes. Los cuatro no bibliográficos (portada y
  capítulos 3 a 5) van en una tabla aparte.
- **Marcas del desarrollador:** las cuatro tienen fila, con su línea del Rmd o su celda del
  notebook 05.

## 7. Pendiente y motivo (resumen)

- **Atoche Murrieta (2022):** página del repositorio ilegible; se requiere el PDF o el enlace.
- **Benzécri (1973):** pasaje del principio no localizado. Conviene preguntar al Dr. Camiz qué
  tomo y pasaje considera su fuente.
- **DOI de Baldi y Hornik, Granger y Newbold, Phillips y Perron, y páginas** de Caliński y
  Harabasz, Bartlett (1950), Dickey y Fuller, Künsch, Kaiser (1960), Fisher y Pyper y Peterman:
  las páginas de las editoriales y doi.org no fueron accesibles.
- **KPSS:** autores de la versión publicada.
- **BCRP:** ninguna publicación accesible. El impacto en el Perú de los episodios sigue sin fuente
  leída.
- **Sin buscar en esta iteración:** vara quebrada, Rencher, Jolliffe, Denimal, Camiz y Diblasi,
  Tukey, Lavit, Engle y Granger, filtros, Markov, Adam, anti-imagen, cos², Bruynooghe, Said y
  Dickey (1984), Tucker (1951) y Quenouille (1947).
- **Numeración de fichas:** las nuevas van de FB-019 a FB-049, correlativas a las existentes;
  la numeración del proyecto no está verificada (como ya advertían las fichas anteriores).

## Vuelta 1 (dictamen `auditorias/2026-10-20_iteracion-3a.md`)

**Archivos modificados:** `tesis/registro_verificacion.md`, `tesis/referencias.bib` (1 entrada
nueva: 48), `papers/tucker_1951.qmd` (nueva, FB-050) y `papers/lorenzo_seva_ten_berge_2006.qmd`
(secciones 6 y 7: remiten a la ficha nueva). Sin commit ni push.

### M-01 · Tucker (1951)

- **Verificado** en el repositorio de publicaciones de ETS (institución de Tucker;
  ets.org/research/policy_research_reports/publications/report/1951/avxw.html, 2026-10-20):
  autor «Tucker, Ledyard R», título *A Method for Synthesis of Factor Analysis Studies*, 1951,
  «PRS Report 984», «ETS Program Report», 120 páginas. No hay resumen ni DOI.
- **Queda `VERIFICAR`:** la entidad emisora y el lugar. El registro no los da; la lectura «PRS =
  Personnel Research Section, Department of the Army» es la de la literatura secundaria. Dos
  búsquedas no devolvieron un registro de DTIC ni del Ejército. Tampoco se comprobó que el
  informe defina el coeficiente (texto no consultado), así que la ficha es preliminar.
- Entrada `@techreport{tucker_1951}` (`type = {PRS Report}`, `number = {984}`, URL de ETS y campo
  `verificar`). biber (biblatex-apa) sin avisos; citeproc imprime «Tucker, L. R. (1951). *A method
  for synthesis of factor analysis studies* (PRS Report 984). URL».
- Fila nueva en el registro con la ubicación en los dos documentos.
- **Para el redactor y el editor:** el `\pendiente` de la definición `def:tucker` y el
  `[CITA PENDIENTE]` de `@def-tucker` dicen «sin ficha». Ahora pueden citar `tucker_1951` con su
  marca de verificación.

### N-08 y números de línea

La columna «Origen de la observación» pasa a ser «Marcas en los documentos». Remite a
capítulo, sección y etiqueta (`sec:…`, `def:…`), a la nota del informe (`v1-…`, `v2-…`), a la
sección o chunk del Rmd, a la celda de NB05 y al módulo y la función de `src/`. **No queda ningún
número de línea.** Esto resuelve N-08, cuyas cinco marcas están en `sec:validacion`. Los números
de línea ya habían vuelto a cambiar durante esta vuelta porque la tesis se está editando
(Tuhin: de la línea 1152 a la 1186).

### Correspondencia de marcas en los dos sentidos

Para el inventario se usó un guion con balanceo de llaves, que capta también las marcas
partidas en dos líneas. Resultado:

- Tesis: 53 `\verificar` o `\pendiente`. Es una instantánea: el redactor estaba editando en paralelo.
- Informe: 33 llamadas a notas `VERIFICAR` y 19 `[CITA PENDIENTE]`.
- Rmd: 36 `[VERIFICAR]`.
- NB05: 4 marcas (celdas 1, 5, 15 y 16).
- `src/`: 5 marcas.

**De las marcas al registro:** todas tienen fila. Antes faltaba Tucker (M-01).

**Del registro a las marcas:** se corrigieron ubicaciones vencidas.

- Horn ya no tiene marca en B.2 ni en A.2: está en `funciones` y en la sección 2.
- Perron no se cita en ningún documento.
- Lorenzo-Seva ya no tiene marca en `src/multivariado.py`.
- Kish no tiene marcas: se declara.
- La fila de quiebres estructurales ahora cubre ADF y KPSS (Perron como candidata para ADF).

**N-02 (Lorenzo-Seva):** la fila pasa a «Cerrado (metadatos); contenido: solo resumen». Así
coincide con el `\verificar` de la tesis y del informe, que es correcto. Horn se trató igual.

**Discrepancias que no le tocan al bibliotecario** (no se tocaron):

- **Redactor LaTeX (N-01 y N-02):** al cierre del inventario, la tesis ya tenía al día las notas
  de Baldi y Hornik y de Fisher, y había retirado el `\verificar` de Lorenzo-Seva. El informe
  conserva `v2-lst`: el registro lo describe y falta alinear el informe.
- **Redactor LaTeX y editor del informe (paridad):** el informe tiene notas que la tesis no tiene:
  - `v2-cmr`, en EPCA;
  - `v2-cr`, en `aede`;
  - `v2-tu`, en «Validación externa».

  A la inversa, la tesis tiene el `\verificar` de Tuhin en «LSTM-autoencoder», sin equivalente
  en el informe.
- **Desarrollador (N-03):** en el Rmd siguen las marcas «sin ficha» de obras que ya están
  fichadas: Horn, Caliński-Harabasz, Granger-Newbold, Phillips, ADF, KPSS, Bartlett, KMO y
  umbrales de congruencia. Lo mismo pasa en NB05 (celda 15) y en `src/multivariado.py`. Los pies
  de tabla «bajo 0,85, distinta» (N-04) no tienen respaldo en la ficha.

### Render

`quarto render tesis/06_referencias.qmd`: exit 0, sin advertencias, 48 referencias y ninguna
marca VERIFICAR en la bibliografía. Las fichas `tucker_1951` y `lorenzo_seva_ten_berge_2006`
renderizan sin advertencias.

### Pendiente y motivo

- Entidad emisora de Tucker (1951): no aparece en ninguna fuente oficial accesible.
- Contenido de Tucker (1951): no hay acceso al informe.

## Vuelta 2 · cierre (21 de octubre de 2026)

**N-13** (`auditorias/2026-10-21_iteracion-3a_vuelta2.md`): se actualizó la columna «Marcas en los
documentos» de cuatro filas del registro: `tucker_1951` (ya citado con `\verificar`, `v2-tk` y
marca en el Rmd), `lorenzo_seva_ten_berge_2006` (sin marca en los tres documentos; `v2-lst`
retirada), `granger_newbold_1974` (NB05 con marca propia) y `tuhin_et_al_2025` (marca de la tesis
en `sec:validacion` y `v2-tu2` del informe). **N-14** queda para la iteración 3b.
