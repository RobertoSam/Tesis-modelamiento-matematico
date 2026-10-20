# Nota del desarrollador · 19 de octubre de 2026 · Iteración 2

**Objetivo de la iteración:** puesta en marcha y paridad de la versión en R
(`R/tesis_ciclo_financiero.Rmd`). Se retoma un trabajo interrumpido por un reinicio del entorno.
Rama `main`, sin commit ni push.

**Entorno:** R 4.3.3; ggplot2 3.4.4, scales 1.3.0, tseries 0.10.55, dendextend 1.17.1,
rmarkdown 2.25, knitr 1.45; pandoc 3.1.3. Locale del servidor: `POSIX` en todas las categorías;
locales disponibles: `C`, `C.utf8`, `POSIX`. Rcamiz y AedeClahfac no están instalados
(`tiene_rcamiz = FALSE`), como se espera: el Rmd usa `R/camiz_port.R`.

**Datos verificados antes de modelar:**

- `data/processed/dataset_niveles_mensual.csv`: 228 filas, de 2007-01 a 2025-12, sin faltantes.
  Tiene 19 series y no 17: 17 entran al análisis y 2 son de referencia (crédito total del SF e
  IPC subyacente), como declara la sección 1 del Rmd.
- `data/processed/dataset_transformado_mensual.csv`: 227 × 17, de 2007-02 a 2025-12, sin
  faltantes.
- El calendario mensual es continuo en ambos archivos (`verificar_calendario` del Rmd y control
  propio en el script de paridad).

---

## 1. Observación O1 (bloqueante): fallo en `b1-datos`

**Diagnóstico: confirmado.** Lo reproduje con un Rmd mínimo en el scratchpad, que define los
literales `"Crédito consumo"` e `"Índice BVL"` y los compara con las columnas del CSV:

| Condición | `print(x)` | `Encoding(x)` | ¿coinciden con el CSV? |
|---|---|---|---|
| Locale POSIX, sin corrección | `"Cr<U+00E9>dito consumo" "<U+00CD>ndice BVL"` | `unknown` | `FALSE` |
| `Sys.setlocale("LC_CTYPE", "C.UTF-8")` en un bloque previo | `"Crédito consumo" "Índice BVL"` | `UTF-8` | `TRUE` |
| Sin corrección, lanzado con `LC_ALL=C.UTF-8` | `"Crédito consumo" "Índice BVL"` | `UTF-8` | `TRUE` |

Con un locale no UTF-8, knitr lee el Rmd como UTF-8, pero el analizador de R convierte cada
carácter no ASCII de un literal en la secuencia `<U+XXXX>`. Por eso `meta$columna` deja de
coincidir con los nombres que `read.csv` lee del archivo, y falla el `stopifnot` de `b1-datos`
(línea 462 del Rmd actual).

**¿Basta la corrección?** Sí. El bloque está al inicio de `configuracion`, y cada bloque de knitr
se analiza justo antes de evaluarse. Por eso el cambio de `LC_CTYPE` alcanza a todos los bloques
y a todo el código *inline* posteriores. El render completo terminó sin errores (sección 2).
Además revisé las categorías que la corrección deja en POSIX:

- `LC_COLLATE` sigue en `C`. Ningún resultado ordena cadenas alfabéticamente: los `order()` y
  `sort()` operan sobre números, y los factores llevan niveles explícitos.
- `LC_TIME` sigue en `C`. No se usan `%b`, `%B`, `months()` ni `weekdays()`.
- `LC_NUMERIC` debe quedarse en `C`, y así queda.

Hay un detalle cosmético sin efecto: los mensajes de `stop()` del propio bloque
`configuracion` se analizan antes del cambio de locale. Si se dispararan, mostrarían
`<U+00F3>`.

**¿Corrección dentro del Rmd o `LC_ALL=C.UTF-8` en el comando?** Recomiendo **mantener la
corrección dentro del Rmd**, por tres razones:

1. Es autocontenida. El comando oficial de `CLAUDE.md` y de la definición del auditor
   (`Rscript -e "rmarkdown::render(...)"`) no fija el locale. Una solución externa exige que todo
   el que renderice recuerde la variable de entorno, y el auditor ejecuta el comando literal.
2. En macOS desde RStudio no hace nada: allí la sesión ya es UTF-8 (`en_US.UTF-8`), así que
   `l10n_info()[["UTF-8"]]` es `TRUE` y el bloque no se ejecuta. Lo mismo vale para Windows con
   R ≥ 4.2, que usa UTF-8 de forma nativa. No hay riesgo de romper RStudio.
3. Falla de forma explícita. Si no existe ningún locale UTF-8, se detiene con un mensaje claro,
   en vez de producir el error críptico del `setequal`.

El único efecto colateral es que, si se llama a `rmarkdown::render()` desde una sesión
interactiva de R con locale POSIX (no desde RStudio en macOS), el `LC_CTYPE` de esa sesión queda
en UTF-8 después del render. Es inocuo. `LC_ALL=C.UTF-8 Rscript -e ...` sigue siendo una
alternativa válida para servidores y puede documentarse como tal, pero no hace falta.

**Archivo modificado:** `R/tesis_ciclo_financiero.Rmd`, +15 líneas al inicio del bloque
`configuracion` (ver `git diff`). No cambia ningún parámetro ni ningún cálculo.

---

## 2. Render completo

**Comando** (desde la raíz del repositorio, en segundo plano, con registro):

```
nohup bash -c 'Rscript -e "rmarkdown::render(\"R/tesis_ciclo_financiero.Rmd\")"' > /tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/rmd_full.log 2>&1 &
```

- **Parámetros:** los valores por defecto del YAML: `bootstrap_reps = 500`, `reps_nulo = 1000` y
  `semilla = 2026`. Horn usa su propia semilla, 42 (`horn()`), y el bootstrap de cortes usa
  `B_cortes = min(200, bootstrap_reps) = 200` réplicas. Esa cifra está fijada en el código
  (línea 2605) y el HTML la declara en el pie de las tablas.
- **Resultado:** `EXIT=0`, 283/283 bloques y `Output created: tesis_ciclo_financiero.html`. No hay
  advertencias ni errores en el registro: las dos coincidencias de «error» son los nombres de
  los bloques `b6-g-error` y `bB5-g-error`. El HTML no contiene secuencias `<U+XXXX>` ni salidas
  `## Error`.
- **Tiempo de render: 144 s** (2 min 24 s, medido de pared a pared e incluyendo pandoc). No hay
  caché de knitr (`cache` no aparece en el Rmd ni existen carpetas `_cache`).
- **Reproducibilidad:** el HTML generado es idéntico byte a byte (mismo MD5) al que había en
  disco de la corrida previa al reinicio, a las 19:18.
- **Archivos versionados regenerados: ninguno.** `git diff --stat` solo muestra
  `R/tesis_ciclo_financiero.Rmd | 15 +++++` (la corrección de O1). El HTML está excluido por
  `.gitignore:35` (`R/*.html`). Los CSV `data/results/R_*` conservan su MD5: el Rmd vigente no
  los escribe (ver 3.3).

---

## 3. Paridad Python–R

### 3.1 Cifras clave que el Rmd declara reproducir

| Resultado | R | Python (CSV de origen) | ¿Coincide? |
|---|---|---|---|
| Transiciones EPCA, vía transformada (seguimiento de PC1, ventana 60, paso 3) | 2013-05, 2017-11, 2018-02 | `data/results/06_epca_transiciones_detectadas.csv`, filas 2–4, columna `fecha_transicion_candidata` | Sí, idénticas |
| Regímenes del notebook 09, vía transformada (Fisher sobre PC1–PC3 con MM12 causal, regla de codo del 10 %) | k = 8; inicios 2009-06, 2010-07, 2013-03, 2016-04, 2020-03, 2021-12, 2023-11; primer mes 2008-01, último 2025-12 | `data/results/09_regimenes_pca.csv`, filas 2–9, columnas `inicio` y `fin` | Sí, idénticos |
| Transiciones EPCA en niveles con las 19 series del notebook 06 (PC2) | 2012-01, 2013-10, 2015-10, 2018-01 | `data/results/06_epca_transiciones_detectadas_niveles.csv`, filas 2–5 | Sí, idénticas |
| Regímenes en niveles (copia de 09 sin transformar) | k = 6; inicios 2008-12, 2010-03, 2014-04, 2020-06, 2022-11 | `data/results/niveles/09_regimenes_pca.csv`, filas 2–7, columna `inicio` | Sí, idénticos |

