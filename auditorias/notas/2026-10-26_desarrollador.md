# Nota del desarrollador · 26 de octubre de 2026 · Iteración 3b, fase 0 (D3 a D8)

**Encargo:** plan `asesoria/2026-10-21_plan-iteracion-3b.md`, sección 4 («Desarrollador», fase 0),
tareas D3, D4, D5, D6, D8 y D7, en ese orden. D1 y D2 ya estaban commiteadas (`f1c68f8`, `fd17c24`).
No se hicieron D9 a D12 (fase 1). Sesión de seguimiento diario, sin Roberto presente. Rama
`iteracion-3b`; un commit por tarea, cada uno con `git push origin iteracion-3b`.

| Tarea | Commit | Estado |
|---|---|---|
| D3 · `09a_datacion_pca.ipynb` | `a7ee103` | hecha y validada |
| D4 · `aede` en grilla | `ccc7682` | hecha y validada |
| D5 · valores propios por ventana | `db9085d` | hecha y validada |
| D6 · regla del 06 por ancho | `2c663c4` | hecha y validada |
| D8 · HFC en 3 y 4 clases y bootstrap | `5dc13eb` | hecha y validada |
| D7 · nulo de estructura constante | `bf471d8` | hecha y validada |
| Esta nota | commit siguiente | — |

**Convención.** «D1»…«D12» sin más son las **tareas** del desarrollador en el plan; las decisiones
de `decisiones.qmd`, cuya numeración coincide en parte, se citan siempre como «decisión Dn».

**Regla 7.** No toqué `04_resultados.*`, `tesis_latex/` ni `tesis/`. Las cifras de esta nota son
insumos de la fase 1: ninguna entra a la tesis ni al informe sin la lectura contra el nulo
(decisiones D10 y D11) y sin la aprobación de Roberto.

## 1. Entorno

- R 4.3.3 (apt). Paquetes de R desde apt (`r-cran-*`), con las mismas versiones de la nota de 3a:
  rmarkdown 2.25, knitr 1.45, ggplot2 3.4.4, scales 1.3.0, tseries 0.10.55, dendextend 1.17.1 (más
  urca y psych).
- Python 3: numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, scikit-learn 1.9.1. Instalé con
  `pip install --break-system-packages` statsmodels, nbconvert, nbformat, ipykernel y pytest, y
  registré el kernel `python3`.
- `torch` no está: 08 y 09 no se ejecutaron.
- **Render de línea base** (antes de tocar nada): exit 0 en 2 min 50 s, sin avisos, y ningún CSV
  de `data/results/` cambió (116 archivos, md5 comparados). Con todo lo de esta sesión el render
  tarda unos 5 min 20 s (D8 agrega 1 000 corridas de `clahfac`).

## 2. Archivos creados o modificados

**Código**

| Archivo | Estado | Tarea | Contenido |
|---|---|---|---|
| `src/datos.py` | nuevo | D3 | Carga verificada de las dos vías: md5 de D4, calendario continuo, sin faltantes, 228 × 17 y 227 × 17, lector de R |
| `src/particion.py` | modificado | D3 | `datar`, `media_movil_causal`, `scores_pca_rcamiz`, `estandarizar_r`, `grilla_datacion`, `estabilidad_cortes`; bucle interno de `fisher_multivariado` vectorizado con la misma aritmética |
| `src/multivariado.py` | modificado | D5 | `umbral_horn` (umbral de Horn sin valores observados) y `n_kish` |
| `src/nulo_estructura.py` | nuevo | D7 | `serie_nula` (bloque conjunto) y `medir` (k* y perfil RV) |
| `notebooks/09a_datacion_pca.ipynb` | nuevo | D3 | Datación PCA-MM12 sin torch, estabilidad de cortes y grilla |
| `notebooks/06c_aede_grilla.ipynb` | nuevo | D4, D5 | `aede` en grilla y valores propios por ventana |
| `notebooks/06_epca.ipynb` | modificado | D6 | Sección 7 nueva: regla del 06 por ancho; las secciones 1 a 6 no cambian |
| `notebooks/07c_hfc_clases.ipynb` | nuevo | D8 | HFC en 3 y 4 clases, factores, representantes y bootstrap |
| `notebooks/07b_nulo_estructura.ipynb` | nuevo | D7 | Nulo de estructura constante, 200 réplicas con L = 24 y 20 con L = 12 y 36 |
| `notebooks/999_port_camiz.ipynb` | modificado | D4 | Filtra `nw = 60, maxcl = 10` del `R_aede_cortes.csv` largo (2 celdas, 5 líneas) |
| `R/tesis_ciclo_financiero.Rmd` | modificado | D3–D8 | `datar` devuelve además `k_caida` y `k_max_efectivo`; sección nueva «Anexo 3b» (bloques `b3b-datacion`, `b3b-aede-grilla`, `b3b-valores-propios`, `b3b-regla06`, `b3b-hfc`, `b3b-nulo`); `tabla_aede` sube a `b3b-aede-grilla`; `escribir_via` recibe la tabla larga de `aede`; filas nuevas de paridad; `fila_tabla` (comparador de tablas discretas) |
| `R/07b_nulo_estructura.R` | nuevo | D7 | Guion R del nulo (fuera del Rmd por su costo, §4.6) |
| `tests/test_particion.py` | modificado | D3 | Media móvil causal frente a `rolling`; regla K y grilla en un caso conocido |
| `tests/test_camiz_port.py` | modificado | D4, D5 | `aede` con nw 24, 36 y 48 contra `R_aede_cortes.csv` (las dos vías, convención i + nw/2); n de Kish |

