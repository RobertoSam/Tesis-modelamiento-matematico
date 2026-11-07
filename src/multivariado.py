"""
Funciones multivariadas sin dependencia de torch (iteración 3a).

Traducción a Python de las funciones del bloque `funciones` de
`R/tesis_ciclo_financiero.Rmd`, con los mismos estimadores, para que el notebook 05 y el
Rmd den el mismo resultado numérico (paridad Python–R):

- estandarizar: media 0 y desviación poblacional 1 (divisor n), como `estandarizar` del Rmd
  y `StandardScaler` de scikit-learn;
- pca_correlacion: descomposición espectral de la matriz de correlaciones (divisor n) con la
  regla de signo determinística de Rcamiz (cuadrática: se invierte el vector propio si la suma de
  cuadrados de sus coeficientes negativos supera la de los positivos), como `pca_basico`;
- horn, vara_quebrada, tucker, coef_rv, procrustes;
- kmo y bartlett_esfericidad, como las funciones `kmo` y `bartlett_esfericidad` del Rmd;
- numero_condicion y log_det: diagnósticos de colinealidad de la matriz de correlaciones.

No modifica `notebooks/modelos_dl.py` (que importa torch); la unificación queda para cuando
haya torch en el entorno.
"""

import numpy as np
import pandas as pd
from scipy import stats


# ---- Estandarización y PCA -------------------------------------------------------------

def estandarizar(X):
    """Centra y divide por la desviación poblacional (divisor n), columna por columna."""
    X = np.asarray(X, dtype=float)
    m = X.mean(axis=0)
    s = np.sqrt(((X - m) ** 2).mean(axis=0))
    return (X - m) / s


def invierte_cuadratica(v):
    """Regla de signo de Rcamiz: True si domina la suma de cuadrados de los coeficientes negativos."""
    v = np.asarray(v, dtype=float)
    return np.sum(v[v < 0] ** 2) > np.sum(v[v > 0] ** 2)


def invierte_lineal(v):
    """Regla de signo de aede (AedeClahfac): True si |suma de negativos| > suma de positivos."""
    v = np.asarray(v, dtype=float)
    return abs(np.sum(v[v < 0])) > np.sum(v[v > 0])


def pca_correlacion(Z):
    """
    PCA de la matriz de correlaciones de Z (ya estandarizada, divisor n).

    Devuelve un diccionario con:
      valores  : valores propios en orden decreciente (suman p);
      vectores : vectores propios (columnas) orientados con la regla de Rcamiz;
      cargas   : correlaciones serie–componente (vector propio por la raíz del valor propio);
      scores   : coordenadas de los meses (Z @ vectores).
    """
    Z = np.asarray(Z, dtype=float)
    n = Z.shape[0]
    R = Z.T @ Z / n
    valores, vectores = np.linalg.eigh(R)
    orden = np.argsort(valores)[::-1]          # eigh devuelve orden creciente
    valores = valores[orden]
    vectores = vectores[:, orden].copy()
    for k in range(vectores.shape[1]):
        if invierte_cuadratica(vectores[:, k]):
            vectores[:, k] = -vectores[:, k]
    cargas = vectores * np.sqrt(np.clip(valores, 0, None))
    return {'R': R, 'valores': valores, 'vectores': vectores, 'cargas': cargas,
            'scores': Z @ vectores}


def cos2(cargas):
    """Calidad de representación cos²_jk = r_jk² (cada fila suma 1 sobre los p ejes)."""
    return np.asarray(cargas) ** 2


def contribuciones(vectores):
    """Contribución (%) de cada serie a la construcción de cada eje: 100 · v_jk²."""
    return 100 * np.asarray(vectores) ** 2


def vara_quebrada(p):
    """Inercia esperada (%) de cada componente bajo el modelo de vara quebrada."""
    return 100 * np.cumsum(1 / np.arange(p, 0, -1))[::-1] / p


