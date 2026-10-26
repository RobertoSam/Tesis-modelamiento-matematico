# Nota del desarrollador · 26 de octubre de 2026 · Parte dinámica con 16 series (D17)

**Encargo:** lo que la adenda (`asesoria/2026-10-26_adenda-plan-iteracion-3b.md`) dejó pendiente por
depender de D17, ya registrada (`decisiones.qmd`, commit `a933ace`). Todo en niveles, con 16 series
y en `data/results/final/`:

- DR: secciones 4 a 6 del Rmd final, y parametrización de 06, 06c, 07b, 07c y 09a con su prueba de
  no regresión;
- D10, D12 y el anexo R.b, con la discriminación de episodios recalculada.

AE y LSTM quedan en `\pendiente` (D17.4). Rama `iteracion-3b`; `git push` después de cada commit.

| Tarea | Commit | Estado |
|---|---|---|
| Parametrización (06, 06c, 07b, 07c, 09a, guion R del nulo) y no regresión con 17 series | `36458d7` | hecha y validada |
| DR · resultados de `aede`, λ por ventana, regla del 06, HFC y datación | `7e70318` | hecha y validada |
| D10 · nulo con el RV de D17.2, criterio de OE4 y 2017-10 | `0fd116c` | hecha y validada |
| D12 · datación con d ∈ {2, 3, 4} | `0ae1d39` | hecha y validada |
| R.b · *walk-forward* del PCA y discriminación | `5d7eb12` | hecha y validada |
| Rmd final: secciones 4 a 8, anexo R.b y paridad | `77588a5` | hecha y validada |
| Esta nota | commit siguiente | — |

**Regla 7.** No toqué `tesis_latex/`, `tesis/`, `04_resultados.*` ni `herramientas/generar_cifras.py`.
Las cifras de esta nota se calcularon con 16 series y **no tienen interpretación consolidada**. Las
líneas de interpretación solo describen las cifras y no dicen nada sobre la Parte C.

## 1. Archivos creados o modificados

| Archivo | Estado | Contenido |
|---|---|---|
| `src/parametros.py` | nuevo | Bloque común de parámetros (`TESIS_VIA`, `TESIS_EXCLUIDAS`, `TESIS_CARPETA`, `TESIS_R_*`), igual que en el 05. Por defecto: niveles, 16 series, `final/`. Se detiene si la salida es una carpeta del antecedente |
| `src/nulo_estructura.py` | modificado | `medir(objetos_rv=...)`: cargas sin centrar y correlación completa (D17.2), cargas centradas (antecedente) y columna `frontera` |
| `src/dinamica.py` | nuevo | `criterio_oe4` (p5 por posición; réplica fuera), `marcar_transiciones`, `fuera_del_nulo`, `tabla_2017_10` |
| `src/particion.py` | modificado | `grilla_datacion` con `n_segmentos_en_minimo` y `segmentos_en_minimo` (D17.1) |
| `src/deteccion.py` | nuevo | *Walk-forward* del PCA (parte PCA del 09), `discriminacion_larga` y `ampliar_episodios` |
| `R/07b_nulo_estructura.R` | modificado | Parámetros por variables de entorno (`TESIS_RV=d17` o `antecedente`); RV de D17.2; criterio de OE4 con las réplicas de R |
| `R/ciclo_financiero_final.Rmd` | modificado | Secciones 4 a 8 y anexo R.b (antes en pendiente); 23 filas nuevas de paridad |
| `notebooks/06_epca.ipynb`, `06c_aede_grilla.ipynb`, `07c_hfc_clases.ipynb`, `09a_datacion_pca.ipynb`, `07b_nulo_estructura.ipynb` | modificado | Parámetros. El 09a agrega la grilla con d ∈ {2, 3, 4} y los episodios contenidos; el 07b agrega OE4 y la lectura de D10 |
| `notebooks/09b_walkforward_pca.ipynb` | nuevo | Anexo R.b en Python |
| `herramientas/no_regresion_dinamica.py` | nuevo | No regresión con 17 series (adenda, §3) |
| `tests/test_dinamica.py`, `tests/test_deteccion.py` | nuevo | Criterio de OE4, regla de 2017-10, *walk-forward* y discriminación |
| `tests/test_nulo_estructura.py` | modificado | Dos objetos de RV, frontera, correlación completa frente a cargas completas y RV del antecedente |
| `data/results/final/` | 46 CSV nuevos | 06\_, 06c\_, 07b\_, 07c\_, 09a\_, `R_*` de las secciones 4 a 6; los dos `R_paridad_python.csv` se actualizaron |
| `data/results/final/anexo/` | 4 CSV nuevos | 09b\_\* y `R_anexo_{walkforward_pca,discriminacion}.csv` |
| `reports/figures/final/06_epca_*_niveles.png` | nuevo | Figuras del 06 |

