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

En esta investigación se estudió el ciclo financiero peruano con técnicas exploratorias multivariadas y de aprendizaje automático. Se analizaron {{nSeries}} series mensuales del Banco Central de Reserva del Perú (BCRP), sin transformar, entre {{fechaInicioNiveles}} y {{fechaFinDatos}} ({{nMesesNiveles}} meses): crédito, liquidez, tasas de interés, precios, actividad, reservas, mercado bursátil y riesgo país. La estrategia de análisis encadenó el análisis de componentes principales (PCA), la clasificación factorial jerárquica (HFC), sus versiones evolutivas en ventanas móviles (EPCA y HFC evolutiva, con los programas del asesor) y la partición óptima de Fisher; los autoencoders y las redes LSTM se emplearon como complemento. Cada resultado se contrastó con nulos simulados y con remuestreo por bloques, y los cortes de régimen se compararon con episodios fechados por fuentes independientes de los datos. El PCA y la HFC identificaron tres bloques estables de series: tendencia común, tasas de política y riesgo de mercado; el dendrograma de la HFC, cortado en 0,7, separó esos mismos tres grupos. El primer eje del PCA ({{inerciaPCUnoNiveles}} % de la inercia) correspondió a la tendencia común y no superó un nulo de caminatas aleatorias con deriva; el eje de tasas sí lo superó. El EPCA con ventana gaussiana de 48 meses fechó dos cortes del primer valor propio, en {{czAedeCortesTexto}}, compatibles con el colapso de las materias primas y la pandemia de COVID-19, aunque la variación de la estructura no se distinguió de la de una estructura constante (menor *p* = {{oePMin}}). La datación con los *scores* suavizados del PCA encontró {{datacionKPrincipal}} regímenes, tres de ellos compatibles con episodios externos. En una corrida exploratoria, el autoencoder no mejoró la reconstrucción fuera de muestra del PCA. Se concluyó que la estructura transversal de las series es el resultado más sólido del avance y que la clasificación en fases requiere una regla que no confunda ciclo con tendencia.

**Palabras clave:** ciclo financiero; análisis de componentes principales; clasificación factorial jerárquica; análisis evolutivo; datación de regímenes.

# ABSTRACT

