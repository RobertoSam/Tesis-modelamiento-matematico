# 3. METODOLOGÍA Y DESARROLLO DEL MODELO

<!-- Borrador del 8-11-2026 para revisión. Decisiones aprobadas por el tesista el 8-11-2026: regla K (D12) para las dos trayectorias, con la caída máxima como sensibilidad; estabilidad de los cortes por remuestreo dentro de cada régimen; cobertura del análisis evolutivo sin ventanas truncadas; sin Monte Carlo Dropout; regla de fases por crecimiento interanual del crédito; terminología «segmentación temporal» en lugar de «datación». -->

## 3.1 Metodología

### 3.1.1 Tipo, nivel y diseño de la investigación

La investigación es cuantitativa, de nivel exploratorio y descriptivo, con un componente comparativo entre métodos. El diseño es no experimental, longitudinal y retrospectivo: se analizan series temporales publicadas, sin manipulación de variables.

### 3.1.2 Datos

**Población y muestra.** La población está formada por los indicadores macrofinancieros mensuales que publica el Banco Central de Reserva del Perú (BCRP). La muestra, seleccionada por criterio, comprende 16 series que representan el crédito, los agregados monetarios, las tasas de interés, los precios, la actividad, el sector externo, el mercado bursátil y el riesgo soberano (Tabla {T:series}), observadas mensualmente de enero de 2007 a diciembre de 2025 ($n=228$ meses). El período inicia en el primer mes en que todas las series están disponibles.

::: {custom-style="Rotulo"}
**Tabla {T:series}**\
*Series analizadas y su código en la base de datos del BCRP*
:::

[[TABLA_SERIES]]

::: {custom-style="Nota"}
*Nota.* TAMN: tasa activa en moneda nacional; TIPMN: tasa pasiva en moneda nacional; BVL: Bolsa de Valores de Lima; EMBIG: diferencial de rendimiento de los bonos soberanos peruanos frente a los del Tesoro de los Estados Unidos. Elaboración propia con datos del BCRP.
:::

**Criterios de selección.** Se excluyeron el crédito total y la liquidez en moneda nacional (M2), casi colineales con los créditos por tipo y con M3, respectivamente: como cada indicador estandarizado aporta una unidad de inercia, su inclusión duplicaría el peso de esa información. El BCRP no publica un índice mensual de precios inmobiliarios, por lo que el componente inmobiliario del ciclo financiero [@drehmann_borio_tsatsaronis_2012] no está representado; es una limitación del estudio. Se incluye el índice bursátil, que Drehmann et al. excluyen de su caracterización, porque el enfoque exploratorio deja que la estructura de los datos indique si su comportamiento difiere del resto.

**Recolección y verificación.** Las series se descargaron de la base de datos estadística del BCRP mediante su código, se verificaron en unidades, frecuencia, cobertura y continuidad, y se congelaron antes de cualquier cálculo, de modo que los resultados no dependen de revisiones posteriores de la fuente. El análisis principal emplea las series en niveles, por la razón expuesta en la sección 2.2.2; las series en logaritmos y en primeras diferencias se emplean como control de robustez.

**Operacionalización.** La Tabla {T:operacional} relaciona cada objetivo específico con lo que se mide y con sus indicadores.

::: {custom-style="Rotulo"}
**Tabla {T:operacional}**\
*Operacionalización: dimensiones e indicadores por objetivo específico*
:::

| Objetivo | Dimensión | Indicadores |
|---|---|---|
| OE1 | Estructura factorial global | Valores propios e inercia; cargas, calidad de representación y contribuciones; clases e índices de la HFC |
| OE2 | Evolución de la estructura | Valores propios evolutivos; correlaciones evolutivas; índices y composición de los grupos por ventana |
| OE3 | Regímenes | Cortes; suma de cuadrados por número de tramos; proporción $\hat p$ frente a series de referencia simuladas; frecuencia de cada corte en el remuestreo |
| OE4 | Caracterización | Crecimiento del crédito, actividad, inflación, tasa de referencia y riesgo soberano por régimen; fase; distancia de cada corte al episodio más cercano |
| OE5 | Comparación de representaciones | Error de reconstrucción fuera de muestra; coeficiente RV entre representaciones de distintas semillas; partición resultante |

::: {custom-style="Nota"}
*Nota.* Elaboración propia.
:::

### 3.1.3 Episodios documentados

Los cortes se comparan con seis episodios cuya fecha proviene de documentos externos a las series (Tabla {T:episodios}). Los episodios no se fechan con las series ni con indicadores derivados de ellas, para que la comparación no sea circular; la fecha corresponde al evento externo y no a su efecto en la economía peruana. Un corte es compatible con un episodio si dista de él tres meses o menos; seis meses se emplean como sensibilidad. Como los episodios son pocos y algunos están próximos entre sí, la comparación es descriptiva.