No cambiaron ni el Rmd de exploración (md5 `c21946b6bb1bc3f3d160cb8b3e8f6e3f`, el de `2be3665`) ni
ningún CSV del antecedente: `git diff --stat a933ace -- data/results ':!data/results/final'` sale
vacío (criterio 17).

## 2. Comandos de ejecución (orden obligatorio)

Desde la raíz:

```
Rscript R/07b_nulo_estructura.R
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')"
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/05_pca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/05c_anexo_no_diferenciar.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06c_aede_grilla.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/07c_hfc_clases.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/09a_datacion_pca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 --ExecutePreprocessor.timeout=7200 notebooks/07b_nulo_estructura.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/09b_walkforward_pca.ipynb
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')"
python3 -m pytest tests/ -q
python3 herramientas/no_regresion_05.py
python3 herramientas/no_regresion_dinamica.py
```

- **Tiempos en este entorno (2 núcleos):** guion del nulo, 9,6 min; render, unos 2 min; 07b, 7 min;
  los demás notebooks, menos de 25 s cada uno; no regresión dinámica, 5,7 min.
- **El 07b va después del 06 y del 06c,** porque lee sus transiciones.
- **El segundo render lee las cifras del nulo con 200 réplicas,** que calcula Python.
- **Semillas:**
  - guion del nulo: `set.seed(2026)` antes de cada L;
  - Rmd: `params$semilla = 2026` (índices bootstrap y Horn por ventana);
  - 06c: `SEMILLA = 2026`, solo para el umbral informativo de numpy;
  - los demás notebooks no sortean (índices compartidos).

**Validación final:**

- `pytest`: 51 pruebas aprobadas. `herramientas/no_regresion_05.py`: superada (37 archivos).
- nbconvert con exit 0: 06, 06c, 07b, 07c, 09a y 09b.
  - El 05 y el 05c no cambiaron en esta sesión: el segundo render los vuelve a comparar (filas en «sí»).
- Render normal y `version_asesor = TRUE`: exit 0, sin `Warning` ni `Error` de R en el registro ni en
  el HTML. Recuadros `class="pregunta"`: 19 en la versión normal y 0 en la del asesor.
- Criterio 16: el Rmd recorre los CSV de `final/` y `final/anexo/` y ninguno contiene «Liquidez M2».

## 3. Paridad Python–R y no regresión

- **64 de 64** comprobaciones coinciden: 55 en `data/results/final/R_paridad_python.csv` y 9 en
  `data/results/final/anexo/R_paridad_python.csv`. La diferencia máxima es 2,7e-13.
- Las tablas discretas (k, cortes, clases, marcas y fechas) coinciden fila a fila.
- **Excepciones declaradas en la propia tabla:**
  - las réplicas 21 a 200 del nulo con L = 24 solo existen en Python (se comprueba que estén las 200);
  - el criterio de OE4 se compara con 20 réplicas, las mismas en las dos lenguas;
  - la lectura de D10 y de 2017-10 en R usa el p5 por posición de las 200 réplicas de Python como
    umbral compartido, igual que los umbrales de Horn.
- **En sentido inverso,** cada notebook compara sus salidas con los `R_*` y falla si difieren. Por
  ejemplo, el 07b informa 0 k\* distintos de 1 464, RV a 7,7e-15 en 48 720 pares, p5 por posición a
  2,0e-15 y criterio de OE4 a 5,0e-16.

