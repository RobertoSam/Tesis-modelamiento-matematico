"""Resumen, tablas y figuras del avance MMC102 (resultados preliminares, solo para el Word).

No estima nada nuevo: agrega y presenta los CSV vigentes de data/results/final/ (16 series,
niveles; decisiones D1, D15 y D16). Escribe:

- data/results/final/avance_resumen.csv: medidas agregadas (medida, valor) que lee
  herramientas/cifras_mapa.csv, de modo que ninguna cifra del capítulo 4 se escribe a mano;
- tesis/_capitulos/_avance_tabla_*.md: tablas en Markdown que el capítulo 4 incluye;
- tesis/figuras/avance_*.png: figuras del capítulo 4.

Uso, desde la raíz del repositorio:
    python3 herramientas/resumen_avance.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
FINAL = RAIZ / "data" / "results" / "final"
REF = RAIZ / "data" / "referencia" / "episodios_referencia.csv"
CAP = RAIZ / "tesis" / "_capitulos"
FIG = RAIZ / "tesis" / "figuras"
FIG.mkdir(exist_ok=True)

# Paleta categórica de referencia (slots 1-3) y tintas recesivas
AZUL, NARANJA, AGUAMARINA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA_SEC, REJILLA, BANDA = "#1f1f1e", "#5f5e5a", "#e6e5e1", "#d9d8d3"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": TINTA_SEC,
    "axes.labelcolor": TINTA, "xtick.color": TINTA_SEC, "ytick.color": TINTA_SEC,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": REJILLA, "grid.linewidth": 0.6, "legend.frameon": False,
    "savefig.dpi": 200, "savefig.bbox": "tight",
})


def num(x, dec=2):
    """Número con coma decimal (convención del informe)."""
    return f"{x:.{dec}f}".replace(".", ",")


def bandas_episodios(ax, episodios):
    """Sombrea los episodios de referencia (D7); los puntuales, como línea discontinua."""
    for e in episodios.itertuples():
        ini = pd.Timestamp(e.inicio + "-01")
        if isinstance(e.fin, str) and e.fin:
            fin = pd.Timestamp(e.fin + "-01") + pd.offsets.MonthEnd(0)
            ax.axvspan(ini, fin, color=BANDA, alpha=0.6, lw=0, zorder=0)
        else:
            ax.axvline(ini, color=TINTA_SEC, lw=0.8, ls="--", zorder=0)


episodios = pd.read_csv(REF, dtype=str).fillna("")
resumen = []

# ---- 1. PCA global: cargas de los tres primeros ejes (tabla) -------------------------------
cargas = pd.read_csv(FINAL / "05_pca_cargas.csv")
cos2 = pd.read_csv(FINAL / "05_pca_cos2.csv") if (FINAL / "05_pca_cos2.csv").exists() else None
filas = ["| Serie | Eje 1 | Eje 2 | Eje 3 |", "|---|---:|---:|---:|"]
for r in cargas.itertuples():
    celdas = []
    for k in ("PC1", "PC2", "PC3"):
        v = getattr(r, k)
        celdas.append(f"**{num(v)}**" if abs(v) >= 0.6 else num(v))
    filas.append(f"| {r.serie} | " + " | ".join(celdas) + " |")
(CAP / "_avance_tabla_cargas.md").write_text("\n".join(filas) + "\n", encoding="utf-8")

# ---- 2. PCA global: scores con episodios (figura 1) ---------------------------------------
sc = pd.read_csv(FINAL / "05_pca_scores.csv", parse_dates=["fecha"])
fig, ax = plt.subplots(figsize=(6.3, 2.9))
bandas_episodios(ax, episodios)
for k, c in zip(("PC1", "PC2", "PC3"), (AZUL, NARANJA, AGUAMARINA)):
    ax.plot(sc["fecha"], sc[k], color=c, lw=1.6, label=f"Eje {k[-1]}")
ax.axhline(0, color=TINTA_SEC, lw=0.6)
ax.set_ylabel("Coordenada (score)")
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(ncol=3, loc="upper left")
fig.savefig(FIG / "avance_scores_pca.png")
plt.close(fig)

# ---- 3. EPCA: estabilidad del eje 2 por ancho de ventana (figura 2) -----------------------
est = pd.read_csv(FINAL / "06_epca_estabilidad_ventanas_niveles.csv", parse_dates=["fecha"])
anchos = sorted(est["ventana"].unique())
fig, axes = plt.subplots(len(anchos), 1, figsize=(6.3, 5.8), sharex=True, sharey=True)
for ax, w in zip(axes, anchos):
    s = est[est["ventana"] == w]
    bandas_episodios(ax, episodios)
    ax.plot(s["fecha"], s["estabilidad"], color=AZUL, lw=1.4)
    ax.axhline(s["umbral"].iloc[0], color=NARANJA, lw=1.0, ls="--")
    bajo = s[s["estabilidad"] < s["umbral"]]
    ax.plot(bajo["fecha"], bajo["estabilidad"], "o", ms=4, color=NARANJA, mec="white", mew=0.8)
    ax.set_title(f"Ventana de {w} meses", loc="left", fontsize=8.5, color=TINTA, pad=2)
    ax.set_ylim(-0.05, 1.05)
axes[-1].xaxis.set_major_locator(mdates.YearLocator(2))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axes[len(anchos) // 2].set_ylabel("Estabilidad del eje 2 (regla del 06)", y=1.05)
fig.savefig(FIG / "avance_estabilidad_epca.png")
plt.close(fig)
for w in anchos:
    s = est[est["ventana"] == w]
    resumen.append((f"epca_bajo_umbral_nw{w}", int((s["estabilidad"] < s["umbral"]).sum())))
    resumen.append((f"epca_ventanas_nw{w}", len(s)))
# El archivo de transiciones detectadas corresponde a la ventana principal del notebook 06 (60 meses)
trans = pd.read_csv(FINAL / "06_epca_transiciones_detectadas_niveles.csv")
fechas_tr = [pd.Timestamp(f).strftime("%Y-%m") for f in trans.iloc[:, 0]]
resumen.append(("epca_transiciones_regla06", ", ".join(fechas_tr)))
resumen.append(("epca_n_transiciones_regla06", len(fechas_tr)))

# ---- 4. Nulo de estructura constante (OE4): menor p-valor de las filas principales ---------
oe4 = pd.read_csv(FINAL / "07b_nulo_estructura_oe4.csv")
prin = oe4[oe4["principal"].astype(str) == "True"]
resumen.append(("oe4_p_min_principal", float(prin["p_valor"].min())))
resumen.append(("oe4_filas_principales", len(prin)))
resumen.append(("oe4_filas_p_menor_005", int((prin["p_valor"] < 0.05).sum())))

# ---- 5. HFC: clases y estabilidad bootstrap ------------------------------------------------
boot = pd.read_csv(FINAL / "07c_hfc_bootstrap.csv")
resumen += [
    ("hfc_replicas", len(boot)),
    ("hfc_prop_ari3_uno", float((boot["ari_3"] == 1).mean())),
    ("hfc_prop_ari4_uno", float((boot["ari_4"] == 1).mean())),
    ("hfc_ari3_media", float(boot["ari_3"].mean())),
    ("hfc_ari4_media", float(boot["ari_4"].mean())),
    ("hfc_cofenetica_mediana", float(boot["cofenetica"].median())),
]
cl = pd.read_csv(FINAL / "07c_hfc_clases3.csv")
filas = ["| Partición | Clase | Series (representante en negrita) |", "|---|---|---|"]
for (p, c), g in cl.groupby(["particion", "clase"], sort=True):
    nombres = [f"**{r.serie}**" if str(r.representante) == "True" else r.serie for r in g.itertuples()]
    filas.append(f"| {p} clases | {c} | " + ", ".join(nombres) + " |")
(CAP / "_avance_tabla_hfc.md").write_text("\n".join(filas) + "\n", encoding="utf-8")

# ---- 6. Datación PCA-MM12 (d = 3, regla K, maxcl = 10): tabla y figura 3 ------------------
reg = pd.read_csv(FINAL / "09a_regimenes_pca.csv").fillna("")
estab = pd.read_csv(FINAL / "09a_estabilidad_cortes.csv")
frec = dict(zip(estab["corte"], estab["frecuencia"]))
filas = ["| N.º | Período | Meses | Crédito medio | Etiqueta | Frec. del corte | Episodios contenidos |",
         "|---:|---|---:|---:|---|---:|---|"]
for i, r in enumerate(reg.itertuples(), 1):
    f = frec.get(r.inicio)
    filas.append(f"| {i} | {r.inicio} a {r.fin} | {r.meses} | {num(r.componente_credito_medio)} | {r.fase} | "
                 f"{num(f) if f is not None else '—'} | {r.episodios_contenidos or '—'} |")
(CAP / "_avance_tabla_regimenes.md").write_text("\n".join(filas) + "\n", encoding="utf-8")
resumen.append(("datacion_n_regimenes", len(reg)))
resumen.append(("datacion_frec_min", float(estab["frecuencia"].min())))
resumen.append(("datacion_corte_frec_min", estab.loc[estab["frecuencia"].idxmin(), "corte"]))

L_MM = 12
mm = sc.set_index("fecha")[["PC1", "PC2", "PC3"]].rolling(L_MM).mean().dropna()
fig, ax = plt.subplots(figsize=(6.3, 2.9))
bandas_episodios(ax, episodios)
for k, c in zip(("PC1", "PC2", "PC3"), (AZUL, NARANJA, AGUAMARINA)):
    ax.plot(mm.index, mm[k], color=c, lw=1.6, label=f"Eje {k[-1]} (MM{L_MM})")
for r in reg.itertuples():
    ax.axvline(pd.Timestamp(r.inicio + "-01"), color=TINTA, lw=1.0)
ax.axhline(0, color=TINTA_SEC, lw=0.6)
ax.set_ylabel("Score suavizado")
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(ncol=3, loc="upper left")
fig.savefig(FIG / "avance_datacion_pca.png")
plt.close(fig)

pd.DataFrame(resumen, columns=["medida", "valor"]).to_csv(FINAL / "avance_resumen.csv", index=False)
print(pd.DataFrame(resumen, columns=["medida", "valor"]).to_string(index=False))
