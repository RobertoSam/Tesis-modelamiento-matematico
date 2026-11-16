# Nota del redactor LaTeX — 16-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `6518536`. Encargo acotado: aplicar la «Regla para el
redactor» de `auditorias/notas/2026-11-15_bibliotecario.md` (cita de `lavit_et_al_1994` para el
STATIS dual). No se tocaron `05_resultados.tex`, las cifras, `tesis/referencias.bib` ni el
informe `tesis/`.

## Archivos tocados

- `tesis_latex/capitulos/02_estado_arte.tex`
- `tesis_latex/capitulos/03_marco_teorico.tex`
- `tesis_latex/capitulos/07_pendientes.tex`

## Lo redactado y las fuentes por sección

### Cap. 2, análisis evolutivo (l. ~275)

- Tras «lo combinan con el STATIS dual» se añadió que el método compara varias tablas con las
  mismas variables, observadas en grupos distintos de observaciones, a partir de sus matrices de
  covarianzas, con `\parencite{lavit_et_al_1994}` y
  `\verificar{número del fascículo y DOI sin ver en la editorial; texto leído en parte (resumen e introducción)}`.
- La equivalencia «con series estandarizadas, esas matrices son de correlación» se redacta como
  paso propio de la tesis, fuera de la cita, tal como pide la nota del bibliotecario. La frase
  sobre los años de quiebre coherentes con el EPCA sigue atribuida a Camiz, Maulucci y Roig (2010).
- No se atribuyen al artículo fórmulas ni pasos del método.
- Fuente: `papers/lavit_et_al_1994.qmd`.

### Cap. 2, cierre de la sección de la escuela francesa (l. ~294)

- Se dividió la marca: el STATIS dual queda citado (arriba) y el `\pendiente` se reduce a
  `\pendiente{Camiz y Diblasi (2013), fuente de la ponderación gaussiana de las ventanas: sin ficha}`.

### Cap. 3, EPCA (l. ~885)

- Se añadió `\parencite{lavit_et_al_1994}` con el mismo `\verificar` junto a «el análisis STATIS
  dual». La frase sigue describiendo lo que hacen Camiz, Maulucci y Roig (2010) con el método; a
  Lavit et al. (1994) solo se le atribuye el método.
- No se tocaron las l. ~609 (Denimal, 2001), ~778 (Camiz y Diblasi, 2013) ni ~1599 (bootstrap por
  bloques conjunto): sus `\pendiente` siguen.

### Cap. 7, `sec:pend-marcas` (l. ~202)

- Se quitó «la del STATIS dual» de la lista de fuentes sin ficha: quedan Denimal (2001), Camiz y
  Diblasi (2013) y la del bootstrap por bloques conjunto.

## Verificación de claves

- `lavit_et_al_1994` existe en `tesis/referencias.bib` (l. 1138) y tiene ficha en
  `papers/lavit_et_al_1994.qmd`.

## Conteo de `\pendiente` por archivo (ocurrencias en `tesis_latex/capitulos/`)

| Archivo | Antes | Después |
|---|---|---|
| 02_estado_arte.tex | 5 | 5 (el de l. ~294 se mantiene, reducido a Camiz y Diblasi) |
| 03_marco_teorico.tex | 3 | 3 |
| 04_metodologia.tex | 2 | 2 |
| 05_resultados.tex | 3 | 3 (no tocado) |
| Resto | 0 | 0 |
| **Total** | **13** | **13** |

El total no baja porque la marca del STATIS dual compartía `\pendiente` con la ponderación
gaussiana; se cierra una fuente, no una marca. Los `\verificar` suben en 2 (uno en el cap. 2 y
otro en el cap. 3). No se cuentan los `\pendiente` que generan `\cifrafalta` o `cifras_stub.tex`.

## Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex` falla por el entorno: babel no encuentra
`spanish.ldf` (error en `babel.sty`, antes de procesar los capítulos; no se produjo PDF).
Problema de entorno ya conocido, no del texto. Comprobaciones hechas en su lugar: balance de
llaves (02 y 07: 0; 03: +1, igual que en `6518536`, de modo que las ediciones son neutras).
Falta compilar en un entorno completo antes de la auditoría (biber debe resolver
`lavit_et_al_1994`).

## Inconsistencias detectadas

- Ninguna entre código y teoría.
- Observación: el informe no cita aún el STATIS dual con Lavit et al. (1994); si el editor lo
  incorpora, la nota `VERIFICAR` debe repetir la del `\verificar`.