**No regresión** (adenda, §3), con `herramientas/no_regresion_dinamica.py`: 17 series, dos vías,
carpetas temporales y los `R_*` del antecedente.

- **Notebooks 06, 06c, 07c y 09a:** los 31 CSV del antecedente son idénticos byte a byte, salvo
  cuatro ampliados en columnas en los que las columnas antiguas son idénticas:
  - `09a_datacion_criterios.csv`, en las dos vías, con las columnas de D17.1;
  - `09a_regimenes_pca.csv`, en las dos vías, con `episodios_contenidos`.
- **Rmd final** con `excluidas = character(0)`: 13 `R_*` del antecedente en niveles.
  - `R_aede_cortes.csv`, `R_hfc_clases3.csv` y otros 10 son idénticos byte a byte.
  - `R_datacion_criterios.csv` está ampliado en columnas.
  - Con 60 meses, la regla del 06 reproduce las transiciones del antecedente (`stopifnot`).
- **`09a_datacion_criterios.csv` y `05_pca_valores_propios.csv`:** el primero está en la lista
  anterior; el segundo ya lo cubre `herramientas/no_regresion_05.py`.
- **Nulo de estructura (parcial, por su costo),** con el RV centrado del antecedente:
  - Python reproduce los k\* de la serie observada y su perfil RV (diferencia máxima 9,7e-17);
  - el guion R reproduce las réplicas 0 a 2 de las dos vías (diferencia 0).
- **Walk-forward:** con 17 series, `src/deteccion.py` y el Rmd reproducen la columna `pca` de
  `09_walkforward_errores.csv` en las dos vías (diferencia máxima 1,5e-13, `tests/test_deteccion.py`).

## 4. Resultados (16 series, niveles; sin interpretación consolidada)

Convención de origen: archivo de `data/results/final/` · fila de datos (1 = primera fila tras el
encabezado) · columna.

### 4.1 `aede` en grilla (sección 4.1; `06c_aede_cortes.csv`)

| Resultado | Cifra | Origen |
|---|---|---|
| Codo con maxcl = 10 (D17.1), nw = 24 | 6 clases (uniformes), cortes 2008-07, 2009-06, 2011-11, 2020-10 y 2024-03; 2 clases (gaussianos), corte 2018-06 | filas 1 y 10 · `k`, `cortes` |
| Codo con maxcl = 10, nw ≥ 36 | 2 clases en las 6 combinaciones, con un corte entre 2020-02 y 2020-09 | filas 19, 28, 37, 46, 55, 64 · `k`, `cortes` |
| CH con k gl en el tope | 23 de 24 combinaciones de ancho × pesos × maxcl; la excepción es nw = 48, gaussianos, maxcl = 10 (k = 3) | filas con `criterio` CH k gl · `k_en_tope`; fila 47 |
| Codo ante maxcl | el mismo k y los mismos cortes con maxcl = 10, 15 y 20 en los 8 pares ancho × pesos | `criterio` = codo · `k`, `cortes` |

- **Interpretación:** con 16 series, el codo de `aede` separa, para nw ≥ 36, un solo cambio del
  primer valor propio, ubicado en 2020.
- **Dudas abiertas:**
  1. Con nw = 24 y pesos gaussianos, el codo da 2 clases y no 6, como con pesos uniformes. ¿Es efecto
     del n de Kish (18,2, cercano a p = 16)?
  2. El CH sigue sin óptimo interior con maxcl = 20, así que D11 lo deja fuera como selector.

### 4.2 Valores propios por ventana (sección 4.2; `06c_aede_valores_propios_resumen.csv`)

