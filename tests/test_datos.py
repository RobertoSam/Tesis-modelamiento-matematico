"""Pruebas de la carga verificada de datos con el parámetro de exclusión (D16, adenda 3b, D0)."""

import os
import sys

import numpy as np
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from src import datos  # noqa: E402


def test_parametro_unico_d16():
    # D16: la única serie excluida al leer es la Liquidez M2
    assert datos.EXCLUIDAS_D16 == ('Liquidez M2',)
    assert len(datos.META) == 17
    m = datos.meta_vigente(datos.EXCLUIDAS_D16)
    assert len(m) == 16 and 'Liquidez M2' not in set(m.columna)
    # el orden de las demás series no cambia
    assert list(m.columna) == [c for c in datos.META.columna if c != 'Liquidez M2']


def test_exclusion_desconocida_falla():
    with pytest.raises(AssertionError):
        datos.meta_vigente(('Serie inexistente',))


def test_cargar_vias_16_y_17():
    X17, Xt17 = datos.cargar_vias(RAIZ)
    X16, Xt16 = datos.cargar_vias(RAIZ, excluidas=datos.EXCLUIDAS_D16)
    assert X17.shape == (228, 17) and Xt17.shape == (227, 17)
    assert X16.shape == (228, 16) and Xt16.shape == (227, 16)
    assert 'M2 (liquidez en soles)' in X17.columns and 'M2 (liquidez en soles)' not in X16.columns
    # mismas cifras, bit a bit, en las columnas comunes (la exclusión no altera la lectura)
    comunes = list(X16.columns)
    assert np.array_equal(X17[comunes].to_numpy(), X16.to_numpy())
    assert np.array_equal(Xt17[comunes].to_numpy(), Xt16.to_numpy())
    assert X16.index[0] == '2007-01' and X16.index[-1] == '2025-12'
    assert Xt16.index[0] == '2007-02' and Xt16.index[-1] == '2025-12'
