---
lang: es-PE
link-citations: false
---

::: {custom-style="Titulo preliminar"}
DEDICATORIA
:::

::: {custom-style="Marcador"}
[Texto por redactar por el tesista.]
:::

::: {custom-style="Salto"}
 
:::

::: {custom-style="Titulo preliminar"}
AGRADECIMIENTOS
:::

::: {custom-style="Marcador"}
[Texto por redactar por el tesista.]
:::

::: {custom-style="Salto"}
 
:::

::: {custom-style="Titulo preliminar"}
COPIA DE DOCUMENTOS
:::

::: {custom-style="Marcador"}
[Según la Guía N.° 2, en esta sección se incorporan, después de la sustentación, el acta de sustentación, el certificado de idioma extranjero, el grado de bachiller, el certificado de notas o de finalización de estudios y los recibos de pago correspondientes.]
:::

::: {custom-style="Salto"}
 
:::

::: {custom-style="Titulo preliminar"}
ÍNDICE DE CONTENIDOS
:::

[[TOC]]

::: {custom-style="Salto"}
 
:::

::: {custom-style="Titulo preliminar"}
LISTA DE TABLAS
:::

[[LISTA_TABLAS]]

::: {custom-style="Titulo preliminar"}
LISTA DE FIGURAS
:::

[[LISTA_FIGURAS]]

# RESUMEN

En esta investigación se estudió el ciclo financiero peruano con técnicas exploratorias multivariadas y de aprendizaje automático. Se analizaron {{nSeries}} series mensuales del Banco Central de Reserva del Perú (BCRP), sin transformar, entre {{fechaInicioNiveles}} y {{fechaFinDatos}} ({{nMesesNiveles}} meses): crédito, liquidez, tasas de interés, precios, actividad, reservas, mercado bursátil y riesgo país. La cadena metodológica combinó el análisis de componentes principales (PCA), la clasificación factorial jerárquica (HFC), el análisis evolutivo de componentes principales (EPCA) y la partición óptima de Fisher; los autoencoders y las redes LSTM se emplearon como complemento. Cada resultado se contrastó con nulos simulados y con remuestreo por bloques, y los cortes de régimen se compararon con episodios fechados por fuentes independientes de los datos. En este informe preliminar, el PCA y la HFC identificaron tres bloques estables de series: tendencia común, tasas de política y riesgo de mercado. El primer eje del PCA ({{inerciaPCUnoNiveles}} % de la inercia) correspondió a la tendencia común y no superó un nulo de caminatas aleatorias con deriva; el eje de tasas sí lo superó. Las variaciones de la estructura de correlación detectadas por el EPCA no se distinguieron de las que produciría una estructura constante (menor *p* = {{oePMin}}). La datación con los *scores* suavizados del PCA encontró {{datacionKPrincipal}} regímenes, con cortes en su mayoría estables bajo remuestreo y tres de ellos compatibles con la crisis financiera global, el colapso de los precios de las materias primas y la pandemia de COVID-19. En una corrida exploratoria, el autoencoder no mejoró la reconstrucción fuera de muestra del PCA. Se concluyó que la estructura transversal de las series es el resultado más sólido del avance y que la clasificación de los regímenes en fases requiere una regla que no confunda ciclo con tendencia.

**Palabras clave:** ciclo financiero; análisis de componentes principales; clasificación factorial jerárquica; análisis evolutivo; datación de regímenes.

# ABSTRACT

This research studied the Peruvian financial cycle using multivariate exploratory techniques and machine learning. {{nSeriesEn}} untransformed monthly series from the Central Reserve Bank of Peru (BCRP) were analysed from January 2007 to December 2025 ({{nMesesNiveles}} months): credit, liquidity, interest rates, prices, activity, reserves, the stock market and country risk. The methodological chain combined principal component analysis (PCA), hierarchical factor classification (HFC), evolutionary principal component analysis (EPCA) and Fisher's optimal partition; autoencoders and LSTM networks were used as a complement. Each result was tested against simulated null models and block resampling, and regime breaks were compared with episodes dated by sources independent of the data. In this preliminary report, PCA and HFC identified three stable blocks of series: common trend, policy rates and market risk. The first PCA axis ({{inerciaPCUnoNivelesEn}} % of inertia) corresponded to the common trend and did not exceed a null of random walks with drift; the interest-rate axis did. The changes in correlation structure detected by EPCA could not be distinguished from those produced by a constant structure (smallest *p* = {{oePMinEn}}). Dating on the smoothed PCA scores found {{datacionKPrincipal}} regimes, with breaks mostly stable under resampling and three of them compatible with the global financial crisis, the commodity price collapse and the COVID-19 pandemic. In an exploratory run, the autoencoder did not improve on the out-of-sample reconstruction of PCA. It was concluded that the cross-sectional structure of the series is the most solid result so far, and that classifying regimes into phases requires a rule that does not confuse cycle with trend.

**Keywords:** financial cycle; principal component analysis; hierarchical factor classification; evolutionary analysis; regime dating.

# INTRODUCCIÓN

El ciclo financiero describe las fases de expansión y contracción del crédito y de los precios de los activos. A diferencia del ciclo económico, no existe una variable que lo observe directamente: la información está repartida entre muchas series —crédito, liquidez, tasas de interés, precios, mercado bursátil, riesgo país— que se mueven juntas solo en parte y cuya relación puede cambiar en el tiempo. Medirlo exige, por tanto, métodos que resuman muchas series a la vez y que permitan ver si esa síntesis se mantiene o cambia.

Para el Perú, los trabajos más cercanos aplicaron análisis exploratorios multivariados a series del BCRP [@atoche_murrieta_2022; @camiz_cerda_atoche_2026]. Esos trabajos describen la estructura de las series y su evolución, pero no clasifican los períodos en fases del ciclo, no incorporan modelos de aprendizaje profundo y no cubren el período posterior a la pandemia. Esta tesis aborda esos tres puntos: propone una metodología que combina el PCA, la HFC y el EPCA con autoencoders y redes LSTM, la aplica a {{nSeries}} series mensuales del BCRP entre 2007 y 2025, y contrasta los regímenes que encuentra con episodios cuya fecha proviene de documentos independientes de los datos.

La investigación es cuantitativa y de nivel exploratorio y descriptivo. Su rasgo metodológico central es que cada resultado se compara con un nulo simulado que reproduce las propiedades que podrían generarlo por azar, en particular la tendencia común de las series, y se somete a remuestreo por bloques de meses para medir su estabilidad.

