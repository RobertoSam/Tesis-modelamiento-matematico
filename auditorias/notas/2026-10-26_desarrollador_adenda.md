# Nota del desarrollador · 26 de octubre de 2026 · Adenda de la iteración 3b (fase 0')

**Encargo:** lote lanzable de la adenda (`asesoria/2026-10-26_adenda-plan-iteracion-3b.md`, §7.1),
con el conforme de Roberto del 26-oct. Roberto aclaró además que el análisis queda con **16 series**:
no se compara 16 frente a 17 (R.c) ni se usa M2 como variable suplementaria. **D17 y R1 no están
registradas.** Por eso no se ejecutó nada que lea k\*, el RV o la regla K con 16 series (DR, D10,
D12 ni R.b). Rama `iteracion-3b`; un commit por tarea y `git push` después de cada commit.

| Tarea | Commit | Estado |
|---|---|---|
| D0 · antecedente congelado y parámetro de exclusión | `f45d59e` | hecha; **el tag no se pudo subir** (§6, desviación 1) |
| `coef_rv` sin centrar (opción) | `f737a72` | hecha y validada |
| D9 · episodios unificados y criterio 8 | `3c416c2` | hecha y validada (el 05 y el Rmd final pasan a leer el CSV en `14b8e13`) |
| DF · Rmd final, secciones 0–3, y notebook 05 con parámetros | `14b8e13` | hecha y validada |
| DX · anexo R.a (sustento de no diferenciar) | `1026db2` | hecha y validada |
| Esta nota | commit siguiente | — |

**Regla 7.** No toqué `tesis_latex/`, `tesis/`, `04_resultados.*` ni `herramientas/generar_cifras.py`.
Las cifras de esta nota se calcularon con 16 series y **no tienen todavía interpretación
consolidada**. Las líneas de interpretación de §4 solo describen las cifras.

## 1. Archivos creados o modificados

| Archivo | Estado | Tarea | Contenido |
|---|---|---|---|
| `data/results/LEEME.md`, `data/results/niveles/LEEME.md` | nuevo | D0 | «Antecedente, 17 series, no consumir», con el tag y el commit |
| `src/datos.py` | modificado | D0 | `EXCLUIDAS_D16 = ('Liquidez M2',)` (parámetro único), `meta_vigente()`, `cargar_vias(excluidas=...)` |
| `tests/test_datos.py` | nuevo | D0 | 16 y 17 series; mismas cifras bit a bit en las columnas comunes |
| `src/multivariado.py`, `R/07b_nulo_estructura.R` | modificado | coef_rv | argumento `centrar` (por defecto `TRUE`, el comportamiento de siempre) |
| `tests/test_coef_rv.py` | nuevo | coef_rv | por defecto idéntico a la versión anterior; valor analítico sin centrar; invariancias; paridad con R |
| `data/referencia/episodios_referencia.csv`, `data/referencia/LEEME.md` | nuevo | D9 | archivo único de episodios (D7) |
| `src/episodios.py` | nuevo | D9 | lector con validación, diccionario, discriminación sin `torch`, bordes de ventana |
| `notebooks/modelos_dl.py` | modificado | D9 | `EPISODIOS_REFERENCIA` se lee del CSV (no se ejecutó: falta `torch`) |
| `notebooks/06a_*.ipynb`, `notebooks/06b_*.ipynb` | modificado | D9 | una celda de nota (antecedente superado); no se reescribieron ni se ejecutaron |
| `tests/test_episodios.py` | nuevo | D9 | claves con ficha, criterio 8, bordes, cero fechas a mano en los consumidores vigentes |
| `R/ciclo_financiero_final.Rmd` | nuevo | DF, DX | Rmd final: secciones 0–3, 4–8 en pendiente, anexo R (R.a) y anexo P (paridad) |
| `notebooks/05_pca.ipynb` | modificado | DF | bloque de parámetros `VIA`, `EXCLUIDAS`, `CARPETA` (+ `DIR_R`); deriva HAC, nulo mixto y dimensión |
| `notebooks/05c_anexo_no_diferenciar.ipynb` | nuevo | DX | R.a en Python |
| `src/series_tiempo.py` | modificado | DF | `t_hac_media` y `tratamiento_mixto` (D8) |
| `src/remuestreo.py` | modificado | DF | `nulo_tendencias(version='mixto', tratamiento=...)` |
| `tests/test_nulo_mixto.py` | nuevo | DF | HAC frente a `statsmodels`, regla de D8, casos límite del nulo mixto |
| `herramientas/no_regresion_05.py` | nuevo | DF | prueba de no regresión del 05 con 17 series (adenda, §3) |
| `data/results/final/` | nuevo | DF, DX | 05\_\*, R\_\* y `R_paridad_python.csv`; `anexo/` con 05c\_\*, R_anexo\_\* y su paridad |
| `reports/figures/final/` | nuevo | DF | figuras del 05 |