**Salidas** (NIV = `data/results/niveles/`, TRA = `data/results/`)

| Tarea | R (Rmd o guion) | Python |
|---|---|---|
| D3 | `R_datacion_criterios.csv`, `R_estabilidad_cortes.csv` (NIV y TRA) | `09a_regimenes_pca.csv`, `09a_estabilidad_cortes.csv`, `09a_datacion_criterios.csv` (NIV y TRA) |
| D4 | `R_aede_cortes.csv` (pasa a formato largo, NIV y TRA) | `06c_aede_cortes.csv` (NIV y TRA) |
| D5 | `R_aede_valores_propios.csv`, `R_aede_valores_propios_resumen.csv`, `R_aede_cruces.csv`, `R_aede_horn_umbrales.csv` (NIV y TRA) | `06c_aede_valores_propios.csv`, `06c_aede_valores_propios_resumen.csv`, `06c_aede_cruces.csv` (NIV y TRA) |
| D6 | `R_epca_regla06_transiciones.csv`, `R_epca_regla06_estabilidad.csv` (NIV y TRA) | `06_epca_transiciones_ventanas{,_niveles}.csv`, `06_epca_estabilidad_ventanas{,_niveles}.csv` (TRA, con el sufijo del 06) |
| D8 | `R_hfc_clases3.csv`, `R_hfc_correlaciones3.csv`, `R_hfc_bootstrap.csv`, `R_hfc_coclasificacion.csv` (NIV y TRA) | `07c_hfc_*` homólogos (NIV y TRA) |
| D7 | `R_nulo_estructura_indices_L{12,24,36}.csv`, `R_nulo_estructura_kstar.csv`, `R_nulo_estructura_rv.csv`, `R_nulo_estructura_rv_resumen.csv` (NIV y TRA) | `07b_nulo_estructura_{kstar,kstar_posicion,rv,rv_resumen,rv_nulo}.csv` (NIV y TRA) |

Más `R_paridad_python.csv` de cada vía, con filas nuevas.

## 3. Comandos de ejecución (orden obligatorio)

El Rmd escribe los índices y umbrales compartidos y los `R_*`; los notebooks los leen y se comparan
con ellos; el Rmd vuelve a leer los CSV de Python para la paridad. Desde la raíz:

```
Rscript R/07b_nulo_estructura.R
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/09a_datacion_pca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06c_aede_grilla.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/06_epca.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/07c_hfc_clases.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/07b_nulo_estructura.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/999_port_camiz.ipynb
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
python3 -m pytest tests/ -q
```

Tiempos medidos en este entorno (2 núcleos): guion del nulo, 26 min 27 s; render, unos 5 min;
07b, 12 min 54 s; 07c, 1 min; los demás, menos de 20 s.

Semillas: el Rmd usa `params$semilla = 2026` para los índices bootstrap (3a) y para el umbral de
Horn por ventana (D5); el guion del nulo fija `set.seed(2026)` antes de cada longitud de bloque.
Los notebooks no sortean nada salvo el umbral de Horn propio de numpy en el 06c (`SEMILLA = 2026`,
informativo; los conteos oficiales usan el umbral de R).

## 4. Resultados por tarea

Convención de origen: `archivo` · fila de datos (1 = primera fila tras el encabezado) · columna.
Las cifras de R y de Python coinciden en todos los casos citados (§5).

### 4.1 D3 · Datación PCA-MM12 sin torch (`09a`)

**No regresión.** Con maxcl = 10, el 09a reproduce `09_regimenes_pca.csv` en las dos vías (inicio,
fin, meses, componente de crédito y fase; `assert` del notebook): 6 regímenes sin transformar y 8
transformados. La columna `episodios_contenidos` no se reproduce (ver §6, desviación 2).

| Resultado | Cifra | Origen |
|---|---|---|
| Regla K con maxcl = 10, sin transformar | k = 6, por el paso 2 (caída máxima) | NIV `09a_datacion_criterios.csv` · fila 4 · `k`, `regla_k` |
| Regla K con maxcl = 15 y 20, sin transformar | k = 11, por el paso 1 (umbral de 10 %) | NIV `09a_datacion_criterios.csv` · filas 8 y 12 · `k`, `regla_k` |
| Regla K con maxcl = 10, 15 y 20, transformadas | k = 8, paso 1, los mismos cortes | TRA `09a_datacion_criterios.csv` · filas 4, 8 y 12 |
| CH con k y con k − 1 gl, sin transformar | 10 (en el tope) con maxcl = 10; 12 con maxcl = 15 y 20 (máximo factible 18) | NIV `09a_datacion_criterios.csv` · filas 2–3, 6–7, 10–11 · `k`, `k_en_tope` |
| Codo por caída máxima, transformadas, maxcl = 20 | k = 17, cortes en junio de cada año de 2009 a 2024 | TRA `09a_datacion_criterios.csv` · fila 9 · `k`, `cortes` |
| Mayor k factible con segmentos de 12 meses | 18 en las dos vías con maxcl = 20 | `09a_datacion_criterios.csv` · columna `k_max_efectivo` |
| Estabilidad de los cortes, sin transformar (200 réplicas, ±3 meses) | 2008-12: 0,85; 2010-03: 0,98; 2014-04: 0,35; 2020-06: 0,955; 2022-11: 1,00 | NIV `09a_estabilidad_cortes.csv` · filas 1–5 · `frecuencia` |
| Estabilidad de los cortes, transformadas | 1,00; 1,00; 0,93; 0,86; 0,93; 0,875; 1,00 (2009-06 a 2023-11) | TRA `09a_estabilidad_cortes.csv` · filas 1–7 · `frecuencia` |

