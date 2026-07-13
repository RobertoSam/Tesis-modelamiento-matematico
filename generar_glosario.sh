#!/bin/bash
# ==============================================================================
# generar_glosario.sh
#
# Genera glosario.qmd en la raíz del repositorio: conceptos metodológicos
# centrales de la tesis (régimen, ciclo, PCA, HFC, EPCA/EHFC, Autoencoder,
# LSTM) en lenguaje accesible para un lector sin formación técnica profunda.
#
# Uso:
#   bash generar_glosario.sh
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
    exit 1
}

echo "Raíz del repositorio detectada en: $RAIZ"

DEST_FILE="$RAIZ/glosario.qmd"

if [ -f "$DEST_FILE" ]; then
    cp "$DEST_FILE" "$DEST_FILE.bak"
    echo "Backup guardado en: $DEST_FILE.bak"
fi

cat > "$DEST_FILE" << 'EOF'
---
title: "Glosario de terminología"
subtitle: "Conceptos metodológicos centrales de la tesis, en lenguaje accesible"
format:
  html:
    toc: true
---

::: {.callout-note title="Alcance de este glosario"}
Este glosario cubre los **conceptos metodológicos** que atraviesan
toda la tesis (régimen, ciclo, métodos de reducción dimensional y
aprendizaje automático). Para la terminología de **variables e
indicadores macrofinancieros** (crédito, liquidez, tasas, etc.), ver el
[Diccionario de datos](papers/diccionario_datos.qmd), que tiene su
propio glosario estadístico básico.
:::

## Conceptos centrales del ciclo financiero

**Régimen financiero**
: Un período de tiempo durante el cual el sistema financiero
  peruano se comporta de forma relativamente estable: las relaciones
  entre variables como crédito, tasas, liquidez e inflación se
  mantienen parecidas. No es "una variable en un nivel alto o bajo",
  sino una forma de organización conjunta del sistema.

**Transición de régimen**
: El momento (o período) en que esa forma de organización cambia de
  manera significativa y duradera — no un movimiento pasajero de una
  sola variable, sino una reconfiguración de cómo se relacionan varias
  variables entre sí.

**Ciclo financiero**
: La secuencia de expansión y contracción del crédito, la liquidez y
  los precios de activos (como bienes raíces o acciones) a lo largo
  del tiempo. Es un fenómeno de **más largo plazo** (típicamente 8 a
  20 años) que el ciclo económico tradicional.

**Ciclo económico**
: La secuencia de expansión y contracción de la actividad económica
  general (medida principalmente por el PBI). Es más corto que el
  ciclo financiero (típicamente 1 a 8 años). Ver la página
  [Ciclo económico](papers/ciclo_economico.qmd) para el desarrollo
  completo de esta distinción.

**Ventana móvil**
: Un tramo de tiempo de tamaño fijo (por ejemplo, 24 meses) que se
  desplaza mes a mes sobre la serie completa de datos, permitiendo
  observar cómo cambian las relaciones entre variables a medida que
  avanza el tiempo, en lugar de calcular un único resultado para todo
  el período histórico.

## Métodos de reducción dimensional y clasificación

**PCA (Análisis de Componentes Principales)**
: Una técnica que toma muchas variables relacionadas entre sí (por
  ejemplo, 15 indicadores financieros) y las resume en unas pocas
  "combinaciones" nuevas, llamadas componentes, que capturan la mayor
  parte de la información original con menos dimensiones.

**Componente principal**
: Cada una de las nuevas variables resumidas que produce el PCA.
  Se interpreta observando qué variables originales tienen mayor peso
  dentro de ella (por ejemplo, un componente puede estar dominado por
  variables de crédito y liquidez, lo que sugiere que representa
  "condiciones de financiamiento").

**Carga factorial**
: El peso o importancia que tiene cada variable original dentro de un
  componente principal. Cargas altas (en valor absoluto) indican que
  esa variable contribuye mucho a ese componente.