El Rmd de exploración `R/tesis_ciclo_financiero.Rmd` **no cambió**: su md5 es el de `2be3665`
(`c21946b6bb1bc3f3d160cb8b3e8f6e3f`). Tampoco cambió ningún CSV antecedente:
`git diff --stat 2be3665 -- data/results ':!data/results/final'` solo lista los dos `LEEME.md`
(criterio 17).

## 2. Comandos de ejecución (orden obligatorio)

Desde la raíz. El Rmd escribe los índices compartidos y los `R_*`; los notebooks los leen y se
comparan con ellos; el Rmd vuelve a leer los CSV de Python para la paridad.

```
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')"
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/05_pca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/05c_anexo_no_diferenciar.ipynb
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')"
python3 -m pytest tests/ -q
python3 herramientas/no_regresion_05.py
```

- Versión para el asesor: `Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd', output_dir = '<carpeta>', params = list(version_asesor = TRUE))"`.
- Tiempos en este entorno: render, unos 40 s; 05, 11 s; 05c, menos de 5 s; no regresión, 15 s.
- Semillas: el Rmd usa `params$semilla = 2026` para los índices del bootstrap (antes de cada L) y del
  nulo de tendencias, y para Horn en R.a; Horn del PCA usa la semilla 42 en las dos lenguas (como
  en 3a). El 05c usa `default_rng(2026)` para Horn. Todo lo demás usa índices compartidos.

**Validación final.**

- Render normal y `version_asesor = TRUE`: exit 0, sin `Warning` ni `Error` en el registro ni en el HTML.
- Recuadros `class="pregunta"`: 15 en la versión normal y 0 en la del asesor.
- 05 y 05c: nbconvert con exit 0.
- `pytest`: 43 pruebas aprobadas.

## 3. Paridad Python–R y no regresión

- **31 de 31** comprobaciones coinciden: 26 en `data/results/final/R_paridad_python.csv` y 5 en
  `data/results/final/anexo/R_paridad_python.csv`.
- La diferencia máxima es 2,7e-13 (contraste sin tendencia, fila 25 del primer archivo).
- **Excepción de generadores (Horn), declarada en cada fila:** se compara el número de componentes
  retenidos, no el umbral (filas 4 del primer archivo y 2 del segundo).
- **En sentido inverso,** el 05 y el 05c comparan sus cifras con los `R_*` y fallan si difieren.
- **Criterio 16:** el Rmd recorre todos los CSV de `final/` y `final/anexo/` y se detiene si
  alguno contiene «Liquidez M2» o «M2 (liquidez en soles)». No hay proyección suplementaria
  (Roberto la descartó).

**No regresión del código (adenda, §3).** `herramientas/no_regresion_05.py` corre el 05 con
`VIA = 'ambas'`, `EXCLUIDAS = []` y una carpeta temporal, contra los índices y `R_*` del
antecedente:

- los **37** CSV `05_*` del antecedente se reproducen byte a byte, incluido
  `05_pca_valores_propios.csv` en las dos vías;
- tres archivos se amplían, y en ellos las filas y columnas antiguas son idénticas:
  - `05_nulo_tendencias.csv` y `05_nulo_simulaciones.csv`, con filas nuevas del nulo mixto al final;
  - `05_tendencia_series.csv`, con columnas nuevas de la deriva HAC al final.

