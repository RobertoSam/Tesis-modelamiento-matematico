"""
Diagnósticos de series de tiempo para el PCA estático (notebook 05, iteración 3a).

- acf: autocorrelación muestral con el estimador de `stats::acf` de R (serie centrada en su
  media y divisor n en todos los rezagos);
- n_efectivo: tamaño muestral efectivo de una correlación entre dos series autocorrelacionadas;
- tendencia_y_residuos: regresión x_t = a + b t + e_t por MCO, ADF y KPSS sobre los residuos,
  Ljung-Box y clasificación TS / DS / indeterminada según la regla D5 de `decisiones.qmd`.

La especificación de D5 (términos determinísticos, rezagos y nivel) se fijó antes de calcular
y está en las constantes de abajo; el Rmd usa las mismas.
"""

import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import acorr_ljungbox

# ---- Especificación fijada de antemano (D5, 20-10-2026) --------------------------------
ADF_REZAGOS = 6        # rezagos de la diferencia en la regresión ADF (constante y tendencia)
KPSS_REZAGOS = 4       # truncamiento del núcleo de Bartlett en la KPSS (nula: tendencia)
ALFA_D5 = 0.05         # nivel de las dos pruebas
LJUNG_BOX_REZAGOS = 12

# Tablas de tseries::adf.test (constante y tendencia) y tseries::kpss.test (null = "Trend"),
# copiadas de tseries 0.10-55 para replicar su interpolación de p-valores.
_ADF_TABLA = -np.array([
    [4.38, 3.95, 3.60, 3.24, 1.14, 0.80, 0.50, 0.15],
    [4.15, 3.80, 3.50, 3.18, 1.19, 0.87, 0.58, 0.24],
    [4.04, 3.73, 3.45, 3.15, 1.22, 0.90, 0.62, 0.28],
    [3.99, 3.69, 3.43, 3.13, 1.23, 0.92, 0.64, 0.31],
    [3.98, 3.68, 3.42, 3.13, 1.24, 0.93, 0.65, 0.32],
    [3.96, 3.66, 3.41, 3.12, 1.25, 0.94, 0.66, 0.33]])
_ADF_T = np.array([25, 50, 100, 250, 500, 1e5])
_ADF_P = np.array([0.01, 0.025, 0.05, 0.10, 0.90, 0.95, 0.975, 0.99])
_KPSS_TABLA_TENDENCIA = np.array([0.216, 0.176, 0.146, 0.119])
_KPSS_P = np.array([0.01, 0.025, 0.05, 0.10])


# ---- Autocorrelación y tamaño muestral efectivo ----------------------------------------

def acf(x, rezagos):
    """ACF muestral como stats::acf de R: r_k = sum_{t>k} d_t d_{t-k} / sum_t d_t², d = x - media."""
    x = np.asarray(x, dtype=float)
    d = x - x.mean()
    den = np.sum(d * d)
    return np.array([np.sum(d[k:] * d[:len(d) - k]) / den if k > 0 else 1.0 for k in rezagos])


