# Bibliotecario · 7 de noviembre de 2026 · Iteración 3c (estado del arte y N-02)

**Alcance.** Fichas nuevas en `papers/` (30), entradas nuevas en `tesis/referencias.bib` (30),
fichas `congreso_2018` y `pcm_2020` alineadas con D18, y `tesis/registro_verificacion.md`
actualizado. No se tocaron `tesis_latex/`, `tesis/_capitulos/`, `src/`, `R/` ni `data/`, ni
`episodios_referencia.csv`.

**Cómo se verificó.** Los metadatos de los artículos se verificaron en el registro del DOI en
Crossref (api.crossref.org); doi.org solo resolvió el DOI de Borio (2014). Los documentos de trabajo
se verificaron en el sitio de la institución (BIS, BCE, FMI, NBER, De Nederlandsche Bank,
Bundesbank, Banco de Canadá, Banco de la República), y los libros, en catálogos o registros
institucionales. RePEc, IDEAS y EconPapers solo sirvieron para localizar las obras. Cada ficha dice
de dónde salió cada dato y qué se leyó. Accesos fallidos: ScienceDirect, PubMed Central (reCAPTCHA),
EconBiz y el repositorio PUCP (Anubis), los sitios del BCRP (Incapsula) y doi.org para el DOI de
Kim y Nelson. No se buscaron rutas alternativas.

## Regla para el redactor

- **«Resumen»:** solo se atribuye lo que dice el resumen oficial.
- **«Solo localizada»:** la obra se cita sin atribuirle hallazgos.
- **Entradas con campo `verificar`:** si se citan, el texto lleva `\verificar{…}`. Son
  `aikman_haldane_nelson_2015`, `kim_nelson_1999`, `chalapathy_chawla_2019`,
  `gomez_gonzalez_et_al_2013` y `brandao_marques_perez_ruiz_2017`.
- **`chalapathy_chawla_2019`** es un *preprint*: solo sirve como exploración, igual que
  `plaut_2018`, y no sostiene ninguna afirmación de la tesis.

## 1. Ciclo financiero: concepto y medición

**`borio_2014`** · resumen.
- Ensayo de síntesis: la macroeconomía de las últimas tres décadas no se entiende sin el ciclo
  financiero.
- Se organiza en hechos estilizados, modelación y política, con énfasis en la fase de contracción.
- *Relación con la tesis:* sirve para definir el objeto de estudio y separarlo del ciclo económico.
  No atribuirle cifras de duración (no se leyó el texto).

**`drehmann_borio_tsatsaronis_2012`** · ya fichada.
- Es la definición empírica de referencia: componente de mediano plazo común al crédito, a la razón
  crédito/PBI y a los precios inmobiliarios.

**`borio_lowe_2002`** · resumen.
- El crecimiento rápido y sostenido del crédito, junto con alzas grandes de los precios de los
  activos, eleva la probabilidad de inestabilidad financiera, incluso con inflación baja.
- *Relación:* justifica analizar juntos los bloques de crédito y de precios de activos.

**`claessens_kose_terrones_2011`** · resumen.
- Muestra: 21 economías avanzadas, 1960–2007, con ciclos del crédito, de la vivienda y de las
  acciones.
- Los ciclos financieros son largos y severos, están sincronizados dentro de cada país y entre
  países (cada vez más), y se amplifican cuando coinciden las contracciones.
- *Relación:* respalda la idea de un ciclo común a varios bloques y el uso de episodios globales
  como referencia de validación.

**`claessens_kose_terrones_2012`** · resumen leído en una fuente secundaria.
- Muestra: 44 países, 1960–2010.
- Las recesiones con caídas de los precios de la vivienda o de las acciones son más largas y
  profundas.
- *Relación:* sustenta la relevancia macroeconómica de describir el régimen financiero. No afirmar
  que el Perú está en la muestra.

**`aikman_haldane_nelson_2015`** · solo localizada.
- Pertenece a la literatura del ciclo crediticio, pero no hay resumen leído.
- *Relación:* solo puede citarse como parte de esa literatura, con `\verificar`.

