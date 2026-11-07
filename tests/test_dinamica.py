"""Pruebas de src/dinamica.py (criterio de OE4 de D17.2 y lectura de 2017-10 de D13 y D17.3)."""

import numpy as np
import pandas as pd
import pytest

from src import dinamica as dn
from src.episodios import cargar_episodios


def test_criterio_oe4_dejando_fuera():
    rng = np.random.default_rng(1)
    R = rng.uniform(0.5, 1, size=(30, 12))
    obs = R[0].copy()
    r = dn.criterio_oe4(obs, R)
    assert np.allclose(r['p5'], np.quantile(R, 0.05, axis=0))
    assert r['prop_obs'] == pytest.approx(np.mean(obs < r['p5']))
    # La proporción de la réplica b usa el p5 de las otras 29
    b = 7
    p5_b = np.quantile(np.delete(R, b, axis=0), 0.05, axis=0)
    assert r['props_nulo'][b] == pytest.approx(np.mean(R[b] < p5_b))
    assert r['p_valor'] == pytest.approx(np.mean(r['props_nulo'] >= r['prop_obs']))
    # Un perfil observado muy bajo queda bajo el p5 en todas las posiciones y fuera del nulo
    bajo = dn.criterio_oe4(np.zeros(12), R)
    assert bajo['prop_obs'] == 1.0 and bajo['p_valor'] == 0.0


def test_fuera_del_nulo_y_tabla_2017_10():
    e = cargar_episodios()
    pares = pd.DataFrame({'objeto': 'cargas_sin_centrar', 'nw': 36, 'pesos': 'uniformes',
                          'frontera': ['2017-06', '2017-09', '2018-02'], 'bajo_p5': [False, True, False]})
    assert dn.fuera_del_nulo('2017-10', pares) == (True, 1, 1)
    assert dn.fuera_del_nulo('2017-08', pares) == (True, 2, 1)
    assert dn.fuera_del_nulo('2016-01', pares) == (False, 0, 0)
    pg = pares.assign(pesos='gaussianos_nsd3')
    p48 = pares.assign(nw=48)
    cand = pd.DataFrame({'metodo': ['regla 06 (PC2)', 'aede codo', 'aede codo'], 'nw': [36, 48, 36],
                         'pesos': ['uniformes', 'uniformes', 'gaussianos_nsd3'],
                         'fecha': ['2017-10', '2017-11', '2017-09']})
    m = dn.marcar_transiciones(cand, pd.concat([pares, pg, p48]), e)
    t, res = dn.tabla_2017_10(m)
    assert len(t) == 12
    # La clasificación depende solo de las marcas: se reconstruye a mano
    cuenta = m[(~m.es_borde_3) & m.fuera_del_nulo]
    anchos_u = set(cuenta.nw[cuenta.pesos == 'uniformes'])
    esperado = 'confirmada' if len(anchos_u) >= 2 and (cuenta.pesos == 'gaussianos_nsd3').any() else 'transición no confirmada'
    assert res['clasificacion'] == esperado
    # Sin candidatos: no confirmada
    t0, r0 = dn.tabla_2017_10(m.iloc[0:0])
    assert r0['clasificacion'] == 'transición no confirmada' and not t0.candidato.any()
