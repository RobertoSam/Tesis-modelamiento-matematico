# Nota del desarrollador · 27 de noviembre de 2026 · Fase 0 de la vuelta 2 de la iteración 3c (F0-3 y F0-4)

**Rama:** `iteracion-3c` (HEAD `402f6f3`, sin commits propios en esta sesión: los hará el
orquestador). **Plan:** `asesoria/2026-11-26_plan-cierre-iteracion-3c.md`, sección 5.1 y criterios
5.3. **Alcance de esta nota:** solo F0-3 (cobertura descriptiva de los episodios) y F0-4
(inventario de la fusión con `main`). F0-1 y F0-2 están en `2026-11-26_desarrollador.md`.

No se tocaron `tesis_latex/capitulos/`, `tesis/` (salvo `_cifras.yml`, que es generado),
`decisiones.qmd`, `CLAUDE.md`, `tesis/referencias.bib` ni `main`. No se fusionó nada. No se creó
ninguna macro nueva.

## 1. Archivos y comandos

### F0-3

| Archivo | Cambio |
|---|---|
| `src/episodios.py` | Funciones nuevas `distancia_a_episodios`, `posiciones_corte_admisibles` y `cobertura_episodios` (y su mención en el docstring del módulo) |
| `notebooks/09a_datacion_pca.ipynb` | Celdas nuevas «5 bis» (markdown `f03cobmd` y código `f03cobpy`), después de la compatibilidad; salida nueva en el texto de la celda 0 |
| `R/ciclo_financiero_final.Rmd` | Constantes `TOLERANCIA_PRINCIPAL <- 3L` y `TOLERANCIA_SENSIBILIDAD <- 6L` junto a `leer_episodios()`; el chunk `b6-compatibilidad` las usa en lugar de los literales 3 y 6 (mismo resultado, comprobado por diff); chunk nuevo `b6-cobertura`; fila nueva de paridad en `anexo-paridad` |
| `tests/test_cobertura_episodios.py` | 3 pruebas nuevas |
| `data/results/final/09a_cobertura_episodios.csv` | Nuevo (Python) |
| `data/results/final/R_cobertura_episodios.csv` | Nuevo (réplica en R) |
| `data/results/final/R_paridad_python.csv`, `R_paridad_resumen.csv` | Fila nueva (línea 58 con el encabezado como línea 1, fila 57 de datos; criterio «Cobertura de los episodios…»); resumen de 57/57 a 58/58 |
| `tesis_latex/cifras.tex`, `tesis/_cifras.yml` | Regenerados: `\filasParidad` y `\filasParidadCoinciden` pasan de 57 a 58 (efecto directo de la fila de paridad). Siguen siendo 200 macros |

### F0-4

Ningún archivo del repositorio cambia: el inventario está en la sección 3.2 de esta nota.

### Comandos ejecutados (desde la raíz del repositorio)

```
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd', output_dir='<scratchpad>/html')"
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=python3 notebooks/09a_datacion_pca.ipynb
Rscript -e "rmarkdown::render('R/ciclo_financiero_final.Rmd', output_dir='<scratchpad>/html')"
python3 herramientas/generar_cifras.py
python3 herramientas/generar_cifras.py --comprobar
python3 -m pytest -q tests/
git fetch origin
git merge-tree --write-tree --name-only HEAD origin/main
```

Orden: Rmd (escribe `R_cobertura_episodios.csv`; la fila de paridad sale «archivo ausente»),
notebook completo (compara con R) y Rmd otra vez (paridad completa). El HTML del Rmd se generó
fuera del repositorio. **Entorno:** el contenedor no traía R ni Jupyter. Se instaló R 4.3.3 con
`apt` (con `rmarkdown`, `knitr`, `ggplot2`, `scales`, `tseries` y `dendextend` de Ubuntu; Rcamiz
no está, es opcional) y, con `pip`, `nbconvert` 7.17.2, `ipykernel` 7.4.0, `statsmodels` 0.15.0,
`scikit-learn` 1.9.1 y `seaborn` 0.13.2. Python 3.13.18, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1.
`requirements.txt` no fija versiones (ver duda 4.3).

## 2. Verificaciones

- **El resto de los CSV no cambia.** Copia de `data/results/final/` (con `anexo/`) antes de
  ejecutar y `diff -rq` después: solo aparecen los dos CSV nuevos y difieren `R_paridad_python.csv`
  (una línea añadida, ninguna modificada) y `R_paridad_resumen.csv`. Las 9 figuras de
  `reports/figures/final/` tienen el mismo md5.
- **Idempotencia del Rmd.** Entre la primera y la segunda ejecución solo cambian
  `R_paridad_python.csv` y `R_paridad_resumen.csv` (la fila nueva pasa de «archivo ausente» a «sí»).
