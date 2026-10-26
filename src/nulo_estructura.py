"""Nulo de estructura constante para la parte dinámica (iteración 3b, tarea D7).

Traducción de `R/07b_nulo_estructura.R` (la referencia en R, D6). Remuestreo por bloques
**conjunto**: los mismos inicios de bloque para las 17 series, de modo que se conservan la
correlación contemporánea y la dinámica corta, pero se dispersa en el tiempo cualquier cambio de
estructura.

- Vía transformada: se remuestrean las filas.
- Vía sin transformar: se remuestrean los incrementos mensuales y se acumulan desde 0 (como la
  versión «con deriva» de `remuestreo.nulo_tendencias`), con la suma acumulada de R (`cumsum`,
  acumulador long double) para partir de los mismos bits.

Los inicios de bloque los sortea el guion de R (semilla 2026) y se leen de
`R_nulo_estructura_indices_L{12,24,36}.csv`.

Para cada serie (observada o nula), ancho n_w y esquema de pesos se miden:
1. el k* de cada criterio de `aede` con maxcl = 20 (codo por caída máxima, CH con k y con k - 1);
2. el perfil del coeficiente RV entre ventanas adyacentes no solapadas: RV entre las cargas
   (`correlationlsq`, 17 × 3) de la ventana que empieza en la fila i y la que empieza en i + n_w.
"""

import numpy as np
import pandas as pd

from src import camiz_port as cp
from src.multivariado import coef_rv
from src.remuestreo import indices_desde_inicios

NW_GRILLA = (24, 36, 48, 60)
PESOS = {'uniformes': 0, 'gaussianos_nsd3': 3}
MAXCL = 20
CRITERIOS = [('codo (caída máxima)', 'k_codo'), ('Calinski-Harabász k gl (aede)', 'k_ch'),
             ('Calinski-Harabász k-1 gl (habitual)', 'k_ch1')]


def serie_nula(M, via, inicios, largo):
    """Serie nula de una réplica (DataFrame con las etiquetas de fila de M)."""
    A = M.to_numpy(dtype=float)
    if via == 'transformadas':
        B = A[indices_desde_inicios(inicios, largo, len(A))]
    else:
        D = np.diff(A, axis=0)
        Dn = D[indices_desde_inicios(inicios, largo, len(D))]
        B = np.vstack([np.zeros(A.shape[1]), cp._cumsum_r(Dn) if Dn.ndim == 1 else
                       np.column_stack([cp._cumsum_r(Dn[:, j]) for j in range(Dn.shape[1])])])
    return pd.DataFrame(B, index=M.index, columns=M.columns)


def medir(M, nw_grilla=NW_GRILLA, pesos=None, maxcl=MAXCL):
    """k* por criterio y perfil RV entre ventanas adyacentes no solapadas, para toda la grilla.

    Devuelve (kstar, rv, rv_resumen) como DataFrames.
    """
    pesos = PESOS if pesos is None else pesos
    kst, rv, rvr = [], [], []
    for nw in nw_grilla:
        for pz, nsd in pesos.items():
            a = cp.aede(M, nw=nw, ndim=3, nsd=nsd, maxcl=maxcl)
            r = cp.resumen_aede(a)
            for crit, kk in CRITERIOS:
                kst.append({'nw': nw, 'pesos': pz, 'criterio': crit, 'k': r[kk], 'k_en_tope': r[kk] == maxcl})
            C = a['correlationlsq']
            wn = C.shape[0]
            fv = list(a['eigenvalues'].index)
            valores = np.array([coef_rv(C[j], C[j + nw]) for j in range(wn - nw)])
            rv.append(pd.DataFrame({'nw': nw, 'pesos': pz, 'fecha_a': fv[:wn - nw], 'fecha_b': fv[nw:wn], 'rv': valores}))
            rvr.append({'nw': nw, 'pesos': pz, 'n_pares': len(valores), 'rv_min': valores.min(),
                        'rv_p05': np.quantile(valores, 0.05), 'rv_p50': np.quantile(valores, 0.5),
                        'rv_media': valores.mean()})
    return pd.DataFrame(kst), pd.concat(rv, ignore_index=True), pd.DataFrame(rvr)
