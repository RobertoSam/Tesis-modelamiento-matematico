# Nota del bibliotecario — 21-nov-2026 (iteración 3c, seguimiento diario)

Rama `iteracion-3c`, commit de partida `b864902`. Encargo:

1. **Prioridad 1:** una o dos fuentes revisadas por pares que apliquen redes recurrentes/LSTM o
   autoencoders a datos macrofinancieros de baja frecuencia y que discutan o evidencien la limitación
   del tamaño de muestra. Son para el `\pendiente{fuente revisada por pares sobre aprendizaje profundo
   con series macrofinancieras cortas: sin ficha}` de `tesis_latex/capitulos/02_estado_arte.tex`,
   `sec:ea-dl`, l. 355.
2. **Prioridad 2:** Sakurada y Yairi (2014), solo si se verifican sus metadatos en fuente primaria.

No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `tesis/informe_mmc102/`, `data/`, `src/`, `R/` ni
`notebooks/`.

## Archivos

- Fichas nuevas (la mayor existente era FB-112):
  - `papers/tolo_2020.qmd` (FB-113, preliminar, resumen);
  - `papers/beutel_list_von_schweinitz_2019.qmd` (FB-114, preliminar; resumen del artículo y texto
    parcial del documento de trabajo previo).
- `tesis/referencias.bib`: dos entradas nuevas, las dos con campo `verificar`. Conteo con expresión
  regular: 113 entradas, sin claves duplicadas, todas con ficha y llaves balanceadas (pybtex no
  instalado).
- `tesis/registro_verificacion.md`: encabezado al día y nueva sección «Pendientes bibliográficos
  (21-11-2026)».

## Lo verificado y la fuente de cada dato

### 1. `tolo_2020` · resumen · la única fuente con redes recurrentes

Tölö, E. (2020). Predicting systemic financial crises with recurrent neural networks. *Journal of
Financial Stability*, 49, 100746.

- **Repositorio del Banco de Finlandia** (urn.fi/URN:NBN:fi:bof-202002181112), la institución del
  autor:
  - título; Eero Tölö; 2020; volumen 49; «August» (2020);
  - nota «Published in BoF 14/2019»;
  - el registro no nombra la revista y no tiene archivos.
- **research.fi** (portal nacional finlandés de información de investigación, registro 0368373920):
  - *Journal of Financial Stability*; 2020; ISSN 1572-3089;
  - tipo A1, «journal article (refereed), original research»; revisado por pares: sí;
  - organización: Bank of Finland;
  - no da volumen, número de artículo ni DOI.
- **RePEc/IDEAS** (secundaria):
  - vol. 49(C); DOI 10.1016/j.jfs.2020.100746; PII S1572308920300243;
  - palabras clave «Early warning system; Systemic Banking crises; Neural networks; Validation»;
  - **no** da el número de artículo: 100746 se toma del sufijo del DOI → `verificar`.
- **Resumen (urn.fi y RePEc):**
  - redes recurrentes para predecir crisis sistémicas con uno a cinco años de anticipación;
  - base de Jordà, Schularick y Taylor: 17 países, 1870–2016;
  - LSTM y GRU superan a las redes simples, que ya superaban al logit; el autor lo atribuye a la
    capacidad de las redes recurrentes de predecir de forma más robusta a partir de series de tiempo;
  - el resultado resiste un análisis de sensibilidad amplio.
- **No leído:** el texto. No se sabe si discute el tamaño de muestra o el número de crisis. El resumen
  no da la frecuencia de los datos.

### 2. `beutel_list_von_schweinitz_2019` · resumen y documento de trabajo previo · sin redes neuronales

Beutel, J., List, S., & von Schweinitz, G. (2019). Does machine learning help us predict banking
crises? *Journal of Financial Stability*, 45, 100693.

- **Repositorio del IWH** (iwh-halle.de; G. von Schweinitz es investigador del IWH):
  - autores en ese orden; título; *Journal of Financial Stability*, vol. 45, diciembre de 2019;
  - DOI 10.1016/j.jfs.2019.100693;
  - resumen (cortado al final);
  - no da el número de artículo.