| Resultado | Cifra | Origen |
|---|---|---|
| n de Kish con pesos gaussianos (nw 24 / 36 / 48 / 60) | 18,24 / 27,63 / 37,01 / 46,40 | filas 4, 10, 16, 22 · `n_omega` |
| Ventanas con λ2 bajo el p95 de Horn, pesos uniformes (nw 24 / 36 / 48 / 60) | 117 / 52 / 20 / 2 (de 205 / 193 / 181 / 169) | filas 2, 8, 14, 20 · `bajo_horn`, `ventanas` |
| Ventanas con λ3 bajo Kaiser, pesos uniformes | 76 / 55 / 50 / 33 | filas 3, 9, 15, 21 · `bajo_kaiser` |
| Ventanas con λ1 bajo Horn | 0 en toda la grilla | filas con `eje` = 1 · `bajo_horn` |
| Ventanas con una serie constante (tasa de referencia), nw = 24 | 7 | filas 1–6 · `serie_constante` |
| Cruces λ2 ↔ λ3 | 19 en la grilla (uniformes 3, 3, 1, 2; gaussianos 5, 1, 3, 1) | `cruces_2_3`; detalle en `06c_aede_cruces.csv` |

- **Interpretación:** λ1 supera a Horn en todas las ventanas. λ2 supera a Horn en al menos el 80 % de
  las ventanas solo con nw ≥ 48, y λ3 queda bajo Kaiser en una de cada cinco ventanas o más con
  cualquier ancho.
- **Dudas abiertas:**
  1. Horn con n = ⌈n_ω⌉ y sin pesos es una aproximación; la duda de la nota de la fase 0 (§4.3)
     sigue abierta.
  2. El 06c informa además el umbral propio de numpy: difiere del de R hasta en 0,031 y cambia el
     conteo en 4 de 24 filas (salida del notebook). Por eso el conteo oficial usa el umbral
     compartido.

### 4.3 Regla del 06 por ancho (sección 4.3; `06_epca_transiciones_ventanas_niveles.csv`)

| Ancho | Transiciones (centro de la ventana posterior) | Origen |
|---|---|---|
| 24 | 7: 2008-07, 2009-10, 2012-07, 2013-07, 2015-01, 2017-01, 2024-07 | filas 1–7 |
| 36 | 5: 2009-10, 2011-04, 2012-07, 2014-07, 2018-10 | filas 8–12 |
| 48 | 7: 2011-07, 2012-01, 2013-04, 2014-04, 2016-01, 2018-04, 2022-07 | filas 13–19 |
| 60 | 5: 2012-01, 2013-10, 2015-10, 2017-10, 2018-01 | filas 20–24 |

- **Interpretación:** con 16 series, la regla da con 60 meses las mismas cinco fechas que con 17
  (nota de la fase 0, §4.4). 2017-10 sigue apareciendo solo con 60 meses.
- **Duda abierta:** la regla marca transiciones con un umbral relativo (media − 1 DE), de modo que
  siempre produce transiciones con cualquier ancho. Su lectura es la de §4.5.

### 4.4 Nulo de estructura y criterio de OE4 (sección 4.4; D10, D17.2)

| Resultado | Cifra | Origen |
|---|---|---|
| **OE4 principal** (cargas sin centrar, L = 24, 200 réplicas): proporción de pares bajo su p5, uniformes (nw 24 / 36 / 48 / 60) | 0,022 / 0,051 / 0 / 0; p-valor 0,695 / 0,45 / 1 / 1 | `07b_nulo_estructura_oe4.csv` · filas 1, 3, 5, 7 · `prop_obs`, `p_valor` |
| Ídem, gaussianos | 0,033 / 0,064 / 0,015 / 0; p-valor 0,62 / 0,38 / 0,475 / 1 | ídem · filas 2, 4, 6, 8 |
| Proporción nula: p50 y p95 (principal) | p50 entre 0 y 0,044; p95 entre 0,15 y 0,24 | ídem · filas 1–8 · `prop_nulo_p50`, `prop_nulo_p95` |
| Sensibilidad: RV de la correlación completa (L = 24, 200) | p-valores de 0,40 a 1 | ídem · filas 9–16 · `p_valor` |
| Sensibilidad L = 12 y L = 36 (20 réplicas) | menor p-valor 0,15 (L = 36, nw = 48, gaussianos, en los dos objetos) | ídem · filas 54 y 62 · `p_valor` |
| k\* del codo observado frente al nulo (L = 24) | nw = 24 uniformes: k = 6, P(k nulo ≥ 6) = 0,245; nw ≥ 36: k = 2, P(k nulo ≤ 2) entre 0,25 y 0,33 | `07b_nulo_estructura_kstar_posicion.csv` · filas 25, 31, 34, 37, 40, 43, 46 · `prop_nulo_ge_obs`, `prop_nulo_le_obs` |
| Réplicas nulas en que el CH con k gl elige el tope (k = 20), L = 24 | 89,5 % a 100 % | ídem · filas 26, 29, …, 47 · `prop_nulo_en_tope` |
| Única excepción interior del CH con k − 1 gl (nw = 48, gaussianos, k = 2) | P(k nulo ≤ 2) = 0,03 | ídem · fila 42 · `prop_nulo_le_obs` |

