# Auditoría · Iteración 3b · Verificación de la vuelta 1 · 30 de octubre de 2026

**Rama:** `iteracion-3b` (HEAD `432b1cb`, igual a `origin/iteracion-3b`) · **Base de la vuelta:**
`e97530c` (dictamen `auditorias/2026-10-29_iteracion-3b.md`) · **Alcance:** `git log e97530c..HEAD`,
cuatro commits: `ea4a71d` (bibliotecario, M-01), `5568f90` (desarrollador, M-02), `de55e86`
(desarrollador, N-01) y `432b1cb` (desarrollador, N-03) · **Auditor:** agente auditor
(independiente), sesión automática de seguimiento diario, sin Roberto presente.

## Dictamen: **APROBADO**, con observaciones

No hay hallazgos bloqueantes. M-01, M-02 y N-01 quedan **resueltos**. N-03 queda **resuelto en la
parte del desarrollador**: falta que el redactor sustituya los valores escritos a mano por las
macros nuevas. N-02 y N-04 siguen **abiertos**, como se esperaba, porque dependen de decisiones de
Roberto.

Las comprobaciones de no regresión salen limpias:

- `generar_cifras.py --comprobar` y `exportar_parametros_diseno.py --comprobar` terminan con exit 0;
- pytest da 51 *passed*;
- LaTeX compila: 75 páginas y 0 avisos;
- Quarto genera el `.docx` con exit 0;
- el Rmd final se genera con exit 0 en sus dos versiones;
- los 290 CSV de `data/results/` son idénticos byte a byte a los versionados, y ninguno de los 289
  previos cambió;
- la regla 7 se cumple.

Hay **un hallazgo mayor nuevo**, M-03. No lo introdujo la vuelta: la auditoría del 29-10 no lo
detectó, y el registro de verificación lo señala ahora. Se trata de `fmi_2015b`, que se cita en la
tesis y en el informe sin marca, aunque su DOI está pendiente en la ficha y en el `.bib`. Se corrige
en una línea en cada documento.

| Severidad | N.º | IDs |
|---|---|---|
| Bloqueante | 0 | — |
| Mayor | 1 (nuevo) | M-03 |
| Menor | 3 (abiertos) | N-02 y N-04 (decisión de Roberto); N-03 (resto para el redactor) |

## Estado de los hallazgos del 29-10-2026

| ID | Estado | Evidencia (repositorio, no notas) |
|---|---|---|
| M-01 | **Resuelto** | Rehice el conteo con `git grep -o` en `4624802`, `d1bf179`, `e97530c` y `HEAD`, y da exactamente la tabla «Conteo de marcas abiertas» del registro: `\verificar` 34 → 51; `\pendiente` 22 → 14; notas `VERIFICAR` del informe 34 → 51; `[CITA PENDIENTE]` 18 → 9; RmdF 25; Rmd de exploración 38; `src` 6; NB05 3; `06a`/`06b` 10; `modelos_dl.py` 0. Cada uno de los 14 `\pendiente` de la tesis tiene su fila: portada, Frontier (×2), cos², anti-imagen, Denimal 2001, Camiz y Diblasi, *bootstrap* conjunto, `sec:met-vias`, Said y Dickey, Kwiatkowski, AE/LSTM con 16 series y caps. 4 y 5. Las 25 marcas del Rmd final (`R/ciclo_financiero_final.Rmd`, ahora registrado como «RmdF») corresponden a las 15 filas que enumera el registro. Los 6 `VERIFICAR` de `src/` también tienen fila. La sección de episodios está al día tras D9/L1: dos `\verificar` de contenido, sin `\pendiente`. La tabla de marcas no bibliográficas incluye `sec:met-vias` y AE/LSTM, y cierra «cap. 3 por redactar». Las 56 claves citadas en la tesis tienen entrada en el `.bib`, ficha y, si llevan el campo `verificar`, fila en el registro (comprobación con guion propio). |
| M-02 | **Resuelto** | `herramientas/cifras_mapa.csv` ya no tiene ninguna ruta fuera de `data/results/final/` y `data/referencia/`, y `generar_cifras.py:49,155` rechaza cualquier otra (`CARPETAS_ADMITIDAS`). Se retiraron 14 macros y ninguna se usa en `tesis_latex/` ni en `tesis/`. Recalculé de forma independiente, con el dataset de niveles menos el crédito total del SF, el IPC subyacente y la Liquidez M2 (228 × 16): PC1 = 65,2 %, PC2 = 19,4 % y 3 valores propios > 1. Coinciden con `\inerciaPCUnoNiveles`, `\inerciaPCDosNiveles` y `\kaiserNiveles`. Además, `\nSeriesTS`/`\nSeriesDS`/`\nSeriesIndeterminadas` = 1/12/3, que suman 16 = `\nSeries`, como en `final/05_clasificacion_d5_resumen.csv`, y `\kmoGlobalNiveles` = 0,84, como en `final/05_adecuacion.csv`. |
| N-01 | **Resuelto** | El tag sigue sin existir (`git tag -l` y `git ls-remote --tags origin`: solo `v0.1-transformadas` y `v0.2-niveles`). Pero todos los lugares citados remiten ahora al commit `2be3665`, que es ancestro de `HEAD`, y declaran el tag como pendiente: `data/results/LEEME.md:11-13`, `data/results/niveles/LEEME.md:10-11`, `R/ciclo_financiero_final.Rmd:109, 1064`, `notebooks/modelos_dl.py:533-534`, `src/datos.py:17`, `src/parametros.py:5` y una celda *markdown* del notebook 05. La creación del tag queda para Roberto. |
| N-02 | **Abierto** (decisión de Roberto) | Sin cambios en `decisiones.qmd`, `papers/`, `tesis_latex/capitulos/` ni `tesis/_capitulos/` desde `e97530c`. `papers/congreso_2018.qmd:38` sigue diciendo «evento interno». El registro lo deja declarado como abierto en las filas de Kuczynski y COVID-19. |
| N-03 | **Resuelto en parte** | `data/results/final/parametros_diseno.csv` (7 filas) lo genera `herramientas/exportar_parametros_diseno.py`, que no fija valores: los extrae del código de Python y del Rmd final, y exige que coincidan. `--comprobar` da «al día». Las 7 macros (`\nuGauss`, `\pasoReglaSeis`, `\ejeReglaSeis`, `\ventanaMediaMovil`, `\clasesHfcMenor`, `\clasesHfcMayor`, `\percentilWalkforward`) están en `cifras.tex`. **Falta:** ningún capítulo las usa todavía (0 usos en `tesis_latex/capitulos/` y en `tesis/_capitulos/`), y `tesis_latex/README.md:83` lo deja como pendiente del redactor. El CSV marca los valores como «provisional», porque no están en `decisiones.qmd`. |
| N-04 | **Abierto** (decisión de Roberto) | `src/remuestreo.py` y `R/07b_nulo_estructura.R` no cambian, y `decisiones.qmd` tampoco. La convención de inicios de bloque de la rama TS sigue sin decidirse. |

