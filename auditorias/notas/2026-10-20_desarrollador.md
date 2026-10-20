# Nota del desarrollador · 20 de octubre de 2026 · Iteración 3a (línea principal)

**Encargo:** sección 7 del plan `asesoria/2026-10-20_plan-iteracion-3.md`, «Desarrollador», con los
apuntes 1, 3, 4, 5 (parte estática), 10 y 11. Decisiones D4, D5 y D6 de `decisiones.qmd`. Rama
`iteracion-3a`, sin commit ni push.

**Cambios del orquestador respecto del plan:** `aede` y la HFC se portan a Python en paralelo
(otro desarrollador, `src/camiz_port.py` y `notebooks/999_port_camiz.ipynb`): no toco esos
archivos. No modifico `notebooks/modelos_dl.py`.

> Nota cerrada tras el render final (hubo un reinicio del límite de uso; verifiqué con `git status` que ningún archivo se perdió).

## 0. Bitácora

1. **Rama de archivo trimestral verificada.** `origin/archivo/v0.3-trimestral` apunta a `ff52c5e`
   y contiene `notebooks/05_pca.ipynb` y los cinco `data/results/05_pca_*.csv` trimestrales. Entre
   `ff52c5e` y `HEAD` no cambió ninguno de ellos (`git diff --stat ff52c5e HEAD -- data/results
   notebooks/05_pca.ipynb` vacío). El tag `v0.3-trimestral` no existe (el proxy bloquea los tags).
2. `statsmodels` 0.15.0 instalado (`pip install --break-system-packages statsmodels`). En R:
   tseries 0.10.55, urca 1.3.3, psych 2.4.1, rmarkdown 2.25.
3. **Render de línea base** del Rmd sin cambios (copia en el scratchpad): exit 0, 2 min 43 s, sin
   avisos; no modificó ningún `R_*` versionado. Proporciones del nulo en el HTML: con deriva
   0,90 / 0,01 / 0,21 / 0,93; sin deriva 0,00 / 0,59 / 0,95 / 0,02 (PC1, PC2, PC3, |r| medio).

## 1. Especificación de la regla D5, fijada antes de calcular

Escrita el 20-10-2026 **antes** de ejecutar ninguna prueba ADF/KPSS sobre residuos; queda igual
en `src/series_tiempo.py` (constantes `ADF_REZAGOS`, `KPSS_REZAGOS`, `ALFA_D5`) y en el bloque
`funciones` del Rmd. No se ajustó después de ver los resultados.

- **Regresión:** $x_t = a + b\,t + e_t$ por MCO, con $t = 1, \dots, n$ (mes 1 = primer mes de la vía).
- **ADF** sobre $e_t$: forma de `tseries::adf.test`, con constante y tendencia en la regresión
  auxiliar y **6 rezagos fijos** de $\Delta e_t$ ($k = \lfloor (n-1)^{1/3} \rfloor = 6$ para
  $n = 228$ y $n = 227$; se fija el entero, no la fórmula). Como $e_t$ es $x_t$ menos una recta, el
  estadístico es idéntico al de la ADF con constante y tendencia sobre $x_t$ (lo compruebo con un
  `assert`), y por eso corresponden los valores críticos del caso con tendencia.
- **KPSS** sobre $e_t$: hipótesis nula de estacionariedad en tendencia (`null = "Trend"`), núcleo
  de Bartlett con **4 rezagos fijos** ($\lfloor 4 (n/100)^{1/4} \rfloor = 4$). También es idéntico
  al KPSS en tendencia sobre $x_t$.
- **Decisión al 5 %:** con los p-valores interpolados en las tablas de `tseries` (las mismas en
  Python, que replica la interpolación de `tseries::adf.test` y `kpss.test`), de modo que la
  clasificación no depende de la lengua. ADF rechaza si $p_{\text{ADF}} < 0{,}05$; KPSS rechaza si
  $p_{\text{KPSS}} < 0{,}05$. Se informan también los p-valores de MacKinnon de `statsmodels`, solo
  como referencia.
- **Clases (D5):** ADF rechaza y KPSS no → **TS**; ADF no rechaza y KPSS rechaza → **DS**; otro
  caso → **indeterminada**.
- **Complementos, no entran en la regla:** ACF de los residuos en los rezagos 1 y 12 y Ljung-Box
  con 12 rezagos (sin corrección de grados de libertad).
- Los estadísticos t de la pendiente no se interpretan: con residuos integrados la regresión es
  espuria (Granger y Newbold, 1974; Phillips, 1986 [VERIFICAR: sin ficha]).

## 2. Archivos creados o modificados

**Código**

