"""Figura del Capítulo 3: esquema del modelo (diagrama, sin datos)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SAL = Path(__file__).resolve().parent / "fig"
SAL.mkdir(exist_ok=True)
AZUL, NARANJA, TINTA, TINTA2 = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 300, "savefig.bbox": "tight"})


def caja(ax, x, y, w, h, titulo, detalle="", fc="white", ec=TINTA2, oe=""):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=fc, edgecolor=ec, linewidth=1.1))
    ax.text(x + w / 2, y + h - 0.22, titulo, ha="center", va="top", fontsize=8.5, fontweight="bold", color=TINTA)
    if detalle:
        ax.text(x + w / 2, y + h - 0.55, detalle, ha="center", va="top", fontsize=7.5, color=TINTA)
    if oe:
        ax.text(x + w, y + h + 0.06, oe, ha="right", va="bottom", fontsize=7, color=AZUL, fontweight="bold")


def flecha(ax, x1, y1, x2, y2, color=TINTA2, estilo="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=estilo, color=color, linewidth=1.1, shrinkA=0, shrinkB=0))


fig, ax = plt.subplots(figsize=(7.4, 5.4))
ax.set_xlim(0, 12); ax.set_ylim(0, 9); ax.axis("off")

caja(ax, 3.6, 7.65, 4.8, 1.25, "Datos", "16 indicadores mensuales del BCRP\n2007-01 a 2025-12, estandarizados", fc="#f0efec")
caja(ax, 0.3, 5.9, 3.7, 1.4, "Representación global", "PCA (d = 3)\nHFC (corte en 0,7)", oe="OE1")
caja(ax, 4.2, 5.9, 3.7, 1.4, "Representación evolutiva", "EPCA y HFC evolutiva\nw = 48, ν = 3", oe="OE2")
caja(ax, 8.1, 5.9, 3.6, 1.4, "Representación no lineal", "Autoencoder\nAutoencoder LSTM")
caja(ax, 8.1, 3.9, 3.6, 1.3, "Comparación con el PCA", "Error fuera de muestra\ny estabilidad entre semillas", oe="OE5")
caja(ax, 0.3, 3.9, 3.7, 1.3, "Trayectoria de posición", "Coordenadas F₁, F₂, F₃\n(media móvil de 12 meses)")
caja(ax, 4.2, 3.9, 3.7, 1.3, "Trayectoria de estructura", "Primer valor propio λ₁(t)")
caja(ax, 2.2, 1.9, 3.7, 1.3, "Segmentación temporal", "Partición de Fisher\nregla K* (reducción < 10 %)", oe="OE3")
caja(ax, 6.4, 1.9, 5.3, 1.3, "Validación", "Series de referencia simuladas\nRemuestreo por bloques y dentro de régimen",
     fc="#fdf0ea", ec=NARANJA)
caja(ax, 2.2, 0.05, 3.7, 1.3, "Regímenes", "Caracterización, fase\ny episodios documentados", fc="#cde2fb", ec=AZUL, oe="OE4")

flecha(ax, 6.0, 7.6, 2.15, 7.3); flecha(ax, 6.0, 7.6, 6.05, 7.3); flecha(ax, 6.0, 7.6, 9.9, 7.3)
flecha(ax, 2.15, 5.9, 2.15, 5.2); flecha(ax, 6.05, 5.9, 6.05, 5.2)
flecha(ax, 2.15, 3.9, 3.6, 3.2); flecha(ax, 6.05, 3.9, 4.6, 3.2)
flecha(ax, 4.05, 1.9, 4.05, 1.35)
flecha(ax, 6.4, 2.55, 5.9, 2.55, color=NARANJA)
flecha(ax, 9.9, 5.9, 9.9, 5.2)
flecha(ax, 9.9, 3.9, 9.9, 3.2, color=NARANJA)

fig.savefig(SAL / "c3_esquema_modelo.png")
print("c3_esquema_modelo.png")
