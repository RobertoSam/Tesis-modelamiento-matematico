# Nota del desarrollador · 7 de noviembre de 2026 · Iteración 3c, D19 (N-04)

Rama `iteracion-3c`. Commit del cambio: `c6e2a27`.

## Qué cambió

En la rama TS del nulo mixto (D8), los inicios de bloque ahora se sortean en $\{1,\dots,n-L+1\}$, con
$n = 228$ y $L = 12$, es decir, en $\{1,\dots,217\}$. Antes se reutilizaban los inicios de los $n-1$
incrementos, sorteados en $\{1,\dots,216\}$.

**Diseño elegido.** La rama TS tiene **inicios propios**, `inicios_nulo_ts` (1000 réplicas × 16 series
× 19 bloques). Se sortean con el mismo generador **a continuación** de los inicios de los incrementos,
sin volver a fijar la semilla 2026. Así, los inicios de los incrementos no cambian y las versiones
con deriva, sin deriva y sin tendencia, así como las series DS del mixto, quedan idénticas bit a bit.
Solo cambian las series simuladas con tratamiento TS. El siguiente uso del generador en el Rmd
(`b3-retencion`, Horn) vuelve a fijar la semilla, de modo que nada posterior cambia.

**Desviación respecto de D19 (para validar).** D19 fija el rango del sorteo, pero no dice si se
sortea aparte o si se reemplaza el sorteo común. Elegí un sorteo aparte, que solo afecta a la rama
TS. Si Roberto o el asesor prefieren otra cosa (p. ej., otra semilla declarada), el cambio es local.

## Archivos modificados

| Archivo | Cambio |
|---|---|
| `src/remuestreo.py` | Nueva `comprobar_inicios(inicios, n, largo)`: rango $\{1,\dots,n-L+1\}$ y $\lceil n/L\rceil$ bloques. `nulo_tendencias(..., inicios_ts=None)`: con alguna serie TS exige `inicios_ts` válidos para $n$ filas. Además valida siempre los inicios de los incrementos para $n-1$ filas. |
| `R/ciclo_financiero_final.Rmd` | Chunk `b2-nulo`: sorteo de `inicios_nulo_ts` con `stopifnot` de los rangos. Ahí se comprueba que los incrementos alcanzan 216 y nunca 217, y que los residuos alcanzan 217. La rama TS de `simular_nulo` usa `inicios_nulo_ts`. Se escribe `R_nulo_indices_ts.csv`. También se actualizan el texto de la sección 2.4 y los comentarios. |
| `notebooks/05_pca.ipynb` | Lee `R_nulo_indices_ts.csv` y comprueba que su máximo sea 217. Si falta y `VIA = 'ambas'` (no regresión con el antecedente, que no tiene mixto), omite el mixto en vez de usar los inicios anteriores a D19. Con la versión vigente, la falta del archivo es un error. Se actualizó el texto. |
| `tests/test_nulo_mixto.py` | Ajuste de la prueba de bloques consecutivos, que ahora usa los inicios 1, 13, …, 217 de la rama TS. Cuatro pruebas nuevas: `test_ts_exige_inicios_propios`, `test_rango_de_inicios_por_rama`, `test_ultimo_inicio_usa_el_residuo_del_ultimo_mes` (con el inicio 217, el bloque incluye el residuo del mes 228 y la simulación coincide con el cálculo a mano) y `test_sorteo_del_rmd_alcanza_el_ultimo_inicio` (en el CSV del Rmd, los inicios TS cubren exactamente {1, …, 217} y el 217 aparece en cada una de las 16 series; los de los incrementos tienen máximo 216). |
| `data/results/final/` | Nuevo `R_nulo_indices_ts.csv`. Regenerados `05_nulo_tendencias.csv`, `05_nulo_simulaciones.csv`, `R_nulo_tendencias.csv`, `R_nulo_simulaciones.csv` y `R_paridad_python.csv`. |

No toqué `tesis_latex/`, `tesis/`, `papers/` ni el Rmd de exploración (md5 `c21946b6…`, sin cambios).

## Comandos ejecutados (en este orden)

```
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')"
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/05_pca.ipynb
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd')"
python3 -m pytest tests/
python3 herramientas/generar_cifras.py
python3 herramientas/exportar_parametros_diseno.py
python3 herramientas/generar_cifras.py --comprobar
python3 herramientas/exportar_parametros_diseno.py --comprobar
python3 herramientas/no_regresion_05.py
```

Se renderiza dos veces porque el Rmd sortea los índices que lee el 05 y luego lee los CSV del 05 para
la tabla de paridad.

**Entorno.** CRAN está bloqueado por el proxy (403 a `cloud.r-project.org`). Los paquetes de R se
instalaron desde los repositorios de Ubuntu (`r-cran-*`): rmarkdown 2.25, knitr 1.45, ggplot2 3.4.4,
scales 1.3.0, tseries 0.10-55, dendextend 1.17.1 y jsonlite 1.8.8, con R 4.3.3. En Python se
instalaron statsmodels 0.15.0 y nbconvert 7.17.2. **Control de línea base:** antes de tocar el
código, se renderizó el Rmd sin cambios, y todos los `R_*.csv` salieron idénticos byte a byte a los
versionados. El entorno nuevo reproduce, por tanto, los resultados auditados.

Las figuras `reports/figures/final/05_*.png` se regeneraron con bytes distintos por la versión de
matplotlib, aunque no dependen del nulo. Restauré las versionadas para no introducir ruido.

## Qué depende de la rama TS (y qué no)

- **Depende:** solo el nulo mixto del notebook 05 y la sección 2.4 del Rmd final, es decir, las filas
  `mixto_ind_ts` y `mixto_ind_ds` de `05_nulo_tendencias.csv` y `05_nulo_simulaciones.csv`.
