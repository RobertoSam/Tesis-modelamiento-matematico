# Nota del desarrollador · 30-oct-2026 · vuelta 1 de la auditoría 3b (N-01 y N-03)

Sesión automática de seguimiento diario, en la rama `iteracion-3b`. Se atienden los hallazgos menores
N-01 y N-03 de `auditorias/2026-10-29_iteracion-3b.md`. **N-02 y N-04 no se tratan**: N-02
corresponde al redactor, al bibliotecario y al editor; N-04 requiere una decisión de Roberto
(corregir el sorteo de la rama TS del nulo mixto o declararlo como convención). No se re-ejecutó
ningún notebook ni el Rmd, y ningún CSV existente de `data/results/` cambió. El capítulo de
resultados (`04_resultados.*`) no se tocó.

## N-01 · Tag `v0.4-17series-dos-vias` inexistente

**Qué cambió.** El tag no existe (`git tag -l`: solo `v0.1-transformadas` y `v0.2-niveles`). El
commit sí existe: `git cat-file -t 2be3665` devuelve `commit`
(`2be36659193934cca7b81b5452fa15a256703669`, 26-oct-2026, «Decisiones D15 … y D16 …»). No se creó
ni se subió ningún tag. La remisión al tag se sustituyó por la remisión al commit `2be3665`, con la
mención de que **el tag queda pendiente de crear por Roberto**, en:

| Archivo | Lugar | Tipo de cambio |
|---|---|---|
| `data/results/LEEME.md` | línea 11 | texto |
| `data/results/niveles/LEEME.md` | línea 10 | texto |
| `R/ciclo_financiero_final.Rmd` | líneas 109 y 1063 (prosa; la segunda dentro de un recuadro `.pregunta`) | solo texto, fuera de los chunks |
| `notebooks/modelos_dl.py` | comentario de la línea 533 | comentario |

Además, por coherencia, en tres lugares con la misma remisión que el dictamen no lista:
`src/parametros.py` (docstring), `src/datos.py` (docstring) y `notebooks/05_pca.ipynb` (celda
Markdown de la cabecera; se editó solo el texto fuente de esa celda, sin tocar salidas). No se tocó
`linea_temporal.qmd` (su línea 45 deja la subida del tag como pendiente) ni los documentos
históricos (`asesoria/`, `auditorias/`).

**Comprobación.** `python3 -m py_compile src/datos.py src/parametros.py notebooks/modelos_dl.py`:
sin errores; el `.ipynb` sigue siendo JSON válido. **El Rmd no pudo renderizarse:** en el entorno de
esta sesión no hay R (`which Rscript` no devuelve nada). El cambio es solo de prosa fuera de los
chunks, de modo que no afecta a la ejecución; conviene que el auditor confirme el render en la
vuelta.

**Pendiente para Roberto:** crear y subir el tag desde un entorno con permiso
(`git tag v0.4-17series-dos-vias 2be3665` y `git push origin v0.4-17series-dos-vias`). Cuando
exista, puede restituirse la remisión al tag en esos lugares.

## N-03 · Parámetros de diseño provisionales a CSV y macros

**Archivos creados.**

- `herramientas/exportar_parametros_diseno.py` (comentado en español). **No fija valores:** lee
  cada parámetro, con una expresión regular que debe coincidir exactamente una vez, del código
  vigente en Python, y lo contrasta con el mismo parámetro en `R/ciclo_financiero_final.Rmd`. Si el
  patrón no aparece una sola vez o Python y R no coinciden, se detiene sin escribir. Es idempotente
  y tiene `--comprobar`.
- `data/results/final/parametros_diseno.csv`: 7 filas (los seis parámetros; las particiones de la
  HFC ocupan dos filas). Columnas: `parametro, simbolo, valor, unidad, descripcion, codigo_python,
  codigo_r, fuente, estado`. La columna `estado` dice para todas «provisional: fijado en el plan 3b
  o en el código previo; no figura en decisiones.qmd».

**Valores exportados (ninguno cambió).**

