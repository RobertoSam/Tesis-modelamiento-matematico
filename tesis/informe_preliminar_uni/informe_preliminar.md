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

::: {custom-style="Titulo preliminar"}
AGRADECIMIENTOS
:::

::: {custom-style="Marcador"}
[Texto por redactar por el tesista.]
:::

::: {custom-style="Titulo preliminar"}
COPIA DE DOCUMENTOS
:::

::: {custom-style="Marcador"}
[Según la Guía N.° 2, en esta sección se incorporan, después de la sustentación, el acta de sustentación, el certificado de idioma extranjero, el grado de bachiller, el certificado de notas o de finalización de estudios y los recibos de pago correspondientes.]
:::

::: {custom-style="Titulo preliminar"}
ÍNDICE DE CONTENIDOS
:::

[[TOC]]

::: {custom-style="Titulo preliminar"}
LISTA DE TABLAS
:::

[[LISTA_TABLAS]]

::: {custom-style="Titulo preliminar"}
LISTA DE FIGURAS
:::

[[LISTA_FIGURAS]]

# RESUMEN

En esta investigación se estudió el ciclo financiero peruano con técnicas exploratorias multivariadas y de aprendizaje automático. Se analizaron {{nSeries}} series mensuales del Banco Central de Reserva del Perú (BCRP), sin transformar, entre {{fechaInicioNiveles}} y {{fechaFinDatos}} ({{nMesesNiveles}} meses): crédito, liquidez, tasas de interés, precios, actividad, reservas, mercado bursátil y riesgo país. La estrategia de análisis encadenó el análisis de componentes principales (PCA), la clasificación factorial jerárquica (HFC), sus versiones evolutivas en ventanas móviles (EPCA y HFC evolutiva, con los programas del asesor) y la partición óptima de Fisher; los autoencoders y las redes LSTM se emplearon como complemento. Cada resultado se contrastó con nulos simulados y con remuestreo por bloques, y los cortes de régimen se compararon con episodios fechados por fuentes independientes de los datos. El PCA y la HFC identificaron tres bloques estables de series: escala del sistema, condiciones monetarias y riesgo de mercado; el dendrograma de la HFC, cortado en 0,7, separó esos mismos tres grupos. El primer eje del PCA ({{inerciaPCUnoNiveles}} % de la inercia) correspondió al crecimiento común de las series y no superó un nulo de series independientes con sus propias tendencias; el eje de las tasas sí lo superó, y sin tendencia apareció un vínculo cíclico entre tasas y saldos. El EPCA con ventana gaussiana de 48 meses fechó un solo corte del primer valor propio, en {{czAedeCorteCodo}}, que se repitió con ventanas de 36 a 60 meses y coincidió con la pandemia de COVID-19, aunque la variación de la estructura entre ventanas no se distinguió de la de una estructura constante (menor *p* = {{oePMin}}). La HFC evolutiva mostró la fragmentación de los bloques en las ventanas que incluyen la pandemia. La datación con los *scores* suavizados del PCA encontró {{datacionKPrincipal}} regímenes con un perfil económico coherente; tres de sus cinco cortes fueron compatibles con episodios externos, y solo el de 2020 coincidió con el del EPCA. En una corrida exploratoria, el autoencoder no mejoró la reconstrucción fuera de muestra del PCA. Se concluyó que la estructura transversal de las series es el resultado más sólido del avance y que la clasificación en fases requiere una regla que no confunda ciclo con tendencia.

**Palabras clave:** ciclo financiero; análisis de componentes principales; clasificación factorial jerárquica; análisis evolutivo; datación de regímenes.

# ABSTRACT

