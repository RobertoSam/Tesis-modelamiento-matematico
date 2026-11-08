"""Pruebas de los productos del 8-nov-2026: columna `orden`, compatibilidad corte × episodio
(`def:tolerancia`, D7) y resúmenes para las cifras de la tesis.

Comprueban los CSV vigentes de `data/results/final/` contra sus definiciones, calculadas aquí de
forma independiente a partir de `data/referencia/episodios_referencia.csv` y de los CSV de origen.
"""

import os

import pandas as pd

from src import episodios as ep

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL = os.path.join(RAIZ, 'data', 'results', 'final')


def leer(nombre, **kw):
    return pd.read_csv(os.path.join(FINAL, nombre), keep_default_na=False, **kw)


def mes(texto):
    a, m = texto.split('-')[:2]
    return int(a) * 12 + int(m)


def test_orden_cronologico_y_paridad_con_r():
    for py, r, col in [('09a_estabilidad_cortes.csv', 'R_estabilidad_cortes.csv', 'corte'),
                       ('09a_regimenes_pca.csv', 'R_regimenes_pca.csv', 'inicio')]:
        t, tr = leer(py), leer(r)
        assert list(t.orden) == list(range(1, len(t) + 1))
        assert list(t[col]) == sorted(t[col])
        assert list(tr.orden) == list(t.orden) and list(tr[col]) == list(t[col])


def test_compatibilidad_segun_la_definicion():
    e = ep.cargar_episodios(RAIZ)
    cortes = leer('09a_estabilidad_cortes.csv')
    t = leer('09a_compatibilidad_cortes.csv')
    assert len(t) == len(cortes) * len(e)
    for r in t.itertuples():
        epi = e[e.nombre == r.episodio].iloc[0]
        ini, fin = mes(epi.inicio), mes(epi.fin_efectivo.strftime('%Y-%m'))
        tau = mes(r.corte)
        assert (r.inicio, r.fin_efectivo) == (epi.inicio, epi.fin_efectivo.strftime('%Y-%m'))
        assert r.distancia_meses == max(ini - tau, 0, tau - fin)
        for h, marca in [(3, r.compatible_h3), (6, r.compatible_h6)]:
            assert str(marca) == str(ini - h <= tau <= fin + h)
    # Paridad con R (TRUE/FALSE de R frente a True/False de Python)
    tr = leer('R_compatibilidad_cortes.csv')
    norm = lambda q: q.astype(str).apply(lambda s: s.str.upper())
    assert norm(tr[t.columns]).equals(norm(t))


def test_resumenes():
    b = leer('07c_hfc_bootstrap.csv')
    s = leer('07c_hfc_bootstrap_resumen.csv').iloc[0]
    assert s.replicas == len(b)
    for c in ['ari_3', 'ari_4', 'cofenetica']:
        assert abs(s[f'{c}_media'] - b[c].mean()) < 1e-12 and abs(s[f'{c}_mediana'] - b[c].median()) < 1e-12
    esp = pd.read_csv(os.path.join(FINAL, 'anexo', '05c_espectro.csv'))
    er = pd.read_csv(os.path.join(FINAL, 'anexo', '05c_espectro_resumen.csv')).set_index('version')
    for v in ['niv', 'niv_det', 'tr']:
        assert abs(er.loc[v, 'mediana_pct'] - 100 * esp[v].median()) < 1e-10
    tr = leer('07b_transiciones_d10.csv')
    rs = leer('07b_transiciones_d10_resumen.csv').set_index('objeto')
    for obj, g in tr.groupby('objeto'):
        cuentan = g[(g.es_borde_3.astype(str) == 'False') & (g.fuera_del_nulo.astype(str) == 'True')]
        assert rs.loc[obj, 'candidatas'] == len(g) and rs.loc[obj, 'cuentan'] == len(cuentan)
        assert rs.loc[obj, 'fecha_cuenta_unica'] == (cuentan.fecha.iloc[0] if len(cuentan) == 1 else '')
    par = pd.read_csv(os.path.join(FINAL, 'R_paridad_python.csv'))
    pr = pd.read_csv(os.path.join(FINAL, 'R_paridad_resumen.csv')).iloc[0]
    assert pr.filas == len(par) and pr.coinciden == (par.coincide == 'sí').sum()
