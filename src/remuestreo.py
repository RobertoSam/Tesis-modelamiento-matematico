"""
Remuestreo por bloques móviles sin dependencia de torch (iteración 3a).

Paridad exacta con R mediante índices compartidos: el Rmd sortea los inicios de bloque con su
generador (semilla `params$semilla` = 2026) y los escribe en `data/results/R_*indices*.csv`;
aquí se leen y se reconstruyen los mismos índices de filas. Así los resultados coinciden al
1e-10 sin depender de que los generadores aleatorios de R y de numpy sean iguales.

Funciones:
- indices_desde_inicios: reconstruye las filas remuestreadas (como `indices_bloques` del Rmd);
- leer_inicios_bootstrap, leer_inicios_nulo: lectura de los CSV de índices del Rmd;
- comprobar_inicios: verifica que los inicios estén en {1, ..., n − L + 1} y sean ⌈n / L⌉ por réplica;
- bootstrap_pca: bootstrap por bloques de las cargas y los valores propios del PCA;
- nulo_tendencias: PCA de p series independientes con la dinámica de cada serie
  (sección 2 del Rmd final, chunk `b2-nulo`).

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


def comprobar_inicios(inicios, n, largo):
    """
    Comprueba que los inicios (1-based) de bloque sirvan para remuestrear n filas con bloques de
    `largo`: todos en {1, ..., n − largo + 1} y ⌈n / largo⌉ por réplica (última dimensión).
    Con inicios sorteados para n − 1 filas (los incrementos), el inicio n − largo + 1 de n filas
    nunca aparece; por eso la rama TS del nulo mixto tiene sus propios inicios (D19).
    """
    inicios = np.asarray(inicios)
    assert np.issubdtype(inicios.dtype, np.integer), 'los inicios deben ser enteros'
    assert inicios.shape[-1] == int(np.ceil(n / largo)), \
        f'se esperaban {int(np.ceil(n / largo))} bloques por réplica para n = {n}, L = {largo}'
    assert inicios.min() >= 1 and inicios.max() <= n - largo + 1, \
        f'inicios fuera de {{1, ..., {n - largo + 1}}} (n = {n}, L = {largo})'


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


def nulo_tendencias(X, inicios, largo=12, version='con_deriva', tratamiento=None, inicios_ts=None):
    """
    Nulo de tendencias independientes (chunk `b2s-nulo` del Rmd).

    Para cada réplica y cada serie se remuestrean sus incrementos mensuales en bloques de
    `largo` meses y se acumulan desde 0: cada serie conserva su dinámica de corto plazo, pero se
    rompe toda relación entre series.
      - 'con_deriva': incrementos tal cual (cada serie conserva su crecimiento medio);
      - 'sin_deriva': se resta antes el incremento medio de la serie;
      - 'sin_tendencia': como 'con_deriva', y luego se quita a cada serie simulada su tendencia
        lineal, igual que a las series observadas en el diagnóstico sin tendencia (D5);
      - 'mixto' (D8): cada serie según `tratamiento[j]` ∈ {'TS', 'con_deriva', 'sin_deriva'}
        (ver `series_tiempo.tratamiento_mixto`). Una serie 'TS' se simula como su recta MCO más
        sus n residuos remuestreados en bloques con los inicios `inicios_ts`, sorteados en
        {1, ..., n − L + 1} (D19, 7-nov-2026: el residuo del último mes también puede iniciar un
        bloque); las otras, como arriba, con `inicios` (sorteados en {1, ..., n − L} para los
        n − 1 incrementos).
    `inicios`: réplicas × series × ⌈(n − 1) / L⌉; `inicios_ts`: réplicas × series × ⌈n / L⌉ (solo se
    exige en el mixto con alguna serie TS). Ambos 1-based, como los escribe el Rmd.
    Devuelve una matriz réplicas × 4 (inercia PC1, PC2, PC3 y |r| medio).
    """
    X = np.asarray(X, dtype=float)
    D = np.diff(X, axis=0)
    nd, p = D.shape
    n = nd + 1
    medias = D.mean(axis=0)
    comprobar_inicios(inicios, nd, largo)
    if version == 'mixto':
        assert tratamiento is not None and len(tratamiento) == p
        assert set(tratamiento) <= {'TS', 'con_deriva', 'sin_deriva'}
        if 'TS' in tratamiento:
            # D19: la rama TS remuestrea n residuos, con inicios propios en {1, ..., n − L + 1}
            assert inicios_ts is not None, 'el nulo mixto con series TS requiere inicios_ts (D19)'
            comprobar_inicios(inicios_ts, n, largo)
            assert inicios_ts.shape[:2] == inicios.shape[:2], 'inicios_ts: mismas réplicas y series que inicios'
        t = np.arange(1, n + 1, dtype=float)
        A = np.column_stack([np.ones(n), t])
        coef, *_ = np.linalg.lstsq(A, X, rcond=None)
        rectas = A @ coef
        residuos = X - rectas
    else:
        tratamiento = [version if version in ('con_deriva', 'sin_deriva') else 'con_deriva'] * p
    reps = inicios.shape[0]
    sims = np.empty((reps, 4))
    for r in range(reps):
        M = np.empty((n, p))
        for j in range(p):
            if tratamiento[j] == 'TS':
                M[:, j] = rectas[:, j] + residuos[indices_desde_inicios(inicios_ts[r, j], largo, n), j]
                continue
            d = D[indices_desde_inicios(inicios[r, j], largo, nd), j]
            if tratamiento[j] == 'sin_deriva':
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
