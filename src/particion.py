"""Partición óptima de series ordenadas en el tiempo (datación de regímenes).

Módulo previsto en el plan de la iteración 3a (sección 7, desarrollador, punto 1). La
recurrencia de Fisher (1958) ya está portada desde R en `src/camiz_port.py` (`fisher`), con
paridad verificada en `tests/test_camiz_port.py`. Este módulo no la reimplementa: la envuelve
para devolver la partición en términos de fechas y etiquetas de régimen, que es la forma en que
la usan los notebooks de datación. Sin dependencia de `torch`.

Tarea D2 de la iteración 3b: se añade la longitud mínima de segmento `n_min` (por defecto 1, que
reproduce el comportamiento anterior) y la partición de series multivariadas (n × q), que necesita
la datación PCA-MM12 del 09a (`tam_min = 12` en `datar`). La recurrencia multivariada con
longitud mínima es la traducción de `particion_fisher` del Rmd (chunk `funciones`), con el mismo
orden de operaciones: sumas acumuladas por columna con acumulador long double (`cumsum` de R),
`rowSums` de los cuadrados y primer mínimo (`which.min`).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.camiz_port import fisher


def _cumsum_ld(x, axis=0):
    # cumsum() de R: acumulador long double y resultado en double
    return np.cumsum(np.asarray(x, dtype=np.longdouble), axis=axis).astype(np.float64)


def fisher_multivariado(Y, k_max=8, n_min=6):
    """Partición óptima de Fisher de una serie ordenada (n × q) con segmentos de al menos
    `n_min` filas, para k = 1..k_max (traducción de `particion_fisher` del Rmd).

    Devuelve un dict k -> {'sce', 'cortes'}, donde 'cortes' son las posiciones 0-based del
    inicio de cada segmento 2..k. Solo aparecen los k factibles (k · n_min <= n).
    """
    Y = np.asarray(Y, dtype=float)
    if Y.ndim == 1:
        Y = Y[:, None]
    n = Y.shape[0]
    if n_min < 1:
        raise ValueError("n_min debe ser al menos 1")
    S1 = np.vstack([np.zeros(Y.shape[1]), _cumsum_ld(Y, axis=0)])
    # rowSums de R acumula en long double; luego cumsum
    filas2 = np.sum(np.asarray(Y, dtype=np.longdouble) ** 2, axis=1).astype(np.float64)
    S2 = np.concatenate([[0.0], _cumsum_ld(filas2)])

    def sce(i, j):
        # segmento de las filas i+1..j (1-based), es decir Y[i:j]
        s = S1[j] - S1[i]
        ss = float(np.sum(np.asarray(s * s, dtype=np.longdouble)))
        return S2[j] - S2[i] - ss / (j - i)

    def sce_vec(ini, j):
        # sce(i, j) para un vector de inicios i, con las mismas operaciones elemento a elemento
        # (iteración 3b: se vectoriza el bucle interno sin cambiar la aritmética, porque la
        # grilla maxcl = 20 y el remuestreo de los cortes lo recorren miles de veces)
        s = S1[j] - S1[ini]
        ss = np.sum(np.asarray(s * s, dtype=np.longdouble), axis=1).astype(np.float64)
        return S2[j] - S2[ini] - ss / (j - ini)

    D = np.full((k_max + 1, n + 1), np.inf)
    B = np.zeros((k_max + 1, n + 1), dtype=int)
    for j in range(n_min, n + 1):
        D[1, j] = sce(0, j)
    for k in range(2, k_max + 1):
        if k * n_min > n:
            break
        for j in range(k * n_min, n + 1):
            ini = np.arange((k - 1) * n_min, j - n_min + 1)
            costos = D[k - 1, ini] + sce_vec(ini, j)
            pos = int(np.argmin(costos))            # primer mínimo, como which.min
            D[k, j] = costos[pos]
            B[k, j] = ini[pos]
    res = {}
    for k in range(1, k_max + 1):
        if not np.isfinite(D[k, n]):
            continue
        cortes, j = [], n
        for kk in range(k, 1, -1):
            i = int(B[kk, j])
            cortes.insert(0, i)
            j = i
        res[k] = {"sce": float(D[k, n]), "cortes": cortes}
    return res


def particion_fisher(y, k, maxcl=None, n_min=1):
    """Partición óptima de Fisher de una serie ordenada en `k` clases contiguas.

    Parámetros
    ----------
    y : array-like o pd.Series
        Serie ordenada (por ejemplo, una componente principal mensual). Si es una Series, su
        índice se usa para fechar los cortes.
    k : int
        Número de clases contiguas (regímenes), con 1 <= k <= len(y).
    maxcl : int, opcional
        Número máximo de clases que calcula la recurrencia (por defecto, `k`).
    n_min : int, opcional
        Longitud mínima de cada clase (por defecto 1, sin restricción). Con `n_min = 1` y una
        serie univariada se usa `camiz_port.fisher`, como antes de la iteración 3b; en otro caso,
        `fisher_multivariado`. Se exige k · n_min <= n.

    Devuelve
    --------
    dict con:
        'etiquetas' : np.ndarray de enteros 1..k, la clase de cada observación;
        'limites'   : lista de límites superiores 1-based de las k clases (el último es n);
        'cortes'    : etiquetas del índice donde empieza cada clase 2..k (o posiciones 0-based
                      si `y` no tiene índice);
        'sce'       : suma de cuadrados intra-clase de la partición óptima en k clases.
    """
    if isinstance(y, pd.DataFrame) or np.asarray(y).ndim == 2:
        return _particion_general(y, k, maxcl, n_min)
    serie = y if isinstance(y, pd.Series) else pd.Series(np.asarray(y, dtype=float))
    if n_min != 1:
        return _particion_general(serie, k, maxcl, n_min)
    n = len(serie)
    if not 1 <= k <= n:
        raise ValueError(f"k debe estar entre 1 y {n}; se recibió {k}")
    maxcl = k if maxcl is None else maxcl
    if maxcl < k:
        raise ValueError("maxcl no puede ser menor que k")

    valores = serie.to_numpy(dtype=float)
    if k == 1:
        # Una sola clase: no hay cortes; la SCE es la de toda la serie
        sce = float(((valores - valores.mean()) ** 2).sum())
        return {"etiquetas": np.ones(n, dtype=int), "limites": [n], "cortes": [], "sce": sce}

    # fisher exige maxcl >= 2 para construir los límites de k >= 2
    res = fisher(valores, max(maxcl, 2))
    limites = [int(v) for v in res["mod1out"][k - 1, :k]]

    # Etiquetas: la clase c ocupa las posiciones (limite_{c-1}, limite_c] en 1-based
    etiquetas = np.empty(n, dtype=int)
    inicio = 0
    for c, lim in enumerate(limites, start=1):
        etiquetas[inicio:lim] = c
        inicio = lim

    # Comienzo de cada clase 2..k, en las etiquetas del índice de la serie
    cortes = [serie.index[lim] for lim in limites[:-1]]
    return {"etiquetas": etiquetas, "limites": limites, "cortes": cortes,
            "sce": float(res["criter"][k - 1])}


def _particion_general(y, k, maxcl, n_min):
    # Partición con longitud mínima y/o datos multivariados (fisher_multivariado)
    indice = y.index if isinstance(y, (pd.Series, pd.DataFrame)) else None
    valores = np.asarray(y, dtype=float)
    if valores.ndim == 1:
        valores = valores[:, None]
    n = valores.shape[0]
    if not 1 <= k <= n:
        raise ValueError(f"k debe estar entre 1 y {n}; se recibió {k}")
    maxcl = k if maxcl is None else maxcl
    if maxcl < k:
        raise ValueError("maxcl no puede ser menor que k")
    if k * n_min > n:
        raise ValueError(f"k · n_min = {k * n_min} supera n = {n}")
    res = fisher_multivariado(valores, k_max=maxcl, n_min=n_min)[k]
    bordes = [0] + res["cortes"] + [n]
    etiquetas = np.empty(n, dtype=int)
    for c, (a, b) in enumerate(zip(bordes[:-1], bordes[1:]), start=1):
        etiquetas[a:b] = c
    cortes = [indice[c] for c in res["cortes"]] if indice is not None else list(res["cortes"])
    return {"etiquetas": etiquetas, "limites": bordes[1:], "cortes": cortes, "sce": res["sce"]}


# ---- Tarea D3 (iteración 3b): datación PCA-MM12 sin torch (notebook 09a) -----------------
#
# Traducción de `datar`, `mm_causal`, `pca_basico` y del chunk `b8-estabilidad-cortes` del Rmd,
# con el orden de operaciones de R donde puede cambiar un empate (medias con acumulador long
# double, como colMeans; media móvil con el orden de stats::filter). La regla del codo del 09 es
# la regla K de D12 (decisiones.qmd): primero el umbral de 10 % y, si no elige, la caída máxima.

CRITERIOS_DATACION = ("codo (caída máxima)", "Calinski-Harabász k gl (aede)",
                      "Calinski-Harabász k-1 gl (habitual)", "regla K (D12)")


def estandarizar_r(X):
    """Estandarización del Rmd (divisor n) con las medias de colMeans (long double)."""
    X = np.asarray(X, dtype=float)
    n = X.shape[0]
    m = (np.sum(X.astype(np.longdouble), axis=0) / n).astype(np.float64)
    c = X - m
    s = np.sqrt((np.sum((c * c).astype(np.longdouble), axis=0) / n).astype(np.float64))
    return c / s


def media_movil_causal(x, w):
    """stats::filter(x, rep(1/w, w), sides = 1): z_t = sum_{j=0}^{w-1} (1/w) x_{t-j}, en ese orden.

    Las primeras w - 1 posiciones quedan en NaN, como en R.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    r = np.full(n, np.nan)
    if n < w:
        return r
    z = np.zeros(n - w + 1)
    for j in range(w):
        z = z + (1 / w) * x[w - 1 - j:n - j]
    r[w - 1:] = z
    return r


