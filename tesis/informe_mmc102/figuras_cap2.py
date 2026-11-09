"""Figuras ilustrativas del Capítulo 2 (Marco teórico).

Todas las figuras usan datos simulados o fórmulas del propio capítulo: ilustran
conceptos, no son resultados de la tesis. Se guardan en tesis/informe_mmc102/fig/.
Uso: python3 tesis/informe_mmc102/figuras_cap2.py
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.ticker import FuncFormatter

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(RAIZ / "src"))
import camiz_port as cp  # noqa: E402  rutinas del asesor trasladadas a Python

SAL = AQUI / "fig"
SAL.mkdir(exist_ok=True)

# Paleta validada (slots 1–3) y tintas de texto
AZUL, NARANJA, VERDE = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA2, GRIS = "#0b0b0b", "#52514e", "#b9b8b2"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": TINTA2,
    "axes.labelcolor": TINTA, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.8,
    "lines.linewidth": 2, "savefig.dpi": 300, "savefig.bbox": "tight",
})
rng = np.random.default_rng(20261108)


def coma(ax, ejes="xy", dec=None):
    """Formato con coma decimal en los ejes indicados."""
    def f(v, _):
        s = f"{v:.{dec}f}" if dec is not None else f"{v:g}"
        return s.replace(".", ",").replace("-", "−")
    if "x" in ejes:
        ax.xaxis.set_major_formatter(FuncFormatter(f))
    if "y" in ejes:
        ax.yaxis.set_major_formatter(FuncFormatter(f))


def rotulo_panel(ax, letra):
    ax.text(-0.12, 1.04, letra, transform=ax.transAxes, fontsize=10, fontweight="bold", color=TINTA)


def guardar(fig, nombre):
    fig.savefig(SAL / nombre)
    plt.close(fig)
    print("  ", nombre)


# 1. Regresión espuria ------------------------------------------------------------
def fig_espuria():
    n = 228
    a = np.cumsum(rng.normal(0.3, 1, n))
    b = np.cumsum(rng.normal(0.3, 1, n))
    r_ab = np.corrcoef(a, b)[0, 1]
    # Distribución de |r| entre pares de series independientes
    rw = [abs(np.corrcoef(np.cumsum(rng.normal(size=n)), np.cumsum(rng.normal(size=n)))[0, 1]) for _ in range(2000)]
    rb = [abs(np.corrcoef(rng.normal(size=n), rng.normal(size=n))[0, 1]) for _ in range(2000)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.8))
    ax1.plot(a, color=AZUL); ax1.plot(b, color=NARANJA)
    ax1.text(120, a[120] + 4, "Serie A", color=TINTA, ha="center", va="bottom")
    ax1.text(110, b[110] - 8, "Serie B", color=TINTA, ha="center", va="top")
    ax1.set_xlabel("Mes"); ax1.set_ylabel("Valor")
    ax1.text(0.03, 0.95, f"r = {r_ab:.2f}".replace(".", ","), transform=ax1.transAxes, va="top", color=TINTA)
    bins = np.linspace(0, 1, 26)
    ax2.hist(rb, bins=bins, color=AZUL, alpha=0.85, edgecolor="white", linewidth=1, label="Ruido blanco")
    ax2.hist(rw, bins=bins, color=NARANJA, alpha=0.75, edgecolor="white", linewidth=1, label="Caminatas aleatorias")
    ax2.set_xlabel("|r| entre series independientes"); ax2.set_ylabel("Frecuencia")
    ax2.legend(frameon=False, loc="upper right")
    coma(ax1, "y"); coma(ax2, "x")
    rotulo_panel(ax1, "a"); rotulo_panel(ax2, "b")
    fig.tight_layout()
    guardar(fig, "c2_regresion_espuria.png")


# 2. Ganancia de la diferenciación ------------------------------------------------
def fig_ganancia():
    P = np.linspace(6, 120, 1000)
    g1 = (2 * np.sin(np.pi / P)) ** 2
    g12 = (2 * np.abs(np.sin(12 * np.pi / P))) ** 2
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.plot(P, g1, color=AZUL); ax.plot(P, g12, color=NARANJA, linewidth=1.6)
    ax.text(100, (2 * np.sin(np.pi / 100)) ** 2 + 0.15, "Primera diferencia", color=TINTA)
    ax.text(70, 2.6, "Diferencia interanual", color=TINTA)
    for p_ in (24, 96):
        ax.axvline(p_, color=GRIS, linewidth=0.8, linestyle="--")
    ax.text(25, 3.7, "2 años", color=TINTA2); ax.text(97, 3.7, "8 años", color=TINTA2)
    ax.set_xlabel("Período de la oscilación (meses)"); ax.set_ylabel("Factor sobre la varianza")
    ax.set_ylim(0, 4.1); ax.set_xlim(6, 120)
    coma(ax, "y")
    fig.tight_layout()
    guardar(fig, "c2_ganancia_diferenciacion.png")


# 3. Geometría del PCA ------------------------------------------------------------
def fig_pca():
    n = 300
    f = rng.normal(size=n)
    X = np.column_stack([f + 0.45 * rng.normal(size=n), 0.8 * f + 0.6 * rng.normal(size=n)])
    Z = (X - X.mean(0)) / X.std(0)
    R = Z.T @ Z / n
    lam, V = np.linalg.eigh(R)
    lam, V = lam[::-1], V[:, ::-1]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.3))
    ax1.scatter(Z[:, 0], Z[:, 1], s=9, color=GRIS, edgecolor="none")
    for k, col in ((0, AZUL), (1, NARANJA)):
        v = V[:, k] * np.sign(V[:, k].sum() if k == 0 else V[1, k]) * np.sqrt(lam[k]) * 2.2
        ax1.add_patch(FancyArrowPatch((0, 0), tuple(v), arrowstyle="-|>", mutation_scale=12, color=col, linewidth=2))
        ax1.text(v[0] * 1.08, v[1] * 1.08, f"Eje {k + 1}", color=TINTA, ha="center")
    ax1.set_aspect("equal"); ax1.set_xlabel("$z_1$"); ax1.set_ylabel("$z_2$")
    ax1.set_xlim(-3.6, 3.6); ax1.set_ylim(-3.6, 3.6)
    # Círculo de correlaciones con cargas ilustrativas
    th = np.linspace(0, 2 * np.pi, 300)
    ax2.plot(np.cos(th), np.sin(th), color=TINTA2, linewidth=0.8)
    ax2.axhline(0, color=GRIS, linewidth=0.6); ax2.axvline(0, color=GRIS, linewidth=0.6)
    cargas = {"V1": (0.93, 0.15), "V2": (0.88, 0.30), "V3": (0.10, 0.90), "V4": (-0.75, 0.40), "V5": (0.25, 0.20)}
    for nom, (x, y) in cargas.items():
        ax2.add_patch(FancyArrowPatch((0, 0), (x, y), arrowstyle="-|>", mutation_scale=10, color=AZUL, linewidth=1.6))
        ax2.text(x * 1.12, y * 1.12, nom, ha="center", va="center", color=TINTA)
    ax2.set_aspect("equal"); ax2.set_xlim(-1.15, 1.15); ax2.set_ylim(-1.15, 1.15)
    ax2.set_xlabel("Correlación con el eje 1"); ax2.set_ylabel("Correlación con el eje 2")
    coma(ax2)
    rotulo_panel(ax1, "a"); rotulo_panel(ax2, "b")
    fig.tight_layout()
    guardar(fig, "c2_pca_geometria.png")


# 4. HFC con la rutina del asesor -------------------------------------------------
def fig_hfc():
    n = 228
    f1, f2 = rng.normal(size=n), rng.normal(size=n)
    X = np.column_stack([
        f1 + 0.25 * rng.normal(size=n), f1 + 0.3 * rng.normal(size=n), f1 + 0.4 * rng.normal(size=n),
        f2 + 0.3 * rng.normal(size=n), -f2 + 0.35 * rng.normal(size=n), rng.normal(size=n)])
    nombres = ["V1", "V2", "V3", "V4", "V5", "V6"]
    res = cp.clahfac(X)
    H = res["hierar"].reset_index(drop=True)
    p = X.shape[1]
    # Coordenadas del dendrograma: hojas ordenadas por recorrido del árbol
    hijos = {int(r.Num) if False else p + 1 + i: (int(r.N1), int(r.N2)) for i, r in H.iterrows()}
    altura = {p + 1 + i: float(r.Index) for i, r in H.iterrows()}
    raiz = max(hijos)
    orden = []

    def recorrer(nodo):
        if nodo <= p:
            orden.append(nodo)
        else:
            a, b = hijos[nodo]; recorrer(a); recorrer(b)
    recorrer(raiz)
    xpos = {hoja: i for i, hoja in enumerate(orden)}

    def coord(nodo):
        if nodo <= p:
            return xpos[nodo], 0.0
        a, b = hijos[nodo]
        xa, ya = coord(a); xb, yb = coord(b); h = altura[nodo]
        return (xa + xb) / 2, h

    fig, ax = plt.subplots(figsize=(5.8, 3.2))
    for nodo, (a, b) in hijos.items():
        xa, ya = coord(a); xb, yb = coord(b); h = altura[nodo]
        ax.plot([xa, xa, xb, xb], [ya, h, h, yb], color=TINTA2, linewidth=1.2)
    ax.axhline(0.7, color=NARANJA, linestyle="--", linewidth=1.4)
    ax.text(len(orden) - 0.6, 0.72, "Corte en 0,7", color=TINTA, ha="right", va="bottom")
    ax.set_xticks(range(len(orden))); ax.set_xticklabels([nombres[h - 1] for h in orden])
    ax.set_ylabel("Índice del nodo"); ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    coma(ax, "y")
    fig.tight_layout()
    guardar(fig, "c2_hfc_dendrograma.png")
    print("     índices:", [round(v, 3) for v in H["Index"]])


# 5. Ventana móvil y pesos gaussianos ---------------------------------------------
def fig_ventana():
    w = 48
    pu, pg = cp.pesos_aede(w, 0), cp.pesos_aede(w, 3)
    r = np.arange(1, w + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.9), gridspec_kw={"width_ratios": [1.1, 1]})
    # Esquema de ventanas sucesivas
    for k, t0 in enumerate([0, 6, 12]):
        ax1.add_patch(Rectangle((t0, k), w, 0.6, facecolor=AZUL, alpha=0.25 + 0.2 * k, edgecolor="none"))
        ax1.plot(t0 + w / 2, k + 0.3, "o", color=TINTA, markersize=4)
    ax1.text(62, 2.3, "Centro de la ventana", color=TINTA, va="center", fontsize=8)
    ax1.set_xlim(0, 90); ax1.set_ylim(-0.4, 3.2); ax1.set_yticks([])
    ax1.spines["left"].set_visible(False); ax1.set_xlabel("Mes")
    # Pesos
    ax2.plot(r, pu, color=TINTA2, linewidth=1.6); ax2.plot(r, pg, color=AZUL)
    ax2.text(2, pu[0] + 0.002, "Uniformes (ν = 0)", color=TINTA, va="bottom")
    ax2.text(w / 2 + 3, pg.max(), "Gaussianos (ν = 3)", color=TINTA, va="top")
    ax2.set_xlabel("Posición en la ventana (r)"); ax2.set_ylabel("Peso ωᵣ")
    neff = 1 / np.sum(pg ** 2)
    ax2.text(0.03, 0.92, f"nω = {neff:.1f} meses".replace(".", ","), transform=ax2.transAxes, color=TINTA2)
    coma(ax2, "y", 3)
    rotulo_panel(ax1, "a"); rotulo_panel(ax2, "b")
    fig.tight_layout()
    guardar(fig, "c2_ventana_pesos.png")


# 6. Partición óptima de Fisher ---------------------------------------------------
def fisher_dp(y, kmax):
    """Programación dinámica de Fisher (1958) para una serie univariada."""
    n = len(y)
    c1, c2 = np.concatenate([[0], np.cumsum(y)]), np.concatenate([[0], np.cumsum(y ** 2)])

    def S(i, j):  # suma de cuadrados del intervalo i..j (0-based, inclusivo)
        m = j - i + 1; s = c1[j + 1] - c1[i]
        return c2[j + 1] - c2[i] - s * s / m
    D = np.full((n, kmax + 1), np.inf); arg = np.zeros((n, kmax + 1), dtype=int)
    for m in range(n):
        D[m, 1] = S(0, m)
    for k in range(2, kmax + 1):
        for m in range(k - 1, n):
            vals = [D[j - 1, k - 1] + S(j, m) for j in range(k - 1, m + 1)]
            j = int(np.argmin(vals)); D[m, k] = vals[j]; arg[m, k] = j + k - 1
    cortes = {}
    for k in range(1, kmax + 1):
        c, m = [], n - 1
        for kk in range(k, 1, -1):
            j = arg[m, kk]; c.append(j); m = j - 1
        cortes[k] = sorted(c)
    return D[n - 1, 1:], cortes


def fig_fisher():
    n = 180
    base = np.r_[np.full(60, 10.5), np.linspace(10.5, 8.0, 15), np.full(55, 8.0), np.full(50, 11.0)]
    y = np.convolve(base + rng.normal(0, 0.45, n), np.ones(7) / 7, mode="same")
    y[:3], y[-3:] = base[:3], base[-3:]
    scd, cortes = fisher_dp(y, 8)
    K = 3
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.8), gridspec_kw={"width_ratios": [1.5, 1]})
    ax1.plot(y, color=AZUL)
    lim = [0] + cortes[K] + [n]
    for a, b in zip(lim[:-1], lim[1:]):
        ax1.hlines(y[a:b].mean(), a, b - 1, color=NARANJA, linewidth=2)
    for c in cortes[K]:
        ax1.axvline(c, color=TINTA2, linestyle="--", linewidth=1)
    ax1.set_xlabel("t"); ax1.set_ylabel("Trayectoria yₜ")
    ax1.text(0.5, 0.55, "Media de cada tramo (K = 3)", transform=ax1.transAxes, color=TINTA, ha="center")
    ks = np.arange(1, 9)
    ax2.plot(ks, scd, color=AZUL, marker="o", markersize=5)
    ax2.set_xlabel("Número de tramos K"); ax2.set_ylabel("SCDₖ")
    ax2.set_xticks(ks)
    coma(ax1, "y"); coma(ax2, "y")
    rotulo_panel(ax1, "a"); rotulo_panel(ax2, "b")
    fig.tight_layout()
    guardar(fig, "c2_fisher.png")


# 7. Distribuciones de referencia del primer valor propio --------------------------
def fig_referencia():
    n, p, B = 228, 10, 1000

    def lam1(X):
        Z = (X - X.mean(0)) / X.std(0)
        return np.linalg.eigvalsh(Z.T @ Z / len(Z))[-1] / p
    l_rb = [lam1(rng.normal(size=(n, p))) for _ in range(B)]
    l_rw = [lam1(np.cumsum(rng.normal(size=(n, p)), axis=0)) for _ in range(B)]
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    bins = np.linspace(0, 0.8, 41)
    ax.hist(l_rb, bins=bins, color=AZUL, edgecolor="white", linewidth=1, label="Ruido blanco independiente")
    ax.hist(l_rw, bins=bins, color=NARANJA, alpha=0.8, edgecolor="white", linewidth=1, label="Caminatas aleatorias independientes")
    ax.set_xlabel("Proporción de inercia del primer eje (λ₁/p)"); ax.set_ylabel("Frecuencia")
    ax.legend(frameon=False)
    coma(ax, "x")
    fig.tight_layout()
    guardar(fig, "c2_referencia_simulada.png")
    print("     p95 ruido:", round(np.percentile(l_rb, 95), 3), "mediana caminatas:", round(np.median(l_rw), 3))


# 8. Bootstrap por bloques --------------------------------------------------------
def fig_bloques():
    n, ell = 48, 8
    nb = n // ell
    colores = [AZUL, NARANJA, VERDE, "#eda100", "#e87ba4", "#6250d6"]
    sel = rng.integers(0, n - ell + 1, nb)
    fig, ax = plt.subplots(figsize=(6.6, 2.0))
    for b in range(nb):
        ax.add_patch(Rectangle((b * ell, 1.2), ell, 0.6, facecolor=colores[b], edgecolor="white", linewidth=2))
    for k, s in enumerate(sel):
        ax.add_patch(Rectangle((k * ell, 0), ell, 0.6, facecolor="none", edgecolor=TINTA2, linewidth=1))
        ax.text(k * ell + ell / 2, 0.3, f"{s + 1}–{s + ell}", ha="center", va="center", fontsize=7, color=TINTA)
    ax.text(-1, 1.5, "Serie original", ha="right", va="center", color=TINTA)
    ax.text(-1, 0.3, "Réplica", ha="right", va="center", color=TINTA)
    ax.text(n / 2, 1.95, "Bloques de ℓ = 8 meses", ha="center", color=TINTA2)
    ax.set_xlim(-14, n + 1); ax.set_ylim(-0.2, 2.2); ax.axis("off")
    guardar(fig, "c2_bootstrap_bloques.png")


# 9. Clasificación de las redes neuronales -----------------------------------------
def caja(ax, x, y, w, h, texto, fc="white", ec=TINTA2, fs=8.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.04", facecolor=fc, edgecolor=ec, linewidth=1))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, color=TINTA, fontweight="bold" if bold else "normal")


def fig_taxonomia():
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5.6); ax.axis("off")
    ax.text(5.9, 5.3, "Arquitectura", ha="center", fontsize=9, fontweight="bold", color=TINTA)
    ax.text(0.75, 2.4, "Tipo de aprendizaje", ha="center", va="center", rotation=90, fontsize=9, fontweight="bold", color=TINTA)
    caja(ax, 3.1, 4.4, 2.9, 0.7, "Prealimentada", fc="#f0efec", bold=True)
    caja(ax, 6.2, 4.4, 2.9, 0.7, "Recurrente", fc="#f0efec", bold=True)
    caja(ax, 1.25, 2.9, 1.75, 1.3, "Supervisado", fc="#f0efec", bold=True, fs=8)
    caja(ax, 1.25, 0.6, 1.75, 2.1, "No\nsupervisado", fc="#f0efec", bold=True, fs=8)
    caja(ax, 3.1, 2.9, 2.9, 1.3, "Perceptrón multicapa\n(regresión,\nclasificación)", fs=8)
    caja(ax, 6.2, 2.9, 2.9, 1.3, "Red recurrente, LSTM\n(predicción\nde secuencias)", fs=8)
    caja(ax, 3.1, 0.6, 2.9, 2.1, "Autoencoder", fc="#cde2fb", ec=AZUL, bold=True)
    caja(ax, 6.2, 0.6, 2.9, 2.1, "Autoencoder LSTM", fc="#cde2fb", ec=AZUL, bold=True)
    ax.text(6.05, 0.25, "En azul, los modelos empleados en la investigación", ha="center", fontsize=7.5, color=TINTA2)
    guardar(fig, "c2_taxonomia_redes.png")


# 10. Arquitectura del autoencoder -------------------------------------------------
def fig_autoencoder():
    capas = [16, 9, 3, 9, 16]
    xs = [0, 1.6, 3.2, 4.8, 6.4]
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    pos = []
    for x, m in zip(xs, capas):
        ys = np.linspace(-m / 2, m / 2, m) * 0.32
        pos.append([(x, y) for y in ys])
    for a, b in zip(pos[:-1], pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                ax.plot([x1, x2], [y1, y2], color=GRIS, linewidth=0.3, zorder=1)
    for i, capa in enumerate(pos):
        col = AZUL if i == 2 else ("#f0efec" if i in (0, 4) else "white")
        for (x, y) in capa:
            ax.scatter(x, y, s=38, facecolor=col, edgecolor=TINTA2, linewidth=0.8, zorder=3)
    ax.text(0, -3.4, "Entrada\n$\\mathbf{z}_t\\in\\mathbb{R}^p$", ha="center", va="top", color=TINTA)
    ax.text(3.2, -3.4, "Representación\nlatente $\\in\\mathbb{R}^d$", ha="center", va="top", color=TINTA)
    ax.text(6.4, -3.4, "Reconstrucción\n$\\hat{\\mathbf{z}}_t\\in\\mathbb{R}^p$", ha="center", va="top", color=TINTA)
    ax.annotate("", xy=(3.0, 3.2), xytext=(0, 3.2), arrowprops=dict(arrowstyle="-|>", color=TINTA2))
    ax.annotate("", xy=(6.4, 3.2), xytext=(3.4, 3.2), arrowprops=dict(arrowstyle="-|>", color=TINTA2))
    ax.text(1.5, 3.35, "Codificador", ha="center", color=TINTA); ax.text(4.9, 3.35, "Decodificador", ha="center", color=TINTA)
    ax.set_xlim(-0.8, 7.2); ax.set_ylim(-4.6, 3.8); ax.axis("off")
    guardar(fig, "c2_autoencoder.png")


# 11. Celda LSTM ------------------------------------------------------------------
def fig_lstm():
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(FancyBboxPatch((1.2, 0.8), 7.4, 4.4, boxstyle="round,pad=0.05,rounding_size=0.2", facecolor="#fcfcfb", edgecolor=TINTA2))
    # Línea de la memoria
    ax.annotate("", xy=(9.6, 4.5), xytext=(0.2, 4.5), arrowprops=dict(arrowstyle="-|>", color=AZUL, linewidth=2))
    ax.text(0.2, 4.7, "$\\mathbf{c}_{t-1}$", color=TINTA); ax.text(9.3, 4.7, "$\\mathbf{c}_t$", color=TINTA)
    for x, s in ((3.0, "×"), (5.2, "+")):
        ax.add_patch(plt.Circle((x, 4.5), 0.25, facecolor="white", edgecolor=AZUL, linewidth=1.5, zorder=3))
        ax.text(x, 4.5, s, ha="center", va="center", fontsize=11, color=TINTA, zorder=4)
    compuertas = [(2.4, "$\\mathbf{f}_t$\nolvido", 3.0), (4.0, "$\\mathbf{i}_t$\nentrada", 5.2), (5.4, "$\\tilde{\\mathbf{c}}_t$\ncandidata", 5.2), (7.0, "$\\mathbf{o}_t$\nsalida", 7.6)]
    for x, txt, destino in compuertas:
        caja(ax, x - 0.55, 1.9, 1.1, 0.9, txt, fc="#cde2fb", ec=AZUL, fs=8)
        ax.annotate("", xy=(destino, 4.25 if destino != 7.6 else 2.9), xytext=(x, 2.8),
                    arrowprops=dict(arrowstyle="-|>", color=TINTA2, linewidth=1))
    ax.add_patch(plt.Circle((7.6, 3.2), 0.25, facecolor="white", edgecolor=AZUL, linewidth=1.5, zorder=3))
    ax.text(7.6, 3.2, "×", ha="center", va="center", fontsize=11, color=TINTA, zorder=4)
    ax.annotate("", xy=(7.6, 3.45), xytext=(7.6, 4.5), arrowprops=dict(arrowstyle="-|>", color=AZUL, linewidth=1))
    ax.annotate("", xy=(9.6, 1.3), xytext=(7.85, 3.1), arrowprops=dict(arrowstyle="-|>", color=TINTA2, linewidth=1.2))
    ax.text(9.3, 0.9, "$\\mathbf{h}_t$", color=TINTA)
    ax.annotate("", xy=(4.6, 1.2), xytext=(0.2, 1.2), arrowprops=dict(arrowstyle="-", color=TINTA2, linewidth=1.2))
    ax.text(0.2, 0.85, "$\\mathbf{h}_{t-1}$, $\\mathbf{u}_t$", color=TINTA)
    for x, _, _ in compuertas:
        ax.plot([x, x], [1.2, 1.9], color=TINTA2, linewidth=1)
    ax.plot([2.4, 7.0], [1.2, 1.2], color=TINTA2, linewidth=1.2)
    guardar(fig, "c2_celda_lstm.png")


if __name__ == "__main__":
    for f in (fig_espuria, fig_ganancia, fig_pca, fig_hfc, fig_ventana, fig_fisher,
              fig_referencia, fig_bloques, fig_taxonomia, fig_autoencoder, fig_lstm):
        f()