Este documento es un **informe preliminar**. Los datos, el análisis exploratorio y la datación de regímenes con el PCA están terminados; la interpretación de los resultados todavía no se ha discutido con el asesor; los modelos de aprendizaje profundo se presentan como una corrida exploratoria, y la clasificación de los regímenes en fases sigue abierta. El Capítulo I presenta el protocolo de la investigación; el Capítulo II, el marco teórico; el Capítulo III, los resultados obtenidos hasta la fecha, su discusión y el estado de las hipótesis, y el Capítulo IV, las conclusiones y recomendaciones preliminares. Los anexos contienen la matriz de consistencia, el estado del avance frente al plan de la ficha de inscripción y el estado de la revisión bibliográfica.

# CAPÍTULO I. PROTOCOLO DE LA INVESTIGACIÓN

## 1.1 Identificación y descripción del problema de estudio

El ciclo financiero es un fenómeno latente. @drehmann_borio_tsatsaronis_2012 lo caracterizan, para siete economías desarrolladas, por el comportamiento conjunto del crédito y de los precios inmobiliarios, y encuentran un componente de mediano plazo, de 8 a 30 años, más largo que el ciclo económico tradicional, cuyos picos coinciden con crisis bancarias. En una economía como la peruana, con series financieras más cortas y una estructura distinta, esa caracterización no puede trasladarse sin más: el problema práctico es identificar qué información común contienen los indicadores disponibles y si esa información cambia de un período a otro.

El BCRP publica decenas de indicadores mensuales relacionados con el crédito, la liquidez, las tasas de interés, los precios, la actividad, el sector externo y los mercados financieros. Estas series presentan tres dificultades: están muy correlacionadas entre sí, por lo que cualquier síntesis debe separar lo común de lo específico; casi todas crecen en el tiempo, de modo que buena parte de su correlación puede deberse solo a la tendencia [@granger_newbold_1974], y su relación puede variar entre períodos, lo que hace que un análisis global oculte cambios importantes.

@atoche_murrieta_2022 y @camiz_cerda_atoche_2026 abordaron esta situación con PCA, HFC y EPCA sobre series del BCRP hasta 2020, e identificaron tres grupos de series —salud económica y financiera, tasas de interés y riesgo de mercado— y transiciones estructurales asociadas a episodios internacionales y locales. Quedan abiertos tres aspectos: (a) la clasificación explícita de los períodos en fases del ciclo, que esos trabajos no realizan; (b) la incorporación de modelos de aprendizaje profundo, capaces de captar relaciones no lineales y dependencia temporal [@hinton_salakhutdinov_2006; @hochreiter_schmidhuber_1997], y su comparación con los métodos exploratorios, y (c) la extensión al período posterior a la pandemia.

### 1.1.1 Formulación del problema general

¿Cómo identificar, fechar y caracterizar los regímenes del ciclo financiero peruano a partir de los indicadores macrofinancieros mensuales del BCRP, combinando métodos exploratorios evolutivos y aprendizaje automático, y cómo se comparan esos métodos entre sí?

### 1.1.2 Formulación de los problemas específicos

- **PE1.** ¿Qué indicadores macrofinancieros mensuales del BCRP permiten construir una base de datos trazable desde la fuente para estudiar el ciclo financiero peruano?
- **PE2.** ¿Cómo se estructura la correlación entre esas series, qué grupos homogéneos forman y cuán estable es esa estructura en el tiempo?
- **PE3.** ¿Qué representaciones latentes no lineales producen los autoencoders y las redes LSTM a partir de esas series, y qué aportan frente al PCA?
- **PE4.** ¿Qué regímenes pueden fecharse y clasificarse en fases con estos métodos, y en qué medida se corresponden con episodios fechados por fuentes independientes de los datos?
- **PE5.** ¿Cómo se comparan los métodos según su interpretabilidad, estabilidad temporal y capacidad descriptiva, incluso en un contexto simulado con regímenes conocidos?

### 1.1.3 Justificación del estudio

- **Justificación teórica.** La investigación contrasta, sobre los mismos datos, dos familias de métodos: la exploratoria, que describe la estructura sin postular un modelo generador [@camiz_et_al_2020; @camiz_roig_2011], y la de aprendizaje profundo, que puede representar relaciones no lineales y dependencia temporal. Se sabe que un autoencoder lineal con error cuadrático recupera el subespacio de las primeras componentes principales [@baldi_hornik_1989]; lo que la tesis evalúa es si las versiones no lineales y temporales aportan información adicional en un contexto de muestra pequeña.
- **Justificación metodológica.** Propone contrastar cada resultado exploratorio con nulos simulados que reproducen la tendencia y la dependencia temporal de las series, y validar los cortes de régimen con episodios fechados por documentos independientes de los datos. Ambos procedimientos reducen el riesgo de interpretar como estructura lo que es tendencia o ruido.
- **Justificación práctica.** Una datación de regímenes reproducible, con datos, código y fuentes públicos, sirve como referencia para el seguimiento del sistema financiero peruano. La ventana 2007–2025 incluye la crisis financiera global, el colapso de los precios de las materias primas, la pandemia de COVID-19 y el período posterior.

### 1.1.4 Alcance del estudio

- **Temático.** Estructura conjunta de los indicadores macrofinancieros y sus cambios de régimen. No se estiman modelos causales ni de pronóstico.
- **Espacial.** Sistema financiero y macroeconomía del Perú, según las estadísticas del BCRP.
- **Temporal.** Datos mensuales de enero de 2007 a diciembre de 2025, congelados antes de los cálculos.

## 1.2 Objetivos

### 1.2.1 Formulación del objetivo general

Proponer y evaluar una metodología que combine técnicas exploratorias evolutivas (PCA, HFC y EPCA) y modelos de aprendizaje profundo (autoencoders y redes LSTM) para identificar cambios de régimen en el ciclo financiero peruano con indicadores macrofinancieros del BCRP.

### 1.2.2 Formulación de los objetivos específicos

- **OE1.** Construir una base de datos mensual de indicadores macrofinancieros del BCRP, trazable desde la fuente.
- **OE2.** Analizar la estructura de correlación de las series, sus grupos homogéneos y su estabilidad en el tiempo con PCA, HFC y EPCA.
- **OE3.** Construir representaciones latentes no lineales con autoencoders y redes LSTM.
- **OE4.** Fechar regímenes, clasificarlos en fases y contrastarlos con episodios fechados por fuentes independientes de los datos.
- **OE5.** Comparar los métodos según su interpretabilidad, estabilidad temporal y capacidad descriptiva, incluso en un contexto simulado con regímenes conocidos.

Los objetivos desarrollan el resumen y el plan de trabajo de la ficha de inscripción de la tesis.

## 1.3 Hipótesis y variables

El estudio es exploratorio: sus métodos centrales describen la muestra sin postular un modelo que la genere, los episodios de referencia son pocos y los resultados no se generalizan a otras economías. Por ello, las hipótesis se formulan como **hipótesis de trabajo**, que se evalúan por la convergencia de la evidencia y que indican de antemano qué resultado contaría en su contra.

### 1.3.1 Formulación de la hipótesis general

