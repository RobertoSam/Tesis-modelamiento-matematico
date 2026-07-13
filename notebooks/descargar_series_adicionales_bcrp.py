"""
descargar_series_adicionales_bcrp.py

Descarga series adicionales del BCRP (las marcadas con pendiente de
verificacion en el diccionario de datos) y las combina con el dataset
de extraccion existente.

USO:
1. Completa el diccionario SERIES_NUEVAS de mas abajo con los codigos
   reales que encuentres en el buscador de series del BCRP:
   https://estadisticas.bcrp.gob.pe/estadisticas/series/buscador
2. Ejecuta este script (o copia las funciones dentro de tu notebook
   01_extraccion_bcrp.ipynb).
3. Revisa el archivo de salida antes de fusionarlo con tu dataset
   principal.

IMPORTANTE:
- La API del BCRP permite un maximo de 10 series por llamada.
- Todas las series de una misma llamada deben tener la misma
  frecuencia (mensual, diaria, trimestral, anual, etc.). Este script
  agrupa automaticamente por frecuencia antes de llamar a la API.
"""

import requests
import pandas as pd
import time

# ==============================================================================
# 1. DICCIONARIO DE SERIES NUEVAS A DESCARGAR
#    Completa esto con los codigos reales encontrados en el buscador BCRP.
#    Formato: "nombre_corto": ("codigo_bcrp", "frecuencia")
#    Frecuencias validas para agrupar: "mensual", "diaria", "trimestral", "anual"
# ==============================================================================

SERIES_NUEVAS = {
    # --- Bloque Liquidez (equivalentes oficiales BCRP a M1/M2/M3) ---
    "m1":                   ("PN00199MM", "mensual"),  # Verificado: Dinero (circulante + depositos vista)
    "m2":                   ("PN00208MM", "mensual"),  # Verificado: Liquidez en Soles (M1 + cuasidinero MN)
    "m3":                   ("PN00214MM", "mensual"),  # Verificado: Liquidez Total (soles + dolares)

    # --- Bloque Tasas ---
    "tasa_referencia":      ("PD04722MM", "mensual"),  # Verificado: Tasa de Referencia de la Politica Monetaria
    "tasa_interbancaria":   ("PN07819NM", "mensual"),  # Verificado: Tasa Interbancaria Promedio
    "tasa_activa":          ("PN07807NM", "mensual"),  # Verificado: Activas - TAMN
    "tasa_pasiva":          ("PN07816NM", "mensual"),  # Verificado: Pasivas - TIPMN

    # --- Bloque Inflacion ---
    "ipc":                  ("PN38705PM", "mensual"),  # Verificado: Indice de Precios al Consumidor (IPC), nivel
    "inflacion_subyacente":  ("PN38708PM", "mensual"),  # Verificado: IPC Subyacente

    # --- Bloque Tipo de cambio ---
    "tc_nominal":           ("PN01210PM", "mensual"),  # Verificado: Tipo de Cambio Bancario - Promedio

    # --- Bloque Mercado de capitales ---
    "indice_bursatil":      ("PN01142MM", "mensual"),  # Verificado: Indice General BVL (base 31/12/91=100)

    # --- Bloque Riesgo ---
    "embi_peru":            ("PD04709XD", "diaria"),  # Verificado: Spread - EMBIG Peru (pbs). OJO: es diaria, no mensual.

    # --- Bloque Actividad economica ---
    "pbi_mensual":          ("PN01773AM", "mensual"),  # Verificado: PBI Desestacionalizado - mensual
    "demanda_interna":      ("PN01732AM", "mensual"),  # Verificado: Indicador de Demanda Interna
}

# Periodo de descarga: ajustar segun el rango historico de tu tesis
PERIODO_INICIAL = "2003-1"
PERIODO_FINAL = "2025-12"


def agrupar_por_frecuencia(series_dict):
    """
    Agrupa el diccionario de series por frecuencia, ya que la API del
    BCRP exige que todas las series de una misma llamada compartan
    frecuencia.
    """
    grupos = {}
    for nombre_corto, (codigo, frecuencia) in series_dict.items():
        if codigo == "PENDIENTE_COMPLETAR":
            print(f"AVISO: '{nombre_corto}' no tiene codigo asignado todavia, se omite.")
            continue
        grupos.setdefault(frecuencia, []).append((nombre_corto, codigo))
    return grupos


def dividir_en_lotes(lista, tamano=10):
    """
    Divide una lista en lotes de maximo 10 elementos, por el limite
    de la API del BCRP.
    """
    for i in range(0, len(lista), tamano):
        yield lista[i:i + tamano]


def descargar_lote(codigos, periodo_inicial, periodo_final):
    """
    Descarga un lote de hasta 10 series (misma frecuencia) desde la
    API del BCRP en formato JSON.
    """
    codigos_str = "-".join(codigos)
    url = (
        f"https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
        f"{codigos_str}/json/{periodo_inicial}/{periodo_final}/esp"
    )

    respuesta = requests.get(url, timeout=30)
    respuesta.raise_for_status()
    datos = respuesta.json()

    # Extraer nombres de columnas (uno por serie en el lote)
    nombres_series = [s["name"] for s in datos["config"]["series"]]

    filas = []
    for periodo in datos["periods"]:
        fila = {"periodo": periodo["name"]}
        for nombre_col, valor in zip(nombres_series, periodo["values"]):
            fila[nombre_col] = None if valor == "n.d." else float(valor)
        filas.append(fila)

    return pd.DataFrame(filas)


def descargar_series_nuevas(series_dict, periodo_inicial, periodo_final):
    """
    Descarga todas las series definidas en SERIES_NUEVAS, agrupando
    por frecuencia y respetando el limite de 10 series por llamada.
    Devuelve un diccionario {frecuencia: DataFrame}.
    """
    grupos = agrupar_por_frecuencia(series_dict)
    resultados = {}

    for frecuencia, lista_series in grupos.items():
        print(f"\nDescargando {len(lista_series)} series de frecuencia '{frecuencia}'...")
        dfs_lote = []

        for lote in dividir_en_lotes(lista_series, tamano=10):
            codigos_lote = [codigo for _, codigo in lote]
            print(f"  Lote: {codigos_lote}")
            df_lote = descargar_lote(codigos_lote, periodo_inicial, periodo_final)
            dfs_lote.append(df_lote)
            time.sleep(1)  # pausa breve para no saturar la API

        # Combinar todos los lotes de esta frecuencia por periodo
        df_frecuencia = dfs_lote[0]
        for df_extra in dfs_lote[1:]:
            df_frecuencia = df_frecuencia.merge(df_extra, on="periodo", how="outer")

        resultados[frecuencia] = df_frecuencia

    return resultados


if __name__ == "__main__":
    resultados = descargar_series_nuevas(SERIES_NUEVAS, PERIODO_INICIAL, PERIODO_FINAL)

    for frecuencia, df in resultados.items():
        salida = f"series_nuevas_{frecuencia}.csv"
        df.to_csv(salida, index=False)
        print(f"\nGuardado: {salida} ({df.shape[0]} filas, {df.shape[1]} columnas)")

    print("\nListo. Revisa los CSV generados antes de fusionarlos con tu dataset principal.")
    print("Recuerda: la fusion con el dataset existente debe hacerse en tu notebook")
    print("02_carga_y_verificacion.ipynb, siguiendo la misma separacion de responsabilidades")
    print("que ya usas en el pipeline (no mezclar extraccion con verificacion).")
