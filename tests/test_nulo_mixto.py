"""Pruebas del nulo mixto por serie (decisión D8), de la deriva HAC (tarea D11 del plan de 3b) y
del sorteo de los inicios de bloque de la rama TS (D19)."""

import os

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from src.remuestreo import (nulo_tendencias, medidas_observadas, comprobar_inicios, indices_desde_inicios,
                            leer_inicios_nulo)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_FINAL = os.path.join(RAIZ, 'data', 'results', 'final')
from src.series_tiempo import t_hac_media, tratamiento_mixto, HAC_REZAGOS, UMBRAL_DERIVA


def _paseos(n=228, p=4, semilla=2026):
    rng = np.random.default_rng(semilla)
    D = rng.normal(size=(n - 1, p)) + np.array([0.3, 0.0, -0.1, 0.05])
    return np.vstack([np.zeros(p), np.cumsum(D, axis=0)]) + 10


def test_t_hac_igual_a_statsmodels():
    # Newey-West con núcleo de Bartlett, 12 rezagos y sin corrección: el mismo error estándar
    # que statsmodels (OLS sobre una constante, cov_type='HAC', use_correction=False)
    rng = np.random.default_rng(7)
    e = rng.normal(size=300)
    d = 0.2 + np.convolve(e, [1, 0.6, 0.3], mode='same')
    m, se, t = t_hac_media(d)
    ajuste = sm.OLS(d, np.ones(len(d))).fit(cov_type='HAC', cov_kwds={'maxlags': HAC_REZAGOS, 'use_correction': False})
    assert m == pytest.approx(ajuste.params[0], abs=1e-14)
    assert se == pytest.approx(ajuste.bse[0], rel=1e-12)
    assert t == pytest.approx(ajuste.tvalues[0], rel=1e-12)


def test_regla_de_tratamiento_d8():
    assert UMBRAL_DERIVA == 2.0 and HAC_REZAGOS == 12
    assert tratamiento_mixto('TS', 5.0, 'DS') == 'TS'
    assert tratamiento_mixto('DS', 2.01, 'TS') == 'con_deriva'
    assert tratamiento_mixto('DS', -2.01, 'TS') == 'con_deriva'
    assert tratamiento_mixto('DS', 2.0, 'TS') == 'sin_deriva'          # |t| > 2 estricto
    assert tratamiento_mixto('indeterminada', 3.0, 'TS') == 'TS'
    assert tratamiento_mixto('indeterminada', 3.0, 'DS') == 'con_deriva'
    assert tratamiento_mixto('indeterminada', 1.0, 'DS') == 'sin_deriva'
    with pytest.raises(AssertionError):
        tratamiento_mixto('DS', 1.0, 'otra')


def test_mixto_sin_ts_reproduce_las_versiones_globales():
    X = _paseos()
    rng = np.random.default_rng(1)
    ini = rng.integers(1, 227 - 12 + 2, size=(5, X.shape[1], 19))
    assert np.array_equal(nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['con_deriva'] * 4),
                          nulo_tendencias(X, ini, 12, 'con_deriva'))
    assert np.array_equal(nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['sin_deriva'] * 4),
                          nulo_tendencias(X, ini, 12, 'sin_deriva'))


def test_ts_con_bloques_consecutivos_reproduce_la_serie():
    # Con inicios 1, 13, 25, ... la recta más los residuos remuestreados es la serie observada
    X = _paseos()
    ini_ts = np.tile(np.arange(1, 229, 12), (2, X.shape[1], 1))             # 1, 13, ..., 217 (19 bloques)
    ini = np.ones_like(ini_ts)                                              # incrementos: no se usan
    S = nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['TS'] * 4, inicios_ts=ini_ts)
    assert np.allclose(S, medidas_observadas(X)[None, :], atol=1e-10)


