"""Pruebas de la opción sin centrar de `coef_rv` (adenda 3b, §1.2 y §7.1).

El comportamiento por defecto (columnas centradas) no cambia; `centrar=False` se agrega como
opción y su uso en el análisis queda pendiente de D17. Las mismas comprobaciones se corren sobre
el código R (`R/07b_nulo_estructura.R` y el Rmd final), extrayendo la función del archivo.
"""

import os
import re
import shutil
import subprocess

import numpy as np
import pytest

from src.multivariado import coef_rv

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _rv_anterior(X, Y):
    # Copia literal de la implementación anterior a la opción (commit 2be3665)
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    X = X - X.mean(axis=0)
    Y = Y - Y.mean(axis=0)
    Sx = X @ X.T
    Sy = Y @ Y.T
    return float(np.sum(Sx * Sy) / np.sqrt(np.sum(Sx * Sx) * np.sum(Sy * Sy)))


def _fijas():
    # Matrices deterministas 16 × 3 (sin generador aleatorio, para comparar con R)
    i = np.arange(1, 17)[:, None]
    j = np.arange(1, 4)[None, :]
    X = np.sin(i * j) + 0.5
    Y = np.cos(i + 2 * j) + 0.3 * X
    return X, Y


def test_por_defecto_sin_cambios():
    rng = np.random.default_rng(2026)
    for _ in range(20):
        X, Y = rng.normal(size=(17, 3)), rng.normal(size=(17, 3)) + 0.4
        assert coef_rv(X, Y) == _rv_anterior(X, Y)
        assert coef_rv(X, Y, centrar=True) == _rv_anterior(X, Y)
    X, Y = _fijas()
    assert coef_rv(X, Y) == _rv_anterior(X, Y)


def test_sin_centrar_valor_analitico():
    # Una columna común (todas las cargas iguales) frente a un solo eje: tr(Sx Sy) = 1,
    # tr(Sx²) = 9 y tr(Sy²) = 1, de modo que RV = 1/3. Centrada, la primera configuración es nula.
    X = np.ones((3, 1))
    Y = np.array([[1.0], [0.0], [0.0]])
    assert coef_rv(X, Y, centrar=False) == pytest.approx(1 / 3, abs=1e-15)
    with np.errstate(invalid='ignore', divide='ignore'):
        assert np.isnan(coef_rv(X, Y))


def test_sin_centrar_invariante_a_rotaciones_y_signos():
    X, _ = _fijas()
    Q, _ = np.linalg.qr(np.array([[2.0, 1.0, 0.5], [0.3, -1.0, 2.0], [1.0, 0.0, -1.0]]))
    assert coef_rv(X, X @ Q, centrar=False) == pytest.approx(1.0, abs=1e-12)
    assert coef_rv(X, X * np.array([1, -1, -1]), centrar=False) == pytest.approx(1.0, abs=1e-12)
    # y al orden de los ejes (cruces λ2 ↔ λ3)
    assert coef_rv(X, X[:, [0, 2, 1]], centrar=False) == pytest.approx(1.0, abs=1e-12)


def test_columnas_centradas_ambas_variantes_coinciden():
    X, Y = _fijas()
    Xc, Yc = X - X.mean(axis=0), Y - Y.mean(axis=0)
    assert coef_rv(Xc, Yc, centrar=False) == pytest.approx(coef_rv(X, Y), abs=1e-14)


def _funcion_r(archivo):
    """Texto de `coef_rv <- function(...) { ... }` en un archivo R o Rmd."""
    texto = open(os.path.join(RAIZ, archivo), encoding='utf-8').read()
    m = re.search(r'^coef_rv <- function\(.*?^\}\s*$', texto, flags=re.S | re.M)
    assert m, f'no se encontró coef_rv en {archivo}'
    return m.group(0)


@pytest.mark.skipif(shutil.which('Rscript') is None, reason='Rscript no disponible')
@pytest.mark.parametrize('archivo', ['R/07b_nulo_estructura.R', 'R/ciclo_financiero_final.Rmd'])
def test_paridad_con_r(archivo):
    if not os.path.exists(os.path.join(RAIZ, archivo)):
        pytest.skip(f'{archivo} aún no existe')
    X, Y = _fijas()
    codigo = _funcion_r(archivo) + '''
i <- 1:16; j <- 1:3
X <- outer(i, j, function(a, b) sin(a * b)) + 0.5
Y <- outer(i, j, function(a, b) cos(a + 2 * b)) + 0.3 * X
cat(sprintf("%.17g %.17g %.17g\\n", coef_rv(X, Y), coef_rv(X, Y, centrar = TRUE), coef_rv(X, Y, centrar = FALSE)))
cat(sprintf("%.17g\\n", coef_rv(matrix(1, 3, 1), matrix(c(1, 0, 0), 3, 1), centrar = FALSE)))
'''
    salida = subprocess.run(['Rscript', '-e', codigo], capture_output=True, text=True, check=True).stdout.split()
    r_def, r_cen, r_sin, r_ana = map(float, salida)
    assert r_def == pytest.approx(coef_rv(X, Y), abs=1e-14)
    assert r_cen == r_def
    assert r_sin == pytest.approx(coef_rv(X, Y, centrar=False), abs=1e-14)
    assert r_ana == pytest.approx(1 / 3, abs=1e-15)