- **Interpretación:**
  - Con el criterio de OE4 de D17.2, ningún ancho ni esquema de pesos tiene más pares bajo el p5 que
    los que da el nulo de estructura constante (todos los p-valores principales ≥ 0,38).
  - Con nw ≥ 48 y pesos uniformes, ningún par observado queda bajo su p5.
- **Dudas abiertas:**
  1. La proporción nula tiene un p95 alto (0,15 a 0,24), es decir, el nulo es muy disperso. El
     criterio tiene, por tanto, poco poder (riesgo 3 del plan).
  2. El nulo acumula incrementos desde 0 y conserva la deriva de cada serie (versión «con deriva»).
     Falta contrastarlo con un nulo que use el tratamiento mixto de D8, que el plan no pidió para D7.
  3. Que la proporción observada sea 0 con nw ≥ 48 puede deberse a que el RV observado entre ventanas
     adyacentes es más alto que el del nulo. Esa lectura no está calculada.

### 4.5 Transiciones con borde de ventana y 2017-10 (sección 4.5; D10, D13, D17.3)

| Resultado | Cifra | Origen |
|---|---|---|
| Candidatos (regla del 06 y codo de `aede` con maxcl = 10) | 36 | `07b_transiciones_d10.csv` · filas 1–36 (`objeto` = cargas_sin_centrar) |
| Candidatos que coinciden con un borde de ventana a ±3 meses | 16 de 36 | ídem · `es_borde_3` |
| Candidatos fuera del nulo | 2: regla del 06 con nw = 36 en 2012-07 (4 de 7 pares cercanos bajo su p5) y `aede` gaussiano con nw = 48 en 2020-05 (2 de 7), este último también borde («Sale Kuczynski / Odebrecht») | ídem · filas 10 y 34 · `fuera_del_nulo`, `pares_cercanos_bajo_p5`, `borde_3` |
| Candidatos a ±3 meses de 2017-10 | solo la regla del 06 con nw = 60: 2017-10 y 2018-01, los dos borde («Entra COVID-19») y ninguno fuera del nulo | `07b_tabla_2017_10.csv` · fila 4 · `candidatos`, `algun_no_borde`, `algun_fuera_del_nulo` |
| **Clasificación de 2017-10** (D13 con D17.3) | **transición no confirmada**, con el RV principal y con el de sensibilidad | `07b_clasificacion_2017_10.csv` · filas 1 y 2 · `clasificacion` |

- **Interpretación:** 2017-10 aparece con un solo ancho, en un solo método y sin pesos gaussianos.
  Coincide con el centro en que el COVID-19 entra en la ventana de 60 meses (2020-03 menos 29 meses)
  y no queda fuera del nulo.
- **Dudas abiertas:**
  1. «Fuera del nulo» es una definición mía: algún par con frontera a ±3 meses bajo su p5. ¿La acepta
     el Dr. Camiz (pregunta en el Rmd)?
  2. En `aede` usé el codo con maxcl = 10. D17.1 fija maxcl para la regla K de la datación, no el
     criterio de `aede`: es una ambigüedad declarada (§6).

### 4.6 HFC (sección 5; `07c_hfc_*`)