- **Interpretación:** en las transformadas, la datación principal no depende de maxcl. Sin
  transformar, la regla K cambia de 6 a 11 regímenes al pasar de maxcl = 10 a 15, porque con 10 la
  grilla termina antes del primer k cuya reducción baja de 10 %. El corte de 2014-04 es el único
  que se reproduce en menos de la mitad de las réplicas.
- **Dudas abiertas:**
  1. La decisión D12 fija la regla K, pero no el maxcl con que se aplica. Sin transformar, el resultado
     depende de esa elección (6 o 11 regímenes). ¿Cuál es la especificación principal? Fijarlo
     ahora, conociendo esta cifra, tiene el mismo problema que el plan señaló para OE6. Lo dejo
     como decisión de Roberto.
  2. Con maxcl = 20 y segmentos de al menos 12 meses, k = 18 obliga a 18 tramos de exactamente
     12 meses. Eso deforma la curva de reducción cerca del tope: el codo por caída máxima en las
     transformadas elige 17 tramos casi anuales (fila 9). ¿Se acota maxcl a un valor menor que
     ⌊n/12⌋ o se informa como artefacto?
  3. La estabilidad de cortes mide la incertidumbre de las cargas con k fijo; no la del número de
     regímenes (ya lo dice el Rmd).

### 4.2 D4 · `aede` en grilla (`06c`, bloque `b3b-aede-grilla`)

**No regresión.** Las 6 filas con `nw = 60` y `maxcl = 10` de cada `R_aede_cortes.csv` (filas 55–57
y 64–66) son las de 3a (`stopifnot` en el Rmd; `assert` contra `999_port_aede_cortes.csv` en el
06c). `999_port_camiz` vuelve a dar sus mismas salidas byte a byte.

| Resultado | Sin transformar | Transformadas | Origen |
|---|---|---|---|
| CH con k gl en el tope (k = maxcl), de 8 combinaciones nw × pesos | 7 (maxcl 10), 8 (15), 8 (20) | 7, 7, 8 | `R_aede_cortes.csv` · `criterio`, `maxcl`, `k_en_tope` |
| CH con k − 1 gl en el tope | 2, 3, 4 de 8 | 6, 6, 8 de 8 | ídem |
| Codo por caída máxima | 6 con nw = 24; 2 con nw = 36, 48 y 60 (todas las combinaciones de pesos y maxcl) | 3 o 4, salvo nw = 24 gaussiano con maxcl 15 y 20 (10) | ídem · `k` |
| Única excepción interior del CH con k gl | nw = 48, gaussianos, maxcl = 10: k = 3 | nw = 36, uniformes, maxcl = 10: k = 9 | NIV fila 47; TRA fila 20 · `k` |

- **Interpretación:** con maxcl = 20, el CH con k gl elige el tope en las 16 combinaciones de las
  dos vías; con k − 1 gl, en 4 de 8 sin transformar y en 8 de 8 transformadas. El codo es estable
  ante maxcl en casi toda la grilla.
- **Dudas abiertas:**
  1. La decisión D11 condiciona el uso del CH a un óptimo interior con maxcl = 20. En esta grilla no lo hay
     con k gl. Sin transformar, con k − 1 gl, sí hay óptimos interiores (k = 2) en 4
     combinaciones. Se leen contra el nulo de la tarea D7 (§4.6).
  2. Sin transformar, el codo pasa de 6 (nw = 24) a 2 (nw ≥ 36). ¿Es la escala de la ventana o el
     tramo de 2011–2013 con la tasa de referencia constante (§4.3)?

### 4.3 D5 · Valores propios por ventana (`06c`, sección 2; bloque `b3b-valores-propios`)

**Comprobaciones del criterio 5 del plan** (`stopifnot` y `assert`): λ1 + λ2 + λ3 ≤ 17 en todas las
filas; $n_\omega = n_w$ con pesos uniformes; con pesos uniformes y nw = 60, las columnas λ son
`aede_u$a$eigenvalues` (idénticas).

