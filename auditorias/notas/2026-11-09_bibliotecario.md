# Bibliotecario · 9 de noviembre de 2026 · Iteración 3c (pendientes del cap. 2)

**Alcance.** Sesión de seguimiento diario sin Roberto presente, rama `iteracion-3c`, commit de
partida `c564c35`. Encargo: cerrar las referencias que el redactor dejó como `\pendiente` en
`tesis_latex/capitulos/02_estado_arte.tex` (`sec:ea-ciclo` y `sec:ea-regimenes`; ver «Pendientes
del estado del arte» en `auditorias/notas/2026-11-07_redactor-latex.md`).

- Fichas nuevas: `bry_boschan_1971` (FB-100), `harding_pagan_2006` (FB-101) y
  `christiano_fitzgerald_2003` (FB-102).
- Fichas corregidas: `kwiatkowski_et_al_1992` (metadatos verificados) y `harding_pagan_2002` (nota
  sobre el índice de concordancia y referencias internas).
- Entradas nuevas en `tesis/referencias.bib`: las cuatro anteriores. El `.bib` pasa de 97 a 101
  entradas, todas con ficha; se parsea sin errores con pybtex (sin claves duplicadas). `biber` no
  está instalado en el entorno.
- Registro: `tesis/registro_verificacion.md`, sección nueva «Pendientes del cap. 2 (09-11-2026)» y
  filas actualizadas (Kwiatkowski et al., Camiz y Diblasi, filtros, obras candidatas).
- No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `data/`, `src/`, `R/` ni `notebooks/`.

**Cómo se verificó.** `curl` hacia api.crossref.org fue rechazado por el proxy del entorno; el
registro de Crossref se consultó con la herramienta de lectura web, que es la vía ordinaria de la
sesión. Dos consultas a Crossref devolvieron límite de frecuencia y funcionaron al repetirlas una
vez. RePEc/IDEAS/EconPapers solo sirvieron para localizar.

## Obras

**1. `bry_boschan_1971`** · texto parcial (cap. 2, pp. 7–63).
- Metadatos: página del libro en el NBER (título; Gerhard Bry y Charlotte Boschan; NBER; enero de
  1971; ISBN 0870142232; capítulos hasta la p. 216) y catálogo de la biblioteca de la Universidad
  de Filipinas («New York: National Bureau of Economic Research [c1971]»; serie *Technical paper,
  NBER, 20*). Sin DOI en las fuentes vistas.
- Discrepancia anotada: la página del NBER atribuye cada capítulo solo a Boschan; el PDF del
  cap. 2 lo encabeza con los dos autores. Se cita el libro con los dos.
- Lectura: el PDF del cap. 2 en nber.org, **mediante una herramienta que resume**. Procedimiento
  por etapas (curva de Spencer, promedio de 12 meses, promedio de corto plazo, serie sin suavizar)
  con reglas finales de duración mínima (15 meses el ciclo, 5 meses la fase, sin giros a menos de
  6 meses de los extremos). Esas cifras deben cotejarse en el PDF antes de citarlas textualmente.

**2. `harding_pagan_2006`** · resumen.
- Metadatos: Crossref (DOI 10.1016/j.jeconom.2005.01.023; *Journal of Econometrics*, 132(1),
  59–79, mayo de 2006); resumen en el portal de la ANU.
- **Ambigüedad, registrada y no resuelta a ciegas.** Hay cuatro obras de Harding y Pagan fechadas
  en 2006: este artículo y tres documentos de trabajo vistos solo en IDEAS («Measurement of
  business cycles», Melbourne WP 966; «The econometric analysis of constructed binary time
  series», Melbourne WP 963 y NCER WP 1). Crossref no muestra otro artículo de revista de ambos en
  2005–2007, salvo el de *Journal of Applied Econometrics* de 2005. Se fichó el artículo porque es
  el único revisado por pares y el único sobre sincronización, que es lo que nombra el capítulo.
- **Atribución del índice de concordancia: sin verificar.** El resumen de 2006 no lo nombra; el de
  2002 menciona «una nueva medida de prociclicidad». Sin los textos no se sabe cuál de las dos
  obras define el índice.