def test_tratamientos_invalidos():
    X = _paseos()
    ini = np.ones((1, 4, 19), dtype=int)
    with pytest.raises(AssertionError):
        nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['TS'] * 3)
    with pytest.raises(AssertionError):
        nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['TS', 'DS', 'TS', 'TS'])


# ---- D19: inicios de la rama TS en {1, ..., n − L + 1} -------------------------------------------

def test_ts_exige_inicios_propios():
    # El mixto con alguna serie TS no corre sin inicios_ts (D19); sin series TS no los necesita
    X = _paseos()
    ini = np.ones((1, 4, 19), dtype=int)
    with pytest.raises(AssertionError):
        nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['TS', 'con_deriva', 'sin_deriva', 'TS'])
    nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['con_deriva'] * 4)


def test_rango_de_inicios_por_rama():
    # Incrementos (n − 1 = 227 filas): el último inicio válido es 216; residuos (n = 228): 217
    n, L = 228, 12
    comprobar_inicios(np.full((1, 19), n - 1 - L + 1), n - 1, L)
    with pytest.raises(AssertionError):
        comprobar_inicios(np.full((1, 19), n - L + 1), n - 1, L)
    comprobar_inicios(np.full((1, 19), n - L + 1), n, L)
    with pytest.raises(AssertionError):
        comprobar_inicios(np.full((1, 19), n - L + 2), n, L)
    with pytest.raises(AssertionError):
        comprobar_inicios(np.zeros((1, 19), dtype=int), n, L)


def test_ultimo_inicio_usa_el_residuo_del_ultimo_mes():
    # Con todos los inicios en n − L + 1 = 217, cada bloque son los residuos de los meses 217..228:
    # la serie TS simulada es la recta más esos residuos repetidos, y el del último mes entra
    X = _paseos()
    n, L = X.shape[0], 12
    assert indices_desde_inicios([n - L + 1], L, n)[-1] == n - 1          # fila 0-based del último mes
    ini = np.ones((1, 4, 19), dtype=int)
    ini_ts = np.full((1, 4, 19), n - L + 1)
    S = nulo_tendencias(X, ini, L, 'mixto', tratamiento=['TS'] * 4, inicios_ts=ini_ts)
    t = np.arange(1, n + 1, dtype=float)
    A = np.column_stack([np.ones(n), t])
    coef, *_ = np.linalg.lstsq(A, X, rcond=None)
    rect = A @ coef
    res = X - rect
    M = rect + np.tile(res[n - L:], (19, 1))[:n]
    assert np.allclose(S[0], medidas_observadas(M), atol=1e-12)
    with pytest.raises(AssertionError):
        nulo_tendencias(X, ini, L, 'mixto', tratamiento=['TS'] * 4, inicios_ts=np.full((1, 4, 19), n - L + 2))


@pytest.mark.skipif(not os.path.exists(os.path.join(DIR_FINAL, 'R_nulo_indices_ts.csv')),
                    reason='falta R_nulo_indices_ts.csv: renderizar R/ciclo_financiero_final.Rmd')
def test_sorteo_del_rmd_alcanza_el_ultimo_inicio():
    # Los inicios que sortea el Rmd (semilla 2026): los de la rama TS cubren {1, ..., 217}, incluido
    # el último inicio posible; los de los incrementos, {1, ..., 216}
    p = 16
    ini = leer_inicios_nulo(os.path.join(DIR_FINAL, 'R_nulo_indices.csv'), p)
    ini_ts = leer_inicios_nulo(os.path.join(DIR_FINAL, 'R_nulo_indices_ts.csv'), p)
    assert ini.shape == (1000, p, 19) and ini_ts.shape == (1000, p, 19)
    comprobar_inicios(ini, 227, 12)
    comprobar_inicios(ini_ts, 228, 12)
    assert ini.max() == 216 and ini_ts.max() == 217
    assert set(np.unique(ini_ts)) == set(range(1, 218))
    # El último inicio se sortea en cada serie (no solo en alguna)
    assert all((ini_ts[:, j, :] == 217).any() for j in range(p))