| Resultado | Cifra | Origen |
|---|---|---|
| $n$ de Kish con pesos gaussianos (nw 24 / 36 / 48 / 60) | 18,24 / 27,63 / 37,01 / 46,40 | `R_aede_valores_propios_resumen.csv` · filas 4, 10, 16, 22 · `n_omega` |
| Ventanas con λ1 bajo el p95 de Horn, transformadas, nw = 24 | 7 de 204 (uniformes) y 33 de 204 (gaussianos) | TRA ídem · filas 1 y 4 · `bajo_horn`, `ventanas` |
| Ventanas con λ1 bajo Horn, cualquier vía, nw ≥ 36 | 0 | NIV y TRA ídem · `eje = 1` · `bajo_horn` |
| Ventanas con λ2 bajo Horn, sin transformar (nw 24 / 36 / 48 / 60, uniformes) | 117 / 53 / 22 / 2 | NIV ídem · filas 2, 8, 14, 20 · `bajo_horn` |
| Ventanas con λ2 bajo Horn, transformadas (ídem) | 51 / 22 / 3 / 0 | TRA ídem · filas 2, 8, 14, 20 · `bajo_horn` |
| Ventanas con λ3 bajo Kaiser, sin transformar (nw 24 / 36 / 48 / 60, uniformes) | 71 / 51 / 49 / 31 | NIV ídem · filas 3, 9, 15, 21 · `bajo_kaiser` |
| Ventanas con λ3 bajo Kaiser, transformadas | 0 en toda la grilla | TRA ídem · `bajo_kaiser` |
| Ventanas con una serie constante (tasa de referencia), nw = 24 | 7 sin transformar (centros 2012-05 a 2012-11) y 6 transformadas (2012-06 a 2012-11); ninguna con nw ≥ 36 | `…_resumen.csv` · `serie_constante` |
| Cruces λ2 ↔ λ3 (total en la grilla) | 16 sin transformar; 26 transformadas | NIV y TRA `R_aede_cruces.csv` (16 y 26 filas) |

- **Interpretación:** con nw = 24 y pesos gaussianos ($n_\omega$ ≈ 18 ≈ p), en las transformadas
  ni siquiera λ1 supera a Horn en una de cada seis ventanas (33 de 204), como anticipaba el
  diagnóstico (§1.6 del plan). λ2 supera a Horn en al menos el 80 % de las ventanas solo con
  nw ≥ 48, en las dos vías y con los dos esquemas de pesos.
- **Dudas abiertas:**
  1. Horn se calcula con $n = \lceil n_\omega \rceil$ observaciones **sin pesos**. Es la
     especificación del plan, pero es una aproximación: la distribución de los valores propios de
     una matriz de correlaciones **ponderada** no es la de una sin pesos con el mismo $n$ de Kish.
     Conviene verificarla con simulaciones ponderadas antes de la fase 1.
  2. El registro de cruces usa una definición mía (§6, desviación 5). ¿Es la que pide el
     apunte 7?

### 4.4 D6 · Regla del 06 por ancho (`06_epca`, sección 7; bloque `b3b-regla06`)

**No regresión.** Con 60 meses, las transiciones coinciden con `06_epca_transiciones_detectadas*.csv`
(`assert` y `stopifnot`), que no cambian.

| Vía (componente) | nw = 24 | nw = 36 | nw = 48 | nw = 60 | Origen |
|---|---|---|---|---|---|
| Sin transformar (PC2) | 8 transiciones (2009-10 … 2024-07) | 6 (2009-10 … 2021-07) | 7 (2011-07 … 2022-07) | 5: 2012-01, 2013-10, 2015-10, 2017-10, 2018-01 | `06_epca_transiciones_ventanas_niveles.csv` · filas 1–8, 9–14, 15–21, 22–26 |
| Transformadas (PC1) | 8 (2011-02 … 2022-08) | 4 (2012-05 … 2019-02) | 4 (2012-11 … 2018-08) | 3: 2013-05, 2017-11, 2018-02 | `06_epca_transiciones_ventanas.csv` · filas 1–8, 9–12, 13–16, 17–19 |

- **Interpretación:** el número y las fechas de las transiciones cambian con el ancho. Sin
  transformar, 2017-10 solo aparece con 60 meses. En las transformadas, 2017-11 aparece con 36 y
  60 meses. En las dos vías hay un candidato en 2018 con 36, 48 y 60 meses.
- **Dudas abiertas:**
  1. La lectura de 2017-10 (decisión D13) exige al menos dos anchos **y** los dos esquemas de pesos. La
     regla del 06 no tiene pesos: ¿se aplica la decisión D13 con `aede` como segundo método, o la regla del 06
     queda fuera de esa condición?
  2. La regla marca transición con un umbral relativo (media − 1 DE) y produce transiciones con
     cualquier ancho. Hace falta el nulo (decisión D10) para leerlas.

### 4.5 D8 · HFC en 3 y 4 clases (`07c`, bloque `b3b-hfc`)