**`schuler_hiebert_peltonen_2015`** · texto parcial.
- Muestra: 13 países de la UE y la zona del euro, 1970–2013.
- Método: medida espectral de frecuencias comunes (*power cohesion*) y agregación con pesos
  variables según las correlaciones entre pares de indicadores.
- **Descartan el PCA** por problemas de comparabilidad entre países y de actualización en tiempo
  real.
- Resultados: ciclo de unos 7,2 años en promedio; concordancia con el ciclo económico de 67 %; el
  ciclo predice crisis mejor que la brecha crédito/PBI.
- *Relación:* es el antecedente más cercano del **EPCA**, porque sus pesos cambian con la estructura
  de correlaciones. Su crítica al PCA es un contrapunto que la tesis debe discutir: el EPCA hace
  explícita la variación de los pesos.

**`schuler_hiebert_peltonen_2020`** · resumen leído en una fuente secundaria.
- La duración de los ciclos difiere entre los países del G-7, contra el supuesto de duración común
  de la brecha de Basilea III.
- Los ciclos construidos como comovimiento de varias variables predicen crisis mejor que esa
  brecha.
- *Relación:* respalda medir el ciclo como fluctuación común de varias series, que es lo que
  resume el primer componente del PCA.

**`galati_et_al_2016`** · resumen del documento de trabajo DNB 495.
- Ojo: el título del documento de trabajo difiere del publicado.
- Muestra: Estados Unidos y cinco países europeos, 1970–2014.
- Método: modelo multivariado de componentes no observables (espacio de estados).
- Resultado: los ciclos financieros son más largos y amplios que los económicos, y su duración y
  amplitud varían en el tiempo y entre países.
- *Relación:* es la vía **confirmatoria** (modelo paramétrico) frente a la exploratoria de la tesis
  («datos primero»).

**`runstler_vlekke_2018`** · resumen.
- Encuentran ciclos grandes y largos del crédito y de la vivienda, correlacionados con un componente
  de mediano plazo del PBI (salvo en Alemania).
- *Relación:* la heterogeneidad entre países justifica estudiar el caso peruano por separado.

**`strohsal_proano_wolters_2019`** · versión DP 22/2015 del Bundesbank.
- Los puntos de giro y los filtros pasa-banda son descriptivos y exigen fijar de antemano una regla
  o un rango de frecuencias.
- Proponen un espectro paramétrico ARMA con *bootstrap*.
- Resultado: en Estados Unidos y el Reino Unido, el ciclo financiero dura unos 15 años.
- *Relación:* argumento a favor de «datos primero», porque los filtros imponen la frecuencia del
  ciclo. No atribuirle la parte de interacción internacional del artículo publicado.

**`hamilton_2018`** · resumen del NBER WP 23429.
- El filtro HP crea dinámica espuria, se comporta mal al final de la muestra y su parámetro de
  suavizamiento no tiene sustento estadístico.
- *Relación:* sostiene no usar HP y fijar de antemano la regla de tendencia (D1, D5).

**`harding_pagan_2002`** · resumen.
- Algoritmo de puntos de giro sobre el **nivel** de la serie, en la tradición de Burns y Mitchell.
- *Relación:* es la datación univariada alternativa a la datación multivariada de la tesis
  (Fisher sobre el primer componente) y es coherente con D1. El índice de concordancia es de 2006,
  obra **no fichada**.

## 2. Índices de estrés y validación con episodios

**`hollo_kremer_lo_duca_2012`** · texto parcial.
- El CISS agrega cinco subíndices (15 medidas) de la zona del euro con teoría de carteras y
  correlaciones variables, de modo que pesa más el estrés simultáneo en varios segmentos.
- Un VAR con umbral identifica el nivel de estrés que deprime la actividad.
- *Relación:* la estructura de correlaciones cambia en los episodios de estrés, que es la intuición
  del EPCA y del RV entre ventanas.

**`illing_liu_2006`** · contenido del WP 2003-14 del Banco de Canadá.
- Índice de estrés para Canadá, con análisis factorial, ponderaciones y GARCH.
- Se valida contra una **encuesta interna** que identifica los episodios de mayor estrés.
- *Relación:* es el antecedente directo de la validación externa de la tesis: regímenes contrastados
  con episodios fechados por una fuente ajena a las series (regla 6, D7, D18).