| Resultado | Cifra | Origen |
|---|---|---|
| 3 clases | C1: créditos (3), M1, M3, TAMN, IPC, tipo de cambio, PBI, demanda interna y reservas (11 series), representante el crédito hipotecario; C2: tasa de referencia, interbancaria y TIPMN, representante la interbancaria; C3: índice BVL y EMBIG, representante el EMBIG | `07c_hfc_clases3.csv` · filas 1–16 · `clase`, `serie`, `representante` |
| 4 clases | C3 se divide en índice BVL y EMBIG | ídem · filas 17–32 |
| Rand ajustado mediano (3 / 4 clases) y p5 | 1,00 / 1,00; p5 0,80 / 0,51 | `07c_hfc_bootstrap.csv` · columnas `ari_3`, `ari_4` (500 filas) |
| Réplicas con la partición exacta (3 / 4 clases) | 80,0 % / 63,2 % | ídem |
| Correlación cofenética mediana | 0,993 | ídem · `cofenetica` |
| Pares con coclasificación entre 0,1 y 0,9 (de 120) | 12 (3 clases), 37 (4 clases) | `07c_hfc_coclasificacion.csv` · `frec_3`, `frec_4` |
| Correlación de los factores C1–C3 | −0,483 (p5 a p95: −0,644 a −0,176); sin tendencia, 0,152 (−0,149 a 0,401) | `07c_hfc_correlaciones3.csv` · filas 2 y 8 · `r`, `p5`, `p95` |
| Correlación de los factores C1–C2 sin tendencia | −0,411 (−0,637 a −0,005) | ídem · fila 7 |

- **Interpretación:** con 16 series, la partición es la del antecedente con 17 series, sin M2, y su
  estabilidad bootstrap es prácticamente la misma.
- **Dudas abiertas:** siguen vigentes las de la fase 0 (§4.5): la definición de la serie
  representante, la estabilidad que puede deberse a la tendencia común y los intervalos con la
  partición fija.

### 4.7 Datación (sección 6; D12, D17.1)

| Resultado | Cifra | Origen |
|---|---|---|
| **Principal** (d = 3, maxcl = 10, regla K) | **6 regímenes**, por el paso 2 (caída máxima): cortes 2008-12, 2010-03, 2014-04, 2020-06, 2022-11 | `09a_datacion_criterios.csv` · fila 4 · `k`, `regla_k`, `cortes` |
| Regla K con maxcl = 15 y 20 (sensibilidad) | 11 regímenes, por el paso 1 (umbral de 10 %) | ídem · filas 8 y 12 |
| Tramos de exactamente 12 meses | 1 o 2 en todas las soluciones; `segmentos_en_minimo` = falso en las 12 filas | ídem · `n_segmentos_en_minimo`, `segmentos_en_minimo` |
| CH con k y k − 1 gl con maxcl = 10 | 10, en el tope | ídem · filas 2–3 · `k_en_tope` |
| D12: regla K con maxcl = 10 (d = 2 / 3 / 4) | 6 / 6 / 4 regímenes; con d = 4: 2012-04, 2020-05, 2022-11 | `09a_datacion_dimension.csv` · filas 4, 16, 28 · `k`, `cortes` |
| D12: regla K con maxcl = 15 y 20 (d = 2 / 3 / 4) | 10 / 11 / 13 | ídem · filas 8, 20, 32 (iguales a 12, 24, 36) |
| Estabilidad de los cortes (200 réplicas, ±3 meses) | 2008-12: 0,855; 2010-03: 0,975; 2014-04: 0,400; 2020-06: 0,955; 2022-11: 1,000 | `09a_estabilidad_cortes.csv` · filas 1–5 · `frecuencia` |
| Fases (regla del 09) | transición, transición, contracción, transición, expansión, expansión; el régimen de 2014-04 a 2020-05 contiene las materias primas, Kuczynski, la guerra comercial y el COVID-19 | `09a_regimenes_pca.csv` · filas 1–6 · `fase`, `episodios_contenidos` |

