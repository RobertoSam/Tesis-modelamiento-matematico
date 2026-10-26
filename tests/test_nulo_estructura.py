"""Pruebas de src/nulo_estructura.py (iteración 3b, tarea D7)."""

import numpy as np
import pandas as pd
import pytest

from src import nulo_estructura as ne


def _datos(n=60, p=4, semilla=2026):
    rng = np.random.default_rng(semilla)
    return pd.DataFrame(rng.normal(size=(n, p)).cumsum(axis=0), index=[f"t{i}" for i in range(n)],
                        columns=[f"v{j}" for j in range(p)])


def test_bloques_consecutivos_reproducen_la_serie():
    # Con inicios 1, 1 + L, 1 + 2L, ... el remuestreo devuelve la serie original (filas) o la serie
    # menos su primer valor (incrementos acumulados desde 0)
    M = _datos()
    L = 12
    ini_f = np.arange(1, 60, L)                       # 60 filas
    assert np.allclose(ne.serie_nula(M, "transformadas", ini_f, L).to_numpy(), M.to_numpy())
    ini_d = np.arange(1, 59, L)                       # 59 incrementos
    nula = ne.serie_nula(M, "niveles", ini_d, L).to_numpy()
    assert np.allclose(nula, M.to_numpy() - M.to_numpy()[0], atol=1e-12)


def test_bloque_conjunto_conserva_la_correlacion_contemporanea():
    # Las mismas filas para todas las series: cada fila remuestreada es una fila observada completa
    M = _datos()
    nula = ne.serie_nula(M, "transformadas", np.array([30, 1, 45, 10, 20]), 12).to_numpy()
    filas = {tuple(f) for f in M.to_numpy()}
    assert all(tuple(f) in filas for f in nula)


def test_medir_devuelve_la_grilla_completa():
    M = _datos(n=80)
    k, rv, rr = ne.medir(M, nw_grilla=(24,), pesos={"uniformes": 0}, maxcl=5)
    assert len(k) == 3 and set(k.criterio) == {c for c, _ in ne.CRITERIOS}
    n_pares = (80 - 24 + 1) - 24
    assert len(rv) == 2 * n_pares and set(rv.objeto) == set(ne.OBJETOS_D17)
    assert rv.rv.between(0, 1 + 1e-12).all()
    assert (rr.n_pares == n_pares).all() and len(rr) == 2
    # Frontera: primer mes de la segunda ventana del par (fila i + nw)
    assert list(rv.frontera[:3]) == [M.index[24], M.index[25], M.index[26]]


def test_rv_correlacion_y_cargas_completas():
    # Con todas las cargas (p ejes), el RV de las cargas sin centrar es el de las correlaciones,
    # porque C Cᵀ = R (src.dinamica)
    from src.dinamica import rv_correlacion
    from src.multivariado import coef_rv
    rng = np.random.default_rng(3)
    Ra = np.corrcoef(rng.normal(size=(40, 5)), rowvar=False)
    Rb = np.corrcoef(rng.normal(size=(40, 5)), rowvar=False)
    def cargas(R):
        val, vec = np.linalg.eigh(R)
        return vec * np.sqrt(np.clip(val, 0, None))
    assert rv_correlacion(Ra, Rb) == pytest.approx(coef_rv(cargas(Ra), cargas(Rb), centrar=False), abs=1e-12)
    assert rv_correlacion(Ra, Ra) == pytest.approx(1.0, abs=1e-15)


def test_antecedente_conserva_rv_centrado():
    from src.multivariado import coef_rv
    from src import camiz_port as cp
    M = _datos(n=80)
    _, rv, _ = ne.medir(M, nw_grilla=(24,), pesos={"uniformes": 0}, maxcl=5, objetos_rv=ne.OBJETOS_ANTECEDENTE)
    C = cp.aede(M, nw=24, ndim=3, nsd=0, maxcl=5)['correlationlsq']
    assert set(rv.objeto) == {'cargas_centradas'}
    assert rv.rv.iloc[0] == coef_rv(C[0], C[24])
