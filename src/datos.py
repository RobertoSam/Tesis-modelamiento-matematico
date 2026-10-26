"""Carga verificada de las dos vías mensuales (iteración 3b).

Reúne en un solo lugar la lectura que repetían `notebooks/999_port_camiz.ipynb` y el 05: las
series del análisis en el orden de `meta_an` del Rmd, leídas con los mismos bits que
`read.csv` de R (`camiz_port.leer_csv_como_r`), y los controles que exige el repositorio antes
de modelar:

- versión congelada de los datos (D4, md5);
- calendario mensual continuo y sin faltantes;
- dimensiones: 228 meses en niveles (2007-01 a 2025-12, D1) y 227 en las transformadas
  (2007-02 a 2025-12), con 17 − len(excluidas) series.

Series excluidas (D16, 26-oct-2026). `EXCLUIDAS_D16` es el **parámetro único** con la lista de
series que se retiran al leer: hoy, la Liquidez M2 (16 series vigentes). Los archivos de D4 no se
modifican; la exclusión se aplica al leer, como la del crédito total del SF y la del IPC
subyacente. `cargar_vias(excluidas=())` (valor por defecto) conserva las 17 series del antecedente
(tag `v0.4-17series-dos-vias`), de modo que los notebooks antecedentes no cambian si se vuelven a
ejecutar; los vigentes pasan `excluidas=EXCLUIDAS_D16` desde su bloque de parámetros.

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

# Parámetro único de D16: columnas del archivo que se retiran al leer (análisis vigente, 16 series)
EXCLUIDAS_D16 = ('Liquidez M2',)


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


def meta_vigente(excluidas=()):
    """Filas de META sin las series excluidas (por nombre de columna del archivo), en el mismo orden."""
    excluidas = tuple(excluidas)
    desconocidas = set(excluidas) - set(META.columna)
    assert not desconocidas, f'series excluidas que no están en META: {sorted(desconocidas)}'
    return META[~META.columna.isin(excluidas)].reset_index(drop=True)


def cargar_vias(raiz=None, excluidas=()):
    """Devuelve (X, Xt): niveles 228 × p y transformadas 227 × p, con índice «AAAA-MM».

    p = 17 − len(excluidas). `excluidas` son nombres de columna del archivo (`META.columna`); para
    el análisis vigente se pasa `EXCLUIDAS_D16`. Falla (AssertionError) si los datos no son la
    versión congelada o están incompletos.
    """
    meta = meta_vigente(excluidas)
    p = len(meta)
    raiz = Path(raiz) if raiz else raiz_repositorio()
    proc = raiz / 'data' / 'processed'
    for nombre, h in MD5_D4.items():
        assert _md5(proc / nombre) == h, f'{nombre} no es la versión congelada (D4)'
    niv = cp.leer_csv_como_r(proc / 'dataset_niveles_mensual.csv')
    tr = cp.leer_csv_como_r(proc / 'dataset_transformado_mensual.csv')
    _verificar(niv, 228, '2007-01-01', '2025-12-01')
    _verificar(tr, 227, '2007-02-01', '2025-12-01')
    X = niv[meta.columna].astype(float).copy()
    X.columns = list(meta.nombre_corto)
    X.index = niv['fecha'].str[:7]
    base = {c.replace('_log_diff', '').replace('_diff', ''): c for c in tr.columns if c != 'fecha'}
    Xt = tr[[base[c] for c in meta.columna]].astype(float).copy()
    Xt.columns = list(meta.nombre_corto)
    Xt.index = tr['fecha'].str[:7]
    assert X.shape == (228, p) and Xt.shape == (227, p)
    assert not X.isna().any().any() and not Xt.isna().any().any()
    return X, Xt