- **Interpretación:**
  - Con 16 series, la datación principal tiene 6 regímenes y los mismos cortes que con 17 (nota de la
    fase 0, §4.1).
  - Pasar a maxcl = 15 lleva a 11 regímenes, como en el antecedente.
  - El corte de 2014-04 es el único que se reproduce en menos de la mitad de las réplicas.
- **Dudas abiertas:**
  1. La marca literal de D17.1 (todos los tramos en 12 meses) no puede cumplirse con 217 meses
     suavizados. ¿Se acepta el conteo como sustituto, o se define otra marca?
  2. Con d = 4 y maxcl = 10, la regla K da 4 regímenes y pierde los cortes de 2008-12 y 2010-03.
     ¿Cómo se informa una sensibilidad de la dimensión que cambia el número de regímenes?
  3. La regla de fases del 09 ordena los regímenes según la tendencia (pregunta en el Rmd).

### 4.8 Anexo R.b: detección de episodios fuera de muestra (`anexo/09b_*`)

| Resultado | Cifra | Origen |
|---|---|---|
| Falsas alarmas del PCA con 16 series, transformadas (tolerancia 0 / ±3 / ±6) | 3,9 % / 0,9 % / 1,0 % | `anexo/09b_discriminacion_episodios.csv` · filas 2, 14, 26 · `valor` |
| Ídem sin transformar (contraste) | 59,7 % / 59,6 % / 56,7 % | ídem · filas 146, 158, 170 |
| Sensibilidad, transformadas, tolerancia 0 | COVID-19 100 % (2 meses), Kuczynski 100 % (1 mes); taper tantrum, materias primas y guerra comercial: 0 % | ídem · filas 4–12 (pares) |
| Sensibilidad, transformadas, ±3 meses | COVID-19 62,5 %, Kuczynski 28,6 %, guerra comercial 15,4 %; los otros dos, 0 % | ídem · filas 16–24 (pares) |
| AE y LSTM con 17 series (antecedente) y episodios nuevos, transformadas, tolerancia 0 | falsas alarmas 3,9 % (AE) y 3,1 % (LSTM); en el archivo, `series` = 17 | ídem · filas con `series` = 17, `via` = transformadas |
| Error *walk-forward* por mes (16 series) | 180 meses por vía (2011-01 a 2025-12) | `anexo/09b_walkforward_pca.csv` · `pca` |

- **Interpretación:** con 16 series y los episodios del archivo único, el PCA en las series
  transformadas tiene pocas falsas alarmas y solo detecta los episodios cortos (COVID-19, Kuczynski).
  Sin transformar, más de la mitad de los meses fuera de episodios son alarmas.
- **Dudas abiertas:**
  1. La tolerancia de ±3 meses de D7 se pensó para fechar transiciones. Aquí la usé para ampliar los
     episodios (lectura propia; pregunta en el Rmd).
  2. Con tolerancia, los episodios ampliados se superponen (Kuczynski con la guerra comercial, esta
     con el COVID-19) y un mes cuenta en los dos.
  3. Los episodios de 1 y 2 meses dan sensibilidades de 0 % o 100 %, sin término medio.

## 5. Qué no se hizo y por qué

1. **AE y LSTM con 16 series:** quedan en `\pendiente` (D17.4; falta `torch`). Solo se recalculó su
   discriminación con los episodios nuevos, a partir de sus errores con 17 series, rotulada como
   antecedente.
2. **No regresión completa del 07b con 17 series:** por su costo (unos 20 min), solo se comprobaron
   la serie observada (Python) y las réplicas 0 a 2 (R). La adenda no la exige.
3. **Estabilidad de cortes con d = 2 y d = 4:** D12 pide la datación con esas dimensiones, no su
   bootstrap.
4. **Tag remoto `v0.4-17series-dos-vias`:** sigue sin subir (HTTP 403; nota de la adenda, §5.1).
5. **El 05 y el 05c no se volvieron a ejecutar:** su código y sus entradas no cambiaron, y la paridad
   del segundo render los compara.

## 6. Desviaciones respecto del encargo, de la adenda o de `decisiones.qmd`