## 3. Regímenes y cambios estructurales

**`hamilton_1989`** · resumen.
- Los parámetros de una autorregresión siguen un proceso de Markov de estados discretos no
  observados.
- Datación de las recesiones del PNB de EE. UU.; caída permanente de alrededor de 3 % por recesión.
- *Relación:* es la referencia de la alternativa paramétrica de regímenes que la tesis no adopta.
  Contraste: en la tesis el régimen es una estructura de correlaciones **descrita**, no un estado
  latente **modelado**.

**`kim_nelson_1999`** · descripción institucional; DOI con `verificar`.
- Manual de modelos de espacio de estados con cambio de régimen (estimación clásica y por muestreo
  de Gibbs).

**`krolzig_1997`** · solo metadatos.
- Monografía sobre MS-VAR, la versión multivariada del enfoque de Hamilton. Citar sin atribuirle
  resultados.

**`bai_perron_1998`** · resumen.
- Múltiples quiebres con fechas desconocidas por mínimos cuadrados, con pruebas de *l* contra
  *l + 1* quiebres (estrategia secuencial).
- *Relación:* análogo econométrico de la partición de Fisher y de la regla K (D12, D17).

**`bai_perron_2003`** · resumen.
- Programación dinámica para el óptimo global de las fechas de quiebre (costo del orden de *T*²).
- *Relación:* sitúa la partición óptima de Fisher (1958) dentro de la segmentación óptima por
  mínimos cuadrados.

## 4. Detección de puntos de cambio

**`truong_oudre_vayatis_2020`** · texto del *preprint* arXiv v3.
- Organiza los métodos en función de costo, método de búsqueda (Opt, Pelt, BinSeg, *bottom-up*,
  ventana deslizante) y restricción sobre el número de cambios. Paquete de Python *ruptures*.
- *Relación:* la datación de la tesis se describe como costo cuadrático + búsqueda exacta + regla
  del número de tramos.
- Usar *ruptures* sería una decisión nueva: **no se propone aquí**.

**`aminikhanghahi_cook_2017`** · resumen.
- Revisión de métodos supervisados y no supervisados; los puntos de cambio son transiciones entre
  estados.
- *Relación:* cita general. No atribuirle una taxonomía concreta.

## 5. PCA y análisis multidimensional

**`pearson_1901`** y **`hotelling_1933`** · solo metadatos.
- Origen histórico del PCA, con la atribución habitual, sin detalles del texto.
- La paginación de Hotelling (417–441) es la de la primera entrega.

**`lebart_morineau_piron_1995`** · solo metadatos.
- Manual de la escuela francesa en que se inscriben la HFC y el EPCA (posición del asesor).
- Es candidato para cos² y contribuciones, pero no se verificó la sección: el `\pendiente` de
  `sec:cos2` sigue abierto.

## 6. Aprendizaje profundo (complemento, regla 5)

**`goodfellow_bengio_courville_2016`** · solo catálogo.
- Manual general de autoencoders y redes recurrentes.

**`chalapathy_chawla_2019`** · *preprint*, resumen.
- Revisión de detección de anomalías con aprendizaje profundo. El resumen **no menciona
  autoencoders ni series de tiempo**.
- Solo exploración: buscar fuentes revisadas por pares si se usa el error de reconstrucción como
  señal.

## 7. Perú y América Latina

**`gomez_gonzalez_et_al_2013`** · texto parcial; orden de autores con `verificar`.
- Ciclos del crédito y del PBI de Chile, Colombia y el **Perú** (1994T1–2012T2), con un filtro
  Christiano-Fitzgerald de corto y mediano plazo, análisis espectral y causalidad en frecuencia.
- En el Perú, la causalidad va del crédito al PBI en todas las frecuencias, y el PBI es más volátil
  que el crédito.
- *Relación:* es el antecedente peruano verificado más cercano después de Atoche Murrieta (2022) y
  Camiz et al. (2026). Su filtro fija las frecuencias de antemano, a diferencia de la vía
  exploratoria.

