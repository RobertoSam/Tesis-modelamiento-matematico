# -*- coding: utf-8 -*-
"""Sensibilidad de la datación con scores al retardo de la media móvil causal (revisión N6).

Repite la datación del notebook 09a (scores del PCA con la regla de signo de Rcamiz, d = 3,
Fisher multivariado, tramos de al menos 12 meses, regla K de D12 con maxcl = 10) con una media
móvil CENTRADA de 12 meses en lugar de la causal, y mide la distancia de cada corte al episodio
de referencia más cercano. La versión causal sigue siendo la principal (D12): esto es sensibilidad.

Uso, desde la raíz del repositorio:
    python3 tesis/informe_preliminar_uni/sensibilidad_media_movil.py
Salida: data/results/final/informe_uni/sensibilidad_media_movil.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
from src import particion as pt                     # noqa: E402
from src.datos import cargar_vias                   # noqa: E402
from src.parametros import leer_parametros          # noqa: E402

L, D, MAXCL, NMIN, UMBRAL = 12, 3, 10, 12, 0.10
PAR = leer_parametros(RAIZ)
X, _ = cargar_vias(RAIZ, excluidas=PAR["EXCLUIDAS"])
_, _, S = pt.scores_pca_rcamiz(X.to_numpy())
fechas = list(X.index)
epis = pd.read_csv(RAIZ / "data/referencia/episodios_referencia.csv", dtype=str).fillna("")


def a_mes(f):
    return int(f[:4]) * 12 + int(f[5:7]) - 1


def distancia(f):
    """Distancia en meses al intervalo [inicio, fin] del episodio más cercano (0 si cae dentro)."""
    m = a_mes(f)
    mejor = (10 ** 6, "")
    for e in epis.itertuples():
        a, b = a_mes(e.inicio), a_mes(e.fin or e.inicio)
        dist = 0 if a <= m <= b else min(abs(m - a), abs(m - b))
        mejor = min(mejor, (dist, e.nombre))
    return mejor


def media_movil_centrada(x, w):
    """Media de w meses centrada: para w par, promedio de las medias causales en t + 5 y t + 6."""
    c = pt.media_movil_causal(x, w)
    r = np.full(len(x), np.nan)
    a, b = w // 2 - 1, w // 2              # desplazamientos de 5 y 6 meses para w = 12
    r[:len(x) - b] = 0.5 * (c[a:len(x) - b + a] + c[b:])
    return r


filas = []
for version, suav in [("causal (principal)", pt.media_movil_causal), ("centrada", media_movil_centrada)]:
    Sm = np.column_stack([suav(S[:, k], L) for k in range(D)])
    ok = ~np.isnan(Sm).any(axis=1)
    fz = [f for f, o in zip(fechas, ok) if o]
    dat = pt.datar(Sm[ok], k_max=MAXCL, n_min=NMIN, umbral=UMBRAL)
    for c in pt.fechas_corte(dat["res"][dat["k_codo"]]["cortes"], fz):
        dist, nombre = distancia(c)
        filas.append({"version": version, "k": dat["k_codo"], "corte": c, "episodio_mas_cercano": nombre,
                      "distancia_meses": dist, "compatible_3": dist <= 3, "compatible_6": dist <= 6})
out = pd.DataFrame(filas)
dest = RAIZ / "data/results/final/informe_uni"
dest.mkdir(parents=True, exist_ok=True)
out.to_csv(dest / "sensibilidad_media_movil.csv", index=False)
print(out.to_string(index=False))
