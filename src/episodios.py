"""Episodios de referencia: lector único y funciones que los usan (tarea D9, decisión D7).

Los episodios se leen **solo** de `data/referencia/episodios_referencia.csv`. Cada fecha es la de
un evento o anuncio externo con fuente fichada (claves `clave_inicio` y `clave_fin`). Un episodio
sin fecha de fin con fuente es **puntual**: solo tiene inicio y no se le inventa un fin (D7).

Funciones:
- cargar_episodios: lee y valida el CSV (columnas, formato AAAA-MM, coherencia de tipo y fin);
- diccionario_episodios: {nombre: ('AAAA-MM-01', 'AAAA-MM-01')}, el formato que usan los
  notebooks 08 y 09 a través de `modelos_dl.EPISODIOS_REFERENCIA`; un episodio puntual se
  representa con fin = inicio (un solo mes);
- discriminacion_episodios: la regla del notebook 09 (umbral 1 de la razón de error
  walk-forward), recalculada sin torch a partir de `09_walkforward_errores.csv`;
- bordes_ventana: meses (centro de ventana) en que cada episodio entra o sale de una ventana de
  n_w meses, con la tolerancia de D7 (±3 meses; ±6 como sensibilidad).

Convención de ventana (la de `borde_ventana` del Rmd): la ventana de n_w meses con centro f va de
f − ⌊n_w/2⌋ a f + n_w − 1 − ⌊n_w/2⌋. Un episodio **entra** cuando el final de la ventana llega a
su inicio y **sale** cuando el inicio de la ventana pasa su fin.
"""

from pathlib import Path

import numpy as np
import pandas as pd

ARCHIVO = Path('data') / 'referencia' / 'episodios_referencia.csv'
COLUMNAS = ['nombre', 'inicio', 'fin', 'clave_inicio', 'clave_fin', 'tipo', 'convencion']
TOLERANCIA_PRINCIPAL = 3      # meses (D7)
TOLERANCIA_SENSIBILIDAD = 6   # meses (D7)


def _raiz(raiz=None):
    r = Path(raiz) if raiz else Path(__file__).resolve().parents[1]
    assert (r / '_quarto.yml').exists(), f'{r} no es la raíz del repositorio'
    return r


def cargar_episodios(raiz=None):
    """Lee y valida el archivo único de episodios.

    Devuelve un DataFrame con las columnas del CSV más `inicio_mes` y `fin_mes` (Timestamp del
    primer día del mes; `fin_mes` es NaT si el episodio es puntual) y `fin_efectivo` (= fin_mes,
    o inicio_mes si es puntual).
    """
    d = pd.read_csv(_raiz(raiz) / ARCHIVO, dtype=str, keep_default_na=False)
    assert list(d.columns) == COLUMNAS, f'columnas inesperadas: {list(d.columns)}'
    assert d['nombre'].is_unique, 'nombres de episodio repetidos'
    assert d['inicio'].str.fullmatch(r'\d{4}-\d{2}').all(), 'inicio fuera del formato AAAA-MM'
    assert d['fin'].str.fullmatch(r'(\d{4}-\d{2})?').all(), 'fin fuera del formato AAAA-MM'
    assert (d['clave_inicio'] != '').all(), 'todo inicio necesita su clave'
    # fin vacío ⇔ clave_fin vacía ⇔ episodio puntual
    puntual = d['fin'] == ''
    assert ((d['clave_fin'] == '') == puntual).all(), 'clave_fin debe estar vacía solo si fin lo está'
    assert ((d['tipo'] == 'puntual') == puntual).all() and d['tipo'].isin(['periodo', 'puntual']).all()
    d['inicio_mes'] = pd.to_datetime(d['inicio'] + '-01')
    d['fin_mes'] = pd.to_datetime(d['fin'].where(~puntual) + '-01')
    d['fin_efectivo'] = d['fin_mes'].fillna(d['inicio_mes'])
    assert (d['fin_efectivo'] >= d['inicio_mes']).all(), 'fin anterior al inicio'
    return d


def diccionario_episodios(episodios=None):
    """{nombre: (inicio, fin)} con fechas 'AAAA-MM-01'; un episodio puntual tiene fin = inicio."""
    e = cargar_episodios() if episodios is None else episodios
    if isinstance(e, dict):
        return dict(e)
    return {r.nombre: (r.inicio_mes.strftime('%Y-%m-%d'), r.fin_efectivo.strftime('%Y-%m-%d'))
            for r in e.itertuples()}