- *Interpretación:* la cadena PCA → MM12 → Fisher del Rmd y la EPCA por seguimiento de cargas
  reproducen exactamente las fechas de Python en ambas vías. El Rmd es, por tanto, una réplica
  fiel y no una reimplementación aproximada.
- *Dudas abiertas para Roberto:*
  - Las tres transiciones transformadas están concentradas: dos de ellas, 2017-11 y 2018-02,
    distan un solo paso de ventana. ¿Se leen como un único cambio?
  - En la vía transformada, el bootstrap de cortes (200 réplicas, ±3 meses) da el corte de
    2016-04 en 86 % de las réplicas y el de 2021-12 en 88 %, los menos estables. ¿Cómo se
    interpretan esos dos cortes?

### 3.2 Verificación independiente (script propio, fuera del Rmd)

Para no depender solo de lo que el Rmd afirma de sí mismo, escribí
`/tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/paridad.R`. El script
reutiliza solo las *definiciones de funciones* del Rmd (vía `knitr::purl`) y `R/camiz_port.R`,
reimplementa la regla del notebook 06 y compara con los CSV versionados. Ejecución:
`Rscript <scratchpad>/paridad.R <scratchpad>` (4 s). Resultado:
`/tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/paridad_resultado.csv`.
Las 16 pruebas coinciden.

| Prueba | R | Referencia (CSV) | ¿Coincide? |
|---|---|---|---|
| Valores propios del PCA transformado | dif. máx. 4,7e-11 | `07_rcamiz_valores_propios.csv`, columna `eigen`, 17 filas (Rcamiz) | Sí |
| Cargas (vector × √λ), d = 1..17, con signo | dif. máx. 5,7e-15 | `07_rcamiz_cargas.csv`, 17 × 17 | Sí (\*) |
| Horn: componentes retenidos | 4 | `08_ae_horn.csv` (autovalor > umbral p95 en PC1–PC4) | Sí |
| Scores PC1–PC3 | dif. máx. 1,8e-14 | `05b_scores_suavizados.csv`, columnas `PC1`–`PC3` | Sí |
| MM12 causal PC1–PC3 | dif. máx. 6,0e-15 | `05b_scores_suavizados.csv`, columnas `PC*_mm12_causal` | Sí |
| EPCA transformada: transiciones | 2013-05 2017-11 2018-02 | `06_epca_transiciones_detectadas.csv`, filas 2–4 | Sí |
| EPCA: número de ventanas | 56 | `06_epca_varianza_explicada.csv`, 56 filas | Sí |
| Regímenes 09: k, inicios, primer y último mes | 8; los 7 inicios; 2008-01 a 2025-12 | `09_regimenes_pca.csv`, filas 2–9 | Sí |
| SCE de Fisher, k = 1..10 | dif. máx. 0 (a 2 decimales) | `R_regimenes_criterios.csv`, columna `sce`, filas 2–11 | Sí |
| k por Calinski-Harabász (fórmula de `aede`) | 9 | `R_regimenes_criterios.csv`, máximo de `ch` (86,9, fila 10) | Sí |
| HFC: jerarquía (`ngr`…`Cum_%2`) | dif. máx. 4,6e-14 | `R_hfc_jerarquia.csv` (binario AedeClahfac) | Sí |
| `aede` con pesos uniformes: k_ch y cortes | 10; 2010-08 … 2023-01 | `R_aede_cortes.csv`, fila 2 (binario) | Sí |
| `aede` con pesos gaussianos (`nsd = 3`): k_ch y cortes | 10; 2010-11 … 2022-02 | `R_aede_cortes.csv`, fila 3 (binario) | Sí |
| HFC por ventanas: correlación cofenética | dif. máx. 6,7e-16 | `R_ehfc_cofenetica.csv`, 55 filas (binario) | Sí |

(\*) En la primera versión del script la prueba de cargas dio una diferencia de 0,40. La causa
es la escala, no el método: `07_rcamiz_cargas.csv` guarda correlaciones variable–componente
(vector propio × √λ), no vectores unitarios. La correlación entre columnas era 1 en todas las
dimensiones. Al comparar en la misma escala, la diferencia es de 5,7e-15, con signo, de modo que
la regla de signos de `pca_basico` coincide con la de Rcamiz en las 17 dimensiones, incluida
Dim_1, cuyo margen de signo es de solo 0,010 (`07_margen_signo.csv`, fila 2, columna `margen`).

- *Interpretación:* el port en R puro reproduce, con error de redondeo, las salidas del binario
  original del asesor (HFC, `aede` con ambos esquemas de pesos y la HFC por ventanas) y las de
  Python (PCA, Horn, scores, EPCA y datación).
- *Dudas abiertas para Roberto:* el margen de signo de Dim_1 transformado (0,010) es muy
  pequeño. Un cambio mínimo en los datos (por ejemplo, la extensión de la muestra desde 1985)
  podría invertir el signo de PC1 y, con él, la lectura «PC1 alto = …». Conviene tenerlo
  presente al interpretar.

### 3.3 Sobre `R_paridad_python.csv` y los CSV `R_*` (diferencia de procedencia, no de cifras)

- **Ningún `R_*` lo genera el Rmd vigente.** Los cinco archivos los escribía
  `R/anteriores/tesis_ciclo_financiero_v1.Rmd` (líneas 752–765), que corría sobre las series
  transformadas con el binario AedeClahfac. Se versionaron por última vez en `563f571` (16/10).
- **Tres de las cinco filas de `R_paridad_python.csv` quedan confirmadas con los datos
  vigentes:** «Horn» (fila 3), «Scores y MM12» (fila 4, 1,8e-14) y «EPCA réplica (06)» (fila 5).
  La «Datación PCA-MM12 (09)» (fila 6) también queda confirmada (3.2). La fila 2, «PCA (Rcamiz vs
  08)», compara con Rcamiz: aquí la confirmé indirectamente contra `07_rcamiz_*` (4,7e-11).
- Los otros cuatro `R_*` coinciden exactamente con lo que produce el port actual (tabla 3.2).
- **Propuesta (no implementada):** que el Rmd vigente, o un script `R/paridad_python_r.R`,
  regenere `R_paridad_python.csv` en cada render, para que el archivo de referencia del auditor
  no dependa de una versión archivada. El script del scratchpad sirve de base. No lo agregué
  porque cambia qué archivo es la referencia de paridad y reescribiría un CSV versionado: queda a
  decisión de Roberto o del orquestador.

### 3.4 Diferencias de método que el Rmd ya documenta (no son fallos de paridad)

- **El notebook 06 corre la EPCA en niveles con 19 series, no con 17.** Incluye el crédito total
  y el IPC subyacente. Con 17 series, el Rmd obtiene 5 transiciones en PC2 (2012-01, 2013-10,
  2015-10, 2017-10, 2018-01) frente a las 4 de Python. Es una desviación del análisis oficial
  D1, que usa 17 series; el propio Rmd la marca como «hallazgo».
- En niveles, la regla del 10 % del notebook 09 no elige k. Tanto el Rmd como las copias de
  `R/redes_python/` usan como respaldo el codo por caída máxima.

---

## 4. Coherencia (solo se señala, sin corregir)

### 4.1 Fechas de episodios sin fuente externa (regla 6 de `CLAUDE.md`)

Los episodios están escritos a mano, sin fuente externa citada, en al menos **cuatro lugares y
con dos versiones distintas**:

