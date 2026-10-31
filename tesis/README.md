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
  Los siete parámetros de diseño de la iteración 3b (`nuGauss`, `pasoReglaSeis`, `ejeReglaSeis`,
  `ventanaMediaMovil`, `clasesHfcMenor`, `clasesHfcMayor` y `percentilWalkforward`, desde
  `data/results/final/parametros_diseno.csv`) se citan igual en los capítulos 2 y 3, también dentro
  del nombre «PCA-MM…». Siguen siendo **provisionales**: no están en `decisiones.qmd`, y cada uso
  lleva un comentario HTML que lo indica. Se escriben a mano, porque no denotan esos parámetros,
  $d=3$ (D9), las tolerancias de 3 y 6 meses ($h$, D7), $n_{\min}=12$ (D17.1), la numeración de los pasos de `aede`
  y las cifras de las fuentes fichadas (p. ej., el parámetro gaussiano de Atoche y Murrieta). Los
  capítulos 4 y 5 no se tocan (regla 7).
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
compilación de la iteración 3b (HEAD `c9424c2`, `tesis_latex/capitulos/*.aux`); puede cambiar si la
tesis se reordena, mientras que la etiqueta es estable. El informe numera sus propias definiciones,
proposiciones y tablas (Quarto), por lo que sus números no coinciden con los del PDF.

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
| 2 · Tamaño efectivo de una ventana y umbrales por ventana | `sec:kish` (2.7.4) |
| 2 · La regla de transiciones del notebook 06 | `sec:regla06` (2.7.5) |
| 2 · Bordes de ventana | `sec:bordes` (2.7.6) |
| 2 · Lectura multiescala del ancho de ventana | `sec:multiescala` (2.7.7) |
| 2 · Partición óptima de Fisher y número de clases | `sec:fisher` (2.8) |
| 2 · La longitud mínima de segmento | `sec:nmin` (2.8.1) |
| 2 · Datación de regímenes con los *scores* del PCA | `sec:datacion` (2.8.2) |
| 2 · Comparación de configuraciones | `sec:comparacion` (2.9) |
| 2 · Nulos de referencia y criterio del ancho de ventana | `sec:nulos` (2.10) |
| 2 · Nulo de tendencias mixto | `sec:nulo-mixto` (2.10.1) |
| 2 · Nulo de estructura constante | `sec:nulo-estructura` (2.10.2) |
| 2 · Criterio de OE4 | `sec:criterio-oe4` (2.10.3) |
| 2 · Aprendizaje profundo | `sec:dl` (2.11) |
| 2 · Criterios de comparación entre métodos | `sec:criterios` (2.12) |
| 2 · Vacíos identificados y aporte de la tesis | `sec:vacios` (2.13) |
| Cap. 3 · Metodología y desarrollo del modelo | `cap:metodologia` (3) |
| 3 · Metodología › Tipo y diseño de la investigación | `sec:met-diseno` (3.1) |
| 3 · Análisis en niveles y anexo de robustez | `sec:met-diseno` (3.1.1, sin etiqueta propia) |
| 3 · Qué vía mide qué (Pendiente) | `sec:met-vias` (3.1.2, `\pendiente`) |
| 3 · Datos (series, período, criterio de inclusión; versión congelada) | `sec:met-datos` (3.2) |
| 3 · Desarrollo del modelo › Procedimiento | `sec:met-procedimiento` (3.3) |
| 3 · Diagnóstico de las series sin transformar | `sec:met-diagnostico` (3.3.1) |
| 3 · PCA estático | `sec:met-pca` (3.3.2) |
| 3 · Parte dinámica | `sec:met-dinamica` (3.3.3) |
| 3 · Clasificación Factorial Jerárquica | `sec:met-hfc` (3.3.4) |
| 3 · Datación de regímenes y fases | `sec:met-datacion` (3.3.5) |
| 3 · Validación externa (AE y LSTM en Pendiente) | `sec:met-validacion` (3.3.6) |
| 3 · Criterios fijados de antemano | `sec:met-criterios` (3.4) |
| 3 · Implementación, paridad y reproducibilidad | `sec:met-implementacion` (3.5) |
| Cap. 4 · Resultados | `tesis_latex/capitulos/04_resultados.tex` (solo `\pendiente`; regla 7) |
| Cap. 5 · Conclusiones | `tesis_latex/capitulos/05_conclusiones.tex` (solo `\pendiente`) |

El capítulo 3 del informe conserva los dos encabezados de la estructura MMC102: «Metodología»
reúne las secciones 3.1 y 3.2 de la tesis, y «Desarrollo del modelo matemático y computacional»,
las secciones 3.3 a 3.5, en el mismo orden.

### Elementos formales del capítulo 2