- **Paridad:** 58 de 58 filas coinciden (`R_paridad_resumen.csv`, fila 2). La fila nueva compara
  universo, n_min, h, primer y último mes, totales, cubiertos y la fracción con 15 cifras
  (`dif_max = 0`). El notebook confirma además los conteos exactos y la fracción con
  diferencia máxima de 3,3e-16.
- **Pruebas:** `pytest tests/` da 64 aprobadas (61 previas y 3 nuevas) y 0 omitidas.
- **Cifras:** `generar_cifras.py --comprobar` termina con código 0 (200 macros). Antes de regenerar
  daba código 1 solo por `\filasParidad` y `\filasParidadCoinciden`.
- **Restricciones:** `git diff 7c58906 -- tesis/referencias.bib decisiones.qmd CLAUDE.md` sale vacío.

## 3. Resultados

### 3.1 F0-3 · Cobertura descriptiva de los episodios

**Definición.** Un mes cae «a h meses o menos de algún episodio» si su distancia al intervalo
[inicio, fin efectivo] de al menos un episodio de `data/referencia/episodios_referencia.csv` es
≤ h, la misma distancia de `09a_compatibilidad_cortes.csv` (`def:tolerancia`, `obs:tolerancia`). Un
episodio puntual ocupa su mes de inicio. Hay dos universos:

- `meses_muestra`: los 228 meses de los datos (2007-01 a 2025-12), antes de la media móvil;
- `posiciones_corte_admisibles`: los meses en que la partición de Fisher puede iniciar un régimen
  nuevo con tramos de al menos n_min meses, sobre las 217 fechas de los scores suavizados que usa la
  datación. Son los índices c (base 0, convención de `fisher_multivariado`) con
  n_min ≤ c ≤ n − n_min. Es la unión sobre k de las posiciones que la partición puede elegir
  (comprobado por enumeración exhaustiva en `tests/test_cobertura_episodios.py`).

**Parámetros.** h se lee de `TOLERANCIA_PRINCIPAL` y `TOLERANCIA_SENSIBILIDAD`
(`src/episodios.py`, D7). n_min se lee de la constante `N_MIN` del notebook 09a, la misma que usa
la datación (D17.1). En el Rmd, n_min sale de `formals(datar)$tam_min`, el valor que usa `datar`. h
sale de las constantes nuevas del mismo nombre (sección 4).

**Cifras** (`data/results/final/09a_cobertura_episodios.csv`, con el encabezado como línea 1;
columnas `n_cubiertos`, `n_total` y `fraccion`; idéntico en `R_cobertura_episodios.csv`):

| Línea | Universo | h | Primer y último mes | Cubiertos / total | `fraccion` |
|---|---|---|---|---|---|
| 2 | `meses_muestra` | 3 | 2007-01 a 2025-12 | 87 / 228 | 0,3816 |
| 3 | `meses_muestra` | 6 | 2007-01 a 2025-12 | 105 / 228 | 0,4605 |
| 4 | `posiciones_corte_admisibles` (n_min = 12) | 3 | 2008-12 a 2025-01 | 81 / 194 | 0,4175 |
| 5 | `posiciones_corte_admisibles` (n_min = 12) | 6 | 2008-12 a 2025-01 | 96 / 194 | 0,4948 |

- **Interpretación (solo descriptiva):** con los seis episodios del archivo, cerca de dos de cada
  cinco posiciones de corte admisibles están a 3 meses o menos de algún episodio, y cerca de la
  mitad a 6 meses o menos. Es una propiedad del calendario de episodios, no de los datos ni de la
  datación. Esta nota **no** la compara con los cortes compatibles de F0-2 ni la usa como
  evidencia a favor o en contra de HT3. Hacerlo requeriría fijar un nulo o un estadístico (O1 del
  plan), y eso no corresponde a la fase 0.
- **Dudas abiertas para Roberto:** (i) la tesis debe decidir cuál de los dos universos es la
  referencia pertinente para HT3. El de posiciones admisibles es el que comparte el dominio con
  los cortes, porque excluye los 12 meses de cada borde y los meses perdidos por la media móvil.
  (ii) El universo de posiciones trata como igualmente posibles todas las posiciones admisibles.
  Eso no es un modelo de la datación: no dice con qué probabilidad caería un corte en cada mes. Por
  eso la cifra no es una «probabilidad de acierto por azar». (iii) Los cortes van en el primer mes
  del régimen nuevo, sin descontar el rezago de la media móvil causal (convención de la sección 5
  del 09a). Con otra convención de fechado de los cortes, el universo de posiciones cambiaría. (iv)
  La cobertura depende de que los episodios son largos (la crisis global, el colapso de las
  materias primas y la guerra comercial duran 10, 20 y 20 meses) y de que se solapan con h = 6.

### 3.2 F0-4 · Inventario de la fusión con `main` (sin fusionar)

