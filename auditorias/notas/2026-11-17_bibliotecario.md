# Nota del bibliotecario — 17-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `d4841e9`. Encargo, con un máximo de dos o tres búsquedas
por tema:

1. Prioridad: fuente del bootstrap por bloques conjunto, con los mismos inicios de bloque para
   todas las series — `03_marco_teorico.tex` l. ~1599 (`obs:nulo-estructura`). Verificar si
   Künsch (1989) o Lahiri (2003) definen el bootstrap de bloques móviles para observaciones
   vectoriales.
2. Si quedaba margen: detección de cambios en la matriz de covarianzas de series multivariadas —
   `02_estado_arte.tex` l. ~235 (`sec:ea-cambio`).

No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `data/`, `src/`, `R/` ni `notebooks/`.

## Archivos

- `papers/lahiri_2003.qmd`: estado de lectura (texto parcial), secciones 4–6 con lo leído de la
  sec. 2.5 y la p. 176, y sus límites.
- `papers/kunsch_1989.qmd`: anotado el intento fallido de hoy.
- Nueva ficha: `papers/aue_et_al_2009.qmd` (FB-108, preliminar, resumen leído).
- `tesis/referencias.bib`: entrada `aue_et_al_2009` con campo `verificar`. Parseo con pybtex:
  107 entradas, sin claves duplicadas, todas con ficha en `papers/`. (pybtex no estaba instalado;
  se instaló con `pip` solo para esta comprobación.) La entrada `lahiri_2003` no cambia: sus
  metadatos ya estaban verificados en la editorial.
- `tesis/registro_verificacion.md`: encabezado puesto al día; filas de `lahiri_2003` y del
  bootstrap conjunto anotadas; nueva sección «Pendientes bibliográficos (17-11-2026)».

## Lo verificado y la fuente de cada dato

### 1. Bootstrap por bloques conjunto · `lahiri_2003`, sec. 2.5, p. 29 · fuente identificada

- **Künsch (1989).** Búsqueda 1 (título y resumen): el único enlace con texto era la versión de
  acceso abierto de Project Euclid («…/10.1214/aos/1176347265.full»). Devolvió la página del
  control antibots (Incapsula), como el 20-10-2026. No se reintentó ni se buscó otra copia. No
  se le atribuye el caso vectorial.
- **Lahiri (2003).** Búsqueda 2 («moving block bootstrap», «R^d-valued», sec. 2.5): localizó una
  copia de los capítulos 2 y 7 en el sitio docente de Kevin Sheppard
  (bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Lahiri_2and7.pdf).
  **No es la editorial**: la copia no trae portada ni página legal. Se identifica con el libro
  porque sus encabezados impresos («2. Bootstrap Methods», «2.5 Moving Block Bootstrap 25»,
  «176 7. Empirical Choice of the Block Size») y su paginación coinciden con el índice verificado
  en SpringerLink el 24-10-2026 (cap. 2, pp. 17–43; cap. 7, pp. 175–197). Leída con una herramienta
  que resume, sobre un texto con errores de OCR en los símbolos.
  - p. 25: observaciones $\mathcal{X}_n=\{X_1,\dots,X_n\}$ de una sucesión estacionaria;
    bloque $B_i=(X_i,\dots,X_{i+\ell-1})$, $1\le i\le N=n-\ell+1$ (bloques móviles solapados).
  - **p. 29** (primera de las dos observaciones que cierran la sección): «it is easy to see that
    the above description of the MBB and the "blocks of blocks" bootstrap applies almost verbatim
    if, to begin with, the observations $X_1,\dots,X_n$ were random vectors instead of random
    variables».
  - p. 176: el cap. 7 plantea la elección del bloque para un proceso estacionario débilmente
    dependiente $\{X_i\}_{i\in\mathbb{Z}}$ en $\mathbb{R}^d$.
- **Lo que sostiene:** que el bootstrap de bloques móviles se aplica a observaciones vectoriales.
  Remuestrear bloques del vector de 16 incrementos $\Delta\mathbf{x}_t$ equivale a usar el mismo
  inicio para todas las series. **Esa equivalencia es lectura de la tesis**: es inmediata, pero el
  libro no la escribe así.
- **Lo que no sostiene:** resultados de validez asintótica del caso vectorial (la observación de
  la p. 29 se refiere a la descripción del método), ni nada sobre la regla de la tesis de
  $\lceil n'/L\rceil$ inicios con recorte final, ni sobre series no estacionarias. No se
  leyeron las demostraciones ni los caps. 3–6.

### 2. Cambio en la matriz de covarianzas · `aue_et_al_2009` · ficha preliminar (resumen)

- Búsqueda 3 (título y autores de un artículo conocido de la literatura de *change-points* en
  covarianzas): resultados en arXiv, Penn State Pure, MaRDI y agregadores.
