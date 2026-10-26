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


# ---- Tarea D2 (iteración 3b): longitud mínima de segmento y datos multivariados ----

from src.particion import fisher_multivariado


def _sce_m(Y):
    # Suma de cuadrados intra-clase de un tramo multivariado
    return float(((Y - Y.mean(axis=0)) ** 2).sum())


def _fuerza_bruta_nmin(Y, k, n_min):
    # Mínima SCE total entre todas las particiones en k tramos de al menos n_min filas
    n = len(Y)
    mejor, arg = np.inf, None
    for cortes in itertools.combinations(range(1, n), k - 1):
        bordes = (0,) + cortes + (n,)
        if min(b - a for a, b in zip(bordes[:-1], bordes[1:])) < n_min:
            continue
        total = sum(_sce_m(Y[a:b]) for a, b in zip(bordes[:-1], bordes[1:]))
        if total < mejor - 1e-12:
            mejor, arg = total, list(cortes)
    return mejor, arg


def test_nmin_coincide_con_fuerza_bruta():
    rng = np.random.default_rng(20261024)
    casos = 0
    for _ in range(40):
        n = int(rng.integers(8, 15))
        q = int(rng.integers(1, 4))
        Y = rng.normal(size=(n, q)).cumsum(axis=0)
        for n_min in (1, 2, 3, 4):
            res = fisher_multivariado(Y, k_max=4, n_min=n_min)
            for k in range(1, 5):
                if k * n_min > n:
                    assert k not in res
                    continue
                sce_bf, _ = _fuerza_bruta_nmin(Y, k, n_min)
                assert np.isclose(res[k]["sce"], sce_bf, atol=1e-9)
                bordes = [0] + res[k]["cortes"] + [n]
                largos = np.diff(bordes)
                assert largos.min() >= n_min
                assert np.isclose(sum(_sce_m(Y[a:b]) for a, b in zip(bordes[:-1], bordes[1:])),
                                  res[k]["sce"], atol=1e-9)
                casos += 1
    assert casos > 400


def test_nmin_1_reproduce_comportamiento_anterior():
    # Con n_min = 1 y datos univariados, la vía general da la misma SCE y los mismos cortes
    rng = np.random.default_rng(7)
    for _ in range(20):
        y = rng.normal(size=int(rng.integers(6, 30))).cumsum()
        for k in (2, 3, 4):
            a = particion_fisher(y, k, maxcl=6)
            b = particion_fisher(y[:, None], k, maxcl=6)
            assert np.isclose(a["sce"], b["sce"], atol=1e-9)
            assert list(a["cortes"]) == list(b["cortes"])
            assert np.array_equal(a["etiquetas"], b["etiquetas"])


def test_nmin_fechas_y_errores():
    idx = pd.period_range("2010-01", periods=12, freq="M")
    y = pd.Series([0.0] * 2 + [5.0] * 10, index=idx)
    # Sin restricción el corte cae en el mes 3; con n_min = 4 debe correrse al mes 5
    assert particion_fisher(y, 2)["cortes"] == [idx[2]]
    assert particion_fisher(y, 2, n_min=4)["cortes"] == [idx[4]]
    import pytest
    with pytest.raises(ValueError):
        particion_fisher(y, 4, n_min=4)


# ---- Tarea D3 (iteración 3b): datación PCA-MM12 -------------------------------------

from src.particion import media_movil_causal, datar, grilla_datacion


def test_media_movil_causal_como_rolling():
    rng = np.random.default_rng(3)
    x = rng.normal(size=40)
    r = media_movil_causal(x, 12)
    esperado = pd.Series(x).rolling(12).mean().to_numpy()
    assert np.all(np.isnan(r[:11])) and np.allclose(r[11:], esperado[11:], atol=1e-14)


def test_datar_regla_k_y_grilla():
    # Tres regímenes nítidos de 20 meses: la regla K (paso «umbral») elige 3 y corta en 20 y 40
    rng = np.random.default_rng(11)
    Y = np.repeat([[0.0, 0.0], [4.0, -4.0], [0.0, 4.0]], 20, axis=0) + 0.1 * rng.normal(size=(60, 2))
    d = datar(Y, k_max=4, n_min=12)
    assert d["k_codo"] == 3 and d["regla_codo"] == "umbral"
    assert d["res"][3]["cortes"] == [20, 40]
    assert d["k_max_efectivo"] == 4
    fechas = [f"2010-{m:02d}" for m in range(1, 13)] * 5
    g = grilla_datacion(Y, fechas, maxcls=(4, 5))
    assert set(g.criterio) == {"codo (caída máxima)", "Calinski-Harabász k gl (aede)",
                               "Calinski-Harabász k-1 gl (habitual)", "regla K (D12)"}
    # Con n_min = 12 y 60 filas, el mayor k factible es 5 aunque maxcl sea mayor
    assert (g.k_max_efectivo[g.maxcl == 5] == 5).all()
    assert (g.k_en_tope == (g.k == g.k_max_efectivo)).all()