- **Repositorio de código del autor** (GitHub, gvschweinitz): cita «Journal of Financial Stability,
  45, 100693». Es una fuente del autor, no de la editorial → `verificar` sobre el número de artículo.
- **RePEc/IDEAS** (secundaria): mismos datos; palabras clave y JEL.
- **Resumen del artículo:**
  - modelos de alerta temprana de crisis bancarias sistémicas, economías avanzadas, unos 45 años;
  - «machine learning methods often attain a very high in-sample fit», pero «they are outperformed by
    the logit approach in recursive out-of-sample evaluations»;
  - el resultado se mantiene con otras métricas, definiciones, longitudes de muestra, variables y
    transformaciones.
- **Documento de trabajo previo** (Deutsche Bundesbank DP 48/2018, PDF del sitio del Bundesbank, leído
  con una herramienta que resume):
  - métodos: k vecinos más cercanos, árboles de decisión, bosques aleatorios y máquinas de vectores de
    soporte (sec. 2.2, p. 3);
  - **redes neuronales excluidas** (nota 3, p. 4): no mostraron ganancias significativas y su
    estimación exige muchos puntos iniciales aleatorios;
  - datos trimestrales, 15 economías avanzadas, 1970–2016, 22 crisis, 1 801 observaciones (sec. 1,
    p. 2; nota 9, p. 8);
  - el sobreajuste sería un problema mayor en al menos algunos modelos y persiste tras ajustar los
    hiperparámetros (sec. 4.4, pp. 16–18);
  - «When the number of crisis events contained in the sample is reduced, estimation uncertainty
    increases» (apéndice A.2, pp. 29–30).
  - La paginación y las frases son del **documento de trabajo**, no del artículo publicado.

### 3. Candidatos revisados y descartados

- **Chung, S., «Inside the black box: Neural network-based real-time prediction of US recessions»**
  (arXiv:2310.17571v3, 23-05-2024).
  - Es lo más cercano al encargo: LSTM y GRU con datos mensuales; sec. 1 dice que el uso de redes
    neuronales en macroeconomía es limitado por «the small sample sizes and low-frequency nature of
    macroeconomic data», sin cita que lo respalde; sec. 3.2 trata el sobreajuste con pocos datos de
    recesión.
  - Ni arXiv ni las búsquedas muestran una versión en revista → **solo exploración, no se fichó**.
- **Almosova y Andresen (2023)**, *Journal of Forecasting*, 42(2), 240–259, DOI 10.1002/for.2901.
  - Metadatos vistos en el catálogo de la red de bibliotecas de Baviera (BVB) y en RePEc.
  - Es una LSTM **univariada** sobre la inflación mensual de los EE. UU. El resumen no trata el tamaño
    de muestra.
  - No se fichó: no es macrofinanciera y no aporta a la limitación.
- **Bluwstein et al. (aprendizaje automático y crisis, datos de Jordà, Schularick y Taylor).**
  - El portal de la Universidad de Bath solo muestra versiones de documento de trabajo (Bank of
    England WP 848, 2020; ECB WP 2614, 2021).
  - No se vio la versión en revista. No se fichó.

## Regla para el redactor (y el editor del informe)

El `\pendiente` de `sec:ea-dl` (l. 355) **puede cerrarse en parte**. Hay una fuente revisada por pares
que aplica redes recurrentes a datos macrofinancieros (Tölö, 2020). Hay otra que evidencia el
sobreajuste de métodos flexibles con pocas crisis (Beutel et al., 2019), pero **sin redes
neuronales**. Ninguna, en lo leído, discute la limitación de muestra **para el aprendizaje profundo**.

**Redacción propuesta** (sustituye el `\pendiente`; va después de la oración que termina en «…que
contiene las crisis.»):