| Lugar | Crisis global | Taper tantrum | COVID-19 | Otros |
|---|---|---|---|---|
| `R/tesis_ciclo_financiero.Rmd`, líneas 152–156 (`episodios`) y 286 (`nota_episodios`) | 2008-09 a 2009-06 | 2013-05 a 2013-12 | 2020-03 a 2020-12 | — |
| `R/tesis_ciclo_financiero.Rmd`, líneas 1206 y 2688 (`covid`, `covid_t`, codificados aparte) | — | — | 2020-03 a 2020-12 | — |
| `notebooks/modelos_dl.py`, líneas 533–537 (`EPISODIOS_REFERENCIA`); el propio comentario dice que «deben sustentarse con fuente» | 2008-09 a 2009-06 | 2013-05 a 2013-12 | 2020-03 a 2020-12 | — |
| `notebooks/06a_*.ipynb` y `06b_*.ipynb` (`EPISODIOS`) | **2008-07** a 2009-06 | **2013-04** a 2013-12 | **2020-01 a 2020-09** | 06b: colapso de commodities (2014-06 a 2016-03) y Kuczynski/Odebrecht (2016-07 a 2018-03) |

**Resultados que dependen de las fechas** (no solo visualmente):

- **Python, notebook 09** → `data/results/09_discriminacion_episodios.csv` (falsas alarmas y
  sensibilidad por episodio). Son las cifras «falsas alarmas de 0,6–1,9 %» y «más de 56 %» que
  sostienen la evidencia de **D2** en `decisiones.qmd`. También dependen la columna
  `episodios_contenidos` de `09_regimenes_pca.csv` y `09_regimenes_lstm.csv` (ambas vías) y las
  copias en `data/results/niveles/`.
- **Rmd:**
  - las tablas que clasifican cada transición de la EPCA como cercana a un episodio (±12 meses;
    líneas 2085 y 3376);
  - la columna «Borde de ventana (±3 meses)» (`borde_ventana`, líneas 448–455), base del
    hallazgo «la transición puede ser la crisis o la pandemia vista desde el borde de la ventana»
    (A.3 y B.3);
  - la tabla de regímenes con los episodios contenidos (líneas 2648 y 3708);
  - el PCA sin la crisis o sin la COVID (líneas 1206–1209 y 1757; `sin_episodio`), que sostiene
    la lectura de robustez de PC3;
  - la clasificación de los meses por episodio en los planos factoriales (líneas 1619–1621 y
    3026);
  - la tabla de la Parte C, «Episodios conocidos» (líneas 3909–3920), que alimenta la
    comparación entre vías.
- **Solo visual:** las bandas grises de todos los gráficos (`capa_episodios`) y de los notebooks
  05b, 08 y 09. En 06a y 06b los episodios solo sombrean gráficos; los CSV
  `06a_*`/`06b_*_resumen*.csv` no tienen columnas que dependan de ellos.

*Interpretación:* el resultado más sensible es la evidencia de D2 sobre la detección fuera de
muestra (sensibilidad y falsas alarmas). Cambiar el inicio o el fin de un episodio en uno o dos
meses mueve esas tasas directamente.
*Dudas abiertas para Roberto:*

- ¿Qué fuente externa fecha cada episodio (cronologías del BCRP, la BIS, el NBER u otra) y con
  qué convención (anuncio frente a impacto en los mercados peruanos)? Ninguna de las dos
  versiones tiene ficha en `papers/`.
- ¿Los episodios adicionales de 06b (commodities, Kuczynski/Odebrecht) entran al conjunto de
  validación o se descartan?
- Una vez fijadas las fechas, conviene una sola definición, en `src/` o en un CSV de
  `data/processed/` leído por Python y por R, para evitar las cuatro copias actuales.

### 4.2 Notación de la EPCA ponderada: Rmd frente a `tesis/_capitulos/02_marco_teorico.qmd`

Verifiqué el código del port (`R/camiz_port.R`, `aede_r`, líneas 539–600) contra las ecuaciones
del marco:

- **Ventana:** el marco define $\mathcal{W}_t=\{t-\lfloor w/2\rfloor,\dots,t+\lceil w/2\rceil-1\}$.
  Tanto el Rmd (`fechas[inicios + VENTANA %/% 2]`) como `aede_r` (`rownames(serie)[(1 + nw/2):…]`)
  etiquetan cada ventana con ese mismo centro. **Coinciden.**
- **Pesos (@eq-pesos):** el marco usa $\nu$ como parámetro de forma; el port calcula
  `exp(-0.5 * (((i - (nw+1)/2) / ((nw-1)/sqrt(2))) * nsd)^2)` normalizado. La fórmula es la misma,
  con $\nu \equiv$ `nsd`. **Diferencia de notación:**
  - el Rmd habla solo de «pesos gaussianos (`nsd = 3`)», sin fórmula y sin la equivalencia con
    $\nu$;
  - el marco no dice qué valor de $\nu$ se usa (3) ni que $\nu$ es `nsd`.

  Propuesta: escribir «$\nu$ (`nsd` en `aede`) $= 3$» en ambos lados.
- **Media y correlación ponderadas (@eq-epca):** `.bstatw_ac` usa pesos que suman uno. Con
  $\omega_s=1/w$, el «seguimiento de cargas» del Rmd (`crossprod(estandarizar(·))/w`, desviación
  poblacional) es el caso uniforme de la ecuación. **Coinciden**, como dice la nota al pie
  `v2-impl` del marco.
- **No están en el marco:**
  1. **El criterio de transición del notebook 06**: correlación entre cargas consecutivas menor
     que su media menos una desviación estándar poblacional. De él salen las fechas 2013-05,
     2017-11 y 2018-02. La Definición 3 del marco solo contempla la partición de Fisher.
  2. **La fórmula de Calinski-Harabász.** El Rmd y `aede` usan $(k, n-k)$ grados de libertad
     («como en el código del asesor»), no los $(k-1, n-k)$ habituales. Esto puede cambiar el k
     elegido.
  3. **La regla de signos de `aede`.** Domina la *suma* de los coeficientes positivos frente a
     la de los negativos. La del PCA de Rcamiz (`pca_basico` y `07_margen_signo.csv`) compara
     *sumas de cuadrados*. El Rmd dice que `aede` «orienta cada eje con la regla de Rcamiz»
     (sección A.3), lo que no es exacto: son dos reglas distintas. No afecta los valores propios
     ni los cortes de Fisher, solo el signo de las correlaciones graficadas.
- **Rótulo «HFC evolutiva» (Rmd, sección A.4, línea 2252).** Es una HFC por ventanas comparada
  con la correlación cofenética y el Rand ajustado. El Rmd no la presenta como un algoritmo EHFC
  publicado, lo que es coherente con el marco (línea 124). Aun así, el rótulo conviene revisarlo
  junto con el editor para que no se lea como un método establecido.

---

## 5. Archivos creados o modificados

| Archivo | Cambio |
|---|---|
| `R/tesis_ciclo_financiero.Rmd` | +15 líneas en `configuracion`: fija `LC_CTYPE` UTF-8 si la sesión no lo es (corrección de O1, ya presente y verificada en esta iteración) |
| `auditorias/notas/2026-10-19_desarrollador.md` | Esta nota (nueva) |
| `R/tesis_ciclo_financiero.html` | Regenerado; no versionado (`.gitignore`); idéntico al anterior |
| Scratchpad (fuera del repo) | `paridad.R`, `paridad_resultado.csv`, `rmd_full.log`, pruebas de locale en `loc/` |

Comandos exactos:

```
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
Rscript /tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/paridad.R /tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad
```

No se ejecutaron notebooks de Python ni se modificó ningún CSV de `data/results/`.

## 6. Desviaciones respecto de `decisiones.qmd` o del marco

1. **Notebook 06 en niveles con 19 series** frente a las 17 del análisis oficial D1 (3.4). La
   paridad en niveles solo se logra con 19 series. Requiere alinear el notebook; es un cambio de
   Python pendiente de autorización.
2. **Evidencia de D2 apoyada en fechas de episodios sin fuente** (4.1), contra la regla 6.
3. **`R_paridad_python.csv` proviene de la v1 archivada**, no del Rmd vigente (3.3). Las cifras
   coinciden; la procedencia no es la que declara la definición del agente.
4. **El marco no formaliza tres elementos** que el Rmd usa (4.2): el criterio de transición del
   notebook 06, la variante de Calinski-Harabász con $(k, n-k)$ y la regla de signos de `aede`.

Ninguna de estas desviaciones se corrigió en silencio: todas se proponen para discusión.

---

