# -*- coding: utf-8 -*-
"""Guion del auditor (iteración 3b, criterio 12 del plan): comprobación numérica de las piezas
formales nuevas del capítulo 2 (L2) de la tesis LaTeX, de forma independiente del código
auditado salvo donde la proposición afirma algo sobre ese código (se indica en cada bloque).

Uso: python proposiciones_3b.py RUTA_COPIA_DEL_REPOSITORIO
"""
import itertools
import math
import sys

import numpy as np
import pandas as pd
from scipy import integrate

RAIZ = sys.argv[1]
sys.path.insert(0, RAIZ)
rng = np.random.default_rng(20261029)
total, fallos = 0, []


def chequear(cond, etiqueta):
    global total
    total += 1
    if not bool(cond):
        fallos.append(etiqueta)


# ---------------------------------------------------------------------------------------------
# Pesos de la def:pesos (implementación propia, no la del repositorio)
def pesos(nw, nu):
    u = np.arange(1, nw + 1)
    if nu == 0:
        return np.full(nw, 1 / nw)
    w = np.exp(-0.5 * (nu * (u - (nw + 1) / 2) / ((nw - 1) / np.sqrt(2))) ** 2)
    return w / w.sum()


def kish(w):
    return 1 / np.sum(w ** 2)


# prop:kish (a): 1 <= n_omega <= nw; igualdades
for _ in range(3000):
    nw = int(rng.integers(1, 80))
    w = rng.random(nw) ** rng.uniform(0.2, 5)
    if rng.random() < 0.2:
        w[rng.random(nw) < 0.5] = 0
    if w.sum() == 0:
        w[0] = 1
    w = w / w.sum()
    n = kish(w)
    chequear(1 - 1e-12 <= n <= nw + 1e-9, f'kish(a) cotas nw={nw}')
