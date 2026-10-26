"""Pruebas del nulo mixto por serie (decisión D8) y de la deriva HAC (tarea D11 del plan de 3b)."""

import numpy as np
import pytest
import statsmodels.api as sm

from src.remuestreo import nulo_tendencias, medidas_observadas
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
    ini = np.tile(np.arange(1, 228, 12)[:19], (2, X.shape[1], 1))
    S = nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['TS'] * 4)
    assert np.allclose(S, medidas_observadas(X)[None, :], atol=1e-10)


def test_tratamientos_invalidos():
    X = _paseos()
    ini = np.ones((1, 4, 19), dtype=int)
    with pytest.raises(AssertionError):
        nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['TS'] * 3)
    with pytest.raises(AssertionError):
        nulo_tendencias(X, ini, 12, 'mixto', tratamiento=['TS', 'DS', 'TS', 'TS'])