| Archivo | Estado | Contenido |
|---|---|---|
| `src/multivariado.py` | nuevo | estandarización (divisor n), PCA con la regla de signo de Rcamiz, cos², contribuciones, Horn, vara quebrada, Tucker, emparejamiento de componentes, RV, Procrustes, KMO, Bartlett, número de condición, ln\|R\| |
| `src/remuestreo.py` | nuevo | índices desde inicios de bloque, lectura de los índices del Rmd, bootstrap del PCA, nulo de tendencias independientes |
| `src/series_tiempo.py` | nuevo (no estaba en el plan) | ACF como `stats::acf`, $n_{\text{ef}}$, prueba t de r, ADF/KPSS con p-valores de `tseries`, regla D5, residuos sin tendencia |
| `notebooks/05_pca.ipynb` | reescrito | PCA estático mensual en dos vías (antes trimestral) |
| `R/tesis_ciclo_financiero.Rmd` | modificado | ver §2.1 |
| `herramientas/generar_cifras.py`, `herramientas/cifras_mapa.csv`, `herramientas/README.md` | nuevos | generador de cifras, mapa versionado y documentación |
| `tesis_latex/cifras.tex`, `tesis/_cifras.yml` | generados | 54 cifras; no toqué ningún otro archivo de `tesis_latex/` ni de `tesis/` |

No creé `src/particion.py`: el 05 no usa la partición de Fisher (es del 09a, iteración 3b), y el
port de `aede` y la HFC lo hace otro desarrollador (D6). No toqué `src/camiz_port.py`,
`notebooks/999_port_camiz.ipynb` ni `notebooks/modelos_dl.py`.

**Salidas del 05** (vía en niveles en `data/results/niveles/`, vía transformada en `data/results/`):
`05_acf`, `05_correlaciones`, `05_n_efectivo`, `05_n_efectivo_resumen`, `05_adecuacion`,
`05_pca_valores_propios`, `05_pca_retencion`, `05_pca_cargas`, `05_pca_contribuciones`,
`05_pca_scores`, `05_pca_cos2`, `05_bootstrap_congruencia`, `05_bootstrap_valores_propios`,
`05_bootstrap_cargas` y `05_pca_tendencia_componentes` en las dos vías; solo en niveles:
`05_correlaciones_sin_tendencia`, `05_tendencia_series`, `05_clasificacion_d5_resumen`,
`05_pca_contraste_tendencia`, `05_nulo_tendencias` y `05_nulo_simulaciones`; y
`data/results/05_dimensiones.csv`. Figuras: `05_correlaciones`, `05_pca_sedimentacion` y
`05_pca_residuos_tendencia` en `reports/figures/` y `reports/figures/niveles/` (más
`05_correlaciones_sin_tendencia` en niveles).

**Salidas nuevas del Rmd** (índices compartidos y cifras que antes solo estaban inline):
`R_bootstrap_indices_L{12,24,36}.csv` (inicios de bloque, 1-based, uno por réplica) en las dos
carpetas; `R_adecuacion`, `R_bootstrap_congruencia`, `R_bootstrap_valores_propios` y
`R_tendencia_componentes` en las dos; solo en niveles: `R_nulo_indices.csv`
(réplica × serie × 19 inicios), `R_nulo_tendencias`, `R_nulo_simulaciones`,
`R_pca_contraste_tendencia` y `R_tendencia_series`.

**Retirados (reemplazo de la versión trimestral, D3):** `data/results/05_pca_cargas_niveles.csv`,
`05_pca_cargas_transformado.csv`, `05_pca_comparacion.csv`, `05_pca_scores_niveles.csv`,
`05_pca_scores_transformado.csv` y `reports/figures/05_pca_{biplot,scree}_{niveles,transformado}.png`.
Ningún otro archivo los leía (búsqueda en todo el repositorio). Se recuperan de
`origin/archivo/v0.3-trimestral`.

### 2.1 Cambios en el Rmd

- **YAML:** parámetro `version_asesor` (FALSE por defecto). Con TRUE, un *hook* de knitr retira los
  bloques `::: {.pregunta}` del markdown antes de pandoc (no quedan ni en el HTML ni en su fuente).
- **C-01 cerrado:** el comentario «Nombres y unidades verificados contra la API del BCRP (consulta
  del 08/10/2026)» pasa a «Código BCRP, nombre y unidad de cada serie del dataset».
- **`funciones`:** `inicios_bloques` + `indices_desde_inicios` (el antiguo `indices_bloques` es su
  composición y consume el generador igual), `generar_inicios`, `bootstrap_pca`, `emparejar`,
  `quitar_tendencia`, `acf_rezagos`, `n_efectivo`, `p_correlacion`, `tabla_n_efectivo`,
  `adecuacion`, `clasificar_d5`, `tendencia_residuos`, `tabla_tendencia` y las constantes D5.
- **`b2-datos`:** `stopifnot` de 228 × 17, 227 × 17, fechas extremas y ausencia de faltantes.
- **Sección 2, `b2s-nulo`:** los inicios de bloque se sortean una vez (mismo orden de consumo del
  generador que antes) y los usan las dos versiones del nulo; antes se volvía a fijar la semilla,
  con el mismo resultado. Nueva versión «sin tendencia».
- **Sección 2, subsección nueva** «Diagnóstico: el PCA de las series sin su tendencia lineal»
  (apunte 10, chunk `b2s-sin-tendencia`).