- **arXiv:0911.3796** (página de resumen): título, los cuatro autores en orden y el campo
  «Journal reference»: «The Annals of Statistics, 2009, Vol. 37, No. 6B, 4046–4087»; DOI
  10.1214/09-AOS707.
- **Penn State Pure** (repositorio institucional): título; autores Alexander Aue, Siegfried
  Hörmann, Lajos Horváth y Matthew Reimherr; *Annals of Statistics*, vol. 37, núm. «6 B»,
  pp. 4046–4087; diciembre de 2009; DOI 10.1214/09-AOS707; «Published»; revisado por pares.
  Resumen coincidente con el de arXiv.
- **No visto:** la página de la editorial (Project Euclid, bloqueado como en el tema 1) ni
  Crossref (api.crossref.org: el permiso no se respondió a tiempo; no se reintentó). Queda en el
  campo `verificar`.
- **Contenido (solo el resumen):** un contraste asintótico, no paramétrico, de la estabilidad
  de las volatilidades y covolatilidades de series multivariadas, lineales y no lineales;
  aplicable a muchos modelos GARCH multivariados; sin estimar parámetros; útil en dimensión alta.
  Incluye simulación, una aplicación a datos financieros y extensiones a cambios múltiples y a
  cuarto momento infinito.
- Revista con revisión por pares: válida para la tesis.

## Regla para el redactor (y el editor del informe)

- **`03_marco_teorico.tex`, l. ~1599** (`obs:nulo-estructura`, inciso (d)): sustituir el
  `\pendiente` por una cita a Lahiri. Propuesta de redacción: «El esquema con los mismos inicios
  para todas las series es el bootstrap de bloques móviles aplicado a las observaciones
  vectoriales $\Delta\vx_t$, cuya descripción se extiende sin cambios a vectores aleatorios
  \parencite[sec.~2.5, p.~29]{lahiri_2003}\verificar{texto leído en parte en una copia no
  oficial de los caps. 2 y 7; la equivalencia con los mismos inicios de bloque es de la tesis}».
  **No** atribuir a Lahiri ni a Künsch la validez asintótica del caso vectorial, la regla de
  $\lceil n'/L\rceil$ inicios ni el uso con incrementos de series no estacionarias. Künsch (1989)
  **no** se cita para este punto. En APA: «Lahiri (2003, sec. 2.5, p. 29)».
- **`03_marco_teorico.tex`, l. ~1465** (`\verificar` de `lahiri_2003`, «texto no consultado»):
  actualizar a «metadatos verificados; texto leído en parte (sec. 2.5 y p. 176) en una copia no
  oficial; se cita como manual del bootstrap por bloques». El `\verificar` de Künsch no cambia.
- **Informe** (`tesis/_capitulos/02_marco_teorico.qmd`, observación sobre los supuestos del nulo,
  `[CITA PENDIENTE: fuente del bootstrap por bloques conjunto…]`): derivarlo de la tesis con la
  misma cita, «(Lahiri, 2003, sec. 2.5, p. 29)», y una nota `VERIFICAR` que repita la del
  `\verificar`.
- **`02_estado_arte.tex`, l. ~235** (`sec:ea-cambio`): se puede sustituir el `\pendiente` por una
  frase que cite `\textcite{aue_et_al_2009}` con
  `\verificar{ficha preliminar: solo resumen leído; metadatos en el repositorio institucional y
  arXiv, no en la editorial}`. Lo único que se le atribuye es la existencia de un contraste
  asintótico no paramétrico de la estabilidad de volatilidades y covolatilidades (la matriz de
  covarianzas) de series multivariadas, aplicable a modelos GARCH multivariados y en dimensión
  alta. **No** describir el estadístico ni sus supuestos. Un contraste con la tesis que sí es
  legítimo: es un contraste de hipótesis con modelo y asintótica, frente a la lectura
  descriptiva y con nulo por remuestreo de la tesis. El informe no tiene marca equivalente
  (`git grep` del 17-11-2026); si el editor deriva la cita, repite la nota `VERIFICAR`.

## Accesos fallidos y lo que no se hizo

- Project Euclid (versión de acceso abierto de Künsch, 1989): control antibots; no se reintentó
  ni se buscó otra ruta.
- api.crossref.org (DOI 10.1214/09-AOS707): permiso no respondido a tiempo; no se reintentó.
- No se abrió Project Euclid para Aue et al. (2009): es el mismo sitio bloqueado.
- No se usó curl ni python para acceder a sitios; solo la herramienta de lectura web (python solo
  para editar archivos locales y validar el `.bib`).
- No se rehízo el conteo de marcas: la tarea no toca los documentos.
- Pendientes que siguen: Camiz y Diblasi (2013) y Denimal (2001) (pedido a Roberto); lectura de
  Lahiri en una copia de editorial o de biblioteca; metadatos de `aue_et_al_2009` y de
  `kunsch_1989` en la editorial.
