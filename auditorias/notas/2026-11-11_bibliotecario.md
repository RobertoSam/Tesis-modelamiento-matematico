# Nota del bibliotecario — 11-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `780450d`. Encargo: cerrar, en lo verificable contra
fuentes oficiales, los `\pendiente` bibliográficos de la tesis LaTeX **fuera** del capítulo de
resultados: Said y Dickey (1984), la fuente del bootstrap por bloques conjunto, y un reintento
acotado (máximo dos búsquedas cada uno) de Frontier (1976) y Denimal (2001). Camiz y Diblasi
(2013) no se buscó otra vez (ya lleva seis búsquedas fallidas).

No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `data/`, `src/`, `R/` ni `notebooks/`.

## Archivos

- Nuevas fichas: `papers/said_dickey_1984.qmd` (FB-103) y `papers/frontier_1976.qmd` (FB-104).
- `tesis/referencias.bib`: entradas `said_dickey_1984` y `frontier_1976` (esta con campo
  `verificar`). Parseo con pybtex: 103 entradas, sin claves duplicadas, todas con ficha en
  `papers/`.
- `papers/camiz_pillar_2018.qmd`: la fila de la ref. [10] remite ahora a `frontier_1976`.
- `tesis/registro_verificacion.md`: filas de Frontier, Denimal, Said y Dickey y bootstrap conjunto
  actualizadas, y nueva sección «Pendientes fuera de resultados (11-11-2026)».

## Lo verificado y la fuente de cada dato

**1. Said y Dickey (1984)** · cerrado (metadatos); contenido: solo resumen.
- Crossref (api.crossref.org/works/10.1093/biomet/71.3.599): autores Said E. Said (primero) y
  David A. Dickey; título «Testing for unit roots in autoregressive-moving average models of
  unknown order»; *Biometrika*, 71(3), 599–607, 1984; Oxford University Press.
- Oxford Academic (academic.oup.com/biomet/article-abstract/71/3/599/258758): mismos datos, fecha
  (diciembre de 1984), afiliaciones y resumen. El resumen dice que la prueba se basa en aproximar
  un ARMA de orden desconocido por una autorregresión, que el estadístico sale de una regresión
  estándar y que su distribución límite tiene percentiles tabulados. **No** dice «aumentada», no
  da la regla del orden de la autorregresión ni de dónde salen las tablas.
- La resolución en doi.org no respondió (permiso no concedido a tiempo); no se reintentó.

**2. Bootstrap por bloques conjunto** · no identificado; no se fichó nada.
- Resumen del cap. 2 de `lahiri_2003` en SpringerLink («Bootstrap methods», pp. 17–43): dice que
  las secciones 2.5–2.7 describen métodos por bloques. No menciona observaciones vectoriales ni
  multivariadas; el texto es de pago. No sustenta el esquema.
- Una búsqueda web general (bloques del vector, mismos índices para todas las series) devolvió
  documentación de programas (rdocumentation, tsbootstrap), un *preprint* de arXiv y un PDF de
  Project Euclid. Ninguno es una fuente revisada por pares cuyo resumen oficial se haya visto y
  sustente el esquema; Project Euclid no es accesible en este entorno (ya registrado para Künsch,
  1989), y no se buscó otra ruta.
- Queda abierto. Sugerencia para una próxima sesión con acceso: revisar en el texto de Künsch
  (1989) o de Lahiri (2003, sec. 2.5) si el bootstrap de bloques móviles se define para
  observaciones con valores en R^d (lo que equivale a usar los mismos inicios para todas las
  series). Mientras no se vea, no se atribuye.

**3a. Frontier (1976)** · cerrado (metadatos); ficha preliminar.
- Búsqueda 1 (web): título en francés, localiza la obra en bases secundarias.
- Búsqueda 2 (Crossref, `query.bibliographic`) y registro del DOI
  (api.crossref.org/works/10.1016/0022-0981(76)90076-9): autor Serge Frontier; «Étude de la
  décroissance des valeurs propres dans une analyse en composantes principales: Comparaison avec
  le modèle du bâton brisé»; *Journal of Experimental Marine Biology and Ecology*, 25(1), 67–75,
  noviembre de 1976; Elsevier BV; idioma francés. Sin resumen en Crossref.
