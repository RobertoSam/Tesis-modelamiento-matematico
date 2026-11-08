# Nota del desarrollador · 8 de noviembre de 2026 · Iteración 3c, pedido del redactor LaTeX

Rama `iteracion-3c`. Atiende las secciones «Macros que faltan» y «Productos pedidos» de
`auditorias/notas/2026-11-07_redactor-latex.md`. Sesión de seguimiento diario, sin Roberto presente.
No se tomó ninguna decisión metodológica, y todas las fechas de episodios se leen de
`data/referencia/episodios_referencia.csv` (regla 6).

## Resumen

- **Macros:** se agregaron las 113 pedidas a `herramientas/cifras_mapa.csv` (79 directas y 34 que
  requerían un resumen o una columna nueva). `cifras.tex` y `_cifras.yml` pasan de 71 a 184 cifras.
  **No queda ninguna faltante.** Los filtros de las 79 directas seleccionan exactamente una fila
  cada uno, como indicaba la nota del redactor. `transicionCuentaFecha` **es única** (julio de 2012).
- **Cifras existentes:** las 71 anteriores son idénticas byte a byte, en `cifras.tex` y en `_cifras.yml`.
  Todo CSV que ya existía conserva sus bytes, salvo los cuatro que reciben la columna `orden` al
  final y `R_paridad_python.csv`, que tiene una fila nueva y dos textos de criterio actualizados.
- **Productos:** se generaron la tabla de compatibilidad corte × episodio (h = 3 y h = 6, con paridad
  R–Python), la figura del dendrograma de la HFC en 3 clases y la figura de la trayectoria PCA-MM12
  con los cortes y los episodios.
- **Tesis:** compila (131 páginas, 0 avisos). Las marcas PENDIENTE bajan de 140 a **22**, y
  `\cifrafalta` queda en **0**.

## Archivos

| Archivo | Cambio |
|---|---|
| `notebooks/09a_datacion_pca.ipynb` | Agrega la columna `orden` (1, 2, …, cronológico, al final) en `09a_regimenes_pca.csv` y `09a_estabilidad_cortes.csv`, y la compara con R. Sección 5 nueva: `09a_compatibilidad_cortes.csv`, comparada con `R_compatibilidad_cortes.csv`. Sección 6 nueva: figura `09a_trayectoria_pca_mm12.png`. |
| `R/ciclo_financiero_final.Rmd` | Misma columna `orden` en `R_estabilidad_cortes.csv` y `R_regimenes_pca.csv`. Chunk nuevo `b6-compatibilidad`, que escribe `R_compatibilidad_cortes.csv`. Tabla de paridad: `orden` entra en las claves de estabilidad y regímenes, y hay una fila nueva para la compatibilidad. Escribe `R_paridad_resumen.csv` (filas y coincidencias). |
| `notebooks/07c_hfc_clases.ipynb` | Escribe `07c_hfc_bootstrap_resumen.csv` (media y mediana de `ari_3`, `ari_4` y `cofenetica`). Sección 5 nueva: figura `07c_hfc_dendrograma.png`. |
| `notebooks/07b_nulo_estructura.ipynb` | Escribe `07b_transiciones_d10_resumen.csv` (candidatas y candidatas que cuentan, por objeto). |
| `notebooks/05c_anexo_no_diferenciar.ipynb` | Escribe `anexo/05c_espectro_resumen.csv` (mediana × 100 por versión). |
| `herramientas/cifras_mapa.csv` | 113 filas nuevas. |
| `herramientas/no_regresion_dinamica.py` | Declara `09a_estabilidad_cortes.csv` y `R_estabilidad_cortes.csv` como ampliados por columna (`orden`). |
| `tests/test_compatibilidad.py` (nuevo) | 3 pruebas: `orden` y su paridad; la compatibilidad recalculada desde la definición y desde el archivo de episodios, y su paridad con R; los cuatro resúmenes recalculados desde sus CSV de origen. |
| `tesis_latex/cifras.tex`, `tesis/_cifras.yml` | Los regenera `generar_cifras.py` (no se editaron a mano). |
| `tesis_latex/cifras_stub.tex` | Retiradas las 113 macros `\cifrafalta` que ya define `cifras.tex`, con un comentario. Es el único archivo de la tesis que se editó. |