## Hallazgos (nuevos o persistentes)

| ID | Severidad | Archivo:línea | Evidencia | Acción requerida | Responsable |
|---|---|---|---|---|---|
| M-03 | Mayor (nuevo; no detectado el 29-10) | `tesis_latex/capitulos/02_marco_teorico.tex:222`; `tesis/_capitulos/02_marco_teorico.qmd:80`; `tesis/referencias.bib` (entrada `fmi_2015b`) | La entrada del `.bib` tiene el campo `verificar = {VERIFICAR: el DOI es del informe completo (página de publicaciones del FMI) y no se comprobó en doi.org}`, y el registro (fila `fmi_2015b`) lo confirma. Aun así, la tesis cita `\parencite{fmi_2015b}` sin `\verificar` y el informe cita `[@fmi_2015b]` sin nota `VERIFICAR`. Incumple el punto A.4: toda verificación pendiente se marca en el texto. El registro ya lo advierte («falta la marca de `fmi_2015b`»), pero el texto sigue sin la marca. | Añadir `\verificar{DOI del informe completo sin comprobar en doi.org}` en la tesis y la nota `VERIFICAR` equivalente en el informe; actualizar después el conteo del registro (51 → 52 en los dos documentos). | Redactor LaTeX (tesis); editor del informe (informe); bibliotecario (conteo del registro) |
| N-03 | Menor (persistente, resto) | `tesis_latex/README.md:83`; capítulos 2 y 3 de la tesis y del informe | Las macros de los seis parámetros de diseño existen, pero el texto sigue escribiendo a mano ν = 3, paso 3, eje 2, 12 meses, 3 y 4 clases y percentil 95. | Sustituir esos valores por las macros de `cifras.tex` y `_cifras.yml`, y retirar el «Pendiente» del README. | Redactor LaTeX; editor del informe |
| N-02 | Menor (persistente) | `papers/congreso_2018.qmd:38`; `def:episodio` (`02_marco_teorico.tex`) | Igual que el 29-10. | Que Roberto decida qué significa «externo». Después: definición (redactor), fichas y registro (bibliotecario) e informe (editor). | Roberto → redactor LaTeX, bibliotecario, editor del informe |
| N-04 | Menor (persistente) | `src/remuestreo.py`; `obs:nulo-mixto` (c) | Igual que el 29-10. | Que Roberto decida si se corrige el sorteo de la rama TS (Python y R, con paridad) o se registra como convención en `decisiones.qmd`. | Roberto → desarrollador |

## Comprobaciones de no regresión

Todas las ejecuciones se hicieron en un clon limpio de `iteracion-3b` (`432b1cb`) dentro del
*scratchpad* del auditor. El repositorio original no se modificó, salvo este dictamen.