# Vuelta 1 · Respuesta al dictamen `auditorias/2026-10-19_iteracion-2.md` (OBSERVADO)

**Alcance:** los 7 hallazgos mayores y los 6 menores del dictamen asignados al desarrollador, más
cuatro puntos que el editor APA encontró al completar el registro y que el orquestador me
trasladó. Sin commit ni push. No se tocaron `tesis/`, `linea_temporal.qmd` ni las páginas del
sitio.

## Comandos ejecutados

```
pip install --break-system-packages nbconvert nbformat ipykernel jupyter_client
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06a_seleccion_ventana_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06b_seleccion_ventana_epca_mensual.ipynb
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
```

- Los tres notebooks terminan con EXIT 0. Ninguno usa `torch`: solo pandas, NumPy, scikit-learn
  y matplotlib. Antes de modelar verifican 17 series, ausencia de faltantes y calendario mensual
  continuo (los `assert` nuevos de la celda 2).
- El Rmd se renderizó dos veces, con EXIT 0 en ambas (131 s la última). Con `warning = TRUE`, el
  HTML tiene 0 avisos, 0 `## Error` y 0 secuencias `<U+…>`. Parámetros por defecto:
  `bootstrap_reps = 500`, `reps_nulo = 1000`, `semilla = 2026`; Horn, semilla 42.
- Registros: `/tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/v1/`
  (`nb_*.log`, `render1.log`, `render2.log`, `ch.R` y respaldo `antes/` de los CSV previos).

## Archivos modificados o creados

| Archivo | Cambio | ID |
|---|---|---|
| `notebooks/06_epca.ipynb` | Niveles con 17 series; controles de datos; markdown con la corrección; celda vacía final eliminada; re-ejecutado | M-01, m-06 |
| `notebooks/06b_seleccion_ventana_epca_mensual.ipynb` | Exclusión de las 2 series de referencia y controles; `[VERIFICAR]` en episodios; texto de cobertura trimestral corregido; re-ejecutado | M-01, M-05, editor 1–2 |
| `notebooks/06a_seleccion_ventana_epca.ipynb` | `[VERIFICAR]` en episodios; nota de cobertura de la crisis; re-ejecutado | M-05, editor 1–2 |
| `notebooks/modelos_dl.py` | `[VERIFICAR]` en `EPISODIOS_REFERENCIA` (solo comentarios) | M-05 |
| `R/tesis_ciclo_financiero.Rmd` | Ver cada ID | M-01 a M-07, m-01 a m-05, editor 1–4 |
| `R/anteriores/tesis_ciclo_financiero_v1.Rmd` | Ya no escribe en `data/results/` | M-02 |
| `data/results/06_epca_transiciones_detectadas_niveles.csv`, `06_epca_cargas_evolutivas_niveles.csv` | Regenerados con 17 series | M-01 |
| `data/results/06_epca_cargas_evolutivas.csv`, `06_epca_varianza_explicada.csv` | Regenerados; vía transformada sin cambio de fondo (dif. máx. 3,9e-15 y 1,1e-13, ruido de punto flotante) | M-01 |
| `data/results/R_*.csv` (vía transformada) y `data/results/niveles/R_*.csv` (vía sin transformar, nuevos) | Los escribe el Rmd vigente | M-02 |
| `reports/figures/06*.png` | Regeneradas por los notebooks | M-01 |

Los CSV `06a_*` y `06b_*` no cambian (mismo MD5).

---

## M-01 · EPCA en niveles con 17 series

**Cambio.** La celda 2 de `06_epca.ipynb` excluye `Crédito SF sector privado` e `IPC Subyacente`
de `dataset_niveles_estandarizado_mensual.csv`. Comprueba además que las 17 series restantes son
las mismas de la vía transformada. `06b` leía el mismo archivo de 19 columnas, pero solo para
imprimir su forma: sus resultados (`06b_seleccion_ventana_resumen_mensual.csv`) usan solo la vía
transformada. Aun así le apliqué la misma exclusión, por coherencia. Su CSV no cambia, así que
**la ventana de 60 meses no se ve afectada**.

**Cifras que cambian**

| Resultado | Antes (19 series) | Ahora (17 series, D1) | Origen |
|---|---|---|---|
| Transiciones EPCA en niveles (PC2) | 2012-01, 2013-10, 2015-10, 2018-01 (4) | 2012-01, 2013-10, 2015-10, **2017-10**, 2018-01 (5) | `data/results/06_epca_transiciones_detectadas_niveles.csv`, filas 2–6, columna `fecha_transicion_candidata` (la nueva es la fila 5) |
| Cargas evolutivas de PC2 en niveles | 57 ventanas × 19 series | 57 × 17 | `data/results/06_epca_cargas_evolutivas_niveles.csv` |
| Coincidencias ±6 meses entre vías (salida de la celda 22 de `06`) | 3 | 5 (2017-11 y 2018-02 coinciden ahora también con 2017-10) | salida impresa del notebook, no CSV |
| Paridad R–Python, EPCA en niveles | solo con 19 series | 17 frente a 17, idénticas | `data/results/niveles/R_paridad_python.csv`, fila 4, columnas `valor_r`, `valor_python`, `coincide` |

- *Interpretación:* la transición adicional de 2017-10 cae entre 2017-11 y 2018-02 de la vía
  transformada. Con las 17 series, el cambio de estructura de fines de 2017 aparece en las dos
  vías, no solo en las variaciones.
- *Dudas abiertas para Roberto:*
  - Con las 17 series, 2017-10 y 2018-01 distan un solo paso de ventana. ¿Se leen como un solo
    episodio, igual que 2017-11 y 2018-02 en la vía transformada?
  - El texto del sitio todavía no refleja las 5 fechas (ver abajo). ¿Cuándo se actualiza?

**Dónde se citan las cifras (no edité estos archivos):**

- **Sitio** (`*.qmd`, sin contar `auditorias/`): ninguna página cita las transiciones de la EPCA
  en niveles ni `06_epca_*_niveles.csv`. `marco_matematico_ae_lstm.qmd:438` cita solo las
  transiciones transformadas (2013-05, 2017-11, 2018-02), que no cambian.
  `linea_temporal.qmd:71` dice que la vía transformada reproduce la EPCA en R; sigue siendo
  cierto.
- **Rmd:** A.3 las lee del CSV y del cálculo en R. Actualicé el recuadro de paridad, que antes
  decía «el notebook 06 corre la EPCA en niveles con 19 series», y el punto 10 de C.7.
- **Resultado aguas abajo desactualizado:** `data/results/niveles/08_ae_contraste_epca.csv`
  (de `R/redes_python/08_autoencoder_niveles.ipynb`, celda 28) contrasta el error del AE con las
  4 fechas antiguas y le falta 2017-10. No lo regeneré porque el notebook necesita `torch`, que no
  está en el servidor, y ningún documento lo lee (ni el Rmd ni el sitio). Lo calculé por mi
  cuenta, sin escribir el archivo, desde `niveles/08_ae_factores_y_error.csv`: la fila de 2017-10
  daría un error máximo a ±6 meses de 0,034 (en 2018-04) frente a un umbral p90 de 0,333, es decir,
  `supera_p90 = False`, igual que las otras cuatro. **Pendiente:** re-ejecutar esa copia cuando
  haya `torch`.

## M-02 · `R_*` generados por el Rmd vigente, en las dos vías

**Convención:** la de la regla 3. La vía sin transformar escribe en `data/results/niveles/` y la
transformada en `data/results/`, con el mismo nombre de archivo. La escritura está en un anexo
nuevo al final del Rmd (chunk `anexo-paridad`). El v1 archivado ya no escribe: comenté su
`write.csv` y el chunk `guardar` quedó con `eval = FALSE`.

**`R_paridad_python.csv`** (8 filas en transformadas y 7 en niveles; columnas `via`, `seccion`,
`criterio`, `valor_r`, `valor_python`, `archivo_python`, `dif_max`, `coincide`). Resultado:
**15 de 15 coinciden**.

