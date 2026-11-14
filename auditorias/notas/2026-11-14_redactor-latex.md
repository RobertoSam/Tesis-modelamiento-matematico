# Nota del redactor LaTeX — 14-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `675e2e5`. Encargo acotado: aplicar la «Regla para el
redactor» de `auditorias/notas/2026-11-13_bibliotecario.md` y la corrección menor de
`sec:retencion` señalada en `auditorias/notas/2026-11-12_redactor-latex.md`. No se tocaron
`05_resultados.tex`, las cifras, `tesis/referencias.bib` ni el informe `tesis/`.

## Archivos tocados

- `tesis_latex/capitulos/03_marco_teorico.tex`
- `tesis_latex/capitulos/02_estado_arte.tex`
- `tesis_latex/capitulos/07_pendientes.tex`

## Lo redactado y las fuentes por sección

### Cap. 3, `sec:cos2` (Calidad de representación y contribuciones)

- Se sustituyó el `\pendiente` por `\textcite{escofier_pages_2023}`, sin `\verificar`.
- Se le atribuye solo la terminología: «calidad de representación» (coseno cuadrado del ángulo
  entre el elemento y el eje) y «contribución» (a la inercia del eje), para individuos y variables.
- Se dice expresamente que las fórmulas de `def:cos2` (calidad en un plano, normalización de las
  contribuciones) son definiciones de la tesis y no se atribuyen a esa obra.
- Fuente: `papers/escofier_pages_2023.qmd` (FB-106; texto parcial, sección 1.9).

### Cap. 3, `sec:retencion` (Número de componentes)

- «las fuentes están pendientes» → «las fuentes primarias tienen ficha preliminar». Es exacto:
  las citas siguientes (`frontier_1976`, `horn_1965`, `kaiser_1960`, `rencher_christensen_2012`)
  llevan todas un `\verificar` de ficha preliminar.

### Cap. 3, `sec:adecuacion` (KMO)

- Primera opción de la nota del bibliotecario. Se cita `\parencite{guttman_1953}` solo por el
  concepto de anti-imagen (error de la regresión de mínimos cuadrados sobre las demás variables) y
  su cálculo desde la inversa de la matriz de correlaciones, con
  `\verificar{solo resumen consultado; el resumen de Guttman no emplea el término «correlación parcial»}`.
- La coincidencia de $q_{jj'}$ con la correlación parcial dado el resto se presenta como «hecho de
  álgebra, que aquí no se atribuye a esa fuente». No se atribuye a ninguna obra.
- Fuente: `papers/guttman_1953.qmd` (FB-105; ficha preliminar, solo resumen).

### Cap. 2, l. ~291 (escuela francesa)

- Se añadió una frase que remite las ayudas a la interpretación a `\textcite{escofier_pages_2023}`
  y a `sec:cos2`. El `\pendiente` quedó reducido al STATIS dual y a la ponderación gaussiana de
  las ventanas (Camiz y Diblasi, 2013). Se quitó la mención de Lebart, Morineau y Piron (1995)
  como candidato (la nota del bibliotecario la descarta para cos²/contribuciones); su cita de la
  l. 249 como manual de la escuela se mantiene.

### Cap. 7, `sec:pend-marcas`

- La lista de fuentes sin ficha ya no incluye las ayudas a la interpretación; incluye el STATIS
  dual (antes implícito) y se aclara que la igualdad anti-imagen = correlación parcial se presenta
  sin fuente atribuida.

## Verificación de claves

- `guttman_1953` y `escofier_pages_2023` existen en `tesis/referencias.bib` (l. 1114 y 1126) y
  tienen ficha en `papers/`.

## Conteo de `\pendiente` por archivo (ocurrencias en `tesis_latex/capitulos/`)

| Archivo | Antes | Después |
|---|---|---|
| 02_estado_arte.tex | 5 | 5 (el de l. ~291 se mantiene, reducido) |
| 03_marco_teorico.tex | 5 | 3 |
| 04_metodologia.tex | 2 | 2 |
| 05_resultados.tex | 4 | 4 (no tocado) |
| Resto | 0 | 0 |
| **Total** | **16** | **14** |

Más los `\pendiente` que generan `\cifrafalta` o `cifras_stub.tex` al compilar, que no se cuentan aquí.

## Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex` falla por el entorno: `biblatex.sty` no está
instalado (error fatal antes de procesar los capítulos; no se produjo PDF). Problema de entorno
ya conocido, no del texto. Comprobaciones hechas en su lugar: balance de llaves de los tres
archivos (02 y 07: 0; 03: +1 igual que antes del cambio, es decir, las ediciones son neutras);
las etiquetas `sec:cos2` y `def:kmo` existen. Hay que compilar en un entorno completo antes de la
auditoría.

## Inconsistencias detectadas

- Ninguna entre código y teoría. Observación menor: el desbalance de llaves +1 del
  `03_marco_teorico.tex` es previo a este cambio (probablemente un intervalo semiabierto en modo
  matemático o similar); conviene confirmarlo con la compilación completa.