La no regresión de `R_aede_cortes.csv`, `09a_datacion_criterios.csv` y `R_hfc_clases3.csv` no se hizo:
exige parametrizar 06c, 09a y 07c y escribir las secciones 4–6 del Rmd final, que son de DR (§5).

## 4. Resultados (16 series, niveles; sin interpretación consolidada)

Convención de origen: archivo de `data/results/final/` · fila de datos (1 = primera tras el
encabezado) · columna.

### 4.1 D9 · Episodios y criterio 8

| Resultado | Cifra | Origen |
|---|---|---|
| Episodios en el archivo único | 6: 5 períodos y 1 puntual (Kuczynski / Odebrecht, 2018-03, sin fin) | `data/referencia/episodios_referencia.csv` · filas 1–6 · `tipo` |
| Criterio 8: con las fechas antiguas, la ruta sin `torch` reproduce `09_discriminacion_episodios.csv` | byte a byte, en las dos vías del antecedente | `tests/test_episodios.py::test_criterio_8_reproduce_discriminacion_del_09` |
| Fechas de episodio a mano en el código vigente (05, Rmd final, `modelos_dl.py`, `src/`) | 0 | `tests/test_episodios.py::test_sin_fechas_de_episodio_a_mano_en_consumidores_vigentes` |

- **Interpretación:** la discriminación puede recalcularse sin volver a entrenar. Con fechas nuevas
  cambia el conjunto evaluable: entran las materias primas, la guerra comercial y Kuczynski, y el
  COVID-19 pasa de 10 meses a 2.
- **Dudas abiertas:**
  1. Las fechas son la propuesta principal del bibliotecario según D7; las alternativas fichadas
     (inicio del COVID-19 en 2020-01, fin en 2023-05; Kuczynski como período desde 2016-12) no
     entran. ¿Las confirma Roberto como principales?
  2. Con un fin del COVID-19 en 2020-04, el episodio dura 2 meses. Para la sensibilidad de HT3 puede
     ser poco discriminante en el sentido contrario al que advertía el bibliotecario.

### 4.2 Sección 2 · Diagnóstico sin transformar

| Resultado | Cifra | Origen |
|---|---|---|
| Clases D5 de las 16 series | 1 TS, 12 DS, 3 indeterminadas (crédito de consumo, TIPMN, PBI) | `05_tendencia_series.csv` · filas 1–16 · `clase_d5` |
| \|t\| HAC de la deriva más cercanos a 2 | PBI 2,29; demanda interna 2,27 | ídem · filas 14 y 15 · `deriva_hac_t` |
| Mediana de $n_{ef}$ de los 120 pares | 10,57 (sin tendencia: 16,28) | `05_n_efectivo_resumen.csv` · filas 1 y 2 · `n_ef_mediana` |
| Pares con r ≠ 0 al 5 %, con $n$ y con $n_{ef}$ | 82,5 % y 42,5 % | ídem · fila 1 · `prop_signif_n`, `prop_signif_n_ef` |
| KMO global | 0,844 | `05_adecuacion.csv` · fila 8 · `valor` |
| Bartlett con la mediana de $n_{ef}$ | χ² = 161,7; p = 0,0067 | ídem · filas 6 y 7 · `valor` |
| Nulo con deriva: P(PC1 nulo ≥ observado) y P(PC2 nulo ≥ observado) | 0,910 y 0,014 | `05_nulo_tendencias.csv` · filas 1 y 2 · `proporcion` |
| Nulo sin deriva: ídem | 0,008 y 0,474 | ídem · filas 5 y 6 · `proporcion` |
| **Nulo mixto (D8)**, indeterminadas como TS: ídem | 0,783 y 0,003 | ídem · filas 13 y 14 · `proporcion` |
| **Nulo mixto (D8)**, indeterminadas como DS: ídem | 0,826 y 0,004 | ídem · filas 17 y 18 · `proporcion` |
| PCA sin tendencia: inercia de PC1; KMO | 38,5 %; 0,684 | `05_pca_contraste_tendencia.csv` · filas 17 y 21 · `valor` |
| Congruencia de PC1 a PC4 con su equivalente sin tendencia | 0,49 (PC1 ↔ PC4 sin tendencia), 0,78, 0,82, 0,76 | ídem · filas 25–32 · `valor` |