**`brandao_marques_perez_ruiz_2017`** · resumen; grafía con `verificar`.
- Índices de condiciones financieras (TVP-FAVAR) para seis países latinoamericanos, **Perú**
  incluido.
- Los mueven un ciclo de materias primas, un ciclo financiero global y episodios nacionales de
  estrés.
- *Relación:* respalda los episodios externos de referencia (materias primas, crisis global) y es un
  antecedente de reducción dimensional con estructura cambiante aplicada al Perú.

**`minaya_lupu_cabello_2017`** · resumen.
- Provisiones dinámicas y encajes condicionales en el Perú (registro de créditos 2004–2014): frenaron
  el crédito comercial en el auge y redujeron la dolarización hipotecaria.
- *Relación:* contexto de política para leer los regímenes del crédito y de su composición por
  moneda.

**`alvarado_vargas_2021`** · resumen; trabajo de pregrado.
- Indicador compuesto del ciclo financiero peruano (1999–2021) y regresión por cuantiles. Según el
  resumen, el efecto sobre el ciclo económico es mayor en las expansiones.
- *Relación:* muestra que hay literatura local reciente. **Usar con cautela**: no tiene revisión por
  pares y no sostiene hallazgos.

**Ya fichados:** `camiz_cerda_atoche_2026` (manuscrito; `verificar`) y `atoche_murrieta_2022`.

## Obras no verificadas (no están en el `.bib`)

| Obra | Motivo |
|---|---|
| Nivin y Pérez (2019), índice de condiciones financieras del Perú (BCRP, DT 2019-006 / REE 37) | Sitios del BCRP bloqueados (Incapsula); solo RePEc (secundaria) |
| BCRP DT 2022-002 (estrés financiero), *Moneda* 188 (índice de estrés) y DT 2024-012 (nuevos FCI) | Mismo bloqueo; autores no vistos |
| Repositorio PUCP, «El ciclo financiero global y las condiciones crediticias en el Perú» | Repositorio bloqueado (Anubis) |
| Pérez Forero (2016), BCRP DT 2016-013 | Solo IDEAS; trata el ciclo económico |
| Rabanal (2022), *Ola Financiera* | Verificada, pero sin Perú y sin nombre completo del autor: no agregada |
| Amaral et al. (2025), BIS Bulletin 113 | Verificada la página, pero sin mención del Perú ni del método: no agregada |
| Harding y Pagan (2006); Hodrick y Prescott (1997); Christiano y Fitzgerald (2003); Hamilton (1994) | No buscadas en esta iteración |

**Pedido a Roberto.** Descargar manualmente desde un navegador los cuatro documentos del BCRP y el
registro de la PUCP (lista arriba) para fichar los antecedentes peruanos que faltan.

## N-02 / D18

- **`congreso_2018`.** La fecha se describe como «evento peruano; externo al análisis en el sentido
  de D18», y la limitación explica la convención. N-02 queda cerrado en la ficha y en el registro.
- **`pcm_2020`.** Deja de calificarse como «interno»: con D18 es una fuente admisible para fechar.
  Que fije un extremo del episodio COVID-19 (por ejemplo, el inicio en el Perú) queda como **tema
  pendiente** en el registro, porque lo decide Roberto. El mes no cambiaría (2020-03, el mismo de
  `oms_2020b`); cambiaría la fuente citada. `episodios_referencia.csv` no se tocó. Sigue faltando su
  URL oficial.
- **Para el redactor y el editor.** La definición `def:episodio` y los textos de «Validación
  externa» deben alinearse con D18. No es tarea del bibliotecario.

## Conteos

- Marcas al commit `605803a`, contadas con `git grep`: sin cambios respecto de `09b9c26`.
  - Tesis: 52 `\verificar` y 14 `\pendiente`.
  - Informe: 52 notas `VERIFICAR`, 9 `[CITA PENDIENTE]` y 5 recuadros.
  - RmdF: 25; Rmd: 38; src: 6; NB05: 3; `06a`/`06b`: 10.
- El `.bib` pasa de 67 a 97 entradas, todas con ficha.
- Fichas FB-070 a FB-099. La numeración es correlativa propuesta.
