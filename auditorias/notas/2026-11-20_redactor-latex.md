# Nota del redactor LaTeX — 20-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `b0a34c4`. Encargo acotado: aplicar la «Regla para el
redactor (y el editor del informe)» de `auditorias/notas/2026-11-19_bibliotecario.md` (error de
reconstrucción como señal de anomalía y revisión de Pang et al., 2021). No se tocaron
`05_resultados.tex`, las cifras, `tesis/referencias.bib`, el informe `tesis/`, `data/`, `src/`,
`R/` ni `notebooks/`.

## Archivos tocados

- `tesis_latex/capitulos/02_estado_arte.tex`
- `tesis_latex/capitulos/07_pendientes.tex`

## Lo redactado y las fuentes por sección

### Cap. 2, `sec:ea-dl`, oración sobre revisiones de detección de anomalías (l. ~331–336)

- Se **complementó** (no se sustituyó) la cita de `chalapathy_chawla_2019`: se añade
  `\parencite{pang_et_al_2021}` con `\verificar{año del fascículo (2021/2022) y número de
  artículo; solo resumen leído.}`, y solo se le atribuye ser «una revisión con taxonomía del
  campo». No se le atribuye nada sobre autoencoders, error de reconstrucción ni series de tiempo.
- Chalapathy y Chawla (2019) se conserva, con su `\verificar` sin cambios, explícitamente «solo
  como fuente de exploración».
- Fuentes: `papers/pang_et_al_2021.qmd`, `papers/chalapathy_chawla_2019.qmd`.

### Cap. 2, `sec:ea-dl`, cierre de la sección (l. ~346–356)

- Se sustituyó el `\pendiente` doble por la redacción propuesta en la nota del bibliotecario, sin
  cambios de contenido:
  - error de reconstrucción del autoencoder como puntuación de anomalía en series multivariadas,
    `\parencite[sec.~3.2]{audibert_et_al_2020}` con `\verificar{texto leído en parte en la versión
    de los autores; páginas de las actas sin verificar.}`;
  - variante con la **probabilidad** de reconstrucción de una red recurrente estocástica entrenada
    con patrones normales, `\parencite{su_et_al_2019}` con `\verificar{orden de autores sin
    verificar en la editorial; solo resumen leído.}` (no se equipara con el error cuadrático de un
    autoencoder determinista);
  - entrenamiento con muchas observaciones y pocas anomalías,
    `\parencite[sec.~3.3 y~5.2]{audibert_et_al_2020}`.
- La frase de contraste («condiciones que no se cumplen en una muestra mensual corta que contiene
  las crisis») va sin cita: es lectura de la tesis, como indica la nota.
- Queda un único `\pendiente{fuente revisada por pares sobre aprendizaje profundo con series
  macrofinancieras cortas: sin ficha}`.
- No se atribuyen a ninguna de las tres obras cifras de desempeño, arquitecturas, tamaños mínimos
  de muestra ni nada sobre series macrofinancieras.
- Fuentes: `papers/audibert_et_al_2020.qmd`, `papers/su_et_al_2019.qmd`.

### Cap. 7, `sec:pend-marcas` (l. ~201–203)

- La lista de «fuentes sin ficha» no mencionaba las del error de reconstrucción; se añadió la que
  sigue abierta: «una fuente revisada por pares sobre aprendizaje profundo con series
  macrofinancieras cortas (`\cref{sec:ea-dl}`)». La lista queda: Denimal (2001), Camiz y Diblasi
  (2013) y esa fuente.
- Adam no aparece en la tesis LaTeX (`grep` de «Adam» y «kingma» sin resultados en
  `tesis_latex/`); su cita corresponde al Rmd (A.5) y al desarrollador. No se tocó.

## Verificación de claves

- `audibert_et_al_2020`: `tesis/referencias.bib` l. 1188; ficha `papers/audibert_et_al_2020.qmd`.
- `su_et_al_2019`: `tesis/referencias.bib` l. 1176; ficha `papers/su_et_al_2019.qmd`.
- `pang_et_al_2021`: `tesis/referencias.bib` l. 1164; ficha `papers/pang_et_al_2021.qmd`.
- `chalapathy_chawla_2019` (ya citada): `.bib` l. 981; ficha presente.
- Etiqueta `sec:ea-dl` existe (02, l. 306).

## Conteo de `\pendiente` (ocurrencias de `\pendiente{` en `tesis_latex/capitulos/`)

| Archivo | Antes | Después |
|---|---|---|
| 02_estado_arte.tex | 4 | 4 (uno doble sustituido por uno acotado) |
| 03_marco_teorico.tex | 2 | 2 |
| 04_metodologia.tex | 2 | 2 |
| 05_resultados.tex | 3 | 3 (no tocado) |
| Resto | 0 | 0 |
| **Total** | **11** | **11** |

El conteo de 02 incluye la mención en el comentario de cabecera (l. 4), igual que en la nota del
18-nov. El número no baja porque el cierre es parcial: la marca pasa de dos fuentes faltantes a
una. Los `\verificar` de 02 suben de 37 a 40 (Pang, Audibert y Su). No se cuentan los
`\pendiente` de `cifras_stub.tex`, preámbulo ni apéndices.

## Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex` falla por el entorno, antes de procesar los
capítulos y sin producir PDF: no se encuentra el módulo `luaotfload-main` y babel rechaza la opción
`spanish` (no encuentra `spanish.ldf`). Problema ya conocido, no del texto. Comprobación hecha en
su lugar: balance de llaves de 02 y 07 = 0. Falta compilar en un entorno completo antes de la
auditoría: biber debe resolver `audibert_et_al_2020`, `su_et_al_2019` y `pang_et_al_2021`, que se
citan por primera vez, y debe revisarse la forma de `\parencite[sec.~3.3 y~5.2]{…}` en el PDF.

## Inconsistencias detectadas

- Ninguna entre código y teoría.
- Observación menor: la frase «datos de sensores o de servidores» procede de la redacción propuesta
  por el bibliotecario y se apoya en las dos fichas en conjunto (la de Su et al. solo con el
  resumen); se cita a Audibert et al. solo para el período de entrenamiento con pocas anomalías.

## Qué debe derivar el editor del informe

- El informe hoy no tiene marca equivalente. Si incorpora el pasaje, usar «(Audibert et al., 2020,
  sec. 3.2)», «(Su et al., 2019)» y «(Audibert et al., 2020, secs. 3.3 y 5.2)», con notas
  `VERIFICAR` que repitan los `\verificar`, y `[CITA PENDIENTE: fuente revisada por pares sobre
  aprendizaje profundo con series macrofinancieras cortas]`.
- Si el informe menciona revisiones de detección de anomalías con aprendizaje profundo: «(Pang et
  al., 2021)» con nota `VERIFICAR` del año del fascículo (2021/2022), atribuyéndole solo ser una
  revisión con taxonomía del campo; Chalapathy y Chawla (2019) solo como fuente de exploración.
- Mantener la frase de contraste con las muestras mensuales cortas como lectura de la tesis, sin
  cita.
