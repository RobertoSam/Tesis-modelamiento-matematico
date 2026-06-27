"""
Visualización de series del BCRP — Ciclo Financiero Perú
Autor: Roberto Samaniego
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

SERIES = {
    "Crédito sector privado":   "PN01207PM",
    "Crédito hipotecario":      "PN01210PM",
    "Crédito consumo":          "PN01209PM",
    "Crédito en ME":            "PN01208PM",
    "Tasa activa (TAMN)":       "PN07807NM",
    "Tasa referencia BCRP":     "PD04722MM",
    "Tipo de cambio S//$":      "PN01246PM",
    "PBI (índice)":             "PN01773AM",
    "Demanda interna":          "PN01774AM",
}

BLOQUES = {
    "Crédito": ["Crédito sector privado", "Crédito hipotecario", "Crédito consumo", "Crédito en ME"],
    "Tasas de interés": ["Tasa activa (TAMN)", "Tasa referencia BCRP"],
    "Tipo de cambio": ["Tipo de cambio S//$"],
    "Actividad económica": ["PBI (índice)", "Demanda interna"],
}

BASE_URL = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

def descargar_serie(codigo, inicio="2000-1", fin="2024-12"):
    url = f"{BASE_URL}/{codigo}/json/{inicio}/{fin}/ing"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        periodos = data.get("periods", [])
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
        return df.dropna(subset=["fecha"]).set_index("fecha").sort_index()
    except:
        return pd.DataFrame()

# Descargar todas
print("Descargando series...")
data = {}
for nombre, codigo in SERIES.items():
    df = descargar_serie(codigo)
    if not df.empty:
        data[nombre] = df["valor"]
        print(f"  ✅ {nombre}")

# Graficar por bloques
colores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

fig = plt.figure(figsize=(16, 14))
fig.suptitle("Series Macroeconómicas del BCRP — Ciclo Financiero Perú\n(2000–2024)",
             fontsize=14, fontweight="bold", y=0.98)

gs = gridspec.GridSpec(4, 2, figure=fig, hspace=0.5, wspace=0.35)

posiciones = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1)]
bloque_pos = {"Crédito": (0, slice(0,2)), "Tasas de interés": (1, 0),
              "Tipo de cambio": (1, 1), "Actividad económica": (2, slice(0,2))}

# Grafico 1: Crédito (fila completa)
ax1 = fig.add_subplot(gs[0, :])
for i, nombre in enumerate(BLOQUES["Crédito"]):
    if nombre in data:
        ax1.plot(data[nombre].index, data[nombre].values,
                label=nombre, color=colores[i], linewidth=1.5)
ax1.set_title("Crédito", fontsize=11, fontweight="bold")
ax1.legend(fontsize=8, loc="upper left")
ax1.grid(True, alpha=0.3)
ax1.set_ylabel("Log S/. / US$")

# Grafico 2: Tasas
ax2 = fig.add_subplot(gs[1, 0])
for i, nombre in enumerate(BLOQUES["Tasas de interés"]):
    if nombre in data:
        ax2.plot(data[nombre].index, data[nombre].values,
                label=nombre, color=colores[i], linewidth=1.5)
ax2.set_title("Tasas de interés (%)", fontsize=11, fontweight="bold")
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)

# Grafico 3: Tipo de cambio
ax3 = fig.add_subplot(gs[1, 1])
if "Tipo de cambio S//$" in data:
    ax3.plot(data["Tipo de cambio S//$"].index, data["Tipo de cambio S//$"].values,
            color="#d62728", linewidth=1.5)
ax3.set_title("Tipo de cambio (S/. por US$)", fontsize=11, fontweight="bold")
ax3.grid(True, alpha=0.3)

# Grafico 4: Actividad económica (fila completa)
ax4 = fig.add_subplot(gs[2, :])
for i, nombre in enumerate(BLOQUES["Actividad económica"]):
    if nombre in data:
        ax4.plot(data[nombre].index, data[nombre].values,
                label=nombre, color=colores[i], linewidth=1.5)
ax4.set_title("Actividad económica (índice)", fontsize=11, fontweight="bold")
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)

# Grafico 5: Correlaciones
ax5 = fig.add_subplot(gs[3, :])
df_all = pd.DataFrame(data).dropna()
corr = df_all.corr()
im = ax5.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax5.set_xticks(range(len(corr.columns)))
ax5.set_yticks(range(len(corr.columns)))
ax5.set_xticklabels([c[:20] for c in corr.columns], rotation=45, ha="right", fontsize=7)
ax5.set_yticklabels([c[:20] for c in corr.columns], fontsize=7)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax5.text(j, i, f"{corr.values[i,j]:.2f}", ha="center", va="center", fontsize=6)
ax5.set_title("Matriz de correlaciones", fontsize=11, fontweight="bold")
plt.colorbar(im, ax=ax5, shrink=0.8)

plt.savefig("reports/figures/exploracion_bcrp.png", dpi=150, bbox_inches="tight")
print("\n✅ Gráfico guardado en reports/figures/exploracion_bcrp.png")
plt.show()