def horn(X, n_sim=1000, percentil=0.95, semilla=42):
    """
    Análisis paralelo de Horn (1965) [VERIFICAR: ficha horn_1965; solo se leyó el resumen]: percentil 95 de los valores propios de
    matrices de correlación de datos gaussianos independientes del mismo tamaño.

    El generador (numpy PCG64 con la semilla dada) es distinto del de R: los umbrales difieren
    en el tercer decimal y la paridad se exige solo en el número de componentes retenidos.
    """
    X = np.asarray(X, dtype=float)
    n, p = X.shape
    obs = np.sort(np.linalg.eigvalsh(np.corrcoef(X, rowvar=False)))[::-1]
    rng = np.random.default_rng(semilla)
    sims = np.empty((n_sim, p))
    for b in range(n_sim):
        G = rng.standard_normal((n, p))
        sims[b] = np.sort(np.linalg.eigvalsh(np.corrcoef(G, rowvar=False)))[::-1]
    umbral = np.quantile(sims, percentil, axis=0)
    retener = 0
    for j in range(p):
        if obs[j] > umbral[j]:
            retener += 1
        else:
            break
    return {'observados': obs, 'umbral': umbral, 'retener': retener}


def umbral_horn(n, p, n_sim=1000, percentil=0.95, semilla=2026):
    """Percentil de Horn de los valores propios con n observaciones gaussianas de p series.

    Es el umbral de `horn` sin los valores observados (iteración 3b, D5: umbral por ventana con
    n = ceil(n_omega) de Kish). Generador PCG64 de numpy: distinto del de R (excepción de
    generadores de la iteración 3a).
    """
    rng = np.random.default_rng(semilla)
    sims = np.empty((n_sim, p))
    for b in range(n_sim):
        G = rng.standard_normal((n, p))
        sims[b] = np.sort(np.linalg.eigvalsh(np.corrcoef(G, rowvar=False)))[::-1]
    return np.quantile(sims, percentil, axis=0)


def n_kish(w):
    """n efectivo de Kish de unos pesos: 1 / sum(w^2), con los pesos normalizados a suma 1."""
    w = np.asarray(w, dtype=float)
    w = w / w.sum()
    return float(1 / np.sum(w ** 2))


# ---- Comparación de configuraciones -----------------------------------------------------

