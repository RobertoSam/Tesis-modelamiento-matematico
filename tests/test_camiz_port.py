# Pruebas unitarias mínimas de src/camiz_port.py (port de R/camiz_port.R, decisión D6).
# Ejecutar desde la raíz del repositorio:  python3 -m pytest tests/test_camiz_port.py -q
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src import camiz_port as cp

RAIZ = Path(__file__).resolve().parents[1]
SEMILLA = 2026          # semilla fija para los datos simulados de las pruebas


# ---- Fisher -------------------------------------------------------------------

def _sce(y):
    return float(np.sum((y - y.mean()) ** 2))


def test_fisher_coincide_con_busqueda_exhaustiva():
    # Para series cortas, la partición óptima en k clases contiguas se verifica por fuerza bruta
    rng = np.random.default_rng(SEMILLA)
    y = rng.normal(size=12) + np.repeat([0.0, 3.0, -1.0], 4)
    f = cp.fisher(y, 4)
    n = len(y)
    for k in (2, 3, 4):
        mejor, lim_mejor = np.inf, None
        for cortes in itertools.combinations(range(1, n), k - 1):
            b = (0,) + cortes + (n,)
            s = sum(_sce(y[b[i]:b[i + 1]]) for i in range(k))
            if s < mejor - 1e-12:
                mejor, lim_mejor = s, list(cortes) + [n]
        assert f["criter"][k - 1] == pytest.approx(mejor, abs=1e-10)
        assert list(f["mod1out"][k - 1, :k].astype(int)) == lim_mejor
    assert f["criter"][0] == f["criter"][1]          # convención de fishersub


# ---- HFC -----------------------------------------------------------------------

def test_distancia_hfc_son_los_valores_propios_2x2():
    a, b, c = 1.3, 0.7, 0.4
    d, l1, al, be = cp.distancia_hfc(a, b, c)
    val = np.linalg.eigvalsh(np.array([[a, c], [c, b]]))
    assert d == pytest.approx(val[0]) and l1 == pytest.approx(val[1])
    assert al ** 2 + be ** 2 == pytest.approx(1.0)


def _datos_bloques(n=200, semilla=SEMILLA):
    # Dos bloques independientes de variables muy correlacionadas entre sí
    rng = np.random.default_rng(semilla)
    f1, f2 = rng.normal(size=(2, n))
    X = np.column_stack([f1 + 0.3 * rng.normal(size=n) for _ in range(3)] +
                        [f2 + 0.3 * rng.normal(size=n) for _ in range(3)])
    return pd.DataFrame(X, columns=[f"v{i}" for i in range(1, 7)])


def test_clahfac_separa_los_bloques_y_conserva_la_inercia():
    h = cp.clahfac(_datos_bloques())
    j = h["hierar"]
    p = 6
    raiz = j.iloc[-1]
    hojas = lambda k: set(v for v in h["nclass"].loc[k] if v > 0) if k > p else {k}
    assert {frozenset(hojas(int(raiz.N1))), frozenset(hojas(int(raiz.N2)))} == {frozenset({1, 2, 3}), frozenset({4, 5, 6})}
    # Inercia perdida en las fusiones + varianza del factor raíz = traza (p)
    ine = h["inertia"].loc["Inertia"]
    assert ine["Hierarchy"] + ine["Repr_Var"] == pytest.approx(ine["Total"])
    assert ine["Total"] == pytest.approx(p)
    # El factor A de la raíz tiene varianza Eigenv
    assert np.var(h["repvar"].iloc[:, -2].to_numpy()) == pytest.approx(raiz.Eigenv)


def test_partclas_y_rand_ajustado():
    h = cp.clahfac(_datos_bloques())
    pos = cp.partclas(h["hier"], 2)["partition"]["Position"].to_numpy()
    assert len(set(pos[:3])) == 1 and len(set(pos[3:])) == 1 and pos[0] != pos[3]
    a = np.array([1, 1, 2, 2, 3, 3])
    assert cp.rand_ajustado(a, a) == pytest.approx(1.0)
    assert cp.rand_ajustado(a, np.array([9, 9, 7, 7, 5, 5])) == pytest.approx(1.0)   # invariante a etiquetas


