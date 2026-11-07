"""Bloque de parámetros común de los notebooks vigentes (adenda 3b, §3).

Los notebooks 06, 06c, 07b, 07c, 09a y 09b corren por defecto la versión vigente (D15, D16):
**niveles, 16 series**, con salidas en `data/results/final/`. El código de dos vías y 17 series del
antecedente (commit `2be3665`; el tag `v0.4-17series-dos-vias` está pendiente) sigue disponible detrás de los parámetros, para la prueba
de no regresión (`herramientas/no_regresion_dinamica.py`).

Parámetros (variables de entorno, como en el notebook 05):

- `TESIS_VIA`: 'niveles' (vigente) o 'ambas' (antecedente en dos vías, D2);
- `TESIS_EXCLUIDAS`: lista JSON de columnas del archivo que se retiran al leer; por defecto,
  `src.datos.EXCLUIDAS_D16` (la Liquidez M2);
- `TESIS_CARPETA`: salidas de la vía en niveles; la transformada, si se corre, va en CARPETA/anexo;
- `TESIS_R_NIVELES`, `TESIS_R_TRANSFORMADAS`: carpetas con los índices compartidos y los CSV R_*
  que escribe el Rmd (por defecto, las mismas de salida).

Nunca se escribe en las carpetas del antecedente (`data/results/` y `data/results/niveles/`).
"""

import json
import os
from pathlib import Path

from src.datos import EXCLUIDAS_D16

CARPETA_FINAL = Path('data') / 'results' / 'final'
ANTECEDENTE = (Path('data') / 'results', Path('data') / 'results' / 'niveles')


def leer_parametros(raiz):
    """Devuelve un dict con VIA, EXCLUIDAS, CARPETA, DIR, DIR_R, DIR_FIG y VIAS_ACTIVAS (rutas absolutas)."""
    raiz = Path(raiz).resolve()
    via = os.environ.get('TESIS_VIA', 'niveles')
    assert via in ('niveles', 'ambas'), via
    excl = tuple(json.loads(os.environ['TESIS_EXCLUIDAS'])) if 'TESIS_EXCLUIDAS' in os.environ else EXCLUIDAS_D16
    carpeta = Path(os.environ.get('TESIS_CARPETA', str(CARPETA_FINAL)))
    carpeta = carpeta if carpeta.is_absolute() else raiz / carpeta
    dir_ = {'niveles': carpeta, 'transformadas': carpeta / 'anexo'}
    dir_r = {'niveles': Path(os.environ.get('TESIS_R_NIVELES', str(dir_['niveles']))),
             'transformadas': Path(os.environ.get('TESIS_R_TRANSFORMADAS', str(dir_['transformadas'])))}
    dir_r = {k: (v if v.is_absolute() else raiz / v) for k, v in dir_r.items()}
    if carpeta.resolve() == (raiz / CARPETA_FINAL).resolve():
        dir_fig = {'niveles': raiz / 'reports' / 'figures' / 'final',
                   'transformadas': raiz / 'reports' / 'figures' / 'final' / 'anexo'}
    else:
        dir_fig = {v: d / 'figuras' for v, d in dir_.items()}
    activas = ['niveles'] if via == 'niveles' else ['niveles', 'transformadas']
    prohibidas = {(raiz / a).resolve() for a in ANTECEDENTE}
    for v in activas:
        assert dir_[v].resolve() not in prohibidas, 'no se escribe en las carpetas del antecedente'
        dir_[v].mkdir(parents=True, exist_ok=True)
        dir_fig[v].mkdir(parents=True, exist_ok=True)
    return {'VIA': via, 'EXCLUIDAS': excl, 'CARPETA': carpeta, 'DIR': dir_, 'DIR_R': dir_r,
            'DIR_FIG': dir_fig, 'VIAS_ACTIVAS': activas}
