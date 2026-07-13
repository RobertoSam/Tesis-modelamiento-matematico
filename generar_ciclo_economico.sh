#!/bin/bash
# ==============================================================================
# generar_ciclo_economico.sh
#
# Genera el archivo papers/ciclo_economico.qmd dentro del repositorio de la
# tesis "Ciclo Financiero Perú". Debe ejecutarse desde la raíz del repositorio
# (donde se encuentra _quarto.yml) o el script buscará esa raíz automáticamente.
#
# Uso:
#   chmod +x generar_ciclo_economico.sh
#   ./generar_ciclo_economico.sh
# ==============================================================================

set -e

# --- 1. Localizar la raíz del repositorio (donde está _quarto.yml) ---
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

DEST_DIR="$RAIZ/papers"
DEST_FILE="$DEST_DIR/ciclo_economico.qmd"

mkdir -p "$DEST_DIR"

if [ -f "$DEST_FILE" ]; then
    echo "AVISO: $DEST_FILE ya existe."
    read -p "¿Deseas sobrescribirlo? (s/N): " respuesta
    if [ "$respuesta" != "s" ] && [ "$respuesta" != "S" ]; then
        echo "Operación cancelada. No se modificó ningún archivo."
        exit 0
    fi
fi

# --- 2. Escribir el contenido del .qmd ---
cat > "$DEST_FILE" << 'EOF'
---
title: "Ciclo económico: conceptos, variables y periodo"
format:
  html:
    toc: true
---

## 1. Definición

El ciclo económico (*business cycle*) se distingue del ciclo financiero
trabajado en esta tesis (ver [Marco conceptual](marco_conceptual.qmd)).
Mientras el ciclo financiero se centra en la dinámica del crédito, la
liquidez y los precios de activos, el ciclo económico —en su formulación
clásica de Burns y Mitchell (1946)— se define sobre la actividad
agregada de la economía: expansiones que ocurren simultáneamente en
muchas actividades económicas, seguidas de contracciones igualmente
generalizadas.

## 2. Variable de referencia y componente cíclico

En la práctica moderna (véase el enfoque de fechado del BCRP), el ciclo
económico se mide extrayendo el **componente cíclico del PBI** mediante
filtros de tendencia-ciclo (p. ej. modelos de componentes no
observables). Un ciclo completo se define como el número de periodos
que toma dicho componente moverse de un pico al siguiente pico.

## 3. Periodo y fases

- Los comités de fechado (como el del NBER) identifican picos y valles
  siguiendo el criterio de disminución significativa y generalizada de
  la actividad económica, no restringida a una sola variable.
- Para el caso peruano, la evidencia disponible sugiere que los ciclos
  de la década de 1990 fueron más volátiles y de menor duración que los
  registrados en las décadas de 2000 y 2010 (Florián & Martínez, 2019).

## 4. Relación entre ciclo económico y ciclo financiero

### 4.1 Diferencias fundamentales

La distinción entre ambos ciclos, siguiendo a Borio (2014) y Drehmann,
Borio & Tsatsaronis (2012), no es solo temática sino estructural:

| Dimensión | Ciclo económico | Ciclo financiero |
|---|---|---|
| Variable de referencia | Componente cíclico del PBI | Crédito, precios de activos (bienes raíces, bolsa) |
| Duración típica | 1–8 años (Burns & Mitchell, 1946) | 8–20 años (Drehmann et al., 2012) |
| Metodología de fechado | Comités de fechado (NBER), filtros de tendencia-ciclo | Filtros de baja frecuencia sobre crédito/PBI y precios de activos |
| Fase crítica | Recesión (caída generalizada de actividad) | Fase de "bust" tras acumulación excesiva de apalancamiento |
| Relación con crisis financieras | Indirecta | Directa: los picos del ciclo financiero suelen anteceder o coincidir con crisis bancarias |

**Punto central para la tesis:** el ciclo financiero es de menor
frecuencia (más lento) que el ciclo económico. Esto significa que un
solo ciclo financiero puede contener varios ciclos económicos
completos.

### 4.2 Esquema temporal comparativo

```{mermaid}
gantt
    title Ciclo financiero como envolvente de varios ciclos económicos
    dateFormat  YYYY
    axisFormat  %Y

    section Ciclo financiero
    Fase expansiva (crédito y precios de activos al alza)   :active, cf1, 2000, 10y
    Fase de ajuste (desapalancamiento)                       :crit, cf2, 2010, 6y

    section Ciclo económico
    Expansión 1   :be1, 2000, 3y
    Recesión 1    :crit, be2, 2003, 1y
    Expansión 2   :be3, 2004, 4y
    Recesión 2 (crisis)   :crit, be4, 2008, 1y
    Expansión 3   :be5, 2009, 5y
    Recesión 3    :crit, be6, 2014, 2y
```

*(Los años son ilustrativos; deben calibrarse con la cronología real
que se defina para el caso peruano, por ejemplo con base en Florián &
Martínez, 2019.)*

### 4.3 Interacción entre ciclos: mecanismo de amplificación