- **A.2:** `b3-acf-nef` (apunte 3 y sensibilidad de Bartlett, apunte 4), `b3-cos2` (apunte 1),
  `b3-tendencia-d5` y `b3-g-residuos` (apunte 11), `b3-bootstrap` reescrito con `bootstrap_pca`
  y `b3-bootstrap-L` (apunte 5).
- **B.2:** los mismos bloques (`bB2-acf-nef`, cos² en `bB2-cargas-tabla`, D5 en `bB2-tiempo`,
  `bB2-g-residuos`, `bB2-bootstrap`, `bB2-bootstrap-L`).
- **Anexo:** 30 filas nuevas de paridad frente a los CSV del 05 y escritura de los `R_*` nuevos.
  Las diferencias son relativas, $|R - Py| / \max(1, |Py|)$: absolutas para magnitudes ≤ 1 y
  relativas para χ² y el número de condición (≈ 67 647 en niveles, donde la diferencia absoluta es
  3,7e-7 y la relativa 5e-12).

## 3. Comandos de ejecución (orden obligatorio)

El 05 lee los índices que sortea el Rmd, y la paridad del Rmd lee los CSV del 05. Desde la raíz:

```
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/05_pca.ipynb
Rscript -e "rmarkdown::render('R/tesis_ciclo_financiero.Rmd')"
python3 herramientas/generar_cifras.py
python3 herramientas/generar_cifras.py --comprobar
```

El primer render deja las filas del 05 como «archivo ausente» si el 05 nunca se ejecutó; el
segundo las completa. Registros en el scratchpad de la sesión (`3a_dev/render1.log`,
`nb05_3.log`, `render2.log`).

## 4. Resultados por apunte

Convención de origen: `archivo` · fila de datos (1 = primera fila tras el encabezado) y clave ·
columna. «NIV» = `data/results/niveles/`; «TRA» = `data/results/`.

### 4.0 Dimensiones

| Cifra | Valor | Origen |
|---|---|---|
| Meses, vía en niveles | 228 (2007-01 a 2025-12) | `05_dimensiones.csv` · fila 1 (`via=niveles`) · `n`, `fecha_inicio`, `fecha_fin` |
| Meses, vía transformada | 227 (2007-02 a 2025-12) | `05_dimensiones.csv` · fila 2 · `n`, `fecha_inicio`, `fecha_fin` |
| Series | 17 | `05_dimensiones.csv` · fila 1 · `p` |

Calendario continuo y sin faltantes en las dos vías (`assert` del 05 y `stopifnot` del Rmd); las
transformadas se reconstruyen desde los niveles con diferencia máxima 5,7e-14.

### 4.1 Apunte 3 · ACF, correlaciones y $n_{\text{ef}}$

| Cifra | Valor | Origen |
|---|---|---|
| ACF rezago 1, rango en niveles | 0,904 (EMBIG) a 0,993 (tipo de cambio) | NIV `05_acf.csv` · col. `acf_1` |
| ACF rezago 24, tasas de política e interbancaria (niveles) | −0,195 y −0,195 | NIV `05_acf.csv` · filas 7–8 · `acf_24` |
| ACF rezago 12, demanda interna (transformadas) | 0,580 | TRA `05_acf.csv` · fila 16 · `acf_12` |
| $n_{\text{ef}}$ mediana (mín.–máx.), niveles | 10,4 (5,0–35,8) de 228 | NIV `05_n_efectivo_resumen.csv` · fila 1 (`version=original`) · `n_ef_mediana`, `n_ef_min`, `n_ef_max` |
| Pares con r ≠ 0 al 5 %, niveles, con n / con $n_{\text{ef}}$ | 83,1 % / 44,9 % | ídem · `prop_signif_n`, `prop_signif_n_ef` |
| Ídem, niveles sin tendencia lineal | 75,7 % / 27,9 %; $n_{\text{ef}}$ mediana 15,6 | NIV `05_n_efectivo_resumen.csv` · fila 2 (`version=sin_tendencia`) |
| $n_{\text{ef}}$ mediana (mín.–máx.), transformadas | 182,0 (39,0–227) de 227 | TRA `05_n_efectivo_resumen.csv` · fila 1 |
| Pares con r ≠ 0 al 5 %, transformadas, con n / con $n_{\text{ef}}$ | 47,1 % / 41,9 % | ídem |

$n_{\text{ef}} \le n$ en los 136 pares de cada versión (`assert`); ningún par tiene $n_{\text{ef}} \le 3$.

- **Interpretación:** en niveles, cada correlación se apoya en unos 10 meses de información
  independiente de 228. Con esa corrección, más de la mitad de las correlaciones deja de ser
  distinguible de cero. En las transformadas, la corrección es pequeña.
- **Dudas abiertas:** (i) la fórmula de $n_{\text{ef}}$ (truncamiento en $J = \lfloor n/5 \rfloor$ y
  ponderación $(n-j)/n$) está marcada `[VERIFICAR]` y no tiene fuente fichada; la elección de $J$
  cambia la cifra, y conviene fijarla con la fuente que entregue el bibliotecario. (ii) Con series
  integradas, la ACF muestral está sesgada hacia abajo en muestras finitas, de modo que
  $n_{\text{ef}}$ en niveles podría ser aún menor. (iii) ¿Se informa $n_{\text{ef}}$ por par o un
  resumen?

