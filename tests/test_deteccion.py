"""Pruebas de src/deteccion.py (anexo R.b: walk-forward del PCA sin torch)."""

import os

import numpy as np
import pandas as pd
import pytest

from src.datos import cargar_vias
from src.deteccion import error_walkforward_pca, discriminacion_larga, ampliar_episodios
from src.episodios import cargar_episodios, discriminacion_episodios

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.mark.parametrize('via,archivo', [('transformadas', 'data/results/09_walkforward_errores.csv'),
                                          ('niveles', 'data/results/niveles/09_walkforward_errores.csv')])
def test_reproduce_la_columna_pca_del_09_con_17_series(via, archivo):
    X, Xt = cargar_vias(RAIZ, excluidas=())
    M = Xt if via == 'transformadas' else X
    wf = error_walkforward_pca(M.to_numpy(), [f + '-01' for f in M.index])
    ref = pd.read_csv(os.path.join(RAIZ, archivo), index_col=0, parse_dates=True)
    assert (wf.index == ref.index).all()
    assert np.max(np.abs(wf.pca.to_numpy() - ref.pca.to_numpy())) < 1e-10


def test_discriminacion_larga_con_tolerancia_0_es_la_regla_del_09():
    e = cargar_episodios(RAIZ)
    wf = pd.read_csv(os.path.join(RAIZ, 'data/results/09_walkforward_errores.csv'), index_col=0, parse_dates=True)
    a = discriminacion_episodios(wf, e)
    b = discriminacion_larga(wf, e, metodos=('pca', 'ae', 'lstm'), tol=0)
    for r in b.itertuples():
        col = r.medida if r.episodio == '' else (f'mediana_{r.episodio}' if r.medida == 'mediana' else f'sensibilidad_{r.episodio}_%')
        assert round(r.valor, 2) == pytest.approx(a.loc[r.metodo, col], abs=1e-9)


def test_ampliar_episodios():
    e = cargar_episodios(RAIZ)
    amp = ampliar_episodios(e, 3)
    r = e.iloc[0]
    ini, fin = amp[r.nombre]
    assert pd.Timestamp(ini) == r.inicio_mes - pd.DateOffset(months=3)
    assert pd.Timestamp(fin) == r.fin_efectivo + pd.DateOffset(months=3)
