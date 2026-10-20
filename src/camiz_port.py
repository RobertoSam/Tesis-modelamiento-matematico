# =============================================================================
# camiz_port.py · Port a Python de R/camiz_port.R (decisión D6)
#
# Métodos y código original: Dr. Sergio Camiz, paquete AedeClahfac 1.2 (GPL >= 3).
# La referencia es la versión en R puro R/camiz_port.R, validada contra el binario
# AedeClahfac 1.2 (R/validacion_port_camiz.R). Este módulo la traduce línea a línea
# para que el análisis en Python reproduzca los resultados de R (paridad).
#
# Funciones principales (mismo nombre que en R, sin el sufijo _r):
#   fisher(y, maxcl)              partición óptima de Fisher (reemplaza a fishersub)
#   agrega(R)                     jerarquía de la HFC por vecinos reducibles (agrega5)
#   clahfacsub(don)               rutina completa clahfacsub (salida cruda)
#   clahfac(don)                  HFC (clahfac de AedeClahfac): jerarquía, índices, factores
#   clahpart(res, noeud, exch)    particiones a partir de los nodos superiores
#   partclas(hier, ncl)           partición en ncl clases (.partclas_ac)
#   hc2axes(hier)                 coordenadas de los nodos del dendrograma (.hc2axes_ac)
#   dendhier(hier, ncl)           partición del dendrograma (sin gráfico)
#   aede(serie, ...)              EPCA con datación por Fisher y Calinski-Harabász
#   bstatw(x, w), ustatw(x, w)    estadísticos ponderados (.bstatw_ac, .ustatw_ac)
#   covp(x, y)                    covarianza con divisor n (.covp_ac)
# Utilidades del Rmd que dependen de ellas:
#   ch_variantes(sce, n)          Calinski-Harabász con k y k - 1 grados de libertad
#   resumen_aede(...)             codo, k de CH y fechas de corte (bloque b4-aede)
#   cofenetica(h), cor_cofenetica(h1, h2)  correlación cofenética (dendextend)
#   rand_ajustado(a, b)           índice de Rand ajustado (Rmd)
#
# Convenciones del port
#   * Índices: internamente se conserva la numeración 1-based de R (nodos 1..2p-1,
#     posiciones 1..p) para que la traducción sea verificable línea a línea; las
#     matrices se rellenan con una fila/columna 0 sin uso cuando hace falta.
#   * Sumas acumuladas: R calcula cumsum() con acumulador de doble extendida
#     (long double); aquí se usa np.longdouble para reproducir esas cifras bit a bit
#     en los lugares donde influyen en un argmin (Fisher).
#   * Empates: which.min/which.max de R devuelven el primer índice, igual que
#     np.argmin/np.argmax.
#   * Comportamientos del binario documentados en R/camiz_port.R (poid sin efecto,
#     Eigentab con NIPALS de dos iteraciones, correp con último elemento diagonal en 0,
#     rho que no se reinicia entre fases) se reproducen tal cual.
# =============================================================================

from __future__ import annotations

import numpy as np
import pandas as pd

XINFINI = 1e6


# ---- Utilidades numéricas que imitan a R --------------------------------------

def _cumsum_r(x):
    """cumsum() de R: acumulador long double, resultado redondeado a double."""
    return np.cumsum(np.asarray(x, dtype=np.longdouble)).astype(np.float64)


def _sum_r(x):
    """sum() de R: suma secuencial con acumulador long double."""
    x = np.asarray(x, dtype=np.longdouble).ravel()
    return float(np.cumsum(x)[-1]) if x.size else 0.0


def _colsums_r(m):
    """colSums() de R: suma secuencial por columna con acumulador long double."""
    m = np.asarray(m, dtype=np.longdouble)
    return np.cumsum(m, axis=0)[-1].astype(np.float64)


def _crossprod_ref(a, b=None):
    """crossprod(a, b) = t(a) %*% b con el orden de suma del BLAS de referencia.

    El BLAS de referencia (dsyrk/dgemm) acumula cada elemento en double de forma
    secuencial sobre las filas; se reproduce ese orden para que las cifras de la HFC
    coincidan bit a bit con R cuando R usa el BLAS de referencia (como en este entorno).
    """
    a = np.asarray(a, dtype=float)
    b = a if b is None else np.asarray(b, dtype=float)
    c = np.zeros((a.shape[1], b.shape[1]))
    for fila_a, fila_b in zip(a, b):
        c = c + np.multiply.outer(fila_a, fila_b)
    return c


def _media_r(x):
    """Media de una columna como en el C de stats::cor (dos pasadas en long double)."""
    xl = np.asarray(x, dtype=np.longdouble)
    n = len(xl)
    tmp = np.cumsum(xl)[-1] / n
    if np.isfinite(float(tmp)):
        tmp = tmp + np.cumsum(xl - tmp)[-1] / n
    return float(tmp)


