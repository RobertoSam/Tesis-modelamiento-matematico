# Nota del bibliotecario — 25-11-2026 (vuelta 1 de la iteración 3c, aviso del redactor)

Rama `iteracion-3c`, commit de partida `34a7181`. Encargo: sección 4 de
`auditorias/notas/2026-11-24_redactor-latex.md` (la ponencia de Camiz y Diblasi no imprime el nombre
del coloquio) y, si había tiempo, un nuevo cotejo de `camiz_spada_2024`. No se tocaron
`tesis_latex/capitulos/`, `tesis_latex/preambulo.tex`, `data/`, `src/`, `R/`, `notebooks/`,
`decisiones.qmd`, `CLAUDE.md` ni `main`. El PDF y los auxiliares de la compilación no se versionan.

## 1. Lo hecho

### `camiz_diblasi_2013`: de `@unpublished` a `@presentation`

| Qué | Detalle | Fuente |
|---|---|---|
| Diagnóstico | El *driver* `unpublished` de biblatex-apa no usa `eventtitle`; el *driver* `presentation` llama a la macro `eventinfo` (`eventtitle`, `venue`), conforme a APA 7, 10.5 | `apa.bbx` v9.17 (2023/03/20), instalado con `texlive-bibtex-extra` |
| Cambio en el `.bib` | Solo el tipo de entrada. Clave, autores, título, `titleaddon = {Ponencia}`, `eventtitle`, `venue`, `year` y `verificar` sin cambios. **Ningún metadato nuevo** (no hay actas; los datos siguen siendo los del PDF) | — |
| Compilación | `latexmk -lualatex -cd tesis_latex/tesis.tex` (biber instalado con apt-get): salida 0; `tesis.log` sin «undefined» (citas ni referencias); `tesis.blg` sin advertencias ni errores; `tesis.bbl`: `\entry{camiz_diblasi_2013}{presentation}{}` | Compilación local |
| Impresión (pdftotext del PDF) | «Camiz, S., & Diblasi, A. (2013). Evolutionary principal component analysis [Ponencia]. XLI Coloquio Argentino de Estadística, Mendoza, Argentina.» El título va en cursiva (formato `presentation` de `apa.bbx` sin `maintitle`) | `tesis_latex/tesis.pdf` (no versionado) |

La forma coincide con APA 7, 10.5 (autor, año, *título* [descripción], nombre del evento, lugar). Falta
el día y mes del coloquio, que APA pide cuando se conocen: **no** se agregó porque no se vio en ninguna
fuente.

**Efecto en el informe (Quarto).** Con pandoc 3.1.3 y `tesis/apa.csl`, `@presentation` se lee sin tipo
CSL y `@unpublished` con evento como `speech`; la salida es la misma en ambos casos: «… analysis.
Ponencia. XLI Coloquio Argentino de Estadística, Mendoza, Argentina.» (sin corchetes). El informe aún
no cita la obra (`[CITA PENDIENTE]`); si llega a citarla, el editor del informe debe revisar la salida
con el pandoc de Quarto, que puede ser otra versión.

### `camiz_spada_2024`: nuevo intento de cotejo

| Fuente | Resultado |
|---|---|
| doi.org/10.12899/asr-2455 | Permiso no respondido en la sesión; no se reintentó |
| Página de la revista (journals-crea.4science.it/index.php/asr/article/view/2455, hallada en el buscador) | Redirige (302) a creajournals.crea.gov.it; ese dominio: permiso no respondido; no se reintentó ni se buscó otra ruta |
| DOAJ (doaj.org, artículo c45929613a3546edac0ae7ed00dfa63d; directorio, **base secundaria**) | Título «Checking the stability of correlation of chronologies over time: an example on Pinus pinea L. rings widths»; autores «Sergio Camiz», «Francesco Spada»; «Vol. 49, no. 1»; DOI 10.12899/asr-2455; fecha **«Oct 2023»**; no da páginas |
| CRIS de la PUCP (hallado en el buscador) | Página antirrobots («Access Denied»); no se buscó otra ruta |

Conclusión: **no confirmado** en fuente oficial. Lo que DOAJ coincide con la entrada (título, autores,
volumen, número, DOI) sirve para localizar, no para verificar. **Discrepancia nueva:** DOAJ fecha el
número en **octubre de 2023**, y la entrada (tomada del PDF) dice 2024. No se cambió nada (ni ficha ni
`.bib`): el año queda en duda hasta ver la revista o doi.org.

### Registro

`tesis/registro_verificacion.md`: frase nueva en el párrafo inicial y sección «Ponencia y cotejo de Camiz
y Spada (25-11-2026)», antes de las marcas no bibliográficas.

## 2. Pendiente y motivo

- `camiz_diblasi_2013`: actas, ISBN o URL; fecha exacta del coloquio; nombre de pila de la segunda
  autora. Sin búsquedas nuevas (ocho previas sin resultado); sigue el pedido a Roberto de preguntar al
  Dr. Camiz.
- `camiz_spada_2024`: año (2023 según DOAJ o 2024 según el PDF), páginas 13–23 y DOI en doi.org o en
  creajournals.crea.gov.it (permisos no respondidos). Si Roberto puede abrir la página del artículo,
  basta con el encabezado del número y la cita sugerida por la revista.

## 3. Para el redactor

- No hay que tocar las citas: la clave no cambió. La entrada ya imprime el nombre del coloquio.
- Si cita `camiz_spada_2024` (cuando Roberto decida sobre la contradicción con el vacío 2), el
  `\verificar` debe mencionar también el año: «año (2023 en DOAJ, 2024 en el PDF), volumen, número,
  páginas y DOI no cotejados en la revista».
