# Borrador de tesis (MMC102 — Seminario de Tesis II)

- `_capitulos/NN_*.qmd`: cuerpo de cada capítulo. Los subtítulos empiezan en `##`. Es el único
  lugar donde se redacta.
- `NN_*.qmd`: página web de cada capítulo (solo incluye el cuerpo).
- `borrador_completo.qmd`: reúne los capítulos y genera HTML y **.docx** con
  `plantilla_uni.docx`.
- `referencias.bib`: bibliografía única, compartida con la tesis LaTeX; cada entrada tiene ficha
  en `papers/` y solo la modifica el bibliotecario.
- `registro_verificacion.md`: referencias con verificación pendiente.
- `apa.csl`: estilo APA 7 (CSL oficial); con `lang: es` genera «et al.» y «Recuperado de». Dos
  defectos conocidos en español, pendientes de una decisión (nota
  `auditorias/notas/2026-10-20_editor-informe.md`): las citas narrativas salen con «&» en lugar de
  «y», y las fechas completas de la bibliografía salen como «2013, mayo 22».
- `_cifras.yml`: cifras generadas por `herramientas/generar_cifras.py` a partir de
  `data/results/`. No se edita a mano. `_metadata.yml` lo declara en `metadata-files`, y en el
  texto se cita con `{{< meta cifras.nMesesNiveles >}}` (lista de claves en
  `herramientas/README.md`).
- `herramientas/generar_plantilla_docx.py`: regenera la plantilla Word (Arial 12, interlineado
  1,5, márgenes de 3 cm a la izquierda y 2,5 cm en el resto, número de página centrado).

**Formato institucional:** las «Pautas para redactar el Trabajo de Tesis de Maestría de la UNI»
que cita MMC102 aún no están en el proyecto. La guía disponible (2018) es de la Universidad
Nacional del Centro del Perú y se usa solo de forma provisional para el formato. Debe
reemplazarse por la pauta de la UNI.

Generar el Word:

```
quarto render tesis/borrador_completo.qmd --to docx
```

## Correspondencia con la tesis LaTeX

El informe se deriva de la tesis maestra (`tesis_latex/`) y no afirma nada que ella no sostenga.
Las tablas siguientes indican, para cada sección y cada elemento formal del informe, la etiqueta
`\label` de la tesis de la que procede. El número entre paréntesis es el del PDF de la tesis en la
compilación de la iteración 3a (`tesis_latex/capitulos/*.aux`); puede cambiar si la tesis se
reordena, mientras que la etiqueta es estable. El informe numera sus propias definiciones y
proposiciones (Quarto), por lo que sus números no coinciden con los del PDF.

### Secciones

| Sección del informe (`_capitulos/`) | Etiqueta de LaTeX |
|---|---|
| Cap. 1 · Introducción | `cap:introduccion` (1) |
| 1 · Planteamiento y descripción del problema | `sec:planteamiento` (1.1) |
| 1 · Justificación de la investigación | `sec:justificacion` (1.2) |
| 1 · Objetivos (general, específicos, condicionales) | `sec:objetivos` (1.3); específicos `sec:oe` (1.3.2) |
| 1 · OE1 a OE12 | `oe:estado-arte`, `oe:datos`, `oe:clasicos`, `oe:ventana`, `oe:robustez-hfc`, `oe:dimension`, `oe:dl`, `oe:incertidumbre`, `oe:datacion`, `oe:episodios`, `oe:simulado`, `oe:comparacion` |
| 1 · OC1 a OC4 | `oc:ehfc`, `oc:statis`, `oc:anticipar`, `oc:extension` |
| 1 · Hipótesis | `sec:hipotesis` (1.4) |
| Cap. 2 · Antecedentes y marco teórico | `cap:marco` (2) |
| 2 · Antecedentes peruanos | `sec:antecedentes` (2.1) |
| 2 · El ciclo financiero y los regímenes como objetos matemáticos | `sec:ciclo` (2.2) |
| 2 · Régimen, transición y detección | `sec:regimen` (2.2.2) |
| 2 · Validación externa | `sec:validacion` (2.2.3) |
| 2 · Posición epistemológica | `sec:epistemologia` (2.3) |
| 2 · Datos y convenciones generales | `sec:datos` (2.4) |
| 2 · Análisis de componentes principales | `sec:pca` (2.5) |
| 2 · Calidad de representación y contribuciones | `sec:cos2` (2.5.2) |
| 2 · Número de componentes | `sec:retencion` (2.5.3) |
| 2 · Adecuación muestral: KMO y Bartlett | `sec:adecuacion` (2.5.4) |
| 2 · Clasificación Factorial Jerárquica | `sec:hfc` (2.6) |
| 2 · Análisis evolutivo de componentes principales | `sec:epca` (2.7) |
| 2 · Partición óptima de Fisher y número de clases | `sec:fisher` (2.8) |
| 2 · Comparación de configuraciones | `sec:comparacion` (2.9) |
| 2 · Aprendizaje profundo | `sec:dl` (2.10) |
| 2 · Criterios de comparación entre métodos | `sec:criterios` (2.11) |
| 2 · Vacíos identificados y aporte de la tesis | `sec:vacios` (2.12) |
| Cap. 3 · Metodología | `tesis_latex/capitulos/03_metodologia.tex` (solo `\pendiente`) |
| Cap. 4 · Resultados | `tesis_latex/capitulos/04_resultados.tex` (solo `\pendiente`; regla 7) |
| Cap. 5 · Conclusiones | `tesis_latex/capitulos/05_conclusiones.tex` (solo `\pendiente`) |