def _cor_r(x, y=None):
    """cor() de Pearson de R, con el mismo orden de operaciones que su código C.

    Medias en dos pasadas con long double; productos cruzados en double acumulados en
    long double; división por n - 1 y por el producto de las desviaciones, con el
    resultado acotado a [-1, 1]. Reproducir el redondeo importa en los nodos de la HFC
    con empate exacto, donde la regla de signo compara dos sumas iguales.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    y = x if y is None else np.asarray(y, dtype=float)
    if y.ndim == 1:
        y = y[:, None]
    n1 = x.shape[0] - 1
    xc = x - np.array([_media_r(x[:, i]) for i in range(x.shape[1])])
    yc = y - np.array([_media_r(y[:, j]) for j in range(y.shape[1])])
    ld = np.longdouble
    sxy = np.cumsum((xc[:, :, None] * yc[:, None, :]).astype(ld), axis=0)[-1]
    ans = (sxy / n1).astype(np.float64)
    sx = np.sqrt(np.cumsum((xc * xc).astype(ld), axis=0)[-1] / n1).astype(np.float64)
    sy = np.sqrt(np.cumsum((yc * yc).astype(ld), axis=0)[-1] / n1).astype(np.float64)
    ans = ans / np.multiply.outer(sx, sy)
    return np.clip(ans, -1.0, 1.0)


def _cov_r(x, y=None):
    """cov() de R (divisor n - 1), con el mismo orden de operaciones que su código C."""
    x = np.asarray(x, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    y = x if y is None else np.asarray(y, dtype=float)
    if y.ndim == 1:
        y = y[:, None]
    n1 = x.shape[0] - 1
    xc = x - np.array([_media_r(x[:, i]) for i in range(x.shape[1])])
    yc = y - np.array([_media_r(y[:, j]) for j in range(y.shape[1])])
    sxy = np.cumsum((xc[:, :, None] * yc[:, None, :]).astype(np.longdouble), axis=0)[-1]
    return (sxy / n1).astype(np.float64)


def covp(data1, data2=None):
    """Port de .covp_ac: covarianza con divisor n, (n - 1)/n * cov()."""
    n = np.asarray(data1).shape[0]
    return (n - 1) / n * _cov_r(data1, data2)


# Motor de valores propios: numpy (por defecto, portable) o el dsyevr del LAPACK de
# referencia del sistema vía ctypes (opcional, solo para verificar paridad bit a bit con R
# cuando R usa ese mismo LAPACK, como en el entorno de la tesis).
_LAPACK_REF = None


def activar_lapack_referencia(ruta="/usr/lib/x86_64-linux-gnu/lapack/liblapack.so.3"):
    """Usa dsyevr del LAPACK de referencia (el que llama eigen() de R) en lugar de numpy.

    Devuelve True si la biblioteca se pudo cargar. Solo sirve para aislar diferencias
    numéricas entre rutinas de valores propios; los resultados de la tesis no dependen de ello.
    """
    global _LAPACK_REF
    import ctypes
    try:
        _LAPACK_REF = ctypes.CDLL(ruta)
        _LAPACK_REF.dsyevr_
    except (OSError, AttributeError):
        _LAPACK_REF = None
    return _LAPACK_REF is not None


def desactivar_lapack_referencia():
    """Vuelve al motor por defecto (numpy.linalg.eigh)."""
    global _LAPACK_REF
    _LAPACK_REF = None


def _dsyevr_ref(m, solo_valores=False):
    """eigen(m, symmetric = TRUE) de R: dsyevr con RANGE = 'A', UPLO = 'L' (JOBZ = 'N' si solo valores)."""
    import ctypes as c
    a = np.array(m, dtype=float, order="F")
    n = a.shape[0]
    jobz, rng, uplo = c.c_char(b"N" if solo_valores else b"V"), c.c_char(b"A"), c.c_char(b"L")
    N = c.c_int(n)
    vl, vu, abstol = c.c_double(0), c.c_double(0), c.c_double(0)
    il, iu, M, info = c.c_int(0), c.c_int(0), c.c_int(0), c.c_int(0)
    w = np.zeros(n)
    z = np.zeros((n, n), order="F")
    isuppz = np.zeros(2 * n, dtype=np.int32)
    ptr = lambda x: x.ctypes.data_as(c.c_void_p)

    def llamar(work, lwork, iwork, liwork):
        _LAPACK_REF.dsyevr_(c.byref(jobz), c.byref(rng), c.byref(uplo), c.byref(N), ptr(a), c.byref(N),
                            c.byref(vl), c.byref(vu), c.byref(il), c.byref(iu), c.byref(abstol), c.byref(M),
                            ptr(w), ptr(z), c.byref(N), ptr(isuppz), work, c.byref(lwork), iwork,
                            c.byref(liwork), c.byref(info), c.c_size_t(1), c.c_size_t(1), c.c_size_t(1))

    tmp, itmp = c.c_double(0), c.c_int(0)
    llamar(c.byref(tmp), c.c_int(-1), c.byref(itmp), c.c_int(-1))      # consulta de espacio
    work = np.zeros(int(tmp.value))
    iwork = np.zeros(int(itmp.value), dtype=np.int32)
    llamar(ptr(work), c.c_int(len(work)), ptr(iwork), c.c_int(len(iwork)))
    if info.value != 0:
        raise RuntimeError(f"dsyevr devolvió info = {info.value}")
    return w[::-1].copy(), z[:, ::-1].copy()


def _eigen_sim(m, solo_valores=False):
    """eigen() de R para matriz simétrica: valores en orden decreciente (triángulo inferior)."""
    if _LAPACK_REF is not None:
        return _dsyevr_ref(m, solo_valores)
    val, vec = np.linalg.eigh(m, UPLO="L")
    orden = np.argsort(val)[::-1]
    return val[orden], vec[:, orden]


def strtod_r(texto):
    """Convierte un número decimal escrito en texto como lo hace R_strtod (read.csv de R).

    R acumula los dígitos en long double y divide por la potencia de 10 (calculada por
    potencias binarias, también en long double) antes de redondear a double. El doble
    redondeo hace que algunos valores difieran en 1 ulp del valor correctamente
    redondeado que da pandas (float_precision='round_trip'). Solo cubre la notación
    decimal simple de los CSV del repositorio; otros formatos se pasan a float().
    """
    t = texto.strip()
    signo = -1.0 if t.startswith("-") else 1.0
    cuerpo = t.lstrip("+-")
    ent, _, dec = cuerpo.partition(".")
    if not (ent + dec).isdigit():
        return float(t)
    ld = np.longdouble
    ans = ld(0)
    for ch in ent + dec:
        ans = ld(10) * ans + ld(ord(ch) - 48)
    n = len(dec)
    if n > 0:
        p10, fac = ld(10), ld(1)
        while n:
            if n & 1:
                fac *= p10
            n >>= 1
            p10 *= p10
        ans = ans / fac
    return signo * float(ans)


def leer_csv_como_r(ruta):
    """Lee un CSV numérico con los mismos bits que read.csv de R (columna 'fecha' como texto)."""
    crudo = pd.read_csv(ruta, dtype=str)
    out = crudo.copy()
    for c in crudo.columns:
        if c != "fecha":
            out[c] = [strtod_r(v) for v in crudo[c]]
    return out


# ---- 1. Partición óptima de Fisher (fisher_r) --------------------------------

def fisher(y, maxcl):
    """Partición óptima de Fisher (1958) de una serie ordenada (port de fisher_r).

    Devuelve un dict con 'criter' (SC intra para k = 1..maxcl; criter[0] repite el
    valor de k = 2, convención de fishersub) y 'mod1out' (matriz (maxcl+1) x (maxcl+1):
    la fila k-1 contiene los límites superiores 1-based de las k clases).
    """
    y = np.asarray(y, dtype=float)
    n = len(y)
    s1 = np.concatenate([[0.0], _cumsum_r(y)])
    s2 = np.concatenate([[0.0], _cumsum_r(y * y)])

    def sce(i, j):
        # filas i..j (1-based, inclusive); i puede ser un vector
        m = j - i + 1
        s = s1[j] - s1[i - 1]
        return s2[j] - s2[i - 1] - s * s / m

    # D y B en indexación 1-based: D[k, j], k = 1..maxcl, j = 1..n
    D = np.full((maxcl + 1, n + 1), np.inf)
    B = np.zeros((maxcl + 1, n + 1), dtype=int)
    for j in range(1, n + 1):
        D[1, j] = sce(1, j)
    for k in range(2, maxcl + 1):
        if k > n:
            break
        for j in range(k, n + 1):
            i = np.arange(k - 1, j)                 # última fila de la clase k - 1
            c = D[k - 1, i] + sce(i + 1, j)
            pos = int(np.argmin(c))                 # primer mínimo, como which.min
            D[k, j] = c[pos]
            B[k, j] = i[pos]
    criter = D[1:, n].copy()
    mod1out = np.zeros((maxcl + 1, maxcl + 1))
    for k in range(2, maxcl + 1):
        lim = [n]
        j = n
        for kk in range(k, 1, -1):
            j = B[kk, j]
            lim.insert(0, j)
        mod1out[k - 1, :k] = lim
    criter[0] = criter[1]                           # convención de fishersub
    return {"criter": criter, "mod1out": mod1out}


# ---- 2. Jerarquía de la HFC (agrega_r) ---------------------------------------

def distancia_hfc(a, b, c):
    """Distancia de la HFC entre dos nodos (segundo valor propio de su fusión).

    Devuelve (dist, l1, alpha, beta): dist = lambda2, l1 = lambda1 y (alpha, beta)
    el vector propio del primer factor.
    """
    if c != 0:
        delta = (a - b) * (a - b) + 4 * (c * c)
        l1 = ((a + b) + np.sqrt(delta)) / 2
        l2 = ((a + b) - np.sqrt(delta)) / 2
        y1 = (l1 - a) / c
        nrm = np.sqrt(1 + y1 * y1)
        return (l2, l1, 1 / nrm, y1 / nrm)
    if a >= b:
        return (b, a, 1.0, 0.0)
    return (a, b, 0.0, 1.0)


def agrega(R, variante_rho="acumula"):
    """Jerarquía de la HFC por vecinos reducibles (port de agrega_r / agrega5).

    variante_rho: "acumula" (rho no se reinicia entre fases, como el Fortran) o
    "reinicia". Devuelve nab ((p-1) x 2, nodos 1-based), indice (lambda2 de cada
    fusión), l1 (varianza del nodo agregado) y albet ((p-1) x 2).
    """
    R = np.asarray(R, dtype=float)
    p = R.shape[0]
    # cov en indexación 1-based (fila y columna 0 sin uso)
    cov = np.zeros((p + 1, p + 1))
    cov[1:, 1:] = R
    nsom = np.arange(p + 1)                         # nsom[1..p] = 1..p
    ncarsom = p
    ii = p + 1
    rho = 0.0
    nab = np.zeros((p - 1, 2), dtype=int)
    ind = np.zeros(p - 1)
    l1v = np.zeros(p - 1)
    albet = np.zeros((p - 1, 2))
    fase_a = True
    aristas = None                                  # filas: dist, u, v, alpha, beta
    naret = kmax = 0
    while True:
        if fase_a:
            if variante_rho == "reinicia":
                rho = 0.0
            kk = 0
            for u in range(1, ncarsom):
                for v in range(u + 1, ncarsom + 1):
                    rho = rho + distancia_hfc(cov[u, u], cov[v, v], cov[u, v])[0]
                    kk += 1
            rho = rho / kk
            while True:
                filas = []
                for u in range(1, ncarsom):
                    for v in range(u + 1, ncarsom + 1):
                        d = distancia_hfc(cov[u, u], cov[v, v], cov[u, v])
                        if d[0] <= rho:
                            filas.append([d[0], u, v, d[2], d[3]])
                if filas:
                    break
                rho = rho * rho
            aristas = np.array(filas, dtype=float)
            naret = aristas.shape[0]
            kmax = naret
        # Fase B: arista mínima (primera en caso de empate)
        k = int(np.argmin(aristas[:, 0]))
        dd = aristas[k, 0]
        ns = int(aristas[k, 1])
        nsp = int(aristas[k, 2])
        alphak = aristas[k, 3]
        betak = aristas[k, 4]
        j = ii - p                                  # 1-based
        nab[j - 1] = (nsom[ns], nsom[nsp])
        ind[j - 1] = dd
        albet[j - 1] = (alphak, betak)
        nsom[ns] = ii
        # recalculcov1: el nodo agregado reemplaza a ns
        nueva = alphak * cov[:, ns] + betak * cov[:, nsp]
        vns = (betak * betak) * cov[nsp, nsp] + (alphak * alphak) * cov[ns, ns] \
            + 2 * alphak * betak * cov[ns, nsp]
        cov[ns, :] = nueva
        cov[:, ns] = nueva
        cov[ns, ns] = vns
        l1v[j - 1] = vns
        # vecinos de ns o nsp en el grafo
        nva = np.zeros(ncarsom + 1, dtype=int)
        for r in range(naret):
            if aristas[r, 0] >= XINFINI:
                continue
            a = int(aristas[r, 1])
            b = int(aristas[r, 2])
            if a == ns or a == nsp:
                nva[b] = 1
            if b == ns or b == nsp:
                nva[a] = 1
        nva[ns] = 0
        nva[nsp] = 0
        for r in range(naret):
            if aristas[r, 0] >= XINFINI:
                continue
            if int(aristas[r, 1]) in (ns, nsp) or int(aristas[r, 2]) in (ns, nsp):
                aristas[r, 0] = XINFINI
                kmax -= 1
        if kmax != 0:
            for ix in range(1, ncarsom + 1):
                if nva[ix] == 0:
                    continue
                d = distancia_hfc(cov[ix, ix], cov[ns, ns], cov[ix, ns])
                if d[0] > rho:
                    continue
                libres = np.nonzero(aristas[:, 0] >= XINFINI)[0]
                if len(libres) == 0:
                    raise RuntimeError("agrega: no hay espacio libre en la lista de aristas")
                aristas[libres[0]] = (d[0], ix, ns, d[2], d[3])
                kmax += 1
        # recalculcov2: el último sommet pasa a la posición nsp
        if nsp != ncarsom:
            nsom[nsp] = nsom[ncarsom]
            cov[nsp, :] = cov[ncarsom, :]
            cov[:, nsp] = cov[:, ncarsom]
            if kmax != 0:
                for r in range(naret):
                    if aristas[r, 0] >= XINFINI:
                        continue
                    if aristas[r, 1] == ncarsom:
                        aristas[r, 1] = nsp
                    if aristas[r, 2] == ncarsom:
                        aristas[r, 2] = nsp
        if ii == 2 * p - 1:
            break
        ii += 1
        ncarsom -= 1
        fase_a = (kmax == 0)
    return {"nab": nab, "indice": ind, "l1": l1v, "albet": albet}


# ---- 3. Rutina completa clahfacsub (clahfacsub_r) -----------------------------

def clahfacsub(don, poid=None):
    """Port de clahfacsub_r: salida cruda de la HFC (mismos componentes que el Fortran).

    Los nodos y las variables se numeran 1-based, como en R. Las matrices indexadas
    por nodo (nclass, noeuind, poids) siguen el orden de R (fila 0 = nodo 1).
    """
    don = np.asarray(don, dtype=float)
    n, p = don.shape
    p2 = 2 * p - 1
    if poid is None:
        poid = np.full(n, 1 / n)
    # El binario v1.2 ignora 'poid': todos los cálculos usan pesos uniformes 1/n
    w = np.full(n, 1 / n)

    # Estadísticos ponderados, matriz de covarianzas y de correlaciones
    xmoy = _colsums_r(don * w[:, None])
    centrado = don - xmoy
    xvar = _colsums_r(centrado * centrado * w[:, None])
    datstd = centrado / np.sqrt(xvar)
    cov = _crossprod_ref(centrado * np.sqrt(w)[:, None])
    cor = cov / np.outer(np.sqrt(xvar), np.sqrt(xvar))

    # Jerarquía (agrega5): nodos p+1 ... 2p-1
    jer = agrega(cor)
    jnab = jer["nab"]
    albet = jer["albet"]
    nab = np.zeros((p - 1, 3), dtype=int)
    nab[:, :2] = jnab

    def hijos(k):
        return [] if k <= p else [int(jnab[k - p - 1, 0]), int(jnab[k - p - 1, 1])]

    def hojas_dfs(k):
        if k <= p:
            return [k]
        h = hijos(k)
        return hojas_dfs(h[0]) + hojas_dfs(h[1])

    def hojas_bfs(k):                               # orden de la subrutina coupure
        res = []
        nivel = [k]
        while True:
            sig = []
            for ll in nivel:
                if ll <= p:
                    res.append(ll)
                    continue
                for h in hijos(ll):
                    if h <= p:
                        res.append(h)
                    else:
                        sig.append(h)
            if not sig:
                break
            nivel = sig
        return res

    for j in range(1, p):
        nab[j - 1, 2] = len(hojas_dfs(p + j))

    # Padre de cada nodo y coeficiente con que entra en él (índices 1-based, 0 sin uso)
    padre = np.zeros(p2 + 1, dtype=int)
    coef = np.zeros(p2 + 1)
    coef[p2] = 1.0
    for j in range(1, p):
        a, b = int(jnab[j - 1, 0]), int(jnab[j - 1, 1])
        padre[a] = p + j
        coef[a] = albet[j - 1, 0]
        padre[b] = p + j
        coef[b] = albet[j - 1, 1]

    def peso_en(k, ancestro):
        s = 1.0
        while k != ancestro:
            s = s * coef[k]
            k = padre[k]
        return s

    peso_global = np.array([0.0] + [peso_en(k, p2) for k in range(1, p2 + 1)])
    signo = np.where(peso_global[p + 1:p2 + 1] < 0, -1.0, 1.0)   # signo[j-1], j = 1..p-1

    # Factores de nodo: A (primer factor) y B (segundo)
    Fv = np.zeros((n, p2 + 1))
    Fv[:, 1:p + 1] = datstd
    datout = np.zeros((n, 2 * (p - 1)))
    for j in range(1, p):
        a, b = int(jnab[j - 1, 0]), int(jnab[j - 1, 1])
        al, be = albet[j - 1]
        Fv[:, p + j] = al * Fv[:, a] + be * Fv[:, b]
        sb = 1.0 if be < 0 else -1.0
        datout[:, 2 * j - 2] = signo[j - 1] * Fv[:, p + j]
        datout[:, 2 * j - 1] = sb * signo[j - 1] * ((-be) * Fv[:, a] + al * Fv[:, b])

    sw = np.sqrt(w)[:, None]

    def covp_w(X, Y):
        Xc = (X - _colsums_r(X * w[:, None])) * sw
        Yc = (Y - _colsums_r(Y * w[:, None])) * sw
        return _crossprod_ref(Xc, Yc)

    covout = covp_w(datstd, datout)                 # el binario usa los datos estandarizados
    covrep = covp_w(datout, datout)
    corout = covout / np.sqrt(np.diag(covrep))[None, :]
    correp = covrep / np.outer(np.sqrt(np.diag(covrep)), np.sqrt(np.diag(covrep)))
    correp[-1, -1] = 0.0                            # el binario deja en 0 el último elemento diagonal

    # Ponderaciones de variables y nodos en el factor raíz
    poids = np.zeros((p2, 2))
    poids[:, 0] = np.concatenate([peso_global[1:p + 1], np.abs(peso_global[p + 1:p2 + 1])])
    poids[:, 1] = poids[:, 0] ** 2

    # Composición de clases, orden del dendrograma y particiones por etapa
    nclass = np.zeros((p2, p), dtype=int)
    for k in range(1, p + 1):
        nclass[k - 1, 0] = k
    for k in range(p + 1, p2):
        h = hojas_bfs(k)
        nclass[k - 1, :len(h)] = h
    nclstr = np.array(hojas_dfs(p2), dtype=int)
    nclass[p2 - 1, :] = nclstr
    ncla = np.zeros((p, p), dtype=int)
    clase = np.arange(1, p + 1)
    ncla[:, 0] = clase
    for s in range(1, p):
        clase = clase.copy()
        clase[np.isin(clase, jnab[s - 1, :2])] = p + s
        ncla[:, s] = clase
    narb = ncla[nclstr - 1, :]
    npart = np.zeros((p, p), dtype=int)
    for s in range(p):
        u = pd.unique(narb[:, s])
        npart[:len(u), s] = u

    # Nodo que une hojas consecutivas del dendrograma (ancestro común más bajo)
    def ancestros(k):
        r = [k]
        while k != p2:
            k = padre[k]
            r.append(int(k))
        return r

    nsg = np.zeros(p, dtype=int)
    for i in range(p - 1):
        a2 = set(ancestros(int(nclstr[i + 1])))
        nsg[i] = next(x for x in ancestros(int(nclstr[i])) if x in a2)

    # Dipolos: lado de cada variable según el signo de la covarianza con el factor A
    noeuind = np.zeros((p, p2), dtype=int)
    for k in range(1, p + 1):
        noeuind[k - 1, k - 1] = 2
    for j in range(1, p):
        for v in hojas_dfs(p + j):
            ps = covout[v - 1, 2 * j - 2]
            noeuind[v - 1, p + j - 1] = 2 if ps >= 0 else 1

    # Columna Eigentab: NIPALS del binario (se detiene en la segunda iteración)
    def nipals_bin(x):
        kl = int(np.nonzero((x * x).sum(axis=0) != 0)[0][0])
        th = x[:, kl].copy()
        ph = np.zeros(x.shape[1])
        for _ in range(2):
            ph = (ph + _crossprod_ref(x, th[:, None])[:, 0]) / _sum_r(th * th)
            ph = ph / np.sqrt(_sum_r(ph * ph))
            th = _crossprod_ref(x.T, ph[:, None])[:, 0]
        return np.sqrt(_sum_r(th * th))

    eigentab = np.zeros(p - 1)
    for j in range(1, p):
        x = cor.copy()
        fuera = noeuind[:, p + j - 1] == 0
        x[fuera, :] = 0.0
        x[:, fuera] = 0.0
        eigentab[j - 1] = nipals_bin(x)

    traza = _sum_r(np.diag(cor))
    l1 = jer["l1"]
    l2 = jer["indice"]
    ddo = np.column_stack([
        l1, l2, 100 * l1 / (l1 + l2), 100 * l2 / (l1 + l2), 100 * l1 / traza,
        100 * l2 / traza, _cumsum_r(100 * l2 / traza), eigentab, l1 / eigentab])

    eig_conv = np.zeros(p - 1)
    for j in range(1, p):
        v = nclass[p + j - 1]
        v = v[v > 0] - 1
        eig_conv[j - 1] = np.max(_eigen_sim(cor[np.ix_(v, v)], solo_valores=True)[0])

    return {"units": n, "variables": p, "don": don, "poid": poid, "datstd": datstd,
            "xmoy": xmoy, "xvar": xvar, "cov": cov, "cor": cor, "nab": nab, "ddo": ddo,
            "albet": albet, "poids": poids, "vt": np.array([_sum_r(l2), l1[p - 2], traza]),
            "nclstr": nclstr, "nsg": nsg, "nclass": nclass, "ncla": ncla, "narb": narb,
            "npart": npart, "noeuind": noeuind, "datout": datout, "covout": covout,
            "corout": corout, "covrep": covrep, "correp": correp, "error": 0,
            "eigentab_convergido": eig_conv}


# ---- 4. clahfac, clahpart, partclas, hc2axes, dendhier ------------------------

COLUMNAS_HIERAR = ["ngr", "N1", "N2", "Num", "Weight", "Weight2", "Eigenv", "Index", "Loc_%1",
                   "Loc_%2", "Glob_%1", "Glob_%2", "Cum_%2", "Eigentab", "Ratio", "Weight_N1",
                   "Weight_N2"]


def clahfac(don, poid=None, verbose=False):
    """Clasificación Factorial Jerárquica (port de clahfac_r con out = TRUE).

    don: DataFrame (filas = unidades, columnas = variables) o matriz.
    Devuelve un dict con las mismas componentes que el objeto 'clahfac' de R:
    data, mevar, cov, cor, weight, hierar (DataFrame, índice p+1..2p-1), inertia,
    nclass, ncla, noeuind, narb, npart, repvar, covout, corout, covrep, correp y
    hier (dict tipo hclust: merge, height, order, labels).
    """
    df = don if isinstance(don, pd.DataFrame) else pd.DataFrame(np.asarray(don, dtype=float))
    X = df.to_numpy(dtype=float)
    nind, nvar = X.shape
    nvar2 = 2 * nvar - 1
    kideni = list(df.index)
    kidenj = [str(c) for c in df.columns]
    out = clahfacsub(X, poid)
    res = {"data": df}
    res["mevar"] = pd.DataFrame([out["xmoy"], out["xvar"]], index=["Means", "Variances"], columns=kidenj)
    res["cov"] = pd.DataFrame(out["cov"], index=kidenj, columns=kidenj)
    res["cor"] = pd.DataFrame(out["cor"], index=kidenj, columns=kidenj)
    res["weight"] = pd.DataFrame(out["poids"][:nvar].T, index=["Weight", "Weight2"], columns=kidenj)
    hierar = np.column_stack([np.arange(nvar - 1, 0, -1), out["nab"], out["poids"][nvar:nvar2],
                              out["ddo"], out["albet"]])
    res["hierar"] = pd.DataFrame(hierar, index=np.arange(nvar + 1, nvar2 + 1), columns=COLUMNAS_HIERAR)
    for c in ["ngr", "N1", "N2", "Num"]:
        res["hierar"][c] = res["hierar"][c].astype(int)
    vt = out["vt"]
    res["inertia"] = pd.DataFrame([vt, vt / vt[2] * 100], index=["Inertia", "Percent"],
                                  columns=["Hierarchy", "Repr_Var", "Total"])
    kidsrt = [kidenj[i - 1] for i in out["narb"][:, 0]]
    res["nclass"] = pd.DataFrame(out["nclass"][nvar:nvar2], index=np.arange(nvar + 1, nvar2 + 1))
    res["ncla"] = pd.DataFrame(out["ncla"].T[::-1], index=list(range(nvar2, nvar, -1)) + [nvar],
                               columns=kidenj)
    res["noeuind"] = pd.DataFrame(out["noeuind"][:, nvar2 - 1:nvar - 1:-1].T,
                                  index=np.arange(nvar2, nvar, -1), columns=kidenj)
    res["narb"] = pd.DataFrame(out["narb"].T[::-1], columns=kidsrt)
    res["npart"] = pd.DataFrame(out["npart"].T[::-1])
    kidenout = []
    for j in range(1, nvar):
        kidenout += [f"*{j + nvar}A*", f"*{j + nvar}B*"]
    repvar = out["datout"].copy()
    covout, corout, covrep, correp = out["covout"], out["corout"], out["covrep"], out["correp"]
    # Corrección de signo de los factores de nodo (dominan los cuadrados positivos)
    flag = False
    for i in range(1, nvar):
        fila = out["nclass"][nvar + i - 1]
        nclassa = fila[fila != 0] - 1
        nrepa = [2 * i - 2, 2 * i - 1]
        cora = _cor_r(X[:, nclassa], repvar[:, nrepa])
        for jj in range(2):
            col = cora[:, jj]
            if _sum_r(col[col < 0] ** 2) > _sum_r(col[col > 0] ** 2):
                if verbose:
                    print(f"\n changed sign at node {i} var {jj + 1} \n")
                repvar[:, nrepa[jj]] = -repvar[:, nrepa[jj]]
                flag = True
    if flag:
        covout = covp(X, repvar)
        corout = _cor_r(X, repvar)
        covrep = covp(repvar)
        correp = _cor_r(repvar)
    res["repvar"] = pd.DataFrame(repvar, index=kideni, columns=kidenout)
    res["covout"] = pd.DataFrame(covout, index=kidenj, columns=kidenout)
    res["corout"] = pd.DataFrame(corout, index=kidenj, columns=kidenout)
    res["covrep"] = pd.DataFrame(covrep, index=kidenout, columns=kidenout)
    res["correp"] = pd.DataFrame(correp, index=kidenout, columns=kidenout)
    merge = out["nab"][:, :2].copy()
    merge = np.where(merge <= nvar, -merge, merge - nvar)
    res["hier"] = {"merge": merge, "height": out["ddo"][:, 1].copy(),
                   "order": out["narb"][:, 0].copy(), "labels": kidenj,
                   "method": "clahfac", "dist.method": "correlation"}
    res["crudo"] = out
    return res


def clahpart(res, noeud=0, exch=None):
    """Port de clahpart_r: clases y coordenadas al cortar los 'noeud' nodos superiores.

    Reproduce el código original, incluida la indexación res$hierar[..., 7.8] de R, que
    se trunca a la columna 7 (Eigenv).
    """
    res = dict(res)
    X = res["data"].to_numpy(dtype=float)
    nind, nvar = X.shape
    nvarm1 = nvar - 1
    kidenj = list(res["cov"].index)
    repvar = res["repvar"].to_numpy(copy=True)
    if exch is not None:
        for e in exch:
            nv = abs(e) - nvar
            iv = 2 * nv - 1 if e > 0 else 2 * nv
            repvar[:, iv - 1] = -repvar[:, iv - 1]
        kout = list(res["repvar"].columns)
        res["repvar"] = pd.DataFrame(repvar, index=res["repvar"].index, columns=kout)
        res["covout"] = pd.DataFrame(covp(X, repvar), index=kidenj, columns=kout)
        res["corout"] = pd.DataFrame(_cor_r(X, repvar), index=kidenj, columns=kout)
        res["covrep"] = pd.DataFrame(covp(repvar), index=kout, columns=kout)
        res["correp"] = pd.DataFrame(_cor_r(repvar), index=kout, columns=kout)
    if noeud > 0:
        npart = res["npart"].to_numpy()
        classes = np.sort(npart[noeud, :noeud + 1])
        cla = classes - nvar
        cla2 = cla[cla > 0]
        clou = list(cla2) + list(range(nvar - noeud, nvar))
        filas = []
        cs = cla[cla <= 0] + nvar
        for c in cs:
            filas.append((str(c), kidenj[c - 1]))
        nclass = res["nclass"].to_numpy()
        cc = nclass[cla2 - 1]
        iclas = (cc != 0).sum(axis=1)
        res["classes"] = np.vstack([classes, np.concatenate([np.ones(len(cs), dtype=int), iclas])])
        for i in range(cc.shape[0]):
            nombre = str(res["nclass"].index[cla2[i] - 1])
            for v in cc[i, :iclas[i]]:
                filas.append((nombre, kidenj[v - 1]))
        res["itemclas"] = pd.DataFrame(filas, columns=["class", "label"])
        res["clout"] = [x for c in clou for x in (2 * c - 1, 2 * c)]
        hier = res["hierar"].to_numpy(dtype=float)
        corout = res["corout"].to_numpy()
        correp = res["correp"].to_numpy()
        coord = []
        for nn in range(1, noeud + 1):
            coor = {}
            node = nvarm1 - nn + 1
            nodeb = 2 * node
            nodea = nodeb - 1
            vars_n = nclass[node - 1]
            vars_n = vars_n[vars_n != 0] - 1
            cols_f = [nodea - 1, nodeb - 1]
            datcl = [X[:, vars_n], repvar[:, cols_f]]
            coor["var"] = corout[np.ix_(vars_n, cols_f)]
            coor["faccov"] = np.sqrt(hier[node - 1, 6:8])
            naj = int(hier[node - 1, 1])
            nbj = int(hier[node - 1, 2])
            coor["sup"] = None
            coor["supcov"] = None
            if min(naj, nbj) > nvar:
                naj -= nvar
                nbj -= nvar
                idx = [2 * naj - 2, 2 * naj - 1, 2 * nbj - 2, 2 * nbj - 1]
                sup = correp[np.ix_(idx, cols_f)]
                # R: hierar[c(naj, nbj), 7.8] = columna 7; el vector de 2 se recicla por filas
                v = np.sqrt(hier[[naj - 1, nbj - 1], 6])
                coor["sup"] = sup
                coor["supcov"] = sup * np.tile(v, 2)[:, None]
                datcl.append(repvar[:, idx])
            elif max(naj, nbj) < nvar:
                pass
            elif naj > nvar:
                naj -= nvar
                idx = [2 * naj - 2, 2 * naj - 1]
                sup = correp[np.ix_(idx, cols_f)]
                coor["sup"] = sup
                coor["supcov"] = sup * np.sqrt(hier[naj - 1, 6:8])[:, None]
                datcl.append(repvar[:, idx])
            elif nbj > nvar:
                nbj -= nvar
                idx = [2 * nbj - 2, 2 * nbj - 1]
                sup = correp[np.ix_(idx, cols_f)]
                coor["sup"] = sup
                coor["supcov"] = sup * np.sqrt(hier[nbj - 1, 6:8])[:, None]
                datcl.append(repvar[:, idx])
            coor["dat"] = np.column_stack(datcl)
            coor["ind"] = repvar[:, cols_f]
            coord.append(coor)
        res["coord"] = coord
    return res


def partclas(hier, ncl):
    """Port de .partclas_ac: partición del dendrograma en ncl clases.

    'Position' es el paso de fusión de la clase (o -hoja si la clase es una sola serie).
    Devuelve dict con partition (DataFrame Position, Class, Number), class, numitem,
    ord.partition y ord.class.
    """
    labels = hier["labels"]
    p = len(labels)
    merge = hier["merge"]
    clasnod = np.zeros((p, p), dtype=int)
    clasnod[0] = -np.arange(1, p + 1)
    for i in range(1, p):
        clasnod[i] = clasnod[i - 1]
        ia, ib = merge[i - 1]
        clasnod[i, clasnod[i - 1] == ia] = i
        clasnod[i, clasnod[i - 1] == ib] = i
    clasnod = clasnod[1:]
    orden = np.asarray(hier["order"]) - 1
    clasnodord = clasnod[:, orden]
    pos = clasnod[p - ncl - 1]
    partition = pd.DataFrame({"Position": pos.astype(float),
                              "Class": [f"*{x + p}*" for x in pos],
                              "Number": np.arange(1, p + 1)}, index=labels)
    u = partition[["Position", "Class"]].drop_duplicates()
    clase = pd.Series(u["Position"].to_numpy(), index=u["Class"].to_numpy()).sort_values(kind="stable")
    posord = clasnodord[p - ncl - 1]
    partitord = pd.DataFrame({"Position": posord.astype(float),
                              "Class": [f"*{x + p}*" for x in posord]},
                             index=[labels[i] for i in orden])
    uo = partitord.drop_duplicates()
    claseord = pd.Series(uo["Position"].to_numpy(), index=uo["Class"].to_numpy())
    tp = partition["Position"].value_counts().sort_index()
    tp.index = clase.index
    return {"numofclass": ncl, "partition": partition, "class": clase, "numitem": tp,
            "ord.partition": partitord, "ord.class": claseord,
            "ord.numitem": tp[claseord.index]}


def hc2axes(hier):
    """Port de .hc2axes_ac: abscisa (posición media de los hijos) y altura de cada nodo."""
    A = hier["merge"]
    n = A.shape[0] + 1
    order = np.asarray(hier["order"])
    zz = np.empty(len(order), dtype=float)
    zz[order - 1] = np.arange(1, len(order) + 1)      # match(1:n, order)
    xa = []
    for i in range(n - 1):
        x = []
        for ai in A[i]:
            x.append(zz[-ai - 1] if ai < 0 else xa[ai - 1])
        xa.append(np.mean(x))
    return pd.DataFrame({"x.axis": xa, "y.axis": hier["height"]})


def dendhier(hier, ncl):
    """Port de dendhier_r sin el gráfico: devuelve la partición en ncl clases."""
    return partclas(hier, ncl)


# ---- 5. EPCA del asesor (aede_r) -----------------------------------------------

def ustatw(x, w):
    """Port de .ustatw_ac: media, varianza, desviación y coef. de variación ponderados."""
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    sw = _sum_r(w)
    if sw != 0:
        w = w / sw
    # t(w) %*% x: producto matricial con el orden de suma del BLAS de referencia
    m = _crossprod_ref(w[:, None], x)[0]
    v = _crossprod_ref(w[:, None], (x - m) ** 2)[0]
    sd = np.sqrt(v)
    with np.errstate(divide="ignore", invalid="ignore"):   # R devuelve Inf/NaN sin aviso
        cv = sd / m
    return np.column_stack([m, v, sd, cv])


def bstatw(x, w):
    """Port de .bstatw_ac: estadísticos univariados, covarianzas y correlaciones ponderados."""
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    sw = _sum_r(w)
    if sw != 0:
        w = w / sw
    sx = ustatw(x, w)
    xc = x - sx[:, 0]
    # t(xc) %*% diag(w) %*% xc, evaluado de izquierda a derecha como en R
    cova = _crossprod_ref(_crossprod_ref(xc, np.diag(w)).T, xc)
    with np.errstate(invalid="ignore", divide="ignore"):
        corr = cova / np.outer(sx[:, 2], sx[:, 2])
    corr[np.isnan(corr)] = 0.0
    return {"univariate": sx, "covariances": cova, "correlations": corr}


def pesos_aede(nw, nsd=0):
    """Pesos de la ventana de aede: uniformes (nsd = 0) o gaussianos."""
    weight = np.full(nw, 1 / nw)
    if nsd != 0:
        am = (nw + 1) / 2
        s = (nw - 1) / np.sqrt(2)
        i = np.arange(1, nw + 1)
        ex = (i - am) / s
        weight = np.exp(-0.5 * (ex * nsd) ** 2)
        weight = weight / _sum_r(weight)
    return weight


def aede(serie, nw, ndim=3, nsd=0, maxcl=10, standard=True,
         title="Evolutionary Principal Component Analysis"):
    """EPCA del asesor con datación por Fisher (port de aede_r).

    serie: DataFrame (filas = meses ordenados; el índice da las etiquetas) o matriz.
    nw: tamaño de la ventana (paso 1); nsd: 0 = pesos uniformes, > 0 = gaussianos.
    Devuelve dict con weights, eigenvalues (DataFrame wn x ndim, índice = fila central
    de la ventana: posición nw/2 + 1 en R), least_squares_differences, correlationsgn y
    correlationlsq (arreglos wn x p x ndim) y cutpoints['part'] (DataFrame con n,
    Within ssq, Calinski-Harabasz y los límites superiores v_1..v_maxcl, 1-based).
    """
    df = serie if isinstance(serie, pd.DataFrame) else pd.DataFrame(np.asarray(serie, dtype=float))
    Xall = df.to_numpy(dtype=float)
    n, p = Xall.shape
    wn = n - nw + 1
    # rownames(serie)[(1 + nw/2):(wn + nw/2)] (R trunca los índices fraccionarios)
    ini = int(np.floor(1 + nw / 2))
    etiquetas = list(df.index[ini - 1:ini - 1 + wn])
    autoval = np.zeros((wn, ndim))
    dif = np.zeros(wn)
    correlsn = np.zeros((wn, p, ndim))
    correlsq = np.zeros((wn, p, ndim))
    weight = pesos_aede(nw, nsd)
    autveto = None
    for i in range(wn):
        dati = Xall[i:i + nw, :p]
        bstat = bstatw(dati, weight)
        covm = bstat["correlations"] if standard else bstat["covariances"]
        val, vec = _eigen_sim(covm)
        autoval[i] = val[:ndim]
        autvet = vec[:p, :ndim].copy()
        # Regla de signo propia de aede: suma lineal de coeficientes
        for k in range(ndim):
            col = autvet[:, k]
            corp = _sum_r(col[col > 0])
            corn = _sum_r(col[col < 0])
            if abs(corn) > corp:
                autvet[:, k] = -autvet[:, k]
        correlsn[i] = autvet * np.sqrt(autoval[i])
        if i != 0:
            # Alineación con la ventana anterior (mínimos cuadrados)
            for k in range(ndim):
                corp = _sum_r((autvet[:, k] - autveto[:, k]) ** 2)
                corn = _sum_r((autvet[:, k] + autveto[:, k]) ** 2)
                if abs(corn) < corp:
                    autvet[:, k] = -autvet[:, k]
            # como en R: se usa el último k del bucle
            dif[i] = _sum_r((autvet[:, ndim - 1] - autveto[:, ndim - 1]) ** 2)
        autveto = autvet
        correlsq[i] = autvet * np.sqrt(autoval[i])
    nombres = [f"Dim_{k:02d}" for k in range(1, ndim + 1)]
    res = {"weights": weight,
           "eigenvalues": pd.DataFrame(autoval, index=etiquetas, columns=nombres),
           "least_squares_differences": dif,
           "correlationsgn": correlsn, "correlationlsq": correlsq,
           "series": [str(c) for c in df.columns], "title": title}
    # Datación del primer valor propio con Fisher y Calinski-Harabász (k gl, como aede)
    nbind = wn
    y = autoval[:, 0]
    # scale(y, center = TRUE): colMeans con acumulador long double
    yc = y - float(np.cumsum(y.astype(np.longdouble))[-1] / nbind)
    tss = _sum_r(yc * yc)
    outpart = fisher(y, maxcl)
    df1 = np.arange(1, maxcl + 1)
    df2 = nbind - df1
    wss = outpart["criter"][:maxcl].copy()
    wss[0] = tss
    bss = tss - wss
    CH = (bss / df1) / (wss / df2)
    classes = outpart["mod1out"][:maxcl, :maxcl]
    part = pd.DataFrame(np.column_stack([df1, wss, CH, classes]),
                        columns=["n", "Within ssq", "Calinski-Harabasz"] +
                        [f"v_{k}" for k in range(1, maxcl + 1)])
    res["cutpoints"] = {"title": title,
                        "act": "Partitioning of variable 1 minimizing the inertia of 2 :",
                        "part": part}
    return res


# ---- 6. Utilidades del Rmd que dependen de aede / clahfac ----------------------

def ch_variantes(sce, n):
    """Calinski-Harabász para k = 1..K a partir de las SC intra (sce[0] = total).

    'k': fórmula del código de aede (grados de libertad k y n - k).
    'k1': forma habitual (k - 1 y n - k). k = 1 no está definido (NaN).
    """
    sce = np.asarray(sce, dtype=float)
    k = np.arange(1, len(sce) + 1)
    tss = sce[0]
    with np.errstate(invalid="ignore", divide="ignore"):
        ch_k = ((tss - sce) / k) / (sce / (n - k))
        ch_k1 = ((tss - sce) / (k - 1)) / (sce / (n - k))
    ch_k[0] = np.nan
    ch_k1[0] = np.nan
    return {"k": ch_k, "k1": ch_k1}


def resumen_aede(a):
    """Codo, k de Calinski-Harabász (dos variantes) y fechas de corte (bloque b4-aede).

    Codo: k en que más cae la reducción relativa de la SC intra al agregar una clase.
    Las fechas de corte son la etiqueta de la primera ventana de cada clase nueva.
    """
    part = a["cutpoints"]["part"]
    fv = list(a["eigenvalues"].index)
    nb = len(fv)
    wss = part["Within ssq"].to_numpy()
    red = np.append(-np.diff(wss) / wss[:-1], np.nan)
    caida = red[:-2] - red[1:-1]
    k_codo = int(np.argmax(caida)) + 2
    vcols = [c for c in part.columns if c.startswith("v_")]

    def limites(k):
        l = part.loc[k - 1, vcols].to_numpy().astype(int)
        l = l[(l > 0) & (l < nb)]
        return [fv[x] for x in l]                    # fv[l + 1] 1-based = fv[l] 0-based

    ch = ch_variantes(wss, nb)
    if not np.allclose(ch["k"][1:], part["Calinski-Harabasz"].to_numpy()[1:], rtol=1.5e-8, atol=0):
        raise AssertionError("ch_variantes no reproduce el CH de aede")
    chk = part["Calinski-Harabasz"].to_numpy()
    k_ch = int(np.argmax(chk)) + 1
    k_ch1 = int(np.nanargmax(ch["k1"])) + 1
    return {"part": part, "red": red, "k_codo": k_codo, "ch1": ch["k1"],
            "k_ch": k_ch, "k_ch1": k_ch1, "cortes_codo": limites(k_codo),
            "cortes_ch": limites(k_ch), "cortes_ch1": limites(k_ch1)}


def cofenetica(hier):
    """Matriz cofenética de una jerarquía tipo hclust (altura del ancestro común).

    Equivale a cophenetic(as.dendrogram(h)) de R: la altura de la fusión en que dos
    hojas quedan juntas por primera vez, aun si las alturas no son monótonas.
    """
    merge = hier["merge"]
    h = hier["height"]
    p = merge.shape[0] + 1
    C = np.zeros((p, p))
    miembros = {}
    for s in range(p - 1):
        grupos = []
        for x in merge[s]:
            grupos.append([-x - 1] if x < 0 else miembros[x])
        a, b = grupos
        C[np.ix_(a, b)] = h[s]
        C[np.ix_(b, a)] = h[s]
        miembros[s + 1] = a + b
    return C


def cor_cofenetica(h1, h2):
    """Correlación de Pearson entre las distancias cofenéticas (dendextend::cor_cophenetic).

    Las hojas se alinean por etiqueta, como hace dendextend al ordenar la matriz.
    """
    C1 = pd.DataFrame(cofenetica(h1), index=h1["labels"], columns=h1["labels"])
    C2 = pd.DataFrame(cofenetica(h2), index=h2["labels"], columns=h2["labels"])
    et = sorted(h1["labels"])
    C1 = C1.loc[et, et].to_numpy()
    C2 = C2.loc[et, et].to_numpy()
    # Triángulo inferior por columnas: el orden de un objeto 'dist' de R
    p = len(et)
    filas = [i for j in range(p) for i in range(j + 1, p)]
    cols = [j for j in range(p) for i in range(j + 1, p)]
    return float(_cor_r(C1[filas, cols], C2[filas, cols])[0, 0])


def rand_ajustado(a, b):
    """Índice de Rand ajustado entre dos particiones (misma fórmula que el Rmd)."""
    t = pd.crosstab(np.asarray(a), np.asarray(b)).to_numpy(dtype=float)
    n = t.sum()

    def comb(x):
        x = np.asarray(x, dtype=float)
        return _sum_r(x * (x - 1) / 2)

    sij = comb(t)
    sa = comb(t.sum(axis=1))
    sb = comb(t.sum(axis=0))
    esp = sa * sb / comb(n)
    return (sij - esp) / ((sa + sb) / 2 - esp)