::: {custom-style="Rotulo"}
**Tabla {T:episodios}**\
*Episodios documentados y fuentes de sus fechas*
:::

| Episodio | Inicio | Fin | Fuente del inicio | Fuente del fin |
|---|---|---|---|---|
| Crisis financiera global | 2008-09 | 2009-06 | @lehman_brothers_2008 | @nber_2010 |
| *Taper tantrum* | 2013-05 | 2013-12 | @bernanke_2013 | @reserva_federal_2013 |
| Colapso de los precios de las materias primas | 2014-06 | 2016-01 | @stocker_et_al_2015 | @fmi_2016 |
| Renuncia presidencial de 2018 (Kuczynski) | 2018-03 | Puntual | @congreso_2018 | — |
| Guerra comercial entre Estados Unidos y China | 2018-06 | 2020-01 | @ustr_2018 | @ustr_2020 |
| Pandemia de COVID-19 | 2020-03 | 2020-04 | @oms_2020b | @nber_2021 |

::: {custom-style="Nota"}
*Nota.* La crisis global va de la quiebra de Lehman Brothers al valle de la recesión estadounidense fijado por el NBER; el *taper tantrum*, del testimonio del presidente de la Reserva Federal ante el Congreso al comunicado que redujo las compras de activos; el colapso de las materias primas, de la caída del precio del petróleo al primer repunte de los precios informado por el FMI; la pandemia, de la declaración de la OMS al valle de la actividad estadounidense fijado por el NBER. Elaboración propia.
:::

### 3.1.4 Estrategia de análisis

El análisis avanza de la estructura global a su evolución y de esta a los regímenes, y cada etapa responde a un objetivo específico (Figura {F:esquema}): (1) la representación global de los indicadores mediante PCA y HFC (OE1); (2) su evolución mediante EPCA y HFC evolutiva (OE2); (3) la segmentación temporal de dos trayectorias mediante la partición de Fisher, con su validación (OE3); (4) la caracterización de los regímenes y su comparación con los episodios (OE4), y (5) la comparación de la representación lineal con las no lineales (OE5).

::: {custom-style="Rotulo"}
**Figura {F:esquema}**\
*Esquema del modelo: etapas, trayectorias y validación*
:::

![](fig/c3_esquema_modelo.png){width=100%}

::: {custom-style="Nota"}
*Nota.* Elaboración propia.
:::

### 3.1.5 Implementación computacional

