# 1. INTRODUCCIÓN

<!-- Texto aprobado por el tesista el 8-11-2026, bloque por bloque, con las correcciones del asesor-agente. Pendiente: verificar la HFC evolutiva (OE2). Pendiente: verificar en Atoche Murrieta (2022) y Camiz et al. (2026) que la partición no se contrasta con series de referencia simuladas ni con remuestreo. -->

## 1.1 Planteamiento y descripción del problema

El ciclo financiero se ha caracterizado como la alternancia de fases de expansión y contracción del crédito y de los precios de los activos; su duración excede la del ciclo económico y sus puntos máximos tienden a coincidir con crisis bancarias [@borio_2014]. En el Perú, los ciclos crediticios no presentan una correlación dinámica fuerte con el ciclo del producto, por lo que una medida macroprudencial basada en este último podría tener una efectividad limitada para atenuar el sobrecalentamiento del crédito [@alcaraz_cabello_nivin_2024]. La fase del ciclo financiero no puede, en consecuencia, inferirse del ciclo del producto, y su identificación requiere incorporar información del sistema financiero junto con la de la actividad y los precios.

En esta investigación, un **régimen financiero** es un intervalo de tiempo contiguo en el que la estructura de asociación entre los indicadores macrofinancieros (régimen de estructura) o su nivel conjunto (régimen de posición) permanece relativamente estable. Como el período de estudio es menor que la duración reportada del ciclo, los regímenes se entienden como subperíodos del ciclo y no como ciclos completos. Un régimen no es directamente observable. Se manifiesta de forma parcial en indicadores de crédito, agregados monetarios, tasas de interés, precios, actividad, reservas internacionales, mercado bursátil y riesgo soberano. Entre ellos hay información redundante y señales divergentes, sus movimientos no son necesariamente sincrónicos y su estructura de asociación puede variar en el tiempo. Cada régimen puede asociarse, además, a una fase del ciclo financiero (expansión, contracción o transición) según el comportamiento del crédito durante el intervalo.

La multiplicidad de indicadores plantea así tres dificultades de modelización: resumir la información común en pocas dimensiones sin imponer de antemano ponderaciones ni agrupaciones de los indicadores; seguir la evolución de esa representación, porque una estimación sobre el período completo puede ocultar sus cambios, y segmentar el período con un criterio explícito cuyos cortes puedan contrastarse con los que producirían la dependencia temporal de las series y la variabilidad muestral. A ello se suma que las relaciones entre los indicadores pueden no ser lineales, lo que plantea si una representación no lineal recoge información que la lineal no capta.

En el Perú, los estudios identificados que aplican métodos de reducción de dimensión a indicadores del BCRP cubren el período hasta 2020 [@atoche_murrieta_2022; @camiz_cerda_atoche_2026]. En ellos, el número de cortes se elige con el índice de Caliński y Harabasz, pero la partición resultante no se contrasta con series de referencia simuladas ni se evalúa su estabilidad ante remuestreo, y no se examinan representaciones no lineales.

### 1.1.1 Problema general

¿Cómo construir un modelo matemático-computacional de reducción de dimensión de los indicadores macrofinancieros mensuales del Perú observados en el período 2007–2025, que identifique los regímenes del ciclo financiero mediante un criterio de segmentación explícito y validado estadísticamente, y que permita interpretarlos en términos de los indicadores originales?

### 1.1.2 Problemas específicos

- **PE1.** ¿Qué estructura factorial (componentes principales y clasificación factorial jerárquica de los indicadores) resume su información común en el período 2007–2025?
- **PE2.** ¿Cómo evoluciona esa estructura factorial a lo largo del período?
- **PE3.** ¿Qué partición del período en regímenes se deriva de esa evolución mediante un criterio explícito de segmentación, contrastado con series de referencia simuladas y evaluado por remuestreo?
- **PE4.** ¿Cómo se caracteriza cada régimen en términos de los indicadores originales, de la fase del ciclo financiero a la que corresponde y de los episodios económicos documentados?
- **PE5.** ¿En qué medida las representaciones no lineales (autoencoder y autoencoder LSTM) difieren de la lineal en error de reconstrucción fuera de muestra, estabilidad de la representación y partición en regímenes resultante?

## 1.2 Justificación

