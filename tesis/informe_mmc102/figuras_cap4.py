"""Figuras nuevas del Capítulo 4 (resultados del 9-11-2026)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

RAIZ = Path.cwd()
RES = RAIZ / "data/results/final/mmc102"
SAL = RAIZ / "tesis/informe_mmc102/fig"
AZUL, NARANJA, VERDE, TINTA, TINTA2, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e", "#b9b8b2"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": TINTA2, "xtick.color": TINTA2,
                     "ytick.color": TINTA2, "savefig.dpi": 300, "savefig.bbox": "tight", "lines.linewidth": 1.8})
coma = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",").replace("-", "−"))
epis = pd.read_csv(RAIZ / "data/referencia/episodios_referencia.csv", dtype=str).fillna("")


def sombrear(ax):
    for e in epis.itertuples():
        a = pd.Timestamp(e.inicio + "-01")
        b = pd.Timestamp((e.fin or e.inicio) + "-01") + pd.offsets.MonthEnd(0)
        ax.axvspan(a, b, color="#e8e7e2", zorder=0, linewidth=0)


def fecha(s):
    return pd.to_datetime(pd.Series(s).astype(str) + "-01")


# 1. Contraste de la partición -----------------------------------------------------
c = pd.read_csv(RES / "contraste_particion.csv")
fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True)
for ax, (tray, col, et) in zip(axs, [("estructura", "p95_estructura constante", "Estructura constante"),
                                     ("posición", "p95_ind_DS", "Tendencia (indeterminadas como DS)")]):
    d = c[c.trayectoria == tray]
    ax.plot(d.K, d.delta_obs, color=AZUL, marker="o", markersize=5, label="Observado")
    ax.plot(d.K, d[col], color=NARANJA, linestyle="--", marker="s", markersize=4, label=f"Percentil 95: {et}")
    ax.set_xlabel("Número de tramos K"); ax.set_xticks(range(2, 11))
    ax.yaxis.set_major_formatter(coma)
    ax.text(0.02, 1.02, "a" if tray == "estructura" else "b", transform=ax.transAxes, fontweight="bold")
axs[0].set_ylabel("Reducción relativa Δₖ")
axs[0].legend(frameon=False, fontsize=7.5, loc="upper right"); axs[1].legend(frameon=False, fontsize=7.5, loc="upper right")
fig.tight_layout(); fig.savefig(SAL / "c4_contraste_particion.png"); plt.close(fig)

# 2. Trayectoria de estructura con cortes preliminares ------------------------------
t = pd.read_csv(RES / "trayectoria_estructura.csv")
t["f"] = fecha(t.fecha)
cortes_e = ["2015-02", "2017-04", "2018-05", "2020-08", "2021-12"]
fig, ax = plt.subplots(figsize=(7.2, 2.9))
sombrear(ax)
ax.plot(t.f, t.lambda1, color=AZUL, label="Primer valor propio λ₁(t)")
ax.plot(t.f, t.lambda1_sin_2020, color=NARANJA, linestyle="--", linewidth=1.4, label="Sin marzo–junio de 2020 (interpolados)")
for cte in cortes_e:
    ax.axvline(pd.Timestamp(cte + "-01"), color=TINTA, linewidth=1, linestyle=":" if cte in ("2018-05", "2021-12") else "-")
ax.set_ylabel("λ₁(t)"); ax.yaxis.set_major_formatter(coma)
ax.legend(frameon=False, fontsize=7.5, loc="lower left")
fig.tight_layout(); fig.savefig(SAL / "c4_trayectoria_estructura.png"); plt.close(fig)

# 3. Perfil del RV entre ventanas adyacentes ---------------------------------------
r = pd.read_csv(RES / "cambio_estructura_perfil.csv")
r["f"] = fecha(r.frontera)
fig, ax = plt.subplots(figsize=(7.2, 2.6))
sombrear(ax)
ax.plot(r.f, r.rv_obs, color=AZUL, label="Observado")
ax.plot(r.f, r.p05_sim, color=NARANJA, linestyle="--", linewidth=1.4, label="Percentil 5, estructura constante")
ax.plot(r.f, r.mediana_sim, color=GRIS, linewidth=1.2, label="Mediana, estructura constante")
ax.set_ylabel("RV entre ventanas adyacentes"); ax.set_ylim(0, 1.02); ax.yaxis.set_major_formatter(coma)
ax.legend(frameon=False, fontsize=7.5, loc="lower left")
fig.tight_layout(); fig.savefig(SAL / "c4_rv_ventanas.png"); plt.close(fig)

# 4. Crecimiento real del crédito, regímenes de posición y fases ---------------------
g = pd.read_csv(RES / "preliminar_credito_real.csv")
g["f"] = fecha(g.fecha)
car = pd.read_csv(RES / "preliminar_caracterizacion.csv")
car = car[car.tipo == "posición"]
res = pd.read_csv(RES / "preliminar_resumen.csv", index_col=0).iloc[:, 0]
m, s = float(res["m_g"]), float(res["s_g"])
fig, ax = plt.subplots(figsize=(7.2, 3.0))
ax.plot(g.f, g.g_credito_real, color=AZUL, linewidth=1.6)
for cval, ls in ((1.0, "--"), (0.5, ":")):
    for sg in (1, -1):
        ax.axhline(m + sg * cval * s, color=NARANJA, linestyle=ls, linewidth=1)
ax.axhline(m, color=GRIS, linewidth=0.8)
for rr in car.itertuples():
    a, b = pd.Timestamp(rr.inicio + "-01"), pd.Timestamp(rr.fin + "-01") + pd.offsets.MonthEnd(0)
    ax.hlines(rr.credito_real_mediana, a, b, color=TINTA, linewidth=2.2)
    ax.text(a + (b - a) / 2, 33, str(rr.regimen), ha="center", color=TINTA2, fontsize=8)
    ax.axvline(a, color=GRIS, linewidth=0.6)
ax.set_ylabel("Crecimiento interanual real del crédito (%)"); ax.yaxis.set_major_formatter(coma)
ax.text(g.f.iloc[-1], m + s + 0.6, "m + s", ha="right", fontsize=7, color=TINTA2)
ax.text(g.f.iloc[-1], m + 0.5 * s + 0.6, "m + 0,5s", ha="right", fontsize=7, color=TINTA2)
ax.set_ylim(-8, 36)
fig.tight_layout(); fig.savefig(SAL / "c4_credito_real_fases.png"); plt.close(fig)

# 5. Estabilidad (congruencia por eje, ℓ = 24) ---------------------------------------
e = pd.read_csv(RES / "estabilidad_replicas.csv")
e = e[e.L == 24]
fig, ax = plt.subplots(figsize=(5.6, 2.6))
bins = np.linspace(0, 1, 26)
for k, col in ((1, AZUL), (2, NARANJA), (3, VERDE)):
    ax.hist(e[f"cong_{k}"], bins=bins, histtype="step", linewidth=1.8, color=col, label=f"Eje {k}")
ax.set_xlabel("Congruencia con el eje original"); ax.set_ylabel("Réplicas"); ax.xaxis.set_major_formatter(coma)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig(SAL / "c4_estabilidad_congruencia.png"); plt.close(fig)
print("figuras listas")