### 4.2 Apunte 4 · KMO y Bartlett

| Cifra | Niveles | Transformadas | Origen (`05_adecuacion.csv`, `ambito=global`) |
|---|---|---|---|
| KMO global | 0,862 | 0,695 | fila 8 (`medida=kmo_global`) · `valor` |
| χ² de Bartlett con n (136 gl) | 12 210 | 1 831 | fila 3 (`bartlett_chi2_n`) y fila 4 (`bartlett_gl`) |
| Mediana de $n_{\text{ef}}$ usada | 10,4 | 182,0 | fila 2 (`n_ef_mediana`) |
| χ² de Bartlett con la mediana de $n_{\text{ef}}$ | 162,5 (p = 0,060) | 1 455,6 (p < 0,001) | filas 6–7 (`bartlett_chi2_nef`, `bartlett_p_nef`) |
| Número de condición de R | 67 647 | 68,1 | fila 9 (`num_condicion`) |
| ln\|R\| | −55,37 | −8,34 | fila 10 (`log_det`) |

Reproducen las cifras del HTML de la iteración 2 (χ² 12 210 y 1 831; KMO 0,86 y 0,70).

- **Interpretación:** con $n$, Bartlett rechaza la esfericidad en las dos vías. En niveles, si se
  usa la mediana de $n_{\text{ef}}$, el rechazo deja de ser claro al 5 % (p = 0,06): la evidencia de
  estructura común en niveles depende casi por completo de tratar los 228 meses como
  independientes. El número de condición de niveles (≈ 6,8 · 10⁴) indica pares casi colineales.
- **Dudas abiertas:** (i) usar un único $n_{\text{ef}}$ (la mediana de los pares) en Bartlett es una
  convención mía, no una prueba con fuente: hay que declararla así o buscar una versión de la
  prueba para series dependientes. (ii) ¿Qué pares sostienen el número de condición (M2–M3, tasa de
  referencia–interbancaria)? No lo descompuse.

### 4.3 Apunte 1 · cos² por eje

Origen: NIV y TRA `05_pca_cos2.csv` (17 filas por vía; columnas `cos2_1`…`cos2_4`, `suma_1_3`,
`plano_1_2`, `plano_1_3`, `suma_total`, `kmo_individual`). `suma_total` = 1 en todas las series
(tolerancia 1e-12, `assert` en las dos lenguas).

**Niveles, una línea por eje:**

- **Eje 1 (67,2 %):** cos² ≥ 0,5 en 12 series: los tres créditos, M1, M2, M3, TAMN, IPC Lima, tipo
  de cambio, PBI, demanda interna y reservas.
- **Eje 2 (18,3 %):** cos² ≥ 0,5 en 3 series: tasa de referencia (0,96), interbancaria (0,96) y
  TIPMN (0,80).
- **Eje 3 (7,1 %):** cos² ≥ 0,5 solo en el EMBIG (0,65). El índice BVL reparte su varianza entre
  los ejes 1 y 3 (0,38 y 0,38).
- **Calidad baja en el plano 1–2 (cos² < 0,5):** índice BVL (0,41; KMO 0,81) y EMBIG (0,21; KMO
  0,59, el menor de la vía). Las dos se recuperan en el plano 1–3 (0,76 y 0,76).
- **Cruce con el KMO:** de las cuatro series con menor KMO (EMBIG 0,59, tasa de referencia 0,61,
  interbancaria 0,63 y TIPMN 0,74), solo el EMBIG está además mal representado en el plano 1–2. Las
  tres tasas tienen KMO bajo, pero cos² de 0,89 a 0,97 en ese plano.

**Transformadas:**

- **Eje 1 (23,3 %):** cos² ≥ 0,5 solo en M2 (0,65) y M3 (0,57).
- **Ejes 2 y 3:** ninguna serie llega a 0,5; la mayor en el eje 2 es la tasa de referencia (0,48) y,
  en el eje 3, el crédito empresarial (0,46).
- **Calidad < 0,5 en el plano 1–2:** 12 de 17 series. Las cinco con menor KMO (PBI 0,46, tipo de
  cambio 0,56, crédito empresarial 0,58, hipotecario 0,63 y demanda interna 0,65) están todas en
  ese grupo, con calidad de 0,02 a 0,21.

- **Interpretación:** en niveles, los dos primeros ejes representan bien 15 de las 17 series. El
  riesgo y la bolsa, en cambio, solo se leen en el eje 3. En las transformadas, ningún plano
  representa bien a la mayoría de las series. Ahí sí, las series con menor adecuación son las peor
  representadas.
- **Dudas abiertas:** (i) en niveles, el KMO bajo de las tasas convive con una representación
  excelente: ¿es porque forman un bloque casi colineal entre sí, que la anti-imagen penaliza? (ii)
  ¿El umbral de 0,5 es el que espera el Dr. Camiz, o prefiere la suma sobre los ejes retenidos?

### 4.4 Apunte 5 · Bootstrap por bloques (parte estática)

