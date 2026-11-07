"""Detección de episodios fuera de muestra con el PCA, sin `torch` (anexo R.b del Rmd final).

Traducción de la parte PCA de la validación *walk-forward* del notebook 09 (sección 2), para poder
recalcularla con 16 series (D16) sin reentrenar los autoencoders:

- para cada año de evaluación a (2011 a 2025, como en el 09), se estandariza con la media y la
  desviación poblacional (divisor n, como `StandardScaler`) de los meses anteriores a enero de a;
- se ajusta un PCA de d = 3 componentes (D9) sobre esos meses estandarizados (centrado en su media,
  como `sklearn.decomposition.PCA`);
- el error de cada mes es el error cuadrático medio de reconstrucción con d componentes, dividido por
  el percentil 95 (tipo 7) del error en los meses de entrenamiento: valores > 1 indican un mes más
  anómalo que el 95 % de lo que el modelo conocía.

La discriminación de episodios usa `src.episodios.discriminacion_episodios` (la regla del 09: razón
mayor que 1), con el archivo único de episodios (D7, D9). `ampliar_episodios` extiende cada episodio
±t meses (tolerancia de D7: 3 meses; 6 como sensibilidad), una lectura propia de esta tarea.
"""

import numpy as np
import pandas as pd

ANIOS = tuple(range(2011, 2026))
D_PCA = 3


def error_walkforward_pca(X, fechas, anios=ANIOS, d=D_PCA):
    """Razón de error walk-forward del PCA por mes (notebook 09, columna `pca`).

    X: matriz n × p sin estandarizar; fechas: n fechas (Timestamp o texto AAAA-MM-DD).
    Devuelve un DataFrame con índice `fecha` y columnas `anio_modelo` y `pca`.
    """
    X = np.asarray(X, dtype=float)
    f = pd.DatetimeIndex(pd.to_datetime(fechas))
    filas = []
    for a in anios:
        ent = f < pd.Timestamp(f'{a}-01-01')
        ev = (f >= pd.Timestamp(f'{a}-01-01')) & (f < pd.Timestamp(f'{a + 1}-01-01'))
        if not ev.any():
            continue
        m = X[ent].mean(axis=0)
        s = X[ent].std(axis=0)                          # divisor n, como StandardScaler
        Xs = (X - m) / s
        E = Xs[ent]
        mu = E.mean(axis=0)
        val, vec = np.linalg.eigh(np.cov(E - mu, rowvar=False, bias=True))
        V = vec[:, np.argsort(val)[::-1][:d]]

        def rec(Z):
            return mu + (Z - mu) @ V @ V.T

        ref = np.percentile(np.mean((E - rec(E)) ** 2, axis=1), 95)
        e = np.mean((Xs[ev] - rec(Xs[ev])) ** 2, axis=1)
        for fecha, v in zip(f[ev], e):
            filas.append({'fecha': fecha, 'anio_modelo': a, 'pca': v / ref})
    return pd.DataFrame(filas).set_index('fecha')


def ampliar_episodios(episodios, tol):
    """Diccionario {nombre: (inicio − tol, fin efectivo + tol)} con fechas AAAA-MM-DD."""
    def mover(x, k):
        return (pd.Timestamp(x) + pd.DateOffset(months=int(k))).strftime('%Y-%m-%d')
    return {r.nombre: (mover(r.inicio_mes, -tol), mover(r.fin_efectivo, tol)) for r in episodios.itertuples()}


def discriminacion_larga(wf, episodios, metodos=('pca',), tol=0, umbral=1.0):
    """Discriminación de episodios en formato largo, con tolerancia de ±tol meses.

    Para cada episodio, sus meses son los de [inicio − tol, fin efectivo + tol]; los meses «fuera de
    episodios» son los que no caen en ningún episodio ampliado. Cada episodio se evalúa por separado
    (si dos episodios ampliados se superponen, el mes cuenta en los dos). Con tol = 0 y episodios
    sin superposición coincide con `src.episodios.discriminacion_episodios` (regla del 09).

    Devuelve un DataFrame con metodo, tolerancia_meses, medida, episodio, meses y valor.
    """
    idx = pd.DatetimeIndex(wf.index)
    amp = ampliar_episodios(episodios, tol)
    mascaras = {nom: (idx >= pd.Timestamp(a)) & (idx <= pd.Timestamp(b)) for nom, (a, b) in amp.items()}
    en_alguno = np.zeros(len(idx), dtype=bool)
    for m in mascaras.values():
        en_alguno |= m
    filas = []
    for metodo in metodos:
        v = wf[metodo].to_numpy(dtype=float)
        fuera = v[~en_alguno]
        filas.append({'metodo': metodo, 'tolerancia_meses': tol, 'medida': 'mediana_fuera_de_episodios',
                      'episodio': '', 'meses': int(len(fuera)), 'valor': float(np.median(fuera))})
        filas.append({'metodo': metodo, 'tolerancia_meses': tol, 'medida': 'falsas_alarmas_%',
                      'episodio': '', 'meses': int(len(fuera)), 'valor': float(100 * np.mean(fuera > umbral))})
        for nom, m in mascaras.items():
            if not m.any():
                continue
            filas.append({'metodo': metodo, 'tolerancia_meses': tol, 'medida': 'mediana', 'episodio': nom,
                          'meses': int(m.sum()), 'valor': float(np.median(v[m]))})
            filas.append({'metodo': metodo, 'tolerancia_meses': tol, 'medida': 'sensibilidad_%', 'episodio': nom,
                          'meses': int(m.sum()), 'valor': float(100 * np.mean(v[m] > umbral))})
    return pd.DataFrame(filas)
