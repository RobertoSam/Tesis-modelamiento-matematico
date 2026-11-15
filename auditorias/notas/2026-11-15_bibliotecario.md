# Nota del bibliotecario — 15-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `9aa3b33`. Encargo: cerrar, en lo verificable contra
fuentes oficiales, tres `\pendiente` bibliográficos fuera del capítulo de resultados, con un
máximo de dos o tres búsquedas por tema:

1. Camiz y Diblasi (2013), ponderación gaussiana de las ventanas — `02_estado_arte.tex` l. ~294 y
   `03_marco_teorico.tex` l. ~778.
2. Fuente del STATIS dual — `02_estado_arte.tex` l. ~294.
3. Denimal (2001) — `03_marco_teorico.tex` l. ~609.
4. Si quedaba margen, el bootstrap por bloques conjunto — `03_marco_teorico.tex` l. ~1599.

No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `data/`, `src/`, `R/` ni `notebooks/`.

## Archivos

- Nueva ficha: `papers/lavit_et_al_1994.qmd` (FB-107, preliminar, texto parcial).
- `tesis/referencias.bib`: entrada `lavit_et_al_1994` con campo `verificar`. Parseo con pybtex:
  106 entradas, sin claves duplicadas, todas con ficha en `papers/`. (pybtex no estaba instalado en
  el entorno; se instaló con `pip` solo para esta comprobación.)
- `papers/lavit_1988.qmd`: la sección 7 remite ahora a la ficha de 1994.
- `tesis/registro_verificacion.md`: encabezado puesto al día; filas de `lavit_1988`, Denimal (2001),
  Camiz y Diblasi (2013) y bootstrap conjunto anotadas con lo de hoy; nueva sección «Pendientes
  bibliográficos (15-11-2026)».

## Lo verificado y la fuente de cada dato

### 1. STATIS dual · `lavit_et_al_1994` · ficha preliminar (texto parcial)

- La candidata ya figuraba en la ficha de `lavit_1988` (sección 7, «alternativa en revista»).
  Búsqueda 1 (título y autores): localizó tres copias: un facsímil en la *Three-Mode Bibliography*
  de Leiden, una copia en el repositorio Horizon del IRD y el registro de MaRDI.
- Horizon (IRD): redirigía a una página de mantenimiento; no se abrió.
- Facsímil de Leiden (three-mode.leidenuniv.nl/pdf/l/lavit_etal1994csda.pdf), leído con una
  herramienta que resume. **Cabecera impresa:** «Computational Statistics & Data Analysis 18 (1994)
  97-119», «North-Holland»; pie «© 1994 - Elsevier Science B.V.», «SSDI 0167-9473(92)00003-A».
  **Autores** en este orden y filiaciones: Christine Lavit, Yves Escoufier (Unité de Biométrie,
  ENSA.M-INRA-UM II, Montpellier), Robert Sabatier (Faculté de Pharmacie, UM I, Montpellier),
  Pierre Traissac (ORSTOM, Montpellier). **Título:** «The ACT (STATIS method)».
- **Contenido visto:** el resumen (ACT calcula distancias euclídeas entre configuraciones de las
  mismas observaciones en *K* circunstancias; datos de tres vías como *K* matrices) y, en la
  sección 1, los pasajes que presentan el programa «ACT (dual STATIS method)», cuya entrada son
  *K* grupos distintos de observaciones con las **mismas *J* variables**, con
  $V_k = X_k' D_k X_k$ como matriz de covarianzas de la etapa *k*.
- **No visto:** el número del fascículo (no figura en la cabecera) y el DOI en la editorial. El DOI
  10.1016/0167-9473(94)90134-1 solo se vio en MaRDI (portal.mardi4nfdi.de, base secundaria, que
  además fecha la publicación el 17-8-1995; se adopta 1994, el año impreso). La página del DOI en
  doi.org no respondió al permiso y no se reintentó. Ambos datos quedan en el campo `verificar`.
- Revista revisada por pares: válida para la tesis.

### 2. Camiz y Diblasi (2013) · sigue sin localizarse

- Búsqueda 1 (términos nuevos: «ventana móvil», «ponderación gaussiana», «análisis evolutivo»,
  «XLI Coloquio Argentino de Estadística»): el único resultado pertinente fueron las actas de
  E-ICES 8 (uncuyo.edu.ar/ices/upload/trabajos-completos-e-ices8-25-9-13.pdf; CNEA, Buenos Aires,
  2013, ISBN 978-987-1323-33-3; evento en Mar del Plata, 30-10 a 2-11-2012; compiladoras María
  Armeite y Emilia Elisa Molina). Su índice, que se vio completo, trae tres trabajos con Camiz
  (pp. 40, 52 y 430) y **ninguno** con Diblasi, sobre PCA evolutivo o sobre ventanas. Descartadas.