| Vía | Comprobación | Archivo de Python | Resultado |
|---|---|---|---|
| niveles | Inercia acumulada d = 1..5 | `niveles/08_ae_anclaje_lineal.csv` | dif. 2,8e-14 |
| niveles | Horn | `niveles/08_ae_horn.csv` | 2 = 2 |
| niveles | EPCA regla 06, PC2 | `06_epca_transiciones_detectadas_niveles.csv` | idénticas (5) |
| niveles | Datación: k, inicios | `niveles/09_regimenes_pca.csv` | 6; 2008-12 … 2022-11 |
| niveles | Fases y componente de crédito | ídem | idénticas; dif. 0 a 2 decimales |
| transformadas | Valores propios frente a Rcamiz | `07_rcamiz_valores_propios.csv` | dif. 4,7e-11 |
| transformadas | Horn | `08_ae_horn.csv` | 4 = 4 |
| transformadas | Scores PC1–PC3 y MM12 causal | `05b_scores_suavizados.csv` | dif. 1,8e-14 (signos +1 +1 +1) |
| transformadas | EPCA regla 06, PC1 | `06_epca_transiciones_detectadas.csv` | idénticas (3) |
| transformadas | Datación: k, inicios | `09_regimenes_pca.csv` | 8; 2009-06 … 2023-11 |
| transformadas | Fases y componente de crédito | ídem | idénticas; dif. 0 |

**Diferencias frente a los `R_*` anteriores** (respaldados en `scratchpad/v1/antes/`):

| Archivo | Diferencia | Explicación |
|---|---|---|
| `R_paridad_python.csv` | Estructura nueva: 8 columnas y una fila por comprobación (antes 3 columnas y 5 filas, solo transformadas) | Cubre lo que pidió el auditor (PCA, EPCA, datación y fases en las dos vías) e indica el archivo de origen. La fila «PCA (Rcamiz vs 08)» antigua se sustituye por la comparación directa con `07_rcamiz_valores_propios.csv` (misma dif., 4,7e-11) |
| `R_hfc_jerarquia.csv` | 17 columnas, antes 8; `N1`/`N2` permutados en los nodos 1–17 | Ahora se guarda `hfc$hierar` completo. Los índices de las hojas cambian porque el v1 numeraba las variables en el orden del archivo transformado y el Rmd vigente en el orden de `meta_an`. Los nodos 18 y siguientes, `ngr`, `Num`, `Eigenv`, `Index`, `Glob_%1` y `Cum_%2` coinciden (dif. máx. 1,1e-14): es la misma jerarquía |
| `R_ehfc_cofenetica.csv` | Columna nueva `rand_ajustado_4g` | Las 55 fechas son las mismas y la cofenética difiere en 1,1e-15 |
| `R_aede_cortes.csv` | 6 filas (codo, CH con k y CH con k−1, por esquema de pesos), antes 2 | Las filas «Calinski-Harabász k gl (aede)» (filas 3 y 6) reproducen las dos filas antiguas: k = 10 y los mismos 9 cortes |
| `R_regimenes_criterios.csv` | Precisión completa y columna nueva `ch1` | El v1 redondeaba (`sce` a 2 decimales, `reduccion` a 3, `ch` a 1). Las diferencias (≤ 0,0036; 0,0005; 0,046) son de redondeo |
| `niveles/R_*.csv` | Nuevos | Vía oficial D1: antes no había ningún `R_*` en niveles |

- *Interpretación:* la versión oficial en R reproduce Python en las dos vías, y el archivo de
  paridad ya no depende de una corrida archivada.
- *Dudas abiertas para Roberto:* `R_paridad_python.csv` no compara el HFC en niveles con Python,
  porque no existe una HFC en Python. ¿Hace falta esa contraparte, o basta la validación del
  port?

## M-03 · Calinski-Harabász con k y con k−1 grados de libertad

**Cambio.** `ch_variantes()` calcula las dos variantes a partir de las mismas sumas de cuadrados
intra. `datar()` devuelve `k_ch` (k gl) y `k_ch1` (k−1 gl), y `correr_aede()` hace lo mismo,
además de comprobar con `stopifnot` que la variante con k reproduce la columna `Calinski-Harabasz`
de `aede_r`. Las tablas de A.3 y B.3 muestran las cuatro columnas de CH, y las de A.6 y B.6 una
fila por variante. Reescribí los textos de A.3 (lectura y síntesis), A.6, B.3 y B.6, añadí una
pregunta para Roberto en A.3 y un punto 12 en C.7.

| Análisis | k con CH (k gl, `aede`) | k con CH (k−1 gl, habitual) | k por codo | Origen |
|---|---|---|---|---|
| `aede` niveles, pesos uniformes | 10 | **2** (corte 2020-03) | 2 | `data/results/niveles/R_aede_cortes.csv`, filas 2–4, columnas `k` y `cortes` |
| `aede` niveles, pesos gaussianos | 10 | 10 | 2 | ídem, filas 5–7 |
| `aede` transformadas, uniformes | 10 | 10 | 4 | `data/results/R_aede_cortes.csv`, filas 2–4 |
| `aede` transformadas, gaussianos | 10 | 10 | 4 | ídem, filas 5–7 |
| Datación niveles (PC1–PC3) | 10 | 10 | 6 | `data/results/niveles/R_regimenes_criterios.csv`, fila 11 (máx. de `ch` = 180,3 y de `ch1` = 200,4) |
| Datación transformadas (PC1–PC3) | 9 | **8** | 8 | `data/results/R_regimenes_criterios.csv`: máx. de `ch` en la fila 10 (k = 9; 86,95); máx. de `ch1` en la fila 9 (k = 8; 99,15) |

**Cómo se acotó la conclusión.** El texto ya no dice que el CH «no ofrece un óptimo interior».
Ahora dice que la afirmación «el CH siempre favorece más cortes» solo vale con la fórmula de
`aede`. Con la habitual deja de valer en `aede` en niveles con pesos uniformes, y en la datación
transformada coincide con el codo. Una precisión frente al dictamen: con k−1, el máximo en k = 2
**no es interior en sentido estricto**. Es el menor k admisible, el borde inferior de la grilla
2..10, y el Rmd lo describe así. En las demás combinaciones las dos variantes quedan en el borde
superior (10).

- *Interpretación:* la conclusión sobre el CH es un artefacto de la fórmula en un caso de cuatro
  en `aede` y en uno de dos en la datación. Con la forma habitual, el CH y el codo coinciden en
  esos dos casos.
- *Duda abierta, para Roberto y el asesor (D-1):* ¿qué fórmula se adopta? ¿Usar $k$ en el
  numerador es una elección deliberada del Dr. Camiz en `aede`? La forma habitual no tiene ficha
  (`[VERIFICAR: sin ficha de Calinski y Harabász (1974)]`).

## M-04 · Regla de signo de `aede` frente a la de Rcamiz

**Cambio.** El texto de A.3 describe la regla real. `aede_r` invierte el eje cuando
$|\sum v_j^-| > \sum v_j^+$ (**suma lineal**) y después lo alinea con la ventana anterior
(mínima suma de cuadrados de la diferencia). `Rcamiz::pca`, en cambio, compara **sumas de
cuadrados**. El Rmd calcula ahora las discrepancias (función `signo_difiere`, chunks `b4-signo` y
`bB3-signo`) y las presenta en dos recuadros de lectura en A.3 y B.3.

| Vía | Ventanas de 60 meses con orientación distinta (eje 1 / 2 / 3) | Ejes del PCA global con orientación distinta |
|---|---|---|
| niveles | 0 / 2 / 20 de 169 | 9, 11, 12, 14, 17 |
| transformadas | 2 / 2 / 4 de 168 | 6, 16 |

Origen: HTML del Rmd, recuadros de lectura tras las tablas de `aede` (A.3 y B.3); se calculan en
el render y no se escriben en CSV. Coinciden con las cifras del auditor.

- *Interpretación:* la regla inicial de `aede` solo fija el signo de partida de las
  correlaciones evolutivas. No altera valores propios, cortes ni ninguna cifra publicada.
- *Dudas abiertas para Roberto:* ¿conviene preguntar al asesor si la diferencia entre `aede` y
  `Rcamiz::pca` es deliberada, para describirla igual en el cap. 2?

## M-05 · Fechas de episodios con `[VERIFICAR]`

No cambié ninguna fecha. Puse la marca `[VERIFICAR: fuente externa para fechar el episodio]` en:

