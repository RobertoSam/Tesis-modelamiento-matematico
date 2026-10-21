"""Partición óptima de series ordenadas en el tiempo (datación de regímenes).

Módulo previsto en el plan de la iteración 3a (sección 7, desarrollador, punto 1). La
recurrencia de Fisher (1958) ya está portada desde R en `src/camiz_port.py` (`fisher`), con
paridad verificada en `tests/test_camiz_port.py`. Este módulo no la reimplementa: la envuelve
para devolver la partición en términos de fechas y etiquetas de régimen, que es la forma en que
la usan los notebooks de datación. Sin dependencia de `torch`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.camiz_port import fisher


def particion_fisher(y, k, maxcl=None):
    """Partición óptima de Fisher de una serie ordenada en `k` clases contiguas.

    Parámetros
    ----------
    y : array-like o pd.Series
        Serie ordenada (por ejemplo, una componente principal mensual). Si es una Series, su
        índice se usa para fechar los cortes.
    k : int
        Número de clases contiguas (regímenes), con 1 <= k <= len(y).
    maxcl : int, opcional
        Número máximo de clases que calcula la recurrencia (por defecto, `k`).

    Devuelve
    --------
    dict con:
        'etiquetas' : np.ndarray de enteros 1..k, la clase de cada observación;
        'limites'   : lista de límites superiores 1-based de las k clases (el último es n);
        'cortes'    : etiquetas del índice donde empieza cada clase 2..k (o posiciones 0-based
                      si `y` no tiene índice);
        'sce'       : suma de cuadrados intra-clase de la partición óptima en k clases.
    """
    serie = y if isinstance(y, pd.Series) else pd.Series(np.asarray(y, dtype=float))
    n = len(serie)
    if not 1 <= k <= n:
        raise ValueError(f"k debe estar entre 1 y {n}; se recibió {k}")
    maxcl = k if maxcl is None else maxcl
    if maxcl < k:
        raise ValueError("maxcl no puede ser menor que k")

    valores = serie.to_numpy(dtype=float)
    if k == 1:
        # Una sola clase: no hay cortes; la SCE es la de toda la serie
        sce = float(((valores - valores.mean()) ** 2).sum())
        return {"etiquetas": np.ones(n, dtype=int), "limites": [n], "cortes": [], "sce": sce}

    # fisher exige maxcl >= 2 para construir los límites de k >= 2
    res = fisher(valores, max(maxcl, 2))
    limites = [int(v) for v in res["mod1out"][k - 1, :k]]

    # Etiquetas: la clase c ocupa las posiciones (limite_{c-1}, limite_c] en 1-based
    etiquetas = np.empty(n, dtype=int)
    inicio = 0
    for c, lim in enumerate(limites, start=1):
        etiquetas[inicio:lim] = c
        inicio = lim

    # Comienzo de cada clase 2..k, en las etiquetas del índice de la serie
    cortes = [serie.index[lim] for lim in limites[:-1]]
    return {"etiquetas": etiquetas, "limites": limites, "cortes": cortes,
            "sce": float(res["criter"][k - 1])}
