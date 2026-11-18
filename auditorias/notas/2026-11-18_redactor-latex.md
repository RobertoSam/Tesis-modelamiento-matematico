# Nota del redactor LaTeX — 18-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `32c7886`. Encargo acotado: aplicar la «Regla para el
redactor» de `auditorias/notas/2026-11-17_bibliotecario.md` (cita de `lahiri_2003` para el
bootstrap por bloques conjunto y de `aue_et_al_2009` en el estado del arte). No se tocaron
`05_resultados.tex`, las cifras, `tesis/referencias.bib`, el informe `tesis/`, `data/`, `src/`,
`R/` ni `notebooks/`.

## Archivos tocados

- `tesis_latex/capitulos/02_estado_arte.tex`
- `tesis_latex/capitulos/03_marco_teorico.tex`
- `tesis_latex/capitulos/07_pendientes.tex`

## Lo redactado y las fuentes por sección

### Cap. 3, introducción de `sec:nulos` (l. ~1465)

- Se actualizó el `\verificar` de `lahiri_2003` a «metadatos verificados; texto leído en parte
  (sec. 2.5 y p. 176) en una copia no oficial; se cita como manual del bootstrap por bloques.».
- El `\verificar` de `kunsch_1989` no cambia.
- Fuente: `papers/lahiri_2003.qmd`.

### Cap. 3, `obs:nulo-estructura`, inciso (d) (l. ~1599)

- Se sustituyó el `\pendiente` por: la descripción del bootstrap de bloques móviles se extiende
  sin cambios a vectores aleatorios, con `\parencite[sec.~2.5, p.~29]{lahiri_2003}` y
  `\verificar{texto leído en parte en una copia no oficial de los caps.~2 y~7; la equivalencia con
  los mismos inicios de bloque es de la tesis.}`.
- Fuera de la cita, como pasos propios de la tesis: que remuestrear bloques del vector
  $\Delta\vx_t$ equivale a usar los mismos inicios para todas las series; la regla de
  $\lceil n'/\Lb\rceil$ inicios (`def:bloques`); y su uso con incrementos de series no
  estacionarias. Se dice de forma explícita que la fuente no se invoca para la validez asintótica
  del caso vectorial. Künsch (1989) no se cita para este punto.
- Fuente: `papers/lahiri_2003.qmd` (sec. 2.5, p. 29, según la nota del bibliotecario).

### Cap. 2, `sec:ea-cambio` (l. ~235)

- Se sustituyó el `\pendiente` por una frase con `\textcite{aue_et_al_2009}` y
  `\verificar{ficha preliminar: solo resumen leído; metadatos en el repositorio institucional y
  arXiv, no en la editorial.}`. Solo se le atribuye un contraste asintótico no paramétrico de la
  estabilidad de las volatilidades y covolatilidades de series multivariadas, aplicable a modelos
  GARCH multivariados y en dimensión alta. No se describe el estadístico ni sus supuestos.
- Se añadió el contraste que la nota declara legítimo: contraste de hipótesis con modelo y teoría
  asintótica, frente a la lectura descriptiva de la tesis con un nulo por remuestreo
  (`\cref{sec:nulos}`).
- Fuente: `papers/aue_et_al_2009.qmd`.

### Cap. 7, `sec:pend-marcas` (l. ~202)

- Se quitó «la del bootstrap por bloques conjunto» de la lista de fuentes sin ficha: quedan
  Denimal (2001) y Camiz y Diblasi (2013). La del cambio en covarianzas no figuraba en la lista.

## Verificación de claves

- `lahiri_2003` existe en `tesis/referencias.bib` (l. 691) y tiene ficha en
  `papers/lahiri_2003.qmd`.
- `aue_et_al_2009` existe en `tesis/referencias.bib` (l. 1150) y tiene ficha en
  `papers/aue_et_al_2009.qmd`.
- Etiquetas y macros usadas: `sec:nulos`, `def:bloques`, `\Lb` y `\vx` existen.

## Conteo de `\pendiente` por archivo (ocurrencias en `tesis_latex/capitulos/`)

| Archivo | Antes | Después |
|---|---|---|
| 02_estado_arte.tex | 5 | 4 |
| 03_marco_teorico.tex | 3 | 2 |
| 04_metodologia.tex | 2 | 2 |
| 05_resultados.tex | 3 | 3 (no tocado) |
| Resto | 0 | 0 |
| **Total** | **13** | **11** |

Los `\verificar` suben en 2 (02: 36 → 37; 03: 38 → 39; el de l. ~1465 se reescribió, no se
añadió). No se cuentan los `\pendiente` que generan `\cifrafalta` o `cifras_stub.tex`.

## Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex` falla por el entorno, antes de procesar los
capítulos y sin producir PDF: no se encuentra el módulo `luaotfload-main` y babel no encuentra
`spanish.ldf`. Problema de entorno ya conocido, no del texto. Comprobación hecha en su lugar:
balance de llaves (02 y 07: 0; 03: +1, igual que en `32c7886`, de modo que las ediciones son
neutras). Falta compilar en un entorno completo antes de la auditoría (biber debe resolver
`aue_et_al_2009`, que se cita por primera vez en la tesis).

## Inconsistencias detectadas

- Ninguna entre código y teoría.

## Qué debe derivar el editor del informe

- `tesis/_capitulos/02_marco_teorico.qmd`, observación sobre los supuestos del nulo: sustituir
  `[CITA PENDIENTE: fuente del bootstrap por bloques conjunto…]` por «(Lahiri, 2003, sec. 2.5,
  p. 29)» con una nota `VERIFICAR` que repita la del `\verificar`, y mantener la equivalencia con
  los mismos inicios como paso de la tesis.
- Si el informe actualiza la nota de `lahiri_2003` en la introducción de los nulos, usar el nuevo
  texto del `\verificar`.
- El informe no tiene marca sobre el cambio en covarianzas; si incorpora la cita de Aue et al.
  (2009), repetir la nota `VERIFICAR` y atribuirle solo lo indicado arriba.
