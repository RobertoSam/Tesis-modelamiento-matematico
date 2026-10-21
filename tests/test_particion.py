"""Pruebas de src/particion.py: la partición de Fisher coincide con la búsqueda exhaustiva."""

import itertools

import numpy as np
import pandas as pd

from src.particion import particion_fisher


def _sce(y):
    # Suma de cuadrados intra-clase de un tramo
    return float(((y - y.mean()) ** 2).sum())


def _fuerza_bruta(y, k):
    # Recorre todas las posiciones de corte y devuelve la mínima SCE total
    n = len(y)
    mejor = np.inf
    for cortes in itertools.combinations(range(1, n), k - 1):
        bordes = (0,) + cortes + (n,)
        total = sum(_sce(y[a:b]) for a, b in zip(bordes[:-1], bordes[1:]))
        mejor = min(mejor, total)
    return mejor


def test_coincide_con_fuerza_bruta():
    rng = np.random.default_rng(20261021)
    for _ in range(30):
        n = int(rng.integers(6, 13))
        y = rng.normal(size=n).cumsum()
        for k in (2, 3, 4):
            res = particion_fisher(y, k)
            assert np.isclose(res["sce"], _fuerza_bruta(y, k), atol=1e-9)
            # La SCE informada es la de las etiquetas devueltas
            sce_etiq = sum(_sce(y[res["etiquetas"] == c]) for c in range(1, k + 1))
            assert np.isclose(res["sce"], sce_etiq, atol=1e-9)
            # Las clases son contiguas y crecientes
            assert np.all(np.diff(res["etiquetas"]) >= 0)
            assert res["limites"][-1] == n


def test_cortes_en_fechas():
    idx = pd.period_range("2010-01", periods=12, freq="M")
    y = pd.Series([0.0] * 4 + [5.0] * 4 + [10.0] * 4, index=idx)
    res = particion_fisher(y, 3)
    assert res["cortes"] == [idx[4], idx[8]]
    assert np.isclose(res["sce"], 0.0)


def test_una_clase():
    y = np.array([1.0, 2.0, 3.0])
    res = particion_fisher(y, 1)
    assert res["cortes"] == [] and np.isclose(res["sce"], 2.0)