- No se hizo una segunda búsqueda: las seis anteriores (24-10 y 09-11) ya cubrieron título,
  autores, «evolutionary PCA» y las actas del Coloquio. Total: siete búsquedas sin resultado.
- Sigue el pedido a Roberto: solicitar la referencia o el PDF al Dr. Camiz.

### 3. Denimal (2001) · sigue sin localizarse

- Búsqueda 1: «"ASMDA 2001" proceedings Compiègne» con los posibles editores y la UTC: resultados
  sin relación.
- Búsqueda 2: «"Applied Stochastic Models and Data Analysis" 2001 Compiègne "Proceedings" ISBN»:
  un registro de Serval (UNIL) que podría corresponder a una ponencia del congreso; redirigía a
  iris.unil.ch y esa página no respondió al permiso, así que no se abrió ni se reintentó. Los demás
  resultados no corresponden al congreso.
- Aunque se hallaran las actas, haría falta ver la ponencia de Denimal en su índice: no se ficha.
  Total: cuatro búsquedas sin resultado (dos el 11-11 y dos hoy). Se sugiere añadirla al pedido al
  Dr. Camiz.

### 4. Bootstrap por bloques conjunto · no se buscó

Sin margen en la jornada después de los tres temas del encargo. Queda explícitamente para otra
jornada. Pista para entonces: verificar si Künsch (1989) o Lahiri (2003, secs. 2.5–2.7) definen
el bootstrap de bloques móviles para observaciones vectoriales (lo que equivale a usar los mismos
inicios de bloque para todas las series).

## Regla para el redactor (y el editor del informe)

- **`02_estado_arte.tex`, l. ~294** (`\pendiente{fuentes del STATIS dual y de la ponderación
  gaussiana…}`): dividir la marca.
  - **STATIS dual:** citar `\parencite{lavit_et_al_1994}` con
    `\verificar{número del fascículo y DOI sin ver en la editorial; texto leído en parte (resumen e
    introducción)}`. Lo único que se le atribuye es que el STATIS dual compara *K* tablas con las
    mismas variables observadas en grupos distintos de observaciones, a partir de sus matrices de
    covarianzas por etapa (con series estandarizadas, de correlaciones: esa equivalencia es de la
    tesis, no del artículo). **No** atribuirle fórmulas ni pasos del método. Lugar natural: la
    frase de l. ~275 («lo combinan con el STATIS dual, que compara las matrices de correlación de
    todas las ventanas…»). En APA: «Lavit et al. (1994)».
  - **Ponderación gaussiana:** dejar `\pendiente{Camiz y Diblasi (2013), fuente de la ponderación
    gaussiana de las ventanas: sin ficha}`.
- **`03_marco_teorico.tex`, l. ~778** (Camiz y Diblasi, 2013): sin cambios; el `\pendiente` sigue.
  Igual en el informe (`02_marco_teorico.qmd`, `[CITA PENDIENTE]` de la misma frase).
- **`03_marco_teorico.tex`, l. ~609** (Denimal, 2001, en la nota de `sec:hfc`): sin cambios; el
  `\pendiente` sigue. Igual en la nota `v2-c20` del informe.
- **`03_marco_teorico.tex`, l. ~1599** (bootstrap por bloques conjunto, `obs:nulo-estructura`): sin
  cambios; no se buscó hoy.
- **`03_marco_teorico.tex`, l. ~885** (STATIS dual en el mismo trabajo de 2010) y
  `07_pendientes.tex`, l. ~202: opcionalmente, añadir `lavit_et_al_1994` junto al STATIS dual en
  l. ~885, con el mismo `\verificar`; y en el cap. 7 quitar «la del STATIS dual» de la lista de
  fuentes faltantes.
- **Informe:** no tiene `[CITA PENDIENTE]` del STATIS dual (`git grep` del 15-11-2026), así que no
  hay marca que cerrar; si el editor incorpora la cita derivándola de la tesis, la nota `VERIFICAR`
  debe repetir la del `\verificar`.

## Accesos fallidos y lo que no se hizo

- doi.org (DOI de Lavit et al., 1994): permiso no respondido a tiempo; no se reintentó.
- Horizon (IRD): en mantenimiento (redirección a maintenance.ird.fr); no se buscó otra ruta.
- iris.unil.ch (registro Serval, posible ponencia del ASMDA 2001): permiso no respondido; no se
  reintentó.
- No se usó curl ni python para acceder a sitios; solo la herramienta de lectura web (python solo
  para validar el `.bib` local y editar el registro).
- No se buscó el bootstrap por bloques conjunto (sin margen).
- No se rehízo el conteo de marcas: la tarea no toca los documentos.
