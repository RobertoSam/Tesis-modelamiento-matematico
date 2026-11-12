# Nota del redactor LaTeX — 12-nov-2026 (iteración 3c, seguimiento diario)

## Qué cambió

Cierre de los `\pendiente` de las dos obras que el bibliotecario fichó el 11-nov-2026
(`auditorias/notas/2026-11-11_bibliotecario.md`, «Regla para el redactor»):

- `tesis_latex/capitulos/04_metodologia.tex`, `sec:met-diagnostico` (≈ l. 148–153): el `\pendiente`
  se sustituye por `\textcite{said_dickey_1984}`, **sin `\verificar`**, atribuyéndole solo la
  versión aumentada de la prueba (aproximación de un ARMA de orden desconocido por una
  autorregresión). El texto declara de forma explícita que la regla de elección de rezagos y los
  valores críticos que reporta el programa son los del código y no se atribuyen a esa obra. La
  remisión de la KPSS a `\textcite{kwiatkowski_et_al_1992}` pasa a una oración propia.
- `tesis_latex/capitulos/01_introduccion.tex`, `oe:dimension` (≈ l. 109–111):
  `\textcite{frontier_1976}` con `\verificar{ficha preliminar: texto no consultado; correspondencia
  con la ref. [10] de Camiz y Pillar (2018) no cotejada}`, citada solo como la obra que compara el
  decrecimiento de los valores propios de un PCA con el modelo de la vara quebrada.
- `tesis_latex/capitulos/03_marco_teorico.tex`, `sec:retencion`, `def:retencion`(a) (≈ l. 483–487):
  misma cita y misma `\verificar`, con el mismo alcance. Se añade que la formulación de
  $\beta_\ell$ y la regla de retención son las de la tesis, apoyadas en
  `\textcite{camiz_pillar_2018}`, no en Frontier.
- `tesis_latex/capitulos/07_pendientes.tex` (l. 201–203): se quitan Frontier (1976) y Said y Dickey
  (1984) de la lista de fuentes sin ficha. Se añade a esa lista la fuente del bootstrap por bloques
  conjunto, que tenía `\pendiente` en el cap. 3 (`obs:nulo-estructura`, l. ~1595) y no figuraba en
  ella.

No se tocó `05_resultados.tex`, ninguna cifra, ni `tesis/referencias.bib`, ni el informe `tesis/`.

## Fuentes por sección

- `sec:met-diagnostico`: `dickey_fuller_1979` (sin cambios), `said_dickey_1984` (ficha completa),
  `kwiatkowski_et_al_1992` (sin cambios).
- `oe:dimension` y `sec:retencion`: `camiz_pillar_2018` (sin cambios), `horn_1965` (sin cambios),
  `frontier_1976` (ficha preliminar, con `\verificar`).

## Cómo se verificó

- `said_dickey_1984` y `frontier_1976` existen en `tesis/referencias.bib` (l. 1086 y 1097) y tienen
  ficha en `papers/` (`said_dickey_1984.qmd`, `frontier_1976.qmd`).
- Llaves balanceadas en los cuatro archivos editados. El contador simple marca +1 en
  `03_marco_teorico.tex`, igual que en `HEAD`: es un falso positivo por `\texorpdfstring{\\}{}`
  (l. ~1679), no un desbalance real.
- `latexmk -lualatex -cd tesis_latex/tesis.tex` **no compila en este entorno**, por la misma causa
  registrada el 10-nov: babel no encuentra `spanish.ldf` («Unknown option 'spanish'») y `biber` no
  está instalado. No lo introduce esta edición. No se generó PDF; queda por compilar en un entorno
  completo.

## `\pendiente` que quedan (conteo por archivo tras la edición)

01: 0 · 02: 5 · 03: 5 · 04: 2 · 05: 3 (resto: 0). Total 15 (antes 18). Siguen abiertos, entre
otros, Denimal (2001), Camiz y Diblasi (2013), el bootstrap por bloques conjunto y las fuentes de
las ayudas a la interpretación.

## Inconsistencias detectadas

- Menor, de redacción (no se corrigió para no ampliar el alcance): en `sec:retencion` (cap. 3,
  l. ~479) la frase «las fuentes están pendientes» ya no es exacta, pues los dos criterios tienen
  ahora cita (Horn y Frontier, ambas con ficha preliminar, y Camiz y Pillar 2018). Se propone
  sustituirla por «las fuentes primarias tienen ficha preliminar» en la próxima pasada.
- Ninguna inconsistencia entre código y teoría.