```{mermaid}
flowchart TD
    A["Ciclo económico:<br/>expansión del PBI"] --> B["Mayor demanda de crédito"]
    B --> C["Ciclo financiero:<br/>expansión de crédito y precios de activos"]
    C --> D{"¿Acumulación de<br/>apalancamiento excesivo?"}
    D -- Sí --> E["Fase de vulnerabilidad financiera"]
    D -- No --> F["Expansión sostenible"]
    E --> G["Shock o punto de inflexión"]
    G --> H["Contracción simultánea:<br/>crisis financiera + recesión económica"]
    H --> I["Desapalancamiento prolongado<br/>(fase 'bust' del ciclo financiero)"]
    F --> A

    style H fill:#f8d7da,stroke:#c0392b
    style E fill:#fdebd0,stroke:#d68910
```

Este esquema resume el argumento central de Borio (2014): las crisis
más severas ocurren cuando el **pico del ciclo financiero coincide con
una fase descendente del ciclo económico**. No toda recesión económica
implica crisis financiera, pero las crisis financieras casi siempre
generan recesiones económicas profundas y prolongadas.

### 4.4 Representación conjunta como sistema multivariado

Retomando la notación ya definida en la sección 2 del marco conceptual:

$$
X_t = (x_{1t}, x_{2t}, \ldots, x_{pt}) \in \mathbb{R}^p
$$

Se puede formalizar la relación entre ambos ciclos separando el vector
de indicadores en dos subconjuntos:

$$
X_t = \big(\underbrace{X_t^{econ}}_{\text{PBI, empleo, demanda interna}},\ \underbrace{X_t^{fin}}_{\text{crédito, tasas, precios de activos}}\big)
$$

donde el **ciclo financiero** se estima sobre $X_t^{fin}$ mediante
PCA/HFC/EPCA-EHFC, y el **ciclo económico** —aunque no es el foco de
esta tesis— actúa como variable de contraste para validar si los
regímenes financieros detectados son coherentes con episodios reales
de expansión o recesión (esto conecta directamente con el criterio de
"interpretabilidad" ya definido en la sección 6.1 del marco
conceptual).

### 4.5 Implicancia para la tesis

Esta distinción justifica por qué la tesis prioriza el **ciclo
financiero** como objeto de estudio: al ser de menor frecuencia y mayor
persistencia estructural, es más adecuado para técnicas de reducción
dimensional evolutivas (EPCA/EHFC), que requieren ventanas móviles
suficientemente largas para capturar cambios estructurales estables. El
ciclo económico, al ser más rápido, se reserva como referencia de
validación y no como variable objetivo de modelamiento.

## Bibliografía

**Literatura clásica (definición y medición del ciclo económico):**

- Burns, A. F., & Mitchell, W. C. (1946). *Measuring Business Cycles*.
  National Bureau of Economic Research.
- Lucas, R. E. (1977). Understanding business cycles. *Carnegie-Rochester
  Conference Series on Public Policy*, 5(1), 7–29.
- Kydland, F. E., & Prescott, E. C. (1982). Time to build and aggregate
  fluctuations. *Econometrica*, 50(6), 1345–1370.

**Literatura sobre el ciclo económico peruano:**

- Florián, D., & Martínez, M. (2019). Identificación y fechado del
  ciclo económico en el Perú a partir de un modelo de componentes no
  observables: 1980-2018. *Revista Moneda*, (179), 25–30. BCRP.

> **PENDIENTE DE VERIFICACIÓN (no citar en el cuerpo de la tesis sin
> confirmar):**
>
> - Paper de Winkelried en la *Revista de Estudios Económicos* del
>   BCRP (No. 34) sobre cronología de ciclos económicos en el Perú.
>   Verificar título completo, año y coautoría.
> - Terrones, M., & Calderón, C. *El ciclo económico en el Perú*.
>   GRADE, Serie Documentos de Trabajo. Verificar año y número exacto
>   de documento.
> - Escobal y Torres (2002), Morón et al. (2002), Ochoa y Lladó
>   (2003), Pérez Forero et al. (2017) — referenciados de forma
>   indirecta en un recuadro del BCRP; verificar cada uno en su fuente
>   original antes de citarlos.

**Literatura sobre ciclo financiero (ya incorporada en el marco
conceptual):**

- Borio, C. (2014). The financial cycle and macroeconomics: What have
  we learnt? *Journal of Banking & Finance*.
- Drehmann, M., Borio, C., & Tsatsaronis, K. (2012). Characterising the
  financial cycle: Don't lose sight of the medium term! *BIS Working
  Papers*.
EOF

echo ""
echo "Archivo generado correctamente en:"
echo "  $DEST_FILE"
echo ""
echo "Siguientes pasos sugeridos:"
echo "  1. Revisar el contenido del archivo."
echo "  2. Añadir la entrada correspondiente en _quarto.yml, por ejemplo:"
echo ""
echo '       - text: Marco conceptual'
echo '         menu:'
echo '           - href: marco_conceptual.qmd'
echo '             text: "Régimen y transición financiera"'
echo '           - href: papers/ciclo_economico.qmd'
echo '             text: "Ciclo económico"'
echo ""
echo "  3. Ejecutar: quarto render"
echo "  4. Confirmar antes de publicar las referencias marcadas como PENDIENTES DE VERIFICACIÓN."