La estructura conjunta de los indicadores macrofinancieros del BCRP entre 2007 y 2025 contiene regímenes identificables, organizados en pocos bloques de series, cuyos cortes se corresponden con episodios fechados externamente; los modelos de aprendizaje profundo aportan sobre esa estructura información que el PCA no capta.

### 1.3.2 Formulación de las hipótesis específicas

- **HE1 (no estacionariedad estructural).** La estructura de correlación no es constante entre 2007 y 2025: hay intervalos estables separados por transiciones. *En contra:* que las ventanas sucesivas resulten tan similares como cabría esperar bajo una estructura constante.
- **HE2 (organización en grupos).** Las series se organizan en pocos grupos homogéneos que se corresponden con los bloques identificados por @camiz_cerda_atoche_2026: salud económica y financiera, tasas de interés y riesgo del mercado financiero. *En contra:* grupos inestables bajo remuestreo o sin correspondencia con esos bloques.
- **HE3 (correspondencia con episodios).** Los regímenes se corresponden, dentro de una tolerancia declarada de antemano, con episodios fechados externamente. *En contra:* cortes sin relación con ningún episodio, o que dependan de la regla que fija su número.
- **HE4 (complementariedad).** Los autoencoders y las redes LSTM aportan información sobre la dinámica y la atipicidad del sistema que el PCA no capta. *En contra:* que no mejoren a su anclaje lineal en ningún criterio fuera de muestra, o que sus resultados cambien con la semilla aleatoria.

### 1.3.3 Variables

Siguiendo la Guía N.° 2, la variable dependiente es la que describe el problema de estudio y la independiente, la que describe la solución propuesta. En un diseño exploratorio no se postula una relación causal entre ambas: la variable independiente es el procedimiento con que se mide la dependiente. La Tabla 1 resume las variables, sus dimensiones y sus indicadores.

::: {custom-style="Rotulo"}
**Tabla 1**\
*Variables, dimensiones e indicadores*
:::

| Variable | Dimensión | Indicadores |
|---|---|---|
| **Dependiente:** regímenes del ciclo financiero peruano | Estructura de correlación | Inercia y cargas por eje; correlación de cada eje con el tiempo |
| | Grupos de series | Clases de la HFC; reproducción de la partición bajo remuestreo |
| | Estabilidad temporal | Similitud entre ventanas sucesivas del EPCA; *p* frente al nulo de estructura constante |
| | Datación y fase | Cortes de régimen; frecuencia de cada corte bajo remuestreo; distancia a los episodios de referencia; etiqueta de fase |
| **Independiente:** metodología híbrida de reducción dimensional y aprendizaje automático | Métodos exploratorios | PCA, HFC, EPCA, partición óptima de Fisher |
| | Aprendizaje profundo | Autoencoder y LSTM-autoencoder: error de reconstrucción fuera de muestra; estabilidad frente a la semilla |

::: {custom-style="Nota"}
*Nota.* Los datos observados son {{nSeries}} series mensuales del BCRP (Tabla 2). Elaboración propia.
:::

## 1.4 Metodología

### 1.4.1 Tipo de investigación

- **Por su enfoque:** cuantitativa.
- **Por su nivel:** exploratoria y descriptiva, con un componente comparativo entre métodos.
- **Por su diseño:** no experimental, longitudinal y retrospectivo: se observan series de tiempo ya publicadas, sin manipular variables.
- **Métodos:** analítico e inductivo. La contrastación con nulos simulados y con episodios externos aporta un componente hipotético-deductivo a las hipótesis de trabajo.

### 1.4.2 Población y muestra

La **población** está formada por los indicadores macrofinancieros mensuales que publica el BCRP. La **muestra** es no probabilística, por criterio: {{nSeries}} series que cubren los ámbitos de la ficha de inscripción (crédito, liquidez, tasas de interés, inflación, mercado bursátil y tipo de cambio), más la actividad, las reservas internacionales y el riesgo país, con información continua de {{fechaInicioNiveles}} a {{fechaFinDatos}} ({{nMesesNiveles}} meses) (Tabla 2). Quedaron fuera tres series disponibles: el crédito total, por su colinealidad con los créditos por tipo; el IPC subyacente, que se conserva solo como serie de contraste, y la liquidez M2, casi colineal con M3 en niveles, que pesaría dos veces en el PCA.

::: {custom-style="Rotulo"}
**Tabla 2**\
*Series analizadas y su código en la base de datos del BCRP*
:::

[[TABLA_SERIES]]

::: {custom-style="Nota"}
*Nota.* TAMN: tasa activa en moneda nacional; TIPMN: tasa pasiva en moneda nacional; BVL: Bolsa de Valores de Lima; EMBIG: diferencial de rendimiento de los bonos soberanos peruanos. Elaboración propia con datos del BCRP.
:::

### 1.4.3 Técnicas e instrumentos de recolección de datos

La técnica es el análisis documental de fuentes estadísticas oficiales. Las series se descargaron de la base de datos estadística del BCRP mediante su código, se verificaron serie por serie (unidades, frecuencia, cobertura y valores faltantes) y se consolidaron en una base de datos multivariada. La base se congeló antes de cualquier cálculo, con una huella digital de cada archivo, para que ningún resultado dependa de revisiones posteriores de la fuente. El instrumento es la propia base de datos, documentada en un diccionario de datos.

### 1.4.4 Técnicas de análisis y procesamiento de datos

El análisis principal usa las series sin transformar, estandarizadas; las series transformadas (logaritmos y diferencias) se reservan para un análisis de robustez. La secuencia es la siguiente:

1. **PCA global.** Estructura de correlación y número de ejes, con los criterios de Kaiser, de la vara quebrada y el análisis paralelo [@horn_1965]. La adecuación muestral se evalúa con la medida KMO y la prueba de esfericidad de Bartlett, esta última corregida por el tamaño efectivo de la muestra.
2. **Nulos de tendencia.** Se simulan series independientes con la misma tendencia o deriva que las observadas, para saber qué inercia tendrían los ejes si no hubiera estructura común.
3. **HFC** [@camiz_et_al_2020]. Agrupa las series; su estabilidad se mide con bootstrap por bloques de meses.
4. **EPCA.** PCA en ventanas móviles de 24, 36, 48 y 60 meses, con pesos uniformes y gaussianos. Se mide cuánto cambia la estructura entre ventanas y se contrasta con un nulo de estructura constante.
5. **Datación.** Partición óptima de Fisher, con el procedimiento de @camiz_cerda_atoche_2026, sobre los tres primeros *scores* del PCA suavizados con una media móvil de 12 meses, con tramos de al menos 12 meses. Los cortes se comparan con los episodios de referencia con una tolerancia de tres meses.
6. **Aprendizaje profundo.** Autoencoders y LSTM-autoencoder, comparados con el PCA fuera de muestra mediante validación por bloques y *walk-forward*.