**Varianza explicada**
: Qué porcentaje de la información (variabilidad) total de los datos
  originales logra capturar un componente o un conjunto de
  componentes. Más varianza explicada con menos componentes significa
  un resumen más eficiente.

**HFC (Clasificación Factorial Jerárquica)**
: Un método que combina el PCA con clasificación: primero reduce la
  dimensión de los datos y luego agrupa observaciones (por ejemplo,
  meses) o variables en clases con comportamiento similar, mostrando
  ese agrupamiento como un árbol jerárquico.

**Dendrograma**
: La representación visual en forma de árbol que produce una
  clasificación jerárquica como la HFC, mostrando en qué nivel de
  similitud se van uniendo los grupos.

**Cluster**
: Un grupo de observaciones (por ejemplo, un conjunto de meses) que
  comparten características similares según el método de
  clasificación usado.

**EPCA (PCA Evolutivo)**
: La versión del PCA que se aplica sobre ventanas móviles en lugar de
  sobre todo el período a la vez, permitiendo observar cómo cambia la
  estructura de componentes a medida que pasa el tiempo.

**EHFC (HFC Evolutivo)**
: La versión evolutiva de la HFC: aplica la clasificación jerárquica
  sobre ventanas móviles sucesivas, permitiendo ver cómo se
  reconfiguran los grupos (clusters) con el tiempo — clave para
  detectar transiciones de régimen.

## Aprendizaje profundo aplicado a series temporales

**Autoencoder**
: Una red neuronal que aprende a comprimir los datos en una
  representación más pequeña (espacio latente) y luego a
  reconstruirlos, intentando que la reconstrucción se parezca lo más
  posible a los datos originales. Es una alternativa no lineal al PCA.

**Espacio latente**
: La representación comprimida que produce un Autoencoder (o método
  similar): un conjunto reducido de números que resume la información
  esencial de los datos originales, de forma similar a los
  componentes principales pero permitiendo relaciones no lineales.

**Error de reconstrucción**
: Qué tan diferente es la salida reconstruida del Autoencoder respecto
  a los datos originales que recibió. Un aumento sostenido en este
  error puede ser una señal de que el sistema está atravesando un
  cambio de régimen (algo "inusual" para el modelo).

**LSTM (Long Short-Term Memory)**
: Un tipo de red neuronal diseñada para trabajar con secuencias
  temporales, con una capacidad especial de "recordar" información
  relevante de períodos pasados y "olvidar" la que ya no es útil, lo
  que la hace apta para modelar dependencias de largo plazo en series
  financieras.

**Estado oculto**
: La "memoria interna" que mantiene una red LSTM mientras procesa una
  secuencia, actualizándose en cada paso de tiempo con la nueva
  información que recibe.

## Evaluación y comparación de métodos

**Interpretabilidad**
: Qué tan fácil es entender y explicar económicamente lo que un método
  encontró (por ejemplo, si un componente principal se puede asociar
  claramente a "condiciones de crédito").

**Estabilidad temporal**
: Si la estructura que encuentra un método se mantiene parecida entre
  ventanas de tiempo consecutivas cuando no hay una transición real, y
  cambia cuando sí la hay.

**Capacidad descriptiva**
: Qué tan bien resume un método la información original del sistema
  (por ejemplo, la varianza explicada en PCA o la calidad de
  reconstrucción en un Autoencoder).

**Robustez**
: Si los resultados de un método cambian mucho o poco ante variaciones
  razonables en las decisiones de diseño (tamaño de ventana, conjunto
  de variables, transformaciones aplicadas).

---

*Este glosario se actualiza conforme se precisan nuevas definiciones
en el marco conceptual. Ver también [Marco conceptual](marco_conceptual.qmd)
para el desarrollo matemático completo de cada concepto.*
EOF

echo ""
echo "Archivo generado: $DEST_FILE"
echo ""
echo "Añade esta entrada a _quarto.yml, por ejemplo en el navbar principal:"
echo ""
echo '       - href: glosario.qmd'
echo '         text: "Glosario"'
echo ""
echo "Siguiente paso: quarto render"