| Resultado | Cifra | Origen |
|---|---|---|
| Sin transformar, 3 clases | C1: 12 series de escala (créditos, M1–M3, TAMN, IPC, tipo de cambio, PBI, demanda interna, reservas), representante crédito hipotecario; C2: tasa de referencia, interbancaria y TIPMN, representante la interbancaria; C3: índice BVL y EMBIG, representante el EMBIG | NIV `R_hfc_clases3.csv` · filas 1–17 · `clase`, `serie`, `representante` |
| Sin transformar, 4 clases | C3 se divide en índice BVL y EMBIG | NIV ídem · filas 18–34 |
| Transformadas, 3 clases | C1: crédito empresarial, M1–M3, TAMN, tipo de cambio, índice BVL, EMBIG y reservas (representante M2); C2: créditos de consumo e hipotecario, tasa de referencia, interbancaria, TIPMN e IPC (representante la interbancaria); C3: PBI y demanda interna (representante el PBI) | TRA ídem · filas 1–17 |
| Transformadas, 4 clases | De C1 sale una clase con tipo de cambio, índice BVL y EMBIG | TRA ídem · filas 18–34 |
| Correlación entre factores C1–C3, sin transformar | −0,486 (p5–p95: −0,647 a −0,187); sin tendencia: 0,116 (−0,170 a 0,353) | NIV `R_hfc_correlaciones3.csv` · filas 2 y 8 · `r`, `p5`, `p95` |
| Correlación entre factores C1–C2, sin transformar, sin tendencia | −0,490 (−0,713 a −0,077) | NIV ídem · fila 7 |
| Correlaciones entre factores, transformadas | −0,235, 0,217 y 0,138 | TRA ídem · filas 1–3 · `r` |
| Rand ajustado con la partición original, mediana (3 / 4 clases) | Sin transformar: 1,00 / 1,00 (p5: 0,81 / 0,52); transformadas: 0,45 / 0,46 | NIV y TRA `R_hfc_bootstrap.csv` · columnas `ari_3`, `ari_4` (500 filas) |
| Réplicas que reproducen la partición exacta (Rand ajustado = 1) | Sin transformar: 79,8 % (3 clases) y 63,6 % (4); transformadas: 0,6 % y 0,6 % | ídem |
| Correlación cofenética con la jerarquía original, mediana | 0,993 sin transformar; 0,599 transformadas | ídem · `cofenetica` |
| Pares con coclasificación entre 0,1 y 0,9 (de 136), 3 clases | 13 sin transformar; 80 transformadas | `R_hfc_coclasificacion.csv` · `frec_3` |

- **Interpretación:** sin transformar, la partición en 3 clases es casi la misma en todas las
  réplicas. En las transformadas, las clases se recomponen en casi todas las réplicas, y la
  jerarquía conserva menos de dos tercios de su estructura cofenética.
- **Dudas abiertas:**
  1. Sin transformar, la estabilidad puede venir de la tendencia común. El bootstrap por bloques
     no la rompe (supuesto de dependencia débil, ya declarado). Sería más informativo un bootstrap
     de la HFC sobre las series sin tendencia (no está en el plan).
  2. «Serie representante» es una definición mía: la de mayor |r| con el factor de la clase
     (§6, desviación 6). ¿Coincide con la del asesor?
  3. Los intervalos son de la correlación entre series **fijas** con las filas remuestreadas; no
     incluyen la incertidumbre de la propia partición.
  4. El signo de los factores sigue la regla de `clahfac`: el factor C1–C2 sin transformar
     correlaciona −0,079 y sus representantes +0,076 (filas 1 y 4). El signo de una correlación
     entre factores no se interpreta sin fijar esa orientación.

### 4.6 D7 · Nulo de estructura constante (`07b`, `R/07b_nulo_estructura.R`)

**Diseño ejecutado.** Remuestreo por bloques conjunto, con 200 réplicas sorteadas por longitud
de bloque (L = 12, 24 y 36; semilla 2026 antes de cada L). En las transformadas se remuestrean
filas; sin transformar, incrementos que luego se acumulan desde 0.
- **Python** calcula 200 réplicas con L = 24 y 20 con L = 12 y con L = 36.
- **R** calcula las 20 primeras de cada L, más la serie observada (réplica 0).
- **Medidas:** k* de los 3 criterios con maxcl = 20 y perfil RV entre ventanas adyacentes no
  solapadas (cargas 17 × 3), para 4 anchos × 2 pesos × 2 vías.
- **Comprobación:** la réplica 0 reproduce los k* de `06c_aede_cortes.csv` con maxcl = 20 (`assert`
  y `stopifnot`).

Origen de la posición de cada k* observado: `07b_nulo_estructura_kstar_posicion.csv`, filas 25–48
(L = 24, 200 réplicas). Las filas 1–24 son L = 12 y las 49–72, L = 36, ambas con 20 réplicas.