def test_cofenetica_de_una_jerarquia_conocida():
    hier = {"merge": np.array([[-1, -2], [-3, 1]]), "height": np.array([1.0, 2.0]), "labels": ["a", "b", "c"]}
    C = cp.cofenetica(hier)
    assert C[0, 1] == 1.0 and C[0, 2] == 2.0 and C[1, 2] == 2.0
    assert cp.cor_cofenetica(hier, hier) == pytest.approx(1.0)


# ---- aede ----------------------------------------------------------------------

def test_aede_valores_propios_signo_y_calinski_harabasz():
    rng = np.random.default_rng(SEMILLA)
    X = pd.DataFrame(rng.normal(size=(80, 5)).cumsum(axis=0), index=[f"t{i}" for i in range(80)])
    a = cp.aede(X, nw=24, ndim=2, nsd=0, maxcl=5)
    # Primera ventana: valores propios de la matriz de correlación (divisor n)
    v0 = np.sort(np.linalg.eigvalsh(np.corrcoef(X.iloc[:24].to_numpy(), rowvar=False)))[::-1][:2]
    assert np.allclose(a["eigenvalues"].iloc[0].to_numpy(), v0, atol=1e-12)
    # Etiqueta de la ventana: fila 1 + nw/2 (1-based), como en R
    assert a["eigenvalues"].index[0] == "t12"
    # Regla de signo lineal en la primera ventana: suma de positivos >= |suma de negativos|
    vec = a["correlationsgn"][0] / np.sqrt(a["eigenvalues"].iloc[0].to_numpy())
    for k in range(2):
        assert vec[vec[:, k] > 0, k].sum() >= abs(vec[vec[:, k] < 0, k].sum())
    # CH de aede = variante k de ch_variantes
    part = a["cutpoints"]["part"]
    ch = cp.ch_variantes(part["Within ssq"].to_numpy(), len(a["eigenvalues"]))
    assert np.allclose(ch["k"][1:], part["Calinski-Harabasz"].to_numpy()[1:])
    r = cp.resumen_aede(a)
    assert 2 <= r["k_codo"] <= 4 and len(r["cortes_codo"]) == r["k_codo"] - 1


def test_pesos_gaussianos_suman_uno_y_son_simetricos():
    w = cp.pesos_aede(60, 3)
    assert w.sum() == pytest.approx(1.0) and np.allclose(w, w[::-1]) and w[30] > w[0]


# ---- Lector como R ---------------------------------------------------------------

def test_strtod_r_reproduce_el_doble_redondeo_de_R():
    assert cp.strtod_r("85281.551109") == 85281.55110899999      # valor que da read.csv de R
    assert cp.strtod_r("0.5") == 0.5 and cp.strtod_r("-3.25") == -3.25 and cp.strtod_r("12") == 12.0


# ---- Regresión contra los CSV de R (si existen) ------------------------------------

@pytest.mark.skipif(not (RAIZ / "data/results/niveles/R_hfc_jerarquia.csv").exists(), reason="sin CSV de R")
def test_regresion_jerarquia_niveles_contra_R():
    cols = ["Crédito empresarial", "Crédito consumo", "Crédito hipotecario", "Liquidez M1", "Liquidez M2",
            "Liquidez M3", "Tasa referencia BCRP", "Tasa interbancaria", "Tasa activa TAMN",
            "Tasa pasiva TIPMN", "IPC Lima", "Tipo de cambio", "Índice BVL", "embi_peru",
            "PBI desestacionalizado", "Demanda interna", "Reservas internacionales"]
    niv = cp.leer_csv_como_r(RAIZ / "data/processed/dataset_niveles_mensual.csv")
    h = cp.clahfac(niv[cols])
    ref = pd.read_csv(RAIZ / "data/results/niveles/R_hfc_jerarquia.csv", index_col=0)
    assert (h["hierar"][["N1", "N2"]].to_numpy() == ref[["N1", "N2"]].to_numpy()).all()
    assert np.max(np.abs(h["hierar"][["Eigenv", "Index"]].to_numpy() - ref[["Eigenv", "Index"]].to_numpy())) < 1e-10