### Elementos formales del capítulo 2

| Identificador en el informe | Etiqueta de LaTeX | Nota |
|---|---|---|
| `def-regimen`, `eq-regimen` | `def:regimen` (Def. 2.1), `eq:regimen` (2.1) | |
| `def-transicion` | `def:transicion` (Def. 2.2) | |
| `def-deteccion` | `def:deteccion` (Def. 2.3) | |
| `def-fase` | `def:fase` (Def. 2.4) | |
| `prp-ganancia`, `eq-ganancia` | `prop:ganancia` (Prop. 2.5), `eq:ganancia` (2.2) | Sin demostración en el informe |
| `def-datos` | `def:datos` (Def. 2.6) | |
| Supuesto «datos completos» (texto) | `sup:datos` (2.7) | |
| `def-pca` | `def:pca` (Def. 2.8) | |
| `eq-pca`, `prp-pca` | `eq:pca` (2.3), `prop:pca` (Prop. 2.9) | Sin demostración |
| Párrafo de Eckart y Young | `teo:eckart-young` (Teo. 2.10) | Citado, no demostrado, en ambos |
| Observación «identificación y signo» | `obs:signo-pca` (2.11) | |
| `def-cos2`, `prp-cos2` | `def:cos2` (Def. 2.12), `prop:cos2` (Prop. 2.13) | Sin demostración |
| `def-retencion` | `def:retencion` (Def. 2.14) | |
| Supuesto «matriz regular» (texto) | `sup:regular` (2.15) | |
| `def-kmo`, `eq-kmo` | `def:kmo` (Def. 2.16), `eq:kmo` (2.4) | |
| `def-bartlett`, `eq-bartlett` | `def:bartlett` (Def. 2.17), `eq:bartlett` (2.5) | |
| Supuesto «prueba de Bartlett» (texto) | `sup:bartlett` (2.18) | |
| `lem-det` | `lem:det` (Lema 2.19) | Sin demostración |
| Observación «lectura con series de tiempo» | `obs:bartlett-series` (2.20) | |
| `def-hfc`, `eq-hfc` | `def:hfc` (Def. 2.21), `eq:hfc` (2.6) | |
| `lem-pca2` | `lem:pca2` (Lema 2.22) | Condensado; sin demostración |
| `prp-hfc-hojas` | `prop:hfc-hojas` (Prop. 2.23) | Sin demostración |
| `prp-hfc-inercia` | `prop:hfc-inercia` (Prop. 2.24) | Sin demostración |
| Observación «correspondencia con el código» | `obs:hfc-codigo` (2.25) | |
| `def-ventana`, `eq-fechado` | `def:ventana` (Def. 2.26), `eq:fechado` (2.7) | |
| `def-pesos`, `eq-pesos` | `def:pesos` (Def. 2.27), `eq:pesos` (2.8) | |
| `def-epca`, `eq-epca` | `def:epca` (Def. 2.28), `eq:epca` (2.9) | |
| Supuesto «ninguna serie constante» (texto) | `sup:ventana` (2.29) | |
| `prp-epca` | `prop:epca` (Prop. 2.30) | Sin demostración |
| Observación «estandarización ponderada» | `obs:m1` (2.31) | |
| Algoritmo `aede` (texto) | `alg:aede` (Alg. 2.32) | |
| Observación «alcance de las convenciones» | `obs:aede` (2.33) | |
| `def-fisher`, `eq-fisher` | `def:fisher` (Def. 2.34), `eq:fisher` (2.10) | |
| (omitido; mencionado en `prp-fisher`) | `lem:costo` (Lema 2.35) | El informe solo menciona las sumas acumuladas |
| `prp-fisher`, `eq-bellman` | `prop:fisher` (Prop. 2.36), `eq:bellman` (2.11) | Sin demostración |
| `def-ch`, `eq-ch` | `def:ch` (Def. 2.37) | La ecuación no tiene etiqueta en la tesis |
| `prp-ch` | `prop:ch` (Prop. 2.38) | Sin demostración |
| Observación «supuestos del índice» | `obs:ch` (2.39) | |
| `def-rv`, `eq-rv` | `def:rv` (Def. 2.40), `eq:rv` (2.12) | |
| `prp-rv` | `prop:rv` (Prop. 2.41) | Sin demostración |
| `def-procrustes` | `def:procrustes` (Def. 2.42) | |
| `prp-procrustes` | `prop:procrustes` (Prop. 2.43) | Sin demostración |
| `def-tucker` | `def:tucker` (Def. 2.44) | |
| `def-ae`, `eq-ae` | `def:ae` (Def. 2.45), `eq:ae` (2.13) | |
| `prp-ae-lineal`, `eq-ae-pca` | `prop:ae-lineal` (Prop. 2.46) | La ecuación es la del apartado (c); sin etiqueta propia en la tesis |
| `def-lstm`, `eq-lstm` | `def:lstm` (Def. 2.47), `eq:lstm` (2.14) | |
| `def-lstm-ae` | `def:lstm-ae` (Def. 2.48) | |

En el informe, los supuestos, las observaciones y el algoritmo se escriben como párrafos con
encabezado en negrita, porque Quarto no tiene entornos numerados para ellos.
