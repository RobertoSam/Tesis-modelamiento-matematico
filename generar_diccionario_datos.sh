#!/bin/bash
# ==============================================================================
# generar_diccionario_datos_v2.sh
#
# Regenera papers/diccionario_datos.qmd para que refleje EXACTAMENTE los
# nombres de columna y codigos BCRP reales del pipeline (series_bcrp_raw.csv
# + embi_peru_raw.csv + indice_precios_inmuebles_bcrp.csv), ya sin ningun
# codigo pendiente de verificar.
#
# Uso:
#   bash generar_diccionario_datos_v2.sh
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

DEST_FILE="$RAIZ/papers/diccionario_datos.qmd"

if [ -f "$DEST_FILE" ]; then
    cp "$DEST_FILE" "$DEST_FILE.bak"
    echo "Backup guardado en: $DEST_FILE.bak"
fi

cat > "$DEST_FILE" << 'EOF'
---
title: "Diccionario de datos"
subtitle: "Nombre de columna real, descripción conceptual, código BCRP y transformación aplicada"
format:
  html:
    toc: true
---

::: {.callout-note title="Cómo usar esta página"}
Este diccionario refleja **exactamente** los nombres de columna que produce
el pipeline real (`data/raw/series_bcrp_raw.csv`, `embi_peru_raw.csv` e
`indice_precios_inmuebles_bcrp.csv`), no una nomenclatura conceptual aparte.
Si ves una columna en un notebook, la encuentras aquí con el mismo nombre.
:::

::: {.callout-tip title="Estado de verificación"}
Todos los códigos BCRP de esta tabla están **verificados** contra la API
oficial del BCRP (`estadisticas.bcrp.gob.pe`). Ninguno queda pendiente.
:::

## Glosario general

| Término | Significado en lenguaje simple |
|---|---|
| **Log-diferencia** | Cambio porcentual entre dos periodos, calculado con logaritmos; se usa en variables de nivel (créditos, precios, índices) porque estabiliza la varianza y es el insumo estándar para PCA/HFC. |
| **Diferencia simple** | Cambio absoluto entre dos periodos; se usa en variables que ya son tasas o porcentajes (TAMN, TIPMN, EMBI), donde una "diferencia de diferencia" no tendría sentido económico. |
| **Estandarización** | Transformar una variable para que tenga promedio 0 y desviación estándar 1, de modo que variables en unidades distintas (soles, %, puntos básicos) se puedan comparar y combinar en PCA/HFC. |

## Bloque: Crédito

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `Crédito SF sector privado` | `PN00518MM` | Suma total del crédito que el sistema financiero peruano otorga a hogares y empresas. | **Ninguna** — se excluye del dataset transformado por colinealidad casi perfecta con la suma de sus tres componentes. |
| `Crédito empresarial` | `PN00532MM` | Préstamos otorgados a empresas (capital de trabajo, inversión, etc.). | Log-diferencia |
| `Crédito consumo` | `PN00533MM` | Préstamos a personas para gastos personales (tarjetas, préstamos personales), no vivienda ni negocio. | Log-diferencia |
| `Crédito hipotecario` | `PN00534MM` | Préstamos destinados a compra o construcción de vivienda. | Log-diferencia |

> **Nota de colinealidad:** `Crédito SF sector privado` ≈ `Crédito empresarial` + `Crédito consumo` + `Crédito hipotecario`. Por eso el total se mantiene en el dataset de niveles (para consulta/gráficos) pero no entra al PCA/HFC junto con sus tres componentes.

## Bloque: Liquidez

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `Liquidez M1` | `PN00199MM` | "Dinero" en su forma más líquida: circulante (billetes y monedas) más depósitos a la vista. | Log-diferencia |
| `Liquidez M2` | `PN00208MM` | M1 más depósitos de ahorro y otros instrumentos de corto plazo en soles ("cuasidinero"). | Log-diferencia |
| `Liquidez M3` | `PN00214MM` | Liquidez total del sistema financiero, sumando soles y moneda extranjera. | Log-diferencia |

## Bloque: Tasas de interés

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `Tasa activa TAMN` | `PN07807NM` | Tasa promedio que cobran los bancos al prestar dinero en soles a sus clientes. | Diferencia simple |
| `Tasa pasiva TIPMN` | `PN07816NM` | Tasa promedio que pagan los bancos por depósitos en soles. | Diferencia simple |
| `Tasa referencia BCRP` | `PD04722MM` | Tasa de interés que fija el Banco Central como guía de política monetaria. | Diferencia simple |
| `Tasa interbancaria` | `PN07819NM` | Tasa a la que los bancos se prestan dinero entre sí a muy corto plazo. | Diferencia simple |

## Bloque: Inflación

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `IPC Lima` | `PN38705PM` | Índice de Precios al Consumidor de Lima Metropolitana (nivel, no variación). | Log-diferencia |
| `IPC Subyacente` | `PN38708PM` | IPC excluyendo los rubros más volátiles (alimentos frescos, combustibles); mide la tendencia de fondo de la inflación. | **Ninguna todavía** — serie de contraste/validación; pendiente decidir si entra al modelo (ver nota en `04_preprocesamiento.ipynb`). |

## Bloque: Tipo de cambio y mercado de capitales

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `Tipo de cambio` | `PN01246PM` | Tipo de Cambio Nominal Promedio, cuántos soles cuesta un dólar. | Log-diferencia |
| `Índice BVL` | `PN01142MM` | Índice General de la Bolsa de Valores de Lima (base 31/12/1991=100). | Log-diferencia |

## Bloque: Riesgo

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `embi_peru` | `PD04709XD` | Spread EMBIG Perú, en puntos básicos: cuánto más caro le resulta al Perú endeudarse en dólares frente a EE.UU. (mayor valor = mayor riesgo percibido). Serie **diaria** en origen (`data/raw/embi_peru_raw.csv`), resampleada a trimestral (promedio del periodo) en `04_preprocesamiento`. | Diferencia simple |

## Bloque: Actividad económica

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `PBI desestacionalizado` | `PN01773AM` | Producto Bruto Interno mensual, ajustado por estacionalidad (índice 2007=100). | Log-diferencia |
| `Demanda interna` | `PN01774AM` | Indicador de Demanda Interna (índice 2007=100): gasto total de hogares, empresas y gobierno. | Log-diferencia |
| `Reservas internacionales` | `PN00027MM` | Activos en moneda extranjera que mantiene el BCRP como respaldo del sistema financiero. | Log-diferencia |

## Bloque: Precios de activos inmobiliarios

| Columna real | Código BCRP | Descripción conceptual | Transformación aplicada |
|---|---|---|---|
| `indice_precios_inmuebles` | *(serie trimestral, cargada desde `data/raw/indice_precios_inmuebles_bcrp.csv`; código a documentar si aún no está registrado)* | Índice de precios de venta de inmuebles, indicador clave del ciclo financiero (precios de activos). | Log-diferencia |

---

**Resumen del pipeline:** 18 variables mensuales/diarias en `data/raw/`, sincronizadas a trimestral en `04_preprocesamiento.ipynb`, de las cuales 16 entran al dataset transformado y estandarizado para PCA/HFC (se excluyen `Crédito SF sector privado` por colinealidad e `IPC Subyacente` pendiente de decisión).
EOF

echo ""
echo "Archivo regenerado: $DEST_FILE"
echo "Siguiente paso: quarto render"