def scores_pca_rcamiz(X):
    """Scores del PCA de la matriz de correlaciones con la regla de signo de Rcamiz (pca_basico).

    Devuelve (valores propios, vectores orientados, scores) a partir de X sin estandarizar.
    """
    from src import camiz_port as cp
    Z = estandarizar_r(X)
    val, V = cp._eigen_sim(cp._crossprod_ref(Z) / len(Z))
    V = V.copy()
    for k in range(V.shape[1]):
        v = V[:, k]
        if np.sum(v[v < 0] ** 2) > np.sum(v[v > 0] ** 2):
            V[:, k] = -v
    return val, V, Z @ V


def datar(Y, k_max=10, n_min=12, umbral=0.10):
    """Datación como `datar` del Rmd: Fisher multivariado sobre Y estandarizada.

    Devuelve un dict con la tabla por k (sce, reducción relativa al pasar de k a k + 1 y las dos
    variantes de Calinski-Harabász), los k elegidos por cada criterio y la partición por k:
      - k_caida: codo por caída máxima de la reducción (k en 2..K-1);
      - k_codo: regla K (D12): menor k con reducción < umbral; si no hay, k_caida;
      - k_ch, k_ch1: máximo del CH con k y con k - 1 grados de libertad;
      - k_max_efectivo: mayor k factible (k · n_min <= n).
    """
    from src.camiz_port import ch_variantes
    Ys = estandarizar_r(Y)
    res = fisher_multivariado(Ys, k_max=k_max, n_min=n_min)
    ks = np.array(sorted(res))
    sce = np.array([res[k]["sce"] for k in ks])
    reduccion = np.append(-np.diff(sce) / sce[:-1], np.nan)
    bajo = np.nonzero(reduccion < umbral)[0]
    caida = np.concatenate([[np.nan], reduccion[:-1]]) - reduccion
    k_caida = int(ks[np.nanargmax(caida)])
    if len(bajo):
        k_codo, regla = int(ks[bajo].min()), "umbral"
    else:
        k_codo, regla = k_caida, "caida"
    ch = ch_variantes(sce, len(Ys))
    tabla = pd.DataFrame({"k": ks, "sce": sce, "reduccion": reduccion, "ch": ch["k"], "ch1": ch["k1"]})
    return {"res": res, "tabla": tabla, "k_codo": k_codo, "regla_codo": regla, "k_caida": k_caida,
            "k_ch": int(ks[np.nanargmax(ch["k"])]), "k_ch1": int(ks[np.nanargmax(ch["k1"])]),
            "k_max_efectivo": int(ks.max())}


