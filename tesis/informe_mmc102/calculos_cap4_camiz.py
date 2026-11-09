# -*- coding: utf-8 -*-
"""Salidas adicionales de los programas del Dr. Camiz para el Capítulo 4 (observaciones del 9-11-2026).

1. PCA: por eje, correlación de cada serie con el eje, cos² y contribución (sin cargas).
2. HFC: tabla completa de los 15 nodos de la jerarquía (tabla «hierar» de clahfac).
3. EPCA (aede, w = 48, nsd = 3):
   - seguimiento de los ejes entre ventanas: además de la alineación de signo de aede
     (mínimos cuadrados frente a la ventana anterior), cada eje se empareja con el eje de la
     ventana anterior de mayor congruencia en valor absoluto, para que el intercambio de ejes
     cuando sus valores propios se cruzan no se lea como un cambio de estructura;
   - valores propios λ1–λ3 de cada ventana frente al umbral del análisis paralelo;
   - correlaciones de cada serie con los ejes seguidos, a lo largo del tiempo.
4. HFC evolutiva: pertenencia de cada serie a la clase C1 (la que contiene al crédito
   hipotecario, representante de C1 en la HFC global) en cada ventana, con el corte en 0,7.

Uso, desde la raíz del repositorio: python3 tesis/informe_mmc102/calculos_cap4_camiz.py
"""
import itertools
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
from src import camiz_port as cp                      # noqa: E402
from src.datos import cargar_vias                     # noqa: E402
from src.parametros import leer_parametros            # noqa: E402

F = RAIZ / "data/results/final"
SAL = F / "mmc102"
FIG = RAIZ / "tesis/informe_mmc102/fig"
AZUL, NARANJA, VERDE, TINTA, TINTA2, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#0b0b0b", "#52514e", "#b9b8b2"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.edgecolor": TINTA2, "xtick.color": TINTA2,
                     "ytick.color": TINTA2, "savefig.dpi": 300, "savefig.bbox": "tight"})
coma = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",").replace("-", "−"))

PAR = leer_parametros(RAIZ)
X, _ = cargar_vias(RAIZ, excluidas=PAR["EXCLUIDAS"])
P = X.shape[1]
NOMBRE = {c: c.replace(" (dinero)", "").replace(" (liquidez total)", "")
          .replace("Reservas internacionales netas", "RIN").replace(" desestacionalizado", "")
          for c in X.columns}
EPIS = pd.read_csv(RAIZ / "data/referencia/episodios_referencia.csv", dtype=str).fillna("")


def sombrear(ax):
    for e in EPIS.itertuples():
        a = pd.Timestamp(e.inicio + "-01")
        b = pd.Timestamp((e.fin or e.inicio) + "-01") + pd.offsets.MonthEnd(0)
        ax.axvspan(a, b, color="#e8e7e2", zorder=0, linewidth=0)


# ------------------------------------------------------------------ 1. PCA
r = pd.read_csv(F / "05_pca_cargas.csv").set_index("serie")      # correlaciones serie–eje
vp = pd.read_csv(F / "05_pca_valores_propios.csv").valor_propio.to_numpy()
pca = pd.DataFrame({"Serie": [NOMBRE[s] for s in r.index]})
for k in (1, 2, 3):
    rk = r[f"PC{k}"].to_numpy()
    pca[f"r{k}"] = rk                                  # correlación con el eje k
    pca[f"cos2_{k}"] = rk ** 2                         # calidad de representación en el eje k
    pca[f"ctr{k}"] = 100 * rk ** 2 / vp[k - 1]         # contribución a la inercia del eje k (%)
pca["calidad"] = pca[["cos2_1", "cos2_2", "cos2_3"]].sum(axis=1)
pca.to_csv(SAL / "camiz_pca_indicadores.csv", index=False)
assert np.allclose(pca[["ctr1", "ctr2", "ctr3"]].sum(), 100, atol=1e-6)

# ------------------------------------------------------------------ 2. HFC: tabla completa
h = cp.clahfac(X)
hi = h["hierar"].copy()


def etiqueta(n):
    n = int(n)
    return NOMBRE[X.columns[n - 1]] if n <= P else f"nodo {n}"


nodos = pd.DataFrame({
    "nodo": hi.index, "une": [f"{etiqueta(a)} + {etiqueta(b)}" for a, b in zip(hi.N1, hi.N2)],
    "series": hi.Num, "lambda1": hi.Eigenv, "indice": hi.Index,
    "local1": hi["Loc_%1"], "local2": hi["Loc_%2"], "global1": hi["Glob_%1"],
    "global2": hi["Glob_%2"], "acum2": hi["Cum_%2"]}).iloc[::-1]
nodos.to_csv(SAL / "camiz_hfc_nodos_completo.csv", index=False)

# ------------------------------------------------------------------ 3. EPCA con seguimiento de ejes
NW, NSD = 48, 3
a = cp.aede(X, nw=NW, ndim=3, nsd=NSD, maxcl=10)
ev = a["eigenvalues"]
fechas = pd.to_datetime(pd.Series(ev.index).astype(str) + "-01")
C = a["correlationlsq"].copy()                      # wn × p × 3, signo alineado por aede
L = ev.to_numpy().copy()


