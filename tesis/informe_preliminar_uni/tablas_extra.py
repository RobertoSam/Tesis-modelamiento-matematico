"""Tablas adicionales del informe preliminar (versión del 8-11-2026).

Lee resultados ya calculados en data/results/final y escribe, en
data/results/final/informe_uni, cuatro tablas listas para el informe:
  - tendencia_series.csv: tipo de tendencia y deriva de cada serie
  - factores_hfc.csv: correlaciones entre los representantes de las clases
  - cortes_grilla.csv: cortes del primer valor propio del EPCA por ventana
  - sensibilidad_media_movil_tabla.csv: cortes con media causal y centrada
No calcula nada nuevo: solo selecciona, redondea y rotula.
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RES = RAIZ / "data" / "results" / "final"
SAL = RES / "informe_uni"


def dec(x, n=2):
    """Número con coma decimal y n decimales."""
    return f"{x:.{n}f}".replace(".", ",").replace("-", "−")


# 1. Tipo de tendencia y deriva
t = pd.read_csv(RES / "05_tendencia_series.csv")
clase = {"DS": "DS", "TS": "TS", "indeterminada": "Ind."}
tabla = pd.DataFrame({
    "Serie": t["nombre"],
    "Tipo": t["clase_d5"].map(clase),
    "t de la deriva": t["deriva_hac_t"].map(dec),
    "r con el tiempo": t["r_tiempo"].map(dec),
})
tabla.to_csv(SAL / "tendencia_series.csv", index=False)

# 2. Correlaciones entre los representantes (factores) de las tres clases
c = pd.read_csv(RES / "07c_hfc_correlaciones3.csv")
c = c[c["tipo"] == "factores"]
nombres = {"C1": "Escala", "C2": "Tasas", "C3": "Riesgo"}
filas = []
for (a, b), g in c.groupby(["clase_a", "clase_b"]):
    fila = {"Par de clases": f"{nombres[a]} – {nombres[b]}"}
    for version, rotulo in [("original", "Niveles"), ("sin_tendencia", "Sin tendencia")]:
        r = g[g["version"] == version].iloc[0]
        fila[rotulo] = f"{dec(r['r'])} [{dec(r['p5'])}; {dec(r['p95'])}]"
    filas.append(fila)
pd.DataFrame(filas).to_csv(SAL / "factores_hfc.csv", index=False)

# 3. Cortes del EPCA por ancho de ventana y pesos (criterio de la tesis)
g = pd.read_csv(RES / "06c_aede_cortes.csv")
g = g[(g["maxcl"] == 10) & g["criterio"].str.startswith("codo")]
g = g.assign(Pesos=g["pesos"].map(lambda p: "Gaussianos" if p.startswith("gau") else "Uniformes"))
pd.DataFrame({
    "Ventana (meses)": g["nw"],
    "Pesos": g["Pesos"],
    "Tramos": g["k"],
    "Cortes": g["cortes"].str.replace(" ", ", "),
}).to_csv(SAL / "cortes_grilla.csv", index=False)

# 4. Sensibilidad de la datación al tipo de media móvil
m = pd.read_csv(SAL / "sensibilidad_media_movil.csv")
m = m.assign(Media=m["version"].map(lambda v: "Causal" if v.startswith("causal") else "Centrada"))
pd.DataFrame({
    "Media móvil": m["Media"],
    "Corte": m["corte"],
    "Episodio más cercano": m["episodio_mas_cercano"],
    "Distancia (meses)": m["distancia_meses"],
    "Compatible (±3 meses)": m["compatible_3"].map({True: "Sí", False: "No"}),
}).to_csv(SAL / "sensibilidad_media_movil_tabla.csv", index=False)

print("Tablas escritas en", SAL)
