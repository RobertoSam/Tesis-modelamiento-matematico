# Auditoría · Iteración 3b · Verificación de la vuelta 2 · 31 de octubre de 2026

**Rama:** `iteracion-3b` (HEAD `e6da3a8`, igual a `origin/iteracion-3b`) · **Base de la vuelta:**
`bc17259` (versión del dictamen `auditorias/2026-10-30_iteracion-3b_vuelta1.md`, que auditó `432b1cb`) ·
**Alcance:** `git log bc17259..HEAD`, seis commits:

- `d7302e0` (redactor, M-03), `09b9c26` (editor, M-03) y `636cc70` (bibliotecario, M-03);
- `74a1ac6` y `c40b7bf` (redactor, N-03) y `e6da3a8` (editor, N-03).

**Auditor:** agente auditor (independiente), en la sesión automática de seguimiento diario, sin
Roberto presente. Las notas de los agentes (`auditorias/notas/2026-10-31_*.md`) no se tomaron como
evidencia. Se aplicaron los tamaños de D16 (228 × 16 y 227 × 16).

## Dictamen: **APROBADO**

No hay hallazgos bloqueantes ni mayores. **M-03** y **N-03** quedan **resueltos**. **N-02** y
**N-04** siguen **abiertos** y sin cambios, porque dependen de decisiones de Roberto. Las
comprobaciones de no regresión salen limpias.

| Severidad | N.º | IDs |
|---|---|---|
| Bloqueante | 0 | — |
| Mayor | 0 | — (M-03 resuelto) |
| Menor | 2 (abiertos, decisión de Roberto) | N-02 y N-04 |

## Estado de los hallazgos de la vuelta 1

| ID | Estado | Evidencia (repositorio, no notas) |
|---|---|---|
| M-03 | **Resuelto** | **Tesis:** `tesis_latex/capitulos/02_marco_teorico.tex:222` dice `\parencite{fmi_2015b}\verificar{el DOI corresponde al informe completo (página de publicaciones del FMI) y no se comprobó en doi.org.}`. **Informe:** `tesis/_capitulos/02_marco_teorico.qmd:80` dice `[@fmi_2015b][^v2-fmi]`, y la nota `v2-fmi` (línea 701) da el mismo motivo; el texto aparece en `word/footnotes.xml` de `02_marco_teorico.docx`. **`.bib`:** la entrada `fmi_2015b` conserva su campo `verificar` y su ficha (`papers/fmi_2015b.qmd`). **Conteo propio** con `git grep -o`, sin el guion del bibliotecario: `\verificar{` en `tesis_latex/capitulos/` sube de 52 (`bc17259`) a 53 en `09b9c26` y `HEAD`. Sin el comentario del preámbulo y contando solo los capítulos, da 51 → 52. Las notas `[^…]:` del informe con `VERIFICAR` pasan de 51 a 52, y `[CITA PENDIENTE]` se mantiene en 9. Coincide con la tabla del registro (columna «M-03 (`09b9c26`)»). Los commits posteriores (`74a1ac6` a `e6da3a8`) no cambian el conteo. **Registro:** la fila de `fmi_2015b`, la del episodio de materias primas y la lista de marcas abiertas de episodios están al día. |
| N-03 | **Resuelto** | **Tesis:** las siete macros (`\nuGauss`, `\pasoReglaSeis`, `\ejeReglaSeis`, `\ventanaMediaMovil`, `\clasesHfcMenor`, `\clasesHfcMayor`, `\percentilWalkforward`) se usan en: `def:datacion` (cap. 2); `tab:etapas`, «EPCA en grilla», el título de `tab:kish`, «Regla del 06», `sec:met-hfc`, `sec:met-datacion` y `def:walkforward` (cap. 3); y `notacion.tex`. `cifras_stub.tex` las define con `\providecommand`. **Informe:** las claves de `_cifras.yml` se usan en los lugares equivalentes, también dentro de la fórmula y del nombre de `def-datacion`. Cada uso lleva un comentario que declara el valor provisional. **Búsqueda de residuos** en `tesis_latex/` y `tesis/` con `MM12`, `\nu=3`, `percentil 95`, `(95)`, `3 y 4 clases`, `paso…= 3`, `\ell_0=2` y `12 meses`: no quedan valores escritos a mano. Solo aparecen los usos genéricos de `nsd` y $\nu=0$, que denotan pesos uniformes y no el parámetro. Se conservan como estaban el parámetro atribuido a Atoche y Murrieta, los «pasos 3 y 4» de `alg:aede` y $n_{\min}=12$ (D17.1), y se declaran en `tesis_latex/README.md` y `tesis/README.md`. **Salidas:** en el PDF y en los `.docx` los valores se resuelven a 3, 3, 2, 12, 3, 4 y 95, idénticos a `data/results/final/parametros_diseno.csv`. En los `.docx` no queda ningún *shortcode* sin resolver. Se retiró el «Pendiente» de `tesis_latex/README.md:83`. Los capítulos 4 y 5 no cambian. |
| N-02 | **Abierto** (decisión de Roberto) | Sin cambios en `decisiones.qmd` ni en `papers/` desde `bc17259`. `papers/congreso_2018.qmd:38` sigue diciendo «evento interno». |
| N-04 | **Abierto** (decisión de Roberto) | Sin cambios en `src/`, `R/` ni `decisiones.qmd` desde `bc17259`. La convención de los inicios de bloque de la rama TS sigue sin decidirse. |

