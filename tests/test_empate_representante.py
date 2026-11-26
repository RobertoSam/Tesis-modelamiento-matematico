"""Pruebas de src/multivariado.empate_maximo_abs (hallazgo m-01 de la auditoría de la iteración 3c)."""

import numpy as np

from src.multivariado import TOL_EMPATE_REPRESENTANTE, empate_maximo_abs


def test_clase_de_dos_series_empate_estructural():
    # En una clase de dos series estandarizadas, ambas tienen |r| = sqrt((1 + |r12|) / 2) con el
    # primer componente de la clase: el máximo de |r| siempre está empatado
    rng = np.random.default_rng(20261126)
    for _ in range(50):
        n = int(rng.integers(30, 300))
        x = rng.standard_normal(n)
        y = float(rng.uniform(-0.95, 0.95)) * x + rng.standard_normal(n)
        Z = np.column_stack([x, y])
        Z = (Z - Z.mean(0)) / Z.std(0)
        R = np.corrcoef(Z, rowvar=False)
        val, vec = np.linalg.eigh(R)
        f = Z @ vec[:, -1]
        r = [np.corrcoef(Z[:, j], f)[0, 1] for j in range(2)]
        assert np.allclose(np.abs(r), np.sqrt((1 + abs(R[0, 1])) / 2))
        assert empate_maximo_abs(r)


def test_cifras_de_la_auditoria():
    # Los valores de 07c_hfc_clases3.csv (filas 16-17) y de R_hfc_clases3.csv para C3
    assert empate_maximo_abs([-0.8676372370227423, 0.8676372370227425])
    assert empate_maximo_abs([-0.867637237022742, 0.867637237022743])


def test_sin_empate_y_una_serie():
    assert not empate_maximo_abs([0.9815437600325186, 0.9851689686021513, 0.9255291370212018])
    assert not empate_maximo_abs([0.9999999999999998])
    # Una diferencia mayor que la tolerancia relativa no es empate
    assert not empate_maximo_abs([0.5, 0.5 * (1 + 10 * TOL_EMPATE_REPRESENTANTE)])
    assert empate_maximo_abs([0.5, -0.5 * (1 + 0.1 * TOL_EMPATE_REPRESENTANTE)])