**3. `christiano_fitzgerald_2003`** · resumen del NBER WP 7257.
- Metadatos: Crossref (DOI 10.1111/1468-2354.t01-1-00076; *International Economic Review*, 44(2),
  435–465, mayo de 2003, Wiley) y la página del NBER (WP 7257, julio de 1999), que da la misma
  versión publicada. El asterisco del título en Crossref es una llamada de nota y se omite.
- Resumen: aproximaciones al filtro pasa-banda ideal en muestras finitas, basadas en proyecciones.

**4. `kwiatkowski_et_al_1992`** · resumen del documento de trabajo; metadatos cerrados.
- Crossref (DOI 10.1016/0304-4076(92)90104-y) registra **cuatro autores**: Denis Kwiatkowski,
  Peter C. B. Phillips, Peter Schmidt y Yongcheol Shin. Título sin subtítulo; *Journal of
  Econometrics*, 54(1–3), 159–178, octubre de 1992. Se cierra la duda de 3a: el documento de trabajo
  de Cowles tenía tres autores. ScienceDirect no se consultó.
- No confundir con Kwiatkowski, Phillips y Schmidt, *Econometric Theory* 7(4) y 8(4), que Crossref
  devuelve en la misma búsqueda.

**5. Camiz y Diblasi (2013)** · no localizada.
- Dos búsquedas web más, que se suman a las cuatro del 24-10-2026, sin resultado pertinente. No hay
  ficha ni entrada. Sigue el pedido a Roberto: solicitar la referencia o el PDF al Dr. Camiz.

## Regla para el redactor (y el editor del informe)

- **`bry_boschan_1971`:** citar como fuente del algoritmo de datación de puntos de giro. Puede
  describirse el procedimiento del cap. 2 en términos generales (etapas y reglas de duración
  mínima). Si se dan cifras (15 y 5 meses), cotejarlas antes en el PDF o acompañarlas de
  `\verificar{cifras del cap. 2 leídas con una herramienta que resume}`.
- **`harding_pagan_2006`:** citar como fuente de la **medición y las pruebas de sincronización**
  de ciclos. **No** atribuirle la definición del índice de concordancia. Si el texto la necesita,
  usar `\verificar{índice de concordancia: no se comprobó si se define en Harding y Pagan (2002) o
  (2006)}` o citar las dos obras como literatura de la concordancia sin decir cuál la define.
- **`christiano_fitzgerald_2003`:** citar como fuente del filtro pasa-banda de muestra finita. No
  atribuirle detalles que no estén en el resumen. Sirve para el contraste con la vía exploratoria,
  que no impone una banda de frecuencias.
- **`kwiatkowski_et_al_1992`:** puede sustituir los `\pendiente` de `sec:ea-regimenes` (cap. 2) y
  `sec:met-diagnostico` (cap. 4) por `\textcite{kwiatkowski_et_al_1992}` o `\parencite`, sin
  `\verificar` de metadatos. En APA son cuatro autores: «Kwiatkowski et al. (1992)». Mientras no se
  lea el texto, citarla solo por la prueba (nula de estacionariedad), no por la forma del
  estadístico ni por sus tablas.
- **Camiz y Diblasi (2013):** el `\pendiente` sigue (cap. 2, `sec:ea-factoriales`, y cap. 3,
  `sec:epca`).
- En el informe, las mismas cuatro claves sirven con `@clave`. La nota `[CITA PENDIENTE]` de
  Kwiatkowski et al. en el cap. 3 puede cerrarse.
- El cap. 7 (`07_pendientes.tex`, líneas ~202–203) lista estas obras como pendientes: el redactor
  debe actualizar esa lista.

## Accesos fallidos y lo que no se hizo

- `curl` a api.crossref.org: rechazado por el proxy del entorno (no se buscó otra ruta; se usó la
  herramienta de lectura web ordinaria).
- Crossref: dos respuestas con límite de frecuencia, resueltas al repetir la consulta una vez.
- ScienceDirect y la página de Wiley no se consultaron (ScienceDirect ya estaba bloqueado en 3c).
- No se ficharon los documentos de trabajo de Harding y Pagan de 2006 ni Hodrick y Prescott (1997).
- No se rehízo el conteo general de marcas: la tarea no toca los documentos. En `c564c35`,
  `02_estado_arte.tex` tiene 7 `\pendiente{`.
