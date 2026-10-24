"""
Remuestreo por bloques móviles sin dependencia de torch (iteración 3a).

Paridad exacta con R mediante índices compartidos: el Rmd sortea los inicios de bloque con su
generador (semilla `params$semilla` = 2026) y los escribe en `data/results/R_*indices*.csv`;
aquí se leen y se reconstruyen los mismos índices de filas. Así los resultados coinciden al
1e-10 sin depender de que los generadores aleatorios de R y de numpy sean iguales.

Funciones:
- indices_desde_inicios: reconstruye las filas remuestreadas (como `indices_bloques` del Rmd);
- leer_inicios_bootstrap, leer_inicios_nulo: lectura de los CSV de índices del Rmd;
- bootstrap_pca: bootstrap por bloques de las cargas y los valores propios del PCA;
- nulo_tendencias: PCA de 17 series independientes con la dinámica de cada serie
  (sección 2 del Rmd, chunk `b2s-nulo`).

Supuesto declarado: el bootstrap por bloques supone dependencia débil (series estacionarias y
mezcladoras). En la vía en niveles, con tendencias, ese supuesto no se cumple: ahí el bootstrap
mide estabilidad descriptiva de los ejes, no incertidumbre muestral.
Fuente del método: Künsch (1989) [VERIFICAR: ficha preliminar kunsch_1989; no se verificó que el
artículo defina el esquema de bloques móviles solapados de este código].
"""

import numpy as np
import pandas as pd

from src.multivariado import estandarizar, emparejar_componentes
from src.series_tiempo import quitar_tendencia


def indices_desde_inicios(inicios, largo, n):
    """Filas (0-based) de una réplica: bloques contiguos de `largo` desde cada inicio (1-based), truncado a n."""
    inicios = np.asarray(inicios, dtype=int)
    filas = np.concatenate([np.arange(i - 1, i - 1 + largo) for i in inicios])
    return filas[:n]


def leer_inicios_bootstrap(archivo):
    """Matriz réplicas × bloques de inicios (1-based) escrita por el Rmd."""
    d = pd.read_csv(archivo)
    return d.sort_values('replica').filter(like='inicio_').to_numpy(dtype=int)


def leer_inicios_nulo(archivo, p):
    """Arreglo réplicas × series × bloques de inicios (1-based) del nulo de tendencias."""
    d = pd.read_csv(archivo).sort_values(['replica', 'serie'])
    reps = d['replica'].nunique()
    assert d['serie'].nunique() == p
    return d.filter(like='inicio_').to_numpy(dtype=int).reshape(reps, p, -1)


def bootstrap_pca(X, cargas_ref, inicios, largo, K=4, candidatos=6):
    """
    Bootstrap por bloques del PCA (traducción de los chunks `b3-bootstrap` y `bB2-bootstrap`).

    En cada réplica se toman las filas de los bloques, se estandariza, se calcula el PCA de la
    matriz de correlaciones y cada componente original k = 1..K se empareja con la componente
    de la réplica (entre las 6 primeras) de mayor |congruencia de Tucker|, sin repetir. La carga
    emparejada se orienta con el signo de la congruencia.

    Devuelve: cargas (B × p × K), valores propios emparejados (B × K), congruencias (B × K) y
    valores propios ordenados de cada réplica (B × p).
    """
    X = np.asarray(X, dtype=float)
    n, p = X.shape
    B = inicios.shape[0]
    boot_c = np.empty((B, p, K))
    boot_vp = np.empty((B, K))
    congr = np.empty((B, K))
    vp_ord = np.empty((B, p))
    for b in range(B):
        idx = indices_desde_inicios(inicios[b], largo, n)
        Zb = estandarizar(X[idx])
        val, vec = np.linalg.eigh(Zb.T @ Zb / n)
        o = np.argsort(val)[::-1]
        val, vec = val[o], vec[:, o]
        Cb = vec[:, :candidatos] * np.sqrt(val[:candidatos])
        j, c, s = emparejar_componentes(cargas_ref, Cb, K, candidatos)
        boot_c[b] = Cb[:, j] * s
        boot_vp[b] = val[j]
        congr[b] = c
        vp_ord[b] = val
    return {'cargas': boot_c, 'valores_emparejados': boot_vp, 'congruencia': congr,
            'valores_ordenados': vp_ord}


def _medidas_nulo(M, p):
    """Inercia (%) de PC1-PC3 y |r| medio entre pares de la matriz de correlaciones de M."""
    R = np.corrcoef(M, rowvar=False)
    e = np.sort(np.linalg.eigvalsh(R))[::-1]
    iu = np.triu_indices(p, 1)
    return np.concatenate([100 * e[:3] / p, [np.mean(np.abs(R[iu]))]])


def nulo_tendencias(X, inicios, largo=12, version='con_deriva'):
    """
    Nulo de tendencias independientes (chunk `b2s-nulo` del Rmd).

    Para cada réplica y cada serie se remuestrean sus incrementos mensuales en bloques de
    `largo` meses y se acumulan desde 0: cada serie conserva su dinámica de corto plazo, pero se
    rompe toda relación entre series.
      - 'con_deriva': incrementos tal cual (cada serie conserva su crecimiento medio);
      - 'sin_deriva': se resta antes el incremento medio de la serie;
      - 'sin_tendencia': como 'con_deriva', y luego se quita a cada serie simulada su tendencia
        lineal, igual que a las series observadas en el diagnóstico sin tendencia (D5).
    Devuelve una matriz réplicas × 4 (inercia PC1, PC2, PC3 y |r| medio).
    """
    X = np.asarray(X, dtype=float)
    D = np.diff(X, axis=0)
    nd, p = D.shape
    medias = D.mean(axis=0)
    reps = inicios.shape[0]
    sims = np.empty((reps, 4))
    for r in range(reps):
        M = np.empty((nd + 1, p))
        for j in range(p):
            d = D[indices_desde_inicios(inicios[r, j], largo, nd), j]
            if version == 'sin_deriva':
                d = d - medias[j]
            M[:, j] = np.concatenate([[0.0], np.cumsum(d)])
        if version == 'sin_tendencia':
            M = quitar_tendencia(M)
        sims[r] = _medidas_nulo(M, p)
    return sims


def medidas_observadas(X):
    """Las mismas cuatro medidas sobre las series observadas."""
    X = np.asarray(X, dtype=float)
    return _medidas_nulo(X, X.shape[1])