500 réplicas por longitud de bloque L ∈ {12, 24, 36}, con la semilla 2026 del Rmd fijada antes de
cada longitud. Los inicios de bloque están en `R_bootstrap_indices_L{12,24,36}.csv`. Con L = 24 se
reproducen exactamente las cifras de la iteración 2: congruencias medianas de 0,984, 0,962, 0,950 y
0,849, y p5 de 0,793 en el PC2 y de 0,608 en el PC4 (HTML de la línea base).

**Congruencia de Tucker con la componente original** (`05_bootstrap_congruencia.csv`, columnas
`mediana` y `p5`; filas 1–4 para L = 12, 5–8 para L = 24 y 9–12 para L = 36):

| Vía | Componente | L = 12 mediana / p5 | L = 24 mediana / p5 | L = 36 mediana / p5 |
|---|---|---|---|---|
| Niveles | PC1 | 0,991 / 0,944 | 0,984 / 0,934 | 0,980 / 0,918 |
| Niveles | PC2 | 0,977 / 0,867 | 0,962 / 0,793 | 0,956 / 0,716 |
| Niveles | PC3 | 0,961 / 0,855 | 0,950 / 0,799 | 0,948 / 0,759 |
| Niveles | PC4 | 0,910 / 0,657 | 0,849 / 0,608 | 0,798 / 0,502 |
| Transformadas | PC1 | 0,976 / 0,848 | 0,978 / 0,907 | 0,976 / 0,883 |
| Transformadas | PC2 | 0,935 / 0,755 | 0,941 / 0,754 | 0,935 / 0,771 |
| Transformadas | PC3 | 0,910 / 0,707 | 0,927 / 0,711 | 0,901 / 0,660 |
| Transformadas | PC4 | 0,824 / 0,542 | 0,834 / 0,484 | 0,773 / 0,498 |

**Valores propios ordenados** (`05_bootstrap_valores_propios.csv`; columnas `p5`, `p95`,
`prop_mayor_1` y `brecha_siguiente_p5`, que es el p5 de λk − λk+1):

- **Niveles:** λ3 tiene p5–p95 de 0,93–1,49 (L = 12), 0,91–1,57 (L = 24) y 0,96–1,74 (L = 36), y es
  mayor que 1 en el 89 %, el 89 % y el 94 % de las réplicas. λ4 no supera 1 en ninguna réplica con
  L = 12 o 24 (0,6 % con L = 36). La brecha λ3 − λ4 tiene un p5 de 0,43 a 0,45; la brecha λ2 − λ3,
  de 0,45 a 0,77.
- **Transformadas:** λ1 a λ4 superan 1 en el 100 % de las réplicas con las tres longitudes, y λ5,
  en el 97 % al 98 %. La brecha λ4 − λ5 tiene un p5 de 0,06 a 0,11.

- **Interpretación:** en niveles, PC1 a PC3 son estables con las tres longitudes. La estabilidad
  de PC2 y PC3 baja al alargar el bloque (p5 de 0,867 a 0,716 en el PC2), y PC4 no es estable. Los
  intervalos separan tres valores propios del resto. En las transformadas, PC4 es el menos estable, y
  λ4 y λ5 no se separan con claridad.
- **Supuesto (declarado en el Rmd y en el 05):** el bootstrap por bloques supone dependencia débil.
  Las series en niveles no la cumplen (§4.5), así que en esa vía estas cifras miden estabilidad
  descriptiva, no incertidumbre muestral.
- **Dudas abiertas:** (i) el criterio para elegir entre 2, 3 y 4 dimensiones (OE6) con estos
  intervalos no está fijado. Un candidato es la separación de λk y λk+1 (p5 de la brecha > 0), pero
  hay que registrarlo antes de usarlo, como se hizo con D5. (ii) ¿Por qué la congruencia del PC2 en
  niveles cae al alargar el bloque? Una hipótesis por verificar: los bloques largos repiten pocos
  tramos de la tendencia y desplazan su peso entre ejes.

### 4.5 Apunte 11 · Regresión sobre el tiempo y residuos (regla D5)

Origen: NIV y TRA `05_pca_tendencia_componentes.csv` (filas 1–4 = PC1–PC4) y NIV
`05_tendencia_series.csv` (17 filas); columnas `pendiente`, `r2`, `r_tiempo`, `acf1_residuos`,
`acf12_residuos`, `ljung_box_q12`, `adf_estadistico`, `adf_p_tseries`, `kpss_estadistico`,
`kpss_p_tseries` y `clase_d5`. Resumen de conteos: NIV `05_clasificacion_d5_resumen.csv`.

**Componentes, niveles:**

| | r(t) | R² | ADF (p) | KPSS (p) | ACF residuos 1 / 12 | Clase D5 |
|---|---|---|---|---|---|---|
| PC1 | 0,993 | 0,985 | −2,77 (0,25) | 0,195 (0,018) | 0,92 / 0,23 | DS |
| PC2 | 0,080 | 0,006 | −3,09 (0,12) | 0,322 (0,010) | 0,99 / 0,36 | DS |
| PC3 | 0,036 | 0,001 | −2,98 (0,16) | 0,154 (0,043) | 0,92 / 0,14 | DS |
| PC4 | 0,015 | 0,000 | −2,49 (0,37) | 0,858 (0,010) | 0,96 / 0,59 | DS |