- **Rmd:** la definición de `episodios` (con un comentario que enumera las fechas de `06a`/`06b`
  que no coinciden), el pie `nota_episodios` y `nota_episodios_en()`, el texto de A.1 sobre la
  crisis global, la sección de sensibilidad del PCA sin los episodios, y los pies de las tablas
  «Episodio a ±12 meses» (A.3 y B.3), «Episodios contenidos» (A.6 y B.6) y «Episodios conocidos»
  (C.4). Las fechas del texto se generan ahora con `rango_epi()` a partir de `episodios`. `covid` y
  `covid_t` ya no repiten las fechas a mano: las leen de `episodios`.
- **`notebooks/06a` y `06b`:** un comentario sobre el diccionario `EPISODIOS` y la marca en cada
  línea. En 06b son cinco episodios.
- **`notebooks/modelos_dl.py`:** comentario y marca en cada entrada de `EPISODIOS_REFERENCIA`. Los
  notebooks 05b, 08, 09 y las copias de `R/redes_python/` importan ese diccionario; no tienen
  copias propias.

**Punto 1 del editor (fechas distintas entre archivos)**, anotado en los comentarios de 06a, 06b
y el Rmd, y añadido como punto 11 de C.7:

| Episodio | `06a`/`06b` | Rmd y `modelos_dl.py` |
|---|---|---|
| Crisis global | 2008-07 a 2009-06 | 2008-09 a 2009-06 |
| *Taper tantrum* | 2013-04 a 2013-12 | 2013-05 a 2013-12 |
| COVID-19 | 2020-01 a 2020-09 | 2020-03 a 2020-12 |

- *Decisión para Roberto:* hace falta una sola definición, con fuente externa fichada y una
  convención de fechado (anuncio o impacto en el Perú). Propuesta: un CSV en `data/processed/` que
  lean Python y R. Las cifras de D2 sobre falsas alarmas (`09_discriminacion_episodios.csv`)
  dependen de estas fechas.

## M-06 · 194,00 y 242,86 (consulta a la API del BCRP)

**Búsqueda.** Ningún archivo de `data/` contiene esos valores (las dos coincidencias de `194.0…`
en `data/processed/` son 194,0368…, de otro mes). `series_bcrp_consolidado.csv` termina en
2024-12. No existe `data/raw/`, que además está en `.gitignore`. No simulé ninguna descarga.
**Cambio:** marqué `[VERIFICAR: descarga de control BCRP no versionada]` en el recuadro de la
sección 1 y en el comentario «Nombres y unidades verificados contra la API (consulta del
08/10/2026)».

- *Pendiente para Roberto:* versionar la descarga de control (fecha, códigos `PN01773AM` y
  `PN01774AM`, valores) en `data/` para que el Rmd lea esas cifras con código.

## M-07 · Citas sin ficha

Marqué con `[VERIFICAR: sin ficha]` en el Rmd: Horn (1965) (comentario de `horn()` y primera
mención en el texto, sección 2); Granger y Newbold (1974) y Phillips (1986), que sustituyen la
antigua marca «verificar antes de citar»; Benzécri (1973); y Engle y Granger (1987). Encontré
además otras referencias sin ficha, todas citadas por el nombre del método, y las marqué en su
primera mención: Calinski y Harabász (1974) (nueva, por M-03); los filtros de Hodrick-Prescott y
pasa-banda; las pruebas ADF y KPSS; la esfericidad de Bartlett; la medida KMO; el criterio de
Kaiser y la vara quebrada; el índice de Rand ajustado; el optimizador Adam; y los modelos de
Markov. Ya tenían ficha y no las marqué: Fisher (1958), Robert y Escoufier (1976), Drehmann,
Borio y Tsatsaronis (2012) y Srivastava, Mansimov y Salakhutdinov (2015). El HTML tiene 36
marcas `[VERIFICAR`. No toqué `tesis/`.

- **Punto 3 del editor:** el comentario de `coef_rv` ahora dice «Robert y Escoufier (1976)».
- **Punto 4 del editor:** confirmado. Horn (1965) y Benzécri (1973) llevan `[VERIFICAR: sin ficha]`
  en el texto del Rmd.

## Menores

- **m-01:** `warning = TRUE` en las opciones globales. `capa_episodios()` acepta ahora límites
  finitos (`y_lim`) y el rango de fechas (`x_lim`). En las cuatro figuras en escala logarítmica
  (`b6-g-error`, `b6-g-walkforward`, `bB5-g-error`, `bB5-g-walkforward`), las bandas se dibujan
  entre el mínimo positivo y el máximo de la serie, y solo para los episodios que caen en el rango
  del gráfico. El pie (`nota_episodios_en()`) anuncia solo esos episodios: en el *walk-forward*,
  que empieza en 2011, ya no se anuncia la crisis de 2008. Resultado: 0 avisos en el HTML
  (el auditor contó 8).
- **m-02:** el chunk `configuracion` guarda `locale_previo` y el chunk final `anexo-locale` lo
  restaura. Prueba: render desde una sesión de R abierta, con el locale antes y después (registro en
  `/tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/v1/render_locale.log`):
  `LC_CTYPE` = `C` antes y `C` después del render (EXIT 0). Sin la restauración quedaría en `C.UTF-8`.
- **m-03:** el chunk nuevo `b3-rcamiz-omitido` imprime «Rcamiz no disponible: verificación no
  ejecutada» cuando falta el paquete. `R/validacion_port_camiz.R` sigue necesitando
  `AedeClahfac`: no puedo usar los binarios del asesor (límite del entorno), así que esa
  validación no se re-ejecutó.
- **m-04:** el ejemplo de A.3 usa ahora la primera transición calculada (2012-01) y el intervalo
  que cubren las dos ventanas comparadas (2009-04 a 2014-06), ambos con código inline.
- **m-05:** «la expansión de 2010–2013» y «hasta 2013» se generan desde `fases_t` (objeto
  `exp_t`). Hoy dan 2010–2013 (2010-07 a 2013-02) y 2013, iguales a `09_regimenes_pca.csv`, fila 4,
  columnas `inicio` y `fin`. También el «diez meses del COVID-19» de A.1 pasó a `sum(covid)`.
- **m-06:** `06_epca.ipynb` se ejecutó de principio a fin con el comando de `CLAUDE.md`
  (`execution_count` 1–13, sin celdas vacías).

**Punto 2 del editor.** El texto incorrecto era el de `06b`. Los datos trimestrales empiezan en
2008-T1 (transformados) y en 2007-T4 (niveles), así que la crisis **sí está en los datos**. Lo
que ocurre es que ninguna serie de estabilidad la alcanza: con la ventana más corta de `06a`
(20 trimestres, paso 2), el primer punto de estabilidad cae en 2011-T1. Corregí la hipótesis 2 de
`06b` y añadí la aclaración en la sección 5 de `06a`, donde la banda se dibuja pero no puede
contrastarse.

## Desviaciones respecto de `decisiones.qmd` y propuestas

1. **M-01 alinea Python con D1.** Sustituye resultados de Python ya versionados. El sitio no cita
   las fechas de niveles, pero queda desactualizado
   `data/results/niveles/08_ae_contraste_epca.csv` (requiere `torch`).
2. **El Rmd incorpora la forma habitual del CH** como variante informada, no adoptada (D-1
   pendiente).
3. **La regla de respaldo del codo en niveles** (caída máxima) sigue sin estar en el notebook 09
   ni en el cap. 2 (D-2 del auditor, sin cambios).
4. **Propuesta:** una definición única de los episodios en `data/processed/`, con fuente y
   convención (punto 11 de C.7).

---

# Vuelta 2 (19 de octubre de 2026)

Respuesta a la sección «Re-auditoría — vuelta 1» de `auditorias/2026-10-19_iteracion-2.md`.
Línea base: md5 de los CSV `06*` y `R_*` (ambas vías) y de las figuras `06*`, guardados antes de
tocar nada en
`/tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/v2/md5_antes.txt`.
Sin commit ni push.

## N-01 · `06a` trimestral como antecedente superado

**Cambios** (solo texto y comentarios; ningún cálculo):