| Paso | Resultado |
|---|---|
| `python3 herramientas/generar_cifras.py --comprobar` | Exit 0 |
| `python3 herramientas/exportar_parametros_diseno.py --comprobar` | Exit 0 («parametros_diseno.csv al día») |
| `pytest tests/` | **51 passed** (9,0 s). En el entorno de sistema faltaba `statsmodels` (2 errores de recolección), que se instaló en un entorno virtual del *scratchpad*; es un problema del entorno, no del material. |
| `latexmk -lualatex -cd tesis_latex/tesis.tex` | Exit 0, **75 páginas**, 0 líneas `Warning` en `tesis.log` (citas, referencias y fuentes), 0 `Overfull`, `tesis.blg` sin avisos. El primer intento falló por falta de `biblatex.sty` en el entorno; se instalaron `texlive-bibtex-extra`, `biber`, `lmodern` y `texlive-luatex`, y se repitió sobre el clon limpio (`git clean -fdx tesis_latex`). |
| `quarto render tesis/ --to docx` (Quarto 1.10.20, `quarto-cli` de PyPI) | Exit 0, 9 de 9 archivos, sin avisos en el log. En ningún `.docx` quedan `?@clave` ni *shortcodes* `meta` sin resolver. |
| `rmarkdown::render('R/ciclo_financiero_final.Rmd')` (R 4.3.3, paquetes `r-cran-*` de Ubuntu instalados en la sesión) | Exit 0 con `version_asesor = FALSE` (3 min) y con `TRUE`. 0 `Warning`/`Error` en los logs y 0 bloques `## Warning`/`## Error` en los HTML. |
| CSV de `data/results/` tras generar el Rmd | 39 CSV reescritos por R; **290 de 290** idénticos (md5) a los del repositorio |
| CSV existentes | `git diff --name-status e97530c..HEAD -- data/` solo da `A final/parametros_diseno.csv` y `M` en los dos `LEEME.md`; ningún CSV previo cambia. `git diff 2be3665 HEAD -- data/results ':!data/results/final'` solo toca los dos `LEEME.md` (criterio 17 de la adenda). |
| Regla 7 | `git diff --stat origin/main..HEAD` sobre `04_resultados.tex` y `04_resultados.qmd`: vacío. Ningún capítulo cambia en la vuelta. |

## Lo que no se verificó, y por qué

- **Notebooks.** No se volvieron a ejecutar: la vuelta no cambia código ejecutable. En `05_pca.ipynb`
  cambia una celda *markdown* (texto del tag) y en `modelos_dl.py`, un comentario. Los CSV que
  producen siguen idénticos.
- **Notebooks 08/09 y `modelos_dl.py`.** Requieren `torch`, que sigue ausente.
- **Rmd de exploración.** No se volvió a generar: no cambia en la vuelta.
- **Contenido de las fuentes.** Se contrastó contra las fichas; no hay acceso a los originales.
- **Lectura de las 176 filas del registro una a una.** Se comprobaron los conteos, la cobertura de
  cada `\pendiente`, de las 25 marcas del RmdF y de las de `src/`, y la correspondencia de las 56
  claves citadas. No se revisó la redacción de cada celda.
- **Sitio completo** (`quarto render` en la raíz) y `quarto publish`: fuera del alcance.

## Para el orquestador

1. **M-03** es mayor según la clasificación. Requiere una línea en la tesis, otra en el informe y el
   ajuste del conteo del registro. Puede entrar en la vuelta 2, que es la última permitida antes de
   escalar, junto con el resto de N-03 (redactor y editor). No bloquea el dictamen.
2. La definición del auditor (`.claude/agents/auditor.md:50-51`) sigue tomando 228 × 17 y 227 × 17
   como tamaños de referencia. Desde D16 son 228 × 16 y 227 × 16. Este dictamen aplicó D16.

## Lo que queda para Roberto

1. **Conforme de la iteración 3b.** El dictamen es APROBADO. Si decide corregir M-03 antes, basta la
   vuelta 2 indicada arriba.
2. **N-02:** decidir qué significa «evento externo» en D7 y en `def:episodio`: externo al análisis
   (compatible con la regla 6) o extranjero. De eso dependen la ficha `congreso_2018` y la lectura de
   `pcm_2020`.
3. **N-04:** decidir si se corrige el sorteo de inicios de bloque de la rama TS del nulo mixto o si
   se registra como convención en `decisiones.qmd`.
4. **N-01:** crear y subir el tag `v0.4-17series-dos-vias` sobre `2be3665` desde un equipo con
   permiso (desde aquí no se pueden subir tags).
5. **Parámetros provisionales:** decidir si los seis parámetros de `parametros_diseno.csv` (ν = 3,
   paso 3, eje 2, MM12, 3 y 4 clases, percentil 95) pasan a `decisiones.qmd`.
6. **Fuera de la auditoría:**
   - la reunión con el Dr. Camiz sobre la Parte C («Qué vía mide qué»);
   - pedirle la referencia de Camiz y Diblasi (2013);
   - la página de Kish (1965).
7. **Regla 7:** este dictamen no autoriza a publicar resultados.