**Componentes, transformadas:**

| | r(t) | R² | ADF (p) | KPSS (p) | ACF residuos 1 / 12 | Clase D5 |
|---|---|---|---|---|---|---|
| PC1 | 0,118 | 0,014 | −4,19 (≤ 0,01) | 0,065 (≥ 0,10) | 0,54 / 0,01 | TS |
| PC2 | −0,196 | 0,039 | −3,70 (0,025) | 0,087 (≥ 0,10) | 0,42 / −0,005 | TS |
| PC3 | −0,334 | 0,111 | −5,49 (≤ 0,01) | 0,056 (≥ 0,10) | 0,12 / 0,27 | TS |
| PC4 | −0,356 | 0,126 | −5,27 (≤ 0,01) | 0,181 (0,023) | 0,27 / 0,04 | indeterminada |

**Conteos D5:**

- componentes en niveles: 0 TS, 4 DS y 0 indeterminadas;
- componentes transformadas: 3 TS, 0 DS y 1 indeterminada;
- 17 series en niveles: 1 TS, 13 DS y 3 indeterminadas.

**Series en niveles, clase por serie:**

- **TS:** EMBIG Perú.
- **Indeterminadas:** crédito de consumo y PBI desestacionalizado (ADF y KPSS rechazan las dos) y
  TIPMN (ídem, KPSS con p = 0,011).
- **DS:** las otras 13. Las tasas de referencia e interbancaria están cerca del umbral de la ADF
  (p = 0,057 y 0,075).

$r(\text{PC1}, t)$ reproduce el 0,993 del HTML. Los estadísticos ADF y KPSS de Python
(`statsmodels`) coinciden con los de `tseries` con una diferencia menor que 1e-13. Los p-valores de
la regla son los de las tablas de `tseries` en las dos lenguas, así que la clasificación coincide.

- **Interpretación (solo la clasificación, sin la Parte C):** con la regla D5 fijada de antemano,
  ninguno de los cuatro ejes en niveles es estacionario alrededor de una recta. En las
  transformadas, PC1 a PC3 lo son, y PC4 queda indeterminado. En las series, predomina DS.
- **Dudas abiertas:**
  1. D5 usa la ADF y la KPSS sin quiebres. Con quiebres (2008, 2020), ambas pierden potencia
     [VERIFICAR: fuente]: la KPSS tiende a rechazar y la ADF a no rechazar, lo que empuja hacia DS.
     ¿Se agrega una prueba con quiebre como sensibilidad declarada, sin cambiar la regla D5?
  2. Los tres casos indeterminados son del tipo «ambas rechazan», no «ninguna rechaza».
  3. Varios p-valores de la KPSS están acotados en 0,01 por la tabla de `tseries`.
  4. La tabla de §4 del plan («qué cambia en la tesis según el resultado») la tiene que leer Roberto
     con el Dr. Camiz; aquí no saco conclusiones sobre la Parte C.

### 4.6 Apunte 10 · Contraste sin tendencia y nulo de tendencias independientes

**Contraste** (NIV `05_pca_contraste_tendencia.csv`, formato largo `version, medida, componente,
valor`; p. ej., fila 17 = `niveles_sin_tendencia, inercia, 1`):

| | Niveles | Niveles sin tendencia lineal | Transformadas |
|---|---|---|---|
| Inercia PC1–PC4 (%) | 67,2 / 18,3 / 7,1 / 2,9 | 40,0 / 19,0 / 11,7 / 7,4 | 23,3 / 16,0 / 11,2 / 8,6 |
| KMO | 0,862 | 0,701 | 0,695 |
| χ² de Bartlett (con n) | 12 210 | 6 104 | 1 831 |
| ln\|R\| | −55,37 | −27,68 | −8,34 |
| Número de condición | 67 647 | 4 551 | 68,1 |
| Equivalente de PC1–PC4 de niveles | — | PC4 / PC1 / PC3 / PC2 | PC2 / PC1 / PC3 / PC5 |
| \|Tucker\| con PC1–PC4 de niveles | 1 / 1 / 1 / 1 | 0,51 / 0,74 / 0,83 / 0,78 | 0,56 / 0,64 / 0,66 / 0,64 |

**Nulo** (NIV `05_nulo_tendencias.csv`; filas 1–4 con deriva, 5–8 sin deriva y 9–12 sin tendencia;
columna `proporcion`; las simulaciones por réplica están en `05_nulo_simulaciones.csv`):

| Medida | Con deriva | Sin deriva | Sin tendencia (sobre las series sin recta) |
|---|---|---|---|
| Inercia PC1 | 0,902 | 0,004 | 0,124 |
| Inercia PC2 | 0,015 | 0,592 | 0,595 |
| Inercia PC3 | 0,212 | 0,950 | 0,604 |
| \|r\| medio | 0,932 | 0,017 | 0,238 |