*Justificación matemática y computacional.* Los antecedentes en el Perú representan los indicadores macrofinancieros mediante análisis en componentes principales, clasificación factorial jerárquica y sus versiones evolutivas, pero no contrastan la partición en regímenes con series de referencia simuladas ni examinan representaciones no lineales [@atoche_murrieta_2022; @camiz_cerda_atoche_2026]. La investigación aborda esas brechas con un modelo compuesto por etapas articuladas: (1) una representación de baja dimensión de los indicadores y su extensión evolutiva en ventanas móviles con pesos gaussianos; (2) la delimitación de regímenes mediante la partición de Fisher, óptima en intervalos contiguos respecto de la dispersión intragrupo para un número dado de regímenes; (3) un procedimiento de validación por contraste con series de referencia simuladas, que compara la partición obtenida con la que el mismo método produciría en series sin cambio de estructura pero con la misma estructura de autocorrelación, y que evalúa su estabilidad mediante remuestreo por bloques, y (4) la comparación de la representación lineal con representaciones no lineales (autoencoder y autoencoder LSTM) bajo un mismo criterio de error fuera de muestra, para valorar el aporte de la no linealidad en series con dependencia temporal y relativamente cortas para modelos neuronales. El procedimiento de validación y la comparación controlada son transferibles a otras aplicaciones del análisis factorial evolutivo. La implementación en Python de los métodos factoriales se contrasta con las rutinas de referencia en R del paquete AedeClahfac, de S. Camiz, y se publica, junto con los datos, en un repositorio de acceso público.

*Justificación práctica.* @alcaraz_cabello_nivin_2024 muestran que en el Perú los ciclos crediticios no presentan una correlación dinámica fuerte con el ciclo del PBI; su medición es, sin embargo, univariada. La investigación busca delimitar, para el período 2007–2025, una cronología de regímenes basada en la estructura conjunta de indicadores de crédito, agregados monetarios, tasas de interés, precios, actividad, sector externo, mercado bursátil y riesgo soberano, contrastada con episodios económicos documentados. Esa cronología complementa la medición univariada del ciclo crediticio y es una referencia retrospectiva para el análisis de la estabilidad financiera.

*Línea de investigación.* La investigación se inscribe en la línea de Probabilidad y estadística del programa, sublínea Ciencia de datos, y en el área de aprendizaje automatizado, en su vertiente no supervisada.

## 1.3 Objetivos

### 1.3.1 Objetivo general

Construir un modelo matemático-computacional de reducción de dimensión de los indicadores macrofinancieros mensuales del Perú observados en el período 2007–2025, que identifique los regímenes del ciclo financiero mediante un criterio de segmentación explícito y validado estadísticamente, y que permita interpretarlos en términos de los indicadores originales.

### 1.3.2 Objetivos específicos

- **OE1.** Determinar la estructura factorial (componentes principales y clasificación factorial jerárquica) que resume la información común de los indicadores en el período 2007–2025.
- **OE2.** Caracterizar la evolución temporal de esa estructura mediante el análisis en componentes principales evolutivo y la clasificación factorial jerárquica evolutiva.
- **OE3.** Delimitar los regímenes mediante la partición de Fisher, con un criterio explícito para el número de regímenes y con validación de la partición por contraste con series de referencia simuladas y por remuestreo por bloques.
- **OE4.** Caracterizar cada régimen en términos de los indicadores originales, de la fase del ciclo financiero (expansión, contracción o transición, según el criterio basado en el crecimiento del crédito definido en la metodología) y de su correspondencia con episodios económicos documentados.
- **OE5.** Comparar las representaciones no lineales (autoencoder y autoencoder LSTM) con la lineal en error de reconstrucción fuera de muestra, estabilidad de la representación y partición en regímenes resultante.

## 1.4 Hipótesis

No se formulan hipótesis de investigación, por tratarse de un estudio exploratorio y descriptivo: su propósito es construir una representación de los indicadores macrofinancieros e identificar regímenes a partir de ella, no contrastar proposiciones sobre el fenómeno establecidas de antemano. Los contrastes estadísticos que se emplean (con series de referencia simuladas y mediante remuestreo por bloques) son instrumentales: evalúan si la partición obtenida es distinguible de la que se produciría sin cambio de estructura y si es estable, y se describen en la metodología.