| Resultado (L = 24, 200 réplicas) | Sin transformar | Transformadas | Origen |
|---|---|---|---|
| Réplicas nulas en que el CH con k gl elige el tope (k = 20) | 90 % a 100 % según nw y pesos | 80 % a 100 % | `…_kstar_posicion.csv` · filas 26, 29, 32, …, 47 · `prop_nulo_en_tope` |
| Ídem, CH con k − 1 gl | 71 % a 98,5 % | 59 % a 99 % | ídem · filas 27, 30, …, 48 |
| Codo por caída máxima: nunca en el tope en el nulo | 0 % | 0 % | ídem · `prop_nulo_en_tope` |
| Codo observado con nw = 24 y su posición | k = 6; P(k nulo ≥ 6) = 0,24 (uniformes) y 0,27 (gaussianos) | k = 4 y 10; P(k nulo ≥ 10) = 0,05 (gaussianos) | NIV filas 25 y 28; TRA filas 25 y 28 · `k_obs`, `prop_nulo_ge_obs` |
| CH con k − 1 gl observado = 2 (nw 36, 48 y 60 uniformes; nw 48 gaussianos), sin transformar | P(k nulo ≤ 2) = 0,060; 0,040; 0,015; 0,025 | — | NIV filas 33, 39, 45, 42 · `prop_nulo_le_obs` |
| p5 del RV nulo agrupado (nw 24 / 36 / 48 / 60, uniformes) | 0,105 / 0,119 / 0,145 / 0,174 | 0,311 / 0,404 / 0,470 / 0,520 | `07b_nulo_estructura_rv_nulo.csv` · filas 10, 12, 14, 16 · `p05` |
| p5 del RV observado entre ventanas adyacentes (ídem) | 0,113 / 0,071 / 0,137 / 0,305 | 0,315 / 0,459 / 0,471 / 0,499 | `07b_nulo_estructura_rv_resumen.csv` · filas con `replica = 0` y pesos uniformes · `rv_p05` |

- **Interpretación (insumo para las tareas D10 y D11 del plan, sin conclusión):** bajo una estructura constante, el CH
  con k gl elige el tope en al menos el 80 % de las réplicas en las dos vías. Que el CH observado
  esté en el tope no distingue los datos del nulo, y eso respalda el criterio de la decisión D11 de no usarlo
  como selector. El codo por caída máxima nunca elige el tope en el nulo.
- **Dudas abiertas:**
  1. **Lectura del RV (decisión D10).** El plan habla del «perfil del RV entre ventanas adyacentes no
     solapadas». Lo implementé como el RV entre las **cargas de `aede`** (17 series × 3
     dimensiones, d = 3 por la decisión D9) de las ventanas que empiezan en i y en i + nw: es la lectura más
     literal con las salidas de `aede` (§6, desviación 10). Otra lectura posible es el RV entre las
     matrices de correlación completas. ¿Cuál quiere el plan?
  2. **Nivel del p5.** El p5 del RV nulo se calcula sobre todos los pares de todas las réplicas,
     agrupados por ancho y pesos. La tarea D10 compara la proporción de pares observados bajo ese p5. ¿Se
     prefiere un p5 por posición? Los extremos de la muestra tienen menos pares solapados.
  3. **Nulo en niveles.** En niveles, el RV nulo y el observado son bajos y de magnitud parecida
     (p5 nulo de 0,105 a 0,174), salvo con nw = 60, donde el observado es mayor. Al acumular
     incrementos remuestreados, cada réplica conserva la deriva de cada serie, y no está claro qué
     parte del RV se debe a ella. Conviene contrastarlo con el nulo mixto (tarea D11 del plan,
     decisión D8).
  4. Los k* de las transformadas con nw = 24 y pesos gaussianos (codo, k = 10) quedan en el
     extremo del nulo (P = 0,05). Es una sola combinación entre 48: el problema de comparaciones
     múltiples (riesgo 1 del plan) hay que tratarlo en la fase 1.

## 5. Paridad Python–R

Render final del Rmd (después del guion del nulo y de todos los notebooks): exit 0, sin `Warning`
ni `Error` en el registro ni en el HTML. Ídem con `version_asesor = TRUE`, renderizado al
scratchpad: exit 0 y 0 bloques `class="pregunta"`, frente a 32 en la versión normal.

- **89 de 89 comprobaciones coinciden:** 48 en NIV `R_paridad_python.csv` y 41 en TRA. Las 49 de 3a
  no cambian; hay **40 nuevas**, 20 por vía.
- **Tablas discretas** (k, cortes, clases, conteos, fechas): 0 filas distintas. Los criterios de
  las filas nuevas son: D3, grilla de la datación y estabilidad de cortes; D4, grilla de `aede`;
  D5, λ por ventana, n de Kish, conteos de Kaiser y de Horn, cruces; D6, transiciones y
  estabilidad por ancho; D8, clases, r con el factor, correlaciones, bootstrap y coclasificación;
  D7, k*, perfiles RV, resúmenes y la excepción declarada.
- **Cifras:** la diferencia máxima entre las filas nuevas es 3,3e-14 (perfil RV del nulo, vía
  transformada).
- **Excepción declarada en la propia tabla:** las réplicas 21 a 200 del nulo con L = 24 solo se
  calculan en Python. La fila comprueba que estén las 200.
- **Umbrales de Horn:** ya no hacen falta como excepción (§6, desviación 4).
- **En sentido inverso,** cada notebook nuevo compara sus salidas con los `R_*` y falla si
  difieren: 09a, 06c, 06 (con 60 meses frente a sus propios archivos), 07c y 07b.

**No regresión** (criterio 3 del plan):