Archivos nuevos en `data/results/final/`: `09a_compatibilidad_cortes.csv`,
`R_compatibilidad_cortes.csv`, `R_paridad_resumen.csv`, `07c_hfc_bootstrap_resumen.csv`,
`07b_transiciones_d10_resumen.csv` y `anexo/05c_espectro_resumen.csv`. Figuras nuevas en
`reports/figures/final/`: `07c_hfc_dendrograma.png` y `09a_trayectoria_pca_mm12.png`.

No se tocaron `tesis/` (salvo `_cifras.yml`, que regenera el script), `papers/`,
`tesis/referencias.bib`, los capítulos de `tesis_latex/` ni el Rmd de exploración
(`R/tesis_ciclo_financiero.Rmd`, md5 `c21946b6…`, sin cambios). Los datos están congelados (D4).

## Comandos (en este orden)

```
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/09a_datacion_pca.ipynb
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')"
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/09a_datacion_pca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/07c_hfc_clases.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/05c_anexo_no_diferenciar.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=7200 notebooks/07b_nulo_estructura.ipynb
python3 herramientas/generar_cifras.py
python3 herramientas/generar_cifras.py --comprobar
python3 herramientas/exportar_parametros_diseno.py --comprobar
python3 -m pytest tests/
python3 herramientas/no_regresion_05.py
python3 herramientas/no_regresion_dinamica.py
latexmk -lualatex -cd tesis_latex/tesis.tex
```

El 09a se ejecuta dos veces: la primera escribe las tablas que lee la paridad del Rmd, y la segunda
compara las tablas de Python con los `R_*` nuevos. El 07b tarda unos 6 minutos.

**Entorno.** La sesión empezó sin R ni algunos paquetes de Python. Se instalaron por apt
(`r-base-core`, `r-cran-rmarkdown`, `knitr`, `ggplot2`, `scales`, `tseries`, `dendextend`,
`jsonlite`, `pandoc`, `biber` y `texlive-*`) y por pip (`statsmodels`, `nbconvert`, `pytest`). Las
versiones son las de la nota del 7-nov: R 4.3.3, rmarkdown 2.25, dendextend 1.17.1, statsmodels
0.15.0, nbconvert 7.17.2 y matplotlib 3.11.2. **Control de línea base:** antes de tocar el código se
renderizó el Rmd sin cambios, y todos los `R_*.csv` salieron idénticos a los versionados. Los
`--comprobar` y `pytest` también pasaron antes de los cambios.

## Pruebas y paridad

- `generar_cifras.py --comprobar`: exit 0 (184 cifras). `exportar_parametros_diseno.py --comprobar`: al día.
- `pytest tests/`: **58 passed** (55 anteriores + 3 nuevas).
- `no_regresion_05.py`: superada (37 archivos idénticos).
- `no_regresion_dinamica.py`: superada. 40 archivos idénticos; los ampliados solo por columnas al
  final (`orden` y las ampliaciones declaradas antes) conservan idénticas las columnas antiguas.
  Nulo de estructura: k* y RV idénticos.
- **Paridad** (`final/R_paridad_python.csv`): **56 de 56 «sí»** (antes 55 de 55). La fila nueva es
  la compatibilidad corte × episodio (30 filas, 0 diferencias). Las filas de estabilidad y de
  regímenes ahora incluyen `orden` en la clave (0 diferencias). `final/anexo/R_paridad_python.csv`:
  9 de 9, sin cambios.
- Rmd final: exit 0, 0 `Warning` en el log y 0 bloques `## Warning`/`## Error` en el HTML.
- Todo CSV de `data/results/final/` que ya existía, salvo los cuatro con `orden` y
  `R_paridad_python.csv`, quedó idéntico byte a byte tras volver a ejecutar 07b, 07c, 05c, 09a y el
  Rmd.
- Tesis: `latexmk` exit 0, 131 páginas, 0 avisos en `tesis.log`. Contadores del `.aux`:
  `npendiente` = **22** (antes 140) y `nverificar` = 82 (sin cambios). No queda ningún `\cifrafalta`
  en el PDF.