def congr(u, v):
    return float(u @ v / np.sqrt((u @ u) * (v @ v)))


cambios, previa = [], (0, 1, 2)
for t in range(1, len(C)):
    # Permutación y signo que maximizan la congruencia con la ventana anterior ya seguida
    mejor, mejor_val = None, -np.inf
    for perm in itertools.permutations(range(3)):
        val = sum(abs(congr(C[t, :, perm[k]], C[t - 1, :, k])) for k in range(3))
        if val > mejor_val + 1e-12:
            mejor, mejor_val = perm, val
    if mejor != previa:
        # El eje seguido k toma el eje mejor[k] (por orden de valor propio) de la ventana t
        cambios.append({"ventana": ev.index[t], "permutacion": "-".join(str(q + 1) for q in mejor)})
        previa = mejor
    C[t] = C[t][:, list(mejor)]
    L[t] = L[t][list(mejor)]
    for k in range(3):
        if congr(C[t, :, k], C[t - 1, :, k]) < 0:
            C[t, :, k] = -C[t, :, k]
# Intercambio relativo a la ventana anterior: se registra la ventana en que ocurre
pd.DataFrame(cambios).to_csv(SAL / "epca_intercambio_ejes.csv", index=False)
cont = [min(abs(congr(C[t, :, k], C[t - 1, :, k])) for k in range(3)) for t in range(1, len(C))]
pd.DataFrame({"ventana": ev.index[1:], **{f"congr_eje{k + 1}": [congr(C[t, :, k], C[t - 1, :, k])
              for t in range(1, len(C))] for k in range(3)}}).to_csv(SAL / "epca_congruencia_consecutiva.csv", index=False)
for k in range(3):
    pd.DataFrame(C[:, :, k], index=ev.index, columns=[NOMBRE[c] for c in X.columns]).to_csv(
        SAL / f"epca_correlaciones_eje{k + 1}_seguido.csv")
pd.DataFrame(L, index=ev.index, columns=["eje1", "eje2", "eje3"]).to_csv(SAL / "epca_valores_propios_seguidos.csv")

# Umbral del análisis paralelo con el tamaño efectivo de la ventana (≈ 37): interpolación 36–38
horn = pd.read_csv(F / "R_aede_horn_umbrales.csv")
n_ef = float(np.sum(cp.pesos_aede(NW, NSD)) ** 2 / np.sum(cp.pesos_aede(NW, NSD) ** 2))
umbral = {k: float(np.interp(n_ef, horn[horn.eje == k].n_horn, horn[horn.eje == k].horn_p95)) for k in (1, 2, 3)}