def tucker(a, b):
    """Coeficiente de congruencia de Tucker entre dos vectores de cargas."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.sum(a * b) / np.sqrt(np.sum(a ** 2) * np.sum(b ** 2)))


def emparejar_componentes(C_ref, C, K=4, candidatos=6):
    """
    Empareja cada componente k = 1..K de C_ref con la componente de C (entre las `candidatos`
    primeras) de mayor |congruencia|, sin repetir, en orden k = 1, 2, ... (regla codiciosa del
    bootstrap del Rmd). Devuelve índices (0-based), congruencias absolutas y signos.
    """
    usadas, idx, cong, signo = [], [], [], []
    for k in range(K):
        tk = np.array([0.0 if j in usadas else abs(tucker(C_ref[:, k], C[:, j]))
                       for j in range(candidatos)])
        j = int(np.argmax(tk))                 # primer máximo, como which.max de R
        usadas.append(j)
        idx.append(j)
        cong.append(tk[j])
        signo.append(np.sign(tucker(C_ref[:, k], C[:, j])))
    return np.array(idx), np.array(cong), np.array(signo)


def coef_rv(X, Y, centrar=True):
    """Coeficiente RV de Robert y Escoufier entre dos configuraciones de las mismas filas.

    RV = tr(Sx Sy) / sqrt(tr(Sx²) tr(Sy²)), con Sx = X Xᵀ y Sy = Y Yᵀ.

    `centrar=True` (por defecto, el comportamiento de siempre) resta antes la media de cada
    columna. `centrar=False` usa X e Y tal cual: es la variante para comparar **cargas**
    (series × ejes), donde el centrado restaría la carga media de cada eje (adenda del
    26-oct-2026, §1.2). Su uso en el análisis queda pendiente de D17; aquí solo se ofrece la
    opción. Con columnas ya centradas, ambas variantes coinciden. Si una configuración es nula
    (p. ej., una columna constante centrada), el cociente no está definido y se devuelve nan.
    """
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    if centrar:
        X = X - X.mean(axis=0)
        Y = Y - Y.mean(axis=0)
    Sx = X @ X.T
    Sy = Y @ Y.T
    return float(np.sum(Sx * Sy) / np.sqrt(np.sum(Sx * Sx) * np.sum(Sy * Sy)))


def procrustes(Z, referencia):
    """Rotación ortogonal de Procrustes de Z (centrada) hacia la referencia (centrada)."""
    Zc = np.asarray(Z, dtype=float) - np.mean(Z, axis=0)
    Rc = np.asarray(referencia, dtype=float) - np.mean(referencia, axis=0)
    u, _, vt = np.linalg.svd(Zc.T @ Rc)
    return Zc @ (u @ vt)


# ---- Adecuación muestral ---------------------------------------------------------------

def bartlett_esfericidad(R, n):
    """
    Prueba de esfericidad de Bartlett (1950, 1951) [VERIFICAR: texto no consultado; no se
    verificó en cuál de las dos obras se formula la prueba]:
    chi² = -(n - 1 - (2p + 5)/6) · ln|R|, con p(p - 1)/2 grados de libertad.
    Si el factor (n - 1 - (2p + 5)/6) no es positivo (n pequeño), el estadístico no está
    definido y se devuelve NaN.
    """
    R = np.asarray(R, dtype=float)
    p = R.shape[0]
    factor = n - 1 - (2 * p + 5) / 6
    gl = p * (p - 1) / 2
    if factor <= 0:
        return {'estadistico': np.nan, 'gl': gl, 'p_valor': np.nan, 'factor': factor}
    _, logdet = np.linalg.slogdet(R)
    estad = -factor * logdet
    return {'estadistico': estad, 'gl': gl, 'p_valor': stats.chi2.sf(estad, gl), 'factor': factor}


def kmo(R):
    """
    Medida KMO de adecuación muestral (Kaiser, 1970; Kaiser y Rice, 1974) [VERIFICAR: texto no
    consultado; la forma de la medida solo consta en la documentación de psych], global
    y por serie, a partir de la matriz anti-imagen: correlaciones parciales
    q_ij = -(R⁻¹)_ij / sqrt((R⁻¹)_ii (R⁻¹)_jj).
    """
    R = np.asarray(R, dtype=float)
    Ri = np.linalg.inv(R)
    d = np.sqrt(np.diag(Ri))
    parcial = -Ri / np.outer(d, d)
    np.fill_diagonal(parcial, 0)
    R0 = R.copy()
    np.fill_diagonal(R0, 0)
    r2 = (R0 ** 2).sum(axis=0)
    q2 = (parcial ** 2).sum(axis=0)
    return {'global': float(r2.sum() / (r2.sum() + q2.sum())), 'por_variable': r2 / (r2 + q2)}


def numero_condicion(R):
    """Número de condición de R: cociente entre el mayor y el menor valor propio."""
    v = np.linalg.eigvalsh(np.asarray(R, dtype=float))
    return float(v.max() / v.min())


def log_det(R):
    """ln|R| (suma de los logaritmos de los valores propios)."""
    signo, valor = np.linalg.slogdet(np.asarray(R, dtype=float))
    if signo <= 0:
        return np.nan
    return float(valor)


def tabla_correlaciones(X, nombres):
    """Matriz de correlaciones de Pearson como DataFrame con los nombres de las series."""
    return pd.DataFrame(np.corrcoef(np.asarray(X, dtype=float), rowvar=False),
                        index=nombres, columns=nombres)