El procesamiento se realizó en R y en Python, con verificación de que ambos producen resultados idénticos hasta el error de redondeo. Los métodos factoriales se calcularon con las rutinas de referencia de @camiz_aedeclahfac —clahfac para la HFC y aede para el análisis evolutivo y la partición de Fisher—; el procedimiento de la HFC evolutiva sigue el programa claede [@camiz_claede_2025]. Las simulaciones y los remuestreos emplean semillas fijas. Los datos, el código y los resultados se publican en un repositorio de acceso público (https://github.com/RobertoSam/Tesis-modelamiento-matematico).

## 3.2 Desarrollo del modelo matemático y computacional

### 3.2.1 Formulación del problema

Sea $X\in\mathbb{R}^{n\times p}$ la matriz de los $p=16$ indicadores observados en $n=228$ meses, y $Z$ su versión estandarizada. El modelo tiene dos componentes:

1. **Representación.** Una aplicación $f:\mathbb{R}^p\to\mathbb{R}^d$, con $d\ll p$, que asigna a cada mes $\mathbf z_t$ una representación $f(\mathbf z_t)$ que conserva la información común de los indicadores y es interpretable en términos de ellos. En el caso lineal, $f(\mathbf z)=V_d^\top\mathbf z$ (PCA); en el no lineal, $f$ es el codificador de un autoencoder.
2. **Segmentación temporal.** Dada una trayectoria $\mathbf y_1,\dots,\mathbf y_n$ derivada de la representación, una partición del índice temporal en $K$ intervalos contiguos $I_1,\dots,I_K$ que minimiza la suma de cuadrados dentro de los intervalos, $\mathrm{SCD}_K$, para un $K$ elegido con una regla fijada de antemano.

Cada intervalo $I_k$ es un régimen. Se segmentan dos trayectorias, que corresponden a las dos componentes de la definición de régimen (sección 2.2.1):

- la **trayectoria de estructura**, $y_t=\lambda_1(t)$, primer valor propio del EPCA en la ventana centrada en $t$, que mide la intensidad de la asociación común;
- la **trayectoria de posición**, $\mathbf y_t=(F_{t1},F_{t2},F_{t3})$, coordenadas del mes $t$ en los tres primeros ejes del PCA global, que miden el nivel conjunto de los indicadores.

### 3.2.2 Representación global

**PCA.** Se aplica a la matriz de correlaciones de las 16 series en niveles. Se informan los valores propios y su proporción de inercia simple y acumulada; las cargas, la calidad de representación y la contribución de cada serie a cada eje; las coordenadas de los meses; los círculos de correlaciones en los planos 1–2 y 1–3, y, como diagnósticos de adecuación, la medida de Kaiser, Meyer y Olkin (KMO), global y por serie, y la prueba de esfericidad de Bartlett, calculada con $n$ y con el tamaño efectivo $n_{\mathrm{ef}}$ (sección 2.2.2). El número de ejes interpretados se fija en $d=3$; los criterios de Kaiser, vara quebrada y análisis paralelo se informan —este último con el percentil 95 de los valores propios de 1000 tablas simuladas, una variante más conservadora que la media empleada por @horn_1965—, y $d=2$ y $d=4$ se emplean como sensibilidad en la segmentación.

**HFC.** Se aplica a las mismas series. Se informan los nodos de la jerarquía con su índice, la varianza de su representante y la proporción de inercia local y acumulada; el dendrograma; la partición por el corte en 0,7, y la correlación de cada serie con el representante de su clase.

### 3.2.3 Representación evolutiva

**Ventana y pesos.** El análisis principal emplea ventanas de $w=48$ meses con pesos gaussianos de parámetro $\nu=3$, la especificación de @camiz_cerda_atoche_2026, para que los resultados sean comparables con el antecedente; el tamaño efectivo de la ventana es $n_\omega\approx 37$ meses. Como lectura multiescala se emplean los anchos de 24, 36 y 60 meses, con pesos uniformes y gaussianos. Con $w=48$ se obtienen 181 ventanas cuyos centros van de enero de 2009 a enero de 2024; los regímenes de estructura se identifican solo en ese intervalo, y no se emplean ventanas truncadas en los extremos.

**EPCA.** En cada ventana se calculan los tres primeros valores propios y las correlaciones de las 16 series con los dos primeros ejes. Cada valor propio se compara con el umbral de Kaiser y con el del análisis paralelo calculado con el tamaño efectivo de la ventana, para identificar cuántos ejes superan el ruido en cada período.

**HFC evolutiva.** En cada ventana se calcula la jerarquía completa con los mismos pesos. Se informan los índices de los tres nodos superiores, el número de clases que deja el corte en 0,7 y la composición de las clases en ventanas seleccionadas.

### 3.2.4 Segmentación temporal

**Trayectorias.** La trayectoria de estructura es $\lambda_1(t)$ con $w=48$ y $\nu=3$. La trayectoria de posición son las coordenadas de los tres primeros ejes del PCA global, suavizadas con la media móvil de los 12 meses anteriores para eliminar la variación mensual; como la media solo usa meses pasados, un cambio ocurrido en el mes $\tau$ se incorpora gradualmente entre $\tau$ y $\tau+11$, con un retardo medio de 5,5 meses. Las coordenadas se estandarizan antes de la partición, para que cada eje pese lo mismo en la norma euclídea (sección 2.2.6).

**Partición y número de tramos.** Cada trayectoria se particiona con el algoritmo de @fisher_1958 para $K=1,\dots,10$, con tramos de al menos 12 meses. El número de tramos se elige con una regla registrada antes de calcular:

$$
K^*=\min\Big\{K:\ \frac{\mathrm{SCD}_K-\mathrm{SCD}_{K+1}}{\mathrm{SCD}_K}<0{,}10\Big\},
$$

es decir, el menor número de tramos a partir del cual un tramo adicional reduce la suma de cuadrados en menos de 10 %; si ningún $K$ cumple la condición, se elige el de mayor caída. El índice de @calinski_harabasz_1974 se informa, pero no se usa para elegir $K$, porque en trayectorias suaves y dependientes puede no presentar un máximo interior y carece de distribución de referencia (sección 2.2.6).

**Sensibilidad.** Se informan los cortes con: la regla de la mayor caída de $\mathrm{SCD}_K$; $d=2$ y $d=4$ ejes en la trayectoria de posición; una media móvil centrada en lugar de la causal, y los anchos de ventana de 24, 36 y 60 meses en la trayectoria de estructura.

### 3.2.5 Validación

**Series de referencia con tendencia.** Para evaluar si los ejes del PCA reflejan asociación entre las series o solo su crecimiento, se generan 1000 conjuntos de 16 series independientes entre sí, cada una con el tipo de tendencia de la serie observada (sección 2.2.2): las series TS, como su recta de tendencia más sus residuos remuestreados; las DS con deriva significativa ($\lvert t\rvert>2$), como caminatas aleatorias con su deriva, y las demás DS, como caminatas sin deriva. Las series de tipo indeterminado se simulan de las dos formas, y se informan ambos resultados. El estadístico es la proporción de inercia de cada uno de los tres primeros ejes, y se informa $\hat p$ para cada uno.

**Series de referencia con estructura constante.** Para evaluar si la estructura de asociación cambia más de lo que cambiaría por azar, se generan 200 conjuntos de series por remuestreo conjunto de bloques de los incrementos mensuales, con los mismos inicios de bloque para todas las series, y se acumulan desde el valor inicial: las series conservan la correlación contemporánea y la dinámica de corto plazo, pero cualquier cambio de estructura queda dispersado en el tiempo. En cada conjunto se calcula el coeficiente RV entre las cargas de ventanas adyacentes que no comparten meses, y se compara el perfil observado con el simulado, para cada ancho y esquema de pesos.

**Estabilidad de la estructura global.** Se evalúa con 500 réplicas de bootstrap por bloques móviles de $\ell=24$ meses, con 12 y 36 meses como sensibilidad: para el PCA, la congruencia de cada eje con el original y la distribución de los valores propios; para la HFC, la frecuencia con que se reproduce la partición, medida con el índice de Rand ajustado, y la correlación cofenética entre dendrogramas.

**Estabilidad de los cortes.** Como el bootstrap por bloques no conserva la ubicación cronológica (sección 2.2.7), la estabilidad de los cortes se evalúa remuestreando **dentro de cada régimen**: en cada réplica, cada régimen se reconstruye con bloques de seis meses consecutivos tomados de ese mismo régimen, de modo que los cortes conservan su posición. Se repite la partición con el mismo $K^*$ y se informa, para cada corte, la proporción de las 200 réplicas en que aparece un corte a tres meses o menos.

**Correspondencia con los episodios.** Para cada corte se informa la distancia, en meses, al episodio más cercano y si es compatible con él (sección 3.1.3).

### 3.2.6 Caracterización de los regímenes y regla de fases

Cada régimen se caracteriza con indicadores calculados directamente de las series: el crecimiento interanual promedio del crédito, del PBI y del índice de precios, la tasa de referencia al inicio y al final del régimen, y el promedio del EMBIG.

La fase se asigna con una regla basada en el crecimiento interanual del crédito total $C_t$, suma de los créditos empresarial, de consumo e hipotecario:

$$
g_t=100\Big(\frac{C_t}{C_{t-12}}-1\Big).
$$

La diferencia interanual conserva las oscilaciones de baja frecuencia y elimina la estacionalidad (sección 2.2.2). Sean $m$ la mediana y $s$ la desviación estándar de $g_t$ en todo el período, y $\tilde g_k$ la mediana de $g_t$ en el régimen $k$. La fase del régimen es:

$$
\text{fase}_k=\begin{cases}
\text{expansión} & \text{si } \tilde g_k>m+s,\\
\text{contracción} & \text{si } \tilde g_k<m-s,\\
\text{transición} & \text{en otro caso.}
\end{cases}
$$

La mediana hace que la fase refleje el comportamiento predominante del régimen aunque contenga meses atípicos. La fase es una etiqueta de referencia univariada sobre regímenes delimitados con información multivariada.

### 3.2.7 Representaciones no lineales

**Autoencoder.** Codificador y decodificador con una capa oculta de 8 neuronas y activación tangente hiperbólica, pesos compartidos entre codificador y decodificador, y $d=3$ dimensiones latentes, como en el PCA. Se entrena con el método de Adam, con penalización de los pesos, ruido en la entrada (variante con eliminación de ruido) y detención temprana sobre un conjunto de validación.

**Autoencoder LSTM.** Codificador y decodificador LSTM con 16 unidades ocultas y $d=3$ dimensiones latentes, aplicados a ventanas de $q=12$ meses; cada vector latente se asigna al último mes de su ventana, de modo que la representación no usa información posterior.

**Evaluación.** Ambos modelos se comparan con el PCA de la misma dimensión mediante el error de reconstrucción fuera de muestra, con dos esquemas cronológicos: validación por cinco bloques contiguos, para $d=1,\dots,5$, y evaluación anual sucesiva (*walk-forward*), en la que el modelo se entrena con los meses anteriores a cada año y se evalúa en ese año, de 2011 a 2025. La estabilidad de la representación se mide con el coeficiente RV entre las representaciones latentes obtenidas con distintas semillas. La trayectoria latente se segmenta con el mismo procedimiento de la sección 3.2.4.
