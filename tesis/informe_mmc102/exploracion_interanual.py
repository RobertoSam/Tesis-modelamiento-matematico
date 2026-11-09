"""Exploración (no incorporada a la tesis): ¿ayuda la variación interanual a identificar regímenes?

Transformación: variación de 12 meses en logaritmos para montos, índices, tipo de cambio,
reservas y EMBIG; diferencia de 12 meses en puntos porcentuales para las cuatro tasas.
Se repite la cadena de la sección 3.2 con los mismos contrastes:
  - PCA: proporción de inercia de cada eje frente a series independientes con la misma
    autocorrelación (bloques de 24 meses remuestreados por separado en cada serie);
  - trayectoria de posición (F1–F3, sin suavizar y con media móvil centrada de 12 meses):
    Δ_K frente a la misma referencia;
  - trayectoria de estructura (λ1 del EPCA, w = 48, ν = 3): Δ_K frente a series con estructura
    constante (bloques conjuntos de 24 meses de las filas).
Salidas: data/results/final/mmc102/exploracion_interanual_*.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tesis/informe_mmc102"))
from src import particion as pt                      # noqa: E402
from src.datos import cargar_vias                    # noqa: E402
from src.parametros import leer_parametros           # noqa: E402
from src.remuestreo import indices_desde_inicios     # noqa: E402

SAL = RAIZ / "data/results/final/mmc102"
KMAX, NMIN, ELL, B = 10, 12, 24, 500
rng = np.random.default_rng(12)

PAR = leer_parametros(RAIZ)
X, _ = cargar_vias(RAIZ, excluidas=PAR["EXCLUIDAS"])
TASAS = ["Tasa de referencia", "Tasa interbancaria", "TAMN", "TIPMN"]
T = pd.DataFrame(index=X.index[12:])
for c in X.columns:
    x = X[c].to_numpy(dtype=float)
    T[c] = (x[12:] - x[:-12]) if c in TASAS else 100 * (np.log(x[12:]) - np.log(x[:-12]))
fechas = np.array([str(f)[:7] for f in T.index])
A = T.to_numpy()
n, p = A.shape
print(f"Variación interanual: {n} meses ({fechas[0]} a {fechas[-1]}) × {p} series")

# Reutiliza las funciones de la cadena principal sin ejecutar su programa
import importlib.util  # noqa: E402
fuente = (RAIZ / "tesis/informe_mmc102/calculos_cap4_segmentacion.py").read_text()
defs = fuente.split("# ------------------------------------------------------------------ 1.")[0]
defs = defs.split("# ------------------------------------------------------------------ utilidades")[1]
ns = {"np": np, "pd": pd, "pt": pt, "W": 48, "NU": 3, "KMAX": KMAX, "NMIN": NMIN, "D": 3, "LMM": 12}
from src import camiz_port as cp  # noqa: E402
ns["cp"] = cp
exec(defs, ns)
lambda1_trayectoria, particionar, deltas = ns["lambda1_trayectoria"], ns["particionar"], ns["deltas"]
media_movil_centrada, p_hat = ns["media_movil_centrada"], ns["p_hat"]
regla_umbral, regla_caida = ns["regla_umbral"], ns["regla_caida"]


def bloques(m):
    return indices_desde_inicios(rng.integers(1, m - ELL + 2, int(np.ceil(m / ELL))), ELL, m)


def pos(M, suav):
    _, _, S = pt.scores_pca_rcamiz(M)
    Y = S[:, :3]
    if suav:
        Y = np.column_stack([media_movil_centrada(Y[:, k]) for k in range(3)])
    ok = ~np.isnan(Y).any(axis=1)
    return Y[ok], ok


val, V, S = pt.scores_pca_rcamiz(A)
iner = val / p
obs = {"pos_sin": deltas(particionar(pos(A, False)[0])[1]),
       "pos_mm": deltas(particionar(pos(A, True)[0])[1])}
l1 = lambda1_trayectoria(A)
obs["estructura"] = deltas(particionar(l1)[1])

sim_iner, sim = [], {k: [] for k in obs}
for b in range(B):
    # Referencia independiente: cada serie remuestreada por separado (sin asociación)
    Mi = np.column_stack([A[bloques(n), j] for j in range(p)])
    v, _, _ = pt.scores_pca_rcamiz(Mi)
    sim_iner.append(v[:3] / p)
    sim["pos_sin"].append(deltas(particionar(pos(Mi, False)[0])[1]))
    sim["pos_mm"].append(deltas(particionar(pos(Mi, True)[0])[1]))
    # Referencia con estructura constante: filas remuestreadas en bloques conjuntos
    Mc = A[bloques(n)]
    sim["estructura"].append(deltas(particionar(lambda1_trayectoria(Mc))[1]))
sim_iner = np.array(sim_iner)
sim = {k: np.array(v) for k, v in sim.items()}

filas = [{"eje": k + 1, "inercia": iner[k], "p95_ref": np.percentile(sim_iner[:, k], 95),
          "p": p_hat(iner[k], sim_iner[:, k])} for k in range(3)]
pd.DataFrame(filas).to_csv(SAL / "exploracion_interanual_ejes.csv", index=False)

cargas = pd.DataFrame(V[:, :3] * np.sqrt(val[:3]), index=X.columns, columns=["Eje 1", "Eje 2", "Eje 3"])
cargas.to_csv(SAL / "exploracion_interanual_cargas.csv")

tray = {"pos_sin": (pos(A, False), "posición sin suavizar"), "pos_mm": (pos(A, True), "posición, media centrada"),
        "estructura": ((l1[:, None], None), "estructura (λ1)")}
fil = []
for k, ((Y, ok), nombre) in tray.items():
    f = fechas[ok] if ok is not None else fechas[24: 24 + len(l1)]
    ks, scd, cortes = particionar(Y)
    p95 = np.nanpercentile(sim[k], 95, axis=0)
    sup = np.nonzero(obs[k] > p95)[0]
    kref = int(sup.max() + 2) if len(sup) else 1
    for i, K in enumerate(range(2, KMAX + 1)):
        fil.append({"trayectoria": nombre, "K": K, "delta_obs": obs[k][i], "p95_ref": p95[i],
                    "p": p_hat(obs[k][i], sim[k][:, i]), "cortes": " ".join(f[c] for c in cortes[K])})
    fil.append({"trayectoria": nombre, "K": f"K* = {kref}", "delta_obs": np.nan, "p95_ref": np.nan, "p": np.nan,
                "cortes": f"umbral 10 %: K={regla_umbral(scd, .10)}; mayor caída: K={regla_caida(scd)}"})
pd.DataFrame(fil).to_csv(SAL / "exploracion_interanual_particion.csv", index=False)
pd.DataFrame(S[:, :3], index=fechas, columns=["F1", "F2", "F3"]).to_csv(SAL / "exploracion_interanual_scores.csv")
print(pd.DataFrame(filas).round(3).to_string(index=False))
print(pd.DataFrame(fil).round(3).to_string(index=False))