> Con datos macrofinancieros, las redes recurrentes se han usado sobre todo en sistemas de alerta
> temprana: \textcite{tolo_2020}\verificar{número de artículo y DOI vistos solo en RePEc; solo resumen
> leído.} predice crisis sistémicas con redes LSTM y GRU sobre un panel de 17 países entre 1870 y
> 2016. En ese mismo campo, los métodos flexibles de aprendizaje automático logran un ajuste muy alto
> dentro de la muestra, pero el logit los supera en la evaluación recursiva fuera de ella
> \parencite{beutel_list_von_schweinitz_2019}\verificar{número de artículo visto en el repositorio del
> autor; el trabajo no incluye redes neuronales.}. La tesis no dispone de un panel así: trabaja con un
> solo país y una muestra mensual corta, lo que refuerza el carácter de complemento de la vía AE/LSTM.
> \pendiente{fuente revisada por pares que discuta el tamaño de muestra para redes profundas con
> series macrofinancieras: sin ficha}

Si el redactor prefiere no dejar el `\pendiente` residual, debe reformular la frase para que no
afirme que la literatura revisada por pares documenta la limitación **para redes profundas**.

**Qué atribuir y qué no:**

- **Tölö (2020):**
  - sí: el uso de LSTM y GRU para predecir crisis sistémicas de uno a cinco años antes; los datos (17
    países, 1870–2016); que superan a las redes simples y al logit, según el resumen;
  - no: nada sobre el tamaño de muestra, el número de crisis, la regularización ni el esquema de
    validación (texto no leído); tampoco la frecuencia anual (el resumen no la da).
- **Beutel, List y von Schweinitz (2019):**
  - sí: el ajuste alto dentro de la muestra y el peor desempeño fuera de ella frente al logit en la
    evaluación recursiva (resumen del artículo); que los datos son de economías avanzadas durante unos
    45 años;
  - con cuidado: el sobreajuste como explicación y el efecto del número de crisis están en el
    **documento de trabajo** (sec. 4.4 y ap. A.2). No citar esas páginas como del artículo; si se usan,
    citar solo el artículo sin localizador;
  - no: nada sobre redes neuronales o aprendizaje profundo (no las incluye); no presentarla como
    evidencia sobre LSTM o autoencoders.
- **Inferencia propia:** que un panel largo de varios países compensa la escasez de crisis, y que la
  muestra peruana no la tiene, es lectura de la tesis. No se atribuye a los autores.
- **Problema distinto:** ambos trabajos son supervisados (predicen crisis fechadas). La tesis es no
  supervisada; conviene decirlo si el párrafo se amplía.
- **Cap. 7, `sec:pend-marcas` (l. ~203):** si se adopta la redacción, la entrada «fuente revisada por
  pares sobre aprendizaje profundo con series macrofinancieras cortas» debe ajustarse al nuevo
  `\pendiente` residual.
- **APA en el informe:** «Tölö (2020)» y «(Beutel et al., 2019)», con notas `VERIFICAR` que repitan los
  `\verificar`. Hoy el informe no tiene marca equivalente (lo registró la nota del 19-11).

## Accesos fallidos y lo que no se hizo

- **doi.org** (10.1016/j.jfs.2020.100746): la solicitud de permiso no se respondió a tiempo. No se
  reintentó.
- **ScienceDirect** (PII S1572308920300243): no se envió por el permiso pendiente anterior. No se
  reintentó.
- **EconStor**, PDF del DP 14/2019 del Banco de Finlandia: sin permiso. No se reintentó ni se buscó
  por otra vía; por eso el texto de Tölö no se leyó.
- **Crossref y ACM Digital Library:** no se intentaron (bloqueados o sin permiso en sesiones
  anteriores).
- **Sakurada y Yairi (2014)**, «Anomaly detection using autoencoders with nonlinear dimensionality
  reduction» (MLSDA 2014):
  - solo se localizó en fuentes secundarias (BibBase y Springer Professional, que reproduce un
    registro con DOI 10.1145/2689746.2689747);
  - no se abrió ACM Digital Library;
  - **no se fichó**; el DOI no se considera verificado.
- **Siguen pendientes:**
  - fuente revisada por pares que discuta el tamaño de muestra para redes profundas con series
    macrofinancieras;
  - DOI y número de artículo de `tolo_2020` en la editorial y su texto;
  - Sakurada y Yairi (2014);
  - los pendientes previos: metadatos de las obras de ACM de la nota del 19-11, Camiz y Diblasi
    (2013), Denimal (2001) y Künsch (1989) en la editorial.
