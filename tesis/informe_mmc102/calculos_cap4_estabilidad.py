"""Estabilidad de la estructura global y contraste global del cambio de estructura (sección 3.2.5).

1. Estabilidad: 500 réplicas por remuestreo conjunto, en bloques de ℓ meses (12, 24, 36), de los
   incrementos mensuales, acumulados desde el valor inicial. PCA: congruencia de los ejes 1–3 con
   el original (emparejados por |congruencia| entre los 6 primeros) y valores propios. HFC:
   índice de Rand ajustado de la partición en tres clases y correlación cofenética.
2. Cambio de estructura: RV entre las cargas de los ejes 1–2 de ventanas adyacentes sin meses
   comunes (w = 48, ν = 3); estadístico global = mínimo del RV; 200 réplicas de estructura
   constante (bloques conjuntos de 24 meses de los incrementos).
Salidas: data/results/final/mmc102/estabilidad_*.csv, cambio_estructura_*.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
from src import camiz_port as cp                     # noqa: E402
from src import particion as pt                      # noqa: E402
from src.datos import cargar_vias                    # noqa: E402
from src.nulo_estructura import serie_nula           # noqa: E402
from src.parametros import leer_parametros           # noqa: E402
from src.remuestreo import indices_desde_inicios     # noqa: E402

SAL = RAIZ / "data/results/final/mmc102"
rng = np.random.default_rng(20261110)
PAR = leer_parametros(RAIZ)
X, _ = cargar_vias(RAIZ, excluidas=PAR["EXCLUIDAS"])
A = X.to_numpy(float)
n, p = A.shape
etiquetas = list(X.columns)


def jerarquia(M):
    H = cp.clahfac(M)["hierar"].reset_index(drop=True)
    merge = np.array([[-int(a) if a <= p else int(a) - p for a in (r.N1, r.N2)] for r in H.itertuples()])
    return {"merge": merge, "height": H["Index"].to_numpy(float), "labels": etiquetas,
            "order": np.arange(1, p + 1)}


def clases_07(h, umbral=0.7):
    nodos = {}
    for i, (a, b) in enumerate(h["merge"], start=1):
        nodos[i] = ({-a} if a < 0 else nodos[a]) | ({-b} if b < 0 else nodos[b])
    clases = [{i} for i in range(1, p + 1)]
    for i in range(1, p):
        if h["height"][i - 1] <= umbral:
            clases = [c for c in clases if not c <= nodos[i]] + [nodos[i]]
    lab = np.zeros(p, int)
    for k, c in enumerate(clases):
        for j in c:
            lab[j - 1] = k
    return lab


def ejes(M, k=6):
    val, V, _ = pt.scores_pca_rcamiz(M)
    return val, V[:, :k] * np.sqrt(val[:k])


val0, C0 = ejes(A)
h0 = jerarquia(A)
lab0 = clases_07(h0)
filas = []
for ell in (12, 24, 36):
    for r in range(500):
        D = np.diff(A, axis=0)
        fil = indices_desde_inicios(rng.integers(1, len(D) - ell + 2, int(np.ceil(len(D) / ell))), ell, len(D))
        M = np.vstack([A[0], A[0] + np.cumsum(D[fil], axis=0)])
        val, C = ejes(M)
        fila = {"L": ell, "replica": r + 1}
        for k in range(3):
            cong = [abs(np.dot(C0[:, k], C[:, j]) / np.linalg.norm(C0[:, k]) / np.linalg.norm(C[:, j])) for j in range(6)]
            j = int(np.argmax(cong))
            fila[f"cong_{k + 1}"] = cong[j]
            fila[f"lambda_{k + 1}"] = val[k]
        if ell == 24:
            h = jerarquia(M)
            fila["ari_3"] = adjusted_rand_score(lab0, clases_07(h))
            fila["n_clases"] = len(set(clases_07(h)))
            fila["cofenetica"] = cp.cor_cofenetica(h0, h)
        filas.append(fila)
    print("ℓ =", ell, "listo", flush=True)
est = pd.DataFrame(filas)
est.to_csv(SAL / "estabilidad_replicas.csv", index=False)
res = est.groupby("L").agg(**{f"cong{k}_p5": (f"cong_{k}", lambda s: s.quantile(.05)) for k in (1, 2, 3)},
                           **{f"cong{k}_mediana": (f"cong_{k}", "median") for k in (1, 2, 3)},
                           **{f"lambda{k}_p5": (f"lambda_{k}", lambda s: s.quantile(.05)) for k in (1, 2, 3)},
                           **{f"lambda{k}_p95": (f"lambda_{k}", lambda s: s.quantile(.95)) for k in (1, 2, 3)})
res.to_csv(SAL / "estabilidad_resumen.csv")
h24 = est[est.L == 24]
pd.Series({"prop_ari3_igual": float(np.mean(h24.ari_3 > 0.999)), "ari3_mediana": float(h24.ari_3.median()),
           "cofenetica_mediana": float(h24.cofenetica.median()),
           "prop_tres_clases": float(np.mean(h24.n_clases == 3))}).to_csv(SAL / "estabilidad_hfc.csv")
print(res.round(3).to_string())

# ---------------------------------------------------------------- cambio de estructura (mín. RV)
W, NU = 48, 3
om = cp.pesos_aede(W, NU)


def cargas_ventana(M, i):
    V = M[i:i + W]
    mu = om @ V
    Cc = V - mu
    S = (Cc * om[:, None]).T @ Cc
    d = np.sqrt(np.diag(S))
    d[d < 1e-12] = 1.0
    R = S / np.outer(d, d)
    val, vec = np.linalg.eigh(R)
    return vec[:, ::-1][:, :2] * np.sqrt(np.maximum(val[::-1][:2], 0))


def rv(a, c):
    aa, cc = a @ a.T, c @ c.T
    return np.trace(aa @ cc) / np.sqrt(np.trace(aa @ aa) * np.trace(cc @ cc))


def perfil_rv(M):
    nv = len(M) - W + 1
return_dummy = None
fechas = np.array([str(f)[:7] for f in X.index])


def perfil_rv(M):  # noqa: F811
    nv = len(M) - W + 1
    car = [cargas_ventana(M, i) for i in range(nv)]
    return np.array([rv(car[i], car[i + W]) for i in range(nv - W)])


obs = perfil_rv(A)
ini = pd.read_csv(RAIZ / "data/results/final/R_nulo_estructura_indices_L24.csv").sort_values("replica")
ini = ini.filter(like="inicio_").to_numpy(int)
sim = np.array([perfil_rv(serie_nula(X, "niveles", ini[r], 24).to_numpy()) for r in range(len(ini))])
frontera = fechas[W: W + len(obs)]                      # primer mes de la segunda ventana
pd.DataFrame({"frontera": frontera, "rv_obs": obs, "p05_sim": np.percentile(sim, 5, axis=0),
              "mediana_sim": np.median(sim, axis=0)}).to_csv(SAL / "cambio_estructura_perfil.csv", index=False)
mins = sim.min(axis=1)
pd.Series({"min_rv_obs": obs.min(), "frontera_min": frontera[int(np.argmin(obs))],
           "p_min": (1 + np.sum(mins <= obs.min())) / (len(mins) + 1),
           "min_rv_p05_sim": np.percentile(mins, 5), "replicas": len(mins)}).to_csv(SAL / "cambio_estructura_resumen.csv")
print(pd.read_csv(SAL / "cambio_estructura_resumen.csv").to_string())
print(pd.read_csv(SAL / "estabilidad_hfc.csv").to_string())