- **D4:** las filas `nw = 60, maxcl = 10` de `R_aede_cortes.csv` son las de 3a (`stopifnot`).
- **D6:** con 60 meses se reproducen `06_epca_transiciones_*`, que no cambian.
- **D3:** el 09a con maxcl = 10 reproduce `09_regimenes_pca.csv` en las dos vías.
- **Demás CSV de 3a:** de los 116 archivos de `data/results/` de la línea base, solo cambian
  `R_aede_cortes.csv` (formato largo, D4) y `R_paridad_python.csv` (filas nuevas), en las dos
  vías. Los otros 112 quedan idénticos byte a byte (md5).
- **Re-ejecuciones:** `999_port_camiz` da salidas idénticas. Re-ejecuté `05_pca.ipynb` con nbconvert
  (exit 0, CSV idénticos) y restauré el notebook versionado, porque solo cambiaban los metadatos de
  ejecución.
- **`pytest tests/`:** 23 pruebas aprobadas.
- **Determinismo:** dos corridas del 07b dan CSV idénticos (md5).

## 6. Desviaciones respecto del plan, de `decisiones.qmd` o del marco

1. **D6: archivos nuevos en lugar de reescribir `06_epca_transiciones_*`.** El plan pide salidas en
   formato largo `06_epca_transiciones_*` con la columna `ventana`, y que con 60 meses se
   reproduzcan los archivos actuales. Los dos archivos actuales los lee el notebook 08, que no
   puede volver a ejecutarse sin `torch`. Por eso los dejé intactos (byte a byte) y escribí el
   formato largo en `06_epca_transiciones_ventanas{,_niveles}.csv`, cuyas filas con
   `ventana = 60` son las actuales. En cambio, `R_aede_cortes.csv` sí pasa a formato largo, como
   pide D4 de forma explícita. Para que `999_port_camiz` siguiera funcionando, filtra las filas de
   3a; sus salidas no cambian.
2. **D3: sin la columna `episodios_contenidos`.** Esa columna lee las fechas de episodios escritas
   a mano, que la tarea D9 (fase 1) reemplazará por el archivo único de la decisión D7. No copié fechas de episodios en
   el código nuevo (criterio 7).
3. **D3: lectura de «codo» y «regla K».** El plan lista cuatro criterios: codo, CH con k, CH con
   k − 1 y regla K. Como la regla K de la decisión D12 es exactamente el `k_codo` de `datar` (umbral y, si no,
   caída máxima), leí «codo» como el codo por caída máxima solo, que es el criterio de `aede`.
   `k_en_tope` compara con el mayor k factible (`k_max_efectivo`), no con maxcl, porque con
   segmentos de 12 meses k = 19 y 20 no son factibles.
4. **D5: umbral de Horn compartido en lugar de la excepción de generadores.** El plan pide comparar
   el número de ventanas bajo el umbral. Con los umbrales de cada generador, esos conteos
   difirieron en 3 de 24 filas sin transformar y en 10 de 24 transformadas: muchas ventanas quedan
   a menos de la diferencia entre umbrales, que llega a 0,035. Por eso el Rmd escribe sus umbrales
   (`R_aede_horn_umbrales.csv`) y Python cuenta con ellos, como con los índices compartidos de 3a.
   El umbral de numpy y su conteo quedan en `06c_aede_valores_propios_resumen.csv`
   (`horn_p95_numpy`, `bajo_horn_numpy`). La paridad de los conteos es exacta.
5. **D5: definiciones operativas mías.**
   - *Empates con Kaiser:* con nw = 24, la tasa de referencia es constante en 7 ventanas sin
     transformar y en 6 transformadas (centros de ventana entre 2012-05 y 2012-11). `aede` la deja aislada y un valor propio
     vale 1 salvo redondeo; el último bit difiere entre R y Python. Por eso «bajo Kaiser» es
     λ < 1 − 10⁻⁹, y las ventanas a menos de 10⁻⁹ de 1 se cuentan aparte (`en_umbral_kaiser`).
   - *Techo de $n_\omega$:* $\lceil n_\omega - 10^{-9} \rceil$, para que el redondeo no convierta
     $n_\omega = n_w$ en $n_w + 1$.
   - *Cruce λ2 ↔ λ3:* el eje 2 de la ventana i es más congruente (|Tucker|) con el eje 3 de la
     ventana i − 1 que con su eje 2.
   - *Horn:* 1 000 simulaciones, semilla del documento.
6. **D8: definiciones operativas mías.**
   - Particiones con `.partclas_ac`: el Rmd comprueba que son las mismas de `clahpart_r`.
   - Clases nombradas C1, C2, … por el orden de su primera serie.
   - Representante: la serie con mayor |r| con el factor de la clase.
   - Intervalos bootstrap de la correlación con las series fijas.
   - Sin tendencia, en niveles: la recta se quita a los factores y a los representantes ya
     calculados.
   - 500 réplicas: todas las de `R_bootstrap_indices_L24.csv`.
   - Las matrices 3 × 3 se calculan solo para la partición en 3 clases, como dice el plan; para
     4 clases se dan la composición, el factor y el representante.
7. **D6: columna constante con nw = 24.** El Rmd replica la convención de `StandardScaler`
   (la columna queda en 0), que es la del notebook 06. Con nw ≥ 36 no hay columnas constantes.
8. **Paridad de tablas discretas.** Agregué `fila_tabla` al anexo: compara fila a fila como texto,
   y `dif_max` es el número de filas distintas. Además, `fila_tabla` marca «columnas ausentes» si el
   CSV de Python es de una versión anterior; antes, en ese caso, el render se detenía.
