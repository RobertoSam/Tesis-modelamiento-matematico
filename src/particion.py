"""Partición óptima de series ordenadas en el tiempo (datación de regímenes).

Módulo previsto en el plan de la iteración 3a (sección 7, desarrollador, punto 1). La
recurrencia de Fisher (1958) ya está portada desde R en `src/camiz_port.py` (`fisher`), con
paridad verificada en `tests/test_camiz_port.py`. Este módulo no la reimplementa: la envuelve
para devolver la partición en términos de fechas y etiquetas de régimen, que es la forma en que
la usan los notebooks de datación. Sin dependencia de `torch`.

Tarea D2 de la iteración 3b: se añade la longitud mínima de segmento `n_min` (por defecto 1, que
reproduce el comportamiento anterior) y la partición de series multivariadas (n × q), que necesita
la datación PCA-MM12 del 09a (`tam_min = 12` en `datar`). La recurrencia multivariada con
longitud mínima es la traducción de `particion_fisher` del Rmd (chunk `funciones`), con el mismo
orden de operaciones: sumas acumuladas por columna con acumulador long double (`cumsum` de R),
`rowSums` de los cuadrados y primer mínimo (`which.min`).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.camiz_port import fisher


def _cumsum_ld(x, axis=0):
    # cumsum() de R: acumulador long double y resultado en double
    return np.cumsum(np.asarray(x, dtype=np.longdouble), axis=axis).astype(np.float64)


def fisher_multivariado(Y, k_max=8, n_min=6):
    """Partición óptima de Fisher de una serie ordenada (n × q) con segmentos de al menos
    `n_min` filas, para k = 1..k_max (traducción de `particion_fisher` del Rmd).

    Devuelve un dict k -> {'sce', 'cortes'}, donde 'cortes' son las posiciones 0-based del
    inicio de cada segmento 2..k. Solo aparecen los k factibles (k · n_min <= n).
    """
    Y = np.asarray(Y, dtype=float)
    if Y.ndim == 1:
        Y = Y[:, None]
    n = Y.shape[0]
    if n_min < 1:
        raise ValueError("n_min debe ser al menos 1")
    S1 = np.vstack([np.zeros(Y.shape[1]), _cumsum_ld(Y, axis=0)])
    # rowSums de R acumula en long double; luego cumsum
    filas2 = np.sum(np.asarray(Y, dtype=np.longdouble) ** 2, axis=1).astype(np.float64)
    S2 = np.concatenate([[0.0], _cumsum_ld(filas2)])

    def sce(i, j):
        # segmento de las filas i+1..j (1-based), es decir Y[i:j]
        s = S1[j] - S1[i]
        ss = float(np.sum(np.asarray(s * s, dtype=np.longdouble)))
        return S2[j] - S2[i] - ss / (j - i)

    D = np.full((k_max + 1, n + 1), np.inf)
    B = np.zeros((k_max + 1, n + 1), dtype=int)
    for j in range(n_min, n + 1):
        D[1, j] = sce(0, j)
    for k in range(2, k_max + 1):
        if k * n_min > n:
            break
        for j in range(k * n_min, n + 1):
            ini = np.arange((k - 1) * n_min, j - n_min + 1)
            costos = np.array([D[k - 1, i] + sce(i, j) for i in ini])
            pos = int(np.argmin(costos))            # primer mínimo, como which.min
            D[k, j] = costos[pos]
            B[k, j] = ini[pos]
    res = {}
    for k in range(1, k_max + 1):
        if not np.isfinite(D[k, n]):
            continue
        cortes, j = [], n
        for kk in range(k, 1, -1):
            i = int(B[kk, j])
            cortes.insert(0, i)
            j = i
        res[k] = {"sce": float(D[k, n]), "cortes": cortes}
    return res


def particion_fisher(y, k, maxcl=None, n_min=1):
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
    n_min : int, opcional
        Longitud mínima de cada clase (por defecto 1, sin restricción). Con `n_min = 1` y una
        serie univariada se usa `camiz_port.fisher`, como antes de la iteración 3b; en otro caso,
        `fisher_multivariado`. Se exige k · n_min <= n.

    Devuelve
    --------
    dict con:
        'etiquetas' : np.ndarray de enteros 1..k, la clase de cada observación;
        'limites'   : lista de límites superiores 1-based de las k clases (el último es n);
        'cortes'    : etiquetas del índice donde empieza cada clase 2..k (o posiciones 0-based
                      si `y` no tiene índice);
        'sce'       : suma de cuadrados intra-clase de la partición óptima en k clases.
    """
    if isinstance(y, pd.DataFrame) or np.asarray(y).ndim == 2:
        return _particion_general(y, k, maxcl, n_min)
    serie = y if isinstance(y, pd.Series) else pd.Series(np.asarray(y, dtype=float))
    if n_min != 1:
        return _particion_general(serie, k, maxcl, n_min)
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


def _particion_general(y, k, maxcl, n_min):
    # Partición con longitud mínima y/o datos multivariados (fisher_multivariado)
    indice = y.index if isinstance(y, (pd.Series, pd.DataFrame)) else None
    valores = np.asarray(y, dtype=float)
    if valores.ndim == 1:
        valores = valores[:, None]
    n = valores.shape[0]
    if not 1 <= k <= n:
        raise ValueError(f"k debe estar entre 1 y {n}; se recibió {k}")
    maxcl = k if maxcl is None else maxcl
    if maxcl < k:
        raise ValueError("maxcl no puede ser menor que k")
    if k * n_min > n:
        raise ValueError(f"k · n_min = {k * n_min} supera n = {n}")
    res = fisher_multivariado(valores, k_max=maxcl, n_min=n_min)[k]
    bordes = [0] + res["cortes"] + [n]
    etiquetas = np.empty(n, dtype=int)
    for c, (a, b) in enumerate(zip(bordes[:-1], bordes[1:]), start=1):
        etiquetas[a:b] = c
    cortes = [indice[c] for c in res["cortes"]] if indice is not None else list(res["cortes"])
    return {"etiquetas": etiquetas, "limites": bordes[1:], "cortes": cortes, "sce": res["sce"]}
