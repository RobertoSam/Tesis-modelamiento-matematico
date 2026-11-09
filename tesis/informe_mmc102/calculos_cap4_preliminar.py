"""Regímenes preliminares (decisión del tesista del 9-11-2026) y su caracterización.

Especificación preliminar, no validada estadísticamente (el contraste con series de referencia
simuladas da K* = 1; ver calculos_cap4_segmentacion.py):
  - posición: coordenadas F1–F3 del PCA en niveles, media móvil de los 12 meses anteriores,
    estandarizadas (como en `datar`), partición de Fisher, regla del 10 % (D12);
  - estructura: λ1(t) del EPCA (w = 48, ν = 3), partición de Fisher, regla del 10 %.
Calcula: cortes, precisión de su ubicación, influencia de meses atípicos, caracterización con la
regla de fases por crecimiento real del crédito (c = 1 y 0,5) y línea base de azar de los
episodios. Salidas: data/results/final/mmc102/preliminar_*.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
fuente = (RAIZ / "tesis/informe_mmc102/calculos_cap4_segmentacion.py").read_text()
ns = {"__name__": "aux"}
exec(fuente.split("# ------------------------------------------------------------------ 1.")[0], ns)
pt, A, X, p, n, fechas, SAL, rng = ns["pt"], ns["A"], ns["X"], ns["p"], ns["n"], ns["fechas"], ns["SAL"], ns["rng"]
lambda1_trayectoria, particionar, regla_umbral = ns["lambda1_trayectoria"], ns["particionar"], ns["regla_umbral"]
idx = {f: i for i, f in enumerate(fechas)}
W = 48

# ---------------------------------------------------------------- trayectorias y cortes
_, _, S = pt.scores_pca_rcamiz(A)
Yp = np.column_stack([pt.media_movil_causal(S[:, k], 12) for k in range(3)])
okp = ~np.isnan(Yp).any(1)
Yp = pt.estandarizar_r(Yp[okp])
f_p = fechas[okp]
_, scd_p, cortes_p = particionar(Yp)
K_P = regla_umbral(scd_p, 0.10)

l1 = lambda1_trayectoria(A)
f_e = fechas[W // 2: W // 2 + len(l1)]
_, scd_e, cortes_e = particionar(l1)
K_E = regla_umbral(scd_e, 0.10)
cp_fechas = [f_p[c] for c in cortes_p[K_P]]
ce_fechas = [f_e[c] for c in cortes_e[K_E]]
print("Posición  K =", K_P, cp_fechas)
print("Estructura K =", K_E, ce_fechas)
assert cp_fechas == ["2008-12", "2010-03", "2014-04", "2020-06", "2022-11"], "no reproduce la especificación anterior"


# ---------------------------------------------------------------- precisión de la ubicación
def precision(Y, cortes, f, K, B=200, ell=6):
    Y = Y if Y.ndim == 2 else Y[:, None]
    lim = [0] + list(cortes) + [len(Y)]
    medias = np.vstack([np.repeat(Y[a:b].mean(0, keepdims=True), b - a, 0) for a, b in zip(lim[:-1], lim[1:])])
    res = Y - medias
    hall = []
    for _ in range(B):
        R = np.empty_like(res)
        for a, b in zip(lim[:-1], lim[1:]):
            m = b - a
            k = int(np.ceil(m / ell))
            fil = np.concatenate([np.arange(s, s + ell) for s in rng.integers(0, m - ell + 1, k)])[:m]
            R[a:b] = res[a:b][fil]
        hall.append(pt.fisher_multivariado(medias + R, k_max=K, n_min=12)[K]["cortes"])
    out = []
    for i, c in enumerate(cortes):
        pos = np.array([min(h, key=lambda x: abs(x - c)) for h in hall])
        out.append({"corte": f[c], "frecuencia_3m": float(np.mean(np.abs(pos - c) <= 3)),
                    "p5": f[int(np.percentile(pos, 5))], "p95": f[int(np.percentile(pos, 95))],
                    "meses_tramo_previo": c - lim[i], "meses_tramo_siguiente": lim[i + 2] - c})
    return out


prec = [dict(trayectoria="posición", **r) for r in precision(Yp, cortes_p[K_P], f_p, K_P)]
prec += [dict(trayectoria="estructura", **r) for r in precision(l1, cortes_e[K_E], f_e, K_E)]
pd.DataFrame(prec).to_csv(SAL / "preliminar_precision_cortes.csv", index=False)

# ---------------------------------------------------------------- influencia de meses atípicos
inc = np.diff(A, axis=0)
med = np.median(inc, axis=0)
esc = 1.4826 * np.median(np.abs(inc - med), axis=0)
esc = np.where(esc > 0, esc, inc.std(axis=0))           # series con muchos meses sin cambio
norma = np.sqrt(np.sum(((inc - med) / esc) ** 2, axis=1))
q1, q3 = np.percentile(norma, [25, 75])
atip = np.nonzero(norma > q3 + 3 * (q3 - q1))[0] + 1
marcas = []
for c in ce_fechas:
    m = idx[c]
    rel = [fechas[t] for t in atip if min(abs(m - (t - 23)), abs(m - (t + 24))) <= 3]
    marcas.append({"corte": c, "meses_atipicos_relacionados": " ".join(rel)})
pd.DataFrame(marcas).to_csv(SAL / "preliminar_influencia.csv", index=False)
pd.DataFrame({"mes": fechas[1:], "norma_robusta": norma, "atipico": np.isin(np.arange(1, n), atip)}).to_csv(
    SAL / "preliminar_norma_incrementos.csv", index=False)
print("Meses atípicos:", [fechas[t] for t in atip])

# ---------------------------------------------------------------- caracterización y fases
cred = X[["Crédito empresarial", "Crédito consumo", "Crédito hipotecario"]].sum(axis=1).to_numpy()
ipc = X["IPC Lima"].to_numpy()


def interanual(x):
    r = np.full(n, np.nan)
    r[12:] = 100 * (x[12:] / x[:-12] - 1)
    return r


g = interanual(cred / ipc)
g_pbi, g_ipc, g_nom = interanual(X["PBI desestacionalizado"].to_numpy()), interanual(ipc), interanual(cred)
m_g, s_g = np.nanmedian(g), np.nanstd(g)
tasa, embig = X["Tasa de referencia"].to_numpy(), X["EMBIG Perú"].to_numpy()


def caracterizar(tipo, cortes_f, f):
    ini = [idx[f[0]]] + [idx[c] for c in cortes_f]
    fin = [i - 1 for i in ini[1:]] + [idx[f[-1]]]
    out = []
    for k, (a, b) in enumerate(zip(ini, fin), start=1):
        gk = g[a:b + 1]
        mk = np.nanmedian(gk)
        gv = gk[~np.isnan(gk)]
        fase = {c: ("expansión" if mk > m_g + c * s_g else "contracción" if mk < m_g - c * s_g else "transición")
                for c in (1.0, 0.5)}
        out.append({"tipo": tipo, "regimen": k, "inicio": fechas[a], "fin": fechas[b], "meses": b - a + 1,
                    "credito_real_mediana": mk, "credito_nominal_media": np.nanmean(g_nom[a:b + 1]),
                    "variacion_g": (gv[-1] - gv[0]) if len(gv) > 1 else np.nan,
                    "pbi": np.nanmean(g_pbi[a:b + 1]), "inflacion": np.nanmean(g_ipc[a:b + 1]),
                    "tasa_inicio": tasa[a:a + 3].mean(), "tasa_fin": tasa[b - 2:b + 1].mean(),
                    "embig": embig[a:b + 1].mean(), "meses_sin_g": int(np.isnan(gk).sum()),
                    "fase_c1": fase[1.0], "fase_c05": fase[0.5]})
    return out


car = caracterizar("posición", cp_fechas, f_p) + caracterizar("estructura", ce_fechas, f_e)
pd.DataFrame(car).to_csv(SAL / "preliminar_caracterizacion.csv", index=False)
pd.DataFrame({"fecha": fechas, "g_credito_real": g}).to_csv(SAL / "preliminar_credito_real.csv", index=False)

# ---------------------------------------------------------------- episodios y línea base
epis = pd.read_csv(RAIZ / "data/referencia/episodios_referencia.csv", dtype=str).fillna("")
bordes = sorted({idx[e.inicio] for e in epis.itertuples()} | {idx[e.fin] for e in epis.itertuples() if e.fin})
dist = lambda m: min(abs(m - b) for b in bordes)  # noqa: E731


def linea_base(f, K, tol, B=10000):
    lo, m = idx[f[0]], len(f)
    vals = []
    while len(vals) < B:
        c = np.sort(rng.choice(np.arange(12, m - 12 + 1), K - 1, replace=False))
        if np.all(np.diff(np.concatenate([[0], c, [m]])) >= 12):
            vals.append(sum(dist(lo + x) <= tol for x in c))
    vals = np.array(vals)
    return vals


fil = []
for tipo, cf, f, K in [("posición", cp_fechas, f_p, K_P), ("estructura", ce_fechas, f_e, K_E)]:
    d = [dist(idx[c]) for c in cf]
    for tol in (3, 6):
        v = linea_base(f, K, tol)
        obs = int(sum(x <= tol for x in d))
        fil.append({"trayectoria": tipo, "tolerancia": tol, "cortes": K - 1, "compatibles": obs,
                    "esperados_azar": float(v.mean()), "p_azar": float(np.mean(v >= obs)),
                    "distancias": " ".join(map(str, d))})
pd.DataFrame(fil).to_csv(SAL / "preliminar_episodios.csv", index=False)
pd.Series({"K_posicion": K_P, "K_estructura": K_E, "m_g": m_g, "s_g": s_g}).to_csv(SAL / "preliminar_resumen.csv")
pd.set_option("display.width", 250)
for nombre in ("precision_cortes", "influencia", "caracterizacion", "episodios"):
    print(pd.read_csv(SAL / f"preliminar_{nombre}.csv").round(2).to_string(index=False))
print("m_g =", round(m_g, 2), " s_g =", round(s_g, 2))