El procesamiento se realizó en Python, con una réplica en R que reproduce los mismos resultados. Datos, código y resultados están en un repositorio público (https://github.com/RobertoSam/Tesis-modelamiento-matematico).

# CAPÍTULO II. MARCO TEÓRICO

## 2.1 Antecedentes de la investigación

Los antecedentes se presentan en orden cronológico, del más antiguo al más reciente. Se incluyen solo trabajos cuyo texto se leyó total o parcialmente; los métodos cuyas fuentes originales aún no se han leído se listan en el Anexo 3.

**Camiz, Maulucci y Roig (2010).** @camiz_maulucci_roig_2010 estudian 23 series sincrónicas de anillos de árboles cuya estructura de correlación no es estable en el tiempo. Combinan un PCA global, el análisis Statis dual sobre subtablas de 25 años y el PCA evolutivo en ventanas móviles. El PCA global explica solo el 48 % de la varianza con tres componentes, y el Statis dual identifica años de quiebre en la estructura de correlación. Es el antecedente metodológico del EPCA y lo enmarca como herramienta exploratoria: describe la muestra y no se generaliza a una población.

**Camiz y Roig (2011).** @camiz_roig_2011 aplican el mismo enfoque a nueve cronologías de *Araucaria araucana* en un período común de 492 años. Combinan el PCA con clasificación jerárquica de los años, la HFC sobre las series y el EPCA con ventanas de 25 y 50 años. Sobre la serie del primer valor propio del EPCA aplican la partición óptima de Fisher, que divide el período en cuatro intervalos homogéneos, y analizan cada uno con un PCA propio. Este procedimiento es el precedente directo de la datación de regímenes de la tesis.

**Drehmann, Borio y Tsatsaronis (2012).** @drehmann_borio_tsatsaronis_2012 caracterizan el ciclo financiero de siete economías desarrolladas con datos trimestrales desde 1960, mediante filtros de frecuencia y análisis de puntos de giro. El crédito y los precios inmobiliarios comparten un componente de mediano plazo (8 a 30 años), cuyos picos coinciden con las crisis bancarias de origen doméstico de la muestra; los precios bursátiles se comportan de forma distinta. Su método requiere series largas, por lo que en esta tesis se usa como referencia conceptual y no como procedimiento.

**Camiz y Pillar (2018).** @camiz_pillar_2018 comparan por simulación diez reglas para decidir cuántas componentes principales retener, entre ellas el criterio de Kaiser, la vara quebrada y un procedimiento de bootstrap con permutación. Según su resumen, la generalización de Rencher de la prueba de Bartlett y el bootstrap de Pillar dan los mejores resultados. El trabajo sustenta la combinación de criterios con que la tesis decide el número de ejes.

**Camiz, Spada, Denimal y Piraino (2020).** @camiz_et_al_2020 exponen la HFC, un método propuesto por Denimal que agrupa variables de forma jerárquica y resume cada grupo con un factor, y la comparan con el PCA en cinco cronologías de *Pinus pinea*. Tres de las cinco cronologías comparten una señal común y pueden sintetizarse en una sola, mientras que las otras dos deben mantenerse separadas. Es el fundamento metodológico de la HFC en la tesis.

**Atoche Murrieta (2022).** @atoche_murrieta_2022 estima el ciclo financiero peruano con 17 series mensuales del BCRP, de 1999 a 2020, mediante PCA, HFC y PCA evolutivo con pesos gaussianos. Según su resumen, identifica tres componentes: una de largo plazo, asociada a la evolución del sistema financiero; otra de mediano plazo, ligada a las tasas activas y pasivas, y una tercera asociada a la volatilidad del mercado financiero.

**Tuhin, Nobi, Rakib y Lee (2025).** @tuhin_et_al_2025 entrenan un LSTM-autoencoder sobre los retornos diarios de 375 acciones del índice S&P 500 entre 2000 y 2022, construyen con los pesos de la capa central redes anuales de influencia entre acciones y muestran que sus propiedades topológicas cambian de forma distintiva en cinco crisis financieras. Los autores advierten que el enfoque requiere muchos datos, una limitación relevante para series mensuales macrofinancieras como las del BCRP.

**Camiz, Cerda Hernández y Atoche Murrieta (2026).** En un manuscrito aún no publicado, @camiz_cerda_atoche_2026 aplican PCA, HFC y EPCA a 17 series mensuales del BCRP entre 1999 y 2020. La HFC identifica tres grupos: salud económica y financiera, tasas de interés y riesgo del mercado financiero. Sobre el primer valor propio del EPCA, con ventana gaussiana de 48 meses, fechan transiciones con la partición óptima de Fisher y eligen el número de cortes con el índice de Caliński y Harabasz. Es el antecedente más directo de la tesis.

**Vacío identificado.** Ningún trabajo peruano revisado incorpora autoencoders o redes LSTM, ni clasifica de forma explícita los regímenes en fases, ni cubre el período posterior a 2020.

## 2.2 Bases teóricas

### 2.2.1 El ciclo financiero

El ciclo financiero es el movimiento conjunto, de expansión y contracción, del crédito y de los precios de los activos. @drehmann_borio_tsatsaronis_2012 lo distinguen del ciclo económico por su duración y su relación con las crisis bancarias. Con los 19 años de datos disponibles en esta tesis no es posible identificar ciclos de 8 a 30 años, de modo que el objeto de estudio no es el ciclo completo, sino los **regímenes** que los datos permiten distinguir.

### 2.2.2 Análisis exploratorio y tendencia

La tesis privilegia el análisis exploratorio: describir la estructura de los datos antes que imponer un modelo. Por eso el análisis principal usa las series sin transformar. Esta elección tiene un costo: @granger_newbold_1974 mostraron que series con tendencia pueden parecer relacionadas sin estarlo. En niveles, las tendencias comunes pueden dominar la correlación; por ello, cada resultado se contrasta con nulos que reproducen ese efecto.

### 2.2.3 Régimen, fase y validación externa

Un **régimen** es un intervalo de meses contiguos en el que la estructura de las series es relativamente homogénea. Una **fase** es la etiqueta —expansión, contracción o transición— que se asigna a cada régimen después de detectarlo. Los cortes se comparan con episodios cuya fecha proviene de documentos independientes de las series (Tabla 3): la bibliografía sirve para identificar los eventos candidatos, pero no para fecharlos. Un corte es compatible con un episodio si dista de él tres meses o menos; seis meses se usan como sensibilidad.

::: {custom-style="Rotulo"}
**Tabla 3**\
*Episodios de referencia y fuentes de sus fechas*
:::

| Episodio | Inicio | Fin | Fuente del inicio | Fuente del fin |
|---|---|---|---|---|
| Crisis financiera global | 2008-09 | 2009-06 | @lehman_brothers_2008 | @nber_2010 |
| *Taper tantrum* | 2013-05 | 2013-12 | @bernanke_2013 | @reserva_federal_2013 |
| Colapso de las materias primas | 2014-06 | 2016-01 | @stocker_et_al_2015 | @fmi_2016 |
| Renuncia de Kuczynski (caso Odebrecht) | 2018-03 | Puntual | @congreso_2018 | — |
| Guerra comercial EE. UU.–China | 2018-06 | 2020-01 | @ustr_2018 | @ustr_2020 |
| COVID-19 | 2020-03 | 2020-04 | @oms_2020b | @nber_2021 |

::: {custom-style="Nota"}
*Nota.* La fecha es la del evento o anuncio, no la de su efecto en el Perú. Elaboración propia.
:::

### 2.2.4 Fundamentos matemáticos de los métodos

Sea $X\in\mathbb{R}^{n\times p}$ la matriz de datos estandarizados, con $n$ meses y $p$ series, y $R=\tfrac1n X^\top X$ su matriz de correlaciones.

**Análisis de componentes principales.** Con la descomposición espectral $R=V\Lambda V^\top$, $\lambda_1\ge\dots\ge\lambda_p$, los *scores* son $F=XV$ y la inercia del eje $k$ es $\lambda_k/p$. La carga de la serie $j$ en el eje $k$ es $\sqrt{\lambda_k}\,v_{jk}$, su correlación con el eje. Con $d$ ejes, $X\approx F_dV_d^\top$ es la mejor aproximación de rango $d$ en norma de Frobenius.

**Clasificación factorial jerárquica.** Parte de $p$ clases de una serie. Cada clase se representa por un factor: el primer componente principal de sus series. En cada paso se hace un PCA de los factores de cada par de clases y se fusionan las dos cuyo PCA tiene el menor segundo valor propio, es decir, las que mejor se resumen con un solo factor [@camiz_et_al_2020].

**Análisis evolutivo de componentes principales.** Para una ventana de ancho $w$ que empieza en el mes $i$, con pesos $\omega_t\ge0$ y $\sum_t\omega_t=1$, la correlación ponderada es

$$
r^{(i)}_{jl}=\frac{\sum_{t}\omega_t\,(x_{tj}-\bar x_j)(x_{tl}-\bar x_l)}{\sqrt{\sum_t\omega_t(x_{tj}-\bar x_j)^2}\sqrt{\sum_t\omega_t(x_{tl}-\bar x_l)^2}},
$$

con medias ponderadas $\bar x_j$. Los pesos son uniformes o gaussianos centrados en la ventana. El PCA de cada $R^{(i)}$ da valores propios y cargas que evolucionan en el tiempo [@camiz_maulucci_roig_2010].

**Similitud entre ventanas.** Dos configuraciones $A$ y $B$ de las mismas $p$ series se comparan con el coeficiente RV,

$$
\mathrm{RV}(A,B)=\frac{\operatorname{tr}(AA^\top BB^\top)}{\sqrt{\operatorname{tr}\big((AA^\top)^2\big)\operatorname{tr}\big((BB^\top)^2\big)}}\in[0,1],
$$

que vale 1 cuando ambas definen el mismo subespacio con las mismas proporciones.

**Partición óptima de Fisher.** Dada una trayectoria $z_1,\dots,z_n\in\mathbb{R}^d$, se buscan $K$ segmentos contiguos $S_1,\dots,S_K$ que minimicen $\sum_{k}\sum_{t\in S_k}\lVert z_t-\bar z_{S_k}\rVert^2$, con $\lvert S_k\rvert\ge12$. La solución exacta se obtiene por programación dinámica, y $K$ se elige con la caída de la suma de cuadrados y el índice de Caliński y Harabasz, como en @camiz_cerda_atoche_2026.

**Autoencoder.** Un codificador $g_\phi:\mathbb{R}^p\to\mathbb{R}^d$ y un decodificador $h_\theta:\mathbb{R}^d\to\mathbb{R}^p$ se entrenan para minimizar $\tfrac1n\sum_t\lVert x_t-h_\theta(g_\phi(x_t))\rVert^2$. Si ambos son lineales, el óptimo genera el mismo subespacio que el PCA de $d$ ejes [@baldi_hornik_1989]. Las versiones profundas [@hinton_salakhutdinov_2006] y con eliminación de ruido [@vincent_et_al_2008] introducen no linealidad.

**Redes LSTM y LSTM-autoencoder.** Las redes LSTM [@hochreiter_schmidhuber_1997] son redes recurrentes con una celda de memoria regulada por compuertas, diseñadas para conservar información a lo largo de secuencias largas. El LSTM-autoencoder codifica ventanas de meses consecutivos en un vector latente y las reconstruye [@srivastava_mansimov_salakhutdinov_2015]; ambas variantes se evalúan frente a su anclaje lineal, el PCA.

## 2.3 Definición de términos

- **Ciclo financiero:** movimiento conjunto de expansión y contracción del crédito y de los precios de los activos [@drehmann_borio_tsatsaronis_2012].
- **Régimen:** intervalo de meses contiguos en el que la estructura de las series es relativamente homogénea.
- **Fase:** etiqueta (expansión, contracción o transición) asignada a un régimen después de detectarlo.
- **Episodio de referencia:** evento con fecha documentada por una fuente independiente de las series, usado para validar los cortes.
- **Inercia:** proporción de la variabilidad total de las series estandarizadas que resume un eje.
- **Carga:** correlación entre una serie y un eje del PCA.
- ***Score*:** coordenada de un mes en un eje del PCA.
- **Clasificación factorial jerárquica (HFC):** clasificación jerárquica de variables en la que cada grupo se resume con un factor [@camiz_et_al_2020].
- **Análisis evolutivo de componentes principales (EPCA):** PCA aplicado en ventanas móviles para observar cómo cambia la estructura de correlación [@camiz_maulucci_roig_2010].
- **Coeficiente RV:** medida, entre 0 y 1, de la similitud entre dos configuraciones de las mismas variables.
- **Partición óptima de Fisher:** división de una secuencia en tramos contiguos que minimiza la suma de cuadrados dentro de los tramos.
- **Nulo simulado:** conjunto de series artificiales que reproduce una propiedad de los datos (tendencia, dependencia temporal o estructura constante) y sirve de referencia para juzgar si un resultado podría deberse a ella.
- **Bootstrap por bloques:** remuestreo de bloques de meses consecutivos que conserva la dependencia temporal de las series.
- **Tamaño efectivo de muestra:** número de observaciones independientes equivalente a una muestra autocorrelacionada.
- **Autoencoder:** red neuronal que comprime los datos en un espacio latente de menor dimensión y los reconstruye [@hinton_salakhutdinov_2006].
- **LSTM:** red recurrente con celdas de memoria y compuertas, capaz de modelar dependencia temporal larga [@hochreiter_schmidhuber_1997].

# CAPÍTULO III. DESARROLLO DEL TRABAJO DE INVESTIGACIÓN

## 3.1 Análisis de los datos y resultados

Los resultados corresponden al análisis principal, con las {{nSeries}} series en niveles. Su interpretación es preliminar y todavía no se ha discutido con el asesor.

### 3.1.1 Las series analizadas

La Figura 1 muestra las {{nSeries}} series en sus unidades originales, con los episodios de referencia sombreados. Casi todas crecen de forma sostenida en el período; las excepciones son las tasas de interés, que siguen el ciclo de la política monetaria, y el EMBIG, que presenta picos en los episodios de tensión.

::: {custom-style="Rotulo"}
**Figura 1**\
*Series analizadas en sus unidades originales*
:::

![](fig/avance_series_niveles.png){width=100%}

::: {custom-style="Nota"}
*Nota.* En gris, los episodios de la Tabla 3; la línea discontinua marca el episodio puntual de marzo de 2018. Elaboración propia con datos del BCRP.
:::

### 3.1.2 Estructura de correlación

La correlación entre las series es muy alta en un bloque grande —crédito, liquidez, precios, actividad y reservas— y menor en las tasas y en los indicadores de mercado (Figura 2). Gran parte de esa correlación proviene de la tendencia común: al quitar a cada serie su tendencia lineal, el bloque se debilita y aparecen relaciones de signo distinto (Figura 3).

::: {custom-style="Rotulo"}
**Figura 2**\
*Matriz de correlación de las series en niveles*
:::

![](fig/05_correlaciones.png){width=80%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura 3**\
*Matriz de correlación de las series sin su tendencia lineal*
:::

![](fig/05_correlaciones_sin_tendencia.png){width=80%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

### 3.1.3 Análisis de componentes principales

Los tres primeros ejes explican el {{inerciaPCUnoNiveles}} %, el {{inerciaPCDosNiveles}} % y el {{inerciaPCTresNiveles}} % de la inercia. El criterio de Kaiser retiene {{kaiserNiveles}} ejes; el análisis paralelo y la vara quebrada, {{hornNiveles}} (Figura 4). Se trabaja con tres ejes porque el tercero tiene una lectura clara y es estable bajo remuestreo. La medida KMO es alta ({{kmoGlobalNiveles}}). Sin embargo, por la fuerte autocorrelación de las series, el tamaño efectivo de la muestra es de unas {{nEfMedianaNiveles}} observaciones independientes, y con él el estadístico de Bartlett pasa de {{chiBartlettNiveles}} a {{chiBartlettNefNiveles}} (*p* = {{pBartlettNefNiveles}}).

::: {custom-style="Rotulo"}
**Figura 4**\
*Valores propios del PCA frente al análisis paralelo y la vara quebrada*
:::

![](fig/05_pca_sedimentacion.png){width=60%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Tabla 4**\
*Cargas de las series en los tres primeros ejes del PCA*
:::

[[TABLA_CARGAS]]

::: {custom-style="Nota"}
*Nota.* En negrita, las cargas con valor absoluto igual o mayor que 0,6. Elaboración propia con datos del BCRP.
:::

La Tabla 4 permite leer los tres ejes:

- **Eje 1, tendencia común.** Cargan los saldos, los precios y la actividad, y la TAMN en sentido opuesto ({{cargaTamnPCUno}}). Su coordenada está casi perfectamente correlacionada con el tiempo (*r* = {{rTiempoPCUnoNiveles}}). Series independientes con deriva producen un primer eje igual o mayor en una proporción {{nuloConDerivaPCUno}} de las simulaciones. El eje 1, por tanto, no prueba una estructura cíclica común: refleja que casi todas las series crecen.
- **Eje 2, política monetaria.** Lo definen la tasa de referencia ({{cargaTasaRefPCDos}}), la tasa interbancaria y la TIPMN ({{cargaTipmnPCDos}}). Es el único eje que supera con claridad los nulos (proporción de {{nuloConDerivaPCDos}}).
- **Eje 3, riesgo de mercado.** Opone el EMBIG ({{cargaEmbigPCTres}}) a la bolsa ({{cargaBvlPCTres}}). Sus picos coinciden con la crisis financiera global, el final del colapso de las materias primas y el inicio de la pandemia (Figura 5), pero no supera el nulo con deriva (proporción de {{nuloConDerivaPCTres}}).

Bajo bootstrap por bloques de 24 meses, el percentil 5 de la congruencia con el eje original es {{congruenciaBootPCUnoNiveles}}, {{congruenciaBootPCDosNiveles}} y {{congruenciaBootPCTresNiveles}} para los ejes 1 a 3, frente a {{congruenciaBootPCCuatroNiveles}} para el cuarto.

::: {custom-style="Rotulo"}
**Figura 5**\
*Coordenadas de los meses en los tres primeros ejes del PCA*
:::

![](fig/avance_scores_pca.png){width=100%}

::: {custom-style="Nota"}
*Nota.* En gris, los episodios de referencia. Elaboración propia con datos del BCRP.
:::

### 3.1.4 Clasificación factorial jerárquica

La HFC agrupa las series en tres clases que coinciden con los tres ejes del PCA: tendencia o «salud económica», tasas y riesgo de mercado (Tabla 5). En {{hfcReplicas}} réplicas por bloques, la partición en tres clases se reproduce exactamente en una proporción {{hfcPropAriTres}} de las réplicas, y la de cuatro, en {{hfcPropAriCuatro}}. La mediana de la correlación cofenética es {{hfcCofeneticaMediana}}.

::: {custom-style="Rotulo"}
**Tabla 5**\
*Clases de la HFC en las particiones de tres y cuatro clases*
:::

[[TABLA_HFC]]

::: {custom-style="Nota"}
*Nota.* En negrita, la serie más correlacionada con el factor de su clase. Elaboración propia con datos del BCRP.
:::

### 3.1.5 Análisis evolutivo de componentes principales

Las cargas y la inercia de los ejes cambian entre ventanas (Figuras 6 y 7). La estabilidad del eje 2 entre ventanas sucesivas tiene caídas puntuales que dependen del ancho de la ventana (Figura 8); con 60 meses, las caídas marcan transiciones candidatas en {{epcaTransicionesSesenta}}.

::: {custom-style="Rotulo"}
**Figura 6**\
*Cargas evolutivas del eje 2 de las seis series con mayor carga (ventana de 60 meses)*
:::

![](fig/06_epca_cargas_evolutivas_niveles.png){width=90%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura 7**\
*Inercia evolutiva de los ejes 2 y 3 (ventana de 60 meses)*
:::

![](fig/06_epca_varianza_evolutiva_niveles.png){width=90%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura 8**\
*Estabilidad del eje 2 entre ventanas sucesivas, por ancho de ventana*
:::

![](fig/avance_estabilidad_epca.png){width=95%}

::: {custom-style="Nota"}
*Nota.* La línea naranja es el umbral; los puntos, las ventanas por debajo de él. Elaboración propia con datos del BCRP.
:::

El nulo de estructura constante simula series con la misma dependencia temporal y una correlación fija, y cuenta cuántos pares de ventanas resultan tan distintos como los observados. En ninguna de las {{oeFilasPrincipales}} configuraciones principales (anchos de 24 a 60 meses, pesos uniformes y gaussianos) el resultado se distingue del nulo: el menor *p* es {{oePMin}}. Con los datos en niveles, las caídas de estabilidad del EPCA son compatibles con el ruido muestral de ventanas cortas.

### 3.1.6 Datación de regímenes

La partición de Fisher sobre los *scores* suavizados da {{datacionKPrincipal}} regímenes, con cortes en {{datacionCortesTexto}} (Tabla 6 y Figura 9). Si se permite un número mayor de regímenes, la regla de selección elige {{datacionKQuince}}: el número depende de la cota.

::: {custom-style="Rotulo"}
**Tabla 6**\
*Regímenes obtenidos con los scores del PCA*
:::

[[TABLA_REGIMENES]]

::: {custom-style="Nota"}
*Nota.* El primer régimen empieza en diciembre de 2007 porque la media móvil consume los primeros 11 meses. *Crédito medio:* promedio del crédito estandarizado en el régimen. *Frec. del corte:* proporción de réplicas bootstrap que reproducen el corte inicial con ±3 meses. La etiqueta de fase es preliminar y no válida (véase el texto). Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura 9**\
*Scores suavizados, cortes de la datación y episodios de referencia*
:::

![](fig/avance_datacion_pca.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Media móvil de 12 meses; en negro, los cortes; en gris, los episodios. Elaboración propia con datos del BCRP.
:::

Cuatro de los cinco cortes se reproducen en más de cuatro de cada cinco réplicas; el de {{datacionCorteFrecMinTexto}}, solo en una proporción {{datacionFrecMin}}. Con la tolerancia de tres meses, el corte de diciembre de 2008 cae dentro de la crisis financiera global, el de abril de 2014 queda a dos meses del inicio del colapso de las materias primas y el de junio de 2020, a dos meses del fin del episodio de la pandemia. Los cortes de marzo de 2010 y noviembre de 2022 no tienen un episodio compatible.

La regla preliminar de fases asigna la etiqueta según el promedio del crédito estandarizado en cada régimen. En niveles, ese promedio refleja la posición en la tendencia: los primeros regímenes quedan por debajo de la media y los últimos por encima. Por eso el período 2010–2014, de fuerte crecimiento del crédito, recibe la etiqueta de «contracción». **Las etiquetas de fase no son válidas todavía.**

### 3.1.7 Aprendizaje profundo: corrida exploratoria

Los autoencoders y el LSTM-autoencoder se corrieron con una versión anterior del conjunto de datos, que incluía la liquidez M2 (17 series); con las {{nSeries}} series vigentes quedan por repetir. Sus resultados se muestran como exploración, no como resultado de la tesis:

- Fuera de muestra, el autoencoder no lineal reconstruye peor que el PCA en todas las dimensiones probadas, con o sin preentrenamiento (Figura 10).
- La trayectoria latente del LSTM-autoencoder reproduce la forma general de los ejes 1 y 2 del PCA, con menos variación, y aplana los picos del eje 3 (Figura 11).
- El error de reconstrucción mensual sube en la crisis financiera global y en la pandemia, y aumenta al final de la muestra (Figura 12).
- Sobre la trayectoria del LSTM-autoencoder, la regla preliminar de fases reproduce el problema descrito en 3.1.6: la variable que define la fase es casi una recta (Figura 13).

::: {custom-style="Rotulo"}
**Figura 10**\
*Error de reconstrucción fuera de muestra del PCA y de dos autoencoders, por dimensión latente*
:::

![](fig/17series_08_cv_pca_vs_ae.png){width=60%}

::: {custom-style="Nota"}
*Nota.* Validación por bloques. Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura 11**\
*Trayectoria latente del LSTM-autoencoder frente a los scores del PCA*
:::

![](fig/17series_09_trayectoria_latente.png){width=75%}

::: {custom-style="Nota"}
*Nota.* Ventana de 12 meses, rotada hacia el PCA. Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura 12**\
*Error de reconstrucción mensual del PCA y del autoencoder no lineal*
:::

![](fig/17series_08_error_reconstruccion.png){width=75%}

::: {custom-style="Nota"}
*Nota.* La banda corresponde al Monte Carlo Dropout. Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura 13**\
*Regímenes de Fisher y clasificación preliminar de fases sobre la trayectoria del LSTM-autoencoder*
:::

![](fig/17series_09_regimenes.png){width=75%}

::: {custom-style="Nota"}
*Nota.* Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

## 3.2 Discusión e interpretación de los resultados

**Síntesis de los resultados.** El PCA y la HFC coinciden en tres bloques de series —tendencia común, tasas de política y riesgo de mercado— que se reproducen bajo remuestreo. En niveles, la tendencia domina: el primer eje no supera un nulo de series con deriva, y el EPCA no supera el nulo de estructura constante. La datación con los *scores* del PCA encuentra cortes mayormente estables, tres de ellos compatibles con episodios externos. En la corrida exploratoria, el aprendizaje profundo no mejora al PCA.

**Explicaciones y comparación con otras investigaciones.** Los tres bloques se parecen a los grupos que @camiz_cerda_atoche_2026 reportan para series del BCRP entre 1999 y 2020 y a las tres componentes de @atoche_murrieta_2022, aunque el conjunto de series no es idéntico; la comparación bloque por bloque está pendiente. La coincidencia sugiere que la organización transversal de los indicadores peruanos es robusta a la elección de series y de período. La dificultad para separar la dinámica del ruido tiene una explicación directa: con unas {{nEfMedianaNiveles}} observaciones efectivas, las ventanas del EPCA contienen poca información independiente, y en niveles la tendencia común absorbe la mayor parte de la correlación, como anticipan @granger_newbold_1974. Que el autoencoder no supere al PCA es coherente con @baldi_hornik_1989, para quienes el PCA es el óptimo lineal de la reconstrucción, y con la advertencia de @tuhin_et_al_2025 sobre la cantidad de datos que estos modelos requieren.

**Hallazgos principales.** (a) La estructura transversal de las series es el resultado más sólido del avance. (b) La evidencia de regímenes no proviene, por ahora, del cambio en la estructura de correlación, sino del movimiento de los *scores*. (c) La regla de fases basada en el nivel del crédito no mide el ciclo, sino la posición en la tendencia.

**Juicio del autor.** La clasificación en fases es el punto metodológico más importante, porque es uno de los aportes que la tesis busca respecto de los trabajos previos. La posición exploratoria pide trabajar con las series sin transformar, pero en niveles lo primero que muestran los datos es su tendencia. Separar tendencia y ciclo exige una decisión explícita, tomada antes de calcular y discutida con el asesor.

**Limitaciones.** La muestra es corta para el ciclo financiero tal como lo definen @drehmann_borio_tsatsaronis_2012; la autocorrelación reduce el tamaño efectivo de la muestra; los modelos de aprendizaje profundo se corrieron con una versión anterior de los datos; el análisis de robustez con series transformadas está pendiente, y varias fuentes de métodos aún no se han leído (Anexo 3).

**Implicaciones e investigaciones futuras.** Si se confirma que en niveles la estructura de correlación no cambia más allá del azar, los regímenes del ciclo financiero peruano deberán buscarse en la posición del sistema dentro de una estructura estable, no en cambios de esa estructura. Quedan para trabajo futuro la extensión de la muestra a años anteriores a 2007, si la homogeneidad de las series lo permite, y la evaluación de la capacidad del LSTM para anticipar transiciones.

## 3.3 Contrastación de las hipótesis

La Tabla 7 resume el estado de cada hipótesis con la evidencia disponible. El dictamen es preliminar.

::: {custom-style="Rotulo"}
**Tabla 7**\
*Estado preliminar de las hipótesis de trabajo*
:::

| Hipótesis | Evidencia disponible | Estado preliminar |
|---|---|---|
| HE1. No estacionariedad estructural | El EPCA no se distingue del nulo de estructura constante en ninguna de las {{oeFilasPrincipales}} configuraciones (menor *p* = {{oePMin}}) | No respaldada en niveles; falta el análisis con series transformadas |
| HE2. Organización en grupos | Tres bloques coincidentes en PCA y HFC; partición en tres clases reproducida en una proporción {{hfcPropAriTres}} de las réplicas | Respaldada parcialmente; falta la comparación bloque por bloque con Camiz et al. (2026) |
| HE3. Correspondencia con episodios | Tres de cinco cortes compatibles con episodios (±3 meses); dos sin episodio; el número de regímenes depende de la cota | Respaldada parcialmente |
| HE4. Complementariedad | El autoencoder no mejora la reconstrucción fuera de muestra del PCA (corrida exploratoria con 17 series) | No respaldada por ahora; falta repetir con {{nSeries}} series |
| Hipótesis general | Combinación de HE1 a HE4 | Abierta |

::: {custom-style="Nota"}
*Nota.* Elaboración propia.
:::

# CAPÍTULO IV. CONCLUSIONES Y RECOMENDACIONES

## 4.1 Conclusiones

1. **Las series del BCRP se organizan en tres bloques estables.** PCA y HFC coinciden en tres bloques —tendencia común, tasas de política y riesgo de mercado— que se reproducen bajo remuestreo por bloques y se parecen a los reportados por los antecedentes peruanos. Es el resultado más sólido del avance.
2. **En niveles, la tendencia domina y la estructura no cambia más allá del azar.** El primer eje del PCA ({{inerciaPCUnoNiveles}} %) es la tendencia común y no supera el nulo de series con deriva; solo el eje de tasas lo supera con claridad. Las variaciones que muestra el EPCA no se distinguen de las de una estructura constante, y la regla preliminar de fases confunde ciclo con tendencia.
3. **La datación con los scores del PCA es estable y en parte externa, pero el aprendizaje profundo aún no aporta.** Se obtuvieron {{datacionKPrincipal}} regímenes, con cuatro de cinco cortes estables bajo remuestreo y tres compatibles con la crisis financiera global, el colapso de las materias primas y la pandemia. En la corrida exploratoria, el autoencoder no mejoró la reconstrucción del PCA.

## 4.2 Recomendaciones

1. **(De la conclusión 1)** Comparar bloque por bloque los grupos obtenidos con los de @camiz_cerda_atoche_2026 y repetir el PCA y la HFC con las series transformadas, para confirmar que los bloques no dependen de la tendencia.
2. **(De la conclusión 2)** Definir, antes de calcular y en acuerdo con el asesor, una regla de fases basada en la desviación respecto de la tendencia o en la tasa de crecimiento del crédito, y medir con datos simulados, con un quiebre de tamaño conocido, si el nulo de estructura constante puede detectar los cambios que interesan.
3. **(De la conclusión 3)** Repetir los autoencoders y el LSTM-autoencoder con las {{nSeries}} series vigentes, fechar también con el EPCA y con la trayectoria del LSTM, y completar la comparación de métodos en el contexto simulado previsto en la ficha de inscripción.

# REFERENCIAS

::: {#refs}
:::

# ANEXOS

## Anexo 1: Matriz de consistencia

[[MATRIZ]]

## Anexo 2: Estado del avance frente al plan de la ficha de inscripción

::: {custom-style="Rotulo"}
**Tabla 9**\
*Estado del avance por etapa del plan de trabajo*
:::

| Etapa del plan | Estado al 7 de noviembre de 2026 |
|---|---|
| 1. Revisión bibliográfica | En curso: fuentes leídas citadas en el texto; fuentes pendientes en el Anexo 3 |
| 2. Plan de tesis | Ficha de inscripción aprobada; protocolo desarrollado en el Capítulo I |
| 3. Recolección y preprocesamiento | Terminada: {{nSeries}} series, {{nMesesNiveles}} meses, datos congelados |
| 4. Análisis exploratorio multivariado | PCA, HFC y EPCA terminados en niveles; falta el análisis de robustez con series transformadas |
| 5. Aprendizaje automático | Corrida exploratoria con 17 series; falta repetirla con {{nSeries}} |
| 6. Evaluación y validación | Datación con el PCA terminada; faltan la datación con EPCA y LSTM, la regla de fases y el contexto simulado |
| 7. Redacción y difusión | Informe preliminar en curso; artículo pendiente |

::: {custom-style="Nota"}
*Nota.* Elaboración propia.
:::

## Anexo 3: Estado de la revisión bibliográfica

Solo se citan en este informe las fuentes cuyo texto se leyó total o parcialmente; en el caso de @horn_1965, su resumen oficial. Se usan, además, métodos cuyas fuentes originales están localizadas pero todavía no se han leído, por lo que se nombran sin citarse: la partición óptima de Fisher (1958), el índice de Caliński y Harabasz (1974), el criterio de Kaiser (1960), la medida KMO (Kaiser, 1970; Kaiser y Rice, 1974), la prueba de esfericidad de Bartlett (1950, 1951), el coeficiente RV (Robert y Escoufier, 1976), el bootstrap por bloques móviles (Künsch, 1989), el tamaño efectivo de muestra (Kish, 1965; Pyper y Peterman, 1998) y la obra de Benzécri (1973) sobre el análisis de datos. Su lectura forma parte del trabajo pendiente, y se incorporarán a las referencias cuando se haya verificado su contenido.