# Figura: valores propios por orden (λ1 ≥ λ2 ≥ λ3) frente al umbral
fig, axs = plt.subplots(2, 1, figsize=(7.2, 4.6), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
for ax in axs:
    sombrear(ax)
axs[0].plot(fechas, ev.Dim_01, color=AZUL, lw=1.6, label="λ₁")
axs[0].axhline(umbral[1], color=AZUL, lw=0.9, ls=":")
axs[0].set_ylabel("λ₁"); axs[0].yaxis.set_major_formatter(coma)
axs[0].legend(frameon=False, loc="lower left")
axs[1].plot(fechas, ev.Dim_02, color=NARANJA, lw=1.4, label="λ₂")
axs[1].plot(fechas, ev.Dim_03, color=VERDE, lw=1.4, label="λ₃")
axs[1].axhline(umbral[2], color=NARANJA, lw=0.9, ls=":")
axs[1].axhline(umbral[3], color=VERDE, lw=0.9, ls=":")
axs[1].set_ylabel("λ₂ y λ₃"); axs[1].yaxis.set_major_formatter(coma)
axs[1].legend(frameon=False, loc="upper left", ncol=2)
for c in cambios:
    for ax in axs:
        ax.axvline(pd.Timestamp(c["ventana"] + "-01"), color=TINTA2, lw=0.7, ls="--")
fig.tight_layout(); fig.savefig(FIG / "c4_epca_valores_propios.png"); plt.close(fig)

# Figura: mapa de correlaciones con los ejes 1 y 2 seguidos
fig, axs = plt.subplots(2, 1, figsize=(7.2, 6.0), sharex=True)
ext = [matplotlib.dates.date2num(fechas.iloc[0]), matplotlib.dates.date2num(fechas.iloc[-1]), P - 0.5, -0.5]
for ax, k in zip(axs, (0, 1)):
    im = ax.imshow(C[:, :, k].T, aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1, interpolation="nearest", extent=ext)
    ax.set_yticks(range(P)); ax.set_yticklabels([NOMBRE[c] for c in X.columns], fontsize=6.5)
    ax.set_title(f"Eje {k + 1} seguido", fontsize=9, loc="left")
    ax.xaxis_date()
fig.colorbar(im, ax=axs, shrink=0.6, label="Correlación con el eje", format=coma)
fig.savefig(FIG / "c4_epca_correlaciones_mapa.png"); plt.close(fig)

# Figura: correlaciones de cada serie con los ejes 1 y 2 seguidos, en el tiempo
fig, axs = plt.subplots(4, 4, figsize=(7.4, 7.0), sharex=True, sharey=True)
for j, ax in enumerate(axs.ravel()):
    sombrear(ax)
    ax.axhline(0, color=GRIS, lw=0.6)
    ax.plot(fechas, C[:, j, 0], color=AZUL, lw=1.2, label="Eje 1")
    ax.plot(fechas, C[:, j, 1], color=NARANJA, lw=1.2, label="Eje 2")
    ax.set_title(NOMBRE[X.columns[j]], fontsize=7.5, loc="left")
    ax.set_ylim(-1.05, 1.05); ax.yaxis.set_major_formatter(coma)
    ax.tick_params(labelsize=6.5)
    ax.xaxis.set_major_locator(matplotlib.dates.YearLocator(5))
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
axs[0, 0].legend(frameon=False, fontsize=6.5, loc="lower left")
fig.tight_layout(); fig.savefig(FIG / "c4_epca_correlaciones_series.png"); plt.close(fig)

# ------------------------------------------------------------------ 4. HFC evolutiva: clase C1
peso = cp.pesos_aede(NW, NSD)


def hfc_ponderada(V):
    R = cp.bstatw(V, peso)["correlations"]
    j = cp.agrega(R)
    merge = np.where(j["nab"] <= P, -j["nab"], j["nab"] - P)
    return {"merge": merge, "height": np.asarray(j["indice"], dtype=float)}


def particion_07(hier, umbral_=0.7):
    nod = {}
    for i, (a_, b_) in enumerate(hier["merge"], start=1):
        ga = {-a_} if a_ < 0 else nod[a_]
        gb = {-b_} if b_ < 0 else nod[b_]
        nod[i] = ga | gb
    clases = [{i} for i in range(1, P + 1)]
    for i in range(1, len(hier["merge"]) + 1):
        if hier["height"][i - 1] <= umbral_:
            clases = [c for c in clases if not c <= nod[i]] + [nod[i]]
    return clases


ref = list(X.columns).index("Crédito hipotecario") + 1
wn = len(X) - NW + 1
ini = int(np.floor(1 + NW / 2))
fechas_c = list(X.index[ini - 1:ini - 1 + wn])
M = np.zeros((wn, P), dtype=int)
ncl = []
for t in range(wn):
    cl = particion_07(hfc_ponderada(X.iloc[t:t + NW].to_numpy()))
    ncl.append(len(cl))
    c1 = next(c for c in cl if ref in c)
    for i in c1:
        M[t, i - 1] = 1
assert fechas_c == list(ev.index)
pd.DataFrame(M, index=fechas_c, columns=[NOMBRE[c] for c in X.columns]).assign(n_clases=ncl).to_csv(SAL / "claede_c1_ventanas.csv")

fig, axs = plt.subplots(2, 1, figsize=(7.2, 5.4), sharex=True, gridspec_kw={"height_ratios": [1, 3.2]})
sombrear(axs[0])
axs[0].step(fechas, ncl, where="mid", color=AZUL, lw=1.3)
axs[0].set_ylabel("Clases"); axs[0].set_yticks(range(1, max(ncl) + 1))
axs[0].set_title("a", fontsize=9, loc="left", fontweight="bold")
cmap = matplotlib.colors.ListedColormap(["#f2f1ec", AZUL])
axs[1].imshow(M.T, aspect="auto", cmap=cmap, vmin=0, vmax=1, interpolation="nearest", extent=ext)
axs[1].set_yticks(range(P)); axs[1].set_yticklabels([NOMBRE[c] for c in X.columns], fontsize=6.5)
axs[1].set_title("b", fontsize=9, loc="left", fontweight="bold")
axs[1].xaxis_date()
fig.tight_layout(); fig.savefig(FIG / "c4_claede_c1.png"); plt.close(fig)

# ------------------------------------------------------------------ Resumen
frac = pd.Series(M.mean(axis=0), index=[NOMBRE[c] for c in X.columns]).sort_values(ascending=False)
frac.round(3).to_csv(SAL / "claede_c1_frecuencia.csv", header=["fraccion_ventanas"])
res = {"n_ef_ventana": n_ef, **{f"umbral_paralelo_{k}": v for k, v in umbral.items()},
       "ventanas": wn, "intercambios": "; ".join(f"{c['ventana']} ({c['permutacion']})" for c in cambios),
       "congr_min_consecutiva": min(cont),
       "ventanas_l2_sobre_umbral": int((ev.Dim_02 > umbral[2]).sum()),
       "ventanas_l3_sobre_umbral": int((ev.Dim_03 > umbral[3]).sum()),
       "tamano_c1_min": int(M.sum(axis=1).min()), "tamano_c1_max": int(M.sum(axis=1).max())}
pd.Series(res).to_csv(SAL / "camiz_epca_resumen.csv", header=["valor"])
print(pd.Series(res).to_string()); print(frac.round(2).to_string())
print(pd.DataFrame(M, index=fechas_c).sum(axis=1).groupby(lambda s: s[:4]).agg(["min", "max"]).T.to_string())
