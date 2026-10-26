"""Carga verificada de las dos vías mensuales (iteración 3b).

Reúne en un solo lugar la lectura que repetían `notebooks/999_port_camiz.ipynb` y el 05: las
17 series del análisis en el orden de `meta_an` del Rmd, leídas con los mismos bits que
`read.csv` de R (`camiz_port.leer_csv_como_r`), y los controles que exige el repositorio antes
de modelar:

- versión congelada de los datos (D4, md5);
- calendario mensual continuo y sin faltantes;
- dimensiones vigentes: 228 × 17 en niveles (2007-01 a 2025-12, D1) y 227 × 17 en las
  transformadas (2007-02 a 2025-12, D2).

Las filas se etiquetan con «AAAA-MM», como las fechas de corte de los CSV `R_*`.
"""

import hashlib
from pathlib import Path

import pandas as pd

from src import camiz_port as cp

# Columna del archivo, nombre corto del Rmd y código BCRP (orden de meta_an, entra == "Sí")
META = pd.DataFrame([
    ('Crédito empresarial', 'Crédito empresarial', 'PN00532MM'),
    ('Crédito consumo', 'Crédito consumo', 'PN00533MM'),
    ('Crédito hipotecario', 'Crédito hipotecario', 'PN00534MM'),
    ('Liquidez M1', 'M1 (dinero)', 'PN00199MM'),
    ('Liquidez M2', 'M2 (liquidez en soles)', 'PN00208MM'),
    ('Liquidez M3', 'M3 (liquidez total)', 'PN00214MM'),
    ('Tasa referencia BCRP', 'Tasa de referencia', 'PD04722MM'),
    ('Tasa interbancaria', 'Tasa interbancaria', 'PN07819NM'),
    ('Tasa activa TAMN', 'TAMN', 'PN07807NM'),
    ('Tasa pasiva TIPMN', 'TIPMN', 'PN07816NM'),
    ('IPC Lima', 'IPC Lima', 'PN38705PM'),
    ('Tipo de cambio', 'Tipo de cambio', 'PN01246PM'),
    ('Índice BVL', 'Índice BVL', 'PN01142MM'),
    ('embi_peru', 'EMBIG Perú', 'PD04709XD'),
    ('PBI desestacionalizado', 'PBI desestacionalizado', 'PN01773AM'),
    ('Demanda interna', 'Demanda interna', 'PN01774AM'),
    ('Reservas internacionales', 'Reservas internacionales netas', 'PN00027MM'),
], columns=['columna', 'nombre_corto', 'codigo'])

MD5_D4 = {'dataset_niveles_mensual.csv': '8088c28cf277419388d9562722faa1ad',
          'dataset_transformado_mensual.csv': '8c49f3e55608f2651be3c1dee4236194'}

CREDITOS = ['Crédito empresarial', 'Crédito consumo', 'Crédito hipotecario']


def raiz_repositorio(desde=None):
    """Sube desde `desde` (o el directorio actual) hasta la carpeta que contiene _quarto.yml."""
    r = Path(desde or Path.cwd()).resolve()
    for c in [r, *r.parents]:
        if (c / '_quarto.yml').exists():
            return c
    raise FileNotFoundError('No se encontró la raíz del repositorio (_quarto.yml)')


def _md5(ruta):
    return hashlib.md5(Path(ruta).read_bytes()).hexdigest()


def _verificar(d, n_esperado, inicio, fin):
    # Calendario mensual continuo, sin faltantes y con la dimensión declarada
    f = pd.to_datetime(d['fecha'])
    cal = pd.date_range(inicio, fin, freq='MS')
    assert len(f) == len(cal) and (f.to_numpy() == cal.to_numpy()).all(), 'calendario con huecos'
    assert not d.isna().any().any(), 'hay valores faltantes'
    assert len(d) == n_esperado, f'se esperaban {n_esperado} meses y hay {len(d)}'


def cargar_vias(raiz=None):
    """Devuelve (X, Xt): niveles 228 × 17 y transformadas 227 × 17, con índice «AAAA-MM».

    Falla (AssertionError) si los datos no son la versión congelada o están incompletos.
    """
    raiz = Path(raiz) if raiz else raiz_repositorio()
    proc = raiz / 'data' / 'processed'
    for nombre, h in MD5_D4.items():
        assert _md5(proc / nombre) == h, f'{nombre} no es la versión congelada (D4)'
    niv = cp.leer_csv_como_r(proc / 'dataset_niveles_mensual.csv')
    tr = cp.leer_csv_como_r(proc / 'dataset_transformado_mensual.csv')
    _verificar(niv, 228, '2007-01-01', '2025-12-01')
    _verificar(tr, 227, '2007-02-01', '2025-12-01')
    X = niv[META.columna].astype(float).copy()
    X.columns = list(META.nombre_corto)
    X.index = niv['fecha'].str[:7]
    base = {c.replace('_log_diff', '').replace('_diff', ''): c for c in tr.columns if c != 'fecha'}
    Xt = tr[[base[c] for c in META.columna]].astype(float).copy()
    Xt.columns = list(META.nombre_corto)
    Xt.index = tr['fecha'].str[:7]
    assert X.shape == (228, 17) and Xt.shape == (227, 17)
    assert not X.isna().any().any() and not Xt.isna().any().any()
    return X, Xt