def fechas_corte(cortes, fechas):
    """Primer mes de cada régimen nuevo, en formato AAAA-MM (como `fechas_corte` del Rmd)."""
    return [pd.Timestamp(fechas[c]).strftime("%Y-%m") for c in cortes]


def grilla_datacion(S, fechas, maxcls=(10, 15, 20), n_min=12, umbral=0.10):
    """Grilla maxcl × criterio de la datación (tarea D3), en formato largo.

    S: scores ya suavizados (sin los NaN iniciales); fechas: las de sus filas. La columna
    `k_en_tope` vale True si el k elegido es el mayor k factible de la grilla (k_max_efectivo, que
    con n_min = 12 puede ser menor que maxcl).

    D17.1 (26-oct-2026): `n_segmentos_en_minimo` cuenta los tramos de exactamente n_min meses y
    `segmentos_en_minimo` marca como artefacto las soluciones en que **todos** los tramos miden
    n_min (lectura literal de D17.1). Con n = 217 meses suavizados y n_min = 12, la marca literal
    no puede cumplirse (217 no es múltiplo de 12); por eso se informa también el conteo.
    """
    filas = []
    n = len(S)
    for maxcl in maxcls:
        d = datar(S, k_max=maxcl, n_min=n_min, umbral=umbral)
        elegidos = [("codo (caída máxima)", d["k_caida"], "caida"),
                    ("Calinski-Harabász k gl (aede)", d["k_ch"], ""),
                    ("Calinski-Harabász k-1 gl (habitual)", d["k_ch1"], ""),
                    ("regla K (D12)", d["k_codo"], d["regla_codo"])]
        for criterio, k, regla in elegidos:
            largos = np.diff([0] + list(d["res"][k]["cortes"]) + [n])
            filas.append({"maxcl": maxcl, "k_max_efectivo": d["k_max_efectivo"], "criterio": criterio,
                          "k": k, "k_en_tope": k == d["k_max_efectivo"], "regla_k": regla,
                          "cortes": " ".join(fechas_corte(d["res"][k]["cortes"], fechas)),
                          "n_segmentos_en_minimo": int(np.sum(largos == n_min)),
                          "segmentos_en_minimo": bool(np.all(largos == n_min))})
    return pd.DataFrame(filas)


