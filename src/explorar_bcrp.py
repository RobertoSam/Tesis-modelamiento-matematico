"""
Exploración de series del BCRP para tesis de ciclo financiero
Autor: Roberto Samaniego
"""

import requests
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

SERIES = {
    # CRÉDITO
    "Crédito sector privado (S/.)":     "PN01207PM",
    "Crédito hipotecario (S/.)":        "PN01210PM",
    "Crédito consumo (S/.)":            "PN01209PM",
    "Crédito en ME (US$)":              "PN01208PM",

    # TASAS DE INTERÉS
    "Tasa activa MN (TAMN %)":          "PN07807NM",
    "Tasa de referencia BCRP (%)":      "PD04722MM",
    "Tipo de cambio S/. por US$":       "PN01246PM",

    # ACTIVIDAD ECONÓMICA
    "PBI (índice)":                     "PN01773AM",
    "Demanda interna (índice)":         "PN01774AM",
}

BASE_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

def descargar_serie(codigo, nombre, inicio="2000-1", fin="2024-12"):
    url = f"{BASE_URL}/{codigo}/json/{inicio}/{fin}/ing"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None, f"Error HTTP {r.status_code}"
        data = r.json()
        periodos = data.get("periods", [])
        if not periodos:
            return None, "Sin datos"
        registros = []
        for p in periodos:
            valor = p["values"][0]
            try:
                valor = float(str(valor).replace(",", "."))
            except:
                valor = None
            registros.append({"fecha": p["name"], "valor": valor})
        df = pd.DataFrame(registros)
        df["fecha"] = pd.to_datetime(df["fecha"], format="%b.%Y", errors="coerce")
        df = df.dropna(subset=["fecha"]).set_index("fecha").sort_index()
        return df, None
    except Exception as e:
        return None, str(e)

def explorar_series():
    print("=" * 65)
    print("EXPLORACIÓN DE SERIES BCRP — CICLO FINANCIERO PERÚ")
    print("=" * 65)
    resumen = []
    for nombre, codigo in SERIES.items():
        print(f"\n⏳ {nombre}...")
        df, error = descargar_serie(codigo, nombre)
        if error:
            print(f"   ❌ Error: {error}")
            resumen.append({"Serie": nombre, "Código": codigo, "Estado": "Error",
                "Inicio": "-", "Fin": "-", "Obs": "-", "Nulos%": "-", "Último": "-"})
        else:
            nulos = round(df["valor"].isna().sum() / len(df) * 100, 1)
            print(f"   ✅ {len(df)} obs. | {df.index[0].strftime('%Y-%m')} a {df.index[-1].strftime('%Y-%m')} | Nulos: {nulos}%")
            resumen.append({"Serie": nombre, "Código": codigo, "Estado": "OK",
                "Inicio": df.index[0].strftime("%Y-%m"), "Fin": df.index[-1].strftime("%Y-%m"),
                "Obs": len(df), "Nulos%": nulos, "Último": round(df["valor"].dropna().iloc[-1], 2)})
    print("\n" + "=" * 65)
    df_r = pd.DataFrame(resumen)
    print(df_r.to_string(index=False))
    df_r.to_csv("data/raw/resumen_series_bcrp.csv", index=False)
    print("\n✅ Guardado en data/raw/resumen_series_bcrp.csv")

if __name__ == "__main__":
    explorar_series()
