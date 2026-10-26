"""Pruebas de src/nulo_estructura.py (iteración 3b, tarea D7)."""

import numpy as np
import pandas as pd

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
    assert len(rv) == (80 - 24 + 1) - 24 and rv.rv.between(0, 1 + 1e-12).all()
    assert rr.n_pares.iloc[0] == len(rv)