This research studied the Peruvian financial cycle using multivariate exploratory techniques and machine learning. {{nSeriesEn}} untransformed monthly series from the Central Reserve Bank of Peru (BCRP) were analysed from January 2007 to December 2025 ({{nMesesNiveles}} months): credit, liquidity, interest rates, prices, activity, reserves, the stock market and country risk. The analysis strategy chained principal component analysis (PCA), hierarchical factor classification (HFC), their evolutionary versions on moving windows (EPCA and evolutionary HFC, with the advisor's programs) and Fisher's optimal partition; autoencoders and LSTM networks were used as a complement. Each result was tested against simulated null models and block resampling, and regime breaks were compared with episodes dated by sources independent of the data. PCA and HFC identified three stable blocks of series: system scale, monetary conditions and market risk; the HFC dendrogram, cut at 0.7, separated the same three groups. The first PCA axis ({{inerciaPCUnoNivelesEn}} % of inertia) corresponded to the common growth of the series and did not exceed a null of independent series with their own trends; the interest-rate axis did, and after detrending a cyclical link between rates and balances appeared. EPCA with a 48-month Gaussian window dated a single break in the first eigenvalue, in {{czAedeCorteCodoEn}}, which recurred with 36- to 60-month windows and coincided with the COVID-19 pandemic, although the variation of the structure across windows could not be distinguished from that of a constant structure (smallest *p* = {{oePMinEn}}). Evolutionary HFC showed the blocks fragmenting in the windows that include the pandemic. Dating on the smoothed PCA scores found {{datacionKPrincipal}} regimes with a coherent economic profile; three of its five breaks were compatible with external episodes, and only the 2020 break coincided with the EPCA break. In an exploratory run, the autoencoder did not improve on the out-of-sample reconstruction of PCA. It was concluded that the cross-sectional structure of the series is the most solid result so far, and that classifying regimes into phases requires a rule that does not confuse cycle with trend.

**Keywords:** financial cycle; principal component analysis; hierarchical factor classification; evolutionary analysis; regime dating.

# INTRODUCCIÓN

El ciclo financiero describe las fases de expansión y contracción del crédito y de los precios de los activos. A diferencia del ciclo económico, no existe una variable que lo observe directamente: la información está repartida entre muchas series —crédito, liquidez, tasas de interés, precios, mercado bursátil, riesgo país— que se mueven juntas solo en parte y cuya relación puede cambiar en el tiempo. Medirlo exige, por tanto, métodos que resuman muchas series a la vez y que permitan ver si esa síntesis se mantiene o cambia.

Para el Perú, los trabajos más cercanos aplicaron análisis exploratorios multivariados a series del BCRP [@atoche_murrieta_2022; @camiz_cerda_atoche_2026]. Esos trabajos describen la estructura de las series y su evolución, pero no clasifican los períodos en fases del ciclo, no incorporan modelos de aprendizaje profundo y no cubren el período posterior a la pandemia. Esta tesis aborda esos tres puntos: propone una metodología que combina el PCA, la HFC y sus versiones evolutivas con autoencoders y redes LSTM, la aplica a {{nSeries}} series mensuales del BCRP entre 2007 y 2025, y contrasta los regímenes que encuentra con episodios cuya fecha proviene de documentos independientes de los datos.

La investigación es cuantitativa y de nivel exploratorio y descriptivo. Su rasgo metodológico central es que cada resultado se compara con un nulo simulado que reproduce las propiedades que podrían generarlo por azar, en particular la tendencia común de las series, y se somete a remuestreo por bloques de meses para medir su estabilidad. Los métodos exploratorios se aplicaron con los programas del asesor: el paquete AedeClahfac, trasladado a Python con verificación de que reproduce sus resultados, y el procedimiento de su programa claede, replicado en Python con una verificación todavía pendiente.

Este documento es un **informe preliminar**. Los datos, el análisis exploratorio y la datación de regímenes con el PCA están terminados; la interpretación de los resultados todavía no se ha discutido con el asesor; los modelos de aprendizaje profundo se presentan como una corrida exploratoria, y la clasificación de los regímenes en fases sigue abierta. El Capítulo I presenta el protocolo de la investigación y la estrategia de análisis; el Capítulo II, el marco teórico con el desarrollo estadístico de cada método; el Capítulo III, los resultados obtenidos hasta la fecha, su discusión y el estado de las hipótesis, y el Capítulo IV, las conclusiones y recomendaciones preliminares.

# CAPÍTULO I. PROTOCOLO DE LA INVESTIGACIÓN

## 1.1 Identificación y descripción del problema de estudio

El ciclo financiero es un fenómeno latente. @drehmann_borio_tsatsaronis_2012 lo caracterizan, para siete economías desarrolladas, por el comportamiento conjunto del crédito y de los precios inmobiliarios, y encuentran un componente de mediano plazo, de 8 a 30 años, más largo que el ciclo económico tradicional, cuyos picos coinciden con crisis bancarias. En una economía como la peruana, con series financieras más cortas y una estructura distinta, esa caracterización no puede trasladarse sin más: el problema práctico es identificar qué información común contienen los indicadores disponibles y si esa información cambia de un período a otro.

El BCRP publica decenas de indicadores mensuales relacionados con el crédito, la liquidez, las tasas de interés, los precios, la actividad, el sector externo y los mercados financieros. Estas series presentan tres dificultades: están muy correlacionadas entre sí, por lo que cualquier síntesis debe separar lo común de lo específico; casi todas crecen en el tiempo, de modo que buena parte de su correlación puede deberse solo a la tendencia [@granger_newbold_1974], y su relación puede variar entre períodos, lo que hace que un análisis global oculte cambios importantes [@camiz_diblasi_2013].

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

- **Justificación teórica.** La investigación contrasta, sobre los mismos datos, dos familias de métodos: la exploratoria, que describe la estructura sin postular un modelo generador [@camiz_2021_pca; @camiz_et_al_2020], y la de aprendizaje profundo, que puede representar relaciones no lineales y dependencia temporal. Se sabe que un autoencoder lineal con error cuadrático recupera el subespacio de las primeras componentes principales [@baldi_hornik_1989]; la tesis evalúa si las versiones no lineales y temporales aportan información adicional en un contexto de muestra pequeña.
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
- **OE2.** Analizar la estructura de correlación de las series, sus grupos homogéneos y su estabilidad en el tiempo con PCA, HFC y sus versiones evolutivas, con un criterio explícito para elegir el ancho de la ventana.
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

Siguiendo la Guía N.° 2, la variable dependiente es la que describe el problema de estudio y la independiente, la que describe la solución propuesta. En un diseño exploratorio no se postula una relación causal entre ambas: la variable independiente es el procedimiento con que se mide la dependiente. La Tabla {T:variables} resume las variables, sus dimensiones y sus indicadores.

::: {custom-style="Rotulo"}
**Tabla {T:variables}**\
*Variables, dimensiones e indicadores*
:::

| Variable | Dimensión | Indicadores |
|---|---|---|
| **Dependiente:** regímenes del ciclo financiero peruano | Estructura de correlación | Inercia, cargas, cos² y contribuciones por eje; correlación de cada eje con el tiempo |
| | Grupos de series | Clases e índices de nodo de la HFC; reproducción de la partición bajo remuestreo |
| | Estabilidad temporal | Valores propios y correlaciones evolutivas; similitud entre ventanas; *p* frente al nulo de estructura constante |
| | Datación y fase | Cortes de régimen; frecuencia de cada corte bajo remuestreo; distancia a los episodios de referencia; etiqueta de fase |
| **Independiente:** metodología híbrida de reducción dimensional y aprendizaje automático | Métodos exploratorios | PCA, HFC, EPCA, HFC evolutiva, partición óptima de Fisher |
| | Aprendizaje profundo | Autoencoder y LSTM-autoencoder: error de reconstrucción fuera de muestra; estabilidad frente a la semilla |

::: {custom-style="Nota"}
*Nota.* Los datos observados son {{nSeries}} series mensuales del BCRP (Tabla {T:series}). Elaboración propia.
:::

## 1.4 Metodología

### 1.4.1 Tipo de investigación

- **Por su enfoque:** cuantitativa.
- **Por su nivel:** exploratoria y descriptiva, con un componente comparativo entre métodos.
- **Por su diseño:** no experimental, longitudinal y retrospectivo: se observan series de tiempo ya publicadas, sin manipular variables.
- **Métodos:** analítico e inductivo. La contrastación con nulos simulados y con episodios externos aporta un componente hipotético-deductivo a las hipótesis de trabajo.

### 1.4.2 Población y muestra

La **población** está formada por los indicadores macrofinancieros mensuales que publica el BCRP. La **muestra** es no probabilística, por criterio: {{nSeries}} series que cubren los ámbitos de la ficha de inscripción (crédito, liquidez, tasas de interés, inflación, mercado bursátil y tipo de cambio), más la actividad, las reservas internacionales y el riesgo país, con información continua de {{fechaInicioNiveles}} a {{fechaFinDatos}} ({{nMesesNiveles}} meses) (Tabla {T:series}). Quedaron fuera tres series disponibles: el crédito total, por su colinealidad con los créditos por tipo; el IPC subyacente, que se conserva solo como serie de contraste, y la liquidez M2, casi colineal con M3 en niveles, que pesaría dos veces en el PCA.

::: {custom-style="Rotulo"}
**Tabla {T:series}**\
*Series analizadas y su código en la base de datos del BCRP*
:::

[[TABLA_SERIES]]

::: {custom-style="Nota"}
*Nota.* TAMN: tasa activa en moneda nacional; TIPMN: tasa pasiva en moneda nacional; BVL: Bolsa de Valores de Lima; EMBIG: diferencial de rendimiento de los bonos soberanos peruanos. Elaboración propia con datos del BCRP.
:::

### 1.4.3 Técnicas e instrumentos de recolección de datos

La técnica es el análisis documental de fuentes estadísticas oficiales. Las series se descargaron de la base de datos estadística del BCRP mediante su código, se verificaron serie por serie (unidades, frecuencia, cobertura y valores faltantes) y se consolidaron en una base de datos multivariada. La base se congeló antes de cualquier cálculo, con una huella digital de cada archivo, para que ningún resultado dependa de revisiones posteriores de la fuente. El instrumento es la propia base de datos, documentada en un diccionario de datos.

### 1.4.4 Estrategia de análisis

La estrategia de análisis es la cadena metodológica planteada en el informe del Seminario de Tesis I (Figura {F:estrategia}): el marco exploratorio clásico —PCA, HFC y EPCA—, ya aplicado a datos del BCRP por los antecedentes, se extiende con autoencoders temporales y redes LSTM, y ambos desembocan en la detección y datación de regímenes. El orden responde al principio de ir de lo más evidente a lo más oculto en los datos [@camiz_2021_pca]: primero las series y su estructura global, luego su organización en grupos, después su variación en el tiempo y, al final, las representaciones no lineales.

::: {custom-style="Rotulo"}
**Figura {F:estrategia}**\
*Estrategia de análisis: cadena metodológica de la tesis*
:::

![](fig/estrategia_mmc101.png){width=95%}

::: {custom-style="Nota"}
*Nota.* Tomado del informe final del curso MMC101, Seminario de Tesis I [@samaniego_2026].
:::

La Tabla {T:estrategia} detalla cada etapa: la pregunta que responde, el método, el programa con que se ejecuta y el contraste que valida su resultado.

::: {custom-style="Rotulo"}
**Tabla {T:estrategia}**\
*Etapas de la estrategia de análisis*
:::

| Etapa | Pregunta | Método | Programa | Validación |
|---|---|---|---|---|
| 1. Series base | ¿Cómo se comporta cada serie? | Gráficos, tendencia, autocorrelación | Python | Diagnóstico de raíz unitaria |
| 2. Estructura global | ¿Qué información común contienen las series? | PCA: valores propios, cargas, cos², contribuciones | Python; réplica en R | Kaiser, vara quebrada, análisis paralelo; nulos de tendencia; bootstrap por bloques |
| 3. Grupos de series | ¿En qué bloques homogéneos se organizan? | HFC: jerarquía, índices de nodo, dendrograma | AedeClahfac (clahfac) | Corte en 0,7; bootstrap por bloques |
| 4. Estructura en el tiempo | ¿Cambia la estructura de correlación? | EPCA y HFC evolutiva en ventanas móviles | AedeClahfac (aede) y réplica del procedimiento claede | Nulo de estructura constante; anchos de 24 a 60 meses |
| 5. Datación (fechado de los cambios de régimen) | ¿En qué meses cambia el sistema de régimen? | Partición óptima de Fisher; regla de la mayor caída (índice de Caliński y Harabasz informado) | aede y Python | Frecuencia bajo remuestreo; episodios externos (±3 meses) |
| 6. Representación no lineal | ¿Qué agrega el aprendizaje profundo? | Autoencoder y LSTM-autoencoder | Python | Validación por bloques y *walk-forward* frente al PCA |
| 7. Comparación | ¿Qué método describe mejor los regímenes? | Comparación de interpretabilidad, estabilidad y capacidad descriptiva | Python | Contexto simulado con regímenes conocidos |

::: {custom-style="Nota"}
*Nota.* AedeClahfac y claede son los programas en R del asesor [@camiz_aedeclahfac; @camiz_claede_2025]. Elaboración propia.
:::

### 1.4.5 Técnicas de análisis y procesamiento de datos

El análisis principal usa las series sin transformar, estandarizadas; las series transformadas (logaritmos y diferencias) se reservan para un análisis de robustez. Los métodos de la Tabla {T:estrategia} se desarrollan formalmente en la sección 2.2. El procesamiento se realizó en Python. Las rutinas del asesor se trasladaron a Python línea a línea y se verificó que reproducen los resultados del paquete en R; el análisis completo tiene además una réplica en R. Datos, código y resultados están en un repositorio público (https://github.com/RobertoSam/Tesis-modelamiento-matematico).

# CAPÍTULO II. MARCO TEÓRICO

## 2.1 Antecedentes de la investigación

Siguiendo la Guía N.° 2, los antecedentes son trabajos de los últimos cinco años (2021–2026), presentados en orden cronológico. Los trabajos fundacionales de cada método —el PCA evolutivo [@camiz_maulucci_roig_2010; @camiz_diblasi_2013], la HFC [@camiz_et_al_2020] y la datación con la partición de Fisher [@camiz_roig_2011]— y la caracterización del ciclo financiero de @drehmann_borio_tsatsaronis_2012 se presentan en las bases teóricas, junto con el método o el concepto que fundamentan.

**Atoche Murrieta (2022).** @atoche_murrieta_2022 estima el ciclo financiero peruano con 17 series mensuales del BCRP —activos internos netos de la banca, circulante, ahorro, encaje, crédito, índice bursátil, fondos de las AFP, tipo de cambio, liquidez, dolarización, reservas, apalancamiento global, tasas activas y pasivas en soles y en dólares, y EMBIG—, mediante PCA, HFC y PCA evolutivo con pesos gaussianos. Según su resumen, identifica tres componentes: una de largo plazo, asociada a la evolución del sistema financiero; otra de mediano plazo, ligada a las tasas activas y pasivas, y una tercera asociada a la volatilidad del mercado financiero.

**Purizaca Rosillo (2023).** @purizaca_2023 aplica el PCA, el EPCA y el PCA dinámico generalizado a 21 precios mensuales de materias primas entre 1990 y 2021. El primer componente recoge el 70,6 % de la inercia y representa la tendencia común de los precios. En el EPCA usa una ventana de 72 meses con pesos gaussianos y parte la serie del primer valor propio con el algoritmo de Fisher; como el índice de Caliński y Harabasz no alcanza un máximo, fija siete tramos en el punto en que sus incrementos se vuelven marginales. Es un antecedente directo del procedimiento de datación y muestra que el número de tramos puede no quedar determinado por el índice.

**Torres Armas y Baltazar Chávez (2023).** @torres_baltazar_2023 analizan el ciclo económico peruano entre 2004 y 2022 con la tradición de los filtros: desestacionalizan las series trimestrales del BCRP, extraen su componente cíclico con el filtro de Baxter-King y calculan su correlación con el ciclo del PBI, adelantada y rezagada, en 2004–2015 y 2016–2022. En el segundo período, el consumo, la inversión, la inflación y la tasa activa en soles resultan procíclicos, y el tipo de cambio y los términos de intercambio, contracíclicos. Representa el enfoque alternativo al de esta tesis: fija de antemano qué es ciclo (una banda de frecuencias) y qué variable lo define (el PBI).

**Camiz y Spada (2024).** @camiz_spada_2024 proponen estudiar si los factores y las clasificaciones de un conjunto de series se mantienen estables en el tiempo. Aplican el EPCA y la **HFC evolutiva** a cinco cronologías de *Pinus pinea* (1925–2003) con una ventana móvil de 10 años y pesos gaussianos, y resumen los resultados con la evolución de los valores propios, de las correlaciones y de los índices de los nodos, y con la sucesión de dendrogramas. Parten el período con el algoritmo de Fisher sobre el primer valor propio y obtienen siete intervalos con estructuras de correlación y de grupos diferentes. Es el antecedente publicado de la HFC evolutiva que usa esta tesis.

**Tuhin, Nobi, Rakib y Lee (2025).** @tuhin_et_al_2025 entrenan un LSTM-autoencoder sobre los retornos diarios de 375 acciones del índice S&P 500 entre 2000 y 2022, construyen con los pesos de la capa central redes anuales de influencia entre acciones y muestran que sus propiedades topológicas cambian de forma distintiva en cinco crisis financieras. Advierten que el enfoque requiere muchos datos. Es el antecedente del uso de autoencoders temporales para detectar crisis.

**Camiz, Cerda Hernández y Atoche Murrieta (2026).** En un manuscrito aún no publicado, @camiz_cerda_atoche_2026 aplican PCA, HFC y EPCA a 17 series mensuales del BCRP entre 1999 y 2020. Excluyen el tipo de cambio interbancario y el apalancamiento bancario, poco correlacionados con el resto, y la HFC identifica tres grupos: salud económica y financiera, tasas de interés y riesgo del mercado financiero. Sobre el primer valor propio del EPCA, con ventana gaussiana de 48 meses, fechan transiciones con la partición de Fisher y eligen el número de cortes con el índice de Caliński y Harabasz. Es el antecedente más directo de la tesis.

**Vacío identificado.** Los antecedentes peruanos aplican el análisis exploratorio hasta 2020, sin aprendizaje profundo y sin clasificar los regímenes en fases. Ninguno contrasta sus resultados con nulos que reproduzcan la tendencia y la autocorrelación de las series, y el número de tramos de la datación queda en todos ellos sujeto a una elección del analista [@purizaca_2023; @camiz_cerda_atoche_2026].

## 2.2 Bases teóricas

### 2.2.1 El ciclo financiero

**Concepto.** El ciclo financiero es el movimiento conjunto, de expansión y de contracción, del crédito y de los precios de los activos. En la fase de expansión, el crédito crece más rápido que la actividad, los precios de los activos suben y las condiciones de financiamiento se relajan; en la de contracción ocurre lo contrario, y el ajuste puede ser abrupto. @drehmann_borio_tsatsaronis_2012 dan una definición operativa a partir de siete economías desarrolladas, con datos trimestrales desde 1960, y llegan a tres conclusiones que fijan el concepto. Primero, el crédito, la razón entre crédito y producto y los precios de los inmuebles comparten un componente común de **mediano plazo**, de 8 a 30 años, más largo que el ciclo económico tradicional, de 1 a 8 años. Segundo, los precios bursátiles no forman parte de ese componente: son más volátiles y menos sincronizados con el crédito. Tercero, los picos del ciclo financiero coinciden con las crisis bancarias de origen doméstico de la muestra, y las recesiones que ocurren en su fase de contracción son, en promedio, más profundas.

**Por qué importa medirlo.** Si los desequilibrios financieros se acumulan durante varios años antes de manifestarse en una crisis, mirar solo el ciclo económico de corto plazo puede ocultarlos. De ahí el interés por medir el ciclo financiero por separado del ciclo económico [@drehmann_borio_tsatsaronis_2012].

**Dos tradiciones de medición.** La primera fija de antemano qué variables componen el ciclo y qué duración tiene, y lo extrae con filtros de frecuencia o fechando los picos y valles de cada serie. Es la de @drehmann_borio_tsatsaronis_2012 y, para el ciclo económico peruano, la de @torres_baltazar_2023. La segunda, exploratoria, parte de un conjunto amplio de indicadores y deja que su estructura de correlación indique qué series se mueven juntas y cómo cambia esa relación en el tiempo. Es la de @atoche_murrieta_2022 y @camiz_cerda_atoche_2026, y es la de esta tesis. Por eso la tesis incluye la bolsa y el riesgo soberano, que Drehmann et al. excluyen de su definición: si su comportamiento es distinto, la propia estructura de los datos lo mostrará.

**Lo que la muestra permite.** La muestra mensual disponible abarca 19 años, de modo que no contiene ni siquiera un ciclo completo de la duración que describen Drehmann et al. Además, el índice de precios de inmuebles del BCRP es trimestral, por lo que las aproximaciones mensuales al ciclo son el crédito, la liquidez, las tasas de interés y el riesgo soberano. Por estas razones, el objeto de estudio no es el ciclo completo, sino los **regímenes** que los datos permiten distinguir dentro de la muestra.

### 2.2.2 Régimen, transición, fase y datación

Estos conceptos organizan la tesis y conviene distinguirlos con precisión.

- Un **régimen** es un intervalo de meses consecutivos en el que la relación entre las series es aproximadamente la misma: las mismas series se mueven juntas, con intensidades parecidas. Es una propiedad del conjunto de las series, no del nivel de una de ellas.
- Una **transición** es el paso de un régimen a otro: un cambio en la estructura que se mantiene en los meses siguientes. Puede ser abrupta o gradual, y puede afectar a todas las series o solo a un bloque.
- Una **fase** es la etiqueta económica —expansión, contracción o transición— que se asigna a cada régimen *después* de detectarlo, según el comportamiento del crédito en ese intervalo. La detección usa toda la información multivariada; la etiqueta interpreta el resultado.
- La **datación de regímenes** es la estimación de los meses en que termina un régimen y empieza el siguiente.

**Qué significa datar.** En la literatura del ciclo, «datar» es asignar fechas a los cambios del ciclo. La tradición clásica fecha los **puntos de giro** —picos y valles— de una serie de referencia; es lo que hacen los comités de fechado, como el del NBER cuyas fechas se usan aquí para cerrar algunos episodios [@nber_2010], y lo que @drehmann_borio_tsatsaronis_2012 aplican al crédito y a los precios con el algoritmo de Bry y Boschan adaptado por Harding y Pagan (como se citan en Drehmann et al., 2012). En esta tesis, datar regímenes es otra cosa: se toma una **trayectoria** —una serie ordenada en el tiempo que resume el sistema— y se divide en **tramos** de meses consecutivos lo más homogéneos posible. El resultado es una lista de **cortes**, el primer mes de cada tramo nuevo, y, entre ellos, los regímenes. Es el problema que @fisher_1958 plantea con el nivel de un lago a lo largo de 96 años: definir «épocas» de años consecutivos con la menor variación interna posible (sección 2.2.8).

**Para qué se data.** El PCA, el EPCA y la HFC evolutiva describen el sistema de forma continua, mes a mes. Para responder al objetivo OE4 hay que convertir esa descripción en intervalos con fecha, que puedan compararse con episodios documentados, recibir una etiqueta de fase y compararse entre métodos.

**Qué se data.** Se datan dos trayectorias distintas, y la diferencia importa para interpretar los resultados. La primera es el **primer valor propio del EPCA**, que mide la intensidad del movimiento común: un corte indica que las series pasan a moverse más, o menos, juntas. La segunda son los ***scores* del PCA**, que miden la posición del sistema: un corte indica que el sistema se desplaza a otra zona —por ejemplo, de tasas bajas a tasas altas— aunque la forma de la correlación no cambie. Los cortes de una y otra no son la misma cosa y no deben sumarse como coincidencias sin explicar por qué ambas cambian.

**Datación y fechado de episodios.** La datación se obtiene de los datos. El **fechado de episodios**, en cambio, toma de un documento externo el mes de un evento: la quiebra de Lehman Brothers, un anuncio de la Reserva Federal, la declaración de pandemia. Los episodios nunca se fechan con las series ni con un indicador derivado de ellas; solo así la comparación entre cortes y episodios no es circular. La bibliografía sirve para identificar los eventos candidatos, pero no para fecharlos. Las fechas son las del evento externo, no las de su efecto en el Perú, que puede llegar con retraso (Tabla {T:episodios}). Un corte es compatible con un episodio si dista de él tres meses o menos; seis meses se usan como sensibilidad. Como los episodios son seis, y algunos están muy próximos —el fin de la guerra comercial y el inicio de la pandemia distan dos meses—, la comparación es descriptiva y no un contraste con poder estadístico.

::: {custom-style="Rotulo"}
**Tabla {T:episodios}**\
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
*Nota.* La crisis global va de la quiebra de Lehman Brothers al valle de la recesión estadounidense fijado por el NBER; el *taper tantrum*, del testimonio del presidente de la Reserva Federal ante el Congreso al comunicado que redujo las compras de activos; el colapso de las materias primas, de la caída del precio del petróleo al primer repunte de los precios informado por el FMI; la pandemia, de la declaración de la OMS al valle de la actividad estadounidense fijado por el NBER. Elaboración propia.
:::

### 2.2.3 Análisis exploratorio, tendencia y transformación de las series

**El enfoque exploratorio.** El análisis exploratorio es la primera parte de un estudio cuantitativo, «una suerte de trabajo detectivesco» que no impone un modelo probabilístico y que lleva a formular hipótesis de estructura que luego pueden validarse con métodos confirmatorios; como no hay un diseño muestral, sus resultados valen para la muestra estudiada y no se infieren a una población [@camiz_maulucci_roig_2010]. Los métodos factoriales reorganizan la información por orden de importancia, de lo más evidente a lo más oculto, mediante operaciones algebraicas, según el principio de que los datos deben «hablar por sí mismos» [Benzécri, 1982, como se citó en @camiz_2021_pca]. Como no se estima un modelo, la inferencia clásica se sustituye por dos herramientas: la **estabilidad** de los resultados ante pequeñas perturbaciones de los datos (remuestreo) y la **comparación con nulos**, es decir, con lo que el método mostraría si no existiera la estructura buscada (sección 2.2.9). Los resultados de la tesis describen el Perú de 2007 a 2025 y no se generalizan a otros países ni períodos.

**Tendencia y regresión espuria.** Casi todas las series macrofinancieras crecen en el tiempo: el crédito, la liquidez, los precios y la actividad se multiplican varias veces en dos décadas. @granger_newbold_1974 mostraron, con caminatas aleatorias independientes, que las regresiones entre series con tendencia dan con frecuencia ajustes altos y coeficientes «significativos» que son espurios. La razón es intuitiva: si dos series se alejan de su punto de partida, aunque lo hagan por causas independientes, en muchos meses ambas están por encima de su media y su correlación es alta. En un PCA de series en niveles el efecto es el mismo: el primer eje puede ser solo el paso del tiempo.

**Tendencia determinística o estocástica.** El nulo con que se contrasta esa posibilidad depende de cómo crece cada serie. Una serie es **estacionaria en tendencia** (TS) si fluctúa alrededor de una recta a la que vuelve. Es **integrada** (DS) si sus incrementos son los que fluctúan, de modo que no vuelve a una recta: es una caminata aleatoria, con o sin **deriva** (un crecimiento promedio por mes). La tesis clasifica cada serie con las pruebas ADF y KPSS sobre los residuos de una recta, con una regla fijada antes de calcular, y evalúa si la deriva es significativa con un error estándar robusto a la autocorrelación [@dickey_fuller_1979; @kwiatkowski_et_al_1992; @newey_west_1987].

**Transformar o no transformar.** La solución habitual en econometría es diferenciar las series o tomar sus tasas de crecimiento. Pero diferenciar es un filtro que altera lo que se quiere medir. Para una oscilación de período $P$ meses, la primera diferencia multiplica su amplitud por

$$
\gamma(P)=\lvert 1-e^{-2\pi i/P}\rvert=2\sin(\pi/P),
$$

que es menor que 1 para todo $P>6$ y tiende a cero cuando $P$ crece. Una oscilación de 2 años ($P=24$) conserva el 6,8 % de su varianza; una de 8 años ($P=96$), solo el 0,43 %. La diferencia borra, por tanto, justamente las oscilaciones lentas que caracterizan al ciclo financiero. La tesis resuelve esta tensión así: analiza las series sin transformar, como las publica la fuente, y contrasta cada resultado con nulos que reproducen el efecto de la tendencia; las series transformadas se reservan para un análisis de robustez.

**Autocorrelación y tamaño efectivo.** Los meses consecutivos de una serie económica no son observaciones independientes: lo que pasa en un mes se parece mucho a lo que pasó el anterior. Por eso una muestra de $n$ meses contiene menos información que $n$ observaciones independientes. El **tamaño efectivo** de muestra cuantifica esa pérdida: para la correlación entre dos series con autocorrelaciones $\rho_{xx}(h)$ y $\rho_{yy}(h)$,

$$
\frac{1}{n_{\mathrm{ef}}}=\frac1n+\frac2n\sum_{h=1}^{J}\rho_{xx}(h)\,\rho_{yy}(h),
$$

con $J$ el retardo máximo [@pyper_peterman_1998]. Con series muy autocorrelacionadas, $n_{\mathrm{ef}}$ puede ser una fracción pequeña de $n$, y todas las pruebas que suponen independencia se vuelven demasiado optimistas.

### 2.2.4 Análisis de componentes principales

**Problema que resuelve.** Las 16 series están muy correlacionadas: contienen mucha información repetida. El PCA las resume en pocos factores no correlacionados que recogen la mayor parte de su variabilidad y permite ver qué series se mueven juntas y cuáles no [@camiz_2021_pca].

**Idea.** Cada mes es un punto en un espacio de 16 dimensiones, una por serie; los 228 meses forman una nube. El PCA busca la dirección en la que esa nube se extiende más, luego la dirección perpendicular a la primera en la que se extiende más, y así sucesivamente. Esas direcciones son los **ejes factoriales**. Proyectar la nube sobre los primeros $d$ ejes da la mejor aproximación de rango $d$ de los datos, la que menos deforma las distancias entre los meses [@eckart_young_1936; @camiz_2021_pca].

**Datos e inercia.** Como las series tienen unidades distintas —soles, porcentajes, índices, puntos básicos—, cada una se centra y se reduce: $z_{tj}=(x_{tj}-\bar x_j)/s_j$. La tabla estandarizada es $Z$ y su matriz de correlaciones, $R=\tfrac1n Z^\top Z$; en el análisis exploratorio se usa el divisor $n$ porque no se estima un parámetro poblacional [@camiz_2021_pca]. La información de la tabla se mide por su **inercia**, la suma de las distancias cuadradas de los puntos a su centro de gravedad; con series estandarizadas cada una aporta una unidad y la inercia total es $\operatorname{tr}R=p=16$. La estandarización da a todas las series el mismo peso, lo que tiene una consecuencia práctica: dos series casi idénticas pesan el doble. Por eso se excluyó la liquidez M2, casi colineal con M3.

**Ejes, valores propios y componentes.** Los ejes son los vectores propios de $R$:

$$
R=V\Lambda V^\top,\qquad \lambda_1\ge\lambda_2\ge\dots\ge\lambda_p\ge0,\qquad \sum_{k}\lambda_k=p .
$$

El valor propio $\lambda_k$ es la inercia que recoge el eje $k$, y $\lambda_k/p$ su proporción. Como cada serie vale una unidad, $\lambda_k$ se lee como «cuántas series resume el eje» [@camiz_2021_pca]. Las **componentes principales** o *scores* son las coordenadas de los meses en los ejes, $F=ZV$. En series de tiempo, cada componente es a su vez una serie: la primera es una especie de compromiso entre las originales; la segunda describe las desviaciones más importantes respecto de la primera, y así sucesivamente [@camiz_diblasi_2013]. El signo de un eje es arbitrario: invertirlo no cambia nada, y solo importa el signo relativo de las series.

**Cómo se lee.** Para saber qué significa cada eje se usan tres medidas:

- La **carga** $c_{jk}=\sqrt{\lambda_k}\,v_{jk}$ es la correlación entre la serie $j$ y el eje $k$.
- El **cos²** $=c_{jk}^2$ es la **calidad de representación**: la parte de la variabilidad de la serie que recoge el eje. Se suma sobre varios ejes; una serie con calidad baja tiene un comportamiento propio que esos ejes no describen [@camiz_2021_pca].
- La **contribución** $v_{jk}^2$ es el peso de la serie en la construcción del eje. Si $q$ series contribuyen por igual, cada una aporta alrededor de $1/q$ y el eje resume lo que tienen en común; si una sola aporta casi todo, el eje es exclusivo de ella [@camiz_2021_pca].

La representación gráfica de las cargas es el **círculo de correlaciones**: cada serie es una flecha; el ángulo entre dos flechas refleja su correlación y la longitud, la calidad de su representación en el plano.

**Cuántos ejes interpretar.** En un marco exploratorio no hay una regla de parada única: se trata de saber si los ejes describen estructura o ruido, y de no reducir la tabla de forma artificial [@camiz_2021_pca]. @camiz_pillar_2018 compararon por simulación diez reglas y encontraron que ninguna es satisfactoria en todos los casos. Por eso la tesis triangula tres criterios, cada uno con su propio supuesto:

- *Kaiser–Guttman:* retener los ejes con $\lambda_k>1$, es decir, los que resumen más que una serie. @horn_1965 muestra que, en una muestra finita, los primeros valores propios se inflan por el error muestral, de modo que este criterio tiende a retener ejes de más.
- *Vara quebrada:* si la inercia se repartiera al azar entre los ejes, como los trozos de una vara rota en $p$ pedazos, el eje $k$ recogería en promedio $b_k=\sum_{i=k}^{p}1/i$; se retienen los ejes con $\lambda_k>b_k$. Tiende a retener pocos ejes [@camiz_2021_pca].
- *Análisis paralelo:* se generan tablas de series aleatorias independientes con el mismo número de meses y de series, y se retienen los ejes cuyo valor propio supera al de las tablas aleatorias, lo que descuenta el inflado por error muestral [@horn_1965]. Supone filas independientes, algo que en series de tiempo no se cumple.

El número de ejes de la tesis ($d=3$) se fijó en la primera iteración del análisis, antes de conocer las cifras actuales, y se informan $d=2$ y $d=4$ como sensibilidad.

**Adecuación de los datos.** La prueba de esfericidad de Bartlett contrasta si $R$ difiere de la matriz identidad, la de series sin correlación [@bartlett_1950]:

$$
\chi^2=-\Big(n-1-\frac{2p+5}{6}\Big)\ln\lvert R\rvert,\qquad \text{gl}=\frac{p(p-1)}{2}.
$$

La medida de Kaiser, Meyer y Olkin (KMO) compara las correlaciones con las correlaciones parciales $a_{jl}$, que miden la relación entre dos series descontando las demás:

$$
\mathrm{KMO}=\frac{\sum_{j\neq l}r_{jl}^2}{\sum_{j\neq l}r_{jl}^2+\sum_{j\neq l}a_{jl}^2};
$$

si las series comparten factores comunes, las parciales son pequeñas y el KMO se acerca a 1 [@kaiser_1970; @kaiser_rice_1974]. La prueba de Bartlett es asintótica: supone observaciones independientes y muchas más que series. Con series autocorrelacionadas se recalcula con el tamaño efectivo, pero si $n_{\mathrm{ef}}$ resulta menor que $p$, la aproximación $\chi^2$ deja de ser fiable y el resultado es solo un indicio.

**Limitaciones.** El PCA es lineal y global. Lineal, porque solo capta relaciones que se resumen con correlaciones. Global, porque calcula las correlaciones con todos los meses a la vez: si la relación entre las series cambia, el PCA da un promedio que puede no representar a ningún período [@camiz_diblasi_2013]. Además, los ejes son ortogonales por construcción, lo que a veces mezcla bloques de series y dificulta interpretar los ejes después del primero [@camiz_et_al_2020]. Por último, si dos valores propios son casi iguales, sus ejes no están determinados por separado: cualquier rotación dentro de su plano es igual de válida, y solo puede interpretarse el plano. La HFC atiende el problema de la ortogonalidad, y el EPCA, el de la globalidad.

### 2.2.5 Clasificación factorial jerárquica

**Problema que resuelve.** Los ejes del PCA son compromisos globales y ortogonales. La HFC responde a otra pregunta: qué series se mueven juntas y pueden resumirse con una sola serie representativa. Da **grupos de series, cada uno con su propio factor**, y esos factores pueden estar correlacionados entre sí. En el PCA de dos variables, el primer componente resume lo que ambas tienen en común y el segundo, sus diferencias; esa facilidad de interpretación llevó a @denimal_2007 a proponer la HFC, que combina la clasificación de las variables con métodos factoriales análogos al PCA [@camiz_et_al_2020].

**Cómo funciona.** La HFC es una clasificación jerárquica ascendente de las **series** [@camiz_et_al_2020]:

1. Cada serie se estandariza y forma un grupo por sí misma; su representante es la propia serie.
2. Para cada par de grupos se hace un PCA de sus dos representantes. El primer valor propio mide lo que tienen en común; el segundo, lo que los diferencia.
3. Se fusiona el par con el **menor segundo valor propio**, el más homogéneo.
4. El primer componente de ese PCA pasa a ser el **representante** del nuevo grupo, y su segundo valor propio es el **índice** del nodo.
5. Se repite hasta reunir todas las series. Con $p$ series se obtienen $p-1$ nodos, numerados de $p+1$ a $2p-1$; el último es la raíz.

Formalmente, si los grupos $A$ y $B$ tienen representantes con varianzas $\lambda_A$ y $\lambda_B$ y correlación $r_{AB}$, el PCA del par da

$$
\mu_{1,2}=\frac{\lambda_A+\lambda_B\pm\sqrt{(\lambda_A-\lambda_B)^2+4r_{AB}^2\lambda_A\lambda_B}}{2},
$$

y el índice de la fusión es $\mu_2$: la inercia que se pierde al resumir los dos grupos con un solo factor. Un índice bajo significa que los dos grupos «son lo mismo»; uno alto, que son cosas distintas. Como la fórmula depende de $r_{AB}^2$ y no de su signo, dos series con correlación negativa fuerte también se fusionan pronto.

**Cómo se interpreta.** El resultado se dibuja como un **dendrograma**, un árbol en el que cada nodo se ubica a la altura de su índice. Las series que se unen abajo son casi intercambiables; las ramas que se unen arriba reúnen grupos distintos. Cada nodo tiene su propio plano factorial: el primer eje sintetiza lo que comparten sus series y el segundo, sus diferencias [@camiz_et_al_2020]. Si las correlaciones del representante con todas sus series tienen el mismo signo, el representante es una especie de centroide, una serie promedio del grupo. Si algunas tienen signo opuesto, el nodo es un **dipolo**, que reúne dos subgrupos que se mueven en sentido contrario y debe leerse como su oposición [@camiz_et_al_2020].

**Dónde cortar.** Para obtener una partición se corta el dendrograma. Como reunir series sin correlación no tiene sentido, el corte se decide con los índices [@camiz_et_al_2020]: se mantienen separados los grupos cuya fusión tiene un índice mayor que 0,7. @camiz_et_al_2020 toman ese umbral de la recomendación de Jolliffe de considerar relevante una dimensión cuyo valor propio sea al menos 0,7; un segundo eje por debajo de ese valor se trata como ruido.

**Relación con el PCA.** Los representantes de los nodos pueden proyectarse sobre el PCA como elementos ilustrativos, lo que permite leer ambos análisis juntos. A diferencia de las componentes principales, no son ortogonales, pero, junto con el representante de la raíz, descomponen la inercia total [@camiz_et_al_2020]: la suma de los índices de todos los nodos más la varianza del representante de la raíz es igual a $p$. Esta identidad dice qué parte de la información resumen los grupos y qué parte queda en sus diferencias internas.

**Limitaciones.** El algoritmo es voraz: en cada paso hace la mejor fusión posible, sin revisar las anteriores, de modo que la jerarquía final no es necesariamente óptima. Además, la jerarquía está anidada por construcción: dos series unidas en un paso no pueden separarse después. Para medir cuánto depende la partición de la muestra, se recalcula en réplicas por bloques de meses (sección 2.2.9) y se compara con la original mediante el índice de Rand ajustado, que vale 1 cuando dos particiones coinciden y alrededor de 0 cuando coinciden al azar [@hubert_arabie_1985], y con la correlación cofenética entre dendrogramas.

### 2.2.6 Análisis evolutivo: EPCA y HFC evolutiva

**Problema que resuelve.** En una tabla de datos ordinaria, las relaciones entre variables pueden suponerse iguales para todas las unidades. En las series de tiempo eso puede dejar de ser cierto: las relaciones pueden variar según condiciones que también cambian en el tiempo, y un PCA de todo el período no da información suficiente sobre la estructura [@camiz_diblasi_2013; @camiz_spada_2024].

**La idea del EPCA.** El análisis evolutivo de componentes principales define una ventana de $w$ meses, hace un PCA con los meses de la ventana, la desplaza un mes y repite el análisis hasta recorrer la muestra [@camiz_maulucci_roig_2010; @camiz_diblasi_2013]. Con 228 meses y una ventana de 48 se obtienen 181 PCA. Esa información se resume en dos gráficos [@camiz_diblasi_2013]:

- **la evolución de los primeros valores propios**: un primer valor propio alto indica que en esa ventana las series se mueven casi como una; uno bajo, que se desincronizan;
- **la evolución de las correlaciones de cada serie con los primeros ejes**: un cambio de signo o de magnitud indica que cambia el *significado* del eje, es decir, quién provoca el cambio.

Cada resultado se fecha en el mes central de su ventana.

**El ancho de la ventana.** La ventana debe tener bastantes más meses que series; si no, la matriz de correlaciones es singular. Por encima de ese mínimo, el ancho es un compromiso. Una ventana corta es sensible y fácil de interpretar, pero puede dar demasiado peso al ruido local; una larga atenúa el ruido, pero sus diferencias son más difíciles de entender. Si las series tienen una periodicidad, conviene que el ancho sea un múltiplo de ella [@camiz_spada_2024]. Con una ventana de 25 unidades, la diferencia entre dos ventanas sucesivas es de alrededor del 4 % de la variación total [@camiz_maulucci_roig_2010]. La tesis no busca la ventana «correcta»: compara anchos de 24, 36, 48 y 60 meses y lee los resultados en varias escalas a la vez. El ancho de 48 meses es el de @camiz_cerda_atoche_2026, para poder comparar.

**Los pesos.** Con pesos uniformes, el cambio entre ventanas depende solo de dos meses separados por $w-1$ meses. @camiz_diblasi_2013 proponen ponderar los meses con una función gaussiana: cada mes entra a la ventana con poco peso, gana peso hasta el centro y lo pierde hasta salir, de modo que la evolución se suaviza y refleja mejor el período en torno al mes central [@camiz_spada_2024]. En el programa del asesor [@camiz_aedeclahfac], el peso del mes $i=1,\dots,w$ de la ventana es

$$
\omega_i\propto\exp\!\Big[-\tfrac12\Big(\nu\,\frac{i-\bar\imath}{s}\Big)^2\Big],\qquad \bar\imath=\frac{w+1}{2},\quad s=\frac{w-1}{\sqrt2},\quad \sum_i\omega_i=1,
$$

donde $\nu$ fija cuán concentrados están los pesos ($\nu=0$ da pesos uniformes); @camiz_spada_2024 usan $\nu=3$. Cada ventana usa la correlación ponderada

$$
r^{(i)}_{jl}=\frac{\sum_{t}\omega_t\,(x_{tj}-\bar x^{\omega}_j)(x_{tl}-\bar x^{\omega}_l)}{\sqrt{\sum_t\omega_t(x_{tj}-\bar x^{\omega}_j)^2}\sqrt{\sum_t\omega_t(x_{tl}-\bar x^{\omega}_l)^2}},
$$

con medias ponderadas $\bar x^{\omega}_j$. Los pesos tienen un costo: al concentrar el peso en el centro, la ventana equivale a menos meses. El tamaño efectivo de una ventana ponderada es $n_\omega=1/\sum_i\omega_i^2$, una fórmula atribuida habitualmente a Kish (1965); con 48 meses y $\nu=3$ equivale a unos 37 meses.

**Resolución temporal y bordes.** Cada valor se fecha en el mes central, pero un evento ocurrido en el mes $s$ afecta a todas las ventanas que lo contienen, centradas entre unos $w/2$ meses antes y $w/2$ meses después. Por eso dos cambios separados por menos de una ventana no se distinguen, y un cambio puede aparecer en la curva antes de ocurrir. Además, cuando un episodio entra o sale de la ventana, puede producir un salto que no es un cambio de régimen sino un efecto de **borde de ventana**.

**El signo de los ejes y los ejes casi iguales.** El signo de un vector propio es arbitrario, de modo que el mismo eje puede salir invertido de una ventana a la siguiente. El programa fija el signo para minimizar la diferencia con la ventana anterior, aunque esa alineación no siempre da el resultado esperado [@camiz_diblasi_2013; @camiz_spada_2024]. Un problema más serio aparece cuando el primer y el segundo valor propio de una ventana son casi iguales: los dos ejes dejan de estar determinados por separado, y lo que parece un cambio de las correlaciones con el eje 1 puede ser solo una rotación dentro del plano 1–2.

**Herramientas complementarias de la tesis.** Tres procedimientos ayudan a leer el EPCA:

- *Umbrales por ventana.* En cada ventana se compara cada valor propio con el umbral de Kaiser y con el del análisis paralelo calculado con el tamaño efectivo de la ventana, para saber cuántos ejes superan el ruido en cada momento.
- *Regla de estabilidad.* Se mide, con la correlación entre sus cargas, cuánto se parece el eje 2 de una ventana al de la ventana tres meses anterior; hay una **transición candidata** cuando esa estabilidad cae por debajo de su media menos una desviación típica. Como el umbral es relativo al propio perfil, la regla marca transiciones aunque la estructura sea constante; por eso sus resultados solo se consideran confirmados si superan el nulo de estructura constante (sección 2.2.9) y aparecen con al menos dos anchos y con los dos esquemas de pesos.
- *Nulo de estructura constante* (sección 2.2.9).

Ventanas sucesivas comparten casi todos sus meses, de modo que la curva del EPCA es suave por construcción: que se vea un cambio no prueba que lo haya.

**HFC evolutiva.** La misma idea se aplica a la HFC: en cada posición de la ventana se construye la jerarquía completa de las series, con los mismos pesos que el EPCA. @camiz_spada_2024 la llaman **HFC evolutiva** y siguen la evolución de los índices de los nodos superiores y la sucesión de dendrogramas, mediante una animación o comparándolos con distancias entre árboles. Dos lecturas resultan útiles: los índices de los nodos superiores muestran si los grupos se mantienen bien diferenciados, y los dendrogramas, qué series cambian de grupo. El programa claede del asesor [@camiz_claede_2025] implementa este procedimiento. Su principal dificultad es que las clases de ventanas distintas no están emparejadas de antemano: hay que reconocer, ventana por ventana, cuál grupo corresponde a cuál.

### 2.2.7 Comparación de configuraciones

Para decir si la estructura de dos ventanas es «parecida», o si una réplica bootstrap reproduce el resultado original, hace falta medir la similitud entre dos configuraciones de las mismas series. @abdi_2010 distingue dos coeficientes. El **coeficiente de congruencia** de Tucker es el coseno entre dos vectores de cargas,

$$
\phi(a,b)=\frac{\sum_j a_jb_j}{\sqrt{\sum_j a_j^2\,\sum_j b_j^2}}\in[-1,1];
$$

es sensible a la orientación de los ejes, por lo que sirve para comparar un eje concreto. El **coeficiente RV** compara configuraciones completas: para dos tablas $A$ y $B$ con las mismas filas,

$$
\mathrm{RV}(A,B)=\frac{\operatorname{tr}(AA^\top BB^\top)}{\sqrt{\operatorname{tr}\big((AA^\top)^2\big)\,\operatorname{tr}\big((BB^\top)^2\big)}}\in[0,1].
$$

Es un coseno entre las matrices de productos escalares; vale 1 cuando las configuraciones coinciden salvo una rotación o un cambio de escala, y no le afecta el signo de los ejes [@abdi_2010]. Un valor alto no basta para afirmar que dos estructuras son iguales: el RV no vale cero cuando no hay relación, y su valor esperado depende del número de filas y de columnas, por lo que se evalúa frente a una distribución simulada y no con un umbral fijo [@abdi_2010]. En la tesis, el RV compara las cargas de los tres primeros ejes de **ventanas adyacentes que no comparten meses**; entre ventanas solapadas, el RV es cercano a 1 por construcción.

### 2.2.8 Datación de regímenes: la partición óptima de Fisher

**El problema.** @fisher_1958 plantea el problema de agrupar $K$ elementos, cada uno con un valor $a_i$ y un peso $w_i$, en $G$ grupos de modo que la variación dentro de los grupos sea mínima:

$$
D=\sum_{i=1}^{K}w_i\,(a_i-\bar a_{g(i)})^2,
$$

donde $\bar a_{g(i)}$ es la media ponderada del grupo del elemento $i$. Distingue dos variantes. En el problema **sin restricciones**, los elementos pueden agruparse libremente. En el problema **restringido**, se impone un orden previo; en una serie de tiempo, cada grupo debe estar formado por períodos **consecutivos**. Su ejemplo es el nivel del lago Michigan-Huron entre 1860 y 1955: definir épocas de años consecutivos con la menor variación interna posible [@fisher_1958]. La contigüidad es esencial para datar regímenes: un régimen es un intervalo de tiempo, y una clasificación libre podría poner en el mismo grupo meses de 2008 y de 2020.

**Cómo se resuelve.** Enumerar todas las particiones es imposible: para 96 años en 10 épocas hay más de un billón. Fisher demuestra un **lema de suboptimización**: si se divide el conjunto en dos partes y cada una se agrupa de forma óptima, la unión de esas soluciones es óptima entre las particiones que respetan esa división. Gracias a él, la solución exacta se obtiene extendiendo paso a paso las mejores particiones de los tramos iniciales [@fisher_1958]; hoy se implementa por programación dinámica. El método da, para cada número de grupos, la partición óptima, sin inicialización aleatoria ni mínimos locales. Cuando la trayectoria tiene varias dimensiones —los tres *scores* del PCA—, $D$ se sustituye por la suma de las distancias cuadradas a la media del tramo; @fisher_1958 ya sugería reducir problemas multivariados con el primer componente principal antes de agrupar.

**Cuántos regímenes.** El método no elige el número de tramos, y ese es su punto débil: al aumentar el número de grupos, $D$ siempre disminuye. @fisher_1958 señala que la forma en que $D$ cae ayuda a decidir. Un criterio formal es el índice de Caliński y Harabasz, que compara la variación entre tramos con la variación dentro de ellos, cada una dividida por sus grados de libertad:

$$
\mathrm{CH}(K)=\frac{B_K/(K-1)}{W_K/(n-K)},
$$

donde $B_K$ y $W_K$ son las sumas de cuadrados entre y dentro de los $K$ tramos de $n$ puntos [@calinski_harabasz_1974]. @camiz_cerda_atoche_2026 y @camiz_spada_2024 eligen el $K$ en un máximo local del índice. En trayectorias suaves, como las del EPCA, la suma dentro de los tramos cae rápido al aumentar $K$ y el índice tiende a crecer sin un máximo interior; @purizaca_2023 encuentra exactamente eso. Por esa razón, la tesis **informa** el índice, en la variante del programa aede [@camiz_aedeclahfac], que usa $K$ en lugar de $K-1$, y en la habitual, pero **no lo usa para elegir**, salvo que muestre un máximo interior con un tope de 20 tramos y fuera del rango del nulo de estructura constante. El número de tramos se elige con una regla fijada antes de calcular: el menor $K$ a partir del cual pasar a $K+1$ tramos reduce $W_K$ en menos de 10 %; si no hay ninguno, el $K$ con la mayor caída de $W_K$. Se exige, además, que cada tramo dure al menos 12 meses, para no aislar meses atípicos; es una elección, no un resultado.

**El suavizado de los *scores* y su retardo.** Antes de partirlos, los *scores* del PCA se suavizan con una media móvil de los 12 meses anteriores, para quitar el ruido mensual. Esa media solo usa meses pasados, de modo que un cambio de nivel ocurrido en el mes $\tau$ aparece en la media gradualmente entre $\tau$ y $\tau+11$, con un retardo medio de $(12-1)/2=5{,}5$ meses. Los cortes tienden, por tanto, a fecharse después del cambio, y la comparación con los episodios debe tenerlo en cuenta. La tesis mantiene la media causal como especificación principal, porque se fijó antes de calcular, y repite la datación con una media centrada como sensibilidad.

**La regla de fases.** Una vez fechados los regímenes, se les asigna una fase con una regla provisional: se promedia, en el régimen, el crédito estandarizado (media de los tres tipos de crédito); la fase es **expansión** si ese promedio es mayor que 0,25, **contracción** si es menor que −0,25 y **transición** si está entre ambos valores o si el régimen dura menos de 18 meses. La regla está pendiente de discusión con el asesor (sección 3.1.7).

### 2.2.9 Nulos de referencia y remuestreo

**Qué es un nulo en un análisis exploratorio.** Un análisis exploratorio siempre encuentra *alguna* estructura: el PCA siempre tiene un primer eje, la HFC siempre forma grupos y el EPCA siempre muestra valores propios que fluctúan. Un **nulo** responde a la pregunta de qué mostraría el método si no existiera la estructura buscada, conservando todo lo demás. @horn_1965 aplica esta idea al número de ejes; la tesis la extiende a otras preguntas. Cada nulo conserva unas propiedades de los datos y destruye otras, y la conclusión depende de cuáles. El resultado se expresa como la proporción de simulaciones que producen un valor igual o más extremo que el observado; no es la probabilidad de que la hipótesis sea cierta. Y no superar un nulo no prueba que la estructura no exista: puede significar que el contraste tiene poca **potencia** con tan pocos datos independientes.

- **Nulo de tendencias.** ¿Es el primer eje una estructura común o solo la tendencia compartida? Se simulan 16 series independientes entre sí, cada una con la forma de crecimiento de la serie real, y se calcula el PCA de cada simulación. Conserva la dinámica de cada serie y destruye la relación entre series. La forma de crecimiento importa: con caminatas aleatorias con deriva para todas las series, el primer eje observado no se distingue del simulado; sin deriva, sí. Por eso la tesis fijó antes de calcular un **nulo mixto**, serie por serie: recta más residuos remuestreados para las series TS; caminata con deriva para las DS con deriva significativa ($\lvert t\rvert$ robusto mayor que 2), y sin deriva para las demás; las series de clasificación indeterminada se simulan de las dos maneras.
- **Nulo de estructura constante.** ¿Cambia la estructura de correlación más de lo que cambiaría por azar? Se simulan series con la misma dependencia temporal que las reales y una correlación fija en todo el período, se les aplica el mismo EPCA y se mide, con el coeficiente RV, cuán distintas son las ventanas adyacentes que no comparten meses. Conserva la correlación entre series y la autocorrelación de cada una, y destruye el cambio en el tiempo. Si los cambios observados no superan a los simulados, no hay evidencia de que la estructura cambie.
- **Bootstrap por bloques.** ¿Se repetiría el resultado con datos algo distintos? El bootstrap habitual sortea meses al azar, lo que destruye la dependencia temporal. El bootstrap por bloques sortea bloques de meses consecutivos y los concatena; usar los mismos inicios de bloque para todas las series conserva también la correlación entre ellas [@kunsch_1989]. El largo del bloque es un compromiso: bloques largos conservan mejor la dependencia, pero dan réplicas más parecidas entre sí. La tesis usa 24 meses y comprueba 12 y 36.

### 2.2.10 Autoencoders y redes LSTM

**Autoencoder.** Un autoencoder es una red neuronal que aprende a comprimir los datos y a reconstruirlos. Tiene dos partes: un codificador $g_\phi:\mathbb{R}^p\to\mathbb{R}^d$, que reduce cada mes a $d$ números (el **espacio latente**), y un decodificador $h_\theta:\mathbb{R}^d\to\mathbb{R}^p$, que intenta reconstruir el mes a partir de ellos. Se entrena minimizando el error de reconstrucción

$$
L(\phi,\theta)=\frac1n\sum_t\lVert z_t-h_\theta(g_\phi(z_t))\rVert^2 .
$$

Si el codificador y el decodificador son lineales, el óptimo genera el mismo subespacio que los $d$ primeros ejes del PCA [@baldi_hornik_1989]: el PCA es el caso lineal del autoencoder. Con capas no lineales, el autoencoder puede representar relaciones curvas que el PCA no capta; @hinton_salakhutdinov_2006 muestran, con miles de imágenes de dígitos y rostros y con documentos de texto, que los autoencoders profundos superan al PCA en la calidad de la representación de baja dimensión, y la variante con eliminación de ruido mejora su robustez [@vincent_et_al_2008].

**Redes LSTM.** El autoencoder trata cada mes por separado. Una red LSTM, en cambio, procesa la secuencia de meses y conserva una memoria de lo ocurrido antes [@hochreiter_schmidhuber_1997]. Su celda de memoria $c_t$ se actualiza en cada mes mediante compuertas que deciden qué información nueva entra ($i_t$), qué parte de la memoria se conserva ($f_t$) y qué parte se usa para producir la salida ($o_t$):

$$
\begin{aligned}
i_t&=\sigma(W_i z_t+U_i h_{t-1}+b_i), & f_t&=\sigma(W_f z_t+U_f h_{t-1}+b_f), & o_t&=\sigma(W_o z_t+U_o h_{t-1}+b_o),\\
\tilde c_t&=\tanh(W_c z_t+U_c h_{t-1}+b_c), & c_t&=f_t\odot c_{t-1}+i_t\odot\tilde c_t, & h_t&=o_t\odot\tanh(c_t),
\end{aligned}
$$

donde $\sigma$ es la función logística y $\odot$, el producto elemento a elemento. Este diseño permite aprender dependencias de muchos pasos, algo que las redes recurrentes simples no logran [@hochreiter_schmidhuber_1997]; la compuerta de olvido $f_t$ es una extensión posterior [@gers_schmidhuber_cummins_2000]. El **LSTM-autoencoder** codifica una ventana de meses consecutivos en un vector latente y la reconstruye [@srivastava_mansimov_salakhutdinov_2015]; su trayectoria latente representa la dinámica del sistema y puede compararse con la de los *scores* del PCA.

**Para qué se usan en la tesis.** El aprendizaje profundo aporta dos cosas que el PCA no puede dar por construcción: representar la dinámica de la trayectoria (la LSTM) y señalar los meses que no comparten la estructura típica, porque el modelo los reconstruye mal. Un error de reconstrucción que sube en ciertos meses es una señal de atipicidad que puede asociarse a episodios de tensión.

**Supuestos y escala.** Estos modelos introducen supuestos que no provienen de los datos: el número de capas, la función de activación, la dimensión latente, la longitud de la ventana, la regularización y la semilla aleatoria. Además, requieren muchos datos: @tuhin_et_al_2025 usan 375 series diarias durante 23 años, mientras que aquí hay 16 series mensuales con un tamaño efectivo de unas diez observaciones, y los parámetros de una red superan con holgura a las observaciones independientes. La tesis acota esa tensión con cuatro principios: (a) el PCA es el anclaje lineal, y cada modelo se compara con él en la misma escala de error; (b) la no linealidad se acepta solo si mejora la reconstrucción **fuera de muestra**, evaluada con validación por bloques y *walk-forward* (entrenar hasta un año y evaluar el siguiente); (c) un resultado que cambia con la semilla aleatoria no se considera emergido de los datos, y (d) la incertidumbre se estima con Monte Carlo Dropout, que repite la predicción desactivando al azar parte de las neuronas, de modo que la dispersión de las predicciones mide cuán segura es la red [@gal_ghahramani_2016]. Con estos principios, los autoencoders y las redes LSTM son un complemento de la cadena PCA–HFC–EPCA y no su reemplazo.

## 2.3 Definición de términos

- **Ciclo financiero:** movimiento conjunto de expansión y contracción del crédito y de los precios de los activos [@drehmann_borio_tsatsaronis_2012].
- **Régimen:** intervalo de meses contiguos en el que la estructura de las series es relativamente homogénea.
- **Fase:** etiqueta (expansión, contracción o transición) asignada a un régimen después de detectarlo.
- **Datación (fechado):** operación de ubicar en el calendario las transiciones entre regímenes, es decir, de dividir el período en tramos de meses consecutivos homogéneos y reportar las fechas de los cortes [@fisher_1958; @drehmann_borio_tsatsaronis_2012].
- **Transición:** cambio de la estructura de las series que se mantiene en los meses siguientes.
- **Episodio de referencia:** evento con fecha documentada por una fuente independiente de las series, usado para validar los cortes.
- **Inercia:** suma de las distancias cuadradas de los puntos a su centro de gravedad; con series estandarizadas, es igual al número de series [@camiz_2021_pca].
- **Carga:** correlación entre una serie y un eje del PCA.
- **Calidad de representación (cos²):** parte de la inercia de una serie que recoge un eje o un plano [@camiz_2021_pca].
- **Contribución:** peso de una serie en la formación de un eje [@camiz_2021_pca].
- ***Score*:** coordenada de un mes en un eje del PCA.
- **Clasificación factorial jerárquica (HFC):** clasificación jerárquica de variables en la que cada grupo se resume con un factor [@camiz_et_al_2020].
- **Índice de nodo:** segundo valor propio del PCA que fusiona dos clases en la HFC; mide la inercia que el nuevo factor no explica.
- **Representante de un nodo:** primer componente principal de las series de un grupo de la HFC; resume lo que tienen en común [@camiz_et_al_2020].
- **Dipolo:** nodo de la HFC cuyas series se correlacionan con el representante con signos opuestos; se interpreta como la oposición de dos subgrupos [@camiz_et_al_2020].
- **Dendrograma:** árbol que representa la jerarquía de la HFC, con cada nodo a la altura de su índice.
- **Análisis evolutivo de componentes principales (EPCA):** PCA aplicado en ventanas móviles, con pesos uniformes o gaussianos, para observar cómo cambia la estructura de correlación [@camiz_diblasi_2013].
- **HFC evolutiva:** HFC aplicada en cada posición de una ventana móvil [@camiz_claede_2025].
- **Coeficiente RV:** medida, entre 0 y 1, de la similitud entre dos configuraciones de las mismas variables [@abdi_2010].
- **Partición óptima de Fisher:** división de una secuencia ordenada en tramos contiguos que minimiza la suma de cuadrados dentro de los tramos [@fisher_1958].
- **Nulo simulado:** conjunto de series artificiales que reproduce una propiedad de los datos (tendencia, dependencia temporal o estructura constante) y sirve de referencia para juzgar si un resultado podría deberse a ella.
- **Bootstrap por bloques:** remuestreo de bloques de meses consecutivos que conserva la dependencia temporal de las series [@kunsch_1989].
- **Tamaño efectivo de muestra:** número de observaciones independientes equivalente a una muestra autocorrelacionada [@pyper_peterman_1998].
- **Trayectoria:** sucesión mensual de un indicador que resume el sistema, como el primer valor propio evolutivo o los *scores* del PCA; es lo que se data.
- **Corte:** primer mes de un nuevo tramo en la datación.
- **Tramo:** intervalo de meses consecutivos entre dos cortes; cuando su estructura es homogénea, se interpreta como un régimen.
- **Ventana:** intervalo de meses consecutivos sobre el que se calcula un análisis evolutivo; se fecha en su mes central.
- **Valor propio evolutivo:** valor propio del PCA calculado en una ventana; su sucesión mide cómo cambia la intensidad de la estructura común [@camiz_maulucci_roig_2010].
- **Pesos gaussianos:** ponderación de los meses de una ventana según una curva normal centrada en el mes central, que reduce el efecto de los meses que entran y salen [@camiz_diblasi_2013].
- **Tamaño efectivo de una ventana:** número de meses con igual peso que equivale a una ventana ponderada, $n_\omega=1/\sum\omega_i^2$.
- **Borde de ventana:** meses iniciales y finales de la muestra, que no pueden ser centro de una ventana completa y por eso quedan fuera del análisis evolutivo.
- **Tolerancia:** distancia máxima, fijada de antemano, entre un corte y un episodio para considerarlos compatibles (tres meses en el análisis principal).
- **Serie estacionaria en tendencia (TS):** serie que oscila alrededor de una tendencia determinista y vuelve a ella después de un choque.
- **Serie integrada (DS):** serie cuyos choques se acumulan; se vuelve estacionaria al diferenciarla [@dickey_fuller_1979].
- **Deriva:** crecimiento medio por período de una serie integrada.
- **Regresión espuria:** correlación alta entre series independientes producida por sus tendencias [@granger_newbold_1974].
- **Nulo de tendencias:** nulo simulado en el que cada serie conserva su propio tipo de tendencia, pero las series son independientes entre sí.
- **Nulo de estructura constante:** nulo simulado con una correlación fija entre las series y la misma autocorrelación que los datos.
- **Congruencia:** coseno del ángulo entre dos vectores de cargas; mide si dos ejes tienen la misma orientación [@abdi_2010].
- **Índice de Rand ajustado:** medida del acuerdo entre dos particiones, que vale 1 si son idénticas y alrededor de 0 si coinciden por azar [@hubert_arabie_1985].
- **Correlación cofenética:** correlación entre las distancias que implican dos dendrogramas; mide si tienen la misma forma.
- **Serie más representativa de una clase:** serie más correlacionada con el representante de su clase.
- **Regla de fases:** regla fijada de antemano que asigna a cada régimen una fase a partir del comportamiento del crédito.
- **Autoencoder:** red neuronal que comprime los datos en un espacio latente de menor dimensión y los reconstruye [@hinton_salakhutdinov_2006].
- **LSTM:** red recurrente con celdas de memoria y compuertas, capaz de modelar dependencia temporal larga [@hochreiter_schmidhuber_1997].

# CAPÍTULO III. DESARROLLO DEL TRABAJO DE INVESTIGACIÓN

## 3.1 Análisis de los datos y resultados

Los resultados corresponden al análisis principal, con las {{nSeries}} series en niveles, y siguen las etapas de la estrategia de análisis (Tabla {T:estrategia}). La HFC y el EPCA se calcularon con las rutinas del asesor trasladadas a Python, cuya equivalencia con el programa en R está verificada; la HFC evolutiva replica el procedimiento de su programa claede, con una verificación todavía pendiente. Cada resultado se acompaña de su interpretación y de su contraste con los nulos. La interpretación es preliminar y todavía no se ha discutido con el asesor.

### 3.1.1 Las series analizadas

La Figura {F:series} muestra las {{nSeries}} series en sus unidades originales, con los episodios de referencia sombreados. Las series se dividen en dos tipos con comportamientos muy distintos.

- **Saldos y niveles que crecen.** Entre enero de 2007 y diciembre de 2025, el crédito empresarial se multiplicó por 6,5; el de consumo, por 9,1; el hipotecario, por 9,5; la liquidez M3, por 5,9, y las reservas internacionales, por 5,1. El índice de precios de Lima creció 85 % y el PBI desestacionalizado se duplicó. Estas series reflejan a la vez el crecimiento de la economía, la inflación acumulada y la **profundización financiera**, es decir, el aumento del peso del crédito y del dinero en la economía.
- **Precios y tasas que oscilan.** La tasa de referencia del BCRP fue de 6,5 % en septiembre de 2008 a 1,25 % en agosto de 2009, se mantuvo en 4,25 % entre mayo de 2011 y octubre de 2013, bajó a 0,25 % entre abril de 2020 y julio de 2021 y subió a 7,75 % en enero de 2023. El EMBIG alcanzó su máximo, 523 puntos básicos, en diciembre de 2008. El tipo de cambio osciló entre 2,55 soles por dólar en enero de 2013 y 4,11 en septiembre de 2021. La TAMN bajó de 23,8 % a 15,9 % en el período.

El diagnóstico de tendencia confirma esta división (Tabla {T:tendencia}). Doce series son integradas (DS), tres quedan sin clasificar —el crédito de consumo, la TIPMN y el PBI— y solo el EMBIG es estacionario alrededor de una tendencia (TS). La deriva es significativa en los créditos, M1, M3, el índice de precios y las reservas, y está en el límite en el PBI y la demanda interna (|*t*| de 2,29 y 2,27). El tipo de cambio y la bolsa, aunque están correlacionados con el tiempo (0,81 y 0,61), no tienen una deriva significativa ($t$ de 0,20 y 1,34): suben y bajan sin una tendencia sostenida. Las tasas no tienen deriva.

::: {custom-style="Rotulo"}
**Figura {F:series}**\
*Series analizadas en sus unidades originales*
:::

![](fig/avance_series_niveles.png){width=100%}

::: {custom-style="Nota"}
*Nota.* En gris, los episodios de la Tabla {T:episodios}; la línea discontinua marca el episodio puntual de marzo de 2018. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Tabla {T:tendencia}**\
*Tipo de tendencia y deriva de cada serie*
:::

[[CSV:tendencia_series.csv]]

::: {custom-style="Nota"}
*Nota.* DS: integrada; TS: estacionaria en tendencia; Ind.: sin clasificar (las pruebas ADF y KPSS no coinciden). *t* de la deriva: media de los incrementos mensuales dividida por su error estándar robusto a la autocorrelación (12 rezagos). *r* con el tiempo: correlación de la serie con el número de mes. Elaboración propia con datos del BCRP.
:::

### 3.1.2 Estructura de correlación

En niveles, 33 de los 120 pares de series tienen una correlación mayor que 0,9 en valor absoluto, y la mediana del valor absoluto de las correlaciones es 0,61 (Figura {F:corr}). Con 228 meses, el 82,5 % de los pares tiene una correlación significativa; con el tamaño efectivo de cada par, solo el 42,5 %. Para saber cuánto de esa asociación se debe a la tendencia, se quitó a cada serie su recta de tendencia y se recalcularon las correlaciones (Figura {F:corrst}): solo un par conserva una correlación mayor que 0,9, la mediana baja a 0,28, el primer eje del PCA pasa de recoger el 65,2 % de la inercia al 38,5 % y el KMO baja de 0,84 a 0,68.

**Interpretación.** Más de la mitad de la estructura visible en niveles es tendencia compartida, el efecto que @granger_newbold_1974 advierten para series con tendencia. Lo que sobrevive al quitar la tendencia es menos, pero no es nada: un KMO de 0,68 indica que las desviaciones de las series respecto de su tendencia todavía comparten información. Esa información residual es la que interesa para el ciclo, y la que los nulos de las secciones siguientes ayudan a separar.

::: {custom-style="Rotulo"}
**Figura {F:corr}**\
*Matriz de correlación de las series en niveles*
:::

![](fig/05_correlaciones.png){width=78%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura {F:corrst}**\
*Matriz de correlación de las series sin su tendencia lineal*
:::

![](fig/05_correlaciones_sin_tendencia.png){width=78%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

### 3.1.3 Análisis de componentes principales

**Adecuación.** La medida KMO es {{kmoGlobalNiveles}}: las series comparten mucha información común. Pero esa información está repetida en el tiempo. Por la fuerte autocorrelación de las series, la mediana del tamaño efectivo de los pares es de {{nEfMedianaNiveles}} observaciones independientes, menos que el número de series. Con ese tamaño, el estadístico de Bartlett baja de {{chiBartlettNiveles}} a {{chiBartlettNefNiveles}} (*p* = 0,007). Como $n_{\mathrm{ef}}$ es menor que $p$, la aproximación $\chi^2$ de la prueba no es fiable y el resultado debe leerse como un indicio, no como una prueba. La consecuencia es la advertencia más importante de este capítulo: la muestra contiene la información independiente de unas diez observaciones, y todo lo que sigue debe leerse con esa limitación.

**Número de ejes.** Los tres primeros ejes explican el {{inerciaPCUnoNiveles}} %, el {{inerciaPCDosNiveles}} % y el {{inerciaPCTresNiveles}} % de la inercia; juntos, el 92,2 % (Figura {F:sedim}). Los criterios discrepan sobre el tercero: su valor propio, 1,21, supera el umbral de Kaiser, pero no el del análisis paralelo (1,36) ni el de la vara quebrada; Kaiser retiene {{kaiserNiveles}} ejes, y el análisis paralelo y la vara quebrada, {{hornNiveles}}. El tercer eje es, por tanto, un eje de frontera. Se trabaja con tres ejes porque así se fijó antes de conocer estas cifras, y la sensibilidad con dos y con cuatro ejes se informa en la datación (sección 3.1.7).

::: {custom-style="Rotulo"}
**Figura {F:sedim}**\
*Valores propios del PCA frente al análisis paralelo y la vara quebrada*
:::

![](fig/05_pca_sedimentacion.png){width=60%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

**Lectura de los ejes.** La Tabla {T:cargas} da las cargas; la Figura {F:circulos}, los círculos de correlaciones, y la Tabla {T:cos2}, la calidad de representación y las contribuciones.

::: {custom-style="Rotulo"}
**Tabla {T:cargas}**\
*Cargas de las series en los tres primeros ejes del PCA*
:::

[[TABLA_CARGAS]]

::: {custom-style="Nota"}
*Nota.* En negrita, las cargas con valor absoluto igual o mayor que 0,6. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura {F:circulos}**\
*Círculos de correlaciones en los planos 1–2 y 1–3*
:::

![](fig/camiz_pca_circulos.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Las flechas son las cargas de las series. Las de saldos, precios y actividad, casi superpuestas sobre el eje 1, se agrupan bajo «Bloque de tendencia». Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Tabla {T:cos2}**\
*Calidad de representación (cos²) y contribuciones de las series a los tres primeros ejes*
:::

[[CSV:camiz_pca_cos2_contrib.csv]]

::: {custom-style="Nota"}
*Nota.* La calidad en el subespacio 1–3 es la suma de los cos² de los tres ejes. Elaboración propia con datos del BCRP.
:::

- **Eje 1: escala del sistema y profundización financiera.** Once series contribuyen al eje en proporciones parecidas, entre 6,1 % y 9,4 %, cerca de 1/11 (9,1 %): el eje lo construyen esas once casi por igual, y las otras cinco aportan poco (la bolsa, 3,7 %; las demás, menos de 1 %). Lo forman los créditos, la liquidez, los precios, la actividad y las reservas, con cargas de 0,93 a 0,99, el tipo de cambio (0,80) y la TAMN en sentido opuesto ({{cargaTamnPCUno}}): en niveles, la caída secular de la tasa activa la alinea, con signo contrario, con el crecimiento de los saldos. La coordenada de los meses en este eje está casi perfectamente correlacionada con el tiempo (*r* = {{rTiempoPCUnoNiveles}}; Figura {F:scores}). Su lectura económica es la escala del sistema: crecimiento, inflación acumulada y profundización financiera. Frente al nulo mixto de tendencias, 16 series independientes, cada una con su propia forma de crecimiento, producen un primer eje igual o mayor en una proporción de 0,783 de las simulaciones (0,826 si las series sin clasificar se tratan como integradas). El eje 1 no prueba, entonces, que las series estén vinculadas por un ciclo común: describe que casi todas crecen.
- **Eje 2: postura de la política monetaria.** Es casi exclusivo de las tres tasas de corto plazo, que suman el 88,0 % de su formación: la tasa de referencia ({{cargaTasaRefPCDos}}), la interbancaria y la TIPMN ({{cargaTipmnPCDos}}). La coordenada de los meses sigue el ciclo de la tasa de referencia descrito en la sección 3.1.1: alcanza su mínimo en julio de 2021, al final del período con la tasa en 0,25 %, y su máximo en agosto de 2023, después del ciclo de alzas que la llevó a 7,75 %. Es ortogonal a la profundización: mide si la política está más o menos restrictiva, independientemente del tamaño del sistema. Frente al nulo mixto, solo 0,003 de las simulaciones (0,004 con la otra variante) producen un segundo eje tan grande: es el único co-movimiento que no puede atribuirse a las tendencias propias de cada serie. Que las tres tasas se muevan juntas es esperable, porque la tasa de referencia se transmite a la interbancaria y a la pasiva; lo relevante es que esa transmisión forma un bloque estructural separado del de los saldos.
- **Eje 3: aversión al riesgo.** Opone el EMBIG ({{cargaEmbigPCTres}}), que mide el riesgo soberano, al índice de la Bolsa de Valores de Lima ({{cargaBvlPCTres}}); ambas series aportan el 85,2 % de su formación. Un valor alto del eje indica mayor riesgo percibido y bolsa deprimida. Sus picos ocurren en diciembre de 2008 (4,47), el mes del máximo del EMBIG; en febrero de 2016 (2,23), al final del colapso de las materias primas; en abril de 2020 (2,41), al inicio de la pandemia, y en agosto de 2021 (1,67). Este último no corresponde a ningún episodio de la Tabla {T:episodios}: es una señal de tensión que la tesis todavía no ha documentado con una fuente externa. Frente al nulo mixto, el eje no se distingue de series independientes (proporción de 0,221 y 0,223), de modo que su lectura es descriptiva.

El tipo de cambio y el índice de la BVL son las series peor representadas por los tres ejes (calidad de 0,77 y 0,79): parte de su información es propia. Bajo bootstrap por bloques de 24 meses, el percentil 5 de la congruencia con el eje original es {{congruenciaBootPCUnoNiveles}}, {{congruenciaBootPCDosNiveles}} y {{congruenciaBootPCTresNiveles}} para los ejes 1 a 3, frente a {{congruenciaBootPCCuatroNiveles}} para el cuarto: en el 95 % de las réplicas, los tres primeros ejes conservan su orientación con una congruencia de al menos 0,79, y el cuarto no. Con bloques de 36 meses, el percentil 5 de los ejes 2 y 3 baja a 0,71 y 0,74: su estabilidad depende del largo del bloque.

::: {custom-style="Rotulo"}
**Figura {F:scores}**\
*Coordenadas de los meses en los tres primeros ejes del PCA*
:::

![](fig/avance_scores_pca.png){width=100%}

::: {custom-style="Nota"}
*Nota.* En gris, los episodios de referencia. Elaboración propia con datos del BCRP.
:::

### 3.1.4 Clasificación factorial jerárquica

**El dendrograma.** La Figura {F:dendro} muestra el dendrograma de la HFC y la Tabla {T:nodos}, sus nodos superiores. La lectura va de abajo hacia arriba. Los primeros nodos unen pares de series casi intercambiables, con índices menores que 0,03: la tasa de referencia con la interbancaria (0,003), el crédito de consumo con el hipotecario (0,008), el crédito empresarial con M3 (0,014) y el PBI con la demanda interna (0,024); el índice de precios y M1 se suman a esos pares con índices similares. Luego se unen esos grupos y se incorporan las reservas (0,101), la TAMN (0,252) y, al final, el tipo de cambio (0,353), coherente con su menor calidad en el PCA. El nodo 28 reúne así once series con un índice de solo {{czIndiceNodo28}}. Por separado se forman el nodo 25, con las tres tasas de corto plazo ({{czIndiceNodo25}}), y el nodo 29, con el EMBIG y la bolsa ({{czIndiceNodo29}}). Los dos últimos nodos tienen índices mucho mayores, y ese salto es lo que hace evidente el corte.

::: {custom-style="Rotulo"}
**Figura {F:dendro}**\
*Dendrograma de la clasificación factorial jerárquica de las series*
:::

![](fig/camiz_hfc_dendrograma.png){width=92%}

::: {custom-style="Nota"}
*Nota.* La altura de cada nodo es su índice (segundo valor propio); la línea discontinua marca el corte en 0,7. Los números identifican los nodos superiores. Elaboración propia con datos del BCRP y la rutina clahfac del asesor [@camiz_aedeclahfac].
:::

::: {custom-style="Rotulo"}
**Tabla {T:nodos}**\
*Nodos superiores de la jerarquía de la HFC*
:::

[[CSV:camiz_hfc_nodos.csv]]

::: {custom-style="Nota"}
*Nota.* λ1: varianza del representante del nodo; λ2: índice del nodo; % local λ1: parte de la inercia de las series del nodo que recoge su representante; % global λ2 acum.: suma acumulada de los índices como porcentaje de la inercia total. Elaboración propia con datos del BCRP.
:::

**Lo que dicen los nodos superiores.**

- El representante de la raíz tiene una varianza de 10,337, el 64,6 % de la inercia, casi igual que el primer eje del PCA (10,437; 65,2 %): la HFC resume prácticamente lo mismo que el PCA, pero organizado en grupos interpretables. La identidad de la sección 2.2.5 se cumple: la suma de los índices (5,663) más la varianza de la raíz da 16.
- El índice de la raíz, 2,768, es casi toda la varianza del representante de las tasas (2,791). Al fusionar las tasas con el resto no se gana casi nada, porque sus representantes no están correlacionados (*r* = −0,07; Tabla {T:factores}). En niveles, la política monetaria es una dimensión independiente de la escala del sistema.
- El nodo 30 une el bloque de escala con el de riesgo con una pérdida moderada (1,11). Sus representantes tienen una correlación de −0,48, con un intervalo bootstrap de −0,64 a −0,18: cuando la escala del sistema crece, el riesgo percibido tiende a bajar.

::: {custom-style="Rotulo"}
**Tabla {T:factores}**\
*Correlaciones entre los representantes de las tres clases*
:::

[[CSV:factores_hfc.csv]]

::: {custom-style="Nota"}
*Nota.* Correlación de Pearson entre los representantes de las clases de la partición en tres; entre corchetes, percentiles 5 y 95 en 500 réplicas bootstrap por bloques de 24 meses. «Sin tendencia»: representantes de las series sin su recta de tendencia. Elaboración propia con datos del BCRP.
:::

**Las tres clases.** El corte en 0,7 deja {{czClasesCorte}} clases (Tabla {T:hfc}), que coinciden con los tres ejes del PCA:

- **C1, escala del sistema o «salud económica y financiera»** (11 series). Su representante recoge el 96,6 % de la inercia de sus series, y la serie que mejor lo representa es el crédito hipotecario (*r* = 0,994). La TAMN entra con signo opuesto: el nodo que la incorpora es un dipolo.
- **C2, condiciones monetarias** (3 series). Su representante recoge el 93,1 % de su inercia; la serie que mejor lo representa es la tasa interbancaria (*r* = 0,985).
- **C3, riesgo de mercado** (2 series). Es también un dipolo: el riesgo soberano y la bolsa se mueven en sentido opuesto, de modo que su representante mide la aversión al riesgo. Es la clase menos homogénea (75,3 %); la serie más representativa es el EMBIG (*r* = 0,868).

Estas tres series —crédito hipotecario, tasa interbancaria y EMBIG— son las que mejor hablan por su bloque, y podrían servir como indicadores sencillos de seguimiento.

::: {custom-style="Rotulo"}
**Tabla {T:hfc}**\
*Clases de la HFC en las particiones de tres y cuatro clases*
:::

[[TABLA_HFC]]

::: {custom-style="Nota"}
*Nota.* En negrita, la serie más correlacionada con el representante de su clase. Elaboración propia con datos del BCRP.
:::

**Estabilidad.** En {{hfcReplicas}} réplicas por bloques, la partición en tres clases se reproduce exactamente en una proporción {{hfcPropAriTres}} de las réplicas, y la de cuatro, en {{hfcPropAriCuatro}}. La mediana de la correlación cofenética entre el dendrograma de cada réplica y el original es {{hfcCofeneticaMediana}}. Los tres bloques son, por tanto, un resultado robusto; la separación del EMBIG y la bolsa en dos clases, que da la partición en cuatro, no lo es.

**Sin tendencia.** Al quitar la tendencia, la correlación entre los representantes de la escala y de las tasas pasa de −0,07 a −0,41, con un intervalo bootstrap de −0,64 a −0,005 (Tabla {T:factores}). Las tasas no se relacionan con la tendencia del sistema, pero sí con sus desviaciones respecto de ella: cuando los saldos están por encima de su tendencia, las tasas tienden a estar más bajas. Es la primera señal de un vínculo cíclico entre el bloque monetario y el financiero.

### 3.1.5 Análisis evolutivo de componentes principales

El EPCA se aplicó con la rutina aede del asesor, con la configuración de @camiz_cerda_atoche_2026: ventana de 48 meses con pesos gaussianos ($\nu=3$), equivalente a unos 37 meses efectivos. Se obtienen {{czAedeVentanas}} ventanas, centradas entre enero de 2009 y enero de 2024.

**Intensidad de la estructura común.** El primer valor propio se mantiene entre 8,4 y 12,1 en las ventanas centradas hasta 2019: en las ventanas de esos años, las 16 series se mueven casi como una sola (Figura {F:aede}). Luego cae hasta {{czLambdaMin}} en la ventana centrada en {{czFechaLambdaMin}}, que abarca de mayo de 2019 a abril de 2023. En esa ventana, el primer eje recoge solo el 39 % de la inercia, frente a cerca del 75 % en las ventanas de 2011.

Las propias series muestran por qué. En 2020 y 2021, el crédito empresarial creció hasta 24,4 % anual (septiembre de 2020), mientras el de consumo cayó hasta −11,1 % (febrero de 2021). M1 creció 47,8 % (septiembre de 2020), la inflación llegó a 8,8 % (junio de 2022) y la tasa de referencia pasó de 0,25 % a 7,75 %. Series que durante una década se movieron juntas pasaron a moverse en direcciones distintas. Una explicación posible son las medidas de liquidez y de crédito garantizado de la pandemia, pero esta tesis no la ha documentado todavía con fuentes y queda como hipótesis.

**Cuántos ejes superan el ruido en cada ventana.** Con el tamaño efectivo de cada ventana, el segundo valor propio queda por debajo del umbral del análisis paralelo en 32 de las 181 ventanas, y el tercero en 164. En la mayoría de las ventanas solo dos ejes superan el ruido, por lo que la lectura dinámica se concentra en los dos primeros.

::: {custom-style="Rotulo"}
**Figura {F:aede}**\
*Valores propios evolutivos del EPCA y partición de Fisher del primer valor propio*
:::

![](fig/camiz_aede_valores_propios.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventana de 48 meses con pesos gaussianos; cada valor se fecha en el mes central de su ventana. Línea roja: corte con el criterio de la tesis (mayor caída de la suma de cuadrados). Líneas discontinuas: cortes con el criterio del antecedente (máximo del índice de Caliński y Harabasz de aede, con un tope de 10 tramos). En gris, los episodios de referencia. Elaboración propia con datos del BCRP y la rutina aede del asesor [@camiz_aedeclahfac].
:::

**Datación del primer valor propio.** La Tabla {T:aedepart} da la partición de Fisher del primer valor propio para 1 a 10 tramos.

- *Criterio de la tesis.* Con la regla fijada antes de calcular —el índice de Caliński y Harabasz se informa, pero no selecciona—, la mayor caída de la suma de cuadrados ocurre al pasar de uno a dos tramos: hay **un solo corte, en {{czAedeCorteCodo}}**. Es el hallazgo dinámico más robusto: con el mismo criterio aparece, entre febrero y septiembre de 2020, con las ventanas de 36, 48 y 60 meses y con los dos esquemas de pesos (Tabla {T:cortesgrilla}).
- *Criterio del antecedente.* Con el criterio de @camiz_cerda_atoche_2026 —el máximo del índice de aede con un tope de 10 tramos—, se obtienen tres tramos, con cortes en {{czAedeCortesTexto}}. Pero el índice tiene ese máximo solo con un tope de 10: con topes de 15 o 20, elige siempre el máximo permitido. Lo mismo ocurre en el 100 % de las 200 simulaciones del nulo de estructura constante, es decir, con series cuya estructura no cambia. El corte de 2014 depende, por tanto, de la cota, y no puede tomarse como resultado.

::: {custom-style="Rotulo"}
**Tabla {T:aedepart}**\
*Partición de Fisher del primer valor propio evolutivo para 1 a 10 tramos*
:::

[[CSV:camiz_aede_particion.csv]]

::: {custom-style="Nota"}
*Nota.* SC intra: suma de cuadrados dentro de los tramos. Caliński-Harabasz: variante de aede. Las fechas son los meses centrales de las ventanas en que empieza cada nuevo tramo. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Tabla {T:cortesgrilla}**\
*Cortes del primer valor propio por ancho de ventana y esquema de pesos (criterio de la tesis)*
:::

[[CSV:cortes_grilla.csv]]

::: {custom-style="Nota"}
*Nota.* Criterio de la mayor caída de la suma de cuadrados, con un tope de 10 tramos. Elaboración propia con datos del BCRP.
:::

Con 24 meses, la ventana es más sensible y el criterio da más cortes: con pesos uniformes, en julio de 2008, junio de 2009, noviembre de 2011, octubre de 2020 y marzo de 2024; los dos primeros enmarcan la crisis financiera global. Con 24 meses y pesos gaussianos, el corte cae en junio de 2018. Es la lectura multiescala del EPCA: las ventanas cortas ven los choques breves y las largas, los cambios persistentes, y solo el de 2020 aparece en todas las escalas largas.

**Significado de los ejes en el tiempo.** La Figura {F:aedecorr} muestra la correlación de cada serie con los ejes 1 y 2 en cada ventana, y la Tabla {T:aedetramos} la resume en tres períodos, los tramos del criterio del antecedente, que sirven aquí como períodos de lectura y no como regímenes confirmados.

- **Hasta 2014.** El eje 1 reúne a los créditos, la liquidez, el índice de precios, el PBI y la demanda interna, con correlaciones mayores que 0,8, y a las reservas (0,61). El crédito, el dinero y la actividad crecen juntos.
- **De 2015 a 2020.** El crédito y la liquidez siguen en el eje 1 (0,94 a 0,97), pero el PBI (0,49) y la demanda interna (0,28) se desacoplan: el crédito siguió creciendo mientras la actividad se desaceleraba. El tipo de cambio entra en el eje (de −0,21 a 0,52), en un período en que el sol se depreció de 2,55 soles por dólar a comienzos de 2013 a más de 3,2 desde agosto de 2015.
- **Desde 2020.** El crédito empresarial, M1 y M3 dejan de correlacionarse con el eje 1 (de −0,05 a 0,09), mientras que el crédito hipotecario (0,90), el de consumo (0,62) y el índice de precios (0,88) se mantienen. Esta lectura debe tomarse con cautela: en las ventanas de 2021, el primer y el segundo valor propio son casi iguales (6,20 y 5,79), de modo que los dos ejes no están determinados por separado y lo que parece un cambio del eje 1 puede ser una rotación dentro del plano 1–2.

Hay además un patrón que atraviesa todo el período: la correlación de la tasa de referencia con el eje 1 cambia de signo según la postura monetaria. Es positiva en las ventanas en que el BCRP subía la tasa mientras los saldos crecían —2011 (0,85), 2015–2016 (0,28 y 0,21) y 2021–2022 (0,62 y 0,96)— y negativa en las de recortes o pausa —2009 (−0,68), 2013–2014 (−0,75 y −0,73) y 2017–2019 (−0,88 a −0,97)—. El eje 1 de cada ventana mezcla, por tanto, la tendencia de los saldos con la fase de la política monetaria.

::: {custom-style="Rotulo"}
**Figura {F:aedecorr}**\
*Correlaciones evolutivas de las series con los ejes 1 y 2 del EPCA*
:::

![](fig/camiz_aede_correlaciones.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventana de 48 meses con pesos gaussianos. Línea continua: corte de la tesis; líneas discontinuas: cortes del criterio del antecedente. Elaboración propia con datos del BCRP y la rutina aede del asesor [@camiz_aedeclahfac].
:::

::: {custom-style="Rotulo"}
**Tabla {T:aedetramos}**\
*Correlación media de cada serie con el eje 1 del EPCA en tres períodos*
:::

[[CSV:camiz_aede_corr_tramos.csv]]

::: {custom-style="Nota"}
*Nota.* Promedio, en las ventanas de cada período, de la correlación de la serie con el eje 1. Los períodos son los tramos del criterio del antecedente. Ventana de 48 meses con pesos gaussianos. Elaboración propia con datos del BCRP.
:::

**¿Es el cambio mayor que el azar?** La regla de estabilidad del eje 2 (sección 2.2.6) marca caídas puntuales que dependen del ancho de la ventana (Figura {F:estab}); con 60 meses, las transiciones candidatas son {{epcaTransicionesSesenta}}. Ninguna se confirma: ninguna supera el nulo, y la de octubre de 2017 no aparece con otros anchos ni con pesos gaussianos, por lo que se informa como «transición no confirmada». El nulo de estructura constante se aplicó a {{oeFilasPrincipales}} configuraciones (anchos de 24 a 60 meses, pesos uniformes y gaussianos): en ninguna, la proporción de pares de ventanas «demasiado distintos» supera a la de una estructura constante; el menor *p* es {{oePMin}}. Es decir, series con una correlación fija y la misma autocorrelación que las reales producen cambios entre ventanas tan grandes como los observados. Hay dos lecturas posibles, y con estos datos no se pueden separar: o la estructura de correlación es realmente estable y los regímenes deben buscarse en otro lado, o el contraste tiene poca potencia, porque cada ventana contiene muy poca información independiente. Distinguirlas requiere simular un cambio de tamaño conocido y medir si el nulo lo detecta (recomendación 2).

::: {custom-style="Rotulo"}
**Figura {F:estab}**\
*Estabilidad del eje 2 entre ventanas sucesivas, por ancho de ventana*
:::

![](fig/avance_estabilidad_epca.png){width=95%}

::: {custom-style="Nota"}
*Nota.* Correlación entre las cargas del eje 2 de ventanas separadas por tres meses, con pesos uniformes. La línea naranja es el umbral (media menos una desviación típica); los puntos, las ventanas por debajo de él. Elaboración propia con datos del BCRP.
:::

### 3.1.6 Clasificación factorial jerárquica evolutiva

La HFC se repitió en las {{czClaedeVentanas}} ventanas de 48 meses, con los mismos pesos gaussianos que el EPCA, siguiendo el procedimiento del programa claede del asesor y de @camiz_spada_2024. La Figura {F:claedeidx} muestra la evolución de los índices de los tres nodos superiores y la Figura {F:claededen}, los dendrogramas de cuatro ventanas. Estos resultados provienen de una réplica en Python del procedimiento; su verificación contra el programa original está pendiente.

**Cuán diferenciados están los grupos.** El índice de la raíz mide cuánto se diferencian los dos grandes grupos que une. Hasta 2018 fluctúa entre 1 y 3,6, con mínimos alrededor de 1 en 2011, 2014 y 2017–2018. En las ventanas de 2019 a 2021 sube de forma sostenida, con promedios anuales de 2,9 a 4,0 y un máximo de 4,9 en 2021. Después de la pandemia, los grupos de series están más separados entre sí, lo que concuerda con la caída del primer valor propio del EPCA en el mismo período. El número de clases por encima del corte en 0,7 varía entre {{czClaedeMin}} y {{czClaedeMax}}; el más frecuente es {{czClaedeModa}}, y tres clases aparecen en una proporción {{czClaedeProp3}} de las ventanas.

**Qué series cambian de grupo** (Figura {F:claededen}).

- **Ventana centrada en julio de 2009** (2007–2011): tres clases. Las cuatro tasas, incluida la TAMN, forman un grupo; el tipo de cambio, la bolsa y el EMBIG, otro, y los saldos, precios y actividad, el tercero. En la ventana de la crisis global, el tipo de cambio se mueve con los indicadores de riesgo.
- **Julio de 2014** (2012–2016): solo dos clases. Las tasas de corto plazo quedan aparte y todas las demás series, incluidos el EMBIG y la bolsa, se reúnen en un solo bloque.
- **Julio de 2020** (2018–2022): cuatro clases. El crédito de consumo queda solo; la bolsa y el EMBIG se unen al PBI y a la demanda interna, que comparten la caída de 2020 y la recuperación posterior, y el crédito empresarial queda con la liquidez y el hipotecario.
- **Julio de 2023** (2021–2025): cinco clases. Los créditos quedan con los precios y el tipo de cambio; M1 y las reservas forman un grupo aparte, y la demanda interna queda sola.

La HFC evolutiva confirma, desde otro ángulo, lo que muestra el EPCA: la organización en pocos bloques es la norma hasta mediados de la década de 2010, y en las ventanas que incluyen la pandemia los bloques se fragmentan. Como el EPCA, este resultado todavía no se ha contrastado con un nulo.

::: {custom-style="Rotulo"}
**Figura {F:claedeidx}**\
*Índices de los tres nodos superiores de la HFC evolutiva*
:::

![](fig/camiz_claede_indices.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventana de 48 meses con pesos gaussianos, fechada en el mes central. La línea discontinua marca el corte en 0,7. Réplica del procedimiento del programa claede [@camiz_claede_2025]; verificación pendiente. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura {F:claededen}**\
*Dendrogramas de la HFC evolutiva en cuatro ventanas*
:::

![](fig/camiz_claede_dendrogramas.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventanas de 48 meses con pesos gaussianos, centradas en las fechas indicadas, con la misma escala vertical. Réplica del procedimiento del programa claede [@camiz_claede_2025]. Elaboración propia con datos del BCRP.
:::

### 3.1.7 Datación de regímenes con los *scores* del PCA

La segunda datación no mira la intensidad de la estructura, sino la **posición** del sistema: en qué zona del espacio de las series se encuentra cada mes. Para ello se aplicó la partición de Fisher a los tres primeros *scores* del PCA, suavizados con la media de los 12 meses anteriores. La regla de la tesis da {{datacionKPrincipal}} regímenes, con cortes en {{datacionCortesTexto}} (Figura {F:datacion}); si se permite un número mayor de regímenes, elige {{datacionKQuince}}.

::: {custom-style="Rotulo"}
**Figura {F:datacion}**\
*Scores suavizados, cortes de la datación y episodios de referencia*
:::

![](fig/avance_datacion_pca.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Media móvil de los 12 meses anteriores; en negro, los cortes; en gris, los episodios. Elaboración propia con datos del BCRP.
:::

**Estabilidad.** Cuatro de los cinco cortes se reproducen en más de cuatro de cada cinco réplicas bootstrap; el de {{datacionCorteFrecMinTexto}}, solo en una proporción {{datacionFrecMin}}.

**Sensibilidad al número de ejes.** Con dos ejes, los cortes son enero de 2010, septiembre de 2011, febrero de 2018, agosto de 2020 y septiembre de 2022; con cuatro, abril de 2012, mayo de 2020 y noviembre de 2022. Solo los cortes de mediados de 2020 y de fines de 2022 aparecen con dos, tres y cuatro ejes. El de diciembre de 2008 aparece solo cuando se incluye el eje 3, el del riesgo, lo que a la vez lo interpreta: es el pico del EMBIG de la crisis global.

**Compatibilidad con los episodios y retardo del suavizado.** Con la tolerancia de tres meses, el corte de diciembre de 2008 cae dentro de la crisis global, el de abril de 2014 queda a dos meses del inicio del colapso de las materias primas y el de junio de 2020, a dos meses del fin del episodio de la pandemia. Pero la media móvil causal retrasa los cortes unos cinco meses y medio (sección 2.2.8). Con una media centrada, la datación da cortes entre cinco y seis meses antes: julio de 2008, septiembre de 2009, noviembre de 2013, enero de 2020 y mayo de 2022 (Tabla {T:mediamovil}). Cuatro de los cinco siguen siendo compatibles con algún episodio, pero no siempre con el mismo: el corte de 2014 pasa a noviembre de 2013, dentro del *taper tantrum*, y el de 2020 pasa a enero de 2020, dentro del episodio de la guerra comercial y antes del inicio de la pandemia. La compatibilidad con los episodios es, por tanto, sensible al suavizado, y la asociación de cada corte con un episodio concreto no es unívoca.

::: {custom-style="Rotulo"}
**Tabla {T:mediamovil}**\
*Cortes de la datación con media móvil causal y centrada, y episodio más cercano*
:::

[[CSV:sensibilidad_media_movil_tabla.csv]]

::: {custom-style="Nota"}
*Nota.* Distancia: meses entre el corte y el intervalo del episodio más cercano (0 si cae dentro). La media causal es la especificación principal; la centrada, una sensibilidad. Elaboración propia con datos del BCRP.
:::

**Qué caracteriza a cada régimen.** La Tabla {T:perfil} describe cada régimen con indicadores calculados directamente de las series.

::: {custom-style="Rotulo"}
**Tabla {T:perfil}**\
*Perfil económico de los regímenes obtenidos con los scores del PCA*
:::

[[CSV:perfil_regimenes.csv]]

::: {custom-style="Nota"}
*Nota.* Crédito: suma de los créditos empresarial, de consumo e hipotecario; variación porcentual respecto del mismo mes del año anterior, promediada en el régimen. PBI e IPC (inflación del índice de precios de Lima): igual cálculo. Tasa BCRP: tasa de referencia en el primer y el último mes del régimen. EMBIG: promedio en puntos básicos. Fase: etiqueta de la regla provisional, no válida (véase el texto). Elaboración propia con datos del BCRP.
:::

Leídos así, los seis regímenes describen una secuencia económica coherente:

1. **Auge previo a la crisis (diciembre de 2007 a noviembre de 2008).** El crédito crecía 35 % al año y el PBI 9,4 %, y el BCRP subía la tasa de 5,0 % a 6,5 %.
2. **Crisis y respuesta monetaria (diciembre de 2008 a febrero de 2010).** El EMBIG promedia 294 puntos básicos, el PBI crece 1,9 % y la tasa baja de 6,5 % a 1,25 %. El corte que cierra este régimen, en marzo de 2010, coincide con el fin del período de tasa mínima, que se mantuvo en 1,25 % hasta abril de 2010.
3. **Expansión posterior a la crisis (marzo de 2010 a marzo de 2014).** El crédito crece 17 % al año y el PBI 6,6 %; el riesgo país es bajo (169 puntos básicos) y la tasa sube a 4,0 %.
4. **Desaceleración (abril de 2014 a mayo de 2020).** Tras el fin del auge de las materias primas, el crecimiento del crédito baja a 8 % y el del PBI a 1,7 %, cifra que incluye la caída de la pandemia. La tasa baja de 4,0 % a 0,25 %.
5. **Reactivación y endurecimiento monetario (junio de 2020 a octubre de 2022).** El PBI rebota (6,1 %), la inflación sube a 4,8 % y la tasa pasa de 0,25 % a 7,0 %.
6. **Estancamiento del crédito (noviembre de 2022 a diciembre de 2025).** El crédito crece solo 1,9 % al año, con tasas altas que empiezan a bajar (de 7,25 % a 4,25 %). El corte que lo abre coincide con el inicio de la meseta de tasa máxima, entre 7,25 % y 7,75 %, de noviembre de 2022 a agosto de 2023.

Las coincidencias de los cortes de 2010 y 2022 con la trayectoria de la tasa de referencia son una descripción, no una validación: la tasa es una de las series analizadas, y usarla para fechar episodios sería circular.

**Por qué falla la regla de fases.** La regla provisional (sección 2.2.8) promedia el crédito estandarizado en cada régimen. En niveles, ese promedio refleja la posición en la tendencia: los primeros regímenes quedan por debajo de la media de todo el período y los últimos por encima, sin importar si el crédito acelera o se frena. Los dos primeros regímenes son «transición» por durar menos de 18 meses; el cuarto, porque su promedio (0,17) está entre −0,25 y 0,25. Pero el régimen 3, con un crecimiento del crédito de 17 % anual, recibe la etiqueta de «contracción», y el régimen 6, con un crecimiento de 1,9 %, la de «expansión». La Tabla {T:perfil} muestra que una regla basada en la **tasa de crecimiento** del crédito daría etiquetas con sentido económico. **Las etiquetas actuales no son válidas.**

**Las dos dataciones juntas.** La datación del primer valor propio del EPCA, con el criterio de la tesis, da un solo corte, en mayo de 2020; la de los *scores*, uno en junio de 2020. Son dos métodos que miran cosas distintas —la intensidad de la estructura común y la posición del sistema— y que coinciden en la pandemia. La aparente coincidencia de 2014 solo existe con el criterio del antecedente para el EPCA, que depende de la cota, y sus cortes distan ocho meses; no se toma como coincidencia.

### 3.1.8 Aprendizaje profundo: corrida exploratoria

Los autoencoders y el LSTM-autoencoder se corrieron con una versión anterior del conjunto de datos, que incluía la liquidez M2 (17 series), y quedan por repetir con las {{nSeries}} vigentes. Sus resultados son un antecedente del análisis, no un resultado de la tesis:

- **Reconstrucción** (Figura {F:aecv}). Fuera de muestra, el autoencoder no lineal reconstruye peor que el PCA en todas las dimensiones probadas: su error es 13,6 % mayor con tres dimensiones latentes y 40,7 % mayor con cinco. Con 228 meses y unas diez observaciones efectivas, el modelo ajusta peculiaridades de los meses de entrenamiento que no se repiten fuera de ellos; es lo esperable por la escala de los datos [@tuhin_et_al_2025].
- **Trayectoria** (Figura {F:lstm}). La trayectoria latente del LSTM-autoencoder reproduce la forma general de los ejes 1 y 2 del PCA, con menos variación, y aplana los picos del eje 3: por ahora no muestra una dinámica que el PCA no tenga.
- **Atipicidad** (Figura {F:errrec}). Es el resultado más útil y la razón declarada para usar estos modelos. En la evaluación *walk-forward*, la mediana del error del PCA en los meses de la pandemia es 1,76, frente a 0,26 fuera de los episodios: unas siete veces mayor. Los tres modelos señalan la mitad de los meses de la pandemia y ninguno del *taper tantrum*: el error de reconstrucción detecta los choques grandes, que alteran la relación entre las series, pero no los de menor intensidad.
- **Fases** (Figura {F:fases}). Sobre la trayectoria del LSTM-autoencoder, la regla provisional reproduce el problema descrito en la sección 3.1.7: la variable que define la fase es casi una recta.

::: {custom-style="Rotulo"}
**Figura {F:aecv}**\
*Error de reconstrucción fuera de muestra del PCA y de dos autoencoders, por dimensión latente*
:::

![](fig/17series_08_cv_pca_vs_ae.png){width=60%}

::: {custom-style="Nota"}
*Nota.* Validación por bloques. Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura {F:lstm}**\
*Trayectoria latente del LSTM-autoencoder frente a los scores del PCA*
:::

![](fig/17series_09_trayectoria_latente.png){width=75%}

::: {custom-style="Nota"}
*Nota.* Ventana de 12 meses, rotada hacia el PCA. Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura {F:errrec}**\
*Error de reconstrucción mensual del PCA y del autoencoder no lineal*
:::

![](fig/17series_08_error_reconstruccion.png){width=75%}

::: {custom-style="Nota"}
*Nota.* La banda corresponde al Monte Carlo Dropout. Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura {F:fases}**\
*Regímenes de Fisher y clasificación preliminar de fases sobre la trayectoria del LSTM-autoencoder*
:::

![](fig/17series_09_regimenes.png){width=75%}

::: {custom-style="Nota"}
*Nota.* Corrida exploratoria con 17 series. Elaboración propia con datos del BCRP.
:::

### 3.1.9 Robustez con series transformadas

El análisis principal usa las series en niveles; el anexo de robustez ya calculó dos comparaciones con series transformadas. Tomar logaritmos no cambia la estructura: los tres primeros ejes son prácticamente los mismos que en niveles (congruencias de 0,999, 0,996 y 0,992). Diferenciar, en cambio, la cambia por completo: el primer eje baja a 23,5 % de la inercia, deja de estar correlacionado con el tiempo y su congruencia con el eje en niveles es de solo 0,61. Además, con las series transformadas, el error de reconstrucción del PCA fuera de muestra separa mejor los episodios: con la tolerancia de tres meses, solo el 0,9 % de los meses fuera de los episodios dan falsas alarmas, frente al 59,6 % con las series en niveles. Las series en niveles describen mejor la estructura; las diferenciadas, los choques.


## 3.2 Discusión e interpretación de los resultados

**a) Síntesis de los resultados.** Los resultados responden a tres preguntas: qué estructura tienen las series, si esa estructura cambia en el tiempo y cuándo cambia la posición del sistema.

- *Estructura.* Las 16 series se organizan en tres bloques: la escala del sistema (crédito, liquidez, precios, actividad y reservas), las condiciones monetarias (tasas de corto plazo) y el riesgo de mercado (EMBIG frente a la bolsa). El PCA y la HFC llegan a esa organización por caminos distintos —ejes ortogonales en un caso, agrupación jerárquica en el otro— y ambos la reproducen bajo remuestreo. De los tres ejes, solo el de las tasas supera el nulo de tendencias.
- *Cambio de la estructura.* El EPCA muestra un solo cambio claro de la intensidad de la estructura común, alrededor de mayo de 2020, que aparece con todas las ventanas largas. La HFC evolutiva muestra que, en las ventanas que incluyen la pandemia, los bloques se fragmentan. Sin embargo, el nulo de estructura constante indica que, con la información independiente que contienen las ventanas, las variaciones entre ventanas no se distinguen de las de una estructura fija.
- *Cuándo cambia el sistema.* La datación de los *scores* describe seis regímenes con un perfil económico coherente: auge previo a la crisis, crisis, expansión posterior, desaceleración, reactivación y estancamiento del crédito. De sus cinco cortes, solo el de mediados de 2020 coincide con el del EPCA.

**b) Explicaciones y comparación con otras investigaciones.**

*Por qué tres bloques.* Los bloques reúnen series que responden a fuerzas distintas. Las del primero comparten el crecimiento de la economía y la profundización financiera; las del segundo responden a la política del BCRP, que mueve la tasa de referencia y, con ella, la interbancaria y la pasiva; las del tercero reaccionan a la percepción de riesgo, que eleva el EMBIG y deprime la bolsa al mismo tiempo. La comparación bloque por bloque con @camiz_cerda_atoche_2026, que trabajan con otras series del BCRP entre 1999 y 2020, muestra coincidencias y diferencias:

- *Salud económica y financiera.* Su grupo reúne activos internos, circulante, ahorro, crédito total, fondos de pensiones, liquidez y reservas internacionales netas; el bloque de escala de esta tesis reúne los tres créditos, M1, M3, las reservas internacionales netas, precios y actividad. El contenido es equivalente: agregados monetarios y crediticios que crecen juntos. Una diferencia es que aquí la TAMN entra en este bloque con signo opuesto, porque en niveles su caída secular la alinea con el crecimiento de los saldos.
- *Tasas de interés.* Su grupo reúne las tasas activas y pasivas en moneda nacional y extranjera; el de esta tesis, la tasa de referencia, la interbancaria y la pasiva en soles. Ellos no incluyen la tasa de referencia, y aquí la tasa activa queda fuera del bloque monetario. El núcleo común es el de las tasas de corto plazo y pasivas.
- *Riesgo de mercado.* Su grupo reúne una serie de reservas, distinta de las reservas internacionales netas, el índice bursátil, el EMBIG y la dolarización, y es también un dipolo; aquí el bloque se reduce al EMBIG y la bolsa, también opuestos. En ambos casos es el grupo menos homogéneo.
- *Series aisladas.* Ellos excluyen el tipo de cambio interbancario y el apalancamiento bancario por su baja correlación con el resto. Aquí el tipo de cambio sí se une al bloque de escala, pero es la última serie en hacerlo y una de las peor representadas por el PCA, lo que es coherente con su resultado.

@atoche_murrieta_2022 describe tres componentes equivalentes. Que la organización en tres bloques aparezca con series y períodos distintos sugiere que es un rasgo estable de los indicadores peruanos, aunque la comparación es solo descriptiva, porque ninguno de los dos trabajos contrasta sus grupos con un nulo.

*Por qué la tendencia domina.* En niveles, el bloque de escala recoge el 65 % de la inercia y su eje es casi una recta en el tiempo. El nulo de tendencias confirma la advertencia de @granger_newbold_1974: series independientes, cada una con su propia tendencia, producen un primer eje igual o mayor en cuatro de cada cinco simulaciones. Lo que suele leerse como un componente «de largo plazo» del ciclo financiero es, en estos datos, indistinguible del crecimiento común. En cambio, el eje de las tasas supera el nulo con holgura: la señal más robusta del sistema en niveles es la monetaria. Y al quitar la tendencia aparece un vínculo que en niveles no se ve: los representantes de la escala y de las tasas pasan a tener una correlación de −0,41. Cuando los saldos están por encima de su tendencia, las tasas tienden a estar bajas. Es una relación cíclica entre el bloque financiero y el monetario, que este avance solo describe y que el análisis con series transformadas debe confirmar.

*Por qué el EPCA da un solo corte.* El criterio del antecedente, el máximo del índice de Caliński y Harabasz, da tres tramos con un tope de 10, pero elige siempre el máximo permitido cuando el tope sube, y lo mismo hace bajo el nulo. Ocurre lo que @purizaca_2023 encontró con 21 precios de materias primas: el índice no tiene un máximo interior, y el número de tramos queda en manos del analista. La regla fijada en esta tesis evita esa elección, al precio de detectar solo el cambio mayor. Que ese cambio sea el de 2020, con todas las ventanas de 36 a 60 meses y con los dos esquemas de pesos, lo convierte en el resultado dinámico más sólido del avance. @camiz_cerda_atoche_2026, cuya muestra termina en 2020, asocian sus transiciones a otros episodios —la crisis financiera global, la renuncia de Kuczynski y la guerra comercial—; con la ventana de 24 meses, aquí también aparecen cortes en 2008 y 2009, pero sus fechas no pueden usarse como validación, porque provienen de un análisis similar.

*Por qué los cambios entre ventanas no superan el azar.* Los 228 meses equivalen a unas diez observaciones independientes, y una ventana de 48 meses contiene todavía menos información propia: sus valores propios fluctúan aunque la estructura de fondo no cambie. @camiz_maulucci_roig_2010 advierten la misma tensión entre sensibilidad y estabilidad al elegir el ancho de la ventana. El nulo de estructura constante hace explícito su costo, pero su resultado tiene dos lecturas: o la estructura es estable y los cambios visibles son ruido, o el contraste no tiene potencia para detectar cambios de este tamaño. El corte de 2020, que el EPCA encuentra con cualquier ventana larga, pero que el nulo no distingue del azar, es justamente el caso en que esas dos lecturas se separan; resolverlo requiere medir la potencia con un cambio simulado de tamaño conocido.

*Por qué solo coincide 2020.* La intensidad de la estructura y la posición del sistema son propiedades distintas, y nada obliga a que cambien al mismo tiempo. Los cortes de los *scores* de 2008, 2010, 2014 y 2022 marcan cambios de posición —el sistema pasa de una zona del espacio a otra— sin que la correlación entre las series cambie de forma detectable. El de 2020 es el único en que ambas cosas ocurren a la vez: el sistema cambia de posición y, además, las series dejan de moverse juntas. Es coherente con lo que muestran las propias series: en 2020 y 2021, el crédito a empresas y el dinero crecieron con fuerza mientras el crédito de consumo caía. La explicación por las medidas de la pandemia es plausible, pero todavía no está documentada.

*Por qué el aprendizaje profundo no aporta todavía.* El autoencoder reconstruye peor que el PCA fuera de muestra. Con unas diez observaciones efectivas, el modelo aprende peculiaridades de los meses de entrenamiento que no se repiten; @tuhin_et_al_2025, que trabajan con 5786 días de 375 acciones, advierten sobre la cantidad de datos que estos modelos necesitan. Su aporte más claro es el error de reconstrucción como indicador de atipicidad: detecta la pandemia, un choque que alteró la relación entre las series, pero no el *taper tantrum*, de menor intensidad.

**c) Hallazgos principales.**

1. Los indicadores macrofinancieros peruanos se organizan en tres bloques —escala del sistema, condiciones monetarias y riesgo de mercado—, estables bajo remuestreo y equivalentes a los grupos de los antecedentes.
2. En niveles, el componente que suele asociarse al ciclo financiero de largo plazo no se distingue de la tendencia común; la señal robusta es la de las tasas, y sin tendencia aparece un vínculo cíclico entre tasas y saldos.
3. El EPCA, con la regla fijada de antemano, da un solo cambio de estructura, alrededor de mayo de 2020, que aparece con todas las ventanas largas y coincide con un corte de la datación de los *scores*.
4. La datación de los *scores* describe seis regímenes con un perfil económico coherente, pero sus fechas se mueven unos cinco meses según el tipo de media móvil y dependen del número de ejes.
5. La regla de fases basada en el nivel del crédito no mide el ciclo: el régimen 2010–2014, con un crecimiento del crédito de 17 % anual, recibe la etiqueta de «contracción».

**d) Juicio del autor, limitaciones e implicancias.**

*Juicio del autor.* La tesis se propuso clasificar los regímenes en fases, algo que los antecedentes no hacen. Este avance muestra que esa clasificación no puede apoyarse en el nivel de las series, porque en niveles lo primero que aparece es la tendencia. La posición exploratoria del asesor pide trabajar con las series tal como son, y eso es lo que se hizo; el resultado es que, para hablar de fases, hay que separar explícitamente tendencia y ciclo. Esa separación es una decisión metodológica que debe tomarse con el asesor y antes de calcular, para que no se ajuste a los resultados.

*Limitaciones.*

- La muestra, de 19 años, es corta para el ciclo financiero tal como lo definen @drehmann_borio_tsatsaronis_2012, cuyos ciclos duran entre 8 y 30 años.
- La autocorrelación reduce la información independiente a unas diez observaciones, lo que limita la potencia de todos los contrastes.
- El número de regímenes depende de la regla de selección, del ancho de la ventana y del número de ejes.
- La HFC evolutiva es una réplica en Python del procedimiento del asesor, todavía no verificada contra su programa.
- Los modelos de aprendizaje profundo se corrieron con una versión anterior de los datos.
- El análisis de robustez con series transformadas está solo parcialmente hecho.
- La interpretación del cambio de 2020 como efecto de las medidas de la pandemia es una hipótesis que falta documentar.
- Varias fuentes de los métodos se citan con sus metadatos verificados, pero sin lectura completa del texto (Anexo 3).

*Implicancias.* Si se confirma que en niveles la estructura de correlación solo cambia en 2020, los regímenes del ciclo financiero peruano deberán buscarse sobre todo en la posición del sistema dentro de una estructura estable, no en cambios de esa estructura. Para el seguimiento del sistema financiero, el resultado sugiere vigilar por separado los tres bloques, porque responden a fuerzas distintas; el crédito hipotecario, la tasa interbancaria y el EMBIG son las series que mejor representan a cada uno. Quedan como trabajo futuro la extensión de la muestra a años anteriores a 2007, si la homogeneidad de las series lo permite; la HFC aplicada a cada bloque por separado, como proponen @camiz_cerda_atoche_2026; el orden de los dendrogramas en la HFC evolutiva, y la capacidad de la LSTM para anticipar transiciones.

## 3.3 Contrastación de las hipótesis

La Tabla {T:hipotesis} resume el estado de cada hipótesis con la evidencia disponible. El dictamen es preliminar.

::: {custom-style="Rotulo"}
**Tabla {T:hipotesis}**\
*Estado preliminar de las hipótesis de trabajo*
:::

| Hipótesis | Evidencia disponible | Estado preliminar |
|---|---|---|
| HE1. No estacionariedad estructural | El EPCA da un corte en mayo de 2020 con todas las ventanas largas, y la HFC evolutiva muestra la fragmentación de los bloques en las ventanas de la pandemia; pero ninguna de las {{oeFilasPrincipales}} configuraciones supera el nulo de estructura constante (menor *p* = {{oePMin}}), cuya potencia no se ha medido | Indicios en 2020, sin respaldo estadístico; falta medir la potencia del nulo |
| HE2. Organización en grupos | Tres bloques coincidentes en PCA, HFC y corte del dendrograma en 0,7; partición en tres clases reproducida en una proporción {{hfcPropAriTres}} de las réplicas; equivalencia con los grupos de Camiz et al. (2026) | Respaldada |
| HE3. Correspondencia con episodios | Datación de los *scores*: tres de cinco cortes compatibles (±3 meses), cuatro de cinco con media centrada, pero no siempre con el mismo episodio. EPCA: un corte, compatible con la pandemia. Ambas coinciden solo en 2020 | Respaldada parcialmente |
| HE4. Complementariedad | El autoencoder no mejora la reconstrucción fuera de muestra del PCA; su error de reconstrucción detecta la pandemia, pero no el *taper tantrum* (corrida exploratoria con 17 series) | No respaldada por ahora; falta repetir con {{nSeries}} series |
| Hipótesis general | Combinación de HE1 a HE4 | Abierta |

::: {custom-style="Nota"}
*Nota.* Las hipótesis específicas HE1 a HE4 corresponden a las hipótesis de trabajo HT1 a HT4 de la ficha de inscripción. Elaboración propia.
:::

# CAPÍTULO IV. CONCLUSIONES Y RECOMENDACIONES

Cada conclusión responde a un objetivo específico y va acompañada de su recomendación.

**Conclusión 1 (OE1).** La base de datos reúne {{nSeries}} series mensuales del BCRP entre enero de 2007 y diciembre de 2025, trazables desde su código de origen. Doce son integradas, una es estacionaria alrededor de una tendencia y tres quedan sin clasificar; su fuerte autocorrelación reduce la información independiente de la muestra a unas diez observaciones.

*Recomendación 1.* Evaluar con el asesor si la homogeneidad de las series permite extender la muestra a años anteriores a 2007, porque la longitud de la muestra es la principal limitación de todos los contrastes.

**Conclusión 2 (OE2).** Las series se organizan en tres bloques —escala del sistema, condiciones monetarias y riesgo de mercado— que el PCA y la HFC reproducen por caminos distintos, que son estables bajo remuestreo y que equivalen a los grupos de los antecedentes peruanos. En niveles, el bloque de escala no se distingue de la tendencia común; solo el eje de las tasas supera el nulo. En el tiempo, el EPCA da un solo cambio de estructura, alrededor de mayo de 2020, robusto a las ventanas de 36 a 60 meses y al esquema de pesos, pero no distinguible del azar con el nulo de estructura constante.

*Recomendación 2.* Repetir el PCA y la HFC con las series transformadas, para confirmar que los bloques y el vínculo cíclico entre tasas y saldos no dependen de la tendencia, y medir con datos simulados, con un cambio de tamaño conocido, la potencia del nulo de estructura constante. Verificar la HFC evolutiva contra el programa original del asesor.

**Conclusión 3 (OE3).** En la corrida exploratoria, con una versión anterior de los datos, el autoencoder reconstruye peor que el PCA fuera de muestra, y la trayectoria del LSTM-autoencoder no muestra una dinámica que el PCA no tenga. Su error de reconstrucción sí señala la pandemia como un período atípico.

*Recomendación 3.* Repetir los autoencoders y el LSTM-autoencoder con las {{nSeries}} series vigentes y orientarlos al uso en que muestran ventaja: la detección de períodos atípicos.

**Conclusión 4 (OE4).** La datación de los *scores* describe seis regímenes con un perfil económico coherente, y tres de sus cinco cortes son compatibles con episodios fechados por fuentes independientes. Pero las fechas dependen del suavizado y del número de ejes, solo el corte de 2020 coincide con el del EPCA, y la regla preliminar de fases, basada en el nivel del crédito, no mide el ciclo.

*Recomendación 4.* Definir, antes de calcular y en acuerdo con el asesor, una regla de fases basada en la tasa de crecimiento del crédito o en su desviación respecto de la tendencia, y fijar el criterio del número de tramos y del ancho de ventana. Documentar con fuentes la interpretación del cambio de 2020.

**Conclusión 5 (OE5).** La comparación disponible favorece, por ahora, a los métodos clásicos en interpretabilidad y estabilidad: el PCA y la HFC dan bloques con sentido económico y estables bajo remuestreo, mientras que el autoencoder no mejora la reconstrucción. La comparación en un contexto simulado con regímenes conocidos todavía no se ha hecho.

*Recomendación 5.* Construir el experimento simulado previsto en la ficha de inscripción, con regímenes y cambios de estructura conocidos, que sirve a la vez para comparar los métodos y para medir la potencia de los nulos.

# REFERENCIAS

::: {#refs}
:::

# ANEXOS

## Anexo 1: Matriz de consistencia

::: {custom-style="Rotulo"}
**Tabla {T:matriz}**\
*Matriz de consistencia*
:::

[[MATRIZ]]

## Anexo 2: Estado del avance frente al plan de la ficha de inscripción

::: {custom-style="Rotulo"}
**Tabla {T:avance}**\
*Estado del avance por etapa del plan de trabajo*
:::

| Etapa del plan | Estado al 8 de noviembre de 2026 |
|---|---|
| 1. Revisión bibliográfica | En curso: fuentes de los métodos pendientes de lectura completa en el Anexo 3 |
| 2. Plan de tesis | Ficha de inscripción aprobada; protocolo desarrollado en el Capítulo I |
| 3. Recolección y preprocesamiento | Terminada: {{nSeries}} series, {{nMesesNiveles}} meses, datos congelados |
| 4. Análisis exploratorio multivariado | PCA, HFC y EPCA terminados en niveles; HFC evolutiva replicada, con verificación pendiente; análisis de robustez con series transformadas parcialmente realizado |
| 5. Aprendizaje automático | Corrida exploratoria con 17 series; falta repetirla con {{nSeries}} |
| 6. Evaluación y validación | Datación con el PCA y con el EPCA terminadas; faltan la regla de fases, la datación con el LSTM y el contexto simulado |
| 7. Redacción y difusión | Informe preliminar en curso; artículo pendiente |

::: {custom-style="Nota"}
*Nota.* Elaboración propia.
:::

## Anexo 3: Estado de la revisión bibliográfica

Todas las afirmaciones sobre métodos se apoyan en una fuente. La mayoría de las fuentes se leyó total o parcialmente; @horn_1965 y @fisher_1958 se leyeron completas el 8 de noviembre de 2026. Las siguientes se citan como fuente original del método, con sus metadatos verificados, pero su texto completo todavía no se ha leído: @bartlett_1950, @kaiser_1970, @kaiser_rice_1974, @pyper_peterman_1998, @hubert_arabie_1985, @robert_escoufier_1976, @calinski_harabasz_1974, @kunsch_1989, @gers_schmidhuber_cummins_2000, @gal_ghahramani_2016, @vincent_et_al_2008, @dickey_fuller_1979, @kwiatkowski_et_al_1992 y @newey_west_1987. De @denimal_2007 solo se leyó el resumen, y de @eckart_young_1936, solo parte del contenido. La fórmula del tamaño efectivo de una ventana ponderada se atribuye habitualmente a Kish (1965), cuya obra no se ha consultado ni se incluye en las referencias. La lectura de las fuentes pendientes forma parte del trabajo inmediato, y las fórmulas que se les atribuyen se confirmarán contra el original.