1. **Commits.** Un commit de código, cuatro de resultados por tarea y uno de integración en el Rmd.
   - Motivo: el Rmd final y las dos tablas de paridad reúnen todas las tareas en un solo archivo.
   - La validación (pytest, nbconvert, render y no regresión) se hizo sobre el estado final, no
     sobre cada commit intermedio.
2. **Criterio de `aede` para D10 y 2017-10.** Usé el codo (caída máxima) con maxcl = 10. D17.1 fija
   maxcl = 10 para la regla K de la datación, y el CH no selecciona (D11). Que el criterio de `aede`
   sea el codo es mi lectura (ambigüedad declarada, no decidida).
3. **Definiciones operativas mías** (en `src/dinamica.py` y en el Rmd):
   - *Frontera del par:* el primer mes de la segunda ventana.
   - *«Fuera del nulo»:* algún par a ±3 meses bajo su p5.
   - *p-valor de OE4:* la proporción de réplicas con una proporción mayor o igual que la observada.
   - *Cuantiles:* tipo 7.
   - *La regla del 06* se lee con los pares de pesos uniformes.
4. **RV de la correlación completa.** Usé la matriz ponderada con los pesos de `aede`, `bstatw`, la
   misma que diagonaliza `aede`. Con una serie constante en la ventana, su fila queda en 0, como en
   `aede`. El RV es tr(R_a R_b)/√(tr R_a² · tr R_b²).
5. **Cifras oficiales del nulo con 200 réplicas solo en Python.** El Rmd las lee de los CSV de Python y
   usa su p5 por posición para la lectura de D10 y de 2017-10. R calcula y compara la versión con
   20 réplicas.
6. **`segmentos_en_minimo`.** Implementé la marca literal de D17.1 y agregué el conteo
   `n_segmentos_en_minimo`, porque la marca literal no puede cumplirse con n = 217.
7. **R.b.**
   - Se agregó la vía sin transformar como contraste, con el mismo código.
   - La tolerancia de ±3 y ±6 meses para ampliar episodios es una lectura propia.
   - Los resultados de AE y LSTM con 17 series quedan en `final/anexo/`, con `series` = 17 y
     `fuente` = antecedente. No contienen nombres de series (criterio 16).
8. **Archivos del 06 en `final/`:** conservan el sufijo `_niveles` para que la no regresión los compare
   por nombre. Las figuras van en `reports/figures/final/`.
9. **`07b_nulo_estructura_rv.csv` pesa 3,6 MB** (dos objetos de RV, 21 réplicas). Los perfiles de las
   réplicas 21 a 200 no se escriben: se resumen en `07b_nulo_estructura_rv_posicion.csv`.
10. **No regresión del RV centrado en Python:** se compara con tolerancia 1e-14 y no byte a byte
    (diferencia 9,7e-17).
11. **El 06 verifica el md5 de D4** de los dos archivos estandarizados que lee. Antes no lo hacía.

## 7. Para Roberto (decisiones o aclaraciones que solo él puede dar)

1. **Ambigüedad de D10 y D13:** ¿el codo de `aede` con maxcl = 10 es el candidato correcto para la
   tabla de 2017-10? (§6.2)
2. **Definición de «fuera del nulo»** y de la frontera del par (§4.5, duda 1). Se lleva al
   Dr. Camiz.
3. **D17.1:** ¿se acepta `n_segmentos_en_minimo` como sustituto de la marca literal? (§4.7, duda 1)
4. **R.b:** ¿se queda la regla del 09 sin tolerancia como lectura principal? (§4.8, duda 1)
5. **Pendientes de la nota anterior:** el tag remoto, la banda de |t| de D8 y las fechas
   alternativas de los episodios.

**Siguiente paso del ciclo:** el redactor LaTeX (L1 a L4) puede tomar de `final/` las macros de
**métodos y datos**: anchos, n de Kish, réplicas, tolerancias y p = 16. Después vienen el editor del
informe (E1 a E3) y la auditoría. El capítulo de resultados no se toca sin la aprobación de Roberto
(regla 7).
