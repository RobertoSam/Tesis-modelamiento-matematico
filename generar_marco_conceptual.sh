#!/bin/bash
# ==============================================================================
# generar_marco_conceptual.sh
#
# Genera marco_conceptual.qmd en la raíz del repositorio de la tesis, a partir
# del contenido de tesis_semana1_marco_conceptual.html. También corrige el
# enlace interno en papers/ciclo_economico.qmd (si existe) para que apunte a
# la ruta correcta ("../marco_conceptual.qmd" en lugar de "marco_conceptual.qmd").
#
# Uso:
#   bash generar_marco_conceptual.sh
# ==============================================================================

set -e

buscar_raiz() {
    dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/_quarto.yml" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

RAIZ="$(buscar_raiz)" || {
    echo "ERROR: no se encontró _quarto.yml en ningún directorio superior."
    echo "Ejecuta este script dentro del repositorio de la tesis."
    exit 1
}

echo "Raíz del repositorio detectada en: $RAIZ"

DEST_FILE="$RAIZ/marco_conceptual.qmd"

if [ -f "$DEST_FILE" ]; then
    echo "AVISO: $DEST_FILE ya existe."
    read -p "¿Deseas sobrescribirlo? (s/N): " respuesta
    if [ "$respuesta" != "s" ] && [ "$respuesta" != "S" ]; then
        echo "Operación cancelada. No se modificó marco_conceptual.qmd."
    else
        SOBRESCRIBIR=1
    fi
else
    SOBRESCRIBIR=1
fi

if [ "$SOBRESCRIBIR" = "1" ]; then
cat > "$DEST_FILE" << 'EOF'
---
title: "Marco conceptual y metodológico preliminar"
subtitle: "Detección evolutiva de regímenes del ciclo financiero peruano mediante Clasificación Factorial Jerárquica y aprendizaje automático"
author: "Roberto Samaniego Salcedo"
date: "2026-06-01"
format:
  html:
    toc: true
    toc-depth: 3
---

::: {.callout-note title="Lectura rápida"}
Este documento convierte los entregables de la Semana 1 en una base más
profunda de discusión. Su función es ordenar conceptos, precisar
términos, vincular cada técnica con una finalidad dentro de la tesis y
preparar una primera conversación académica más rigurosa.
:::

**Programa:** Maestría en Ciencias en Modelización Matemática y Computacional
**Versión:** 0.2 — material de discusión
**Fecha:** Junio 2026

## 1. Objetivo del documento

La ficha de inscripción de tesis ya plantea un problema relevante:
identificar cambios de régimen en el ciclo financiero peruano usando
indicadores macrofinancieros del BCRP, técnicas exploratorias
evolutivas y métodos de aprendizaje automático. La propuesta combina
PCA, HFC, EPCA/EHFC, Autoencoders temporales y LSTM.

El objetivo de esta Semana 1 es transformar esa formulación inicial en
un marco de investigación más claro. Para ello se requiere precisar
cuatro aspectos:

1. qué se entenderá por régimen financiero;
2. qué se entenderá por transición de régimen;
3. qué significa detectar un régimen mediante datos;
4. qué tipo de evidencia permitirá sostener que hubo cambio estructural.

::: {.callout-important title="Pregunta rectora de la Semana 1"}
¿Cómo convertir la idea económica de "régimen financiero" en un objeto
matemático-computacional que pueda ser estudiado mediante análisis
multivariado, métodos evolutivos y aprendizaje automático?
:::

## 2. Marco conceptual de trabajo

La tesis requiere distinguir entre tres niveles de análisis que suelen
mezclarse:

| Nivel | Pregunta | Ejemplo en la tesis |
|---|---|---|
| Fenómeno económico | ¿Qué ocurre en el sistema financiero? | Expansión del crédito, estrés financiero, cambios en liquidez o tasas. |
| Objeto matemático | ¿Cómo represento ese fenómeno? | Matriz multivariada temporal, estructura de covarianza, espacio latente, partición de observaciones. |
| Procedimiento computacional | ¿Cómo lo estimo o detecto? | PCA, HFC, EPCA, Autoencoder, LSTM, métricas de estabilidad. |

Una tesis sólida necesita que estos tres niveles estén conectados. El
fenómeno económico motiva el estudio; el objeto matemático lo hace
tratable; el procedimiento computacional genera evidencia.

### 2.1 Régimen financiero

**Definición operacional preliminar**

> Un régimen financiero es un intervalo temporal durante el cual el
> sistema macrofinanciero presenta una configuración relativamente
> estable de relaciones entre variables financieras, monetarias y
> macroeconómicas.

Esta definición pone el énfasis en la **configuración conjunta**, no
en una variable aislada. Un régimen financiero no equivale simplemente
a "tasas altas", "inflación baja" o "crédito creciente". Es una forma
de organización del sistema observada a través de múltiples variables.

$$
X_t = (x_{1t}, x_{2t}, \ldots, x_{pt}) \in \mathbb{R}^p
$$

Donde $X_t$ representa el vector de indicadores macrofinancieros en el
tiempo $t$. El sistema financiero se observa como una trayectoria:

$$
\{X_t\}_{t=1}^{T}
$$

Un régimen puede entenderse como un subconjunto temporal $I_k$ en el
cual las propiedades estructurales de esa trayectoria se mantienen
relativamente estables.

$$
I_k = [t_a, t_b] \quad \text{tal que la estructura de } X_t \text{ es estable para } t \in I_k
$$

**Dimensiones estructurales del régimen**

| Dimensión | Interpretación | Representación posible |
|---|---|---|
| Factorial | Variables que se mueven conjuntamente y explican la variabilidad dominante. | Componentes principales, cargas factoriales, varianza explicada. |
| Clasificatoria | Agrupación de observaciones, períodos o variables con comportamiento similar. | Clusters, dendrogramas, particiones temporales. |
| Latente no lineal | Representación compacta que captura relaciones no necesariamente lineales. | Embeddings de Autoencoder, códigos latentes. |
| Dinámica | Dependencias temporales y memoria del sistema. | Estados ocultos, secuencias, LSTM, medidas de persistencia. |

**Implicancia para la tesis**

El régimen financiero será más defendible si se define como una
**propiedad de la estructura multivariada**. Esto permite conectar la
definición con PCA, HFC, EPCA/EHFC y Autoencoders sin reducir la tesis
a una clasificación subjetiva de episodios históricos.

::: {.callout-tip title="Definición de trabajo para revisión"}
Un régimen financiero será entendido como una configuración
temporalmente persistente de relaciones multivariadas entre
indicadores macrofinancieros, identificable mediante estructuras
factoriales, agrupamientos o representaciones latentes.
:::

### 2.2 Transición de régimen

**Definición operacional preliminar**

> Una transición de régimen es un cambio significativo y persistente
> en la estructura multivariada que caracteriza al sistema financiero.

La transición no se define como un salto puntual de una variable, sino
como una reconfiguración de relaciones. Por ejemplo, un aumento
transitorio del tipo de cambio puede no constituir transición si no
altera la estructura conjunta del sistema. En cambio, una modificación
sostenida en la relación entre crédito, liquidez, inflación, tasas y
mercado cambiario puede ser interpretada como transición.

**Tipos de transición**

| Tipo | Descripción | Señal esperada |
|---|---|---|
| Transición suave | Cambio gradual en la estructura del sistema. | Rotación progresiva de factores o desplazamiento continuo del espacio latente. |
| Transición abrupta | Reconfiguración rápida asociada a shock financiero o macroeconómico. | Cambio marcado en componentes, clusters o error de reconstrucción. |
| Transición parcial | Cambio en un bloque del sistema sin alterar toda la estructura. | Reordenamiento de variables específicas o clusters parciales. |
| Transición persistente | Cambio que permanece en varias ventanas temporales. | Estabilidad posterior de una nueva configuración. |

**Objeto matemático de la transición**

La transición puede formularse como un cambio entre estructuras
estimadas en dos ventanas temporales consecutivas:

$$
S(W_j) \neq S(W_{j+1})
$$

donde $S(W_j)$ representa la estructura estimada en la ventana $W_j$.
Esa estructura puede ser una matriz de cargas factoriales, una matriz
de distancias, una partición de clusters o una representación latente.

**Implicancia metodológica**

El uso de ventanas móviles permite convertir el problema en una
comparación entre estructuras sucesivas. Esta lógica es compatible con
EPCA/EHFC y también con representaciones latentes obtenidas mediante
modelos de aprendizaje profundo.

### 2.3 Detección de régimen

**Definición operacional preliminar**

> Detectar un régimen consiste en identificar intervalos temporales
> donde las observaciones comparten una estructura multivariada
> relativamente homogénea y diferenciable de otros intervalos.

La detección puede tener varios grados de exigencia:

| Nivel | Descripción | Ejemplo de evidencia |
|---|---|---|
| Descriptivo | El método muestra agrupamientos o patrones diferenciados. | Clusters temporales, mapas factoriales. |
| Estructural | El método muestra cambios en las relaciones entre variables. | Cambios en cargas factoriales o distancias entre estructuras. |
| Evolutivo | El método muestra cuándo y cómo cambian las estructuras. | Trayectorias de componentes, secuencias de particiones. |
| Comparativo | El método permite contrastar resultados con otras aproximaciones. | Coincidencia o divergencia entre EPCA, HFC y Autoencoder. |

::: {.callout-important title="Pregunta clave"}
Cuando dos métodos detecten períodos diferentes, la tesis necesitará
criterios para interpretar la discrepancia: sensibilidad al cambio,
estabilidad temporal, interpretabilidad económica, robustez o
capacidad de reconstrucción.
:::

### 2.4 Evidencia de cambio de régimen

La evidencia deberá ser multidimensional. Una única señal puede ser
insuficiente para sostener una transición. El diseño puede organizar
la evidencia en cuatro familias:

| Familia de evidencia | Qué observa | Métricas candidatas |
|---|---|---|
| Geométrica | Cambios en la posición, orientación o distancia dentro del espacio de representación. | Distancia entre subespacios, ángulo entre componentes, distancia Procrustes. |
| Factorial | Cambios en la explicación de varianza y cargas de variables. | Varianza explicada, correlación entre cargas, estabilidad de componentes. |
| Clasificatoria | Cambios en agrupamientos o pertenencias. | Adjusted Rand Index, matriz de transición, persistencia de clusters. |
| Latente-computacional | Cambios en embeddings o capacidad de reconstrucción. | Error de reconstrucción, distancia entre embeddings, separación latente. |

## 3. Mapa metodológico

El flujo de trabajo puede organizarse en cinco capas. Esta separación
ayuda a distinguir el dato original, la representación matemática, la
estimación computacional, la detección de estructuras y la validación.

```
CAPA 1: DATOS OBSERVADOS
Indicadores BCRP / SBS / mercado
        │
        ▼
CAPA 2: PREPROCESAMIENTO
Frecuencia común, limpieza, transformación, estandarización
        │
        ▼
CAPA 3: REPRESENTACIONES
Matriz temporal multivariada, ventanas móviles, espacios latentes
        │
        ├──────────────► PCA / EPCA
        │                    └── estructura factorial evolutiva
        │
        ├──────────────► HFC / EHFC
        │                    └── agrupamientos y evolución de clases
        │
        ├──────────────► Autoencoder temporal
        │                    └── representación latente no lineal
        │
        └──────────────► LSTM
                             └── representación dinámica secuencial
        │
        ▼
CAPA 4: DETECCIÓN DE REGÍMENES
Identificación de intervalos, transiciones y patrones persistentes
        │
        ▼
CAPA 5: VALIDACIÓN Y COMPARACIÓN
Interpretabilidad, estabilidad temporal, capacidad descriptiva, robustez
```

### Lectura del mapa

El mapa no debe interpretarse como una cadena rígida donde un método
reemplaza al anterior. La tesis puede organizarse como una comparación
de representaciones:

- **representación lineal:** PCA / EPCA;
- **representación clasificatoria:** HFC / EHFC;
- **representación no lineal:** Autoencoder;
- **representación dinámica:** LSTM.

El aporte se fortalecerá cuando la comparación no se limite a "qué
método funciona mejor", sino a **qué tipo de estructura revela cada
método** y bajo qué criterios se considera útil, estable o
interpretable.

## 4. Rol de cada método dentro de la tesis

### 4.1 PCA: análisis de componentes principales

El PCA permite construir combinaciones lineales de variables que
explican la mayor parte de la variabilidad. En esta tesis, su función
es generar una primera representación de la estructura macrofinanciera.

| | |
|---|---|
| **Entrada** | Matriz de indicadores estandarizados. |
| **Salida** | Componentes principales, cargas factoriales, scores. |
| **Utilidad** | Identificar factores dominantes del sistema financiero. |
| **Lectura económica** | Los componentes pueden asociarse a dimensiones como liquidez, crédito, condiciones monetarias o estrés financiero, siempre que las cargas lo permitan. |

### 4.2 HFC: Clasificación Factorial Jerárquica

La HFC combina representación factorial y clasificación jerárquica. Su
utilidad está en clasificar observaciones o variables dentro de un
espacio reducido, evitando clasificar directamente en una dimensión
alta y potencialmente ruidosa.

| | |
|---|---|
| **Entrada** | Coordenadas factoriales o estructura derivada del PCA. |
| **Salida** | Árbol jerárquico, clases, grupos homogéneos. |
| **Utilidad** | Identificar agrupamientos asociados a períodos financieros o familias de variables. |
| **Valor para la tesis** | Permite traducir estructuras continuas en clases interpretables. |

### 4.3 EPCA y EHFC: dimensión evolutiva

EPCA y EHFC incorporan explícitamente la dimensión temporal. El
interés no está solo en obtener una estructura promedio para todo el
período, sino en observar cómo esa estructura cambia al desplazarse en
el tiempo.

| | |
|---|---|
| **Entrada** | Ventanas móviles de la matriz temporal multivariada. |
| **Salida** | Secuencia de estructuras factoriales o clasificatorias. |
| **Utilidad** | Evaluar estabilidad temporal, rotación de componentes y reconfiguración de clases. |
| **Conexión con régimen** | Un régimen corresponde a un tramo donde la estructura evolutiva presenta estabilidad relativa. |

### 4.4 Autoencoder temporal

Un Autoencoder aprende una representación comprimida de los datos
intentando reconstruir la entrada. En la tesis puede utilizarse para
generar un espacio latente no lineal que complemente la representación
lineal del PCA.

| | |
|---|---|
| **Entrada** | Vectores o ventanas temporales de indicadores. |
| **Salida** | Código latente, error de reconstrucción, representación no lineal. |
| **Utilidad** | Capturar relaciones no lineales entre indicadores macrofinancieros. |
| **Indicador de transición** | Incrementos persistentes en error de reconstrucción o desplazamientos en el espacio latente. |

### 4.5 LSTM

Las redes LSTM modelan dependencias temporales mediante mecanismos de
memoria. En el contexto de la tesis, su papel puede estar vinculado a
representar secuencias macrofinancieras y detectar patrones donde el
estado actual depende de trayectorias pasadas.

| | |
|---|---|
| **Entrada** | Secuencias temporales multivariadas. |
| **Salida** | Estados ocultos, predicción, representación secuencial o clasificación de regímenes. |
| **Utilidad** | Capturar memoria temporal y dependencia de largo plazo. |
| **Conexión con régimen** | Un cambio de régimen puede expresarse como cambio en el patrón secuencial aprendido. |

## 5. Inventario inicial de variables

El diseño de variables debe representar el sistema financiero desde
varios bloques. Cada bloque cumple una función conceptual distinta.

| Bloque | Variables candidatas | Justificación | Transformaciones candidatas |
|---|---|---|---|
| Crédito | Crédito total, empresarial, consumo, hipotecario, microempresa, pequeña empresa. | El crédito es una dimensión central del ciclo financiero y de la expansión/contracción del sistema. | Variación mensual, variación anual, ratio sobre PBI, log-diferencias. |
| Liquidez | M1, M2, M3, liquidez del sistema financiero. | Representa condiciones monetarias y disponibilidad de fondos. | Crecimiento anual, ratios, estandarización. |
| Tasas | Tasa de referencia, interbancaria, activa promedio, pasiva promedio. | Capturan el precio del dinero y condiciones de financiamiento. | Niveles, spreads, diferencias. |
| Inflación | IPC, inflación anual, inflación subyacente. | Condiciona política monetaria, tasas reales y dinámica de crédito. | Variación anual, inflación mensual anualizada. |
| Tipo de cambio | Tipo de cambio nominal, variación cambiaria. | Representa presión externa, dolarización financiera y expectativas. | Log-diferencias, volatilidad móvil. |
| Mercado de capitales | Índice bursátil, rendimientos, capitalización si está disponible. | Introduce una dimensión de valoración financiera y apetito por riesgo. | Rendimiento mensual, volatilidad móvil. |
| Riesgo | EMBI Perú, spreads, indicadores de estrés si están disponibles. | Permite capturar estrés financiero y percepción de riesgo soberano. | Niveles, cambios mensuales, z-score. |
| Actividad económica | PBI mensual, demanda interna, producción sectorial. | Permite relacionar la dinámica financiera con el ciclo real. | Variación anual, brecha respecto a tendencia. |

::: {.callout-warning title="Punto de diseño"}
El inventario inicial deberá depurarse considerando frecuencia,
disponibilidad histórica, estabilidad de definiciones, valores
faltantes, cambios metodológicos y redundancia entre variables.
:::

**Nota de actualización (revisión posterior):** las series de crédito
del inventario original (PN01208PM, PN01209PM, PN01210PM) fueron
identificadas como series de tipo de cambio mal etiquetadas y
reemplazadas por los códigos verificados del Cuadro 19 del BCRP:
PN00532MM (crédito empresarial), PN00533MM (crédito consumo) y
PN00534MM (crédito hipotecario). Adicionalmente, se eliminó "Crédito
bancario SP" (PN00522MM) por colinealidad casi perfecta con la serie
de crédito total. Ver notebooks 01–02 del pipeline de datos para el
detalle de esta corrección.

## 6. Criterios iniciales de validación

La ficha de tesis plantea comparar los métodos en términos de
interpretabilidad, estabilidad temporal y capacidad descriptiva. Estos
criterios deben convertirse en métricas observables.

### 6.1 Interpretabilidad

Evalúa si el resultado puede asociarse a dimensiones económicas
comprensibles.

- concentración de cargas factoriales;
- variables dominantes por componente;
- coherencia económica de clusters;
- capacidad de explicar episodios históricos sin forzar la interpretación.

### 6.2 Estabilidad temporal

Evalúa si las estructuras identificadas permanecen relativamente
constantes dentro de un período y cambian cuando aparece una
transición.

- correlación entre componentes de ventanas sucesivas;
- distancia entre subespacios factoriales;
- persistencia de clusters;
- estabilidad de embeddings latentes.

### 6.3 Capacidad descriptiva

Evalúa si el método resume de manera útil la información del sistema.

- varianza explicada en PCA;
- calidad de reconstrucción en Autoencoder;
- separación entre grupos;
- coherencia temporal de los regímenes detectados.

### 6.4 Robustez

Aunque no aparece como criterio central en la ficha, la robustez será
importante para sostener conclusiones.

- sensibilidad al tamaño de ventana;
- sensibilidad al conjunto de variables;
- sensibilidad a transformaciones;
- sensibilidad a períodos de entrenamiento.

## 7. Bibliografía inicial comentada

La bibliografía se organiza por función dentro de la tesis. Esta
primera lista no reemplaza la revisión sistemática; sirve como punto
de partida para estructurar el estado del arte. Ver también la página
[Ciclo económico](papers/ciclo_economico.qmd) para la bibliografía
específica sobre ciclo económico (business cycle), que complementa —y
se distingue de— la del ciclo financiero listada aquí.

### 7.1 Ciclo financiero y regímenes financieros

1. **Borio, C. (2014).** *The financial cycle and macroeconomics: What
   have we learnt?* Journal of Banking & Finance. Texto base para
   entender el ciclo financiero como fenómeno diferente del ciclo
   económico tradicional.
2. **Drehmann, M., Borio, C., & Tsatsaronis, K. (2012).**
   *Characterising the financial cycle: Don't lose sight of the medium
   term!* BIS Working Papers. Referencia central para indicadores del
   ciclo financiero, especialmente crédito y precios de activos.
3. **Claessens, S., Kose, M. A., & Terrones, M. E. (2011/2012).**
   Trabajos sobre ciclos financieros y ciclos de negocios. Útiles para
   conectar régimen financiero con episodios de expansión y
   contracción.

### 7.2 Regime switching y cambios estructurales

4. **Hamilton, J. D. (1989).** *A New Approach to the Economic
   Analysis of Nonstationary Time Series and the Business Cycle.*
   Econometrica. Referencia clásica para modelos de cambio de régimen
   en series económicas.
5. **Hamilton, J. D. (1994).** *Time Series Analysis.* Princeton
   University Press. Base teórica amplia para series de tiempo y
   regímenes.
6. **Kim, C. J., & Nelson, C. R. (1999).** *State-Space Models with
   Regime Switching.* MIT Press. Útil para comprender regímenes como
   estados no observados.
7. **Krolzig, H. M. (1997).** *Markov-Switching Vector
   Autoregressions.* Springer. Referencia para enfoques multivariados
   de cambio de régimen.

### 7.3 Change Point Detection

8. **Truong, C., Oudre, L., & Vayatis, N. (2020).** *Selective review
   of offline change point detection methods.* Signal Processing.
   Organiza los métodos de detección de cambios en tres elementos:
   función de costo, método de búsqueda y restricción sobre número de
   cambios.
9. **Aminikhanghahi, S., & Cook, D. J. (2017).** *A survey of methods
   for time series change point detection.* Knowledge and Information
   Systems. Referencia de revisión para métodos de detección de puntos
   de cambio.

### 7.4 Análisis factorial, PCA y clasificación

10. **Pearson, K. (1901).** *On lines and planes of closest fit to
    systems of points in space.* Philosophical Magazine. Origen
    geométrico del PCA.
11. **Hotelling, H. (1933).** *Analysis of a complex of statistical
    variables into principal components.* Journal of Educational
    Psychology. Formalización clásica del análisis de componentes
    principales.
12. **Jolliffe, I. T. (2002).** *Principal Component Analysis.*
    Springer. Referencia estándar para teoría y aplicaciones de PCA.
13. **Lebart, L., Morineau, A., & Piron, M. (1995).** *Statistique
    exploratoire multidimensionnelle.* Dunod. Base para análisis
    exploratorio multidimensional.
14. **Camiz, S. y coautores.** Trabajos sobre análisis factorial,
    clasificación y métodos evolutivos. Esta línea deberá organizarse
    con especial cuidado por su vínculo directo con PCA, HFC, EPCA y
    EHFC. Ver fichas FB-001 y FB-002 en el sistema de fichas
    bibliográficas del proyecto.

### 7.5 Autoencoders y representaciones latentes

15. **Hinton, G. E., & Salakhutdinov, R. R. (2006).** *Reducing the
    Dimensionality of Data with Neural Networks.* Science. Referencia
    clásica sobre autoencoders como método no lineal de reducción de
    dimensionalidad.
16. **Goodfellow, I., Bengio, Y., & Courville, A. (2016).** *Deep
    Learning.* MIT Press. Marco general de aprendizaje profundo y
    representaciones.
17. **Chalapathy, R., & Chawla, S. (2019).** *Deep Learning for
    Anomaly Detection: A Survey.* Relevante si el error de
    reconstrucción se utiliza como indicador de cambio o anomalía.

### 7.6 LSTM y modelamiento secuencial

18. **Hochreiter, S., & Schmidhuber, J. (1997).** *Long Short-Term
    Memory.* Neural Computation. Referencia fundacional de LSTM.
19. **Gers, F. A., Schmidhuber, J., & Cummins, F. (2000).** *Learning
    to forget: Continual prediction with LSTM.* Neural Computation.
    Introduce mecanismos relevantes para memoria secuencial.

### 7.7 Fuentes de datos

20. **Banco Central de Reserva del Perú (BCRP).** Series estadísticas
    macroeconómicas y financieras. Fuente principal para variables
    monetarias, financieras, cambiarias y de actividad.
21. **Superintendencia de Banca, Seguros y AFP (SBS).** Información
    del sistema financiero peruano. Fuente complementaria para
    crédito, tasas, morosidad y estructura financiera.

## 8. Agenda de revisión

Para revisar este documento de forma eficiente, las siguientes
preguntas ordenan la discusión:

1. ¿La definición de régimen financiero captura adecuadamente el
   fenómeno que se quiere estudiar?
2. ¿El régimen debe definirse sobre observaciones temporales, sobre
   variables o sobre estructuras de relación?
3. ¿La transición de régimen debe exigir persistencia mínima? Si sí,
   ¿cuántos períodos o ventanas?
4. ¿La comparación entre métodos debe ser simétrica o cada método debe
   tener un rol específico?
5. ¿LSTM será un método central de detección, una extensión
   computacional o un modelo comparativo?
6. ¿Qué variables son esenciales para representar el ciclo financiero
   peruano?
7. ¿Qué métrica será prioritaria cuando los métodos entreguen
   conclusiones distintas?

---

*Documento generado como asistente de investigación. Versión
preliminar para revisión conceptual, metodológica y bibliográfica. Las
referencias deberán validarse y completarse en la matriz bibliográfica
correspondiente.*
EOF
echo "Archivo generado: $DEST_FILE"
fi

# --- Corregir el enlace interno en papers/ciclo_economico.qmd, si existe ---
CICLO_ECON="$RAIZ/papers/ciclo_economico.qmd"
if [ -f "$CICLO_ECON" ]; then
    if grep -q "\](marco_conceptual.qmd)" "$CICLO_ECON"; then
        # Backup antes de modificar
        cp "$CICLO_ECON" "$CICLO_ECON.bak"
        sed -i.tmp 's/\](marco_conceptual\.qmd)/](..\/marco_conceptual.qmd)/g' "$CICLO_ECON"
        rm -f "$CICLO_ECON.tmp"
        echo "Enlace corregido en: $CICLO_ECON"
        echo "  (marco_conceptual.qmd -> ../marco_conceptual.qmd)"
        echo "  Se guardó una copia de respaldo en: $CICLO_ECON.bak"
    else
        echo "No se encontró el patrón de enlace a corregir en $CICLO_ECON (puede que ya esté corregido)."
    fi
else
    echo "AVISO: no se encontró $CICLO_ECON. Omite este paso si aún no lo has generado."
fi

echo ""
echo "Siguientes pasos sugeridos:"
echo "  1. Revisar marco_conceptual.qmd."
echo "  2. Añadir la entrada en _quarto.yml, por ejemplo:"
echo ""
echo '       - href: marco_conceptual.qmd'
echo '         text: "Marco conceptual"'
echo ""
echo "  3. Ejecutar: quarto render"