- `notebooks/06a_seleccion_ventana_epca.ipynb`: nueva celda markdown inicial
  (`id: antecedente-superado`). Declara que el notebook trabaja con los datasets trimestrales
  (transformado 72 × 18, 2008-T1 a 2025-T4; niveles 73 × 20, 2007-T4 a 2025-T4), cita la
  decisión de octubre de 2026 (solo frecuencia mensual, 17 series de D1: 228 × 17 y 227 × 17) e
  indica que la selección vigente es `06b_seleccion_ventana_epca_mensual.ipynb`. No lo renombré
  ni lo saqué del sitio (R-2). Celda de la grilla (antes celda 6, ahora 7): «p ≈ 16» pasa a
  **p = 18**; el piso queda «n = 20 > p = 18, no 18»; la regla 5–10 × p pasa de «80–160 obs.» a
  «90–180 obs.». Comprobé además que en niveles p = 20, así que la ventana de 20 trimestres tiene
  n = p y una matriz de correlación singular (rango ≤ 19), y lo dejé escrito en ese comentario.
- `notebooks/06_epca.ipynb`, celda 0: la referencia a `06a_seleccion_ventana_epca_v2.ipynb` apunta
  ahora a `06a_seleccion_ventana_epca.ipynb` («antecedente trimestral»), frente a
  `06b_seleccion_ventana_epca_mensual.ipynb`. Agregué un párrafo «Frecuencia» con la decisión
  mensual y la advertencia de que `05_pca.ipynb` sigue en trimestral.
- `notebooks/06b_seleccion_ventana_epca_mensual.ipynb`: celda 0, la referencia a `_v2` apunta a
  `06a_seleccion_ventana_epca.ipynb` y se declara vigente. Corregí también «n/p … vs. 4.5 en
  trimestral», que pasa a **4.0** (72 / 18; el 4,5 salía de p = 16). Celda 5: «n = 8 < p = 16»
  pasa a «p = 18». Celda 12: el mensaje de respaldo que remitía a `_v2` apunta al archivo
  existente.

**Ejecución** (exit 0 en los tres, sin celdas con error; `execution_count` 1–13, 1–9 y 1–7):

```
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06a_seleccion_ventana_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06b_seleccion_ventana_epca_mensual.ipynb
```

**Verificación:** `md5sum -c` contra la línea base: los 28 archivos (CSV `06*` y `R_*`, y las
12 figuras `06*`) son **idénticos byte a byte**. Ninguna cifra cambió.

- *Interpretación:* el cambio es documental; `06` ya usaba la ventana de 60 meses de `06b`.
- *Dudas abiertas para Roberto:* (1) la decisión «solo mensual» no tiene entrada en
  `decisiones.qmd`; propongo registrarla (D3) para que la celda de `06a` pueda enlazarla.
  (2) `05_pca.ipynb` (PCA estático) también lee los datasets trimestrales (72 × 18 y 73 × 20),
  y `06` dice que el «enfoque híbrido» parte de él: es la misma situación que `06a` y no la
  toqué, porque alinearlo cambia resultados versionados. (3) R-2 (archivar `06a` con prefijo
  999 o retirarlo del sitio) sigue abierta.

## N-05 · Trazas del proceso interno

Reemplacé por texto neutro, sin tocar el contenido técnico:

- `R/tesis_ciclo_financiero.Rmd`: texto neutro en los comentarios de los chunks `configuracion`,
  episodios, metadatos, `capa_episodios`, signo, CH en `datar` y en los bloques de `aede` de A.3
  y B.3, `b3-rcamiz-omitido`, paridad de EPCA, `fases_t`, `anexo-locale`; y en el texto: el
  recuadro de paridad de A.3, «Una versión anterior del notebook…», el punto 10 de C.7 y el
  párrafo inicial del anexo. También sustituí «regla 6 de CLAUDE.md» por el criterio en sí
  («los episodios se fechan con fuentes externas…») y «pendiente de Roberto [y el asesor]» por
  «pendiente» en los comentarios. Mantengo los recuadros «Para Roberto», que son parte del
  diseño del documento y no del proceso de revisión.
- `R/anteriores/tesis_ciclo_financiero_v1.Rmd`: 2 comentarios (bloques de paridad y `guardar`).
- `notebooks/06_epca.ipynb`, `06a`, `06b` (celdas indicadas en N-01, más las de `EPISODIOS`
  y la nota de la sección 5 de `06a`) y `notebooks/modelos_dl.py` (comentario de
  `EPISODIOS_REFERENCIA`; sintaxis verificada con `ast.parse`).

**Verificación:** búsqueda de `M-0x`, `m-0x`, `N-0x`, «vuelta N», «iteración N», «auditor»,
«re-auditoría», «CLAUDE.md», `_v2.ipynb` y «p ≈ 16» en `notebooks/`, `src/`, `R/*.R`,
`R/redes_python/` y los dos Rmd: **0 coincidencias** (código y salidas de las celdas). La palabra
«dictamen» queda solo como nombre de la columna técnica ADF/KPSS del Rmd.

## M-06 · 194,00 y 242,86 (parcial; decisión R-4)

No puedo descargar del BCRP (límite del entorno), así que no creé ningún archivo ni simulé la
consulta. Las dos cifras siguen escritas a mano y marcadas. Reescribí las dos marcas del Rmd para
que digan exactamente qué hay que versionar:

- Comentario de `metadatos_series`: «hay que versionar en data/ un archivo con: la fecha de
  consulta (08/10/2026), los códigos de serie consultados (PN01773AM, PBI desestacionalizado;
  PN01774AM, demanda interna) y los valores devueltos para 2025-12 (194,00 y 242,86)».
- Recuadro de la sección 1 (texto visible): «[VERIFICAR: descarga de control BCRP no versionada:
  los valores 194,00 y 242,86 no están en ningún archivo de `data/`; para leerlos con código hay
  que versionar la fecha de consulta (08/10/2026), los códigos de serie (PN01773AM y PN01774AM) y
  los valores devueltos para 2025-12]».

Los códigos coinciden con `notebooks/01_extraccion_bcrp.ipynb` (diccionario de series) y con el
vector `codigo` de `metadatos_series`.

- *Pendiente para Roberto (R-4):* repetir la consulta y versionarla en `data/` (y que el Rmd la
  lea), o retirar las dos cifras. La fila del registro de verificación (N-03) es del editor APA.

## N-04 · Hojas de `R_hfc_jerarquia.csv` identificadas

**Cambio** (anexo de paridad del Rmd, función nueva `jerarquia_con_series()`, usada por
`escribir_via()` en las dos vías): después de `N1` y `N2` se agregan cuatro columnas,
`N1_serie`, `N1_codigo`, `N2_serie`, `N2_codigo`. Si el nodo es una hoja (≤ 17), llevan el
nombre corto y el código BCRP de la serie; si es una fusión, «Nodo k» y código vacío. La función
comprueba con `stopifnot` que las hojas siguen el orden de `meta_an` en `X` y `Xt` y que cada
una de las 17 hojas aparece una sola vez.

**Resultado:** `data/results/R_hfc_jerarquia.csv` y `data/results/niveles/R_hfc_jerarquia.csv`
pasan de 16 × 17 a 16 × 21. Las 17 columnas originales son **idénticas** a las anteriores
(`DataFrame.equals`). Ejemplo, fila «18» (primera fusión): `N1_serie` = M2 (liquidez en soles),
`N2_serie` = M3 (liquidez total), en las dos vías.

**Comparabilidad entre versiones:** traduje a códigos BCRP las hojas de la versión de `HEAD`
(vía transformada, numeradas por el orden de columnas de `dataset_transformado_mensual.csv`) y
las comparé con las del archivo nuevo. Los 16 grupos (composición de cada nodo) son los mismos
y `Eigenv` coincide (dif. máx. 0), aunque la numeración de las hojas es otra. Confirma lo que
dice el auditor: es una permutación del mismo árbol.

- *Interpretación:* el archivo ya puede leerse sin el Rmd y compararse por código de serie.
- *Duda abierta:* ninguna.

## Render del Rmd y paridad

```
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
```

