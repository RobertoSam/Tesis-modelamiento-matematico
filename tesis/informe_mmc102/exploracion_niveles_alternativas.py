"""Exploración (no incorporada): regímenes de posición con las series originales en niveles.

Alternativa 1 — tendencias segmentadas: partición de las coordenadas F1–F3 del PCA en niveles
en tramos contiguos donde se ajusta una RECTA (costo = suma de cuadrados respecto de la recta
del tramo); los cortes son cambios de pendiente (aceleración o desaceleración).
Alternativa 3 — desviaciones respecto de la tendencia: se resta a cada coordenada su tendencia
lineal (y cuadrática, como sensibilidad) estimada en todo el período, y se aplica la partición
de Fisher por medias a las desviaciones, suavizadas con media móvil centrada de 12 meses.

En ambos casos el PCA se calcula con las series en niveles, sin transformar. El contraste es el
mismo de la sección 3.2.5: series de referencia con tendencia (independientes entre sí, cada una
con su tipo de tendencia), K* = mayor K con Δ_K > percentil 95 simulado.
Salidas: data/results/final/mmc102/exploracion_niveles_*.csv
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
tend_src = fuente.split("# Series de referencia con tendencia")[1].split("inercia_obs = None")[0]
exec("tend = pd.read_csv(RAIZ / 'data/results/final/05_tendencia_series.csv')\n" + tend_src.split("\n", 1)[1], ns)
pt, A, p, fechas, SAL = ns["pt"], ns["A"], ns["p"], ns["fechas"], ns["SAL"]
media_movil_centrada, deltas, p_hat = ns["media_movil_centrada"], ns["deltas"], ns["p_hat"]
particionar, serie_tendencia, tipos = ns["particionar"], ns["serie_tendencia"], ns["tipos"]
KMAX, NMIN, B = 10, 12, 500


def fisher_lineal(Y, kmax=KMAX, nmin=NMIN):
    """Partición óptima en tramos contiguos con una recta por tramo y dimensión (programación dinámica)."""
    Y = Y if Y.ndim == 2 else Y[:, None]
    n = len(Y)
    t = np.arange(n, dtype=float)
    c = lambda v: np.concatenate([[0.0], np.cumsum(v)])     # noqa: E731
    St, Stt = c(t), c(t * t)
    Sy = np.vstack([np.zeros(Y.shape[1]), np.cumsum(Y, 0)])
    Syy = np.concatenate([[0.0], np.cumsum(np.sum(Y * Y, 1))])
    Sty = np.vstack([np.zeros(Y.shape[1]), np.cumsum(Y * t[:, None], 0)])

    def costo(i, j):            # tramo Y[i:j] (i vector de inicios), j fin exclusivo
        m = j - i
        st, stt = St[j] - St[i], Stt[j] - Stt[i]
        sy, sty = Sy[j] - Sy[i], Sty[j] - Sty[i]
        syy = Syy[j] - Syy[i]
        sxx = stt - st * st / m
        sxy = sty - (st / m)[:, None] * sy
        return syy - np.sum(sy * sy, 1) / m - np.sum(sxy * sxy, 1) / sxx

    D = np.full((kmax + 1, n + 1), np.inf)
    arg = np.zeros((kmax + 1, n + 1), dtype=int)
    for j in range(nmin, n + 1):
        D[1, j] = costo(np.array([0]), j)[0]
    for k in range(2, kmax + 1):
        for j in range(k * nmin, n + 1):
            ini = np.arange((k - 1) * nmin, j - nmin + 1)
            v = D[k - 1, ini] + costo(ini, j)
            b = int(np.argmin(v))
            D[k, j], arg[k, j] = v[b], ini[b]
    scd, cortes = [], {}
    for k in range(1, kmax + 1):
        scd.append(D[k, n])
        cs, j = [], n
        for kk in range(k, 1, -1):
            j = arg[kk, j]
            cs.append(j)
        cortes[k] = sorted(cs)
    return np.array(scd), cortes


def scores(M):
    _, _, S = pt.scores_pca_rcamiz(M)
    return S[:, :3]


def tray_pendiente(M):
    return scores(M), np.ones(len(M), bool)


def tray_desviacion(M, grado=1):
    S = scores(M)
    t = np.arange(len(S))
    Dv = np.column_stack([S[:, k] - np.polyval(np.polyfit(t, S[:, k], grado), t) for k in range(3)])
    Dm = np.column_stack([media_movil_centrada(Dv[:, k]) for k in range(3)])
    ok = ~np.isnan(Dm).any(1)
    return Dm[ok], ok


variantes = {
    "1. pendientes (coordenadas en niveles)": (tray_pendiente, fisher_lineal),
    "3. desviación de tendencia lineal": (lambda M: tray_desviacion(M, 1), lambda Y: particionar(Y)[1:]),
    "3b. desviación de tendencia cuadrática": (lambda M: tray_desviacion(M, 2), lambda Y: particionar(Y)[1:]),
}
filas, resumen = [], []
for nombre, (tray, part) in variantes.items():
    Y, ok = tray(A)
    f = fechas[ok]
    scd, cortes = part(Y)
    dobs = deltas(scd)
    sims = {}
    for version in ("ind_TS", "ind_DS"):
        tp = tipos(version)
        ds = []
        for _ in range(B):
            Ms = np.column_stack([serie_tendencia(A[:, j], tp[j]) for j in range(p)])
            ds.append(deltas(part(tray(Ms)[0])[0]))
        sims[version] = np.array(ds)
    kstar = {}
    for version, s in sims.items():
        p95 = np.nanpercentile(s, 95, axis=0)
        sup = np.nonzero(dobs > p95)[0]
        kstar[version] = int(sup.max() + 2) if len(sup) else 1
    for i, K in enumerate(range(2, KMAX + 1)):
        filas.append({"variante": nombre, "K": K, "delta_obs": dobs[i],
                      **{f"p95_{v}": np.nanpercentile(s[:, i], 95) for v, s in sims.items()},
                      **{f"p_{v}": p_hat(dobs[i], s[:, i]) for v, s in sims.items()},
                      "cortes": " ".join(f[c] for c in cortes[K])})
    resumen.append({"variante": nombre, **{f"K*_{v}": k for v, k in kstar.items()},
                    "umbral10": ns["regla_umbral"](scd, .10), "mayor_caida": ns["regla_caida"](scd)})
    print(nombre, kstar, flush=True)
pd.DataFrame(filas).to_csv(SAL / "exploracion_niveles_particion.csv", index=False)
pd.DataFrame(resumen).to_csv(SAL / "exploracion_niveles_resumen.csv", index=False)
pd.set_option("display.width", 250)
print(pd.DataFrame(resumen).to_string(index=False))
print(pd.DataFrame(filas).round(3).to_string(index=False))