- **Interpretación:** con el nulo mixto, que D8 fija como pertinente, el PC1 sin transformar sigue
  sin superar a series independientes con sus tendencias (P ≈ 0,78–0,83), y el PC2 sí lo supera
  (P ≤ 0,004) en las dos variantes de las indeterminadas.
- **Dudas abiertas:**
  1. D8 pide declarar las series con |t| «cercano a 2» sin fijar una banda. El Rmd usa ±0,5 solo
     para describir: el PBI (indeterminada) y la demanda interna (DS) quedan a 0,3 del umbral.
     ¿Se fija una banda con una sensibilidad que cambie su tratamiento?
  2. El PC1 sin transformar no tiene equivalente sin tendencia (su eje más parecido es el PC4, con
     congruencia 0,49), y la congruencia de los demás está bajo 0,85. ¿Qué parte de PC2 y PC3 es
     estructura propia y qué parte es efecto de la tendencia?

### 4.3 Sección 3 · PCA estático

| Resultado | Cifra | Origen |
|---|---|---|
| Inercia de PC1, PC2 y PC3 | 65,2 %, 19,4 %, 7,6 % (acumulada 92,2 %) | `05_pca_valores_propios.csv` · filas 1–3 · `inercia`, `inercia_acumulada` |
| Componentes retenidas: Kaiser, Horn, vara quebrada | 3, 2, 2 | `05_pca_retencion.csv` · filas 1–3 · `componentes` |
| Correlación del score con el tiempo | PC1 0,993; PC2 0,073 | `05_pca_tendencia_componentes.csv` · filas 1–2 · `r_tiempo` |
| Clase D5 de PC1 a PC4 | DS en las cuatro | ídem · `clase_d5` |
| Congruencia bootstrap mediana (L = 24), PC1 a PC4 | 0,982; 0,960; 0,950; 0,851 | `05_bootstrap_congruencia.csv` · filas 5–8 · `mediana` |
| D9 · d = 3: la inercia de PC3 frente a la vara quebrada | 7,55 % < 11,75 % | `05_pca_dimension.csv` · fila 2 · `inercia_d`, `vara_quebrada_d` |
| D9 · réplicas con λ_d > 1 (d = 2, 3, 4) | 100 %, 88,4 %, 0 % | ídem · filas 1–3 · `prop_lambda_mayor_1_L24` |
| D9 · calidad media con d ejes (d = 2, 3, 4) | 0,846; 0,922; 0,952 | ídem · `calidad_media` |

- **Interpretación:** con 16 series, la tercera dimensión de D9 la retiene Kaiser, pero no Horn ni la
  vara quebrada. Su eje se reproduce en el bootstrap (congruencia mediana 0,95), y λ3 supera 1 en
  el 88 % de las réplicas.
- **Dudas abiertas:**
  1. ¿Cómo se sostiene d = 3 ante el Dr. Camiz si Horn y la vara quebrada retienen 2? D9 lo fijó
     antes de las cifras, y la adenda no cambia eso.
  2. El bootstrap por bloques en niveles mide estabilidad descriptiva, no incertidumbre muestral
     (supuesto declarado).

### 4.4 Anexo R.a · Sustento de no diferenciar