- No se leyó texto ni resumen (ScienceDirect no accesible desde 3c; no se intentó). La
  correspondencia con la ref. [10] de Camiz y Pillar (2018) no se cotejó: su lista de referencias
  sigue sin leerse.

**3b. Denimal (2001)** · sigue sin localizarse.
- Búsqueda 1: «Denimal 2001 "Hierarchical factorial analysis" ASMDA Compiègne proceedings».
- Búsqueda 2: «"ASMDA 2001" proceedings "Applied Stochastic Models and Data Analysis" Compiègne
  Denimal hierarchical factorial».
- Ambas devuelven Denimal (2007) (Numdam, EuDML) y una página del CNAM con otra ponencia del
  mismo congreso (Lorga da Silva, Bacelar-Nicolau y Saporta, «ASMDA 2001, 10th International
  Conference on Applied Stochastic Models and Data Analysis»), sin editorial, páginas ni ISBN de
  actas. No hay ficha ni entrada.

**3c. Camiz y Diblasi (2013)** · no se buscó (instrucción del encargo). Sigue el pedido a
Roberto: solicitar la referencia o el PDF al Dr. Camiz. Lo mismo valdría para Denimal (2001), que
el Dr. Camiz cita en Camiz y Roig (2011).

## Regla para el redactor (y el editor del informe)

- **`said_dickey_1984`** (cap. 4, `sec:met-diagnostico`, l. ~150): sustituir el `\pendiente` por
  la cita, p. ej. «…\textcite{dickey_fuller_1979}\verificar{…}, en su versión aumentada
  \parencite{said_dickey_1984}…». Sin `\verificar` de metadatos. Atribuirle **solo** la prueba de
  raíz unitaria que aproxima un ARMA de orden desconocido por una autorregresión (la versión
  aumentada). **No** atribuirle la regla de elección de rezagos del código ni los valores críticos
  que reporta el programa; si el texto los menciona, que se remitan al código. Quitarla de la
  lista de fuentes sin ficha del cap. 7. En APA: «Said y Dickey (1984)».
- **`frontier_1976`** (cap. 1, `sec:oe`, l. ~109; cap. 3, `sec:retencion`, l. ~484): sustituir el
  `\pendiente` por `\textcite{frontier_1976}` **con**
  `\verificar{ficha preliminar: texto no consultado; correspondencia con la ref. [10] de Camiz y
  Pillar (2018) no cotejada}`. Citarla solo como la obra que compara el decrecimiento de los
  valores propios de un PCA con el modelo de la vara quebrada (lo que dice el título). La fórmula
  de los valores esperados y la regla operativa de retención siguen apoyándose en la definición de
  la tesis y en Camiz y Pillar (2018), no en Frontier. En APA: «Frontier (1976)».
- **Denimal (2001)** (cap. 3, `sec:hfc`) y **bootstrap por bloques conjunto** (cap. 3,
  `obs:nulo-estructura`): los `\pendiente` siguen. En la observación del bootstrap, la frase «es
  una elección de la tesis» es la formulación honesta mientras no haya fuente.
- **Camiz y Diblasi (2013):** sin cambios.
- **Informe:** las mismas dos claves sirven con `@said_dickey_1984` y `@frontier_1976` (esta con
  nota `VERIFICAR` del mismo contenido). Las notas `[CITA PENDIENTE]` de Said y Dickey (cap. 3,
  «Diagnóstico de las series sin transformar») y de Frontier (secciones de objetivos y de número de
  componentes) pueden cerrarse; el RmdF (3.1) puede citar a Frontier con su `[VERIFICAR]` ajustado
  («texto no consultado»).

## Accesos fallidos y lo que no se hizo

- doi.org (resolución de 10.1093/biomet/71.3.599): permiso no respondido a tiempo; no se reintentó.
- ScienceDirect y Project Euclid: no se consultaron (inaccesibles en esta iteración); no se buscó
  otra ruta.
- No se usó curl ni python para acceder a sitios; solo la herramienta de lectura web.
- No se rehízo el conteo de marcas: la tarea no toca los documentos.