Redondeadas a dos decimales, las columnas con y sin deriva reproducen el HTML de la iteración 2
(0,90; 0,01; 0,21; 0,93 y 0,00; 0,59; 0,95; 0,02; fila de paridad «Proporciones … frente al HTML de
la iteración 2»). La proporción del PC2 con deriva es 15/1 000 = 0,015, que el Rmd muestra como
«0,01» (formato a dos decimales del valor binario). En el mapa de cifras, las proporciones del nulo
llevan tres decimales para no perder esa diferencia.

- **Interpretación:** sin la recta de cada serie, el PC1 pasa de 67,2 % a 40,0 % y el KMO, de 0,86
  a 0,70, el mismo nivel que en las transformadas. La tendencia explica buena parte de la inercia
  del PC1 y de la adecuación en niveles: es el sentido mecánico de «el trend ha ayudado a la PCA».
  Ningún eje de niveles conserva su dirección sin la recta con congruencia ≥ 0,85. El PC3 es el más
  parecido (0,83), y el orden de los ejes cambia: el PC2 de niveles corresponde al PC1 sin tendencia.
  Frente al nulo aplicado a las series sin recta, ni el PC1 (0,124) ni el PC2 (0,595) se separan de
  lo que darían 17 series independientes.
- **Dudas abiertas:**
  1. El nulo «sin tendencia» quita la recta a las series simuladas con deriva. Es la versión
     coherente con el diagnóstico, pero no distingue series TS de DS. El plan (sección 4, fila
     «mixto») sugiere un nulo por serie según su clase D5; no lo construí porque no está en el
     encargo de 3a.
  2. Los umbrales de congruencia (0,85 y 0,95) siguen sin fuente fichada (`[VERIFICAR]` en el Rmd).
  3. El emparejamiento codicioso asigna el PC1 de niveles al PC4 sin tendencia con congruencia de
     0,51, un emparejamiento débil: conviene leer la matriz completa de congruencias antes de
     interpretar «equivalentes».

## 5. Paridad Python–R

Render final del Rmd: exit 0, sin `Warning` ni `Error` en el registro ni en el HTML. **49 de 49**
comprobaciones coinciden: 28 en `data/results/niveles/R_paridad_python.csv` y 21 en
`data/results/R_paridad_python.csv`. Las 15 anteriores no cambiaron, y hay 34 nuevas:

- en las dos vías: valores propios, cargas, cos², Horn, ACF, $n_{\text{ef}}$, KMO y Bartlett,
  bootstrap (congruencias, valores propios e intervalos de cargas), tendencia, estadísticos ADF y
  KPSS y clase D5;
- solo en niveles: tendencia, ADF y KPSS y clase de las 17 series; las proporciones del nulo frente
  al HTML de la iteración 2; las 12 000 medidas simuladas del nulo; el resumen del nulo; el
  contraste sin tendencia; las dimensiones.

Diferencia máxima entre las filas nuevas: 5,4e-12 (relativa, en χ² y el número de condición); el
resto, por debajo de 1e-13. La mayor de todo el archivo (4,7e-11) es la fila previa de valores
propios frente a Rcamiz (`07_rcamiz_valores_propios.csv`), que no cambió.

En sentido inverso, la sección 8 del 05 compara sus cifras con los `R_*` exportados por el Rmd
(15 comprobaciones, todas por debajo de su tolerancia).

**Excepción declarada:** Horn usa generadores distintos (numpy PCG64 frente a Mersenne-Twister de
R, semilla 42 en los dos). Los umbrales p95 difieren en el tercer decimal (p. ej., 1,604 frente a
1,612 para λ1 en niveles), y por eso se compara solo el número de componentes retenidos (2 y 4).

Los demás `R_*` del port (`R_aede_cortes`, `R_hfc_jerarquia`, `R_ehfc_cofenetica` y
`R_regimenes_criterios`) no cambiaron, byte a byte.

## 6. Desviaciones respecto del plan, de `decisiones.qmd` o del marco

1. **`src/series_tiempo.py`** es un módulo que el plan no listaba. Separa los diagnósticos de series
   de tiempo de `multivariado.py`.
2. **No hay `src/particion.py`** (instrucción del orquestador: solo lo necesario para el 05, que no
   usa Fisher).
3. **Especificación de D5:** D5 pide «especificación y rezagos fijos y declarados en el código».
   Fijé ADF con constante y tendencia (6 rezagos) y KPSS en tendencia (4 rezagos), con los p-valores
   de las tablas de `tseries` en las dos lenguas (§1). Fue una elección mía, anterior a los
   resultados. Si Roberto prefiere otra especificación, cambiarla después de ver estos resultados
   contradiría el espíritu de D5: habría que registrarlo como decisión nueva y declararlo.
4. **Bartlett con $n_{\text{ef}}$:** usa la mediana de los $n_{\text{ef}}$ de los pares. Es una
   convención propuesta (§4.2), no un método con fuente.
5. **El nulo del Rmd ahora sortea una sola vez** los inicios que comparten las dos versiones. El
   resultado es idéntico (verificado: proporciones, p50 y p95 sin cambio).