| Identificador en el informe | Etiqueta de LaTeX | Nota |
|---|---|---|
| `def-regimen`, `eq-regimen` | `def:regimen` (Def. 2.1), `eq:regimen` (2.1) | |
| `def-transicion` | `def:transicion` (Def. 2.2) | |
| `def-deteccion` | `def:deteccion` (Def. 2.3) | |
| `def-fase` | `def:fase` (Def. 2.4) | |
| `def-episodio` | `def:episodio` (Def. 2.5) | |
| `def-tolerancia` | `def:tolerancia` (Def. 2.6) | |
| Observación «alcance de la tolerancia» | `obs:tolerancia` (2.7) | |
| `tbl-episodios` | `tab:episodios` (Tabla 2.1) | Fechas por `{{< meta cifras.episodio* >}}` |
| `prp-ganancia`, `eq-ganancia` | `prop:ganancia` (Prop. 2.8), `eq:ganancia` (2.2) | Sin demostración en el informe |
| `def-datos` | `def:datos` (Def. 2.9) | |
| Supuesto «datos completos» (texto) | `sup:datos` (2.10) | |
| `def-pca` | `def:pca` (Def. 2.11) | |
| `eq-pca`, `prp-pca` | `eq:pca` (2.3), `prop:pca` (Prop. 2.12) | Sin demostración |
| Párrafo de Eckart y Young | `teo:eckart-young` (Teo. 2.13) | Citado, no demostrado, en ambos |
| Observación «identificación y signo» | `obs:signo-pca` (2.14) | |
| `def-cos2`, `prp-cos2` | `def:cos2` (Def. 2.15), `prop:cos2` (Prop. 2.16) | Sin demostración |
| `def-retencion` | `def:retencion` (Def. 2.17) | |
| Supuesto «matriz regular» (texto) | `sup:regular` (2.18) | |
| `def-kmo`, `eq-kmo` | `def:kmo` (Def. 2.19), `eq:kmo` (2.4) | |
| `def-bartlett`, `eq-bartlett` | `def:bartlett` (Def. 2.20), `eq:bartlett` (2.5) | |
| Supuesto «prueba de Bartlett» (texto) | `sup:bartlett` (2.21) | |
| `lem-det` | `lem:det` (Lema 2.22) | Sin demostración |
| Observación «lectura con series de tiempo» | `obs:bartlett-series` (2.23) | |
| `def-hfc`, `eq-hfc` | `def:hfc` (Def. 2.24), `eq:hfc` (2.6) | |
| `lem-pca2` | `lem:pca2` (Lema 2.25) | Condensado; sin demostración |
| `prp-hfc-hojas` | `prop:hfc-hojas` (Prop. 2.26) | Sin demostración |
| `prp-hfc-inercia` | `prop:hfc-inercia` (Prop. 2.27) | Sin demostración |
| Observación «correspondencia con el código» | `obs:hfc-codigo` (2.28) | |
| `def-ventana`, `eq-fechado` | `def:ventana` (Def. 2.29), `eq:fechado` (2.7) | |
| `def-pesos`, `eq-pesos` | `def:pesos` (Def. 2.30), `eq:pesos` (2.8) | |
| `def-epca`, `eq-epca` | `def:epca` (Def. 2.31), `eq:epca` (2.9) | |
| Supuesto «ninguna serie constante» (texto) | `sup:ventana` (2.32) | |
| `prp-epca` | `prop:epca` (Prop. 2.33) | Sin demostración |
| Observación «estandarización ponderada» | `obs:m1` (2.34) | |
| Algoritmo `aede` (texto) | `alg:aede` (Alg. 2.35) | |
| Observación «alcance de las convenciones» | `obs:aede` (2.36) | |
| `def-kish`, `eq-kish` | `def:kish` (Def. 2.37), `eq:kish` (2.10) | |
| `prp-kish` | `prop:kish` (Prop. 2.38) | Sin demostración (se indica que usa Cauchy-Schwarz) |
| `def-umbral-ventana` | `def:umbral-ventana` (Def. 2.39) | Enumeración (a)–(b) en línea |
| Observación «alcance de los umbrales por ventana» | `obs:umbral-ventana` (2.40) | (c) remite al supuesto sin citar su número |
| `def-regla06` | `def:regla06` (Def. 2.41) | La estabilidad va en línea, no en display |
| `cor-regla06` | `cor:regla06` (Cor. 2.42) | Sin demostración; el supuesto 2.32 se enuncia en palabras |
| Observación «alcance de la regla del 06» | `obs:regla06` (2.43) | |
| `lem-ventana-mes` | `lem:ventana-mes` (Lema 2.44) | Sin demostración |
| `def-borde` | `def:borde` (Def. 2.45) | |
| Observación «qué cambia con el ancho» | `obs:multiescala` (2.46) | |
| `def-fisher`, `eq-fisher` | `def:fisher` (Def. 2.47), `eq:fisher` (2.11) | |
| (omitido; mencionado en `prp-fisher`) | `lem:costo` (Lema 2.48) | El informe solo menciona las sumas acumuladas |
| `prp-fisher`, `eq-bellman` | `prop:fisher` (Prop. 2.49), `eq:bellman` (2.12) | Sin demostración |
| `cor-fisher-factible` | `cor:fisher-factible` (Cor. 2.50) | Sin demostración |
| `prp-fisher-monotonia` | `prop:fisher-monotonia` (Prop. 2.51) | Sin demostración; el contraejemplo de (c) solo se describe |
| `def-datacion` | `def:datacion` (Def. 2.52) | La media móvil va en línea |
| `def-criterios-k` | `def:criterios-k` (Def. 2.53) | |
| Observación «lectura de las reglas» | `obs:criterios-k` (2.54) | |
| `def-ch`, `eq-ch` | `def:ch` (Def. 2.55) | La ecuación no tiene etiqueta en la tesis |
| `prp-ch` | `prop:ch` (Prop. 2.56) | Sin demostración |
| Observación «supuestos del índice» | `obs:ch` (2.57) | Incluye el uso de D11 |
| `def-rv`, `eq-rv` | `def:rv` (Def. 2.58), `eq:rv` (2.13) | Sin exigir centrado (D17.2) |
| `prp-rv` | `prop:rv` (Prop. 2.59) | Sin demostración |
| `def-rv-cargas` | `def:rv-cargas` (Def. 2.60) | |
| `prp-rv-cargas` | `prop:rv-cargas` (Prop. 2.61) | Sin demostración |
| `def-pares` | `def:pares` (Def. 2.62) | |
| `def-procrustes` | `def:procrustes` (Def. 2.63) | |
| `prp-procrustes` | `prop:procrustes` (Prop. 2.64) | Sin demostración |
| `def-tucker` | `def:tucker` (Def. 2.65) | |
| `def-bloques` | `def:bloques` (Def. 2.66) | |
| `def-hac` | `def:hac` (Def. 2.67) | La ecuación no tiene etiqueta en ninguno de los dos |
| `lem-hac` | `lem:hac` (Lema 2.68) | Sin demostración; la identidad va en línea |
| `def-nulo-mixto` | `def:nulo-mixto` (Def. 2.69) | Enumeración (a)–(d) en línea |
| Observación «supuestos del nulo mixto» | `obs:nulo-mixto` (2.70) | |
| `def-nulo-estructura` | `def:nulo-estructura` (Def. 2.71) | La recursión va en línea |
| `prp-nulo-estructura` | `prop:nulo-estructura` (Prop. 2.72) | Sin demostración; se explicita $\mathbf{G}_b$, que la tesis define en la prueba de la Prop. 2.33 |
| Observación «supuestos y límites del nulo de estructura» | `obs:nulo-estructura` (2.73) | |
| `def-oe4` | `def:oe4` (Def. 2.74) | Enumeración (a)–(d) en línea |
| Supuesto «intercambiabilidad bajo el nulo» (texto) | `sup:intercambiable` (2.75) | |
| `prp-oe4` | `prop:oe4` (Prop. 2.76) | Sin demostración |
| Observación «la versión implementada» | `obs:oe4` (2.77) | |
| `def-fuera-nulo` | `def:fuera-nulo` (Def. 2.78) | |
| `def-confirmada` | `def:confirmada` (Def. 2.79) | |
| `def-ae`, `eq-ae` | `def:ae` (Def. 2.80), `eq:ae` (2.14) | |
| `prp-ae-lineal`, `eq-ae-pca` | `prop:ae-lineal` (Prop. 2.81) | La ecuación es la del apartado (c); sin etiqueta propia en la tesis |
| `def-lstm`, `eq-lstm` | `def:lstm` (Def. 2.82), `eq:lstm` (2.15) | |
| `def-lstm-ae` | `def:lstm-ae` (Def. 2.83) | |

### Elementos formales del capítulo 3

| Identificador en el informe | Etiqueta de LaTeX | Nota |
|---|---|---|
| `tbl-etapas` | `tab:etapas` (Tabla 3.1) | |
| `def-regla-d5` | `def:regla-d5` (Def. 3.1) | |
| `tbl-kish` | `tab:kish` (Tabla 3.2) | Valores por `{{< meta cifras.nOmegaGauss* >}}` y `nHornGauss*`; $\nu$ del título por `nuGauss` |
| `def-walkforward` | `def:walkforward` (Def. 3.2) | |
| `tbl-decisiones` | `tab:decisiones` (Tabla 3.3) | |

En el informe, los supuestos, las observaciones y el algoritmo se escriben como párrafos con
encabezado en negrita, porque Quarto no tiene entornos numerados para ellos. Como cada capítulo es
una página web aparte, las remisiones del capítulo 3 a elementos del capítulo 2 se escriben como
texto («capítulo 2, definición de …») y no como referencias cruzadas.
