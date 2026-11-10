# Nota del redactor LaTeX — 10-nov-2026 (iteración 3c, seguimiento diario)

## Qué cambió

Cierre de los `\pendiente` de las cuatro obras que el bibliotecario fichó el 9-nov-2026
(`auditorias/notas/2026-11-09_bibliotecario.md`, «Regla para el redactor»):

- `tesis_latex/capitulos/02_estado_arte.tex`, `sec:ea-ciclo` (≈ l. 110–116): el `\pendiente` se
  sustituye por un párrafo que cita `\textcite{bry_boschan_1971}` (algoritmo de datación por etapas
  con reglas de duración mínima, **sin cifras**), `\textcite{harding_pagan_2006}` (medición y pruebas
  de sincronización; junto con `harding_pagan_2002` como «literatura de la concordancia», **sin
  atribuir a ninguna la definición del índice**) y `\textcite{christiano_fitzgerald_2003}` (solo
  como filtro pasa-banda de muestra finita, en contraste con la vía exploratoria, que no impone una
  banda).
- `02_estado_arte.tex`, `sec:ea-regimenes` (≈ l. 168): KPSS citada con
  `\parencite{kwiatkowski_et_al_1992}`, solo por la nula de estacionariedad.
- `tesis_latex/capitulos/04_metodologia.tex`, `sec:met-diagnostico` (l. 151):
  `\textcite{kwiatkowski_et_al_1992}` (APA: «Kwiatkowski et al.», cuatro autores).
- `tesis_latex/capitulos/07_pendientes.tex` (l. 200–203): se quitan las cuatro obras de la lista de
  fuentes sin ficha y se añade Said y Dickey (1984), que ya tenía `\pendiente` en el cap. 4 y no
  figuraba en la lista.

No se tocó `05_resultados.tex`, ninguna cifra, ni el `.bib`.

## Cómo se verificó

- Las cinco claves usadas existen en `tesis/referencias.bib` y tienen ficha en `papers/`.
- Llaves balanceadas en los tres archivos editados.
- `latexmk -lualatex -cd tesis_latex/tesis.tex` **no compila en este entorno**: falta el soporte
  de babel para español (`spanish.ldf`) y no está instalado `biber`. El mismo error se reproduce sin
  estos cambios (comprobado con `git stash`), de modo que no lo introduce esta edición. No se generó
  PDF; queda por compilar en un entorno completo.

## `\pendiente` que quedan (conteo por archivo tras la edición)

01: 1 · 02: 5 · 03: 6 · 04: 3 · 05: 3. Siguen abiertos, entre otros, Frontier (1976), Denimal
(2001), Said y Dickey (1984), Camiz y Diblasi (2013) y las fuentes de las ayudas a la
interpretación.

## Inconsistencias detectadas

Ninguna nueva.