## Macros: lo que hay que saber

1. **Las 79 directas** se copiaron tal cual de la nota del redactor, con dos cambios de formato:
   - `pOEcuatro*` (8 macros) pasan de `decimal:2` a `decimal:3`. Con 200 réplicas, el p-valor es un
     múltiplo exacto de 0,005, y dos valores caen justo en el medio: 0,695 (nw = 24, uniformes) y
     0,475 (nw = 48, gaussianos). Con 2 decimales, la representación binaria los redondea hacia
     abajo (0,69 y 0,47), de forma inconsistente con el redondeo habitual. Con 3 decimales se
     muestran exactos.
   - `estabilidadCorte*` (5 macros, de las 34) pasan de `decimal:2` a `decimal:3` por la misma razón:
     0,855 se mostraba como 0,85, y 0,975 y 0,955 como 0,97 y 0,95.

   **Para el redactor:** si prefiere 2 decimales, debe decidir el redondeo (p. ej., formatear en
   porcentaje); no lo cambié en el texto.
2. **Columna `orden`:** va al final en `09a_estabilidad_cortes.csv` y `09a_regimenes_pca.csv` (y en
   sus `R_*`), para no alterar las columnas anteriores. El régimen *k* empieza en el corte *k*−1.
   Así, en la tabla del cap. 5 (líneas 446–450), `estabilidadCorteUno` acompaña al régimen 2, que es
   lo correcto.
3. **`transicionCuentaFecha` es única:** julio de 2012 (`07b_transiciones_d10_resumen.csv`, fila 2,
   columna `fecha_cuenta_unica`; origen `07b_transiciones_d10.csv`, fila 11: regla del 06, nw = 36,
   uniformes). Si en el futuro hubiera varias, la columna queda vacía y `generar_cifras.py` falla:
   no se elige una a mano.
4. **`filasParidad` = 56**, no 55, porque la tabla de compatibilidad agregó una comprobación de
   paridad.
5. Resúmenes: `ariTresMediana` 1,00, `ariTresMedia` 0,95, `ariCuatroMedia` 0,88 y
   `cofeneticaMediana` 0,99 (`07c_hfc_bootstrap_resumen.csv`, fila 2); medianas espectrales de
   93,4 % sin tendencia y 23,4 % en transformadas (`anexo/05c_espectro_resumen.csv`, filas 3 y 4,
   `mediana_pct`).

## Productos

### (a) Compatibilidad corte × episodio · `data/results/final/09a_compatibilidad_cortes.csv`

Implementa la `def:tolerancia` de la tesis (D7): $\tau$ es compatible con $e$ con tolerancia $h$
si $\text{inicio}(e) - h \le \tau \le \text{fin efectivo}(e) + h$. La distancia se mide al
intervalo, como en `obs:tolerancia`, y un episodio puntual termina en su mes de inicio. Hay una fila
por par corte × episodio (5 × 6 = 30), con `orden`, `corte`, `episodio`, `tipo`, `inicio`,
`fin_efectivo`, `lado` (antes/dentro/después), `distancia_meses`, `compatible_h3` y `compatible_h6`.
**No asigna** episodios a cortes ni decide qué corte «corresponde» a qué episodio.

| Corte (orden) | Compatible con h = 3 | Solo con h = 6 | Fila del CSV |
|---|---|---|---|
| 2008-12 (1) | Crisis financiera global (dentro, 0 meses) | — | 2 |
| 2010-03 (2) | ninguno (9 meses después de la crisis) | ninguno | 8 |
| 2014-04 (3) | Colapso de las materias primas (2 meses antes) | Taper tantrum (4 meses después) | 16, 15 |
| 2020-06 (4) | COVID-19 (2 meses después) | Guerra comercial (5 meses después) | 25, 24 |
| 2022-11 (5) | ninguno (31 meses después de COVID-19) | ninguno | 31 |

*Interpretación (una línea):* con h = 3, tres de los cinco cortes son compatibles con algún
episodio, y con h = 6 los mismos tres; el taper tantrum y la guerra comercial solo entran con h = 6,
y Kuczynski/Odebrecht no queda cerca de ningún corte.