| Resultado | Cifra | Origen |
|---|---|---|
| Congruencia de PC1–PC3 con solo logaritmo | 0,999; 0,996; 0,992 | `anexo/05c_pasos.csv` · filas 16–18 · `valor` |
| Congruencia de PC1–PC3 con la transformación completa | 0,666; 0,844; 0,698 | ídem · filas 34–36 · `valor` |
| Inercia de PC1: sin transformar, solo diferencia y log-diferencia | 65,2 %; 23,5 %; 21,7 % | ídem · filas 1, 19 y 28 · `valor` |
| Horn retiene (sin transformar, log, diferencia, log-diferencia) | 2, 2, 3, 4 | ídem · filas 5, 14, 23 y 32 · `valor` |
| Mediana de la varianza en períodos ≥ 24 meses | 93,4 % sin transformar y sin tendencia; 23,4 % transformadas | `anexo/05c_espectro.csv` · columnas `niv_det`, `tr` (mediana de las 16 filas) |
| Ganancia de Δ a 96 meses (varianza conservada) | 0,0654 (0,43 %) | `anexo/05c_ganancia.csv` · fila 6 · `ganancia`, `varianza_conservada` |
| Series transformadas con ACF a 12 meses > 2/√n (0,133) | 7 de 16; la mayor, demanda interna (0,58) | `anexo/05c_estacional.csv` · filas 1–16 · `acf12` (fila 15) |

- **Interpretación:** con 16 series se repite lo que ya mostraba el antecedente con 17: el logaritmo
  no cambia la estructura, y la diferencia sí la cambia y atenúa las frecuencias bajas.
- **Dudas abiertas:**
  1. ¿Está desestacionalizada la demanda interna (PN01774AM)? La pregunta del antecedente sigue
     abierta.
  2. R.b (episodios fuera de muestra con el *walk-forward* del PCA con 16 series) espera D17.

## 5. Qué no se hizo y por qué

1. **Tag remoto.** `git push origin v0.4-17series-dos-vias` devolvió **HTTP 403**, una denegación de
   la política del proxy. No lo reintenté por otra vía. El tag existe en el clon local, sobre
   `2be3665`. Para subirlo, Roberto o el orquestador deben correr ese mismo comando desde un entorno
   con permiso.
2. **DR (secciones 4–6 del Rmd final), D10, D12 y R.b:** dependen de D17 (maxcl de la regla K,
   lectura del RV, D13 con la regla del 06) y de R1, que no están registradas.
   - La parametrización de 06, 06c, 07b, 07c y 09a se hará en DR.
   - Con ella irá la no regresión de `R_aede_cortes.csv`, `09a_datacion_criterios.csv` y
     `R_hfc_clases3.csv`.
3. **R.c (16 frente a 17) y M2 suplementaria:** descartadas por Roberto.
4. **D9, punto 4.** No escribí `09a_discriminacion_episodios.csv`.
   - El criterio 8 se verifica con una prueba (`pytest`) para no agregar resultados con 17 series en
     las carpetas del antecedente.
   - La discriminación oficial con fechas nuevas es R.b (adenda, §4).
5. **D9, punto 5 (bordes de ventana).** Están implementados y probados: `src/episodios.bordes_ventana`
   y `borde_ventana`, y la función del Rmd final. El CSV se escribirá en DR/D10, que es donde se
   consume.
6. **`modelos_dl.py`:** se cambió solo la lectura del diccionario. No se ejecutó porque falta
   `torch`; el bloque nuevo se probó aislado.

## 6. Desviaciones respecto de la adenda, de `decisiones.qmd` o del marco

1. **Commit del tag.** El encargo decía `81d8a94` «o el que indique la adenda». La adenda indica
   `2be3665`, y ese es el que usé. `2be3665` solo agrega D15 y D16 (`decisiones.qmd` y `CLAUDE.md`)
   sobre `81d8a94`: los resultados son los mismos.
2. **`cargar_vias(excluidas=())` por defecto conserva 17 series.**
   - La adenda dice que `src/datos.py` excluye M2 al leer. La exclusión es el parámetro único
     `EXCLUIDAS_D16`, y los notebooks vigentes (05, 05c) lo pasan desde su bloque de parámetros.
   - Dejé el valor por defecto en 17 para que los notebooks antecedentes (06c, 07b, 07c, 09a,
     `999_port_camiz`) sigan reproduciendo sus CSV si se vuelven a ejecutar.
   - En DR, cada uno recibirá el parámetro explícito.
