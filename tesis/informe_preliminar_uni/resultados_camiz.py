# -*- coding: utf-8 -*-
"""Resultados de los programas del Dr. Camiz para el informe preliminar (Guía N.° 2).

Usa el port a Python de AedeClahfac 1.2 (src/camiz_port.py, paridad verificada con el binario
en R) sobre las 16 series en niveles congeladas. Reproduce las salidas de:

- clahfac: jerarquía de la HFC (tabla «hierar»), inercia y dendrograma con el corte en 0,7;
- aede: valores propios evolutivos, correlaciones evolutivas y partición de Fisher del primer
  valor propio con el índice de Caliński y Harabasz que calcula aede;
- claede (Claede-2_2.R): la HFC repetida en cada ventana móvil; valores propios de los nodos
  superiores y dendrogramas de ventanas seleccionadas;
- PCA: círculos de correlaciones y tabla de cos² y contribuciones (desde data/results/final).

Uso, desde la raíz del repositorio:
    python3 tesis/informe_preliminar_uni/resultados_camiz.py <carpeta_salida>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
from src import camiz_port as cp                      # noqa: E402
from src.datos import cargar_vias                     # noqa: E402
from src.parametros import leer_parametros            # noqa: E402

SAL = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "data/results/final/informe_uni"
(SAL / "fig").mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 150})
AZUL, NARANJA, VERDE, GRIS, ROJO = "#1f5fa8", "#d9822b", "#2e8b57", "#bdbdbd", "#c0392b"

PAR = leer_parametros(RAIZ)
X, _ = cargar_vias(RAIZ, excluidas=PAR["EXCLUIDAS"])
P = X.shape[1]
EPIS = pd.read_csv(RAIZ / "data/referencia/episodios_referencia.csv", dtype=str).fillna("")
NOMBRE = {c: c.replace(" (dinero)", "").replace(" (liquidez total)", "")
          .replace("Reservas internacionales netas", "RIN").replace(" desestacionalizado", "")
          for c in X.columns}


def sombrear(ax, fechas):
    """Sombrea los episodios de referencia sobre un eje con fechas 'AAAA-MM' como posiciones."""
    pos = {f: i for i, f in enumerate(fechas)}
    for e in EPIS.itertuples():
        ini, fin = e.inicio, (e.fin or e.inicio)
        a = [i for f, i in pos.items() if ini <= f <= fin]
        if a:
            ax.axvspan(min(a) - 0.5, max(a) + 0.5, color=GRIS, alpha=0.45, lw=0)


def eje_anios(ax, fechas, paso=2):
    t = [i for i, f in enumerate(fechas) if f.endswith("-01") and int(f[:4]) % paso == 0]
    ax.set_xticks(t)
    ax.set_xticklabels([fechas[i][:4] for i in t])


def dibujar_dendrograma(ax, hier, etiquetas, corte=0.7, ymax=None, rotar=90):
    """Dendrograma con las coordenadas de hc2axes del programa del asesor."""
    ejes = cp.hc2axes(hier)
    merge, altura = hier["merge"], hier["height"]
    orden = list(hier["order"])
    xpos = {j: orden.index(j + 1) + 1 for j in range(len(etiquetas))}

    def coord(k):
        if k < 0:
            return xpos[-k - 1], 0.0
        return ejes["x.axis"][k - 1], altura[k - 1]

    for i, (a, b) in enumerate(merge):
        xa, ya = coord(a)
        xb, yb = coord(b)
        yh = altura[i]
        ax.plot([xa, xa, xb, xb], [ya, yh, yh, yb], color="black", lw=0.9)
        if yh >= corte * 0.7 or i == len(merge) - 1:
            ax.text((xa + xb) / 2, yh, f" {i + 1 + len(etiquetas)}", fontsize=6.5, color="#555555",
                    va="bottom", ha="center")
    ax.axhline(corte, color=ROJO, lw=1, ls="--")
    ax.set_xticks(range(1, len(etiquetas) + 1))
    ax.set_xticklabels([NOMBRE[etiquetas[j - 1]] for j in orden], rotation=rotar, fontsize=7.5)
    ax.set_ylabel("Índice (segundo valor propio del nodo)")
    if ymax:
        ax.set_ylim(0, ymax)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0)


# ---------------------------------------------------------------- 1. HFC global (clahfac)
h = cp.clahfac(X)
fig, ax = plt.subplots(figsize=(7.2, 4.4))
dibujar_dendrograma(ax, h["hier"], list(X.columns))
fig.tight_layout()
fig.savefig(SAL / "fig/camiz_hfc_dendrograma.png", dpi=200)
plt.close(fig)

hi = h["hierar"].copy()
nombres_nodo = {j + 1: NOMBRE[c] for j, c in enumerate(X.columns)}


def etiqueta(n):
    return nombres_nodo.get(int(n), f"nodo {int(n)}")


def composicion(n):
    fila = h["nclass"].loc[n].to_numpy()
    miembros = [nombres_nodo[int(v)] for v in fila if v > 0]
    return "las 16 series" if len(miembros) == P else ", ".join(miembros)


tab = pd.DataFrame({
    "Nodo": hi.index,
    "Une": [f"{etiqueta(a)} + {etiqueta(b)}" for a, b in zip(hi.N1, hi.N2)],
    "Composición": [composicion(n) for n in hi.index],
    "Series": hi.Num,
    "λ1": hi.Eigenv.round(3),
    "λ2 (índice)": hi.Index.round(3),
    "% local λ1": hi["Loc_%1"].round(1),
    "% global λ2 acum.": hi["Cum_%2"].round(2),
})
tab = tab.iloc[::-1].head(8)
tab.to_csv(SAL / "camiz_hfc_nodos.csv", index=False)
inercia = h["inertia"]

# ---------------------------------------------------------------- 2. PCA: círculos y cos²
cargas = pd.read_csv(RAIZ / "data/results/final/05_pca_cargas.csv")
vp = pd.read_csv(RAIZ / "data/results/final/05_pca_valores_propios.csv")
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.7))
for ax, (i, j) in zip(axs, [(1, 2), (1, 3)]):
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(t), np.sin(t), color="black", lw=0.7)
    ax.axhline(0, color=GRIS, lw=0.6)
    ax.axvline(0, color=GRIS, lw=0.6)
    for r in cargas.itertuples():
        x, y = getattr(r, f"PC{i}"), getattr(r, f"PC{j}")
        ax.annotate("", xy=(x, y), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="->", color=AZUL, lw=0.8))
        if abs(y) >= 0.3 or x < 0.5:
            ax.text(x * 1.08, y * 1.08 + (0.06 if r.serie == "Tasa interbancaria" else 0),
                    NOMBRE[r.serie], fontsize=6.5, ha="center", va="center")
    resto = [r for r in cargas.itertuples() if abs(getattr(r, f"PC{j}")) < 0.3 and getattr(r, f"PC{i}") >= 0.5]
    ax.text(0.62, -0.42 if j == 2 else 0.52, f"Bloque de tendencia\n({len(resto)} series)", fontsize=6.5,
            ha="center", color=AZUL)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal")
    ax.set_xlabel(f"Eje {i} ({vp.inercia[i - 1]:.1f} %)".replace(".", ","))
    ax.set_ylabel(f"Eje {j} ({vp.inercia[j - 1]:.1f} %)".replace(".", ","))
fig.tight_layout()
fig.savefig(SAL / "fig/camiz_pca_circulos.png", dpi=200)
plt.close(fig)

cos2 = pd.read_csv(RAIZ / "data/results/final/05_pca_cos2.csv")
ctr = pd.read_csv(RAIZ / "data/results/final/05_pca_contribuciones.csv")
ccols = [c for c in ctr.columns if c.lower().startswith(("ctr", "contrib", "pc"))][:3]
tcos = pd.DataFrame({"Serie": cos2.serie,
                     "cos² eje 1": cos2.cos2_1.round(2), "cos² eje 2": cos2.cos2_2.round(2),
                     "cos² eje 3": cos2.cos2_3.round(2), "Calidad (1–3)": cos2.suma_1_3.round(2)})
for k, c in enumerate(ccols, start=1):
    v = ctr[c].to_numpy(dtype=float)
    tcos[f"Contrib. eje {k} (%)"] = (100 * v if v.max() <= 1.0001 else v).round(1)
for c in [c for c in tcos.columns if c.startswith("Contrib.")]:
    tcos[c] = tcos[c].map(lambda v: f"{v:.1f}")
tcos.to_csv(SAL / "camiz_pca_cos2_contrib.csv", index=False, float_format="%.2f")

# ---------------------------------------------------------------- 3. aede (EPCA del asesor)
NW, NSD, MAXCL = 48, 3, 10
a = cp.aede(X, nw=NW, ndim=3, nsd=NSD, maxcl=MAXCL)
ev = a["eigenvalues"]
part = a["cutpoints"]["part"]
k_ch = int(part["n"][part["Calinski-Harabasz"].iloc[1:].idxmax()])
fila = part.iloc[k_ch - 1]
lim = [int(fila[f"v_{q}"]) for q in range(1, k_ch + 1)]
fechas_ev = list(ev.index)
cortes = [fechas_ev[v] for v in lim[:-1]]          # criterio del antecedente (CH de aede, maxcl = 10)
# Criterio principal (D11, D12): el CH no selecciona; codo = mayor caída de la suma intra
wss = part["Within ssq"].to_numpy()
caida = -np.diff(wss)
k_codo = int(np.argmax(caida)) + 2
fila_c = part.iloc[k_codo - 1]
cortes_codo = [fechas_ev[int(fila_c[f"v_{q}"])] for q in range(1, k_codo)]
fig, axs = plt.subplots(2, 1, figsize=(7.4, 4.8), sharex=True, gridspec_kw={"height_ratios": [2, 1.2]})
sombrear(axs[0], fechas_ev)
axs[0].plot(range(len(ev)), ev.Dim_01, color=AZUL, lw=1.4, label="λ1")
for c in cortes:
    axs[0].axvline(fechas_ev.index(c) - 0.5, color="black", lw=0.9, ls="--")
for c in cortes_codo:
    axs[0].axvline(fechas_ev.index(c) - 0.5, color=ROJO, lw=1.6)
axs[0].set_ylabel("Primer valor propio")
axs[0].legend(loc="lower right", frameon=False)
sombrear(axs[1], fechas_ev)
axs[1].plot(range(len(ev)), ev.Dim_02, color=NARANJA, lw=1.2, label="λ2")
axs[1].plot(range(len(ev)), ev.Dim_03, color=VERDE, lw=1.2, label="λ3")
axs[1].axhline(1, color=GRIS, lw=0.8, ls=":")
axs[1].set_ylabel("λ2 y λ3")
axs[1].legend(loc="upper right", frameon=False, ncol=2)
eje_anios(axs[1], fechas_ev)
fig.tight_layout()
fig.savefig(SAL / "fig/camiz_aede_valores_propios.png", dpi=200)
plt.close(fig)

tpart = pd.DataFrame({"Tramos (k)": part["n"].astype(int),
                      "SC intra": part["Within ssq"].round(2),
                      "Caliński-Harabasz": part["Calinski-Harabasz"].round(1)})
tpart["Cortes (primer mes del nuevo tramo)"] = [
    ", ".join(fechas_ev[int(part.iloc[k - 1][f"v_{q}"])] for q in range(1, k)) if k > 1 else "—"
    for k in tpart["Tramos (k)"]]
tpart.to_csv(SAL / "camiz_aede_particion.csv", index=False)

# correlaciones evolutivas con el eje 1 (con alineación de signo de aede)
corr1 = a["correlationlsq"][:, :, 0]
corr2 = a["correlationlsq"][:, :, 1]
fig, axs = plt.subplots(2, 1, figsize=(7.4, 6.2), sharex=True)
for ax, C, tit in [(axs[0], corr1, "Eje 1"), (axs[1], corr2, "Eje 2")]:
    im = ax.imshow(C.T, aspect="auto", cmap="RdBu_r", vmin=-1, vmax=1, interpolation="nearest")
    ax.set_yticks(range(P))
    ax.set_yticklabels([NOMBRE[c] for c in X.columns], fontsize=6.5)
    ax.set_title(tit, fontsize=9, loc="left")
    for c in cortes:
        ax.axvline(fechas_ev.index(c) - 0.5, color="black", lw=0.8, ls="--")
    for c in cortes_codo:
        ax.axvline(fechas_ev.index(c) - 0.5, color="black", lw=1.4)
eje_anios(axs[1], fechas_ev)
fig.colorbar(im, ax=axs, shrink=0.6, label="Correlación con el eje")
fig.savefig(SAL / "fig/camiz_aede_correlaciones.png", dpi=200, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- 4. HFC evolutiva (procedimiento de claede)
# claede (Claede-2_2.R) aplica la HFC a cada ventana con pesos gaussianos (nsd = 3), como Camiz y
# Spada (2024). El binario AedeClahfac 1.2 ignora los pesos, de modo que aquí la jerarquía de cada
# ventana se construye con el algoritmo de agregación del port (agrega) sobre la matriz de
# correlaciones PONDERADA de la ventana. Paridad con el programa original: pendiente.
peso_c = cp.pesos_aede(NW, NSD)


def hfc_ponderada(V):
    R = cp.bstatw(V, peso_c)["correlations"]
    j = cp.agrega(R)
    p_ = R.shape[0]
    merge = np.where(j["nab"] <= p_, -j["nab"], j["nab"] - p_)
    def hojas(k):
        if k < 0:
            return [-k]
        a_, b_ = merge[k - 1]
        return hojas(a_) + hojas(b_)
    orden = np.array(hojas(len(merge)))
    return {"merge": merge, "height": np.asarray(j["indice"], dtype=float), "order": orden}


def particion_07(hier, umbral=0.7):
    """Clases que quedan al no fusionar nodos con índice mayor que el umbral."""
    p_ = len(hier["order"])
    grupo = {i: {i} for i in range(1, p_ + 1)}
    nodos = {}
    for i, (a_, b_) in enumerate(hier["merge"], start=1):
        ga = {-a_} if a_ < 0 else nodos[a_]
        gb = {-b_} if b_ < 0 else nodos[b_]
        nodos[i] = ga | gb
    clases = [{i} for i in range(1, p_ + 1)]
    for i, (a_, b_) in enumerate(hier["merge"], start=1):
        if hier["height"][i - 1] <= umbral:
            u = nodos[i]
            clases = [c for c in clases if not c <= u] + [u]
    return clases


wn = len(X) - NW + 1
ini = int(np.floor(1 + NW / 2))
fechas_c = list(X.index[ini - 1:ini - 1 + wn])
alt = np.zeros((wn, 3))
jer = []
for it in range(wn):
    hw = hfc_ponderada(X.iloc[it:it + NW].to_numpy())
    alt[it] = np.sort(hw["height"])[-3:][::-1]          # índices de los tres nodos superiores
    jer.append(hw)
fig, ax = plt.subplots(figsize=(7.4, 3.2))
sombrear(ax, fechas_c)
for k, (col, lab) in enumerate([(AZUL, "Nodo raíz"), (NARANJA, "Segundo nodo"), (VERDE, "Tercer nodo")]):
    ax.plot(range(wn), alt[:, k], color=col, lw=1.2, label=lab)
ax.axhline(0.7, color=ROJO, lw=1, ls="--")
ax.set_ylabel("Índice del nodo (λ2)")
ax.legend(frameon=False, ncol=3, loc="upper right", fontsize=8)
eje_anios(ax, fechas_c)
fig.tight_layout()
fig.savefig(SAL / "fig/camiz_claede_indices.png", dpi=200)
plt.close(fig)
raiz_c = pd.Series(alt[:, 0], index=fechas_c)
raiz_c.groupby(raiz_c.index.str[:4]).agg(["min", "mean", "max"]).round(2).to_csv(SAL / "claede_raiz_por_anio.csv")
comp = []
for s_ in ["2009-07", "2014-07", "2020-07", "2023-07"]:
    for k, cl in enumerate(particion_07(jer[fechas_c.index(s_)]), start=1):
        comp.append({"ventana": s_, "clase": k, "series": ", ".join(NOMBRE[X.columns[i - 1]] for i in sorted(cl))})
pd.DataFrame(comp).to_csv(SAL / "claede_composicion.csv", index=False)

sel = ["2009-07", "2014-07", "2020-07", "2023-07"]
sel = [s for s in sel if s in fechas_c]
ymax = max(max(jer[fechas_c.index(s)]["height"]) for s in sel) * 1.05
fig, axs = plt.subplots(2, 2, figsize=(7.4, 7.0))
for ax, s in zip(axs.ravel(), sel):
    dibujar_dendrograma(ax, jer[fechas_c.index(s)], list(X.columns), ymax=ymax)
    ax.set_title(f"Ventana centrada en {s}", fontsize=8.5, loc="left")
    ax.set_ylabel("Índice" if ax in axs[:, 0] else "")
    ax.tick_params(axis="x", labelsize=6)
fig.tight_layout()
fig.savefig(SAL / "fig/camiz_claede_dendrogramas.png", dpi=200)
plt.close(fig)

n3 = [len(particion_07(j)) for j in jer]
resumen = {"inercia_jerarquia_pct": float(inercia.loc["Percent", "Hierarchy"]),
           "inercia_repr_pct": float(inercia.loc["Percent", "Repr_Var"]),
           "altura_raiz": float(h["hier"]["height"][-1]),
           "clases_corte_07": int(np.sum(np.asarray(h["hier"]["height"]) > 0.7)) + 1,
           "aede_k_ch": k_ch, "aede_cortes": " ".join(cortes),
           "aede_k_codo": k_codo, "aede_cortes_codo": " ".join(cortes_codo),
           "claede_ventanas": wn, "claede_clases_min": min(n3), "claede_clases_max": max(n3),
           "claede_clases_moda": int(pd.Series(n3).mode()[0]),
           "claede_prop_3clases": round(float(np.mean(np.array(n3) == 3)), 2),
           "aede_lambda1_min": float(ev.Dim_01.min()), "aede_lambda1_max": float(ev.Dim_01.max()),
           "fecha_lambda1_min": ev.Dim_01.idxmin()}
# ---------------------------------------------------------------- 5. Tramos del EPCA y perfiles
lim_t = [0] + [fechas_ev.index(c) for c in cortes] + [len(fechas_ev)]
tramos_ev = [(fechas_ev[a_], fechas_ev[b_ - 1]) for a_, b_ in zip(lim_t[:-1], lim_t[1:])]
C1 = pd.DataFrame(a["correlationlsq"][:, :, 0], index=fechas_ev, columns=X.columns)
tabla_tr = pd.DataFrame({"Serie": [NOMBRE[c] for c in X.columns]})
for k, (x, y) in enumerate(tramos_ev, start=1):
    tabla_tr[f"Tramo {k} ({x[:4]}–{y[:4]})"] = C1.loc[x:y].mean().round(2).to_numpy()
tabla_tr.to_csv(SAL / "camiz_aede_corr_tramos.csv", index=False, float_format="%.2f")
for k, (x, y) in enumerate(tramos_ev):
    letra = "ABC"[k] if k < 3 else str(k)
    resumen[f"aede_l1_tramo{letra}"] = float(ev.Dim_01.loc[x:y].mean())
    resumen[f"aede_l2_tramo{letra}"] = float(ev.Dim_02.loc[x:y].mean())
resumen["aede_ventanas"] = len(fechas_ev)
for n in (25, 28, 29, 30):
    resumen[f"indice_nodo{n}"] = float(hi.loc[n, "Index"])

# Perfil económico de los regímenes de la datación con los scores del PCA
reg = pd.read_csv(RAIZ / "data/results/final/09a_regimenes_pca.csv")
cred = X[["Crédito empresarial", "Crédito consumo", "Crédito hipotecario"]].sum(axis=1)
anual = lambda s: 100 * (s / s.shift(12) - 1)
gc, gp, gi = anual(cred), anual(X["PBI desestacionalizado"]), anual(X["IPC Lima"])
filas = []
for i, r in enumerate(reg.itertuples(), start=1):
    m = (X.index >= r.inicio) & (X.index <= r.fin)
    tr_ = X.loc[m, "Tasa de referencia"]
    filas.append({"N.º": i, "Período": f"{r.inicio} a {r.fin}", "Meses": r.meses,
                  "Crédito (% anual)": round(gc[m].mean(), 1), "PBI (% anual)": round(gp[m].mean(), 1),
                  "Inflación (%)": round(gi[m].mean(), 1),
                  "Tasa de referencia (%)": f"{tr_.iloc[0]:.2f} → {tr_.iloc[-1]:.2f}".replace(".", ","),
                  "EMBIG (pb)": int(round(X.loc[m, "EMBIG Perú"].mean())),
                  "Fase preliminar": r.fase})
pd.DataFrame(filas).to_csv(SAL / "perfil_regimenes.csv", index=False, float_format="%.1f")

pd.Series(resumen).to_csv(SAL / "camiz_resumen.csv", header=["valor"])
print(pd.Series(resumen))
print(tab.to_string(index=False))
print(tpart.to_string(index=False))