*Dudas abiertas para Roberto:*
1. El corte es el primer mes del régimen en la trayectoria **suavizada con media móvil causal de 12
   meses**, que responde con rezago. ¿Debe medirse la compatibilidad con algún ajuste por ese
   rezago? No lo apliqué: sería una decisión metodológica nueva.
2. El corte de 2014-04 es compatible con dos episodios con h = 6 (taper tantrum y materias primas), y
   el de 2020-06 con dos (guerra comercial y COVID-19). La definición no dice cómo asignar un corte a
   un episodio cuando hay más de uno; la tabla solo informa.
3. El corte de 2014-04 es también el menos estable (0,400 de las réplicas,
   `09a_estabilidad_cortes.csv`, fila 4). ¿Se informa su compatibilidad con esa salvedad?

### (b) Dendrograma de la HFC · `reports/figures/final/07c_hfc_dendrograma.png`

Jerarquía de `clahfac` (port de Python, D6; sin `hclust`/`scipy`) dibujada con la convención de
`plot.hclust`: hojas en el orden de `order` y nodos en el punto medio de sus hijos, a la altura del
índice de agregación. Los colores son las 3 clases de `07c_hfc_clases3.csv`. El notebook comprueba
que coinciden con `partclas(hier, 3)` y que las alturas son monótonas. La línea discontinua marca
el nivel de corte entre la segunda y la tercera fusiones más altas.

*Interpretación:* C1 agrupa 11 series (créditos, M1, M3, TAMN, IPC, tipo de cambio, PBI, demanda
interna y reservas), C2 las 3 tasas de política, interbancaria y TIPMN, y C3 el índice BVL y el
EMBIG. C3 se une a C1 antes que a C2.

*Duda:* la altura de la última fusión aplasta visualmente las fusiones bajas. ¿Prefiere el asesor
una escala de raíz o logarítmica? No la cambié.

### (c) Trayectoria PCA-MM12 · `reports/figures/final/09a_trayectoria_pca_mm12.png`

Muestra los tres scores suavizados y estandarizados que entran en la partición de Fisher (d = 3), con
los 5 cortes de la datación principal en rojo y los 6 episodios del archivo único como bandas grises.

*Interpretación:* el PC1 suavizado es casi monótono (la tendencia que ya señala `sec:res-tendencia`).
A simple vista, los cortes acompañan sobre todo cambios de
PC2 y PC3. Es una lectura visual, no un resultado.

*Duda:* las bandas no llevan el nombre del episodio, solo la nota al pie de la figura. Si el redactor
lo necesita, se agregan etiquetas.

## Avisos para Roberto y para el redactor

1. **Transición de 2012-07 y h = 6.** La única candidata que cuenta con h = 3 (2012-07, regla del 06,
   nw = 36) **es un borde de ventana con h = 6** («Entra Colapso de las materias primas»;
   `07b_transiciones_d10.csv`, fila 11, columna `es_borde_6` = True). Con la tolerancia de
   sensibilidad no quedaría ninguna. Conviene que el texto de `sec:res-transiciones` lo diga.
2. **Los tres `\pendiente` del cap. 5 sobre estos productos** (líneas 420, 489 y 510 de
   `05_resultados.tex`) siguen en el texto: integrarlos corresponde al redactor. Los archivos ya existen.
3. La columna «Fase» de la tabla de regímenes del cap. 5 está escrita en el texto, no sale de una
   macro. No es un número, pero sale de `09a_regimenes_pca.csv` (`fase`). Si se quiere trazabilidad
   completa, puedo agregar macros de texto (`formato texto`).
4. El tilde de «Calinski-Harabász» (aviso 5 del redactor) no se tocó: cambiarlo altera bytes de CSV
   versionados y las claves de paridad. Si se decide corregirlo, se hace en una tarea aparte.

## Desviaciones respecto de `decisiones.qmd`

Ninguna. La compatibilidad implementa la `def:tolerancia` y la `obs:tolerancia` ya escritas en la
tesis (distancia al intervalo, D7). Lo que no está definido (ajuste por el rezago de la media móvil
y asignación de un corte con varios episodios compatibles) quedó sin implementar y está anotado
arriba como duda.