9. **Vectorización de `fisher_multivariado`.** El bucle interno usa las mismas operaciones
   elemento a elemento. Las pruebas contra la fuerza bruta y la paridad (cortes idénticos, SCE a
   ≤ 1e-12) lo confirman.
10. **D7: lectura del RV entre ventanas adyacentes no solapadas.**
    - Ventana i frente a la ventana i + nw, con paso de un mes: hay wn − nw pares por ancho.
    - RV (`coef_rv` del Rmd y de `src/multivariado.py`, con columnas centradas) entre las cargas
      de `aede` (`correlationlsq`, 17 × 3).
    - Fechas: el centro de cada una de las dos ventanas (`fecha_a`, `fecha_b`).
    - La alternativa (RV entre las matrices de correlación completas) no se calculó.
11. **D7: implementación y salidas.**
    - **Guion R aparte.** El cálculo en R está en `R/07b_nulo_estructura.R` y no dentro del render,
      porque dura unos 26 min y superaría el umbral de unos 15 min del riesgo 9 del plan. El Rmd
      lee sus CSV, comprueba la réplica 0 y agrega las filas de paridad. No reduje réplicas: 200
      sorteadas por L, 20 calculadas en R para cada L y 200 en Python con L = 24.
    - **Índices.** Un archivo por L, `R_nulo_estructura_indices_L{12,24,36}.csv`, en lugar del
      `R_nulo_estructura_indices.csv` único del plan («nombres por confirmar»). Las dos vías usan
      los mismos inicios, porque las dos remuestrean 227 filas.
    - **Sensibilidad L = 12 y L = 36.** Incluida (riesgo 2 del plan), con 20 réplicas en las dos
      lenguas.
    - **Nulo en niveles.** Versión «con deriva»: los incrementos se remuestrean tal cual. El plan
      dice «como en `nulo_tendencias`», cuya versión base es esa.
    - **Archivos de Python que el plan no nombraba:** `07b_nulo_estructura_kstar_posicion.csv`
      (criterio 6: posición de cada k* observado en el nulo) y `07b_nulo_estructura_rv_nulo.csv`
      (cuantiles agrupados del RV nulo).
12. **Numeración de notebooks.** `06c_aede_grilla` (el plan lo proponía), `07b_nulo_estructura` (el
    plan lo proponía «por confirmar») y `07c_hfc_clases`. El 07c no lo nombraba el plan: lo numeré
    junto al 07, porque la HFC es, como el PCA de Rcamiz, un método del asesor.

## 7. Qué queda para la fase 1 y para Roberto

**Fase 1 (no ejecutada en esta sesión).** D9 (episodios unificados), D10 (criterio de OE4 y
2017-10), D11 (nulo mixto) y D12 (sensibilidad de la dimensión, cifras y nota). Las decisiones que
las bloqueaban ya están registradas (D7 a D14 de `decisiones.qmd`, 24-oct). La fase 0 deja listos
sus insumos:

- **Tarea D10:** perfiles RV observados y nulos, en `07b_nulo_estructura_rv*.csv`. Las
  transiciones por ancho están en `06_epca_transiciones_ventanas*` y `R_aede_cortes.csv`.
- **Tarea D12:** `src/particion.datar` y `grilla_datacion` ya admiten otra dimensión; basta pasar
  scores con d = 2 o 4.

**Decisiones o confirmaciones que solo Roberto puede dar** (ninguna bloquea lo hecho):

1. **maxcl de la regla K.** Sin transformar, la datación principal da 6 regímenes con maxcl = 10 y
   11 con maxcl = 15 o 20 (§4.1, duda 1). Ningún documento fija el maxcl de la especificación
   principal.
2. **RV entre ventanas.** ¿Cargas 17 × 3 (lo implementado) o matrices de correlación completas?
   ¿p5 agrupado o por posición? (§4.6, dudas 1 y 2.)
3. **Definiciones operativas** de la serie representante (HFC) y del cruce λ2 ↔ λ3 (§6,
   desviaciones 5 y 6).
4. **Decisión D13 y la regla del 06**, que no tiene pesos (§4.4, duda 1).
5. **maxcl = 20 con segmentos de 12 meses.** Fuerza tramos de exactamente 12 meses cerca del tope y
   deforma el codo (§4.1, duda 2). ¿Se acota maxcl en la datación?

**Para el Dr. Camiz (decisión J / D11 de `decisiones.qmd`):** bajo un nulo de estructura
constante, el CH de `aede` con k gl elige el tope en al menos el 80 % de las réplicas
(§4.6). Es un insumo para la pregunta, que se le hace sin corregirlo, de si el k de `aede` es
deliberado.

**Para el auditor.** Convención de fechado de `def:ventana` con nw = 24: la primera ventana
(filas 1 a 24) se fecha en la fila 13, i + nw/2. Lo comprueba `tests/test_camiz_port.py`
(`test_aede_anchos_cortos_contra_R`); en NIV `R_aede_valores_propios.csv`, la primera fila con
`nw = 24` tiene fecha 2008-01.