6. **Plan, apunte 3:** «la fórmula de $n_{\text{ef}}$ figura con su fuente fichada o con
   `[VERIFICAR]` y una fila en el registro». Puse `[VERIFICAR]` en el Rmd, en el 05 y en
   `src/series_tiempo.py`, pero **no edité `tesis/registro_verificacion.md`**: lo mantiene el
   bibliotecario, que trabaja en paralelo, y editarlo los dos a la vez generaría conflictos. Marcas
   nuevas que necesitan fila en el registro:
   - fórmula de $n_{\text{ef}}$;
   - bootstrap por bloques móviles (se suele atribuir a Künsch, 1989);
   - umbrales de congruencia de Tucker (0,85 y 0,95);
   - fuente de la pérdida de potencia de la ADF y la KPSS ante quiebres.

   Ya tenían fila: Granger y Newbold, Phillips, ADF y KPSS, Bartlett y KMO.
7. **CLAUDE.md, «Estructura»:** dice que `R/` «requiere Rcamiz/AedeClahfac locales». Ya no es así,
   porque el Rmd usa `R/camiz_port.R`. No lo edité: CLAUDE.md no me corresponde.

## 7. Parámetro `version_asesor`

Render de prueba con `params = list(version_asesor = TRUE)` hacia el scratchpad
(`3a_dev/version_asesor.html`): exit 0, **0** bloques `class="pregunta"` (32 en la versión
normal). Solo queda la cadena «Para Roberto» en la regla CSS `.pregunta::before`, que no se
muestra. Además, la síntesis del bloque 1 mencionaba «los recuadros "Para Roberto"»: ahora esa
mención se omite cuando el parámetro es TRUE.

## 8. Criterios de aceptación de la sección 7 del plan que me corresponden

| # | Criterio | Estado | Evidencia |
|---|---|---|---|
| 1 | El 05 corre con nbconvert sin errores, los `assert` de dimensiones pasan y escribe los CSV de la sección 3 | Cumple | `nb05_3.log` exit 0, sin salidas `stderr` ni `error`; `05_pca_cos2`, `05_acf`, `05_correlaciones`, `05_n_efectivo`, `05_adecuacion`, `05_bootstrap_congruencia`, `05_bootstrap_valores_propios`, `05_pca_tendencia_componentes` (dos vías), `05_tendencia_series`, `05_pca_contraste_tendencia` y `05_dimensiones` |
| 2 | Rmd con exit 0, sin `Warning` ni `Error`; paridad con las filas nuevas, todas coincidentes | Cumple | `render3.log` exit 0, 0 `## Warning`/`## Error` en el HTML; 49/49 «sí» (valores propios mensuales, cos², ACF, KMO y Bartlett, bootstrap con índices compartidos, ADF y KPSS de residuos, nulo) |
| 3 | El CSV del nulo reproduce las proporciones del HTML | Cumple | `R_nulo_tendencias.csv` y `05_nulo_tendencias.csv`, redondeados a 2 decimales: 0,90; 0,01; 0,21; 0,93 y 0,00; 0,59; 0,95; 0,02 (fila de paridad con diferencia 0) |
| 4 | `generar_cifras.py` dos veces → `cifras.tex` idéntico byte a byte; cada macro remite a una fila del mapa y cada fila del mapa a un CSV existente | Cumple | md5 idéntico tras dos ejecuciones; `--comprobar` exit 0; el script falla si el archivo, la columna o la fila única no existen. 54 macros, incluidas las 6 del contrato y `\anioInicioDatos`/`\anioFinDatos`, pedidas por el redactor |
| 11 | El capítulo de resultados no cambia | Cumple | No modifiqué ningún archivo de `tesis/` (solo creé `tesis/_cifras.yml`) ni de `tesis_latex/capitulos/` (solo creé `tesis_latex/cifras.tex`) |

## 9. Dudas abiertas para Roberto (resumen)

1. **D5 y quiebres:** ¿se añade una prueba de raíz unitaria con quiebre como sensibilidad
   declarada, sin tocar la regla? Los tres casos indeterminados son del tipo «ambas rechazan».
2. **$n_{	ext{ef}}$:** hay que fijar la fórmula (truncamiento $J$) con su fuente y decidir cómo se
   resume para Bartlett. Con la mediana, Bartlett en niveles da p = 0,06.
3. **Dimensiones (OE6):** hay que registrar de antemano un criterio basado en los intervalos bootstrap
   de los valores propios.
4. **Nulo por serie según la clase D5:** el plan lo sugiere para el caso «mixto», pero está fuera
   del encargo de 3a. ¿Va en 3b?
5. **Textos interpretativos previos del Rmd:** el hallazgo de A.2 («el movimiento cíclico está en PC2
   en adelante») y el de la sección 2 («co-movimiento real») se escribieron antes de la
   clasificación D5. No los reescribí, porque eso es interpretación de la Parte C. Conviene
   revisarlos con el Dr. Camiz.
6. **Registro de verificación:** las cuatro marcas `[VERIFICAR]` nuevas (§6, punto 6) necesitan
   fila; las agrega el bibliotecario.
