"""Pruebas de los episodios unificados (tarea D9, decisión D7) y del criterio 8 del plan de 3b."""

import io
import json
import os
import re

import pandas as pd
import pytest

from src import episodios as ep

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Fechas escritas a mano antes de D9 (Rmd, modelos_dl.py y 05: tres episodios). Solo se usan aquí,
# para la prueba de no regresión de la ruta sin torch (criterio 8).
FECHAS_ANTIGUAS = {'Crisis financiera global': ('2008-09-01', '2009-06-01'),
                   'Taper tantrum': ('2013-05-01', '2013-12-01'),
                   'COVID-19': ('2020-03-01', '2020-12-01')}


def test_archivo_unico_valido_y_con_fuentes():
    e = ep.cargar_episodios(RAIZ)
    assert len(e) == 6
    bib = open(os.path.join(RAIZ, 'tesis', 'referencias.bib'), encoding='utf-8').read()
    claves = set(re.findall(r'^@\w+\{([^,]+),', bib, flags=re.M))
    for c in pd.concat([e['clave_inicio'], e['clave_fin']]):
        if c:
            assert c in claves, f'{c} no está en el .bib'
            assert os.path.exists(os.path.join(RAIZ, 'papers', f'{c}.qmd')), f'{c} sin ficha'
    # puntual: sin fin ni clave de fin; su fin efectivo es el inicio (no se inventa el fin)
    p = e[e['tipo'] == 'puntual']
    assert (p['fin'] == '').all() and (p['fin_efectivo'] == p['inicio_mes']).all()
    assert (e['convencion'] == 'evento o anuncio externo (D7)').all()


@pytest.mark.parametrize('carpeta', ['data/results', 'data/results/niveles'])
def test_criterio_8_reproduce_discriminacion_del_09(carpeta):
    # La ruta sin torch, con las fechas antiguas, reproduce byte a byte el CSV del notebook 09
    wf = pd.read_csv(os.path.join(RAIZ, carpeta, '09_walkforward_errores.csv'), index_col=0, parse_dates=True)
    d = ep.discriminacion_episodios(wf, FECHAS_ANTIGUAS)
    original = open(os.path.join(RAIZ, carpeta, '09_discriminacion_episodios.csv'), encoding='utf-8').read()
    buf = io.StringIO()
    d.to_csv(buf)
    assert buf.getvalue() == original


def test_diccionario_y_puntual():
    dic = ep.diccionario_episodios(ep.cargar_episodios(RAIZ))
    assert dic['Kuczynski / Odebrecht'][0] == dic['Kuczynski / Odebrecht'][1]
    assert list(dic) == list(ep.cargar_episodios(RAIZ)['nombre'])


def test_bordes_ventana_coherentes_con_borde_ventana():
    e = ep.cargar_episodios(RAIZ)
    b = ep.bordes_ventana(e)
    assert len(b) == len(e) * 4 * 2
    for r in b.itertuples():
        texto = ep.borde_ventana(r.centro + '-01', r.nw, e, tol=0)
        assert f'{"Entra" if r.evento == "entra" else "Sale"} {r.episodio}' in texto
        # fuera de la tolerancia, el mismo episodio ya no marca ese borde
        lejos = ep._mover(r.centro + '-01', ep.TOLERANCIA_PRINCIPAL + 1)
        evento = f'{"Entra" if r.evento == "entra" else "Sale"} {r.episodio}'
        cerca = ep._mover(r.centro + '-01', ep.TOLERANCIA_PRINCIPAL)
        assert evento in ep.borde_ventana(cerca, r.nw, e)
        if r.tipo == 'periodo':
            assert evento not in ep.borde_ventana(lejos, r.nw, e)
    # convención del Rmd: con n_w = 60, un episodio entra cuando el centro está 29 meses antes
    fila = b[(b.episodio == 'Taper tantrum') & (b.nw == 60) & (b.evento == 'entra')].iloc[0]
    assert fila.centro == ep._mover('2013-05-01', -29).strftime('%Y-%m')


def _codigo_notebook(ruta):
    nb = json.load(open(ruta, encoding='utf-8'))
    return '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type'] == 'code')


def test_sin_fechas_de_episodio_a_mano_en_consumidores_vigentes():
    # Criterio 7: el código de los consumidores vigentes no contiene fechas de episodio
    e = ep.cargar_episodios(RAIZ)
    meses = set(e['inicio']) | set(x for x in e['fin'] if x)
    meses |= {f[:7] for par in FECHAS_ANTIGUAS.values() for f in par}
    meses |= {'2008-07', '2013-04', '2020-01', '2020-09', '2016-03', '2016-07'}   # 06a y 06b
    patron = re.compile('|'.join(re.escape(m) for m in sorted(meses)))
    fuentes = {'notebooks/modelos_dl.py': open(os.path.join(RAIZ, 'notebooks/modelos_dl.py'), encoding='utf-8').read(),
               'notebooks/05_pca.ipynb': _codigo_notebook(os.path.join(RAIZ, 'notebooks/05_pca.ipynb')),
               'R/ciclo_financiero_final.Rmd': open(os.path.join(RAIZ, 'R', 'ciclo_financiero_final.Rmd'), encoding='utf-8').read()}
    for nombre in os.listdir(os.path.join(RAIZ, 'src')):
        if nombre.endswith('.py'):
            fuentes[f'src/{nombre}'] = open(os.path.join(RAIZ, 'src', nombre), encoding='utf-8').read()
    for archivo, texto in fuentes.items():
        assert not patron.search(texto), f'{archivo}: fecha de episodio escrita a mano ({patron.search(texto).group(0)})'