def discriminacion_episodios(wf, episodios, metodos=('pca', 'ae', 'lstm'), umbral=1.0):
    """Discriminación de episodios fuera de muestra con la regla del notebook 09 (sección 2.1).

    `wf`: errores walk-forward con índice de fechas (columnas `pca`, `ae`, `lstm`). `episodios`:
    diccionario {nombre: (inicio, fin)} o DataFrame de `cargar_episodios`. Se evalúan los
    episodios con al menos un mes en el período de `wf`, en el orden del diccionario (con las
    fechas antiguas son el taper tantrum y el COVID-19, como en el 09). Devuelve la tabla con
    índice `metodo`, redondeada a 2 decimales, como `09_discriminacion_episodios.csv`.
    """
    dic = diccionario_episodios(episodios)
    idx = pd.DatetimeIndex(wf.index)
    en_episodio = pd.Series(False, index=wf.index)
    etiqueta = pd.Series('', index=wf.index)
    for nombre, (ini, fin) in dic.items():
        m = (idx >= ini) & (idx <= fin)
        en_episodio[m] = True
        etiqueta[m] = nombre
    evaluables = [nom for nom in dic if (etiqueta == nom).any()]
    filas = []
    for metodo in metodos:
        fila = {'metodo': metodo,
                'mediana_fuera_de_episodios': wf.loc[~en_episodio, metodo].median(),
                'falsas_alarmas_%': 100 * (wf.loc[~en_episodio, metodo] > umbral).mean()}
        for nombre in evaluables:
            v = wf.loc[etiqueta == nombre, metodo]
            fila[f'mediana_{nombre}'] = v.median()
            fila[f'sensibilidad_{nombre}_%'] = 100 * (v > umbral).mean()
        filas.append(fila)
    return pd.DataFrame(filas).set_index('metodo').round(2)


def _mover(fecha, k):
    return (pd.Timestamp(fecha) + pd.DateOffset(months=int(k))).normalize()


def bordes_ventana(episodios, anchos=(24, 36, 48, 60)):
    """Centro de ventana en que cada episodio entra o sale de la ventana, por ancho n_w.

    Una transición candidata con centro a ≤ tol meses de esas fechas coincide con un borde de
    ventana (D7). Para un episodio puntual, inicio y fin son el mismo mes.
    """
    filas = []
    for r in episodios.itertuples():
        for w in anchos:
            filas.append({'episodio': r.nombre, 'tipo': r.tipo, 'nw': w, 'evento': 'entra',
                          'centro': _mover(r.inicio_mes, -(w - 1 - w // 2)).strftime('%Y-%m')})
            filas.append({'episodio': r.nombre, 'tipo': r.tipo, 'nw': w, 'evento': 'sale',
                          'centro': _mover(r.fin_efectivo, w // 2).strftime('%Y-%m')})
    return pd.DataFrame(filas)


def meses_entre(a, b):
    """|a − b| en meses (fechas al primer día del mes)."""
    a, b = pd.Timestamp(a), pd.Timestamp(b)
    return abs((a.year - b.year) * 12 + a.month - b.month)


def borde_ventana(fecha, w, episodios, tol=TOLERANCIA_PRINCIPAL):
    """Texto «Entra X; Sale Y» si la transición con centro `fecha` coincide con un borde, o «—».

    Traducción de `borde_ventana` del Rmd, con fin = inicio para los episodios puntuales.
    """
    f = pd.Timestamp(fecha)
    sale = [r.nombre for r in episodios.itertuples() if meses_entre(_mover(f, -(w // 2)), r.fin_efectivo) <= tol]
    entra = [r.nombre for r in episodios.itertuples() if meses_entre(_mover(f, w - 1 - w // 2), r.inicio_mes) <= tol]
    partes = [f'Entra {e}' for e in entra] + [f'Sale {s}' for s in sale]
    return '; '.join(partes) if partes else '—'


def meses_en_episodio(fechas, episodios):
    """Vector booleano: el mes está dentro de algún episodio (inicio a fin efectivo, inclusive)."""
    f = pd.DatetimeIndex(pd.to_datetime(fechas))
    m = np.zeros(len(f), dtype=bool)
    for r in episodios.itertuples():
        m |= (f >= r.inicio_mes) & (f <= r.fin_efectivo)
    return m