| Fila (`parametro`) | `valor` | Código Python | Código R | Fuente documental (columna `fuente`) |
|---|---|---|---|---|
| `nu_pesos_gaussianos` | 3 | `notebooks/06c_aede_grilla.ipynb` (`PESOS`) | `pesos_grilla` | plan 3b, tarea D4 del desarrollador |
| `paso_regla06` | 3 | `notebooks/06_epca.ipynb` (`PASO`) | `PASO <- 3` | código previo a 3b (notebook 06) |
| `eje_regla06_niveles` | 2 | `notebooks/06_epca.ipynb` (`corridas06`, índice 1 + 1) | `regla06_grilla(X, fechas, 2)` | código previo a 3b (notebook 06, PC2 en niveles) |
| `ventana_media_movil` | 12 | `notebooks/09a_datacion_pca.ipynb` (`L_MM`) | `L_mm <- 12` | plan 3b, tareas D3 y D12; antes, notebook 09 |
| `clases_hfc_menor` | 3 | `notebooks/07c_hfc_clases.ipynb` (`for ncl in (3, 4)`) | `for (ncl in 3:4)` | plan 3b, tarea D8 |
| `clases_hfc_mayor` | 4 | ídem | ídem | plan 3b, tarea D8 |
| `percentil_walkforward` | 95 | `src/deteccion.py` (`error_walkforward_pca`) | `quantile(…, 0.95)` | código previo a 3b (notebook 09) |

Interpretación: el CSV solo da trazabilidad a valores de diseño fijados antes de calcular. No es
un resultado ni sustituye una decisión. Duda abierta para Roberto: ¿se registran como decisión en
`decisiones.qmd` (la otra opción que propone el dictamen) o basta con el CSV? Es una propuesta; no
se tomó ninguna decisión metodológica.

**Macros nuevas** en `herramientas/cifras_mapa.csv` (7 filas, todas con `parametro=…`, columna
`valor`, formato `entero`): `\nuGauss` (3), `\pasoReglaSeis` (3), `\ejeReglaSeis` (2),
`\ventanaMediaMovil` (12), `\clasesHfcMenor` (3), `\clasesHfcMayor` (4) y
`\percentilWalkforward` (95). `tesis_latex/cifras.tex` y `tesis/_cifras.yml` se regeneraron: 71
cifras.

**Otros archivos modificados.** `tesis_latex/README.md`: la clase «Parámetros de diseño del plan
(provisional)» ahora remite al CSV y a las macros, y el pendiente pasa al redactor (sustituir los
valores escritos a mano). `herramientas/README.md`: sección del nuevo script.

**Dónde están hoy esos números escritos a mano** (para el redactor; no los toqué):

- Tesis LaTeX:
  - `tesis_latex/capitulos/03_metodologia.tex`: línea 121 (tabla: «Particiones en 3 y 4 clases»);
    182, 183 y 197 ($\nu=3$; la 197 es el pie de la tabla de Kish); 216 (paso $\paso=3$ y eje
    $\ell_0=2$); 242 («se corta en 3 y en 4 clases»); 260 y 261 («media móvil causal de 12
    meses», PCA-MM12); 291 y 292 ($E^{(95)}_a$, «percentil 95»).
  - `tesis_latex/capitulos/02_marco_teorico.tex`: 1262 y siguientes (`def:datacion`, título
    «PCA-MM12»; en la definición la ventana es simbólica, $w_{\mathrm m}$).
  - El nombre «PCA-MM12» es una etiqueta. Cabe decidir si se deja como identificador.
- Informe (para el editor): `tesis/_capitulos/03_metodologia.qmd`, líneas 60, 102, 106, 117, 121 y
  132 (en Quarto: `{{< meta cifras.<macro> >}}`).

## Comandos ejecutados

```
git cat-file -t 2be3665
python3 herramientas/exportar_parametros_diseno.py
python3 herramientas/exportar_parametros_diseno.py --comprobar      # exit 0
python3 herramientas/generar_cifras.py                               # 71 cifras
python3 herramientas/generar_cifras.py --comprobar                   # exit 0
python3 -m pytest -q tests/ --ignore=tests/test_nulo_estructura.py --ignore=tests/test_nulo_mixto.py
```

`pytest`: 39 passed y 2 skipped. Los dos módulos excluidos no se pueden importar en este entorno
porque falta `statsmodels`; en `HEAD` falla igual, así que no se debe a estos cambios. Los 2 skipped
dependen de R, que no está instalado.

## Limitaciones del entorno de esta sesión (declaradas)

- **Sin R:** el Rmd no se renderizó (N-01 solo cambia prosa).
- **LaTeX:** `latexmk` sobre una copia en el scratchpad falla por un motivo ajeno a estos cambios:
  falta `spanish.ldf` de babel (`Unknown option 'spanish'`). En el entorno del auditor la tesis
  compilaba. Las siete macros nuevas se probaron en un documento mínimo con `lualatex` (exit 0, sin
  errores) y no chocan con ninguna macro de `preambulo.tex` ni de `notacion.tex`. Como ningún
  capítulo las usa todavía, la tesis no cambia.

## Desviaciones respecto de `decisiones.qmd`

Ninguna. Los seis parámetros siguen fuera de `decisiones.qmd`, como estaban. Su registro como
decisión queda como propuesta para Roberto.