`git fetch origin`; `git merge-tree --write-tree --name-only HEAD origin/main` devuelve código 1,
árbol `1f8005f`, **16 archivos en conflicto**. HEAD = `402f6f3`, `origin/main` = `1bb4dcb`, base
común `b893b23` (cierre auditado de la 3b). Desde la base hay 38 commits en la rama y 51 en `main`.
El inventario se hizo sobre los commits, no sobre el árbol de trabajo. Los cambios sin commit de
esta fase 0 (los de esta nota y los del bibliotecario en `tesis/registro_verificacion.md` y
`papers/camiz_spada_2024.qmd`) recaen en archivos que ya están en la lista, así que la lista no
cambia, aunque sí pueden crecer los bloques en conflicto.

| # | Archivo | Tipo | Bloques | Cambios desde la base (rama / `main`) | Resolución propuesta |
|---|---|---|---|---|---|
| 1 | `CLAUDE.md` | contenido | 1 | +2/−1 / +2/−1 | **Espera R-2.** El bloque es la descripción de D18 y D19 de la regla 4: la rama dice «corrección del sorteo», `main` dice «convención; se corrige en la iteración 4». Se alinea con D20 o con la reversión (W-1) |
| 2 | `decisiones.qmd` | contenido | 1 | +32 / +40 | **Espera R-2.** Dos textos distintos de D19 (rama: corregir el código; `main`: mantener como convención), y D18 en ambos. Según W-1 se conservan **ambos** textos de D19 y se agrega D20 |
| 3 | `herramientas/cifras_mapa.csv` | contenido | 1 | +129 / +28 | **Unión del mapa y regeneración.** Hay 201 claves en la rama y 100 en `main`. Las 23 claves que solo están en `main` se agregan y las 124 que solo están en la rama se conservan. Las 5 claves comunes con distinta definición (`congruenciaBootPCUnoNiveles`, `congruenciaBootPCTresNiveles`, `nuloMixtoTsPCUno`, `nuloMixtoTsPCDos`, `nuloMixtoDsPCDos`) difieren solo en la descripción, no en archivo, filtro, columna ni formato: se propone la descripción de la rama, que menciona D19. Ver el riesgo (a) |
| 4 | `tesis_latex/cifras.tex` | contenido (generado) | 1 | +258 / +56 | **No se resuelve a mano.** Se toma cualquiera de los dos lados y se regenera con `generar_cifras.py` después de unir el mapa |
| 5 | `tesis/_cifras.yml` | contenido (generado) | 1 | +129 / +28 | Igual que el anterior. Los valores del nulo mixto de `main` son los previos a D19 (p. ej., `nuloMixtoTsPCDos` 0,003 en `main` y 0,002 en la rama). Si se regenera desde `data/results/` de la rama, no queda ninguno (criterio 8) |
| 6 | `tesis_latex/capitulos/03_marco_teorico.tex` | renombre + modificación (la rama renombró `02_marco_teorico.tex` a `03_…`, similitud del 87 %; `main` modificó `02_…`, +5/−2) | 1 | +1891 (archivo nuevo) / +5/−2 en `02_…` | **Comparación de fragmentos.** El bloque marcado es `obs:nulo-mixto` (c), con el texto de D19 de cada lado: **espera R-2**. Además, la fusión automática **duplica** sin marcar la aclaración de D18 en `def:episodio`: queda la frase de la rama («Por la decisión D18, *externo* significa externo al análisis…») y, tres líneas después, la de `main` («Aquí, «externo» significa externo al análisis… (decisión D18)»). Se propone quitar la frase de `main`, que ya está cubierta. Lo hace el redactor LaTeX |
| 7 | `tesis/registro_verificacion.md` | contenido | 2 | +337/−35 / +22/−3 | Unión manual a cargo del **bibliotecario** (F0-6, W-7). Bloque 1: la fila de `congreso_2018` (redacción de D18). Bloque 2: la tabla de episodios y la sección «Estado del arte (iteración 3c)», que solo existe en la rama |
| 8 | `papers/abdi_2010.qmd` | add/add | 2 | +79 / +23 | Ficha de la rama, si F0-6 (b) confirma que no pierde nada de la de `main` (bibliotecario) |
| 9 | `papers/camiz_2021_pca.qmd` | add/add | 3 | +77 / +23 | Igual que el anterior |
| 10 | `papers/camiz_diblasi_2013.qmd` | add/add | 2 | +85 / +23 | Igual que el anterior |
| 11 | `papers/camiz_spada_2024.qmd` | add/add | 2 | +92 / +23 | Igual que el anterior, más el cotejo de F0-5 (año 2023/2024, páginas y DOI) |
| 12 | `papers/purizaca_2023.qmd` | add/add | 2 | +80 / +23 | Igual que `abdi_2010` |
| 13 | `papers/torres_baltazar_2023.qmd` | add/add | 2 | +71 / +23 | Igual que `abdi_2010` |
| 14 | `papers/congreso_2018.qmd` | contenido | 1 | +2/−2 / +1/−1 | Una sola línea, la redacción de D18 («evento peruano» frente a «evento nacional»). Se elige la redacción que fije el bibliotecario, sin pérdida de contenido |
| 15 | `papers/fisher_1958.qmd` | contenido | 2 | +32/−8 / +10/−5 | Comparación de fragmentos por el bibliotecario (F0-6 b) |
| 16 | `papers/horn_1965.qmd` | contenido | 1 | +8/−4 / +1/−1 | Fila «Estado de lectura»: comparación por el bibliotecario (F0-6 b) |