- **No depende:** el 07b (nulo de estructura, OE4, D10). Remuestrea de forma conjunta los incrementos
  con sus propios índices `R_nulo_estructura_indices_L*.csv` y solo usa `indices_desde_inicios`,
  que no cambió. Tampoco dependen el bootstrap (05, 07c, 09a), la regla del 06 ni la datación. Por
  eso no se re-ejecutaron: sus CSV y los criterios de OE4, la ventana elegida y las transiciones de
  D10 no cambian. El antecedente (`data/results/`, `data/results/niveles/`) no tiene mixto:
  `no_regresion_05.py` pasa (37 archivos idénticos).

## Resultados que cambiaron (`data/results/final/05_nulo_tendencias.csv`)

Columnas `p50`, `p95` y `proporcion` (proporción de réplicas con valor ≥ observado). El observado no
cambia (PC1 65,23 %, PC2 19,38 %, PC3 7,55 %, |r| medio 0,556).

| Fila | Versión, medida | p50 antes → después | p95 antes → después | Proporción antes → después |
|---|---|---|---|---|
| 14 | mixto_ind_ts, inercia_pc1 | 68,81 → 68,73 | 76,67 → 76,51 | 0,783 → 0,775 |
| 15 | mixto_ind_ts, inercia_pc2 | 10,22 → 10,19 | 14,76 → 14,68 | 0,003 → 0,002 |
| 16 | mixto_ind_ts, inercia_pc3 | 6,81 → 6,76 | 8,55 → 8,74 | 0,221 → 0,221 |
| 17 | mixto_ind_ts, r_abs_medio | 0,594 → 0,594 | 0,699 → 0,696 | 0,747 → 0,727 |
| 18 | mixto_ind_ds, inercia_pc1 | 70,12 → 70,12 | 78,59 → 78,91 | 0,826 → 0,824 |
| 19 | mixto_ind_ds, inercia_pc2 | 11,15 → 11,17 | 16,44 → 16,38 | 0,004 → 0,003 |
| 20 | mixto_ind_ds, inercia_pc3 | 6,52 → 6,51 | 9,01 → 8,96 | 0,223 → 0,218 |
| 21 | mixto_ind_ds, r_abs_medio | 0,621 → 0,622 | 0,734 → 0,733 | 0,842 → 0,846 |

Filas 2 a 13 (con deriva, sin deriva y sin tendencia): sin cambios. En `05_nulo_simulaciones.csv`,
la diferencia máxima en esas versiones es 0.

**Interpretación (una línea).** Con el sorteo corregido, el PC1 observado sigue sin superar al nulo
mixto (proporción ≥ observado de 0,775 y 0,824), mientras que el PC2 sí lo supera (0,002 y 0,003).
Es la misma lectura que antes de D19: la corrección mueve las proporciones en milésimas.

**Dudas abiertas para Roberto.**
1. Con tres o cuatro series TS de 16 (EMBIG Perú; más Crédito consumo, TIPMN y PBI cuando las
   indeterminadas se tratan como TS), ¿basta el nulo mixto para la conclusión sobre el PC2, o
   conviene una sensibilidad con $L \in \{24, 36\}$ también en este nulo?
2. ¿Prefiere el asesor que la rama TS tenga su propia semilla declarada, en lugar de la continuación
   del generador? Es una cuestión de presentación: el resultado cualitativo no depende de ella.

## Cifras de la tesis (macros)

**Ninguna macro cambió.** `cifras_mapa.csv` no lee filas del mixto. Las macros del nulo
(`nuloConDerivaPCUno`, `nuloConDerivaPCDos`, `nuloSinDerivaPCUno`, `nuloSinDerivaPCDos`,
`nuloSinTendenciaPCUno`, `nuloSinTendenciaPCDos` y `nuloConDerivaMedianaPCUno`) usan versiones que
no cambian. `generar_cifras.py` reescribió `cifras.tex` y `_cifras.yml` sin diferencias (71 cifras),
y `--comprobar` termina con exit 0 en los dos scripts. `parametros_diseno.csv` está al día.

**Para el redactor (no lo edité).** `obs:nulo-mixto` (c) y el texto de `03_marco_teorico.tex` cerca
de las líneas 1511, 1533 y 1547 todavía describen la convención anterior: la rama TS con
$n' = n-1$, que reutiliza los inicios de los incrementos. Debe pasar a $n' = n$ con inicios propios
(D19). Si el informe lo menciona, el editor debe hacer el mismo cambio.

## Pruebas y paridad

- `pytest tests/`: **55 passed** (antes 51; las 4 nuevas son de D19), exit 0.
- `final/R_paridad_python.csv`: **55 de 55 «sí»**. Filas del nulo: simulaciones por réplica
  (5 versiones × 1000 × 4), dif. máx. 6,4e-15; resumen, 1,8e-15. `final/anexo/R_paridad_python.csv`:
  9 de 9 «sí» (sin cambios).
- Comprobaciones internas del notebook 05 contra el Rmd: todas coinciden (nulo por réplica y
  resumen ≤ 1e-10).
- Rmd final: exit 0, 0 `Warning` en el log y 0 bloques `## Warning`/`## Error` en el HTML. Solo se
  renderizó con `version_asesor = FALSE`. El cambio no toca los recuadros `.pregunta`.
- `herramientas/no_regresion_05.py`: superada (37 archivos).

## Respuesta a la observación del auditor

- **N-04:** corregido según D19 (ver arriba). Los inicios de la rama TS están en $\{1,\dots,n-L+1\}$
  en Python y en R, con paridad, y el último inicio (217) se sortea, como verifica
  `test_sorteo_del_rmd_alcanza_el_ultimo_inicio`.