def estabilidad_cortes(Z, boot_cargas, boot_valores, cortes_ref, k_ref, ventana=12, n_min=12,
                       tolerancia=3, d=3):
    """Proporción de réplicas bootstrap que reproducen cada corte a ±tolerancia filas (b8).

    En cada réplica b los scores se recalculan con las cargas emparejadas de la réplica
    (V = cargas / sqrt(valor propio)), se suavizan con la media causal y se parten con Fisher en
    k_ref clases de al menos n_min meses. Devuelve (frecuencias, cortes de cada réplica).
    """
    Z = np.asarray(Z, dtype=float)
    cortes_b = []
    for b in range(boot_cargas.shape[0]):
        V = np.column_stack([boot_cargas[b, :, k] / np.sqrt(boot_valores[b, k]) for k in range(d)])
        Sb = Z @ V
        Sm = np.column_stack([media_movil_causal(Sb[:, k], ventana) for k in range(d)])[ventana - 1:]
        r = fisher_multivariado(estandarizar_r(Sm), k_max=k_ref, n_min=n_min)[k_ref]
        cortes_b.append(np.array(r["cortes"]))
    frec = np.array([np.mean([np.any(np.abs(cb - c0) <= tolerancia) for cb in cortes_b])
                     for c0 in cortes_ref])
    return frec, cortes_b
