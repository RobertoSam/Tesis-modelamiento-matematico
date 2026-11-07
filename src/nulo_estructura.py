"""Nulo de estructura constante para la parte dinámica (iteración 3b, tareas D7 y D10).

Traducción de `R/07b_nulo_estructura.R` (la referencia en R, D6). Remuestreo por bloques
**conjunto**: los mismos inicios de bloque para todas las series, de modo que se conservan la
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
2. el perfil del coeficiente RV entre ventanas adyacentes no solapadas (la ventana que empieza en la
   fila i y la que empieza en i + n_w), con uno o más objetos (`objetos_rv`):
   - `cargas_sin_centrar` (principal de D17.2): RV de las cargas de `aede` (`correlationlsq`,
     p × 3) sin centrar las columnas;
   - `correlacion` (sensibilidad de D17.2): RV de las matrices de correlación completas p × p de
     cada ventana, con los pesos de `aede` (`camiz_port.bstatw`, la misma matriz que diagonaliza
     `aede`);
   - `cargas_centradas`: la lectura del antecedente (iteración 3b, fase 0, 17 series), que la
     adenda del 26-oct-2026 (§1.2) descartó; se conserva solo para la prueba de no regresión.
   La `frontera` de cada par es la etiqueta de la fila i + n_w (primer mes de la segunda ventana).
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


OBJETOS_D17 = ('cargas_sin_centrar', 'correlacion')
OBJETOS_ANTECEDENTE = ('cargas_centradas',)


def _rv_correlacion(Ra, Rb):
    # tr(Ra Rb) / sqrt(tr(Ra²) tr(Rb²)) para matrices simétricas (misma fórmula que src.dinamica)
    return float(np.sum(Ra * Rb) / np.sqrt(np.sum(Ra * Ra) * np.sum(Rb * Rb)))


def medir(M, nw_grilla=NW_GRILLA, pesos=None, maxcl=MAXCL, objetos_rv=OBJETOS_D17):
    """k* por criterio y perfil RV entre ventanas adyacentes no solapadas, para toda la grilla.

    Devuelve (kstar, rv, rv_resumen) como DataFrames; `rv` y `rv_resumen` llevan la columna
    `objeto` (uno por elemento de `objetos_rv`).
    """
    pesos = PESOS if pesos is None else pesos
    A = M.to_numpy(dtype=float)
    etiquetas = list(M.index)
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
            frontera = etiquetas[nw:nw + wn - nw]
            if 'correlacion' in objetos_rv:
                Rw = [cp.bstatw(A[j:j + nw], a['weights'])['correlations'] for j in range(wn)]
            for obj in objetos_rv:
                if obj == 'cargas_centradas':
                    valores = np.array([coef_rv(C[j], C[j + nw]) for j in range(wn - nw)])
                elif obj == 'cargas_sin_centrar':
                    valores = np.array([coef_rv(C[j], C[j + nw], centrar=False) for j in range(wn - nw)])
                elif obj == 'correlacion':
                    valores = np.array([_rv_correlacion(Rw[j], Rw[j + nw]) for j in range(wn - nw)])
                else:
                    raise ValueError(f'objeto RV desconocido: {obj}')
                rv.append(pd.DataFrame({'objeto': obj, 'nw': nw, 'pesos': pz, 'fecha_a': fv[:wn - nw],
                                        'fecha_b': fv[nw:wn], 'frontera': frontera, 'rv': valores}))
                rvr.append({'objeto': obj, 'nw': nw, 'pesos': pz, 'n_pares': len(valores), 'rv_min': valores.min(),
                            'rv_p05': np.quantile(valores, 0.05), 'rv_p50': np.quantile(valores, 0.5),
                            'rv_media': valores.mean()})
    return pd.DataFrame(kst), pd.concat(rv, ignore_index=True), pd.DataFrame(rvr)
