"""Segmentación temporal del Capítulo 3 (versión del 9-11-2026) y su validación.

Implementa las secciones 3.2.4 a 3.2.6 del borrador MMC102:
  1. trayectoria de estructura: λ1(t) del EPCA (w = 48, ν = 3), partición de Fisher, Δ_K;
  2. trayectoria de posición: coordenadas F1–F3 del PCA global, media móvil centrada de 12
     meses, sin estandarizar; partición de Fisher, Δ_K;
  3. contraste de la partición con series de referencia simuladas (estructura constante para
     la trayectoria de estructura; tendencia para la de posición) y K* = mayor K con Δ_K > p95;
  4. sensibilidad: regla del umbral (10, 12, 15 %), mayor caída, media causal, coordenadas
     estandarizadas;
  5. diagnóstico de influencia de los meses atípicos y EPCA sin marzo–junio de 2020;
  6. precisión de la ubicación de los cortes (residuos remuestreados dentro de cada tramo);
  7. caracterización de los regímenes, regla de fases y línea base de azar de los episodios.

Uso, desde la raíz del repositorio:  python3 tesis/informe_mmc102/calculos_cap4_segmentacion.py
Salidas: data/results/final/mmc102/*.csv
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
from src import camiz_port as cp                     # noqa: E402
from src import particion as pt                      # noqa: E402
from src.datos import cargar_vias                    # noqa: E402
from src.nulo_estructura import serie_nula           # noqa: E402
from src.parametros import leer_parametros           # noqa: E402
from src.remuestreo import indices_desde_inicios     # noqa: E402

SAL = RAIZ / "data/results/final/mmc102"
SAL.mkdir(parents=True, exist_ok=True)
W, NU, KMAX, NMIN, D, LMM = 48, 3, 10, 12, 3, 12
B_TEND, B_UBIC, ELL = 1000, 200, 24
rng = np.random.default_rng(20261109)

PAR = leer_parametros(RAIZ)
X, _ = cargar_vias(RAIZ, excluidas=PAR["EXCLUIDAS"])
fechas = np.array([str(f)[:7] for f in X.index])
A = X.to_numpy(dtype=float)
n, p = A.shape
print(f"Datos: {n} meses × {p} series, {fechas[0]} a {fechas[-1]}")


# ------------------------------------------------------------------ utilidades
def lambda1_trayectoria(M, w=W, nu=NU):
    """Primer valor propio de la correlación ponderada en cada ventana (fecha: posición w/2+1)."""
    om = cp.pesos_aede(w, nu)
    out = np.empty(len(M) - w + 1)
    for i in range(len(out)):
        V = M[i:i + w]
        mu = om @ V
        C = V - mu
        S = (C * om[:, None]).T @ C
        d = np.sqrt(np.diag(S))
        cero = d < 1e-12 * max(d.max(), 1.0)
        d[cero] = 1.0
        Rw = S / np.outer(d, d)
        # Serie constante en la ventana (posible en las réplicas: tasas sin cambios durante
        # varios meses): correlación indefinida; se trata como no correlacionada.
        Rw[cero, :] = 0.0; Rw[:, cero] = 0.0; Rw[cero, cero] = 1.0
        out[i] = np.linalg.eigvalsh(Rw)[-1]
    return out


def media_movil_centrada(x, w=LMM):
    c = pt.media_movil_causal(x, w)
    r = np.full(len(x), np.nan)
    a, b = w // 2 - 1, w // 2
    r[:len(x) - b] = 0.5 * (c[a:len(x) - b + a] + c[b:])
    return r


def trayectoria_posicion(M, suav="centrada", estandarizar=False, d=D):
    _, _, S = pt.scores_pca_rcamiz(M)
    f = media_movil_centrada if suav == "centrada" else (lambda x: pt.media_movil_causal(x, LMM))
    Y = np.column_stack([f(S[:, k]) for k in range(d)])
    ok = ~np.isnan(Y).any(axis=1)
    Y = Y[ok]
    if estandarizar:
        Y = pt.estandarizar_r(Y)
    return Y, ok


def particionar(Y):
    """SCD_K y cortes (0-based) para K = 1..KMAX con tramos de al menos NMIN."""
    res = pt.fisher_multivariado(Y, k_max=KMAX, n_min=NMIN)
    ks = np.array(sorted(res))
    scd = np.array([res[k]["sce"] for k in ks])
    return ks, scd, {k: res[k]["cortes"] for k in ks}


def deltas(scd):
    """Δ_K = (SCD_{K-1} − SCD_K) / SCD_{K-1} para K = 2..KMAX (índice 0 ↔ K = 2)."""
    return (scd[:-1] - scd[1:]) / scd[:-1]


def regla_caida(scd):
    """Como `datar` (k_caida): k con la mayor caída de la reducción relativa respecto de k − 1."""
    r = deltas(scd)                       # r[i]: reducción al pasar de K=i+1 a K=i+2
    caida = np.concatenate([[np.nan], r[:-1]]) - r
    return int(np.nanargmax(caida) + 1)


def regla_umbral(scd, umbral):
    """Regla K (D12), como `datar` (k_codo): menor K con reducción < umbral; si no hay, k_caida."""
    r = deltas(scd)
    bajo = np.nonzero(r < umbral)[0]
    return int(bajo.min() + 1) if len(bajo) else regla_caida(scd)


def regla_referencia(dobs, dsim):
    """Mayor K con Δ_K observado > percentil 95 simulado."""
    p95 = np.nanpercentile(dsim, 95, axis=0)
    ok = np.nonzero(dobs > p95)[0]
    return (int(ok.max() + 2) if len(ok) else 1), p95


def p_hat(obs, sim):
    sim = np.asarray(sim)
    sim = sim[~np.isnan(sim)]
    return (1 + np.sum(sim >= obs)) / (len(sim) + 1)


# ------------------------------------------------------------------ 1. Trayectoria de estructura
t0 = time.time()
l1 = lambda1_trayectoria(A)
f_l1 = fechas[W // 2: W // 2 + len(l1)]            # posición w/2+1 (0-based w/2)
ref = pd.read_csv(RAIZ / "data/results/final/06c_aede_valores_propios.csv")
ref = ref[(ref.nw == W) & ref.pesos.str.startswith("gau")]
assert np.allclose(ref.lambda1.to_numpy(), l1, atol=1e-8), "λ1 no coincide con aede"
assert ref.fecha.iloc[0] == f_l1[0] and ref.fecha.iloc[-1] == f_l1[-1]
ks, scd_e, cortes_e = particionar(l1)
dobs_e = deltas(scd_e)
print(f"Estructura: {len(l1)} ventanas, {f_l1[0]} a {f_l1[-1]} (λ1 verificado contra aede)")

# Series de referencia con estructura constante (incrementos remuestreados en bloques conjuntos)
ini = pd.read_csv(RAIZ / "data/results/final/R_nulo_estructura_indices_L24.csv").sort_values("replica")
ini = ini.filter(like="inicio_").to_numpy(dtype=int)
dsim_e = []
for r in range(len(ini)):
    Mn = serie_nula(X, "niveles", ini[r], ELL).to_numpy()
    _, s, _ = particionar(lambda1_trayectoria(Mn))
    dsim_e.append(deltas(s))
dsim_e = np.array(dsim_e)
kref_e, p95_e = regla_referencia(dobs_e, dsim_e)
print(f"  K* (referencia) = {kref_e}; {len(ini)} réplicas; {time.time() - t0:.0f} s")

# ------------------------------------------------------------------ 2. Trayectoria de posición
Yp, okp = trayectoria_posicion(A)
f_p = fechas[okp]
_, scd_p, cortes_p = particionar(Yp)
dobs_p = deltas(scd_p)

# Series de referencia con tendencia (independientes entre series, remuestreo por bloques)
tend = pd.read_csv(RAIZ / "data/results/final/05_tendencia_series.csv")
assert list(tend.nombre) == list(X.columns)


def bloques(m, ell=ELL):
    k = int(np.ceil(m / ell))
    inicios = rng.integers(1, m - ell + 2, k)
    return indices_desde_inicios(inicios, ell, m)


def serie_tendencia(x, tipo):
    t = np.arange(len(x))
    if tipo == "TS":
        b, a = np.polyfit(t, x, 1)
        res = x - (a + b * t)
        return a + b * t + res[bloques(len(x))]
    dx = np.diff(x)
    deriva = dx.mean()
    inc = (dx - deriva)[bloques(len(dx))]
    if tipo == "DS_deriva":
        inc = inc + deriva
    return np.concatenate([[x[0]], x[0] + np.cumsum(inc)])


def tipos(version):
    out = []
    for r in tend.itertuples():
        if r.clase_d5 == "TS" or (r.clase_d5 == "indeterminada" and version == "ind_TS"):
            out.append("TS")
        else:
            out.append("DS_deriva" if abs(r.deriva_hac_t) > 2 else "DS")
    return out


inercia_obs = None
resultados_tend = {}
for version in ("ind_TS", "ind_DS"):
    tp = tipos(version)
    dsim, inercias = [], []
    for b in range(B_TEND):
        Ms = np.column_stack([serie_tendencia(A[:, j], tp[j]) for j in range(p)])
        val, _, _ = pt.scores_pca_rcamiz(Ms)
        inercias.append(val[:3] / p)
        Ys, _ = trayectoria_posicion(Ms)
        _, s, _ = particionar(Ys)
        dsim.append(deltas(s))
    resultados_tend[version] = (np.array(dsim), np.array(inercias))
    print(f"  Referencia con tendencia ({version}): {B_TEND} réplicas; {time.time() - t0:.0f} s")
val_obs, _, _ = pt.scores_pca_rcamiz(A)
inercia_obs = val_obs[:3] / p
kref_p = {v: regla_referencia(dobs_p, resultados_tend[v][0])[0] for v in resultados_tend}
print(f"Posición: K* (referencia) = {kref_p}")

# Tabla de Δ_K y p̂
filas = []
for nombre, dobs, sims in [("estructura", dobs_e, {"estructura constante": dsim_e}),
                           ("posición", dobs_p, {v: resultados_tend[v][0] for v in resultados_tend})]:
    for i, k in enumerate(range(2, KMAX + 1)):
        fila = {"trayectoria": nombre, "K": k, "delta_obs": dobs[i]}
        for etiqueta, sim in sims.items():
            fila[f"p95_{etiqueta}"] = np.nanpercentile(sim[:, i], 95)
            fila[f"p_{etiqueta}"] = p_hat(dobs[i], sim[:, i])
        filas.append(fila)
pd.DataFrame(filas).to_csv(SAL / "contraste_particion.csv", index=False)

# Contraste de los ejes del PCA con la nueva referencia con tendencia
filas = []
for v, (_, iner) in resultados_tend.items():
    for k in range(3):
        filas.append({"version": v, "eje": k + 1, "inercia_obs": inercia_obs[k],
                      "p50": np.median(iner[:, k]), "p95": np.percentile(iner[:, k], 95),
                      "p": p_hat(inercia_obs[k], iner[:, k])})
pd.DataFrame(filas).to_csv(SAL / "referencia_tendencia_ejes.csv", index=False)

# ------------------------------------------------------------------ 3. Cortes y sensibilidad
def cortes_fecha(cortes, f):
    return [f[c] for c in cortes]


K_E = kref_e
K_P = kref_p["ind_DS"] if kref_p["ind_DS"] == kref_p["ind_TS"] else max(kref_p.values())
sens = []
for nombre, scd, cortes, f, kref in [("estructura", scd_e, cortes_e, f_l1, K_E),
                                     ("posición", scd_p, cortes_p, f_p, K_P)]:
    reglas = {"referencia simulada (principal)": kref, "umbral 10 %": regla_umbral(scd, 0.10),
              "umbral 12 %": regla_umbral(scd, 0.12), "umbral 15 %": regla_umbral(scd, 0.15),
              "mayor caída": regla_caida(scd)}
    for regla, k in reglas.items():
        sens.append({"trayectoria": nombre, "variante": regla, "K": k,
                     "cortes": " ".join(cortes_fecha(cortes[k], f)) if k > 1 else ""})
# Posición: media causal y estandarizada (con K de la regla de referencia del principal)
for etiqueta, kw in [("media causal", dict(suav="causal")), ("estandarizada", dict(estandarizar=True)),
                     ("d = 2", dict(d=2)), ("d = 4", dict(d=4))]:
    Y2, ok2 = trayectoria_posicion(A, **kw)
    _, s2, c2 = particionar(Y2)
    sens.append({"trayectoria": "posición", "variante": etiqueta, "K": K_P,
                 "cortes": " ".join(cortes_fecha(c2[K_P], fechas[ok2]))})
# Estructura: otros anchos (con el K de la regla del umbral, sin simulación para cada ancho)
for w2 in (36, 60):
    l2 = lambda1_trayectoria(A, w=w2)
    _, s2, c2 = particionar(l2)
    sens.append({"trayectoria": "estructura", "variante": f"w = {w2}", "K": K_E,
                 "cortes": " ".join(cortes_fecha(c2[K_E], fechas[w2 // 2: w2 // 2 + len(l2)]))})
pd.DataFrame(sens).to_csv(SAL / "cortes_sensibilidad.csv", index=False)

# ------------------------------------------------------------------ 4. Influencia de meses atípicos
inc = np.diff(A, axis=0)
med = np.median(inc, axis=0)
mad = 1.4826 * np.median(np.abs(inc - med), axis=0)
norma = np.sqrt(np.sum(((inc - med) / mad) ** 2, axis=1))
q1, q3 = np.percentile(norma, [25, 75])
atip = np.nonzero(norma > q3 + 3 * (q3 - q1))[0] + 1        # índice del mes (incremento t-1 → t)
meses_atip = list(fechas[atip])
A2 = A.copy()
i0, i1 = list(fechas).index("2020-02"), list(fechas).index("2020-07")
for j in range(p):
    A2[i0:i1 + 1, j] = np.linspace(A[i0, j], A[i1, j], i1 - i0 + 1)
l1b = lambda1_trayectoria(A2)
_, scd_b, cortes_b = particionar(l1b)
idx = {f: i for i, f in enumerate(fechas)}
marcas = []
for c in cortes_fecha(cortes_e[K_E], f_l1):
    m = idx[c]
    cerca = [fechas[t] for t in atip if min(abs(m - (t - 23)), abs(m - (t + 24))) <= 3]
    marcas.append({"corte": c, "meses_atipicos_relacionados": " ".join(cerca)})
pd.DataFrame(marcas).to_csv(SAL / "influencia_cortes.csv", index=False)
pd.DataFrame({"mes": fechas[1:], "norma_robusta": norma}).to_csv(SAL / "norma_incrementos.csv", index=False)
inf = {"meses_atipicos": " ".join(meses_atip),
       "cortes_sin_2020_mismo_K": " ".join(cortes_fecha(cortes_b[K_E], f_l1)),
       "K_umbral10_sin_2020": regla_umbral(scd_b, 0.10)}
pd.Series(inf).to_csv(SAL / "influencia_resumen.csv")
pd.DataFrame({"fecha": f_l1, "lambda1": l1, "lambda1_sin_2020": l1b}).to_csv(SAL / "trayectoria_estructura.csv", index=False)
pd.DataFrame(Yp, columns=["F1", "F2", "F3"]).assign(fecha=f_p).to_csv(SAL / "trayectoria_posicion.csv", index=False)

# ------------------------------------------------------------------ 5. Precisión de la ubicación
def precision(Y, cortes, f, K, B=B_UBIC, ell=6):
    Y = Y if Y.ndim == 2 else Y[:, None]
    lim = [0] + list(cortes) + [len(Y)]
    medias = np.vstack([np.repeat(Y[a:b].mean(0, keepdims=True), b - a, 0) for a, b in zip(lim[:-1], lim[1:])])
    res = Y - medias
    hallados = []
    for _ in range(B):
        R = np.empty_like(res)
        for a, b in zip(lim[:-1], lim[1:]):
            m = b - a
            if m <= ell:
                R[a:b] = res[a:b][rng.integers(0, m, m)]
            else:
                R[a:b] = res[a:b][indices_desde_inicios(rng.integers(1, m - ell + 2, int(np.ceil(m / ell))), ell, m)]
        res_k = pt.fisher_multivariado(medias + R, k_max=K, n_min=NMIN)
        hallados.append(res_k[K]["cortes"])
    filas = []
    for i, c in enumerate(cortes):
        pos = np.array([min(h, key=lambda x: abs(x - c)) for h in hallados])
        filas.append({"corte": f[c], "frecuencia_3m": np.mean(np.abs(pos - c) <= 3),
                      "p5": f[int(np.percentile(pos, 5))], "p95": f[int(np.percentile(pos, 95))],
                      "meses_tramo_previo": c - lim[i], "meses_tramo_siguiente": lim[i + 2] - c})
    return filas


prec = [dict(trayectoria="estructura", **r) for r in precision(l1, cortes_e[K_E], f_l1, K_E)] if K_E > 1 else []
prec += [dict(trayectoria="posición", **r) for r in precision(Yp, cortes_p[K_P], f_p, K_P)] if K_P > 1 else []
pd.DataFrame(prec).to_csv(SAL / "precision_cortes.csv", index=False)

# ------------------------------------------------------------------ 6. Caracterización y fases
cred = X[["Crédito empresarial", "Crédito consumo", "Crédito hipotecario"]].sum(axis=1).to_numpy()
ipc = X["IPC Lima"].to_numpy()
real = cred / ipc
g = np.full(n, np.nan)
g[12:] = 100 * (real[12:] / real[:-12] - 1)


def interanual(x):
    r = np.full(n, np.nan)
    r[12:] = 100 * (x[12:] / x[:-12] - 1)
    return r


g_pbi, g_ipc = interanual(X["PBI desestacionalizado"].to_numpy()), interanual(ipc)
m_g, s_g = np.nanmedian(g), np.nanstd(g)
tasa = X["Tasa de referencia"].to_numpy()
embig = X["EMBIG Perú"].to_numpy()


def caracterizar(nombre, cortes, f):
    ini_idx = [idx[f[0]]] + [idx[f[c]] for c in cortes]
    fin_idx = [i - 1 for i in ini_idx[1:]] + [idx[f[-1]]]
    filas = []
    for k, (a, b) in enumerate(zip(ini_idx, fin_idx), start=1):
        gk = g[a:b + 1]
        mk = np.nanmedian(gk)
        fases = {}
        for c in (1.0, 0.5):
            fases[c] = "expansión" if mk > m_g + c * s_g else ("contracción" if mk < m_g - c * s_g else "transición")
        gv = gk[~np.isnan(gk)]
        filas.append({"tipo": nombre, "regimen": k, "inicio": fechas[a], "fin": fechas[b], "meses": b - a + 1,
                      "credito_real_mediana": mk, "credito_real_media": np.nanmean(gk),
                      "variacion_g": (gv[-1] - gv[0]) if len(gv) > 1 else np.nan,
                      "pbi": np.nanmean(g_pbi[a:b + 1]), "inflacion": np.nanmean(g_ipc[a:b + 1]),
                      "tasa_inicio": tasa[a:a + 3].mean(), "tasa_fin": tasa[b - 2:b + 1].mean(),
                      "embig": embig[a:b + 1].mean(), "meses_sin_g": int(np.isnan(gk).sum()),
                      "fase_c1": fases[1.0], "fase_c05": fases[0.5]})
    return filas


carac = caracterizar("estructura", cortes_e[K_E], f_l1) + caracterizar("posición", cortes_p[K_P], f_p)
pd.DataFrame(carac).to_csv(SAL / "caracterizacion_regimenes.csv", index=False)
pd.DataFrame({"fecha": fechas, "g_credito_real": g}).to_csv(SAL / "crecimiento_credito_real.csv", index=False)

# ------------------------------------------------------------------ 7. Episodios y línea base de azar
epis = pd.read_csv(RAIZ / "data/referencia/episodios_referencia.csv", dtype=str).fillna("")
bordes = sorted({idx[e.inicio] for e in epis.itertuples()} | {idx[e.fin] for e in epis.itertuples() if e.fin})


def distancia(m):
    return min(abs(m - b) for b in bordes)


def linea_base(f, K, tol=3, B=10000):
    """Proporción esperada de cortes compatibles si se ubican al azar con tramos ≥ NMIN."""
    lo, hi = idx[f[0]], idx[f[-1]]
    m = hi - lo + 1
    comp = []
    while len(comp) < B:
        c = np.sort(rng.choice(np.arange(NMIN, m - NMIN + 1), K - 1, replace=False))
        if np.all(np.diff(np.concatenate([[0], c, [m]])) >= NMIN):
            comp.append(np.mean([distancia(lo + x) <= tol for x in c]))
    return float(np.mean(comp))


filas = []
for nombre, cortes, f, K in [("estructura", cortes_e[K_E], f_l1, K_E), ("posición", cortes_p[K_P], f_p, K_P)]:
    if K < 2:
        continue
    obs = [distancia(idx[f[c]]) for c in cortes]
    for tol in (3, 6):
        filas.append({"trayectoria": nombre, "tolerancia": tol, "K": K,
                      "compatibles_obs": int(np.sum(np.array(obs) <= tol)), "cortes": K - 1,
                      "proporcion_obs": float(np.mean(np.array(obs) <= tol)),
                      "proporcion_azar": linea_base(f, K, tol),
                      "distancias": " ".join(str(d) for d in obs)})
pd.DataFrame(filas).to_csv(SAL / "episodios_linea_base.csv", index=False)

pd.Series({"K_estructura": K_E, "K_posicion": K_P, "K_posicion_indTS": kref_p["ind_TS"],
           "K_posicion_indDS": kref_p["ind_DS"], "m_g": m_g, "s_g": s_g,
           "replicas_estructura": len(ini), "replicas_tendencia": B_TEND}).to_csv(SAL / "resumen.csv")
print(f"Listo en {time.time() - t0:.0f} s. Resultados en {SAL}")