for nw in range(1, 80):
    chequear(abs(kish(np.full(nw, 1 / nw)) - nw) < 1e-9, f'kish(a) uniforme nw={nw}')
    e = np.zeros(nw); e[nw // 2] = 1
    chequear(abs(kish(e) - 1) < 1e-12, f'kish(a) degenerado nw={nw}')
# (b) y (c): nu=0 da nw; nu>0 y nw>=3 da < nw; nw=2 da 2
for nw in range(2, 121):
    chequear(abs(kish(pesos(nw, 0)) - nw) < 1e-9, f'kish(b) nu=0 nw={nw}')
    for nu in (0.1, 0.5, 1, 2, 3, 5):
        k = kish(pesos(nw, nu))
        if nw >= 3:
            chequear(k < nw - 1e-9, f'kish(b) nu={nu} nw={nw}')
        else:
            chequear(abs(k - 2) < 1e-12, 'kish nw=2 iguales')
        # extremos: e^{-nu^2/4} relativo al centro
        wt = np.exp(-0.5 * (nu * (np.arange(1, nw + 1) - (nw + 1) / 2) / ((nw - 1) / np.sqrt(2))) ** 2)
        chequear(abs(wt[0] - math.exp(-nu ** 2 / 4)) < 1e-12, 'pesos extremos')


# (d): límite c(nu) y 0 < c < 1
def c_nu(nu):
    a = nu / np.sqrt(2)
    i1 = integrate.quad(lambda x: np.exp(-x ** 2 / 2), -a, a)[0]
    i2 = integrate.quad(lambda x: np.exp(-x ** 2), -a, a)[0]
    return i1 ** 2 / (2 * a * i2)


for nu in (0.3, 1, 2, 3, 4, 6):
    c = c_nu(nu)
    chequear(0 < c < 1, f'kish(d) rango nu={nu}')
    r = kish(pesos(200000, nu)) / 200000
    chequear(abs(r - c) < 1e-4, f'kish(d) limite nu={nu}: {r} vs {c}')
c3 = c_nu(3)
# Macros de la tesis (n_omega con nu = 3) recalculadas aquí: 18,2 / 27,6 / 37,0 / 46,4 y ceil
esperado = {24: ('18.2', 19), 36: ('27.6', 28), 48: ('37.0', 38), 60: ('46.4', 47)}
for nw, (txt, nh) in esperado.items():
    k = kish(pesos(nw, 3))
    chequear(f'{k:.1f}' == txt, f'macro nOmega nw={nw}: {k:.4f}')
    chequear(math.ceil(k - 1e-9) == nh, f'macro nHorn nw={nw}')
# Con el código del repositorio (afirmación sobre el código): pesos_aede y n_kish
from src import camiz_port as cp
from src.multivariado import n_kish, coef_rv
for nw in (2, 3, 24, 36, 48, 60, 101):
    for nu in (0, 3):
        chequear(np.allclose(cp.pesos_aede(nw, nu), pesos(nw, nu), rtol=0, atol=1e-15), f'pesos_aede = def:pesos nw={nw}')
        chequear(abs(n_kish(cp.pesos_aede(nw, nu)) - kish(pesos(nw, nu))) < 1e-9, 'n_kish')

# ---------------------------------------------------------------------------------------------
# def:ventana y lem:ventana-mes (fechado: centro en la fila i + floor(nw/2), 1-based)
for nw in range(1, 61):
    n = 228
    for i in range(1, n - nw + 2):
        t = i + nw // 2
        W = set(range(t - nw // 2, t + math.ceil(nw / 2)))
        chequear(W == set(range(i, i + nw)), f'def:ventana nw={nw} i={i}')
    for s in (1, 50, 120, 228):
        centros = [i + nw // 2 for i in range(1, n - nw + 2) if i <= s <= i + nw - 1]
        teor = [t for t in range(s - math.ceil(nw / 2) + 1, s + nw // 2 + 1)
                if 1 + nw // 2 <= t <= n - math.ceil(nw / 2) + 1]
        chequear(centros == teor, f'lem:ventana-mes nw={nw} s={s}')
        if 1 + nw // 2 <= s - math.ceil(nw / 2) + 1 and s + nw // 2 <= n - math.ceil(nw / 2) + 1:
            chequear(len(centros) == nw, 'lem:ventana-mes cuenta')
# Convención de fechado con el port de aede y nw = 24 (pide el plan, D4): etiqueta = fila i + nw/2
fechas = pd.period_range('2007-01', periods=228, freq='M').astype(str)
X = pd.DataFrame(rng.standard_normal((228, 5)).cumsum(axis=0), index=fechas)
for nw in (24, 36, 48, 60, 25):
    a = cp.aede(X, nw=nw, ndim=3, nsd=0, maxcl=5)
    et = list(a['eigenvalues'].index)
    chequear(et[0] == fechas[nw // 2] and et[-1] == fechas[228 - nw + nw // 2], f'aede fechado nw={nw}')
    chequear(len(et) == 228 - nw + 1, 'aede N')
    # el valor propio de la ventana 1 es el de las filas 1..nw
    R = np.corrcoef(X.iloc[:nw].to_numpy(), rowvar=False)
    chequear(abs(np.linalg.eigvalsh(R)[-1] - a['eigenvalues'].iloc[0, 0]) < 1e-10, 'aede ventana 1')
# def:borde con el código (bordes_ventana) frente a la fórmula de la tesis
from src.episodios import cargar_episodios, bordes_ventana
ep = cargar_episodios(RAIZ)
bv = bordes_ventana(ep)
for r in ep.itertuples():
    for w in (24, 36, 48, 60):
        ent = (pd.Period(r.inicio_mes, 'M') - (math.ceil(w / 2) - 1)).strftime('%Y-%m')
        sal = (pd.Period(r.fin_efectivo, 'M') + w // 2).strftime('%Y-%m')
        f = bv[(bv.episodio == r.nombre) & (bv.nw == w)]
        chequear(f[f.evento == 'entra'].centro.iloc[0] == ent, f'borde entra {r.nombre} {w}')
        chequear(f[f.evento == 'sale'].centro.iloc[0] == sal, f'borde sale {r.nombre} {w}')
# Comparación con el CSV publicado de bordes
bcsv = pd.read_csv(f'{RAIZ}/data/results/final/07b_bordes_ventana.csv')
chequear(len(bcsv) == len(bv), 'bordes CSV filas')

# ---------------------------------------------------------------------------------------------
# cor:regla06: la correlación sin ponderar de la ventana es R_t con pesos uniformes
for _ in range(50):
    nw = int(rng.integers(5, 40)); p = int(rng.integers(2, 8))
    Z = rng.standard_normal((nw, p)) @ rng.standard_normal((p, p))
    Rs = np.corrcoef(Z, rowvar=False)
    w = np.full(nw, 1 / nw)
    m = w @ Z; C = (Z - m).T @ np.diag(w) @ (Z - m); D = np.diag(1 / np.sqrt(np.diag(C)))
    chequear(np.allclose(D @ C @ D, Rs, atol=1e-12), 'cor:regla06')
    chequear(np.allclose(cp.bstatw(Z, w)['correlations'], Rs, atol=1e-12), 'cor:regla06 con bstatw')

# ---------------------------------------------------------------------------------------------
# Fisher con n_min: fuerza bruta propia
def costo(y, a, b):
    s = y[a:b]
    return float(np.sum((s - s.mean(axis=0)) ** 2))


def bruta(y, K, nmin):
    N = len(y); mejor = math.inf
    for cortes in itertools.combinations(range(1, N), K - 1):
        lim = (0,) + cortes + (N,)
        if min(np.diff(lim)) < nmin:
            continue
        mejor = min(mejor, sum(costo(y, lim[k], lim[k + 1]) for k in range(K)))
    return mejor


from src.particion import particion_fisher
for _ in range(120):
    N = int(rng.integers(4, 15)); nmin = int(rng.integers(1, 5)); q = int(rng.integers(1, 3))
    y = rng.standard_normal((N, q)).round(int(rng.integers(0, 3)))
    Q = {}
    for K in range(1, N + 1):
        Q[K] = bruta(y, K, nmin)
        # cor:fisher-factible (a)
        chequear((Q[K] < math.inf) == (K * nmin <= N), f'factible N={N} nmin={nmin} K={K}')
        if K * nmin <= N and K <= 6:
            r = particion_fisher(y if q > 1 else y[:, 0], K, n_min=nmin)
            sce = r['sce'] if isinstance(r, dict) and 'sce' in r else None
            if sce is not None:
                chequear(abs(sce - Q[K]) < 1e-9, f'particion_fisher n_min N={N} K={K}')
    for K in range(1, N):
        if (K + 1) * nmin <= N and N > K * (2 * nmin - 1):
            chequear(Q[K + 1] <= Q[K] + 1e-12, f'monotonia (a) N={N} nmin={nmin} K={K}')
        if nmin == 1:
            chequear(Q[K + 1] <= Q[K] + 1e-12, 'monotonia (b)')
    # (b) del corolario: segmentos todos de longitud n_min solo si N = K n_min
    for K in range(1, N + 1):
        existe = any(all(d == nmin for d in np.diff((0,) + c + (N,)))
                     for c in itertools.combinations(range(1, N), K - 1))
        chequear(existe == (N == K * nmin), 'factible (b)')
# prop:fisher-monotonia (c): contraejemplo del texto
y = np.array([0.0] * 13 + [5.0] * 13 + [10.0] * 14)
chequear(len(y) == 40, 'contraejemplo N')
q3 = costo(y, 0, 13) + costo(y, 13, 26) + costo(y, 26, 40)
q4 = sum(costo(y, 10 * k, 10 * (k + 1)) for k in range(4))
chequear(q3 == 0 and q4 > 0, 'contraejemplo Q4 > Q3')
r3 = particion_fisher(y, 3, n_min=10); r4 = particion_fisher(y, 4, n_min=10)
chequear(abs(r3['sce']) < 1e-12 and r4['sce'] > 0, 'contraejemplo con particion_fisher')

# ---------------------------------------------------------------------------------------------
# prop:ch (ya existente, se repite): K^a >= K^h
for _ in range(2000):
    N = int(rng.integers(25, 300)); Kmax = int(rng.integers(3, 20))
    T = 1.0
    Q = np.sort(rng.uniform(0.01, 0.99, Kmax))[::-1]
    Q = np.concatenate([[T], Q[1:]])
    K = np.arange(1, Kmax + 1)
    cha = ((T - Q) / K) / (Q / (N - K)); chh = ((T - Q) / np.maximum(K - 1, 1)) / (Q / (N - K))
    ka = int(np.argmax(cha[1:])) + 2; kh = int(np.argmax(chh[1:])) + 2
    chequear(ka >= kh, 'prop:ch')

# ---------------------------------------------------------------------------------------------
# prop:rv-cargas (a)-(d) y coef_rv(centrar=False) del repositorio
def rv(F1, F2):
    G = F1 @ F1.T; H = F2 @ F2.T
    return np.sum(G * H) / np.sqrt(np.sum(G * G) * np.sum(H * H))


for _ in range(300):
    p = int(rng.integers(3, 17)); d = int(rng.integers(1, p + 1))
    A = rng.standard_normal((80, p)) @ rng.standard_normal((p, p)); R1 = np.corrcoef(A, rowvar=False)
    B = rng.standard_normal((80, p)) @ rng.standard_normal((p, p)); R2 = np.corrcoef(B, rowvar=False)
    l1, v1 = np.linalg.eigh(R1); l2, v2 = np.linalg.eigh(R2)
    l1, v1, l2, v2 = l1[::-1], v1[:, ::-1], l2[::-1], v2[:, ::-1]
    F1 = v1[:, :d] * np.sqrt(np.clip(l1[:d], 0, None)); F2 = v2[:, :d] * np.sqrt(np.clip(l2[:d], 0, None))
    Rd1 = F1 @ F1.T; Rd2 = F2 @ F2.T
    val = rv(F1, F2)
    chequear(abs(val - np.sum(Rd1 * Rd2) / (np.linalg.norm(Rd1) * np.linalg.norm(Rd2))) < 1e-12, 'rv-cargas (a)')
    chequear(abs(val - coef_rv(F1, F2, centrar=False)) < 1e-12, 'coef_rv sin centrar = RV')
    O, _ = np.linalg.qr(rng.standard_normal((d, d)))
    Pm = np.eye(d)[rng.permutation(d)] * rng.choice([-1, 1], d)
    chequear(abs(rv(F1 @ O, F2 @ Pm) - val) < 1e-12, 'rv-cargas (b)')
    chequear(0 <= val <= 1 + 1e-12, 'prop:rv (a)')
    Fp1 = v1 * np.sqrt(np.clip(l1, 0, None)); Fp2 = v2 * np.sqrt(np.clip(l2, 0, None))
    chequear(abs(rv(Fp1, Fp2) - np.sum(R1 * R2) / (np.linalg.norm(R1) * np.linalg.norm(R2))) < 1e-10, 'rv-cargas (c)')
    from src.dinamica import rv_correlacion
    chequear(abs(rv(Fp1, Fp2) - rv_correlacion(R1, R2)) < 1e-10, 'rv-cargas (c) con dinamica.rv_correlacion')
# (d)
p = 9
F = np.column_stack([np.full(p, 1 / np.sqrt(p)) * 2.0, rng.standard_normal(p)])
Fc = F - F.mean(axis=0)
chequear(np.allclose(Fc[:, 0], 0), 'rv-cargas (d)')

# ---------------------------------------------------------------------------------------------
# def:pares: N - nw = n - 2 nw + 1 pares, disjuntos y contiguos; frontera = i + nw
for nw in (24, 36, 48, 60):
    n = 228; N = n - nw + 1
    pares = [(i, i + nw) for i in range(1, N - nw + 1)]
    chequear(len(pares) == n - 2 * nw + 1, 'pares cuenta')
    for i, j in pares[:3] + pares[-3:]:
        a = set(range(i, i + nw)); b = set(range(j, j + nw))
        chequear(not (a & b) and max(a) + 1 == min(b), 'pares disjuntos y contiguos')
# Contra el CSV publicado: número de pares por ancho en el RV observado
rvp = pd.read_csv(f'{RAIZ}/data/results/final/07b_nulo_estructura_rv.csv')
col_rep = [c for c in rvp.columns if 'replica' in c.lower()]
obs = rvp[rvp[col_rep[0]] == 0] if col_rep else rvp
for nw in (24, 36, 48, 60):
    g = obs[(obs.nw == nw) & (obs.objeto == 'cargas_sin_centrar') & (obs.pesos == 'uniformes')]
    if 'L' in g.columns:
        g = g[g.L == g.L.iloc[0]]
    chequear(len(g) == 228 - 2 * nw + 1, f'pares en CSV nw={nw}: {len(g)}')

# ---------------------------------------------------------------------------------------------
# lem:hac: identidad con sumas móviles y no negatividad; t_hac_media del código = def:hac
from src.series_tiempo import t_hac_media


def sigma_hac(x, m):
    n = len(x); u = x - x.mean()
    g = [np.sum(u[k:] * u[:n - k]) / n for k in range(m + 1)]
    return g[0] + 2 * sum((1 - k / (m + 1)) * g[k] for k in range(1, m + 1))


for _ in range(400):
    n = int(rng.integers(25, 250)); m = int(rng.integers(0, 20))
    x = rng.standard_normal(n).cumsum() * rng.uniform(0.1, 3)
    u = x - x.mean(); mb = m + 1
    up = np.concatenate([np.zeros(mb - 1), u, np.zeros(mb - 1)])
    sm = sum(np.sum(up[t:t + mb]) ** 2 for t in range(n + mb - 1))
    s2 = sigma_hac(x, m)
    chequear(abs(sm / (n * mb) - s2) < 1e-9 * max(1, abs(s2)), f'lem:hac identidad n={n} m={m}')
    chequear(s2 >= -1e-12, 'lem:hac no negativo')
    media, se, t = t_hac_media(x, rezagos=m)
    chequear(abs(t - x.mean() / np.sqrt(s2 / n)) < 1e-9 * max(1, abs(t)), 't_hac_media = def:hac')
chequear(abs(sigma_hac(np.full(30, 2.0), 12)) < 1e-15, 'lem:hac constante')

# ---------------------------------------------------------------------------------------------
# prop:nulo-estructura (b) y (c), con el código (serie_nula y aede): invariancia afín por serie
from src.nulo_estructura import serie_nula, medir
Xn = pd.DataFrame(rng.standard_normal((120, 6)).cumsum(axis=0) + np.linspace(0, 5, 120)[:, None],
                  index=pd.period_range('2010-01', periods=120, freq='M').astype(str))
ini = rng.integers(1, 119 - 12 + 2, size=math.ceil(119 / 12))
a_ = rng.uniform(-50, 50, 6); b_ = rng.uniform(0.1, 20, 6)
Xt = Xn * b_ + a_
N0 = serie_nula(Xn, 'niveles', ini, 12); N1 = serie_nula(Xt, 'niveles', ini, 12)
chequear(np.allclose(N1.to_numpy(), N0.to_numpy() * b_, rtol=1e-10, atol=1e-8), 'nulo (b) X G_b')
D0 = np.diff(Xn.to_numpy(), axis=0)
from src.remuestreo import indices_desde_inicios
chequear(np.allclose(np.diff(N0.to_numpy(), axis=0), D0[indices_desde_inicios(ini, 12, 119)]), 'nulo (a)')
k0, r0, _ = medir(N0, nw_grilla=(24,), maxcl=8); k1, r1, _ = medir(N1, nw_grilla=(24,), maxcl=8)
chequear((k0.k.to_numpy() == k1.k.to_numpy()).all(), 'nulo (b) k*')
chequear(np.allclose(r0.rv.to_numpy(), r1.rv.to_numpy(), atol=1e-9), 'nulo (b) RV')
Nc = N0 + Xn.iloc[0].to_numpy()
k2, r2, _ = medir(Nc, nw_grilla=(24,), maxcl=8)
chequear((k0.k.to_numpy() == k2.k.to_numpy()).all() and np.allclose(r0.rv, r2.rv, atol=1e-9), 'nulo (c)')

# ---------------------------------------------------------------------------------------------
# prop:oe4: validez de la versión simétrica bajo intercambiabilidad (simulación) y cercanía de la
# versión implementada (dinamica.criterio_oe4)
from src.dinamica import criterio_oe4


def varpi_sim(P):
    Bp1, m = P.shape
    out = np.empty(Bp1)
    for j in range(Bp1):
        q = np.quantile(np.delete(P, j, axis=0), 0.05, axis=0)
        out[j] = np.mean(P[j] < q)
    return out


pv_sim, pv_impl = [], []
for _ in range(400):
    B = 39; m = 15
    # perfiles intercambiables con dependencia entre posiciones
    base = rng.standard_normal((B + 1, 1))
    P = 0.6 * base + rng.standard_normal((B + 1, m))
    v = varpi_sim(P)
    pv_sim.append((1 + np.sum(v[1:] >= v[0])) / (B + 1))
    pv_impl.append(criterio_oe4(P[0], P[1:])['p_valor'])
pv_sim = np.array(pv_sim); pv_impl = np.array(pv_impl)
for a0 in (0.05, 0.1, 0.2, 0.5):
    # cota con margen de Monte Carlo (3 errores estándar)
    chequear(np.mean(pv_sim <= a0) <= a0 + 3 * np.sqrt(a0 * (1 - a0) / len(pv_sim)), f'prop:oe4 alfa={a0}')
print('p-valor simétrico, P(p<=0.05) =', np.mean(pv_sim <= 0.05), '; implementado =', np.mean(pv_impl <= 0.05))

# ---------------------------------------------------------------------------------------------
print(f'Comprobaciones: {total}; fallos: {len(fallos)}')
for f in fallos[:40]:
    print('  FALLO:', f)
print('c(3) =', round(c3, 4))
