# Nota del redactor LaTeX — 22-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `539289e`. Encargo acotado: aplicar la «Regla para el
redactor (y el editor del informe)» de `auditorias/notas/2026-11-21_bibliotecario.md` (redes
recurrentes con datos macrofinancieros, Tölö, 2020; sobreajuste del aprendizaje automático en
alerta temprana, Beutel, List y von Schweinitz, 2019). No se tocaron `05_resultados.tex`, las
cifras, `tesis/referencias.bib`, el informe `tesis/`, `data/`, `src/`, `R/` ni `notebooks/`.

## Archivos tocados

- `tesis_latex/capitulos/02_estado_arte.tex`
- `tesis_latex/capitulos/07_pendientes.tex`

## Lo redactado y las fuentes por sección

### Cap. 2, `sec:ea-dl`, cierre de la sección (l. ~355–367)

- Se sustituyó `\pendiente{fuente revisada por pares sobre aprendizaje profundo con series
  macrofinancieras cortas: sin ficha}` por un párrafo nuevo, después de la oración que termina en
  «…que contiene las crisis.». Sigue la redacción propuesta por el bibliotecario, con una frase
  añadida sobre el carácter supervisado de ambos trabajos:
  - `\textcite{tolo_2020}` con `\verificar{número de artículo y DOI vistos solo en RePEc; solo
    resumen leído.}`: se le atribuye solo predecir crisis sistémicas con redes LSTM y GRU sobre un
    panel de 17 países entre 1870 y 2016 (resumen). Nada sobre tamaño de muestra, número de crisis,
    regularización, validación ni frecuencia de los datos.
  - `\parencite{beutel_list_von_schweinitz_2019}` con `\verificar{número de artículo visto en el
    repositorio del autor; el trabajo no incluye redes neuronales.}`: se le atribuye solo que los
    métodos flexibles de aprendizaje automático logran un ajuste muy alto dentro de la muestra y que
    el logit los supera en la evaluación recursiva fuera de ella (resumen del artículo). Nada sobre
    redes neuronales ni aprendizaje profundo; no se usan las páginas del documento de trabajo
    (sec. 4.4, ap. A.2) ni se le atribuye explícitamente el sobreajuste como explicación.
  - Frase nueva, sin cita (lectura de la tesis, como sugiere la nota): ambos trabajos resuelven un
    problema supervisado, la predicción de crisis fechadas de antemano, mientras que la tesis usa
    estas redes sin etiquetas para describir regímenes.
  - Frase de contraste sin cita (inferencia propia): la tesis no dispone de un panel así, trabaja con
    un solo país y una muestra mensual corta, lo que refuerza el carácter de complemento de la vía
    AE/LSTM. No se atribuye a los autores que el panel compense la escasez de crisis.
  - `\pendiente` residual acotado: `\pendiente{fuente revisada por pares que discuta el tamaño de
    muestra para redes profundas con series macrofinancieras: sin ficha}`.
- Las cifras «17 países» y «1870 y 2016» son datos bibliográficos del resumen de Tölö (2020), no
  resultados de la tesis; no corresponden a `cifras.tex`.
- Fuentes: `papers/tolo_2020.qmd` (FB-113), `papers/beutel_list_von_schweinitz_2019.qmd` (FB-114).

### Cap. 7, `sec:pend-marcas` (l. ~201–204)

- La entrada «una fuente revisada por pares sobre aprendizaje profundo con series macrofinancieras
  cortas» se ajustó al `\pendiente` residual: «una fuente revisada por pares que discuta el tamaño
  de muestra para redes profundas con series macrofinancieras (`\cref{sec:ea-dl}`); las aplicaciones
  de redes recurrentes y de aprendizaje automático a la alerta temprana de crisis ya tienen ficha».
  La lista sigue siendo: Denimal (2001), Camiz y Diblasi (2013) y esa fuente.

## Verificación de claves

- `tolo_2020`: `tesis/referencias.bib` l. 1209; ficha `papers/tolo_2020.qmd`.
- `beutel_list_von_schweinitz_2019`: `tesis/referencias.bib` l. 1220; ficha
  `papers/beutel_list_von_schweinitz_2019.qmd`.
- Etiqueta `sec:ea-dl` existe (02, l. 306).

## Conteo de marcas (líneas con `\pendiente{` / `\verificar{` en `tesis_latex/capitulos/`)

| Archivo | `\pendiente` antes | después | `\verificar` antes | después |
|---|---|---|---|---|
| 01_introduccion.tex | 0 | 0 | 10 | 10 |
| 02_estado_arte.tex | 4 | 4 | 40 | 42 |
| 03_marco_teorico.tex | 2 | 2 | 39 | 39 |
| 04_metodologia.tex | 2 | 2 | 3 | 3 |
| 05_resultados.tex | 3 | 3 | 0 | 0 (no tocado) |
| Resto | 0 | 0 | 0 | 0 |
| **Total** | **11** | **11** | **92** | **94** |

El conteo de 02 incluye la mención en el comentario de cabecera (l. 4). El número de `\pendiente`
no baja porque el cierre es parcial: la marca pasa de «aprendizaje profundo con series
macrofinancieras cortas» a la discusión específica del tamaño de muestra para redes profundas. Los
`\verificar` suben en 2 (Tölö y Beutel et al.). No se cuentan los de `cifras_stub.tex`, preámbulo
ni apéndices.

## Compilación

`latexmk -lualatex -cd tesis_latex/tesis.tex` falla por el entorno (código 12), antes de procesar
los capítulos y sin producir PDF: no se encuentra el módulo `luaotfload-main` y babel no encuentra
`spanish.ldf`. Problema ya conocido, no del texto; no se intentó arreglar. Comprobación hecha en su
lugar: balance de llaves de 02 y 07 = 0. Falta compilar en un entorno completo antes de la
auditoría: biber debe resolver `tolo_2020` y `beutel_list_von_schweinitz_2019`, que se citan por
primera vez, y debe revisarse la forma de «Tölö (2020)» (diéresis) y de «(Beutel et al., 2019)» en
el PDF.

## Inconsistencias detectadas

- Ninguna entre código y teoría.
- Observación menor: la cita de Beutel et al. aparece en un párrafo sobre aprendizaje profundo. El
  texto la presenta como evidencia de «métodos flexibles de aprendizaje automático» y la
  `\verificar` aclara que no incluye redes neuronales; el auditor debe comprobar que no se lea como
  evidencia sobre LSTM o autoencoders.

## Qué debe derivar el editor del informe

- El informe hoy no tiene marca equivalente. Si incorpora el pasaje, usar «Tölö (2020)» con nota
  `VERIFICAR: número de artículo y DOI vistos solo en RePEc; solo resumen leído` y «(Beutel et al.,
  2019)» con nota `VERIFICAR: número de artículo visto en el repositorio del autor; el trabajo no
  incluye redes neuronales`.
- Atribuir a Tölö solo LSTM/GRU para predecir crisis sistémicas con el panel de 17 países
  (1870–2016); a Beutel et al. solo el contraste entre ajuste dentro y fuera de la muestra frente al
  logit. Nada sobre tamaño de muestra o frecuencia a Tölö; nada sobre redes neuronales a Beutel et al.
- Mantener sin cita, como lectura propia, el carácter supervisado de ambos trabajos frente al uso no
  supervisado de la tesis y el contraste panel largo / muestra mensual peruana.
- Marca residual: `[CITA PENDIENTE: fuente revisada por pares que discuta el tamaño de muestra para
  redes profundas con series macrofinancieras]`.