3. **Nulo mixto: definiciones operativas mías**, porque D8 no las fija.
   - *Indeterminadas:* «se informa con las dos variantes» lo leí como dos nulos completos: uno que
     trata las indeterminadas como TS (`mixto_ind_ts`) y otro como DS, con la regla HAC
     (`mixto_ind_ds`).
   - *Series TS:* se simulan como su recta MCO más sus residuos remuestreados en bloques de 12 meses,
     con los mismos inicios sorteados para los incrementos (caben en las 228 filas).
   - *HAC:* Newey-West con núcleo de Bartlett, 12 rezagos y sin corrección por grados de libertad.
     Coincide con `statsmodels` (`use_correction=False`).
   - *\|t\| > 2:* estricto.
4. **Secciones 2 y 3 del Rmd final: qué partes del documento de exploración se trasladaron.**
   - *Trasladadas:* D5, $n_{ef}$, adecuación, nulo y contraste sin tendencia en la sección 2; todo
     A.2 en la sección 3, más la tabla nueva de d = 2, 3, 4.
   - *No trasladadas:* la prueba ADF/KPSS «en nivel» de las dos vías (`b2-estacionariedad`) y la
     exploración de A.1 (mapas, saltos del crédito, correlaciones móviles). La adenda dice «partes
     de §2 y de A.1» sin enumerarlas. Si Roberto las quiere, se agregan.
   - *Prosa retirada:* los recuadros «Hallazgo» y las lecturas con conclusiones escritas para 17
     series (p. ej., «el primer componente es la tendencia común»). Las lecturas nuevas solo
     describen cifras calculadas en línea.
5. **Contraste sin tendencia sin la vía transformada.** En el Rmd final y en el 05 vigente, el
   contraste tiene dos versiones (niveles y sin tendencia). La comparación con las transformadas
   pasa a R.a.1. Con `VIA = 'ambas'`, el 05 conserva las tres versiones del antecedente.
6. **Episodios puntuales.** Para los cálculos (diccionario de `modelos_dl.py`, bordes, meses en
   episodio), fin efectivo = inicio. En los gráficos se dibujan con una línea discontinua. El CSV
   deja el fin vacío, como pide D7.
7. **Consumidores de D9.** El 06 y el 09a no usan episodios, así que no cambian. La columna
   `episodios_contenidos` del 09a sigue ausente (desviación 2 de la nota de la fase 0) y se agrega en
   DR. El Rmd de exploración, el 06a y el 06b conservan sus fechas a mano: están fuera del criterio 7
   (adenda, §4).
8. **Rutas de salida.** `05_dimensiones.csv` se escribe en `CARPETA` (antes, en `data/results/`).
   Las figuras del 05 vigente van en `reports/figures/final/`.
9. **Comprobaciones condicionadas en el 05.** La reproducción de las proporciones del HTML de la
   iteración 2 se exige solo con 17 series. Las comprobaciones de deriva, nulo mixto y dimensión, solo
   si el `R_*` las trae.
10. **`coef_rv`.** La opción también se agregó en `R/07b_nulo_estructura.R`, con el valor por
    defecto sin cambios. La copia del Rmd de exploración no se tocó (D15). Ningún resultado usa la
    variante sin centrar: su uso espera D17.
11. **Render para el asesor.** Lo hice con `output_dir` y sin `intermediates_dir`. Con
    `intermediates_dir` en el scratchpad, `rmarkdown` emite más de 50 avisos propios del entorno,
    ajenos al documento.

## 7. Para Roberto (decisiones que solo él puede tomar)

1. **D17 y R1** (adenda, §5): siguen sin registrar y bloquean DR, D10, D12 y R.b.
2. **Tag:** subir `v0.4-17series-dos-vias` desde un entorno con permiso (§5.1).
3. **Episodios:** confirmar las fechas principales de D9 frente a las alternativas fichadas (§4.1,
   duda 1).
4. **D8:** banda de «|t| cercano a 2» (§4.2, duda 1).
5. **Diagnóstico:** ¿se agregan al Rmd final las partes de A.1 que no se trasladaron (§6.4)?
