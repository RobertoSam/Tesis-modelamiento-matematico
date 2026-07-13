#!/bin/bash
# ==============================================================================
# generar_index_dashboard_v2.sh
#
# Regenera index.qmd reflejando la ampliacion del pipeline de datos
# (de 13 a 18 variables) y enlazando el diccionario de datos actualizado.
#
# Uso:
#   bash generar_index_dashboard_v2.sh
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

DEST_FILE="$RAIZ/index.qmd"

if [ -f "$DEST_FILE" ]; then
    cp "$DEST_FILE" "$DEST_FILE.bak"
    echo "Backup guardado en: $DEST_FILE.bak"
fi

cat > "$DEST_FILE" << 'EOF'
---
title: "Medición del ciclo financiero en Perú"
subtitle: "Mediante técnicas de reducción dimensional y machine learning"
format:
  html:
    toc: false
---

::: {.callout-note title="Sobre este sitio"}
Este sitio documenta el avance de la tesis de maestría de Roberto
Samaniego Salcedo, bajo la supervisión del Dr. Sergio Camiz. Reúne el
marco conceptual, la revisión bibliográfica y el pipeline de datos del
BCRP en un solo lugar de consulta.
:::

## Resumen del avance

<!--
NOTA METODOLÓGICA (visible solo en el código fuente, no en el HTML):
Este avance se calcula solo sobre frentes con una unidad discreta
contable ("X de Y completos"). El marco conceptual y la validación de
resultados no tienen todavía una unidad de conteo clara y por eso se
muestran como estado cualitativo, no como porcentaje.

Fórmula del avance global: promedio simple de los tres frentes
cuantificables (bibliografía, pipeline de datos, modelamiento).
Para actualizar: cambia los numeradores/denominadores de cada frente
más abajo y recalcula el promedio a mano antes de publicar.
-->

::: {.callout-important title="Avance global aproximado: 40%"}
Cálculo informal de trabajo (no es una evaluación del asesor), basado
en el promedio de los tres frentes con conteo discreto: bibliografía
(20%), pipeline de datos (100%) y modelamiento (0%). El marco
conceptual y la validación de resultados se muestran aparte porque no
tienen todavía una unidad de conteo definida.
:::

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 24px 0;">

<div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px;">
<strong>Marco conceptual</strong><br/>
<span style="color: #6b7280; font-size: 14px;">v0.2 — en revisión con el asesor</span>
</div>

<div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px;">
<strong>Bibliografía</strong><br/>
<div style="background: #e5e7eb; border-radius: 999px; height: 10px; margin: 8px 0;">
  <div style="background: #486581; width: 20%; height: 10px; border-radius: 999px;"></div>
</div>
<span style="color: #6b7280; font-size: 14px;">3 de 15 fichas núcleo completas</span>
</div>

<div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px;">
<strong>Pipeline de datos BCRP</strong><br/>
<div style="background: #e5e7eb; border-radius: 999px; height: 10px; margin: 8px 0;">
  <div style="background: #486581; width: 100%; height: 10px; border-radius: 999px;"></div>
</div>
<span style="color: #6b7280; font-size: 14px;">4 de 4 etapas completas · 18 variables (ampliado de 13)</span>
</div>

<div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px;">
<strong>Modelamiento</strong><br/>
<div style="background: #e5e7eb; border-radius: 999px; height: 10px; margin: 8px 0;">
  <div style="background: #486581; width: 0%; height: 10px; border-radius: 999px;"></div>
</div>
<span style="color: #6b7280; font-size: 14px;">0 de 3 técnicas (notebooks por regenerar)</span>
</div>

<div style="border: 1px solid #e5e7eb; border-radius: 12px; padding: 16px;">
<strong>Validación de resultados</strong><br/>
<span style="color: #6b7280; font-size: 14px;">No iniciado</span>
</div>

</div>

## Literatura revisada

Fichas bibliográficas completas siguiendo la Ficha Estándar del
proyecto. Ver el detalle de cada una en la sección [Papers](papers/camiz_et_al_2020.qmd).

- [x] **Camiz et al. (2020)** — Hierarchical Factor Classification of
  Dendrochronological Time Series. Referencia metodológica central
  para HFC.
- [x] **Drehmann, Borio & Tsatsaronis (2012)** — Characterising the
  financial cycle. Referencia central para indicadores del ciclo
  financiero.
- [x] **Camiz, Maulucci & Roig (2010)** — EPCA / Statis dual.
  Fundamento metodológico de la extensión evolutiva del PCA.
- [ ] **Camiz & Roig (2011)** — eslabón faltante en la cadena
  metodológica HFC → EHFC. *Pendiente de localizar y procesar.*
- [ ] Referencias adicionales del núcleo (11 pendientes) — ver
  [Marco conceptual, sección 7](marco_conceptual.qmd#bibliografia)
  para el listado completo de la bibliografía inicial identificada.

## Pipeline de datos BCRP

Organizado por etapa metodológica, no por notebook individual:

- [x] **Extracción** — conexión a la API del BCRP, descarga de series.
  Ampliado recientemente de 13 a **18 variables** (se agregaron
  liquidez M1/M2/M3, tasa interbancaria, IPC subyacente y el spread
  EMBI Perú). Ver el [Diccionario de datos](papers/diccionario_datos.qmd)
  para el detalle completo de cada serie y su código BCRP verificado.
- [x] **Carga y verificación** — corrección de códigos de series mal
  etiquetados (tipo de cambio vs. crédito), verificación de
  integridad.
- [x] **Análisis exploratorio** — documentación de la colinealidad
  entre crédito total y sus componentes (empresarial, consumo,
  hipotecario).
- [x] **Preprocesamiento** — transformaciones (log-diferencia para
  niveles, diferencia simple para tasas y spreads), remuestreo
  trimestral, estandarización. Dataset final: **72 trimestres × 18
  variables transformadas**, listo para PCA/HFC.

## Modelamiento (próxima etapa)

- [ ] **PCA / HFC** — análisis de componentes principales y
  clasificación factorial jerárquica.
- [ ] **EPCA / EHFC** — extensión evolutiva con ventanas móviles.
- [ ] **Autoencoder / LSTM** — representaciones latentes no lineales y
  modelamiento secuencial.

---

*Este resumen se actualiza manualmente conforme avanza la tesis. Última
actualización: ver historial de commits de `index.qmd` en GitHub.*
EOF

echo ""
echo "index.qmd regenerado en: $DEST_FILE"
echo "Siguiente paso: quarto render"