Exit 0, 292/292 chunks, 2 min 15 s (registro en
`/tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/v2/render.log`). No hay
avisos: 0 coincidencias de `## Warning`, `## Error`, `Warning message` o `<U+00` en el HTML, y
en el registro solo aparecen los nombres de los chunks `b6-g-error` y `bB5-g-error`.

- **Paridad: 15/15** (`data/results/niveles/R_paridad_python.csv`, columna `coincide`: 7 «sí»;
  `data/results/R_paridad_python.csv`: 8 «sí»).
- Los otros ocho `R_*` (`R_aede_cortes`, `R_ehfc_cofenetica`, `R_paridad_python` y
  `R_regimenes_criterios`, en las dos vías) son **idénticos byte a byte** a los anteriores.
- Diferencias de texto en el HTML frente al render anterior (texto visible, sin imágenes): solo
  las sustituciones de N-05 y M-06 y el comentario de `jerarquia_con_series`. Ninguna cifra
  cambia; el HTML tiene 35 líneas con `VERIFICAR`.

## Archivos modificados en la vuelta 2

- `notebooks/06_epca.ipynb`, `notebooks/06a_seleccion_ventana_epca.ipynb`,
  `notebooks/06b_seleccion_ventana_epca_mensual.ipynb` (texto y comentarios; re-ejecutados).
- `notebooks/modelos_dl.py` (un comentario).
- `R/tesis_ciclo_financiero.Rmd`, `R/tesis_ciclo_financiero.html` (render).
- `R/anteriores/tesis_ciclo_financiero_v1.Rmd` (dos comentarios; no se renderiza).
- `data/results/R_hfc_jerarquia.csv`, `data/results/niveles/R_hfc_jerarquia.csv` (cuatro columnas
  nuevas).
- Esta nota.

No toqué `tesis/`, `decisiones.qmd` ni `linea_temporal.qmd`. Sin commit ni push.

## Desviaciones y propuestas (vuelta 2)

1. **La decisión «solo mensual» (octubre de 2026) no está en `decisiones.qmd`.** La cito en
   `06`, `06a` y `06b` sin enlace. Propongo registrarla como D3, con la alternativa descartada
   (trimestral) y el rastro.
2. **`05_pca.ipynb` sigue en trimestral** (lee 72 × 18 y 73 × 20, con inmuebles y, en niveles, las
   dos series de referencia). Contradice esa decisión y D1 igual que `06a`. No lo modifiqué
   porque alinearlo cambia resultados versionados (`05_pca_*.csv`). Queda como propuesta para
   Roberto: declararlo antecedente, como `06a`, o re-ejecutarlo en mensual con 17 series.
3. `R_hfc_jerarquia.csv` cambia de forma (16 × 17 a 16 × 21) sin cambiar valores; ningún otro
   archivo del repositorio lo lee.

# Cierre (20 de octubre de 2026)

## M-06 · Cifras retiradas (decisión de Roberto, opción R-4 «retirar»)

- **Bloque `funciones` (comentario antes de `metadatos_series()`):** eliminé la marca
  `[VERIFICAR: descarga de control BCRP no versionada]` y las cuatro líneas que citaban los
  códigos PN01773AM y PN01774AM y los valores 194,00 y 242,86. Se mantiene la línea «Nombres y
  unidades verificados contra la API del BCRP (consulta del 08/10/2026)», que no contiene cifras.
  Los códigos PN01773AM y PN01774AM siguen en el vector `codigo`, porque son la ficha de las
  series y no la cifra de control.
- **Sección 1, «Fuente, periodo y cobertura», recuadro «Las series desestacionalizadas se
  revisan»:** la frase dice ahora que el BCRP recalcula el ajuste estacional de las dos series,
  que estas cambian según la fecha de descarga, y da sus valores de diciembre de 2025 *en el
  dataset de la tesis*, leídos con código inline de `data/processed/` (HTML: 193,43 y 242,17).
  Cierra con la recomendación de fijar y declarar la fecha de corte. También retiré «Las demás
  series coinciden con el BCRP», porque esa afirmación se apoyaba en la misma consulta no
  versionada.
- **Control en el código:** no había ninguno. Los dos valores solo aparecían en texto y en
  comentarios, así que no retiré ningún control.
- Ya no queda «194,00» ni «242,86» en el Rmd ni en el HTML. Los `VERIFICAR` bajan de 35 a 33 en
  el HTML.
- **Pendiente para el editor APA (no lo toqué):** la fila de `tesis/registro_verificacion.md`
  (línea 36, «Descarga de control de la API del BCRP», abierta por N-03) quedó sin marca
  correspondiente en el Rmd. Hay que cerrarla o retirarla.

## N-06 · Referencia a D3

Leí D3 en `decisiones.qmd` («Solo la vía mensual», registrada el 20 de octubre). Cambié solo
celdas markdown, con el mismo estilo con que se citan D1 y D2 (`D1 (decisiones.qmd)`):

- `notebooks/06_epca.ipynb`: «*Frecuencia:* por D3 (`decisiones.qmd`), el análisis se realiza
  solo con datos mensuales…».
- `notebooks/06a_seleccion_ventana_epca.ipynb`: «Por D3 (`decisiones.qmd`), el análisis de la
  tesis se realiza **solo con frecuencia mensual**…».
- `notebooks/06b_seleccion_ventana_epca_mensual.ipynb`: «Por D3 (`decisiones.qmd`), el análisis
  se realiza solo con frecuencia mensual…».

Ya no queda «octubre de 2026» en ninguno de los tres. Esto también resuelve la desviación 1 de
la vuelta 2.

**Ejecución:**

```
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06a_seleccion_ventana_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06b_seleccion_ventana_epca_mensual.ipynb
```

Los tres terminan con exit 0 y sin celdas de error. Los tres notebooks volvieron a escribir sus 7
CSV (`06_epca_*` ×5, `06a_seleccion_ventana_resumen.csv`, `06b_seleccion_ventana_resumen_mensual.csv`)
y sus 10 figuras (`reports/figures/06_*`, `06a_*`, `06b_*`). Antes y después tomé el SHA-256 de
los 100 archivos de `data/results/` y `reports/figures/`, y todos son **idénticos byte a byte**.

## Render del Rmd y paridad

```
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
```

- Exit 0, 292/292 chunks. El HTML no tiene ninguna coincidencia de `## Warning`, `## Error`,
  `Warning message` ni `<U+00`. En el registro, «error» solo aparece en los nombres de los chunks
  `b6-g-error` y `bB5-g-error`.
- **Paridad 15/15:** `data/results/R_paridad_python.csv`, columna `coincide`, 8 «sí» de 8;
  `data/results/niveles/R_paridad_python.csv`, 7 «sí» de 7.
- El render volvió a escribir los diez `R_*` (cinco por vía), que son idénticos byte a byte a los
  anteriores. Ninguna cifra del análisis cambia.
- Registros guardados en
  `/tmp/claude-0/-home-claude/a217f36f-6870-55d3-82d1-8c23d5e0dcf2/scratchpad/cierre/`:
  `render_rmd.log`, `nbconvert_*.log` y `hash_antes.txt`, `hash_despues_nb.txt`,
  `hash_despues_rmd.txt`.

## Archivos modificados en el cierre

- `R/tesis_ciclo_financiero.Rmd` y `R/tesis_ciclo_financiero.html` (render).
- `notebooks/06_epca.ipynb`, `notebooks/06a_seleccion_ventana_epca.ipynb` y
  `notebooks/06b_seleccion_ventana_epca_mensual.ipynb` (texto y re-ejecución).
- Esta nota.

No toqué `tesis/`, `decisiones.qmd` ni `linea_temporal.qmd`. Sin commit ni push.

## Dudas abiertas para Roberto

1. La fecha de corte de los datos sigue sin declararse. El recuadro la recomienda, pero no hay
   ningún archivo en `data/` que registre la fecha de descarga de `series_bcrp_consolidado.csv`.
2. El comentario «Nombres y unidades verificados contra la API del BCRP (consulta del
   08/10/2026)» no tiene cifras, pero se refiere a la misma consulta no versionada. Se puede
   dejar como nota de trabajo o retirar.
3. Sigue pendiente la desviación 2 de la vuelta 2: según D3, `05_pca.ipynb` debe rehacerse en
   mensual.