## Hallazgos (persistentes)

| ID | Severidad | Archivo:línea | Evidencia | Acción requerida | Responsable |
|---|---|---|---|---|---|
| N-02 | Menor (persistente) | `papers/congreso_2018.qmd:38`; `def:episodio` (`02_marco_teorico.tex`) | Igual que el 29-10 y el 30-10 | Que Roberto decida qué significa «externo» en D7. Después se ajustan la definición (redactor), la ficha y el registro (bibliotecario) y el informe (editor) | Roberto → redactor LaTeX, bibliotecario, editor del informe |
| N-04 | Menor (persistente) | `src/remuestreo.py`; `obs:nulo-mixto` (c) | Igual que el 29-10 y el 30-10 | Que Roberto decida si se corrige el sorteo de la rama TS (Python y R, con paridad) o si se registra como convención en `decisiones.qmd` | Roberto → desarrollador |

No hay hallazgos nuevos.

## Comprobaciones de no regresión

Todas las ejecuciones se hicieron en un clon limpio de `iteracion-3b` (`e6da3a8`) dentro del
*scratchpad* del auditor. El repositorio original no se modificó, salvo este dictamen.

| Paso | Resultado |
|---|---|
| `python3 herramientas/generar_cifras.py --comprobar` | Exit 0 (`cifras.tex` y `_cifras.yml` al día) |
| `python3 herramientas/exportar_parametros_diseno.py --comprobar` | Exit 0 («parametros_diseno.csv al día») |
| `pytest tests/` | **49 passed y 2 skipped**. Los 2 omitidos (`tests/test_coef_rv.py:84`) se deben a que este entorno no tiene `Rscript`; en la vuelta 1, con R instalado, pasaron (51 *passed*). La vuelta no cambia código (`git diff bc17259..HEAD -- src R notebooks herramientas tests` vacío). `statsmodels` se instaló en un entorno virtual del *scratchpad* |
| `latexmk -lualatex -cd tesis_latex/tesis.tex` | Exit 0, **75 páginas**. `tesis.log`: 0 líneas `Warning` (sin citas ni referencias indefinidas) y 0 `Overfull`; `tesis.blg` sin avisos |
| `quarto render tesis/ --to docx` (Quarto 1.10.20) | Exit 0, sin avisos en el log; 9 `.docx`. Ningún `?@clave` ni *shortcode* `meta` sin resolver |
| CSV de `data/results/` | `git diff --name-status bc17259..HEAD -- data/` vacío: ningún CSV cambia. Los 290 versionados siguen igual. Después de los renders, `git status` del clon está limpio |
| Regla 7 | `git diff --stat origin/main..HEAD` sobre `tesis_latex/capitulos/04_resultados.tex` y `tesis/_capitulos/04_resultados.qmd`: vacío |
| Notación | Las entradas de `notacion.tex` que cambiaron (`w_m`, $E^{(q)}_a$) coinciden con el uso de los capítulos 2 y 3 |

## Lo que no se verificó, y por qué

- **Rmd final y paridad Python–R:** no se volvieron a generar, porque este entorno no tiene R y la
  vuelta no cambia código, datos ni el Rmd. La vuelta 1 los verificó sobre el mismo código (exit 0;
  290/290 CSV idénticos).
- **Notebooks:** no se ejecutaron, porque la vuelta no los toca.
- **DOI de `fmi_2015b` en doi.org:** no se comprobó. La marca queda abierta a propósito y así figura
  en el registro.
- **Contenido de las fuentes:** solo se contrastó con las fichas.
- **Sitio completo y `quarto publish`:** quedan fuera del alcance.

## Para el orquestador

- Esta es la última vuelta permitida. No queda ningún hallazgo bloqueante ni mayor, de modo que no hay
  nada que escalar por esa vía. Los dos menores abiertos ya eran decisiones de Roberto.
- La definición del auditor (`.claude/agents/auditor.md`) sigue usando 228 × 17 y 227 × 17. Desde
  D16 son 228 × 16 y 227 × 16, y este dictamen aplicó D16.

## Lo que queda para Roberto

1. **Conforme de la iteración 3b** («conforme iteración 3b»). El dictamen es APROBADO.
2. **N-02:** decidir qué significa «evento externo» en D7 y en `def:episodio`.
3. **N-04:** decidir si se corrige el sorteo de los inicios de bloque de la rama TS del nulo mixto o
   si se registra como convención.
4. **N-01 (pendiente operativo):** crear y subir el tag `v0.4-17series-dos-vias` sobre `2be3665`.
5. **Parámetros provisionales:** decidir si los siete parámetros de `parametros_diseno.csv` pasan a
   `decisiones.qmd`. Hoy el texto los toma por macro y los declara provisionales.
6. **Regla 7:** este dictamen no autoriza a publicar el capítulo de resultados.