**Diferencia con el plan.** El plan habla de «las 8 *add/add* y `congreso_2018`». `merge-tree` da
6 *add/add* (`abdi_2010`, `camiz_2021_pca`, `camiz_diblasi_2013`, `camiz_spada_2024`,
`purizaca_2023`, `torres_baltazar_2023`) y 3 conflictos de contenido (`congreso_2018`,
`fisher_1958`, `horn_1965`), porque estas tres fichas ya existían en la base. El total sigue siendo
9 fichas y 16 archivos.

**Riesgos de la fusión que no aparecen como conflicto** (para W-2):

- **(a) `data/results/final/avance_resumen.csv`.** Lo agrega `main` sin conflicto, junto con
  `herramientas/resumen_avance.py`. 11 de las 23 claves que solo están en el mapa de `main`
  (`epcaTransicionesSesenta`, `oeFilasPrincipales`, `oeFilasSignificativas`, `oePMin`,
  `hfcReplicas`, `hfcPropAriTres`, `hfcPropAriCuatro`, `hfcAriTresMedia`,
  `hfcCofeneticaMediana`, `datacionFrecMin` y `datacionCorteFrecMin`) leen ese archivo, que se calculó con los resultados de `main`, anteriores a D19 y a los
  cambios de la 3c. Antes de regenerar las cifras hay que ejecutar `herramientas/resumen_avance.py`
  sobre los resultados de la rama, o quitar esas claves del mapa. Si no, entran al
  `_cifras.yml` valores que no salen de `data/results/` vigente.
- **(b) Subcarpetas nuevas en `data/results/final/`.** `main` agrega `mmc102/` (48 CSV),
  `informe_uni/` (15 CSV y 6 PNG) y `R/informe_mmc102_corridas.Rmd`. No entran en conflicto, pero
  después de la fusión `diff -rq data/results/final` dejará de servir como prueba de «no cambia
  nada» si no se excluyen esas carpetas. La comprobación de series excluidas del Rmd final
  (criterio 16) recorre solo los CSV del nivel superior: sí leerá `avance_resumen.csv`, que no
  contiene la serie excluida.
- **(c) Informe en Quarto.** `main` modifica `tesis/_capitulos/00_resumen.qmd` y
  `02_marco_teorico.qmd` (fusión automática, la rama no los tocó), y agrega
  `tesis/informe_mmc102/` y `tesis/informe_preliminar_uni/` con sus `.bib` (F0-6 los inventaría).

## 4. Desviaciones respecto de `decisiones.qmd` y del plan

- **Ninguna desviación metodológica.** F0-3 es un conteo determinista: no tiene nulo, estadístico,
  semilla ni umbral nuevo. Los parámetros son los de D7 (h = 3 y 6) y D17.1 (n_min = 12).
- **Constantes en el Rmd.** El Rmd final no tenía constantes para la tolerancia de D7 (usaba los
  literales 3 y 6). Se definieron una sola vez, con los nombres de `src/episodios.py`, y ahora las
  usan el chunk nuevo y `b6-compatibilidad`, con una comprobación de que valen 3 y 6, porque los
  nombres de columna `compatible_h3`/`h6` dependen de ellas. `R_compatibilidad_cortes.csv` no
  cambia. n_min **no** se fijó de nuevo: se lee de `datar`.
- **Universo «meses de la muestra».** Se tomó el calendario de los datos (228 meses), no el de los
  scores suavizados (217). El plan no lo precisaba: se declara aquí.
- **Cifra de paridad.** `\filasParidad` y `\filasParidadCoinciden` pasan de 57 a 58. Es la única
  cifra existente que cambia, como consecuencia de la fila de paridad pedida. Se usan en
  `tesis_latex/apendices/reproducibilidad.tex:53-54`.
- **Pendiente (4.3).** `requirements.txt` no fija versiones y el contenedor no traía las
  dependencias. Las versiones instaladas hoy (sección 1) reproducen byte a byte todos los CSV
  previos de 09a. Se propone fijarlas en una iteración posterior, para la reproducibilidad del
  asesor.
