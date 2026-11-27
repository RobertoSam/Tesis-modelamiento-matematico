"""Pruebas de la cobertura descriptiva de los episodios (F0-3 del plan de cierre de la iteración 3c).

Comprueban las funciones de `src/episodios.py` con casos sintéticos y el CSV vigente
`data/results/final/09a_cobertura_episodios.csv` contra un recálculo independiente desde
`data/referencia/episodios_referencia.csv`, los datos congelados y su réplica en R.
"""

import itertools
import os

import numpy as np
import pandas as pd

from src import episodios as ep
from src.parametros import leer_parametros
from src.datos import cargar_vias

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL = os.path.join(RAIZ, 'data', 'results', 'final')


def leer(nombre):
    return pd.read_csv(os.path.join(FINAL, nombre), keep_default_na=False)


def mes(f):
    f = pd.Timestamp(f)
    return f.year * 12 + f.month


def test_distancia_al_intervalo_y_puntual():
    e = pd.DataFrame({'inicio_mes': pd.to_datetime(['2010-05-01', '2012-01-01']),
                      'fin_efectivo': pd.to_datetime(['2010-08-01', '2012-01-01'])})   # el segundo es puntual
    fechas = pd.to_datetime(['2010-01-01', '2010-05-01', '2010-07-01', '2010-11-01', '2011-10-01', '2012-04-01'])
    assert list(ep.distancia_a_episodios(fechas, e)) == [4, 0, 0, 3, 3, 3]
    t = ep.cobertura_episodios(fechas, e, hs=(3, 6)).set_index('h')
    assert t.loc[3, 'n_cubiertos'] == 5 and t.loc[6, 'n_cubiertos'] == 6
    assert t.loc[3, 'n_total'] == 6 and abs(t.loc[3, 'fraccion'] - 5 / 6) < 1e-15


def test_posiciones_admisibles_son_las_de_alguna_particion():
    # Enumeración exhaustiva para n pequeño: unión de los cortes de toda partición con tramos >= n_min
    for n, n_min in [(10, 2), (11, 3), (7, 3), (5, 3)]:
        union = set()
        for k in range(2, n // n_min + 1):
            for cortes in itertools.combinations(range(1, n), k - 1):
                largos = np.diff([0, *cortes, n])
                if (largos >= n_min).all():
                    union.update(cortes)
        assert set(ep.posiciones_corte_admisibles(n, n_min)) == union, (n, n_min)


def test_csv_vigente_recalculado_y_paridad_con_r():
    param = leer_parametros(RAIZ)
    X, _ = cargar_vias(RAIZ, excluidas=param['EXCLUIDAS'])
    e = ep.cargar_episodios(RAIZ)
    t = leer('09a_cobertura_episodios.csv')
    hs = (ep.TOLERANCIA_PRINCIPAL, ep.TOLERANCIA_SENSIBILIDAD)
    assert list(t.h) == list(hs) * 2
    # Meses de la muestra: los de los datos; posiciones admisibles: sobre las fechas suavizadas (MM12)
    n_min = int(t.loc[t.universo == 'posiciones_corte_admisibles', 'n_min'].iloc[0])
    # Las fechas suavizadas empiezan en el inicio del primer régimen de la datación
    inicio_z = pd.Timestamp(leer('09a_regimenes_pca.csv').inicio.iloc[0] + '-01')
    fz = [f for f in X.index if pd.Timestamp(f) >= inicio_z]
    universos = {'meses_muestra': list(X.index),
                 'posiciones_corte_admisibles': [fz[c] for c in range(n_min, len(fz) - n_min + 1)]}
    for r in t.itertuples():
        f = universos[r.universo]
        cub = sum(any(mes(a) - r.h <= mes(x) <= mes(b) + r.h for a, b in zip(e.inicio_mes, e.fin_efectivo)) for x in f)
        assert (r.n_total, r.n_cubiertos) == (len(f), cub)
        assert (r.primer_mes, r.ultimo_mes) == (pd.Timestamp(f[0]).strftime('%Y-%m'), pd.Timestamp(f[-1]).strftime('%Y-%m'))
        assert abs(r.fraccion - cub / len(f)) < 1e-15
    # Los cortes de la datación principal están entre las posiciones admisibles
    cortes = set(leer('09a_estabilidad_cortes.csv').corte)
    assert cortes <= {pd.Timestamp(x).strftime('%Y-%m') for x in universos['posiciones_corte_admisibles']}
    # Réplica en R
    tr = leer('R_cobertura_episodios.csv')
    cols = ['universo', 'n_min', 'h', 'primer_mes', 'ultimo_mes', 'n_total', 'n_cubiertos']
    assert tr[cols].astype(str).equals(t[cols].astype(str))
    assert np.max(np.abs(tr.fraccion.to_numpy() - t.fraccion.to_numpy())) < 1e-15