def n_efectivo(x, y, max_rezago=None):
    """
    Tamaño muestral efectivo de la correlación entre x e y
    Pyper y Peterman (1998) [VERIFICAR: ficha preliminar; no se comprobó que el truncamiento
    J = floor(n/5) sea el del artículo]:

        1/n_ef = 1/n + (2/n) · sum_{j=1}^{J} ((n - j)/n) · rho_x(j) · rho_y(j),   J = floor(n/5),

    con las ACF muestrales de cada serie. Se acota n_ef <= n; si el denominador no es positivo,
    n_ef = n.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    J = n // 5 if max_rezago is None else max_rezago
    j = np.arange(1, J + 1)
    s = np.sum((n - j) / n * acf(x, j) * acf(y, j))
    inv = 1 / n + 2 / n * s
    if inv <= 0:
        return float(n)
    return float(min(n, 1 / inv))


def prueba_correlacion(r, n_ef, alfa=0.05):
    """
    Prueba t bilateral de H0: rho = 0 con n_ef - 2 grados de libertad (no enteros).
    Con n_ef <= 3 no se evalúa (se devuelve p = NaN y no significativa).
    """
    if n_ef <= 3:
        return np.nan, False
    gl = n_ef - 2
    t = r * np.sqrt(gl / (1 - r ** 2))
    p = 2 * stats.t.sf(abs(t), gl)
    return float(p), bool(p < alfa)


# ---- ADF y KPSS con p-valores de tseries -----------------------------------------------

def p_adf_tseries(estadistico, n_dif):
    """p-valor de tseries::adf.test: interpola la tabla en n (= longitud de diff(x)) y luego en el estadístico."""
    fila = np.array([np.interp(n_dif, _ADF_T, _ADF_TABLA[:, i]) for i in range(_ADF_TABLA.shape[1])])
    return float(np.interp(estadistico, fila, _ADF_P))


def p_kpss_tseries(estadistico):
    """p-valor de tseries::kpss.test (null = "Trend"), acotado a [0,01; 0,10]."""
    return float(np.interp(estadistico, _KPSS_TABLA_TENDENCIA[::-1], _KPSS_P[::-1]))


def adf_ct(x, rezagos=ADF_REZAGOS):
    """ADF con constante y tendencia y rezagos fijos (sin selección automática)."""
    x = np.asarray(x, dtype=float)
    # result_object=False: tupla clásica (estadístico, p, rezagos, nobs, críticos), sin aviso de statsmodels 0.15
    res = adfuller(x, maxlag=rezagos, regression='ct', autolag=None, result_object=False)
    return {'estadistico': float(res[0]), 'p_mackinnon': float(res[1]),
            'p_tseries': p_adf_tseries(res[0], len(x) - 1), 'rezagos': int(res[2])}


def kpss_tendencia(x, rezagos=KPSS_REZAGOS):
    """KPSS con nula de estacionariedad en tendencia y núcleo de Bartlett con rezagos fijos."""
    import warnings
    x = np.asarray(x, dtype=float)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')     # statsmodels avisa cuando el p-valor sale de la tabla
        res = kpss(x, regression='ct', nlags=rezagos)
    return {'estadistico': float(res[0]), 'p_tseries': p_kpss_tseries(res[0]), 'rezagos': int(res[2])}


def clasificar_d5(p_adf, p_kpss, alfa=ALFA_D5):
    """Regla D5: TS si ADF rechaza y KPSS no; DS si ADF no rechaza y KPSS sí; si no, indeterminada."""
    adf_rechaza = p_adf < alfa
    kpss_rechaza = p_kpss < alfa
    if adf_rechaza and not kpss_rechaza:
        return 'TS'
    if (not adf_rechaza) and kpss_rechaza:
        return 'DS'
    return 'indeterminada'


def tendencia_y_residuos(x):
    """
    Regresión x_t = a + b t + e_t (t = 1..n) y diagnóstico de los residuos (regla D5).

    Devuelve un diccionario con la pendiente, el R², la correlación con el tiempo, los residuos,
    la ACF de los residuos (rezagos 1 y 12), Ljung-Box (12 rezagos), ADF y KPSS sobre los
    residuos y la clasificación D5.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    t = np.arange(1, n + 1, dtype=float)
    A = np.column_stack([np.ones(n), t])
    coef, *_ = np.linalg.lstsq(A, x, rcond=None)
    e = x - A @ coef
    r2 = 1 - np.sum(e ** 2) / np.sum((x - x.mean()) ** 2)
    adf = adf_ct(e)
    kp = kpss_tendencia(e)
    # Invariancia: ADF y KPSS con tendencia dan lo mismo sobre x que sobre sus residuos
    assert abs(adf['estadistico'] - adf_ct(x)['estadistico']) < 1e-8
    assert abs(kp['estadistico'] - kpss_tendencia(x)['estadistico']) < 1e-8
    lb = acorr_ljungbox(e, lags=[LJUNG_BOX_REZAGOS], return_df=True)
    a1, a12 = acf(e, [1, 12])
    return {
        'intercepto': float(coef[0]), 'pendiente': float(coef[1]), 'r2': float(r2),
        'r_tiempo': float(np.corrcoef(x, t)[0, 1]), 'residuos': e,
        'acf1_residuos': float(a1), 'acf12_residuos': float(a12),
        'ljung_box_q12': float(lb['lb_stat'].iloc[0]), 'ljung_box_p12': float(lb['lb_pvalue'].iloc[0]),
        'adf_estadistico': adf['estadistico'], 'adf_rezagos': adf['rezagos'],
        'adf_p_tseries': adf['p_tseries'], 'adf_p_mackinnon': adf['p_mackinnon'],
        'kpss_estadistico': kp['estadistico'], 'kpss_rezagos': kp['rezagos'],
        'kpss_p_tseries': kp['p_tseries'],
        'clase_d5': clasificar_d5(adf['p_tseries'], kp['p_tseries']),
    }


def quitar_tendencia(X):
    """Residuos de cada columna de X sobre (1, t): las series sin su tendencia lineal."""
    X = np.asarray(X, dtype=float)
    n = X.shape[0]
    A = np.column_stack([np.ones(n), np.arange(1, n + 1, dtype=float)])
    coef, *_ = np.linalg.lstsq(A, X, rcond=None)
    return X - A @ coef


# ---- Deriva de una serie integrada (nulo mixto, decisión D8, 24-oct-2026) --------------
HAC_REZAGOS = 12       # rezagos del estimador de Newey-West (D8)
UMBRAL_DERIVA = 2.0    # |t| HAC > 2: la serie DS se simula con deriva (D8)


def t_hac_media(d, rezagos=HAC_REZAGOS):
    """
    Estadístico t de la media de los incrementos `d` con error estándar HAC de Newey y West
    (1987) [VERIFICAR: ficha newey_west_1987 con orden de autores y DOI pendientes; los 12
    rezagos y el umbral |t| > 2 son elecciones de la tesis (D8)].

        γ_k = (1/n) Σ_{t=k+1}^{n} (d_t − d̄)(d_{t−k} − d̄),
        Ω   = γ_0 + 2 Σ_{k=1}^{L} (1 − k/(L+1)) γ_k      (núcleo de Bartlett, L = rezagos),
        t   = d̄ / sqrt(Ω / n).

    Sin corrección por grados de libertad. Devuelve (media, error estándar, t).
    """
    d = np.asarray(d, dtype=float)
    n = len(d)
    u = d - d.mean()
    omega = np.sum(u * u) / n
    for k in range(1, rezagos + 1):
        omega += 2 * (1 - k / (rezagos + 1)) * np.sum(u[k:] * u[:-k]) / n
    se = float(np.sqrt(omega / n))
    return float(d.mean()), se, float(d.mean() / se)


def tratamiento_mixto(clase_d5, t_hac, indeterminada_como):
    """
    Regla del nulo mixto (D8), fijada antes de calcular:
      - TS → 'TS' (recta más residuos remuestreados);
      - DS → 'con_deriva' si |t| HAC > 2, 'sin_deriva' en otro caso;
      - indeterminada → se informa con las dos variantes: `indeterminada_como` = 'TS' o 'DS'.
    """
    assert indeterminada_como in ('TS', 'DS')
    clase = clase_d5 if clase_d5 != 'indeterminada' else indeterminada_como
    if clase == 'TS':
        return 'TS'
    return 'con_deriva' if abs(t_hac) > UMBRAL_DERIVA else 'sin_deriva'