This research studied the Peruvian financial cycle using multivariate exploratory techniques and machine learning. {{nSeriesEn}} untransformed monthly series from the Central Reserve Bank of Peru (BCRP) were analysed from January 2007 to December 2025 ({{nMesesNiveles}} months): credit, liquidity, interest rates, prices, activity, reserves, the stock market and country risk. The analysis strategy chained principal component analysis (PCA), hierarchical factor classification (HFC), their evolutionary versions on moving windows (EPCA and evolutionary HFC, with the advisor's programs) and Fisher's optimal partition; autoencoders and LSTM networks were used as a complement. Each result was tested against simulated null models and block resampling, and regime breaks were compared with episodes dated by sources independent of the data. PCA and HFC identified three stable blocks of series: common trend, policy rates and market risk; the HFC dendrogram, cut at 0.7, separated the same three groups. The first PCA axis ({{inerciaPCUnoNivelesEn}} % of inertia) corresponded to the common trend and did not exceed a null of random walks with drift; the interest-rate axis did. EPCA with a 48-month Gaussian window dated two breaks in the first eigenvalue, in {{czAedeCortesEn}}, compatible with the commodity price collapse and the COVID-19 pandemic, although the variation of the structure could not be distinguished from that of a constant structure (smallest *p* = {{oePMinEn}}). Dating on the smoothed PCA scores found {{datacionKPrincipal}} regimes, three of them compatible with external episodes. In an exploratory run, the autoencoder did not improve on the out-of-sample reconstruction of PCA. It was concluded that the cross-sectional structure of the series is the most solid result so far, and that classifying regimes into phases requires a rule that does not confuse cycle with trend.

**Keywords:** financial cycle; principal component analysis; hierarchical factor classification; evolutionary analysis; regime dating.

# INTRODUCCIÓN

El ciclo financiero describe las fases de expansión y contracción del crédito y de los precios de los activos. A diferencia del ciclo económico, no existe una variable que lo observe directamente: la información está repartida entre muchas series —crédito, liquidez, tasas de interés, precios, mercado bursátil, riesgo país— que se mueven juntas solo en parte y cuya relación puede cambiar en el tiempo. Medirlo exige, por tanto, métodos que resuman muchas series a la vez y que permitan ver si esa síntesis se mantiene o cambia.

Para el Perú, los trabajos más cercanos aplicaron análisis exploratorios multivariados a series del BCRP [@atoche_murrieta_2022; @camiz_cerda_atoche_2026]. Esos trabajos describen la estructura de las series y su evolución, pero no clasifican los períodos en fases del ciclo, no incorporan modelos de aprendizaje profundo y no cubren el período posterior a la pandemia. Esta tesis aborda esos tres puntos: propone una metodología que combina el PCA, la HFC y sus versiones evolutivas con autoencoders y redes LSTM, la aplica a {{nSeries}} series mensuales del BCRP entre 2007 y 2025, y contrasta los regímenes que encuentra con episodios cuya fecha proviene de documentos independientes de los datos.

La investigación es cuantitativa y de nivel exploratorio y descriptivo. Su rasgo metodológico central es que cada resultado se compara con un nulo simulado que reproduce las propiedades que podrían generarlo por azar, en particular la tendencia común de las series, y se somete a remuestreo por bloques de meses para medir su estabilidad. Los métodos exploratorios se aplicaron con los programas del asesor —el paquete AedeClahfac y el programa claede— trasladados a Python con verificación de que reproducen sus resultados.

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
- **OE2.** Analizar la estructura de correlación de las series, sus grupos homogéneos y su estabilidad en el tiempo con PCA, HFC y sus versiones evolutivas.
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
| 2. Estructura global | ¿Qué información común contienen las series? | PCA: valores propios, cargas, cos², contribuciones | Python; réplica con Rcamiz | Kaiser, vara quebrada, análisis paralelo; nulos de tendencia; bootstrap por bloques |
| 3. Grupos de series | ¿En qué bloques homogéneos se organizan? | HFC: jerarquía, índices de nodo, dendrograma | AedeClahfac (clahfac) | Corte en 0,7; bootstrap por bloques |
| 4. Estructura en el tiempo | ¿Cambia la estructura de correlación? | EPCA y HFC evolutiva en ventanas móviles | AedeClahfac (aede) y claede | Nulo de estructura constante; anchos de 24 a 60 meses |
| 5. Datación | ¿Cuándo cambian los regímenes? | Partición óptima de Fisher; índice de Caliński y Harabasz | aede y Python | Frecuencia bajo remuestreo; episodios externos (±3 meses) |
| 6. Representación no lineal | ¿Qué agrega el aprendizaje profundo? | Autoencoder y LSTM-autoencoder | Python | Validación por bloques y *walk-forward* frente al PCA |
| 7. Comparación | ¿Qué método describe mejor los regímenes? | Comparación de interpretabilidad, estabilidad y capacidad descriptiva | Python | Contexto simulado con regímenes conocidos |

::: {custom-style="Nota"}
*Nota.* AedeClahfac y claede son los programas en R del asesor [@camiz_aedeclahfac; @camiz_claede_2025]. Elaboración propia.
:::

### 1.4.5 Técnicas de análisis y procesamiento de datos

El análisis principal usa las series sin transformar, estandarizadas; las series transformadas (logaritmos y diferencias) se reservan para un análisis de robustez. Los métodos de la Tabla {T:estrategia} se desarrollan formalmente en la sección 2.2. El procesamiento se realizó en Python. Las rutinas del asesor se trasladaron a Python línea a línea y se verificó que reproducen los resultados del paquete en R; el análisis completo tiene además una réplica en R. Datos, código y resultados están en un repositorio público (https://github.com/RobertoSam/Tesis-modelamiento-matematico).

# CAPÍTULO II. MARCO TEÓRICO

## 2.1 Antecedentes de la investigación

Los antecedentes se presentan en orden cronológico, del más antiguo al más reciente.

**Camiz, Maulucci y Roig (2010).** @camiz_maulucci_roig_2010 estudian 23 series sincrónicas de anillos de árboles cuya estructura de correlación no es estable en el tiempo. Combinan un PCA global, el análisis Statis dual sobre subtablas de 25 años y el PCA evolutivo en ventanas móviles. El PCA global explica solo el 48 % de la varianza con tres componentes, y el Statis dual identifica años de quiebre en la estructura de correlación. Es el antecedente metodológico del EPCA y lo enmarca como herramienta exploratoria: describe la muestra y no se generaliza a una población.

**Camiz y Roig (2011).** @camiz_roig_2011 aplican el mismo enfoque a nueve cronologías de *Araucaria araucana* en un período común de 492 años. Combinan el PCA con clasificación jerárquica de los años, la HFC sobre las series y el EPCA con ventanas de 25 y 50 años. Sobre la serie del primer valor propio del EPCA aplican la partición óptima de Fisher, que divide el período en cuatro intervalos homogéneos, y analizan cada uno con un PCA propio. Es el precedente directo de la datación de regímenes de la tesis.

**Drehmann, Borio y Tsatsaronis (2012).** @drehmann_borio_tsatsaronis_2012 caracterizan el ciclo financiero de siete economías desarrolladas con datos trimestrales desde 1960, mediante filtros de frecuencia y análisis de puntos de giro. El crédito y los precios inmobiliarios comparten un componente de mediano plazo (8 a 30 años), cuyos picos coinciden con las crisis bancarias de origen doméstico de la muestra; los precios bursátiles se comportan de forma distinta.

**Camiz y Diblasi (2013).** @camiz_diblasi_2013 formalizan el EPCA: un PCA en cada posición de una ventana móvil, con pesos gaussianos que dan más importancia a los meses centrales. Lo aplican a diez acciones de la bolsa de París (2009–2010) y muestran que los valores propios evolutivos y las correlaciones de las series con los primeros ejes permiten distinguir períodos con estructura distinta.

**Camiz y Pillar (2018).** @camiz_pillar_2018 comparan por simulación diez reglas para decidir cuántas componentes principales retener, entre ellas el criterio de Kaiser, la vara quebrada y un procedimiento de bootstrap con permutación. Según su resumen, la generalización de Rencher de la prueba de Bartlett y el bootstrap de Pillar dan los mejores resultados.

**Camiz, Spada, Denimal y Piraino (2020).** @camiz_et_al_2020 exponen la HFC, propuesta por @denimal_2007, que agrupa variables de forma jerárquica y resume cada grupo con un factor, y la comparan con el PCA en cinco cronologías de *Pinus pinea*. Tres de las cinco cronologías comparten una señal común y pueden sintetizarse en una sola; las otras dos deben mantenerse separadas.

**Atoche Murrieta (2022).** @atoche_murrieta_2022 estima el ciclo financiero peruano con 17 series mensuales del BCRP, de 1999 a 2020, mediante PCA, HFC y PCA evolutivo con pesos gaussianos. Según su resumen, identifica tres componentes: una de largo plazo, asociada a la evolución del sistema financiero; otra de mediano plazo, ligada a las tasas activas y pasivas, y una tercera asociada a la volatilidad del mercado financiero.

**Tuhin, Nobi, Rakib y Lee (2025).** @tuhin_et_al_2025 entrenan un LSTM-autoencoder sobre los retornos diarios de 375 acciones del índice S&P 500 entre 2000 y 2022, construyen con los pesos de la capa central redes anuales de influencia entre acciones y muestran que sus propiedades topológicas cambian de forma distintiva en cinco crisis financieras. Advierten que el enfoque requiere muchos datos.

**Camiz, Cerda Hernández y Atoche Murrieta (2026).** En un manuscrito aún no publicado, @camiz_cerda_atoche_2026 aplican PCA, HFC y EPCA a 17 series mensuales del BCRP entre 1999 y 2020. La HFC identifica tres grupos: salud económica y financiera, tasas de interés y riesgo del mercado financiero. Sobre el primer valor propio del EPCA, con ventana gaussiana de 48 meses, fechan transiciones con la partición óptima de Fisher y eligen el número de cortes con el índice de Caliński y Harabasz. Es el antecedente más directo de la tesis.

**Vacío identificado.** Ningún trabajo peruano revisado incorpora autoencoders o redes LSTM, ni clasifica de forma explícita los regímenes en fases, ni cubre el período posterior a 2020.

## 2.2 Bases teóricas

### 2.2.1 El ciclo financiero

El ciclo financiero es el movimiento conjunto, de expansión y contracción, del crédito y de los precios de los activos. @drehmann_borio_tsatsaronis_2012 lo distinguen del ciclo económico por su duración y su relación con las crisis bancarias, y su método requiere series largas. Con los 19 años de datos disponibles no es posible identificar ciclos de 8 a 30 años, de modo que el objeto de estudio no es el ciclo completo, sino los **regímenes** que los datos permiten distinguir.

### 2.2.2 Análisis exploratorio, tendencia y regresión espuria

El análisis exploratorio reorganiza la información de una tabla de datos por orden de importancia, sin imponer hipótesis estadísticas, y puede preceder a cualquier modelización [@camiz_2021_pca]. Por eso el análisis principal usa las series sin transformar. Esta elección tiene un costo: @granger_newbold_1974 mostraron que series con tendencia pueden parecer relacionadas sin estarlo. En niveles, las tendencias comunes pueden dominar la correlación; por ello, cada resultado se contrasta con nulos que reproducen ese efecto (sección 2.2.9).

### 2.2.3 Régimen, fase y validación externa

Un **régimen** es un intervalo de meses contiguos en el que la estructura de las series es relativamente homogénea. Una **fase** es la etiqueta —expansión, contracción o transición— que se asigna a cada régimen después de detectarlo. Los cortes se comparan con episodios cuya fecha proviene de documentos independientes de las series (Tabla {T:episodios}): la bibliografía sirve para identificar los eventos candidatos, pero no para fecharlos. Un corte es compatible con un episodio si dista de él tres meses o menos; seis meses se usan como sensibilidad.

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
*Nota.* La fecha es la del evento o anuncio, no la de su efecto en el Perú. Elaboración propia.
:::

### 2.2.4 Análisis de componentes principales

**Datos y notación.** Sea $X=(x_{tj})$ la tabla de $n$ meses por $p$ series. Cada serie se centra y se reduce: $z_{tj}=(x_{tj}-\bar x_j)/s_j$, con $\bar x_j$ y $s_j$ la media y la desviación típica de la serie $j$; $Z$ es la tabla estandarizada y $R=\tfrac1n Z^\top Z$ la matriz de correlaciones. La **inercia** total de la nube de meses es la suma de las distancias cuadradas a su centro de gravedad; con datos estandarizados vale $\operatorname{tr}R=p$, porque cada serie aporta una unidad [@camiz_2021_pca].

**Ejes, valores propios y componentes.** El PCA busca la sucesión de ejes ortogonales que recogen la mayor parte posible de la inercia. Es la descomposición espectral

$$
R=V\Lambda V^\top,\qquad \Lambda=\operatorname{diag}(\lambda_1,\dots,\lambda_p),\quad \lambda_1\ge\lambda_2\ge\dots\ge\lambda_p\ge0,\quad \sum_{k}\lambda_k=p,
$$

donde la columna $v_k$ de $V$ es el vector propio unitario del eje $k$. Las **componentes principales** (o *scores*) son las coordenadas de los meses en los ejes, $F=ZV$; la componente $k$ tiene varianza $\lambda_k$, y la proporción de inercia del eje es $\tau_k=\lambda_k/p$ [@camiz_2021_pca]. En series de tiempo, las componentes son a su vez series: la primera es un compromiso entre las originales, la segunda describe las desviaciones más importantes respecto de la primera, y así sucesivamente [@camiz_diblasi_2013].

**Cargas, calidad de representación y contribuciones.** La correlación entre la serie $j$ y el eje $k$ (su **carga**) es $c_{jk}=\sqrt{\lambda_k}\,v_{jk}$. Su cuadrado, $\cos^2_{jk}=c_{jk}^2$, es la parte de la inercia de la serie que recoge el eje: la **calidad de representación** de la serie en el eje, que se acumula en un plano o subespacio y suma 1 sobre todos los ejes. La **contribución** de la serie a la formación del eje es $\mathrm{ctr}_{jk}=v_{jk}^2$, que suma 1 sobre las series; un eje al que todas contribuyen por igual (alrededor de $1/p$) resume lo común, y uno dominado por una serie es casi exclusivo de ella [@camiz_2021_pca]. La representación gráfica de las cargas es el **círculo de correlaciones**.

**Número de ejes.** En un marco exploratorio no hay una regla de parada única: se trata de saber si los ejes describen estructura o ruido [@camiz_2021_pca]. Se combinan cuatro criterios:

- *Kaiser–Guttman:* retener los ejes con $\lambda_k>1$, es decir, los que resumen más inercia que una serie. @horn_1965 discute su justificación y señala que, en una muestra finita, los primeros valores propios se inflan por el error muestral.
- *Vara quebrada:* si la inercia se repartiera al azar, el eje $k$ recogería en promedio $b_k=\sum_{i=k}^{p}1/i$ (en la escala de los valores propios); se retienen los ejes con $\lambda_k>b_k$ [@camiz_2021_pca].
- *Análisis paralelo:* se generan muchas tablas de series aleatorias independientes con las mismas $n$ y $p$, se calculan sus valores propios y se retienen los ejes cuyo valor propio supera el de las tablas aleatorias [@horn_1965]. Horn usa el promedio; en la tesis se usa el percentil 95.
- *Rencher–Bartlett:* contrasta si cada valor propio difiere de los siguientes con el estadístico $\chi^2_k=\big(n-\tfrac{2p+11}{6}\big)\big(k\ln\bar\lambda-\sum_{i=k}^{p}\ln\lambda_i\big)$, con $\bar\lambda$ la media de $\lambda_k,\dots,\lambda_p$ [@camiz_2021_pca].

**Adecuación muestral.** La prueba de esfericidad de Bartlett contrasta si $R$ difiere de la identidad [@bartlett_1950; @camiz_2021_pca], con el estadístico

$$
\chi^2=-\Big(n-1-\frac{2p+5}{6}\Big)\ln\lvert R\rvert,\qquad \text{gl}=\frac{p(p-1)}{2}.
$$

La medida de Kaiser, Meyer y Olkin (KMO) compara las correlaciones con las correlaciones parciales $a_{jl}$:

$$
\mathrm{KMO}=\frac{\sum_{j\neq l}r_{jl}^2}{\sum_{j\neq l}r_{jl}^2+\sum_{j\neq l}a_{jl}^2},
$$

y valores cercanos a 1 indican que las series comparten información común [@kaiser_1970; @kaiser_rice_1974]. Como las series son autocorrelacionadas, $n$ meses no equivalen a $n$ observaciones independientes; la prueba de Bartlett se recalcula con el **tamaño efectivo de muestra** $n_{\mathrm{ef}}$, que descuenta la autocorrelación de los pares de series [@pyper_peterman_1998]:

$$
\frac{1}{n_{\mathrm{ef}}}=\frac1n+\frac2n\sum_{h=1}^{J}\rho_{xx}(h)\,\rho_{yy}(h),
$$

con $\rho(h)$ las autocorrelaciones de orden $h$ y $J$ el retardo máximo.

### 2.2.5 Clasificación factorial jerárquica

La HFC clasifica las **series** (no los meses) en una jerarquía en la que cada grupo se resume con un factor [@denimal_2007; @camiz_et_al_2020]. Parte de $p$ clases de una serie y, en cada paso, fusiona las dos clases que mejor se resumen juntas con un solo factor.

**Criterio de fusión.** Cada clase $A$ tiene un factor $f_A$, el primer componente principal de sus series, con varianza $\lambda_A$ (su primer valor propio). Para dos clases $A$ y $B$ con factores correlacionados en $r_{AB}$, se hace el PCA de los dos factores ponderados, cuya matriz de covarianzas es

$$
C_{AB}=\begin{pmatrix}\lambda_A & r_{AB}\sqrt{\lambda_A\lambda_B}\\ r_{AB}\sqrt{\lambda_A\lambda_B} & \lambda_B\end{pmatrix},
\qquad
\mu_{1,2}=\frac{\lambda_A+\lambda_B\pm\sqrt{(\lambda_A-\lambda_B)^2+4r_{AB}^2\lambda_A\lambda_B}}{2}.
$$

El **índice** de la fusión es el segundo valor propio $\mu_2$: la inercia que el nuevo factor deja sin explicar. Se fusionan las dos clases con menor $\mu_2$; el nuevo nodo recibe como factor el primer componente de ese PCA, con varianza $\mu_1$ [@camiz_et_al_2020]. Cada nodo tiene así un plano factorial propio: el primer eje resume lo que sus series tienen en común y el segundo, sus diferencias. Con $p$ series se forman $p-1$ nodos, numerados de $p+1$ a $2p-1$; el último es la raíz.

**Lectura y corte.** El dendrograma dibuja cada nodo a la altura de su índice. La suma de los índices es la inercia que la jerarquía no resume con factores; el resto queda representado por los factores de los nodos. Siguiendo a @camiz_et_al_2020, se cortan los nodos cuyo segundo valor propio supera 0,7: las clases resultantes pueden resumirse con un solo factor.

**Estabilidad.** La partición se recalcula en réplicas por bloques de meses (sección 2.2.9) y se compara con la original mediante el índice de Rand ajustado [@hubert_arabie_1985], que vale 1 cuando las particiones coinciden y alrededor de 0 cuando coinciden al azar.

### 2.2.6 Análisis evolutivo: EPCA y HFC evolutiva

**EPCA.** El PCA describe la correlación entre series en todo el período, sin considerar variaciones locales; en series de tiempo, esas relaciones pueden cambiar [@camiz_diblasi_2013]. El EPCA define una ventana móvil de $w$ meses y realiza un PCA en cada posición [@camiz_maulucci_roig_2010; @camiz_diblasi_2013]. Con ventanas uniformes, dos ventanas sucesivas difieren en solo dos meses, cada uno con peso $1/w$; por eso @camiz_diblasi_2013 proponen pesos gaussianos que dan más importancia a los meses centrales. En la implementación del asesor [@camiz_aedeclahfac], el peso del mes $i=1,\dots,w$ de la ventana es

$$
\omega_i\propto\exp\!\Big[-\tfrac12\Big(\nu\,\frac{i-\bar\imath}{s}\Big)^2\Big],\qquad \bar\imath=\frac{w+1}{2},\quad s=\frac{w-1}{\sqrt2},\quad \sum_i\omega_i=1,
$$

donde $\nu$ fija cuántas desviaciones típicas abarca la ventana ($\nu=0$ da pesos uniformes). En cada ventana se calcula la correlación ponderada

$$
r^{(i)}_{jl}=\frac{\sum_{t}\omega_t\,(x_{tj}-\bar x^{\omega}_j)(x_{tl}-\bar x^{\omega}_l)}{\sqrt{\sum_t\omega_t(x_{tj}-\bar x^{\omega}_j)^2}\sqrt{\sum_t\omega_t(x_{tl}-\bar x^{\omega}_l)^2}},
$$

con medias ponderadas $\bar x^{\omega}_j$, y su descomposición espectral. Como el signo de un vector propio es arbitrario, el programa lo fija para mantener la orientación de una ventana a la siguiente [@camiz_diblasi_2013]. Las salidas son dos series de gráficos: la evolución de los primeros valores propios, cuyos cambios marcan variaciones en la intensidad de la estructura común, y la evolución de las correlaciones de las series con los primeros ejes, cuyos cambios marcan variaciones en su significado [@camiz_diblasi_2013]. La ventana debe tener más meses que series, y cada resultado se fecha en el mes central de la ventana.

**HFC evolutiva.** El programa claede del asesor [@camiz_claede_2025] aplica la HFC completa en cada posición de la ventana móvil y guarda, para cada ventana, la jerarquía, el dendrograma y los valores propios de los nodos. La evolución de los índices de los nodos superiores muestra si los grupos se mantienen —índices bajos y estables— o se reorganizan, y la sucesión de dendrogramas muestra qué series cambian de grupo. En la literatura revisada, la HFC y el EPCA se aplican de forma secuencial [@camiz_roig_2011; @camiz_cerda_atoche_2026]; la HFC evolutiva los integra.

### 2.2.7 Comparación de configuraciones

Para comparar dos configuraciones de las mismas series —por ejemplo, las cargas de dos ventanas o las de una réplica bootstrap y la original— se usan dos coeficientes [@abdi_2010]. El **coeficiente de congruencia** de Tucker es el coseno entre dos vectores de cargas,

$$
\phi(a,b)=\frac{\sum_j a_jb_j}{\sqrt{\sum_j a_j^2\,\sum_j b_j^2}}\in[-1,1].
$$

El **coeficiente RV**, introducido por Escoufier y desarrollado por @robert_escoufier_1976, compara configuraciones completas: para $A$ y $B$ con las mismas filas,

$$
\mathrm{RV}(A,B)=\frac{\operatorname{tr}(AA^\top BB^\top)}{\sqrt{\operatorname{tr}\big((AA^\top)^2\big)\,\operatorname{tr}\big((BB^\top)^2\big)}}\in[0,1].
$$

Es un coseno entre matrices de productos escalares; vale 1 cuando las configuraciones coinciden salvo rotación o dilatación, y es la base de métodos como Statis [@abdi_2010].

### 2.2.8 Partición óptima de Fisher y número de tramos

@fisher_1958 plantea agrupar $K$ elementos con valores $a_i$ y pesos $w_i$ en $G$ grupos que minimicen la suma de cuadrados dentro de los grupos,

$$
D=\sum_{i=1}^{K}w_i\,(a_i-\bar a_{g(i)})^2,
$$

donde $\bar a_{g(i)}$ es la media ponderada del grupo al que pertenece el elemento $i$. Cuando los elementos tienen un orden previo —en una serie de tiempo, el orden de los meses— solo se admiten **particiones contiguas**: es el problema restringido. El lema de suboptimización de Fisher —si cada parte de una partición es óptima, la unión de esas partes es óptima entre las particiones que respetan esa división— permite resolverlo de forma exacta sin enumerar todas las particiones [@fisher_1958]; hoy se implementa por programación dinámica. Fisher también señala que conocer cómo cambia $D$ al aumentar $G$ ayuda a decidir el número de grupos. En la tesis, la partición se aplica a la serie del primer valor propio del EPCA, como en @camiz_roig_2011 y @camiz_cerda_atoche_2026, y a los *scores* suavizados del PCA, extendiendo el criterio a la suma de distancias cuadradas en $\mathbb{R}^d$, con tramos de al menos 12 meses.

**Número de tramos.** Con $B_K$ y $W_K$ las sumas de cuadrados entre y dentro de los $K$ tramos de $n$ puntos, el índice de Caliński y Harabasz es

$$
\mathrm{CH}(K)=\frac{B_K/(K-1)}{W_K/(n-K)},
$$

y se elige el $K$ que lo maximiza [@calinski_harabasz_1974]. El programa aede del asesor usa $K$ en lugar de $K-1$ en el numerador [@camiz_aedeclahfac]; ambas variantes se reportan. Como criterio complementario se examina la caída de $W_K$, en la línea sugerida por @fisher_1958.

### 2.2.9 Nulos de referencia y remuestreo

Un resultado exploratorio se juzga frente a lo que producirían datos sin la estructura que se busca.

- **Nulo de tendencias.** Se simulan $p$ series independientes, cada una como una caminata aleatoria con la deriva estimada de la serie real (o como una tendencia determinista más ruido, según el diagnóstico de cada serie), y se calcula el PCA de cada simulación. La proporción de simulaciones con un primer eje igual o mayor que el observado indica si ese eje puede explicarse por las tendencias, en la línea del argumento de @granger_newbold_1974.
- **Nulo de estructura constante.** Se simulan series con la dependencia temporal de las reales y una correlación fija en todo el período, se aplica el mismo EPCA y se cuenta cuántos pares de ventanas resultan tan distintos como los observados (medido con el coeficiente RV). Si los cambios observados no superan a los simulados, no hay evidencia de que la estructura cambie.
- **Bootstrap por bloques.** Para remuestrear sin destruir la dependencia temporal, se toman bloques de meses consecutivos —con los mismos inicios para todas las series— y se concatenan [@kunsch_1989]. Sobre cada réplica se recalculan el PCA, la HFC y la datación.

### 2.2.10 Autoencoders y redes LSTM

**Autoencoder.** Un codificador $g_\phi:\mathbb{R}^p\to\mathbb{R}^d$ y un decodificador $h_\theta:\mathbb{R}^d\to\mathbb{R}^p$ se entrenan para minimizar el error de reconstrucción

$$
L(\phi,\theta)=\frac1n\sum_t\lVert z_t-h_\theta(g_\phi(z_t))\rVert^2 .
$$

Si ambos son lineales, el óptimo genera el mismo subespacio que el PCA de $d$ ejes [@baldi_hornik_1989]; el PCA es, por tanto, el anclaje lineal de la comparación. Los autoencoders profundos [@hinton_salakhutdinov_2006] y los de eliminación de ruido [@vincent_et_al_2008] introducen no linealidad.

**Redes LSTM.** Una red LSTM procesa una secuencia $z_1,\dots,z_T$ con una celda de memoria $c_t$ regulada por compuertas [@hochreiter_schmidhuber_1997]:

$$
\begin{aligned}
i_t&=\sigma(W_i z_t+U_i h_{t-1}+b_i), & f_t&=\sigma(W_f z_t+U_f h_{t-1}+b_f), & o_t&=\sigma(W_o z_t+U_o h_{t-1}+b_o),\\
\tilde c_t&=\tanh(W_c z_t+U_c h_{t-1}+b_c), & c_t&=f_t\odot c_{t-1}+i_t\odot\tilde c_t, & h_t&=o_t\odot\tanh(c_t),
\end{aligned}
$$

donde $\sigma$ es la función logística y $\odot$ el producto elemento a elemento. La compuerta de olvido $f_t$ es una extensión posterior [@gers_schmidhuber_cummins_2000]. El **LSTM-autoencoder** codifica una ventana de meses consecutivos en un vector latente y la reconstruye [@srivastava_mansimov_salakhutdinov_2015].

**Evaluación.** Los modelos se comparan con el PCA por su error de reconstrucción fuera de muestra, con validación por bloques de meses y *walk-forward* (entrenar hasta un año y evaluar el siguiente). La incertidumbre se estima con Monte Carlo Dropout, que mantiene la desactivación aleatoria de neuronas al predecir y repite la predicción [@gal_ghahramani_2016].

## 2.3 Definición de términos

- **Ciclo financiero:** movimiento conjunto de expansión y contracción del crédito y de los precios de los activos [@drehmann_borio_tsatsaronis_2012].
- **Régimen:** intervalo de meses contiguos en el que la estructura de las series es relativamente homogénea.
- **Fase:** etiqueta (expansión, contracción o transición) asignada a un régimen después de detectarlo.
- **Episodio de referencia:** evento con fecha documentada por una fuente independiente de las series, usado para validar los cortes.
- **Inercia:** suma de las distancias cuadradas de los puntos a su centro de gravedad; con series estandarizadas, es igual al número de series [@camiz_2021_pca].
- **Carga:** correlación entre una serie y un eje del PCA.
- **Calidad de representación (cos²):** parte de la inercia de una serie que recoge un eje o un plano [@camiz_2021_pca].
- **Contribución:** peso de una serie en la formación de un eje [@camiz_2021_pca].
- ***Score*:** coordenada de un mes en un eje del PCA.
- **Clasificación factorial jerárquica (HFC):** clasificación jerárquica de variables en la que cada grupo se resume con un factor [@camiz_et_al_2020].
- **Índice de nodo:** segundo valor propio del PCA que fusiona dos clases en la HFC; mide la inercia que el nuevo factor no explica.
- **Análisis evolutivo de componentes principales (EPCA):** PCA aplicado en ventanas móviles, con pesos uniformes o gaussianos, para observar cómo cambia la estructura de correlación [@camiz_diblasi_2013].
- **HFC evolutiva:** HFC aplicada en cada posición de una ventana móvil [@camiz_claede_2025].
- **Coeficiente RV:** medida, entre 0 y 1, de la similitud entre dos configuraciones de las mismas variables [@abdi_2010].
- **Partición óptima de Fisher:** división de una secuencia ordenada en tramos contiguos que minimiza la suma de cuadrados dentro de los tramos [@fisher_1958].
- **Nulo simulado:** conjunto de series artificiales que reproduce una propiedad de los datos (tendencia, dependencia temporal o estructura constante) y sirve de referencia para juzgar si un resultado podría deberse a ella.
- **Bootstrap por bloques:** remuestreo de bloques de meses consecutivos que conserva la dependencia temporal de las series [@kunsch_1989].
- **Tamaño efectivo de muestra:** número de observaciones independientes equivalente a una muestra autocorrelacionada [@pyper_peterman_1998].
- **Autoencoder:** red neuronal que comprime los datos en un espacio latente de menor dimensión y los reconstruye [@hinton_salakhutdinov_2006].
- **LSTM:** red recurrente con celdas de memoria y compuertas, capaz de modelar dependencia temporal larga [@hochreiter_schmidhuber_1997].

# CAPÍTULO III. DESARROLLO DEL TRABAJO DE INVESTIGACIÓN

## 3.1 Análisis de los datos y resultados

Los resultados corresponden al análisis principal, con las {{nSeries}} series en niveles, y siguen las etapas de la estrategia de análisis (Tabla {T:estrategia}). Los de la HFC, el EPCA y la HFC evolutiva se obtuvieron con los programas del asesor. Su interpretación es preliminar y todavía no se ha discutido con el asesor.

### 3.1.1 Las series analizadas

La Figura {F:series} muestra las {{nSeries}} series en sus unidades originales, con los episodios de referencia sombreados. Casi todas crecen de forma sostenida en el período; las excepciones son las tasas de interés, que siguen el ciclo de la política monetaria, y el EMBIG, que presenta picos en los episodios de tensión.

::: {custom-style="Rotulo"}
**Figura {F:series}**\
*Series analizadas en sus unidades originales*
:::

![](fig/avance_series_niveles.png){width=100%}

::: {custom-style="Nota"}
*Nota.* En gris, los episodios de la Tabla {T:episodios}; la línea discontinua marca el episodio puntual de marzo de 2018. Elaboración propia con datos del BCRP.
:::

### 3.1.2 Estructura de correlación

La correlación entre las series es muy alta en un bloque grande —crédito, liquidez, precios, actividad y reservas— y menor en las tasas y en los indicadores de mercado (Figura {F:corr}). Gran parte de esa correlación proviene de la tendencia común: al quitar a cada serie su tendencia lineal, el bloque se debilita y aparecen relaciones de signo distinto (Figura {F:corrst}).

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

Los tres primeros ejes explican el {{inerciaPCUnoNiveles}} %, el {{inerciaPCDosNiveles}} % y el {{inerciaPCTresNiveles}} % de la inercia. El criterio de Kaiser–Guttman retiene {{kaiserNiveles}} ejes; el análisis paralelo y la vara quebrada, {{hornNiveles}} (Figura {F:sedim}). Se trabaja con tres ejes porque el tercero tiene una lectura clara y es estable bajo remuestreo. La medida KMO es alta ({{kmoGlobalNiveles}}). Sin embargo, por la fuerte autocorrelación de las series, el tamaño efectivo de la muestra es de unas {{nEfMedianaNiveles}} observaciones independientes, y con él el estadístico de Bartlett pasa de {{chiBartlettNiveles}} a {{chiBartlettNefNiveles}} (*p* = {{pBartlettNefNiveles}}).

::: {custom-style="Rotulo"}
**Figura {F:sedim}**\
*Valores propios del PCA frente al análisis paralelo y la vara quebrada*
:::

![](fig/05_pca_sedimentacion.png){width=60%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia con datos del BCRP.
:::

La Tabla {T:cargas} da las cargas y la Figura {F:circulos}, los círculos de correlaciones de los planos 1–2 y 1–3.

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

La Tabla {T:cos2} completa la lectura con la calidad de representación y las contribuciones. El eje 1 recibe contribuciones parecidas, cercanas a 1/16 (6,25 %), de once series: resume lo que tienen en común. El eje 2 es casi exclusivo de las tres tasas, que suman más del 85 % de su formación, y el eje 3 lo forman el EMBIG y la bolsa. El tipo de cambio y el índice de la BVL son las series peor representadas por los tres ejes.

::: {custom-style="Rotulo"}
**Tabla {T:cos2}**\
*Calidad de representación (cos²) y contribuciones de las series a los tres primeros ejes*
:::

[[CSV:camiz_pca_cos2_contrib.csv]]

::: {custom-style="Nota"}
*Nota.* La calidad en el subespacio 1–3 es la suma de los cos² de los tres ejes. Elaboración propia con datos del BCRP.
:::

Con estos elementos, los tres ejes se leen así:

- **Eje 1, tendencia común.** Cargan los saldos, los precios y la actividad, y la TAMN en sentido opuesto ({{cargaTamnPCUno}}). Su coordenada está casi perfectamente correlacionada con el tiempo (*r* = {{rTiempoPCUnoNiveles}}). Series independientes con deriva producen un primer eje igual o mayor en una proporción {{nuloConDerivaPCUno}} de las simulaciones. El eje 1, por tanto, no prueba una estructura cíclica común: refleja que casi todas las series crecen.
- **Eje 2, política monetaria.** Lo definen la tasa de referencia ({{cargaTasaRefPCDos}}), la tasa interbancaria y la TIPMN ({{cargaTipmnPCDos}}). Es el único eje que supera con claridad los nulos (proporción de {{nuloConDerivaPCDos}}).
- **Eje 3, riesgo de mercado.** Opone el EMBIG ({{cargaEmbigPCTres}}) a la bolsa ({{cargaBvlPCTres}}). Sus picos coinciden con la crisis financiera global, el final del colapso de las materias primas y el inicio de la pandemia (Figura {F:scores}), pero no supera el nulo con deriva (proporción de {{nuloConDerivaPCTres}}).

Bajo bootstrap por bloques de 24 meses, el percentil 5 de la congruencia con el eje original es {{congruenciaBootPCUnoNiveles}}, {{congruenciaBootPCDosNiveles}} y {{congruenciaBootPCTresNiveles}} para los ejes 1 a 3, frente a {{congruenciaBootPCCuatroNiveles}} para el cuarto.

::: {custom-style="Rotulo"}
**Figura {F:scores}**\
*Coordenadas de los meses en los tres primeros ejes del PCA*
:::

![](fig/avance_scores_pca.png){width=100%}

::: {custom-style="Nota"}
*Nota.* En gris, los episodios de referencia. Elaboración propia con datos del BCRP.
:::

### 3.1.4 Clasificación factorial jerárquica

La Figura {F:dendro} muestra el dendrograma de la HFC obtenido con el programa clahfac del asesor y la Tabla {T:nodos}, los nodos superiores de la jerarquía. La raíz (nodo 31) une el bloque de las tasas con el resto, con un índice de {{czAlturaRaiz}}; el nodo 30 separa el riesgo de mercado (nodo 29: EMBIG y bolsa) del bloque de tendencia (nodo 28). El corte en 0,7 deja {{czClasesCorte}} clases, que coinciden con los tres ejes del PCA: tendencia o «salud económica» (11 series), tasas (3) y riesgo de mercado (2). Los factores de los nodos resumen el {{czInerciaRepr}} % de la inercia total; el {{czInerciaJer}} % restante es la suma de los índices de la jerarquía.

::: {custom-style="Rotulo"}
**Figura {F:dendro}**\
*Dendrograma de la clasificación factorial jerárquica de las series*
:::

![](fig/camiz_hfc_dendrograma.png){width=92%}

::: {custom-style="Nota"}
*Nota.* La altura de cada nodo es su índice (segundo valor propio); la línea discontinua marca el corte en 0,7. Los números identifican los nodos superiores. Elaboración propia con datos del BCRP y el programa clahfac [@camiz_aedeclahfac].
:::

::: {custom-style="Rotulo"}
**Tabla {T:nodos}**\
*Nodos superiores de la jerarquía de la HFC*
:::

[[CSV:camiz_hfc_nodos.csv]]

::: {custom-style="Nota"}
*Nota.* λ1: varianza del factor del nodo; λ2: índice del nodo; % local λ1: parte de la inercia del nodo que recoge su factor; % global λ2 acum.: suma acumulada de los índices como porcentaje de la inercia total. Elaboración propia con datos del BCRP.
:::

En {{hfcReplicas}} réplicas por bloques, la partición en tres clases se reproduce exactamente en una proporción {{hfcPropAriTres}} de las réplicas, y la de cuatro, en {{hfcPropAriCuatro}}. La mediana de la correlación cofenética entre el dendrograma de cada réplica y el original es {{hfcCofeneticaMediana}}. La Tabla {T:hfc} da la composición de las particiones en tres y cuatro clases; la de cuatro separa el EMBIG y la bolsa.

::: {custom-style="Rotulo"}
**Tabla {T:hfc}**\
*Clases de la HFC en las particiones de tres y cuatro clases*
:::

[[TABLA_HFC]]

::: {custom-style="Nota"}
*Nota.* En negrita, la serie más correlacionada con el factor de su clase. Elaboración propia con datos del BCRP.
:::

### 3.1.5 Análisis evolutivo de componentes principales

**Valores propios evolutivos.** El programa aede del asesor se aplicó con la configuración de @camiz_cerda_atoche_2026: ventana de 48 meses con pesos gaussianos ($\nu=3$). El primer valor propio varía entre {{czLambdaMin}} y {{czLambdaMax}} (Figura {F:aede}); su mínimo, en la ventana centrada en {{czFechaLambdaMin}}, indica la menor intensidad de la estructura común del período. La partición de Fisher del primer valor propio, con el número de tramos que maximiza el índice de Caliński y Harabasz del programa, da {{czAedeK}} tramos, con cortes en {{czAedeCortesTexto}} (Tabla {T:aedepart}). El primero cae dentro del colapso de las materias primas y el segundo, a tres meses del fin del episodio de la pandemia.

::: {custom-style="Rotulo"}
**Figura {F:aede}**\
*Valores propios evolutivos del EPCA y partición de Fisher del primer valor propio*
:::

![](fig/camiz_aede_valores_propios.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventana de 48 meses con pesos gaussianos; cada valor se fecha en el mes central de su ventana. Las líneas negras son los cortes de Fisher; en gris, los episodios de referencia. Elaboración propia con datos del BCRP y el programa aede [@camiz_aedeclahfac].
:::

::: {custom-style="Rotulo"}
**Tabla {T:aedepart}**\
*Partición de Fisher del primer valor propio evolutivo para 1 a 10 tramos*
:::

[[CSV:camiz_aede_particion.csv]]

::: {custom-style="Nota"}
*Nota.* SC intra: suma de cuadrados dentro de los tramos. Caliński-Harabasz: variante del programa aede. Elaboración propia con datos del BCRP.
:::

La elección del número de tramos es frágil: el índice tiene un máximo local en tres tramos, pero vuelve a crecer a partir de ocho. Con otras ventanas, la misma regla da números de tramos muy distintos; con 24 meses y pesos uniformes, el criterio de la mayor caída de la suma de cuadrados da cortes en julio de 2008 y junio de 2009, que enmarcan la crisis financiera global.

**Correlaciones evolutivas.** La Figura {F:aedecorr} muestra la correlación de cada serie con los ejes 1 y 2 en cada ventana. El bloque de tendencia mantiene una correlación alta con el eje 1 hasta la pandemia; después del corte de 2020 la estructura se reorganiza y las tasas pasan a correlacionarse con el eje 1.

::: {custom-style="Rotulo"}
**Figura {F:aedecorr}**\
*Correlaciones evolutivas de las series con los ejes 1 y 2 del EPCA*
:::

![](fig/camiz_aede_correlaciones.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventana de 48 meses con pesos gaussianos; las líneas verticales son los cortes de Fisher. Elaboración propia con datos del BCRP y el programa aede [@camiz_aedeclahfac].
:::

**Estabilidad entre ventanas y nulo.** La estabilidad del eje 2 entre ventanas sucesivas tiene caídas puntuales que dependen del ancho de la ventana (Figura {F:estab}); con 60 meses, las caídas marcan transiciones candidatas en {{epcaTransicionesSesenta}}. El nulo de estructura constante (sección 2.2.9) se aplicó a {{oeFilasPrincipales}} configuraciones principales (anchos de 24 a 60 meses, pesos uniformes y gaussianos): en ninguna el resultado se distingue del nulo, y el menor *p* es {{oePMin}}. Con los datos en niveles, las variaciones de la estructura que muestra el EPCA son compatibles con el ruido muestral de ventanas cortas.

::: {custom-style="Rotulo"}
**Figura {F:estab}**\
*Estabilidad del eje 2 entre ventanas sucesivas, por ancho de ventana*
:::

![](fig/avance_estabilidad_epca.png){width=95%}

::: {custom-style="Nota"}
*Nota.* La línea naranja es el umbral; los puntos, las ventanas por debajo de él. Elaboración propia con datos del BCRP.
:::

### 3.1.6 Clasificación factorial jerárquica evolutiva

Con el programa claede, la HFC se repitió en {{czClaedeVentanas}} ventanas de 48 meses. La Figura {F:claedeidx} muestra la evolución de los índices de los tres nodos superiores y la Figura {F:claededen}, los dendrogramas de cuatro ventanas. El número de clases por encima del corte en 0,7 varía entre {{czClaedeMin}} y {{czClaedeMax}}; el más frecuente es {{czClaedeModa}}, y tres clases aparecen en una proporción {{czClaedeProp3}} de las ventanas. El índice de la raíz crece a partir de 2016: los grupos se diferencian más entre sí. La composición también cambia: en 2014 las tasas forman un grupo aparte, mientras que en 2020 la bolsa se agrupa con la actividad.

::: {custom-style="Rotulo"}
**Figura {F:claedeidx}**\
*Índices de los tres nodos superiores de la HFC evolutiva*
:::

![](fig/camiz_claede_indices.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventana de 48 meses, fechada en el mes central. La línea discontinua marca el corte en 0,7. Elaboración propia con datos del BCRP y el programa claede [@camiz_claede_2025].
:::

::: {custom-style="Rotulo"}
**Figura {F:claededen}**\
*Dendrogramas de la HFC evolutiva en cuatro ventanas*
:::

![](fig/camiz_claede_dendrogramas.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Ventanas de 48 meses centradas en las fechas indicadas, con la misma escala vertical. Elaboración propia con datos del BCRP y el programa claede [@camiz_claede_2025].
:::

### 3.1.7 Datación de regímenes con los *scores* del PCA

La partición de Fisher sobre los tres primeros *scores* suavizados da {{datacionKPrincipal}} regímenes, con cortes en {{datacionCortesTexto}} (Tabla {T:regimenes} y Figura {F:datacion}). Si se permite un número mayor de regímenes, la regla de selección elige {{datacionKQuince}}: el número depende de la cota.

::: {custom-style="Rotulo"}
**Tabla {T:regimenes}**\
*Regímenes obtenidos con los scores del PCA*
:::

[[TABLA_REGIMENES]]

::: {custom-style="Nota"}
*Nota.* El primer régimen empieza en diciembre de 2007 porque la media móvil consume los primeros 11 meses. *Crédito medio:* promedio del crédito estandarizado en el régimen. *Frec. del corte:* proporción de réplicas bootstrap que reproducen el corte inicial con ±3 meses. La etiqueta de fase es preliminar y no válida (véase el texto). Elaboración propia con datos del BCRP.
:::

::: {custom-style="Rotulo"}
**Figura {F:datacion}**\
*Scores suavizados, cortes de la datación y episodios de referencia*
:::

![](fig/avance_datacion_pca.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Media móvil de 12 meses; en negro, los cortes; en gris, los episodios. Elaboración propia con datos del BCRP.
:::

Cuatro de los cinco cortes se reproducen en más de cuatro de cada cinco réplicas; el de {{datacionCorteFrecMinTexto}}, solo en una proporción {{datacionFrecMin}}. Con la tolerancia de tres meses, el corte de diciembre de 2008 cae dentro de la crisis financiera global, el de abril de 2014 queda a dos meses del inicio del colapso de las materias primas y el de junio de 2020, a dos meses del fin del episodio de la pandemia. Los cortes de marzo de 2010 y noviembre de 2022 no tienen un episodio compatible. Las dos dataciones —la del primer valor propio del EPCA y la de los *scores*— coinciden en un corte a mediados de 2020 y en otro entre 2014 y 2015.

La regla preliminar de fases asigna la etiqueta según el promedio del crédito estandarizado en cada régimen. En niveles, ese promedio refleja la posición en la tendencia: los primeros regímenes quedan por debajo de la media y los últimos por encima. Por eso el período 2010–2014, de fuerte crecimiento del crédito, recibe la etiqueta de «contracción». **Las etiquetas de fase no son válidas todavía.**

### 3.1.8 Aprendizaje profundo: corrida exploratoria

Los autoencoders y el LSTM-autoencoder se corrieron con una versión anterior del conjunto de datos, que incluía la liquidez M2 (17 series); con las {{nSeries}} series vigentes quedan por repetir. Sus resultados se muestran como exploración, no como resultado de la tesis:

- Fuera de muestra, el autoencoder no lineal reconstruye peor que el PCA en todas las dimensiones probadas, con o sin preentrenamiento (Figura {F:aecv}).
- La trayectoria latente del LSTM-autoencoder reproduce la forma general de los ejes 1 y 2 del PCA, con menos variación, y aplana los picos del eje 3 (Figura {F:lstm}).
- El error de reconstrucción mensual sube en la crisis financiera global y en la pandemia, y aumenta al final de la muestra (Figura {F:errrec}).
- Sobre la trayectoria del LSTM-autoencoder, la regla preliminar de fases reproduce el problema descrito en 3.1.7: la variable que define la fase es casi una recta (Figura {F:fases}).

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

## 3.2 Discusión e interpretación de los resultados

**Síntesis de los resultados.** El PCA y la HFC coinciden en tres bloques de series —tendencia común, tasas de política y riesgo de mercado— que se reproducen bajo remuestreo; el dendrograma, cortado en 0,7, los separa con claridad. En niveles, la tendencia domina: el primer eje no supera un nulo de series con deriva. El EPCA fecha dos cortes del primer valor propio, en 2014 y 2020, y la HFC evolutiva muestra que los grupos se reorganizan después de 2016, pero esas variaciones no superan el nulo de estructura constante. La datación con los *scores* del PCA encuentra cortes mayormente estables, tres de ellos compatibles con episodios externos. En la corrida exploratoria, el aprendizaje profundo no mejora al PCA.

**Explicaciones y comparación con otras investigaciones.** Los tres bloques se parecen a los grupos que @camiz_cerda_atoche_2026 reportan para series del BCRP entre 1999 y 2020 y a las tres componentes de @atoche_murrieta_2022, aunque el conjunto de series no es idéntico: en ese trabajo el grupo de riesgo incluye, además del índice bursátil y el EMBIG, una serie de reservas y el coeficiente de dolarización, que no forman parte de la muestra de esta tesis. La coincidencia sugiere que la organización transversal de los indicadores peruanos es robusta a la elección de series y de período. La dificultad para separar la dinámica del ruido tiene una explicación directa: con unas {{nEfMedianaNiveles}} observaciones efectivas, las ventanas del EPCA contienen poca información independiente, y en niveles la tendencia común absorbe la mayor parte de la correlación, como anticipan @granger_newbold_1974. Que el autoencoder no supere al PCA es coherente con @baldi_hornik_1989, para quienes el PCA es el óptimo lineal de la reconstrucción, y con la advertencia de @tuhin_et_al_2025 sobre la cantidad de datos que estos modelos requieren.

**Hallazgos principales.** (a) La estructura transversal de las series es el resultado más sólido del avance. (b) Los cortes de 2014 y 2020 aparecen tanto en el EPCA como en la datación con los *scores*, pero, por ahora, como movimientos de la intensidad de la estructura y de la posición de los meses, no como un cambio de estructura que supere el azar. (c) La regla de fases basada en el nivel del crédito no mide el ciclo, sino la posición en la tendencia.

**Juicio del autor.** La clasificación en fases es el punto metodológico más importante, porque es uno de los aportes que la tesis busca respecto de los trabajos previos. La posición exploratoria pide trabajar con las series sin transformar, pero en niveles lo primero que muestran los datos es su tendencia. Separar tendencia y ciclo exige una decisión explícita, tomada antes de calcular y discutida con el asesor.

**Limitaciones.** La muestra es corta para el ciclo financiero tal como lo definen @drehmann_borio_tsatsaronis_2012; la autocorrelación reduce el tamaño efectivo de la muestra; el número de tramos de la datación depende de la regla y de la ventana; los modelos de aprendizaje profundo se corrieron con una versión anterior de los datos; el análisis de robustez con series transformadas está pendiente, y varias fuentes de métodos se citan con sus metadatos verificados, pero sin lectura completa del texto (Anexo 3).

**Implicaciones e investigaciones futuras.** Si se confirma que en niveles la estructura de correlación no cambia más allá del azar, los regímenes del ciclo financiero peruano deberán buscarse en la posición del sistema dentro de una estructura estable, no en cambios de esa estructura. Quedan para trabajo futuro la extensión de la muestra a años anteriores a 2007, si la homogeneidad de las series lo permite, la optimización de la HFC —clases que se modelen con un solo factor— y del orden de los dendrogramas en la HFC evolutiva, y la evaluación de la capacidad del LSTM para anticipar transiciones.

## 3.3 Contrastación de las hipótesis

La Tabla {T:hipotesis} resume el estado de cada hipótesis con la evidencia disponible. El dictamen es preliminar.

::: {custom-style="Rotulo"}
**Tabla {T:hipotesis}**\
*Estado preliminar de las hipótesis de trabajo*
:::

| Hipótesis | Evidencia disponible | Estado preliminar |
|---|---|---|
| HE1. No estacionariedad estructural | El EPCA fecha cortes en 2014 y 2020 y la HFC evolutiva cambia de composición, pero ninguna de las {{oeFilasPrincipales}} configuraciones supera el nulo de estructura constante (menor *p* = {{oePMin}}) | No respaldada en niveles; falta el análisis con series transformadas |
| HE2. Organización en grupos | Tres bloques coincidentes en PCA, HFC global y corte del dendrograma en 0,7; partición en tres clases reproducida en una proporción {{hfcPropAriTres}} de las réplicas | Respaldada parcialmente; falta la comparación bloque por bloque con Camiz et al. (2026) |
| HE3. Correspondencia con episodios | Datación con los *scores*: tres de cinco cortes compatibles (±3 meses). EPCA: dos de dos cortes compatibles. El número de tramos depende de la regla | Respaldada parcialmente |
| HE4. Complementariedad | El autoencoder no mejora la reconstrucción fuera de muestra del PCA (corrida exploratoria con 17 series) | No respaldada por ahora; falta repetir con {{nSeries}} series |
| Hipótesis general | Combinación de HE1 a HE4 | Abierta |

::: {custom-style="Nota"}
*Nota.* Elaboración propia.
:::

# CAPÍTULO IV. CONCLUSIONES Y RECOMENDACIONES

## 4.1 Conclusiones

1. **Las series del BCRP se organizan en tres bloques estables.** PCA y HFC coinciden en tres bloques —tendencia común, tasas de política y riesgo de mercado— que el dendrograma separa con el corte en 0,7, que se reproducen bajo remuestreo por bloques y que se parecen a los reportados por los antecedentes peruanos. Es el resultado más sólido del avance.
2. **En niveles, la tendencia domina y los cambios de estructura no superan el azar.** El primer eje del PCA ({{inerciaPCUnoNiveles}} %) es la tendencia común y no supera el nulo de series con deriva; solo el eje de tasas lo supera con claridad. El EPCA y la HFC evolutiva muestran variaciones —cortes en 2014 y 2020 y reorganización de los grupos después de 2016— que no se distinguen de las de una estructura constante, y la regla preliminar de fases confunde ciclo con tendencia.
3. **La datación es en parte externa, pero depende de la regla y el aprendizaje profundo aún no aporta.** La datación con los *scores* del PCA dio {{datacionKPrincipal}} regímenes, con cuatro de cinco cortes estables y tres compatibles con episodios externos; el EPCA fechó dos cortes compatibles con el colapso de las materias primas y la pandemia. El número de tramos depende de la regla y de la ventana. En la corrida exploratoria, el autoencoder no mejoró la reconstrucción del PCA.

## 4.2 Recomendaciones

1. **(De la conclusión 1)** Comparar bloque por bloque los grupos obtenidos con los de @camiz_cerda_atoche_2026 y repetir el PCA y la HFC con las series transformadas, para confirmar que los bloques no dependen de la tendencia.
2. **(De la conclusión 2)** Definir, antes de calcular y en acuerdo con el asesor, una regla de fases basada en la desviación respecto de la tendencia o en la tasa de crecimiento del crédito, y medir con datos simulados, con un quiebre de tamaño conocido, si el nulo de estructura constante puede detectar los cambios que interesan.
3. **(De la conclusión 3)** Fijar con el asesor el criterio del número de tramos y del ancho de ventana; repetir los autoencoders y el LSTM-autoencoder con las {{nSeries}} series vigentes, y completar la comparación de métodos en el contexto simulado previsto en la ficha de inscripción.

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

| Etapa del plan | Estado al 7 de noviembre de 2026 |
|---|---|
| 1. Revisión bibliográfica | En curso: fuentes de los métodos pendientes de lectura completa en el Anexo 3 |
| 2. Plan de tesis | Ficha de inscripción aprobada; protocolo desarrollado en el Capítulo I |
| 3. Recolección y preprocesamiento | Terminada: {{nSeries}} series, {{nMesesNiveles}} meses, datos congelados |
| 4. Análisis exploratorio multivariado | PCA, HFC, EPCA y HFC evolutiva terminados en niveles; falta el análisis de robustez con series transformadas |
| 5. Aprendizaje automático | Corrida exploratoria con 17 series; falta repetirla con {{nSeries}} |
| 6. Evaluación y validación | Datación con el PCA y con el EPCA terminadas; faltan la regla de fases, la datación con el LSTM y el contexto simulado |
| 7. Redacción y difusión | Informe preliminar en curso; artículo pendiente |

::: {custom-style="Nota"}
*Nota.* Elaboración propia.
:::

## Anexo 3: Estado de la revisión bibliográfica

Todas las afirmaciones sobre métodos se apoyan en una fuente. La mayoría de las fuentes se leyó total o parcialmente. Las siguientes se citan como fuente original del método, con sus metadatos verificados, pero su texto completo todavía no se ha leído: @bartlett_1950, @kaiser_1970, @kaiser_rice_1974, @pyper_peterman_1998, @hubert_arabie_1985, @robert_escoufier_1976, @calinski_harabasz_1974, @kunsch_1989, @denimal_2007 (solo el resumen), @gers_schmidhuber_cummins_2000, @gal_ghahramani_2016 y @vincent_et_al_2008. En el caso de @horn_1965 y @fisher_1958, el texto completo se leyó el 7 de noviembre de 2026. La lectura de las fuentes pendientes forma parte del trabajo inmediato, y las fórmulas que se les atribuyen se confirmarán contra el original.
